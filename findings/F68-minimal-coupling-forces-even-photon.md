# F68 — U(1) minimal coupling forces the chirality-even (non-birefringent) photon; the birefringent bilinear is a different SU(2) channel

**Date:** 2026-06-01 - 14:41
**Status:** Confirmed — derivation + 3/3 checks against the model's real operators (residuals 1.1×10⁻¹⁶ / 0 / 0). Resolves the F67 either/or in favour of the even photon being the physical EM photon — conditional on the physical photon being the gauge connection.
**Script:** `model-tests/test_F68_minimal_coupling_forces_even_photon.py`
**Results:** `test-results/F68_minimal_coupling_forces_even_photon.json`
**Cross-references:** [[F67-even-law-photon-vs-bilinear-mutually-exclusive]] (the either/or this resolves), [[F66-allsky-birefringence-anisotropy-no-rescue]] (option 1), [[F65-helicity-chirality-map-confirmed]], [[F39-two-helicity-photon-bilinear]] (§5.1 non-unification), [[F29-w-triplet-bilinear-su2-bridge]], [[F27-complex-mass-chiral-su2]]; `ca_dirac.py` (`mass_step_1flavor_u1`), `ca_hypercharge.py`; McPhee notebook `reference-research/physics-notes-complete.md` pp.5–6, 12–13.

---

## The question

F67 showed the composite two-branch bilinear photon (birefringent, chiral law) and the chirality-even photon (non-birefringent) are mutually exclusive, separated by exactly $\Delta\Omega/2$. The decisive open item: **is the photon that minimally couples to electric charge structurally forced to be the even one?** If yes, F66 option 1 is derived rather than chosen, and the birefringence tension dissolves.

## The derivation

In this model the U(1)/hypercharge gauge field enters the fermion update **only as a scalar (Peierls) phase proportional to the identity** in Weyl-spinor space:

- complex-mass U(1) (`ca_dirac.mass_step_1flavor_u1`): the per-cell unitary off-diagonal block is $i\,s_m\,e^{i\theta}\,\mathbf I$;
- hypercharge (`ca_hypercharge`): $e^{i\alpha(x)Y/2}\,\mathbf I$ per chirality, obeying $S[\alpha+\beta]\big(e^{i\beta Y/2}\chi\big)=e^{i\beta Y/2}S[\alpha](\chi)$.

So the gauge coupling operator is $P=e^{i\theta}\mathbf I_2$. The Weyl QCA unitary is $U^\pm(k)=u\,\mathbf I-i(\mathbf n\cdot\boldsymbol\sigma)$ (F26/Paper 1). Then:

1. **$[P,U^\pm(k)]=0$ — minimal coupling is helicity-blind.** A c-number phase commutes with everything. Verified $1.1\times10^{-16}$ over 4000 random $k$ × both branches. Hence $P\,\psi^\pm=e^{i\theta}\psi^\pm$: the gauge phase advances *both* helicity eigenstates identically.
2. **It can source only the helicity-symmetric dispersion.** Birefringence is, by F65, the two RS helicities $F^\pm=E\pm iB$ acquiring *different* magnitudes ($\Omega^+\neq\Omega^-$). An identity coupling produces equal phase on both → the common magnitude → $\Omega_\text{even}$ → the even law. **Non-birefringent, forced.** (Confirmed on the real U(1) mass step: the phase picked up by the two helicity/spin channels is equal to $0.0$, T2.)
3. **The composite photon is a different SU(2) channel.** The bilinear photon is $F^i\sim\phi^\dagger\sigma^i\psi$ (F39). The operator $\sigma^i$ does **not** commute with $\mathbf n\cdot\boldsymbol\sigma$: $\lVert[\sigma_x,\mathbf n\cdot\boldsymbol\sigma]\rVert=1.99$. So the bilinear couples to the branch splitting and carries $\Omega^\pm$ per helicity → **birefringent**. The birefringence $\Delta\Omega$ lives *entirely* in this $\sigma$-vector channel (T3: even-channel helicity gap $=0$; chiral-channel gap $=1.03\times10^{-2}$ on the body diagonal at $k=0.4$).

**Conclusion.** The U(1) connection and the composite bilinear are two different representations of the same lattice SU(2): the gauge photon is the **identity/singlet** channel (helicity-blind → even → non-birefringent); the composite photon is the **$\sigma$-vector** channel (branch-split → chiral → birefringent). Minimal coupling selects the identity channel. **The field that couples to electric charge is therefore the even-law, non-birefringent photon — F66 option 1 is derived, not chosen.**

## The necessary caveat (what this commits the model to)

