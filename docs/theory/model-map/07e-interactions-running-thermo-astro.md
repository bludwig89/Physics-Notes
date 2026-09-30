# Interactions — running couplings, thermodynamics, astrophysics and odds

This section maps 20 modules in `src/casim/engine/interactions/`. They fall into four groups. (i) Strong-field astrophysics on the canonical F178 geometry: Schwarzschild QNMs, shadow ray-tracing, TOV stars, the Tolman discriminator and the vacuum-energy sign. (ii) The QCD/QED running-coupling chain F144→F145→F151→F152→F155 and the B9 re-derivation F322/F334. (iii) Lattice thermodynamics F300/F309/F376. (iv) Stand-alone phenomenology: superconductivity F210–F375, slow light, and the Higgs–Dirac unified stepper.

**Shared conventions**
- **Units.** Almost nothing here runs a BCC field kernel. The astrophysics modules use geometric units ($G=c=1$, lengths in $M$ or km). The running modules use GeV. Only `thermodynamics*.py` works in lattice units ($\Theta=k_BT\tau/\hbar$, $c_\text{lat}=1/\sqrt3$, F26), with the SI tick taken from $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107).
- **Lattice.** Several strong-sector kernels (`running_njl`, `running_gap_solve`, `running_scheme_constant`, `running_qstar_logmoment`) use the **simple-cubic** kernel $\hat K=\sum_i2(1-\cos q_i)$. That is the D1 reference lattice, not BCC. Each block flags it.
- **Registry exactness.** 16 of the 20 modules are `manifest` records with `exactness=None`, so their equations are tagged `unknown` unless `exactness-inventory.md` names the result.
- **Brackets.** `alpha_eff_star` is **bracketed** $(0.376,0.411)$ (F88/F117/F145/F151). Only its endpoints are results. Where the code forms a midpoint, the block flags it.

**Modules covered:** `qnm.py`, `raytrace.py`, `run_q3_omega_degeneracy.py`, `running_alpha_lattice_bound.py`, `running_alpha_s.py`, `running_gap_solve.py`, `running_ir_coupling.py`, `running_njl.py`, `running_qstar_logmoment.py`, `running_scale_ratio.py`, `running_scheme_constant.py`, `slowlight.py`, `stellar.py`, `superconductivity.py`, `thermodynamics.py`, `thermodynamics_gstar.py`, `thermodynamics_interacting.py`, `tolman.py`, `unified.py`, `vacuum_energy.py`.

---

### `engine/interactions/qnm.py` — Schwarzschild quasinormal ringdown (WKB)
**Status:** live · test-only · **Findings:** — (docstring: F187, F183; F178 canonical BH) · **Lattice:** n/a · **Law:** n/a · **Units:** geometric ($G=c=1$, $M=1$)

