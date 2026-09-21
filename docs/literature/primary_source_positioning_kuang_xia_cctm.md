# Primary-source positioning — Kuang–Xia PRM and Shaer et al. CCTM

Date: 2026-09-21

Status: **primary-source audit complete for the two closest 2026 references**

Primary sources checked:

1. Qi Kuang and Yin Xia, *Anytime-Valid Distribution Shift Detection via Predictive Rank Martingales*, arXiv:2609.00536v1, 2026.
2. Shalev Shaer, Yarin Bar, Drew Prinster, and Yaniv Romano, *Testing For Distribution Shifts with Conditional Conformal Test Martingales*, arXiv:2602.13848v2, 2026.

This note fixes attribution before drafting the Abstract and Introduction.

---

## 1. What Kuang–Xia already proves

Kuang–Xia assumes a **clean fixed calibration/reference sample**:

\[
D_0=(Y_1,\ldots,Y_n)
\]

and an online stream such that, under the null,

\[
Y_1,\ldots,Y_n,X_1,X_2,\ldots
\overset{\mathrm{iid}}{\sim}P.
\]

They define the fixed-reference rank

\[
R_t
=
1+\sum_{i=1}^{n}\mathbf 1\{Y_i\le X_t\}
\in\{1,\ldots,n+1\}
\]

and the rank-history filtration

\[
\mathcal G_t=\sigma(R_1,\ldots,R_t).
\]

Their Theorem 2.1 states exactly:

\[
\Pr(R_t=j\mid\mathcal G_{t-1})
=
\pi_{t,j}
=
\frac{1+N_{t-1,j}}{n+t}.
\]

More importantly, the same theorem already allows **any**
\(\mathcal G_{t-1}\)-measurable probability vector \(q_t\) over the next rank and defines

\[
E_t
=
\frac{q_{t,R_t}}{\pi_{t,R_t}},
\qquad
M_t=\prod_{s=1}^{t}E_s.
\]

They prove that \(M_t\) is a nonnegative martingale and therefore

\[
\sup_P
\Pr_{H_0(P)}
\left(
\sup_{t\ge0}M_t\ge1/\alpha
\right)
\le\alpha.
\]

They also explicitly use convex portfolios of PRMs, so the generic fact that a fixed convex mixture of nonnegative martingales remains valid is not a LIMEN-RF novelty claim.

### Attribution consequence

The following pieces in the LIMEN-RF draft are **not novel** and must be cited as Kuang–Xia results or immediate corollaries:

- the exact Pólya/Dirichlet predictive-rank law for a clean fixed reference;
- the generic predictable-\(q_t\) likelihood-ratio martingale;
- Ville-based anytime marginal type-I control for that clean PRM;
- convex portfolios/mixtures of valid PRM wealth processes.

Our indexing \(0,\ldots,n\) instead of their \(1,\ldots,n+1\) is purely notational.

### What Kuang–Xia does not assume in the checked paper

Their null reference sample is iid from \(P\). Their fixed-reference theorem does **not** start from a reference bank containing an unknown static set of arbitrary replacement cells.

The word “contamination” in their motivation refers to **test-time contamination of a growing reference set by post-change observations**. Their PRM avoids that issue by keeping the original calibration sample fixed and clean.

Therefore LIMEN-RF must not claim novelty for “fixed-reference predictive ranks.” The possible novelty begins only after introducing an already-contaminated fixed reference bank with unknown persistent contamination identities.

---

## 2. Correct relation between Kuang–Xia and the LIMEN-RF theorem stack

The clean PRM result should be presented in the manuscript as a known building block.

A clean attribution-friendly structure is:

### Known Result A — Clean fixed-reference predictive law (Kuang–Xia, 2026)

State their predictive law, translated to our indexing.

### Known Result B — Clean PRM martingale (Kuang–Xia, 2026)

State their predictable-\(q_t\) martingale construction.

### LIMEN-RF Lemma 1 — true-candidate rank reconstruction

For a candidate contamination-position set \(C\),

\[
R_t^{(C)}
=
Q_t-\#\{c\in C:c\le Q_t\}.
\]

For the true static set \(C^\star\),

\[
R_t^{(C^\star)}
=
\#\{i\in G:Y_i\le X_t\}.
\]

This is the bridge from the contaminated observed bank to the clean PRM theorem.

### LIMEN-RF Theorem 1 — robust anytime crossing by static-candidate domination

Let \(E_t^{(C)}\) be the PRM wealth computed on candidate-reconstructed ranks and define

\[
\underline E_t=\min_C E_t^{(C)}.
\]

Since

\[
\underline E_t
\le
E_t^{(C^\star)}
\]

pathwise for every \(t\), and the true-candidate process is the Kuang–Xia clean PRM,

\[
\Pr_{H_0}
\left(
\sup_t\underline E_t\ge1/\alpha
\right)
\le\alpha.
\]

This is the first theorem in the current paper core that should be presented as a LIMEN-RF contribution, subject to the broader prior-art search already recorded in P−1.

