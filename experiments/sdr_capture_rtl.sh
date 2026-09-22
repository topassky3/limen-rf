#!/usr/bin/env bash
set -euo pipefail

# RTL-SDR semi-synthetic publication capture.
# Raw files stay under data/ and are intentionally gitignored.

OUT_DIR=${1:-data/sdr_publication_v1}
FREQ_HZ=${2:-100000000}
COUNT=${3:-1}
DURATION_S=${4:-10}
GAIN_DB=${5:-28.0}
SAMPLE_RATE=2048000
SLEEP_S=2

if ! command -v rtl_sdr >/dev/null 2>&1; then
  echo 'ERROR: rtl_sdr not found. Install the rtl-sdr command-line tools first.' >&2
  exit 2
fi

mkdir -p "$OUT_DIR"
SAMPLES=$((SAMPLE_RATE * DURATION_S))

echo "RTL-SDR publication capture"
echo "out_dir=$OUT_DIR freq_hz=$FREQ_HZ sample_rate=$SAMPLE_RATE gain_db=$GAIN_DB duration_s=$DURATION_S count=$COUNT"
echo "IMPORTANT: use an antenna; do not use the previous open-SMA setup."

for ((i=0; i<COUNT; i++)); do
  printf -v IDX '%03d' "$i"
  FILE="$OUT_DIR/capture_${IDX}.u8"
  echo "[$((i+1))/$COUNT] $FILE"
  rtl_sdr -f "$FREQ_HZ" -s "$SAMPLE_RATE" -g "$GAIN_DB" -n "$SAMPLES" "$FILE"
  if (( i + 1 < COUNT )); then
    sleep "$SLEEP_S"
  fi
done

cat > "$OUT_DIR/capture_manifest.txt" <<EOF
format=rtl_sdr_u8_interleaved_iq
frequency_hz=$FREQ_HZ
sample_rate_hz=$SAMPLE_RATE
gain_db=$GAIN_DB
duration_s=$DURATION_S
count=$COUNT
samples_per_capture=$SAMPLES
agc=off_manual_gain
EOF

echo "CAPTURE_COMPLETE: $OUT_DIR"