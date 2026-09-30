# Notebook Reconstruction — Ledger

Cold, independent reconstruction of `references/physics-notes-complete.md` (the transcribed 2007
Ludwig notebook, pages 1–182). This ledger enumerates every distinct BUILD in page order. No
"existing coverage" column — this pass does not consult the repo's findings/claims (see the
firewall in the governing prompt).

Statuses: PENDING · IN-PROGRESS · SOLID · SOLID-WITH-CORRECTION · INCORRECT ·
DEAD-END-AUTHOR-CALLED-IT · DEAD-END-WE-CALLED-IT · NEEDS-WORK · NOT-TESTABLE

Created: 2026-09-22 - (Phase 0). All rows start PENDING.

**Note on page 39:** the transcription file carries a "Simulation notes (added 2026-05-13)"
addendum (lines 944–962) that is *not* part of the 2007 notebook — it is a later annotation
already reporting numerical results for the page-38 CA update rule. Per the firewall's cold-pass
rule, NB-045/NB-046 will be reconstructed independently, from our own code, without reading that
addendum's conclusions as a starting point or a check.

---

## Pages 1–2 — Quantum Scalars I

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-001 | 1 | 9–47 | KG field equation, Lagrangian, canonical momentum, Hamiltonian density for a real scalar field | derivation | SOLID |
| NB-002 | 1 | 49–58 | Fourier-mode convention $\phi_k=((2\pi)^3 2\omega_k)^{-1/2}\int\phi(x)e^{ikx}d^3x$ and its inverse | closed form | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-003 | 1–2 | 59–81 | Substitution of Fourier transforms into $\mathcal H$, integration over $x$ set up but not completed on the page | derivation | SOLID |

## Page 3 — Photon/Graviton Diagrams

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-004 | 3 | 87–90 | "Photon antisymmetric / graviton symmetric" bare assertion | mechanism | SOLID |
| NB-005 | 3 | 92–96 | Tetrahedron with 3 particle types at each vertex has exactly 2 isomers | table/combinatorial claim | SOLID |
| NB-006 | 3 | 98–102 | Octahedron, 2-particle case: bottom fully determined by top, exactly 3 isomers | table/combinatorial claim | NOT-TESTABLE |

(Page 4 blank — no build.)

## Pages 5–6 — Superconductivity vs Spinor Electrodynamics

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-007 | 5 | 112–126 | Spinor-photon-pair mechanism: two spin-½ $\gamma_{1/2}$ exchanged together, behaving as one boson that "only occurs as a pair" | mechanism | SOLID-WITH-CORRECTION |
| NB-008 | 5–6 | 124–136 | Photon-as-Cooper-pair analogy; "superconducting" travel at $c$ without lattice hindrance; negative binding energy conjecture | mechanism | NOT-TESTABLE |
| NB-009 | 6 | 136–142 | Higgs-as-Cooper-pair speculation; questions about $W,Z$ as other spinor-photon states | mechanism/sketch | NOT-TESTABLE |

## Page 7 — Heat of Combustion (chemistry aside)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-010 | 7 | 146–175 | Heat-of-combustion data table + polymerization question ($CH_4+CH_4\to CH_3CH_3+H_2$, etc.) | table | SOLID |

(Page 8 blank — no build.)

## Pages 9–11 — Sachs Motivation; Mass from Field Energy

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-011 | 9 | 184–189 | Narrative motivation for Sachs electrogravity unification (no independent claim) | mechanism/sketch | NOT-TESTABLE |
| NB-012 | 10 | 200–206 | EM energy density $\xi=(8\pi)^{-1}(E^2+B^2)$ motivates charge-sourced self-mass | closed form | SOLID |
| NB-013 | 11 | 214–220 | Point-charge self-energy $\int_{r_0}^\infty E^2\,dV$ diverges as $r_0\to0$; qualitative mass hierarchy (quark > electron > neutrino) tied to interaction count | derivation + mechanism | NEEDS-WORK |

## Pages 12–13 — Weyl Representation

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-014 | 12 | 234–240 | Massive Weyl-basis equations (1a,1b) for $\psi_\pm$ | closed form | SOLID |
| NB-015 | 12–13 | 240–252 | $m_0\to0$ decoupling into independent helicity equations (2a,2b); parity interchanges them | derivation | SOLID |

## Page 14 — Riemannian Geometry Background

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-016 | 14 | 260–276 | Standard metric-tensor/local-flatness definitions, $ds^2$, dot product | closed form (background) | NOT-TESTABLE |

