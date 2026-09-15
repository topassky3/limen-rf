# P−1 Search Pass 02 — targeted mismatch / heterogeneous order-statistic check

Status: targeted novelty check after Pass 01.

## Question under test

Can the proposed T2 claim — that the worst-case upper tail of

\[
Z^{OS}=\frac{A}{A+B_{(k)}}
\]

under bounded heterogeneous target/reference mismatch occurs at the boundary configuration — be defended as a nontrivial new theorem?

Assume under H0 that

\[
A=\sigma_X^2 U,\qquad B_j=\sigma_{R,j}^2 V_j,
\]

with independent nonnegative base variables and bounded ratios

\[
r_j=\frac{\sigma_X^2}{\sigma_{R,j}^2}\in[1/c,c].
\]

Then

\[
\sigma_{R,j}^2\ge \sigma_X^2/c.
\]

## Targeted literature findings

1. Classical CFAR literature already studies clutter edges / nonhomogeneous backgrounds where CUT and reference cells may lie in different power regions. These works document excessive false alarms when the CUT is in a higher-power region while some reference cells are lower-power, and they motivate GO/OS/switching/censored variants.
2. OS-CFAR under nonhomogeneous reference windows, multiple interferers and clutter transitions is mature prior art.
3. Probability literature on order statistics from independent non-identically distributed exponential samples is substantial; stochastic comparison results exist for heterogeneous exponential order statistics.

These sources do not appear to provide the exact LIMEN-RF anytime-valid construction, but they materially weaken novelty claims around the least-favourable boundary itself.

## Key mathematical observation

The proposed boundary least-favourable result appears to admit an elementary coupling proof.

For each reference cell write

\[
B_j(\mathbf r)=\frac{\sigma_X^2}{r_j}V_j,
\qquad r_j\in[1/c,c].
\]

For the same realization of each \(V_j\), if \(r_j\le c\), then

\[
B_j(\mathbf r)\ge \frac{\sigma_X^2}{c}V_j = B_j(c,\ldots,c)
\]

coordinatewise. Since the k-th order statistic is increasing in every coordinate,

\[
B_{(k)}(\mathbf r)\ge B_{(k)}(c,\ldots,c)
\]

pathwise. Since \(a/(a+b)\) is decreasing in \(b\) for \(a>0\),

\[
Z^{OS}(\mathbf r)\le Z^{OS}(c,\ldots,c)
\]

pathwise under the same coupling. Therefore

\[
Z^{OS}(\mathbf r)\le_{st} Z^{OS}(c,\ldots,c)
\]

and hence for every threshold z,

\[
\sup_{\mathbf r\in[1/c,c]^K}\Pr_{\mathbf r}(Z^{OS}\ge z)
=\Pr_{(c,\ldots,c)}(Z^{OS}\ge z).
\]

Subject to the stated independent scale-family model, this means the boundary LFN is likely mathematically correct but also likely too elementary to carry the paper as the main theorem by itself.

## Consequence for novelty

This is an important negative result for the project firewall:

- T2 in its current form is probably **not sufficiently novel alone**.
- The result may still be useful as a lemma enabling a stronger contribution.
- The central contribution must move beyond simple coordinatewise bounded mismatch.

## Candidate reformulations that may remain nontrivial

### R1 — Coupled / constrained nuisance set
Replace the rectangular nuisance set by a physically motivated set where reference scales are coupled, estimated, drifting, or constrained by a smooth spectral-noise model. Then the worst case may no longer be a trivial coordinatewise boundary.

### R2 — Unknown time-varying mismatch with predictable side information
Build an anytime-valid process when the admissible nuisance set \(\mathcal R_t\) changes predictably with time and is learned from calibration/reference data. The contribution would need more than invoking Ville: the one-step e-factor or conditional superuniform bound must remain valid under adaptation.

### R3 — Correlated / colored reference cells
Introduce realistic RF correlation induced by filtering / overlapping FFT windows. Order-statistic monotonicity remains pathwise in scales, but the exact null and e-factor construction may become nontrivial because independence-based formulas fail.

### R4 — Partially adversarial contaminated references with formal validity
Specify a contamination model where up to M cells may be arbitrary while the remaining K-M obey bounded mismatch, and derive a valid anytime construction that is not just standard partial-conjunction p-value merging.

### R5 — Explicit RF-specific e-factor with provable uniform validity and materially better growth
Even if the LFN is simple, an explicit computable e-factor for the induced OS statistic may still be worthwhile if it is not a routine corollary of existing RIPr/invariance theory and gives a measurable delay advantage over safe p-to-e calibration.

## P−1 provisional decision after Pass 02

**REFORMULATE, not NO-GO.**

The basic bounded-rectangle T2 survives as a correct-looking lemma, but its proof is likely too routine to be the paper's main novelty. The project should not proceed to long simulations under the assumption that T2 itself is the central new theorem.

Next gate: choose one strengthened model (R2, R3, R4, or R5), run a focused prior-art check on that exact model, and only then begin P0/P1 implementation.
