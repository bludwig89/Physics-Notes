# Physics Notes — Pages 1–15

Source: `physics_notes_0708.pdf`
Transcribed: 2026-05-13
Author of original notes: Richard McPhee

---

## Page 1 — Quantum Scalars I

Top-of-page scratch:

$$E^2 = p^2 + m^2$$

$$(E^2 - p^2) - m^2 = 0 \quad\quad -\partial_\mu \partial^\mu - m^2 = 0$$

**Quantum Scalars I**

First we quantize a scalar field using my method, then a single spinor field or pair.

A scalar field obeys

$$\partial_\mu \partial^\mu \phi + m^2 \phi = 0$$

Its Lagrangian is

$$\mathcal{L} = \tfrac{1}{2}(\partial^\mu \phi)(\partial_\mu \phi) - \tfrac{1}{2} m^2 \phi^2$$

$$\mathcal{H} = \frac{\partial \mathcal{L}}{\partial \dot\phi}\dot\phi - \mathcal{L}$$

$$\pi_\phi = \frac{\partial \mathcal{L}}{\partial \dot\phi}$$

and the Lagrangian field equation is

$$\partial_\mu\!\left(\frac{\partial \mathcal{L}}{\partial(\phi, \mathcal{v})}\right) - \frac{\partial \mathcal{L}}{\partial \phi} = 0$$

Writing $\mathcal{L}$ out,

$$\mathcal{L} = \tfrac{1}{2}(\partial_0 \phi)^2 - \tfrac{1}{2}(\nabla\phi)^2 - \tfrac{1}{2} m^2 \phi^2$$

So

$$\frac{\partial \mathcal{L}}{\partial \dot\phi} = \partial_0 \phi = \dot\phi = \pi_\phi$$

and

$$\mathcal{H} = \tfrac{1}{2}\pi_\phi^2 + \tfrac{1}{2}(\nabla\phi)^2 + \tfrac{1}{2} m^2 \phi^2$$

Change this to $k$-space. With $\omega_k = (m^2 + k^2)^{1/2}$,

$$\phi_k = \left((2\pi)^3 \, 2\omega_k\right)^{-1/2} \int \phi(x)\, e^{i k \cdot x} d^3 x$$

$$\phi(x) = (2\pi)^{3} \int \phi_k\, (2\omega_k)^{1/2}\, e^{-i k \cdot x} d^3 x$$

Now with

$$H = \int \mathcal{H}(x)\, dx$$

we substitute the Fourier transform for $\phi$ into $\mathcal{H}$ and integrate with respect to $x$:

---

## Page 2 — Hamiltonian in k-space

$$\mathcal{H} = \tfrac{1}{2}\left(\pi^2(x) + (\nabla\phi(x))^2 + \phi^2(x)\right)$$

Substituting the Fourier transforms (schematically):

$$= \tfrac{1}{2}\Big[\Big((2\pi)^{3}\!\!\int \pi_k (2\omega_k)^{1/2} e^{-i k\cdot x}\, d^3k\Big)\Big((2\pi)^{3}\!\!\int \pi_p (2\omega_p)^{1/2} e^{-i p\cdot x}\, d^3p\Big)$$

$$- (2\pi)^{6}\!\!\int \vec{k}\, \phi_k (2\omega_k)^{1/2} e^{-i k\cdot x}\, d^3k \cdot \int \vec{p}\, \phi_p (2\omega_p)^{1/2} e^{-i p\cdot x}\, d^3p$$

$$+ (2\pi)^{6}\!\!\int \phi_k (2\omega_k)^{1/2} e^{-i k\cdot x}\, d^3k \cdot \int \phi_p (2\omega_p)^{1/2} e^{-i p\cdot x}\, d^3p\Big]$$

and combining gives

$$H = \frac{(2\pi)^{6}}{2} \iiint \Big[(\pi_k \pi_p - (\vec{k}\cdot\vec{p})\,\phi_k \phi_p + \phi_k \phi_p) (2\omega_k)^{1/2}(2\omega_p)^{1/2}\, e^{-i k\cdot x} e^{-i p\cdot x}\Big]\, d^3k\, d^3p\, d^3x$$

This must be integrated with respect to $x$ first. The only $x$ dependency is in the exponentials,

$$H = \int F(k, p)\, e^{-i(k+p)x}\, d^3k\, d^3p\, d^3x$$

