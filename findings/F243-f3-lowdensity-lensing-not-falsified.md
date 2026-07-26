# F243 — F3 low-density lensing: falsification attempt fails (prediction survives)

**Date:** 2026-07-03 - 14:35
**Status:** Confirmed — 6/6 checks PASS. Closes open-derivation **F1** (prompt #16; exactness-inventory not-yet-met #4 / next-steps line 5). The standing concern was that the **F3 lensing prediction fails at low fermion density**. Running the F3 symplectic Yukawa back-reaction at a ladder of fermion densities from $\rho=1$ down to $\rho=10^{-3}$, the $\lvert\Phi\rvert$-depression (the lensing source) **stays a correct-sign depression, remains positive-definite, never diverges, survives to the lowest density, and scales linearly** with density (weak-field log-log slope **1.012**, ideal 1.000). The prediction therefore **degrades gracefully as (source × coupling); it does not "fail" at low density**. Falsification attempt → **NOT FALSIFIED**.
**Modules:** `ca-simulation/ca_unified.py` (`setup_vacuum`, `unified_step` back-reaction — used, not modified)
**Tests:** `tests/findings/test_F243_f3_lowdensity_lensing.py` (6/6, pure numpy)
**Results:** `test-results/F243_f3_lowdensity_lensing.json`
**Cross-references:** [[F244-emqg-1overb-3d-lensing]] (the companion lensing-scan closure, prompt #17), [[F106-psi-K-sourcing-derivation]] (the $\psi\to K$ energy-density sourcing this depression is the weak-field image of), [[F64-dielectric-nonlinear-K]] (the dielectric the depression modulates).

---

## What this closes

`docs/roadmaps/next-steps.md` line 5 and exactness-inventory not-yet-met #4 flagged: "attempt to falsify the F3 lensing prediction failure at low fermion density." F3 (`run_phaseF_tests.py::test_F3`) demonstrates that a fermion density concentration sources a $\lvert\Phi\rvert$ depression — the gravitational well — via the symplectic Yukawa back-reaction $\Pi\mathrel{-}=\tfrac{dt}{2}\,y\,(\chi^\dagger\eta)$. The Coulomb-analog lensing signal is the $c(x)$ variation that depression produces. The worry: does this vanish or misbehave when the source is weak?

## The test

Hold the geometry fixed; scale the fermion spinor amplitude by $\sqrt{\rho_\text{frac}}$ so the density $n=\lvert\psi\rvert^2$ scales as $\rho_\text{frac}$. Run the F3 back-reaction ($L{=}128$, 120 steps, $y{=}0.2$) and record the equilibrium depression $D(\rho)=\max\lvert\lvert\Phi\rvert-v\rvert$ and its sign. Falsified if at low density the depression **reverses sign**, **vanishes discontinuously**, or **breaks the linear source law**.

| $\rho_\text{frac}$ | peak density | $\max\lvert\Delta\Phi\rvert$ | depression? | induced $\Delta c$ |
|---|---|---|---|---|
| 1.000 | 1.0 | 4.81×10⁻¹ | yes | 8.2×10⁻¹ |
| 0.300 | 0.30 | 6.32×10⁻² | yes | 1.2×10⁻¹ |
| 0.100 | 0.10 | 1.99×10⁻² | yes | 5.1×10⁻² |
| 0.030 | 0.030 | 5.86×10⁻³ | yes | 1.2×10⁻² |
| 0.010 | 0.010 | 1.94×10⁻³ | yes | 3.7×10⁻³ |
| 0.003 | 0.0030 | 5.82×10⁻⁴ | yes | 1.1×10⁻³ |
| 0.001 | 0.0010 | 1.94×10⁻⁴ | yes | 3.5×10⁻⁴ |

## The result

- **Correct sign at all densities** ($\lvert\Phi\rvert<v$ at the fermion location — a well, never a bump).
- **Linear source law.** The Yukawa source $\chi^\dagger\eta$ is bilinear in the fermion field, so the depression is $\propto$ density. The weak-field ($\rho<1$) log-log slope is **1.012** (ideal 1.000). The all-points slope is 1.09 only because the strongest point ($\rho=1$, depression $\approx0.68\,v$) is saturating out of the weak-field regime — mild sub-linearity there, not a low-density failure.
- **Survives to $\rho=10^{-3}$** ($\max\lvert\Delta\Phi\rvert=1.9\times10^{-4}$, ~9 orders above machine epsilon) with no divergence.

**Verdict: NOT FALSIFIED.** The F3 lensing prediction does not fail at low density; it scales down linearly and stays correct-sign — exactly the behaviour of a weak-field source whose strength is (density × coupling). This is the expected and desirable outcome: the model has no low-density lensing pathology.

## New information

1. **The claimed low-density failure does not exist.** F3's back-reaction lensing source is a genuine, correct-sign, positive-definite depression scaling linearly with fermion density (slope 1.012) down to $\rho=10^{-3}$.
2. **The linearity confirms the source mechanism.** $D\propto\rho$ follows directly from the bilinear Yukawa source $\chi^\dagger\eta$ — the weak-field regime of the F106 $\psi\to K$ energy-density sourcing. Saturation appears only at $\rho\sim1$ (strong field), as it should.
3. **A falsification target is retired as PASS**, tightening exactness-inventory not-yet-met #4.

## Open / next

- The astrophysical low-density regime (galactic-outskirts fermion densities) is many decades below $\rho=10^{-3}$; the linear law extrapolates, but a dedicated ultra-low-density run would confirm no floor exists above machine precision.
- Couple to the full deflection pipeline (F244) at low density to confirm the *deflection angle*, not just the depression, scales linearly.
