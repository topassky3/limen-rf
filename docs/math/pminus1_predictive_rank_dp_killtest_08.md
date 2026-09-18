# P−1 Kill-Test 08 — Static-contamination predictive-rank DP

Status: **theorem prototype + computational gate**

Date: 2026-09-18

## Goal

Test whether the static coupling of a fixed contaminated reference set creates a genuinely nontrivial predictive-rank structure that can be exploited more sharply than a generic CDF-band robustification.

This document separates two contamination models that must not be conflated.

### Model A — exogenous/static contaminated cells

After sorting the observed reference values \(Y_{(1)}<\cdots<Y_{(K)}\), there exists a fixed unknown set of positions \(C^\star\subseteq\{1,\ldots,K\}\), \(|C^\star|=m\le M\), such that deleting those entries leaves \(n=K-m\) i.i.d. samples from an unknown continuous null \(F\), independent of the future null stream \(X_1,X_2,\ldots\sim F\).

The contaminant values themselves may be arbitrary and fixed.

This model matches a common CFAR interpretation: some reference cells contain external interference while the remaining cells are ordinary null references.

### Model B — adaptive replacement after seeing a clean reference sample

Start with \(K\) i.i.d. clean references; an adversary observes their values and then chooses which \(m\le M\) entries to replace.

The surviving observed clean subset can then be selection-biased. The exact predictive-rank result below does **not** automatically cover Model B.

A DKW/CDF-band argument remains safer for Model B because replacing at most \(M\) of \(K\) observations changes an ECDF by at most \(M/K\) pathwise.

## Clean fixed-reference predictive ranks

For a clean reference of size \(n\), define

\[
R_t=\#\{i:Y_i\le X_t\}\in\{0,\ldots,n\}.
\]

Under the probability integral transform, the \(n\) clean references divide \([0,1]\) into \(n+1\) random spacings. Their vector has a Dirichlet\((1,\ldots,1)\) law.

After observing clean-rank history \(R_1,\ldots,R_{t-1}\), let

\[
N_{j,t-1}=\sum_{s<t}\mathbf 1\{R_s=j\}.
\]

Then the exact predictive null law is the Pólya-urn formula

\[
\Pr(R_t=j\mid R_{1:t-1})
=
\frac{N_{j,t-1}+1}{n+t},
\qquad j=0,\ldots,n.
\]

This is the structural object exploited by predictive-rank martingales.

## Mapping observed contaminated ranks to a candidate clean rank

Let

\[
Q_t=\#\{i:Y_{(i)}\le X_t\}\in\{0,\ldots,K\}
\]

be the observable rank relative to all \(K\) references.

For a candidate contamination-position set \(C\),

\[
R_t^{(C)}
=
Q_t-\#\{c\in C:c\le Q_t\}.
\]

Deleting a contaminated reference at sorted position \(c\) merges the two adjacent observed-rank bins \(Q=c-1\) and \(Q=c\).

Therefore a fixed contamination pattern corresponds exactly to a contiguous partition of the \(K+1\) observed-rank bins into \(K-m+1\) clean-rank bins.

## Candidate-specific predictive-rank martingale

Fix any strictly positive alternative categorical distribution

\[
a^{(m)}=(a_0,\ldots,a_n),\qquad \sum_j a_j=1.
\]

For candidate \(C\), define

\[
e_t^{(C)}
=
\frac{a^{(m)}_{R_t^{(C)}}}
{(N^{(C)}_{R_t^{(C)},t-1}+1)/(n+t)}
\]

and

\[
E_t^{(C)}=\prod_{s=1}^t e_s^{(C)}.
\]

If \(C=C^\star\), then under Model A \(E_t^{(C^\star)}\) is a nonnegative martingale under \(H_0\).

A convenient one-sided family for experiments is the rank law induced by \(U\sim\mathrm{Beta}(\gamma,1)\), \(\gamma>1\):

\[
a_j^{(m)}
=
\binom{n}{j}\gamma B(j+\gamma,n-j+1).
\]

This is only a diagnostic alternative family; it is not part of the validity theorem.

## Robust evidence by static coupling

Define

\[
\underline E_t
=
\min_{\substack{C\subseteq\{1,\ldots,K\}\\|C|\le M}}
E_t^{(C)}.
\]

For the true fixed contamination set \(C^\star\),

\[
\underline E_t\le E_t^{(C^\star)}
\quad\text{for every }t.
\]

Hence

\[
\Pr_{H_0}\!\left(\sup_t\underline E_t\ge 1/\alpha\right)
\le
\Pr_{H_0}\!\left(\sup_t E_t^{(C^\star)}\ge1/\alpha\right)
\le\alpha.
\]

Thus \(\underline E_t\) is an anytime-valid robust evidence process in the pathwise-domination sense for Model A, even though the pointwise minimum need not itself be a martingale.

