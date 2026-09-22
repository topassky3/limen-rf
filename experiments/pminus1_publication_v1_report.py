#!/usr/bin/env python3
"""Inspect publication-validation V1 outputs without changing the experiment."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "").strip()
    return float("nan") if not value else float(value)


def fmt_ci(row: dict[str, str], stem: str) -> str:
    lo = f(row, f"{stem}_ci_low")
    hi = f(row, f"{stem}_ci_high")
    return f"[{lo:.4f}, {hi:.4f}]"


def method_row(
    rows: list[dict[str, str]],
    k: int,
    condition: str,
    horizon: int,
    method: str,
) -> dict[str, str]:
    matches = [
        r
        for r in rows
        if int(r["K"]) == k
        and r["condition"] == condition
        and int(r["horizon"]) == horizon
        and r["reported_method"] == method
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one row for K={k} condition={condition} "
            f"T={horizon} method={method}, got {len(matches)}"
        )
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        default="results/publication_v1",
        help="Publication V1 output directory",
    )
    args = parser.parse_args()

    root = Path(args.dir)
    summary_path = root / "summary.csv"
    paired_path = root / "paired_differences.csv"
    figures_dir = root / "figures"

    rows = read_csv(summary_path)
    paired = read_csv(paired_path)

    print("=== V1 NULL CHECK ===")
    for k in (24, 32):
        for horizon in (40, 100, 200):
            static = method_row(rows, k, "null", horizon, "static")
            baseline = method_row(
                rows, k, "null", horizon, "best_grid_baseline"
            )
            oracle = method_row(rows, k, "null", horizon, "oracle")
            print(
                f"K={k} T={horizon:3d} "
                f"static={f(static,'cross_rate'):.4f} "
                f"{fmt_ci(static,'cross')} "
                f"baseline={f(baseline,'cross_rate'):.4f} "
                f"{fmt_ci(baseline,'cross')} "
                f"oracle={f(oracle,'cross_rate'):.4f} "
                f"{fmt_ci(oracle,'cross')}"
            )

    print("")
    print("=== V1 T=200 ALTERNATIVE DELAYS ===")
    for k in (24, 32):
        for gamma in (2.0, 4.0, 8.0):
            condition = f"beta_{gamma:g}"
            print(f"K={k} gamma={gamma:g}")
            for method in ("static", "best_grid_baseline", "oracle"):
                row = method_row(rows, k, condition, 200, method)
                delay = row["median_delay_detected"] or "NA"
                delay_ci = (
                    "NA"
                    if not row["delay_ci_low"]
                    else f"[{f(row,'delay_ci_low'):.2f}, "
                         f"{f(row,'delay_ci_high'):.2f}]"
                )
                extra = ""
                if method == "best_grid_baseline":
                    extra = (
                        f" ({row['underlying_method']}, "
                        f"delta={row['delta'] or '-'}, "
                        f"D={row['D'] or '-'})"
                    )
                print(
                    f"  {method:18s} "
                    f"cross={f(row,'cross_rate'):.4f} "
                    f"{fmt_ci(row,'cross')} "
                    f"delay={delay} {delay_ci}"
                    f"{extra}"
                )

    print("")
    print("=== PRIMARY PAIRED GAP ===")
    primary = [
        r
        for r in paired
        if int(r["K"]) == 32
        and r["condition"] == "beta_4"
        and int(r["horizon"]) == 200
    ]
    if len(primary) != 1:
        raise RuntimeError(f"expected one primary paired row, got {len(primary)}")
    p = primary[0]
    print(
        "K=32 gamma=4 T=200 "
        f"static-baseline={f(p,'static_minus_baseline'):.4f} "
        f"[{f(p,'static_minus_baseline_ci_low'):.4f}, "
        f"{f(p,'static_minus_baseline_ci_high'):.4f}] "
        f"oracle-static={f(p,'oracle_minus_static'):.4f} "
        f"[{f(p,'oracle_minus_static_ci_low'):.4f}, "
        f"{f(p,'oracle_minus_static_ci_high'):.4f}]"
    )

    print("")
    print("=== FIGURES ===")
    if figures_dir.exists():
        for path in sorted(figures_dir.iterdir()):
            if path.is_file():
                print(path)
    else:
        print(f"MISSING: {figures_dir}")

    print("")
    print("V1_REPORT: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
