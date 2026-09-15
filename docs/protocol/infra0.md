# INFRA-0 — Reproducible research infrastructure

## Objective

Before scientific experiments begin, LIMEN-RF must be reproducible across WSL, GitHub Actions CI, and Google Colab.

## Source of truth

GitHub is the source of truth for code, configuration, tests, protocol decisions, and reproducible experiment definitions.

## INFRA-0.2 acceptance criteria

- [x] `uv sync` succeeds in WSL.
- [x] `uv run pytest` passes in WSL.
- [x] `uv run ruff check .` passes in WSL.
- [x] `uv run python -m limen_rf.smoke` produces deterministic output for the fixed seed.
- [x] `uv.lock` is committed.
- [x] GitHub Actions runs Ruff + pytest + smoke test on pull requests.
- [x] GitHub Actions is green for the reproducible baseline.
- [x] Colab clones the exact frozen commit used for the reproducibility check.
- [x] Colab reproduces the fixed-seed smoke digest.

## Colab verification

Verified digest:

`516b25698869a8e0cf8c43549e47d4b6d5f6c1b548421c969540eba43f657ffb`

Verified seed:

`20260914`

Observed Colab result:

`INFRA-0 COLAB CHECK: PASS`

## Reproducibility rule

Scientific logic must live in `src/limen_rf/` or versioned experiment scripts. Colab notebooks are execution front-ends, not independent sources of scientific logic.

## Gate result

**INFRA-0: PASS**

The project may proceed to P−1 (Prior Art Firewall), followed by P0 foundational distribution validation.
