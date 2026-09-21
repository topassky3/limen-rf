# LIMEN-RF paper core — theorem draft v0.1

Date: 2026-09-21

Status: **formalization draft; method frozen after Kill-Test 13**

This document turns the frozen empirical construction into explicit theorem statements and proof obligations. It intentionally separates what is already proved from what still needs manuscript-level verification.

---

## 1. Null model

Let the observed reference bank contain \(K\) cells. There is an unknown clean index set \(G\subseteq\{1,\ldots,K\}\) with

\[
|G|=n=K-m,
\]

and a contaminated index set \(B=G^c\) with \(|B|=m\).

For \(i\in G\),

\[
Y_i\overset{\mathrm{iid}}{\sim}F,
\]

where \(F\) is an unknown continuous distribution.

The future null stream satisfies

\[
X_1,X_2,\ldots\overset{\mathrm{iid}}{\sim}F,
\]

independently of the clean reference variables.

The \(m\) contaminated reference values may be arbitrary, but they are **static/exogenous**: they are fixed before the future stream and may not be selected as a value-adaptive function of the realized clean reference sample.

After sorting the \(K\) observed reference values, let

\[
C^\star\subseteq\{1,\ldots,K\},\qquad |C^\star|=m,
\]

denote the realized sorted positions occupied by contaminated cells.

The positions \(C^\star\) need not be deterministic. The essential assumption is that deleting those realized positions recovers the original iid clean reference sample.

Ties may be excluded by an almost-sure no-tie assumption or handled by a fixed random tie-breaking rule independent of the data.

---

## 2. Observable and reconstructed ranks

Let the sorted observed reference bank be

\[
Z_{(1)}\le\cdots\le Z_{(K)}.
\]

For each future observation define the observable full-reference rank

\[
Q_t
=
\#\{i:Z_{(i)}\le X_t\}
\in\{0,\ldots,K\}.
\]

For a candidate sorted contamination-position set

\[
C\subseteq\{1,\ldots,K\},\qquad |C|=m,
\]

define the candidate clean rank

\[
R_t^{(C)}
=
Q_t-\#\{c\in C:c\le Q_t\}.
\]

For the true realized set \(C^\star\),

\[
R_t^{(C^\star)}
=
\#\{i\in G:Y_i\le X_t\}.
\]

Thus the true candidate exactly reconstructs the rank of \(X_t\) relative to the iid clean reference sample.

This identity is pathwise.

---

## 3. Theorem 1 — exact clean predictive-rank law

### Statement

Let

\[
R_t=\#\{i=1,\ldots,n:Y_i\le X_t\}\in\{0,\ldots,n\},
\]

where

\[
Y_1,\ldots,Y_n,X_1,X_2,\ldots
\]

are iid from an unknown continuous distribution \(F\).

Define

\[
N_{j,t-1}
=
\sum_{s=1}^{t-1}\mathbf 1\{R_s=j\}.
\]

Then for every \(t\ge1\) and \(j\in\{0,\ldots,n\}\),

\[
\Pr(R_t=j\mid R_1,\ldots,R_{t-1})
=
\frac{N_{j,t-1}+1}{n+t}.
\]

The law is distribution-free: it does not depend on \(F\).

### Proof

Apply the probability integral transform:

\[
U_i=F(Y_i),\qquad V_t=F(X_t).
\]

Because \(F\) is continuous,

\[
U_1,\ldots,U_n,V_1,V_2,\ldots
\overset{\mathrm{iid}}{\sim}\mathrm{Unif}(0,1).
\]

Let

\[
0=U_{(0)}<U_{(1)}<\cdots<U_{(n)}<U_{(n+1)}=1
\]

and define the \(n+1\) spacings

\[
P_j=U_{(j+1)}-U_{(j)},\qquad j=0,\ldots,n.
\]

The uniform-spacing vector satisfies

\[
(P_0,\ldots,P_n)\sim\mathrm{Dirichlet}(1,\ldots,1).
\]

Conditional on \(P=(P_0,\ldots,P_n)\),

\[
R_1,R_2,\ldots\mid P
\overset{\mathrm{iid}}{\sim}\mathrm{Categorical}(P).
\]

After observing rank counts \(N_{j,t-1}\), Dirichlet conjugacy gives

