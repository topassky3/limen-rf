#!/usr/bin/env python3
"""Kill-Test 09: adaptive-mixture predictive-rank robustness.

Repairs the fixed-bettor mismatch exposed by Kill-Test 08 while preserving
anytime validity for the true static contamination candidate.

Standard-library only.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import itertools
import math
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


SEED = 20260918
K = 8
M = 2
N = K - M
ALPHA = 0.05
GAMMA_GRID = (1.25, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0)
SYMMETRIC_ALPHA = (0.1, 0.25, 0.5)
TILT_TOTAL = (1.0, 3.5, 7.0)
TILT_BETA = (0.5, 1.0, 2.0, 4.0)
HEDGE_WEIGHT = 0.05
HORIZONS = (40, 100, 200)
TRUE_GAMMAS: tuple[float | None, ...] = (None, 2.0, 4.0, 8.0)


def logsumexp(values: list[float]) -> float:
    maximum = max(values)
    return maximum + math.log(sum(math.exp(v - maximum) for v in values))


def beta_rank_probs(n: int, gamma: float) -> tuple[float, ...]:
    probs: list[float] = []
    for j in range(n + 1):
        logp = (
            math.lgamma(n + 1)
            - math.lgamma(j + 1)
            - math.lgamma(n - j + 1)
            + math.log(gamma)
            + math.lgamma(j + gamma)
            - math.lgamma(n + gamma + 1)
        )
        probs.append(math.exp(logp))

    total = sum(probs)
    return tuple(p / total for p in probs)


@dataclass(frozen=True)
class Component:
    name: str
    kind: Literal["fixed", "dirichlet"]
    params: tuple[float, ...]


def build_components(n: int) -> tuple[Component, ...]:
    components: list[Component] = []

    for gamma in GAMMA_GRID:
        components.append(
            Component(
                name=f"fixed_beta_gamma_{gamma:g}",
                kind="fixed",
                params=beta_rank_probs(n, gamma),
            )
        )

    for alpha in SYMMETRIC_ALPHA:
        components.append(
            Component(
                name=f"dirichlet_symmetric_{alpha:g}",
                kind="dirichlet",
                params=tuple(alpha for _ in range(n + 1)),
            )
        )

    for total in TILT_TOTAL:
        for beta in TILT_BETA:
            weights = [math.exp(beta * j / n) for j in range(n + 1)]
            norm = sum(weights)
            params = tuple(total * w / norm for w in weights)
            components.append(
                Component(
                    name=f"dirichlet_tilt_total_{total:g}_beta_{beta:g}",
                    kind="dirichlet",
                    params=params,
                )
            )

    return tuple(components)


COMPONENTS = build_components(N)
ALT_COMPONENT_WEIGHT = (1.0 - HEDGE_WEIGHT) / len(COMPONENTS)
LOG_HEDGE_WEIGHT = math.log(HEDGE_WEIGHT)
LOG_ALT_COMPONENT_WEIGHT = math.log(ALT_COMPONENT_WEIGHT)


def contamination_candidates(k: int, m: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.combinations(range(1, k + 1), m))


CANDIDATES = contamination_candidates(K, M)
TRUE_C = tuple(range(K - M + 1, K + 1))


def candidate_rank_map(
    k: int,
    contamination_positions: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        q - sum(c <= q for c in contamination_positions)
        for q in range(k + 1)
    )


RANK_MAPS = {c: candidate_rank_map(K, c) for c in CANDIDATES}


@dataclass
class CandidateState:
    counts: list[int]
    component_log_wealth: list[float]


def fresh_states() -> dict[tuple[int, ...], CandidateState]:
    return {
        c: CandidateState(
            counts=[0] * (N + 1),
            component_log_wealth=[0.0] * len(COMPONENTS),
        )
        for c in CANDIDATES
    }


def candidate_mixture_log_wealth(state: CandidateState) -> float:
    terms = [LOG_HEDGE_WEIGHT]
    terms.extend(
        LOG_ALT_COMPONENT_WEIGHT + logw
        for logw in state.component_log_wealth
    )
    return logsumexp(terms)


def update_candidate_state(
    state: CandidateState,
    transformed_rank: int,
    t: int,
) -> None:
    old_count = state.counts[transformed_rank]
    p0 = (old_count + 1.0) / (N + t)

    for index, component in enumerate(COMPONENTS):
        if component.kind == "fixed":
            q = component.params[transformed_rank]
        else:
            total_alpha = sum(component.params)
            q = (
                old_count + component.params[transformed_rank]
            ) / ((t - 1) + total_alpha)

        state.component_log_wealth[index] += math.log(q / p0)

    state.counts[transformed_rank] += 1


@dataclass(frozen=True)
class PathResult:
    robust_crossed: bool
    oracle_crossed: bool
    robust_max_loge: float
    oracle_max_loge: float
    robust_final_loge: float
    oracle_final_loge: float
    final_worst_candidate: tuple[int, ...]


def evaluate_rank_path(ranks: list[int], alpha: float) -> PathResult:
    threshold = math.log(1.0 / alpha)
    states = fresh_states()

    robust_max = float("-inf")
    oracle_max = float("-inf")
    robust_crossed = False
    oracle_crossed = False
    final_candidate_logs: dict[tuple[int, ...], float] = {}

    for t, observed_rank in enumerate(ranks, start=1):
        candidate_logs: dict[tuple[int, ...], float] = {}

        for candidate in CANDIDATES:
            transformed_rank = RANK_MAPS[candidate][observed_rank]
            state = states[candidate]
            update_candidate_state(state, transformed_rank, t)
            candidate_logs[candidate] = candidate_mixture_log_wealth(state)

        robust_now = min(candidate_logs.values())
        oracle_now = candidate_logs[TRUE_C]

        robust_max = max(robust_max, robust_now)
        oracle_max = max(oracle_max, oracle_now)
        robust_crossed = robust_crossed or robust_now >= threshold
        oracle_crossed = oracle_crossed or oracle_now >= threshold
        final_candidate_logs = candidate_logs

    final_worst = min(final_candidate_logs, key=final_candidate_logs.get)

    return PathResult(
        robust_crossed=robust_crossed,
        oracle_crossed=oracle_crossed,
        robust_max_loge=robust_max,
        oracle_max_loge=oracle_max,
        robust_final_loge=min(final_candidate_logs.values()),
        oracle_final_loge=final_candidate_logs[TRUE_C],
        final_worst_candidate=final_worst,
    )


def simulate_observed_ranks(
    rng: random.Random,
    horizon: int,
    true_gamma: float | None,
) -> list[int]:
    clean_reference = sorted(rng.random() for _ in range(N))

    observed_reference = clean_reference + [2.0] * M
    observed_reference.sort()

    if true_gamma is None:
        stream = [rng.random() for _ in range(horizon)]
    else:
        stream = [
            rng.betavariate(true_gamma, 1.0)
            for _ in range(horizon)
        ]

    return [
        bisect.bisect_right(observed_reference, x)
        for x in stream
    ]


def median(values: list[float]) -> float:
    ordered = sorted(values)
    size = len(ordered)
    mid = size // 2
    if size % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def scenario_seed(true_gamma: float | None, horizon: int) -> int:
    gamma_code = 0 if true_gamma is None else int(true_gamma * 1000)
    return SEED + 10_000 * gamma_code + horizon


def run_scenario(
    reps: int,
    horizon: int,
    true_gamma: float | None,
) -> dict[str, object]:
    rng = random.Random(scenario_seed(true_gamma, horizon))

    robust_cross = 0
    oracle_cross = 0
    robust_max: list[float] = []
    oracle_max: list[float] = []
    robust_final: list[float] = []
    oracle_final: list[float] = []
    worst_candidates: Counter[tuple[int, ...]] = Counter()

    for _ in range(reps):
        ranks = simulate_observed_ranks(rng, horizon, true_gamma)
        result = evaluate_rank_path(ranks, ALPHA)

        robust_cross += int(result.robust_crossed)
        oracle_cross += int(result.oracle_crossed)
        robust_max.append(result.robust_max_loge)
        oracle_max.append(result.oracle_max_loge)
        robust_final.append(result.robust_final_loge)
        oracle_final.append(result.oracle_final_loge)
        worst_candidates[result.final_worst_candidate] += 1

    worst_candidate, worst_count = worst_candidates.most_common(1)[0]

    return {
        "condition": "null" if true_gamma is None else f"beta_{true_gamma:g}",
        "true_gamma": "" if true_gamma is None else true_gamma,
        "horizon": horizon,
        "reps": reps,
        "robust_cross_rate": robust_cross / reps,
        "oracle_cross_rate": oracle_cross / reps,
        "median_robust_max_loge": median(robust_max),
        "median_oracle_max_loge": median(oracle_max),
        "median_robust_final_loge": median(robust_final),
        "median_oracle_final_loge": median(oracle_final),
        "modal_final_worst_candidate": str(worst_candidate),
        "modal_final_worst_fraction": worst_count / reps,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reps",
        type=int,
        default=200,
        help="Monte Carlo repetitions per scenario (default: 200)",
    )
    parser.add_argument(
        "--output",
        default="results/pminus1_killtest09_summary.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.reps <= 0:
        raise SystemExit("--reps must be positive")

    print("P−1 Kill-Test 09 — adaptive-mixture predictive ranks")
    print(
        f"K={K} M={M} n={N} alpha={ALPHA} reps={args.reps} "
        f"components={len(COMPONENTS)} hedge={HEDGE_WEIGHT}"
    )
    print(f"true contamination positions={TRUE_C}")
    print("")

    rows: list[dict[str, object]] = []

    for true_gamma in TRUE_GAMMAS:
        for horizon in HORIZONS:
            row = run_scenario(args.reps, horizon, true_gamma)
            rows.append(row)

            print(
                "{condition:>7} T={horizon:3d} "
                "robust_cross={robust_cross_rate:.4f} "
                "oracle_cross={oracle_cross_rate:.4f} "
                "med_max_logE_rob={median_robust_max_loge:8.4f} "
                "med_max_logE_orc={median_oracle_max_loge:8.4f} "
                "worst={modal_final_worst_candidate} "
                "freq={modal_final_worst_fraction:.3f}".format(**row)
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("")
    print("=== DECISION AIDS ===")

    null_rows = [row for row in rows if row["condition"] == "null"]
    alt_rows = [row for row in rows if row["condition"] != "null"]

    max_null_robust = max(float(row["robust_cross_rate"]) for row in null_rows)
    print(f"max_null_robust_cross_rate={max_null_robust:.4f}")

    for gamma in (2.0, 4.0, 8.0):
        subset = [
            row
            for row in alt_rows
            if float(row["true_gamma"]) == gamma
        ]
        best = max(subset, key=lambda row: float(row["robust_cross_rate"]))
        print(
            f"gamma={gamma:g} best_robust_cross="
            f"{float(best['robust_cross_rate']):.4f} "
            f"at_T={best['horizon']}"
        )

    print(f"CSV: {output}")
    print("KILLTEST09: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