## Pages 15–29 — Sachs Electrogravity Lagrangian (Quaternion $q^\mu$ Formalism)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-017 | 15 | 282–304 | Sachs gravitational Lagrangian $\mathcal L_E=R\sqrt g$ and supporting quoted formulas ($g$, $\partial_\sigma g^{\mu\nu}$, $K_{\rho\lambda}$, $R$, $\Omega_\mu$, $\Gamma^\rho_{\mu\alpha}$) — cites Sachs eqns 6.41/3.59'/6.40/6.45/3.88/2.33b | closed form (quoted) | SOLID (3.88 operator order reversed in notebook convention; see 02b §7.4) |
| NB-018 | 16 | 318–326 | Free 2-spinor Lagrangians $\mathcal L_\eta,\mathcal L_\chi$ and boxed covariant matter coupling $\mathcal L_M^\eta$ | derivation | SOLID |
| NB-019 | 16 | 330–344 | $q^\mu,\tilde q^\mu$ expressed in Pauli-matrix components; Sachs' (3.60),(3.62) forms | closed form | SOLID-WITH-CORRECTION / NOT-TESTABLE (Sachs quote) |
| NB-020 | 17 | 352–372 | $\chi=\varepsilon\eta^*$ ansatz; covariant derivatives $\eta_{;\mu},\chi_{;\mu}$; $\Omega^{(\chi)}_\rho$ formulas (3.77),(3.79b) | derivation | SOLID / cited formulas tested: (3.79b) SOLID, (3.77) operator order reversed (see 02b §7.4) |
| NB-021 | 17 | 365–378 | Boxed total Lagrangian $\mathcal L=\sqrt g\{R+i\eta^+q^\mu\eta_{;\mu}+i\chi^+\tilde q^\mu\chi_{;\mu}\}$ | assembly | SOLID |
| NB-022 | 18 | 384–406 | $T_{00}=\mathcal H$; $G_{\mu\nu}=8\pi T_{\mu\nu}$; boxed $\partial\mathcal L/\partial\dot\varphi_E=(8\pi)^{-1}G_{00}$; $R_{00}$ expansion | derivation | SOLID |
| NB-023 | 19 | 411–418 | Non-spinor GR Hamiltonian $\mathcal H_E$ in first-order (independent $\Gamma,g$) form | derivation | SOLID |
| NB-024 | 19 | 420–431 | Spinor GR Hamiltonian $\mathcal H_E$ in terms of $K,q,\tilde q$ trace formula | derivation | SOLID |
| NB-025 | 20 | 437–453 | First attempt at matter Hamiltonian via $\pi_\eta=i\eta^+q^0$; margin note "$\mathcal H=A\dot\eta-A\dot\eta=0!$"; abandoned mid-line ("$=\cdots$ No, we want") | derivation | DEAD-END-AUTHOR-CALLED-IT |
| NB-026 | 20 | 455–466 | Symmetrized $\mathcal L_M$; energy-momentum tensor $\Theta^{\mu\nu}$ (flat-space form) | derivation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION (sign; see 02b, 2026-09-22) |
| NB-027 | 21 | 470–476 | $\mathcal H_M=\Theta^{00}$ flat-space result; author flags it as missing curvature coupling | derivation + self-critique | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION (inherits NB-026 sign; see 02b) |
| NB-028 | 21 | 476–483 | $\Theta^{\mu\nu}$ redefined with covariant derivatives; corrected $\mathcal L_M,\Theta^{00}$ | correction/derivation | SOLID-WITH-CORRECTION (inherits sign; Tetrode symmetrization; see 02b) |
| NB-029 | 21 | 485–491 | Scalar-field toy matter Lagrangian $\mathcal L_M=i\partial_\mu\varphi\partial^\mu\varphi-\mu^2\varphi^2$ (flat and GR forms) | derivation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-030 | 22 | 497–511 | $\mathcal H_M$ for the toy scalar; boxed full Hamiltonian density combining $\Gamma$-gravity terms + scalar matter | assembly | SOLID-WITH-CORRECTION |
| NB-031 | 23 | 519–538 | Concise total Lagrangian restated; Euler–Lagrange variational principle set up for $q^\mu,\tilde q^\mu,\Omega_\mu,\Omega^{(\chi)}_\mu$ as independent fields | assembly | SOLID |
| NB-032 | 23–24 | 542–548 | Trace-derivative identity $\partial\mathrm{Tr}(AB)/\partial B=\tilde A$; $\partial(-g)^{1/2}/\partial\tilde q^\lambda$; covariant Euler–Lagrange form | derivation | SOLID (trace identity) / $\partial(-g)^{1/2}/\partial\tilde q$ line SOLID-WITH-CORRECTION (power; see 02b §7.2) |
| NB-033 | 24 | 554–579 | Variation of $\mathcal L_\eta$ w.r.t. $\eta_{;\mu},\eta,\eta^+$; covariant-derivative terms of the field equation | derivation | SOLID |
| NB-034 | 25 | 584–608 | Combine variations using $(-g)^{1/2}_{;\mu}=0$ and $q^\mu_{;\mu}=\tilde q^\mu_{;\mu}=0$ (cited "notebook 2 p.42/64"); final boxed EOM $q^\mu\partial_\mu\eta+q^\mu\Omega_\mu\eta=0$ | derivation | SOLID |
| NB-035 | 26–28 | 611–637 | Variation of $\mathcal L$ w.r.t. $\Omega_{\rho,\nu}$: long trace-derivative matrix algebra using $\partial\mathrm{Tr}(ABC)/\partial B=A^tC^t$ | derivation | SOLID |
| NB-036 | 28 | 665–681 | $\partial\mathcal L/\partial\Omega_{\rho,\nu}$ assembled; $\partial\mathcal L/\partial\Omega_\rho=(i/2)\eta^+q^\rho\eta\sqrt g$ current term | derivation | SOLID |
| NB-037 | 28–29 | 683–696 | $(\partial\mathcal L/\partial\Omega_{\rho,\nu})_{;\nu}$ computed two ways; first "appears to all go to 0 — not good!"; second gives $\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}=-\tfrac i2\eta^+q^\rho\eta$; author flags disagreement with Sachs (who gets 0 on LHS) | derivation, self-flagged discrepancy | SOLID-WITH-CORRECTION (resolved 2026-09-22: LHS = Cartan tensor; RHS kept only the U(1) trace, spin part restored — see 02b §8) |
| NB-038 | 29 | 703–711 | $\partial\mathcal L/\partial q^\lambda$ (gravity term) and $\partial\mathcal L_M/\partial q^\lambda$ (matter term); page ends mid-derivation | derivation (incomplete) | SOLID-WITH-CORRECTION (completed 2026-09-22: q-equation G(Ω)=κΘ(Ω), χ and torsion-coupled EOMs constructed — see 02b §9) |

(Page 30 blank — no build.)

## Pages 31–32 — σ-Matrix Motivation

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-039 | 31 | 723–756 | $\sigma^\mu\partial_\mu\psi=0$ proposed as "square root" of KG equation; Clifford relations $(\sigma^0)^2=(\sigma^i)^2=1$, anticommutation | derivation | SOLID |
| NB-040 | 31 | 758–772 | Explicit self-consistency check that $(\sigma^\nu\partial_\nu)(\sigma^\mu\partial_\mu)\psi=(\partial_0^2-\nabla^2)\psi$ via symmetrized Clifford algebra | derivation | SOLID |
| NB-041 | 32 | 778–786 | Does Lorentzian $g^{\mu\nu}$ force $q^\mu=\sigma^\mu$? Answer: no — general Hermitian-basis expansion $q^\mu=\sum q^\mu_a\sigma^a$ | derivation | SOLID |

## Pages 33–34 — Sachs Lagrangian Restated

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-042 | 33–34 | 790–820 | Two-matter-field Sachs Lagrangian restated in full; Euler–Lagrange equation form for curved spacetime set up for $q^\mu,\Omega_\mu,\eta,\chi$ | assembly/restatement | SOLID |

## Pages 35–36 — CA Speculation

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-043 | 35 | 828–844 | "Dependence implies neighborhood. Rules imply geometry." — CA local-rule ⟹ lattice-geometry thesis, via Game-of-Life example | mechanism | SOLID |
| NB-044 | 36 | 848–858 | Dimensionality-from-connection-number classification: 0/1/2/3/4 connections ⟹ 0D/degenerate/1D/(strip or 2D)/(2D or 3D) structures; asymmetric-connection idea | table/classification | SOLID |

## Pages 37–39 — Discretized Wave Equation → Spinor CA

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-045 | 37 | 862–884 | Standard centered-difference discretization of the 2D wave equation on a lattice; noted 2nd-order-in-time dependence problem | derivation | SOLID |
| NB-046 | 37–38 | 885–924 | Boxed explicit finite-difference update rule for the 2-component massless Weyl CA (first-order-in-time causal form) | derivation | SOLID |
| NB-047 | 39 | 928–941 | Numerical stability exploration: naive explicit scheme blows up without the ½ factors; empirical "$\sim0.43$" stabilization observation, interpreted as related to $c$ | numeric | SOLID |

(Page 40 blank — no build.)

## Pages 41–49 — "Quantum Hierarchy Equations of a Free Scalar Field" (clean redo of pp. 1–2)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-048 | 41 | 973–999 | KG Lagrangian/Hamiltonian redo (paper p.1), citing Goldstein 12-23/12-53/12-50 | derivation | SOLID |
| NB-049 | 42 | 1013–1039 | Lorentz-invariant Fourier convention $\tilde\phi(k)=2\omega_k\int\phi e^{ikx}d^3x$; self-consistency check via $\delta^3$; measure identity (IzZ 3.35) | derivation | SOLID |
| NB-050 | 42–43 | 1041–1061 | $H$ transformed to $k$-space, integrated over $x$ to a single-$k$ integral, boxed $(\ast)$ | derivation | SOLID |
| NB-051 | 43 | 1063–1084 | Creation/annihilation mode expansions with commutators (IzZ 3.36/3.37a/3.37b) | closed form | SOLID |
| NB-052 | 44 | 1089–1099 | False-start substitution into $(\ast)$; algebra crossed out by the author, includes a wrong trial commutator | derivation | DEAD-END-AUTHOR-CALLED-IT |
| NB-053 | 44 | 1101–1109 | Side computation of $\phi(x)\phi(y)$ product; also crossed out ("note no sense") | derivation | DEAD-END-AUTHOR-CALLED-IT |
| NB-054 | 45 | 1113–1153 | Clean redo: boxed $H=\tfrac12\int\omega_k(a_k^+a_k+a_ka_k^+)\frac{d^3k}{(2\pi)^32\omega_k}$ ("Ludwig eq. 3") | derivation | SOLID |
| NB-055 | 46 | 1159–1169 | Discretization to lattice sum, boxed $H=\sum\tfrac12\omega_j(a_ja_j^++a_j^+a_j)$ ($\boxtimes$); Schrödinger equation $i\partial_t|\psi\rangle=H|\psi\rangle$ | derivation | SOLID |
| NB-056 | 46 | 1171–1181 | Eigenstate equation $H|n\rangle=\sum(n_j+\tfrac12)\omega_j|n\rangle$; general-state expansion substituted | derivation | SOLID |
| NB-057 | 46–47 | 1183–1209 | Normalization constant $A$ relating Fock coefficients $C_n$ to the continuum wavefunction $\psi_N$ (Ludwig eqns 19, 8) | derivation | SOLID |
| NB-058 | 47–48 | 1211–1237 | Substitution into $\boxtimes$; factors cancel; vacuum constant $K=\sum\tfrac12\omega_j$ isolated; phase redefinition $\psi'=e^{-iKt}\psi$ removes it | derivation | SOLID |
| NB-059 | 48 | 1237–1239 | Final multiparticle free-boson equation $i\partial_t\psi'_N=\sum_j\omega_{k_j}\psi'_N$ ("Ludwig eq. 3") | derivation | SOLID |
| NB-060 | 48–49 | 1239–1253 | Self-critique: the equation is not manifestly covariant, $\omega_k=\sqrt{k^2+m^2}$ resists a simple Fourier-local operator picture | mechanism/critique | NOT-TESTABLE |
| NB-061 | 49 | 1247–1255 | Bose symmetrization requirement stated; Bose/Fermi statistics tied to (anti)commutation of ladder operators | closed form (standard) | NOT-TESTABLE |

