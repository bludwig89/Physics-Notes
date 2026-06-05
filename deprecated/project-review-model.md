# Project Review — Model & Software Structure

*2026-05-22. Describes the architecture, modules, phases, and design decisions of the "universe in a bottle" lattice-CA simulation.*

---

## 1. Top-Level Goal

The project aims to build a **self-consistent cellular automaton that reproduces known physics** at the quantum, relativistic, and gravitational levels from local lattice rules alone — a "universe in a bottle" in miniature. The design philosophy is:

- All equations should hold to **algebraic exactness** where possible.
- Where not exact, aim for **machine-precision** (FFT round-off floor).
- Where not machine-precision, aim for **quantitative agreement** inside a stated tolerance.
- New predictions must be falsifiable by real observations.

---

## 2. Repository Layout

```
Physics Notes/
├── ca-simulation/          Core simulation modules
│   ├── ca_core.py          Pedagogical Euler + split-step propagators
│   ├── ca_dirac.py         Dirac 4-spinor, U(1) gauge, Aharonov-Bohm
│   ├── ca_bcc.py           3D BCC Weyl QCA (Paper 1 Eq. 15, sign-corrected)
│   ├── ca_core_exact.py    2D exact arccos QCA (Paper 1 Eq. 16)
│   ├── ca_curved.py        Variable-c refraction, Cayley/Crank-Nicolson
│   ├── ca_weak.py          SU(2) weak gauge, parity violation
│   ├── ca_strong.py        SU(3) link-variable lattice gauge + Yukawa
│   ├── ca_higgs.py         Complex scalar Φ, Mexican-hat potential
│   ├── ca_unified.py       Coupled Φ-Dirac via Yukawa (Phase F)
│   ├── ca_maxwell.py       Composite photon bilinear, Mohr formalism
│   ├── ca_maxwell_2d.py    2D composite-photon bilinear
│   ├── ca_emqg.py          EMQG Poisson, variable-c gravity
│   ├── ca_dirac_bcc.py     3D BCC Dirac propagator
│   ├── ca_fft.py           Multi-core scipy FFT backend
│   ├── ca_lattice.py       k-grid construction, LatticeConfig
│   ├── ca_propagator.py    Cached spectral propagators
│   ├── ca_lazy.py          TickCounter, lazy_step wrapper
│   ├── poisson_open.py     Open-BC James/Hockney free-space Poisson solver
│   ├── derive_beta_LV.py   Sympy derivation of β_LV, γ_LV, δ_LV, ε_LV
│   ├── derive_velocity_addition.py  Deformed velocity-addition formula
│   └── forks/              Fork harnesses for GR-3 and curl-residual tests
│       ├── gr3_fork_harness.py
│       ├── curl_fork_harness.py
│       ├── curl_fork_baseline_bcc.py
│       └── curl_fork_cubic.py
├── model-tests/            Test scripts
│   ├── test_*.py / run_*.py
│   └── tests-priority/     Priority 10-test suite
│       ├── test_01b_GR1_openBC.py
│       ├── test_02_QM1_CHSH.py
│       ├── test_04_GR3_pound_rebka.py
│       ├── test_05b_GR2_openBC.py
│       ├── test_06_QG2_planck_LV.py
│       ├── test_07_QFT5_neutrino.py
│       ├── test_08_QM2_tunneling.py
│       ├── test_09_GR4_mercury.py
│       └── test_10_QG4_charge.py
├── test-results/           JSON dumps, markdown summaries, figures/
├── reference-research/     PDFs and research-summary markdown files
├── findings/               Individual finding files F16-F22 and beyond
├── findings.md             Findings F1–F15 (main log)
├── exactness-inventory.md  Tier-1/2/3 exactness table
├── project-status.md       Current status, module list, test results
├── changelog.md            Non-trivial software changes
└── CLAUDE.md               Project instructions for AI assistant
```

---

## 3. Lattice Design

### 3.1 Geometry

The primary lattice is the **body-centred cubic (BCC)** in 3D, the unique lattice forced by the QCA informational principles (linearity + unitarity + locality + homogeneity + isotropy). A **2D-square** lattice is also used for tests and derivations.

