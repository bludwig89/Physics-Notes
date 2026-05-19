# Page 35 — Cellular Automata & Spacetime: Research Notes

Companion document to `physics_notes_pages_31-45.md`, page 35 speculation.

The author asked: *"Would it be possible to model spacetime geometry and elementary particle physics using cellular automata?"* and *"Has anything been written about this?"*

The notes appear to date from 2007–08. Much of the literature below postdates them, meaning the author was anticipating an active research direction rather than rediscovering a closed one.

---

## Core insight from the notes

> **Dependence implies neighborhood. Rules imply geometry.**

This is the exact organizing principle of the Wolfram Physics Project (2020) and is structurally compatible with Causal Set Theory.

---

## Published research in this direction

### Stephen Wolfram

- *A New Kind of Science* (2002) — extensive exploration of CA as a foundation for physics.
- **Wolfram Physics Project** (launched April 2020) — the direct descendant of page 35's speculation. Moved from rigid CA lattices to **hypergraphs**: nodes and links *are* spacetime; rewrite rules generate causal structure. Elementary particles appear as persistent localized propagating structures within the hypergraph.
- Reference: [wolframphysics.org — Elementary Particles](https://www.wolframphysics.org/technical-introduction/potential-relation-to-physics/elementary-particles/)

### Gerard 't Hooft

- *The Cellular Automaton Interpretation of Quantum Mechanics* (Springer, 2016).
- Argues quantum mechanics is the statistical description of a deterministic CA at the Planck scale.
- Reference: [Majorana tower and cellular automaton interpretation of QM](https://link.springer.com/article/10.1134/S0040577923020101)

### Causal Set Theory (Sorkin et al.)

- Initiated late 1980s by Rafael Sorkin; ongoing.
- Spacetime is a locally finite partially-ordered set ("causet").
- Directly addresses the author's worry about Lorentzian geometry: Lorentz invariance is preserved by **random Poisson sprinkling** of points, not a rigid lattice.
- References:
  - [Causal Sets — Wikipedia](https://en.wikipedia.org/wiki/Causal_sets)
  - [Surya, "The causal set approach to quantum gravity" (arXiv:1903.11544)](https://arxiv.org/abs/1903.11544)
  - [Geometry from order — Einstein Online](https://www.einstein-online.info/en/spotlight/causal_sets/)

### Quantum Cellular Automata / Quantum Walks

- Active research area; the discrete Weyl/Dirac equation derived on pages 37–39 is a **quantum walk**, provably equivalent to a Quantum Cellular Automaton in the continuum limit.
- Reference: [Farrelly, "A review of Quantum Cellular Automata," *Quantum* (2020)](https://quantum-journal.org/papers/q-2020-11-30-368/)

### Bridging CA and causal sets

- Tommaso Bolognesi, "Spacetime Computing: Towards Algorithmic Causal Sets with Special-Relativistic Properties" (2016) — uses Boolean networks (a CA generalization) to derive Lorentz-like behavior.
- Reference: [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-319-33924-5_12)

---

## Central obstruction the author already sensed

Page 35: *"Could they also generate a time coordinate?"*
Page 36: dimensionality is bounded by connection number.

Together these touch the field's hardest problem: a rigid CA lattice picks a preferred frame and breaks Lorentz invariance. The three modern routes around it:

1. **Hypergraph rewriting** (Wolfram) — geometry is emergent, not pre-imposed.
2. **Random sprinkling** (Sorkin) — statistical Lorentz invariance over discrete elements.
3. **Spinor-valued evolution** (the author's pages 37–39) — encode the Lorentz structure into the field values rather than the lattice; this is the QCA / quantum walk route.

---

## What the author did on pages 36–39

Without naming it as such, the author wrote a functional sketch of a quantum walk:

- **Page 36** — dimensionality from connection number (anticipates graph-based emergence).
- **Page 37** — finite-differenced scalar wave equation; identifies the second-order-in-time problem.
- **Page 38** — fixes it via Dirac reduction; derives an explicit spinor-valued CA update rule from the massless Weyl equation.
- **Page 39** — numerical stability experiment; observes the update needs a factor of ~0.43 to stay bounded, and notes this factor "has to do with the speed of light" — i.e., it is the CFL stability number, equivalent to the lattice speed of light.

This is essentially the construction now used in quantum-walk discretizations of the Dirac/Weyl equation.

---

*Compiled 2026-05-13.*

---

### Simulation notes (added 2026-05-13)

The equations on pages 37–39 were implemented in Python (`ca-simulation/ca_core.py`) and run to 200 time steps.

**Explicit-Euler scheme (as written on page 38):**
The scheme is unconditionally unstable. Every value of $c$ diverges over a sufficient number of steps; the notebook's observation of ~0.43 as a stabilization threshold reflects only that divergence is slower at lower $c$ — not that there is a true stable region. This is consistent with the general result that explicit Euler applied to a skew-Hermitian operator is always unstable.

**Split-step FFT propagator (derived from the same page 38 equations):**
Each Fourier mode $\mathbf{k}$ is propagated by the exact $2\times2$ unitary:

$$U(\mathbf{k}) = \cos(c\kappa)\,I - \frac{i\sin(c\kappa)}{\kappa}(\boldsymbol\sigma\cdot\mathbf{k}), \qquad \kappa = |\mathbf{k}|$$

This is exactly unitary for all $c$. Results at 200 steps:
- All $c$ values from 0.10 to 0.61 remained stable.
- Time-reversal residuals (100 steps forward, 100 back) were $\sim 6\times10^{-14}$ — machine-precision, independent of $c$.
- Norm $\|\psi\|^2$ was conserved to double precision at every step.

The split-step result confirms the physical content of the page 38 equations: the Weyl CA is unitary and time-reversible. The instability in the notebook was a property of the numerical method, not the physics.
