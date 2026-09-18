# P−1 Kill-Test 13 Result — final baseline-strength audit

Status: **STRONG PASS on the frozen primary criterion**

Date: 2026-09-18

## Full-run configuration

- alpha = 0.05
- reps = 200
- delta grid = {0.005,0.010,0.015,0.020,0.025,0.030,0.035,0.040,0.045}
- CCTM one-sided D grid = {0.50,0.90,0.99}
- K in {24,32}, M=2
- T=200 primary summary
- static-coupling method frozen
- baseline envelope selected ex post only as an adversarial benchmark

## Headline full-run results

| K | condition | static | strongest tuned baseline | gap | oracle |
|---:|---|---:|---:|---:|---:|
| 24 | beta_4 | 0.880 | 0.005 (band_mix) | 0.875 | 0.965 |
| 24 | beta_8 | 1.000 | 0.340 (band_ons) | 0.660 | 1.000 |
| 32 | beta_4 | 0.935 | 0.170 (band_mix) | 0.765 | 0.995 |
| 32 | beta_8 | 1.000 | 0.840 (band_mix) | 0.160 | 1.000 |

Observed null crossing at T=200:
- K=24: static=0.020, oracle=0.060, tuned confidence-band baselines=0.000 in the printed best configurations;
- K=32: static=0.015, oracle=0.040, tuned confidence-band baselines=0.000 in the printed best configurations.

## Frozen decision rule

The primary stress point was K=32, T=200, gamma=4.

Strong PASS required:

static crossing - strongest tuned baseline crossing >= 0.15.

Observed:

0.935 - 0.170 = 0.765.

This exceeds the frozen strong-PASS margin by a large amount.

At gamma=8 the gap is smaller but still positive:

1.000 - 0.840 = 0.160.

That also clears the same 0.15 reference margin, although only narrowly.

## Interpretation

The final baseline audit materially strengthened the competitors:
- delta was swept over nine valid allocations;
- the exact-count band was tested both as a fixed mixture and with adaptive ONS betting;
- CCTM-style ONS was allowed D up to 0.99;
- the reported comparison uses the best configuration selected ex post for each scenario.

Despite that deliberately favorable treatment of the baselines, static coupling retained a very large advantage at the primary moderate-shift stress point.

This supports the finite-reference thesis that persistent static contamination structure contains information that generic simultaneous confidence-set robustification discards.

## Scope guardrail

The ex-post best-grid envelope is not itself one precommitted level-alpha test. Therefore it is only an adversarial benchmark.

Also, the tested CCTM comparator is a contamination-widened one-sided adaptation, not a theorem claiming optimality over every possible contaminated CCTM construction.

The strongest defensible current statement remains scenario/model specific:

> Under the frozen static bounded-replacement model, exact static-coupling predictive-rank evidence exhibits substantially higher finite-reference power than the tested valid generic confidence-band robustifications, even after aggressive baseline tuning.

## Remaining non-tuning check

Before declaring the experimental firewall completely closed, inspect the already-generated Kill-Test 13 CSV for:
- median detection delay among detected paths;
- median log evidence;
- the exact tuned delta/D configurations that achieve the strongest baseline rows.

This is a reporting/audit step only. No further bettor or detector tuning is allowed.

## Decision

**Primary power firewall: STRONG PASS.**

If the delay/log-evidence audit contains no contradiction, freeze the method and move directly to theorem statements/proofs and manuscript v0.1.