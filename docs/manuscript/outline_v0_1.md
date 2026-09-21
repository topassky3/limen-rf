# LIMEN-RF manuscript v0.1 — working outline

Date: 2026-09-21

Status: **paper phase started**

## Working title

**Anytime-Valid Predictive-Rank Detection with a Statically Contaminated Reference Set**

Alternative, more engineering-oriented title:

**Robust Anytime-Valid CFAR-Style Detection from a Statically Contaminated Reference Bank**

Do not freeze the title until the prior-art positioning pass is complete.

## One-sentence contribution

For a fixed reference bank containing an unknown set of static/exogenous contaminated cells, enumerate the possible contamination positions, reconstruct candidate clean predictive ranks, build a valid predictive-rank martingale for each candidate, and use the pointwise lower envelope to obtain finite-sample anytime crossing control while preserving substantially more finite-reference power than generic confidence-band robustification in the frozen experiments.

## Claims allowed in v0.1

1. Exact distribution-free predictive-rank null law for a clean fixed reference bank.
2. Candidate-wise nonnegative martingales from predictable normalized rank betting distributions.
3. Anytime-valid robust threshold crossing under known static contamination count by pathwise domination through the true candidate.
4. Candidate contamination sets correspond to contiguous partitions of observed-rank bins.
5. For a fixed categorical bettor, the candidate minimization has an additive closed form and an \(O(Km^2)\)-type dynamic program.
6. In the frozen simulation family, the robust static-coupling construction retains substantially more finite-reference power and shorter detection delay than the tested generic confidence-band baselines.

## Claims explicitly forbidden in v0.1

- “beats CCTM in general”;
- minimax optimality;
- universal adversarial robustness;
- conditional-on-reference validity unless separately proved;
- asymptotic consistency;
- polynomial-time optimization of the full frozen wealth mixture;
- hardware/RF field validity;
- unknown-\(m\) validity as if experimentally verified.

## Proposed manuscript structure

### 1. Introduction

Motivate sequential detection with a fixed reference bank that can contain a small number of persistent interferers/outliers.

Core distinction:

- generic robustification treats reference uncertainty through a confidence set/band;
- static contamination has persistent latent structure because the same bad cells remain bad over the whole future stream.

Research question:

> Can that persistent structure be used without sacrificing anytime-valid false-alarm control?

State the answer narrowly: yes under the frozen static/exogenous replacement model.

### 2. Related work

Four blocks:

1. classical CA/OS/reference CFAR and contaminated-reference handling;
2. predictive ranks / rank martingales / distribution-free sequential detection;
3. conformal test martingales and fixed-reference CDF uncertainty;
4. robust/composite-null e-processes and contamination models.

This section requires a fresh primary-source citation pass before prose is finalized.

### 3. Problem formulation

Define:
- \(K\) observed reference cells;
- exact contamination count \(m\);
- unknown clean set \(G\);
- iid clean reference values from continuous \(F\);
- iid future null stream from \(F\);
- static/exogenous arbitrary contaminated values;
- sorted contamination-position set \(C^\star\);
- full rank \(Q_t\);
- candidate reconstructed rank \(R_t^{(C)}\).

Clearly contrast this with value-adaptive replacement after observing the clean reference sample.

### 4. Clean predictive ranks

State and prove Theorem 1 using PIT + uniform spacings + Dirichlet conjugacy:

\[
\Pr(R_t=j\mid R_{1:t-1})
=
\frac{N_{j,t-1}+1}{n+t}.
\]

Explain that the guarantee is marginal over the random fixed reference, not conditional on its realized numerical values.

### 5. Candidate-wise sequential evidence

State Theorem 2:

\[
e_t
=
\frac{q_{t,R_t}}{p_{t,R_t}},
\qquad
E_t=\prod_{s\le t}e_s.
\]

For any predictable normalized \(q_t\), \(E_t\) is a nonnegative martingale.

Then state the convex wealth-mixture corollary covering the frozen mixture family.

### 6. Robust static-contamination construction

Define

\[
\underline E_t
=
\min_{|C|=m}E_t^{(C)}.
\]

State Theorem 3:

\[
\Pr_{H_0}
\left(
\sup_t\underline E_t\ge1/\alpha
\right)
\le\alpha.
\]

Proof:
- true candidate reconstructs the clean ranks;
- \(\underline E_t\le E_t^{(C^\star)}\) pathwise;
- apply Ville.

Explicitly state that \(\underline E_t\) itself is not claimed to be an e-process.

### 7. Combinatorial structure

Show:
- each deleted sorted reference removes one boundary between adjacent observed-rank bins;
- a candidate is a contiguous partition;
- for a fixed categorical bettor, candidate log wealth depends only on merged histogram counts;
- derive the dynamic program.

State clearly that the full frozen wealth mixture is currently evaluated by candidate enumeration in the experiments.

### 8. Experimental design

Use only frozen post-firewall settings.

Report:
- \(K\in\{8,16,20,24,32\}\) as appropriate for the progression;
- primary final comparisons \(K=24,32\), \(m=2\);
- null Uniform;
- Beta right-shift alternatives;
- horizons 40/100/200;
- alpha 0.05;
- exact same paths across methods;
- tuned confidence-band adversarial audit from Kill-Test 13.

Separate exploratory development experiments from final frozen comparison.

### 9. Results

Primary table should emphasize Kill-Test 13.

At \(K=32,T=200,\gamma=4\):

- static: crossing 0.935, median detected delay 13;
- strongest tuned generic band: crossing 0.170, delay 78.5;
- oracle: crossing 0.995, delay 8.

At \(K=32,T=200,\gamma=8\):

- static: 1.000, delay 7;
- strongest tuned generic band: 0.840, delay 55.5;
- oracle: 1.000, delay 5.

Also report weak-shift \(\gamma=2\) as a limitation.

### 10. Discussion

Interpret the result as a finite-reference structural advantage:
persistent contamination identities couple all future observations, whereas a generic simultaneous band deliberately discards that latent identity information.

Discuss:
- robustness-efficiency gap to oracle;
- finite-reference information ceiling;
- marginal versus conditional validity;
- exact-\(m\) assumption;
- Model A versus value-adaptive Model B;
- computational cost of the full mixture.

### 11. Conclusion

Keep the conclusion narrow.

Suggested core conclusion:

> Static reference contamination can be treated as a persistent latent combinatorial structure rather than only as pointwise CDF uncertainty. Under an exogenous bounded-replacement model, candidate-wise predictive ranks yield finite-sample anytime crossing control and can retain substantial finite-reference detection power.

## Figures/tables for v0.1

1. Diagram: observed contaminated reference bank -> candidate deletion -> reconstructed ranks -> candidate martingales -> lower envelope.
2. Table: theorem assumptions and guarantees.
3. Table: primary Kill-Test 13 power + delay results.
4. Figure: crossing probability versus horizon for \(K=32\), gamma 4 and 8.
5. Figure: static/oracle/baseline median detection delay.
6. Small table: scope boundaries (Model A covered / Model B not covered).

## Immediate next tasks

1. primary-source verification of the predictive-rank theorem attribution and exact relationship to Kuang-Xia;
2. primary-source verification of the CCTM guarantee and correct way to describe our contamination-widened adaptation;
3. convert theorem draft into manuscript notation;
4. generate the first Results tables/figures directly from frozen CSV outputs;
5. draft Abstract + Introduction only after the novelty wording is verified.
