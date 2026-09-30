# Forks — dark sector, cosmological constant, gauge, lattice, electroweak and particle forks

Scope: the dark-sector and vacuum-energy forks under `src/casim/engine/forks/gravity/` (F164 → F193 → F196 cosmological-constant chain; the F197 → F198 → F199b → F266 (file "F200") → F201 → F202 → F203 → F205 → F237 keV-sterile chain; the F216 → F223 → F228 → F238 spin-2 geon chain; the F180/F248 graviton-speed forks), plus every module in `forks/darkmatter/`, `forks/electroweak/`, `forks/gauge/`, `forks/lattice/` and `forks/particles/`. A fork is a recorded alternative, not dead code. It is either a tested-and-rejected branch that keeps the falsification record, or a live exploratory branch. Each block gives the registry status (`fork_live` / `fork_unclaimed` / `live`) and what `docs/theory/supersessions.yaml` and `key-decisions.md` say about the branch.

**Shared conventions.**
- Most dark-sector forks are **particle-cosmology bookkeeping in SI or natural GeV units**, not lattice kernels. Their Law/Lattice fields are `n/a`.
- SI inputs come from the registry where the code imports them: $c$, $\hbar$, $G_\text{CODATA}$, $\ell_P$ (CODATA, `external`) and the F107 cell $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107, exact).
- Many cosmological numbers stay **inline literals**, with the fork status recorded as the reason: $\rho_\Lambda=6.0\times10^{-10}$ J/m³, $H_0$, $M_\text{Pl}$ in GeV, $G_F$, $\alpha$, $s_0$, $\rho_c/h^2$, $g_*$ and PDG masses. They are listed once per block under *Flags* only when they matter.
- Where a fork evaluates the BCC dispersion, it uses the Paper-1 Eq. 15 branch $u^\pm=c_xc_yc_z\pm s_xs_ys_z$ with $c_i=\cos(k_i/\sqrt3)$ (see 03-lattice.md § `bcc.py`). Some modules write this in the variable $q=k/\sqrt3$. The graviton forks (F180, F248) use the **even** (paired) law $\Omega=\omega^+(k/2)+\omega^-(k/2)$ (F91 class, see 05c-gauge-photon-lpt-weak.md § `photon.py`).
- The registry gives `exactness: None` for every manifest-origin fork. Per the brief, the equations are therefore tagged `unknown` unless `docs/status/exactness-inventory.md` names the specific result (F180, F193, F196, F223, F228, F248 rows 216/221/222/252–257/F248-A…E, F94, F404, F407).
- **Hazard shared by F216, F223, F228, F238:** these run their whole battery and **write `test-results/*.json` at import time**. There is no `__main__` guard, so they break the CLAUDE.md §5 rule. They were not imported for this map.

Modules covered (35 = 30 registered modules + 5 package `__init__`s): `forks/gravity/` gr_fork_F164, F180, F193, F196, F197, F198, F199, F200, F201, F202, F203, F216, F223, F228, F238, F248; `forks/darkmatter/` `__init__`, dm_fork_F205, F237, F364; `forks/electroweak/` `__init__`, hypercharge_fork; `forks/gauge/` `__init__`, curl_fork_baseline_bcc, curl_fork_cubic, curl_fork_harness, lgt_fork_A_mc, u1_link_unitarity_forks; `forks/lattice/` `__init__`, smearing_fork_harness; `forks/particles/` `__init__`, complex_mass_fork, derive_weight_as_phase, koide_pseudomass_fork, koide_pseudomass_minimal.

---

### `engine/forks/gravity/gr_fork_F164_cosmological_constant.py` — bare BCC zero-point vacuum energy
**Status:** fork_unclaimed · unreferenced · **Findings:** F164 · **Lattice:** BCC (Paper-1 Eq. 15 "+" branch, variable $q=k/\sqrt3$) · **Law:** single chiral branch $\omega^+$ · **Units:** lattice integral → SI

**Does:** evaluates the Brillouin-zone zero-point integral of the BCC Weyl dispersion and converts it to an SI vacuum-energy density at the F107 cell. This is the model's "$10^{121}$" cosmological-constant problem.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u=\cos q_x\cos q_y\cos q_z+\sin q_x\sin q_y\sin q_z,\ \omega^+=\arccos u$ | BCC "+" branch per tick | `gr_fork_F164_cosmological_constant.py:L53 omega_plus()` | unknown |
| 2 | $I_\text{CC}=\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{\omega}{2}=\frac{3^{3/2}}{(2\pi)^3}\sum_q\frac{\omega(q)}{2}\,\Delta q^3$, $q\in[-\pi,\pi]^3$ midpoint grid | dimensionless zero-point integral (Jacobian $d^3k=3^{3/2}d^3q$) | `…:L73 zero_point_integral()` | unknown |
| 3 | $u(q)+u(q+\pi\hat x)=0\Rightarrow\omega+\omega'=\pi\Rightarrow\langle\omega\rangle_\text{BZ}=\pi/2$ | pairing identity for the mean rotation (checked as a residual) | `…:L99 run()` | unknown |
| 4 | $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P,\ \tau=a/(c\sqrt3)$ | F107 canonical cell and tick | `…:L41–L42` | unknown |
| 5 | $\rho_\text{vac}=g_*\,\frac{\hbar}{\tau a^3}\,I_\text{CC}=g_*\sqrt3\,I_\text{CC}\,\hbar c/a^4$, $g_*=2$ | bare vacuum-energy density (magnitude; the code notes the sign is $-1$ for an all-fermion vacuum) | `…:L79 vacuum_energy_density()`, `g_star` L101 | unknown |
| 6 | $E=(\rho(\hbar c)^3)^{1/4}/\text{eV}$ | quartic energy scale | `…:L84 quartic_scale_eV()` | unknown |

**Inputs → outputs:** grid size $n$ → $I_\text{CC}$ (spot-checked: $I_\text{CC}(n{=}60)=4.081$; grid mean $\omega=\pi/2$ to double precision), $\rho_\text{vac}$, and the ratio to $\rho_\Lambda$. **Depends on:** `casim.constants` a_over_ellP (F79/F107, exact), c_SI, hbar_SI, ell_P_m (CODATA). It reimplements the BCC $u^+$ inline instead of calling 03-lattice.md § `bcc.py`. **Flags:** $\rho_\Lambda=6.0\times10^{-10}$ J/m³ and the eV conversion are inline literals. This fork is the "template density" that the S25 supersession keeps live (F193 A3). The chain built on it (F193 Part A) is excluded; see F193 below.

---

### `engine/forks/gravity/gr_fork_F180_gw_speed.py` — gravitational-wave speed from the rotation rule
**Status:** fork_live · test-only · **Findings:** F180 · **Lattice:** continuum (checks A–D) + 2-D square reference grid (check E, D1 reference) · **Law:** even (argued; not evaluated) · **Units:** lattice ($c=1$ in A), dimensionless

**Does:** five checks that the induced (Sakharov) graviton inherits the constituent light cone $q_0=c_\text{lat}|q|$. The conclusion is $c_\text{grav}=c_\text{lat}=c_\gamma$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$, $\eta=\tfrac1{12},\ g_*=48$ → at $d=3$: $8\pi\sqrt3\,\hbar/(a^2c^3)$ | F79 structural $G$ (sympy) | `gr_fork_F180_gw_speed.py:L61–L65 check_A_coefficient_identity()` | exact (inv 216) |
| 2 | $8\pi G/c^4=a^2c_\text{lat}/(\hbar c)$ at $c=1$, $c_\text{lat}=1/\sqrt d$ | F106-E1 coefficient identity (sympy residual 0) | `…:L69–L71` | exact (inv 216) |
| 3 | $c\cdot\int_{\lvert k\rvert<\Lambda}\frac{d^dk}{2c\lvert k\rvert}$ independent of $c$ ($d=1,2,3$) | induced inverse coupling $\propto1/c_\text{lat}$ | `…:L115 check_B_inverse_coupling_carries_clat()` | machine (inv 216) |
| 4 | $\Pi_E(q_1,q_4)=\int\frac{d^2k}{(2\pi)^2}G(k)G(k+q),\ G=1/(c^2k_1^2+k_4^2+m^2),\ m=0.3$; flat along $c^2q_1^2+q_4^2=P_0^2$ | Euclidean 1+1 bubble depends only on the constituent invariant ⇒ pole $q_0=c\lvert q\rvert$ | `…:L144–L146 _bubble_euclid()`, isocontour L155–L161 | quantitative (inv 216) |
| 5 | $\lvert c_g-c_\gamma\rvert/c\le(f_\text{LIGO}/f_\text{Pl})^2$; slope residual set to $0$ | GW170817 margin | `…:L211–L213 check_D_dispersion_and_gw170817()` | exact (inv 216; slope by assignment) |
| 6 | $P^{n+1}=2P^n-P^{n-1}+(c_g\Delta t)^2(\nabla^2_\square P^n-s)$, $c_g=c_\text{lat}$; static seed $\hat P=-\hat s/k^2$ | hyperbolic $\ln K$ equation, leapfrog on a 2-D square 5-point stencil; wavefront speed + F106 Poisson fixed point | `…:L260, L270 check_E_realspace_wavefront()`, Poisson seed L253 | quantitative (inv 216) |

**Inputs → outputs:** none → five pass/fail dicts. Inventory row 216 gives wavefront $1.03\,c_\text{lat}$ and Poisson fixed-point $8.6\times10^{-4}$. **Depends on:** c_lat $=1/\sqrt3$ (F26, exact); `casim.numerics.fft` (02-numerics.md); the static law of 07b-interactions-gravity-relativity.md § gravity. **Flags:**
- ⚠ DOC/CODE MISMATCH: the check-D header comment L197 says the residual is "~1e-40". The code's bound $x^2$ (L211) evaluates to $\approx2.9\times10^{-83}$, which matches the note at L222.
- Check D does not compute the graviton slope. `slope_residual = 0.0` is assigned (L213).
- In check E the speed $c_g$ is the imported `C_LAT` placed in the stencil (L238). The measured wavefront therefore checks the leapfrog, not an independent derivation of the speed.

---

### `engine/forks/gravity/gr_fork_F193_ontic_vacuum.py` — "ontic vacuum gravitates as zero" + holographic residual
**Status:** fork_live · test-only · **Findings:** F193 · **Lattice:** BCC "+" branch (template integral only) · **Law:** n/a · **Units:** SI
**SUPERSEDED (partially) by F319/F408** — supersessions `S25-F193-partA-excluded-and-secB-sign-reading`:
- Part A ("bare CC = 0") is excluded (F319 U8 / CL275).
- Section B is not the residual: it is negative and 130.6× the F196 ceiling (F408 S2).
- Test legs A1/A2 are dead. A3 and B stay live as arithmetic.

**Does:** Part A shows that a diagonal "beable" energy functional vanishes on $\psi\equiv0$. Part B multiplies the F164 template density by $(a/R_H)^2$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $e=(\hbar/\tau)\sum_x\psi(x)^2$ | "beable" energy (no $+\tfrac12$ per mode); $=0$ on $\psi\equiv0$ | `gr_fork_F193_ontic_vacuum.py:L106 beable_energy_density()` | exact (inv 221) — **dead leg (S25)** |
| 2 | $K-1=\exp(2GM/rc^2)-1$ with $M=T^{00}_\text{vac}/c^2=0$ | flat dielectric on the empty lattice | `…:L123–L125 part_A()` | exact (inv 221) — **dead leg** |
| 3 | $I_\text{CC}$, $\rho_\text{vac}^\text{template}=g_*(\hbar/\tau a^3)I_\text{CC}$, $g_*=2$ | F164 template density recomputed | `…:L89 I_CC_zero_point()`, L130 | unknown (live, A3) |
| 4 | $R_H=c/H_0$, $H_0=67$ km/s/Mpc; $\rho_\text{grav}=\rho_\text{vac}(a/R_H)^2$ | holographic IR dilution (Part B) | `…:L151–L157 part_B()` | quantitative (inv 221; 0.54 dex coincidence) |
| 5 | $\rho_\text{CKN}=c^4/(8\pi GR_H^2)$ | Cohen–Kaplan–Nelson cross-check | `…:L165` | unknown |
| 6 | $f=\rho_\Lambda/\rho_\text{vac}$ | mean excitation fraction | `…:L167` | unknown |

