# P−1 Kill-Test 12 Result — strongly non-vacuous comparison

Status: **STRONG PASS for the frozen comparison / paper-core candidate survives**

Date: 2026-09-18

## Frozen configuration

- K in {24,32}
- M=2
- alpha=0.05
- delta=0.025
- conditional confidence-band level = 0.02564103
- horizons T in {40,100,200}
- null Uniform(0,1)
- alternatives Beta(gamma,1), gamma in {2,4,8}
- two fixed high contaminants
- 200 Monte Carlo paths per condition
- identical paths across all methods

## Full-run headline results at T=200

| K | condition | static | band | CCTM-style | oracle |
|---:|---|---:|---:|---:|---:|
| 24 | null | 0.020 | 0.000 | 0.000 | 0.060 |
| 24 | beta_2 | 0.225 | 0.000 | 0.000 | 0.495 |
| 24 | beta_4 | 0.880 | 0.000 | 0.000 | 0.965 |
| 24 | beta_8 | 1.000 | 0.235 | 0.005 | 1.000 |
| 32 | null | 0.015 | 0.000 | 0.000 | 0.040 |
| 32 | beta_2 | 0.195 | 0.000 | 0.000 | 0.425 |
| 32 | beta_4 | 0.935 | 0.120 | 0.010 | 0.995 |
| 32 | beta_8 | 1.000 | 0.735 | 0.300 | 1.000 |

## Interpretation

Kill-Test 12 finally reaches a genuinely non-vacuous regime for the generic confidence-band baselines.

At K=32 the exact-count band has substantial power for beta_8 (0.735) and the CCTM-style baseline is also active (0.300), yet static coupling reaches 1.000.
For beta_4 at K=32, static coupling reaches 0.935 versus 0.120 for the band and 0.010 for CCTM-style, while the oracle is 0.995.

This is a materially stronger result than Kill-Tests 10 and 11 because the baselines now demonstrably cross the anytime threshold in the same frozen geometry.

## Null sanity check

Observed static null crossing at T=200:
- K=24: 0.020
- K=32: 0.015

These simulations are compatible with alpha=0.05 but do not prove validity. The validity claim remains the pathwise domination argument for the true static contamination candidate.

## Scope limitation

This does not justify saying that the method beats CCTM in general. The comparator is a one-sided contamination-widened adaptation of the published CCTM betting/ONS construction, and delta=0.025 was frozen.

The strongest defensible current claim is:

> In the frozen static high-contamination model, exact static-coupling predictive-rank evidence retains much higher finite-reference power than the tested generic simultaneous confidence-band constructions, even after those baselines become non-vacuous.

## Decision

**Strong PASS for Kill-Test 12.**

The candidate now deserves transition from exploratory power-gating to paper-core formalization.

Before broad superiority claims, run one final baseline-strength audit:
1. evaluate a pre-specified grid of valid delta allocations for the confidence-band methods;
2. inspect stopping-time and median log-evidence columns, not only crossing probabilities;
3. compare the strongest valid baseline configuration against static coupling;
4. then freeze the method and begin theorem/manuscript v0.1 work.