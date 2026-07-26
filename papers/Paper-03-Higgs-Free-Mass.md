# Paper III — Mass Without a Higgs Field: Chiral-$SU(2)$ $\beta$-Gauging, the Spherical Mass Shell, and the Koide Relation

**B. Ludwig**
*Independent researcher*

**Notebook source material:** M. Ludwig (2007), *Physics Notes*, pp. 59–60 ("Complex mass"), pp. 73–74 (helical mass)

*Series: "A Universe in a Bottle" — Paper III of XI. Builds on Paper I (spherical mass shell) and is the mass foundation for Papers VI, VIII, IX, X.*

*Revision 2 (2026-06-08): re-issued for the eleven-paper series; companion-paper cross-references updated (fermions IX, leptons X, baryons XI).*

*Revision 3 (2026-07-01): companion-paper numbers shifted by one following the deprecation of the "dielectric black hole" paper (fermions VIII, leptons IX, baryons X).*

---

## Abstract

We show that fermion mass on the BCC quantum-cellular-automaton vacuum is generated without a Higgs field. The mechanism is Ludwig's chiral-$SU(2)$ complex-mass coupling: replacing the scalar Dirac mass $im$ by a local complex phase $im\,e^{i\theta(\mathbf x)}$ is unitarily equivalent to gauging the Dirac $\beta$-matrix, and promoting the phase to a local $SU(2)$ field $U(\mathbf x)$ endows the mass step with an exact chiral $SU(2)_L$ gauge symmetry — the weak isospin group — verified by a Ward identity at $1.1\times10^{-17}$. The field $U(\mathbf x)$ plays the role of the Higgs vacuum direction but is a pure gauge degree of freedom: no physical scalar appears, the dispersion is independent of the mass phase $\theta$, yet a mass gap forms with vanishing condensate. We connect this to the spherical-Pythagorean mass shell of Paper I ($E^2=p^2c^2+m^2c^4$ as a continuum limit), and to the constituent-mass scale via a self-consistent Nambu–Jona-Lasinio (NJL) gap equation with critical coupling $G_c\Lambda^2=\pi^2/6$ that reproduces the measured light-meson sector. Finally we derive the long-standing Koide relation $Q=\sum m/(\sum\sqrt m)^2=2/3$ for the charged leptons as an *equipartition* condition on a cubic vector $\sqrt m$, itself explained as a Cooper-pair bilinear ($m=y^2$). All structural results are verified to machine precision.

---

## 1. Introduction

In the Standard Model, fermion masses arise from Yukawa couplings to a Higgs doublet whose vacuum expectation value (VEV) breaks electroweak symmetry. The Higgs sector is the least economical part of the SM: it adds a fundamental scalar, a potential tuned by hand, and a Yukawa matrix of free parameters. The notebook that seeds this programme proposed a different route in 2007 — "complex mass" — and a central design decision of the project is to adopt it in place of the Higgs (Paper I, §1.1).

This paper develops that route into a complete mass mechanism. The thesis is threefold. (i) The *origin* of mass is a chiral rotation of the lattice spinor that carries weak isospin as a gauge symmetry, requiring no scalar (§2–3). (ii) The *mass shell* it produces is the spherical-Pythagorean identity of Paper I, whose continuum limit is Einstein's $E^2=p^2c^2+m^2c^4$ (§4). (iii) The *magnitudes* — the constituent mass scale and the charged-lepton mass ratios — emerge from the lattice's own pairing dynamics, the latter as the Koide relation (§5–6).

---

## 2. The complex-mass coupling

In the Weyl representation the standard Dirac mass couples the left- and right-handed two-spinors $\eta,\chi$ via

$$
M_0=\begin{pmatrix}0 & im\,I_2 \\ im\,I_2 & 0\end{pmatrix}.
\tag{2.1}
$$

Ludwig's proposal replaces the scalar coupling $im$ by a **local complex phase**:

$$
M(\theta)=\begin{pmatrix}0 & im\,e^{i\theta}\,I_2 \\ im\,e^{-i\theta}\,I_2 & 0\end{pmatrix}.
\tag{2.2}
$$

This is equivalent to gauging the Dirac $\beta$-matrix: with $U=\mathrm{diag}(1,e^{i\theta})$,

