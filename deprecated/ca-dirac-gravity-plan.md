# Dirac CA with Gravitational Curve Structure — Implementation Plan

A plan to extend the existing massless Weyl CA (`ca-simulation/ca_core.py`) into a Dirac CA with a curved-background structure. Builds directly on the split-step FFT propagator that has already been verified to machine precision for the Weyl case.

The notebook itself already contains the physics for both extensions: pages 16–34 set up the Sachs curved-spacetime spinor formalism, and pages 59–60 / 81–88 work out the Dirac plane-wave solutions in the Weyl representation. This plan turns those pages into discrete update rules.

*Drafted 2026-05-14.*

---

## Architecture overview

Three stages, layered:

| Stage | Adds | Field on each cell | Notebook reference |
|---|---|---|---|
| D1 | Mass term (Weyl → Dirac) | 4-component spinor $\Psi = (\eta, \chi)$ | pages 38, 59–60, 81–88 |
| D2 | Static curved background | Tetrad $e^a{}_\mu(\mathbf{x})$ and spin connection $\Omega_\mu(\mathbf{x})$ — fixed in time | pages 16–17, 33 |
| D3 | Backreaction (geometry sourced by matter) | $\Omega_\mu$, $e^a{}_\mu$ evolve from discrete Einstein equations | pages 18–29 |

D1 is engineering; D2 is engineering on top of D1; D3 is research. Each stage is independently testable.

---

## Stage D1 — Dirac CA on a flat lattice

**Goal.** Add a mass coupling between the two Weyl components without losing exact unitarity or the split-step Fourier structure.

### Physics

The Dirac equation in the Weyl (chiral) representation, using two 2-component spinors $\eta$ (left-handed) and $\chi$ (right-handed):

$$i\partial_t \eta = -i c\,\boldsymbol{\sigma}\cdot\nabla\eta + mc^2\,\chi$$

$$i\partial_t \chi = +i c\,\boldsymbol{\sigma}\cdot\nabla\chi + mc^2\,\eta$$

Equivalently, with $\Psi = (\eta, \chi)^T$ a 4-component spinor:

$$i\partial_t \Psi = H_D\,\Psi, \qquad H_D = c\,\boldsymbol{\alpha}\cdot\hat{\mathbf{p}} + m c^2\,\beta$$

with Dirac matrices in Weyl form:

$$\boldsymbol{\alpha} = \begin{pmatrix} \boldsymbol{\sigma} & 0 \\ 0 & -\boldsymbol{\sigma} \end{pmatrix}, \qquad \beta = \begin{pmatrix} 0 & I \\ I & 0 \end{pmatrix}$$

In Fourier space the Hamiltonian is the constant $4\times 4$ matrix:

$$H_D(\mathbf{k}) = c\,\boldsymbol{\alpha}\cdot\mathbf{k} + m c^2\,\beta$$

with eigenvalues $\pm E(\mathbf{k})$ where $E(\mathbf{k}) = \sqrt{c^2|\mathbf{k}|^2 + m^2 c^4}$ — the Dirac dispersion.

### Discrete propagator (Stage D1)

The exact unitary per timestep is:

$$U_D(\mathbf{k}) = \exp\!\bigl(-i\,H_D(\mathbf{k})\,\Delta t\bigr) = \cos(E\Delta t)\,I_4 - i\,\frac{\sin(E\Delta t)}{E}\,H_D(\mathbf{k})$$

This is the direct generalization of the existing Weyl $U(\mathbf{k}) = \cos(c\kappa) I - i\sin(c\kappa)/\kappa\,\boldsymbol{\sigma}\cdot\mathbf{k}$. Same structure, just $4\times 4$ instead of $2\times 2$, with the energy $E$ replacing $c\kappa$.

Setting $m = 0$ reduces $H_D$ to block-diagonal $\mathrm{diag}(c\,\boldsymbol{\sigma}\cdot\mathbf{k}, -c\,\boldsymbol{\sigma}\cdot\mathbf{k})$ and recovers two independent copies of the existing Weyl propagator (one per chirality). This is the regression test.

### Deliverables

