# Publication validation V1b — contamination-geometry stress test

Date: 2026-09-28

Status: **PREREGISTERED BEFORE V1b OUTCOMES — FROZEN METHOD, GEOMETRY ONLY**

## 1. Purpose

Publication V1 established the frozen Monte Carlo behavior using two deterministic high contaminants at value 2.0, outside the clean support [0,1].

V1b asks one narrow question:

> Does the observed finite-reference advantage of static candidate coupling persist when the geometry of the same two static/exogenous contaminants is changed without retuning the detector?

This is a post-freeze stress test, not a detector-development stage.

No bettor, mixture weight, alpha level, baseline grid, reference size, contamination count, alternative family, or stopping threshold may be changed after V1b outcomes are viewed.

## 2. Scientific scope

V1b tests sensitivity of the empirical power claim to contamination geometry.

It does not:
- prove a new validity theorem;
- validate conditional-on-reference guarantees;
- test value-adaptive identity selection (Model B);
- tune a new bettor;
- tune a new baseline;
- alter the frozen SDR results;
- evaluate the post-freeze accumulated-crossing variant.

The exact-m frozen detector remains the object under test.

## 3. Frozen primary configuration

- K = 32;
- m = 2;
- n = 30;
- alpha = 0.05;
- maximum horizon T = 200;
- reporting horizons: 40, 100, 200;
- clean reference distribution: Uniform(0,1);
- null future stream: Uniform(0,1);
- alternatives: Beta(gamma,1), gamma in {2,4,8};
- 5,000 replications per condition;
- exact frozen static-coupling bettor portfolio from Kill-Test 13;
- exact frozen baseline grid from Kill-Test 13;
- exact frozen oracle candidate wealth construction;
- threshold 1/alpha = 20 for static and oracle.

Primary stress point:

K = 32, gamma = 4, T = 200.

The null and gamma = 2,8 conditions are retained as implementation sanity and weak/strong-shift context.

## 4. Paired path design

V1b must isolate contamination geometry from ordinary Monte Carlo variation.

For each condition and replication:

1. generate the clean reference and future stream using the same per-path seed construction as Publication V1;
2. hold that clean reference and future stream fixed;
3. evaluate all four contamination geometries on that same underlying path.

Thus geometry comparisons are paired at path level.

### Control regression requirement

For geometry G0 below, the observed reference model is exactly Publication V1.

Therefore V1b must reproduce Publication V1 pathwise for G0 when the same seeds and frozen implementation are used.

At K=32, gamma=4, T=200, the archived Publication V1 aggregate targets are:

- static crossing = 0.9144;
- best-grid baseline crossing = 0.1152;
- oracle crossing = 0.9810.

If path-level archived outputs permit exact comparison, use a pathwise regression assertion. Otherwise the G0 aggregate summary must exactly match the archived Publication V1 summary under the reproduced seed stream.

Any mismatch in G0 is an implementation stop condition. Do not interpret G1-G3 until resolved.

## 5. Frozen contamination geometries

Exactly two contaminant values are inserted in each reference bank and labeled contaminated before sorting.

### G0 — high_outside (control)

B = (2.0, 2.0).

Purpose:
- reproduce Publication V1;
- verify the V1b engine before new geometry results are interpreted.

### G1 — upper_inside

B = (0.85, 0.95).

Purpose:
- test deterministic upper-tail contamination inside the clean support;
- force sorted contamination positions to depend on the realized clean reference.

These are fixed population-scale values, not empirical quantiles.

### G2 — mixed_inside

B = (0.10, 0.90).

Purpose:
- test one lower-tail and one upper-tail contaminant inside the clean support;
- remove the special case in which both contaminants occupy the same extreme tail.

### G3 — random_static_inside

For each replication draw independently:

B1, B2 ~ Beta(1/2, 1/2).

Use a dedicated contamination RNG independent of the clean-reference and future-stream RNGs.

Draw the two values once per replication and keep them fixed for the entire online path.

