# F218 — First-principles α²F(ω) and the dynamic strong-coupling gap ratio via Padé continuation

**Date:** 2026-07-01 - 03:20
**Status:** Confirmed — 7/7 checks PASS. Part A derives the Eliashberg spectral function α²F(ω)=λω²/ω_max² from the F213 deformation potential on a Debye acoustic band (weight normalizes to λ exactly; ω_log=ω_max/√e exact), and shows T_c is nearly **shape-insensitive** at fixed ω_log — the reason F215's single Einstein mode already reproduced the data. Part B analytically continues Δ(iω_n) to the real axis (Vidberg-Serene Padé, mpmath), giving the strong-coupling reduced gap **2Δ₀/kT_c dynamically**: it rises from 3.56 (Al) to 4.6–4.7 (Pb, Hg), correlates with measured at r=0.988, and the first-principles Debye spectrum tightens it (mean error 6.4%→5.2%) because the gap ratio — unlike T_c — is shape-sensitive.
**Modules:** `ca-simulation/ca_superconductivity.py` (added `alpha2F_debye`, `omega_max_from_omega_log`, `omega_log_of_alpha2F_debye`, `lambda_nu_debye`, `_lambda_matrix` + Debye spectrum in the solver; `_pade_continue_mp`, `gap_edge_real_axis`, `gap_ratio_dynamic`)
**Tests:** `tests/findings/test_F218_alpha2F_and_pade_gap.py` (7/7, numpy + mpmath)
**Results:** `test-results/F218_alpha2F_and_pade_gap.json`
**Cross-references:** [[F215-eliashberg-solver]] (the solver this feeds a realistic spectrum and continues to the real axis), [[F213-hopfield-firstprinciples-and-gap-renormalization]] (the deformation potential the spectrum is built from + the gap-ratio fit formula this supersedes dynamically), [[F210-electrical-superconductivity]] (the Task-1 kernel + weak-coupling 3.528 this extends), [[F211-tc-magnitude-real-superconductors]] (the (λ, ω_log, μ*) inputs).

---

## What this closes

F215 left two extensions: derive a realistic α²F(ω) (to remove the single-Einstein-mode approximation) and Padé-continue to the real axis (to get the strong-coupling gap ratio dynamically). This finding does both, and the first — combined with the shape-insensitivity of T_c — reframes the F215 residual.

## Part A — the first-principles spectral function

**The spectrum is model-derived.** Acoustic phonons $\omega_q=c_sq$ with the F213 deformation-potential vertex $|g_q|^2\propto D^2q^2/(2\rho\omega_q)$, Fermi-surface averaged over the spherical-FS phase space ($\propto q\,dq$, $q$ up to $2k_F$) with $\delta(\omega-c_sq)$, give the standard low-frequency Eliashberg function

$$\boxed{\;\alpha^2F(\omega)=\lambda\,\frac{\omega^2}{\omega_\text{max}^2}\quad(0<\omega<\omega_\text{max}),\qquad\omega_\text{max}=2c_sk_F\;}$$

with the weight fixed by $\lambda=2\int\alpha^2F/\omega\,d\omega=A\,\omega_\text{max}^2\Rightarrow A=\lambda/\omega_\text{max}^2$ (AF1, normalizes to λ). The Matsubara coupling is closed-form,

$$\lambda(\nu)=2\int_0^{\omega_\text{max}}\alpha^2F(\omega)\frac{\omega}{\omega^2+\nu^2}\,d\omega=\lambda\Big[1-\frac{\nu^2}{\omega_\text{max}^2}\ln\!\Big(1+\frac{\omega_\text{max}^2}{\nu^2}\Big)\Big]$$

(AF3, matches the numerical integral), and the log-moment gives the exact relation $\omega_\text{log}=\omega_\text{max}/\sqrt e$ (AF2), so the model reuses the elastic-sector $\omega_\text{log}$ to fix the whole spectrum with no extra input.

**T_c is shape-insensitive (AF4) — the reframing.** Feeding this distributed spectrum to the F215 solver, at fixed $\omega_\text{log}$ the Debye and Einstein T_c agree to within a few % across all seven elements (mean 27.6% vs 27.4% error). This is the well-known Eliashberg result that $T_c\approx f(\lambda,\omega_\text{log},\mu^*)$ depends on the spectrum only through its moments, not its shape — and it **explains why F215's single Einstein mode already reproduced the data**. The consequence is that the F215 residual (~27% high) is *not* a shape artifact but a μ*/ω_log **calibration** matter (our Matsubara μ* cutoff convention vs the tabulated μ*), which a Morel-Anderson μ* from the F64 retarded dielectric would settle.

## Part B — the dynamic strong-coupling gap ratio (Padé)

The reduced gap needs the **real-axis** gap edge, obtained by analytically continuing the low-T Matsubara solution $\Delta(i\omega_n)$ with the Vidberg-Serene continued-fraction Padé (high-precision mpmath, hand-rolled — no `np.linalg` on the complex recursion, per the CLAUDE.md caveat) and solving $\omega=\mathrm{Re}\,\Delta(\omega)$ for the edge $\Delta_0$. The reduced gap $2\Delta_0/kT_c$ then comes out with **no fit formula**:

| Element | measured | Padé (Einstein) | Padé (Debye) |
|---|---|---|---|
| Al | 3.40 | 3.56 | 3.55 |
| Sn | 3.50 | 3.80 | 3.76 |
| In | 3.65 | 3.90 | 3.86 |
| Ta | 3.60 | 3.78 | 3.74 |
| Nb | 3.80 | 4.12 | 4.08 |
| Pb | 4.38 | 4.71 | 4.63 |
| Hg | 4.60 | 4.77 | 4.70 |

- **PA1:** the weakest-coupling element (Al) recovers the BCS 3.53 (3.56, +1%).
- **PA2:** the strong-coupling elements rise dynamically — Pb 4.6–4.7, Hg 4.7 — reproducing the well-known departure from 3.53, correlating with measured at **r=0.988**.
- **PA3:** the first-principles Debye α²F **tightens** the ratio versus the single Einstein mode (mean error 6.4%→5.2%; Pb 4.71→4.63) — the gap ratio *is* shape-sensitive, exactly where T_c is not. This is the one place the derived spectral shape earns its keep.

The systematic ~5% overestimate mirrors the T_c calibration residual and is expected for the single-band Einstein/Debye treatment with tabulated μ*.

## New information

1. **The Eliashberg spectral function is model-native**: α²F(ω)=λω²/ω_max² from the F213 deformation potential + acoustic phase space, with ω_log=ω_max/√e exact — the pairing spectrum is derived, not assumed.
2. **T_c is shape-insensitive; the gap ratio is not.** This cleanly separates the F215 T_c residual (a μ* calibration issue, since Einstein≈Debye) from the gap ratio (genuinely shape-sensitive, and improved by the derived spectrum).
3. **The strong-coupling gap ratio is now dynamic**: 3.53→4.7 straight from the Padé-continued Eliashberg solution, superseding the F213 Marsiglio-Carbotte fit formula, r=0.988 with experiment.

## Open / next

- Morel-Anderson μ*(ω_c) from the F64 retarded dielectric, tied to the solver's Matsubara cutoff — expected to remove the ~5–27% calibration residual in both T_c and the gap ratio.
- Two-band α²F (MgB₂) and A15 compounds (Nb₃Sn) as harder spectral-shape tests.
- Real-axis Δ(ω) line shape and the tunneling density of states N(ω)=Re[ω/√(ω²−Δ(ω)²)] — the phonon structure that is the fingerprint of Eliashberg (vs BCS) superconductivity.
