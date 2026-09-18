# P−1 Kill-Test 11 Result — audit after execution

Status: **STATIC METHOD STRONG / COMPARISON GATE INCONCLUSIVE**

Date: 2026-09-18

## Observed full-run results

### K=16, M=2

At T=200:
- null: static 0.015, band 0.000, CCTM-style 0.000, oracle 0.045;
- Beta(2,1): static 0.125, band 0.000, CCTM-style 0.000, oracle 0.430;
- Beta(4,1): static 0.720, band 0.000, CCTM-style 0.000, oracle 0.935;
- Beta(8,1): static 0.980, band 0.000, CCTM-style 0.000, oracle 0.995.

### K=20, M=2

At T=200:
- null: static 0.010, band 0.000, CCTM-style 0.000, oracle 0.030;
- Beta(2,1): static 0.150, band 0.000, CCTM-style 0.000, oracle 0.470;
- Beta(4,1): static 0.820, band 0.000, CCTM-style 0.000, oracle 0.975;
- Beta(8,1): static 1.000, band 0.015, CCTM-style 0.000, oracle 1.000.

The 50-repetition smoke run had the same qualitative pattern.

## What is genuinely encouraging

The static-coupling method scales well from K=8 to K=16 and K=20:
- gamma=4 power rises to 0.72 and 0.82 at T=200;
- gamma=8 power rises to 0.98 and 1.00;
- null crossing remains low in this simulation;
- the oracle gap narrows at stronger signals.

These are strong internal results for the method itself.

## Why the comparison is not yet decisive

The intended premise of Kill-Test 11 was that both generic confidence-band baselines would be non-vacuous.

That premise fails under the frozen high-contaminant geometry.

Because the two contaminants are above the clean support, q_t can never exceed n=K-M.

For the exact-count band:

L_max = 1 - M/n - epsilon_clean.

At K=16 this is about 0.4615, so it cannot support a positive one-sided bet.

At K=20 it is about 0.5400, so it is only barely informative.

For the CCTM-style baseline:

u_max = n/K,

and positive one-sided betting requires roughly u_max-0.5 > epsilon_sym.

The margins are:
- K=16: about -0.0962;
- K=20: about -0.0140.

So CCTM-style remains completely vacuous at both K values.

## Decision

Do **not** claim general superiority over non-vacuous CCTM from Kill-Test 11.

Do retain the stronger and now repeatedly reproduced claim:

> Static-coupling predictive-rank evidence remains useful in regimes where generic simultaneous confidence-band methods are unable, or nearly unable, to extract one-sided evidence.

The next corrected comparison should use K=24 and K=32 with M=2, where both confidence-band baselines have positive one-sided margin under the same high-contaminant geometry.
