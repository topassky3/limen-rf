#!/usr/bin/env python3
"""Publication validation V1b: frozen contamination-geometry stress test.

Preregistered in:
docs/experiments/publication_validation_v1b_geometry_runbook.md

This script changes contamination geometry only. The LIMEN-RF detector,
bettor portfolio, thresholds, baseline grid, clean/null model, alternatives,
and horizons remain frozen.

IMPORTANT:
- G0 must reproduce Publication V1 under the same per-path seeds.
- The oracle true candidate is computed dynamically for every replication.
- The primary comparator is precommitted band_mix, delta=0.045.
- The full Kill-Test 13 best-grid envelope is secondary/descriptive.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
import os
import platform
import random
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pminus1_baseline_strength_audit_killtest13 as kt13
import pminus1_publication_validation_v1 as pubv1


K = 32
M = 2
N = K - M
HORIZONS = (40, 100, 200)
MAX_T = 200
TRUE_GAMMAS: tuple[float | None, ...] = (None, 2.0, 4.0, 8.0)

DEFAULT_REPS = 5_000
DEFAULT_BOOTSTRAP = 2_000
DEFAULT_BLOCK_SIZE = 25

V1B_CONTAM_SEED = 20260928
SMOKE_SEED_SALT = 900_000_000

GEOMETRIES = (
    "high_outside",
    "upper_inside",
    "mixed_inside",
    "random_static_inside",
)

GEOMETRY_INDEX = {name: i for i, name in enumerate(GEOMETRIES)}

PRIMARY_BASELINE = pubv1.MethodSpec(
    "primary_baseline",
    "band_mix",
    0.045,
    None,
)

STATIC = pubv1.STATIC
ORACLE = pubv1.ORACLE
BASELINE_SPECS = pubv1.BASELINE_SPECS


@dataclass(frozen=True)
class PathRecord:
    rep_index: int
    path_seed: int
    geometry: str
    contaminants: tuple[float, float]
    true_positions: tuple[int, int]
    output: kt13.PathSummary


def condition_name(gamma: float | None) -> str:
    return "null" if gamma is None else f"beta_{gamma:g}"


def scenario_code(gamma: float | None) -> int:
    return pubv1.scenario_code(gamma)


def v1_path_seeds(gamma: float | None, reps: int, smoke: bool) -> list[int]:
    if not smoke:
        return pubv1.make_path_seeds(K, gamma, reps)

    rng = random.Random(
        pubv1.publication_scenario_seed(K, gamma) + SMOKE_SEED_SALT
    )
    return [rng.randrange(0, 2**63 - 1) for _ in range(reps)]


def contam_seed(gamma: float | None, rep_index: int, smoke: bool) -> int:
    salt = SMOKE_SEED_SALT if smoke else 0
    return (
        V1B_CONTAM_SEED
        + salt
        + 100_000 * scenario_code(gamma)
        + rep_index
    )


def generate_clean_stream(
    seed: int,
    gamma: float | None,
    cfg: kt13.base.Config,
) -> tuple[list[float], list[float]]:
    """Reproduce Publication V1 clean/stream RNG order exactly."""
    rng = random.Random(seed)
    clean = sorted(rng.random() for _ in range(cfg.n))

    if gamma is None:
        stream = [rng.random() for _ in range(MAX_T)]
    else:
        stream = [rng.betavariate(gamma, 1.0) for _ in range(MAX_T)]

    return clean, stream


def contaminants_for(
    geometry: str,
    gamma: float | None,
    rep_index: int,
    smoke: bool,
) -> tuple[float, float]:
    if geometry == "high_outside":
        return (2.0, 2.0)
    if geometry == "upper_inside":
        return (0.85, 0.95)
    if geometry == "mixed_inside":
        return (0.10, 0.90)
    if geometry == "random_static_inside":
        rng = random.Random(contam_seed(gamma, rep_index, smoke))
        return (
            rng.betavariate(0.5, 0.5),
            rng.betavariate(0.5, 0.5),
        )
    raise ValueError(f"unknown geometry: {geometry}")


def detector_inputs(
    clean: list[float],
    stream: list[float],
    contaminants: tuple[float, float],
) -> tuple[list[int], tuple[int, int]]:
    if len(clean) != N:
        raise ValueError(f"expected {N} clean references, got {len(clean)}")

    tagged: list[tuple[float, bool, int]] = [
        (float(value), False, i)
        for i, value in enumerate(clean)
    ]
    tagged.extend(
        (float(value), True, N + j)
        for j, value in enumerate(contaminants)
    )

    # Deterministic tie policy. Clean/contaminated exact ties have probability
    # zero under the continuous Model-A clean system, but ordering is explicit.
    tagged.sort(key=lambda item: (item[0], item[1], item[2]))

    true_positions = tuple(
        i + 1
        for i, (_, is_bad, _) in enumerate(tagged)
        if is_bad
    )
    if len(true_positions) != M:
        raise RuntimeError(
            f"expected {M} contaminated positions, got {true_positions}"
        )

    observed = [float(value) for value, _, _ in tagged]
    ranks = [bisect.bisect_right(observed, float(x)) for x in stream]

    return ranks, (int(true_positions[0]), int(true_positions[1]))


def assert_g0_path_regression(
    cfg: kt13.base.Config,
    seed: int,
    gamma: float | None,
    clean: list[float],
    ranks: list[int],
) -> None:
    """G0 must reproduce the original Publication V1 path exactly."""
    rng = random.Random(seed)
    ref_clean, ref_ranks = kt13.base.generate_path(cfg, rng, gamma)

    if clean != ref_clean:
        raise AssertionError(
            "G0 regression failed: clean reference differs from Publication V1"
        )
    if ranks != ref_ranks:
        raise AssertionError(
            "G0 regression failed: rank path differs from Publication V1"
        )


def evaluate_geometry(
    cfg_base: kt13.base.Config,
    rep_index: int,
    path_seed: int,
    gamma: float | None,
    geometry: str,
    clean: list[float],
    stream: list[float],
    smoke: bool,
) -> PathRecord:
    contaminants = contaminants_for(geometry, gamma, rep_index, smoke)
    ranks, true_positions = detector_inputs(clean, stream, contaminants)

    if geometry == "high_outside":
        if true_positions != (K - 1, K):
            raise AssertionError(
                f"G0 true positions must be (31,32), got {true_positions}"
            )
        assert_g0_path_regression(
            cfg_base,
            path_seed,
            gamma,
            clean,
            ranks,
        )

    true_index = cfg_base.candidates.index(tuple(true_positions))
    cfg = replace(cfg_base, true_candidate_index=true_index)

    out = kt13.evaluate_path(cfg, ranks)

    return PathRecord(
        rep_index=rep_index,
        path_seed=path_seed,
        geometry=geometry,
        contaminants=contaminants,
        true_positions=true_positions,
        output=out,
    )


def _simulate_block(
    payload: tuple[
        float | None,
        tuple[tuple[int, int], ...],
        bool,
    ],
) -> list[PathRecord]:
    gamma, indexed_seeds, smoke = payload
    cfg = kt13.base.build_config(K)
    records: list[PathRecord] = []

    for rep_index, path_seed in indexed_seeds:
        clean, stream = generate_clean_stream(path_seed, gamma, cfg)

        for geometry in GEOMETRIES:
            records.append(
                evaluate_geometry(
                    cfg,
                    rep_index,
                    path_seed,
                    gamma,
                    geometry,
                    clean,
                    stream,
                    smoke,
                )
            )

    return records


def chunks(
    values: list[tuple[int, int]],
    size: int,
) -> Iterable[tuple[tuple[int, int], ...]]:
    for start in range(0, len(values), size):
        yield tuple(values[start : start + size])


def run_condition(
    gamma: float | None,
    reps: int,
    workers: int,
    block_size: int,
    smoke: bool,
) -> dict[str, list[PathRecord]]:
    seeds = v1_path_seeds(gamma, reps, smoke)
    indexed = list(enumerate(seeds))
    blocks = [
        (gamma, block, smoke)
        for block in chunks(indexed, block_size)
    ]

    print(
        f"[simulate] condition={condition_name(gamma)} reps={reps} "
        f"geometries={len(GEOMETRIES)} workers={workers} "
        f"blocks={len(blocks)} smoke={smoke}"
    )

    records: list[PathRecord] = []

    if workers <= 1:
        for index, payload in enumerate(blocks, start=1):
            records.extend(_simulate_block(payload))
            print(
                f"  block {index}/{len(blocks)} complete",
                flush=True,
            )
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for index, block_records in enumerate(
                pool.map(_simulate_block, blocks),
                start=1,
            ):
                records.extend(block_records)
                print(
                    f"  block {index}/{len(blocks)} complete",
                    flush=True,
                )

    expected = reps * len(GEOMETRIES)
    if len(records) != expected:
        raise RuntimeError(
            f"expected {expected} geometry records, got {len(records)}"
        )

    grouped = {geometry: [] for geometry in GEOMETRIES}
    for record in records:
        grouped[record.geometry].append(record)

    for geometry in GEOMETRIES:
        grouped[geometry].sort(key=lambda r: r.rep_index)
        rep_ids = [r.rep_index for r in grouped[geometry]]
        if rep_ids != list(range(reps)):
            raise RuntimeError(
                f"replication ordering mismatch for {geometry}"
            )

    return grouped


def outputs(records: list[PathRecord]) -> list[kt13.PathSummary]:
    return [record.output for record in records]


def stop_array(
    outs: list[kt13.PathSummary],
    spec: pubv1.MethodSpec,
) -> np.ndarray:
    values = [
        0 if (stop := pubv1.stop_for(out, spec)) is None else int(stop)
        for out in outs
    ]
    return np.asarray(values, dtype=np.int16)


def indicator_array(
    outs: list[kt13.PathSummary],
    spec: pubv1.MethodSpec,
    horizon: int,
) -> np.ndarray:
    stops = stop_array(outs, spec)
    return ((stops > 0) & (stops <= horizon)).astype(float)


def truncated_stops(
    outs: list[kt13.PathSummary],
    spec: pubv1.MethodSpec,
    horizon: int,
) -> np.ndarray:
    stops = stop_array(outs, spec).astype(float)
    return np.where(
        (stops > 0) & (stops <= horizon),
        stops,
        float(horizon + 1),
    )


def detected_stops(
    outs: list[kt13.PathSummary],
    spec: pubv1.MethodSpec,
    horizon: int,
) -> np.ndarray:
    stops = stop_array(outs, spec)
    mask = (stops > 0) & (stops <= horizon)
    return stops[mask].astype(float)


def log_array(
    outs: list[kt13.PathSummary],
    spec: pubv1.MethodSpec,
    horizon: int,
) -> np.ndarray:
    return np.asarray(
        [pubv1.loge_for(out, spec, horizon) for out in outs],
        dtype=float,
    )


def bootstrap_mean_ci(
    values: np.ndarray,
    reps: int,
    seed: int,
) -> tuple[float, float]:
    return pubv1.bootstrap_percentile_ci(
        values.astype(float),
        "mean",
        reps,
        seed,
    )


def bootstrap_median_ci(
    values: np.ndarray,
    reps: int,
    seed: int,
) -> tuple[float, float]:
    return pubv1.bootstrap_percentile_ci(
        values.astype(float),
        "median",
        reps,
        seed,
    )


def v1b_bootstrap_seed(
    gamma: float | None,
    geometry: str,
    horizon: int,
    salt: int,
) -> int:
    return (
        V1B_CONTAM_SEED
        + 1_000_000_000
        + 1_000_000 * scenario_code(gamma)
        + 10_000 * GEOMETRY_INDEX[geometry]
        + 10 * horizon
        + salt
    )


def method_stats(
    outs: list[kt13.PathSummary],
    spec: pubv1.MethodSpec,
    horizon: int,
    bootstrap_reps: int,
    seed: int,
) -> dict[str, float | int | str]:
    ind = indicator_array(outs, spec, horizon)
    successes = int(ind.sum())
    n = int(ind.size)
    cross = successes / n
    cross_lo, cross_hi = pubv1.wilson_interval(successes, n)

    det = detected_stops(outs, spec, horizon)
    if det.size:
        med = float(np.median(det))
        med_lo, med_hi = bootstrap_median_ci(
            det,
            bootstrap_reps,
            seed + 1,
        )
    else:
        med = float("nan")
        med_lo = float("nan")
        med_hi = float("nan")

    trunc = truncated_stops(outs, spec, horizon)
    trunc_mean = float(np.mean(trunc))
    trunc_lo, trunc_hi = bootstrap_mean_ci(
        trunc,
        bootstrap_reps,
        seed + 2,
    )

    logs = log_array(outs, spec, horizon)

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
        "truncated_stop_mean": trunc_mean,
        "truncated_stop_ci_low": trunc_lo,
        "truncated_stop_ci_high": trunc_hi,
        "median_delay_detected": med,
        "median_delay_ci_low": med_lo,
        "median_delay_ci_high": med_hi,
        "median_loge": float(np.median(logs)),
        "threshold": threshold,
    }


def strongest_baseline(
    outs: list[kt13.PathSummary],
    horizon: int,
) -> pubv1.MethodSpec:
    return pubv1.strongest_baseline(outs, horizon)


def fmt(value: float | int | str) -> float | int | str:
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise RuntimeError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def paired_effect(
    a: np.ndarray,
    b: np.ndarray,
    bootstrap_reps: int,
    seed: int,
) -> tuple[float, float, float]:
    return pubv1.paired_difference(
        a.astype(float),
        b.astype(float),
        bootstrap_reps,
        seed,
    )


def summarize_condition(
    gamma: float | None,
    grouped: dict[str, list[PathRecord]],
    bootstrap_reps: int,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    summary_rows: list[dict[str, object]] = []
    paired_rows: list[dict[str, object]] = []
    geometry_rows: list[dict[str, object]] = []
    cdf_rows: list[dict[str, object]] = []
    position_rows: list[dict[str, object]] = []

    per_geometry_best_t200: dict[str, pubv1.MethodSpec] = {}

    for geometry in GEOMETRIES:
        recs = grouped[geometry]
        outs = outputs(recs)
        per_geometry_best_t200[geometry] = strongest_baseline(
            outs,
            200,
        )

        position_counts = Counter(
            record.true_positions
            for record in recs
        )
        for positions, count in sorted(position_counts.items()):
            position_rows.append(
                {
                    "condition": condition_name(gamma),
                    "true_gamma": "" if gamma is None else gamma,
                    "geometry": geometry,
                    "pos1": positions[0],
                    "pos2": positions[1],
                    "count": count,
                    "rate": count / len(recs),
                }
            )

        for horizon in HORIZONS:
            best = strongest_baseline(outs, horizon)

            reported = (
                ("static", STATIC),
                ("primary_baseline", PRIMARY_BASELINE),
                ("best_grid_baseline", best),
                ("oracle", ORACLE),
            )

            for offset, (name, spec) in enumerate(reported, start=1):
                stats = method_stats(
                    outs,
                    spec,
                    horizon,
                    bootstrap_reps,
                    v1b_bootstrap_seed(
                        gamma,
                        geometry,
                        horizon,
                        100 + offset,
                    ),
                )
                summary_rows.append(
                    {
                        "K": K,
                        "M": M,
                        "condition": condition_name(gamma),
                        "true_gamma": "" if gamma is None else gamma,
                        "geometry": geometry,
                        "horizon": horizon,
                        "reps": len(outs),
                        "reported_method": name,
                        "underlying_method": spec.method,
                        "delta": "" if spec.delta is None else spec.delta,
                        "D": "" if spec.d_bound is None else spec.d_bound,
                        **{
                            key: fmt(value)
                            for key, value in stats.items()
                        },
                    }
                )

            static_ind = indicator_array(outs, STATIC, horizon)
            primary_ind = indicator_array(
                outs,
                PRIMARY_BASELINE,
                horizon,
            )
            oracle_ind = indicator_array(outs, ORACLE, horizon)

            sb, sb_lo, sb_hi = paired_effect(
                static_ind,
                primary_ind,
                bootstrap_reps,
                v1b_bootstrap_seed(
                    gamma,
                    geometry,
                    horizon,
                    201,
                ),
            )
            os_gap, os_lo, os_hi = paired_effect(
                oracle_ind,
                static_ind,
                bootstrap_reps,
                v1b_bootstrap_seed(
                    gamma,
                    geometry,
                    horizon,
                    202,
                ),
            )

            paired_rows.append(
                {
                    "K": K,
                    "M": M,
                    "condition": condition_name(gamma),
                    "true_gamma": "" if gamma is None else gamma,
                    "geometry": geometry,
                    "horizon": horizon,
                    "reps": len(outs),
                    "primary_baseline_method": PRIMARY_BASELINE.method,
                    "primary_baseline_delta": PRIMARY_BASELINE.delta,
                    "static_minus_primary": sb,
                    "static_minus_primary_ci_low": sb_lo,
                    "static_minus_primary_ci_high": sb_hi,
                    "oracle_minus_static": os_gap,
                    "oracle_minus_static_ci_low": os_lo,
                    "oracle_minus_static_ci_high": os_hi,
                }
            )

    # Geometry effects relative to G0, paired by replication.
    control_outs = outputs(grouped["high_outside"])

    for geometry in GEOMETRIES[1:]:
        geom_outs = outputs(grouped[geometry])

        for horizon in HORIZONS:
            for label, spec in (
                ("static", STATIC),
                ("primary_baseline", PRIMARY_BASELINE),
                ("oracle", ORACLE),
            ):
                geom_ind = indicator_array(
                    geom_outs,
                    spec,
                    horizon,
                )
                ctrl_ind = indicator_array(
                    control_outs,
                    spec,
                    horizon,
                )
                cross_diff, cross_lo, cross_hi = paired_effect(
                    geom_ind,
                    ctrl_ind,
                    bootstrap_reps,
                    v1b_bootstrap_seed(
                        gamma,
                        geometry,
                        horizon,
                        301 + {"static": 1, "primary_baseline": 2, "oracle": 3}[label],
                    ),
                )

                geom_trunc = truncated_stops(
                    geom_outs,
                    spec,
                    horizon,
                )
                ctrl_trunc = truncated_stops(
                    control_outs,
                    spec,
                    horizon,
                )
                delay_diff = geom_trunc - ctrl_trunc
                delay_est = float(np.mean(delay_diff))
                delay_lo, delay_hi = bootstrap_mean_ci(
                    delay_diff,
                    bootstrap_reps,
                    v1b_bootstrap_seed(
                        gamma,
                        geometry,
                        horizon,
                        401 + {"static": 1, "primary_baseline": 2, "oracle": 3}[label],
                    ),
                )

                geometry_rows.append(
                    {
                        "condition": condition_name(gamma),
                        "true_gamma": "" if gamma is None else gamma,
                        "geometry": geometry,
                        "control_geometry": "high_outside",
                        "horizon": horizon,
                        "method": label,
                        "cross_rate_difference_vs_G0": cross_diff,
                        "cross_diff_ci_low": cross_lo,
                        "cross_diff_ci_high": cross_hi,
                        "truncated_stop_mean_difference_vs_G0": delay_est,
                        "truncated_stop_diff_ci_low": delay_lo,
                        "truncated_stop_diff_ci_high": delay_hi,
                    }
                )

    # Detection CDF. For the descriptive best-grid curve, use the T=200
    # selected configuration as one fixed curve over t.
    for geometry in GEOMETRIES:
        outs = outputs(grouped[geometry])
        best_t200 = per_geometry_best_t200[geometry]

        for reported_name, spec in (
            ("static", STATIC),
            ("primary_baseline", PRIMARY_BASELINE),
            ("best_grid_T200", best_t200),
            ("oracle", ORACLE),
        ):
            stops = stop_array(outs, spec)
            for t in range(1, MAX_T + 1):
                rate = float(
                    np.mean((stops > 0) & (stops <= t))
                )
                cdf_rows.append(
                    {
                        "condition": condition_name(gamma),
                        "true_gamma": "" if gamma is None else gamma,
                        "geometry": geometry,
                        "reported_method": reported_name,
                        "underlying_method": spec.method,
                        "delta": "" if spec.delta is None else spec.delta,
                        "D": "" if spec.d_bound is None else spec.d_bound,
                        "t": t,
                        "F_tau": rate,
                    }
                )

    return (
        summary_rows,
        paired_rows,
        geometry_rows,
        cdf_rows,
        position_rows,
    )


def append_raw_arrays(
    store: dict[str, list[np.ndarray]],
    gamma: float | None,
    grouped: dict[str, list[PathRecord]],
) -> None:
    horizons = np.asarray(HORIZONS, dtype=np.int16)

    for geometry in GEOMETRIES:
        recs = grouped[geometry]
        outs = outputs(recs)
        count = len(recs)

        store["condition_code"].append(
            np.full(
                count,
                -1 if gamma is None else int(gamma),
                dtype=np.int16,
            )
        )
        store["geometry_index"].append(
            np.full(
                count,
                GEOMETRY_INDEX[geometry],
                dtype=np.int8,
            )
        )
        store["rep_index"].append(
            np.asarray(
                [r.rep_index for r in recs],
                dtype=np.int32,
            )
        )
        store["path_seed"].append(
            np.asarray(
                [r.path_seed for r in recs],
                dtype=np.int64,
            )
        )
        store["contaminants"].append(
            np.asarray(
                [r.contaminants for r in recs],
                dtype=np.float64,
            )
        )
        store["true_positions"].append(
            np.asarray(
                [r.true_positions for r in recs],
                dtype=np.int16,
            )
        )

        store["static_stop"].append(
            stop_array(outs, STATIC)
        )
        store["primary_stop"].append(
            stop_array(outs, PRIMARY_BASELINE)
        )
        store["oracle_stop"].append(
            stop_array(outs, ORACLE)
        )

        baseline_stops = np.empty(
            (count, len(BASELINE_SPECS)),
            dtype=np.int16,
        )
        for j, spec in enumerate(BASELINE_SPECS):
            baseline_stops[:, j] = stop_array(outs, spec)
        store["baseline_stops"].append(baseline_stops)

        static_logs = np.empty(
            (count, len(horizons)),
            dtype=np.float32,
        )
        oracle_logs = np.empty_like(static_logs)
        baseline_logs = np.empty(
            (count, len(BASELINE_SPECS), len(horizons)),
            dtype=np.float32,
        )

        for hidx, horizon in enumerate(HORIZONS):
            static_logs[:, hidx] = log_array(
                outs,
                STATIC,
                horizon,
            ).astype(np.float32)
            oracle_logs[:, hidx] = log_array(
                outs,
                ORACLE,
                horizon,
            ).astype(np.float32)

            for j, spec in enumerate(BASELINE_SPECS):
                baseline_logs[:, j, hidx] = log_array(
                    outs,
                    spec,
                    horizon,
                ).astype(np.float32)

        store["static_logs"].append(static_logs)
        store["oracle_logs"].append(oracle_logs)
        store["baseline_logs"].append(baseline_logs)


def save_raw_npz(
    path: Path,
    store: dict[str, list[np.ndarray]],
) -> None:
    arrays = {
        key: np.concatenate(value, axis=0)
        for key, value in store.items()
    }
    arrays["horizons"] = np.asarray(HORIZONS, dtype=np.int16)
    np.savez_compressed(path, **arrays)


def regression_against_archived_v1(
    summary_rows: list[dict[str, object]],
    reps: int,
    smoke: bool,
) -> None:
    if smoke or reps != 5_000:
        return

    archived_path = ROOT / "results" / "publication_v1" / "summary.csv"
    if not archived_path.exists():
        raise RuntimeError(
            f"full-run G0 regression requires {archived_path}"
        )

    with archived_path.open(newline="") as handle:
        archived = list(csv.DictReader(handle))

    archived = [
        row
        for row in archived
        if int(row["K"]) == K
    ]

    for row in archived:
        target = next(
            candidate
            for candidate in summary_rows
            if candidate["geometry"] == "high_outside"
            and candidate["condition"] == row["condition"]
            and int(candidate["horizon"]) == int(row["horizon"])
            and candidate["reported_method"] == row["reported_method"]
        )

        if int(target["cross_count"]) != int(row["cross_count"]):
            raise AssertionError(
                "G0 aggregate regression failed for "
                f"{row['condition']} T={row['horizon']} "
                f"{row['reported_method']}: "
                f"{target['cross_count']} != {row['cross_count']}"
            )

        if target["reported_method"] == "best_grid_baseline":
            if target["underlying_method"] != row["underlying_method"]:
                raise AssertionError(
                    "G0 best-grid method mismatch"
                )
            target_delta = "" if target["delta"] == "" else float(target["delta"])
            archived_delta = "" if row["delta"] == "" else float(row["delta"])
            if target_delta != archived_delta:
                raise AssertionError(
                    "G0 best-grid delta mismatch"
                )

    print("G0_FULL_REGRESSION: PASS")


def null_sanity_failures(
    summary_rows: list[dict[str, object]],
) -> list[str]:
    failures: list[str] = []
    for row in summary_rows:
        if (
            row["condition"] == "null"
            and row["horizon"] == 200
            and row["reported_method"] == "static"
            and float(row["cross_ci_low"]) > 0.05
        ):
            failures.append(
                f"{row['geometry']}: "
                f"static null CI low={float(row['cross_ci_low']):.6f}"
            )
    return failures


def make_figures(
    summary_rows: list[dict[str, object]],
    cdf_rows: list[dict[str, object]],
    outdir: Path,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # Primary crossing plot, gamma=4, T=200.
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    x = np.arange(len(GEOMETRIES), dtype=float)
    width = 0.25

    for offset, method in enumerate(
        ("static", "primary_baseline", "oracle")
    ):
        rows = [
            next(
                row
                for row in summary_rows
                if row["geometry"] == geometry
                and row["true_gamma"] == 4.0
                and row["horizon"] == 200
                and row["reported_method"] == method
            )
            for geometry in GEOMETRIES
        ]
        y = np.asarray([float(row["cross_rate"]) for row in rows])
        ax.bar(
            x + (offset - 1) * width,
            y,
            width=width,
            label=method.replace("_", " "),
        )

    ax.set_xticks(x)
    ax.set_xticklabels(GEOMETRIES, rotation=18, ha="right")
    ax.set_ylabel("Crossing probability by T=200")
    ax.set_ylim(0.0, 1.02)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "crossing_by_geometry_gamma4_T200.pdf")
    fig.savefig(
        outdir / "crossing_by_geometry_gamma4_T200.png",
        dpi=180,
    )
    plt.close(fig)

    # Static detection CDF by geometry at gamma=4.
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for geometry in GEOMETRIES:
        rows = [
            row
            for row in cdf_rows
            if row["geometry"] == geometry
            and row["true_gamma"] == 4.0
            and row["reported_method"] == "static"
        ]
        rows.sort(key=lambda row: int(row["t"]))
        ax.plot(
            [int(row["t"]) for row in rows],
            [float(row["F_tau"]) for row in rows],
            label=geometry,
        )

    ax.set_xlabel("t")
    ax.set_ylabel("Empirical F_tau(t)")
    ax.set_ylim(0.0, 1.02)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "static_detection_cdf_gamma4.pdf")
    fig.savefig(
        outdir / "static_detection_cdf_gamma4.png",
        dpi=180,
    )
    plt.close(fig)

    # Truncated stopping-time mean at primary point.
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    for offset, method in enumerate(
        ("static", "primary_baseline", "oracle")
    ):
        rows = [
            next(
                row
                for row in summary_rows
                if row["geometry"] == geometry
                and row["true_gamma"] == 4.0
                and row["horizon"] == 200
                and row["reported_method"] == method
            )
            for geometry in GEOMETRIES
        ]
        y = np.asarray(
            [float(row["truncated_stop_mean"]) for row in rows]
        )
        ax.bar(
            x + (offset - 1) * width,
            y,
            width=width,
            label=method.replace("_", " "),
        )

    ax.set_xticks(x)
    ax.set_xticklabels(GEOMETRIES, rotation=18, ha="right")
    ax.set_ylabel("Mean truncated stopping time")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "truncated_stop_by_geometry_gamma4.pdf")
    fig.savefig(
        outdir / "truncated_stop_by_geometry_gamma4.png",
        dpi=180,
    )
    plt.close(fig)


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def write_sha256s(outdir: Path) -> None:
    targets = sorted(
        path
        for path in outdir.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    )
    lines = []
    for path in targets:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rel = path.relative_to(ROOT)
        lines.append(f"{digest}  {rel.as_posix()}")
    (outdir / "SHA256SUMS").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=DEFAULT_REPS)
    parser.add_argument(
        "--bootstrap-reps",
        type=int,
        default=DEFAULT_BOOTSTRAP,
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(4, os.cpu_count() or 1),
    )
    parser.add_argument(
        "--block-size",
        type=int,
        default=DEFAULT_BLOCK_SIZE,
    )
    parser.add_argument(
        "--output-dir",
        default="results/publication_v1b_geometry",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="use a separate smoke seed namespace; never interpret scientifically",
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

    if args.smoke and args.output_dir == "results/publication_v1b_geometry":
        args.output_dir = "results/publication_v1b_geometry_smoke"

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("LIMEN-RF Publication Validation V1b")
    print("PREREGISTERED contamination-geometry stress test")
    print(
        f"K={K} M={M} horizons={HORIZONS} "
        f"reps={args.reps} bootstrap={args.bootstrap_reps} "
        f"workers={args.workers} smoke={args.smoke}"
    )
    print(f"geometries={GEOMETRIES}")
    print("primary baseline=band_mix delta=0.045")
    print("")

    all_summary: list[dict[str, object]] = []
    all_paired: list[dict[str, object]] = []
    all_geometry: list[dict[str, object]] = []
    all_cdf: list[dict[str, object]] = []
    all_positions: list[dict[str, object]] = []

    raw_store: dict[str, list[np.ndarray]] = {
        "condition_code": [],
        "geometry_index": [],
        "rep_index": [],
        "path_seed": [],
        "contaminants": [],
        "true_positions": [],
        "static_stop": [],
        "primary_stop": [],
        "oracle_stop": [],
        "baseline_stops": [],
        "static_logs": [],
        "oracle_logs": [],
        "baseline_logs": [],
    }

    for gamma in TRUE_GAMMAS:
        grouped = run_condition(
            gamma,
            args.reps,
            args.workers,
            args.block_size,
            args.smoke,
        )

        append_raw_arrays(raw_store, gamma, grouped)

        (
            summary_rows,
            paired_rows,
            geometry_rows,
            cdf_rows,
            position_rows,
        ) = summarize_condition(
            gamma,
            grouped,
            args.bootstrap_reps,
        )

        all_summary.extend(summary_rows)
        all_paired.extend(paired_rows)
        all_geometry.extend(geometry_rows)
        all_cdf.extend(cdf_rows)
        all_positions.extend(position_rows)

        del grouped

    regression_against_archived_v1(
        all_summary,
        args.reps,
        args.smoke,
    )

    raw_path = outdir / "raw_paths.npz"
    save_raw_npz(raw_path, raw_store)

    write_csv(outdir / "summary.csv", all_summary)
    write_csv(outdir / "paired_effects.csv", all_paired)
    write_csv(outdir / "geometry_effects.csv", all_geometry)
    write_csv(outdir / "detection_cdf.csv", all_cdf)
    write_csv(
        outdir / "true_position_diagnostics.csv",
        all_positions,
    )

    make_figures(
        all_summary,
        all_cdf,
        outdir / "figures",
    )

    baseline_manifest = [
        {
            "index": i,
            "method": spec.method,
            "delta": spec.delta,
            "D": spec.d_bound,
        }
        for i, spec in enumerate(BASELINE_SPECS)
    ]

    failures = null_sanity_failures(all_summary)

    manifest = {
        "status": (
            "smoke implementation check"
            if args.smoke
            else "preregistered post-freeze V1b geometry stress test"
        ),
        "git_commit": git_commit(),
        "runbook": (
            "docs/experiments/"
            "publication_validation_v1b_geometry_runbook.md"
        ),
        "K": K,
        "M": M,
        "N": N,
        "alpha": kt13.ALPHA,
        "horizons": list(HORIZONS),
        "conditions": [
            None if gamma is None else gamma
            for gamma in TRUE_GAMMAS
        ],
        "geometries": {
            "high_outside": [2.0, 2.0],
            "upper_inside": [0.85, 0.95],
            "mixed_inside": [0.10, 0.90],
            "random_static_inside": {
                "distribution": "iid Beta(1/2,1/2)",
                "seed_base": V1B_CONTAM_SEED,
            },
        },
        "reps": args.reps,
        "bootstrap_reps": args.bootstrap_reps,
        "workers": args.workers,
        "block_size": args.block_size,
        "smoke": args.smoke,
        "publication_v1_seed": pubv1.PUB_SEED,
        "primary_baseline": {
            "method": PRIMARY_BASELINE.method,
            "delta": PRIMARY_BASELINE.delta,
            "D": PRIMARY_BASELINE.d_bound,
        },
        "baseline_grid_order_for_raw_npz": baseline_manifest,
        "raw_npz_horizons": list(HORIZONS),
        "null_sanity_failures": failures,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "note": (
            "G0 path generation is asserted against Publication V1. "
            "Full 5000-rep non-smoke runs also regress G0 aggregate "
            "cross-counts and selected best-grid methods against the "
            "archived Publication V1 summary. Best-grid results are "
            "secondary/descriptive; primary inference uses the fixed "
            "band_mix delta=0.045 comparator."
        ),
    }

    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    write_sha256s(outdir)

    print("")
    print("=== V1B PRIMARY gamma=4 T=200 ===")
    for geometry in GEOMETRIES:
        rows = [
            row
            for row in all_summary
            if row["geometry"] == geometry
            and row["true_gamma"] == 4.0
            and row["horizon"] == 200
        ]
        by_method = {
            row["reported_method"]: row
            for row in rows
        }
        pair = next(
            row
            for row in all_paired
            if row["geometry"] == geometry
            and row["true_gamma"] == 4.0
            and row["horizon"] == 200
        )

        static = by_method["static"]
        primary = by_method["primary_baseline"]
        best = by_method["best_grid_baseline"]
        oracle = by_method["oracle"]

        print(
            f"{geometry:>20} "
            f"static={float(static['cross_rate']):.4f} "
            f"primary={float(primary['cross_rate']):.4f} "
            f"gap={float(pair['static_minus_primary']):.4f} "
            f"best_grid={float(best['cross_rate']):.4f} "
            f"oracle={float(oracle['cross_rate']):.4f} "
            f"trunc_static={float(static['truncated_stop_mean']):.2f}"
        )

    print("")
    if failures:
        print("V1B_NULL_SANITY: FAIL")
        for failure in failures:
            print(f"  {failure}")
    else:
        print("V1B_NULL_SANITY: PASS")

    print(f"results: {outdir}")
    print(f"raw:     {raw_path}")
    print(f"hashes:  {outdir / 'SHA256SUMS'}")

    if args.smoke:
        print("V1B_SMOKE: COMPLETE")
    else:
        print("V1B_PUBLICATION: COMPLETE")

    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
