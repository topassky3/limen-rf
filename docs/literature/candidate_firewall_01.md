# P−1 Candidate Firewall 01 — surviving novelty candidates

Status: **candidate selection pass**

Purpose: after the static worst-case lemma and the sequentialization firewall removed the original T2/T1 novelty claims, compare three narrower candidate contributions and select at most one for deeper work.

## Candidates under review

### C1 — Data-driven nuisance envelope
Learn or certify an upper bound \(c_t\) on the target/reference scale mismatch from past/background data, then use that bound inside a robust CFAR tail while preserving a rigorous sequential false-alarm guarantee.

### C2 — Correlated / colored reference cells
Replace the independent Gamma reference model by a correlated/colored RF background and derive a robust CFAR guarantee under dependence.

### C3 — RF-specific efficient e-factor
Construct an RF-specific e-variable/e-process for the OS/reference statistic that is substantially more efficient than generic p→e calibration.

---

## Evidence matrix

| ID | Source / family | Relevant result | Threat | Candidate affected |
|---|---|---|---|---|
| C01 | Howard, Ramdas, McAuliffe & Sekhon (2021), *Time-uniform, nonparametric, nonasymptotic confidence sequences* | General nonasymptotic confidence-sequence machinery, including self-normalized and matrix settings. | HIGH | C1 |
| C02 | Wang & Ramdas (2025), *Anytime-valid t-tests and confidence sequences for Gaussian means with unknown variance* | Explicit e-processes and CSs with an unknown nuisance scale. | HIGH | C1 |
| C03 | Wasserman, Ramdas & Balakrishnan (2020), *Universal inference* | Split likelihood methods handle composite nulls, nuisance/profile likelihoods, and sequential anytime-valid inference. | VERY HIGH | C1, C3 |
| C04 | Pace, Salvan & Sartori (2023), *Confidence sequences with composite likelihoods* | Confidence sequences with nuisance parameters and dependent/composite likelihood components are already a studied problem. | HIGH | C1, C2 |
| C05 | Jennison & Turnbull (1991), sequential t/chi-square/F tests | Classical exact sequential inference already includes scale/variance testing. | MEDIUM-HIGH | C1 |
| C06 | Barkat/Varshney adaptive CFAR line (1980s onward) | Adaptive CFAR was explicitly designed for unknown/nonstationary background power. | HIGH | generic C1 |
| C07 | Kay (1999), *Adaptive detection for unknown noise power spectral densities* | Adaptive detection in colored noise with unknown PSD; asymptotic CFAR property. | VERY HIGH | C2 |
| C08 | Recent stationary-GP detector in complex Gaussian colored noise (2024/2025 literature) | Models CUT and adjacent cells as a Gaussian process and derives exact PFA under colored noise. | VERY HIGH | C2 |
| C09 | Classical OS/TM/LCOS/VI/GO/SO CFAR literature | Correlation, clutter edges, nonhomogeneity and adaptive reference processing have decades of prior art. | VERY HIGH | C2 |
| C10 | Grünwald, de Heide & Koolen (2024), *Safe testing* | GRO e-values for composite null/alternative models with nuisance parameters. | VERY HIGH | C3 |
| C11 | Pérez-Ortiz et al. (2024), *E-statistics, group invariance and anytime-valid testing* | GROW invariant e-statistics; scale-location families are explicit examples. | VERY HIGH | C3 |
| C12 | Larsson, Ramdas & Ruf (2025), *The numeraire e-variable and reverse information projection* | A log-optimal e-variable exists for arbitrary composite null vs point alternative; generalized RIPr. | VERY HIGH | C3 |
| C13 | Hao & Grünwald (2024), *E-Values for Exponential Families: the General Case* | RIPr, conditional e-values, universal inference and sequentialized RIPr for composite exponential-family nulls. | VERY HIGH | C3 |
| C14 | Direct targeted searches for exact `anytime-valid CFAR + learned mismatch bound` | No obvious paper was found that gives a finite-sample RF-CFAR theorem with an online-certified local target/reference mismatch envelope and continuous-monitoring guarantee. | weak positive signal only | C1 |

---

## Candidate C2 — correlated / colored references

### Decision: **NO-GO as a generic novelty direction**

There is extensive signal-processing prior art on:

- CFAR under correlated sweeps;
- colored noise and unknown PSD;
- adaptive covariance/noise estimation;
- nonhomogeneous clutter and clutter edges;
- Gaussian-process based background modelling;
- rank/censoring/variability-index reference selection.

