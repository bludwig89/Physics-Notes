# 07c — Interactions III: the QED sector (`qed_*`)

*Written 2026-09-28 - 00:00 (part p07c). Code is the source of truth; every row cites `file.py:L<n> function()` at the line where the quantity is computed. Exactness defaults to the module registry's `exactness` field (13 of the 15 modules are `None` → `unknown`), overridden only where `docs/status/exactness-inventory.md` names the specific result (rows #228–229, #275–332 of that file).*

**Scope.** The fifteen `qed_*.py` modules under `src/casim/engine/interactions/`: one-loop QED (vacuum polarisation F251, vertex / $a_e$ / Lamb F252, electron self-energy F258), the Bethe logarithm (F257), IR/Bloch–Nordsieck (F259), tree S-matrix (F260), two loops ($a_e$, $a_\mu$, F261; VP non-log F336), nonlinear QED (Euler–Heisenberg, Schwinger, F263), all-orders renormalisability (F264), the Casimir effect (F207/F209) and the UV-completion derivation (F319).

**Read this before quoting any number from this batch — what is lattice and what is not.** Almost everything here is **continuum QED re-derived symbolically or evaluated from textbook closed forms**, with α and lepton masses as **external literal inputs** (CODATA 2022). The lattice enters in only four places:
1. `qed_vacuum_polarization._fermion_B` and `qed_electron_self_energy._selfenergy_AB`: a subtracted *lattice-minus-continuum* coefficient in which only the **internal photon** propagator is replaced by the rule kernel $K=3\,\Omega_\text{even}^2+k_t^2$ (the electron line stays continuum $k^2+m^2$), integrated on a **4-D hypercubic** midpoint grid over $[-\pi,\pi)^4$. The absolute BZ measure for this kernel is open (F272 §4; supersession S12).
2. `qed_casimir.pair_bending_coeff`, `casimir_energy_3d_naive(disp='pair')`, `disp_1d(kind='axis')`: mode sums on the F69 pair dispersion.
3. `qed_twoloop_vacuum_polarization_nonlog` / `qed_uv_completion`: see their blocks.
4. $c_\text{lat}=1/\sqrt3$ (F26, exact) is imported by several modules but multiplies out of every dimensionless QED result.

**Shared conventions.**
- *Metric / gammas.* $(+,-,-,-)$, Dirac representation $\gamma^0=\mathrm{diag}(I,-I)$, $\gamma^i=[[0,\sigma^i],[-\sigma^i,0]]$, $\slashed v=\sum_a\eta_{aa}v^a\gamma^a$; $\alpha=e^2/4\pi$ (Heaviside–Lorentz, $\hbar=c=1$). The same `_dirac_gammas` block is duplicated in five modules. Symbolic gates are sympy; numeric Dirac traces (`qed_scattering`) are complex128 numpy.
- *Lattice / law.* Where a propagator is lattice at all it is the **even** pair law (F69/F91) $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$ from `lattice.bcc.bcc_dispersion` (see 03-lattice.md § bcc.py, 05c-gauge-photon-lpt-weak.md § photon.py). No module uses the σ-bilinear photon; no chiral 2×2 unitary passes through numpy eig/FFT here (the one FFT, `qed_casimir.modulated_weight_signals`, is a real `rfft` of a real signal).
- *Units.* Natural units $m=1$ for shapes; MeV / barn / MHz via literal $\hbar c$, $h$; `qed_casimir*` and `qed_schwinger_pair.critical_field` in SI.
- *Constants.* Registry symbols used: `c_lat` $=1/\sqrt3$ (F26, exact), `a_over_ellP` $=\sqrt{8\pi}\,3^{1/4}$ (F79/F107, exact), `ell_P_m`, `c_SI`, `hbar_SI`, `G_CODATA`, `m_e_GeV` (external). **α is not in the registry**: every module types $\alpha^{-1}=137.035999177$ (or 137.035999 in `qed_renormalization`). Other unregistered literals: $m_e,m_\mu,m_\tau$ (MeV), $\hbar c=197.3269804$ MeV fm / $1.97327\times10^{-16}$ GeV m, $h=4.135667696\times10^{-15}$ eV s, $e$, $k_B$, $m_e$ (kg), the F107 cell $a=1.06638\times10^{-34}$ m (twice), $g=9.81$ m/s², and literature comparison targets.
- *Supersession.* S12 (`docs/theory/supersessions.yaml`, 2026-08-02, by F277): the `mod 2π` refold in `qed_vacuum_polarization._fermion_B` and `qed_electron_self_energy._selfenergy_AB` was removed; the code mapped here is the post-fix code; F251/F258 are **partially superseded (numbers only)** — any F251/F258 lattice-Δ figure computed before 2026-08-02 is dead.

**Spot-checks run for this section** (PYTHONPATH=src, <5 s): `casimir_energy_3d_abelplana(30,pol=2)/casimir_energy_3d_closed(30,pol=2)` $=1+2\times10^{-16}$; `pair_dispersion(k,0,0)-k/\sqrt3` $\le3\times10^{-13}$ for $k\in[10^{-3},2]$ (exactly linear on axis); `pair_bending_coeff` axis $=-1.5\times10^{-4}$ (round-off, see flags), body-diagonal $-6.57\times10^{-3}$; `ae_schwinger_symbolic` integral $=1$; `lamb_shift()` $=1052.19$ MHz with Uehling $-27.13$ MHz and Dirac gap $0.0$; `leptonic_running()` $\Delta\alpha_\ell=0.031421$, $1/\alpha(M_Z)|_\ell=132.730$.

**Modules (path order):** amu · bethe_log · casimir · casimir_materials · electron_self_energy · euler_heisenberg · ir_bremsstrahlung · renormalization · scattering · schwinger_pair · twoloop_ae · twoloop_vacuum_polarization_nonlog · uv_completion · vacuum_polarization · vertex_loop.

---

### `engine/interactions/qed_amu.py` — muon anomaly $a_\mu$ at two loops (QED only) and lepton universality
**Status:** live · test-only · **Findings:** (registry none; docstring F261) · **Lattice:** n/a · **Law:** n/a · **Units:** dimensionless

