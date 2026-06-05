# F91 — Pairing classification theorem: the branch structure of each coupling forces its channel — γ even (forced), W± chiral (forced), Z mixed (derived), gluon even (forced; the chiral BCC gluon assignment is unforced)

**Date:** 2026-06-04 - 14:05
**Numbering:** built as F90 concurrently with the E2E non-Abelian certification that took F90 → renumbered **F91**.
**Status:** Confirmed — 13/13 checks (5 exact over ℚ / structural-zero, 6 machine ≤ 2×10⁻¹³, 2 quantitative/contrast). Completes the F68→F89 chain: the chiral pairing is now *derived* where it holds (W±) and shown *unforced* where it was assumed (gluon BCC).
**Script:** `model-tests/test_F91_pairing_classification.py`
**Results:** `test-results/F91_pairing_classification.json`
**Cross-references:** [[F89-singlet-bilinear-is-paired-photon]] (the open item this closes), [[F68-minimal-coupling-forces-even-photon]] (the argument mirrored), [[F90-e2e-nonabelian-bilinear-backreaction]] (independent closed form for the chiral-Proca mass suppression, corroborating Z3), [[F67-even-law-photon-vs-bilinear-mutually-exclusive]], [[F45]] (θ_W = π/6), [[F42]] (hypercharge, Q = T3 + Y/2), [[F37]] (chiral step), [[F30]]; `ca_z_field.py`, `ca_wmu.py`, `ca_gluon.py`, `ca_photon_pair.py`.

---

## The question (F89's open item)

F68 forced the photon to the even/identity channel: its coupling is a scalar in branch space, so it can only source the helicity-symmetric dispersion. F89 showed photon vs W/Z/gluon is a channel split of one spinor-pair entity — but the *chiral* pairing of the non-Abelian sectors was used, not forced. Is there an F68-strength argument per sector?

## The theorem

Let $(g_L, g_R)$ be a sector's coupling weights on the two BCC chiral branches (the model's γ⁵). The branch structure of the coupling operator forces the propagation channel:

| sector | $(g_L, g_R)$ | branch operator | forced channel | code status |
|---|---|---|---|---|
| γ | $(Q, Q)$ | scalar $\propto\mathbf I$ | **even** (identity) | ✓ conforms (`ca_photon_pair`, F68/F69) |
| W± | $(g, 0)$ | projector $P_L$ | **chiral** (single-branch) | ✓ conforms (`w_propagation_step_chiral`, F37) |
| Z | $(T_3{-}Qs^2,\,{-}Qs^2)$ | neither | **neither pure channel** — even exact for the vector part; the axial part is the branch split, mass-suppressed | ✓ even step justified as the $O(k^3/m_Z)$-accurate choice |
| gluon | $(g_s, g_s)$ | scalar $\propto\mathbf I$ (colour acts on colour only) | **even** — the F68 argument verbatim | ✗ BCC path uses the chiral W step — **unforced**; 2D path already even |

## What the test shows (13/13)

**γ anchor (A1, exact ℚ):** $Q_L - Q_R = 0$ for every charged species over ℚ (the axial EM coupling vanishes identically from $Q = T_3 + Y/2$); model float tables match the rationals at $0.0$.

