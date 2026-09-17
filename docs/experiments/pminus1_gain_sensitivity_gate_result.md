# P−1 Gain-Sensitivity Gate Result — LIMEN-RF

Status: **FAIL under frozen criterion**

Date: 2026-09-17

## Purpose

Test whether increasing fixed manual tuner gain on the RTL-SDR Blog V4 moves the open-input noise sufficiently away from the 8-bit ADC quantization floor to support a more sensitive hardware-aging experiment.

Frozen criterion before measurement:

- `min(std_I, std_Q) >= 4.0` ADC counts;
- clipping fraction exactly `0`;
- choose the lowest passing gain if multiple gains pass.

## Configuration

- center frequency: `300 MHz`
- sample rate: `2.048 MS/s`
- input: open SMA input, antenna disconnected
- fixed manual gains tested: `28.0, 32.8, 38.6, 43.9, 49.6 dB`
- two 1 s captures per gain

## Results

| Gain dB | std I | std Q | central fraction I | central fraction Q | clipping | PASS |
|---:|---:|---:|---:|---:|---:|:---:|
| 28.0 | 0.527 / 0.526 | 0.526 / 0.526 | 0.9770 / 0.9773 | 0.9770 / 0.9772 | 0 | No |
| 32.8 | 0.598 / 0.598 | 0.598 / 0.598 | 0.9382 / 0.9382 | 0.9382 / 0.9382 | 0 | No |
| 38.6 | 0.816 / 0.816 | 0.817 / 0.816 | 0.8032 / 0.8033 | 0.8029 / 0.8033 | 0 | No |
| 43.9 | 1.309 / 1.309 | 1.309 / 1.307 | 0.5648 / 0.5643 | 0.5637 / 0.5647 | 0 | No |
| 49.6 | 1.705 / 1.701 | 1.704 / 1.701 | 0.4472 / 0.4482 | 0.4470 / 0.4483 | 0 | No |

## Decision

**FAIL.** No tested gain met the frozen `>= 4 ADC-count` sensitivity criterion.

The highest available tested gain, 49.6 dB, improved digital dispersion substantially relative to 28 dB but still reached only about 1.70 ADC counts standard deviation. Therefore the current open-input architecture cannot satisfy the predeclared sensitivity gate simply by increasing tuner gain.

This result does **not** prove that hardware-state drift is absent. It says that this particular measurement architecture does not meet the frozen sensitivity requirement for another 45-minute hardware-aging run.

## Scientific consequence

Do not lower the 4-count threshold after seeing the data and do not repeat the 45-minute warm-up trace under the same open-input architecture merely with higher gain.

The gate also revealed a separate physical fact worth screening: raw RTL-SDR samples in this low-input regime are strongly quantized, and the continuous-Gaussian/Gamma assumptions used by classical energy/CFAR derivations may be a poor model at moderate gain. This observation is **not** a novelty claim. Quantization effects in CFAR and energy detection have prior literature and require a dedicated firewall before becoming a candidate direction.
