% A Universe in a Bottle — Claims and Falsifiers
% B. Ludwig (independent researcher)
% 2026-08-27 (revision 7; first issued 2026-06-08)

> **Revision 7 — 2026-08-27.** One **status change**, no new claim. Claim 13 (the Born rule via Gleason) moves from `contingent` to `live`: F304 §5.5 had named one external step — that a non-negative frame function is automatically continuous, cited to the Cooke-Keane-Moran (1985) regularity lemma without being reproved. F329 closes it by showing the identical proposition is already Theorem 2.8 of Gleason's own 1957 paper, the same primary source whose *other* half F304 §5 already independently re-derives, needing nothing beyond non-negativity and compactness of the sphere — no appeal to Cooke-Keane-Moran's separate, later, lower-prerequisite proof of the same fact was required or made. Verified for every dimension the model builds a Born-rule measurement context on.

> **Revision 6 — 2026-08-26.** One **narrowing** and one **addition**, and they are the same
> result seen from two sides. F327 did the confrontation claim 15 said had not been done: the
> chiral $O(\lvert k\rvert^2)$ Lorentz defect, converted through the F79/F107 ruler, is a local
> dimension-5 CPT-odd operator with a parameter-free $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}\,3^{1/4}/9=1.4662$,
> and the LHAASO/Crab electron limits exclude it by **7.05 decades**. **(i)** Claim 15 is
> **narrowed** to its structural, per-channel content — the defect is still one scalar and its
> order still follows from the branch structure — and the sentence saying the claim was "not yet
> observationally constrained" is withdrawn. **(ii)** The exclusion itself becomes **claim 19**:
> this model may not assign an elementary matter field to a single BCC chiral branch. It is a
> `no_go`, it fires CL262's own falsifier 1, and it localises on exactly one leg — F301's algebra,
> F91's classification and F246's photon coefficient are all untouched, and the same ruler leaves
> the photon fine, which is why F28 passed. **This is the first claim in this document that a
> measurement has taken away.** It is published here in the same revision that recorded it.

> **Revision 5 — 2026-08-18.** One **withdrawal of a non-claim**, seven **additions**, one
> **correction**, and one **structural** change. **(i)** The Scope entry "$m_W$ and $m_Z$ in absolute terms are not
> predicted" is **withdrawn**. F320 (2026-08-16) derives both absolutely; the boundary had been
> drawn in the wrong place, because the premise ("$v$ is an anchor") was true and the conclusion
> did not follow from it. The masses become **core claim 12**, carrying $\rho=1$ with them.
> **(ii)** Seven results issued since revision 4 are added as **claims 12–18**, with their
> falsifiers: the electroweak masses, the Born rule via Gleason, exact no-signalling, the
> finite-$a$ Lorentz defect, the UV sector, linear structure formation, and the primordial tilt.
> **(iii)** The $\alpha_s(M_Z)$ row is **corrected**, not in value but in what it omitted: $0.11955$
> is the H1 (centre-normalised) branch of an unclosed colour-normalisation fork, and the other
> branch gives $0.03970$. Quoting the $2.1\sigma$ without the branch overstated it.
> **(iv)** Revision 4 made this document a *summary* of `docs/claims/` rather than the register —
> and then the register moved without the summary following, which is how a withdrawn claim stayed
> published for two days. So every claim, falsifier and scope entry below now carries a
> machine-checked anchor naming the card it stands on **and the status it is recording it at**.
> `make citations` fails when the two disagree, and when a headline card never reaches this page at
> all. The check is `tools/check_summary_claims.py`; the CL016 miss is its selftest fixture.

> **Revision 4 — 2026-08-04 - 23:55.** Two changes, one an **addition** and one
> **structural**. **(i)** The charged-lepton **shape angle** is added as core claim 11.
> $\delta^*=\tfrac29$ rad has been a *founding principle* of the model since
> 2026-07-16 (F253/F255/F256), and revision 3 — issued seventeen days later — did not
> carry it. That gap is the reason for the second change. **(ii)** This document is no
> longer the register. Every claim below now has a **card** in `docs/claims/`, with a
> status, a falsifier field, and the findings it rests on; `claims-index.md` lists all
> of them and `make gate` fails a card that says `live` while every finding under it is
> superseded. A prose summary could record the revision-2 withdrawals and the revision-3
> correction only as blockquotes — true, but not checkable, not discoverable from the
> finding, and not countable. See §"Where the claims live" at the end.

> **Revision 3 — 2026-08-02 - 09:12.** One change, and it is an **addition**, not a
> withdrawal: revision 2's Scope entry on **charge quantisation was wrong**, and understated
> a result the tree already had. F165 (2026-06-29) derives the hypercharge assignment up to
> one overall normalisation; revision 2 listed it as an input. **F279** adjudicated the
> contradiction by re-deriving the constraint system independently, upheld F165's conclusion,
> and corrected its attribution — the closing constraint is the F47 Higgs-free Majorana step,
> not the gravitational anomaly. Charge quantisation moves from **Scope** to a **core claim**
> (new claim 10). The residual input is named: one charge unit, plus $N_c=3$ for the specific
> thirds.

> **Revision 2 — 2026-08-02 - 10:15.** Issued against audit-V items V-024, V-029, V-030 and
> V6.8. Four changes, all withdrawals or corrections, none an addition of new physics:
> **(i)** the horizon-free black hole and its four dependent falsifiers are **withdrawn** —
> superseded by F178, under which the exact vacuum solution is Schwarzschild and the
> exponential metric is the PPN-order weak-field representation only; **(ii)** the
> $m_Z/m_W$ headline moves from the UV value $2/\sqrt3$ (1.77%) to the on-shell endpoint
> $3/\sqrt7$ (−0.064%, F49/F138), the number the tree actually computes; **(iii)** "three
> generations is a theorem" is corrected to match F75's own status line — the group theory
> is exact, the physical identification is a stated hypothesis; **(iv)** $\alpha_s$ and the
> deuteron residuals are re-checked against PDG 2025, and a **Scope** section is added
> saying what is *not* claimed.

