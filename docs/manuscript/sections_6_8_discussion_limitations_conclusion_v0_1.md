# LIMEN-RF manuscript v0.1 — Sections 6–8

Date: 2026-09-21

Status: **Discussion + Limitations/Future Work + Conclusion draft**

Working title:

# Anytime-Valid Predictive-Rank Detection with a Statically Contaminated Reference Set

---

# 6. Discussion

## 6.1 What the method is exploiting

The empirical advantage of the proposed construction is best understood as a consequence of **persistent latent structure**.

A generic confidence-band robustification asks which null distributions remain compatible with the observed contaminated reference data. In doing so, it deliberately forgets which individual reference observations might be contaminated.

The static-coupling construction keeps that information in latent form. It asks which fixed candidate set

\[
C\subseteq\{1,\ldots,K\}
\]

could explain the contaminated bank and then reuses the same candidate at every future time point.

The statistical difference is therefore not simply

\[
\text{rank method}
\quad\text{vs.}\quad
\text{CDF method}.
\]

It is more precisely

\[
\text{persistent latent identity uncertainty}
\quad\text{vs.}\quad
\text{generic distributional uncertainty}.
\]

This distinction matters because the same unknown contamination pattern constrains every future rank simultaneously.

The lower envelope

\[
\underline E_t
=
\min_C E_t^{(C)}
\]

can be conservative, but it does not discard the fact that the nuisance parameter is one persistent combinatorial object shared across the entire online sequence.

---

## 6.2 Relation to the oracle

The oracle experiment helps separate two sources of difficulty:

1. finite-reference uncertainty even when the clean subset is known;
2. additional uncertainty from not knowing which reference values are contaminated.

At the primary frozen setting

\[
K=32,\qquad m=2,\qquad \gamma=4,\qquad T=200,
\]

the oracle crossing probability is

\[
0.995,
\]

while static coupling reaches

\[
0.935.
\]

Thus most of the oracle power is retained in this scenario despite not knowing the contaminated positions.

The remaining gap is the cost of robustifying over candidate identities.

For the weaker alternative

\[
\gamma=2,
\]

the gap to the oracle is much larger.

This suggests that the unknown-candidate penalty is most important when the online evidence is weak.

The present paper does not derive an analytical efficiency bound for this gap. Characterizing how the static lower envelope approaches the oracle as a function of

\[
K,\quad m,\quad T,
\]

and the alternative strength is an important open problem.

---

## 6.3 Why the confidence-band comparison is conservative

The confidence-band baselines were designed to represent a strong generic alternative to candidate enumeration.

On the event that the latent clean ECDF lies within its DKW band, the contamination uncertainty is widened to account for the unknown bad references.

This approach remains valid without identifying contaminated positions.

The price is that reference uncertainty is represented pointwise through a CDF set.

That can be substantially larger than the set of distributions compatible with a **single fixed contamination pattern reused over time**.

The final baseline-strength audit intentionally favors the confidence-band family by searching a pre-specified grid of confidence allocations and betting caps and then reporting the best configuration ex post for each scenario.

This ex-post envelope is not itself a precommitted level-\(\alpha\) testing procedure.

Its role is adversarial benchmarking.

The fact that the static method retains a large advantage at the moderate-shift stress point therefore supports the structural interpretation rather than a claim of poor baseline tuning.

---

## 6.4 Marginal anytime validity versus conditional calibration guarantees

The guarantee in Theorem 1 is inherited from the clean predictive-rank martingale.

It is marginal over the random clean reference sample.

This differs from calibration-conditional guarantees such as those developed for CCTM.

Conditional validity can be desirable when the realized reference dataset is viewed as fixed after calibration and one wants error control conditional on that exact realization.

The present construction does not provide that stronger statement.

Instead, it provides exact distribution-free anytime crossing control under the joint model generating the clean reference and future null stream.

These are different inferential targets.

The manuscript therefore avoids describing one guarantee as categorically stronger than the other.

---

## 6.5 Connection to CFAR

The motivating radar analogy is direct but should be interpreted carefully.

Classical CFAR methods use neighboring reference cells to estimate a background level and set a detection threshold for a cell under test.

Nonhomogeneous reference windows and multiple interfering targets motivate order-statistic, censored, and trimmed variants.

The present method addresses a different operating mode:

- a finite reference bank is reused repeatedly;
- some reference cells are persistently contaminated;
- online observations arrive sequentially;
- optional stopping must be safe.

In that regime, the repeated use of the same finite bank creates dependence that can be modeled through predictive ranks.

The proposed method is therefore **CFAR-style** in its use of reference cells and distribution-free ranking, but it is not a drop-in replacement for classical sliding-window OS-CFAR.