**BCC primitive vectors** (in units of $a$):

$$\mathbf{a}_1 = (1,0,0), \quad \mathbf{a}_2 = (0,1,0), \quad \mathbf{a}_3 = (\tfrac12,\tfrac12,\tfrac12).$$

The 8 BCC nearest-neighbour directions produce the $u, \tilde{n}_x, \tilde{n}_y, \tilde{n}_z$ kernel.

### 3.2 Lattice spacing and speed of light

The dimensionless lattice speed of light is $c_\text{lat} = 1/\sqrt{d}$, emerging automatically from the arccos dispersion. In 3D: $c_\text{lat} = 1/\sqrt{3} \approx 0.577$. In 2D: $c_\text{lat} = 1/\sqrt{2} \approx 0.707$.

The SI identification $a = \ell_P$, $\tau = t_P$ gives $c_\text{physical} = c/\sqrt{d}$ (under investigation, Finding 10).

### 3.3 Field types

| Field | Type | Shape | Used in |
|---|---|---|---|
| Weyl spinor $\psi$ | complex64/128 array | $(L^d, 2)$ | ca_bcc, ca_core_exact |
| Dirac 4-spinor | complex128 array | $(L^d, 4)$ | ca_dirac, ca_dirac_bcc |
| Complex scalar $\Phi$ | complex128 | $(L^d,)$ | ca_higgs, ca_unified |
| SU(2) gauge $A_\mu$ | real128 | $(L^d, 3)$ | ca_weak |
| SU(3) link $U_\mu$ | complex128 | $(L^d, 4, 3, 3)$ | ca_strong |
| Gravitational potential $\phi$ | float64 | $(L^d,)$ | ca_emqg, ca_curved |
| Composite photon $G$ | complex128 | $(L^d, 3)$ | ca_maxwell |
| Tick counter $N$ | int/float | $(L^d,)$ | ca_lazy |

---

## 4. Phase Architecture

The simulation is organised into **phases**, each adding a layer of physics.

### Phase A — Free Weyl (Baseline)
- Module: `ca_bcc.py`, `ca_core_exact.py`
- Physics: Massless BCC Weyl QCA propagation
- Key result: Dispersion $\omega = \arccos(u_\text{BCC})$ exact to $4.4\times10^{-16}$

### Phase B — Wavepacket dynamics
- Physics: Group velocity $v_g = c\hat{k}$, wavepacket spreading, BCC vs 2D-square comparison

### Phase C — Curved spacetime (variable-c)
- Module: `ca_curved.py`
- Physics: Position-dependent $c(\mathbf{x})$ with exact-unitary Cayley stepper
- Key result: Snell refraction, Shapiro time delay, emergent tick ratio

### Phase D — Dirac (massive)
- Module: `ca_dirac.py`
- Physics: 4-spinor propagation, zitterbewegung, Klein paradox
- Key result: Dispersion $\omega = \arccos(\sqrt{1-m^2}\cos k_x\cos k_y)$ exact

### Phase E1 — U(1) gauge (Aharonov-Bohm)
- Module: `ca_dirac.py` (extended)
- Physics: Minimal coupling $\partial_\mu \to \partial_\mu - iA_\mu$, flux-tube phase pickup
- Key result: Phase pickup $= \exp(i\oint A)$ to $4.4\times10^{-16}$

### Phase E2 — SU(2) weak gauge
- Module: `ca_weak.py`
- Physics: Left-chirality-only SU(2) coupling, parity violation
- Key result: Right-chirality leak = 0 (machine zero)

### Phase E3 — SU(3) strong gauge
- Module: `ca_strong.py`
- Physics: Link-variable formulation, Gell-Mann generators, Wilson plaquette, Yukawa wiring
- Key results: Cold-link vacuum regression exact; global colour charge conserved to $3.8\times10^{-13}$

### Phase F1 — Higgs scalar
- Module: `ca_higgs.py`
- Physics: Complex scalar $\Phi$, Mexican-hat $V(\Phi)$, Goldstone boson, radial Higgs mode
- Key result: Goldstone dispersion $\omega = |k|$ exact; CFL stability constraint $dt < 2/\sqrt{8+2\mu^2}$