Purpose:
- create random, exogenous, in-support contamination;
- induce random sorted positions without adapting to the realized clean bank.

The Beta(1/2,1/2) law is frozen before outcomes and must not be replaced after V1b.

## 6. Model-A compliance

For every geometry, contaminant values are deterministic or sampled independently of the clean reference and future stream.

No geometry may:
- inspect the realized clean sample before choosing contaminant values;
- choose which clean observations survive based on their values;
- use empirical quantiles of the realized clean reference;
- change contamination values over online time.

All V1b geometries therefore remain inside the static/exogenous Model A addressed by the theorem.

## 7. Dynamic true-candidate bookkeeping — REQUIRED

Publication V1 could hard-code the true candidate as the final two sorted positions because 2.0 > 1.

That assumption is invalid for G1-G3.

For every geometry and replication V1b must:

1. construct a tagged reference list containing n clean values and the two labeled contaminants;
2. sort the tagged reference list by value with a deterministic tie policy;
3. record the one-based sorted positions occupied by contaminated entries;
4. compute observed ranks Q_t against the sorted full reference using the existing bisect_right convention;
5. locate the realized position pair in cfg.candidates;
6. replace true_candidate_index before oracle evaluation.

The robust static lower envelope itself is unchanged.

Implementation should follow the already-audited pattern used in experiments/sdr_semi_synthetic_v1.py.

## 8. Frozen methods reported

### Static coupling — primary method

Use the exact frozen candidate mixture and simultaneous-crossing rule from Publication V1.

The accumulated-running-max variant is not allowed in V1b.

### Precommitted primary baseline

Primary inferential comparator:

band_mix with delta = 0.045.

This comparator is frozen before V1b and is the same precommitted comparator used in SDR validation.

Paired confidence intervals for static minus this primary baseline may be reported because the comparator is fixed independently of V1b outcomes.

### Best-grid baseline envelope — descriptive secondary comparator

Also evaluate the full already-frozen Kill-Test 13 baseline grid.

For every geometry/condition/horizon, report the strongest grid member as a deliberately baseline-favorable descriptive ex-post envelope.

Do not describe an ordinary bootstrap interval conditional on its selected configuration as selection-adjusted.

### Oracle

Use the same frozen candidate wealth family but index the dynamically realized true contamination positions for every replication.

The oracle is an ideal benchmark, not an implementable method.

## 9. Required outputs

Preserve path-level information sufficient to reconstruct every summary.

### Crossing probabilities

For every geometry, condition, method and horizon report:
- crossing count;
- crossing probability;
- 95% Wilson interval.

### Primary paired effect

For static versus the fixed primary baseline, report the paired difference in crossing indicators and a path-paired bootstrap 95% interval.

### Oracle gap

Report oracle minus static crossing probability using paired paths.

### Detection CDF

For each method define the empirical:

F_tau(t) = P(tau <= t), t = 1,...,200.

Save the complete detection CDF to CSV.

Primary CDF figure: gamma = 4.

### Horizon-truncated stopping time

Define tau_dagger as:
- tau if tau <= T;
- T+1 otherwise.

Report E[tau_dagger].

This is the primary delay-like metric because non-detections are included.

Use bootstrap uncertainty where useful.

### Conditional median delay

Retain median stopping time among detected paths only as a secondary descriptive metric.

Always present it together with crossing probability.

### True-position diagnostics

Report the empirical distribution of realized true sorted contamination positions for every geometry.

For G0 the true pair must always be (31,32).

## 10. Null sanity rule

The theorem, not Monte Carlo, supplies validity.

Nevertheless the null is an implementation check.

For any geometry, if the static null crossing estimate at T=200 has a 95% Wilson interval whose lower endpoint exceeds 0.05:

> stop interpretation of alternative results and audit implementation/model generation.

Do not change the detector to repair such an outcome.

A conservative or near-0.05 estimate is only a sanity result, not proof of conditional or hardware validity.

## 11. Pre-specified interpretation at the primary stress point

