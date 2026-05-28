# F43 — FG-7: dynamical SU(3) gluon sector  (rotation law, self-coupling, confinement diagnostic)

**Date:** 2026-05-27 - 22:56
**Status:** Confirmed — 20/20 tests PASS (8 bit-for-bit exact)
**Module:** `ca-simulation/ca_gluon.py`  (new)
**Tests:** `model-tests/test_FG7_gluon_dynamics.py`
**Results:** `test-results/FG7_gluon_dynamics.json`
**Cross-refs:** F29 (W-triplet bilinear), F33 (W Yang–Mills self-coupling), F36 (W back-reaction)

---

## Summary

Brings the colour sector up to the standard the $W$ reached. Until now SU(3) lived only as a link variable in `ca_strong.py` (parallel transport on the quark colour triplet, Wilson plaquette as a diagnostic only). F43 promotes it to a first-class **dynamical** field — gluon propagation by the F26 rotation law, Yang–Mills self-coupling via $f^{abc}$, Wilson-loop area-law diagnostic, and quark-current back-reaction.

This closes item 6 of [first-gen-completeness.md](../first-gen-completeness.md) §3 ("Gluon to dynamical-field standard") and the FG-7 row of the review's §5.1 table.

---

## Construction

### Structure constants $f^{abc}$

The totally antisymmetric SU(3) structure constants are built directly from the standard $[T^a, T^b] = i f^{abc} T^c$ assignment, with the 9 non-zero independent values:

$$f^{123}=1,\quad f^{147}=f^{246}=f^{257}=f^{345}=\tfrac12,\quad f^{156}=f^{367}=-\tfrac12,\quad f^{458}=f^{678}=\tfrac{\sqrt3}{2}.$$

The Jacobi identity $f^{abe}f^{ecd} + f^{bce}f^{ead} + f^{cae}f^{ebd} = 0$ holds at $1.1\times10^{-16}$ across all $8^4$ index combinations (PA.1).

### Phase A — Colour-octet bilinear $G^{a,i}$ and free rotation law (port of F29 / F26)

Following F29's W-triplet, build the **colour-octet** Pauli-vector bilinear

