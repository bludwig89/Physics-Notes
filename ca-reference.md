# Weyl Spinor Cellular Automaton — Reference

*Based on physics notebook pages 35–39, Mark Ludwig (2007–08). Implementation in `ca-simulation/ca_core.py`.*

---

## What this CA is

A **cellular automaton (CA)** is a grid of cells, each holding a value, updated simultaneously at every timestep by a fixed local rule. This CA propagates a two-component complex field (a **spinor**) on a regular lattice. The update rule is the discretized, massless **Weyl equation** — the equation governing massless spin-½ particles like neutrinos. Each timestep corresponds to one unit of discrete time; each cell corresponds to one unit of discrete space. The lattice is the spacetime.

The simulation has two modes: an explicit finite-difference scheme (from the notebook, unstable) and a split-step FFT propagator (derived from the same equations, exactly unitary and unconditionally stable). All production runs use the split-step propagator.

---

## The lattice

- **2D**: an $L \times L$ periodic (toroidal) grid. Each cell has 4 neighbors (±x, ±y).
- **3D**: an $L \times L \times L$ periodic cubic lattice. Each cell has 6 neighbors (±x, ±y, ±z).
- **Cell state**: a two-component complex spinor $\psi = (f, g) \in \mathbb{C}^2$.
- **Lattice speed**: $c$ — a dimensionless parameter controlling how fast the field propagates. Sets the discrete speed of light.

---

## Stage 1 — Scalar Wave CA

**Source:** page 37 of the notebook.

The simplest starting point: a real scalar field $f$ evolving by the discrete wave equation.

### Equation

$$f(x, y, t+1) = 2f(x,y,t) - f(x,y,t-1) + c^2 \nabla^2 f(x,y,t)$$

where the **4-neighbor Laplacian** is:

$$\nabla^2 f(x,y) = f(x{+}1,y) + f(x{-}1,y) + f(x,y{+}1) + f(x,y{-}1) - 4f(x,y)$$

### Problem

This scheme requires **two** time levels of memory ($t$ and $t-1$), and is numerically stable only when:

$$c \leq \frac{1}{\sqrt{2}} \approx 0.71 \quad \text{(2D CFL condition)}$$

The notebook writes the equation with $c = 1$, which violates this bound and diverges within steps (confirmed in Stage 1 output: peak amplitude hits $10^6$ almost immediately). More fundamentally, the two-time-step structure makes it hard to write a spinor-valued or reversible version. This motivates the Weyl reduction.

---

## Stage 2 — Weyl Spinor CA

**Source:** pages 38–39 of the notebook.

### Why spinors

The scalar wave equation is second-order in time. Dirac's trick (also used on page 38) reduces it to first-order by introducing a two-component spinor $\psi = (f, g)$ and factoring the wave operator:

$$\partial_t^2 - \nabla^2 = (\partial_t + \boldsymbol\sigma \cdot \nabla)(\partial_t - \boldsymbol\sigma \cdot \nabla)$$

where $\boldsymbol\sigma = (\sigma_x, \sigma_y, \sigma_z)$ are the **Pauli matrices**:

$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

Setting one factor to zero gives the **massless Weyl equation**:

$$\frac{\partial \psi}{\partial t} = -\boldsymbol\sigma \cdot \nabla\psi$$

This is first-order in both space and time. Each timestep requires only the current state — no memory of the previous step.

### Explicit finite-difference scheme (2D)

From page 38, dropping the $z$-derivative terms (which vanish in 2D):

$$f_{\text{new}} = f + c\left(-\partial_x g + i\,\partial_y g\right)$$

$$g_{\text{new}} = g + c\left(-\partial_x f - i\,\partial_y f\right)$$

where centred differences are used:

$$\partial_x h = h(x+1, y) - h(x-1, y), \qquad \partial_y h = h(x, y+1) - h(x, y-1)$$

**This scheme is unconditionally unstable** — explicit Euler applied to a skew-Hermitian operator always diverges, regardless of $c$. The notebook's observation that the simulation "interestingly stabilises at $\sim 0.43$" reflects slower divergence at lower $c$, not true stability. Confirmed by the CFL sweep (Stage 3).

