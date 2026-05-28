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

---

## Page 16

where $\mathcal{L}_M$ is the matter-field.

Now $\mathcal{L}_M$ will have an overall $(-g)^{1/2}$ for the invariant volume element $(-g)^{1/2} d^4x$.

At the next fundamental level, suppose we have only matter fields that are massless and 2-spinors, $\eta$ and $\chi$, where $\tilde{q}^{\mu}\partial_{\mu}\eta = 0$, $\tilde{\sigma}^{\mu}\partial_{\mu}\chi = 0$. Their free Lagrangians then take the form

$$\mathcal{L}_\eta = i\,\eta^{+}q^{\mu}\partial_{\mu}\eta \;-\; i\,\partial_{\mu}\eta^{+}q^{\mu}\eta \qquad \left(q^{\mu+} = q^{\mu}\;\text{etc.}\right)$$

$$\mathcal{L}_\chi = i\,\chi^{+}\tilde{q}^{\mu}\partial_{\mu}\chi \;-\; i\,\partial_{\mu}\chi^{+}\tilde{q}^{\mu}\chi$$

The interaction is added in the canonical fashion, s.t.

$$\boxed{\;\mathcal{L}_M^{\eta} = (-g)^{1/2}\!\left\{ i\,\eta^{+}q^{\mu}\eta_{;\mu} \;-\; i\,\eta_{;\mu}^{+}q^{\mu}\eta \right\}\;}$$

---

$$q_{\mu}\tilde{q}^{\mu} = -4\,\sigma^{0}_{0}$$

$$
\begin{aligned}
q^{\mu} &= q^{\mu}_{i}\,\sigma^{i} \\
        &= q^{\mu}_{4}\sigma_{0} - i\sigma_{1}q^{\mu}_{1} - i\sigma_{2}q^{\mu}_{2} - i\sigma_{3}q^{\mu}_{3} \\[4pt]
\tilde{q}^{\mu} &= -\sigma_{0}q^{\mu}_{4} - i\sigma_{1}q^{\mu}_{1} - i\sigma_{2}q^{\mu}_{2} - i\sigma_{3}q^{\mu}_{3}
\end{aligned}
$$

Sachs writes

$$\tag{3.60} q^{\mu}(x) = \sigma_{\nu}\!\left(\nu\sigma^{\mu}(x)\right) = \begin{pmatrix} 0v^{\mu}-{}_{3}v^{\mu} & -{}_{1}v^{\mu}+i_{2}v^{\mu} \\ -{}_{1}v^{\mu}-i_{2}v^{\mu} & {}_{0}v^{\mu}+{}_{3}v^{\mu} \end{pmatrix}$$

$$\tag{3.62} \tilde{q}^{\mu}(x) = \begin{pmatrix} -{}_{0}v^{\mu}-{}_{3}v^{\mu} & -{}_{1}v^{\mu}+i_{2}v^{\mu} \\ -{}_{1}v^{\mu}-i_{2}v^{\mu} & -{}_{0}v^{\mu}+{}_{3}v^{\mu} \end{pmatrix}$$

---

## Page 17

where

$$\eta_{;\mu} = \partial_{\mu}\eta + \Omega_{\mu}\,\eta$$

Can we simplify this and equate $\chi$ with $\eta^{+}$?

$$\chi = \varepsilon\,\eta^{*}, \qquad \varepsilon = \text{(antisymmetric)}$$

These are time-reflected fields. Space-reflected fields might be better, as

$$\sigma^{\mu}\partial_{\mu}\varphi + i\,m\,\zeta = 0$$
$$-\tilde{\sigma}^{\mu}\partial_{\mu}\zeta + i\,m\,\varphi = 0$$

since weak interactions have to do w/ Left–Right handedness — but I guess this falls out either way, so use $\eta$ and $\chi$.

$$\boxed{\begin{aligned}
\eta_{;\mu} &= \partial_{\mu}\eta + \Omega_{\mu}\,\eta \\
\chi_{;\mu} &= \partial_{\mu}\chi + \Omega^{(\chi)}_{\mu}\chi
\end{aligned}}$$

$$\boxed{\Omega^{(x)}_{\rho} = -\tfrac{1}{4}\,\tilde{q}_{\mu}\!\left(\partial_{\rho}q^{\mu} + \Gamma^{\mu}_{\tau\rho}\,q^{\tau}\right)} \tag{3.77}$$

$$= \tfrac{1}{4}\,q_{\mu}\!\left(\partial_{\rho}\tilde{q}^{\mu} + \Gamma^{\mu}_{\tau\rho}\,\tilde{q}^{\tau}\right) \tag{3.79b}$$

Do we need the hermitian conjugates? Why? I don't think so. These should be equivalent to a single Dirac Bispinor. Then, in concise notation,

$$\boxed{\;\mathcal{L} = (-g)^{1/2}\!\left\{\,R + i\,\eta^{+}q^{\mu}\eta_{;\mu} + i\,\chi^{+}\tilde{q}^{\mu}\chi_{;\mu}\,\right\}\;}$$

as the total Lagrangian.

---

## Page 18

Now, an important question is, where do *complex constants* come in, if they do? (at a fundamental level)

This must also be cleaned up for a Hamiltonian formulation in order to generate a multi-particle quantum formulation.

$$T_{00} = \mathcal{H} = \frac{\partial\mathcal{L}}{\partial\dot{\varphi}}\,\dot{\varphi} - \mathcal{L} \;\equiv\; \pi\,\dot{\varphi} - \mathcal{L}$$

If $\;G_{\mu\nu} = 8\pi\,T_{\mu\nu}$, then $\;T_{00} = \mathcal{H} = \dfrac{1}{8\pi}\,G_{00}$ for the gravitational field itself.

$$G_{\mu\nu} = R_{\mu\nu} - \tfrac{1}{2}g_{\mu\nu}R$$

$$\boxed{\;\frac{\partial\mathcal{L}}{\partial\dot{\varphi}_{\text{E}}} = \tfrac{1}{8\pi}G_{00} = \tfrac{1}{8\pi}\!\left(R_{00} - \tfrac{1}{2}g_{00}R\right)\;}$$

$$\boxed{\begin{aligned}
R_{00} &= R^{\lambda}_{\,00\lambda} = \partial_{\lambda}\Gamma^{\lambda}_{00} - \cdots \\
       &= R^{\lambda}_{\,0\lambda 0} = \partial_{\lambda}\Gamma^{\lambda}_{00} - \partial_{0}\Gamma^{\lambda}_{0\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{00} - \Gamma^{\alpha}_{\beta 0}\Gamma^{\beta}_{0\alpha}
\end{aligned}}$$

$\mathcal{H}$, however, should *not* be expressed merely in terms of $q^{\mu\nu}$, but in terms of independent $g$ and $\Gamma$.

For a field $\varphi$,

$$\pi_{\varphi} = \frac{\partial \mathcal{L}}{\partial(\partial_{0}\varphi)}$$

---

## Page 19

For non-spinor Gen. Rel.,

$$\mathcal{H}_{E} = \tfrac{1}{8\pi}\!\left(R_{00} - \tfrac{1}{2}g_{00}R\right) \qquad \text{(ok)}$$

$$= \tfrac{1}{8\pi}\!\left\{\partial_{\lambda}\Gamma^{\lambda}_{00} - \partial_{0}\Gamma^{\lambda}_{0\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{00} - \Gamma^{\alpha}_{\beta 0}\Gamma^{\beta}_{0\alpha}\right.$$
$$\left.\quad -\;\tfrac{1}{2}g_{00}\!\left[g^{\mu\nu}\!\left(\partial_{\lambda}\Gamma^{\lambda}_{\mu\nu} - \partial_{\mu}\Gamma^{\lambda}_{\nu\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{\mu\nu} - \Gamma^{\alpha}_{\beta\nu}\Gamma^{\beta}_{\mu\alpha}\right)\right]\right\}$$

To keep this 1st order in derivatives, we must treat $\Gamma^{\lambda}_{\mu\nu}$ and $g^{\mu\nu}$ as independent variables and let the formulation derive the relation between them.

For Spinor Gen. Rel.,

$$\mathcal{H}_{E} = \tfrac{1}{8\pi}\!\left(R_{00} - \tfrac{1}{2}g_{00}R\right) \qquad \text{(ok)}$$

$$= \tfrac{1}{8\pi}\!\left\{\tfrac{1}{4}\mathrm{Tr}\!\left(K_{0\lambda}q^{\lambda}\tilde{q}_{0} - q_{0}\tilde{q}^{\lambda}K_{0\lambda} + q^{\lambda}K^{+}_{0\lambda}\tilde{q}_{0} - q_{0}K^{+}_{0\lambda}\tilde{q}^{\lambda}\right)\right.$$
$$\left.\quad + \tfrac{1}{2}g^{0}_{\,0}\tilde{q}^{0}\cdot \tfrac{1}{4}\mathrm{Tr}\!\left(K_{\nu\mu}q^{\mu}\tilde{q}^{\nu} - K_{\nu\mu}\tilde{q}^{\mu}q^{\nu} + q^{\mu}K^{+}_{\mu\nu}\tilde{q}^{\nu} - q^{\nu}K^{+}_{\mu\nu}\tilde{q}^{\mu}\right)\right\}$$

where

$$K_{\rho\lambda} \;\equiv\; \partial_{\rho}\Omega_{\lambda} - \partial_{\lambda}\Omega_{\rho} + \Omega_{\rho}\Omega_{\lambda} - \Omega_{\lambda}\Omega_{\rho}$$

Again, to keep 1st order derivatives, we must treat $\Omega_{\mu}$ and $q^{\mu}$ as separate independent variables.

---

## Page 20

To handle the matter-field Hamiltonian in the spinor case, we use

$$\mathcal{H} = \frac{\partial \mathcal{L}}{\partial(\dot{\eta})}\,\dot{\eta} - \mathcal{L}, \qquad \pi_{\eta} = \frac{\partial \mathcal{L}}{\partial \dot{\eta}}$$

i.e. on

$$\mathcal{L}_M = i\,\eta^{+}q^{\mu}(\partial_{\mu}+\Omega_{\mu})\eta \;+\; i\,\chi^{+}\tilde{q}^{\mu}(\partial_{\mu}+\Omega^{(\chi)}_{\mu})\chi$$

$$\frac{\partial \mathcal{L}_M}{\partial \dot{\eta}} = i\,\eta^{+}q^{0} = \pi_{\eta}, \qquad \frac{\partial \mathcal{L}_M}{\partial \dot{\chi}} = i\,\chi^{+}\tilde{q}^{0} = \pi_{\chi}$$

*(margin):  $\mathcal{L} = A\dot{\eta}$, $\;\partial\mathcal{L}/\partial\dot{\eta} = A$, $\;\mathcal{H} = A\dot{\eta} - A\dot{\eta} = 0\,!$*

So

$$\mathcal{H} = i\,\eta^{+}q^{0}\pi_{\eta} + i\,\chi^{+}\tilde{q}^{0}\pi_{\chi} \;-\; i\,\eta^{+}q^{\mu}(\partial_{\mu}+\Omega_{\mu})\eta \;-\; i\,\chi^{+}\tilde{q}^{\mu}(\partial_{\mu}+\Omega^{(\chi)}_{\mu})\chi$$

$$= \cdots$$

No, we want

$$\mathcal{L}_M = \tfrac{i}{2}\!\left(\eta^{+}q^{\mu}\partial_{\mu}\eta - (\partial_{\mu}\eta^{+})q^{\mu}\eta\right) \;+\; \tfrac{i}{2}\!\left(\chi^{+}\tilde{q}^{\mu}\partial_{\mu}\chi - (\partial_{\mu}\chi^{+})\tilde{q}^{\mu}\chi\right)$$

*(assuming $q^{\mu+} = q^{\mu}$).*

The energy-momentum tensor is

$$\Theta^{\mu\nu} = (\partial^{\nu}\eta^{+})\frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\eta^{+})} + \frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\eta)}\,\partial^{\nu}\eta$$
$$\quad + (\partial^{\nu}\chi^{+})\frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\chi^{+})} + \frac{\partial \mathcal{L}}{\partial(\partial_{\mu}\chi)}\,\partial^{\nu}\chi \;-\; g^{\mu\nu}\mathcal{L}$$

$$= \tfrac{i}{2}\!\left(\eta^{+}q^{\mu}\partial^{\nu}\eta + (\partial^{\nu}\eta^{+})q^{\mu}\eta + \chi^{+}\tilde{q}^{\mu}\partial^{\nu}\chi + (\partial^{\nu}\chi^{+})\tilde{q}^{\mu}\chi\right)$$

---

## Page 21

and

$$\mathcal{H}_M = \Theta^{00} = \tfrac{i}{2}\!\left(\eta^{+}q^{0}(\partial_{0}\eta) + (\partial_{0}\eta^{+})q^{0}\eta + \chi^{+}\tilde{q}^{0}(\partial_{0}\chi) + (\partial_{0}\chi^{+})\tilde{q}^{0}\chi\right)$$

This does not seem right — maybe ok for flat spacetime, but not curved, as this doesn't show any interaction of $\eta$ & $\chi$ with curvature. It seems like $\Theta^{\mu\nu}$ needs to be redefined with covariant derivatives,

$$\Theta^{\mu\nu} = \eta^{+;\nu}\frac{\partial \mathcal{L}}{\partial(\eta^{+}_{;\mu})} + \frac{\partial \mathcal{L}}{\partial(\eta_{;\mu})}\,\eta^{;\nu}$$
$$\quad + \chi^{+;\nu}\frac{\partial \mathcal{L}}{\partial(\chi^{+}_{;\mu})} + \frac{\partial \mathcal{L}}{\partial \chi_{;\mu}}\,\chi^{;\nu} \;-\; g^{\mu\nu}\mathcal{L}$$

$$\mathcal{L}_M = \tfrac{i}{2}\!\left(\eta^{+}q^{\mu}\eta_{;\mu} - \eta^{+}_{;\mu}q^{\mu}\eta\right) + \tfrac{i}{2}\!\left(\chi^{+}\tilde{q}^{\mu}\chi_{;\mu} - \chi^{+}_{;\mu}\tilde{q}^{\mu}\chi\right)$$

$$\Theta^{00} = \tfrac{i}{2}\!\left(\eta^{+}q^{0}\eta_{;0} + \eta^{+}_{;0}q^{0}\eta + \chi^{+}\tilde{q}^{0}\chi_{;0} + \chi^{+}_{;0}\tilde{q}^{0}\chi\right)$$

We must derive classical equations of motion to see if these are correct. Try w/ non-spinor form first. Add a scalar field for matter to interact w/:

$$\mathcal{L}_M = i\,\partial_{\mu}\varphi\,\partial^{\mu}\varphi - \mu^{2}\varphi^{2}$$

or, in G.R.,

$$\mathcal{L}_M = i\,\varphi_{;\mu}\varphi^{;\mu} - \mu^{2}\varphi^{2}$$

---

## Page 22

$$\frac{\partial \mathcal{L}}{\partial(\varphi_{;\mu})} = 2i\,\varphi_{;\mu}$$

$$\mathcal{H}_M = \varphi_{;0}\,\frac{\partial \mathcal{L}}{\partial(\varphi_{;0})} - \mathcal{L}$$

$$= 2i\,\varphi_{;0}\,\varphi^{;0} + i\,\varphi_{;i}\,\varphi^{;i} + \mu^{2}\varphi^{2}$$

But the covariant derivative of a scalar is just the ordinary derivative, so

$$\mathcal{H}_M = i\,\partial_{0}\varphi\,\partial^{0}\varphi + i\,\nabla\varphi\cdot\nabla\varphi + \mu^{2}\varphi^{2}$$

So the total Hamiltonian density, w/ the measure factor, is

$$\boxed{\;\mathcal{H} = \frac{(-g)^{1/2}}{8\pi}\!\left\{\partial_{\lambda}\Gamma^{\lambda}_{00} - \partial_{0}\Gamma^{\lambda}_{0\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{00} - \Gamma^{\alpha}_{\beta 0}\Gamma^{\beta}_{0\alpha}\right.}$$
$$\boxed{\quad\left.-\tfrac{1}{2}g_{00}g^{\mu\nu}\!\left(\partial_{\lambda}\Gamma^{\lambda}_{\mu\nu} - \partial_{\mu}\Gamma^{\lambda}_{\nu\lambda} + \Gamma^{\alpha}_{\beta\alpha}\Gamma^{\beta}_{\mu\nu} - \Gamma^{\alpha}_{\beta\nu}\Gamma^{\beta}_{\mu\alpha}\right)\right\}}$$
$$\boxed{\quad +\; i(-g)^{1/2}\!\left(\partial_{0}\varphi\,\partial^{0}\varphi + i\,\nabla\varphi\cdot\nabla\varphi + \mu^{2}\varphi^{2}\right)\;}$$

$$\frac{d}{dx_{\nu}}\!\left(\frac{\partial \mathcal{L}}{\partial \eta_{\rho,\nu}}\right) - \frac{\partial \mathcal{L}}{\partial \eta_{\rho}} = 0 \qquad \text{Lagrange field eqn.}$$

---

## Page 23 — Lagrangian Approach

The Lagrangian, in concise notation, is

$$\boxed{\;\mathcal{L} = (-g)^{1/2}\!\left\{R + i\,\eta^{+}q^{\mu}\eta_{;\mu} + i\,\chi^{+}\tilde{q}^{\mu}\chi_{;\mu}\right\}\;}$$

where

$$\eta_{;\mu} = \partial_{\mu}\eta + \Omega_{\mu}\,\eta$$
$$\chi_{;\mu} = \partial_{\mu}\chi + \Omega^{(\chi)}_{\mu}\,\chi$$

$$R = \tfrac{1}{4}\mathrm{Tr}\!\left(K_{\mu\nu}q^{\mu}\tilde{q}^{\nu} - K_{\mu\nu}\tilde{q}^{\mu}q^{\nu} + q^{\mu}K^{+}_{\mu\nu}\tilde{q}^{\nu} - q^{\nu}K^{+}_{\mu\nu}\tilde{q}^{\mu}\right)$$

$$\to \;\Omega_{\lambda,\rho} - \Omega_{\rho,\lambda}$$

$$K_{\rho\lambda} = \partial_{\rho}\Omega_{\lambda} - \partial_{\lambda}\Omega_{\rho} + \Omega_{\rho}\Omega_{\lambda} - \Omega_{\lambda}\Omega_{\rho}$$

$$g \equiv -\det g_{\mu\nu}, \qquad \text{or}\;\; g^{\mu\nu} = -\tfrac{1}{2}(q^{\mu}\tilde{q}^{\nu} + q^{\nu}\tilde{q}^{\mu})$$

Now, treating $q^{\mu}$, $\tilde{q}^{\mu}$, $\Omega^{\mu}$ and $\Omega^{(\chi)}_{\mu}$ independently, can we derive equations of motion? We should write all of this out, then apply the Lagrange eqn:

$$\partial^{\nu}\!\left(\frac{\partial \mathcal{L}}{\partial \eta_{\rho,\nu}}\right) - \frac{\partial \mathcal{L}}{\partial \eta_{\rho}} = 0$$

*(margin: No)*

We may use $\;\dfrac{\partial\,\mathrm{Tr}(AB)}{\partial B} = \tilde{A}\;$ to get

$$\frac{\partial(-g)^{1/2}}{\partial \tilde{q}^{\lambda}} = \left(\tfrac{1}{4}q_{\lambda}(-g)^{-1/2}\right)^{*}$$

*(margin: In curved space:)*

$$\left(\frac{\partial \mathcal{L}}{\partial(\eta_{\rho;\nu})}\right)_{\!;\nu} - \frac{\partial \mathcal{L}}{\partial \eta_{\rho}} = 0$$

---

## Page 24

Trying this with $\eta$:

$$\frac{\partial \mathcal{L}}{\partial \eta_{;\mu}} = \frac{\partial}{\partial \eta_{;\mu}}\!\left[(-g)^{1/2}\,i\,\eta^{+}q^{\nu}\eta_{;\nu}\right]$$

$$= (-g)^{1/2}\,i\,\eta^{+}q^{\mu}$$

$$\left(\frac{\partial \mathcal{L}}{\partial \eta_{;\mu}}\right)_{\!;\mu} = \left((-g)^{1/2}\,i\,\eta^{+}q^{\mu}\right)_{\!;\mu}$$

$$= i\,\left\{(-g)^{1/2}_{\;;\mu}\,\eta^{+}q^{\mu} + (-g)^{1/2}\,\eta^{+}_{;\mu}\,q^{\mu} + (-g)^{1/2}\,\eta^{+}q^{\mu}_{\;;\mu}\right\}$$

$$\frac{\partial \mathcal{L}}{\partial \eta} = \cdots\;\frac{\partial \mathcal{L}}{\partial \eta^{+}}$$

If we write the interaction term so that $\mathcal{L} = \mathcal{L}^{+}$, then

$$\mathcal{L}_\eta = \tfrac{1}{2}\!\left[i\,\eta^{+}q^{\mu}\eta_{;\mu} - i\,\eta^{+}_{;\mu}q^{\mu}\eta\right](-g)^{1/2}$$

Then

$$\frac{\partial \mathcal{L}}{\partial \eta} = -\tfrac{1}{2}i\,\eta^{+}_{;\mu}q^{\mu}(-g)^{1/2}$$

$$\frac{\partial \mathcal{L}}{\partial \eta^{+}} = \tfrac{1}{2}i\,q^{\mu}\eta_{;\mu}(-g)^{1/2}$$

$$\left(\frac{\partial \mathcal{L}}{\partial \eta_{;\mu}}\right)_{\!;\mu} = \tfrac{i}{2}\!\left((-g)^{1/2}_{\;;\mu}\,\eta^{+}q^{\mu} + (-g)^{1/2}\eta^{+}_{;\mu}q^{\mu} + (-g)^{1/2}\eta^{+}q^{\mu}_{\;;\mu}\right)$$

$$\left(\frac{\partial \mathcal{L}}{\partial \eta^{+}_{;\mu}}\right)_{\!;\mu} = -\tfrac{i}{2}\!\left((-g)^{1/2}_{\;;\mu}\,q^{\mu}\eta + (-g)^{1/2}q^{\mu}_{\;;\mu}\eta + (-g)^{1/2}q^{\mu}\eta_{;\mu}\right)$$

---

## Page 25

Whereby

(1a) $\quad\tfrac{i}{2}\!\left((-g)^{1/2}_{\;;\mu}\,\eta^{+}q^{\mu}\right) + \tfrac{i}{2}(-g)^{1/2}\!\left(\eta^{+}_{;\mu}q^{\mu} + \eta^{+}q^{\mu}_{\;;\mu} + \eta^{+}_{;\mu}q^{\mu}\right) = 0$

(1b) $\quad -\tfrac{i}{2}(-g)^{1/2}_{\;;\mu}\,q^{\mu}\eta - \tfrac{i}{2}(-g)^{1/2}\!\left(q^{\mu}_{\;;\mu}\eta + q^{\mu}\eta_{;\mu} + q^{\mu}\eta_{;\mu}\right) = 0$

Now $(-g)^{1/2}_{\;;\mu} = 0$ per p. 52 of Notebook 2. This follows from $g = -\det g_{\mu\nu}$ and $g_{\mu\nu;\rho} = g^{\mu\nu}_{\;;\rho} = 0$ &

$$\frac{\partial (-g)^{1/2}}{\partial g^{\rho\sigma}} = -\tfrac{1}{2}(-g)^{1/2}g_{\rho\sigma}$$

Whereby

(2a) $\quad 2\eta^{+}_{;\mu}q^{\mu} + \eta^{+}q^{\mu}_{\;;\mu} = 0$

(2b) $\quad 2q^{\mu}\eta_{;\mu} + q^{\mu}_{\;;\mu}\eta = 0$

What can we say of $q^{\mu}_{\;;\mu}$? $\;\tilde{q}^{\mu}_{\;;\rho} = 0$ per back of Sachs, p. 64. Per notebook p. 42, this gives $q^{\mu}_{\;;\rho} = 0$ too. Whereby

$$\eta^{+}_{;\mu}q^{\mu} = 0$$
$$q^{\mu}\eta_{;\mu} = 0$$

And if $q^{\mu}$ is hermitian, $q^{\mu+} = q^{\mu}$, these are just the same equation,

$$\boxed{\;q^{\mu}\partial_{\mu}\eta + q^{\mu}\Omega_{\mu}\eta = 0\;}$$

---

## Page 26

*(small sketch at top: a coil/spring icon flowing into a rectangular block — perhaps representing a flow or transformation diagram.)*

Next, we want to consider $\mathcal{L}$ and the terms $q^{\mu}$ and $\Omega_{\rho}$. Starting with $\Omega$,

$$\mathcal{L} = (-g)^{1/2}\!\left\{\tfrac{1}{4}\mathrm{Tr}\!\left(K_{\mu\nu}q^{\mu}\tilde{q}^{\nu} - K_{\nu\mu}q^{\mu}\tilde{q}^{\nu} + q^{\mu}K^{+}_{\mu\nu}\tilde{q}^{\nu} - q^{\nu}K^{+}_{\nu\mu}\tilde{q}^{\mu}\right)\right.$$
$$\left.\quad + \tfrac{i}{2}\eta^{+}q^{\mu}(\partial_{\mu}\eta + \Omega_{\mu}\eta) - \tfrac{i}{2}(\partial_{\mu}\eta^{+} + \eta^{+}\Omega^{+}_{\mu})\,q^{\mu}\eta\right\}$$

$$K_{\mu\nu} = \Omega_{\nu,\mu} - \Omega_{\nu,\mu} \quad\text{(antisymmetric in $\mu,\nu$)}$$

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}} = (-g)^{1/2}\,\tfrac{1}{4}\,\frac{\partial}{\partial \Omega_{\rho,\nu}}\mathrm{Tr}\!\left[(\Omega_{\nu,\nu} - \Omega_{\nu;\mu})q^{\mu}\tilde{q}^{\nu}\right.$$
*(margin: Treat $\Omega \;\&\; \Omega^{+}$ as separate variables.)*
$$\quad - (\Omega_{\nu,\mu} - \Omega_{\nu,\nu})\,\tilde{q}^{\mu}q^{\nu} - q^{\mu}(\Omega^{+}_{\nu,\nu} - \Omega^{+}_{\nu,\mu})\tilde{q}^{\nu}$$
$$\left.\quad + q^{\mu}(\Omega^{+}_{\nu,\mu} - \Omega^{+}_{\nu,\nu})\tilde{q}^{\nu}\right]$$

Now we need some formulas:

$$\frac{\partial\,\mathrm{Tr}[AB]}{\partial B_{ij}} = A_{ji}, \qquad \text{or}\;\; \frac{\partial\,\mathrm{Tr}(AB)}{\partial B} = \tilde{A} \;\;(\text{transpose})$$

$$\frac{\partial\,\mathrm{Tr}(ABC)}{\partial B} = A^{t}C^{t}$$

So

$$\frac{\partial}{\partial \Omega_{\rho,\nu}}\mathrm{Tr}\!\left((\Omega_{\nu,\nu} - \Omega_{\nu,\mu})\,q^{\mu}\tilde{q}^{\nu}\right) = (q^{\rho}\tilde{q}^{\nu})^{t} - (q^{\nu}\tilde{q}^{\rho})^{t} = \widetilde{q^{\nu}}\tilde{q}^{\rho} - \widetilde{q^{\rho}}\tilde{q}^{\nu}$$

$$\frac{\partial}{\partial \Omega_{\rho,\nu}}\mathrm{Tr}\!\left((\Omega_{\nu,\nu} - \Omega_{\nu,\nu})\,\tilde{q}^{\mu}q^{\nu}\right) = (\tilde{q}^{\rho}q^{\nu} - \tilde{q}^{\nu}q^{\rho})^{t}$$

---

## Page 27 — Question