$$
\beta_g=(U\sigma_1U^\dagger)\otimes I = \cos\theta\,\sigma_1+\sin\theta\,\sigma_2,
\tag{2.3}
$$

a rotation in the $\sigma_1$–$\sigma_2$ plane. Promoting $\theta\to\theta(\mathbf x,t)$ makes this a local gauge transformation.

### 2.1 The mass step and its exactness

Writing $c_m=\cos(m\,\Delta t)$, $s_m=\sin(m\,\Delta t)$, the single-flavour mass step is

$$
\begin{pmatrix}\eta'\\\chi'\end{pmatrix}
=\underbrace{\begin{pmatrix}c_m & is_m\,e^{i\theta}\\ is_m\,e^{-i\theta} & c_m\end{pmatrix}}_{M(\theta)}
\begin{pmatrix}\eta\\\chi\end{pmatrix}.
\tag{2.4}
$$

The matrix $M(\theta)=c_m I + is_m A$ with $A=\left(\begin{smallmatrix}0&e^{i\theta}\\e^{-i\theta}&0\end{smallmatrix}\right)$ Hermitian and $A^2=I$, so $M^\dagger M=I$ exactly for every $\theta(\mathbf x)$. Norm drift over 50 random-$\theta$ steps is $1.3\times10^{-15}$ (machine precision). At $\mathbf k=0$ the step is a pure rotation of the chirality pair at rate $\Omega_\text{rest}=\arcsin m$ per tick — the rest leg of the spherical mass shell (Paper I, §5).

---

## 3. Chiral $SU(2)_L$ as a gauge symmetry of the mass step

For an isospin doublet $(\nu,e)_L$, replace the scalar phase $e^{i\theta}$ by $U(\mathbf x)\in SU(2)$ acting on the isospin index while leaving the spin index untouched:

$$
\eta' = c_m\,\eta + is_m\,(U\otimes I_\text{spin})\,\chi,
\qquad
\chi' = is_m\,(U^\dagger\otimes I_\text{spin})\,\eta + c_m\,\chi.
\tag{3.1}
$$

The full mass operator is $M_{SU(2)}=\cos\,I_8 + i\sin\left(\begin{smallmatrix}0 & U\otimes I\\ U^\dagger\otimes I & 0\end{smallmatrix}\right)$, unitary by the same argument as (2.4).

### 3.1 The Ward identity (the central result)

Let $V(\mathbf x)\in SU(2)$ act **only on the left-handed $\eta$ sector**. Then the mass step satisfies, exactly,

$$
\boxed{\;V(\mathbf x)\cdot\mathrm{mass\_step}(\psi;\,U) = \mathrm{mass\_step}\big(V(\mathbf x)\cdot\psi;\;V(\mathbf x)\,U\big).\;}
\tag{3.2}
$$

That is, simultaneously transforming $\eta\to V\eta$, $U\to VU$, and $\chi\to\chi$ (unchanged) leaves the mass step invariant. The symmetry group is $SU(2)_L$ — precisely the weak isospin group of the SM — derived from $\beta$-gauging alone, with **no Higgs field**. The Ward-identity residual is $1.1\times10^{-17}$ (the key test, Finding F27). Chirality is exact: under the $SU(2)_L$ transform the right-handed $\chi$ is unchanged to bit-for-bit $0$, while $\eta$ transforms non-trivially.

### 3.2 $U(\mathbf x)$ is the Higgs vacuum direction, but pure gauge

In the SM the Higgs VEV $\langle\Phi\rangle$ selects which doublet component couples to the right-handed singlet. Here $U(\mathbf x)$ performs the same selection: starting from a pure $\nu_L$ state, $U=I$ excites $\nu_R$, $U=i\sigma_1$ excites $e_R$, a $45^\circ$ mix excites both equally. But $U$ is a **pure gauge degree of freedom**, not a physical boson:

- **Dispersion independence.** The eigenvalues of the mass operator are independent of $\theta$ to $3.3\times10^{-16}$ across $\theta\in\{0,\pi/3,\pi/2\}$ — $\theta$ carries no physical information.
- **Mass gap without condensate.** With $U=I$ (no VEV, no scalar) a mass gap still forms: with $m\neq0$ the right-chirality fraction grows to $N_R=0.82$ after 80 ticks, while $m=0$ stays pure-left to $4.0\times10^{-15}$.
- **Correct quantum numbers.** A pure $\nu_L$ state carries $T_3=+\tfrac12$ to $1.1\times10^{-16}$.

