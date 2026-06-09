# Paper IX — The Fermion Sector: Weyl Quanta, Chirality and Helicity, Exactly Three Generations, and the Anomaly-Free First Generation

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper IX of XI. Builds on Papers I (Weyl walk, spherical mass), III (mass / Koide), and VI (weak isospin); the generation theorem here feeds the Newton-constant mode count of Paper VII. Specialised to leptons in Paper X and to baryons in Paper XI.*

*Revision 2 (2026-06-08): re-issued as Paper IX of the eleven-paper series (was Paper VIII). Lepton-specific Koide/EM-selection and Majorana detail are now deferred to Paper X; baryon-specific colour structure to Paper XI. This paper carries the generic fermion structure common to all matter.*

---

## Abstract

We assemble the fermion sector of the BCC quantum-cellular-automaton model. The fundamental matter field is the two-component Weyl spinor of the lattice walk; a massive Dirac fermion is the pairing of two opposite-chirality Weyl quanta through the chiral mass step of Paper III. We establish the exact correspondence between the two BCC dispersion branches and the two physical helicities (Riemann–Silberstein eigenstates), the chirality-exactness of the mass step, and the spherical-Pythagorean dispersion that yields $E^2=p^2c^2+m^2c^4$ in the continuum. The central structural result is that the vacuum's point group $O_h$ admits a maximal single-valued irreducible representation of dimension **three** — the odd-parity vector triplet $T_{1u}$ — and the chiral scalar mass selects exactly that triplet from the nearest-neighbour shell, so the model contains **exactly three fermion generations and forbids a fourth**. The generation hierarchy is an orthorhombic ("crystal-field") splitting of $T_{1u}$ into three axes, with the charged-lepton Koide relation $Q=\tfrac23$ as its equipartition signature (developed in Paper X). The first generation is anomaly-free: all six gauge and gravitational anomaly traces vanish as exact rationals. Per-species $C$, $P$, $CP$ and CPT are verified.

---

## 1. Introduction

The matter content of the Standard Model is a triplication of one generation of spin-$\tfrac12$ fermions — leptons and quarks — with identical gauge quantum numbers and a steep mass hierarchy. Two facts are inputs in the SM and outputs here: *why spin-$\tfrac12$ Weyl/Dirac fields*, and *why exactly three generations*.

The first is answered by the substrate: the unique non-trivial $3$D QCA (Paper I) is the Weyl walk, so the fundamental matter field is a two-component spinor by derivation, not assumption. The second is answered by the vacuum's discrete symmetry: the cubic point group $O_h$ caps the protected degeneracy at three. This paper develops both, fixes the first-generation field content and its anomaly freedom, and specifies the chirality/helicity and discrete-symmetry structure that the lepton (X) and baryon (XI) papers inherit.

---

## 2. Weyl quanta, chirality, and helicity

### 2.1 The fundamental field