G.R. says the world is locally Lorentzian. e.g. in a small enough neighborhood of any given point $x$, in the local coord. sys. at that point, $g_{\mu\nu}(x) \to g^{*}_{\mu\nu} = (1, -1, -1, -1)$. Is this identical to requiring $q^{\mu} \to \sigma^{\mu}$ at that point or not? Could there be a whole set of $q$'s at any point that give the same $g_{\mu\nu}$? Presumably so, like a gauge invariance, with $\sigma^{\mu}g^{\mu\nu} = -\tfrac{1}{2}(q^{\mu\nu}\tilde{q} + q^{\nu}\tilde{q}^{\mu})$ and $q^{\mu} = \sum_{\nu} q^{\mu}_{\;\nu}\sigma^{\nu}$. $q^{\mu}$ is a matrix, $g^{\mu\nu}$ a scalar.

Factor the Lorentz metric,

$$g^{*}_{\mu\nu} = \tfrac{1}{2}(q^{\mu}\tilde{q}^{\mu}) = \begin{cases} 1, & \mu = 0 \\ -1, & \mu = 1,2,3 \end{cases}$$

and

$$g^{\mu\nu} = 0 = -\tfrac{1}{2}(q^{\mu}\tilde{q}^{\nu} + q^{\nu}\tilde{q}^{\mu}), \quad \mu \neq \nu$$

Writing the spinor component form,

$$q^{\mu\nu} = \sum_{\alpha\beta} q^{\mu}_{\;\alpha}\,q^{\nu}_{\;\beta}\,\sigma^{\alpha}\tilde{\sigma}^{\beta}, \qquad \tilde{\sigma}^{\beta} = \begin{cases} \sigma^{0}, & \beta = 0 \\ -\sigma^{\beta}, & \beta = 1,2,3 \end{cases}$$

$$\frac{\partial(\mathrm{Tr}(AB^{\pm}C))}{\partial B} = CA$$

$$\frac{\partial}{\partial B_{mn}}\!\left(\sum_{i,j,k} A_{ij}B_{kj}C_{ki}\right) = \sum_{i} A_{in}C_{mi} = (CA)_{mn} = (A^{t}C^{t})_{mn}$$

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}}\,\mathrm{Tr}\!\left(q^{\mu}(\Omega^{+}_{\nu,\nu} - \Omega^{+}_{\nu,\mu})\tilde{q}^{\nu}\right) = \widetilde{q}^{\nu}q^{\rho} - \widetilde{q}^{\rho}q^{\nu}$$

---

## Page 28

$$\frac{\partial}{\partial \Omega_{\rho,\nu}}\!\left(q_{\mu}(\Omega_{\mu,\nu}^{+} - \Omega^{+}_{\nu,\mu})\tilde{q}^{\nu}\right) = \widetilde{q}_{\rho}\,q_{\nu} - \widetilde{q}_{\nu}\,q_{\rho}$$

So

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}} = \tfrac{1}{4}(-g)^{1/2}\!\left[\widetilde{q^{\nu}\tilde{q}^{\rho}} - \widetilde{q^{\rho}\tilde{q}^{\nu}} - \widetilde{\tilde{q}^{\rho}q^{\nu}} + \widetilde{\tilde{q}^{\nu}q^{\rho}}\right.$$
$$\left.\qquad + \widetilde{q^{\nu}\tilde{q}^{\rho}} - \widetilde{q^{\rho}\tilde{q}^{\nu}} - \widetilde{\tilde{q}^{\rho}q^{\nu}} + \widetilde{\tilde{q}^{\nu}q^{\rho}}\right]$$

$$= \tfrac{1}{4}(-g)^{1/2}\!\left[\widetilde{q^{\nu}}\tilde{q}^{\rho} + \widetilde{q^{\nu}}\tilde{\tilde{q}}^{\rho} + \tilde{q}^{\nu}\widetilde{q^{\rho}} + \tilde{\tilde{q}}^{\nu}\widetilde{q^{\rho}}\right.$$
$$\left.\qquad - \widetilde{q^{\rho}}\tilde{q}^{\nu} - \widetilde{q^{\rho}}\tilde{\tilde{q}}^{\nu} - \tilde{q}^{\rho}\widetilde{q^{\nu}} - \tilde{\tilde{q}}^{\rho}\widetilde{q^{\nu}}\right]$$

Likewise,

$$\frac{\partial \mathcal{L}}{\partial \Omega_{\rho}} = \tfrac{i}{2}\,\eta^{+}q^{\rho}\eta(-g)^{1/2}$$

is a current term.

Now, we need to *(margin: This way above — many a $\sim$)*

$$\left(\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}}\right)_{\!;\nu} = \tfrac{i}{4}(-g)^{1/2}\!\left(\widetilde{q}^{\nu}q^{\rho} + q^{\nu}\widetilde{q}^{\rho} - \widetilde{q}^{\rho}q^{\nu} - q^{\rho}\widetilde{q}^{\nu}\right)_{\!;\nu}$$

This appears to all go to 0 — not good! See notebook 2 p 53.

$$\left(\frac{\partial \mathcal{L}}{\partial \Omega_{\rho,\nu}}\right)_{\!;\nu} = \left[\tfrac{1}{4}(-g)^{1/2}\!\left(\widetilde{q}^{\nu}q^{\rho}\tilde{q}^{\nu} - \widetilde{q}^{\nu}\tilde{q}^{\rho}q^{\nu}\right)\right]_{\!;\nu}$$

And for matrix $(-g)^{1/2}_{\;;\nu} = 0$, so

$$\tfrac{1}{2}\!\left(\widetilde{q}^{\rho}q^{\nu} - \widetilde{q}^{\nu}q^{\rho}\right)_{\!;\nu} = -\tfrac{i}{2}\eta^{+}q^{\rho}\eta$$

Sachs gets 0 on the LHS & gets usual relation of $\Omega$ to $q$... but apparently this

---

## Page 29

doesn't hold! Now, also

We also get, for the field part,

$$\frac{\partial \mathcal{L}}{\partial q^{\lambda}} = (-g)^{1/2}\!\left(-\tfrac{1}{2}\!\left(K^{+}_{\lambda\rho}\widetilde{q}^{\rho} + \widetilde{q}^{\rho}K_{\lambda\rho}\right)^{*} + \tfrac{1}{4}R\,\widetilde{q}^{*}_{\lambda}\right)$$

and

$$\frac{\partial \mathcal{L}_M}{\partial q^{\lambda}} = \left(\tfrac{i}{2}\eta^{+}\eta_{;\lambda} - \tfrac{i}{2}\eta^{+}_{;\lambda}\eta\right)(-g)^{1/2}$$

Need $\;\widetilde{\Omega}^{(\chi)}_{\rho} = -\Omega^{x+}_{\rho} = \Omega_{\rho}\;$

---

## Page 30

*(Page is blank/bleed-through from previous pages — no original content.)*

---

## Page 31 — Motivation & Development of the σ-Matrices

The standard field equation for a scalar field is

$$\partial_\mu \partial^\mu \psi = 0 = (\partial_0^2 - \nabla^2)\psi$$

Generalizing to a non-Lorentzian metric,

$$g_{\mu\nu}\,\partial^\mu \partial^\nu \psi = 0$$

Now, in going to spinors, an operator $\sigma^\mu \partial_\mu$ is proposed such that

$$\sigma^\mu \partial_\mu \psi = 0$$

is the equivalent wave equation, and

$$(\sigma^\nu \partial_\nu)(\sigma^\mu \partial_\mu \psi) = 0$$

is just

$$(\partial_0^2 - \nabla^2)\psi = 0$$

*Margin:*

$$\tilde\sigma_\nu = \begin{cases} +\sigma & \nu = 0 \\ -\sigma & \nu = 1,2,3 \end{cases} \qquad$$

*Spatially reflected version:*
$$\tilde\sigma = \begin{cases} -\sigma & \nu = 0 \\ \sigma & \nu = 1,2,3 \end{cases}$$

This leads to equations for $\sigma$:

$$(\sigma^0)^2 = 1$$

$$(\sigma^i)^2 = 1$$

$$\sigma^\nu \sigma^\mu + \sigma^\mu \sigma^\nu = 0 \quad (\mu \neq \nu)$$

*Verifying that the system is self-consistent:*

$$(-\sigma^0 \partial_0 - \sigma\cdot\nabla)(\sigma^0 \partial_0 - \sigma\cdot\nabla)\psi$$

$$\big(-\partial_0^2 \psi - (\sigma\cdot\nabla)(\sigma_0 \partial_0) + (\sigma_0\partial_0)(\sigma\cdot\nabla) + (\sigma\cdot\nabla)^2\big)\psi$$

$$\tfrac{1}{2}(\sigma_\mu \tilde\sigma_\nu + \sigma_\nu \tilde\sigma_\mu)\,\partial^\mu \partial^\nu \psi = 0 \qquad \text{(symmetrized form)}$$

With $\sigma_\mu = (\sigma_0, \vec\sigma)$ and $\tilde\sigma_\mu = (\sigma_0, -\vec\sigma)$, then

$$\sigma_i \sigma_j + \sigma_j \sigma_i = 0 \qquad$$

$$\tfrac{1}{2}(\sigma_\mu \sigma_\nu + \sigma_\mu \sigma_\mu) = \mathbb{1} \qquad$$

$$\sigma_0 \sigma_i - \sigma_i \sigma_0 = 0 \qquad$$

---

## Page 32 — Question

If $g^{\mu\nu}$ is the Lorentz metric, does this force $q^\mu = \sigma^\mu$? Plainly, no:

$$g^{\mu\nu} = \tfrac{1}{2}\!\left(q^\mu \tilde q^\nu + q^\nu \tilde q^\mu\right)$$

$\sigma^\mu$ forms a Hermitian basis of $2 \times 2$ matrices, so

$$q^\mu = q^\mu_{\,0}\,\sigma^0 - q^\mu_{\,1}\,\sigma^1 - q^\mu_{\,2}\,\sigma^2 - q^\mu_{\,3}\,\sigma^3$$

$$\tilde q^\mu = q^\mu_{\,0}\,\sigma^0 + q^\mu_{\,1}\,\sigma^1 + q^\mu_{\,2}\,\sigma^2 + q^\mu_{\,3}\,\sigma^3$$

---

## Page 33 — Lagrangian Approach to Sachs Electrogravity

Here we will write a Lagrangian for Sachs Electrogravity with two matter fields, and solve for the equations of motion.

$$\mathcal{L} = (-g)^{1/2}\!\left\{\, R + \tfrac{1}{2}\!\left[\,i\eta^{+} q^\mu \eta_{j\mu} - i\eta^{+}_{i\mu}\, q^\mu \eta\,\right] + \tfrac{1}{2}\!\left[\,i\chi^{+}\, \tilde q^\mu \chi_{i\mu} - i\chi^{+}_{j\mu}\, \tilde q^\mu \chi\,\right]\right\}$$

Where

$$\eta_{i\mu} \equiv \partial_\mu \eta + \Omega_\mu\, \eta$$

$$\chi_{j\mu} \equiv \partial_\mu \chi + \Omega_\mu^{(\chi)}\, \chi$$

and

$$\Omega_\mu^{(\chi)} = -\Omega_\mu^{+}$$

$$\sigma^0 g^{\mu\nu} = \tfrac{1}{2}(q^\mu \tilde q^\nu + q^\nu \tilde q^\mu) \qquad g \equiv -\det g_{\mu\nu}$$

$$R = \tfrac{1}{4}\mathrm{Tr}\!\left(K_{\mu\nu}\, q^\mu \tilde q^\nu - K_{\nu\mu}\, q^\mu q^\nu + q^\mu K^{+}_{\mu\nu}\, q^\nu - q^\nu K^{+}_{\mu\nu}\, \tilde q^\mu\right)$$

$$K_{\mu\nu} \equiv \Omega_{\nu{i}\mu} - \Omega_{\mu{i}\nu} = \partial_\mu \Omega_\nu - \partial_\nu \Omega_\mu + \Omega_\mu \Omega_\nu - \Omega_\nu \Omega_\mu$$

In curved spacetime, the Lagrangian equations of motion are

---

## Page 34

$$\left(\frac{\partial \mathcal{L}}{\partial \psi_{;\mu}}\right)_{\!;\mu} - \frac{\partial \mathcal{L}}{\partial \psi} = 0$$

for each independent field variable $\psi$. Here we will treat $q^\mu$, $\Omega_\mu$, $\eta$ and $\chi$ as independent field variables and derive the equations of motion for them.

*(Remainder of page blank.)*

---

## Page 35 — Cellular Automata & Spacetime Geometry (Speculation)

Would it be possible to model spacetime geometry and elementary particle physics using cellular automata?

In other words: links of cells to one another, and their behavior according to those links, leads to geometry, etc.?

Geometry from rules of interaction is implicit in cellular automata rules. For example, in the game of life, a cell is turned on or off depending on its neighbors:

```
      [ 2 ]
[ 1 ] [ A ] [ 3 ]
      [ 4 ]
```

The state of $A$ in the next time increment depends on the state of $A$, 1, 2, 3 & 4 *now*. But, that $A$ depends on 1, 2, 3 & 4 and *not* 23, 47, 217, 1098 **implies** that 1, 2, 3 & 4 are neighbors. And the lists of all neighbors creates a 2D lattice geometry.

> **Dependence implies neighborhood. Rules imply geometry.**

Has anything been written about this? How could we create a cellular automaton that generates a Lorentzian geometry? Could they also generate a time coordinate?

---

## Page 36 — Dimensionality from Connection Number

It would appear that a CA can only establish a certain dimensionality based on the number of connections it can establish.

- A CA with **0 connections** is 0-dimensional.
- A CA with **1 connection** has a sort of 1D structure but cannot form a 1D space.
- CA's with **2 connections** can form 1-dimensional lines & circles.
- CA's with **3 connections** can form a variety of different structures — *Linear Strip, Circular Strip, Möbius Strip*, or 2D lattice.
- **4 connections** can form a 2D lattice or a 3D lattice, or something like a 3D tube or torus.

We could also consider **asymmetric connections** — e.g. if there are two cells $A$ & $B$, the state of $A$ could depend on $B$, but not $B$ on $A$; or $B$ could depend on $A$ in a different way than $A$ on $B$.

---

## Page 37 — Discretized Wave Equation on a CA

For cells to propagate waves / particles they must obey some kind of wave equation, i.e., in 2D,

$$\frac{\partial^2 f}{\partial t^2} - \frac{\partial^2 f}{\partial y^2} - \frac{\partial^2 f}{\partial z^2} = 0$$

where $f$ is in some sense the value of the cell. Presumably we can discretize this by writing

$$\frac{\partial^2 f}{\partial z^2}(x) = \frac{\dfrac{f(x+\Delta x) - f(x)}{\Delta x} - \dfrac{f(x) - f(x-\Delta x)}{\Delta x}}{\Delta x} = \frac{f(x + \Delta x) - 2f(x) + f(x - \Delta x)}{\Delta x^2}$$

etc., or in cellular form,

$$\frac{\partial^2 f}{\partial z^2} \;\to\; f(m,n+1) - 2 f(m,n) + f(m,n-1)$$

so

$$f(m,n,t+1) - 2f(m,n,t) + f(m,n,t-1) = f(m+1,n,t) - 2f(m,n,t) + f(m-1,n,t)$$
$$\quad + f(m,n+1,t) - 2f(m,n,t) + f(m,n-1,t)$$

would be the basic relation, i.e.

$$f(m,n,t+1) = -2f(m,n,t) - f(m,n,t-1) + f(m+1,n,t) + f(m-1,n,t) + f(m,n+1,t) + f(m,n-1,t)$$

The problem with this is that $f(m,n,t+1)$ is *not* dependent just on $f(-,-,t)$ but also on $f(m,n,t-1)$. To get it to depend only on the previous time step we have to make the Dirac reduction and make each cell spinor-valued. Try just a 2-component massless equation:

$$i\hbar \frac{\partial \psi_{+}}{\partial t} = -i\hbar c\, \boldsymbol\sigma \cdot \nabla \psi_{+}$$

---

## Page 38 — Spinor-Valued CA (continued)

With $\hbar = c = 1$,

$$\frac{\partial \psi_{+}}{\partial t} = -\boldsymbol\sigma \cdot \nabla \psi_{+}$$

$$\boldsymbol\sigma \cdot \nabla = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}\frac{\partial}{\partial x} + \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}\frac{\partial}{\partial y} + \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}\frac{\partial}{\partial z}$$

$$\frac{\partial \psi}{\partial t} = \begin{pmatrix} -\partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_z \end{pmatrix} \psi$$

and with $\psi = \begin{pmatrix} f \\ g \end{pmatrix}$,

$$\frac{\partial f}{\partial t} = -\partial_z f - \partial_x g + i\partial_y g$$

$$\frac{\partial g}{\partial t} = -\partial_x f - i\partial_y f + \partial_z g$$

Finite-differencing (centered):

$$\left.\frac{\partial f}{\partial z}\right|_{(x,y,z,t)} \approx \tfrac{1}{2}\!\left(\frac{f(x,y,z+\Delta z, t) - f(x,y,z, t)}{\Delta z} + \frac{f(x,y,z, t) - f(x,y,z - \Delta z, t)}{\Delta z}\right)$$

$$= \frac{1}{2\Delta z}\!\left(f(x,y,z+\Delta z,t) - f(x,y,z-\Delta z,t)\right)$$

giving (with $\Delta = 1$):

$$\boxed{\;\begin{aligned}
f(l,m,n,t+1) - f(l,m,n,t) &= -\tfrac{1}{2}\!\big(f(l,m,n+1,t) - f(l,m,n-1,t)\big) \\
&\quad -\tfrac{1}{2}\!\big(g(l+1,m,n,t) - g(l-1,m,n,t)\big) \\
&\quad +\tfrac{i}{2}\!\big(g(l,m+1,n,t) - g(l,m-1,n,t)\big) \\[4pt]
g(l,m,n,t+1) - g(l,m,n,t) &= -\tfrac{1}{2}\!\big(f(l+1,m,n,t) - f(l-1,m,n,t)\big) \\
&\quad -\tfrac{i}{2}\!\big(f(l,m+1,n,t) - f(l,m-1,n,t)\big) \\
&\quad +\tfrac{1}{2}\!\big(g(l,m,n+1,t) - g(l,m,n-1,t)\big)
\end{aligned}\;}$$

These spinor equations provide relations in which $f(l,m,n,t)$ etc. are dependent only on $t-1$ states — really a 1st-order causal relation.

---

## Page 39 — Numerical Stability Notes

If we made $\Delta x = \Delta y = \Delta z = \tfrac{1}{2}$ while $\Delta t = 1$, then these equations would work with integer-valued complex numbers. I wonder if they're stable.

Let's try to write this in spinor notation:

$$\psi(l,m,n,t+1) = \sigma_0\, \psi(l,m,n,t) - \tfrac{1}{2}\sigma_z\!\big(\psi(l,m,n+1,t) - \psi(l,m,n-1,t)\big)$$
$$\quad - \tfrac{1}{2}\sigma_x\!\big(\psi(\ell+1,m,n,t) - \psi(\ell-1,m,n,t)\big)$$
$$\quad - \tfrac{1}{2}\sigma_y\!\big(\psi(\ell,m+1,n,t) - \psi(\ell,m-1,n,t)\big)$$

> Programming this up certainly does something, but it blows up w/o the $\tfrac{1}{2}$'s there — goes from unity values to values of about 11,000 in ~10 time steps. And, well, $2^{10} = 1024$, so how surprised are we? Putting the $\tfrac{1}{2}$ in brings it down to about 120 — still not ideal.
>
> I wonder if the factor needed to keep it at unity varies much? It "interestingly" seems to stabilize at $\sim 0.43$. In this world, that factor has to do with the speed of light, so to speak. A $\tfrac{1}{2}$ in the above eqn gives $c = 1$. A smaller value gives a smaller $c$. Renormalization of everything sort of like a change of $c$.

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

---

## Page 40

*Blank / back-of-page bleed-through only.*

---

## Page 41 — Quantum Hierarchy Equations of a Free Scalar Field (paper, p. 1)

This paper is intended to take up where my dissertation left off and advance the art of numerical quantum field calculations somewhat. Let us start with the simplest possible example, a massive spin-zero field whose equation of motion is

$$\partial_\mu \partial^\mu \phi + m^2 \phi = 0$$

The corresponding Lagrangian density is

$$\mathcal{L} = \tfrac{1}{2}(\partial_\nu \phi)(\partial^\nu \phi) - \tfrac{1}{2} m^2 \phi^2$$

and the Lagrangian field equation is

$$\partial_\nu\!\left(\frac{\partial \mathcal{L}}{\partial \phi_{,\nu}}\right) - \frac{\partial \mathcal{L}}{\partial \phi} = 0, \qquad \phi_{,\nu} \equiv \partial_\nu \phi \qquad \text{(Goldstein 12-23)}$$

The canonical momentum is

$$\pi_\phi \equiv \frac{\partial \mathcal{L}}{\partial \phi_{,0}} = \partial_0 \phi \qquad \text{(Goldstein 12-53)}$$

*(which we hereinafter refer to as $\partial_0 \phi$).*

and the Hamiltonian density is given by

$$\mathcal{H} = \frac{\partial \mathcal{L}}{\partial \phi_{,0}} \partial_0 \phi - \mathcal{L} \qquad \text{(Goldstein 12-50)}$$

so

$$\mathcal{H} = \tfrac{1}{2}\!\left(\pi_\phi^{\,2} + (\nabla\phi)^2 + m^2 \phi^2\right)$$

The Hamiltonian field equations are

$$\phi_{,0} = \frac{\partial \mathcal{H}}{\partial \pi_\phi} \qquad \pi_{,0} = -\frac{\partial \mathcal{H}}{\partial \phi} \qquad \text{(Goldstein 12-62)}$$

To proceed, we must transform the Hamiltonian

$$H \equiv \int \mathcal{H}(x)\, d^3 x$$

to momentum space, for which we must introduce some Fourier transforms. We want to have a measure that will be Lorentz invariant & easily generalizable. For this purpose we diverge from the dissertation and write

---

## Page 42 — (paper, p. 2)

$$\tilde\phi(k) \equiv 2\omega_k \int \phi(x)\, e^{ik\cdot x}\, d^3 x \qquad \nabla\phi(x) = \int -ik\, \tilde\phi(k)\, e^{-ik\cdot x}\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k}$$

$$\phi(x) = \int \tilde\phi(k)\, e^{-ik\cdot x}\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k} \qquad \text{(also for } \pi\text{)}$$

where

$$\omega_k \equiv \sqrt{k^2 + m^2}$$

This gives

$$\phi(x) = \iint \phi(y)\, e^{ik\cdot y}\, e^{-ik\cdot x}\, d^3 y\, \frac{d^3 k}{(2\pi)^3}$$

$$= \frac{1}{(2\pi)^3} \int \phi(y) \!\left[\int e^{ik(y-x)}\, d^3 k\right]\! d^3 y$$

$$= \int \phi(y)\, \delta^3(y - x)\, d^3 y = \phi(x)$$

given that

$$(2\pi)^3\, \delta^3(x) = \int e^{ik\cdot x}\, dk$$

which is the standard definition of the $\delta$-function.

The advantage of this measure is that

$$\int_k \frac{d^3 k}{(2\pi)^3\, 2\omega_k} = \int_{\vec k} \int_{k_0} 2\pi\, \delta(k^2 - m^2)\, \Theta(k_0)\, \frac{d^4 k}{(2\pi)^4} \qquad \text{(IzZ 3.35)}$$

where $\Theta(x) \equiv 1$ if $x \geq 0$, $\equiv 0$ if $x < 0$. This will be useful later.

Now we transform $\mathcal{H}$ to $k$-space:

$$H = \tfrac{1}{2}\int\!\big(\pi^2 + (\nabla\phi)^2 + m^2\phi^2\big)\, d^3 x$$

$$= \tfrac{1}{2}\iiint \frac{1}{(2\pi)^6 (2\omega_k)(2\omega_p)}\,\Big(\tilde\pi(k)\tilde\pi(p) - k\!\cdot\!p\, \tilde\phi(k)\tilde\phi(p) + m^2\, \tilde\phi(k)\tilde\phi(p)\Big)\, e^{-ik\cdot x}\, e^{-ip\cdot x}\, d^3 k\, d^3 p\, d^3 x$$

---

## Page 43 — (paper, p. 3)

The integration over $x$ is given by

$$\int e^{-i(k+p)\cdot x}\, d^3 x = (2\pi)^3\, \delta^3(k+p)$$

so

$$H = \tfrac{1}{2}\iint \frac{1}{(2\pi)^3\, 2\omega_p\, 2\omega_k}\, \delta^3(k+p)\, \Big(\tilde\pi(k)\tilde\pi(p) + m^2\, \tilde\phi(k)\tilde\phi(p) - k\!\cdot\!p\, \tilde\phi(k)\tilde\phi(p)\Big)\, d^3 k\, d^3 p$$

$$= \tfrac{1}{2}\!\int \frac{1}{(2\pi)^3\, 4\omega_k^2}\Big(\big(\tilde\pi(k)\big)^2 + m^2\big(\tilde\phi(k)\big)^2 + k^2\big(\tilde\phi(k)\big)^2\Big)\, d^3 k$$

$$= \frac{1}{8(2\pi)^3}\int \!\left(\frac{\tilde\pi_k^{\,2}}{\omega_k^2} + \frac{m^2 + k^2}{\omega_k^2}\, \tilde\phi_k^{\,2}\right)\! d^3 k \qquad (\ast)$$

Now we want to write $H$ in terms of creation & annihilation operators, $a_k^+$ and $a_k$, where $a_k^+$ creates and $a_k$ annihilates. Then, to quantize, the operators are made to fulfill

$$[a_k, a_p^+] = (2\pi)^3\, 2\omega_k\, \delta^3(k - p) \qquad \text{(IzZ 3.36)}$$

$$[a_k, a_p] = [a_k^+, a_p^+] = 0$$

whereby

$$\phi(x) = \int\!\big(a_k\, e^{ik\cdot x} + a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3 (2\omega_k)} \qquad \text{(IzZ 3.37a)}$$

or

$$\tilde\phi_k = a_k^+ + a_{-k}$$

and

$$\pi(x) = -i \int \omega_k\, \big(a_k\, e^{ik\cdot x} - a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3 (2\omega_k)} \qquad \text{(IzZ 3.37b)}$$

or

$$\tilde\pi_k = i\omega_k\, a_k^+ - i\omega_k\, a_{-k} = i\omega_k\,(a_k^+ - a_{-k})$$

Substituting these into $(\ast)$ above gives

---

## Page 44 — (false-start algebra, crossed out in original)

*The author began the substitution into $(\ast)$ on this page, but crossed the entire calculation out and re-did it on the next page. For completeness:*

$$H \overset{?}{=} \frac{1}{8(2\pi)^3}\int \Big[-(a_k^+ - a_k)^2 + (a_k^+ + a_k)^2\Big]\, d^3 k$$

$$= \frac{1}{8(2\pi)^3}\int\!\Big[\,-a_k^{+\,2} - a_k^{\,2} + 2 a_k^+ a_{-k} + a_k^{+\,2} + a_{-k}^{\,2} + 2 a_k^+ a_k\,\Big]\, d^3 k$$

$$\overset{?}{=} \frac{1}{2(2\pi)^3}\int a_k^+ a_{-k}\, d^3 k \qquad \text{\small (crossed out)}$$

*Marginal note:* "if we assume $a_k$ commute" — also crossed out, as does the trial commutator $a_k a_k^+ - a_k^+ a_k = \delta$.

A separate side-computation of $\phi(x)\phi(y)$ appears:

