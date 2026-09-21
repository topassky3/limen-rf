# LIMEN-RF manuscript v0.1 — Sections 2 and 3

Date: 2026-09-21

Status: **first formal manuscript draft after Abstract + Introduction**

Working title:

# Anytime-Valid Predictive-Rank Detection with a Statically Contaminated Reference Set

---

# 2. Problem Formulation and Predictive-Rank Background

## 2.1 Fixed reference with static contamination

Let the observed reference bank contain \(K\) scalar observations. We assume that exactly \(m\) of these observations are contaminated and that the remaining

\[
n=K-m
\]

are clean.

Let

\[
G\subseteq\{1,\ldots,K\},
\qquad |G|=n,
\]

denote the unknown set of clean physical reference-cell identities, and let

\[
B=G^c,
\qquad |B|=m,
\]

denote the contaminated physical cells.

For every \(i\in G\), the clean reference observation satisfies

\[
Y_i\overset{\mathrm{iid}}{\sim}F,
\]

where \(F\) is an unknown continuous distribution. The online null stream satisfies

\[
X_1,X_2,\ldots\overset{\mathrm{iid}}{\sim}F,
\]

independently of the clean reference observations.

The contaminated observations \(\{Y_i:i\in B\}\) may take arbitrary values. We assume, however, that the contamination is **static and exogenous**: the contaminated physical cells are fixed before online monitoring begins, and the surviving clean sample is not selected adaptively after inspecting the realized clean values.

This distinction is essential. The present theory does not cover a stronger adversarial model in which one first draws \(K\) clean iid observations and then chooses which realized observations to replace after inspecting their values. Such selection can bias the surviving clean subset and invalidate the predictive-rank law recalled below.

We further assume continuity of \(F\), so ties among clean observations and future null observations occur with probability zero. Fixed random tie-breaking independent of the data can be used if ties must be supported in an implementation.

---

## 2.2 Sorted reference representation

Let

\[
Z_{(1)}\le Z_{(2)}\le\cdots\le Z_{(K)}
\]

be the sorted observed reference values, including both clean and contaminated observations.

After sorting, the contaminated physical cells occupy an unknown set of sorted positions

\[
C^\star
\subseteq
\{1,\ldots,K\},
\qquad
|C^\star|=m.
\]

The set \(C^\star\) is generally random because its realized sorted positions depend on both the clean reference values and the contaminated values. This randomness is not problematic: deleting the realized positions \(C^\star\) recovers the original iid clean reference sample.

For a new online observation \(X_t\), define its observable rank relative to the complete contaminated bank by

\[
Q_t
=
\#\{i:Z_{(i)}\le X_t\}
\in\{0,\ldots,K\}.
\]

The sequence \(Q_1,Q_2,\ldots\) is observable.

---

## 2.3 Candidate contamination sets and reconstructed ranks

Let

\[
\mathcal C_m
=
\left\{
C\subseteq\{1,\ldots,K\}:|C|=m
\right\}
\]

be the set of all candidate contamination-position sets.

For a candidate \(C\in\mathcal C_m\), define

\[
R_t^{(C)}
=
Q_t
-
\#\{c\in C:c\le Q_t\}.
\tag{1}
\]

The reconstructed value \(R_t^{(C)}\in\{0,\ldots,n\}\) is the rank that would be observed if the candidate positions \(C\) were deleted from the sorted reference bank.

The true candidate has a special property.

### Lemma 1 (true-candidate rank reconstruction)

Under the static/exogenous contamination model,

\[
R_t^{(C^\star)}
=
\#\{i\in G:Y_i\le X_t\}
\qquad
\text{for every }t.
\tag{2}
\]

#### Proof

The full observed rank \(Q_t\) counts every sorted reference observation not exceeding \(X_t\), including both clean and contaminated values. Among those counted observations, exactly

\[
\#\{c\in C^\star:c\le Q_t\}
\]

correspond to contaminated sorted positions. Subtracting that quantity leaves precisely the number of clean references not exceeding \(X_t\). Therefore (2) holds pathwise. \(\square\)

