# CA Rules and the Four Forces — Integration of Ludwig + Fredkin

Companion document to `page35-cellular-automata-research.md` and `fredkin-correlation.md`.

Speculative integration. Established published work is cited; the synthesis itself is theoretical and clearly flagged below.

---

## What integrates cleanly from Ludwig + Fredkin

Fredkin's central constraints — locality, determinism, reversibility, finite information per cell — combined with the Ludwig page 36–38 move (dimensionality from connection number; spinor-valued cell state to resolve the two-time-step problem) give a single object: a **reversible spinor-valued CA on a graph of fixed local valence**.

That object is close to what the modern literature now calls a Quantum Cellular Automaton (QCA) or a discrete quantum walk on a graph. Fredkin supplied the reversibility; Ludwig supplied the spinor reduction; Wolfram (2020) and the causal-set program independently supplied the graph (not a lattice). The pages already in the project anticipate this synthesis without naming it.

---

## The 3-vs-4 connection question

Connection number does two things at once: it sets the lattice's effective dimensionality (Ludwig page 36) and it constrains what vertex algebra the rule can support.

A **trivalent (3-connection) graph** is the minimum structure that admits non-Abelian gauge interactions. This is not a guess — it is exactly the structure Penrose used in his 1971 spin networks and that loop quantum gravity now builds on. The three-edge vertex is also the natural carrier of Yang–Mills three-boson vertices.

A **4-valent graph** is the smallest connectivity that can plausibly recover 3+1 dimensional spacetime locally (three space-like links plus one time-like link), and matches the 4-simplex structure in causal dynamical triangulations (Ambjørn & Loll) and spin-foam models.

So the choice maps roughly: **3 = minimal gauge algebra**, **4 = minimal spacetime dimensionality**. A hybrid — 3 space-like links + 1 distinguished link per node, total valence 4 — is the structure that has the best chance of carrying both simultaneously. This is also closest to Ludwig's page 36 framing.

---

## Where each force could live in such a rule (speculative)

In a spinor-valued CA on a graph of valence 3 or 4, the four forces have to be realized at different "layers" of the construction.

**Gravity** is the natural one. Curvature is variation in graph connection density; geodesics are shortest paths in the graph; Einstein's equations should emerge as the continuum limit of local rewrite statistics. This is the Wolfram-project line and the causal-set line, and Ludwig page 36 gestures the same direction.

**Electromagnetism** lives as a U(1) phase carried by the spinor state at each node — a local gauge degree of freedom in the cell value, not in the graph topology. This is the standard quantum-walk reading of the discrete Weyl equation Ludwig wrote on page 38.

**Weak interaction** is an SU(2) sub-structure of the cell state acting only on one chirality half of the spinor — exactly the symmetry Ludwig stumbled onto independently on page 60 (the "gauged β representation, broken to U(1)" speculation). It is striking that the page-60 sketch already singles out *one helicity* of the bispinor.

**Strong interaction** is the hardest. SU(3) color either needs a 3-fold structure in the connection pattern (which is where the trivalent-graph choice pays off) or a 3-valued internal state per node. Neither is a derivation; both are places where a real construction would have to do work.

In this picture, gravity is geometric (graph-level), and the other three forces are gauge structures carried by the spinor field on top of the graph. That split is exactly the split Sachs tries to avoid in the earlier pages of the notebook — and exactly the split modern unification programs (LQG + Standard Model on a spin network) currently make.

---

## Summary table

| Force | Where it lives in the CA | Required structure |
|---|---|---|
| Gravity | Graph topology / connection density | Variable local geometry; emergent in the continuum limit |
| Electromagnetic | U(1) phase on the spinor at each node | One internal phase degree of freedom per cell |
| Weak | SU(2) on one chirality half of the spinor | Two-component sub-state, broken symmetry |
| Strong | SU(3) color | Either 3-fold connection pattern (trivalent graph) or 3-valued internal state |

---

## The honest obstructions

Lorentz invariance is still the unsolved hard problem. A fixed trivalent or 4-valent graph picks a preferred frame; only random Poisson sprinkling (causal sets) or carrying the Lorentz structure inside the spinor values (Ludwig's route) has a serious case.

Fermion/boson statistics, the Higgs mechanism, and renormalization at the cell scale have no clean CA derivation today. Anyone who claims otherwise is overselling.

---

## Published work in this direction

- [Penrose, "Angular momentum: an approach to combinatorial space-time" (1971)](https://math.ucr.edu/home/baez/penrose/) — trivalent graphs as proto-geometry.
- [Loop Quantum Gravity — Rovelli & Smolin](https://en.wikipedia.org/wiki/Loop_quantum_gravity) — 4-valent spin networks; SU(2) labels on edges.
- [Spin foam models — Wikipedia](https://en.wikipedia.org/wiki/Spin_foam) — 4-valent simplicial complexes; transition amplitudes between spin networks.
- [Ambjørn & Loll, Causal Dynamical Triangulations](https://en.wikipedia.org/wiki/Causal_dynamical_triangulation) — 4-simplex updates that recover 4D spacetime.
- [Wolfram Physics Project — Technical Introduction](https://www.wolframphysics.org/technical-introduction/) — variable-arity hypergraph rewriting.
- ['t Hooft, *The Cellular Automaton Interpretation of Quantum Mechanics* (Springer, 2016)](https://link.springer.com/book/10.1007/978-3-319-41285-6)
- [Farrelly, "A review of Quantum Cellular Automata," *Quantum* (2020)](https://quantum-journal.org/papers/q-2020-11-30-368/)
- [Fredkin & Toffoli, "Conservative Logic" (1982)](https://www.cs.princeton.edu/courses/archive/fall05/frs119/papers/fredkin_toffoli82.pdf)

---

*Compiled 2026-05-13.*
