# LIMEN-RF manuscript v0.1 — Sections 4 and 5

Date: 2026-09-21

Status: **frozen experimental design + first results draft**

Working title:

# Anytime-Valid Predictive-Rank Detection with a Statically Contaminated Reference Set

---

# 4. Experimental Design

## 4.1 Purpose of the experiments

The experiments are designed to answer a finite-reference question rather than to establish validity empirically.

The validity guarantee follows from Theorem 1. Simulation is used instead to measure how much detection power is lost when the contaminated reference identities are unknown, and whether exploiting their persistent structure can retain more power than generic confidence-band robustification.

Three comparisons are central:

1. **Static-coupling method:** the proposed lower envelope over candidate contamination-position sets.
2. **Oracle:** the same predictive-rank betting construction applied after revealing the true contaminated positions.
3. **Confidence-band baselines:** conservative robustifications that discard persistent identity information and instead represent the contaminated reference through simultaneous bounds on the unknown null CDF.

The oracle quantifies the cost of not knowing the contamination identities. The confidence-band methods quantify the cost of replacing persistent combinatorial uncertainty by generic distributional uncertainty.

---

## 4.2 Data-generating model

The final frozen comparisons use

\[
K\in\{24,32\}
\]

observed reference values with exactly

\[
m=2
\]

static contaminated observations.

Thus the clean reference size is

\[
n=K-2.
\]

The clean reference values are iid

\[
Y_i\sim\mathrm{Uniform}(0,1).
\]

The two contaminated values are fixed at the high value

\[
Y_{\mathrm{bad}}=2.
\]

This choice makes the contaminated cells persistently occupy the extreme upper tail of the observed reference bank while keeping them outside the support of both the clean null and the simulated alternatives.

Under the null,

\[
X_t\sim\mathrm{Uniform}(0,1).
\]

Under the alternatives,

\[
X_t\sim\mathrm{Beta}(\gamma,1),
\qquad
\gamma\in\{2,4,8\}.
\]

The parameter \(\gamma\) controls the strength of an upper-tail shift:

- \(\gamma=2\): weak/moderate shift;
- \(\gamma=4\): primary moderate-shift stress point;
- \(\gamma=8\): strong shift.

The maximum horizon is

\[
T=200,
\]

with intermediate reporting horizons

\[
T\in\{40,100,200\}.
\]

The target anytime crossing level is

\[
\alpha=0.05.
\]

All methods are evaluated on identical simulated paths within each condition.

---

## 4.3 Proposed static-coupling method

For each path, the observed reference bank is sorted and every candidate set

\[
C\subseteq\{1,\ldots,K\},
\qquad
|C|=2,
\]

is considered.

For each candidate, the observed full-reference rank sequence \(Q_t\) is mapped to candidate clean ranks

\[
R_t^{(C)}
=
Q_t
-
\#\{c\in C:c\le Q_t\}.
\]

A fixed predictive-rank betting portfolio is applied to each candidate sequence.

The robust evidence statistic is

\[
\underline E_t
=
\min_{|C|=2} E_t^{(C)}.
\]

A detection occurs when

\[
\underline E_t\ge \frac1\alpha=20.
\]

The method and betting portfolio were frozen before the final baseline-strength audit.

---

## 4.4 Oracle benchmark

The oracle is given the true contaminated sorted positions \(C^\star\).

It applies the same predictive-rank betting portfolio directly to

\[
R_t^{(C^\star)}.
\]

Its threshold is also

\[
20.
\]

The oracle is not implementable in the target problem and is included only to quantify how much power is lost because the contamination identities are unknown.

---

## 4.5 Confidence-band baselines

The comparison baselines deliberately avoid using persistent contamination identities.

Let

\[
q(x)
=
\#\{\text{all }K\text{ observed references}\le x\}.
\]

Because exactly \(m\) observed references are arbitrary replacements, the unknown clean count below \(x\) satisfies

