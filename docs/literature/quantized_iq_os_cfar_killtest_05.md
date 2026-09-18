# P−1 Quantized-IQ OS-CFAR Kill-Test 05 — LIMEN-RF

Status: **NO-GO as central novelty**

Date: 2026-09-18

## Question

Does the narrow candidate survive?

> Exact finite-sample OS-CFAR calibration for multi-bit I/Q quantization applied before energy formation, with unknown analog noise scale and discrete ties near the ADC floor.

## Mathematical observation

Let the analog null samples be independent zero-mean Gaussian I/Q with scale parameter sigma and let Q_Delta be a fixed uniform finite-bit ADC quantizer with step Delta. The digital energy of one complex sample is

E_q = Q_Delta(I)^2 + Q_Delta(Q)^2.

For fixed Delta, the probability mass function of E_q depends on the dimensionless operating point sigma/Delta. Therefore a block energy

A_m = sum E_q

is a discrete family whose shape changes with sigma/Delta; it is not merely a scaled copy of a fixed Gamma law.

Consequently the usual analog scale cancellation behind a ratio such as

Z = A / (A + B_(k))

does not generally survive fixed pre-square quantization.

This is a valid observation, but it is not enough for novelty.

## Limiting argument

For a symmetric midriser quantizer, as sigma/Delta -> 0, almost all I/Q samples fall on the two central output levels. Block energies become nearly deterministic and ties dominate.

At very large sigma/Delta, a finite ADC increasingly saturates, again producing a highly discrete/degenerate regime.

Hence a single deterministic OS scaling constant cannot generally maintain the same nontrivial Pfa over all analog noise scales. The nuisance parameter has moved from a pure scale family into the discrete code probabilities.

## Why this still does not survive as a paper core

### Existing quantized-CFAR theory

Gandhi (1996) analytically treats uniform quantization effects on both CA-CFAR and OS-CFAR, including Pfa and Pd.

Lehtomäki et al. (2005) directly treat pre-square I/Q quantization for a total-power radiometer, false-alarm threshold setting, exact randomized decisions when the analog noise scale is known, and a CA-CFAR strategy with quantized reference samples when it is estimated.

One-bit radar literature applies CFAR after raw ADC quantization, and recent one-bit detector work derives CFAR-aware tests under colored-noise uncertainty.

Thus “quantization breaks nominal CFAR and needs recalibration” is established prior art.

### Distribution-free escape route is also established

The obvious scale-free rescue is to abandon amplitude ratios and use ranks/permutations under exchangeability.

That route is also established:
- classical rank-sum nonparametric CFAR;
- permutation-test CFAR;
- rank-quantization nonparametric CFAR;
- recent modified rank-sum CFAR variants for clutter edges and multiple targets.

With randomized tie handling, discrete ADC outputs do not create a fundamentally new statistical principle: exact finite-sample rank/permutation validity under exchangeability is standard machinery.

## Decision

The narrow candidate is **NO-GO as the central novelty**.

A paper whose main result is one of the following would be too incremental:

1. derive the exact discrete null pmf for quantized I/Q block energy;
2. numerically optimize an OS threshold over sigma/Delta;
3. show that fixed quantization breaks the analog Gamma scale invariance;
4. restore Pfa using randomized ties/ranks/permutation;
5. validate those known effects on an RTL-SDR.

The combination may still be useful as a methods/engineering section inside a broader paper, but it should not carry the novelty claim.

## What the hardware experiment still contributed

The RTL-SDR result was scientifically useful because it falsified an experimental assumption:
- at 28 dB the open-input samples were almost entirely concentrated on the central ADC codes;
- increasing gain up to the tested 49.6 dB still failed the predeclared >=4-count dispersion gate;
- therefore the planned analog hardware-aging experiment did not have the desired measurement sensitivity.

That negative result prevents us from building theory around an inadequately resolved measurement regime.

## P−1 consequence

Close the quantized-IQ branch as a novelty candidate.

Do not run more hardware experiments for this branch.

The next candidate should require a structural result that is not already supplied by:
- classical quantized CFAR;
- quantized radiometer theory;
- rank/permutation nonparametric CFAR;
- general anytime-valid/e-process theory.

P−1 remains open until a genuinely distinct candidate is identified or the project is terminated/reframed.
