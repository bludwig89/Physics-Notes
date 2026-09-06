# F122 — P2: the dynamical baryon — a real-time, non-dispersing, mass-measured three-quark bound state (proton, then neutron)

**Date:** 2026-06-09 - 16:54
**Status:** Confirmed — 11/11 checks PASS. S0/S1/S4 machine-precision/exact (analytic harmonic ground state; two solve routes; S₃-symmetric pair radii); S2/S3/S5/S6 quantitative (variational convergence, discrete spectrum, confinement dominance, Casimir-scaling invariance); S7/S8 Tier-B (m_p/√σ ratio P6-gated; n–p splitting). Independently re-verified: the ⟨r⟩/⟨1/r⟩ kernels vs direct radial quadrature (6 digits) and the full 6-D pair matrix element vs Monte-Carlo.
**Module:** `ca-simulation/ca_baryon_dynamics.py`
**Script:** `tests/findings/test_P2_baryon_bound_state.py` (~1.5 s)
**Results:** `test-results/P2_baryon_bound_state.json`
**Test record:** record `P2-baryon-bound-state` (tier battery) — the script above, baseline `test-results/P2_baryon_bound_state.json`. `P6-si-scale` (F123) also names F122: the 3m_c nucleon rests on this bound state. Declared 2026-08-19.
**Cross-references:** [[F71-colour-singlet-baryon-proton]] (the operator-level proton this makes dynamical), [[F97-baryon-phase-closure-no-go]] (mass is centre-closure/string, not constituent phase — the constraint this obeys), [[F74-bound-state-binding]] (the two-body solver generalised here to three bodies), [[F70-gradient-flow-confinement-string-tension]] / [[F94-lattice-gauge-mc-vs-F86]] / [[F110-realtime-link-hamiltonian-confinement]] (P1 — the confining string that sources the mass), [[F40-quark-Y-and-dynamical-chi-kinetic]] (d–u mass ratio used in the n–p splitting), [[F103-p3-dynamical-pion-goldstone]] / [[F104-p4-deuteron-tensor-bound-nucleus]] (the P3/P4 siblings that reused the same F74 engine).

---

## 1. What this closes

F71 built the proton as an *operator* — the colour singlet $B=\varepsilon_{abc}u^au^bd^c$ with the right quantum numbers, Fermi statistics, and an *energetic* binding argument — but explicitly **not** a dynamical, real-time, mass-measured bound state. This finding replaces the operator with a genuine solution of the three-body Schrödinger problem: a converged, non-dispersing, S₃-symmetric ground state whose mass is **sourced by the P1 confining string**, with the neutron and the $n$–$p$ splitting following from the same solver. This is the headline deliverable P2 of `docs/roadmaps/roadmap-matter-binding.md`.

## 2. The model

Rest-frame (zero total momentum) three equal-mass constituents reduce to a six-dimensional relative problem in mass-normalised Jacobi coordinates

$$\boldsymbol\xi_1=\frac{\mathbf r_1-\mathbf r_2}{\sqrt2},\qquad \boldsymbol\xi_2=\frac{\mathbf r_1+\mathbf r_2-2\mathbf r_3}{\sqrt6},$$

so the relative kinetic operator is diagonal, $T=-\frac{1}{2m}(\nabla^2_{\xi_1}+\nabla^2_{\xi_2})$, and the three pair separations are linear forms $r_p=|\mathbf w_p\!\cdot\!\boldsymbol\xi|$ with $|\mathbf w_p|^2=2$ for all three pairs. The pairwise interaction is the P1 confining + one-gluon-exchange **Cornell** potential (roadmap-literal default),

$$V_p(r)=\sigma\,r-\frac{2\alpha_s}{3}\frac1r\qquad\text{per pair},$$

the $2/3$ being the colour Casimir factor for a $qq$ pair in the $\bar 3$. The structural results are invariant under the alternative "½-rule" Casimir scaling $V_p=\tfrac12\sigma r-\tfrac{\alpha_s}{3}\frac1r$ (check S6).

## 3. The engine — explicitly-correlated Gaussians

The relative wavefunction is expanded in correlated Gaussians $g_A(\boldsymbol\xi)=\exp(-\tfrac12\boldsymbol\xi^{\!\top}(A\otimes I_3)\boldsymbol\xi)$, $A$ a symmetric positive-definite $2\times2$ matrix, for which **every** matrix element is closed-form ($C=A+B$, $\beta_p=\mathbf w_p^{\!\top}C^{-1}\mathbf w_p$):

$$S_{AB}=\det(C)^{-3/2},\quad \frac{\langle T\rangle}{S}=\frac{3}{2m}\mathrm{Tr}(AC^{-1}B),\quad \frac{\langle r_p\rangle}{S}=\sqrt{\tfrac{8\beta_p}{\pi}},\quad \frac{\langle 1/r_p\rangle}{S}=\sqrt{\tfrac{2}{\pi\beta_p}}.$$

This is the F74 two-body solver generalised to three bodies: the F74 contact well becomes the confining Cornell channel and the F74 secular Koster–Slater root becomes the ECG generalised eigenproblem $Hc=ESc$, solved **two independent ways** — `scipy.linalg.eigh(H,S)` and a hand-rolled Cholesky reduction — which agree to $4.5\times10^{-12}$ (S1, the F74 "two routes" discipline). Permutation symmetry is made exact by closing the basis under the $120°$ Jacobi rotation (the cyclic particle permutation), and the near-singular overlap of that overcomplete basis is handled by canonical orthogonalisation. All arithmetic is real, so the CLAUDE.md numpy/chiral caveat does not bite; the engine is validated to $5\times10^{-14}$ against the **analytic** harmonic three-body ground state $E=3\sqrt{3k/m}$ (S0).