\[
\max\{0,q(x)-m\}
\le
q_{\mathrm{clean}}(x)
\le
\min\{n,q(x)\}.
\]

For a clean DKW confidence radius

\[
\epsilon_n(\delta)
=
\sqrt{
\frac{\log(2/\delta)}{2n}
},
\]

the exact-count lower confidence bound used in the experiments is

\[
L_\delta(x)
=
\max
\left\{
0,
\frac{\max(0,q(x)-m)}{n}
-
\epsilon_n(\delta)
\right\}.
\tag{14}
\]

A second comparator widens the observed-reference ECDF uncertainty symmetrically. Since

\[
\widetilde F_K
=
\frac nK\widehat F_{\mathrm{clean}}
+
\frac mK\widehat F_{\mathrm{bad}},
\]

the clean DKW event implies

\[
|\widetilde F_K(x)-F(x)|
\le
\epsilon_{\mathrm{sym}}(\delta)
=
\frac nK\epsilon_n(\delta)
+
\frac mK.
\tag{15}
\]

Equation (15) is inserted into a one-sided CCTM-style betting geometry.

These contaminated-reference confidence-band procedures are comparison constructions derived for this study. They are not algorithms claimed by Shaer et al. for contaminated calibration data.

---

## 4.6 Final baseline-strength audit

To avoid comparing the proposed method with a weakly chosen baseline configuration, the final audit evaluates a deliberately favorable parameter grid for the confidence-band methods.

The confidence-budget grid is

\[
\delta
\in
\{
0.005,
0.010,
0.015,
0.020,
0.025,
0.030,
0.035,
0.040,
0.045
\}.
\]

For a target marginal level \(\alpha=0.05\), each confidence-band configuration uses the internal crossing level

\[
a(\delta)
=
\frac{\alpha-\delta}{1-\delta},
\qquad
\delta<\alpha,
\tag{16}
\]

and therefore threshold

\[
1/a(\delta).
\]

This follows from the conservative marginal bound

\[
a(1-\delta)+\delta
\le
\alpha.
\]

Three baseline families are evaluated.

### Band mixture

The lower confidence signal is converted to

\[
h_t
=
2\left(L_\delta(X_t)-\frac12\right).
\]

The one-step factor is

\[
1+\eta h_t
\]

for a fixed mixture over

\[
\eta
\in
\{0.05,0.10,0.20,0.40,0.60,0.80,0.95\},
\]

together with a \(5\%\) constant-one hedge.

### Band ONS

The same lower-confidence signal is used with a predictable one-dimensional online Newton step update for

\[
\eta_t\in[0,0.99].
\]

This baseline was introduced specifically to avoid handicapping the confidence-band approach with a fixed betting grid.

### CCTM-style ONS

The symmetric radius in (15) is used in a one-sided unsmoothed CCTM-style betting factor with

\[
D\in\{0.50,0.90,0.99\}.
\]

The betting parameter is projected to the nonnegative interval \([0,D]\), consistent with the right-shift alternatives studied here.

---

## 4.7 Oracle-tuned baseline envelope

For each simulated condition, the strongest baseline configuration is selected **after the experiment** from the frozen \((\delta,D)\) grid.

This best-grid baseline is intentionally favorable to the confidence-band family.

It is important that the resulting envelope is **not itself a single precommitted level-\(\alpha\) test**. Each individual grid configuration has its own valid threshold; selecting the best configuration ex post is used only as an adversarial descriptive benchmark.

Consequently, the comparison asks a stronger descriptive question:

> Does the proposed method retain an advantage even relative to the best confidence-band configuration selected after observing the simulation condition?

The answer is not interpreted as a new testing procedure and is not used in the validity theorem.

---

## 4.8 Monte Carlo protocol

The final baseline-strength audit uses

\[
200
\]

Monte Carlo paths per condition with seed

\[
20260918.
\]

All methods are evaluated on the same path realization within each replication.

The principal reported metrics are:

1. **crossing probability by horizon**
   \[
   \widehat P(\tau\le T);
   \]
2. **median detection delay among detected paths**;
3. **median terminal log evidence**, used only as a diagnostic.

Detection delay is conditional on detection and therefore can be selection-biased when one method detects only a small fraction of paths.

Terminal log evidence is also not directly comparable across all methods because the confidence-band threshold depends on \(\delta\), while the static and oracle thresholds equal 20.

The primary comparison metric is therefore crossing probability, with conditional delay as a secondary descriptive metric.

---

## 4.9 Frozen primary decision point

Before executing the final audit, the primary stress point was fixed as

\[
K=32,\qquad
\gamma=4,\qquad
T=200.
\]

A strong empirical pass was defined as

\[
\widehat P_{\mathrm{static}}
-
\widehat P_{\mathrm{strongest\ tuned\ baseline}}
\ge
0.15.
\tag{17}
\]

No bettor or detector tuning was permitted after this decision rule was evaluated.

---

# 5. Results

## 5.1 Null sanity check

At horizon \(T=200\), the observed null crossing probabilities for the proposed method are

\[
0.020
\quad\text{for }K=24
\]

and

\[
0.015
\quad\text{for }K=32.
\]

The oracle null crossing probabilities are \(0.060\) and \(0.040\), respectively.

These finite Monte Carlo estimates do not establish type-I validity. The theorem provides the validity guarantee. Their role is only to check that the implementation does not show an obvious contradiction with the nominal level

\[
\alpha=0.05.
\]

No such contradiction is observed.

---

## 5.2 Final crossing probabilities at \(T=200\)

Table 1 summarizes the final frozen Kill-Test 13 comparison.

### Table 1. Crossing probability by \(T=200\)

| \(K\) | Condition | Static coupling | Strongest tuned confidence-band baseline | Oracle |
|---:|---|---:|---:|---:|
| 24 | null | 0.020 | 0.000 | 0.060 |
| 24 | \(\mathrm{Beta}(2,1)\) | 0.225 | 0.000 | 0.495 |
| 24 | \(\mathrm{Beta}(4,1)\) | 0.880 | 0.005 | 0.965 |
| 24 | \(\mathrm{Beta}(8,1)\) | 1.000 | 0.340 | 1.000 |
| 32 | null | 0.015 | 0.000 | 0.040 |
| 32 | \(\mathrm{Beta}(2,1)\) | 0.195 | 0.000 | 0.425 |
| 32 | \(\mathrm{Beta}(4,1)\) | 0.935 | 0.170 | 0.995 |
| 32 | \(\mathrm{Beta}(8,1)\) | 1.000 | 0.840 | 1.000 |

For \(K=24\), the strongest tuned confidence-band baseline at \(\gamma=4\) is the band mixture with crossing probability \(0.005\). At \(\gamma=8\), band ONS reaches \(0.340\).

For \(K=32\), the strongest tuned baseline at both \(\gamma=4\) and \(\gamma=8\) is the fixed band mixture, with crossing probabilities \(0.170\) and \(0.840\), respectively.

---

## 5.3 Primary moderate-shift stress point

At the pre-specified primary point

\[
K=32,\qquad
\gamma=4,\qquad
T=200,
\]

the crossing probabilities are

\[
\widehat P_{\mathrm{static}}=0.935,
\]

\[
\widehat P_{\mathrm{best\ band}}=0.170,
\]

and

\[
\widehat P_{\mathrm{oracle}}=0.995.
\]

Therefore the pre-specified static-versus-baseline gap is

\[
0.935-0.170
=
0.765.
\tag{18}
\]

The required strong-pass margin in (17) was \(0.15\).

Thus the observed gap exceeds the frozen margin by

\[
0.615.
\]

Relative to the oracle, the static method retains

\[
\frac{0.935}{0.995}
\approx
0.94
\]

of the observed oracle crossing probability in this scenario.

