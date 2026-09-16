# P−1 Certified-Mismatch Firewall 02 — LIMEN-RF

Status: **kill-test / decision pass**

Purpose: test whether the surviving candidate from `candidate_firewall_01.md` — learning/certifying a target/reference scale-mismatch envelope and coupling it to CFAR with continuous-monitoring guarantees — contains a nontrivial methodological contribution.

## Candidate under test

For a detection block `t`, define a target/reference scale ratio

\[
r_t = \frac{\sigma^2_{X,t}}{\sigma^2_{R,t}}.
\]

The detector would like to use a predictable upper envelope `C_t` satisfying, in some rigorous sense,

\[
r_t \le C_t,
\]

before processing the current CUT. The robust tail from the previous static result would then use `C_t` rather than a user-specified fixed mismatch constant.

The novelty claim under test is **not** "confidence sequences + CFAR" or "adaptive thresholding". It would have to be a finite-sample theorem showing that the RF information structure allows nuisance learning and detection to be coupled without losing false-alarm control.

---

## Firewall question 1 — Stationary variance ratio

Assume independent Gaussian calibration samples are available from two stationary populations with

\[
\sigma_X^2,\sigma_R^2 \text{ constant}, \qquad r=\sigma_X^2/\sigma_R^2.
\]

### Decision: **NO-GO as a novelty source**

This problem is classical.

- The ratio of independent Gaussian sample variances has an exact `F` distribution, giving exact fixed-sample confidence intervals for `r`.
- Sequential and group-sequential monitoring of `F` statistics and repeated confidence intervals is old prior art. Jennison & Turnbull (Biometrika, 1991) give exact calculations for sequential `t`, chi-square and `F` tests, including repeated confidence intervals.
- General modern confidence-sequence/e-process machinery provides additional time-uniform routes.

Therefore, if Certified-Mismatch CFAR reduces to "estimate a constant variance ratio with an F interval/confidence sequence, take its upper endpoint, and plug it into a robust threshold", it is a routine combination and fails the novelty gate.

Key source:

- C. Jennison and B. W. Turnbull, “Exact calculations for sequential t, χ² and F tests,” *Biometrika*, 78(1), 133–141, 1991. DOI: 10.1093/biomet/78.1.133.

---

## Firewall question 2 — Estimated noise uncertainty is already an RF topic

### Decision: **HIGH prior-art threat**

The RF/spectrum-sensing literature has already studied the practical consequences of estimating noise variance and then adapting thresholds.

Examples include:

- Bahamou & Nafkha (EUSIPCO 2013), “Noise Uncertainty Analysis of Energy Detector: Bounded and Unbounded Approximation Relationship.” They explicitly connect a confidence interval for an estimated noise level to a bounded noise-uncertainty interval and analyze resulting `Pfa`/`Pd`.
- Kim (2019), “Robust spectrum sensing under noise uncertainty for spectrum sharing,” derives exact false-alarm/detection probabilities for order-statistic sensing under noise uncertainty and calculates thresholds for a target CFAR.
- “Statistical Properties of Energy Detection for Spectrum Sensing by Using Estimated Noise Variance” (2019) analyzes false-alarm behavior under estimated noise variance and proposes improved CFAR thresholds.
- Shams et al. (Scientific Reports, 2026) adapt frequency-domain CFAR thresholds continuously from local interference/noise estimates under uncertainty/jamming.

Thus a paper whose main contribution is only "replace an assumed noise bound by an estimate/confidence interval" is too close to established spectrum-sensing and adaptive-CFAR work.

---

## Firewall question 3 — Arbitrarily time-varying mismatch predicted only from the past

Suppose `C_t` is required to be `F_{t-1}`-measurable, but `r_t` is allowed to vary arbitrarily from block to block with no deterministic or probabilistic dynamics constraint.

### Decision: **ILL-POSED / IMPOSSIBLE without additional structure**

For any finite predictable rule

\[
C_t=C_t(\mathcal F_{t-1}),
\]

if the admissible null class allows arbitrary next-step `r_t`, then after the past is fixed one can choose an admissible null process with

\[
r_t > C_t.
\]

Therefore no nontrivial finite past-only envelope can satisfy

\[
r_t\le C_t
\]

uniformly over such a class.

This is not an advanced statistical obstacle; it is an identifiability/information limitation. A future value cannot be bounded from past observations alone unless the model constrains how the parameter may evolve or provides contemporaneous calibration information.

### Consequence

The scientifically meaningful question must specify at least one of:

1. a dynamics constraint on `r_t` (bounded drift, variation budget, piecewise constancy, stochastic state model, etc.);
2. calibration observations informative about the **current** block before the CUT is tested;
3. a weaker estimand (for example, a running-average conditional quantity rather than instantaneous `r_t`).

General nonstationary confidence-sequence literature reinforces this distinction: valid time-uniform statements under nonstationarity often concern running averaged conditional distributions/parameters, not unrestricted instantaneous latent parameters.

---

## Firewall question 4 — Contemporaneous independent calibration before each CUT

Assume each detection round supplies independent calibration samples from the current target-like and reference-like noise scales before the CUT is evaluated.

### Decision: **NO-GO in the basic Gaussian model**

For Gaussian calibration streams, a current-block variance ratio can be bounded through the classical F distribution. If a per-block bound is constructed independently/predictably before the CUT, coupling it to the static robust threshold is technically clean; generic alpha-spending, repeated-confidence, or e-process machinery can supply time-uniform control.

This architecture may be useful engineering, but in its basic form it does not create enough new mathematics for the central contribution.

---

## Current verdict on Certified-Mismatch CFAR

The broad C1 candidate from `candidate_firewall_01.md` **does not survive in its simplest forms**:

- stationary `r`: **NO-GO** — classical F/sequential-F inference;
- arbitrary time-varying `r_t` from past only: **NO-GO / impossible without structure**;
- contemporaneous independent Gaussian calibration: **NO-GO as methodological novelty** — classical variance-ratio inference plus generic sequential control;
- generic estimated-noise adaptive threshold: **HIGHLY COVERED in RF prior art**.

This is an important narrowing result, not a project failure.

---

## Surviving research space

A candidate can survive only if the **dynamics/information structure itself** creates a nontrivial finite-sample problem.

The next candidate should therefore have the form

> **Lagged calibration under constrained RF drift:** the noise/mismatch state changes between calibration and detection, so a bound valid for the previous calibration state is not automatically valid for the current CUT. Derive a finite-sample inflation/envelope rule that explicitly accounts for admissible drift and preserves false-alarm control under continuous monitoring.

This is intentionally narrower than “adaptive CFAR under changing noise”.

### Minimal model to firewall next

Work in log-scale:

\[
\theta_t = \log r_t.
\]

A calibration stage provides information about a past/current anchor `theta_s`, but the CUT is tested after a lag. Introduce an explicit physical drift class, for example

\[
|\theta_t-\theta_s| \le L\,|t-s|
\]

or a total-variation budget.

The key question is not whether a confidence interval can be widened by a known `L` — that would likely be routine. The kill-test must determine whether a **data-certified or physically measurable drift envelope**, under the RF sampling architecture, yields a theorem not already subsumed by adaptive CFAR, nonstationary confidence bounds, change-point methods, or generic variation-budget theory.

---

## Next kill-test criteria

Before implementation, the lagged-drift candidate must answer:

1. **Physical quantity:** what mechanism makes `r_t` drift (receiver gain, temperature, AGC, frequency response, calibration lag, etc.)?
2. **Information timing:** exactly which samples are observed before the CUT and how old are they?
3. **Dynamics class:** what restriction on `theta_t=log r_t` is justified and falsifiable?
4. **Finite-sample target:** what probability statement is new — current-block nuisance coverage, false-alarm envelope, or joint continuous-monitoring control?
5. **Prior art:** do radar/spectrum-sensing or nonstationary sequential-inference papers already provide the same result under different terminology?

### Kill criterion

If a known drift constant merely adds `L Δt` to a standard confidence bound and everything else follows from generic p/e-process theory, classify the candidate **NO-GO**.

### Survival criterion

Continue only if the calibration lag + RF drift model creates a genuinely nontrivial finite-sample envelope/control problem and the same theorem is not found in prior art.

---

## P−1 state after Firewall 02

- Static OS replacement-contamination worst case: **valid, not central novelty**.
- Generic p→e/Ville sequentialization: **subsumed**.
- Generic colored/correlated CFAR: **mature prior art**.
- Generic RF-specific e-factor: **heavily covered by e-value theory**.
- Stationary certified variance-ratio mismatch: **subsumed by F/sequential-F inference**.
- Arbitrary past-predicted time-varying mismatch: **unidentifiable without dynamics assumptions**.
- Basic current-block independent calibration: **routine**.
- **Only next candidate:** lagged calibration under an explicit, physically defensible drift class — still UNPROVEN and must pass its own firewall.

Decision: **REFORMULATE → Lagged-Drift CFAR firewall.**