**Inputs → outputs:** none → Part A zeros, Part B densities and log ratios. **Depends on:** F164 block above; constants G_CODATA, a_over_ellP, c_SI, ell_P_m, hbar_SI. **Flags:**
- SUPERSEDED (S25; F319/F408).
- Units mislabel: `beable_energy_density` returns J (no $1/a^3$), but it is stored under key `T00_ontic_vacuum_J_per_m3` (L134).
- Dead assignment at L163 (overwritten at L165).
- The section-B agreement uses $g_*=2$ against a $G$ induced at 48 Weyl fields (the F408 finding).

---

### `engine/forks/gravity/gr_fork_F196_dilution_exponent.py` — capacity ceiling $\rho=3c^4/8\pi GL^2$ ($p=2$)
**Status:** fork_live · test-only · **Findings:** F196 · **Lattice:** n/a · **Law:** n/a · **Units:** SI
**Sub-claim SUPERSEDED (S25):** reading $p=2$ as a dilution law of $\rho_\text{vac}$ is dead. Everything this module *computes* is live (F408 identifies the ceiling as the positive $a_1$ object).

**Does:** two independent routes to the maximal gravitating density a region of size $L$ can hold. Both land at $\rho_\text{crit}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M_\text{max}(L)=Lc^2/2G$ | Schwarzschild capacity (F183) | `gr_fork_F196_dilution_exponent.py:L80 schwarzschild_max_mass()` | exact (inv 222) |
| 2 | $\rho(L)=M_\text{max}c^2/(\tfrac43\pi L^3)=3c^4/(8\pi GL^2)$ | route 1 ceiling | `…:L85–L87 rho_grav_bh()` | exact (inv 222) |
| 3 | $d\ln\rho/d\ln L=-2$ | $p=3-1$ (two-point log slope) | `…:L93 exponent_slope()` | exact (inv 222) |
| 4 | $N=4\pi R_H^2/(4\ell_P^2),\ E/\text{dof}=\hbar c/(2\pi R_H)$ ⇒ $\rho=3\hbar c/(8\pi\ell_P^2R_H^2)$ | route 2: F190 area count × Gibbons–Hawking temperature | `…:L102–L107 rho_grav_holographic()` | exact (inv 222; route identity $\hbar c/\ell_P^2=c^4/G$) |
| 5 | $\rho_\text{crit}=3H_0^2c^2/8\pi G$ | energy critical density | `…:L116 run()` | unknown |
| 6 | $\rho_\text{vac}(a/R_H)^{3/2}$ vs $\rho_\text{vac}(a/R_H)^2$ | excluded statistical $p=3/2$ and naive $p=2$ | `…:L122–L123` | quantitative (inv 222) |
| 7 | $a^2/(4\ell_P^2)=2\pi\sqrt3$ | F190 per-cell entropy from the F107 cell | `…:L127` | exact (inv 222) |

**Inputs → outputs:** $H_0=67$ → ceiling $7.58\times10^{-10}$ J/m³ (0.10 dex above $\rho_\Lambda$; residual $\Omega_\Lambda$). **Depends on:** constants as in F193. **Flags:**
- `RHO_VAC = 3.4563582491862774e111` (L69) is a hard-coded copy of the F164 output. It is not recomputed and not registered.
- The sub-claim is superseded (S25).

---

### `engine/forks/gravity/gr_fork_F197_first_excitation_dark.py` — first excitation above vacuum as a unified dark sector
**Status:** fork_live · test-only · **Findings:** F197 · **Lattice:** n/a · **Law:** n/a · **Units:** mixed (EoS dimensionless, galactic kpc–km/s, cgs cross-section)

**Does:** classifies near-vacuum channels by equation of state: VEV gives $w=-1$, gapped gives $w\to0$, gapless gives $w=1/3$. It then computes the Hessian of the $E_g$ Landau functional to show both $E_g$ modes are gapped, and runs a halo/Bullet proxy.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $w_\text{VEV}=-1;\ w_\text{cold}=\tfrac13(\sigma_v/c)^2;\ w_\text{rad}=\tfrac13$ | EoS by excitation type ($\sigma_v=200$ km/s) | `gr_fork_F197_first_excitation_dark.py:L72, L78, L83` | unknown |
| 2 | $F(e,\delta)=\tfrac r2e^2+\tfrac b3e^3\cos3\delta+\tfrac u4e^4+\tfrac{w_6}6e^6\cos^23\delta$ | F93 $E_g$ Landau functional | `…:L92 _landau_F()` | unknown |
| 3 | $b\leftarrow\tfrac12\big(b-\cos3\delta^*\,w_6e_*^3\big)$ iterated, $\cos3\delta^*=$ `cos3_delta_data` $=0.785874$ | fixes $b$ so the grid minimum sits at the data angle ($r=-1,u=w_6=1$) | `…:L119–L123 eg_condensate_gap()` | unknown |
| 4 | $H=\begin{pmatrix}F_{ee}&F_{e\delta}\\F_{e\delta}&F_{\delta\delta}/e_*^2\end{pmatrix}$ (finite differences, $h=10^{-4}$); $m^2=\operatorname{eig}H$ | amplitude/angular mode curvatures | `…:L127–L133` | unknown |
| 5 | $\rho=\rho_c/(1+(s/r_s)^2)^{3/2}$; $v=\sqrt{GM(<r)/r}$, $G=4.30091\times10^{-6}$ kpc (km/s)²/M☉ | cored clump rotation curve vs homogeneous $M\propto r^3$ | `…:L188–L191 clustering_test()` | unknown |
| 6 | $\sigma/m=\lambda_6^2\times10^{-2}$ cm²/g, $\lambda_6=0.05$; F69 channel $\sigma/m=50$ (set by hand) | Bullet-Cluster proxy | `…:L218–L219 collisionless_proxy()` | unknown |

**Inputs → outputs:** none → per-channel verdicts. Channel A ($E_g$) is "unified dark sector". Channel B (F69 photon, gap set to $0$ by hand, L148) is excluded. **Depends on:** cos3_delta_data (F93/F95, `quantitative`, empirical); F93 functional (06a-particles-derivations-baryons.md § eg_sextic). **Flags:**
- ⚠ DOC/CODE MISMATCH: the Part-4 comment (L211) gives $\sigma/m\sim\lambda_6^2/m^3$. The code (L218) has no mass dependence and uses a bare $10^{-2}$ factor.
- $\lambda_6=0.05$ is illustrative. It disagrees with the registered $\lambda_6=0.243$ (key decision 7, F234).
- Later forks overturn the $E_g$ DM identification: F198 (under-production), F199b (instability) and F266/F237.

---

### `engine/forks/gravity/gr_fork_F198_angular_misalignment.py` — ALP misalignment + WIMP freeze-out for the $E_g$ modes
**Status:** fork_live · test-only · **Findings:** F198 · **Lattice:** n/a · **Law:** n/a · **Units:** natural (GeV)

**Does:** runs the standard constant-mass misalignment relic for the $E_g$ angular mode and a dimensional freeze-out estimate for the amplitude mode.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $H=1.66\sqrt{g_*}\,T^2/M_\text{Pl}$ | radiation-era Hubble | `gr_fork_F198_angular_misalignment.py:L47 H_rad()` | unknown |
| 2 | $3H(T_\text{osc})=m_a\Rightarrow T_\text{osc}=\sqrt{m_aM_\text{Pl}/(3\cdot1.66\sqrt{g_*})}$ | oscillation onset | `…:L53 T_osc()` | unknown |
| 3 | $s=\tfrac{2\pi^2}{45}g_*T^3,\ n/s=\tfrac12m_af^2\theta_i^2/s,\ \Omega h^2=m_a(n/s)s_0/(\rho_c/h^2)\ \propto m_a^{1/2}f^2\theta_i^2$ | misalignment relic | `…:L61–L64 omega_h2_misalignment()` | unknown |
| 4 | $f_\text{req}=\sqrt{0.12/\Omega(f{=}1)}$; $m_\text{req}=(0.12/\Omega(m{=}1))^2$ | contour inversions | `…:L77, L84` | unknown |
| 5 | $\langle\sigma v\rangle=g^4/(16\pi m^2)$; $\Omega h^2=0.12\cdot3\times10^{-26}/\langle\sigma v\rangle_{\text{cm}^3/\text{s}}$ | WIMP freeze-out | `…:L95–L97 omega_h2_freezeout()` | unknown |
| 6 | $m_\text{light}=\sqrt{\lambda_6}\cdot10^{-3}\cdot f$, $\lambda_6=0.05,\ f=123.11$ GeV | "natural" light mode | `…:L120 run()` | unknown |

**Inputs → outputs:** none → scaling check, contour, verdict: misalignment under-produces and the amplitude mode reaches the WIMP window. **Depends on:** nothing from casim. All constants ($M_\text{Pl}$, $s_0$, $\rho_c/h^2$, $g_*=80$) are inline. **Flags:** the $10^{-3}$ factor and $\lambda_6=0.05$ at L120 are arbitrary illustrations. The amplitude-mode route is closed by the F199 fork (instability).

---

### `engine/forks/gravity/gr_fork_F199_amplitude_mode_stability.py` — $E_g$ amplitude mode decays to leptons (finding now **F199b**)
**Status:** fork_live · test-only · **Findings (registry):** F199 — see Flags · **Lattice:** n/a · **Law:** n/a · **Units:** natural (GeV, s)

**Does:** assumes a Yukawa coupling $g_\ell=m_\ell/f$ for the $E_g$ amplitude mode and computes its lepton-pair width and lifetime against the age of the Universe.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $m_H=\sin(2\arcsin m_c)=2m_c\sqrt{1-m_c^2}$ | F73 composite-mass law (defined, not called by `run`) | `gr_fork_F199_amplitude_mode_stability.py:L54 f73_composite_mass()` | unknown |
| 2 | $\tau_H=\hbar/\Gamma_H$ | observed Higgs lifetime | `…:L59 higgs_mode()` | unknown |
| 3 | $\Gamma_S=\sum_\ell\frac{(m_\ell/f)^2m_S}{8\pi}\big(1-4m_\ell^2/m_S^2\big)^{3/2}$, $f=123.11$ GeV | scalar → $\ell^+\ell^-$ width | `…:L77–L81 scalar_to_leptons_width()` | unknown |
| 4 | $\tau=\hbar/\Gamma_S$; $\log_{10}(t_0/\tau)$ | stability vs age | `…:L91, L97 eg_amplitude_mode()` | unknown |
| 5 | $m_a=\sqrt{\lambda_6}\cdot27$ MeV | illustrative light angular mode | `…:L106 angular_mode_decay()` | unknown |

**Inputs → outputs:** none → lifetime of about $10^{-21}$ s, far below cosmological; the verdict is that the $E_g$ sector has no stable relic. **Depends on:** nothing imported; PDG masses are inline (registered as `runtime` sites in constants/geometry.py). **Flags:**
- Finding-number collision resolved on 2026-07-31 (`docs/design/finding-numbers.yaml`): this topic is now **F199b**. `findings/F199-*` is the angular self-duality posit. The registry `findings: F199` and the module filename are stale.
- `f73_composite_mass` is dead code within the fork.

---

### `engine/forks/gravity/gr_fork_F200_sterile_neutrino_dm.py` — keV sterile $\nu_R$ as dark matter (finding now **F266**)
**Status:** fork_live · test-only · **Findings (registry):** F200 — see Flags · **Lattice:** n/a · **Law:** n/a · **Units:** natural (GeV, s)