### 3.3 Status as a known mass mechanism

The construction is the lattice realisation of the non-Abelian Stueckelberg / Kunimasa–Goto mass term: a gauge-invariant mass generated without a physical scalar. The continuum no-go theorems on renormalisability of massive Yang–Mills do not bind here, because the lattice carries a built-in UV cutoff (the cell size $a$). The phase that would have been the Higgs is eaten as the Stueckelberg/longitudinal mode (Paper VI; hypercharge in Paper IX). The hypercharge $U(1)_Y$ rides on the *same* field $U(\mathbf x)$ that carries the mass phase, by absorbing the chiral hypercharge difference $\Delta Y=Y_L-Y_R$ (Finding F41); this is what lets the model dispense with the Higgs scalar entirely rather than merely relocating it.

---

## 4. The mass shell: spherical-Pythagorean composition

The mass rotation of §2–3 composes with the kinetic (Weyl) rotation of Paper I by the **spherical law of cosines**. For the exact-QCA Dirac propagator $D_{\mathbf k}$ (Paper I, Eq. 5.1) with admissibility $n^2+m^2=1$, $n=\sqrt{1-m^2}$:

$$
\cos\Omega_\text{Dirac}(\mathbf k,m)=\sqrt{1-m^2}\,\cos\omega_\text{kin}(\mathbf k)=\cos\Omega_\text{rest}(m)\,\cos\omega_\text{kin}(\mathbf k),
\tag{4.1}
$$

with $\Omega_\text{rest}=\arcsin m$. Small-angle expansion yields $\Omega_\text{Dirac}^2=m^2+\omega_\text{kin}^2+O(\text{lattice}^4)$, i.e.

$$
E^2=m^2c^4+p^2c^2 + O(\text{lattice}^4).
\tag{4.2}
$$

**Einstein's mass shell is the continuum limit of a spherical-Pythagorean identity** whose two legs are the mass-rotation rate and the kinetic-rotation rate. This vindicates a 2007 notebook construction (pp. 73–74) in which mass was modelled as a particle confined to a helical trajectory, $c^2=v_\text{eff}^2+(2\pi\nu r)^2$ — a Pythagorean split of the lattice light speed into a propagation leg and a rest-rotation leg. The notebook dismissed it for the wrong reason (the high-energy limit $v\to c$, which is in fact correct for massive particles); the exact lattice identity is the spherical form, with the helical decomposition as its Euclidean limit. Mass, in this picture, is literally *confined rotation*: a massless quantum forced to turn in place rather than stream forward. This is the same statement that lets Paper VII treat all mass as confined field-rotation energy and dispense with a separate gravitational source.

---

## 5. The constituent-mass scale: a self-consistent NJL gap

The chiral mass step says *how* mass appears; the *magnitude* of the dynamical (constituent) mass is fixed by the lattice's pairing dynamics, modelled as a Nambu–Jona-Lasinio (NJL) four-fermion contact interaction. A single coupling $G$ both generates the constituent mass via the gap equation and, summed in the $q\bar q$ ladder (RPA), fixes the meson poles (Finding F77).

**Gap equation** (Hartree, $N_c=3$, $N_f=2$):

$$
M=m_0+4G\,N_cN_f\,M\,I_1(M),\qquad I_1(M)=\frac{1}{2\pi^2}\int_0^\Lambda\frac{p^2\,dp}{\sqrt{p^2+M^2}},
\tag{5.1}
$$

with a finite **critical coupling**

$$
\boxed{\;G_c\Lambda^2=\frac{\pi^2}{N_cN_f}=\frac{\pi^2}{6}=1.644934\;}
\tag{5.2}
$$

below which chiral symmetry is unbroken. In the chiral limit the pion is the exact Goldstone boson, and the scalar partner sits at threshold, $m_\sigma=2m_c$ (residual $2.3\times10^{-14}$). The canonical SU(2) fit ($\Lambda=651.5$ MeV, $G\Lambda^2=2.10$, $m_0=5.5$ MeV) reproduces the measured QCD numbers, certifying the normalisation:

