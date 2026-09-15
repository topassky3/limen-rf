# P−1 Sequentialization Firewall — LIMEN-RF

Status: **decision pass**

Purpose: determine whether the robust fixed-sample test obtained in `docs/math/static_worst_case.md` yields a genuinely nontrivial anytime-valid contribution, or whether sequential validity follows routinely from existing theory.

## Starting point

For one block, the current replacement-contamination model yields a least-favourable statistic

\[
Z_t^*=\frac{c_t U_t}{c_t U_t+V_{t,(q)}}
\]

with a conservative fixed-sample upper-tail p-value

\[
p_t = \Pr(Z_t^* \ge Z_t^{\mathrm{obs}}).
\]

The static kill-test established that this p-value is valid for the stated composite null class. The present firewall asks whether moving from these per-block p-values to an anytime-valid detector is mathematically routine.

## Exact sequential null needed for a valid product construction

Let \(\mathcal F_{t-1}\) denote the history before block \(t\). Assume that, conditionally on \(\mathcal F_{t-1}\), the current block law belongs to the same admissible null class used in the static theorem, with all detector design quantities such as \(c_t,K,M,k,m\) fixed or \(\mathcal F_{t-1}\)-measurable before block \(t\) is observed.

Then the static tail result applies conditionally and gives

\[
\Pr(p_t \le u\mid\mathcal F_{t-1})\le u,
\qquad 0\le u\le1.
\]

Thus \(p_t\) is a **conditionally superuniform p-variable**.

For any valid decreasing p-to-e calibrator \(f\) with

\[
\int_0^1 f(u)\,du\le1,
\]

we have

\[
\mathbb E[f(p_t)\mid\mathcal F_{t-1}]\le1.
\]

In particular, for \(0<\kappa<1\),

\[
e_t=\kappa p_t^{\kappa-1}
\]

is a sequential e-variable. Consequently

\[
E_T=\prod_{t=1}^{T}e_t
\]

is a nonnegative supermartingale under every null process satisfying the conditional membership assumption. Ville's inequality therefore yields

\[
\Pr\left(\sup_{T\ge1}E_T\ge1/\alpha\right)\le\alpha.
\]

No temporal independence assumption is needed beyond the conditional null-membership statement that makes each \(p_t\) conditionally superuniform.

## Evidence matrix

| ID | Source | Result relevant to this firewall | Threat to LIMEN-RF sequential novelty | Assessment |
|---|---|---|---|---|
| S01 | Vovk & Wang, *E-values: Calibration, Combination, and Applications*, AoS 2021 | Characterizes p-to-e calibrators. In particular \(f_\kappa(p)=\kappa p^{\kappa-1}\) is a valid calibrator. | Directly makes the proposed p→e step generic once a p-value is available. | **FATAL for novelty of the p→e step.** |
| S02 | Ramdas, Grünwald, Vovk & Shafer, *Game-Theoretic Statistics and Safe Anytime-Valid Inference*, Statistical Science 2023 | General e-process / test-supermartingale framework for optional stopping and composite hypotheses. | Ville/e-process anytime validity is established general machinery. | **FATAL for novelty of generic T1.** |
| S03 | Howard et al., *Time-uniform Chernoff bounds via nonnegative supermartingales*, Probability Surveys 2020 | General time-uniform crossing guarantees from nonnegative supermartingales. | Reinforces that time-uniform control from a supermartingale is standard. | **HIGH.** |
| S04 | Ramdas, Ruf, Larsson & Koolen, *Admissible anytime-valid sequential inference must rely on nonnegative martingales* | Shows martingale structure is essentially universal for admissible anytime-valid inference. | Makes a generic martingale/supermartingale construction a framework application, not a new principle. | **HIGH.** |
| S05 | Ruf, Larsson, Koolen & Ramdas, *A composite generalization of Ville's martingale theorem* | Develops e-processes as composite generalizations of nonnegative martingales. | Composite-null sequential validity itself is mature theory. | **HIGH.** |
| S06 | Wasserman, Ramdas & Balakrishnan, *Universal Inference*, PNAS 2020 | General composite likelihood inference and sequential / anytime-valid extensions. | Demonstrates broad routes from composite tests to anytime-valid procedures. | **MEDIUM-HIGH.** |
| S07 | Grünwald, de Heide & Koolen, *Safe Testing*, JRSS-B 2024 | General GRO e-values for composite nulls and nuisance parameters. | Any claim based only on handling a composite nuisance with e-values is too broad. | **VERY HIGH for T3-style claims.** |
| S08 | Pérez-Ortiz et al., *E-statistics, group invariance and any time valid testing*, AoS 2024 | Growth-optimal invariant e-statistics and anytime-valid tests for invariant models. | Threatens any claim based only on scale removal / energy-ratio invariance. | **VERY HIGH for invariant-LR novelty.** |
| S09 | Koning & van Meer, *Anytime validity is free: inducing sequential tests*, JRSS-B 2026 | Any valid fixed-horizon test can induce an anytime-valid sequential test; composite hypotheses are explicitly treated. | Gives another generic route from fixed tests to anytime-valid tests. | **VERY HIGH.** |
| S10 | Same, composite-hypothesis section | Composite induction can require an essential infimum over pointwise tests; natural choices may be unclear or degenerate. | Shows composite induction is not always computationally trivial, but this does not rescue our p→e construction because our conditional p-value route already gives a routine valid process. | **Not a rescue of T1.** |
| S11 | Johari et al., *Always Valid Inference*, Operations Research 2021 | Always-valid p-values and sequential testing under continuous monitoring. | Confirms mature literature on continuous monitoring and optional stopping. | **MEDIUM.** |
| S12 | Direct searches for `anytime-valid CFAR`, `e-process CFAR radar`, `e-value CFAR radar`, `sequential OS-CFAR e-value` | No obvious exact RF paper combining OS-CFAR with e-process terminology appeared in the initial targeted search. | Absence of a direct RF-labelled paper does not establish novelty because S01–S10 already subsume the generic statistical construction. | **No positive novelty evidence.** |

