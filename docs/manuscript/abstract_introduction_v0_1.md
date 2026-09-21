# LIMEN-RF manuscript v0.1 — Abstract + Introduction

Date: 2026-09-21

Status: **first prose draft after novelty firewall**

Working title:

# Anytime-Valid Predictive-Rank Detection with a Statically Contaminated Reference Set

## Abstract

Sequential distribution-shift detection often relies on a fixed reference sample that represents the nominal distribution. Recent predictive-rank martingales provide exact anytime-valid monitoring when that reference is clean, but in radar, monitoring, and calibration systems the reference bank itself may contain a small number of persistent interferers or outliers. We study a finite fixed reference containing an unknown set of static, exogenous replacements whose identities remain unchanged throughout online monitoring. For every candidate set of contaminated sorted positions, we reconstruct the corresponding clean-reference rank sequence and apply a valid predictive-rank martingale. The true candidate recovers the clean rank process exactly; therefore, the pointwise lower envelope of the candidate wealth processes is pathwise dominated by a valid clean predictive-rank martingale, yielding finite-sample anytime threshold-crossing control without estimating the unknown null distribution. The static contamination pattern also induces a contiguous-partition structure on observed-rank bins; for a fixed categorical bettor, this yields an additive objective and a dynamic-programming reduction. In frozen finite-reference simulations, the proposed static-coupling construction substantially outperforms conservative confidence-band baselines adapted to contaminated references while remaining close to an oracle that knows the contaminated positions. For example, with \(K=32\), two contaminated references, horizon \(T=200\), and a moderate \(\mathrm{Beta}(4,1)\) shift, the crossing probability is \(0.935\) for the proposed method, \(0.170\) for the strongest tuned confidence-band baseline, and \(0.995\) for the oracle; median detected delays are 13, 78.5, and 8, respectively. These results isolate a finite-reference advantage from exploiting persistent contamination identities rather than treating contamination only as generic CDF uncertainty.

**Keywords:** anytime-valid inference; predictive ranks; martingales; e-values; contaminated reference data; CFAR; sequential change detection; robust statistics.

---

# 1. Introduction

Many sequential detection systems compare incoming observations against a finite bank of nominal reference data. This pattern appears in radar constant-false-alarm-rate (CFAR) detection, statistical process monitoring, anomaly detection, conformal monitoring, and distribution-shift detection. The reference data are often treated as a stable proxy for the unknown null distribution. In practice, however, a small number of reference observations may already be corrupted before online monitoring begins. In radar this can occur when interfering targets or heterogeneous clutter occupy reference cells; in calibration and monitoring systems it can arise from mislabeled, anomalous, or otherwise nonrepresentative historical observations. The statistical difficulty is not merely that the empirical distribution function is uncertain. When the same finite reference bank is reused over time, the identities of the contaminated reference observations form a persistent latent structure shared by every future decision.

Robust handling of contaminated reference cells has a long history in radar. Order-statistic CFAR was introduced to improve robustness in multiple-target and clutter-edge environments, and later censored, trimmed, and robust quantile-based CFAR variants continued this line of work [Rohling1983; CFAR-Robust-Refs]. These methods demonstrate that contaminated reference cells are a classical and practically important problem. Their guarantees and operating principles, however, are typically one-shot or window-based: a local statistic computed from the reference cells is used to set a detection threshold under a specified clutter model. They do not exploit the exact dependence created by repeatedly comparing an online stream against the same finite contaminated reference bank, nor are they designed to provide optional-stopping-valid sequential evidence.

A separate literature has developed distribution-free sequential monitoring through conformal martingales, e-processes, and rank-based tests [Vovk2021; RamdasEtAl2022]. Of particular relevance, Kuang and Xia [KuangXia2026] recently introduced predictive-rank martingales for distribution-shift detection with a fixed clean reference sample. If \(n\) clean reference observations and the future null stream are iid from an unknown continuous distribution, and \(R_t\in\{0,\ldots,n\}\) denotes the rank of the \(t\)-th online observation relative to the fixed reference, then the repeated reuse of the same reference produces the exact predictive law