**Does:** computes lifetimes, the Dodelson–Widrow abundance and the X-ray mixing bound for a 7.1 keV sterile neutrino (the F47 $\nu_R$, $Y=0$).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Gamma_{3\nu}=G_F^2m_s^5\sin^22\theta/(768\pi^3)$ | $\nu_s\to3\nu$ | `gr_fork_F200_sterile_neutrino_dm.py:L59 decay_width_3nu()` | unknown |
| 2 | $\Gamma_\gamma=\frac{9\alpha}{1024\pi^4}G_F^2\sin^22\theta\,m_s^5$ | radiative $\nu_s\to\nu\gamma$ (X-ray line) | `…:L65 decay_width_gamma()` | unknown |
| 3 | $\tau=\hbar/(\Gamma_{3\nu}+\Gamma_\gamma)$ | lifetime | `…:L70 lifetime_s()` | unknown |
| 4 | $\sin^22\theta=4m_\nu/m_s$ | single-flavour see-saw mixing | `…:L77 naive_seesaw_mixing()` | unknown |
| 5 | $\Omega h^2=0.3\,(\sin^22\theta/10^{-10})(m_s/100\,\text{keV})^2$ | DW abundance fit | `…:L84 dw_abundance()` | unknown |
| 6 | $\sin^22\theta_\text{max}=3\times10^{-7}(\text{keV}/m_s)^5$ | X-ray bound (calibrated) | `…:L91 xray_bound()` | unknown |
| 7 | $\sin^22\theta_\text{res}=5\times10^{-12}$ | resonant benchmark (input) | `…:L107 run()` | unknown |

**Inputs → outputs:** none → benchmarks. Spot-check at the resonant point: $\tau=1.26\times10^{27}$ s, $\tau/t_0\approx2.9\times10^9$. **Depends on:** none (all inline). **Flags:**
- Finding-number collision resolved by moving the topic to **F266** (finding-numbers.yaml). The registry `findings: F200` is stale.
- ⚠ DOC/CODE MISMATCH: the `decay_width_gamma` docstring (L63) says $\Gamma_\gamma/\Gamma_{3\nu}\approx1/128$. The coded coefficients give $27\alpha/(4\pi)\approx1/64$ (computed 0.01568), which is a factor 2.
- ⚠ DOC/CODE MISMATCH: the verdict text (L166) says "tau ~ 1e25-26 s, ~8 orders". The code gives $1.26\times10^{27}$ s (~9.5 orders), in line with the L137 note.
- The keV-sterile-as-100%-DM route is later excluded by F237.

---

### `engine/forks/gravity/gr_fork_F201_kev_from_eg_texture.py` — $Z_3$/$E_g$ texture node for a light sterile
**Status:** fork_live · test-only · **Findings:** F201 · **Lattice:** n/a · **Law:** n/a · **Units:** GeV

**Does:** applies the Koide-form $Z_3$ texture to $M_R$ and finds the angle near the cancellation node that gives $M_1/M_3=10^{-6}$ (keV/GeV).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sqrt{m_a}/M_0=1+\sqrt2\cos(\delta+2\pi a/3),\ a=0,1,2$ | $Z_3$ texture | `gr_fork_F201_kev_from_eg_texture.py:L42 z3_sqrt_masses()` | unknown |
| 2 | $m_a=M_0^2(\ldots)^2$ (sign-folded) | eigenvalue magnitudes | `…:L48 masses_from_texture()` | unknown |
| 3 | $1+\sqrt2\cos\phi=0\Rightarrow\phi=\arccos(-1/\sqrt2)=135°$ | cancellation node | `…:L68 node_angle_deg()` | unknown |
| 4 | $\delta_\nu=\arg\min\lvert\log_{10}(M_\text{min}/M_\text{max})-\log_{10}10^{-6}\rvert$ over node $\pm5°$ (200001 pts) | tuning angle | `…:L86–L93 find_delta_for_ratio()` | unknown |
| 5 | $\delta_e=12.7328°$ reproduces $m_e:m_\mu:m_\tau$ | charged-lepton check | `…:L53–L57 charged_lepton_check()` | unknown |

**Inputs → outputs:** $M_{R0}=1$ GeV → $\delta_\nu\approx134.86°$, $M_1\approx$ keV. **Depends on:** none imported. **Flags:**
- `DELTA_E_DEG = 12.7328` (L35) is an unregistered literal. It is the data angle, not the founding $\delta^*=2/9$ rad $=12.7324°$ (key decision 7, `delta_star`). A near-coincident literal is not imported.
- The PDG lepton masses are registered as `runtime` sites.

---

### `engine/forks/gravity/gr_fork_F202_leptogenesis_sakharov.py` — Sakharov-condition checklist
**Status:** fork_live · test-only · **Findings:** F202 · **Lattice:** n/a · **Law:** n/a · **Units:** $n/s$

**Does:** counts CP phases and records the three Sakharov conditions as booleans. It is a checklist, not a computation; F364 replaces it with a Boltzmann number.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $N_\text{Dirac}=(n-1)(n-2)/2,\ N_\text{Maj}=n-1$ ($n=3$: 1+2) | physical CP phases | `gr_fork_F202_leptogenesis_sakharov.py:L53–L54 cp_phase_count()` | unknown |
| 2 | $\Delta L/s\,/\,Y_B=10^{-4}/8.7\times10^{-11}$ | required lepton-to-baryon asymmetry ratio | `…:L87 asymmetry_reach()` | unknown |

**Inputs → outputs:** none → `all_sakharov_met`. **Depends on:** none. **Flags:** every condition's `met: True` is hard-coded (L63–L80). Nothing is evaluated.

---

### `engine/forks/gravity/gr_fork_F203_dark_sector_falsifiers.py` — six-test dark-sector falsifier battery
**Status:** fork_live · test-only · **Findings:** F203 · **Lattice:** n/a · **Law:** n/a · **Units:** SI + GeV

**Does:** states a prediction and a data comparison for each of T1–T6. Only a few numbers are computed.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Gamma_\gamma=\frac{9\alpha}{1024\pi^4}G_F^2\sin^22\theta\,m_s^5/\hbar$ [s⁻¹] | T1 line rate (same formula as the F200 fork) | `gr_fork_F203_dark_sector_falsifiers.py:L67–L68 radiative_decay_rate_s()` | unknown |
| 2 | $E_\gamma=m_s/2$; margin $=10^{-27}/\Gamma_\gamma$ | T1 line and XRISM headroom | `…:L73–L74, L84 t1_xray_line()` | unknown |
| 3 | $\lambda_\text{fs}=0.3\,\text{Mpc}/(m_s/\text{keV})$ | T2 free-streaming | `…:L128 free_streaming_scale_mpc()` | unknown |
| 4 | $a_0=cH_0/6$, $H_0=67.4$ | T6 MOND-scale coincidence | `…:L294 t6_a0_coincidence()` | unknown |

**Inputs → outputs:** none → six-test dict. Spot-check: $\Gamma_\gamma(7.1\,\text{keV})=1.23\times10^{-29}$ s⁻¹, about 1.9 dex under the limit. **Depends on:** c_SI (CODATA). **Flags:**
- Every `status` string (T1–T6) is a hard-coded literal, not derived from the margins (e.g. L108, L163, L210). The summary count only tallies these literals.
- F205 later replaces T1/T2 with Boltzmann numbers, and F237 excludes the keV sterile.

---

### `engine/forks/gravity/gr_fork_F216_massive_spin2.py` — does induced gravity admit a massive spin-2 mode?
**Status:** fork_unclaimed · unreferenced · **Findings:** F216 · **Lattice:** n/a (continuum little-group algebra) · **Law:** n/a · **Units:** SI + lattice symbols

