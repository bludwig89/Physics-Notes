# Appendix A5 — Symbol Glossary

*Collects every "Notation established or extended in this chapter" table from all 26 chapter files
(Chapters 1–25, with 13 split into 13a/13b) into one master glossary, organized by chapter of first
appearance. Within a chapter's block, symbols are grouped Latin / Greek / calligraphic-blackboard /
named objects, alphabetized within each group. Where a later chapter *extends* a symbol another
chapter introduced, both are noted at the earlier chapter's entry with a forward cross-reference, and
no entry is duplicated. A dedicated **Notation collisions** section at the end flags every symbol
used with two (or more) distinct meanings across chapters — the collisions are named explicitly, not
silently resolved by picking one meaning.*

*Build note: this file is written and re-saved incrementally as chapters are read, per the build
plan's instruction to save early and often. Chapters not yet incorporated are listed at the bottom
under "Not yet incorporated" until the pass reaches them.*

## Chapter 1 — Postulates and ontology

**Latin**

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $a$ | Lattice spacing (cell-to-cell distance); $=1$ in lattice-native units. SI value fixed in Ch.17. Extended in Ch.2 §2.3.6 to the concrete value $a=2/\sqrt3$. | Ch.1 §1.2 (P1, P3) |
| $G$ | The Cayley-graph group whose vertices are the lattice sites (abstract, in Ch.1); realized concretely as $\mathbb Z^3$ on BCC in Ch.2. | Ch.1 §1.2 (P3) |
| $H$ | Generator ("Hamiltonian") of $\mathcal U$ via $\mathcal U=e^{-iH}$; formal at Ch.1, made explicit per-sector in later chapters (e.g. Ch.3 §3.2.2, $H(\mathbf k)=\theta(\mathbf k)\hat{\mathbf n}(\mathbf k)\cdot\boldsymbol\sigma$). | Ch.1 §1.2 (P4) |
| $L$ | Finite point-symmetry subgroup acting isotropically on the neighbor set (abstract, Ch.1); realized as $O_h$/$D_{2h}$/$D_{4h}$ in Ch.2 §2.3.7. | Ch.1 §1.2 (P3) |
| $t$ | Discrete time-tick index, $t\in\mathbb Z$. | Ch.1 §1.2 (P1) |
| $U(x)$ | Postulated local $SU(2)$ (chiral) connection field carrying complex mass and hypercharge; distinct from the scalar evolution operator $\mathcal U$. | Ch.1 §1.2 (P6) |
| $\mathbf{x}$ | A lattice-site (cell) index; fixed to $\mathbb Z^3$-on-BCC in Ch.2. | Ch.1 §1.2 (P2, P3) |

**Greek**

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\tau$ | Tick duration; $=1$ in lattice-native units. SI value fixed in Ch.17. | Ch.1 §1.2 (P1) |
| $\sigma^i$ | Pauli matrices; $\sigma^\mu\equiv(\mathbb 1,\vec\sigma)$, $\tilde\sigma^\mu\equiv(\mathbb 1,-\vec\sigma)$. | Ch.1 §1.2 (P5) |
| $\psi(\mathbf x,t)$ | Per-cell primitive field: a two-component complex (Weyl) spinor, $\psi\in\mathbb C^2$. The chapter's beable candidate. | Ch.1 §1.2 (P4, P5) |
| $\Psi$ | Four-component Dirac bispinor (pair of Weyl spinors, once mass is introduced); notational reservation, built in Ch.11. | Ch.1 §1.2 (P5, P6 forward) |

**Calligraphic / named objects**

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\mathcal U$ | One-tick evolution (update) operator: linear, unitary, $\mathcal U=e^{-iH}$. | Ch.1 §1.2 (P4) |
| $\mathbf k$ | Lattice wavenumber (Fourier dual to $\mathbf x$); $\omega(\mathbf k)$ the free dispersion. Detail deferred to Ch.6. | Ch.1 §1.2 (P4, forward) |
| $c_\text{lat}$ | Lattice-native speed of light; a rotation rate, not a phase velocity (reserved here, derived in Ch.6 to $1/\sqrt3$). | Ch.1 §1.2 (forward reservation; derived Ch.6) |
| beable / changeable / superimposable | 't Hooft's ontology vocabulary: an operator diagonal in the privileged ontological basis / one that permutes such states / one that maps an ontological state to a superposition. | Ch.1 §1.3 |

## Chapter 2 — Why 3+1 dimensions, and why this lattice

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $s$ | Per-cell internal (spinor) dimension; $s=2$ is BDPT's minimal Weyl cell (imported, not derived). | Ch.2 §2.1–2.2 |
| $d$ | Number of spatial dimensions; Ch.2's central result is $d=3$ (R2.3). | Ch.2 §2.2 |
| $D$ | Spacetime dimension, $D=d+1$; used in the chirality-parity argument (R2.4). | Ch.2 §2.3.4 |
| $A(\mathbf k)$ | Bloch-space form of the per-tick update $\mathcal U$, free single-particle sector: $A=u\mathbb I-i\boldsymbol\sigma\cdot\tilde{\mathbf n}$. Extended with explicit coefficients in Ch.3 §3.2.1 (R3.1); extended to the massive Dirac doublet $D(\mathbf k)$ in Ch.4 §4.2.5. | Ch.2 §2.2 |
| $u(\mathbf k)$, $\tilde{\mathbf n}(\mathbf k)$ | Scalar and Bloch-vector parts of $A(\mathbf k)$'s Pauli decomposition. | Ch.2 §2.2 |
| $J$ | Jacobian of $\tilde{\mathbf n}$ at $\mathbf k=0$, $J:\mathbb R^d\to\mathbb R^3$; every dimension selector is a statement about $J$. | Ch.2 §2.2 |
| $\Lambda$ | The automaton's own BCC Cayley group (index 4 in $\mathbb Z^3$); realizes Ch.1's abstract $G$. | Ch.2 §2.3.5 |
| $R$ | Laurent ring $\mathbb C[w_1^{\pm1},w_2^{\pm1},w_3^{\pm1}]$ over which local homogeneous operators are represented ("local" $\equiv$ finite Laurent support). | Ch.2 §2.3.5 |
| $\mathcal C$ | Commutant of $A$ inside the local homogeneous unitaries; $\dim_R\mathcal C=2$. | Ch.2 §2.3.5 |
| $a$ | (Extends Ch.1.) BCC conventional cube edge, fixed at $a=2/\sqrt3=2c_\text{lat}$ (dimensionless, lattice-native). | Ch.2 §2.3.6 |
| $O_h$, $D_{2h}$, $D_{4h}$ | Full octahedral point group (order 48, exact symmetry of the BCC neighbor shell) and the two subgroups (orders 8, 16) the propagating dynamics actually realizes exactly. Realizes Ch.1's reserved $L$. | Ch.2 §2.3.7 |
| $N$ | Internal (colour) tensor-factor multiplicity; cost in space/time directions is independent of $N$ (R2.14); forced value ($N=3$) is Ch.13's content. | Ch.2 §2.3.8 |

