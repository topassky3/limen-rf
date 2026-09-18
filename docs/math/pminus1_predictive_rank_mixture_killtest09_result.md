# P−1 Kill-Test 09 Result — adaptive-mixture predictive ranks

Status: **PASS power gate — corrected rerun confirmed**

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

## Exact CSV results

| condition | T | robust cross | oracle cross | med max logE robust | med max logE oracle | med final logE robust | med final logE oracle | modal worst C | frequency |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| null | 40 | 0.000 | 0.020 | -0.455406 | 0.302691 | -1.975034 | -1.515860 | (1,7) | 0.255 |
| null | 100 | 0.010 | 0.035 | -0.524667 | 0.087181 | -1.951021 | -1.672660 | (1,7) | 0.260 |
| null | 200 | 0.000 | 0.025 | -0.455406 | 0.165265 | -1.961053 | -1.753041 | (7,8) | 0.400 |
| beta_2 | 40 | 0.025 | 0.220 | -0.039038 | 1.238158 | -1.503191 | -0.179366 | (1,2) | 0.320 |
| beta_2 | 100 | 0.060 | 0.230 | -0.039038 | 1.395121 | -1.482974 | -0.212577 | (1,7) | 0.515 |
| beta_2 | 200 | 0.040 | 0.255 | -0.039038 | 1.411503 | -1.327162 | -0.115373 | (1,7) | 0.600 |
| beta_4 | 40 | 0.230 | 0.590 | 0.741542 | 4.041483 | 0.019301 | 3.055960 | (1,2) | 0.755 |
| beta_4 | 100 | 0.370 | 0.720 | 1.944488 | 4.914229 | 0.924419 | 4.099961 | (1,2) | 0.640 |
| beta_4 | 200 | 0.455 | 0.800 | 2.646468 | 5.975928 | 1.597985 | 4.631208 | (1,2) | 0.540 |
| beta_8 | 40 | 0.580 | 0.930 | 3.562315 | 7.345986 | 3.059658 | 6.810920 | (1,2) | 0.950 |
| beta_8 | 100 | 0.715 | 0.955 | 5.269478 | 8.877438 | 4.840796 | 8.031209 | (1,2) | 0.960 |
| beta_8 | 200 | 0.800 | 0.960 | 6.508636 | 10.539881 | 5.715863 | 9.714326 | (1,2) | 0.890 |

## Interpretation

### Null sanity check

The robust crossing frequencies were 0, 0.01 and 0 for T=40,100,200.

These Monte Carlo frequencies are compatible with conservative behavior, but 200 repetitions are not enough to empirically certify an alpha=0.05 guarantee. The validity claim must come from the pathwise domination theorem, not from these frequencies.

For example, 2/200 crossings at T=100 has a 95% Wilson interval of approximately 0.0027 to 0.0357.

### Weak alternative gamma=2

The robust detector remains weak:
- best crossing rate = 0.06;
- median maximum log evidence stays at about -0.039;
- median final robust log evidence remains negative.

This is a real power limitation and should not be hidden.

### Moderate alternative gamma=4

Power becomes meaningful and increases with horizon:
- 0.23 at T=40;
- 0.37 at T=100;
- 0.455 at T=200.

Median final robust log evidence changes from approximately 0.019 to 0.924 to 1.598, showing sustained rather than merely transient growth as T increases.

The robust/oracle crossing ratio improves from approximately 0.39 at T=40 to 0.57 at T=200.

### Strong alternative gamma=8

The robust detector is strong:
- 0.58 at T=40;
- 0.715 at T=100;
- 0.80 at T=200.

The robust/oracle crossing ratio improves from approximately 0.62 to 0.83 across the same horizons.

Median final robust log evidence reaches 5.716 at T=200, corresponding to median final evidence of exp(5.716) ≈ 304.

### Worst-candidate structure

Under strong alternatives the pessimistic contamination interpretation is overwhelmingly C=(1,2), despite the true contaminated positions being C*=(7,8):
- frequency 0.755 / 0.640 / 0.540 for gamma=4;
- frequency 0.950 / 0.960 / 0.890 for gamma=8.

This is scientifically important. The robust cost is not primarily caused by failure to identify the true contaminated cells. It is caused by the requirement that evidence survive an alternative admissible explanation in which the two lowest reference positions are contaminated.