$$\phi(x)\phi(y) = \iint\!\big(a_k\, e^{ik\cdot x} + a_k^+\, e^{-ik\cdot x}\big)\!\big(a_p\, e^{ip\cdot y} + a_p^+\, e^{-ip\cdot y}\big)\, dk\, dp$$

$$= \iint\!\Big(a_k a_p\, e^{i(k\cdot x + p\cdot y)} + a_k^+ a_p\, e^{i(p\cdot y - k\cdot x)} + a_k a_p^+\, e^{-i(p\cdot y - k\cdot x)} + a_k^+ a_p^+\, e^{-i(k\cdot x + p\cdot y)}\Big)\, dk\, dp$$

$$= \iint\!\Big(a_k a_p + a_{-k}^+ a_p^+ + a_k^+ a_p + a_k a_p^+\Big)\, e^{i(k\cdot x + p\cdot y)}\, dk\, dp$$

*("...note no sense.")*

---

## Page 45 — (paper, p. 4 — clean redo)

$$H = \frac{1}{2(2\pi)^3}\int \frac{1}{4\omega_k^2}\!\Big(\tilde\pi_k \tilde\pi_{-k} + (m^2 + k^2)\, \tilde\phi_k \tilde\phi_{-k}\Big)\, d^3 k$$

$$= \frac{1}{8(2\pi)^3}\!\int \!\left(\frac{\tilde\pi_k\, \tilde\pi_{-k}}{\omega_k^2} + \tilde\phi_k\, \tilde\phi_{-k}\right)\! d^3 k \qquad (\ast)$$

Now we want to write $H$ in terms of creation & annihilation operators, $a_k^+$ and $a_k$ where $a_k^+$ creates and $a_k$ annihilates. These obey commutation relations

$$[a_k, a_p^+] = (2\pi)^3\, 2\omega_k\, \delta^3(k - p) \qquad \text{(IzZ 3-36)}$$

$$[a_k, a_p] = [a_k^+, a_p^+] = 0$$

whereby

$$\phi(x) = \int\!\big(a_k\, e^{ik\cdot x} + a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k} \qquad \text{(IzZ 3.37a)}$$

or

$$\tilde\phi_k = a_k^+ + a_{-k}$$

with the inverses

$$a_k^+ = \tfrac{1}{2}\!\left(\tilde\phi_k - \tfrac{i}{\omega_k}\,\tilde\pi_k\right) \qquad a_{-k} = \tfrac{1}{2}\!\left(\tilde\phi_k + \tfrac{i}{\omega_k}\,\tilde\pi_k\right)$$

and

$$\pi(x) = -i \int \omega_k\, \big(a_k\, e^{ik\cdot x} - a_k^+\, e^{-ik\cdot x}\big)\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k} \qquad \text{(IzZ 3.37b)}$$

or

$$\tilde\pi_k = i\omega_k\, a_k^+ - i\omega_k\, a_{-k} = i\omega_k\,(a_k^+ - a_{-k})$$

Substituting these into $(\ast)$ gives

$$H = \frac{1}{8(2\pi)^3}\!\int\!\Big[\, -(a_k^+ - a_{-k})(a_{-k}^+ - a_k) + (a_k^+ + a_{-k})(a_{-k}^+ + a_k)\,\Big]\, d^3 k$$

$$= \frac{1}{4(2\pi)^3}\!\int\!\big(\, a_k^+ a_k + a_{-k}\, a_{-k}^+ \,\big)\, d^3 k$$

$$= \frac{1}{4(2\pi)^3}\!\int\!\big(\, a_k^+ a_k + a_k\, a_k^+ \,\big)\, d^3 k$$

$$\boxed{\; H = \tfrac{1}{2}\!\int \omega_k\,\big(a_k^+ a_k + a_k\, a_k^+\big)\, \frac{d^3 k}{(2\pi)^3\, 2\omega_k}\;} \qquad \text{(Ludwig eq.\ 3)}$$

---

## Page 46 (notebook page 5)

Then to derive a hierarchy, we go to discrete space by defining

$$a_j = a_{k_j} \frac{d^3k}{(2\pi)^3 2\omega_k}$$

and writing $H$ as a discrete sum over finite volume elements. Then $H$ becomes

$$H = \sum_{j=-p}^{p} \tfrac{1}{2}\,\omega_j\,(a_j a_j^+ + a_j^+ a_j) \tag{$\boxtimes$}$$

which is the free-field case of eq. 7 in Ludwig [i]. Now we write a Schrödinger equation,

$$i \frac{\partial |\psi\rangle}{\partial t} = H |\psi\rangle \qquad \text{(Ludwig eq. 1)} \quad \text{\textcircled{A}}$$

The eigenstates are written as $|n_{-p}\ldots n_j \ldots n_p\rangle$ which represent $n_j$ particles in the $k_j$ state. This is by definition an eigenstate of $H$ with

$$H |n_{-p}\ldots n_p\rangle = \left[\sum_{j=-p}^{p} \left(n_j + \tfrac{1}{2}\right)\omega_j \right] |n_{-p}\ldots n_p\rangle \qquad \text{(Ludwig eq. 4)} \quad \text{\textcircled{B}}$$

Expand a general state

$$|\psi\rangle = \sum_{n_{-p}\ldots n_p = 0}^{\infty} C_{n_{-p}\ldots n_p}\, |n_{-p}\ldots n_p\rangle \qquad \text{(Ludwig eq. 2)}$$

and substitute into Ludwig [a], giving

$$\sum_{n_{-p}\ldots n_p = 0}^{\infty} i \frac{\partial C_{n_{-p}\ldots n_p}}{\partial t}\, |n_{-p}\ldots n_p\rangle \;=\; \sum_{n_{-p}\ldots n_p = 0}^{\infty} \left[\sum_{j=-p}^{p} \omega_j (n_j + \tfrac{1}{2}) \right] C_{n_{-p}\ldots n_p}\, |n_{-p}\ldots n_p\rangle \qquad \text{(Ludwig eq. 3)}$$

By orthogonality of the basis vectors, we write

$$i \frac{\partial C_{n_{-p}\ldots n_p}}{\partial t} = \sum_{j=-p}^{p} \omega_j \left(n_j + \tfrac{1}{2}\right) C_{n_{-p}\ldots n_p} \qquad (\ast\ast) \quad \text{(Ludwig eq. 15)}$$

---

## Page 47 (notebook page 6)

Now write

$$C_{n_{-p}\ldots n_p} = A\,\psi_N(k_1,\ldots,k_N)$$

The constant $A$ is selected so that $|\psi\rangle$ may be understood as a Schrödinger wavefunction with

$$1 = \langle \psi | \psi \rangle = \sum_{N=0}^{\infty} \int \psi_N^*(k_1\ldots k_N)\, \psi_N(k_1\ldots k_N)\, \frac{d^3k_1}{(2\pi)^3 2\omega_{k_1}}\cdots \frac{d^3k_N}{(2\pi)^3 2\omega_{k_N}} \qquad \text{(Ludwig eq. 19)}$$

In discrete terms,

$$\langle \psi | \psi \rangle = \sum_{N=0}^{\infty} \sum_{k_1\ldots k_N = -p}^{p} |\psi_N(k_1\ldots k_N)|^2 \,\prod_{j=1}^{N} \frac{(\Delta k)^3}{(2\pi)^3 2\omega_{k_j}} \qquad \text{(Ludwig eq. 19)}$$

Compare this with the $C$'s, defined such that

$$1 = \langle \psi | \psi \rangle = \sum_{N=0}^{\infty} \sum_{\sum n_j = N} \left| C_{n_{-p}\ldots n_p}\right|^2 \qquad \text{(Ludwig eq. 8)}$$

Whereby (per Ludwig p.22)

$$C_{n_{-p}\ldots n_p} = \psi_N(k_1\ldots k_N) \cdot \sqrt{\frac{(\Delta k)^{3N}}{\prod_{j=1}^{N}(2\omega_{k_j})}\,\frac{N!}{\prod_{j=-p}^{p} n_j!}}$$

Substituting into $\boxtimes$ $(\ast\ast)$, these factors cancel on both sides yielding

$$i \frac{\partial \psi_N(k_1\ldots k_N)}{\partial t} = \left(\sum_{j=-p}^{p} \tfrac{1}{2}\omega_j + \sum_{j=-p}^{p} n_j \omega_j\right)\psi_N(k_1\ldots k_N)$$

$$\qquad = \sum_{j=-p}^{p} \tfrac{1}{2}\omega_j \,\psi_N(k_1\ldots k_N) + \sum_{j=1}^{N} \omega_{k_j}\, \psi_N(k_1\ldots k_N)$$

Now, we can write

$$K = \sum_{j=-p}^{p} \tfrac{1}{2}\omega_j$$

as a constant, dependent only on the lattice (as usual),

---

## Page 48 (notebook page 7)

and then define

$$|\psi'| = e^{-iKt}\, |\psi|$$

so that

