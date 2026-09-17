# P−1 Hardware Pilot Run 01 — First-pass result

Status: **NO evidence of material calibration-aging effect in this run; measurement-sensitivity diagnostic required before final kill**

Run: `pilot_open_01`

Input condition: open SMA input, antenna disconnected

Frozen analysis plan: `docs/experiments/pminus1_hardware_analysis_plan_v0.1.md`

## Integrity

The acquisition and analysis integrity gate passed:

- 46 / 46 captures analyzed;
- 1000 blocks per capture;
- 5000 baseline blocks from captures 0..4;
- no integrity errors;
- maximum clipping fraction = 0.

## Frozen first-pass numerical result

- baseline median block power, DC-removed: `0.5539149046`
- power drift range: `-0.015602 dB .. +0.007928 dB`
- final drift at 45 min: `+0.002812 dB`
- stale-calibration PFA range: `0.002 .. 0.021`
- stale-calibration PFA final: `0.007`
- local-normalized PFA range: `0.004 .. 0.019`
- local-normalized PFA final: `0.007`
- nominal alpha: `0.01`

The total observed power-location span is only about `0.02353 dB`. The stale-threshold and local-normalized PFA trajectories have comparable ranges and identical final value in the frozen summary. Therefore Run 01 does not show the predicted signature of a scalar warm-up drift that specifically degrades stale calibration while local normalization remains stable.

## Statistical caution

Each epoch contains 1000 blocks at nominal alpha = 0.01, so ordinary binomial sampling variability is non-negligible. A single high epoch such as 0.021 should not be treated as evidence by itself, especially across 46 inspected epochs and because threshold estimation and block dependence make an ideal independent-binomial calculation only approximate.

## Important new diagnostic observation

The baseline DC-removed median block power is about `0.554` ADC-count-squared units. With unsigned 8-bit I/Q represented around half-code 127.5, this is very close to the minimum two-channel power scale produced by samples concentrated around adjacent center codes (roughly 0.5 for I/Q values near 127 and 128).

This raises a measurement-sensitivity concern: the open-input, 28 dB configuration may be operating close to the ADC quantization floor. If so, small analog receiver-noise changes could be masked by quantization and Run 01 would be an under-sensitive test of thermal gain/noise drift.

This is not evidence for the hardware-aging hypothesis. It is a concrete measurement-system observation that must be checked before declaring a clean NO-GO.

## Decision

Do **not** run another 45-minute trace yet.

First perform a short quantization-adequacy diagnostic on existing IQ data and, if needed, a very short fixed-gain sweep. Inspect:

- I and Q sample-code occupancy / histograms;
- standard deviation of I and Q in ADC counts;
- fraction of samples in the central codes 127/128;
- mean raw power versus DC-removed power;
- whether increasing fixed gain moves the noise distribution well above quantization while remaining far from clipping.

If Run 01 is not quantization-limited, then its result is a strong NO-GO signal for the warm-up/calibration-aging direction under this condition and a second 45-minute run is not justified.

If it is quantization-limited, redesign only the measurement sensitivity (gain/input termination), not the scientific hypothesis, and repeat the kill-test under a configuration with adequate ADC occupancy.

## Publication / novelty interpretation

Run 01 provides no positive novelty evidence. It does not support a calibration-aging claim, and no publication claim should be made from it. The surviving question is purely whether the measurement configuration had enough sensitivity to falsify the physical hypothesis.