**Does:** Computes the axial (Regge–Wheeler, spin-2) QNM frequencies of the canonical F178 Schwarzschild hole by first-order WKB, compares them with tabulated GR values, and gives an order-of-magnitude echo bound.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $V(r)=(1-2M/r)\,[\ell(\ell+1)/r^2-6M/r^3]$ | Regge–Wheeler potential | `qnm.py:L38 rw_potential()` | unknown |
| 2 | $V_0''\big\rvert_{r_*}=f_0^2\,\partial_r^2V$, $f_0=1-2M/r_0$ (3-point FD on a 2,000,001-point grid over $r\in[2.001M,12M]$) | curvature at the peak in the tortoise coordinate, using $\partial_rV=0$ there | `qnm.py:L50–51 _peak()` | unknown |
| 3 | $\omega^2=V_0-i(n+\tfrac12)\sqrt{-2V_0''}$, root taken with $\mathrm{Re}\,\omega>0$ and $\mathrm{Im}\,\omega<0$ | WKB-1 QNM frequency | `qnm.py:L58–62 qnm_wkb()` | quantitative (inv #220, F184–F192: WKB QNM <7%) |
| 4 | $h(t)=e^{-t/\tau}\cos(\omega_Rt)$, $\tau=1/\lvert\omega_I\rvert$, $Q=\omega_R/(2\lvert\omega_I\rvert)$ | ringdown waveform and quality factor | `qnm.py:L84–86 ringdown_waveform()` | unknown |
| 5 | $T\sim\exp(-2\pi\,b_c\,\omega)$ with $b_c=3\sqrt3$, $\omega M=0.3737$ (literal) | "illustrative" single-barrier transmission for the echo bound | `qnm.py:L101 echo_amplitude_bound()` | unknown |

**Inputs → outputs:** $(\ell,n,M)$ → complex $\omega$, plus relative error against `QNM_TAB` (Berti–Cardoso–Will literals, L27–33).
**Depends on:** numpy only. Geometry per 07b (F178/F183).
**Flags:** The registry records no finding, although the docstring names F187. Exactness is unknown for every row (the inventory row 220 grades F187 as "WKB QNM <7%", i.e. quantitative). Row 5 is a hard-coded scale, not a computation: the docstring says a real bound needs a Teukolsky solve.

### `engine/interactions/raytrace.py` — black-hole shadow by null-geodesic ray tracing
**Status:** partial · test-only · **Findings:** — (docstring: F186; F178; F114 as exclusion record) · **Lattice:** n/a · **Law:** n/a · **Units:** geometric for orbits; SI for the on-sky angles

**Does:** Bisects the capture/escape boundary of Schwarzschild photon orbits numerically to recover $b_c=3\sqrt3M$, converts the shadow to µas for M87\* and Sgr A\*, and reports Kerr shadow extents.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u''=3Mu^2-u$, $u=1/r$ (Binet), RK4 in $\phi$; capture when $u\ge1/(2M)$, escape when $u\le0$ | photon-orbit integrator | `raytrace.py:L45–56 _plunges()` | quantitative (inv #220, F184–F192: $b_c$ numeric <1e-3) |
| 2 | bisection on $b\in[4,7]$, 40 iterations | numerical $b_c$ | `raytrace.py:L60–69 numeric_shadow_b()` | quantitative (inv #220, F184–F192) |
| 3 | $\theta_\text{diam}=2\,b_c\,(GM/c^2)/D$, converted to µas | on-sky shadow diameter | `raytrace.py:L78–81 angular_shadow_uas()` | unknown |
| 4 | GR uses $b_c=3\sqrt3M$. The excluded F114 value is $2eM$, with enlargement $100\,[2e/(3\sqrt3)-1]\%$ | EHT predictions plus the standing exclusion record | `raytrace.py:L113–118 eht_predictions()` | exact (inv #220, F184–F192: $b_c=3\sqrt3M$) |
| 5 | Kerr outline delegated to `blackhole.kerr_shadow_outline` | spin dependence | `raytrace.py:L127 kerr_shadow_extents()` | unknown (inferred: see 07b) |

**Inputs → outputs:** $(M_\odot, D)$ → µas diameters; spin → Kerr width, height and offset.
**Depends on:** `interactions.blackhole` (07b), `G_CODATA` and `c_SI` (external, CODATA). $M_\odot=1.98892\times10^{30}$ kg and Mpc $=3.0857\times10^{22}$ m are unregistered module literals (L77).
**Flags:** The `*_F114` fields are **SUPERSEDED by F178** (S-record for F114; the ledger code note says this was resolved at C6 by relabelling). They are kept as a live exclusion gate for test_F186 T2. Two separate issues: the initial condition `du = 1/b` is a coarse aim, and the local `sys.path.insert` at L26 is plumbing.

### `engine/interactions/run_q3_omega_degeneracy.py` — is $g_{\omega NN}$ deuteron-observable? (Q3)
**Status:** live · standalone · **Findings:** F113 F240 F247 · **Lattice:** n/a · **Law:** n/a · **Units:** MeV, fm

**Does:** Maps the deuteron binding valley in the (quark-Pauli core strength $g_\text{cm}$, $\omega$ coupling) plane. The point is to show that $g_{\omega NN}$ is degenerate with the core, so it is a genuine free input (F247).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g_{\omega,\text{univ}}^2/4\pi=9\,g_{\rho\pi\pi}^2/4\pi$ with $g_{\rho\pi\pi}=m_\omega/(\sqrt2 f_\pi)$ (KSRF; ratio $g_\omega/g_\rho=3$ from F240). Evaluates to 25.88 | universality ceiling | `run_q3_omega_degeneracy.py:L31` | quantitative (reg) |
| 2 | $E_b(g_\text{cm},g_\omega^2/4\pi)$ from `nuclear.solve_deuteron(core="derived", b=0.55\,\text{fm}, σ, ω, tensor, N=500)` | deuteron binding | `…:L34–38 Eb()` | quantitative (reg) |
| 3 | bisect $g_\omega^{*}$ such that $E_b=2.224$ MeV | valley point | `…:L41–53 bisect_gw()` | quantitative (reg) |
| 4 | linear fit $g_\omega^{*2}/4\pi=11.13-0.313\,g_\text{cm}$, max residual $\le0.03$ | degeneracy = linearity | `…:L118–124 check_degeneracy()` | quantitative (reg) |
| 5 | quench $=g_\omega^*/g_{\omega,\text{univ}}$: 0.208 at $g_\text{cm}=18.31$ (N-Δ derived), 0.431 core-off | F247's correction to F240 | `…:L132–138 check_degeneracy()` | quantitative (reg) |

**Inputs → outputs:** anchor cores $(0, 9.155, 18.31, 27.47)$ MeV → $g_\omega^*$ valley, fit, and quenches.
**Depends on:** `particles.nuclear` (06a/06b) for `solve_deuteron`, `M_OMEGA_DEFAULT`=782.66, `F_PI_DEFAULT`=92.07, `GCM_DEFAULT`.
**Flags:** `main()` writes a JSON artifact, but only under `__main__` (OK). Target 2.224 MeV, $b=0.55$ fm and $R_\text{max}$ are unregistered literals. The code comment at L105–110 records that the finding's table misprints the 8.26 row (the solver gives 8.2549).

### `engine/interactions/running_alpha_lattice_bound.py` — B9 re-derivation, post-F277 (F322) + hadronic VMD (F334)
**Status:** live · standalone · **Findings:** F322 F251 F277 F261 F115 F138 F231 · **Lattice:** 4-D Euclidean BZ grid (inherited from `qed_vacuum_polarization`; see 07c/07d) · **Law:** n/a · **Units:** MeV/GeV, continuum $\alpha$

**Does:** Six checks. It shows the leptonic $\Delta\alpha(M_Z)$ is independent of the F277 refold, bounds the lattice contribution to $\Delta\alpha$, attributes the 0.24% PDG shortfall to the two-loop leading log, and measures how much of the electroweak leg's precision depends on the $\alpha_\text{em}$ input. It also (F334) adds a model-internal ρ+ω VMD estimate of the hadronic piece.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Delta\alpha_\text{lep}$ recomputed after replacing the kernel with $\hat K\to7.3\hat K+0.5$ must be bitwise equal | L1: refold independence (call-closure test) | `running_alpha_lattice_bound.py:L116–126 refold_independence()` | quantitative (reg) |
| 2 | $f=(\alpha/3\pi)\big/\big(b_0^\text{QED}/16\pi^2\big)=4\pi\alpha$, with $b_0^\text{QED}=4/3$ | L2a: conversion from B-units to $\Delta\alpha$ | `…:L144–145 b_to_dalpha_factor()` | exact (inv #324, F322) |
| 3 | $B=\big(\langle N_{00}/D\rangle-\langle N_{11}/D\rangle\big)/Q^2$, with $N_{mn}=4(k_mk'_n+k_nk'_m-\delta_{mn}k\cdot k')$, $D=\hat K(k)\hat K(\text{refold}(k+Q))$ | control re-implementation of `vp._fermion_B` with the F277 modular refold restored | `…:L163–176 _fermion_B_refold()` | quantitative (reg) |
| 4 | bound $=f\cdot\dfrac{\text{spread}_Q(B_\text{rule}-B_\text{cont})}{\ln(Q_\max^2/Q_\min^2)}\cdot\ln(M_Z^2/m_e^2)$ | L2: lattice bound on $\Delta\alpha(M_Z)$ | `…:L193–196 lattice_bound_on_dalpha()` | quantitative (inv #324, F322) |
| 5 | $\Delta\alpha^{(1)}_\ell=\frac{\alpha}{3\pi}\big[\ln(M_Z^2/m_\ell^2)-\tfrac53\big]$; $\Delta\alpha^{(2)}_\ell=b_1\frac{\alpha^2}{4\pi^2}\ln(M_Z^2/m_\ell^2)$ with $b_1=1$ (F261, sympy) | L3: one-loop plus two-loop leading-log leptonic running | `…:L238–240 two_loop_leading_log()` | quantitative (inv #325, F322; inv gen-T3 B9-5); $b_1$ exact (inv #298, F261) |
| 6 | $b_1=\tfrac43n_g+\tfrac{n_H}{10}$, $b_2=-\tfrac{22}{3}+\tfrac43n_g+\tfrac{n_H}{6}$ ($n_H=0$, Higgs-free), $b_\text{em}=b_2+\tfrac53b_1$, $\mu_*=4\pi v$; $\alpha_2^{-1}(M_Z)=\sin^2\theta_W^{UV}\big[\alpha_\text{em}^{-1}-\tfrac{b_\text{em}}{2\pi}L\big]+\tfrac{b_2}{2\pi}L$, $\sin^2\theta_W(M_Z)=\alpha_2^{-1}/\alpha_\text{em}^{-1}$, $\sin^2\theta_W^{UV}=1/4$ (F45/F231) | L4: one-loop EW leg (F138) | `…:L274–281 _sin2_MZ()` | quantitative (inv #326, F322) |
| 7 | $\alpha^{-1}_{\overline{MS},\text{model}}=\alpha^{-1}_\text{lep,2L}-(\alpha^{-1}_\text{OS,meas}-127.951)$ | on-shell → MS-bar shift before the EW leg | `…:L296–298 ew_leg_alpha_dependence()` | quantitative (inv #326, F322) |
| 8 | $g_{\rho\pi\pi}=m_V/(\sqrt2f_\pi)$ (KSRF); $g_{\omega,EM}/g_{\rho,EM}=(Q_u-Q_d)/(Q_u+Q_d)=3$ | F334 couplings (ratio sympy-exact) | `…:L421–423`, `…:L399–402 _quark_charge_photon_weights()` | quantitative (reg) |
| 9 | $\Delta\alpha_V(s)=\dfrac{4\pi\alpha}{g_V^2}\,\dfrac{s}{s-m_V^2}$ (narrow-resonance VMD with $\Gamma_{ee}$ eliminated) | hadronic ρ, ω pieces | `…:L473 _dalpha_V_exact()` | quantitative (inv gen-T3 V1, F334) |
| 10 | $\Gamma_{ee}=4\pi\alpha^2m_V/(3g_\rho^2)$; quench $=\sqrt{\Gamma_{ee}^\text{pred}/\Gamma_{ee}^\text{PDG}}$ | V5 universality check | `…:L437–438 hadronic_vmd_narrow_resonance()` | quantitative (reg) |

**Inputs → outputs:** $\alpha$, lepton masses, PDG references (from `vp`) → leg verdicts B9-1…B9-6 and F334 V1…V6.
**Depends on:** `qed_vacuum_polarization`, `qed_twoloop_ae` (07c/07d), `particles.nuclear` (06a/06b), `sin2_thetaW_uv_f`.
**Flags:** The F334 section is live code, but **F334 is not among the registry findings** for this module. Both ρ and ω use `nuc.M_OMEGA_DEFAULT` as $m_V$ (this relies on the F240 ρ–ω degeneracy). The code never uses $m_\rho$. The PDG/EW reference numbers 127.951, 0.23122, 246.22, 91.1876, 0.02760 and 7.04e-3 are bare literals, which the module declares as external anchors.

### `engine/interactions/running_alpha_s.py` — Route A: $\alpha_s$ from the rotor lock (F144)
**Status:** live · test-only · **Findings:** — (docstring: F144, F101, F110, F107, F124) · **Lattice:** cubic $L^3$ FFT grid for the F26 step check · **Law:** even (F26 rotation step via `weak_wmu._f26_rotation_step`) · **Units:** GeV

**Does:** Derives the bare lock $g_s^2=1/4$, so $\alpha_s(\mu_0)=1/(16\pi)$ at $\mu_0=\hbar c/a$. It then runs $\alpha_s$ down at 1–4 loops in MS-bar and reports $\alpha_s(M_Z)$, $\Lambda^{(3,5)}$, and the implied scheme shift.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | per-mode $R=\begin{psmallmatrix}E_1&E_2\\B_1&B_2\end{psmallmatrix}$: residuals of $R^TR=1$, $\det R=1$, $E_1=B_2$ | the F26 step is an exact circular rotation | `running_alpha_s.py:L94–98 rule_step_rotation_residual()` | machine (inv §F144 #92) |
| 2 | $M(t)=\begin{psmallmatrix}\cos wt&(b/w)\sin wt\\-(a/w)\sin wt&\cos wt\end{psmallmatrix}$, $w=\sqrt{ab}$; $M^TM-I=\sin^2 wt\,\mathrm{diag}(a/b-1,\,b/a-1)$, so orthogonal ⇔ $a=b$ | lemma: circular flow ⇔ equal stiffness ($\chi=1$) | `…:L124–140 circular_iff_equal_stiffness()` | exact (inv §F144 #92) |
| 3 | $H_\text{dual}^{1\text{-plaq}}(g^2)=H_\text{rotor}(\chi=1/4g^2)$ as matrices; with $\chi=1$ this gives $g_s^2=1/4$ | F110 C7 identity | `…:L163–168 chi_lock_identity()` | exact (inv §F144 #92: matrix resid = 0) |
| 4 | $\alpha_s^{UV}=g_s^2/4\pi=1/(16\pi)$; $\mu_0=E_P/(a/\ell_P)$ with $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107) | UV boundary condition | `…:L72`, `…:L63` | exact (inv §F144 #92) |
| 5 | $\dfrac{da}{d\ln\mu}=-2a^2\sum_{i<\text{loops}}b_ia^i$, $a=\alpha_s/4\pi$; $b_0=11-\tfrac23n_f$, $b_1=102-\tfrac{38}{3}n_f$, $b_2$, $b_3$ (van Ritbergen–Vermaseren–Larin) | MS-bar β, RK4 in $\ln\mu$ (4000 steps), Landau-pole guard | `…:L182–198 _beta_coeffs(), _beta()`, `…:L201–215 run_alpha()` | unknown (RK4, 4000 steps in code) |
| 6 | $\mu_0\to m_t$ ($n_f=6$) $\to M_Z\to m_b$ ($n_f=5$) $\to m_c$ ($n_f=4$), continuous matching | threshold chain | `…:L222–227 alpha_s_chain()` | quantitative (inv §F144 #93) |
| 7 | $\Lambda=\mu\,(b_0a)^{-b_1/(2b_0^2)}e^{-1/(2b_0a)}$ | 2-loop $\Lambda_{\overline{MS}}$ | `…:L233–235 lambda_msbar_2loop()` | unknown |
| 8 | $\Delta(1/\alpha)=1/\alpha_\text{meas}(\mu_0)-16\pi$; $\Lambda$-ratio $=\exp\!\big[\Delta/(2\,b_0/4\pi)\big]$ | implied scheme shift | `…:L252–256 implied_scheme_shift()` | quantitative (inv §F144 #93) |

**Inputs → outputs:** loops → $\alpha_s(M_Z)$, $\Lambda_3$, $\Lambda_5$, hierarchy $N=\Lambda_3/\mu_0$, scheme diagnostic.
**Depends on:** `gauge.weak_wmu._f26_rotation_step` and `gauge.link_hamiltonian` (05b/05c), `a_over_ellP` (01).
**Flags:** $E_P=1.220890\times10^{19}$ GeV, $m_t$, $m_b$, $m_c$, $M_Z$, `ALPHA_S_MZ_PDG` and `LAMBDA3_FLAG` are unregistered literals, labelled as targets. CLAUDE.md's table names the step `casim.engine.gauge.wmu._f26_rotation_step`, but the code imports `casim.engine.gauge.weak_wmu` (the file on disk is `weak_wmu.py`). The docstring's STEP-4 formula for $d_1$ is garbled ("… + d1/(2 pi) * (2 pi) ..."); the code computes only the implied shift in row 8. Exactness is unknown for every row (manifest record).

### `engine/interactions/running_gap_solve.py` — full nonlinear chiral-SB gap $M(k)$ (F145/F151-S5/F155)
**Status:** live · test-only · **Findings:** — (docstring: F145, F151, F77, F88, F117, F155) · **Lattice:** **simple-cubic** $L^3$ BZ, $\hat K=\sum_i2(1-\cos k_i)$ (D1 reference) · **Law:** n/a · **Units:** lattice, with 1 lattice unit $=\Lambda_\text{NJL}/\pi$

**Does:** Solves the momentum-resolved NJL gap equation self-consistently, and inverts it for the IR coupling that gives $M(0)=1.50$ (the F77 constituent mass).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G_S(q)=c_F\,\dfrac{g^2/2}{\epsilon_cK(q)+M_g^2}$, $c_F=2/9$ (F77/F116); running mode uses $g^2\to g^2(\mu_q)$ with $\mu_q=\sqrt{K+M_g^2}\,\Lambda_\text{NJL}/\pi$ | resolved gluon-exchange kernel | `running_gap_solve.py:L74`, `…:L76–78 gap_solve()` | unknown |
| 2 | $M_{n+1}(k)=m_0+24\,\big\langle G_S(k-q)\,M(q)/\sqrt{K(q)+M(q)^2}\big\rangle_q$ via FFT convolution, clipped $\ge0$ and mixed 50/50 | gap iteration (24 = 4 Dirac × 3 colour × 2 flavour) | `…:L87–90 gap_solve()` | quantitative (inv T1 #199, F154-B) (tol 1e-10 in code) |
| 3 | bisect $\alpha_\text{eff}=g^2/4\pi$ such that $M(0)=1.50$ | inverse solve: gives the endpoints of `alpha_eff_star` | `…:L111–131 alpha_eff_for_target()` | quantitative (inv T1 #199, F154-B); endpoints are the registered bracket `alpha_eff_star` |
| 4 | $f_\pi^2\approx4N_c\,\langle M^2/(K+M^2)\rangle$ | Pagels–Stokar lattice proxy | `…:L163 f_pi_pagels_stokar()` | unknown |
| 5 | onset $\alpha$ where $M(0)$ crosses 0.30 (bisection) | anchor-free chiral-SB onset | `…:L176–184 chiSB_onset()` | quantitative (inv §F155 #203) |
| 6 | window $[\text{onset},\alpha_\text{phys}]$ and `freeze_midpoint` $=\tfrac12(\text{onset}+\alpha_\text{phys})$ | F155 freeze bracket | `…:L215–221 freeze_window()` | quantitative (inv §F155 #203); a bracket, midpoint display only |

**Inputs → outputs:** $(M_g,g^2)$ → $M(0)$, MeV conversion, $\alpha_\text{eff}^*$, onset, freeze window.
**Depends on:** `running_njl` (`_K`, `g2_running`, `criticality_R`). Constants: `c_fierz_colour_f`$=2/9$ (F77), `GeV_per_lattice_unit`$=\Lambda_\text{NJL}/\pi$ with $\Lambda_\text{NJL}=0.6515$ GeV fitted (F77/F116), `M0_constituent_lattice`$=1.50$ (F77), `m0_current_quark_MeV`$=5.5$ (fitted, F77/F116), `Lambda_QCD_nf3_GeV`$=0.347$ (F151).
**Flags:** Uses the cubic reference kernel (D1), not BCC. `freeze_midpoint` is the **midpoint of a bracket**, which is display only and not a result. FFTs act on real data and the code takes the real part, so there is no chiral hazard.

### `engine/interactions/running_ir_coupling.py` — the IR face of the strong coupling (F152)
**Status:** live · test-only · **Findings:** — (docstring: F152, F151, F145, F150) · **Lattice:** n/a · **Law:** n/a · **Units:** GeV

**Does:** Packages the IR coupling bracket $\alpha_\text{eff}^*$, checks that a gluon-mass-regulated one-loop coupling saturates, and compares with continuum frozen-coupling data.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\alpha_\text{eff}^*\in[0.376,\,0.411]$ via `endpoint("alpha_eff_star","lo"/"hi")` (F88/F117/F145/F151) | IR bracket | `running_ir_coupling.py:L48–49` | unknown (inferred: bracketed (constants registry `alpha_eff_star`)) |
| 2 | `alpha_eff_star_mean` $=\tfrac12(\text{lo}+\text{hi})$; spread $=(\text{hi}-\text{lo})/\text{mean}$ | J1 summary | `…:L66–70 ir_coupling_value()` | unknown (inferred: bracketed (constants registry; midpoint display only)) |
| 3 | $\alpha(Q^2)=\dfrac{4\pi}{b_0\ln[(Q^2+4m^2)/\Lambda^2]}$, $b_0=9$ ($n_f=3$), evaluated at $Q^2=0$ with $m=\sqrt\sigma=0.42$ GeV (F122/F124/F146) | J2 saturating (massive) one-loop coupling | `…:L83–87 saturating_branch()` | quantitative (inv T1 #195, F152-J2) |
| 4 | $\Lambda_3$ from `running_alpha_s` 2-loop chain | scale input | `…:L78–79` | unknown |
| 5 | $0.30\le\text{mean}\le0.50$; $\lvert\sqrt\sigma-m_g\rvert\le0.35$ GeV | J3 continuum grounding tests | `…:L105–107 continuum_grounding()` | unknown |

**Inputs → outputs:** none → J1–J5 report dicts.
**Depends on:** `running_alpha_s`. Constants: `alpha_hat0_over_pi_CZBR`=0.97 (external), `m_g_continuum_GeV`=0.50 (external), `sqrt_sigma_GeV`=0.42 (F122/F124/F146), `lambda_6`=0.243 (F234 output).
**Flags:** J3 uses the **bracket midpoint** as a result (the range test at L106–107). The brief says a midpoint is never a result. J2 sets the dual-Meissner scale $m_D$ equal to $\sqrt\sigma$ by assignment (L81). `M_G_ERR` and the 0.30/0.50 range edges are unregistered literals.

### `engine/interactions/running_njl.py` — Route C: induced NJL coupling (F145)
**Status:** live · test-only · **Findings:** — (docstring: F145, F116, F117, F88, F144, F77) · **Lattice:** **simple-cubic** $L^3$ BZ (D1 reference) · **Law:** n/a · **Units:** lattice, GeV for running

**Does:** Computes the exact Fierz coefficient of one-gluon exchange into the NJL channels. It then builds the momentum-resolved lattice gap kernel and finds its criticality eigenvalue $R=G/G_c$ in contact, resolved and running modes.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathcal O=\sum_{\mu,a}\eta_{\mu\mu}(\gamma^\mu T^a)\otimes(\gamma_\mu T^a)$ on the 24-dim Dirac⊗colour⊗flavour space; exchanged projection $c(\Gamma_1,\Gamma_2)=\tilde{\mathcal O}_{abcd}\Gamma^\dagger_{1,ba}\Gamma^\dagger_{2,dc}/(\lVert\Gamma_1\rVert^2\lVert\Gamma_2\rVert^2)$; result $c=2/9$ in all four chiral channels | C1 exact Fierz | `running_njl.py:L125–156 fierz_coefficients()` | exact (inv §F145 #96) |
| 2 | $\sum\eta\,\gamma^\mu T^a\gamma_\mu T^a=4C_F\,\mathbb 1=\tfrac{16}{3}\mathbb 1$ | Fock identity | `…:L164–172 fock_kernel_identity()` | exact (inv §F145 #96) |
| 3 | $\hat K=\sum_i2(1-\cos k_i)$ | cubic lattice kernel | `…:L179–181 _K()` | unknown |
| 4 | $g^2(\mu)=4\pi\Big/\Big[\tfrac{9}{2\pi}\ln\big(\sqrt{\mu^2+\mu_\text{fr}^2}/\Lambda_3\big)\Big]$, 1-loop, $n_f=3$, IR-frozen | running coupling | `…:L186–188 g2_running()` | unknown |
| 5 | $R=$ largest eigenvalue of $M(k)=24\,\langle G_S(k-q)M(q)/\sqrt{K(q)+M_\text{reg}^2}\rangle_q$, with $G_S$ contact $=c_F(g^2/2)/M_g^2$, resolved $=c_F(g^2/2)/(\epsilon_cK+M_g^2)$, running uses $g^2(\mu_q)$ | criticality by power iteration | `…:L205–228 criticality_R()` | quantitative (inv §F145 #97) (tol 1e-12 in code) |
| 6 | $R_\text{contact}=24c_F(g_s^2/2)/M_g^2\cdot\langle1/\sqrt{K}\rangle$ | C2 analytic anchor | `…:L234–236 contact_anchor()` | machine (inv §F145 #97: contact anchor 5e-15) |
| 7 | $\alpha_\text{crit}=1/(4\pi R_0)$ with $R_0=R(g^2{=}1)$; $\alpha_\text{fit}=1.277/(4\pi R_0)$; $\hat g=R\cdot\pi^2/6$ | C4/C5 derived quantities | `…:L265–266, L276–279 route_c_report()` | quantitative (inv §F145 #97) |

**Inputs → outputs:** $M_g$ (F88 0.532 / F117 0.727) → $R$ values, $\alpha_\text{crit}$, $\hat g$ ranges.
**Depends on:** constants `c_fierz_colour_f`=2/9 (F77), `m_D_F88_lattice`, `m_V_F117_lattice`, `Lambda_NJL_GeV` (fitted), `G_Lambda2_NJL`=2.1 (fitted).
**Flags:** Uses the cubic reference kernel (D1). `G_S2_BARE=0.25` (F144 lock), `LAMBDA3_1L=0.272`, `GGC_F77=1.277` and `GC_LAM2=π²/6` are unregistered literals. The $\lambda_8$ normalisation $1/\sqrt3$ at L112 is registered as a `coincidence` with `c_lat` (01, measured.py L85).

### `engine/interactions/running_qstar_logmoment.py` — first-principles matching scale $q^*$ (Residual A)
**Status:** live · test-only · **Findings:** — (docstring: F151) · **Lattice:** **simple-cubic/hypercubic** midpoint BZ, $d=3,4$ (D1 reference) · **Law:** n/a · **Units:** $1/a$

**Does:** Estimates the BLM/Lepage–Mackenzie scale as a weighted log-moment of the lattice gluon kernel, and compares it with F151's implied $q^*a=0.733$ and the band $[1/\sqrt3,1]$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\hat K=\sum_{i=1}^d2(1-\cos q_i)$ on a midpoint grid (avoids $q=0$) | kernel | `running_qstar_logmoment.py:L47–50 _Khat()` | unknown |
| 2 | $q^*a=\exp\big(\tfrac12\langle\ln\hat K\rangle_w\big)$ with $w\in\{1,\ 1/\hat K,\ 1/\hat K^2\}$ | log-moment scale | `…:L65–66 logmoment_qstar()` | quantitative (inv T1 #200, F154-A; $\langle\ln K\rangle_{4D}=2$ exact) |
| 3 | band $=[1/\sqrt3,\,1]$ (`q_star_a_band_lo`, F151/F155); geometric mean $3^{-1/4}$ | comparison band | `…:L41–42` | unknown |

**Depends on:** `running_scheme_constant.implied_qstar`, `a1`.
**Flags:** The cubic reference kernel is used for the "rule's gluon kinetic kernel", but the canonical lattice is BCC (D1). `GEOM_MEAN_BAND = 3**-0.25` is an unregistered literal (the same value appears as `QSTAR_GEO` in `running_scheme_constant`).

### `engine/interactions/running_scale_ratio.py` — $\sqrt\sigma/f_\pi$ from two lattice factors (F123 debt)
**Status:** live · driven (3 ch) · **Findings:** — (docstring: F123, F77, F103, F86, F88, F100, F101, F115, F116) · **Lattice:** n/a (lattice-unit scalars) · **Law:** n/a · **Units:** GeV and lattice $1/a$

**Does:** Factors $\sqrt\sigma/f_\pi=(\Lambda/f_\pi)\times(\sqrt\sigma/\Lambda)$. The first factor comes from the NJL/Pagels–Stokar solver. The second comes from one of two confinement sources and one of two BZ-cutoff conventions.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G=G\Lambda^2/\Lambda^2$; $M=$ NJL gap; $f_\pi$ from `meson.f_pi`; check $f_\pi/M=2\sqrt{N_cK_0}$ | chiral factor $\Lambda/f_\pi$ | `running_scale_ratio.py:L80–94 njl_chiral_ratios()` | machine (inv gen-T2 C1, F124: $f_\pi/M$); $\Lambda/f_\pi$ quantitative (inv gen-T3 C2, F124) |
| 2 | $\Lambda_\text{lat}=\pi$ (axis) or $(6\pi^2)^{1/3}$ (sphere of equal BZ volume) | cutoff convention | `…:L102–105 bz_cutoff_lattice()` | unknown |
| 3 | $\sigma_\text{lat}=2\pi v^2$ with $v=0.713$ (F88), or $\sigma_\text{lat}=0.2015$ (bare rotor, F101); ×2 for the Casimir option; returns $\sqrt{\sigma_\text{lat}}$ | confinement factor | `…:L111–119 sigma_lattice()` | quantitative (inv gen-T3 C5, C6, F124) |
| 4 | $\sqrt\sigma/f_\pi=(\Lambda/f_\pi)\cdot\sqrt{\sigma_\text{lat}}/\Lambda_\text{lat}$ | headline ratio | `…:L125–129 sqrt_sigma_over_fpi()` | quantitative (inv T3 #43, F124) |

**Depends on:** `particles.meson` (06b); constants `Lambda_NJL_GeV`, `G_Lambda2_NJL`, `m0_current_quark_MeV` (all fitted, F77/F116), `sqrt_sigma_GeV`=0.42.
**Flags:** The docstring calls the chiral factor 7.04 "EXACT", but it is a numerical NJL solve on fitted inputs. The registry has exactness=None, so it is tagged unknown here. `V_F88=0.713`, `SIGMA_ROTOR=0.2015` and `F_PI_PHYS=0.09207` are unregistered literals. The docstring labels `SIGMA_ROTOR` "(F100/F101, 2D)".

### `engine/interactions/running_scheme_constant.py` — rule → MS-bar scheme constant (F151)
**Status:** live · test-only · **Findings:** — (docstring: F151, F144, F145, F110, F124) · **Lattice:** mixed: exact-symbol $\lvert k\rvert^2$ Green's function (S1), 4-D Wilson kernel (S2), **simple-cubic** kernel (S5) · **Law:** n/a · **Units:** GeV, $1/a$

**Does:** Identifies $\alpha_\text{rule}=\alpha_V$, applies the exact one-loop V→MS-bar constant $a_1$, and fixes the residual as a matching scale $q^*$ in the band $[1/\sqrt3,1]/a$. It also recomputes the IR face.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $a_1(n_f)=(31C_A-20T_Fn_f)/9$; $a_1(6)=11/3$; $\Delta(1/\alpha)=a_1/4\pi$; $\Lambda_V/\Lambda_{\overline{MS}}=\exp[a_1/(2b_0)]$ | exact scheme constant | `running_scheme_constant.py:L85`, `…:L93–94 a1_ledger()` | exact (inv #268, F239: $\Lambda$ ratio $=\exp(a_1/2b_0)$) |
| 2 | ground energy at $\lambda=0$: $E_0(R)=\tfrac{g^2}{2}R$ for a unit string of length $R$ | static-energy lock (V-scheme identification) | `…:L114–115 static_energy_lock()` | unknown |
| 3 | $\phi(R)=L^{-3}\sum_k e^{ikR}/\lvert k\rvert^2$ vs image-summed $1/(4\pi d)$, compared as differences | exact-symbol Coulomb check | `…:L127–151 spectral_coulomb_check()` | unknown |
| 4 | $Z_0=\langle1/\hat K\rangle_{BZ^4}$, $\hat K=4\sum\sin^2(k/2)$, known value 0.154933 | Wilson tadpole contrast | `…:L166–168 wilson_tadpole()` | unknown |
| 5 | $1/\alpha_{\overline{MS}}(q^*)=16\pi+a_1(6)/4\pi$, then `run_alpha` chain from $\mu=q^*\mu_0$ | corrected chain | `…:L179–185 corrected_chain()` | unknown |
| 6 | bisect $q^*\in[0.3,1.2]$ such that $\alpha_s(M_Z)=0.1180$ | implied $q^*$ (≈0.733) | `…:L195–202 implied_qstar()` | unknown |
| 7 | same gap iteration as `running_gap_solve` row 2 (with $m_0=0$, $\epsilon_c=1$), bisect for $M(0)=1.50$ | IR face $\alpha_\text{eff}^*$ | `…:L215–235 ir_alpha_eff()` | unknown |

**Depends on:** `running_alpha_s` (RA), `gauge.link_hamiltonian`; constants `c_fierz_colour_f`, `m_D_F88_lattice`, `m_V_F117_lattice`, `q_star_a_band_lo`$=1/\sqrt3$, `M0_constituent_lattice`.
**Flags:** Row 7 duplicates the gap iteration in `running_gap_solve` (a separate copy that can drift). The S5 kernel is the cubic reference (D1). `QSTAR_GEO=3**-0.25` is unregistered.

### `engine/interactions/slowlight.py` — slow/fast light as a test of the rotation-rate picture
**Status:** live · test-only · **Findings:** — (docstring: F26, CLAUDE.md decision 2; "Track 1.b") · **Lattice:** n/a (continuum optics; the $O(k^3)$ term is quoted for BCC) · **Law:** n/a (real SO(2) rotation per Fourier mode) · **Units:** SI

**Does:** Propagates optical pulses through EIT and gain-doublet media two ways, as a complex phase and as a real $(E,B)$ rotation. It shows the two agree and bounds the lattice dispersion term.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\chi(\delta)=\dfrac{i\alpha_0}{\gamma_\text{opt}+i\delta+(\Omega_c^2/4)/(\gamma_\text{gnd}+i\delta)}$ | EIT susceptibility (FIM 2005) | `slowlight.py:L74–75 eit_susceptibility()` | unknown |
| 2 | $\chi(\delta)=-M\big[(\delta-s+iw)^{-1}+(\delta+s+iw)^{-1}\big]$ | Raman gain doublet | `…:L87–88 gain_doublet_susceptibility()` | unknown |
| 3 | $n=\mathrm{Re}\sqrt{1+\chi}$; $v_p=c/n$; $n_g=n+\omega\,dn/d\omega$ (central difference), $v_g=c/n_g$ | index, phase and group velocity | `…:L97`, `…:L102`, `…:L114–116 group_index_and_velocity()` | unknown |
| 4 | $E_L(t)=\mathcal F^{-1}\big[\mathcal F E_0\cdot e^{-i\,\mathrm{Re}\beta L}\,e^{\text{clip}(-\mathrm{Im}\beta L)}\big]$, $\beta=\sqrt{1+\chi}\,\omega/c$ | complex-phase propagation | `…:L137–148 propagate_phase()` | unknown |
| 5 | per mode $\begin{psmallmatrix}E\\B\end{psmallmatrix}\to A\begin{psmallmatrix}\cos\Phi&-\sin\Phi\\\sin\Phi&\cos\Phi\end{psmallmatrix}\begin{psmallmatrix}E\\B\end{psmallmatrix}$, $\Phi=-\mathrm{Re}\beta L$, with $E_k=\mathcal F[\mathrm{Re}E_0]$, $B_k=\mathcal F[\mathrm{Im}E_0]$; output $\mathcal F^{-1}E'+i\mathcal F^{-1}B'$ | "real (E,B) rotation" propagation | `…:L171–179 propagate_rotation()` | unknown |
| 6 | $v_\text{front}=c/n(\omega\to\infty)$ sampled at $\delta=10^6\omega_0$ | front velocity | `…:L198–200 front_velocity_index()` | unknown |
| 7 | $(a\,k)^2$, $k=2\pi/\lambda_\text{vac}$, "C absorbed" | size of the lattice $O(k^3)$ term | `…:L216–217 lattice_liv_fraction()` | unknown |

**Depends on:** `c_SI`, `casim.numerics.fft`.
**Flags:** Row 5 is **a chiral-transform hazard only in name**. $\Phi(\omega)$ is not odd about zero frequency, so after the inverse FFT the "real" $E'$ and $B'$ are complex. The equality with row 4 holds by linearity, $\mathcal F^{-1}[e^{i\Phi}(E_k+iB_k)]$. It is not evidence that a real-pair evolution was carried out. Row 7: the docstring says $C=O(1)$ and the code sets $C=1$. The derived BCC coefficient (F300) is $\langle A\rangle=1/315$, so the code's $(ak)^2$ overstates the term by roughly $300\times$ (it is still an upper-bound scale). The module imports numpy directly (D8).

### `engine/interactions/stellar.py` — hydrostatic stars: TOV vs the dielectric model
**Status:** partial · test-only · **Findings:** — (docstring: F173, F174, F175; ledger: canonical interior solver with `theory='gr'` under F178) · **Lattice:** n/a · **Law:** n/a · **Units:** geometric ($G=c=1$), km; $1\,M_\odot=1.476625$ km

**Does:** Integrates stellar structure under GR (TOV) and under the literal F106 energy-only dielectric law (plus a covariant F175 variant), and returns mass–radius and redshift curves.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $p=K\rho^\Gamma$; two-piece version with pressure continuity $K_2=K_1\rho_b^{\Gamma_1-\Gamma_2}$ | EoS | `stellar.py:L50–53 Polytrope`, `…:L215–226 TwoPiecePolytrope` | unknown |
| 2 | $m'=4\pi r^2\rho$, $p'=-(\rho+p)(m+4\pi r^3p)/[r(r-2m)]$ | TOV (canonical under F178) | `…:L61–63 _tov_rhs()` | unknown |
| 3 | $m_E'=4\pi r^2\rho$, $p'=-(\rho+p)\,m_E/r^2$ | literal F106 energy-only model | `…:L68–70 _model_rhs()` | unknown |
| 4 | RK4 in $r$ ($h=10^{-3}$) with linear surface refinement at $p\to0$; $z=(1-2M/R)^{-1/2}-1$ (GR) or $z=e^{M/R}-1$ (model) | star integration and surface redshift | `…:L83–102 integrate_star()` | unknown |
| 5 | $u'=s/r^2$, $s'=-\tfrac12\big[s^2/r^2+8\pi\,\text{src}\,e^{2u}r^2\big]$, $p'=(\rho+p)u'$, with src $\in\{\rho,\ \rho+3p\}$ | covariant dielectric variant (F175) | `…:L142–146 _cov_deriv()` | unknown |
| 6 | $u''(0)=-\tfrac{4\pi}{3}\rho_ce^{2u_c}$ | central regularity | `…:L153 _cov_to_surface()` | unknown |
| 7 | $u_\infty=u_R+2\ln(1+s_R/2R)$, $M_E=-1/(1/s_R+1/2R)$ | closed-form vacuum tail ($s'=-s^2/2r^2$) | `…:L174–175 _cov_uinf_M()` | unknown |
| 8 | secant shoot on $u_c$ such that $u(\infty)=0$; $z=e^{u_R}-1$ | BVP solve | `…:L182–195 solve_covariant()` | unknown |

**Depends on:** numpy only. Gravity sector per 07b.
**Flags:** Rows 3 and 5–8 (the energy-only model) are **SUPERSEDED by F178** (F106 reclassified to a weak-field reduction; the F173/F174 departures are "artifacts"). They survive as the falsification record, and only `theory='gr'` is canonical. The registry status is `partial` with no findings. The row-7 sign convention matters: $s<0$ outside, so $M_E>0$. `MSUN_KM` is an unregistered literal.

### `engine/interactions/superconductivity.py` — electrical superconductivity (F210–F218, F242, F374, F375)
**Status:** live · test-only · **Findings:** — (docstring and inventory: F210 F211 F212/F213 F215 F216 F218b F242 F374 F375) · **Lattice:** n/a (dimensionless or SI; "emergent lattice") · **Law:** even (Proca photon, F69) · **Units:** dimensionless and $k_B=1$ in K; SI through literal CODATA values

**Does:** Assembles BCS/Eliashberg superconductivity as the electric S-dual of F86: phonon glue, gap equation, Meissner/London, flux quantum, Josephson, $T_c$ estimators, jellium λ and μ*, and the imaginary-axis Eliashberg solve with Padé continuation.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $V_\text{eff}=V_c+g^2\,2\omega_q/(\omega^2-\omega_q^2)$ | retarded Fröhlich kernel (attractive for $\lvert\omega\rvert<\omega_q$) | `superconductivity.py:L80 frohlich_kernel()` | exact (inv gen-T1 SC1a) |
| 2 | $\omega_D=c_s\pi/a_\text{mat}$; $V=D^2/(\rho c_s^2)$ (small-$q$ contact limit) | cutoff and contact attraction | `…:L98 debye_from_elastic()`, `…:L115 small_q_contact_limit()` | exact (inv gen-T1 SC1b, SC1c) |
| 3 | $\Delta(0)=\omega_D/\sinh(1/N_0V)$ | T=0 gap, closed form | `…:L164 gap_T0()` | machine (inv gen-T2 SC2d) |
| 4 | $1/N_0V=\int_0^X\tanh u/u\,du$, $X=\omega_D/2kT_c$; for $X>40$: $X^*=40\,e^{1/N_0V-C_0}$ | $T_c$ (log-tail split) | `…:L194–199 Tc()` | machine (inv gen-T2 SC2a) |
| 5 | $1=N_0V\!\int_0^{\omega_D}\tanh(E/2kT)/E\,d\xi$, $E=\sqrt{\xi^2+\Delta^2}$, arcsinh tail beyond $\xi_c=80kT$; bisection | finite-T gap | `…:L216–230 gap_at_T()` | quantitative (inv gen-T3 SC2c) |
| 6 | $2\Delta/kT_c\to2\pi/e^{\gamma_E}$; $\Delta C/C_n=12/[7\zeta(3)]$; $\xi_0=v_F/(\pi\Delta_0)$ | BCS universals | `…:L240`, `…:L251`, `…:L257` | machine (inv gen-T2 SC2a, SC2b) |
| 7 | $\lambda_L=\sqrt{m^*/(\mu_0n_s(2e)^2)}$; $\omega^2=m_\gamma^2+(c_\text{lat}k)^2$ with $c_\text{lat}=1/\sqrt3$ (F26) | London depth and Proca even-law photon | `…:L300 london_depth()`, `…:L308 massive_photon_omega()` | exact (inv gen-T1 SC4a, SC4c) |
| 8 | $B=B_0e^{-x/\lambda_L}$; FD solve of $(\partial_x^2-\lambda_L^{-2})B=0$ (Thomas algorithm) | Meissner profile (analytic vs numeric) | `…:L315`, `…:L326–349 meissner_slab_solve()` | quantitative (inv gen-T3 SC4b) |
| 9 | $\Phi=nh/2e$; $\kappa=\lambda_L/\xi_0$; $I=I_c\sin\Delta\theta$; $\dot{\Delta\theta}=2eV/\hbar$; $J=J_0+(n_s(2e)^2/m)Et$; Drude $J_0e^{-t/\tau}$ | flux quantum, GL, Josephson, persistent current | `…:L363`, `L369`, `L374`, `L379`, `L402`, `L410` | exact (inv gen-T1 SC3a, SC5a, SC5b, SC6); Josephson machine (inv gen-T2 SC5c) |
| 10 | $T_c^\text{BCS}=1.134\,\omega_\text{log}e^{-1/(\lambda-\mu^*)}$; McMillan $T_c=(\theta_D/1.45)\exp[-1.04(1+\lambda)/(\lambda-\mu^*(1+0.62\lambda))]$; Allen–Dynes $T_c=(f_1f_2\omega_\text{log}/1.20)\exp[\cdots]$ with $f_1=[1+(\lambda/\Lambda_1)^{3/2}]^{1/3}$, $\Lambda_1=2.46(1+3.8\mu^*)$ | $T_c$ estimators (F211) | `…:L434`, `…:L439–443`, `…:L454–466` | unknown (empirical formulas; F211 fit SUPERSEDED by F215) |
| 11 | $E_F=\tfrac{\hbar^2}{2m}(3\pi^2n)^{2/3}$; $D=\tfrac23E_F$; $N_0=3n/4E_F$; $\lambda=N_0D^2/(\rho c_s^2)$; $c_s=v_F\sqrt{Zm_e/3M}$ | jellium electron-phonon λ (F212/F213) | `…:L524–526`, `L539`, `L544`, `L559–564`, `L572–574` | exact (inv gen-T1 HOP2, HOP3; inv #241, F213); $E_F$ quantitative (inv gen-T3 HOP1) |
| 12 | $r_s=(3/4\pi n)^{1/3}/a_0$; $\mu=0.082930\,r_s\ln(1+6.0299/r_s)$; $\mu^*=\mu/(1+\mu\ln(E_F/\omega_c))$ | Coulomb μ, Morel–Anderson μ* (F242) | `…:L621–622`, `…:L636–637 mu_coulomb_jellium()`, `…:L656–657` | exact closed form $\mu(r_s)$ + quantitative $\mu^*$ (inv #271, F242) |
| 13 | $\omega_c=6\,k_B\,s/e$ with $s=\omega_\text{log}$ (Einstein) or $\sqrt e\,\omega_\text{log}$ (Debye) | solver-consistent cutoff (F374) | `…:L671–672 eliashberg_matsubara_cutoff_eV()` | unknown |
| 14 | $\mu(r_s,\alpha)=\alpha\cdot0.082930\,r_s\ln(1+6.0299/(r_s\alpha))$ | real-DOS generalisation (F375, Nb $\alpha=3.0839$) | `…:L723–724 mu_coulomb_real_dos()` | unknown |
| 15 | $2\Delta/kT_c=3.528[1+12.5(T_c/\omega_\text{log})^2\ln(\omega_\text{log}/2T_c)]$; $Z=1+\lambda$ | strong-coupling gap-ratio formula | `…:L765–769`, `…:L753` | machine (inv gen-T2 MR1); ratio vs measured quantitative (inv gen-T3 MR2) |
| 16 | $\alpha^2F=\lambda\omega^2/\omega_\max^2$ on $(0,\omega_\max)$; $\omega_\max=\sqrt e\,\omega_\text{log}$; $\lambda(\nu)=\lambda[1-(\nu^2/\omega_\max^2)\ln(1+\omega_\max^2/\nu^2)]$; Einstein $\lambda(\nu)=\lambda\omega_E^2/(\omega_E^2+\nu^2)$ | model-derived spectral function (F216/F218b) | `…:L845`, `L852`, `L866–869`, `L824` | exact (inv gen-T1 AF2; inv #249, F216); $\lambda(\nu)$ quantitative (inv gen-T3 AF3) |
| 17 | $\omega_n=\pi T(2n+1)$; $Z_n=1+\tfrac{\pi T}{\omega_n}\sum_m\lambda_{n-m}\omega_m/\sqrt{\omega_m^2+\Delta_m^2}$; $Z_n\Delta_n=\pi T\sum_m(\lambda_{n-m}-\mu^*\theta_c)\Delta_m/\sqrt{\omega_m^2+\Delta_m^2}$ | imaginary-axis Eliashberg (damped fixed point) | `…:L816`, `…:L907–917 eliashberg_solve()` | quantitative (inv gen-T3 EL1) |
| 18 | $\rho(T)=$ largest eigenvalue of $M_{nm}=\pi T(\lambda_{n-m}-\mu^*\theta_c)/(Z_n\lvert\omega_m\rvert)$ with linearised $Z_n$; $T_c$ at $\rho=1$ (bisection) | dynamic $T_c$ (no fit) | `…:L933–949`, `…:L959–976 eliashberg_tc()` | quantitative (inv gen-T3 EL4, EL5) |
| 19 | Vidberg–Serene continued-fraction Padé (mpmath, 60 dps); gap edge at $\omega=\mathrm{Re}\,\Delta(\omega)$; ratio $2\Delta_0/T_c$ | real-axis continuation (F218b) | `…:L1004–1022 _pade_continue_mp()`, `…:L1047–1058 gap_edge_real_axis()` | quantitative (inv gen-T3 PA1–PA3) |

**Depends on:** `c_lat` (registry, F26); everything else is local.
**Flags:** ⚠ **DOC/CODE MISMATCH**, `mu_coulomb_jellium` L633–637. The docstring derives $(2k_F/k_{TF})^2=\pi k_Fa_0=\pi(9\pi/4)^{1/3}/r_s=6.02921/r_s$, but the code hard-codes 6.0299 (a $1.1\times10^{-4}$ relative literal error, repeated at L723). The prefactor 0.082930 agrees with $1/[2\pi(9\pi/4)^{1/3}]=0.0829296$. `_C_RS` (L615) is defined and never used. SI constants ($h$, $e$, $k_B$, $m_e$, $a_0$, amu) are module literals rather than D7 registry symbols. The registry has no findings for this module, although nine findings cite it. Material tables are literature inputs (external).

### `engine/interactions/thermodynamics.py` — lattice-native thermodynamics, photon sector (F300, rubric G10)
**Status:** live · standalone · **Findings:** F300 · **Lattice:** BCC (paired-photon dispersion; the single-branch BCC walk for §B/C) · **Law:** even (§A: `pair_dispersion` $=\omega^+(k/2)+\omega^-(k/2)$); single chiral branch `sign="+"` for the §B/C walk · **Units:** lattice ($\Theta=k_BT\tau/\hbar$); SI through the tick

**Does:** Builds the photon-gas equation of state from the derived pair dispersion, with closed-form lattice corrections. It also shows fine-grained entropy conservation and coarse-grained entropy growth to a GGE under the free walk, and states the F190 cell-count no-go.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_\text{pair}=c_\text{lat}\lvert k\rvert[1-A(\hat n)\lvert k\rvert^2]+O(k^5)$, $A=\tfrac1{72}\sum_{i<j}n_i^2n_j^2+\tfrac1{24}(n_xn_yn_z)^2$, $c_\text{lat}=1/\sqrt3$ (F26) | closed-form low-$k$ expansion | `thermodynamics.py:L120–122 A_anisotropy()`; checked `…:L145–151 dispersion_expansion()` | exact (inv T1 #219) |
| 2 | $A\equiv0$ along $\langle100\rangle$ (dispersion exactly linear there) | axis exactness | `…:L149–151` | exact (inv T1 #220: identity, 6e-14) |
| 3 | $\langle A\rangle_{S^2}=1/360+1/2520=1/315$ | sphere average | `…:L125`; quadrature `…:L157–167 mean_anisotropy()` | exact (inv T1 #219) |
| 4 | $u=\tfrac{g}{(2\pi)^3}\!\int\!d^3k\,\Omega\,n_B$, $p=\tfrac{g}{3(2\pi)^3}\!\int\!d^3k\,(k\cdot\nabla_k\Omega)\,n_B$ (4th-order radial FD), $s=(u+p)/\Theta$, $n_B=1/(e^{\Omega/\Theta}-1)$, $g=2$; $u_{SB}=g\pi^2\Theta^4/(30c^3)$ | BZ quadrature EoS (momentum-flux pressure) | `…:L221–247 photon_eos()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |
| 5 | $u/u_{SB}-1=\tfrac{40\pi^2}{441}\Theta^2$, $\tfrac13-p/u=\tfrac{16\pi^2}{1323}\Theta^2$, $s/s_{SB}-1=\tfrac{4\pi^2}{49}\Theta^2$, $C_u/C_w=15/2$ (from $\tfrac{200\pi^2}{21}\langle A\rangle/c^2$ and $\tfrac{80\pi^2}{63}\langle A\rangle/c^2$) | closed-form lattice corrections | `…:L191–193`; measured `…:L250–273 eos_coefficients()` | exact (reg) |
| 6 | $a=(a/\ell_P)\,\ell_P$ with $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107); $\tau=a/(\sqrt3\,c)$; $T_\text{lat}=\hbar/(k_B\tau)\approx3.72\times10^{31}$ K | the one temperature scale | `…:L294–297 lattice_scales()` | exact (reg) |
| 7 | margins $\delta u/u=C_u\Theta^2$, softening $3C_w\Theta^2$ at CMB/BBN/QCD/EW temperatures; $\Theta_{1\%}=\sqrt{0.01/(3C_w)}$ | cosmology margins | `…:L316–323 cosmology_margins()` | quantitative (inv §F300 §3.1) |
| 8 | Gaussian-state evolution: $G(t)=U^tG_0U^{t\dagger}$, per-$k$ $2\times2$ `bcc_unitary(sign="+")` diagonalised, $U^t=V\,\mathrm{diag}(\lambda^t)V^{-1}$; $S=-\sum[e\ln e+(1-e)\ln(1-e)]$ over eigenvalues of the correlation matrix | exact free-fermion entropy machinery | `…:L338–355 _walk_setup()`, `…:L359–363 _prop()`, `…:L367–368 _vn()` | machine (inv §F300 G10-7, G10-8) |
| 9 | GGE $=$ dephased $G$ in the branch eigenbasis; plateau/GGE vs subsystem fraction; $S_A(-t)$ vs $S_A(+t)$ | §B3/B4 coarse-graining and time reversal | `…:L419–457 entropy_ledger()` | quantitative (inv §F300 G10-9…G10-11) |
| 10 | $s_\text{cell}=2\pi\sqrt3$; $W=e^{s}$ and $s/\ln2$ are not integers; capacity $96\ln2$ (48 Weyl × 2) | F190 no-go and capacity bound | `…:L492–511 cell_capacity()` | exact (registry); capacity quantitative (inv §F300 G10-13) |

**Depends on:** `gauge.photon.pair_dispersion` (05c), `lattice.bcc.bcc_unitary` (03); constants `c_lat`, `ell_P_m`, `c_SI`, `hbar_SI`, `a_over_ellP`, `J_per_GeV` (01).
**Flags:** `K_B_SI` is an unregistered literal (declared in the docstring). §B/C evolve a single chiral branch with `np.linalg.eig`/`inv` on complex 2×2 blocks, which is complex arithmetic throughout, so no real/imag loss. Numpy is imported directly next to the `xp` alias (D8 ratchet). The quadrature legs (rows 4, 5, 9) are quantitative with tolerances, while the registry says `exact`; the exactness belongs to the closed forms.

### `engine/interactions/thermodynamics_gstar.py` — $g_*(T)$ from the model's own content (F309)
**Status:** live · standalone · **Findings:** F309 · **Lattice:** BCC single-branch walk `bcc_dispersion(sign=±)` · **Law:** chiral (the two branches summed with equal weight, "branch-balanced") · **Units:** lattice $\Theta$ for §A/B; MeV for §C–E

**Does:** Expands the single-branch BCC Weyl dispersion and derives the fermionic EoS corrections, including the branch-odd term. It lists the relativistic species with inclusion and exclusion reasons, computes $g_*$ and $g_{*s}$ in the BBN window, and reruns BBN with the model electron mass.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\omega^\pm=c\lvert k\rvert[1\mp b\lvert k\rvert-a\lvert k\rvert^2]+O(k^4)$, $b=n_xn_yn_z/\sqrt3$, $a=4A$ | single-branch expansion | `thermodynamics_gstar.py:L146 b_branch_odd()`, `…:L151 a_branch_even()`; checked `…:L183–190` | exact (reg) |
| 2 | $\langle a\rangle=4/315$, $\langle b^2\rangle=1/315$ | sphere means | `…:L154`, `…:L158`; quadrature `…:L195–214` | exact (reg) |
| 3 | $u=\sum_\pm\tfrac1{(2\pi)^3}\!\int\!\omega\,n_F$, $p$ by momentum flux, $n_F=1/(e^{\omega/\Theta}+1)$; $u_{SB}=2\cdot\tfrac78\pi^2\Theta^4/(30c^3)$ | fermionic BZ quadrature (branch-odd control = average both branches) | `…:L297–321 fermion_eos()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |
| 4 | $C_u^F=\tfrac{310\pi^2}{441}=3\pi^2\tfrac{1550}{147}(\langle a\rangle+3\langle b^2\rangle)$, $C_w^F=\tfrac{124\pi^2}{1323}$, $C_s^F=\tfrac{31\pi^2}{49}$; branch-odd share $3/7$; $C^F/C^\gamma=31/4=7\times31/28$; $C_u/C_w=15/2$ | closed-form fermionic corrections | `…:L243–253`; ratios `…:L360–374 fermion_photon_ratios()` | exact (reg) |
| 5 | 3 gens × (8 L + 8 R) = 48 Weyl, imbalance 0, 2 dof per Weyl | content | `…:L423–435 weyl_content()` | exact (reg) |
| 6 | $\rho/T^4=\tfrac1{2\pi^2}\!\int u^2\sqrt{u^2+x^2}f$, $p/T^4=\tfrac1{6\pi^2}\!\int u^4/\sqrt{u^2+x^2}f$ (Gauss–Legendre, $u\le80$) | one-dof massive gas | `…:L522–528 _rho_p_hat()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |
| 7 | $g_*=\tfrac{30}{\pi^2}\sum g_i r_i^4\hat\rho_i$, $g_{*s}=\tfrac{45}{2\pi^2}\sum g_ir_i^3(\hat\rho_i+\hat p_i)$, $r_i=T_i/T_\gamma$ | $g_*(T)$, $g_{*s}(T)$ | `…:L550–562 g_star()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |
| 8 | targets $g_*=10.75$ (early); $g_{*s}\to2+\tfrac{21}{4}\tfrac4{11}$, $g_*\to2+\tfrac{21}{4}(\tfrac4{11})^{4/3}$ with $T_\nu/T_\gamma$ from `cosmology_bbn.thermal_history` | BBN-window checks | `…:L590–594 bbn_window()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |
| 9 | $\delta g_*$ for $\mu^\pm$, $\nu_R$; $m_{E_g}$ bound where $\delta g_*<10^{-3}$ at 10 MeV (bisection) | pricing the excluded species | `…:L604–631 excluded_species_prices()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |
| 10 | $\delta g_*/g_*=(2C_u^\gamma+8.75C_u^F)\Theta^2/10.75$ | lattice correction at BBN | `…:L643–647 lattice_correction_at_bbn()` | exact (reg) |
| 11 | plateau table: 3.363 … 105.75 / 107.75 vs SM 106.75 | high-T $g_*$ | `…:L672–693 plateau_table()` | exact (reg) |
| 12 | $Y_p$, D/H from `cosmology_bbn.run_bbn` with $m_e=0.51069$ vs PDG 0.51099895 | BBN shift | `…:L723–745 bbn_shift()` | quantitative (registry exact; quadrature/solver output → quantitative per brief) (reg: exact; row is weaker — see flags) |

**Depends on:** `lattice.bcc.bcc_dispersion` (03), `thermodynamics` (above), `cosmology_bbn` (07a).
**Flags:** `MODEL_M_E_MEV=0.51069`, `MODEL_M_MU_MEV` and `MODEL_M_TAU_MEV` (F121) are module literals, not D7 constants. The docstring states D7 applies. Row 11 is asserted data, and GS-12 checks the table against itself. Registry exactness is `exact`, but rows 3, 7–9 and 12 are tolerance/quadrature results (quantitative).

### `engine/interactions/thermodynamics_interacting.py` — GGE → ETH onset in an interacting chain (F376)
**Status:** live · standalone · **Findings:** F376 · **Lattice:** **1-D open chain** (toy; not BCC) · **Law:** n/a · **Units:** dimensionless ($t=1$)

**Does:** Exact diagonalisation of the spinless t–V1–V2 chain at half filling in three regimes (free, integrable V1, generic V1+V2). It reads off level statistics, the entanglement plateau and the ETH fluctuation.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $H=-t\sum_i(c_i^\dagger c_{i+1}+\text{h.c.})+V_1\sum n_in_{i+1}+V_2\sum n_in_{i+2}+\epsilon\sum(i-c)n_i$, Jordan–Wigner signs by parity-below | many-body Hamiltonian (OBC, fixed $N$) | `thermodynamics_interacting.py:L175–201 build_H()` | quantitative (reg) |
| 2 | reflection-parity basis $(\lvert b\rangle\pm\lvert\bar b\rangle)/\sqrt2$, grouped even then odd | symmetry resolution | `…:L219–238 build_parity_transform()` | quantitative (reg) |
| 3 | $r_n=\min(\delta_n,\delta_{n+1})/\max(\delta_n,\delta_{n+1})$, $\langle r\rangle$ vs Poisson 0.3863 and GOE 0.5307 | level-spacing ratio | `…:L242–249 gap_ratio()` | quantitative (reg) |
| 4 | $S_A=-\sum p\ln p$, $p=$ squared singular values of $\psi$ reshaped $2^{L_A}\times2^{L-L_A}$ | entanglement entropy | `…:L258–266 half_chain_entropy_from_state()` | quantitative (reg) |
| 5 | $\psi(t)=V e^{-iEt}V^\dagger\psi_0$ (domain-wall quench); plateau/$(L_A\ln2)$; eigenstate $\mathrm{std}(S_A)$ in an energy window | D2/D3 diagnostics | `…:L286–312 run_regime()` | quantitative (reg) |

**Depends on:** numpy only (imported directly next to `xp`).
**Flags:** ⚠ **DOC/CODE MISMATCH (naming):** the entry point is `check_f375()` (L350; docstring L124), but the registry finding, `build_H` docstring and output artifact are **F376**. F375 is the Nb real-DOS finding in `superconductivity.py`. The module docstring calls the chain "the model's own single-band OBC hopping chain (the L^3 BCC walk collapsed…)", but it is a generic toy t–V chain. The docstring admits $V_1$, $V_2$ and $t$ are not derived (SCOPE §2).

### `engine/interactions/tolman.py` — pressure/Tolman discriminator (F173)
**Status:** live · test-only · **Findings:** — (docstring: FC08, F64, F106; finding F173) · **Lattice:** n/a · **Law:** n/a · **Units:** geometric ($8\pi\rho$ etc.); $s=GM/Rc^2$

**Does:** Computes the exact Einstein tensor of the isotropic exponential-dielectric metric symbolically. It then quantifies the uniform-sphere central time-dilation difference between the energy-only model and GR.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g=\mathrm{diag}(-1/K,\,K,\,Kr^2,\,Kr^2\sin^2\theta)$, $K=e^{2u(r)}$; Christoffels → Ricci → $G^\mu{}_\nu$; $8\pi\rho=-G^t{}_t$, $8\pi p_r=G^r{}_r$, $8\pi p_t=G^\theta{}_\theta$ (docstring: $-e^{-2u}(u'^2+2u''+\tfrac4ru')$, $-e^{-2u}u'^2$, $+e^{-2u}u'^2$) | exact effective source (sympy) | `tolman.py:L50–79 effective_source_symbolic()` | exact (inv T1 #217, F181 reproduces the F173 anisotropic stress) |
| 2 | remainder $=8\pi\rho_\text{eff}+\nabla^2_\text{flat}\ln K$, which is second order | the F106 law as the leading term | `…:L87–90 leading_density_residual()` | unknown (sympy in code) |
| 3 | omitted fraction $=3w/(1+3w)$ for $p=w\rho$ | pressure source omitted | `…:L101 source_fraction_omitted()` | unknown |
| 4 | model $g_{tt}(0)=-e^{-3s}$; GR $g_{tt}(0)=-\big[\tfrac32\sqrt{1-2s}-\tfrac12\big]^2$; fractional difference of $\sqrt{-g_{tt}}$ | uniform-sphere central redshift | `…:L107`, `…:L113`, `…:L118–120` | unknown (mpmath closed forms in code) |
| 5 | $g_{tt}^\text{model}-g_{tt}^\text{GR}=-\tfrac{15}{4}s^2+O(s^3)$ | leading divergence (spot-checked: sympy returns $-15s^2/4$) | `…:L126–128 leading_coefficient()` | unknown (sympy in code; spot-checked $-15s^2/4$) |

**Depends on:** sympy, mpmath.
**Flags:** Rows 3–5, read as a model-vs-GR discriminator, are **SUPERSEDED by F178** (S-record F178: F173 partially superseded, P3/P4 dead). The departure is an artifact of the demoted energy-only law. Rows 1–2, the tensor algebra, stay live and motivated F178. The module docstring still says "the model uses rho only", which is stale relative to F178 (docstring vs ledger, not a code error). L52 builds `g` once and L54 overwrites it (dead line).

### `engine/interactions/unified.py` — Higgs Φ ⊗ Dirac unified stepper (F1–F4 era, "ca_unified")
**Status:** live · test-only · **Findings:** — (docstring: F3/F4, Finding 9; inventory row 14, F134 row 75) · **Lattice:** **2-D square** (D1 reference; `dirac_step_2d_*`) · **Law:** n/a (split-step exact-QCA Dirac, $n=\sqrt{1-m^2}$) · **Units:** lattice

**Does:** Strang-composes a Klein–Gordon/Mexican-hat Φ half-step, a variable complex-mass Dirac step with $M=y\Phi$, and optional symplectic Yukawa kicks on Π.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $v=\sqrt{\mu^2/2\lambda}$ for $V=-\mu^2\lvert\Phi\rvert^2+\lambda\lvert\Phi\rvert^4$ | vacuum | `unified.py:L64 setup_vacuum()` | unknown |
| 2 | $\Phi$-free($dt/2$) → [kick] → Dirac($dt$) → [kick] → $\Phi$-free($dt/2$); the sign of the potential is set by `phase` | Strang composition | `…:L180–219 unified_step()` | unknown |
| 3 | $\Pi\mathrel{-}=\tfrac{dt}{2}\,y\,\chi^\dagger\eta$, $\chi^\dagger\eta=\bar\chi_u\eta_u+\bar\chi_d\eta_d$ (from $H_Y=y(\Phi\eta^\dagger\chi+\Phi^*\chi^\dagger\eta)$, $\dot\Pi=-\partial H_Y/\partial\Phi^*$) | symplectic Yukawa back-reaction | `…:L191–193`, `…:L212–214` | unknown; inv T3 #14 grades the F3 drift qualitative ($O(dt^2)$, 3 ppm) |
| 4 | $m_R=y\,\mathrm{Re}\,\Phi$, $m_I=y\,\mathrm{Im}\,\Phi$ fed to `dirac_step_2d_varm_complex_splitstep` | complex Yukawa mass | `…:L199–207` | unknown |
| 5 | $H_{KG}=\sum\lvert\Pi\rvert^2+N^{-1}\sum_kk^2\lvert\tilde\Phi_k\rvert^2+\sum(-\mu^2\lvert\Phi\rvert^2+\lambda\lvert\Phi\rvert^4)$ | Φ energy | `…:L249–261 phi_energy()` | unknown |
| 6 | $H=H_{KG}+N^{-1}\sum_k\Psi_k^\dagger(n_0\,\alpha\cdot k)\Psi_k+2y\,\mathrm{Re}\sum\Phi\,\eta^\dagger\chi$, $n_0=\sqrt{1-m_0^2}$, $m_0=y\,\overline{\mathrm{Re}\Phi}$ | joint energy (continuum small-$k$ kinetic form) | `…:L288–319 total_energy()` | unknown |

**Depends on:** `particles.higgs` (`kg_step_strang`, `_laplacian_2d`), `particles.dirac` (06b).
**Flags:** A Higgs-field stepper sits in tension with **Core Design Decision 3** (hypercharge on U(x), "avoiding any need for the Higgs field"). No supersession record covers this module, so it is flagged OTHER and not called superseded. `phi_energy` always uses $-\mu^2$ even when the step runs `phase='symmetric'` ($+\mu^2$), so the energy is wrong in the symmetric phase. `grad_Phi` (L250) is computed and never used. The kinetic energy uses continuum $k^2$ and $\alpha\cdot k$, while the Dirac step is exact-QCA (the docstring acknowledges this approximation).

### `engine/interactions/vacuum_energy.py` — cosmological-constant sign under the full-tensor source (F192)
**Status:** live · test-only · **Findings:** — (docstring: F192, F164, F178) · **Lattice:** BCC (through the F164 fork's zero-point integral) · **Law:** n/a · **Units:** SI (J/m³)

**Does:** States that vacuum $w=-1$ accelerates under the full-tensor source, and tabulates the bare BCC zero-point overshoot against the observed $\rho_\Lambda$ (about $10^{120}$). Candidate cancellations are listed as underived.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $w=-1$: $(\rho+3p)/\rho=1+3w=-2$; acceleration sign $-(1+3w)=+2>0$ | full-tensor sign | `vacuum_energy.py:L36–43 vacuum_equation_of_state()` | exact (inv #220, F184–F192: F192 $w=-1$ sign) |
| 2 | $I_{cc}$ = `f164.zero_point_integral(n=160)`; $\rho_\text{vac}$ = `f164.vacuum_energy_density(I_cc, g_star=2)`; ratio $=\rho_\text{vac}/6.0\times10^{-10}$ J m⁻³ | bare overshoot | `…:L48–53 bare_overshoot()` | unknown |
| 3 | cancellation ledger (all `derived: False`) | open-status table | `…:L61–75 cancellation_ledger()` | n/a (plumbing) |

**Depends on:** `forks.gravity.gr_fork_F164_cosmological_constant` (08a).
**Flags:** `RHO_LAMBDA_OBS=6.0e-10` is an unregistered literal. The overshoot uses $g_*=2$ (photon content). **S25 (F319/F408)** records that pairing $\rho_\text{vac}$ at $g_*=2$ with a $G$ induced at 48 Weyl fields is a content mismatch, and that the all-fermion zero-point sum is negative. The sign comment "the full-tensor source gets the SIGN right automatically" (L42–43) concerns the $w=-1$ source term only. The *sign of $\rho_\text{vac}$ itself* is open per F408. This module is not named in S25, so it is flagged OTHER.