**Does:** counts graviton polarisations, posits the induced self-energy $\Pi\propto Q^2$, and runs dark-matter screens for a massive spin-2 bound state. **Runs at import and writes `test-results/F216_massive_spin2.json` (no `__main__` guard).**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $D(D-3)/2=2$ at $D=4$; $e_+=(\hat x\hat x-\hat y\hat y)/\sqrt2,\ e_\times=(\hat x\hat y+\hat y\hat x)/\sqrt2$ | massless TT dof on-axis | `gr_fork_F216_massive_spin2.py:L62–L66` | unknown |
| 2 | dof $=5$; $T_{m}$ from $\operatorname{sym}(e_\pm\otimes e_\pm)$, $m{=}0$: $\operatorname{diag}(-1,-1,2)/\sqrt6$ | massive spin-2 basis, helicity 0 = breathing | `…:L82, L85–L97 sph2()` | unknown |
| 3 | $m_\text{est}=\arg(T'_{ij}/T_{ij})/\theta$, $T'=R_z(\theta)TR_z^T$ | $J_z$ eigenvalue estimate | `…:L105–L112 jz_eigenvalue()` | unknown |
| 4 | $\Pi=A\,Q^2,\ Q^2=c_\text{lat}^2\lvert q\rvert^2-q_0^2$ ⇒ $\Pi(0)=0$, pole $q_0=\pm c_\text{lat}\lvert q\rvert$ | "graviton exactly massless" (sympy) | `…:L149–L154` | unknown |
| 5 | $m_g^2/\Lambda^2\to b^{-n}m_g^2/\Lambda^2$, $b=2,n=2$, 60 steps | LIV mass irrelevant under F130 block-spin | `…:L168` | unknown |
| 6 | $w(\kappa)=\kappa^2/(3(\kappa^2+1))$, $\kappa=c k/\mu$ | EoS of a massive mode | `…:L182 w_of_kappa()` | unknown |
| 7 | $\sigma/m=\pi(2Gm/v^2)^2/m$ (×10 → cm²/g), $v=10^6$ m/s | gravitational self-scattering | `…:L199–L203 sigma_over_m()` | unknown |
| 8 | $m=\hbar c^2/(Lv\,\text{eV})$, $L=1$ kpc, $v=200$ km/s | fuzzy-DM floor | `…:L222–L223 mass_for_lambda()` | unknown |

**Inputs → outputs:** none → 6 checks + JSON. **Depends on:** c_lat (F26, exact), G_CODATA, c_SI, hbar_SI. **Flags:**
- Import-time physics and JSON write (CLAUDE.md §5).
- Check B1 posits $\Pi=A_\text{loop}Q^2$ (L150) and then "verifies" that $\Pi(0)=0$, which is circular. F180-C and F248-E are the actual evidence.
- The dof formula at L80 is dead (overwritten by the hard-coded `massive_dof = 5`, L82).

---

### `engine/forks/gravity/gr_fork_F223_spin2_binding_relic.py` — graviton–graviton $J=2$ geon binding and relic
**Status:** fork_unclaimed · unreferenced · **Findings:** F223 · **Lattice:** n/a (1-D radial finite-difference grid) · **Law:** n/a · **Units:** natural ($\hbar=c=1$) + SI/GeV

**Does:** solves the $L=2$ Coulomb problem in the derived $V=-\alpha_g/r$, sets the geon mass at $\sqrt N M_\text{Pl}$, gives the $\nu_R\nu_R$ no-go and the CGPP relic suppression. **Runs at import and writes JSON (no `__main__` guard).**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $-\tfrac1{2m}u''+\big[\tfrac{L(L+1)}{2mr^2}-\tfrac{\alpha}{r}\big]u=Eu$; 3-point FD, shifted inverse iteration with Thomas solve | $D$-wave ground energy | `gr_fork_F223_spin2_binding_relic.py:L113–L130 radial_coulomb_ground()` | machine (inv 252; grid-limited) |
| 2 | $E_3=-m\alpha^2/(2n^2)$, $n=L+1=3$ ⇒ $-1/18$ | analytic target | `…:L136` | unknown |
| 3 | $E_b/m=(m/M_\text{Pl})^4/36$; self-binding at $36^{1/4}M_\text{Pl}$ | fractional binding with $\alpha_g=(m/M_\text{Pl})^2$ | `…:L152, L154 frac_binding()` | quantitative (inv 253) |
| 4 | $\mu=\sqrt N\,M_\text{Pl}$, $N=2$ | geon virial mass | `…:L157–L160 geon_mass_over_Mpl()` | quantitative (inv 253) |
| 5 | $\alpha_g=(M_R/M_\text{Pl})^2$; max frac binding over $M_R\in[\text{keV},10^{14}\text{ GeV}]$ | $\nu_R\nu_R$ no-go | `…:L185–L189` | exact (inv 254) |
| 6 | $\log_{10}\lvert\beta\rvert^2=-2\pi\mu/(H\ln10)$; $\Omega h^2_\text{pre}=\frac{\mu}{3.64\times10^{-9}}\frac{\alpha_\text{eff}}{32\pi^3}\frac{HT_\text{RH}}{M_\text{Pl}^2}$ | CGPP relic band | `…:L204, L209, L230–L233` | quantitative (inv 254) |
| 7 | $\lambda_{dB}=\hbar/(\mu v)$; $\sigma/m=\pi(2G\mu/v^2)^2/\mu$ | DM screens | `…:L252, L259–L260` | unknown |

**Inputs → outputs:** none → 6 checks + JSON. **Depends on:** G_CODATA, c_SI, hbar_SI (CODATA; $M_\text{Pl}=\sqrt{\hbar c/G}$ computed, not F79's lattice $G$). **Flags:**
- Import-time physics and JSON write.
- ⚠ DOC/CODE MISMATCH (minor): the S1 comment L79 says "np.linalg.eigh on a real symmetric tridiagonal", but the code uses hand-rolled shifted inverse iteration (L104–L130).
- The prose says "two gravitons" while the check uses a massive reduced mass $m_\text{red}=1$ (dimensionless test).

---

### `engine/forks/gravity/gr_fork_F228_geon_production_stability.py` — geon = one-cell Planck remnant; production channels
**Status:** fork_unclaimed · unreferenced · **Findings:** F228 · **Lattice:** n/a (uses the F107 cell area) · **Law:** n/a · **Units:** natural GeV + SI

**Does:** stability through the one-cell horizon remnant, the PBH-remnant abundance band, and a validated Bogoliubov integrator applied to exponentially suppressed channels. **Runs at import and writes JSON.**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $N_\text{cells}=A/a^2=16\pi(M/M_\text{Pl})^2/(8\pi\sqrt3)=2(M/M_\text{Pl})^2/\sqrt3$ | horizon cells (F190 + F107 $a^2=8\pi\sqrt3\,\ell_P^2$) | `gr_fork_F228_geon_production_stability.py:L154 N_cells()` | exact (inv 255) |
| 2 | $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}$ | $N=1$ remnant mass | `…:L155` | exact (inv 255) |
| 3 | $T_\text{form}=\sqrt{\gamma M_\text{Pl}^3/(3.32\sqrt{g_*}M_\text{form})}$; $\beta=0.12/\big[M_\text{rem}\tfrac34\tfrac{T_\text{form}}{M_\text{form}}\tfrac{s_0}{\rho_c/h^2}\big]\ \propto M_\text{form}^{3/2}$ | PBH fraction for $\Omega h^2=0.12$ | `…:L195 T_form_GeV()`, L200–L201 `beta_required()` | quantitative (inv 257) |
| 4 | $\tau_\text{evap}=4.35\times10^{17}\,\text{s}\,(M/5.1\times10^{14}\,\text{g})^3$ | pre-BBN check | `…:L205 tau_evap_s()` | unknown |
| 5 | $\lvert\beta\rvert^2=\sinh^2(\pi\omega_-/\rho)/[\sinh(\pi\omega_\text{in}/\rho)\sinh(\pi\omega_\text{out}/\rho)]$ for $\omega^2=A+B\tanh\rho\eta$ | Bernard–Duncan closed form | `…:L234–L236 bernard_duncan_beta2()` | machine (inv 256; closed form used as reference) |
| 6 | $\chi''+\omega^2\chi=0$ as real RK4 on $(u,v,p,q)$; $\lvert\beta\rvert^2=\lvert\chi'+i\omega_\text{out}\chi\rvert^2/2\omega_\text{out}$ | hand-rolled Bogoliubov integrator (Re/Im tracked by hand) | `…:L248–L268 integrate_bogoliubov()` | machine (inv 256) |
| 7 | $\log_{10}\text{supp}=-2\pi\mu/H\,/\ln10;\ -2\mu/T_\text{RH}/\ln10;\ -\mu/T/\ln10$ | CGPP / UV freeze-in / coalescence | `…:L278, L292, L304` | quantitative (inv 257) |
| 8 | $\Omega_c=0.12/0.674^2$ | fits inside $\Omega_m=0.3153$ | `…:L338` | unknown |
| 9 | $\mu_\text{geon}/M_\text{rem}=\sqrt2/(\sqrt3/2)^{1/2}\approx1.52$ | "same object" | `…:L353` | unknown |

**Inputs → outputs:** none → 9 checks + JSON. Spot-check (formula re-run in scratch): $\beta=6.6\times10^{-15},\,6.6\times10^{-12},\,6.6\times10^{-9}$ for $M_\text{form}=10^4,10^6,10^8$ g. **Depends on:** G_CODATA, c_SI, hbar_SI; `casim.engine.interactions.cosmology.lcdm_summary()` (07a-interactions-cosmology.md), with a hard-coded fallback. **Flags:**
- Import-time physics and JSON write.
- ⚠ DOC/CODE MISMATCH: the P_a docstring (L51, "β~1e-4..1e-2") and `summary.viable_production` (L387) disagree with the computed β ($10^{-14.2}$…$10^{-8.2}$). The header L30 and inventory row 257 agree with the code.
- The code gate for the integrator is rel $<5\times10^{-3}$ (L273), while the inventory row 256 quotes $10^{-12}$.
- Inventory rows 255–257 are labelled "F226".

---

### `engine/forks/gravity/gr_fork_F238_geon_relic_abundance.py` — PBH fraction β is a free cosmological input
**Status:** fork_unclaimed · unreferenced · **Findings:** F238 · **Lattice:** n/a · **Law:** n/a · **Units:** natural GeV

**Does:** inverts Press–Schechter to get the required small-scale $\sigma$, shows that a scale-invariant spectrum under-produces by about $2\times10^7$ orders, and scans the repo for an inflaton sector. **Runs at import and writes JSON.**

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\operatorname{erfc}x\approx t(a_1+a_2t+\dots+a_5t^4)e^{-x^2}$, $t=1/(1+0.3275911x)$ (A&S 7.1.26) | hand-rolled erfc (≈1 % relative error at $x\sim5.5$, checked) | `gr_fork_F238_geon_relic_abundance.py:L112–L115 erfc_real()` | unknown |
| 2 | $\log_{10}\operatorname{erfc}x\approx[-x^2-\ln(x\sqrt\pi)+\ln(1-1/2x^2)]/\ln10$ | large-$x$ tail | `…:L119–L120 log10_erfc_asymptotic()` | unknown |
| 3 | $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}$; $\beta_\text{req}(M_\text{form})$ | copied from F228 | `…:L135, L141–L146` | unknown (F228 copy; cf. inv 255/257) |
| 4 | $\beta=\tfrac12\operatorname{erfc}\big(\delta_c/\sqrt2\sigma\big)\Rightarrow\sigma=\delta_c/(\sqrt2\,\operatorname{erfc}^{-1}(2\beta))$, $\delta_c=0.45$ | required PBH-scale amplitude | `…:L175–L176` | unknown |
| 5 | $x_\text{HZ}=\delta_c/(\sqrt2\sqrt{A_s})\approx6944$; $\log_{10}\Omega_\text{HZ}=\log_{10}\beta_\text{HZ}-\log_{10}\beta_\text{req}+\log_{10}0.12$ | scale-invariant no-go | `…:L196–L201` | unknown |
| 6 | boost $=(\sigma_\text{req}/\sigma_\text{CMB})^2$; $n_s-1=\log_{10}\text{boost}/18$ | required blue tilt | `…:L216–L224` | unknown |

**Inputs → outputs:** none → 7 checks + JSON. **Depends on:** G_CODATA, c_SI, hbar_SI. The A&S coefficient 1.453152027 is a registered `coincidence` MeasuredConstant (not W*). **Flags:**
- Import-time physics and JSON write.
- ⚠ DOC/CODE MISMATCH: the header (L23) writes $\beta=\operatorname{erfc}(\ldots)$, while the code uses $\tfrac12\operatorname{erfc}$ (L168, L175).
- Check S6 (L262–L273) is a filesystem keyword search of `findings/` and `engine/interactions/`. Its result depends on repo state and is not physics.

---

### `engine/forks/gravity/gr_fork_F248_tt_graviton_bcc.py` — explicit TT graviton on the BCC lattice
**Status:** fork_unclaimed · unreferenced (has test `test_F248_tt_graviton_bcc.py`) · **Findings:** F248 · **Lattice:** BCC (Eq. 15, $k_i/\sqrt3$) · **Law:** even $\Omega=\omega^+(k/2)+\omega^-(k/2)$; the check-E loop uses the single chiral $\omega^+$ · **Units:** lattice

**Does:** builds the TT basis for any $\hat k$, the spin-2 projector and its common pole, the non-birefringence of the even law, a spectral TT packet, and an explicit BCC tensor bubble.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^\pm=c_xc_yc_z\pm s_xs_ys_z$, $c_i=\cos(k_i/\sqrt3)$; $\omega^\pm=\arccos u^\pm$ | BCC branches | `gr_fork_F248_tt_graviton_bcc.py:L97, L104, L109, L114` | unknown |
| 2 | $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$ | graviton/photon even law (odd $s_xs_ys_z$ term cancels) | `…:L130 graviton_even_dispersion()` | exact (inv F248-C) |
| 3 | $e_+=(e_1e_1-e_2e_2)/\sqrt2,\ e_\times=(e_1e_2+e_2e_1)/\sqrt2$, $e_{1,2}\perp\hat k$; $R\,e_{\pm2}R^T=e^{\pm2i\theta}e_{\pm2}$ | TT basis + helicity ±2 | `…:L157–L158 tt_polarizations()`, L188–L194 | machine (inv F248-A) |
| 4 | $\Lambda_{ij,kl}=\tfrac12(P_{ik}P_{jl}+P_{il}P_{jk})-\tfrac12P_{ij}P_{kl}$, $P=1-\hat k\hat k$ | spin-2 TT projector (idempotent; fixes $e_{+,\times}$; kills trace and longitudinal) | `…:L232 spin2_tt_projector()` | machine (inv F248-B) |
| 5 | $f_2=A\,Q^2,\ Q^2=\tfrac13\lvert q\rvert^2-q_0^2$ ⇒ $q_0=\lvert q\rvert/\sqrt3$ | common pole (sympy) | `…:L269–L276 check_B_projector_and_pole()` | exact (inv F248-B) |
| 6 | $\Omega(k\hat n)/k\to1/\sqrt3$ at $k=10^{-3}$ for [100],[110],[111],random; [111] deviation ratio $d(0.04)/d(0.02)\approx4$ | isotropic slope + $O(k^2)$ anisotropy | `…:L307, L322, L330–L332 check_C_…()` | exact (inv F248-C) |
| 7 | $h(x,t)=\mathcal F^{-1}[\text{env}(k)\,e^{-i\Omega(k_x)t}]$; centroid speed vs $v_g=d\Omega/dk_x$ | one-way TT packet along [100] (on-axis $\Omega=\lvert k_x\rvert/\sqrt3$ exactly) | `…:L394–L401 check_D_realspace_bcc_wavefront()` | quantitative (inv F248-D/E) |
| 8 | $\Pi_{ij,kl}(q)=\langle V_{ij}V_{kl}\,G(p)G(p+q)\rangle_\text{BZ}$, $V_{ij}=\tfrac12(p_i(p+q)_j+p_j(p+q)_i)$, $G=1/(\omega^{+2}+m^2)$, $m=0.35$, $n=28$ | explicit static tensor bubble; $e^T\Pi e$ helicity-degenerate, fit $a+bq^2$ | `…:L447–L464 _bcc_constituent_bubble_tensor()`, fit L497–L501 | quantitative (inv F248-D/E) |