## One-page summary

A deterministic **quantum cellular automaton (QCA)** on a body-centred-cubic (BCC) lattice is proposed as the physical vacuum. The free dynamics are *forced* (not chosen) by the Bisio–D'Ariano–Perinotti–Tosini uniqueness theorem: in 3D the minimal non-trivial one-particle QCA is the Weyl walk on the BCC lattice. From one reinterpretation — **the speed of light is the angular rotation rate of a real $(\mathbf E,\mathbf B)$ pair per unit wavenumber**, $c_\text{lat}=1/\sqrt3$ — the model recovers Maxwell's equations (as a linearised rotation), the Einstein mass shell (as a spherical-Pythagorean identity), and, with gauge structure added, the Standard-Model sectors and gravity. Every structural claim is verified numerically to machine precision (residuals $10^{-14}$–$10^{-16}$) or as exact rationals, in a public test suite. An eleven-paper series gives the full construction.

## Core claims (each a deviation from, or derivation of, the Standard Model)

1. **Light is a rotation rate, not a phase velocity** ($c_\text{lat}=d\Omega/d|\mathbf k|=1/\sqrt3$). Maxwell's curl law is its $O(\Omega)$ linearisation; energy conservation is geometric (length-preserving rotation). <!-- claims: CL001=live -->
2. **The photon is a bound pair of two spin-½ Weyl quanta** (de Broglie's neutrino theory of light), not a fundamental spin-1 boson — massless, luminal, transverse, and **exactly non-birefringent**. <!-- claims: CL002=live -->
3. **Mass without a Higgs field**: a chiral-$SU(2)$ complex-mass step carries weak isospin as an exact gauge symmetry (Ward identity to $1.1\times10^{-17}$); the would-be Higgs direction is pure gauge. Hypercharge rides the same field. <!-- claims: CL003=live -->
4. **Exactly three fermion generations.** The group theory is a **theorem** about the cubic point group $O_h$: from $\sum d^2=\lvert O_h\rvert=48$ the maximal single-valued irrep dimension is 3, and the parity-odd triplet $T_{1u}$ is unique. The **physical identification** — that a generation *is* that triplet, realised by the scalar mass selecting the odd-parity shell — is a **stated hypothesis**, not a theorem (F75 §7; F75 is a Candidate finding). Granting the hypothesis, a fourth generation is forbidden. Recorded this way because F79's structural $G$ inherits the same status. <!-- claims: CL004=contingent -->
5. **The Koide relation $Q=\tfrac23$** is an exact $45^\circ$ equipartition of the cubic amplitude $\sqrt m$ ($Q(\phi)=1/3\cos^2\phi$); electromagnetism selects the colour-free charged leptons to sit there. <!-- claims: CL005=live -->
6. **Confinement** is exact in 2D (area law, $\sigma=-\ln w(\beta)>0$ for all $\beta$); in 3+1D it is a colour-dielectric dual superconductor cross-checked against gauge Monte-Carlo, governed by $\mathbb Z_3$ centre-phase closure. <!-- claims: CL006=narrowed -->
7. **The Weinberg angle is derived**, with its scale: $\sin^2\theta_W=\tfrac14$ is the **matching value at the compositeness scale** $\mu_\star=4\pi v=3.09$ TeV, forced by hypercharge having no lattice kinetic term (F41/F138). Running Higgs-free to $M_Z$ gives $0.23173$ (**+0.22%** vs MS-bar $0.23122$), and the on-shell endpoint is $\sin^2\theta_W^\text{os}=\tfrac29\Leftrightarrow m_Z/m_W=3/\sqrt7$ (F49). Zero new parameters; the model's two existing rulers only. <!-- claims: CL007=live -->
8. **Gravity is sourced by the full stress-energy tensor** — the canonical law is the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ (F178). The impedance-matched lattice dielectric $K=e^{2GM/rc^2}$ (reciprocal lock $AB\equiv1$) is its **vacuum/weak-field representation**: GR-identical PPN ($\beta=\gamma=1$), plus the rotation-rate origin story. **Newton's constant is structural**, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, fixing $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$. <!-- claims: CL008=live -->
9. **Gravitational waves travel at exactly the photon speed**, $c_\text{grav}=c_\text{lat}=1/\sqrt3=c_\gamma$, inherited through the F79 zero-tree-stiffness channel rather than imposed (F180). This is a genuine zero, not a small number. <!-- claims: CL009=live -->
10. **Charge quantisation is derived, not assumed** (F165, re-attributed by F279). Given the lattice-fixed representation content, the generation hypercharges are the **unique** solution — up to a single overall normalisation — of two anomaly rows, the three F27/F41 mass-step rows, and the **F47 Higgs-free Majorana step**. That last row is what closes the system: $\nu_R^{\mathsf T}C\nu_R$ carries hypercharge $2y_\nu$, so gauge invariance forces $y_\nu=0$ exactly, and a Majorana mass is available only to a field of exactly zero hypercharge. The solution is $y_Q:y_u:y_d:y_L:y_e:y_\nu=1:4:-2:-3:-6:0$ with $y_\phi=3y_Q$; normalising $y_Q=\tfrac16$ gives the SM assignment and the measured electric charges $(\tfrac23,-\tfrac13,0,-1)$, exactly over ℚ. Both the gravitational and the cubic $U(1)^3$ anomalies are then identically zero on that line — consistency checks, not constraints. **Two inputs remain and are named:** the overall charge unit (the $\alpha$/$\sin^2\theta_W$ question, F49), and $N_c=3$ — commensurability holds for any $N_c$ (ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$), so colour supplies the *value* of the fraction, not the *fact* of quantisation. Unlike the Standard-Model theorems this parallels (Minahan–Ramond–Warner; Geng–Marshak), the closing constraint here is Higgs-free structure the model already needed for the see-saw. <!-- claims: CL010=live -->

11. **The charged-lepton shape is fixed by a representation weight, with zero shape parameters.** The condensate angle **is** the second-shell $E_g$ weight, $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad (exact $O_h$, F175) — *weight-as-phase*. $\delta^*$ is **primary** and the sextic clock coupling $\lambda_6=0.243$ (equivalently $W=6\lambda_6=1.46$) is an **output** via the F234 arrow $\lambda_6=\lvert B\rvert/(2e^6\cos\tfrac23)$, not a fit. From $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ the whole charged-lepton shape follows to $\le0.007\%$. It is adopted because **every alternative is closed, not because it fits best**: the angle is a genuine radian with $R=1$ forced by Schur-isotropy of the $E_g$ irrep metric (F255, derived not posited); a scale-free topological origin is excluded, the only available holonomy being $2\pi/3$ (F253); and the dynamical Landau route provably cannot give exact $3\delta^*=Q$, since the sea $B$ and the induced $C$ have independent $O(1)$ origins and the identity holds only to $1.7\times10^{-5}$ (F256). Together with claim 5 this fixes the *shape*; the overall *scale* remains an input (see Scope). Supersedes the F179/CN3 reading, under which the spectrum was a one-angle **fit**. <!-- claims: CL028=live -->

12. **$m_W$ and $m_Z$ are predicted absolutely, from two electroweak inputs where the Standard Model needs three.** Given $\{\alpha,G_F\}$ and nothing else, $m_W=\tfrac{3v}{2}\sqrt{2\pi\alpha}$ and $m_Z=\tfrac{9v}{2}\sqrt{2\pi\alpha/7}$ with $v=(\sqrt2\,G_F)^{-1/2}$ — the rationals being the BCC Wigner–Seitz facet count (7) and sublattice count (2), and the stiffness quantum $u=18\pi\alpha/7$ being *determined* by $e=g\sin\theta_W$ rather than free. The Standard Model's third input is a measured boson mass; here $\sin^2\theta^\text{os}_W=\tfrac29$ is lattice geometry, so the input count falls by one and **both masses become outputs**. The residual is free of radiative corrections: model and SM sit on the same on-shell relation with the same $\Delta r$, which cancels in the ratio (verified to $2.2\times10^{-16}$ over $\Delta r\in[0,0.10]$), giving $+0.222\%$ on $m_W$ and $+0.158\%$ on $m_Z$; the brackets $[80.147,80.548]$ and $[90.879,91.332]$ GeV both contain the PDG values, and their width is the SM's own $\Delta r_\text{rem}$. Carried with them: $\rho\equiv m_W^2/(m_Z^2\cos^2\theta_W)=1$ **exactly**, from the **rank** of the Higgs-free breaking — F41 absorbs exactly one Stueckelberg direction, so $\det M^2\equiv0$ identically in $u$, not at a tuned point — and *not* from a custodial $SU(2)$, which a Higgs-free model cannot invoke. Two inputs is not zero inputs: $v$ remains an anchor, $\alpha$ remains the EM input, and the absolute masses are conditional on F141's equal-stiffness hypothesis. **This withdraws the revision-2 Scope entry** that said the absolute masses were not predicted. <!-- claims: CL276=live, CL277=live -->
13. **The Born rule is derived rather than assumed, because the rule supplies both premises of Gleason's theorem.** In ordinary quantum mechanics Gleason's theorem is not used as a derivation, since both of its premises — $\dim\mathcal H\ge3$ and a non-contextual weight — are free assumptions there. In this model neither is: a measurement is not defined without a *record*, a record lives on environment cells, so the space cannot be two-dimensional; and the record channel is minimal coupling, a fixed operator carrying no reference to the measured basis. The same minimal coupling **einselects** the pointer observable instead of leaving it a choice — $[H_\text{int},\hat n(y)]=0$ exactly (a literal $0.0$, not $10^{-16}$), so classicality is position definiteness, while spin is *not* einselected (commutator $6.2219$) and a spin superposition survives until amplified into a position difference. **Live as of 2026-08-27**: the theorem is proved on the model's own evidence for $f\in L^2$ (F304 §5), the non-Abelian premises hold for any compact gauge group (F312), and the last external step — that a non-negative frame function is automatically regular, the bridge from bounded to $L^2$ — closes by reusing Gleason's own 1957 Theorem 2.8 rather than by an independent re-derivation (F329). <!-- claims: CL264=live, CL253=live -->
14. **No-signalling is exact, not asymptotic.** A local operation on region $A$ leaves the reduced state at $B$ unchanged to $7.8\times10^{-16}$ across product, Bell/GHZ and generic entangled states and twelve local unitaries, while a unitary applied *across* the cut moves it by $0.461$. Where a generic Lieb–Robinson system bounds leakage by an exponential tail, the automaton's causal cone is **strictly finite** — outside it the perturbed and unperturbed reduced states are bit-for-bit identical — and the cone is measured *tight*, exactly one site per brick-wall layer ($r\le t$), pinned by a control that goes red when the radius is shrunk by one cell. <!-- claims: CL256=live -->
15. **At finite lattice spacing the entire failure of Poincaré covariance is the gradient of one scalar.** With $\Phi=(\Omega^2-c_\text{lat}^2\lvert\mathbf k\rvert^2)/2c_\text{lat}^2$, the whole algebra defect is $D_i=\partial_i\Phi$ — so finite-$a$ boost covariance is *exactly* the statement that the off-shell invariant mass does not run with momentum. There is no second obstruction: $[K_i,P_j]$ has no defect at all, and the $[K_i,K_j]$ defect is the same $D_i$. It vanishes identically on the cubic axes, and is $O(\lvert k\rvert^3)$ for the paired-spinor photon against $O(\lvert k\rvert^2)$ on a chiral branch. **Narrowed in revision 6:** this is now asserted as a *structural, per-channel* statement — given a channel and its branch structure, the defect and its order follow. Which channels the model may **use** is no longer part of it, because the chiral branch has since been excluded by measurement (claim 19). Revision 5 said the confrontation with dispersion data "has not been done"; it has, and the coefficient lost. <!-- claims: CL262=narrowed -->
16. **The model's UV sensitivity is exactly two operator coefficients, and both are Sakharov sectors.** On a lattice with a physical Brillouin-zone cutoff there are no divergences: the four QED counterterms are **finite** bare-to-measured reparametrisations, not subtractions of infinities. Enumerating every operator of superficial degree $D\ge0$ in the full theory including gravity, and asking of each whether the model has a free parameter to absorb its cutoff-dependence, leaves exactly two that it does not — the cosmological constant ($D=4$) and the Einstein–Hilbert term $1/16\pi G$ ($D=2$). The model gets one right and one wrong, and the failure is **structural rather than a missing mechanism**: the two are the $a_0$ and $a_1$ moments of one zero-point sum, so any uniform reweighting moves both, and demanding the measured $G$ *and* the measured $\rho_\text{vac}$ together returns an 8.3 Gpc cell. The model cannot delete its zero-point sum without deleting its own $G$. <!-- claims: CL273=live, CL275=live -->
17. **Linear structure formation is fixed with zero free functions, where the EFT of dark energy has two.** In the linear, sub-horizon, quasi-static regime $\mu(a,k)\equiv1$ and $\Sigma(a,k)\equiv1$, with no scale and no time dependence, from three structurally independent sources (the Poisson collapse with coefficient exactly $4\pi G$; $G$ structural on a rigid substrate so $\dot G/G\equiv0$; the impedance match $AB\equiv1$ forcing the linear-order slip to a literal zero). Hence the growth index is $\gamma_g=6/11$ **exactly**. Because $\mu=1$ is $k$-independent *by derivation* rather than by choice, the model has **no screening mechanism** — the standard escape from linear-scale bounds is unavailable, and there is nothing to tune to relieve the $S_8$ tension. $\sigma_8$ itself is not claimed: it is linear in $\sqrt{A_s}$, and $A_s$ is a free initial condition. <!-- claims: CL254=live -->
18. **The primordial tilt's anomalous dimension is the anomalous part of the model's own block-spin eigenvalue.** The $t=0$ state of the rigid 3D automaton is a probability measure on 3D field configurations — a 3D Euclidean statistical field theory — so the primordial spectrum is that measure's energy–energy correlator and $\gamma\equiv\tfrac12(1-n_s)=y-1$ **identically**, with no holographic dual required or claimed. Two consequences follow, and the first is a bill the model has not yet paid: every block-spin eigenvalue exponent measured so far is an integer, which gives $n_s=1$ exactly — Harrison–Zel'dovich, excluded at $8.4$–$9.9\sigma$ — so the model *requires* exactly one non-integer eigenvalue of size $\gamma\approx0.014$–$0.018$, and producing it is the open calculation. Second, the stress tensor's dimension is protected by its own conservation, giving $n_t=2$ **exactly** (strongly blue) and $\log_{10}r(k_*)\approx-118$. Contingent on the statistical-field identification. <!-- claims: CL267=contingent -->
19. **An elementary fermion of this model may not ride a single BCC chiral branch — measurement has closed that option by seven decades.** This is the first claim in this document taken away by data rather than by a later derivation. A massive Dirac fermion built from the model's own one-tick unitary carries **one** branch invariant: its four eigenphases are $\pm\arccos(n\,u_+)$, each two-fold degenerate, so the chirality-odd defect of claim 15 is carried **spin-independently**, with the sign flipping between particle and antiparticle. The photon's escape is unavailable in principle — $\Omega_\text{even}$ is a **sum over both branches inside one eigenvalue**, carrying $k/2$ on two constituents, and a one-quantum channel cannot reproduce that. Pairing a massive fermion's two Weyl blocks onto opposite branches is unitary at $m=0$ and non-unitary for every $m\neq0$ with a $k$-independent mass (any such mixing forces $B(\mathbf k)=VA(\mathbf k)^\dagger V^\dagger$, whose trace is $\operatorname{tr}A(\mathbf k)$); a **local** $k$-dependent mixing that does pair them exists, and rescues nothing — its mass enters linearly rather than as $m^2/2E$, so it is an axial CPT-odd term and not a Lorentz-scalar mass, and its spectrum **splits** $b_2$ to $\mp\lvert b_2\rvert$ instead of cancelling, leaving a superluminal eigenstate. In physical units the defect is a local, analytic, CPT-odd **dimension-5** operator, $E^2=m^2c^4+c^2p^2-\tfrac{2}{\sqrt3}(cp_x)(cp_y)(cp_z)/E_a$ with $E_a=\hbar c/a$, a **pure SME $(j,m)=(3,\pm2)$** spherical coefficient, giving $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}\,3^{1/4}/9=1.4662$ and $E_\text{LV}=\tfrac92E_a=8.33\times10^{18}$ GeV. Li & Ma's LHAASO/Crab analysis requires $\ge9.4\times10^{25}$ GeV superluminal and $\ge10^{24}$ GeV subluminal: **short by 7.05 and 5.08 decades**, with the model's own vacuum-Cherenkov threshold at 12.96 TeV against electrons the Crab demonstrably accelerates past 1.1 PeV. Every escape is measured and closed — the coefficient is odd in both $\hat k$ and charge so *both* bounds bite; only $6.2\times10^{-7}$ of the sky evades; buying the escape from the ruler costs $G$ a factor $1.3\times10^{14}$; and the same ruler leaves the photon $2.0\times10^{13}$ times softer because it is dimension-6, which is why the GRB bound passed. What survives is everything structural: F301's algebra, F91's classification, F246's photon coefficient. What is gone is the physical assignment. The conversion itself was first done inside this tree by `docs/reviews/F301-review-2026-08-12.md` at a bound 1.6 decades looser; F327 sharpens it, corrects the operator class from helicity-odd to spin-independent, and arms it with a gate record. <!-- claims: CL284=live -->
20. **A discrete CPT theorem holds for the free (gauge-decoupled) BCC Dirac walk, exact at every momentum and mass — and it is not the continuum theorem re-derived, since its own hypothesis (continuum Lorentz invariance) is only partially available here.** For $\Theta=\Sigma\cdot(\sigma_y\!\oplus\!\sigma_y)\cdot K$ (block swap, an internal $\sigma_y$ twist on each Weyl block, and complex conjugation), $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ holds identically — no small-$k$ expansion, every $\mathbf k$ in the Brillouin zone, every mass $\lvert m\rvert\le1$ — with $\Theta^2=-1$, the Kramers signature of a genuine antiunitary involution rather than a bookkeeping relabelling. The companion result is a no-go: no fixed unitary can implement parity alone at any finite generic $\mathbf k$, because $D(\mathbf k)$ and $D(-\mathbf k)$ have different spectra there ($\omega(\mathbf k)\ne\omega(-\mathbf k)$, vanishing only on the cubic axes) — the same chirality-odd defect claim 19 measures, now shown to obstruct C, P, and T individually rather than only the combination. This closes rubric row A4 for the free sector only: the SU(2)$_L$ charged-current coupling is a nonlinear multiplicative gate, not a closed-form momentum-diagonal unitary, so the operator method does not transfer mechanically and that extension is named open rather than assumed. Distinct from claim 6's $\theta_\text{QCD}$ reality argument, which concerns a different object (the Euclidean action's reality under loop-set reversal) and is not a CPT statement. <!-- claims: CL285=live -->
21. **Cluster decomposition extends to the interacting, 3-D BCC theory.** The free massive BCC Dirac field's equal-time (100)-axis correlator decays as $e^{-\kappa_{100}(m)r}$ with $\kappa_{100}(m)=\sqrt3\,\operatorname{arccosh}(1/\sqrt{1-m^2})$, an exact closed form from a genuine 3-D pole extremisation over the transverse momenta — not a 1-D result dressed up as 3-D: the dominant singularity is proved, via a bilinear-function corner argument, to sit exactly on the (100) axis rather than assumed to. Validated against the model's own dispersion, but only after a real bug was diagnosed and fixed: the naive cubic FFT grid is the wrong Brillouin zone for this lattice (the same hazard F267 names for mode-sum observables, now shown to bite a real-space transform too), giving both the wrong magnitude and a spurious checkerboard artifact; the fix samples the model's own reciprocal generators directly. Separately, a lattice-native self-consistent NJL gap equation — regulated by the model's own finite Brillouin zone rather than an artificial cutoff — dynamically generates a mass from a bare-massless starting point for couplings in a narrow measured window ($g_c\approx2.637$ measured, $g_\max=\pi$ **exact**, from $I_1^\text{lat}(m{=}1)=1/\pi$ at the model's own $|m|\le1$ admissibility endpoint); cluster decomposition is then demonstrated **at** that dynamically generated mass. Explicitly mean-field (the same scope claim 7's NJL treatment already carries), not a full non-perturbative correlator, and the residual does not reach machine precision at any mass or window tested (best $\approx5\%$ at $m=0.95$, worst $\approx53\%$ at $m=0.05$, shrinking monotonically with mass) — graded QUANT, not MACHINE. Closes row A10's own residual: F290 had shown no-signalling exact and the causal cone strict, but its clustering measurement was 1-D and free-fermion only. <!-- claims: CL286=live -->


