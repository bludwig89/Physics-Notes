# F89 — One entity, two channels: the singlet bilinear of the same Weyl constituents IS the paired photon; the σ-vector channel IS the W/Z/gluon law

**Date:** 2026-06-04 - 01:25
**Numbering:** built as F88 concurrently with the colour-condensate finding that took F88 → renumbered **F89** (same F53/F54-style collision).
**Status:** Confirmed — 10/10 checks against the real model operators (worst machine residual $4.9\times10^{-13}$ over 8 ticks × 2000 k; one identity exactly $0$). Closes the "are we introducing two different photon entities?" question raised against F68/F69.
**Script:** `tests/findings/test_F89_singlet_bilinear_is_paired_photon.py`
**Results:** `test-results/F89_singlet_bilinear_paired_photon.json`
**Cross-references:** [[F69-paired-spinor-photon]] (the pair construction this grounds), [[F68-minimal-coupling-forces-even-photon]] (the channel claim made constructive), [[F67-even-law-photon-vs-bilinear-mutually-exclusive]], [[F39-two-helicity-photon-bilinear]], [[F29-w-triplet-bilinear-su2-bridge]], [[F26-speed-of-light-as-rotation-rate]]; `ca_photon_pair.py`, `ca_wmu._f26_rotation_step`, `ca_maxwell.py` (kept σ-bilinear machinery), `ca_bcc.py`.

---

## The question

F69 retired the composite σ-bilinear *as the photon* but kept it for W/Z/gluon, while the EM photon became the bound (+,−) spinor pair. Does the model then contain **two unrelated kinds of gauge-boson entity** — a "pair photon" and a "bilinear boson"? F68 argued no (identity channel vs σ-vector channel of the same lattice SU(2)), but the argument was operator-commutator level; the singlet identification was never verified constructively with the model's real evolution operators.

## The claim, made precise

A pair of Weyl constituents decomposes in spin space as

$$2\otimes 2 \;=\; \mathbf{1}\;(\varepsilon=i\sigma_y \text{ contraction})\;\oplus\;\mathbf{3}\;(\sigma\text{-vector}),$$

and the photon/W distinction is **which channel of the same bilinear object you read**, combined with **which branch pairing you feed it**:

| | cross-branch (+,−) pair, $k/2$ each | same-branch pair |
|---|---|---|
| rate carried | $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)=\Omega_\text{even}$ | $\Omega^\pm=2\omega^\pm(k/2)$ (chiral law) |
| birefringence | none (branch-symmetric) | $\Delta\Omega\neq0$ (body diagonal) |
| physical role | **photon** (F69) | **W/Z/gluon** (F39/F29) |

## What the test shows (10/10)

Constituents are built closed-form (no `np.linalg.eig` on chiral matrices, per practice): $\chi_+$ is the algebraic $(\hat{\mathbf n}\cdot\boldsymbol\sigma)=+1$ spinor, and evolution is literal matrix application of $U^\pm(k/2)=u\mathbf I-i(\mathbf n\cdot\boldsymbol\sigma)$.

| # | Check | Residual | Tier |
|---|---|---|---|
| T1a | cross-branch singlet $G_s=\phi^T(i\sigma_y)\psi$ advances per tick at exactly $\Omega_\text{pair}(k)$ = `ca_photon_pair.pair_dispersion` (2000 k, 8 ticks) | $4.9\times10^{-13}$ | machine |
| T1b | **every** Paper-1 channel $G^i=\phi^T\sigma^i\psi$ of the *same* cross-branch pair rides the *same* $\Omega_\text{pair}$ — the rate attaches to the pairing (the entity), not the channel operator | $4.9\times10^{-13}$ | machine |
| T2 | measured pair rate == rotation angle actually applied by `ca_wmu._f26_rotation_step` (the canonical photon/even propagator), mode by mode | $4.9\times10^{-13}$ | machine |
| T3 | branch swap (ψ on −, φ on +) leaves the rate unchanged — "only occurs as a pair" has no orientation | $1.2\times10^{-13}$ | machine |
| T4 | same-branch pairs through the *same* σ-channel operators ride $\Omega^+$ / $\Omega^-$ | $2.0\times10^{-14}$ | machine |
| T4 | their split == `pair_birefringence` | $0.0$ | **exact** |
| T4 | chiral split nonzero: median $6.4\times10^{-3}$, body diagonal $k=0.4$: $-1.03\times10^{-2}$ (matches F68's chiral-channel gap) | — | structural |
| T5 | under simultaneous same-branch transport, the Hermitian identity channel $\phi^\dagger\sigma^0\psi$ is invariant (the U(1) coupling channel is blind) | $2.8\times10^{-15}$ | machine |
| T5 | the Hermitian σ-vector $\phi^\dagger\sigma^i\psi$ precesses about $\hat{\mathbf n}$ by exactly $2\omega$ per tick (the adjoint rotation the W sector rides) | $6.1\times10^{-14}$ | machine |

## What this settles

1. **No second photon entity.** The singlet channel of the same spinor-pair bilinear, fed the cross-branch pairing, reproduces the F69 paired-photon dispersion and the `_f26_rotation_step` propagator angle to machine precision. "Paired photon" and "σ-bilinear machinery" are one object read in two irreps.
2. **F68's channel argument is now constructive**, not just a commutator statement: σ⁰ frozen / σ-vector precessing at $2\omega$ under the real walk (T5) is the dynamical content of $[P,U^\pm]=0$ vs $[\sigma_i,\mathbf n\cdot\boldsymbol\sigma]\neq0$.
3. **The propagator split is derived, not stipulated.** Even law for the photon and chiral law for W/Z/gluon both follow from the operator content + branch pairing of one construction — mirroring the SM's singlet-mixture photon vs triplet W.
4. T1b sharpens the picture: for the *cross-branch* pair, all four channels ride $\Omega_\text{pair}$ — so what distinguishes photon from W is **not** the rate of a frozen mode but the channel's transformation law and which pairing the sector's propagator implements (T4/T5).

## Open / next

- **Two-body binding dynamics** (carried over from F69): this test is still at the eigenmode/dispersion level; a genuine two-constituent bound-state simulation with negative binding energy remains the deeper follow-up.
- The σ-vector channel's same-branch pairing is *used* by W/Z/gluon but not *forced* there by an argument of F68's strength; a minimal-coupling-style derivation of why the non-Abelian sectors must take the chiral pairing would complete the symmetry.

## Files
- Test: `tests/findings/test_F89_singlet_bilinear_is_paired_photon.py`
- Results: `test-results/F89_singlet_bilinear_paired_photon.json`
- Operators exercised: `ca_bcc._bcc_uvec`/`bcc_dispersion`, `ca_photon_pair.pair_dispersion`/`pair_birefringence`, `ca_wmu._f26_rotation_step`.