**Inputs → outputs:** none → 5 checks (JSON only under `__main__`). **Depends on:** c_lat (F26); `casim.numerics.fft` (L395); BCC branches reimplemented from 03-lattice.md § `bcc.py`. **Flags:**
- ⚠ DOC/CODE MISMATCH: the module docstring (L26, L43) states the even law as $\Omega=2\omega_+(k/2)$. The code (L130) and its own function docstring (L128: "2*omega_+(k/2) … is NOT the paired photon law") use $\omega^+(k/2)+\omega^-(k/2)$.
- ⚠ DOC/CODE MISMATCH: the docstring (L50) says check D evolves $h(k,0)\cos(\Omega t)$. The code (L394) evolves a one-way $e^{-i\Omega t}$ packet.
- Check C's birefringence measure is `abs(Om - Om)` (L320), which is identically 0 (tautological).
- Check D applies the same scalar density to both polarisations (L396), so the polarisation speed difference is 0 by construction.
- Check E's constituent loop uses only the chiral $\omega^+$ branch.

---

### `engine/forks/darkmatter/__init__.py` — package docstring
**Status:** not in module registry (package init) · **Findings:** — · plumbing: a docstring that says forks are recorded alternatives, with status carried in the migration manifest and registry. No code. **Flags:** none.

---

### `engine/forks/darkmatter/dm_fork_F205_sterile_qke_boltzmann.py` — momentum-resolved keV-sterile QKE production
**Status:** fork_live · test-only · **Findings:** F205 · **Lattice:** n/a · **Law:** n/a · **Units:** natural (GeV), cgs for $s_0$, $\rho_c$

**Does:** a one-generation Boltzmann/QKE active→sterile production integral (Dodelson–Widrow for $L=0$, Shi–Fuller resonant for $L>0$). It gives $\Omega_sh^2$, the frozen spectrum $\langle\varepsilon\rangle$, and maps the result onto X-ray and Lyman-α bounds.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g_*(T),g_{*s}(T)$ log-log interpolation of a 14-point table; $H=1.66\sqrt{g_*}T^2/M_\text{Pl}$ | cosmology background | `dm_fork_F205_sterile_qke_boltzmann.py:L92, L97, L102` | unknown |
| 2 | $T_\text{peak}=0.133\,\text{GeV}\,(m_s/\text{keV})^{1/3}$; grid $[0.02,30]\,T_\text{peak}$ | temperature window | `…:L116–L119 _T_grid()` | unknown |
| 3 | $\Delta=m_s^2/2p,\ \Gamma_a=d\,G_F^2pT^4\ (d{=}1.27),\ V_T=-b\,G_F^2pT^4\ (b{=}10.88),\ V_D=\sqrt2G_F\frac{2\zeta_3}{\pi^2}T^3L$ | oscillation, damping, thermal and asymmetry potentials | `…:L136–L140 production()` | unknown |
| 4 | $\langle\sin^22\theta_M\rangle=\dfrac{\Delta^2\sin^22\theta}{\Delta^2\sin^22\theta+(\Delta-V)^2+(\Gamma_a/2)^2}$ ($\cos2\theta\approx1$) | in-medium mixing | `…:L142–L144` | unknown |
| 5 | $\dot f_s=\tfrac14\Gamma_a\langle\sin^22\theta_M\rangle f_\text{FD}(\varepsilon)$ | production rate | `…:L146` | unknown |
| 6 | $Y_s=\int dT\,\frac{45}{4\pi^4g_{*s}}\frac{\int\varepsilon^2\dot f_s\,d\varepsilon}{HT}$; $\Omega h^2=m_sY_ss_0/(\rho_c/h^2)$ | relic yield | `…:L149–L157` | unknown |
| 7 | $f_s(\varepsilon)\propto\int\dot f_s/(HT)\,dT$; $\langle\varepsilon\rangle=\int\varepsilon^3f_s/\int\varepsilon^2f_s$ | frozen spectrum and coldness | `…:L163–L166` | unknown |
| 8 | $\sin^22\theta_\text{DM}=\sin^22\theta_\text{ref}\cdot0.12/\Omega(\sin^22\theta_\text{ref})$ | linear rescale (Ω linear in mixing) | `…:L177 mixing_for_omega()` | unknown |
| 9 | $\sin^22\theta_\text{max}=1.7\times10^{-11}(7.1\,\text{keV}/m_s)^5$ | aggregate X-ray bound | `…:L187 xray_bound()` | unknown |
| 10 | $m_\text{th}=(m_s/4.43\,\text{keV})^{3/4}(\omega_X/0.1225)^{1/4}\cdot\langle\varepsilon\rangle_\text{DW}/\langle\varepsilon\rangle$; floor $m_s\ge4.43\,(m_\text{bound}/\text{coldness}/(\omega_X/0.1225)^{1/4})^{4/3}$ | Viel thermal-equivalent mass and Lyman-α floor (bounds 5.3 / 3.5 keV) | `…:L205–L208, L216` | unknown |

**Inputs → outputs:** none → DW/resonant scans, floors, verdict (`_finalize`). **Depends on:** none imported. The $2\zeta_3/\pi^2$ prefactor is a registered `coincidence` MeasuredConstant (vs $\lambda_6$). **Flags:**
- The module global `MEAN_EPS_NRP_REF` is mutated by `run()` (L231) and by the F237 fork. The comment at L220 says it is "filled at import", but it is filled in `run()`.
- The verdict text (L365, L373) hard-codes "2.5 dex" and "was order-of-magnitude" beside computed values.
- The keV sterile as 100 % DM is later excluded by F237. No supersessions.yaml entry.

---

### `engine/forks/darkmatter/dm_fork_F237_kev_sterile_resolution.py` — resonant + entropy-dilution attempt (exclusion)
**Status:** fork_live · test-only · **Findings:** F237 · **Lattice:** n/a · **Law:** n/a · **Units:** natural (GeV)

**Does:** adds late entropy dilution $S$ on top of the F205 solver. It shows the X-ray and Lyman-α levers move in opposite directions in $\log S$, so no $(m_s,L,S)$ point passes both. The hand-off is to the F223/F228 geon.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sin^22\theta_\text{need}=S\cdot\sin^22\theta_\text{undiluted}$; $\langle\varepsilon\rangle_\text{eff}=\langle\varepsilon\rangle/S^{1/3}$ | dilution scalings | `dm_fork_F237_kev_sterile_resolution.py:L96–L97 diluted_point()` | unknown |
| 2 | X-ray ok iff $\sin^22\theta\le$ bound; Lyα ok iff $m_s\ge$ floor$(\langle\varepsilon\rangle_\text{eff})$ | viability test on a 14×11 $(L,S)$ grid | `…:L99–L105, L120–L122` | unknown |
| 3 | best case: $\sin^22\theta=S\cdot$bound, $\langle\varepsilon\rangle=1.57/S^{1/3}$; X-ray cost $=\log_{10}S$ dex | "does a door exist" test | `…:L143–L147 best_case()` | unknown |
| 4 | $d\log\sin^22\theta/d\log S=+1$; $d\log m_\text{floor}/d\log S=-4/9$ | opposite-sign exponents | `…:L173–L178 scaling_exponents()` | unknown |
| 5 | $f_\text{max}=\min(1,\text{bound}/\sin^22\theta(L{=}2\times10^{-3}))$ | sub-dominant fraction | `…:L197 subdominant_fraction()` | unknown |

**Inputs → outputs:** none → grid counts, best case, verdict. **Depends on:** the F205 fork (all physics). **Flags:**
- The X-ray slope in `scaling_exponents` is tautological: `log_sin2 = np.log10(Ss)` (L173) fits the $+1$ that was put in.
- `me_cold = 1.57` (L130, L176) is a hard-coded copy of an F205 output.
- The module mutates `F205.MEAN_EPS_NRP_REF` (L77).

---

### `engine/forks/darkmatter/dm_fork_F364_baryogenesis_boltzmann.py` — resonant leptogenesis Boltzmann for $Y_B$
**Status:** live · standalone · spine · **Findings:** F364 F202 F201 F47 F53 F320 · **Registry exactness:** bracketed · **Lattice:** n/a · **Law:** n/a · **Units:** natural (GeV)

**Does:** Casas–Ibarra Dirac masses, the Pilaftsis–Underwood resonant CP asymmetry, and unflavoured vanilla-leptogenesis Boltzmann equations from $T_i=10^5$ GeV to $T_\text{sph}=131.7$ GeV. Heavy masses come from the F201 texture. It turns the F202 checklist into a number.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M_a=M_{R0}^2\lvert1+\sqrt2\cos(\delta_\nu+2\pi a/3)\rvert^2$, $\delta_\nu=134.86°$ | F201 texture heavy masses (spot: $M_1=5.99$ keV, $M_2=0.398$, $M_3=5.60$ GeV, split 1.73) | `dm_fork_F364_baryogenesis_boltzmann.py:L102, L107 f201_texture_masses()` | bracketed (reg) |
| 2 | $U_\text{PMNS}(\theta_{12},\theta_{23},\theta_{13},\delta)$ standard; $\hat U=U_{[:,2:3]}$, $m_1=0$ | light sector (global-fit inputs) | `…:L133–L142 pmns_matrix()` | bracketed (reg) |
| 3 | $M_D=i\,\hat U\,\sqrt{\hat m}\,R(\omega)\sqrt{M}$, $R=\begin{pmatrix}\cos\omega&\sin\omega\\-\sin\omega&\cos\omega\end{pmatrix}$, $\omega\in\mathbb C$ | Casas–Ibarra | `…:L151 casas_ibarra_MD()` | bracketed (reg) |
| 4 | $m_\nu=M_DM^{-1}M_D^T$; residual vs input masses | seesaw reproduction check | `…:L157–L160` | bracketed (reg) |
| 5 | $Y=\sqrt2M_D/v$, $\Gamma_I=(Y^\dagger Y)_{II}M_I/8\pi$; $\varepsilon_I=\dfrac{\operatorname{Im}[(Y^\dagger Y)_{IJ}^2]}{(Y^\dagger Y)_{II}(Y^\dagger Y)_{JJ}}\dfrac{(M_I^2-M_J^2)M_I\Gamma_J}{(M_I^2-M_J^2)^2+M_I^2\Gamma_J^2}$ | widths and regulated resonant CP asymmetry | `…:L169–L181 widths_and_epsilon()`; well-conditioned $M_3^2-M_2^2=M_2^2(2r+r^2)$ L193–L202 | bracketed (reg) |
| 6 | $\frac{dY_{N_I}}{dz}=-\frac{\Gamma_I}{Hz}\frac{K_1}{K_2}(Y_{N_I}-Y^\text{eq}_{N_I})$; $\frac{dY_{B-L}}{dz}=\sum_I\varepsilon_I\frac{\Gamma_I}{Hz}\frac{K_1}{K_2}(Y_{N_I}-Y^\text{eq})-\tfrac12\sum_I\frac{\Gamma_I}{Hz}\frac{K_1}{K_2}\frac{Y^\text{eq}_{N_I}}{Y^\text{eq}_\ell}Y_{B-L}$ in $u=\ln z$ (Radau) | Boltzmann system, freeze-in $Y_N(T_i)=0$ | `…:L247–L264 run_boltzmann()` | bracketed (reg) |
| 7 | $Y^\text{eq}_N=\frac{M^3}{\pi^2z}K_2(z)/s$ (UR limit $\tfrac34\frac{\zeta_3}{\pi^2}2T^3/s$); $Y^\text{eq}_\ell=\tfrac34\frac{\zeta_3}{\pi^2}6T^3/s$; $s=\tfrac{2\pi^2}{45}g_*T^3$ | equilibrium abundances | `…:L217, L226–L237` | bracketed (reg) |
| 8 | $Y_B=\tfrac{28}{79}Y_{B-L}$ | SM sphaleron conversion (inherited) | `…:L266` | bracketed (reg) |
| 9 | $\Gamma_\text{sph}/H=\kappa\,\alpha_W^5T^4/H$, $\alpha_W=\alpha/\sin^2\theta_W$, $\sin^2\theta_W=2/9$ | condition-1 rate | `…:L276–L278 sphaleron_rate_over_hubble()` | bracketed (reg) |

