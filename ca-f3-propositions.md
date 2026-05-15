# Phase F3 — Propositions for a Conserving Yukawa Back-Reaction

*Drafted 2026-05-14. Companion to `ca-unified-proposition.md`. Does not modify code; lists candidate fixes for the open F3 problem so the next implementation step can choose one.*

---

## What F3 actually does today

Current implementation in `run_phaseF_tests.py::test_F3`:

```
for each step:
    psi_bar_psi = 2·Re( η_u*·χ_u + η_d*·χ_d )       # scalar density at each cell
    state.Pi    -= 0.5·dt·y·psi_bar_psi              # hand-coded Yukawa kick (half-step)
    state        = un.unified_step(...)              # Strang Φ-Dirac sub-step
    state.Pi    -= 0.5·dt·y·psi_bar_psi              # second half-step
```

The fermion → Φ feedback is bolted on outside the symplectic integrator. The hand kick `Π −= dt·y·ψ̄ψ` is the right *direction* (it is the Euler–Lagrange source term `□Φ = −∂V/∂Φ − y·ψ̄ψ`) but it is **not** derived from a single Hamiltonian that includes both the Φ and the fermion kinetic terms, so:

1. **Total energy is not conserved.** The kick borrows energy from "nowhere" — the Dirac side never pays for the Φ depression. Long runs eventually diverge (the test catches this with the `> 100.0` early-stop guard).
2. **The Yukawa source uses ψ̄ψ frozen from before the Φ half-step.** The two outer half-kicks reuse the same `psi_bar_psi`, so the Strang structure is not symmetric in `(Φ, ψ̄ψ)`.
3. **The fermion mass term is `m(x) = y·|Φ(x)|`, not `y·Re(Φ)·γ⁰·...`.** Taking `|Φ|` instead of the proper bilinear `Φ + Φ†` (or Re Φ in real-Φ approximation) means the fermion side is responding to `|Φ|`, while the scalar side is being fed by `ψ̄ψ` — the two are not conjugate variables of the same Lagrangian. The vacuum-regression contract (F1) still passes because at `Φ = v`, `|Φ| = Re Φ = v`, but off-vacuum the two diverge.

Pages 26–28 of the original notebook flagged a related issue with Sachs' tetrad derivation; this proposition routes around it but does not resolve it.

---

## Propositions (ranked by cost vs. payoff)

### P1 — Symplectic Yukawa via a joint Hamiltonian (recommended)

Treat `(Φ, Π)` and the fermion 4-spinor `Ψ = (η, χ)` as conjugate coordinates of a single Hamiltonian:

$$H = \tfrac12\sum_x |\Pi|^2 + \tfrac12|\nabla\Phi|^2 + V(|\Phi|^2) + \Psi^\dagger H_D(\Phi)\,\Psi$$

with `H_D(Φ) = c·α·k + y·Re(Φ)·β` (real-scalar reduction first; complex-scalar later). The interaction term `y·Re(Φ)·Ψ̄Ψ` is now a single object that contributes both:

- a force on `Π`: `−∂H/∂Φ_R = −y·Ψ̄Ψ`
- a force on `Ψ`: `−i·∂H/∂Ψ† = −i·y·Re(Φ)·β·Ψ`

Implement as a **three-piece symplectic split**:

```
A_step(dt/2):   Φ-kinetic + V'(|Φ|)         # existing kg_step_strang
B_step(dt/2):   Π −= dt·y·Ψ̄Ψ                # uses current Ψ
C_step(dt):     Dirac kinetic + mass=y·Re(Φ) # existing dirac_step_2d_varm_splitstep
B_step(dt/2):   Π −= dt·y·Ψ̄Ψ                # uses post-Dirac Ψ
A_step(dt/2):   Φ-kinetic + V'(|Φ|)
```

This is the same Strang pattern already used everywhere else in the codebase. Energy is conserved to `O(dt²)`. **Cost:** ~30 lines of code; reuses `dirac_step_2d_varm_splitstep` and `kg_step_strang` unchanged.

**Validation:** add `test_F3a` that runs 1000 steps and checks `|H(t) − H(0)| / H(0) < 1e-3` (symplectic-integrator drift is bounded, not zero, but stays inside an `O(dt²)` envelope).

### P2 — Make the Yukawa coupling complex-bilinear from day one

Change `m_eff(x) = y·|Φ(x)|` to the standard Yukawa form:

$$\mathcal{L}_Y = -y\,(\Phi\,\bar\Psi_L\Psi_R + \Phi^*\,\bar\Psi_R\Psi_L)$$

In the Weyl basis this couples `η ↔ χ` via two terms:

- mass on `(η→χ)`: `y·Φ`
- mass on `(χ→η)`: `y·Φ*`

