# P−1 Kill-Test 10 Result — matched baseline comparison

Status: **PASS for the small-reference regime / not yet sufficient for the paper-core claim**

Date: 2026-09-18

## Frozen configuration

- K=8
- M=2
- n=6 clean references
- alpha=0.05
- delta=0.025
- confidence-band conditional alpha = 0.02564103
- PRM threshold = 20
- confidence-band threshold = 39
- 200 Monte Carlo paths per condition
- horizons T in {40,100,200}
- conditions: null, Beta(2,1), Beta(4,1), Beta(8,1)

## Main observed crossing rates

| condition | T | static coupling | generic band | CCTM-style | oracle |
|---|---:|---:|---:|---:|---:|
| null | 40 | 0.000 | 0.000 | 0.000 | 0.030 |
| null | 100 | 0.000 | 0.000 | 0.000 | 0.035 |
| null | 200 | 0.000 | 0.000 | 0.000 | 0.035 |
| beta_2 | 40 | 0.050 | 0.000 | 0.000 | 0.220 |
| beta_2 | 100 | 0.060 | 0.000 | 0.000 | 0.270 |
| beta_2 | 200 | 0.080 | 0.000 | 0.000 | 0.295 |
| beta_4 | 40 | 0.225 | 0.000 | 0.000 | 0.600 |
| beta_4 | 100 | 0.330 | 0.000 | 0.000 | 0.700 |
| beta_4 | 200 | 0.440 | 0.000 | 0.000 | 0.760 |
| beta_8 | 40 | 0.530 | 0.000 | 0.000 | 0.910 |
| beta_8 | 100 | 0.725 | 0.000 | 0.000 | 0.950 |
| beta_8 | 200 | 0.810 | 0.000 | 0.000 | 0.960 |

The 50-repetition smoke rerun showed the same qualitative pattern.

## Critical interpretation

The result is strong, but the zeros for the two confidence-band baselines are not mysterious and must not be oversold.

For n=6 and delta=0.025,

epsilon_DKW = sqrt(log(2/delta)/(2n)) = 0.604292.

Therefore even at the most favorable observed rank, the exact-count lower CDF bound satisfies

L_max = 1 - epsilon_DKW = 0.395708 < 0.5.

For the right-shift linear betting family used in the generic band baseline, every admissible score is therefore nonpositive. The method cannot accumulate positive evidence in this regime.

For the CCTM-style symmetric contaminated-ECDF construction,

epsilon_sym = (n/K) epsilon_DKW + M/K = 0.703219 > 0.5.

Hence even u=1 is inside a confidence region too wide to support a positive one-sided CCTM bet. Its zero power is also expected from the geometry of the band, not from a coding failure.

This is itself an important result:

> finite-sample rank coupling can remain informative in a regime where simultaneous DKW confidence-band approaches are effectively vacuous.

However, it is only a **small-reference regime** result. It does not yet establish a general superiority claim against informative CCTM/band baselines.

## Next non-vacuity gate

We need move to reference sizes where the generic baselines can actually bet positively.

With M=2 and delta=0.025:

| K | n=K-M | epsilon_clean | epsilon_sym |
|---:|---:|---:|---:|
| 12 | 10 | 0.4681 | 0.5567 |
| 14 | 12 | 0.4273 | 0.5091 |
| 16 | 14 | 0.3956 | 0.4712 |
| 20 | 18 | 0.3489 | 0.4140 |

Thus:
- the exact-count band first becomes non-vacuous by K=12;
- the symmetric CCTM-style baseline becomes non-vacuous by about K=16.

The next comparison should therefore include at least K=16,M=2 and K=20,M=2.

## Scientific status

Kill-Test 10 passes the small-reference gate and strengthens the article hypothesis:

- static-coupling PRM remains useful at K=8,M=2;
- generic uniform-band approaches are too conservative to use the available information in that regime;
- oracle performance shows substantial remaining room for efficiency improvements.

But the paper-core claim remains provisional until the static-coupling method is compared against non-vacuous confidence-band baselines at larger K.