This says the physical electromagnetic photon is the **U(1) gauge connection** — the very object removed from `ca_dirac` on 2026-05-26 in favour of the composite bilinear (Phase E1). The composite $\sigma$-bilinear is then a *distinct* excitation (the "antisymmetric spin-1 pair"), not the free EM photon. So:

- The F39 §5.1 composite-vs-gauge non-unification is resolved by **separation**, not unification: they are different channels, and the *gauge* one is the physical EM photon.
- The birefringence prediction (F30/F65/F66) attaches to the $\sigma$-bilinear, **not** to the charge-coupling photon that GRB/AGN polarimetry probes. So the F64/F65/F66 tension **dissolves** — the Planck-scale cell is no longer excluded by polarimetry, because the polarimetric photon is the even one.
- Cost: the appealing "photon *is* the same $(\mathbf E,\mathbf B)$-bilinear as mass/gravity" picture (F26/F29/F64) no longer applies to the *electromagnetic* photon; it applies to the $\sigma$-channel excitation. The F29 SU(2) W-triplet bridge still stands on the bilinear, but the U(1) photon is now outside it (consistent with the SM, where the photon is a $U(1)_Y$–$SU(2)_L$ mixture, not a pure triplet member).

The remaining open item is therefore *constructive*, not conceptual: **reinstate the U(1) connection photon as the physical EM field** (the removed `dirac_step_u1_*` path), give it the even-law $(\mathbf E,\mathbf B)$ propagator (`_f26_rotation_step`, already the W/Z law), and verify Aharonov–Bohm / Maxwell behaviour on that field — then the photon sector is birefringence-safe and Planck-cell-consistent.

## What the notebooks add

**McPhee's notebook** (`physics-notes-complete.md`) is strikingly on point and *anticipated this degree of freedom*:
- pp.5–6: "spinor electrodynamics involves two spin-½ fermion-photons … they behave together like a single boson $\gamma$ that only occurs as a pair … Could photons be a Cooper pair of spinor photons?" — this is the composite ($\sigma$-bilinear) photon, the birefringent channel.
- **p.6 item 6: "Is there a scalar photon?"** — the notebook explicitly raises the helicity-blind/identity channel. F68 answers: yes — the *scalar* (identity-channel) photon is precisely the U(1) gauge connection, and it is the non-birefringent one. The notebook flagged the exact mode that resolves the birefringence problem.
- p.6 item 8: "Can we understand W and Z bosons … other states of spinor photons?" — consistent with the channel/multiplet picture.
- pp.12–13: $\psi^\pm$ as the two helicity branches that "transform into one another under parity" — the F65 helicity↔chirality content the whole chain rests on.
- The notebook's Sachs framing (one spinor/quaternion field unifying gravity+EM, criticising arbitrary $SU(2)\times U(1)$) is the philosophical anchor for F64's one-field gravity.

**Ludwig's thesis** (`mark_a_ludwig_thesis.pdf`, *Numerical solutions of lattice quantum fields with a hierarchy of Schroedinger-like equations*, U. Arizona) is about a Schrödinger-picture coupled hierarchy for an interacting **scalar** field — perturbation/renormalisation and 1-D lattice scattering numerics. It is methodologically adjacent (lattice QFT in the Schrödinger picture, which "singles out a time axis so manifest covariance is lost, though the system is relativistically invariant" — echoing the model's emergent-time stance) but it does **not** treat the photon, helicity, or gauge construction. It does not bear on the even-vs-chiral question; useful only as background on Schrödinger-picture lattice QFT.

## Exact vs numeric

| Result | Tier | Residual |
|---|---|---|
| $[e^{i\theta}\mathbf I,\,U^\pm(k)]=0$ (helicity-blind coupling) | machine | $1.1\times10^{-16}$ |
| gauge phase equal on both helicities (real U(1) mass step) | exact | $0.0$ |
| birefringence absent from even channel | exact | $0.0$ |
| $[\sigma_x,\mathbf n\cdot\boldsymbol\sigma]\neq0$ (composite channel splits) | structural | $1.99$ |
| chiral-channel birefringence (body diag, $k{=}0.4$) | quantitative | $1.03\times10^{-2}$ |

## Files
- Test: `model-tests/test_F68_minimal_coupling_forces_even_photon.py`
- Results: `test-results/F68_minimal_coupling_forces_even_photon.json`
- Operators: `ca-simulation/ca_dirac.py` (`mass_step_1flavor_u1`), `ca_hypercharge.py`, `ca_bcc.py` (`bcc_unitary`, `_bcc_uvec`).