$$i \frac{\partial |\psi'|}{\partial t} = K |\psi'| \;+\; e^{-iKt}\left(i\frac{\partial |\psi|}{\partial t}\right)$$

and thus,

$$i \frac{\partial \psi'_N}{\partial t}(k_1\ldots k_N) = \sum_{j=1}^{N} \omega_{k_j}\, \psi'_N(k_1\ldots k_N) \qquad \text{(Ludwig eq. 3)}$$

The constant $K$ is just the vacuum energy, which we have subtracted away. Thus we may drop the prime on $\psi$, and this is the multiparticle state equation for a free scalar boson. It is perhaps not very interesting, but it illustrates a technique, and brings up a number of issues that arise as a result of that technique which are important.

One problem we immediately see here is that this equation cannot easily be converted back to spacetime coordinates. The presence of $\omega_k = \sqrt{k^2 + m^2}$ acts effectively as an operator $\sqrt{m^2 + \nabla^2}$ that cannot be **differentiated** integrated by a Fourier transform. The derivation seems to single out a single time direction, which is not very elegant, ~~first~~ in defining the Hamiltonian, and then in defining the Schrödinger equation. It would be much nicer if it were entirely covariant. Secondly, it is unclear how the bosonic symmetry, which

---

## Page 49 (notebook page 8)

requires

$$\psi_N(k_1,\ldots,k_i,\ldots,k_j,\ldots,k_N) = \psi_N(k_1,\ldots,k_j,\ldots,k_i,\ldots,k_N)$$

is enforced. This is very important and must be understood.

It is to be supposed that some of the issues of coordinate space will be easier to work out with Dirac spinors, as well as issues of a covariant presentation, since the Dirac equation is linear first order in its derivatives, whereas the Klein–Gordon equation can't be written as a 1st order equation in the first place. Thus we will defer these issues to the development of the spinor formulation of these systems. However, it would be good to understand the boson symmetry here now before we try to tackle antisymmetric fermions.

Bose and Fermi statistics are enforced by the commutation relations. Bose particles must have creation and annihilation operators that commute. Fermi particles have operators that anti-commute.

---

## Page 50 (bleed-through / blank)

*Page is blank — only a faint mirror image of pen pressure from the verso shows through. No content to transcribe.*

---

## Page 51

Going from $\text{\textcircled{A}}$ to $\text{\textcircled{B}}$:

$$\mathcal{H} = \tfrac{1}{2}(\pi_j \pi_{-j} + \omega_j^2 \phi_j \phi_{-j})$$

$$i \frac{\partial}{\partial t} |n_{-p}\ldots n_p\rangle = \sum_{j=-p}^{p} \tfrac{1}{2}\,\omega_j\,(a_j a_j^+ + a_j^+ a_j)\, |n_{-p}\ldots n_p\rangle$$

is the Schrödinger equation, where $|n_{-p}\ldots n_p\rangle$ is taken as an eigenstate of $H$.

$$a_k^+ = \tfrac{1}{2}\!\left(\phi_{-k} - \frac{i}{\omega_k}\pi_k\right) \qquad a_k = \tfrac{1}{2}\!\left(\phi_k + \frac{i}{\omega_k}\pi_{-k}\right) \qquad \big[a_k = (a_{-k}^+)^*\big]$$

In quantum theory, $\pi_j = i\hbar\,\dfrac{\partial}{\partial \phi_j}$.

The state $|n_{-p}\ldots n_p\rangle$ is a wave function that is a function of the value of $\phi$ at each $k_j$:

$$|n_{-p}\ldots n_p\rangle = \Psi(\phi_{-p},\ldots,\phi_j,\ldots,\phi_p)$$

Rather than speaking of the value of the field $\phi$ at any point $k_j$, we speak of a probability density of the field at that point, given by

$$P(\phi_j) = \int \Psi^* \Psi\,\bigl(\phi_{-p},\ldots,\phi_p\bigr)\, d\phi_{-p}\cdots d\phi_{j-1}\, d\phi_{j+1}\cdots d\phi_p$$

Now we should get a harmonic oscillator at any point, and if we were sloppy about $k$ and $-k$ we could get it right off — but this is oversimplistic.

$$N_j = a_j^+ a_j \qquad H = \sum \omega_j N_j \qquad a_j a_j^+ - a_j^+ a_j = 0$$

$$a_k^+ a_k = \tfrac{1}{4}\!\left(\phi_k - \frac{i}{\omega_k}\pi_k\right)\!\!\left(\phi_{-k} + \frac{i}{\omega_k}\pi_{-k}\right)$$

$$\qquad\quad = \tfrac{1}{4}\!\left(\phi_k \phi_{-k} - \frac{i}{\omega_k}(\pi_k \phi_{-k} - \phi_k \pi_{-k}) + \frac{1}{\omega_k^2}\pi_k \pi_{-k}\right)$$

It is **overly simplistic** to say $a_k^+ a_k$ are creation & annihilation operators for a "harmonic oscillator."

---

## Page 52

[chain-rule sidebar at the top:]

$x = f(x', y')$

$$\frac{\partial}{\partial x} = \frac{\partial x'}{\partial x}\frac{\partial}{\partial x'} + \frac{\partial y'}{\partial x}\frac{\partial}{\partial y'} = \tfrac{1}{\sqrt{2}}\!\left(\frac{\partial}{\partial x'} + \frac{\partial}{\partial y'}\right)$$

$$a_j^+ a_j = N_j, \qquad a_j |n_{-p}\ldots n_j\ldots n_p\rangle = \sqrt{n_j}\,|n_{-p}\ldots n_j-1\ldots n_p\rangle$$
$$a_j^+ |n_{-p}\ldots n_j\ldots n_p\rangle = \sqrt{n_j+1}\,|n_{-p}\ldots n_j+1\ldots n_p\rangle$$
$$a_j^+ a_j |n_{-p}\ldots n_j\ldots n_p\rangle = n_j\,|n_{-p}\ldots n_j\ldots n_p\rangle$$
$$a_j a_j^+ |n_{-p}\ldots n_j\ldots n_p\rangle = (n_j+1)\,|n_{-p}\ldots n_j\ldots n_p\rangle$$

So $\tfrac{1}{2}(a_j^+ a_j + a_j a_j^+) = (N_j + \tfrac{1}{2})\;\checkmark$.

This gets us from $\boxtimes$ to $\ast\ast$.

$$\mathcal{H} \simeq \frac{\pi_k \pi_{-k}}{\omega_k^2} - \omega_k^2\,\phi_k \phi_{-k}$$

If it were $\pi^2$ and $\phi^2$ we could do harmonic oscillators. As it is, each of these is more like a coupled pair of oscillators. It's like having a system $\psi(x,y) = \cdots$

$$\mathcal{H}\psi = -\hbar^2\frac{\partial^2}{\partial x\,\partial y}\psi(x,y) - \omega_0^2 x y\,\psi(x,y) = E_0\,\psi \quad \text{\textcircled{C}}$$

instead of

$$-\hbar^2\,\frac{\partial^2 \psi}{\partial x^2} + \omega^2 x^2\,\psi(x) = E_0\,\psi$$

What kind of mess is this? What if we rotate $\text{\textcircled{C}}$ $45°$ so that

$$x^* = \tfrac{1}{\sqrt{2}}(x' + y'), \qquad x' = \tfrac{1}{\sqrt{2}}(x + y)$$
$$y^* = \tfrac{1}{\sqrt{2}}(x' - y'), \qquad y' = \tfrac{1}{\sqrt{2}}(x - y)$$

$$xy = \tfrac{1}{2}(x'+y')(x'-y') = \tfrac{1}{2}(x'^2 - y'^2)$$

$$\frac{\partial}{\partial x} = \tfrac{1}{\sqrt{2}}\!\left(\frac{\partial}{\partial x'} + \frac{\partial}{\partial y'}\right) \qquad \frac{\partial}{\partial y} = \tfrac{1}{\sqrt{2}}\!\left(\frac{\partial}{\partial x'} - \frac{\partial}{\partial y'}\right)$$

$$\frac{\partial^2}{\partial x\,\partial y} = \tfrac{1}{2}\!\left(\frac{\partial^2}{\partial x'^2} - \frac{\partial^2}{\partial y'^2}\right)$$

so

$$\mathcal{H}\psi \simeq -\tfrac{1}{2}\frac{\partial^2 \psi(x', y')}{\partial x'^2} + \tfrac{\omega^2}{2}x'^2\,\psi \;-\; \tfrac{1}{2}\frac{\partial^2 \psi}{\partial y'^2} - \tfrac{\omega^2}{2}y'^2\,\psi$$

One is a positive harmonic oscillator; the other negative. These perhaps correspond to sin and cos waves.

$$a_{\cos}^+ = \tfrac{1}{2}\!\left(x + \tfrac{i}{\omega}\pi_x\right), \qquad a_x = \tfrac{1}{2}(y - \cdots)$$

---

## Page 53

Bose statistics mean that $\psi$ must be completely symmetric w.r.t. the exchange of any pair of particles. It must be set up by hand to be this symmetric. See Messiah V.2 pp.586–600. Since there is no interaction with a free field, maintaining this symmetrization is trivial.

If I apply creation & annihilation operators, their commutator relations enforce the symmetry, e.g.

$$a_k^+ a_p^+ |\psi\rangle = a_p^+ a_k^+ |\psi\rangle$$

since $a_k^+ a_p^+ - a_p^+ a_k^+ = 0$. It may be of interest to see how the creation & annihilation operators are written in the Schrödinger representation we are discussing. Part of it is that $|n_{-p}\ldots n_j\ldots n_p\rangle$ naturally reflects the degeneracies, as one particle in slot $j$ is the same as any other. Thus,

$$|n_{-p}\ldots n_j\ldots n_p\rangle \;\longrightarrow\; \psi_N(\underbrace{-p,-p,-p,\ldots}_{n_{-p}\text{ times}}\;\ldots\;j,j,j\;\ldots\;\underbrace{p,p,p,\ldots}_{n_p\text{ times}})$$

and this $\psi_N$ must be symmetric, i.e. $\psi_N = S\psi_N = \dfrac{1}{N!}\sum_P P\,\psi_N$.

---

## Page 54

$$\bar\phi_p = \tfrac{1}{\sqrt{2}}(\phi_p + \phi_{-p}) \qquad \widetilde{\phi}_q = \tfrac{1}{\sqrt{2}}(\phi_p - \phi_{-p})$$

$$\phi_k = \tfrac{1}{\sqrt{2}}(\bar\phi_p + \widetilde{\phi}_q), \qquad \phi_{-k} = \tfrac{1}{\sqrt{2}}(\bar\phi_p - \widetilde{\phi}_q)$$

Let $\alpha_p^+$ create $\bar\phi_p$ and $\beta_q^+$ create $\widetilde{\phi}_q$:

$$\alpha_p^+ = \tfrac{1}{2}\!\left(\bar\phi_p - \tfrac{i}{\omega_p}\bar\pi_p\right), \qquad \beta_q^+ = \tfrac{1}{2}\!\left(\widetilde{\phi}_q - \tfrac{i}{\omega_q}\widetilde{\pi}_q\right)$$

$$\alpha_p = \tfrac{1}{2}\!\left(\bar\phi_p + \tfrac{i}{\omega_p}\bar\pi_p\right), \qquad \beta_q = \tfrac{1}{2}\!\left(\widetilde{\phi}_q + \tfrac{i}{\omega_q}\widetilde{\pi}_q\right)$$

$$\bar\phi_k = \alpha_k^+ + \alpha_k, \qquad \widetilde{\phi}_k = \beta_k^+ + \beta_k$$
$$\bar\pi_k = i\omega_k(\alpha_k^+ - \alpha_k), \qquad \widetilde{\pi}_k = i\omega_k(\beta_k^+ - \beta_k)$$

Then if $\phi_k = \tfrac{1}{\sqrt{2}}(\bar\phi_p + \widetilde{\phi}_q)$, we can create $\phi_k$ with

$$\phi_k = a_k^+ + a_{-k}$$

$$a_k^+ = \tfrac{1}{\sqrt{2}}(\alpha_p^+ + \beta_q^+)$$

$$\quad = \tfrac{1}{2}\!\left(\tfrac{1}{\sqrt{2}}\!\left(\bar\phi_p - \tfrac{i\bar\pi_k}{\omega_k}\right) + \tfrac{1}{\sqrt{2}}\!\left(\widetilde{\phi}_q - \tfrac{\widetilde\pi_q}{\omega_k}\right)\right)$$

$$\quad = \tfrac{1}{2}\!\left(\tfrac{1}{\sqrt{2}}(\bar\phi_p + \widetilde{\phi}_q) - \tfrac{i}{\omega_k}\tfrac{1}{\sqrt{2}}(\bar\pi_k + \widetilde{\pi}_q)\right)$$

$$\quad = \tfrac{1}{2}\!\left(\phi_k - \tfrac{i}{\omega_k}\pi_k\right)$$

$$a_k = \tfrac{1}{\sqrt{2}}(\alpha_p + \beta_q) = \tfrac{1}{\sqrt{2}}\!\left(\phi_k - \tfrac{i}{\omega_k}\pi_k\right)$$

(Standard rep uses $\alpha_p^+ = \left(\sqrt{\omega}\,\bar\phi_p - \tfrac{1}{\sqrt{\omega_p}}\bar\pi_p\right)$ etc.)

$$h_k \sim \alpha_k^+ \alpha_k + \alpha_k \alpha_k^+ \;-\; \beta_k^+ \beta_k - \beta_k \beta_k^+$$

If $\phi(x)$ is real, what can we say about $\phi_k$?

$$\phi_k = 2\omega_k \int \phi(x)\,e^{ik\cdot x}\,d^3x$$

$$\quad = 2\omega_k \int \phi(x)\cos(k\!\cdot\!x)\,d^3x \;+\; i\,2\omega_k\int \phi(x)\sin(k\!\cdot\!x)\,d^3x$$

$$\phi_{-k} = 2\omega_k \int \phi(x)\cos(k\!\cdot\!x) - i\phi(x)\sin(k\!\cdot\!x)\,d^3x$$

$$\phi_k - \phi_{-k} = 0 \quad\Longrightarrow\quad \widetilde{\phi}_q = 0$$

---

## Page 55

$$H = \frac{1}{8(2\pi)^3}\int \left(\frac{\pi_k \pi_{-k}}{\omega_k^2} + \phi_k \phi_{-k}\right) d^3k$$

$$\quad = \frac{1}{16(2\pi)^3} \int \frac{1}{\omega_k^2}\!\left(\bar\pi_k^2 + \omega_k^2 \bar\phi_k^2 \;+\; \widetilde\pi_k^2 + \omega_k^2 \widetilde\phi_k^2\right) d^3k$$

$$\quad = \tfrac{1}{8}\int \frac{d^3k}{(2\pi)^3 \, 2\omega_k}\,\frac{1}{\omega_k}\!\left(\bar\pi_k^2 + \omega_k^2 \bar\phi_k^2 + \widetilde\pi_k^2 + \omega_k^2 \widetilde\phi_k^2\right)$$

Note that $\bar\phi_k = \bar\phi_{-k}$ and $\widetilde\phi_k = -\widetilde\phi_{-k}$.

Introduce $\alpha_k$, $\beta_k$ operators now so that

$$H = \frac{1}{16(2\pi)^3}\int \frac{d^3k}{\omega_k}\!\left(-(\alpha_k - \alpha_k^+)^2 + (\alpha_k^+ + \alpha_k)^2\right) + (\beta)$$

$$\quad = \frac{1}{16(2\pi)^3}\int d^3k\,\Big(-\alpha_k^+\alpha_k^+ - \alpha_k \alpha_k + \alpha_k^+\alpha_k + \alpha_k \alpha_k^+ \;+\; \alpha_k^+\alpha_k^+ + \alpha_k\alpha_k + \alpha_k^+\alpha_k + \alpha_k\alpha_k^+\Big)$$

$$\quad = \frac{1}{8(2\pi)^3}\int \left(\alpha_k^+ \alpha_k + \alpha_k\alpha_k^+ + \beta_k^+\beta_k + \beta_k\beta_k^+\right) d^3k$$

$$\quad = \tfrac{1}{4}\int \omega_k\!\left(\alpha_k^+\alpha_k + \alpha_k\alpha_k^+ + \beta_k^+\beta_k + \beta_k\beta_k^+\right) \frac{d^3k}{(2\pi)^3 2\omega_k}$$

Two sets of particles described here. Can antisymmetric be done away with due to non-Bose statistics?

[ink-blot redaction at lower right, partial commutator algebra below visible:]

$$[\alpha_k,\alpha_p^+]\,f \quad \text{with } \pi_k = i\frac{\partial}{\partial\phi_k}$$

$$= \tfrac{1}{4}\!\left(\phi_k + \tfrac{i}{\omega_k}\frac{\partial}{\partial\phi_k}\right)\!\!\left(\phi_p - \tfrac{i}{\omega_p}\cdots\right)\,f$$

$$\;\;\vdots\;\;\;\text{(further algebra, partly obscured by ink blot)}$$

$$= \tfrac{i}{4}\!\left[\,\phi_k\phi_p\,f - \tfrac{i}{\omega_p}\phi_k\frac{\partial f}{\partial\phi_p} + \phi_p\,(\text{partial})\,f - \tfrac{i}{\omega_p}\phi_p\,\frac{\partial f}{\partial\phi_p}\right]$$

$$= \tfrac{1}{4}\Big(\cdots - \tfrac{i}{\omega_p}(\partial\phi_p/\partial\phi_k)\,f + \phi_p\,(\cdots) - \tfrac{i}{\omega_p}\,\frac{\partial}{\partial\phi_p}f + \phi_p\,(\cdots)\Big)$$

---

## Page 56

$$a_k^+ = \tfrac{1}{\sqrt{2}}(\alpha_k^+ + i\beta_k^+), \qquad a_k = \tfrac{1}{\sqrt{2}}(\alpha_k - i\beta_k)$$

create pure $\phi_k$ particles

$$a_k^+ a_k + a_k a_k^+ = \tfrac{1}{2}\Big((\alpha_k^+ + i\beta_k^+)(\alpha_k - i\beta_k) + (\alpha_k - i\beta_k)(\alpha_k^+ + i\beta_k^+)\Big)$$

$$\quad = \tfrac{1}{2}\Big(\alpha_k^+\alpha_k + \beta_k^+\beta_k + i(\beta_k^+\alpha_k - \alpha_k^+\beta_k) + \alpha_k\alpha_k^+ + \beta_k\beta_k^+ - i\beta_k\alpha_k^+ + i\alpha_k\beta_k^+\Big)$$

Can we say anything about these 4 terms,

$$T = \tfrac{1}{2}i\,\big(\beta_k^+\alpha_k - \alpha_k^+\beta_k + \beta_k\alpha_k^+ - \alpha_k\beta_k^+\big)\;?$$

If $\alpha$ and $\beta$ all commute, then

$$\beta_k^+\alpha_k - \alpha_k\beta_k^+ = 0$$

so

$$T = \alpha_k^+\beta_k + \alpha_k\beta_k^+$$

No, **but** $\alpha_k = \alpha_{-k}$, $\beta_k = -\beta_{-k}$, whereby

$$T_k = -T_{-k}$$

and

$$\int T_k\, d^3k \;=\; 0$$

---

## Page 57 (inserted printed page — Sakurai-style angular momentum text, oriented sideways)

*This page is a photocopy / insertion from a printed textbook section "2. Angular Momentum Algebra Representations of Angular Momentum Operators," not handwritten notes. Equation references on the page include (2.20)–(2.22b). The visible content includes:*

The matrix elements are the integrals

$$\langle j', m' | J_\pm | j, m \rangle = \delta_{j j'}\,\delta_{m', m\pm 1}\sqrt{(j\mp m)(j\pm m + 1)}$$

In the case of angular momentum $j = \tfrac{1}{2}$, we obtain the Pauli matrices.

$$(J_x)_{m m'} = \tfrac{1}{2}\!\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = \tfrac{1}{2}\sigma_x$$

and

$$(J_y)_{m m'} = \tfrac{1}{2}\sigma_y, \qquad (J_z)_{m m'} = \tfrac{1}{2}\sigma_z \tag{2.22}$$

In the case of angular momentum $j = 1$ (absolute value $\sqrt{2}\hbar$) we obtain three-dimensional matrices with $m = -1, 0, 1$:

$$S_x = \tfrac{1}{\sqrt{2}}\!\begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}, \quad
S_y = \tfrac{1}{\sqrt{2}}\!\begin{pmatrix} 0 & -i & 0 \\ i & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad
S_z = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & -1 \end{pmatrix} \tag{2.22a}$$

In the same way we used the spinors $\chi_+, \chi_-$ and $\chi_\pm \tfrac{1}{2}$ to describe the states with spin $\tfrac{1}{2}$, we now may use the vectors $\chi_m$, i.e.

$$\chi_1 = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}, \;\; \chi_0 = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \;\; \chi_{-1} = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$$

which represent the possible states for spin 1. Hence, the vectors $\chi_m$ are eigenstates of the matrix $S_z$.

*[Right column of the printed page — partially legible:]*

This will be the velocity-like spin 1 behaves like a part of, the photon (as a vector field) has spin 1. The relation $\text{Eq.}(0) \to$ representation in (2.21)

For higher spin we obtain analogous matrices:

$$S_x = \tfrac{1}{\sqrt{2}}\!\begin{pmatrix} 0 & \sqrt{3} & 0 & 0 \\ \sqrt{3} & 0 & 2 & 0 \\ 0 & 2 & 0 & \sqrt{3} \\ 0 & 0 & \sqrt{3} & 0 \end{pmatrix},$$

$$S_y = \cdots$$

$$S_z = \tfrac{1}{2}\!\begin{pmatrix} 3 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & -3 \end{pmatrix} \tag{2.22b}$$

which have matrix elements as components. We mapping in such representations are not closed in quantum mechanics, in part as a product of irreducible representations.

EXERCISES — *(headings only visible)*

---

## Page 58 (mostly blank verso of the inserted printed page)

*Blank apart from faint vertical column rules from the printed page on the verso. No handwritten content.*

---

## Page 59 — "Complex mass" (dated 9/6/2007)

**Complex mass**

The usual Dirac equation takes the form

$$i\hbar\,\frac{\partial}{\partial t}\Psi = i\hbar c\,\vec\alpha \cdot \nabla \Psi + \beta\, m_0 c^2\,\Psi \tag{1}$$

This is the result of taking the square root of

$$\sqrt{p^2 c^2 + m^2 c^4} \tag{2}$$

using matrices $\vec\alpha$, $\beta$, i.e.

$$\bigl(\vec\alpha \cdot \vec p\, c + m c^2 \beta\bigr)^2 = (p^2 c^2 + m^2 c^4)\,\mathbb{I} \tag{3}$$

Interestingly, the choice of these matrices need not be unique. ~~For example,~~ A typical representation of these matrices is given by

$$\alpha_i = \sigma_3 \otimes \sigma_i, \qquad \beta = -\sigma_1 \otimes \sigma_0 \tag{4}$$

where

$$\sigma_0 = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad
\sigma_1 = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad
\sigma_2 = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad
\sigma_3 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \tag{5}$$

We might simply look at the fact that one could just as well write

$$\beta = (a\,\sigma_1 + b\,\sigma_2)\otimes \sigma_0 \tag{6}$$

where $a^2 + b^2 = 1$ and get the same solution of (3) above. Normally this choice of the $\alpha$ and $\beta$ are considered arbitrary, and left at that. Then one picks a convenient representation & solves the equation.

---

## Page 60

Suppose, however, that these representations were gauged, so that they weren't the same from point to point. This seems to introduce an $SU(2)$ gauge symmetry of sorts into the system. If we start by just looking at the symmetries in $\beta$ for a fixed $\alpha$, then we can write a general $\beta_g$ of the form $\beta$ using the $\beta$ in (4) via the formula

$$\beta_g = (U \sigma_1 U^+)\otimes \sigma_0$$

where

$$U = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{pmatrix}$$

If we gauge $U$, then $\theta = \theta(x)$. It is fascinating to note that such a gauge symmetry acts on only one half of the bispinor. In this, the Weyl representation, that half of the bispinor corresponds to one particular helicity. This would seem to tie in with the weak interaction, which is also helicity-dependent and *thus related to mass*, and which involves an $SU(2)$ symmetry that is **broken**, while here we're looking at an $SU(2)$ symmetry broken by $U(1)$.


---

## Page 61 — Weak Interactions

1. The weak interaction bosons, $W_\pm, Z$, act only on the **left**-handed half of the Dirac spinor of a 4-spinor.
2. The electromagnetic interaction boson, $\gamma$ or $A$, acts only on the **bottom** part of the 4-spinors
   $$\binom{\nu_L}{e_L}\qquad \binom{\nu_R}{e_R}$$
3. The $L \leftrightarrow R$ interaction creates, or defines, mass. $W_\pm$ and $Z$, which make a distinction here, have mass. Does their having mass have to do with the $L$-only coupling? Or does it have to do with its charge?
4. *(blank — author started numbering a 4th point but did not continue)*

---

## Page 62 — Weinberg–Salam w/o Higgs

We try to formulate W–S without the Higgs since it isn't physical, and we don't worry about renormalizability or gauge violation of mass terms yet.

Introduce 2 fields, $\vec W^\mu$ an $SU(2)$ field and $W_0^\mu$, a $U(1)$ field. Call
$$L = \binom{\nu_L}{e_L}, \qquad R = \binom{\nu_R}{e_R}.$$

Then
$$\vec G^{\mu\nu} = \partial^\mu \vec W^\nu - \partial^\nu \vec W^\mu - g\, \vec W^\mu \times \vec W^\nu$$
$$H^{\mu\nu} = \partial^\mu W_0^\nu - \partial^\nu W_0^\mu$$

and
$$\mathcal L = -\tfrac14\!\left(\vec G^{\mu\nu}\!\cdot\!\vec G_{\mu\nu} + H^{\mu\nu} H_{\mu\nu}\right) \;-\; m_\nu c^2\!\left(\bar L_\nu R_\nu + \bar R_\nu L_\nu\right) \;-\; m_e c^2\!\left(\bar L_e R_e + \bar R_e L_e\right)$$
$$\hphantom{\mathcal L =}\; + \bar L\, i\,\bar\sigma^\mu D^L_\mu L \;+\; \bar R\, i\,\bar\sigma^\mu D^R_\mu R$$

with covariant derivatives
$$D^L_\mu \equiv \partial_\mu + i g\, \vec W_\mu \!\cdot\! \vec\tau + i g'\, W_{0\mu}\, \tau_0 \qquad (\text{where } \tau_a = \tfrac{1}{2}\sigma_a \text{ on the } \nu\text{-}e\text{ doublet})$$
$$D^R_\mu \equiv \partial_\mu + i e\, A_\mu (\tau_3 - \tau_0)$$

and $A_\mu$ is a linear combination of $W_0$ and $W_3$. Part of our problem here is that conventional W–S throws out $\nu_R$ and makes $e_R$ a singlet. That's stupid because it destroys the basic ⟶

---

## Page 63

⟶ symmetry between $\binom{\nu_R}{e_R}$ and $\binom{\nu_L}{e_L}$ which is the key to deeper understanding. Now if we give $\vec W$ and $W_0$ masses, the mass term would be
$$\mathcal L_m = \tfrac12 m_W^2 \vec W_\mu \!\cdot\! \vec W^\mu + \tfrac12 m_{W_0}^2 W_{0\mu} W_0^\mu$$
but of course these screw up the gauge symmetry, as terms that go as $W'_\mu = W_\mu + \partial_\mu \Theta$ aren't invariant.

Now W–S has $W_0$ coupling to both $e_L$ and $\nu_L$ and one wants an electromagnetic interaction that operates only on $e_L$. This is obtained by combining $W_0$ and $W_3$ in a linear combination. In other words, we have
$$(\bar\nu_L\ \bar e_L)\!\left(\partial_\mu + i g\, W^1_\mu \tau_1 + i g\, W^2_\mu \tau_2 + i g\, W^3_\mu \tau_3 + i g' W_{0\mu}\right)\!\binom{\nu_L}{e_L}$$

So the last two terms look like
$$i\!\begin{pmatrix} g + g' & 0 \\ 0 & -g + g' \end{pmatrix}\;\longrightarrow\; i\!\begin{pmatrix} g W^3_\mu + g' W^0_\mu & 0 \\ 0 & -g W^3_\mu + g' W^0_\mu\end{pmatrix}$$

So we want to write
$$W^3_\mu = Z_\mu \cos\theta - A_\mu \sin\theta \qquad Z_\mu = \cos\theta\, W^3_\mu + \sin\theta\, W^0_\mu$$
$$W^0_\mu = Z_\mu \sin\theta + A_\mu \cos\theta \qquad A_\mu = -\sin\theta\, W^3_\mu + \cos\theta\, W^0_\mu$$

in such a way that $A_\mu$ doesn't couple to $\nu_L$. That is,
$$g\, W^3_\mu + g'\, W^0_\mu = \alpha\, Z_\mu$$

---

## Page 64

or, substituting,
$$\alpha Z_\mu = g(Z_\mu \cos\theta - A_\mu \sin\theta) + g'(Z_\mu \sin\theta + A_\mu \cos\theta)$$
$$= (g\cos\theta + g'\sin\theta) Z_\mu + (g'\cos\theta - g\sin\theta) A_\mu$$

so
$$\boxed{\;\frac{g'}{g} = \tan\theta\;} \quad (*)$$
gives what we want — an $A_\mu$ that does not couple to $\nu_L$. We also want $A$'s coupling to $e_L$ to be $e$, so
$$g\, W^3_\mu + g'\, W^0_\mu = e A_\mu + \beta Z_\mu$$

so substituting,
$$g(Z_\mu \cos\theta - A_\mu \sin\theta) + g'(Z_\mu \sin\theta + A_\mu \cos\theta) = e A_\mu + \beta Z_\mu$$

and, separately,
$$g'\cos\theta + g\sin\theta \;\to\; e \quad\text{(should be }-g\sin\theta\text{ — sign flipped)}$$
$$g\cos\theta - g'\sin\theta = \beta$$

And using $(*)$ above,
$$e = g'\cos\theta - g\sin\theta = g\sin\theta + g\sin\theta = 2g\sin\theta$$
$$\beta = g\cos\theta - g'\sin\theta = g\cos\theta - g\tan\theta\sin\theta = \tfrac12 e\,(\cot\theta - \tan\theta)$$

*(margin: the author flips a sign somewhere; both forms are kept as written.)*

---

## Page 65

These results are in accord with Huey p. 108, 109. They're really not too extraordinary, in as much as such a rotation, in combination with $g, g'$ chosen at will, allows one to fit theory to experiment. It would appear strange that a massless vector boson $A_\mu$ should emerge from this. The right-handed doublet also poses problems! After all, it doesn't couple to $Z$ at all, and only to $A$. Yet the $A$ consists partly of $W^3_\mu$ and so by symmetry it should couple to $W_+, W_-$ too.

Let's look at the mass term
$$\mathcal L_m = \tfrac12 m_W^2 \vec W_\mu \!\cdot\! \vec W^\mu + \tfrac12 m_{W_0}^2 W_{0\mu} W_0^\mu$$
$$= \tfrac12 m_W^2 W_{\mu 1} W_1^\mu + \tfrac12 m_W^2 W_{\mu 2} W_2^\mu + \tfrac12 m_W^2 W_{\mu 3} W_3^\mu + \tfrac12 m_{W_0}^2 W_{0\mu} W_0^\mu$$

and substituting our formulae for $W_3$ and $W_0$, we get
$$\mathcal L_{m_{30}} = \tfrac12 m_W^2 W_{\mu 3} W_3^\mu + \tfrac12 m_{W_0}^2 W_{\mu 0} W_0^\mu$$
$$= \tfrac12 m_W^2 (Z_\mu \cos\theta - A_\mu \sin\theta)^2 + \tfrac12 m_{W_0}^2 (Z_\mu \sin\theta + A_\mu \cos\theta)^2$$
$$= \tfrac12 m_W^2 Z_\mu^2 \cos^2\theta + \tfrac12 m_W^2 A_\mu^2 \sin^2\theta - \tfrac12 m_W^2 Z_\mu A^\mu \sin\theta\cos\theta$$
$$\quad + \tfrac12 m_{W_0}^2 Z_\mu^2 \sin^2\theta + \tfrac12 m_{W_0}^2 A_\mu^2 \cos^2\theta + m_{W_0}^2 Z_\mu A_\mu \sin\theta\cos\theta$$

$$\Rightarrow\quad m_Z^2 = m_W^2 \cos^2\theta + m_{W_0}^2 \sin^2\theta$$
$$m_A^2 = m_W^2 \sin^2\theta + m_{W_0}^2 \cos^2\theta$$

W–S gets $\;m_Z^2 = \dfrac{m_W^2}{\cos^2\theta}$.

---

## Page 66

Perhaps a better way to see it is to say $m_W$ and $m_{W_0}$ are wholly from $m_Z$ and $m_A = 0$. Thus,
$$\tfrac12 m_Z^2 Z_\mu^2 = \tfrac12 m_W^2 W_3^2 + \tfrac12 m_{W_0}^2 W_0^2$$
$$Z_\mu = W_{3\mu}\cos\theta + W_{0\mu}\sin\theta$$
$$\tfrac12 m_Z^2 Z_\mu^2 = \tfrac12 m_Z^2 W_{3\mu}^2 \cos^2\theta + \tfrac12 m_Z^2 W_{0\mu}^2 \sin^2\theta + m_Z^2 W_{0\mu} W_{3\mu}\sin\theta\cos\theta$$

So $\;m_Z^2 \cos^2\theta = m_W^2 \quad\Longrightarrow\quad \boxed{\;m_Z^2 = \dfrac{m_W^2}{\cos^2\theta}\;}$

This is the W–S model prediction. However, there is an anomalous term,
$$\mathcal L_{\text{Anom}} = m_Z^2\, W_{0\mu} W_{3\mu}$$
and what happens to it? Presumably, it is transformed away or hidden somehow.

It seems like the kinetic term would pose a similar problem.

---

## Page 67

Now let's get some new ideas. $A_\mu$ works on the isospin vector just like $W$ works on the spin vector. In other words, $A_\mu$ couples to $\binom{\nu_L}{e_L}$ like
$$\begin{pmatrix} 0 & 0 \\ 0 & 1\end{pmatrix} = \tfrac12 (\tau_0 + \tau_3)$$
and $W$ couples to $\binom{e_R}{e_L}$ as
$$\begin{pmatrix} 0 & 0 \\ 0 & 1\end{pmatrix} = \tfrac12 (\sigma_0 + \sigma_3) \ldots \text{identical}.$$
This kind of cross coupling looks very elegant. Can we write a more concrete theory? A completely massless one to start? Or is the mass/charge fundamental and endemic to the theory?

OK, the mass terms take the form
$$mc^2 \bar\psi \psi = mc^2 (\bar R L + \bar L R)$$

So we have
$$\mathcal L_{\text{mass}} = m_e c^2 (\bar e_R e_L + \bar e_L e_R) + m_\nu c^2 (\bar\nu_R \nu_L + \bar\nu_L \nu_R)$$

The complement to this mass term in isospin space would be
$$\mathcal L_{\text{weak}} = g\,(\bar\nu_L e_L + \bar e_L \nu_L) + g'\,(\bar\nu_R e_R + \bar e_R \nu_R)$$

Interestingly $m_\nu \approx 0$ and $g' \approx 0$ and both interactions have the same nature. This is not at all a dynamically mediated force, but rather more like a contact force. But like mass, we should understand that it really arises dynamically, from a field.

---

## Page 68

It would appear that this is, or very nearly is, what the original Fermi theory of weak interactions comprised. Clearly it does not explain neutral currents, or the particulate nature of $W_\pm, Z$. Yet we might find these as we add kinetic and gauge terms.

The non-interacting kinetic term for the $\binom{e_R}{e_L}$ or $\binom{\nu_R}{\nu_L}$ takes the form
$$(\bar e_R\ \bar e_L)\!\left(\tfrac{\partial}{\partial t} - \sigma_3 \otimes \vec\sigma\!\cdot\!\nabla\right)\!\binom{e_R}{e_L}$$
etc. What would a complementary kinetic term be for the weak interaction? Presumably
$$(\bar\nu_L\ \bar e_L)\!\left(\tfrac{\partial}{\partial t} - \tau_3 \otimes \vec\sigma\!\cdot\!\nabla\right)\!\binom{\nu_L}{e_L}$$

Yet if we put one of these in, what is the need for the other? If we have an $\bar e_L \tfrac{\partial}{\partial t} e_L$ term for one, isn't it there for the other too? The big question appears to be, are these consistent? Can they be made consistent?

While we are at it, perhaps we should use a gauge field with them too. In other words, the pair $\binom{e_R}{e_L}$ can transform as $\psi_e \to e^{i\theta(x)} \psi_e$. However, at the same time, $\psi_\nu \to \psi_\nu$ because the charge of $\nu$ is $0$ and generally speaking $\psi \to e^{i Q \theta(x)} \psi$. Plainly then, a pair $\binom{\nu_L}{e_L}$ will not transform the same, and is not $U(1)$ symmetric for this gauge symmetry. Yet it ⟶

---

## Page 69

*(Two Feynman diagrams at the top:)*
- *Left: charged current.* $\nu_\mu \to \mu^- $ via $W^-$, with $\nu_e \to e^-$ on the other vertex. Labelled "charge current."
- *Right: neutral current.* $\nu_\mu \to \nu_\mu$ via $Z$, with $e^- \to e^-$ on the other vertex. Labelled "neutral current."

⟶ would appear that another $U(1)$ field could be introduced such that $\binom{\nu_L}{e_L} \to e^{i\phi(x)}\binom{\nu_L}{e_L}$ while $\binom{\nu_R}{e_R} \to \binom{\nu_R}{e_R}$. This gauge field would, in fact, provide the neutral currents we need, although it wouldn't particulate $W_\pm$.

If we call $A_\mu$ the usual electromagnetic field, and $B_\mu$ the new field, then the two kinetic terms would be of the form
$$i\hbar(\partial_0 + i g A_0)\!\binom{e_R}{e_L} - i\hbar c \sigma_3 \!\otimes\! \left[\vec\sigma\!\cdot\!(\nabla + i g\vec A)\right]\!\binom{e_R}{e_L}$$
$$+\; i\hbar(\partial_0 + i g A_0)\!\binom{\nu_R}{\nu_L} - i\hbar c \sigma_3\!\otimes\!\left[\vec\sigma\!\cdot\!(\nabla + i g\vec A)\right]\!\binom{\nu_R}{\nu_L}$$

and
$$i\hbar(\partial_0 + i g B_0)\!\binom{\nu_L}{e_L} - i\hbar c \sigma_3 \!\otimes\! \left[\vec\sigma\!\cdot\!(\nabla + i g\vec B)\right]\!\binom{\nu_L}{e_L}$$
$$+\; i\hbar(\partial_0 + i g_R B_0)\!\binom{\nu_R}{e_R} - i\hbar c \sigma_3\!\otimes\!\left[\vec\sigma\!\cdot\!(\nabla + i g_R \vec B)\right]\!\binom{\nu_R}{e_R}$$

where $g_\nu \approx 0$ and $g_R \approx 0$. Note that $g_\nu$ has nothing, per se, to do with $m_\nu$ and $g_R$ has nothing per se, to do with $g'$ in our "mass" equations, but, amazingly, $g_\nu = 0, m_\nu = 0, g_R = 0, g' \approx 0$, making a perfect symmetry between the two equations.

If I work out all of the kinetic terms, what do I get? Will I see a "why" to all of these zeros? Or understand why $B$ should end up with an effective mass? And all of this seems to have something to do with the gauging of the mass term.

Above all, we don't want **different** kinetic terms. If they all get doubled, we can absorb it somewhere, but if we have $2 \partial_0 e_R + \partial_0 e_R$ then we can't do that.

---

## Page 70

OK, the pure kinetic terms will be ($\hbar = c = 1$)
$$\binom{i\partial_0 e_R - i\vec\sigma\!\cdot\!\nabla e_R}{i\partial_0 e_L + i\vec\sigma\!\cdot\!\nabla e_L} \;+\; \binom{i\partial_0 \nu_R - i\vec\sigma\!\cdot\!\nabla \nu_R}{i\partial_0 \nu_L + i\vec\sigma\!\cdot\!\nabla \nu_L}$$
$$\binom{i\partial_0 \nu_L - i\vec\sigma\!\cdot\!\nabla \nu_L}{i\partial_0 e_L + i\vec\sigma\!\cdot\!\nabla e_L} \;+\; \binom{i\partial_0 \nu_R - i\vec\sigma\!\cdot\!\nabla \nu_R}{i\partial_0 e_R + i\vec\sigma\!\cdot\!\nabla e_R}$$

Combining terms, we have
$$\binom{i\bar\sigma_\mu \partial^\mu e_R + i\sigma_\mu \partial^\mu \nu_R + i\sigma_\mu \partial^\mu \nu_L}{2 i\sigma_\mu \partial^\mu e_L + i\sigma_\mu \partial^\mu \nu_L + i\sigma_\mu \partial^\mu e_R}$$
where $\sigma_\mu \partial^\mu = \partial_0 - \vec\sigma\!\cdot\!\nabla$, $\;\bar\sigma_\mu \partial^\mu = \partial_0 + \vec\sigma\!\cdot\!\nabla$, and we do get inconvenient factors of 2 here. If we flip $\binom{e_R}{e_L} \to \binom{e_L}{e_R}$ as I think we may need to, then the kinetic terms become
$$\binom{i\bar\sigma_\mu \partial^\mu e_L + 2 i\sigma_\mu \partial^\mu \nu_L + i\sigma_\mu \partial^\mu \nu_R}{2 i\sigma_\mu \partial^\mu e_R + i\bar\sigma_\mu \partial^\mu \nu_R + i\bar\sigma_\mu \partial^\mu e_L}$$

Now there is a 2 on both particles that couple to only one of $A_\mu, B_\mu$, and a single term for those that couple to both or neither. In any case all particles have 2 kinetic terms that don't cancel.

This is becoming an ugly way to write equations of motion like this. We shall instead use a quadruplet $(e_L\ e_R\ \nu_L\ \nu_R)$ or some such thing. I don't want to go that way yet — but only pursue the symmetry between the two separated equations to understand the neutral current.

---

## Page 71

The neutral current is mediated by $B_\mu$. In Lagrangian language it's something like
$$(\bar\nu_L\ \bar e_L)\!\left(-g_L (B_0 + \sigma_3 \vec B)\right)\!\binom{\nu_L}{e_L}$$
and equivalent to
$$(\bar e_L\ \bar e_R)\!\left(-e(A_0 + \sigma_3 \vec A)\right)\!\binom{e_L}{e_R}$$

This differs from Weinberg in that the cross-couplings $\nu_L e_L$ have a variable field acting between them, instead of a constant. The connection, where "mass" arises dynamically, is of great interest.

**Key questions:**

**Q)** Neutral current aside, what is the experimental evidence that the coupling between $\nu_L$ and $e_L$ is a particle, and not merely a mass term?

**A)** The obvious answer lies in the fact that a decay like $\mu^- \to e^- + \bar\nu_e + \nu_\mu$ exists. If it were merely a "mass term" it couldn't happen. You'd need higher order terms connecting $\mu$ and $e$, etc., unless of course the neutral current alone was responsible for all such transactions (which may be, but not by the Fermi-style representation of things). By particulizing the contact interaction, a $\mu, \nu_\mu$ doublet can give off a $W_-$ which then acts on an $e, \nu_e$ doublet easily enough.

**Q)** If $W_\pm$ are the dynamic expression of a contact term between $e, \nu_e$, then could there be a ⟶

---

## Page 72

⟶ similar dynamic nature to mass, e.g. the contact term $m(\bar e_L e_R + \bar e_R e_L)$ is really mediated by a boson of some sort?

**A)** That might be true.

**Q)** How would $\mu$ decay work in a mass-term-like theory with only a neutral current?

**A)**

i) $\mu_L$ couples to $\nu_L$ via a direct contact $\;\mu_L \times \nu_\mu\;$
ii) $\nu_\mu$ radiates a $B_\mu$, which then decays into a pair of $\bar\nu_e, e$'s. *(margin: "i.e. $\nu_e \bar\nu_e$.")* One $\nu_e$ turns into an $e$ by the contact interaction.

Clearly in this scenario, charge conservation is violated temporarily. This leads back to viewing charge as a dynamic quantity, not static, and the idea that a Heisenberg uncertainty principle is in operation for it too, like $\Delta p \Delta x \geq \hbar$, $\Delta E \Delta t \geq \hbar$. In a normal mass term, there are things like $\bar e_R \times e_L$ which make angular momentum get violated temporarily, too, e.g., $L_z$. Both charge and angular momentum seem to have to do with a rotational variable too.

---

## Page 73 — Mass & rotational travel

Suppose that a particle, rather than being able to travel in a straight line $\longrightarrow$ had to travel in a helical spiral *(little drawn helix)*. Then it would have a lower forward velocity.

To describe a helix in $x$-$y$-$z$ space, we suppose the direction of travel is along $z$, and the helix has diameter $r$ and frequency $\nu$. Thus,
$$\vec X(t) = r\cos(2\pi\nu t)\,\hat x + r\sin(2\pi\nu t)\,\hat y + a t\,\hat z$$

We wish to find $\dfrac{dz}{dt}$ as a function of $|\vec v|$.
$$\vec v(t) = \dot{\vec X}(t) = -2\pi\nu r \sin(2\pi\nu t)\,\hat x + 2\pi\nu r\cos(2\pi\nu t)\,\hat y + a\,\hat z$$
$$\vec v\!\cdot\!\vec v = 4\pi^2 \nu^2 r^2 + a^2 \qquad \frac{dz}{dt} = a$$

Now supposing that $|\vec v| = c$ and $\dfrac{dz}{dt}$ is $v_{\text{eff}}$, the effective velocity, then
$$c^2 = 4\pi^2 \nu^2 r^2 + v_{\text{eff}}^2$$
or
$$v_{\text{eff}} = \sqrt{c^2 - 4\pi^2 \nu^2 r^2}$$
whereby the effective velocity can be reduced arbitrarily with such a "trick." Now,
$$E^2 = p^2 c^2 + m^2 c^4$$
coupled with a quantum understanding of $E$ and $p$ also relates speed to frequencies & wavelengths.

---

## Page 74

$$\hbar^2 \omega^2 = \tfrac{4\pi^2}{\lambda^2}\,\hbar^2 c^2 + m^2 c^4 = \hbar^2 \nu^2 c^2 + m^2 c^4$$
$$\frac{\hbar^2 \omega^2}{m^2 c^2} = v^2 + c^2$$
$$v_{\text{eff}} = \sqrt{\frac{\hbar^2 \omega^2}{m^2 c^2} - c^2}$$

