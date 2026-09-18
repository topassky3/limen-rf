# P−1 Kill-Test 10 — matched generic-band vs static-coupling comparison

Status: **frozen comparison gate**

Date: 2026-09-18

## Purpose

Kill-Test 09 is now a confirmed PASS. The next question is whether the static-coupling predictive-rank construction contributes anything beyond a generic fixed-reference confidence-band method.

This gate compares, on the same simulated reference/stream paths:

1. **Static-coupling robust PRM mixture** — the method that survived Kill-Test 09.
2. **Generic exact-count DKW band mixture** — a deliberately strong one-sided baseline that uses the known contamination budget M but does not exploit fixed contamination identities across time.
3. **CCTM-style one-sided ONS** — based on the betting function and ONS update used by Shaer et al. (2026), with the confidence radius widened for bounded contamination.
4. **Oracle clean-subset PRM mixture** — knows the true contamination positions and is not a feasible method; it is an upper comparator.

Primary references:
- Shaer, Bar, Prinster & Romano (2026), *Testing For Distribution Shifts with Conditional Conformal Test Martingales*, ICML 2026 / arXiv:2602.13848.
- Kuang & Xia (2026), *Anytime-Valid Distribution Shift Detection via Predictive Rank Martingales*, arXiv:2609.00536.
- Official CCTM code: https://github.com/shaersh/cctm

## Shared contamination model

Model A from the previous gates:

- K=8 observed references;
- exactly M=2 fixed exogenous contaminants;
- n=K-M=6 clean reference values iid from continuous F;
- future null stream iid from F;
- diagnostic contaminants fixed above the support of F;
- exact M is given to every robust method.

The alternatives are one-sided Beta(gamma,1) shifts on the probability-integral-transform scale.

## Matched error budget

Target marginal anytime type-I error:

\[
\alpha=0.05.
\]

The static-coupling PRM has a direct marginal anytime guarantee at threshold 1/alpha.

The confidence-band methods have a reference-confidence event with failure probability delta. We freeze

\[
\delta=\alpha/2=0.025.
\]

If the conditional test level on the good reference event is a, then

\[
P(\text{ever reject})
\le
\delta+(1-\delta)a.
\]

Hence use

\[
a=\frac{\alpha-\delta}{1-\delta}
=0.0256410256\ldots
\]

and threshold 1/a for both confidence-band baselines.

This makes the marginal error budget comparable rather than giving the confidence-band method an extra delta of type-I error.

## Contamination-aware DKW band

Let q(x) be the number of the K observed references less than or equal to x.

Among those q values, at most M can be contaminants. Therefore the number of clean observations <=x is constrained by

\[
\max(0,q-M)
\le q_{\rm clean}
\le \min(n,q).
\]

For the clean empirical CDF Fhat_n,

\[
\frac{\max(0,q-M)}{n}
\le \widehat F_n(x)
\le
\frac{\min(n,q)}{n}.
\]

On the DKW event

\[
\|\widehat F_n-F\|_\infty\le
\epsilon_n,\qquad
\epsilon_n=\sqrt{\frac{\log(2/\delta)}{2n}},
\]

the true PIT value F(x) lies in

\[
L(x)=\max\left(0,\frac{\max(0,q-M)}n-\epsilon_n\right),
\]

\[
U(x)=\min\left(1,\frac{\min(n,q)}n+\epsilon_n\right).
\]

This is sharper than simply taking the contaminated ECDF and adding M/K to a symmetric radius.

## Generic band-mixture baseline

For a right-shift test, on the good reference event,

\[
L(X_t)\le F(X_t).
\]

Under H0, F(X_t) is Uniform(0,1), so

\[
E[2(L(X_t)-1/2)\mid D_0]\le0.
\]

For any predictable/fixed eta in [0,1],

\[
e_t(\eta)=1+\eta\,2(L(X_t)-1/2)
\]

is nonnegative and has conditional expectation <=1 on the confidence event.

We use the frozen grid

\[
\eta\in\{0.05,0.1,0.2,0.4,0.6,0.8,0.95\}
\]

and a 5% constant-one hedge. Their convex mixture is a valid conditional e-process on the DKW event.

This baseline is intentionally simple but stronger than comparing only a DKW half-width.

## CCTM-style ONS baseline

We also implement a one-sided version of the official CCTM betting construction.

Let the contaminated empirical CDF be

\[
u_t=q_t/K.
\]

A symmetric valid radius under Model A is

\[
\epsilon_{\rm sym}
=
\frac{n}{K}\epsilon_n+\frac{M}{K}.
\]

The CCTM-style factor is the smoothed form

\[
b_t
=
1+
\frac{
\eta_t(u_t-1/2)
-\sqrt{\eta_t^2+k^2}\,\epsilon_{\rm sym}
}{
1/2+(1+k)\epsilon_{\rm sym}
},
\]

with k=1e-6.

The ONS update follows the official implementation, except eta is projected to [0,D] rather than [-D,D] because this gate targets only right shifts. We freeze D=0.5. This makes the baseline stronger for the stated one-sided alternative.

## Frozen experiment

- K=8
- M=2
- alpha=0.05
- delta=0.025
- horizons T={40,100,200}
- conditions: null, Beta(2,1), Beta(4,1), Beta(8,1)
- 200 Monte Carlo paths per condition
- seed=20260918
- same path used by all four methods
- exact M known
- two fixed high contaminants

Outputs:
- crossing probability by each horizon;
- median stopping time among detected paths;
- median log evidence at each horizon;
- empirical fraction of references satisfying the clean DKW event.

## Decision rule

### Continue toward paper core

Continue if:
- static-coupling null behavior remains sane;
- static-coupling power/delay is materially better than **both** generic confidence-band baselines for gamma=4 and/or gamma=8;
- the gain is not merely a tiny numerical difference;
- oracle remains above static coupling, leaving a credible robustness-efficiency story.

### Reassess / no-go

Reassess the central novelty if a generic band/CCTM construction matches static coupling closely. In that case the added latent-contamination structure may not buy enough to justify a new method.

## Guardrail

Beating CCTM is not by itself a novelty claim. Kuang & Xia already report that clean-reference PRM can outperform CCTM. The scientific question here is narrower:

> Does explicitly exploiting **static contamination coupling** recover useful evidence that a generic contamination confidence set loses?

No hardware work before this gate is resolved.
