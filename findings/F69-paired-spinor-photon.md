# F69 — The photon as a bound pair of two spin-½ Weyl quanta (non-birefringent); the composite σ-bilinear retired as the photon

**Date:** 2026-06-01 - 15:02
**Status:** Confirmed — new module `ca_photon_pair.py` + 5/5 checks (residuals 0 / 1.8×10⁻¹⁵ / 7.7×10⁻⁶ FD / 0 / ≤6×10⁻¹⁵). The composite σ-bilinear is retired *as the photon* (kept for the non-Abelian sectors).
**Script:** `model-tests/test_F69_paired_photon.py`
**Module:** `ca-simulation/ca_photon_pair.py`
**Results:** `test-results/F69_paired_photon.json`
**Cross-references:** [[F68-minimal-coupling-forces-even-photon]] (the identity channel this realizes), [[F67-even-law-photon-vs-bilinear-mutually-exclusive]], [[F66-allsky-birefringence-anisotropy-no-rescue]], [[F65-helicity-chirality-map-confirmed]], [[F39-two-helicity-photon-bilinear]] (the retired construction), [[F26-speed-of-light-as-rotation-rate]]; McPhee notebook `reference-research/physics-notes-complete.md` pp.5–6, 12–13; `key-decisions.md`, `CLAUDE.md` core decision 5.

---

## The decision

Build out Ludwig's "spinor electrodynamics" photon (notebook pp.5–6) — *two spin-½ "fermion-photons" γ₁/₂ that "behave together like a single boson γ that only occurs as a pair; they don't occur separately"* — as **the** electromagnetic photon, and retire the composite σ-bilinear (`ca_maxwell.py`) as the photon because its linear vacuum birefringence is not real-world tenable (excluded by GRB/AGN polarimetry, F65/F66/F67).

## The construction

The photon is a **bound (+,−) pair**: total momentum $k$ shared by two Weyl constituents at $k/2$ each — one on the $+$ chiral branch, one on the $-$. Because the pair is bound and symmetric, its phase per tick is the **sum** of the constituent phases:

$$\Omega_\text{pair}(k)=\omega^+(k/2)+\omega^-(k/2)\;\equiv\;\Omega_\text{even}(k).$$

This is *exactly* the even-law rate of `ca_wmu._f26_rotation_step` (verified residual $0$, PP1), so the paired photon's $(\mathbf E,\mathbf B)$ propagator is the even law — no new propagator is invented; `ca_photon_pair.photon_step_spectral` names it as the photon law and adds the pair construction + verification.

**Why this is non-birefringent — the mechanism.** In the retired composite bilinear, the two photon helicities $F^\pm=\mathbf E\pm i\mathbf B$ were assigned to the two branches independently ($F^+\!\to\!\Omega^+$, $F^-\!\to\!\Omega^-$), so a generic linear polarization split by $\Delta\Omega$. In the paired photon there is **no single-branch photon**: it "only occurs as a pair," always containing both branches symmetrically, so both helicities of the resulting field ride the one rate $\Omega_\text{pair}$. The split has nothing to split against. The pairing is the physical realization of the U(1) **identity channel** that minimal coupling forces (F68): the helicity-symmetric sum is the helicity-blind dispersion.

## What the test shows (5/5)

| # | Check | Result | Tier |
|---|---|---|---|
| PP1 | $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)=$ even-law rate | resid $0$ (2000 $k$) | exact |
| PP2 | Non-birefringent: linearly polarized body-diagonal mode, 6 ticks, $S=\phi_++\phi_-$ | paired $S=-1.8\times10^{-15}$ (none) vs retired chiral $S=+0.07924=-\Delta\Omega N$ | machine |
| PP3 | Massless & luminal: $\Omega_\text{pair}/k\to0.577350$, $\Omega_\text{pair}(0)=0$, group velocity $\to1/\sqrt3$ | max err $7.7\times10^{-6}$ (FD) | quantitative |
| PP4 | "Only as a pair": pair phase $=\omega^+(k/2)+\omega^-(k/2)$ (constituent sum); an unpaired single branch would carry $\Omega^\pm$ (split median $5.3\times10^{-3}$) | resid $0$ | machine |
| PP5 | Spin-1: two transverse polarizations ($|\mathbf E\!\cdot\!\hat k|/|\mathbf E|=1.8\times10^{-17}$), real ($10^{-15}$) and norm-conserving ($6\times10^{-15}$) | — | machine |

## What was retired, and what was kept

- **Retired as the photon:** the composite σ-bilinear $G^i=\phi^\dagger\sigma^i\psi$ and the chiral propagator `w_propagation_step_chiral` *in their role as the U(1) electromagnetic photon*. A deprecation banner now heads `ca_maxwell.py`.
- **Kept:** the same σ-bilinear / chiral machinery for the **massive and non-Abelian sectors** — W (`ca_wmu`), Z (`ca_z_field`), gluon (`ca_gluon`) — which use the chiral propagator and are **not** under the photon polarimetry bound (massive/confined, no astrophysical vacuum-birefringence constraint). Retiring it there would break those sectors and is not warranted by the observation that excludes it for the photon.

