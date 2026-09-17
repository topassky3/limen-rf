# P−1 Hardware Pilot Analysis Plan v0.1 — LIMEN-RF

Status: **frozen before inspecting the IQ values from pilot_open_01**

Purpose: define the first-pass analysis for the 45-minute open-input hardware identifiability run without tuning thresholds after seeing the data.

## Run under analysis

- run: `pilot_open_01`
- input: open SMA input, antenna disconnected
- center frequency: 300 MHz
- sample rate: 2.048 MS/s
- manual gain: 28.0 dB
- capture duration: 2 s
- cadence: 60 s
- total captures: 46
- expected complex samples per capture: 4,096,000
- expected bytes per capture: 8,192,000

This run is exploratory because an open input is not a 50-ohm terminated null and can still couple ambient RF/EMI.

## Integrity gate

Before interpreting signal statistics:

1. require 46 metadata rows;
2. require all `size_ok=True`;
3. require all capture return codes to be zero;
4. require every IQ file to contain exactly 8,192,000 bytes;
5. retain the capture SHA-256 values already recorded by the acquisition script.

A failed integrity check blocks scientific interpretation until explained.

## Frozen block definition

Partition each 2-s capture into non-overlapping blocks of

\[
4096\ \text{complex samples}.
\]

Because each capture contains 4,096,000 samples, this gives exactly

\[
1000\ \text{blocks per capture}.
\]

This block size is frozen for the first-pass analysis.

## IQ scaling and power views

RTL-SDR files contain interleaved unsigned 8-bit I/Q samples. The nominal ADC center is 127.5.

Report both:

1. raw-centered power using `I-127.5`, `Q-127.5`;
2. a DC-removed power view after subtracting the per-capture mean I and Q.

The primary drift metric uses the DC-removed view so that center-bin / ADC DC offset changes are not silently interpreted as broadband power-scale drift. Raw-centered power and I/Q means remain diagnostics.

For each block, define mean power

\[
P_b=\frac{1}{4096}\sum_{n\in b}(I_n^2+Q_n^2).
\]

For each capture record mean block power, median block power, IQR, coefficient of variation, and clipping fraction.

## Baseline window

Freeze captures `0..4` (minutes 0 through 4) as the **early calibration window**.

The primary baseline location is the median of all DC-removed block powers from those five captures.

For capture `t`, define

\[
\Delta_t = 10\log_{10}\left(\frac{\operatorname{median}(P_{b,t})}{\operatorname{median}(P_{b,0:4})}\right).
\]

No absolute dBm claim is made.

## Stale-calibration false-alarm proxy

Freeze nominal per-block level

\[
\alpha_0=0.01.
\]

Construct a threshold from the pooled 5,000 baseline block powers using the empirical 99th percentile with the conservative `higher` quantile convention.

For every capture estimate

\[
\widehat P_{FA}^{stale}(t)=\frac{\#\{P_{b,t}>q_{0.99}^{baseline}\}}{1000}.
\]

Report a 95% Wilson binomial interval.

This is an exploratory stale **energy-threshold** proxy, not yet the final OS-CFAR detector.

## Local-normalization control

For each capture normalize its block powers by that capture's own median. Build a baseline 99th-percentile threshold from the normalized baseline blocks, then compute

\[
\widehat P_{FA}^{local}(t)
\]

on each later capture.

Interpretation:

- stale PFA changes while local-normalized PFA remains stable: consistent with a mostly scalar power-scale drift;
- both stale and local-normalized PFA change: distribution-shape change / RF contamination / non-scalar hardware effect remains plausible;
- neither changes materially: weak evidence for a calibration-aging problem under this condition.

This local normalization is only a sanity baseline, not a publication-grade CFAR comparison.

## Confound checks

Record and inspect:

- ADC clipping fraction;
- I and Q DC means;
- within-capture block-power spread;
- capture/log integrity;
- host thermal-zone values as **host covariates only**, never as dongle temperature;
- abrupt single-capture excursions that could indicate environmental RF pickup.

## Decision after run 1

Run 1 alone cannot establish repeatability.

- If no structured drift or stale-threshold distortion is visible, the candidate is weakened and may be killed without a second identical run if the effect is clearly negligible.
- If a structured effect is visible, perform a second independent cold-start run under the exact same settings before calling the phenomenon repeatable.
- A second run with an open input still does not replace a later 50-ohm terminated confirmation if this direction survives.

No publication-novelty claim follows from this analysis.