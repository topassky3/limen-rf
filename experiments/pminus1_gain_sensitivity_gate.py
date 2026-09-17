#!/usr/bin/env python3
"""Short gain-sensitivity gate for the P−1 RTL-SDR hardware pilot."""

from __future__ import annotations

import argparse
import csv
import subprocess
import tempfile
from pathlib import Path

import numpy as np

GAINS_DB = [28.0, 32.8, 38.6, 43.9, 49.6]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--rtl-sdr", default="/usr/local/bin/rtl_sdr")
    p.add_argument("--center-freq", type=int, default=300_000_000)
    p.add_argument("--sample-rate", type=int, default=2_048_000)
    p.add_argument("--seconds", type=float, default=1.0)
    p.add_argument("--repetitions", type=int, default=2)
    p.add_argument("--min-std", type=float, default=4.0)
    p.add_argument("--output", default=str(Path.home() / "limen-rf-captures" / "gain_sensitivity_gate.csv"))
    return p.parse_args()


def stats(path: Path) -> dict[str, float | int]:
    raw = np.fromfile(path, dtype=np.uint8)
    if raw.size % 2:
        raise ValueError(f"odd byte count in {path}")
    iq = raw.reshape(-1, 2)
    i = iq[:, 0]
    q = iq[:, 1]
    clip = (i <= 1) | (i >= 254) | (q <= 1) | (q >= 254)
    return {
        "n_complex": int(i.size),
        "i_mean": float(i.mean()),
        "q_mean": float(q.mean()),
        "i_std": float(i.std()),
        "q_std": float(q.std()),
        "i_central_fraction": float(np.mean((i == 127) | (i == 128))),
        "q_central_fraction": float(np.mean((q == 127) | (q == 128))),
        "i_min": int(i.min()),
        "i_max": int(i.max()),
        "q_min": int(q.min()),
        "q_max": int(q.max()),
        "clipping_fraction": float(clip.mean()),
    }


def main() -> int:
    args = parse_args()
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    n_samples = round(args.sample_rate * args.seconds)
    expected_bytes = 2 * n_samples
    rows: list[dict[str, object]] = []

    print("P−1 gain-sensitivity gate")
    print(f"center={args.center_freq} Hz sample_rate={args.sample_rate} S/s")
    print(f"criterion: min(std_I,std_Q) >= {args.min_std:.1f} and clipping_fraction == 0")

    with tempfile.TemporaryDirectory(prefix="limen_gain_gate_") as td:
        tdir = Path(td)
        for gain in GAINS_DB:
            for rep in range(1, args.repetitions + 1):
                iq_path = tdir / f"g{gain:.1f}_r{rep}.iq"
                cmd = [
                    args.rtl_sdr,
                    "-f", str(args.center_freq),
                    "-s", str(args.sample_rate),
                    "-g", f"{gain:.1f}",
                    "-n", str(n_samples),
                    str(iq_path),
                ]
                result = subprocess.run(cmd, check=False, text=True, capture_output=True)
                size = iq_path.stat().st_size if iq_path.exists() else -1
                row: dict[str, object] = {
                    "gain_db": gain,
                    "repetition": rep,
                    "returncode": result.returncode,
                    "size_bytes": size,
                    "expected_bytes": expected_bytes,
                    "size_ok": size == expected_bytes,
                }
                if size == expected_bytes:
                    row.update(stats(iq_path))
                    row["pass"] = (
                        result.returncode == 0
                        and min(float(row["i_std"]), float(row["q_std"])) >= args.min_std
                        and float(row["clipping_fraction"]) == 0.0
                    )
                else:
                    row.update({
                        "n_complex": 0,
                        "i_mean": float("nan"), "q_mean": float("nan"),
                        "i_std": float("nan"), "q_std": float("nan"),
                        "i_central_fraction": float("nan"), "q_central_fraction": float("nan"),
                        "i_min": -1, "i_max": -1, "q_min": -1, "q_max": -1,
                        "clipping_fraction": float("nan"), "pass": False,
                    })
                rows.append(row)
                print(
                    f"gain={gain:4.1f} rep={rep} "
                    f"stdI={float(row['i_std']):7.3f} stdQ={float(row['q_std']):7.3f} "
                    f"centralI={float(row['i_central_fraction']):.4f} "
                    f"centralQ={float(row['q_central_fraction']):.4f} "
                    f"clip={float(row['clipping_fraction']):.3g} PASS={row['pass']}"
                )

    fieldnames = list(rows[0].keys())
    with output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    passing: list[float] = []
    for gain in GAINS_DB:
        subset = [r for r in rows if float(r["gain_db"]) == gain]
        if len(subset) == args.repetitions and all(bool(r["pass"]) for r in subset):
            passing.append(gain)

    print("\n=== GATE RESULT ===")
    if passing:
        print(f"PASS: lowest eligible gain = {min(passing):.1f} dB")
    else:
        print("FAIL: no tested gain met the frozen sensitivity criterion")
    print(f"CSV: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