\[
P\mid R_{1:t-1}
\sim
\mathrm{Dirichlet}
(1+N_{0,t-1},\ldots,1+N_{n,t-1}).
\]

Therefore

\[
\Pr(R_t=j\mid R_{1:t-1})
=
\mathbb E[P_j\mid R_{1:t-1}]
=
\frac{N_{j,t-1}+1}
{(n+1)+(t-1)}
=
\frac{N_{j,t-1}+1}{n+t}.
\]

QED.

### Important interpretation

This is a **marginal fixed-reference** guarantee over the random reference sample. Conditional on the realized reference values, the rank probabilities are the realized spacing probabilities \(P_j\), not generally \((N_j+1)/(n+t)\).

The martingale filtration used below is therefore the predictive-rank filtration, not a filtration that conditions on the full numerical reference vector.

---

## 4. Theorem 2 — candidate-wise predictive-rank martingale

### Statement

Let

\[
\mathcal G_t=\sigma(R_1,\ldots,R_t)
\]

be the clean predictive-rank filtration.

At time \(t\), let

\[
q_t=(q_{t,0},\ldots,q_{t,n})
\]

be any \(\mathcal G_{t-1}\)-measurable probability vector:

\[
q_{t,j}\ge0,\qquad
\sum_{j=0}^{n}q_{t,j}=1.
\]

Define the null predictive probabilities

\[
p_{t,j}
=
\frac{N_{j,t-1}+1}{n+t}
\]

and the one-step factor

\[
e_t
=
\frac{q_{t,R_t}}{p_{t,R_t}}.
\]

Let

\[
E_0=1,\qquad
E_t=\prod_{s=1}^{t}e_s.
\]

Then \((E_t)_{t\ge0}\) is a nonnegative martingale under the null, and hence an e-process with respect to \((\mathcal G_t)\).

### Proof

By Theorem 1,

\[
\Pr(R_t=j\mid\mathcal G_{t-1})=p_{t,j}.
\]

Therefore

\[
\mathbb E[e_t\mid\mathcal G_{t-1}]
=
\sum_{j=0}^{n}
p_{t,j}
\frac{q_{t,j}}{p_{t,j}}
=
\sum_{j=0}^{n}q_{t,j}
=
1.
\]

Hence

\[
\mathbb E[E_t\mid\mathcal G_{t-1}]
=
E_{t-1},
\]

so \(E_t\) is a nonnegative martingale with \(E_0=1\).

QED.

---

## 5. Corollary 2.1 — convex wealth mixtures remain valid

Suppose \(E_t^{(h)}\), \(h=1,\ldots,H\), are candidate-wise nonnegative martingales constructed as in Theorem 2, and let

\[
w_0,w_1,\ldots,w_H\ge0,
\qquad
w_0+\sum_{h=1}^{H}w_h=1.
\]

Define

\[
E_t^{\mathrm{mix}}
=
w_0+\sum_{h=1}^{H}w_hE_t^{(h)}.
\]

Then \(E_t^{\mathrm{mix}}\) is a nonnegative martingale with initial value one.

This formally covers the frozen LIMEN-RF mixture:
- constant-one hedge \(w_0=0.05\);
- fixed Beta-rank components;
- symmetric Dirichlet predictive components;
- upper-tilted Dirichlet predictive components.

No special property of those particular alternatives is required for validity beyond predictability and normalization.

---

## 6. Theorem 3 — robust anytime crossing control under static contamination

### Statement

Let

\[
\mathcal C_m
=
\{C\subseteq\{1,\ldots,K\}:|C|=m\}.
\]

For every candidate \(C\in\mathcal C_m\), compute a candidate evidence process

\[
E_t^{(C)}
\]

by applying the same valid predictive-rank betting construction to the reconstructed sequence

\[
R_1^{(C)},\ldots,R_t^{(C)}.
\]

Define the robust lower envelope

\[
\underline E_t
=
\min_{C\in\mathcal C_m}E_t^{(C)}.
\]

Under the static/exogenous replacement null model of Section 1, for every \(\alpha\in(0,1)\),

\[
\Pr_{H_0}
\left(
\sup_{t\ge0}\underline E_t\ge\frac1\alpha
\right)
\le\alpha.
\]

### Proof

For the true realized sorted contamination positions \(C^\star\),

