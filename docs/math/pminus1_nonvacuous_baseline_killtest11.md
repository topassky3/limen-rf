# P−1 Kill-Test 11 — non-vacuous confidence-band comparison

Status: **completed, but non-vacuity premise was too weak for the chosen high-contaminant geometry**

Date: 2026-09-18

## Purpose

Kill-Test 10 showed that the static-coupling predictive-rank method is useful at K=8,M=2 while the generic DKW/CCTM-style baselines are vacuous because their confidence radii exceed the useful one-sided range.

Kill-Test 11 removes that excuse.

We move to reference sizes where both generic confidence-band baselines can make positive one-sided bets:

- K=16, M=2, n=14;
- K=20, M=2, n=18.

The question is now sharper:

> When the confidence-band baselines are genuinely informative, does the static-coupling method still retain a material power or delay advantage?

## Methods compared

On identical simulated reference/stream paths:

1. **Static-coupling robust predictive-rank mixture**
   - exact M known;
   - minimum over all fixed size-M contamination-position hypotheses;
   - same mixture family that passed corrected Kill-Test 09.

2. **Generic exact-count DKW lower-band mixture**
   - uses only the count q of observed references <= X_t;
   - uses the exact clean-count interval implied by K,M;
   - does not exploit persistence of the same contamination identities over time.

3. **One-sided CCTM-style ONS baseline**
   - official CCTM betting geometry and ONS logic;
   - contamination-widened symmetric confidence radius;
   - eta projected to [0,D] because only right shifts are tested.

4. **Oracle predictive-rank mixture**
   - knows the true contaminated positions;
   - unattainable benchmark.

## Error budget

Target marginal anytime type-I level:

\[
\alpha=0.05.
\]

For confidence-band baselines:

\[
\delta=\alpha/2=0.025,
\]

and conditional test level

\[
a=\frac{\alpha-\delta}{1-\delta}
=0.0256410256\ldots
\]

so their threshold is

\[
1/a=39.
\]

Static-coupling and oracle PRM use threshold

\[
1/\alpha=20.
\]

## Confidence radii

For n=K-M clean references,

\[
\epsilon_{\rm clean}
=
\sqrt{\frac{\log(2/\delta)}{2n}}.
\]

The symmetric contaminated-ECDF radius used by the CCTM-style baseline is

\[
\epsilon_{\rm sym}
=
\frac{n}{K}\epsilon_{\rm clean}+\frac{M}{K}.
\]

At the frozen sizes:

| K | M | n | epsilon_clean | epsilon_sym |
|---:|---:|---:|---:|---:|
| 16 | 2 | 14 | about 0.3956 | about 0.4712 |
| 20 | 2 | 18 | about 0.3489 | about 0.4140 |

Both methods are therefore non-vacuous in the one-sided upper tail.

## Static-coupling implementation

For K=16 or 20 and M=2, exhaustive contamination enumeration gives 120 or 190 candidates. This is still manageable, but Kill-Test 11 vectorizes candidate and component updates with NumPy to avoid making the experiment unnecessarily slow.

The mixture family is frozen from Kill-Test 09:

- fixed Beta-rank alternatives gamma in {1.25,1.5,2,3,4,6,8,12};
- symmetric Dirichlet predictors alpha in {0.1,0.25,0.5};
- upper-rank tilted Dirichlet predictors with total concentration in {1,3.5,7} and slope in {0.5,1,2,4};
- 5% constant-one hedge.

The corrected Beta-rank identity is used, with the gamma=1 uniform-rank regression guard retained.

## Frozen scenarios

- K in {16,20}
- M=2
- alpha=0.05
- delta=0.025
- T in {40,100,200}
- null Uniform(0,1)
- alternatives Beta(gamma_true,1), gamma_true in {2,4,8}
- true contaminants fixed above the clean support
- true contamination positions are the top two sorted reference positions
- exact M known to robust methods
- 200 Monte Carlo paths per condition and K
- seed 20260918
- identical path for all four methods

## Primary endpoints

For each method and horizon:

- crossing probability;
- median stopping time among detected paths;
- median log evidence;
- DKW-good-reference fraction.

## Decision rule

### Strong survival

The candidate advances toward theorem/paper-core formalization if, at K=16 and/or K=20:

- static-coupling power is materially larger than both generic baselines for gamma=4 or gamma=8;
- or static-coupling reaches comparable power with materially shorter detection delay;
- null behavior remains sane;
- oracle remains above static coupling, giving a credible robustness-efficiency gap.

### Weak / narrow survival

If the advantage exists only at K=16 but mostly disappears by K=20, the contribution may be specifically a **small-to-moderate reference regime** result. That can still be publishable, but the claim must be narrow.

### No-Go for the central advantage claim

If generic band/CCTM baselines match the static method closely once they become non-vacuous, then the main advantage seen at K=8 is attributable mostly to confidence-band vacuity. We should not build the paper around a broad superiority claim.

## Reproducibility

Run the full gate:

\`\`\`bash
uv run python experiments/pminus1_nonvacuous_baseline_killtest11.py
\`\`\`

Optional smoke run:

\`\`\`bash
uv run python experiments/pminus1_nonvacuous_baseline_killtest11.py --reps 50
\`\`\`

Output:

\`\`\`
results/pminus1_killtest11_nonvacuous.csv
\`\`\`

No hardware work is involved.


## Post-run audit correction

The original non-vacuity check used only the nominal radii and assumed the observed rank could reach q=K.

That is false for the frozen diagnostic geometry because the two contaminants are fixed above the support of the clean stream. Therefore, for every test sample X_t in [0,1],

q_t <= K-M = n.

This changes the actual best-case betting geometry.

### Exact-count lower-band baseline

At q_max=n,

L_max
=
(n-M)/n - epsilon_clean
=
1 - M/n - epsilon_clean.

For K=16, M=2, n=14:

L_max ≈ 0.46154 < 0.5,

so the exact-count lower-band baseline is still completely vacuous for a one-sided right-shift bet.

For K=20, M=2, n=18:

L_max ≈ 0.54000,

so the baseline is technically non-vacuous, but only by about 0.04 above 0.5. With the matched threshold 39, this is an extremely weak betting regime.

### CCTM-style baseline

For the contaminated empirical CDF,

u_max = n/K = 1-M/K.

A positive one-sided CCTM bet requires approximately

u_max - 0.5 > epsilon_sym.

For K=16:

u_max - 0.5 - epsilon_sym
=
0.875 - 0.5 - 0.471152
≈ -0.09615.

For K=20:

u_max - 0.5 - epsilon_sym
=
0.9 - 0.5 - 0.413999
≈ -0.01400.

Thus the CCTM-style baseline is still vacuous in both frozen K=16 and K=20 scenarios.

### Consequence

Kill-Test 11 does **not** yet provide the intended non-vacuous comparison against both confidence-band baselines.

The static-coupling results remain valid and strong, but the comparison claim must be downgraded.

A corrected gate must use larger K. For M=2 and delta=0.025:
- K=21 is approximately the first size where the CCTM-style one-sided margin becomes positive;
- K=24 gives a small positive margin;
- K=32 gives a materially positive margin.

The recommended corrected comparison is K in {24,32}, M=2.