The lattice carries a two-component complex spinor obeying the free Weyl walk, with dispersion branches $\omega^\pm(\mathbf k)=\arccos(c_xc_yc_z\pm s_xs_ys_z)$ (Paper I, Eq. 2.1). The two branches are the two chiralities. Massless matter "need not be represented as a four-component Dirac field" (in the notebook's words): the natural objects are the decoupled two-spinors $\psi_\pm$ obeying

$$
i\hbar\,\partial_t\psi_+=-i\hbar c\,\boldsymbol\sigma\!\cdot\!\nabla\psi_+,\qquad
i\hbar\,\partial_t\psi_-=+i\hbar c\,\boldsymbol\sigma\!\cdot\!\nabla\psi_-,
\tag{2.1}
$$

interchanged by parity. A massive Dirac fermion is the *pairing* of $\psi_+$ and $\psi_-$ by the chiral mass step (Paper III, §2–3): mass is precisely the coupling that binds the two Weyl quanta into a four-component bispinor. The dynamical (real-time) fermion field with this structure is built and validated in Finding F85.

### 2.2 Chirality–helicity correspondence (exact)

The two physical helicities are the Riemann–Silberstein eigenstates $\mathbf F_\pm=\mathbf E\pm i\mathbf B$ (for the gauge fields) and, equivalently for the matter walk, the two eigenvectors $(1,\mp i)^\mathsf T$ of the one-tick rotation. Reality forces $\mathbf F_+(-\mathbf k)=\mathbf F_-^*(\mathbf k)$, and the BCC branches satisfy $\Omega^+(-\mathbf k)=\Omega^-(\mathbf k)$, so the unique Hermitian-symmetry-preserving assignment is $\mathbf F_+\!\leftrightarrow\!\Omega^+$ (positive helicity, RCP) and $\mathbf F_-\!\leftrightarrow\!\Omega^-$ (negative helicity, LCP). This correspondence is exact (Finding F37/F65) and is the matter-sector basis for the photon construction of Paper II.

### 2.3 The mass shell

Pairing the two chiralities through the mass step gives the spherical-Pythagorean dispersion (Papers I, III)

$$
\cos\Omega_\text{Dirac}=\sqrt{1-m^2}\,\cos\omega_\text{kin}=\cos\Omega_\text{rest}\,\cos\omega_\text{kin},\qquad\Omega_\text{rest}=\arcsin m,
\tag{2.2}
$$

whose continuum limit is $E^2=p^2c^2+m^2c^4$. The mass step is chiral-exact: the $SU(2)_L$ transform acts on $\eta$ (left) only, leaving $\chi$ (right) bit-for-bit unchanged (Paper III, §3.1).

---

## 3. Exactly three generations from the cubic point group

### 3.1 What "a generation" is, group-theoretically

A generation multiplet is a set of fermion states that (i) carry identical gauge quantum numbers, (ii) are related by an exact symmetry of the vacuum (so they are forced degenerate and mutually equivalent), and (iii) are mutually independent. Conditions (ii)+(iii) state that the multiplet fills a single **irreducible representation** of the vacuum symmetry group. For the BCC vacuum that group is the cubic point group $O_h$ (order 48).

### 3.2 The cap: $O_h$ has maximal single-valued irrep dimension 3

Built from generators, $O_h$ has 10 conjugacy classes and ten single-valued (tensor) irreps of dimensions $1,1,2,3,3$ in each parity sector; $\sum d^2=2(1+1+4+9+9)=48$ (Burnside — the table is complete), and the character table is orthonormal over the integers. The largest single-valued irrep is **3-dimensional**. By Schur's lemma a symmetry-protected, equivalent, independent multiplet fills one irrep, so it has **at most three** members; a fourth would need a 4-dimensional single-valued irrep, **which $O_h$ does not possess.**

### 3.3 The realisation: the chiral scalar mass selects $T_{1u}$

The mass step couples the anchored chirality to its partner on the eight body-diagonal nearest neighbours. Their permutation representation decomposes exactly as

$$
\Gamma_\text{shell}=A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}\qquad(1+1+3+3=8),
\tag{3.1}
$$

which *contains a triplet*. The Dirac/chiral mass is a **scalar** (required for the clean rest-rotation $\arcsin m$ of (2.2); a pseudoscalar mass would spoil it). A scalar mass links opposite chiralities, which carry opposite spatial parity, so the partner must occupy an odd-parity ($u$) shell orbital. The odd content is $A_{2u}\oplus T_{1u}$; the *only triplet* there is $T_{1u}$. Hence the mass-carrying generation multiplet is **uniquely $T_{1u}$, dimension exactly 3** (Finding F75).

$$
\boxed{\;\text{generations}=\dim T_{1u}=3,\qquad\text{no 4-dim single-valued irrep of }O_h\Rightarrow\text{no fourth.}\;}
\tag{3.2}
$$

A group-averaged random $O_h$-invariant mass operator has eigenvalue degeneracies exactly $[1,1,3,3]$ (commutator $4.4\times10^{-16}$); a forced 4-fold degeneracy fails to commute with $O_h$ (commutator $1.0$) — the fourth is forbidden as a symmetry partner and split off as an independent level. This agrees with the experimental exclusion of a sequential fourth generation ($Z$ invisible width $N_\nu=2.984\pm0.008$), here as a theorem about the vacuum's point group, and it ties the number 3 to the three spatial dimensions through the same vector irrep $T_{1u}\cong(x,y,z)$.

