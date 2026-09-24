# RTL-SDR semi-synthetic validation V2 — weaker-SNR characterization

Date: 2026-09-24

Status: **pre-outcome protocol, created after V1 showed saturation at -12 dB**.

V2 does not replace or modify V1. V1 remains the confirmatory external-validation result. V2 is a fresh characterization experiment designed to resolve the lower-SNR transition.

## What is unchanged from V1

- detector and bettor portfolio
- K=32, m=2, T=200
- score = log mean block power
- block_len=16384, stride=32768, first 1 s skipped
- contaminated reference identities = blocks 7 and 24 (zero-based)
- reference contamination = +6 dB post-ADC tone
- tone offset = 271 kHz
- precommitted comparator = band_mix, delta=0.045
- QC thresholds
- receiver settings = 100 MHz, 2.048 MS/s, manual gain 28.0 dB
- RTL-SDR Blog V4 physically connected to the Orange Pi sensor node

## What changes, and why

V1 already gave 20/20 static detections at -12 dB, so it did not resolve the method's transition region. V2 changes only the future injected-SNR grid to:

    {-24, -21, -18, -15, -12} dB

The -12 dB point is retained as an anchor to V1. This grid is frozen before any V2 detector outcome is viewed.

## Fresh-data requirement

Do not reuse the 20 V1 captures. Acquire 30 fresh 10-second captures on the Orange Pi at the already-frozen receiver settings.

From WSL on the development PC:

    cd ~/projects/limen-rf
    git pull --rebase origin research/p-1-prior-art

    ssh -i ~/.ssh/orangepi_ed25519 \
      felipe@192.168.0.103 \
      'rm -rf ~/limen-rf-sdr-v2 && mkdir -p ~/limen-rf-sdr-v2 && bash -s -- ~/limen-rf-sdr-v2 100000000 30 10 28.0' \
      < experiments/sdr_capture_rtl.sh

Copy the fresh captures back:

    rm -rf data/sdr_publication_v2
    mkdir -p data/sdr_publication_v2

    scp -i ~/.ssh/orangepi_ed25519 \
      'felipe@192.168.0.103:~/limen-rf-sdr-v2/capture_*.u8' \
      data/sdr_publication_v2/

    scp -i ~/.ssh/orangepi_ed25519 \
      felipe@192.168.0.103:~/limen-rf-sdr-v2/capture_manifest.txt \
      data/sdr_publication_v2/

## Gate 1 — QC only

Before any V2 detector result:

    uv run python experiments/sdr_semi_synthetic_v2.py \
      --input-dir data/sdr_publication_v2 \
      --output-dir results/sdr_publication_v2_qc \
      --qc-only \
      --min-captures 25

Target: 30 fresh captures. At least 25 must pass the unchanged V1 QC gates. If fewer than 25 pass, acquire replacement captures at the same frozen receiver settings. Do not change the QC thresholds.

## Gate 2 — first and only V2 detector run

After Gate 1 closes:

    uv run python experiments/sdr_semi_synthetic_v2.py \
      --input-dir data/sdr_publication_v2 \
      --output-dir results/sdr_publication_v2 \
      --min-captures 25

Expected terminal marker:

    SDR_PUBLICATION_V2: COMPLETE

Outputs:

- `qc.csv`
- `raw_results.csv`
- `summary.csv`
- `manifest.json`
- `figures/sdr_v2_crossing_vs_snr.{pdf,png}`
- `figures/sdr_v2_delay_vs_snr.{pdf,png}`

## Interpretation discipline

- V2 is a post-V1 characterization experiment, not a replacement confirmatory test.
- Do not change the detector, baseline, SNR grid, reference injection, block geometry, QC thresholds, frequency, sample rate, or gain after V2 detector outcomes are viewed.
- Null behavior remains descriptive because real score sequences exhibit serial dependence and the iid theorem is not asserted for hardware data.
- Injection is post-ADC; the experiment does not model signal-induced analog front-end compression or nonlinearity.