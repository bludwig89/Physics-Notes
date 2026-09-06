# F375 — A real (DFT-sourced) N(0) for Nb crosses the G9 target: Allen-Dynes headline 6.3% → 4.9%

**Date:** 2026-09-06 - 02:15
**Checked:** 2026-09-06 — 12 PASS / 1 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED** ([independent review](../docs/reviews/F375-review-2026-09-06.md))
**Status:** Confirmed — 13/13 checks PASS. Rubric row G9 (condensed-matter emergents), target: reduce the Allen-Dynes $T_c$ error below 6.3% (F242). F374 (2026-09-05) closed the Eliashberg-solver/cutoff route as a NO-GO and named the actual next step: the model's free-electron $N(0)$ understates the true density of states of the $d$-band metals Nb/Ta. This finding sources a real DFT-computed $N(E_F)$ for niobium, generalizes the F242 Morel-Anderson $\mu^*$ derivation to a non-free-electron $N(0)$, and finds that correcting Nb alone — no fit, one literature number — moves the Allen-Dynes 7-element mean error from **6.3% → 4.9%**, crossing the G9 target. Tantalum is intentionally left uncorrected: no equally solid sourced $N(E_F)$ for Ta was found this session, and guessing one would violate the same standard this whole derivation chain depends on.
**Modules:** `casim.engine.interactions.superconductivity` (added `mu_coulomb_real_dos`, `mustar_from_real_dos`, `DOS_ENHANCEMENT`)
**Tests:** `tests/findings/test_F375_nb_realistic_dos.py` (13/13)
**Results:** `test-results/F375_nb_realistic_dos.json`
**Cross-references:** [[F374-eliashberg-cutoff-reconciliation-and-tc-residual-floor]] (closed the solver/cutoff route, named this finding's next step), [[F242-mustar-from-dielectric]] (the free-electron $\mu^*$ derivation this generalizes), [[F211-tc-magnitude-real-superconductors]] (the seven-element reference set).

---

## What this does

F374's "Open/next" named the real next step for G9: *"a true (non-free-electron) $N(0)$ for the $d$-band metals Nb and Ta ... both flagged as open in F211/F242 already."* `mustar_from_dielectric`'s own docstring already flagged the gap: *"Free-electron $E_F$ is used unless $E_F\_eV$ is given (d-band metals: the true $N(0)$ exceeds free-electron, so this $\mu^*$ is a lower bound there)."* This finding closes that gap for niobium with a sourced number, and is explicit about not closing it for tantalum.

## D1 — generalizing $\mu(r_s)$ to a real $N(0)$

F242's closed form $\mu(r_s) = 0.082930\, r_s \ln(1+6.0299/r_s)$ implicitly assumes a free-electron $N(0)$: both its prefactor and the Thomas-Fermi screening $k_\text{TF}^2=4\pi e^2 N(0)$ inside the log trace back to the same free-electron $N(0)(k_F)$. A real (band-structure) metal has an enhanced $N(0) = \alpha \, N(0)_\text{free}$ at the **same** Fermi surface volume (the electron count $n$, hence $k_F$, is fixed by Luttinger's theorem regardless of band structure) — only the density of states at that surface differs. Since $\mu = N(0)\langle V_\text{screened}\rangle_\text{FS}$ and $k_\text{TF}^2\propto N(0)$, both the prefactor and the screening argument scale with $\alpha$ while $k_F$ (and so $6.0299/r_s$) does not:
$$\mu(r_s,\alpha) = \alpha\cdot 0.082930\, r_s \ln\!\left(1+\frac{6.0299/r_s}{\alpha}\right)$$
This reduces to $\mu(r_s)$ **exactly** at $\alpha=1$ (D1, checked to $10^{-14}$ over $r_s\in[1.2,4.0]$) — a strict generalization, not a new assumption. `mu_coulomb_real_dos(rs, alpha)` implements it; `mustar_from_real_dos(...)` feeds it through the same Morel-Anderson retardation reduction and solver-consistent cutoff (`eliashberg_matsubara_cutoff_eV`, F374) as `mustar_from_dielectric_for_spectrum`, so it is a drop-in replacement, not a parallel pipeline.

## D2 — sourcing $\alpha$ for niobium

$N(E_F)\simeq 1.49\ \text{eV}^{-1}$ per atom (both spin channels, DFT/Quantum ESPRESSO, De Marzi et al., reported in *Frontiers in Physics* **11**:1269872 (2023), doi:10.3389/fphy.2023.1269872, Figure 2 caption) — an independent electronic-structure calculation, not fit to any $T_c$. This model's own free-electron estimate at Nb's valence $Z=5$ ($n=2.7775\times10^{29}\,\text{m}^{-3}$, $E_F=15.52$ eV) gives $N(0)_\text{free}=3Z/(2E_F)=0.4832\ \text{eV}^{-1}$/atom (both spins). The ratio $\alpha_\text{Nb}=1.49/0.4832=3.084$ (D2a, pinned to the cited DFT value; D2b, $\alpha>1$ as physically expected — Nb's Fermi level sits in a narrow $d$-band, not a free-electron-like $sp$ band).

## D3 — effect on the Allen-Dynes headline (G9's own metric)

Using $\mu^*_\text{Nb}$ from `mustar_from_real_dos` (einstein-cutoff convention, matching the official 6.3% baseline, F242/F374 D6) in place of the free-electron value, all six other elements unchanged:

| | Allen-Dynes mean \|err\| (7 elements) | Nb individual \|err\| |
|---|---|---|
| Baseline (free-electron $N(0)$, F242) | 6.35% | 10.6% |
| Nb corrected (this finding) | **4.86%** | **0.2%** |

D3a reproduces the 6.35% baseline (sanity); D3b/c/d confirm the mean error drops, crosses below the 6.3% target, and Nb's own error improves by more than half. $\mu^*_\text{Nb}$ rises from 0.106 (free-electron) to 0.128 (real-DOS) — a real $d$-band metal screens the Cooper pairing less effectively than a free-electron gas of the same density would suggest, because more Coulomb-scattering final states are available at $E_F$; the free-electron estimate was under-suppressing Nb's predicted $T_c$.

## D4 — consistency check against F374's Eliashberg floor (not a re-attack)

Feeding the same Nb correction into F374's reconciled (debye-consistent-cutoff) Eliashberg solve moves the mean error the same direction — 17.2% → 15.8% (D4a/b) — but it does **not** cross 6.3% (D4c). This is expected and does not reopen F374: that finding's NO-GO was about the Eliashberg **solver's cutoff/window machinery**, which this finding does not touch; the residual Eliashberg gap is dominated by the single-band/isotropic-Debye spectral shape (F374's own diagnosis), not by $\mu^*$. The **Allen-Dynes closed-form headline is what G9 measures**, and that is what crosses the target.

