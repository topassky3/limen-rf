# Formal audit after external review — LIMEN-RF paper core

Date: 2026-09-28

Status: **PASS WITH REQUIRED CLARIFICATIONS / IMPLEMENTATION GUARDRAILS**

Purpose: audit the frozen LIMEN-RF theorem and implementation against the strongest concerns raised by an external review before running the contamination-geometry stress test.

This audit does **not** retune the detector or reinterpret frozen Monte Carlo / SDR results.

## Executive decision

No fatal flaw was found in the current exact-\(m\), static/exogenous-contamination theorem.

The core crossing argument remains valid under the stated model:

1. the true candidate reconstructs the canonical clean rank pathwise;
2. the frozen betting rule is the same deterministic predictable functional for every candidate;
3. therefore the true-candidate wealth is exactly the clean predictive-rank martingale;
4. the robust lower envelope is pathwise bounded by that true-candidate wealth;
5. Ville controls the robust crossing event.

Three items require action before the next publication experiment:

- **A. Model wording:** make the minimum probabilistic assumptions more explicit, especially the requirement that the surviving clean reference sample and future null stream form the clean iid system. Do not blur this with the stronger value-adaptive identity-selection model.
- **B. V1b oracle bookkeeping:** the old Monte Carlo code hard-codes the true candidate as the top \(m\) sorted positions because the frozen contaminants are \(2.0\). V1b changes contamination geometry, so it must compute the true sorted contamination positions separately for every replication before evaluating the oracle.
- **C. Ex-post baseline interval wording:** the publication V1 “best-grid baseline” is selected ex post from a frozen grid. Its point estimate is deliberately favorable to the baseline, but the currently reported paired bootstrap interval conditions on the selected configuration and does not re-select the grid winner inside each bootstrap replicate. It must not be described as a selection-adjusted confidence interval for the full best-grid envelope.

A new accumulated-crossing stopping rule raised in the external review is mathematically valid under the same true-candidate argument and pathwise dominates the current stopping rule, but it is a **post-freeze detector variant**, not part of the frozen LIMEN-RF results. It requires a narrow prior-art check before any novelty claim.

---

## 1. Reference model

There are \(K\) observed reference cells. A subset \(G\) of size \(n=K-m\) is clean and, together with the future null stream, forms the clean iid system from an unknown continuous \(F\). The remaining \(m\) physical reference identities are contaminated and remain in the fixed bank throughout monitoring.

**Audit: PASS, with wording clarification.**

The proof needs the clean subset left after deleting the true contaminated identities to be an iid reference sample from \(F\), jointly compatible with the future iid null stream.

The proof does not require the contaminated numerical values themselves to follow any distribution. The essential failure mode is instead selection of which clean observations survive based on their realized values.

Example outside the theorem: draw \(K\) iid clean values, inspect them, and replace the \(m\) largest. The surviving sample is order-selected rather than iid from \(F\).

Required manuscript clarification: state the assumption in terms of the surviving clean system, not merely the phrase “static contamination”.

## 2. Rank indexing and reconstruction

Current definitions:

\[
Q_t=\#\{i:Z_{(i)}\le X_t\}\in\{0,\ldots,K\},
\]

with candidate sorted positions \(C\subseteq\{1,\ldots,K\}\), and

\[
R_t^{(C)}=Q_t-\#\{c\in C:c\le Q_t\}.
\]

**Audit: PASS.**