### Phase F2 — Higgs with mass gap
- Physics: Radial mode $\omega = \sqrt{k^2+2\mu^2}$, $O(dt^2)$ Verlet accuracy

### Phase F — Unified Dirac-Higgs
- Module: `ca_unified.py`
- Physics: Coupled $\Phi$-Dirac system via Yukawa $m_\text{eff}(\mathbf{x}) = y\,\mathrm{Re}(\Phi)$
- Key result: Symplectic-Yukawa energy drift 3 ppm over 200 steps; Yukawa uniform-Φ regression exact to bit-zero (V13c)

### Phase L1 — 3D BCC Maxwell (composite photon)
- Module: `ca_maxwell.py`
- Physics: Bilinear $G^i = \phi^T\sigma^i\psi$, Mohr 6-component formalism, polarization basis, Lorentz boost, VSH angular-momentum eigenstates, Green function
- Key result: Transversality, orthonormality, completeness, Poynting conservation all at Tier 1/2 precision

### Phase L2 — 2D composite photon
- Module: `ca_maxwell_2d.py`
- Physics: 2D bilinear, frequency-dependent $c$

### Phase L3 — Composite photon dispersion
- Physics: $\Omega_\gamma = c_\text{lat}|k|$ confirmed to 0.21%

### Phase L4 — EMQG gravity
- Module: `ca_emqg.py`
- Physics: EMQG Poisson solver, variable-c gravity, Newtonian lensing
- Key result: Newtonian lensing linear-in-$M$ to 0.35% (3D solver)

### Phase T — Emergent time
- Module: `ca_lazy.py`
- Physics: Tick counters, vacuum freezing, proper-time / coordinate-time ratio
- Key result: Vacuum freezing $N_\text{binary} = 0$ exact; phase-tick ratio $= c_\text{in}/c_\text{out}$ to $2.7\times10^{-16}$

---

## 5. Core Propagator Machinery

### 5.1 Spectral propagator

All propagation uses the spectral method:

1. **Forward FFT**: $\psi(\mathbf{x}) \to \tilde\psi(\mathbf{k})$.
2. **Multiply by unitary**: $\tilde\psi(\mathbf{k}) \to U(\mathbf{k})\tilde\psi(\mathbf{k})$.
3. **Inverse FFT**: $\tilde\psi(\mathbf{k}) \to \psi(\mathbf{x})$.

The unitary matrix $U(\mathbf{k}) = u(\mathbf{k})I + i\tilde{\mathbf{n}}(\mathbf{k})\cdot\boldsymbol\sigma$ is computed analytically from the BCC or square-lattice kernel.

### 5.2 Strang composition

For multi-dimensional or coupled systems the Strang symmetric splitting gives second-order accuracy with exact unitarity:

$$U_\text{Strang} = U_x^{1/2} \cdot U_y^{1/2} \cdot U_z \cdot U_y^{1/2} \cdot U_x^{1/2}.$$

### 5.3 Cayley transform

For the variable-$c$ stepper, the Cayley transform replaces direct exponentiation:

$$U_\text{Cayley} = (I - iH\Delta t/2)(I + iH\Delta t/2)^{-1}.$$

This is **exactly unitary** for any $\Delta t$, as opposed to the Strang approximation which has $O(\Delta t^3)$ norm drift per step.

### 5.4 Caching

`ca_propagator.py` caches the spectral unitary $U(\mathbf{k})$ and the $\mathbf{k}$-grid arrays. `ca_fft.py` uses scipy's multi-core FFT backend (rfftn/irfftn for real fields, fftn/ifftn for complex). `ca_lattice.py` constructs the $\mathbf{k}$-grid and the `LatticeConfig` data structure (grid size $L$, spacing $a$, dimensionality $d$).

### 5.5 Lazy stepper

`ca_lazy.py` wraps any propagator with a tick-counter layer. The `TickCounter` accumulates $N(\mathbf{x})$ using either the binary threshold or the phase-accumulation method. The `lazy_step` wrapper calls the underlying stepper only for cells with non-zero amplitude, saving computation in sparse runs.

