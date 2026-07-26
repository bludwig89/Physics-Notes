# Paper IX — The Lepton Sector: Higgs-Free Hypercharge, the Koide Equipartition as an Electromagnetically-Selected $45^\circ$ Critical Point, and the See-Saw Neutrino

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper IX of XI. Specialises the fermion sector (Paper VIII) to the colourless leptons; builds on Papers III (mass / Koide), VI (weak isospin), and the Majorana extension of the weak sector.*

*New for the eleven-paper series (2026-06-08): the ten-paper draft folded leptons into the fermion paper; this paper gives the charged-lepton and neutrino sectors a dedicated, full treatment.*

*Revision (2026-07-01): re-issued as Paper IX (was Paper X) following the deprecation of the horizon-free "dielectric black hole" paper and the consequent renumbering of Papers IX–XIII down by one.*

---

## Abstract

We assemble the lepton sector of the BCC quantum-cellular-automaton model: the colourless, $SU(2)_L$-charged fermions whose masses arise — like all masses in the model — from the chiral mass step of Paper III, with no Higgs field. Three results organise the sector. First, hypercharge is carried Higgs-free: the right-handed singlets are dynamical $U(1)_Y$ fields whose hypercharge difference $\Delta Y=Y_L-Y_R$ is absorbed onto the same gauge field $U(\mathbf x)$ that carries the mass phase, so no scalar is needed and a pure $\nu_L$ state carries $T_3=+\tfrac12$ exactly. Second, the charged-lepton masses obey the Koide relation $Q=\sum m/(\sum\sqrt m)^2=2/3$ to $0.91\sigma$ ($Q=0.6666605$), which we show is exactly a $45^\circ$ equipartition of the cubic amplitude $\sqrt m=y$ via the closed map $Q(\phi)=1/(3\cos^2\phi)$; the use of $\sqrt m$ is the Cooper-pair bilinear $m=y^2$, the $45^\circ$ is the *same* $SO(2)$ equipartition that caps the bound pair, and electromagnetism is the *selector* that puts only the colour-free, charged leptons on the critical point (quarks are pushed off by QCD; neutrinos are neutral and unpinned). Third, the neutrino acquires a small mass through a Higgs-free Majorana mass step on $\nu_R$: the QCA Majorana step is exactly R-unitary, lepton-number-violating, gauge-allowed only for $Y_{\nu_R}=0$, and combined with the chiral Dirac mass reproduces the see-saw $m_\nu\approx M_D^2/M_R$ to machine precision across $M_R/M_D\in[3,10^5]$ — explaining the smallness of the neutrino mass with a single large scale rather than an unnaturally tiny coupling. All structural results are verified to machine precision; the one honest residual (the *magnitude* of the $45^\circ$ rotation) is recorded.

---

## 1. Introduction

Leptons are the colourless half of the matter content: the charged leptons $e,\mu,\tau$ (electric charge $-1$, weak isospin doublet partners of the neutrinos) and the neutrinos $\nu_e,\nu_\mu,\nu_\tau$ (neutral). In the Standard Model their masses come from Yukawa couplings to the Higgs, and the smallness of the neutrino mass is either an unexplained tiny Yukawa or a see-saw involving a heavy right-handed Majorana scale. The lepton sector is also where the most precise unexplained mass relation in particle physics lives: the Koide relation $Q=\tfrac23$, which the charged leptons satisfy to one part in $10^5$ but which has no SM explanation.

This paper treats all three pieces on the model's Higgs-free footing. Section 2 fixes the lepton field content and the Higgs-free hypercharge. Section 3 derives the Koide relation as a cubic-vector equipartition and identifies its $45^\circ$ amplitude with the bound-pair stability cap. Section 4 builds the Higgs-free Majorana/see-saw neutrino. Section 5 states the electromagnetic selection rule that explains why *only* the charged leptons equipartition. The lepton sector inherits the three-generation $T_{1u}$ structure and the spherical mass shell from Paper VIII, and the chiral $SU(2)_L$ from Paper VI.

---

## 2. The lepton doublet and Higgs-free hypercharge

