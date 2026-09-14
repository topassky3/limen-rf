from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class SmokeResult:
    seed: int
    sample_mean: float
    sample_power: float
    digest: str


def run_smoke(seed: int = 20260914, n: int = 4096) -> SmokeResult:
    """Run a deterministic NumPy smoke computation for infrastructure checks."""
    if n <= 0:
        raise ValueError("n must be positive")

    rng = np.random.Generator(np.random.PCG64(seed))
    i = rng.standard_normal(n)
    q = rng.standard_normal(n)
    x = (i + 1j * q) / np.sqrt(2.0)

    sample_mean = float(np.mean(x.real))
    sample_power = float(np.mean(np.abs(x) ** 2))

    payload = {
        "seed": seed,
        "n": n,
        "sample_mean": round(sample_mean, 15),
        "sample_power": round(sample_power, 15),
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    return SmokeResult(
        seed=seed,
        sample_mean=sample_mean,
        sample_power=sample_power,
        digest=digest,
    )


def main() -> None:
    print(json.dumps(asdict(run_smoke()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
