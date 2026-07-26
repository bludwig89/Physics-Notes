# Paper VI — The Weak Force: Chiral $SU(2)_L$ Without a Higgs, the Derived Weinberg Angle, and the $\beta$-Decay Charged Current

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper VI of XI. Builds on Paper III (chiral mass / $SU(2)_L$), Paper IV (electromagnetism), and supplies the weak interactions used in the lepton (IX) and baryon (X) sectors.*

*Revision 2 (2026-06-08): re-issued for the eleven-paper series; the chiral $W^\pm$ / even-$Z$ propagator assignment is now noted as forced by the F91 classification theorem.*

---

## Abstract

We present the weak interaction of the BCC quantum-cellular-automaton model as a chiral $SU(2)_L\times U(1)_Y$ gauge theory realised **without a Higgs field**. The left-handed weak isospin symmetry is the exact gauge symmetry of Ludwig's chiral mass step (Paper III); its gauge bosons $W^a_\mu$ are introduced dynamically with covariant fermion vertices, Yang–Mills self-coupling, and a rank-1 Stueckelberg mass that leaves the photon massless while giving $W^\pm$ and $Z$ their masses — the Higgs-eaten longitudinal mode supplied by the pure-gauge phase of the mass step. The Weinberg mixing angle is **derived, not fitted**: the $\sigma\!\leftrightarrow\!\tau$ swap geometry of the BCC doublet gives $\sin^2\theta_W=\tfrac14$ (with $m_Z/m_W=2/\sqrt3=1.1547$, within $1.8\%$ of experiment with zero parameters), and a bond-axis/sublattice count gives the alternative $\sin^2\theta_W=\tfrac29$ ($0.44\%$ from PDG). The dynamical $Z$ carries the correct per-species neutral current, and the full $\beta$-decay charged current $d\to u+W^-\to u+e^-+\bar\nu_e$ runs end-to-end on the lattice with maximal ($V\!-\!A$) parity violation, exact charge/baryon/lepton-number conservation, and the heavy-$W$ Fermi limit $G_F/\sqrt2=g^2/8m_W^2$. All structural relations are verified to machine precision.

---

## 1. Introduction

The weak interaction is the Standard Model's most intricate sector: it is chiral (couples only to left-handed fermions), spontaneously broken (the $W$ and $Z$ are massive while the photon is not), and mixed with hypercharge through the Weinberg angle. In the SM all three features rest on the Higgs mechanism.

The thesis of this paper, anticipated in Paper III, is that the chiral $SU(2)_L$ symmetry is *already present* as the exact gauge symmetry of the lattice mass step, so the weak sector can be built by gauging that symmetry directly — with the longitudinal/Goldstone mode supplied by the mass step's pure-gauge phase rather than by a physical scalar. We then show that the lattice geometry fixes the Weinberg angle, and that the canonical weak process — nuclear $\beta$ decay — runs as an integrated lattice computation.

---

## 2. Chiral $SU(2)_L$ from the mass step

From Paper III (§3) the chiral mass step satisfies the exact Ward identity

$$
V(\mathbf x)\cdot\mathrm{mass\_step}(\psi;U)=\mathrm{mass\_step}\big(V(\mathbf x)\psi;\,V(\mathbf x)U\big),\qquad V\in SU(2),
\tag{2.1}
$$

with $V$ acting only on the left-handed $\eta$ doublet and the right-handed $\chi$ unchanged — a manifestly **chiral** $SU(2)_L$, the weak isospin group, with no Higgs. The left-handed lepton doublet is literally $(\psi_\nu,\psi_e)_L$ and a pure $\nu_L$ state carries $T_3=+\tfrac12$ exactly.

As in any chiral gauge theory, the *kinetic* step alone is not $SU(2)_L$-invariant; local invariance of kinetic + mass requires gauge bosons $W^a_\mu$, introduced next in the standard Yang–Mills fashion. This is not a defect of the complex-mass proposal — it is the universal feature that makes the gauge field necessary.

---

## 3. The dynamical $W$ boson

The $W^a_\mu$ ($a=1,2,3$) are introduced through the same machinery as the gluon (Paper V) and photon (Paper IV):