## High-risk equivalence check

### Question A — Does the static p-value become an anytime-valid detector mechanically?

**Yes, under the conditional null-membership assumption.**

Once

\[
\Pr(p_t\le u\mid\mathcal F_{t-1})\le u
\]

holds, Vovk–Wang calibration gives a conditional e-variable and multiplication gives a nonnegative supermartingale. Ville then gives the desired time-uniform error bound. This is a short corollary of existing theory, not a standalone methodological theorem.

### Question B — Is temporal independence required?

**No.** The product construction needs

\[
\mathbb E[e_t\mid\mathcal F_{t-1}]\le1,
\]

not i.i.d. blocks. Thus allowing \(c_t\) or other nuisance quantities to vary predictably with the past is not novel by itself, provided the true conditional block law remains inside the null class selected before observing block \(t\).

### Question C — Is there still a nontrivial condition hidden here?

**Yes, but it is not the sequentialization theorem.** The real requirement is that the assumed bound is true conditionally:

\[
P_t(\cdot\mid\mathcal F_{t-1})\in\mathcal P_{0,t}(c_t,M,k,\ldots).
\]

If \(c_t\) is merely an estimate from past data and can underestimate the true mismatch, conditional superuniformity can fail and the e-process guarantee collapses. Proving a valid data-driven upper bound for the nuisance, or integrating nuisance uncertainty into the evidence process, would be a separate problem.

### Question D — Does Koning & van Meer (2026) create a nontrivial obstacle that rescues T1?

**No for our current safe construction.** Their composite-hypothesis induction has genuine issues of choosing pointwise tests, essential infima, measurability and possible degeneracy. Those issues are theoretically interesting. However, we do not need their induction construction to sequentialize the current robust per-block test: conditional p-value validity plus a standard p-to-e calibrator already gives an explicit anytime-valid process.

### Question E — Did the targeted RF search find the exact same named method?

No exact `OS-CFAR + e-process` paper was identified in this pass. This is insufficient for a novelty claim because a publication cannot claim methodological novelty for a direct domain-specific instantiation of a general theorem unless the instantiation contains an additional nontrivial result.

## Firewall decision

### T1 as originally planned

Target:

\[
\sup_{H_0}\Pr\left(\sup_T E_T\ge1/\alpha\right)\le\alpha.
\]

**Decision: SUBSUMED / NOT A CENTRAL NOVELTY.**

Given a conditionally valid robust p-value for every block, the theorem follows routinely from established p-to-e and e-process machinery.

### What remains scientifically meaningful

The following are still useful engineering/statistical results but should be presented as ingredients or guarantees rather than primary novelty:

1. the explicit static least-favourable CFAR tail derived in `static_worst_case.md`;
2. its conservative per-block p-value;
3. a standard calibrated e-process providing continuous-monitoring guarantees;
4. empirical power/delay comparison against fixed-sample and sequential baselines.

### What could still create a real contribution

A future central contribution must add a nontrivial result **before** or **inside** the conditional-validity step, for example:

- a data-driven predictable nuisance bound \(c_t\) with a simultaneous guarantee that preserves conditional validity;
- a broader RF model (correlated / colored / dependent reference cells, gain uncertainty, etc.) for which a valid least-favourable envelope is genuinely nontrivial;
- an explicit RF-specific e-factor whose uniform validity and efficiency require new analysis beyond generic calibration, provided prior art does not already subsume it.

These are hypotheses for a future reformulation, not current novelty claims.

## Gate consequence

The sequentialization firewall **kills T1 as an independent methodological contribution**.

Combined with the static kill-test, two planned central pieces are now classified as follows:

- static least-favourable corner under the current replacement model: **valid but too direct for central novelty**;
- anytime-valid sequentialization via p→e / Ville: **generic consequence of existing theory**.

Therefore the current formulation should not proceed to large simulations as though T1/T2 were the paper's novel theorem set.

### P−1 status after this pass

**REFORMULATE.**

This is not a claim that no publishable LIMEN-RF project exists. It is a claim that the current mathematical core is insufficiently novel as a methodological paper.

## Next decision rule

Do not introduce another broad idea immediately. The next research task must identify exactly one additional RF/statistical assumption whose treatment is both physically justified and not already covered by the same generic machinery. That candidate must pass its own narrow prior-art kill-test before implementation.
