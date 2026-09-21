# P−1 Final novelty sweep — static contaminated fixed reference + anytime ranks

Date: 2026-09-21

Status: **GO TO MANUSCRIPT WITH A NARROW NOVELTY CLAIM**

This is the final targeted novelty search before drafting the Abstract and Introduction.

The purpose is not to prove a negative (“no related paper exists anywhere”), which a literature search cannot do. The purpose is to look aggressively for a theorem or method that already contains the same structural combination as the frozen LIMEN-RF paper core.

## 1. Exact equivalence target

A prior result is potentially fatal only if it substantially contains all or nearly all of the following:

**A. Pre-contaminated fixed reference.**
A finite reference/calibration bank already contains bad observations before online monitoring starts.

**B. Persistent unknown contamination identities.**
The same unknown bad reference cells remain in the reused bank over the online stream.

**C. Candidate-wise rank reconstruction.**
Possible contamination identities/positions induce candidate clean rank sequences.

**D. Anytime sequential validity.**
Evidence is valid under optional stopping / continuous monitoring, e.g. via a martingale, supermartingale, e-process, or equivalent anytime construction.

**E. Robust crossing via the persistent candidate.**
The true candidate supplies a valid clean sequential process and a worst-case/lower-envelope construction inherits crossing control by pathwise domination.

A paper that contains only contaminated references, only ranks, only sequential monitoring, or only robust e-processes does not by itself subsume LIMEN-RF.

---

## 2. Search families used

The final sweep used combinations of:

- "contaminated reference" + sequential + rank + martingale;
- "fixed reference" + contamination + e-process;
- "predictive rank" + contamination;
- "conformal martingale" + contaminated calibration/reference;
- "Huber contamination" + sequential e-value/e-process;
- "reference sample contamination" + sequential change detection;
- "Phase I contamination" + nonparametric/rank control chart;
- "contaminated reference cells" + CFAR/order statistic/censoring;
- "lower envelope" + martingale/e-process + contamination;
- "persistent contamination" + rank/sequential detection.

Sources searched included arXiv, IEEE/Elsevier/Springer/Wiley publisher pages, PMLR, PMC, and broad scholarly web indexes.

---

## 3. Highest-threat sequential / anytime literature

### 3.1 Kuang & Xia (2026)
**Anytime-Valid Distribution Shift Detection via Predictive Rank Martingales**, arXiv:2609.00536.

**Contains:** clean fixed reference; exact repeated-reference predictive rank law; predictable rank betting; nonnegative martingale; anytime marginal type-I control; finite-reference power ceiling.

**Does not contain in the checked source:** an initially contaminated fixed reference bank with unknown persistent bad-cell identities, candidate deletion/reconstruction, or a robust lower envelope over contamination positions.

**Threat:** HIGH to the original clean-PRM claim; **not fatal** after attribution.

**Disposition:** their Theorem 2.1 is imported background. LIMEN-RF novelty must start after the clean-reference theorem.

---

### 3.2 Shaer, Bar, Prinster & Romano (2026)
**Testing For Distribution Shifts with Conditional Conformal Test Martingales**, arXiv:2602.13848.

**Contains:** clean iid fixed reference; finite-reference ECDF confidence bands; robust betting against CDF estimation error; reference-conditional/PAC anytime guarantee.

**Contamination meaning in that paper:** post-shift online samples contaminating a *growing* reference used by standard CTMs. CCTM avoids that by keeping a clean fixed \(D_0\).

**Does not contain:** arbitrary bad cells already present in the fixed \(D_0\), persistent unknown contamination positions, or candidate-reconstructed PRMs.

**Threat:** HIGH as a generic fixed-reference confidence-band baseline; **not fatal**.

**Disposition:** our contaminated-reference DKW and CCTM-style baselines are our adaptations and must be labeled that way.

---

### 3.3 Saha & Ramdas (2024/2025)
**Huber-Robust Likelihood Ratio Tests for Composite Nulls and Alternatives**, arXiv:2408.14015; later IEEE TIT.

**Contains:** e-value/supermartingale methods with anytime validity under strong contamination models. Their sequential null can allow the conditional distribution of each new online observation, given the past, to lie in an \(\epsilon\)-TV neighborhood of the ideal null.

