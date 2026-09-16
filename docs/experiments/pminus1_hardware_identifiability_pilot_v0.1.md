# P−1 Hardware Identifiability Pilot v0.1 — LIMEN-RF

Status: **experimental kill-test design**

Purpose: determine whether low-cost SDR receiver state / calibration age produces a repeatable power-scale drift large enough to alter nominal CFAR false-alarm behavior. This pilot is not intended to prove the final paper claim. It decides whether the surviving engineering-novelty candidate is physically measurable before more theory or implementation effort.

## Scientific question

Does a stale calibration from an RTL-SDR-class receiver cause a reproducible change in the null distribution seen by a nominal CFAR detector as the hardware warms or its state evolves?

The key observable is not frequency PPM drift. It is **power-scale / noise-floor drift** relevant to energy detection and CFAR thresholds.

## Hypotheses

### H-kill

After fixing receiver configuration, the power-scale change over warm-up / elapsed time is negligible relative to block-to-block sampling variability, or ordinary local normalization completely absorbs it. In that case this direction is killed.

### H-survive

There is a repeatable calibration-age or hardware-state effect that materially changes the null distribution and therefore the empirical false-alarm rate when an early calibration is reused later.

No novelty claim is made if H-survive is observed. It only licenses a deeper experiment and another prior-art check.

---

## Measurement architecture

Preferred input:

1. **50-ohm termination** connected directly to the SDR input.
2. If unavailable, use the quietest controlled input configuration possible and document it explicitly. An antenna/open input is a fallback only; external RF then becomes a major confounder.

Receiver controls:

- AGC: OFF.
- tuner gain: fixed for a run;
- center frequency: fixed within each run;
- sample rate: fixed;
- bandwidth: fixed/recorded if exposed by the driver;
- direct sampling / bias-tee / offset tuning: fixed and recorded;
- no manual reconfiguration during a run.

Do not interpret host CPU temperature as dongle temperature. If only host temperature is available, record it as a proxy covariate with that limitation.

---

## Preflight — do this before the first pilot run

On the Orange Pi / capture host, record the outputs of:

```bash
uname -a
python3 --version
rtl_test -t
rtl_eeprom
rtl_sdr -h 2>&1 | head -n 40
rtl_power -h 2>&1 | head -n 60
lsusb
```

Also check available Linux thermal sensors:

```bash
for z in /sys/class/thermal/thermal_zone*; do
  [ -r "$z/type" ] && [ -r "$z/temp" ] && \
  printf '%s %s %s\n' "$z" "$(cat "$z/type")" "$(cat "$z/temp")"
done
```

Save the exact dongle model / tuner reported by `rtl_test -t`, supported gain range if shown, USB identification, kernel and rtl-sdr tool version if available.

### Preflight PASS

- SDR is detected reliably;
- a fixed manual gain can be selected;
- IQ capture works without dropped-sample errors for at least a short test;
- exact hardware/software metadata can be recorded.

If preflight fails, fix infrastructure before collecting scientific data.

---

## Pilot v0.1 design

### Stage A — single-condition warm-up trace

Use one center frequency, one fixed gain and one sample rate.

Initial suggested values (may be adjusted after tuner preflight):

- sample rate: `2.4e6` samples/s;
- IQ capture duration per observation: `2 s`;
- cadence: one capture every `60 s`;
- total elapsed time: `45 min`;
- repetitions: at least `2` independent cold-start runs on different sessions;
- gain: one mid-range fixed tuner gain, chosen from the actual tuner-supported values;
- input: 50-ohm termination preferred.

A true cold-start run should begin after the SDR has been unpowered long enough to return near ambient conditions. Record the unpowered interval rather than silently assuming a cold start.

### Stage B — limited state sweep, only if Stage A shows a signal

Repeat a shorter trace at:

- three center frequencies spanning the useful tuner range;
- two fixed manual gain settings (moderate and higher, both within linear/non-overload operation);
- at least two repetitions per condition if time permits.

Do not start Stage B if Stage A does not show a plausible effect.

---

## Data products

For every capture, preserve or compute:

- `run_id`;
- `capture_id`;
- UTC timestamp;
- elapsed seconds since SDR power-on;
- elapsed seconds since reference calibration;
- center frequency Hz;
- sample rate Hz;
- tuner gain dB / driver gain code;
- bandwidth Hz if known;
- AGC state;
- input condition (`50ohm`, `open`, `antenna`, other);
- number of complex samples;
- mean IQ power;
- median IQ-block power;
- median PSD floor over a predefined interior band;
- robust PSD spread (IQR or MAD);
- clipping / saturation indicator;
- dropped-sample / capture error flag;
- host temperature sensors if available, explicitly labelled as host sensors;
- git commit;
- capture command / software version.

