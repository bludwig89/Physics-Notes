# F48 — FG-4: Dynamical Z neutral-current sector

**Date:** 2026-05-28 - 23:30
**Status:** Confirmed — 12/12 tests PASS (6 bit-for-bit zero, 6 at machine ε)
**Module:** `ca-simulation/ca_z_field.py` (new, additive — no existing surface modified)
**Verification script:** `model-tests/test_FG4_dynamical_Z.py`
**Results:** `test-results/FG4_dynamical_Z.json`
**Closes:** first-gen-completeness §3 item 5 and §5.1 row FG-4

---

## 1. Result

The algebraic Weinberg mixing of F35 is promoted to a *propagating* Z field with a dynamical fermion neutral-current source. The new module `ca_z_field.py` adds (i) free massless and massive (Proca) Z propagation under the F26 even-dispersion rotation law, (ii) the SM per-species neutral-current couplings $(g_L^f, g_R^f) = (T_3^f - Q^f s^2_W,\; -Q^f s^2_W)$ for all seven first-generation chiralities, (iii) the neutral-current builder $J^Z_0(x) = J^3_0(x) - \sin^2\theta_W\,J^{\rm em}_0(x)$ with a per-species cross-check, and (iv) the sourced step $\partial_t E_Z = \omega_{\rm eff} B_Z + g_Z J_Z$ with $g_Z = g/\cos\theta_W$. All twelve tests pass; the source-basis identity that ties the (W^3, B) gauge basis to the (A, Z) mass basis closes at FFT floor with no fit parameters.

The headline non-trivial prediction is **Z11**: at the F45 bare lattice Weinberg angle $\sin^2\theta_W = 1/4$, the electron's Z vector coupling vanishes,

$$\boxed{\;g_V^{e_L} \;=\; T_3^{e_L} \;-\; 2 Q^{e_L} \sin^2\theta_W \;=\; -\tfrac{1}{2} \;-\; 2(-1)(\tfrac{1}{4}) \;=\; 0\;}$$

bit-for-bit. The counter-check at the PDG on-shell angle 0.4916 rad ($\sin^2\theta_W \approx 0.231$) gives $g_V^{e_L} \approx -0.038$ — visibly non-zero, so the vanishing at F45 is a structural feature of the σ ↔ τ swap geometry (F45), not a generic property of the formula.

---

## 2. What this changes

Before this finding the Z was a label on a mass eigenstate. F35 verified the *rotation* that produces it ($O(2)$ in $(B, W^3)$ with $\theta_W$ an input) and the mass *ratio* $m_Z = m_W/\cos\theta_W$, but no Z field was ever evolved as a degree of freedom and no fermion ever sourced one. The W4.5 lepton-current residual was the only place a Z-like coupling was exercised, and only in passing.

F48 closes that gap. The (E_Z, B_Z) pair is now a real propagating field on the BCC lattice, with:

- **Free dispersion** = F26 even rotation (test Z4, $1.0\times 10^{-13}$ rel after 40 ticks)
- **Proca dispersion** $\omega^2 = m_Z^2 + \Omega_{\rm even}^2(\mathbf k)$ (test Z5, $1.5\times 10^{-13}$ rel after 30 ticks across four masses)
- **Mass-eigenstate consistency**: extract Z via `weinberg_mix(W^3, B)` then propagate massless = propagate W^3, B in gauge basis then mix (test Z6, $7.0\times 10^{-15}$ over 25 ticks at $\theta_W = \pi/6$)
- **Source kick**: $E_Z(t+1) = E_Z^{\rm free}(t+1) + g_Z J_Z \Delta t$ (test Z7, $8.9\times 10^{-16}$ — round-off cancellation of `(A+B)-A`, not algorithmic)
- **Source-basis identity**: the SM Lagrangian identity $g W^3 J^3 + g'(B)(J^{\rm em}-J^3) = e A J^{\rm em} + g_Z Z (J^3 - s^2_W J^{\rm em})$ holds per site to FFT floor (test Z2, $2.7\times 10^{-15}$)