> **Withdrawn in revision 2.** The former claim 9, "black holes are horizon-free dielectric
> condensates", is **retracted**. F178 demotes the exponential metric to the PPN-order
> weak-field representation; the **exact vacuum solution is Schwarzschild**, with a horizon.
> The horizon-free throat, the $+4.63\%$ shadow, the absent Hawking spectrum, the late-time
> ringdown echoes and the $4\pi$ second-order deflection coefficient were all consequences of
> treating the exponential form as fundamental, and none of them is predicted by the model as
> it now stands. They are listed here, rather than deleted silently, because they were
> published as live falsifiers between 2026-06-08 and 2026-08-02. <!-- claims: CL023=withdrawn -->

## Headline verified numbers

All reference values are **PDG 2025 / CODATA 2022** as of 2026-08-02.

| Quantity | Model | Reference | Residual | Free parameters |
|---|---|---|---|---|
| $c_\text{lat}$ | $1/\sqrt3=0.5773503$ | — (definition of the lattice unit) | exact | 0  <!-- claims: CL001=live -->|
| BCC lattice constant $a$ | $2/\sqrt3=1.1547005$ | — (closed form, F278) | exact | 0 |
| $\sin^2\bar\theta_W(M_Z)$ | $0.23173$ | $0.23122$ | $+0.22\%$ | 0  <!-- claims: CL007=live -->|
| $m_Z/m_W$ (on-shell, $\sin^2\theta^\text{os}_W=\tfrac29$) | $3/\sqrt7=1.133893$ | $91.1880/80.3692=1.134614$ | $\mathbf{-0.064\%}$ | 0  <!-- claims: CL014=live -->|
| Koide $Q$ | $0.6666605$ | $\tfrac23$ | $0.91\sigma$; predicts $m_\tau=1776.97$ MeV ($6\times10^{-5}$) | 0  <!-- claims: CL005=live -->|
| Electric charges $(Q_u,Q_d,Q_\nu,Q_e)$ | $(\tfrac23,-\tfrac13,0,-1)$ | same | exact over ℚ (literal 0) | 1 (charge unit) + $N_c{=}3$  <!-- claims: CL010=live -->|
| $a/\ell_P$; $G$ | $6.5978$; $6.6743\times10^{-11}$ | CODATA | $3\times10^{-8}$ | 0  <!-- claims: CL008=live -->|
| $m_W$ (absolute, from $\{\alpha,G_F\}$) | $\tfrac{3v}{2}\sqrt{2\pi\alpha}\in[80.147,80.548]$ GeV | $80.3692\pm0.0133$ | $+0.222\%$ ($\Delta r$-free) | 0 (2 inputs, not 3) <!-- claims: CL276=live -->|
| $m_Z$ (absolute, same two inputs) | $\tfrac{9v}{2}\sqrt{2\pi\alpha/7}\in[90.879,91.332]$ GeV | $91.1880$ | $+0.158\%$ ($\Delta r$-free) | 0 (2 inputs, not 3) <!-- claims: CL276=live -->|
| $\rho=m_W^2/(m_Z^2\cos^2\theta_W)$ | $1$, from rank (not custodial $SU(2)$) | $1$ | exact over ℚ, identically in $u$ | 0 <!-- claims: CL277=live -->|
| Growth index $\gamma_g$; $\mu,\Sigma$ | $6/11$; $\equiv1$ | GR: $6/11$; $\equiv1$ | exact (no screening available) | 0 <!-- claims: CL254=live -->|
| $\alpha_s(M_Z)$ | $0.11955$ (1-loop) | $0.1175\pm0.0010$ | $+1.7\%$ ($2.1\sigma$) | 1 scheme-matching input; **branch closed 2026-08-18** <!-- claims: CL022=open, CL282=live -->|
| Deuteron $E_b$ | $2.224$ MeV | $2.22457$ MeV | $0.026\%$ | 1 ($b=0.55$ fm) |