## Chapter 3 — The update rule

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $M_{\mathbf d}$ | The eight fixed $2\times2$ matrices, one per BCC hop direction $\mathbf d\in\{\pm1\}^3$, summed against neighbor spinors for one tick (R3.2). | Ch.3 §3.2.1 |
| $\theta(\mathbf k)$ | Single-branch rotation angle, $\theta=\arccos u(\mathbf k)$, i.e. $H(\mathbf k)=\theta(\mathbf k)\hat{\mathbf n}(\mathbf k)\cdot\boldsymbol\sigma$ in $\mathcal U(\mathbf k)=e^{-iH(\mathbf k)}$. Rotation-rate reading as $c_\text{lat}$ is Ch.6's result. | Ch.3 §3.2.2 |
| $c(\mathbf x)=c_0+\delta c(\mathbf x)$ | Position-dependent generalization of the free walk's propagation speed, used in the split-step construction for variable-speed media (gravity, Ch.18). | Ch.3 §3.2.6 |
| $W$ | Weyl-symmetric generator of the inhomogeneous half-step, $W=\tfrac12\{\delta c,\boldsymbol\sigma\cdot\nabla\}$, anti-Hermitian by construction (R3.7). | Ch.3 §3.2.6 |

## Chapter 4 — Structural theorems

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\Theta$ | Antiunitary CPT-type operator for the free BCC Dirac walk, $\Theta=M\cdot K$, $M=\Sigma\cdot(\sigma_y\oplus\sigma_y)$; $\Theta^2=-1$ (Kramers). | Ch.4 §4.2.5 |
| $\Theta'$ | SU(2)-gauged-kinetic-sector analogue of $\Theta$, using $\sigma_y\otimes\tau_2$; $\Theta'^2=+1$ (flipped, non-Kramers). | Ch.4 §4.2.7 |
| $\Sigma$ | The $\eta\leftrightarrow\chi$ chirality-block swap; standard Dirac parity matrix $\gamma^0$ in the Weyl basis. | Ch.4 §4.2.5 |
| $\tau_2$ | SU(2) pseudoreality matrix (numerically $\sigma_y$, kept distinct for the isospin factor); $\tau_2U\tau_2^{-1}=U^{*}$ for every $U\in SU(2)$. | Ch.4 §4.2.7 |
| $\Gamma$ | Classical (pre-quantum) phase space of a spin-$s$ system, $\Gamma=S^2$; the level at which Anastopoulos's Postulate 1 is stated, prior to any Hamiltonian. | Ch.4 §4.2.4 |
| Postulate 1 (Anastopoulos) | The belt trick's isolated non-topological content: exchange realizable as a smooth diagonal-$SO(3)$-orbit path on $\Gamma$, composing twice to one $2\pi$ rotation, spin transported via the *same* rotation as the positional exchange. | Ch.4 §4.2.4 |
| $\kappa_{100}(m)$, $\kappa_{110}(m)$ | Exact closed-form correlation-decay rates along BCC (100)/(110) axes for the free massive Dirac field. | Ch.4 §4.2.9 |
| $p_\text{eff}$ | Implied algebraic-prefactor power of the 3-D correlator's asymptotic decay (OLS fit-bias formula); measured $1.489\pm0.039$, matching derived $p=3/2$. | Ch.4 §4.2.9 |
| $D(\mathbf k)$ | Massive BCC Dirac one-tick unitary (branch-$+$/dagger construction), extending $A(\mathbf k)$ to the doubled ($s=4$) cell. | Ch.4 §4.2.5 |

## Chapter 5 — Quantum structure

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $H_\text{int}$ | System–environment/record generator forced by minimal coupling, $\sum_x\hat\alpha(x)\otimes\hat n(x)$ ($U(1)$) or $\sum_x\hat A^a(x)\otimes\hat J^a(x)$ (non-Abelian). | Ch.5 §5.2.1, §5.2.8 |
| $\hat J^a(x)$ | Site-local non-Abelian current, $\psi^\dagger(x)T^a\psi(x)$; exact intra-site algebra $[\hat J^a(x),\hat J^b(y)]=i\delta_{xy}f^{abc}\hat J^c(x)$. | Ch.5 §5.2.8 |
| $R_b$ | Model's exact block-average (renormalization) operator (F130/F133); coherence eigenvalue $\lambda_\text{coh}(k,b)=\lvert D_b(k)\rvert^2$ is the classicality result. | Ch.5 §5.2.10 |
| $D_b(k)$ | Dirichlet kernel, $\tfrac1b\sum_{j=0}^{b-1}e^{ikj}$, whose squared modulus is $\lambda_\text{coh}$. **Collision note**: same letter $D$ as the massive Dirac unitary $D(\mathbf k)$ of Ch.4 — see Notation collisions. | Ch.5 §5.2.10 |
| $b_k$ | Eigenvalue of the frame-condition averaging operator $B$ on the $k$-th isotypic component of $L^2(\mathbb{CP}^{d-1})$; $b_k=(-1)^k/\binom{k+d-2}{k}$. | Ch.5 §5.2.7 |
| $V$ | Internal (gauge) Hilbert-space factor carrying a unitary irrep of $G$ ($\mathbb C^2$ for $SU(2)_L$, $\mathbb C^3$ for $SU(3)_c$), distinct from the pointer factor $\mathcal H_p$. **Collision note**: same letter $V$ as Ch.2's second dispersive flow $V=\mathbb I\otimes A$ (R2.8) — unrelated objects; see Notation collisions. | Ch.5 §5.2.8 |

