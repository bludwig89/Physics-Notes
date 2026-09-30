# Notebook × SM Cross-Check — pp. 31–39: σ-Matrix Clifford Algebra, Sachs Restatement,
# CA Lattice Speculation, Spinor-CA Stability

*2026-09-22 - 21:50 · checks `notebook-reconstruction-03-sigma-clifford-ca-lattice.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 1 verdict (NB-043/044, IMPROVES), 0 changed. An independent subagent
with no access to this write-up's reasoning confirmed all five citations (Wolfram 2021 update,
Leuenberger arXiv:2110.03388, Abajian & Carlip arXiv:1710.00938/PRD 97 066007, and Elze's
arXiv:2504.06883 + arXiv:2401.08253) exist and support the claims made; it also independently
confirmed the "three distinct programs" count (causal sets / Wolfram Physics Project / 't Hooft-Elze
CA program) is accurate, since the two Elze papers are one author's continuing line of work, not two
separate programs — this write-up already grouped them that way.

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.31-32 | 31–32 | REINFORCES | SETTLED | Standard Clifford/Dirac square-root-of-KG algebra, plus a correct tetrad-gauge-freedom observation (any Hermitian 2-spinor basis reproduces the flat metric); a real sign-convention slip elsewhere in the notebook was caught in the process. |
| pp.33-34 | 33–34 | NEUTRAL | SETTLED | Pure restatement of already-checked batch-02 material, no new content. |
| pp.35-36 | 35–36 | IMPROVES | ACTIVE | "Rules imply geometry" and "dimension from connection number" are exactly the thesis of several genuine, currently active discrete/emergent-spacetime research programs (causal sets, the Wolfram Physics Project, 't Hooft's cellular-automaton program). |
| pp.37-39 | 37–39 | REINFORCES | SETTLED | Standard finite-difference discretization of the Weyl equation, with its explicit-Euler numerical instability proven (not just observed) by textbook von Neumann analysis; the broader project of a CA reproducing the Dirac/Weyl equation is itself a live 2020s research direction (noted in hindsight, not counted toward this section's tag since the specific discretization checked here is the standard/settled numerical piece). |

## What the field learned since 2007 that matters for this batch
- **"Rules imply geometry" is now a named, active research direction, not just a CA-literature
  truism.** The Wolfram Physics Project (launched publicly in April 2020) is built on exactly this
  thesis: hypergraph rewriting rules are claimed to generate emergent space, an emergent (possibly
  non-integer, evolving) dimension, and — in specific constructed cases — dynamics resembling
  Einstein's equations and the Dirac/Schrödinger equations in a continuum limit. [The Wolfram Physics Project: A One-Year Update (Wolfram, 2021)](https://writings.stephenwolfram.com/2021/04/the-wolfram-physics-project-a-one-year-update/) [D — the project's own account]; [Emergence of Minkowski-Spacetime by Simple Deterministic Graph Rewriting (arXiv:2110.03388, 2021)](https://arxiv.org/pdf/2110.03388) [C]
- **Causal set theory derives emergent dimension from a discrete order relation ("dependency"),
  quantitatively, via the Myrheim–Meyer estimator** — a decades-old but still actively used tool in
  quantum-gravity phenomenology; recent (2017–2021) work studies exactly the "how many neighbors ⇒
  what dimension" question this notebook poses, for causal sets built to resemble a manifold. [Dimensional reduction in manifold-like causal sets (arXiv:1710.00938, 2017/2018)](https://arxiv.org/pdf/1710.00938) [C]
- **'t Hooft's deterministic cellular-automaton interpretation of quantum mechanics remains an
  active program through 2024–2025**, including recent work specifically deriving the Dirac
  equation and particle mass from permutations of discrete automaton states — directly on the same
  research question as this notebook's pp.37–39 spinor-CA construction. [The Dirac Equation, Mass and Arithmetic by Permutations of Automaton States (Elze, arXiv:2504.06883, 2025)](https://arxiv.org/pdf/2504.06883) [C]; [Cellular automaton ontology, bits, qubits, and the Dirac equation (arXiv:2401.08253, 2024)](https://arxiv.org/pdf/2401.08253) [C]
- None of these programs is mainstream-consensus physics — the Wolfram Physics Project in
  particular has drawn substantial criticism for making large claims without the peer-reviewed
  validation standard fields expect — but all three are genuinely live (2020+ papers, continuing
  through 2024–2025), not merely a 2007-era curiosity that the field has since dropped.

## Per-build verdicts

### NB-039, NB-040 (p.31) — σ-Matrix Clifford Relations; Square-Root-of-KG Check
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** the Pauli-matrix Clifford algebra $\{\sigma^\mu,\sigma^\nu\}=2\eta^{\mu\nu}$
  makes $\sigma^\mu\partial_\mu\psi=0$ a legitimate first-order "square root" of the Klein-Gordon
  equation (the standard route to the Weyl/Dirac equation).
- **Anchor:** foundations — same structural fact as batch 02's NB-014/015, the defining property of
  the Weyl/Dirac construction used throughout electroweak theory.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — unchanged since the 1920s-30s.

### NB-041 (p.32) — Tetrad/Frame Gauge Freedom; a Sign-Convention Catch
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** the flat Minkowski metric does not uniquely fix which Hermitian
  2-spinor basis ($q^\mu$) represents it — a continuous family of distinct bases (e.g. any
  rotation of the spatial Pauli matrices) reproduces the same metric.
- **Anchor:** foundations — this is local-frame (tetrad) gauge freedom, the same freedom that
  underlies local Lorentz invariance in any tetrad-based (Einstein–Cartan-type) formulation of GR
  with spinor matter.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none relevant to the physics; the reconstruction's own check of this build
  incidentally surfaced a genuine internal sign-convention inconsistency in the notebook's own
  $q^\mu/\tilde q^\mu$ metric formula (a batch-02-adjacent notebook slip, already logged there —
  not itself an external-physics question, so not re-graded here).

### NB-042 (pp.33–34) — Restated Two-Field Sachs Lagrangian
- **Checked against:** reconstruction status `SOLID` (by reference to already-verified batch-02 material)
- **Claim (field terms):** none new — direct restatement.
- **Anchor:** none new (already covered in the pp.15-29 cross-check).
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-043, NB-044 (pp.35–36) — "Rules Imply Geometry"; Dimensionality From Connection Number
- **Checked against:** reconstruction status `SOLID` (both; NB-044's specific numerical claims —
  including that a coordination number of 4 can support a genuine 3D lattice, via the diamond-cubic
  structure — independently confirmed by the reconstruction from real lattice geometry)
- **Claim (field terms):** a cellular automaton's local update-dependency structure (which cells a
  rule reads from) is logically prior to, and determines, the emergent geometry/dimensionality one
  can draw for the automaton; specific coordination numbers (2, 3, 4, 6, 8) map onto specific
  possible lattice dimensionalities and structures.
- **Anchor:** quantum-gravity foundations — the general question of whether continuum spacetime
  (and its dimension) is emergent from a more primitive discrete/combinatorial structure, rather
  than fundamental. This is a recognized, if non-mainstream, research question with several
  distinct active programs.
- **Current status:** no discrete/emergent-spacetime program is part of the accepted mainstream
  (GR + QFT remain the tested, working description at all currently accessible scales/energies),
  but "does discreteness at the Planck scale produce continuum geometry, and how" is a genuinely
  open question the field has not settled either way.
- **Live work:** yes, on (at least) three fronts, none excluded by data (all such approaches are
  explicitly designed to reduce to ordinary GR/QM at accessible scales, so none is in tension with
  current precision tests by construction): causal set theory's Myrheim–Meyer dimensional analysis
  (2017–2021 continuing work), the Wolfram Physics Project's hypergraph rewriting (2020–2023,
  ongoing), and 't Hooft's cellular-automaton program (2020, 2024, 2025 papers). See the batch-level
  bullets above for citations.
- **Verdict:** IMPROVES · ACTIVE
- **What would decide it:** none of these programs currently has a distinguishing, near-term
  experimental test; they are assessed on internal consistency and on whether they can be shown to
  reproduce known GR/QM/SM physics in a controlled continuum limit (which is exactly what much of
  the 2020s work cited above is trying to establish).
- **Hindsight:** in 2007 this was a reasonable-sounding but essentially untested intuition; it is
  now the explicit organizing thesis of at least one large, actively-funded, continuing research
  program (Wolfram Physics, since 2020) plus older, more conservative programs (causal sets) that
  have kept producing 2020s results on precisely the "neighbor count ⇒ dimension" question this
  notebook poses.

### NB-045, NB-046 (pp.37–38) — Discretized Wave Equation; Boxed Spinor-CA Update Rule
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** a standard centered-difference discretization of the 2D wave equation,
  and a correctly-formed explicit finite-difference discretization of the massless Weyl equation
  $\partial_t\psi=-\boldsymbol\sigma\cdot\nabla\psi$.
- **Anchor:** foundations — correctly discretizing a known continuum PDE is a numerical-methods
  fact (does this scheme's continuum limit reproduce the known equation — yes), not itself a novel
  physical claim; the broader enterprise (build a CA whose continuum limit is a relativistic wave
  equation) is the same research question as the batch-level 't Hooft/Elze citations above.
- **Verdict:** REINFORCES · SETTLED (a non-standard [CA/discrete] route to a standard
  [continuum Weyl equation] result — textbook-correct discretization, no open question here)
- **Hindsight:** the specific discretization technique is unchanged, standard numerical analysis;
  see the batch-level bullets for the live research context this construction sits inside.

### NB-047 (p.39) — Numerical (In)stability of the Explicit-Euler Spinor-CA Scheme
- **Checked against:** reconstruction status `SOLID` (empirical instability reproduced) and
  extended to a closed analytic proof (unconditional instability for any $c>0$, via von Neumann
  stability analysis)
- **Claim (field terms):** the specific explicit-Euler finite-difference scheme of NB-046 is
  numerically unstable for every value of its Courant-type coefficient $c$; no choice of $c$
  stabilizes it.
- **Anchor:** none in SM/GR terms — this is a pure numerical-analysis result (a textbook
  application of von Neumann/Fourier stability analysis, standard since the 1940s-50s) about a
  specific integration scheme's numerical behavior, not a physical prediction.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a for the specific numerical fact. More broadly, that explicit-Euler-type
  schemes are generically unstable for norm-preserving (unitary-generator) evolution equations,
  and that some other scheme (implicit, symplectic, or a genuinely unitary/staggered update) is
  needed, is exactly why real lattice field theory and lattice-QCD-style constructions use
  carefully designed (not naive-explicit) time-evolution schemes — a well-known fact long predating
  2007, not something the field learned since.

## Reconstruction queries
None. The reconstruction's own NB-041 sign-convention finding and NB-047's closed stability proof
are both externally consistent (standard tetrad gauge freedom; standard von Neumann analysis) and
not disputed here.

## Handoff items raised (mirrored into the handoff file)
One item — see `notebook-sm-crosscheck-handoff.md` §B (paste-ready research prompt on the
discrete/emergent-geometry research programs vs. the model's own lattice foundation).

## Contamination log
None. This run drew only on the reconstruction file and the sources cited above, fetched in-session.

## Appendix — search queries used
- "causal set theory emergent dimension Myrheim-Meyer dimension estimator 2020 2023 review"
- "Wolfram Physics Project hypergraph rewriting emergent spacetime dimension 2020 2023 status"
- "'t Hooft cellular automaton interpretation quantum mechanics 2016 2020 review status"
- (WebFetch) arxiv.org/abs/2504.06883 — Elze 2025, Dirac equation from automaton-state permutations

## Sources
- [The Wolfram Physics Project: A One-Year Update (Wolfram, 2021)](https://writings.stephenwolfram.com/2021/04/the-wolfram-physics-project-a-one-year-update/) [D]
- [Emergence of Minkowski-Spacetime by Simple Deterministic Graph Rewriting (arXiv:2110.03388, 2021)](https://arxiv.org/pdf/2110.03388) [C]
- [Dimensional reduction in manifold-like causal sets (arXiv:1710.00938, 2017/2018)](https://arxiv.org/pdf/1710.00938) [C]
- [The Dirac Equation, Mass and Arithmetic by Permutations of Automaton States (Elze, arXiv:2504.06883, 2025)](https://arxiv.org/pdf/2504.06883) [C]
- [Cellular automaton ontology, bits, qubits, and the Dirac equation (arXiv:2401.08253, 2024)](https://arxiv.org/pdf/2401.08253) [C]
