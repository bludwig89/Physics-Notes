# Reference Research Papers 1–6 — Derivations, Ideas, and CA Model Comparison

*Compiled 2026-05-15. Paper 6 added 2026-05-15. Source PDFs in `Reference Research/`. Companion to `ca-reference.md`, `ca-unified-proposition.md`, and `ostoma-trushyk-1999-summary.md`.*

The six documents form a coherent (if not entirely uniform) literature on cellular-automaton physics:

1. **Bisio, D'Ariano, Perinotti, Tosini (2015) — *Free QFT from Quantum Cellular Automata***. *Foundations of Physics* 45, 1137. The axiomatic / informational-principles derivation.
2. **Raynal (2017) — *Simple Derivation of the Weyl and Dirac Quantum CA***. arXiv:1703.05890v2. A cleaner re-derivation of the BCC-lattice result via the Gram matrix.
3. **Ostoma & Trushyk (1999) — *Special Relativity Derived from Cellular Automata Theory***. Privately circulated, ~50 pp. A heuristic, physically-motivated CA derivation of SR, paired with the EMQG / Quantum Inertia program. *This is the SR-focused excerpt of Paper 6.*
4. **Bisio, D'Ariano, Perinotti, Tosini (2016) — *Weyl, Dirac and Maxwell Quantum CA: analytical solutions and phenomenological predictions***. arXiv:1601.04842. Same group as Paper 1; deeper phenomenology and explicit testable predictions.
5. **Fredkin (1990) — *Digital Mechanics***. *Physica D* 45, 254–270. The original CA-as-physics manifesto: a single reversible CA rule is hypothesized to model all of microscopic physics exactly. Source of the "Digital Mechanics" lineage cited by Papers 3 and 6.
6. **Ostoma & Trushyk (1999) — *Cellular Automata Theory and Physics: A New Paradigm For The Unification of Physics***. Privately circulated, 100 pp. The full Ostoma–Trushyk treatise. Paper 3 is its SR-only excerpt; Paper 6 adds the complete EMQG (Electro-Magnetic Quantum Gravity) framework — quantum inertia, three mass definitions, gravity-as-photon-scattering through the accelerating vacuum, EMQG field equations, and Milne kinematic cosmology. A detailed structured summary is in `ostoma-trushyk-1999-summary.md`.

Papers 1, 2, and 4 are rigorous mathematical derivations of QCA structures equivalent to the free Weyl / Dirac / Maxwell equations. Papers 3 and 6 are physics-essay re-derivations of SR (paper 3) and SR+GR+QFT+cosmology (paper 6) from a generic 3D-cubic CA, with quantum-vacuum/inertia speculation layered on top. Paper 5 is the foundational manifesto for the field. Papers 1 and 4 share three authors and form a deliberate pair (review + phenomenology); papers 3 and 6 share authors and form a corresponding pair (SR excerpt + full unification proposal).

---

## Paper 1 — Free QFT from Quantum Cellular Automata

### Core claim

Free quantum field theory (Weyl, Dirac, Maxwell in vacuum) can be **derived** — not assumed — from five informational principles applied to a discrete cellular automaton:

(1) linearity, (2) unitarity, (3) locality, (4) homogeneity, (5) isotropy.

Plus a minimality-of-internal-dimension constraint: each cell carries a Fermionic field with $s$ components, and $s$ is chosen to be the smallest value admitting a non-trivial evolution. The result: $s=2$ (a 2-spinor) in dimensions 1, 2, 3.

### Cayley graph as emergent geometry

Homogeneity + locality forces the cells to sit at the vertices of a **Cayley graph** of some group $G$, with edges labelled by a generator set $S$. Each cell-update rule has the form

