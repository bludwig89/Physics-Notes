# 't Hooft (2015) — *The Cellular Automaton Interpretation of Quantum Mechanics*

*Compiled 2026-05-21 - 01:05. Source PDF: `Cellular-Automaton-Interpretation-of-Quantum-Mechanics.pdf` (259 pp., version 3, December 2015, arXiv:1405.1548v3). Companion to `qca-papers-1-4-overview.md`, `ostoma-trushyk-1999-summary.md`, `mohr-2010-maxwell-photon-wf-summary.md`.*

This document summarises Gerard 't Hooft's CAI monograph and then compares its central claims against the cellular-automaton model developed in this project (architecture in `ca-unified-v2.md`, status in `project-status.md`, exact results in `exactness-inventory.md`).

---

## 1. What the book is

A monograph — not a primary research paper — laying out an *interpretation* of quantum mechanics in which the underlying ontology is a classical, deterministic cellular automaton. Quantum mechanics is treated as a mathematical tool, not a fundamental theory of nature. The book is split into two parts:

- **Part I (chapters 1–10):** philosophy, framework, response to Bell/CHSH, and the conceptual sketch of the CAI.
- **Part II (chapters 11–23):** technical calculation tools — `PQ` theory (discrete integer–rotor formalism), fermions (Jordan–Wigner, 'neutrino' beable model), bosons, strings, symmetries, the Hamilton problem on discrete lattices, and quantum field theory in this language.

The author is explicit that the book is "speculative" and that no model in it reproduces the Standard Model. The goal is to motivate the *interpretation* and develop the *language* in which a deterministic underlying theory might one day be written.

---

## 2. Core claim (the CAI in one paragraph)

The universe is in a single **ontological state** at every moment, drawn from a privileged orthonormal basis of Hilbert space called the **ontological basis**. The evolution operator, in this basis, does nothing more than permute basis elements. Wave functions ("templates") that we use in practice are unitary changes of basis on this single ontic state; the Schrödinger equation is the *same* equation in either basis. Born's rule, the collapse postulate, and Schrödinger's cat are not separate axioms but consequences of the assumption that the universe was, is, and always will be in *one* basis element of the ontological basis at any given time.

---

## 3. Key constructions and terminology

### 3.1 Beables, changeables, superimposables

- **Beables** $\mathcal B_{op}$: operators diagonal in the ontological basis. They commute with one another at all times — including over time-like separations. They are the only operators with a classical, "really happening" reading.
- **Changeables** $\mathcal C_{op}$: operators that permute ontological states, e.g. the evolution operator itself, or any specific permutation matrix.
- **Superimposables** $\mathcal S_{op}$: operators that map an ontological state onto a superposition of others. Almost every "operator" used in classroom quantum mechanics — position, momentum, spin in some basis — is a superimposable.

The split is the central technical move. *Standard QM treats all three on the same footing; the CAI insists only beables describe reality.*

### 3.2 Templates and the ontological basis

- A **template** is a state vector used to *calculate*. It need not be ontological. Hydrogen-atom eigenstates, photon polarisation kets, position eigenstates — all templates.
- The **ontological basis** is the (unknown, but postulated to exist) basis in which the universe's state is one basis element with amplitude 1 at all times. Born's rule applies to bra-ket inner products where *at least one* side is ontological.
- The ontological basis is not unique: continuous symmetry transformations may map one ontological basis to another. Which one is "the real" basis may be undetermined in principle (axiom (c), p. 61).

### 3.3 The cellular automaton

- Cells $Q(\vec x, t)$ sit at discrete spatial lattice positions $\vec x \in \mathbb Z^d$ and discrete time $t \in \mathbb Z$.
- Each cell carries finitely many bits — possibly an integer modulo $N$.
- The evolution rule depends only on a bounded neighbourhood:

$$Q(\vec x, t+1) = Q(\vec x, t-1) + F(\vec x, \{Q(t)\}), \qquad \text{addition mod }N. \tag{5.2}$$

This two-step form is time-reversible by construction: $Q(\vec x, t-1) = Q(\vec x, t+1) - F$.

