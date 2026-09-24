# RTL-SDR semi-synthetic validation V2 — frozen result

Date: 2026-09-24

Status: **FINALIZED FROM THE FIRST AND ONLY V2 DETECTOR RUN — NO DETECTOR RERUN**

## Purpose

V2 is a post-V1, preregistered characterization experiment. It was created only because RTL-SDR V1 saturated at the weakest tested alternative (-12 dB).

V2 does not replace V1 and is not a new tuning stage. It preserves the frozen detector, betting portfolio, comparator, block geometry, reference contamination, receiver configuration, and QC rules from V1. Only the future injected-SNR grid was shifted downward before any V2 detector outcome was viewed.

## Frozen protocol

Receiver and acquisition:

- RTL-SDR Blog V4 on Orange Pi sensor node
- center frequency: 100 MHz
- sample rate: 2.048 MS/s
- manual gain: 28.0 dB
- 30 fresh 10 s captures
- antenna connected
- pre-outcome QC: **30/30 PASS**
- zero clipping in all captures

Frozen statistical settings:

- K=32
- m=2
- T=200
- score = log mean block power
- block_len=16384
- stride=32768
- first 1 s skipped
- contaminated physical reference identities: blocks 7 and 24 (zero-based)
- reference tone contamination: +6 dB post-ADC
- tone offset: 271 kHz
- precommitted comparator: band_mix, delta=0.045
- V2 injected-SNR grid: {-24,-21,-18,-15,-12} dB
- deterministic V2 injection seed: 20260924

The physical score streams show non-negligible and variable serial dependence; observed lag-1 correlations were approximately 0.035--0.906. Therefore hardware-null behavior is descriptive only and the iid theorem is not asserted for these captures.

## Detector results

| condition | static cross | static delay | baseline cross | baseline delay | oracle cross | oracle delay |
|---|---:|---:|---:|---:|---:|---:|
| null | 0.067 [0.018,0.213] | 72.0 | 0.000 [0.000,0.114] | NA | 0.133 [0.053,0.297] | 16.5 |
| -24 dB | 0.067 [0.018,0.213] | 11.0 | 0.000 [0.000,0.114] | NA | 0.133 [0.053,0.297] | 43.5 |
| -21 dB | 0.100 [0.035,0.256] | 13.0 | 0.000 [0.000,0.114] | NA | 0.167 [0.073,0.336] | 8.0 |
| -18 dB | 0.467 [0.302,0.639] | 8.5 | 0.000 [0.000,0.114] | NA | 0.600 [0.423,0.754] | 6.0 |
| -15 dB | 0.733 [0.556,0.858] | 8.0 | 0.400 [0.246,0.577] | 58.5 | 0.800 [0.627,0.905] | 5.0 |
| -12 dB | 1.000 [0.886,1.000] | 4.0 | 0.867 [0.703,0.947] | 30.0 | 1.000 [0.886,1.000] | 3.0 |

Delays are median stopping times among captures that crossed by T=200 and must be interpreted together with crossing probabilities.

Approximate crossing counts out of 30:

- null: static 2/30, baseline 0/30, oracle 4/30
- -24 dB: static 2/30, baseline 0/30, oracle 4/30
- -21 dB: static 3/30, baseline 0/30, oracle 5/30
- -18 dB: static 14/30, baseline 0/30, oracle 18/30
- -15 dB: static 22/30, baseline 12/30, oracle 24/30
- -12 dB: static 30/30, baseline 26/30, oracle 30/30

## Interpretation

### 1. V2 resolves the transition that V1 could not resolve

V1 was already saturated for static coupling at -12 dB. V2 moves into the lower-SNR regime and exposes a clear transition.

The most informative points are -18 dB and -15 dB:

- At -18 dB, static coupling crosses on 14/30 captures while the precommitted baseline crosses on 0/30 and the oracle on 18/30.
- At -15 dB, static coupling crosses on 22/30 captures, the baseline on 12/30, and the oracle on 24/30.
- Among detected -15 dB captures, median stopping time is 8 for static coupling versus 58.5 for the baseline and 5 for the oracle.

These results provide a non-saturated engineering characterization of the finite-reference sensitivity advantage.

### 2. The -12 dB anchor is qualitatively reproducible across independent capture batches

V1 and V2 used fresh, independent capture batches at the same frozen receiver settings.

At -12 dB:

- V1 static: cross 1.00, median stop 4.5
- V2 static: cross 1.00, median stop 4.0
- V1 baseline: cross 0.75, median stop 29
- V2 baseline: cross 0.867, median stop 30
- V1 oracle: cross 1.00, median stop 3.5
- V2 oracle: cross 1.00, median stop 3.0

The close stopping-time scale at the shared anchor is useful evidence that the qualitative behavior is not tied to one capture batch.

### 3. Null behavior is not a hardware type-I validation

Under the V2 null condition, static crosses on 2/30 captures and oracle on 4/30. The corresponding Wilson intervals are wide. More importantly, the real RTL-SDR score streams exhibit serial dependence that is outside the iid null theorem.

Therefore V2 must not be described as proving hardware false-alarm control at alpha=0.05.

The defensible claim is narrower:

> On real RTL-SDR background IQ with controlled post-ADC tone injection, the frozen static-coupling detector exhibits a clear lower-SNR transition and retains a substantial sensitivity/delay advantage over the precommitted confidence-band comparator in the moderate-SNR region.

### 4. Post-ADC scope

Signal and contamination injection are performed after ADC. The experiment therefore retains real receiver/background IQ, quantization and environmental structure, but does not model signal-induced analog front-end compression or other nonlinear response to over-the-air injected signals.

## Plotting-only failure and finalization

The first and only V2 detector execution successfully wrote:

- `qc.csv`
- `raw_results.csv`
- `summary.csv`

before figure generation.

The run then stopped in Matplotlib because a Wilson interval at a boundary produced a tiny negative error-bar width from floating-point subtraction:

`ValueError: 'yerr' must not contain negative values`

This was a post-processing-only numerical issue. No detector result or statistical parameter was invalidated.

The plotting function was patched to clamp error-bar widths to nonnegative values, and `experiments/sdr_v2_finalize.py` was added. The finalizer reads the already-existing CSV outputs and creates the figures and manifest without executing the detector again.

The successful finalizer marker was:

`SDR_PUBLICATION_V2_FINALIZE: COMPLETE`

Therefore the V2 detector was **not rerun**.

## Gate decision

**SDR VALIDATION V2: PASS FOR WEAKER-SNR EXTERNAL ENGINEERING CHARACTERIZATION; NOT A HARDWARE TYPE-I VALIDATION.**

V1 remains the preregistered first external-validation experiment. V2 is a separate, preregistered post-V1 characterization that resolves the lower-SNR transition.

## Frozen local artifacts

The completed local result directory is:

`results/sdr_publication_v2/`

Expected frozen artifacts:

- `qc.csv`
- `raw_results.csv`
- `summary.csv`
- `manifest.json`
- `figures/sdr_v2_crossing_vs_snr.pdf`
- `figures/sdr_v2_crossing_vs_snr.png`
- `figures/sdr_v2_delay_vs_snr.pdf`
- `figures/sdr_v2_delay_vs_snr.png`

These local outputs should be versioned verbatim before submission. They must not be regenerated merely to change detector outcomes or improve the curves.