---

## Page 3 — Photon / Graviton (diagrams)

Heading at top of page: **photon / graviton**

- Wavy line labeled *photon*; double-arc / "bump" line labeled *graviton* with parameter $a$.
- Note: **Photon antisymmetric / Graviton symmetric**

**Tetrahedron with 3 types of particles — how many isomers are there?**

> Only 2 — cannot have anything else if all must join each vertex.

(Two tetrahedron sketches showing the two isomers.)

**With octahedron, gets more interesting. You can do it w/ 2 or 4 particles.**

> For 2-particle, bottom is completely determined by top. How many isomers? **3 only.**

(Five octahedron sketches showing the three isomers and variations on the bottom row.)

---

## Page 4 — (blank / back-of-page bleed-through)

The page contains only faint show-through from the diagrams on page 3. No new content.

---

## Page 5 — Superconductivity vs Spinor Electrodynamics

**1.** The idea of spinor electrodynamics involves two spin-½ fermion-photons exchanged in a correlated fashion between two charged particles. That is, instead of the usual

(diagram: two $e^-$ exchanging a single photon $\gamma$)

one has something like

(diagram: two $e^-$ exchanging a pair of $\gamma_{1/2}$ particles in an "X" configuration)

Yet these $\gamma_{1/2}$'s behave together like a single boson $\gamma$ that only occurs as a pair. They don't occur separately.

**2.** This is similar to superconductivity, in which two electrons pair up to create a single Cooper pair, a spin-0 state.

**3.** Could photons be a Cooper pair of spinor photons, or some such thing? The lattice could be the geometric structure of spacetime itself.

---

## Page 6 — Superconductivity / Spinor Electrodynamics (cont.)

**4.** The "superconductivity" state then, might simply be travel at the speed $c$, without hindrance from the "lattice" so to speak.

**5.** There should be some kind of negative binding energy associated with the bound pair of spinor photons.

**6.** This all has to do with symmetry breaking. How exactly does that work? The Higgs is the Cooper pair, we presume. Is there a scalar photon?

**7.** How does current flow in one direction or the other in a superconductor?

**8.** Can we understand $W$ and $Z$ bosons in this context? Could they have to do with other states of spinor photons?

> We need more detail on BCS & BCS + hole theory.

---

## Page 7 — Heat of Combustion

Heading: **heat of combustion, cal / gram mol wt**

| Substance | Formula | Heat (cal) | Mol wt |
|---|---|---|---|
| Cellulose | $C_6 H_{10} O_5$ | — | — |
| Octane | $CH_3(CH_2)_6 CH_3$ | 1302.7 | 114.23 |
| Ethane | $CH_3 CH_3$ | 372.81 | 30.07 |
| Butane | $CH_3(CH_2)_2 CH_3$ | — | 58.12 |
| Propane | $CH_3(CH_2)CH_3$ | 530.57 | 44.11 |
| Methane | $CH_4$ | 212.79 | 16.04 |

Sketched structural formula for butane: H–C–C–C–C–H with all hydrogens shown.

**Question:** Under what conditions will chains polymerize? e.g.

$$CH_4 + CH_4 \;\longrightarrow\; CH_3 CH_3 + H_2$$

$$CH_3 CH_3 + CH_3 CH_3 \;\longrightarrow\; CH_3(CH_2)_2 CH_3 + H_2$$

etc.? Perhaps in the presence of $O_2$ so $H_2 \to H_2 O$?

| Substance | kcal/g |
|---|---|
| Methane | 13.26 |
| Propane | 12.03 |
| Ethane  | 12.39 |
| Octane  | 11.40 |

---

## Page 8 — (blank)

Faint bleed-through only. No content.

---

## Page 9 — Sachs Made Easy

The unification of gravitational and electromagnetic forces made by Mendel Sachs is, in this author's opinion, one of the most significant and fundamental achievements of the twentieth century. Unfortunately Sachs has been outside the mainstream of physics ever since the phenomenologically-oriented gauge theories have become popular. As such his work is relatively unknown and unappreciated. The difficult concepts and mathematics involved in the theory also make it difficult for the average physicist to comprehend. The purpose of this paper is to make Sachs' work more accessible, in the hope that it could be built upon, in order to comprehend all the forces of nature, including the strong and weak forces.