Decision recorded in `key-decisions.md` and `CLAUDE.md` (core decision 5).

## Why this is the right object (not an ad-hoc patch)

It is forced from three independent directions that now agree:
1. **Observation** (F65/F66): the photon must be non-birefringent → $\Omega_\text{even}$.
2. **Minimal coupling** (F68): the charge-coupling photon is the identity channel $e^{i\theta}\mathbf I$ → helicity-blind → $\Omega_\text{even}$.
3. **Ludwig's construction** (pp.5–6): the photon is a bound pair of two γ₁/₂ → symmetric $(+,-)$ → rate $\omega^+(k/2)+\omega^-(k/2)=\Omega_\text{even}$.

All three land on the same dispersion. The notebook's open question "Is there a scalar photon?" (p.6 #6) is answered: the *scalar/identity* photon is the paired photon, and it is the physical one.

## Reconciliation — the paired photon de-falsifies the F64 G-matched cell size

**Added 2026-06-01 - 17:08.**

The non-birefringence of the paired photon does more than settle a polarimetry tension in the abstract — it **restores the cell size that the gravity sector independently requires.** The chain:

- **F64 (D-EM10) pins $a$ to reproduce Newton's $G$.** With the Sakharov-induced coupling $a=\sqrt{2\pi\eta g_*}\,d^{1/4}\ell_P$ ($\eta_\text{Weyl}=\tfrac1{12}$, $g_*=16$, $d=3$), the cell comes out $a\approx3.81\,\ell_P\approx6.2\times10^{-35}$ m. This is not a free choice: it is *the* value that makes $G$ the induced coupling rather than a by-hand input.
- **With the retired σ-bilinear photon, that same $a$ was falsified.** F65/F66 showed the bilinear's body-diagonal linear birefringence overshoots the GRB/AGN polarimetry bound by $\sim14$ decades at $a\approx6.2\times10^{-35}$ m — the model was excluded *precisely at the G-matched cell size* (F66: "falsified at the F64 one-generation cell size").
- **The paired photon removes that prediction entirely** (PP2: $S=-1.8\times10^{-15}$, exactly non-birefringent). There is no helicity split to accumulate, so the $\sim14$-decade overshoot vanishes.

Net effect: the two results now **co-certify a single cell size.** $a\approx6.2\times10^{-35}$ m simultaneously (i) reproduces $G$ via D-EM10 and (ii) survives all astrophysical vacuum-birefringence bounds, with the Lorentz-violation cutoff landing at $E_\text{LV}\sim2.9\times10^{19}$ GeV (F65), comfortably above the $\sim10^{19}$ GeV GRB time-of-flight bound. This is a **consistency gain, not an accuracy gain**: the model's dimensionless predictions (Weinberg angle, mass ratios, $c_\text{lat}=1/\sqrt3$, PPN $\beta=\gamma=1$, Mercury $42.98''$/cy, factor-2 bending) are $a$-independent and unchanged. What the paired photon buys is that the gravity-fixed $a$ is no longer ruled out by the photon sector.

*Caveat:* $g_*=16$ is one-generation and the gauge-sector contribution to the gravitating mode count is still posited (F64 D-EM10 open item), so $a\approx6.2\times10^{-35}$ m carries a mild $\sqrt{\cdot}$ uncertainty — it is the current best pin, not a locked number. Cross-references: [[F64-em-connection-gravity]], [[F65-helicity-chirality-map-confirmed]], [[F66-allsky-birefringence-anisotropy-no-rescue]], [[F61-weyl-eta-and-gstar-prefactor]].

## Open / next

- **Reinstate the dynamical U(1) connection + Aharonov–Bohm.** The paired photon supplies the free-field dispersion/propagator; the charge coupling itself (the `dirac_step_u1_*` path removed 2026-05-26) should be re-added on the even-law field and AB phase / Maxwell curl re-verified (the F68 constructive item).
- **Two-body binding dynamics.** Here the pair is treated at the dispersion/propagator level (its rate is the constituent sum, exact). A genuine two-constituent bound-state simulation (the "negative binding energy," McPhee #5; the massless-pair condition) is the deeper follow-up.
- **W/Z/gluon birefringence.** Those sectors keep the chiral law; confirm no observational tension arises there (expected none — massive/confined), or migrate them by the same pairing argument if a clean one exists.

## Files
- Module: `ca-simulation/ca_photon_pair.py` (`pair_dispersion`, `photon_step_spectral`, `build_pair_mode`, `group_velocity`, `pair_birefringence`)
- Test: `model-tests/test_F69_paired_photon.py`
- Results: `test-results/F69_paired_photon.json`
- Retirement banner: `ca-simulation/ca_maxwell.py` (top docstring).