A statement such as “we extend CFAR to correlated or colored reference cells” would be too broad and too close to mature literature. A very specific dependence model could still support an engineering paper, but it is not currently the strongest novelty candidate.

---

## Candidate C3 — RF-specific efficient e-factor

### Decision: **NO-GO as the next primary direction**

General theory is already exceptionally strong. The existence and optimality of e-variables for composite nulls is not new; scale-invariant constructions are specifically covered; and exponential-family e-values/e-processes are already developed.

A closed-form RF specialization could still be useful, but unless it requires genuinely new mathematics and gives a substantial practical advantage, it risks being a domain-specific instantiation of known theory. It is therefore not the best place to spend the next research cycle.

---

## Candidate C1 — online-certified mismatch envelope

### Decision: **SURVIVES, but only after sharpening**

The generic statement

> “estimate \(c_t\) from past data and plug it into the detector”

is **not novel** and is not automatically valid.

General confidence-sequence, universal-inference and nuisance-parameter theory already provide broad tools for sequential uncertainty quantification. Classical adaptive CFAR also already tracks unknown/time-varying background power.

The potentially nontrivial question is narrower:

> Can we construct a **finite-sample, time-uniformly certified upper envelope for the local target/reference RF scale mismatch**, based only on permissible background/calibration observations, and couple that envelope to the robust CFAR tail so that the final continuously monitored detector has a rigorously controlled false-alarm probability despite nuisance uncertainty?

This is materially different from simply plugging in an estimate. If the learned bound underestimates the true mismatch, the conditional superuniformity argument in the sequentialization firewall fails.

### Important validity warning

A standard confidence sequence with simultaneous coverage

\[
\Pr(\forall t:\ r_t\le C_t)\ge 1-\delta
\]

is not by itself enough to claim that a p→e product remains an \(\alpha\)-level e-process when the same dependent data drive both \(C_t\) and the detector. Conditioning on a global coverage event can change the law of the detection statistic.

Any valid construction must therefore make the information structure explicit. Possible safe architectures include:

1. an independent/background-only calibration stream whose history determines \(C_t\) before the current detection block;
2. a joint supermartingale/e-process that accounts for nuisance estimation and detection simultaneously;
3. a sample-splitting or predictable likelihood construction with a proof of conditional validity.

These are not assumed novel; they define the next kill-test.

---

## Selected survivor

The only candidate worth a dedicated next firewall is:

### **Certified-Mismatch CFAR**

Provisional scientific question:

\[
\boxed{
\text{Can an RF receiver learn a local mismatch envelope online and retain a finite-sample continuous-monitoring false-alarm guarantee?}
}
\]

The intended novelty is **not** confidence sequences, adaptive CFAR, or e-processes separately. It would have to be an explicit finite-sample coupling theorem for the RF mismatch quantity and detector under a physically defensible information structure.

---

## Exact next kill-test

Before implementation, answer these four questions:

1. **Parameter:** what exact RF quantity is \(r_t\)? Is it a stationary scale ratio, a locally constant ratio, or a time-varying latent process?
2. **Observations:** which samples are available to estimate/bound it without using the current CUT in an invalid way?
3. **Guarantee:** can we derive an exact or conservative predictable upper envelope \(C_t\) with a finite-sample guarantee strong enough to imply detector validity?
4. **Prior art:** does radar/spectrum-sensing literature already contain the same certified adaptive threshold, perhaps under different terminology such as noise uncertainty, adaptive CFAR, cognitive CFAR, or feedback false-alarm regulation?

### Kill criterion

If the chosen RF model reduces to a standard confidence sequence for a Gamma/variance ratio followed by a standard CFAR threshold, and the validity proof is a routine combination of existing results, classify this candidate **NO-GO** as a methodological novelty.

### Survival criterion

Continue only if the RF information structure creates a nontrivial finite-sample problem that is not already covered by existing adaptive-CFAR or confidence-sequence theory and can be stated as a precise theorem.

---

## Current P−1 state

- Original static least-favourable theorem: **valid, but not central novelty**.
- Generic anytime-valid sequentialization: **subsumed**.
- Generic colored/correlated CFAR: **too mature**.
- Generic RF-specific e-factor: **too heavily covered by modern e-value theory**.
- Online-certified mismatch envelope: **only surviving candidate, still UNPROVEN**.

Decision: **REFORMULATE → narrow firewall on Certified-Mismatch CFAR.**