### 3.4 Hilbert-space packaging

The set of classical states is treated as an orthonormal basis of a Hilbert space. The one-step evolution operator $U_{op}(\delta t)$ is unitary (permutation matrices are unitary), eigenvalues $e^{-i\omega_i}$, and the formal Hamiltonian satisfies

$$U_{op}(\delta t) = e^{-iH_{op}\,\delta t}, \qquad 0 \le H_{op} < 2\pi/\delta t. \tag{5.5}$$

This Hamiltonian is mathematically well-defined but has at least three obstructions to physical use:

1. **It is defined modulo $2\pi/\delta t$.** Two non-interacting subsystems do not have additive Hamiltonians without extra work (subsection 5.2).
2. **Locality is hard.** The naive expansion of $H_{op}$ in $U_{op}^n$ gives terms whose interaction range grows as $n$, not as a single cell-spacing (subsection 5.6.1).
3. **Positivity is hard.** A Hamiltonian bounded below is needed for stability of any quantum theory; the naive $H_{op}$ is bounded only to $[0, 2\pi/\delta t)$, which is not the same as $\ge 0$ extensively in space (subsection 9.1).

These three obstructions — locality, positivity, additivity — are the technical heart of the book's open problems.

### 3.5 Response to Bell / CHSH

't Hooft does not deny the experimental violations of the CHSH inequality. He argues instead that:

- **Counterfactual definiteness is not assumed.** The CAI explicitly denies that Alice or Bob can "have measured a different setting" without modifying the rest of the universe (including the entangled photons in flight and their common past).
- **Superdeterminism is invoked.** All events — including detector settings — are part of the same deterministic evolution. The "mouse-dropping function" of section 3.6.1 constructs a three-point probability distribution $W(c\mid a,b) = \tfrac12|\sin(4c-2a-2b)|$ that reproduces the QM correlation $\langle AB\rangle = \cos(2(a-b))$ via correlations between detector settings $a, b$ and the hidden photon polarisation $c$.
- **Conspiracy is unavoidable but not "absurd"** — it follows from the ontology-conservation law: ontic states evolve into ontic states; superpositions evolve into superpositions; the apparatus settings inherit correlations from the deep past (e.g. inflationary common past for quasars used as setting choosers).

This is the most discussed and most contested part of the book.

### 3.6 Other key constructions

- **Cogwheel model (chapter 2):** the prototype deterministic system whose Hilbert-space description has exactly the spectrum of a quantum harmonic rotor. The CAI's "Hello, world."
- **`PQ` theory (chapter 16):** discrete pairs of conjugate variables $(P, Q)$ obeying a finite-displacement algebra, intermediate between continuous canonical mechanics and a fully discrete automaton. Used to encode the harmonic oscillator and the multi-dimensional free boson in a deterministic ontological basis.
- **'Neutrino' beable model (section 15.2):** a specific deterministic-looking model in 3+1 D whose template formulation reproduces a massless Weyl fermion. The author's flagship existence proof.
- **Information loss (chapter 7):** automata where states are *not* time-reversible (multiple pasts collapse to one future). Information-equivalence classes are taken as the ontological basis, and the resulting unitary evolution restores time reversibility. Equivalence classes are conjectured to be the same kind of object as local gauge equivalence classes — pointing to a possible deep link between gauge symmetry and erased classical information.
- **Holography & Hawking radiation (section 9.4):** the Bekenstein bound says no volume can contain more information than the surface-area of a black hole that would fit inside it; the CAI interprets this as the underlying CA losing bulk information at horizons while keeping surface information accessible.
- **Arrow of time (section 7.3):** the radical proposal that microscopic laws need *not* be time-reversal symmetric — large-scale time asymmetry is read directly off the asymmetry of the underlying CA, not solely from initial-condition entropy.

---

## 4. What the book delivers and what it does not

### 4.1 Delivers