### LIMEN-RF Proposition — persistent candidate structure

Unknown static contamination positions induce a single persistent latent candidate \(C^\star\) shared by all future observations. Deleting sorted candidate positions merges adjacent observed-rank bins and yields a contiguous partition.

This persistent coupling is absent from the clean Kuang–Xia setup and is the structural feature exploited by the robust lower envelope.

---

## 3. What CCTM actually assumes and proves

Shaer et al. also begin with a **clean iid fixed reference dataset**.

Their setup explicitly assumes

\[
D_0=\{X_1^{\mathrm{in}},\ldots,X_n^{\mathrm{in}}\}
\]

consists of \(n\) iid draws from the unknown null distribution \(P\).

Their use of the term “test-time contamination” refers to a different problem: standard CTMs continually add online observations to a growing reference pool, so after a change the pool becomes contaminated by post-shift observations.

CCTM avoids that problem by never adding online test points to the fixed reference \(D_0\).

### CDF uncertainty in CCTM

With clean iid \(D_0\), CCTM forms

\[
\widehat F_0(x)
=
\frac1n\sum_{i=1}^{n}\mathbf 1\{X_i^0\le x\}
\]

and assumes a simultaneous confidence band satisfying

\[
\Pr_{D_0}
\left(
|\widehat F_0(x)-F(x)|
\le
\epsilon(x)
\quad\forall x
\right)
\ge1-\delta.
\]

They give DKW as a standard choice:

\[
\epsilon_n
=
\sqrt{\frac{\log(2/\delta)}{2n}}.
\]

Their unsmoothed robust betting form is

\[
b_t(\widehat p_t)
=
1+\eta_t(\widehat p_t-1/2)
-
|\eta_t|\epsilon(\widehat p_t),
\]

followed by a smoothed version for ONS.

### Their Theorem 3.1

The paper states a PAC/calibration-conditional guarantee: with probability at least \(1-\delta\) over the draw of the clean reference \(D_0\), the conditional anytime type-I error is at most the internal test level.

This is not the same guarantee as Kuang–Xia's unconditional/marginal level-\(\alpha\) PRM statement.

Kuang–Xia Appendix B explicitly analyzes this difference. If the conditional crossing level is \(a\), then the simple marginal bound is

\[
a(1-\delta)+\delta.
\]

Therefore a sufficient matched marginal target \(\alpha\) is

\[
a
\le
\frac{\alpha-\delta}{1-\delta},
\qquad
\delta<\alpha.
\]

LIMEN-RF used this matched-budget conversion in the final baseline audits.

---

## 4. What our “contamination-widened CCTM-style” baseline is

This must be described as **our adaptation**, not as an algorithm or theorem proposed by Shaer et al.

Our frozen simulation model observes \(K=n+m\) reference values, of which \(n\) are iid clean samples from \(F\) and \(m\) are static arbitrary replacements.

Shaer et al.'s CCTM theorem does not provide a confidence band for this pre-contaminated fixed-reference model.

We constructed two conservative extensions.

### 4.1 Exact-count lower band — LIMEN-RF adaptation

At a test point \(x\), let

\[
q(x)
=
\#\{\text{all }K\text{ observed references}\le x\}.
\]

If exactly \(m\) observed references are arbitrary replacements, then the unknown clean count satisfies pathwise

\[
\max\{0,q(x)-m\}
\le
q_{\mathrm{clean}}(x)
\le
\min\{n,q(x)\}.
\]

On the DKW-good event for the latent clean iid sample,

\[
\|\widehat F_{\mathrm{clean}}-F\|_\infty
\le\epsilon_n,
\]

we therefore obtain the lower bound

\[
L(x)
=
\max\left\{
0,
\frac{\max(0,q(x)-m)}{n}
-
\epsilon_n
\right\}.
\]

This exact-count contamination correction is a **LIMEN-RF baseline construction**. It is not stated in the checked CCTM paper.

### 4.2 Symmetric contaminated-ECDF radius — LIMEN-RF adaptation

Let \(\widetilde F_K\) be the ECDF of all \(K=n+m\) observed references.

Write it as

\[
\widetilde F_K
=
\frac nK\widehat F_{\mathrm{clean}}
+
\frac mK\widehat F_{\mathrm{bad}}.
\]

Since two CDF values differ by at most one,

\[
|\widehat F_{\mathrm{bad}}(x)-F(x)|\le1.
\]

Therefore, on the clean DKW event,

\[
|\widetilde F_K(x)-F(x)|
\le
\frac nK\epsilon_n+\frac mK.
\]

We defined

\[
\epsilon_{\mathrm{sym}}
=
\frac nK\epsilon_n+\frac mK
\]

and inserted this widened radius into the CCTM betting geometry.

Again, this is **our contamination-widened CCTM-style comparator**, not a result claimed by Shaer et al.

### 4.3 One-sided specialization — also ours

