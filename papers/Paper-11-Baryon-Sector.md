# Paper XI — The Baryon Sector: The Colour-Singlet Proton, Centre-Phase Closure, the Dynamical Pion, and the First Nucleus

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper XI of XI. Specialises the fermion sector (Paper IX) and the strong force (Paper V) to colour-singlet bound states; uses the NJL constituent-mass machinery of Paper III.*

*New for the eleven-paper series (2026-06-08): the baryon sector is given a dedicated, full treatment — the colour-singlet proton, the centre-phase closure principle, the dynamical pion, the deuteron, and the derived NN repulsive core.*

---

## Abstract

We assemble the baryon sector of the BCC quantum-cellular-automaton model: how confined colour (Paper V) produces colourless, bound, stable matter, from the single proton up to the first nucleus. Five results organise it. First, the proton is the colour-singlet interpolating operator $B=\varepsilon_{abc}\,u^a u^b d^c$, gauge-invariant because $\det V=1$ for $SU(3)$, with exactly zero colour charge ($C_2=0$), the correct quantum numbers ($Q=+1$, $B=1$, $T_3=\tfrac12$), a fully antisymmetric total wavefunction (Fermi statistics via colour-$\varepsilon$ $\times$ spin-flavour-symmetric), and energetic binding from the exact string tension. Second, the baryon's stability is governed by a **centre-phase closure principle**: a colour state is asymptotic iff its $\mathbb Z_3$ centre-phase budget closes (N-ality 0), and a no-go theorem proves the two-body bound-pair fixed point does *not* extend to three constituents — which *predicts* that baryon mass is $\sim99\%$ field energy (the PDG quark sum is $0.96\%$ of $m_p$), the object enforcing the budget (the colour-dielectric condensate) being itself the binder. Third, the pion is delivered as a dynamical $q\bar q$ pseudoscalar Goldstone: massless in the chiral limit (exact), GMOR-linear at the physical point, and reproducing the measured $m_\pi,f_\pi,\langle\bar qq\rangle$ to $0.2$–$4\%$ from a single NJL coupling. Fourth, the deuteron — the first nucleus — binds as a single shallow $J^P=1^+$, $I=0$ state **only** through the pion tensor force, with the exact Rarita–Schwinger tensor strength and the physical $E_b=2.224$ MeV, $\kappa=0.2316$ fm$^{-1}$. Fifth, the short-range NN repulsive core is *derived* from the model's own algebra — quark Pauli antisymmetry plus the chromomagnetic interaction give $+341.8$ MeV at zero separation, with the one external number ($g_\text{cm}$) fixed by the same $N$–$\Delta$ splitting the model already uses. All structural results are verified to machine precision or exact rationals.

---

## 1. Introduction

Baryons are the colour-singlet three-quark bound states; the proton and neutron are the lightest and the building blocks of nuclei. The strong force (Paper V) confines colour and makes the singlet the only finite-energy configuration, but confinement alone does not deliver a proton, a pion, or a deuteron — those are *composite* objects with definite quantum numbers, statistics, masses, and a residual nuclear force. This paper builds them, following the project's matter-binding roadmap from the single hadron (the proton) up to the first nucleus (the deuteron).

The treatment is layered. Section 2 builds the proton as a colour-singlet operator with the right symmetry and an energetic binding argument. Section 3 states the closure principle that governs which colour combinations are stable and *why baryon mass is field energy, not constituent rest mass*. Sections 4–6 build the residual nuclear force from the bottom up: the dynamical pion (the long-range carrier), the deuteron it binds (through the tensor force), and the short-range repulsive core derived from quark substructure. Throughout, the constituent-mass scale and the chiral condensate are inherited from the NJL machinery of Paper III.

---

## 2. The colour-singlet proton

### 2.1 The interpolating operator

The first composite hadron is the colour-singlet baryon operator

$$
B(x)=\varepsilon_{abc}\,q_1^a(x)\,q_2^b(x)\,q_3^c(x),\qquad (q_1,q_2,q_3)=(u,u,d)\ \text{for the proton},
\tag{2.1}
$$

with the totally antisymmetric $SU(3)$ colour tensor $\varepsilon_{abc}$. Under a local gauge rotation $q^a\to V^a{}_{a'}q^{a'}$ with $V\in SU(3)$,