\[
R_t^{(C^\star)}
=
\#\{i\in G:Y_i\le X_t\}.
\]

Thus \(E_t^{(C^\star)}\) is exactly the clean predictive-rank martingale from Theorem 2 (or Corollary 2.1 for the frozen mixture).

By definition of the lower envelope,

\[
\underline E_t
\le
E_t^{(C^\star)}
\qquad\text{for every }t
\]

on every sample path.

Therefore

\[
\left\{
\sup_t\underline E_t\ge1/\alpha
\right\}
\subseteq
\left\{
\sup_tE_t^{(C^\star)}\ge1/\alpha
\right\}.
\]

Ville's inequality for the nonnegative martingale \(E_t^{(C^\star)}\) gives

\[
\Pr
\left(
\sup_tE_t^{(C^\star)}\ge1/\alpha
\right)
\le\alpha.
\]

Combining the two displays proves the result.

QED.

### Terminology guardrail

The theorem proves **anytime-valid threshold crossing control** for \(\underline E_t\).

It does **not** prove that

\[
(\underline E_t)_{t\ge0}
\]

is itself a martingale, supermartingale, or e-process.

The manuscript should call it an **anytime-valid robust evidence lower envelope** or **anytime-valid robust crossing construction**, unless a stronger process property is separately established.

---

## 7. Why the random sorted contamination positions do not invalidate Theorem 3

The physical contaminated cell identities may be fixed before sampling while their locations after sorting are random.

This causes no random-selection problem in Theorem 3.

For whichever sorted position set \(C^\star\) is realized,

\[
R_t^{(C^\star)}
\]

is the same canonical clean-reference rank

\[
\#\{i\in G:Y_i\le X_t\}.
\]

Hence \(E_t^{(C^\star)}\) is not an arbitrary post-selected member of unrelated martingales. It is a representation of the single clean-rank martingale through the realized sorted contamination map.

This distinction should be made explicit in the paper.

---

## 8. Proposition 4 — candidate sets are contiguous partitions of observed-rank bins

The observable rank \(Q_t\) takes values in

\[
\{0,\ldots,K\},
\]

which defines \(K+1\) observed-rank bins.

Deleting one sorted reference at position \(c\) merges the two adjacent observed-rank bins

\[
c-1
\quad\text{and}\quad
c.
\]

Therefore deleting a candidate set \(C\) of \(m\) sorted positions is equivalent to deleting \(m\) boundaries among the \(K+1\) observed-rank bins.

Equivalently, every candidate \(C\) induces a contiguous partition of the \(K+1\) observed-rank bins into

\[
K-m+1=n+1
\]

candidate clean-rank groups.

This gives the combinatorial structure exploited by the Kill-Test 08 dynamic program.

---

## 9. Proposition 5 — closed form and DP for a fixed categorical bettor

This proposition applies to **one fixed categorical alternative**
\(a=(a_0,\ldots,a_n)\), not automatically to the full frozen wealth mixture.

Let

\[
H_q(t)
=
\sum_{s=1}^{t}\mathbf 1\{Q_s=q\}
\]

be the observable rank histogram.

For a candidate \(C\), let

\[
N_j^{(C)}(t)
\]

be the histogram obtained after merging observed bins according to the candidate partition.

For the fixed categorical alternative \(q_t\equiv a\),

\[
\log E_t^{(C)}
=
\log\Gamma(n+t+1)-\log\Gamma(n+1)
+
\sum_{j=0}^{n}
\left[
N_j^{(C)}(t)\log a_j
-
\log\Gamma(N_j^{(C)}(t)+1)
\right].
\]

### Derivation

Starting from

\[
E_t^{(C)}
=
\prod_{s=1}^{t}
\frac{a_{R_s^{(C)}}}
{(N_{R_s^{(C)},s-1}^{(C)}+1)/(n+s)},
\]

the numerator groups by final candidate-rank counts:

\[
\prod_{s=1}^{t}a_{R_s^{(C)}}
=
\prod_{j=0}^{n}a_j^{N_j^{(C)}(t)}.
\]

The denominator count terms give

\[
\prod_{j=0}^{n}N_j^{(C)}(t)!,
\]

while

\[
\prod_{s=1}^{t}(n+s)
=
\frac{\Gamma(n+t+1)}{\Gamma(n+1)}.
\]

Taking logs yields the stated expression.