(Page 50 blank — no build.)

## Page 51 — Harmonic-Oscillator Structure

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-062 | 51 | 1267–1291 | Mode Schrödinger equation from $\boxtimes$; $a_k^\pm$ in terms of $\phi_k,\pi_k$ (real-mode convention, $a_k=(a_{-k}^+)^*$) | derivation | SOLID |
| NB-063 | 51 | 1279–1289 | Wavefunction interpretation $|n\rangle=\Psi(\phi_{-p}\ldots\phi_p)$; probability density $P(\phi_j)$ | closed form (standard) | NOT-TESTABLE |
| NB-064 | 51 | 1291–1295 | Note that $a_k^+a_k$ read naively as a single-oscillator number operator is "overly simplistic" | mechanism/critique | SOLID |

## Page 52 — Coupled-Oscillator / 45° Rotation

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-065 | 52 | 1316–1320 | $\mathcal H\simeq\pi_k\pi_{-k}/\omega_k^2-\omega_k^2\phi_k\phi_{-k}$ recognized as a *coupled* pair of oscillators, not two independent ones; toy model $\mathcal H\psi=-\hbar^2\partial_x\partial_y\psi-\omega_0^2xy\psi$ | derivation/observation | SOLID |
| NB-066 | 52 | 1326–1343 | 45° rotation $x^*,y^*$ diagonalizes the $xy$-coupled toy Hamiltonian into one positive + one negative harmonic oscillator | derivation | SOLID |

## Page 53 — Bose Symmetrization Mechanics

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-067 | 53 | 1349–1359 | Symmetrization operator $S=\tfrac1{N!}\sum_P P$; commuting creation operators automatically enforce Bose exchange symmetry | derivation (standard) | SOLID |

## Page 54 — Even/Odd Mode Decomposition

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-068 | 54 | 1365–1394 | $\bar\phi_p,\tilde\phi_q$ even/odd combinations defined; $\alpha_p^+,\beta_q^+$ creation operators; relation to $a_k^+$ | derivation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-069 | 54 | 1396–1404 | Reality of $\phi(x)$ used to argue $\phi_k=\phi_{-k}^*$, concluding $\phi_k-\phi_{-k}=0\Rightarrow\tilde\phi_q=0$ | derivation/claim | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |

## Page 55 — Hamiltonian in α, β Operators

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-070 | 55 | 1410–1426 | $H$ rewritten via $\bar\pi_k,\bar\phi_k,\tilde\pi_k,\tilde\phi_k$, then via $\alpha_k,\beta_k$: final form $H\propto\int(\alpha^+\alpha+\alpha\alpha^++\beta^+\beta+\beta\beta^+)$ | derivation | SOLID |
| NB-071 | 55 | 1428 | Open question: can the antisymmetric ($\beta$) sector be discarded as "non-Bose"? | mechanism/question | NOT-TESTABLE |
| NB-072 | 55 | 1430–1440 | $[\alpha_k,\alpha_p^+]$ commutator computation, partly obscured by an ink blot in the original | derivation (damaged) | NEEDS-WORK |

## Page 56 — Mixed Operators; T Cross Term

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-073 | 56 | 1446–1452 | $a_k^\pm=\tfrac1{\sqrt2}(\alpha_k^\pm\pm i\beta_k^\pm)$ mixing ansatz; expansion of $a_k^+a_k+a_ka_k^+$ | derivation | SOLID |
| NB-074 | 56 | 1454–1472 | Cross term $T=\tfrac i2(\beta^+\alpha-\alpha^+\beta+\beta\alpha^+-\alpha\beta^+)$; using $\alpha_k=\alpha_{-k}$, $\beta_k=-\beta_{-k}$ parity to get $T_k=-T_{-k}\Rightarrow\int T_k\,d^3k=0$ | derivation | SOLID |

## Page 57 — Sakurai Insert (reference, not author's derivation)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-075 | 57 | 1476–1518 | Photocopied textbook page: $J_\pm$ matrix elements, spin-½ Pauli/spin-1 $S$ matrices | reference (quoted) | NOT-TESTABLE |

(Page 58 blank — no build.)

## Pages 59–60 — Complex Mass / Gauged Dirac Matrices

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-076 | 59 | 1532–1546 | Standard Dirac $\alpha_i,\beta$ from $(\vec\alpha\cdot\vec p\,c+mc^2\beta)^2=(p^2c^2+m^2c^4)\mathbb I$ | closed form (standard) | SOLID |
| NB-077 | 59 | 1555–1559 | Non-uniqueness of $\beta$: $\beta=(a\sigma_1+b\sigma_2)\otimes\sigma_0$, $a^2+b^2=1$, solves the same Dirac algebra | derivation | SOLID |
| NB-078 | 60 | 1565–1573 | Gauging $\beta_g=(U\sigma_1U^+)\otimes\sigma_0$ with $U=\mathrm{diag}(1,e^{i\theta})$; interpreted as a local $SU(2)$-flavored symmetry acting on one helicity, likened to weak-interaction handedness | mechanism/speculation | SOLID |

## Page 61 — Weak Interaction Facts (restated SM facts)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-079 | 61 | 1580–1584 | $W^\pm,Z$ couple only left-handed; $\gamma$ couples to the "bottom" component; $L\leftrightarrow R$ mixing ⟺ mass | closed form (SM fact) | SOLID |