**W± — chiral forced:**
- **W1 (exact):** $T_3 = 0$ over ℚ for every right-handed species; in branch space the SU(2)_L coupling is $P_L=\mathrm{diag}(1,0)$, which annihilates the right branch exactly ($\|P_L\psi_R\| = 0.0$). The model's `fermion_current_isospin` is left-doublet-only *by construction* (W4.3 parity violation).
- **W2 (machine + exact):** a single-branch source makes same-branch bilinears, which ride $\Omega^s = 2\omega^s(k/2)$ ($2.1\times10^{-14}$, both branch conventions); and $|\Omega^s - \Omega_\text{even}| = |\Delta\Omega|/2$ exactly ($1.4\times10^{-17}$ — F67's separation), nonzero on the body diagonal ($5.1\times10^{-3}$ at $k{=}0.4$). **The even law is excluded for the W**: its source can never populate the cross-branch pair, because the right constituent weight is identically zero.
- **W3 (machine):** $\Omega^+(-k) = \Omega^-(k)$ exactly ($0.0$) — a real $(\mathbf E,\mathbf B)$ field whose analytic content is one branch at $+k$ necessarily carries the conjugate branch at $-k$, which **is** the F37 helicity↔branch chiral assignment; and `w_propagation_step_chiral` advances $F^\pm$ at exactly $\Omega^\pm$ ($0.0$, planted modes). So "left-projected coupling + real field" ⇒ the chiral step, uniquely.

**Z — mixed channel, derived (not chosen):**
- **Z1 (exact ℚ, $s^2 = 1/4$ from θ_W = π/6):** $g_A = T_3 \neq 0$ on the doublet (not the identity channel → even not F68-forced) and $g_R = -Q/4 \neq 0$ for charged species (not a projector → chiral not forced). `z_couplings()` floats match ℚ at $5.6\times10^{-17}$.
- **Z2 (exact ℚ):** **photon uniqueness** — any neutral coupling $a\,T_3 + b\,Y/2$ has axial part $(a-b)\,T_3$ for every species (identity $Y_L/2 = Q-T_3$, $Y_R/2 = Q$); it vanishes on the doublet iff $a=b$, i.e. iff the coupling $\propto Q$. The Weinberg rotation isolates **all** axial coupling in the Z; the identity-channel (non-birefringent) member of the neutral sector is exactly the photon. This upgrades F68: the photon isn't just *an* identity channel, it is *the unique* identity-channel direction in the neutral sector.
- **Z3 (quantitative):** the branch split the even massive-Z step neglects is $\mathrm{rel}\,\delta\omega = 8.6\times10^{-4}$ at $(m_Z{=}0.4,\,k{=}0.2)$ body-diagonal, vanishing like $k^3$ — mass-suppressed, corroborated independently by F90's chiral-Proca closed form.

**Gluon — even forced, chiral unforced:**
- **G1 (machine):** $[\,\mathrm{diag}(U^+,U^-)\otimes\mathbf I_3,\ \mathbf I_4\otimes e^{i\theta\cdot T}\,] = 0$ ($1.1\times10^{-16}$, random $k,\theta$) — the F68 commutator replayed verbatim in colour. The model's own octet bilinear applies the *same* $T^a$ to both chiralities (η and χ): vector-like by construction.
- **G2 (exact):** a colour phase advances left- and right-branch quark eigenmodes by the identical colour phase (split $= 0.0$).
- **G3 (machine + contrast):** the even-law octet step is clean — non-birefringent ($S = 0.0$) and norm-conserving ($6.8\times10^{-15}$) — while the current `gluon_rotation_step_spectral_bcc` (which reuses the chiral W step) splits by exactly $-\Delta\Omega N$ ($S = +0.56779$ vs predicted $+0.56779$). Confinement makes this unobservable, so nothing is falsified — but the assignment is **unforced**, and the F68-mirror argument + the elegant-design philosophy select the even law. The 2D gluon path (`gluon_rotation_step_spectral_2d`) already uses an even-type rotation, so BCC is the only nonconforming path.

## What this settles

1. **The F89 open item is closed**: the chiral pairing *is* F68-forced exactly where the coupling is chiral — the W±, whose source has identically zero right-branch weight. No symmetry is missing.
2. **The Z's even propagator is derived**, not a convenience: even is exact for the vector part; the axial remainder is the mass-suppressed branch split (Z3 + F90 §2).
3. **One mechanism classifies all four sectors**: channel = branch structure of the coupling. The model now has a single forcing principle from the photon through the gluon.

## Migration executed (2026-06-04 - 14:40)

The recommendation below was carried out. `ca_gluon.gluon_rotation_step_spectral_bcc` now applies the even law (`cwmu._f26_rotation_step` per octet component); the pre-migration chiral implementation is preserved verbatim as `gluon_rotation_step_spectral_bcc_chiral` for historical comparison and the F91 G3 contrast. `free_gluon_dispersion_residual_bcc` now checks against `_omega_even` (was `_chiral_dispersions`). Coherence gain: the massive gluon step already used the even law (ω_eff = √(m²+Ω_even²)), so the m→0 free limit is now consistent with it rather than relying on a special-case shortcut.

Regression after migration (all green):

| Suite | Result | Note |
|---|---|---|
| `test_FG7_gluon_dynamics.py` | 20/20 | PD.4 dispersion residual now even-law, $1.8\times10^{-13}$; PD.3 massless reduction still bit-for-bit $0.0$ |
| `test_E2E_nonabelian_bilinear.py` | 14/14 | G3 causal front, G4 massless reduction, B1/B2 back-reaction loop unaffected |
| `test_F91_pairing_classification.py` | 13/13 | unchanged |
| `test_FG7d_colour_dielectric.py` | 6/6 | CD4 references the 2D path (already even) — unaffected |
| `test_FG7e_colour_condensate.py` | 8/8 | unaffected |
| `test_F72_universal_even_propagator.py` | PASS | C5 catalog entry updated: gluon now EVEN |

No other `ca-simulation` module calls the BCC gluon step directly (verified by grep); `key-decisions.md` and `CLAUDE.md` decision 5 updated.

## Recommendation as originally flagged (now executed)

Migrate `gluon_rotation_step_spectral_bcc` from the chiral W step to the even law (the 2D path's convention), or document the chiral choice as a deliberate deviation. Nothing observable changes (confined sector); the change makes the code conform to the forcing principle.

## Open / next

- The W's chiral forcing is at the source/channel level; the deeper two-body dynamics (which branch the bound W constituents ride in a genuine binding simulation) remains with the F69 binding-dynamics item.
- Physical θ_W ≠ π/6: Z1/Z2 are ℚ-exact at the F45 bare value; for arbitrary θ_W they hold symbolically (gA = T3 is θ_W-independent), so nothing changes qualitatively.

## Files
- Test: `model-tests/test_F91_pairing_classification.py`
- Results: `test-results/F91_pairing_classification.json`
- Operators exercised: `ca_z_field.z_couplings`/`T3_TABLE`/`Q_TABLE`, `ca_wmu.w_propagation_step_chiral`/`_f26_rotation_step`, `ca_gluon` octet conventions, `ca_photon_pair.pair_dispersion`/`pair_birefringence`, `ca_bcc`.
