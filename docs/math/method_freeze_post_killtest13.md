# LIMEN-RF Method Freeze — post Kill-Test 13

Date: 2026-09-18

Status: **FROZEN FOR PAPER-CORE FORMALIZATION**

## Frozen statistical core

Model A:
- K fixed observed references;
- exactly M static/exogenous arbitrary replacements;
- remaining n=K-M references iid/exchangeable from an unknown continuous F;
- future null observations iid from the same F;
- contamination identities fixed before the future stream.

Observed full-reference rank:

Q_t = # { observed reference <= X_t }.

For a candidate contamination-position set C of size M, transform

R_t^(C) = Q_t - # { c in C : c <= Q_t }.

Under the true candidate C*, the clean predictive-rank law is the Dirichlet/Pólya predictive law

P(R_t=j | past) = (N_{j,t-1}+1)/(n+t).

For each candidate C, form a convex mixture of pre-frozen normalized alternative predictive distributions and keep a constant-one hedge.

Robust evidence is the pathwise lower envelope

Ebar_t = min_C E_t^(C).

Because the true fixed candidate C* is among the candidates,

Ebar_t <= E_t^(C*)

pathwise. Hence threshold crossing of Ebar is controlled by the true-candidate e-process.

Important terminology:
- the lower envelope need not itself be a supermartingale/e-process;
- call it an anytime-valid robust crossing/evidence construction unless a stronger property is proved.

## Frozen mixture family

- Beta-rank alternatives gamma in {1.25,1.5,2,3,4,6,8,12};
- symmetric Dirichlet predictors alpha in {0.1,0.25,0.5};
- upper-rank tilted Dirichlet predictors with total concentration in {1,3.5,7} and slope in {0.5,1,2,4};
- 5% constant-one hedge.

No further tuning before manuscript v0.1.

## Empirical gate status

Kill-Tests 08–13 establish:
- exact candidate-state DP/exhaustive logic checked;
- fixed-gamma minimum alone can fail badly;
- adaptive mixture repaired power;
- confidence-band baselines become non-vacuous at larger K;
- after aggressive delta/D tuning, static coupling retained a large finite-reference power and delay advantage in the frozen high-contaminant model;
- final descriptive audit found no contradiction.

Primary K=32, gamma=4, T=200 result:
- static crossing 0.935, median detected delay 13;
- strongest tuned baseline crossing 0.170, median detected delay 78.5;
- oracle crossing 0.995, median detected delay 8.

## Scope guardrails

Do not claim:
- superiority over all CCTM/conformal methods;
- optimality;
- asymptotic consistency without a separate proof;
- that the lower envelope is itself an e-process;
- general adversarial robustness beyond the frozen static/exogenous replacement model.

Current defensible thesis:

> Under static bounded replacement contamination of a fixed reference set, exact candidate-wise predictive-rank coupling can retain substantially more finite-reference sequential evidence than generic simultaneous confidence-band robustification.

## Next proof obligations

1. formalize the clean predictive-rank law from exchangeability / Dirichlet spacings;
2. prove candidate-wise e-process validity for any predictable normalized betting distribution;
3. prove robust crossing control by pathwise domination through the true contamination candidate;
4. characterize the candidate-partition representation and polynomial-time dynamic program where applicable;
5. state precisely the contamination model and what changes under value-adaptive replacement selection;
6. analyze finite-reference information limits and avoid unsupported asymptotic claims.
