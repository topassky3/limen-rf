# P−1 Candidate Firewall 06 — Contamination-Robust Predictive-Rank CFAR

Status: **PROVISIONAL SURVIVOR — theorem kill-test required**

Date: 2026-09-18

## Why this candidate exists

The quantized-IQ branch was closed as central novelty. The next search therefore returned to the strongest RF-specific structural assumption we already know how to state cleanly:

> a fixed reference/calibration set may contain at most M arbitrary contaminated cells, while the remaining cells are clean null references.

The new question is not another amplitude-model CFAR derivation. It is whether we can obtain an **anytime-valid, distribution-free sequential detector when the same finite reference set is reused over time and up to M of its entries are adversarially contaminated**.

## Exact candidate

Let a fixed reference multiset R = {R_1,...,R_K} contain at least K-M clean observations from an unknown continuous null distribution F; the remaining at most M reference values are arbitrary replacements.

A future null stream X_1, X_2, ... is generated from F under H0. The same finite reference set is reused to score every X_t.

Goal:

Construct an e-process E_t satisfying an anytime guarantee

P_H0(sup_t E_t >= 1/alpha) <= alpha

uniformly over:
- the unknown null distribution F;
- the unknown identities and values of up to M contaminated reference cells;
- repeated reuse of the same finite reference set.

The detector should target one-sided high-energy departures relevant to radar/spectrum sensing.

## Why ordinary conformal/rank p-values are not enough

With a clean fixed calibration set, marginal rank p-values are valid, but repeated reuse of that finite set induces dependence across time. Treating those p-values as independent or conditionally superuniform and multiplying arbitrary p-to-e factors is not automatically valid.

A September 2026 preprint by Kuang and Xia, “Anytime-Valid Distribution Shift Detection via Predictive Rank Martingales,” directly attacks this fixed-reference dependence problem. They derive the exact conditional null distribution of the next rank given previous ranks and construct predictive rank martingales with finite-sample anytime type-I control.

Therefore:

**clean fixed-reference anytime-valid ranks are NOT novel.**

## Contamination prior art

Robust conformal work also exists:
- Clarkson et al. (2024), Split Conformal Prediction under Data Contamination;
- Bashari, Sesia & Romano (ICML 2025), Robust Conformal Outlier Detection under Contaminated Reference Data.

These works analyze contaminated calibration/reference data and robust type-I/coverage behavior.

Therefore:

**contaminated conformal calibration by itself is NOT novel.**

## Gap not found verbatim in the targeted search

The targeted search did not identify a paper giving the following exact combination:

1. fixed finite reference set reused sequentially;
2. distribution-free rank-based detection;
3. anytime-valid / e-process guarantee;
4. at most M **adversarial arbitrary replacements** in the reference set;
5. finite-sample validity uniform over the identities/values of those contaminated references;
6. radar/CFAR interpretation where reference cells may contain interferers.

This absence is not proof of novelty. The candidate survives only long enough for a theorem-level kill-test.

## Structural starting point

For a one-sided high-value test, if the clean reference subset C were known, a clean conformal rank p-value would use the count of clean reference values at least as large as x.

Because up to M identities are unknown, the observed count over all K references only determines an interval of possible clean counts. A conservative fixed-sample p-value can be obtained by maximizing the clean p-value over every admissible clean subset.

That fixed-sample robustification is straightforward and is NOT enough for novelty.

The hard part is sequential reuse:

> derive a predictive conditional law/envelope for the next clean rank when the clean subset itself is latent and only constrained by a bounded-replacement model.

A useful theorem would construct predictable e-factors e_t satisfying

sup_{F, contamination} E[e_t | F_{t-1}] <= 1

without pretending that robust marginal p-values are conditionally independent.

## Candidate theorem target

Possible target:

**Theorem (contamination-robust predictive-rank e-process).**
For a fixed reference set of size K containing at most M arbitrary replacements and K-M exchangeable clean null references, define an observable rank-information state S_t. Construct a predictable betting factor e_t(S_{t-1}, X_t) such that for every continuous F and every admissible contamination pattern,

E_F[e_t | F_{t-1}, R] <= 1

in the appropriate conditional/marginal formulation, yielding an anytime-valid e-process.

The theorem must state carefully whether validity is:
- conditional on the realized contaminated reference;
- marginal over the clean reference sample;
- or uniform in a stronger sense.

Do not blur these notions.

## Kill criteria

Kill the candidate immediately if any of the following occurs:

1. Kuang–Xia PRM extends to arbitrary reference contamination by a routine monotonic rank interval substitution.
2. Existing robust conformal contamination theory already supplies a sequential martingale/e-process under adversarial bounded replacements.
3. The only valid construction is a trivial Bonferroni/union bound over all possible clean subsets with unusable power.
4. The RF mapping adds no mathematical or experimental content beyond a generic robust sequential outlier detector.
5. The theorem requires assumptions stronger than ordinary CFAR practice (e.g. known contamination identities).

## Survival criteria

Continue only if we can prove a nontrivial finite-sample result with at least one of:
- a sharp predictive rank envelope under latent bounded contamination;
- a computationally efficient robust e-factor avoiding enumeration of all clean subsets;
- a minimax/worst-case characterization showing the least-favourable contamination state;
- a power result demonstrating a meaningful advantage over static robust rank tests and clean-reference PRM baselines.

## Immediate next step

No hardware work.

First derive the one-step conditional predictive rank set/envelope for K references with M arbitrary replacements after observing rank history. If that state collapses to a simple known robust-conformal bound, kill the candidate. If it has nontrivial sequential structure, implement a small exact dynamic-programming experiment for K<=12, M<=2 before doing general theory.

## Current assessment

Novelty threat: **high**.

Scientific interest if theorem survives: **high**.

Engineering relevance: **high** for OS/reference-CFAR with interfered reference cells.

Decision: **PROVISIONAL SURVIVOR, not GO**.