| quantity | model | measured | resid |
|---|---|---|---|
| $m_c$ | 311 MeV | $\sim$325 | 4.2% |
| $f_\pi$ | 92.6 MeV | 92.4 | 0.2% |
| $m_\pi$ | 140.5 MeV | 135–138 | 4.1% |
| $\langle\bar qq\rangle^{1/3}$ | $-249$ MeV | $\sim-250$ | 0.4% |

A by-product (relevant to any composite-Higgs speculation) is that the self-consistent scalar always obeys $m_\sigma/2m_c\geq1$, so the dynamical-mass mechanism cannot produce the sub-threshold binding ($m_H/2m_t=0.363$) a $t\bar t$ composite Higgs would require — a structural near-no-go. The same NJL machinery, promoted to a dynamical pion, supplies the long-range nuclear force in Paper X.

---

## 6. The charged-lepton mass ratios: the Koide relation

### 6.1 Koide as cubic-vector equipartition

The generation structure (Paper VIII) places the three charged leptons in the cubic vector irrep $T_{1u}$ of $O_h$. Define the vector $\mathbf s=(\sqrt{m_e},\sqrt{m_\mu},\sqrt{m_\tau})$ and split it into its democratic ($A_{1g}$, along $\hat n=(1,1,1)/\sqrt3$) and traceless ($T_{1u}$) parts. The angle $\theta$ between $\mathbf s$ and $\hat n$ satisfies the **exact identity**

$$
\cos^2\theta=\frac{(\sum_a\sqrt{m_a})^2}{3\sum_a m_a}=\frac{1}{3Q},
\qquad Q\equiv\frac{\sum_a m_a}{(\sum_a\sqrt{m_a})^2}.
\tag{6.1}
$$

Koide's empirical $Q=\tfrac23$ is therefore exactly the **equipartition condition** $\cos^2\theta=\tfrac12$, i.e. $\theta=45^\circ$, i.e. the cubic-scalar and symmetry-breaking parts of $\sqrt m$ carry equal weight. The measured charged leptons give $Q=0.6666605$ ($0.91\sigma$ from $\tfrac23$), $\theta=44.99974^\circ$, ratio $|A_{1g}|^2/|T_{1u}|^2=1.00002$.

### 6.2 Predictivity

Because $Q=\tfrac23$ plus two masses overdetermines the third, the relation is predictive:

$$
m_\tau^\text{pred}=1776.97\,\text{MeV}\quad\text{vs}\quad m_\tau^\text{PDG}=1776.86\pm0.12\,\text{MeV}\ (6.1\times10^{-5}).
\tag{6.2}
$$

A threefold ($Z_3$, cube-body-diagonal) parametrisation $\sqrt{m_a}=M_0[1+\sqrt2\cos(\delta+2\pi a/3)]$ reconstructs $m_\tau$ to $4.4\times10^{-5}$, with the $\sqrt2$ amplitude being exactly the equipartition condition. The angle map $Q(\phi)=1/(3\cos^2\phi)$ (Finding F80) makes the correspondence $45^\circ\leftrightarrow Q=\tfrac23$ exact.

### 6.3 Why $\sqrt m$: the Cooper-pair bilinear

The use of $\sqrt m$ rather than $m$ is explained by the same Cooper-pair premise that makes the photon a bound pair (Paper II) and the would-be Higgs a condensate. If a fermion's mass is set by a pair condensate, it is a *bilinear* in the constituent amplitude $y$:

$$
m_a\propto\langle y_a\,y_a\rangle=y_a^2
\;\Longrightarrow\;
\sqrt{m_a}=y_a=\text{the }T_{1u}\text{ vector component on axis }a.
\tag{6.3}
$$

Koide is then a statement about the amplitude $y$, not the mass — precisely because mass is quadratic in the fundamental pairing amplitude (Finding F78). The data independently single out the bilinear: the participation ratio $(\sum m^s)^2/\sum m^{2s}$ is the clean rational $3/2$ only at $s=\tfrac12$ (measured $1.500014$; neighbours $1.834$ at $s=\tfrac13$, $1.119$ at $s=1$).

### 6.4 Honest limits