## Pages 62–72 — Weinberg–Salam Without Higgs

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-080 | 62 | 1590–1606 | W–S Lagrangian without Higgs: $\vec G^{\mu\nu},H^{\mu\nu}$ field strengths, $D_\mu^L,D_\mu^R$ covariant derivatives, explicit mass terms $m_\nu,m_e$ | closed form (standard framework) | SOLID |
| NB-081 | 62 | 1606–1609 | Critique: dropping $\nu_R$/making $e_R$ a singlet in conventional W–S destroys $L\leftrightarrow R$ symmetry | mechanism/critique | SOLID |
| NB-082 | 63 | 1611–1628 | $A_\mu,Z_\mu$ as rotations of $W^3_\mu,W^0_\mu$; combined-coupling matrix requiring $A_\mu$ not couple to $\nu_L$ | derivation | SOLID |
| NB-083 | 64 | 1634–1652 | Boxed $g'/g=\tan\theta$ condition $(\ast)$; $e=2g\sin\theta$; $\beta=\tfrac12e(\cot\theta-\tan\theta)$ — author flags a sign issue mid-derivation | derivation, self-flagged sign issue | SOLID / SOLID-WITH-CORRECTION (beta sign) |
| NB-084 | 65–66 | 1660–1690 | Mass terms $m_Z^2=m_W^2\cos^2\theta+m_{W_0}^2\sin^2\theta$, $m_A^2=m_W^2\sin^2\theta+m_{W_0}^2\cos^2\theta$, contrasted directly with the standard W–S result $m_Z^2=m_W^2/\cos^2\theta$; anomalous cross term $\mathcal L_{\rm Anom}=m_Z^2W_{0\mu}W_3^\mu$ left unresolved | derivation, direct comparison to SM | SOLID |
| NB-085 | 67 | 1698–1702 | $A_\mu$-to-isospin / $W$-to-spin coupling-matrix analogy, $\tfrac12(\tau_0+\tau_3)\leftrightarrow\tfrac12(\sigma_0+\sigma_3)$ | mechanism/observation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-086 | 67 | 1704–1713 | Mass term $mc^2(\bar RL+\bar LR)$ vs proposed weak "contact" term $g(\bar\nu_Le_L+\bar e_L\nu_L)+g'(\ldots)$; noted $m_\nu\approx0$, $g'\approx0$ symmetry | derivation/construction | SOLID |
| NB-087 | 68 | 1721–1729 | Kinetic terms for $e,\nu$ doublets; factor-of-2 consistency problem flagged when adding EM + weak kinetic pieces | derivation, self-critique | SOLID |
| NB-088 | 69 | 1738–1752 | Proposed second $U(1)$ field $B_\mu$ for neutral currents; combined $A_\mu,B_\mu$ kinetic Lagrangian; symmetry $g_\nu=m_\nu=g_R=g'\approx0$ noted as "amazing" | construction/mechanism | NOT-TESTABLE |
| NB-089 | 70 | 1758–1770 | Explicit attempt to combine all kinetic terms; factor-of-2 mismatches persist under an $e_R\leftrightarrow e_L$ flip; author abandons in favor of a quadruplet notation ("becoming an ugly way") | derivation, self-abandoned | DEAD-END-AUTHOR-CALLED-IT |
| NB-090 | 71 | 1775–1780 | Neutral-current Lagrangian ansatz via $B_\mu$, contrasted with the analogous EM form via $A_\mu$ | construction | SOLID |
| NB-091 | 71–72 | 1782–1796 | Q&A: existence of $\mu^-\to e^-\bar\nu_e\nu_\mu$ requires a *dynamical* $W$ boson, not merely a mass-like contact term | physics argument | SOLID |
| NB-092 | 72 | 1798–1805 | Proposed $\mu$-decay mechanism through $B_\mu$ radiation + contact interaction, with charge temporarily non-conserved; likened to $\Delta E\Delta t\ge\hbar$ | mechanism, speculative | NOT-TESTABLE |

## Pages 73–74 — Mass & Rotational Travel (helical-motion model)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-093 | 73 | 1813–1824 | Helical trajectory $\vec X(t)$; $v_{\rm eff}=\sqrt{c^2-4\pi^2\nu^2r^2}$ from $|\vec v|=c$ constraint | derivation | SOLID |
| NB-094 | 73–74 | 1826–1836 | Attempted link $\hbar\omega\leftrightarrow v_{\rm eff}$ via $E^2=p^2c^2+m^2c^4$; leads to $v\to\infty$ pathology; author flags "That isn't right!" | derivation | DEAD-END-AUTHOR-CALLED-IT |
| NB-095 | 74 | 1838–1846 | Corrected attempt using relativistic $p=m_0v/\sqrt{1-v^2/c^2}$; derives $v^2=c^2-E_0^2/E^2$; author flags "Way way — no good" | derivation, self-flagged wrong (compare to correct group-velocity relation $v^2=c^2(1-E_0^2/E^2)$) | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |

## Page 75 — Ferbel Reference Data

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-096 | 75 | 1852–1877 | Bibliographic EW precision data ($m_W,m_Z,\sin^2\theta_W,\rho$-parameter, cross-section formulas) copied from Ferbel's ASI text | numeric (reference table) | SOLID |

## Page 76 — Majorana Mass, Fermi Theory, V−A

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-097 | 76 | 1883–1897 | Majorana mass matrix $(M_L,M_D,M_R)$ form; neutrino mass bound table | closed form (standard, quoted) | SOLID |
| NB-098 | 76 | 1899–1911 | Fermi 4-fermion $\mathcal L_F$, $G_F$ value; V$-$A current $J_\mu^{\ell\ell}$ | closed form (standard, quoted) | SOLID |

## Page 77 — Angular Momentum Conservation With a Mass Term

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-099 | 77 | 1917–1926 | Mass term conserves $J=L+S$ not $L$ alone; quoted commutators $[L,\vec\alpha\cdot\vec p]$, $[S,\vec\alpha\cdot\vec p]$ (Greiner) | derivation (standard) | SOLID |

## Page 78 — Blackbody Radiation (minor aside)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-100 | 78 | 1932–1939 | Standard Bose occupation number and spectral density formulas; visible-spectrum wavelength table | closed form (standard) | NOT-TESTABLE |

## Pages 79–81 — Contact Interaction vs Gauge Exchange; Charge Puzzle

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-101 | 79 | 1947–1961 | $m_{W}\to\infty$ contact-interaction limit of a gauge exchange (EFT collapse of propagator to a point) | mechanism (standard EFT) | SOLID |
| NB-102 | 80 | 1965–1979 | Proposed diagrams: neutral current as two mass-like vertices joined by a $W$ exchange, replacing direct $Z$ exchange; photon-exchange analogy sketch | mechanism/speculation | NOT-TESTABLE |
| NB-103 | 80–81 | 1981–1991 | Extended "no spin-0" analogy to $W_\pm,Z$; charge non-conservation puzzle with a weak "mass" vertex | mechanism/question | NOT-TESTABLE |
| NB-104 | 81 | 1989–1991 | $S$ "invented to save $L$ conservation" — spin/angular-momentum bookkeeping analogy proposed for charge | mechanism/observation | SOLID |
| NB-105 | 81 | 1993–2004 | Explicit unitary transform $U_{DW}$ between Dirac-standard and Weyl representations | derivation | INCORRECT (numeric matrix only) / SOLID-WITH-CORRECTION |