The new fermion sector hook is intentionally species-keyed: site densities are passed in as a `dict` species → $\rho^f(x)$, and the per-species couplings are looked up from the standard SM table — so anomaly cancellation (F38), per-species charge bookkeeping (F35 W6.4), and the σ ↔ τ swap value (F45) all enter through the same registry.

---

## 3. The module

`ca-simulation/ca_z_field.py` exports:

| Function | Purpose |
|---|---|
| `SPECIES`, `T3_TABLE`, `Q_TABLE`, `THETA_W_F45` | first-generation registry |
| `z_couplings(theta_W)` | per-species $(g_L, g_R, g_V, g_A, T_3, Q)$ |
| `z_coupling_strength(g, theta_W)` | $g_Z = g/\cos\theta_W$ |
| `photon_coupling_strength(g, theta_W)` | $e = g\sin\theta_W$ |
| `z_mass_from_w(m_W, theta_W)` | $m_Z = m_W/\cos\theta_W$ (F35 W6.3 helper) |
| `fermion_em_current(densities)` | $J^{\rm em}_0(x) = \sum_f Q^f \rho^f(x)$ |
| `fermion_T3_current(densities)` | $J^3_0(x) = \sum_f T_3^f \rho^f(x)$ |
| `fermion_neutral_current(densities, theta_W)` | $J^Z_0 = J^3 - s^2_W J^{\rm em}$ |
| `fermion_neutral_current_per_species(...)` | $\sum_f (g_L^f \rho_L^f + g_R^f \rho_R^f)$ (cross-check) |
| `make_z_field(L, mode)` | initialise $(E_Z, B_Z)$ |
| `z_propagation_step_spectral` | free massless rotation (F26 even) |
| `z_massive_propagation_step_spectral` | Proca step |
| `z_sourced_propagation_step` | Strang-split free + source kick |
| `z_from_w3_b`, `photon_from_w3_b` | bridge to gauge basis via F35 |
| `source_basis_identity_residual` | the Z2 diagnostic |

Default Weinberg angle throughout is the **F45 bare lattice value** $\theta_W = \pi/6$ (so $\sin^2\theta_W = 1/4$, $\cos^2\theta_W = 3/4$). Pass `theta_W=…` explicitly for the W6.3 input value 0.4916 rad or any other choice. The default is *not* the SM phenomenological one because (a) F45 supplies the value from first principles on the BCC lattice and (b) the model has no RG running yet, so the lattice prediction is the honest default.

---

## 4. Test results

| # | Test | Residual | Target | Status |
|---|---|---|---|---|
| Z1 | Per-species $(g_L, g_R)$ — 3 angles × 7 species | $0.0$ | $10^{-15}$ | **PASS** (bit-for-bit) |
| Z2 | Source-basis identity, both forms of $J^Z$ | $2.7\times 10^{-15}$ | $10^{-14}$ | **PASS** |
| Z3 | $m_Z = m_W/\cos\theta_W$ — 5 angles × 3 masses | $0.0$ | $0.0$ | **PASS** (bit-for-bit) |
| Z4 | Free Z dispersion = $\Omega_{\rm even}(\mathbf k)$ — 40 ticks | $1.0\times 10^{-13}$ | $10^{-12}$ | **PASS** |
| Z5 | Proca dispersion at $m_Z \in \{0, 0.1, 0.3, 0.5\}$ — 30 ticks | $1.5\times 10^{-13}$ | $10^{-12}$ | **PASS** |
| Z6 | $[\text{mix}, z\text{-propagate}] = 0$ at $\theta_W = \pi/6$, 25 ticks | $7.0\times 10^{-15}$ | $10^{-12}$ | **PASS** |
| Z7 | Source kick: $E_Z^{\rm src} - E_Z^{\rm free} = g_Z J_Z \Delta t$ | $8.9\times 10^{-16}$ | $10^{-14}$ | **PASS** |
| Z8 | $\nu_L$ Z couplings $\theta_W$-independent — 20 angles | $0.0$ | $0.0$ | **PASS** (bit-for-bit) |
| Z9 | Photon-neutrino coupling $\equiv 0$ | $0.0$ | $0.0$ | **PASS** (bit-for-bit) |
| Z10 | $(g_V, g_A) = (T_3 - 2Q s^2_W,\;T_3)$ — 4 angles × 7 species | $2.8\times 10^{-17}$ | $10^{-15}$ | **PASS** |
| Z11 | F45: $g_V^{e_L} = 0$ at $\sin^2\theta_W = 1/4$; non-zero at PDG | $1.1\times 10^{-16}$ | $10^{-15}$ | **PASS** |
| Z12 | $m_Z = 0$ Proca step reduces bit-for-bit to massless step | $0.0$ | $0.0$ | **PASS** (bit-for-bit) |