$$
B\to\varepsilon_{abc}V^a{}_{a'}V^b{}_{b'}V^c{}_{c'}\,q^{a'}q^{b'}q^{c'}=\det(V)\,B=B,
\tag{2.2}
$$

because $\det V=1$. The proton is therefore exactly colour-neutral (Finding F71, residual $1.2\times10^{-15}$). The $\varepsilon$ contraction is the unique singlet of $3\otimes3\otimes3=1\oplus8\oplus8\oplus10$; the normalised singlet $|S\rangle=\tfrac1{\sqrt6}\varepsilon_{abc}|abc\rangle$ is annihilated by every total colour generator $G^a=\sum_i T^a_{(i)}$, with quadratic Casimir $C_2|S\rangle=0$ (vs $4/3$ for a single quark, $3$ for the octet) to $1.4\times10^{-16}$.

### 2.2 Quantum numbers and Fermi statistics

The proton $uud$ has $Q=\tfrac23+\tfrac23-\tfrac13=1$, baryon number $B=\tfrac13\cdot3=1$, $T_3=\tfrac12$, all exact via rational arithmetic, with Gell-Mann–Nishijima $Q=T_3+Y/2$ per quark ($Y=\tfrac13$) consistent with the anomaly-free assignment of Paper IX. Fermi statistics are made explicit: with two identical $u$ colour-triplets, $\varepsilon_{abc}u^au^bd^c\equiv0$ unless the rest of the wavefunction supplies the matching symmetry, so the total wavefunction factorises as

$$
\Psi=\underbrace{(\text{colour }\varepsilon)}_{\text{antisymmetric}}\otimes\underbrace{(\text{spin-flavour})}_{\text{symmetric}}\otimes\underbrace{(\text{space, ground})}_{\text{symmetric}}.
\tag{2.3}
$$

The proton spin-up $SU(6)$ spin-flavour wavefunction (the 56-plet symmetric combination, 9 terms) is built explicitly and verified fully $S_3$-symmetric (bit-for-bit). Under any quark transposition the colour part flips sign while spin-flavour and space are even, so $\Psi\to-\Psi$: the proton obeys Fermi statistics exactly.

### 2.3 Energetic binding

Using the exact 2D string tension (Paper V), the cost to pull one quark a distance $R$ out of the singlet is $V(R)=\sigma(\beta)R$, strictly linear and unbounded (at $\beta=2.0$, $\sigma=2.051$, giving $V=2.05,4.10,8.20,\dots$). The colour singlet is the finite-energy configuration; an isolated quark costs infinite energy. Confinement ($\sigma>0$) plus the colour singlet together answer both halves of "why no free quarks, and why a proton exists." This is an operator-level construction with an energetic binding argument; a real-time three-body flux-tube bound state (and the calibrated proton mass) is roadmap phase P2, not claimed here.

---

## 3. The centre-phase closure principle and the origin of baryon mass

### 3.1 Closure governs stability

The pair sector (Paper III §6 / Finding F92) obeys a closure law: a two-constituent bound state is stable at the unique angle where its unitarity phase budget closes, and the object enforcing the budget *is* the binder. The baryon sector obeys the *same grammar* with a different budget — the $\mathbb Z_3$ **centre phase** (Findings F97/F98):

> **Closure principle.** A stable composite is a configuration whose phase budget closes exactly; the object enforcing the budget is itself the binding agent. Non-closure is priced either by over-wrap (kinematic instability, the pair sector) or linearly in separation (confinement, the colour sector).

The closure arithmetic is exact: $qqq$ gives $3\times\tfrac{2\pi}3=2\pi\equiv0$ (closed), $q\bar q$ gives $0$ (closed), but a diquark $qq$ gives $\tfrac{4\pi}3\not\equiv0$ (open — confined, never asymptotic). The enforcer/binder identification is exact (Finding F98): the centre charge $n$ is simultaneously the **budget label** (N-ality 0 $\Leftrightarrow$ asymptotic) and the **binder coefficient** (the multiplier of the dual-superconductor flux-tube tension $\sigma_\text{BPS}=2\pi v^2|n|$, Paper V §4), so $\sigma=0$ exactly when the budget closes and $\sigma>0$ otherwise. Only N-ality-0 combinations appear as asymptotic states — $qqq$, $q\bar q$, pentaquark, hexaquark, hybrids — a selection rule that matches every observed hadron and would be falsified by any free quark, free diquark, or fractionally-charged asymptotic state.

### 3.2 The no-go: baryon mass is field energy