## Pages 82–90 — Explicit Dirac/Weyl Plane-Wave Spinors

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-106 | 82 | 2010–2019 | Standard Dirac plane-wave solutions $u^\alpha(k),v^\alpha(k)$ | closed form (standard) | SOLID |
| NB-107 | 82 | 2020–2022 | $U_{DW}$ applied to the four standard basis spinors $u^{1,2}(0),v^{1,2}(0)$ | derivation | SOLID |
| NB-108 | 83 | 2028–2033 | $\gamma_i=\beta\alpha_i=-i\sigma_2\otimes\sigma_i$ in the Weyl representation | derivation | SOLID |
| NB-109 | 83–84 | 2035–2045 | Boxed $\psi_z^{(2)+}(k)$ from $u^\alpha(k)=(\gamma^\mu k_\mu+mI)/\sqrt{2m(m+E)}\,u^\alpha(0)$ restricted to $k_0,k_3$ | derivation | SOLID |
| NB-110 | 84 | 2049–2061 | Three more boxed solutions $\psi_z^{(2)+}$ (redo), $\psi_z^{(1)-}$, $\psi_z^{(2)-}$ | derivation | SOLID |
| NB-111 | 84 | 2063–2068 | Massless limit $m\to0$ of the four solutions; degeneracy puzzle — "why not $(1,0,0,0)^T$ or $(0,0,1,0)^T$?" | observation/question | SOLID-WITH-CORRECTION |
| NB-112 | 85–86 | 2074–2091 | Alternative solution method: plane-wave ansätze (1)/(2), eigen-equations (3a,3b) for $A_\pm$, positive/negative-energy branches | derivation | SOLID |
| NB-113 | 86 | 2101–2103 | Handedness identification of upper/lower components as R/L particle/antiparticle; mass term conserves helicity (mixes particle↔antiparticle only) | physics claim (standard) | SOLID |
| NB-114 | 86–88 | 2105–2165 | Four boxed mass-perturbed solutions $\Psi_{RP},\Psi_{LA},\Psi_{RA},\Psi_{LP}$ (6A–6D) | derivation | NEEDS-WORK |
| NB-115 | 87 | 2124–2127 | $p_z^2-E_z^2=-m_0^2c^2$ — author flags "off by a sign, but pretty close" | derivation, self-flagged sign issue | SOLID |
| NB-116 | 89 | 2171–2189 | EM/weak particle-mass-charge-spin analogy table; margin table sketch | table/classification | SOLID |
| NB-117 | 90 | 2202–2206 | "Could $Z$ be viewed as a bound state of $W^+W^-$?" box diagram; author's own answer: "energies just don't work out" | mechanism/question | DEAD-END-AUTHOR-CALLED-IT |
| NB-118 | 90 | 2210–2235 | Extended EM/Weak classification tables (continued from p.89) | table/classification | SOLID |

## Page 91 — Charge Conservation, Exact vs Perturbative

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-119 | 91 | 2241–2247 | Claim: perturbative mixing $e_R\leftrightarrow e_R^+$ doesn't visibly "conserve charge" order by order; only exact solution restores it | physics claim | SOLID |

## Pages 92–97 — EM/Weak Symmetry Motivational Paper

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-120 | 92–97 | 2263–2288 | 8-component lepton-doublet decomposition; EM/Weak interaction table: 4 charged-interacting, 2 EM-only, 2 W-only, 2 non-interacting states | table/classification | SOLID |
| NB-121 | 97 | 2290–2292 | "Neutrino as the missing magnetic monopole" analogy (both are the "absent" charge state) | mechanism/speculation | NOT-TESTABLE |
| NB-122 | 97 | 2294–2298 | Quark confinement likened to orbital-angular-momentum quantization forcing intrinsic (spin-like) charges to stay unobservable in isolation | mechanism/speculation | NOT-TESTABLE |

## Pages 98–101 — Rotation Matrices, Tensor Products, 3D "Dirac" Equation

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-123 | 98 | 2306 | $R_z\otimes R_z$ tensor-product computation | derivation | SOLID |
| NB-124 | 98 | 2310–2314 | $R_x(\phi)=\exp(i\sigma_x\phi/2)$ explicit matrix and $R_x\otimes R_x$ | derivation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-125 | 98–99 | 2316–2324 | $R_y(\phi)\otimes R_y(\phi)$; attempted double-angle simplification to remove $\phi/2$, left incomplete | derivation (incomplete) | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-126 | 99 | 2326–2332 | Explicit 3×3 spin-1 matrices $S_x,S_y,S_z$; $\sigma_x\otimes\sigma_x,\sigma_y\otimes\sigma_y,\sigma_z\otimes\sigma_z$ | closed form | SOLID |
| NB-127 | 99–100 | 2334–2344 | Basis transformation block-diagonalizing $\sigma\otimes\sigma$ into spin-1 ⊕ spin-0 (Clebsch–Gordan $\tfrac12\otimes\tfrac12=1\oplus0$) | derivation | SOLID-WITH-CORRECTION |
| NB-128 | 100–101 | 2346–2358 | 3D "Dirac" equation $\partial_t\psi_\pm=\mp c\,\mathbf S\cdot\nabla\psi_\pm$ using the 3×3 spin matrices; explicit component form | derivation, speculative extension | SOLID |
| NB-129 | 101 | 2360 | Margin note "if $\psi_+=E+iB$" — links the 3-component field to an EM field-strength pair | mechanism/observation | SOLID (independent claim; basis caveat — see batch 09) |

## Pages 103–104 — Neutral Charge Operator; sin²θ_W Numerology

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-130 | 103 | 2368–2375 | $Q'=t_3\cot\theta_W-t_0\tan\theta_W$ operator evaluated numerically at the experimental $\sin^2\theta_W=0.232$ | numeric | SOLID |
| NB-131 | 104 | 2377–2382 | Hypothetical $\sin\theta_W=\tfrac12$ exploration | numeric/speculative | SOLID |
| NB-132 | 104 | 2383–2395 | $\tau_\pm,V_\pm$ combinations; coupling-normalization algebra $gW_1\tau_1+gW_2\tau_2=g(W_-\tau_++W_+\tau_-)$ | derivation | SOLID |
| NB-133 | 104 | 2397–2405 | Hypothetical "coupling to $W^\pm=3e$" ⟹ $\sin^2\theta_W=2/9\approx0.2222$ | numeric/speculative | SOLID |
| NB-134 | 104 | 2407–2416 | $Q_z$ eigenvalue computation at $\sin^2\theta_W=2/9$; author's own algebra check fails ("✗") | derivation, self-flagged error | NEEDS-WORK |

## Page 105 — EM/Yukawa Self-Energy Integrals

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-135 | 105 | 2422–2425 | Classical EM self-energy $\mathcal E_e=e^2/2r_0$ from $\int E^2dV$ | derivation (standard) | SOLID |
| NB-136 | 105 | 2427–2439 | Yukawa-field self-energy integral $\mathcal E_W$ with exponential-integral form; called "quite ugly" | derivation | SOLID |
| NB-137 | 105 | 2441–2457 | Ratio $\mathcal E_W/\mathcal E_e$; numeric table $I(n)$ vs. $n$; $M_W$, $\hbar$, $k=\hbar c/m_ec^2$, $\alpha r_0$ values | numeric | NEEDS-WORK |

## Page 106 — Newton's Method; Classical Electron Radius

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-138 | 106 | 2463–2473 | Linear-interpolation / Newton's-method formulas (generic math aside) | closed form (standard) | NOT-TESTABLE |
| NB-139 | 106 | 2477–2481 | Classical electron radius computed from $\mathcal E=e^2/2r_0=m_ec^2$, numeric result $r_0\approx1.43\times10^{-15}$ m | numeric | SOLID |

## Page 107 — Ellipse Foci (pure-math aside)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-140 | 107 | 2487–2504 | Ellipse foci relation $a^2+1=b^2$ derived from $d_++d_-=$ const at the axis intercepts; numeric example $b=1.2\Rightarrow a\approx0.67$ | derivation | SOLID-WITH-CORRECTION |

## Pages 108–109 — W–S With Vector W± Bosons

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-141 | 108 | 2510–2524 | Scalar-to-vector promotion of the $W_\pm$ contact term; combined Lagrangian ansatz $\mathcal L_{WS}$ | construction | NEEDS-WORK |
| NB-142 | 109 | 2526–2528 | Critique: the Weinberg angle as a "kludge" allowing $g_0\ne g_e$; question of why $B,W^\pm$ should be massive if they couple only to themselves | mechanism/critique | NOT-TESTABLE |