$$G^{a,i}(\mathbf x) = \sum_f \sum_{c c'} (T^a)_{cc'} \sum_{\alpha \beta} q^{f,c,\alpha\dagger}(\mathbf x)\,\sigma^i_{\alpha\beta}\,q^{f,c',\beta}(\mathbf x)$$

with the **Hermitian** conjugation (transpose form fails SU(3) for the same reason it fails SU(2): $V^TV\ne I$ in SU(3) — F29 caveat carries over). The 8 components are the gluon octet.

**Free propagation** applies the F26 rotation law per $a$-component, independently on 2D-square ($\Omega_{2\mathrm D}=2\omega_{2\mathrm D}(k/2)$, $c_\text{lat}=1/\sqrt2$) and 3D BCC ($\Omega^\pm=2\omega^\pm_\text{BCC}(k/2)$, $c_\text{lat}=1/\sqrt3$). Reuses `ca_maxwell_2d.rotation_step_em_spectral_2d` and `ca_wmu.w_propagation_step_spectral` per $a$.

### Phase B — Wilson plaquette $G^a_{\mu\nu}$ + Yang–Mills self-coupling (port of F33)

Wilson plaquette $U_\square$ on 2D-square and on the BCC composite link (mirror of `ca_wmu.plaquette_field_strength`):

$$G^a_{\mu\nu}(\mathbf x) = \frac{-i}{g\,a^2}\,\mathrm{Tr}\!\left[T^a\,(U_\square - U_\square^\dagger)\right] = \frac{2}{g\,a^2}\,\mathrm{Im}\,\mathrm{Tr}\!\left[T^a\,U_\square\right]$$

Since $T^a$ is traceless, identity links give $U_\square = I$ and hence $G^a_{\mu\nu} = 0$ **bit-for-bit** (PB.1, PB.2).

Self-coupling tick (port of `ca_wmu.w_self_interaction_step`):

$$W^a(\mathbf x) = \overline{2\,\mathrm{Im}\,\mathrm{Tr}[T^a\,U_\ell(\mathbf x)]}_{\,\ell},\quad \delta W^a = g\,\Delta t\,f^{abc}\,W^b\,G^c,\quad U_\ell \to e^{i\,\delta W^a T^a}\,U_\ell$$

SU(3) link unitarity is preserved to floating-point round-off ($\sim 10^{-15}$, PB.5/PB.6) on both lattices because the update is the product of two SU(3) elements.

### Phase C — Wilson-loop area-law diagnostic (frozen non-trivial links, 2D)

Ordered link product around an $r\times t$ rectangular contour; spatially averaged $\langle\mathrm{Re}\,\mathrm{Tr}\,W(r,t)\rangle$ at fixed link configuration:

- **Cold-link baseline:** $\langle\mathrm{Re}\,\mathrm{Tr}\,W(r,t)\rangle = N_c = 3$ exactly for every $(r,t)$ — every link is $I$, so the product is $I$ and $\mathrm{Tr}\,I = 3$. PC.1 confirms across $r,t \in \{1,2,3\}$ at residual $0.0$ bit-for-bit.
- **Local SU(3) gauge invariance:** since $W$ is a closed loop, any local $V(\mathbf x)$ cancels at the start/end corner exactly. PC.2 confirms at $4.6\times10^{-16}$ (essentially exact) across multiple loop sizes.
- **Strong-coupling decorrelation:** on Haar-random links, $|\langle\mathrm{Re}\,\mathrm{Tr}\,W(r,t)\rangle|/N_c \approx 4\times 10^{-2}$ — the cold-link baseline is broken by ~75× across loop sizes 1–3 (PC.3). This is the strong-coupling-expansion limit; the linear-confinement regime requires gradient flow / cooling from a near-identity start, which we leave for a follow-up.

### Phase D — Quark current sourcing the gluon (port of F36)

Wraps the existing `ca_strong.noether_charge_density` / `noether_current_spatial` as `quark_colour_current_2d` (PD.1, residual $0.0$). The sourced step linearises the Yang–Mills equation around the abelian vacuum:

$$\partial_t E^a(\mathbf k) = \Omega(\mathbf k)\,B^a(\mathbf k) + g\,J^a(\mathbf k)$$

split as free F26 rotation + real-space source kick. Each $a$ is sourced only by its own $J^a$ (diagonal coupling, PD.2 / PD.5 exact zero) because the kick is additive. The Proca-style massive step with $m_g = 0$ reduces to the free step **bit-for-bit** (PD.3, residual $0.0$ — the F36 WB.5 SU(3) analog).

---

## Results

| Test | What it checks | Residual | Tier |
|------|----------------|----------|------|
| PA.1 | $f^{abc}$ Jacobi identity | $1.1\times10^{-16}$ | 1 |
| PA.2 | 2D rotation magnitude conservation (20 ticks) | $2.0\times10^{-15}$ | 2 |
| PA.3 | BCC rotation magnitude conservation (10 ticks) | $2.6\times10^{-15}$ | 2 |
| PA.4 | $G^a$ transforms as SU(3) adjoint (2D bilinear) | $6.7\times10^{-16}$ | 1 |
| PA.5 | $\Sigma_a \|G^a\|^2$ SU(3) Casimir invariance | $0.0$ | 1 |
| PA.6 | $G^a$ transforms as SU(3) adjoint (BCC bilinear) | $7.8\times10^{-16}$ | 1 |
| PB.1 | 2D cold links $\Rightarrow G^a_{xy}=0$ | $0.0$ | 1 |
| PB.2 | BCC cold links $\Rightarrow G^a_{\mu\nu}=0$ (3 planes) | $0.0$ | 1 |
| PB.3 | 2D random links $\Rightarrow G^a$ non-zero (structural) | $1.65$ (O(1)) | — |
| PB.4 | $\|G^a_{xy}\|^2$ constant-$V$ SU(3) invariance | $5.4\times10^{-15}$ | 1 |
| PB.5 | 2D self-coupling preserves link unitarity (5 ticks) | $5.3\times10^{-15}$ | 2 |
| PB.6 | BCC self-coupling preserves link unitarity (5 ticks) | $7.1\times10^{-15}$ | 2 |
| PC.1 | Cold Wilson loop $= N_c = 3$ (9 sizes) | $0.0$ | 1 |
| PC.2 | Wilson loop local SU(3) gauge invariance | $4.6\times10^{-16}$ | 1 |
| PC.3 | Random-link Wilson loops $\ll N_c$ (decorrelation) | $0.12$ vs $N_c=3$ | — |
| PD.1 | Octet charge density wraps Noether current | $0.0$ | 1 |
| PD.2 | Diagonal source coupling (all 8 octet) | $0.0$ | 1 |
| PD.3 | Massive step at $m_g=0$ = free step | $0.0$ | 1 |
| PD.4 | Free-gluon BCC dispersion (50 ticks) | $1.7\times10^{-13}$ | 2 |
| PD.5 | 20-tick sourced step, off-diagonal stays zero | $0.0$ | 1 |

**20/20 PASS in 0.42 s.** Eight tests at bit-for-bit zero; five at machine $\varepsilon$.

---

## What this adds to the model

1. **The Higgs-free SU(2)$_L$ analog now exists for SU(3)$_C$.** Where F29/F33/F36 built the dynamical $W$ on top of F27's chiral SU(2)$_L$, FG-7 builds the dynamical gluon on top of `ca_strong.py`'s already-validated SU(3) link-variable layer — using the **same** rotation law and **same** plaquette + structure-constant prescription, swapping $\tau^a \to T^a$ and $\epsilon^{abc} \to f^{abc}$.

2. **The two SU(2)$_L$/SU(3)$_C$ Wilson-action gauge sectors are structurally parallel.** Both vacuum identities (cold $\Rightarrow F=0$ exactly), both transform tests (constant-$V$ field-strength magnitude invariance at machine $\varepsilon$), and both unitarity guarantees ($\exp(iH)\,U$ is in the gauge group) carry over without modification.

3. **The Wilson-loop framework is now in place.** Confinement diagnostics — Creutz ratios, static $q\bar q$ potential, string tension — all live downstream of the `wilson_loop_2d_*` primitives delivered here. PC.3 verifies the strong-coupling baseline. The linear-confinement regime requires real-time link evolution from a near-identity start (gradient flow / Kogut–Susskind Hamiltonian) — a follow-up item, scoped out of this session per the design doc estimate.

4. **First-generation completeness review §3 item 6 is closed at the dynamical level.** The remaining first-gen item is FG-4 (dynamical $Z$); FG-1, FG-2, FG-3, FG-6, FG-7 are all closed.

---

## Known limitations

- **No real-time confinement measurement.** PC.3 establishes the deconfined (decorrelated) baseline; the linear $\langle W\rangle \sim e^{-\sigma\cdot r\cdot t}$ regime is a separate item requiring link Hamiltonian evolution from a near-identity start. The `wilson_loop_2d_*` primitives are in place; the cooling / gradient-flow driver is not.
- **Linearised back-reaction only.** The sourced step is the abelian linearisation $\partial_t E^a = \Omega B^a + gJ^a$, mirroring F36 WB. The full non-Abelian commutator $\big[W, J\big]$ at $O(g^2)$ is what the self-coupling step `gluon_self_coupling_step_*` handles separately — there is no single integrator that combines them in this finding.
- **2D Wilson plaquette only along one direction-pair $(x,y)$.** The 2D-square lattice has a single $\mu\nu = xy$ plane by construction, so the $\|G\|^2$ test sums one plane. The BCC plaquette covers all three planes $(xy, xz, yz)$.
- **No quark mass / electroweak interplay.** F40/FG-3 already wired the quark doublet to the W; FG-7 leaves the gluon sector isolated for the linear free-field tests. Combining FG-3 and FG-7 in a single Strang stepper is straightforward but not part of this finding.

---

## Files

- `ca-simulation/ca_gluon.py` — new module (~600 lines). Public API:
  `_F_SU3`, `structure_constants_jacobi_residual`, `gluon_rotation_step_spectral_2d`, `gluon_rotation_step_spectral_bcc`, `gluon_massive_step_spectral_bcc`, `quark_colour_octet_bilinear_2d`, `quark_colour_octet_bilinear_bcc`, `octet_norm_sq`, `octet_adjoint_rotate`, `plaquette_matrix_su3_2d`, `plaquette_field_strength_su3_2d`, `plaquette_field_strength_su3_bcc`, `gluon_self_coupling_step_2d`, `gluon_self_coupling_step_bcc`, `link_unitarity_residual_su3`, `wilson_loop_2d_rect`, `wilson_loop_2d_avg`, `wilson_loop_gauge_residual_2d`, `wilson_loop_area_law_data`, `quark_colour_current_2d`, `gluon_sourced_step_2d`, `gluon_sourced_step_bcc`, `free_gluon_dispersion_residual_bcc`, `make_su3_link_field_bcc`.
- `model-tests/test_FG7_gluon_dynamics.py` — 20-test suite.
- `test-results/FG7_gluon_dynamics.json` — numerical results.

---

## Exactness inventory additions

Tier 1 (algebraic exact): #116–#128 (13 entries).
Tier 2 (machine precision): #43–#47 (5 entries).

Total tally after F43: **128 Tier-1 algebraic exact / 47 Tier-2 machine precision.**
