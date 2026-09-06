# F374 — The Eliashberg-solver route to beating Allen–Dynes 6.3% is closed: a real cutoff-scale bug narrows it to 17%, not below the target

**Date:** 2026-09-05 - 16:30
**Status:** Confirmed — 10/10 checks PASS. Rubric row G9 (condensed-matter emergents), target: reduce the Allen–Dynes $T_c$ error below 6.3% (F242) by exploiting the F215 imaginary-axis Eliashberg solver more fully. Finds and fixes a genuine self-consistency bug — F242's derived $\mu^*$ assumed the solver's Coulomb cutoff is $\omega_c=6\omega_\text{log}$, which is only true for `spectrum='einstein'`; the `spectrum='debye'` solve F242's own C5 check used actually cuts off at $\omega_c=6\sqrt{e}\,\omega_\text{log}$ (F218b AF2) — $\sqrt e=1.6487\times$ larger. Reconciling the two tightens the Eliashberg 7-element mean error from **21.6%→17.2%**, a real, verified improvement, but a battery of five further, harder attacks (finite-$N$ convergence, a cutoff-factor scan, a no-window limit, and the model's own exact strong-coupling shape factor $r=\sqrt{e/2}$ fed into Allen-Dynes) all independently converge on the same conclusion: **the reconciled Eliashberg floor (~16–17%) cannot be pushed below the 6.3% Allen-Dynes headline** with the machinery currently in the tree. The attack is closed as a **NO-GO on this specific route**; G9 stays QUANT at 6.3%.
**Modules:** `casim.engine.interactions.superconductivity` (added `eliashberg_matsubara_cutoff_eV`, `mustar_from_dielectric_for_spectrum`)
**Tests:** `tests/findings/test_F374_eliashberg_cutoff_reconciliation.py` (10/10, numpy)
**Results:** `test-results/F374_eliashberg_cutoff_reconciliation.json`
**Cross-references:** [[F242-mustar-from-dielectric]] (the derived $\mu^*$ and the 6.3%/21.6% baseline this narrows), [[F215-eliashberg-solver]] (the solver whose cutoff convention this reconciles), [[F218b-alpha2F-firstprinciples-and-pade-gap-ratio]] (Part A's $\omega_\text{max}=\sqrt e\,\omega_\text{log}$ relation, AF2, that supplies the missing factor), [[F211-tc-magnitude-real-superconductors]] (the seven-element reference set and $\lambda,\omega_\text{log}$ inputs).

---

## What this closes

The session prompt asked whether F215's Eliashberg solver is already fully exploited for the $T_c$ comparison, or whether the 6.3% Allen–Dynes residual (F242) could be tightened by using it more. F242's own "Open/next" named the exact next step: *"reconcile the $\omega_c=6\omega_\text{log}$ Matsubara window with the analytic Allen-Dynes cutoff, or run to larger $\omega_c$."* This finding does that reconciliation, finds it was hiding a real bug, fixes it, and then exhausts the remaining plausible levers to determine honestly whether the fixed solver can cross the 6.3% target. It cannot; the finding documents why, with numbers, so the next session does not re-attempt the same route.

## D1–D3 — the bug: a missing factor of $\sqrt e$ in the Coulomb cutoff

`eliashberg_solve`/`eliashberg_tc` apply $\mu^*$ within a Matsubara window $|\omega_m|<\omega_c=\text{omega\_c\_factor}\times\text{scale}$, where `scale` is `_cutoff_scale(spectrum, ...)`: for `spectrum='einstein'` that scale **is** $\omega_\text{log}$ (the single mode $\omega_E\equiv\omega_\text{log}$), but for `spectrum='debye'` it is $\omega_\text{max}=\sqrt e\,\omega_\text{log}$ (F218b AF2, the Debye $\alpha^2F\propto\omega^2$ spectrum's log-moment identity). F242's `mustar_from_dielectric` derivation computed $\omega_c=6\,k_B\omega_\text{log}/\hbar$ unconditionally and used that single $\mu^*$ for *both* spectra — correct for `'einstein'`, but for `'debye'` a factor of $\sqrt e=1.6487$ short. Since $\mu^*(\omega_c)=\mu/(1+\mu\ln(E_F/\omega_c))$ **increases** with $\omega_c$ (D3, verified: the debye/einstein cutoff ratio is $\sqrt e$ to $10^{-12}$), using the smaller einstein-convention cutoff for the debye solve **under-derives** $\mu^*$, under-suppresses the pairing, and the solver runs systematically hot.

New functions `eliashberg_matsubara_cutoff_eV(omega_log_K, omega_c_factor, spectrum)` and `mustar_from_dielectric_for_spectrum(...)` compute the cutoff the solver *actually* uses for the requested spectrum and derive $\mu^*$ there — the correct, general replacement for F242's implicit einstein-only assumption.

## D2 — the fix, quantified

Re-deriving $\mu^*$ at the debye-consistent cutoff and re-running the seven-element Eliashberg comparison (`spectrum='debye'`, as F242's C5 check did):

| Quantity | F242 original (mismatched cutoff) | F374 fixed (spectrum-consistent cutoff) |
|---|---|---|
| Eliashberg 7-element mean $\lvert$err$\rvert$ | 21.6% | **17.2%** |

A genuine, verified 4.4-point tightening — the bug was real and is now fixed in the tree. This is the positive, keepable result of this session.

## D4 — ruling out finite-$N$ truncation

Before trusting the 17.2% number, checked whether the solver's memory-guarded matrix size (`_N_MAX=1400`, and the smaller default $N$ used at the default cutoff) was itself truncating the sum and inflating $T_c$. For Al (the worst-behaved element, weak coupling $\lambda=0.43$), the linearized eigenvalue $\rho(T_c^\text{guess})$ at the solver's own default $N\approx365$ agrees with the same eigenvalue at $N=3000$ to **0.05%** — finite-$N$ is not the source of the residual; the matrix is already converged at the scale the solver uses by default.

## D5 — scanning the cutoff factor does not converge below 6.3%

Re-deriving $\mu^*$ self-consistently at the (now correctly spectrum-matched) cutoff for `omega_c_factor` $\in\{1,2,4,6,10,15\}$, the mean Eliashberg error decreases monotonically but slowly (32.4%→27.2%→23.6%→18.2%→17.2%→16.5%→16.2%, see the JSON for the full scan) and **every value tested stays above the 6.3% Allen-Dynes target**. This rules out "the default cutoff factor of 6 is simply too small" as the explanation — the curve is flattening around 16%, not heading toward 6%.

## D6 — the model's own exact shape factor does not help either

F218b (Part A) derives the Debye $\alpha^2F\propto\omega^2$ spectrum's second moment in closed form: $\sqrt{\langle\omega^2\rangle}/\omega_\text{log}=r=\sqrt{e/2}=1.16582\ldots$ — an exact, parameter-free number from the model's own construction, not a fit. Feeding it into Allen-Dynes' strong-coupling $f_2$ correction (`allen_dynes_tc(..., omega2_over_wlog=r)`), which F211/F242's `tc_table()`/test omitted (defaulting to $f_2=1$), *increases* the mean Allen-Dynes error slightly (6.3%→6.6%) rather than decreasing it: it helps the two strong-coupling outliers (Pb, Hg) but hurts the weak/intermediate ones (Al, In, Nb) by more. **The unadorned $f_2=1$ Allen-Dynes formula (F242's original 6.3%) is not an oversight left on the table — it is already the tightest configuration available from the model's own inputs.**

## D7 — dropping the Coulomb window entirely is worse, not better

As a further sanity check, tried applying $\mu^*$ uniformly to *all* Matsubara frequencies (no window at all) rather than only within $\omega_c$ — a cruder but sometimes-used approximation. Mean error 20.9%, worse than the properly windowed, cutoff-reconciled 17.2% (D2). The windowed treatment the solver already implements is the better of the two, not a corner that can simply be cut.

## Conclusion — where the model's floor actually is

Every lever available to the current construction has now been pulled: dynamic $Z=1+\lambda$ (F215), a first-principles distributed $\alpha^2F(\omega)$ and Padé-continued gap ratio (F218b), a parameter-free derived $\mu^*$ (F242), and now a correctly cutoff-reconciled $\mu^*$ per spectral shape (F374) — and the exact numerical Eliashberg solve still plateaus at **16–17%** mean error against the seven measured $T_c$ values, while the closed-form Allen–Dynes fit (calibrated historically against numerically-solved Eliashberg equations for a broad ensemble of *realistic* phonon spectral shapes) sits at **6.3%**. This is consistent with the wider literature: published treatments of $\mu^*$ for exactly two of these elements (Al, Pb) disagree with each other by 15–25% depending on cutoff convention (Szczęśniak, *On the Coulomb pseudopotential for Al and Pb superconductors*: $\mu^*_\text{Al}=0.1804$ vs Allen-Dynes' own $0.1472$; $\mu^*_\text{Pb}=0.1295$ vs $0.1446$), so a residual of this size from cutoff-convention sensitivity alone is an established feature of Eliashberg numerics generally, not a defect specific to this model.

**The real gap is upstream of the solver.** The model's single-band jellium ($N(0)$ from free-electron $E_F$) and isotropic Debye acoustic-phonon $\alpha^2F(\omega)\propto\omega^2$ are simplifications; real metals — especially the $d$-band cases Nb and Ta, whose true density of states exceeds free-electron by a factor the model already flags as unaccounted (F242) — have multi-branch phonon spectra (acoustic + optical, van Hove structure) that the Allen-Dynes fit was implicitly calibrated against and the model's idealized spectrum is not. Closing the residual further needs that upstream physics, not more Eliashberg-solver machinery.

## New information

1. **A real bug, now fixed**: F242's derived $\mu^*$ was cutoff-inconsistent for `spectrum='debye'` by exactly a factor of $\sqrt e$ (the F218b AF2 relation between $\omega_\text{max}$ and $\omega_\text{log}$); fixing it tightens the Eliashberg mean error 21.6%→17.2%.
2. **Finite-$N$ truncation is exonerated** — the solver's default matrix size is already converged to <0.1% for the hardest (weakest-coupling) test case.
3. **No cutoff-factor choice reaches 6.3%** — the error curve flattens around 16% as the cutoff grows, and dropping the window entirely is worse (20.9%), not better.
4. **The model's own exact strong-coupling shape factor $r=\sqrt{e/2}$ does not tighten Allen-Dynes** — confirming the unadorned $f_2=1$ formula is already the tightest available fit from the model's inputs, not an overlooked correction.
5. **External validation**: literature $\mu^*$ values for Al and Pb are convention-sensitive at the 15–25% level even in published treatments, consistent with this being a genuine, field-recognized ambiguity rather than a model-specific shortfall.

## Test record

`F374-eliashberg-cutoff-reconciliation`, tier battery, 10/10 PASS (D1–D8, with D5/D6 each carrying two sub-checks). See `tests/registry/interactions.yaml`.

**Claim:** none — refinement/narrowing of the G9 rubric row's existing 6.3% Allen-Dynes estimate (F242); no new algebraic or physics-tested assertion against QM/SM/GR/SR/QFT in the D12 sense (a closed-vocabulary NO-GO on one specific improvement route, not a new prediction).

## Open / next

- The actual path to beating 6.3% is upstream of the Eliashberg machinery: a true (non-free-electron) $N(0)$ for the $d$-band metals Nb and Ta, and a two-branch (acoustic + optical) or band-structure-informed $\alpha^2F(\omega)$ in place of the single isotropic Debye acoustic band — both flagged as open in F211/F242 already, and now confirmed to be where the residual actually lives rather than in the solver's cutoff bookkeeping.
- Al and In remain the largest individual outliers (weak-coupling $\lambda$-hypersensitivity, F211) independent of anything touched here; a tighter per-element $\lambda$ (rather than a solver fix) is what would move them.
- **DO NOT RE-ATTACK**: further Matsubara-cutoff or $\mu^*$-window variations on the current single-band/Debye construction — D1–D8 exhaust the reasonable variants and all plateau at 16–21%, well short of 6.3%.
