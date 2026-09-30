# Gauge sector II — derivations, gluon, confinement, EM current, hypercharge

**Scope.** Twenty modules of `src/casim/engine/gauge/`: the SU(3) gluon kernel and its confinement/smoothing layer (`gluon`, `gluon_self_energy`, `confinement`, `cooling`), the colour-structure and $N_c$ derivation scripts (`derive_su3_structure`, `derive_internal_index_existence`, `derive_premise_a_irreducibility`, `derive_ncolour*`, `derive_coupling_normalisation`, `derive_x1_branch`, `derive_bilinear_so3`), the electroweak derivations (`hypercharge`, `derive_charge_partition`, `derive_gauge_boson_masses`), the U(1) photon–fermion coupling layer (`em_current`, `em_photon_sourcing`), and two stand-alone pieces (`emission`, `factorization`). The code is the source of truth. Where a docstring or finding says something different, the entry carries a `⚠ DOC/CODE MISMATCH` flag. Every flag is also listed in `flags/p05b.md`.

**Conventions shared by the batch.**
- **Lattice (D1).** The canonical BCC kernels are the gluon BCC steps, `em_current` and `em_photon_sourcing` (BCC walk `lattice.bcc.weyl_step_3d_bcc`, curl symbol `charge_coupling.bcc_curl_symbol`). The **2D-square** code is a reference implementation: the whole of `confinement.py` and `cooling.py`, the `*_2d` functions in `gluon.py`, and `hypercharge.py`, whose kinetic step is `particles.dirac._weyl_half_step_2c`, a 2D exact-QCA walk. BCC momentum enters through $c_\text{lat}=1/\sqrt3$ (F26, exact) as the $k/\sqrt3$ argument of `bcc._bcc_uvec`.
- **Rotation law (F91).** The gluon propagates by the **even** law $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$, the same law as the photon. A retained **chiral** step exists for comparison only. `gluon_self_energy` also uses $\Omega_\text{even}$.
- **Units.** Lattice units ($a=1$, one tick $=1$) throughout, except in `emission` (atomic units → SI), `derive_gauge_boson_masses` (GeV, PDG inputs) and the running-coupling scripts (GeV via $\mu_0=\hbar c/a=1.850\times10^{18}$ GeV, a module literal).
- **Signs.** $T^a=\lambda^a/2$ with $\mathrm{Tr}\,T^aT^b=\tfrac12\delta^{ab}$ and $[T^a,T^b]=if^{abc}T^c$. The Gell-Mann–Nishijima convention is $Q=T_3+Y/2$ (so $Y=2y$). The spectral $(E,B)$ rotation is $E'=\cos\Omega\,E+\sin\Omega\,B$, $B'=-\sin\Omega\,E+\cos\Omega\,B$, which is equivalent to $E+iB\to e^{-i\Omega}(E+iB)$.
- **Hazards.** Every spectral step here acts on real $(E,B)$ through complex FFTs and takes `.real` after the inverse transform. For the even law this is exact, because $\Omega_\text{even}(-k)=\Omega_\text{even}(k)$; spot-checked at $2\times10^{-14}$ on $L=6$. The σ-bilinear construction appears only as the gluon's colour-octet bilinear, which is Hermitian (allowed per F65–F69), and in the F302 audit. No module here builds the photon from a σ-bilinear.

**Modules:** confinement · cooling · derive_bilinear_so3 · derive_charge_partition · derive_coupling_normalisation · derive_gauge_boson_masses · derive_internal_index_existence · derive_ncolour · derive_ncolour_bracket · derive_ncolour_ceiling · derive_premise_a_irreducibility · derive_su3_structure · derive_x1_branch · em_current · em_photon_sourcing · emission · factorization · gluon · gluon_self_energy · hypercharge.

---

### `engine/gauge/confinement.py` — 2D SU(3) area law, string tension, static potential
**Status:** live · driven (15 ch) · **Findings:** none in registry (FG-7c; docstring cites F43) · **Lattice:** 2D square (reference, D1) · **Law:** n/a · **Units:** lattice

