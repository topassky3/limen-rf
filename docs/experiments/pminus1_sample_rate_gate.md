# P−1 Sample-Rate Gate — LIMEN-RF

Status: **closed / parameter frozen for pilot v0.1**

Hardware: RTL-SDR Blog V4, RTL2832U + Rafael Micro R828D, attached to Orange Pi / Debian 12 capture host.

Driver: Osmocom `rtl-sdr` built from commit `797f8143266d983c56d8f35d2d442527529dd8a5`.

## Trials

Each rate was tested with three 30 s `rtl_test` runs.

| Sample rate | Trial 1 | Trial 2 | Trial 3 | Summary |
|---|---:|---:|---:|---|
| 2.4 MS/s | >=16 B lost, 0 ppm | >=164 B lost, 1 ppm | >=100 B lost, 0 ppm | usable but one nonzero ppm report |
| 2.048 MS/s | >=32 B lost, 0 ppm | >=40 B lost, 0 ppm | >=72 B lost, 0 ppm | best high-rate candidate |
| 1.8 MS/s | >=104 B lost, 0 ppm | >=88 B lost, 0 ppm | >=8 B lost, 0 ppm | no advantage over 2.048 MS/s |
| 1.6 MS/s | >=96 B lost, 1 ppm | >=24 B lost, 0 ppm | >=128 B lost, 1 ppm | worse than 2.048/1.8 MS/s |

## Decision

Freeze the pilot sample rate at:

\[
\boxed{f_s = 2.048\ \text{MS/s}}
\]

Rationale:

- all three 2.048 MS/s runs reported `0 samples per million lost (minimum)`;
- 1.8 MS/s did not improve loss behavior enough to justify reduced bandwidth;
- 1.6 MS/s was measurably worse in this host/device configuration;
- 2.4 MS/s produced one run with a nonzero minimum ppm loss report.

The tiny byte-loss reports at 2.048 MS/s are not ignored. They are treated as a capture-quality covariate and motivate an exact fixed-length capture sanity test before the 45 min warm-up experiment.

## Next gate

Do not start the 45 min warm-up trace yet. First validate the actual acquisition mode used by the experiment with fixed-length IQ captures at 2.048 MS/s rather than relying only on timeout-terminated `rtl_test` runs.

For each fixed-length capture, record command, exit status, file size, expected size, SHA-256, and stderr. A mismatch in expected file size or a driver error fails the gate.

## Scientific interpretation

This gate is infrastructure only. It does not support any claim about calibration drift, CFAR false-alarm behavior, or publication novelty.