Let Delta_g be static crossing probability minus the fixed primary-baseline crossing probability at K=32, gamma=4, T=200.

### STRONG GEOMETRY-ROBUST SUPPORT

Use this label only if for every non-control geometry G1-G3:

- the estimated Delta_g is at least 0.15;
- no null sanity stop is triggered.

The 0.15 margin is inherited from the pre-existing Kill-Test 13 effect-size gate rather than chosen after V1b.

### PARTIAL GEOMETRY SUPPORT

Use this label if static remains positively separated from the primary baseline in all G1-G3 but one or more primary-point gaps are below 0.15.

Consequence:
- narrow the empirical claim;
- report geometry dependence explicitly;
- do not retune.

### GEOMETRY-SENSITIVE

Use this label if any non-control geometry has estimated Delta_g <= 0 at the primary point.

Consequence:
- abandon any broad empirical claim of dominance across geometries;
- retain the validity theorem;
- report which geometry removes/reverses the observed advantage;
- do not modify the frozen detector in response.

These labels govern claim scope, not theorem validity.

## 12. Paired geometry effects

Because all geometries share the same clean reference and future stream per replication, report paired changes relative to G0 for:
- static crossing;
- primary-baseline crossing;
- oracle crossing;
- truncated stopping time.

This isolates sensitivity to contamination geometry.

## 13. Seeds and reproducibility

### Publication paths

Reuse exactly the Publication V1 per-path seed construction for K=32 and each condition.

The implementation should import/reuse the existing path-seed helper rather than invent a second clean/stream seed scheme.

### Random-static contamination

Freeze:

V1B_CONTAM_SEED = 20260928.

Derive each G3 contamination RNG deterministically from:
- V1B_CONTAM_SEED;
- condition code;
- replication index.

This RNG must not alter the RNG state used to generate the Publication V1 clean reference/future stream.

### Bootstrap

Use deterministic geometry/condition/horizon/method-specific bootstrap seeds and record them in the manifest.

## 14. Smoke-test discipline

Before the publication run, a smoke test may verify only:
- array/data shapes;
- dynamic oracle positions;
- path pairing;
- output files;
- G0 regression behavior;
- deterministic reproducibility.

The smoke test must use a separate smoke seed namespace and must not be interpreted scientifically.

Only implementation errors may be fixed after smoke testing. Power patterns are not a reason to modify the method.

## 15. Publication run

Run exactly:
- 5,000 replications;
- four conditions: null, Beta(2,1), Beta(4,1), Beta(8,1);
- four frozen geometries;
- same underlying path shared across geometries.

Write all full-run outputs before drafting an interpretation document.

## 16. Required artifacts

Directory:

results/publication_v1b_geometry/

Minimum artifacts:
- raw_paths.csv or equivalent path-level artifact;
- summary.csv;
- paired_effects.csv;
- geometry_effects.csv;
- detection_cdf.csv;
- true_position_diagnostics.csv;
- manifest.json;
- SHA256SUMS;
- PDF and PNG figures.

Recommended figures:
1. crossing probability by geometry at gamma=4, T=200;
2. empirical detection CDF at gamma=4;
3. truncated stopping-time summary by geometry;
4. oracle-static gap by geometry.

## 17. No-retuning rule after first full run begins

Do not:
- change contaminant values/distribution;
- change bettor components or weights;
- change baseline parameters;
- change K, m, T or alpha;
- drop an unfavorable geometry;
- add a favorable geometry;
- alter the random-static law;
- change primary metrics;
- switch to the accumulated-crossing variant.

If a software failure occurs after detector result files are written, preserve those outputs and use post-processing-only finalization, following the SDR V2 discipline.

## 18. Gate after V1b

After all frozen artifacts are written and hashed:

1. interpret geometry results using Section 11;
2. update manuscript claims without retuning;
3. only then proceed to the separately scoped theoretical question:
   what statistical value is obtained by requiring one persistent latent contamination explanation across the entire history?

V1b is the last planned Monte Carlo stress matrix for the frozen detector.
