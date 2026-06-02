# F67 — Option 1 tested: the chirality-even photon kills birefringence, but the even photon and the two-branch Weyl bilinear are mutually exclusive

**Date:** 2026-06-01 - 14:23
**Status:** Confirmed — 3/3 sections PASS against the model's *real* propagators (residuals 1.8×10⁻¹⁵ / 7.7×10⁻⁶ FD / 1.4×10⁻¹⁷). The wedge between the two photons is, exactly, the excluded birefringence.
**Script:** `model-tests/test_F67_option1_even_law_photon.py` (imports `ca_wmu._f26_rotation_step`, `ca_wmu.w_propagation_step_chiral`, `ca_bcc`; no propagator re-derivation).
**Results:** `test-results/F67_option1_even_law_photon.json`
**Cross-references:** [[F66-allsky-birefringence-anisotropy-no-rescue]] (this tests its option 1), [[F65-helicity-chirality-map-confirmed]] (birefringence is forced for the bilinear), [[F39-two-helicity-photon-bilinear]] (the bilinear; §5.1 non-unification flag), [[F29-w-triplet-bilinear-su2-bridge]] (what the bilinear buys), [[F26-speed-of-light-as-rotation-rate]], [[F64-em-connection-gravity]] (the cell size under threat).

---

## The question

F66 closed the anisotropy escape and left **option 1** as the highest-value survivor: build the physical U(1) photon so that *both* helicities ride the chirality-even dispersion $\Omega_\text{even}=\tfrac12(\Omega^++\Omega^-)$, so the F30/F65 linear birefringence vanishes and the F64 Planck-scale cell survives. The open worry (F39 §5.1) was that the model's *composite* photon (a bilinear of the two BCC Weyl branches) and the U(1) *gauge* photon are not unified — and the user's sharper framing: **the bilinear photon and the gauge photon cannot both exist at once.** F67 tests exactly that.

The model already ships both propagators, so this is a confrontation with real code, not a thought experiment:

- `ca_wmu.w_propagation_step_chiral` — the photon's propagator since F37. $F^\pm=E\pm iB$ rotate at their own branches $\Omega^\pm$. This *is* the honest two-branch Weyl bilinear (F39). Birefringent.
- `ca_wmu._f26_rotation_step` — the **even** law $R(\Omega_\text{even})$ on $(E,B)$. Non-birefringent. Already used for the massive W and the Z (`ca_z_field`).

"Option 1" = run the U(1) photon under `_f26_rotation_step` instead.

## What the test shows (3/3)

**S1 — The even law removes birefringence exactly. [resid 1.8×10⁻¹⁵]**
A real, linearly polarized body-diagonal mode (both helicities populated) is propagated $N{=}6$ ticks under each law; the birefringence observable is $S\equiv\phi_++\phi_-$ (twice the polarization-plane rotation).
- Chiral: $S_\text{meas}=+0.07924$ vs predicted $-\Delta\Omega\,N=+0.07924$ (resid $1.8\times10^{-15}$) → **birefringent**, as F65 forced.
- Even: $S_\text{meas}=-1.8\times10^{-15}\approx0$ → **no birefringence.**

**S2 — The even-law field is still a legitimate photon.**
- Group velocity $d\Omega_\text{even}/d|k|\to 0.5773497$ vs $1/\sqrt3=0.5773503$ (max dir. err $7.7\times10^{-6}$, finite-difference limited): the **speed of light is preserved**. The birefringence lives entirely in the $O(k^2)$ term; the linear (speed) term is common to $\Omega^+,\Omega^-,\Omega_\text{even}$.
- Real field preserved ($\max|\text{Im}|=9\times10^{-16}$ over 50 steps) and field-space norm conserved (drift $7.7\times10^{-15}$): the even step is a clean unitary rotation on real $(E,B)$.

**S3 — The even photon has no two-branch Weyl bilinear representation. [resid 1.4×10⁻¹⁷] (the cost)**
Converting the bilinear (chiral) photon into the even photon requires a forced phase on *each* helicity:

$$\delta_+=(-\Omega_\text{even})-(-\Omega^+)=\tfrac{\Omega^+-\Omega^-}{2}=+\tfrac{\Delta\Omega}{2},\qquad \delta_-=(\Omega_\text{even})-(\Omega^-)=+\tfrac{\Delta\Omega}{2},$$

