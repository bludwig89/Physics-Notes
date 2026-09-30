# Interactions I — cosmology, black holes, dark matter

*Model map, part p07a. Written 2026-09-28 - 00:00 from the code at HEAD (working tree). The code is the source of truth; every row cites the line where the quantity is computed.*

**Scope.** The strong-field / cosmological end of `src/casim/engine/interactions/`: the F183 black hole (the canonical Schwarzschild/Kerr object that replaced the F114 dielectric black hole), the FLRW background under the F178 full-tensor source, the primordial-sector no-go chain (F282 → F283/F284 → F285 → F286/F295/F296 → F310 → F362), linear growth and the transfer function (F288, F369), BBN (F297/F361/F372), the cosmological-constant chain (F332 → F367 → F368 → F408), horizon thermodynamics (F360), the geon dark-matter abundance checks (F365, F366), and the S8 dark-matter toy (F191).

**Conventions shared by the batch.**
- **None of these modules evolves a lattice.** No module here runs a BCC or cubic propagator; the even/chiral rotation law (F91) is therefore `n/a` everywhere, except that `lambda_dynamics`, `lambda_sequestering` and `lambda_sign_split` integrate the **single-branch BCC Weyl dispersion** $\omega^+(\mathbf k)=\arccos u^+(\mathbf k)$ (`lattice/bcc.py:bcc_dispersion`, sign `'+'`) over the BZ through `qed_uv_completion.sakharov_moments` (see 07c-interactions-qed.md § qed_uv_completion.py, and 03-lattice.md § bcc.py). Where the BCC cell enters, it enters as the length $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P$ (`a_over_ellP`, exact, F79/F107).
- **Units.** Three unit systems appear and are never mixed inside one function: (i) geometric $G=c=1$, lengths in $M$ (`blackhole` Schwarzschild/Kerr sector); (ii) "natural" FLRW units $8\pi G/3=1$, $c=1$ (`cosmology.py` barotropic sector) or $H_0=1$ with $\Omega$'s (`cosmology.py` ΛCDM, `growth`); (iii) SI, entered through the registry constants `c_SI`, `hbar_SI`, `ell_P_m`, `G_CODATA` (external, CODATA) times $a/\ell_P$. **SI conversion enters** only where a physical number is quoted: `blackhole.hawking_temperature_SI / hawking_lifetime_years / lattice_core_radius`, `cosmology_bbn` (MeV, s, cm), `cosmology_growth.discreteness_bound`, `cosmology_initial_conditions.required_non_genericity`, `cosmology_critical_measure.tensor_prediction`, `cosmology_lattice_elasticity.earliest_resolvable_epoch / lattice_cell_budget`, `cosmology_lambda_dynamics`, `cosmology_lambda_sign_split`. The route from the lattice to SI is always $a = (a/\ell_P)\,\ell_P$ with $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ exact (F79/F107); `lattice/si_scale.canonical_cell()` is used only by `cosmology_bbn.model_G()`.
- **Gravity law.** Every module uses the **induced Einstein equation** (decision 4 / F178). The energy-only law $\nabla^2\ln K=-8\pi G T^{00}/c^4$ (F106) appears only as (a) its static weak-field reduction (`growth` S2, `lambda_dynamics` K2) or (b) a declared *control* that must fail (`cosmology.accel_over_a(source="energy")`, `cosmology_bbn.expansion_normalisation("energy")`).
- **Signature / signs.** Where a trace appears (`lambda_sequestering`, `lambda_sign_split` S5) the dust trace is $T=-\rho$ (mostly-plus). The dielectric is $K=e^{2\Phi}$ with $\Phi=+GM/rc^2>0$ (decision 4 sign), $A=1/K$, $B=K$.
- **External data** (Planck 2018, BK18, RSD, LLR, BBN rates, …) are literal module constants, not registry constants; they are listed under *Inputs* and never tagged as model results.
- **Exactness.** Default = module-registry `exactness`; overridden where `docs/status/exactness-inventory.md` names the specific row; numerical integrations with a tolerance are tagged `quantitative` even in `exact` modules (flagged).
- **Numerics façade (D8).** `blackhole`, `cosmology`, `darkmatter` import `numpy` directly (pre-C9 manifest modules); the rest use `casim.numerics.xp`/`fft`, `math`, or `sympy`. No chiral (complex) transform is performed in this batch; the one FFT (`lambda_dynamics.homogeneous_source_blind`) acts on a real field and keeps `.real` of an exactly real inverse (safe).

**Modules covered (22):** `__init__.py`, `blackhole.py`, `cosmology.py`, `cosmology_anomalous_dimension.py`, `cosmology_bbn.py`, `cosmology_blockspin_fluctuation.py`, `cosmology_critical_measure.py`, `cosmology_geon_domain_wall_reopening.py`, `cosmology_geon_relic_gw_bounds.py`, `cosmology_growth.py`, `cosmology_holographic.py`, `cosmology_horizon_thermodynamics.py`, `cosmology_initial_conditions.py`, `cosmology_lambda_dynamics.py`, `cosmology_lambda_sequestering.py`, `cosmology_lambda_sequestering_consistency.py`, `cosmology_lambda_sign_split.py`, `cosmology_lattice_elasticity.py`, `cosmology_primordial.py`, `cosmology_second_scale.py`, `cosmology_transfer_function.py`, `darkmatter.py`.

---

### `engine/interactions/__init__.py` — package marker
Plumbing: docstring + `from __future__ import annotations`; no exports, no physics.

---

### `engine/interactions/blackhole.py` — the black hole under F178 (Schwarzschild/Kerr + lattice core)
**Status:** live · test-only · **Findings:** (registry: none) — code cites F183, F178, F107, F114 · **Lattice:** n/a (BCC cell $a$ enters only as a length) · **Law:** n/a · **Units:** geometric $G=c=1$ (lengths in $M$) for `schwarzschild/kerr/…`; SI for `hawking_*`, `schwarzschild_radius_km`, `lattice_core_radius`

**Does:** closed-form strong-field observables of the canonical (F178/F183) vacuum solution — Schwarzschild and Kerr with a real horizon — plus Oppenheimer–Snyder collapse and the one non-GR item, a lattice-scale curvature cap; `f114_dielectric_contrast()` keeps the **SUPERSEDED F114** dielectric-hole numbers as an exclusion record.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $r_h=2M,\ r_\text{ph}=3M,\ b_c=3\sqrt3\,M,\ r_\text{ISCO}=6M,\ \kappa=1/4M,\ T_H=\kappa/2\pi$ | Schwarzschild scales | `blackhole.py:L67-L72 schwarzschild()` | exact (inventory row 219, F183) |
| 2 | $\Omega_c=\sqrt{M/r_\text{ph}^3}=1/(3\sqrt3 M)=\lambda_\text{Lyap}$; $\omega\approx\Omega_c\,\ell-\tfrac{i}{2}\lambda$ ($n=0$) | eikonal QNM tied to photon sphere | `blackhole.py:L75-L84 schwarzschild()` | unknown (inferred: exact (row 219)) |
| 3 | $T_H=\hbar c^3/(8\pi G M k_B)$ | Hawking temperature, SI | `blackhole.py:L92 hawking_temperature_SI()` | unknown (inferred: exact formula; SI inputs external) |
| 4 | $t_\text{evap}=5120\pi G^2M^3/(\hbar c^4)$ | photon-only evaporation lifetime | `blackhole.py:L98 hawking_lifetime_years()` | unknown (inferred: exact formula) |
| 5 | $r_s=2GM/c^2$ | Schwarzschild radius, km | `blackhole.py:L103 schwarzschild_radius_km()` | unknown (inferred: exact) |
| 6 | $V(r)=(1-2M/r)/r^2,\ b_c=1/\sqrt{V_\max}$ (grid $2.01M$–$12M$, 400 001 pts) | numeric photon-sphere check | `blackhole.py:L111, L121 numeric_shadow()` | unknown (inferred: quantitative (<1e-3, row 219)) |
| 7 | $r_\pm=M\pm\sqrt{M^2-a^2},\ r_\text{ergo,eq}=2M,\ \Omega_H=a/(r_+^2+a^2)$ | Kerr horizons, frame dragging | `blackhole.py:L136-L139 kerr()` | unknown (inferred: exact) |
| 8 | $Z_1=1+(1-a_*^2)^{1/3}[(1+a_*)^{1/3}+(1-a_*)^{1/3}],\ Z_2=\sqrt{3a_*^2+Z_1^2},\ r_\text{ISCO}^{\mp}=M[3+Z_2\mp\sqrt{(3-Z_1)(3+Z_1+2Z_2)}]$ | Bardeen–Press–Teukolsky ISCO (pro/retro) | `blackhole.py:L142-L145 kerr()` | unknown (inferred: exact) |
| 9 | $\xi=-\dfrac{r^3-3Mr^2+a^2r+a^2M}{a(r-M)},\ \eta=\dfrac{r^3[4a^2M-r(r-3M)^2]}{a^2(r-M)^2},\ \alpha=-\xi/\sin\theta_o,\ \beta^2=\eta+a^2\cos^2\theta_o-\xi^2\cot^2\theta_o$ | Bardeen shadow outline (sampled in $r$) | `blackhole.py:L168-L172 kerr_shadow_outline()` | unknown (inferred: exact curve; widths sampled (quantitative)) |
| 10 | $R(\eta)=\tfrac{R_0}{2}(1+\cos\eta),\ \tau(\eta)=\sqrt{R_0^3/8M}\,(\eta+\sin\eta),\ \tau_\text{sing}=\pi\sqrt{R_0^3/8M}$ | Oppenheimer–Snyder dust collapse | `blackhole.py:L209-L211 oppenheimer_snyder()` | unknown (inferred: exact; $\tau_\text{horizon}$ = nearest grid point (quantitative)) |
| 11 | $\mathcal K=48M^2/r^6$ | Kretschmann scalar | `blackhole.py:L235 kretschmann_schwarzschild()` | unknown (inferred: exact) |
| 12 | $r_\text{core}=\big(48\,(GM/c^2)^2\,a^4\big)^{1/6}$, $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ | radius where $\mathcal K=1/a^4$ — lattice-regulated core (non-GR postulate) | `blackhole.py:L248 lattice_core_radius()` | unknown (inferred: exact algebra; the cap $\mathcal K_\max=a^{-4}$ is a posited criterion) |
| 13 | F114: $r_\text{ph}=2\sqrt e\,M,\ b_c=2eM,\ b_c/b_c^\text{GR}-1=2e/(3\sqrt3)-1=+4.63\%$ | **SUPERSEDED by F178/F183** — exclusion record only | `blackhole.py:L268-L270 f114_dielectric_contrast()` | unknown (inferred: exact (of the dead premise)) |

**Inputs → outputs:** $M$ (geometric) or $M/M_\odot$ (SI), spin $a$, inclination, $R_0$ → dicts of radii, frequencies, temperatures, shadow curves. Constants: `G_CODATA`, `c_SI`, `hbar_SI`, `ell_P_m` (external), `a_over_ellP` $=\sqrt{8\pi}\,3^{1/4}$ (exact, F79/F107); literals $k_B$, $M_\odot=1.98892\times10^{30}$ kg, year. **Depends on:** `casim.constants` only (see 01-constants.md). **Flags:** `f114_dielectric_contrast` is **SUPERSEDED by F178** (S4-F178-full-stress-energy; F114 partially superseded, successor F183); unregistered module findings (registry `findings` empty although docstring is F183); registry exactness `None`; direct `import numpy` (D8, pre-C9 manifest module); literals $k_B$, $M_\odot$ not from the registry; the core radius (row 12) rests on the unproved criterion "$\mathcal K$ caps at $a^{-4}$".

