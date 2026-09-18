# P−1 External Review Audit 07 — Gemini critique of robust predictive-rank CFAR

Status: **candidate downgraded to REFORMULATE / high novelty threat**

Date: 2026-09-18

## What the external review got right

1. A pointwise worst-case treatment that lets the adversary effectively change which references matter at each time can destroy power and ignores the static coupling of a fixed contaminated reference set.
2. The fixed contamination pattern induces latent temporal structure; a sharp method would need to exploit that coupling rather than re-solve a one-step worst case independently at every time.
3. Power under adversarial high-valued reference contamination is a central issue and must be analyzed explicitly.
4. A useful theorem would need finite-sample anytime validity plus a nontrivial power/growth statement.

## Important corrections

### 1. The proposed pointwise-min proof is not automatically valid

The suggested formula

e_t^rob = min_{r in interval_t} e_t^PRM(r)

is not justified merely because the current clean rank lies in that interval. Predictive-rank martingale factors depend on the **past clean rank history** through the predictive null law/state. A factor evaluated using the observed contaminated history is not generally the same factor that would have been used on the latent clean history.

To obtain pathwise domination, the minimization would have to range over entire compatible latent histories/states, not just the current rank. That may lead to a dynamic program, but the one-line substitution is not yet a proof.

### 2. “Conditional validity is impossible” is false as stated

Shaer, Bar, Prinster & Romano (2026), *Testing For Distribution Shifts with Conditional Conformal Test Martingales* (arXiv:2602.13848), explicitly construct an anytime-valid method for a fixed reference set and describe it as valid conditional on the reference data by accounting for finite-reference CDF estimation uncertainty through uniform confidence bands.

Thus reference-conditional anytime validity is not categorically impossible.

### 3. Static bounded replacement contamination admits an immediate CDF-band robustification

If an observed reference empirical CDF \tilde F_K is obtained from an original clean empirical CDF \hat F_K by replacing at most M of K points, then pathwise

sup_x |\tilde F_K(x) - \hat F_K(x)| <= M/K.

Combining this with a DKW band for the original clean sample gives, with the same reference-sample coverage probability,

sup_x |\tilde F_K(x) - F(x)| <= epsilon_K + M/K.

The conditional-CTM framework explicitly allows a general uniform CDF confidence band. Therefore, under a replacement-contamination model, widening the reference uncertainty band by M/K appears to give a **routine valid robustification** of the CCTM construction.

This does not settle whether an *exact predictive-rank* solution is routine, but it seriously threatens the broader claim “anytime-valid fixed-reference detection under bounded adversarial contamination.”

### 4. The subset-mixture argument in the external review is incorrect

If only one subset S* is guaranteed clean, then only E_t^(S*) is guaranteed to be an e-process. An arithmetic mixture

(1/N) sum_S E_t^(S)

is not automatically valid when the other components may be invalid and arbitrarily large.

A mixture of e-processes is valid when **all** mixed components are valid under the null. “At least one valid component” is insufficient.

Therefore the claimed combinatorial-mixture baseline and its stated factor-N penalty are not established as written.

### 5. The +infinity contamination example is a power warning, not an impossibility theorem

Putting M contaminated references at +infinity caps the observed rank relative to all K references, but this does not imply that every robust detector has zero power. A detector can calibrate its upper-tail evidence relative to the effective clean-rank range or use an uncertainty-set CDF method.

A true impossibility result would need to show overlap/non-identifiability between the robust null family and the target alternative family, not only failure of a bettor that requires the top M observed ranks.

### 6. One cited robust-e-values reference could not be verified

The external review names “Gaudenzi et al. (2023), Robust e-values for testing in the presence of contamination.” Targeted search did not verify that exact paper.

A directly relevant verified work is Saha & Ramdas, *Robust likelihood ratio tests for composite nulls and alternatives* (arXiv:2408.14015; later IEEE Transactions on Information Theory), which develops sequential e-value/supermartingale tests under epsilon/TV contamination.

## Updated candidate status

The broad candidate

> fixed contaminated reference + anytime-valid sequential detection

is **too threatened** because CCTM plus the deterministic M/K ECDF perturbation bound appears to yield a routine robust confidence-band construction.

A narrower candidate remains possible:

> an **exact finite-sample predictive-rank** e-process under at most M static adversarial replacements, exploiting latent contamination coupling to be strictly sharper/more powerful than the widened-band CCTM baseline.

This narrower candidate is worth only one final theorem-level comparison.

## Required next kill-test

1. Formalize the CCTM + M/K contamination-band baseline and prove its validity.
2. For small K,M, compute the exact latent-state predictive-rank envelope.
3. Compare the exact envelope to the CCTM band:
   - if no meaningful sharpness/power gain appears, kill the candidate;
   - if the exact static-coupling structure gives a provably sharper betting set or positive growth region, continue.

No hardware work is justified at this stage.
