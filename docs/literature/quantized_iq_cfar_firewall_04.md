# P−1 Quantized-IQ CFAR Firewall 04 — LIMEN-RF

Status: **REFORMULATE / broad candidate rejected**

Date: 2026-09-18

## Candidate screened

Candidate motivated by the RTL-SDR pilot:

> Exact false-alarm calibration for CFAR when complex Gaussian I/Q is uniformly quantized **before** square-law / energy formation, especially in a low-input regime near the ADC quantization floor.

The practical observation motivating the search was that the RTL-SDR Blog V4 open-input data at 28 dB gain were concentrated overwhelmingly on the central ADC codes, and even the maximum tested manual gain did not satisfy the predeclared dispersion gate.

This document is a novelty firewall, not a novelty claim.

## Prior art that materially threatens the broad candidate

### 1. Gandhi (1996) — quantization + CA/OS-CFAR already analyzed

P. P. Gandhi, “Data quantization effects in CFAR signal detection,” IEEE Transactions on Aerospace and Electronic Systems, vol. 32, no. 4, pp. 1277–1289, 1996.

Model:
- square-law detector first;
- exponential observations;
- uniform quantization after square-law;
- CA-CFAR and OS-CFAR.

Contribution:
- analytical false-alarm and detection probabilities for quantized CA- and OS-CFAR;
- quantization can destroy nominal false-alarm invariance unless resolution/dynamic range are adequate.

Threat:
- **HIGH** for any claim framed merely as “quantization changes CFAR/OS-CFAR false alarm.”

Important distinction:
- Gandhi quantizes the post-square-law observation, not I and Q separately before energy formation.

### 2. Lehtomäki et al. (2005) — pre-square I/Q quantization + energy detector + CA-CFAR

J. J. Lehtomäki, M. Juntti, H. Saarnisaari, and S. Koivu, “Threshold setting strategies for a quantized total power radiometer,” IEEE Signal Processing Letters, vol. 12, no. 11, pp. 796–799, 2005. DOI: 10.1109/LSP.2005.855521.

Model:
- zero-mean white Gaussian input;
- in-phase and quadrature channels quantized before the energy statistic;
- uniform quantization;
- total-power/energy detection;
- unknown-noise case studied using a CA-CFAR-style reference estimate.

Contribution:
- false-alarm analysis for the quantized radiometer;
- exact randomized decision rule for arbitrary target false-alarm probability when the pre-quantization noise variance is known;
- CA-CFAR-style thresholding when the noise level is estimated.

Threat:
- **VERY HIGH** for the proposed “pre-square quantized I/Q energy detector with false-alarm calibration” framing.
- This is the closest direct prior art found.

### 3. Lehtomäki doctoral work (2005)

J. Lehtomäki, “Analysis of energy based signal detection,” University of Oulu, 2005.

The thesis explicitly treats a receiver with separate quantization and sampling of I and Q, derives false-alarm behavior for a quantized radiometer, and analyzes a CA-CFAR strategy using quantized reference samples.

Threat:
- reinforces that pre-square quantization + energy detection + CFAR thresholding is an established line, not a new combination.

### 4. Jin et al. — one-bit LFMCW radar + OS-CFAR predetection

B. Jin, J. Zhu, Q. Wu, Y. Zhang, and Z. Xu, “One-bit LFMCW Radar: Spectrum Analysis and Target Detection,” 2019/2020.

Model:
- one-bit ADC applied directly to radar samples;
- FFT-domain target processing;
- OS-CFAR used for predetection;
- nonlinear DR-GAMP stage suppresses quantization-generated harmonics/false alarms.

Threat:
- **HIGH** for any broad “raw quantized radar samples + OS-CFAR” claim.
- Their OS-CFAR scaling is used as a predetection mechanism rather than an exact finite-sample discrete calibration theorem.

### 5. Xiao et al. (IEEE TSP 2024) — one-bit target detection with CFAR guarantee under colored background

Y.-H. Xiao, D. Ramírez, L. Huang, X.-P. Li, and H. C. So, “One-Bit Target Detection in Colocated MIMO Radar With Colored Background Noise,” IEEE Transactions on Signal Processing, vol. 72, pp. 5274–5290, 2024. DOI: 10.1109/TSP.2024.3484582.

