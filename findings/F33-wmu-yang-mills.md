# F33 — W_μ Phase 3: Yang–Mills Self-Coupling on the BCC Lattice

**Date:** 2026-05-24  
**Status:** Confirmed — 5/5 tests PASS  
**Module:** `ca-simulation/ca_wmu.py`  
**Tests:** `model-tests/test_wmu_phase3.py` (W3.1–W3.5)  
**Results:** `test-results/wmu_phase3.json`  
**Roadmap:** `roadmap-wmu-implementation.md` Phase 3

---

## Summary

Phase 3 promotes $W_\mu$ from a background gauge field (Phases 1–2) to a dynamical field that updates itself through the non-Abelian SU(2) Wilson plaquette action. The field-strength tensor $F^a_{\mu\nu}$ is computed from composite BCC link products; the self-coupling step preserves all unitarity and gauge-invariance contracts. All five correctness tests pass.

---

## Key Results

| Test | Description | Residual | Target | Status |
|------|-------------|----------|--------|--------|
| W3.1 | Identity links → F = 0 exactly | $0.0$ | exact | ✓ PASS |
| W3.2 | Plaquette ≠ I for random links (non-trivial F) | structural | structural | ✓ PASS |
| W3.3 | ‖F‖² gauge-invariant under constant SU(2) rotation | $5.93 \times 10^{-16}$ | $\le 10^{-14}$ | ✓ PASS |
| W3.4 | Link unitarity preserved after self-coupling steps | $\le 10^{-13}$ | $\le 10^{-13}$ | ✓ PASS |
| W3.5 | Yang–Mills action decreases under gradient flow | structural | structural | ✓ PASS |

---

## Field Strength Construction

The SU(2) field strength is extracted from the Wilson plaquette. For the $(\mu,\nu)$ plane at site $x$:

$$U_\square(x) = U_\mu(x)\,U_\nu(x+\hat\mu)\,U_\mu^\dagger(x+\hat\nu)\,U_\nu^\dagger(x)$$

$$F^a_{\mu\nu}(x) = -\tfrac{i}{2}\,\mathrm{tr}\bigl[\tau^a\,(U_\square(x) - U_\square^\dagger(x))\bigr]$$

On the BCC lattice the composite links are assembled from the four-directional BCC hop structure; the three independent plaquettes per site yield the triplet $F^a$ for $a \in \{1,2,3\}$.

### W3.1 — Identity vacuum is exact

For $U_\mu(x) = I$ everywhere, $U_\square = I\cdot I\cdot I\cdot I = I$, so $U_\square - U_\square^\dagger = 0$ exactly in floating point. Residual: $0.0$ (bit-for-bit).

### W3.3 — Gauge invariance of ‖F‖²

Under a constant (spatially uniform) SU(2) rotation $V$:

$$U_\mu(x) \to V U_\mu(x) V^\dagger \implies U_\square \to V U_\square V^\dagger$$

$$F^a \to R^{ab}(V) F^b \quad (\text{adjoint representation})$$

$$\|F\|^2 = \sum_{a,\mu\nu} \|F^a_{\mu\nu}\|^2 \to \sum_{a,\mu\nu} \|R^{ab} F^b_{\mu\nu}\|^2 = \|F\|^2$$

since $R(V) \in \mathrm{SO}(3)$ is orthogonal. Residual: $5.93\times 10^{-16}$ (machine $\varepsilon$ — consistent with four successive SU(2) multiplications and one adjoint trace).

### W3.4 — Link unitarity is preserved exactly

The self-coupling update applies an SU(2) element $e^{i\epsilon F}$ (constructed via the $(a,b)$ Cayley–Klein representation) to each link. Since the product of SU(2) matrices is SU(2), unitarity is preserved to floating-point round-off. Residual: $\le 10^{-13}$ after multiple update steps.

---

## Non-Abelian vs Abelian distinction

The critical new feature versus Phase 2 (Abelian free propagation) is the **commutator term** in the covariant field strength:

$$F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + g[A_\mu, A_\nu]$$

On the lattice this commutator is captured automatically by the plaquette product — $U_\mu U_\nu \ne U_\nu U_\mu$ in SU(2). Test W3.2 verifies that $F \ne 0$ for random links (i.e. the computation is non-trivial and not reduced to the Abelian case by accident).

---

## Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| F29 — W-triplet bilinear | F33 extends from kinematic bilinears to dynamical plaquette field strength |
| F32 — Phase 2 free W propagation | Self-coupling in F33 breaks the abelian decoupling of W2.4 for $g \ne 0$ |
| F27 — Chiral SU(2) fermion coupling | Phase 4 (F34) wires the dynamical W field from F33 into the fermion vertex |

---

## Files

- `ca-simulation/ca_wmu.py` — `wilson_plaquette_field_strength`, `yang_mills_self_coupling_step`, `link_unitarity_residual`
- `model-tests/test_wmu_phase3.py` — W3.1–W3.5
- `test-results/wmu_phase3.json` — numerical results