Lemma 1 is the bridge between an observed contaminated reference bank and the clean fixed-reference predictive-rank theory.

---

## 2.4 Clean fixed-reference predictive ranks

We now recall the clean predictive-rank result of Kuang and Xia [KuangXia2026], translated to the \(0,\ldots,n\) rank convention used here.

Consider a clean reference sample

\[
Y_1,\ldots,Y_n
\overset{\mathrm{iid}}{\sim}F
\]

and an independent online null stream

\[
X_1,X_2,\ldots
\overset{\mathrm{iid}}{\sim}F,
\]

where \(F\) is continuous.

Define

\[
R_t
=
\#\{i=1,\ldots,n:Y_i\le X_t\}
\in\{0,\ldots,n\},
\]

and let

\[
N_{j,t-1}
=
\sum_{s=1}^{t-1}
\mathbf 1\{R_s=j\}
\]

be the number of previous online ranks equal to \(j\).

Let

\[
\mathcal G_t
=
\sigma(R_1,\ldots,R_t)
\]

denote the rank-history filtration.

### Known Result 1 (Kuang--Xia predictive law)

Under the clean fixed-reference null,

\[
\Pr(R_t=j\mid\mathcal G_{t-1})
=
p_{t,j}
=
\frac{N_{j,t-1}+1}{n+t},
\qquad
j=0,\ldots,n.
\tag{3}
\]

This law is distribution-free: it does not depend on \(F\).

A convenient derivation uses the probability integral transform. After mapping the clean reference sample through \(F\), the \(n+1\) uniform spacings have a

\[
\mathrm{Dirichlet}(1,\ldots,1)
\]

distribution. Conditional on those spacings, future ranks are iid categorical draws with spacing probabilities. Integrating the spacing vector under its Dirichlet posterior yields (3).

An important distinction is that (3) is a **marginal fixed-reference** predictive law. Conditional on the realized numerical reference values, the rank probabilities are the realized spacing probabilities and are not generally equal to (3). The anytime guarantee used in this work is therefore inherited from the marginal predictive-rank formulation of Kuang and Xia rather than from a conditional-on-reference confidence-band statement.

---

## 2.5 Clean predictive-rank martingales

Kuang and Xia further show that any predictable normalized betting distribution can be compared with the null predictive law in (3).

At time \(t\), let

\[
q_t
=
(q_{t,0},\ldots,q_{t,n})
\]

be a probability vector satisfying

\[
q_{t,j}\ge0,
\qquad
\sum_{j=0}^{n}q_{t,j}=1,
\]

and assume \(q_t\) is measurable with respect to \(\mathcal G_{t-1}\).

Define

\[
e_t
=
\frac{q_{t,R_t}}{p_{t,R_t}}
\tag{4}
\]

and

\[
E_0=1,
\qquad
E_t
=
\prod_{s=1}^{t}e_s.
\tag{5}
\]

### Known Result 2 (Kuang--Xia predictive-rank martingale)

Under the clean null, \((E_t)_{t\ge0}\) is a nonnegative martingale with respect to \((\mathcal G_t)\).

Indeed,

\[
\mathbb E[e_t\mid\mathcal G_{t-1}]
=
\sum_{j=0}^{n}
p_{t,j}
\frac{q_{t,j}}{p_{t,j}}
=
1.
\]

Therefore,

\[
\mathbb E[E_t\mid\mathcal G_{t-1}]
=
E_{t-1}.
\]

Ville's inequality then implies

\[
\Pr_{H_0}
\left(
\sup_{t\ge0}E_t\ge \frac1\alpha
\right)
\le\alpha
\tag{6}
\]

for every \(\alpha\in(0,1)\).

This clean predictive-rank construction is prior work and is used here as a building block.

---

## 2.6 Frozen betting portfolio

The experiments use a fixed convex portfolio of candidate-wise predictive-rank wealth processes. A constant-one hedge receives weight \(0.05\), and the remaining weight is divided among a frozen family containing:

