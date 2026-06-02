# F72 — The paired/even-law photon propagator cannot be adopted universally: the propagator law is fixed by the coupling channel (identity → even, σ-vector → chiral)

**Date:** 2026-06-01 - 16:36
**Status:** Confirmed — 4/4 checks PASS (residuals 1.8×10⁻¹⁶ / structural / a₁=−2.4×10⁻⁵ / 1.8×10⁻¹⁵). The post-F69 question "use the same method everywhere" is answered: **no** — and the model is already self-consistent.
**Script:** `model-tests/test_F72_universal_even_propagator.py`
**Results:** `test-results/F72_universal_even_propagator.json`
**Cross-references:** [[F69-paired-spinor-photon]] (the even/paired photon this generalizes), [[F68-minimal-coupling-forces-even-photon]] (the commutator selection criterion), [[F67-even-law-photon-vs-bilinear-mutually-exclusive]] (the sourceless ΔΩ/2 override), [[F39-two-helicity-photon-bilinear]] (the σ-bilinear), [[F37-rs-bcc-chirality-helicity]] (W chiral propagator), [[F43-fg7-dynamical-gluons]] (gluon as σ-bilinear), [[F29-w-triplet-bilinear-su2-bridge]].

---

## The question

After F69 retired the composite σ-bilinear *as the photon* in favour of the paired/even-law propagator (`_f26_rotation_step`), the natural follow-up: can the same even-law method be adopted **universally**, retiring the chiral propagator (`w_propagation_step_chiral`) for the W/Z/gluon sectors too, so one propagator serves everything?

## Answer

**No.** The even law is not a stylistic choice that can be applied everywhere — F68 *derives* it, and the derivation only fires in one channel. The propagator law is selected, per sector, by a single criterion:

> A gauge field rides the **even/paired** law iff its minimal-coupling operator **commutes** with the Weyl unitary $U^\pm(k)=u\mathbf I-i(\mathbf n\!\cdot\!\boldsymbol\sigma)$ (the identity/singlet channel — helicity-blind). If the coupling lives in the **σ-vector channel** (does *not* commute), the two Riemann–Silberstein helicities carry distinct rates $\Omega^+\neq\Omega^-$ and the **chiral** propagator is the faithful one. Forcing the even law there is the sourceless $\Delta\Omega/2$ override of F67 §S3 — an imposition, not a derivation.

The photon goes even because U(1) minimal coupling is a c-number phase $e^{i\theta}\mathbf I$ (F68). The W and the **as-built** gluon are σ-vector bilinears $\phi^\dagger\tau^a\sigma^i\psi$ / $\phi^\dagger T^a\sigma^i\psi$ (F29/F43); $\sigma^i$ does not commute with $\mathbf n\!\cdot\!\boldsymbol\sigma$, so the chiral law is faithful and the even law would discard real content. They are also **not under the GRB/AGN polarimetry bound** (massive / confined → no astrophysical birefringence baseline), so the observation that forced the photon to even has no analog that forces — or even motivates — the swap for them.

## What the test shows (4/4)

| # | Check | Result | Tier |
|---|---|---|---|
| C1 | U(1)$_\text{EM}$ coupling $e^{i\theta}\mathbf I$ commutes with $U^\pm(k)$ → even **forced** | $\max\lVert[\,\cdot\,]\rVert=1.8\times10^{-16}$ (4000 $k$×2 branches) | machine |
| C2 | σ-vector channel (W & gluon bilinear): $\lVert[\sigma^i,\mathbf n\!\cdot\!\boldsymbol\sigma]\rVert\neq0$ → chiral faithful | $\min=1.6\times10^{-3}$ (generically $O(1)$; only →0 at measure-zero $k$) | structural |
| C3 | The branch split $\Delta\Omega=\Omega^+-\Omega^-$ the even law discards is **pure $O(k^2)$** | linear coef $a_1=-2.4\times10^{-5}\approx0$; quad coef $a_2=-0.0640\neq0$; $\Delta\Omega/k\big\|_{k\to0}=-6.4\times10^{-5}$ | quantitative |
| C4 | Forcing even on the real W field erases its branch content | chiral $S=\phi_++\phi_-=+0.07924=-\Delta\Omega N$; even/paired $S=-1.8\times10^{-15}\approx0$ | machine |

