# Cellular Automata Simulation — Implementation Plan & Results

Based on pages 35–39 of the physics notebook (2007–08), `page35-cellular-automata-research.md`, `fredkin-correlation.md`, and `ca-forces-integration.md`.

**Status (2026-05-13):** All five stages implemented in `ca-simulation/` and run to 200 time steps. The explicit-Euler scheme (pages 38–39) has been supplemented with an exact split-step FFT propagator that is unconditionally stable. See [Simulation Results](#simulation-results) below.

---

## Goals

Implement the three stages of CA the notebook developed, from scalar wave to spinor-valued Weyl propagation, and verify the numerical results the author noted on page 39. A fourth stage extends to graph-based geometry per page 36.

---

## Tech Stack

| Layer | Tool | Reason |
|---|---|---|
| Core numerics | Python / NumPy | Complex-valued array operations map directly to spinor grids |
| Graph CAs | NetworkX | Arbitrary neighbor topology for the page 36 connection-number experiments |
| Visualization | Matplotlib + Plotly | 2D heatmaps, 3D isosurfaces, real-time animation |
| Notebooks | Jupyter | Mirrors the exploratory style of the original notes |

No external physics libraries needed; the update rules are fully explicit in the notebook.

---

## Stage 1 — Scalar Wave CA (Page 37)

**Physics:** The second-order finite-differenced wave equation in 2+1D:

$$f(m,n,t+1) = -2f(m,n,t) - f(m,n,t-1) + f(m+1,n,t) + f(m-1,n,t) + f(m,n+1,t) + f(m,n-1,t)$$

**Key issue the notes flag:** requires two time steps of state ($t$ and $t-1$), so the CA state is not purely Markovian.

**Implementation:**

```
grid shape:  (Nx, Ny)
state:       two arrays  f_now, f_prev  (real or complex float64)
update:      f_next = -2*f_now - f_prev + roll(f_now, +1, axis=0)
                                        + roll(f_now, -1, axis=0)
                                        + roll(f_now, +1, axis=1)
                                        + roll(f_now, -1, axis=1)
boundary:    periodic (toroidal) to start; absorbing later
```

**Experiments:**
1. Initialize with a Gaussian pulse; observe radial wave propagation.
2. Observe the instability the notes describe — the rule as written diverges.
3. Add the ½ coefficient (as in the page 38 fix) and compare.

---

## Stage 2 — Spinor-Valued Weyl CA (Pages 38–39)

> **Equation correction (2026-05-13):** The original transcription of the page 38 boxed finite-difference equations was missing the imaginary factor `i` on the y-derivative terms. The corrected equations (consistent with the PDE on the same page and with the Pauli matrix σ_y) are:
>
> $$f(\ell,m,n,t+1) - f = -\tfrac{1}{2}(f_{\ell,m,n+1} - f_{\ell,m,n-1}) - \tfrac{1}{2}(g_{\ell+1} - g_{\ell-1}) + \tfrac{i}{2}(g_{\ell,m+1} - g_{\ell,m-1})$$
>
> $$g(\ell,m,n,t+1) - g = -\tfrac{1}{2}(f_{\ell+1} - f_{\ell-1}) - \tfrac{i}{2}(f_{\ell,m+1} - f_{\ell,m-1}) + \tfrac{1}{2}(g_{\ell,m,n+1} - g_{\ell,m,n-1})$$
>
> The `i` on the y-derivative arises directly from σ_y = [[0,−i],[i,0]] in the Weyl equation ∂ψ/∂t = −σ·∇ψ.

**Physics:** The Dirac reduction. Each cell carries a 2-component complex spinor $\psi = (f, g)$. The update rule is first-order in time (depends only on $t$, not $t-1$):

$$f(\ell,m,n,t+1) = f(\ell,m,n,t)
  - \tfrac{1}{2}\bigl(f(\ell,m,n{+}1,t) - f(\ell,m,n{-}1,t)\bigr)
  - \tfrac{1}{2}\bigl(g(\ell{+}1,m,n,t) - g(\ell{-}1,m,n,t)\bigr)
  + \tfrac{i}{2}\bigl(g(\ell,m{+}1,n,t) - g(\ell,m{-}1,n,t)\bigr)$$

$$g(\ell,m,n,t+1) = g(\ell,m,n,t)
  - \tfrac{1}{2}\bigl(f(\ell{+}1,m,n,t) - f(\ell{-}1,m,n,t)\bigr)
  - \tfrac{i}{2}\bigl(f(\ell,m{+}1,n,t) - f(\ell,m{-}1,n,t)\bigr)
  + \tfrac{1}{2}\bigl(g(\ell,m,n{+}1,t) - g(\ell,m,n{-}1,t)\bigr)$$

In compact notation using NumPy array rolls:

```python
import numpy as np

def weyl_step(f, g, c=0.5):
    """One time step of the massless Weyl CA (page 38).
    f, g: complex128 arrays of shape (Lx, Ly, Lz)
    c: lattice speed-of-light factor (stability threshold ~0.43 per page 39)
    """
    f_new = (f
             - c * (np.roll(f,  -1, axis=2) - np.roll(f,  1, axis=2))
             - c * (np.roll(g,  -1, axis=0) - np.roll(g,  1, axis=0))
             + c * 1j * (np.roll(g, -1, axis=1) - np.roll(g,  1, axis=1)))

    g_new = (g
             - c * (np.roll(f,  -1, axis=0) - np.roll(f,  1, axis=0))
             - c * 1j * (np.roll(f, -1, axis=1) - np.roll(f,  1, axis=1))
             + c * (np.roll(g,  -1, axis=2) - np.roll(g,  1, axis=2)))

    return f_new, g_new
```

**Experiments:**
1. Sweep `c` from 0.1 to 0.6; measure max amplitude over 100 steps to map the CFL stability boundary.
2. Confirm that `c ≈ 0.43` is the marginal stable value (reproducing the page 39 observation).
3. Initialize with a circularly-polarized pulse; verify the two helicity components separate.
4. Measure probability density $|\psi|^2 = |f|^2 + |g|^2$ and verify approximate conservation (the equation is unitary in the continuum; numerical unitarity degrades with large `c`).

---

## Stage 3 — Numerical Stability Sweep (Page 39 Verification)

The notebook notes: "it interestingly seems to stabilize at ~0.43."

In Courant–Friedrichs–Lewy (CFL) terms, the stability criterion for the centered-difference Weyl equation in 3D is:

$$c \leq \frac{1}{\sqrt{d}}$$

where $d$ is the spatial dimension. For $d = 3$: $c \leq 1/\sqrt{3} \approx 0.577$. The author's observed value of 0.43 is plausibly the empirical CFL number for the specific initialization used (a sharply-peaked pulse, not a smooth plane wave).

> **Simulation result (2026-05-13):** The explicit-Euler Weyl scheme is in fact *unconditionally unstable* — every c value diverged over 200 steps. The notebook's ~0.43 observation reflects the divergence rate being slow enough to stay bounded for a small number of steps (the author ran ~10 steps). The ~0.43 threshold is real but is the boundary between "blows up in a few steps" and "blows up more slowly", not a true stability boundary. True stability requires a unitary integrator — see Stage 2b (Split-Step) below.

**Output:** A plot of $\max|\psi|$ after $N$ steps vs. `c`, with the analytic CFL bound marked.

---

## Stage 2b — Split-Step FFT Propagator (Stability Fix)

The explicit-Euler update is unconditionally unstable because it is not unitary — it does not conserve $\|\psi\|^2$ exactly. The fix is to replace the time-step with the **exact propagator** for each Fourier mode.

### Derivation

The Weyl equation in Fourier space (per mode $\mathbf{k}$) is:

$$\frac{\partial \hat\psi}{\partial t} = -i(\boldsymbol\sigma \cdot \mathbf{k})\,\hat\psi$$

The exact solution over one time step $\Delta t = 1$ is:

$$\hat\psi(\mathbf{k},\,t+1) = e^{-i(\boldsymbol\sigma\cdot\mathbf{k})}\,\hat\psi(\mathbf{k},\,t)$$

Using the identity $e^{-i\theta(\boldsymbol\sigma\cdot\hat n)} = \cos\theta\,I - i\sin\theta\,(\boldsymbol\sigma\cdot\hat n)$ with $\theta = c\,|\mathbf{k}|$ and $\kappa = |\mathbf{k}|$:

$$U(\mathbf{k}) = \cos(c\kappa)\,I - \frac{i\sin(c\kappa)}{\kappa}(\boldsymbol\sigma\cdot\mathbf{k})$$

Expanded with $\boldsymbol\sigma\cdot\mathbf{k} = \begin{pmatrix} k_z & k_x - ik_y \\ k_x + ik_y & -k_z \end{pmatrix}$:

$$U = \begin{pmatrix}
\cos c\kappa - \dfrac{i\sin c\kappa}{\kappa}\,k_z & -\dfrac{i\sin c\kappa}{\kappa}(k_x - ik_y) \\[8pt]
-\dfrac{i\sin c\kappa}{\kappa}(k_x + ik_y) & \cos c\kappa + \dfrac{i\sin c\kappa}{\kappa}\,k_z
\end{pmatrix}$$

This matrix is exactly unitary ($U^\dagger U = I$) for all $c$ and all $\mathbf{k}$.

### Algorithm per step

1. $(\hat f, \hat g) \leftarrow \text{FFT}(f, g)$ along all spatial axes.
2. Apply $U(\mathbf{k})$ element-wise across the $k$-grid.
3. $(f, g) \leftarrow \text{IFFT}(\hat f, \hat g)$.

The speed parameter $c$ scales the phase as $c\kappa$ — equivalent to rescaling the lattice speed of light, consistent with the notebook's interpretation on page 39. At $\kappa = 0$ (the DC mode) $U = I$ by L'Hôpital's rule ($\sin(c\kappa)/\kappa \to c$).

### Implementation

`ca_core.py` exposes `weyl_step_2d_splitstep(f, g, c)` and `weyl_step_3d_splitstep(f, g, c)`. Both use `numpy.fft.fft2` / `fftn` and their inverses; no external dependencies. All stages of `run_simulation.py` use the split-step versions.

---

## Stage 4 — Graph-Based CA (Page 36)

**Physics:** "A CA with 3 connections can form a variety of different structures — Linear Strip, Circular Strip, Möbius Strip, or 2D lattice."

Move from a regular rectangular lattice to a NetworkX graph, where each node carries a spinor and edges define the neighborhood.

```python
import networkx as nx

def build_lattice_graph(Nx, Ny, valence=4):
    """Build a 2D grid graph (valence=4) or triangular graph (valence=6)."""
    if valence == 4:
        return nx.grid_2d_graph(Nx, Ny, periodic=True)
    elif valence == 3:
        # Hexagonal lattice - 3-connected
        return nx.hexagonal_lattice_graph(Nx, Ny, periodic=True)

def graph_weyl_step(G, psi, c=0.43):
    """Generalized spinor step over any graph G.
    psi: dict {node: np.array of shape (2,), complex128}
    Each edge contributes a sigma_i difference term; direction assigned by edge attribute.
    """
    psi_new = {}
    for node in G.nodes:
        delta = np.zeros(2, dtype=complex)
        for neighbor in G.neighbors(node):
            sigma = G[node][neighbor].get('sigma', np.eye(2))  # assigned at build time
            delta -= c * sigma @ (psi[neighbor] - psi[node])
        psi_new[node] = psi[node] + delta
    return psi_new
```

**Experiments (mapping to page 36):**

| Valence | Graph | Expected behavior |
|---|---|---|
| 2 | 1D ring | Unidirectional wave propagation |
| 3 | Hexagonal lattice | 2D wave with 6-fold symmetry; Möbius strip as a variant |
| 4 | Square lattice | Standard 2D Weyl propagation; matches Stage 2 |
| 4 (asymmetric) | Directed graph | One-way propagation; test the "asymmetric connections" note on page 36 |

---

## Stage 5 — Reversibility (Fredkin Correlation)

The Fredkin connection (`fredkin-correlation.md`) identifies two routes to a reversible CA:

1. **Carry prior state** (Fredkin/SALT): store both $\psi(t)$ and $\psi(t-1)$; update rule is $\psi(t+1) = F(\psi(t)) - \psi(t-1)$.
2. **Unitary evolution** (the notes' route): the Weyl update matrix is unitary; reversibility is automatic if the update is norm-preserving.

**Test:** Run 100 steps forward then 100 steps backward (negate $c$) and measure residual $\|\psi_\text{final} - \psi_\text{initial}\| / \|\psi_\text{initial}\|$.

> **Simulation result (2026-05-13, split-step):**
>
> | c | Residual |
> |---|---|
> | 0.20 | 6.4 × 10⁻¹⁴ |
> | 0.30 | 6.6 × 10⁻¹⁴ |
> | 0.43 | 5.8 × 10⁻¹⁴ |
> | 0.50 | 5.9 × 10⁻¹⁴ |
>
> All residuals are at the FFT floating-point noise floor (~10⁻¹⁴ for double precision on this grid). The Weyl CA is time-reversible to machine precision. Contrast with the explicit-Euler scheme at 200 steps, where residuals reached ~10³⁵ at c = 0.50.

---

## File Structure

```
ca-simulation/
├── stage1_scalar_wave.ipynb     # Page 37 — second-order scalar CA
├── stage2_weyl_spinor.ipynb     # Page 38 — spinor-valued Weyl CA
├── stage3_cfl_sweep.ipynb       # Page 39 — stability boundary
├── stage4_graph_ca.ipynb        # Page 36 — connection number / dimensionality
├── stage5_reversibility.ipynb   # Fredkin correlation — time reversal test
├── ca_core.py                   # Shared: weyl_step(), graph_weyl_step()
└── viz.py                       # Shared: animate_2d(), plot_stability_curve()
```

---

## Priority Order

1. **Stage 2 + Stage 3 first** — they directly verify the page 38–39 claims and are self-contained.
2. **Stage 1** — establishes the instability the notes describe, motivating the spinor fix.
3. **Stage 4** — page 36's dimensionality argument; requires NetworkX setup.
4. **Stage 5** — Fredkin verification; depends on Stage 2 working.

---

## Simulation Results

> Recorded 2026-05-13. All stages run to 200 time steps using the split-step FFT propagator.

### Stage 1 — Scalar Wave CA (Page 37)

Explicit-Euler scalar wave with periodic boundary, 64×64 grid, 200 steps.

| c | Behavior |
|---|---|
| 1.00 | Diverges immediately (peak capped at 10⁶) |
| 0.70 | Marginally stable at CFL limit; peak ~0.43 |
| 0.50 | Stable; pulse disperses, peak ~0.60 |
| 0.30 | Stable, slower dispersal; peak ~0.38 |

The 2D CFL bound for the explicit scalar scheme is $c \leq 1/\sqrt{2} \approx 0.71$, consistent with results.

### Stage 2 — Weyl Spinor CA (Pages 38–39, split-step)

64×64 grid, c = 0.43, snapshots at t = 0, 50, 100, 200. All three helicity configurations (left, right, mixed) propagate cleanly without blow-up. Norm conservation confirmed flat to double-precision across all c values tested.

### Stage 3 — CFL Stability Sweep (split-step, 200 steps)

All 18 c values from 0.10 to 0.61 remained stable. Peak amplitudes ranged from ~0.03 to ~0.31 (pulse spreading, not growth). This directly confirms that the split-step propagator is unconditionally stable — the notebook's ~0.43 threshold was an artifact of the explicit-Euler scheme.

### Stage 4 — Graph Topology

1D ring (2-connection): wave propagates cleanly around the ring over 200 steps, visible as diagonal bands in the spacetime diagram.

2D square grid (4-connection): Gaussian spinor pulse disperses outward symmetrically, snapshots at t = 0, 50, 100, 200 show progressive spreading.

### Stage 5 — Reversibility

100 steps forward + 100 steps backward. All c values returned residuals of ~6 × 10⁻¹⁴ — consistent with double-precision FFT noise, not physics. The Weyl CA is time-reversible to machine precision, confirming the unitary character of the split-step propagator and supporting Fredkin's reversibility requirement from first principles.

---

## Open Questions

- Can a glider (stable localized propagating structure) be found in the 3D spinor CA? This would correspond to the "elementary particle as stable pattern" idea from the Wolfram-Fredkin line.
- Does the graph topology measurably affect the effective speed of light? Page 36 suggests it should. The 1D ring result (200 steps) shows clean propagation but has not yet been compared quantitatively against the 2D result.
- The notebook's page 39 observation (~0.43 stabilization) is now understood as an empirical artifact of the explicit-Euler scheme. A write-up of this result — contrasting the two integrators — would be a self-contained addition to the notes.
- Extension to massive Dirac equation: add a mass term $m\beta\psi$ to the Weyl update. In split-step, this adds a rotation in spinor space between spatial propagation steps.

---

*Drafted 2026-05-13. Updated with implementation and simulation results 2026-05-13. Companion to `page35-cellular-automata-research.md`, `fredkin-correlation.md`, `ca-forces-integration.md`.*
