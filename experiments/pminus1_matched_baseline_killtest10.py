#!/usr/bin/env python3
"""Kill-Test 10: matched generic-band vs static-coupling comparison."""

from __future__ import annotations

import argparse
import bisect
import csv
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pminus1_predictive_rank_mixture_killtest09 as kt9


SEED = 20260918
K = kt9.K
M = kt9.M
N = kt9.N
ALPHA = kt9.ALPHA
DELTA = ALPHA / 2.0
COND_ALPHA = (ALPHA - DELTA) / (1.0 - DELTA)
HORIZONS = (40, 100, 200)
MAX_T = max(HORIZONS)
TRUE_GAMMAS: tuple[float | None, ...] = (None, 2.0, 4.0, 8.0)

BAND_ETAS = (0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95)
BAND_HEDGE = 0.05
CCTM_D = 0.5
CCTM_SMOOTH = 1e-6

EPS_CLEAN = math.sqrt(math.log(2.0 / DELTA) / (2.0 * N))
EPS_SYM = (N / K) * EPS_CLEAN + M / K

LOG_PRM_THRESHOLD = math.log(1.0 / ALPHA)
LOG_BAND_THRESHOLD = math.log(1.0 / COND_ALPHA)

BAND_ALT_WEIGHT = (1.0 - BAND_HEDGE) / len(BAND_ETAS)
LOG_BAND_HEDGE = math.log(BAND_HEDGE)
LOG_BAND_ALT_WEIGHT = math.log(BAND_ALT_WEIGHT)


def logsumexp(values: list[float]) -> float:
    maximum = max(values)
    return maximum + math.log(sum(math.exp(v - maximum) for v in values))


def median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def dkw_good(clean_reference: list[float]) -> bool:
    """Check the two-sided empirical-CDF sup norm against Uniform(0,1)."""
    xs = sorted(clean_reference)
    n = len(xs)
    d_plus = max((i + 1) / n - x for i, x in enumerate(xs))
    d_minus = max(x - i / n for i, x in enumerate(xs))
    return max(d_plus, d_minus) <= EPS_CLEAN


def contaminated_band_lower(q: int) -> float:
    clean_count_low = max(0, q - M)
    return max(0.0, clean_count_low / N - EPS_CLEAN)


@dataclass
class CCTMState:
    eta: float = 0.0
    a: float = 1.0
    log_wealth: float = 0.0

    def step(self, u: float) -> float:
        eta = self.eta
        smooth = CCTM_SMOOTH
        denom = 0.5 + (1.0 + smooth) * EPS_SYM

        root = math.sqrt(eta * eta + smooth * smooth)
        v_dot_eta = (
            eta * (u - 0.5) - root * EPS_SYM
        ) / denom
        bet = 1.0 + v_dot_eta
        if bet <= 0.0:
            raise RuntimeError(f"nonpositive CCTM bet: {bet}")

        self.log_wealth += math.log(bet)

        dv = (
            u - 0.5 - eta * EPS_SYM / root
        ) / denom
        z = dv / bet

        self.a += z * z
        eta_new = eta + (2.0 / (2.0 - math.log(3.0))) * z / self.a
        self.eta = min(CCTM_D, max(0.0, eta_new))
        return self.log_wealth


@dataclass(frozen=True)
class PathOutput:
    stop_static: int | None
    stop_oracle: int | None
    stop_band: int | None
    stop_cctm: int | None
    logs_static: dict[int, float]
    logs_oracle: dict[int, float]
    logs_band: dict[int, float]
    logs_cctm: dict[int, float]
    dkw_good: bool


def generate_path(
    rng: random.Random,
    true_gamma: float | None,
) -> tuple[list[float], list[float], list[int]]:
    clean = sorted(rng.random() for _ in range(N))
    observed = sorted(clean + [2.0] * M)

    if true_gamma is None:
        stream = [rng.random() for _ in range(MAX_T)]
    else:
        stream = [
            rng.betavariate(true_gamma, 1.0)
            for _ in range(MAX_T)
        ]

    ranks = [bisect.bisect_right(observed, x) for x in stream]
    return clean, observed, ranks


