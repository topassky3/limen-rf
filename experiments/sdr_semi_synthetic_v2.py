#!/usr/bin/env python3
"""RTL-SDR V2 weaker-SNR characterization for frozen LIMEN-RF.

This is a post-V1, pre-registered extension motivated only by V1 saturation
at -12 dB. The detector, score, receiver settings, reference contamination,
and comparator remain unchanged. Only the future injected-SNR grid is moved
downward and fresh captures are required.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import sdr_semi_synthetic_v1 as v1

V2_SNR_DB = (-24.0, -21.0, -18.0, -15.0, -12.0)
V2_SEED = 20260924
TARGET_CAPTURES = 30
DEFAULT_MIN_CAPTURES = 25


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise RuntimeError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    conditions = ["null"] + [f"snr_{x:g}dB" for x in V2_SNR_DB]
    out: list[dict[str, object]] = []
    for condition in conditions:
        group = [r for r in rows if r["condition"] == condition]
        for method in ("static", "baseline", "oracle"):
            crosses = [int(r[f"{method}_cross"]) for r in group]
            stops = [
                int(r[f"{method}_stop"])
                for r in group
                if r[f"{method}_stop"] != ""
            ]
            count = sum(crosses)
            lo, hi = v1.wilson(count, len(group))
            out.append({
                "condition": condition,
                "captures": len(group),
                "method": method,
                "cross_count": count,
                "cross_rate": count / len(group),
                "cross_ci_low": lo,
                "cross_ci_high": hi,
                "median_stop_detected": "" if not stops else float(np.median(stops)),
            })
    return out


def make_figures(summary: list[dict[str, object]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    snrs = list(V2_SNR_DB)

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for method, label in (
        ("static", "Static coupling"),
        ("baseline", "Precommitted band baseline"),
        ("oracle", "Oracle"),
    ):
        selected = [
            next(
                r for r in summary
                if r["condition"] == f"snr_{snr:g}dB" and r["method"] == method
            )
            for snr in snrs
        ]
        y = np.asarray([float(r["cross_rate"]) for r in selected])
        lo = np.asarray([float(r["cross_ci_low"]) for r in selected])
        hi = np.asarray([float(r["cross_ci_high"]) for r in selected])
        ax.errorbar(snrs, y, yerr=np.vstack((y - lo, hi - y)), marker="o", capsize=3, label=label)
    ax.set_xlabel("Offline injected tone SNR (dB)")
    ax.set_ylabel("Crossing probability by T=200")
    ax.set_ylim(-0.03, 1.03)
    ax.set_xticks(snrs)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "sdr_v2_crossing_vs_snr.pdf")
    fig.savefig(outdir / "sdr_v2_crossing_vs_snr.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for method, label in (
        ("static", "Static coupling"),
        ("baseline", "Precommitted band baseline"),
        ("oracle", "Oracle"),
    ):
        xs: list[float] = []
        ys: list[float] = []
        for snr in snrs:
            row = next(
                r for r in summary
                if r["condition"] == f"snr_{snr:g}dB" and r["method"] == method
            )
            if row["median_stop_detected"] != "":
                xs.append(snr)
                ys.append(float(row["median_stop_detected"]))
        if xs:
            ax.plot(xs, ys, marker="o", label=label)
    ax.set_xlabel("Offline injected tone SNR (dB)")
    ax.set_ylabel("Median stopping time among detected captures")
    ax.set_xticks(snrs)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "sdr_v2_delay_vs_snr.pdf")
    fig.savefig(outdir / "sdr_v2_delay_vs_snr.png", dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/sdr_publication_v2")
    parser.add_argument("--output-dir", default="results/sdr_publication_v2")
    parser.add_argument("--qc-only", action="store_true")
    parser.add_argument("--min-captures", type=int, default=DEFAULT_MIN_CAPTURES)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    files = sorted(input_dir.glob("capture_*.u8"))
    if not files:
        raise SystemExit(f"no capture_*.u8 files in {input_dir}")

    qc_rows = [v1.qc_capture(path) for path in files]
    print("=== SDR V2 QC ===")
    for row in qc_rows:
        print(
            f"{Path(str(row['file'])).name}: pass={row['pass']} "
            f"unique=({row['unique_i']},{row['unique_q']}) "
            f"std=({float(row['std_i_codes']):.2f},{float(row['std_q_codes']):.2f}) "
            f"clip={float(row['clip_fraction']):.4f} "
            f"power_span_db={float(row['power_p95_p5_db']):.2f} "
            f"lag1={float(row['score_lag1']):.3f} "
            f"reasons={row['reasons'] or '-'}"
        )

    output_dir = Path(args.output_dir)
    write_csv(output_dir / "qc.csv", qc_rows)
    passing = [Path(str(r["file"])) for r in qc_rows if bool(r["pass"])]

    if args.qc_only:
        print(f"QC_PASSING={len(passing)}/{len(files)}")
        print("SDR_V2_QC: COMPLETE")
        return 0

    if len(passing) < args.min_captures:
        raise SystemExit(
            f"only {len(passing)} captures passed QC; need at least {args.min_captures}. "
            "Acquire replacements at the same frozen receiver settings; do not change QC thresholds."
        )

    # Fresh V2 injection phases are made deterministic but distinct from V1.
    old_seed = v1.SEED
    v1.SEED = V2_SEED
    try:
        rows: list[dict[str, object]] = []
        for capture_index, path in enumerate(passing):
            for snr in (None,) + V2_SNR_DB:
                rows.append(v1.evaluate_one(path, capture_index, snr))
    finally:
        v1.SEED = old_seed

    summary = summarize(rows)
    write_csv(output_dir / "raw_results.csv", rows)
    write_csv(output_dir / "summary.csv", summary)
    make_figures(summary, output_dir / "figures")

    manifest = {
        "status": "post-V1 pre-registered weaker-SNR RTL-SDR characterization",
        "motivation": "V1 static coupling saturated at the weakest tested alternative (-12 dB)",
        "fresh_capture_requirement": True,
        "target_captures": TARGET_CAPTURES,
        "passing_captures": len(passing),
        "total_captures": len(files),
        "K": v1.K,
        "M": v1.M,
        "T": v1.T,
        "sample_rate_hz": v1.SAMPLE_RATE,
        "block_len": v1.BLOCK_LEN,
        "stride": v1.STRIDE,
        "skip_samples": v1.SKIP_SAMPLES,
        "reference_contaminated_blocks_zero_based": list(v1.REFERENCE_CONTAMINATED_BLOCKS),
        "reference_injection_snr_db": v1.REFERENCE_INJECTION_SNR_DB,
        "alternative_snr_db": list(V2_SNR_DB),
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
        "injection_seed": V2_SEED,
        "note": "Detector, score, QC, reference contamination, receiver settings and comparator are unchanged from V1. Only the future SNR grid is shifted downward. Injection remains post-ADC."
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("")
    print("=== SDR V2 SUMMARY ===")
    for row in summary:
        print(
            f"{row['condition']:>10s} {row['method']:>8s} "
            f"cross={float(row['cross_rate']):.3f} "
            f"[{float(row['cross_ci_low']):.3f},{float(row['cross_ci_high']):.3f}] "
            f"delay={row['median_stop_detected'] or 'NA'}"
        )
    print(f"results: {output_dir}")
    print("SDR_PUBLICATION_V2: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())