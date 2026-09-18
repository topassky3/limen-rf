# P−1 Kill-Test 13 — final baseline-strength audit

Status: **frozen final adversarial baseline gate**

Date: 2026-09-18

## Purpose

Kill-Test 12 produced a strong finite-reference advantage for static-coupling predictive ranks after the generic confidence-band baselines became non-vacuous.

Before freezing the method and moving to theorem/manuscript work, this gate gives the baselines one final advantage.

We do **not** modify the static-coupling method.

Instead we strengthen the competitors by:

1. sweeping a pre-specified valid DKW failure-budget grid;
2. adding an adaptive one-sided ONS bettor to the exact-count lower-band baseline;
3. sweeping several globally nonnegative one-sided CCTM betting bounds;
4. reporting the best-performing valid configuration from the grid as an **oracle-tuned benchmark**.

The oracle-tuned envelope is deliberately favorable to the baseline. It is not itself a single precommitted test, because selecting delta after seeing power results is post hoc. Every individual grid configuration, however, is evaluated with its own matched marginal alpha budget.

## Frozen model

Same as Kill-Test 12:

- K in {24,32};
- M=2 fixed high contaminants;
- n=K-M clean references;
- null Uniform(0,1);
- alternatives Beta(gamma,1), gamma in {2,4,8};
- horizons T in {40,100,200};
- alpha=0.05;
- 200 Monte Carlo paths per K/condition;
- seed 20260918;
- identical paths across all methods.

## Delta audit grid

Freeze

delta in {0.005,0.010,0.015,0.020,0.025,0.030,0.035,0.040,0.045}.

For each delta,

a(delta) = (alpha-delta)/(1-delta),

and the confidence-band crossing threshold is

1/a(delta).

The clean DKW radius is

epsilon_clean(delta)
= sqrt(log(2/delta)/(2n)),

and the symmetric contaminated-ECDF radius is

epsilon_sym(delta)
= (n/K) epsilon_clean(delta) + M/K.

## Baseline A — exact-count fixed-mixture band

Same as Kill-Test 12.

For observed rank count q,

L_delta(q)
=
max(0, max(0,q-M)/n - epsilon_clean(delta)).

Define

h_delta(q)=2(L_delta(q)-1/2).

Each fixed eta in

{0.05,0.1,0.2,0.4,0.6,0.8,0.95}

uses

e_t = 1 + eta h_delta(q_t).

A 5% constant-one hedge and equal mixture over eta are retained.

## Baseline B — exact-count adaptive ONS band

To avoid handicapping the generic band with a fixed eta grid, add a predictable adaptive bettor:

e_t = 1 + eta_t h_delta(q_t),

with eta_t in [0,0.99].

The next eta is updated by one-dimensional ONS using only past/current information and is projected to [0,0.99]. Since eta_t is predictable and the factor remains nonnegative, the conditional e-process argument is preserved on the DKW-good reference event.

## Baseline C — one-sided CCTM-style ONS

Use the unsmoothed official CCTM update geometry, but project eta to a one-sided nonnegative interval because the frozen alternatives are right shifts.

Audit

D in {0.50,0.90,0.99}.

The upper value remains below 1 so the betting factor is globally nonnegative for u in [0,1].

This is stronger and cleaner than the earlier single D=0.5 choice.

## Static and oracle methods

The static-coupling and oracle predictive-rank mixtures are **unchanged** from corrected Kill-Test 12.

Their threshold remains 1/alpha=20.

## Outputs

Long-form CSV containing, for every K, condition, horizon and baseline configuration:

- method;
- delta;
- D when applicable;
- crossing rate;
- median stopping time among detected paths;
- median log evidence;
- threshold.

The script also prints an oracle-tuned summary at T=200:
- best fixed-mixture band over delta;
- best adaptive-ONS band over delta;
- best CCTM-style configuration over delta and D;
- static coupling;
- oracle.

Tie-breaking for “best baseline” is frozen:
1. highest crossing rate;
2. lower median detection delay;
3. higher median log evidence.

## Decision rule

Primary stress point:

K=32, T=200, gamma=4.

**Strong PASS** if static coupling remains at least 0.15 absolute crossing probability above the strongest oracle-tuned valid baseline configuration.

**Narrow PASS** if the gap is positive but below 0.15, or the advantage exists mainly at K=24 / gamma=8.

**Broad-advantage NO-GO** if the strongest tuned baseline comes within 0.10 of static coupling for both gamma=4 and gamma=8 at K=32.

Regardless of simulation, type-I validity is not inferred from empirical null frequency; it rests on the corresponding theoretical construction.

## After this gate

No more bettor tuning.

If the candidate survives, freeze the method and move to:
1. theorem statements/proofs;
2. prior-art positioning;
3. manuscript v0.1;
4. broader reproducibility experiments only after the paper core is fixed.