**Important distinction:** this is robustness to contamination/model misspecification of the *sequential observations/distribution*. It does not exploit a finite reused reference bank with fixed latent bad-cell identities.

**Does not contain:** candidate sorted-position reconstruction of a contaminated reference bank or persistent-reference coupling.

**Threat:** MEDIUM-HIGH as general robust e-process theory; **not equivalent**.

**Disposition:** cite as evidence that robust anytime inference under contamination exists generally. Our claim is a rank/reference-structure specialization with a different nuisance geometry.

---

### 3.4 Ramdas, Ruf, Larsson & Koolen (2022)
**Testing exchangeability: Fork-convexity, supermartingales and e-processes**, International Journal of Approximate Reasoning 141, 83–109.

**Contains:** safe e-processes, pathwise domination concepts, sequential exchangeability testing, and explicit examples where the valid process is not itself a supermartingale but is dominated by one.

**Does not contain:** contaminated fixed reference identities or our candidate-rank construction.

**Threat:** MEDIUM conceptually because it warns that “dominated valid process” is established general methodology.

**Disposition:** do not claim pathwise domination itself as a new probability principle. Claim the **static-reference candidate structure and its resulting construction**.

---

### 3.5 Vovk et al. (2021)
**Retrain or not retrain: Conformal test martingales for change-point detection**, PMLR 152.

**Contains:** conformal/exchangeability martingales for online change detection with anytime validity.

**Does not contain:** a fixed pre-contaminated reference model with unknown persistent cell identities.

**Threat:** MEDIUM background.

---

### 3.6 Vovk (2021)
**Testing Randomness Online**, Statistical Science 36(4), 595–611.

**Contains:** general conformal martingale framework for online tests of randomness/exchangeability and change detection.

**Does not contain:** the LIMEN-RF contaminated-reference structure.

**Threat:** LOW-MEDIUM background.

---

## 4. Contaminated-reference conformal literature

### 4.1 Bashari, Sesia & Romano (2025)
**Robust Conformal Outlier Detection under Contaminated Reference Data**, ICML 2025 / arXiv:2502.04807.

**Contains:** directly contaminated reference/calibration data; finite numbers of inliers and outliers; analysis of conservative behavior and power loss; active labeling/trimming to recover power.

**Model distinction:** the paper emphasizes realistic non-adversarial contamination and offline/new-point conformal outlier detection.

**Does not contain in the checked source:** an indefinitely reused fixed reference with predictive-rank dependence, an anytime martingale/e-process, candidate contamination-position reconstruction, or a lower-envelope crossing theorem.

**Threat:** HIGH to any broad claim that “contaminated reference data is unexplored”; **not fatal** to the sequential candidate-coupling claim.

---

### 4.2 Clarkson, Xu, Cucuringu, Swan & Reinert (2024/2025)
**Split Conformal Prediction under Data Contamination**, arXiv:2407.07700 / PMLR.

**Contains:** contaminated calibration scores under a Huber-type iid mixture
\[
(1-\epsilon)\pi_1+\epsilon\pi_2,
\]
coverage/efficiency bounds and contamination-robust conformal adjustments.

The paper explicitly assumes contamination independently across observations.

**Does not contain:** persistent unknown deterministic reference identities shared across every future online decision; predictive-rank martingales; anytime lower-envelope crossing.

**Threat:** MEDIUM-HIGH neighboring robust calibration literature; **not equivalent**.

---

## 5. Sequential monitoring with contaminated training / Phase-I samples

### 5.1 El Sibai et al. (2020)
**Efficient anomaly detection on sampled data streams with contaminated phase I data**, Internet Technology Letters 3:e205.

**Contains:** exactly the practical concern that a learning/Phase-I reference can already contain outliers and then harm Phase-II online anomaly detection. Proposes an EWMA/change-point based cleaning/monitoring approach.

**Does not contain:** distribution-free fixed-reference predictive ranks or finite-sample anytime martingale control.

**Threat:** MEDIUM to novelty of the *problem statement*; LOW to theorem equivalence.

---

### 5.2 Díaz-Pulido, Cordero-Franco & Tercero-Gómez (2026)
**Nonparametric multivariate control chart with guaranteed in-control performance and cautious learning**, Computers & Industrial Engineering 218, 112124.

**Contains:** sequential rank statistics, distribution-free monitoring, guaranteed in-control performance, and cautious learning intended to prevent reference-sample contamination.

