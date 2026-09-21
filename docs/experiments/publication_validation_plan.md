# Publication validation plan — frozen LIMEN-RF method

Date: 2026-09-21

Status: **post-freeze validation only; no retuning**

## Decision

The mathematical paper does not require SDR data to prove Theorem 1.

However, because LIMEN-RF is motivated by RF/CFAR-style reference banks and is intended for an engineering audience, a controlled SDR validation can materially strengthen the manuscript if it is treated as **external validation**, not as a new tuning stage.

The previous open-SMA RTL-SDR pilot is not reusable as evidence: the digitizer stayed close to the quantization floor even after the gain sweep. It should not be repeated under the same geometry.

The validation sequence is therefore:

\[
\text{frozen high-rep simulation}
\rightarrow
\text{semi-synthetic real-IQ validation}
\rightarrow
\text{optional observational RF demo}.
\]

## Phase V1 — publication-grade frozen Monte Carlo

Keep the paper-core conditions unchanged:

- \(K\in\{24,32\}\);
- \(m=2\);
- \(\alpha=0.05\);
- \(T\in\{40,100,200\}\);
- null Uniform\((0,1)\);
- alternatives Beta\((2,1)\), Beta\((4,1)\), Beta\((8,1)\);
- contaminants: two fixed high values at 2.0;
- same frozen bettor portfolio;
- same frozen baseline grids.

Target at least 5,000 replications per final condition if runtime permits.

Report crossing probabilities with 95% binomial intervals, paired static-minus-baseline differences, median detected delay with bootstrap intervals, oracle gap, and null crossing estimates.

This is estimation, not another kill gate.

## Phase V1b — contamination-geometry stress tests

Without changing the method, add a small validation matrix:

1. outside-support high contaminants;
2. in-support upper contaminants;
3. mixed low/high contaminants;
4. static random contaminants sampled independently before the stream.

Do not choose new bettor parameters after seeing the results.

## Phase V2 — semi-synthetic RTL-SDR validation

### Rationale

Use real RTL-SDR IQ to retain quantization, tuner noise, oscillator error, front-end imperfections, and environmental RF, while using controlled offline injection to preserve known ground truth.

This is more defensible than repeating the failed open-input pilot.

### Acquisition

Use RTL-SDR V4 with an antenna or controlled input producing a non-degenerate digitized signal.

Freeze:

- center frequency during a capture;
- sample rate;
- manual gain;
- AGC off;
- identical receiver configuration for reference and online blocks.

Record IQ plus metadata.

### Quality gates

Reject a capture before looking at detector outcomes if:

- I/Q effectively use only a few ADC codes;
- there is severe clipping;
- robust I/Q variation is again near the prior open-SMA quantization floor;
- block power is grossly nonstationary over the intended null interval;
- dropped-sample discontinuities are evident.

Freeze exact QC thresholds from receiver diagnostics before viewing LIMEN-RF outcomes.

### Scalar score

Use a precommitted scalar block score such as

\[
S_b=
\log\left(
\frac1L\sum_{\ell=1}^{L}|x_{b,\ell}|^2
\right).
\]

### Reference construction

From an initial stationary interval, obtain \(n\) clean reference block scores.

Create exactly \(m\) contaminated reference cells by controlled offline injection into selected reference IQ blocks, e.g. a deterministic complex tone or controlled wideband energy.

The same contamination identities remain fixed throughout the online run.

### Null and alternative streams

Use later blocks from the same stationary capture for the null stream.

Measure scalar-score autocorrelation and thin blocks if needed.

Create known alternatives by injecting controlled signal energy into future IQ blocks after a fixed change point.

Do not retune the frozen bettor portfolio on SDR outcomes.

### Replication

Prefer multiple independent capture sessions rather than many pseudo-replicates from a single recording.

Store capture metadata, preprocessing code, injection seeds/parameters, contamination identities, and derived scalar scores.

### Claim scope

If successful, the paper may state that a semi-synthetic RTL-SDR experiment with real receiver IQ reproduces the qualitative finite-reference behavior seen in simulation.

It must not claim that hardware validates the theorem or establishes universal real-world CFAR performance.

## Phase V3 — optional observational RF demo

Only after V2 succeeds.

A fully observational RF example may use persistent occupied/interfered reference bins and a scalar spectral feature, but ground truth will be weaker.

It should not delay the manuscript.

## Preferred evidence stack

\[
\boxed{
\text{theorem}
+
\text{5k-rep frozen simulation}
+
\text{semi-synthetic RTL-SDR validation}
}
\]

This gives mathematical validity, statistically stable finite-reference estimates, and an engineering bridge to RF without reopening method development.