**Two residuals moved since revision 1, and in both cases the *measurement* moved, not the
model.** $\alpha_s(M_Z)$ was recorded at $+1.3\%$ against a PDG average of $0.1180$; that
average is now $0.1175\pm0.0010$, so the same unchanged model number is $+1.7\%$, i.e.
$\approx2.1\sigma$ of experiment. This is the register's largest open tension and is stated
as such.

**That number carried a branch from revision 5, and the branch is now CLOSED (2026-08-18).**
$0.11955$ assumes the model's bare coupling is centre-normalised, $1/(16\pi)$ — hypothesis
**H1**. The alternative, **H2**, put the coupling at $1/(16\pi C_F)$ and gave
$\alpha_s(M_Z)=0.03970$: not a $2.1\sigma$ tension but a $-66\%$ miss. **H2 is excluded and H1
is adopted**, on two independent grounds, neither of which needed the $\Lambda$-ratio
computation the fork had named as its decider.

*Structural.* The $C_F$ exists only in a **mixed** evaluation of the underlying matching — the
abelian rotor's integer flux level against the $SU(N)$ link's quadratic Casimir. Under either
self-consistent evaluation the matching gives the same stiffness for **every** $N$ and every
irrep, exactly, with no group factor at all; and the mixed evaluation is not even
self-consistent at $N=3$ once one leaves the restricted tower it was built on, where it assigns
**zero** electric cost to a colour-neutral (triality-0) link.

