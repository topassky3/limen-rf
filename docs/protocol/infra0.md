# INFRA-0 — Reproducible research infrastructure

## Objective

Before scientific experiments begin, LIMEN-RF must be reproducible across the local WSL environment and CI, with Colab added as a remote executor later.

## Source of truth

GitHub is the source of truth for code, configuration, tests, protocol decisions, and reproducible experiment definitions.

## INFRA-0.2 acceptance criteria

- [ ] `uv sync` succeeds in WSL.
- [ ] `uv run pytest` passes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run python -m limen_rf.smoke` produces deterministic output for the fixed seed.
- [ ] `uv.lock` is committed.
- [ ] GitHub Actions runs Ruff + pytest + smoke test on pull requests.
- [ ] CI is green.

## Reproducibility rule

Scientific logic must live in `src/limen_rf/` or versioned experiment scripts. Colab notebooks are execution front-ends, not independent sources of scientific logic.

## Current milestone

Issue #1: reproducible Python environment, deterministic smoke test, and CI.