## Chapter 6 — Free propagation and the light cone

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $c_\text{lat}$ | (Extends Ch.1 reservation.) The lattice speed of light, $c_\text{lat}=d\Omega/d\lvert\mathbf k\rvert\rvert_0=1/\sqrt3$ in lattice-native units — a rotation rate of the real $(\mathbf E,\mathbf B)$ pair, not a phase velocity. | Ch.6 §6.2.3 |
| $\Omega(\mathbf k)$, $\Omega_\text{even}(\mathbf k)$ | Rotation angle of the real bilinear pair per tick, $\Omega=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$; even under $\mathbf k\to-\mathbf k$ (R6.12). | Ch.6 §6.2.3 |
| $\hat{\mathbf n}(\mathbf k)$ | The BCC spin axis: Bloch vector of the positive-helicity eigenmode of $A(\mathbf k)$, closed form R6.8. | Ch.6 §6.2.5 |
| $\Omega_\text{rest}(m)$, $\Omega_\text{Dirac}(\mathbf k,m)$ | Mass-step rotation angle $\arcsin m$ and full Dirac dispersion, related by the spherical Pythagorean identity R6.10. | Ch.6 §6.2.6 |
| $\Theta$ | **Collision**: here, the dimensionless lattice temperature $\Theta=k_BT\tau/\hbar$ (§6.7 only). Distinct from Ch.4's antiunitary CPT operator $\Theta$ — see Notation collisions. | Ch.6 §6.7 |

## Chapter 7 — Relativity on a lattice

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $K_i$ | Minimal boost generator, $K_i=\tfrac1{2c^2}\{x_i,\Omega\}$, $x_i=i\partial_{k_i}$ on the BZ torus. | Ch.7 §7.2.2 |
| $\Phi(\mathbf k)$ | Off-shell invariant mass, $\Phi=(\Omega^2-c_\text{lat}^2\lvert\mathbf k\rvert^2)/2c_\text{lat}^2$; single scalar whose gradient is the entire finite-$a$ Poincaré defect. | Ch.7 §7.2.2 |
| $D_i(\mathbf k)$ | The Poincaré defect, $D_i=\partial_i\Phi$; zero to all orders on cubic axes, $O(k^3)$ for the even/paired photon, $O(k^2)$ on a bare chiral branch. **Collision note**: same letter as Ch.3's hop matrices $M_{\mathbf d}$... no — see below for $D$ collision entry. | Ch.7 §7.2.2 |
| $\beta_\text{LV},\gamma_\text{LV},\delta_\text{LV},\varepsilon_\text{LV}(m)$ | Closed-form SR-2 time-dilation Lorentz-violation coefficients, all strictly negative on $(0,1)$. | Ch.7 §7.2.3 |
| $\rho(m)$ | $\rho(m)=\tan(\arcsin m)/\arcsin m=1-2\beta_\text{LV}(m)$; leading isotropic term of $D_i$. | Ch.7 §7.2.4 |
| $\eta(\hat k)$, $E_\text{LV}$ | Myers–Pospelov dimension-5 coefficient/energy scale for the excluded single-branch chiral fermion operator. | Ch.7 §7.2.7 |

## Chapter 8 — The photon

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\mathbf F_\pm(\mathbf k)$ | Riemann–Silberstein combinations $\mathbf E\pm i\mathbf B$; exact eigenvectors of the $(\mathbf E,\mathbf B)$ rotation, eigenvalues $e^{\mp i\Omega}$. | Ch.8 §8.2.1 |
| $\Omega^\pm(\mathbf k)$ | The (excluded) single-branch photon dispersion, $2\omega^\pm(\mathbf k/2)$; carries genuine linear birefringence. | Ch.8 §8.2.1 |
| $\Omega_\text{pair}(\mathbf k)$ | The physical paired-photon dispersion $\equiv\Omega_\text{even}(\mathbf k)$ (Ch.6 R6.3); rate a bound cross-branch two-Weyl-quantum pair carries. | Ch.8 §8.2.3 |
| $(g_L,g_R)$ | A sector's coupling weights on the two BCC chiral branches; pairing-classification input. | Ch.8 §8.2.2 |
| $T(\mathbf k)$ | Free two-body continuum floor, $\min_p[\omega^+(\mathbf k/2+p)+\omega^-(\mathbf k/2-p)]$. | Ch.8 §8.2.5 |
| $M_6(\mathbf k)$, $P_T(\mathbf k)$ | The 6-vector $(\mathbf E,\mathbf B)$ evolution block operator and transverse projector. | Ch.8 §8.2.7 |
| $K(\mathbf x)$ | Position-dependent dielectric (F64, owned by Ch.18); forward-reserved here for the photon-propagator generalization. | Ch.8 §8.2.11 |

## Chapter 9 — Electromagnetism

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $P=e^{i\theta}\mathbb I_2$ | Identity-channel Peierls (gauge) phase the U(1) connection applies to a Weyl spinor; forces the even/non-birefringent channel. | Ch.9 §9.2.1 |
| $\rho(\mathbf x)$, $\mathbf J(\mathbf x)$ | The BCC Weyl walk's exactly conserved U(1) charge density and current. | Ch.9 §9.2.3 |
| $\mathbf C(\mathbf k)$, $\hat{\mathbf C}(\mathbf k)$ | The (odd-in-$\mathbf k$) BCC curl symbol; exactly anisotropic in *direction* off cubic axes, isotropic in magnitude. | Ch.9 §9.2.2/§9.2.3 |
| $U_{\mathbf d}(\mathbf x)=e^{iq\mathbf A(\mathbf x)\cdot\mathbf d/\sqrt3}$ | Per-link Peierls phase attached to each of the 8 BCC hop directions individually. | Ch.9 §9.2.4 |
| $\mu_\star$ | Higgs-free electroweak matching scale, $=4\pi v$ exactly (F138). | Ch.9 §9.3.2 |

## Chapter 10 — Photon-fermion live edge

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\mathbf J_\text{full}=\mathbf J_\text{exact}^L+\mathbf J_\text{naive}^T$ | Physically motivated current sourcing the radiative sector; exact longitudinal solution plus a disclosed constitutive-choice transverse piece. | Ch.10 §10.3.3 |
| $g_\text{lat}$ | Field-sourcing coupling constant; governs only the field-sourcing half of the loop, not the matter push. | Ch.10 §10.3.4 |
| $R=\text{diag}(1,-1,1)$ | Exact reflection relating $\hat{\mathbf C}(\mathbf k)$'s small-$k$ direction to $\hat{\mathbf k}$. | Ch.10 §10.3.5 |