This ratio is descriptive and is not interpreted as an efficiency theorem.

---

## 5.4 Strong-shift regime

For

\[
K=32,
\qquad
\gamma=8,
\qquad
T=200,
\]

both the proposed method and the oracle cross on every simulated path:

\[
\widehat P_{\mathrm{static}}
=
\widehat P_{\mathrm{oracle}}
=
1.000.
\]

The strongest confidence-band comparator reaches

\[
0.840.
\]

The absolute static-versus-baseline difference is therefore

\[
0.160.
\]

This regime is informative because the confidence-band method is no longer close to vacuous: it has substantial power, yet the static-coupling construction still crosses more frequently.

The smaller gap relative to the \(\gamma=4\) scenario is expected when the signal becomes strong enough for all reasonable methods to approach saturation.

---

## 5.5 Weak-shift limitation

For the weaker alternative

\[
\gamma=2,
\]

the proposed method has substantially less power:

\[
0.225
\quad(K=24)
\]

and

\[
0.195
\quad(K=32).
\]

The oracle reaches \(0.495\) and \(0.425\), respectively.

This is an important limitation.

Unknown contamination identities impose a real finite-reference price, and the frozen betting portfolio does not recover oracle-level sensitivity under weak shifts.

The method is therefore not presented as uniformly powerful across all alternatives.

---

## 5.6 Detection delays

Table 2 reports the median stopping time among paths that cross by \(T=200\).

### Table 2. Median detected delay at \(T=200\)

| \(K\) | Alternative | Static | Best band mix/ONS | CCTM-style | Oracle |
|---:|---|---:|---:|---:|---:|
| 24 | \(\mathrm{Beta}(4,1)\) | 25 | 123 / 131 | not detected | 9 |
| 24 | \(\mathrm{Beta}(8,1)\) | 8 | 90 / 73 | 149 | 5 |
| 32 | \(\mathrm{Beta}(4,1)\) | 13 | 78.5 / 72 | 107 | 8 |
| 32 | \(\mathrm{Beta}(8,1)\) | 7 | 55.5 / 48 | 84.5 | 5 |

At the primary \(K=32,\gamma=4\) point, the proposed method detects with median delay

\[
13,
\]

compared with

\[
78.5
\]

for the strongest crossing-probability band mixture and

\[
8
\]

for the oracle.

The adaptive band ONS has median detected delay \(72\), while the CCTM-style comparator has median delay \(107\).

Because these medians condition on successful detection, they should not be compared independently of the crossing probabilities. In particular, a method that detects only a small selected subset of easy paths can appear artificially fast.

Despite that possible selection effect, the proposed method is substantially faster than the confidence-band methods in the primary scenario.

---

## 5.7 Evidence diagnostics

At the primary \(K=32,\gamma=4,T=200\) point, the median terminal log evidence is

\[
9.309764
\]

for the proposed method and

\[
13.358775
\]

for the oracle.

The strongest band mixture has median log evidence

\[
-1.402095,
\]

band ONS has

\[
-1.601856,
\]

and the CCTM-style method has

\[
-2.160841.
\]

For the strong \(K=32,\gamma=8\) alternative, the corresponding medians are

\[
27.937381
\]

for static coupling,

\[
33.873675
\]

for the oracle,

\[
18.750086
\]

for band mixture,

\[
19.274469
\]

for band ONS, and

\[
5.313818
\]

for CCTM-style betting.

These values are diagnostic only.

The static/oracle threshold equals

\[
20,
\]

whereas tuned confidence-band configurations can have thresholds such as

\[
96
\quad\text{or}\quad
191.
\]

Raw log evidence is therefore not a calibrated cross-method effect-size scale.

---

## 5.8 Effect of baseline tuning

The final audit strengthens the confidence-band comparison in two ways.

First, it allows

\[
\delta
\]

to range over nine pre-specified values instead of fixing a single confidence allocation.

