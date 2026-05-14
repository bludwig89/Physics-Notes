# CA Simulation — Next Steps Implementation Plan

Plan to implement the five "Next Steps" items listed in `ca-reference.md`. Grouped into three phases by theme; ordered so earlier phases produce tools the later phases depend on.

*Drafted 2026-05-14, after the dispersion-verification work landed.*

---

## Phase A — Visualization (items 1 and 5)

The two visualization items go together: item 5 ("spinor states as colors") is the encoding; item 1 ("particle/wave passing through the field") is the rendered output that uses that encoding.

### A1. Bloch-sphere color encoding for the spinor field

**Goal.** Map the four real numbers per cell — Re(f), Im(f), Re(g), Im(g) — to a single color so a 2D heatmap shows spinor orientation, not just density.

**Method.** A spinor $(f,g)$ up to overall phase and normalization defines a point on $\mathbb{CP}^1 \cong S^2$ (the Bloch sphere). Standard parameterization:

$$\theta = 2\arctan(|g|/|f|), \qquad \phi = \arg(g) - \arg(f)$$

Map $(\theta, \phi)$ to a color: hue from $\phi$, lightness from $\cos\theta$, optionally saturation from $|\psi|^2$ so unoccupied cells appear black.

**Deliverable.**
- New function `spinor_to_rgb(f, g)` in a new file `ca-simulation/spinor_color.py`.
- A test rendering of the three helicity initial conditions (left / right / mixed Gaussian) side by side. Left and right should be solid colors of opposite hue; mixed should show a definite intermediate hue.

**Effort.** Small. ~30 lines plus a matplotlib test plot.

**Risk.** Low. The math is standard. The only judgment call is the color map for the Bloch sphere — start with the HSL parameterization above, switch to a colorblind-friendly scheme later if needed.

---

### A2. Animated particle/wave propagation

**Goal.** Build animations showing |ψ|² and the Bloch-sphere coloring evolving through time, for both 2D and 1D-spacetime views.

**Method.**
- **2D field over time.** Frame loop over n_steps; each frame is the Bloch-coloring of (f,g) on the lattice. Output as MP4 (matplotlib FuncAnimation) and a static "strip" image showing 4–6 evenly-spaced frames. Mirrors Stage 2 / Stage 4 but in color rather than scalar density.
- **1D spacetime diagram with color.** Re-do the existing Stage 4 (1D ring) spacetime plot using the Bloch coloring instead of |ψ|². This is the "graph" view — time along one axis, lattice position along the other, color showing spinor orientation. Reveals chirality / helicity structure that the existing intensity-only plot hides.
- **Graph-network view.** Use NetworkX (already in `requirements.txt`) to draw the lattice as a node-edge graph and color each node by Bloch coloring. Useful as a sanity check on small lattices (8×8 or 16×16) — confirms the "graph" framing the integration doc emphasizes.

**Deliverable.**
- `run_simulation.py` gains a new Stage 7 (visualization). Outputs:
  - `stage7_bloch_evolution_2d.mp4`
  - `stage7_bloch_strip_2d.png`
  - `stage7_spacetime_color_1d.png`
  - `stage7_graph_network.png`

**Effort.** Medium. The 2D animation is straightforward; the graph-network drawing needs care to stay legible past L=16.

**Risk.** Low. Visualization only — does not change the propagator.

---

## Phase B — Measurement (items 2 and 3)

Items 2 and 3 are both about characterizing the existing CA — measuring what it actually does rather than extending it. They're cheap because they run over the existing split-step propagator.

### B1. Speed-of-light measurement: c as structure vs measurement (item 3)

**Goal.** Answer the question the reference poses: is $c$ a structural element of the lattice, or a measurement of lattice connections?

**Method.** Group-velocity measurement. Set up a narrow-band Gaussian wave packet centered at wavevector $\mathbf{k}_0$:

$$\psi(\mathbf{x}, 0) = h_+(\mathbf{k}_0)\,e^{i\mathbf{k}_0\cdot\mathbf{x}}\,\exp\!\left(-\frac{|\mathbf{x}-\mathbf{x}_0|^2}{2\sigma_x^2}\right)$$

