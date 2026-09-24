#!/usr/bin/env python3
"""Finalize an already-computed SDR V2 run without rerunning the detector."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sdr_semi_synthetic_v1 as v1
import sdr_semi_synthetic_v2 as v2


def read_csv(path: Path) -> list[dict[str, object]]:
    with path.open(newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results/sdr_publication_v2")
    args = parser.parse_args()

    outdir = Path(args.output_dir)
    summary_path = outdir / "summary.csv"
    raw_path = outdir / "raw_results.csv"
    qc_path = outdir / "qc.csv"
    for path in (summary_path, raw_path, qc_path):
        if not path.exists():
            raise SystemExit(f"missing existing V2 artifact: {path}")

    summary = read_csv(summary_path)
    raw = read_csv(raw_path)
    qc = read_csv(qc_path)

    passing = sum(str(r.get("pass", "")).lower() in {"true", "1"} for r in qc)
    v2.make_figures(summary, outdir / "figures")

    manifest = {
        "status": "post-V1 pre-registered weaker-SNR RTL-SDR characterization",
        "finalization_mode": "existing detector outputs; detector was not rerun",
        "motivation": "V1 static coupling saturated at the weakest tested alternative (-12 dB)",
        "fresh_capture_requirement": True,
        "target_captures": v2.TARGET_CAPTURES,
        "passing_captures": passing,
        "total_captures": len(qc),
        "detector_result_rows": len(raw),
        "K": v1.K,
        "M": v1.M,
        "T": v1.T,
        "sample_rate_hz": v1.SAMPLE_RATE,
        "block_len": v1.BLOCK_LEN,
        "stride": v1.STRIDE,
        "skip_samples": v1.SKIP_SAMPLES,
        "reference_contaminated_blocks_zero_based": list(v1.REFERENCE_CONTAMINATED_BLOCKS),
        "reference_injection_snr_db": v1.REFERENCE_INJECTION_SNR_DB,
        "alternative_snr_db": list(v2.V2_SNR_DB),
        "tone_offset_hz": v1.TONE_OFFSET_HZ,
        "baseline_key": list(v1.BASELINE_KEY),
        "receiver_settings": {
            "center_frequency_hz": 100_000_000,
            "sample_rate_hz": 2_048_000,
            "manual_gain_db": 28.0,
        },
        "qc": {
            "min_unique_codes": v1.MIN_UNIQUE_CODES,
            "min_adc_std_codes": v1.MIN_ADC_STD_CODES,
            "max_clip_fraction": v1.MAX_CLIP_FRACTION,
            "max_power_p95_p5_db": v1.MAX_POWER_P95_P5_DB,
        },
        "injection_seed": v2.V2_SEED,
        "note": "Figures and manifest finalized from already-written V2 CSV outputs after a plotting-only floating-point error. No detector result was recomputed."
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("=== SDR V2 SUMMARY (existing outputs) ===")
    for row in summary:
        print(
            f"{str(row['condition']):>10s} {str(row['method']):>8s} "
            f"cross={float(row['cross_rate']):.3f} "
            f"[{float(row['cross_ci_low']):.3f},{float(row['cross_ci_high']):.3f}] "
            f"delay={row['median_stop_detected'] or 'NA'}"
        )
    print(f"figures: {outdir / 'figures'}")
    print(f"manifest: {outdir / 'manifest.json'}")
    print("SDR_PUBLICATION_V2_FINALIZE: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())