Here, the larger $\omega$ is, the larger $v$ is. Yet $v$ can apparently go to $\infty$ with this formulation. That isn't right!

$p \neq m v$, $\;p = m v = \dfrac{m_0 v}{\sqrt{1 - v^2/c^2}}$
$$\hbar^2 \omega^2 = \frac{m_0^2 v^2 c^2}{1 - v^2/c^2} + m_0^2 c^4$$
$$\hbar^2 \omega^2 (1 - v^2/c^2) = m_0^2 v^2 c^2 + m_0^2 c^4 (1 - v^2/c^2)$$
$$\hbar^2 \omega^2 (c^2 - v^2) = m_0^2 v^2 c^4 + m_0^2 c^4 (c^2 - v^2)$$
$$\hbar^2 \omega^2 c^2 - \hbar^2 \omega^2 v^2 = m_0^2 v^2 c^4 + m_0^2 c^6 - m_0^2 c^4 v^2$$
$$\hbar^2 \omega^2 c^2 - m_0^2 c^6 = (\hbar^2 \omega^2 + m_0^2 c^4 - m_0^2 c^4) v^2$$
$$v^2 = c^2 - \frac{m_0^2 c^4}{\hbar^2 \omega^2} = c^2 - \frac{E_0^2}{E^2}$$

**Way way — no good.**

---

## Page 75 — Reference: Ferbel (ASI)

*(Reference page — bibliographic data from a textbook the author was reading. Top header:)*

**NATO Advanced Science Institutes Series — Techniques & Concepts of High Energy Physics — Thomas Ferbel, Vol 7, Plenum Press NY**

Selected numerical values copied from the book:

$$m_W = 80.22 \pm 0.26\ \text{GeV (exp)} \quad \text{vs}\quad 80.213 \pm .12$$
$$80.10 \pm .27\ \text{theory w/ LEP}$$

$$m_W^2 = \frac{\pi\alpha}{\sqrt 2\, G_F\, \sin^2\theta_W} \qquad m_Z^2 = \frac{\pi\alpha}{\sqrt 2\, \bar\rho\, G_F\, \sin^2\theta_W \cos^2\theta_W}$$
$$\bar\rho = 1 + \frac{3\sqrt 2}{16\pi^2} G_F\, m_t^2 \qquad \sin^2\theta_W = \frac{e^2}{g^2} = 1 - \frac{m_W^2}{\bar\rho\, m_Z^2}$$

$$m_Z = 91.187 \pm .007\ \text{GeV (LEP)}$$
$$m_\tau = 1776.9^{+.4}_{-.5} \pm .2\ \text{MeV}$$
$$\tau_\tau = 296.8 \pm 3.2\ \text{fs lifetime, so}\quad \frac{G_F^\tau}{G_F^\mu} = 0.987 \pm .006\quad (2.2\sigma\text{ away from standard!})$$

$$1 - \left(\frac{m_W}{m_Z}\right)^2 = 0.2283 \pm 0.0026 \qquad \sin^2\theta_W = .232 \pm .009$$

$$\sigma_{\nu_\mu e} = \frac{2 G_F^2 m_e}{\pi}\, E_\nu \!\left[(g_{Ve} + g_{Ae})^2 + \tfrac13 (g_{Ve} - g_{Ae})^2\right]$$
$$\frac{\sigma_{\bar\nu_\mu e}}{\sigma_{\nu_\mu e}} = 3\,\frac{1 - 4\sin^2\theta_W + \tfrac{16}{3}\sin^4\theta_W}{1 - 4\sin^2\theta_W + 16\sin^4\theta_W}$$

$$g_{Ve} = -0.075 \pm 0.020,\quad g_{Ae} = -.503 \pm 0.017\quad \text{ref Z3p.125}$$

At LEP: $g_{V\ell} = -0.372 \pm .0029$, $\;g_{A\ell} = -.4999 \pm 0.0009$.
At LEP: $\sin^2\theta_W = .2319 \pm .0007 \;\Rightarrow\; m_t = 160^{+16+16}_{-17-20}\ \text{GeV}$.
Vol 9 has $m_t = 175 \pm 6$ w/ 172 for standard model.

---

## Page 76 — Majorana mass / Fermi 4-particle

**Majorana mass term** violates charge conservation, but not for neutrinos:
$$M_D \bar\psi_L \psi_R + \tfrac12 M_L \bar\psi_L (\psi_L)^c + \tfrac12 M_R \bar\psi_R (\psi_R)^c + \text{h.c.}$$

Written in matrix form:
$$\tfrac12 \bar\Psi\!\begin{pmatrix} M_L & M_D \\ M_D^+ & M_R\end{pmatrix}\!\Psi^c + \text{h.c.}$$

Margin: "*ln V10 p 265*"

|  | (book) |
|---|---|
| $m_{\nu_e} < 3.4\ \text{eV}$ | $15\ \text{eV}$ |
| $m_{\nu_\mu} < 160\ \text{keV}$ | $170\ \text{keV}$ |
| $m_{\nu_\tau} < 24\ \text{MeV}$ | $18.2\ \text{MeV}$ |

*Reference noted:* "The Physics of Massive Neutrinos — Francois Vannucci, LPNHE Univ Paris 7, 4 Place Jussieu Tour 33, 75252 Paris."

**Fermi 4-particle interaction** for $n \to p\, e^-\,\bar\nu_e$:
$$\mathcal L_F = -\frac{G_F}{\sqrt 2}\, \bar p\, \gamma_\lambda n\, \bar e\, \gamma^\lambda \nu_e$$
$$G_F = 1.167 \times 10^{-5}\ \text{GeV}^{-2}$$

Parity:
$$J_\mu \sim V_\mu - A_\mu$$
$$V^\mu = \bar\psi\gamma^\mu\psi \quad\xrightarrow{P}\quad +\bar\psi\gamma^\mu\psi \;\;/\;\; -\bar\psi\gamma_\mu\psi$$
$$A^\mu = \bar\psi\gamma^\mu\gamma^5\psi \quad\xrightarrow{P}\quad -\bar\psi\gamma^\mu\gamma^5\psi \;\;/\;\; \bar\psi\gamma_\mu\gamma^5\psi$$

Parity violation comes from $\mathcal L \sim J_\mu J^\mu$.
**V–A Theory** Feynman & Gell-Mann:
$$\mathcal L_{VA} = -\frac{G_F}{\sqrt 2}\, J_\mu^{\ell\ell}\, J^{\mu\ell\,+}$$
$$J_\mu^{\ell\ell} = \bar\nu_e \gamma_\mu (1 - \gamma_5) e + \bar\nu_\mu \gamma_\mu (1 - \gamma_5)\mu + \bar\nu_\tau \gamma_\mu (1 - \gamma_5)\tau$$

---

## Page 77 — Program for Weak Interaction Physics

We have shown the similarity between a massive free Dirac equation and a reduced weak interaction. The difference between this and what is observable is that the equivalent of a mass term in the weak interaction violates charge conservation, at least when charge is seen as a property of a particle.

However, a mass term in the free Dirac equation apparently violates spin conservation too. Yet with free Dirac we understand that there's a bigger concept — angular momentum conservation — which holds the conservation principle. When the mass term flips spin it creates angular momentum in the field, so that $S_{-1/2} \to S_{1/2}$ is compensated with $J_N \to J_{N+1}$. Perhaps charge should be understood in a better way too, such that it is partly due to intrinsic properties of a particle, and partly not. These intrinsic qualities, then, would become $W_\pm$ bosons in a more advanced theory.

With such an understanding, we might then turn around and understand mass as arising quite naturally from another field.

**Greiner Rel QM, p. 216, 217** — Shows $J$ commutes w/ $H$ w/ spherical potential:
$$J = L + S = L + \tfrac12 \hbar \vec\Sigma$$
$$[L, \vec\alpha\!\cdot\!\vec p] = i\hbar\, \vec\alpha \times \vec p \qquad (\vec L = \vec r \times \vec p)$$
$$\vec\Sigma = \begin{pmatrix}\vec\sigma & 0 \\ 0 & \vec\sigma\end{pmatrix}\qquad [S, \vec\alpha\!\cdot\!\vec p] = \tfrac12 \hbar [\vec\Sigma, \vec\alpha\!\cdot\!\vec p] = -i\hbar\, \vec\alpha \times \vec p \;=\; -\tfrac{i}{\hbar}(\vec r \times \nabla)$$

---

## Page 78 — Black-body Radiation

$$\bar n_\omega = \frac{1}{e^{\hbar\omega/kT} - 1}$$
$$dN_\omega = \frac{V}{\pi^2 c^3}\,\frac{\omega^2\, d\omega}{e^{\hbar\omega/kT} - 1}$$
$$E \sim \omega N$$

Visible spectrum (nm):
- Red: 620–750
- Green: 495–570
- Blue: 450–495

*(Rest of page blank.)*

---

## Page 79

How does a gauge theory with a massive WB reduce to a contact interaction as $m_{WB} \to \infty$? Can the contact interaction be modeled as a 2-point term instead of a 4-point term? Can we do this naively, with a simple mass term and ignore the Higgs?

Think of something like:

*(diagram: $\mu^- \to \nu_\mu$ at one vertex via $W^-$, which gives $\bar\nu_e + e^-$ at the other vertex. Standard 4-fermion vertex with $W^-$ propagator.)*

Taking $m_{W^-} \to \infty$ with a corresponding change in $G$ pulls the $W$ line in to zero length:

*(diagram: same as above, but $W^-$ propagator collapsed to a single 4-fermion point.)*

This is a 4-point interaction. Suppose, however, there was still a neutral current with a non-infinite mass WB, or a mass-like term between $\mu_L, \nu_{\mu L}$, etc. Then, we'd have interactions like this:

*(diagram: $\mu_L \to \nu_{\mu L}$ via a $\times$ ("mass") vertex; then $\nu_{\mu L} \to \bar\nu_{eL}$ via a $B_0$ exchange to an $e^- \to \nu_{eL}$ pair at the other end. A second $\times$ symbol on the lepton line on the right.)*

Instant-by-instant, charge is **not** conserved in this diagram. What would it be like for the electromagnetic current? $B_0$ seems like it would correspond to a spinless photon. Maybe we should let $W_\pm$ exist but not $Z$, similar to spin $\pm 1$ photons & no spin 0 photon?

---

## Page 80

Then a neutral current interaction must look like:

*(diagram top: $e_L^-, e_L^+$ scatter via $Z$ exchange to $\bar e_L, e_L^+$. The $Z$-line connects two crossed-vertex pairs.)*

$\Downarrow$

*(diagram middle: same external legs, but $Z$ replaced by two $\times$ ("mass") vertices joined by an internal $\bar\nu_e \to W_- \to \bar\nu_e$ chain, showing the neutral current as two contact interactions linked by a charged $W$ exchange.)*

plus 3 other possibilities. Much like:

*(diagram bottom: photon-band scattering — $e_L^+ \to \bar e_R^+ \to e_R^+$ via two crossed vertices, photon $\gamma_{s=+1}$ exchanged, then $e_L^- \to \bar e_R^- \to e_L^+$ on the other side.)*

This allows photon-based scattering in this mode, though there is no spin-0 photon. But here $W_\pm$ are just like two spin states of one field — not really separate fields. How can we formulate that mathematically and get the charge states to come out, just like spin states come out for a photon??

The analogy we're drawing clearly suggests that the exchange particles are neutral in the first analysis, if the symmetry is to hold. And if the $B$ should have mass then $A$ has a certain interaction with the $W_\pm$ reduced to "weak mass."

We obviously lose charge conservation with a weak mass — naively speaking, and yet somehow Dirac conserves $L$ despite a mass term. How??

---

## Page 81

Somehow there is an interchange between $L$ and $S$ so that $J = L + S$ is conserved although $L$ is not and $J$ is not. One might even say that $S$ was invented to save $L$ conservation. Thus, for example,
$$\overline{e_L} \xrightarrow{\,\times\, m\,} e_R$$
happens and it doesn't bother anyone. We need to understand the details of how that happens. Then maybe we can do a similar thing with charge.

Let us start by examining electron states in both Dirac and **Weyl** representations. For this we first need a matrix transform between the two. Then we'll look at steady state & pure spin components of an electron field travelling along the $z$ axis.

**Dirac standard rep:** (diagonalizes mass term)
$$\alpha_i = \sigma_1 \otimes \sigma_i \qquad \beta = \sigma_3 \otimes I$$

**Weyl rep:** (diagonalizes $\beta$)
$$\alpha_i = -\sigma_3 \otimes \sigma_i \qquad \beta = -\sigma_1 \otimes I$$

We want a unitary map $U$ to go between these, specifically $\sigma_1 \to -\sigma_3, \;\sigma_3 \to -\sigma_1$. This is a rotation about the $y$-axis of $90°$ and then a reflection in the $y$-$z$ plane. First rotate about the $y$-axis to get $\sigma_1 \to \sigma_3, \sigma_3 \to -\sigma_1$ with
$$U_y = \frac{1}{2}\!\begin{pmatrix} 1+i & 1+i \\ -1-i & 1+i\end{pmatrix}$$
and then rotate $180°$ using $U_0 = \sigma_1 = \begin{pmatrix}0 & 1\\ 1& 0\end{pmatrix}$, namely $\sigma_3 \to -\sigma_3,\;\sigma_1 \to \sigma_1$. So
$$U_{DW} = U_0\, U_y = \frac{1}{2}\!\begin{pmatrix} 0 & 1\\ 1 & 0\end{pmatrix}\!\begin{pmatrix} 1+i & 1-i \\ -1-i & 1+i\end{pmatrix} = \frac12\!\begin{pmatrix} -1-i & 1+i \\ 1+i & 1-i\end{pmatrix}$$

---

## Page 82

In the standard representation, there are plane wave solutions of the form (positive energy)
$$\psi_+^{(\alpha)}(x) = e^{-i(k_0 x_0 - \vec k\!\cdot\!\vec x)}\, u^\alpha(k)$$
$$u^\alpha(k) = \frac{\gamma^\mu k_\mu + m I}{\sqrt{2m(m+E)}}\, u^\alpha(0)$$
$$u^1(0) = \begin{pmatrix} 1\\0\\0\\0 \end{pmatrix}\quad u^2(0) = \begin{pmatrix} 0\\1\\0\\0 \end{pmatrix}$$

and (negative energy)
$$\psi_-^{(\alpha)}(x) = e^{+i(k_0 x_0 + \vec k\!\cdot\!\vec x)}\, v^{(\alpha)}(k)$$
$$v^\alpha(k) = \frac{-\gamma^\mu k_\mu + m I}{\sqrt{2m(m+E)}}\, v^\alpha(0)$$
$$v^1(0) = \begin{pmatrix} 0\\0\\1\\0 \end{pmatrix}\quad v^2(0) = \begin{pmatrix} 0\\0\\0\\1 \end{pmatrix}$$

We want to transform these solutions to the Weyl rep. so we can better see the dynamic interdependence of spin states and angular momentum. Applying $U_{DW}$ to $\psi$ just re-casts the $\gamma$ matrices into Weyl form and acts straight on the basis vectors $u^\alpha(0)$ etc. Thus
$$U_{DW}\, u^1(0) = \tfrac12\!\begin{pmatrix} -1-i & 1+i \\ 1+i & 1-i\end{pmatrix}\!\begin{pmatrix} 1\\0\\0\\0\end{pmatrix} = \tfrac12\!\begin{pmatrix} -1-i \\ 0\\ 1+i\\ 0\end{pmatrix}$$
$$U_{DW}\, u^2(0) = \tfrac12\!\begin{pmatrix} 0\\ -1-i\\ 0\\ 1-i\end{pmatrix} \qquad U_{DW}\, v^1(0) = \tfrac12\!\begin{pmatrix} 0\\ 1+i\\ 0\\ 1-i\end{pmatrix} \qquad U_{DW}\, v^2(0) = \tfrac12\!\begin{pmatrix} 1+i\\ 0\\ 1-i\\ 0\end{pmatrix}$$

The $\gamma$ matrices are given by $\gamma^0 = \beta,\;\gamma^i = \beta \alpha_i$.

---

## Page 83

whereby in Weyl representation,
$$\alpha_i = -\sigma_3 \otimes \sigma_i \qquad \beta = -\sigma_1 \otimes I$$
so
$$\gamma_i = \beta \alpha_i = (\sigma_1 \otimes I)(\sigma_3 \otimes \sigma_i) = (\sigma_1 \sigma_3 \otimes \sigma_i) = \begin{pmatrix} 0 & 1\\ 1 & 0\end{pmatrix}\!\begin{pmatrix} 1 & 0\\ 0 & -1\end{pmatrix}\!\otimes\sigma_i = \begin{pmatrix} 0 & -1\\ 1 & 0\end{pmatrix}\!\otimes\sigma_i = -i\sigma_2 \otimes \sigma_i$$

Plane wave solution for the upper:
$$u^\alpha(k) = \frac{1}{\sqrt{2m(m+E)}}\,(\gamma^\mu k_\mu + m I)$$
$$= \frac{1}{\sqrt{2m(m+E)}}\,(\gamma^0 k_0 - \gamma^i k_i + m I)$$

and if only $k_0,\,k_3 = k_z \neq 0$, then
$$u^\alpha(k) = \frac{1}{\sqrt{2m(m+E)}}\!\left[ -\!\begin{pmatrix} 0 & 0 & k_0 & 0\\ 0 & 0 & 0 & k_0\\ k_0 & 0 & 0 & 0\\ 0 & k_0 & 0 & 0\end{pmatrix} + i\!\begin{pmatrix} 0 & 0 & -ik_3 & 0\\ 0 & 0 & 0 & ik_3\\ ik_3 & 0 & 0 & 0\\ 0 & -ik_3 & 0 & 0\end{pmatrix} + \begin{pmatrix} m & 0 & 0 & 0\\ 0 & m & 0 & 0\\ 0 & 0 & m & 0\\ 0 & 0 & 0 & m\end{pmatrix}\right]\!u^\alpha(0)$$

So
$$u_z^{(2)}(k) = \frac{1}{2\sqrt{2m(m+E)}}\,\left[\!\begin{pmatrix} 0\\ 0\\ -k_0(1+i)\\ 0\end{pmatrix} + \begin{pmatrix} 0\\ 0\\ k_3(1+i)\\ 0\end{pmatrix} + \begin{pmatrix} (-1-i)m \\ 0\\ 0\\ (1+i)m\end{pmatrix}\right]$$

$$\boxed{\;\psi_z^{(2)+} = \frac{1}{2\sqrt{2m(m+E)}}\,\begin{pmatrix}(1+i)(k_3 - k_0 - m)\\ 0\\ (1+i)(k_3 + k_0 + m)\\ 0\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;}$$

---

## Page 84

$$\psi_z^{(2)+} = \frac{1}{2\sqrt{2m(m+E)}}\!\left[-\!\begin{pmatrix} 0 & 0 & k_3 & 0\\ 0 & 0 & 0 & k_0\\ k_0 & 0 & 0 & 0\\ 0 & k_3 & 0 & 0\end{pmatrix}\!\begin{pmatrix} 0\\ -1-i\\ 0\\ 1+i\end{pmatrix} + \begin{pmatrix} 0 & 0 & k_3 & 0\\ 0 & 0 & 0 & -k_3\\ -k_3 & 0 & 0 & 0\\ 0 & k_3 & 0 & 0\end{pmatrix}\!\begin{pmatrix} 0\\ -1-i\\ 0\\ 1+i\end{pmatrix} + \begin{pmatrix} 0\\ -1-i\\ 0\\ 1+i\end{pmatrix}m\,\right]\,e^{-i(k_0 t - k_3 z)}$$

$$\boxed{\;\psi_z^{(2)+} = \frac{1+i}{2\sqrt{2m(m+E)}}\,\begin{pmatrix}0\\ -k_0 - k_3 - m\\ 0\\ +k_0 - k_3 + m\end{pmatrix}\,e^{-i(k_0 t - k_3 z)}\;}$$

$$\psi_z^{(1)-} = \frac{1}{2\sqrt{2m(m+E)}}\!\left[\!\begin{pmatrix} 0 & 0 & k_0 & 0\\ 0 & 0 & 0 & k_0\\ k_0 & 0 & 0 & 0\\ 0 & k_0 & 0 & 0\end{pmatrix} + \begin{pmatrix} 0 & 0 & -k_3 & 0\\ 0 & 0 & 0 & k_3\\ k_3 & 0 & 0 & 0\\ 0 & -k_3 & 0 & 0\end{pmatrix} + m\right]\!\begin{pmatrix} 1+i\\ 0\\ 1-i\\ 0\end{pmatrix} e^{i(k_0 t + k_3 z)}$$

$$\boxed{\;\psi_z^{(1)-} = \frac{1}{2\sqrt{2m(m+E)}}\!\begin{pmatrix} (1-i)(k_0 - k_3) + (1+i)m\\ 0\\ (1+i)(k_0 + k_3) + (1-i)m\\ 0\end{pmatrix}\,e^{i(k_0 t + k_3 z)}\;}$$

$$\psi_z^{(2)-} = \frac{1}{2\sqrt{2m(m+E)}}\!\left[\!\begin{pmatrix} m & 0 & k_0 - k_3 & 0\\ 0 & m & 0 & k_3 + k_0\\ k_0 + k_3 & 0 & m & 0\\ 0 & k_0 - k_3 & 0 & m\end{pmatrix}\!\begin{pmatrix} 0\\ 1+i\\ 0\\ 1-i\end{pmatrix}\right]\,e^{i(k_0 t + k_3 z)}$$

$$\boxed{\;\psi_z^{2-} = \frac{1}{2\sqrt{2m(m+E)}}\!\begin{pmatrix} 0\\ (1-i)(k_0 + k_3) + (1+i)m\\ 0\\ (1+i)(k_0 - k_3) + (1-i)m\end{pmatrix}\,e^{i(k_0 t + k_3 z)}\;}$$

In the $m \to 0$ limit,
$$\psi_z^{(2)+} \sim \frac{1}{\sqrt{8 k_3}}\,(1-i)\,2 k_3 \begin{pmatrix} 0\\ 0\\ 0\\ 1\end{pmatrix}\, e^{i k_3(t+z)}$$
$$\psi_z^{2-} \sim \frac{1}{\sqrt{2 k_3}}(1+i) k_3 \begin{pmatrix} 0\\ 1\\ 0\\ 0\end{pmatrix} e^{i k_3 (t+z)}$$
$$\psi_z^{(1)-} \sim \frac{-(1+i)}{\sqrt{2 k_3}}\!\begin{pmatrix} 0\\ k_3\\ 0\\ 0\end{pmatrix} e^{i k_3(t+z)}$$

Note that there seems to be a degeneracy here, in that we don't get any $\begin{pmatrix} 1\\0\\0\\0\end{pmatrix}$ or $\begin{pmatrix} 0\\0\\1\\0\end{pmatrix}$ states as the limit of $m \to 0$. Why not? Are we going to a negative energy state in which $k_0 = -k_3$?

---

## Page 85

Let's try another way to solve these. Write Weyl out like this:
$$i\hbar\,\frac{\partial \psi_+}{\partial t} = -i\hbar c\,\vec\sigma\!\cdot\!\nabla\psi_+ - m_0 c^2 \psi_- \tag{4a}$$
$$i\hbar\,\frac{\partial \psi_-}{\partial t} = i\hbar c\,\vec\sigma\!\cdot\!\nabla\psi_- - m_0 c^2 \psi_+ \tag{4b}$$
where $\psi_+$ and $\psi_-$ are both 2-component spinors. To factor out space–time dependences, we have to write
$$\psi_+ \sim A_+ e^{i(k_0 c t - \vec k\!\cdot\!\vec x)} \;(1) \qquad\text{or}\qquad \psi_+ \sim B_+ e^{i(k_0 c t + \vec k\!\cdot\!\vec x)}\;(2)$$
and take the derivatives. Let's start with (1).
$$i\hbar\,\tfrac{\partial}{\partial t}\!\big(A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}\big) = -\hbar c k_0 A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}$$
$$i\hbar c\,\vec\sigma\!\cdot\!\nabla\!\big(A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}\big) = i\hbar c\, \vec\sigma\!\cdot\!\big(A_\pm (-i\vec k) e^{i(k_0 c t - \vec k\!\cdot\!\vec x)}\big) = \hbar c\, (\vec\sigma\!\cdot\!\vec k) A_\pm e^{i(k_0 c t - \vec k\!\cdot\!\vec x)} \tag{3a/3b}$$

whereby (4a/b) becomes
$$-\hbar c k_0 A_+ = -\hbar c\,(\vec\sigma\!\cdot\!\vec k) A_+ - m_0 c^2 A_- \tag{3a}$$
$$-\hbar c k_0 A_- = \hbar c\,(\vec\sigma\!\cdot\!\vec k) A_- - m_0 c^2 A_+ \tag{3b}$$

Now, we want solutions such that as $m_0 \to 0$, only one component of the four is non-zero. Is this possible? In the massless case, 3a & 3b are completely independent, so $A_+$ or $A_-$ can be non-zero without affecting the other. We treat $m_0$ as an interaction & a perturbation. Now, 3a takes the form
$$k_0 I A_+ = (\vec\sigma\!\cdot\!\vec k) A_+$$
If $\vec k = k_3 \hat z$ then
$$\begin{pmatrix} k_0 & 0\\ 0 & k_0\end{pmatrix} A_+ = \begin{pmatrix} k_3 & 0\\ 0 & -k_3\end{pmatrix} A_+$$
If $A_+^{(1)} = \binom{1}{0}$ then $k_0 = k_3$ and if $A_+^{(2)} = \binom{0}{1}$ then $k_0 = -k_3$. Simply put, $A_+^{(1)}$ is the positive energy solution and $A_+^{(2)}$ is the negative ⟶

---

## Page 86

⟶ energy solution. Doing the same with $A_-$, we get
$$\begin{pmatrix} k_0 & 0\\ 0 & k_0\end{pmatrix} A_- = \begin{pmatrix} -k_3 & 0\\ 0 & k_3\end{pmatrix} A_-$$
so $A_-^{(1)} = \binom{1}{0}$ is the negative energy solution and $A_-^{(2)} = \binom{0}{1}$ is the positive energy solution. This also encompasses the $B$-solutions (2) above. The standard normalization of these solutions is $\dfrac{1}{(2\pi)^3 \sqrt{2E}}$. (Greiner 14.5)

The upper component of $A^+$ is understood as a right handed (spin in the direction of motion) particle. The lower component is understood as a left handed antiparticle. This is clear because $\vec\sigma\!\cdot\!\vec p$ is pure helicity for a massless particle & these are its eigenstates. In the same way, the upper component of $A^-$ is a right-handed antiparticle and the lower component is a left-handed particle. *(margin: "helicity, really, for a plane wave")*

Now, the mass term **conserves spin**. It mixes a right-handed particle with a right-handed antiparticle and a left-handed antiparticle with a left-handed particle.

To derive solutions that reduce to the above in the massless case, write $A_+^{(1)} = \binom{1}{\alpha}$, $A_-^{(1+)} = \binom{\beta}{\gamma}$ and plug these into the equations (3):
$$-\hbar c k_0 \binom{1}{\alpha} = -\hbar c \sigma_3 k_3 \binom{1}{\alpha} - m_0 c^2 \binom{\beta}{\gamma}$$
$$-\hbar c k_0 \binom{\beta}{\gamma} = \hbar c \sigma_3 k_3 \binom{\beta}{\gamma} - m_0 c^2 \binom{1}{\alpha}$$

This gives us 4 equations,
$$\delta k_0 = \delta k_3 + \frac{m_0 c}{\hbar}\,\beta \tag{4a}$$
$$k_0 \alpha = -k_3 \alpha + \frac{m_0 c}{\hbar}\,\gamma \tag{4b}$$