*Quantitative.* H2 requires a lattice-to-$\overline{\rm MS}$ ratio of $3.4\times10^{6}$, which
is **5.6 decades outside** the model's own previously committed bracket $[1,\,7.98]$ — a bracket
published the day before the fork was framed and never compared with it — and would require the
model action's one-loop constant to exceed the Wilson action's by $7.2\times$, for an action
*measured* to have $5.3$–$5.7\times$ **smaller** discretisation error than Wilson's.

The 2D $SU(3)$ engine that had been read as measuring H2 turns out not to discriminate: it
returns $\sigma_6/\sigma_3=2.49115$ at H1's coupling and $2.49540$ at H2's, because Casimir
scaling in two dimensions is a theorem about the $SU(3)$ Wilson measure at weak coupling and is
independent of the coupling. What it does establish — that link cost is set by the quadratic
Casimir — is precisely the premise under which the $C_F$ cancels, so it is evidence **for** the
adopted reading. **The $2.1\sigma$ therefore stands unconditionally**, and the remaining
scheme-matching input is a residual rather than a branch.
<!-- claims: CL282=live -->
<!-- claims: CL022=open --> The deuteron moved the other way, $0.34\%\to0.026\%$ — but at a chosen $b=0.55$ fm,
so it is a one-parameter result and is no longer described as zero-parameter.