The existing `dirac_step_2d_varm_splitstep` takes a *real* `m_field`. To support complex `m`, the `_mix_eta_chi` per-cell rotation has to become `exp(−i·β·(m_R·1 + i·m_I·γ⁵)·c²·dt)` — still a 2×2 unitary per cell, still exact. **Cost:** rewrite `_mix_eta_chi` to take `m_R, m_I` separately (~20 lines). After this change, `F1` regression still passes (at `Φ = v` real, `m_I = 0`); `F2` is unchanged; `F3` and `F4` now have the *correct* coupling structure to compare with the Standard Model.

Pairs naturally with P1 — the complex bilinear is what plugs into the joint Hamiltonian in P1.

### P3 — Cayley/Padé for the variable-`c` kinetic step (the bottleneck)

This is the engineering item flagged in `ca-unified-proposition.md` line 159. F3 *currently* uses fixed `c = 0.5` (no metric coupling). The full F3 demonstration ("wave packet refracts toward fermion density") requires switching the kinetic step from FFT to a position-space Cayley step:

$$U_\text{kin}(\Delta t) = \left(I + \tfrac{i\Delta t}{2}c(x)\,\alpha\cdot \nabla\right)^{-1}\left(I − \tfrac{i\Delta t}{2}c(x)\,\alpha\cdot\nabla\right)$$

This is **exactly unitary** even with position-dependent `c(x)`, but requires a sparse linear solve per step (banded matrix, ~5L² nonzeros on a 2D L×L lattice). For 64×64 this is ~5 ms per step with `scipy.sparse.linalg.spsolve` — acceptable. **Cost:** 3–5 days as flagged in the proposition; the time-consuming part is correctness testing against the FFT propagator at constant `c`.

Alternative: **higher-order Trotter splitting** (Yoshida 4th-order, McLachlan SS6). Cheaper to implement (~1 day) but only reduces drift, doesn't eliminate it.

### P4 — Drop |Φ| and use Re(Φ) for the Yukawa coupling

Smallest possible change: replace

```python
m_eff = yukawa * np.abs(state.Phi)
```

with

```python
m_eff_R = yukawa * state.Phi.real
m_eff_I = yukawa * state.Phi.imag
```

and (per P2) use both. Reasoning: `|Φ|` is non-analytic in Φ at the origin — fine when `Φ = v + small`, but during F4 (symmetry-restored, `Φ ≈ 0`) the derivative `∂|Φ|/∂Φ` blows up and the Yukawa source `−y·ψ̄ψ` does not match the variational derivative of `m_eff·ψ̄ψ`. Using `Re(Φ)` makes both sides analytic everywhere and the proposition becomes a strict instance of the Standard Model Yukawa term.

This is P2 by another name; called out separately so the minimal version can be tried first.

### P5 — Stronger short-term workaround: backreaction with a damping term

If P1–P3 are too expensive, the *informational* F3 sketch can be stabilised by adding a small viscous damping to `Π`:

```python
state.Pi *= (1.0 - gamma * dt)   # γ ≪ 1
```

This is non-symplectic (it dissipates energy) but bounds the runaway. **Use only as a diagnostic** — it cannot be used in any test that claims a physics result. Existing F3 status (sketch, informational) would be honest with `γ ≈ 0.01`.

---

## Recommended sequencing

| # | Step | Cost | Test added |
|---|---|---|---|
| 1 | P4 — switch `\|Φ\|` to `Re(Φ)` + `Im(Φ)` everywhere | ½ day | F1 regression unchanged; F4 cleaner |
| 2 | P2 — promote `_mix_eta_chi` to complex mass | ½ day | F1, F4 regression |
| 3 | P1 — joint Hamiltonian split (symplectic Yukawa) | 1 day | new F3a: ΔH/H < 1e-3 over 1000 steps |
| 4 | P3 — Cayley kinetic for variable `c` | 3–5 days | new F3b: probe-packet refraction toward density spike (Newtonian gravity demo) |

Steps 1–3 turn F3 from a sketch into a real, energy-conserving demonstration. Step 4 is the gravity demo and is the single biggest remaining engineering item in the whole proposition.

---

## What this proposition does *not* fix

- **Renormalization.** Lattice cutoff issues persist; the continuum limit is open.
- **Yang–Mills self-coupling for W.** Still deferred (proposition lines 161, 190).
- **Tetrad / spin-connection compatibility.** Page 26 disagreement is routed around, not resolved (proposition line 165). A full curved-space implementation would need to revisit this.

---

## Cross-references

- `ca-unified-proposition.md` — original unification proposition; lines 147 (F3 spec), 159 (variable-c bottleneck), 189 (F3 sequencing).
- `run_phaseF_tests.py::test_F3` — current sketch implementation.
- `ca_unified.py::unified_step` — Strang Φ–Dirac composition. P1 modifies this.
- `ca_dirac.py::dirac_step_2d_varm_splitstep`, `_mix_eta_chi` — P2 modifies these.
- `ca_curved.py` — current variable-c stepper; P3 replaces its kinetic step.