The first-generation leptons are the left-handed doublet $L=(\nu_e,e)_L$ with $Y_L=-1$, the right-handed charged singlet $e_R$ with $Y_{e_R}=-2$, and the right-handed neutral singlet $\nu_R$ with $Y_{\nu_R}=0$ (Paper VIII, §5). Electric charge follows from Gell-Mann–Nishijima $Q=T_3+Y/2$, exact per state.

In the SM the right-handed singlets get their hypercharge coupling to the photon/$Z$ through the Higgs Yukawa structure. Here there is no Higgs, so the hypercharge must be carried directly. Finding F41 shows this is consistent: the chiral mass step that couples $\eta_L\leftrightarrow\chi_R$ changes hypercharge by $\Delta Y=Y_L-Y_R$, and that difference is absorbed onto the *same* $SU(2)$ gauge field $U(\mathbf x)$ that carries the complex-mass phase. The right-handed singlets are then promoted to genuinely dynamical $U(1)_Y$-coupled fields by a Stueckelberg-wrapped kinetic half-step (Finding F42), whose $U(1)_Y$ Ward identity holds to $1.8\times10^{-15}$. The net effect: the full lepton hypercharge structure is reproduced with no scalar, and a pure $\nu_L$ state carries $T_3=+\tfrac12$ to $1.1\times10^{-16}$. The would-be Higgs vacuum direction is the pure-gauge field $U(\mathbf x)$ of Paper III, not a physical boson.

---

## 3. The charged-lepton masses: the Koide relation as a $45^\circ$ equipartition

### 3.1 Koide as cubic-vector equipartition

The three charged leptons fill the cubic vector irrep $T_{1u}$ of $O_h$ (Paper VIII, §3). Form the amplitude vector $\mathbf y=(\sqrt{m_e},\sqrt{m_\mu},\sqrt{m_\tau})$ and decompose it into its democratic ($A_{1g}$, along $\hat n=(1,1,1)/\sqrt3$) and traceless ($T_{1u}$) parts. Writing $\phi$ for the angle between $\mathbf y$ and $\hat n$, the perpendicular part contributes nothing to the signed sum, so $\sum y=\sqrt3\,|\mathbf y|\cos\phi$ and $\sum y^2=|\mathbf y|^2$, giving the **exact closed map** (Finding F80)

$$
\boxed{\;Q(\phi)\equiv\frac{\sum y^2}{(\sum y)^2}=\frac{\sum m}{(\sum\sqrt m)^2}=\frac{1}{3\cos^2\phi}\;}
\tag{3.1}
$$

with three landmark angles:

| $\phi$ | $Q$ | meaning |
|---|---|---|
| $0^\circ$ | $1/3$ | democratic floor (degenerate generations) |
| $\mathbf{45^\circ}$ | $\mathbf{2/3}$ | **equipartition — the charged-lepton point** |
| $54.7356^\circ=\arccos\tfrac1{\sqrt3}$ | $1$ | single-axis ceiling (one massive generation) |

The measured charged leptons give $Q=0.6666605$ ($0.91\sigma$ from $\tfrac23$), $\phi_\text{lepton}=44.99974^\circ$, $|A_{1g}|^2/|T_{1u}|^2=1.00002$, coefficient of variation $\mathrm{CV}(y)=0.99999$. So $Q=\tfrac23$ is *exactly* a $45^\circ$ rotation of the mass amplitude away from democracy, equivalently the equal-weight condition $|A_{1g}|=|T_{1u}|$. It is also the exact midpoint of the allowed range, $Q=\tfrac23=\tfrac12(\tfrac13+1)$ — the maximally balanced point between "all generations equal" and "only one generation exists" (Finding F78).

### 3.2 Predictivity

$Q=\tfrac23$ plus two masses overdetermines the third:

$$
m_\tau^\text{pred}=1776.97\,\text{MeV}\quad\text{vs}\quad m_\tau^\text{PDG}=1776.86\pm0.12\,\text{MeV}\ (6.1\times10^{-5}).
\tag{3.2}
$$

(We re-verified $Q=0.6666605$ from the PDG masses $m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV for this paper.)

