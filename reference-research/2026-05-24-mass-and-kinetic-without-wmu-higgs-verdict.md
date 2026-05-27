# Verdict — Can Stueckelberg + AKT + Chen–Lin help with mass coupling and kinetic steps without $W_\mu$ or the Higgs?

**Date:** 2026-05-24 - 15:30
**Question (Ben):** Review the three papers and determine if they can help our model with mass coupling and kinetic steps without $W_\mu$ or the Higgs field.
**Source summaries:**
- `ruegg-ruiz-altaba-2003-stueckelberg-summary.md`
- `hattori-hidaka-yang-2019-axial-kinetic-summary.md`
- `chen-lin-2022-quantum-kinetic-axial-summary.md`
**Linked project state:** F27 (chiral SU(2) mass without Higgs), F31 (covariant BCC hopping with $W_\mu$), F32 (free $W_\mu$ propagation), `roadmap-wmu-implementation.md` (Phase 5B is the open Stueckelberg path).

---

## TL;DR

- **Higgs:** all three papers, taken together, support the F27 claim that the Higgs is not required for fermion mass coupling. Stueckelberg gives the canonical theoretical justification for what F27 already does at the CA level. **Verdict: yes, can drop the Higgs.**
- **$W_\mu$:** none of the three papers offer a route to eliminate $W_\mu$ as a dynamical field. Stueckelberg gives $W_\mu$ a mass; AKT treats $W_\mu$ as outside its scope; Chen–Lin treats $A^5_\mu$ as a *background probe*, not a dynamical gauge boson. **Verdict: no, $W_\mu$ stays.**
- **Kinetic step:** AKT and Chen–Lin provide rigorous continuum benchmarks that F27's complex-mass step should match in the long-wavelength limit (specifically: Bargmann–Michel–Telegdi spin precession, V↔A coupling through mass, magnetization currents). These are testable, not architectural.

---

## 1. The Question, Re-Stated

The user's working model has three relevant facts:

1. F27 has already demonstrated chiral SU(2)$_L$ mass coupling **without a Higgs** — the gauge phase $U(x) \in$ SU(2) acts in the mass step and is pure gauge. The mass gap appears with $\langle\Phi\rangle = 0$.
2. F31 and F32 have promoted $W_\mu$ to a dynamical lattice gauge field, with link variables and free propagation matching the F26 rotation law.
3. The W_μ roadmap explicitly lists Path 5B ("Promote F27 $U(x)$ to dynamical, Stueckelberg / nonlinear sigma") as the alternative to a separate Higgs sector.

The question — can these three papers replace $W_\mu$ and the Higgs? — splits cleanly into the two halves above.

---

## 2. Mass Coupling Without the Higgs

### What Stueckelberg actually does for the model

The Ruegg–Ruiz-Altaba review establishes:

1. For U(1), the Stueckelberg mechanism is **unitary AND renormalizable** in continuum perturbation theory. The auxiliary scalar $B$ is the Goldstone-like phase of a frozen-modulus Higgs.

2. For non-Abelian SU(N), the Stueckelberg / Kunimasa–Goto construction is the natural generalization:

   $$\mathcal{L} = -\tfrac{1}{4}F^{i\,2}_{\mu\nu} + \tfrac{m^2}{2}\,\mathrm{Tr}\!\left[A^i_\mu T^i - \tfrac{i}{g}U^{-1}\partial_\mu U\right]^2, \quad U = \exp(i\tfrac{g}{m}B^i T_i)$$

   This is **unitary** but not power-counting renormalizable in continuum perturbation theory (Hurth 1997). It is the **nonlinear-sigma** form of a frozen-Higgs theory.

3. **F27 is precisely this construction at the CA level.** F27's $U(x) \in$ SU(2), introduced as the gauge phase of the complex-mass step, is exactly the Stueckelberg matrix $U$ in the Kunimasa–Goto Lagrangian. F27's "U(x) plays the role of the Higgs VEV direction but is pure gauge" is the standard Stueckelberg interpretation. The Ward identity in F27 (T5, residual $10^{-17}$) is the lattice-exact statement of Pauli's gauge invariance ($\delta A_\mu = \partial_\mu \Lambda$, $\delta B = m\Lambda$).

### Why the renormalizability no-go doesn't kill this for the project

The continuum perturbation-theory no-go (Slavnov 1972, Hurth 1997) says: in continuum perturbative QFT, non-Abelian Stueckelberg is either unitary OR renormalizable, not both. The Higgs is the only known continuum-perturbative route.