Propagate, then track the centroid $\langle \mathbf{x}\rangle(t) = \sum_\mathbf{x} \mathbf{x}\,|\psi(\mathbf{x},t)|^2 / \sum_\mathbf{x} |\psi(\mathbf{x},t)|^2$. The group velocity is $\mathbf{v}_g = d\langle\mathbf{x}\rangle/dt$.

For the massless Weyl dispersion $\omega = c|\mathbf{k}|$ we have $\mathbf{v}_g = c\,\hat{\mathbf{k}}$ — speed exactly $c$, direction along $\mathbf{k}_0$.

**Predicted outcome (already implied by the dispersion verification).** $|\mathbf{v}_g| = c$ to machine precision for narrow-band packets, independent of position or lattice neighbors. This shows $c$ is *structural* in the sense that it is built into the propagator $U(\mathbf{k})$, and *measurable* in the sense that any localized excitation moves at exactly that speed.

**Deliverable.**
- New function `measure_group_velocity` in `ca_core.py`.
- A new section in `ca-reference.md` recording the measurement and concluding: $c$ is built into the propagator's $\cos(c\kappa)$ / $\sin(c\kappa)$ structure (structural), and observable as the centroid speed of any wave packet (measurable). These are the same number; the apparent "or" in the question is a false dichotomy.

**Effort.** Small. ~50 lines including a plot.

**Risk.** Low. The result is essentially predetermined by the analytic dispersion, but the measurement makes the equivalence concrete.

---

### B2. Minimum size / structure (item 2)

**Goal.** Find the smallest meaningful lattice and the smallest meaningful wave packet — the CA equivalents of a minimum length scale.

**Method.** Two sweeps.

1. **Minimum lattice size L.** Hold $\sigma = 3$ and $c = 0.5$ fixed. Run a Gaussian helicity-left packet on $L \times L$ lattices for $L \in \{4, 6, 8, 12, 16, 24, 32\}$. For each $L$, propagate 100 steps and measure (a) norm conservation, (b) deviation from the analytic group velocity $c$, (c) packet width broadening relative to free-space prediction.
   - Expected: small $L$ shows artifacts from periodic wraparound (the packet meets itself). Recover free behaviour above some $L_{\min}(\sigma)$.

2. **Minimum packet width σ.** Hold $L = 32$ fixed. Vary $\sigma \in \{0.5, 1.0, 1.5, 2.0, 3.0, 5.0\}$. Measure how much of the spectrum exceeds the Nyquist cutoff $|\mathbf{k}| < \pi$ as a function of $\sigma$.
   - Expected: $\sigma < 1$ excites modes near Nyquist where the lattice dispersion stops matching the continuum Weyl dispersion. This sets a minimum-particle-size scale: roughly $\sigma \gtrsim 1$ in lattice units.

**Deliverable.**
- New function `size_sweep` in `ca_core.py` and a new Stage 8 in `run_simulation.py`.
- Output: `stage8_minimum_size.png` with two subplots (L sweep, σ sweep) plus a concise reference-doc paragraph stating the empirical thresholds.

**Effort.** Small to medium. The sweeps are slow-but-trivial; the analysis is the work.

**Risk.** Low. Result interpretation is honest: this measures lattice-artifact-free regimes, not "fundamental quantum-gravity minimum length." Worth flagging that distinction in the writeup.

---

## Phase C — Curvature and backreaction (item 4)

This is the genuinely speculative one. The reference flags it as a current limitation, and `ca-forces-integration.md` already discusses why it's hard (it is the "graph topology + dynamic geometry" item in that doc's roadmap). Plan only outlines the smallest viable first step.

### C1. Position-dependent c — refractive-index analog (no backreaction yet)

**Goal.** Allow $c$ to vary across the lattice as a fixed field $c(\mathbf{x})$, decoupled from $\psi$. This is the optics analog of a refractive index, not real GR curvature, but it is the cleanest test that the split-step approach can accommodate a spatially-varying speed at all.

**Method.** Operator splitting. One timestep becomes a fractional-step:
1. Apply the kinetic propagator with fixed $c_0$ (the split-step in Fourier space).
2. Apply a position-space phase correction proportional to $(c(\mathbf{x}) - c_0)\cdot$(some operator).

The cleanest version: in the limit of small spatial variation, replace each per-cell propagator argument from $c_0\kappa$ to $c(\mathbf{x})\kappa$. The honest implementation requires Trotter-splitting the kinetic and "potential" parts, which has a $O((dt)^2)$ Trotter error. Worth stating upfront.