**One prediction survived an out-of-sample revision.** $m_Z/m_W=3/\sqrt7$ was fixed before
PDG 2025 excluded the CDF-II $m_W$ measurement for low compatibility. Against the resulting
$m_W=80.3692\pm0.0133$ the model gives $-0.064\%$ (implied $m_W=80.4203$). Had it been tuned
to CDF it would now look worse; it was not, and it survives the exclusion cleanly.

## Falsifiable predictions (with thresholds)

- **Quantum-gravity dispersion.** A quadratic ($n=2$) vacuum dispersion with energy scale $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV. **Any measured $n=2$ time-of-flight bound above $1.36\times10^{19}$ GeV kills the adopted lattice cell.** <!-- claims: CL011=live -->
- **Vacuum birefringence.** The physical (paired) photon is **exactly non-birefringent** — not within a tolerance, but structurally: the pair carries one single-valued rotation rate $\Omega_\text{pair}$, so there is no second branch to split from. A confirmed first-order vacuum birefringence in GRB/AGN polarimetry would contradict it (and would, conversely, revive the excluded chiral construction). <!-- claims: CL012=live -->
- **Gravitational-wave speed.** $c_\text{grav}=c_\gamma$ **exactly**, with no free coefficient (F180; GW170817 residual $\le3\times10^{-83}$). Any confirmed non-zero $c_\text{grav}/c_\gamma-1$ falsifies the inheritance mechanism. <!-- claims: CL013=live -->
- **Weinberg angle.** The chain is committed to $\sin^2\theta_W=\tfrac14$ at $\mu_\star=4\pi v$ and $\sin^2\theta_W^\text{os}=\tfrac29$ on shell. A precision $m_W$ that moved $m_Z/m_W$ off $3/\sqrt7$ by more than the running uncertainty would falsify it — which makes the PDG 2025 re-analysis (CDF-II excluded) a passed test, not a retrofit. <!-- claims: CL014=live -->
- **Charged-lepton shape.** A charged-lepton mass measurement inconsistent with the $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ shape at better than $0.007\%$. Because $\delta^*$ is an exact rational fixed by $O_h$ representation theory, **there is no parameter to re-fit** — the two no-gos (F253, F256) closed the alternatives deliberately, and that is what makes this falsifiable rather than adjustable. <!-- claims: CL028=live -->
- **Absolute $m_W$.** The whole residual on claim 12 is the on-shell Weinberg angle and there is no parameter left to absorb a change in it: the claim dies if $\sqrt{\sin^2\theta_W^\text{obs}/(2/9)}$ leaves $[0.995,1.005]$, equivalently if the measured $m_Z/m_W$ moves off $3/\sqrt7$ by more than $0.1\%$. A measurement of $m_W$ at fixed $\{\alpha,G_F\}$ outside $[80.147,80.548]$ GeV that is not attributable to $\Delta r$ kills it directly. <!-- claims: CL276=live -->
- **No dimension-5 photon operator.** The leading Lorentz-violating photon operator is dimension-**6**, established by measuring the scaling exponent $p=2$ rather than by bounding a coefficient, with the exact rational coefficient $-\bigl[(1-\sum_i\hat n_i^4)/144+(\hat n_x\hat n_y\hat n_z)^2/24\bigr]$ (verified to $1.1\times10^{-20}$ in 60-digit arithmetic; range exactly $[-1/162,0]$, vanishing along $\langle100\rangle$). **Any detection of dimension-5 photon Lorentz violation — linear energy-dependent arrival times, or birefringence — falsifies it**, because the claim is that the operator is *absent*, not small. This is also why the paired photon survives the GRB bound that excluded the chiral $\sigma$-bilinear construction. <!-- claims: CL274=live -->
- **$S_8$ and late-time growth.** Claim 17 predicts the combined-CMB $S_8$ propagated forward by GR growth, with nothing to tune: $0.8410$ against combined CMB $0.836^{+0.012}_{-0.013}$ ($0.29\sigma$), KiDS-Legacy 2025 ($1.17\sigma$) and **DES Y6 $3\times2$pt $0.789\pm0.012$ ($3.00\sigma$)**. If the DES Y6 direction consolidates as physical rather than as photo-$z$ or baryonic-feedback systematics, the claim is dead and the gravity sector with it — and the usual escape, modified gravity confined to nonlinear scales by screening, is unavailable here. Secondary thresholds: $\lvert\mu-1\rvert>0.011$, a detected linear-order slip $\lvert\eta-1\rvert\gg2\times10^{-5}$, or a measured $\dot G/G\neq0$. <!-- claims: CL254=live -->
- **Tensor-to-scalar ratio.** Claim 18 gives $n_t=2$ exactly and $r\sim10^{-118}$ at the CMB pivot, with no parameter to move: **any detection of $r$ at all** — BICEP Array targets $\sigma(r)\lesssim0.003$ — falsifies it. The claim also requires exact power laws, so a significantly non-zero running $dn_s/d\ln k$ falsifies it, with the discriminator at $\sigma\sim2.6\times10^{-4}$. <!-- claims: CL267=contingent -->
- **Mercury precession.** PPN $\beta=\gamma=1$ (42.98″/cy). The naive *linear* dielectric ($\beta=\tfrac12$, 50.1″/cy) is excluded. Under F178 this is now a consistency requirement rather than a distinctive prediction: in vacuum the model **is** GR, so a confirmed PPN deviation falsifies it exactly as it would falsify GR. <!-- claims: CL015=narrowed -->

