# F90 — E2E certification of the non-Abelian W/Z/gluon couplings on the σ-bilinear + the full fermion/radiation back-reaction loop; chiral-Proca birefringence is mass-suppressed

**Date:** 2026-06-04 - 01:59
**Status:** Confirmed — 14/14 PASS (new suite) + the repaired Phase-7 suite 5/5 PASS. Primarily an **integration / certification** finding (the F85-style kind): it certifies that the sector design decision #5 retains on the σ-bilinear — W, Z, gluon — works *end-to-end* (fermion current → source kick → causal propagation → back-action on the fermion), with the energy bookkeeping closed. One small new algebraic result: the chiral-Proca birefringence closed form and its mass suppression.
**Module:** none new (one test-local candidate primitive, `chiral_massive_step`). **Tests:** `tests/findings/test_E2E_nonabelian_bilinear.py` (~0.4 s); `tests/findings/test_wmu_phase7_backreaction.py` (WB.5 repaired).
**Results:** `test-results/E2E_nonabelian_bilinear.json`, `test-results/phase7_backreaction_results.json`.
**Cross-references:** F36 (Phase-7 back-reaction), F43/FG-7 (gluons), FG-4 (Z), FG-8 (β-decay pipeline), F30/F37 (birefringence / chiral aliasing), [[F68-minimal-coupling-forces-even-photon]], [[F69-paired-spinor-photon]], [[F89-singlet-bilinear-is-paired-photon]].
**Test record:** record `E2E-nonabelian-bilinear` (tier battery), record `wmu-phase7-backreaction` (tier battery) — `tests/registry/`, D9.

---

## 1. What was certified (new suite, 14/14)

| Part | Statement | Residual | Tier |
|------|-----------|----------|------|
| W1 | Sourced − free == g·J·dt with J from a real doublet (kick exactness) | $4.4\times10^{-16}$ | exact |
| W2 | Work–energy ledger: $\Delta U_\text{field}$ per tick $= g\,dt\sum J\!\cdot\!E_\text{rot} + \tfrac12 g^2dt^2\sum|J|^2$, J(t) from an evolving Weyl doublet, 30 ticks | $4.0\times10^{-17}$ | machine |
| W3 | Causal W front: pulse at A, signal at B (d=8) zero on emission ($0.0$), arrives after the light time $d\sqrt3=13.9$ ticks ($3.3\times10^{-2}$) | — | quant |
| W4 | Proca consistency: even-massive$(m{=}0)$ == even-law step; chiral-massive$(m{=}0)$ == chiral step; $\Delta\omega_\text{eff}$ closed form (§2) | $2.8\times10^{-13}$ | machine |
| W5 | Non-Abelian self-coupling: identity links a fixed point; unitarity preserved on Haar-random links | $8.9\times10^{-16}$ | exact/machine |
| Z1 | Massive-Z neutral-current kick exact + per-species == decomposed current + causal massive front ($m_Z=m_W/\cos\theta_W$) | $2.2\times10^{-16}$ | exact |
| Z2 | Source-basis identity $gW^3J^3+g'B(J^\text{em}{-}J^3)=eAJ^\text{em}+g_ZZJ_Z$ at $g'=g\tan\theta_W$ | $1.8\times10^{-15}$ | machine |
| G1 | Colour kick from the real `ca_strong` Noether current exact + colour-diagonal ($a{=}3$ drives only $a{=}3$) | $2.2\times10^{-16}$ | exact |
| G2 | Global SU(3) covariance: $J(Vq)=R_\text{adj}(V)J(q)$ AND the full sourced step commutes with the adjoint rotation | $3.1\times10^{-15}$ | machine |
| G3 | Causal gluon front on BCC (emit $0.0$; arrival $2.0\times10^{-2}$ after $d\sqrt3$) | — | quant |
| G4 | $m_g=0$ massive gluon step == free step | $0.0$ | exact |
| G5 | SU(3) $f^{abc}$ Jacobi identity | $1.1\times10^{-16}$ | exact |
| B1 | **Closed fermion↔W loop** (20 ticks): J sources the field; the field, exponentiated into SU(2) links $U=\exp(i\varepsilon A^a\tau^a/2)$ with $A\mathrel{+}=E_W dt$, acts back via the covariant step. Norm $6.4\times10^{-15}$; ledger $6.9\times10^{-18}$; $g{=}0$ control bit-for-bit ($0.0$); back-action nonzero ($3.3\times10^{-3}$) | $6.4\times10^{-15}$ | machine |
| B2 | Radiation: field energy $0\to3.9\times10^{-2}$ under the fermion current; zero-current control stays exactly $0$ | $0.0$ | exact |