This corrects the invalid arithmetic-mixture idea in the external review: the safe operation here is domination by the true candidate process, not averaging processes of which only one is guaranteed valid.

## Closed form

Let \(H_q(t)=\#\{s\le t:Q_s=q\}\) be the histogram of observed ranks.

For a candidate \(C\), let \(N_j^{(C)}\) be the histogram after merging the observed-rank bins according to \(C\).

The candidate log wealth has the exact closed form

\[
\log E_t^{(C)}
=
\log\Gamma(n+t+1)-\log\Gamma(n+1)
+
\sum_{j=0}^{n}
\left[
N_j^{(C)}\log a_j^{(m)}
-
\log\Gamma(N_j^{(C)}+1)
\right].
\]

Therefore the robust minimization depends only on the current rank histogram, not on the full ordering of the history, for this fixed categorical alternative bettor.

## Dynamic programming reduction

Brute force requires

\[
\binom{K}{m}
\]

candidate contamination sets for a fixed \(m\).

But deleting \(m\) reference positions is equivalent to deleting \(m\) boundaries among the \(K+1\) observed-rank bins.

A clean-rank bin is therefore a contiguous segment of observed-rank bins.

For a segment \([b,b+\ell-1]\) assigned to clean-rank index \(j\), let

\[
N=\sum_{q=b}^{b+\ell-1}H_q(t).
\]

Its additive cost is

\[
c(j,b,\ell)=N\log a_j^{(m)}-\log\Gamma(N+1).
\]

If the first \(b\) observed-rank bins have been consumed using \(d\) deleted boundaries, then exactly \(b-d\) clean-rank groups have already been formed. Hence the next group index is \(j=b-d\).

A transition using a segment of length \(\ell\) consumes \(\ell-1\) more deleted boundaries.

State:

\[
DP[b,d]
=
\text{minimum additive cost after consuming the first }b\text{ bins and }d\text{ deletions}.
\]

Transition:

\[
DP[b+\ell,d+\ell-1]
=
\min\left(
DP[b+\ell,d+\ell-1],
DP[b,d]+c(b-d,b,\ell)
\right).
\]

Since \(\ell\le M-d+1\), this gives a direct implementation in approximately

\[
O(KM^2)
\]

time and \(O(KM)\) memory for a fixed \(m\), rather than enumeration of \(\binom Km\) subsets.

The accompanying script verifies the DP result against exhaustive enumeration for small \(K,M\).

## Baseline: CCTM + replacement band

Shaer et al. (2026) construct a fixed-reference conditional conformal test martingale using a uniform CDF confidence band.

For an original clean ECDF \(\widehat F_K\) and an observed ECDF \(\widetilde F_K\) obtained by replacing at most \(M\) points,

\[
\|\widetilde F_K-\widehat F_K\|_\infty\le M/K
\]

pathwise.

Combining this with a DKW event

\[
\|\widehat F_K-F\|_\infty\le
\epsilon_{\mathrm{DKW}}
=
\sqrt{\frac{\log(2/\delta)}{2K}}
\]

gives

\[
\|\widetilde F_K-F\|_\infty
\le
\epsilon_{\mathrm{DKW}}+M/K.
\]

This yields a routine robust CDF-band baseline. It is conservative but valid even under the stronger adaptive-replacement Model B, because the ECDF perturbation inequality is pathwise.

## What this gate can and cannot establish

### If the DP equals brute force

That proves only the combinatorial reduction is correct.

### If the robust evidence has useful power in small experiments

That motivates a sharper theorem/power analysis.

### If robust evidence stays essentially flat while the oracle clean-subset PRM grows

That is evidence of a serious identifiability/power cost from unknown contamination identities. It does not by itself prove impossibility.

### Novelty is still unproven

General composite-null e-process theory already legitimizes worst-case/dominated constructions. The only potentially distinctive contribution would be a sharp rank-specific result showing that the static contamination coupling admits substantially better finite-sample power or a structural minimax characterization beyond the generic CDF-band baseline.

## Frozen computational gate

Run:

\`\`\`bash
uv run python experiments/pminus1_predictive_rank_dp_killtest.py
\`\`\`

Required outputs:

1. exact equality between DP and exhaustive enumeration for \(K=8,M=2\);
2. polynomial-time benchmark for \(K=50,M=5\);
3. DKW+\(M/K\) baseline widths;
4. a small seeded null/alternative diagnostic comparing:
   - oracle true-clean-subset PRM;
   - robust static-coupling minimum.

Decision after the run:
- **NO-GO** if the robust statistic has essentially no usable evidence growth even under a strong one-sided alternative and no sharper construction is visible;
- **CONTINUE** only if static coupling preserves meaningful evidence and the DP structure offers a material advantage over the generic band baseline.
