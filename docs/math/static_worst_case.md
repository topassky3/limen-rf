# Static worst-case lemma for LIMEN-RF

Status: **P−1 kill-test result**

This note settles the static worst-case question for the replacement-contamination model currently under consideration.

## Model

Let

\[
A=\sigma_X^2 U, \qquad U\sim \mathrm{Gamma}(m,1),
\]

and let there be `K` reference energies. At least `K-M` references are valid. For a valid reference `j`,

\[
B_j=\frac{\sigma_X^2}{r_j}V_j,
\qquad
V_j\sim \mathrm{Gamma}(m,1),
\qquad
r_j\in[1/c,c],
\]

with `c >= 1`. The valid `V_j` are taken i.i.d. and independent of `U` for the exact distributional formula below.

Up to `M` remaining reference energies may be replaced by arbitrary **nonnegative** values. This is a Byzantine/replacement model; it is not the same as additive RF interference.

Let `W_(k)` denote the `k`-th smallest value among all `K` references and define

\[
Z=\frac{A}{A+W_{(k)}}.
\]

We use ascending order statistics throughout.

## Theorem 1 — Degeneracy when `k <= M`

If `k <= M`, then the adversary can set at least `k` contaminated reference energies to zero. Hence

\[
W_{(k)}=0
\]

and, since `A > 0` almost surely,

\[
Z=1 \quad \text{a.s.}
\]

Therefore no nontrivial upper-tail false-alarm guarantee is possible under this replacement-contamination model unless

\[
k>M.
\]

## Theorem 2 — Exact static least-favourable configuration for `k > M`

Assume `k > M`. Set

\[
n=K-M, \qquad q=k-M.
\]

Let `B_(q)^valid` be the `q`-th smallest of the `n` valid reference energies.

For every realization of the valid and contaminated energies,

\[
W_{(k)} \ge B_{(q)}^{\mathrm{valid}}.
\]

### Proof of the order-statistic inequality

Among the first `k` values of the combined ordered sample, at most `M` can be contaminated. Therefore at least

\[
k-M=q
\]

of those values must be valid. Consequently the `q`-th smallest valid value cannot exceed the `k`-th smallest value of the combined sample:

\[
B_{(q)}^{\mathrm{valid}} \le W_{(k)}.
\]

Equality is attained by setting all `M` contaminated reference energies to zero, because valid Gamma energies are strictly positive almost surely. In that case the first `M` combined order statistics are the zeros and

\[
W_{(k)}=B_{(k-M)}^{\mathrm{valid}}.
\]

## Theorem 3 — Worst bounded mismatch occurs at `r_j=c`

Couple all admissible mismatch configurations using the same baseline variables `V_1,...,V_n`. For every valid reference,

\[
B_j(r_j)=\frac{\sigma_X^2}{r_j}V_j.
\]

Since `r_j <= c`,

\[
B_j(r_j)\ge \frac{\sigma_X^2}{c}V_j
\]

pathwise for every `j`. Order statistics are coordinatewise monotone, hence

\[
B_{(q)}^{\mathrm{valid}}(\mathbf r)
\ge
\frac{\sigma_X^2}{c}V_{(q)},
\]

where `V_(q)` is the `q`-th smallest of `V_1,...,V_n`.

Combining this with Theorem 2 gives

\[
W_{(k)}
\ge
\frac{\sigma_X^2}{c}V_{(q)}.
\]

Because `z(a,b)=a/(a+b)` is decreasing in `b` for `a>0`,

\[
Z
\le
Z^*:=
\frac{\sigma_X^2 U}
{\sigma_X^2 U+(\sigma_X^2/c)V_{(q)}}
=
\frac{cU}{cU+V_{(q)}}
\]

pathwise under this coupling.

Equality is attained by the configuration

\[
C_1=\cdots=C_M=0,
\qquad
r_1=\cdots=r_n=c.
\]

Therefore, for every `z` in `[0,1]`,

\[
\boxed{
\sup_{H_0}\Pr(Z\ge z)
=
\Pr\left(\frac{cU}{cU+V_{(q)}}\ge z\right)
}
\]

for the stated replacement-contamination model.

This is stronger than stochastic dominance alone: the bound follows from a pathwise coupling and the supremum is attained.

## Exact worst-case distribution

Let

\[
f_m(v)=\frac{v^{m-1}e^{-v}}{\Gamma(m)},
\qquad
F_m(v)=\Pr(\mathrm{Gamma}(m,1)\le v).
\]

For `n=K-M` and `q=k-M`, the density of the `q`-th order statistic is

\[
f_{V_{(q)}}(v)
=
\frac{n!}{(q-1)!(n-q)!}
[F_m(v)]^{q-1}
[1-F_m(v)]^{n-q}
f_m(v).
\]

For `0<z<1`, define

\[
a(z)=\frac{z}{c(1-z)}.
\]

Then

\[
\Pr(Z^*\ge z)
=
\int_0^\infty
\bar F_m(a(z)v)
 f_{V_{(q)}}(v)\,dv,
\]

where `\bar F_m=1-F_m`.

Equivalently,

\[
\Pr(Z^*\ge z)
=
\int_0^\infty
F_{V_{(q)}}\left(\frac{c(1-z)}{z}u\right)
 f_m(u)\,du.
\]

These one-dimensional integrals are enough for stable numerical evaluation; a closed form is not needed for the kill-test.

## Corollary — Fixed-sample robust p-value

Because `Z <=_st Z^*` and `Z^*` is continuous, the upper-tail quantity

\[
p(z)=\Pr(Z^*\ge z)
\]

is a valid conservative p-value for every distribution in the composite null class above.

This corollary is useful operationally but is **not** being claimed as methodological novelty.

## P−1 interpretation

The kill-test resolves the static problem cleanly:

1. `k <= M` is degenerate under arbitrary nonnegative replacement contamination.
2. For `k > M`, the worst contamination is `M` zero-energy replacements.
3. The worst bounded mismatch is the corner `r_j=c` for every valid reference.
4. The resulting least-favourable tail distribution is explicit up to a one-dimensional integral.

### Scientific consequence

The static least-favourable result is mathematically useful but too direct to serve as the central novelty claim. It should be treated as a lemma / design constraint.

The next gate is therefore not another static CFAR derivation. It is to determine whether the resulting composite fixed-sample test can be sequentialized by existing anytime-valid theory in a completely routine way, or whether a nontrivial obstacle remains.

## Assumptions that must not be silently generalized

This proof depends on the present model:

- contaminated energies are arbitrary **nonnegative replacements**;
- valid references differ through multiplicative scale mismatch only;
- the Gamma shape `m` is common for the exact distributional formula;
- `k` denotes the ascending order statistic;
- the exact density formula assumes independent valid Gamma blocks and independence from `A`.

The pathwise order-statistic inequalities themselves are more general than the Gamma distribution, but claims beyond the stated model require a separate proof.
