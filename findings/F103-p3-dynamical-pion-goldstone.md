# F103 — P3 (matter-binding): the dynamical pion as the q-qbar pseudoscalar Goldstone

**Date:** 2026-06-06 - 06:42
**Status:** Confirmed — 13/13 checks PASS. Goldstone theorem and the polarization split reproduce to machine precision (2.3×10⁻¹⁴, 1.8×10⁻¹⁶); the calibrated spectrum reproduces the **measured** m_c, m_π, f_π, ⟨q̄q⟩ to 0.2–4.2%; GMOR holds to 0.39%; the Goldstone scaling m_π²∝m₀ is flat to 0.86%; and the real-space relative-coordinate bound state agrees with dense diagonalisation to 1.3×10⁻¹⁵.
**Roadmap:** `docs/roadmaps/roadmap-matter-binding.md` Phase **P3** (the pion / chiral pseudoscalar — force carrier for P4 nuclei). *Not* to be confused with the particle-layer roadmap's "P3" (GUI sidebar).
**Module:** `ca-simulation/ca_meson.py`
**Script:** `tests/findings/test_P3_pion.py` (~7 s, numpy only)
**Results:** `test-results/P3_pion.json`
**Test record:** record `P3-pion` (tier battery) — the script above, baseline `test-results/P3_pion.json`. `P6-si-scale` (F123) also names F103: it carries m_π/f_π into the SI closure. Declared 2026-08-19.
**Cross-references:** [[F77-njl-gap-rpa-selfconsistent]] (the calibrated NJL gap+RPA ladder this reuses), [[F74-two-constituent-bound-state-binding]] (the relative-coordinate two-body solver reused for the real-space cross-check), [[F73-spin0-bound-pair-scalar]] (the m→2m_c kinematic ceiling = the scalar partner), [[F69-paired-spinor-photon]] (the spin-1 sibling pairing channel; the pion is the spin-0 antisymmetric partner).

---

## Goal

`docs/roadmaps/roadmap-matter-binding.md` P3 asks for the pion as a **dynamical** q̄q state: the pseudoscalar Goldstone of chiral-symmetry breaking, the long-range carrier of the residual nuclear force that P4 (deuteron) will consume. F77 already reproduced m_π, f_π and ⟨q̄q⟩ self-consistently from a single coupling, so the *calibration exists*; P3 promotes the pion from "the RPA pseudoscalar pole exists" to a **certified dynamical bound state** with the Goldstone signature made sharp, the GMOR slope verified, an explicit light/heavy contrast, and a real-space relative-coordinate cross-check.

## Construction

`ca_meson.py` reuses two already-validated engines with no new free physics:

- **F77 NJL gap + RPA ladder** — one coupling G generates the constituent mass via the gap equation $M=m_0+4G N_c N_f M\,I_1(M)$ and, summed in the q̄q ladder, fixes the meson poles $1-2G\,\Pi_M(q^2)=0$. The pseudoscalar pole is the pion, the scalar pole its chiral partner σ. Prefactors are inherited verbatim from the F77 fit (Λ=651.5 MeV, GΛ²=2.10, m₀=5.5 MeV) validated against measured data.
- **F74 relative-coordinate solver** — the 3D lattice tight-binding + contact-well two-body problem in the relative coordinate, cross-checked secular-root vs dense-diagonalisation, makes the bound state a *real-space dynamical object* rather than only a continuum pole.

The pion mass enters as the pseudoscalar pole; the decay constant is $f_\pi^2=4N_c M^2K(0)$; the condensate is $\langle\bar qq\rangle_f=-2N_c M\,I_1(M)$.

## Results

**A — Goldstone theorem (exact).** In the chiral limit (m₀→0), $1-2G\,\Pi_{\rm PS}(0)=0$ is *identically* the gap equation (residual 2.3×10⁻¹⁴), so the pion is the exact massless Goldstone; the pseudoscalar pole sits at m_π=0 (1.6×10⁻⁷).

**B — Polarization split (exact).** $\Pi_S-\Pi_{\rm PS}=-8N_cN_fM^2K(q^2)$ holds to 1.8×10⁻¹⁶.

**C — Calibrated spectrum vs experiment.**

| quantity | model | measured | resid |
|---|---|---|---|
| m_c | 311.2 MeV | ~325 | 4.2% |
| m_π | 140.5 MeV | 135–138 | 4.1% |
| f_π | 92.6 MeV | 92.4 | 0.2% |
| ⟨q̄q⟩^{1/3} | −249.1 MeV | ~−250 | 0.4% |
| m_σ | 622.4 MeV | ≈2m_c (broad) | — |
| m_ρ | 785.6 MeV | 775 (KSRF) | 1.4% |

**D — GMOR.** $m_\pi^2 f_\pi^2=-m_0\langle\bar qq\rangle_{\rm tot}$ holds to 0.39% at the physical point — confirming the F77 numbers as the roadmap asked.

**E — Goldstone scaling (the sharp check).** Scanning m₀ from 2→8 MeV, the slope $m_\pi^2/m_0$ stays constant to 0.86% (3.61→3.58), i.e. $m_\pi^2$ is **linear in m₀** as m₀→0 — the defining Goldstone signature. If the pseudoscalar were not the Goldstone, this slope would not be flat.

**F — Light/heavy contrast (one coupling, no extra input).** The same single G that breaks chiral symmetry puts the scalar chiral partner σ at the 2m_c threshold (m_σ/2m_c = 1.0000), so the pion is anomalously light against both its chiral partner ($m_\pi/m_\sigma=0.226$) and the vector ($m_\pi/m_\rho=0.179$). The ρ uses the KSRF relation $m_\rho^2=2g_{\rho\pi\pi}^2 f_\pi^2$ tying it to the **model output** f_π; the only external number is the empirical $g_{\rho\pi\pi}\simeq6$ (flagged Tier-3, used only for the contrast).

**G — Real-space bound state (machine).** The F74-engine relative-coordinate q̄q bound state from the secular Koster-Slater root agrees with dense diagonalisation to 1.3×10⁻¹⁵ (L=12, g=8t above the Watson threshold g_c=3.957t) — certifying the bound state as a real-space dynamical object.

## Verdict

The pion is delivered as a dynamical q̄q pseudoscalar Goldstone: massless in the chiral limit (exact), light and GMOR-linear at the physical point (0.4–4%), anomalously light against its σ partner and the ρ, and realisable as a machine-precision real-space bound state. No new free physics beyond the F77 calibration; P3 adds the Goldstone-scaling and relative-coordinate certifications plus the explicit light/heavy contrast.

- **Predicted by the model:** the pion as the exact chiral-limit Goldstone; the GMOR slope; the σ chiral partner pinned at 2m_c from the same single coupling; the whole light-meson sector as cross-check.
- **External (flagged):** the ρ via KSRF carries one empirical coupling $g_{\rho\pi\pi}$ — illustrative contrast only, not a precision claim.

## Scope / next (feeds P4)

The pion mass and the pion-nucleon coupling are exactly the inputs P4 (deuteron) consumes: the long-range nuclear force is one-pion exchange, an OPEP Yukawa tail $\propto e^{-m_\pi r}/r$ with strength set by Goldberger-Treiman ($g_{\pi qq}f_\pi=M$, F77 1.1%) lifted to the nucleon via $g_A$. The σ width above threshold (Im K for q²>4M²) is a small extension and is not needed for P4.

## Files
- Module: `ca-simulation/ca_meson.py`
- Script: `tests/findings/test_P3_pion.py`
- Results: `test-results/P3_pion.json`
