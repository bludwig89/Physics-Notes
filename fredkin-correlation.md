# Edward Fredkin — Correlation with Pages 35–39

Companion document to `page35-cellular-automata-research.md` and `physics_notes_pages_31-45.md`.

Fredkin (1934–2023) is the figure most directly anticipated by the page 35–39 sideline. He is the founder of *digital physics* / *digital philosophy* and the originator of several of the technical ideas the notes independently sketch. The notes appear to date from 2007–08, by which time Fredkin's program was mature but well outside mainstream physics — making the parallel notable rather than derivative.

---

## Who Fredkin was

- American computer scientist and physicist; professor at MIT (Director of Project MAC, 1971–1974), later Caltech, Carnegie Mellon, and Boston University.
- Early advocate of the idea that the universe is, at base, a deterministic informational process running on a discrete substrate — his *Finite Nature* hypothesis.
- Coined "digital philosophy"; co-developer with Tommaso Toffoli of the framework now called *conservative logic*.

Source: [Edward Fredkin — Wikipedia](https://en.wikipedia.org/wiki/Edward_Fredkin)

---

## Fredkin's relevant contributions

### Finite Nature hypothesis

Every finite volume of spacetime carries a finite amount of information; every small region (a cell) is in one of a small number of states; updates are local and deterministic.

Source: [Fredkin, "Finite Nature" (MIT AI Lab)](http://www.ai.mit.edu/projects/im/ftp/poc/fredkin/Finite-Nature)

### Reversible cellular automata

Fredkin showed that any cellular automaton can be transformed into a reversible one (by carrying a copy of the previous state). His SALT (Six-state Asynchronous Logic Tiling) family is a 2+1-dimensional, reversible, universal CA that is *second-order in time* and respects CPT-style reversibility.

Source: [Reversible cellular automaton — Wikipedia](https://en.wikipedia.org/wiki/Reversible_cellular_automaton)

### Conservative logic and the Fredkin gate

With Toffoli, Fredkin built a reversible, information-conserving model of computation explicitly modeled on physical conservation laws (energy, particle number). The Fredkin gate (controlled-SWAP) is a universal reversible gate; the Toffoli gate (CCNOT) is its three-input cousin.

Sources: [Fredkin gate — Wikipedia](https://en.wikipedia.org/wiki/Fredkin_gate) · [Fredkin & Toffoli, "Conservative Logic" (1982)](https://www.cs.princeton.edu/courses/archive/fall05/frs119/papers/fredkin_toffoli82.pdf)

### Billiard-ball model

A reversible mechanical model (Fredkin & Toffoli, 1982) showing that elastic collisions of identical balls on a lattice can implement universal computation without dissipation — a physically motivated proof-of-concept for the conservative-logic program.

Source: [Billiard-ball computer — Wikipedia](https://en.wikipedia.org/wiki/Billiard-ball_computer)

### Digital Mechanics

Fredkin's later program; the position that physics is the study of a particular reversible universal CA.

Source: [Fredkin, "Digital Mechanics" (PhilPapers)](https://philpapers.org/rec/FREDM)

---

## Correlation to specific pages

### Page 35 — "Dependence implies neighborhood. Rules imply geometry."

This is the organizing thesis of Finite Nature. Fredkin's framing is nearly verbatim: state is local, evolution is rule-driven, geometry is whatever the neighborhood structure says it is. The page 35 question — *"would it be possible to model spacetime geometry and elementary particle physics using cellular automata?"* — is the question Fredkin spent four decades on.

### Page 36 — dimensionality from connection number

Fredkin worked predominantly on **fixed regular lattices** (2D for SALT, 3D for later universal-CA constructions). The page 36 idea — that dimensionality emerges from how many neighbors each cell has — is a step *beyond* Fredkin's lattice framework and in the direction Wolfram later took with hypergraphs. Fredkin himself accepted the lattice and tried to recover physics on top of it.

Source: [Two-state, Reversible, Universal CA in Three Dimensions (Fredkin)](https://www.researchgate.net/publication/2147195_Two-state_Reversible_Universal_Cellular_Automata_in_Three_Dimensions)

### Pages 37–38 — the two-time-step problem and the spinor fix

This is the cleanest correlation, and it goes both ways.

- The notes observe that a finite-differenced second-order wave equation requires two time steps of memory.
- Fredkin's general solution: make the CA *reversible* by explicitly carrying the prior state as part of the cell — this is exactly the "second-order in time" structure of SALT.
- The notes' solution: reduce to first-order via the Dirac/Weyl factorization, producing a spinor-valued update rule.

Both are valid routes to a well-posed discrete dynamics, and both are reversible. The notes' route is closer to the modern quantum-walk / QCA discretizations of the Dirac equation; Fredkin's is closer to classical reversible computing. The conceptual content — *you cannot have a physically meaningful CA without resolving the two-time-step issue* — is the same observation.

### Page 39 — the ~0.43 stability factor

The notes interpret the factor as "having to do with the speed of light." In Fredkin/Toffoli terms this is the conservation-of-signal-propagation requirement: in the billiard-ball model and in conservative logic, the *maximum signal speed* on the lattice is built into the rule and corresponds to the lattice's effective $c$. The CFL number the notes are stabilizing against is the discrete-physics analogue of the Fredkin-Toffoli "ballistic" speed limit.

**Simulation follow-up (2026-05-13):** The explicit-Euler scheme on page 38 is unconditionally unstable; the ~0.43 threshold is the boundary between fast divergence and slow divergence, not true stability. Replacing it with the exact split-step FFT propagator (which applies the exact unitary $e^{-i(\boldsymbol\sigma\cdot\mathbf{k})c}$ per Fourier mode) yields unconditional stability and time-reversal residuals at machine precision (~10⁻¹⁴). This aligns with Fredkin's requirement that a physically meaningful CA must be *reversible* — the split-step scheme satisfies this exactly, while the explicit-Euler scheme violates it.

Source: [Fredkin & Toffoli, "Conservative Logic" (1982)](https://www.cs.princeton.edu/courses/archive/fall05/frs119/papers/fredkin_toffoli82.pdf)

---

## Where Fredkin agrees, and where the notes (and the field) diverge

| Question | Fredkin's position | The notes' position |
|---|---|---|
| Is spacetime fundamentally discrete? | Yes — Finite Nature. | Open — explored as a model. |
| Are updates local? | Yes — strict CA neighborhood. | Yes (page 35). |
| Is the dynamics reversible? | Yes — central to the program. | Implicitly yes (the Weyl equation is unitary). |
| Geometry: imposed or emergent? | Imposed (regular lattice). | Hints at emergent (page 36, "connection number"). |
| How are particles realized? | As stable propagating patterns in the CA — "gliders." | Not addressed on these pages, but the spinor field is the natural carrier. |
| Lorentz invariance? | Acknowledged as the hardest problem; not resolved in Fredkin's lattice framework. | Sensed as the obstruction (page 35 closing question). |

The Lorentz-invariance gap is the well-known critique of Fredkin's program. The three modern workarounds — Wolfram's hypergraphs, Sorkin's causal-set sprinkling, and the spinor / quantum-walk route the notes are already on — are all attempts to keep Fredkin's *spirit* while abandoning the rigid lattice.

---

## One-line summary

Pages 35–39 reproduce, independently and in compressed form, two of Fredkin's central moves (deterministic local-rule cosmology; reversibility as a constraint on the dynamics) and then take a third step Fredkin did not — the spinor reduction — which lands closer to the modern quantum-walk literature than to Fredkin's own SALT/billiard-ball constructions.

---

## Sources

- [Edward Fredkin — Wikipedia](https://en.wikipedia.org/wiki/Edward_Fredkin)
- [Fredkin, "Finite Nature" (MIT AI Lab archive)](http://www.ai.mit.edu/projects/im/ftp/poc/fredkin/Finite-Nature)
- [Fredkin, "Digital Mechanics" (PhilPapers)](https://philpapers.org/rec/FREDM)
- [Fredkin & Toffoli, "Conservative Logic" (1982)](https://www.cs.princeton.edu/courses/archive/fall05/frs119/papers/fredkin_toffoli82.pdf)
- [Fredkin gate — Wikipedia](https://en.wikipedia.org/wiki/Fredkin_gate)
- [Billiard-ball computer — Wikipedia](https://en.wikipedia.org/wiki/Billiard-ball_computer)
- [Reversible cellular automaton — Wikipedia](https://en.wikipedia.org/wiki/Reversible_cellular_automaton)
- [Edward Fredkin — LifeWiki (CA community profile)](https://conwaylife.com/wiki/Edward_Fredkin)
- ["There's Plenty of Boole at the Bottom" — *Minds and Machines* (2016)](https://link.springer.com/article/10.1007/s11023-016-9401-6)

*Compiled 2026-05-13.*