---

## Page 87

$$-k_0 \beta = k_3 \beta - \frac{m_0 c}{\hbar} \tag{4c}$$
$$-k_0 \gamma = -k_3 \gamma - \frac{m_0 c}{\hbar}\,\alpha \tag{4d}$$

4b and 4d are completely independent of 4a & 4c so solve 4a & 4c. Writing $\lambda_0 = \dfrac{m_0 c}{\hbar}$ and $\delta = 1$,
$$k_0 = k_3 + \lambda_0 \beta \tag{4a}$$
$$k_0 \beta = -k_3 \beta + \lambda_0 \;\Rightarrow\; \beta = \frac{\lambda_0}{k_0 + k_3} \tag{4c}$$

Substituting into 4a,
$$k_3 - k_0 = -\frac{\lambda_0^2}{k_0 + k_3}$$
$$k_3^2 - k_0^2 = -\lambda_0^2 = -\frac{m_0^2 c^2}{\hbar^2}$$
$$p_z^2 - E_z^2 = -m_0^2 c^2 \quad\text{(off by a sign, but pretty close)}$$

To normalize, we'd like to write $A_+^{(1)} = \binom{a}{0}$, $A_-^{(1+)} = \binom{b}{0}$ where $a^2 + b^2 = 1$.
$$\eta \equiv 1 + \frac{\lambda_0^2}{(k_0 + k_3)^2} \qquad a = \frac{1}{\eta^{1/2}}\qquad b = \frac{\beta}{\eta^{1/2}}$$
$$1/\eta = \frac{(k_0 + k_3)^2}{(k_0 + k_3)^2 + \lambda_0^2}\qquad 1/\eta^{1/2} = \frac{k_0 + k_3}{\sqrt{(k_0 + k_3)^2 + \lambda_0^2}}$$
$$\beta/\eta = \frac{\lambda_0 (k_0 + k_3)}{(k_0 + k_3)^2 + \lambda_0^2}\qquad \beta/\eta^{1/2} = \frac{\lambda_0}{\sqrt{(k_0 + k_3)^2 + \lambda_0^2}}$$

and
$$\boxed{\;\Psi_{RP} = \binom{\psi_+}{\psi_-} = \frac{1}{(2\pi)^3 \sqrt{2E}}\!\begin{pmatrix} k_0 + k_3\\ 0\\ \lambda_0\\ 0\end{pmatrix} \big((k_0 + k_3)^2 + \lambda_0^2\big)^{-1/2}\, e^{i(k_0 t - k_3 z)}\;} \tag{6A}$$
**Right-handed particle:** $k_0 > 0$, $\lambda_0 = \dfrac{m_0 c}{\hbar}$.

As $\lambda_0 \to 0$ this reduces to the proper values for a pure right particle.

If we set $\beta = 1$ then
$$\delta k_0 = \delta k_3 + \lambda_0 \;\Rightarrow\; \delta = \frac{\lambda_0}{k_0 - k_3} \tag{5a}$$
$$-k_0 = k_3 - \lambda_0 \delta \;\Rightarrow\; \delta = \frac{k_0}{\lambda_0}\!\cdot\!\frac{1}{k_0 + k_3} \tag{5b}$$
$$k_0 + k_3 = \lambda_0^2 / (k_0 - k_3)$$

---

## Page 88

$$\boxed{\;\Psi_{LA} = \frac{1}{(2\pi)^3 \sqrt{2E}}\big((k_0 - k_3)^2 + \lambda_0^2\big)^{-1/2}\!\begin{pmatrix} \lambda_0\\ 0\\ k_0 - k_3\\ 0\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;} \tag{6B}$$
**The Left-Handed Antiparticle**, ($k_0 < 0$)!

Using 4b & 4d with $\alpha = 1$, we get
$$k_0 = -k_3 + \lambda_0 \gamma$$
$$k_0 \gamma = k_3 \gamma + \lambda_0 \;\Rightarrow\; \gamma = \frac{\lambda_0}{k_0 - k_3}$$
$$1/\eta^{1/2} = \frac{(k_0 - k_3)}{\sqrt{(k_0 - k_3)^2 + \lambda_0^2}}$$

$$\boxed{\;\Psi_{RA} = \frac{1}{(2\pi)^3 \sqrt{2E}}\,\big((k_0 - k_3)^2 + \lambda_0^2\big)^{-1/2}\!\begin{pmatrix} 0\\ k_0 - k_3\\ 0\\ \lambda_0\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;} \tag{6C}$$
**The Right-handed Antiparticle**, ($k_0 < 0$)!

Finally, setting $\gamma = 1$,
$$k_0 \alpha = -k_3 \alpha + \lambda_0 \;\Rightarrow\; \alpha = \frac{\lambda_0}{k_0 + k_3}$$
$$k_0 = k_3 + \lambda_0 \alpha$$

$$\boxed{\;\Psi_{LP} = \frac{1}{(2\pi)^3 \sqrt{2E}}\,\big((k_0 + k_3)^2 + \lambda_0^2\big)^{-1/2}\!\begin{pmatrix} 0\\ \lambda_0\\ 0\\ k_0 + k_3\end{pmatrix}\, e^{-i(k_0 t - k_3 z)}\;} \tag{6D}$$
**The Left-Handed Particle** ($k_0 > 0$).

---

## Page 89

Now, note that the mass term mixes particle–antiparticle for either handedness, but does **not** mix handedness — i.e. it conserves helicity/spin. The introduction of the photon gets the spin though, and the photon carries spin $\pm 1$ in itself. (Never spin 0.) If we think of the photon as 2 separate particles, one w/ spin $+1$ and one w/ spin $-1$ then it is somewhat like the $W_\pm$ bosons. They carry charge instead of spin though, and flip spin states instead of charge states, whereas the $W$ flips charge states but not spin states … thus its "handedness."

In Weyl, $\gamma_5 = i\gamma_0 \gamma_1 \gamma_2 \gamma_3 = \begin{pmatrix} I & 0\\ 0 & -I\end{pmatrix}$ and the weak interaction couples via $1 - \gamma_5$ — that is, to the left-handed particle and right-handed antiparticle. This we take to be analogous to E–M coupling to $e$ and not $\nu_e$. Take the analogy 1 step further: If $e$ has "mass", or a mixing between $e_L^+ \leftrightarrow e_R^+$, $e_L^- \leftrightarrow e_R^-$ as a result of $A_\mu$, couldn't there be something like a "mass" as a result of $W$? Could the $Z$ be the result of that?

We should be able to draw the analogy clearly. The E&M ⟶ (margin) ⟶ interactions here are the "new idea." They don't conserve charge any more than the mass term in e&m. The mass term conserves magnetic moment.

*(Table sketched in the left margin — electromagnetic block:)*

| mass | particle | charge | spin | comment |
|---|---|---|---|---|
| m | $e_R^-$ | $-q$ | $+1$ | $A$ is to $S$ what $W$ is to $Q$ |
| m | $e_L^+$ | $+q$ | $-1$ | $A$ is to $Q$ what $W$ is to $S$ |
| m | $e_R^+$ | $+q$ | $-1$ | $\mu$ violates $q$ |
| m | $e_L^-$ | $-q$ | $+1$ | $n$ violates $q_3, g$ |
| 0 | $\nu_R$ | 0 | $+1$ | So if $A$ couple to $Q$, $W$ couples to $S$.  |
| 0 | $\bar\nu_L$ | 0 | $-1$ | Since 2-component spinor flips, not a scalar like $g$ |
| 0 | $\bar\nu_R$ | 0 | $-1$ | Could $W$ be a scalar field?  |
| 0 | $\nu_L$ | 0 | $+1$ | |

Bottom: separate **Weak** block — same particles, but now charges $\pm g$ and the curly braces label $P_C$ violation pairs. $\mu$ acts like $W$? Author labels the chains $)P_{C_Z}$ and $)P_{C_W}, P_{C_V}$.

---

## Page 90

*(Top of page — three Feynman diagrams of the weak/EM vertices:)*

- $\nu_L \to \bar\nu_R \to e_L^-,\;\bar\nu_e \to e_L^+$ via a $Z$ exchange (neutral current).
- $\bar\nu_R \to e_L^-$ and $\nu_L \to e_L^-$ via a $W^-$ exchange (charged current).
- $\bar\nu_{eR} \to e_L^-,\; \nu_{eR} \to e_L^-$ via $W^-$ (another configuration).

**Could $Z$ be viewed as a bound state of $W^+ W^-$?**

*(box diagram: $\nu_e$ and $e^-$ on one side, $\nu_e$ and $e^-$ on the other; two $W^+$ exchanges plus two intermediate $\nu_e$ propagators forming a closed box.)*

"One would certainly think so. Energies just don't work out."

---

### **Electromagnetic** *(tabulation continued)*

| $m$ | $\binom{e_R^-}{e_L^+}$ | $-q$ | $+1$ | |
| $m$ | $\binom{e_R^+}{e_L^-}$ | $+g$ | $-1$ | $A$ is to $S$ what $W$ is to $Q$ |
| $m$ |  | $-g$ | $+1$ | $A$ is to $Q$ what $W$ is to $S$ |
| $m$ |  | $+g$ | $-1$ | $\mu$ violates $q$ |
| $m$ |  | $-g$ | $+1$ | $n$ violates $q_3, g$ |
| 0 | $\nu_R$ | 0 | $+1$ | So if $A$ couples to $Q$, $W$ couples to $S$. |
| 0 | $\bar\nu_L$ | 0 | $-1$ | Since 2-component spinor flips, not a scalar like $g$. |
| 0 | $\bar\nu_R$ | 0 | $-1$ | Could $W$ be a scalar field?  |
| 0 | $\nu_L$ | 0 | $+1$ | |

### **Weak** *(separate block)*

|  | particle | $Q$ | spin |  |
|---|---|---|---|---|
| 0 | $e_R^-$ | 0 | $+1$ | |
| 0 | $e_L^+$ |  | $-1$ | |
| $\mu$ | $e_R^+$ | $+g$ | $-1$ | $\big\}P_{C_Z}\;\mu$ violates $q, g, \beta$ |
| $\mu$ | $e_L^-$ | $-g$ | $+1$ |  |
| 0 | $\nu_R$ | 0 | $+1$ | $\big\}P_{C_W}$  $\mu$ ↔ $W$ the same?  |
| 0 | $\bar\nu_L$ | 0 | $-1$ |  |
| $\bar\mu$ | $\bar\nu_R$ | $+g$ | $-1$ | $\big\}P_{C_V}$ |
| $\mu$ | $\nu_L$ | $-g$ | $+1$ |  |

*(margin: "$\mu \alpha W$ the same?")*

---

## Page 91 — Dirac Mass Term and Charge Conservation

The ordinary mass term in the Dirac equation does not really conserve charge, if viewed in terms of perturbation theory. Only by solving exactly do we get a balance between the two charge states with the result of charge conservation. In diagrammatic terms, though, we have something like

$$e_R \quad e_R^+ \quad e_R \quad e_R^+ \quad e_R \quad e_R^+$$

where the switching decreases at higher energies.

**Can we say that W actually couples to spin?** Apparently, yes. **In what sense is it a vector particle??**

---

## Pages 92–97 — Electromagnetic and Weak Interactions

*(Motivational paper introduction)*

This paper will explore the similarities between the electromagnetic and weak interactions, and their respective charge spectra. It is intended as a motivational paper that will provide guidance for future, more detailed research.

There are some important likenesses between the electromagnetic and weak interactions which may provide important clues to a deeper understanding of these interactions. Although the Weinberg–Salam theory of electro-weak interactions has had some success in making predictions, it leaves some important questions unanswered, that we might expect a proper theory to answer. For example, W-S posits a symmetry that is then broken to give the W and Z mass. The Higgs boson supposed to be associated to this theory has not been found. Where is it? Or is the supposed symmetry merely an artificial construct to hide the abnormalities of a renormalization scheme? After all, what is the difference between a broken symmetry with no Higgs and a symmetry that never existed in the first place?

Another important problem with W-S is that it uses non-specific techniques that could be formulated in a variety of ways. This fact lays aside a whole class of questions that are simply never asked. They are rooted in the choice of $U(1) \times SU(2)$ as a gauge field. The question is, why did God/Nature choose $U(1) \times SU(2)$, and not something else, like $U(1) \times SO(6,2)$? Our supposition is that there is something important to be learned, probably about the structure of spacetime, in the particulars of $U(1) \times SU(2)$.

By looking at the symmetries of these interactions, we both raise the questions that need to be raised and frame those questions in a way that will hopefully point to an answer, without unwittingly introducing unspoken assumptions.

First, let us consider the leptonic doublets of the electro-weak interaction,

$$\begin{pmatrix} e \\ \nu_e \end{pmatrix} \quad \begin{pmatrix} \mu \\ \nu_\mu \end{pmatrix} \quad \begin{pmatrix} \tau \\ \nu_\tau \end{pmatrix}$$

and potentially others, undiscovered as yet. Let us write these out in detail using the Weyl representations:

$$\begin{pmatrix} e \\ \nu_e \end{pmatrix} = \begin{pmatrix} e_R^- \\ e_L^+ \\ e_R^+ \\ e_L^- \\ \nu_R \\ \bar{\nu}_L \\ \bar{\nu}_R \\ \nu_L \end{pmatrix}$$

Note that we have included $\nu_R$ and $\bar{\nu}_L$, which most treatments of W-S omit, and claim to be non-existent. That claim is based on the assertion that neutrino masses are exactly zero. Experimentally, this claim is open to question.

Certainly the fact that they interact at all suggests that they ought to gain some renormalization mass from the interaction. Leaving it out also clouds the symmetry between electromagnetic and weak interactions. (W-S does this for simplicity, so one can deal with only one singlet and one doublet for each leptonic pair. That way the singlet covariant derivative need only deal with the charged electron, and it needn't have two forms.)

In this representation, we may see that both electromagnetic and weak interactions have four charged states and four neutral states that do not interact:

| State | EM | W |
|---|---|---|
| $e_R^-$ | EM | — |
| $e_L^+$ | EM | — |
| $e_R^+$ | EM | W |
| $e_L^-$ | EM | W |
| $\nu_R$ | — | — |
| $\bar{\nu}_L$ | — | — |
| $\bar{\nu}_R$ | — | W |
| $\nu_L$ | — | W |

These include two states that interact both weakly and electromagnetically, two that interact only electromagnetically, two that interact only weakly, and two that do not interact at all. This is a very symmetric representation of these forces.

It is interesting to note that these neutral states correspond to a "missing" charge state. The right-handed weak interaction does not exist, and neither does the magnetic monopole. By this line of reasoning the neutrino would be the magnetic monopole that doesn't exist. Both a right-handed weak interaction and a magnetic monopole would require the introduction of new sets of fields, a $(W_R^\pm, Z')$ for right-handed weak and an $A'$ for monopoles. We should also mention that with symmetry breaking and Higgs, we may not be able to rule these out completely — perhaps we can only set lower limits on the mass of thin IVBs, as the interaction becomes weaker as the mass goes up.

Again, we must ask: why is there no right-handed weak interaction? Why is there no magnetic monopole? This is something a fundamental theory should answer.

The similarity between electromagnetic and weak interactions might also be examined at the level of the IVB. The photon is massless and carries no charge, only angular momentum, coupling charged particles. The weak interaction carries charge, but no angular momentum (coupling only to left-handed particles). It is essential that the weak IVB be massive in order to avoid coupling to right-handed particles too *(it has a longitudinal mode, not just transverse, and can flip chirality)*. And it is essential that the photon be chargeless to avoid developing a mass from self-energy. In other words, electromagnetism is to charge as the weak interaction is to left-handedness.

The strong interaction appears to be a quantum effect, in ways similar to the Heisenberg Uncertainty Principle, in ways similar to spin and angular momentum.

The fact that quarks cannot be observed alone in nature seems to correspond in a way to spin and orbital angular momentum — that orbital angular momentum occurs in quantum steps of $0, 1, 2, 3$ etc. whereas spin takes values of $\frac{1}{2}, \frac{3}{2}$, etc. too. These spin values cannot exist as independent orbital angular momentum values, but they can be attached to the mathematics of particles as an intrinsic property. In the same way, perhaps electric charge has a deeper principle or something such that only charge-1 particles can be seen on a macroscopic level, but there are intrinsic charges $\frac{1}{3}e$ that do exist under a Heisenberg-like arrangement that cannot be seen macroscopically, due to some fundamental principle.

---

## Pages 98–101 — Rotation Matrices, Tensor Products, 3D Dirac

### Tensor Products of Rotation Matrices

$$R_z \otimes R_z = \begin{pmatrix} e^{i\theta/2} & 0 \\ 0 & e^{-i\theta/2} \end{pmatrix} \otimes \begin{pmatrix} e^{i\theta/2} & 0 \\ 0 & e^{-i\theta/2} \end{pmatrix} = \begin{pmatrix} e^{i\theta} & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & e^{-i\theta} \end{pmatrix}$$

$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \qquad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$$

$$R_x(\phi) = \exp(i\sigma_x \phi/2) = \begin{pmatrix} i\sin\phi/2 & \cos\phi/2 \\ \cos\phi/2 & i\sin\phi/2 \end{pmatrix}$$

$$R_x = R_x \otimes R_x = \begin{pmatrix} i\sin\phi/2 & \cos\phi/2 \\ \cos\phi/2 & i\sin\phi/2 \end{pmatrix} \otimes \begin{pmatrix} i\sin\phi/2 & \cos\phi/2 \\ \cos\phi/2 & i\sin\phi/2 \end{pmatrix}$$

$$= \begin{pmatrix} -\sin^2\phi/2 & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & i\cos\frac{\phi}{2}\sin\frac{\phi}{2} & \cos^2\frac{\phi}{2} \\ i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & -\sin^2\frac{\phi}{2} & \cos^2\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} \\ i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & \cos^2\frac{\phi}{2} & -\sin^2\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} \\ \cos^2\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & i\sin\frac{\phi}{2}\cos\frac{\phi}{2} & -\sin^2\frac{\phi}{2} \end{pmatrix}$$

$$R_y(\phi) = \exp(i\sigma_y \phi/2) = \begin{pmatrix} \sin\phi/2 & \cos\phi/2 \\ -\cos\phi/2 & -\sin\phi/2 \end{pmatrix}$$

$$R_y = R_y \otimes R_y = \begin{pmatrix} \sin^2\phi/2 & -\sin\frac{\phi}{2}\cos\frac{\phi}{2} & -\sin\frac{\phi}{2}\cos\frac{\phi}{2} & \cos^2\frac{\phi}{2} \\ \cos^2\frac{\phi}{2}\sin\frac{\phi}{2} & \sin^2\frac{\phi}{2} & -\cos^2\frac{\phi}{2} & -\cos^2\frac{\phi}{2}\sin\frac{\phi}{2} \\ \cos\frac{\phi}{2}\sin\frac{\phi}{2} & -\cos^2\frac{\phi}{2} & \sin^2\frac{\phi}{2} & -\cos\frac{\phi}{2}^2\sin\frac{\phi}{2} \\ \cos^2\frac{\phi}{2} & \cos\frac{\phi}{2}^2\sin\frac{\phi}{2} & \sin^2\frac{\phi}{2}\cos\frac{\phi}{2} & \sin^2\frac{\phi}{2} \end{pmatrix}$$

Using $\sin 2\theta = 2\sin\theta\cos\theta$ and $\cos 2\theta = \cos^2\theta - \sin^2\theta$:

$$R_x = \begin{pmatrix} -\sin^2\phi/2 & 2i\sin\phi & 2i\sin\phi & \cos^2\phi/2 \\ 2i\sin\phi & -\sin^2\phi/2 & \cos^2\phi/2 & 2i\sin\phi \\ 2i\sin\phi & \cos^2\phi/2 & -\sin^2\phi/2 & 2i\sin\phi \\ \cos^2\phi/2 & 2i\sin\phi & 2i\sin\phi & -\sin^2\phi/2 \end{pmatrix}$$

We want to transform this to get rid of all $\phi/2$, presumably making $\cos^2\frac{\phi}{2} - \sin^2\frac{\phi}{2}$ into $\cos\frac{\phi}{2} + \sin^2\frac{\phi}{2}$ out of it.

### Spin-1 Matrices

$$S_x = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad S_y = \begin{pmatrix} 0 & 0 & i \\ 0 & 0 & 0 \\ -i & 0 & 0 \end{pmatrix}, \quad S_z = \begin{pmatrix} 0 & -i & 0 \\ i & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$$

$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

$$\sigma_x \otimes \sigma_x = \begin{pmatrix} 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{pmatrix}, \quad \sigma_y \otimes \sigma_y = \begin{pmatrix} 0 & 0 & 0 & -1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \end{pmatrix}, \quad \sigma_z \otimes \sigma_z = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

We want a basis transformation to turn $\sigma_z \otimes \sigma_z$ etc. into $\begin{pmatrix} 0 & \cdot \\ \cdot & S_x \end{pmatrix}$.

Let $A = \begin{pmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & \cdots \end{pmatrix}$, then $A(\sigma_z \otimes \sigma_z)A^\dagger$ is computed.

Need a rep where $S_z$ is diagonal. The required transformation for the Z direction:

$$\begin{pmatrix} 1/\sqrt{2} & 0 & 1/\sqrt{2} \\ 0 & 1 & 0 \\ 1/\sqrt{2} & 0 & -1/\sqrt{2} \end{pmatrix}$$

In the new basis:

$$S_x = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}, \quad S_y = \begin{pmatrix} 0 & -i & 0 \\ i & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad S_z = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & -1 \end{pmatrix}$$

### 3D Dirac Equation

A 3D Dirac equation:

$$\frac{\partial \psi_+}{\partial t} = -c\, \mathbf{S} \cdot \nabla\, \psi_+$$

$$\frac{\partial \psi_-}{\partial t} = c\, \mathbf{S} \cdot \nabla\, \psi_-$$

Breaking these out:

$$\begin{pmatrix} \partial_0 \psi_+^1 \\ \partial_0 \psi_+^2 \\ \partial_0 \psi_+^3 \end{pmatrix} = -c \begin{pmatrix} \partial_3 & \partial_1 - i\partial_2 & 0 \\ \partial_1 + i\partial_2 & 0 & \partial_1 - i\partial_2 \\ 0 & \partial_1 + i\partial_2 & -\partial_3 \end{pmatrix} \begin{pmatrix} \psi_+^1 \\ \psi_+^2 \\ \psi_+^3 \end{pmatrix}$$

$$= -c \begin{pmatrix} \partial_3\psi_+^1 + \partial_1\psi_+^2 - i\partial_2\psi_+^2 \\ \partial_1\psi_+^1 + i\partial_2\psi_+^1 + \partial_1\psi_+^3 - i\partial_2\psi_+^3 \\ \partial_1\psi_+^2 + i\partial_2\psi_+^2 - \partial_3\psi_+^3 \end{pmatrix}$$

If $\psi_+ = E + iB$ [note for further investigation]

---

## Pages 103–104 — Neutral Charge and Weinberg Angle

### Neutral Charge Operator

$$Q' = t_3 \cot\theta_W - t_0 \tan\theta_W$$

Experimental values:
$$\sin^2\theta_W = 0.232 \pm 0.009, \quad \cos^2\theta_W = 0.768$$
$$\sin\theta_W = 0.481, \quad \cos\theta_W = 0.876$$
$$\cot\theta_W = 1.821, \quad \tan\theta_W = 0.549$$

$$Q' = \begin{pmatrix} 1.821 + 0.549 & 0 \\ 0 & -1.821 + 0.549 \end{pmatrix} = \begin{pmatrix} 2.37 & 0 \\ 0 & -1.27 \end{pmatrix}$$

### Hypothetical $\sin\theta_W = \frac{1}{2}$

What if $\sin\theta_W = \frac{1}{2}$? Then $\cos\theta_W = \frac{\sqrt{3}}{2}$, $\cot\theta_W = \sqrt{3}$, $\tan\theta_W = \frac{1}{\sqrt{3}}$.

*(After all, renormalization could throw it off a little.)*

For W coupling: $e = g\sin\theta_W$, so $g$ couples $W_1$, $W_2$.

$$\tau_\pm = \frac{1}{\sqrt{2}}(\tau_1 \pm i\tau_2) = \begin{pmatrix} 0 & \sqrt{2} \\ 0 & 0 \end{pmatrix}, \quad \begin{pmatrix} 0 & 0 \\ \sqrt{2} & 0 \end{pmatrix}$$

$$V_\pm = \frac{1}{\sqrt{2}}(W_1 \pm iW_2)$$

$$W_+\tau_+ + W_-\tau_- = \frac{1}{\sqrt{2}}W_1\tau_1 + \frac{1}{\sqrt{2}}W_2\tau_2$$

$$|W_+|^2 + |W_-|^2 = |W_1|^2 + |W_2|^2$$

$$gW_1\tau_1 + gW_2\tau_2 = g(W_-\tau_+ + W_+\tau_-)$$

So coupling $\sim \sqrt{2}g \sim \frac{\sqrt{2}}{\sin\theta_W} e$

### Hypothetical $\text{Coupling to } W^\pm = 3e$

What if coupling to $W^\pm = 3e$ exactly? Then $\frac{\sqrt{2}}{\sin\theta_W} = 3 \Rightarrow \sin\theta_W = \frac{\sqrt{2}}{3}$

$$\sin^2\theta_W = \frac{2}{9} = 0.222\overline{2} = \frac{2}{9}$$

Is there any significance to this?

$$\sin\theta_W = \frac{\sqrt{2}}{3}, \qquad \tan\theta_W = \sqrt{\frac{1}{7}} \approx 0.535, \qquad \cot\theta_W = \sqrt{\frac{7}{2}} \approx 1.871$$

$$Q_z = \begin{pmatrix} \cot\theta_W + \tan\theta_W & 0 \\ 0 & \cot\theta_W - \tan\theta_W \end{pmatrix} = \begin{pmatrix} 2\sqrt{7}/3 & 0 \\ 0 & 1/\sqrt{3} \end{pmatrix} \approx \begin{pmatrix} 2.37 & 0 \\ 0 & 1.33 \end{pmatrix}$$

Other algebra: $\cot\theta + \tan\theta = 7/3$, $\cot\theta - \tan\theta = 4/3$,
$2\cot\theta = 11/3$, $\cot\theta = 11/6$,
$x + 1/x = 7/3$, $x - 1/x = 4/3$, $2x = 11/3$, $x = 11/6$,
$\frac{11}{6} + \frac{6}{11} = \frac{121+36}{66} = \frac{157}{66} = 2\frac{25}{66}$ ✗

Working out $Q'\sin^2\theta$:
$$t_3\left(\frac{\cos\theta}{\sin\theta} - t_0\frac{\sin\theta}{\cos\theta}\right)\sin^2\theta = t_3\frac{\sin^{2\theta}}{\cos\theta}\cdot\cos\theta - t_0\frac{\sin^{2\theta}}{\cos\theta}\cos\theta$$
$$= t_3 2\cos^2\theta - t_0 2\sin^2\theta$$

---

## Page 105 — Electromagnetic Self-Energy Calculation

### Electromagnetic Field Energy

$$\mathcal{E}_e = \int_{r_0}^\infty |E|^2 \, dV = \int_{r_0}^\infty \frac{e^2}{r^4} 4\pi r^2 \, dr = 4\pi e^2 \int_{r_0}^\infty \frac{dr}{r^2}$$
$$= 4\pi e^2 / r_0 \quad \text{(adding factors of } 8\pi\text{)} \quad \Rightarrow \mathcal{E} = \frac{e^2}{2r_0}$$

### Yukawa Field Energy

For a Yukawa field, $V = \frac{e}{r^2}e^{-\alpha r}$:

$$\mathcal{E}_W = \int_{r_0}^\infty |W|^2 \, dV = \int_{r_0}^\infty \frac{e^2}{r^4} e^{-2\alpha r} 4\pi r^2 \, dr = 4\pi e^2 \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r^2} \, dr$$