## Pages 110–124 — "What is a Spinor?" (spinor-as-direction paper)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-143 | 110–111 | 2538–2556 | Spinor ratio $\eta=\alpha/\beta$ invariant under $\Psi\to a\Psi$; thesis "a spinor is a direction without a magnitude" | conceptual claim | SOLID |
| NB-144 | 111–112 | 2560–2576 | Topological argument: sphere ≠ plane ⟹ two complex components needed, not one | conceptual/topological argument | SOLID |
| NB-145 | 112–113 | 2578–2600 | Stereographic-projection setup: sphere of radius $\tfrac12$ at $(0,0,\tfrac12)$; parametrized line (18a–c); intersection condition (19)/(20) | derivation | SOLID-WITH-CORRECTION |
| NB-146 | 113 | 2604–2621 | $t=(1+|\zeta|^2)^{-1}$ (21,23); projection formulas $x,y,z$ in terms of $\zeta,\zeta^*$ (24a–c) | derivation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-147 | 113 | 2623–2627 | Inverse map $\zeta=(x+iy)/(1-z)$ (25) | derivation | SOLID |
| NB-148 | 113–114 | 2629–2649 | Point-at-infinity issue; homogeneous spinor ratio $\zeta=\xi/\eta$ (26); projective formulas (27a–c) | derivation | SOLID-WITH-CORRECTION |
| NB-149 | 114–115 | 2655–2669 | Light cone as the "sphere" $V_0^2-|\vec V|^2=0$; length-contraction argument that a photon's own trajectory is "a single point" — direction without length | conceptual/physical argument | SOLID |
| NB-150 | 115 | 2673–2687 | Four light-cone connections $f_{12},f_{21},p_{12},p_{21}$ between two spacetime points; $\mathcal S,\mathcal T$ reflection relations among them | derivation | SOLID |
| NB-151 | 115–116 | 2689–2711 | $\mathcal S(\zeta)=\mathcal T(\zeta)=-1/\zeta^*$ derived two ways, using $x^2+y^2=t^2-z^2$ | derivation | SOLID |
| NB-152 | 116 | 2713–2721 | Ambiguity in how $\mathcal S,\mathcal T$ act on the separate components $\xi,\eta$ | derivation/observation | SOLID |
| NB-153 | 121–124 | 2723–2785 | General-radius-$r$ rederivation of the stereographic projection (eqns 30a–c, 32–40); two-antipodal-projection reading of a null quaternion as a spinor pair | derivation | SOLID-WITH-CORRECTION |

## Pages 127–140 — "Spinor Functions" (Weyl component form, light-cone field equations)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-154 | 127 | 2797–2815 | $\sigma^\mu\partial_\mu\Psi=0$ in explicit $(\eta,\xi)$ component form (1a,1b) | derivation | SOLID |
| NB-155 | 127–128 | 2817–2822 | Attempted equation for the spinor ratio $\varphi=\eta/\xi$ directly from (1a,1b); called "an intractable mess" | derivation, abandoned mid-attempt | INCORRECT (as transcribed) / DEAD-END-AUTHOR-CALLED-IT |
| NB-156 | 128–129 | 2824–2835 | Wave equations $(\partial_0^2-\nabla^2)\xi=0$ (2b) and $(\partial_0^2-\nabla^2)\eta=0$ (2a) derived from the 1st-order system | derivation | SOLID |
| NB-157 | 129 | 2837–2859 | Attempted factorization of the $\varphi\xi$ wave equation into a wave equation for $\varphi$ (3a) plus a "gauge" cross term (3b) | derivation, speculative split | SOLID |
| NB-158 | 129–130 | 2861–2899 | Light-cone constraint field equation for a vector field $V_\mu(x)$: boxed $V^\mu\partial_\nu V_\mu=0$, derived from a finite-difference light-cone argument | derivation | SOLID |
| NB-159 | 130–131 | 2907–2911 | Unimodular constraint $\vec V\cdot\partial_\mu\vec V=0$; combined with the above to get $V_0=$ const | derivation | SOLID |
| NB-160 | 131 | 2913 | Spinor↔null-vector-field correspondence $\zeta=(V_1+iV_2)/(V_0-V_3)$ | construction | SOLID |
| NB-161 | 131–132 | 2915–2934 | "Maxwell equations from the Weyl equation applied to null vectors" — main component derivation, real/imaginary split of $\sigma^\mu\partial_\mu(\eta,\xi)=0$ with $\xi,\eta$ identified with $V_0,\vec V$ combinations | derivation | NEEDS-WORK |
| NB-162 | 132–133 | 2936–2946 | Boxed $\partial_0\vec V=-\nabla V_0$ (3b) and $\partial_0V_0=\vec\nabla\cdot\vec V$ | derivation | NEEDS-WORK |
| NB-163 | 133 | 2948–2960 | Paired second field $\xi'=-\eta^*,\eta'=\xi^*$; note that treating them as independent gives extra degrees of freedom | derivation/observation | NEEDS-WORK |
| NB-164 | 133 | 2961–2973 | Quaternion $q=\sigma^\mu V_\mu$ construction; decomposition into two 2-component spinors $\varphi_1,\varphi_2$ | derivation | SOLID |

## Pages 141–160 — "Spinors as Null Vectors; Vector Decomposition"

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-165 | 141 | 2979–2987 | Light-cone field equation restated: boxed $V^\mu\partial_\nu V_\mu=0$ and $\vec V\cdot\partial_\mu\vec V=0$ | restatement | SOLID |
| NB-166 | 141–142 | 2989–3000 | "Is a spinor a null vector?" — null condition $V^\mu V_\mu=0$ expressed as proportional-column condition on $\sigma^\mu V_\mu$ | derivation | SOLID |
| NB-167 | 143–144 | 3001–3009 | Tensor-product construction of a null vector from a spinor, $(\alpha^*\ \beta^*)\otimes(\alpha,\beta)^T$, with reality condition on $k_1,k_2$ | derivation | SOLID |
| NB-168 | 144 | 3011–3025 | Decomposition of an arbitrary (non-null) $V_\mu$ into two null vectors $a_\mu+b_\mu$; explicit timelike example decomposition | derivation | SOLID |
| NB-169 | 144 | 3027–3042 | Classification table of $V_\mu$ by sign of $1\pm V_0/|\vec V|$ (timelike±, spacelike±); ellipse/hyperbola geometric picture | derivation/table | NEEDS-WORK |
| NB-170 | 144–145 | 3044–3078 | Explicit timelike decomposition: boxed $a_\mu=\tfrac1{2V_0}(V_0^2-|\vec V|^2+2\hat a\cdot\vec V)(1,\hat a)$, $b_\mu=V_\mu-a_\mu$ | derivation | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |

## Pages 161–175 — "Maxwell Equations from Spinor" (full derivation)

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-171 | 161 | 3088–3100 | $\sigma^\mu\partial_\mu$ acting on the quaternion $\sigma^\mu V_\mu$; four resulting component equations (1a,1b,2a,2b) | derivation | SOLID |
| NB-172 | 161–162 | 3102–3111 | Real/imaginary decomposition of (1a): curl-free condition $\nabla\times\vec V=0$ (2d) | derivation | SOLID |
| NB-173 | 162–163 | 3113–3127 | Full boxed system (7),(8),(9): $\partial_0\vec V=-\nabla V_0$, $\nabla\times\vec V=0$, $\vec\nabla\cdot\vec V=-\partial_0V_0$, asserted as "Maxwell-like equations... in source-free form" | derivation — **central claim of pp.161–175**, needs careful comparison to real vacuum Maxwell (two fields $E,B$, not one field $V$ plus scalar $V_0$) | SOLID |
| NB-174 | 163–164 | 3136–3150 | Wave equation $\partial_0^2\vec V=\nabla^2\vec V$ (10) derived by combining (7),(8),(9) | derivation | SOLID |
| NB-175 | 164 | 3156–3162 | Plane-wave ansatz $\vec V=v\hat z\,e^{i(kz-\omega t)}$; self-consistency of (7),(9) forces $k=\omega$ (not $k=-\omega$) | derivation | SOLID |
| NB-176 | 164 | 3164 | Restated full wave equation $(\partial_0^2-\nabla^2)V_\mu=0$ (11), including $V_0$ | derivation | SOLID |
| NB-177 | 166–167 | 3168–3193 | Null-vector special case $V_0=|\vec V|$: attempted simultaneous solution of (7),(9); equations (12)–(15′) left in a tangled, seemingly-inconsistent state | derivation, messy/incomplete | NEEDS-WORK (root cause identified: invalid chain-rule shortcut, see batch 14) |
| NB-178 | 167–168 | 3195–3201 | Transverse-vs-longitudinal analysis: claim that a pure transverse wave is **not allowed** by $\nabla\times\vec V=0$, forcing a longitudinal wave | derivation/claim — **striking result, contradicts a transverse EM photon; needs very careful checking** | SOLID (confirmed correct; resolved as not conflicting with real EM — a different, single-vector construction, see batch 14) |
| NB-179 | 168–175 | 3203–3261 | Stereographic-projection summary re-derivation ("numbered paper pp.20–21"), general radius $r$ — restates NB-145–148/153 in consolidated form | restatement | SOLID |

