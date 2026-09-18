#!/usr/bin/env python3
"""Kill-Test 13: final baseline-strength audit.

The static-coupling method is frozen. This script strengthens the generic
confidence-band baselines via a pre-specified delta sweep, adaptive ONS
betting for the exact-count lower band, and a safe one-sided CCTM D sweep.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pminus1_nonvacuous_strong_killtest12 as base


ALPHA = 0.05
DELTA_GRID = (0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045)
CCTM_D_GRID = (0.50, 0.90, 0.99)
BAND_ONS_D = 0.99
ONS_SCALE = 2.0 / (2.0 - math.log(3.0))

K_VALUES = base.K_VALUES
HORIZONS = base.HORIZONS
MAX_T = base.MAX_T
TRUE_GAMMAS = base.TRUE_GAMMAS
M = base.M
SEED = base.SEED

BAND_ETAS = base.BAND_ETAS
BAND_HEDGE = base.BAND_HEDGE
LOG_STATIC_THRESHOLD = math.log(1.0 / ALPHA)


@dataclass(frozen=True)
class DeltaConfig:
    delta: float
    cond_alpha: float
    log_threshold: float
    eps_clean: float
    eps_sym: float


def delta_configs(k: int, n: int) -> tuple[DeltaConfig, ...]:
    configs = []
    for delta in DELTA_GRID:
        cond_alpha = (ALPHA - delta) / (1.0 - delta)
        if cond_alpha <= 0.0:
            raise ValueError("delta must be strictly below alpha")
        eps_clean = math.sqrt(math.log(2.0 / delta) / (2.0 * n))
        eps_sym = (n / k) * eps_clean + M / k
        configs.append(
            DeltaConfig(
                delta=delta,
                cond_alpha=cond_alpha,
                log_threshold=math.log(1.0 / cond_alpha),
                eps_clean=eps_clean,
                eps_sym=eps_sym,
            )
        )
    return tuple(configs)


@dataclass
class BandONS:
    eta: float = 0.0
    a: float = 1.0
    log_wealth: float = 0.0

    def step(self, h: float) -> float:
        bet = 1.0 + self.eta * h
        if bet <= 0.0:
            raise RuntimeError(f"nonpositive band-ONS factor: {bet}")

        self.log_wealth += math.log(bet)

        z = h / bet
        self.a += z * z
        eta_new = self.eta + ONS_SCALE * z / self.a
        self.eta = min(BAND_ONS_D, max(0.0, eta_new))
        return self.log_wealth


@dataclass
class CCTMOneSided:
    eps_sym: float
    d_bound: float
    eta: float = 0.0
    a: float = 1.0
    log_wealth: float = 0.0

    def step(self, u: float) -> float:
        if self.eta > 0.0:
            sign = 1.0
        elif self.eta < 0.0:
            sign = -1.0
        else:
            sign = 0.0

        v = (u - 0.5 - sign * self.eps_sym) / (0.5 + self.eps_sym)
        bet = 1.0 + self.eta * v
        if bet <= 0.0:
            raise RuntimeError(
                f"nonpositive CCTM factor={bet} eta={self.eta} D={self.d_bound}"
            )

        self.log_wealth += math.log(bet)

        z = v / bet
        self.a += z * z
        eta_new = self.eta + ONS_SCALE * z / self.a
        self.eta = min(self.d_bound, max(0.0, eta_new))
        return self.log_wealth


@dataclass
class BaselineState:
    fixed_logs: np.ndarray
    ons: BandONS
    cctm: dict[float, CCTMOneSided]


def new_baseline_state(dc: DeltaConfig) -> BaselineState:
    return BaselineState(
        fixed_logs=np.zeros(len(BAND_ETAS), dtype=float),
        ons=BandONS(),
        cctm={
            d: CCTMOneSided(eps_sym=dc.eps_sym, d_bound=d)
            for d in CCTM_D_GRID
        },
    )


def logsumexp(values: np.ndarray) -> float:
    m = float(np.max(values))
    return m + math.log(float(np.exp(values - m).sum()))


def fixed_band_log(state: BaselineState) -> float:
    alt_weight = (1.0 - BAND_HEDGE) / len(BAND_ETAS)
    terms = np.concatenate(
        (
            np.asarray([math.log(BAND_HEDGE)]),
            math.log(alt_weight) + state.fixed_logs,
        )
    )
    return logsumexp(terms)


def lower_band(q: int, n: int, eps_clean: float) -> float:
    clean_low = max(0, q - M)
    return max(0.0, clean_low / n - eps_clean)


@dataclass(frozen=True)
class PathSummary:
    static_stop: int | None
    oracle_stop: int | None
    static_logs: dict[int, float]
    oracle_logs: dict[int, float]
    baseline_stops: dict[tuple[str, float, float | None], int | None]
    baseline_logs: dict[
        tuple[str, float, float | None],
        dict[int, float],
    ]


def evaluate_path(
    cfg: base.Config,
    ranks: list[int],
) -> PathSummary:
    static_state = base.fresh_static_state(cfg)

    dconfigs = delta_configs(cfg.k, cfg.n)
    states = {dc.delta: new_baseline_state(dc) for dc in dconfigs}

    static_stop = None
    oracle_stop = None
    static_logs: dict[int, float] = {}
    oracle_logs: dict[int, float] = {}

    baseline_stops: dict[tuple[str, float, float | None], int | None] = {}
    baseline_logs: dict[
        tuple[str, float, float | None],
        dict[int, float],
    ] = {}

    for dc in dconfigs:
        for key in (
            ("band_mix", dc.delta, None),
            ("band_ons", dc.delta, None),
        ):
            baseline_stops[key] = None
            baseline_logs[key] = {}
        for d in CCTM_D_GRID:
            key = ("cctm", dc.delta, d)
            baseline_stops[key] = None
            baseline_logs[key] = {}

    for t, q in enumerate(ranks, start=1):
        static_log, oracle_log = base.update_static_state(
            cfg, static_state, q, t
        )

        if static_stop is None and static_log >= LOG_STATIC_THRESHOLD:
            static_stop = t
        if oracle_stop is None and oracle_log >= LOG_STATIC_THRESHOLD:
            oracle_stop = t

        if t in HORIZONS:
            static_logs[t] = static_log
            oracle_logs[t] = oracle_log

        u = q / cfg.k

        for dc in dconfigs:
            st = states[dc.delta]
            lower = lower_band(q, cfg.n, dc.eps_clean)
            h = 2.0 * (lower - 0.5)

            factors = 1.0 + BAND_ETAS * h
            if np.any(factors <= 0.0):
                raise RuntimeError("nonpositive fixed-band factor")
            st.fixed_logs += np.log(factors)
            mix_log = fixed_band_log(st)

            ons_log = st.ons.step(h)

            key_mix = ("band_mix", dc.delta, None)
            key_ons = ("band_ons", dc.delta, None)

            if (
                baseline_stops[key_mix] is None
                and mix_log >= dc.log_threshold
            ):
                baseline_stops[key_mix] = t
            if (
                baseline_stops[key_ons] is None
                and ons_log >= dc.log_threshold
            ):
                baseline_stops[key_ons] = t

            if t in HORIZONS:
                baseline_logs[key_mix][t] = mix_log
                baseline_logs[key_ons][t] = ons_log

            for d in CCTM_D_GRID:
                key = ("cctm", dc.delta, d)
                cctm_log = st.cctm[d].step(u)
                if (
                    baseline_stops[key] is None
                    and cctm_log >= dc.log_threshold
                ):
                    baseline_stops[key] = t
                if t in HORIZONS:
                    baseline_logs[key][t] = cctm_log

    return PathSummary(
        static_stop=static_stop,
        oracle_stop=oracle_stop,
        static_logs=static_logs,
        oracle_logs=oracle_logs,
        baseline_stops=baseline_stops,
        baseline_logs=baseline_logs,
    )


def median(values: list[float]) -> float | None:
    if not values:
        return None
    return float(np.median(np.asarray(values, dtype=float)))


def scenario_seed(k: int, true_gamma: float | None) -> int:
    gamma_code = 0 if true_gamma is None else int(1000 * true_gamma)
    return SEED + 1_000_000 * k + 100_000 * gamma_code


def summarize_method(
    outputs: list[PathSummary],
    horizon: int,
    method: str,
    delta: float | None,
    d_bound: float | None,
) -> dict[str, object]:
    if method == "static":
        stops = [
            out.static_stop
            for out in outputs
            if out.static_stop is not None and out.static_stop <= horizon
        ]
        logs = [out.static_logs[horizon] for out in outputs]
        threshold = 1.0 / ALPHA
    elif method == "oracle":
        stops = [
            out.oracle_stop
            for out in outputs
            if out.oracle_stop is not None and out.oracle_stop <= horizon
        ]
        logs = [out.oracle_logs[horizon] for out in outputs]
        threshold = 1.0 / ALPHA
    else:
        assert delta is not None
        key = (method, delta, d_bound)
        stops = [
            out.baseline_stops[key]
            for out in outputs
            if out.baseline_stops[key] is not None
            and out.baseline_stops[key] <= horizon
        ]
        logs = [out.baseline_logs[key][horizon] for out in outputs]
        cond_alpha = (ALPHA - delta) / (1.0 - delta)
        threshold = 1.0 / cond_alpha

    delay = median([float(s) for s in stops])
    return {
        "cross_rate": len(stops) / len(outputs),
        "median_delay_detected": "" if delay is None else delay,
        "median_loge": median(logs),
        "threshold": threshold,
    }


def run_condition(
    cfg: base.Config,
    reps: int,
    true_gamma: float | None,
) -> list[dict[str, object]]:
    rng = random.Random(scenario_seed(cfg.k, true_gamma))
    outputs: list[PathSummary] = []

    for _ in range(reps):
        _clean, ranks = base.generate_path(cfg, rng, true_gamma)
        outputs.append(evaluate_path(cfg, ranks))

    condition = "null" if true_gamma is None else f"beta_{true_gamma:g}"
    rows: list[dict[str, object]] = []

    for horizon in HORIZONS:
        for method in ("static", "oracle"):
            stats = summarize_method(
                outputs, horizon, method, None, None
            )
            rows.append(
                {
                    "K": cfg.k,
                    "M": cfg.m,
                    "condition": condition,
                    "true_gamma": "" if true_gamma is None else true_gamma,
                    "horizon": horizon,
                    "reps": reps,
                    "method": method,
                    "delta": "",
                    "D": "",
                    **stats,
                }
            )

        for delta in DELTA_GRID:
            for method in ("band_mix", "band_ons"):
                stats = summarize_method(
                    outputs, horizon, method, delta, None
                )
                rows.append(
                    {
                        "K": cfg.k,
                        "M": cfg.m,
                        "condition": condition,
                        "true_gamma": "" if true_gamma is None else true_gamma,
                        "horizon": horizon,
                        "reps": reps,
                        "method": method,
                        "delta": delta,
                        "D": "",
                        **stats,
                    }
                )

            for d in CCTM_D_GRID:
                stats = summarize_method(
                    outputs, horizon, "cctm", delta, d
                )
                rows.append(
                    {
                        "K": cfg.k,
                        "M": cfg.m,
                        "condition": condition,
                        "true_gamma": "" if true_gamma is None else true_gamma,
                        "horizon": horizon,
                        "reps": reps,
                        "method": "cctm",
                        "delta": delta,
                        "D": d,
                        **stats,
                    }
                )

    return rows


def delay_value(row: dict[str, object]) -> float:
    value = row["median_delay_detected"]
    if value == "":
        return float("inf")
    return float(value)


def best_row(
    rows: list[dict[str, object]],
    method: str,
) -> dict[str, object]:
    candidates = [row for row in rows if row["method"] == method]
    return max(
        candidates,
        key=lambda row: (
            float(row["cross_rate"]),
            -delay_value(row),
            float(row["median_loge"]),
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=200)
    parser.add_argument(
        "--output",
        default="results/pminus1_killtest13_baseline_strength.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.reps <= 0:
        raise SystemExit("--reps must be positive")

    configs = [base.build_config(k) for k in K_VALUES]

    print("P−1 Kill-Test 13 — final baseline-strength audit")
    print(
        f"alpha={ALPHA} reps={args.reps} "
        f"deltas={DELTA_GRID} cctm_D={CCTM_D_GRID}"
    )
    print("static method frozen; baseline grid is oracle-tuned only for comparison")
    print("")

    all_rows: list[dict[str, object]] = []

    for cfg in configs:
        for gamma in TRUE_GAMMAS:
            rows = run_condition(cfg, args.reps, gamma)
            all_rows.extend(rows)

            horizon_rows = [
                row for row in rows
                if int(row["horizon"]) == 200
            ]
            static = next(
                row for row in horizon_rows if row["method"] == "static"
            )
            oracle = next(
                row for row in horizon_rows if row["method"] == "oracle"
            )
            best_mix = best_row(horizon_rows, "band_mix")
            best_ons = best_row(horizon_rows, "band_ons")
            best_cctm = best_row(horizon_rows, "cctm")

            condition = static["condition"]
            print(
                f"K={cfg.k:2d} {condition:>7} T=200 "
                f"static={float(static['cross_rate']):.3f} "
                f"band_mix={float(best_mix['cross_rate']):.3f}"
                f"(d={float(best_mix['delta']):.3f}) "
                f"band_ons={float(best_ons['cross_rate']):.3f}"
                f"(d={float(best_ons['delta']):.3f}) "
                f"cctm={float(best_cctm['cross_rate']):.3f}"
                f"(d={float(best_cctm['delta']):.3f},D={float(best_cctm['D']):.2f}) "
                f"oracle={float(oracle['cross_rate']):.3f}"
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    print("")
    print("=== PRIMARY DECISION AIDS ===")
    for k in K_VALUES:
        for gamma in (4.0, 8.0):
            subset = [
                row for row in all_rows
                if row["K"] == k
                and row["true_gamma"] == gamma
                and row["horizon"] == 200
            ]
            static = next(row for row in subset if row["method"] == "static")
            oracle = next(row for row in subset if row["method"] == "oracle")
            best_mix = best_row(subset, "band_mix")
            best_ons = best_row(subset, "band_ons")
            best_cctm = best_row(subset, "cctm")
            strongest = max(
                (best_mix, best_ons, best_cctm),
                key=lambda row: (
                    float(row["cross_rate"]),
                    -delay_value(row),
                    float(row["median_loge"]),
                ),
            )
            gap = float(static["cross_rate"]) - float(strongest["cross_rate"])
            print(
                f"K={k} gamma={gamma:g} "
                f"static={float(static['cross_rate']):.3f} "
                f"strongest={strongest['method']}:{float(strongest['cross_rate']):.3f} "
                f"gap={gap:.3f} "
                f"oracle={float(oracle['cross_rate']):.3f}"
            )

    print("")
    print("NOTE: best-grid baseline is an ex-post oracle-tuned benchmark,")
    print("not a single precommitted level-alpha procedure.")
    print(f"CSV: {output}")
    print("KILLTEST13: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