$$= 4\pi e^2 \left[ -\frac{e^{-2\alpha r}}{r}\Big|_{r_0}^\infty - 2\alpha \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r} \, dr \right]$$

$$= 4\pi e^2 \left[ \frac{e^{-2\alpha r_0}}{r_0} - \left\{ \log(2\alpha r_0) + \sum_{n=1}^\infty \frac{(-2\alpha)^n r^n}{n \cdot n!} \right\}_{r_0}^\infty \right]$$

$$= 4\pi e^2 \left[ \frac{e^{-2\alpha r_0}}{r_0} + \log(2\alpha r_0) + \sum_{n=1}^\infty \frac{(-2\alpha)^n r^n}{n \cdot n!}\Big|_{r_0}^\infty \right]$$

This is quite ugly, and should probably be done numerically.

### Ratio of Energies

$$\frac{\mathcal{E}_W}{\mathcal{E}_e} = \frac{g^2}{e^2} \left\{ \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r^2} \, dr \Bigg/ \int_{r_0}^\infty \frac{1}{r^2} \, dr \right\} = \frac{g^2}{e^2 r_0} \int_{r_0}^\infty \frac{e^{-2\alpha r}}{r^2} \, dr$$

Numerical results for $I(n) = \int$ with $\alpha \sim k = \frac{2\pi}{\lambda_c}$, $\lambda_c = \frac{\hbar}{m_e c}$:

| $n$ | $I(n)$ | Note |
|---|---|---|
| 1 | 0.1493 | $m_e = 511\text{ keV}$ |
| 2 | 0.01885 | $m_\nu = 5\text{ eV}$ |
| 3 | 0.00356 | $\to 10^{-5}$ |
| 5 | 0.000 (truncated) | |
| 7 | $1.48 \times 10^{-5}$ | |

$$M_W = 80\text{ GeV} = 1.43 \times 10^{-25}\text{ kg}$$
$$h = 6.626 \times 10^{-34}\text{ J·s}$$
$$k = \frac{\hbar c}{m_e c^2} = 1.39, \qquad \alpha \sim 4 \times 10^{17}, \qquad \alpha r_0 = 400$$

---

## Page 106 — Newton's Method / Classical Electron Radius

### Linear Interpolation

$$f(x) = \left(\frac{f(x_1) - f(x_2)}{x_1 - x_2}\right)^{(x - x_0)} + f(x_2)$$

$$f(x) = f(x_2) + \partial f\,(x - x_2)$$

$$\frac{f(x) - f(x_0)}{\partial f} + x_2 = x, \qquad f'(x_0) = \frac{f(x) - f(x_0)}{x - x_0}$$

$$f(x) = f(x_0) + f'(x_0)\,\Delta x, \qquad \frac{1}{f'(x_0)} = \frac{x - x_0}{f(x) - f(x_0)}$$

