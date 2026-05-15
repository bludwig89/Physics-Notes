# Changelog

Non-trivial software changes and decisions for the Physics Notes simulation work.

## 2026-05-16

### P1 — symplectic Yukawa back-reaction (corrected c² factor)
- **Files:** `ca-simulation/ca_unified.py` (`unified_step` gains `back_react=True` Strang-symmetric half-kicks; new `total_energy` helper); `ca-simulation/run_phaseF_tests.py::test_F3` rewritten to use the symplectic API and a 200-step run with a bounded-energy check.
- **Derivation:** the Yukawa Hamiltonian density is `H_Y = c²·y·(Φ·η†χ + Φ*·χ†η)`. The factor `c²` is essential because the Dirac stepper uses `m·c²·β` for the mass-Hamiltonian — without it, the Π update is too small to balance the Ψ rotation, leaving a constant Strang offset (1.85% drift independent of dt). With `c²` included, Hamilton's equation `δΠ/δt = -∂H_Y/∂Φ* = -c²·y·χ†η` matches the Ψ rotation generator and the symplectic split is exact.
- **Test result:** `max|H − H₀| / |H₀|` over 200 steps with dt=0.5 is **3 ppm** (was 1.85% before the correction). Drift scales as O(dt²) exactly: dt=0.5 → 3.0e-6, dt=0.25 → 7.4e-7, dt=0.125 → 1.8e-7, dt=0.0625 → 4.6e-8 (every factor-2 dt drop reduces drift by 4×).
- **|Φ−v| range** dropped from 0.012–1.247 (old divergent sketch, 30 steps) to 0.66–0.73 (200 steps), confirming the back-reaction stays in a bounded oscillation around vacuum instead of running away. F1/F2/F4 unchanged with the default `back_react=False`.

### P3 — Cayley/Crank–Nicolson exact-unitary variable-c kinetic step
- **Files:** `ca-simulation/ca_curved.py` (added `_build_cayley_matrix_2d`, `CayleyVarcSolver2D`, `weyl_step_2d_varc_cayley`, `method='cayley'` option in `measure_refraction`); `ca-simulation/run_phase_tests.py::test_C1` extended with a Cayley arm; new `test_F3b` Newtonian-gravity demo in `run_phaseF_tests.py`.
- **What:** solves `(I + i·dt/2·H_disc)·ψ_new = (I − i·dt/2·H_disc)·ψ_old` where `H_disc` is the Hermitized variable-c Weyl operator with face-averaged c (`c_face(i+½,j) = (c(i,j)+c(i+1,j))/2`). Sparse 10-nonzero/row matrix; LU-factored once per c-field change via `scipy.sparse.linalg.splu`. Sub-stepping (`n_sub`) inside the solver reduces O(dt²) Crank–Nicolson dispersion without giving up exact unitarity.
- **Norm conservation:** drift 5.5e-15 over 200 steps on variable c (range 0.2–0.6) vs **32.6%** for the existing Strang-split stepper. That's a 6×10¹³ improvement — Cayley is at the complex128 machine-precision floor.
- **C1 refraction:** Cayley measures the right qualitative refraction direction but is 5.4° off the continuum Snell prediction at |k|≈0.5. This is the **lattice dispersion** of centered first-differences (ω(k)=c·sin(k) instead of c·|k|), not a bug. The existing Strang+FFT path avoids it for the c₀ baseline because the FFT propagator gives exact-k dispersion. Closing the gap requires a higher-order spatial stencil — flagged as future work.
- **F3b — gravitational lensing demo:** static |Φ| depression at the lattice centre (sigma=12, depth 0.35); `c(x) = c₀·(|Φ|/v)^α` with α=1.5 so the depression makes c *slower* at the centre (the proposition's published sign `(-α)` is inconsistent with F3's depression direction; the `+α` form is what produces attraction). A Weyl probe packet at impact parameter +18 cells is deflected an extra 6.6 cells **toward** the depression vs the flat-c baseline. Norm drift 1.1e-15.
- **Test totals:** 13/13 phases pass (A1–E2 + F1–F4 + F3b). Full Phase A–E suite still 8/8 unchanged.

## 2026-05-15

### Added structured summary of Ostoma & Trushyk (1999) *Cellular Automata Theory*
- **File:** `ostoma-trushyk-1999-summary.md` (new).
- **Source:** `Cellular Automata Theory.pdf` (108 pages, July 7 1999).
- **Method:** extracted via `pdftotext -layout` to a working text file; structured into 18 sections covering CA postulates, two-layer space-time, Lorentz derivation, quantum vacuum, Quantum Inertia, EMQG, three-mass framework, the EMQG field equations, Fizeau-like photon scattering account of 4D curvature, two CA wavefunction proposals, Milne kinematic cosmology re-read of the Big Bang, and a section mapping the paper's claims onto this project's existing files (`ca-reference.md`, `cellular-automata-research.md`, `ca-forces-integration.md`, `fredkin-correlation.md`).
- **Why:** the paper sits in the same lineage as Fredkin's *Digital Mechanics* (already in the project) and is the most CA-physics-aligned external source in the workspace. Captured the postulates, equations, and falsifiable predictions in math-mode markdown per project conventions.

