# P−1 Search Pass 01 — LIMEN-RF / AV-OS

Status: **provisional screening**. This pass is based on abstracts, publisher metadata, and accessible full-text/author copies where available. Threat ratings are not final until the highest-overlap papers are checked in full.

## Current candidate contribution

The firewall is testing whether a nontrivial gap remains for the combination

`OS/reference-CFAR + bounded target/reference mismatch + composite least-favourable null + anytime-valid sequential evidence + predictable time-varying nuisance`.

The optional multi-reference contamination idea and an RF-specific e-factor are treated as secondary until the core theorem survives prior art.

## Evidence matrix — pass 01

| ID | Citation | Family | Model / method | Relevant guarantee | Overlap with LIMEN-RF | Provisional threat | Remaining gap / action |
|---|---|---|---|---|---|---|---|
| P01 | H. Rohling, “Radar CFAR Thresholding in Clutter and Multiple Target Situations,” IEEE TAES, 1983. DOI: 10.1109/TAES.1983.309350 | OS-CFAR | Uses an ordered reference sample to set the CFAR threshold; designed for multiple targets and clutter edges. | Fixed-sample CFAR analysis. | Establishes OS-CFAR itself as classical prior art. | **HIGH** for any novelty claim based on OS selection alone. | Our novelty cannot be the OS statistic or robustness to multiple targets by itself. |
| P02 | M. Barkat, S. D. Himonas, P. K. Varshney et al., “CFAR detection for multiple target situations,” IEE Proc. F, 1989. DOI: 10.1049/IP-F-2.1989.0033 | Robust CFAR | Weighted CA, censored mean-level and generalized censored mean-level detectors for interfering targets in reference cells. | Fixed-sample false-alarm/detection performance. | Strongly overlaps with contaminated-reference motivation. | **HIGH** for contamination novelty. | Partial contamination must not be sold as new; any contribution must be sequential/composite-null specific. |
| P03 | E. K. Al-Hussaini and M. B. El-Mashade, “Performance of cell-averaging and order-statistic CFAR detectors processing correlated sweeps for multiple interfering targets,” Signal Processing, 1996. DOI: 10.1016/0165-1684(95)00150-6 | OS-CFAR | CA/OS-CFAR with correlated sweeps and multiple interferers in reference cells. | Exact/numerical fixed-sample detection analysis. | Shows OS-CFAR under correlated data/interferers is mature. | **MEDIUM-HIGH**. | Need a theorem that is not merely another fixed-sample OS-CFAR distribution calculation. |
| P04 | M. B. El-Mashade, “Detection analysis of linearly combined order statistic CFAR algorithms in nonhomogeneous background environments,” Signal Processing, 1998. DOI: 10.1016/S0165-1684(98)00057-7 | Robust OS-CFAR | Linear combinations of order statistics in nonhomogeneous clutter. | Fixed-sample performance analysis. | Threatens claims around order-statistic aggregation and nonhomogeneity. | **MEDIUM-HIGH**. | Sequential anytime-valid control under a composite nuisance remains distinct if nontrivial. |
| P05 | A. Farrouki and M. Barkat, “Automatic censored mean level detector using a variability-based censoring with non-coherent integration,” Signal Processing, 2007. DOI: 10.1016/j.sigpro.2006.12.012 | Censored CFAR | Automatic censoring under clutter transitions/interfering targets; ranked subset used for background estimation. | Exact Pfa expression plus performance analysis. | Strong overlap with adaptive rejection of contaminated references. | **HIGH** for censoring/robust-reference novelty. | Contamination should be a stress model, not the headline contribution unless a new sequential guarantee appears. |
| P06 | R. Tandra and A. Sahai, “SNR Walls for Signal Detection,” IEEE JSTSP, 2008. DOI: 10.1109/JSTSP.2007.914879 | Noise uncertainty | Low-SNR detection under model/noise uncertainty; establishes SNR-wall phenomena. | Impossibility/robustness results under uncertainty models. | Directly relevant to any claim about unknown noise and low SNR. | **HIGH** against “breaks SNR wall” language. | We must frame reference information/mismatch assumptions explicitly and never claim universal wall-breaking. |
| P07 | Q. Zou, S. Zheng and A. H. Sayed, “Cooperative spectrum sensing via sequential detection for cognitive radio networks,” IEEE SPAWC, 2009. DOI: 10.1109/SPAWC.2009.5161759 | Sequential RF sensing | Sequential LLR accumulation; robust variants under model uncertainty. | Reduced average sensing time under sequential detection. | Shows sequential spectrum sensing and uncertainty handling are old. | **HIGH** for generic sequential-RF novelty. | Our distinction must be optional-stopping-valid evidence plus OS/reference composite-null structure, not “sequential sensing”. |
| P08 | J. K. Sreedharan and V. Sharma, “Spectrum sensing using distributed sequential detection via noisy reporting MAC,” Signal Processing 106, 2015. DOI: 10.1016/j.sigpro.2014.07.009 | Sequential/composite sensing | Decentralized sequential tests; extensions for SNR uncertainty/fading. | Theoretical sequential performance, asymptotic comparisons. | Strong overlap with composite sequential spectrum sensing. | **HIGH**. | Must check full text for nuisance modelling and whether their robust sequential tests imply anything close to T1/T2. |
| P09 | S. Xie et al., “Asynchronous cooperative spectrum sensing via sequential detection in fuzzy hypothesis testing under noise uncertainty in cognitive radio networks,” IET Communications, 2023. DOI: 10.1049/cmu2.12526 | Sequential noise uncertainty | Sequential cooperative sensing under noise uncertainty. | Simulation/performance claims for sequential detector. | Confirms active prior art on sequential sensing with noise uncertainty. | **MEDIUM**. | Likely different formal guarantee, but full-text check needed. |
| P10 | S. R. Howard, A. Ramdas, J. McAuliffe and J. Sekhon, “Time-uniform Chernoff bounds via nonnegative supermartingales,” Probability Surveys 17, 2020. DOI: 10.1214/18-PS321 | Anytime-valid inference | Nonnegative supermartingales and time-uniform boundary crossing. | Uniform-in-time crossing guarantees. | Provides general machinery behind our desired Ville-style T1. | **HIGH** for novelty of T1 in isolation. | T1 alone may be routine unless the RF-specific composite-null factor/LFN is mathematically nontrivial. |
| P11 | A. Ramdas, P. Grünwald, V. Vovk and G. Shafer, “Game-Theoretic Statistics and Safe Anytime-Valid Inference,” Statistical Science 38(4), 2023. DOI: 10.1214/23-STS894 | e-processes | General e-process/test-supermartingale framework for optional stopping/continuation. | Safe anytime-valid testing at all stopping times. | Directly subsumes generic e-process + Ville arguments. | **HIGH**. | We need RF-specific construction/least-favourable result, not a generic application of Ville. |
| P12 | L. Wasserman, A. Ramdas and S. Balakrishnan, “Universal inference,” PNAS, 2020. | Anytime/composite inference | Split likelihood and universal inference; includes anytime-valid p-value constructions. | Valid inference under broad models, including anytime-valid p-values. | Threatens claims that optional-stopping validity itself is novel. | **MEDIUM-HIGH**. | Need determine whether our composite OS statistic is merely a plug-in instance of broad general theory. |
| P13 | P. Grünwald, R. de Heide and W. Koolen, “Safe testing,” JRSS-B 86(5), 2024. | Composite-null e-values | Growth-rate-optimal e-variables for composite null/alternative with nuisance parameters; RIPr/Bayes-factor constructions. | e-validity and growth optimality under composite hypotheses. | Very close to intended T3 philosophy. | **VERY HIGH** for naive LR/RIPr novelty. | A proposed LR against a worst-case null is not novel and is not automatically valid; we must prove the RF model’s concrete RIPr/LFN structure. |
| P14 | M. F. Pérez-Ortiz, T. Lardy, R. de Heide and P. Grünwald, “E-statistics, group invariance and any time valid testing,” Annals of Statistics 52(4), 2024. | Invariant e-statistics | Growth-optimal e-statistics from maximally invariant statistics; scale-location families included under conditions. | Anytime-valid tests from invariant/GROW e-statistics. | Potentially very close because our energy ratios remove an unknown scale. | **VERY HIGH**. | Critical full-text check: does the scale-invariance theorem make our target/reference ratio e-factor a routine invariant-e construction? |
| P15 | M. Larsson, A. Ramdas and J. Ruf, “The numeraire e-variable and reverse information projection,” Annals of Statistics 53(3), 2025. | Composite-null e-values | General existence/optimality of a numeraire e-variable for arbitrary composite null vs point alternative; generalized RIPr. | Log-optimal e-variable existence and generalized RIPr. | Strong threat to any claim that deriving “optimal e-value for composite null” is novel. | **VERY HIGH**. | Novelty can only lie in an explicit RF-specific characterization/computable form or in the LFN/time-varying structure. |
| P16 | Y. Hao and P. Grünwald, “E-Values for Exponential Families: the General Case,” arXiv:2409.11134, 2024. | Composite e-processes | RIPr, conditional e-variable, universal inference, sequentialized RIPr for composite exponential-family nulls. | e-validity/e-power comparisons; sequentialized constructions. | High relevance if Gamma/exponential energy models place our null in or near exponential-family structure. | **VERY HIGH**. | Critical task: determine whether bounded scale mismatch + OS transform escapes routine exponential-family treatment or not. |
| P17 | Y. Benjamini and R. Heller, “Screening for Partial Conjunction Hypotheses,” Biometrics 64(4), 2008. DOI: 10.1111/j.1541-0420.2007.00984.x | Adjacent multiple testing | Partial-conjunction tests using ordered p-values, with validity under specified dependence structures. | Valid partial-conjunction p-values. | Threatens multi-reference constructions based only on p-value order statistics. | **HIGH** for the abandoned multi-p idea. | Do not claim novelty for `p_(M+1)`/Bonferroni-style robust aggregation. |
| P18 | H. Rohling / broader OS-CFAR literature summarized in order-statistics CFAR reviews and later robust CFAR work | CFAR review context | Decades of OS, trimmed, censored, GO/SO and hybrid CFAR variants. | Many fixed-sample CFAR guarantees. | Establishes that “robust order statistic reference processing” is a mature family, not a new concept. | **HIGH**. | Contribution must be a new sequential/composite theorem, not a new acronym around known CFAR pieces. |

