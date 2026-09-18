# P−1 Kill-Test 09 — adaptive-mixture repair

Status: **frozen computational power gate**

Date: 2026-09-18

## Goal

Kill-Test 08 showed that the exact dynamic program works, but the robust minimum built from one fixed Beta-rank alternative has almost no power. This gate tests the specific explanation that the failure is caused by numerator/bettor mismatch rather than a fundamental identifiability barrier.

The model remains the static/exogenous contamination model: K=8 observed references, exactly M=2 fixed contaminant positions, n=6 clean i.i.d. references from an unknown continuous F, and future null observations from F.

## Null predictive law

For candidate contamination set C, transform observable rank Q_t into

R_t^(C) = Q_t - #{c in C : c <= Q_t}.

If C is the true contamination set and N_j,t-1 is the previous count of transformed rank j, then

P(R_t=j | history) = (N_j,t-1 + 1)/(n+t).

## Repair A: finite one-sided mixture

Use fixed Beta-rank categorical alternatives for

Gamma = {1.25, 1.5, 2, 3, 4, 6, 8, 12}.

Each component uses e_t = q_t(R_t)/p0_t(R_t), so under the true C it has conditional mean one.

## Repair B: adaptive Dirichlet predictors

Also use predictable categorical forecasts

q_t(j) = (N_j,t-1 + alpha_j)/(t-1 + sum alpha).

The family contains symmetric alpha values 0.1, 0.25 and 0.5, plus upper-rank tilted Dirichlet priors. For total concentration A in {1.0, 3.5, 7.0} and beta in {0.5, 1, 2, 4},

alpha_j = A exp(beta j/n) / sum_l exp(beta l/n).

These components adapt to the transformed rank distribution instead of committing to one fixed shift magnitude.

## Candidate mixture

Reserve weight 0.05 for the constant process E=1 and distribute the remaining 0.95 equally over all alternative components.

For each candidate C,

E_t^(C,mix) = 0.05 + sum_h w_h E_t,h^(C).

For the true C this is a convex mixture of e-processes and is therefore valid.

The robust evidence is

E_t^rob = min_C E_t^(C,mix).

Since E_t^rob <= E_t^(C*,mix) pathwise for the true contamination set C*, crossing 1/alpha remains anytime-valid, even though the minimum process itself need not be a martingale.

## Frozen Monte Carlo gate

- alpha = 0.05
- K = 8
- M = 2
- horizons T = 40, 100, 200
- null stream Uniform(0,1)
- alternatives Beta(gamma_true,1), gamma_true = 2, 4, 8
- two fixed high contaminants
- exact M known
- 200 repetitions per scenario
- seed 20260918

Record robust and oracle crossing fractions, median maximum log evidence, median final log evidence, and the modal contamination candidate attaining the final robust minimum.

## Decision

CONTINUE only if robust power becomes materially nonzero, increases with signal strength and/or horizon, and null crossing remains controlled.

NO-GO if robust crossing remains essentially zero for gamma_true 4 and 8 even after the adaptive mixture. That would make bettor mismatch an implausible explanation and point toward a composite-null identifiability barrier.

No hardware is involved.