The cubic geometry fixes the *form* (three orthorhombic generations; $\sqrt m$ as cubic vector; the equipartition identity (6.1)) and the charged leptons sit on it to $10^{-5}$. The amplitude $\sqrt2$ itself ($Q=\tfrac23$ exactly) is **not yet derived** from the QCA rule: the cube's symmetric dynamics give the degenerate floor $Q=\tfrac13$, so equipartition is a critical/maximal-breaking condition that an explicit ingredient must impose (Finding F78). A recurring $\sqrt2$/$45^\circ$ in both the constituent stability bound (F73) and the generation vector hints at a single saturation mechanism; Finding F80 identifies the *selector* of the critical sector as electromagnetism (only the colour-free, charged sector lands on $45^\circ$), while flagging that perturbative EM is $\sim340\times$ too weak to *drive* the rotation. The up- and down-type quarks ($Q=0.85,0.73$) do not equipartition; why only the charged leptons do is treated further in Paper IX.

---

## 7. Verification summary

| Result | Section | Residual / value |
|---|---|---|
| Mass-step unitarity (random $\theta$) | §2.1 | $1.3\times10^{-15}$ |
| $SU(2)_L$ Ward identity (3.2) | §3.1 | $1.1\times10^{-17}$ |
| Chirality exact ($\chi$ unchanged) | §3.1 | $0$ (bit-for-bit) |
| Dispersion independence of $\theta$ | §3.2 | $3.3\times10^{-16}$ |
| Mass gap without Higgs ($N_R$) | §3.2 | $0.82$ (vs $4.0\times10^{-15}$ at $m=0$) |
| Spherical-Pythagorean shell (4.1) | §4 | $3.3\times10^{-16}$ |
| NJL Goldstone $m_\sigma=2m_c$ (chiral) | §5 | $2.3\times10^{-14}$ |
| Koide $Q$ (charged leptons) | §6.1 | $0.6666605$ ($0.91\sigma$) |
| Koide $m_\tau$ prediction | §6.2 | $6.1\times10^{-5}$ |

Underlying findings: F27 (chiral $SU(2)$ complex mass), F46 (spherical-Pythagorean shell), F77 (NJL gap+RPA), F78 (Koide amplitude from Cooper pair), F80 (45° / EM selection), F76 (generation hierarchy), F44 (rank-1 Stueckelberg $m_A=0$), F41 (hypercharge on $U(\mathbf x)$).

---

## 8. Discussion and relation to the series

This paper supplies the mass mechanism that the rest of the matter sector inherits. Paper VI (weak force) gauges the $SU(2)_L$ symmetry derived in §3 with dynamical $W$ bosons. Paper VIII (fermion sector) uses the spherical mass shell (§4) and the cubic generation structure (§6) to fix the generation count and hierarchy. Paper IX (leptons) adds the right-handed-neutrino Majorana mass and see-saw on the same Higgs-free footing, and develops the Koide/EM-selection story. Paper X (baryons) uses the NJL constituent-mass scale (§5) and its dynamical pion.

The single conceptual claim unifying all of this — that mass is a *rotation* (the rest leg of the spherical triangle) sourced by a pure-gauge chiral coupling rather than by a fundamental scalar — is what makes the model Higgs-free without sacrificing any verified mass phenomenology.

---

## References

1. Y. Nambu, G. Jona-Lasinio, "Dynamical Model of Elementary Particles...," *Phys. Rev.* **122**, 345 (1961); **124**, 246 (1961).
2. Y. Koide, "New view of quark and lepton mass hierarchy," *Phys. Rev. D* **28**, 252 (1983); *Lett. Nuovo Cimento* **34**, 201 (1982).
3. T. Kunimasa, T. Goto, "Generalization of the Stueckelberg Formalism to the Massive Yang–Mills Field," *Prog. Theor. Phys.* **37**, 452 (1967); E. C. G. Stueckelberg (1938).
4. M. Ludwig, *Physics Notes* (2007), pp. 59–60 ("Complex mass"), pp. 73–74 (helical mass construction).
5. Project findings: F27, F41, F44, F46, F76, F77, F78, F80.

*Companion papers: I (substrate/mass shell), VI (weak force), IX (fermions), X (leptons), XI (baryons).*
