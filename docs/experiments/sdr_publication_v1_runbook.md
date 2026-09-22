# RTL-SDR semi-synthetic validation V1

Status: **pre-outcome protocol**. The detector is frozen.

Purpose: add engineering evidence using real RTL-SDR IQ while keeping known ground truth through offline baseband injection.

## Frozen statistical settings

- K=32, m=2, T=200, alpha=0.05.
- Score: log mean block power.
- Block length: 16,384 complex samples.
- Stride: 32,768 complex samples.
- First 1 second of each capture is skipped.
- Physical contaminated reference blocks: 7 and 24 (zero-based).
- Reference contamination: complex tone at +6 dB relative to each block RMS.
- Future alternatives: tone SNR in {-12,-6,-3,0} dB, injected from t=1.
- Tone offset: 271 kHz from complex baseband center.
- Comparator: precommitted frozen `band_mix`, delta=0.045; no hardware-grid tuning.
- Oracle: true contaminated sorted positions, for diagnostic upper reference.

## Important boundary

The synthetic tone is added **after ADC**. Real receiver noise, quantization, oscillator/front-end background, and environmental RF remain in the capture, but signal-induced analog front-end compression/nonlinearity is not simulated.

## Step 0 — sensor node and antenna

Use the RTL-SDR V4 with an antenna. Do not repeat the earlier open-SMA capture. The SDR may be physically attached to a remote sensor node (for example an Orange Pi); the capture helper only requires `rtl_sdr` on that node. Analysis remains on the development machine.

Before capture, verify on the sensor node:

    rtl_test -t

## Step 1 — one-capture smoke/QC

First pull the branch on the development machine. Then capture one 10-second file on the machine that physically hosts the SDR. The initial suggested center frequency is 100 MHz; frequency/gain may be changed only if this pre-outcome QC fails.

Local-SDR path:

    cd ~/projects/limen-rf
    git pull --rebase origin research/p-1-prior-art
    bash experiments/sdr_capture_rtl.sh data/sdr_publication_v1 100000000 1 10 28.0

Remote-SDR path: execute the same helper over SSH, copy `capture_000.u8` back into `data/sdr_publication_v1/`, and perform all QC/analysis locally. This preserves one versioned capture script without requiring the full repository on the sensor node.

Run QC only:

    uv run python experiments/sdr_semi_synthetic_v1.py \
      --input-dir data/sdr_publication_v1 \
      --output-dir results/sdr_publication_v1_smoke \
      --qc-only \
      --min-captures 1

QC is decided before detector outcomes. A capture fails if it has too few ADC codes, ADC standard deviation near the previous quantization floor, excessive clipping, or gross block-power nonstationarity.

If the capture fails QC, do not run the detector. Change center frequency or manual gain based only on the QC reason, delete the failed pilot directory, and repeat Step 1. Once one setting passes, freeze that frequency and gain for the final captures.

## Step 2 — final captures

After the smoke capture passes, start a fresh directory and collect 20 independent 10-second capture sessions at the frozen frequency/gain on the SDR sensor node:

    rm -rf data/sdr_publication_v1_final
    bash experiments/sdr_capture_rtl.sh data/sdr_publication_v1_final <FREQ_HZ> 20 10 <GAIN_DB>

Raw IQ is ignored by Git and must not be committed.

## Step 3 — final semi-synthetic analysis

    uv run python experiments/sdr_semi_synthetic_v1.py \
      --input-dir data/sdr_publication_v1_final \
      --output-dir results/sdr_publication_v1 \
      --min-captures 10

Expected terminal marker:

    SDR_PUBLICATION_V1: COMPLETE

Outputs include QC, per-capture results, summary crossing rates, a reproducibility manifest, and a crossing-vs-SNR figure.

## Decision discipline

- Do not alter the detector, bettor portfolio, thresholds, injected SNR grid, reference contamination indices, or QC thresholds after detector outcomes are viewed.
- If fewer than 10 captures pass QC, acquire more captures under the same frozen receiver settings.
- Do not interpret the smoke capture scientifically.
- Hardware results are external validation, not a proof of theorem-level iid assumptions.