### 3.4 The roles divide cleanly

The **lattice supplies** the triplet (it caps the count at three and physically furnishes a triplet in the shell); the **chiral mass step selects** which triplet (the scalar/opposite-parity rule picks the unique odd $T_{1u}$, collapsing the two shell triplets to one). They compose; neither alone gives three.

---

## 4. The generation mass hierarchy

The three $T_{1u}$ partners are degenerate at the fully symmetric point. Distinct masses require a symmetry-lowering crystal field. Counting distinct eigenvalues of the real-symmetric $3\times3$ mass operator (Finding F76):

| vacuum symmetry | operator | pattern | distinct masses |
|---|---|---|---|
| cubic $O_h$ | $m_0\mathbb 1$ | $[3]$ | 1 |
| tetragonal $D_{4h}$ | $\mathrm{diag}(a,a,b)$ | $[2,1]$ | 2 |
| **orthorhombic $D_{2h}$** | $\mathrm{diag}(a,b,c)$ | $[1,1,1]$ | **3** |

So three non-degenerate generations require breaking to three inequivalent axes, $T_{1u}\to B_{1u}\oplus B_{2u}\oplus B_{3u}$: **the three generations are the three orthorhombic axes** of a triaxially-distorted cubic vacuum (the BCC dispersion's anisotropy, and the orthorhombic $E_g$ vacuum of Finding F93, supply a natural source). A mass-*linear* crystal field is excluded (the splitting exceeds the mean — non-perturbative). The correct variable is $\sqrt m$ (Paper III, §6.3: the Cooper-pair bilinear $m=y^2$), in which the Koide relation $Q=\tfrac23$ is the exact equipartition $|A_{1g}|=|T_{1u}|$ of $\sqrt m$ — verified for charged leptons to $10^{-5}$ and predicting $m_\tau=1776.97$ MeV. The full equipartition story, the $45^\circ$ unification with the bound-pair cap, and the electromagnetic selection rule that explains why only the charged leptons sit at $Q=\tfrac23$ are the subject of Paper X.

---

## 5. The first-generation field content and its anomaly freedom

### 5.1 Content

The anomaly-free, Higgs-free first generation is 16 Weyl fields:

| field | $SU(3)_c$ | $SU(2)_L$ | $U(1)_Y$ | $Q=T_3+Y/2$ |
|---|---|---|---|---|
| $L=(\nu_e,e)_L$ | $\mathbf 1$ | $\mathbf 2$ | $-1$ | $0,-1$ |
| $e_R$ | $\mathbf 1$ | $\mathbf 1$ | $-2$ | $-1$ |
| $Q=(u,d)_L$ | $\mathbf 3$ | $\mathbf 2$ | $+\tfrac13$ | $+\tfrac23,-\tfrac13$ |
| $u_R$ | $\mathbf 3$ | $\mathbf 1$ | $+\tfrac43$ | $+\tfrac23$ |
| $d_R$ | $\mathbf 3$ | $\mathbf 1$ | $-\tfrac23$ | $-\tfrac13$ |
| $\nu_R$ | $\mathbf 1$ | $\mathbf 1$ | $0$ | $0$ |

This count $L{=}2,e_R{=}1,Q{=}6,u_R{=}3,d_R{=}3,\nu_R{=}1=16$ Weyl fields per generation is the mode count $g_*=16\times3=48$ that fixes Newton's constant (Paper VII, §5.3). Mass is via the chiral step everywhere (no Higgs–Yukawa anywhere); the right-handed singlets are dynamical $U(1)_Y$-coupled fields via a Stueckelberg-wrapped kinetic step (Finding F42), with hypercharge carried on the mass gauge field $U(\mathbf x)$ (Finding F41).

### 5.2 Anomaly cancellation (exact)

All six gauge + gravitational anomaly traces of the generation vanish as exact rationals (Finding F38):

$$
\sum Y=0,\quad \sum Y^3=6-6=0,\quad [SU(2)_L]^2Y=-\tfrac12+\tfrac12=0,\quad [SU(3)_c]^2Y=\tfrac13-\tfrac23+\tfrac13=0,
$$
$$
[SU(3)_c]^3=2-1-1=0,\quad [SU(2)_L]^3=0\ (\text{pseudo-real}),
\tag{5.1}
$$

and $Q=T_3+Y/2$ is reproduced exactly per particle. The charge assignments are therefore not free inputs but are forced by quantum consistency.

### 5.3 Discrete symmetries

Per-species $C$, $P$, $CP$ and CPT are verified (Finding F53): the antiparticle table negates $(T_3,Q,Y)$ with Gell-Mann–Nishijima exact for both; $C$ and $P$ are maximally violated by the left-only charged current ($A_C=A_P=1$); $CP$ is conserved with the single-generation Jarlskog invariant $N(1)=0$ (no physical CP phase), and the chiral mass phase $\theta$ is confirmed pure gauge; CPT per species reproduces to $0$.

---

## 6. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| Chirality–helicity (RS ↔ branch) | §2.2 | exact algebraic |
| Spherical mass shell | §2.3 | $3.3\times10^{-16}$ |
| Chirality-exact mass step | §2.3 | $0$ (bit-for-bit) |
| $O_h$ max single-valued irrep $=3$ | §3.2 | exact ($\sum d^2=48$) |
| Shell decomposition $\to T_{1u}$ | §3.3 | exact rationals |
| Schur degeneracies $[1,1,3,3]$; no 4-fold | §3.3 | $4.4\times10^{-16}$; comm. $1.0$ |
| Orthorhombic split $\to[1,1,1]$ | §4 | exact |
| Koide $Q=\tfrac23$ (charged leptons) | §4 | $0.91\sigma$; $m_\tau$ to $6\times10^{-5}$ |
| Six anomaly traces | §5.2 | exactly $0$ (rationals) |
| $C/P/CP$/CPT per species | §5.3 | exact / bit-for-bit |

Underlying findings: F37 (chirality/helicity), F46 (mass shell), F75 (three generations), F76 (hierarchy), F78/F80 (Koide amplitude / EM selection), F85 (dynamical fermions), F93 (orthorhombic $E_g$ vacuum), F38 (anomaly), F53 ($C$/$CP$).

---

## 7. Discussion

The fermion sector exhibits the model's signature: structure that is an *input* in the SM becomes an *output* of the lattice. Spin-$\tfrac12$ matter is forced by the QCA uniqueness theorem; the generation count is a theorem about the vacuum's point group; the anomaly-free charge assignment is the unique consistent one; and the generation hierarchy is a crystal-field splitting whose charged-lepton signature is the Koide relation.

The honest limits: the *physical identification* "generation index = orbital irrep of the nearest-neighbour shell" is a well-motivated hypothesis, not a theorem derived from the update rule; the mass-hierarchy *amplitude* $\sqrt2$ (the Koide $\tfrac23$) is not yet derived; the quark sector does not equipartition; and a double-group (spinor) subtlety underlies the "no fourth" argument (the family label is taken to factorise from spin). These are sharply stated open problems, not gaps in the verified structure, and they are taken further in Papers X (leptons) and XI (baryons).

---

## References

1. A. Bisio, G. M. D'Ariano, P. Perinotti, A. Tosini (2015) — Weyl walk uniqueness.
2. L. D. Landau, E. M. Lifshitz, *Quantum Mechanics* §93–99; M. Tinkham, *Group Theory and Quantum Mechanics* (1964) — $O_h$ representation theory and crystal-field splitting.
3. Y. Koide (1982, 1983) — charged-lepton mass relation.
4. ALEPH/DELPHI/L3/OPAL, "Precision electroweak measurements on the $Z$ resonance," *Phys. Rep.* **427**, 257 (2006) — $N_\nu=2.984\pm0.008$.
5. Project findings: F37, F38, F46, F53, F75, F76, F78, F80, F85, F93.

*Companion papers: I (Weyl walk), III (mass / Koide), VI (weak isospin), VII ($g_*$), X (leptons), XI (baryons).*
