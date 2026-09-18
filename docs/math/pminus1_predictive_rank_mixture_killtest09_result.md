# P−1 Kill-Test 09 Result — adaptive-mixture predictive ranks

Status: **PASS power gate / candidate survives this kill-test**

Date: 2026-09-18

## Configuration

- K = 8
- M = 2
- n = 6 clean references
- alpha = 0.05
- 200 Monte Carlo repetitions per scenario
- 23 mixture components
- 5% constant-one hedge
- true contamination positions = (7, 8)
- horizons T in {40, 100, 200}
- alternatives Beta(gamma,1) with gamma in {2,4,8}

## Results

### Null

| T | robust crossing | oracle crossing | median max logE robust | median max logE oracle |
|---:|---:|---:|---:|---:|
| 40 | 0.000 | 0.020 | -0.4554 | 0.3027 |
| 100 | 0.010 | 0.035 | -0.5247 | 0.0872 |
| 200 | 0.000 | 0.025 | -0.4554 | 0.1653 |

Maximum robust null crossing observed: 0.01, below nominal alpha=0.05 in this finite simulation.

### Alternative gamma=2

| T | robust crossing | oracle crossing | median max logE robust | median max logE oracle |
|---:|---:|---:|---:|---:|
| 40 | 0.025 | 0.220 | -0.0390 | 1.2382 |
| 100 | 0.060 | 0.230 | -0.0390 | 1.3951 |
| 200 | 0.040 | 0.255 | -0.0390 | 1.4115 |

Weak shift remains difficult for the robust procedure.

### Alternative gamma=4

| T | robust crossing | oracle crossing | median max logE robust | median max logE oracle |
|---:|---:|---:|---:|---:|
| 40 | 0.230 | 0.590 | 0.7415 | 4.0415 |
| 100 | 0.370 | 0.720 | 1.9445 | 4.9142 |
| 200 | 0.455 | 0.800 | 2.6465 | 5.9759 |

Robust power increases clearly with horizon.

### Alternative gamma=8

| T | robust crossing | oracle crossing | median max logE robust | median max logE oracle |
|---:|---:|---:|---:|---:|
| 40 | 0.580 | 0.930 | 3.5623 | 7.3460 |
| 100 | 0.715 | 0.955 | 5.2695 | 8.8774 |
| 200 | 0.800 | 0.960 | 6.5086 | 10.5399 |

Robust power is strong and increases with horizon.

## Decision

**Kill-Test 09 survives.**

The failure in Kill-Test 08 was not a fundamental impossibility result. A broader valid adaptive mixture restores substantial robust power while keeping the simulated null crossing rate low.

This specifically supports the “bettor mismatch” explanation for Kill-Test 08.

The candidate should now advance to the next gate, but novelty is still not established.

## Key scientific observation

The robust/oracle gap remains substantial, especially at moderate signal strength, but the robust detector is no longer powerless:

- gamma=4 reaches 45.5% robust crossing at T=200;
- gamma=8 reaches 80.0% robust crossing at T=200.

The worst contamination candidate is frequently (1,2) under strong alternatives, not the true contamination set (7,8). This shows that the robust minimum is driven by a pessimistic but fixed alternative contamination interpretation. The method nevertheless accumulates usable evidence once bettor mismatch is mitigated.

## Next gate

Before claiming a new method, compare this exact static-coupling construction against the strongest generic baseline:

1. CCTM / confidence-band robustification;
2. the DP/static-coupling method with the adaptive mixture;
3. oracle clean-subset predictive-rank martingale.

The next experiment should compare power/delay at matched anytime-valid type-I control across K, M, and signal strength.

No additional hardware work is justified yet.
