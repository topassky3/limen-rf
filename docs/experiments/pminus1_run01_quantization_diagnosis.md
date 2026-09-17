# P−1 Run 01 quantization diagnosis — LIMEN-RF

Status: **Run 01 scientifically inconclusive for drift; acquisition sensitivity gate required**

## Observed Run 01 result

The first 45-minute open-input run completed with integrity PASS and no clipping. The frozen first-pass analysis showed only a very small relative power excursion and no clear separation between stale-threshold and locally normalized false-alarm behavior.

However, inspection of the raw ADC-code distribution in `capture_000.iq` revealed that the acquisition is strongly quantization-limited:

- I mean: 127.3634, std: 0.5260 ADC counts, min/max: 125/130;
- Q mean: 127.3628, std: 0.5257 ADC counts, min/max: 125/130;
- I fraction in codes 127 or 128: 0.977324;
- Q fraction in codes 127 or 128: 0.977403;
- more than 97.7% of both I and Q samples occupy only the two central ADC codes.

This means the experiment had very little effective amplitude resolution. The measured broadband variation is therefore dominated enough by quantization that a small analog noise-floor or gain drift could be hidden.

## Scientific decision

Do **not** interpret Run 01 as evidence that calibration aging is absent.

Do **not** interpret Run 01 as evidence that calibration aging exists.

Classify it as an **instrument-sensitivity failure / inconclusive run** for the physical drift hypothesis.

The correct next action is not another 45-minute cold-start trace. First establish an acquisition condition with substantially larger ADC-code spread while remaining comfortably away from clipping.

## Frozen gain-sensitivity gate

At the same center frequency (300 MHz), sample rate (2.048 MS/s), open input, and current warm device state, sweep the following supported manual gains:

- 28.0 dB
- 32.8 dB
- 38.6 dB
- 43.9 dB
- 49.6 dB

Use two 1-second captures per gain.

For each capture report:

- I and Q standard deviation in ADC counts;
- fraction of samples in central codes 127/128;
- min/max code;
- clipping fraction, where clipping means I or Q <= 1 or >= 254.

### Sensitivity PASS criterion

A gain is eligible for the next cold-start run only if, in both repetitions:

- `min(std_I, std_Q) >= 4.0` ADC counts;
- clipping fraction is zero;
- no capture/USB error occurs.

The 4-count criterion is an instrumentation rule chosen before the sweep: it places the analog/code spread well above a 1-LSB quantizer step, so first-pass power statistics are not dominated by two-code toggling.

If multiple gains pass, choose the **lowest** passing gain to retain headroom against RF/EMI transients.

### Gate outcomes

- If at least one gain passes: freeze that gain and repeat the 45-minute cold-start pilot as Run 02 under the same open-input limitation.
- If no gain passes even at 49.6 dB: do not repeat the long experiment. Revisit the measurement architecture (frequency, controlled termination/noise source, analog chain, or input condition) before collecting more warm-up data.

## Guardrail

This gate addresses measurement sensitivity only. Passing it does not establish calibration-aging physics or publication novelty.