**Withdrawn in revision 2** (all four were consequences of the pre-F178 exponential-metric-as-fundamental reading, and the model no longer predicts any of them): photon-ring imaging at $+4.63\%$; gravitational-wave ringdown echoes; absence of a thermal Hawking spectrum; the $4\pi$ second-order light-bending coefficient. **An observation matching Schwarzschild in any of these four would previously have been recorded as falsifying the model. It does not.** <!-- claims: CL024=withdrawn, CL025=withdrawn, CL026=withdrawn, CL027=withdrawn -->

## Scope — what is *not* claimed

Stated explicitly so that absence is not read as a prediction. Each is open and acknowledged,
not quietly omitted.

- ~~**$m_W$ and $m_Z$ in absolute terms.**~~ **Moved to core claim 12 in revision 5.** Revision 2 recorded this as a scope boundary; F320 (2026-08-16) shows the boundary was in the wrong place. The premise was true and remains true — $v$ *is* an anchor, not an output — but the absolute masses do not follow from $v$ alone, and eliminating the stiffness quantum against $e=g\sin\theta_W$ determines them. What is still an input is named in claim 12: $v$, $\alpha$, and F141's equal-stiffness hypothesis. <!-- claims: CL016=withdrawn, CL276=live -->
- **The CKM matrix and measured CP violation.** The construction is first-generation; $J=0$ is the arithmetic consequence of one generation ($N_\text{phase}=(n-1)(n-2)/2$), not a prediction that the CKM phase vanishes (F53). Three-generation mixing is out of scope. <!-- claims: CL017=not_claimed -->
- **Neutrino mass scale.** F47 supplies a Higgs-free see-saw *mechanism*; nothing in the model fixes $M_R$, so no absolute neutrino mass is predicted. <!-- claims: CL018=not_claimed -->
- **Muon $g-2$ beyond QED.** The QED piece is computed through two loops ($A_2(\mu)=0.765857$ vs the known $0.765857410$). Hadronic vacuum polarisation, hadronic light-by-light and electroweak contributions are **not** computed and not claimed. <!-- claims: CL019=not_claimed -->
- ~~**Charge quantisation.**~~ **Moved to core claim 10 in revision 3.** Revision 2 listed this as an input; that was wrong. It is derived (F165, re-derived and re-attributed by F279). What remains an input is the **one charge unit** — the overall normalisation, which is the $\alpha$ / $\sin^2\theta_W$ question (F49) — and, for the specific *thirds* rather than commensurability as such, $N_c=3$. Both are named in claim 10. <!-- claims: CL010=live -->
- **"No doublers" has a domain.** The BCC Weyl walk has exactly one zero, at $k=0$, and no $\omega=\pi$ point **on the cubic FFT grid** ($L$ up to 128, both branches). On the true BCC zone the $\omega=\pi$ mode sits exactly at the corner H, $\lvert\mathbf k\rvert=2\pi/a=\pi\sqrt3$ (F278). Every observable in the tree is computed on the grid, so no result depends on the distinction — but the unqualified form of the claim overstates it, and the discriminating test is not yet built. <!-- claims: CL020=narrowed -->
- **The cosmological constant** is not derived; F193/F196 reduce the classic 121-order problem to the $\Omega_\Lambda\approx0.69$ coincidence, which is not the same as explaining it. Revision 5 sharpens the *shape* of what is missing rather than the result: by claim 16 the one obvious internal route — reweighting the zero-point sum — is **excluded**, because the same sum supplies $G$. Whatever solves this is not a rescaling. <!-- claims: CL021=not_claimed, CL275=live -->