## Pages 176–182 — Construction of Null Vectors; Final Pages

| ID | Page(s) | Lines | Statement | Kind | Status |
|---|---|---|---|---|---|
| NB-180 | 176 | 3267–3271 | Two coordinate systems; rotation about $z$ ⟹ overall phase $x_0+iy_0\to e^{i\theta}(x_0+iy_0)$ | derivation | SOLID |
| NB-181 | 176 | 3277–3283 | Outline for the spinor paper (3 to-do items) | outline | NOT-TESTABLE |
| NB-182 | 176–177 | 3285–3301 | Tensor-product null-vector construction $(\alpha^*\ \beta^*)\otimes(\alpha,\beta)^T$, $\det Q=0$ check, phase decomposition $\alpha=\sqrt{V_0-V_z}e^{i\theta}$, $\beta=\sqrt{V_0+V_z}e^{i\phi}$ | derivation | SOLID |
| NB-183 | 177 | 3303 | "Ambiguity of $e^{i\theta}$" flagged as the key unresolved point | observation | NOT-TESTABLE |
| NB-184 | 178 | 3305–3313 | General null $2\times2$ matrix factorization ($\det M=0\Rightarrow M=a(1,\alpha)\otimes(1,\beta)^T$) | derivation (standard linear algebra) | SOLID-WITH-CORRECTION |
| NB-185 | 178–179 | 3315–3339 | Timelike decomposition restated in final form (redo of NB-168/170) | restatement | SOLID-WITH-CORRECTION |
| NB-186 | 179–182 | 3341–3360 | Final null-component geometry: $a_0$ formula in terms of $\hat a,b,\vec u$; special case $\vec V\parallel\hat z$; cylindrical-coordinate transform $\rho_s=2r\rho_0/(r^2-\rho_0^2)$ | derivation | SOLID-WITH-CORRECTION |

---

## Summary