## First-pass synthesis

### What is already clearly not novel

1. OS-CFAR itself.
2. Censoring / trimming / ordering contaminated reference cells.
3. Sequential spectrum sensing by SPRT-like methods.
4. Noise-uncertainty-aware spectrum sensing in general.
5. Ville/e-process optional-stopping validity in general.
6. Composite-null e-values, RIPr and growth-optimality in general.
7. Partial-conjunction/order-statistic p-value aggregation in general.

### Highest-risk novelty threats

The most dangerous papers for the current theorem map are **P13–P16**, not the classical radar papers. General e-value theory is strong enough that a paper whose contribution is merely “take an OS-CFAR statistic, compute a conservative p-value, convert p→e, multiply over time and invoke Ville” is unlikely to be a substantial methodological contribution.

P14 is especially important because scale invariance may interact directly with the target/reference ratio structure. P16 is important because the raw energy variables are Gamma/exponential-family objects. These two require full mathematical comparison before P−1 can pass.

### Provisional surviving gap

A potentially defensible gap remains only if at least one of the following is genuinely non-routine:

- an **explicit least-favourable null** for the OS/reference ratio under **bounded heterogeneous target/reference mismatch**;
- a proof that this least-favourable or conservative construction remains valid with **predictable time-varying nuisance parameters** and therefore yields a nontrivial anytime-valid RF detector;
- an **explicit computable RF-specific e-factor** whose uniform composite-null validity is not an immediate corollary of RIPr/invariance theory and whose growth materially improves on the safe p→e fallback.