Shaer et al. develop a two-sided betting parameter. Our frozen experiments concern right-shift alternatives, so the comparison projected the betting parameter to a nonnegative interval.

That is a one-sided specialization made for our simulation study.

### 4.4 Marginal-level matching — comparison protocol, not original CCTM

Our final baseline threshold used

\[
a
=
\frac{\alpha-\delta}{1-\delta}
\]

so that the PAC conditional guarantee admits the conservative marginal bound

\[
a(1-\delta)+\delta\le\alpha.
\]

This comparison protocol follows the conversion discussed by Kuang–Xia Appendix B. It is not the thresholding rule used in the original CCTM experiments, where Shaer et al. report \(\alpha=0.05,\delta=0.1\).

---

## 5. Required terminology in the manuscript

### Use

- “clean predictive-rank theorem of Kuang and Xia (2026)”;
- “our static-contamination extension”;
- “candidate-reconstructed predictive ranks”;
- “persistent latent contamination-position set”;
- “anytime-valid robust evidence lower envelope”;
- “contamination-widened CCTM-style baseline (ours)”;
- “generic confidence-band robustification derived from the CCTM principle.”

### Do not use

- “our predictive-rank theorem” for the clean rank law;
- “our generic PRM martingale theorem”;
- “CCTM with contaminated reference” as if Shaer et al. proposed it;
- “Shaer et al. prove robustness to arbitrary contaminated calibration cells”;
- “we beat CCTM in general”;
- “CCTM is invalid” without the exact distinction between its PAC calibration-conditional statement and marginal level matching.

---

## 6. Novelty attribution matrix

| Component | Primary attribution | LIMEN-RF status |
|---|---|---|
| Fixed clean reference ranks | Kuang–Xia 2026 | prior art |
| Exact predictive law \((1+N)/(n+t)\) | Kuang–Xia Theorem 2.1 | prior art |
| Predictable \(q_t/\pi_t\) PRM | Kuang–Xia Theorem 2.1 | prior art |
| Convex PRM portfolio | Kuang–Xia Section 2.6 / standard martingale fact | prior art |
| Fixed clean ECDF + confidence band | Shaer et al. 2026 | prior art |
| CCTM robust betting correction for ECDF estimation | Shaer et al. 2026 | prior art |
| Pre-contaminated static reference bank | not covered by the two checked methods | LIMEN-RF model |
| Candidate reconstruction \(R_t^{(C)}\) | not found in the two checked methods | LIMEN-RF construction |
| Persistent contamination-position coupling | not found in the two checked methods | LIMEN-RF structural idea |
| Lower envelope dominated by true-candidate PRM | not found in the two checked methods | LIMEN-RF theorem candidate |
| Contiguous-partition interpretation | not found in the two checked methods | LIMEN-RF proposition candidate |
| Fixed-categorical DP | not found in the two checked methods | LIMEN-RF algorithmic candidate |
| Exact-count DKW contamination baseline | our comparison construction | baseline, not main contribution |
| Symmetric radius \(n\epsilon/K+m/K\) | our comparison construction | baseline, not main contribution |
| One-sided contamination-widened CCTM-style ONS | our comparison construction | baseline, not Shaer et al. |
| Marginal alpha-budget matching \(a=(\alpha-\delta)/(1-\delta)\) | Kuang–Xia Appendix B conversion | comparison protocol |

---

## 7. Revised novelty sentence

A safe manuscript-level novelty sentence is:

> Building on the clean fixed-reference predictive-rank martingale of Kuang and Xia, we study a different setting in which the fixed reference bank itself contains an unknown set of persistent static replacements. We exploit the fact that the same latent contamination-position set governs every future rank: candidate deletion reconstructs a clean-rank process for the true candidate, and a lower envelope over candidate PRM wealths inherits anytime-valid threshold-crossing control by pathwise domination.

A stronger empirical follow-up sentence may say:

> In our frozen finite-reference simulations, exploiting this persistent candidate structure retains substantially more detection power and shorter delay than conservative confidence-band baselines that discard contamination identities.

Do not turn the empirical sentence into a universal theoretical superiority claim.

---

## 8. Audit decision

### Kuang–Xia threat

**Resolved by attribution, not by competing with it.**

Their Theorem 2.1 subsumes our former clean Theorems 1 and 2. Those results must move to the background/known-results layer.

It does **not** subsume the static contaminated-reference reconstruction and robust lower-envelope result under the checked assumptions.

### CCTM threat

**Resolved as a distinct clean-reference conditional-band method.**

The checked CCTM paper assumes an iid clean reference dataset. Its “contamination” motivation concerns post-shift test observations entering a growing reference set.

Our pre-contaminated fixed-reference confidence-band baselines are derived adaptations and must be labeled as such.

### Paper-core consequence

The paper should center its claimed contribution on:

\[
\boxed{
\text{persistent static contamination identities}
+
\text{candidate rank reconstruction}
+
\text{true-candidate pathwise domination}
}
\]

—not on the clean predictive-rank law itself.