\[
\Pr(R_t=j\mid R_{1:t-1})
=
\frac{N_{j,t-1}+1}{n+t},
\]

where \(N_{j,t-1}\) is the number of previous online ranks equal to \(j\). Kuang and Xia further show that any predictable normalized betting distribution \(q_t\) yields a nonnegative predictive-rank martingale through the likelihood-ratio factor \(q_{t,R_t}/p_{t,R_t}\), and hence anytime-valid type-I error control by Ville's inequality. This clean fixed-reference result is the probabilistic engine used in the present work; we do not claim the predictive-rank law or its generic martingale construction as new.

Fixed-reference uncertainty has also been studied from a conformal perspective. Shaer et al. [ShaerEtAl2026] proposed conditional conformal test martingales (CCTMs), which compare incoming observations to a fixed iid null reference dataset and explicitly account for finite-reference CDF estimation error through a simultaneous confidence band. Their construction addresses an important weakness of conformal test martingales that continually enlarge the reference set: after a change, post-shift observations can enter that growing reference and dilute subsequent evidence. CCTM instead keeps the null reference fixed and corrects the betting process for uncertainty in the empirical CDF. The reference dataset in their theoretical setup is nevertheless clean iid null data. In this paper, any confidence-band method applied to an already contaminated fixed reference is therefore an adaptation used for comparison, not a result attributed to CCTM.

Contaminated calibration and reference data have themselves received increasing attention in conformal inference. Clarkson et al. [ClarksonEtAl2024] study split conformal prediction when a fraction of calibration scores is drawn from a contaminating distribution, while Bashari, Sesia, and Romano [BashariEtAl2025] study conformal outlier detection under contaminated reference data and develop procedures to mitigate the associated loss of power. These works establish that contaminated reference data are not a new problem. Their objectives, however, differ from the one considered here: they do not construct a repeatedly reused fixed-reference predictive-rank martingale indexed by persistent unknown contamination identities, nor an anytime-valid lower-envelope procedure based on those identities.

Anytime-valid robustness under contamination also exists at a more general level. Saha and Ramdas [SahaRamdas2024] develop robust likelihood-ratio/e-value methods for composite hypotheses under Huber-type contamination, including sequentially adaptive contamination of the online observations. This is a stronger adversarial model along one dimension, but it represents a different nuisance structure. Their uncertainty lies in the conditional distribution of the arriving observations, whereas our setting contains a finite reused reference bank with a small unknown set of bad cells whose identities persist throughout the stream. General e-process theory also makes clear that pathwise domination by a valid process is not itself a new probability principle [RamdasEtAl2022]. Our question is instead whether the specific persistent structure of contaminated reference identities can be exploited to obtain a sharper finite-reference construction.

We consider a fixed observed bank of \(K\) reference values containing exactly \(m\) arbitrary static/exogenous replacements and \(n=K-m\) clean iid observations from an unknown continuous null distribution \(F\). The future null stream is iid from the same \(F\), independently of the clean reference observations. After sorting the observed bank, let \(C^\star\) denote the unknown set of sorted positions occupied by the contaminated values. For an incoming observation \(X_t\), let \(Q_t\in\{0,\ldots,K\}\) be its observable rank relative to all \(K\) references. Every candidate contamination-position set \(C\) induces a reconstructed rank

\[
R_t^{(C)}
=
Q_t-\#\{c\in C:c\le Q_t\}.
\]

The key observation is pathwise: for the true candidate \(C^\star\),

\[
R_t^{(C^\star)}
=
\#\{i\in G:Y_i\le X_t\},
\]

which is exactly the rank relative to the latent clean reference sample. Hence the true candidate inherits the clean predictive-rank martingale of Kuang and Xia.

This observation leads to the robust construction studied here. Let \(E_t^{(C)}\) denote the predictive-rank wealth generated from candidate \(C\), using the same pre-specified betting family for every candidate, and define

\[
\underline E_t
=
\min_{C:|C|=m}E_t^{(C)}.
\]

Although the pointwise minimum need not itself be a martingale or an e-process, it satisfies