i.e. **both helicities must be force-rotated by $+\Delta\Omega/2$** — verified equal to $\Delta\Omega/2$ to $1.4\times10^{-17}$. Along the body diagonal this override is $\tfrac12|\Delta\Omega|=(\sqrt3/54)\,k^2$ (confirmed: measured $5.137\times10^{-3}$ vs closed $5.132\times10^{-3}$). Crucially, the spinor inputs that build the photon bilinear sit at $k/2$ and carry the **branch** phases $\omega_+(k/2)=0.12743$ and $\omega_-(k/2)=0.13404$; the even law demands $0.13073$ of *each*. Neither branch supplies it — gap $3.3\times10^{-3}\neq0$. The override $\Delta\Omega/2$ is therefore a phase with **no single-Weyl-branch source**.

## Verdict

**Option 1 works as advertised, and it is exactly as expensive as the user suspected.** The even-law photon is a perfectly good photon (right speed, real, unitary, non-birefringent) — but it is *not* the F39 composite bilinear. The two constructions are separated by precisely $\Delta\Omega/2$ per helicity, which is half the birefringence that F65/F66 must remove. Since each BCC Weyl branch rigidly carries its own $\omega^\pm$, that override has no spinor provenance: you cannot assemble an $\Omega_\text{even}$ photon out of the two Weyl branches. Hence

> **the two-branch Weyl bilinear photon (birefringent) and the chirality-even gauge photon (non-birefringent) are mutually exclusive.** Choosing non-birefringence (saving the F64 cell) means the U(1) photon is a *primitive* gauge field with its own even-law propagator — abandoning the composite "photon = bilinear of the two Weyl branches" picture.

This is no longer the soft non-unification flag of F39 §5.1; it is a forced either/or, and the quantity that forbids having both is the same number the polarimetry bound forbids being nonzero.

## What this costs, concretely

The bilinear is not decoration — it is what gives:
- the **SU(2) W-triplet bridge** (F29): $W^{a}$ built as $\phi^\dagger\tau^a\sigma^i\psi$ from the same Weyl content, i.e. the photon and the weak triplet sharing one construction;
- the F64 claim that **gravity is made of the same $(E,B)$ rotation** as light and mass (F26), since the dielectric renormalizes the bilinear's rotation.

An even-law U(1) photon keeps the *kinematics* (speed, reality, two transverse polarizations) but forfeits this shared-substance bookkeeping for the photon specifically. The W/Z already run on `_f26_rotation_step`, so the even photon is *consistent* with the massive sector; what it severs is the photon↔Weyl-bilinear identity, not the gauge structure.

## Where this leaves the three F66 options

1. **Even-law photon (this finding):** saves F64's cell and birefringence, costs the composite-photon identity. Internally consistent and now fully characterized. The honest cost is structural, not empirical.
2. **Sub-Planck cell:** still closed — $\eta\propto a$, and the F64 G-match pins $a\propto\sqrt{g_*}$, so $a\lesssim10^{-14}\ell_P$ needs $g_*\sim10^{-29}$ (impossible) unless gravity is re-sourced.
3. **Genuine falsification of the rotation-photon construction:** avoided only by adopting (1).

## Open / next

- **Is the even law *forced* on the gauge photon, or merely *available*?** S3 shows it is available and is the only non-birefringent choice, but does not derive it from minimal coupling. The decisive follow-up is whether the photon minimally coupled in `ca_dirac` (the covariant-derivative $A_\mu$) is structurally the even-law object independent of the bilinear — if so, option 1 is *derived*, not chosen.
- **Reconcile with F29:** if the U(1) photon is even-law and primitive, does the W-triplet bridge still stand on the bilinear alone, or does the whole electroweak multiplet need re-expressing? This is the real content behind F39 §5.1 now that the photon has split off.

## Exact vs numeric

| Result | Tier | Residual |
|---|---|---|
| chiral $S=-\Delta\Omega\,N$ (birefringent) | machine | $1.8\times10^{-15}$ |
| even $S=0$ (no birefringence) | machine | $1.8\times10^{-15}$ |
| even-law group velocity $=1/\sqrt3$ | quantitative (FD) | $7.7\times10^{-6}$ |
| even step real + norm-conserving | machine | $9\times10^{-16}$ / $7.7\times10^{-15}$ |
| override $=\Delta\Omega/2$ on both helicities | machine | $1.4\times10^{-17}$ |
| body-diag override $=(\sqrt3/54)k^2$ | quantitative | $5\times10^{-6}$ |

## Files
- Test: `model-tests/test_F67_option1_even_law_photon.py`
- Results: `test-results/F67_option1_even_law_photon.json`
- Builds on `ca-simulation/ca_wmu.py` (`_f26_rotation_step`, `w_propagation_step_chiral`), `ca_bcc.py` (`bcc_dispersion`, `bcc_unitary`).