**Crucial distinction:** it cautiously updates/learns the reference and uses control-chart calibration/approximations; it is not a fixed already-contaminated reference with unknown persistent identities.

**Threat:** MEDIUM as recent rank-based sequential monitoring; **not equivalent**.

---

### 5.3 Wang & Ning (2024)
**Nonparametric Shiryaev-Roberts change-point detection procedures based on modified empirical likelihood**, Journal of Applied Statistics 51(13), 2558–2591.

**Contains:** nonparametric sequential change detection with training samples used to estimate pre/post-change distributions.

**Does not contain:** a persistent arbitrary contaminated training/reference subset with candidate rank reconstruction or anytime e-process guarantee.

**Threat:** LOW-MEDIUM sequential nonparametric neighbor.

---

### 5.4 Phase-I robust SPC literature
Representative works include robust Phase-I estimators/control charts and recent studies of contaminated historical samples.

**Contains:** extensive recognition that contaminated historical/reference data degrade Phase-II monitoring, often addressed by robust estimation, trimming, cleaning, or simulation-calibrated limits.

**Does not contain in the checked representative sources:** the exact LIMEN-RF PRM + persistent candidate lower-envelope construction.

**Threat:** LOW to exact theorem, but important for motivation and honest positioning.

---

## 6. Classical CFAR / contaminated reference-cell literature

### 6.1 Rohling (1983)
**Radar CFAR Thresholding in Clutter and Multiple Target Situations**, IEEE Transactions on Aerospace and Electronic Systems AES-19(4), 608–621. DOI 10.1109/TAES.1983.309350.

**Contains:** classical OS-CFAR; order-statistic robustness when multiple interfering targets occupy the reference window.

**Does not contain:** repeated fixed-reference predictive dependence or anytime sequential martingale guarantees.

**Threat:** HIGH to any claim that rank/order-statistic handling of contaminated reference cells is new; **not fatal** to LIMEN-RF sequential theorem.

---

### 6.2 Al-Hussaini & El-Mashade (1996)
**Performance of cell-averaging and order-statistic CFAR detectors processing correlated sweeps for multiple interfering targets**, Signal Processing 49(2), 111–118.

**Contains:** CA/OS-CFAR performance with one or more interfering target returns in reference cells.

**Does not contain:** distribution-free predictive ranks, optional-stopping validity, or persistent candidate identity inference.

**Threat:** MEDIUM CFAR background.

---

### 6.3 El Mashade (1998)
**Detection analysis of linearly combined order statistic CFAR algorithms in nonhomogeneous background environments**, Signal Processing 68(1), 59–71. DOI 10.1016/S0165-1684(98)00057-7.

**Contains:** LCOS/trimmed-order-statistic CFAR in nonhomogeneous and contaminated reference channels.

**Does not contain:** our sequential repeated-reference dependence or anytime lower-envelope theorem.

**Threat:** MEDIUM CFAR background.

---

### 6.4 Farrouki & Barkat (2007)
**Automatic censored mean level detector using a variability-based censoring with non-coherent integration**, Signal Processing 87(6), 1462–1473. DOI 10.1016/j.sigpro.2006.12.012.

**Contains:** automatic censoring of ranked reference observations in multiple-target/nonhomogeneous environments.

**Does not contain:** candidate-wise predictive martingales or anytime-valid crossing.

**Threat:** MEDIUM to claims about censoring/identifying interference; LOW to theorem equivalence.

---

### 6.5 Later robust CFAR families
Trimmed-mean, censored-mean, variability-index, maximum-reference-cell, truncated-statistic and hybrid CFAR methods all address nonhomogeneous/contaminated reference windows in various ways.

**Common distinction:** they set one-step/adaptive thresholds from local reference statistics under specified clutter/target models. They do not model repeated reuse of the same finite contaminated bank via the exact predictive-rank dependence and an anytime e-process-style construction.

**Threat:** background, not equivalence.

---

## 7. Threat matrix against the exact LIMEN-RF combination

Legend:
- ✓ explicit/central;
- ~ related but materially different;
- — not present in checked source.