---

### `engine/interactions/cosmology.py` — FLRW under the full-tensor source (F182/F188)
**Status:** live · test-only · **Findings:** (registry: none) — code cites F178, F182; S5 ΛCDM background · **Lattice:** n/a · **Law:** n/a · **Units:** barotropic sector $K_{83}\equiv8\pi G/3=1$, $c=1$; ΛCDM sector $H_0$ units with Gyr conversion

**Does:** Friedmann pair for a barotropic fluid (with the demoted energy-only law as a control), RK4 integration of $a(t)$, and a flat 3-component ΛCDM background (equality, acceleration onset, age).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\rho=\rho_0(a/a_0)^{-3(1+w)}$ | continuity, constant $w$ | `cosmology.py:L49 rho_of_a()` | unknown (inferred: exact) |
| 2 | $H=\sqrt{K_{83}\,\rho(a)}$ | Friedmann I | `cosmology.py:L54 hubble()` | unknown (inferred: exact) |
| 3 | $\ddot a/a=-\tfrac{K_{83}}{2}(\rho+3p/c^2)$ (full); $-\tfrac{K_{83}}{2}\rho$ (energy-only control) | acceleration equation, F178 vs demoted F106 | `cosmology.py:L64, L66 accel_over_a()` | exact (inventory row 218, F182) |
| 4 | $q=\tfrac12(1+3w)$ (full); $q=\tfrac12$ (energy) | deceleration parameter | `cosmology.py:L75, L77 deceleration_parameter()` | unknown (inferred: exact) |
| 5 | $3w/(1+3w)$ | fraction of GR source the energy-only law drops (radiation ½) | `cosmology.py:L84 omitted_source_fraction()` | unknown (inferred: exact) |
| 6 | RK4 on $\dot a=aH(a)$; power-law fit $a\propto t^n$ on the late half | recovers $n=1/2$ (rad.), $2/3$ (dust) | `cosmology.py:L100-L107 integrate_scale_factor()`, `L115 fit_power_law_exponent()` | unknown (inferred: quantitative) |
| 7 | $E(a)^2=\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_\Lambda$ | flat ΛCDM Hubble rate | `cosmology.py:L135 E_of_a()` | unknown (inferred: exact) |
| 8 | $\ddot a/a=-\tfrac{H_0^2}{2}[2\Omega_r a^{-4}+\Omega_m a^{-3}-2\Omega_\Lambda]$ | $\rho+3p$ per component | `cosmology.py:L141 accel_over_a_lcdm()` | unknown (inferred: exact) |
| 9 | $1+z_\text{eq}=\Omega_m/\Omega_r$; $a_\text{acc}=(\Omega_m/2\Omega_\Lambda)^{1/3}$ | equality and acceleration onset (radiation neglected in the latter) | `cosmology.py:L146, L151 z_matter_radiation_equality(), z_acceleration_onset()` | unknown (inferred: exact) |
| 10 | $t_0=H_0^{-1}\int_0^1 da/(aE)$ (trapezoid, $2\times10^6$ pts) | age | `cosmology.py:L158-L160 age_of_universe_gyr()` | unknown (inferred: quantitative) |

**Inputs → outputs:** $w$, $a$, $t_\text{end}$; Planck-2018 defaults $H_0=67.4$, $\Omega_{r0}=9.182\times10^{-5}$, $\Omega_{m0}=0.3153$, $\Omega_\Lambda=1-\Omega_r-\Omega_m$ (external; re-imported by `lambda_sequestering*` and `lambda_sign_split`). **Depends on:** nothing but numpy. **Flags:** registry findings empty, exactness `None`; direct `import numpy` (D8); `np.trapz` (removed in NumPy ≥ 2.0 — will break `age_of_universe_gyr` on a modern NumPy; `cosmology_bbn` already uses `xp.trapezoid`).

---

### `engine/interactions/cosmology_anomalous_dimension.py` — the tilt is an anomalous dimension (F295)
**Status:** live · standalone · **Findings:** F295 · **Lattice:** n/a · **Law:** n/a · **Units:** dimensionless; GeV/eV literals for the inverse problems

**Does:** shows a constant tilt function is a scale-free anomalous dimension with exactly zero running, then solves the inverse problem for $\alpha$ and $G$ as the loop coupling and compares the required $g_\text{eff}$ with the registered $2/9$ weights.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Delta^2=Ak^{-2\gamma}\Rightarrow k\,\partial_k\ln\Delta^2=-2\gamma,\ dn_s/d\ln k=0$ | constant-$\gamma$ branch (sympy) | `cosmology_anomalous_dimension.py:L133-L136 anomalous_dimension_branch()` | exact (literal 0, inventory F295 A1a) |
| 2 | $\gamma=(1-n_s)/2$ | required anomalous dimension | `…:L144 anomalous_dimension_branch()` | exact (reg) (row read: computed from Planck $n_s$) |
| 3 | $dn_s/d\ln k\big\rvert_\text{log}=-(1-n_s)/L,\ L=58.2596\ln10$ | F286 log-class prediction vs constant-$\gamma$ 0 | `…:L155-L156 subclass_discriminator()` | exact (reg) (row read: computed) |
| 4 | $g_\text{eff}=2\pi(1-n_s)\pm2\pi\sigma_{n_s}$ | one-loop coupling the data demand | `…:L175 _g_eff()` | exact (reg) (row read: computed) |
| 5 | $\ln(\mu/m_e)=\dfrac{\alpha^{-1}-g_\text{eff}^{-1}}{(2/3\pi)N_\ell}$, $N_\ell=3$; cutoff $\Lambda_\text{UV}=M_\text{Pl}\,3^{-1/4}$ | one-loop QED running to reach $g_\text{eff}$ vs lattice cutoff | `…:L181-L184 alpha_inverse_problem()` | exact (reg) (row read: computed) |
| 6 | $g_\text{grav}=(k_*/M_\text{Pl,red})^2$ | gravitational coupling at the pivot ($p=2$) | `…:L202 gravity_inverse_problem()` | exact (reg) (row read: computed) |
| 7 | $(2/9-g_\text{eff})/\sigma_g=0.064$ | distance of $2/9$ from the target | `…:L226 representation_weight_target()` | exact (reg) (row read: computed (spot-check 0.0638)) |

**Inputs → outputs:** Planck $n_s=0.9649\pm0.0042$, running $-0.0045\pm0.0067$, $\alpha$, $m_e$, $M_\text{Pl}$ (literals) → dict; `NS_OBS` is re-imported live by `cosmology_growth`. Constants: `delta_star_f`$=2/9$ (exact, F175/F253), `sin2_thetaW_onshell`$=2/9$ (exact, F138); `c_lat` imported but unused. **Depends on:** `casim.constants`. **Flags:** row 7 compares against a bare literal `2.0/9.0` (L222) rather than the registry symbols it then checks equal — harmless but a D7 near-miss; $\Lambda_\text{UV}$ uses the non-reduced $M_\text{Pl}=1.22\times10^{19}$ GeV while F282 defines $\Lambda_\text{UV}=\sqrt{c_\text{lat}}\,M_\text{Pl}$ in reduced units (OTHER, convention); registry `exact` but rows 2–7 are computed from external data.

---

### `engine/interactions/cosmology_bbn.py` — Big-Bang nucleosynthesis on the model's expansion law (F297, F361, F372)
**Status:** live · standalone · **Findings:** F297 (code also F361, F372) · **Lattice:** n/a · **Law:** n/a · **Units:** MeV, s, cm, g; $G$ in SI