### 3.3 Why $\sqrt m$: the Cooper-pair bilinear

The amplitude coordinate is $\sqrt m$, not $m$, because the model treats the symmetry-breaking sector as superconductor-like: the would-be Higgs is a Cooper pair (Papers II–III). Applying the same premise to fermion mass, generation $a$'s mass is a pair condensate, a bilinear in the constituent amplitude $y_a$:

$$
m_a\propto\langle y_a y_a\rangle=y_a^2\;\Longrightarrow\;\sqrt{m_a}=y_a=\text{the }T_{1u}\text{ vector component on axis }a.
\tag{3.3}
$$

Koide is then a statement about the amplitude $y$, not the mass, precisely because mass is quadratic in the pairing amplitude (Finding F78, Part A — a derivation, not a fit). The data independently single out the bilinear power: the participation ratio $(\sum m^s)^2/\sum m^{2s}$ is the clean rational $3/2$ only at $s=\tfrac12$ (measured $1.500014$; neighbours $1.834$ at $s=\tfrac13$, $1.119$ at $s=1$).

### 3.4 The $45^\circ$ is the bound-pair cap — one $SO(2)$ rotation

The $45^\circ$ of Koide is the *same* equipartition angle that caps a two-constituent bound state (Finding F73, used in Paper X). Both of the model's mass "rotations" are a unit 2-vector turned by an angle, whose two squared weights $(\cos^2,\sin^2)$ become equal at $45^\circ$:

- **Constituent (bound-pair) level:** the constituent carries $(n_c,m_c)=(\cos t,\sin t)$ (kinetic complement and rest mass). The pair phase $\Omega_\text{pair}=2t$ saturates the stability bound $\Omega=\pi/2$ exactly at $t=45^\circ$, i.e. $m_c=1/\sqrt2$, where rest and kinetic weights equipartition.
- **Generation level:** the amplitude carries $(\text{common},\text{diff})=(\cos\phi,\sin\phi)$ ($A_{1g}$ vs $T_{1u}$); Koide equipartition is $\phi=45^\circ$.

Numerically the two states are the identical $45^\circ$-rotated unit vector $(1/\sqrt2,1/\sqrt2)$, with the pair phase exactly $\pi/2$ there (Finding F80, D2). The constituent-level $45^\circ$ and the generation-level $45^\circ$ are one and the same $SO(2)$ equipartition, appearing once per level. Finding F81 sharpens the value: $45^\circ$ is the two-constituent pair's half of the $\pi/2$ phase budget — the spin-0 Cooper singlet $(\uparrow\downarrow-\downarrow\uparrow)/\sqrt2$ is itself a maximally-mixed $45^\circ$ state, and the generation equipartition is plausibly the image of that internal structure.

---

## 4. The neutrino sector: a Higgs-free see-saw

### 4.1 The Majorana mass step

A singlet $\nu_R$ admits a bare Majorana mass $\mathcal L_M=-\tfrac12 M_R(\nu_R^T\varepsilon\nu_R+\text{h.c.})$, $\varepsilon=i\sigma^2$. In QCA form the Majorana step on one Weyl singlet is the closed-form integration of the BdG equations of motion $i\partial_t\chi_u=+M_R\chi_d^*$, $i\partial_t\chi_d=-M_R\chi_u^*$:

$$
\boxed{\;\chi_u'=c_M\chi_u-is_M\chi_d^*,\qquad \chi_d'=c_M\chi_d+is_M\chi_u^*,\;}\qquad c_M=\cos(M_R\,dt),\ s_M=\sin(M_R\,dt).
\tag{4.1}
$$

The step is **anti-linear** (couples $\chi$ to $\chi^*$) — intrinsic to a Majorana mass and the source of lepton-number violation. It is exactly R-unitary on the four real degrees of freedom ($|\chi_u'|^2+|\chi_d'|^2=|\chi_u|^2+|\chi_d|^2$; verified over $M_R\in[0,10^6]$, $dt\in[0.05,1.27]$, 200-step compose, residual $2.3\times10^{-11}$). The $U(1)_Y$ selection rule is exact: the bilinear $\chi^T\varepsilon\chi$ picks up $e^{i\beta Y_{\nu_R}}$, so the step is gauge-invariant **iff $Y_{\nu_R}=0$** — the *same* hypercharge constraint that forbids a Higgs scalar, now forcing $\nu_R$ to be a $Y=0$ singlet for a Majorana mass to exist (Finding F47). In the SM this is presented as a coincidence of the hypercharge assignment; here it is a consequence of one structural choice.