- **Total builds:** 186 (NB-001 – NB-186)
- **All 186 builds disposed as of 2026-09-22** (batches 01–14, NB-001–NB-179, plus the
  contamination-deferred subagent pass covering NB-099 and NB-180–186 — see
  `docs/theory/notebook-reconstruction-15-contaminated-defer-pass.md`). The cold reconstruction of
  `references/physics-notes-complete.md` is complete; remaining work is the operator's own
  correlation pass against the model's findings/claims, using the correlation-queue file as the
  handoff artifact. Batches 07–08 add
  NB-086 – NB-119 (34 builds; see those write-ups for full detail): mostly SOLID, with two
  genuine algebra errors found and corrected (NB-095's dropped $c^2$ factor in the helical
  relativistic-velocity derivation; NB-105's isolated $U_{DW}$ matrix sign slip, shown not to
  propagate), one self-flagged sign doubt resolved as unwarranted (NB-115), one open question
  resolved (NB-111's massless-limit "missing states" puzzle), and one held at NEEDS-WORK pending
  a convention cross-check (NB-114). Batch 09 adds NB-120 – NB-129 (10 builds): the EM/Weak
  lepton-doublet table exactly reproduced from SM group theory (NB-120); two speculative analogies
  assessed NOT-TESTABLE (NB-121/122); two independent transcription errors found and corrected in
  the spin-1/2 rotation-matrix tensor products (NB-124/125, both a diagonal/off-diagonal sin↔cos
  swap plus, for NB-124, a further factor-of-4 double-angle slip); one genuine error found and
  corrected two independent ways in the spin-1 Clebsch–Gordan block-diagonalization (NB-127,
  missing $1/\sqrt2$ on two of three new-basis generators); and the 3D "Dirac" equation and its
  $\psi_+=E+iB$ margin note both confirmed SOLID (NB-128/129), the latter an exactly-correct,
  independently-verified Riemann–Silberstein-vector identity with vacuum Maxwell.
- **Note on the per-verdict tallies below:** this ledger is now being edited concurrently by
  more than one session (confirmed 2026-09-22 — see `notebook-reconstruction-02b-nb028-theta-curved.md`,
  which revises some batch-02 verdicts this session had marked SOLID, e.g. NB-026–028). Per
  operator instruction, concurrent edits are left as-is rather than reconciled here. **The
  authoritative per-build verdict is always the table row's own Status cell**, not the hand-kept
  aggregate counts below, which may lag or drift given concurrent writers — treat them as
  indicative, not exact.
- Pages with no independent build: 4, 8, 30, 40, 50, 58 (blank/bleed-through only).
- Page 7 (heat of combustion) and page 107 (ellipse foci) are non-physics asides, kept as rows for
  completeness but expected to close NOT-TESTABLE or with a quick derivation check only.

## Errata — errors in the notebook (2007)

- **p.1 (NB-002):** Fourier inverse-transform prefactor transcribed as $(2\pi)^{+3}$ where
  self-consistency requires $(2\pi)^{-3/2}$ (confirmed numerically, off by exactly
  $(2\pi)^{3/2}\approx15.75$). A "scratch" slip, superseded by the author's own self-verified
  convention at p.42 (NB-049); not load-bearing since the p.1 calculation stalls at NB-003 and is
  never carried through with this broken convention. See batch 01 write-up.
- **p.16 (NB-019):** "$q_\mu\tilde q^\mu=-4\sigma^0_0$" doesn't match either natural reading of
  the tilde convention used on nearby pages. See batch 02 write-up.
- **p.21 (NB-029, propagating to NB-030):** scalar toy-matter Lagrangian
  $\mathcal L_M=i\partial_\mu\varphi\partial^\mu\varphi-\mu^2\varphi^2$ has a spurious factor of
  $i$, confirmed by direct symbolic Euler–Lagrange computation to give a non-real equation of
  motion. Corrected form: $\mathcal L_M=\tfrac12\varphi_{;\mu}\varphi^{;\mu}-\tfrac12\mu^2\varphi^2$.
  Does not propagate past NB-030. See batch 02 write-up.
- **p.23 vs p.27 (batch 03, extends the NB-019 finding above):** boxed metric formula
  $g^{\mu\nu}=-\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$ (p.23) has the wrong overall sign;
  self-consistency (confirmed via the core Pauli identity) requires the $+\tfrac12$ the notebook
  itself uses two pages later at p.27. Not load-bearing. See batch 03 write-up.
- **p.39 (batch 03):** the empirical "$\sim0.43$ stabilization" observed for the explicit-Euler
  spinor-CA update rule is not a genuine stability threshold — von Neumann analysis proves the
  scheme is unconditionally unstable for every $c>0$. See batch 03 write-up.
- **Batch 04:** none found — every build in pp.41–49 checks out as written.
- **p.54 (batch 05, NB-068/069):** the stated reality condition
  "$\phi_k-\phi_{-k}=0\Rightarrow\tilde\phi_q=0$" is wrong for a generic real field — confirmed
  numerically ($|\phi_k-\phi_{-k}|=1.03\ne0$ on an asymmetric real test function). The correct
  condition, directly readable off the notebook's own two displayed formulas, is
  $\phi_{-k}=\phi_k^*$. Has a live consequence for the still-open question at NB-071. See batch
  05 write-up.
- **p.64 (batch 06, NB-083):** the $\beta=\tfrac12e(\cot\theta-\tan\theta)$ formula has the wrong
  overall sign — corrected $\beta=\tfrac1{\cos\theta}g-2g\cos\theta$ (exact negative of the
  notebook's stated closed form). This precisely locates and resolves the author's own
  self-flagged sign uncertainty on this page. See batch 06 write-up.
- **p.67 (batch 06, NB-085):** $\begin{pmatrix}0&0\\0&1\end{pmatrix}=\tfrac12(\tau_0+\tau_3)$ has
  the wrong sign; corrected to $\tfrac12(\tau_0-\tau_3)$, confirmed by direct matrix computation
  using the standard $\tau_3=\mathrm{diag}(1,-1)$ convention used throughout the surrounding
  pages. See batch 06 write-up.
- **p.74 (batch 07, NB-095):** claimed $v^2=c^2-E_0^2/E^2$ is missing a factor of $c^2$ on the
  second term; correct result (obtained by solving the notebook's own, correctly-set-up starting
  equation) is $v^2=c^2(1-E_0^2/E^2)$ — exactly the standard relativistic group-velocity
  relation. See batch 07 write-up.
- **p.81 (batch 08, NB-105):** the explicit numerical matrix stated for $U_{DW}=U_0U_y$ has the
  wrong sign in its $(2,2)$ entry; direct multiplication of the notebook's own stated $U_0,U_y$
  gives $1+i$ there, not $1-i$. Isolated — doesn't propagate into the boxed final spinor results
  (NB-109/110), independently confirmed correct via the Dirac-equation test. See batch 08
  write-up.
- **p.87 (batch 08, NB-115):** the author's own self-flagged sign doubt on
  $p_z^2-E_z^2=-m_0^2c^2$ is unwarranted — this is algebraically identical to the correct
  $E_z^2-p_z^2=+m_0^2c^2$. No correction needed, just resolved. See batch 08 write-up.

## Errata — errors in my framing of these prompts

- None found in batches 01–03.
- **Batch 04:** an initial verification script for NB-056/NB-057 compared the wrong two
  quantities (a raw creation-operator-product norm against the $N!/\prod n_j!$ combinatorial
  factor, which express different facts) and reported a false mismatch; caught and corrected
  before being written into a verdict. See batch 04 write-up.
- **Batch 05:** two separate script bugs caught pre-verdict — a repeated-operator chain-rule
  slip in the NB-065/066 45°-rotation check (spurious cross term), and two sign errors (a missing
  overall $\tfrac12$, then two flipped-sign terms) in the NB-073/074 $\alpha,\beta$-mixing check,
  the latter caught by cross-checking against an independent sympy noncommutative-symbol
  expansion. See batch 05 write-up.
- **Batch 06:** none found.
- **Batch 08:** an initial attempt to verify NB-114 by re-embedding its boxed spinors into the
  $\gamma^0,\gamma^3$ matrices built for NB-109/110 produced nonzero residuals for every
  sign/branch combination tried; recognized as a likely component-ordering mismatch rather than
  assumed to be a notebook error, and the verdict was based instead on the more directly
  appropriate self-consistency check (does the construction solve its own stated defining
  equations 4a/4c? — yes, exactly). Logged as an incomplete verification. See batch 08 write-up.

## Contamination log

- **Batch 01 (NB-007–009):** `references/mohr-2010-maxwell-photon-wf-summary.md` — nominally
  permitted external literature — turned out to carry a second half describing this project's
  own composite-photon implementation (module names, a finding number, exactness-inventory
  entries). Read before recognized as model-internal. Operator direction: stop pulling from that
  file, use only genuinely external sources going forward (used here: de Broglie 1932, Jordan,
  Pryce 1938, Case, Berezinskii, W. A. Perkins arXiv:1503.00661, read directly). NB-007–009 and,
  later, the pp.161–175 Maxwell-from-Weyl-CA builds (same territory) are flagged for extra
  scrutiny in the eventual correlation pass — see the correlation queue's "Notes for the
  correlation pass" section.
- **End of batch 01 (NB-099, NB-180–186):** `tail -n 20 docs/status/changelog.md` (checking
  entry format before writing a batch note) landed on two live changelog entries naming
  **finding F396** ("p.77 charge partition closed as a relabel of F27's Stueckelberg Ward
  identity") and **finding F397** ("notebook pp.176–182 factorization route," including that it
  disputes the notebook's own boxed $a_\mu$ formula). This directly names verdicts for **p.77**
  (→ NB-099, and by thematic overlap possibly NB-091/NB-092/NB-097/NB-098) and **pp.176–182**
  (→ NB-180–186). Operator direction: (1) hand those specific builds to a fresh, isolated
  subagent when Phase 1 reaches them, rather than reconstruct them in this session; (2) this
  session avoids `docs/status/changelog.md` entirely for the remainder of the work — no more
  changelog entries will be written by this reconstruction, in this or future batches, to avoid
  repeating the exposure. **NB-099 and NB-180–186 are marked CONTAMINATED-DEFER-TO-SUBAGENT
  below and must not be reconstructed by the main session.** — **Resolved 2026-09-22:** a fresh,
  isolated subagent (spawned in its own git worktree, with no access to this or any prior
  session's conversation) reconstructed all six builds cold, per this note's own instruction. See
  `docs/theory/notebook-reconstruction-15-contaminated-defer-pass.md` for the full write-up; all
  six now carry final verdicts in the ledger below (NB-099 SOLID; NB-180/182 SOLID; NB-184/185/186
  SOLID-WITH-CORRECTION, three further genuine 2007 errors found and corrected in NB-186 alone).
  The main session read the subagent's finished write-up and JSON results purely for a quality
  spot-check (script sizes, verdict consistency, that claims were quoted and checked, not
  asserted) and copied them back verbatim from the worktree — it did not re-derive, second-guess,
  or edit any of the subagent's own verdicts, and never read the underlying notebook pages for
  these six builds itself.

## Next steps

**The cold reconstruction is complete.** Batches 01–14 (NB-001–NB-179, see
`docs/theory/notebook-reconstruction-01-scalar-qft-opening.md` through
`docs/theory/notebook-reconstruction-14-maxwell-from-spinor.md`) plus the contamination-deferred
subagent pass (NB-099, NB-180, NB-182, NB-184, NB-185, NB-186 — see
`docs/theory/notebook-reconstruction-15-contaminated-defer-pass.md`) together dispose all 186
ledger rows. NB-181 and NB-183 were already NOT-TESTABLE from the Phase-0 pass (bare
outline/observation, no math). Every row in this ledger now carries a final verdict; there is no
more cold-reconstruction work left to do on `references/physics-notes-complete.md`.

**What's left is the operator's own correlation pass** (explicitly out of scope for this
reconstruction, per the governing prompt's firewall): comparing this ledger's independent verdicts
and the questions logged in `docs/theory/notebook-reconstruction-correlation-queue.md` against the
model's own findings and claims. If a future session resumes work in this file tree, check first
whether another concurrent session has already begun that correlation pass or has revised any of
this ledger's verdicts (per the Summary section's standing note about concurrent editors) before
assuming this ledger is stale.
