#!/usr/bin/env python3
"""Publication validation V1 for the frozen LIMEN-RF method.

This script does NOT tune the detector. It reuses Kill-Test 13 exactly and
only increases Monte Carlo precision, adds uncertainty intervals, paired
comparisons, and publication figures.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import platform
import random
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pminus1_baseline_strength_audit_killtest13 as kt13


PUB_SEED = 20260922
DEFAULT_REPS = 5_000
DEFAULT_BOOTSTRAP = 2_000
DEFAULT_BLOCK_SIZE = 50
CI_LEVEL = 0.95
Z_95 = 1.959963984540054

K_VALUES = kt13.K_VALUES
HORIZONS = kt13.HORIZONS
TRUE_GAMMAS = kt13.TRUE_GAMMAS


@dataclass(frozen=True)
class MethodSpec:
    label: str
    method: str
    delta: float | None = None
    d_bound: float | None = None


STATIC = MethodSpec("static", "static")
ORACLE = MethodSpec("oracle", "oracle")


def baseline_specs() -> tuple[MethodSpec, ...]:
    specs: list[MethodSpec] = []
    for delta in kt13.DELTA_GRID:
        specs.append(MethodSpec("band_mix", "band_mix", delta, None))
        specs.append(MethodSpec("band_ons", "band_ons", delta, None))
        for d_bound in kt13.CCTM_D_GRID:
            specs.append(MethodSpec("cctm", "cctm", delta, d_bound))
    return tuple(specs)


BASELINE_SPECS = baseline_specs()


def scenario_code(gamma: float | None) -> int:
    return 0 if gamma is None else int(round(1000.0 * gamma))


def publication_scenario_seed(k: int, gamma: float | None) -> int:
    return PUB_SEED + 1_000_000 * k + 10_000 * scenario_code(gamma)


def bootstrap_seed(k: int, gamma: float | None, horizon: int, salt: int) -> int:
    return (
        PUB_SEED
        + 100_000_000
        + 1_000_000 * k
        + 10_000 * scenario_code(gamma)
        + 10 * horizon
        + salt
    )


def _simulate_block(
    payload: tuple[int, float | None, tuple[int, ...]],
) -> list[kt13.PathSummary]:
    k, gamma, seeds = payload
    cfg = kt13.base.build_config(k)
    outputs: list[kt13.PathSummary] = []
    for seed in seeds:
        rng = random.Random(seed)
        _clean, ranks = kt13.base.generate_path(cfg, rng, gamma)
        outputs.append(kt13.evaluate_path(cfg, ranks))
    return outputs


def make_path_seeds(k: int, gamma: float | None, reps: int) -> list[int]:
    rng = random.Random(publication_scenario_seed(k, gamma))
    return [rng.randrange(0, 2**63 - 1) for _ in range(reps)]


def chunks(values: list[int], size: int) -> Iterable[tuple[int, ...]]:
    for start in range(0, len(values), size):
        yield tuple(values[start : start + size])


def run_outputs(
    k: int,
    gamma: float | None,
    reps: int,
    workers: int,
    block_size: int,
) -> list[kt13.PathSummary]:
    seeds = make_path_seeds(k, gamma, reps)
    blocks = [(k, gamma, block) for block in chunks(seeds, block_size)]

    condition = "null" if gamma is None else f"beta_{gamma:g}"
    print(
        f"[simulate] K={k} condition={condition} reps={reps} "
        f"workers={workers} blocks={len(blocks)}"
    )

    outputs: list[kt13.PathSummary] = []
    if workers <= 1:
        for index, payload in enumerate(blocks, start=1):
            outputs.extend(_simulate_block(payload))
            print(f"  block {index}/{len(blocks)} complete", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for index, block_outputs in enumerate(
                pool.map(_simulate_block, blocks),
                start=1,
            ):
                outputs.extend(block_outputs)
                print(f"  block {index}/{len(blocks)} complete", flush=True)

    if len(outputs) != reps:
        raise RuntimeError(f"expected {reps} outputs, got {len(outputs)}")
    return outputs


def stop_for(out: kt13.PathSummary, spec: MethodSpec) -> int | None:
    if spec.method == "static":
        return out.static_stop
    if spec.method == "oracle":
        return out.oracle_stop
    key = (spec.method, spec.delta, spec.d_bound)
    return out.baseline_stops[key]


def loge_for(out: kt13.PathSummary, spec: MethodSpec, horizon: int) -> float:
    if spec.method == "static":
        return float(out.static_logs[horizon])
    if spec.method == "oracle":
        return float(out.oracle_logs[horizon])
    key = (spec.method, spec.delta, spec.d_bound)
    return float(out.baseline_logs[key][horizon])


def indicators(
    outputs: list[kt13.PathSummary],
    spec: MethodSpec,
    horizon: int,
) -> np.ndarray:
    return np.asarray(
        [
            int((stop := stop_for(out, spec)) is not None and stop <= horizon)
            for out in outputs
        ],
        dtype=float,
    )


def detected_stops(
    outputs: list[kt13.PathSummary],
    spec: MethodSpec,
    horizon: int,
) -> np.ndarray:
    values = [
        int(stop)
        for out in outputs
        if (stop := stop_for(out, spec)) is not None and stop <= horizon
    ]
    return np.asarray(values, dtype=float)


def terminal_logs(
    outputs: list[kt13.PathSummary],
    spec: MethodSpec,
    horizon: int,
) -> np.ndarray:
    return np.asarray([loge_for(out, spec, horizon) for out in outputs], dtype=float)


def wilson_interval(successes: int, n: int) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    p = successes / n
    z = Z_95
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = (
        z
        * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))
        / denom
    )
    return (max(0.0, center - half), min(1.0, center + half))


def bootstrap_percentile_ci(
    values: np.ndarray,
    statistic: str,
    reps: int,
    seed: int,
) -> tuple[float, float]:
    if values.size == 0:
        return (float("nan"), float("nan"))
    if values.size == 1 or reps <= 0:
        value = float(values[0])
        return (value, value)

    rng = np.random.default_rng(seed)
    sampled_stats = np.empty(reps, dtype=float)
    chunk = 64

    for start in range(0, reps, chunk):
        count = min(chunk, reps - start)
        idx = rng.integers(0, values.size, size=(count, values.size))
        sampled = values[idx]
        if statistic == "median":
            sampled_stats[start : start + count] = np.median(sampled, axis=1)
        elif statistic == "mean":
            sampled_stats[start : start + count] = np.mean(sampled, axis=1)
        else:
            raise ValueError(f"unknown statistic: {statistic}")

    alpha = 1.0 - CI_LEVEL
    lo, hi = np.quantile(sampled_stats, [alpha / 2.0, 1.0 - alpha / 2.0])
    return (float(lo), float(hi))


def basic_score(
    outputs: list[kt13.PathSummary],
    spec: MethodSpec,
    horizon: int,
) -> tuple[float, float, float]:
    ind = indicators(outputs, spec, horizon)
    stops = detected_stops(outputs, spec, horizon)
    logs = terminal_logs(outputs, spec, horizon)
    cross = float(ind.mean())
    delay = float(np.median(stops)) if stops.size else float("inf")
    med_loge = float(np.median(logs))
    return (cross, -delay, med_loge)


def strongest_baseline(
    outputs: list[kt13.PathSummary],
    horizon: int,
) -> MethodSpec:
    return max(BASELINE_SPECS, key=lambda spec: basic_score(outputs, spec, horizon))


def detailed_stats(
    outputs: list[kt13.PathSummary],
    spec: MethodSpec,
    horizon: int,
    boot_reps: int,
    boot_seed: int,
) -> dict[str, float | int | str]:
    ind = indicators(outputs, spec, horizon)
    stops = detected_stops(outputs, spec, horizon)
    logs = terminal_logs(outputs, spec, horizon)

    successes = int(ind.sum())
    n = int(ind.size)
    cross = successes / n
    cross_lo, cross_hi = wilson_interval(successes, n)

    if stops.size:
        median_delay = float(np.median(stops))
        delay_lo, delay_hi = bootstrap_percentile_ci(
            stops,
            "median",
            boot_reps,
            boot_seed,
        )
    else:
        median_delay = float("nan")
        delay_lo = float("nan")
        delay_hi = float("nan")

    if spec.delta is None:
        threshold = 1.0 / kt13.ALPHA
    else:
        cond_alpha = (kt13.ALPHA - spec.delta) / (1.0 - spec.delta)
        threshold = 1.0 / cond_alpha

    return {
        "cross_count": successes,
        "cross_rate": cross,
        "cross_ci_low": cross_lo,
        "cross_ci_high": cross_hi,
        "median_delay_detected": median_delay,
        "delay_ci_low": delay_lo,
        "delay_ci_high": delay_hi,
        "median_loge": float(np.median(logs)),
        "threshold": threshold,
    }


def paired_difference(
    a: np.ndarray,
    b: np.ndarray,
    boot_reps: int,
    seed: int,
) -> tuple[float, float, float]:
    if a.shape != b.shape:
        raise ValueError("paired arrays must have identical shapes")
    diff = a - b
    estimate = float(diff.mean())
    lo, hi = bootstrap_percentile_ci(diff, "mean", boot_reps, seed)
    return estimate, lo, hi


def fmt_float(value: float) -> str | float:
    return "" if not math.isfinite(value) else value


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=HERE.parent,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def condition_name(gamma: float | None) -> str:
    return "null" if gamma is None else f"beta_{gamma:g}"


def label_for_plot(method: str) -> str:
    return {
        "static": "Static coupling",
        "best_grid_baseline": "Best-grid baseline",
        "oracle": "Oracle",
    }[method]


def make_figures(summary_rows: list[dict[str, object]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    for k in K_VALUES:
        rows = [
            row
            for row in summary_rows
            if int(row["K"]) == k
            and int(row["horizon"]) == 200
            and row["true_gamma"] != ""
            and row["reported_method"]
            in {"static", "best_grid_baseline", "oracle"}
        ]

        fig, ax = plt.subplots(figsize=(7.0, 4.6))
        for method in ("static", "best_grid_baseline", "oracle"):
            selected = sorted(
                [row for row in rows if row["reported_method"] == method],
                key=lambda row: float(row["true_gamma"]),
            )
            x = np.asarray([float(row["true_gamma"]) for row in selected])
            y = np.asarray([float(row["cross_rate"]) for row in selected])
            lo = np.asarray([float(row["cross_ci_low"]) for row in selected])
            hi = np.asarray([float(row["cross_ci_high"]) for row in selected])
            yerr = np.vstack((y - lo, hi - y))
            ax.errorbar(
                x,
                y,
                yerr=yerr,
                marker="o",
                capsize=3,
                label=label_for_plot(method),
            )

        ax.set_xlabel(r"Alternative strength $\gamma$ in Beta($\gamma$,1)")
        ax.set_ylabel("Crossing probability by T=200")
        ax.set_ylim(-0.02, 1.02)
        ax.set_xticks([2.0, 4.0, 8.0])
        ax.grid(True, alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(outdir / f"crossing_T200_K{k}.pdf")
        fig.savefig(outdir / f"crossing_T200_K{k}.png", dpi=180)
        plt.close(fig)

    k = 32
    rows = [
        row
        for row in summary_rows
        if int(row["K"]) == k
        and int(row["horizon"]) == 200
        and row["true_gamma"] != ""
        and row["reported_method"] in {"static", "best_grid_baseline", "oracle"}
    ]

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for method in ("static", "best_grid_baseline", "oracle"):
        selected = sorted(
            [
                row
                for row in rows
                if row["reported_method"] == method
                and row["median_delay_detected"] != ""
            ],
            key=lambda row: float(row["true_gamma"]),
        )
        if not selected:
            continue
        x = np.asarray([float(row["true_gamma"]) for row in selected])
        y = np.asarray([float(row["median_delay_detected"]) for row in selected])
        lo = np.asarray([float(row["delay_ci_low"]) for row in selected])
        hi = np.asarray([float(row["delay_ci_high"]) for row in selected])
        yerr = np.vstack((y - lo, hi - y))
        ax.errorbar(
            x,
            y,
            yerr=yerr,
            marker="o",
            capsize=3,
            label=label_for_plot(method),
        )

    ax.set_xlabel(r"Alternative strength $\gamma$ in Beta($\gamma$,1)")
    ax.set_ylabel("Median stopping time among detected paths")
    ax.set_xticks([2.0, 4.0, 8.0])
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "delay_T200_K32.pdf")
    fig.savefig(outdir / "delay_T200_K32.png", dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=DEFAULT_REPS)
    parser.add_argument("--bootstrap-reps", type=int, default=DEFAULT_BOOTSTRAP)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument("--block-size", type=int, default=DEFAULT_BLOCK_SIZE)
    parser.add_argument(
        "--output-dir",
        default="results/publication_v1",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.reps <= 0:
        raise SystemExit("--reps must be positive")
    if args.bootstrap_reps < 0:
        raise SystemExit("--bootstrap-reps must be nonnegative")
    if args.workers <= 0:
        raise SystemExit("--workers must be positive")
    if args.block_size <= 0:
        raise SystemExit("--block-size must be positive")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("LIMEN-RF publication validation V1")
    print("FROZEN detector: Kill-Test 13 implementation reused without retuning")
    print(
        f"reps={args.reps} bootstrap_reps={args.bootstrap_reps} "
        f"workers={args.workers} block_size={args.block_size}"
    )
    print(
        f"K={K_VALUES} horizons={HORIZONS} gammas={TRUE_GAMMAS} "
        f"alpha={kt13.ALPHA}"
    )
    print("")

    summary_rows: list[dict[str, object]] = []
    paired_rows: list[dict[str, object]] = []

    for k in K_VALUES:
        for gamma in TRUE_GAMMAS:
            outputs = run_outputs(
                k,
                gamma,
                args.reps,
                args.workers,
                args.block_size,
            )

            for horizon in HORIZONS:
                strongest = strongest_baseline(outputs, horizon)

                reported = (
                    ("static", STATIC),
                    ("best_grid_baseline", strongest),
                    ("oracle", ORACLE),
                )

                for offset, (reported_name, spec) in enumerate(reported, start=1):
                    stats = detailed_stats(
                        outputs,
                        spec,
                        horizon,
                        args.bootstrap_reps,
                        bootstrap_seed(k, gamma, horizon, offset),
                    )
                    summary_rows.append(
                        {
                            "K": k,
                            "M": kt13.M,
                            "condition": condition_name(gamma),
                            "true_gamma": "" if gamma is None else gamma,
                            "horizon": horizon,
                            "reps": args.reps,
                            "reported_method": reported_name,
                            "underlying_method": spec.method,
                            "delta": "" if spec.delta is None else spec.delta,
                            "D": "" if spec.d_bound is None else spec.d_bound,
                            **{
                                key: fmt_float(float(value))
                                if isinstance(value, float)
                                else value
                                for key, value in stats.items()
                            },
                        }
                    )

                static_ind = indicators(outputs, STATIC, horizon)
                baseline_ind = indicators(outputs, strongest, horizon)
                oracle_ind = indicators(outputs, ORACLE, horizon)

                sb, sb_lo, sb_hi = paired_difference(
                    static_ind,
                    baseline_ind,
                    args.bootstrap_reps,
                    bootstrap_seed(k, gamma, horizon, 11),
                )
                os_gap, os_lo, os_hi = paired_difference(
                    oracle_ind,
                    static_ind,
                    args.bootstrap_reps,
                    bootstrap_seed(k, gamma, horizon, 12),
                )

                paired_rows.append(
                    {
                        "K": k,
                        "M": kt13.M,
                        "condition": condition_name(gamma),
                        "true_gamma": "" if gamma is None else gamma,
                        "horizon": horizon,
                        "reps": args.reps,
                        "baseline_method": strongest.method,
                        "baseline_delta": strongest.delta,
                        "baseline_D": ""
                        if strongest.d_bound is None
                        else strongest.d_bound,
                        "static_minus_baseline": sb,
                        "static_minus_baseline_ci_low": sb_lo,
                        "static_minus_baseline_ci_high": sb_hi,
                        "oracle_minus_static": os_gap,
                        "oracle_minus_static_ci_low": os_lo,
                        "oracle_minus_static_ci_high": os_hi,
                    }
                )

            del outputs

    summary_path = outdir / "summary.csv"
    paired_path = outdir / "paired_differences.csv"
    write_csv(summary_path, summary_rows)
    write_csv(paired_path, paired_rows)

    manifest = {
        "status": "post-freeze publication validation",
        "detector_source": "Kill-Test 13",
        "git_commit": git_commit(),
        "publication_seed": PUB_SEED,
        "reps": args.reps,
        "bootstrap_reps": args.bootstrap_reps,
        "workers": args.workers,
        "block_size": args.block_size,
        "K_values": list(K_VALUES),
        "M": kt13.M,
        "horizons": list(HORIZONS),
        "true_gammas": [None if g is None else g for g in TRUE_GAMMAS],
        "alpha": kt13.ALPHA,
        "delta_grid": list(kt13.DELTA_GRID),
        "cctm_D_grid": list(kt13.CCTM_D_GRID),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "note": (
            "Best-grid baseline remains an ex-post adversarial benchmark; "
            "it is not one precommitted level-alpha procedure."
        ),
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    make_figures(summary_rows, outdir / "figures")

    print("")
    print("=== PUBLICATION V1 PRIMARY T=200 ===")
    for k in K_VALUES:
        for gamma in (2.0, 4.0, 8.0):
            rows = [
                row
                for row in summary_rows
                if row["K"] == k
                and row["true_gamma"] == gamma
                and row["horizon"] == 200
            ]
            by_method = {row["reported_method"]: row for row in rows}
            static = by_method["static"]
            baseline = by_method["best_grid_baseline"]
            oracle = by_method["oracle"]
            pair = next(
                row
                for row in paired_rows
                if row["K"] == k
                and row["true_gamma"] == gamma
                and row["horizon"] == 200
            )
            print(
                f"K={k} gamma={gamma:g} "
                f"static={float(static['cross_rate']):.4f} "
                f"[{float(static['cross_ci_low']):.4f},"
                f"{float(static['cross_ci_high']):.4f}] "
                f"baseline={float(baseline['cross_rate']):.4f} "
                f"({baseline['underlying_method']},"
                f"d={baseline['delta'] or '-'},D={baseline['D'] or '-'}) "
                f"oracle={float(oracle['cross_rate']):.4f} "
                f"paired_gap={float(pair['static_minus_baseline']):.4f} "
                f"[{float(pair['static_minus_baseline_ci_low']):.4f},"
                f"{float(pair['static_minus_baseline_ci_high']):.4f}]"
            )

    print("")
    print(f"summary: {summary_path}")
    print(f"paired:  {paired_path}")
    print(f"figures: {outdir / 'figures'}")
    print(f"manifest:{outdir / 'manifest.json'}")
    print("PUBLICATION_V1: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
