#!/usr/bin/env python3
"""Kill-Test 12: non-vacuous baseline comparison.

Compare static-coupling predictive ranks against informative generic
confidence-band baselines at K=24 and K=32, M=2.

NumPy is used only to vectorize the candidate/component state updates.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import itertools
import math
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np


SEED = 20260918
M = 2
ALPHA = 0.05
DELTA = ALPHA / 2.0
COND_ALPHA = (ALPHA - DELTA) / (1.0 - DELTA)

K_VALUES = (24, 32)
HORIZONS = (40, 100, 200)
MAX_T = max(HORIZONS)
TRUE_GAMMAS: tuple[float | None, ...] = (None, 2.0, 4.0, 8.0)

GAMMA_GRID = (1.25, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0)
SYMMETRIC_ALPHA = (0.1, 0.25, 0.5)
TILT_TOTAL = (1.0, 3.5, 7.0)
TILT_BETA = (0.5, 1.0, 2.0, 4.0)
HEDGE_WEIGHT = 0.05

BAND_ETAS = np.asarray((0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95), dtype=float)
BAND_HEDGE = 0.05

CCTM_D = 0.5
CCTM_SMOOTH = 1e-6

LOG_PRM_THRESHOLD = math.log(1.0 / ALPHA)
LOG_BAND_THRESHOLD = math.log(1.0 / COND_ALPHA)


def logsumexp_1d(values: np.ndarray) -> float:
    m = float(np.max(values))
    return m + math.log(float(np.exp(values - m).sum()))


def logsumexp_rows(values: np.ndarray) -> np.ndarray:
    m = np.max(values, axis=1, keepdims=True)
    return m[:, 0] + np.log(np.exp(values - m).sum(axis=1))


def median(values: list[float]) -> float | None:
    if not values:
        return None
    return float(np.median(np.asarray(values, dtype=float)))


def beta_rank_probs(n: int, gamma: float) -> np.ndarray:
    probs = []
    for j in range(n + 1):
        logp = (
            math.lgamma(n + 1)
            - math.lgamma(j + 1)
            + math.log(gamma)
            + math.lgamma(j + gamma)
            - math.lgamma(n + gamma + 1)
        )
        probs.append(math.exp(logp))
    arr = np.asarray(probs, dtype=float)
    arr /= arr.sum()
    return arr


def validate_beta_rank_probs(n: int) -> None:
    probs = beta_rank_probs(n, 1.0)
    target = np.full(n + 1, 1.0 / (n + 1), dtype=float)
    err = float(np.max(np.abs(probs - target)))
    if err > 1e-12:
        raise AssertionError(f"gamma=1 rank law is not uniform: err={err:.3e}")


@dataclass(frozen=True)
class ComponentFamily:
    fixed_probs: np.ndarray
    dirichlet_alpha: np.ndarray

    @property
    def n_fixed(self) -> int:
        return self.fixed_probs.shape[0]

    @property
    def n_dirichlet(self) -> int:
        return self.dirichlet_alpha.shape[0]

    @property
    def total_components(self) -> int:
        return self.n_fixed + self.n_dirichlet


def build_components(n: int) -> ComponentFamily:
    fixed = np.stack(
        [beta_rank_probs(n, gamma) for gamma in GAMMA_GRID],
        axis=0,
    )

    alphas: list[np.ndarray] = []
    for alpha in SYMMETRIC_ALPHA:
        alphas.append(np.full(n + 1, alpha, dtype=float))

    for total in TILT_TOTAL:
        for beta in TILT_BETA:
            weights = np.exp(beta * np.arange(n + 1, dtype=float) / n)
            weights /= weights.sum()
            alphas.append(total * weights)

    return ComponentFamily(
        fixed_probs=fixed,
        dirichlet_alpha=np.stack(alphas, axis=0),
    )


@dataclass(frozen=True)
class Config:
    k: int
    m: int
    n: int
    candidates: tuple[tuple[int, ...], ...]
    rank_maps: np.ndarray
    true_candidate_index: int
    components: ComponentFamily
    eps_clean: float
    eps_sym: float


def build_config(k: int) -> Config:
    n = k - M
    validate_beta_rank_probs(n)

    candidates = tuple(itertools.combinations(range(1, k + 1), M))
    rank_maps = np.empty((len(candidates), k + 1), dtype=np.int16)

    for i, candidate in enumerate(candidates):
        for q in range(k + 1):
            rank_maps[i, q] = q - sum(c <= q for c in candidate)

    true_c = tuple(range(k - M + 1, k + 1))
    true_idx = candidates.index(true_c)

    eps_clean = math.sqrt(math.log(2.0 / DELTA) / (2.0 * n))
    eps_sym = (n / k) * eps_clean + M / k

    return Config(
        k=k,
        m=M,
        n=n,
        candidates=candidates,
        rank_maps=rank_maps,
        true_candidate_index=true_idx,
        components=build_components(n),
        eps_clean=eps_clean,
        eps_sym=eps_sym,
    )


@dataclass
class StaticState:
    counts: np.ndarray
    log_wealth: np.ndarray


def fresh_static_state(cfg: Config) -> StaticState:
    c = len(cfg.candidates)
    h = cfg.components.total_components
    return StaticState(
        counts=np.zeros((c, cfg.n + 1), dtype=np.int32),
        log_wealth=np.zeros((c, h), dtype=float),
    )


def update_static_state(
    cfg: Config,
    state: StaticState,
    observed_rank: int,
    t: int,
) -> tuple[float, float]:
    c_count = len(cfg.candidates)
    candidate_idx = np.arange(c_count)
    ranks = cfg.rank_maps[:, observed_rank]
    old_count = state.counts[candidate_idx, ranks].astype(float)

    p0 = (old_count + 1.0) / (cfg.n + t)

    fixed = cfg.components.fixed_probs[:, ranks].T

    alpha = cfg.components.dirichlet_alpha[:, ranks].T
    alpha_totals = cfg.components.dirichlet_alpha.sum(axis=1)
    dirichlet = (
        old_count[:, None] + alpha
    ) / ((t - 1.0) + alpha_totals[None, :])

    q = np.concatenate((fixed, dirichlet), axis=1)
    state.log_wealth += np.log(q / p0[:, None])
    state.counts[candidate_idx, ranks] += 1

    h = cfg.components.total_components
    alt_weight = (1.0 - HEDGE_WEIGHT) / h
    terms = np.concatenate(
        (
            np.full((c_count, 1), math.log(HEDGE_WEIGHT), dtype=float),
            math.log(alt_weight) + state.log_wealth,
        ),
        axis=1,
    )
    candidate_log_mix = logsumexp_rows(terms)

    static_log = float(np.min(candidate_log_mix))
    oracle_log = float(candidate_log_mix[cfg.true_candidate_index])
    return static_log, oracle_log


def contaminated_band_lower(cfg: Config, q: int) -> float:
    clean_count_low = max(0, q - cfg.m)
    return max(0.0, clean_count_low / cfg.n - cfg.eps_clean)


def dkw_good(clean_reference: list[float], eps: float) -> bool:
    xs = sorted(clean_reference)
    n = len(xs)
    d_plus = max((i + 1) / n - x for i, x in enumerate(xs))
    d_minus = max(x - i / n for i, x in enumerate(xs))
    return max(d_plus, d_minus) <= eps


@dataclass
class CCTMState:
    eps_sym: float
    eta: float = 0.0
    a: float = 1.0
    log_wealth: float = 0.0

    def step(self, u: float) -> float:
        eta = self.eta
        smooth = CCTM_SMOOTH
        denom = 0.5 + (1.0 + smooth) * self.eps_sym

        root = math.sqrt(eta * eta + smooth * smooth)
        v_dot_eta = (
            eta * (u - 0.5) - root * self.eps_sym
        ) / denom

        bet = 1.0 + v_dot_eta
        if bet <= 0.0:
            raise RuntimeError(f"nonpositive CCTM bet={bet}")

        self.log_wealth += math.log(bet)

        dv = (
            u - 0.5 - eta * self.eps_sym / root
        ) / denom
        z = dv / bet

        self.a += z * z
        eta_new = eta + (2.0 / (2.0 - math.log(3.0))) * z / self.a
        self.eta = min(CCTM_D, max(0.0, eta_new))
        return self.log_wealth


@dataclass(frozen=True)
class PathOutput:
    stop_static: int | None
    stop_band: int | None
    stop_cctm: int | None
    stop_oracle: int | None
    logs_static: dict[int, float]
    logs_band: dict[int, float]
    logs_cctm: dict[int, float]
    logs_oracle: dict[int, float]
    dkw_good: bool


def generate_path(
    cfg: Config,
    rng: random.Random,
    true_gamma: float | None,
) -> tuple[list[float], list[int]]:
    clean = sorted(rng.random() for _ in range(cfg.n))
    observed = sorted(clean + [2.0] * cfg.m)

    if true_gamma is None:
        stream = [rng.random() for _ in range(MAX_T)]
    else:
        stream = [
            rng.betavariate(true_gamma, 1.0)
            for _ in range(MAX_T)
        ]

    ranks = [bisect.bisect_right(observed, x) for x in stream]
    return clean, ranks


def evaluate_path(
    cfg: Config,
    clean_reference: list[float],
    ranks: list[int],
) -> PathOutput:
    static = fresh_static_state(cfg)

    band_logs = np.zeros(len(BAND_ETAS), dtype=float)
    band_alt_weight = (1.0 - BAND_HEDGE) / len(BAND_ETAS)
    band_terms_constant = math.log(band_alt_weight)

    cctm = CCTMState(cfg.eps_sym)

    stop_static = None
    stop_band = None
    stop_cctm = None
    stop_oracle = None

    logs_static: dict[int, float] = {}
    logs_band: dict[int, float] = {}
    logs_cctm: dict[int, float] = {}
    logs_oracle: dict[int, float] = {}

    for t, q in enumerate(ranks, start=1):
        static_log, oracle_log = update_static_state(cfg, static, q, t)

        lower = contaminated_band_lower(cfg, q)
        h = 2.0 * (lower - 0.5)
        factors = 1.0 + BAND_ETAS * h
        if np.any(factors <= 0.0):
            raise RuntimeError("nonpositive generic-band factor")
        band_logs += np.log(factors)
        band_mix_terms = np.concatenate(
            (
                np.asarray([math.log(BAND_HEDGE)]),
                band_terms_constant + band_logs,
            )
        )
        band_log = logsumexp_1d(band_mix_terms)

        u = q / cfg.k
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
            logs_band[t] = band_log
            logs_cctm[t] = cctm_log
            logs_oracle[t] = oracle_log

    return PathOutput(
        stop_static=stop_static,
        stop_band=stop_band,
        stop_cctm=stop_cctm,
        stop_oracle=stop_oracle,
        logs_static=logs_static,
        logs_band=logs_band,
        logs_cctm=logs_cctm,
        logs_oracle=logs_oracle,
        dkw_good=dkw_good(clean_reference, cfg.eps_clean),
    )


def scenario_seed(k: int, true_gamma: float | None) -> int:
    gamma_code = 0 if true_gamma is None else int(1000 * true_gamma)
    return SEED + 1_000_000 * k + 100_000 * gamma_code


def run_condition(
    cfg: Config,
    reps: int,
    true_gamma: float | None,
) -> list[dict[str, object]]:
    rng = random.Random(scenario_seed(cfg.k, true_gamma))
    outputs: list[PathOutput] = []

    for _ in range(reps):
        clean, ranks = generate_path(cfg, rng, true_gamma)
        outputs.append(evaluate_path(cfg, clean, ranks))

    good_rate = sum(int(x.dkw_good) for x in outputs) / reps
    condition = "null" if true_gamma is None else f"beta_{true_gamma:g}"

    specs = (
        ("static", "stop_static", "logs_static"),
        ("band", "stop_band", "logs_band"),
        ("cctm", "stop_cctm", "logs_cctm"),
        ("oracle", "stop_oracle", "logs_oracle"),
    )

    rows: list[dict[str, object]] = []

    for horizon in HORIZONS:
        row: dict[str, object] = {
            "K": cfg.k,
            "M": cfg.m,
            "n": cfg.n,
            "eps_clean": cfg.eps_clean,
            "eps_sym": cfg.eps_sym,
            "condition": condition,
            "true_gamma": "" if true_gamma is None else true_gamma,
            "horizon": horizon,
            "reps": reps,
            "dkw_good_rate": good_rate,
        }

        for label, stop_attr, log_attr in specs:
            stops = [
                getattr(out, stop_attr)
                for out in outputs
                if getattr(out, stop_attr) is not None
                and getattr(out, stop_attr) <= horizon
            ]
            logs = [getattr(out, log_attr)[horizon] for out in outputs]

            row[f"{label}_cross_rate"] = len(stops) / reps
            delay = median([float(s) for s in stops])
            row[f"{label}_median_delay_detected"] = "" if delay is None else delay
            row[f"{label}_median_loge"] = median(logs)

        rows.append(row)

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=200)
    parser.add_argument(
        "--output",
        default="results/pminus1_killtest12_nonvacuous_strong.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.reps <= 0:
        raise SystemExit("--reps must be positive")

    configs = [build_config(k) for k in K_VALUES]

    print("P−1 Kill-Test 12 — non-vacuous baseline comparison")
    print(
        f"alpha={ALPHA} delta={DELTA} conditional_alpha={COND_ALPHA:.8f} "
        f"reps={args.reps}"
    )
    print(
        f"PRM_threshold={math.exp(LOG_PRM_THRESHOLD):.3f} "
        f"band_threshold={math.exp(LOG_BAND_THRESHOLD):.3f}"
    )
    for cfg in configs:
        print(
            f"K={cfg.k} M={cfg.m} n={cfg.n} candidates={len(cfg.candidates)} "
            f"eps_clean={cfg.eps_clean:.6f} eps_sym={cfg.eps_sym:.6f}"
        )
    print("")

    all_rows: list[dict[str, object]] = []

    for cfg in configs:
        for gamma in TRUE_GAMMAS:
            rows = run_condition(cfg, args.reps, gamma)
            all_rows.extend(rows)

            for row in rows:
                print(
                    "K={K:2d} {condition:>7} T={horizon:3d} "
                    "static={static_cross_rate:.3f} "
                    "band={band_cross_rate:.3f} "
                    "cctm={cctm_cross_rate:.3f} "
                    "oracle={oracle_cross_rate:.3f} "
                    "dkw={dkw_good_rate:.3f}".format(**row)
                )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    print("")
    print("=== DECISION AIDS ===")
    for k in K_VALUES:
        for gamma in (4.0, 8.0):
            row = next(
                r for r in all_rows
                if r["K"] == k
                and r["true_gamma"] == gamma
                and r["horizon"] == 200
            )
            print(
                f"K={k} gamma={gamma:g} T=200 "
                f"static={row['static_cross_rate']:.3f} "
                f"band={row['band_cross_rate']:.3f} "
                f"cctm={row['cctm_cross_rate']:.3f} "
                f"oracle={row['oracle_cross_rate']:.3f}"
            )

    print(f"CSV: {output}")
    print("KILLTEST11: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