## Where the claims live

Since 2026-08-04 this document is a **summary**, not the register. The register is
`docs/claims/` — one card per claim, `CL{NNN}-{slug}.md`, each carrying a present-tense
status (`live` · `narrowed` · `contingent` · `open` · `withdrawn` · `not_claimed`), a
falsifier field, the findings it rests on, and its own revision history. `claims-index.md`
lists every card.

The distinction the cards exist to make: **a finding is a research record and a claim is a
position.** A finding is written once and superseded rather than rewritten — it is correct
for it to keep saying what a session concluded. The claim resting on it is what has to move,
and until now there was nowhere to move it. Sixteen findings in this project are named in a
`superseded:` list while their own headers still read `Confirmed — N/N PASS`; that is not a
defect in the findings, it is the gap the cards fill.

Three consequences worth stating here, because they are what a reader of *this* document
should know:

- **The revision-2 withdrawals are cards, not a blockquote.** The horizon-free black hole
  and its four dependent falsifiers are `CL023`–`CL027`, each `status: withdrawn`, each
  card's history section *being* the retraction record. A gate test asserts they are never
  deleted, because a withdrawn claim that is deleted is a claim that gets re-made.
- **Overstatement is now machine-checkable.** `tools/check_claims.py` fails a card marked
  `live` when *every* finding it rests on is named in a `superseded:` list. On its first
  run it caught seven. It deliberately does **not** fire on partial supersessions: of
  fourteen files one audit called superseded, exactly one was.
- **Not every card is authored.** 58 are; 223 are `review_state: unreviewed-seed` —
  extracted from a finding, classification *not* confirmed by a reviewer, and not citable
  as independent support. The count is a ratcheted debt, not a claim of 223 results.
- **This document can no longer drift from the register.** Every claim, falsifier and scope entry
  above carries an anchor — an HTML comment, invisible in the PDF — naming the cards it stands on
  *and the status it records them at*, and `make citations` fails when a card's status moves and
  this page does not follow it. Added 2026-08-18, after CL016 stayed published here for two days
  past its withdrawal; that miss is the check's own selftest fixture. A headline card that never
  reaches this page at all is counted as declared debt rather than failing the gate, so a new
  result can be recorded before it has been written up for a lay reader.

## Reproducibility

Every claim above runs in a public test suite to the stated residual. The **structural** sector — lattice cell, gauge couplings, metric — carries **no free fit parameters**; the two rows that do carry one ($\alpha_s$, the deuteron) are marked in the table rather than folded into a headline. Source, tests, and per-finding write-ups accompany the papers.

*Barrier: `make gate`. A green bare `pytest` is not sufficient — it cannot collect the three
scenario records that run the engine on a lattice.*

*Full series (11 papers) and this summary: see the accompanying `papers/` directory. Contact: benludwig6382@gmail.com.*
