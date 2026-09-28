# Publication validation V1b — contamination-geometry result

Date: 2026-09-28

Status: **FINALIZED FROM THE FIRST PREREGISTERED 5,000-REPLICATION V1b RUN — DO NOT RERUN FOR OUTCOME IMPROVEMENT**

Runbook:
\`docs/experiments/publication_validation_v1b_geometry_runbook.md\`

Implementation:
\`experiments/pminus1_publication_validation_v1b_geometry.py\`

## Gate integrity

The official output directory was verified absent before the run.

The publication run used:

- \(K=32\);
- \(m=2\);
- \(\alpha=0.05\);
- horizons \(40,100,200\);
- 5,000 replications per condition;
- null Uniform(0,1);
- alternatives Beta(2,1), Beta(4,1), Beta(8,1);
- four preregistered contamination geometries;
- frozen LIMEN-RF bettor portfolio;
- fixed primary comparator \`band_mix, delta=0.045\`;
- full Kill-Test 13 baseline grid as descriptive secondary benchmark only;
- dynamic true sorted contamination positions for the oracle.

All four conditions completed.

The required control regression passed:

\[
\boxed{\text{G0\_FULL\_REGRESSION: PASS}}
\]

Thus the \`high_outside\` control exactly reproduces the archived Publication V1 results under the reused Publication V1 path seeds.

The null implementation sanity gate also passed:

\[
\boxed{\text{V1B\_NULL\_SANITY: PASS}}
\]

The run ended with:

\[
\boxed{\text{V1B\_PUBLICATION: COMPLETE}}
\]

## Primary preregistered stress point

Primary point:

\[
K=32,\qquad \gamma=4,\qquad T=200.
\]

| Geometry | Static | Primary baseline | Static - primary | Best-grid baseline | Oracle | Mean truncated static stop |
|---|---:|---:|---:|---:|---:|---:|
| high_outside | 0.9144 | 0.1152 | 0.7992 | 0.1152 | 0.9810 | 42.78 |
| upper_inside | 0.8894 | 0.2162 | 0.6732 | 0.2162 | 0.9810 | 41.23 |
| mixed_inside | 0.9422 | 0.3742 | 0.5680 | 0.3742 | 0.9810 | 27.49 |
| random_static_inside | 0.9468 | 0.3948 | 0.5520 | 0.3948 | 0.9810 | 26.39 |

## Preregistered decision

The runbook specified **STRONG GEOMETRY-ROBUST SUPPORT** if, for each non-control geometry G1-G3:

1. the estimated static-minus-primary-baseline crossing gap is at least 0.15 at the primary point; and
2. no null sanity stop is triggered.

Observed gaps:

- upper_inside: \(0.6732\);
- mixed_inside: \(0.5680\);
- random_static_inside: \(0.5520\).

All exceed the preregistered 0.15 margin by a large amount, and the null sanity gate passed.

Therefore:

\[
\boxed{\text{V1b DECISION: STRONG GEOMETRY-ROBUST SUPPORT}}
\]

This decision is about the empirical finite-reference comparison under the preregistered Model-A geometries. It does not strengthen the theorem beyond its stated assumptions.

## Interpretation

### 1. The Publication V1 advantage is not an artifact of placing both contaminants at 2.0

The robust static procedure retains high crossing probability when contaminants are moved inside the clean support, split across low/high regions, or sampled randomly and independently inside the support.

The weakest static crossing probability among the three new primary-point geometries is 0.8894.

### 2. Geometry changes the difficulty of the primary confidence-band comparator substantially

The fixed primary baseline rises from 0.1152 in the original outside-support geometry to:

- 0.2162 for upper_inside;
- 0.3742 for mixed_inside;
- 0.3948 for random_static_inside.

Thus the original geometry was especially unfavorable to this generic band comparator.

This makes the V1b result scientifically useful: the large original gap shrinks under more favorable baseline geometries, but remains far above the preregistered 0.15 effect-size gate.

### 3. Static coupling remains close to the oracle in crossing probability

Oracle crossing is 0.9810 in all four geometries at the primary point.

This is structurally expected: once the true contaminated positions are supplied, the oracle reconstructs the same canonical clean-rank sequence, so contaminant geometry should not change oracle behavior when the clean reference and future path are held fixed.

The static procedure remains:

- 0.0666 below oracle for high_outside;
- 0.0916 below oracle for upper_inside;
- 0.0388 below oracle for mixed_inside;
- 0.0342 below oracle for random_static_inside.

These are descriptive point gaps; uncertainty should be read from the frozen paired artifacts.

### 4. The stronger delay metric does not reveal a hidden penalty

The preregistered mean horizon-truncated stopping metric for static is:

- 42.78 high_outside;
- 41.23 upper_inside;
- 27.49 mixed_inside;
- 26.39 random_static_inside.

Because this metric assigns \(T+1\) to non-detections, it does not condition on successful detection.

At the primary point, the mixed and random-static geometries are not merely associated with high crossing probability; they also have substantially smaller truncated stopping means than the outside-support control.

No causal or universal monotonic geometry claim should be inferred from four designed geometries.

## Claim discipline

The defensible empirical statement after V1b is:

> Under the preregistered \(K=32,m=2\) Model-A stress matrix, the frozen static-coupling detector retained high finite-horizon crossing probability across outside-support, in-support upper-tail, mixed-tail, and independently random static contamination geometries. The fixed primary confidence-band comparator improved substantially for in-support geometries, reducing but not eliminating the large empirical gap.

Do not claim:

- uniform dominance over all contamination geometries;
- minimax optimality;
- conditional-on-reference validity;
- robustness to value-adaptive identity selection;
- robustness to online-changing contamination identities;
- hardware type-I validity.

## Frozen artifacts

Expected official local artifacts:

- \`results/publication_v1b_geometry/raw_paths.npz\`
- \`results/publication_v1b_geometry/summary.csv\`
- \`results/publication_v1b_geometry/paired_effects.csv\`
- \`results/publication_v1b_geometry/geometry_effects.csv\`
- \`results/publication_v1b_geometry/detection_cdf.csv\`
- \`results/publication_v1b_geometry/true_position_diagnostics.csv\`
- \`results/publication_v1b_geometry/manifest.json\`
- \`results/publication_v1b_geometry/SHA256SUMS\`
- publication figures in PDF and PNG.

Observed frozen hashes:

- \`detection_cdf.csv\`: \`f800eed7be53557207f931dbe122c74a38478b402e7c87adace24d49d71f7899\`
- \`crossing_by_geometry_gamma4_T200.pdf\`: \`841fe3ef24968dac6db9562033afdd429b41bc0d9353fb5cd91351866b857642\`
- \`crossing_by_geometry_gamma4_T200.png\`: \`157d44ee92303c5f316aade9720e5bcf4ddd39432cdd53779d37f8f672de0d3a\`
- \`static_detection_cdf_gamma4.pdf\`: \`7a4f8c1d9ecb520864620d5ebae41825c1e1623bbf2611c4e85b64ed724b46ef\`
- \`static_detection_cdf_gamma4.png\`: \`e78403bcff8bf446045c47c7521b84874a7c67fb532ec8af9544663f13a6a54c\`
- \`truncated_stop_by_geometry_gamma4.pdf\`: \`f6723b03ebe3a43f6d0a3c7c7abe17c39a1be20b3e3219d9c8a2e0e516ca3f39\`
- \`truncated_stop_by_geometry_gamma4.png\`: \`e524d832064807f8e8a886bd4fe56031682492f2c63a2a2538fffdc71884a56f\`
- \`geometry_effects.csv\`: \`a0e3545a9601d50e0813b8021fa588cfbea5c5bf5f4bfcfc6e9339201b063d10\`
- \`manifest.json\`: \`edec6ceaca7357dcebd12b20ae7687860f7b0f7b83218779636bd51cd7a1daec\`
- \`paired_effects.csv\`: \`67540be1bf312badf3179adc37aae2e45857ae705a23bee21167225bce9d04b6\`
- \`raw_paths.npz\`: \`bf65c4cf49dea3477b11a1f35aed0482c3f8aa6b3166058864b2a9f3cbc12673\`
- \`summary.csv\`: \`504c3431b25dbd849e350ec0badacab33f026cc3e7b8d767d2967f96badfebae\`
- \`true_position_diagnostics.csv\`: \`0991542fc92bc803d948d5ec3d3bdd380752088c82be0208807d78ff989f49f5\`

These artifacts must be archived verbatim before manuscript updating or any new theoretical exploration.

## Next gate

Do not run another V1b Monte Carlo matrix.

Next sequence:

1. archive/version the frozen V1b artifacts;
2. extract the pre-specified paired uncertainty summaries from existing outputs only;
3. update the manuscript experimental section with V1b plus SDR V1/V2;
4. perform a targeted prior-art firewall for the post-freeze accumulated-candidate-elimination stopping rule;
5. allow at most one bounded theoretical extension on the statistical value of persistent contamination identity.