| Work | A pre-contaminated fixed ref | B persistent unknown identities | C candidate rank reconstruction | D anytime sequential validity | E true-candidate lower-envelope |
|---|---:|---:|---:|---:|---:|
| Kuang–Xia PRM | — | — | — | ✓ | — |
| Shaer et al. CCTM | — | — | — | ✓ | — |
| Saha–Ramdas robust LR | — | — | — | ✓ | — |
| Ramdas et al. exchangeability e-process | — | — | — | ✓ | ~ general domination ideas |
| Vovk conformal martingales | — | — | — | ✓ | — |
| Bashari et al. contaminated reference | ✓ | ~ random/non-adversarial labels | — | — | — |
| Clarkson et al. contaminated split conformal | ✓ | — iid mixture | — | — | — |
| El Sibai et al. contaminated Phase I | ✓ | ~ | — | ~ online monitoring | — |
| Díaz-Pulido et al. cautious sequential ranks | ~ | — | — | ~ control-chart guarantee | — |
| Rohling OS-CFAR | ✓ reference interferers | ~ persistent within decision window | — | — | — |
| Al-Hussaini/El-Mashade CFAR | ✓ | ~ | — | — | — |
| El Mashade LCOS-CFAR | ✓ | ~ | — | — | — |
| Farrouki/Barkat censored CFAR | ✓ | ~ | — | — | — |

**Result:** no checked source contains columns A–E together, and no source found in the targeted exact-phrase searches exposed candidate deletion/reconstructed PRMs or an equivalent persistent-candidate lower-envelope theorem.

---

## 8. What is NOT novel

The manuscript must explicitly avoid claiming novelty for:

1. fixed-reference rank monitoring;
2. the Pólya/Dirichlet predictive rank law;
3. generic predictable PRM/e-process construction;
4. Ville's inequality;
5. convex martingale portfolios;
6. robust sequential testing under contamination in general;
7. contaminated calibration/reference data as a problem;
8. order-statistic/censoring robustness to interfering CFAR reference cells;
9. pathwise domination as a general probability technique;
10. DKW confidence bands.

---

## 9. Remaining novelty candidate

The narrow contribution that survived the search is:

> **An anytime-valid sequential construction for an already-contaminated, repeatedly reused finite reference bank, which treats the unknown static contamination identities as one persistent latent combinatorial object. Candidate deletion reconstructs a clean predictive-rank process for the true candidate, and a lower envelope over candidate PRM wealths obtains robust threshold-crossing control by pathwise domination.**

Associated secondary structural contribution:

> Static sorted contamination positions correspond to persistent contiguous partitions of the observed-rank bins; for a fixed categorical bettor this yields an additive objective and a polynomial dynamic program.

The DP claim must remain scoped to the fixed categorical bettor unless the full mixture is separately optimized.

---

## 10. Novelty decision

### Search outcome

**NO EQUIVALENT THEOREM FOUND IN THIS TARGETED SWEEP.**

This is not a claim of exhaustive mathematical uniqueness. It means the most obvious neighboring literatures and exact search combinations did not reveal a result that already contains the frozen LIMEN-RF theorem stack.

### P−1 decision

**GO TO MANUSCRIPT, with a narrow and attributed novelty claim.**

The paper should say:

> Building on the clean fixed-reference predictive-rank martingale of Kuang and Xia, we consider a different setting in which the reference bank itself contains an unknown fixed set of static/exogenous replacements. The contribution is to exploit the persistence of those latent contamination identities across repeated reference reuse through candidate-reconstructed ranks and a robust lower envelope with anytime-valid crossing control.

Do **not** say “the first method ever” unless a journal reviewer/later expanded systematic search provides enough basis. Safer wording is:

> “To our knowledge, we are not aware of prior work combining …”

followed by the exact A–E combination.

---

## 11. Manuscript consequence

The novelty firewall is now sufficiently resolved to start the Abstract and Introduction.

The Introduction should present the literature in this order:

1. contaminated reference cells are classical in CFAR and robust monitoring;
2. contaminated calibration data is established in conformal inference;
3. anytime rank martingales with a *clean* fixed reference are established by Kuang–Xia;
4. CCTM handles clean fixed-reference estimation uncertainty by confidence bands;
5. robust e-processes under general contamination exist (Saha–Ramdas);
6. the gap is the **persistent identity structure of a finite reference bank that is already contaminated before monitoring**.

That is the exact location of the LIMEN-RF contribution.
