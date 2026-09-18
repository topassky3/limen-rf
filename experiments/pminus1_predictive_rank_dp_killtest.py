#!/usr/bin/env python3
"""P-1 kill-test: robust predictive ranks under static reference contamination.

This script checks an exact dynamic-programming reduction against brute-force
enumeration and runs a small seeded diagnostic. It is a theorem/novelty gate,
not a final detector benchmark.
"""

from __future__ import annotations

import bisect
import itertools
import math
import random
import time
from collections.abc import Iterable


SEED = 20260918


def beta_rank_alt_probs(n: int, gamma: float) -> list[float]:
    """Marginal rank probabilities induced by U ~ Beta(gamma, 1)."""
    out: list[float] = []
    for j in range(n + 1):
        logp = (
            math.lgamma(n + 1)
            - math.lgamma(j + 1)
            - math.lgamma(n - j + 1)
            + math.log(gamma)
            + math.lgamma(j + gamma)
            + math.lgamma(n - j + 1)
            - math.lgamma(n + gamma + 1)
        )
        out.append(math.exp(logp))
    total = sum(out)
    return [value / total for value in out]


def clean_rank(q: int, contamination_positions: tuple[int, ...]) -> int:
    return q - sum(c <= q for c in contamination_positions)


def candidate_log_wealth(
    rank_hist: list[int],
    k: int,
    contamination_positions: tuple[int, ...],
    gamma: float,
) -> float:
    m = len(contamination_positions)
    n = k - m
    counts = [0] * (n + 1)
    for q, count in enumerate(rank_hist):
        r = clean_rank(q, contamination_positions)
        counts[r] += count

    alt = beta_rank_alt_probs(n, gamma)
    t = sum(rank_hist)
    value = math.lgamma(n + t + 1) - math.lgamma(n + 1)
    for j, count in enumerate(counts):
        value += count * math.log(alt[j]) - math.lgamma(count + 1)
    return value


def brute_force_min_log_wealth(
    rank_hist: list[int],
    k: int,
    m: int,
    gamma: float,
) -> float:
    return min(
        candidate_log_wealth(rank_hist, k, c, gamma)
        for c in itertools.combinations(range(1, k + 1), m)
    )


def dp_min_log_wealth(
    rank_hist: list[int],
    k: int,
    m: int,
    gamma: float,
) -> float:
    """Exact min over all size-m static contamination-position sets."""
    if len(rank_hist) != k + 1:
        raise ValueError("rank_hist must have K+1 bins")
    if not 0 <= m <= k:
        raise ValueError("m must satisfy 0 <= m <= K")

    n = k - m
    groups_total = n + 1
    bins_total = k + 1
    alt = beta_rank_alt_probs(n, gamma)

    prefix = [0]
    for value in rank_hist:
        prefix.append(prefix[-1] + value)

    inf = float("inf")
    dp = [[inf] * (m + 1) for _ in range(bins_total + 1)]
    dp[0][0] = 0.0

    for b in range(bins_total):
        for deleted in range(m + 1):
            current = dp[b][deleted]
            if not math.isfinite(current):
                continue

            groups_formed = b - deleted
            if groups_formed >= groups_total:
                continue

            max_segment_len = min(
                bins_total - b,
                m - deleted + 1,
            )

            for seg_len in range(1, max_segment_len + 1):
                b2 = b + seg_len
                deleted2 = deleted + seg_len - 1
                groups_formed2 = groups_formed + 1

                if bins_total - b2 < groups_total - groups_formed2:
                    continue

                count = prefix[b2] - prefix[b]
                group_index = groups_formed
                cost = (
                    count * math.log(alt[group_index])
                    - math.lgamma(count + 1)
                )
                candidate = current + cost
                if candidate < dp[b2][deleted2]:
                    dp[b2][deleted2] = candidate

    t = sum(rank_hist)
    constant = math.lgamma(n + t + 1) - math.lgamma(n + 1)
    return constant + dp[bins_total][m]


def robust_min_log_wealth(
    rank_hist: list[int],
    k: int,
    max_m: int,
    gamma: float,
    exact_m: bool,
) -> float:
    ms: Iterable[int] = [max_m] if exact_m else range(max_m + 1)
    return min(dp_min_log_wealth(rank_hist, k, m, gamma) for m in ms)


def dkw_replacement_halfwidth(k: int, m: int, delta: float) -> float:
    return math.sqrt(math.log(2.0 / delta) / (2.0 * k)) + m / k


def validate_dp() -> None:
    rng = random.Random(SEED)
    k = 8
    max_m = 2
    hist = [rng.randrange(0, 11) for _ in range(k + 1)]
    gamma = 4.0

    print("=== EXACT DP VS BRUTE FORCE ===")
    print(f"seed={SEED} K={k} M={max_m} hist={hist}")
    for m in range(max_m + 1):
        brute = brute_force_min_log_wealth(hist, k, m, gamma)
        dp = dp_min_log_wealth(hist, k, m, gamma)
        err = abs(brute - dp)
        print(
            f"m={m} brute={brute:.12f} dp={dp:.12f} "
            f"abs_error={err:.3e}"
        )
        if err > 1e-10:
            raise AssertionError(f"DP mismatch for m={m}: {err}")
    print("DP_EXACTNESS: PASS")


