# Publication validation V1 — 5,000-rep frozen result

Date: 2026-09-22

Status: **FULL RUN COMPLETE — detector remained frozen**

Command:

    uv run python experiments/pminus1_publication_validation_v1.py \
      --reps 5000 \
      --bootstrap-reps 2000 \
      --workers 4 \
      --output-dir results/publication_v1

The run finished with:

    PUBLICATION_V1: COMPLETE

## T=200 reported alternative results

| K | gamma | static | 95% CI | strongest frozen-grid baseline | oracle | paired static-baseline gap | 95% paired CI |
|---:|---:|---:|:---|---:|---:|---:|:---|
| 24 | 2 | 0.1824 | [0.1719, 0.1933] | 0.0000 | 0.4258 | 0.1824 | [0.1722, 0.1934] |
| 24 | 4 | 0.8758 | [0.8664, 0.8847] | 0.0106 | 0.9740 | 0.8652 | [0.8556, 0.8750] |
| 24 | 8 | 0.9980 | [0.9963, 0.9989] | 0.3434 | 1.0000 | 0.6546 | [0.6410, 0.6682] |
| 32 | 2 | 0.2036 | [0.1927, 0.2150] | 0.0002 | 0.4396 | 0.2034 | [0.1918, 0.2142] |
| 32 | 4 | 0.9144 | [0.9063, 0.9218] | 0.1152 | 0.9810 | 0.7992 | [0.7880, 0.8104] |
| 32 | 8 | 0.9998 | [0.9989, 1.0000] | 0.8362 | 1.0000 | 0.1636 | [0.1532, 0.1734] |

## Primary frozen criterion

Primary condition: K=32, m=2, gamma=4, T=200.

Frozen development criterion: static crossing - strongest baseline crossing >= 0.15.

Observed publication-V1 result: 0.9144 - 0.1152 = 0.7992.

Paired bootstrap 95% CI: [0.7880, 0.8104].

Therefore the primary criterion passes by a wide margin without detector retuning.

## Stability relative to the 200-rep development audit

The qualitative ordering from Kill-Test 13 survives the 5,000-rep run: oracle > static coupling >> strongest generic confidence-band comparator for the moderate gamma=4 setting, while gamma=8 approaches saturation.

Representative development -> publication estimates:

- K=24, gamma=4: static 0.880 -> 0.8758.
- K=32, gamma=4: static 0.935 -> 0.9144.
- K=32, gamma=8: baseline 0.840 -> 0.8362.
- K=32, gamma=2: static 0.195 -> 0.2036.

## Interpretation guardrails

- The strongest baseline is still an ex-post best-grid descriptive benchmark, not one precommitted level-alpha procedure.
- The paired CI describes the paired empirical difference against the selected benchmark; it should not be sold as a formal superiority theorem.
- Null rows were simulated but are not printed in the terminal primary summary. They must be inspected from results/publication_v1/summary.csv before V1 is declared fully archived.
- Delay CIs and publication figures are also in the local V1 outputs and should be inspected before updating the manuscript.

## Next gate

1. Inspect null rows, delay intervals, and generated figures.
2. Archive/version the V1 CSV/manifest/figures.
3. Update manuscript empirical numbers from 200-rep development values to 5,000-rep publication values.
4. Then proceed to the pre-registered semi-synthetic RTL-SDR validation.

No bettor or detector retuning is permitted.