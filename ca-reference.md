# Weyl Spinor Cellular Automaton — Reference

*Based on physics notebook pages 35–39, Mark Ludwig (2007–08). Implementation in `ca-simulation/ca_core.py`.*

---

## External cross-reference (added 2026-05-15)

### Bisio, D'Ariano, Perinotti, Tosini (2015, 2016); Raynal (2017) — *QCA framework*

Detailed comparison in `qca-papers-1-4-overview.md`. Most directly relevant observations for the implementation in `ca_core.py` / `ca_dirac.py`:

- **The 2D square-lattice Weyl QCA in our split-step propagator is the small-$\mathbf{k}$ linearization** of the unique 2D QCA derived in Bisio *et al.* 2015 Eq. 16, $\omega = \arccos(c_x c_y)$ with $c_i = \cos(k_i/\sqrt 2)$. Our $\omega = c|\mathbf{k}|$ holds only for $|\mathbf{k}|\ll 1$; non-trivial QCA phenomenology (frequency-dependent $c$, Klein paradox shape, cosmic-ray spreading) lives in the higher-$|\mathbf{k}|$ corrections we have not yet measured.
- **The 3D simple-cubic lattice in `ca_core.py` is not the unique non-trivial 3D QCA.** Papers 1 (Bisio *et al.* 2015) and 2 (Raynal 2017) prove that the unique $s=2$ 3D QCA satisfying linearity / unitarity / locality / homogeneity / isotropy lives on the **body-centred cubic (BCC) lattice** with 8 generators (regular tetrahedron + dual). On a simple-cubic 3D lattice only the trivial automaton is admitted. V6 in the overview document proposes a BCC implementation as a regression target.
- **The Dirac coupling parameter satisfies $n^2 + m^2 = 1$ — *landed in code 2026-05-18 per Finding 9*.** Paper 1 Eq. 23 and Paper 2 Eq. 75 give the unique form $D_{\mathbf{k}} = \mathrm{diag}(nA_{\mathbf{k}}, nA_{\mathbf{k}}^*) + \mathrm{antidiag}(im I, im I)$ with $n^2 + m^2 = 1$, so the dimensionless mass is bounded by 1.  `ca_dirac.py::dirac_step_2d_splitstep` now builds the exact single-tick 4×4 unitary with $W_k$ from `ca_core_exact.exact2d_unitary` on the upper-left block and $W_k^\dagger$ on the lower-right (the form forced by unitarity).  The `c` argument is removed everywhere; kinetic coefficient $n = \sqrt{1-m^2}$ is derived internally.  Dispersion $\omega_k = \arccos(\sqrt{1-m^2}\,c_x c_y)$ at machine precision; zitterbewegung target $2\arcsin(m)$ replaces the old linearized $2m$.
- **The transition matrix at the centre of the primitive cell must vanish.** Paper 2's central result: $A_0 = 0$. Our split-step propagator should satisfy $U(\mathbf{k}=0) = I$ (no on-cell self-coupling); verify by inspection.
- **The photon is composite, not elementary.** Paper 1's Maxwell sector is built as a bilinear of two correlated Weyl fields (the De Broglie neutrino theory of light), and the free Maxwell equations emerge in the $|\mathbf{k}|\ll 1$ limit. Our model has U(1) as an externally-imposed gauge phase; implementing the composite-photon construction (test V4) is the single biggest physics extension available.
- **Lorentz covariance breaks at the Planck scale; DSR / deformed-Lorentz restores it.** Paper 4 Eq. 25: a non-linear representation $L_{\beta}^D = \mathcal D^{-1}\circ L_{\beta}\circ \mathcal D$ preserves the discrete dispersion $\omega(k) = \arccos(\sqrt{1-m^2}\cos k)$. Our 2D/3D lattices inherit the same Lorentz-breaking; no resolution is currently implemented.
- **Frequency-dependent $c(\mathbf{k}) \approx 1 \pm k/\sqrt 3$** at Planck scale (Paper 4 Eq. 23). This is *intrinsic* to the BCC dispersion — different from our Phase C1 variable-$c(\mathbf{x})$ (which is a position-dependent metric coefficient). The two are complementary, not redundant.

