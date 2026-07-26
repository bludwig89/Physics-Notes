# Paper I — The Base Structure of the Cellular-Automaton Universe: A Body-Centred-Cubic Quantum Cellular Automaton and Its Emergent Kinematics

**B. Ludwig**
*Independent researcher*

**Notebook source material:** M. Ludwig (2007), *Physics Notes* (unpublished)

*Series: "A Universe in a Bottle" — Paper I of XI. This paper establishes the substrate, update rule, and emergent special-relativistic kinematics on which all subsequent papers (the photon, mass, the four interactions, and the fermion/lepton/baryon sectors) are built.*

*Revision 2 (2026-06-08): re-issued as Paper I of the eleven-paper series (the matter sector is now split across three papers — fermions IX, leptons X, baryons XI — and the dielectric black hole is given its own Paper VIII). All numerical results carried over from Revision 1 are unchanged.*

*Revision 3 (2026-07-01): the horizon-free "dielectric black hole" paper (formerly Paper VIII, F114) is deprecated following the adoption of the full-tensor induced Einstein equation (F178, Paper VII §4.2) — the exact strong-field object is Schwarzschild/Kerr. Subsequent papers are renumbered consecutively (fermions VIII, leptons IX, baryons X, unification XI, Koide angle XII).*

---

## Abstract

We propose that the physical vacuum is a deterministic quantum cellular automaton (QCA) on a body-centred-cubic (BCC) lattice, and we derive the kinematics that such a substrate forces. Building on the uniqueness results of Bisio, D'Ariano, Perinotti and Tosini for one-particle QCAs, we adopt the BCC Weyl walk with exact dispersion $\omega^\pm(\mathbf k)=\arccos(c_xc_yc_z \pm s_xs_ys_z)$, $c_i=\cos(k_i/\sqrt3)$, $s_i=\sin(k_i/\sqrt3)$, as the free-field propagator. The central structural claim is that the speed of light is not a phase velocity but the **angular rotation rate of a real field pair per unit wavenumber**, $c_\text{lat}=d\Omega/d|\mathbf k|\big|_{|\mathbf k|\to0}=1/\sqrt d$, equal to $1/\sqrt3$ in three dimensions (verified numerically as $0.57735027$). From this single reinterpretation we recover: (i) Maxwell's curl equations as the first-order Taylor expansion of an exact discrete rotation; (ii) the imaginary unit $i$ as the continuum image of a real $2\times2$ rotation generator; (iii) exact (machine-precision) energy conservation as a geometric consequence of length-preserving rotation; and (iv) a falsifiable $O(\omega^2/\omega_\text{Planck}^2)$ correction to the photon dispersion. We further show that the relativistic mass-shell $E^2=p^2c^2+m^2c^4$ is the small-angle limit of an **exact spherical-Pythagorean identity** $\cos\Omega_\text{Dirac}=\cos\Omega_\text{rest}\cdot\cos\omega_\text{kin}$ on the lattice. All structural identities are verified numerically to machine precision. This paper fixes the notation and the foundational results used throughout the series.

---

## 1. Introduction and motivation

The hypothesis examined in this series is the oldest dream of digital physics: that spacetime and its contents are the output of a discrete computational rule running on a lattice, and that the regularities we call "laws of physics" are emergent properties of that rule. If our universe is a cosmic lattice of cellular automata — or one single tremendous one — then a faithful small-scale model should run on a computer. That is the working programme of this series.