**Deliverable.**
- New function `weyl_step_varc_2d` in `ca_core.py`.
- A two-region test: $c(\mathbf{x}) = c_0$ on the left half, $c_0/2$ on the right. Demonstrate that a wave packet refracts when it crosses the boundary, with refraction angle matching Snell's law for the analog refractive index.
- Reference-doc section flagging the Trotter error and the gap between "refractive-index analog" and "GR backreaction."

**Effort.** Medium. The function itself is small; the test and writeup take longer.

**Risk.** Medium. Trotter error is real and could be confused with physical effects. Need to compare against the small-step limit ($dt \to 0$ via multiple sub-steps) to bound it.

### C2. Backreaction — field-dependent c (genuine open question)

**Goal.** Make $c$ depend on local $|\psi|^2$ — the simplest nonlinear coupling. This is the CA stand-in for "energy curves spacetime."

**Status: design only, no implementation in this plan.** This breaks linearity, unitarity in the standard sense, and the Fourier-space exact propagator. It opens the actual research question — how to add gravity-like backreaction without losing the conservation laws — which is the same question Sachs (notebook pages 9–34) and modern LQG/CDT/Wolfram programs are still working on.

The honest deliverable here is a *design note*, not an implementation: a `ca-backreaction-design.md` that lists candidate coupling forms (refractive-index proportional to $|\psi|^2$; metric perturbation $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}[\psi]$ with $h$ small; graph-rewrite rules triggered by local density thresholds) and the conservation-law problem each introduces.

**Effort.** Open. The design note is a day; an implementation is a research project.

**Risk.** High. This is where the existing literature has not converged.

---

## Phase D — Mass term (Weyl → Dirac)

The full implementation plan for this lives in `ca-dirac-gravity-plan.md` (Stage D1). Summarized here so the next-steps sequence is complete.

### D1. Dirac CA on the flat lattice

**Goal.** Extend the 2-component Weyl spinor to a 4-component Dirac spinor $\Psi = (\eta, \chi)$ in the Weyl/chiral representation, adding a mass coupling between the two halves.

**Method.** The Dirac Hamiltonian in Fourier space is the constant $4\times 4$ matrix:

$$H_D(\mathbf{k}) = c\,\boldsymbol{\alpha}\cdot\mathbf{k} + m c^2\,\beta$$

with dispersion $E(\mathbf{k}) = \sqrt{c^2|\mathbf{k}|^2 + m^2 c^4}$. The split-step propagator generalizes directly:

$$U_D(\mathbf{k}) = \cos(E\Delta t)\,I_4 - i\,\frac{\sin(E\Delta t)}{E}\,H_D(\mathbf{k})$$

Setting $m = 0$ block-diagonalizes $H_D$ into two decoupled Weyl propagators — the regression test.

**Deliverable.**
- `dirac_step_2d_splitstep` / `_3d` in `ca_core.py`.
- `verify_dirac_dispersion_*` patterned on the existing Weyl verifier; expected residual at machine precision.
- Zitterbewegung test: a localized non-eigenstate packet's centroid oscillates at frequency $\sim 2mc^2$ — the cleanest "mass is real" observable.

**Effort.** Small to medium. ~150 lines plus tests.

**Risk.** Low. Closed-form physics; direct extension of the existing Weyl architecture.

**Reference.** Notebook pages 38 (Weyl factorization), 59–60 (Dirac representation choices), 81–88 (plane-wave solutions in Weyl rep). Full plan in `ca-dirac-gravity-plan.md`.

---

## Phase E — Gauge phases (U(1) electromagnetic, SU(2) weak)

Adds internal gauge structure on top of the Dirac field. Builds on Phase D — the spinor must be Dirac (or at least chirality-split Weyl) before SU(2) can act on "one helicity half" the way the Standard Model demands.

### E1. U(1) electromagnetic phase

**Goal.** Couple the Dirac field to a U(1) gauge field $A_\mu(\mathbf{x})$ via minimal coupling $\partial_\mu \to \partial_\mu - iq A_\mu$.

**Method.** Per-cell gauge field $A_\mu(\mathbf{x})$, four real numbers per lattice site (one per spacetime direction). Trotter-split the timestep:
1. Apply the Phase D kinetic propagator (Dirac in flat space).
2. Apply a per-cell phase correction: $\Psi(\mathbf{x}) \to e^{-iq A_0(\mathbf{x})\Delta t}\,\Psi(\mathbf{x})$, and similarly for the spatial components folded into the kinetic step.