$$\psi_g(t+1) = \sum_{g' \in S_g} A_{gg'}\,\psi_{g'}(t).$$

Isotropy adds a covariance condition: there exists a finite subgroup $L$ of graph automorphisms and a faithful unitary representation $U_l$ such that

$$A = \sum_{h \in S} T_h \otimes A_h = \sum_{h \in S} T_{l(h)} \otimes U_l A_h U_l^\dagger, \qquad \forall l \in L. \tag{Paper 1, Eq. 5}$$

Unitarity gives quadratic constraints on the $A_h$:

$$\sum_{h \in S} A_h^\dagger A_h = \mathbb{I}, \qquad \sum_{\substack{h,h' \in S \\ h^{-1}h' = h''}} A_h^\dagger A_{h'} = 0 \quad (h'' \neq e). \tag{Paper 1, Eq. 6}$$

### Spacetime is emergent

The discrete time $T$ comes from the automaton's update steps; space $X$ comes from the **word-metric** $d_x$ on the Cayley graph (length of the shortest word in $S$ connecting two vertices). For Abelian $G$ quasi-isometrically embeddable in $\mathbb{R}^n$ (i.e. *virtually Abelian*), the embedding space is a **Bravais lattice**; for non-Abelian $G$, the embedding lives on a curved manifold (e.g. hyperbolic $\mathbb{H}^2$ in the paper's Fig. 1).

This is the paper's strongest single line: *no spacetime background is assumed; the lattice metric and time coordinate fall out of the group structure of the automaton.*

### The Weyl QCA (BCC lattice in 3D)

For $G = \mathbb{Z}^3$ with isotropic embedding in $\mathbb{R}^3$, **only the body-centered cubic (BCC) lattice** admits a non-trivial $s=2$ unitary automaton. The two solutions (modulo unitary conjugation) are

$$A^{\pm}_{\mathbf{k}} = I\,u^{\pm}_{\mathbf{k}} - i\boldsymbol\sigma \cdot \tilde{\mathbf{n}}^{\pm}_{\mathbf{k}}, \qquad
\tilde{\mathbf{n}}^{\pm}_{\mathbf{k}} = \begin{pmatrix} s_x c_y c_z \mp c_x s_y s_z \\ \mp c_x s_y c_z - s_x c_y s_z \\ c_x c_y s_z \pm s_x s_y c_z \end{pmatrix}, \quad u^{\pm}_{\mathbf{k}} = c_x c_y c_z \pm s_x s_y s_z, \tag{Paper 1, Eq. 15}$$

with $c_i := \cos(k_i/\sqrt 3)$, $s_i := \sin(k_i/\sqrt 3)$. The dispersion relation is

$$\omega^{\pm}_{\mathbf{k}} = \arccos(c_x c_y c_z \pm s_x s_y s_z).$$

In 2D the only choice is the **square lattice**, with unique solution

$$\tilde{\mathbf{n}}_{\mathbf{k}} = (s_x c_y,\ c_x s_y,\ s_x s_y),\qquad u_{\mathbf{k}} = c_x c_y, \qquad
\omega_{\mathbf{k}} = \arccos(c_x c_y),\quad c_i := \cos(k_i/\sqrt 2). \tag{Paper 1, Eq. 16}$$

In 1D the unique solution is $A_k = u_k I - i\boldsymbol\sigma\cdot\tilde{\mathbf{n}}_k$ with $\tilde{\mathbf{n}}_k = (0, 0, \sin k)$, $u_k = \cos k$, $\omega_k = k$.

### Recovery of Weyl, Dirac, Maxwell

The **interpolating Hamiltonian** $H^A_I(\mathbf{k})$ is defined by $A_{\mathbf{k}} = e^{-iH_I^A(\mathbf{k})}$, and a power expansion in $\mathbf{k}$ around $\mathbf{0}$ gives

$$i\partial_t \psi(\mathbf{k}, t) = H_A(\mathbf{k})\psi(\mathbf{k}, t), \qquad H_W(\mathbf{k}) = \frac{1}{\sqrt d}\boldsymbol\sigma\cdot\mathbf{k}, \tag{Paper 1, Eq. 21}$$

which is exactly the **Weyl Hamiltonian in $d$ dimensions**. The factor $1/\sqrt d$ is the lattice-imposed speed of light (the analog of the CFL bound in finite-difference schemes).

**Dirac** is obtained by coupling two Weyl automata $W_{\mathbf{k}}$ and $W'_{\mathbf{k}}$ via a $4\times 4$ matrix with off-diagonal mass blocks. The unique local-coupling solution is

$$D_{\mathbf{k}} = \begin{pmatrix} n W_{\mathbf{k}} & im\,I \\ im\,I & n W'_{\mathbf{k}} \end{pmatrix}, \qquad n^2 + m^2 = 1, \tag{Paper 1, Eq. 23}$$

with dispersion $\omega_{\mathbf{k}} = \arccos(\sqrt{1-m^2}\,u_{\mathbf{k}})$. Power-expanding the interpolating Hamiltonian for $|\mathbf{k}| \ll 1$ and $m \ll 1$ gives

$$H_D(\mathbf{k}) = \frac{n}{\sqrt d}\gamma^0\boldsymbol\gamma\cdot\mathbf{k} + m\gamma^0 + \mathcal{O}(m^2) + \mathcal{O}(|\mathbf{k}|^2),$$

i.e. the **Dirac Hamiltonian** with rest mass $m$ in the relativistic limit.

**Maxwell** comes from a *composite* construction: build the photon as a correlated pair of Weyl fermions (the De Broglie neutrino theory of light). Define bilinears $G^i_T(\mathbf{k}, t)$, then the operators $\mathbf{E}_G := |\mathbf{n}_{\mathbf{k}/2}|(\mathbf{G}_T + \mathbf{G}_T^\dagger)$, $\mathbf{B}_G := i|\mathbf{n}_{\mathbf{k}/2}|(\mathbf{G}_T^\dagger - \mathbf{G}_T)$ obey

$$2\mathbf{n}_{\mathbf{k}/2}\cdot\mathbf{E}_G = 0, \quad 2\mathbf{n}_{\mathbf{k}/2}\cdot\mathbf{B}_G = 0, \quad
\partial_t \mathbf{E}_G = i\,2\mathbf{n}_{\mathbf{k}/2}\times\mathbf{B}_G, \quad
\partial_t \mathbf{B}_G = -i\,2\mathbf{n}_{\mathbf{k}/2}\times\mathbf{E}_G. \tag{Paper 1, Eq. 35}$$

In the substitution $2\mathbf{n}_{\mathbf{k}/2} \to \mathbf{k}$ (valid for $|\mathbf{k}|\ll 1$), these are free Maxwell's equations. Bosonic statistics emerge approximately when one defines polarization operators $\gamma^i(\mathbf{k}) := u^i_{\mathbf{k}}\cdot\mathbf{F}(\mathbf{k}, 0)$ with smearing function $f_{\mathbf{k}}(\mathbf{q})$.

### Non-Abelian extension (sketched)

For non-Abelian $G$ quasi-isometric to $\mathbb{R}^n$, the *virtually-Abelian* tiling procedure lets you re-express the automaton on an Abelian subgroup with a larger internal Hilbert space. This is a route to scalar QCAs from spinor ones on non-Abelian groups.

---

## Paper 2 — Simple Derivation via the Gram Matrix

### Same QCA, cleaner derivation

This paper reaches the **same** BCC-lattice QCAs of Paper 1 (and the original Bialynicki-Birula 1994 derivation) by a more transparent route: write the transition matrices $A_h$ in the Pauli decomposition $A_h = \tfrac{\alpha}{2}(\mathbb{I} + \mathbf{a}_h\cdot\boldsymbol\sigma)$, and study the two Gram matrices

$$G^R_{jk} = \mathbf{a}_j\cdot\mathbf{a}_k, \qquad G^C_{jk} = \mathbf{a}_j^*\cdot\mathbf{a}_k. \tag{Paper 2, Eq. 18}$$

### Key structural identity

For the four non-normalized BCC tetrahedron vectors $\mathbf{h}_j$,

$$\mathbf{h}_j\cdot\mathbf{h}_k = 4\delta_{jk} - 1 \quad\Longrightarrow\quad
G = \begin{pmatrix} 3 & -1 & -1 & -1 \\ -1 & 3 & -1 & -1 \\ -1 & -1 & 3 & -1 \\ -1 & -1 & -1 & 3 \end{pmatrix}. \tag{Paper 2, Eq. 20}$$

The transition matrices "essentially are the matrix representation of the vertices of the lattice's primitive cell" (paper's emphasis). This is the same regular tetrahedron + dual tetrahedron structure that Paper 1's BCC analysis lands on, but derived from rank constraints on $G^R, G^C$ rather than from solving the unitarity equations directly.

### Two important constraints

1. **The transition matrix at the centre of the primitive cell vanishes**:  $A_0 = 0$. This is proven rigorously in Paper 2 and was *not* explicitly assumed in earlier derivations. (Paper 1 assumed $A_0 = 0$.)
2. **The amplitude coefficients are fixed**: $\alpha = (1\pm i)/4$ (so $|\alpha|^2 = 1/8$) up to a unitary global phase. There are **only two unitarily-inequivalent automata** (modulo conjugation), realising the two helicity-handed Weyl equations.

### Dispersion

$$\cos\omega_{\pm}(\mathbf{k}) = \cos k_x\cos k_y\cos k_z \pm \sin k_x\sin k_y\sin k_z, \tag{Paper 2, Eq. 65}$$

agreeing with Paper 1 (different conventions, same content). In the continuum limit $|\mathbf{k}|\ll 1$: $\mathcal{H} = -\mathbf{k}\cdot\boldsymbol\sigma$.

### 4D Dirac case (sketched)

Replacing 2D Pauli matrices by the 4D Gamma matrices $\gamma_0, \gamma_i = (0, \sigma_i; -\sigma_i, 0)$, with $\mathbb{I} = \gamma_0\gamma_0$, one obtains a two-parameter family of Dirac QCAs

$$\mathcal{B}(\mathbf{k}, s, \pm) = \begin{pmatrix} s\mathcal{A}(\mathbf{k}) & \pm i\sqrt{1-s^2}\,\mathbb{I} \\ \pm i\sqrt{1-s^2}\,\mathbb{I} & s\mathcal{A}^\dagger(\mathbf{k}) \end{pmatrix}, \tag{Paper 2, Eq. 75}$$

with $s = \sqrt{1-r^2}$, $r$ the dimensionless mass. In the small-mass, small-wavevector limit,

$$i\gamma_0\partial_t\Psi = \mathbf{k}\cdot\boldsymbol\gamma\,\Psi + r\Psi. \tag{Paper 2, Eq. 79}$$

This is the same construction as Paper 1's Eq. 23, with the mass parameter $r = m$ and $s = n$ (so $n^2 + m^2 = 1$).

---

## Paper 3 — Special Relativity Derived from CA (Ostoma & Trushyk)

### Different in kind from Papers 1, 2, 4

This is a **physics-essay**, not a mathematical derivation. The authors postulate a 3D Cartesian cubic CA with 26-cell neighborhood, then argue that the ordinary results of special relativity follow from the structure of the CA. The derivations are physical / verbal rather than formal.

### Core claims

1. **Maximum signal speed is automatic.** Information shifts at most one cell per CA clock cycle, so $V_{\max} = L_P / T_P \approx 3\times 10^8\,\text{m/s} = c$. Light is identified with the *fastest* (single-cell-per-clock) information pattern.
2. **Two-layer spacetime.** Absolute CA space and clock cycles ("CA absolute reference frame") exist but are hidden from experiment. Observers' rulers and clocks measure a different, derived 4D Minkowski spacetime — that's the only spacetime accessible to physical measurement.
3. **Lorentz transformations derived.** From the constancy of $V_P$ in absolute CA units, the algebra goes through:

$$x^* = \gamma(x - vt), \quad t^* = \gamma(t - vx/c^2), \quad \gamma = (1 - v^2/c^2)^{-1/2}, \tag{Paper 3, Eq. 9.2}$$

with $c$ now interpreted as the measured light speed.

### Quantum Inertia and the mass-velocity formula

The paper's most provocative claim: the standard relativistic mass-increase $m = m_0/\sqrt{1-v^2/c^2}$ is **really a force decrease** caused by Doppler-shifted exchange-particle flux. Their derivation: a particle moving at velocity $v$ relative to the source receives exchange bosons at a reduced rate (time-dilation of the exchange-particle flux), so the force is

$$F = F_0\,\sqrt{1 - v^2/c^2}, \tag{Paper 3, Eq. 10.1}$$

and combining $F = ma$ with absolute mass $m \equiv m_0$ gives the same kinematic predictions as Einstein's mass-velocity formula but with a different physical interpretation: it is the *force* that drops to zero as $v\to c$, not the mass that diverges. The two are observationally indistinguishable in any experiment to date.

### EMQG / Quantum Inertia framework (sketched)

- Inertia comes from electromagnetic coupling of mass particles to charged virtual particles of the quantum vacuum (Haisch, Rueda, Puthoff line).
- The quantum vacuum gives a *local* absolute reference frame for **acceleration** (not for constant-velocity motion), resolving Mach's principle.
- Newton's three laws are then re-derived as consequences of the quantum-vacuum exchange-boson dynamics.
- Equivalence principle becomes a derived statement (similar vacuum interactions in accelerated frames and gravitational fields), not a fundamental postulate.

### What is and isn't testable

The mass-vs-force reinterpretation is **observationally indistinguishable** from standard SR by any experiment to date — the paper explicitly acknowledges this. The EMQG-specific predictions (e.g. tiny equivalence-principle violations from differential photon-vs-graviton scattering) are at $\sim 10^{-40}$, far below current sensitivity.

---

## Paper 4 — Weyl, Dirac, Maxwell QCA: phenomenology and predictions

### Same automaton as Papers 1 and 2, with explicit observable predictions

The first half restates the BCC-lattice Weyl automaton (Paper 1's Eqs. 4–6, with the unitary $A^{\pm}_{\mathbf{k}} = d^{\pm}_{\mathbf{k}}I + \tilde{\mathbf{n}}^{\pm}_{\mathbf{k}}\cdot\boldsymbol\sigma$). Dirac with $U_k = \begin{pmatrix} nA_k & imI \\ imI & nA_k^* \end{pmatrix}$, $n^2 + m^2 = 1$. Maxwell as composite bilinear of two Weyl fields.

The novel content is phenomenology.

### Approximate dynamics for narrow wavepackets

Power-expanding the interpolating Hamiltonian to second order gives a **dispersive Schrödinger equation** for the envelope $\bar g(\mathbf{x}, t)$:

$$i\partial_t \bar g(\mathbf{x}, t) = \pm\left[\mathbf{v}\cdot\nabla + \tfrac{1}{2}\mathbf{D}\cdot\nabla\nabla\right]\bar g(\mathbf{x}, t), \tag{Paper 4, Eq. 16}$$

with drift $\mathbf{v} = (\nabla_{\mathbf{k}}\omega)(\mathbf{k}_0)$ (group velocity) and diffusion tensor $\mathbf{D} = (\nabla_{\mathbf{k}}\nabla_{\mathbf{k}}\omega)(\mathbf{k}_0)$. The wave packet spreads as it travels; the spreading is exactly the discreteness signature.

### Phenomenological predictions

**(a) Zitterbewegung.** The 1D Dirac QCA exhibits exact zitterbewegung: positions oscillate at frequency $2mc^2$ around the classical trajectory, with amplitude bounded by $\hbar/(mc)$ (the Compton wavelength). Their Eq. 19 decomposes $\langle X(t)\rangle$ into a drift + an oscillating interference between positive and negative frequency components.

**(b) Klein paradox at a potential step.** For a Dirac particle of mass $m=0.4$ at $k_0 = 2$ hitting a step of height $\phi$, the reflection coefficient $R(\phi)$ rises to $R=1$ on a plateau roughly $\phi \in [m, 2-2m] \approx [1.55, 2.0]$, then drops as transmitted antiparticle modes appear for $\phi > 2-2m$. This is the QCA implementation of the standard Klein paradox.

**(c) Frequency-dependent speed of light.** From the dispersion $\omega(\mathbf{k}) = 2|\mathbf{n}_{\mathbf{k}/2}|$, the photon group velocity at leading order in $|\mathbf{k}|$ is

$$c(\mathbf{k}) \approx 1 \pm \tfrac{1}{\sqrt 3}\,k, \tag{Paper 4, Eq. 23}$$

i.e. the vacuum behaves as a *dispersive medium* with $|\Delta c/c| \sim k$ at the Planck scale. This is the **same form** as predictions from quantum-gravity models (Doubly Special Relativity, Lorentz-violation phenomenology). Possibly testable via differential arrival times of cosmologically distant gamma-ray bursts.

**(d) Cosmic-ray spreading time.** For a proton of mass $m_p \approx 10^{-19}$ in Planck units, the time for the QCA prediction to differ from the standard Dirac prediction by one wave-packet width is

$$t_{\text{CR}} \approx 6\hat\sigma / m_p^2. \tag{Paper 4, Eq. 21}$$

For $\hat\sigma = 10^2\,\text{fm}$ this is $\sim 10^{17}\,\text{s} \approx$ age of the universe — currently unobservable.

**(e) Composite photon polarization deviations.** The photon polarization plane is *not* exactly orthogonal to $\mathbf{k}$; the offset angle is $\theta \approx 10^{-15}$ rad at gamma-ray wavelengths. Far below detection sensitivity.

**(f) Modified Planck blackbody law.** Composite photons give Planck-law deviations $\lesssim 10^{-8}$ — below current experimental sensitivity.

### Deformed Lorentz covariance

A rigid Cayley-graph QCA *cannot* respect ordinary Lorentz covariance — the lattice picks a preferred frame. Paper 4 introduces a **non-linear representation** of the Lorentz group in wave-vector space (Doubly Special Relativity, DSR):

$$L_{\beta}^D := \mathcal{D}^{-1}\circ L_{\beta}\circ \mathcal{D}, \tag{Paper 4, Eq. 25}$$

with $\mathcal{D}: \mathbb{R}^4\to\mathbb{R}^4$ a non-linear deformation map. For the 3D Dirac QCA the result is that the rest mass must transform along with the boosts, and the emergent spacetime is **de Sitter** rather than Minkowski. Lorentz symmetry is *recovered* in the small-$\mathbf{k}$, small-$m$ limit; broken at the Planck scale.

### Interactions (sketched)

To go beyond free fields, relax the linearity assumption in one of the two split-step stages. Doing so yields a local non-trivial gauge coupling — the QCA analog of QED.

---

## Paper 6 — Cellular Automata Theory and Physics (Ostoma & Trushyk, full treatise)

### Relationship to Paper 3

Paper 6 is the **full 100-page version** of the Ostoma–Trushyk program; Paper 3 (the ~50-page "Special Relativity Derived from Cellular Automata Theory") is essentially its §§1–7 (CA postulates, two-layer spacetime, the SR derivation). Paper 6's §§8–20 add the EMQG framework. The structural-CA claims and SR derivation are identical between the two; this section covers what Paper 6 adds.

A full structured summary is in `ostoma-trushyk-1999-summary.md`. This entry only highlights the elements most directly relevant to comparing against Papers 1, 2, 4 and against the implementation in `ca-simulation/`.

### Three mass definitions (§9)

EMQG distinguishes three masses where conventional physics uses one:

| Mass type | Defined by | Source |
|---|---|---|
| **Inertial mass** $m_i$ | $F = m_i a$ — EM resistance to acceleration through the charged virtual vacuum | "Absolute" in EMQG; equals SR rest mass |
| **Gravitational mass** $m_g$ | $F = G m_g M_2 / r^2$ — what a scale measures | Almost equal to $m_i$; differs at $\sim 10^{-40}$ |
| **Low-level "mass charge"** | Pure graviton emission/absorption rate (analog of electric charge in QED) | Not directly measurable; swamped by EM vacuum interactions |

Photons and gravitons carry $m_i$ and $m_g$ (via $E/c^2$) but **no** low-level mass charge — they do not emit/absorb gravitons. This is offered as a resolution of the canonical-quantum-gravity renormalization tangle (graviton self-coupling).

### Quantum Inertia as EMQG postulate (§8)

The third postulate of EMQG: the state of relative acceleration of the charged virtual particles of the quantum vacuum with respect to a mass is what produces inertial force. Newton's $F = M A$ becomes the macroscopic sum of microscopic EM photon-exchange forces between the charged matter particles of the mass and the surrounding accelerating charged virtual particles. Constant-velocity motion has zero net inertial force because the vacuum's acceleration vectors sum to zero in that frame.

### Gravity as Fizeau-like photon scattering (§§17–18)

The most consequential novel claim. **4D curvature is not geometric** — it is the cumulative effect of photons (and matter) scattering off the downward-accelerating charged virtual vacuum near a mass. Concretely:

- Real masses emit gravitons at a fixed rate (the "mass charge" — analog of electric charge in QED).
- Gravitons exchanged with the charged virtual particles of the vacuum cause those virtual particles to accelerate downward (toward the mass).
- The accelerating charged virtual particles then exert EM forces on the charged particles of any nearby test mass, via the same QI mechanism that produces inertia.
- The same accelerating vacuum acts as a Fizeau-like medium for photons: light is continually absorbed and re-emitted by the charged virtual particles, with a time delay constrained by $\Delta E\,\Delta t > \hbar/2$.

The Fizeau analog (Paper 6 §18.3, Eq. 18.31):

$$v_c = \frac{c}{n} + \left(1 - \frac{1}{n^2}\right) V \tag{Paper 6, Eq. 18.31}$$

For the vacuum index of refraction $n \gg 1$, the downward photon velocity becomes (Paper 6, Eqs. 18.51–18.52):

$$v_c(t) = c\left(1 + \frac{g\,t}{c}\right) \quad \text{(downward photon)}, \qquad v_c(t) = c\left(1 - \frac{g\,t}{c}\right) \quad \text{(upward photon)}.$$

This is claimed to reproduce gravitational redshift and time dilation without invoking geometric curvature. **The ladder thought experiment in §18.2 demonstrates that variable-$c$ and curved-geometry interpretations are observationally identical** by any clock/ruler measurement.

### EMQG field equations (§§15, 19)

In the weak-field limit, replace Einstein's tensor equation with a modified Poisson equation in absolute CA coordinates (Paper 6 Eq. 15.2 / 19.7):

$$\nabla^2 \phi - \frac{1}{c^2}\frac{\partial^2 \phi}{\partial t^2} = 4\pi G\, \rho(x,y,z,t). \tag{Paper 6, Eq. 19.7}$$

The acceleration vector of an average virtual particle at $(x,y,z)$ is the gradient of the potential, $\mathbf{a} = \nabla\phi$. The retarded EMQG potential for high-speed mass distributions (Paper 6 Eq. 19.6):

$$\phi_R(\mathbf{x},t) = -G \int \frac{\rho(\mathbf{y},\,t - r/c)}{r}\, d^3 y, \qquad r = |\mathbf{x}-\mathbf{y}|. \tag{Paper 6, Eq. 19.6}$$

These equations are **not generally covariant** — they live in absolute CA coordinates (cell counts, clock counts). The authors argue Einstein's $G_{\alpha\beta} = (8\pi G/c^2)\, T_{\alpha\beta}$ is the same physics formulated for an arbitrary matter-based observer.

### Equivalence principle as a derived "coincidence" (§17.3)

EMQG re-derives WEP rather than postulating it. The vacuum state appears the same in two physical situations:

- **Rocket at 1g**: mass particles accelerate relative to a stationary vacuum.
- **Earth at rest**: vacuum particles accelerate (downward) relative to the stationary mass particles.

The acceleration vectors are reversed in direction but identical in magnitude, so the resulting summed EM forces match. **Prediction:** the principle is *not exact* — pure graviton exchanges between Earth and a test mass slightly upset equivalence for unequal masses, with a larger mass arriving slightly sooner. Imbalance at $\sim 10^{-40}$, currently below experimental sensitivity (current WEP bound: 1 part in $10^{-15}$ for laboratory bodies, $10^{-12}$ for Earth–Moon system).

### Negative mass charge and the cosmological constant (§17.1)

EMQG postulates negative "mass charge" carried by anti-particles. The vacuum contains roughly equal numbers of positive and negative mass-charged virtual particles — explaining why the cosmological constant from vacuum mass-charge cancels (Paper 6's claimed resolution of the CC problem; references Ostoma & Trushyk's own arXiv:physics/9903040).

### Cosmology — Milne kinematic re-read of the Big Bang (§20)

Paper 6 rejects expanding 4D spacetime: the CA cannot create or destroy cells, so 4D space cannot literally expand, and the initial singularity is incompatible with discrete cells. The proposed alternative:

- The cells pre-exist any Big Bang ("hardware" is outside our universe).
- There was a "Matter Creation Era" — virtual/real particle pair production from some violent initial energy yielding a broad isotropic velocity distribution.
- Hubble redshift is reinterpreted as **Milne kinematic cosmology** (Milne 1934): outward inertial motion of matter through pre-existing flat low-level CA space.
- Apparent "expansion of space" is the changing curvature of light's path through the accelerating vacuum — a function of overall matter density, which decreases as matter spreads.

The authors acknowledge Milne cosmology violates the strict cosmological principle (isotropy seen by all observers) but do not consider this fatal.

### Two CA-compatible wavefunction models (§5.1) — both speculative

- **Direct oscillating numeric pattern.** The wavefunction *is* the periodic CA pattern; De Broglie wavelength $\lambda = h/(mv)$ is the spacing of one oscillation cycle in cells. Motion is a Doppler shift of the static pattern.
- **Quantum-vacuum bow-wave (Bohm-like).** The particle is a small information pattern; the wavefunction is the wake of disturbed virtual particles surrounding it.

Both have unresolved issues (large-wavelength coherence; collapse non-locality). Offered as starting points for future work.

### Where Paper 6 sits relative to Papers 1, 2, 4

- Paper 6 is **physics essay** in the same sense Paper 3 is — verbal/heuristic, with worked-out classical equations (modified Poisson, Fizeau analog) but no formal derivation from informational axioms.
- Papers 1, 2, 4 say *nothing* about gravity. Paper 6 says nothing rigorous about Weyl/Dirac structure — the wavefunction models in §5.1 are explicitly tentative.
- The two literatures are **complementary, not competing**: Papers 1, 2, 4 establish the microscopic Weyl/Dirac/Maxwell content of a 3D QCA; Paper 6 proposes a macroscopic vacuum-scattering account of inertia and gravity that sits on top of any underlying CA. In principle they could share a microscopic substrate.
- Where Papers 1, 2, 4 cleanly predict frequency-dependent $c(\mathbf{k})$ from lattice dispersion (Paper 4 Eq. 23, $\Delta c/c \sim k$ at the Planck scale), Paper 6 predicts position-dependent $c(\mathbf{x})$ from accelerated-vacuum scattering near a mass (Paper 6 Eq. 18.51). Both are "variable speed of light" claims with very different physical mechanisms; both produce GR-like phenomenology in their respective regimes.

---

## Synthesis: what these papers establish together

| Question | Established result | Source |
|---|---|---|
| Is a QCA a valid microscopic model of free QFT? | **Yes**, in the small-wavevector / continuum limit. | Papers 1, 2, 4 |
| Which lattice and internal dimension? | **BCC lattice, $s=2$** is the unique choice in 3D for $G = \mathbb{Z}^3$. Square lattice in 2D; $\mathbb{Z}$ in 1D. | Papers 1, 2 |
| What does the spacetime look like at Planck scale? | Discrete; word-metric on a Cayley graph. Emergent, not assumed. | Papers 1, 4 |
| Lorentz covariance? | **Broken at Planck scale**, recoverable in the deformed (DSR) sense. | Paper 4 |
| Speed of light? | Frequency-dependent at Planck scale, $\Delta c/c \sim k/\sqrt 3$. | Paper 4 |
| Particle phenomenology: Zitterbewegung, Klein paradox? | Reproduced exactly. | Paper 4 |
| Photon as elementary or composite? | **Composite** — neutrino-antineutrino bilinear (De Broglie's old idea, made rigorous). | Papers 1, 4 |
| Special relativity from CA structure? | Lorentz transformations follow heuristically from the maximum-information-propagation speed (Papers 3, 6) and rigorously in the small-$\mathbf{k}$ limit (Papers 1, 4). | Papers 1, 3, 4, 6 |
| Mass-velocity formula physical interpretation? | Standard: mass increases. Ostoma-Trushyk: force decreases (flux time-dilated). **Indistinguishable by experiment.** | Papers 3, 6 |
| Origin of inertia? | EM resistance to acceleration through the charged virtual vacuum (Quantum Inertia, modified HRP). Newton's $F=MA$ as macroscopic sum of microscopic photon exchanges. | Paper 6 |
| Origin of gravity? | Photons + matter scattering through a downward-accelerating virtual vacuum (Fizeau analog). Curvature is emergent, not geometric. | Paper 6 |
| Equivalence principle? | Derived: vacuum looks the same in accelerated and gravitational frames (with reversed acceleration directions). Predicted to fail at $\sim 10^{-40}$. | Paper 6 |
| Gravitational redshift / time dilation? | Variable-$c$ from photon scattering through accelerated vacuum: $c(t) = c(1 \pm gt/c)$. Same observations as GR, different ontology. | Paper 6 |
| Field equation? | Modified Poisson with retardation: $\nabla^2\phi - c^{-2}\partial_t^2\phi = 4\pi G\rho$ in absolute CA coordinates. | Paper 6 |
| Cosmology? | Milne kinematic outward flow of matter through pre-existing flat CA space. Cells pre-date the Big Bang. | Paper 6 |

---

## Comparison with the current CA model

The CA implementation in `ca-simulation/` is broadly consistent with the QCA framework of Papers 1, 2, 4, but it differs in specific structural choices. Phase-by-phase:

### Where the current model agrees with the literature

- **Spinor-valued field, $s=2$ internal dimension.** The 2-component Weyl spinor in `ca_core.py` is exactly what Papers 1 and 2 derive as the minimum non-trivial internal dimension. The 4-component Dirac field in `ca_dirac.py` is exactly Paper 1's Eq. 24 / Paper 2's Eq. 75 in the small-mass small-$\mathbf{k}$ limit.
- **Split-step FFT propagator.** The exact-unitary 2D Weyl propagator $U(\mathbf{k}) = \cos(c\kappa)\,I - i\sin(c\kappa)/\kappa\,(\boldsymbol\sigma\cdot\mathbf{k})$ (`ca-reference.md` lines 116–124) is the small-$\mathbf{k}$ linearization of Paper 1's exact QCA dispersion $\omega = \arccos(c_x c_y)$ (2D) — equivalent **only** in the regime $|\mathbf{k}| \ll 1$.
- **Dirac mass coupling.** `ca_dirac.py` implements the off-diagonal $imI$ coupling that matches Paper 1's Eq. 23 / Paper 2's Eq. 75. The dispersion residual of $9\times 10^{-17}$ (Phase D1) is consistent with the predicted $\omega = \arccos(\sqrt{1-m^2}\cos k)$ in 1D.
- **Zitterbewegung at $2mc^2$.** Phase D1 measures the Compton-wavelength oscillation at 3.5% of $2mc^2$, qualitatively matching Paper 4's exact zitterbewegung prediction (Paper 4, Eq. 19).
- **Aharonov–Bohm / per-cell phase structure.** The U(1) phase pickup at $4\times 10^{-16}$ (Phase E1) is a per-cell phase — the same architectural pattern Paper 4 sketches for interacting extensions (relax linearity in one split-step stage to get gauge couplings).

### Where the current model diverges

- **3D lattice is cubic, not BCC.** The `ca_core.py` 3D stepper uses an $L^3$ simple-cubic lattice with 6-neighbor Laplacian. Papers 1 and 2 prove the **unique** non-trivial $s=2$ 3D QCA lives on the BCC lattice (8 neighbors: tetrahedron + dual tetrahedron). The cubic lattice in our 3D code admits only the trivial automaton (identity). **The 3D Weyl regression in the current model is not the same object as the published 3D Weyl QCA.**
- **Dispersion is linearized, not exact.** Our split-step uses $\omega = c|\mathbf{k}|$ at every $\mathbf{k}$; Papers 1, 2, 4 give $\omega = \arccos(c_x c_y)$ (2D) and $\omega = \arccos(c_x c_y c_z \pm s_x s_y s_z)$ (3D BCC). These agree only as $|\mathbf{k}|\to 0$. **The frequency-dependent $c(\mathbf{k})$ of Paper 4 Eq. 23 is absent from the current implementation.**
- **Mass parameter constraint $n^2 + m^2 = 1$.** Paper 1 Eq. 23 / Paper 2 Eq. 75 require the Dirac coupling coefficients to satisfy $n^2 + m^2 = 1$, so $m$ is bounded by 1. Our `ca_dirac.py` takes a free `m` parameter; we should check whether the test values stay in the regime $m \lesssim 1$ and document this constraint.
- **Variable-$c$ as gravity.** Phase C1 (`ca_curved.py`) treats $c(\mathbf{x})$ as a position-dependent metric coefficient — the gravity-by-refraction approach. Papers 1–4 don't address gravity; their $c(\mathbf{k})$ dependence is **intrinsic to the lattice**, not a back-reaction. **Paper 6, by contrast, is the closest published analog**: its Fizeau-vacuum-scattering account of curvature gives $c(t) = c(1 \pm gt/c)$ (Paper 6 Eqs. 18.51–18.52), a position- and direction-dependent variable-$c$ near a mass, identical in form to a refractive-index gradient. The Phase C1 stepper is structurally the same kind of model — it does not derive the dependence from photon-virtual-particle scattering, but the variable-$c$ ansatz is the published Paper-6 hypothesis. Phase F3b's lensing demo is the closest concrete test against Paper 6's predicted scattering-induced light bending. **The two views are complementary, not contradictory:** the QCA framework's $c(\mathbf{k})$ is Planck-scale lattice dispersion; Paper 6 / our $c(\mathbf{x})$ is the macroscopic, position-dependent vacuum index of refraction. A unified model would need both.
- **Composite photon construction absent.** The Maxwell sector of Papers 1 and 4 is built from bilinears of two correlated Weyl fields (the De Broglie photon). Our model has U(1) as an external classical gauge phase, not as a derived composite particle. **This is a clean opportunity — see Test V4 below.**
- **SU(2) on left chirality.** Phase E2's parity-violation construction is consistent with the QCA framework (it's a per-cell phase on a spinor subspace) but is not explicitly derived in Papers 1–4. The weak interaction is not addressed in these papers.
- **Higgs / F-phase work is original.** Papers 1–4 do not address Higgs mass generation. Our Phase F unification proposition stands alone in the project's literature.

### Where the current model **could be replacing an existing measurement** vs **extending beyond**

Per the project's CLAUDE.md test ("either explain existing measurements better, or extend beyond them"):

- **Existing measurements the current model explains.** Weyl dispersion (machine precision), Dirac dispersion with mass (machine precision), Zitterbewegung at $2mc^2$ (3.5%), U(1) Aharonov–Bohm (machine precision), SU(2) parity violation (exact). All consistent with standard QFT, *equivalent to* the QCA framework in the small-$\mathbf{k}$ limit.
- **Extensions beyond.** The unified Phase-F proposition adds Higgs mass generation and metric back-reaction from a single scalar field. The Cayley/CN variable-$c$ stepper achieves Newtonian-gravity-analog deflection (F3b) at machine precision unitarity. These are extensions; they would be falsified if (e.g.) the F3 lensing prediction failed at low fermion density.

The current model and the QCA literature **agree in their domain of overlap** (free Weyl/Dirac in the continuum limit) but **make different choices** about what to extend toward (we go toward Higgs + gravity; D'Ariano *et al.* go toward composite Maxwell + DSR phenomenology). That divergence is the most useful place to look for tests.

---

## Tests and verifications that arise

Ordered roughly by ease of implementation. Items marked **(P)** are independent verification tests against published predictions; **(E)** are extensions of the current code.

### V1. Exact QCA dispersion check (P) — *highest priority*

Replace the linearized FFT propagator's $\omega = c|\mathbf{k}|$ with Paper 1's exact dispersion $\omega_{\mathbf{k}} = \arccos(c_x c_y)$ (2D) and measure the group velocity for plane waves at varying $|\mathbf{k}|$. Expected result for the 2D square-lattice QCA:

$$v_g(\mathbf{k}) = \nabla_{\mathbf{k}}\omega_{\mathbf{k}} = \frac{(s_x c_y/\sqrt 2,\ c_x s_y/\sqrt 2)}{\sin(\omega_{\mathbf{k}})},$$

which deviates from the linearized $|v_g| = c$ by terms of order $|\mathbf{k}|^2$. **Pass criterion:** at $|\mathbf{k}| \approx 0.5$ (well within the Brillouin zone), measure a $\lesssim 10\%$ deviation from $c$ and check it matches the analytic prediction. This is the QCA analog of Phase B1.

### V2. Klein paradox quantitative test (P)

Implement Paper 4's Eq. 20 — a 1D Dirac QCA with a step potential $\phi(x) = \phi\,\theta(x)$. For $m=0.4$, $k_0 = 2$, sweep $\phi \in [0, \pi]$ and measure $R(\phi)$. **Pass criterion:** plateau at $R=1$ for $\phi \in [\sim 1.4, \sim 1.6]$ (the Klein region between $\sim m$ and $\sim 2-2m$), with $R \to 0$ as $\phi \to 0$ and $R$ decreasing for $\phi$ beyond the plateau. Paper 4 Fig. 3 gives a directly comparable plot.

### V3. Mass-parameter constraint $n^2 + m^2 = 1$ (P/E)

Audit `ca_dirac.py` to confirm whether the mass parameter is treated as the dimensionless $m$ of Paper 1 Eq. 23 (bounded by 1) or as a free SI-mass parameter. Document the constraint. **Pass criterion:** existing D1 tests still pass with $m$ explicitly normalized so $n^2 + m^2 = 1$, where $n$ is the kinetic coefficient.

### V4. Composite photon construction (E) — *most physics value*

Implement Paper 1's Maxwell construction: take two correlated Weyl fields $\psi$ and $\varphi$, build the bilinears $G^i(\mathbf{k}, t) = \varphi^T(\mathbf{k}/2, t)\sigma^i\psi(\mathbf{k}/2, t)$, define $\mathbf{E}_G, \mathbf{B}_G$ as in Paper 1 Eq. 35, and verify that

$$\partial_t \mathbf{E}_G = i\,2\mathbf{n}_{\mathbf{k}/2}\times\mathbf{B}_G, \qquad \partial_t \mathbf{B}_G = -i\,2\mathbf{n}_{\mathbf{k}/2}\times\mathbf{E}_G$$

holds in the lattice (substituting $2\mathbf{n}_{\mathbf{k}/2}\to\mathbf{k}$ in the small-$\mathbf{k}$ limit recovers free Maxwell). **Pass criterion:** measured violation of the curl equations decays as $\mathcal{O}(k^3)$ as $|\mathbf{k}|\to 0$. This is a major addition — the current model has no Maxwell sector beyond an externally-imposed U(1) phase.

### V5. Frequency-dependent c (P)

Measure $|v_g(\mathbf{k})|$ for the 2D QCA's exact dispersion and check it matches Paper 4 Eq. 23, $c(\mathbf{k}) \approx 1 \pm k/\sqrt 3$ (or its 2D analog). **Pass criterion:** linear-in-$|\mathbf{k}|$ slope matches the prediction's sign and magnitude.

### V6. 3D BCC vs simple-cubic regression (E)

Currently `ca_core.py` runs a 3D simple-cubic lattice. Implement the BCC lattice (or its equivalent in our split-step framework: 4 generators $\mathbf{h}_j$ instead of $\pm\hat e_i$) and check that the dispersion matches Paper 1 Eq. 15. **Pass criterion:** at $|\mathbf{k}|\ll 1$ the BCC dispersion linearizes to the same $\omega = c|\mathbf{k}|$ as the simple-cubic case, but the corrections at higher $|\mathbf{k}|$ match Paper 1's $\arccos(c_x c_y c_z \pm s_x s_y s_z)$ — and the simple-cubic case does not.

### V7. $A_0 = 0$ audit (P)

Paper 2 proves that the transition matrix at the centre of the primitive cell must vanish. Check that our split-step propagators have no $A_0$ term — verify by inspecting the Fourier-space unitary at $\mathbf{k} = 0$ (it should be the identity, i.e. no on-cell self-coupling). **Pass criterion:** $U(\mathbf{k}=0) = I$ exactly.

### V8. Deformed Lorentz / DSR signature (P) — *low priority*

Implement a discrete boost on a 1D Dirac wave packet using Paper 4's Eq. 24, $\omega(k) = \arccos(\sqrt{1-m^2}\cos k)$, and check that standard Lorentz boosts do **not** preserve the dispersion at large $k$, but the deformed boost $L_{\beta}^D = \mathcal{D}^{-1}\circ L_{\beta}\circ \mathcal{D}$ does. **Pass criterion:** discrete boost preserves $\omega$ at machine precision under the deformed transformation; fails by $\mathcal{O}(k^2/c^2)$ under the standard one.

### V9. Cosmic-ray spreading time (P) — *quantitative spot-check, not a unit test*

Just numerically evaluate Paper 4 Eq. 21 for representative parameters and confirm the prediction lies above current experimental reach. **Pass criterion:** $t_{\text{CR}} > 10^{17}\,\text{s}$ for proton-scale parameters. (This is a sanity check on the published claim, not an extension.)

### V10. Mass-as-force-decrease decisive test (Ostoma-Trushyk, Papers 3, 6) — *speculative*

The Paper 3 / 6 reinterpretation ($F = F_0\sqrt{1-v^2/c^2}$, $m = m_0$) is observationally indistinguishable from standard SR. The authors do not propose any decisive test. **No test arises** — this is a philosophical / interpretive reframing, not an experimentally distinguishable theory. Note this honestly when comparing.

### V11. EMQG modified-Poisson regression (Paper 6) — *natural extension of Phase F3b*

Paper 6 Eq. 19.7 gives the EMQG weak-field potential $\nabla^2\phi - c^{-2}\partial_t^2 \phi = 4\pi G \rho$ as the governing equation for the virtual-vacuum acceleration field whose gradient drives both inertia and gravity. Solve this on the lattice for a static spherical mass distribution and feed the resulting $|\nabla\phi|$ into `ca_curved.py`'s $c(\mathbf{x})$ field (since in Paper 6 the local $c$ varies linearly with $g = |\nabla\phi|$ — Eqs. 18.51–18.52). **Pass criterion:** the resulting Weyl-packet deflection at impact parameter $b$ matches the closed-form Newtonian prediction $\Delta\theta \approx 2GM/(bc^2)$ to within the simulation's geometry tolerance. The F3b setup already produces qualitative bending; this is a regression for *exact Newtonian* deflection from a published derivation rather than the ad-hoc $\alpha=1.5$ exponent currently in F3b. Should also reproduce GR-level light bending at $4GM/(bc^2)$ if the photon's effective potential picks up a factor of 2 from the time-component contribution, per Paper 6's claim of recovering GR observables.

### V12. Gravitational redshift from variable-$c$ (Paper 6) — *cheap and falsifiable*

Paper 6 §18.5 predicts that a clock at height $h$ in a gravitational field runs at rate $\nu' = \nu(1 - gh/c^2)$ purely from the variable-$c$ scattering picture. Set up a uniform $\nabla c$ in `ca_curved.py` (linear $c(z)$ profile) and propagate a monochromatic Weyl plane wave from $z=0$ to $z=L$. Measure the apparent frequency shift in a Fourier window at the receiving end. **Pass criterion:** $\Delta\nu/\nu \approx -|\nabla c|\,L / c$, matching both Paper 6's Eq. 18.51 derivation and the standard GR result at leading order. Failure (or wrong sign) falsifies the variable-$c$ ansatz; success is a direct lattice check of Paper 6's central claim.

### V13. WEP violation order-of-magnitude (Paper 6) — *paper claim is unfalsifiable in lattice*

Paper 6 predicts a ~$10^{-40}$ violation of the weak equivalence principle from differential graviton flux to a heavy vs. light test mass. The current lattice has float64 precision ($\sim 10^{-16}$); the prediction is 24 orders of magnitude below numerical resolution. **No test arises in our framework.** Document this honestly in any future writeup of F3b — Paper 6's WEP-violation prediction cannot be checked numerically with our tooling.

---

## Honest caveats

1. **Papers 3 and 6 are essays, not derivations.** Where Papers 1, 2, 4 are formal mathematical derivations from informational principles, Papers 3 and 6 are physics-essays with verbal arguments. Paper 6 in particular makes substantive claims about gravity, inertia, equivalence, and cosmology that rest on physical analogy (the Fizeau effect, vacuum fluid mechanics) rather than first-principles derivation. The EMQG / Quantum Inertia ideas have not been independently developed in mainstream literature in the 27 years since publication; the authors' modification of the Haisch-Rueda-Puthoff (1994) inertia proposal is the closest mainstream lineage and remains contested. Treat any Paper-6 prediction as a *consistency hypothesis* against the lattice, not an established result.
2. **Lorentz invariance is unsolved.** All four papers acknowledge that rigid lattice QCAs break Lorentz covariance. The DSR / deformed-Lorentz route in Paper 4 is the current best attempt; whether it survives more rigorous scrutiny is an open question. Our model inherits this problem — its choices of 2D square / 3D simple-cubic lattices have the same status as Paper 1's BCC.
3. **The "speed of light" parameter** in our `c` and in the QCA framework's $1/\sqrt d$ factor are the same dimensionless quantity. The notebook's "0.43 stability factor" (page 39) and the QCA framework's $1/\sqrt d$ scaling are the same CFL-like constraint with different conventions.
4. **None of the QCA phenomenological predictions in Paper 4 are currently testable** (cosmic rays: 10⁶⁰ Planck times; polarization angles: 10⁻¹⁵ rad; Planck spectrum deviations: 10⁻⁸). The frequency-dependent $c$ may eventually become testable with cosmologically distant gamma-ray bursts.

---

*A new theory must either explain existing scientific measurements better than the current standard, or extend beyond them in falsifiable ways. The QCA framework of Papers 1, 2, 4 sits in the first category (it reproduces free QFT exactly in the continuum limit; its extensions are not yet testable). Papers 3 and 6 make one decisive predictive move each — reinterpreting $m$-vs-$F$ (both papers) and predicting WEP violation at $10^{-40}$ (Paper 6 only) — that are observationally undecidable today. Paper 6's variable-$c$ account of gravitational redshift and lensing is in principle testable as a lattice consistency check (V11–V12 above), and reduces in the weak field to a published modified-Poisson equation that can be cross-checked against F3b. Our model is currently in agreement with the first category and proposing extensions (Higgs + gravity from one scalar) that have a clearer falsifiability path through F1–F4 regression checks than the QCA framework's Planck-scale predictions do; Paper 6 supplies an external published target for the variable-$c$ branch (Phase C1, F3b) that previously had only project-internal justification.*