C3 confirms the two laws share the linear (speed-of-light, $c=1/\sqrt3$) term exactly; they differ **only** in the $O(k^2)$ term — i.e. the quantity the even law throws away is precisely the vacuum birefringence. C4's chiral value $+0.07924$ reproduces the F67 S1 / F69 PP2 number bit-for-bit (independent consistency cross-check). For the W that discarded $S$ carries the helicity asymmetry tied to its maximal parity violation, so the even law is not a free swap there.

## Current code map (already self-consistent)

| Sector | Propagator | Channel |
|---|---|---|
| photon (`ca_photon_pair.photon_step_spectral`) | **even** `_f26_rotation_step` (F69) | identity / vector |
| Z (`ca_z_field.z_propagation_step_spectral`) | **even** `_f26_rotation_step` | mixing eigenstate inherits A's even law |
| hypercharge B (`ca_wmu.hypercharge_propagation_step`) | **even** `_f26_rotation_step` | U(1)$_Y$ identity |
| W (`ca_wmu.w_propagation_step_chiral`) | **chiral** $\Omega^\pm$ (F37) | σ-vector, parity-violating |
| gluon (`ca_gluon.gluon_rotation_step_spectral_bcc`) | **chiral** (reuses W step, F43) | σ-vector (as built) |

The split is not arbitrary: every field that couples through the **identity** channel (photon, Z, B) already rides the even law; every field built as a **σ-vector** bilinear (W, gluon) rides the chiral law. No change is warranted, and unifying everything onto the even law would silently apply the F67 §S3 sourceless override to the σ-vector sectors.

## The one genuine open lead (gluon parity)

Unlike the W, **QCD conserves parity** — the gluon couples *vectorially* ($\bar q\gamma^\mu T^a q$), and the colour generators $T^a$ act on the colour factor, **outside** the helicity ($\sigma$) space, so $[T^a\otimes\mathbf I_\sigma,\;\mathbf I_c\otimes\mathbf n\!\cdot\!\boldsymbol\sigma]=0$. That makes the physical gluon a *candidate* identity-channel (even-law) object — but only after re-deriving it that way. In this model the gluon was **built** as a σ-vector bilinear (F43, port of F29), which places it in the chiral channel by construction. So migrating the gluon to the even/paired law is **not** granted by the F69 argument; it would require an SU(3) analog of the F68 minimal-coupling derivation (plausible, since colour commutes with $\mathbf n\!\cdot\!\boldsymbol\sigma$) plus re-expressing $G^{a,i}$ off the σ-vector bilinear. That is a real research item, flagged here, not a blanket retirement. The W, by contrast, is closed: its parity violation **is** the branch split, so it must stay chiral.

## Verdict

The paired/even-law photon (F69) is the right object for the **electromagnetic** photon and is already shared by the Z and hypercharge B. It cannot be made universal: the chiral propagator stays for the W (forced — parity violation) and for the gluon **as currently constructed** (σ-vector bilinear; an even-law gluon is a possible future re-derivation, not a swap). This confirms and sharpens F69's "what was kept" note with a quantitative selection criterion.

## Exact vs numeric

| Result | Tier | Residual |
|---|---|---|
| $[e^{i\theta}\mathbf I,U^\pm]=0$ (even forced for U(1)) | machine | $1.8\times10^{-16}$ |
| $[\sigma^i,\mathbf n\!\cdot\!\boldsymbol\sigma]\neq0$ (chiral faithful for σ-vector) | structural | min $1.6\times10^{-3}$ |
| $\Delta\Omega$ linear coef $a_1\approx0$ (no speed split) | quantitative | $2.4\times10^{-5}$ |
| W chiral $S=-\Delta\Omega N$ kept / even $S=0$ | machine | $1.8\times10^{-15}$ |

## Files
- Test: `model-tests/test_F72_universal_even_propagator.py`
- Results: `test-results/F72_universal_even_propagator.json`
- Operators: `ca-simulation/ca_wmu.py` (`_f26_rotation_step`, `w_propagation_step_chiral`), `ca_bcc.py` (`_bcc_uvec`, `bcc_dispersion`), `ca_photon_pair.py` (`build_pair_mode`, `photon_step_spectral`, `pair_birefringence`).