Of particular interest here is the natural and fundamental way in which gravitation and electromagnetism are unified. Sachs does not rely on arbitrary combinations of groups, etc., as is normal with gauge unifications like $SU(2)\times U(1)$ electro-weak in Weinberg–Salam, and supersymmetric follow-ons, which leave the student wondering "Why $SU(2)\times U(1)$? What does nature prefer in that over $SU(2)\times SU(2)$ or anything else?" In Sachs' theory, both gravitation and electromagnetism arise naturally out of the basic …

---

## Page 10 — Fundamental Matter Fields

… structure of spacetime.

### Fundamental Matter Fields

In attempting to formulate a fundamental theory of matter, we must first consider what properties a "fundamental" matter field should have. In conventional particle physics, matter fields are understood to be spin-½ fields which describe the basic constituents of matter: electrons, quarks, muons, neutrinos, etc. For the most part these are massive particles, and thus they are described as Dirac Spinors, with four complex-valued components to each field.

Most particle physicists understand in some qualitative way, however, that mass is and ought to be generated by the interactions of those particles and their associated fields. For example, the electric and magnetic fields $\mathbf{E}$ and $\mathbf{B}$ are associated with an energy density

$$\xi = \frac{1}{8\pi}(E^2 + B^2)$$

so it makes sense to suggest that a particle of charge $q$ inescapably has a mass arising from its electric field $E = q/r^2$.

We may apply this idea quantitatively to the different particles to understand their masses.

---

## Page 11 — Mass Generation, Continued

Quarks, which interact strongly, weakly and electromagnetically are very massive. Electrons, which interact only electromagnetically and weakly are on the order of 1800 times lighter, and neutrinos, which interact only weakly, are much lighter still.

Serious obstacles prevent physicists from turning this qualitative picture into quantitative predictions. For example, for a point particle,

$$\int_{r_0}^{\infty} E^2\, dV$$

is divergent as $r_0 \to 0$. Neither does such a simplistic picture explain why there should be particles which apparently undergo the exact same interactions, yet which differ in mass, like the $e^-$, $\mu^-$ and $\tau^-$ leptons. If their mass were due only to interactions, one would at first think they should all have the same mass.

Regardless of these difficulties, we expect mass to be somehow generated at the most fundamental levels. We might also expect general relativity to be intimately associated with mass generation. As such, it makes sense to start with massless spinor fields as the "basic" matter fields, and to "clothe" them with mass derived from their interactions.

Massless spinor fields need not be represented …

---

## Page 12 — Spinor Representations of Matter Fields

… as Dirac fields, with four complex-valued components. Indeed, the Dirac representation is designed to simplify the interpretation of the fields when a particle is at rest. Being at rest is, however, a property that's only attributable to massive particles.

Much better in dealing with massless particles is a representation which separates the four-component spinor into a pair of decoupled two-spinors. Such representations are only possible for massless particles, and effectively allow one to think in terms of particles that are just two-component spinors.

### Spinor Representations of Matter Fields

The most well-known representation of massless spinor matter fields is the so-called **Weyl Representation**. For a massive field, one may write

$$i\hbar \frac{\partial \psi_+}{\partial t} = -i\hbar c\, \boldsymbol\sigma \cdot \nabla \psi_+ \; - \; m_0 c^2\, \psi_- \tag{1a}$$

$$i\hbar \frac{\partial \psi_-}{\partial t} = \;\;\; i\hbar c\, \boldsymbol\sigma \cdot \nabla \psi_- \; - \; m_0 c^2\, \psi_+ \tag{1b}$$

When $m_0 \to 0$ these become two decoupled equations for $\psi_+$ and $\psi_-$, respectively. We may note that under a parity transformation $\vec{x} \to -\vec{x}$, $\vec{\nabla} \to -\vec{\nabla}$, and equations (1a) and (1b) …

---

## Page 13 — Helicity States; GR and Curved Spacetime

… transform into one another. As such, these equations are properly interpreted as states of positive and negative helicity. The state of positive helicity is a particle with its spin oriented along the axis of motion, or an antiparticle with its spin oriented opposite to the axis of motion. The state of negative helicity is the opposite.

We will use this representation for massless particles throughout this paper. In his original work, Sachs uses another representation most of the time, in which time reversal is explicit, rather than space reflection. Sachs did most of his work before the Standard Model of electroweak interactions was verified in many facts, which relies so heavily on the difference between left-handed and right-handed particles. Thus, for our purposes there are two basic types of fundamental matter field in flat spacetime. They obey the equations