**Inputs → outputs:** none → CP-phase scan, splitting scan, verdict: the native split falls about 10–11 decades short, and a resonance window near $r\sim10^{-17}$ is needed. **Depends on:** `sin2_thetaW_onshell` $=2/9$ (F49/F138/F141/F231, exact; imported as a float); the F201 fork texture (re-implemented). **Flags:**
- It imports `scipy.special.kv` and `scipy.integrate.solve_ivp` directly (L72–L73), a D8 deviation acknowledged in the docstring.
- `live` status sits inside `forks/` (spine origin).
- The literal $\delta_\nu=134.86°$ gives $M_1=5.99$ keV, not the 5.6 keV "F201 landing" used by F203/F205/F237.
- `findings-index.md` says "no test record", but `tests/registry/forks.yaml:756` has `F364-baryogenesis-boltzmann`.

---

### `engine/forks/electroweak/__init__.py` — package docstring
**Status:** not in module registry · plumbing (docstring only). **Flags:** none.

---

### `engine/forks/electroweak/hypercharge_fork.py` — Higgs-free Majorana $\nu_R$ step + see-saw (staging area)
**Status:** fork_live · test-only · **Findings (registry):** none — code is F47 (docstring says "F43") · **Lattice:** n/a (per-cell mass steps, no kinetic) · **Law:** n/a · **Units:** lattice (dt)

**Does:** re-exports the promoted `casim.engine.gauge.hypercharge` primitives, and adds an anti-linear Majorana mass step, a Strang Dirac+Majorana step, the closed-form see-saw and an 8×8 BdG Hamiltonian.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\chi_u'=c_M\chi_u-is_M\chi_d^*,\ \chi_d'=c_M\chi_d+is_M\chi_u^*$, $c_M=\cos M_R\Delta t$ (from $i\dot\chi_u=M_R\chi_d^*,\ i\dot\chi_d=-M_R\chi_u^*$) | bare Majorana step (R-linear, norm-preserving) | `hypercharge_fork.py:L163–L164 mass_step_majorana_chi()` | unknown |
| 2 | $\eta'=c_D\eta+is_D\chi,\ \chi'=c_D\chi+is_D\eta$ (F27 sign, $U=I$) | Dirac sub-step | `…:L207–L210 mass_step_dirac_majorana_nu()` | unknown |
| 3 | $S(\Delta t)=\text{Maj}(\Delta t/2)\circ\text{Dirac}(\Delta t)\circ\text{Maj}(\Delta t/2)$ | Strang split | `…:L203–L213` | unknown |
| 4 | $M=\begin{pmatrix}0&M_D\\M_D&M_R\end{pmatrix}$; $\lambda_\pm=\tfrac12(M_R\pm\sqrt{M_R^2+4M_D^2})$, small root via Vieta $\lambda_-=-M_D^2/\lambda_+$ | see-saw eigenvalues | `…:L229, L257–L270 seesaw_eigenvalues()` | unknown |
| 5 | $m_\nu\approx M_D^2/M_R$ | leading see-saw | `…:L277` | unknown |
| 6 | $H_{02}=H_{13}=-M_D,\ H_{46}=H_{57}=+M_D,\ H_{27}=+M_R,\ H_{36}=-M_R$ (symmetric) on $(\eta_u,\eta_d,\chi_u,\chi_d,\text{c.c.})$ | BdG Hamiltonian (dt→0 of the step) | `…:L311–L320 bdg_hamiltonian_nu()`; spectrum L336 | unknown |

**Inputs → outputs:** complex spinor arrays / masses → updated spinors, eigenvalues. Spot-check at $M_D=1,M_R=100$: $\lambda=(-0.009999, 100.01)$; BdG gives $\pm0.009999,\pm100.01$, each doubly degenerate. **Depends on:** `casim.engine.gauge.hypercharge` (05c-gauge-photon-lpt-weak.md § hypercharge); registered hypercharge constants (Y_NU_R etc., electroweak.py sites). **Flags:**
- Stale finding number: the docstring labels the Majorana branch "F43". F43 is now the dynamical-gluon finding, and the Majorana/see-saw content is **F47** (`findings/F47-majorana-seesaw-higgs-free.md`). The registry `findings` field is empty.
- Complex numpy elementwise arithmetic with `np.conj` carries both Re and Im. There is no FFT and no `casim.numerics.chiral` routing (the D8 chiral hazard does not bite here).
- The M1–M6 tests named in the docstring live elsewhere, in the test registry (`tests/registry/gauge.yaml`).

---

### `engine/forks/gauge/__init__.py` — package docstring
**Status:** not in module registry · plumbing. **Flags:** none.

---

### `engine/forks/gauge/curl_fork_baseline_bcc.py` — BCC baseline wrapper for the curl-O(k) study
**Status:** fork_unclaimed · unreferenced · **Findings:** (F2, F10 cited in docstring; registry none) · **Lattice:** BCC (canonical) · **Law:** chiral single branch (sign ±) · **Units:** lattice

**Does:** a thin wrapper around 03-lattice.md § `bcc.py` (`_bcc_uvec`, `bcc_dispersion`, `bcc_unitary`) plus an eigen-decomposition.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U=\begin{pmatrix}U_{ff}&U_{fg}\\U_{gf}&U_{gg}\end{pmatrix}$, $U\psi_\pm=e^{\mp i\omega}\psi_\pm$, $\omega=-\arg\lambda_\text{max}$ | eigenmodes via `np.linalg.eig` | `curl_fork_baseline_bcc.py:L36–L41 eigenmodes()` | unknown |

**Inputs → outputs:** $k$ → $(\psi_+,\psi_-,\omega)$. **Depends on:** `lattice.bcc`; c_lat (F26). **Flags:** complex eigen-decomposition goes through `np.linalg.eig` (chiral-transform hazard; phases only, not re-verified here).

---

### `engine/forks/gauge/curl_fork_cubic.py` — simple-cubic Weyl QCA candidate (rejected)
**Status:** fork_unclaimed · unreferenced · **Findings:** (D1, F26 via MeasuredConstant) · **Lattice:** simple cubic (D1 reference, rejected candidate) · **Law:** single family · **Units:** lattice

**Does:** implements the naive cubic Weyl walk. It was built to test whether cubic geometry gives $c=1$ and fixes the curl residual. It gives $c=1$ at the cost of 8 doublers; the D1 decision kept BCC.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $s_i=\sin k_i$, $u=\cos\lvert s\rvert$, $\mathbf n=\mathbf s\,\sin\lvert s\rvert/\lvert s\rvert$ ($u^2+\lvert n\rvert^2=1$) | cubic unitary parameters | `curl_fork_cubic.py:L61–L68 uvec()` | unknown |
| 2 | $\omega=\lvert s\rvert=\sqrt{\sum\sin^2k_i}$ | dispersion ($\omega\approx\lvert k\rvert$ ⇒ $c=1$; zeros at $k_i\in\{0,\pi\}$) | `…:L74 dispersion()` | unknown |
| 3 | $U=u\,I-i\,\boldsymbol\sigma\cdot\mathbf n$ | one-tick unitary | `…:L79–L83 unitary()` | unknown |

**Inputs → outputs:** $k$ → $u,\mathbf n,\omega,U$. **Depends on:** none. `C_LAT = 1.0` is a registered `measured` MeasuredConstant (the quantity under test). **Flags:** rejected geometry (D1). Kept as a falsification record.

---

### `engine/forks/gauge/curl_fork_harness.py` — cross-geometry curl/c/doubler diagnostics
**Status:** fork_unclaimed · unreferenced · **Findings:** (F2 self-check; registry none) · **Lattice:** BCC vs simple cubic · **Law:** chiral single branch · **Units:** lattice
**SUPERSEDED (construction):** it tests the σ-bilinear *composite photon* (`gauge.bilinear.EM_bilinears`). F65–F69 exclude that construction for the photon (key decision 5; see 05a-gauge-actions-bilinear-colour.md § bilinear).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $(E,B)=\text{EM\_bilinears}(\psi_+,\psi_-,\mathbf n(k/2))$; after one tick $\psi\to\psi e^{-i\omega(k/2)}$; residual $\lVert\Delta E-i\,2\mathbf n\times B\rVert/(\lVert E\rVert+\lVert B\rVert)$, same for $B$ with $-i$ | composite-photon curl residual | `curl_fork_harness.py:L57–L70 curl_residual()` | unknown |
| 2 | $c=\omega(k\hat x)/k$, $c_\text{diag}=\omega(k\hat d)/k$ at $k=10^{-4}$ | emergent light speed | `…:L76–L78 emergent_c()` | unknown |
| 3 | $\omega(\text{diag})/\omega(\text{axis})$ at $k=0.1$ | isotropy | `…:L84–L87` | unknown |
| 4 | $\#\{\omega<10^{-9}\}$ on $N^3=12^3$ FFT grid | doubler count | `…:L93–L96 count_doublers()` | unknown |
| 5 | slope of $\log$ residual vs $\log k$; residual$/k\to1/\sqrt6$ (BCC self-check) | scaling exponent (F2) | `…:L99–L103, L137–L141` | unknown |

**Inputs → outputs:** none → per-geometry dict (JSON under `__main__`, dated). **Depends on:** `gauge.bilinear`; `casim.numerics.fft.fftfreq`; the two fork geometries above. **Flags:**
- SUPERSEDED photon construction (σ-bilinear, F65–F69).
- Stale docstring run path "python3 forks/curl_fork_harness.py" (L20).
- `CASIM` is first set (L28) and then overwritten (L31).

---

### `engine/forks/gauge/lgt_fork_A_mc.py` — Fork A: SU(3) Wilson lattice-gauge Monte-Carlo + Lüscher–Weisz
**Status:** fork_live · driven (2 ch) · **Findings (registry):** none; docstring/inventory F94 · **Lattice:** simple hypercubic $D=3,4$ (textbook Wilson; last axis Euclidean time) — **not** the model's BCC lattice · **Law:** n/a (Euclidean MC) · **Units:** lattice
**SUPERSEDED by F323/F265** — `S21-F94-hypercubic-action-not-the-model-lattice`: the ensemble samples a simple-hypercubic Wilson action whose composite construction leaves a $\langle111\rangle$ link axis free (F265). F94's confinement measurement is not the model's lattice.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U_P=U_\mu(x)U_\nu(x+\hat\mu)U_\mu^\dagger(x+\hat\nu)U_\nu^\dagger(x)$ | plaquette | `lgt_fork_A_mc.py:L99 plaquette()` | unknown |
| 2 | $\langle P\rangle=\langle\tfrac13\operatorname{Re}\operatorname{Tr}U_P\rangle$; $S=\beta\sum_P(1-\tfrac13\operatorname{Re}\operatorname{Tr}U_P)$ | mean plaquette, Wilson action | `…:L110–L112, L122–L123` | unknown |
| 3 | $R_\mu=\sum_{\nu\ne\mu}[U_\nu(x{+}\mu)U_\mu^\dagger(x{+}\nu)U_\nu^\dagger(x)+U_\nu^\dagger(x{+}\mu{-}\nu)U_\mu^\dagger(x{-}\nu)U_\nu(x{-}\nu)]$; $\sum\operatorname{Re}\operatorname{Tr}(U_\mu R_\mu)=4\sum_P\operatorname{Re}\operatorname{Tr}U_P$ | staple completion | `…:L146, L151 staple_field()` | machine (inv F94-FA3) |
| 4 | $a_0=\tfrac12\operatorname{Re}(w_{00}+w_{11}),\ a_1=\tfrac12\operatorname{Im}(w_{01}+w_{10}),\ a_2=\tfrac12\operatorname{Re}(w_{01}-w_{10}),\ a_3=\tfrac12\operatorname{Im}(w_{00}-w_{11})$; $k=\lvert a\rvert$, $V=M(a/k)$, $M(q)=q_0+i\,q\cdot\sigma$ | SU(2)-subgroup projection | `…:L171–L178 _su2_from_block()`, L185–L188 | unknown |
| 5 | $\xi=\tfrac23\beta k$; $a_0\sim\sqrt{1-a_0^2}\,e^{\xi a_0}$ via proposal $a_0=1+\xi^{-1}\ln(u+(1-u)e^{-2\xi})$, accept w.p. $\sqrt{1-a_0^2}$; $R_2=X_2V^\dagger$ | Cabibbo–Marinari heat-bath (Creutz sampler) | `…:L211–L223, L240–L241` | unknown |
| 6 | $R_2=(V^\dagger)^2$ | over-relaxation (action-preserving) | `…:L254 _su2_overrelax()` | machine (inv F94-FA2) |
| 7 | $U_\mu\to E_{ij}(R_2)U_\mu$ checkerboard; reunitarise at cadence | sweep update | `…:L305–L310 _update_direction()` | unknown |
| 8 | $W(R,T)=\langle\tfrac13\operatorname{Re}\operatorname{Tr}\prod\text{links}\rangle$ | planar Wilson loop | `…:L392–L400 wilson_loop_planar()` | unknown |
| 9 | $P(\mathbf x)=\operatorname{Tr}\prod_tU_t(\mathbf x,t)$; $C(R)=\langle P(\mathbf x)P^*(\mathbf x+R)\rangle$ | Polyakov loop and correlator | `…:L415–L418, L426–L427` | unknown |
| 10 | $M_b[(ij),(i'j')]=\langle L_b(x)_{ii'}\,L_b(x{+}R)^*_{jj'}\rangle_\text{sub}$; $C=\operatorname{Tr}_9\prod_bM_b$ | Lüscher–Weisz two-level estimator | `…:L485–L495 polyakov_correlator_twolevel()` | unknown |
| 11 | $V(R)=-\ln C(R)/T$; $\sigma_\text{sc}=-\ln(\beta/18)$; fit $V=\mu+\sigma R-e/R$ | static potential, strong-coupling σ, Cornell fit | `…:L556, L561, L571–L575` | unknown |