This is not yet a GO decision. The current state is **PROVISIONAL REFORMULATE / CONTINUE FIREWALL**: the broad idea survives, but the novelty must be narrowed to the composite OS mismatch theorem rather than to e-processes, OS-CFAR, or sequential sensing separately.

## Next high-priority full-text checks

1. Pérez-Ortiz et al. (2024): determine exactly when maximally invariant likelihood ratios give GROW anytime-valid tests for scale families, and whether our OS ratio falls directly inside their theorem.
2. Hao & Grünwald (2024): determine whether sequentialized RIPr for exponential-family composite nulls directly covers Gamma energy blocks with bounded scale ratios.
3. Grünwald, de Heide & Koolen (2024): identify the assumptions needed for composite-null GRO e-values and whether a bounded nuisance rectangle has a standard RIPr solution.
4. Sreedharan & Sharma (2015): inspect their composite sequential handling of SNR/noise uncertainty for any least-favourable or generalized likelihood construction overlapping T2.
5. Classical OS-CFAR literature: search specifically for **noise-power mismatch between CUT and reference cells**, not merely clutter edges/interferers.

## Pass-01 count against Issue #3

- Total screened: **18**
- CFAR / OS-CFAR / robust-reference: **6+**
- Sequential / anytime-valid / e-process: **7+**
- Robust/composite-null: **5+**

The numerical minimum is met at screening level, but the gate remains open because the highest-overlap mathematical sources still require full-text equivalence checks.
