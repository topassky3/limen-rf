# LIMEN-RF paper-core strengthening v0.2

Date: 2026-09-21

Status: **mathematical strengthening after manuscript v0.1 compile; detector remains frozen**

This pass does not change the detector, bettor family, baseline grid, or frozen Kill-Test results. It extracts additional formal consequences from the already-frozen structure.

## 1. Filtration and predictability closure

Define the canonical clean rank

\[
R_t^\star=\#\{i\in G:Y_i\le X_t\},
\qquad
\mathcal G_t^\star=\sigma(R_1^\star,\ldots,R_t^\star).
\]

Treat the betting strategy as a deterministic measurable functional

\[
\mathsf q_t:
\{0,\ldots,n\}^{t-1}\to\Delta_n.
\]

For candidate \(C\),

\[
q_t^{(C)}
=
\mathsf q_t
(R_1^{(C)},\ldots,R_{t-1}^{(C)}).
\]

For the realized true candidate \(C^\star\),

\[
R_t^{(C^\star)}=R_t^\star
\]

pathwise, hence

\[
q_t^{(C^\star)}
=
\mathsf q_t(R_1^\star,\ldots,R_{t-1}^\star)
\]

is \(\mathcal G_{t-1}^\star\)-measurable.

Thus the true-candidate process is a single canonical clean PRM and not a post-selected martingale.

## 2. Upper-bound-only contamination count

Suppose the true count \(m^\star\) is unknown but

\[
m^\star\le M.
\]

For every \(r\in\{0,\ldots,M\}\), set \(n_r=K-r\) and define

\[
\mathcal C_r
=
\{C\subseteq\{1,\ldots,K\}:|C|=r\}.
\]

Compute size-specific candidate PRM wealths \(E_t^{(r,C)}\) using the clean predictive null law for \(n_r\) references and define

\[
\underline E_t^{(\le M)}
=
\min_{0\le r\le M}
\min_{C\in\mathcal C_r}
E_t^{(r,C)}.
\]

The true pair \((m^\star,C^\star)\) belongs to this family, so

\[
\underline E_t^{(\le M)}
\le
E_t^{(m^\star,C^\star)}
\]

pathwise. Therefore

\[
\Pr_{H_0}
\left(
\sup_t
\underline E_t^{(\le M)}
\ge1/\alpha
\right)
\le\alpha.
\]

This is now a formal corollary in the manuscript.

Important: the frozen experiments remain exact-\(m=2\). No power claim is made yet for the upper-bound-only procedure.

## 3. Exact candidate/partition bijection

The \(K+1\) observed-rank bins are the vertices of a path; sorted reference position \(c\in\{1,\ldots,K\}\) is exactly the boundary/edge between bins \(c-1\) and \(c\).

Deleting a candidate set \(C\) of \(m\) positions removes \(m\) path edges and leaves exactly

\[
K+1-m=n+1
\]

connected components, each a nonempty contiguous block.

Conversely, every partition of the ordered \(K+1\) bins into \(n+1\) nonempty contiguous blocks has exactly \(m\) missing internal boundaries. Those boundaries uniquely recover \(C\).

Therefore candidate sets and contiguous partitions are in bijection.

## 4. Exact fixed-categorical DP theorem

For observed-rank histogram \(H_q(t)\), precompute prefix sums so every segment count

\[
N(b,\ell)
=
\sum_{q=b}^{b+\ell-1}H_q(t)
\]

is \(O(1)\).

For fixed categorical bettor \(a=(a_0,\ldots,a_n)\), segment cost is

\[
c(j,b,\ell)
=
N(b,\ell)\log a_j
-
\log\Gamma(N(b,\ell)+1).
\]

Let \(DP[b,d]\) be the minimum additive cost after consuming \(b\) observed-rank bins and deleting exactly \(d\) boundaries.

Because \(b-d\) contiguous blocks have been completed, the next clean-rank index is

\[
j=b-d.
\]

Transition:

\[
DP[b+\ell,d+\ell-1]
=
\min\{
DP[b+\ell,d+\ell-1],
DP[b,d]+c(b-d,b,\ell)
\}.
\]

Feasibility requires

\[
b+\ell\le K+1,
\qquad
d+\ell-1\le m.
\]

By the candidate/partition bijection, paths from \(DP[0,0]\) to \(DP[K+1,m]\) are in one-to-one correspondence with candidate sets. Induction on \(b\) proves exact optimality.

There are \(O(Km)\) states and at most \(O(m)\) transitions per state, yielding

\[
O(Km^2)
\]

time and

\[
O(Km)
\]

memory.

The theorem remains restricted to a fixed categorical bettor. The full frozen convex portfolio contains a log-sum-exp and is not covered by this DP.

## 5. Finite-reference asymptotics

Let

\[
k=n+1,
\qquad
\widehat\pi_{j,t}=N_j(t)/t
\to\pi_j>0.
\]

### 5.1 Fixed categorical bettor

For a fixed positive categorical vector \(a\),

\[
\frac1t\log E_t^{(a)}
\to
-D_{\mathrm{KL}}(\pi\Vert a).
\]

Thus, unless

\[
\pi=a,
\]

the fixed categorical component decays exponentially.

### 5.2 Dirichlet predictive bettor

For

\[
q_{t,j}
=
\frac{N_{j,t-1}+\alpha_j}
{t-1+A},
\qquad
A=\sum_j\alpha_j,
\]

the exact wealth is

\[
E_t^{(\boldsymbol\alpha)}
=
\frac{\Gamma(A)\Gamma(k+t)}
{\Gamma(A+t)\Gamma(k)}
\prod_j
\frac{\Gamma(N_j(t)+\alpha_j)}
{\Gamma(\alpha_j)\Gamma(N_j(t)+1)}.
\]

Gamma-ratio asymptotics give

\[
E_t^{(\boldsymbol\alpha)}
\to
\frac{\Gamma(A)}
{\Gamma(k)\prod_j\Gamma(\alpha_j)}
\prod_j
\pi_j^{\alpha_j-1},
\]

a finite positive constant whenever \(\pi\) is interior.

### 5.3 Consequence for the frozen finite portfolio

If the limiting interior rank-frequency vector \(\pi\) differs from every fixed categorical vector in the frozen finite menu, then:

- every fixed categorical component decays exponentially;
- every Dirichlet predictive component converges to a finite constant;
- the constant-one hedge stays constant;
- therefore the true-candidate convex portfolio has a finite limit.

Since

\[
\underline E_t\le E_t^{(C^\star)},
\]

the robust lower envelope cannot diverge to \(+\infty\) in that regime.

This formally explains the finite-reference information ceiling of the frozen betting family and supports the paper's finite-horizon focus.

## 6. Manuscript consequences

The paper now has the following mathematical stack:

1. imported Kuang--Xia clean predictive-rank law;
2. imported clean PRM martingale;
3. canonical true-candidate filtration lemma;
4. exact-\(m\) anytime robust crossing theorem;
5. unknown-\(m\), known-\(M\) corollary;
6. candidate/contiguous-partition bijection;
7. exact \(O(Km^2)\) DP theorem for fixed categorical bettors;
8. finite-reference asymptotic proposition for the frozen bettor families.

No detector retuning was performed.