Static $A_\mu$ first (external field, no Maxwell evolution). Tests: hydrogen-like bound-state spectrum for $A_0 = -e/r$; Aharonov–Bohm phase pickup around a flux tube.

**Then dynamic $A_\mu$.** Evolve the gauge field via Maxwell's equations sourced by the Dirac current $j^\mu = \bar\Psi\gamma^\mu\Psi$. This is QED on a lattice (lattice QED has a substantial literature; the CA framing is just a specific discretization choice).

**Deliverable.**
- `dirac_step_u1_2d_splitstep` taking an additional $A_\mu$ array.
- Static-field tests with analytic comparisons.
- A separate `maxwell_step_2d` for the photon field, then a coupled run.

**Effort.** Medium. ~300 lines plus the Maxwell side.

**Risk.** Low to medium. The minimal-coupling implementation is standard; the Maxwell back-coupling needs care so charge is conserved exactly.

**Reference.** `ca-forces-integration.md` ("EM lives as a U(1) phase carried by the spinor state at each node"). Notebook pages 1–8 already work out the canonical-quantization scaffolding that grounds this.

### E2. SU(2) weak isospin (one chirality only)

**Goal.** Add an SU(2) gauge field $W^a_\mu(\mathbf{x})$ that acts on the *left-chirality* component of the Dirac spinor only — the parity-violating coupling of the Standard Model.

**Method.** Extend the cell state to carry isospin: $\eta(\mathbf{x})$ becomes a doublet $\eta_L(\mathbf{x}) = (\eta_\nu, \eta_e)$, while $\chi(\mathbf{x})$ stays a singlet (with $\nu_R$ optionally retained per notebook page 62). The gauge field $W^a_\mu$ ($a = 1, 2, 3$) is three real numbers per lattice site per spacetime direction, valued in the Lie algebra $\mathfrak{su}(2)$.

The minimal-coupling extension is per-cell multiplication by an SU(2) matrix:

$$\eta_L(\mathbf{x}) \to \exp\!\bigl(-i g\,W^a_\mu(\mathbf{x})\,\tau^a\,\Delta t\bigr)\,\eta_L(\mathbf{x})$$

with $\tau^a = \sigma^a/2$ the SU(2) generators. The right-handed $\chi$ is untouched.

**Deliverable.**
- Extended state object: $\Psi = (\eta_L^\nu, \eta_L^e, \chi_R^\nu, \chi_R^e)$ per cell (8 complex numbers, or 4 if neutrino is purely left-handed).
- `dirac_step_su2_2d_splitstep` taking a $W^a_\mu$ array.
- Test: parity-violating decay analog — a left-handed packet couples to $W$; a right-handed one of the same wavevector does not. Should reproduce the (1 − γ⁵) projector behaviour.

**Effort.** Medium to large. ~500 lines plus the gauge-field dynamics.

**Risk.** Medium. The chirality-projection part is bookkeeping; the gauge-field self-coupling (the SU(2) is non-Abelian) needs a careful discretization that preserves gauge invariance to machine precision.