Model:
- one-bit ADC;
- colored Gaussian background;
- unknown/noisy covariance aspects.

Contribution:
- Rao-test detector derived from quantized likelihood;
- explicitly studies CFAR behavior and covariance uncertainty;
- analytical detection characterization.

Threat:
- **VERY HIGH** to any broad statement that CFAR-aware theory for pre-square low-bit quantized radar is absent.

### 6. Hybrid quantized distributed radar (IEEE TAES 2023)

“Hybrid Quantized Signal Detection with a Bandwidth-Constrained Distributed Radar System,” IEEE Transactions on Aerospace and Electronic Systems, vol. 59, no. 6, pp. 7835–7850, 2023. DOI: 10.1109/TAES.2023.3296344.

Contribution reported by the publication record:
- theoretical detector distributions;
- CFAR property;
- optimization of quantization thresholds;
- numerical and experimental results;
- 2-bit quantization shown effective.

Threat:
- shows modern low-bit detection + explicit CFAR analysis is an active, established area.

## Firewall decision

### Broad claim: NO-GO

The following claim is not defensible as central novelty:

> “CFAR under quantized I/Q / low-bit ADC observations.”

Prior work already covers all of the major ingredients separately and, in some cases, together:
- quantization + CA/OS-CFAR;
- pre-square I/Q quantization + energy detection + false-alarm calibration;
- one-bit raw radar + OS-CFAR;
- one-bit likelihood-based detection + CFAR under colored noise.

### Narrow candidate that remains unverified

A much narrower statement was **not found verbatim** in the targeted search:

> Exact finite-sample OS-CFAR calibration for **multi-bit pre-square I/Q quantization**, with unknown pre-quantization noise scale, explicitly treating the discrete lattice/ties induced near the ADC floor, plus validation on commodity RTL-SDR measurements.

This is only a **provisional survivor**, not a GO.

Why it is still threatened:
1. Gandhi already gives OS-CFAR theory for quantized post-square-law data.
2. Lehtomäki already gives pre-square quantized-I/Q energy/CA-CFAR theory.
3. Combining the two may be viewed as a routine extension unless a genuinely nontrivial theorem appears.
4. Exact tie/randomization handling for discrete order statistics is standard probability machinery in isolation.
5. An RTL-SDR validation alone is not enough if the mathematics is only a direct substitution.

## Required next kill-test

Do **not** collect more 45-minute hardware traces yet.

Mathematical question:

> Under H0, let I and Q be Gaussian with unknown scale, pass them through a fixed uniform finite-bit quantizer, form block energies from squared quantized I/Q values, and construct an OS-CFAR statistic from a CUT and quantized reference cells. Does fixed ADC quantization destroy the usual scale-invariance strongly enough that no scale-free OS threshold exists? If yes, can an exact finite-sample calibration be obtained that is not a routine application of known discrete-order-statistic formulas?

Kill this candidate if:
- the exact null law/threshold is a direct, routine extension of Gandhi + Lehtomäki;
- conditioning/randomization trivially restores nominal Pfa with no RF-specific insight;
- the only contribution left is an RTL-SDR case study.

Continue only if at least one nontrivial result emerges, e.g.:
- a theorem characterizing when CFAR invariance is impossible under fixed pre-square quantization;
- a sharp worst-case Pfa envelope over unknown analog noise scale;
- an exact calibration with a meaningful structural result for OS order statistics/ties that is not already subsumed by known quantized-CFAR theory.

## Current P−1 status

- static worst-case OS mismatch theorem: useful lemma, not central novelty;
- anytime-valid sequentialization: subsumed by general theory;
- certified/lagged mismatch candidates: generic forms rejected;
- hardware-aging open-input architecture: failed sensitivity gate;
- broad quantized-IQ CFAR candidate: rejected;
- narrow exact multi-bit pre-square OS-CFAR candidate: **one final mathematical kill-test only**.

No further hardware acquisition is justified until this mathematical kill-test survives.