- `weyl_step_2d_splitstep` and `_3d` kept as-is. New `dirac_step_2d_splitstep(eta_f, eta_g, chi_f, chi_g, c, m)` and `dirac_step_3d_splitstep(...)` in `ca_core.py`.
- New initial-condition helpers: `gaussian_dirac_2d(shape, ..., chirality)` analogous to the existing Weyl helpers.
- New verification function `verify_dirac_dispersion_2d` / `_3d`. Same pattern as the Weyl version, but the analytic phase is $E\Delta t = \sqrt{c^2|\mathbf{k}|^2 + m^2 c^4}\,\Delta t$.

### Tests

| Test | Expected outcome |
|---|---|
| $m = 0$ | Bitwise (to machine eps) equal to two decoupled Weyl runs |
| Norm conservation | $|\Delta|\Psi|^2| < 10^{-13}$ over 5000 steps |
| Time-reversibility (negate $\Delta t$) | Residual $\sim 10^{-14}$ over 5000 forward + 5000 backward |
| Dispersion ω = E(k) | Max $|\Delta\omega|$ at machine precision, all $\mathbf{k}$ |
| Wave-packet group velocity | $v_g = c^2|\mathbf{k}|/E < c$, slowing as $m$ grows |
| Zitterbewegung | Centroid of a localized non-eigenstate packet oscillates at frequency $\approx 2mc^2/\hbar$ (set $\hbar = 1$). This is the cleanest "particle-with-mass" observable; verifies the $\eta\leftrightarrow\chi$ coupling. |

**Effort.** Small to medium. The 4×4 propagator is a straightforward extension; the test suite is the substantive work. Estimate: 1–2 days.

**Risk.** Low. All physics is closed-form; closely parallel to the existing Weyl implementation.

---

## Stage D2 — Static curved background

**Goal.** Place the Dirac field on a curved spacetime represented by a fixed-in-time tetrad and spin connection. Verify that wave packets follow geodesics of the underlying metric.

### Physics (Sachs route, notebook pages 16–17, 33)

In curved spacetime the partial derivative becomes a covariant derivative:

$$\nabla_\mu \eta = \partial_\mu\eta + \Omega_\mu\,\eta, \qquad \nabla_\mu \chi = \partial_\mu\chi + \widetilde{\Omega}_\mu\,\chi$$

where $\Omega_\mu(\mathbf{x})$ is the spin connection (a 2×2 matrix at each spacetime point, acting on each Weyl component; for Dirac, a 4×4 block-diagonal with $\Omega_\mu$ and $\widetilde\Omega_\mu = -\Omega_\mu^\dagger$, per page 33).

The flat-space Pauli derivative $\boldsymbol\sigma\cdot\nabla$ generalizes via the tetrad $e^a{}_\mu$:

$$\sigma^\mu(\mathbf{x}) = e^\mu{}_a(\mathbf{x})\,\sigma^a$$

Sachs writes this as $q^\mu(\mathbf{x}) = e^\mu{}_a \sigma^a$, with $q^\mu \tilde q^\nu + q^\nu \tilde q^\mu = 2 g^{\mu\nu}$ (page 32). The curved-space Dirac equation is:

$$i\,q^\mu(\mathbf{x})\,\nabla_\mu\,\eta + mc\,\chi = 0$$

and similarly for $\chi$ with $\tilde q^\mu$ and $\widetilde\Omega_\mu$. This is exactly what notebook pages 24–25 derive via the Euler–Lagrange equation $q^\mu\partial_\mu\eta + q^\mu\Omega_\mu\eta = 0$ in the massless limit.

### Discrete implementation

Per-cell data extends from scalar $\Psi$ to:
- $\Psi(\mathbf{x})$ — the 4-component spinor (Stage D1)
- $e^a{}_\mu(\mathbf{x})$ — the tetrad, a $4\times 4$ real array per cell (in 3+1D)
- $\Omega_\mu(\mathbf{x})$ — the spin connection, three $2\times 2$ complex matrices per cell (one per spatial direction)

The propagator is no longer Fourier-diagonal because $e^a{}_\mu$ varies with $\mathbf{x}$. Two implementation paths:

**Path D2a — Operator splitting (recommended first attempt).** Trotter-split the per-timestep evolution into:
1. A flat-space kinetic step using the Stage D1 propagator with the *average* $e^a{}_\mu$.
2. A position-space "correction" step that applies the local deviation $\delta e^a{}_\mu(\mathbf{x}) = e^a{}_\mu(\mathbf{x}) - \bar e^a{}_\mu$ as a per-cell unitary phase.