- fixed Beta-rank alternatives with
  \[
  \gamma\in
  \{1.25,1.5,2,3,4,6,8,12\};
  \]
- symmetric Dirichlet predictive alternatives with concentration
  \[
  a\in\{0.1,0.25,0.5\};
  \]
- upper-rank tilted Dirichlet predictive alternatives with total concentration
  \[
  A\in\{1,3.5,7\}
  \]
  and slope
  \[
  \beta\in\{0.5,1,2,4\}.
  \]

If \(E_t^{(h)}\) denotes the wealth of component \(h\), the candidate portfolio is

\[
E_t^{\mathrm{mix}}
=
w_0+\sum_{h=1}^{H}w_hE_t^{(h)},
\qquad
w_0+\sum_{h=1}^{H}w_h=1.
\tag{7}
\]

A fixed convex combination of nonnegative martingales is again a nonnegative martingale. This closure property, and convex PRM portfolios more generally, are not novelty claims of the present paper.

---

# 3. Robust Anytime-Valid Detection under Static Reference Contamination

## 3.1 Candidate-wise evidence processes

For every candidate contamination set \(C\in\mathcal C_m\), apply the clean predictive-rank construction of Section 2.5 to the reconstructed sequence

\[
R_1^{(C)},R_2^{(C)},\ldots.
\]

This produces a candidate wealth process

\[
E_t^{(C)}.
\]

For candidates \(C\neq C^\star\), the reconstructed sequence need not satisfy the clean predictive-rank law, and \(E_t^{(C)}\) is not claimed to be a martingale under the null.

For the true candidate \(C^\star\), however, Lemma 1 shows that the reconstructed sequence is exactly the clean-reference rank sequence. Consequently,

\[
E_t^{(C^\star)}
\]

is a valid nonnegative predictive-rank martingale under the null.

The method therefore does not require every candidate process to be valid. It requires only that the candidate class contain the true static contamination pattern.

---

## 3.2 Robust evidence lower envelope

Define the robust evidence statistic

\[
\underline E_t
=
\min_{C\in\mathcal C_m}
E_t^{(C)}.
\tag{8}
\]

Because \(C^\star\in\mathcal C_m\),

\[
\underline E_t
\le
E_t^{(C^\star)}
\qquad
\text{for every }t
\tag{9}
\]

on every sample path.

Equation (9) is the key robustification step. It uses the persistence of the unknown contamination identities: the same candidate \(C^\star\) explains all future observations.

---

## 3.3 Main theorem

### Theorem 1 (anytime-valid robust crossing under static contamination)

Assume the model of Section 2.1 with exactly \(m\) static/exogenous contaminated reference observations. For every candidate \(C\in\mathcal C_m\), let \(E_t^{(C)}\) be the predictive-rank wealth obtained by applying the same pre-specified valid betting construction to the reconstructed candidate ranks \(R_t^{(C)}\). Define \(\underline E_t\) by (8).

Then, for every \(\alpha\in(0,1)\),

\[
\Pr_{H_0}
\left(
\sup_{t\ge0}
\underline E_t
\ge
\frac1\alpha
\right)
\le
\alpha.
\tag{10}
\]

#### Proof

By Lemma 1,

\[
R_t^{(C^\star)}
=
\#\{i\in G:Y_i\le X_t\}
\]

for every \(t\). Hence \(E_t^{(C^\star)}\) is exactly a clean predictive-rank martingale of the form described in Section 2.5.

By construction,

\[
\underline E_t
=
\min_{C\in\mathcal C_m}E_t^{(C)}
\le
E_t^{(C^\star)}
\]

for every \(t\). Therefore,

\[
\left\{
\sup_{t\ge0}
\underline E_t
\ge
\frac1\alpha
\right\}
\subseteq
\left\{
\sup_{t\ge0}
E_t^{(C^\star)}
\ge
\frac1\alpha
\right\}.
\]

Applying Ville's inequality to the nonnegative martingale \(E_t^{(C^\star)}\) gives

