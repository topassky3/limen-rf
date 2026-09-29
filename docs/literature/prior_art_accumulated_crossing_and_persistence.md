# Targeted prior-art firewall — accumulated crossing and persistence value

Date: 2026-09-29

Status: **ACCUMULATED RULE = VALID BUT NOT A NOVELTY CLAIM; PERSISTENCE THEOREM = GO ONLY IF MODEL-SPECIFIC AND QUANTITATIVE**

## 1. Question

After the external review, two possible extensions were considered:

1. an accumulated candidate-elimination stopping rule
   [
   \tau_{\rm accum}
   =
   \inf\left\{
   t:
   \min_C\max_{s\le t}E_s^{(C)}\ge1/\alpha
   \right\};
   ]

2. a theorem quantifying the statistical value of requiring one persistent contamination explanation across the entire online history.

This note checks whether either direction is sufficiently distinct from established testing / online-learning principles to justify changing the paper core.

## 2. Accumulated rule

For each candidate C define its persistent rejection indicator
[
\phi_t^{(C)}
=
\mathbf 1\left\{
\max_{s\le t}E_s^{(C)}\ge1/\alpha
\right\}.
]

Under the candidate-specific null corresponding to the true candidate, Ville gives
[
\Pr\left(\sup_t E_t^{(C^\star)}\ge1/\alpha\right)\le\alpha.
]

The accumulated global rule rejects when
[
\min_C \phi_t^{(C)}=1,
]
i.e. when every component candidate null has been rejected, possibly at different previous times.

This is exactly an intersection-union style construction for a union/composite null.

### Relevant prior art

- Berger (1982), *Multiparameter Hypothesis Testing and Acceptance Sampling*, Technometrics 24(4):295--300, develops the classical intersection-union principle: for a union null, reject only when every component null is rejected; local level-alpha tests yield a global level-alpha test without a multiplicity penalty.
- Koning & van Meer (2026), *Anytime validity is free: inducing sequential tests*, JRSS-B, DOI 10.1093/jrsssb/qkag050, explicitly treats composite hypotheses using infima / running infima of component sequential tests and discusses pointwise optional continuation for families of component tests.
- Ramdas, Grünwald, Vovk & Shafer (2023), *Game-Theoretic Statistics and Safe Anytime-Valid Inference*, Statistical Science 38(4):576--601, surveys anytime-valid inference for composite hypotheses and e-processes.

### Decision

[
\boxed{\text{ACCUMULATED RULE: MATHEMATICALLY VALID, BUT NO NOVELTY CLAIM}}
]

It may be mentioned as a post-freeze observation, remark, or possible alternative stopping implementation, but it should not be promoted as a new central contribution.

None of the frozen Monte Carlo or SDR evidence is to be reassigned to this rule.

## 3. Pathwise dominance over the frozen simultaneous rule

The accumulated rule satisfies
[
\max_{s\le t}\min_C E_s^{(C)}
\le
\min_C\max_{s\le t}E_s^{(C)}.
]

Therefore
[
\tau_{\rm accum}\le\tau_{\rm current}
]
pathwise.

This is useful but algebraically elementary once component-wise persistent rejection indicators are allowed. It is not enough to elevate the paper.

## 4. Persistence versus time-varying nuisance explanation

A tempting comparison is
[
\prod_{s=1}^t \min_C e_s^{(C)}
\le
\min_C\prod_{s=1}^t e_s^{(C)}.
]

Taking logs gives
[
\underbrace{
\min_C\sum_{s=1}^t \ell_{s,C}
}_{\text{one fixed candidate}}
-
\underbrace{
\sum_{s=1}^t\min_C \ell_{s,C}
}_{\text{candidate can change each time}}
\ge0,
\qquad
\ell_{s,C}=\log e_s^{(C)}.
]

This quantity measures the price paid by the relaxed adversary for being allowed to change which candidate is worst at every time.

### Prior-art threat

As a generic optimization object, this is closely aligned with the classical online-learning distinction between the best fixed expert and a switching/tracking expert.

Herbster & Warmuth (1998), *Tracking the Best Expert*, Machine Learning 32:151--178, explicitly studies comparison with one best expert over the full sequence versus a sequence of experts that may change across segments.

Therefore the generic inequality, equality condition, or an arbitrary-sequence separation example is not enough to support a novelty claim.

## 5. What would count as a real persistence theorem for LIMEN-RF

A useful extension must exploit the specific rank/partition geometry of static contaminated references, not merely the generic fact that
min-of-products >= product-of-mins.

The extension is a GO only if a clean theorem can establish at least one of the following.

### Target A — model-specific quantitative separation

For an explicit nonempty class of alternatives / rank-frequency limits, prove a bound such as
[
\frac1t
\left[
\log \underline E_t^{\rm persistent}
-
\log E_t^{\rm refreshed}
\right]
\ge c(K,m,\pi,a)>0
]
eventually or with controlled probability, where the positive constant arises from incompatible persistent candidate partitions.

### Target B — characterization of zero versus positive persistence advantage

Use the contiguous-partition representation to characterize when the best fixed candidate can simultaneously realize all locally worst rank reconstructions and when it cannot.

A result is interesting only if it yields more than the tautology that equality holds when the same candidate minimizes every factor.

### Target C — candidate-identity information bound

Derive a finite-horizon or asymptotic bound on oracle loss caused specifically by uncertainty over the persistent candidate:
[
\text{oracle evidence/delay}
-
\text{robust evidence/delay},
]
with explicit dependence on K, m, horizon, and/or rank-frequency geometry.

A generic online-learning regret bound with candidates treated as anonymous experts is not sufficient; the proof must exploit candidate partitions / rank reconstruction.

## 6. Hard NO-GO criteria

Stop the extension and submit the current paper if the best result reduces to any of:

1. the intersection-union principle;
2. min-product versus product-min algebra;
3. a best-fixed-versus-switching-expert restatement;
4. a constructed example with no use of the rank/partition structure;
5. another tuned Monte Carlo comparison;
6. an unproved intuition that persistence should help;
7. changing the frozen detector to obtain a stronger empirical result.

## 7. Current scientific decision

The existing paper is already complete enough to stand on:

- the exact contaminated-reference crossing theorem;
- the upper-bound-on-m corollary;
- persistent contiguous-partition representation;
- fixed-categorical exact DP;
- finite-reference asymptotic characterization;
- frozen 5,000-rep Publication V1;
- preregistered V1b geometry stress with strong support;
- semi-synthetic RTL-SDR V1/V2 engineering validation.

The accumulated stopping rule does not justify delaying the paper.

One bounded theoretical attempt remains justified only for a **model-specific quantitative persistence theorem** satisfying Section 5.

If that theorem does not materialize cleanly, the correct action is:
[
\boxed{\text{NO MORE EXPERIMENTS; FINAL ADVERSARIAL REVIEW AND SUBMISSION}}
]