$$x_0 + (f(x) - f(x_0)) \cdot \frac{1}{f'(x_0)} \approx x$$

### Classical Electron Radius

Setting $\mathcal{E} = \frac{e^2}{2r_0} = m_e c^2 = 9.11 \times 10^{-28} \times 9 \times 10^{20}\text{ cm}^2\text{/s}^2$:

$$\frac{(1.602 \times 10^{-19})^2 (3 \times 10^9)^2}{2r_0} = \frac{2.9 \times 10^{-38} \cdot 9 \times 10^{20}}{(1.602 \times 10^{-19} \cdot 3 \times 10^9)^2}$$

$$r_0 = \frac{e^2}{2mc^2} \approx 1.43 \times 10^{-15}\text{ m}$$

---

## Page 107 — Ellipse Foci

Given an ellipse of the form:

$$\frac{x^2}{b^2} + \frac{y^2}{b^2} = 1$$

it should have foci at $x = \pm a$, $y = 0$. We seek to calculate $a$ as a function of $b$.

The foci have the property that $d_1 + d_2 = \text{constant}$ for every point on the ellipse, where:
$$d_+ = \sqrt{(x-a)^2 + y^2}, \qquad d_- = \sqrt{(x+a)^2 + y^2}$$

The x-intercepts are $x = \pm b$, $y = 0$. Here $d_+ + d_- = |b - a| + |b + a| = 2b$.

The y-intercepts are $x = 0$, $y = \pm 1$, whereby:
$$d_+ + d_- = 2\sqrt{a^2 + 1}$$

Whereby:
$$\sqrt{a^2 + 1} = b \quad \Rightarrow \quad a^2 + 1 = b^2$$

*(b is the y-factor)* So if $b = 1.2$: $a = \sqrt{1.44 - 1} = \sqrt{0.44} \approx 0.67$ — **quite large!**

---

## Pages 108–109 — Weinberg–Salam and W Bosons as Vectors

To get W-S, we want the mass-like term to be mediated by a boson instead. That is, take:

$$\mathcal{L}_{\text{local}} = g(\bar{\nu}_e e_L + \bar{e}_L \nu_e) + g'(\bar{\nu}_R e_R + \bar{e}_R \nu_R)$$

and turn it into something like:

$$\mathcal{L}_{WS} = g_0 W_+ \bar{\nu}_L e_L + g_0 W_- \bar{e}_L \nu_L$$

Putting $g' = 0$. These $W^\pm$ are still scalars. How are they turned into a vector field? Presumably by writing something like $W_\pm = \partial_\mu W_\pm^\mu$, etc. Then:

$$\mathcal{L}_{WS} = g_0 (\sigma_\mu \otimes \tau_0) W_\mu^{\ +} \bar{\nu}_L e_L + g_0 (\sigma_\mu \otimes \tau) W_\mu^{\ -} \bar{e}_L \nu_L$$

This has the essential form necessary for W-S, and naturally goes with the term:

$$(\bar{\nu}_L\; \bar{e}_L)\; \frac{1}{2}\big((\sigma_0 \otimes \tau_0) B_\mu + \bar{\tau}_0 \otimes \tau_3 B^{\ \mu}\big)\begin{pmatrix} \nu_L \\ e_L \end{pmatrix}$$

Yet how can we properly expect $g_0 = g_e$? In general, we cannot. Such would be the source of the so-called Weinberg angle, which is just a kludge to allow $g_0 \neq g_e$ and yet still pretend a gauge field of $SU(2)$ symmetry.

Now, is there any reason $B$ and $W^\pm$ should be massive? It seems funny they should be, in view of the fact that a massive field is one that shifts L and R components, yet this one specifically couples only to itself.

---

## Pages 110–124 — What is a Spinor?

*(Numbered paper, pages 5–15)*

### The Spinor as a Two-Component Complex Vector

A spinor is a two-component complex vector:

$$\begin{pmatrix} \alpha \\ \beta \end{pmatrix} \tag{11}$$

which exists in an abstract complex space. At the same time, it is commonly understood that this abstract space has some connection with the spacetime we live in, by virtue of the spin matrices. For example, the spin of a particle in the Z direction is given by:

$$\frac{1}{2} \otimes \sigma_z \begin{pmatrix} \alpha \\ \beta \end{pmatrix} \tag{12}$$

etc. As such, we understand that this abstract space has something to do with direction, but what? How does one map $(x, y, z, t)$ into a spinor and vice versa?

Part of the problem we face is that a spinor contains a certain amount of ambiguity. If any 2-spinor field $\Psi_+$ is a solution of the Weyl equation, then so is $a\Psi_+$, where $a$ is any complex number. *(This is only a trivial phase-invariance and normalization of theory.)* Thus, considered at any point $x_0$, $a\Psi_+(x_0) = \begin{pmatrix} a\alpha \\ a\beta \end{pmatrix}$. $\tag{13}$

The values $\alpha$ and $\beta$ have no meaning in any absolute terms. The only real meaning is in the single complex ratio:

$$\eta = \frac{\alpha}{\beta} \tag{14}$$

which is invariant under the transformation $\Psi_+ \to a\Psi_+$.

This immediately raises the question: if a spinor's only real content consists of a single complex number, why must it be represented by two complex numbers? Why can't it be represented as a single complex number and have an ordinary scalar wave equation? **In the answer to this question lies the key to what a spinor is.**

### What is a Spinor?

*(Section heading, crossed out in original)*

Rather than trying to work backward to what a spinor is, we will state what it is and then show why this "what" leads to the spinor's natural structure. As it turns out, that structure is rather convoluted *(it is not very easy to guess)*, and not so easy to work backward.

We understand that a scalar $q$ is a magnitude only. A vector $\vec{v} = x\hat{x} + y\hat{y} + z\hat{z}$ is both a magnitude and a direction. **A spinor, then, is a direction without a magnitude.** It should be no surprise that a spinor has something to do with direction in as much as it describes spin, or intrinsic angular momentum, and angular momentum is directional.

Note that angular momentum is also apparently the same — $\frac{1}{2}\hbar$ — for all spinor particles, so no magnitude information is really needed.

To complete this geometrical picture, a map between a direction-without-magnitude and a complex spinor is needed. A direction without magnitude can be described as a point on the unit sphere:

$$x^2 + y^2 + z^2 = r^2 \tag{15}$$

Every point on this sphere corresponds to a particular direction. Every vector starting at the origin passing through this sphere passes through a single point which indicates its directional component.

To equate the unit sphere with spinors, we need a mapping between it and the complex plane, which consists of all complex numbers $\alpha + i\beta$. Since the surface of a sphere is two-dimensional and the complex plane is two-dimensional, a mapping can be imagined.

However, the sphere is topologically different from the plane. On a sphere, one may proceed in a certain direction and eventually return to the point where they started. On a plane, going in any direction will never lead back to where one started. **This topological difference between the sphere and the plane** *(a direction-without-magnitude)* **is the source of the reason why a spinor cannot be described by a single complex number.** (We will come to it in a moment.)

### Stereographic Projection

There is a well-known mapping between the unit sphere and the complex plane in the mathematics of complex analysis, known as the **stereographic projection**. Imagine a sphere with radius $\frac{1}{2}$ situated with its center on the Z axis, at $x=0$, $y=0$, $z=\frac{1}{2}$. Then the bottom of the sphere will be at the origin and the top will be at $x=0$, $y=0$, $z=1$ on the Z axis.

Now, if one draws a line from $(0,0,1)$ that passes through any point on the sphere or the plane, the line will intersect the sphere exactly once and the plane exactly once. This creates defines a one-to-one mapping of the sphere into the plane.

If we let $(x,y,z)$ be the coordinates on the sphere centered at the origin, we translate the sphere up $\frac{1}{2}$ unit:

$$(x,y,z) \to (x',y',z') = \left(x, y, z+\frac{1}{2}\right)$$

whereby:

$${x'}^2 + {y'}^2 + \left(z' - \frac{1}{2}\right)^2 = \frac{1}{4} \tag{17}$$

Now, a line passing through $(0,0,1)$ and $(\alpha, \beta, 0)$ is parameterized by the equations:

$$x = \frac{1}{2}\alpha t \tag{18a}$$
$$y = \beta t \tag{18b}$$
$$z = 1 - t \tag{18c}$$

with $t$ ranging from 0 to 1. This line will intersect the sphere at:

$$(\alpha t)^2 + (\beta t)^2 + \left(\frac{1}{2} - t\right)^2 = \frac{1}{4} \tag{19}$$

or:

$$\alpha^2 + \beta^2 + \frac{1}{4t^2} + 1 - \frac{1}{t} = \frac{1}{4t^2} + \frac{1}{2} \tag{20}$$

which gives:

$$t = (\alpha^2 + \beta^2 + 1)^{-1} \tag{21}$$

or, writing $\zeta = \alpha + i\beta$:

$$\zeta = \alpha + i\beta \tag{22a}$$
$$t = (1 + |\zeta|^2)^{-1} \tag{23}$$

Whereupon:

$$x = \frac{\zeta + \bar{\zeta}}{1 + |\zeta|^2} \tag{24a}$$

$$y = \frac{\zeta - \bar{\zeta}}{1 + |\zeta|^2} \tag{24b}$$

$$z = \frac{|\zeta|^2}{1 + |\zeta|^2} \tag{24c}$$

and:

$$\zeta = \frac{x + iy}{1 - z} \tag{25}$$

These define the stereographic projection in both directions.

Yet this stereographic projection has a problem due to the topological difference between the sphere and the plane. The one point where it does not work is at the very top of the sphere, $x=0$, $y=0$, $z=1$. In this case, $\zeta$ takes the ambiguous form $0/0$, which tends to $\infty$ in every direction of approach.

The standard solution which complex analysts use is to add the single point $\infty$, called infinity, to the complex plane. Then $(x,y,z) = (0,0,1) \leftrightarrow \infty$ and the mapping is complete.

Note that this choice, to map all "infinite points", if you will, into the single point $\infty$ effectively forces the topology of the plane to become that of the sphere. It effectively equates all possible infinities. Another mapping could be imagined that did not do that, but then we would not have a stereographic projection for the sphere.

Our purpose here is not to explore such mappings, but to show how a single complex number maps into a direction-without-magnitude. Yet it is this one point, $\infty$, which makes the direct mapping of a spinor/complex number into a direction-without-magnitude impossible. One must wonder that a single mathematical point should cause so much trouble, but it does, since it is the difference between two topologies.

In order to define all of the mapping without an abstract point $\infty$, we must write $\zeta$ as a ratio of two complex numbers:

$$\zeta = \frac{\xi}{\eta} \tag{26}$$

Now $\zeta$ can be $\infty$ if $\eta = 0$ and $\xi$ is any finite number. Thus we may write:

$$x = \frac{\xi\bar{\eta} + \eta\bar{\xi}}{\bar{\xi}\xi + \eta\bar{\eta}} \tag{27a}$$

$$y = \frac{\xi\bar{\eta} - \eta\bar{\xi}}{\bar{\xi}\xi + \eta\bar{\eta}} \tag{27b}$$

$$z = \frac{\xi\bar{\xi} - \eta\bar{\eta}}{\bar{\xi}\xi + \eta\bar{\eta}} \tag{27c}$$

Clearly there is some ambiguity in $\xi$ and $\eta$, because if $\xi$ and $\eta$ solve (27) then so do $\lambda\xi$ and $\lambda\eta$, where $\lambda$ is any complex number. This is exactly the ambiguity we observed in a spinor, summarized in eq. (14). As such, we may recognize $\xi$ and $\eta$ as two components of a spinor.

In consequence, we may understand the spinor as a direction, since every point on a sphere corresponds to a unique direction. To fully understand the spinor, though, we must consider it in the context of Minkowskian 4-space.

### Spinors in Minkowski 4-Space

Every null vector satisfies:

$$V_0^2 - V_x^2 - V_y^2 - V_z^2 = 0$$

which is the equation of a sphere of radius $V_0^n$. More generally, the set of all such vectors corresponds to the "light cone." Physically speaking, all of the points on the light cone are points connected by the origin along the trajectories of massless particles. These points are "zero distance" from the origin in Minkowski space.

If we think in terms of length contraction and time dilation, as any body or particle approaches the speed of light, the distance along its direction of motion contracts as:

$$d = d_0\sqrt{1 - v^2/c^2}$$

and time dilates as:

$$t = t_0 / \sqrt{1 - v^2/c^2}$$

In that body's frame of reference, the distances between two objects gets smaller, and the time required to travel between them shrinks. In the limit $v \to c$, the dimensions of time and direction of motion collapse. If we could speak of the frame of reference of a photon, then all points through which it travels are identified. They are zero distance apart and zero time apart. In this sense, every line along the light cone is as a single point. Every vector pointing to a point on this line has only a direction, and zero length. **This is exactly what we understood a spinor to be — a direction without a length.**

### Spinors, Space Reflection and Time Reversal

If we consider two points in space, $x_1$ and $x_2$, then, at any given time, there are exactly four connections between them on the light cone, two past and two future:

- $f_{12} = \left(\frac{|\Delta x|}{c},\; \vec{X}_2 - \vec{X}_1\right) = \left(\frac{|\Delta x|}{c},\; \Delta\vec{x}\right)$
- $f_{21} = \left(\frac{|\Delta x|}{c},\; \vec{X}_1 - \vec{X}_2\right) = \left(\frac{|\Delta x|}{c},\; -\Delta\vec{x}\right)$
- $p_{12} = \left(-\frac{|\Delta x|}{c},\; \Delta\vec{x}\right)$
- $p_{21} = \left(-\frac{|\Delta x|}{c},\; -\Delta\vec{x}\right)$

where $\Delta\vec{x} = \vec{X}_2 - \vec{X}_1$.

Note that $p_{21} = -f_{12}$ and $p_{12} = -f_{21}$.

These four vectors represent the only possible direct communication paths between $x_1$ and $x_2$ using massless particles. They also represent the space and time reflections of a null vector. Writing the space reflection operator as $\mathcal{S}$ and the time reflection operator as $\mathcal{T}$, we have:

$$f_{21} = \mathcal{S}(f_{12}), \quad p_{12} = \mathcal{T}(f_{12}), \quad p_{21} = \mathcal{T}(f_{21})$$
$$p_{21} = \mathcal{S}(p_{12}), \quad p_{21} = \mathcal{S}(\mathcal{T}(f_{12})) = -f_{12}, \quad p_{12} = \mathcal{T}(\mathcal{S}(f_{21})) = -f_{21}$$

From these relations we can work out the effect of $\mathcal{S}$ and $\mathcal{T}$ on spinors. Recognizing the "1" in the denominator of (25) as $t$ on the light cone, we may write:

$$\zeta = \frac{x + iy}{t - z}$$

and:

$$\mathcal{S}(\zeta) = \frac{-x - iy}{t + z} = -\frac{t - z}{x - iy} = -\frac{1}{\zeta^*}$$

$$\mathcal{T}(\zeta) = -\left(\frac{x + iy}{-t + z}\right) = -\frac{1}{\zeta^*}$$

*(for the definitions of space and time reflection)*

We then use the fact that:

$$x^2 + y^2 = t^2 - z^2$$

or $(x + iy)(x - iy) = (t - z)(t + z)$, or $\frac{x+iy}{t+z} = \frac{t-z}{x-iy}$, to write:

$$\mathcal{S}(\zeta) = -\left(\frac{x+iy}{t+z}\right) = -\frac{t-z}{x-iy} = -\frac{1}{\zeta^*}$$

Likewise:

$$\mathcal{T}(\zeta) = -\left(\frac{x+iy}{t+z}\right) = -\left(\frac{t+z}{x-iy}\right) = -\frac{1}{\zeta^*}$$

In terms of two-component spinors $\zeta = \xi/\eta$, the ambiguity in the definitions of $\xi$ and $\eta$ leaves some ambiguity in the definition of the action of $\mathcal{S}$ and $\mathcal{T}$ on them. For example, we might write:

$$\mathcal{S}(\xi/\eta) = -\eta^*/\xi^*$$

and say:

$$\mathcal{S}(\xi) = -\eta^*, \qquad \mathcal{S}(\eta) = \xi^*$$

etc. Yet this is rather ambiguous given the variability in $\eta$ and $\xi$.

### Stereographic Projection — Detailed Derivation (Revised)

*(Pages 121–124 present a rederivation for general sphere of radius $r$.)*

Sphere equation: $x^2 + y^2 + z^2 = r^2$

Parametric line from $(0,0,r)$ through $(\alpha, \beta)$ on the plane at $z=0$:

$$x = \alpha t, \quad y = \beta t, \quad z = r(1-t)$$

with $t = 0$ at top, $t=1$ at $(\alpha, \beta)$.

Substituting into the sphere equation:

$$(\alpha t)^2 + (\beta t)^2 + r^2(1-t)^2 = r^2$$

$$\frac{2r}{t} = r^2 + \alpha^2 + \beta^2 \quad \Rightarrow \quad t = \frac{2r}{r^2 + \alpha^2 + \beta^2}$$

If $\eta = \alpha + i\beta$:

$$x = \frac{r^2(\eta + \eta^*)}{r^2 + \eta\eta^*}, \qquad y = \frac{-ir^2(\eta - \eta^*)}{r^2 + \eta\eta^*}, \qquad z = r\cdot\frac{\eta\eta^* - r^2}{r^2 + \eta\eta^*}$$

And the inverse:

$$\eta = \frac{x + iy}{t} = \frac{x + iy}{r - z}$$

The $\eta = \frac{x+iy}{r-z}$ formula is independent of $r$, given that $x,y,z$ are on the sphere.

#### Inverse Stereographic Projection: Finding $(x_0, y_0)$

Given $(x_c, y_c, z_c)$ on the sphere and seeking $(x_0, y_0)$ on the plane:

$$x_c = \frac{2r^2 x_0}{r^2 + x_0^2 + y_0^2}, \quad y_c = \frac{2r^2 y_0}{r^2 + x_0^2 + y_0^2}, \quad z_c = r\left(\frac{x_0^2 + y_0^2 - r^2}{x_0^2 + y_0^2 + r^2}\right) \tag{30a,b,c}$$

Solving for $x_0$ (setting $y_0 = 0$ for simplicity and using a rotation to generalize):

$$x_c x_0^2 - 2r^2 x_0 + x_c r^2 = 0 \tag{32}$$

$$x_0^\pm = \frac{r}{x_c}\left(r \pm \sqrt{r^2 - x_c^2}\right) \tag{33}$$

Generally, there are two points on the sphere with $x = x_c$, one at $z_c$ and one at $-z_c$.

The spinor ratio:

$$\tilde{\zeta} = \frac{x_0 + iy_0}{r} \tag{34}$$

From similar triangles (Figure 1, stereographic projection):

$$\zeta^*_g = \frac{x_c + iy_c}{r - z_c} \tag{36}$$

Note that $x_0^+ x_0^- = r^2$ (37) and $\frac{x_0}{r} = \frac{r}{x_0^+}$ (38).

From Figure 2:

$$\frac{x_c}{r - z_c} = \frac{r + z_c}{x_c} \tag{39}$$

or when rotated:

$$\frac{x_c + iy_c}{r - z_c} = \frac{r + z_c}{x_c - iy_c} \tag{40}$$

Comparing these results with (23a) and (23b), we may see that the **stereographic projection defines a unique complex number $\zeta$ which is the ratio of the two spinor components of a null quaternion treated as a pair of spinors.** In other words, we must treat this as two separate projections from the antipodes. The "top" involves a rotation by $\theta$ and the bottom by $-\theta$.

It would be nice to show that all of the ambiguity in the spinor is due to the arbitrariness of the projection.

---

## Pages 127–140 — Spinor Functions

*(New spiral-bound notebook, repeats/continues spinor paper)*

### Spinor Functions

A spinor function $\Psi(x)$ assigns a spinor — a direction-without-magnitude — to each point of spacetime. We would like to investigate how equations of motion for spinor functions act on the various forms of the spinor. Let's consider the basic equation:

$$\sigma^\mu \partial_\mu \Psi = (\partial_0 - \sigma^i \partial_i)\Psi = 0$$

If we write:

$$\Psi = \begin{pmatrix} \eta \\ \xi \end{pmatrix}$$

then:

$$\partial_0 \begin{pmatrix} \eta \\ \xi \end{pmatrix} = \begin{pmatrix} 0 & \partial_x - i\partial_y \\ \partial_x + i\partial_y & 0 \end{pmatrix} \begin{pmatrix} \eta \\ \xi \end{pmatrix} + \begin{pmatrix} \partial_z & 0 \\ 0 & -\partial_z \end{pmatrix} \begin{pmatrix} \eta \\ \xi \end{pmatrix}$$

or:

$$\partial_0 \eta = \partial_x \xi - i\partial_y \xi + \partial_z \eta$$
$$\partial_0 \xi = \partial_x \eta + i\partial_y \eta - \partial_z \xi$$

Rewriting:

$$(\partial_0 - \partial_z)\eta = (\partial_x - i\partial_y)\xi \tag{1a}$$
$$(\partial_0 + \partial_z)\xi = (\partial_x + i\partial_y)\eta \tag{1b}$$

Can we write an equation for the spinor ratio $\eta/\xi$? Write $\varphi_g = \eta/\xi$, then $\eta = \varphi\xi$. Substituting into (1a) and (1b):

$$(\partial_0 - \partial_z)\varphi\xi = (\partial_x - i\partial_y)\xi = \varphi(\partial_0 - \partial_z)\xi + (\partial_0 + \partial_z)\varphi \cdot \xi$$
$$-(\partial_0 + \partial_z)\xi = (\partial_x + i\partial_y)(\varphi\xi) = \xi(\partial_x + i\partial_y)\varphi + \varphi(\partial_x + i\partial_y)\xi$$

This seems an intractable mess! Do we need to write a 2nd-order equation out of it?

$$(\partial_0 + \partial_z)(\partial_0 - \partial_z)(\varphi\xi) = (\partial_0 + \partial_z)\left[\varphi(\partial_0 - \partial_z)\xi + \xi(\partial_0 - \partial_z)\varphi\right]$$
$$= (2\partial_0 + \partial_z)\ldots$$

Taking (1b) and applying $(\partial_0 - \partial_z)$ to both sides, using (1a):

$$(\partial_0^2 - \partial_z^2)\xi = (\partial_0 - \partial_z)(\partial_x + i\partial_y)\eta = (\partial_x + i\partial_y)(\partial_x - i\partial_y)\xi = (\partial_x^2 + \partial_y^2)\xi$$

or:

$$(\partial_0^2 - \nabla^2)\xi = 0 \tag{2b}$$

Likewise we can show $(\partial_0^2 - \nabla^2)\eta = 0$ (2a), whereby we have the wave equation for $\xi$ and $\eta$.

Writing $\varphi = \eta/\xi$ and then $\eta = \varphi\xi$:

$$(2b') \quad (\partial_0^2 - \nabla^2)(\varphi\xi) = 0$$

$$\partial_0^2(ab) = \partial_0(a\partial_0 b + b\partial_0 a) = 2\partial_0 a\,\partial_0 b + a\partial_0^2 b + b\partial_0^2 a$$

So:

$$0 = \xi\partial_0^2\varphi + \varphi\partial_0^2\xi + 2(\partial_0\varphi)(\partial_0\xi) - \xi\nabla^2\varphi - \varphi\nabla^2\xi - 2(\nabla\varphi)\cdot(\nabla\xi)$$

Applying (2a):

$$\xi(\partial_0^2\varphi - \nabla^2\varphi) = 2(\nabla\varphi)\cdot(\nabla\xi) - 2(\partial_0\varphi)(\partial_0\xi)$$

Could we split these, writing both:

$$\partial_0^2\varphi - \nabla^2\varphi = 0 \tag{3a}$$

and:

$$(\nabla\varphi)\cdot(\nabla\xi) - (\partial_0\varphi)(\partial_0\xi) = 0 \tag{3b}$$

Then interpreting (3a) as an equation of motion for $\varphi$ and (3b) as a "gauge" term?

Maybe we should work the other way. Suppose we have a 4-vector field $V_\mu(x)$. We want to constrain $V_\mu$ to be such that it is always on the light cone:

$$V_0^2(x) - V_x^2(x) - V_y^2(x) - V_z^2(x) = 0$$

and always unimodular. Both of these conditions impose constraints on $V_\mu(x)$ that should be expressible as differential equations.

Let us begin with the light-cone constraint. To simplify this, consider only one dimension. If $V_\mu(x_0)$ is on the light cone then:

$$V_0(t_0) = V_z(x_0) \tag{4}$$

Let us then write:

$$V_\mu(x_0 + \Delta x) = V_\mu(x_0) + \Delta x^\mu \partial_\mu V_\mu(x_0)$$

The light-cone constraint for $V_\mu(x_0 + \Delta t)$ is then:

$$V_0(x_0 + \Delta x) + \Delta x^0\partial_0 V_0 + \Delta x^1\partial_1 V_0 = V_1(x_0) + \Delta x^0\partial_0 V_1 + \Delta x^1\partial_1 V_1$$

and applying (4):

$$\Delta x^0\partial_0 V_0 - \Delta x^1\partial_1 V_0 = \Delta x^0\partial_0 V_1 - \Delta x^1\partial_1 V_1$$

or, generalizing:

$$\Delta x^\mu \partial_\mu V_0 = \Delta x^\mu \partial_\mu \vec{V}$$

and for any $\Delta x^\mu$:

$$\boxed{V^\mu \partial_\mu V_0 = \vec{\Delta x}\cdot\nabla V_\mu}$$

We'd like to eliminate the $\Delta x$'s and get an equation in $V$. Think about this in 2-d again: if $V_0(x_0) = u_0$ then $V_1(x_0) = \pm u_0$, so that $V_0^2(x_0) - V_1^2(x_0) = 0$.

From the unimodular condition plus the light-cone constraint we derive (in 4D):

$$\boxed{V^\mu \partial_\nu V_\mu = 0}$$

This is the essential equation. And since $u^\mu = V^\mu(x_0)$, the field equation is:

$$\boxed{V^\mu \partial_\nu V_\mu = 0}$$

This reduces, in 2D, to:

$$V^0\partial_0 V_0 = V^1\partial_1 V_1, \qquad V^0\partial_1 V_0 = V^1\partial_1 V_1$$

*(It works, using the example above.)*

Now if we also constrain $V^\mu$ to have a fixed length, so that it becomes a direction-without-magnitude, then $V\cdot V = 1 = V_x^2 + V_y^2 + V_z^2$. The unit-length condition gives:

$$\boxed{\vec{V}\cdot(\partial_\mu\vec{V}) = 0}$$

Combining with $V^\mu\partial_\nu V_\mu = 0$, we also obtain $V^0\partial_\mu V_0 = 0$, whereby $V_0 = \text{const}$, which makes complete sense, and the vector equation tells us that $\vec{V}$ varies such that $\partial_\mu\vec{V}$ is at right angles to $\vec{V}$ for all $\mu = 0\ldots 3$. In other words, $\vec{V}$ varies from point to point only by a rotation.

If we convert this to a spinor, using $\zeta = \frac{x+iy}{t-z}$, or here $\zeta = \frac{V_1+iV_2}{V_0-V_3}$, or $\eta = V_1+iV_2$, $\xi = V_0-V_3$ with $\zeta = \eta/\xi$.

### Maxwell Equations from the Weyl Equation Applied to Null Vectors

$$\sigma^\mu\partial_\mu = \begin{pmatrix} \partial_0 - \partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_0 + \partial_z \end{pmatrix}$$

So:

$$\sigma^\mu\partial_\mu \begin{pmatrix} \eta \\ \xi \end{pmatrix} = \begin{pmatrix} (\partial_0-\partial_z)\eta + (\partial_x - i\partial_y)\xi \\ -(\partial_x+i\partial_y)\eta + (\partial_0+\partial_z)\xi \end{pmatrix} = 0 \tag{1}$$

With $\xi = V_x + iV_y = V_0 - V_z$ and $\eta = t - z$. Separating real and imaginary parts (since $V_\mu$ is real):

$$\partial_0 V_x - \partial_z V_x - \partial_x V_0 + \partial_x V_z = 0$$
$$\partial_0 V_y - \partial_z V_y + \partial_y V_0 - \partial_y V_z = 0$$
$$-\partial_x V_x + \partial_y V_y + \partial_0 V_0 + \partial_z V_0 - \partial_0 V_z + \partial_z V_0 = 0$$
$$\partial_y V_x - \partial_x V_y = 0$$

By symmetry, arguing therefore $\nabla \times \vec{V} = 0$, these reduce to:

$$\partial_0 V_x - \partial_z V_x + \partial_x V_z = 0 \tag{2a}$$
$$\partial_0 V_y + \partial_y V_0 = 0 \tag{2b}$$
$$\partial_0 V_0 + \partial_z V_0 - \nabla\cdot\vec{V} + 2\partial_y V_y = 0 \tag{2c}$$

By symmetry again:

$$\boxed{\partial_0 \vec{V} = -\nabla V_0} \tag{3b}$$

whereby:

$$\partial\partial_0 V_0 + \partial_0 V_0 - \nabla\cdot\vec{V} + 2\partial_y V_y = 0 \tag{3a}$$

and by symmetry:

$$\boxed{\partial_0 V_0 = \vec{\nabla}\cdot\vec{V}}$$

Considering the pair of equations simultaneously:

$$\sigma^\mu\partial_\mu\begin{pmatrix} \xi \\ \eta \end{pmatrix} = 0 \quad \text{and} \quad \sigma^\mu\partial_\mu\begin{pmatrix} \xi' \\ \eta' \end{pmatrix} = 0$$

If $\xi' = -\eta^*$ and $\eta' = \xi^*$, then these equations transform into:

- $(3b)$: $\partial_0\eta + \partial_z\eta - \partial_x\xi^* - i\partial_y\xi^* = 0$
- $(3a)$: $\partial_x\eta - i\partial_y\eta - \partial_0\xi^* + \partial_z\xi^* = 0$

These are the same as (1a) and (1b). But if we treat $\xi'$ and $\eta'$ as independent fields, we have more degrees of freedom.

**"Let me find grace in thy sight, oh Yahweh. Let I might see thy way here."**

These transform into Maxwell equations. 4-vectors are transformed into spinors by way of quaternions. Any 4-vector is a quaternion by virtue of:

$$q = \sigma^\mu V_\mu$$

and this is a $2\times2$ matrix of the form:

$$q = \begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

This $q$ consists of two spinors: $\frac{V_x - iV_y}{V_0 + V_z}$ and $\frac{V_0 - V_z}{V_x + iV_y}$.

Or if we prefer, two 2-component spinors:

$$\varphi_1 = \begin{pmatrix} V_0 - V_z \\ -V_x - iV_y \end{pmatrix}, \quad \varphi_2 = \begin{pmatrix} -V_x + iV_y \\ V_0 + V_z \end{pmatrix}$$

---

## Pages 141–160 — Spinors as Null Vectors; Vector Decomposition

### Light-Cone Field Equation (Boxed Result)

From the constraint that $V_\mu(x)$ always lies on the light cone and is unimodular:

$$\boxed{V^\mu\partial_\nu V_\mu = 0}$$

$$\boxed{\vec{V}\cdot(\partial_\mu\vec{V}) = 0}$$

And combining: $V^0\partial_\mu V_0 = 0$.

### Is a Spinor a Null Vector?

Write a 4-vector as:

$$V = \sigma^\mu V_\mu = \begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

If $V$ is a null vector, $V^\mu V_\mu = 0$, and then the left-hand and right-hand columns are equal within a constant $k$:

$$\frac{V_0 - V_z}{-V_x - iV_y} = \frac{-V_x + iV_y}{V_0 + V_z}$$

which gives $V_0^2 - V_z^2 = V_x^2 + V_y^2$, i.e., $V^\mu V_\mu = 0$.

If we alternatively write $V = \sigma^\mu V_\mu$ as a tensor product:

$$(k_1 \quad k_2) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} k_1\alpha & k_2\alpha \\ k_1\beta & k_2\beta \end{pmatrix}$$

This tensor product always represents a null vector if $k_1\alpha$ is real (which requires $k_1 = k_0\alpha^*$, $k_2 = k_0'\beta^*$ where $k_0, k_0'$ are real). Thus:

$$\sigma^\mu V_\mu = (k_0\alpha^* \quad k_0'\beta^*) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$$

where $k_0' = k_0$. The spinor $\begin{pmatrix} \alpha \\ \beta \end{pmatrix}$ with complex $\alpha$ and $\beta$ forms a null vector via the tensor product $(\alpha^*\;\beta^*) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$.

### Decomposition of Any Vector into Two Null Vectors

Can any vector $V_\mu$ (not null) be composed of two null vectors?

$$V_\mu = a_\mu + b_\mu, \qquad a^\mu a_\mu = 0, \quad b^\mu b_\mu = 0$$

$$V^\mu V_\mu = 2a^\mu b_\mu$$

For a timelike $V_\mu = (t, \vec{V})$, a possible decomposition is:

$$\boxed{V_\mu = \left(\frac{1}{2}(t + |\vec{V}|),\; \frac{1}{2}(\vec{V} + \hat{V}\,t)\right) + \left(\frac{1}{2}(t - |\vec{V}|),\; \frac{1}{2}(\vec{V} - \hat{V}\,t)\right)}$$

$$= \frac{1}{2}\left(1 + \frac{V_0}{|\vec{V}|}\right)(|\vec{V}|,\; \vec{V}) + \frac{1}{2}\left(1 - \frac{V_0}{|\vec{V}|}\right)(-|\vec{V}|,\; \vec{V})$$

This is a possible decomposition, but not the only one. $(t, 0)$ can break down into $(t/2, \hat{u}\,t/2) + (t/2, -\hat{u}\,t/2)$ for any unit vector $\hat{u}$.

### Classification of $V_\mu$ by Type

| $V_\mu$ | $V_0$, $|\vec{V}|$ | $1 + V_0/|\vec{V}|$ | $1 - V_0/|\vec{V}|$ |
|---|---|---|---|
| + timelike | $V_0 > |\vec{V}|$ | $> 1$ | $< 0$ |
| − timelike | $V_0 < -|\vec{V}|$ | $< 0$ | $> 1$ |
| + spacelike | $V_0 < |\vec{V}|$ | $> 1$ | $> 1$ |
| − spacelike | $V_0 > -|\vec{V}|$ | $> 1$ | $> 0$ |

Two possible decompositions for spacelike, only 1 for timelike. On the spacelike, we can switch the signs of both — just the order is all that changes.

*(Two light-cone diagrams drawn showing decomposition geometry for timelike and spacelike cases. Intersection of two light cones is a hyperbolic or elliptic surface generally.)*

- Timelike points → ellipse
- Spacelike points → 2 hyperbolas
- The ellipse and hyperbolas are 2D surfaces, generally

### Solution for Timelike $V_\mu$

For timelike $V_\mu$: consider 2 points, $a_\mu$ and $0$. Then $V_\mu = a_\mu + b_\mu$ where $a_\mu$ is on the 0-light cone and $b_\mu$ is on the light cone for $V_\mu$:

$$a^\mu a_\mu = 0 \quad (a), \qquad (V_\mu - a_\mu)(V^\mu - a^\mu) = 0 \quad (b)$$

So: $V_\mu V^\mu - 2a_\mu V^\mu + a_\mu a^\mu = V^\mu V_\mu - 2a^\mu V_\mu = 0$

Writing $v^2 = V^\mu V_\mu \neq 0$:

$$2a^\mu V_\mu = v^2 \qquad (b')$$

and $a_0^2 = a_x^2 + a_y^2 + a_z^2 \quad (a')$.

Pick any direction $\hat{a}$. Then:

$$a_\mu = (a_0, a_0\hat{a}) \quad \text{is a null vector}$$

$$V_\mu = a_\mu + b_\mu = a_\mu + (V_\mu - a_\mu)$$

Both $a_\mu$ and $V_\mu - a_\mu$ on the light cone:

$$a^\mu a_\mu = 0, \qquad (V_\mu - a_\mu)(V^\mu - a^\mu) = 0$$

$$(V_\mu - a_\mu)(V^\mu - a^\mu) = V_\mu V^\mu - 2V_\mu a^\mu + a_\mu a^\mu = 0$$

$$v^2 = V_\mu V^\mu = 2V_\mu a^\mu = 2V^\mu a_\mu = 2a_0 V_0 - 2\hat{a}\cdot\vec{V} \cdot a_0$$

which can be solved for $a_0$:

$$\boxed{a_\mu = \frac{1}{2V_0}\left(V_0^2 - |\vec{V}|^2 + 2\hat{a}\cdot\vec{V}\right)(1,\;\hat{a})}$$

$$\boxed{b_\mu = V_\mu - a_\mu}$$

**This is valid for all positive timelike $V_\mu$.**

Note that $\sqrt{V_\mu V^\mu} = \det(\sigma^\mu V_\mu)$.

---

## Pages 161–175 — Maxwell Equations from Spinor; Final Stereographic Results

### Weyl Operator Acting on a Vector/Quaternion

$$\sigma^\mu\partial_\mu\Psi = \begin{pmatrix} \partial_0 - \partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_0 + \partial_z \end{pmatrix}\begin{pmatrix} \psi_1 \\ \psi_2 \end{pmatrix} = 0$$

Acting on the quaternion $\sigma^\mu V_\mu$:

$$\begin{pmatrix} \partial_0 - \partial_z & -\partial_x + i\partial_y \\ -\partial_x - i\partial_y & \partial_0 + \partial_z \end{pmatrix}\begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

The result expands to four equations, two from each row. Writing them out with real $V_\mu$:

$$(\partial_0 - \partial_z)(V_0 - V_z) + (\partial_x - i\partial_y)(V_x + iV_y) = 0 \tag{1a}$$
$$(\partial_x + i\partial_y)(V_0 - V_z) + (\partial_0 + \partial_z)(V_x + iV_y) = 0 \tag{1b}$$

$$(\partial_0 - \partial_z)(V_x - iV_y) + (\partial_x - i\partial_y)(V_0 + V_z) = 0 \tag{2a}$$
$$(\partial_x + i\partial_y)(V_x - iV_y) + (\partial_0 + \partial_z)(V_0 + V_z) = 0 \tag{2b}$$

Separating real and imaginary parts (since $V_\mu$ is real):

From (1a):
$$\partial_0 V_0 + \partial_z V_z - \partial_z V_0 - \partial_0 V_z + \partial_x V_x - \partial_y V_y + \partial_y V_x + \partial_x V_y = 0 \quad \text{Re(1a)}$$

From Im(1a): $\partial_x V_y - \partial_y V_x = 0$ ✓

By symmetry and combining equations:

$$(\nabla\times\vec{V})_z = 0 \Rightarrow \nabla\times\vec{V} = 0 \tag{2d}$$

$$\partial_0\vec{V} = -\nabla V_0 \tag{7}$$

$$\nabla\times\vec{V} = 0 \tag{8}$$

$$\vec{\nabla}\cdot\vec{V} = -\partial_0 V_0 \tag{9}$$

Adding and subtracting Re(1b) and Re(2a):

$$\partial_0 V_x + \partial_x V_0 = 0 \tag{4+} \checkmark$$
$$\partial_z V_x - \partial_x V_z = 0 \tag{4-} \checkmark$$

Adding and subtracting Re(2b) and Re(1a):

$$\partial_0 V_0 + \partial_x V_x + \partial_y V_y + \partial_z V_z = 0 \tag{5+} \checkmark$$
$$\partial_z V_0 + \partial_0 V_z = 0 \tag{5-} \checkmark$$

**These are Maxwell-like equations to be sure:**

$$\nabla\times\vec{B} = -\partial_0\vec{E}, \qquad \vec{\nabla}\cdot\vec{B} = 0$$
$$\nabla\times\vec{E} = \partial_0\vec{B}, \qquad \vec{\nabla}\cdot\vec{E} = 0$$

in source-free form. There is no $E_0$, $B_0$ here.

### Wave Equation from (7) and (9)

Applying (9) to (7):

$$\partial_0(\nabla V_0) = -\partial_0^2\vec{V} = \nabla(\partial_0 V_0) = -\nabla(\nabla\cdot\vec{V})$$

And for $\nabla\times\vec{V} = 0$:

$$= \nabla^2\vec{V}$$

So (7), (8), and (9) together give:

$$\boxed{\partial_0^2\vec{V} = \nabla^2\vec{V}} \tag{10}$$

which is the standard wave equation.

At this level it appears that $\vec{V}$ is completely decoupled from $V_0$, and $V_0$ is defined as a sort of ancillary field for which:

$$\nabla V_0 = -\partial_0\vec{V}, \qquad \partial_0 V_0 = -\vec{\nabla}\cdot\vec{V}$$

Now suppose $\vec{V} = v\hat{z}\,e^{i(kz-\omega t)}$. Then requiring $k^2 = \omega^2$ for (10):

$$\partial_0\vec{V} = -i\omega v\hat{z}\,e^{i(kz-\omega t)}$$

so $\nabla V_0 = i\omega v\hat{z}\,e^{i(kz-\omega t)}$ and $\vec{\nabla}\cdot\vec{V} = ikv\hat{z}\,e^{i(kz-\omega t)}$, giving:

$$V_0 = v\,e^{i(kz-\omega t)} \quad \text{if and only if } k = \omega \text{ (not } k = -\omega\text{)}$$

So: $(\partial_0^2 - \nabla^2)V_\mu = 0 \tag{11}$

### Null Vector Constraint Equations

Now, suppose $V_\mu$ is a null vector. Then $V_0$ is essentially determined by $\vec{V}$:

$$V_0 = \sqrt{V_x^2 + V_y^2 + V_z^2}$$

Can equations (7) and (9) be satisfied?

$$\nabla V_0 = \nabla\sqrt{V_x^2 + V_y^2 + V_z^2} = \frac{1}{2V_0}(2V_x\partial_x V_x + 2V_y\partial_y V_y + 2V_z\partial_z V_z)\,\ldots$$

$$= \frac{1}{\vec{V}_0}\vec{V} = -\partial_0\vec{V}$$

or:

$$V_0\partial_0\vec{V} = -\vec{V} \tag{12}$$

From (12), write $\partial_0\vec{V} = -\vec{V}/V_0$ and combine with (13) to get:

$$V_0(\vec{\nabla}\cdot\vec{V}) = -\vec{V}\cdot(\partial_0\vec{V})$$

$$\vec{\nabla}\cdot\vec{V} = \frac{\vec{V}\cdot\vec{V}}{V_0^2} = 1$$

but from (7): $\vec{\nabla}\cdot\vec{V} = -\partial_0 V_0$

Working this through carefully:

$$-V_0\partial_0\vec{V} = V_j\partial_j V_j \quad j = x,y,z \tag{14'}$$
$$V_0\vec{\nabla}\cdot\vec{V} = -\vec{V}\cdot\partial_0\vec{V} \tag{15'}$$

### Transverse vs Longitudinal Waves

If $\nabla\times\vec{V} = 0$, can $\vec{V}$ exist as a longitudinal or transverse wave?

This is the "spin-0 condition." If $\vec{V} = v\hat{z}\,e^{i(kz-\omega t)}$, then $\partial_z V_z \neq 0$ but $\partial_x V_z$, $\partial_y V_z$ etc. are all 0, so $\nabla\times\vec{V} = 0$ and longitudinal waves are OK.

A pure transverse wave, e.g., $\vec{V} = v\hat{x}\,e^{i(kz-\omega t)}$, has $\partial_z V_x \neq 0$ but $\partial_x V_z = 0$, so it is **not allowed**. One way or another, this drives us to a **pure longitudinal wave**.

### Stereographic Projection — Summary (Numbered Paper, Pages 20–21)

*Figure 1: Stereographic projection diagram — sphere of radius $r$ with point $(x_c, y_c, z_c)$ on the sphere and $(x_0, y_0)$ on the plane at $z=0$.*

We may compute $(x_0, y_0)$ for any given $(x_c, y_c, z_c)$ by parametrizing the line:

$$x(t) = x_0 t \tag{27a}$$
$$y(t) = y_0 t \tag{27b}$$
$$z(t) = r(1-t) \tag{27c}$$

Now, at $(x_c, y_c, z_c)$ the sphere equation is satisfied:

$$(x_0 t)^2 + (y_0 t)^2 + r^2(1-t)^2 = r^2 \tag{28}$$

Solving for $t$:

$$t = \frac{2r^2}{r^2 + x_0^2 + y_0^2} \tag{29}$$

So:

$$x_c = \frac{2r^2 x_0}{r^2 + x_0^2 + y_0^2}, \qquad y_c = \frac{2r^2 y_0}{r^2 + x_0^2 + y_0^2}, \qquad z_c = r\cdot\frac{x_0^2 + y_0^2 - r^2}{x_0^2 + y_0^2 + r^2} \tag{30a,b,c}$$

The inverse solutions for $(x_0, y_0)$ in terms of $(x_c, y_c, z_c)$ (taking $y_c = 0$ for simplicity):

$$x_c = \frac{2r^2 x_0}{r^2 + x_0^2} \tag{31}$$

or:

$$x_c x_0^2 - 2r^2 x_0 + x_c r^2 = 0 \tag{32}$$

with solutions:

$$x_0^\pm = \frac{r}{x_c}\left(r \pm \sqrt{r^2 - x_c^2}\right) \tag{33}$$

Generally speaking, there are two points on the sphere with $x = x_c$, one at $z_c$ and one at $-z_c$.

The quantities $x_0/r$ and $y_0/r$ depend only on the direction. These may be written as a complex number:

$$\tilde{\zeta} = \frac{x_0 + iy_0}{r} \tag{34}$$

From the law of similar triangles, we see from Figure 1 that $\frac{x_c}{r - z_c} = \frac{x_0}{r}$, so:

$$\zeta^*_g = \frac{x_c + iy_c}{r - z_c} \tag{36}$$

Note that $x_0^+ x_0^- = r^2$ (37) and $\frac{x_0}{r} = \frac{r}{x_0^+}$ (38).

From Figure 2:

$$\frac{x_c}{r - z_c} = \frac{r + z_c}{x_c} \tag{39}$$

or when rotated:

$$\frac{x_c + iy_c}{r - z_c} = \frac{r + z_c}{x_c - iy_c} \tag{40}$$

Comparing with (23a) and (23b), we may see that the stereographic projection defines a unique complex number $\zeta$ which is the ratio of the two spinor components of a null **quaternion** treated as a pair of spinors.

We must treat this as two separate projections from the antipodes. The "top" involves a rotation by $\theta$ and the bottom by $-\theta$. Be exact here, and explain carefully. We want to fully understand the quaternion $V$. Use $V_\mu$ not $x_\mu$. Fully explore the arbitrariness of the Z axis and the inherent ambiguity in the spinor.

**★ It would be nice to show that all of the ambiguity in the spinor is due to the arbitrariness of the projection.**

---

## Pages 176–182 — Construction of Null Vectors; Spinor Paper Outline

### Two Coordinate Systems

Consider two separate coordinate systems and their respective stereographic representations $(x_s, y_s, z_s)$ versus $(x_s', y_s', z_s')$ and $(x_0, y_0)$ vs $(x_0', y_0')$.

Rotation about $z$: changes overall phase of $(x_0, y_0)$, sending $x_0 + iy_0 \to e^{i\theta}(x_0 + iy_0)$.

- $Z$ determined by direction of motion of photon
- $R$ of sphere determines relative magnitude
- What is overall phase?

### Outline for Spinor Paper

*(Marked with × for to-do items)*

1. Deal with null vectors as tensor products
2. Discuss breakdown of non-null vectors into 2 null vectors
3. Discuss equations of motion of spinor field

### Construction of Null Vectors as Tensor Products

$$(\alpha^* \quad \beta^*) \otimes \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} \alpha\alpha^* & \beta^*\alpha \\ \alpha^*\beta & \beta^*\beta \end{pmatrix} = \begin{pmatrix} V_0 - V_z & -V_x + iV_y \\ -V_x - iV_y & V_0 + V_z \end{pmatrix}$$

So $\det Q = \alpha\alpha^*\beta\beta^* - \alpha^*\beta\alpha\beta^* = 0$ ✓

$$\alpha\alpha^* = V_0 - V_z, \qquad \beta\beta^* = V_0 + V_z, \qquad \alpha^*\beta = -V_x - iV_y$$

Write:

$$\alpha = \sqrt{V_0 - V_z}\,e^{i\theta}, \qquad \beta = \sqrt{V_0 + V_z}\,e^{i\phi}$$

$$\alpha^*\beta = \sqrt{(V_0-V_z)(V_0+V_z)}\,e^{i(\phi-\theta)} = \sqrt{V_0^2 - V_z^2}\,e^{i(\phi-\theta)} = \sqrt{V_x^2+V_y^2}\,e^{i(\phi-\theta)}$$

so:

$$\frac{V_x + iV_y}{\sqrt{V_x^2 + V_y^2}} = -e^{i(\phi-\theta)}$$

**Ambiguity of $e^{i\theta}$ key.**

### Null Matrix Factorization

A matrix $M = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ with $\det(M) = ad - bc = 0$:

$$ad = bc \quad \Rightarrow \quad \frac{a}{b} = \frac{c}{d} \quad \text{and} \quad \frac{a}{c} = \frac{b}{d}$$

So if $b = \alpha a$ then $c = \alpha d$; if $c = \beta a$ then $d = \beta b$; so:

$$M = \begin{pmatrix} a & \alpha a \\ \beta a & \alpha\beta a \end{pmatrix} = a\begin{pmatrix} 1 & \alpha \end{pmatrix} \otimes \begin{pmatrix} 1 \\ \beta \end{pmatrix}, \quad \alpha = b/a$$

### Timelike Decomposition (Final Form)

1) **Timelike** — diagram shows $a$ and $b$ both future-pointing with $a + b = b + a = V$:

$$\frac{1}{2}(V_0^2 - |\vec{V}|^2)^{1/2} = a_0(V_0 - \hat{a}\cdot\vec{V})$$

2) **Spacelike** — diagram shows $a + b = V = b + a$

**Timelike:** $a_\mu = (a_0, a_0\hat{a})$ is a null vector.

$$V_\mu = a_\mu + b_\mu = a_\mu + (V_\mu - a_\mu)$$

For both $a_\mu$ and $V_\mu - a_\mu$ on the light cone:

$$a^\mu a_\mu = 0, \qquad (V_\mu - a_\mu)(V^\mu - a^\mu) = 0$$

$$(V_\mu - a_\mu)(V^\mu - a^\mu) = V_\mu V^\mu - 2V_\mu a^\mu + a_\mu a^\mu = 0$$

$$v^2 \equiv V_\mu V^\mu = 2V_\mu a^\mu = 2a_0 V_0 - 2a_0(\hat{a}\cdot\vec{V})$$

which can be solved for $a_0$:

$$a_0 = \frac{1}{2V_0}(V_0^2 - |\vec{V}|^2 + 2\hat{a}\cdot\vec{V})$$

$$\boxed{a_\mu = \frac{1}{2V_0}(V_0^2 - |\vec{V}|^2 + 2\hat{a}\cdot\vec{V})(1,\;\hat{a})}$$

### Final Calculation — Null Component Geometry (Last Pages)

$$a_0 = \frac{1}{2V_0}(V_0^2 - |V|^2 + 2\hat{a}\cdot\vec{V}) = b + \hat{a}\cdot\vec{u}$$

where $\hat{a} = \frac{a_x\hat{x} + a_y\hat{y} + a_z\hat{z}}{\sqrt{a_x^2 + a_y^2 + a_z^2}}$, $b = \frac{V_0^2 - |V|^2}{2V_0}$, $\vec{u} = \frac{\vec{V}}{V_0}$.

If $\vec{V}$ is along the $\hat{z}$ axis, then $u_x = u_y = 0$ and:

$$a_0(V_0 - a_z V_z) = \frac{1}{2}(V_0^2 - V_z^2)$$

$$\sqrt{a_x^2 + a_y^2 + a_z^2} = a_0 = \frac{1}{4}\cdot\frac{(V_0^2 - V_z^2)}{(V_0 - a_z V_z)^2}$$

$$a_x^2 + a_y^2 + \left(a_z - \frac{1}{2}V_z\right)^2 = \frac{1}{4}\alpha, \qquad \alpha = 1 - \frac{V_z^2}{V_0^2}$$

where $\alpha > 0$ if $|V_z| < |V_0|$ (timelike) and $\alpha < 0$ if $|V_z| > |V_0|$ (spacelike).

In cylindrical coordinates:

$$\rho_s = \frac{2r\,\rho_0}{r^2 - \rho^2}, \qquad \theta_s = \theta_0$$

*(End of notebook)*

---