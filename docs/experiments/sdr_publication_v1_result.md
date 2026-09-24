# RTL-SDR semi-synthetic validation V1 — frozen result

Date: 2026-09-24

Status: **FULL RUN COMPLETE — detector and preregistered SDR protocol remained frozen**

Receiver settings:

- RTL-SDR Blog V4 on Orange Pi sensor node
- center frequency: 100 MHz
- sample rate: 2.048 MS/s
- manual gain: 28.0 dB
- 20 final 10 s captures
- pre-outcome QC: 20/20 PASS

Frozen statistical settings:

- K=32, m=2, T=200
- score = log mean block power
- block_len=16384, stride=32768
- contaminated reference identities: 7 and 24 (zero-based physical blocks)
- reference tone contamination: +6 dB
- future injection grid: {-12,-6,-3,0} dB from t=1
- precommitted comparator: band_mix, delta=0.045

## QC summary

All 20 captures passed the frozen QC gates. No clipping was observed.
Observed score lag-1 dependence ranged approximately from 0.253 to 0.888, so the real receiver/background sequence is not close to an iid ideal in every capture. This is a model-mismatch limitation and is not used as a post-outcome rejection rule.

## Detector results

| condition | static cross | static delay | baseline cross | baseline delay | oracle cross | oracle delay |
|---|---:|---:|---:|---:|---:|---:|
| null | 0.10 [0.028,0.301] | 85.0 | 0.00 [0.000,0.161] | NA | 0.10 [0.028,0.301] | 85.0 |
| -12 dB | 1.00 [0.839,1.000] | 4.5 | 0.75 [0.531,0.888] | 29.0 | 1.00 [0.839,1.000] | 3.5 |
| -6 dB | 1.00 [0.839,1.000] | 3.0 | 1.00 [0.839,1.000] | 24.0 | 1.00 [0.839,1.000] | 3.0 |
| -3 dB | 1.00 [0.839,1.000] | 3.0 | 1.00 [0.839,1.000] | 24.0 | 1.00 [0.839,1.000] | 3.0 |
| 0 dB | 1.00 [0.839,1.000] | 3.0 | 1.00 [0.839,1.000] | 24.0 | 1.00 [0.839,1.000] | 3.0 |

## Interpretation

1. The real-receiver semi-synthetic experiment reproduces the qualitative sensitivity advantage of static coupling under injected alternatives. At -12 dB the proposed method and oracle cross on all 20 captures, while the precommitted band comparator crosses on 15/20; the detected median stopping time is 4.5 versus 29.
2. From -6 dB upward, all methods saturate in crossing probability. Static coupling and the oracle nevertheless stop much earlier (median 3) than the baseline (median 24).
3. The null result is not evidence of hardware-level type-I control: static/oracle cross on 2/20 captures (0.10), with a wide Wilson interval [0.028,0.301] that includes 0.05. Because the physical score stream shows non-negligible serial dependence, the iid theorem should not be applied directly to this hardware experiment.
4. The preregistered SNR grid is too strong to map a detailed power transition: the method is already saturated at -12 dB. Any weaker-SNR follow-up must therefore be labeled a new post-V1, pre-registered extension and should use fresh captures rather than altering V1.

## Gate decision

**SDR VALIDATION V1: PASS FOR EXTERNAL ENGINEERING SENSITIVITY; NOT A HARDWARE TYPE-I VALIDATION.**

The defensible paper claim is that, on real RTL-SDR background IQ with controlled post-ADC tone injection, the frozen static-coupling detector preserved a strong qualitative detection-speed/sensitivity advantage over the precommitted confidence-band comparator. The experiment does not establish iid null validity or front-end nonlinear response to an over-the-air signal.

Recommended next step for an engineering paper: archive V1 artifacts, then preregister a fresh weaker-SNR V2 characterization to resolve the transition below -12 dB and improve the engineering power curve, without changing the detector.