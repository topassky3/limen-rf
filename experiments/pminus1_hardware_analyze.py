#!/usr/bin/env python3
"""Analyze the P−1 RTL-SDR hardware-identifiability pilot.

Requires numpy. The first-pass analysis is frozen in
`docs/experiments/pminus1_hardware_analysis_plan_v0.1.md`.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--run-dir",
        default=str(Path.home() / "limen-rf-captures" / "pilot_open_01"),
    )
    p.add_argument("--block-size", type=int, default=4096)
    p.add_argument("--baseline-captures", type=int, default=5)
    p.add_argument("--alpha", type=float, default=0.01)
    return p.parse_args()


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n <= 0:
        return float("nan"), float("nan")
    phat = k / n
    denom = 1.0 + z * z / n
    center = (phat + z * z / (2.0 * n)) / denom
    half = z * math.sqrt(phat * (1.0 - phat) / n + z * z / (4.0 * n * n)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def quantile_higher(x: np.ndarray, q: float) -> float:
    return float(np.quantile(x, q, method="higher"))


def load_metadata(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["capture_id"]))
    return rows


def analyze_iq(path: Path, block_size: int) -> dict[str, object]:
    raw = np.fromfile(path, dtype=np.uint8)
    if raw.size % 2:
        raise ValueError(f"odd byte count in {path}")

    iq = raw.reshape(-1, 2).astype(np.float32)
    i = iq[:, 0] - 127.5
    q = iq[:, 1] - 127.5

    n = i.size
    if n % block_size:
        raise ValueError(f"sample count {n} not divisible by block size {block_size}")

    i_mean = float(i.mean())
    q_mean = float(q.mean())

    raw_power = i * i + q * q
    i_dc = i - i_mean
    q_dc = q - q_mean
    dc_power = i_dc * i_dc + q_dc * q_dc

    blocks_raw = raw_power.reshape(-1, block_size).mean(axis=1)
    blocks_dc = dc_power.reshape(-1, block_size).mean(axis=1)

    clip = (
        (iq[:, 0] <= 1)
        | (iq[:, 0] >= 254)
        | (iq[:, 1] <= 1)
        | (iq[:, 1] >= 254)
    )

    q25, q75 = np.quantile(blocks_dc, [0.25, 0.75])
    mean_block_dc = float(blocks_dc.mean())
    std_block_dc = float(blocks_dc.std(ddof=1))

    return {
        "n_complex": int(n),
        "n_blocks": int(blocks_dc.size),
        "i_mean_adc_centered": i_mean,
        "q_mean_adc_centered": q_mean,
        "mean_power_raw": float(raw_power.mean()),
        "mean_power_dc_removed": float(dc_power.mean()),
        "median_block_power_dc_removed": float(np.median(blocks_dc)),
        "iqr_block_power_dc_removed": float(q75 - q25),
        "cv_block_power_dc_removed": std_block_dc / mean_block_dc if mean_block_dc > 0 else float("nan"),
        "clipping_fraction": float(clip.mean()),
        "blocks_dc": blocks_dc,
        "blocks_raw": blocks_raw,
    }


def main() -> int:
    args = parse_args()
    run_dir = Path(args.run_dir).expanduser().resolve()
    metadata_path = run_dir / "metadata.csv"
    if not metadata_path.exists():
        raise SystemExit(f"missing metadata: {metadata_path}")

    rows = load_metadata(metadata_path)
    if not rows:
        raise SystemExit("metadata.csv has no rows")

    integrity_errors: list[str] = []
    analyses: list[dict[str, object]] = []

    print(f"Analyzing {len(rows)} captures from {run_dir}")

    for row in rows:
        cid = int(row["capture_id"])
        iq_path = Path(row["filename"])
        expected = int(row["expected_bytes"])
        recorded_size = int(row["size_bytes"])
        returncode = int(row["returncode"])

        if not iq_path.exists():
            integrity_errors.append(f"capture {cid}: missing {iq_path}")
            continue
        actual_size = iq_path.stat().st_size
        if actual_size != expected or recorded_size != expected:
            integrity_errors.append(
                f"capture {cid}: size actual={actual_size}, recorded={recorded_size}, expected={expected}"
            )
        if row["size_ok"].strip().lower() != "true":
            integrity_errors.append(f"capture {cid}: metadata size_ok={row['size_ok']}")
        if returncode != 0:
            integrity_errors.append(f"capture {cid}: returncode={returncode}")

        a = analyze_iq(iq_path, args.block_size)
        a["capture_id"] = cid
        a["actual_elapsed_s"] = float(row["actual_elapsed_s"])
        a["utc_timestamp"] = row["utc_timestamp"]
        a["thermal_json"] = row["thermal_json"]
        a["sha256"] = row["sha256"]
        analyses.append(a)
        print(f"  capture {cid:03d}: median power={a['median_block_power_dc_removed']:.6g}")

    if len(analyses) != len(rows):
        integrity_errors.append(f"analyzed {len(analyses)} of {len(rows)} metadata rows")

    if len(analyses) < args.baseline_captures:
        raise SystemExit("not enough valid captures for baseline")

    baseline = analyses[: args.baseline_captures]
    baseline_blocks = np.concatenate([a["blocks_dc"] for a in baseline])
    baseline_location = float(np.median(baseline_blocks))
    stale_threshold = quantile_higher(baseline_blocks, 1.0 - args.alpha)

    baseline_norm_blocks = np.concatenate(
        [
            a["blocks_dc"] / float(np.median(a["blocks_dc"]))
            for a in baseline
        ]
    )
    local_threshold = quantile_higher(baseline_norm_blocks, 1.0 - args.alpha)

    summary_rows: list[dict[str, object]] = []
    for a in analyses:
        blocks = a["blocks_dc"]
        median_power = float(np.median(blocks))
        delta_db = 10.0 * math.log10(median_power / baseline_location)

        stale_hits = int(np.count_nonzero(blocks > stale_threshold))
        stale_pfa = stale_hits / blocks.size
        stale_lo, stale_hi = wilson_interval(stale_hits, int(blocks.size))

        norm_blocks = blocks / median_power
        local_hits = int(np.count_nonzero(norm_blocks > local_threshold))
        local_pfa = local_hits / norm_blocks.size
        local_lo, local_hi = wilson_interval(local_hits, int(norm_blocks.size))

        summary_rows.append(
            {
                "capture_id": a["capture_id"],
                "elapsed_s": f"{a['actual_elapsed_s']:.3f}",
                "elapsed_min": f"{a['actual_elapsed_s'] / 60.0:.3f}",
                "utc_timestamp": a["utc_timestamp"],
                "n_complex": a["n_complex"],
                "n_blocks": a["n_blocks"],
                "i_mean_adc_centered": f"{a['i_mean_adc_centered']:.9g}",
                "q_mean_adc_centered": f"{a['q_mean_adc_centered']:.9g}",
                "mean_power_raw": f"{a['mean_power_raw']:.9g}",
                "mean_power_dc_removed": f"{a['mean_power_dc_removed']:.9g}",
                "median_block_power_dc_removed": f"{median_power:.9g}",
                "delta_db_vs_baseline": f"{delta_db:.9g}",
                "iqr_block_power_dc_removed": f"{a['iqr_block_power_dc_removed']:.9g}",
                "cv_block_power_dc_removed": f"{a['cv_block_power_dc_removed']:.9g}",
                "clipping_fraction": f"{a['clipping_fraction']:.9g}",
                "stale_hits": stale_hits,
                "stale_pfa": f"{stale_pfa:.9g}",
                "stale_pfa_wilson_low": f"{stale_lo:.9g}",
                "stale_pfa_wilson_high": f"{stale_hi:.9g}",
                "localnorm_hits": local_hits,
                "localnorm_pfa": f"{local_pfa:.9g}",
                "localnorm_pfa_wilson_low": f"{local_lo:.9g}",
                "localnorm_pfa_wilson_high": f"{local_hi:.9g}",
                "thermal_json": a["thermal_json"],
                "sha256": a["sha256"],
            }
        )

    out_csv = run_dir / "analysis_summary.csv"
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    deltas = np.array([float(r["delta_db_vs_baseline"]) for r in summary_rows])
    stale = np.array([float(r["stale_pfa"]) for r in summary_rows])
    local = np.array([float(r["localnorm_pfa"]) for r in summary_rows])
    clipping = np.array([float(r["clipping_fraction"]) for r in summary_rows])

    report = {
        "run_dir": str(run_dir),
        "capture_count": len(rows),
        "analyzed_count": len(analyses),
        "integrity_pass": not integrity_errors,
        "integrity_errors": integrity_errors,
        "block_size_complex": args.block_size,
        "blocks_per_capture": int(analyses[0]["n_blocks"]),
        "baseline_capture_ids": [int(a["capture_id"]) for a in baseline],
        "baseline_block_count": int(baseline_blocks.size),
        "alpha0": args.alpha,
        "baseline_median_block_power_dc_removed": baseline_location,
        "stale_threshold": stale_threshold,
        "local_normalized_threshold": local_threshold,
        "delta_db_min": float(deltas.min()),
        "delta_db_max": float(deltas.max()),
        "delta_db_final": float(deltas[-1]),
        "stale_pfa_min": float(stale.min()),
        "stale_pfa_max": float(stale.max()),
        "stale_pfa_final": float(stale[-1]),
        "localnorm_pfa_min": float(local.min()),
        "localnorm_pfa_max": float(local.max()),
        "localnorm_pfa_final": float(local[-1]),
        "max_clipping_fraction": float(clipping.max()),
        "interpretation_guardrail": (
            "Run 1 is exploratory and open-input. It cannot establish repeatability or publication novelty."
        ),
    }
    out_json = run_dir / "analysis_report.json"
    out_json.write_text(json.dumps(report, indent=2) + "\n")

    print("\n=== INTEGRITY ===")
    print("PASS" if not integrity_errors else "FAIL")
    for err in integrity_errors:
        print(f"- {err}")
    print("\n=== FROZEN FIRST-PASS SUMMARY ===")
    print(f"baseline captures: {report['baseline_capture_ids']}")
    print(f"baseline blocks: {report['baseline_block_count']}")
    print(f"delta dB range: {report['delta_db_min']:.6f} .. {report['delta_db_max']:.6f}")
    print(f"delta dB final: {report['delta_db_final']:.6f}")
    print(f"stale PFA range: {report['stale_pfa_min']:.6f} .. {report['stale_pfa_max']:.6f}")
    print(f"stale PFA final: {report['stale_pfa_final']:.6f}")
    print(f"local-normalized PFA range: {report['localnorm_pfa_min']:.6f} .. {report['localnorm_pfa_max']:.6f}")
    print(f"local-normalized PFA final: {report['localnorm_pfa_final']:.6f}")
    print(f"max clipping fraction: {report['max_clipping_fraction']:.9g}")
    print(f"CSV: {out_csv}")
    print(f"JSON: {out_json}")
    return 0 if not integrity_errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