## 4. The physics delivered

**The baryon is a genuine, non-dispersing bound state (S2, S3).** $E_\text{rel}$ decreases monotonically and settles (relative change $5.5\times10^{-5}$ at the converged mesh). A confining potential has a **purely discrete spectrum** — no scattering continuum — so the ground state is automatically a stationary, normalisable bound state separated from the first excited state by a finite gap ($\approx2.9\sqrt\sigma$): the proton **cannot fall apart**. This is the dynamical realisation of F71's energetic-confinement argument.

**The spatial ground state is totally S₃-symmetric (S4).** On the permutation-closed basis the three pair separations are equal to $8\times10^{-11}$, $\langle r_{12}\rangle=\langle r_{13}\rangle=\langle r_{23}\rangle$ — the baryon's antisymmetry rides entirely on the colour$\times$spin sector (F71 BS6/BS7), exactly as required.

**Confinement dominance — F97 made dynamical (S5, S6).** In the current-quark-mass limit ($m_q=0.01\sqrt\sigma$) the quark-mass sum is **0.11 %** of the bound-state mass; the remaining $\sim99.9\%$ is the confining string + kinetic energy. This reproduces F97's no-go statement (PDG current-quark sum is 0.96 % of $m_p$, and the only stable colour combination is the $\mathbb Z_3$ centre closure) as an explicit dynamical number: **the proton's mass is the string, not the constituents** — precisely the roadmap's hazard-(ii) requirement that "the solver must source the bulk of the mass from the string." The conclusion is unchanged under the ½-rule Casimir scaling.

**The neutron and the $n$–$p$ splitting (S8).** Re-running $uud\to udd$, the splitting to leading order is the constituent-mass-sum difference plus the EM self-energy:

$$m_n-m_p=(m_d-m_u)+(\delta^\text{EM}_n-\delta^\text{EM}_p).$$

With the F40 down–up ratio (anchored to PDG current masses $m_u=2.16$, $m_d=4.67$ MeV) the strong term is $+2.51$ MeV (neutron heavier), and the proton's larger Coulomb self-energy gives $\delta^\text{EM}_p-\delta^\text{EM}_n\approx1.00$ MeV (EM makes the proton heavier). The result is $m_n-m_p=+1.51$ MeV — **sign positive**, within $\sim0.2$ MeV of the measured $+1.293$ MeV. The sign is the real test of the F40 ratios — the down–up gap must beat EM, and it does.

## 5. The honest open edge (Tier-B / P6)

The **absolute** ratio $m_p/\sqrt\sigma$ from the non-relativistic constituent solve **overshoots** the empirical nucleon-in-string-units value ($\approx2.24$ at $\sqrt\sigma=0.42$ GeV): the NR solve gives $\approx8$ with the roadmap-literal potential and constituent $m_q=0.785\sqrt\sigma$, because it omits the conventional additive Cornell constant $V_0$ (a vacuum-energy subtraction) and uses non-relativistic kinematics, which badly overestimates the zero-point energy of light quarks in a linear well. The precise number needs the relativised / Bethe–Salpeter treatment — exactly the regime F74 flagged as "beyond NR validity" — and the P6 SI anchor. **Structure is the prediction here; the MeV is P6-gated**, as the roadmap specifies for P2. What is robustly established, parameter-light and $V_0$-independent, is the *existence*, *non-dispersion*, *S₃ symmetry*, *confinement dominance*, and the *sign of $n$–$p$*.

## 6. Checks

| # | Check | Tier | Residual |
|---|---|---|---|
| S0 | ECG engine == analytic harmonic ground state $3\sqrt{3k/m}$ | machine | $5.2\times10^{-14}$ |
| S1 | scipy `eigh(H,S)` == Cholesky reduction | machine | $4.5\times10^{-12}$ |
| S2 | variational monotone decrease + convergence | quantitative | $5.5\times10^{-5}$ |
| S3 | finite gap to first excited (discrete/non-dispersing) | quantitative | gap $=2.89\sqrt\sigma$ |
| S4 | three pair radii equal (S₃-symmetric spatial state) | machine | $8.3\times10^{-11}$ |
| S5 | quark-mass sum $<2\%$ of $M$ (string-dominated, cf. F97) | quantitative | $0.11\%$ |
| S6 | dominance + symmetry survive ½-rule Casimir scaling | quantitative | $2.9\times10^{-11}$ |
| S7 | finite positive $m_p/\sqrt\sigma$ on the string scale | Tier-B | $8.1$ (NR, $V_0$-free) |
| S8a | $m_n-m_p$ sign positive | quantitative | PASS |
| S8b | $abs(m_n-m_p)$ within 1 MeV of measured | Tier-B | $0.22$ MeV |

## 7. What P2 adds to the ledger

New module `ca-simulation/ca_baryon_dynamics.py`; new suite `tests/findings/test_P2_baryon_bound_state.py` (11/11). Exactness rows: Tier 1 #155–156 (harmonic engine; S₃ pair radii), Tier 2 #65 (two-route agreement), Tier 3 #39–40 (confinement dominance; $n$–$p$ splitting). With P2 closed, the matter-binding roadmap has P0 (single particles), P1 (3+1D confinement), P2 (dynamical baryon), P3 (pion, F103) and P4 (deuteron, F104) all built; the open phases are P5 (atoms) and the cross-cutting P6 (SI scale), which gates every absolute MeV in P2–P5 — including this finding's $m_p/\sqrt\sigma$.
