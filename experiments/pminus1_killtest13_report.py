#!/usr/bin/env python3
"""Report the decisive Kill-Test 13 rows including delay and median log-evidence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


TARGETS = ((24, 4.0), (24, 8.0), (32, 4.0), (32, 8.0))
METHODS = ("static", "oracle", "band_mix", "band_ons", "cctm")


def key(row: dict[str, str]) -> tuple[float, float, float]:
    delay = (
        float(row["median_delay_detected"])
        if row["median_delay_detected"]
        else float("inf")
    )
    return (
        float(row["cross_rate"]),
        -delay,
        float(row["median_loge"]),
    )


def gamma_matches(row: dict[str, str], gamma: float) -> bool:
    """Return False for null rows, whose true_gamma field is intentionally empty."""
    value = row.get("true_gamma", "").strip()
    if not value:
        return False
    return float(value) == gamma


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        default="results/pminus1_killtest13_baseline_strength.csv",
    )
    args = parser.parse_args()

    path = Path(args.csv)
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    for k, gamma in TARGETS:
        subset = [
            r
            for r in rows
            if int(r["K"]) == k
            and gamma_matches(r, gamma)
            and int(r["horizon"]) == 200
        ]

        if not subset:
            raise RuntimeError(
                f"No rows found for K={k}, gamma={gamma:g}, T=200 in {path}"
            )

        print(f"K={k} gamma={gamma:g} T=200")
        for method in METHODS:
            candidates = [r for r in subset if r["method"] == method]
            if not candidates:
                continue
            best = max(candidates, key=key)
            print(
                f"  {method:9s} cross={float(best['cross_rate']):.3f} "
                f"delay={best['median_delay_detected'] or 'NA'} "
                f"med_logE={float(best['median_loge']):.6f} "
                f"delta={best['delta'] or '-'} D={best['D'] or '-'} "
                f"threshold={float(best['threshold']):.3f}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