Trotter error is $O(\Delta t^2 \cdot |\nabla e|)$. For slowly-varying metrics this is acceptable. Refinable to higher-order splittings (Strang, etc.) if needed.

**Path D2b — Direct discrete covariant derivative.** Replace $\partial_\mu \eta$ everywhere with the centred difference *plus* the local spin connection: $\nabla_\mu\eta(\mathbf{x}) = \tfrac{1}{2}(\eta(\mathbf{x}+\hat\mu) - \eta(\mathbf{x}-\hat\mu)) + \Omega_\mu(\mathbf{x})\eta(\mathbf{x})$. Apply explicit Euler. This is the easy-to-write version but inherits the unconditional instability of the page 38 explicit Weyl scheme — same problem. Not recommended for production.

Path D2a keeps the unitarity-by-construction property of the existing split-step.

### Test geometries

These are the smallest curved backgrounds with closed-form geodesics, so wave-packet trajectories can be compared against analytic predictions.

| Background | Metric | What it tests |
|---|---|---|
| Rindler (uniformly accelerated frame) | $ds^2 = -(1 + a x)^2 dt^2 + dx^2 + dy^2 + dz^2$ | Equivalence principle: a free wave packet should follow a hyperbolic worldline at proper acceleration $a$ |
| Weak Schwarzschild (linearized) | $g_{00} = -(1 - 2GM/r)$, $g_{ii} = 1 + 2GM/r$ | Bending of a wave packet around a "mass" — Newtonian limit |
| Wave-packet redshift | Static metric with $g_{00}$ varying along packet trajectory | Frequency shift matches gravitational-redshift formula |

### Deliverables

- New module `ca-simulation/ca_curved.py` with `dirac_step_curved_2d_splitstep` and tetrad/connection setup helpers.
- New stage in `run_simulation.py`: Rindler test, Schwarzschild bending test, redshift test. Each outputs a figure showing the wave-packet centroid trajectory overlaid on the analytic geodesic.
- Section in `ca-reference.md` documenting (a) the split-step + connection-correction scheme, (b) the Trotter error bound, (c) the three test results.

**Effort.** Medium to large. The tetrad/connection bookkeeping is finicky. Estimate: 1–2 weeks of careful work, mostly in correctly building $\Omega_\mu$ for each test metric.

**Risk.** Medium. The cleanest failure mode is connection-coefficient sign errors; the dispersion-style verification framework already in place catches these by comparing wave-packet trajectories to known analytic geodesics.

---

## Stage D3 — Backreaction (research-level)

**Goal.** Allow the geometry to evolve in response to the matter field — the discrete analog of $G_{\mu\nu} = 8\pi T_{\mu\nu}$.

### Physics (Sachs route, notebook pages 18–29)

The notebook already has this worked out as a Hamiltonian system. Page 18 derives $\mathcal{H}_{\text{grav}} = G_{00}/8\pi$. Pages 24–29 vary the action with respect to the independent field variables: $\eta$, $\chi$, $q^\mu$, $\Omega_\mu$. The matter variation gives the curved-space Dirac equation (D2); the geometric variation gives the discrete Einstein equations:

- Variation w.r.t. $q^\lambda$ (page 29): a relation involving $K_{\lambda\rho}\tilde q^\rho$ and the matter current — the discrete version of $R_{\mu\nu} - \tfrac{1}{2}g_{\mu\nu}R = 8\pi T_{\mu\nu}$.
- Variation w.r.t. $\Omega_\rho$ (pages 26–28): an algebraic relation that fixes $\Omega$ in terms of $q^\mu$ — i.e., the spin connection is not independent.

Page 26 flags a non-trivial issue: $(\partial\mathcal{L}/\partial\Omega_{\rho,\nu})_{;\nu}$ appears to vanish, in conflict with Sachs. The author writes: "Sachs gets 0 on the LHS … but apparently this doesn't hold!" This is an open question in the notebook itself. **Any D3 implementation has to resolve this**, or take a different route.

### Implementation strategy

Two honest paths:

**D3a — Linearized backreaction.** Treat the metric as $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}(\mathbf{x},t)$ with $|h| \ll 1$. Evolve $h_{\mu\nu}$ via the linearized Einstein equation $\Box h_{\mu\nu} = -16\pi G\, T_{\mu\nu}^{(0)}$, where $T_{\mu\nu}^{(0)}$ is computed from $\Psi$ on the flat background. Couple back: the Dirac field sees the modified tetrad. This is gravitational-wave-emission territory, well-defined, and the linearization makes the Trotter splitting tractable. It does *not* test strong-field GR.

