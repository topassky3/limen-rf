# P−1 IQ Capture Gate Result — LIMEN-RF

Status: **PASS**

Purpose: verify that the Orange Pi + RTL-SDR Blog V4 acquisition path can produce exact-length IQ files under the candidate pilot sample rate before starting the hardware identifiability experiment.

## Frozen hardware/software context

- Capture host: Orange Pi / Debian 12, host `debian-12-aml-s905x-cc`
- SDR: RTL-SDR Blog V4, SN `00000001`
- Tuner: Rafael Micro R828D
- rtl-sdr source commit: `797f8143266d983c56d8f35d2d442527529dd8a5`
- Candidate sample rate: `2,048,000 samples/s`
- Diagnostic center frequency: `100,000,000 Hz`
- Diagnostic fixed tuner gain: `28.0 dB`
- Capture duration: `2 s`
- Complex samples per capture: `4,096,000`
- Expected byte count for unsigned 8-bit interleaved I/Q: `8,192,000 bytes`

The diagnostic center frequency and gain are not yet claimed as final scientific pilot parameters; they were used to validate the acquisition path.

## Observed result

Four fixed-length captures completed successfully. Every file had exactly the expected size:

| Capture | Size | SHA-256 |
|---|---:|---|
| `capture_test.iq` | 8,192,000 bytes | `f5abecc9911607a430c223cdd7228a3224f99c5438e73306097c76cd490cff72` |
| `capture_test_1.iq` | 8,192,000 bytes | `af6296a51f2e5b5755dee387787bb5e8190cf6ef290ea615429e1300b231d43b` |
| `capture_test_2.iq` | 8,192,000 bytes | `1534a9fa2e960607e93619850ca9a0717b42fe46be42318f26529b222e28ead1` |
| `capture_test_3.iq` | 8,192,000 bytes | `e08e68c5a022290e25faab417f71c6e6a5b98f278ae36c50eb70e0cec32ff098` |

The differing hashes are expected because the IQ noise realization changes between captures. Exact file length confirms that the requested number of samples was written each time.

`rtl_sdr` printed `User cancel, exiting...` after reaching the requested finite sample count. In this context it is not treated as a capture failure because each file closed at the exact requested length and no device/USB error was emitted.

## Gate decision

**PASS.** The acquisition path is ready for the P−1 hardware identifiability pilot, subject to freezing the controlled RF input condition and scientific run parameters.

## Important remaining experimental constraint

The warm-up/calibration-aging experiment should preferably use a direct 50-ohm termination at the SDR input. If a termination is unavailable, the input condition must be explicitly documented and the result treated as more confounded by ambient RF pickup.

The diagnostic captures performed while the dongle was already warm do not count as a cold-start pilot run.

## Next gate

Before starting the 45-minute trace:

1. confirm the physical input condition (`50ohm` preferred; otherwise document fallback);
2. freeze Stage-A center frequency and manual gain;
3. power down/unplug the SDR long enough to return near ambient;
4. start the scripted run immediately after reconnecting;
5. collect 2-s IQ captures every 60 s for 45 min with exact timestamps, hashes and available host thermal metadata;
6. do not tune, change gain, enable AGC, or alter bandwidth during the run.

A second independent cold-start session is required before declaring the hardware-aging phenomenon reproducible.