### Ostoma & Trushyk (1999), *Cellular Automata Theory and Physics* — summary in `ostoma-trushyk-1999-summary.md`; Reference Research Papers 3 (SR-only excerpt) and 6 (full 100-page treatise). Most directly relevant observations for the Weyl-spinor CA project:

- **Neighbor count vs lattice dimension**: $C_N = 3 C_{N-1} + 2$, so 1D = 2, 2D = 8, 3D = 26 neighbors. Our 2D/3D simulations use 4 and 6 neighbors (axis-only); a 26-neighbor stencil would more closely match the EMQG ontology and is worth piloting if isotropy artifacts appear.
- **Rule-space size**: $2^{2^{m+1}}$ for binary cells with $m$ neighbors → $2^{2^{27}}$ in 3D. Brute search for "the rule" is infeasible; targeted physics-motivated ansätze (Weyl/Dirac/Yukawa, our route) are the only practical path.
- **Photon = 1 cell/clock**: in the EMQG framing the maximum information-propagation rate per step **is** the speed of light. Our `c` parameter is the same dimensionless quantity; the CFL-like upper bound on stable explicit stepping in `ca_core.py` is the numerical analog.
- **Two-layer space-time**: the paper distinguishes absolute CA units (cell counts, clock-cycle counts) from measured units (meters, seconds). Our simulation is entirely in the absolute layer; relativistic effects (Lorentz transforms, dispersion measurements in B1) emerge from it as expected.
- **Raw vs measured $c$**: $c_{\text{measured}} = c_{\text{raw}} / n$ where $n$ is a vacuum index of refraction from photon-virtual-particle scattering. Suggests an experiment: introduce a uniform scattering term in `ca_core.py` and verify dispersion velocity scales by $1/n$ — a Fizeau analog within the simulation.
- **Equivalence-principle violation prediction**: at ~$10^{-40}$, far below any reachable simulation precision, but conceptually a falsifiable extension of GR. Not relevant to current Phase A–F tests.
- **F3 (Yukawa back-reaction) thematic alignment**: Ostoma–Trushyk's "masseon" coupling to the vacuum is conceptually parallel to F3's Φ ↔ Dirac coupling, though our implementation is purely the Standard-Model Yukawa, not their masseon proposal.

### Paper 6 — additional EMQG-specific observations relevant to Phase C1 / F3b (variable-$c$ branch)

Paper 6 (the full 100-page Ostoma–Trushyk treatise) adds the macroscopic EMQG framework that Paper 3 only references. The pieces that bear directly on `ca_curved.py` and the F3b gravitational-lensing demo:

- **Variable-$c$ as an *established published hypothesis*, not project-internal speculation.** Paper 6 Eqs. 18.51–18.52 give $c(t) = c(1 \pm gt/c)$ — a position- and direction-dependent local light speed near a mass, identical in form to the refractive-index profile used in `weyl_step_2d_varc_cayley`. The Phase C1 / F3b $c(\mathbf{x})$ ansatz is the same kind of model; what F3b lacks is a derivation of the depth profile $c(|\Phi|)$ from microscopic physics. Paper 6 supplies an external published target (modified Poisson equation 19.7) for that derivation.
- **EMQG weak-field equation: modified Poisson with retardation.** $\nabla^2\phi - c^{-2}\partial_t^2\phi = 4\pi G \rho$ (Paper 6 Eq. 19.7). The acceleration field $\mathbf{a} = \nabla\phi$ is what drives both inertia and gravity in EMQG, and is the gradient that would set the local $c$ profile in any EMQG-aligned `ca_curved.py` implementation. **Test V11 in `qca-papers-1-4-overview.md` proposes solving this equation on the lattice for a static spherical mass and feeding the result into the variable-$c$ stepper.**
- **Three mass definitions.** Inertial $m_i$ (resistance to acceleration via EM coupling to virtual vacuum), gravitational $m_g$ (graviton-mediated, almost equal to $m_i$), and "low-level mass charge" (pure graviton emission rate, not directly measurable). Our F3b uses a single mass parameter; no friction with this currently, but if F3b is ever extended to include differential-mass falling tests (paper's $10^{-40}$ WEP violation), the three-mass framework would be the natural starting point.
- **Equivalence principle as a derived coincidence, not a postulate.** The vacuum state appears the same in accelerated and gravitational frames with reversed acceleration vectors. Paper 6's derivation in §17.3 is purely verbal/heuristic; a lattice realisation would need both an inertial-EMQG sector (charged matter coupling to a charged-virtual-vacuum field) and a graviton sector (mass-charged matter coupling to a separate exchange field). Neither exists in `ca-simulation/`.
- **Photon and graviton both carry inertial/gravitational mass via $E/c^2$, but no low-level mass charge.** Resolves the canonical-quantum-gravity renormalization tangle (graviton-graviton self-coupling) by analogy with QED's photon non-self-coupling. Compatible with our model's treatment of U(1) and (eventual) gravitational sectors as separate per-cell phases.
- **Cosmology — Milne kinematic.** Paper 6 §20: matter moves outward through pre-existing flat low-level CA space; apparent expansion is the changing curvature of light's path through density-varying accelerated vacuum. Not relevant to any current Phase A–F test, but rules out any future test that assumes expanding-cell semantics in our lattice (consistent with our toroidal `L^3` topology).
- **Fizeau analog for the speed of light in vacuum**: Paper 6 Eq. 18.31 gives $v_c = c/n + (1 - 1/n^2)V$ for light through a medium of refractive index $n$ moving at velocity $V$. **Test V12** in the overview proposes running this in reverse: set up a linear $c(z)$ profile in `ca_curved.py` and verify the gravitational redshift $\Delta\nu/\nu \approx -|\nabla c|\,L/c$ falls out of the propagator's measured frequency shift. This would be a direct lattice check of Paper 6's central scattering claim.

---

## What this CA is

A **cellular automaton (CA)** is a grid of cells, each holding a value, updated simultaneously at every timestep by a fixed local rule. This CA propagates a two-component complex field (a **spinor**) on a regular lattice. The update rule is the discretized, massless **Weyl equation** — the equation governing massless spin-½ particles like neutrinos. Each timestep corresponds to one unit of discrete time; each cell corresponds to one unit of discrete space. The lattice is spacetime.

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

A scaling sweep at $c = 0.43$ (2026-05-14 rerun, complex128) confirms the residual is **precision-bound, not algorithmic**:

| $n$ steps (each direction) | Residual |
|---|---|
| 100 | $5.85 \times 10^{-14}$ |
| 500 | $2.95 \times 10^{-13}$ |
| 1000 | $5.92 \times 10^{-13}$ |
| 2500 | $1.48 \times 10^{-12}$ |
| 5000 | $2.96 \times 10^{-12}$ |

The residual scales linearly in $n$ at roughly $6 \times 10^{-16}$ per timestep — exactly one ulp of complex128 per round-trip FFT. Upgrading the working type to `longdouble` (80-bit) would buy about one extra decimal per step but is not worth the slowdown.

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
- **SI identification of $(a, \tau)$ is currently undefined.** The lattice cell distance $a$ in metres and tick $\tau$ in seconds have not been pinned down. The naive choice $a = \ell_P$, $\tau = t_P$ predicts a measured speed of light $c_\text{physical} = c/\sqrt d$ — in 3D, $1.732 \times 10^{8}$ m/s, or 0.5774× the observed value. All dimensionless lattice tests are unaffected; only lattice-to-SI absolute-magnitude conversions need the choice. See `findings.md` Finding 10 and `changelog.md` 2026-05-17 for the three internally consistent resolutions.

---

## Next Steps


- Build a represenation both visual and with graphs showing a particle and/or wave passing through the field.
- Determine structure and "minimum size".
- Determine how the speed of light is either a structure element or a measurement of the lattice connections.
- Continue figuring out the lattice topology and curvature in response to the field. Use physics_notes_pages documents for reference if applicable.
- Can the two spinor states of the CA be represented somehow in a 2 or 3-dimensional space with colors possibly?


*Last updated: 2026-05-15 — added QCA literature cross-reference (Bisio/D'Ariano/Perinotti/Tosini, Raynal); BCC vs simple-cubic divergence flagged for 3D code; composite photon construction noted as the largest available physics extension.*

---

## v2 layered build — what is exact vs machine-precision (2026-05-15)

Per CLAUDE.md's preference for distinguishing "exact" results (analytically derivable, no floating-point dependence) from "machine-precision" (correct to ε but accumulating round-off), the L1–L4 tests sort as follows.

### Exact (analytically zero or 1)
| Test | Result | Why exact |
|---|---|---|
| L1 — A_0 = I at k=0 (Paper 2 V7) | `(1+0j, -0j, -0j, 1+0j)` exact | At k=0 every cos = 1, every sin = 0; the BCC structure vector ñ vanishes identically |
| L2 — A_0 = I at k=0 (2D) | exact | Same reason as L1 |
| L1 — analytic 'u² + abs(n)² = 1' (with corrected ñ_y) | derived by direct expansion | The expansion `c_x² c_y² c_z² + ...` telescopes to `(c_x²+s_x²)(c_y²+s_y²)(c_z²+s_z²) = 1` (after cross-term cancellation) |
| L2 — analytic `u² + abs(n)² = 1` (2D) | derived | `(c_x²+s_x²)(c_y²+s_y²) = 1` by Pythagorean identity, no cancellation needed |
| L3 — composite-photon dispersion along (1,0,0) | residual 3.85e-15 | `2 arccos(cos(k/2/√3)·1·1) = k/√3` is an algebraic identity; FFT round-off is the floor |
| L3 — analytic `Ω_γ − k/√3 = k/18 + O(k²)` along (1,1,1) | derived | Direct Taylor expansion `u(k/2) ≈ 1 − k²/24 + k³/216 + ...`; reproduces measured `k/18` factor |
| L4 — vacuum c uniform | exact 0.0 | ρ=0 → FFT gives φ(k)=0 ∀k → c(x)=c_0 identically |

### Machine precision (correct to ε)
| Test | Result | Floor source |
|---|---|---|
| L1 — BCC unitarity across BZ | 7.85e-16 (4096 modes) | FFT round-off |
| L1 — analytic ω(k) = measured eigenvalue phase | 7.22e-16 | numpy.linalg.eig round-off |
| L1 — norm drift over 200 steps (16³) | 3.73e-14 | accumulating FFT round-off ~2e-16/step |
| L1 — single-step norm drift | 7.77e-16 | one FFT round-trip |
| L2 — BCC-2D unitarity across BZ (32×32) | 3.24e-16 | FFT round-off |
| L2 — norm drift over 200 steps (32×32) | 8.44e-15 | accumulating FFT round-off |
| L3 — transversality `2ñ·E = 2ñ·B = 0` | 4.58e-17 | projection round-off |

### Approximate but published targets
| Test | Result | Comparison |
|---|---|---|
| L1 — small-k Weyl regression at \|k\|=0.005 | 4.96e-04 | analytic prediction k²/24 ≈ 1e-6 along (1,1,1) gives leading O(k) correction k/18 ≈ 2.8e-4; measured 5e-4 is within the BCC anisotropy spread across 12 random directions |
| L2 — small-k linear ω = (1/√2)\|k\| at \|k\|=0.01 | 2.08e-06 | matches O(k²) scaling expected from 2D arccos lattice corrections |
| L2 — Δc/c at \|k\|=0.5 along (1,1) | −1.13% | matches Paper 4 Eq. 23 directional analog; zero along axes |
| L3 — composite-photon dispersion | 0.21% at \|k\|=0.05 | matches `k/18` analytic along (1,1,1) per Paper 1 |
| L4 — static Poisson Laplacian | 2.75% on 64² | finite-difference discretization error on a Gaussian source with σ=3 cells; expected scale ~(spacing/sigma)² |
| L4 — lensing scaling Δ(2M)/Δ(M) | 1.83 vs analytic 2.0 (8.5% off) | Newtonian-limit linearity; lattice 128×128, n_steps=80 |

### Combined test inventory (post-v2 build)

| Suite | Total | Exact | Machine ε | Approx (published targets) | Info-only |
|---|---|---|---|---|---|
| `run_phase_tests.py` (A–E) | 8/8 | E2 right leakage | D1 (5e-16), E1 (4.4e-16) | B1, C1, D1 zitterbewegung | — |
| `run_phaseF_tests.py` (F) | 5/5 | F1, F4 Φ=0 | F1 (8e-16), F4 η (7.6e-16) | F2 (0.1%), F3, F3b (Cayley 1.1e-15) | — |
| `run_L_tests.py` (L1–L4) | 17/17 | 3 (see above) | 7 (see above) | 7 (see above) | 1 (L3 curl) |
| **Total** | **30 / 30** | 6 exact | 11 at ε | 12 published-target | 1 info |

The "exact" column is the strongest claim available for a numerical lattice model: a result that comes out of the algebra without any floating-point contribution at all.

---

## 10× test execution — updates to the exactness inventory (2026-05-16, later)

Following the fresh-test pass at 10× scaled parameters (full table in `changelog.md` 2026-05-16 entry "10× test execution pass" and detailed findings in `findings.md` Findings 3–6), two new rows are added to the **exact algebraic** column of the inventory:

| Construct | Exactness | Where it lives |
|---|---|---|
| Goldstone dispersion $\omega = \|k\|$ on lattice (at $L\ge 640$) | **Exact algebraic** — residual / $(\|k\|\cdot\varepsilon_\text{double}) \le 0.88$ across measured modes | `ca_higgs.py::verify_higgs_dispersion_2d`; Finding 3 |
| Curl-residual leading coefficient $1/\sqrt{2d}$ for composite-photon bilinear on dimension-$d$ Weyl QCA | **Exact algebraic** — $d=2$ measured to 10 decimals on 2D-square, $d=3$ to 7 figures on BCC | `ca_maxwell.py` (3D), `ca_maxwell_2d.py` (2D); Findings 2 update + Finding 7 resolution |

And one row is added documenting a stability-bound match exposed by the 10× lattice:

| Construct | Status | Where it lives |
|---|---|---|
| Higgs KG sub-step CFL bound $dt_\text{sub} < 2/\sqrt{8+2\mu^2}$ | **Standard explicit-Verlet bound on 5-point 2D Laplacian** — empirical critical dt = 0.85–0.95 at L=320, μ²=0.5; F1 needs `n_phi_sub≥2` at the 10× bump | `ca_higgs.py::kg_step_strang`; Finding 4 |

The 10× pass also confirmed that the per-step FFT round-off floor is exactly 1 ulp of complex128, scaling as $\sqrt{N_\text{cells}}$ across the lattice and linearly in step count (Finding 5).

**Updated total:** 8 exact algebraic results (6 prior + 2 added).

---

## SI identification of $(a, \tau)$ — exact $\sqrt d$ factor at the lattice-to-SI boundary (2026-05-17)

Per `findings.md` Finding 10, the Weyl-QCA lattice light speed $c_\text{lat} = 1/\sqrt d$ is *dimensionless*. Converting it to SI requires a lattice spacing $a$ (metres) and tick $\tau$ (seconds):

$$c_\text{physical} \;=\; \frac{a}{\tau}\cdot c_\text{lat} \;=\; \frac{a}{\tau}\cdot\frac{1}{\sqrt d}.$$

Two new rows for the **exact algebraic** column:

| Construct | Exactness | Where it lives |
|---|---|---|
| Weyl-QCA lattice light speed $c_\text{lat} = 1/\sqrt d$ | **Exact algebraic** — Bisio *et al.* 2015 uniqueness result; verified to 10 decimals at $d=2$ (`ca_maxwell_2d.py`) and 7 figures at $d=3$ (`ca_maxwell.py`) | Findings 2, 7 |
| Lattice-to-SI mapping factor $\sqrt d$ from naive Planck identification $a = \ell_P,\,\tau = t_P$ | **Exact algebraic** — consequent of $\ell_P/t_P = c$ definitional identity; predicts $c_\text{physical} = c/\sqrt d$ in any $d > 1$ | Finding 10 |

The second row is a *decision point*, not a measurement: the SI identification is currently undefined in the project. Any future lattice-to-SI absolute-magnitude calculation (e.g., the L4 lensing absolute-coefficient extension) must declare which of three resolutions is in force — full menu in `findings.md` Finding 10. The $\sqrt d$ factor itself is exact algebraic; the choice is what to do with it.

**Updated total:** 9 exact algebraic results (8 prior + 1 added — the lattice-light-speed row formalises a result already implicit in Findings 2 and 7; the SI-mapping row is the new entry).

---

## Dirac stepper — exact-QCA form (2026-05-18, Finding 9)

`ca_dirac.py` now implements Paper 1 Eq. 23 directly.  Single-tick unitary:

$$D_k = \begin{pmatrix} n\,W_k & im\,I \\ im\,I & n\,W_k^\dagger \end{pmatrix},\qquad n^2 + m^2 = 1.$$

Dispersion $\omega_k = \arccos(n\,c_x\,c_y)$ with $c_i = \cos(k_i/\sqrt 2)$.  Spectral interpolation for arbitrary $dt$: $U(dt) = \cos(\omega\,dt)\,I + (\sin(\omega\,dt)/\sin\omega)\,(D_k - \cos\omega\,I)$.

New rows for the exactness inventory:

| Construct | Exactness | Where it lives |
|---|---|---|
| Exact-QCA Dirac dispersion $\omega = \arccos(\sqrt{1-m^2}\,c_x c_y)$, 2D | **Machine ε** — residual $3.9\times 10^{-16}$ at $m=0.3$ (L=64, n_steps=20) | `ca_dirac.py::verify_dirac_dispersion_2d`; Finding 9 |
| Zitterbewegung frequency $\omega_Z = 2\arcsin(m)$ | **Within FFT bin** — measured $1.04877$ vs $\pi/3 = 1.04720$ at $m=0.5$ (L=256, n_steps=2000, dt=0.5) | `ca_dirac.py::measure_zitterbewegung_freq_2d`; Finding 9 |
| F1 vacuum regression at exact-QCA $\Phi=v$ (η_diff vs constant-m Dirac) | **Machine ε** — $1.43\times 10^{-15}$ | `run_phaseF_tests.py::test_F1` |
| F4 symmetric regression at exact-QCA $\Phi=0$ (η vs `weyl_step_2d_arccos_splitstep`) | **Bit-for-bit zero** — exact-QCA Dirac at $m=0$ is diag$(W_k, W_k^\dagger)$, η-block equals the standalone 2D Weyl QCA exactly | `run_phaseF_tests.py::test_F4` |
| Aharonov-Bohm π-flux phase pickup under exact-QCA kinetic | **Machine ε** — $4.4\times 10^{-16}$ at L=128 | `run_phase_tests.py::test_E1` |

**API change.** The `c=` argument is removed from every Dirac stepper signature.  The kinetic coefficient is now $n = \sqrt{1-m^2}$ by the QCA admissibility constraint, derived internally from `m`.  Callers that previously passed `c=0.5, m=…` should now pass only `m=…`.  Variable-mass steppers (`*_varm_*`) take `m0` (baseline mass) instead.  See `changelog.md` 2026-05-18 entry for full call-site migration.

**Note on `W'_k`.** Finding 9 paraphrased the QCA literature as "$W_k^* = W_k(-\mathbf{k})$ on the lower-right".  Element-wise complex conjugation of the explicit 2D Eq. 16 unitary differs from the Hermitian conjugate; the form that closes the unitarity algebra (off-diagonal $D^\dagger D$ blocks vanish) is $W' = W_k^\dagger$.  Confirmed numerically: $\|D^\dagger D - I\|_\infty = 1.11\times 10^{-16}$ across the BZ.

**Does not yet close.** 3D-BCC Dirac stepper (no 3D code path); composite-photon derivation (V4); DSR / Paper 4 boost map (V8) — each is a separate piece of work tracked in `qca-papers-1-4-overview.md`.

**Updated total:** 9 exact-algebraic results + 1 machine-ε exact-QCA dispersion + 1 FFT-bin zitterbewegung row.

---

## Emergent-time roadmap T1–T2, T5 — exactness inventory (2026-05-18)

Rows added from the emergent-time gates (`ca-emergent-time-plan.md` §T1, §T2, §T5).

| Construct | Exactness | Where it lives |
|---|---|---|
| T1.A — lazy-vs-sync max field residual (Weyl 2D free) | **Bit-for-bit zero** — the lazy wrapper does not modify propagator output; bookkeeping-only laziness | `test_emergent_time_T1.py::test_T1A_weyl` |
| T1.A — lazy-vs-sync max field residual (Higgs Mexican-hat) | **Bit-for-bit zero** | `test_emergent_time_T1.py::test_T1A_higgs` |
| T1.A — lazy-vs-sync max field residual (F1 unified step) | **Bit-for-bit zero** | `test_emergent_time_T1.py::test_T1A_F1_unified` |
| T1.A — vacuum-cell residual floor (pure-vacuum Φ=v, Π=0 state) | **Machine ε** — $1.18\times 10^{-16}$ over 40 steps; ε=1e-13 sits 849× above the floor | `test_emergent_time_T1.py::test_T1A_eps_calibration` |
| T2.A — group velocity agreement, n-reading vs τ-reading (flat metric) | **Machine ε** — relative diff $5.75\times 10^{-16}$ | `test_emergent_time_shapiro.py::test_T2A` |
| T2.B — Shapiro tick-ratio, $N_{\text{phase, in}}/N_{\text{phase, out}}$ vs $c_{\text{in}}/c_{\text{out}}$ | **Exact algebraic** — algebraically follows from $\omega = c\cdot k$ and $c(\phi) = c_0/(1-2\phi/c_0^2)$; numerical residual $2.73\times 10^{-16}$ at L=128, k_mode=6 (on-grid) | `test_emergent_time_shapiro.py::test_T2B` |
| T2.C — Gravitational redshift $z = -2\phi_s/c_0^2$ from tick reading | **Exact algebraic** — substitution $z_\text{tick} = 1/r_s - 1$ with $r_s = c_s/c_0$ collapses to $-2\phi_s/c_0^2$ exactly; numerical residual $4.7\times 10^{-16}$ | `test_emergent_time_shapiro.py::test_T2C` |
| T5.A — vacuum-cell tick count exact zero (L=256, n=40) | **Bit-for-bit zero** — 80.4% of the lattice satisfies $N(\mathbf x) = 0$ exactly | `test_emergent_time_T5.py::test_T5A` |
| T5.C — asymmetric tick-clock ratio equals c-ratio | **Exact algebraic** — same algebra as T2.B; numerical residual $2.73\times 10^{-16}$ | `test_emergent_time_T5.py::test_T5C` |

And one row tracking implementation overhead:

| Construct | Status | Where it lives |
|---|---|---|
| T5.B — lazy-wrapper wall-clock overhead | **Bounded constant factor** — 9.3% / 10.3% / 13.0% at L ∈ {64, 128, 256}; bookkeeping-only, FFT cost dominates | `test_emergent_time_T5.py::test_T5B` |

**Updated total:** 13 exact-algebraic / bit-zero results (9 prior + 4 new: T1.A-Weyl, T1.A-Higgs, T1.A-F1-unified, T5.A), 2 machine-ε rows (T2.A, T2.B, T2.C, T5.C), 1 implementation-overhead row.

**Open question — T2.B "binary tick" vs "phase tick" ambiguity** in the proposition.  Resolved in `findings.md` Finding 11: both forms satisfy the proposition's $\|U\psi - \psi\| > \varepsilon$ criterion; the binary form is load-bearing for vacuum freezing (T5.A), the phase form is load-bearing for the Shapiro / redshift / asymmetric-clock ratios (T2.B, T2.C, T5.C).  Implementation: `ca_lazy.py::TickCounter` is the binary form; phase-tick is computed inline.  Promoting phase-tick to a first-class `PhaseTickCounter` class is a deferred follow-up.

**What did not match anything new:** every other 10× test reproduced the prior residual or improved monotonically with resolution; nothing in the new data resembled an approximation to an imaginary number, $\pi$, $e$, or any other transcendental constant. The matches that surfaced are all real-valued algebraic ($1/\sqrt 6$, $\varepsilon_\text{double}$, the CFL bound, $2mc^2$).

---

## Model-observations items 8–14 — new tests and what they measured (2026-05-16, later still)

Cleanup pass to address the cosmetic-but-load-bearing flags in `model-observations.md`. New observations to fold into the reference:

- **Strang composition of `unified_step` is empirically second-order in dt** (item 13).  Richardson ratio over $\Delta t \in \{1.0, 0.5, 0.25\}$ at fixed $T=8$ measured at $4.07$, exactly the $O(\Delta t^2)$ signature.  This is the first dt-scan in the suite; previously the unconditionally-stable propagator's exact-norm-preservation masked any order-of-accuracy bug.  Result: the Verlet-Strang composition behaves as advertised; no hidden first-order term.

- **Discrete Noether $\partial_t \rho + \nabla\!\cdot\!J = 0$ holds at $O(\Delta t^2)$ for the U(1)-coupled Dirac CA** (item 14).  Residual ratios at $\Delta t = \{0.20, 0.10, 0.05\}$: $4.05$ and $4.01$.  The lattice current built from the chiral-basis bilinears
  $$J^x = 2\,\mathrm{Re}(\eta_\uparrow^*\eta_\downarrow) - 2\,\mathrm{Re}(\chi_\uparrow^*\chi_\downarrow),\quad J^y = 2\,\mathrm{Im}(\eta_\uparrow^*\eta_\downarrow) - 2\,\mathrm{Im}(\chi_\uparrow^*\chi_\downarrow)$$
  with central-difference divergence satisfies the discrete continuity equation at the integrator's order.  Adds the **local** Noether identity to the suite; previously only the **integrated** total norm was tested.

- **SU(2) isospin rotation preserves $\rho$ at $4.4 \times 10^{-16}$ pointwise** (item 14b).  The per-cell unitary $\exp(-i g\,\boldsymbol{W}\!\cdot\!\boldsymbol{\tau}\,\Delta t)$ acts only on the doublet index, not on space; local density is preserved exactly by construction.  Documents the design contract.

- **F3b-scan: $|\Delta y(b)|$ scales as $1/b$ in the far-field $b > 2\sigma_\Phi$** (item 12; pending full run).  Per-run sanity (L=192, $b=60$): $\Delta y = -0.376$ cells with norm drift $1.0\times 10^{-14}$.  Power-law fit across five $b$ values is the verification target; passes if slope $\in [-1.4, -0.6]$.

These are additions to the exact-and-O(dt²) ledger; they do not change any of the prior-pass results.
