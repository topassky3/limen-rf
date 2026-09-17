#!/usr/bin/env python3
"""P−1 hardware identifiability pilot capture orchestrator.

Stdlib-only so it can run directly on the Orange Pi. Captures fixed-length
RTL-SDR IQ snapshots on a monotonic cadence and records reproducibility metadata.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def thermal_snapshot() -> dict[str, object]:
    out: dict[str, object] = {}
    base = Path("/sys/class/thermal")
    for zone in sorted(base.glob("thermal_zone*")):
        type_path = zone / "type"
        temp_path = zone / "temp"
        if not (type_path.is_file() and temp_path.is_file()):
            continue
        try:
            ztype = type_path.read_text().strip()
            raw = float(temp_path.read_text().strip())
            value_c = raw / 1000.0 if abs(raw) > 200 else raw
            out[f"{zone.name}:{ztype}"] = value_c
        except (OSError, ValueError):
            continue
    return out


def run_text(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, check=False, text=True, capture_output=True)
        return (result.stdout + result.stderr).strip()
    except OSError as exc:
        return f"ERROR: {exc}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", default=str(Path.home() / "limen-rf-captures" / "pilot_open_01"))
    p.add_argument("--rtl-sdr", default="/usr/local/bin/rtl_sdr")
    p.add_argument("--center-freq", type=int, default=300_000_000)
    p.add_argument("--sample-rate", type=int, default=2_048_000)
    p.add_argument("--gain-db", type=float, default=28.0)
    p.add_argument("--capture-seconds", type=float, default=2.0)
    p.add_argument("--cadence-seconds", type=float, default=60.0)
    p.add_argument("--duration-minutes", type=float, default=45.0)
    p.add_argument("--input-condition", default="open")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    outdir = Path(args.output_dir).expanduser().resolve()
    raw_dir = outdir / "raw"
    logs_dir = outdir / "logs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    n_samples = round(args.sample_rate * args.capture_seconds)
    expected_bytes = n_samples * 2
    n_captures = int((args.duration_minutes * 60) // args.cadence_seconds) + 1
    expected_total = expected_bytes * n_captures

    free_bytes = shutil.disk_usage(outdir).free
    if free_bytes < expected_total * 2:
        raise SystemExit(
            f"Insufficient free disk: need at least {expected_total * 2} bytes, have {free_bytes}"
        )

    rtl_path = Path(args.rtl_sdr)
    if not rtl_path.exists():
        raise SystemExit(f"rtl_sdr not found at {rtl_path}")

    metadata = {
        "started_utc": utc_now(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "rtl_sdr_path": str(rtl_path),
        "rtl_sdr_git_commit": run_text(["git", "-C", str(Path.home() / "rtl-sdr"), "rev-parse", "HEAD"]),
        "lsusb": run_text(["lsusb"]),
        "center_freq_hz": args.center_freq,
        "sample_rate_hz": args.sample_rate,
        "gain_db": args.gain_db,
        "capture_seconds": args.capture_seconds,
        "samples_per_capture": n_samples,
        "expected_bytes_per_capture": expected_bytes,
        "cadence_seconds": args.cadence_seconds,
        "duration_minutes": args.duration_minutes,
        "n_captures": n_captures,
        "input_condition": args.input_condition,
        "note": "Exploratory open-input pilot; not equivalent to a 50-ohm terminated null.",
        "thermal_at_start_c": thermal_snapshot(),
    }
    (outdir / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    csv_path = outdir / "metadata.csv"
    fieldnames = [
        "capture_id",
        "scheduled_elapsed_s",
        "actual_elapsed_s",
        "utc_timestamp",
        "filename",
        "size_bytes",
        "expected_bytes",
        "size_ok",
        "sha256",
        "returncode",
        "thermal_json",
        "log_file",
    ]

    start_mono = time.monotonic()
    print(f"RUN START: {metadata['started_utc']}")
    print(f"Output: {outdir}")
    print(f"Captures: {n_captures}; expected raw total ≈ {expected_total / 1e6:.1f} MB")
    print("Do not touch antenna/input, USB, gain, or receiver configuration during the run.")

    with csv_path.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        csvfile.flush()

        for i in range(n_captures):
            target_elapsed = i * args.cadence_seconds
            target_mono = start_mono + target_elapsed
            delay = target_mono - time.monotonic()
            if delay > 0:
                time.sleep(delay)

            actual_elapsed = time.monotonic() - start_mono
            timestamp = utc_now()
            iq_path = raw_dir / f"capture_{i:03d}.iq"
            log_path = logs_dir / f"capture_{i:03d}.log"

            cmd = [
                str(rtl_path),
                "-f",
                str(args.center_freq),
                "-s",
                str(args.sample_rate),
                "-g",
                str(args.gain_db),
                "-n",
                str(n_samples),
                str(iq_path),
            ]

            print(f"[{i + 1:02d}/{n_captures}] t={actual_elapsed:7.2f}s {timestamp}", flush=True)
            result = subprocess.run(cmd, check=False, text=True, capture_output=True)
            log_path.write_text(result.stdout + result.stderr)

            size = iq_path.stat().st_size if iq_path.exists() else -1
            digest = sha256(iq_path) if iq_path.exists() else ""
            row = {
                "capture_id": i,
                "scheduled_elapsed_s": f"{target_elapsed:.3f}",
                "actual_elapsed_s": f"{actual_elapsed:.3f}",
                "utc_timestamp": timestamp,
                "filename": str(iq_path),
                "size_bytes": size,
                "expected_bytes": expected_bytes,
                "size_ok": size == expected_bytes,
                "sha256": digest,
                "returncode": result.returncode,
                "thermal_json": json.dumps(thermal_snapshot(), sort_keys=True),
                "log_file": str(log_path),
            }
            writer.writerow(row)
            csvfile.flush()
            os.fsync(csvfile.fileno())

            if size != expected_bytes or result.returncode != 0:
                print(
                    f"WARNING capture {i}: returncode={result.returncode}, size={size}, expected={expected_bytes}",
                    flush=True,
                )

    finished = {
        "finished_utc": utc_now(),
        "actual_total_elapsed_s": time.monotonic() - start_mono,
        "thermal_at_end_c": thermal_snapshot(),
    }
    (outdir / "run_finished.json").write_text(json.dumps(finished, indent=2) + "\n")
    print("RUN COMPLETE")
    print(f"Metadata: {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