## Chapter 11 — Mass without a Higgs

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\alpha_i,\beta$ | Dirac matrices in a Weyl-basis representation; $\beta_g=(U\sigma_1U^\dagger)\otimes\sigma_0$ the gauged form. | Ch.11 §11.2.1–11.2.2 |
| $U(x)\in SU(2)$ | (Fills Ch.1's P6 reservation.) The chiral $SU(2)$ connection carrying complex mass; shown pure gauge in the mass step, no propagating d.o.f. | Ch.11 §11.2.2–11.2.3 |
| $M(\theta)$, $M_\text{SU2}$ | Per-cell mass-step unitary. | Ch.11 §11.2.3 |
| $\theta(x)$ | Pure-gauge chiral phase; the $\gamma^0\gamma^5$ covariant. | Ch.11 §11.2.1, §11.2.6 |
| $V(x)$ | Gauge-coupled construction's independent mass-sector $SU(2)$ link (distinct from kinetic-sector link $U$); object of R4.11's no-go. **Collision note**: reuses letter $V$ already used in Ch.2 (R2.8, second dispersive flow) and Ch.5 (§5.2.8, internal gauge representation space) for unrelated objects. | Ch.11 §11.5 |
| $m_f$ | Dimensionless lattice mass parameter, one per fermion flavor; magnitude free at this chapter's level. | Ch.11 §11.1 |
| $\Omega_\text{rest}(m)=\arcsin m$ | Zero-$\mathbf k$ rest rotation angle (extends Ch.6's forward citation). | Ch.11 §11.2.6 |
| $\omega_Z=2\arcsin(m)$ | Zitterbewegung frequency, dynamically measured. | Ch.11 §11.2.5 |

## Chapter 12 — Hypercharge and electroweak

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $W_\mu^a(x)$, $U_\ell\in SU(2)$ | Dynamical $SU(2)_L$ gauge field and BCC link variables. | Ch.12 §12.2.2 |
| $\Omega_W(\mathbf k)=\Omega_\text{even}(\mathbf k)$ | Free $W$-field dispersion, adopted for Hermitian-symmetry reasons (see Gap G-7). | Ch.12 §12.2.3 |
| $F^a_{\mu\nu}(x)$ | $SU(2)$ Wilson-plaquette field strength. | Ch.12 §12.2.4 |
| $U_\text{st}(x)\in SU(2)$ | Stueckelberg scalar generating $m_W$ without a Higgs VEV. | Ch.12 §12.2.6 |
| $\theta_W$ | Weinberg angle; input at F35, derived by three routes in Group D. | Ch.12 §12.2.7, §12.2.17–24 |
| $\Delta Y_e,\Delta Y_\nu,\Delta Y_u,\Delta Y_d$ | Higgs-equivalent hypercharge differences $Y_L-Y_R$ absorbed into $U(x)$. | Ch.12 §12.2.10–11 |
| $P=(-1)^{x_1+x_2+x_3}$ | BCC bipartite sublattice parity; unique carrier of hypercharge. | Ch.12 §12.2.12 |
| $y_Q,y_u,y_d,y_L,y_e,y_\nu,y_\phi$ | Normalised hypercharge unknowns of the quantisation system. | Ch.12 §12.2.13 |
| $u$ | F141's universal per-channel stiffness quantum ($=18\pi\alpha/7$, F320). **Collision note**: reuses letter $u$ also used generically for the scalar Bloch-dispersion part $u(\mathbf k)$ (Ch.2 §2.2 onward) — a different object, context distinguishes. | Ch.12 §12.2.21, §12.2.24 |
| $\mu_\star=4\pi v$ | NDA compositeness matching scale where $\sin^2\theta_W=1/4$ holds exactly (extends Ch.9's reservation). | Ch.12 §12.2.19 |
| $\Delta r$ | Electroweak radiative correction to the on-shell mass relation; shown to cancel in F320's mass-ratio theorem. | Ch.12 §12.2.24 |
| $T^\pm=T^1\pm iT^2$, $J^\pm(x)$ | Charged-current raising/lowering generators and currents. | Ch.12 §12.2.25 |

## Chapter 13a — Colour structure and confinement

*Note: this chapter carries no dedicated "Notation established" table of its own (checked directly —
absent from the file). Symbols below are extracted from its running text instead, at the sections
cited.*

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\varepsilon_c(x)$ | Colour-dielectric field renormalising the gluon $(\mathbf E,\mathbf B)$ rotation rule; confining analogue of Ch.18's gravity dielectric $K(x)$, opposite impedance regime (broken vs. matched). | Ch.13a §13a.4.2 |
| $v$ (condensate VEV) | Colour-magnetic condensate vacuum expectation value; simultaneously fixes $\varepsilon_c$, the dual-Meissner gluon mass $m_V=ev$, the screening length, and (via $\sigma=2\pi v^2n$) the string tension. **Collision note**: reuses the letter $v$ already used for the electroweak VEV $v=246.22$ GeV (Ch.12) — a different, colour-sector condensate scale. | Ch.13a §13a.4.2–13a.4.5 |
| $\sigma_k$ | String tension for N-ality $k$; the Lagrange multiplier conjugate to $\mathbb Z_N$ centre-phase non-closure (F99), exact identity. | Ch.13a §13a.4.4 |
| $\chi$ | Rotor "mass"/stiffness parameter in the compact quantum (Mathieu) rotor Hamiltonian $H=\frac1{2\chi}\hat E^2-\lambda\cos\hat\phi$; related to $g_s$ via $\chi=1/(4g_s^2)$ (F110 C7 identity). | Ch.13a §13a.3.2, §13a.4.4 |
| $N_c$ | Number of colours; structurally bracketed to odd, $\ne1$ ($\{3,5,7,\ldots\}$), selected to 3 only empirically (28-decade confinement-scale lever). | Ch.13a §13a.3 throughout |

## Chapter 13b — Dynamical QCD and the X1 saga

*Note: this chapter also carries no dedicated "Notation established" table (checked directly).*

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\chi$ | Rotor stiffness (extends Ch.13a); locked to $\chi=1$ by circular-rotation forcing, giving $g_s=1/2$. | Ch.13b §13b.2.1 |
| $q_\ast$ | Lattice-to-continuum one-loop matching scale (equivalently $d_1$); the chapter's single largest open computation. | Ch.13b §13b.2.4, §13b.4 |
| $a_1(n_f)$ | Exact one-loop $V\to\overline{\rm MS}$ conversion coefficient, $a_1(6)=11/3$. | Ch.13b §13b.2.4 |
| $\alpha_\text{eff}^\ast$ | IR-face frozen/saturated coupling ($\approx0.39$), the gap-equation fixed point. | Ch.13b §13b.2.4 |
| $\beta_t/\beta_s$ | Lattice temporal/spatial gauge-action anisotropy; derived $=4$ (not the naive hypercubic $\xi^2$). | Ch.13b §13b.3.4 |

## Chapter 14 — Hadrons

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $B(x)=\varepsilon_{abc}q_1^aq_2^bq_3^c$ | Colour-singlet baryon interpolating operator. | Ch.14 §14.2.1 |
| $t^*$ | F92/F97 phase-closure angle; forbidden for $N\ge3$ baryons. | Ch.14 §14.2.2 |
| $k$ (N-ality) | $\mathbb Z_3$ centre charge; simultaneously closure-budget label and string-tension winding coefficient. | Ch.14 §14.2.3 |
| $\boldsymbol\xi_1,\boldsymbol\xi_2$ | Mass-normalised Jacobi coordinates, three-quark relative problem. | Ch.14 §14.2.4 |
| $\rho^2=\xi_1^2+\xi_2^2$ | Hyperradius of the coarse-grained baryon element. | Ch.14 §14.2.6 |
| $m_c$ | NJL constituent quark mass. | Ch.14 §14.3.1 |
| $m_\sigma,\,g_{\sigma NN}$ | Scalar-isoscalar meson mass and nucleon coupling (pion's chiral partner). **Collision note**: $\sigma$ here is the meson, distinct from the string tension $\sigma$ (Ch.13a) and the Pauli matrices $\sigma^i$ (Ch.1) — the chapter's own header explicitly flags this. | Ch.14 §14.4.3 |
| $m_\omega,\,g_{\omega NN}$ | Isoscalar-vector meson mass and nucleon coupling; $g_{\omega NN}^2/4\pi$ is a genuine free input (R14.14). | Ch.14 §14.4.4 |
| $g_\text{cm}$ | Colour-magnetic (colour-hyperfine) coupling, fixed externally by the $N$–$\Delta$ splitting. | Ch.14 §14.4.2 |
| $b$ | Single-quark Gaussian cluster size regulating every OBE vertex ($=0.55$ fm). | Ch.14 §14.4.2–14.4.8 |
| $R_\text{conf}$ | Gauge-dynamics-derived single-constituent confinement radius, $\approx1.11/\sqrt\sigma$. | Ch.14 §14.5.5 |
| $S_{12}$ | Tensor spin-angular operator mixing the deuteron's $^3S_1$/$^3D_1$ channels. | Ch.14 §14.4.1 |
| $E_b,\,\kappa,\,r_d,\,P_D$ | Deuteron binding energy, asymptotic wavenumber, matter radius, D-state probability. | Ch.14 §14.4.1 |

## Chapter 15 — Generations and lepton spectrum

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $T_{1u}$ | Unique odd-parity 3-dimensional irrep of $O_h$; the generation multiplet. | Ch.15 §15.2.1 |
| $E_g$ | 2-dimensional $O_h$ irrep carrying the generation-splitting order parameter, on the BCC second-neighbour shell. | Ch.15 §15.2.1/§15.2.4 |
| $Q$ | Koide ratio $\sum m_a/(\sum\sqrt{m_a})^2$; $Q=2/3$ is the 45° equipartition point. **Collision warning (flagged explicitly by the task brief)**: this is a lepton-sector dimensionless ratio, unrelated to any electric-charge $Q=T_3+Y/2$ used from Ch.9/Ch.11 onward — same letter, definitely different objects; a reader must track which "$Q$" is meant by context in every chapter from here on. | Ch.15 §15.2.1 |
| $y_a=\sqrt{m_a}$ | Pairing/condensate amplitude carrying the $T_{1u}$/$E_g$ vector quantum numbers. | Ch.15 §15.2.3 |
| $\phi,\ t$ | Generation-space rotation angle / per-constituent pair phase; $45°$ the universal equipartition point. | Ch.15 §15.2.3 |
| $\bar y,\ e,\ \delta$ | $E_g$ condensate's democratic ($A_{1g}$) amplitude, splitting ($E_g$) magnitude, phase angle. **Collision note**: $e$ here is the condensate saturation amplitude, not the elementary charge (Ch.9's $e$, $\alpha_\text{em}=e^2/4\pi$) — same letter, different sector. | Ch.15 §15.2.4 |
| $B,\ C,\ \lambda_6$ | Cubic and sextic Landau invariants of the $E_g$ condensate; $\lambda_6\equiv C/e^6=0.243$, the sextic clock coupling (registered constant). | Ch.15 §15.2.4–15.2.5 |
| $\delta^*$ | Physical (saturated-condensate) value of $\delta$; adopted $=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=2/9$ rad. **Deliberate numerical coincidence, per CLAUDE.md D7 — kept as a separate registered constant**: this $2/9$ is unrelated to Ch.12's $\sin^2\theta_W^\text{on-shell}=2/9$ (F231/F141) and to Ch.13b's strong-sector Fierz coefficient $c=2/9$ (F145) — three independent $2/9$'s from three different sectors, never to be merged. | Ch.15 §15.2.6 |
| POSIT-N | The (now-derived, R15.19) statement that the $E_g$ generator norm $R=1$. | Ch.15 §15.2.6 |
| $\eta^2$ | Equipartition amplitude, $\sin^2t^*=1/2$ at the pair-saturation angle $t^*=45°$. | Ch.15 §15.2.3–15.2.4 |
| $N$ | Overall fermion mass scale (dimensionless lattice mass $\to$ MeV); left free, forward-cited to Ch.13/17. | Ch.15 §15.1, §15.6 |

## Chapter 16 — Neutrinos

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\nu_R$ | Right-handed neutrino: total SM gauge singlet ($Y_{\nu_R}=0$, structurally forced). | Ch.16 §16.2.1 |
| $M_D$ | Dirac mass coupling $\eta_L$ to $\nu_R$, via the F27/F41 mass step. | Ch.16 §16.2.1 |
| $M_R$ / $M_{R0}$ | Bare Majorana mass on $\nu_R$ / overall texture prefactor; proven fixed by nothing in the model (F343). | Ch.16 §16.2.1, §16.2.3/§16.2.6 |
| $\delta_\nu$ | Neutrino-sector's own $E_g$ condensate angle; shares charged-lepton texture *form* (Ch.15) but not its value. | Ch.16 §16.2.3 |
| $t_{xy},t_{yz},t_{zx}$ | Three second-shell $T_{2g}$ (axis-mixing) amplitudes; proven to transform as three inequivalent 1-d irreps of $D_{2h}$, hence genuinely free. | Ch.16 §16.2.3–16.2.4 |
| $D_{2h}$ | Residual point-group stabilizer of a generic-angle $E_g$ condensate (order 8, no axis permutations); inherits Ch.15's F93 O3. | Ch.16 §16.2.4 |
| $J$ | Rephasing-invariant Jarlskog combination extracting $\delta_{CP}$ basis-independently. **Collision note**: unrelated to any current $J$ (Ch.5's $\hat J^a$) or Ch.20/21 cosmology usage — check context. | Ch.16 §16.2.5 |

## Chapter 18 — Gravity

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $K(x)$ | Single lattice dielectric index, $A=1/K,B=K$, canonical form $K=e^{2GM/rc^2}$; vacuum/weak-field *representation*, not the fundamental law. **Collision note**: distinct from Ch.15's Koide ratio $Q$ and from Ch.13a's $\chi$; also distinct usage from any Boltzmann/kinetic $K$ elsewhere — check context per chapter. | Ch.18 §18.2.8 |
| $G$ | Structural/induced Newton constant, $G=a^2c^3/(8\pi\sqrt3\hbar)$; dimensionless content $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$ (registered constant `a_over_ellP`). | Ch.18 §18.2.7 |
| $a$ (this chapter) | Physical (dimensionful) BCC lattice cell size. **Collision note, explicitly flagged by the chapter itself**: distinct from Ch.2's dimensionless $a=2/\sqrt3$ in lattice-native units (R2.10) — same letter, one is a pure number, the other a length in metres (fixed in Ch.17). | Ch.18 §18.2.1 onward |
| $\eta_\text{Weyl}$ | Per-Weyl-field Seeley–DeWitt heat-kernel coefficient, $=1/12$ exactly. | Ch.18 §18.2.6 |
| $g_*$ | Count of gravitating Weyl polarizations sourcing induced $1/G$; $=48=16\times3$ (F38 content × F75 generation count, Ch.15 — an undeclared cross-chapter dependency, Gap G-8). | Ch.18 §18.2.7 |
| $T^{00}[\psi]$ | Fermion energy density (not bare $\lvert\Psi\rvert^2$) sourcing $\ln K$. | Ch.18 §18.2.9 |
| $H_{\mu\nu}$ | Lanczos–Lovelock tensor, identically zero at the model's derived $d=4$. | Ch.18 §18.2.12 |
| $\Pi(\mathbf q)=\Pi_0-\Pi_2q^2+\Pi_4q^4-\dots$ | Scalar-channel vacuum polarization; successive coefficients are the induced cosmological-constant, Einstein–Hilbert, and curvature-squared terms. | Ch.18 §18.2.2, §18.2.13 |

## Chapter 19 — Strong-field and wave gravity

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $r_h,\ b_c,\ \kappa$ | Schwarzschild horizon ($2M$), critical impact parameter/shadow radius ($3\sqrt3M$), surface gravity ($1/4M$). | Ch.19 §19.2.1 |
| $T_H$ | Hawking temperature, $\hbar c^3/(8\pi Gk_BM)$. | Ch.19 §19.2.1 |
| $r_\text{core}$ | Lattice-regulated black-hole core radius, $\propto M^{1/3}$, where curvature saturates at $1/a^4$. | Ch.19 §19.2.1 |
| $A(r),\ B(r)$ | Two independent metric functions of the genuine GR/TOV interior kernel ($AB\ne1$, unlike the demoted dielectric's $AB\equiv1$). | Ch.19 §19.2.8 |
| $\Omega_\text{max}$ | Exact top of the paired photon/graviton dispersion band, $=\pi$ radians/tick. | Ch.19 §19.2.10 |
| $M_\text{rem}$ | Model's minimal, one-cell, stable Planck-mass black-hole remnant (F228, reused). | Ch.19 §19.2.10 |

## Chapter 20 — Cosmology

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $t_\text{min}$, $H_\text{max}$ | Earliest resolvable cosmological epoch (Hubble radius = one cell); $H_\text{max}=3^{-3/4}M_\text{Pl}$, $t_\text{min}=\sqrt3$ ticks native $=6.5978\,t_P$ SI (corrected). | Ch.20 §20.2.3–20.2.4 |
| $r_\text{min}$ | Exact, scale-free inflation obstruction, $M_\text{Pl}^2/\Lambda_\text{UV}^2=\sqrt3=1/c_\text{lat}$. | Ch.20 §20.2.6 |
| $\gamma$ | Primordial tilt's anomalous dimension, $n_s-1\equiv-2\gamma$; identically the anomalous part of the model's block-spin relevant eigenvalue. **Collision note**: unrelated to Ch.5's $\hat J^a$-adjacent notation or Ch.13a's Lorentz factor usage — a fourth distinct $\gamma$ in the monograph (see also Ch.11's Dirac matrices $\gamma^0,\gamma^5$ and QED's $\gamma$ for the photon itself). | Ch.20 §20.2.10, §20.2.12 |
| $g_*(T)$ | Cosmological relativistic degree-of-freedom count from the model's own 48 Weyl fields. **Collision flagged explicitly by the chapter itself**: NOT the same object as Ch.18's $g_*=48$ (the gravitating-Weyl-mode count in the induced-$G$ prefactor) — same symbol, temperature-dependent cosmological count vs. a fixed structural integer. | Ch.20 §20.2.14 |
| $\mu(a,k)$, $\Sigma(a,k)$ | Two free functions of general modified-gravity structure-formation phenomenology; both fixed to exactly 1. | Ch.20 §20.2.13 |
| $\gamma_g$ | Linear growth-rate index, $f=\Omega_m^{\gamma_g}$; forced to $6/11$ exactly given $\mu=1$. | Ch.20 §20.2.13 |

## Chapter 21 — The cosmological constant

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\rho_\text{vac}$ | Bare lattice zero-point energy density, $g_*\sqrt3 I_\text{CC}\hbar c/a^4$. | Ch.21 §21.2.1 |
| $I_\text{CC}$ | Dimensionless BCC BZ integral $\int_\text{BZ}d^3k/(2\pi)^3\,\omega(k)/2=4.081049$. | Ch.21 §21.2.1 |
| $p$ | Holographic dilution exponent in $\rho_\text{grav}(L)\propto L^{-p}$; derived $=2$. | Ch.21 §21.2.3–21.2.4 |
| $\rho_\text{crit}$ | Critical density $3H_0^2c^2/(8\pi G)$. | Ch.21 §21.2.4 |
| $\Omega_\Lambda$ | $\rho_\Lambda/\rho_\text{crit}\approx0.6847$; chapter's central undischarged residual, not derivable from the holographic sector. | Ch.21 §21.2.5 |
| $s_\text{cell}$ | Per-F107-cell horizon entropy required by $S=A/4$, $=2\pi\sqrt3$ nats exactly. | Ch.21 §21.2.6 |
| $c_\text{walk}$ | F355's directly-computed vacuum-entanglement coefficient per BCC walk per unit horizon area. | Ch.21 §21.2.6 |
| $C$ | A spacetime-constant piece of the matter trace $T(t)$; the object Kaloper–Padilla sequestering annihilates exactly under spacetime averaging. **Collision note**: yet another $C$ distinct from Ch.15's sextic Landau invariant $C$ and Ch.13a's condensate-related uses — a very overloaded letter across the monograph. | Ch.21 §21.2.8 |

## Chapter 22 — The dark sector

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $a_0$ | MOND/emergent-gravity critical acceleration scale, $a_0=cH_0/6$; the route it belongs to is falsified, retained only as an unexplained coincidence. | Ch.22 §22.2.2 |
| $\rho_\text{dyn}$ | QUMOND/emergent-gravity phantom density, a local functional of baryon distribution. | Ch.22 §22.2.2 |
| $\delta$ | $E_g$ second-shell condensate clock/phase angle (extends Ch.15); reused for both the dark-matter angular mode and the F366 domain-wall precondition. | Ch.22 §22.2.3, §22.2.13 |
| $L$ | Lepton asymmetry driving resonant (Shi–Fuller) sterile-neutrino production. | Ch.22 §22.2.6 |
| $S$ | Post-production entropy-dilution factor from late $N_{2,3}$ decay. **Collision note**: unrelated to Ch.13a's string tension $S$ or Ch.5's Fock-normalization $S$ usage — check context. | Ch.22 §22.2.7 |
| $\mu$ | Graviton–graviton geon's virial (bound-state) mass, $\mu\simeq\sqrt2M_\text{Pl}$. **Collision note**: unrelated to Ch.16's $\mu_\star$ (Ch.9/12 electroweak matching scale) — different symbol form but easily confused. | Ch.22 §22.2.9 |
| $\alpha_g$ | Gravitational "fine structure constant" between two quanta of mass $m$, $\alpha_g=(m/M_\text{Pl})^2$. | Ch.22 §22.2.9 |
| $M_\text{rem}$ | Exact one-cell Planck-mass black-hole remnant mass (extends Ch.19's reuse), $=(\sqrt3/2)^{1/2}M_\text{Pl}\approx0.9306M_\text{Pl}$ — the geon's stable identity. | Ch.22 §22.2.10 |
| $\beta(M_\text{form})$ | Primordial-black-hole collapse fraction at formation mass; the geon's sole free abundance input. | Ch.22 §22.2.10 |
| $\sigma(k)$ | Primordial curvature-perturbation RMS amplitude at comoving scale $k$; the quantity $\beta$ traces to, unfixed by the model. | Ch.22 §22.2.11 |

## Chapter 23 — QED precision

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $v(p,s)=C\bar u(p,s)^\top$ | Positron spinor, electron's charge conjugate; $C=i\gamma^2\gamma^0$. | Ch.23 §23.2.1 |
| $\Lambda^\mu(p,p')$ | One-loop QED vertex correction. | Ch.23 §23.2.3 |
| $F_1(q^2)$, $F_2(q^2)$ | Electric and magnetic (anomalous-moment) form factors; $a_e=F_2(0)$. | Ch.23 §23.2.3 |
| $\ln k_0(n,l)$ | Bethe logarithm, derived from the model's own Coulomb resolvent. | Ch.23 §23.2.4 |
| $f_{IR}(q^2)$ | Shared infrared coefficient of the virtual and soft-real one-loop corrections. | Ch.23 §23.2.5 |
| $A_2$, $A_2^\text{VP}$, $A_2^\text{vertex}$ | Two-loop $a_e$ coefficient and its VP/vertex decomposition. | Ch.23 §23.2.6 |
| $K_1(u)$ | F252's Feynman-parameter kernel, reused with F251's spectral function. | Ch.23 §23.2.6 |
| $\mathcal L_\text{EH}$ | Euler–Heisenberg effective Lagrangian. | Ch.23 §23.2.8 |
| $w$, $E_\text{crit}$ | Schwinger pair-production rate and critical field. | Ch.23 §23.2.8 |
| $D=4-\tfrac32E_f-E_\gamma$ | Superficial degree of divergence of a 1PI QED amplitude. | Ch.23 §23.2.9 |
| $\{Z_1,Z_2,Z_3,\delta m\}$ | Four QED counterterms; $Z_1=Z_2$ proved at every order. | Ch.23 §23.2.9 |
| $\Delta=B_\text{rule}-B_\text{cont}$ | Subtracted lattice-minus-continuum transverse VP coefficient; central diagnostic of the F277/F311/F322 momentum-refold correction. | Ch.23 §23.3.1 |
| $\Delta\alpha_V(M_Z^2)=4\pi\alpha/g_V^2$ | Narrow-resonance VMD estimate of a vector meson's hadronic-VP contribution. | Ch.23 §23.4 |

## Chapter 24 — Atoms and matter

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\mathrm{Ry}=\tfrac12\mu c^2(Z\alpha)^2$ | Physical Rydberg energy, built from the model's own $m_e$/$\alpha$ anchors and reduced mass $\mu$. | Ch.24 §24.2.1 |
| $R_b$ | Block-spin coarse-graining map (extends Ch.14's F130/F133), applied here to a nuclear charge density. | Ch.24 §24.2.4 |
| $b$ (block factor) | Representation choice carrying the proton-to-orbit scale ratio on two tractable lattices; not a fitted parameter. | Ch.24 §24.2.4–24.2.5 |
| $\text{atom}(Z,N)=\text{NUCLEUS}(Z,N)+\text{ELECTRON CLOUD}(Z)$ | Modular element-assembler composition rule. | Ch.24 §24.2.6 |
| $Z_\text{eff}=n\sqrt{-2\varepsilon}$ | Per-orbital hydrogenic effective charge used in the scalar Dirac-Coulomb shift. | Ch.24 §24.2.9 |
| $\Delta E_{n\ell}$ | Scalar (spin-averaged) Dirac-Coulomb $O((Z\alpha)^4)$ ionization-energy shift, per orbital in the SCF. | Ch.24 §24.2.9 |

## Chapter 25 — Emergent condensed matter and information

| Symbol | Meaning | Chapter/section |
|---|---|---|
| $\Delta(0)$, $T_c$ | BCS/Eliashberg gap and critical temperature; $2\Delta(0)/k_BT_c=2\pi/e^\gamma$ and $\Delta C/C_n=12/(7\zeta(3))$ coupling-independent universals. | Ch.25 §25.2.1 |
| $\lambda$, $\mu^*$ | Eliashberg electron-phonon coupling and Morel-Anderson Coulomb pseudopotential; both derived from Ch.18's dielectric $K$. | Ch.25 §25.2.3, §25.2.6 |
| $Z(i\omega_n)$ | Eliashberg mass-renormalization function on the Matsubara axis; $Z(i\omega_0)\to1+\lambda$. | Ch.25 §25.2.4 |
| $\alpha^2F(\omega)$ | Eliashberg spectral function; derived as $\lambda\omega^2/\omega_\text{max}^2$. | Ch.25 §25.2.5 |
| $J$ | Antiferromagnetic super-exchange coupling; $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, from hopping $t(m)$ and mass gap $U(m)=2\arcsin m$. **Collision note**: unrelated to the Jarlskog invariant $J$ (Ch.16) or the current $\hat J^a$ (Ch.5) — track by context in condensed-matter sections. | Ch.25 §25.3.2 |
| $U_\text{exch}(\theta)$ | Native two-qubit entangling gate, $e^{-i\theta\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$; perfect entangler at $\theta=\pi/8$. | Ch.25 §25.3.1 |
| $d$ | Doublon (double-occupancy) leakage fraction; $d=(2t/U)^2$ at leading order. | Ch.25 §25.4.6 |
| $S_\text{CHSH}$ | CHSH Bell parameter; the model's genuinely-generated entangled state saturates $2\sqrt2$ exactly. | Ch.25 §25.4.7 |
| $\langle r\rangle$ | Mean level-spacing ratio (Oganesyan-Huse), distinguishing Poisson (integrable) from GOE (thermalising) spectral statistics. | Ch.25 §25.5.1 |

---

## Notation collisions

*Flagged explicitly per the build instructions — both meanings are recorded, none silently
resolved. This section is extended as later chapters are read.*

1. **$D$** — In Ch.4 (§4.2.5), $D(\mathbf k)$ is the massive BCC Dirac one-tick unitary matrix. In
   Ch.5 (§5.2.10), $D_b(k)$ is the Dirichlet kernel of the block-average operator. In Ch.7 (§7.2.2),
   $D_i(\mathbf k)$ is the finite-$a$ Poincaré defect vector, $\partial_i\Phi$. Three distinct
   objects sharing one letter, distinguished only by subscript/argument convention — a reader should
   check context every time.
2. **$\Theta$** — In Ch.4 (§4.2.5), $\Theta$ is the antiunitary CPT-type operator ($\Theta^2=-1$).
   In Ch.6 (§6.7), $\Theta=k_BT\tau/\hbar$ is the dimensionless lattice temperature. Unrelated
   objects, same letter, both load-bearing in their own chapters.
3b. **$v$** — Ch.12's electroweak VEV ($v=246.22$ GeV, $=(\sqrt2 G_F)^{-1/2}$) vs. Ch.13a's colour-
   magnetic condensate VEV (a dimensionless/lattice-native confinement-sector scale, F86/F88/F117).
   Two different symmetry-breaking scales, same letter, different sectors — do not conflate.
3. **$V$** (three-way) — Ch.2's $V=\mathbb I\otimes A$ (R2.8, the $s{=}4$ composite's second
   dispersive flow); Ch.5's $V$ (the internal gauge-representation Hilbert-space factor, §5.2.8);
   Ch.11's $V(x)$ (the gauge-coupled construction's mass-sector $SU(2)$ link, §11.5). Three
   unrelated objects, one letter, across three chapters.
2. **$V$** — In Ch.2 (§2.3.5, R2.8), $V=\mathbb I_\text{branch}\otimes A$ is the $s=4$ composite's
   second dispersive commuting flow (shown not to survive interaction, F315). In Ch.5 (§5.2.8), $V$
   is the internal gauge-representation Hilbert-space factor. Unrelated objects, same letter.
3. **$s$** — Ch.2 uses $s$ for the per-cell internal (spinor) dimension ($s=2$). Later chapters (per
   the build plan's citation of Ch.15) may use $s$ for a chirality-branch label (Ch.3 §3.1 free input
   1, "$s=\pm1$ the chirality branch label" in R3.1) — already a second, in-tree meaning by Ch.3.
   Watch for a third meaning (e.g. a Mandelstam variable) in later kinematic chapters.

*(Further collisions — anticipated per the task brief, not yet confirmed: $Q$ as the Koide ratio
(Ch.15) vs. electric charge $Q$ (expected from Ch.9 onward); $J$ as a current (Ch.5's $\hat J^a$)
vs. a possible coupling or angular-momentum use in later chapters; $K$ as the gravitational
dielectric $K=\exp(2GM/rc^2)$ (Ch.18, per CLAUDE.md) vs. any other use. To be confirmed and detailed
once those chapters are read.)*

---

## Build status

All 26 chapter files (Chapters 1–25, with 13 split into 13a/13b) have been read and incorporated.
This glossary is complete as of this build. Chapters 13a and 13b carry no dedicated "Notation
established" table of their own (noted at their respective headers above); their key symbols were
extracted from running text instead.
