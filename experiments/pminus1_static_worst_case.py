from __future__ import annotations

import argparse
import json

import numpy as np


def run_kill_test(
    *,
    trials: int,
    k_total: int,
    m_contaminated: int,
    kth: int,
    gamma_shape: float,
    c_bound: float,
    seed: int,
) -> dict[str, float | int]:
    if not 0 <= m_contaminated < k_total:
        raise ValueError("m_contaminated must satisfy 0 <= M < K")
    if not 1 <= kth <= k_total:
        raise ValueError("kth must satisfy 1 <= k <= K")
    if c_bound < 1.0:
        raise ValueError("c_bound must be >= 1")
    if gamma_shape <= 0:
        raise ValueError("gamma_shape must be > 0")

    if kth <= m_contaminated:
        return {
            "trials": trials,
            "k_total": k_total,
            "m_contaminated": m_contaminated,
            "kth": kth,
            "degenerate": 1,
        }

    n_valid = k_total - m_contaminated
    q_valid = kth - m_contaminated

    rng = np.random.default_rng(seed)
    u = rng.gamma(shape=gamma_shape, scale=1.0, size=trials)
    v = rng.gamma(shape=gamma_shape, scale=1.0, size=(trials, n_valid))

    r = rng.uniform(1.0 / c_bound, c_bound, size=(trials, n_valid))
    valid = v / r

    contaminated = rng.exponential(scale=1.0, size=(trials, m_contaminated))
    combined = np.concatenate([valid, contaminated], axis=1)
    combined_k = np.partition(combined, kth - 1, axis=1)[:, kth - 1]

    worst_valid = v / c_bound
    worst_q = np.partition(worst_valid, q_valid - 1, axis=1)[:, q_valid - 1]

    z = u / (u + combined_k)
    z_worst = u / (u + worst_q)

    tolerance = 1e-12
    order_violations = int(np.count_nonzero(combined_k + tolerance < worst_q))
    z_violations = int(np.count_nonzero(z > z_worst + tolerance))

    zeros = np.zeros((trials, m_contaminated))
    equality_combined = np.concatenate([worst_valid, zeros], axis=1)
    equality_k = np.partition(equality_combined, kth - 1, axis=1)[:, kth - 1]
    max_equality_error = float(np.max(np.abs(equality_k - worst_q)))

    return {
        "trials": trials,
        "seed": seed,
        "k_total": k_total,
        "m_contaminated": m_contaminated,
        "kth": kth,
        "n_valid": n_valid,
        "q_valid": q_valid,
        "gamma_shape": gamma_shape,
        "c_bound": c_bound,
        "order_violations": order_violations,
        "z_violations": z_violations,
        "max_equality_error": max_equality_error,
        "mean_z_random_null": float(np.mean(z)),
        "mean_z_static_worst": float(np.mean(z_worst)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P-1 static worst-case coupling kill-test")
    parser.add_argument("--trials", type=int, default=100_000)
    parser.add_argument("--K", dest="k_total", type=int, default=8)
    parser.add_argument("--M", dest="m_contaminated", type=int, default=2)
    parser.add_argument("--k", dest="kth", type=int, default=6)
    parser.add_argument("--m", dest="gamma_shape", type=float, default=32.0)
    parser.add_argument("--c", dest="c_bound", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=20260915)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_kill_test(**vars(args))
    print(json.dumps(result, indent=2, sort_keys=True))

    if result.get("degenerate") == 1:
        print("P-1 STATIC KILL-TEST: DEGENERATE because k <= M")
        return

    if result["order_violations"] != 0 or result["z_violations"] != 0:
        raise SystemExit("P-1 STATIC KILL-TEST: FAIL")
    if result["max_equality_error"] > 1e-12:
        raise SystemExit("P-1 STATIC KILL-TEST: FAIL equality construction")

    print("P-1 STATIC KILL-TEST: PASS")


if __name__ == "__main__":
    main()
