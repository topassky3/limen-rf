# Reproducibility guide

This document separates **software verification**, **frozen simulation regeneration**, and **RTL-SDR artifact auditing**. The scientific method and publication-scale detector settings are frozen; do not retune parameters in response to reproduced outcomes.

## 1. Environment

Requirements:

- Python 3.13 or 3.14;
- [uv](https://docs.astral.sh/uv/);
- a POSIX-like shell for the commands below.

From a fresh clone:

```bash
git clone https://github.com/topassky3/limen-rf.git
cd limen-rf
uv sync --locked
```

Verify the software layer:

```bash
uv run ruff check .
uv run pytest
uv run python -m limen_rf.smoke
```

The GitHub Actions workflow runs the same lint/test/smoke sequence on `main`.

## 2. Publication Monte Carlo V1

Protocol:

`docs/experiments/publication_validation_v1_runbook.md`

Run a small implementation smoke test first:

```bash
uv run python experiments/pminus1_publication_validation_v1.py \
  --reps 20 \
  --bootstrap-reps 100 \
  --workers 2 \
  --output-dir results/reproduction_publication_v1_smoke
```

Expected terminal marker:

```text
PUBLICATION_V1: COMPLETE
```

For an independent full reproduction, write to a new directory rather than overwriting the archived publication artifacts:

```bash
uv run python experiments/pminus1_publication_validation_v1.py \
  --reps 5000 \
  --bootstrap-reps 2000 \
  --workers 4 \
  --output-dir results/reproduction_publication_v1
```

The archived publication result is under `results/publication_v1/`.

## 3. Contamination-geometry stress test V1b

Frozen protocol:

`docs/experiments/publication_validation_v1b_geometry_runbook.md`

Implementation:

`experiments/pminus1_publication_validation_v1b_geometry.py`

The historical V1b protocol was pre-specified and committed before V1b outcomes. Some internal artifacts use the word *preregistered*; the manuscript uses the more precise wording **repository-frozen before outcomes were viewed**, because there was no external preregistration registry.

Implementation-only smoke test:

```bash
uv run python experiments/pminus1_publication_validation_v1b_geometry.py \
  --reps 20 \
  --bootstrap-reps 100 \
  --workers 2 \
  --block-size 25 \
  --output-dir results/reproduction_publication_v1b_smoke \
  --smoke
```

A full independent reproduction may be run into a separate directory:

```bash
uv run python experiments/pminus1_publication_validation_v1b_geometry.py \
  --reps 5000 \
  --bootstrap-reps 2000 \
  --workers 4 \
  --block-size 25 \
  --output-dir results/reproduction_publication_v1b_geometry
```

Do **not** overwrite `results/publication_v1b_geometry/`. Those files are the archived first full-run artifacts and include `SHA256SUMS`.

## 4. Archived result integrity

Publication V1b includes a SHA-256 manifest:

```bash
sha256sum -c results/publication_v1b_geometry/SHA256SUMS
```

SDR V2 also includes:

```bash
sha256sum -c results/sdr_publication_v2/SHA256SUMS
```

Run these from the repository root.

## 5. RTL-SDR V2

Protocol:

`docs/experiments/sdr_publication_v2_runbook.md`

Frozen result note:

`docs/experiments/sdr_publication_v2_result.md`

The repository versions the derived V2 artifacts:

- `qc.csv`;
- `raw_results.csv`;
- `summary.csv`;
- `manifest.json`;
- figures;
- `SHA256SUMS`.

The raw IQ captures are **not** committed because `data/` is intentionally ignored. Detector-level replay of the physical experiment therefore requires the original captures or a fresh acquisition performed under the documented receiver settings. The committed derived artifacts remain auditable and hash-verifiable.

The SDR score streams exhibit serial dependence and injection is post-ADC. These experiments are engineering sensitivity characterizations, not hardware validation of the iid type-I theorem.

## 6. Manuscript

The shared scientific source is under:

```text
paper/sections/
paper/references.bib
```

The REDIN-format wrappers are:

- `paper/redin/article.tex` — identified author version;
- `paper/redin/article_blind.tex` — double-blind reviewer version.

The REDIN class supplied by the journal requires XeLaTeX in practice. See:

`paper/redin/README.md`

for the required template-support files and exact compilation commands.

## 7. Scientific freeze

The frozen statistical core is documented in:

`docs/math/method_freeze_post_killtest13.md`

The independent formal audit is:

`docs/math/formal_audit_external_review_v0_1.md`

The narrow prior-art/novelty sweep is:

`docs/literature/final_novelty_sweep_static_contaminated_reference.md`

Reproducing an archived experiment is welcome; retuning the frozen detector and presenting the result as the original publication experiment is not.