Extending the F92 two-body fixed point to three constituents fails as an exact theorem (Finding F97). The F92 triple coincidence — amplitude unitarity, composite-mass peak, and phase wrap all meeting at $45^\circ$ — holds *only* for $N=2$: the caps $\sin(\pi/2N)=N^{-1/2}$ coincide at $N=1,2$ and split strictly for $N\ge3$. For $N=3$ a forbidden gap $(30^\circ,35.264^\circ)$ opens between the per-constituent wrap cap ($m_c\le\tfrac12$ exactly) and the unitarity cap, and both candidate three-body fixed points (trilinear $m=y^3$ and bilinear $m=y^2$) land inside it — allowed by unitarity, killed by over-wrap. **No three-constituent state can be a phase-kinematic bound state.**

This no-go is itself a successful prediction: if the baryon sat at a phase fixed point its mass would be bounded by the constituent rest-phase sum, but the measured proton has

$$
\frac{2m_u+m_d}{m_p}=\frac{2(2.16)+4.67}{938.272}=0.96\%\qquad(\text{PDG }\overline{\rm MS},\ 2\ \text{GeV}).
$$

Baryon mass is $\sim99\%$ **field energy** — set by the string tension $\sigma$ and the colour-dielectric condensate, not by constituent rest mass. The split in the model matches the split in nature: the lepton sector (no colour, no confinement) is exactly where the phase chain *can* close (Paper X, Koide $Q=\tfrac23$); the baryon sector is exactly where it *cannot*. The model also predicts there is **no** exact constituent-phase baryon-mass relation of the Koide type.

---

## 4. The dynamical pion: the $q\bar q$ pseudoscalar Goldstone

The residual nuclear force at long range is one-pion exchange, so the baryon sector needs a dynamical pion. It is delivered (Finding F103) by reusing the NJL gap + RPA ladder of Paper III with no new free physics: one coupling $G$ generates the constituent mass via the gap equation $M=m_0+4GN_cN_fM\,I_1(M)$ and, summed in the $q\bar q$ ladder, fixes the meson poles $1-2G\Pi_M(q^2)=0$. The pseudoscalar pole is the pion, the scalar pole its chiral partner $\sigma$.

- **Goldstone theorem (exact).** In the chiral limit ($m_0\to0$), $1-2G\Pi_\text{PS}(0)=0$ is *identically* the gap equation (residual $2.3\times10^{-14}$), so the pion is the exact massless Goldstone ($m_\pi=0$ to $1.6\times10^{-7}$).
- **Polarization split (exact).** $\Pi_S-\Pi_\text{PS}=-8N_cN_fM^2K(q^2)$ to $1.8\times10^{-16}$.
- **Calibrated spectrum.** $m_c=311.2$, $m_\pi=140.5$, $f_\pi=92.6$, $\langle\bar qq\rangle^{1/3}=-249.1$ MeV — matching measurement to $0.2$–$4.2\%$; the $\sigma$ partner sits at $2m_c$ (ratio $1.0000$).
- **GMOR.** $m_\pi^2 f_\pi^2=-m_0\langle\bar qq\rangle$ to $0.39\%$; the Goldstone scaling $m_\pi^2\propto m_0$ is flat to $0.86\%$ — the defining signature.
- **Real-space bound state.** The relative-coordinate $q\bar q$ bound state agrees with dense diagonalisation to $1.3\times10^{-15}$.

The pion is thus an anomalously light, certified dynamical Goldstone, with its mass and $\pi NN$ coupling (via Goldberger–Treiman, $g_{\pi qq}f_\pi=M$ to $1.1\%$) ready to drive the nuclear force.

---

## 5. The deuteron: the first nucleus, bound by the pion tensor force

The deuteron is the proton–neutron bound state and the simplest nucleus. Its construction (Finding F104) generalises the two-body solver to the two coupled partial waves $^3S_1$–$^3D_1$ of the $J^P=1^+$, $I=0$ channel, with the static one-pion-exchange potential

$$
V_\pi(r)=-\frac{f^2}{4\pi}\,m_\pi\big[(\boldsymbol\sigma_1\!\cdot\!\boldsymbol\sigma_2)Y(x)+S_{12}T(x)\big],\quad x=\frac{m_\pi r}{\hbar c},
\tag{5.1}
$$