### P4 — replaced `m_eff = y·|Φ|` with `m_eff = y·Re(Φ)`
- **File:** `ca-simulation/ca_unified.py::unified_step`.
- **Why:** `|Φ|` is non-analytic at Φ=0 (the F4 vacuum). For the F1 vacuum at `Φ = v` real, `Re(Φ) = |Φ| = v`, so F1 regression is preserved at machine precision (`|Φ−v|=1.11e-16`, `max fermion diff=8.41e-16`). For F2/F3 Φ stays close to real so Re(Φ) and |Φ| agree numerically; F2 dispersion residuals unchanged (max 1.06e-3 radial, 4.42e-4 Goldstone); F3 sketch range `max|Φ−v|=6.97e-01` vs 6.95e-01 previously (within sketch noise). F4 unchanged at exact zero.
- **Tests:** `run_phaseF_tests.py` → 4/4 pass.

### P2 — complex Yukawa bilinear
- **Files:** `ca-simulation/ca_dirac.py` (added `_mix_eta_chi_complex` and `dirac_step_2d_varm_complex_splitstep`), `ca-simulation/ca_unified.py::unified_step` (rewired to pass `Re(Φ)` and `Im(Φ)` separately).
- **What:** the Standard-Model Yukawa Lagrangian `L_Y = -y·(Φ·η†χ + Φ*·χ†η)` produces a *complex* mass `M(x) = y·Φ(x)` coupling η→χ with `y·Φ` and χ→η with `y·Φ*`. The new per-cell rotation `exp(-i·c²·dt·[[0, M·I],[M*·I, 0]])` is exactly unitary; eigenvalues are `±|M|·c²·dt` with eigenvectors `(1, ±M*/|M|)/√2`. Handles `|M|=0` via the well-defined limit `sin(θ)/|M| → factor`.
- **Strang structure:** kinetic step at the real baseline `m_0 = mean(m_R)` (existing `dirac_step_2d_splitstep`), per-cell complex δ-rotation for `(M−m_0)`. Reduces exactly to `dirac_step_2d_varm_splitstep` when `m_I ≡ 0` (verified bit-for-bit, `diff = 0.000e+00`).
- **Unit tests added inline (one-shot):**
  1. `m_I=0` reduction → 0.0 difference vs real stepper.
  2. `m_I≠0` norm conservation over 500 steps → drift 6.8e-14.
  3. Sensitivity: toggling `m_I` from 0 to 0.5 changes the output by 8e-2 after one step (proves the code path is exercised).
- **Tests:** Phase F suite 4/4 pass; full Phase A–E suite still 8/8. **Total 12/12.**
- **F1 regression preserved** because vacuum Φ=v is real → m_I≡0 → complex rotation reduces to identity-after-subtraction → kinetic step matches reference Dirac CA at constant `m = y·v` bit-for-bit.

## 2026-05-14

### F3 propositions document
- Added `ca-f3-propositions.md`. Five ranked candidates (P1 symplectic joint Hamiltonian, P2 complex Yukawa bilinear, P3 Cayley/Padé for variable-c, P4 use Re/Im(Φ) instead of |Φ|, P5 viscous damping as diagnostic only).
- Root-cause: the current F3 test in `run_phaseF_tests.py::test_F3` bolts the Yukawa source onto `state.Pi` outside the Strang split, so the (Φ, Ψ) pair are not conjugate variables of a single Hamiltonian. Energy is not conserved, and the test guards against this with an explicit `> 100.0` early-stop.

### Double-precision regression run
- Re-ran `run_simulation.py` (stages 1–6), `run_phase_tests.py` (Phases A–E, 8 phases), and `run_phaseF_tests.py` (Phase F, 4 phases). Total 12/12 phases + 6 Weyl stages still pass.
- Verified the codebase already runs at native float64/complex128 under NumPy 2.2.6. Cleared `__pycache__` via `PYTHONDONTWRITEBYTECODE=1` so no stale bytecode could mask a regression.
- **No variation** vs. the values tabulated in `project-status.md`. Residuals are at the same 1e-16 floor; Stage 5's reversibility residual scales linearly with run length at ~6e-16/step, confirming it is precision-bound rather than a structural bug.
- New numeric data points captured: Stage 5 residual scaling (n=100..5000 → 5.8e-14..3e-12), Stage 6 3D norm constant at 150.3449 across t=0..5000, and F3 `max|Φ−v|=6.95e-01` over 30 steps (informational baseline for the eventual symplectic fix).

## Earlier (pre-2026-05-14)

Earlier non-trivial decisions live in `project-status.md` under the "Corrections Log" and `ca-unified-proposition.md`. Notable:

- Page-38 boxed FD equations corrected to include `i` on y-derivative terms (2026-05-13).
- Phase F suite (F1–F4) added on top of Phases A–E; F3 ships as a sketch only, with the open engineering item flagged in `ca-unified-proposition.md` line 159.
- Split-step FFT propagator adopted everywhere for production runs; explicit Euler steppers retained only to reproduce the page-39 instability observation.