**Does:** computes the exact 2D SU(3) area law from a single-plaquette Weyl-torus quadrature, with a Metropolis cross-check.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $w(\beta)=\dfrac{\int d\phi_1d\phi_2\,\lvert\Delta\rvert^2\,\tfrac13\sum_i\cos\phi_i\;e^{(\beta/N)\sum_i\cos\phi_i}}{\int d\phi_1d\phi_2\,\lvert\Delta\rvert^2\,e^{(\beta/N)\sum_i\cos\phi_i}}$, $\phi_3=-\phi_1-\phi_2$ | single-plaquette mean $\langle\tfrac1N\mathrm{Re\,Tr}\,U\rangle$, rectangle rule on the maximal torus | `confinement.py:L94 plaquette_mean()` | unknown |
| 2 | $\lvert\Delta\rvert^2=\prod_{i<j}2(1-\cos(\phi_i-\phi_j))$ | Weyl (Haar) measure on the torus | `confinement.py:L74 _weyl_measure()` | unknown |
| 3 | $\langle\tfrac1N\mathrm{Tr}\,U\rangle$ (complex) with $\mathrm{Im}=0$ by $\phi\to-\phi$ | Schur's lemma $\langle U\rangle=w\,\mathbb 1$ | `confinement.py:L111 plaquette_mean_complex()` | unknown |
| 4 | $\sigma(\beta)=-\ln w(\beta)$ | string tension | `confinement.py:L117 string_tension()` | unknown |
| 5 | $\langle W(R,T)\rangle=w^{RT}$ | exact 2D area law | `confinement.py:L126 area_law_loops()` | unknown |
| 6 | $\chi(R,T)=-\ln\dfrac{W(R,T)W(R-1,T-1)}{W(R-1,T)W(R,T-1)}$ | Creutz ratio ($=\sigma$ on the exact law); NaN below the MC noise floor | `confinement.py:L147 creutz_ratio()` | unknown |
| 7 | $V(R)=-\ln[W(R,T)/W(R,T-1)]$ | one-step static-potential estimator | `confinement.py:L175 static_potential_from_loops()` | unknown |
| 8 | $V(R)=\sigma R$ | closed-form linear potential | `confinement.py:L180 static_potential_linear()` | unknown |
| 9 | $\Delta S=-(\beta/3)\,\mathrm{Re\,Tr}[(U'-U)\Sigma^\dagger]$, $U'=R\,U$, $R=\exp(i\,\epsilon\,\theta^aT^a)$ | Metropolis link update (2D), accept $\min(1,e^{-\Delta S})$ | `confinement.py:L212 metropolis_sweep_2d()` | unknown (stochastic) |
| 10 | $\Delta S=-(\beta/N)\,\mathrm{Re\,Tr}(U'-U)$ | single-matrix Metropolis for $\langle U\rangle$ | `confinement.py:L238 single_plaquette_mean_matrix()` | unknown (stochastic) |

**Inputs → outputs:** $\beta$ (Wilson normalisation $S=\beta\sum_\square(1-\tfrac1N\mathrm{Re\,Tr}\,U_\square)$) → $w,\sigma,\chi,V$, plus MC loop estimates via `gluon.wilson_loop_2d_avg` / 3. **Depends on:** `strong` (su3_exp, cold_links_2d; see 05a/05c), `cooling.staple_sum_2d`, `gluon.wilson_loop_2d_avg`. **Flags:** EXACTNESS unknown, because the registry has no class (the docstring says "machine precision"/"exact"). In #1, `plaquette_mean` hardcodes `/3.0` and a 3-phase torus while exposing an `n_c` argument, so `n_c≠3` would be inconsistent. The Metropolis sweep recomputes the full staple field per link (plumbing inefficiency only).

### `engine/gauge/cooling.py` — SU(3) Wilson gradient flow and cooling (2D)
**Status:** live · driven (17 ch) · **Findings:** none in registry (FG-7b; F43) · **Lattice:** 2D square (reference) · **Law:** n/a · **Units:** lattice (flow time $t$)

**Does:** runs the Lüscher Wilson flow and checkerboard cooling on 2D SU(3) links, i.e. gauge-covariant gradient descent on $S_W$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathrm{TA}(M)=\tfrac12(M-M^\dagger)-\tfrac1{2N}\mathrm{Tr}(M-M^\dagger)\mathbb 1$ | traceless anti-Hermitian projection | `cooling.py:L88 ta_project()` | unknown |
| 2 | $\exp(X)=V\,\mathrm{diag}(e^{iw})V^\dagger$, $X=iH$, $H=V\,\mathrm{diag}(w)V^\dagger$ | su(3) exponential via `eigh` | `cooling.py:L102 su3_exp_algebra()` | unknown |
| 3 | $U=W V_h/\det(WV_h)^{1/3}$ from $M=W\Sigma V_h$ | maximal SU(3) projection (the cooling physics) | `cooling.py:L136 su3_project()` | unknown |
| 4 | Gram–Schmidt rows, $e_2=\overline{e_0\times e_1}$, then $/\det^{1/3}$ | cheap reunitarisation (not interchangeable with #3) | `cooling.py:L194 su3_reunitarise()` | unknown |
| 5 | $\Sigma^+_x=U_y(x)U_x(x+\hat y)U_y^\dagger(x+\hat x)$, $\Sigma^-_x=U_y^\dagger(x-\hat y)U_x(x-\hat y)U_y(x+\hat x-\hat y)$ (and $x\leftrightarrow y$) | staple sum, $\sum_{p\ni U}\mathrm{Re\,Tr}\,U_p=\mathrm{Re\,Tr}[U\Sigma^\dagger]$ | `cooling.py:L217–231 staple_sum_2d()` | unknown |
| 6 | $S_W=\beta\sum_\square(1-\tfrac13\mathrm{Re\,Tr}\,U_\square)$; $\langle P\rangle=\tfrac13\langle\mathrm{Re\,Tr}\,U_\square\rangle$ | action and mean plaquette | `cooling.py:L245 wilson_action_2d()`, `L239 mean_plaquette_2d()` | unknown |
| 7 | $Z_\mu=-\mathrm{TA}[U_\mu\Sigma_\mu^\dagger]$ | flow force | `cooling.py:L263 wilson_flow_force_2d()` | unknown |
| 8 | $U\leftarrow e^{\epsilon Z}U$ | explicit Euler flow step | `cooling.py:L275 wilson_flow_step_euler_2d()` | unknown |
| 9 | $W_1=e^{Z_0/4}W_0$; $W_2=e^{\frac89Z_1-\frac{17}{36}Z_0}W_1$; $W_3=e^{\frac34Z_2-\frac89Z_1+\frac{17}{36}Z_0}W_2$, $Z_i=\epsilon Z(W_i)$ | Lüscher RK3 flow step | `cooling.py:L297–307 wilson_flow_step_rk3_2d()` | unknown |
| 10 | $U_\mu(x)\leftarrow\mathrm{Proj}_{SU(3)}\Sigma_\mu(x)$ on one checkerboard parity at a time | cooling sweep (maximises $\mathrm{Re\,Tr}\,U\Sigma^\dagger$ locally) | `cooling.py:L354 cooling_step_2d()` | unknown |

**Inputs → outputs:** 2D link field `(2,Lx,Ly,3,3)` → flowed/cooled links plus a history of $(t,S_W,\langle P\rangle)$ (`run_wilson_flow_2d` L311, `run_cooling_2d` L359). The builders `near_identity_links_2d` and `hot_links_2d` are plumbing. **Depends on:** `numerics.linalg.batched_matmul` (02-numerics.md; 1–2 ULP vs einsum), `strong` (plaquette_trace, T_GEN). **Flags:** EXACTNESS unknown, because the registry has no class. `numpy` is imported directly (D8 debt, a manifest module).

### `engine/gauge/derive_bilinear_so3.py` — which spinor bilinear is an SO(3) vector (F302)
**Status:** live · standalone · **Findings:** F302 · **Lattice:** BCC eigenmodes (via `bilinear.weyl_eigenmodes_3d_bcc`) · **Law:** n/a · **Units:** n/a

**Does:** proves that the transpose bilinear $\psi^T\sigma\psi$ is not a 3-vector and that the Cartan form $\psi^T\epsilon\sigma\psi$ is one. It also audits that no live W/Z/gluon construction uses the transpose form.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\epsilon=i\sigma_2$, $U^T\epsilon U=\det(U)\,\epsilon$ (any $2\times2$ $U$) | SU(2) invariant tensor (adjugate identity) | `derive_bilinear_so3.py:L345 symbolic_core()` | exact (reg) |
| 2 | $U^T(\epsilon\sigma^i)U=R^{ij}(\epsilon\sigma^j)$, $R^{ij}=\tfrac12\mathrm{tr}(\sigma^iU\sigma^jU^\dagger)$ | Cartan bilinear $G'^i=\phi^T\epsilon\sigma^i\psi$ is covariant | `derive_bilinear_so3.py:L108 cartan_bilinear()`, `L123 su2_so3_pair()` | exact (reg) |
| 3 | $\psi^T\sigma\psi=(2ab,0,a^2-b^2)$, $\psi^T\epsilon\sigma\psi=(a^2-b^2,\,i(a^2+b^2),\,-2ab)$ | explicit components; $\psi^T\sigma_2\psi\equiv0$ | `derive_bilinear_so3.py:L352–356 symbolic_core()` | exact (reg) |
| 4 | $G'\cdot G'=0$ for every $\psi$; $(\psi^T\sigma\psi)^2=(\psi^T\psi)^2$ | Cartan nullity vs Fierz value | `derive_bilinear_so3.py:L354–355 symbolic_core()` | exact (reg) |
| 5 | $\lVert G_{T,\perp}\rVert^2=2(\hat n\cdot\hat y)^2$ (transpose) vs $2$ (Cartan) | transverse amplitude on BCC helicity eigenmodes, $k=0.05$ | `derive_bilinear_so3.py:L245–249 amplitude_signature()` | machine ($<10^{-12}$) (reg: exact; row is weaker — see flags) |
| 6 | $\psi^\dagger\sigma\psi=\hat n$ (purely longitudinal) | Hermitian self-singlet carries no transverse field | `derive_bilinear_so3.py:L266 amplitude_signature()` | machine (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** seed, $k$ → covariance residuals per construction, amplitude table, and the static `sector_audit()` list; the gate is `f302_bilinear_so3_check` (L368). **Depends on:** `bilinear` (05a), `weak_wmu.fermion_current_isospin`, `gluon.quark_colour_octet_bilinear_{2d,bcc}`. **Flags:** check C6 reads a hand-written static list (`sector_audit`, L281), so it cannot detect a code change in the sectors it names (OTHER). `main()` writes JSON behind `__main__` only (OK).

### `engine/gauge/derive_charge_partition.py` — p.77 charge partition: J = L + S and per-tick charge bookkeeping (F396)
**Status:** live · standalone · **Findings:** F396 F27 F41 F54 · **Lattice:** BCC (Leg A, `dirac_bcc`); 2D arrays of the F41 mass step (Leg B) · **Law:** n/a · **Units:** lattice

**Does:** Leg A checks that the Dirac mass step conserves $S_z$ and that only the kinetic step exchanges spin with orbital motion. Leg B checks that the F27/F41 mass step conserves $Q$ in the unitary frame while violating $T_3$ and $Y$ in opposite amounts.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $S_z=\tfrac{s}{2}\sum(\lvert f_{\uparrow}\rvert^2-\lvert f_\downarrow\rvert^2)$, $s=-1$ ("primed", $S_z=-\sigma_z/2$) | lattice spin generator (conjugate rep $\sigma^*=(\sigma_x,-\sigma_y,\sigma_z)$) | `derive_charge_partition.py:L60 _sz()` | machine (reg) |
| 2 | $L_z=\sum_a\langle a\mid X\,k_y-Y\,k_x\mid a\rangle$ (spectral) | orbital angular momentum | `derive_charge_partition.py:L69 _lz()` | machine (reg) |
| 3 | $\eta'=c\,\eta-is\,\chi$, $\chi'=c\,\chi-is\,\eta$ ⇒ $\Delta S_z=0$ | mass step commutes with $\Sigma$ | `derive_charge_partition.py:L87–89 _mass_step_dSz()` | machine (reg) |
| 4 | $\mathrm{ptp}(S_z+L_z)/\mathrm{ptp}(S_z)$ | $J_z$ conservation ratio (small-$k$ $<0.2$, grows with $k$) | `derive_charge_partition.py:L80 _jz_ratio()` | quantitative (reg: machine; row is weaker — see flags) |
| 5 | $A(k)\approx\mathbb 1-i\,c_\text{lat}(k_x\sigma_x+k_y\sigma_y^*+k_z\sigma_z)$, $c_\text{lat}=1/\sqrt3$ (F26) | low-$k$ BCC block in the conjugate representation | `derive_charge_partition.py:L123 _lowk_frame_residual()` | quantitative ($<10^{-3}$) (reg: machine; row is weaker — see flags) |
| 6 | point group of the block is $D_2$ (C2x/y/z), not C4z | symmetry residuals | `derive_charge_partition.py:L113–116 _symmetry_residuals()` | machine (reg) |
| 7 | $Q=T_3+Y/2$ on $(\nu_L,e_L,\nu_R,e_R)$: $T_3=(\tfrac12,-\tfrac12,0,0)$, $Y=(-1,-1,0,-2)$, $Q=(0,-1,0,-1)$ | exact operator identity over ℚ | `derive_charge_partition.py:L129–131, L299` | machine (reg) (row read: exact) |
| 8 | $\eta\to\tilde\eta=U^\dagger\eta$ frame: $\Delta Q=0$, $\Delta T_3=-\Delta Y/2$ | charge bookkeeping of `hypercharge.mass_step_doublet_su2xu1y` | `derive_charge_partition.py:L154–160 _charges()`, `L168 _leg_b()` | machine (reg) |
| 9 | raw frame, pure-$\eta_e$ state: $\Delta Q_\text{raw}=\sin^2 m\sum\lvert U_b\rvert^2(\lvert\eta_{e\uparrow}\rvert^2+\lvert\eta_{e\downarrow}\rvert^2)$ | closed form of the gauge-artefact charge change | `derive_charge_partition.py:L227 _pure_eta_e_closed_form()` | machine (reg) |
| 10 | $Q'=\dfrac{t_3-s^2Q}{sc}=t_3\cot\theta-t_0\tan\theta$, $t_0=Q-t_3$; at $\sin^2\theta=\tfrac14$: $\cot\theta=\sqrt3$, $\tan\theta=1/\sqrt3$ | neutral-charge operator identity (pp.103–104) | `derive_charge_partition.py:L261–265 _qprime_identity()` | machine (reg) (row read: exact (checked at machine)) |

**Inputs → outputs:** frame/control switches → dict of 14 checks. **Depends on:** `particles.dirac_bcc.dirac_step_3d_bcc_splitstep` (06a), `lattice.bcc.bcc_unitary`, `hypercharge.mass_step_doublet_su2xu1y` (below). **Flags:** #10 compares $\tan\theta_W$ against `c_lat`, a *speed* constant, which merges two coincident $1/\sqrt3$ constants against the constants rule (OTHER). The $S_z$ sign is "fixed empirically" (docstring L16), not derived.

### `engine/gauge/derive_coupling_normalisation.py` — is F144's bare colour coupling centre-normalised? (F303)
**Status:** live · standalone · **Findings:** F303 F299 F298 F294 F144 F115 F101 F110 F91 · **Lattice:** BCC (loop-count enumeration) · **Law:** even (argued, F91) · **Units:** GeV for the running

**Does:** closes three candidate reconciliations of the Casimir $C_F$ with $g_s=\tfrac12$ and puts the Casimir branch against F280's Λ band. **SUPERSEDED in part by F325** (S22): the Casimir reading is a mixed-matching artefact, and branch B is adopted. The arithmetic stands.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $b_0=(11N_c-2n_f)/(12\pi)$; $1/\alpha(M_Z)=1/\alpha_0-2b_0\ln(\mu_0/M_Z)$ | one-loop running (∞ ⇒ Landau pole above $M_Z$) | `derive_coupling_normalisation.py:L140 _b0()`, `L146 _run_to_mz()` | exact (reg) |
| 2 | $M(t)=\begin{pmatrix}\cos\omega t&\frac b\omega\sin\omega t\\-\frac a\omega\sin\omega t&\cos\omega t\end{pmatrix}$, $\omega=\sqrt{ab}$; $M^TM=\mathbb 1\iff a=b$ | rotor lemma: fixes only $a/b$ (group-blind) | `derive_coupling_normalisation.py:L167–204 circularity_lemma_is_group_blind()` | exact (reg) |
| 3 | $s(m)^2=1$ ($m=1,2$ at $N=3$) vs $C_2(\mathbf 3)=C_2(\bar{\mathbf 3})=4/3$ ⇒ ratio $C_F=4/3$ | integer and SU(3) ladders are exactly proportional | `derive_coupling_normalisation.py:L238–249 ladder_proportionality()` | exact (reg) |
| 4 | no closed 3-hop loop on BCC ($\sum$ of three odd = odd); $n_3=0$, $n_4=216$ | minimal loop is the 4-bond rhombus | `derive_coupling_normalisation.py:L270–273 plaquette_link_count()` | exact (reg) |
| 5 | $n\,C_F=4\Rightarrow n=3$; $3(N^2-1)/(2N)=4\Rightarrow N=3$ | the closed "three-link" rescue | `derive_coupling_normalisation.py:L297–301 n_that_would_rescue_gs()` | exact (reg) |
| 6 | $\Delta(1/\alpha_0)=16\pi(C_F-1)$; $\Lambda$-ratio $=e^{\Delta/(2b_0)}$ | Casimir as scheme constant (26× the 0.64 residual) | `derive_coupling_normalisation.py:L321–322 scheme_absorption_test()` | exact (reg) |
| 7 | $\lvert\lambda\rvert^2=t_3^2+t_8^2=\tfrac13$ for all fundamental weights ⇒ $\alpha_0=3/(16\pi)$ | Cartan reading (Landau pole) | `derive_coupling_normalisation.py:L347–349 cartan_weight_norm_sq()` | exact (reg) |
| 8 | $\alpha_0^{H1}=g_s^2/4\pi$, $\alpha_0^{H2}=g_s^2/(4\pi C_F)$, $\alpha_0^{H2'}=3g_s^2/4\pi$, $g_s=\tfrac12$ | three normalisations run to $M_Z$ | `derive_coupling_normalisation.py:L370–379 hypothesis_predictions()` | quantitative (reg: exact; row is weaker — see flags) |
| 9 | $\chi_\text{req}=1/(4g^2_\text{req})$, $g^2_\text{req}=4\pi\alpha_\text{req}(\mu_0)$ | χ the data demands ($=1.000828$) | `derive_coupling_normalisation.py:L387–390 chi_required_by_data()` | quantitative (reg: exact; row is weaker — see flags) |
| 10 | band $[1,\,e^{\Delta C_W^\text{loops}/2}]$, $\Delta C_W^\text{loops}=6.138643-131/66$; $\Lambda_\text{Cas}=e^{16\pi(C_F-1)/(2b_0)}$ | Casimir branch vs F280 band ($[1,7.98]$) | `derive_coupling_normalisation.py:L433–442 casimir_branch_vs_f280_band()` | quantitative (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** control knobs → 9 checks N1–N8. **Depends on:** `su3_ladder.casimir2/triality` (05a/c), `derive_ncolour` (MU0_GEV, MZ_GEV, ALPHA_S_MZ_PDG, N_F, $g_s$). **Flags:** SUPERSEDED (partial) by F325 (supersessions S22). The literals 0.64, 1.78, 28.81, 28.8086, 6.138643 and F280 target 1.773444 are unregistered (L120–136). ⚠ DOC/CODE MISMATCH: the comment at L134–135 says the F280 target is "not written as a literal", but L136 is a literal, and the "band is rebuilt here" rests on literal inputs. The docstring's $\alpha_s(M_Z)=0.1186$ matches the code ($0.11858$).

### `engine/gauge/derive_gauge_boson_masses.py` — absolute $m_W$, $m_Z$ and $\rho=1$ (F320)
**Status:** live · standalone · **Findings:** F320 F141 F138 F231 F49 F51 F41 F27 F119 F127 · **Lattice:** BCC counts only (7 Wigner–Seitz axes, 2 sublattices) · **Law:** n/a · **Units:** GeV (PDG inputs)

**Does:** eliminates F141's stiffness quantum against $e$, predicting $m_W,m_Z$ from $\{\alpha,G_F\}$. It shows that $\rho=1$ follows from rank-one breaking and brackets the absolute masses by $\Delta r$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $g^2=7u$, $g'^2=2u$ ⇒ $\sin^2\theta_W=2/9$, $c^2/s^2=7/2$, $m_Z^2/m_W^2=9/7$ | counting → angle; $\sin^2\theta_W^\text{os}=2/9$ is registry constant `sin2_thetaW_onshell` (F49/F138/F141/F231, exact) | `derive_gauge_boson_masses.py:L148–155 counting_to_angle()` | bracketed (reg) (row read: exact) |
| 2 | $M^2=\tfrac{v^2}4\begin{pmatrix}g^2&-gg'\\-gg'&g'^2\end{pmatrix}$, $\det M^2\equiv0$ | rank-one (single F41 Stueckelberg direction) mass matrix; control adds $u$ to $M_{22}$ | `derive_gauge_boson_masses.py:L177–184 mass_matrix()` | bracketed (reg) (row read: exact (ℚ)) |
| 3 | $\rho=m_W^2/(m_Z^2\cos^2\theta_W)=1$ | ρ from rank, no custodial SU(2) | `derive_gauge_boson_masses.py:L206 rho_from_counting()` | bracketed (reg) (row read: exact (ℚ)) |
| 4 | $A=(g'W^3+gB)/\sqrt{g^2+g'^2}=(\sqrt2,\sqrt7)/3$ | massless eigenvector | `derive_gauge_boson_masses.py:L221–224 photon_eigenvector()` | bracketed (reg) (row read: machine) |
| 5 | $e^2=\frac{g^2g'^2}{g^2+g'^2}=\tfrac{14}9u$ ⇒ $u=\tfrac9{14}e^2$, $g^2=18\pi\alpha$, $g'^2=\tfrac{36}7\pi\alpha$ | stiffness quantum eliminated | `derive_gauge_boson_masses.py:L247–251 stiffness_quantum()` | bracketed (reg) (row read: exact) |
| 6 | $m_W=\tfrac{3v}2\sqrt{2\pi\alpha}$, $m_Z=\tfrac{9v}2\sqrt{2\pi\alpha/7}$, $v=(\sqrt2G_F)^{-1/2}$ | closed forms (tree) | `derive_gauge_boson_masses.py:L259–263 closed_forms()`, `L133` | bracketed (reg) (row read: exact (algebra)) |
| 7 | $m_W^2\sin^2\theta_W=\dfrac{\pi\alpha}{\sqrt2G_F(1-\Delta r)}$ | on-shell solve | `derive_gauge_boson_masses.py:L276–277 onshell_mW()` | bracketed (reg) (row read: exact (formula)) |
| 8 | $\dfrac{m_W^\text{model}}{m_W^\text{obs}}=\sqrt{s^2_\text{obs}/(2/9)}$ for all $\Delta r$ | Δr-cancelling ratio (+0.221 % $m_W$, +0.157 % $m_Z$) | `derive_gauge_boson_masses.py:L307–316 dr_invariance_scan()` | bracketed (reg) (row read: machine ($<10^{-12}$)) |
| 9 | $\Delta\rho_t=3G_Fm_t^2/(8\sqrt2\pi^2)$; $\Delta r_\text{lo}=\Delta\alpha-\tfrac{c^2}{s^2}\Delta\rho_t$, $\Delta r_\text{hi}$ = PDG-implied | Δr bracket → absolute mass bracket | `derive_gauge_boson_masses.py:L292 delta_rho_top()`, `L298–299 delta_r_bracket()` | bracketed (reg) |

**Inputs → outputs:** $\alpha^{-1}=137.035999177$, $G_F$, PDG masses, $m_t$, $\Delta\alpha(M_Z)$ (module literals, L125–130) → tree masses (−1 to −2 %), Δr-free excess, bracket containing PDG. **Depends on:** `constants.sin2_thetaW_onshell` (01-constants.md). **Flags:** ⚠ DOC/CODE MISMATCH: the docstring (L76) quotes +0.222 %/+0.158 %, where the code checks 0.221/0.157. The docstring also calls the $c^2/s^2$-in-Δr leg "B4c" (L81), but it is `B4d` in code (L407). The external inputs are unregistered literals (declared in the comment L118–123).

### `engine/gauge/derive_internal_index_existence.py` — must the colour index exist? (F333)
**Status:** live · standalone · **Findings:** F333 F317 F318 F324 F289 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** turns "the index exists by fiat" into a conditional on two observations (baryons are fermions, quarks are confined), giving $N\in\{3,5,7,\dots\}$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\dim\mathfrak{su}(N)=N^2-1$ ($=0$ at $N=1$) | no gauge boson at $N=1$ | `derive_internal_index_existence.py:L154 dim_su()` | exact (reg) |
| 2 | $P_{\Lambda^k}=\tfrac1{k!}\sum_\pi\mathrm{sgn}(\pi)\,\pi$ on $(\mathbb C^n)^{\otimes k}$ | antisymmetriser | `derive_internal_index_existence.py:L166–171 _antisymmetriser_projector()` | exact (reg) |
| 3 | $\dim(\Lambda^k\mathbb C^N)^{SU(N)}=1\iff k=N$ | joint kernel of $G^a=\sum_\text{slots}T^a$ on $\Lambda^k$ (SVD, tol $10^{-9}$) | `derive_internal_index_existence.py:L215 constituent_singlet()` | machine (reg: exact; row is weaker — see flags) |
| 4 | block swap of two $k$-fermion blocks has sign $(-1)^k$ | composite statistics (sympy Permutation) | `derive_internal_index_existence.py:L246 composite_block_swap_parity()` | exact (reg) |
| 5 | $\{N:\ N\text{ odd}\wedge N^2-1>0\}=\{3,5,7,9,11\}$ | the bracket | `derive_internal_index_existence.py:L288–296 the_bracket()` | exact (reg) |

**Inputs → outputs:** `n_probe` and controls → 6 checks S0–S5. The premises `observed_fermion=True` (L270) and `quarks_observed_confined=True` (L280) are hardcoded observations. **Depends on:** `derive_su3_structure.su_n_generators`. **Flags:** S5's "matches F324 bracket" compares against a list built inside this function with equivalent logic (L294), so it cannot fail independently (OTHER). F324's own module still returns {3} (see derive_ncolour_bracket).

### `engine/gauge/derive_ncolour.py` — why three colours? α_s / Λ selector (F293, F294)
**Status:** live · standalone · **Findings:** F293 F294 F279 F144 F110 F107 F280 F291 · **Lattice:** n/a (C7 audit uses `link_hamiltonian` Z_N/U(1)) · **Law:** n/a · **Units:** GeV

**Does:** closes anomaly and spatial-3 routes to $N_c$, records the $Z_3$ route as circular, and inverts the N_c-free bare coupling $\alpha_0=1/(16\pi)$ for $N_c$ (empirical selector).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | rows $N_cy_Q+y_L$, $2y_Q-y_u-y_d$, $y_d-y_Q+y_\phi$, $y_e-y_L+y_\phi$, $y_\nu-y_L-y_\phi$, $2y_\nu$ $=0$ | six-constraint hypercharge system; nullspace dim 1 ∀$N_c$, ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c:0$ | `derive_ncolour.py:L198–215 hypercharge_nullspace_symbolic()` | bracketed (reg) (row read: exact (sympy)) |
| 2 | $\sum Y$ and $\sum Y^3$ (colour-weighted, LH−RH) on the line $\equiv0$ in $N_c$ | grav and cubic anomalies select nothing | `derive_ncolour.py:L222–228` | bracketed (reg) (row read: exact) |
| 3 | $[C_3,\lambda^a]\neq0$, $\det C_3=+1$ | colour ≠ spatial axes | `derive_ncolour.py:L284–287 colour_is_not_spatial()` | bracketed (reg) (row read: machine) |
| 4 | $g_s=\tfrac12$ (hardcoded), $\alpha_s(\mu_0)=g_s^2/4\pi=1/(16\pi)$ | N_c-free bare coupling (F144: χ=1, χ=1/(4g²)) | `derive_ncolour.py:L348–350 alpha_s_at_lattice_scale()` | bracketed (reg) (row read: exact (by assertion)) |
| 5 | $b_0=(11N_c-2n_f)/(12\pi)$; $1/\alpha(M_Z)=1/\alpha_0+2b_0\ln(M_Z/\mu_0)$ | one-loop running ($N_c=3$ → 0.11858) | `derive_ncolour.py:L361 _b0()`, `L371–372 alpha_s_at_MZ()` | bracketed (reg) (row read: exact (formula)) |
| 6 | $\Lambda=\mu_0\exp[-1/(2b_0\alpha_0)]$ | confinement scale; ~28 decades across $N_c=2..4$ | `derive_ncolour.py:L379 lambda_qcd()` | bracketed (reg) (row read: exact (formula)) |
| 7 | $N_c=\big[12\pi\,\tfrac{1/\alpha_0-1/\alpha_t}{2\ln(\mu_0/M_Z)}+2n_f\big]/11$ | selector inversion (→ 2.9981) | `derive_ncolour.py:L403–405 solve_ncolour()` | bracketed (reg) (row read: quantitative) |
| 8 | $N_c=\dfrac{12\pi(1/\alpha_0-1/\alpha_t)+12A+10B}{11(A+B)}$, $A=2\ln(\mu_0/m_t)$, $B=2\ln(m_t/M_Z)$ | with the top threshold ($n_f$ 6→5) | `derive_ncolour.py:L423–426 solve_ncolour_thresholded()` | bracketed (reg) (row read: quantitative) |
| 9 | $\chi=s(m)^2/(2H_{mm})$ on the $Z_N$/U(1) dual Hamiltonian ⇒ $1/(4g^2)$ | C7 χ-map N-independence (worst 0.0) | `derive_ncolour.py:L493–494 c7_zn_independence()` | bracketed (reg) (row read: exact (measured 0.0)) |
| 10 | $\alpha_0\to\alpha_0h(N)$, $h\in\{1,\,1/C_F(N),\,1/N\}$, $C_F=(N^2-1)/2N$ | translation hypotheses H1/H2/H3 root-found | `derive_ncolour.py:L521 _casimir_F()`, `L568–575 c7_translation_hypotheses()` | bracketed (reg) (row read: quantitative) |

**Inputs → outputs:** $\alpha_s(M_Z)=0.1180$, $\mu_0=1.850\times10^{18}$ GeV, $M_Z$, $n_f=6$, band $[1,7.98]$ (literals, L162–168) → 17 checks. **Depends on:** `link_hamiltonian` (05a/c). **Flags:** ⚠ DOC/CODE MISMATCH: the comment at L210 says ratios are "normalised to $y_Q=1/6$", but the code (L214) normalises $y_Q=1$. The docstring (L104) says the band gives $N_c\in[2.90,3.00]$, while the code comment (L770–777) records the measured $[2.898,3.110]$. H2/H3 in #10 are made moot by F325 (Casimir reading withdrawn, S22). $g_s$ and $\mu_0$ are unregistered literals (OTHER).

### `engine/gauge/derive_ncolour_bracket.py` — N_c odd ∧ C7 support = {3} (F324)
**Status:** live · standalone · **Findings:** F324 F317 F318 F298 F293 F279 F27 F75 F144 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** pairs the Witten $Z_2$ doublet parity (lower) with F298's C7 support {2,3} (upper), giving {3}. **Upper leg SUPERSEDED by F325** (S22: F298's mixed matching withdrawn, so B10 is {3,5,7,…}). The code still returns {3}.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | Witten obstruction iff $2j\equiv1\pmod4$ | mod-2 index rule (quoted) | `derive_ncolour_bracket.py:L184 witten_contributes()` | exact (reg) |
| 2 | $T(j)=\tfrac23j(j+1)(2j+1)$ ($T(\tfrac12)=1$) | Dynkin cross-check (odd ⇔ #1) | `derive_ncolour_bracket.py:L195 dynkin_index_normalised()` | exact (reg) |
| 3 | $D_\text{gen}=\dim R_\text{colour}(N_c)+1$; $D=f\,n_\text{gen}D_\text{gen}$; consistent iff $D$ even | doublet parity ⇒ $N_c$ odd (fundamental) | `derive_ncolour_bracket.py:L228 su2L_doublet_content()`, `L265–270 witten_scan()` | exact (reg) |
| 4 | $y_Q=1$, $y_L=-N_c$ both odd ⇔ $N_c$ odd | local U(2) quantisation reading | `derive_ncolour_bracket.py:L346–349 local_u2_quantisation()` | exact (reg) |
| 5 | $\chi_k=s(k)^2/(4g^2C_2(\Lambda^k))$ single-valued | C7 support on the antisymmetric ladder; support {2,3} | `derive_ncolour_bracket.py:L409–413 _c7_exists_on_ladder()` | exact (reg) |
| 6 | sextet: $s^2=1$, $C_2=10/3$ ⇒ $\chi=3/10\neq3/4$ | mixed-symmetry breaks level-independence at N=3 | `derive_ncolour_bracket.py:L427–430 mixed_symmetry_breaks_n3()` | exact (reg) |
| 7 | $\{N\text{ odd}\}\cap\{2,3\}=\{3\}$ | the bracket | `derive_ncolour_bracket.py:L509–513 bracket()` | exact (reg) |
| 8 | $\dim(\Lambda^n\mathbb C^N)^{SU(N)}$ via kernel of $E_{ij}$ and Cartan on the wedge basis | exact partner of F317 S6 | `derive_ncolour_bracket.py:L576–608 lambda_n_singlets()` | exact (reg) |

**Inputs → outputs:** premise switches (n_gen, rep, doubling, conventions) → 15 checks + declarations. **Depends on:** `casimir_ladder` (05a/c), `derive_ncolour.hypercharge_nullspace_symbolic`, `derive_su3_structure.multiplicity_squeeze`. **Flags:** SUPERSEDED (upper leg, U1/B1) by F325/S22. The live code and `summary()` still assert $N_c=\{3\}$; downstream modules (`derive_premise_a_irreducibility` S4/S5) consume `bracket()["premises"]`.

### `engine/gauge/derive_ncolour_ceiling.py` — odd-N_c bracket does not narrow further (F338)
**Status:** live · standalone · **Findings:** F338 F324 F325 F293 F298 F317 F75 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** recomputes the post-F325 bracket {3,5,7,…} from the Witten leg alone and closes the colour-$\pi_4$ route. It also records an unverified mod-16 lead.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | bracket $=\{n\in\texttt{witten\_scan}\}\setminus\{1\}$ | current B10 bracket (odd, >1) | `derive_ncolour_ceiling.py:L319–321 check_ncolour_ceiling()` | exact (reg) |
| 2 | $\lvert\pi_4(SU(N))\rvert=2$ at $N=2$, else 1 | cited table (Bott) | `derive_ncolour_ceiling.py:L119 PI4_SUN_ORDER` | exact (reg) |
| 3 | $n_\text{Weyl}=2N_c+N_c+N_c+2+1+1=4(N_c+1)$ (=16 at $N_c=3$) | per-generation Weyl count | `derive_ncolour_ceiling.py:L164–165 weyl_fermion_count_per_generation()` | exact (reg) |
| 4 | $16\mid n_\text{gen}\cdot4(N_c+1)$ ⇒ $N_c\equiv3\pmod4$ (odd $n_\text{gen}$) | flagged, unverified mod-16 premise; excluded from pass count | `derive_ncolour_ceiling.py:L184–192 mod16_flagged_condition()` | exact (reg) |

**Inputs → outputs:** controls → 4 checks + `declarations` (G3 unverified, G4 literature ledger). **Depends on:** `derive_ncolour_bracket.witten_scan`. **Flags:** none beyond #4's declared unverified premise.

### `engine/gauge/derive_premise_a_irreducibility.py` — F333 premise (a) is not reducible to F289/F330 (F381)
**Status:** live · standalone · **Findings:** F381 F333 F289 F330 F324 · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** a meta-audit, largely source-text and signature scanning, showing that the derived spin-statistics carries no colour count. No new physics equation.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | composite parity $(-1)^N$ over $N=2..7$ bifurcates | imported from `composite_block_swap_parity` | `derive_premise_a_irreducibility.py:L185–189 bifurcation_over_n()` | exact (reg) |
| 2 | net premise change $=\lvert\texttt{bracket()["premises"]}\rvert-2=+4$ | substitution cost | `derive_premise_a_irreducibility.py:L218 substitution_net_cost()` | exact (reg) |

S1/S2 are token/regex scans of `qi_spin_statistics.py` and `qi_belt_trick.py` source (plumbing, L152–175). S4 is a string match on F324's premise list. **Depends on:** `derive_internal_index_existence`, `derive_ncolour_bracket.bracket` (SUPERSEDED upper leg, but only its premise list is read), `interactions.qi_spin_statistics`, `qi_belt_trick` (07c). **Flags:** ⚠ DOC/CODE MISMATCH: the docstring S1 (L67–71) lists "constituent" among the scanned tokens, but `_COLOUR_TOKENS` (L129–131) deliberately excludes it.

### `engine/gauge/derive_su3_structure.py` — structure of the colour gauge field (F317)
**Status:** live · standalone · **Findings:** F317 F91 F27 F68 F279 F293 F298 F289 F43 · **Lattice:** 1-D ring toy + 2D `strong` links + re-typed BCC walk · **Law:** even (forced, S2) · **Units:** lattice

**Does:** given an internal index the rule does not read, derives unitary → U(N), local → connection, special → SU(N), vector-like → even law, $N^2-1$ gluons, and $N=3$ given three-constituent baryons.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $T^a$: symmetric/antisymmetric off-diagonal $\pm\tfrac12$, Cartan $c\,\mathrm{diag}(1^m,-m,0)$, $c=\sqrt{1/(2m(m+1))}$ | su(N) basis, $\mathrm{Tr}\,T^aT^b=\tfrac12\delta^{ab}$ | `derive_su3_structure.py:L115–142 su_n_generators_exact()` | exact (reg) |
| 2 | $A^{abc}=2\,\mathrm{Tr}(T^a\{T^b,T^c\})$; $\equiv0$ for SU(2), $A^{888}=4\mathrm{Tr}(T_8^3)=-1/\sqrt3$ for SU(3) | anomaly coefficient: colour cannot be chiral | `derive_su3_structure.py:L176 anomaly_coefficients_exact()`, `L199 anomaly_witness_exact()` | exact (reg) |
| 3 | $A_L-A_R$: vector-like 0; chiral $A(\mathbf 3)$; conjugate $2A(\mathbf 3)$ | only vector-like colour is consistent | `derive_su3_structure.py:L228–247 chirality_assignment_table()` | machine (reg: exact; row is weaker — see flags) |
| 4 | $\lVert\mathrm{diag}(g_L,g_R)-\tfrac12\mathrm{tr}\rVert=0$ iff $g_L=g_R$ | branch-scalar coupling ⇒ even law (F68/F91) | `derive_su3_structure.py:L260–262 branch_coupling_traceless_part()` | exact (reg) |
| 5 | $\lvert\Omega^+-\Omega_\text{even}\rvert=\lvert\Omega^+-\Omega^-\rvert/2$, $\Omega^\pm=2\omega^\pm(k/2)$ on the body diagonal | chiral-colour contrast | `derive_su3_structure.py:L274–284 branch_split_on_body_diagonal()` | machine (reg: exact; row is weaker — see flags) |
| 6 | $U(x)\to V(x)U(x)V^\dagger(x+\hat\mu)$ restores covariance of the hop; on-site step commutes with $V(x)$ | locality forces the connection (1-D toy + `strong` 2D) | `derive_su3_structure.py:L343–352 locality_forces_connection()`, `L387–399 _tree()` | machine (reg: exact; row is weaker — see flags) |
| 7 | $M_{27}=\cos m\,\mathbb 1+i\sin m\begin{pmatrix}0&e^{i\theta}\\e^{-i\theta}&0\end{pmatrix}\otimes\mathbb 1_2$; $W(k)=\oplus_\pm[u_\pm\mathbb 1+i\,\mathbf n_\pm\cdot\sigma]$ | re-typed F27 mass step and BCC walk | `derive_su3_structure.py:L419 _f27_mass_step()`, `L447–452 _bcc_walk()` | exact (reg) |
| 8 | $\dim\{X: [R_i\otimes\mathbb 1_n,X]=0\}=n^2$ | commutant = $M_n$ ⇒ U(n); spectrum $n$-fold degenerate | `derive_su3_structure.py:L533–538 commutant_of_the_rule()`, `L557–570 internal_index_degeneracy()` | machine (reg: exact; row is weaker — see flags) |
| 9 | $A_{[SU(2)]^2Y}=\tfrac12(N_cy_Q+y_L)\equiv0$; $A_{[SU(2)]^2\mathrm{tr}}=N_cb/2\neq0$ | U(N)→SU(N): the trace U(1) cannot be gauged | `derive_su3_structure.py:L614–615 trace_u1_is_anomalous()` | exact (reg) |
| 10 | $SU(N)^3:\ A(\mathbf 3)(n_L-n_R)=A(2-2)=0$; $SU(N)^2Y:\ 2y_Q-y_u-y_d\equiv0$ | colour anomalies on the model content | `derive_su3_structure.py:L653, L664 colour_anomalies_on_the_model_content()` | exact (reg) |
| 11 | $\dim(\Lambda^3\mathbb C^N)^{SU(N)}=1$ only at $N=3$ | multiplicity given 3-constituent baryons | `derive_su3_structure.py:L723 antisymmetric_three_index_singlet()` | machine (reg: exact; row is weaker — see flags) |
| 12 | $f^{abc}=-2i\,\mathrm{Tr}([T^a,T^b]T^c)$, closure $[T^a,T^b]=if^{abc}T^c$ | $N^2-1$ gluons | `derive_su3_structure.py:L761–763 adjoint_dimension_and_closure()` | machine (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** controls (`use_compensator`, `chiral_colour`, `rule_reads_colour`, `drop_d_R`, `n_colour`) → 20 checks. **Depends on:** `strong` (05a/c), `weak_wmu._omega_even/bcc_dispersion`, `derive_ncolour.hypercharge_nullspace_symbolic`. **Flags:** `_bcc_walk` uses $u\mathbb 1+i\,\mathbf n\cdot\sigma$, while `lattice.bcc.bcc_spin_axis` documents $U=u\mathbb 1-i\,\mathbf n\cdot\sigma$. The sign convention differs, though unitarity and the commutant count are unaffected (OTHER). The docstring and `summary()` cite "F298's structural $N_c\le3$" as agreeing, and that bound was withdrawn by F325 (SUPERSEDED reference). L136–137 compute `mat` twice (dead code, harmless).

### `engine/gauge/derive_x1_branch.py` — X1 resolved: Casimir branch closed, centre branch adopted (F325)
**Status:** live · standalone · **Findings:** F325 F324 F303 F299 F298 F294 F144 F111b F110 F101 F280 · **Lattice:** n/a (character rotor; BCC 4-bond count) · **Law:** n/a · **Units:** lattice / GeV (quoted)

**Does:** audits the magnetic side of C7 against a genuine SU(N) character rotor. It exposes the F111b T7 1-vs-4-link artefact and the $\sigma_1$ offset $\ln((N^2-1)/2)$, and assembles the branch verdict.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $d_\lambda=\prod_{i<j}\frac{\lambda_i-\lambda_j+j-i}{j-i}$; $F\otimes R$ by adding one box (strip height-N columns) | SU(N) irrep dim and fusion | `derive_x1_branch.py:L162–169 _dim()`, `L181–193 _fuse_box()` | exact (reg) |
| 2 | $H=\tfrac{g^2}2n\,C_2(R)\,\delta_{RR'}-\tfrac\lambda2(\chi_F+\chi_{\bar F})$; $s_1=\langle\chi_F\rangle/d_F$ | SU(N) character rotor, ground state | `derive_x1_branch.py:L227–236 suN_character_rotor_s1()` | machine (eigh) (reg: exact; row is weaker — see flags) |
| 3 | $H=m^2/(2\chi)-\lambda\cos\phi$; $s_1=\langle e^{i\phi}\rangle$ | U(1) rotor (F101), $\lvert m\rvert\le40$ | `derive_x1_branch.py:L246–254 u1_rotor_s1()` | machine (reg: exact; row is weaker — see flags) |
| 4 | magnetic adjacency entries $\in\{0,1\}$ in both theories | magnetic term adds no factor to χ | `derive_x1_branch.py:L270–278 magnetic_adjacency_is_unit()` | exact (reg) |
| 5 | $s_1^{SU(N)}/s_1^{U(1)}\to2/(N^2-1)$ at equal $n$ (first-order PT: $s_1=4\lambda/(g^2n(N^2-1))$ vs $2\lambda/(ng^2)$) | ratio law, Richardson-extrapolated in λ | `derive_x1_branch.py:L325–329 s1_ratio_law()` | quantitative ($<10^{-7}$) (reg: exact; row is weaker — see flags) |
| 6 | gap ratio $\frac{\frac{g^2}2\cdot4}{\frac{g^2}2\cdot1\cdot C_F}=4/C_F=3$ | F111b T7 link-count defect | `derive_x1_branch.py:L367–375 f111b_link_count_defect()` | exact (reg) |
| 7 | $\Delta\sigma_1=\ln\frac{N^2-1}2=\ln4$ at $N=3$ | string-tension offset SU(3) vs Z_3/U(1) (affects F99–F101) | `derive_x1_branch.py:L390 sigma_offset_su3_vs_zn()` | exact (reg) |
| 8 | at $a=b$: $\omega=b$ ⇒ $\chi=1/\Omega(k)$ | circularity fixes ratio only; χ=1 is a normalisation | `derive_x1_branch.py:L414–430 circularity_fixes_ratio_only()` | exact (reg) |

**Inputs → outputs:** `su3_cut`, `magnetic_scale` → 7 checks X1–X7 + verdict. **Depends on:** `su3_ladder`, `casimir_ladder` (05a/c), `derive_coupling_normalisation.casimir_branch_vs_f280_band`. **Flags:** ⚠ DOC/CODE MISMATCH: `branch_verdict` hardcodes branch B $\alpha_s(M_Z)=0.11954$ (L472), where the docstring (L11) and the actual `_run_to_mz(1/16π)` give 0.1186 (0.11858, spot-checked). `import numpy as np` directly (L136) is a D8 violation in a spine module (OTHER). The `n_links` parameter of `check_x1_branch` is recorded but unused (OTHER).

### `engine/gauge/em_current.py` — the U(1) current the BCC walk conserves (F384, F389)
**Status:** live · standalone · **Findings:** F389 F384 · **Lattice:** BCC · **Law:** n/a (current of the Weyl walk) · **Units:** lattice

**Does:** builds the exactly-conserved longitudinal current from one walk tick, the naive Noether current, and (F389) the full current = exact longitudinal + naive transverse.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\rho=q(\lvert f\rvert^2+\lvert g\rvert^2)$ | charge density | `em_current.py:L149 charge_density()` | machine (reg) (row read: exact) |
| 2 | $J^i=q\,\psi^\dagger\sigma^i\psi$ | naive continuum Weyl current (closes continuity only to $O(ka)$) | `em_current.py:L162–164 bcc_naive_current()` | quantitative (reg: machine; row is weaker — see flags) |
| 3 | $\tilde J(k)=i\,\hat C(k)\,[\tilde\rho(t{+}1)-\tilde\rho(t)]/\lvert C(k)\rvert$, $\tilde J=0$ where $C=0$ | minimal longitudinal solution of discrete continuity | `em_current.py:L213–217 conserved_current()` | machine (reg) |
| 4 | $\tilde\rho(t{+}1)-\tilde\rho(t)+i\,C(k)\cdot\tilde J(k)=0$ | discrete continuity residual ($C$ = `bcc_curl_symbol`) | `em_current.py:L219, L247 continuity_residual()` | machine (reg) |
| 5 | $\max\lvert\Delta\tilde\rho\rvert$ on the 7 non-zero BZ corners where $C\equiv0$ | disclosed Nyquist gap (shrinks with packet bandwidth) | `em_current.py:L222 conserved_current()` | quantitative (reg: machine; row is weaker — see flags) |
| 6 | $J_T=\Pi_\perp^{C}\,J_\text{naive}$ | transverse (radiative) projection of #2 | `em_current.py:L373–375 noether_transverse_current()` | machine (reg) |
| 7 | $J=J_L^\text{(3)}+J_T^\text{(6)}$ | full current; continuity unaffected by $J_T$ | `em_current.py:L392–394 full_current()` | machine (reg) |

**Inputs → outputs:** Weyl $(f,g)$ on $L^3$, sign, $q$ → $(J,\text{residual},\text{gap})$; gates `check_conserved_current` (F384) and `check_full_current` (F389). **Depends on:** `lattice.bcc.weyl_step_3d_bcc` (03-lattice.md), `charge_coupling.bcc_curl_symbol` (05a/c), `em_photon_sourcing.split_transverse_longitudinal`, `core.coupled.gaussian_packet` (04-core.md). **Flags:** ⚠ DOC/CODE MISMATCH: the docstring (L75, L410) claims the transverse addition leaves continuity "bit-identical, to the last ULP", but the gate tests $<10^{-12}$ (L467) and $<10^{-10}$ (L474). The naive current uses $\sigma$, while the BCC walk's low-$k$ block is in the conjugate representation $\sigma^*$ (see derive_charge_partition #5). This sign on the $y$-component is not addressed in the naive/transverse current (OTHER). The docstring also records that momentum is not exactly conserved (independently derived recoil and sourcing).

### `engine/gauge/em_photon_sourcing.py` — Ĉ(k) anisotropy, Ω_pair/|C| mismatch and the T/L sourcing split (F387, F391)
**Status:** live · standalone · **Findings:** F391 F390 F387 F386 F384 · **Lattice:** BCC · **Law:** even (paired-spinor photon `photon.photon_step_spectral`, decision 5) · **Units:** lattice

**Does:** shows that scalar-rotation propagation plus $E\mathrel{+}=gJ$ with a longitudinal $J$ creates a monopole $B$. It fixes this by propagating only the $\hat C$-transverse sector and solving the longitudinal $E$ from Gauss's law. It also builds a mode-by-mode $\hat C$-transverse beam.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\angle(\hat C(k),\hat k)$; $\hat C\to(k_x,-k_y,k_z)/\lvert k\rvert$: 0° on x/z, 180° on y, 90° face diagonal, $\arccos\tfrac13$ body diagonal | curl-direction anisotropy | `em_photon_sourcing.py:L105–106 curl_direction_angle()` | unknown (inferred: machine) |
| 2 | $V_L=C\,(C\cdot\tilde V)/\lvert C\rvert^2$, $V_T=\tilde V-V_L$ (all of $V$ in $V_T$ where $C=0$) | $C$-transverse/longitudinal split | `em_photon_sourcing.py:L136–141 split_transverse_longitudinal()` | unknown (inferred: machine) |
| 3 | $\lVert i\,C\cdot\tilde B\rVert_2$ | no-monopole residual | `em_photon_sourcing.py:L152–153 iC_dot_B_norm()` | unknown (inferred: machine) |
| 4 | per tick: $(E,B)\leftarrow R(\Omega_\text{pair})(E,B)$, $E\leftarrow E+gJ$ | naive recipe (control; violates #3) | `em_photon_sourcing.py:L177–178 naive_sourced_scenario()` | n/a (control) |
| 5 | $(E_T,B_T)\leftarrow R(\Omega_\text{pair})(E_T,B_T)$, $E_T\mathrel{+}=gJ_T$; $\rho\mathrel{+}=-iC\cdot\tilde J$; $\tilde E_L=-iC\tilde\rho/\lvert C\rvert^2$ (i.e. $iC\cdot E_L=\rho$); $B_L\equiv0$ | split sourcing fix | `em_photon_sourcing.py:L209–226 split_sourced_scenario()` | unknown (inferred: machine ($iC\cdot B<10^{-8}$)) |
| 6 | $[R(\Omega),\Pi_{T/L}]=0$ | scalar per-mode rotation commutes with the projection | `em_photon_sourcing.py:L280–290 check_em_photon_sourcing()` | unknown (inferred: machine ($<10^{-12}$)) |
| 7 | $\Omega_\text{pair}/\lvert C\rvert\to1$ at small $k$, $>1.3$ near the zone edge | propagator vs curl-symbol value mismatch | `em_photon_sourcing.py:L272–274` | unknown (inferred: quantitative) |
| 8 | $e(k)=\mathrm{normalize}(v_0-\hat C(\hat C\cdot v_0))$; $E=\mathrm{Re}\,\mathcal F^{-1}[\tilde F e]$, $B=\mathrm{Im}\,\mathcal F^{-1}[\tilde F e]$, $F=\text{env}\cdot e^{ik_0x}$ | mode-wise $C$-transverse beam packet | `em_photon_sourcing.py:L440–452 build_ck_transverse_beam_packet()` | unknown (inferred: machine) |

**Inputs → outputs:** $L$, $g_\text{lat}$, current from `em_current.conserved_current` → 12 checks (F387). `check_ck_transverse_beam_mechanism` runs a coupled `EmPhotonChannel`/`FermionEmChannel` Simulation (F391, 9 checks; `_push_scenario` is harness plumbing). **Depends on:** `photon.photon_step_spectral`, `photon.pair_dispersion` (05a), `charge_coupling.bcc_curl_symbol`, `core.coupled` / `core.simulation` / `core.observers` (04-core.md). **Flags:** EXACTNESS unknown (registry has no class). In #5 the transverse sector is sourced with $+gJ_T$, but $E_L$ solves $iC\cdot E_L=+\rho$ with no factor $g$. The naive accumulation $E_L=\sum gJ_L$ would instead give $iC\cdot E_L=-g\rho$, so the relative sign and coupling of the two sectors is inconsistent. This is not settled here (OTHER, open). The docstrings write "$i\hat C\cdot E_L=\rho$", but the code uses the unnormalised $C$ (notation only).

### `engine/gauge/emission.py` — hydrogenic lines and Einstein A (P1)
**Status:** live · test-only · **Findings:** none in registry (docstring F125, F156, F120) · **Lattice:** n/a (radial 1-D grid via `particles.atom`) · **Law:** n/a · **Units:** eV / nm / s (atomic units → SI)

**Does:** computes the hydrogenic spectral lines and electric-dipole spontaneous-emission rates from the F125 radial solver.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $E_n=-Z^2\,\mathrm{Ry}/n^2$ | level energy (Ry from `atom.RY_EV_CODATA`) | `emission.py:L51 level_eV()` | unknown |
| 2 | $\lambda=hc/(E_i-E_f)$, $hc=1239.841984$ eV·nm | line wavelength | `emission.py:L61 wavelength_nm()` | unknown |
| 3 | $d=\int u_f\,x\,u_i\,dx$ (rectangle rule, $h$) | reduced radial dipole | `emission.py:L89 radial_dipole()` | unknown |
| 4 | $A=\tfrac43\alpha^3\omega^3\frac{l_>}{2l_i+1}\lvert d/Z\rvert^2/t_\text{au}$, $\omega=\tfrac12Z^2(n_f^{-2}-n_i^{-2})$; 0 unless $\Delta l=\pm1$ | Einstein A, s⁻¹ | `emission.py:L100–106 einstein_A_si()` | unknown |

**Inputs → outputs:** $(n,l)$ pairs, $Z$ → eV, nm, s⁻¹, lifetimes. **Depends on:** `particles.atom` (06a/b). **Flags:** EXACTNESS unknown. $\omega$ uses exact Bohr levels ($\tfrac12Z^2\Delta(1/n^2)$ Ha), not the solver's eigenvalues `Ei/Ef`, which are computed and discarded (L84–85) (OTHER). Unregistered literals $t_\text{au}$ and $hc$ (L42–43). `sys.path` insertion (L34–36) is legacy plumbing. Direct `numpy` import (D8 debt).

### `engine/gauge/factorization.py` — a vector as two null vectors; a null vector as a spinor outer product (F397)
**Status:** live · standalone · **Findings:** F397 F24 F69 F91 F168 F169 · **Lattice:** BCC dispersion (constituent/pair defects) · **Law:** even (pair $\Omega_\text{even}$ vs legs) · **Units:** lattice / abstract Minkowski

**Does:** checks the notebook's factorisation theorems T1/T2 in closed-form 2×2 algebra and corrects the notebook's boxed $a_0$. It also measures leg and pair defects of the BCC paired-spinor dispersion.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sigma\!\cdot\!V=\begin{pmatrix}V_0-V_z&-V_x+iV_y\\-V_x-iV_y&V_0+V_z\end{pmatrix}$, $\det=V\cdot V$; $\bar\sigma\!\cdot\!V=\sigma_y(\sigma\!\cdot\!V)^T\sigma_y$ | notebook p.176 convention | `factorization.py:L47 sigma_dot()`, `L53 sigma_bar_dot()` | quantitative (reg) (row read: exact) |
| 2 | $a=a_0(1,\hat a)$, $a_0=\dfrac{V\cdot V}{2(V_0-\hat a\cdot\vec V)}$, $b=V-a$ (both null) | T2 corrected decomposition | `factorization.py:L73 t2_decompose()` | quantitative (reg) (row read: machine ($<10^{-12}$)) |
| 3 | notebook boxed $a_0=(V_0^2-\lvert\vec V\rvert^2+2\hat a\cdot\vec V)/(2V_0)$ | declared-wrong control (not null) | `factorization.py:L75 t2_decompose(formula="notebook")` | n/a (control) |
| 4 | $\psi=e^{i\theta}(\sqrt{N_0-N_z},\,(-N_x-iN_y)/\sqrt{N_0-N_z})$, $\psi\psi^\dagger=\sigma\!\cdot\!N$ | T1 null vector → spinor | `factorization.py:L86–93 t1_spinor()` | quantitative (reg) (row read: machine) |
| 5 | $\sqrt M=(M+\sqrt{\det M}\,\mathbb 1)/\sqrt{\mathrm{tr}M+2\sqrt{\det M}}$ | closed-form Hermitian square root (no chiral eigensolver) | `factorization.py:L102–104 sqrtm_herm2()` | quantitative (reg) (row read: exact) |
| 6 | $S=\cosh r\,\mathbb 1+\frac{\sinh r}{r}\,z\!\cdot\!\sigma$, $z=\tfrac12(\zeta-i\theta)$; $V\to S(\sigma\!\cdot\!V)S^\dagger$ | SL(2,ℂ) covariance of T2 | `factorization.py:L116 sl2c_element()`, `L121 lorentz_act()` | quantitative (reg) (row read: machine) |
| 7 | $\delta_\pm=\omega^\pm(k/2)^2-(c_\text{lat}\lvert k/2\rvert)^2\sim k^3$ (opposite signs); $\Omega_\text{even}^2-(c_\text{lat}\lvert k\rvert)^2\sim k^4$ | leg vs pair defects ($c_\text{lat}=1/\sqrt3$, F26) | `factorization.py:L145–147 _pair_lattice()` | quantitative (reg) |
| 8 | $\omega^+(q)=c\lvert q\rvert+\epsilon(q)+O(q^3)$, $\epsilon=-q_xq_yq_z/(3\lvert q\rvert)$ | leading odd-chirality term | `factorization.py:L152 _eps()` | quantitative (reg) |
| 9 | $E_0(p;k)=\omega^+(k/2+p)+\omega^-(k/2-p)$; $\Omega_\text{even}-\min_pE_0=\lvert\epsilon(k)\rvert+O(k^3)$ | F169 two-body threshold offset (pattern search) | `factorization.py:L156 _E0()`, `L159–175 _threshold()` | quantitative (reg) |
| 10 | $\mathcal A=\mathrm{Im}\,\psi^\dagger\nabla\psi$, $\mathcal A\to\mathcal A+\nabla\theta$; $F=\tfrac12\hat n\cdot(\partial_x\hat n\times\partial_y\hat n)$ | Berry connection of the T1 phase (local U(1)) | `factorization.py:L358–363, L377–384 _u1_checks()` | quantitative (reg) |

**Inputs → outputs:** seed, $n$, `formula` → ~20 checks + measurements. **Depends on:** `lattice.bcc.bcc_dispersion` (03-lattice.md), `constants.c_lat`. **Flags:** none.

### `engine/gauge/gluon.py` — dynamical SU(3) gluon: even-law propagator, plaquette, Yang–Mills tick, Wilson loops, colour-current source
**Status:** partial · driven (15 ch) · **Findings:** none in registry (docstring FG-7/F43; F29, F33, F36, F91, F265) · **Lattice:** BCC (canonical) and 2D square (reference, D1) · **Law:** **even** (`gluon_rotation_step_spectral_bcc`, F91); chiral retained · **Units:** lattice

**Does:** propagates the colour-octet $(E^a,B^a)$ with the F26 rotation law applied independently to each $a$. It also extracts $G^a_{\mu\nu}$ from Wilson plaquettes, applies an $f^{abc}$ self-coupling tick, measures Wilson loops, and sources $E^a$ with the quark colour current.

**The two BCC rotation laws, verified from code.** Both act per Fourier mode on the complex FFT of the real fields and keep `.real` after the inverse FFT.
- **EVEN (canonical, migrated 2026-06-04, F91)**: `gluon_rotation_step_spectral_bcc` (L167). $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$ (L202–204, with $\omega^\pm=\arccos u^\pm$ from `bcc.bcc_dispersion`), then $\tilde E'=\cos\Omega\,\tilde E+\sin\Omega\,\tilde B$ and $\tilde B'=-\sin\Omega\,\tilde E+\cos\Omega\,\tilde B$ (L210–211), i.e. $\tilde E+i\tilde B\to e^{-i\Omega_\text{even}}(\tilde E+i\tilde B)$. The spot-check on $L=6$, 8 colours found residual $2.2\times10^{-14}$ against $C_0e^{-i\Omega_\text{even}}$. $\Omega_\text{even}(-k)=\Omega_\text{even}(k)$, so realness is preserved exactly.
- **CHIRAL (retired, comparison only)**: `gluon_rotation_step_spectral_bcc_chiral` (L215). This calls `weak_wmu.w_propagation_step_spectral` (≡ `w_propagation_step_chiral`, `weak_wmu.py:L889–918`) on colour triples (8 padded to 3+3+2). There $F^\pm=\tilde E\pm i\tilde B$, $F^+\to e^{-i\Omega^+}F^+$ and $F^-\to e^{+i\Omega^-}F^-$ with $\Omega^\pm=2\omega^\pm(k/2)$. On even grids the Nyquist bins use $\Omega^\pm\to\tfrac12(\Omega^++\Omega^-)$ (`weak_wmu._chiral_dispersions`, L698). The output is $E=\mathrm{Re}\,\mathcal F^{-1}[(F^+{}'+F^-{}')/2]$ and $B=\mathrm{Re}\,\mathcal F^{-1}[-\tfrac i2(F^+{}'-F^-{}')]$. It differs from the even step by $O(1)$ on random fields (0.42 at $L=6$). This is birefringent.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $[T^a,T^b]=if^{abc}T^c$; $f^{123}=1$, $f^{147}=f^{246}=f^{257}=f^{345}=\tfrac12$, $f^{156}=f^{367}=-\tfrac12$, $f^{458}=f^{678}=\tfrac{\sqrt3}2$ | SU(3) structure constants (totally antisymmetric) | `gluon.py:L77–85 _build_f_su3()` | unknown |
| 2 | $f^{abe}f^{ecd}+f^{bce}f^{ead}+f^{cae}f^{ebd}=0$ | Jacobi residual | `gluon.py:L109–111 structure_constants_jacobi_residual()` | unknown |
| 3 | $\Omega_{2D}(k)=2\,\omega_{2D}(k/2)$, $\omega_{2D}=\arccos[\cos\tfrac{k_x}{\sqrt2}\cos\tfrac{k_y}{\sqrt2}]$; same $2\times2$ rotation | 2D reference gluon step, per $a$ | `gluon.py:L134–140 _rotation_step_em_scalar_2d()` | unknown |
| 4 | $\Omega_\text{even}=\omega^+(k/2)+\omega^-(k/2)$; $(\tilde E,\tilde B)\to R(\Omega_\text{even})(\tilde E,\tilde B)$ | **BCC gluon step (even, F91)** | `gluon.py:L204, L210–211 gluon_rotation_step_spectral_bcc()` | unknown (inferred: machine (spot-check $2\times10^{-14}$); registry unknown) |
| 5 | $F^\pm\to e^{\mp i\Omega^\pm}F^\pm$, $\Omega^\pm=2\omega^\pm(k/2)$ | retired chiral BCC step (via `weak_wmu`) | `gluon.py:L232/L239 gluon_rotation_step_spectral_bcc_chiral()` | unknown — **SUPERSEDED by F91** (S2-F91-gluon-chiral-to-even) |
| 6 | $\omega_\text{eff}=\sqrt{m_g^2+\Omega_\text{even}^2}$, rotate by $\omega_\text{eff}\,dt$; $m_g=0$ returns #4 exactly | Proca-style massive gluon (via `weak_wmu.w_massive_propagation_step_spectral`) | `gluon.py:L258, L265–274 gluon_massive_step_spectral_bcc()` | unknown |
| 7 | $G^{a,1}=\sum(\psi_\uparrow^\dagger T^a\psi_\downarrow+\psi_\downarrow^\dagger T^a\psi_\uparrow)$, $G^{a,2}=i\sum(\psi_\downarrow^\dagger T^a\psi_\uparrow-\psi_\uparrow^\dagger T^a\psi_\downarrow)$, $G^{a,3}=\sum(\psi_\uparrow^\dagger T^a\psi_\uparrow-\psi_\downarrow^\dagger T^a\psi_\downarrow)$, summed over flavours and both chiralities | Hermitian colour-octet σ-bilinear (W/Z/gluon use permitted) | `gluon.py:L340–342 (2D)`, `L378–380 (BCC) quark_colour_octet_bilinear_*()` | unknown (F302: covariant at $<10^{-12}$) |
| 8 | $G\to R_\text{adj}(V)G$; $\lVert G\rVert^2=\sum\lvert G^{a,i}\rvert^2$ | adjoint rotation, octet norm | `gluon.py:L397 octet_adjoint_rotate()`, `L386 octet_norm_sq()` | unknown |
| 9 | $U_\square=U_\mu(x)U_\nu(x{+}\hat\mu)U_\mu^\dagger(x{+}\hat\nu)U_\nu^\dagger(x)$; $G^a_{\mu\nu}=2\,\mathrm{Im\,Tr}(T^aU_\square)/(g\,a^2)$ | 2D plaquette field strength | `gluon.py:L416 plaquette_matrix_su3_2d()`, `L442 plaquette_field_strength_su3_2d()` | unknown |
| 10 | $W^a=\tfrac1{n_\text{dir}}\sum_\mu2\,\mathrm{Im\,Tr}(T^aU_\mu)$; $\delta W^a=g\,dt\,f^{abc}W^bG^c$; $U_\ell\leftarrow e^{i\delta W^aT^a}U_\ell$ | Yang–Mills self-coupling tick (2D; BCC uses $G=\tfrac13(G_{xy}+G_{xz}+G_{yz})$) | `gluon.py:L473–485 gluon_self_coupling_step_2d()`, `L612–630 _bcc()` | unknown |
| 11 | $V(x)=\exp(i\theta^a(x)T^a)$ via batched `eigh` of $H=\theta^aT^a$ | su(3) exponential field | `gluon.py:L504–511 _su3_expmap_field()` | unknown |
| 12 | BCC $G^a_{\mu\nu}$ on the genuine 4-bond rhombus plaquettes (6 orientations, area $2\sqrt2$) | delegated to `bcc_action.plaquette_field_strength_su3` (F265) | `gluon.py:L561 plaquette_field_strength_su3_bcc()` | unknown |
| 13 | composite-SC plaquette from length-2 link pairs, $a^2=4$ | deprecated F265 no-go reproduction | `gluon.py:L587–600 _plaquette_field_strength_su3_composite_sc()` | unknown (inferred: **SUPERSEDED by F265**) |
| 14 | $W(r,t)=\mathrm{Re\,Tr}\prod_\text{rect}U$; $\langle W\rangle$ averaged over corners; $\langle W\rangle\approx N_ce^{-\sigma rt}$ | Wilson loops (2D) | `gluon.py:L687 wilson_loop_2d_rect()`, `L697 _avg()`, `L715 area_law_data()` | unknown |
| 15 | $\tilde E^a\leftarrow$ #4, then $E^a\mathrel{+}=g\,J^a\,dt$ | colour-current back-reaction (linearised YM, diagonal in $a$) | `gluon.py:L767–768 (2D)`, `L778–779 (BCC) gluon_sourced_step_*()` | unknown |
| 16 | $\max_k\lvert C_n-C_0e^{-i\Omega_\text{even}n}\rvert/\lvert C_0\rvert$, $C=\tilde E+i\tilde B$ | free-gluon dispersion check (even law) | `gluon.py:L813–818 free_gluon_dispersion_residual_bcc()` | unknown |

**Inputs → outputs:** octet fields `(8,L,L,L)` real, link lists (8 BCC directions × `(L,L,L,3,3)`), quark dicts → updated fields and links, $G^a_{\mu\nu}$, loop traces. `link_unitarity_residual_su3` (L634) and `make_su3_link_field_bcc` (L825) are plumbing/initialisers. **Depends on:** `lattice.bcc.bcc_dispersion` (03-lattice.md), `weak_wmu` (`_kgrid3d`, `_omega_even`, chiral and massive steps; 05a/c), `bilinear_2d.rotation_omega_2d`, `strong` (T_GEN, adjoint_rotation, noether currents), `bcc_action`. **Flags:** EXACTNESS unknown (registry `None`, status `partial`, no findings attached in registry → OTHER: F91/F43/F265 not linked). `numpy` is imported directly (D8 debt). The even law is confirmed as canonical in code, and the chiral step is correctly retained only for comparison (no mismatch). The massive step at $m_g\neq0$ uses $\Omega_\text{even}$, consistent with #4.

### `engine/gauge/gluon_self_energy.py` — residual A: tadpole-free lock and the q* bracket (F155)
**Status:** live · test-only · **Findings:** none in registry (docstring F144, F151, F154, F155) · **Lattice:** BCC dispersion, midpoint BZ grids (3D/4D, 4th leg continuum) · **Law:** even · **Units:** lattice ($q^*$ in $1/a$)

**Does:** shows the rule's link update is exactly SO(2), so there is no Wilson tadpole. It checks that the gluon is luminal, builds a continuum-subtracted scalar bubble and Lepage–Mackenzie $q^*$, and brackets $q^*\in[1/\sqrt3,\,\sim0.97]/a$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_\text{even}=\omega^+(k/2)+\omega^-(k/2)\to c_\text{lat}\lvert k\rvert$, $c_\text{lat}=1/\sqrt3$ (F26) | rule gluon dispersion; luminality check | `gluon_self_energy.py:L93–95 omega_even()`, `L157–158 gluon_is_luminal()` | unknown (docstring "machine") |
| 2 | $K_3=3\Omega_\text{even}^2$, $K_4=3\Omega_\text{even}^2+k_t^2$ | inverse propagators (normalised to $\lvert k\rvert^2$) | `gluon_self_energy.py:L101, L107 K_true_3d/4d()` | unknown |
| 3 | $\lvert E'\rvert^2+\lvert B'\rvert^2=1$, $\det R=1$ for `_f26_rotation_step` ⇒ $u_0=1$; contrast $Z_0^W=\langle1/\hat K^2\rangle$, $\hat K^2=4\sum\sin^2(k_\mu/2)$ | tadpole sector empty | `gluon_self_energy.py:L129–139 tadpole_sector_empty()` | unknown (docstring "exact") |
| 4 | $B(p)=\langle1/(K(k)K(k+p))\rangle_\text{BZ}$, lattice vs continuum, unwrapped shift | scalar vacuum-polarisation bubble | `gluon_self_energy.py:L178–183 _bubble()` | unknown (inferred: quantitative) |
| 5 | $d_1^\text{bubble}=16\pi^2(B_\text{lat}-B_\text{cont})$ | subtracted finite constant (grid-convergent) | `gluon_self_energy.py:L214 subtracted_bubble_constant()` | unknown (inferred: quantitative) |
| 6 | $\ln(q^{*2}a^2)=\langle\ln(K_\text{lat}/K_\text{cont})\rangle_w$, $w\in\{1,1/K,1/K^2\}$ | Lepage–Mackenzie $q^*$, continuum-subtracted | `gluon_self_energy.py:L250–251 qstar_lm_subtracted()` | unknown (inferred: quantitative) |
| 7 | $\Lambda_{\overline{MS}}/\Lambda_\text{rule}=\exp\!\big[\tfrac{a_1/4\pi+2b_0\ln(1/q^*a)}{2b_0}\big]$, $a_1=(31C_A-10n_f)/9=11/3$, $b_0=(11-2n_f/3)/4\pi$ | Λ-ratio from $q^*$ | `gluon_self_energy.py:L316–318 lambda_ratio()`, `L84 B0_ALPHA` | unknown (inferred: exact (formula)) |

**Constants:** `c_lat` $=1/\sqrt3$ (F26, exact); `q_star_a_band_lo` $=1/\sqrt3$ (F151/F155, exact; a separate constant from `c_lat` by design); `q_star_a_implied` $=0.7327$ (F151/F155, quantitative, PDG-implied). **Inputs → outputs:** grid sizes → q* bracket, Λ-ratio bracket (`qstar_highres`, L324, a runner hook). **Depends on:** `lattice.bcc`, `weak_wmu._f26_rotation_step`. **Flags:** EXACTNESS unknown (registry `None`, no findings attached: OTHER). Unregistered literals `GEOM_MEAN_BAND=3^{-1/4}`, `C_A=3`, targets 1.78/28.81/0.348. `numpy` is imported directly (D8 debt). The "open" gluonic 3g+ghost finite part is declared unfinished.

### `engine/gauge/hypercharge.py` — U(1)_Y carried on U(x); Higgs-free mass step (F41, F42)
**Status:** live · driven (6 ch) · **Findings:** none in registry (docstring F27, F41, F42, F165, F279, F47) · **Lattice:** 2D square (kinetic step `dirac._weyl_half_step_2c`; reference, D1) · **Law:** n/a (Weyl QCA kinetic) · **Units:** lattice

**Does:** implements **design decision 3** as the code does it. The pure-gauge SU(2)_L field $U(x)$ of the F27 mass step is extended by a site-centred, pure-gauge U(1)_Y angle $\alpha(x)$, so the mass step is SU(2)_L × U(1)_Y invariant with no Higgs field. $\alpha$ is never evolved dynamically; it is only shifted under gauge transformations. Right-handed singlets get a Stueckelberg-wrapped kinetic half-step.

**Constants.** $Y_{L}=-1$ (`Y_LEPTON_L`, F165/F279, exact; the unit of charge), $Y_{e_R}=2Y_L=-2$ (`Y_E_R`, F165/F279, exact), $Y_{\nu_R}=0$ (`Y_NU_R`, F279/F47/F266, exact). $\Delta Y_e=Y_L-Y_{e_R}=+1$ and $\Delta Y_\nu=Y_L-Y_{\nu_R}=-1$ are computed as `Fraction`s (L159–160). The quark values $Y_{Q_L}=\tfrac13$, $Y_{u_R}=\tfrac43$, $Y_{d_R}=-\tfrac23$ are **unregistered float literals**, deliberately so because they depend on $N_c=3$ (L317–336). This gives $\Delta Y_u=-1$ and $\Delta Y_d=+1$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $M=\cos m\,\mathbb 1+i\sin m\begin{pmatrix}0&U\,D(\alpha)\\D^\dagger(\alpha)U^\dagger&0\end{pmatrix}$, $D=\mathrm{diag}(e^{i\alpha\Delta Y_\nu/2},e^{i\alpha\Delta Y_e/2})$, $U=\begin{pmatrix}U_a&-\bar U_b\\U_b&\bar U_a\end{pmatrix}$ | lepton mass step with hypercharge absorbed in $U(x)$ (the F41 construction); $\alpha\equiv0$ gives the F27 step exactly | `hypercharge.py:L229–259 mass_step_doublet_su2xu1y()` (η at L243–246, χ at L256–259) | unknown |
| 2 | $\psi\to e^{i\beta Y_\psi/2}\psi$ ($Y_L$ on η, $Y_{\nu_R}$ on $\chi_\nu$, $Y_{e_R}$ on $\chi_e$) with $\alpha\to\alpha+\beta$ | U(1)_Y gauge transformation and compensating shift (Ward identity Y1/Y2) | `hypercharge.py:L278–282 apply_u1y_transform()`, `L291 u1y_shift_alpha()` | unknown |
| 3 | $(e^{i\beta Y_L/2},e^{i\beta Y_{\nu_R}/2},e^{i\beta Y_{e_R}/2})$ | per-chirality covariant phases (docstring: exact only for global β) | `hypercharge.py:L307–309 covariant_phase_per_chirality()` | unknown |
| 4 | same as #1 with $D=\mathrm{diag}(e^{i\alpha\Delta Y_u/2},e^{i\alpha\Delta Y_d/2})$, one colour at a time | quark mass step (F42) | `hypercharge.py:L385–410 mass_step_quark_doublet_su2xu1y()` | unknown |
| 5 | $\chi'=e^{+i\alpha Y_R/2}\,K_{dt/2}\,e^{-i\alpha Y_R/2}\chi$; $S_{\alpha+\beta}(e^{i\beta Y/2}\chi)=e^{i\beta Y/2}S_\alpha(\chi)$ exactly | Stueckelberg-wrapped U(1)_Y-covariant kinetic half-step for $e_R,u_R,d_R$ | `hypercharge.py:L479–484 kinetic_half_step_chi_u1y()`, `L501–503 _singlets_all()` | unknown (covariance exact by algebra) |

**Inputs → outputs:** 8 Weyl components on an $(L_x,L_y)$ grid, $U_a,U_b$ ($\lvert U_a\rvert^2+\lvert U_b\rvert^2=1$), $\alpha(x)$, $m$, $dt$ → the updated 8-tuple. `make_u1y_field` (L168) is an initialiser. **Depends on:** `particles.dirac._weyl_half_step_2c` (06a), `casim.constants` (01-constants.md). Consumed by `derive_charge_partition` Leg B. **Flags:** EXACTNESS unknown (registry `None`, no findings attached: OTHER). The docstring of #1 says $E_\text{phase}$ "acts on the isospin index AFTER U". The code applies $D(\alpha)$ to χ before $U$ (L236–241 comment), i.e. $U\cdot D$. The matrix is consistent, but the wording is reversed (⚠ DOC/CODE MISMATCH, minor). The kinetic wrap #5 makes χ̃ gauge-invariant, so a local α enters only through the wrap phases. It is not a dynamical B-field, and there is no U(1)_Y kinetic/field-strength term anywhere in this module. `numpy` is imported directly (D8 debt).