Total: **12 / 12 PASS** (`OVERALL: PASS`, 0.25 s wall time).

Six results are bit-for-bit zero (Z1, Z3, Z8, Z9, Z12, and effectively Z7 modulo float-add round-off); the remainder are at machine ε / FFT floor.

---

## 5. The Z11 prediction (electron vector coupling)

At the F45 bare lattice angle the SM vector / axial decomposition

$$g_V^f \;=\; T_3^f - 2 Q^f \sin^2\theta_W,\qquad g_A^f \;=\; T_3^f$$

yields the table

| Species $f$ | $T_3^f$ | $Q^f$ | $g_V^f$ at $\sin^2\theta_W=1/4$ | $g_V^f$ at PDG $0.2312$ |
|---|---:|---:|---:|---:|
| $\nu_L$ | $+1/2$ | $0$ | $+1/2$ | $+1/2$ |
| $e_L$ | $-1/2$ | $-1$ | **$0$** | $-0.0376$ |
| $u_L$ | $+1/2$ | $+2/3$ | $+1/6$ | $+0.1916$ |
| $d_L$ | $-1/2$ | $-1/3$ | $-1/3$ | $-0.3458$ |

The $g_V^{e_L} = 0$ entry is a structural prediction of the σ ↔ τ swap (F45 §"Casimirs"): the L-electron's effective vector coupling to Z is a balance between the SU(2)$_L$ contribution $-1/2$ and the electromagnetic contribution $+2 s^2_W$. F45 fixes $s^2_W = 1/4$ from the swap dimension count alone, and that value is *exactly* what makes those two contributions cancel. The corresponding right-handed coupling is $g_V^{e_R} = -2 Q^{e_R} s^2_W = +1/2$ (twice the magnitude of the L coupling but opposite sign in the $T_3$ contribution it doesn't have).

This is testable: at the F45 bare angle, parity-violating asymmetries in $e^+e^-$ collisions on the Z pole would vanish at tree level. The 1.77 % gap between $m_Z/m_W = 2/\sqrt 3$ (F45) and the PDG 1.1346 is the same gap that separates $g_V^{e_L} = 0$ (F45) from the measured $\approx -0.04$ — i.e. the F45 zero is the *same* prediction as the F45 mass ratio, expressed in a different observable. RG running and lattice loop corrections (neither implemented) must close the same numerical gap in both places.

---

## 6. The Z2 source-basis identity

The algebraic identity tested in Z2 is

$$g\,W^3_\mu\,J^{3\mu} \;+\; g'\,B_\mu\,(J^{\rm em\,\mu} - J^{3\mu}) \;\equiv\; e\,A_\mu\,J^{\rm em\,\mu} \;+\; g_Z\,Z_\mu\,(J^{3\mu} - s^2_W\,J^{\rm em\,\mu})$$

with $A = \cos\theta_W B + \sin\theta_W W^3$, $Z = -\sin\theta_W B + \cos\theta_W W^3$, $e = g\sin\theta_W = g'\cos\theta_W$, $g_Z = g/\cos\theta_W$. Substituting and using $\tan\theta_W = g'/g$:

- A coefficient: $g s_W J^3 + g' c_W (J^{\rm em} - J^3) = (g s_W - g' c_W) J^3 + g' c_W J^{\rm em} = 0 \cdot J^3 + e J^{\rm em}$ ✓
- Z coefficient: $g c_W J^3 - g' s_W (J^{\rm em} - J^3) = (g c_W + g' s_W) J^3 - g' s_W J^{\rm em} = (g/c_W) J^3 - g(s^2_W/c_W) J^{\rm em}$
  $= g_Z (J^3 - s^2_W J^{\rm em})$ ✓