with $Y(x)=e^{-x}/x$, $T(x)=(1+3/x+3/x^2)e^{-x}/x$, and the tensor operator $S_{12}=3(\boldsymbol\sigma_1\!\cdot\!\hat n)(\boldsymbol\sigma_2\!\cdot\!\hat n)-\boldsymbol\sigma_1\!\cdot\!\boldsymbol\sigma_2$ that mixes $L=0$ and $L=2$.

**The headline result is that the deuteron binds *only* through the pion tensor force.** At a fixed core radius the full $^3S_1$–$^3D_1$ OPEP binds ($-2.00$ MeV) while central-only OPEP is unbound ($+0.66$ MeV): the tensor $L=0\leftrightarrow L=2$ coupling supplies the missing attraction — the textbook reason the deuteron exists. The tensor strength is certified exactly: the spin-angular $\langle S_{12}\rangle$ matrix built from Clebsch–Gordan + spinor-spherical-harmonic quadrature equals the Rarita–Schwinger form $\left[\begin{smallmatrix}0&2\sqrt2\\2\sqrt2&-2\end{smallmatrix}\right]$ to $9.8\times10^{-15}$, the off-diagonal $2\sqrt2$ being exactly the mixing that binds. The result is a single shallow bound state, $J^P=1^+$, $I=0$, with a few-percent tensor-induced D-state ($P_D\approx7\%$, vanishing when the tensor is switched off), and the $^3S_1$ tail reproducing $\kappa=\sqrt{M_N E_b}/\hbar c$ to $0.34\%$. Tuned to the physical $E_b=2.224$ MeV, the model returns the physical $\kappa=0.2316$ fm$^{-1}$. The carrier $m_\pi$ is the Paper-III/§4 model output; the external numbers are the $\pi NN$ coupling via Goldberger–Treiman (one number, $g_A$) and $M_N$ (absolute scale, roadmap P2/P6).

---

## 6. The short-range NN repulsive core, derived

The deuteron build initially used a *tuned* hard core to regularise the $1/x^3$ tensor singularity — the one ingredient the roadmap flagged as not yet derived. Finding F113 supplies it from the model's own first principles, with no new free physics.

A nucleon is a colour-singlet of three genuine CA fermions ($\varepsilon_{abc}$ colour-antisymmetric $\times$ $SU(6)$ spin-flavour-symmetric). Two nucleons pushed together are **six identical fermions**, so the total six-quark wavefunction must be antisymmetric. Pauli antisymmetry forces the two clusters into the spatially-symmetric $[6]$ colour-spin configuration, which is **chromomagnetically unfavourable** — its colour-spin energy sits far above two free nucleons. The overlap therefore costs energy. The colour-magnetic interaction is built from the model's own generators through exact $SU(N)$ Fierz swap identities (everything rational, avoiding the chiral-transform numerical hazard):

$$
\boldsymbol\lambda_i\!\cdot\!\boldsymbol\lambda_j=2P^c_{ij}-\tfrac23,\quad \boldsymbol\sigma_i\!\cdot\!\boldsymbol\sigma_j=2P^s_{ij}-1,\quad H_\text{CM}=-\sum_{i<j}(\boldsymbol\lambda_i\!\cdot\!\boldsymbol\lambda_j)(\boldsymbol\sigma_i\!\cdot\!\boldsymbol\sigma_j)\ [g_\text{cm}].
\tag{6.1}
$$

The single coupling $g_\text{cm}$ is fixed by the measured $N$–$\Delta$ splitting, $M_\Delta-M_N=16\,g_\text{cm}=293$ MeV $\Rightarrow g_\text{cm}=18.31$ MeV — the *same* coupling the model already uses for baryon mass splittings, not a new parameter. The exact six-quark RGM norm kernel gives $n(R{=}0)=20/9>0$, so the deuteron channel is **not** Pauli-forbidden (consistent with the deuteron existing), and the repulsion is the dynamical chromomagnetic one: **$+341.8$ MeV at zero separation** (exact given $g_\text{cm}$), falling monotonically to zero over the quark-overlap range. Re-binding the deuteron with this derived core (no hard wall) returns the physical $E_b=2.224$ MeV, $\kappa=0.2316$ fm$^{-1}$, a single bound $1^+$ state, with the tensor still essential (16/16 PASS). The one remaining tuned quantity is the physical quark size $b\approx0.41$ fm, not an ad-hoc wall radius.

---

