# P−1 Kill-Test 08 Result — Static-contamination predictive-rank DP

Status: **DP PASS / current robust-min bettor FAILS power gate / candidate not yet globally killed**

Date: 2026-09-18

## Reproduced output

Configuration:
- seed: 20260918
- exactness gate: K=8, M=2
- benchmark: K=50, M=5
- diagnostic: K=8, M=2, T=40, gamma=4, alpha=0.05
- contamination in diagnostic: two fixed high-valued reference contaminants
- exact M assumed known in the robust diagnostic

### DP exactness

Observed histogram:

\[
[4,2,9,0,9,6,5,10,5].
\]

Results:

| m | brute-force log wealth | DP log wealth | absolute error |
|---:|---:|---:|---:|
| 0 | -25.904876806815 | -25.904876806815 | 5.684e-14 |
| 1 | -36.382785882897 | -36.382785882897 | 1.421e-14 |
| 2 | -54.659576056007 | -54.659576056007 | 2.132e-14 |

Decision: **DP_EXACTNESS PASS**.

### Computational benchmark

For K=50, M=5:

\[
\binom{50}{5}=2,118,760
\]

candidate contamination subsets would be required by exhaustive enumeration.

The DP returned the exact objective in approximately:

\[
0.001806\ \text{s}.
\]

This confirms that the static-contamination minimization has an exploitable contiguous-partition structure and is computationally easy for the tested fixed-categorical bettor.

### DKW + M/K baseline widths

At delta=0.05:

| K | M | half-width |
|---:|---:|---:|
| 8 | 2 | 0.730161 |
| 12 | 2 | 0.558717 |
| 50 | 5 | 0.292065 |

The generic confidence-band baseline is therefore extremely wide in the small-reference regimes most relevant to the first experiments.

### Seeded bettor diagnostic

Threshold:

\[
\log(1/\alpha)=\log 20\approx 2.9957.
\]

Null:
- robust crossing rate: 0.0000
- oracle crossing rate: 0.0433
- median maximum robust log wealth: -2.014903
- median maximum oracle log wealth: 0.154151

Alternative:
- robust crossing rate: 0.0000
- oracle crossing rate: 0.4633
- median maximum robust log wealth: -0.251314
- median maximum oracle log wealth: 2.758084

## Interpretation

### What survived

The **algorithmic structure** survived strongly.

The DP exactly matches exhaustive enumeration to numerical precision while replacing millions of subset evaluations at K=50,M=5 by a millisecond-scale computation.

This is a real structural fact about static contamination positions: candidate deletions correspond to merging adjacent rank bins, so the worst fixed contamination pattern for the chosen additive log-wealth objective can be solved as a contiguous-partition dynamic program.

### What failed

The specific robust statistic

\[
\underline E_t=\min_C E_t^{(C)}
\]

with a fixed Beta(gamma,1)-induced categorical alternative **fails the power gate badly** in the diagnostic.

Even though the oracle knowing the true contaminated positions crosses the alpha=0.05 threshold in 46.33% of the strong-alternative repetitions by T=40, the robust minimum never crosses.

The result is especially damaging because:
- the exact contamination count M was given to the robust procedure;
- the alternative bettor used gamma=4, matching the simulated stream parameter;
- the contamination was static rather than adaptive.

Thus the failure cannot be blamed on uncertainty about M or on the stronger adaptive-replacement model.

## Important guardrail

This result does **not** prove that every anytime-valid procedure for the static-contamination problem has zero power.

The current construction can fail because the minimum is taken over candidate-specific wealths whose **alternative numerator is itself candidate-dependent**. A wrong contamination pattern may transform the observed ranks into a sequence poorly matched by the fixed Beta-rank alternative, causing its wealth to collapse; the minimum then selects that collapse even if another candidate (including the true one) has strong evidence.

Therefore the experiment rejects the **current robust-min fixed-bettor construction**, not yet the entire statistical problem.

## Final remaining question before killing the candidate

We need distinguish two explanations:

1. **Bettor-mismatch failure:** every admissible contamination pattern still exhibits a one-sided departure, but the fixed gamma=4 numerator is a poor model after the wrong candidate's rank merging. A candidate-specific mixture/adaptive one-sided bettor could repair power.

2. **Fundamental non-identifiability:** under the strong alternative there exists at least one admissible contamination pattern for which the transformed rank process is statistically compatible with a clean null predictive model. Then no uniformly valid rank-only detector can have strong power against that alternative.

The next gate must target this distinction directly.

## Proposed Kill-Test 09

For K=8,M=2, exhaustive enumeration is cheap. Avoid DP initially.

For every candidate contamination set C:

1. transform the observed rank sequence into \(R_t^{(C)}\);
2. use a **mixture over a grid of one-sided alternative strengths** rather than one fixed gamma;
3. record each candidate's maximum/path wealth;
4. identify which C attains the robust minimum;
5. compare the empirical transformed-rank histogram for that worst C against its null predictive behavior;
6. repeat over T in {40,100,200} and alternative strengths gamma in {2,4,8}.

Decision:
- if the robust mixture still has essentially zero crossing probability under strong alternatives as T grows, move to **NO-GO / likely identifiability barrier**;
- if mixture/adaptation restores substantial robust power, then the previous failure was bettor mismatch and the candidate remains alive long enough for a theorem comparison against CCTM.

No hardware work is justified.