$$i\hbar \frac{\partial \psi_+}{\partial t} = -i\hbar c\, \boldsymbol\sigma \cdot \nabla \psi_+ \tag{2a}$$

$$i\hbar \frac{\partial \psi_-}{\partial t} = \;\;\; i\hbar c\, \boldsymbol\sigma \cdot \nabla \psi_- \tag{2b}$$

### General Relativity and Curved Spacetime

One major step in formulating Sachs' unification is simply defining the mathematics of …

---

## Page 14 — Riemannian Geometry, Metric Tensor

… spinors in curved spacetime. Classical General Relativity is a tensor theory, so an extension to spinors is necessary, and non-trivial. It is non-trivial in the sense that it naturally leads to new dynamics that aren't present in the classical tensor theory.

General Relativity is formulated within the framework of Riemannian geometry such that spacetime is everywhere locally Minkowskian. That is, at every point there is a metric tensor $g_{\mu\nu}(x)$ which can be transformed by some coordinate transform so that

$$g_{\mu\nu}(x)\big|_{x_0} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & -1 \end{pmatrix}$$

That is, the metric reduces to the metric for flat Minkowskian spacetime at the point $x_0$. This metric defines distances using the formula

$$ds^2 = \sum_{\mu\nu} g_{\mu\nu}\, dx^\mu\, dx^\nu$$

and makes it possible to create scalar quantities using a dot product rule of vectors,

$$\mathbf{u}\cdot\mathbf{v} = \sum_{\mu\nu=0} g_{\mu\nu}\, u^\mu\, v^\nu$$

In Minkowski space, this vector product …

---

## Page 15 — Deriving the Hierarchy Equations for Sachs Electrogravity

The gravitational field Lagrangian is

$$\mathcal{L}_E = R\,(g)^{1/2} \quad\quad \tag{(6.41 + my notes p.56)}$$

Supporting / cross-referenced equations:

$$g \equiv -\det(g_{\mu\nu}) \quad\quad \tag{p.30}$$

$$\partial_\sigma g^{\mu\nu} = -\tfrac{1}{2}\left(q^\mu \tilde{q}^\nu + q^\nu \tilde{q}^\mu\right) \quad\quad \tag{3.59'}$$

$$K_{\rho\lambda} = \partial_\rho \Omega_\lambda - \partial_\lambda \Omega_\rho + \Omega_\rho \Omega_\lambda - \Omega_\lambda \Omega_\rho \quad\quad \tag{6.40}$$

$$\phantom{K_{\rho\lambda}} = \Omega_{\lambda;\rho} - \Omega_{\rho;\lambda} \quad\quad \left(\Omega_{\mu;\rho} = (\partial_\mu + \Omega_\rho)\Omega_\mu\right) \quad \tag{6.45}$$

$$R = \tfrac{1}{4}\,\mathrm{Tr}\!\left(K_{\mu\nu}\, q^\mu \tilde{q}^\nu - K_{\mu\nu}\, q^\mu q^\nu + q^\mu K^{+}_{\mu\nu}\, q^\nu - q^\nu K^{+}_{\mu\nu}\, \tilde{q}^\mu\right)$$

$$\Omega_\mu = -\tfrac{1}{4}\, q_\rho \left(\partial_\mu \tilde{q}^\rho + \Gamma^{\rho}_{\;\tau\mu}\, \tilde{q}^\tau\right)$$

$$\phantom{\Omega_\mu} = \tfrac{1}{4}\!\left(\partial_\mu q^\rho + \Gamma^{\rho}_{\;\tau\mu}\, q^\tau\right) \tilde{q}_\rho \quad\quad \tag{3.88}$$

$$\Gamma^{\rho}_{\;\mu\alpha} = \tfrac{1}{2}\, g^{\rho\lambda}\!\left(\partial_\mu g_{\lambda\alpha} + \partial_\alpha g_{\lambda\nu} - \partial_\lambda g_{\alpha\mu}\right) \quad\quad \tag{2.33b}$$

This gives $\mathcal{L}_E$ as a function of $q_\mu$.

The full Lagrangian is of the form

$$\mathcal{L} = \mathcal{L}_E + \mathcal{L}_M$$