That equality is the substantive content of "Weinberg mixing produces the correct Z neutral current". F35 verified the rotation of the *fields*; Z2 verifies that the same rotation produces the correct rotation of the *currents* — and that the SM bookkeeping $J^Y/2 = J^{\rm em} - J^3$ (from $Q = T_3 + Y/2$) closes consistently per site. The residual $2.7\times 10^{-15}$ across four Weinberg angles is the FFT-free, pure-arithmetic floor for `L = 16` random fields.

---

## 7. Relationship to prior findings

| Finding | Connection |
|---|---|
| F26 — c_lat as rotation rate | Z propagates via the same even-dispersion F26 rotation as photon (test Z4) |
| F27 — Chiral SU(2)$_L$ mass | $T_3$ assignment for L-doublet supplies $g_L^f$ via the SM formula |
| F35 — Electroweak mixing | F48 promotes the algebraic mixing to a dynamical Z field; Z3 replays W6.3; Z6 confirms commutation extends to the propagating Z |
| F36 — Massive W (Proca) | Same Proca dispersion structure $\omega^2 = m^2 + \Omega_{\rm even}^2$ used for Z (Z5) |
| F38 — FG-1 anomaly cancellation | Per-species $(T_3, Q)$ registry used here is the anomaly-cancelling assignment |
| F40 — Quark electroweak | Z couplings extend to $u_L, d_L, u_R, d_R$ with the same SM formula; verified per species |
| F41 — Hypercharge Higgs-free | Y assignment used for the $J^{\rm em} - J^3 = J^Y/2$ identity in Z2 |
| F42 — Dynamical χ kinetic | The R-handed singlets that now feel Y via F42 are exactly the R-couplings $g_R^f$ tested here |
| F44 — Rank-1 $m_A = 0$ | $m_A = 0$ and $m_Z = m_W/\cos\theta_W$ are structurally the same identity used by Z3 |
| F45 — σ ↔ τ swap Weinberg angle | F45 default $\theta_W = \pi/6$ supplies the bare lattice value tested in Z11 |
| F46 — Spherical Pythagorean mass | Z's Proca dispersion is the bosonic analogue of the same identity Z is a spin-1 Proca, not a Dirac, but the structural form $\omega^2 = m^2 + \Omega^2$ is the small-angle Euclidean limit of the same spherical law |

---

## 8. Exactness-inventory updates

### Tier 1 — Exact algebraic results

| # | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| 133 | Z1 — per-species $(g_L, g_R) = (T_3 - Q s^2_W,\,-Q s^2_W)$, 3 angles × 7 species | identity | $0.0$ | F48-Z1; `test_FG4_dynamical_Z.py` |
| 134 | Z3 — $m_Z / m_W = 1/\cos\theta_W$, 5 angles × 3 masses (replay of W6.3 via z_mass_from_w) | identity | $0.0$ | F48-Z3 |
| 135 | Z8 — $\nu_L$ Z couplings $(g_L,g_R,g_V,g_A) = (1/2, 0, 1/2, 1/2)$ ∀ θ_W (20 angles) | identity | $0.0$ | F48-Z8 |
| 136 | Z9 — photon coupling to neutrinos $\equiv 0$ (Q_ν = 0) | identity | $0.0$ | F48-Z9 |
| 137 | Z10 — $(g_V, g_A) = (T_3 - 2Q s^2_W, T_3)$, 4 angles × 7 species | identity | $2.8\times 10^{-17}$ | F48-Z10 |
| 138 | Z11 — F45 prediction $g_V^{e_L} = 0$ at $\sin^2\theta_W = 1/4$, with counter-check at PDG angle | identity at F45 | $1.1\times 10^{-16}$ | F48-Z11 |
| 139 | Z12 — Proca step at $m_Z = 0$ = massless step (bit-for-bit code equivalence) | identity | $0.0$ | F48-Z12 |
| 140 | Z2 — source-basis identity $g W^3 J^3 + g'(B)(J^{\rm em}-J^3) = e A J^{\rm em} + g_Z Z (J^3 - s^2_W J^{\rm em})$, 4 angles | identity | $2.7\times 10^{-15}$ | F48-Z2 |
| 141 | Z7 — source kick bit-for-bit additive in $E_Z$, $B_Z$ unchanged | identity | $8.9\times 10^{-16}$ (FP-add cancellation) | F48-Z7 |

