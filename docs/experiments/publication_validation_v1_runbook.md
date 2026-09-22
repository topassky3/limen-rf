# Publication validation V1

This stage is **estimation after method freeze**, not detector development.

The detector, bettor portfolio, baseline grids, horizons, K, m, and primary
data-generating model are inherited unchanged from Kill-Test 13.

## Smoke test

Run first:

    uv run python experiments/pminus1_publication_validation_v1.py \
      --reps 20 \
      --bootstrap-reps 100 \
      --workers 2 \
      --output-dir results/publication_v1_smoke

Expected final marker: `PUBLICATION_V1: COMPLETE`.

## Publication run

After the smoke test passes:

    uv run python experiments/pminus1_publication_validation_v1.py \
      --reps 5000 \
      --bootstrap-reps 2000 \
      --workers 4 \
      --output-dir results/publication_v1

If memory is constrained, use `--workers 2`.

## Outputs

- `summary.csv`: static, strongest ex-post baseline, and oracle with Wilson 95% CIs.
- `paired_differences.csv`: paired gaps with bootstrap 95% CIs.
- `manifest.json`: frozen settings, seed, versions, and Git commit.
- publication figures under `figures/` in PDF and PNG.

The strongest confidence-band result remains an **ex-post adversarial best-grid benchmark**.
It is not one precommitted level-alpha procedure.

## Decision discipline

Do not change bettor, baseline grid, or detector parameters after seeing V1.
Interpretation comes only after the complete run.