- A consistent *interpretation* of QM (templates + ontological basis + ontology conservation) that
  - eliminates the measurement problem (cat is always either dead or alive ontically),
  - removes the collapse axiom (collapse is automatic when written in the ontological basis),
  - derives Born's rule from the requirement that ontological and template bases be related by a unitary,
  - acknowledges and accommodates Bell/CHSH violations via superdeterminism + ontology conservation.
- Worked toy models: cogwheel, $PQ$ theory, the 'neutrino' beable model, deterministic strings, the Earth–Mars interchange operator (a pedagogical example of a non-beable observable in classical mechanics).
- A technical vocabulary (beable/changeable/superimposable; template/ontological; cogwheel/automaton; info-equivalence class) that is reused throughout the QCA / digital-physics literature.

### 4.2 Does not deliver

- **No CA for the Standard Model.** Section 8.1 explicitly states this as the largest open problem: "What will be the CA for the SM?"
- **No positive, local, additive Hamiltonian** built from a finite CA in $\ge 3$ spatial dimensions (section 9.1; chapters 14, 22).
- **No Lorentz invariance.** Generic CAs pick a preferred frame; deformed Lorentz (DSR) is mentioned as a possible route but not realised in any model in the book.
- **No prediction beyond Copenhagen QM** in regimes where Copenhagen makes a prediction. The book is conservative on this — it deliberately does *not* modify Schrödinger's equation or Born's rule.
- **No quantitative test against experimental data.** The author concedes that "real-world" comparison is for future work once a CA for the SM is found.

---

## 5. Comparison to the model in this project

The project's CA architecture is laid out in `ca-unified-proposition.md` (v1), `ca-unified-v2.md` (v2, current), `ca-electroweak-design.md`, and `ca-emergent-time-plan.md`. The reference papers absorbed so far are Bisio–D'Ariano–Perinotti–Tosini (Papers 1, 4), Raynal (Paper 2), Ostoma–Trushyk (Papers 3, 6), Fredkin (Paper 5), Mohr (2010), and now 't Hooft (2015). All 30 exact-algebraic and 7 machine-precision results are catalogued in `exactness-inventory.md`.

### 5.1 Where the two match