The one-based sorted-position convention and zero-based count rank are consistent. The Python implementation uses \`bisect.bisect_right\`, which implements the same “\(\le\)” convention.

For the realized true candidate,

\[
R_t^{(C^\star)}=\#\{i\in G:Y_i\le X_t\}
\]

pathwise. No off-by-one error was found.

## 3. Ties

**Audit: PASS within theorem scope; hardware remains outside this theorem.**

Continuity of clean \(F\) eliminates clean-reference / future-null ties almost surely. Repeated contaminated values do not by themselves invalidate reconstruction. Quantized SDR scores may have ties and serial dependence; the paper already does not claim that the iid continuous theorem is validated by hardware-null data.

## 4. Predictive-rank law

For the canonical clean rank,

\[
p_{t,j}=\Pr(R_t^\star=j\mid R_{1:t-1}^\star)=\frac{N_{j,t-1}+1}{n+t}.
\]

**Audit: PASS.**

The denominator is correct because

\[
\sum_{j=0}^{n}(N_{j,t-1}+1)=(t-1)+(n+1)=n+t.
\]

The manuscript correctly states that this is a **marginal fixed-reference** predictive law, not a law conditional on the realized numerical reference vector.

## 5. Filtration and predictability

This was the most dangerous external-review concern.

The paper defines one deterministic betting functional

\[
\mathsf q_t:\{0,\ldots,n\}^{t-1}\to\Delta_n
\]

and applies the same map to every reconstructed candidate history.

For the true candidate,

\[
R_t^{(C^\star)}=R_t^\star
\]

pathwise, hence

\[
q_t^{(C^\star)}=\mathsf q_t(R_1^\star,\ldots,R_{t-1}^\star)
\]

is measurable with respect to the canonical clean-rank filtration.

**Audit: PASS. No filtration leak found in the frozen method.**

Implementation agreement:

- fixed Beta-rank components depend only on frozen \(n\) and gamma grid;
- Dirichlet components depend only on candidate rank counts from previous steps;
- mixture weights are fixed;
- the 5% constant-one hedge is fixed;
- no candidate bettor uses numerical reference values;
- no candidate bettor uses future observations;
- the same component family is used for all candidates.

Critical guardrail: future implementations must not silently make the betting map depend on numerical reference values, candidate identity in a data-dependent way, another candidate's future/current evidence, or future ranks without a new proof.

## 6. Random true sorted position set

**Audit: PASS.**

The manuscript's “random sorted positions do not create post-selection” lemma addresses the correct issue.

For every realized bank,

\[
E_t^{(C^\star)}=\Phi_t(R_1^\star,\ldots,R_t^\star)
\]

pathwise for the same deterministic wealth functional. Thus \(C^\star\) is a random representation of one canonical clean martingale, not post-selection among unrelated martingales.

## 7. Candidate wealth mixture

Frozen candidate wealth combines fixed Beta-rank categorical PRMs, symmetric Dirichlet predictive PRMs, tilted Dirichlet predictive PRMs, and a 5% constant-one hedge.

**Audit: PASS.**

Each component uses \(e_t=q_{t,R_t}/p_{t,R_t}\) with positive predictable normalized \(q_t\), and component wealths are combined with fixed nonnegative weights summing to one.

The code includes the corrected Beta-rank formula and a gamma \(=1\) regression guard for the uniform rank law.

## 8. Robust lower envelope and stopping rule

\[
\underline E_t=\min_C E_t^{(C)}.
\]

**Audit: PASS.**

Because

\[
\underline E_t\le E_t^{(C^\star)}
\]

for every \(t\),

\[
\{\sup_t\underline E_t\ge1/\alpha\}
\subseteq
\{\sup_tE_t^{(C^\star)}\ge1/\alpha\}.
\]

Ville gives the desired type-I crossing control. No multiplicity penalty in the number of candidates is required for this containment argument.

The manuscript correctly avoids claiming that \(\underline E_t\) itself is a martingale, supermartingale, or e-process.

## 9. Post-freeze accumulated candidate elimination rule

Define

\[
M_t^{(C)}=\max_{0\le s\le t}E_s^{(C)}
\]

and

\[
\tau_{\rm accum}=
\inf\left\{t:\min_C M_t^{(C)}\ge1/\alpha\right\}.
\]

**Mathematical audit: VALID AS A SEPARATE STOPPING RULE.**

If \(\tau_{\rm accum}<\infty\), every candidate has crossed at least once, including the true candidate. Therefore

\[
\Pr_{H_0}(\tau_{\rm accum}<\infty)\le\alpha.
\]

Also,

\[
\max_{s\le t}\min_C E_s^{(C)}
\le
\min_C\max_{s\le t}E_s^{(C)},
\]

so pathwise

\[
\tau_{\rm accum}\le\tau_{\rm current}.
\]

Scope decision: this is not part of the frozen detector and none of the existing Monte Carlo / SDR results may be attributed to it. Treat it as a post-freeze candidate variant only after a targeted prior-art check against sequential intersection-union / composite-null testing.

## 10. Exact-\(m\) and upper-bound-only \(m^\star\le M\)

**Audit: PASS as a theoretical corollary.**

If all candidate sizes \(r=0,\ldots,M\) are included and each uses its correct clean-reference count \(n_r=K-r\), the family contains the true pair. The same containment proof applies.

Frozen experiments remain exact-\(m=2\); no empirical claim for the upper-bound procedure is made.

## 11. Candidate/partition DP

**Audit: PASS for the stated fixed-categorical scope.**

Deleting \(m\) sorted reference boundaries gives a contiguous partition of the \(K+1\) observed-rank bins into \(K-m+1\) blocks.

The DP state \((b,d)\), next rank index \(j=b-d\), and block length \(\ell\) deleting \(\ell-1\) boundaries are consistent.

The claimed complexity remains scoped to a fixed categorical bettor:

\[
O(Km^2)\text{ time},\qquad O(Km)\text{ memory}.
\]

The paper correctly does not claim this exact DP for the full convex mixture.

## 12. Original Monte Carlo oracle bookkeeping

Kill-Tests 12/13 use clean Uniform(0,1) references and two contaminants fixed at \(2.0\).

Therefore true sorted contaminated positions are deterministically

\[
(K-m+1,\ldots,K),
\]

and the hard-coded \`true_candidate_index\` in those frozen experiments is correct.

**Audit: PASS for existing frozen Monte Carlo.**

No correction to the 5,000-rep publication run is needed for this reason.

## 13. REQUIRED CHANGE for V1b geometry stress test

V1b will place contaminants inside the clean support, in mixed tails, and/or at random static locations. Their sorted positions are then no longer deterministically the final \(m\) positions.

For **every replication**, V1b must:

1. retain labels identifying contaminated references;
2. sort the tagged bank;
3. compute realized one-based contaminated sorted positions;
4. map that set into \`cfg.candidates\`;
5. replace \`true_candidate_index\` before oracle evaluation.

This is already the pattern used correctly by \`experiments/sdr_semi_synthetic_v1.py\`.

Failing to do this would leave the robust static statistic unchanged but make the reported oracle wrong for non-high-contaminant geometries.

## 14. Confidence-band alpha accounting

Kill-Test 13 uses

\[
\alpha_{\rm internal}=\frac{\alpha-\delta}{1-\delta},
\]

so

\[
\delta+(1-\delta)\alpha_{\rm internal}=\alpha.
\]

**Audit: PASS for the stated marginal error-budget calculation.**

The contaminated-reference CCTM/band procedures are our adaptations and are not attributed as original results of the clean-reference CCTM paper.

## 15. Ex-post strongest baseline and uncertainty interval

Publication V1 selects the strongest baseline configuration ex post from a grid frozen before the run. This intentionally favors the baseline for the descriptive power comparison.

**Audit: WARN — reporting precision, not detector validity.**

The point estimate “static minus strongest frozen-grid baseline” is a legitimate descriptive adversarial comparison.

However, the current bootstrap interval is computed after fixing the configuration selected on the original dataset. It does not re-select the strongest grid configuration inside each bootstrap replicate.

Therefore that interval should be described as conditional on the selected configuration, not as a selection-adjusted interval for the random best-grid envelope.

Clean options:

1. keep the ex-post envelope point estimate and soften/remove inferential language around its CI;
2. report a CI against one precommitted comparator such as \`band_mix, delta=0.045\`;
3. perform a separate explicitly post-hoc bootstrap that repeats the selection inside each bootstrap sample.

No detector retuning is implied by honest relabeling.

## 16. Detection-delay summaries

Current paper reports median stopping time conditional on crossing and already warns that it must be interpreted jointly with crossing probability.

**Audit: PASS with recommended strengthening for V1b.**

Pre-specify additionally:

\[
F_\tau(t)=\Pr(\tau\le t)
\]

and

\[
\mathbb E[\min(\tau,T+1)],
\]

assigning \(T+1\) to paths without detection by \(T\).

## 17. SDR evidence

**Audit: PASS under current claim scope.**

The frozen SDR result is external engineering sensitivity characterization using real receiver/background IQ and controlled post-ADC injection.

Serial dependence means it is not an iid hardware type-I validation. Post-ADC injection does not test analog front-end signal-induced nonlinearities.

No additional SDR acquisition is required by this audit.

## 18. Final audit matrix

| Item | Status | Action |
|---|---|---|
| Static/exogenous clean-system model | PASS/WARN | sharpen wording |
| Rank indexing / reconstruction | PASS | none |
| Clean predictive law | PASS | none |
| Filtration / predictability | PASS | preserve same candidate functional |
| Random sorted \(C^\star\) | PASS | none |
| Frozen mixture validity | PASS | none |
| Lower-envelope crossing theorem | PASS | none |
| Unknown \(m^\star\le M\) corollary | PASS | theoretical only |
| Fixed-categorical DP | PASS | keep scope narrow |
| Frozen MC oracle | PASS | high contaminants justify fixed index |
| V1b oracle | REQUIRED FIX | dynamic true sorted positions |
| Baseline alpha budget | PASS | none |
| Best-grid bootstrap CI | WARN | relabel or selection-adjust |
| Conditional median delay | PASS/WARN | add truncated metric in V1b |
| SDR claim scope | PASS | no new hardware claim |
| Accumulated-crossing rule | VALID NEW VARIANT | prior-art firewall before novelty |

## Gate

\[
\boxed{\text{FORMAL AUDIT: PASS WITH REQUIRED V1b BOOKKEEPING AND REPORTING CLARIFICATIONS}}
\]

Next safe sequence:

1. preserve the frozen detector;
2. write/freeze the V1b runbook with dynamic oracle positions and stronger stopping-time metrics;
3. run V1b once;
4. separately evaluate the accumulated-crossing rule after a targeted prior-art check;
5. allow at most one bounded theoretical extension centered on the statistical value of persistent contamination identity.
