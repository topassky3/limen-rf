# P−1 RTL-SDR sample-rate preflight results

Status: **measured / preflight decision**

Hardware: RTL-SDR Blog V4, R828D tuner, serial `00000001`.

Driver: osmocom `rtl-sdr`, commit `797f8143266d983c56d8f35d2d442527529dd8a5`, installed under `/usr/local`.

Host: Debian 12 on `debian-12-aml-s905x-cc`.

## Test method

For each sample rate, run three 30 s `rtl_test` acquisitions separated by 5 s:

```bash
for i in 1 2 3; do
  timeout 30s rtl_test -s <RATE>
  sleep 5
done
```

## Results

### 2.4 MS/s

- Trial 1: `lost at least 16 bytes`; reported `0` samples per million lost.
- Trial 2: `lost at least 164 bytes`; reported `1` sample per million lost.
- Trial 3: `lost at least 100 bytes`; reported `0` samples per million lost.

### 2.048 MS/s

- Trial 1: `lost at least 32 bytes`; reported `0` samples per million lost.
- Trial 2: `lost at least 40 bytes`; reported `0` samples per million lost.
- Trial 3: `lost at least 72 bytes`; reported `0` samples per million lost.

## Interpretation

Both rates are operational. However, neither is literally loss-free because every run emitted at least one byte-loss warning. The 2.048 MS/s condition is clearly cleaner in this small comparison: all three trials rounded to `0` samples per million lost, while one 2.4 MS/s trial reached `1` per million.

Because the upcoming pilot is about small power-distribution shifts, the acquisition path should be made as clean as reasonably possible before scientific collection. The sample-rate decision is therefore **not yet frozen**.

## Next micro-gate

Test 1.8 MS/s and 1.6 MS/s using the same three-by-30-second protocol.

Freeze the highest rate that produces no `lost at least ...` messages across all three trials. If both lower rates still emit only tiny byte-loss warnings, prefer 2.048 MS/s and treat the residual loss rate as negligible only after confirming that short 2 s captures used by the pilot do not report losses.

## Current decision

**2.048 MS/s is the provisional preferred rate, but one final lower-rate comparison is required before the hardware pilot configuration is frozen.**