**Does:** assembles $A_2(\mu)$ from `qed_twoloop_ae` pieces and compares with the known QED coefficient; hadronic/EW pieces explicitly out of scope.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A_1^{(e)}=A_1^{(\mu)}=\tfrac12$, $A_2^{(e)}=A_2^{(\mu)}=A_2^\text{mass-indep}$ (same Python object read once) | universality gate | `qed_amu.py:L71–73 universality_gate()` | exact (inventory #300: literal equality) |
| 2 | $A_2^{VP}(e\text{ in }\mu)$ = `tl.A2_vp_dispersive(m_e, m_mu)`; leading $\tfrac13\ln(m_\mu/m_e)-\tfrac{25}{36}$, $+\tfrac{\pi^2}4\,m_e/m_\mu$ | light loop in heavy vertex | `L95–97 vp_e_in_mu()` | quantitative (inventory #301, abs err $1.0\times10^{-8}$) |
| 3 | reverse $A_2^{VP}(\mu\text{ in }e)$ (decouples, $\sim5\times10^{-7}$) | asymmetry | `L98` | unknown (inferred: quantitative) |
| 4 | $A_2(\mu)=A_2^\text{mi}+A_2^{VP}(e)+A_2^{VP}(\tau)$ | muon two-loop coefficient | `L126 a_mu_two_loop()` | quantitative (inventory #302, vs 0.765857410) |
| 5 | $a_\mu^{(2)}=A_1(\alpha/\pi)+A_2(\mu)(\alpha/\pi)^2$ | $a_\mu^\text{QED}$ | `L128` | unknown (inferred: quantitative) |

**Inputs → outputs:** α, $m_e,m_\mu,m_\tau$ (literals re-exported from `qed_twoloop_ae`) → dict of coefficients. Comparison targets `A2_MU_KNOWN`, `A_MU_MEASURED` are literature literals, reference only. **Depends on:** `qed_twoloop_ae` (this file, below). **Flags:** row 1 is identity by construction (the same float is assigned to both leptons), not an independent check; α unregistered.

### `engine/interactions/qed_bethe_log.py` — hydrogen Bethe logarithm by Dalgarno–Lewis resolvent (F257)
**Status:** live · test-only · **Findings:** (registry none; docstring F257) · **Lattice:** 1-D uniform radial finite-difference grid (not the CA lattice) · **Law:** n/a · **Units:** atomic (Hartree), result converted to Rydberg by $+\ln2$

**Does:** computes $\ln k_0(n,l)$ for 1s/2s/2p from the resolvent of a finite-difference nonrelativistic Coulomb Hamiltonian.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $H_l$: diag $1/h^2+l(l+1)/2r^2-1/r$, off-diag $-1/(2h^2)$ | FD Schrödinger–Coulomb operator, $Z=1$ | `qed_bethe_log.py:L89 _Hdiag()`, `L94 _applyH()` | unknown (inferred: exact (definition)) |
| 2 | exact $u_{nl}(r)$: $2re^{-r}$; $(2\sqrt2)^{-1}(2-r)re^{-r/2}$; $(2\sqrt6)^{-1}r^2e^{-r/2}$; $E=-\tfrac12,-\tfrac18,-\tfrac18$ | source states | `L64–68 U_FUNCS` | unknown (inferred: exact) |
| 3 | $g_r=r\,u_n$; $M_p=\langle g_r\lvert(H_l-E_n)^p\rvert g_r\rangle$, $p=0..3$ | energy moments (length gauge, $M_3=\sum\lvert\langle p\rangle\rvert^2\Delta E$) | `L106–110 _dl_channel()` | unknown (inferred: machine) |
| 4 | $F(t)=\langle g_r\lvert(H_l-E_n+t)^{-1}\rvert g_r\rangle$ (batched Thomas tridiagonal solve) | resolvent | `L113–114` | unknown (inferred: machine) |
| 5 | integrand $M_3/(1+t)-M_2+tM_1-t^2M_0+t^3F(t)$, from $\ln e=\int_0^\infty[\tfrac1{1+t}-\tfrac1{e+t}]dt$ | Dalgarno–Lewis identity | `L115` | unknown (inferred: exact (identity)) |
| 6 | $t=u/(1-u)$, midpoint in $u$, Jacobian $(1-u)^{-2}$ | $t$-quadrature | `L123` | unknown (inferred: quantitative) |
| 7 | below-threshold / degenerate states projected out; explicit $D\mathrel{+}=a^2\epsilon^3$, $J\mathrel{+}=a^2\epsilon^3\ln\lvert2\epsilon\rvert$ ($\epsilon=E_d-E_n$, skipped if $\lvert\epsilon\rvert<10^{-9}$) | 2p: remove 1s (below) and 2s (degenerate) | `L136–144 bethe_log_raw()` | unknown (inferred: exact (algebra)) |
| 8 | $\ln k_0=\big[\sum_l(\int\!\text{integrand}+\ln2\,M_3)+J_\text{expl}\big]/D$ | assemble, Hartree→Rydberg | `L147–148` | unknown (inferred: quantitative) |
| 9 | $\ln k_0=2b_{2N}-b_N$ | O(h) Richardson | `L157 bethe_log()` | quantitative (inventory #277: ~2–3% vs 2.984/2.812/−0.030) |

**Inputs → outputs:** state name, $N$, $r_\text{max}$, $n_t$ → $\ln k_0$. `ACCEPTED` values are comparison-only. **Depends on:** numpy directly (not `casim.numerics`, D8). **Flags:** "from the model's own hydrogen spectrum" means a generic nonrelativistic FD Coulomb Hamiltonian, not the CA/Dirac walk or F125's Dirac–Coulomb solver (OTHER).

### `engine/interactions/qed_casimir.py` — Casimir effect from the F69 photon dispersion (F207, F209)
**Status:** live · test-only · **Findings:** (registry none; docstring F207 F209 F69 F107 F178 F193) · **Lattice:** BCC dispersion (`pair_dispersion`) on a cubic $k$-grid for the diagnostic sums; the headline C2 is continuum · **Law:** even (F69 pair law) · **Units:** lattice ($a=1$, $\hbar=1$) for C1–C4; SI for G1/F209

**Does:** mode-sum Casimir energies (1-D warm-up, 3-D closed form, naive BZ-cutoff sum), δ-mirror source channel, and bookkeeping for whether Casimir energy gravitates.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\omega=c\lvert k\rvert$; $2c\lvert\sin(k/2)\rvert$; axis $\Omega_\text{pair}(k\hat x)$ | 1-D dispersions ($c=c_\text{lat}=1/\sqrt3$, F26) | `qed_casimir.py:L64/L66/L68 disp_1d()` | unknown (inferred: exact) |
| 2 | $E_\text{sub}(L)=\tfrac12\sum_{n=1}^{\lfloor L/a\rfloor}\omega(n\pi/L)-\tfrac12\tfrac L\pi\int_0^{\pi/a}\omega\,dk$ | 1-D Dirichlet mode-sum minus bulk | `L79–82 casimir_energy_1d()` | unknown (inferred: quantitative) |
| 3 | lstsq fit $E_\text{sub}=e_0+C_1/L$, target $C_1=-\pi c/24$ | 1-D Casimir coefficient | `L90 fit_coeff_1d()` | quantitative (inventory #228: 3.5e-5) |
| 4 | $E/A=-\text{pol}\,\tfrac{cL}{6\pi^2}\int_0^\infty\tfrac{s^3}{e^{2Ls}-1}ds$ (trapezoid, $s\le25/L$) | Abel–Plana form for $\omega=c\lvert k\rvert$ | `L113 casimir_energy_3d_abelplana()` | unknown (inferred: quantitative (numeric integral of an exact form)) |
| 5 | $E/A=-\text{pol}\,\pi^2c/(1440L^3)$ (pol=2: $-\pi^2c/720L^3$) | closed form | `L119 casimir_energy_3d_closed()` | exact (inventory #228) |
| 6 | $F/A=-\text{pol}\,\pi^2c/(480L^4)$ (pol=2: $-\pi^2c/240L^4$) | force | `L125 casimir_force_3d_abelplana()` | unknown (inferred: exact) |
| 7 | $E/A=(2\pi)^{-2}\sum_{k_\perp}w\,\tfrac12[\sum_{n}\omega(k_\perp,n\pi/L)-\tfrac L\pi\int_0^{\pi}\omega\,dk_z]$, disp `cont` (analytic antiderivative) or `pair` | naive hard-BZ-cutoff sum | `L162–182 casimir_energy_3d_naive()` | unknown (inferred: quantitative) |
| 8 | fit $c_0+b_1/L+b_3/L^3+b_5/L^5$, EM $=2b_3$ | extract $1/L^3$ | `L190–192 fit_coeff_3d_naive()` | unknown (inferred: quantitative) |
| 9 | $\beta(\hat k)=\langle(\Omega_\text{pair}(k\hat k)/(ck)-1)/k^2\rangle_{k\in\{1,2,4\}\times10^{-3}}$ | $O(k^2)$ bending (lattice signature) | `L201 pair_bending_coeff()` | unknown (inferred: quantitative) |
| 10 | $E(L)=\tfrac c{2\pi}\int_0^\infty d\kappa\,\ln[1-(\tfrac\lambda{2\kappa+\lambda})^2e^{-2\kappa L}]$ | two δ-mirrors (Jaffe) | `L216 casimir_energy_delta_1d()` | unknown (inferred: quantitative) |
| 11 | $E_C=-\pi^2\hbar cA/(720L^3)$, $\Delta m=E_C/c^2$, weight $9.81\,\Delta m$ | SI gravitating shift | `L228–230 casimir_gravitating_mass()` | unknown (inferred: exact (algebra)) |
| 12 | $M_\text{grav}=E_C/c^2$ | Gauss closure of $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ (stated, not solved) | `L237 dielectric_enclosed_mass_gauss()` | unknown (inferred: exact (algebra)) |
| 13 | $H=g(a^\dagger b^\dagger+ab)$ on the $\lvert n,n\rangle$ ladder; Crank–Nicolson $\psi\to(I+iH\,dt/2)^{-1}(I-iH\,dt/2)\psi$; compare $\langle n\rangle$ to $\sinh^2gt$ | dynamical Casimir pair emission | `L258–281 two_mode_squeezing()` | unknown (inferred: machine (CN unitary; $O(dt^2)$ vs closed form)) |
| 14 | $E_C(\eta)=\eta^2E_C^\text{ideal}$ | reflectivity switch | `L303 casimir_energy_reflectivity()` | unknown (inferred: exact (posited form)) |
| 15 | $W_\text{beable}=gE_C(\eta)/c^2$; $W_\text{SEP}=gE_C(\eta)/c^2$ | two weight shifts | `L312 weight_beable()`, `L323 weight_sep_buoyancy()` | unknown (inferred: exact (identical arithmetic)) |
| 16 | $\eta(t)=\eta_0+\delta\eta\cos2\pi ft$; max time-domain and `rfft` differences | modulated degeneracy test | `L336–342 modulated_weight_signals()` | unknown (inferred: exact (0 by construction)) |
| 17 | offset differential $=x-x\equiv0$; beable differential $g\,\Delta E_C/c^2$ | tared weighing | `L354–357 homogeneous_offset_differential()` | unknown (inferred: exact (0 by construction)) |
| 18 | $E_\text{rad}=\hbar\Omega_d\sinh^2(gt)\,n_\text{modes}$, $\Delta m_\text{beable}=\Delta m_\text{SEP}=E_\text{rad}/c^2$ | DCE radiated mass | `L371–375 dce_radiated_gravitating_mass()`; `L386–388 dce_change_beable_vs_template()` | unknown (inferred: exact (0 by construction)) |

**Inputs → outputs:** $L$ (cells), polarisation count, coupling λ; SI area/separation → energies, forces, weights. **Depends on:** `gauge.photon.pair_dispersion` (05c § photon.py), `casim.numerics.fft`, `c_lat`, `c_SI`, `hbar_SI`, `G_CODATA` (01-constants.md). **Flags:** (a) the headline "EXACT" C2 (rows 4–6) never calls `pair_dispersion` — it is the continuum formula with $c=c_\text{lat}$, justified only by the IR-limit argument; the lattice appears only in rows 1, 7, 9. (b) Rows 15–18: the "independent formulas" for beable vs SEP weight are the same expression, so their zero residual is by construction (⚠ DOC/CODE MISMATCH with the "INDEPENDENT formulas" wording in the docstring and inventory #229). (c) `two_mode_squeezing` sets $n_b$ to the same list as $n_a$ (L276), so `max|n_a-n_b|` is 0 by construction. (d) `pair_bending_coeff` along the axis returns $-1.5\times10^{-4}$ instead of 0: the $k=10^{-3}$ sample is dominated by `arccos` round-off ($\sim3\times10^{-13}$ divided by $ck^3$). (e) $a=1.06638\times10^{-34}$ m is an unregistered literal (F107; the registry has `a_over_ellP`·`ell_P_m`).

### `engine/interactions/qed_casimir_materials.py` — Lifshitz finite-conductivity curve vs sphere–plate data (F207 companion)
**Status:** dead_candidate · unreferenced · **Findings:** F207 · **Lattice:** n/a (continuum Lifshitz) · **Law:** n/a · **Units:** SI

**Does:** maps the ideal Casimir law onto gold, plasma-model, optionally finite-T, and quotes the F207 lattice deviation.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $P_0=\pi^2\hbar c/(240a^4)$ | ideal plate pressure (magnitude) | `qed_casimir_materials.py:L42 pressure_ideal()` | unknown (registry none; closed form) |
| 2 | $F_\text{sp}=\pi^3\hbar cR/(360a^3)$ (PFA, $2\pi R\,E_{pp}$) | ideal sphere–plate force | `L47 sphere_plate_force_ideal()` | unknown |
| 3 | $\omega_p=9.0\,\text{eV}/\hbar$ | gold plasma frequency (literal) | `L35` | external |
| 4 | $\varepsilon=1+(W_p/\zeta)^2$, $s=\sqrt{W_p^2+x^2}/\zeta$, $p=x/\zeta$; $r_\text{TM}^2=((\varepsilon p-s)/(\varepsilon p+s))^2$, $r_\text{TE}^2=((p-s)/(p+s))^2$; $\int_\zeta x^2\sum_\nu(r_\nu^{-2}e^x-1)^{-1}dx$ | Lifshitz mode integral, plasma model | `L64–72 _lifshitz_pressure.mode_integral()` | unknown |
| 5 | $T=0$: $P=\tfrac{\hbar}{2\pi^2c^3}(\tfrac c{2a})^4\int d\zeta\,(\ldots)$ | zero-T pressure | `L80` | unknown |
| 6 | $T>0$: $P=\tfrac{k_BT}{\pi c^3}(\tfrac c{2a})^3\sum_n'(\ldots)$, $\xi_n=2\pi nk_BT/\hbar$ | Matsubara sum | `L82–90` | unknown |
| 7 | $\eta(a)=P/P_0$; $F_\text{real}=F_\text{sp}\,\eta$ | reduction factor | `L95`, `L100` | unknown |
| 8 | $\lvert\Delta F/F\rvert=\beta(a_\text{cell}/a)^2$, $\beta=6.6\times10^{-3}$ | model lattice deviation | `L107 lattice_fractional_deviation()` | unknown |

**Inputs → outputs:** separation $a$, radius $R$, $\omega_p$, $T$ → forces/pressures. **Depends on:** `c_SI`, `hbar_SI`. **Flags:** unreferenced dead-candidate; $\beta=6.6\times10^{-3}$ is a literal copy of the off-axis `qed_casimir.pair_bending_coeff` output ($-6.57\times10^{-3}$, sign dropped); $k_B$, $e$, $a_\text{cell}$ unregistered literals. Note: the symbol $a$ here is the plate *separation*, while `A_CELL` is the lattice cell.

### `engine/interactions/qed_electron_self_energy.py` — one-loop electron self-energy Σ(p), δm, Z₂ (F258)
**Status:** live · test-only · **Findings:** (registry none; docstring F258, F251, F252) · **Lattice:** continuum symbolic (S0–S4); S5 = 4-D hypercubic midpoint grid with the BCC even-law photon kernel · **Law:** even (internal photon only) · **Units:** natural ($m=1$ or lattice $a=1$)

**Does:** Feynman-gauge one-loop Σ: numerator algebra, log coefficients of δm and Z₂, the differential WT identity, on-shell subtraction, and a lattice-vs-continuum subtracted check. **SUPERSEDED (numbers only) by F277** — S12 removed the refold in `_selfenergy_AB`; F258 is partially superseded.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\gamma^\mu(\slashed k+m)\gamma_\mu=-2\slashed k+4m$ ($d=4$), explicit γ | numerator seed | `qed_electron_self_energy.py:L161–165 contraction_identity_symbolic()` | exact (inventory #280) |
| 2 | $\int_0^1(4-2x)dx=3$; $\delta m/(m\,\alpha\ln\Lambda^2/m^2)=\tfrac14\pi^{-1}\cdot3=3/4\pi$ | mass-shift log coefficient (textbook $\delta m=\tfrac{3\alpha}{4\pi}m\ln\tfrac{\Lambda^2}{m^2}$) | `L199–202 delta_m_coefficient_symbolic()` | unknown (inferred: exact) |
| 3 | $\int_0^1(-2x)dx=-1$; $(Z_2-1)/(\alpha\ln)=-1/4\pi$ | wavefunction renormalisation (textbook) | `L242–246 z2_coefficient_symbolic()` | unknown (inferred: exact) |
| 4 | $Z_1$ coefficient $=-1/4\pi$ (typed literal) and $Z_1=Z_2$ check | vertex log coefficient | `L247`, `L254` | unknown (inferred: exact (but see flags)) |
| 5 | $\partial_{p^\mu}(\slashed p-m)=\gamma_\mu$; $\partial S_F=-S_F\gamma_\mu S_F$ (exact 4×4 inverse, $\mu=0,1$, base $p=(5,2,1,3)$, $m=1$) | differential WT ingredients | `L295–322 differential_ward_identity_symbolic()` | unknown (inferred: exact) |
| 6 | model $\Sigma(s)=\tfrac1{4\pi}[-Ls+4mL+f(s)]$; $\Sigma_R=\Sigma-\Sigma(m)-(s-m)\Sigma'(m)$; $S_R^{-1}=(s-m)-\Sigma_R$ | on-shell subtraction: pole at $m$, residue 1 | `L368–383 renormalized_propagator_symbolic()` | unknown (inferred: exact) |
| 7 | $K_\text{lat}=3\,\Omega_\text{even}(k)^2+k_t^2$, $\Omega_\text{even}=\omega^+(k/2)+\omega^-(k/2)$ | rule photon inverse propagator | `L406 _omega_even()`, `L411 _K_lat()` | unknown (inferred: exact (closed form)) |
| 8 | Euclidean $D_e=k^2+m^2$; $D_\gamma=(k-p)^2+\mu^2$ or $K_\text{lat}(k-p)+\mu^2$; $A=\langle-2(p\cdot k)/p^2\,/(D_eD_\gamma)\rangle$, $B=\langle4/(D_eD_\gamma)\rangle$; $p=(P,0,0,0)$, $m=0.2$, $\mu=0.05$ | projected Lorentz coefficients, midpoint grid $n^4$ on $[-\pi,\pi)^4$ | `L437–438 _selfenergy_AB()` | unknown (inferred: quantitative) |
| 9 | $\Delta_A=A_\text{rule}-A_\text{cont}$, $\Delta_B$; pass if spread $<5\times10^{-2}$ over $P\in\{0.1,0.15,0.2,0.3\}$ | lattice = continuum log coefficient | `L451–461 lattice_consistency()` | unknown (inferred: quantitative) |

**Inputs → outputs:** none (symbolic) / $n$, $P$ list → coefficients and spreads. **Depends on:** `lattice.bcc.bcc_dispersion` (03-lattice.md), `c_lat` (imported, unused in formulas). **Flags:** (a) row 4 — the Z₁ coefficient is a hard-coded literal, so "Z₁ = Z₂ between the two computed loop objects" (docstring S3, inventory #280) compares a computed Z₂ with a typed-in Z₁ (⚠ DOC/CODE MISMATCH). (b) Row 5 checks generic matrix-calculus identities (derivative of an inverse), not the loop integral; the claim "dΣ/dp = −Λ(p,p) derived from the integrand" rests on the argument in the docstring. (c) Row 6's subtraction is zero by construction (Σ_R is defined as Σ minus its first two Taylor terms). (d) Row 8 uses a lattice photon but a continuum electron, on a hypercubic cell that is not the BCC zone (absolute measure open, F272 §4).

### `engine/interactions/qed_euler_heisenberg.py` — Euler–Heisenberg Lagrangian, light-by-light, vacuum birefringence (F263)
**Status:** live · test-only · **Findings:** (registry none; docstring F263) · **Lattice:** n/a (continuum constant-field effective action) · **Law:** n/a · **Units:** natural, Heaviside–Lorentz

**Does:** derives the weak-field EH coefficients from the proper-time integrand, then the low-energy γγ→γγ cross section and field-induced birefringence ratio from it.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | core $=(x\coth x)(y\cot y)-1-(x^2-y^2)/3$ to 4th order: $c_{x^4}=c_{y^4}=-\tfrac1{45}$, $c_{x^2y^2}=-\tfrac19$ | proper-time series | `qed_euler_heisenberg.py:L114–120 eh_coefficients_symbolic()` | exact (inventory #306) |
| 2 | $\mathcal L=-\tfrac1{8\pi^2}(c_{x^4}a^4+c_{y^4}b^4+c_{x^2y^2}a^2b^2)\cdot16\pi^2\alpha^2/m^4$ (uses $\int_0^\infty s\,e^{-m^2s}ds=1/m^4$, $e^4=16\pi^2\alpha^2$) | effective Lagrangian | `L123–125` | unknown (inferred: exact) |
| 3 | $a^4+b^4=4\mathcal F^2+2\mathcal G^2$, $a^2b^2=\mathcal G^2$ ⇒ $c_{\mathcal F^2}=8/45$, $c_{\mathcal G^2}=14/45$ (×α²/m⁴) | invariant basis | `L131–132` | unknown (inferred: exact) |
| 4 | $\mathcal L_\text{EH}=\tfrac{2\alpha^2}{45m^4}[(E^2-B^2)^2+7(E\cdot B)^2]$ (textbook value) | prefactor 2/45, weight 7 | `L135–139` | unknown (inferred: exact) |
| 5 | $\mathcal L=\mu(F\!\cdot\!F)^2+\nu(F\!\cdot\!\tilde F)^2$, $\mu=\alpha^2/90m^4$, $\nu=7\alpha^2/360m^4$; $\mathcal M=8\mu S_\Phi+8\nu S_\Psi$ with $f^i_{\mu\nu}=k^i_\mu\epsilon^i_\nu-k^i_\nu\epsilon^i_\mu$, $S$ = sum over the 3 pairings | contact 4-photon amplitude | `L196–205 _amp_builder()` | unknown (inferred: exact) |
| 6 | $\sigma=\tfrac12\cdot2\pi\int_{-1}^1\tfrac{\overline{\lvert\mathcal M\rvert^2}}{64\pi^2s}dc$, $s=4\omega^2$, avg over 4 initial pols, 16 linear-pol configurations | cross section | `L230–239 light_by_light_cross_section()` | exact (inventory #307) |
| 7 | $\sigma(\gamma\gamma\to\gamma\gamma)=\tfrac{973}{10125\pi}\alpha^4\omega^6/m^8$ (Karplus–Neuman, textbook) | target equality | `L241–243` | unknown (inferred: exact) |
| 8 | $\mathcal M(\epsilon^i\to k^i)=0$ each leg; invariance under $1\leftrightarrow2$, $3\leftrightarrow4$ | Ward + Bose | `L270–285 ward_and_bose_gates()` | exact (inventory #308) |
| 9 | $\mathcal L=\kappa(S^2+7P^2)$ about background $B\hat x$; 2nd-order probe coefficient: parallel $7\kappa B^2e^2$, perpendicular $4\kappa B^2e^2$ | birefringence ratio 7:4 | `L316–330 birefringence_ratio_symbolic()` | exact (inventory #309) |

**Inputs → outputs:** symbolic → rational coefficients; EH5 (`observational_contact`, L351) is a text record only. **Depends on:** sympy. **Flags:** (a) ⚠ DOC/CODE MISMATCH — the returned strings/docstring give $n_\parallel-1=(7/2)(2\alpha^2/45)B^2/m^4$ "via $n-1=\Delta L/2e^2$"; from the Lagrangian the code uses, the parallel mode has $\delta\varepsilon=14\kappa B^2$, so $n_\parallel-1=7\kappa B^2=\tfrac{14\alpha^2}{45}\tfrac{B^2}{m^4}$ (the textbook Heaviside–Lorentz value, $=\tfrac{7\alpha}{90\pi}(B/B_c)^2$); the string is a factor 2 low. Only the ratio 7:4 is computed. (b) The docstring statement "7 = 2/45 + 5/45 over 2/45" is arithmetically 7/2; the code's actual decomposition is $(4/45+10/45)/(2/45)=7$.

### `engine/interactions/qed_ir_bremsstrahlung.py` — soft photons, Bloch–Nordsieck, Sudakov (F259)
**Status:** live · test-only · **Findings:** (registry none; docstring F259, F252, F258) · **Lattice:** n/a (continuum; $c_\text{lat}$ argued to cancel) · **Law:** even (stated for the soft photon, not used) · **Units:** natural / MeV

**Does:** eikonal soft-emission factor, current conservation, the IR log, the μ-cancellation between virtual and real, and a Sudakov number.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\gamma^\mu(\slashed p+m)+(\slashed p-m)\gamma^\mu=2p^\mu$ (⇒ $\bar u(p')\gamma^\mu(\slashed p'+m)=2p'^\mu\bar u$) | on-shell eikonal identity | `qed_ir_bremsstrahlung.py:L138–142 eikonal_factor_symbolic()` | exact (inventory #281) |
| 2 | $J^\mu=p'^\mu/p'\!\cdot\!k-p^\mu/p\!\cdot\!k$, $k\cdot J=0$ | eikonal current conservation | `L185–186 eikonal_current_conservation_symbolic()` | exact (inventory #282) |
| 3 | $-J\cdot J=2p\cdot p'/((p\cdot k)(p'\cdot k))-m^2/(p'\cdot k)^2-m^2/(p\cdot k)^2$ | pol-sum collapse | `L191–194` | unknown (inferred: exact) |
| 4 | $\int_\mu^{\Delta E}d\omega/\omega=\ln(\Delta E/\mu)$ | IR log | `L228` | exact (inventory #283) |
| 5 | $c_\text{lat}^{-3}/c_\text{lat}^{-3}=1$ | "c_lat cancels" | `L240 ir_log_coefficient_symbolic()` | unknown (inferred: exact (tautology)) |
| 6 | $A(\hat n)=2p\cdot p'/((p\cdot\hat k)(p'\cdot\hat k))-m^2/(p'\cdot\hat k)^2-m^2/(p\cdot\hat k)^2$, $\hat k=(1,\hat n)$; $f_\text{IR}=\tfrac12\cdot\tfrac1{4\pi}\int A\,d\Omega$ ($\theta_s=\pi/2$, $400^2$ midpoint grid); closed $\ln(-q^2/m^2)-1$ | shared IR coefficient | `L292–301 eikonal_ir_function()` | quantitative (inventory #285, 8e-4) |
| 7 | virtual $-(\alpha/\pi)f_\text{IR}\ln(-q^2/\mu^2)$ + real $+(\alpha/\pi)f_\text{IR}\ln(\Delta E^2/\mu^2)$; $\partial_{\mu^2}(\text{sum})=0$; sum $=-(\alpha/\pi)f_\text{IR}\ln(-q^2/\Delta E^2)$ | Bloch–Nordsieck | `L340–350 bloch_nordsieck_cancellation_symbolic()` | exact (inventory #284) |
| 8 | $f_\text{IR}=\ln(-q^2/m^2)-1$; $\delta=-(\alpha/\pi)f_\text{IR}\ln(-q^2/\Delta E^2)$; YFS $e^\delta$; double log $-(\alpha/\pi)\ln(-q^2/m^2)\ln(-q^2/\Delta E^2)$ | finite Sudakov observable | `L381–385 sudakov_observable()` | quantitative (inventory #286) |

**Inputs → outputs:** $-q^2/m^2$, $\sqrt{-q^2}$, $\Delta E$ fraction → $f_\text{IR}$, O(α) correction. **Depends on:** `c_lat` (imported; unused numerically). **Flags:** (a) ⚠ DOC/CODE MISMATCH — module docstring Q2 writes $\sigma/\sigma_0=1-(\alpha/2\pi)f_\text{IR}\ln(\ldots)$ and double log with $\alpha/2\pi$; the code (rows 7–8) uses $\alpha/\pi$. (b) Row 7: both the virtual and real terms are typed with the *same* symbol $f_\text{IR}$, so the μ-cancellation is by construction; neither is computed from F252/F258 here. (c) Row 5 is a tautology ($x/x=1$), not a derivation of $c_\text{lat}$-independence.

### `engine/interactions/qed_renormalization.py` — renormalisability, WT to all orders, charge universality, Callan–Symanzik, Landau pole (F264 part 1)
**Status:** live · test-only · **Findings:** (registry none; docstring F264, F251, F252, F258, F107) · **Lattice:** n/a (continuum; lattice enters only as the F107 UV cutoff) · **Law:** n/a · **Units:** natural; GeV for R3c

**Does:** the structural closure of QED: power counting, counterterm census, the telescoping WT proof, $Z_1=Z_2$, $e_R=Z_3^{1/2}e_0$, β/γ functions, and the Landau-pole-vs-cutoff comparison.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $D=4L-I_f-2I_g$ with $L=I_f+I_g-V+1$, $2V=2I_f+E_f$, $V=2I_g+E_\gamma$ ⇒ $D=4-\tfrac32E_f-E_\gamma$, $\partial_VD=\partial_LD=0$ | superficial degree | `qed_renormalization.py:L193–211 superficial_degree_symbolic()` | exact (inventory #313) |
| 2 | enumerate even $E_f$, $E_\gamma\le8$ with $D\ge0$; Furry kills odd $E_\gamma$ at $E_f=0$; $D_\text{eff}=D-E_\gamma$ for $E_f=0,E_\gamma\ge2$; counterterms assigned per case | divergent-amplitude census → $\{Z_1,Z_2,Z_3,\delta m\}$ | `L272–339 divergent_amplitude_census()` | exact (inventory #314) |
| 3 | 12-row hand-typed operator catalogue (dim, gauge, P, C flags); keep dim ≤ 4, all flags true, not unit op | counterterm operator basis (4 survivors) | `L375–424 counterterm_operator_basis()` | exact (inventory #315; lookup table) |
| 4 | $S(v)=(\slashed v+m)/(v^2-m^2)$; $S(p')\slashed qS(p)=S(p)-S(p')$ symbolic; telescope $\sum_{i=0}^n S(k_n{+}q)\cdots S(k_i{+}q)\,\slashed q\,S(k_i)\cdots S(k_0)=T_{n+1}-T_0$ in exact rationals, $n\le4$, 3 draws, seed 20260726 | all-orders WT engine | `L519–585 photon_insertion_telescoping_symbolic()` | exact (inventory #316) |
| 5 | $\Gamma^\mu(p,p)=\partial S^{-1}/\partial p_\mu$ with $S^{-1}=Z_2^{-1}(\slashed p-m)$, $\Gamma^\mu=Z_1^{-1}\gamma^\mu$ ⇒ unique entrywise solution $Z_1=Z_2$ | $Z_1=Z_2$ | `L658–690 differential_wt_forces_z1_eq_z2_symbolic()` | exact (inventory #317) |
| 6 | $Z_1^{1\text{-loop}}=Z_2^{1\text{-loop}}=1-\tfrac\alpha{4\pi}\ln(\Lambda^2/m^2)$ (both typed) | one-loop instance | `L697–699` | unknown (inferred: exact (tautology)) |
| 7 | $Z_{1,2}^{(f)}=1-\tfrac\alpha{4\pi}\ln(\Lambda^2/m_f^2)$; $e_R=Z_1^{-1}Z_2Z_3^{1/2}e_0\to Z_3^{1/2}e_0$, $e_R^{(1)}-e_R^{(2)}=0$; $Z_3=1-\tfrac\alpha{3\pi}\ln(\Lambda^2/m^2)$ | charge universality | `L762–778 charge_universality_symbolic()` | exact (inventory #318) |
| 8 | $\alpha=e^2/4\pi$, $(d\alpha/de)\beta=2\alpha^2/3\pi$ ⇒ $\beta(e)=e^3/12\pi^2$; $b_0$ read back $=4/3$ | β from F251 $b_0$ | `L851–867 callan_symanzik_symbolic()` | exact (inventory #319) |
| 9 | $\gamma_3=\tfrac12\mu\,\partial_\mu\ln Z_3\to\alpha/3\pi=e^2/12\pi^2$; $\gamma_2=\alpha/4\pi$ (Feynman gauge) | anomalous dimensions | `L870–883` | unknown (inferred: exact) |
| 10 | $\beta-e\gamma_3=0$ | structural all-orders relation (checked at one loop on the target strings) | `L886` | exact (inventory #320) |
| 11 | $\mu_L=m_e\exp(3\pi/2\alpha_0)$; $\Lambda_a=\hbar c/a$, $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ (F79/F107); $\alpha(\mu)=\alpha_0/[1-\tfrac{\alpha_0}{3\pi}\ln(\mu^2/m_e^2)]$ | Landau pole vs lattice cutoff | `L958–970 landau_pole()` | quantitative (inventory #332: $\log_{10}\mu_L=277.2$ vs 18.3) |

**Inputs → outputs:** symbolic; $\alpha_0^{-1}=137.035999$ (literal), `m_e_GeV`, `a_over_ellP`, `ell_P_m` → pole scale and decades. **Depends on:** 01-constants.md (`a_over_ellP`, `ell_P_m`, `m_e_GeV`). **Flags:** (a) rows 2–3 are classification tables with hand-assigned verdicts/flags; the "exact" is of a lookup, not a derivation. (b) Row 6 compares two identical typed expressions. (c) Row 10 checks $\beta=e\gamma_3$ on the typed target strings, not on the computed β and γ₃ (those are checked separately against the same targets, so the chain is consistent). (d) $\hbar c=1.97327\times10^{-16}$ GeV m and $\alpha_0^{-1}=137.035999$ (differs from the 137.035999177 used by every other module in this batch) are unregistered literals.

### `engine/interactions/qed_scattering.py` — tree-level QED S-matrix and the positron sector (F260)
**Status:** live · test-only · **Findings:** (registry none; docstring F260, F249) · **Lattice:** n/a (continuum Dirac spinors and traces) · **Law:** n/a · **Units:** natural ($m=1$), MeV/barn for cross sections

**Does:** Compton, Møller, Bhabha, pair annihilation and $e^+e^-\to\mu^+\mu^-$ from explicit Dirac traces, checked against the textbook $\overline{\lvert\mathcal M\rvert^2}$ and σ.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $C=i\gamma^2\gamma^0$; $C\gamma^\mu C^{-1}=-(\gamma^\mu)^T$, $C^T=-C$, $C^\dagger C=1$, $C^2=-1$ (sympy) | charge conjugation | `qed_scattering.py:L143–151 charge_conjugation_symbolic()` | exact (inventory #287) |
| 2 | $u=\sqrt{E+m}\,(\chi,\ \boldsymbol\sigma\!\cdot\!\mathbf p\,\chi/(E+m))$; $v=C\bar u^T$ | spinors (ū u = 2m) | `L101 u_spinor()`, `L121–122 v_spinor()` | unknown (inferred: exact) |
| 3 | $(\slashed p-m)u=0$, $(\slashed p+m)v=0$, $\sum u\bar u=\slashed p+m$, $\sum v\bar v=\slashed p-m$ (8 random momenta, tol $10^{-11}$) | positron / completeness | `L181–186 positron_spinor_gates()` | machine (inventory #288) |
| 4 | $\overline{\lvert\mathcal M\rvert^2}=\tfrac{e^4}4\sum_{\mu\nu}\eta_{\mu\mu}\eta_{\nu\nu}\mathrm{Tr}[(\slashed p'+m)\Gamma(\slashed p+m)\bar\Gamma]$, $\Gamma=\gamma^\nu(\slashed p+\slashed k+m)\gamma^\mu/(2p\cdot k)+\gamma^\mu(\slashed p-\slashed k'+m)\gamma^\nu/(-2p\cdot k')$ | Compton trace | `L251–257 compton_M2_trace()` | unknown (inferred: machine) |
| 5 | vs $2e^4[\tfrac{p\cdot k'}{p\cdot k}+\tfrac{p\cdot k}{p\cdot k'}+2m^2(\tfrac1{p\cdot k}-\tfrac1{p\cdot k'})+m^4(\tfrac1{p\cdot k}-\tfrac1{p\cdot k'})^2]$ (PS 5.87, textbook) | Klein–Nishina $\lvert\mathcal M\rvert^2$ | `L282–284 compton_M2_vs_textbook()` | machine (inventory #290) |
| 6 | $k_\mu\mathcal M^{\mu\nu}=k'_\nu\mathcal M^{\mu\nu}=0$ on explicit spinors | Compton Ward | `L309–318 compton_ward_symbolic()` | machine (inventory #291) |
| 7 | $\omega'=\omega/(1+x(1-\cos\theta))$; $d\sigma/d\Omega=\tfrac1{64\pi^2m^2}(\omega'/\omega)^2\lvert\mathcal M\rvert^2$; KN closed $2\pi r_e^2\{\tfrac{1+x}{x^2}[\tfrac{2(1+x)}{1+2x}-\tfrac{\ln(1+2x)}x]+\tfrac{\ln(1+2x)}{2x}-\tfrac{1+3x}{(1+2x)^2}\}$, $r_e=\alpha/m$ | KN total σ | `L263 _compton_lab_kin()`, `L341 sigma_num`, `L347 sigma_closed` | quantitative (inventory #292) |
| 8 | $\sigma_T=\tfrac{8\pi}3r_e^2$, $r_e=\alpha\hbar c/m_e$ (barn) | Thomson limit | `L360–363 klein_nishina()` | unknown (inferred: quantitative) |
| 9 | Møller: $[\text{Tr}\,\text{Tr}/t^2+\text{Tr}\,\text{Tr}/u^2-2\,\text{Tr}/(tu)]\,e^4/4$ vs $2e^4[\tfrac{s^2+u^2}{t^2}+\tfrac{s^2+t^2}{u^2}+\tfrac{2s^2}{tu}]$ (massless) | Møller | `L398–401 moller_M2_trace()`, `L420 moller_vs_textbook()` | machine (inventory #293) |
| 10 | Bhabha: $t$ + $s$ channels, $-2\,\text{Tr}/(st)$, vs $2e^4[\tfrac{s^2+u^2}{t^2}+\tfrac{u^2+t^2}{s^2}+\tfrac{2u^2}{st}]$ | Bhabha | `L409–412 bhabha_M2_trace()`, `L433` | machine (inventory #293) |
| 11 | Bhabha$(s,t,u)$ = Møller$(u,t,s)$; annihilation$(a,b)=-$Compton$(-a,b)$ (sympy) | crossing | `L449–456 crossing_symbolic()` | exact (inventory #289) |
| 12 | $d\sigma/d\Omega=\lvert\mathcal M\rvert^2/(64\pi^2s)\cdot(\hbar c)^2$ → barn/sr | CM differentials | `L473–474 moller_bhabha_differential()` | unknown (inferred: quantitative) |
| 13 | annihilation trace (t/u electron exchange, $\slashed p'-m$ for $e^+$) vs $2e^4[\tfrac{p\cdot k}{p\cdot k'}+\tfrac{p\cdot k'}{p\cdot k}+2m^2(\tfrac1{p\cdot k}+\tfrac1{p\cdot k'})-m^4(\ldots)^2]$; Bose $k\leftrightarrow k'$; Ward both photons | $e^+e^-\to\gamma\gamma$ | `L493–503 annih_M2_trace()`, `L523–548 annihilation_gates()` | machine (inventory #294) |
| 14 | $\sigma=\tfrac12\int\tfrac{\lvert\mathcal M\rvert^2}{64\pi^2s\beta}d\Omega$ vs $\tfrac{2\pi\alpha^2}{s\beta}[\tfrac{3-\beta^4}{2\beta}\ln\tfrac{1+\beta}{1-\beta}-(2-\beta^2)]$ | Dirac total σ | `L562–564` | quantitative (inventory #294) |
| 15 | $\lvert\mathcal M\rvert^2=\tfrac{e^4}{4s^2}\sum\eta\eta\,\mathrm{Tr}_e\mathrm{Tr}_\mu$ vs $\tfrac{8e^4}{s^2}[(p_1k_1)(p_2k_2)+(p_1k_2)(p_2k_1)+m_\mu^2p_1p_2]$; $\sigma=\tfrac{4\pi\alpha^2}{3s}\beta(1+2m_\mu^2/s)$ | $e^+e^-\to\mu^+\mu^-$ | `L591–594 mupair_M2_trace()`, `L612`, `L634` | machine / quantitative (inventory #295) |

**Inputs → outputs:** α, $m_e$, $m_\mu$, $\hbar c$, $\sigma_T$ (all literals) → residuals, σ. **Depends on:** numpy (complex128 traces; no eig). **Flags:** ⚠ DOC/CODE MISMATCH (minor) — the module header says "the Ward identities are sympy-exact (literal 0)", but `compton_ward_symbolic` and the annihilation Ward check are numeric (tol $10^{-12}$), consistent with inventory #291's "machine". Masses are called "model anchors F120/F121" but are CODATA literals.

### `engine/interactions/qed_schwinger_pair.py` — Schwinger pair production (F263)
**Status:** live · test-only · **Findings:** (registry none; docstring F263) · **Lattice:** n/a · **Law:** n/a · **Units:** natural (SC1, SC3), SI (SC2)

**Does:** imaginary part of the pure-electric proper-time effective action; critical fields; instanton sum.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathcal L=-\tfrac1{8\pi^2}\int\tfrac{ds}{s^3}e^{-m^2s}[eEs\cot(eEs)-1+\tfrac{(eEs)^2}3]$; pole $s_n=n\pi/eE$; $\mathrm{Im}\mathcal L_n=-\pi\,\mathrm{Res}_{s_n}=\tfrac{(eE)^2}{8\pi^3n^2}e^{-n\pi m^2/eE}$ (textbook) | Schwinger residues | `qed_schwinger_pair.py:L82–87 schwinger_exponent_symbolic()` | exact (inventory #310) |
| 2 | $w=2\,\mathrm{Im}\mathcal L=\tfrac{(eE)^2}{4\pi^3}\sum_n n^{-2}e^{-n\pi m^2/eE}$, $E_\text{crit}=m^2/e$ | rate (string) | `L94` | unknown (inferred: exact) |
| 3 | $E_\text{crit}=m_e^2c^3/(e\hbar)$, $B_\text{crit}=m_e^2c^2/(e\hbar)$ | SI critical fields | `L111–112 critical_field()` | quantitative (inventory #311) |
| 4 | $R(x)=\sum_{n=1}^{100}n^{-2}e^{-n\pi/x}$, $x=E/E_\text{crit}$ | instanton sum | `L137–138 pair_production_rate()` | unknown (inferred: quantitative) |
| 5 | Taylor series of $e^{-\pi E_c/E}$ about $E=0$ $\equiv0$ | non-perturbative | `L159–160 non_perturbative_check()` | exact (inventory #312) |

**Inputs → outputs:** symbolic; $m_e$ (kg), $e$ literals + `c_SI`, `hbar_SI` → $E_\text{crit}=1.323\times10^{18}$ V/m. **Depends on:** 01-constants.md (`c_SI`, `hbar_SI`). **Flags:** OTHER — the docstring calls $w=2\,\mathrm{Im}\mathcal L$ "the vacuum pair-creation probability per unit volume-time"; that is the vacuum-decay (persistence) rate; the mean number of pairs produced per unit volume-time is the $n=1$ term only (Nikishov). Code does not depend on the reading. $m_e$ (kg) and $e$ unregistered.

### `engine/interactions/qed_twoloop_ae.py` — two-loop $a_e$ ($A_2$) and two-loop running of α (F261)
**Status:** live · test-only · **Findings:** (registry none; docstring F261, F251, F252) · **Lattice:** n/a (continuum dispersive integrals) · **Law:** n/a · **Units:** dimensionless (coefficients of $(\alpha/\pi)^n$), masses in MeV

**Does:** the VP-insertion group of $A_2$ by a Källén–Lehmann integral, the closed-form $A_2$, $a_e$ through two loops, and the two-loop β.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $K_1(u)=\int_0^1\frac{x^2(1-x)}{x^2+u(1-x)}dx$ (128-pt Gauss–Legendre), $K_1(0)=\tfrac12$ | massive-photon anomaly kernel | `qed_twoloop_ae.py:L111 K1()` | unknown (inferred: machine (spot-check $K_1(0)=0.5-10^{-16}$)) |
| 2 | $\tfrac1\pi\mathrm{Im}\,\Pi(s)/(\alpha/\pi)=\tfrac13(1+2m_f^2/s)\sqrt{1-4m_f^2/s}$, $s>4m_f^2$ | one-loop spectral function (textbook form; defined but not called by row 3, which inlines it) | `L126 vp_spectral()` | unknown (inferred: exact (closed form)) |
| 3 | $A_2^{VP,f}(\ell)=\tfrac23\int_0^{\Theta}d\theta\,(1+\tfrac1{2\cosh^2\theta})\tanh^2\theta\,K_1(4m_f^2\cosh^2\theta/m_\ell^2)$, $s=4m_f^2\cosh^2\theta$, $\Theta=\ln(m_\ell/m_f)+30$, 400-pt GL | dispersive VP insertion | `L148–154 A2_vp_dispersive()` | quantitative (inventory #296: equal mass $119/36-\pi^2/3$ to 3e-10) |
| 4 | $A_2=(\tfrac{119}{36}-\tfrac{\pi^2}3)+(-\tfrac{31}{16}+\tfrac{5\pi^2}{12}-\tfrac{\pi^2}2\ln2+\tfrac34\zeta_3)=\tfrac{197}{144}+\tfrac{\pi^2}{12}-\tfrac{\pi^2}2\ln2+\tfrac34\zeta_3=-0.328478966$ (Sommerfield–Petermann, textbook) | $A_2$ closed form; group II is a cited literature constant | `L193–200 A2_assembly_symbolic()` | exact (inventory #297; group II external) |
| 5 | $A_2(e)=A_2^\text{mi}+A_2^{VP}(\mu\text{ in }e)+A_2^{VP}(\tau\text{ in }e)$; $a_e=\tfrac12\tfrac\alpha\pi+A_2(e)(\tfrac\alpha\pi)^2$ | $a_e$ through two loops | `L233–234 a_e_two_loop()` | quantitative (inventory #299, rel err 1.3e-5) |
| 6 | $\mu\,de/d\mu=\tfrac{e^3}{12\pi^2}+\tfrac{e^5}{64\pi^4}$ (typed, textbook) → $\mu\,d\alpha/d\mu=\tfrac{2\alpha^2}{3\pi}+\tfrac{\alpha^3}{2\pi^2}$; $b_0=4/3$, $b_1=1$ (typed) | two-loop running | `L274–294 two_loop_beta_symbolic()` | exact (inventory #298) |

**Inputs → outputs:** α, $m_e,m_\mu,m_\tau$ (literals, called "F120/F121 anchors" but CODATA/PDG values) → $A_2$, $a_e$, β coefficients. **Depends on:** numpy directly (`np.polynomial.legendre.leggauss`, D8 debt). Used by `qed_amu`. **Flags:** (a) ⚠ DOC/CODE MISMATCH — the docstring says group (I) is "computed HERE FROM THE MODEL'S OWN Π" (F251); the spectral function in rows 2–3 is the textbook continuum formula typed in; `qed_vacuum_polarization` never computes $\mathrm{Im}\,\Pi$. (b) The $A_2$ fed to `a_e_two_loop` and `qed_amu` is the typed closed form (row 4), not the numeric dispersive value; the dispersive integral enters only through the heavy-lepton insertions and the $e$-in-$\mu$ term. (c) Row 6's $b_1=1$ is a typed integer; what is checked is the $\alpha^3$ coefficient $1/2\pi^2$. (d) L276–278 compute `beta_alpha` and immediately overwrite it (dead code).

### `engine/interactions/qed_twoloop_vacuum_polarization_nonlog.py` — two-loop VP leading log by unitarity + dispersion; non-log constant scoped (F336)
**Status:** live · standalone · **Findings:** F336 F251 F261 F311 F322 · **Lattice:** n/a (continuum dispersion) · **Law:** n/a · **Units:** dimensionless, $m_f=1$

**Does:** calibrates a Euclidean dispersion integral at one loop, then feeds a cited constant two-loop spectral density to recover the $b_1$ leading log; records what the non-log constant would need.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathrm{Im}\,\Pi^{(1)}/\alpha=\tfrac13(1+2m_f^2/s)\sqrt{1-4m_f^2/s}$ | one-loop spectral density (duplicate of `qed_twoloop_ae.vp_spectral`) | `qed_twoloop_vacuum_polarization_nonlog.py:L135 im_pi1_over_alpha()` | quantitative (reg) |
| 2 | $\Delta\alpha(Q^2)=\tfrac{Q^2}\pi\int_{4m^2}^\infty\frac{ds\,\mathrm{Im}\Pi(s)}{s(s+Q^2)}$, $s=4m^2\cosh^2\theta$, $\theta\le60$, 4000-pt GL, $Q^2=10^{12}$; vs $\tfrac\alpha{3\pi}[\ln(Q^2/m^2)-\tfrac53]$ | CAL one-loop gate (rel tol 1e-8) | `L152–160 one_loop_dispersion_calibration_gate()` | quantitative (reg) |
| 3 | $R_\text{tree}=1\Rightarrow\mathrm{Im}\Pi^{(1)}_\infty/\alpha=\tfrac13$; $R^{(1)}=\tfrac34\tfrac\alpha\pi$ (**cited**, Appelquist–Georgi/Zee); $\mathrm{Im}\Pi^{(2)}_\infty=\tfrac\alpha3R^{(1)}=\alpha^2/4\pi$; LL coefficient $=\mathrm{Im}\Pi^{(2)}_\infty/\pi/(\alpha/\pi)^2=\tfrac14=b_1/4$ | two-loop leading log (sympy) | `L201–213 two_loop_leading_log_symbolic()` | quantitative (reg) |
| 4 | $C=\tfrac\alpha3\cdot R^{(1)}$; dispersion of constant $C$ vs $\tfrac C\pi\ln(1+Q^2/4m^2)$; $C/\pi$ vs $(\alpha/\pi)^2/4$ | numeric leading log | `L255–275 two_loop_leading_log_numeric_check()` | quantitative (reg) |
| 5 | three-leg map F336-1/2/3; `R1_control` perturbs rows 3–4 only | registry entry point | `L365–382 check_f336_twoloop_nonlog()` | n/a (plumbing) |

`nonlog_constant_scope()` (L306) returns text only: the non-log constant $(\alpha/\pi)^2[\zeta_3-5/24]$ (Källén–Sabry) is **not derived**. **Inputs → outputs:** α literal, optional control → leg map; `__main__` writes `test-results/F336_twoloop_vp_nonlog.json` (guarded). **Depends on:** `casim.numerics.xp` (D8-compliant), sympy. **Flags:** (a) ⚠ DOC/CODE MISMATCH — the docstring header calls the LL result "genuinely NEW model-internal content ... independent", while the in-docstring review note (2026-08-30) says it is "largely RG-forced" given the two citations; the code's LL leg is $\tfrac13\cdot\tfrac34=\tfrac14$ with $R^{(1)}$ typed in. (b) Row 1 is the textbook spectral function, not one extracted from `qed_vacuum_polarization` (same issue as `qed_twoloop_ae`). (c) Registry says `quantitative` for rows that are sympy identities — left as registry per the brief.

### `engine/interactions/qed_uv_completion.py` — physical cutoff + counterterms reconciled; leading irrelevant photon operator; Sakharov over-determination (F319)
**Status:** live · standalone · **Findings:** F319 F264 F164 F116 F284 F59 F79 F107 F251 F301 F69 F26 · **Lattice:** U1–U4 use a **4-D hypercubic** Wilson/Symanzik symbol $\hat k^2=4\sin^2(k/2)$ (simple-cubic reference, D1 — not BCC); U5/U6/U8 use the BCC dispersion (F26) · **Law:** even (U5 via `pair_dispersion`) · **Units:** lattice; SI/GeV for U6–U8

**Does:** shows lattice loop finite vs continuum log, scheme constants IR-blind, universal $1/16\pi^2$; derives the $O(k^2)$ photon dispersion excess in closed form; solves the uniform zero-point reweighting for (λ, a); tabulates Λ-sensitive operators.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $D(t)=\langle e^{-t\hat k^2}\rangle_{k\in[-\pi,\pi)}$ (periodic trapezoid, 8192 pts); wilson $\hat k^2=4\sin^2(k/2)$, symanzik $\hat k^2+\hat k^4/12$ | 1-D BZ factor ($=e^{-2t}I_0(2t)$ for Wilson) | `qed_uv_completion.py:L171–180 bz_factor()` | machine (docstring 2.2e-16) (reg: exact; row is weaker — see flags) |
| 2 | $\varepsilon(T)=D(T)^4(4\pi T)^2-1$; tail $\varepsilon\,e^{-Tm^2}/16\pi^2$ | measured asymptotic defect, analytic tail | `L199–200 _asymptotic_defect()`, `L214–215 _tail_correction()` | quantitative (reg: exact; row is weaker — see flags) |
| 3 | $I_\text{lat}-I_\text{PV}=\int dt\,[t\,e^{-tm^2}D^4-(e^{-tm^2}-e^{-tM^2})/(16\pi^2t)]$ (trapezoid in $\ln t$, $t\in[10^{-8},10^4]$) + small-$t$ piece $\tfrac12t_0^2-(M^2-m^2)t_0/16\pi^2$ + tail; $I_\text{PV}=\ln(M^2/m^2)/16\pi^2$ | lattice scheme constant | `L233–245 I_lattice_minus_pv()` | quantitative (reg: exact; row is weaker — see flags) |
| 4 | $I_\text{lat}=\text{const}+\ln(1/m^2)/16\pi^2$ | lattice loop | `L251 I_lattice()` | quantitative (reg: exact; row is weaker — see flags) |
| 5 | $I_\text{sphere}=[\ln((\Lambda^2+m^2)/m^2)-\Lambda^2/(\Lambda^2+m^2)]/16\pi^2$ | continuum hard 4-sphere | `L256 I_continuum_sphere()` | exact (reg) |
| 6 | $\lim_{m\to0}(I_a-I_b)=\int dt\,t(D_a^4-D_b^4)$ + tail $C/T$ | scheme constant at $m=0$ | `L268–277 scheme_constant()` | quantitative (reg: exact; row is weaker — see flags) |
| 7 | log coefficient $=t^2D(t)^4\vert_{t=10^5}\to1/16\pi^2$ | universality read off the kernel | `L299–300 log_coefficient()` | quantitative (spot-check: Wilson $1+2.5\times10^{-6}$, Symanzik $1+8\times10^{-12}$ in units $1/16\pi^2$) (reg: exact; row is weaker — see flags) |
| 8 | $\frac{\Omega_\text{pair}(k)-c_\text{lat}\lvert k\rvert}{c_\text{lat}\lvert k\rvert}=\big[-\tfrac{1-\sum_i\hat n_i^4}{144}-\tfrac{(\hat n_x\hat n_y\hat n_z)^2}{24}\big]\lvert k\rvert^2+O(k^4)$; range $[-\tfrac1{162},0]$ | leading irrelevant (dim-6) operator | `L319–322 dispersion_excess_closed_form()`; `L355 closed_form_mp()` | exact (reg) |
| 9 | $\sum_\pm\arccos(\cos q_x\cos q_y\cos q_z\pm\sin q_x\sin q_y\sin q_z)$, $q=k\hat n/(2\sqrt3)$, 60 digits, $\lvert k\rvert=10^{-10}$ | engine symbol re-implemented in mpmath | `L376–389 dispersion_excess_mp()` | exact (reg) |
| 10 | float engine excess via `pair_dispersion` at $\lvert k\rvert=10^{-2}$; scaling exponent $p=\log_{10}(\text{rel}(0.1)/\text{rel}(0.01))\approx2$ along ⟨111⟩ | "no dim-5 operator" | `L336–338 dispersion_excess()`, `L609–613 check_uv_completion()` | quantitative (tol $10^{-4}$ on $p$) (reg: exact; row is weaker — see flags) |
| 11 | $\Lambda_\text{UV}=\hbar c/a$, $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ (F79/F107), in GeV | UV cutoff | `L394–396 lambda_uv_GeV()` | exact (reg) |
| 12 | $I_{cc}=\langle\omega/2\rangle$, $I_g=\langle1/2\omega\rangle$ over a $90^3$ midpoint grid on the cube of side $2\pi\sqrt3$, measure $(L/n)^3/(2\pi)^3$, $\omega=\omega^+$ (BCC) | two Sakharov moments | `L413–421 sakharov_moments()` | quantitative (reg: exact; row is weaker — see flags) |
| 13 | $\rho_0=\lambda\,g_*\sqrt3\,I_{cc}\,\hbar c/a_0^4$ ($g_*=2$); $R=\rho_0/\rho_\Lambda$, $\rho_\Lambda=6.0\times10^{-10}$ J/m³; $a^*=a_0\sqrt R$, $\lambda^*=R$; selectivity $R\times2.2\times10^{-5}$ | uniform-reweighting over-determination | `L445–459 two_sector_solve()` | quantitative (leg: $\log_{10}R=120.76\pm0.02$) (reg: exact; row is weaker — see flags) |
| 14 | $D=4-\tfrac32E_f-E_\gamma$, $\partial_VD=\partial_LD=0$ | power counting (re-derived) | `L493–499 superficial_degree()` | exact (reg) |
| 15 | $\lvert\Delta\Omega/\Omega\rvert_\text{max}=(E/\Lambda_\text{UV})^2/162$ at $m_e$, $M_Z$, 13 TeV, 1.4 PeV | decoupling | `L639–641` | exact (reg) |
| 16 | $\log_{10}\mu_L=\log_{10}m_e+\tfrac{3\pi}{2\alpha}/\ln10$; $1/\alpha(\Lambda_\text{UV})=1/\alpha-\tfrac2{3\pi}\ln(\Lambda_\text{UV}/m_e)$ | perturbative domain | `L647–648` | quantitative (reg: exact; row is weaker — see flags) |
| 17 | 8-row `UV_LEDGER`; unabsorbable = $D\ge0$, no free parameter, not "FORBIDDEN" → exactly 2 (CC, EH) | Λ-sensitivity ledger | `L467–482`, `L665–676` | exact (reg) |

**Inputs → outputs:** control parameters (`zero_point_weight`, `linear_control`, `scheme_b`, `break_universality`) → `checks` leg map + payload; `__main__` writes `test-results/F319_uv_completion.json` (guarded). **Depends on:** `casim.numerics.xp`; `c_lat`, `a_over_ellP`, `ell_P_m`, `hbar_SI`, `c_SI`, `J_per_GeV`, `m_e_GeV` (01-constants.md); `gauge.photon.pair_dispersion` (05c); `lattice.bcc.bcc_dispersion` (03-lattice.md). **Flags:** (a) EXACTNESS tension — registry says `exact` for the whole module, but rows 2–4, 6, 7, 10, 12, 13, 16 are quadratures/fits with tolerances (quantitative). (b) The U1–U4 "lattice" is the simple-cubic Wilson/Symanzik symbol in 4-D, a reference regulator (D1), not the BCC walk. (c) Row 13's $\sqrt3$ factor and $g_*=2$ are not explained in the code (presumably the $k$-convention Jacobian and two polarisations) — UNPINNED. (d) U3's Pauli–Villars and dim-reg "closed forms" (L555–558) are typed expressions whose $L$-derivative is $1/16\pi^2$ by construction. (e) $\rho_\Lambda$, $G$ uncertainty, α ($1/137.035999177$, L646), 1 Gpc in m are unregistered literals. (f) U8 is the result that EXCLUDED F193 Part A (supersession S25, by F319); the code itself is live.

### `engine/interactions/qed_vacuum_polarization.py` — one-loop photon self-energy Π^{μν}, $b_0^\text{QED}=4/3$, running α (F251)
**Status:** live · test-only · **Findings:** (registry none; docstring F251, F162, F250) · **Lattice:** continuum symbolic (Π1, Π2, Π4); Π3 = 4-D hypercubic midpoint grid with the BCC even-law photon kernel · **Law:** even (Π3 kernel) · **Units:** natural; MeV for Π4

**Does:** symbolic UV-log coefficient of the fermion bubble (transversality + $b_0=4/3$), explicit-γ trace check, lattice-vs-continuum subtracted coefficient, leptonic $\Delta\alpha(M_Z)$. **SUPERSEDED (numbers only) by F277** — S12 removed the refold in `_fermion_B` (Δ changed sign); F251 partially superseded.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $N^{\mu\nu}=4[k^\mu(k+q)^\nu+k^\nu(k+q)^\mu-\delta^{\mu\nu}k\cdot(k+q)]$ (Euclidean, massless) | Dirac-trace numerator | `qed_vacuum_polarization.py:L113 b0_gate_symbolic.fermion_M()` | exact (inventory #275) |
| 2 | $1/(k+q)^2\to1/K-(2k\cdot q+q^2)/K^2+(2k\cdot q)^2/K^3$; 4-D angular averages $\langle k^ak^b\rangle=K\delta^{ab}/4$, $\langle k^4\rangle=K^2(\delta\delta+\delta\delta+\delta\delta)/24$; keep degree $-4$ | UV log extraction | `L117–154 log_coeff()` | unknown (inferred: exact) |
| 3 | scalar bubble coefficient $g=1$ (calibrates $1/16\pi^2$) | normalisation | `L156` | unknown (inferred: exact) |
| 4 | $g^{\mu\nu}=C_f(q^2\delta^{\mu\nu}-q^\mu q^\nu)$, $C_f=4/3$; $b_0^\text{QED}=C_f$ | transversality + $b_0=4/3$ (textbook: $\mu\,d\alpha/d\mu=2\alpha^2/3\pi$) | `L163–168` | exact (inventory #275) |
| 5 | $\{\gamma^a,\gamma^b\}=2\eta^{ab}$; $\mathrm{Tr}[\gamma^\mu\slashed k\gamma^\nu(\slashed k+\slashed q)]=4[k^\mu(k+q)^\nu+(k+q)^\mu k^\nu-\eta^{\mu\nu}k\cdot(k+q)]$ (Minkowski) | explicit-γ trace check | `L204–230 gamma_trace_check()` | unknown (inferred: exact) |
| 6 | $q_\mu(q^2\delta^{\mu\nu}-q^\mu q^\nu)=0$ | "Ward identity" | `L251–253 ward_identity_symbolic()` | unknown (inferred: exact (tautology)) |
| 7 | $K_\text{lat}=3\,\Omega_\text{even}^2+k_t^2$ | rule photon kernel | `L267 _omega_even()`, `L272 _K_lat()` | unknown (inferred: exact (closed form)) |
| 8 | $B=[\langle N^{00}/\text{den}\rangle-\langle N^{11}/\text{den}\rangle]/Q^2$, den $=k^2(k+q)^2$ or $K_\text{lat}(k)K_\text{lat}(k+q)$, $q=(Q,0,0,0)$, no refold | transverse coefficient on $n^4$ grid over $[-\pi,\pi)^4$ | `L278–300 _fermion_B()` | unknown (inferred: quantitative) |
| 9 | $\Delta=B_\text{rule}-B_\text{cont}$ flat in $Q\in\{0.1,..,0.3\}$ (spread $<5\times10^{-2}$) | lattice $b_0$ = continuum $b_0$ | `L308–316 lattice_b0_consistency()` | quantitative (inventory #275: "convergent") |
| 10 | $\mathrm{Re}\,\Delta\alpha_\ell(s)=\tfrac\alpha{3\pi}[\ln(s/m_\ell^2)-\tfrac53]$ (textbook, $s\gg m^2$) | per-lepton VP | `L333 _dalpha_lepton()` | unknown (inferred: exact (closed form)) |
| 11 | $\Delta\alpha_\text{lep}=\sum_{e,\mu,\tau}$; $1/\alpha(M_Z)\vert_\ell=\alpha^{-1}(1-\Delta\alpha_\text{lep})$ | leptonic running to $M_Z$ | `L342–344 leptonic_running()` | quantitative (inventory #275: 0.03142 vs 0.03150; spot-check 0.031421, 132.730) |

**Inputs → outputs:** $n$, $Q$ list; α, $M_Z$, lepton masses (literals) → $b_0$, Δ spreads, $\Delta\alpha$. **Depends on:** `lattice.bcc.bcc_dispersion` (03-lattice.md), `c_lat` (imported, unused). **Flags:** (a) ⚠ DOC/CODE MISMATCH — Π1 claims "$q_\mu\Pi^{\mu\nu}=0$ over the whole BZ"; row 6 contracts $q$ with the *assumed* transverse tensor (tautology), and the real transversality check (row 4) is on the continuum UV-log piece only, not on the lattice Π. (b) ⚠ DOC/CODE MISMATCH (minor) — the `_dalpha_lepton` docstring writes $d(1/\alpha)/d\ln s=-1/3\pi=-(b_0/4)(\alpha/\pi)$; the second equality is off by a factor α ($-(b_0/4)(\alpha/\pi)=-\alpha/3\pi$). (c) `fermion_loop_sign=-1` is reported but not applied; $b_0$ is the magnitude of $C_f$. (d) Row 10 is a quoted continuum formula; the "running α" is not computed from the lattice bubble. (e) Row 8 has a lattice photon on both lines but the numerator stays continuum; the absolute BZ measure is open (S12/F272 §4).

### `engine/interactions/qed_vertex_loop.py` — one-loop vertex: WT identity, $a_e=\alpha/2\pi$, Uehling, Lamb shift (F252)
**Status:** live · test-only · **Findings:** (registry none; docstring F252, F251, F257, F125) · **Lattice:** n/a (continuum symbolic + closed-form bound-state QED) · **Law:** n/a · **Units:** natural; MHz / eV for the Lamb shift

**Does:** tree-level WT identity with explicit γ, the Schwinger term from the Feynman-parameter integral, the Uehling moment, and the leading-order Lamb shift.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\slashed q=(\slashed p'-m)-(\slashed p-m)$, $q=p'-p$; Clifford check | WT identity at tree level ($\Lambda^\mu=\gamma^\mu$) | `qed_vertex_loop.py:L115–118 wt_identity_symbolic()` | exact (inventory #276) |
| 2 | $\int_0^1(1-z)\frac{2z(1-z)}{(1-z)^2}dz=\int_0^12z\,dz=1$ ⇒ $F_2(0)=\alpha/2\pi$ (textbook Schwinger) | anomalous moment | `L142–145 ae_schwinger_symbolic()` | exact (inventory #276; spot-check integral $=1$) |
| 3 | $\int_0^1x^2(1-x)^2dx=\tfrac1{30}$; $\Pi$ low-$q$ coefficient $2\times\tfrac1{30}=\tfrac1{15}$ (×α/π); S-state coefficient $-\tfrac4{15}$ (typed) | Uehling | `L176–178 uehling_coefficient_symbolic()` | exact (inventory #276) |
| 4 | $E_1=\alpha(Z\alpha)^4m_ec^2/(\pi n^3)$, $n=2$, $Z=1$ | Lamb energy unit | `L218–219 lamb_shift()` | unknown (inferred: exact (formula)) |
| 5 | $F_{2s}=\tfrac43\ln(Z\alpha)^{-2}-\tfrac43\ln k_0(2s)+\tfrac{10}9$; $F_{2p_{1/2}}=-\tfrac43\ln k_0(2p)-\tfrac16$ (textbook $A_{40}$) | self-energy level functions | `L223–225` | unknown (inferred: exact (formula)) |
| 6 | $\Delta E_{VP}(2s)=-\tfrac4{15}E_1$ | Uehling shift (spot-check $-27.13$ MHz) | `L228–229` | unknown (inferred: exact (formula)) |
| 7 | Lamb $=(F_{2s}-F_{2p}-\tfrac4{15})E_1$; $\ln k_0(2s)=2.811769893$, $\ln k_0(2p)=-0.030016709$ (literature default) | leading-order Lamb shift | `L231` | quantitative (inventory #276: 1052.2 MHz, 99.5%) |
| 8 | Dirac–Coulomb $E(2s_{1/2})-E(2p_{1/2})$ via `atom.sommerfeld_binding_eV` ($\kappa=\mp1$) | degeneracy baseline (spot-check 0.0) | `L195–197 _dirac_degeneracy_eV()` | exact (inventory #161) |
| 9 | same with $\ln k_0$ from `qed_bethe_log.bethe_log(N=12000)` | model-Bethe Lamb shift | `L261–263 lamb_shift_model_bethe()` | quantitative (inventory #277) |

**Inputs → outputs:** α, $m_e$, $h$ (literals), Bethe logs → $a_e$, Lamb MHz. **Depends on:** `particles.atom` (06a/06b § atom.py), `qed_bethe_log` (above). **Flags:** (a) ⚠ DOC/CODE MISMATCH — inventory #276 and the docstring describe a *one-loop* vertex WT identity fixing $Z_1=Z_2$; the code checks only the tree identity $\slashed q=S^{-1}(p')-S^{-1}(p)$. (b) ⚠ DOC/CODE MISMATCH — the Uehling $-4/15$ is "DERIVED" per docstring/inventory, but row 3 types `-Rational(4,15)`; only the moment $1/30$ is computed. The docstring also writes the low-$q$ limit as $+(2\alpha/\pi)(q^2/m^2)/30$ after a first line with an overall minus (sign inconsistency; textbook $\Pi_2(q^2)\to-\tfrac{\alpha}{15\pi}q^2/m^2$). (c) Row 2's integrand is the Peskin–Schroeder 6.56 parametric form typed in, not obtained from a loop computation; the lattice photon does not enter. (d) α, $m_e$, $h$, Bethe logs, measured values are unregistered literals.