As horizon increases for gamma=4, the modal frequency of C=(1,2) falls from 0.755 to 0.540 while robust power rises. This suggests that accumulating rank history can partially reduce the damage of the pessimistic contamination interpretation.

## Decision

**Kill-Test 09 survives.**

The failure in Kill-Test 08 was not a fundamental impossibility result. A broader valid adaptive mixture restores substantial robust power while retaining the pathwise anytime-valid argument under the static/exogenous contamination model.

This supports the bettor-mismatch explanation for Kill-Test 08.

However, novelty is still not established.

## Next gate

The next experiment must test whether the exact static-coupling construction contributes anything beyond a generic robust fixed-reference method.

Compare, at matched anytime-valid type-I control:

1. generic CDF-confidence-band / CCTM-style robustification;
2. static-coupling robust predictive-rank mixture;
3. oracle clean-subset predictive-rank mixture.

Primary endpoints:
- crossing probability by fixed horizon;
- stopping-time distribution / median detection delay among detected runs;
- robust/oracle efficiency gap;
- behavior across K, M and shift strength.

A fair comparison must not claim that the simple DKW+M/K half-width is itself the complete CCTM detector; the baseline must implement the corresponding valid betting construction rather than compare only confidence-band widths.

No additional hardware work is justified yet.


## Reproducibility audit correction — 2026-09-18

The original Kill-Test 09 fixed Beta-rank component contained an algebraic
implementation error: an uncancelled `-lgamma(n-j+1)` term. The output
distribution was still normalized and positive, so it remained a legitimate
betting distribution and did not invalidate the type-I/e-process argument.
It was, however, not the Beta(gamma,1)-induced rank distribution stated in the
experiment specification.

Therefore the numerical power conclusions above are now marked
**provisional**. The corrected script must be rerun using the same frozen
seed, horizons, mixture family, hedge and number of repetitions. Only that
corrected output will determine whether Kill-Test 09 remains a PASS.


## Corrected rerun confirmation — 2026-09-18

After fixing the Beta-rank probability implementation and adding the gamma=1
uniform-rank regression guard, the frozen Kill-Test 09 experiment was rerun
with the same seed, scenarios, hedge, mixture family, alpha and 200
repetitions per scenario.

### Corrected headline results

| condition | T | robust crossing | oracle crossing | median max logE robust | median max logE oracle |
|---|---:|---:|---:|---:|---:|
| null | 40 | 0.000 | 0.005 | -0.3630 | 0.3587 |
| null | 100 | 0.010 | 0.035 | -0.4459 | 0.3587 |
| null | 200 | 0.000 | 0.035 | -0.3986 | 0.3587 |
| beta_2 | 40 | 0.025 | 0.200 | 0.0348 | 1.2673 |
| beta_2 | 100 | 0.060 | 0.250 | -0.0098 | 1.3572 |
| beta_2 | 200 | 0.040 | 0.270 | 0.0348 | 1.5627 |
| beta_4 | 40 | 0.230 | 0.605 | 0.7431 | 3.6903 |
| beta_4 | 100 | 0.370 | 0.730 | 1.9445 | 4.7550 |
| beta_4 | 200 | 0.455 | 0.785 | 2.6465 | 6.0060 |
| beta_8 | 40 | 0.580 | 0.925 | 3.5623 | 6.6228 |
| beta_8 | 100 | 0.715 | 0.950 | 5.2695 | 8.5229 |
| beta_8 | 200 | 0.800 | 0.960 | 6.5086 | 10.2192 |

### Decision after correction

**PASS confirmed.**

The robust crossing rates for every scenario are unchanged from the original
run at the displayed precision:
- best gamma=2 robust crossing: 0.06;
- gamma=4 at T=200: 0.455;
- gamma=8 at T=200: 0.80;
- maximum robust null crossing: 0.01.

The oracle numbers moved modestly, as expected after correcting the fixed
Beta-rank components, but the scientific conclusion is unchanged.

This is an important reproducibility result: the observed recovery of robust
power is not an artifact of the Beta-rank implementation error.

The fact that the robust numbers are essentially invariant while some oracle
values move suggests that the robust minimum may often be controlled by
components/candidates other than the corrected fixed-Beta component. That is
a hypothesis for later component-ablation analysis, not yet a proved fact.

Kill-Test 09 is now closed as a **confirmed PASS**.

Proceed to Kill-Test 10: matched comparison against a properly implemented
generic fixed-reference confidence-band/CCTM-style baseline and the oracle
predictive-rank method.
