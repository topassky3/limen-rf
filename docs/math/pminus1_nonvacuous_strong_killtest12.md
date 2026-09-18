# P−1 Kill-Test 12 — strongly non-vacuous confidence-band comparison

Status: **frozen comparison gate**

Date: 2026-09-18

## Purpose

Kill-Test 11 showed that the static-coupling method remains strong at K=16 and K=20, but a post-run audit found that the confidence-band baselines were still vacuous or nearly vacuous under the frozen geometry with two high contaminants.

Kill-Test 12 moves farther into a regime where both confidence-band baselines have positive one-sided margin.

Frozen configurations:

- K=24, M=2, n=22;
- K=32, M=2, n=30.

## Why these sizes

With delta=0.025,

epsilon_clean = sqrt(log(2/delta)/(2n))

and

epsilon_sym = (n/K) epsilon_clean + M/K.

Because the two contaminants are above the clean support, the largest observable contaminated rank is q_max=n, so

u_max = n/K.

For the exact-count lower-band baseline,

L_max = 1 - M/n - epsilon_clean.

For the CCTM-style baseline, the maximum one-sided margin is approximately

u_max - 0.5 - epsilon_sym.

Numerically:

| K | n | epsilon_clean | epsilon_sym | L_max-0.5 | CCTM margin |
|---:|---:|---:|---:|---:|---:|
| 24 | 22 | 0.31558 | 0.37262 | 0.09351 | 0.04405 |
| 32 | 30 | 0.27025 | 0.31586 | 0.16309 | 0.12164 |

Thus both baselines are genuinely non-vacuous, especially at K=32.

## Methods

Identical to Kill-Test 11:

1. static-coupling robust predictive-rank mixture;
2. exact-count DKW lower-band mixture;
3. one-sided CCTM-style ONS;
4. oracle predictive-rank mixture.

All methods see the same simulated paths.

## Error budget

Target marginal anytime type-I error:

alpha = 0.05.

Confidence-band failure budget:

delta = 0.025.

Conditional level:

a = (alpha-delta)/(1-delta) = 0.0256410256...

Thresholds:

- static/oracle PRM: 1/alpha = 20;
- confidence-band baselines: 1/a = 39.

## Frozen scenarios

- K in {24,32}
- M=2
- horizons T in {40,100,200}
- null Uniform(0,1)
- alternatives Beta(gamma,1), gamma in {2,4,8}
- two fixed high contaminants
- exact M known
- seed 20260918
- 200 Monte Carlo paths per K/condition
- identical paths across methods

## Primary decision

### Strong survival

Advance toward theorem/paper-core formalization if static coupling remains materially better than both generic confidence-band baselines at K=24 and/or K=32, especially for gamma=4, while null behavior remains sane.

### Narrow contribution

If the gap is strong at K=24 but small at K=32, frame the contribution around finite/small-to-moderate reference regimes.

### No-Go for broad advantage

If generic band/CCTM methods catch up closely at K=32, do not claim broad superiority. The article may still focus on finite-reference efficiency and exact static-contamination structure.

## Reproducibility

Smoke run:

```bash
uv run python experiments/pminus1_nonvacuous_strong_killtest12.py --reps 50
```

Full run:

```bash
uv run python experiments/pminus1_nonvacuous_strong_killtest12.py
```

Output:

```
results/pminus1_killtest12_nonvacuous_strong.csv
```

No hardware work is involved.
