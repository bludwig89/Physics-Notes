# F32 — W_μ Phase 2: Free W Propagation — F26 Rotation Law per Isospin Component

**Date:** 2026-05-24  
**Status:** Confirmed — 4/4 tests PASS  
**Module:** `ca-simulation/ca_wmu.py`  
**Tests:** `model-tests/test_wmu_phase2.py` (W2.1–W2.4)  
**Results:** `test-results/wmu_phase2.json`  
**Roadmap:** `roadmap-wmu-implementation.md` Phase 2

---

## Summary

Phase 2 establishes that the free W boson field propagates exactly as a triplet of decoupled photons, each obeying the F26 rotation law with a **symmetrized (even) dispersion**.  All four correctness tests pass at machine precision.

---

## Key Results

| Test | Description | Residual | Target | Status |
|------|-------------|----------|--------|--------|
| W2.1 | Ω_W(k) = ω_+(k/2)+ω_-(k/2) for all 3 a-components | $9.6 \times 10^{-13}$ | $\le 10^{-10}$ | ✓ PASS |
| W2.2 | ‖E^a‖²+‖B^a‖² conserved per a / 200 steps | $3.1 \times 10^{-14}$ | $\le 10^{-13}$ | ✓ PASS |
| W2.3 | Transversality residual O(k) (structural) | $2.6 \times 10^{-16}$ | structural | ✓ PASS |
| W2.4 | Superposition + zero-seepage (abelian decoupling) | $0.0$ | $\le 10^{-14}$ | ✓ PASS |

---

## Critical Finding: Even/Symmetrized Dispersion Required for Real W Fields

The BCC dispersion $\omega_+(k)$ is **not** even in $k$:

$$\omega_+(-k) = \omega_-(k) \neq \omega_+(k) \quad (\text{in general})$$

The W gauge potential is a real-valued field, so its Fourier transform has Hermitian symmetry: $\hat{W}(-k) = \hat{W}(k)^*$.  Applying a chirally asymmetric rotation $\Omega = 2\omega_+(k/2)$ breaks this symmetry:

$$R(\Omega(k)) \cdot \hat{W}(k) \implies \widehat{R \cdot W}(-k) \neq [\widehat{R \cdot W}(k)]^*$$

This causes IFFT imaginary parts up to $\sim 0.8$ (not round-off noise) and ~56% energy drift per 200 steps.

**Fix:** Use the symmetrized (even) dispersion:

$$\Omega_\text{even}(k) = \omega_+(k/2) + \omega_-(k/2)$$

which satisfies $\Omega_\text{even}(-k) = \Omega_\text{even}(k)$ exactly, preserving Hermitian symmetry at machine precision.  IFFT imaginary parts are zero; energy drift over 200 steps is $3.1\times10^{-14}$.

**Continuum limit:** both agree: $\Omega_\text{even} \to 2c|k|$ as $|k| \to 0$ (no physical distinction).

---

## W2.1 Measurement Note

The dispersion is measured by comparing the evolved Fourier field against the expected rotated field:

$$\text{residual} = \max_k \frac{|\hat{C}_n(k) - \hat{C}_0(k) e^{-i\Omega_\text{even}(k) n}|}{|\hat{C}_0(k)|}$$

where $\hat{C} = \hat{E} + i\hat{B}$.  This avoids the phase-wrapping artefact of the naive $|\angle(C_n/C_0)|/n$ estimator, which gives $\sim 1.0$ relative error for large-$k$ modes where $\Omega \cdot n_\text{steps}$ wraps many times through $2\pi$.

---

## W2.4 — Abelian Decoupling (Two Sub-tests)

1. **Superposition**: joint evolution of all 3 components equals sum of independent evolutions — residual $0.0$ (exact by construction, confirms no accidental cross-coupling in the loop).
2. **Zero-seepage**: starting with $a=0$ component identically zero, 50 steps of evolution with $a=1,2$ non-zero — $a=0$ remains exactly zero.  Residual $0.0$.

---

## Files

- `ca-simulation/ca_wmu.py` — `_f26_rotation_step` (even dispersion), `w_propagation_step_spectral`, `w_free_dispersion_check`
- `model-tests/test_wmu_phase2.py` — W2.1–W2.4
- `test-results/wmu_phase2.json` — numerical results