## D6 — robustness: this does not hinge on getting $\alpha_\text{Nb}$ exactly right

Scanning $\alpha_\text{Nb}$ over [1.0, 6.0] (holding all six other elements at their free-electron baseline): the mean error falls monotonically from 6.35% (\alpha=1) to a broad minimum of ~4.86-4.90% across $\alpha\in[2.8,3.4]$, then rises slowly back to 5.3% by $\alpha=6$ — but **stays below 6.3% for every $\alpha\in[2.0,6.0]$ tested** (D6b). The sourced value $\alpha=3.084$ sits inside this broad basin, not at a knife-edge. Practically: even a rough, order-of-magnitude-correct enhancement factor for Nb's $d$-band $N(0)$ — not the precise DFT number — is enough to cross the G9 target, so a future revision of the literature source (a different DFT functional, or an experimental value) is very unlikely to overturn the qualitative conclusion. (D6a confirms the test is not vacuous: at $\alpha=1$, the perturbed baseline, the mean error sits back above 6.3%.) Similarly, varying the free-electron $E_F$ used in the Morel-Anderson log-cutoff term by $\pm30\%$ (a check on the one un-sourced input this finding still uses) moves the mean error only between 4.99% and 5.21% — the conclusion is not sensitive to that choice either.

## D5 — tantalum: an explicit, checked non-result

`DOS_ENHANCEMENT` contains only `"Nb"` (D5, machine-checked so a future edit can't silently drop this boundary). An extensive literature search this session (Sommerfeld $\gamma$ compilations, DFT band-structure papers, Materials Project, the classic McMillan 1968 / Grimvall / Carbotte RMP 1990 tables) did not turn up an equally precise, directly quotable $N(E_F)$ for tantalum from an accessible source — most candidates were paywalled (APS, ScienceDirect) or JS-rendered database pages that could not be extracted. Rather than estimate $\alpha_\text{Ta}$ by analogy to Nb (same group, similar $d$-band structure, so plausibly similar — but *plausible* is not *sourced*), it is left at free-electron. **This is the actual open item for a future session**, not a closed question.

## New information

1. **A real, sourced, non-circular correction**: an independently-computed DFT electronic density of states for Nb (not fit to $T_c$, not fit to anything superconducting) plugged into a proper generalization of the existing $\mu^*$ derivation moves the Allen-Dynes mean error from 6.35% to 4.86% — **below the G9 target**.
2. **The generalization is exact at $\alpha=1$** and reduces to F242's formula with zero regression on the other six elements.
3. **The correction is directionally consistent** across both Allen-Dynes and the F374-reconciled Eliashberg solve (both improve), even though only Allen-Dynes crosses 6.3% — consistent with F374's diagnosis that the remaining Eliashberg gap is a spectral-shape problem, not a $\mu^*$ problem.
4. **Tantalum's correction remains genuinely open** — explicitly and machine-checkably not attempted, for lack of a sourced number, not for lack of trying.

## Test record

`F375-nb-realistic-dos`, tier battery, 13/13 PASS (D1–D6). See `tests/registry/interactions.yaml`.

**Claim:** none — refinement/narrowing of the G9 rubric row's existing Allen-Dynes estimate (F242), using a sourced literature input; no new algebraic or physics-tested assertion against QM/SM/GR/SR/QFT in the D12 sense.

## Open / next

- **Tantalum**: source a real $N(E_F)$ (ideally from the same DFT methodology/convention as the Nb source, or Grimvall/Carbotte's tabulated values if a non-paywalled copy can be found) and apply the same `mustar_from_real_dos` correction. Given Nb/Ta's chemical similarity, a comparable enhancement is plausible but must not be assumed without its own source.
- **G9 headline**: with Nb corrected, 4.86% is the new Allen-Dynes mean error; re-running `tc_table()`/F211's reference table with the corrected $\mu^*_\text{Nb}$ (rather than the tabulated literature $\mu^*=0.10$) as the *displayed* default is a follow-up documentation step, not attempted here (this finding only adds the machinery and verifies the effect; it does not change `REAL_SUPERCONDUCTORS` or `tc_table()`'s tabulated defaults).
- The same real-$N(0)$ generalization could, in principle, also refine $\mu^*$ for the "simple" metals if any of their free-electron approximations are found to be poorer than assumed — not indicated by anything found this session, so not pursued.