The CA model **is not a continuum perturbative theory.** The BCC lattice provides a natural UV cutoff; there is no infinite renormalization that needs to be controlled. F27's tests (norm conservation, Ward identity, dispersion invariance) all run at machine precision — there is no UV singularity to renormalize away.

This means: **the obstruction that forces continuum QFT to use the Higgs does not apply to the CA model.** Stueckelberg-on-a-lattice can be unitary AND have no renormalization issues, because the lattice spacing is the cutoff.

### What AKT and Chen–Lin add to the mass-without-Higgs case

- **AKT (Hattori, Hidaka, Yang 2019):** Treats mass as a fixed parameter. Has nothing to say about mass *generation*, but provides the algebraic identity $m\mathcal{S} = \Pi\cdot\mathcal{V}$ — mass acts as the coupling between vector and axial currents. F27's complex-mass step, in the long-wavelength limit, should reproduce this. **Confirmation, not generation.**
- **Chen–Lin 2022:** Explicitly massless. Their explicit outlook statement: "Since mass breaks axial symmetry explicitly, it requires a nontrivial modification to the solution presented in this work." They point to AKT as the route. **Silent on mass generation.**

### Verdict on the Higgs

The three papers, taken together, **support replacing the Higgs sector with F27's $U(x)$ for the project's purposes**. The Stueckelberg review gives the literature grounding; AKT and Chen–Lin do not push back. Path 5B in `roadmap-wmu-implementation.md` is now well-supported by the literature.

**Concrete action:** rename Path 5B to "non-Abelian Stueckelberg / Kunimasa–Goto mass term" in the roadmap and cite Ruegg–Ruiz-Altaba 2003 and Kunimasa & Goto 1967.

---

## 3. Eliminating $W_\mu$ — Where the Three Papers Cannot Help

The user asks whether we can drop $W_\mu$ as well. Honest assessment of each paper:

### Stueckelberg review

The Stueckelberg mechanism gives $W_\mu$ a mass; it does not eliminate $W_\mu$. Every Lagrangian in the paper contains a dynamical vector field $A_\mu$ (Abelian) or $A^i_\mu$ (non-Abelian). The auxiliary scalar $B$ couples to the vector and dies on physical states; it is the longitudinal d.o.f., not a replacement for the vector.

So Stueckelberg cannot answer "no $W_\mu$" at all. It answers "$W_\mu$ massive without a Higgs."

### AKT

AKT treats only U(1) electromagnetic background — there is no $W_\mu$, no SU(2) gauge field, and no fermion–weak-boson vertex. The paper is structurally about quantum kinetic theory for a single Dirac field. The chirality coupling that exists is U(1) axial (the $\gamma^5$ direction), not SU(2)_L.

For the project: AKT is silent on weak interactions and cannot inform whether $W_\mu$ is necessary.

### Chen–Lin 2022

Chen–Lin's axial gauge field $A^5_\mu$ is the closest of the three to a substitute for $W_\mu$, but it is an **external probe field**, not a dynamical gauge boson. Its purpose is to source the axial current and derive correlation functions by functional differentiation. There is no kinetic term $-\tfrac{1}{4}(F^5)^2$ for it.

In a CA model, the analogous role would be played by an external field used to source the axial current; it would not propagate, not self-interact, and not give a covariant derivative to fermions in any meaningful sense.

So Chen–Lin also cannot eliminate $W_\mu$ as a dynamical field.

### What "eliminating $W_\mu$" would actually mean

If $W_\mu$ is dropped:
- F27's Ward identity ($V(x)\cdot$mass-step$(\psi;U) = $ mass-step$(V\psi; VUV^\dagger$)) still holds for the **mass step alone** — F27 verified this at $10^{-17}$.
- But the **kinetic step** (Weyl walk) is NOT SU(2)_L invariant without $W_\mu$. F27 explicitly listed this as Known Limitation #1, and F31's whole purpose was to close it.
- Without $W_\mu$ the model is a chiral mass-only theory; it has SU(2)_L as a global symmetry of the mass term but no local SU(2)_L. This is far from the Standard Model — it does not give the weak charged current, β decay, or weak isospin gauging.

The three papers do not provide a workaround. None of them constructs a chiral SU(2)_L invariant kinetic step without an explicit vector gauge field.

### Verdict on $W_\mu$

The three papers **do not help eliminate $W_\mu$.** If the goal is a fully gauged SU(2)_L theory with weak isospin as a local symmetry of *both* the mass and the kinetic step, $W_\mu$ is required. F31 and F32 are the right way forward, and Phase 4 (the fermion-$W_\mu$ vertex) is the explicit closure of F27 Known Limitation #1.

