# F34b — W_μ Phase 5B: Stueckelberg W-Boson Mass Generation

**Date:** 2026-05-24  
**Status:** Confirmed — 5/5 tests PASS  
**Module:** `ca-simulation/ca_wmu.py`  
**Tests:** `model-tests/test_wmu_phase5_stueckelberg.py` (W5.1–W5.5)  
**Results:** `test-results/wmu_phase5_stueckelberg.json`  
**Roadmap:** `roadmap-wmu-implementation.md` Phase 5B

---

## Summary

Phase 5B generates a W-boson mass via the Stueckelberg/nonlinear-sigma mechanism. A scalar SU(2) field $U_\text{st}(x) \in \mathrm{SU}(2)$ is promoted to a dynamical degree of freedom; its kinetic energy $\mathrm{tr}[(\partial_\mu U_\text{st})^\dagger(\partial_\mu U_\text{st})]$ acts as the mass term. All five tests pass, confirming both the mass-generation mechanism and the longitudinal degree of freedom (the Goldstone mode eaten by the W).

---

## Key Results

| Test | Description | Residual | Target | Status |
|------|-------------|----------|--------|--------|
| W5.1 | Identity $U_\text{st}$ → $m_W = 0$; random → $m_W > 0$ | $0.0$ (id); $m_W=3.161$ (rand) | structural | ✓ PASS |
| W5.2 | Link unitarity preserved after 10 mass steps | $1.776 \times 10^{-15}$ | $\le 10^{-13}$ | ✓ PASS |
| W5.3 | $m_W$ invariant under constant SU(2) rotation of $U_\text{st}$ | $0.0$ | $\le 10^{-14}$ | ✓ PASS |
| W5.4 | Gradient flow damps kinetic energy of $U_\text{st}$ | $E_\text{kin}$ decreases | structural | ✓ PASS |
| W5.5 | All 3 SU(2) components of mass_field non-zero | $\|F^1\|=0.97, \|F^2\|=0.98, \|F^3\|=0.98$ | all $> 10^{-6}$ | ✓ PASS |

---

## Mass Generation Mechanism

The Stueckelberg kinetic term is:

$$\mathcal{L}_\text{mass} = \frac{f^2}{2}\,\mathrm{tr}\bigl[(\partial_\mu U_\text{st})^\dagger(\partial_\mu U_\text{st})\bigr]$$

In Fourier space this becomes:

$$\mathcal{L}_\text{mass} = \frac{f^2}{2}\sum_k (k_x^2+k_y^2+k_z^2)\bigl(|\hat{U}^a_k|^2 + |\hat{U}^b_k|^2\bigr)$$

where $(a,b)$ are the Cayley–Klein components of $U_\text{st}$. The W mass is:

$$m_W = g \cdot f, \qquad f = \sqrt{\langle|\partial_\mu U_\text{st}|^2\rangle}$$

---

## W5.3 — Exact Gauge Invariance of $m_W$

For a constant (spatially uniform) $V \in \mathrm{SU}(2)$:

$$U_\text{st}(x) \to V \cdot U_\text{st}(x) \implies \partial_\mu(V U_\text{st}) = V\,\partial_\mu U_\text{st}$$

Therefore:

$$\mathrm{tr}[(\partial_\mu(VU_\text{st}))^\dagger(\partial_\mu(VU_\text{st}))] = \mathrm{tr}[(V\,\partial_\mu U_\text{st})^\dagger(V\,\partial_\mu U_\text{st})] = \mathrm{tr}[(\partial_\mu U_\text{st})^\dagger V^\dagger V\,\partial_\mu U_\text{st}] = \mathrm{tr}[(\partial_\mu U_\text{st})^\dagger(\partial_\mu U_\text{st})]$$

using $V^\dagger V = I$. Thus $m_W$ is exactly gauge-invariant under left-multiplication by a constant SU(2) matrix. Residual: $0.0$ (bit-for-bit).

---

## W5.4 — Gradient Flow (Heat Kernel)

The evolution step applies a heat-kernel gradient flow to $U_\text{st}$:

$$\hat{U}_\text{st,new}(k) = e^{-dt(k_x^2+k_y^2+k_z^2)}\,\hat{U}_\text{st}(k)$$

Since $-(k^2) \le 0$ for all $k$, every Fourier mode is multiplied by $e^{-dt\,k^2} \le 1$. The spectral kinetic energy $\sum_k k^2|\hat{U}|^2$ therefore decreases monotonically with each flow step (before re-unitarisation). After re-unitarisation the decrease may be partial, but the net kinetic energy after $N$ steps is bounded by the initial value.

Measured: $E_\text{kin}: 2.681\times10^6 \to 5.503\times10^5$ after 5 steps with $dt=0.1$ — a 79.5% reduction.

---

## W5.5 — Longitudinal Degree of Freedom

In the massless theory ($U_\text{st} = I$), only two transverse polarisations propagate. After Stueckelberg mass generation, the $U_\text{st}$ field's three SU(2) generators supply three scalar components $F^a$ ($a=1,2,3$), all non-zero for a generic configuration. This confirms the longitudinal degree of freedom is present in the mass field — the Goldstone mode has been "eaten."

For the identity $U_\text{st}$: $\mathrm{mass\_field} = 0$ exactly. For random $U_\text{st}$: all three components satisfy $\max_x|F^a(x)| > 1$.

---

## Connection to Ludwig's Derivation

The promotion of the SU(2) mass link $U_m(x)$ (F27) to a dynamical field is the Stueckelberg interpretation: the mass link *is* the longitudinal Goldstone boson of $SU(2)_L$ symmetry breaking. The kinetic term for $U_\text{st}$ corresponds to the $f^2$ term in the nonlinear sigma model, with $f$ playing the role of the Higgs vacuum expectation value in the mass relation $m_W = gf/2$.

---

## Files

- `ca-simulation/ca_wmu.py` — `make_stueckelberg_field`, `stueckelberg_mass_term`, `wmu_mass_stueckelberg`
- `model-tests/test_wmu_phase5_stueckelberg.py` — W5.1–W5.5
- `test-results/wmu_phase5_stueckelberg.json` — numerical results
