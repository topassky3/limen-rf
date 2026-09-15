# P−1 Prior Art Firewall — LIMEN-RF / AV-OS

Issue: #3

## Purpose

This document is a novelty firewall. Its job is not to collect citations for the introduction; it must actively try to falsify the claim that LIMEN-RF / AV-OS contains a publishable methodological contribution.

## Candidate contribution under test

Provisional combination:

- OS/reference-CFAR statistic based on a target energy and an order statistic of reference-band energies;
- bounded target/reference mismatch under the composite null;
- explicit or conservative least-favourable null construction;
- anytime-valid sequential inference via e-processes / test supermartingales;
- nuisance parameters that may vary predictably with time;
- optional robustness to partially contaminated reference cells;
- RF-specific evidence factor if a uniformly valid construction can be proved.

No component above is assumed novel individually.

## Planned theorem map

### T1 — Anytime validity
Target guarantee:

\[
\sup_{H_0}\Pr\left(\sup_{T\ge 1}E_T\ge 1/\alpha\right)\le \alpha.
\]

### T2 — Least-favourable null
Determine whether the robust OS/reference statistic admits an explicit least-favourable null under bounded mismatch, or whether only a conservative upper-tail bound is available.

### T3 — Efficient RF-specific evidence factor
Determine whether a likelihood-ratio-like or RIPr/invariant construction is uniformly valid for the composite null and yields useful positive log-growth under relevant alternatives.

T3 is optional. Failure of T3 does not kill the project if T1/T2 plus a safe p-to-e construction remain scientifically useful.

## Search protocol

For every relevant paper record:

1. Full citation / DOI / stable URL.
2. Problem addressed.
3. Statistical model and nuisance assumptions.
4. Test statistic / detector.
5. Fixed-sample or sequential setting.
6. Formal guarantee.
7. Relation to T1/T2/T3.
8. Exact overlap with LIMEN-RF.
9. Novelty threat: LOW / MEDIUM / HIGH / FATAL.
10. Remaining gap, if any.

## Search families

### A. Classical and robust CFAR
- CA-CFAR
- OS-CFAR / order-statistic CFAR
- censored / trimmed / greatest-of / smallest-of CFAR
- nonhomogeneous clutter
- multiple interferers / contaminated reference cells
- clutter edges
- noise-power mismatch / uncertainty

### B. Sequential RF detection
- sequential spectrum sensing
- sequential energy detection
- sequential CFAR
- SPRT with unknown noise power
- quickest detection under noise uncertainty

### C. Anytime-valid inference
- e-values
- e-processes
- test martingales / test supermartingales
- always-valid p-values
- confidence sequences
- optional stopping guarantees

### D. Composite-null robust evidence
- least-favourable distributions
- reverse information projection / RIPr
- invariant e-statistics
- composite-null e-values
- nuisance-robust sequential testing

### E. Adjacent novelty threats
- partial conjunction
- p-value merging / e-value merging
- multiple-testing order statistics
- SNR-wall / noise-uncertainty spectrum sensing

## Evidence matrix

| ID | Citation | Family | Model | Statistic / method | Guarantee | T1 overlap | T2 overlap | T3 overlap | Threat | Remaining gap |
|---|---|---|---|---|---|---|---|---|---|---|
| P01 | TBD |  |  |  |  |  |  |  |  |  |

## High-risk equivalence checks

The search must explicitly answer these questions:

- Does any paper already combine OS-CFAR with sequential optional-stopping-valid inference?
- Does a general e-process theorem make our intended T1 a routine corollary with no RF-specific mathematical content?
- Is the least-favourable mismatch result already standard in robust OS-CFAR theory?
- Is the multi-reference contamination idea merely a known censored/trimmed/OS-CFAR construction?
- Is the proposed e-factor just a standard p-to-e or likelihood-ratio construction under a known least-favourable null?
- Does prior work allow time-varying nuisance parameters at equal or greater generality?

## Gate decision

Final result must be one of:

- **GO** — a defensible methodological gap remains and is nontrivial.
- **REFORMULATE** — current idea is too close to prior art, but a narrower/different theorem is promising.
- **NO-GO** — the central contribution is already known or follows routinely from existing results.

## Minimum acceptance threshold

Before leaving P−1:

- at least 15 highly relevant papers;
- at least 5 CFAR / OS-CFAR papers;
- at least 5 sequential / anytime-valid / e-process papers;
- at least 3 robust/composite-null papers;
- explicit novelty-threat assessment for every high-overlap source;
- a written GO / REFORMULATE / NO-GO decision.
