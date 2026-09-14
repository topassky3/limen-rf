import math

import pytest

from limen_rf.smoke import run_smoke


def test_smoke_is_deterministic() -> None:
    a = run_smoke()
    b = run_smoke()

    assert a == b


def test_smoke_statistics_are_sane() -> None:
    result = run_smoke()

    assert abs(result.sample_mean) < 0.05
    assert math.isclose(result.sample_power, 1.0, rel_tol=0.05, abs_tol=0.05)


def test_smoke_rejects_nonpositive_n() -> None:
    with pytest.raises(ValueError, match="n must be positive"):
        run_smoke(n=0)