**D3b — Full nonlinear backreaction via the Sachs Hamiltonian.** Implement $\mathcal{H} = \mathcal{H}_{\text{grav}} + \mathcal{H}_{\text{matter}}$ from notebook page 22 directly as a discrete update. This requires resolving the page-26 disagreement, choosing a discretization for $R$ and $K_{\mu\nu}$, and proving (or just numerically verifying) that the discrete update conserves a positive-definite analog of total energy. This is research, not engineering.

### Deliverables

- For D3a: a working linearized backreaction stage. The honest test is gravitational redshift sourced *by the field itself* — a wave packet's own mass causes a small frequency shift in a second probe packet.
- For D3b: a design document `ca-backreaction-design.md` that (i) makes a concrete choice for the discrete curvature operator, (ii) lays out the analog of the page 26 / Sachs disagreement and proposes a resolution path (most likely: switch from Sachs' tetrad formulation to a metric formulation where the disagreement does not arise), and (iii) defines the conservation-law audit needed before any implementation begins.

**Effort.** D3a: 2–3 weeks. D3b: open research.

**Risk.** D3a: medium — the linearization makes the engineering clean but the test is subtle (the self-redshift effect is small and easily swamped by numerical artifacts). D3b: high. This is where the literature has not converged.

---

## Visualization implications

The Bloch-sphere coloring in `ca-next-steps-plan.md` Phase A1 was for the 2-component Weyl spinor. The Dirac field has 4 complex components per cell.

Two natural extensions:

1. **Two-sphere visualization.** Show $\eta$ (left chirality) and $\chi$ (right chirality) on adjacent panels, each Bloch-colored as in the Weyl plan. The mass coupling makes them interconvert; the animation reveals chirality flipping at rate $\sim m c^2 / \hbar$.
2. **Bispinor-as-vector visualization.** A Dirac spinor up to overall phase is a point on $\mathbb{CP}^3$, a 6-real-dimensional manifold. There is no clean single-color encoding. Recommend (1) instead.

The curved-background work (D2) needs an additional channel to visualize the geometry itself: a separate overlay or animation showing the local metric or spin connection. Suggest a wireframe deformation of the lattice or a vector field for $\Omega_\mu$.

---

## Summary table

| Stage | Adds | Effort | Risk | Engineering vs Research |
|---|---|---|---|---|
| D1 | Mass term, 4-spinor, Dirac propagator | S–M | Low | Engineering |
| D2 | Static curved background, tetrad + connection | M–L | Med | Engineering |
| D3a | Linearized backreaction (weak-field) | L | Med | Engineering with care |
| D3b | Full nonlinear backreaction | open | High | Research |

Recommended order: D1 → verify against Weyl regression → D2 (Rindler test first, then Schwarzschild) → D3a. D3b only after the page-26 disagreement is understood.

---

## Dependencies on the existing codebase

- `weyl_step_2d_splitstep` and `_3d` stay untouched and serve as the $m \to 0$ regression test.
- `verify_dispersion_2d` / `_3d` becomes the template for `verify_dirac_dispersion_*` — only the analytic phase needs to change.
- `run_and_reverse` and `norm_over_time` work without modification (they take an arbitrary `step_fn`).
- The Bloch-coloring helpers from `ca-next-steps-plan.md` Phase A1 are needed for D1 visualization.

No existing code is broken by any of these stages. Each new stage is purely additive.

---

## What this plan deliberately does *not* do

- **Quantum field theory.** The Dirac CA here is a single-particle relativistic quantum mechanics simulation — one wavefunction $\Psi(\mathbf{x},t)$, not a second-quantized field $\hat\Psi$. The notebook's pages 41–56 second-quantization work is a separate (and much harder) extension.
- **Gauge fields.** EM and weak interactions remain in `ca-forces-integration.md` as future work. The Dirac+gravity plan is independent of them.
- **Dynamic graph topology.** The lattice stays a fixed regular grid. The Wolfram-project-style hypergraph rewriting is outside the scope here. The "curve" in this plan lives in the metric and connection fields, not in the graph itself.