A direct radar implementation would require an application-specific mapping from complex/IQ or power measurements to the scalar reference-bank model used here.

---

## 6.6 Structural versus distributional robustness

The present model illustrates a broader distinction in robust sequential inference.

Distributional robustness treats nuisance uncertainty by enlarging the set of possible laws.

Structural robustness can instead exploit restrictions on how contamination persists.

Here the nuisance parameter is not an arbitrary sequence of corruptions over time.

It is a fixed set

\[
C^\star
\]

that simultaneously explains every candidate reconstruction.

The lower-envelope theorem is simple once that structure is stated, but the important modeling step is recognizing that a fixed contaminated reference bank carries this form of persistence.

The simulations suggest that preserving that structural constraint can materially reduce finite-reference conservatism.

---

## 6.7 Computational considerations

Exact enumeration over candidate contamination sets requires

\[
\binom{K}{m}
\]

candidate processes for known \(m\).

This is practical for the frozen experiments with

\[
m=2
\]

and moderate \(K\), but it does not scale well when both \(K\) and \(m\) increase.

The contiguous-partition formulation provides an important reduction for a fixed categorical bettor, where the robust candidate minimization has an additive objective and can be solved in approximately

\[
O(Km^2)
\]

time.

The complete frozen experimental method uses a convex wealth portfolio, for which the current objective is not additive because of the mixture log-sum-exp.

We therefore do not currently claim polynomial-time exact optimization for the full portfolio.

Developing an exact or certified approximate optimizer for the full mixture is a natural algorithmic extension.

---

## 6.8 Finite-reference information ceiling

The clean repeated-rank model has the de Finetti representation

\[
P\sim\mathrm{Dirichlet}(1,\ldots,1),
\]

followed by

\[
R_t\mid P
\overset{\mathrm{iid}}{\sim}
\mathrm{Categorical}(P).
\]

For fixed \(n\), increasing the online horizon reveals the realized spacing vector \(P\), but does not eliminate the randomness of the finite clean reference itself.

Consequently, some persistent rank patterns under an alternative may also be compatible with rare null spacing realizations.

This is the finite-reference information ceiling observed during method development.

It is one reason the paper does not claim universal asymptotic consistency for fixed \(n\).

A complete asymptotic theory would need to distinguish at least:

- fixed \(n\), \(T\to\infty\);
- \(n\to\infty\) with fixed \(T\);
- joint limits of \(n\) and \(T\).

---

# 7. Limitations and Future Work

## 7.1 Exact contamination count

The theory and frozen experiments assume the exact number of contaminated references

\[
m
\]

is known.

In many applications only an upper bound

\[
m\le M
\]

would be available.

A lower envelope over all candidate sizes is a natural extension because the true candidate size would remain represented, but the predictive null law changes with

\[
n=K-m.
\]

That extension should be formalized and tested separately.

---

## 7.2 Static/exogenous contamination assumption

The theorem requires that deleting the true contaminated cells leaves an iid clean reference sample.

This covers static/exogenous interferers but not value-adaptive replacement after observing the clean reference values.

If an adversary first observes a clean reference sample and then chooses which realized values to remove or replace, the surviving clean observations can be selection-biased.

The current predictive-rank argument does not automatically survive that stronger model.

This boundary is fundamental and not merely technical.

---

## 7.3 Scalar continuous observations

The theory assumes scalar observations from a continuous null distribution.

Many sensing applications involve:

- vectors;
- complex-valued IQ samples;
- dependent time series;
- discrete measurements;
- ties induced by quantization.

Extensions may be possible through scalar scores, randomized ranks, multivariate conformal scores, or application-specific transformations, but these are outside the theorem proved here.

---

## 7.4 Independence assumptions

The clean reference observations and future null stream are assumed iid from the same unknown distribution \(F\).

Temporal dependence, nonstationarity, reference/test mismatch, and slowly drifting backgrounds are not covered.

These effects are particularly relevant in RF sensing and radar.

The current result should therefore be interpreted as a mathematically controlled core model rather than a complete physical-layer model.

---

## 7.5 Frozen contaminant geometry

The final simulations use two high contaminants fixed at value \(2\), outside the support of the clean null and Beta alternatives.

This geometry is useful because it makes the contamination persistent and interpretable, but it is not exhaustive.

Future evaluation should vary:

- contaminant magnitude;
- contaminants inside the clean support;
- low-tail and mixed-tail contamination;
- larger \(m/K\);
- heterogeneous or random contaminant values.

Such experiments should be treated as external validation, not as additional tuning of the frozen paper-core method.

