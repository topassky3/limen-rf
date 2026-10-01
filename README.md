# LIMEN-RF

**Anytime-valid predictive-rank detection with a statically contaminated fixed reference set**

[![CI](https://github.com/topassky3/limen-rf/actions/workflows/ci.yml/badge.svg)](https://github.com/topassky3/limen-rf/actions/workflows/ci.yml)

LIMEN-RF is a reproducible research repository for sequential distribution-shift detection when a finite reference bank already contains a small, unknown set of **static/exogenous contaminated observations** and the same bank is repeatedly reused online.

**Author:** Juan Felipe Orozco Cortés  
**Manuscript:** *Anytime-Valid Predictive-Rank Detection with a Statically Contaminated Reference Set*  
**Research status:** theory core frozen, publication-scale Monte Carlo complete, contamination-geometry stress test complete, RTL-SDR V1/V2 engineering characterization complete, manuscript prepared for peer review.

## Core idea

Let a fixed reference bank contain (K) observed values, exactly (m) of which are static/exogenous contaminants. For every candidate set (C) of contaminated sorted positions, LIMEN-RF reconstructs a candidate clean-reference rank sequence

[
R_t^{(C)} = Q_t - \#\{c \in C : c \le Q_t\}.
]

For the true candidate (C^\star), this is exactly the rank against the latent clean reference sample. The same pre-specified predictive-rank betting functional is applied to every candidate. The robust evidence is the pointwise lower envelope

[
\underline E_t = \min_C E_t^{(C)}.
]

Because (\underline E_t \le E_t^{(C^\star)}) pathwise and the true-candidate wealth is a valid clean predictive-rank martingale, threshold crossing is anytime-valid under the stated iid continuous, static/exogenous model.

**Important:** the lower envelope itself is **not** claimed to be a martingale, supermartingale, or e-process.

## Main scientific contributions

- pathwise reconstruction of the latent clean rank process under unknown persistent contamination identities;
- finite-sample anytime threshold-crossing control through true-candidate domination;
- an upper-bound-only contamination-count corollary;
- a one-to-one contiguous-partition representation of candidate deletions;
- an exact (O(Km^2))-time, (O(Km))-memory dynamic program for a fixed categorical bettor;
- frozen publication-scale Monte Carlo, a pre-specified contamination-geometry stress test, and semi-synthetic RTL-SDR engineering validation.

## Publication-scale results

Primary frozen simulation setting: (K=32), (m=2), (T=200), (X_t\sim\mathrm{Beta}(4,1)), 5,000 replications.

| Method | Crossing probability by (T=200) |
|---|---:|
| Static candidate coupling | 0.9144 |
| Designated band comparator | 0.1152 |
| Oracle | 0.9810 |

The pre-specified V1b geometry stress test retained static crossing probabilities from **0.8894 to 0.9468** across the three non-control geometries at the primary point.

RTL-SDR V2 uses 30 fresh captures and a weaker injected-SNR grid. At (-18\) dB, static coupling crossed on **14/30** captures, the fixed band comparator on **0/30**, and the oracle on **18/30**. At (-15\) dB the counts were **22/30**, **12/30**, and **24/30**.

The SDR experiments are **engineering sensitivity characterizations only**: the score streams exhibit serial dependence and the controlled signal injection occurs after the ADC, so the iid theorem is not claimed as hardware type-I validation.

## Scope

The theorem assumes:

- scalar observations from an unknown continuous null distribution (F);
- a fixed observed reference bank;
- static/exogenous contaminated identities;
- deleting the true contaminated cells leaves an iid clean reference sample;
- future null observations are iid from the same (F).

The current paper does **not** claim validity for value-adaptive replacement after inspecting the clean bank, online-changing contamination identities, temporal dependence, arbitrary drift, minimax optimality, or universal superiority over conformal/CCTM/e-process methods.

## Repository map

- `src/limen_rf/` — reusable implementation.
- `tests/` — regression/unit tests.
- `experiments/` — frozen simulation and SDR experiment drivers.
- `configs/` — experiment configuration.
- `docs/math/` — theorem development, method freeze, and formal audit.
- `docs/experiments/` — pre-outcome protocols/runbooks and frozen result notes.
- `docs/literature/` — prior-art and novelty audits.
- `results/publication_v1/` — publication-scale Monte Carlo summaries and figures.
- `results/publication_v1b_geometry/` — geometry-stress artifacts, hashes, and figures.
- `results/sdr_publication_v2/` — finalized SDR V2 derived outputs and figures.
- `paper/` — shared manuscript source.
- `paper/redin/` — journal-format identified and double-blind manuscript wrappers.

## Quick start

The repository uses Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/topassky3/limen-rf.git
cd limen-rf

uv sync --locked
uv run ruff check .
uv run pytest
uv run python -m limen_rf.smoke
```

For the frozen publication workflows, see **[REPRODUCIBILITY.md](REPRODUCIBILITY.md)**.

## Reproducibility discipline

The detector portfolio and experiment settings were frozen before the publication-scale outcomes were used for manuscript conclusions. Historical runbooks are preserved in `docs/experiments/`.

Terminology note: some historical internal artifacts use the word **“preregistered.”** The manuscript uses the more precise description **“pre-specified and repository-frozen before outcomes were viewed”** because the protocol was frozen in repository history rather than registered in an external preregistration registry.

No additional Monte Carlo matrix or SDR detector rerun is planned for outcome improvement.

## Data availability

Simulation outputs, manifests, hashes, figures, source code, protocols, and derived RTL-SDR result tables are versioned in this repository.

Raw receiver IQ captures are intentionally not versioned under `data/` (the directory is ignored by Git). Therefore the simulation study is directly reproducible from the repository, while the physical-capture portion is auditable from frozen derived artifacts and requires the original/local IQ captures for detector-level replay.

## Citation

GitHub will expose citation metadata from **[CITATION.cff](CITATION.cff)**. Once the associated article receives a DOI, the citation file should be updated to prefer the published article.

## License

No open-source license has been selected yet. Public visibility alone does not grant reuse rights. A software/data license should be chosen explicitly before encouraging third-party redistribution.