**Does:** thermal history → weak $n\leftrightarrow p$ freeze-out → 8-species/12-reaction implicit network, run on the model's structural $G$ and the F178 source law; uses it to (i) validate the network, (ii) exclude the energy-only law, (iii) confront the model's $m_n-m_p=1.51$ MeV.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $N_\text{eff}=3+0.044$ | three light LH neutrinos; $\nu_R$ decoupled (F47/F165/F279) | `cosmology_bbn.py:L203 n_eff_model()` | quantitative (reg) (row read: exact count + external 0.044) |
| 2 | $S(\text{law})=\sqrt{\kappa/2}$, $\kappa=2$ (full), $1$ (energy-only) | $H$ normalisation from power-matching $\ddot a/a=-\tfrac{4\pi G}{3}\kappa\rho$ with continuity | `…:L250-L251 expansion_normalisation()` | exact ($S=1/\sqrt2$; inventory F297 row 46) |
| 3 | $\rho_{e^\pm},p_{e^\pm}=\frac{4}{2\pi^2}\int_0^{60}u^2E\,f\,du,\ \frac{4}{6\pi^2}\int u^4/E\,f\,du$, $E=\sqrt{u^2+x^2}$, $x=m_e/T$ | massive FD $e^\pm$ (4 dof, $\mu=0$), units $T^4$ | `…:L263-L264 _fermi_integrals()` | quantitative (reg) |
| 4 | $s_\text{EM}=(\rho_\gamma+p_\gamma+\rho_e+p_e)T^3,\ a=(s_0/s)^{1/3},\ T_\nu=T_0a_0/a$ | entropy conservation → $T_\nu/T_\gamma\to(4/11)^{1/3}$ emerges | `…:L287-L290 thermal_history()`; check `L1118 _tnu_ratio_error()` | quantitative (reg) |
| 5 | $\rho=(\pi^2/15+\rho_e)T^4+N_\text{eff}\tfrac78\tfrac{\pi^2}{15}T_\nu^4$ | total radiation density | `…:L302-L303 _energy_density()` | quantitative (reg) |
| 6 | $H=S\sqrt{8\pi\rho/3}/E_\text{Pl}\cdot\hbar^{-1}$, $E_\text{Pl}=\sqrt{\hbar c^5/G}$ | Hubble rate in s⁻¹ | `…:L314-L316 hubble_rate()` | quantitative (reg) (row read: exact formula) |
| 7 | $G_\text{model}=a^2c^3/(8\pi\sqrt3\hbar)$ via `si_scale.canonical_cell()["G_pred"]` | structural $G$ (F79/F107) | `…:L322 model_G()` | quantitative (reg) (row read: exact closed form (3e-8 of CODATA)) |
| 8 | $A=\int_{\max(1,q)}^{60}\epsilon\sqrt{\epsilon^2-1}(\epsilon-q)^2f_\nu(\epsilon-q)[1-f_e]$, $B=\int_1^{60}\epsilon\sqrt{\epsilon^2-1}(\epsilon+q)^2f_e[1-f_\nu(\epsilon+q)]$, $C=\int_1^q\epsilon\sqrt{\epsilon^2-1}(q-\epsilon)^2[1-f_e][1-f_\nu]$ (+ primed reverses) | six Born-level $n\leftrightarrow p$ phase-space integrals, $q=\Delta m/m_e$, $e$ at $T_\gamma$, $\nu$ at $T_\nu$ | `…:L355-L373 _rate_integrals()` | quantitative (reg) (row read: quantitative; detailed balance emerges to <1e-3 (K2-4, `L464`)) |
| 9 | $f(q)=\int_1^q\epsilon\sqrt{\epsilon^2-1}(q-\epsilon)^2d\epsilon$; $\tau_n=1/(K_\text{cal}f(q))$, $K_\text{cal}=1/(\tau_n^\text{meas}f(q_\text{PDG}))$; or $1/\tau=G_F^2V_{ud}^2(1+3g_A^2)m_e^5f/2\pi^3$ | neutron lifetime at a given $\Delta m$ | `…:L379, L403-L407 decay_phase_space(), neutron_lifetime()` | quantitative (reg) |
| 10 | $\lambda_{np}=K_\text{cal}(A+B+C),\ \lambda_{pn}=K_\text{cal}(A'+B'+C')$ | weak rates, calibrated on measured $\tau_n$ | `…:L425-L426 weak_rates()` | quantitative (reg) |
| 11 | $X_{n,0}=[1+e^{\Delta m/T_0}]^{-1}$; $X_{i+1}=\dfrac{X_i+\Delta t\,\lambda_{pn}}{1+\Delta t(\lambda_{np}+\lambda_{pn})}$, $\Delta t=\Delta\ln a/\bar H$ | backward-Euler freeze-out | `…:L455-L461 np_freezeout()` | quantitative (reg) |
| 12 | $T_\text{fo}$: $\lambda_{np}+\lambda_{pn}=H$ (linear interp.) | freeze-out temperature | `…:L477-L481 _freezeout_temperature()` | quantitative (reg) |
| 13 | $N_A\langle\sigma v\rangle$ fits (Smith–Kawano–Malaney 1993 / NUC123), with narrowed $t_{9x}=t_9/(1+c\,t_9)$ for the five A=7 rates (F361) | external nuclear rates | `…:L517-L594 _rate_fits()` | external data |
| 14 | $\lambda_\text{rev}=\lambda_\text{fwd}\,c_\text{rev}\,T_9^{p}\,e^{-11.6045\,Q/T_9}$, $Q=\sum B_\text{prod}-\sum B_\text{reac}$ | detailed-balance reverse rates; model $B_d$ enters via $Q$ | `…:L620, L710-L715 _q_value(), _network_step()` | quantitative (reg) (row read: exact relation, external $c_\text{rev}$) |
| 15 | $(\mathbb 1+\Delta t\,M)\,Y_{i+1}=Y_i$, $Y$ clipped to $[0,1]$ | linearised implicit network step (Wagoner/Kawano) | `…:L751-L753 _network_step()` | quantitative (reg) |
| 16 | $n_\gamma=2\zeta(3)T^3/\pi^2$, $n_b=\eta\,n_\gamma(a_\text{end}/a)^3$; $Y_p=4Y_{^4\!He}$, D/H, $^3$He/H, $(^7\text{Li}+{}^7\text{Be})$/H | outputs | `…:L648-L650, L671-L676 _run_bbn_inner()` | quantitative ($Y_p=0.2449$, $-0.11\sigma$; D/H $-1.8\sigma$; Li $-6.3\%$; inventory rows 44, 45, 48a) |
| 17 | $\partial Y_p/\partial\Delta m$ by central difference ($\pm0.02$ MeV); $\sigma_{\Delta m}=\sigma_{Y_p}/\lvert\partial Y_p/\partial\Delta m\rvert$ | BBN as a measurement of $m_n-m_p$ | `…:L865, L879 delta_m_confrontation()` | quantitative (reg) |
| 18 | shortfall $=1.2933-(2.51-1.00)=-0.217$ MeV | which F122 term is off | `…:L901 f122_decomposition()` | quantitative (reg) (row read: computed) |
| 19 | $(1.51-1.2933)/\sigma_\text{th}$, $\sigma_\text{th}=\sqrt{0.16^2+0.23^2}=0.280$ MeV (BMW 2015) | theory-aware significance (F372) | `…:L955-L970 delta_m_theory_uncertainty()` | quantitative (reg) (row read: computed) |
| 20 | $\Delta(\text{D/H})$ at $B_d$ model vs PDG; per +1 % | $B_d$ sensitivity (declared null) | `…:L997-L1009 bd_sensitivity()` | quantitative (reg) |
| 21 | $\dot G/G\equiv0$; $\Delta Y_p$ per 1 % in $G$ | consistency, not a bound | `…:L1042-L1046 gdot_over_g_prediction()` | quantitative (reg) (row read: exact (structural 0) / quantitative) |

**Inputs → outputs:** $\Delta m$, law, $\eta_{10}$, $N_\text{eff}$, $G$, $B_d$, $m_e$, `legacy_a7_bug` → abundances and a 15-leg K2 verdict (`check_k2`, `L1121`). External: $\eta_{10}=6.137$, $V_{ud}$, $\tau_n=878.4$ s, $G_F$, reaction rates, nuclear binding energies, $g_A$ (registry, external PDG), `G_CODATA`, `c_SI`, `hbar_SI`. Model-native: structural $G$ (F79/F107), $\kappa=2$ (F178), $\Delta m=1.51$ (F122/F123), $B_d=2.224$ (F104/F113/F126/F240). **Depends on:** `casim.numerics.xp`, `lattice.si_scale` (03-lattice.md), `particles.baryon_dynamics.em_self_energy_pairwise` (06a-particles-derivations-baryons.md). **Flags:** ⚠ DOC/CODE MISMATCH `hubble_rate` (L307-L316): docstring says the Planck mass is built from the model's structural $G$ "by default", but the signature default is `G=G_CODATA`; the structural default is actually supplied one level up by `np_freezeout` (`G=None → model_G()`, L443-L444), so `run_bbn` is correct but a direct `hubble_rate(rho)` call uses CODATA. `bd_sensitivity` mutates the module-global `BINDING_MEV["d"]` (L1000) outside `run_bbn`'s save/restore. Registry lists only F297 though the code also carries F361 and F372 legs. Many unregistered SI/physics literals (MeV/J, $\hbar c$, $m_u$, $\zeta(3)$, $m_e$).

---

### `engine/interactions/cosmology_blockspin_fluctuation.py` — fluctuation corrections to F130's confinement eigenvalue (F362)
**Status:** live · standalone · **Findings:** F362 F310 F295 F296 F285 F130 · **Lattice:** n/a here (reads a Z3 Kogut–Susskind plaquette strip via `gauge.link_hamiltonian` and `lattice.blockspin`) · **Law:** n/a · **Units:** lattice couplings ($g^2$, $\lambda$ dimensionless)

**Does:** composes second-order strong-coupling PT for the string tension with F130's bond-moving rule ($g^2\to bg^2$, $\lambda$ fixed) and shows the resulting "effective" eigenvalue is integer order-by-order, scheme-dependent in $b$, and non-perturbative at the model's own coupling.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\hat\sigma(g^2,\lambda)=\tfrac{g^2}{2}-\tfrac{1}{6g^2}\lambda^2$ ($c_2=\tfrac16/g^2$, `Fraction(1,6)`) | 2nd-order strong-coupling string tension | `cosmology_blockspin_fluctuation.py:L140-L141 sigma_hat_2nd_order()` | exact (reg) |
| 2 | $R=\hat\sigma(bg^2,\lambda)/\hat\sigma(g^2,\lambda)$; $y_\text{eff}=\log_bR$, $\gamma_\text{eff}=y_\text{eff}-1$ (NaN if $R\le0$) | effective RG eigenvalue | `…:L149, L159, L165 confinement_ratio(), fluctuation_eigenvalue(), fluctuation_gamma()` | exact (reg) |
| 3 | term $n$: $a_n\lambda^{2n}g^{2(1-2n)}\to b^{1-2n}$; relative $b^{-2n}$ | power counting: every order is an integer eigenvalue | `…:L175, L184 term_eigenvalue(), relative_term_eigenvalue()` | exact (reg) |
| 4 | $\epsilon=\lambda^2/\big(3\,(g^2)^2\big)$ (code variable `g2` $=g^2$) | expansion parameter; perturbative iff $\epsilon<0.2$ | `…:L195, L201 epsilon_scale(), is_perturbative()` | exact (reg) |
| 5 | $R(\epsilon,b)=\dfrac{b^2-\epsilon}{b(1-\epsilon)}$ ($g^2$ cancels); Newton-solve $\epsilon$ so $\gamma_\text{eff}=\gamma_\text{target}$ at one $b$, evaluate at others | universality scan (C3/C4) | `…:L217, L226-L237 universality_scan()` | exact (reg) |
| 6 | measured $R_c/R_f$ vs $b^{-2}$ at $\lambda\in\{0.005,0.01\}$, tol 2 % | C2: $n=1$ relative eigenvalue vs `blockspin.magnetic_deformation_ratio` | `…:L299-L307 check_c2_power_counting()` | quantitative (asymptotic, residual $O(\lambda)$) (reg: exact; row is weaker — see flags) |
| 7 | $\epsilon(g^2=\tfrac14,\lambda=\Omega^2)$, $\Omega\in\{1.3,0.99783\}$ ⇒ $\epsilon\approx15$ | C5: model point is non-perturbative | `…:L339-L344 check_c5_physical_point()` | exact (reg) |

**Inputs → outputs:** $g^2$, $\lambda$, $b$, $\gamma_\text{target}=0.015$ → four check legs (`run_all`, L348) with declared controls `wrong_sign`, `wrong_power`. **Depends on:** `gauge.link_hamiltonian.PlaquetteGrid / sigma_strong_pt2` (05a–05c gauge map files), `lattice.blockspin.magnetic_deformation_ratio` (03-lattice.md). **Flags:** the docstring (L46-L55) calls C2 "exact power counting", but the code's C2 check is a 2 % small-$\lambda$ numerical comparison (row 6) with a documented $O(\lambda)$ residual — the *exact* statement is only row 3; registry exactness `exact` vs a `quantitative` leg (EXACTNESS). $g_s^2=1/4$ and $\Omega$ values are literals (F115/F325, F101), not registry imports.

---

### `engine/interactions/cosmology_critical_measure.py` — γ is a block-spin eigenvalue (F310)
**Status:** live · standalone · **Findings:** F310 · **Lattice:** n/a (BCC cell enters only as $k_\text{BZ}=\pi/a$) · **Law:** n/a · **Units:** dimensionless; SI for the pivot/BZ ratio

**Does:** identifies the primordial tilt with the scaling dimension of the energy operator of the $t=0$ 3D measure ($\gamma=y-1$), corrects F285's critical-Gaussian² sub-case, shows F130's measured RG spectrum is all-integer (⇒ Harrison–Zel'dovich), and predicts $n_t=2$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Delta_\varepsilon=d-1/\nu$; $n_s=2\Delta_\varepsilon-d\big\rvert_{d=3}=3-2/\nu=3-2y$; $\gamma\equiv\tfrac12(1-n_s)=y-1$ | operator identification (sympy) | `cosmology_critical_measure.py:L207-L213 dimension_relation()` | exact (inventory F310 C1) |
| 2 | $3+(2\Delta_\varepsilon-3)-4=n_s-1$ | Poisson bridge to $\Delta^2_\Phi\propto k^{n_s-1}$ (F285) | `…:L216-L217 dimension_relation()` | exact (reg) |
| 3 | $\nu=1\Rightarrow n_s=1$; $\nu=\tfrac12\Rightarrow n_s=-1$ | limits | `…:L219-L220 dimension_relation()` | exact (reg) |
| 4 | $2\sum_{j\ge0}(2j+1)^{-2}=\pi^2/4$; bracket $=2\times\pi^2/4=\pi^2/2$; $P_\rho=(2\pi/k)(\pi^2/2)=\pi^3/k\Rightarrow n_s=-1$ | critical Gaussian² — corrects F285 D1 row 2 | `…:L248-L256 critical_gaussian_squared()` | exact (reg) |
| 5 | gapped: $P_\rho\to$ const ⇒ $n_s=0$ | the sub-case F285 had right | `…:L280 gapped_measure_is_white_noise()` | exact (reg) |
| 6 | all exponents in $\{0,1,-2,-3,-4,-2,-2\}$ integer | F130 Kadanoff spectrum has no anomalous dimension | `…:L301-L302 rg_spectrum_is_integer()` | exact (reg) |
| 7 | $y=1\Rightarrow n_s=3-2y=1$; exclusion $\lvert1-n_s^\text{obs}\rvert/\sigma$ | model's own RG predicts HZ | `…:L322-L327 model_rg_predicts_harrison_zeldovich()` | exact (reg) |
| 8 | $\gamma=(1-n_s)/2,\ y=1+\gamma,\ \nu=1/(1+\gamma)$ | required eigenvalue per dataset | `…:L346-L353 required_eigenvalue()` | exact (reg) (row read: computed) |
| 9 | $\Delta_T=d\Rightarrow n_t=2\Delta_T-d-1\big\rvert_{d=3}=2$; $\log_{10}r=(n_t-(n_s-1))\log_{10}(k_*/k_\text{BZ})$, $k_\text{BZ}=\pi/a$ | tensor prediction, $r\sim10^{-118}$ | `…:L370, L379 tensor_prediction()` | exact (reg) |
| 10 | $\Delta^2=e^{-2\gamma u}\Rightarrow dn_s/d\ln k=0$ | C7, re-derives F295 A1 | `…:L414-L416 running_is_zero()` | exact (reg) |
| 11 | $\nu=1-\dfrac{32}{3\pi^2N}$, $n_s=3-2/\nu$; $N_\text{req}=\dfrac{32}{3\pi^2(1-\nu)}$ | large-$N$ O(N) target (not a derivation) | `…:L434-L442 large_n_target()` | exact (reg) (row read: computed) |

**Inputs → outputs:** three $n_s$ datasets (Planck 2018, CMB-2025, +DESI DR2), BK18 $r<0.034$, $k_*=0.05$ Mpc⁻¹ → 16 gate assertions (`check_critical_measure`, L526; controls `protected_stress_tensor`, `integer_spectrum_control`). Constants: `a_over_ellP` (exact), `ell_P_m` (external). **Depends on:** `cosmology_holographic.tensor_ratio_from_model_content` (below). **Flags:** row 4 — the integral $\int_0^1\frac{dx}{x}\ln\frac{1+x}{1-x}$ is never evaluated; the code computes the series and sets `upper_half = lower_half` (L250) by the asserted $x\to1/x$ invariance, and nothing checks integral = series. Row 5 is vacuous: `sp.limit(1/(q**2+m**2)**2, k, 0)` (L280) has no $k$ dependence. The tensor-tilt formula $n_t=2\Delta_T-d-1$ is only valid at $d=3$ (scalar uses $2\Delta-d$ with $\Delta^2_\Phi$, tensor $\Delta_t^2$ directly — convention, not an error). `R_BOUND_BK18=0.034` here vs `0.036` in `cosmology_holographic` (OTHER). Row 8/11 labelled "computed" inside a registry-`exact` module.

---

### `engine/interactions/cosmology_geon_domain_wall_reopening.py` — is F238's abundance exclusion scoped? (F366)
**Status:** live · standalone · **Findings:** F366 F238 F228 F282 F285 F150 F175 F234 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a (symbolic)

**Does:** checks that the E_g clock potential has an exact $\mathbb Z_6$ with six degenerate vacua (the Kibble-mechanism precondition for a domain-wall channel of geon production) and greps six framing findings for defect vocabulary.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $V(\delta)=\tfrac A2(1+\cos6\delta)$; minima $\cos6\delta=-1$ on $[0,2\pi)$ ⇒ 6 solutions, equal $V$ | vacuum count / degeneracy (sympy `solveset`) | `cosmology_geon_domain_wall_reopening.py:L140-L153 z6_degeneracy_exact()` | exact (reg) |
| 2 | $V(\delta+\pi/3)-V(\delta)\equiv0$ | exact $\mathbb Z_6$ | `…:L171-L173 z6_symmetry_exact()` | exact (reg) |
| 3 | text search of F238/F228/F282/F283/F284/F285 for {domain wall, topological defect, bubble collision, kibble, cosmic string} | C4 "never examined" (structural, not physics) | `…:L194-L203 scope_of_f238_exclusion()` | n/a (text grep) |
| 4 | reports $A=\lambda_6\,e_\text{sat}^6$ from `cosmology_primordial.eg_clock_coefficient()` | reuses the clock amplitude | `…:L250, L263 run_all()` | exact (reg) (row read: see `cosmology_primordial`) |

**Inputs → outputs:** none → four checks + open-items list. **Depends on:** `cosmology_primordial.eg_clock_coefficient` (below). **Flags:** `A` is declared `positive=False` (L139) — i.e. non-positive — yet $\cos6\delta=-1$ are minima only for $A>0$; the code later substitutes a positive $A$ (L151) and never checks the sign of the reused amplitude, so "minima" vs "maxima" is assumed (OTHER). ⚠ DOC/CODE MISMATCH: docstring says $V$ is "reused verbatim from F282's own `eg_clock_coefficient`", but $V$ is re-typed locally (L140, L171); only the amplitude is read back, and only for display. Leg C4 is a text search whose result depends on finding prose, not on physics.

---

### `engine/interactions/cosmology_geon_relic_gw_bounds.py` — geon relic vs 2025 GW bounds (F365)
**Status:** live · standalone · **Findings:** F365 F228 F238 F223 F216 · **Lattice:** n/a · **Law:** n/a · **Units:** GeV, g, cm⁻³ (external cosmology literals)

**Does:** reproduces F228's required PBH collapse fraction and F238's Press–Schechter $\sigma_\text{req}$, and places them against arXiv:2506.16154 (DLS/PVL SIGW bounds) and arXiv:2509.20533 (LIGO Gaussian-relic exclusion).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M_\text{rem}/M_\text{Pl}=(\sqrt3/2)^{1/2}$ | geon remnant mass (F228) | `cosmology_geon_relic_gw_bounds.py:L78` (module constant) | quantitative (reg) (row read: exact (literal, F228)) |
| 2 | $T_f=\sqrt{\gamma M_\text{Pl}^3/(3.32\sqrt{g_*}M_f)}$, $\gamma=0.2$, $g_*=106.75$ | formation temperature | `…:L83 T_form_GeV()` | quantitative (reg) |
| 3 | $\beta_\text{req}=\Omega_\text{DM}h^2\big/\big[M_\text{rem}\,\tfrac34\tfrac{T_f}{M_f}\,\tfrac{s_0}{\rho_c/h^2}\big]$ | F228 required $\beta$ | `…:L89-L90 beta_required_F228()` | quantitative (reg) |
| 4 | $\beta^{(2.3)}=5.65\times10^{-22}(M_f/\text{g})^{1.5}f$; $\beta_\text{PVL}=1.4\times10^{-4}(M_f/10^9)^{-1/4}$; $\beta_\text{DLS}=1.1\times10^{-6}(M_f/10^4)^{-17/24}$ | external formulas | `…:L100, L104, L108` | external |
| 5 | crossover $\beta^{(2.3)}(M)=\beta_\text{bound}(M)$ by log-bisection | formation-mass ceiling ($\sim1.6\times10^8$ g, DLS) | `…:L110-L129 _bisect_log10_crossover(), M_ceiling_*()` | quantitative (reg) (row read: bracketed (bound itself model-dependent)) |
| 6 | $\beta=\tfrac12\operatorname{erfc}\!\big(\delta_c/\sqrt2\sigma\big)$, $\delta_c=0.45$; $\sigma_\text{req}$ by bisection | Press–Schechter inversion (F238) | `…:L138, L140-L150 beta_of_sigma(), sigma_req()` | quantitative (reg) |
| 7 | $P_\mathcal R=\tfrac{81}{16}\sigma^2$ (general) and $\tfrac94\sigma^2$ (narrow bump) | curvature power for the LIGO band | `…:L156, L167` | bracketed (inventory: F365 S6) |

**Inputs → outputs:** $M_f\in\{10^4,10^6,10^8\}$ g → six records S1–S6 (`run_all`, L178). **Depends on:** nothing in-tree. **Flags:** all constants are local literals (incl. the F228 exact $M_\text{rem}$ ratio and $M_\text{Pl}$), not registry imports; `_records` is a mutable module global cleared on each run (plumbing). S2's constant ratio is structural (both $\propto M^{1.5}$) — the module says so.

---

### `engine/interactions/cosmology_growth.py` — linear structure formation with zero free functions (F288)
**Status:** live · standalone · **Findings:** F288 · **Lattice:** n/a (cell $a$ only in the discreteness bound) · **Law:** n/a · **Units:** $H_0=1$, $x=\ln a$; Mpc / $h^{-1}$Mpc; SI in B1

**Does:** shows the model fixes $\mu=\Sigma=1$ with no $k$ or $t$ dependence (from F106-as-reduction, $AB\equiv1$, $\dot G=0$), derives $\gamma_g=6/11$ and Mészáros exactly, integrates growth, and reports $\sigma_8$/$f\sigma_8$/S8 with $A_s$ declared free.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_r h^2=2.47282\times10^{-5}(T/2.7255)^4\,[1+3.046\cdot\tfrac78(\tfrac4{11})^{4/3}]$ | radiation density | `cosmology_growth.py:L170-L172 _omega_r()` | external |
| 2 | $E^2=\Omega_ra^{-4}+\Omega_ma^{-3}+\Omega_\Lambda$; $\Omega_m(a)=\Omega_ma^{-3}/E^2$; $\frac{d\ln E}{d\ln a}=-\tfrac12(4\Omega_ra^{-4}+3\Omega_ma^{-3})/E^2$ | background | `…:L185, L190, L194` | exact (reg) |
| 3 | $K=e^{2\Phi}$: $\Psi=\tfrac12(K^{-1}-1)$, $\Phi_N=\tfrac12(1-K)$, slip $\Phi_N-\Psi=1-\cosh2\Phi$ (linear coeff. $0$); $\eta-1=2\Phi+O(\Phi^2)$ | S1: $AB\equiv1$ kills linear slip | `…:L216-L226 slip_from_impedance_match()` | exact (literal 0, inventory F288 S1) |
| 4 | $-k^2\,2\Phi/c^2=-(8\pi G/c^4)\rho c^2\Rightarrow\Phi=4\pi G\rho/k^2$; $\mu=1,\ \partial_k\mu=0$ | S2: F106 reduction ⇒ Poisson | `…:L267-L274 mu_from_f106_poisson()` | exact (inventory F288 S2) |
| 5 | $f'+f^2+f(2-\tfrac32\Omega_m)=\tfrac32\mu\Omega_m$, $f=c\,\Omega_m^\gamma$, $\Omega_m=1-\epsilon$: $O(\epsilon^0)$ ⇒ $c=\tfrac{-1+\sqrt{1+24\mu}}{4}$; $O(\epsilon^1)$ at $\mu=c=1$ ⇒ $\gamma_g=6/11$ | D1 growth index | `…:L339-L352 growth_index_exact()` | exact (inventory F288 D1) |
| 6 | $D''+\frac{2+3y}{2y(1+y)}D'-\frac{3D}{2y(1+y)}=0$; $D_+=1+\tfrac32y$, $D_-=(1+\tfrac32y)\ln\frac{\sqrt{1+y}+1}{\sqrt{1+y}-1}-3\sqrt{1+y}$ | D2 Mészáros (residual 0) | `…:L392-L404 meszaros_exact()` | exact (reg) |
| 7 | $\delta''=-(2+\tfrac{d\ln E}{d\ln a})\delta'+\tfrac32\mu\Omega_m(a)\delta$, $\delta=\delta'=a_i=10^{-3}$, RK4, $n=4000$ | growth factor ($D\to a$ in MD) | `…:L437-L459 growth_factor()` | quantitative (reg: exact; row is weaker — see flags) |
| 8 | $g_\text{CPT}=\tfrac52\Omega_m/[\Omega_m^{4/7}-\Omega_\Lambda+(1+\Omega_m/2)(1+\Omega_\Lambda/70)]$; $\gamma_\text{num}=\ln f_0/\ln\Omega_{m0}$ | integrator validation (+0.10 %) | `…:L488-L494 growth_summary()` | quantitative (reg: exact; row is weaker — see flags) |
| 9 | $f\sigma_8(z)=f(a)\,\sigma_8\,D(a)/D_0$; diagonal $\chi^2$ | vs 7 RSD points | `…:L537-L539 fsigma8_curve()` | quantitative ($\chi^2/N=1.012$) (reg: exact; row is weaker — see flags) |
| 10 | Eisenstein–Hu 1998 no-wiggle $T(k)$: $s$, $\alpha_\Gamma$, $\Gamma_\text{eff}$, $q=k\Theta^2/(h\Gamma)$, $T=L_0/(L_0+C_0q^2)$ | imported transfer function | `…:L574-L583 transfer_eh98()` | external fit |
| 11 | $\Delta^2=\tfrac4{25}A_s(k/k_p)^{n_s-1}(ck/H_0)^4\Omega_m^{-2}T^2D_1^2$; $\sigma_R^2=\int\Delta^2W^2d\ln k$ (Simpson), $W=3(\sin x-x\cos x)/x^3$ | $\sigma_R$ from $A_s$ | `…:L588-L631 _window_tophat(), sigma_R()` | quantitative (reg: exact; row is weaker — see flags) |
| 12 | $f_\nu=\Sigma m_\nu/(93.14h^2\Omega_m)$; $\sigma_8\to\sigma_8(1-4f_\nu)$; $S_8=\sigma_8\sqrt{\Omega_m/0.3}$ | massive-ν correction, S8 | `…:L647-L650 sigma8_from_As()` | quantitative ($\sigma_8=0.8204$, +1.15 %) (reg: exact; row is weaker — see flags) |
| 13 | $p(\mu)=\tfrac{-1+\sqrt{1+24\mu}}4$, $p'(1)=3/5$; $\Delta\chi^2=1$ scans (anchored / amplitude-marginalised $\alpha=\sum xy/\sum x^2$) | D5: $\mu$ pinned by growth | `…:L710-L740 mu_bound_from_growth()` | exact (reg) |
| 14 | $(a/L)^2$ at $R_8$, Ly-α (0.3 Mpc), $c/H_0$ | B1 discreteness bound | `…:L793-L794 discreteness_bound()` | bound (inventory F288 B1) |
| 15 | $T_\text{WDM}=[1+(\alpha k)^{2\nu}]^{-5/\nu}$, $\alpha=0.049\,m^{-1.11}(\Omega_m/0.25)^{0.11}(h/0.7)^{1.22}/h$; $k_{1/2}=(2^{\nu/10}-1)^{1/2\nu}/\alpha$ | B2 free streaming (geon vs 5.6 keV sterile) | `…:L816-L819, L832-L834 transfer_wdm(), dark_matter_free_streaming()` | external fit |
| 16 | $(S_8^\text{model}-S_8^\text{obs})/\sqrt{\sigma^2+\sigma_\text{CMB}^2}$ | S8 falsifier | `…:L884-L885 s8_falsifier()` | exact (reg) (row read: computed) |

**Inputs → outputs:** `EXTERNAL` dict (Planck 2018 Ω's, $h$, $T_\text{cmb}$, $A_s$, $\Sigma m_\nu$, S8 landscape, Viel fit), RSD table, $n_s$ from `cosmology_anomalous_dimension.NS_OBS` → `run(mu, A_s)` with a $\mu=0.90$ control. Constants: `a_over_ellP` (exact), `ell_P_m`. **Depends on:** `cosmology_anomalous_dimension` (above), `casim.numerics.xp`. **Flags:** registry `exact` but rows 7–13, 15–16 are numerical/external (EXACTNESS: module class too strong for D3–D5); S1's "$AB$ product" string (L233) is a trivial `(1/K)*K`; geon mass in B2 re-typed as `sqrt(sqrt3/2)*1.22089e19` (L837) rather than imported; `growth_summary` runs growth on a radiation-free background by declared convention (sensitivity 3.8e-5 measured).

---

### `engine/interactions/cosmology_holographic.py` — holographic cosmology as F295's literature home (F296)
**Status:** live · standalone · **Findings:** F296 · **Lattice:** n/a · **Law:** n/a · **Units:** dimensionless

**Does:** evaluates F286 T1's tilt-shape diagnostic on the Afshordi et al. (2017) holographic-cosmology fit (retrodicting its tension) and computes $r$ from the model's field content read as the 3D dual (excluded).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u=g$ (at $q=q_*$), $L=\ln\lvert\beta u\rvert$, $D=1-uL$; $n_s-1=-u(L+1)/D$; $d\ln\lvert n_s-1\rvert/d\ln q=-(L+2)/(L+1)$; running $=(n_s-1)\cdot$ that | HC tilt/running at $g=-0.00703$, $\ln\beta=0.877$ | `cosmology_holographic.py:L129-L140 hc_spectrum_tilt()` | computed (inventory F296 L2a: 0.6754, running +0.01506) |
| 2 | $\lvert d\ln F/d\ln x\rvert/0.32$; $(\alpha_s-\alpha_\text{obs})/\sigma$ | T1 retrodiction (2.11×, 2.92σ) | `…:L147-L159 t1_retrodiction()` | quantitative (reg) (row read: computed) |
| 3 | $r=\dfrac{32\,[1+N_\Phi(1-8\xi)^2]}{1+2N_\psi+N_\Phi}$, $N_\psi=48$, $N_\Phi=2$, $\xi\in\{0,\tfrac18\}$; $N_\Phi^\text{need}=32/r_\text{BK18}-1-2N_\psi$ | tensor ratio from model content (0.970 / 0.323; 792) | `…:L206-L210 tensor_ratio_from_model_content()` | quantitative (reg) (row read: exact arithmetic (spot-checked); external formula) |

**Inputs → outputs:** HC fit parameters, Planck $n_s$/running, BK18 $r<0.036$ → L1–L5 dict (`run`, L229). **Depends on:** nothing in-tree; read by `cosmology_critical_measure`. **Flags:** BK18 bound 0.036 here vs 0.034 in `cosmology_critical_measure` (OTHER); the scalar sum is written `n_phi*(1-8ξ)^2` (all scalars share one $\xi$) — a simplification of the external $\sum_M$ formula; registry `quantitative` consistent.

---

### `engine/interactions/cosmology_horizon_thermodynamics.py` — Friedmann from horizon Clausius relation (F360)
**Status:** live · standalone · **Findings:** F360 F182 F188 F284 F178 F180 F79 F190 F355 · **Lattice:** n/a · **Law:** n/a · **Units:** $c=\hbar=k_B=1$, $G$ a free positive symbol

**Does:** re-derives the Friedmann pair from $dQ=T\,dS$ at the apparent horizon (Cai–Kim) and quantifies the term the quasi-static surface gravity drops.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $r_A=1/H$, $\kappa_\text{qs}=-1/r_A$, $T=-\kappa/2\pi$, $S=\pi r_A^2/G$, $\dot Q=4\pi r_A^3H(\rho+p)$; $\dot Q=T\dot S\Rightarrow\dot H=-4\pi G(\rho+p)$ | Friedmann II (sympy) | `cosmology_horizon_thermodynamics.py:L81-L100 verify_quasistatic()` | exact (reg) |
| 2 | with $\rho+p=-\dot\rho/3H$: $d(H^2)/dt=\tfrac{8\pi G}{3}\dot\rho$ | Friedmann I on integration | `…:L103-L106 verify_quasistatic()` | exact (reg) |
| 3 | $\kappa=-\frac1{r_A}\big(1-\frac{\dot r_A}{2Hr_A}\big)$; residual quadratic in $\dot H$: $c_2\dot H^2+c_1\dot H+c_0$; $\dot H_0=-c_0/c_1$; $\dfrac{c_2\dot H_0^2}{c_1\dot H_0}\Big\rvert_{H^2=8\pi G\rho/3,\ p=w\rho}=-\tfrac34(1+w)$ | size of the dropped quasi-static term (radiation −1, matter −3/4, Λ 0) | `…:L139-L173 quantify_approximation()` | exact (reg) |

**Inputs → outputs:** none → `run_all` (L202). **Depends on:** sympy only. **Flags:** ⚠ DOC/CODE MISMATCH (mild): docstring says the Unruh temperature is set by the model's light cone ($c_\text{lat}=c_\text{grav}$, F26/F180) and the entropy uses the model's induced $G$ (F79); the code imports neither — $c=1$ and $G$ is a free symbol, so the result is the standard continuum Cai–Kim derivation with no model input. $S=A/4G$ and the Hayward–Kodama $\kappa$ are imports (the docstring says so).

---

### `engine/interactions/cosmology_initial_conditions.py` — what $n_s$ can an initial-condition measure give? (F285)
**Status:** live · standalone · **Findings:** F285 · **Lattice:** n/a ($k_\text{BZ}=\pi/a$ only) · **Law:** n/a · **Units:** dimensionless; SI for the pivot/BZ ratio

**Does:** maps candidate $t=0$ measures to $n_s$ via $P_\rho\propto k^{n_s}$, measures the pivot's distance from the BZ edge, and proves block-spin leaves the spectral index marginal.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $P_\rho\propto k^m\Rightarrow n_s=m$; slopes {white 0, short-range 0, conserved 4, scale-free metric 1} | D1 measure table (identity + table) | `cosmology_initial_conditions.py:L116-L126, L135-L139 ns_from_density_slope(), measure_predictions()` | exact (table); σ computed (HZ 8.357σ, inventory F285 D1a) |
| 2 | $x=k_*/k_\text{BZ}$, $k_\text{BZ}=\pi/a$, $a=\sqrt{8\pi}3^{1/4}\ell_P$; suppression $x^{n_s}$, enhancement $x^{n_s-4}$ | D1b required non-genericity (58.26 dec.) | `…:L161-L173 required_non_genericity()` | computed (inventory F285 D1b) |
| 3 | $ka=\pi x$, correction $(ka)^2$ | D2 BZ reach | `…:L186-L191 brillouin_zone_reach()` | exact (reg) (row read: computed) |
| 4 | $P=Ak^n\mapsto b^{-3}P(k/b)=b^{-(3+n)}Ak^n$; $k\partial_k\ln P'=n$ | D3 power laws are block-spin fixed points; $n$ marginal | `…:L240-L262 blockspin_tilt_marginality()` | exact (reg) |

**Inputs → outputs:** Planck $n_s$, pivot → `run` (L294). Constants: `a_over_ellP` (exact), `ell_P_m`. **Depends on:** nothing in-tree. **Flags:** the D1 row "local short-range-correlated (…even a critical Gaussian field squared) → $n_s=0$" is **partially SUPERSEDED by F310 C2** (critical Gaussian² gives $n_s=-1$); the table value 0 is still right for the gapped case. The key relation $P_\rho\propto k^{n_s}$ is only stated here (identity function); it is computed in `cosmology_critical_measure` row 2. `b_value` parameter is unused ($b$ is symbolic). $\Delta^2_\Phi$ Poisson step uses the F106 reduction.

---

### `engine/interactions/cosmology_lambda_dynamics.py` — is the zero-point sum dynamically capped? (F332)
**Status:** live · standalone · **Findings:** F332 F164 F193 F196 F241 F319 F311 F178 F182 F130 F79 F59 · **Lattice:** BCC dispersion (single Weyl branch $\omega^+$, via `sakharov_moments` / `bcc_dispersion`) · **Law:** n/a (no propagation; moment integrals of $\omega^+$) · **Units:** SI for K1; lattice $k$ for K2–K4

**Does:** K1 shows the capacity ceiling is Friedmann-I and that the bare zero-point source self-consistently gives a sub-cell horizon; K2 shows the static Poisson law is Fredholm-blind to a homogeneous source; K3/K4 show F130-style blocking of the Sakharov moments cannot be order-selective.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G=a^2c^3/(8\pi\sqrt3\hbar)$ | structural $G$ (F79) | `cosmology_lambda_dynamics.py:L130 structural_G_SI()` | quantitative (reg) (row read: exact) |
| 2 | $\rho_\text{ceil}=3c^4/(8\pi GR_H^2)\equiv3H^2c^2/(8\pi G)$ at $H=c/R_H$ | ceiling = Friedmann I | `…:L139-L142 ceiling_is_friedmann()` | quantitative (reg) (row read: exact (float floor)) |
| 3 | $I_{cc}=\langle\omega/2\rangle_\text{BZ}$, $I_g=\langle1/2\omega\rangle_\text{BZ}$ (midpoint grid, period $2\pi\sqrt3$) | Sakharov moments (external helper) | `qed_uv_completion.py:L418-L420 sakharov_moments()` | machine (closed form $I_{cc}=3\sqrt3\pi/4$, inventory F408 row 88) |
| 4 | $\tau=a/(\sqrt3c)$; $\rho_\text{vac}=g_*\,\hbar I_{cc}/(\tau a^3)$; $H=\sqrt{8\pi G\rho/3c^2}$; $R_H=a\sqrt{3/(g_*I_{cc})}=0.606a$ ($g_*=2$) | K1 bare-source horizon | `…:L155-L163 bare_source_horizon()` | quantitative (reg) (row read: exact (closed form) / machine (numeric match)) |
| 5 | $\nabla^2u=-S$ on an $N^3$ torus: $\hat u=\hat S/k^2$ ($k\ne0$), $\hat u_0=0$; DC residual $=\langle S\rangle$ | K2 Fredholm obstruction (real FFT) | `…:L197-L208 homogeneous_source_blind()` | quantitative (reg) (row read: machine (residual/S₀ = 1 to 1e-8)) |
| 6 | $I_{cc}(b),I_g(b)$ with $\omega(\kappa/b)$ over the fixed BZ; fit $I_{cc}\sim C_{cc}b^{p_{cc}}$, $I_g\sim C_gb^{p_g}$ on $b\in[10^2,10^4]$ | K3 asymptotics ($p_{cc}\to-1$, $p_g\to+1$) | `…:L248-L252, L268-L270 blockspin_moment(), blockspin_asymptotics()` | quantitative (reg) |
| 7 | $b^*=10^{\text{dex}/(3-p_{cc})}$; $G_\text{coarse}/G=I_g(1)\,b^{*2}/I_g(b^*)$; excluded iff $\lvert\Delta G/G\rvert>2.2\times10^{-5}$ | K4 order-selectivity excluded | `…:L298-L307 blockspin_selectivity()` | quantitative (reg) |

**Inputs → outputs:** $g_*$, grid $n$, controls `subtract_source_mean`, `required_dex`, `allowed_delta_G_over_G` → five checks (`run`, L321). Constants: `a_over_ellP` (exact), `c_SI`, `ell_P_m`, `hbar_SI` (external); `G_REL_UNCERTAINTY=2.2e-5`, `two_sector_solve` (F319 U8 overshoot) from `qed_uv_completion`. **Depends on:** `interactions.qed_uv_completion` (07c-interactions-qed.md), `lattice.bcc.bcc_dispersion` (03-lattice.md). **Flags:** all moments use the single chiral branch `sign='+'` of the BCC Weyl dispersion — no even/paired law (OTHER: convention, a branch choice worth stating); `bcc_dispersion(κ/b)` underflows silently for $b\gtrsim3\times10^8$ — guarded at $b\le10^6$ (L238); the observed $R_H=1.3807\times10^{26}$ m is a literal (L171); K4 relies on a two-point power-law extrapolation to $b^*\sim10^{30}$.

---

### `engine/interactions/cosmology_lambda_sequestering.py` — Kaloper–Padilla sequestering against the model (F367)
**Status:** live · standalone · **Findings:** F367 F332 F164 F193 F196 F241 F319 F178 F182 F79 F59 · **Lattice:** n/a · **Law:** n/a · **Units:** $\rho$ in units of $\rho_\text{crit}$

**Does:** verifies symbolically that the KP subtraction $T(t_0)-\langle T\rangle_{V_4}$ removes any additive constant and gives a surviving residual $3n\rho(t_0)$ for power-law histories; compares $2\Omega_{m0}$ with $\Omega_\Lambda$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $a=(t/t_0)^n$, $T=-\rho_{m0}a^{-3}-C$, $\langle T\rangle=\int a^pT\,dt/\int a^pdt$; $\partial_C[T(t_0)-\langle T\rangle]\equiv0$; $\dfrac{T(t_0)-\langle T\rangle}{\rho_{m0}}=\dfrac{3n}{(p-3)n+1}\ \to3n$ at $p=3$ | S3 exact cancellation + coefficient | `cosmology_lambda_sequestering.py:L169-L186 sequestering_symbolic_identity()` | quantitative (reg) (row read: exact (sympy)) |
| 2 | $3n$ as `Fraction` | residual coefficient (matter 2, radiation 3/2) | `…:L208 sequestering_residual_coefficient()` | quantitative (reg) (row read: exact) |
| 3 | $\log_{10}[2\Omega_{m0}/(1-\Omega_{m0}-\Omega_{r0})]=-0.036$ | S5 matter-dominated toy vs $\Omega_\Lambda$ | `…:L218-L221 matter_dominated_residual_dex()` | quantitative (reg) (row read: computed (toy; not a derivation)) |

**Inputs → outputs:** $n$, $p$, $\Omega_{m0}$, control `include_vacuum_subtraction` → three checks (`run`, L247). **Depends on:** `cosmology.OMEGA_M0/OMEGA_R0` (above), `qed_uv_completion.two_sector_solve`. **Flags:** registry `quantitative` while S3 is exact — fine; `required_relative_selectivity: 1.27e116` is a hard-coded literal (L239) not re-derived; `a_over_ellP`, `c_SI`, `ell_P_m`, `hbar_SI`, `RHO_LAMBDA_SI`, `sakharov_moments` imported but unused; the `include_vacuum_subtraction=False` control sets the check False by assignment rather than recomputing (L263-L264).

---

### `engine/interactions/cosmology_lambda_sequestering_consistency.py` — KP base action vs decision 4 (F368)
**Status:** live · standalone · **Findings:** F368 F367 F332 F164 F241 F319 F178 F182 F79 F59 · **Lattice:** n/a · **Law:** n/a · **Units:** $M_\text{pl}$, $H$ symbolic

**Does:** runs CL303 falsifier 4: shows the KP local equation reduces in vacuum to GR + $\Lambda_\text{eff}$, and that KP's finite-$V_4$ requirement is violated by eternal de Sitter and flat matter but met by a closed recollapse.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M_\text{pl}^2G_{\mu\nu}=\tau_{\mu\nu}-\tfrac14g_{\mu\nu}\langle\tau\rangle$, $\tau=0\Rightarrow G_{\mu\nu}=-\Lambda_\text{eff}g_{\mu\nu}$, $\Lambda_\text{eff}=\langle\tau\rangle/4M_\text{pl}^2$ | C1 vacuum reduction (one scalar component) | `cosmology_lambda_sequestering_consistency.py:L149-L158 vacuum_reduces_to_gr_plus_lambda_eff()` | quantitative (reg) (row read: exact (algebraic)) |
| 2 | $V_4=\int_0^Te^{3Ht}dt=(e^{3HT}-1)/3H\to\infty$ | C2a eternal de Sitter | `…:L176-L179 eternal_de_sitter_v4_diverges()` | quantitative (reg) (row read: exact) |
| 3 | $V_4=\int_0^T(t/t_*)^{2}dt\to\infty$ ($a\propto t^{2/3}$, $p=3$) | C2b flat matter | `…:L199-L201 flat_open_matter_only_v4_diverges()` | quantitative (reg) (row read: exact) |
| 4 | $a=A(1-\cos\eta)$: $V_4\propto\int_0^{2\pi}a^{4}d\eta$ finite | C2c closed matter recollapse | `…:L227-L231 closed_recollapse_v4_finite()` | quantitative (reg) (row read: exact) |
| 5 | CPL $w=w_0+w_a(1-a)$, $dw/da=-w_a>0$ for $w_a=-1.05$ | C3 DESI direction (qualitative) | `…:L253-L256 desi_w_evolution_direction()` | quantitative (reg) (row read: exact (sign only)) |

**Inputs → outputs:** controls `substitute_vacuum`, `measure_power`, `finite_time_only`, `wa_sign_flip` → five checks and a falsifier-4 verdict (`run`, L268). **Depends on:** `cosmology` (imports unused `OMEGA_M0`, `OMEGA_R0`). **Flags:** ⚠ DOC/CODE MISMATCH — `flat_open_matter_only_v4_diverges` and the module docstring (C2) claim flat **and open** matter-only expansion is checked; the code computes only the flat $a\propto t^{2/3}$ case. The C2c recollapse is matter-only (no Λ), so "finite $V_4$ requires $k>0$" is illustrated, not derived (the docstring says the Padilla eq. 7.23 proof is cited). The DESI $w_0=-0.727$, $w_a=-1.05$ are "illustrative" literals, used only for sign. The `finite_time_only` control sets `de_sitter_diverges=False` by assignment (L285).

---

### `engine/interactions/cosmology_lambda_sign_split.py` — the a₀/a₁ sign split of the heat-kernel sum (F408)
**Status:** live · standalone · **Findings:** F408 F164 F61 F193 F196 F183 F190 F332 F367 F241 F79 F86 · **Lattice:** BCC single-branch dispersion (via `sakharov_moments`, $n=64$ even) · **Law:** n/a · **Units:** SI for S2/S4 numerics; symbolic otherwise

**Does:** shows the all-fermion content gives $a_0<0$, $a_1>0$; that "F193 §B" ($a_0$ diluted) and "F196" ($a_1$ ceiling) are opposite-sign objects with ratio $24\sqrt3\pi$; that the capacity ceiling cannot act on a negative $a_0$; that the $a_1$ capacity energy is linear in $L$; and that KP sequestering is sign-blind. **SUPERSEDES** the F193 §B sign reading (supersessions S25).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g_*=3\times(2+1+6+3+3+1)=48$ | Weyl content | `cosmology_lambda_sign_split.py:L119 model_weyl_content()` | exact (reg) |
| 2 | $c_\text{Weyl}=-2(\tfrac16-E_L)$, $E_L=\tfrac14\Rightarrow+\tfrac16$; $c_\text{scalar}=\tfrac16$; $c_\text{vector}=\tfrac46-1-\tfrac26=-\tfrac23$; $a_0$: Weyl $-2$, scalar $+1$, vector $+2$; $\sum\eta=\tfrac12\sum c=g_*/12=4$ | S1 statistics-signed $a_0$, $a_1$; $\operatorname{sign}a_0\operatorname{sign}a_1=-1$ | `…:L146-L157 heat_kernel_signs()` | exact (`Fraction`, inventory F408 row 245) |
| 3 | $a=\sqrt{2\pi\eta}\,3^{1/4}\ell_P$ (content-derived); check $(a/\ell_P)^2=2\pi\eta\sqrt3$ at $\eta=4$ | canonical cell = content | `…:L207, L227 route_halves()` | exact (reg) |
| 4 | $\rho_\text{br}=\sqrt3I_{cc}\hbar c/a^4$; $\rho_{193B}=\operatorname{sign}a_0\,N_b\rho_\text{br}(a/R_H)^2$; $\rho_{196}=3c^4/(8\pi\operatorname{sign}(a_1)G_\text{str}R_H^2)$; $\lvert\rho_{193B}\rvert/\lvert\rho_{196}\rvert=\dfrac{4N_bI_{cc}}{3\eta}\overset{N_b=2g,\,\eta=g/12}{=}32I_{cc}=24\sqrt3\pi$ | S2 the two halves (sympy + numeric) | `…:L210-L236 route_halves()` | exact (sympy) / machine ($I_{cc}$ grid, inventory rows 246, 88) |
| 5 | F193 as written: $g_*=2$ branches vs 48-Weyl $G$ ⇒ $\sqrt3\pi/2$ | content-mismatch artifact (reported) | `…:L239-L241 route_halves()` | exact (reg) (row read: computed) |
| 6 | $2G\cdot\tfrac43\pi\rho L^3/(Lc^2)=1$ has no positive root for $\rho<0$; $H^2=8\pi G\rho/3<0$ | S3 ceiling domain | `…:L274-L279 ceiling_domain()` | exact (inventory row 247) |
| 7 | $E(L)=\rho_\text{ceil}\tfrac43\pi L^3=c^4L/2G$, $E''=0$, $\sigma_H=c^4/2G=4\pi\sqrt3\hbar c/a^2$ (with structural $G$) | S4 linear capacity tension | `…:L297-L304 capacity_tension()` | exact (inventory row 248) |
| 8 | as `lambda_sequestering` row 1 with $C\in\mathbb R$; residual($+X$) $-$ residual($-X$) $=0$ | S5 sign-blind | `…:L323-L334 sequestering_sign_blind()` | exact (reg) |

**Inputs → outputs:** levers `lichnerowicz_E`, `fundamental_bosons`, `fundamental_vectors`, `zero_point_weight`, `sequester` → 13 checks (`run`, L346). Constants: `a_over_ellP`$=\sqrt{8\pi}3^{1/4}$ (exact, F79/F107), `G_CODATA`, `c_SI`, `ell_P_m`, `hbar_SI`; $H_0$, Mpc from `cosmology`. **Depends on:** `qed_uv_completion.sakharov_moments`, `cosmology`. **Flags:** the S2 symbolic ratio uses $G=\ell_P^2c^3/\hbar$ with a content-derived $a(\eta)$ — equivalent to calibrating $a$ on $G$; consistent with F59/F79 but note the two routes to the cell (OTHER, convention). $R_H=c/H_0$ uses `cosmology.H0_KM_S_MPC=67.4` (external) — the ratio is $H_0$-independent, the absolute densities are not.

---

### `engine/interactions/cosmology_lattice_elasticity.py` — can the BCC lattice be elastic? (F283, F284)
**Status:** live · standalone · **Findings:** F283 F284 · **Lattice:** BCC (via $c_\text{lat}$, $a$) · **Law:** n/a · **Units:** reduced Planck units and SI (ticks = $a/c$ per cell step)

**Does:** shows F282's obstruction $r=M_\text{Pl}^2/\Lambda_\text{UV}^2=\sqrt3$ is invariant under $a\to sa$, bounds any elastic fraction by LLR/BBN/Cassini/GW170817, and gives the earliest resolvable epoch of a rigid lattice.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G=(sa)^2c^3/(8\pi\sqrt3\hbar)$, $M^2=\hbar c/8\pi G$, $\Lambda=\hbar/(sac)$; $r=M^2/\Lambda^2=\sqrt3=1/c_\text{lat}$, $\partial_sr=0$ | E1 scale invariance | `cosmology_lattice_elasticity.py:L137-L142 invariance_under_stretch()` | exact (inventory F283 E1) |
| 2 | $\dot G/G=2qH_0$; $q_\max^\text{LLR}=b/2H_0$; $q_\max^\text{BBN}=\delta/(2\ln(1+z_\text{BBN}))$; $G_\text{BBN}/G_0=(1+z)^{-2}$ at $q=1$ | E2 elastic fraction bounds | `…:L160-L172 varying_G_bounds()` | computed (inventory F283 E2) |
| 3 | $\alpha^2=g/(2-g)$ from $\lvert\gamma-1\rvert=2\alpha^2/(1+\alpha^2)$, $g=2.3\times10^{-5}$ | E3 Cassini bound on a new scalar | `…:L198 volume_mode_dichotomy()` | exact (reg) (row read: computed) |
| 4 | $f_\text{tree}=2(\delta c/c)/(c_s^2/c_\text{lat}^2-1)$, offset = 1 | E4 GW170817 bound | `…:L223 graviton_cone_bound()` | exact (reg) (row read: computed (order of magnitude)) |
| 5 | $H_\max/M_\text{Pl}=c_\text{lat}/3^{1/4}=3^{-3/4}$; $t_\min=1/c_\text{lat}=\sqrt3$ ticks $=a/(c_\text{lat}c)=11.43\,t_P$ | F284 earliest epoch | `…:L247-L249 earliest_resolvable_epoch()` | exact (reg) |
| 6 | $R_H=c/H_0$, cells $=R_H/a$, volume $(R_H/a)^3$ | F284 cell budget | `…:L271-L276 lattice_cell_budget()` | exact (reg) (row read: computed) |

**Inputs → outputs:** $H_0=67.4$, LLR, BBN $\delta G$, Cassini, GW170817, $t_P$ (literals) → `run` (L283). Constants: `c_lat`$=1/\sqrt3$ (exact, F26), `a_over_ellP` (exact), `c_SI`, `ell_P_m`. **Depends on:** constants only. **Flags:** SI $t_\min=a/(c_\text{lat}\,c)=\sqrt3\,a/c$ (L249) makes one tick $=a/c$, so the lattice light speed $c_\text{lat}$ cells/tick would be $c/\sqrt3$ in SI; `lambda_dynamics.bare_source_horizon` (L155) instead uses $\tau=a/(\sqrt3c)$, i.e. $c_\text{lat}\,a/\tau=c$. The two SI tick conventions differ by a factor $\sqrt3$ (OTHER — for the 03-lattice `si_scale` reconciliation, not settled here). The F284 SI number $t_\min=11.43\,t_P$ rests on the first. `a_over_ell_red=3^{1/4}` is a literal (F282 A1).

---

### `engine/interactions/cosmology_primordial.py` — primordial-sector no-go: no slow-roll inflaton (F282)
**Status:** live · standalone · **Findings:** F282 · **Lattice:** BCC (via $a/\ell_P$, $c_\text{lat}$) · **Law:** n/a · **Units:** reduced Planck units; field in units of a decay constant $f$ ($\phi=f\chi$, $r\equiv M_\text{Pl}^2/f^2$)

**Does:** shows the lattice cutoff is sub-Planckian with a universal obstruction $r=\sqrt3$, that both E_g directions (clock angle, radial hat) need super-Planckian $f$, that periodic potentials cap $n_s\le1-p^2r$, that the Starobinsky $R^2$ coefficient is ~10 decades short, and that the F130 RG spectrum has an O(1) gap around marginality.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $a/\ell_\text{red}=(a/\ell_P)/\sqrt{8\pi}=3^{1/4}$; $\Lambda_\text{UV}/M_\text{Pl}=3^{-1/4}=\sqrt{c_\text{lat}}$; $r_\min=\sqrt3=1/c_\text{lat}$ | Leg A cutoff | `cosmology_primordial.py:L114-L123 cutoff_ratio()` | exact (inventory F282 A1) |
| 2 | $\epsilon/r=\tfrac12(V'/V)^2$, $\lvert\eta\rvert/r=\lvert V''/V\rvert$; $K=\min_\chi\max(\epsilon,\lvert\eta\rvert)/r$ (400 001-pt grid) | generic slow-roll machinery | `…:L137-L147 slowroll(), min_slowroll()` | quantitative (grid) (reg: exact; row is weaker — see flags) |
| 3 | $r_\text{req}=0.02/K$, $f/M_\text{Pl}=r_\text{req}^{-1/2}$, $J=(1/c_\text{lat})/r_\text{req}$ | required decay constant / N-flation count | `…:L152-L158 required_decay_constant()` | exact (reg) |
| 4 | $V=\tfrac A2(1+\cos6\delta)$, $A=\lambda_6e_\text{sat}^6$; $u=\cos6\delta$: $\epsilon/r=18\frac{1-u}{1+u}$, $\lvert\eta\rvert/r=\frac{36\lvert u\rvert}{1+u}$, cross at $u=\tfrac13$ ⇒ $K=9$ | E_g clock direction | `…:L178-L193 eg_clock_coefficient()` | exact ($K=9$, inventory F282 B1); numeric $K$ quantitative |
| 5 | $\hat V(e)=\tfrac{\kappa_E}2e^2+c\,e^4+\lambda_6e^6$, $e_\min^2=\dfrac{-4c+\sqrt{16c^2-24\lambda_6\kappa_E}}{12\lambda_6}$, $V=\hat V-\hat V(e_\min)$; $\eta/r\rvert_0=\hat V''(0)/V_0$ | E_g radial hat, $V(e_\min)=0$ imposed | `…:L219-L244 eg_radial_coefficient()` | machine/quantitative (inventory F282 B2: $K=5.9215$) |
| 6 | $n_s-1=-p^2r\frac{3+u}{1-u}\Rightarrow n_s\le1-p^2r$, $r=(1/c_\text{lat})/J$ | periodic-direction spectral bound | `…:L263-L264 periodic_ns_bound()` | exact (inventory F282 C1) |
| 7 | $c_2^\text{req}=1/(12(M_s/M_\text{Pl})^2)$, $M_s/M_\text{Pl}=1.3\times10^{-5}$; $c_2^\text{ind}=N/(96\pi^2)$, $M_s^\text{ind}=1/\sqrt{12c_2^\text{ind}}$ vs $\sqrt{c_\text{lat}}$ | Starobinsky escape | `…:L288-L299 starobinsky_gap()` | computed (9.67 decades, inventory F282 C2) |
| 8 | exponents $\{+1,-2,-2,-3,-4\}$; gap $=\min\lvert\text{exp}\rvert=1$ | RG marginality gap (F130) | `…:L326-L336 rg_marginality()` | exact (reg) |

**Inputs → outputs:** none → `run` (L341). Constants: `a_over_ellP`$=\sqrt{8\pi}3^{1/4}$ (exact, F79/F107), `c_lat`$=1/\sqrt3$ (exact, F26), `lambda_6`$=0.243$ (quantitative; output of $\delta^*=2/9$ via F234, founding decision 7), `e_saturation`$=0.733$ (quantitative, F92/F118/F234); literals $\kappa_E=-2.156$, $c=1.10$ (F118), Planck $n_s$. **Depends on:** `casim.numerics.xp`; read by `cosmology_geon_domain_wall_reopening`. **Flags:** **SUPERSEDED premise** — `eg_radial_coefficient` fixes $V_0=-\hat V(e_\min)$ as "forced by F193" (L211-L213, L231) i.e. the "ontic vacuum gravitates as zero" of F193 Part A, which supersessions S25 records as EXCLUDED (F319 U8 / CL275, 2026-08-18); the radial-direction numbers (row 5) rest on it (the clock direction, row 4, does not). F118 hat coefficients are literals, not registry constants. `rg_marginality` hard-codes F130's exponents rather than reading them.

---

### `engine/interactions/cosmology_second_scale.py` — a second scale must be a log, not a length (F286)
**Status:** live · standalone · **Findings:** F286 · **Lattice:** n/a (uses F285's 58.26-decade pivot/BZ separation) · **Law:** n/a · **Units:** dimensionless; eV literals

**Does:** proves a constant tilt needs a logarithmic, not power-law, second scale; predicts the running of the log class; inventories the model's couplings; and runs a look-elsewhere count on $\delta^*/2\pi$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $x\partial_x\ln(Cx^p)=p$; $L\partial_L\ln(C/L)=-1$; bound $\lvert d\ln F/d\ln x\rvert<(\sigma_\alpha+\lvert\alpha_\text{obs}\rvert)/(1-n_s)=0.319$ | T1 classification | `cosmology_second_scale.py:L143-L145 classification_theorem()` | exact (sympy) + external bound (inventory F286 T1) |
| 2 | $L=58.2596\ln10$; $dn_s/d\ln k=-(1-n_s)/L=-2.62\times10^{-4}$ | T2 class prediction | `…:L134, L168 _L(), running_prediction()` | exact (reg) (row read: computed (no free parameter)) |
| 3 | $C=(1-n_s)L=4.709$ | T3 required coefficient | `…:L184 required_coefficient()` | exact (reg) (row read: computed) |
| 4 | $\alpha/2\pi$; $\log_{10}(\Lambda_\text{QCD}/k_*)$ | T4 coupling inventory | `…:L200, L211 coupling_inventory()` | exact (reg) (row read: computed) |
| 5 | hits of $v\,\pi^m$, $v\in\{p/q\le12\}\cup$ registry constants, $m\in\{-2,-1,0,1\}$, in $[1-n_s\pm\sigma]$; $\delta^*/2\pi=1/9\pi$ | T5 look-elsewhere | `…:L240-L279 coincidence_look_elsewhere()` | exact identity; count computed (inventory F286 T5) |

**Inputs → outputs:** Planck $n_s$, running; $\alpha$, $\alpha_s(M_Z)=0.11955$, $\Lambda_\text{QCD}$, $k_*$ (literals) → `run` (L290). Constants: `delta_star_f`$=2/9$, `sin2_thetaW_onshell`$=2/9$, `cos3_delta_star`, `c_lat`, `lambda_6`, `e_saturation` (seeds only). **Depends on:** constants only. **Flags:** the p = 0 reading of T1 is **corrected by F295** (a constant $F$ is a scale-free anomalous dimension, not trivial) — a prose correction, not a ledger supersession; the code's T1 check still passes because it tests only $p=2$ and the log class. `DECADES_PIVOT_TO_BZ` is a transcribed float (L119) rather than re-computed from `a_over_ellP` as `cosmology_initial_conditions` does. Registry `exact` for a module whose T2–T5 are computed from data.

---

### `engine/interactions/cosmology_transfer_function.py` — model-native sound horizon and Saha recombination (F369)
**Status:** live · standalone · **Findings:** F369 · **Lattice:** n/a · **Law:** n/a · **Units:** Mpc, $H_0=100h$ km/s/Mpc; eV, nm

**Does:** replaces two EH98 scale-setting fits with model-side calculations — the sound horizon by integrating the F182/F188 background, and $z_*$ by Saha with the F125 Rydberg energy — and measures what that does to $\sigma_8$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_\gamma=2.47282\times10^{-5}(T/2.7255)^4/h^2$; $R=3\Omega_ba/4\Omega_\gamma$; $c_s=1/\sqrt{3(1+R)}$ | photon–baryon fluid | `cosmology_transfer_function.py:L110, L116, L123 omega_gamma(), R_of_a(), sound_speed()` | quantitative (reg) (row read: exact (S1: $c_s\to1/\sqrt3$; S2: $R/a$ constant, sympy)) |
| 2 | $r_s(a)=\frac{c}{H_0}\int_{10^{-10}}^{a}\frac{c_s(a')\,da'}{a'^2E(a')}$ (Simpson, $2\times10^5$) | sound horizon on the model background | `…:L171-L183 sound_horizon_mpc()` | quantitative (reg) |
| 3 | $s_\text{EH98}=44.5\ln(9.83/\omega_m)/\sqrt{1+10\omega_b^{3/4}}$ | EH98 internal fit, for D2 | `…:L237-L239 eh98_internal_fitting_s()` | external fit |
| 4 | EH98 no-wiggle $T(k)$ with $s$ passed in; $\sigma_8$ via `cosmology_growth`'s $\sigma_R$ integrand + $(1-4f_\nu)$ | D3 σ₈ shift from the substitution | `…:L281-L290, L311-L325 transfer_eh98_with_sound_horizon(), sigma8_model_native_sound_horizon()` | quantitative (reg) |
| 5 | $B=$ `atom.rydberg_eV`$(\mu_{ep})$ | model-native ionisation energy (F125) | `…:L385-L386 _model_native_B_ion_eV()` | quantitative (reg) (row read: machine (per F125)) |
| 6 | $\frac{X_e^2}{1-X_e}=\frac{S}{n_b}$, $S=\left(\frac{m_eT}{2\pi(\hbar c)^2}\right)^{3/2}e^{-B/T}$, $n_b=\eta\,\frac{2\zeta(3)}{\pi^2}\left(\frac{T}{\hbar c}\right)^3$, $T=k_BT_0(1+z)$; $X_e=\tfrac12(-\rho+\sqrt{\rho^2+4\rho})$ | Saha ionisation | `…:L391, L399-L405 _n_gamma_per_nm3(), saha_xe()` | quantitative (reg) (row read: exact formula) |
| 7 | bisection $X_e(z_*)=0.5$ on $[400,3000]$ | recombination redshift (D4: +26 % bias vs Planck, by design) | `…:L417-L433 find_z_recombination_saha()` | quantitative (reg) |

**Inputs → outputs:** `cosmology_growth.EXTERNAL` (Ω's, $h$, $T_\text{cmb}$, $A_s$), Planck $z_\text{drag}$, $r_\text{drag}$, $z_*$, $\eta_{10}$ from `cosmology_bbn` → six legs (`run`, L533) with controls `z_drag_multiplier`, `b_ion_multiplier`. **Depends on:** `cosmology_growth`, `cosmology_bbn` (above), `particles.atom` (06a/06b particles map files). **Flags:** D1 is an internal-consistency check (same Planck inputs on both sides — the module says so); `transfer_eh98_with_sound_horizon` duplicates `cosmology_growth.transfer_eh98` line-for-line apart from `s` (drift risk); Saha uses $n_b$ with no helium correction (stated); $k_B$, $\zeta(3)$ literals. Registry `quantitative` consistent.

---

### `engine/interactions/darkmatter.py` — rotation curves and the Bullet-Cluster toy (F191, scenario S8)
**Status:** live · test-only · **Findings:** (registry: none) — code cites F191, F178 · **Lattice:** n/a · **Law:** n/a · **Units:** kpc, km/s, $M_\odot$; Mpc and arbitrary mass units in the Bullet toy

**Does:** contrasts baryon-only, NFW-halo and MOND rotation curves, and builds a 1-D post-collision mass toy showing the lensing peak offset from the gas peak (favouring a real dark source over baryon-tracking modified gravity).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M(<r)=M_d[1-(1+x)e^{-x}]$, $x=r/R_d$; $v=\sqrt{GM/r}$ | exponential disk (spherical enclosed-mass approx.) | `darkmatter.py:L37-L38 v_disk()` | unknown (inferred: exact formula (approximation declared)) |
| 2 | $M(<r)=M_{200}\dfrac{\ln(1+x)-x/(1+x)}{\ln(1+c)-c/(1+c)}$, $x=r/r_s$, $r_s=R_{200}/c$ | NFW halo | `darkmatter.py:L43-L47 v_nfw()` | unknown (inferred: exact formula) |
| 3 | $v_\text{tot}=\sqrt{v_\text{disk}^2+v_\text{NFW}^2}$ | total (defaults only) | `darkmatter.py:L51 v_total()` | unknown (inferred: exact) |
| 4 | $g_\text{eff}=\sqrt{g_Na_0+g_N^2}$, $v=\sqrt{g_\text{eff}r}$, $a_0=3.6\times10^3$ (km/s)²/kpc | MOND toy | `darkmatter.py:L60-L61 v_mond()` | unknown (inferred: exact formula (interpolation: see flags)) |
| 5 | gas $=f_g M_b[\mathcal G(-0.15,0.18)+\mathcal G(0.15,0.18)]$, collisionless $=(5M_b+(1-f_g)M_b)[\mathcal G(\mp0.36,0.15)]$; X-ray peak $=\arg\max$ gas; lensing peaks $=\arg\max$ total on each side | Bullet-Cluster toy | `darkmatter.py:L90-L99 bullet_cluster()` | unknown (inferred: toy (hand-placed Gaussians)) |

**Inputs → outputs:** $r$ grid, disk/halo parameters, gas fraction → rotation-curve flatness metrics; peak positions. $G=4.30091\times10^{-6}$ kpc (km/s)²/$M_\odot$ (literal). **Depends on:** numpy only. **Flags:** ⚠ DOC/CODE MISMATCH `v_mond` (L59-L60): the comment says the simple interpolating function $\mu(x)=x/(1+x)$, which inverts to $g=\tfrac12g_N+\sqrt{\tfrac14g_N^2+g_Na_0}$; the code computes $g=\sqrt{g_Na_0+g_N^2}$ (same deep and Newtonian limits, different transition). `v_total(r, **kw)` ignores `**kw` (always default disk/halo). The Bullet result is set by where the Gaussians are placed (collisionless at $\pm0.36$ Mpc, gas at $\pm0.15$), i.e. it illustrates rather than computes the offset. Registry findings empty, exactness `None`; direct `import numpy` (D8).
