# P−1 Hardware preflight result — RTL-SDR Blog V4

Status: **PASS with one transport-rate follow-up**

Date: 2026-09-16

## Hardware / host confirmed

- Capture host: `debian-12-aml-s905x-cc` (Orange Pi class host)
- SDR: `RTLSDRBlog, Blog V4`
- Serial: `00000001`
- Baseband: RTL2832U
- Tuner: Rafael Micro R828D
- Manual tuner gain values reported: 29 discrete settings from 0.0 to 49.6 dB
- RTL-SDR Blog V4 support detected by the installed userspace driver

## Driver frozen

The Debian Bookworm package `rtl-sdr 0.6.0-4` was removed and a current upstream `osmocom/rtl-sdr` build was installed from source.

Exact source commit:

`797f8143266d983c56d8f35d2d442527529dd8a5`

CMake reported library version `2.0.3` and installed binaries under `/usr/local/bin` and libraries under `/usr/local/lib`.

The DVB kernel module `dvb_usb_rtl28xxu` was blacklisted before reboot so the SDR can be used as a software-defined radio without requiring runtime detachment.

## Functional checks

`rtl_test -t` after reboot reported:

- device detected;
- R828D tuner detected;
- explicit `RTL-SDR Blog V4 Detected`;
- supported tuner gains enumerated.

The message `No E4000 tuner found, aborting.` is expected for the `-t` benchmark because this unit uses an R828D tuner rather than an Elonics E4000 tuner. It is not a hardware failure.

## Streaming check

Command:

```bash
timeout 10s rtl_test -s 2400000
```

Result:

- 2.4 MS/s asynchronous streaming started successfully;
- at least 52 bytes were reported lost during the approximately 10 s run;
- tool summary: `Samples per million lost (minimum): 1`.

This is a very small loss rate, but the scientific pilot should prefer a sample rate that produces zero reported losses under repeated short tests if available.

## Preflight decision

**PASS** for device identity, userspace access, V4-capable driver, tuner recognition and basic streaming.

One follow-up remains before freezing the acquisition configuration: compare 2.4 MS/s and 2.048 MS/s (and, only if needed, a lower rate) over repeated 30 s streaming tests and choose the highest rate that is consistently loss-free or demonstrably negligible under the pilot requirements.

## Next command gate

Run three 30 s trials at 2.4 MS/s and three at 2.048 MS/s. Record all loss messages and the final `Samples per million lost` values. Do not begin the 45-minute warm-up experiment until the acquisition rate is frozen.