> ⚠️ **Pedagogical-only.** `weyl_step_2d` and `weyl_step_3d` in `ca_core.py` are retained solely to reproduce the page 39 instability observation. `cfl_sweep` defaults to `use_splitstep=True`; pass `False` only when intentionally reproducing divergence. All production code paths use the split-step propagator below.

### Explicit finite-difference scheme (3D)

From page 38, full Weyl equation with all three Pauli-matrix terms:

$$f_{\text{new}} = f + c\left(-\partial_z f - \partial_x g + i\,\partial_y g\right)$$

$$g_{\text{new}} = g + c\left(-\partial_x f - i\,\partial_y f + \partial_z g\right)$$

Same instability applies.

---

## Stage 2b — Split-Step FFT Propagator

**The scheme actually used.** Derived from the same Weyl equation, but propagated exactly in Fourier space.

### How it works

Transform the spinor field to Fourier space. Each wavevector mode $\mathbf{k} = (k_x, k_y, k_z)$ evolves independently under the exact $2 \times 2$ unitary matrix:

$$U(\mathbf{k}) = \cos(c\kappa)\,I - \frac{i\sin(c\kappa)}{\kappa}\,(\boldsymbol\sigma \cdot \mathbf{k}), \qquad \kappa = |\mathbf{k}| = \sqrt{k_x^2 + k_y^2 + k_z^2}$$

In 2D ($k_z = 0$), the four elements of $U$ are:

$$U_{ff} = \cos(c\kappa), \qquad U_{fg} = -\frac{i\sin(c\kappa)}{\kappa}(k_x - ik_y)$$

$$U_{gf} = -\frac{i\sin(c\kappa)}{\kappa}(k_x + ik_y), \qquad U_{gg} = \cos(c\kappa)$$

In 3D, the $\sigma_z$ term adds:

$$U_{ff} = \cos(c\kappa) - \frac{i\sin(c\kappa)}{\kappa}\,k_z, \qquad U_{gg} = \cos(c\kappa) + \frac{i\sin(c\kappa)}{\kappa}\,k_z$$

(and $U_{fg}$, $U_{gf}$ unchanged from 2D).

One step in practice:

1. Compute $\hat F = \mathcal{F}[f]$, $\hat G = \mathcal{F}[g]$
2. Apply $U(\mathbf{k})$ to $(\hat F, \hat G)$ at each $\mathbf{k}$
3. Inverse transform back

### Why this is better

$U(\mathbf{k})$ is exactly unitary for all $c$ and all $\mathbf{k}$. The scheme is unconditionally stable — no CFL condition applies. Norm is conserved to machine precision ($\sim 10^{-15}$) at every step.

---

## Key properties (verified by simulation)

### Norm conservation

Total probability is conserved exactly:

$$\|\psi\|^2 = \sum_{x,y,z} \left(|f(x,y,z)|^2 + |g(x,y,z)|^2\right) = \text{const}$$

Verified over 5000 steps for $c \in \{0.30, 0.43, 0.50\}$: deviation $< 10^{-13}$.

### Time-reversibility

Running $n$ steps forward at speed $c$, then $n$ steps backward at speed $-c$, returns to the initial state. Negating $c$ reverses the sign of all spatial-derivative terms, implementing time-reversal.

Measured residual after 5000 forward + 5000 backward steps:

$$\frac{\|\psi_{\text{final}} - \psi_{\text{initial}}\|}{\|\psi_{\text{initial}}\|} \approx 6 \times 10^{-14}$$

This is machine-precision. The CA is, within floating-point limits, perfectly reversible.

### Weyl dispersion ω = c|k|

A separate check that the propagator implements the *correct* unitary, not just *a* unitary. For a plane-wave field $\psi_{\mathbf{k}}(\mathbf{x}) = h_+(\mathbf{k})\,e^{i\mathbf{k}\cdot\mathbf{x}}$ where $h_+$ is the positive-helicity eigenvector of $\boldsymbol\sigma\cdot\mathbf{k}$:

$$\psi_{\mathbf{k}}(t + 1) = e^{-i c|\mathbf{k}|}\,\psi_{\mathbf{k}}(t)$$