def evaluate_path(
    clean_reference: list[float],
    observed_reference: list[float],
    ranks: list[int],
) -> PathOutput:
    del observed_reference  # ranks already encode the contaminated ECDF counts.

    states = kt9.fresh_states()

    band_component_logs = [0.0] * len(BAND_ETAS)
    cctm = CCTMState()

    stop_static = None
    stop_oracle = None
    stop_band = None
    stop_cctm = None

    logs_static: dict[int, float] = {}
    logs_oracle: dict[int, float] = {}
    logs_band: dict[int, float] = {}
    logs_cctm: dict[int, float] = {}

    for t, q in enumerate(ranks, start=1):
        candidate_logs: dict[tuple[int, ...], float] = {}

        for candidate in kt9.CANDIDATES:
            transformed_rank = kt9.RANK_MAPS[candidate][q]
            state = states[candidate]
            kt9.update_candidate_state(state, transformed_rank, t)
            candidate_logs[candidate] = kt9.candidate_mixture_log_wealth(state)

        static_log = min(candidate_logs.values())
        oracle_log = candidate_logs[kt9.TRUE_C]

        lower = contaminated_band_lower(q)
        h = 2.0 * (lower - 0.5)
        for i, eta in enumerate(BAND_ETAS):
            factor = 1.0 + eta * h
            if factor <= 0.0:
                raise RuntimeError(f"nonpositive band factor: {factor}")
            band_component_logs[i] += math.log(factor)

        band_log = logsumexp(
            [LOG_BAND_HEDGE]
            + [
                LOG_BAND_ALT_WEIGHT + value
                for value in band_component_logs
            ]
        )

        u = q / K
        cctm_log = cctm.step(u)

        if stop_static is None and static_log >= LOG_PRM_THRESHOLD:
            stop_static = t
        if stop_oracle is None and oracle_log >= LOG_PRM_THRESHOLD:
            stop_oracle = t
        if stop_band is None and band_log >= LOG_BAND_THRESHOLD:
            stop_band = t
        if stop_cctm is None and cctm_log >= LOG_BAND_THRESHOLD:
            stop_cctm = t

        if t in HORIZONS:
            logs_static[t] = static_log
            logs_oracle[t] = oracle_log
            logs_band[t] = band_log
            logs_cctm[t] = cctm_log

    return PathOutput(
        stop_static=stop_static,
        stop_oracle=stop_oracle,
        stop_band=stop_band,
        stop_cctm=stop_cctm,
        logs_static=logs_static,
        logs_oracle=logs_oracle,
        logs_band=logs_band,
        logs_cctm=logs_cctm,
        dkw_good=dkw_good(clean_reference),
    )


def scenario_seed(true_gamma: float | None) -> int:
    code = 0 if true_gamma is None else int(1000 * true_gamma)
    return SEED + 100_000 * code


def run_condition(
    reps: int,
    true_gamma: float | None,
) -> list[dict[str, object]]:
    rng = random.Random(scenario_seed(true_gamma))
    outputs: list[PathOutput] = []

    for _ in range(reps):
        clean, observed, ranks = generate_path(rng, true_gamma)
        outputs.append(evaluate_path(clean, observed, ranks))

    rows: list[dict[str, object]] = []
    condition = "null" if true_gamma is None else f"beta_{true_gamma:g}"
    good_rate = sum(int(x.dkw_good) for x in outputs) / reps

    method_specs = (
        ("static", "stop_static", "logs_static"),
        ("band", "stop_band", "logs_band"),
        ("cctm", "stop_cctm", "logs_cctm"),
        ("oracle", "stop_oracle", "logs_oracle"),
    )

    for horizon in HORIZONS:
        row: dict[str, object] = {
            "condition": condition,
            "true_gamma": "" if true_gamma is None else true_gamma,
            "horizon": horizon,
            "reps": reps,
            "dkw_good_rate": good_rate,
        }

        for label, stop_name, logs_name in method_specs:
            stops = [
                getattr(out, stop_name)
                for out in outputs
                if getattr(out, stop_name) is not None
                and getattr(out, stop_name) <= horizon
            ]
            crossing = len(stops) / reps
            delay = median([float(s) for s in stops])
            logs = [getattr(out, logs_name)[horizon] for out in outputs]

            row[f"{label}_cross_rate"] = crossing
            row[f"{label}_median_delay_detected"] = "" if delay is None else delay
            row[f"{label}_median_loge"] = median(logs)

        rows.append(row)

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=200)
    parser.add_argument(
        "--output",
        default="results/pminus1_killtest10_comparison.csv",
    )
    return parser.parse_args()


def main() -> int:
    kt9.validate_beta_rank_probs()

    args = parse_args()
    if args.reps <= 0:
        raise SystemExit("--reps must be positive")

    print("P−1 Kill-Test 10 — matched baseline comparison")
    print(
        f"K={K} M={M} n={N} alpha={ALPHA} delta={DELTA} "
        f"conditional_alpha={COND_ALPHA:.8f} reps={args.reps}"
    )
    print(
        f"eps_clean={EPS_CLEAN:.6f} eps_sym={EPS_SYM:.6f} "
        f"PRM_threshold={math.exp(LOG_PRM_THRESHOLD):.3f} "
        f"band_threshold={math.exp(LOG_BAND_THRESHOLD):.3f}"
    )
    print("")

    all_rows: list[dict[str, object]] = []

    for gamma in TRUE_GAMMAS:
        rows = run_condition(args.reps, gamma)
        all_rows.extend(rows)

        for row in rows:
            print(
                "{condition:>7} T={horizon:3d} "
                "static={static_cross_rate:.3f} "
                "band={band_cross_rate:.3f} "
                "cctm={cctm_cross_rate:.3f} "
                "oracle={oracle_cross_rate:.3f} "
                "dkw_good={dkw_good_rate:.3f}".format(**row)
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    print("")
    print("=== DECISION AIDS ===")
    for gamma in (4.0, 8.0):
        rows = [
            row for row in all_rows
            if row["true_gamma"] == gamma and row["horizon"] == 200
        ]
        row = rows[0]
        print(
            f"gamma={gamma:g} T=200 "
            f"static={row['static_cross_rate']:.3f} "
            f"band={row['band_cross_rate']:.3f} "
            f"cctm={row['cctm_cross_rate']:.3f} "
            f"oracle={row['oracle_cross_rate']:.3f}"
        )

    print(f"CSV: {output}")
    print("KILLTEST10: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
