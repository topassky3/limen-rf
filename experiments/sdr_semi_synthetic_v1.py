#!/usr/bin/env python3
"""Semi-synthetic RTL-SDR validation for frozen LIMEN-RF.

Real unsigned-8-bit RTL-SDR IQ supplies the receiver/background process.
Signals are injected offline after ADC so ground truth is controlled.
The detector and baseline configuration remain frozen.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import math
import random
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pminus1_baseline_strength_audit_killtest13 as kt13

SAMPLE_RATE = 2_048_000
K = 32
M = 2
T = 200
BLOCK_LEN = 16_384
STRIDE = 32_768
SKIP_SAMPLES = SAMPLE_RATE
REFERENCE_CONTAMINATED_BLOCKS = (7, 24)  # zero-based physical reference identities
REFERENCE_INJECTION_SNR_DB = 6.0
ALT_SNR_DB = (-12.0, -6.0, -3.0, 0.0)
TONE_OFFSET_HZ = 271_000.0
SEED = 20260922
ALPHA = 0.05

# Pre-outcome receiver QC. These gates are evaluated before any detector call.
MIN_UNIQUE_CODES = 16
MIN_ADC_STD_CODES = 2.0
MAX_CLIP_FRACTION = 0.01
MAX_POWER_P95_P5_DB = 8.0

# Precommitted hardware comparator: primary simulation's fixed band mixture.
BASELINE_KEY = ("band_mix", 0.045, None)


def wilson(successes: int, n: int) -> tuple[float, float]:
    z = 1.959963984540054
    if n <= 0:
        return (float("nan"), float("nan"))
    p = successes / n
    den = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / den
    half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / den
    return max(0.0, center - half), min(1.0, center + half)


def read_u8_iq(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    raw = np.fromfile(path, dtype=np.uint8)
    if raw.size % 2:
        raw = raw[:-1]
    i_codes = raw[0::2]
    q_codes = raw[1::2]
    i = (i_codes.astype(np.float32) - 127.5) / 128.0
    q = (q_codes.astype(np.float32) - 127.5) / 128.0
    return i + 1j * q, i_codes, q_codes


def base_blocks(iq: np.ndarray) -> np.ndarray:
    needed = SKIP_SAMPLES + (K + T - 1) * STRIDE + BLOCK_LEN
    if iq.size < needed:
        raise ValueError(f"capture too short: need {needed} complex samples, got {iq.size}")
    starts = SKIP_SAMPLES + STRIDE * np.arange(K + T)
    return np.stack([iq[s : s + BLOCK_LEN] for s in starts], axis=0)


def score(block: np.ndarray) -> float:
    power = float(np.mean(np.abs(block) ** 2))
    return math.log(max(power, 1e-30))


def qc_capture(path: Path) -> dict[str, object]:
    iq, i_codes, q_codes = read_u8_iq(path)
    blocks = base_blocks(iq)
    scores = np.asarray([score(b) for b in blocks], dtype=float)
    db = 10.0 / math.log(10.0) * scores

    unique_i = int(np.unique(i_codes).size)
    unique_q = int(np.unique(q_codes).size)
    std_i = float(np.std(i_codes.astype(float)))
    std_q = float(np.std(q_codes.astype(float)))
    clip = float(np.mean((i_codes <= 1) | (i_codes >= 254) | (q_codes <= 1) | (q_codes >= 254)))
    span = float(np.percentile(db, 95.0) - np.percentile(db, 5.0))
    lag1 = float(np.corrcoef(scores[:-1], scores[1:])[0, 1]) if scores.size > 2 else float("nan")

    reasons: list[str] = []
    if unique_i < MIN_UNIQUE_CODES or unique_q < MIN_UNIQUE_CODES:
        reasons.append("too_few_adc_codes")
    if std_i < MIN_ADC_STD_CODES or std_q < MIN_ADC_STD_CODES:
        reasons.append("adc_std_near_floor")
    if clip > MAX_CLIP_FRACTION:
        reasons.append("clipping")
    if span > MAX_POWER_P95_P5_DB:
        reasons.append("gross_power_nonstationarity")

    return {
        "file": str(path),
        "pass": not reasons,
        "reasons": ";".join(reasons),
        "complex_samples": int(iq.size),
        "unique_i": unique_i,
        "unique_q": unique_q,
        "std_i_codes": std_i,
        "std_q_codes": std_q,
        "clip_fraction": clip,
        "power_p95_p5_db": span,
        "score_lag1": lag1,
    }


def inject_tone(block: np.ndarray, snr_db: float, phase: float) -> np.ndarray:
    p = float(np.mean(np.abs(block) ** 2))
    tone_power = p * (10.0 ** (snr_db / 10.0))
    amp = math.sqrt(tone_power)
    n = np.arange(block.size, dtype=float)
    tone = amp * np.exp(1j * (2.0 * math.pi * TONE_OFFSET_HZ * n / SAMPLE_RATE + phase))
    return block + tone.astype(np.complex64)


def detector_inputs(blocks: np.ndarray, alt_snr_db: float | None, capture_index: int):
    ref = blocks[:K].copy()
    stream = blocks[K : K + T].copy()
    rng = random.Random(SEED + 100_000 * capture_index + (0 if alt_snr_db is None else int((alt_snr_db + 30) * 100)))

    contaminated = set(REFERENCE_CONTAMINATED_BLOCKS)
    for idx in contaminated:
        ref[idx] = inject_tone(ref[idx], REFERENCE_INJECTION_SNR_DB, rng.random() * 2.0 * math.pi)

    if alt_snr_db is not None:
        for t in range(T):
            stream[t] = inject_tone(stream[t], alt_snr_db, rng.random() * 2.0 * math.pi)

    ref_scores = np.asarray([score(b) for b in ref], dtype=float)
    stream_scores = np.asarray([score(b) for b in stream], dtype=float)

    tagged = sorted((float(v), i in contaminated) for i, v in enumerate(ref_scores))
    true_positions = tuple(i + 1 for i, (_, is_bad) in enumerate(tagged) if is_bad)
    if len(true_positions) != M:
        raise RuntimeError(f"expected {M} contaminated sorted positions, got {true_positions}")

    observed = sorted(float(x) for x in ref_scores)
    ranks = [bisect.bisect_right(observed, float(x)) for x in stream_scores]
    return ranks, true_positions


def evaluate_one(path: Path, capture_index: int, alt_snr_db: float | None) -> dict[str, object]:
    iq, _, _ = read_u8_iq(path)
    blocks = base_blocks(iq)
    ranks, true_positions = detector_inputs(blocks, alt_snr_db, capture_index)

    cfg = kt13.base.build_config(K)
    true_index = cfg.candidates.index(tuple(true_positions))
    cfg = replace(cfg, true_candidate_index=true_index)
    out = kt13.evaluate_path(cfg, ranks)

    baseline_stop = out.baseline_stops[BASELINE_KEY]
    return {
        "file": path.name,
        "capture_index": capture_index,
        "condition": "null" if alt_snr_db is None else f"snr_{alt_snr_db:g}dB",
        "alt_snr_db": "" if alt_snr_db is None else alt_snr_db,
        "true_sorted_positions": ";".join(str(x) for x in true_positions),
        "static_stop": "" if out.static_stop is None else out.static_stop,
        "baseline_stop": "" if baseline_stop is None else baseline_stop,
        "oracle_stop": "" if out.oracle_stop is None else out.oracle_stop,
        "static_cross": int(out.static_stop is not None and out.static_stop <= T),
        "baseline_cross": int(baseline_stop is not None and baseline_stop <= T),
        "oracle_cross": int(out.oracle_stop is not None and out.oracle_stop <= T),
        "static_loge_T": out.static_logs[T],
        "baseline_loge_T": out.baseline_logs[BASELINE_KEY][T],
        "oracle_loge_T": out.oracle_logs[T],
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise RuntimeError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    conditions = ["null"] + [f"snr_{x:g}dB" for x in ALT_SNR_DB]
    out: list[dict[str, object]] = []
    for condition in conditions:
        group = [r for r in rows if r["condition"] == condition]
        for method in ("static", "baseline", "oracle"):
            crosses = [int(r[f"{method}_cross"]) for r in group]
            stops = [int(r[f"{method}_stop"]) for r in group if r[f"{method}_stop"] != ""]
            count = sum(crosses)
            lo, hi = wilson(count, len(group))
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


def make_figure(summary: list[dict[str, object]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    snrs = list(ALT_SNR_DB)
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for method, label in (("static", "Static coupling"), ("baseline", "Precommitted band baseline"), ("oracle", "Oracle")):
        selected = [next(r for r in summary if r["condition"] == f"snr_{snr:g}dB" and r["method"] == method) for snr in snrs]
        y = np.asarray([float(r["cross_rate"]) for r in selected])
        lo = np.asarray([float(r["cross_ci_low"]) for r in selected])
        hi = np.asarray([float(r["cross_ci_high"]) for r in selected])
        ax.errorbar(snrs, y, yerr=np.vstack((y-lo, hi-y)), marker="o", capsize=3, label=label)
    ax.set_xlabel("Offline injected tone SNR (dB)")
    ax.set_ylabel("Crossing probability by T=200")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "sdr_crossing_vs_snr.pdf")
    fig.savefig(outdir / "sdr_crossing_vs_snr.png", dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/sdr_publication_v1")
    parser.add_argument("--output-dir", default="results/sdr_publication_v1")
    parser.add_argument("--qc-only", action="store_true")
    parser.add_argument("--min-captures", type=int, default=10)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    files = sorted(input_dir.glob("capture_*.u8"))
    if not files:
        raise SystemExit(f"no capture_*.u8 files in {input_dir}")

    qc_rows = [qc_capture(path) for path in files]
    print("=== SDR QC ===")
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
        print("SDR_QC: COMPLETE")
        return 0

    if len(passing) < args.min_captures:
        raise SystemExit(f"only {len(passing)} captures passed QC; need at least {args.min_captures}. Capture more without changing QC thresholds.")

    rows: list[dict[str, object]] = []
    for capture_index, path in enumerate(passing):
        for snr in (None,) + ALT_SNR_DB:
            rows.append(evaluate_one(path, capture_index, snr))

    summary = summarize(rows)
    write_csv(output_dir / "raw_results.csv", rows)
    write_csv(output_dir / "summary.csv", summary)
    make_figure(summary, output_dir / "figures")

    manifest = {
        "status": "semi-synthetic RTL-SDR external validation",
        "K": K, "M": M, "T": T,
        "sample_rate_hz": SAMPLE_RATE,
        "block_len": BLOCK_LEN, "stride": STRIDE, "skip_samples": SKIP_SAMPLES,
        "reference_contaminated_blocks_zero_based": list(REFERENCE_CONTAMINATED_BLOCKS),
        "reference_injection_snr_db": REFERENCE_INJECTION_SNR_DB,
        "alternative_snr_db": list(ALT_SNR_DB),
        "tone_offset_hz": TONE_OFFSET_HZ,
        "baseline_key": list(BASELINE_KEY),
        "qc": {
            "min_unique_codes": MIN_UNIQUE_CODES,
            "min_adc_std_codes": MIN_ADC_STD_CODES,
            "max_clip_fraction": MAX_CLIP_FRACTION,
            "max_power_p95_p5_db": MAX_POWER_P95_P5_DB,
        },
        "passing_captures": len(passing),
        "total_captures": len(files),
        "note": "Offline injection occurs after ADC; this validates the detector over real receiver/background IQ but does not model signal-induced front-end nonlinearity."
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("")
    print("=== SDR SUMMARY ===")
    for row in summary:
        print(f"{row['condition']:>10s} {row['method']:>8s} cross={float(row['cross_rate']):.3f} [{float(row['cross_ci_low']):.3f},{float(row['cross_ci_high']):.3f}] delay={row['median_stop_detected'] or 'NA'}")
    print(f"results: {output_dir}")
    print("SDR_PUBLICATION_V1: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())