Running $N$ steps and extracting $\omega_{\text{num}}$ from the ratio $\langle\psi_0,\psi_N\rangle/\langle\psi_0,\psi_0\rangle = e^{-i\omega_{\text{num}}N}$, the residual against the analytic prediction $\omega = c|\mathbf{k}|$ is:

| Test | $L$ | $N$ | $c$ | $\max|\Delta\omega|$ |
|---|---|---|---|---|
| 2D, six wavevectors | 32 | 20 | 0.5 | $5 \times 10^{-17}$ |
| 3D, seven wavevectors | 16 | 20 | 0.5 | $8 \times 10^{-17}$ |

Machine precision. This confirms $U(\mathbf{k})$ is the exact Weyl propagator and would catch sign errors or component swaps that norm conservation and reversibility miss. Implementation: `verify_dispersion_2d` / `verify_dispersion_3d` in `ca_core.py`.

### Helicity

The two spinor components carry opposite helicities. A left-helicity initial state ($f = G$, $g = 0$) and a right-helicity state ($f = 0$, $g = G$) propagate differently. A mixed state ($f = g = G/\sqrt{2}$) propagates as a symmetric superposition.

---

## Initial conditions

All runs use a Gaussian envelope:

$$G(x, y) = \exp\!\left(-\frac{(x - x_c)^2 + (y - y_c)^2}{2\sigma^2}\right)$$

centered at $(x_c, y_c)$ with width $\sigma$. The spinor initial state is:

| Helicity | $f_0$ | $g_0$ |
|---|---|---|
| Left | $G$ | $0$ |
| Right | $0$ | $G$ |
| Mixed | $G/\sqrt{2}$ | $G/\sqrt{2}$ |

---

## The spacetime interpretation

The CA is not just a field on a background spacetime — **the lattice and its causal connections *are* spacetime**.

Each cell-timestep pair $(x, y, t)$ is an **event**. The neighborhood rule defines which events can causally influence which others: cell $(x, y)$ at time $t$ influences its neighbors at time $t+1$. This directed relationship — drawn as a graph — is a discrete **causal set**: the partial order of cause and effect that defines Lorentzian geometry.

The lattice speed $c$ sets the discrete light cone. No information propagates faster than $c$ lattice units per timestep. This is the CA equivalent of the speed of light.

---

## What the CA says about maximum density (black holes)

In GR, a singularity is a point of infinite curvature where the equations become undefined. In the CA:

- **Maximum local density is bounded.** Global norm conservation means the maximum possible density at any single cell is the total initial norm — a finite number. The equations do not change at high density. There is no breakdown.

- **Information is never destroyed.** Exact unitarity means the map from initial state to any future state is invertible. This is structural, not a numerical artifact.

- **The "singularity" is a finite state.** Where GR predicts infinity, the CA predicts a maximum-amplitude cell with the rest of the lattice at lower amplitude. The CA keeps running through it.

This is consistent with Loop Quantum Gravity and Loop Quantum Cosmology (Bojowald, 2001), which replace the singularity with a minimum-volume quantum-geometry state. The CA provides a computationally explicit version of the same argument.

---

## Current limitations

- **No dynamic geometry.** The lattice topology is fixed. Spacetime does not curve in response to the field. General relativity's backreaction (matter curves geometry; curved geometry guides matter) is not implemented.
- **No mass.** The Weyl equation is massless. Adding mass requires coupling $f$ and $g$ (the Dirac equation), which has not yet been implemented.
- **No self-interaction.** The evolution is linear. Gravitational collapse requires nonlinearity, which the current equations do not have.
- **Lorentz invariance is approximate.** The fixed regular lattice picks a preferred frame. The spinor-valued approach encodes Lorentz structure into the field values rather than the lattice, which partially mitigates this, but it is not fully resolved.

---

## Next Steps


- Build a represenation both visual and with graphs showing a particle and/or wave passing through the field.
- Determine structure and "minimum size".
- Determine how the speed of light is either a structure element or a measurement of the lattice connections.
- Continue figuring out the lattice topology and curvature in response to the field. Use physics_notes_pages documents for reference if applicable.
- Can the two spinor states of the CA be represented somehow in a 2 or 3-dimensional space with colors possibly?


*Last updated: 2026-05-14 — added pedagogical-only warning for Euler steppers and Weyl-dispersion verification section.*
