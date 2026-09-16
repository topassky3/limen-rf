# P−1 Lagged-Drift Firewall 03 — LIMEN-RF

Status: **kill-test / decision pass**

Purpose: test whether the surviving `Lagged-Drift CFAR` idea contains a nontrivial methodological contribution, or whether its mathematical core is already subsumed by adaptive-CFAR, calibration-drift, nonstationary inference, and set-membership estimation literature.

## Candidate under test

Let

\[
\theta_t = \log r_t, \qquad r_t = \sigma^2_{X,t}/\sigma^2_{R,t}.
\]

A calibration at time `s<t` gives information about `theta_s`, while a CUT is tested at time `t`. The receiver state may drift in the interval. A schematic deterministic drift class is

\[
|\theta_t-\theta_s|\le L|t-s|.
\]

The original hope was that a finite-sample drift inflation/envelope could be coupled to the robust CFAR tail and then to continuous monitoring.

The novelty claim under test is **not** “RF gain drifts”, “periodic calibration”, “bounded drift”, “set-membership tracking”, or “adaptive CFAR” separately. A central theorem would have to solve an RF-specific inferential/control problem not obtainable by routine composition of those tools.

---

## Evidence matrix

| ID | Source / family | Relevant result | Threat | Assessment |
|---|---|---|---|---|
| D01 | Classical and modern CFAR literature | CFAR already adapts thresholds to local/nonstationary noise and clutter; clutter edges and nonhomogeneous backgrounds are mature topics. | Generic “time-varying background” claim is not novel. | **VERY HIGH** |
| D02 | Shams et al., *Scientific Reports* 2026, adaptive frequency-domain CFAR | Explicitly motivates adaptive thresholding by time-varying receiver noise due to temperature, hardware and environment, and continuously updates thresholds from local noise/interference estimates. | Direct RF-domain overlap with dynamic thresholds under changing noise. | **VERY HIGH** |
| D03 | Alhashimi et al., *Autonomous Robots* 2024, BFAR | Radar detector with a specified upper bound on false-alarm probability and learned threshold parameters; evaluated under heterogeneous noise. | Shows “bounded false alarm” + learned radar threshold is already a named engineering direction. | **HIGH** |
| D04 | Receiver/radiometer calibration literature | Gain fluctuations/drift caused by temperature and active components are well known; periodic calibration, injected references and gain correction are standard engineering remedies. | Physical motivation alone is not novel. | **VERY HIGH** |
| D05 | LiteBIRD simulation framework / radiometer practice | Linear and thermal gain-drift models, including periodic recalibration and 1/f temperature-driven gain drift, are explicit system models. | Known-drift + periodic calibration model is established engineering practice. | **HIGH** |
| D06 | Mineiro & Howard, NeurIPS 2023, time-uniform confidence bands under nonstationarity | Gives time-uniform inference for running averaged conditional distributions and explicitly notes limitations/impossibility for unrestricted instantaneous nonstationary targets. | Reinforces that current-state inference requires structural assumptions. | **HIGH** |
| D07 | Besbes et al. / Chen-Wang-Wang nonstationary optimization | Variation budgets and bounded temporal variation are mature abstractions for nonstationarity. | A variation-budget assumption is not itself novel. | **HIGH** |
| D08 | Set-membership estimation literature (Bertsekas-Rhodes lineage; Belforte-Bona-Cerone 1990; Walter-Piet-Lahanier 1990; later time-varying filters) | Recursively propagates sets containing unknown states/parameters under bounded disturbances; time-varying systems and incomplete observations are covered. | A bounded-drift state envelope from delayed/noisy measurements is a classical estimation architecture. | **FATAL to generic mathematical novelty** |
| D09 | Parameter bounding for time-varying systems / set-membership identification | Explicitly treats time-varying parameters with bounded perturbations and recursive uncertainty sets. | Directly threatens a theorem based on “parameter moves by at most L per step; propagate interval/ellipsoid”. | **FATAL to simple drift theorem** |
| D10 | RTL-SDR hardware documentation and practice | RTL-SDR devices exhibit warm-up/temperature-related frequency drift; manual gain is recommended for stable sensing; noise floor depends strongly on gain/overload. | Confirms a cheap-SDR drift problem is physically plausible. | **Positive motivation, not novelty** |
| D11 | Targeted search: `RTL-SDR + CFAR + temperature/noise-floor drift + certified Pfa` | No obvious peer-reviewed paper was identified in this pass that characterizes low-cost RTL-SDR power-scale drift and couples a measured calibration envelope to a finite-sample CFAR false-alarm guarantee. | Possible engineering gap. Absence from targeted search is not proof of novelty. | **SURVIVING SIGNAL** |