def benchmark_dp() -> None:
    rng = random.Random(SEED + 1)
    k = 50
    m = 5
    hist = [rng.randrange(0, 30) for _ in range(k + 1)]
    gamma = 4.0
    brute_candidates = math.comb(k, m)

    start = time.perf_counter()
    result = dp_min_log_wealth(hist, k, m, gamma)
    elapsed = time.perf_counter() - start

    print("\n=== POLYNOMIAL-TIME BENCHMARK ===")
    print(f"K={k} M={m}")
    print(f"brute_force_subsets=C(K,M)={brute_candidates:,}")
    print(f"dp_log_wealth={result:.9f}")
    print(f"dp_elapsed_seconds={elapsed:.6f}")


def simulated_observed_ranks(
    rng: random.Random,
    k: int,
    m: int,
    t: int,
    alternative_gamma: float | None,
) -> tuple[list[int], tuple[int, ...]]:
    """Model A: n clean U(0,1) references plus m fixed high contaminants."""
    n = k - m
    clean = sorted(rng.random() for _ in range(n))
    observed = clean + [2.0] * m
    observed.sort()

    if alternative_gamma is None:
        stream = [rng.random() for _ in range(t)]
    else:
        stream = [rng.betavariate(alternative_gamma, 1.0) for _ in range(t)]

    ranks = [bisect.bisect_right(observed, x) for x in stream]
    true_contamination = tuple(range(k - m + 1, k + 1))
    return ranks, true_contamination


def oracle_log_wealth_from_sequence(
    ranks: list[int],
    k: int,
    contamination_positions: tuple[int, ...],
    gamma: float,
) -> float:
    hist = [0] * (k + 1)
    for q in ranks:
        hist[q] += 1
    return candidate_log_wealth(hist, k, contamination_positions, gamma)


def path_max_log_wealth(
    ranks: list[int],
    k: int,
    m: int,
    gamma: float,
) -> tuple[float, float]:
    hist = [0] * (k + 1)
    prefix: list[int] = []
    robust_max = float("-inf")
    oracle_max = float("-inf")
    true_c = tuple(range(k - m + 1, k + 1))

    for q in ranks:
        hist[q] += 1
        prefix.append(q)
        robust_now = robust_min_log_wealth(
            hist,
            k,
            m,
            gamma,
            exact_m=True,
        )
        oracle_now = oracle_log_wealth_from_sequence(
            prefix,
            k,
            true_c,
            gamma,
        )
        robust_max = max(robust_max, robust_now)
        oracle_max = max(oracle_max, oracle_now)

    return robust_max, oracle_max


def monte_carlo_diagnostic() -> None:
    k = 8
    m = 2
    t = 40
    gamma = 4.0
    alpha = 0.05
    threshold = math.log(1.0 / alpha)
    reps = 300

    def run(
        alt: float | None,
        seed_offset: int,
    ) -> tuple[float, float, float, float]:
        rng = random.Random(SEED + seed_offset)
        robust_cross = 0
        oracle_cross = 0
        robust_maxima: list[float] = []
        oracle_maxima: list[float] = []

        for _ in range(reps):
            ranks, _ = simulated_observed_ranks(rng, k, m, t, alt)
            robust_max, oracle_max = path_max_log_wealth(
                ranks,
                k,
                m,
                gamma,
            )
            robust_maxima.append(robust_max)
            oracle_maxima.append(oracle_max)
            robust_cross += robust_max >= threshold
            oracle_cross += oracle_max >= threshold

        robust_maxima.sort()
        oracle_maxima.sort()
        med = reps // 2
        return (
            robust_cross / reps,
            oracle_cross / reps,
            robust_maxima[med],
            oracle_maxima[med],
        )

    null_result = run(None, 10)
    alt_result = run(gamma, 20)

    print("\n=== SEEDED DIAGNOSTIC BETTOR ===")
    print(
        "Model A; high contaminants; exact M known; "
        f"K={k} M={m} T={t} gamma={gamma} alpha={alpha}"
    )
    print(
        "null: robust_cross={:.4f} oracle_cross={:.4f} "
        "median_max_logE_robust={:.6f} "
        "median_max_logE_oracle={:.6f}".format(*null_result)
    )
    print(
        "alt : robust_cross={:.4f} oracle_cross={:.4f} "
        "median_max_logE_robust={:.6f} "
        "median_max_logE_oracle={:.6f}".format(*alt_result)
    )
    print(
        "Guardrail: failure of this diagnostic bettor is evidence of a power "
        "problem, not a general impossibility theorem."
    )


def print_cctm_band_widths() -> None:
    delta = 0.05
    print("\n=== DKW + M/K CDF-BAND BASELINE ===")
    for k, m in [(8, 2), (12, 2), (50, 5)]:
        eps = dkw_replacement_halfwidth(k, m, delta)
        print(f"K={k:2d} M={m} delta={delta:.2f} halfwidth={eps:.6f}")


def main() -> int:
    validate_dp()
    benchmark_dp()
    print_cctm_band_widths()
    monte_carlo_diagnostic()
    print("\nKILLTEST08: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