- **Covariant hopping / fermion vertex.** The left-handed doublet hops with $SU(2)$ link variables; the covariant Dirac-doublet step satisfies the $SU(2)_L$ Ward identity to $1.7\times10^{-17}$ (leptons) and $2.8\times10^{-16}$ (the quark-doublet analogue). The right-handed $\chi$ is decoupled from $W$ bit-for-bit — maximal parity violation built in (Findings F31/F34).
- **Free propagation** by the lattice rotation law (Paper I) on the $W$-triplet bilinear. The charged $W^\pm$ ride the **chiral** law — forced by the F91 classification theorem because the $W$ couples through the left-projector $(g,0)$ (right-branch weight $\equiv0$ over $\mathbb Q$, so the even law is excluded by the exact $|\Delta\Omega|/2$ branch separation). Because $W^\pm$ are massive and not under any astrophysical vacuum-birefringence bound, the chiral law is admissible here (unlike for the photon).
- **Yang–Mills self-coupling** via $\epsilon^{abc}$, the $SU(2)$ analogue of Paper V's $f^{abc}$ (Finding F33).
- **Stueckelberg mass** (next subsection), giving the Proca dispersion $\omega^2=m_W^2+\Omega^2(\mathbf k)$.

### 3.1 The Higgs-free $W$ mass: rank-1 Stueckelberg

The $W$ mass arises from a rank-1 Stueckelberg term whose would-be scalar is the pure-gauge phase already present in the mass step (Paper III, §3.3). The key structural fact is that the rank-1 projector that gives mass to the charged/neutral combinations leaves a massless direction — the photon — exactly massless ($m_A=0$; Finding F44). No physical scalar is introduced; the longitudinal mode of the massive $W/Z$ is the eaten gauge phase. This is the lattice realisation of the non-Abelian Stueckelberg / Kunimasa–Goto construction, and the continuum renormalisability no-go does not bind because of the lattice cutoff.

---

## 4. Electroweak mixing and the derived Weinberg angle

### 4.1 The mixing

The hypercharge field $B$ and the neutral $W^3$ mix by a $k$-independent $O(2)$ rotation (Paper IV, Eq. 4.1) producing the massless photon $A$ and the massive $Z$. The mixing commutes exactly with the rotation propagator ($1.6\times10^{-15}$), and the SM mass ratio is recovered as an algebraic identity,