---

## 7.6 Limited Monte Carlo size

The final Kill-Test 13 audit uses

\[
200
\]

replications per condition.

This was sufficient to distinguish the large primary power gap used as the exploratory decision gate, but it is modest for publication-quality interval estimation.

A journal-ready reproducibility pass should increase the number of replications substantially and report uncertainty intervals for crossing probabilities and stopping-time summaries.

That future pass should preserve all frozen method and baseline parameters.

---

## 7.7 Confidence-band baselines are adaptations

The contaminated-reference confidence-band comparators are derived in this work from clean-reference DKW/CCTM principles.

They should not be interpreted as canonical or optimal extensions of CCTM to arbitrary contaminated calibration data.

A different robust conditional conformal construction might perform better.

Accordingly, the empirical claim is limited to the tested valid confidence-band adaptations.

---

## 7.8 No universal optimality claim

The proposed lower envelope is valid, but no minimax or uniformly most powerful property is proved.

The frozen betting portfolio was selected through exploratory development before the final firewall closed.

There may exist better predictable betting families, alternative candidate aggregation schemes, or problem-specific scores.

The contribution is the static-candidate validity mechanism and its observed finite-reference behavior, not an optimal betting rule.

---

## 7.9 Full-mixture optimization

The polynomial dynamic program is currently established only for a fixed categorical bettor.

The full frozen portfolio is evaluated through candidate enumeration.

For larger \(K\) and \(m\), this becomes a practical bottleneck.

Possible future directions include:

- exact state augmentation for the mixture;
- convex/variational bounds on candidate wealth;
- branch-and-bound;
- certified pruning;
- approximate dynamic programming with conservative lower bounds.

Any approximation used for testing would need to preserve the pathwise lower-envelope inequality required by Theorem 1.

---

## 7.10 Hardware and RF validation

The current manuscript core is simulation-based.

No hardware validation is included in the theorem or final empirical claim.

A future RF study could examine whether a suitably constructed scalar score from SDR measurements approximates the fixed-reference model closely enough to make the method useful.

Such work would require separate treatment of:

- receiver quantization;
- AGC/gain effects;
- correlated samples;
- spectral leakage;
- reference/test mismatch;
- nonstationary clutter or interference.

Hardware validation should therefore be considered a second-stage engineering study rather than evidence for the mathematical theorem itself.

---

# 8. Conclusion

This paper studies anytime-valid sequential detection when a finite fixed reference bank is already contaminated before monitoring begins.

The key modeling feature is that the unknown contaminated reference identities are **persistent**: the same latent contamination set is reused at every future comparison.

Building on the clean fixed-reference predictive-rank martingale of Kuang and Xia, we reconstruct a candidate clean-rank sequence for every possible static contamination-position set.

For the true candidate,

\[
R_t^{(C^\star)}
=
R_t^{\mathrm{clean}},
\]

so the corresponding candidate wealth is a valid clean predictive-rank martingale.

Taking the lower envelope

\[
\underline E_t
=
\min_C E_t^{(C)}
\]

therefore gives the pathwise inequality

\[
\underline E_t
\le
E_t^{(C^\star)},
\]

which yields

\[
\Pr_{H_0}
\left(
\sup_t \underline E_t
\ge
\frac1\alpha
\right)
\le
\alpha.
\]

The lower envelope itself need not be an e-process; its guarantee follows from domination by the true-candidate process.

The static contamination model also induces a contiguous-partition representation of observed-rank bins.

For a fixed categorical bettor, this structure leads to an additive candidate objective and an approximately

\[
O(Km^2)
\]

dynamic program.

In the frozen simulation study, exploiting persistent contamination identities retains substantially more finite-reference power than the tested confidence-band robustifications.

At the primary setting

\[
K=32,\qquad
m=2,\qquad
T=200,\qquad
X_t\sim\mathrm{Beta}(4,1),
\]

the proposed method reaches crossing probability

\[
0.935,
\]

compared with

\[
0.170
\]

for the strongest ex-post tuned confidence-band baseline and

\[
0.995
\]

for the contamination-aware oracle.

The corresponding median detected delays are

\[
13,\qquad 78.5,\qquad 8.
\]

These results support a narrow conclusion: when contamination is static, preserving its persistent identity structure can provide useful finite-reference information that is lost when uncertainty is represented only through a generic confidence band.

The result is not a claim of universal robustness or superiority.

It applies to a specific static/exogenous contamination model and inherits the marginal fixed-reference interpretation of predictive-rank martingales.

Within that scope, it provides a simple route from contaminated reference uncertainty to finite-sample anytime-valid sequential crossing control.