## 7. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| Colour-singlet gauge invariance $B\to\det(V)B$ | §2.1 | $1.2\times10^{-15}$ |
| Zero colour charge, $C_2|S\rangle=0$ | §2.1 | $1.4\times10^{-16}$ |
| Proton $Q,B,T_3$ exact | §2.2 | $0$ (rational) |
| Spin-flavour $S_3$-symmetry; full $\Psi$ antisymmetric | §2.2 | $0$ (bit-for-bit) |
| Linear binding $V(R)=\sigma R$ | §2.3 | $0$ (exact area law) |
| $\mathbb Z_3$ closure ($qqq,q\bar q\to0$; $qq\to4\pi/3$) | §3.1 | exact (integer) |
| Enforcer = binder ($\sigma=0$ iff N-ality 0) | §3.1 | exact / BPS Tier-1 |
| Three-constituent no-go (over-wrap gap) | §3.2 | exact (50 dp) |
| Quark-sum/$m_p=0.96\%$ (baryon mass = field energy) | §3.2 | quantitative |
| Pion Goldstone (chiral limit) | §4 | $2.3\times10^{-14}$ |
| GMOR / Goldstone scaling | §4 | $0.39\%$ / $0.86\%$ |
| Deuteron tensor strength $\langle S_{12}\rangle=$ R–S | §5 | $9.8\times10^{-15}$ |
| Deuteron binds only via tensor; $E_b=2.224$ MeV | §5 | $-2.00$ vs $+0.66$ MeV; $2\times10^{-5}$ |
| NN core $+341.8$ MeV from quark Pauli + CM | §6 | exact (rational, given $g_\text{cm}$) |
| Derived-core re-binding | §6 | 16/16 PASS |

Underlying findings: F71 (colour-singlet proton), F86/F88/F94 (confinement / condensate), F97 (centre-phase no-go), F98 (enforcer = binder), F103 (dynamical pion), F104 (deuteron / tensor force), F113 (NN repulsive core).

---

## 8. Discussion and scope

The baryon sector closes the matter content: confined colour (Paper V) produces a colour-neutral, correctly-charged, Pauli-consistent proton; a centre-phase closure principle governs which colour states are stable and *predicts* that baryon mass is field energy rather than constituent rest mass; and the residual nuclear force is built bottom-up — a dynamical pion Goldstone, the deuteron it binds through the tensor force, and a short-range repulsive core derived from quark substructure rather than tuned. The lepton/baryon contrast is structural: the phase chain closes for the colourless leptons (Koide) and provably cannot for the three-quark baryon, matching nature's split.

The honest scope is the matter-binding roadmap's remaining phases. P2 (a dynamical, real-time three-quark baryon with a measured mass, beyond the operator-level proton and energetic binding argument) is open; the proton mass and QCD scale $\Lambda$ are Tier-B calibration. P5 (atoms / hydrogen — binding a proton and electron electromagnetically) and the cross-cutting P6 (SI absolute scale via the Paper-VII cell) complete the chain from substrate to nucleus to atom. None of these affects the verified structure delivered here: the proton, the closure principle, the pion, the deuteron, and the derived NN core all stand at machine precision or exact rationals.

---

## References

1. M. Gell-Mann, "Symmetries of Baryons and Mesons," *Phys. Rev.* **125**, 1067 (1962); "A schematic model of baryons and mesons," *Phys. Lett.* **8**, 214 (1964).
2. Y. Nambu, G. Jona-Lasinio, *Phys. Rev.* **122**, 345 (1961) — dynamical chiral symmetry breaking / the pion.
3. M. Gell-Mann, R. Oakes, B. Renner, *Phys. Rev.* **175**, 2195 (1968) — GMOR relation.
4. H. Yukawa, "On the interaction of elementary particles," *Proc. Phys.-Math. Soc. Japan* **17**, 48 (1935) — one-pion exchange.
5. M. Oka, K. Yazaki, *Prog. Theor. Phys.* **66**, 556 (1981); A. Faessler *et al.* — quark-Pauli / colour-magnetic origin of the NN repulsive core.
6. Particle Data Group, *Review of Particle Physics* (2024) — quark and hadron masses; deuteron $E_b$.
7. Project findings: F71, F86, F88, F94, F97, F98, F103, F104, F113.

*Companion papers: III (NJL constituent mass / pion machinery), V (strong force / confinement / closure), IX (fermion content), X (lepton/baryon closure contrast).*