### 4.2 See-saw scaling

Combined with the chiral Dirac mass step, the $(\nu_L,\nu_R^c)$ sector has the canonical see-saw matrix and eigenvalues

$$
M=\begin{pmatrix}0&M_D\\M_D&M_R\end{pmatrix},\qquad \lambda_\pm=\frac{M_R\pm\sqrt{M_R^2+4M_D^2}}{2},\qquad |\lambda_-|\xrightarrow{M_R\gg M_D}\frac{M_D^2}{M_R}.
\tag{4.2}
$$

The lattice (8$\times$8 BdG) light eigenvalue matches the closed form to $\le10^{-12}\,M_R$, and the see-saw scaling $m_\nu\cdot M_R/M_D^2\to1$ holds within the next-order $(M_D/M_R)^2$ bound at every sampled ratio $M_R/M_D\in\{3,10,30,\dots,10^5\}$ (Finding F47, M1–M6, 6/6). Concretely, with $M_D\sim m_e$ and $M_R\sim10^{12}$–$10^{15}$ GeV, the see-saw produces $m_\nu\sim10^{-2}$–$10^{-5}$ eV — the observed range — automatically. **The smallness of the neutrino mass is explained Higgs-free, by a single large scale $M_R$ rather than an unnaturally tiny Yukawa.**

### 4.3 Three generations and mixing (outlook)

The single-flavour block generalises to a $3\times3$ Dirac matrix $M_D$ and a $3\times3$ Majorana matrix $M_R$; the $6\times6$ see-saw then yields three light (active) and three heavy (sterile) neutrinos, with PMNS mixing from the diagonalisation. The large *leptonic* mixing (near tribimaximal PMNS), in contrast to the small quark CKM mixing, is the democratic signature of the neutral sector — consistent with the neutrinos sitting *off* the charged-lepton critical point (§5). A full $3\times3$ build is flagged as the natural next step.

---

## 5. Why only the charged leptons equipartition: the electromagnetic selection rule

The charged leptons sit exactly at the $45^\circ$ critical point; the quarks and neutrinos do not. The model's answer (Finding F80) is that **electric charge selects the sector**: only the charged leptons are simultaneously EM-coupled *and* colour-free, so only they land on the clean abelian critical point.

| sector | EM coupling | $Q$ | at $2/3$? |
|---|---|---|---|
| charged leptons $e,\mu,\tau$ | full ($q=-1$), no colour | $0.66666$ | **yes ($45^\circ$)** |
| up-type quarks $u,c,t$ | $q=+\tfrac23$, **+ colour/QCD** | $0.849$ | no |
| down-type quarks $d,s,b$ | $q=-\tfrac13$, **+ colour/QCD** | $0.731$ | no |
| neutrinos $\nu$ | none ($q=0$; Majorana/see-saw) | ordering-dependent $0.34$–$0.59$ | no (unpinned) |

Quarks carry the EM rotation too, but their mass dynamics are dominated by the non-abelian QCD condensate, which pushes them off the clean EM point — and the two quark charges give two *different* $Q$'s ($0.85\neq0.73$), so there is no universal value. Neutrinos have no EM rotation at all, so nothing pins them to $\tfrac23$, and indeed their Koide ratio is not yet well-defined (it swings with the unknown lightest mass and ordering).

**The honest residual.** Electromagnetism explains *which* sector sits at the critical point, but not the *magnitude* of the rotation. A perturbative EM self-energy supplies only $\Delta\phi_\text{EM}\sim\alpha/\pi=0.13^\circ$, whereas the rotation from democracy to equipartition is a full $45^\circ$ — a factor $\sim340$ too weak. The value $45^\circ$ is therefore a *non-perturbative critical/saturation condition*, pinned by the data and by the recurring $1/\sqrt2$ of the Cooper-pair singlet, but not yet derived from a non-perturbative EM-driven gap. This is the single sharpest open problem of the lepton sector, and we record it rather than overclaim.