The back-reaction loop is closed **in both directions** for the first time as a single co-evolution: F36 verified fermion→field only; B1 adds field→fermion in the same tick loop with all three conservation statements (fermion norm, field work–energy, exact $g{=}0$ reduction) holding simultaneously.

## 2. The one new algebraic result — chiral-Proca birefringence is mass-suppressed

The chirally-faithful massive step (each Riemann–Silberstein branch on its own massive dispersion $\omega^\pm_\text{eff}=\sqrt{m^2+(\Omega^\pm)^2}$; real fields preserved because $\Omega^+(-k)=\Omega^-(k)$) has the exact birefringence

$$
\Delta\omega_\text{eff} \;=\; \omega^+_\text{eff}-\omega^-_\text{eff}
\;=\; \frac{(\Omega^+)^2-(\Omega^-)^2}{\omega^+_\text{eff}+\omega^-_\text{eff}}
\;=\; \Delta\Omega\cdot\frac{\Omega^++\Omega^-}{\omega^+_\text{eff}+\omega^-_\text{eff}}.
$$

verified to $10^{-15}$ relative and monotonically decreasing in $m$ (measured $1.03\times10^{-2}\to1.18\times10^{-3}$ as $m:0\to2$ at $k=0.4$ body-diagonal). Since $\tfrac{\Omega^++\Omega^-}{\omega^++\omega^-}\to\Omega_\text{even}/m$ for $m\gg\Omega$, a heavy boson's birefringence is suppressed by $\sim\Omega_\text{even}/m$. **Physical reading:** this strengthens design decision #5 — the birefringent σ-channel is safe for W/Z not only because polarimetry bounds don't apply to massive bosons, but because the mass itself dilutes the chiral splitting.

## 3. Repair: WB.5 (test_wmu_phase7_backreaction) was stale, not a model failure

The 2026-06-02 full rerun reported WB.5 FAIL (4/5). Root cause: F37 (2026-05-24) re-aliased `w_propagation_step_spectral` to the *chiral* step, while `w_massive_propagation_step_spectral` is built on the *even* law — so WB.5 was comparing two different propagators; the gap (1.3) is exactly the vacuum birefringence, not an error. The test now compares against the even-law reference (PASS, machine) and reports the chiral gap informationally. The chiral massless limit is covered by W4(b) of the new suite.

## 4. Scope / honest limits

- The source coupling remains the **linearised** (diagonal-in-$a$) Yang–Mills kick of F36/F43; the $O(g^2)$ commutator term lives in `w_self_interaction_step` (structure verified, W5) but is not co-evolved with the source in one integrator.
- The B1 field→fermion map ($A\mathrel{+}=E\,dt$, site-centred links) is a physically-motivated O(a) construction (same status as `covariant_weyl_step_3d_bcc`, see its docstring), not an exact lattice gauge-dynamics derivation.
- Fermion *energy loss* (true radiation damping) is not measured — what is closed is the exact work–energy ledger on the field side plus unitary norm conservation on the fermion side.
- `chiral_massive_step` is test-local; promoting it to `ca_wmu` (and deciding whether the canonical massive W/Z propagator should be even or chiral) is a standing model decision flagged for review — F89's open question "why non-Abelian sectors must take the chiral pairing" is the relevant context.
