# F31 — W_μ Phase 1: SU(2) Link Variables & Exact Covariant BCC Hopping

**Date:** 2026-05-24  
**Status:** Confirmed — 6/6 tests PASS  
**Module:** `ca-simulation/ca_wmu.py`  
**Tests:** `model-tests/test_wmu_phase1.py` (W1.1–W1.6)  
**Results:** `test-results/wmu_phase1.json`  
**Roadmap:** `roadmap-wmu-implementation.md` Phase 1  
**Closes:** F27 known limitation #1 (kinetic step not SU(2)-invariant without $W_\mu$) — partial; full closure deferred to F34 (Phase 4 fermion vertex).

---

## Summary

Phase 1 introduces $\mathrm{SU}(2)$ link variables $U_\ell \in \mathrm{SU}(2)$ on all 8 BCC nearest-neighbour directions and builds an exact gauge-covariant Weyl step that:

1. Reduces **exactly** to `weyl_step_3d_bcc` when all links are identity (W1.2, W1.6).
2. Conserves the doublet norm to machine precision for any unitary link field (W1.3).
3. Satisfies the local SU(2)$_L$ Ward identity $V(x) \cdot \mathrm{step}(\psi; U) = \mathrm{step}(V\psi; V U V^\dagger)$ at machine precision for constant $V$ (W1.4 residual $1.2 \times 10^{-17}$).
4. Satisfies the F27 mass-step Ward identity exactly (W1.5 residual $7.0 \times 10^{-18}$).

---

## Key Results

| Test | Description | Residual | Target | Status |
|------|-------------|----------|--------|--------|
| W1.1 | Link unitarity $\|a\|^2 + \|b\|^2 = 1$ | $6.7 \times 10^{-16}$ | $\le 10^{-15}$ | ✓ PASS |
| W1.2 | Identity links → standard `weyl_step_3d_bcc` | $0.0$ (exact) | $\le 10^{-15}$ | ✓ PASS |
| W1.3 | Norm conserved / 100 steps, random $U_\ell$ | $1.9 \times 10^{-14}$ | $\le 10^{-13}$ | ✓ PASS |
| W1.4 | Local Ward identity, constant $V$ (k-space exact) | $1.2 \times 10^{-17}$ | $\le 10^{-14}$ | ✓ PASS |
| W1.5 | F27 mass Ward identity, random $V$ | $7.0 \times 10^{-18}$ | $\le 10^{-14}$ | ✓ PASS |
| W1.6 | Exact step: identity links $\equiv$ `weyl_step_3d_bcc` | $9.8 \times 10^{-18}$ | $\le 10^{-14}$ | ✓ PASS |

---

## Architecture: Why Two Covariant Steppers

The BCC QCA unitary decomposes as

$$U_\mathrm{BCC}(\mathbf{k}) = \sum_{d \in \mathrm{BCC}} M_d \cdot e^{i\mathbf{k}\cdot\mathbf{d}/\sqrt{3}}$$

where each $M_d$ is a precomputed $2\times 2$ spin matrix and the phase $e^{i\mathbf{k}\cdot\mathbf{d}/\sqrt{3}}$ is a **fractional** hop of $1/\sqrt{3}$ lattice units per axis. This is **not** an integer nearest-neighbour shift; `np.roll` applies $e^{i\mathbf{k}\cdot\mathbf{d}}$ (integer hop), not $e^{i\mathbf{k}\cdot\mathbf{d}/\sqrt{3}}$.

This forces two design choices:

### `covariant_weyl_step_3d_bcc` (site-average, O(a) Ward identity)
- Re-unitarises the average of 8 link variables into $U_\mathrm{eff}(x)$, then applies the spectral BCC unitary.
- Preserves norm exactly for any unitary $U_\ell$ (W1.3 at $10^{-14}$).
- Ward identity accurate to $O(a \cdot |\nabla V| \cdot L)$ — the same status as $O(a)$-improved fermion actions in lattice QCD.

### `covariant_weyl_step_3d_bcc_exact` (per-link fractional shift, exact Ward identity)
- Uses `bcc_fractional_shift` to apply the $e^{i\mathbf{k}\cdot\mathbf{d}/\sqrt{3}}$ phase per link, then sums over all 8 directions with their $M_d$ spin matrices and $U_\ell$ gauge links.
- Ward identity exact at machine precision for constant $V$ (W1.4 residual $1.2\times 10^{-17}$).
- Norm not conserved for non-identity links (sum of 8 partially-rotated contributions is not unitary unless all $U_\ell = I$).
- ~3.5× slower (36 FFTs vs ~10).

**Usage rule**: use `covariant_weyl_step_3d_bcc` for long dynamics (norm safety); use `covariant_weyl_step_3d_bcc_exact` for Ward-identity certification and structural tests.

---

## Key Algebraic Identity (new, Tier 1)

The $\mathrm{SU}(2)$ link decomposition

$$U_\mathrm{BCC}(\mathbf{k}) = \sum_{d \in \mathrm{BCC}} M_d \cdot e^{i\mathbf{k}\cdot\mathbf{d}/\sqrt{3}}$$

with $M_d$ given by `_spinor_matrix(a, b, c, sign)` is verified to Frobenius norm $< 4 \times 10^{-16}$ over 20 random $k$-points.

---

## Exact Local SU(2)$_L$ Ward Identity (for constant V)

For any constant $V \in \mathrm{SU}(2)$ and any unitary link field $\{U_\ell\}$:

$$V \cdot \mathrm{step}(\psi; U) = \mathrm{step}(V\psi;\; V \cdot U \cdot V^\dagger)$$

where the gauge transform uses fractional k-space shifts matched to the fractional kinetic hops.
Residual: $1.2 \times 10^{-17}$ (machine precision).

---

## Known Limitations (inherited / deferred)

- Full local SU(2)$_L$ Ward identity (spatially-varying $V$) holds to $O(a)$, as in lattice QCD — not exact at finite lattice spacing. This is expected and not a defect.
- $W_\mu$ as a dynamical propagating field enters in Phase 2 (F32).
- Fermion–$W_\mu$ vertex (closing F27 limitation #1 fully) enters in Phase 4 (F34).

---

## Files

- `ca-simulation/ca_wmu.py` — `make_w_link_field`, `link_unitarity_residual`, `covariant_weyl_step_3d_bcc`, `covariant_weyl_step_3d_bcc_exact`, `gauge_transform_links`, `gauge_transform_links_kspace`, `verify_spinor_matrix_decomp`, `_SPINOR_MATS`, `BCC_DIRS`
- `model-tests/test_wmu_phase1.py` — W1.1–W1.6
- `test-results/wmu_phase1.json` — numerical results