\[
\underline E_t
\le
E_t^{(C^\star)}
\qquad\text{for every }t
\]

on every sample path. The true-candidate process is a nonnegative martingale under the null, so Ville's inequality immediately gives

\[
\Pr_{H_0}
\left(
\sup_{t\ge0}\underline E_t\ge\frac1\alpha
\right)
\le\alpha.
\]

Thus the method obtains finite-sample anytime threshold-crossing control without knowing either \(F\) or the contaminated positions. The guarantee is marginal over the random clean reference sample, as is the clean predictive-rank guarantee on which it is built; it is not a conditional-on-the-numerical-reference guarantee of the CCTM type.

The construction also exposes a combinatorial structure that is hidden when contamination is represented only as CDF uncertainty. Deleting a sorted reference at position \(c\) merges the two adjacent observed-rank bins \(c-1\) and \(c\). Consequently, a candidate set of \(m\) contaminated positions corresponds to a contiguous partition of the \(K+1\) observed-rank bins into \(K-m+1\) candidate clean-rank bins. For a fixed categorical bettor, the candidate log wealth depends only on the merged rank histogram and becomes additive across partition segments, leading to a dynamic program with approximately \(O(Km^2)\) time and \(O(Km)\) memory. The complete frozen experimental method uses a convex portfolio of betting strategies and is evaluated by candidate enumeration; we therefore restrict the polynomial-time claim to the fixed-categorical case.

The main contribution of this work is not a new rank law, a new form of Ville's inequality, or the observation that reference data can be contaminated. Rather, it is the use of **persistent contamination identities as a shared latent combinatorial object across repeated reference reuse**. To our knowledge, the literature surveyed above does not combine an already-contaminated finite fixed reference, candidate reconstruction of clean predictive ranks, and an anytime-valid robust lower envelope dominated by the true candidate process. Our contributions are therefore:

1. **Static-contamination extension of clean predictive-rank monitoring.** We formulate an exact fixed-reference model with unknown persistent contaminated positions and show that the true candidate reconstructs the clean predictive-rank process pathwise.
2. **Anytime-valid robust crossing construction.** A lower envelope over candidate predictive-rank wealths inherits finite-sample threshold-crossing control through pathwise domination by the true-candidate martingale, without requiring estimation of \(F\).
3. **Persistent partition structure.** We characterize candidate contamination sets as contiguous partitions of observed-rank bins and derive an additive closed form and dynamic-programming reduction for fixed categorical betting strategies.
4. **Finite-reference empirical evaluation.** Using frozen simulations and adversarially tuned confidence-band comparators, we quantify the power cost of unknown contamination identities relative to an oracle and compare it with robustification that discards identity information.

The empirical results suggest that the structural distinction can matter substantially at finite reference sizes. In the primary frozen scenario with \(K=32\), \(m=2\), horizon \(T=200\), and a \(\mathrm{Beta}(4,1)\) right shift, the robust static-coupling method crosses the level-\(0.05\) threshold on \(93.5\%\) of runs, compared with \(17.0\%\) for the strongest ex-post tuned confidence-band baseline and \(99.5\%\) for the oracle that knows the contaminated positions. Among detected paths, the corresponding median stopping times are 13, 78.5, and 8. For a stronger \(\mathrm{Beta}(8,1)\) shift, the proposed method and oracle both reach a crossing probability of one, while the strongest tuned confidence-band comparator reaches \(0.84\). These comparisons are intentionally scoped to the frozen simulation family and do not imply universal superiority over CCTM, conformal methods, or robust e-processes.

The remainder of the paper is organized as follows. Section 2 formalizes the contaminated fixed-reference model and recalls the clean predictive-rank result. Section 3 introduces candidate rank reconstruction and establishes anytime-valid robust crossing control. Section 4 develops the partition representation and the fixed-categorical dynamic program. Section 5 describes the frozen experimental design and confidence-band baselines. Section 6 reports finite-reference power and detection-delay results. Section 7 discusses scope, computational limitations, the distinction between static/exogenous and value-adaptive contamination, and the finite-reference information ceiling.