\[
\Pr_{H_0}
\left(
\sup_{t\ge0}
E_t^{(C^\star)}
\ge
\frac1\alpha
\right)
\le
\alpha.
\]

Combining the last two displays proves (10). \(\square\)

---

## 3.4 Interpretation of the guarantee

Theorem 1 establishes an anytime-valid threshold-crossing guarantee for the lower envelope \(\underline E_t\).

It does **not** establish that

\[
(\underline E_t)_{t\ge0}
\]

is itself a martingale, supermartingale, or e-process.

The safe terminology throughout the paper is therefore:

- **anytime-valid robust evidence lower envelope**, or
- **anytime-valid robust crossing construction**.

This distinction matters because a pointwise minimum of martingales need not preserve the martingale or supermartingale property.

The validity argument instead relies on the pathwise domination relation (9) and the fact that the dominating true-candidate process is valid.

---

## 3.5 Why random sorted contamination positions are harmless

Although the contaminated physical-cell identities are fixed before monitoring, their positions after sorting may be random.

This does not create a post-selection problem.

For whichever sorted position set \(C^\star\) is realized,

\[
R_t^{(C^\star)}
\]

is simply another representation of the canonical clean-reference rank

\[
\#\{i\in G:Y_i\le X_t\}.
\]

Thus \(E_t^{(C^\star)}\) is not selected from unrelated martingales after inspecting the online evidence. It is the unique clean predictive-rank process expressed through the realized sorted contamination map.

The lower envelope is conservative precisely because it includes that true representation among all candidates.

---

## 3.6 Persistent partition structure

The observable rank \(Q_t\) takes values in

\[
\{0,\ldots,K\},
\]

which can be viewed as \(K+1\) adjacent observed-rank bins.

Deleting one sorted reference at position \(c\) merges the two adjacent bins

\[
c-1
\quad\text{and}\quad
c.
\]

Therefore deleting a candidate set \(C\) of \(m\) sorted reference positions is equivalent to deleting \(m\) boundaries among the \(K+1\) observed-rank bins.

Every candidate \(C\) consequently induces a contiguous partition of the observed-rank bins into

\[
K-m+1=n+1
\]

candidate clean-rank groups.

The same partition is reused for all \(t\), which is the combinatorial expression of the persistent contamination identities.

---

## 3.7 Fixed-categorical closed form

For clarity, consider first one fixed categorical betting distribution

\[
a=(a_0,\ldots,a_n),
\qquad
a_j>0,
\qquad
\sum_{j=0}^{n}a_j=1.
\]

Let

\[
H_q(t)
=
\sum_{s=1}^{t}
\mathbf 1\{Q_s=q\},
\qquad
q=0,\ldots,K,
\]

be the histogram of observed full-reference ranks up to time \(t\).

For a candidate \(C\), let

\[
N_j^{(C)}(t)
\]

denote the candidate clean-rank histogram obtained by merging the observed-rank bins according to the partition induced by \(C\).

The candidate wealth is

\[
E_t^{(C)}
=
\prod_{s=1}^{t}
\frac{
a_{R_s^{(C)}}
}{
(N_{R_s^{(C)},s-1}^{(C)}+1)/(n+s)
}.
\]

Grouping terms by final candidate-rank counts gives

\[
\log E_t^{(C)}
=
\log\Gamma(n+t+1)
-
\log\Gamma(n+1)
+
\sum_{j=0}^{n}
\left[
N_j^{(C)}(t)\log a_j
-
\log\Gamma(N_j^{(C)}(t)+1)
\right].
\tag{11}
\]

Thus, for a fixed categorical bettor, the candidate objective depends on the online history only through the observed-rank histogram and the contiguous merges induced by \(C\).

---

## 3.8 Dynamic-programming reduction for the fixed-categorical case

Suppose an observed-rank segment

\[
[b,b+\ell-1]
\]

is merged into one candidate clean-rank group. Let