**Inputs → outputs:** link field $U$ (shape $(D,)+(L,)^D+(3,3)$), β, rng → thermalised ensemble, loops, $V(R)$. **Depends on:** `gauge.cooling` (`_mm`, `_dag`, `su3_reunitarise`), `gauge.strong.su3_haar` (05a/05b gauge maps). **Flags:**
- SUPERSEDED (S21; F323/F265): hypercubic, not BCC.
- The registry `findings` field is empty; the natural finding is F94.
- A leftover `sys.path` insert (L45–L48) is plumbing.

---

### `engine/forks/gauge/u1_link_unitarity_forks.py` — U(1) per-link Peierls step: forks (b) Strang and (d) renormalised
**Status:** live · standalone · spine · **Findings:** F385 F384 · **Registry exactness:** machine · **Lattice:** BCC (8 directions $(\pm1,\pm1,\pm1)$, fractional spectral shifts) · **Law:** single chiral Weyl branch (`sign` ±) · **Units:** lattice

**Does:** carries the two alternatives to the primary per-link construction (fork (a), `gauge.minimal_coupling.u1_link_weyl_step_3d_bcc`). It also holds the F385 gate entry, which adjudicates unitarity against momentum transfer. Per F385 (Confirmed-narrower), fork (a) is the primary construction. Fork (b) does not improve the drift power. Fork (d) is exactly norm-conserving but not derived from an action, and its "comparable kick" holds only for localised fields. Fork (c) collapses to (a).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\psi'=\sum_{j=1}^{8}e^{i\phi_j(x)/2}\,M_j\,\mathcal T_{d_j}\!\big[e^{i\phi_j(x)/2}\psi\big]$, $\phi_j=q\,c_\text{lat}\,\mathbf A(x)\cdot\mathbf d_j$ | fork (b): half Peierls phase at the source, half at the destination, per BCC direction | `u1_link_unitarity_forks.py:L71–L85 u1_link_step_strang_split()` | machine (reg) |
| 2 | $\psi'(x)=\psi_a(x)\sqrt{\rho_\text{free}(x)/\rho_a(x)}$, $\rho=\lvert f\rvert^2+\lvert g\rvert^2$ | fork (d): per-site magnitude projection onto the free step's density (nonlinear, not unitary) | `…:L113–L120 u1_link_step_renormalized()` | machine (reg) |
| 3 | $\langle\mathbf k\rangle=\frac1N\sum_k\mathbf k(\lvert\tilde f\rvert^2+\lvert\tilde g\rvert^2)$ | spectral matter momentum | `…:L130–L137 matter_momentum()` | machine (reg) |
| 4 | $\lVert S[A+\nabla\beta](e^{iq\beta}\psi)-e^{iq\beta}S[A]\psi\rVert_\infty$, $\nabla\beta=\mathcal F^{-1}[i\mathbf k\hat\beta]$ | Ward residual (fork a) | `…:L153–L164 gauge_covariance_residual()` | machine (reg) |
| 5 | uniform $\mathbf A$: $\psi'=\mathcal F^{-1}[U_\text{BCC}(\mathbf k+q\mathbf A)\hat\psi]$ | exact rigid-momentum-shift special case (checked against fork a) | `…:L209–L219 check_u1_link_forks()` | machine (reg) |
| 6 | $\log(\text{norm drift})$ vs $\log\lvert qA\rvert$ slope $\approx1$ | fork (a) drift is $O(\lvert qA\rvert)$ | `…:L231–L238` | machine (reg) |

**Inputs → outputs:** $(f,g)$ complex 3-D arrays, $\mathbf A$ (3,L,L,L), charge $q$ → updated spinors; the gate returns 10 legs with a declared control `corrupt_a0`. **Depends on:** `casim.numerics` (xp, fft) (02-numerics.md); `lattice.bcc.bcc_fractional_shift`, `weyl_step_3d_bcc`, `bcc_unitary` (03-lattice.md § bcc.py); `lattice.geometry.make_kgrid_3d`; `gauge.weak_wmu.BCC_DIRS/_SPINOR_MATS`; `gauge.minimal_coupling` (05c-gauge-photon-lpt-weak.md). **Flags:**
- Tagged `live` although it sits in `forks/`.
- Complex spinor fields go through `casim.numerics.fft` (sanctioned route). Re and Im are both kept (complex arrays throughout).

---

### `engine/forks/lattice/__init__.py` — package docstring
**Status:** not in module registry · plumbing. **Flags:** none.

---

### `engine/forks/lattice/smearing_fork_harness.py` — $f_k(q)$ smearing of the σ-bilinear curl residual
**Status:** fork_unclaimed · unreferenced · **Findings:** (F21 in docstring; registry none) · **Lattice:** BCC · **Law:** chiral single branch, pair rate $\Omega_j=\omega(k/2+q)+\omega(k/2-q)$ · **Units:** lattice
**SUPERSEDED (construction):** it smears the σ-bilinear *composite photon* $G^i=\phi^T\sigma^i\psi$. F65–F69 exclude that construction for the photon (key decision 5; the paired-spinor photon replaces it; see 05c § photon.py).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $G=\text{bilinear\_G}(\psi_+(k/2{+}q),\psi_-(k/2{-}q))$, $G_T$ = transverse part; $E_0=\lvert n\rvert(G_T+G_T^*)$, $B_0=i\lvert n\rvert(G_T^*-G_T)$; $\Omega_j=\omega_++\omega_-$ | displaced-pair EM bilinears | `smearing_fork_harness.py:L118–L128 _pair_EM()` | unknown |
| 2 | $w(q)\propto e^{-\lvert q\rvert^2/2\sigma^2}$ ($q_0=0$ forced); BCC shell $q=\delta(\pm1,\pm1,\pm1)/2$, $w=1/8$ | smearing kernels | `…:L139–L151` | unknown |
| 3 | $E_1=\lvert n\rvert(e^{-i\Omega}G_T+e^{i\Omega}G_T^*)$, $B_1=i\lvert n\rvert(e^{i\Omega}G_T^*-e^{-i\Omega}G_T)$; residual $\lVert\Delta E-i\,2\mathbf n\times B_0\rVert/(\lVert E_0\rVert+\lVert B_0\rVert)$ | smeared one-tick curl residual; transversality $2\mathbf n\cdot E_0$; $\Omega_\text{eff}=\sum w_j\Omega_j$ vs $2\omega(k/2)$ | `…:L236–L263 smeared_curl_residual()` | unknown |
| 4 | baseline coefficient $c_\text{lat}/\sqrt2=1/\sqrt6$ | σ=0 self-check target | `…:L85, L383` | unknown |
| 5 | log–log slope and residual$/k$ | scaling fit | `…:L275–L284, L302–L303` | unknown |

**Inputs → outputs:** none → per-variant slopes and coefficients (dated JSON under `__main__`). **Depends on:** `gauge.bilinear` (`weyl_eigenmodes_3d_bcc`, `bilinear_G`, `_transverse_part`, `_random_dirs`), `lattice.bcc._bcc_uvec`, c_lat (F26). **Flags:**
- SUPERSEDED photon construction (σ-bilinear, F65–F69).
- Docstring inconsistency: this file attributes the $1/\sqrt6$ baseline to "Finding 21", while `curl_fork_harness.py` attributes it to "Finding 2".
- Stale run path "python3 forks/smearing_fork_harness.py" (L57).
- The docstring claim "residual O(k) → O(σ²/k)" (L30) is an analytic expectation, not computed.

---

### `engine/forks/particles/__init__.py` — package docstring
**Status:** not in module registry · plumbing. **Flags:** none.

---

### `engine/forks/particles/complex_mass_fork.py` — Higgs-free complex-mass (gauged-β) Dirac CA, U(1) and chiral SU(2)
**Status:** fork_unclaimed · unreferenced · **Findings (registry):** none — content is F27 · **Lattice:** 2-D square (`core_exact.exact2d_*`, D1 reference, not canonical) · **Law:** chiral single-branch Weyl kinetic + local mass step · **Units:** lattice

**Does:** the staging fork of Ludwig's 2007 "gauge the β matrix" proposal. A mass step couples left $\eta$ to right $\chi$ through $e^{i\theta(x)}$ (U(1)) or $U(x)\in SU(2)$ (doublet), and is invariant under left-only transformations with $U\to VU$. The step is promoted as F27 (`particles.dirac.mass_step_doublet`, `gauge.hypercharge`; see 06b/05c).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U(t)=\cos(\omega t)\,I+\frac{\sin\omega t}{\sin\omega}\big(U(1)-\cos\omega\,I\big)$, $\omega=\arccos(c_xc_y)$ | spectral fractional kinetic step (2-D) | `complex_mass_fork.py:L117–L141 _weyl_half_step()` | unknown |
| 2 | $\eta'=\cos m\,\eta+i\sin m\,e^{i\theta}\chi,\ \chi'=i\sin m\,e^{-i\theta}\eta+\cos m\,\chi$ | U(1) complex-mass step (unitary: $A^2=I$) | `…:L168–L176 mass_step_1flavor()` | unknown |
| 3 | $S=K(\Delta t/2)\,M(\Delta t)\,K(\Delta t/2)$ | Strang step | `…:L200–L207 complex_mass_step_1flavor()` | unknown |
| 4 | $U=\begin{pmatrix}a&-b^*\\b&a^*\end{pmatrix}$; Haar: unit quaternion $\to a=q_0+iq_3,\ b=q_2+iq_1$ | SU(2) field | `…:L248–L270 make_su2_field()` | unknown |
| 5 | $\eta\to V\eta,\ \chi\to\chi,\ U\to VU$ ($a''=V_aU_a-V_b^*U_b,\ b''=V_bU_a+V_a^*U_b$) | chiral SU(2)$_L$ gauge transform | `…:L296–L313 su2_gauge_transform()` | unknown |
| 6 | $\eta'=\cos m\,\eta+i\sin m\,(U\otimes I_2)\chi,\ \chi'=i\sin m\,(U^\dagger\otimes I_2)\eta+\cos m\,\chi$ | doublet mass step | `…:L361–L373 mass_step_doublet()` | unknown |
| 7 | $N_{L,R}$; $T_3=\tfrac12(N_\nu-N_e)$; "$\langle T^2\rangle$" $=\langle T_3\rangle^2+\lvert\langle T_+\rangle\rvert^2$ | chirality / isospin observables | `…:L489–L511, L539–L548 su2_casimir_left()` | unknown |