---

## 6. Open-BC Poisson Solver

`poisson_open.py` implements the James/Hockney algorithm:

1. Zero-pad $(L,L,L)$ source $\rho$ to $(2L,2L,2L)$.
2. Build free-space Green's function $G(r) = -1/(4\pi r)$ with half-cell self-regularisation ($r_\min = 0.5$).
3. FFT-convolve to get $\phi$.
4. Extract the central $(L,L,L)$ block.

Verification: $\phi(r) = -G_N M/r$ recovered to $2.2\times10^{-16}$ at $r\ge20$ cells.

This replaces the periodic-BC Poisson solver that was the largest accuracy bottleneck on the GR-domain tests (reducing GR-1 error from 12.5% to 3.0%, GR-2 from 38% to 0.06%).

---

## 7. Analytic Derivation Modules

### 7.1 `derive_beta_LV.py`

Uses sympy to derive and verify the four closed-form Lorentz-violation coefficients $\beta_\text{LV}, \gamma_\text{LV}, \delta_\text{LV}, \varepsilon_\text{LV}$ from the 2D-square Dirac dispersion. The derivation:

1. Series-expand $\omega(u) = \arccos(n\cos u)$ to order $u^9$.
2. Differentiate to get $v_g(u)$.
3. Invert series $u(\beta)$.
4. Compute $R(\beta) = (\omega - u\omega')/\omega_0$ and subtract $1/\gamma_\text{SR}$.
5. Read off coefficients.

All four reduce the symbolic-minus-closed-form residual to **0** in sympy.

### 7.2 `derive_velocity_addition.py`

Derives the closed-form deformed velocity-addition formula from the same QCA dispersion (Finding 22). Uses the 4-momentum velocity $u_p = kc_\text{lat}^2/\omega$ and the SR boost law.

---

## 8. Fork Architecture

The GR-3 fork harness (`forks/gr3_fork_harness.py`) and curl-residual fork harness (`forks/curl_fork_harness.py`) implement a **geometry/physics fork interface** pattern:

Each fork module exposes a standard API: `metric()`, `uvec()`, `unitary()`, `dispersion()`, `eigenmodes()`. The harness instantiates all forks, runs identical diagnostics on each, and compares results in a single output table. This design allows testing multiple physical hypotheses (e.g., Fork A vs B vs C for the GR-3 factor-2) without duplicating boilerplate.

---

## 9. Test Infrastructure

### 9.1 Phase tests (`run_phase_tests.py`)

Tests each simulation phase in sequence (A through L4). Each phase test checks the primary observable against its expected value and reports PASS/FAIL with tolerance.

### 9.2 Priority tests (`tests-priority/`)

The 10-test **priority suite** maps onto the most discriminating experimental predictions:

| Test | File | Observable | Status |
|---|---|---|---|
| GR-1 | test_01b_GR1_openBC.py | Light deflection coefficient $K=4$ | PASS (3.0% off) |
| QM-1 | test_02_QM1_CHSH.py | Tsirelson bound $2\sqrt{2}$ | PASS (machine precision) |
| SR-2 | (inline) | Time dilation $1/\gamma$ | PASS (dispersion identity) |
| GR-3 | test_04_GR3_pound_rebka.py | Pound-Rebka $\Delta\nu/\nu$ | FAIL baseline; PASS with forks |
| GR-2 | test_05b_GR2_openBC.py | Shapiro delay $\gamma=1$ | PASS (0.06% off) |
| QG-2 | test_06_QG2_planck_LV.py | Lorentz-violation energy scale | PASS ($1.87\times10^{20}$ GeV) |
| QFT-5 | test_07_QFT5_neutrino.py | Neutrino oscillations (PMNS) | PASS (mechanism) |
| QM-2 | test_08_QM2_tunneling.py | Tunneling / Klein paradox | Narrow-window PASS |
| GR-4 | test_09_GR4_mercury.py | Mercury perihelion 1PN | PASS (1.5% off) |
| QG-4 | test_10_QG4_charge.py | Noether charge conservation | PASS (FFT floor) |

### 9.3 QCA verifications (`run_qca_verifications.py`)

Automated checks of all QCA properties derived from the Papers:

- V1: 2D dispersion identity
- V2: Klein paradox plateau shape
- V5: Frequency-dependent $c$ off-axis
- V6: BCC vs simple-cubic regression
- V7: $A_0 = 0$ audit (Paper 2)
- V8: DSR Lorentz-deformation signature
- V13a/b/c: SU(3) colour charge suites

---

## 10. Key Design Decisions

### 10.1 Exact-unitary vs approximate propagators

The choice of the Cayley transform over simple exponentiation was motivated by the finding that the Strang split-step gives 32.6% norm drift per step in the variable-$c$ regime, while the Cayley version gives $5.5\times10^{-15}$ — 10 orders of magnitude better. This choice is recorded in `changelog.md` as the C1 phase-transition decision.

### 10.2 Open-BC vs periodic Poisson

The periodic-BC Poisson solver suppresses the $1/r$ tail of the gravitational potential, introducing systematic errors of 12–38% in GR line-integral tests. The switch to the James/Hockney open-BC solver (May 2026) was the single most impactful accuracy improvement in the project's GR sector.

### 10.3 Off-diagonal Dirac block: $U_k^\dagger$, not $U_k^*$

The lower-right block of the 4×4 Dirac propagator must be $U_k^\dagger$ (Hermitian conjugate), not $U_k^*$ (element-wise conjugate). This is forced by the requirement that the full $4\times4$ matrix be unitary. Using $U_k^*$ would break unitarity and give incorrect dispersion for the right-chirality sector.

### 10.4 Paper 1 Eq. 15 sign correction (Finding 1)

The original Paper 1 had a typo: the $\tilde{n}_y$ second term was transcribed as $-s_xc_ys_z$ instead of $+s_xc_ys_z$. With the wrong sign the unitarity residual $|u^2 + |\tilde{n}|^2 - 1|$ was $0.47$; with the correction it is $4.4\times10^{-16}$.

### 10.5 CFL constraint in Phase F1

The Higgs radial mode propagation with `n_phi_sub=1`, `dt=1.0` violates the CFL stability bound $dt_\text{sub} < 2/\sqrt{8+2\mu^2} \approx 0.667$, causing NaN divergence at $L=320$. Fix: use `n_phi_sub=2` (sub-steps the Φ propagation twice per fermion step).

### 10.6 2D Poisson gives wrong 3D lensing

A 2D Poisson solver gives $\phi \sim \ln r$ (logarithmic), not $1/r$ (Newtonian), which is dimensionally inconsistent with the 3D gravity target. The EMQG lensing tests now use a 3D Poisson solver sliced at the equatorial plane.

### 10.7 Periodic-BC phase-wrap ambiguity (E1)

The Aharonov-Bohm test measured `abs(measured - analytic)` which reports $2\pi$ when the wavepacket traverses the flux tube in the reverse sense. Physics is correct; the measurement is fixed by using $\min(|\Delta|, 2\pi - |\Delta|) < 10^{-12}$.

---

## 11. Known Open Items

| Item | Status | What blocks it |
|---|---|---|
| SI unit identification for $a$ and $\tau$ (Finding 10) | Open | Project hasn't committed to one of three resolutions |
| Composite-photon curl at $O(k^3)$ | Open | Need to implement Paper 1's smearing function $f_\mathbf{k}(\mathbf{q})$ |
| $1/b$ scaling of 3D EMQG lensing | Open | 3D potential / scanning needed |
| GR-3 fork selection (A vs B) | Open | Forks A and B both fix GR-3; Fork C falsified by GR-4 |
| F19 area-vs-volume tick scaling | Open (stub) | No run data; test spec only |
| Subleading curl coefficient | Open | No closed form yet ($\beta\approx0.01883$ in 3D) |
| Cayley stepper at $L\ge960$ | Open | Memory exceeds sandbox (~5-10 GB sparse-LU) |

---

*End of Model Structure Summary. Cross-reference: `project-status.md`, `changelog.md`, and the module headers in `ca-simulation/`.*