If the goal is **a less-ambitious model** — one where SU(2)_L is only a global symmetry of the mass term, with no charged-current physics — then $W_\mu$ could be dropped. But that would be a different theory, and the project's commitment is to a full chiral gauge theory (per the F27 / F29 / F31 / F32 finding sequence).

---

## 4. Kinetic Step — What the Papers Actually Contribute

The "kinetic step" in the project's vocabulary is the discrete time-step that evolves the Weyl spinor on the BCC lattice. The two kinetic-theory papers (AKT and Chen–Lin) give a continuum benchmark that the kinetic step should match in the long-wavelength limit. Three useful targets:

### A. Bargmann–Michel–Telegdi spin precession (AKT)

The AKT zeroth-order axial kinetic equation reduces to:

$$q\cdot\Delta\,a^\mu = F^\mu{}_\nu a^\nu$$

— classical relativistic spin precession in an EM field. **Testable in the CA**: prepare a polarized fermion wavepacket on the BCC lattice with F27's complex-mass step in a uniform EM background; verify the spin four-vector evolves according to BMT. Expected to be algebraically exact in the long-wavelength limit; lattice-discretization corrections at $O(a^2)$.

### B. $m\mathcal{S} = \Pi\cdot\mathcal{V}$ (AKT)

The continuum-level identity that mass couples scalar density and vector current. F27's mass step at small $k$ should reproduce this. **Testable** as: bilinear identity between F27's $\bar\psi\psi$ and $\bar\psi\gamma^\mu\psi$ structures, evaluated to leading order in $k$.

### C. Killing condition for global equilibrium (Chen–Lin)

For a CA run with thermal vorticity / chemical potential, the Killing condition

$$\partial_\mu \beta_\nu + \partial_\nu \beta_\mu = 0, \qquad \partial_\mu \bar\mu_s = -F^s_{\mu\nu}\beta^\nu$$

must hold for a steady-state distribution to exist. **Useful as a sanity check** for extended thermal-equilibrium CA experiments (when those become relevant).

These are **verification targets**, not architectural changes. They do not eliminate $W_\mu$ or the mass parameter; they test that F27's step has the right continuum face.

---

## 5. Concrete Recommendations

### Update the roadmap
1. **Path 5B → "non-Abelian Stueckelberg / Kunimasa–Goto"** in `roadmap-wmu-implementation.md` § Phase 5. Cite Ruegg & Ruiz-Altaba 2003 §VI.C, Kunimasa & Goto 1967, and F27's algebraic match.
2. Note that the continuum no-go (Slavnov 1972, Hurth 1997) does not bind the CA model because the lattice provides a UV cutoff.

### Add verification tests (low priority, post-Phase 4)
1. **BMT precession test** for the F27 mass step in a uniform EM background, target $10^{-12}$ relative error at $L \ge 64$.
2. **$m\mathcal{S} = \Pi\cdot\mathcal{V}$ bilinear identity** test in the long-wavelength limit, target algebraic exactness.
3. **Killing condition** sanity check for thermal-equilibrium CA experiments (deferred until thermal-CA work is on the table).

### Do not drop $W_\mu$
F27 Known Limitation #1 (kinetic step not SU(2) invariant alone) is real and is closed only by F31 + Phase 4. The three papers reviewed here do not provide a workaround. The project's commitment to a fully gauged chiral SU(2)_L theory requires $W_\mu$ as a dynamical field. F31 and F32 are the right approach; Phases 3–6 of the roadmap should proceed.

### Add the literature anchors
These three summaries are the project's first formal contact with the post-2000 kinetic-theory literature (AKT 2019, Chen–Lin 2022) and the canonical Stueckelberg review (Ruegg & Ruiz-Altaba 2003). They are the right anchors to cite when describing F27 to anyone outside the project.

---

## 6. One-Line Verdict

**The three papers confirm that the Higgs can be dropped (F27 is the non-Abelian Stueckelberg construction), provide kinetic-theory benchmarks for the F27 mass step, and do not offer a route to eliminate $W_\mu$.**

---

## Cross-references

- `findings/F27-complex-mass-chiral-su2.md` — mass without Higgs, the CA-level Stueckelberg
- `findings/F31-wmu-covariant-hopping.md` — closes F27 Limitation #1 partially
- `findings/F32-wmu-free-propagation.md` — free $W_\mu$ propagation
- `roadmap-wmu-implementation.md` — Phase 5B is the Stueckelberg path
- `reference-research/ruegg-ruiz-altaba-2003-stueckelberg-summary.md`
- `reference-research/hattori-hidaka-yang-2019-axial-kinetic-summary.md`
- `reference-research/chen-lin-2022-quantum-kinetic-axial-summary.md`