### Tier 2 — Machine-precision under time evolution

| # | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| 51 | Z4 — free Z dispersion = $\Omega_{\rm even}(\mathbf k)$ over 40 ticks | identity | $1.0\times 10^{-13}$ rel | F48-Z4 |
| 52 | Z5 — Proca Z dispersion $\omega^2(\mathbf k) = m^2 + \Omega_{\rm even}^2$ over 30 ticks, 4 masses | identity | $1.5\times 10^{-13}$ rel | F48-Z5 |
| 53 | Z6 — mixing $\circ$ z-propagation commutator over 25 ticks at $\theta_W = \pi/6$ | $\equiv 0$ | $7.0\times 10^{-15}$ | F48-Z6 |

Net new: **9 Tier-1 + 3 Tier-2 = 12 entries**.

---

## 9. What this does and does not derive

**Derived / verified:**

- A dynamical Z field as a real $(E_Z, B_Z)$ propagating pair on the BCC lattice, with both massless and Proca dispersion.
- The SM neutral current $J^Z = J^3 - \sin^2\theta_W J^{\rm em}$ built explicitly from per-species densities; cross-checked against the per-species sum $\sum_f (g_L^f \rho_L^f + g_R^f \rho_R^f)$ — both forms agree per site to FFT floor.
- The source-basis identity that connects the (W^3, B) gauge basis to the (A, Z) mass basis — the linchpin of "Weinberg mixing produces the correct neutral current".
- The F45 prediction that $g_V^{e_L} = 0$ exactly at the bare lattice angle, and the entire bare-angle vector-coupling table.
- The Z mass equation $m_Z = m_W / \cos\theta_W$ as a `z_mass_from_w` helper that consumes any θ_W — including the F45 default — and reproduces W6.3 bit-for-bit.

**Not derived (open questions):**

- Full non-Abelian Z self-coupling. Z is Abelian at tree level (no $[Z, J]$ commutator), so this is structurally correct *to leading order in the coupling*; the gauge-field self-interactions live entirely in the W$^\pm$ and W$^3$ sectors and inherit the Z component only through the F35 mixing.
- The Z's coupling to the *spatial* currents (J⃗) — only the time-component $J^0(x)$ was tested. Extending to the full 4-current $J^\mu$ requires a gauge-covariant temporal slicing convention that is open across the project (the same issue F36 backreaction worked around for W).
- Quantitative loop-level corrections (vertex corrections, $\rho$ parameter, $\sin^2\theta_W^{\rm eff}$). These require an explicit loop integrator the model does not yet have.
- The Z decay width $\Gamma_Z$ from the dynamical coupling — needs phase-space measure + a renormalisation prescription.

---

## 10. Provenance

- Task source: `first-gen-completeness.md` §3 item 5 (2026-05-22) and §5.1 row FG-4.
- Mathematical derivation: §6 above; standard SM Lagrangian rewriting in the (A, Z) mass basis; the F45 bare-angle electron prediction (§5) is the structural novelty.
- Module: `ca-simulation/ca_z_field.py` (~440 lines, additive — no existing surface modified).
- Numerical verification: `model-tests/test_FG4_dynamical_Z.py` (~440 lines), 12/12 PASS in 0.25 s on a 16³ BCC lattice.
- Filed `test-results/FG4_dynamical_Z.json`.

This discharges the FG-4 entry on the Tier-A first-generation checklist. The remaining Tier-A items are FG-8 (end-to-end β-decay charged-current integration) and FG-9 (per-species $C/CP$); FG-5 (R-handed hypercharge dynamics) was already closed by F42.

---

## 11. Files

- `ca-simulation/ca_z_field.py` — new module (this finding)
- `model-tests/test_FG4_dynamical_Z.py` — verification script (Z1–Z12)
- `test-results/FG4_dynamical_Z.json` — numerical results
- `findings/F48-dynamical-Z-neutral-current.md` — this finding