Because the candidate objective is additive over contiguous merged segments, the minimum over \(C\) can be computed by the dynamic program already verified against brute force in Kill-Test 08, in approximately

\[
O(Km^2)
\]

time and \(O(Km)\) memory for fixed \(m\).

### Scope warning

The current frozen method uses a convex mixture of multiple wealth processes. The candidate objective then contains a log-sum-exp across component wealths and is no longer the same additive segment objective.

Therefore the polynomial DP above is **not yet a theorem for the complete frozen mixture**.

The paper must either:
1. present the DP only as a structural result for fixed categorical bettors; or
2. derive a new exact optimization for the mixture before claiming polynomial-time robust minimization for the full method.

No such stronger claim is currently frozen.

---

## 10. Model boundary — value-adaptive replacement is not covered

Suppose instead that one first draws \(K\) iid clean references, then an adversary observes their values and chooses which cells to replace.

The surviving clean subset can be selection-biased.

In that model, deleting the true contaminated cells need not leave an iid reference sample distributed as \(F\).

Consequently Theorem 1 cannot simply be inserted into Theorem 3.

This is the previously identified Model B and is outside the frozen paper-core theorem.

Generic ECDF perturbation bounds remain safer in that stronger model.

---

## 11. Known-\(m\) versus upper bound \(M\)

The frozen implementation and experiments assume the contamination count \(m=M\) is known.

A possible theoretical extension for only a known upper bound \(m\le M\) is to include candidate sets of every size

\[
0\le r\le M
\]

and form a lower envelope over the corresponding size-specific valid processes.

However, each size has a different clean-reference count \(n=K-r\) and therefore a different predictive null law.

This extension is plausible by the same pathwise-domination argument because the true size is included, but it is **not part of the frozen experimental method** and should be stated as a corollary only after writing the details carefully.

---

## 12. Finite-reference information ceiling

For fixed clean-reference size \(n\), the predictive-rank sequence has the de Finetti representation

\[
P\sim\mathrm{Dirichlet}(1,\ldots,1),
\qquad
R_t\mid P\overset{\mathrm{iid}}{\sim}\mathrm{Categorical}(P).
\]

Thus a long future stream learns the realized random spacing vector \(P\).

This means that some alternative predictive distributions can be statistically indistinguishable from rare but valid null spacing realizations when \(n\) is fixed.

Therefore no asymptotic consistency claim is made here.

A separate theorem would be required to characterize:
- which alternatives yield unbounded evidence for fixed \(n\);
- which yield only a finite Bayes-factor limit;
- what happens when \(n\to\infty\) jointly with \(t\).

The manuscript should frame the current contribution as **finite-reference anytime-valid robustness**, not asymptotic universal consistency.

---

## 13. Current theorem status

### Essentially complete modulo exposition / primary-source attribution

- Theorem 1: exact clean predictive-rank law.
- Theorem 2: candidate-wise martingale for predictable normalized betting distributions.
- Corollary 2.1: convex wealth mixtures.
- Theorem 3: robust anytime crossing control by pathwise domination.
- Proposition 4: contamination positions as contiguous partitions.
- Proposition 5: fixed-categorical closed form and DP scope.

### Still requiring deliberate proof work

- rigorous upper-bound-only \(m\le M\) corollary, if desired;
- any polynomial-time optimization theorem for the full frozen mixture;
- finite-reference power/asymptotic characterization;
- manuscript-level primary-source attribution for predictive-rank martingales and CCTM comparisons.

---

## 14. Paper-core theorem stack

The manuscript should be organized around the following logical chain:

\[
\boxed{
\text{iid clean reference}
\Longrightarrow
\text{Dirichlet predictive ranks}
}
\]

\[
\boxed{
\text{predictable normalized betting}
\Longrightarrow
\text{candidate-wise martingale}
}
\]

\[
\boxed{
\text{true static candidate is among all candidates}
\Longrightarrow
\underline E_t\le E_t^{(C^\star)}
}
\]

\[
\boxed{
\text{Ville}
\Longrightarrow
\Pr\!\left(\sup_t\underline E_t\ge1/\alpha\right)\le\alpha.
}
\]

The empirical contribution then studies the finite-reference price of the robust lower envelope relative to the oracle and to generic confidence-band robustifications.

This is the current paper core.
