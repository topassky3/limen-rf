# Publication validation V1 — 5,000-rep frozen result

Date: 2026-09-22

Status: **PASS — full frozen publication validation complete**

Command:

    uv run python experiments/pminus1_publication_validation_v1.py \
      --reps 5000 \
      --bootstrap-reps 2000 \
      --workers 4 \
      --output-dir results/publication_v1

The run finished with:

    PUBLICATION_V1: COMPLETE

## Null calibration check

At the nominal anytime level \(\alpha=0.05\), the proposed static-coupling detector remains conservative over the simulated null paths.

| K | T | static | 95% CI | best-grid baseline | oracle | oracle 95% CI |
|---:|---:|---:|:---|---:|---:|:---|
| 24 | 40  | 0.0096 | [0.0072, 0.0127] | 0.0000 | 0.0278 | [0.0236, 0.0327] |
| 24 | 100 | 0.0110 | [0.0085, 0.0143] | 0.0000 | 0.0324 | [0.0278, 0.0377] |
| 24 | 200 | 0.0112 | [0.0086, 0.0145] | 0.0000 | 0.0328 | [0.0282, 0.0381] |
| 32 | 40  | 0.0116 | [0.0090, 0.0150] | 0.0000 | 0.0272 | [0.0230, 0.0321] |
| 32 | 100 | 0.0140 | [0.0111, 0.0176] | 0.0000 | 0.0320 | [0.0275, 0.0372] |
| 32 | 200 | 0.0144 | [0.0115, 0.0181] | 0.0000 | 0.0324 | [0.0278, 0.0377] |

These null simulations are sanity checks only; finite-sample validity is supplied by the theorem, not by Monte Carlo calibration.

## T=200 reported alternative results

| K | gamma | static | 95% CI | strongest frozen-grid baseline | oracle | paired static-baseline gap | 95% paired CI |
|---:|---:|---:|:---|---:|---:|---:|:---|
| 24 | 2 | 0.1824 | [0.1719, 0.1933] | 0.0000 | 0.4258 | 0.1824 | [0.1722, 0.1934] |
| 24 | 4 | 0.8758 | [0.8664, 0.8847] | 0.0106 | 0.9740 | 0.8652 | [0.8556, 0.8750] |
| 24 | 8 | 0.9980 | [0.9963, 0.9989] | 0.3434 | 1.0000 | 0.6546 | [0.6410, 0.6682] |
| 32 | 2 | 0.2036 | [0.1927, 0.2150] | 0.0002 | 0.4396 | 0.2034 | [0.1918, 0.2142] |
| 32 | 4 | 0.9144 | [0.9063, 0.9218] | 0.1152 | 0.9810 | 0.7992 | [0.7880, 0.8104] |
| 32 | 8 | 0.9998 | [0.9989, 1.0000] | 0.8362 | 1.0000 | 0.1636 | [0.1532, 0.1734] |

## T=200 detected-delay results

Median stopping time is reported conditional on crossing by T=200.

| K | gamma | static median [95% CI] | best-grid baseline median [95% CI] | oracle median [95% CI] |
|---:|---:|:---|:---|:---|
| 24 | 2 | 29 [26, 31.5] | NA | 17 [16, 18] |
| 24 | 4 | 20 [19, 20.02] | 117 [96, 149] | 9 [8, 9] |
| 24 | 8 | 8 [8, 9] | 75 [74, 79] | 5 [5, 5] |
| 32 | 2 | 22 [20, 25.5] | 178 [178, 178] | 16 [16, 17] |
| 32 | 4 | 15 [14.5, 16] | 97 [92.5, 102] | 8 [8, 8] |
| 32 | 8 | 7 [7, 7] | 53 [52, 54] | 4 [4, 5] |

Delay must be interpreted jointly with crossing probability because it is conditional on detection.

## Primary frozen criterion

Primary condition: K=32, m=2, gamma=4, T=200.

Frozen development criterion:

    static crossing - strongest baseline crossing >= 0.15.

Observed publication-V1 result:

    0.9144 - 0.1152 = 0.7992.

Paired bootstrap 95% CI:

    [0.7880, 0.8104].

Oracle-minus-static paired gap:

    0.0666 [0.0598, 0.0736].

The primary criterion therefore passes by a wide margin without detector retuning.

## Stability relative to the 200-rep development audit

The qualitative ordering from Kill-Test 13 survives the 5,000-rep run:

    oracle > static coupling >> strongest generic confidence-band comparator

for the moderate gamma=4 setting, while gamma=8 approaches saturation.

Representative development -> publication estimates:

- K=24, gamma=4: static 0.880 -> 0.8758.
- K=32, gamma=4: static 0.935 -> 0.9144.
- K=32, gamma=8: baseline 0.840 -> 0.8362.
- K=32, gamma=2: static 0.195 -> 0.2036.

This substantially reduces the chance that the development conclusion was an artifact of 200 Monte Carlo paths.

## Publication figures generated locally

- results/publication_v1/figures/crossing_T200_K24.pdf
- results/publication_v1/figures/crossing_T200_K32.pdf
- results/publication_v1/figures/delay_T200_K32.pdf
- PNG counterparts for each figure.

## Interpretation guardrails

- The strongest baseline is an ex-post best-grid descriptive benchmark, not one precommitted level-alpha procedure.
- The paired CI describes the paired empirical difference against that selected benchmark; it is not a formal superiority theorem.
- Null Monte Carlo is a sanity check; theorem-level validity is not inferred from empirical false-alarm rates.
- Delay is conditional on detection and can be selection-biased for methods with low crossing probability.
- No bettor, detector, threshold, or baseline grid was changed after method freeze.

## Gate decision

**SIMULATION VALIDATION V1: PASS**

Next phase:

1. Version the local V1 CSV/manifest/figures.
2. Update manuscript results from the 200-rep development audit to the 5,000-rep publication estimates.
3. Execute the pre-registered semi-synthetic RTL-SDR validation.