**Inputs → outputs:** 4 or 8 complex $(L_x,L_y)$ spinor arrays, θ or $(a,b)$, $m$ → updated spinors, observables. **Depends on:** `lattice.core_exact.exact2d_unitary/exact2d_dispersion` (03-lattice.md § core_exact, reference implementation); `particles.dirac._check_mass`; `casim.numerics.fft`. **Flags:**
- ⚠ DOC/CODE MISMATCH: `su2_casimir_left` says the result "should be 3/4 if the state is a pure doublet". The code returns $\lvert\langle\vec T\rangle\rvert^2=\langle T_3\rangle^2+\lvert\langle T_+\rangle\rvert^2\le1/4$ (e.g. $1/4$ for pure $\nu$). That is not the Casimir expectation $\langle T^2\rangle=3/4$.
- ⚠ DOC/CODE MISMATCH (minor): `make_su2_field` mode `'plane'` says $b=\sin(\pi/4)e^{ikx}$, but the code sets a uniform $b=\sin(\pi/4)$ (L262).
- It uses `np.fft.fftfreq` directly (allowed) and a `sys.path` insert (L88–L90). The reference is 2-D square, not BCC (D1).
- The registry `findings` field is empty; the natural finding is F27.

---

### `engine/forks/particles/derive_weight_as_phase.py` — E1 attack on the weight-as-phase principle ($\delta^*=2/9$ rad)
**Status:** fork_live · standalone · spine · **Findings:** F230 F253 F255 F256 · **Lattice:** $O_h$ group theory + BCC 2nd shell (6 axis sites) · **Law:** n/a · **Units:** dimensionless (rad)
**Fork status (supersessions `S15-E1-weight-as-phase-attack-is-a-fork`):** F230 is SUPERSEDED by F253/F255/F256. Weight-as-phase is adopted as a **founding principle** (key decision 7). This script's attempt to *derive* it is the recorded alternative: route A reduces it to "POSIT-N", route B is negative (only holonomy $2\pi/3$). F255 later derives $R=1$ from Schur isotropy.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $n_\Gamma=\frac1{24}\sum_c\lvert c\rvert\chi_V(c)^2\chi_\Gamma(c)$ on $O$; $T_{1u}\otimes T_{1u}=A_1+E+T_1+T_2$; $w_{E_g}=\dim E\cdot n_E/9=2/9$ | E_g representation weight (reproduces F175) | `derive_weight_as_phase.py:L53–L57` | unknown |
| 2 | $c_a=\sqrt{m_a}/\bar s-1$; $\delta=\operatorname{atan2}(-\sum c_a\sin\tfrac{2\pi a}3,\sum c_a\cos\tfrac{2\pi a}3)\bmod 2\pi/3$; $Q=\sum m/(\sum\sqrt m)^2$ | measured lepton angle and Koide $Q$ | `…:L74, L77–L87 fit_delta()` | unknown |
| 3 | $F=B\cos3\delta+C\cos^23\delta$ ⇒ $\cos3\delta=-B/2C$ | Landau interior relation (sympy) | `…:L115–L118` | unknown |
| 4 | $\delta=w_{E_g}\cdot R$; $R=1$ (POSIT-N) ⇒ $\delta^*=2/9$ | equipartition route | `…:L134–L136` | unknown |
| 5 | candidate norms $\{1,e,1/e,\sqrt2e^2,e^2\}$, $e=$ `e_saturation` $=0.733$ | is $R=1$ forced? (no) | `…:L156–L166` | unknown |
| 6 | $M_{C_3}=\begin{pmatrix}u_P\cdot u&w_P\cdot u\\u_P\cdot w&w_P\cdot w\end{pmatrix}$, $\theta=\operatorname{atan2}(M_{10},M_{00})$ ($=2\pi/3$ magnitude) on the $(d_{z^2},d_{x^2-y^2})$ basis of the 6 axis sites | $C_3$ holonomy on the $E_g$ plane | `…:L186–L201` | unknown |
| 7 | $\lvert2\pi p/q-2/9\rvert<10^{-3}$, $q<25$ | quantised-phase sweep (no symmetry-natural hit) | `…:L238–L241` | unknown |

**Inputs → outputs:** none → `RESULTS` dict. **The derivation runs and prints at import**; only the JSON write is `__main__`-guarded. **Depends on:** `delta_star` $=2/9$ (Fraction; F175/F253/F255/F256, exact), `delta_star_f`, `e_saturation` $=0.733$ (F92/F118/F234, quantitative). **Flags:**
- SUPERSEDED (S15): the attack is a fork; the principle is adopted, not derived here.
- Import-time computation with prints (no write).
- The comment L277 names the module path `casim.engine.particles.derive_weight_as_phase`, but it now lives in `forks.particles`.
- Inline $2/3$ literal (L91) and PDG masses.

---

### `engine/forks/particles/koide_pseudomass_fork.py` — Koide pseudo-masses for quarks (F404, excluded / non-predictive)
**Status:** fork_live · standalone · spine · **Findings:** F404 F403 F76 F78 F93 F175 F346 F347 · **Registry exactness:** quantitative · **Lattice:** $T_{1u}$ generation triplet (cube axes) · **Law:** n/a · **Units:** MeV

**Does:** tests amplitude matrices $S_f=\mu_f(1+\sqrt2E(\delta_f))+T_f$ (exact-Koide diagonal plus $T_{2g}/T_{1g}$ off-diagonals). It requires $M_f=S_f^2$ to reproduce quark masses and $V=U_U^\dagger U_D$ to reproduce the CKM. The fork's verdict: excluded with lepton-like amplitudes; viable but non-predictive with a negative lightest down amplitude. Not adopted.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | shape $1+\sqrt2\cos(\delta+2\pi a/3)$; $Q=\sum\lambda^2/(\sum\lambda)^2$ | exact-Koide diagonal, Koide ratio | `koide_pseudomass_fork.py:L86, L91, L95` | quantitative (reg) |
| 2 | $\operatorname{tr}S^2=\sum S_{aa}^2+2\sum_{a<b}\lvert S_{ab}\rvert^2$ ⇒ $Q_\text{phys}-Q_\text{pseudo}=\lVert S_\text{off}\rVert_F^2/(\operatorname{tr}S)^2$ | P1 trace identity (sympy) | `…:L127–L137 p1_trace_identity()` | exact (inv 241) |
| 3 | $\lVert S_\text{off}\rVert_F/\operatorname{tr}S=\sqrt{Q-2/3}$ | required off-diagonal weight | `…:L142–L144 required_offdiag_fraction()` | quantitative (inv 53) |
| 4 | Schur–Horn: $d\prec\lambda$ ⇔ $d_{(1)}\le\lambda_{(1)}$, $d_{(1)}+d_{(2)}\le\lambda_{(1)}+\lambda_{(2)}$, equal traces | admissible $\delta$ windows on $[0,\pi/3]$ | `…:L100–L102 schur_horn()`, L109–L119 | quantitative (inv 53) |
| 5 | $s_f=\lvert U_f\rvert^{\circ2}\lambda_f$ vs $\tfrac{\operatorname{tr}}3\text{shape}(\delta_f)$; CKM residuals $(\lvert V_{us}\rvert,\lvert V_{cb}\rvert,\lvert V_{ub}\rvert,\lvert V_{td}\rvert,J)$, $V=U_U^\dagger PU_D$ | joint pseudo-mass + CKM fit (hand LM, 24 starts) | `…:L211–L226 joint_search()`, LM L166–L195 | quantitative (inv 53) |
| 6 | $J=\operatorname{Im}(V_{11}V_{22}V_{12}^*V_{21}^*)$; real $S\Rightarrow J=0$ | P6: CP needs $T_{1g}$ | `…:L159, L268–L272 real_S_gives_J_zero()` | exact (inv 241) |
| 7 | best unitary $\chi^2$ over 5 observables | unitary floor | `…:L254–L262 unitary_floor()` | quantitative (reg) |

**Inputs → outputs:** scheme, down sign pattern → record with legs P1–P7 (`check_koide_pseudomass_fork`). **Depends on:** `delta_star_f` $=2/9$ (F175/F253/F255/F256); `casim.numerics` rng/xp. **Flags:** PDG/CKM data are inline, as declared. Not adopted (fork record F404).

---

### `engine/forks/particles/koide_pseudomass_minimal.py` — minimal pseudo-mass quark fit (F407, one dof, non-predictive)
**Status:** fork_live · standalone · spine · **Findings:** F407 F404 F78 F93 F175 F346 · **Registry exactness:** quantitative · **Lattice:** $T_{1u}$ triplet · **Law:** n/a · **Units:** MeV

**Does:** the report's minimal ansatz: exact-Koide diagonal, three real $T_{2g}$ amplitudes per sector, and one $T_{1g}$ phase in one slot. That is 9 parameters against 10 observables. Masses and CKM are fitted with errors. The fork's verdict: fits exist for the named $\delta$ pairs, with one real dof "spent on nothing".

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $S=\mu\,\operatorname{diag}(1+\sqrt2\cos(\delta+2\pi a/3))+\sum_{a<b}t_{ab}(e_{ab}+e_{ba})+i\phi\,(e_{a'b'}-e_{b'a'})$, the last term on one optional slot $(a',b')=$ `_OFF[t1g_index]` only | minimal amplitude matrix | `koide_pseudomass_minimal.py:L140–L147 amplitude_matrix()` | quantitative (reg) |
| 2 | $S=U\operatorname{diag}(\lambda)U^\dagger$ (eigh, sorted by $\lvert\lambda\rvert$); $m=\lambda^2$; $V=U_U^\dagger U_D$; $J$ | observables (signed amplitudes are an output) | `…:L151–L168 observables()` | quantitative (reg) |
| 3 | $r=[(m/m_\text{PDG}-1)/\sigma_\text{rel}]\oplus[(\text{CKM}-\text{obs})/\sigma]$ (+ optional pins/positivity penalties) | residual vector; $\chi^2=\lVert r\rVert^2$ | `…:L175–L183 _residuals()` | quantitative (reg) |
| 4 | multistart LM / continuation along $\delta$ / re-polished certificates | fit machinery | `…:L186–L240` | quantitative (reg) |
| 5 | $\operatorname{rank}\partial r/\partial p$ (SVD, $\text{rtol}=10^{-8}$) $=9$ | M1: one dof | `…:L243–L252 jacobian_rank()` | quantitative (inv 56) |
| 6 | $\Delta\chi^2=\chi^2-\chi^2_\text{floor}\le3.84$ for $(\delta^*,\delta^*),(\delta^*/3,2\delta^*/3),(\delta^*/3,\delta^*/2)$; off-band $>9$ | M2/M3 | `…:L317–L353 check_koide_pseudomass_minimal()` | quantitative (inv 56) |
| 7 | $\sqrt{m_d/m_s}$ vs fitted $\lvert V_{us}\rvert$ spread; $\lvert V_{us}\rvert\ge J/(\lvert V_{cb}\rvert\lvert V_{ub}\rvert)$ | M5: GST not emergent | `…:L365–L381` | quantitative (inv 56) |

**Inputs → outputs:** scheme → record M1–M5. **Depends on:** the F404 fork (data, LM, `unitary_floor`); `delta_star_f` (2/9); `casim.numerics` rng/xp. **Flags:**
- `ms_profile` temporarily mutates the shared `QUARK_MASSES_MEV` dict imported from the F404 fork (restored in `finally`, L278–L283). This is a side-effect hazard if run concurrently.
- The `CERTIFICATES` vectors (L99–L132) came from scipy runs outside the repo. They are re-polished, not trusted.
- `UNITARY_FLOOR = 0.119` is display-only (recomputed).