Second, it adds adaptive ONS betting to the exact-count band and allows the CCTM-style betting cap to vary up to

\[
D=0.99.
\]

At \(K=32,\gamma=4,T=200\), the strongest configuration is the band mixture with

\[
\delta=0.040,
\]

crossing probability \(0.170\), and threshold

\[
96.
\]

The strongest band ONS reaches \(0.160\) with

\[
\delta=0.045
\]

and threshold

\[
191.
\]

The CCTM-style comparator reaches \(0.045\) at

\[
\delta=0.040,
\qquad
D=0.99.
\]

At \(K=32,\gamma=8,T=200\), the strongest band mixture reaches \(0.840\) at

\[
\delta=0.045
\]

with threshold \(191\).

Thus the final result does not depend on comparing the static method against only one arbitrarily chosen confidence-band setting.

---

## 5.9 Earlier non-vacuous comparison

Before the final tuning audit, a frozen comparison with

\[
\delta=0.025
\]

already demonstrated that the generic confidence-band methods were non-vacuous at larger reference sizes.

For \(K=32,T=200\),

\[
\gamma=4:
\qquad
0.935
\text{ static},
\quad
0.120
\text{ exact-count band},
\quad
0.010
\text{ CCTM-style},
\quad
0.995
\text{ oracle},
\]

and

\[
\gamma=8:
\qquad
1.000
\text{ static},
\quad
0.735
\text{ exact-count band},
\quad
0.300
\text{ CCTM-style},
\quad
1.000
\text{ oracle}.
\]

This earlier gate is useful because it shows that the observed advantage is not merely an artifact of confidence bands being mathematically unable to cross.

The final audit then confirms that the qualitative conclusion survives substantially more aggressive baseline tuning.

---

## 5.10 Interpretation

The experiments support a finite-reference structural interpretation.

A confidence-band method asks which null CDFs remain compatible with the contaminated reference.

The static-coupling method asks a different question:

> Which single persistent set of contaminated reference identities could have generated the entire repeated rank history?

The latter constraint couples all future observations through the same latent candidate.

The empirical results suggest that this persistent coupling can preserve substantially more usable evidence than a generic simultaneous band, particularly for moderate shifts where the confidence-band methods remain conservative.

The effect should not be interpreted as universal superiority.

The result is specific to:

- a finite reused reference bank;
- exactly two static/exogenous arbitrary replacements;
- the frozen predictive-rank betting portfolio;
- right-shift alternatives studied here;
- the tested confidence-band adaptations.

---

## 5.11 Reproducibility note

The Kill-Test 13 script that generates the final audit is

\[
\texttt{experiments/pminus1\_baseline\_strength\_audit\_killtest13.py}.
\]

The final simulation run used

\[
200
\]

replications and seed

\[
20260918.
\]

The generated CSV is

\[
\texttt{results/pminus1\_killtest13\_baseline\_strength.csv}.
\]

At the time this manuscript section was drafted, the CSV exists in the local experimental workspace but is not committed to the repository branch. Before archival release or journal submission, the frozen result table or the full CSV should be versioned so that every reported value can be reconstructed without rerunning the Monte Carlo experiment.

---

## 5.12 Main empirical conclusion

Within the frozen static-contamination model, the proposed method remains close to the contamination-aware oracle at moderate and strong shifts while substantially outperforming the tested confidence-band robustifications.

The primary observed result is

\[
\boxed{
0.935
\text{ static}
\; \text{vs.} \;
0.170
\text{ strongest tuned band}
\; \text{vs.} \;
0.995
\text{ oracle}
}
\]

at

\[
K=32,\quad
m=2,\quad
\gamma=4,\quad
T=200.
\]

The corresponding median detected delays are

\[
\boxed{
13
\; \text{vs.} \;
78.5
\; \text{vs.} \;
8
}.
\]

These results motivate the interpretation that persistent contamination identities contain finite-reference information that is discarded when contamination is represented only through generic CDF uncertainty.