---

## Kill-test A — Known deterministic drift constant

Assume a valid calibration upper bound at time `s`,

\[
\theta_s \le U_s,
\]

and a known deterministic drift limit

\[
|\theta_t-\theta_s|\le L(t-s).
\]

Then immediately

\[
\theta_t\le U_s+L(t-s),
\]

or equivalently

\[
r_t\le \exp\{U_s+L(t-s)\}.
\]

Plugging this inflated bound into the previously derived monotone worst-case CFAR tail is a routine robust-design step.

### Decision

**NO-GO as central novelty.**

The propagation is elementary, and the surrounding ideas — bounded drift, robust envelopes, periodic calibration and adaptive thresholding — are mature.

---

## Kill-test B — Unknown drift estimated from bounded-error calibration history

Suppose calibration observations are noisy but errors and state increments are deterministically bounded. Then the problem becomes a set-membership state/parameter estimation problem:

\[
\theta_{t+1}=\theta_t+w_t, \qquad |w_t|\le L_t,
\]

with bounded observation uncertainty.

Recursive feasible intervals/ellipsoids containing the current state under bounded disturbances have existed for decades. Time-varying systems, missing observations, outliers and nonlinear models have extensive set-membership literature.

### Decision

**NO-GO as a generic methodological theorem.**

An RF specialization could be useful, but “propagate a certified state set under bounded drift and use its upper endpoint in a detector” is not a new statistical/control principle.

---

## Kill-test C — Stochastic drift model

If drift is modeled probabilistically (random walk, AR process, 1/f thermal process, Gaussian state-space model), then current-state prediction from lagged calibration becomes filtering/prediction under a state model. Kalman/Bayesian filters, robust filters, set-membership filters and sequential uncertainty methods provide standard machinery.

### Decision

**NO-GO unless a very specific RF model produces a new exact result.**

Simply placing an e-process after a state estimator does not establish validity, and deriving a valid joint construction would still have to overcome substantial prior art in state-space inference and safe/sequential testing.

---

## Important discovery — BFAR changes our terminology discipline

Alhashimi et al. (2024) already use the name **bounded false-alarm rate (BFAR)** for a radar detector. Their method is different from LIMEN-RF, but the existence of this paper means we should avoid framing our novelty as merely “bounded false alarm” or inventing confusingly similar terminology.

Any future name/claim must state the exact guarantee and information structure.

---

## Physical reality check

Lagged calibration is not an artificial problem. RF hardware really drifts:

- receiver gain can change with temperature and active-device state;
- radiometric systems use periodic calibration, noise injection and reference signals to track gain;
- RTL-SDR-class devices exhibit warm-up/temperature effects, frequency drift, gain/noise-floor dependence and overload effects;
- local CFAR estimates can adapt to environmental noise, but that is different from certifying receiver transfer-function drift between calibration and detection.

Thus the **engineering phenomenon is real**, even though the generic mathematics is mature.

---

## Firewall decision on Lagged-Drift CFAR

### As a new general statistical theorem

**NO-GO.**

The simple cases are covered by elementary drift inflation, set-membership estimation, state-space filtering, nonstationary-inference abstractions, and generic anytime-valid machinery.

### As an RF engineering contribution

**SURVIVES in a narrower form.**

The targeted search did not identify an obvious peer-reviewed study with the exact combination:

1. low-cost RTL-SDR-class receiver;
2. controlled characterization of *power-scale/noise-floor* drift (not just frequency PPM drift) versus warm-up / temperature / center frequency / gain state;
3. explicit demonstration that stale calibration breaks a nominal CFAR false-alarm target;
4. a calibration-age / hardware-state envelope derived from measured data;
5. a finite-sample or conservatively validated upper bound on false-alarm performance;
6. reproducible open SDR experiment/data/code.

This is **not yet a novelty claim**. It is the first candidate in the firewall whose plausible contribution may be primarily measurement/system engineering rather than a new general theorem.

---

## Proposed reformulation — Hardware-Aware Calibrated CFAR (working title)

The paper question becomes:

> **How much does calibration aging in a low-cost SDR distort CFAR false-alarm control, and can a hardware-state-aware calibration envelope restore a certified/conservative false-alarm bound?**

The intended contribution would be a combination of:

- measurement characterization of receiver drift;
- a physically measurable calibration-age/state variable;
- a minimal conservative threshold/envelope rule;
- empirical and, where possible, finite-sample false-alarm validation;
- open reproducible implementation on inexpensive SDR hardware.

The mathematical pieces may individually be known. The contribution would have to lie in the experimentally validated RF system formulation and the exact guarantee claimed for that system.

---

## Next firewall / experiment gate

Do **not** build the final detector yet.

First run a small `P−1 hardware identifiability pilot` whose sole purpose is to determine whether the supposed phenomenon is measurable on our RTL-SDR setup.

### Minimum pilot

Use a 50-ohm terminated input if available; otherwise use the quietest controlled input configuration available and document the limitation. Disable AGC and fix tuner gain, sample rate, center frequency and bandwidth.

For repeated short captures during warm-up, record:

- elapsed time since receiver start;
- center frequency;
- configured gain;
- block mean power / median PSD floor;
- optionally host / dongle temperature if measurable;
- exact software/hardware metadata.

Repeat at several center frequencies and at least two fixed gain settings.

### Pilot question

Is the observed power-scale drift large and structured enough that using an early calibration distribution for later blocks causes a reproducible inflation/deflation of nominal `Pfa`?

### Kill criterion

If power-scale drift is negligible relative to sampling variability, or ordinary local CFAR completely absorbs it under controlled conditions, stop this direction.

### Survival criterion

Continue only if there is a repeatable calibration-age / hardware-state effect that materially changes the nominal false-alarm behavior and cannot be removed merely by standard local normalization.

---

## Current P−1 state after Firewall 03

- static replacement/mismatch theorem: **valid, not central novelty**;
- generic anytime-valid sequentialization: **subsumed**;
- stationary certified mismatch: **subsumed**;
- generic lagged bounded-drift theorem: **subsumed / routine**;
- generic set-membership drift tracking: **mature prior art**;
- **hardware-specific calibration-aging + CFAR characterization on low-cost SDR: SURVIVES as an engineering-novelty candidate, still unproven**.

Decision: **REFORMULATE → hardware identifiability pilot before any further theorem work.**

## Key references from this pass

- Alhashimi, A. et al. (2024). *BFAR: improving radar odometry estimation using a bounded false alarm rate detector*. Autonomous Robots 48, 29. DOI: 10.1007/s10514-024-10176-2.
- Mineiro, P. & Howard, S. R. (2023). *Time-uniform confidence bands for the CDF under nonstationarity*. NeurIPS 2023.
- Belforte, G., Bona, B., & Cerone, V. (1990). *Parameter estimation algorithms for a set-membership description of uncertainty*. Automatica 26(5), 887–898.
- Walter, E. & Piet-Lahanier, H. (1990). *Estimation of parameter bounds from bounded-error data: a survey*. Mathematics and Computers in Simulation 32, 449–468.
- Shams et al. (2026). *Adaptive frequency-domain CFAR for robust spectrum sensing under jamming and administrator-controlled counter-access*. Scientific Reports.