---

## 6. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| $T_3=+\tfrac12$ for pure $\nu_L$ (Higgs-free $Y$) | §2 | $1.1\times10^{-16}$ |
| $U(1)_Y$ Ward identity (Stueckelberg kinetic) | §2 | $1.8\times10^{-15}$ |
| Koide map $Q(\phi)=1/(3\cos^2\phi)$; $45^\circ\to\tfrac23$ | §3.1 | exact at $0/45/54.74^\circ$ |
| Charged-lepton $Q$ | §3.1 | $0.6666605$ ($0.91\sigma$) |
| Bilinear power $s=\tfrac12$ uniquely clean | §3.3 | $1/Q=1.500014$ |
| $SO(2)$ unification of F73 cap & Koide $45^\circ$ | §3.4 | identical $(1/\sqrt2,1/\sqrt2)$; $\Omega_\text{pair}=\pi/2$ |
| $m_\tau$ prediction | §3.2 | $6.1\times10^{-5}$ |
| Majorana step R-unitarity | §4.1 | $2.3\times10^{-11}$ |
| $U(1)_Y$ selection $Y_{\nu_R}=0$ | §4.1 | $0$ exact at $Y=0$ |
| See-saw scaling $m_\nu\to M_D^2/M_R$ | §4.2 | within $(M_D/M_R)^2$ bound, all ratios |
| BdG light eigenvalue vs closed form | §4.2 | $\le10^{-12}M_R$ |
| EM selection contrast (leptons/quarks/$\nu$) | §5 | $0.667$ vs $0.85,0.73$, unpinned |

Underlying findings: F41 (Higgs-free hypercharge), F42 (dynamical $\chi$ kinetic), F47 (Majorana see-saw), F78 (Koide amplitude / Cooper bilinear), F80 (45° / EM selection), F81 ($45^\circ$ as half the phase budget), F75/F76 (three generations / hierarchy).

---

## 7. Discussion

The lepton sector ties together three of the model's signatures. Hypercharge is Higgs-free because it rides the same gauge field as the mass phase. The Koide relation — the most precise unexplained lepton mass relation — becomes an exact statement: $Q=\tfrac23$ is the $45^\circ$ equipartition of the cubic amplitude $\sqrt m$, the same $SO(2)$ equal-split that caps the bound pair, and electromagnetism is the rule that selects the colour-free charged sector to sit there. The neutrino mass is small for the see-saw reason, realised Higgs-free with the $Y_{\nu_R}=0$ constraint structural rather than coincidental.

Two open problems are stated sharply: (i) the *magnitude* of the $45^\circ$ Koide rotation is a non-perturbative critical condition not yet derived (perturbative EM is $\sim340\times$ too weak); (ii) the full $3\times3$ Dirac+Majorana neutrino build, with PMNS mixing, is not yet done. Neither affects the verified structure of the sector.

---

## References

1. Y. Koide, "New view of quark and lepton mass hierarchy," *Phys. Rev. D* **28**, 252 (1983); *Lett. Nuovo Cimento* **34**, 201 (1982).
2. P. Minkowski, *Phys. Lett. B* **67**, 421 (1977); M. Gell-Mann, P. Ramond, R. Slansky (1979); T. Yanagida (1979); R. N. Mohapatra, G. Senjanović, *Phys. Rev. Lett.* **44**, 912 (1980) — see-saw mechanism.
3. Y. Nambu, "Quasi-particles and gauge invariance in the theory of superconductivity," *Phys. Rev.* **117**, 648 (1960) — pairing / BdG.
4. Particle Data Group, *Review of Particle Physics* (2024) — charged-lepton and neutrino mass data; PMNS.
5. Project findings: F41, F42, F47, F73, F75, F76, F78, F80, F81.

*Companion papers: III (mass / Koide), VI (weak isospin / Majorana extension), VIII (fermion structure / generations), X (baryons / bound-pair cap).*