This is not a new aspiration (Zuse 1969; Fredkin 1990; 't Hooft 2016), but two ingredients make the present attempt tractable. First, the QCA uniqueness theorems of Bisio *et al.* (2015) show that the requirements of locality, homogeneity, unitarity and isotropy are so restrictive that, in three spatial dimensions, the simplest non-trivial one-particle QCA is essentially **forced** to be the Weyl walk on the BCC lattice. The free dynamics are not chosen; they are derived. Second, modern numerical tooling allows every algebraic claim to be checked to floating-point precision, so the model can be falsified continuously as it is built. Throughout this series we hold to a strict standard of evidence: a structural claim is "exact" only if it reduces to an algebraic identity (ideally bit-for-bit over the rationals), and "machine-precision" if it is verified numerically at the $10^{-14}$–$10^{-16}$ level.

The remainder of the series treats the photon (Paper II), the Higgs-free origin of mass (Paper III), the four interactions (Papers IV–VII: electromagnetism, the strong force, the weak force, gravity — the last including the strong-field regime, exact Schwarzschild/Kerr under the full-tensor source), and the matter content split into the fermion (Paper VIII), lepton (Paper IX) and baryon (Paper X) sectors. The present paper supplies the common substrate and the two foundational reinterpretations — light as rotation, and mass as a second rotation composing spherically with the first — on which every later result depends.

### 1.1 Standing design decisions

This programme deliberately diverges from the Standard Model (SM) in a small number of places, each justified by the lattice structure rather than imposed. The full list of deviations is maintained in `docs/theory/key-decisions.md`; the four that bear on the foundations are:

1. **The speed of light is a rotation rate, not a phase velocity** (§4; Finding F26). This reframes the $O(k)$ "curl residual" of a discrete Maxwell evolution from a numerical defect into a structural prediction.
2. **Mass is generated by Ludwig's chiral-$SU(2)$ complex-mass coupling, not by a Higgs field** (§5; developed fully in Papers III and VI; Finding F27). The would-be Higgs vacuum direction is a pure-gauge degree of freedom of the lattice mass step. Hypercharge is carried on the same gauge field $U(\mathbf x)$, so no scalar appears anywhere in the model.
3. **The electromagnetic photon is a bound pair of two spin-$\tfrac12$ lattice quanta** (de Broglie's neutrino theory of light), not a fundamental spin-1 gauge boson (Paper II; Finding F69).
4. **Gravity is a single impedance-matched lattice dielectric** that renormalises the field-rotation rate of decision 1, with canonical index $K=\exp(2GM/rc^2)$ (Paper VII; Finding F64). This is *not* a metric sourced by a separate mass substance; there is no mass substance, only confined field-rotation energy.

A fifth philosophical commitment runs through the series: the conviction that the universe is both completely intelligible and *elegant* — that its construction is simple — and that the right model should therefore convert SM inputs (the photon, the Weinberg angle, the generation count, Newton's constant) into outputs.

---

## 2. The substrate: a BCC quantum cellular automaton

### 2.1 Why body-centred cubic

A one-particle QCA assigns to every lattice site a finite-dimensional internal state and updates it by a unitary operator that is local (couples only neighbouring sites), homogeneous (the same rule everywhere) and isotropic (covariant under the lattice point group). Bisio, D'Ariano, Perinotti and Tosini (2015) proved that in $d=3$ these constraints admit, at minimal internal dimension $s=2$, exactly the **Weyl automaton on the BCC lattice** (and its parity conjugate). The simple-cubic lattice admits only the trivial automaton; the BCC lattice, whose nearest-neighbour shell is the eight body-diagonal vertices of the surrounding cube, is the unique non-trivial host.

We therefore take the vacuum to be the BCC lattice $\Lambda_\text{BCC}$, with a two-component complex spinor $\psi(\mathbf x,t)\in\mathbb C^2$ at each site. The relevant discrete symmetry group is the cubic point group $O_h$ (order $48$); its representation theory will later (Paper VIII) fix the number of fermion generations at exactly three, and the same count enters the mode count $g_*=48$ that fixes Newton's constant (Paper VII).

### 2.2 The free Weyl walk and its exact dispersion

The single-tick update is a translation-and-rotation acting on the eight neighbours. In momentum space it is a $2\times2$ unitary $W_{\mathbf k}=u(\mathbf k)I_2 - i\,\mathbf n(\mathbf k)\!\cdot\!\boldsymbol\sigma$ with $u^2+|\mathbf n|^2=1$, whose two eigen-phases are the **exact BCC dispersion**

$$
\omega^{\pm}(\mathbf k) = \arccos\!\big(c_xc_yc_z \pm s_xs_ys_z\big),
\qquad c_i=\cos\!\frac{k_i}{\sqrt3},\quad s_i=\sin\!\frac{k_i}{\sqrt3}.
\tag{2.1}
$$

The two branches $\pm$ are the two chiralities/helicities of the walk; they are exchanged by parity, $\omega^+(-\mathbf k)=\omega^-(\mathbf k)$, an identity that becomes load-bearing for the photon in Paper II and for the chirality–helicity correspondence in Paper VIII. Linearising (2.1) about $\mathbf k=0$ gives $\omega^\pm\to|\mathbf k|/\sqrt3$, i.e. an isotropic light cone with slope $1/\sqrt3$; the leading anisotropy is $O(k^2)$ off the cube axes and $O(k)$ along the body diagonals. We confirm the slope directly: along a cube axis $\omega(k,0,0)/k = 0.57735027$ at $k=10^{-4}$, matching $1/\sqrt3 = 0.57735027$ to eight figures.

### 2.3 Conventions used throughout the series

- Lattice units: cell spacing $a$, tick duration $\tau$, with the light-cone constraint $a/\tau = c\sqrt d$ (Option C lightcone; Paper VII fixes $a$).
- $c_\text{lat}\equiv 1/\sqrt d = 1/\sqrt3$ in three dimensions; we set $c_\text{lat}=1$ except where SI numbers are quoted.
- The rotation angle a field pair traverses per tick is written $\Omega$; for the paired photon $\Omega_\text{pair}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ (Paper II).
- Pauli matrices $\boldsymbol\sigma=(\sigma_1,\sigma_2,\sigma_3)$; weak isospin generators $\tau^a/2$; colour generators $T^a=\lambda^a/2$ (Gell-Mann).
- $u\equiv GM/(rc^2)=-\phi/c^2$ is the dimensionless gravitational potential (Paper VII).

---

## 3. The exact discrete-time field rotation

A composite of two correlated lattice spinors furnishes a pair of real three-vectors $(\mathbf E,\mathbf B)$ (the construction is given in Paper II). The free single-tick evolution of this pair is an **exact rigid rotation** in the plane they span:

$$
\mathbf E(t+1) = \cos\Omega\,\mathbf E(t) + \sin\Omega\,\mathbf B(t),
\qquad
\mathbf B(t+1) = -\sin\Omega\,\mathbf E(t) + \cos\Omega\,\mathbf B(t),
\tag{3.1}
$$

with $\Omega = 2\,\omega(|\mathbf k|/2)$. Equation (3.1) is algebraically exact — there is no small-$k$ approximation and no discrete-time truncation. Numerically the rotation residual is $2.0\times10^{-16}$ (machine precision), whereas the residual of the corresponding Maxwell curl law is $2.0\times10^{-2}$ at $k=0.05$. The exactness of (3.1) is the seed of the entire kinematic reinterpretation that follows (Finding F25).

---

## 4. The speed of light as a rotation rate

### 4.1 Statement

> The speed of light $c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf E,\mathbf B)$ vector pair per unit spatial wavenumber:
> $$ c_\text{lat} = \frac{d\Omega}{d|\mathbf k|}\bigg|_{|\mathbf k|\to0}, \qquad \Omega = 2\,\omega(|\mathbf k|/2). \tag{4.1}$$

In classical electromagnetism, $c$ enters as a phase velocity: a plane wave $e^{i(\mathbf k\cdot\mathbf x-\omega t)}$ carries crests of phase that move at $\omega/|\mathbf k|=c$. On the lattice the physical fields are the *real* vectors $(\mathbf E,\mathbf B)$, and their evolution (3.1) is a rotation. Reading $\Omega\approx c_\text{lat}|\mathbf k|$ at small $|\mathbf k|$ identifies $c_\text{lat}$ with the slope of the rotation angle versus wavenumber. **The fields do not move through space; they turn.** What we call a wave "propagating" is the progression in time of this internal rotation. From the linearised dispersion of (2.1), $c_\text{lat}=1/\sqrt d=1/\sqrt3$, a property of the BCC rotation algebra rather than a separately postulated constant.

This reinterpretation is the conceptual pivot of the series. It makes the speed of light a *property of the update rule*, ties it to the spatial dimension $d$, and — when the rotation rate is allowed to vary with position — turns gravity into a renormalisation of $c$ itself (Paper VII).

### 4.2 Maxwell's equations as a linearisation

Taylor-expanding (3.1) to first order in $\Omega$ and dividing by $\Delta t\to0$:

$$
\frac{d\mathbf E}{dt} = \Omega\,\mathbf B = c_\text{lat}|\mathbf k|\,\mathbf B
\;\;\Longrightarrow\;\;
\partial_t\mathbf E = c_\text{lat}\,\nabla\times\mathbf B,
\tag{4.2}
$$

which is Maxwell's curl law. Maxwell's equations are thus the first-order Taylor expansion of $\cos\Omega,\sin\Omega$ in $\Omega$, valid when $\Omega\ll1$. The exact law is the full trigonometric rotation; Maxwell is its linearisation. (This is developed into the electromagnetic sector in Paper IV.)

### 4.3 The imaginary unit is a real rotation in disguise

The one-tick rotation matrix is $R(\Omega)=\left(\begin{smallmatrix}\cos\Omega&\sin\Omega\\-\sin\Omega&\cos\Omega\end{smallmatrix}\right)$. In the $\Delta t\to0$ limit $R(\Omega)\to I+\Omega J$ with

$$
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad J^2=-I.
\tag{4.3}
$$

The antisymmetric generator $J$ is the real-matrix representation of $i$. In this framework the imaginary unit pervading Maxwell theory and quantum mechanics is not fundamental: it is the algebraic artifact of linearising a real rotation in the $(\mathbf E,\mathbf B)$ plane. The Riemann–Silberstein eigenvectors $(1,\mp i)^\mathsf T$ that diagonalise $R(\Omega)$ (Paper II) are the complex repackaging of this real rotation.

### 4.4 Consequences

**(a) Energy conservation is geometric.** A rotation preserves vector length, so $\|\mathbf E\|^2+\|\mathbf B\|^2$ is conserved exactly — Pythagoras, not a dynamical Poynting balance. This is why lattice energy conservation holds to machine precision ($4.8\times10^{-14}$ over 200 ticks) while the Maxwell curl fails at $O(k)$.

**(b) The $O(k)$ curl residual is a prediction.** The difference between the exact rotation and its Maxwell linearisation is $\Delta\mathbf E\approx-\tfrac12\Omega^2\mathbf E$; normalising gives a curl residual per wavenumber of $c_\text{lat}/\sqrt2$, exactly the geometry-independent coefficient measured numerically (Finding F21/F23). The historical "curl residual" is therefore the expected linearisation error of a discrete real rotation, not an open problem.

**(c) A falsifiable Planck-scale dispersion.** At $\Omega\sim\pi/2$ the exact and linearised laws diverge by order unity; the leading phase-velocity correction is

$$
\frac{\delta v_\phi}{c_\text{lat}} \approx -\frac{\Omega^2}{6} = -\frac{c_\text{lat}^2|\mathbf k|^2}{6},
\tag{4.4}
$$

a quadratic-in-frequency ($n=2$) correction testable in principle by gamma-ray-burst arrival-time studies. With the canonical cell of Paper VII the $n=2$ energy scale is $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a \approx 1.36\times10^{19}$ GeV, clearing the LHAASO bound by $\sim1.9\times10^7$ (Finding F28/F107). Any measured $n=2$ time-of-flight bound above that scale would falsify the adopted cell.

---

## 5. Mass as a second rotation: the spherical-Pythagorean mass shell

The free walk of §2 is massless. Mass enters (Papers III, VIII) through a second rotation that mixes the two chiralities $\eta\leftrightarrow\chi$ at rate $\Omega_\text{rest}(m)=\arcsin m$ per tick — Ludwig's chiral-$SU(2)$ complex-mass step (§5.1 below; full treatment in Paper III). The remarkable structural fact is how the two rotations compose.

For the exact-QCA Dirac propagator

$$
D_{\mathbf k}=\begin{pmatrix} n\,W_{\mathbf k} & im\,I_2 \\ im\,I_2 & n\,W_{\mathbf k}^\dagger\end{pmatrix},
\qquad n=\sqrt{1-m^2},
\tag{5.1}
$$

with $W_{\mathbf k}$ the massless Weyl unitary, a direct eigenvalue computation using the admissibility constraint $n^2+m^2=1$ gives the **spherical-Pythagorean identity**

$$
\boxed{\;\cos\Omega_\text{Dirac}(\mathbf k,m)=\sqrt{1-m^2}\,\cos\omega_\text{kin}(\mathbf k)=\cos\Omega_\text{rest}(m)\,\cos\omega_\text{kin}(\mathbf k)\;}
\tag{5.2}
$$

This is the spherical law of cosines for a right spherical triangle whose two legs are the mass-rotation rate $\Omega_\text{rest}=\arcsin m$ and the kinetic rotation rate $\omega_\text{kin}(\mathbf k)$, and whose hypotenuse is the full Dirac dispersion $\Omega_\text{Dirac}$. Expanding both sides for small angles ($\cos x\approx1-x^2/2$):

$$
\Omega_\text{Dirac}^2 = m^2+\omega_\text{kin}^2 + O(\text{lattice}^4)
\;\xrightarrow[\text{F26}]{\omega_\text{kin}\to c_\text{lat}|\mathbf k|}\;
E^2 = m^2c^4 + p^2c^2 + O(\text{lattice}^4).
\tag{5.3}
$$

**Einstein's relativistic dispersion is the continuum (small-angle) limit of a spherical-Pythagorean identity on the lattice.** It is not an axiom but a geometric theorem about how two rotation rates — one for propagation, one for rest mass — combine on the quantum clock $S^1$, flattening to Euclidean Pythagoras only as $a\to0$. The first lattice deviation is $\Omega^2-m^2-\omega_\text{kin}^2=-\tfrac1{12}(m^4+\omega_\text{kin}^4-6m^2\omega_\text{kin}^2)+\cdots$, confirmed by a measured continuum-limit log-log slope of $4.0055$ (target $4$).

The identity holds on both the 2D-square and 3D-BCC lattices and for both helicity branches; the two limits $m=0$ (photon, $\Omega_\text{Dirac}=\omega_\text{kin}$) and $\mathbf k=0$ (rest, $\Omega_\text{Dirac}=\arcsin m$) are recovered exactly (residual $\le2.2\times10^{-16}$). The spherical-Pythagorean shell is Finding F46.

### 5.1 The mass rotation (preview of Paper III)

The mass step replaces the scalar Dirac coupling $im$ with a local complex phase $im\,e^{i\theta(\mathbf x)}$, which is unitarily equivalent to gauging the $\beta$-matrix, $\beta_g=\cos\theta\,\sigma_1+\sin\theta\,\sigma_2$. Promoting $\theta(\mathbf x)$ and its $SU(2)$ generalisation $U(\mathbf x)$ to local fields makes the mass coupling carry an exact chiral $SU(2)_L$ gauge symmetry — the weak isospin group — *without any Higgs scalar*. The field $U(\mathbf x)$ plays the role of the Higgs vacuum direction but is pure gauge. This is the foundation of Papers III (mass) and VI (weak force).

---

## 6. Verification summary

Every structural identity in this paper is algebraic and was checked numerically. Representative residuals:

| Result | Section | Residual / status |
|---|---|---|
| Exact discrete-time rotation (3.1) | §3 | $2.0\times10^{-16}$ |
| Light-cone slope $\omega/k\to1/\sqrt3$ | §2.2 | $0.57735027$ vs $0.57735027$ |
| Maxwell curl residual at $k=0.05$ | §4.2 | $2.0\times10^{-2}$ (the linearisation error) |
| Energy conservation over 200 ticks | §4.4(a) | $4.8\times10^{-14}$ |
| Curl residual coefficient $=c_\text{lat}/\sqrt2$ | §4.4(b) | geometry-independent, exact |
| Spherical-Pythagorean identity (5.2), 2D + BCC | §5 | $3.3\times10^{-16}$ |
| Continuum-limit slope (Einstein limit) | §5 | $4.0055$ (target $4$) |
| Rest limit $\Omega_\text{Dirac}(0,m)=\arcsin m$ | §5 | $\le2.2\times10^{-16}$ |

The findings underlying these results are F25 (exact rotation), F26 (light as rotation rate), F37 (chirality branches), and F46 (spherical-Pythagorean mass).

---

## 7. Discussion: what is derived and what is posited

**Derived from the substrate.** The free dynamics (the BCC Weyl walk) follow from the QCA uniqueness theorem; the value $c_\text{lat}=1/\sqrt3$ follows from the rotation algebra; Maxwell's equations, the imaginary unit, geometric energy conservation and the Einstein mass shell all follow from the exact rotation and its spherical composition with the mass rotation.

**Posited / open.** The identification of the lattice with physical space picks a preferred frame; ordinary Lorentz invariance is recovered only in the small-$k$ limit, with a deformed (doubly-special-relativistic) covariance available at finite $k$ (Findings F22, F24). The continuum limit $a\to0$ (renormalisation) is the field-wide open problem and is not solved here. The SI-unit identification that fixes $a$ and $\tau$ is deferred to Paper VII, where it is pinned without free parameters to $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.5978\,\ell_P=1.0664\times10^{-34}$ m.

These caveats are honest limits of a research programme, not defects of the substrate: the point of Paper I is that an enormous amount of standard kinematics is *forced* once the BCC QCA and the rotation interpretation are adopted.

---

## 8. Relation to the rest of the series

- **Paper II (Photon)** builds the $(\mathbf E,\mathbf B)$ pair of §3 from two lattice quanta and shows the physical photon is their bound, non-birefringent pair.
- **Paper III (Mass)** develops the chiral-$SU(2)$ mass rotation of §5.1 into a complete Higgs-free mass mechanism and the Koide relation.
- **Papers IV–VII** gauge the substrate into electromagnetism, the strong and weak forces, and gravity (the last as a position-dependent renormalisation of the rotation rate of §4, extended to the full-tensor strong field — exact Schwarzschild/Kerr — per F178).
- **Papers VIII–X** populate the lattice with the fermion, lepton and baryon content, with the generation count fixed by the $O_h$ representation theory introduced in §2.1.

---

## References

1. A. Bisio, G. M. D'Ariano, P. Perinotti, A. Tosini, "Free Quantum Field Theory from Quantum Cellular Automata," *Found. Phys.* **45**, 1137 (2015); and "Weyl, Dirac and Maxwell quantum cellular automata," *Ann. Phys.* (2015).
2. G. M. D'Ariano, P. Perinotti, "Derivation of the Dirac equation from principles of information processing," *Phys. Rev. A* **90**, 062106 (2014).
3. K. Zuse, *Rechnender Raum* (Vieweg, 1969); English: *Calculating Space*.
4. E. Fredkin, "Digital mechanics," *Physica D* **45**, 254 (1990).
5. G. 't Hooft, *The Cellular Automaton Interpretation of Quantum Mechanics* (Springer, 2016).
6. L. de Broglie, *Une nouvelle conception de la lumière* (1934) — neutrino theory of light.
7. M. Ludwig, *Physics Notes* (unpublished notebook, 2007): "Complex mass"; helical-motion mass construction (pp. 73–74).
8. Project findings: F25 (exact discrete-time Maxwell rotation), F26 (speed of light as rotation rate), F37 (Riemann–Silberstein/BCC chirality), F46 (spherical-Pythagorean lattice mass).

*Companion papers: II (photon), III (mass), IV–VII (interactions), VIII (black hole), IX–XI (matter sectors).*