$$
\frac{m_Z}{m_W}=\frac{\sqrt{g^2+g'^2}}{g}=\frac{1}{\cos\theta_W}\qquad(\text{residual }0,\ \text{bit-for-bit}).
\tag{4.1}
$$

The Gell-Mann–Nishijima relation $Q=T_3+Y/2$ holds for all seven first-generation states ($5.6\times10^{-17}$).

### 4.2 The Weinberg angle from BCC geometry

In the SM $\theta_W$ is a free input. Here it is derived from the lattice structure. The chiral $SU(2)$ extension places at every BCC site a spinor carrying both a spin index ($\sigma$-space) and a weak-isospin index ($\tau$-space), $|\text{state}\rangle\in\mathbb C^2_\sigma\otimes\mathbb C^2_\tau$. The $\sigma\!\leftrightarrow\!\tau$ swap involution $\Pi:A\otimes B\mapsto B\otimes A$ decomposes the 4D space into a 3D swap-symmetric triplet ($\Pi=+1$) and a 1D swap-antisymmetric singlet ($\Pi=-1$). Identifying the swap-singlet direction with $U(1)_Y$ and the swap-triplet directions with $SU(2)_L$, equal bare per-direction coupling strength gives

$$
\frac{g'^2}{1}=\frac{g^2}{3}\;\Longleftrightarrow\;\frac{g'^2}{g^2}=\frac13
\;\Longrightarrow\;
\boxed{\;\sin^2\theta_W=\tfrac14,\quad\cos^2\theta_W=\tfrac34,\quad \frac{m_Z}{m_W}=\frac{2}{\sqrt3}=1.1547.\;}
\tag{4.2}
$$

The factor of $3$ is the dimension of the swap-triplet — the same $3$ that counts the $SU(2)_L$ generators. An independent Casimir check gives the same ratio: $C_2(U(1)_Y)/C_2(SU(2)_L)=(1/4)/(3/4)=1/3$. The mass ratio $m_Z/m_W=2/\sqrt3=1.1547$ lands within $1.77\%$ of the PDG value $1.1346$ with **zero fit parameters** — closer than the tree-level $SU(5)$ GUT value $3/8$, which must be run through $\sim13$ decades to reach experiment (Findings F45/F49).

A second, distinct lattice count — two sublattices versus seven second-shell bond axes — gives $\sin^2\theta_W=\tfrac29=0.2222$, only $0.44\%$ from the PDG $0.2232$ as an exact rational. The two countings ($\tfrac14$ from swap dimension, $\tfrac29$ from bond/sublattice) are tree-level predictions; reconciling them, fixing the overall normalisation, and accounting for the residual gap (RG running, currently absent) are open.

### 4.3 The dynamical $Z$ and the neutral current

The $Z$ is a propagating real $(\mathbf E_Z,\mathbf B_Z)$ pair with free **even**-law rotation (its vector part is helicity-symmetric; the axial branch split is mass-suppressed $\sim k^3$, per F91) and Proca mass $\omega^2=m_Z^2+\Omega_\text{even}^2$. Its fermion neutral current is built explicitly,

$$
J^Z_0(\mathbf x)=J^3_0(\mathbf x)-\sin^2\theta_W\,J^\text{em}_0(\mathbf x)=\sum_f\big(g_L^f\rho_L^f+g_R^f\rho_R^f\big),
\qquad (g_L^f,g_R^f)=(T_3^f-Q^fs_W^2,\,-Q^fs_W^2),
\tag{4.3}
$$

with the source-basis identity holding per site to $2.7\times10^{-15}$ (Finding F48). At the derived bare angle $\sin^2\theta_W=\tfrac14$, the electron $Z$ vector coupling vanishes exactly, $g_V^{e_L}=-\tfrac12-2(-1)(\tfrac14)=0$ — a structural prediction of the $\sigma\!\leftrightarrow\!\tau$ swap, verified bit-for-bit.

---

## 5. $\beta$ decay: the charged current end-to-end

The signature first-generation weak process runs on the lattice as a single integrated chain:

$$
d\;\to\;u+W^-\;\to\;u+e^-+\bar\nu_e.
\tag{5.1}
$$

The raising/lowering structure uses $T^\pm=T^1\pm iT^2$, with site charged currents $J^\pm(\mathbf x)=\psi_L^\dagger T^\pm\psi_L=f_\text{up}^*f_\text{down}$. The $W^-$ field is sourced by the raising quark current exactly,

$$
\Delta E(W^-)=\frac{g}{\sqrt2}\,(J^1+iJ^2)\,\Delta t=\frac{g}{\sqrt2}\,J^+_\text{quark}\,\Delta t,\qquad J^+_\text{quark}=u_L^*d_L,
\tag{5.2}
$$

with residual $9.2\times10^{-16}$ — the $d\to u+W^-$ vertex falls out of the existing sourced-propagation machinery once the charged combination $W^-=(W^1+iW^2)/\sqrt2$ is formed, with no new dynamics (Finding F54). Verified physics content:

- **Maximal parity violation ($V\!-\!A$).** The vertex projector $P_L=(1-\gamma^5)/2$ annihilates a right-handed spinor bit-for-bit; combined with the $W$-decoupling of $\chi$, $C$ and $P$ are maximally violated ($A_C=A_P=1$) while $CP$ is conserved, with the single-generation Jarlskog invariant $N(1)=0$ exactly (no physical CP phase; Finding F53).
- **Quark–lepton universality.** The same bilinear $J^+=f_\text{up}^*f_\text{down}$ and coupling $g/\sqrt2$ describe the quark and lepton vertices ($V_{ud}=1$ for one generation).
- **Conservation laws.** $\Delta Q=\Delta B=\Delta L=\Delta(B-L)=0$ exactly (over $\mathbb Q$) at both vertices and for the full process.
- **Fermi limit.** Integrating out a heavy $W$ gives $G_F/\sqrt2=g^2/8m_W^2$ exactly at $q^2=0$, with leading correction $-q^2/m_W^2$ — the textbook propagator expansion.
- **Causal pipeline.** A localised quark current sources a $W^-$ that propagates causally (Proca) to a distant absorption site driving the leptonic vertex — the lattice realisation of $n\to p\,e^-\bar\nu_e$ at quark level (10/10 checks).

---

## 6. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| $SU(2)_L$ Ward identity (lepton / quark doublet) | §2, §3 | $1.7\times10^{-17}$ / $2.8\times10^{-16}$ |
| Right-handed $\chi$ decoupled from $W$ | §3 | $0$ (bit-for-bit) |
| Chiral $W^\pm$ propagator forced (F91) | §3 | structural (left-projector coupling) |
| $m_A=0$ (rank-1 Stueckelberg) | §3.1 | exact massless direction |
| $m_Z/m_W=1/\cos\theta_W$ | §4.1 | $0$ (bit-for-bit) |
| $\sin^2\theta_W=\tfrac14$ from swap geometry | §4.2 | exact rational; $m_Z/m_W$ within $1.77\%$ |
| $\sin^2\theta_W=\tfrac29$ from bond/sublattice | §4.2 | $0.44\%$ from PDG |
| $Z$ source-basis identity; $g_V^{e_L}=0$ | §4.3 | $2.7\times10^{-15}$; bit-for-bit |
| $W^-$ sourced by $J^+$ | §5 | $9.2\times10^{-16}$ |
| Fermi limit $G_F/\sqrt2=g^2/8m_W^2$ | §5 | exact at $q^2=0$ |
| Full-process conservation $\Delta(B-L)=0$ | §5 | exact ($\mathbb Q$) |

Underlying findings: F27/F31/F34/F34b (chiral $SU(2)_L$, $W$ vertex, Stueckelberg mass), F33 (Yang–Mills self-coupling), F35 (electroweak mixing), F44 ($m_A=0$), F45/F49 (Weinberg angle), F48 (dynamical $Z$), F53 ($C$/$CP$), F54 ($\beta$-decay charged current), F91 (propagator classification).

---

## 7. Discussion

The weak sector is the most direct payoff of the Higgs-free design decision. Because the chiral $SU(2)_L$ is the gauge symmetry of the mass step itself, gauging it requires no new scalar: the $W$ and $Z$ masses come from a rank-1 Stueckelberg term whose longitudinal mode is the pure-gauge phase that would have been the Higgs. The Weinberg angle, an SM input, becomes a tree-level prediction of the BCC swap geometry. And the full $\beta$-decay chain — parity violation, universality, conservation laws, the Fermi limit — runs as one integrated lattice process.

The honest limits are calibration (Tier B): the absolute couplings $g,g'$ and boson masses are uncalibrated, and the $\sim12\%$ gap in $\sin^2\theta_W$ (for the $\tfrac14$ counting) is what RG running and currently-absent lattice loop corrections would have to close; reconciling the $\tfrac14$ and $\tfrac29$ countings is open. None of this affects the structural completeness: every Tier-A weak-sector test passes. The neutrino-mass extension of the weak sector — the right-handed Majorana mass and the see-saw — is developed in Paper IX.

---

## References

1. S. L. Glashow, *Nucl. Phys.* **22**, 579 (1961); S. Weinberg, *Phys. Rev. Lett.* **19**, 1264 (1967); A. Salam (1968) — electroweak unification.
2. E. C. G. Stueckelberg (1938); T. Kunimasa, T. Goto, *Prog. Theor. Phys.* **37**, 452 (1967) — gauge-invariant mass without a scalar.
3. E. Fermi, "An attempt at a theory of beta radiation," *Z. Phys.* **88**, 161 (1934); R. P. Feynman, M. Gell-Mann, "Theory of the Fermi interaction," *Phys. Rev.* **109**, 193 (1958) — $V\!-\!A$.
4. C. Jarlskog, *Phys. Rev. Lett.* **55**, 1039 (1985) — CP invariant.
5. Project findings: F27, F31, F33, F34, F34b, F35, F44, F45, F48, F49, F53, F54, F91.

*Companion papers: I (substrate), III (mass / $SU(2)_L$), IV (electromagnetism), X (leptons), XI (baryons).*