**Reference.** Notebook page 60 (Ludwig's independent guess that *one helicity half* carries an SU(2) symmetry broken to U(1) — strikingly close to the standard electroweak story); pages 61–66 (Weinberg–Salam without Higgs); page 77 (program statement). `ca-forces-integration.md` ("SU(2) on one chirality half of the spinor").

### E3. Electroweak unification (design only)

**Goal.** Combine E1 and E2 into the $SU(2)_L \times U(1)_Y$ structure of the Standard Model, with the photon $A_\mu$ and $Z_\mu$ emerging from a rotation of $W^3_\mu$ and the U(1) hypercharge field $B_\mu$ by the Weinberg angle.

**Status: design only, no implementation in this plan.** The Higgs mechanism that gives the W and Z their masses is the genuine open question — notebook pages 62–66 ("Weinberg–Salam without Higgs") explore one route but flag the unwanted factor-of-2 in the kinetic Lagrangian (page 70). A CA implementation has to take a stance on mass generation: (a) put W/Z masses in by hand (cheating, but works as engineering); (b) implement a Higgs-like scalar field that breaks the symmetry (research); (c) try the chirality-flipping mass term in E2 as a stand-in (Ludwig's page-60 speculation; would need verification).

The honest deliverable is a `ca-electroweak-design.md` analogous to the C2 / D3b notes, listing the three mass-generation paths and what each would cost.

**Effort.** Design note: a day or two. Implementation: open research.

**Risk.** High. Not because the math is hard but because mass generation in the Standard Model is the part the notebook itself is uncertain about.

---

## Cross-cutting work

### Honest accounting of physics_notes_pages references

The reference doc says "use physics_notes_pages documents for reference if applicable." Two relevant places in the transcribed pages:

- **Pages 1–34** (Sachs unification): The covariant-derivative / spin-connection apparatus from these pages is the standard route from flat-space spinor fields to curved-space ones. If Phase C escalates beyond the refractive-index analog, the Sachs material is the natural template — $\Omega_\mu$ becomes a per-cell connection field carried alongside the spinor.
- **Pages 38, 59–60, 81–88** (Weyl factorization, complex mass, Dirac plane-wave solutions): the physics that grounds Phase D. The Dirac extension is worked out in detail in `ca-dirac-gravity-plan.md`.
- **Pages 60–72, 77, 89–90** (electroweak without Higgs, V–A current, fermion-state table): the source material for Phase E. Ludwig's page-60 speculation that one helicity half carries an SU(2) symmetry broken to U(1) is independently very close to the Standard Model electroweak structure, and it is the natural CA framing for the gauge phases.

### Maximum-density section in `ca-reference.md`

A small documentation tightening identified in an earlier review: the "maximum density (black holes)" section currently lists "bounded density" and "information never destroyed" as separate observations. They are the same statement (exact unitarity ⇒ global norm fixed ⇒ max single-cell density finite). Worth collapsing into one bullet to tighten the argument. Two-minute edit; defer until Phase A lands so the section can also reference the new visualizations.

---

## Summary table

| Phase | Item | Map to reference Next Steps / source doc | Effort | Risk |
|---|---|---|---|---|
| A1 | Bloch-sphere coloring | #5 | S | Low |
| A2 | Animated propagation + graph view | #1 | M | Low |
| B1 | Group-velocity measurement | #3 | S | Low |
| B2 | Min-size / min-σ sweeps | #2 | S–M | Low |
| C1 | Position-dependent c (refractive analog) | #4 (first step) | M | Med |
| C2 | Backreaction design note | #4 (open) | open | High |
| D1 | Mass term / Dirac propagator | `ca-dirac-gravity-plan.md` Stage D1 | S–M | Low |
| E1 | U(1) electromagnetic phase | `ca-forces-integration.md`; notebook 1–8 | M | Low–Med |
| E2 | SU(2) weak isospin (left-chirality only) | `ca-forces-integration.md`; notebook 60–66 | M–L | Med |
| E3 | Electroweak unification design note | notebook 62–70 | open | High |

Recommended order: A1 → A2 → B1 → B2 → D1 → C1 → E1 → E2 → C2 → E3. The reordering puts D1 (mass) before C1 (curvature) because the Dirac propagator is needed for the equivalence-principle test in Stage D2 of the Dirac/gravity plan. E1 and E2 can run in parallel once D1 is in.

---

## Notes on what's *not* in this plan

- **Strong interaction (SU(3) color).** The "trivalent graph or 3-valued internal state" question in `ca-forces-integration.md` is the relevant open issue, and neither route has a clean CA derivation today. Deferred.
- **Second quantization / lattice QFT.** Phases D and E build single-particle relativistic QM with classical gauge fields. Promoting $\Psi$ to an operator-valued field $\hat\Psi$ — and $A_\mu$ likewise — is a separate (much larger) project. Notebook pages 41–56 are the entry point for this when it is taken up.
- **3D Bloch-coloring visualization (Phase A could be extended).** 3D volume rendering is much more work and not strictly needed to answer reference-doc item 5; deferred.
- **Higher-order Trotter splitting for Phases C1, D2, E1, E2.** Only relevant if the first-order error proves problematic on the test geometries.
- **Dynamic graph topology** (Wolfram-style hypergraph rewriting). The lattice stays a fixed regular grid throughout; the "curve" lives in fields on the lattice (metric, gauge connections), not in the lattice itself.