| Element | 't Hooft CAI | Our model (v2) | Status |
|---|---|---|---|
| **The universe is a deterministic cellular automaton at the most fundamental scale.** | Postulated as the *interpretation* of QM. | Postulated as the substrate; QCA is implemented and simulated. | Match in worldview. |
| **Discrete cells; integer / finite per-cell state; local update rule.** | Generic automaton (chapter 5), $Q(\vec x, t)\in\mathbb Z_N$. | BCC lattice (Papers 1, 2); 2-component complex spinor per cell (Weyl) / 4-component (Dirac) / scalar (Higgs Φ); split-step propagator from local sub-steps. | Same architecture; we are at the concrete-implementation end of the family of CAs 't Hooft contemplates. |
| **Time reversibility from a two-step (or unitary) update.** | $Q(\vec x, t+1) = Q(\vec x, t-1) + F$ (Eq. 5.2). | Split-step Strang composition; every stepper is exactly unitary; Cayley variable-$c$ stepper has $5.5\times 10^{-15}$ norm drift. | Match in form. The CAI's "ontological basis evolution = permutation" maps to our exact-unitary propagators. |
| **The Hamiltonian is the log of one-step evolution; mod $2\pi/\delta t$ ambiguity is acknowledged.** | Eq. 5.4–5.5; locality, positivity, additivity all open. | We use the QCA dispersion $\omega_{\vec k} = \arccos(\sqrt{1-m^2}\,c_x c_y)$ (Paper 1 Eq. 23 / Finding 13) directly; the mod-$2\pi$ structure is what makes the spectrum bounded. | Match. The arccos dispersion is the resolution of the mod-$2\pi$ ambiguity for our specific automaton class. |
| **Ontological basis exists but may not be unique; symmetry transformations relate equivalent ontological bases.** | Axioms (a)–(c), p. 61. | The Weyl/Dirac/Maxwell construction in Paper 1 is unique up to a unitary conjugacy class; our beable basis is the cell-occupation basis of the per-cell state. We do not claim it is *the* unique ontological basis. | Match in principle; both leave room for non-uniqueness. |
| **Classical states are diagonal in the ontological basis (Schrödinger's cat is resolved).** | Section 4.2: classical observables = beables at macroscopic scale. | Our macroscopic readouts (centroid position, energy density, $\phi(\mathbf x)$ in `ca_emqg.py`) are diagonal in the per-cell basis by construction. No superposition of dead/alive ever appears in simulation. | Match; the resolution is automatic in any concrete CA implementation. |
| **The single largest open problem is producing a CA whose continuum limit is the Standard Model.** | Section 8.1 ("What will be the CA for the SM?"). | We have implemented Weyl, Dirac, U(1), SU(2), Higgs, EMQG-Poisson gravity, and composite Maxwell, but not the full SM. The hierarchy problem and Poincaré invariance are open. | Match in honest acknowledgement of the gap. |
| **Information loss and equivalence classes might be identified with local gauge equivalence.** | Section 9.3 ("Information loss and time inversion"). | Not implemented, but `ca-emergent-time-plan.md` Phase T5 (vacuum freezing, $N(\vec x) = 0$ on 80% of an $L=256$ lattice) is the closest analog: cells that do not change collapse into the same equivalence class for any observer reading the field. | Conceptual match; we have a partial empirical realisation in the emergent-time work. |
| **Arrow of time may have a microscopic (not just initial-condition) origin.** | Section 7.3. | The emergent-time roadmap explicitly takes proper time as a per-cell tick count $N(\vec x)$, which is monotonically increasing — built-in time asymmetry at the lattice level. | Match in spirit; our $\tau(\vec x) = \tau_0 N(\vec x)$ is a concrete realisation. |
| **Holography and the Bekenstein bound as a CA information-density constraint.** | Section 9.4. | Not implemented; flagged as a long-term target in `lattice-vs-spacetime-tests.md`. | Match in principle, untested in our code. |
| **Superdeterminism is the route around Bell/CHSH.** | Chapters 3.6, 5.7.2–3, 10.3. | Our CHSH test (QM-1 in `exactness-inventory.md`) saturates Tsirelson at $|S|=2\sqrt 2$ to $4.4\times 10^{-16}$ on the lattice singlet, then degrades to $2.2\times 10^{-9}$ after 12 Weyl ticks. We achieve the violation by computing exact lattice quantum correlations, not by a superdeterministic correlation construction. | **Partial match** — same conclusion (Bell violation reproduced on a deterministic substrate), different mechanism (we use the quantum-mechanical bilinears built from the lattice; 't Hooft constructs the violation from a three-point correlation function $W(c\mid a,b)$ at the ontic level). See §5.2 below for the contrast. |

### 5.2 Where the two differ

| Element | 't Hooft CAI | Our model (v2) | Significance of the gap |
|---|---|---|---|
| **What level of physics the project addresses.** | An *interpretation*: a re-reading of the same equations that experimental QM already confirms. Deliberately produces no new prediction. | An *implementation*: concrete propagators, concrete numerics, lattice-specific predictions (frequency-dependent $c$, BCC dispersion correction $\propto k^3/54$ along $(1,1,1)$, curl-residual constant $1/\sqrt{2d}$, GR Shapiro/lensing to <0.5%). | The CAI deliberately makes no Standard-Model prediction; we have ~30 lattice-scale algebraic identities and ~20 quantitative SM/GR matches. The two are at different levels of the same research programme. |
| **Lattice choice and dispersion.** | Generic / unspecified; the book lists desiderata (locality, time reversibility, finite per-cell info) without committing to a lattice geometry. | **BCC in 3D, square in 2D** — *uniquely* determined by the Bisio–D'Ariano five informational principles (Papers 1, 2). $c_\text{lat} = 1/\sqrt d$ is an exact algebraic identity, not a tunable parameter. | 'Hooft leaves the lattice open. We close it with the QCA uniqueness result. This is information the CAI does not have available; it post-dates the construction. |
| **Spinor / fermion construction.** | 'Neutrino' beable model (section 15.2) — a specific construction in 3+1 D using Jordan–Wigner, with the algebra worked out at length. The discrete substrate is implicit. | Per-cell complex spinor, Weyl QCA (Paper 1 Eq. 16 in 2D, Eq. 15 in 3D), with the constraint $n^2 + m^2 = 1$ enforced (Finding 9). Dispersion $\omega = \arccos(\sqrt{1-m^2}\,u_{\vec k})$ at $3.9\times 10^{-16}$ residual. | Different fermion-construction *families*. The CAI's 'neutrino' is built to be a beable; our Weyl spinor is built from informational uniqueness. We have not checked whether the two are unitarily equivalent at the propagator level. |
| **Photon construction.** | Photons are not explicitly constructed as beables in the book; the Maxwell sector is discussed at the QFT level (chapter 20) but no deterministic CA for it is presented. | **Composite (De Broglie) photon** — Paper 1 Eq. 35: $G^i(\vec k, t) = \varphi^T(\vec k/2)\sigma^i\psi(\vec k/2)$. Transversality, dispersion $\Omega_\gamma = \abs(k)/\sqrt 3$ at 0.21%, and curl-residual leading constant $1/\sqrt{2d}$ all verified (Findings 2, 7; exactness-inventory items 22–30 from Mohr 2010 extensions). | A concrete construction we have that the CAI does not. The Maxwell sector is one of the places the CAI is most aware of being incomplete (§5.7.4, 8.1). |
| **Gravity.** | "Section 6, Quantum gravity": a four-page essay arguing that gravity is essential to solving the Hamiltonian positivity / locality problems, but no model is offered. Section 9.4 sketches holography. | **EMQG modified Poisson** (Paper 6 Eq. 19.7) implemented in `ca_emqg.py`: $\nabla^2\phi - c_0^{-2}\partial_t^2\phi = 4\pi G\rho_\text{tot}$; couples to a Cayley variable-$c$ stepper via $c(\vec x) = c_0/(1 - 2\phi/c_0^2)$ (GR-Shapiro form). 3D Newtonian lensing ratio $\Delta(2M)/\Delta(M) = 1.99647$ at 0.35%; absolute deflection coefficient $K = 3.881$ vs Einstein's 4 (3% off at $L=192$ open-BC); Shapiro delay 0.06% (PPN $\gamma=1$ pinned). | Substantially ahead of the CAI on the gravity side. The CAI flags this as the most important unsolved problem; we have a working (open-source-published-target) lattice realisation through Ostoma–Trushyk's EMQG. |
| **Mechanism for Bell / CHSH violation.** | Superdeterminism + ontology conservation + a three-point correlation function $W(c\mid a, b) = \tfrac12 \abs{\sin(4c-2a-2b)}$ engineered at the ontic level to reproduce the QM correlation. The "mouse-dropping function" (§3.6.1). | Direct simulation of the lattice singlet state with discrete polariser bilinears; the CHSH value $abs(S) = 2\sqrt 2$ at $4.4\times 10^{-16}$ comes out of the unitary evolution, *not* out of a constructed correlation. The lattice obeys QM where QM has been tested. | **Different mechanisms for the same conclusion.** This is the cleanest philosophical gap. The CAI insists the lattice cannot internally know about $W(c\mid a,b)$; we never wrote one — we just evolved the singlet and measured. If the CAI is right, our test is sampling from the marginal of $W$. If we are right, the lattice produces Bell violations from local unitary evolution alone (modulo the entangled initial state). Either reading is consistent with the data. |
| **Counterfactual definiteness.** | Explicitly denied (§10.2). | Not addressed in code. Our CHSH measurement is operational: we evolve a state, measure $S$; we never ask "what would have happened if Alice had chosen differently." | We *also* do not assume counterfactual definiteness; we just have not made an issue of it. The CAI's denial is articulated; ours is implicit. |
| **Free will.** | Explicitly denied — apparatus settings are part of the deterministic evolution (§10.3.4). | Not addressed. We treat detector settings as free parameters when configuring simulations. | This is a metaphysical commitment 't Hooft makes that we do not need to make. Operationally, when we run CHSH at $abs(S) = 2\sqrt 2$, we choose the angles — the simulation does not. Whether *we* are choosing them or whether *our brains* are part of a larger deterministic CA is outside the scope of the project. |
| **Ontological basis: uniqueness.** | Allowed to be non-unique up to continuous symmetries (axiom (c), p. 61). | The Paper 1 / Paper 2 uniqueness theorem says the QCA *propagator* is unique on BCC in 3D and on the square in 2D (modulo a unitary conjugacy class and trivial automaton). This is a stronger statement than the CAI makes. | Constraint we have that the CAI does not. |
| **Lorentz invariance.** | Explicitly broken in all toy models. DSR is mentioned but not constructed (§10.4, §22). | Lorentz invariance is broken by construction (BCC picks a preferred frame). DSR via Paper 4 Eq. 25 ($L^D_\beta = \mathcal D^{-1}L_\beta\mathcal D$) is **proposed** in `ca-unified-v2.md` §S5 but not yet implemented. SR-2 (moving-clock time dilation) has a closed-form Lorentz-violation coefficient $\beta_\text{LV}(m) = \tfrac12(1 - m/(\sqrt{1-m^2}\arcsin m))$ (Finding 15, exact-algebraic items 20–21). | Match in the negative ("LI is broken"); we have advanced one step further by writing down the closed-form LV coefficient on the 2D-square QCA. |
| **Born's rule.** | Derived from the unitarity of the transformation between ontological and template bases (chapter 4.3). | Treated as a direct consequence of the inner-product structure of the lattice Hilbert space; not separately axiomatised; verified in CHSH and PMNS tests. | Match in principle; the derivation is the same in spirit. |
| **Renormalisation / continuum limit.** | Acknowledged as not yet addressed (Conclusions). | Same status — `ca-unified-v2.md` caveat 6: "renormalization is still not addressed." | Match. |
| **Existence of an underlying ontology.** | Asserted as the central axiom. | We *implement* one (the per-cell beable basis) without committing to whether it is *the* ontology. The project's working stance is closer to "the lattice is what we simulate, and it reproduces what we measure" than to "this is what nature is." | Soft difference of stance, not a substantive disagreement. |
| **Information loss as a source of negative-energy avoidance.** | Section 9.2: second quantisation of fermions exploits the Dirac sea trick; section 9.4 connects information loss to surface holography. | We have a positive Hamiltonian on the lattice by construction in each implemented sector (Weyl, Dirac, Higgs, EMQG-Poisson); we have not exercised information-loss mechanisms because our automata are unitary by design. | Different *strategy*. The CAI uses information loss as a tool for the positivity problem; we use unitarity directly. The CAI's strategy is closer to thermodynamic / holographic; ours is closer to quantum-information / unitary-circuit. |
| **The Hierarchy Problem.** | Discussed at length (§8.2); acknowledged as unsolved. | Acknowledged in `ca-unified-v2.md` caveat 6 and `lattice-vs-spacetime-tests.md` as out of scope. | Match in honest acknowledgement. |
| **Superstrings / extra dimensions.** | Section 17.3 — deterministic strings constructed on a lattice in 1+1 D. | Not in our model. | The CAI explores this; we do not. |
| **Equivalence-Principle violation.** | Not addressed quantitatively. | Ostoma–Trushyk predict $\sim 10^{-40}$ — below numerical resolution. We have not run a WEP test. | Match in the negative. |

### 5.3 Areas where one project could inform the other

**What our project could borrow from 't Hooft:**

1. **The beable / changeable / superimposable split** is a sharper bookkeeping device than our current "per-cell phase vs. propagator structure" distinction in `ca-unified-proposition.md` §3. Adopting the terminology in `ca-reference.md` would make it easier to argue about which operators in our simulation are "really happening" vs. computational scaffolding.
2. **Information-equivalence classes as gauge classes** (§9.3) is a concrete proposal for what U(1) gauge symmetry might mean in a deterministic substrate. Our implementation of U(1) is currently an external phase $\exp(-iqA_0\Delta t)$ — i.e. we *put in* the gauge symmetry by hand. The CAI suggestion that gauge equivalence is information-loss equivalence is testable in our setting once we implement an information-loss automaton (currently out of scope).
3. **The cogwheel model** (chapter 2.2) is the simplest non-trivial CAI prototype and could be added as a one-page test (`tests-priority/test_NN_cogwheel.py`?) for pedagogy and as a regression target for the cleanest version of the ontological-basis claim. Cheap.
4. **Strong distinction between ontological and effective Hamiltonians** (§5.6). We currently use one Hamiltonian per sector and treat it as "the" generator. The CAI insists that the *effective* Hamiltonian we compute (e.g. via Baker–Campbell–Hausdorff on the QCA propagator) is only conjugate to the ontological one within its conjugacy class. This is a useful frame for understanding why some of our lattice predictions (e.g. the $\beta_\text{LV}(m)$ in Finding 15) depend on $m$ in a way that *looks* like a continuum prediction but is in fact a one-parameter family of conjugacy-class members.

**What 't Hooft's program could borrow from us (i.e. from the Bisio/Raynal/Ostoma–Trushyk synthesis):**

1. **The BCC lattice uniqueness theorem** (Papers 1, 2). The CAI is silent on lattice geometry; our work shows it is forced once locality + isotropy + linearity + unitarity + homogeneity are demanded.
2. **The composite-photon construction** (Paper 1 Eq. 35). The CAI flags Maxwell as an open sector; the Paper-1 De Broglie bilinear plus our verifications (transversality, dispersion, curl-residual) is a concrete realisation.
3. **EMQG modified Poisson** as a *concrete* gravity sector (Paper 6 Eq. 19.7 + our `ca_emqg.py` and Cayley variable-$c$ stepper). The CAI says gravity is essential to solving positivity; we have a working lattice gravity that has been tested against Newtonian lensing (0.35%) and Shapiro delay (0.06%) — even if it is not GR-exact.
4. **Exact-algebraic identities at machine precision** — our `exactness-inventory.md` lists 30 such results. The CAI's claim that "the Schrödinger equation is obeyed by the ontological states" becomes a *testable* statement in any concrete implementation; we have the testing infrastructure the CAI does not.

### 5.4 The biggest single conceptual gap

't Hooft proposes that the universe is in a *single* ontological basis element at every moment, and that all of QM is the result of using a different basis (the template basis) to do calculations. Our model does not need this — we evolve the *templates themselves* unitarily on the lattice and reproduce QM directly. We do not commit to whether the per-cell amplitude $\psi(\vec x, t) \in \mathbb C^2$ is a template or an ontic state.

If 't Hooft is right, our lattice is the template view, and there is an underlying classical CA whose ontological states we are not simulating. If we are right (or, more honestly, if the QCA literature's framing is right), the lattice *is* the deepest description and the question "but what is *really* happening?" is not well-formed below the QCA level — because the QCA is, by construction, the unique informational realisation of the Schrödinger equation in a discrete, local, isotropic, homogeneous, unitary, linear setting.

This is the only place where the two projects make incompatible claims at the *foundational* level. At the *practical* level — what lattice, what propagator, what tests pass — they are talking about different things and could be combined: the QCA is one *interpretation* of what 't Hooft's "ontological cellular automaton" is.

---

## 6. Concrete takeaways for the project

These are the items that arose from reading the CAI that may warrant follow-up in the project. None of them invalidates work to date; all of them are additive.

1. **Adopt the beable/changeable/superimposable vocabulary in `ca-reference.md`.** This is a clarification, not a code change. It would let us label which operators in our simulation are diagonal in the per-cell basis (energy density, charge density, position centroid, $N(\vec x)$ tick counter) and which are not (Pauli spin in any non-cell basis, the Hamiltonian itself). Effort: small.

2. **Add a cogwheel-model test as a pedagogical / regression target.** A single $\mathbb Z_N$ cyclic permutation with the spectrum $\{2\pi k/N\delta t\}$. Useful as the simplest possible example of "the ontological basis is the eigenbasis of a beable; the energy basis is a superimposable." Effort: ~half a day.

3. **Document the conceptual choice between the CAI superdeterminism reading and the QCA-direct-evolution reading of our CHSH result.** Currently the CHSH test in `tests-priority/test_02_QM1_CHSH.py` reports $|S| = 2\sqrt 2$ at $4.4\times 10^{-16}$ residual without commentary on which mechanism is operative. A paragraph in `findings.md` (Finding 14.3 or a new finding) noting that our test is consistent with both readings, and that distinguishing them requires a test that probes the *correlations between settings and initial state* (which our current tests do not), would be honest. Effort: half a page.

4. **Consider whether information-loss / equivalence-class machinery is worth implementing.** The CAI's chapter 7 is a concrete proposal: take a non-unitary classical CA, compute info-equivalence classes (states that merge under future evolution), and treat *those* as the ontological basis. The result is a unitary quantum evolution that may have nontrivial gauge / locality properties not present in the original CA. *None* of our automata currently have information loss because we use exact-unitary propagators by construction. If we wanted to test the CAI claim that local gauge equivalence = info-equivalence, this is the route. Effort: large (new module, new test suite).

5. **Re-read 't Hooft chapter 9.4 (Holography and Hawking radiation) alongside `ca-emergent-time-plan.md` Phase T5.** The CAI suggests information at horizons should be allocated by surface area, and our T5.A finding (80% of an $L=256$ lattice has $N(\vec x) = 0$ exactly) is in the spirit of "information about a small interior region is mostly stored in the cells at the boundary that *do* tick." Whether this is a coincidence or a hint is open. Effort: re-read + a paragraph in `findings.md`.

6. **The CAI's mod-$2\pi/\delta t$ Hamiltonian ambiguity (Eq. 5.5) and the QCA arccos dispersion ($\omega = \arccos(\sqrt{1-m^2}u_{\vec k})$) are the same observation seen from two sides.** Documenting this connection in `exactness-inventory.md` would tighten the bridge between the CAI vocabulary and our concrete implementation. Effort: small.

7. **The Hamiltonian-positivity problem (CAI §9.1) is *not* solved in our model either.** Each sector has a positive Hamiltonian by construction (we use unitary blocks), but the additivity (CAI Eq. 5.6) of those Hamiltonians is unverified for the *full* coupled v2 stack (Weyl + Dirac + Higgs + EMQG + composite Maxwell). A test that checks $\langle\psi|H_\text{total}|\psi\rangle \ge 0$ for representative templates would be informative. Effort: medium.

---

## 7. Bibliographic note

't Hooft, G., *The Cellular Automaton Interpretation of Quantum Mechanics*, arXiv:1405.1548v3 [quant-ph], 21 Dec 2015 (version 3, extensively modified). Subsequently published as *Fundamental Theories of Physics* vol. 185 (Springer, 2016) — open-access reissue. The book builds on a sequence of earlier 't Hooft papers (ref. [72] in the book is the 2014 CAI proposal); is in dialogue with Fredkin's Digital Mechanics (Paper 5 in our overview), de Broglie–Bohm, GRW, and many-worlds; and cites Bell, CHSH, Tsirelson, Brans, and others throughout the foundations discussion.

---

*End of summary. Cross-references:*
- *`qca-papers-1-4-overview.md` for Bisio–D'Ariano–Perinotti–Tosini and Raynal — the rigorous-derivation half of the CA-as-physics programme.*
- *`ostoma-trushyk-1999-summary.md` for EMQG — the gravity-from-CA half.*
- *`mohr-2010-maxwell-photon-wf-summary.md` for the photon wave function.*
- *`ca-unified-v2.md` for this project's current model architecture.*
- *`exactness-inventory.md` for the empirical state of the implementation.*
- *`findings.md` for the catalogue of observations and possible new finds.*