\[
N
=
\sum_{q=b}^{b+\ell-1}H_q(t)
\]

be the total count in that segment.

If the segment is assigned to clean-rank index \(j\), its additive contribution to (11), ignoring constants independent of the partition, is

\[
c(j,b,\ell)
=
N\log a_j
-
\log\Gamma(N+1).
\tag{12}
\]

Let

\[
DP[b,d]
\]

denote the minimum additive cost after consuming the first \(b\) observed-rank bins while deleting \(d\) boundaries. Since consuming \(b\) bins with \(d\) deleted boundaries creates \(b-d\) completed clean-rank groups, the next clean-rank index is

\[
j=b-d.
\]

A segment of length \(\ell\) consumes \(\ell-1\) additional deleted boundaries, yielding the transition

\[
DP[b+\ell,d+\ell-1]
=
\min
\left\{
DP[b+\ell,d+\ell-1],
\;
DP[b,d]
+
c(b-d,b,\ell)
\right\}.
\tag{13}
\]

Because

\[
1\le\ell\le m-d+1,
\]

the fixed-categorical candidate minimization can be computed in approximately

\[
O(Km^2)
\]

time with

\[
O(Km)
\]

memory.

This reduction was verified computationally against exhaustive enumeration in the development experiments.

The full frozen experimental method uses a convex mixture of several wealth processes. The logarithm of that mixture introduces a log-sum-exp term across components, so the additive structure in (11)--(13) does not directly yield the same dynamic program for the complete frozen portfolio. We therefore restrict the polynomial-time claim to the fixed-categorical case.

---

## 3.9 Exact contamination count and scope boundary

The theory and experiments in this manuscript assume that the contamination count \(m\) is known.

If only an upper bound \(M\) were known, one could in principle include candidate sets of every size

\[
0\le r\le M
\]

and construct size-specific predictive-rank processes using

\[
n_r=K-r.
\]

The same pathwise-domination argument suggests that a lower envelope over all sizes would remain valid because the true size and true contamination set are included.

However, the predictive null law changes with \(r\), and this extension was not part of the frozen experiments. We therefore leave unknown-\(m\) adaptation as future work rather than treating it as an established contribution.

Likewise, value-adaptive replacement after observing an originally clean reference sample is outside the present theorem. In that stronger model, the surviving clean subset can be selection-biased and need not satisfy the iid reference assumption required by the clean predictive-rank law.

---

## 3.10 Finite-reference interpretation

For fixed \(n\), the clean predictive-rank process admits the representation

\[
P
\sim
\mathrm{Dirichlet}(1,\ldots,1),
\qquad
R_t\mid P
\overset{\mathrm{iid}}{\sim}
\mathrm{Categorical}(P).
\]

As the online horizon grows, the repeated ranks increasingly reveal the realized random spacing vector \(P\).

This produces a finite-reference information ceiling: some persistent online rank patterns may be compatible with rare but valid realizations of \(P\). Consequently, the present paper does not claim universal asymptotic consistency for fixed \(n\).

Our focus is instead finite-reference anytime validity and the power retained by exploiting persistent contamination identities relative to methods that summarize reference uncertainty only through confidence bands.

---

## 3.11 Summary

The construction can be summarized as

\[
\text{contaminated fixed bank}
\longrightarrow
\text{candidate deletion maps}
\longrightarrow
\text{candidate predictive ranks}
\longrightarrow
\text{candidate PRM wealths}
\longrightarrow
\underline E_t.
\]

The theoretical guarantee relies only on one candidate:

\[
C^\star
\longrightarrow
R_t^{(C^\star)}=R_t^{\mathrm{clean}}
\longrightarrow
E_t^{(C^\star)}
\text{ is a valid PRM}
\longrightarrow
\underline E_t\le E_t^{(C^\star)}
\longrightarrow
\text{anytime crossing control}.
\]

The next section of the manuscript will describe the frozen experimental protocol used to quantify the finite-reference cost of unknown contamination identities and to compare static-candidate coupling with conservative confidence-band robustifications.