Raw IQ should not automatically be committed to GitHub. Store large IQ files outside git or in an artifact/data location and commit metadata + hashes + analysis code.

For each raw capture compute a SHA-256 digest.

---

## Analysis definitions frozen before collection

### Power metric

For complex IQ samples `x[n]`, define

\[
P = \frac{1}{N}\sum_{n=1}^N |x[n]|^2.
\]

Also report

\[
P_{dB}=10\log_{10} P.
\]

Use identical scaling for every capture. Absolute dBm calibration is **not required** for this identifiability pilot; relative receiver-scale stability is the target.

### Calibration-age drift

For a baseline window from the early calibration period, define a baseline location `mu0` on the chosen log-power metric. For later capture `t`, report

\[
\Delta_t = P_{dB,t} - \mu_0.
\]

Report both the temporal trajectory and within-capture / between-block variability so that a visually small drift is not mistaken for a statistically meaningful effect.

### Stale-calibration false-alarm test

Freeze a threshold from the baseline calibration period to obtain a nominal per-block false-alarm target `alpha0` under the baseline null distribution.

For later epochs, apply the **unchanged** baseline threshold and estimate

\[
\widehat P_{FA}(t).
\]

Use binomial confidence intervals for each epoch/window. Do not call an observed deviation meaningful from a single threshold crossing or a small number of blocks.

At least two detector views should be compared:

1. **stale/global calibration** — baseline threshold retained;
2. **ordinary local normalization / local CFAR baseline** — threshold recomputed from contemporaneous reference data using a standard method.

The candidate survives only if stale calibration produces a repeatable material distortion and the phenomenon is not completely removed by the ordinary local baseline relevant to the intended application.

---

## Primary pilot endpoints

The pilot has two primary outputs:

1. magnitude and repeatability of relative power-scale drift versus elapsed time / hardware state;
2. change in empirical false-alarm behavior caused by applying an early calibration to later null data.

Secondary outputs (frequency dependence, gain dependence, temperature association) are exploratory in v0.1.

---

## Decision rule

### FAIL / kill this direction

Classify the hardware-aging candidate `NO-GO` if, under controlled input and fixed manual settings, either:

- the drift is not reproducible across cold-start repetitions and is comparable to ordinary sampling variability; or
- stale calibration does not materially alter empirical false-alarm behavior; or
- a standard contemporaneous local CFAR/reference normalization absorbs the effect so completely that no distinct calibration-age problem remains for the intended detector.

Do not rescue the candidate by adding more model complexity after a clean FAIL without a new physical observation.

### PASS / continue

Classify the identifiability pilot `PASS` only if:

- a structured calibration-age / hardware-state effect is visible in at least two independent runs;
- the effect is large relative to null sampling variability;
- an early/stale calibration produces a reproducible false-alarm distortion;
- the effect survives basic sanity checks for clipping, dropped samples, external RF contamination and configuration changes;
- the phenomenon is not trivially eliminated by the standard local-normalization baseline relevant to the use case.

PASS does **not** establish publication novelty. It opens P0 hardware characterization and a tighter literature search against the exact measured phenomenon.

---

## Confounders to actively rule out

- AGC accidentally enabled;
- tuner gain quantization / automatic gain changes;
- ADC clipping or front-end overload;
- external transmitters when input is not terminated;
- DC spike / center-bin artifacts;
- USB power / host-power changes;
- sample loss or driver resets;
- different software scaling between captures;
- frequency retuning transients;
- hidden bandwidth or direct-sampling changes;
- comparing host temperature with actual dongle temperature as if they were the same quantity.

---

## Reproducibility layout proposed

```text
data/
  README.md                 # no large IQ committed by default
experiments/
  pminus1_hardware_capture.py   # capture orchestration after preflight
  pminus1_hardware_analyze.py   # frozen analysis
configs/
  pminus1_hardware_pilot.yaml
results/
  pminus1_hardware_pilot/
    metadata.csv
    summary.json
    figures/
```

The scripts/config should only be implemented after the hardware preflight identifies the actual tuner, supported gain values and available capture commands.

---

## Immediate next action

Do **not** start the 45-minute collection yet.

Run the preflight commands and save their output. From that output we will freeze:

- exact tuner/gain values;
- one safe center frequency for Stage A;
- capture command;
- IQ datatype/scaling;
- whether host thermal metadata are available.

Only then create the capture script/config so the pilot is reproducible rather than improvised.
