# Gauge sector (a): actions, the σ-bilinear construction, charge coupling and colour

*Model map section p05a. Written 2026-09-28 - 00:00. Source of truth: the code under `src/casim/engine/gauge/`. Line numbers are from the files as they stood on 2026-09-27 (tree `ed51277` plus the working-tree edits).*

This section maps fourteen modules in the gauge sector, taken in path order. They are the BCC Wilson action and its 3+1D sampler, the continuum background-field b₀ gate, the retired σ-bilinear "composite photon" (3-D BCC and 2-D square), the U(1) charge-coupling path (Aharonov–Bohm holonomy plus the sourced curl step), the Coulomb-gauge A convention, the SU(2) charged current, the ABJ anomaly, and the colour modules (Casimir ladder and scaling, condensate, dielectric, θ).

**Conventions shared by this batch**
- **Lattice (D1).** BCC is canonical. Two conventions for the BCC hop appear here. The *action* modules (`bcc_action`) use a conventional cubic cell of side 2, where a hop is the integer vector $d\in\{\pm1\}^3$ and `np.roll` is an exact translation. The *spectral* modules use the momentum-space walk $u^\pm(k)=c_xc_yc_z\pm s_xs_ys_z$ with $c_i=\cos(k_i/\sqrt3)$ (`lattice/bcc.py:_bcc_uvec`, see 03-lattice.md). `bilinear_2d` runs on the 2-D square QCA (`core_exact._arccos_2d_uvec`, $c_i=\cos(k_i/\sqrt2)$), which is a **reference lattice, not canonical**.
- **Rotation laws (F91).** The *even* law is $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$. The *single-branch chiral* law is $\Omega^\pm(k)=2\omega^\pm(k/2)$. The σ-bilinear helpers in `bilinear.py` use the single-branch law $\Omega^+$. `charge_coupling.maxwell_curl_step` uses a third rate, $\theta=\lvert C_\text{odd}(k)\rvert$. It matches $\Omega_\text{even}$ only as $k\to0$ (flagged below).
- **Units.** Lattice units throughout (hop spacing 1, $c_\text{lat}=1/\sqrt3$, **F26**, exact, `constants/geometry.py`). The exceptions are `chiral_anomaly.pi0_to_gamma_gamma` (MeV/eV with PDG inputs) and `bgfield_loop` (continuum 4-D Euclidean).
- **σ-bilinear hazard (F65–F69).** `bilinear.py` / `bilinear_2d.py` still carry the RETIRED-AS-PHOTON banner. **Result of the audit:** no live photon channel calls `bilinear.py`. Its engine consumers are `gauge/derive_bilinear_so3.py` (an SO(3)-covariance derivation), two fork harnesses (`forks/lattice/smearing_fork_harness.py`, `forks/gauge/curl_fork_harness.py`), and historical test records in `tests/registry/gauge.yaml` (F20–F26, F306). The gluon code (`gluon.py`, `colour_dielectric.py`) uses `bilinear_2d` only for its **2-D square rotation rate** `rotation_omega_2d`. That is a propagator dispersion, not the σ-bilinear field construction, and it is not a photon.
- **D8.** Several modules still `import numpy as np` directly: `bcc_action`, `bgfield_loop`, `bilinear`, `bilinear_2d`, `charge_coupling` and `charged_current`. They are recorded in the flags file, not re-litigated here.

Modules covered: `__init__.py`, `a_field_convention.py`, `bcc_action.py`, `bgfield_loop.py`, `bilinear.py`, `bilinear_2d.py`, `casimir_ladder.py`, `casimir_scaling.py`, `charge_coupling.py`, `charged_current.py`, `chiral_anomaly.py`, `colour_condensate.py`, `colour_dielectric.py`, `colour_theta.py`.

---

### `engine/gauge/__init__.py` — package marker
**Status:** not in registry (package file) · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

Plumbing: an empty package docstring (a C3-era placeholder). It holds no equations.

---

### `engine/gauge/a_field_convention.py` — which vector potential A the U(1) link step reads
**Status:** live · standalone · **Findings:** F384 F385 F386 · **Lattice:** BCC (spectral curl symbol) · **Law:** photon free step = `photon.photon_step_spectral` (even, see 05b) · **Units:** lattice

**Does:** implements the two candidate conventions for $A$: *accumulate* ($A\leftarrow A+E$) and *solve* (Coulomb-gauge inversion of $B$). It also provides the diagnostics that pick *solve*: *solve*'s $A$ is purely $\hat C$-transverse, while *accumulate* inherits the longitudinal charge content of the F384 current.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A_{t+1}=A_t+E_t$ | "accumulate" convention (the `WSourcedChannel` pattern) | `a_field_convention.py:L65 accumulate_A()` | machine (reg) (row read: exact (definition)) |
| 2 | $f_\parallel=\dfrac{\big[\sum_{C\neq0}\lvert C\cdot\tilde A\rvert^2/\lvert C\rvert^2\big]^{1/2}}{\lVert\tilde A\rVert}$, with $C=C_\text{odd}(k)$ | $\hat C$-longitudinal fraction of $A$ | `a_field_convention.py:L88-89 longitudinal_fraction()` | machine (reg) |
| 3 | $E\leftarrow R_\text{photon}(E)+g_\text{lat}J,\ \ A\leftarrow A+E$ ($J$ = F384 current of a static Weyl packet, held fixed) | controlled accumulate scenario | `a_field_convention.py:L124-127 build_accumulate_scenario()` | machine (reg) |
| 4 | $A=\nabla\chi$, $\hat A_j=i k_j\hat\chi$, $\chi=a\sin(2\pi m x/L)$ | pure-gradient (gauge) test field | `a_field_convention.py:L144-151 pure_gradient_A()` | machine (reg) |
| 5 | $\max_{C\neq0}\lvert iC\times\hat A-\hat B_T\rvert$, $\hat B_T=\hat B-\hat C(\hat C\cdot\hat B)$ | solve recovers the transverse part of $B$ | `a_field_convention.py:L206-210 check_a_field_convention()` | machine (reg) |

**Inputs → outputs:** $(E,B)$ of shape (3,L,L,L), a Weyl packet → $A$, fractions, and a 7-leg checklist. The gate thresholds are $10^{-10}$, $10^{-8}$ and $10^{-20}$ (machine), plus two inequality legs. **Depends on:** `charge_coupling.bcc_curl_symbol` and `solve_A_coulomb_3d` (this file, below); `photon.photon_step_spectral` and `build_beam_packet` (05b); `em_current.conserved_current` (05b); `forks/gauge/u1_link_unitarity_forks.gauge_covariance_residual` (08a). **Flags:** the in-code comment (L212-222) records that sourcing $E$ with a purely longitudinal current under the scalar paired-photon rotation produces a nonzero, $\hat C$-longitudinal $B$ ("monopole" artifact, $i\hat C\cdot B\neq0$) because $\Omega_\text{pair}$ and $\lvert C_\text{odd}\rvert$ agree only at small $k$. This is a disclosed inconsistency between the photon propagator and the curl symbol (see `charge_coupling` flags).

---

### `engine/gauge/bcc_action.py` — Wilson gauge action on the genuine BCC lattice, 3-D and 3+1-D
**Status:** live · driven (29 ch) · **Findings:** registry lists none; the code and inventory cite F265, F299, F303, F313, F323 · **Lattice:** BCC (cubic cell of side 2, sites = same-parity integer points, index 4 in ℤ³) × ℤ Euclidean time · **Law:** n/a (action/Monte-Carlo, not a propagator) · **Units:** lattice ($\lambda=1$ per integer coordinate; $a_t$ derived)

**Does:** builds the 4-bond rhombic plaquettes of BCC. It reconstructs Cartesian $F^a_{\mu\nu}$ from the 6 plaquette orientations and defines the anisotropic $\mathrm{BCC}_3\times\mathbb Z$ Wilson action (6 rhombi + 4 mixed rectangles). It also provides a Cabibbo–Marinari heat-bath/over-relaxation sampler, Wilson/Creutz/Polyakov observables, the derived anisotropy $\beta_t/\beta_s=4/(3c_\text{lat}^2)$, and the higher-representation character loops for F299's $d=4$ Casimir test.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $B(x)=A(x+d)$ via integer roll | exact lattice translation (plumbing) | `bcc_action.py:L114 shift_by()` | unknown (inferred: exact) |
| 2 | $U_{-d}(x)=U_d(x-d)^\dagger$ | link-reversal identity (4 stored axis fields, 8 directions) | `bcc_action.py:L195 symmetrise_links()`; residual `L178-180 link_reversal_residual()` | unknown (inferred: exact) |
| 3 | $P(x)=U_{d_1}(x)\,U_{d_2}(x{+}d_1)\,U_{-d_1}(x{+}d_1{+}d_2)\,U_{-d_2}(x{+}d_2)$ | minimal rhombic plaquette (no 3-bond loops exist, F303) | `bcc_action.py:L222-228 bcc_plaquette()` | unknown (inferred: exact) |
| 4 | $s=\big\langle 1-\operatorname{Re}\operatorname{tr}P/N\big\rangle_{6\text{ orient., BCC sites}}$ | 3-D Wilson action density | `bcc_action.py:L250-252 wilson_action_density()` | unknown (inferred: machine) |
| 5 | $\Phi^a_p=\operatorname{Im}\operatorname{tr}(T^aP)/(g\,c)$, $c=\operatorname{tr}(T^0T^0)$ measured | loop phase per orientation | `bcc_action.py:L275-276 plaquette_phases()` | unknown (inferred: machine) |
| 6 | $f^a=\tfrac18\sum_p m_p\Phi^a_p$, $f^a=(F^a_{23},-F^a_{13},F^a_{12})$ (uses $\sum_p m_pm_p^{\mathsf T}=4I$) | closed-form 6→3 field-strength projection | `bcc_action.py:L299-300 cartesian_field_strength()` | exact (projection); inventory #231 |
| 7 | $\lVert 2Mf-\Phi\rVert_\infty/\lVert\Phi\rVert_\infty$ | overdetermined-fit (Bianchi-type) residual, $O(\Phi^2)$ | `bcc_action.py:L321-328 cartesian_reconstruction_residual()` | unknown (inferred: quantitative) |
| 8 | 10 loops/site: 6 rhombi + 4 mixed rectangles $(a,\hat t,-a,-\hat t)$, rectangle area $\lvert d\rvert a_t=\sqrt3\,a_t$ | $\mathrm{BCC}_3\times\mathbb Z$ loop table | `bcc_action.py:L486-501 _build_loops()`; `L508 BCC4_MIXED_AREA` | unknown (inferred: exact) |
| 9 | $S=\beta_s\sum_\text{rhombi}(1-\operatorname{Re}\operatorname{tr}P/N)+\beta_t\sum_\text{rect}(1-\operatorname{Re}\operatorname{tr}P/N)$ over BCC sites | anisotropic 3+1-D Wilson action | `bcc_action.py:L677-682 wilson_action_4d()` | unknown (inferred: exact (definition)) |
| 10 | $A_\ell=\sum_{\text{loops}\ni\ell}\beta\,(\text{3-leg staple})$; $\sum_\ell\operatorname{Re}\operatorname{tr}(U_\ell A_\ell)=4\sum_\text{loops}\beta\operatorname{Re}\operatorname{tr}P$ | staple = $dS/dU$ identity | `bcc_action.py:L695-707 staple_sum()`, `L723-742 staple_identity_residual()` | machine (inventory #235: $2.3\times10^{-16}$) |
| 11 | $U\to W(x)UW(x+d)^\dagger$ | random SU(N) gauge transform | `bcc_action.py:L613-615 gauge_transform_4d()` | unknown (inferred: exact (holonomy invariance, machine residual)) |
| 12 | $a_0\sim\sqrt{1-a_0^2}\,e^{\xi a_0}$, $\xi=2k/N$ (β folded into staple) | Creutz SU(2)-subgroup heat bath | `bcc_action.py:L795, L812 _creutz_a0()/_sample_su2_heatbath()` | unknown (inferred: quantitative (stochastic)) |
| 13 | $R_2=(V_2^\dagger)^2$ | microcanonical over-relaxation (action-preserving) | `bcc_action.py:L826 _su2_overrelax()` | exact (inventory #236: literal 0.0) |
| 14 | 4-colouring = (spatial parity) × (time parity) | checkerboard legality from BCC bipartiteness | `bcc_action.py:L866-870 _update_field()` | unknown (inferred: exact) |
| 15 | $\chi(R,T)=-\ln\dfrac{W(R,T)W(R{-}1,T{-}1)}{W(R{-}1,T)W(R,T{-}1)}$ | Creutz ratio (string-tension estimator) | `bcc_action.py:L988 creutz_ratios()` | unknown (inferred: quantitative) |
| 16 | $P=\langle\operatorname{tr}\prod_tU_t/N\rangle$ | Polyakov loop | `bcc_action.py:L996-999 polyakov_loop_4d()` | unknown (inferred: quantitative) |
| 17 | $a_t=c_\text{lat}\lambda\sqrt3,\ \ \beta_t/\beta_s=4\lambda^2/a_t^2=\dfrac{4}{3c_\text{lat}^2},\ \ \xi^2=1/c_\text{lat}^2$; at $c_\text{lat}^2=\tfrac13$: $\beta_t/\beta_s=4,\ \xi=\sqrt3,\ (\beta_t/\beta_s)/\xi^2=\tfrac43$ | derived anisotropy (tree-level isotropy matching) | `bcc_action.py:L1413-1415 anisotropy_from_c_lat()` | exact (inventory #233) |
| 18 | $\theta(X,H)=\tfrac g2X^\mu F_{\mu\nu}H^\nu$, $U=\exp(i\theta T_3)$ | constant-$F$ abelian test configuration | `bcc_action.py:L1479, L1486 constant_field_links_4d()` | unknown (inferred: exact (construction)) |
| 19 | $\beta_t/\beta_s\big\lvert_\text{meas}=S_B/S_E$, Richardson $(4r(g/2)-r(g))/3$ | measured isotropy ratio → 4 | `bcc_action.py:L1541 weak_field_isotropy()`; `L1252 check_bcc_gauge_mc()` | unknown (inferred: quantitative (gate $<10^{-8}$)) |
| 20 | $\sum_pm_pm_p^{\mathsf T}=4I$ (6 ⟨110⟩), $\sum_a aa^{\mathsf T}=4I$ (4 ⟨111⟩) | two closure identities, integer arithmetic | `bcc_action.py:L1566-1575 bcc_closure_identities()` | exact (inventory #231–232) |
| 21 | $\chi_3=t_1,\ \chi_6=\tfrac12(t_1^2+t_2),\ \chi_8=t_1\bar t_1-1,\ \chi_{10}=\tfrac16(t_1^3+3t_1t_2+2t_3)$, $t_n=\operatorname{tr}W^n$ | SU(3) characters from loop-matrix traces | `bcc_action.py:L1658-1665 rep_character_from_traces()` | exact (inventory #238, vs explicit reps $\le4.6\times10^{-16}$) |
| 22 | $d_{(p,q)}=\tfrac12(p{+}1)(q{+}1)(p{+}q{+}2)$; $C_2(p,q)=\tfrac13(p^2{+}q^2{+}pq{+}3p{+}3q)$, $C_F=\tfrac43$; ratios $1,\tfrac52,\tfrac94,\tfrac92$ | rep dimension, Casimir ratio | `bcc_action.py:L1672 rep_dimension()`, `L1683-1685 casimir_ratio_exact()` | exact (inventory #234) |
| 23 | $\mathrm{Sym}^k(U)=S^\dagger U^{\otimes k}S$; $\mathrm{Ad}(U)_{ab}=2\operatorname{tr}(T_aUT_bU^\dagger)$ | explicit reps for the cross-check | `bcc_action.py:L1717 sym_power_rep()`, `L1741 adjoint_rep()` | unknown (inferred: machine) |
| 24 | $\sigma_R/\sigma_3$ from per-rep Creutz ratios vs $C_2(R)/C_F$ | $d=4$ Casimir-scaling readout | `bcc_action.py:L1815-1878 casimir_scaling_from_loops()` | quantitative (inventory "PRELIMINARY d=4", 3 configs) |

**Inputs → outputs:** SU(N) link fields (8-direction legacy layout, or `{'s':[4], 't':…}` for 3+1-D), $\beta_s,\beta_t$ → plaquettes, $F^a_{\mu\nu}$, action, thermalised configurations, loop tables, Creutz ratios and the gate dict (`check_bcc_gauge_mc`, 25+ legs with 5 declared controls). **Depends on:** `lattice/geometry` BCC constants (`BCC_HOP_DIRS`, `BCC_LINK_AXES`, `BCC_PLAQUETTES`, `BCC_PLAQ_NORMALS`, `bcc_site_mask`; see 03-lattice.md); `numerics.rng.for_channel` (02-numerics.md). **Flags:** (a) the registry records no findings and no exactness for a 29-channel driven module, although the inventory rows #231–238 cite it by name. (b) The anisotropy derivation hard-codes $c_\text{lat}^2=$ `Fraction(1, 3)` (L1410) instead of importing `c_lat` from `casim.constants`. (c) `import numpy` is direct (D8). (d) The module docstring still calls it `ca_bcc_gauge.py` and says constants "live in `ca_lattice`"; that is stale naming. (e) The comment block L377-384 says "$\beta_t=\beta_s$ is a convention, flagged, not a result", but the later section (L1347-1398) derives $\beta_t/\beta_s=4$. The earlier note is superseded within the same file.

---

### `engine/gauge/bgfield_loop.py` — background-field one-loop gluon self-energy and the b₀ = 11 gate
**Status:** live · test-only · **Findings:** registry none; docstring and inventory: F162 (with F151, F155, F272) · **Lattice:** continuum 4-D (symbolic); the numerical leg uses a 4-D cubic midpoint grid with the Wilson or "rule" kernel · **Law:** the rule kernel is $K=$ `gluon_self_energy.K_true_4d` (even-law based; see 05b) · **Units:** continuum / lattice momentum

**Does:** assembles the Abbott Feynman-background-gauge gluon + ghost self-energy. It extracts the UV log coefficient symbolically, confirming transversality and $b_0=\tfrac{11}{3}C_A=11$. It then checks numerically that swapping the continuum propagator for a lattice one shifts the transverse coefficient only by a $q$-independent constant.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Gamma^F_{a\mu\lambda}(k,q)=-2q_\lambda\delta_{a\mu}+2q_a\delta_{\mu\lambda}-(2k+q)_\mu\delta_{\lambda a}$ | BQQ vertex (Abbott Eq. 18) | `bgfield_loop.py:L74-76 gammaF_tensor_continuum()`; symbolic `L100` | unknown (inferred: exact) |
| 2 | $M_{\mu\nu}=\Gamma^F_{a\mu\lambda}(k,q)\Gamma^F_{\lambda\nu a}(k{+}q,-q)-2(2k{+}q)_\mu(2k{+}q)_\nu$ | gluon loop + ghost loop numerator | `bgfield_loop.py:L108-112` (inside `b0_gate_symbolic()`) | unknown (inferred: exact) |
| 3 | $\dfrac1{(k+q)^2}\approx\dfrac1K-\dfrac{2k\cdot q+q^2}{K^2}+\dfrac{(2k\cdot q)^2}{K^3}$; $\langle k_ak_b\rangle=\tfrac K4\delta$, $\langle k^4\rangle=\tfrac{K^2}{24}(\delta\delta+\delta\delta+\delta\delta)$ | large-$k$ expansion and 4-D angular average | `bgfield_loop.py:L116, L125-130` | unknown (inferred: exact) |
| 4 | $g_{\mu\nu}=\tfrac{22}{3}(q^2\delta_{\mu\nu}-q_\mu q_\nu)$, $b_0=\tfrac N2\cdot\tfrac{22}3=11$; scalar-bubble calibration $g=1$ | the b₀ gate (transverse, with gluon/ghost split) | `bgfield_loop.py:L166-185 b0_gate_symbolic()` | unknown (inferred: exact (sympy)) |
| 5 | $B=(\Pi_{00}-\Pi_{11})/Q^2$, $\Pi=\tfrac{C_A}{2}\langle M/(K(k)K(k{+}q))\rangle_\text{grid}$ with $K\in\{k^2,\ 4\sum\sin^2(k_\mu/2),\ K_\text{rule}\}$; **no** mod-2π refold (F272) | transverse coefficient per kernel | `bgfield_loop.py:L243-262 _Bcoeff_numeric()` | unknown (inferred: quantitative) |
| 6 | $\Delta=B_\text{lat}-B_\text{cont}$ flat in $Q$ (spread $<10^{-3}$ Wilson) ⇒ lattice $b_0=11$ | propagator-independence of b₀ | `bgfield_loop.py:L270-285 lattice_b0_consistency()` | unknown (inferred: quantitative) |

**Inputs → outputs:** none (symbolic) / $(Q, n)$ → rationals, shift tables and status dicts. **Depends on:** `constants`: `q_star_a_band_lo` $=1/\sqrt3$ (exact, F151/F155) and `q_star_a_implied` $=0.7327$ (quantitative, F151/F155), see 01-constants.md; `gauge.gluon_self_energy.K_true_4d` (05b). **Flags:** (a) `status()`/`d1_qstar_status()` hard-code the literals 0.733, 0.97, 28.81 and 1.78 (L304-306, L322) beside the registered `q_star_a_implied`. These are unregistered literals, and 0.733 duplicates a registered constant. (b) `C_A=3.0` and `B0_PURE_GAUGE=11.0/3.0*C_A` are float literals (L55-57). (c) The finite constant $d_1$ (and so the $q^*$ digit) is declared OPEN. The module asserts only the bracket $q^*a\in[1/\sqrt3,\sim0.97]$.

---

### `engine/gauge/bilinear.py` — σ-bilinear "composite photon" (RETIRED AS THE PHOTON)
**Status:** partial · package-only · **Findings:** registry none; code: F20–F26, F26b, F29, F30, F37, F306 · **Lattice:** BCC (momentum-space walk) · **Law:** **single-branch chiral**, $\Omega^+(k)=2\omega^+(k/2)$ (default `sign='+'`) · **Units:** lattice

**SUPERSEDED as the photon by F67/F68/F69** (banner L5-22). The paired-spinor photon (`gauge/photon.py`, even law) is the photon. This module is retained for the W/Z/gluon σ-bilinear construction and for the historical F20–F26/F306 tests. **Audit:** no live photon channel imports it (see the header). Its only engine consumers are `derive_bilinear_so3.py` and two fork harnesses.

**Does:** builds $E_G,B_G$ from the transpose bilinear $G^i=\phi^{\mathsf T}\sigma^i\psi$ of BCC Weyl eigenmodes at $k/2$. It provides the single-branch spectral rotation propagator, Mohr-style photon wavefunction checks (polarisation, boosts, VSH, Green function), and the F306 and F26b closed-form gates.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $U(k)=\begin{pmatrix}u-in_z&-i(n_x-in_y)\\-i(n_x+in_y)&u+in_z\end{pmatrix}$; eigenphases by `np.linalg.eig`, $\psi_\pm$ with $U\psi_\pm=e^{\mp i\omega}\psi_\pm$ | BCC Weyl eigenmodes at one $k$ | `bilinear.py:L149-153 _hamiltonian_matrix()`, `L164-172 weyl_eigenmodes_3d_bcc()` | unknown (inferred: machine (eig)) |
| 2 | $G^i=\phi^{\mathsf T}\sigma^i\psi$ (transpose, not dagger) | σ-bilinear | `bilinear.py:L194 bilinear_G()` | unknown (inferred: exact) |
| 3 | $E_G=\lvert n\rvert(G_T+G_T^*)$, $B_G=i\lvert n\rvert(G_T^*-G_T)$, $G_T=G-(G\cdot\hat n)\hat n$, $n=n(k/2)$ | Paper-1 Eq. 35 fields (transverse **by construction**) | `bilinear.py:L252-256 EM_bilinears()` | unknown (inferred: exact) |
| 4 | same-helicity identity $\lVert G_T\rVert=\sqrt2\,\lvert\hat n_y\rvert$ (so $E_G=B_G=0$ on $\hat n_y=0$) | degeneracy of the transpose bilinear | docstring `bilinear.py:L227-243` (not computed by a function here) | unknown |
| 5 | $G_H^i=\sum_\alpha\phi^{\alpha\dagger}\sigma^i\psi^\alpha$; $W_H^{a,i}=\sum_{\alpha\beta}\tau^a_{\alpha\beta}\phi^{\alpha\dagger}\sigma^i\psi^\beta$ | Hermitian singlet / SU(2) triplet bilinears (W sector) | `bilinear.py:L376-382`, `L387-398` | unknown (inferred: exact) |
| 6 | $(E,B)=\alpha_+(E_+,B_+)+\alpha_-(E_-,B_-)$ from both branches | two-helicity assembly | `bilinear.py:L338-341 EM_bilinears_two_helicity()`; triplet `L464-469` | unknown (inferred: exact) |
| 7 | $F^\pm=E\pm iB$ | Riemann–Silberstein split | `bilinear.py:L361-363 riemann_silberstein_decomp()` | unknown (inferred: exact) |
| 8 | $\Omega(k)=2\,\omega_\text{BCC}^\pm(k/2)$, $\omega^\pm=\arccos u^\pm$ | rotation angle per tick (**single branch**) | `bilinear.py:L1904 rotation_omega_bcc()` | unknown (inferred: exact (closed form)) |
| 9 | $\hat E'=\cos\Omega\,\hat E+\sin\Omega\,\hat B,\ \ \hat B'=-\sin\Omega\,\hat E+\cos\Omega\,\hat B$ (all three Cartesian components together) | spectral rotation step, `sign='+'` default | `bilinear.py:L1973-1974 rotation_step_em_spectral()` | machine (inventory #51: an identity, "not a prediction") |
| 10 | $c=\Omega(\epsilon\hat k)/\epsilon$, $\epsilon=10^{-5}$ | $c_\text{lat}=d\Omega/d\lvert k\rvert$ | `bilinear.py:L2021-2023 c_from_rotation_rate()` | unknown (inferred: quantitative (spot-check: $0.5773529$ vs $1/\sqrt3$)) |
| 11 | $\delta v_\varphi/c=\Omega/(c_\text{lat}k)-1$ along (1,1,1); theory line $-k/18$ | dispersion nonlinearity / "Planck correction" | `bilinear.py:L2089-2091 dispersion_nonlinearity()`, `L2151-2153 planck_correction_prediction()` | unknown (inferred: quantitative) |
| 12 | $\Omega^+-\Omega^-\approx-\tfrac{\sqrt3}{27}k^2$ on (1,1,1) | single-branch birefringence (why it is retired) | quoted at `bilinear.py:L268, L286-288`; spot-checked (matches to $10^{-6}$ rel.) | unknown (inferred: quantitative) |
| 13 | $E(t{+}1)=\cos\Omega\,E+\sin\Omega\,B$ vs curl $E+i(2n)\times B$ | rotation vs curl residuals | `bilinear.py:L1615-1622 real_rotation_vs_maxwell_curl()`; `L2218-2222 rotation_law_consistency()` | unknown (inferred: machine (rotation) / quantitative (curl)) |
| 14 | analytic amplitudes $\hat E=\lvert n\rvert G_T$, $\hat B=\hat n\times\hat E$; $R=\lvert\Omega-2\lvert n\rvert\rvert$-type residual $\to c_\text{lat}^3k^2/48=k^2/(144\sqrt3)$ | F306: curl closes at $O(k^3)$ | `bilinear.py:L2586-2593 maxwell_curl_residual_analytic()`; `L2631 check_curl_closes_at_k3()` | unknown (inferred: quantitative (closed form matched to <5% at k ≥ 1e-2)) |
| 15 | $\psi^{\mathsf T}\psi=\cos^2\tfrac\Theta2+\sin^2\tfrac\Theta2e^{2i\Phi}$; $\lvert\psi^{\mathsf T}\psi\rvert^2=1-\hat n_y^2$ | F26b scalar contamination of the (1,0) bilinear | `bilinear.py:L1730-1732 psi_scalar_bilinear_analytic()`; gate `L2792-2802 check_spin_axis_scalar_contamination()` | unknown (inferred: exact (algebraic track <1e-13)) |
| 16 | $\hat n\to(k_x,-k_y,k_z)/\lvert k\rvert$ as $k\to0$ | BCC chirality sign flip on $y$ | `bilinear.py:L2767-2769` | unknown (inferred: machine) |
| 17 | $A=\cosh\tfrac\zeta2 I-\sinh\tfrac\zeta2\,\sigma\cdot\hat v$; $R=\cos\tfrac\theta2I-i\sin\tfrac\theta2\,\sigma\cdot\hat n$; $j^\mu=(\psi^\dagger\psi,\psi^\dagger\sigma\psi)$, $j'=\Lambda j$ | SL(2,ℂ)→SO(1,3) covariance of the Weyl current | `bilinear.py:L1027, L2395-2396`; gate `L2496-2505 sl2c_covariance_full()` | unknown (inferred: machine (conditioning-limited, $\le10^{-10}$ boost)) |
| 18 | $H(k)=c\lvert k\rvert\begin{pmatrix}0&\tau\cdot\hat k\\\tau\cdot\hat k&0\end{pmatrix}$, $G=(H-\omega-i\epsilon)^{-1}$, $\Xi=(-\mu_0cJ_s,0)$ with $\mu_0c:=1$ | Mohr 6-spinor Hamiltonian, Green function, source | `bilinear.py:L1391-1394`, `L1404-1405`, `L1414-1417` | unknown (inferred: machine) |
| 19 | Mohr polarisation basis, 6×6 boost $V=\begin{pmatrix}I+(\tau\cdot\hat v)^2(\cosh\zeta-1)&\tau\cdot\hat v\sinh\zeta\\\cdots\end{pmatrix}$, VSH $Y^m_{jl}$ via CG | continuum photon-wavefunction algebra (not lattice physics) | `bilinear.py:L600-639, L737-749, L1194-1241` | unknown (inferred: machine) |

**Inputs → outputs:** $k$ and Weyl spinors, or full $(E,B)$ arrays of shape $(L,L,L,3)$ → fields, residual dicts and gate dicts. **Depends on:** `lattice.bcc._bcc_uvec`, `bcc_dispersion`, `bcc_spin_axis` (03-lattice.md); `constants.c_lat` $=1/\sqrt3$ (F26); `numerics.fft`. **Flags:** see the flags file. The main items: (a) the module docstring still lists `rotation_step_em_spectral` as the "EXACT EM propagator … primary" (L72), and it is single-branch chiral. SUPERSEDED as the photon by F67–F69; F306 withdrew the curl coefficient (inventory #49). (b) With the default real input, `rotation_step_em_spectral` returns complex fields, because the one-branch law breaks Hermitian symmetry (acknowledged at L1980-1984; chiral-transform hazard). (c) `planck_correction_prediction` docstring says $\delta v/c\approx-c_\text{lat}^2k^2/6=-k^2/18$ (L2109), but the code uses $-k/18$ (L2153). The spot-check confirms $-k/18$ (linear) is right for branch +, so the docstring is wrong. (d) The C8 header (L1535) writes the rotation with $\hat k\times B$, but the code (L1615) has no cross product. (e) The `maxwell_curl_residual` docstring step 4 says $\phi\to e^{+i\omega}\phi$, but the code evolves both by $e^{-i\omega}$ (L528-530, acknowledged by an inline comment). (f) The file has two `__main__` blocks; the second writes an artifact only when `CASIM_F24=1`.

---

### `engine/gauge/bilinear_2d.py` — σ-bilinear on the 2-D square QCA (reference lattice)
**Status:** live · driven (15 ch) · **Findings:** registry none; code: F7, F26 · **Lattice:** 2-D square (reference, **not canonical**, D1) · **Law:** single-branch rotation $\Omega(k)=2\omega_\text{2D}(k/2)$ (the 2-D walk has no ± branch pair here) · **Units:** lattice ($c_\text{lat}^{2D}=1/\sqrt2$)

**Does:** a 2-D port of `bilinear.py` (eigenmodes, bilinear, curl/transversality/dispersion tests). Its one live export is `rotation_omega_2d`, which `gluon.py` and `colour_dielectric.py` use as the 2-D gluon rotation rate. That use is why the registry marks it "driven (15 ch)".

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u=c_xc_y,\ n=(s_xc_y,\ c_xs_y,\ s_xs_y)$, $c_i=\cos(k_i/\sqrt2)$; $U$ as in `bilinear` #1 | 2-D square walk (via `core_exact._arccos_2d_uvec`) | `bilinear_2d.py:L50-55 _hamiltonian_matrix_2d()` | unknown (inferred: exact) |
| 2 | $G^i=\phi^{\mathsf T}\sigma^i\psi$; $E,B$ as `bilinear` #3 | bilinear, transverse by construction | `bilinear_2d.py:L83, L94-103` | unknown (inferred: exact) |
| 3 | $\Omega_\text{2D}(k)=2\arccos\!\big(\cos\tfrac{k_x}{2\sqrt2}\cos\tfrac{k_y}{2\sqrt2}\big)$ | 2-D rotation rate (**used by the gluon code**) | `bilinear_2d.py:L218 rotation_omega_2d()` | unknown (inferred: exact (closed form)) |
| 4 | $\hat E'=\cos\Omega\hat E+\sin\Omega\hat B,\ \hat B'=-\sin\Omega\hat E+\cos\Omega\hat B$; `.real` taken if the input was real | 2-D spectral rotation step | `bilinear_2d.py:L250-259 rotation_step_em_spectral_2d()` | unknown (inferred: machine) |
| 5 | $c=\Omega(\epsilon\hat k)/\epsilon\to1/\sqrt2$ | 2-D light speed | `bilinear_2d.py:L284-288 c_from_rotation_rate_2d()` | unknown (inferred: quantitative) |
| 6 | curl residual $\lVert\dot E-i(2n)\times B\rVert$, same construction as 3-D | the F7 "1/√6 vs 1/2" discriminator | `bilinear_2d.py:L150-159 maxwell_curl_residual_2d()` | quantitative (the coefficient was WITHDRAWN by F306, inventory #7) |

**Inputs → outputs:** $(k_x,k_y)$ or $(L,L,3)$ fields → Ω, stepped fields, residuals. **Depends on:** `lattice.core_exact._arccos_2d_uvec` and `exact2d_dispersion` (03-lattice.md, reference implementation). **Flags:** (a) `rotation_step_em_spectral_2d` takes `.real` of the IFFT for real inputs (L256-259). It is safe here because the single 2-D rate is even in $k$, but it is exactly the pattern CLAUDE.md warns about for chiral laws. (b) The `maxwell_dispersion_residual_2d` docstring calls the deviation "the BCC lattice's nonlinear dispersion" (L184), but this is the 2-D square lattice. (c) `c_analytic = 1/√2` is a literal (L288); a `MeasuredConstant` $1/\sqrt2$ (F26) exists in `constants/measured.py`. (d) The curl-residual constant this module was built to discriminate was withdrawn by F306.

---

### `engine/gauge/casimir_ladder.py` — SU(N) k-string Casimir ladder vs the F110 C7 rotor matching
**Status:** live · standalone · **Findings:** F298 F294 F293 F110 F144 F86 F97 · **Lattice:** n/a (group theory over ℚ) · **Law:** n/a · **Units:** n/a (the empirical leg uses GeV via `derive_ncolour`)

**Does:** computes exact SU(N) quadratic Casimirs. It re-runs the C7 matching $\chi_k=s(k)^2/(4g^2C_2(R_k))$ on the antisymmetric (k-string) tower and shows the identity is level-independent only for $N\le3$, where it gives $\chi=1/(4g^2C_F)$. The operator-consistent control ($C_2$ on both sides) gives $\chi=1/(4g^2)$ at every $N$. It also shows that the k-string tension laws are degenerate at $N=3$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $C_2(\lambda)=\tfrac12\Big[\sum_i\lambda_i(\lambda_i+N+1-2i)-\tfrac{(\sum\lambda)^2}{N}\Big]$ | SU(N) Casimir from Young rows | `casimir_ladder.py:L97-100 su_n_casimir()` | exact (reg) |
| 2 | $C_F=(N^2-1)/(2N)$ | fundamental Casimir | `casimir_ladder.py:L105 casimir_fundamental()` | exact (reg) |
| 3 | $s(k)=((k+\lfloor N/2\rfloor)\bmod N)-\lfloor N/2\rfloor$, level $s(k)^2$ | $\mathbb Z_N$ rotor level (symmetric residue) | `casimir_ladder.py:L111-112 zn_symmetric_residue_sq()` | exact (reg) |
| 4 | $\chi_k=\dfrac{\text{num}_k}{4g^2C_2(1^k)}$, num $=s(k)^2$ ("zn", mixed) or $C_2$ ("casimir"); identity iff $\chi_k$ is $k$-independent | C7 re-run | `casimir_ladder.py:L168-172 c7_against_casimir_ladder()` | exact (reg) |
| 5 | three matchings (abelian/abelian, mixed, SU(N)/SU(N)), including off-tower SU(3) irreps via triality $(p-q)\bmod3$ | operator-consistency audit | `casimir_ladder.py:L244-248, L285-291 operator_consistency()` | exact (reg) |
| 6 | $\sigma_k/\sigma_1$: Casimir $C_2(1^k)/C_2(1)$; sine $\sin(\pi k/N)/\sin(\pi/N)$; centre 1 for $\lvert N\text{-ality}\rvert=1$; BPS $k$ | k-string law table | `casimir_ladder.py:L341-348 kstring_tension_laws()` | exact (reg) |
| 7 | $b_0=(33-2N_f)/(12\pi)$, $\alpha_0^\text{req}=\big[\alpha_s(M_Z)^{-1}+b_0\cdot2\ln(\mu_0/M_Z)\big]^{-1}$; H1 $=1/(16\pi)$, H2 $=H1/C_F$ | empirical H1 vs H2 | `casimir_ladder.py:L379-383 h1_vs_h2_empirical()` | quantitative (PDG inputs) (reg: exact; row is weaker — see flags) |

**Inputs → outputs:** N list, $g^2$ (default $\tfrac14$), matching mode → Fraction tables and the F298 gate (`check_casimir_ladder`, L1–L6, three declared controls). **Depends on:** `gauge.derive_ncolour` (`MU0_GEV`, `MZ_GEV`, `ALPHA_S_MZ_PDG`, `N_F`; see 05b). **Flags:** (a) The module docstring (L20-49) presents "(1) the C7 identity carries $1/C_F$" and "(2) exists only for $N\le3$" as results. The later `operator_consistency` and the L6 leg (added 2026-08-18) show both come only from the *mixed* matching; with the same operator on both sides, $\chi=1/(4g^2)$ at every $N$. The header was not revised. (b) Registry exactness `exact` is correct for L1–L4 and L6, but the L5 empirical leg is quantitative.

---

### `engine/gauge/casimir_scaling.py` — F299: higher-rep string tensions on the exactly solvable 2-D SU(3) engine
**Status:** live · standalone (2 reachable) · **Findings:** F299 F298 F294 F293 F144 F110 F94 F86 · **Lattice:** 2-D single-plaquette Wilson measure (axial gauge, plaquettes independent); Weyl-torus quadrature · **Law:** n/a · **Units:** lattice ($\beta=2N/g_s^2$); the $\mu_0$ leg uses GeV

**Does:** generalises `confinement.py`'s exact 2-D SU(3) engine from the fundamental to arbitrary irreps (division-free Jacobi–Trudi characters). It measures $\sigma_R/\sigma_3$ at the model's $\beta$ and compares with the Casimir and centre laws. It also checks the F94 higher-rep polynomial identities and the $\mu_0$ that H2 would require.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\beta=2N/g_s^2$, $g_s$ from `derive_ncolour.alpha_s_at_lattice_scale` ($g_s=\tfrac12\Rightarrow\beta=24$, F144) | model Wilson coupling | `casimir_scaling.py:L160-161 model_wilson_beta()` | quantitative (reg) (row read: exact (given $g_s$)) |
| 2 | $\sigma_R/\sigma_F=C_2(R)/C_F$; centre: $0$ if triality 0, else $1$ | the two laws over ℚ | `casimir_scaling.py:L170-171 casimir_law()`, `L181-182 centre_law()` | quantitative (reg) (row read: exact) |
| 3 | $d\mu\propto\prod_{i<j}2(1-\cos(\phi_i-\phi_j))$, $\phi_3=-\phi_1-\phi_2$, midpoint grid | SU(3) Weyl-torus class measure | `casimir_scaling.py:L235-242 _torus()` | quantitative (reg) (row read: machine) |
| 4 | $h_k=\sum_{a+b+c=k}z_1^bz_2^cz_3^a$; $\chi_{(p,q)}=\det[h_{\lambda_i-i+j}]$, $\lambda=(p{+}q,q,0)$ | division-free Jacobi–Trudi characters | `casimir_scaling.py:L252-262 _h_basis()`, `L272-275 rep_character()` | quantitative (reg) (row read: exact (polynomial)) |
| 5 | $w_R(\beta)=\langle\chi_R/d_R\rangle$ under $e^{(\beta/3)\operatorname{Re}\chi_F}d\mu$ (max-shifted) | single-plaquette rep mean | `casimir_scaling.py:L288-293 plaquette_rep_means()` | quantitative (reg) (row read: machine (spectral quadrature; S6 grid agreement $<10^{-10}$)) |
| 6 | $\sigma_R=-\ln\lvert w_R\rvert$, ratio $\sigma_R/\sigma_3$ | exact-in-2D string tension | `casimir_scaling.py:L301-304 sigma_ratios()` | quantitative (reg) (row read: machine (2-D exact)) |
| 7 | continuum limit $\sigma_R\to(g_0^2/2)C_2(R)$, $g_0^2=2N/\beta$ | residual trend $\beta=24\to192$ | `casimir_scaling.py:L381-389 weak_coupling_trend()` | quantitative (reg) |
| 8 | $\chi_6=\tfrac12(t_1^2+t_2),\ \chi_8=\lvert t_1\rvert^2-1,\ \chi_{10}=\tfrac16(t_1^3+3t_1t_2+2t_3)$ vs Jacobi–Trudi on the torus | F94 reach identities | `casimir_scaling.py:L414-420 mc_reach()` | quantitative (reg) (row read: machine (<1e-9)) |
| 9 | $\ln(\mu_0/M_Z)=\big(\alpha_0^{-1}-\alpha_s(M_Z)^{-1}\big)/(2b_0)$, $\alpha_0^{-1}\in\{16\pi,\ 16\pi C_F\}$ | $\mu_0$ each hypothesis needs | `casimir_scaling.py:L457-458 mu0_required_for_H2()` | quantitative (reg) |

**Inputs → outputs:** $\beta$ and a rep list → $w_R$, $\sigma_R$ ratios, verdicts and the F299 gate (S1–S8, controls `tower=kstring` and `beta=2.0`). **Depends on:** `gauge.su3_ladder` (`casimir2`, `dim_irrep`, `triality`), `gauge.derive_ncolour`, `gauge.confinement.string_tension` (05b); `numerics.xp`. **Flags:** (a) The docstring was **re-characterised by F325** (L73-91, in-file). "The model's own confinement sector says H2" is to be read as "the links carry SU(3) irreps", because the same ratios come out at $\beta=32$. The `engine_verdict` verdict string (L361-366) and the S4 labels still use the pre-F325 wording. (b) Literal $m_\text{Planck}=1.220890\times10^{19}$ GeV (L453), plus the literals $16\pi$ and $11\cdot3$ (L452, L455). These are unregistered. (c) Registry exactness `quantitative` is right for the module; S1 and S2 are exact.

---

### `engine/gauge/charge_coupling.py` — U(1) charge coupling: Aharonov–Bohm holonomy + sourced curl step
**Status:** live · driven (13 ch) · **Findings:** registry none; code/inventory: F68, F384, F385, F386, F390, F393; inventory rows #179, #180 · **Lattice:** Part 1 is a 2-D square finite-difference grid (reference); Parts 2–3 use the BCC spectral curl symbol · **Law:** **curl-symbol rotation, $\theta=dt\,\lvert C_\text{odd}(k)\rvert$** (see flag (a)); not the even $\Omega_\text{even}$ and not the single-branch $\Omega^+$ · **Units:** lattice

**Does:** Part 1 is the exact discrete Stokes / Aharonov–Bohm check (the Peierls loop phase equals the enclosed plaquette flux). Part 2 defines the odd BCC curl symbol $C(k)$, the unitary sourced curl step used by the `charge_photon`/`photon_sourced` channels, the Coulomb-gauge $A$, Gauss and continuity residuals, and magnetostatics. Part 3 is the charge → field → holonomy loop, plus the $\operatorname{curl}\operatorname{grad}\neq0$ defect diagnostic.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $B_z=(A_y[x{+}1]-A_y)-(A_x[y{+}1]-A_x)$ | plaquette curl (forward difference) | `charge_coupling.py:L84-86 discrete_curl_z()` | unknown (inferred: exact) |
| 2 | $\operatorname{div}A=(A_x-A_x[x{-}1])+(A_y-A_y[y{-}1])$ | backward divergence (adjoint, div∘curl ≡ 0) | `charge_coupling.py:L95-97 discrete_div()` | unknown (inferred: exact) |
| 3 | $a_j=e^{ik_j}-1,\ b_j=1-e^{-ik_j}$, $\hat k^2=\lvert a_x\rvert^2+\lvert a_y\rvert^2$; $\hat A_x=b_y\hat B_z/\hat k^2,\ \hat A_y=-b_x\hat B_z/\hat k^2$ | 2-D Coulomb-gauge solve | `charge_coupling.py:L114-126 solve_A_coulomb_2d()` | unknown (inferred: machine) |
| 4 | $q\oint A\cdot dl=q\sum_{\text{plaq}}B_z$ | discrete Stokes / AB holonomy | `charge_coupling.py:L153-166 peierls_loop_phase()`, `L172-173 enclosed_flux()` | unknown (inferred: exact (telescoping; machine residual)) |
| 5 | $C_\text{odd}(k)=\tfrac12\big[C(k)-C(k^*)\big]$ with $C(k)=n^+(k/2)-n^+(-k/2)$ and $k^*$ the FFT index negation | odd, grid-Hermitian BCC curl symbol | `charge_coupling.py:L214-225 bcc_curl_symbol()` | exact (inventory #180) |
| 6 | $\exp(dt\,G)=1+(\cos\theta-1)P_T+\sin\theta\,\hat G$, $G=\begin{pmatrix}0&iC\times\\-iC\times&0\end{pmatrix}$, $\theta=dt\lvert C\rvert$; then $E\leftarrow E-dt\,J$ | **sourced curl step** (unitary per mode; longitudinal part invariant) | `charge_coupling.py:L267-288 maxwell_curl_step()` | exact (inventory #179); FFT round-trip machine |
| 7 | $E\leftarrow E+dt(iC\times B-J),\ B\leftarrow B-dt\,iC\times E$ ($\lvert\lambda\rvert^2=1+dt^2\lvert C\rvert^2$) | forward-Euler reference (**unstable**, kept for regression) | `charge_coupling.py:L306-311 maxwell_curl_step_euler()` | unknown (inferred: exact (definition)) |
| 8 | $A=i(C\times B_T)/\lvert C\rvert^2$, $B_T=B-\hat C(\hat C\cdot B)$; $A=0$ on the 7 corner modes where $C\equiv0$ | 3-D Coulomb-gauge $A$ ($C\cdot A\equiv0$) | `charge_coupling.py:L358-369 solve_A_coulomb_3d()` | unknown (inferred: machine) |
| 9 | $iC\cdot\hat E-\hat\rho$; $iC\cdot\hat J$ | Gauss residual; continuity RHS ($\partial_t\rho=-iC\cdot J$) | `charge_coupling.py:L381-383 gauss_residual()`, `L392 div_from_current()` | unknown (inferred: exact (definitions)) |
| 10 | $B=i(C\times J_T)/\lvert C\rvert^2$ | magnetostatic Ampère solve | `charge_coupling.py:L413-419 magnetostatic_B()` | unknown (inferred: machine) |
| 11 | $J_x=B_z-B_z[y{-}1],\ J_y=-(B_z-B_z[x{-}1])$ | 2-D Ampère wall current | `charge_coupling.py:L435-436 ampere_current_2d()` | unknown (inferred: exact) |
| 12 | $\lvert C\times G\rvert/(\lvert C\rvert\lvert G\rvert)$ for $G=k$ or $e^{ik}-1$; measured means 0.741692, 0.707173; $\hat C\cdot\hat k=+1$ on the $x,z$ axes, $-1$ on $y$ | $\operatorname{curl}\operatorname{grad}\neq0$ defect gate (known-failing, monitored) | `charge_coupling.py:L545-564 check_curl_grad_identity_diagnostic()` | unknown (inferred: machine (asserted to 1e-4 as the *defect* value)) |

**Inputs → outputs:** real fields of shape (3,L,L,L) and currents → stepped fields, $A$, residuals. **Depends on:** `lattice.bcc._bcc_uvec` and `bcc_dispersion`; `lattice.geometry.make_kgrid_3d` (03-lattice.md); `numerics.fft`. Consumed by `core/coupled.py` (L194) and `a_field_convention`. **Flags:** (a) **LAW MISMATCH.** `src/casim/README.md` (L110, L113) labels the `charge_photon` and `photon_sourced` channels "even" and routes them to `maxwell_curl_step`. That step rotates each transverse mode by $\lvert C_\text{odd}(k)\rvert$, not by $\Omega_\text{even}=\omega^+(k/2)+\omega^-(k/2)$. The two agree to $O(k^3)$ only. Spot-check on the $x$-axis: $\lvert C_\text{odd}\rvert=2\sin(k/2\sqrt3)$, which is $1.0916$ vs $\Omega_\text{even}=1.1547$ at $k=2$. The module docstring (L27-30) also says "the paired photon propagates by the even-law rotation … carried by $C(k)=2n(k/2)$". (b) $C$ is built from branch '+' only, then odd-projected. It is branch-asymmetric at finite $k$ and fails $\operatorname{curl}\operatorname{grad}=0$ maximally (item 12, gated as a known defect; F393). (c) The docstring's "C(k)=2n(k/2)" and the code's $n(k/2)-n(-k/2)$ are the same thing only after odd projection, which is consistent. (d) `import numpy` is direct (D8).

---

### `engine/gauge/charged_current.py` — SU(2) charged current and the β-decay pipeline (FG-8)
**Status:** live · driven (19 ch) · **Findings:** registry none; code: F29, F34, F35, F36, F48 · **Lattice:** BCC (via `weak_wmu` spectral steps) · **Law:** W propagation in this module is the **even** massive law $\omega_\text{eff}=\sqrt{m_W^2+\Omega_\text{even}^2}$ (`weak_wmu.w_massive_propagation_step_spectral`); see flag (a) · **Units:** lattice

**Does:** defines the raising and lowering isospin generators, the site-local charged currents $J^\pm$, the charged-W components and the tree-level Fermi limit. It also provides exact ℚ charge/B/L bookkeeping, and a driver that sources a W⁻ from a quark doublet and propagates it with the Proca step.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $T^a=\tau^a/2$, $T^\pm=T^1\pm iT^2$; $[T^3,T^\pm]=\pm T^\pm$, $[T^+,T^-]=2T^3$ | SU(2) raising/lowering algebra | `charged_current.py:L93-99`; residuals `L118-121 su2_raising_algebra_residuals()` | unknown (inferred: exact) |
| 2 | $J^+=f_\text{up}^*f_\text{down}$, $J^-=f_\text{down}^*f_\text{up}=(J^+)^*$; $J^\pm=J^1\pm iJ^2$ | site charged currents | `charged_current.py:L152, L162, L175-176` | unknown (inferred: exact) |
| 3 | $P_{L,R}=(1\mp\gamma^5)/2$, $\gamma^5=\operatorname{diag}(-1,-1,1,1)$ | V−A projector check | `charged_current.py:L185-205 va_vertex_kills_right_handed()` | unknown (inferred: exact) |
| 4 | $Q=T_3+Y/2$ (Y: $u,d=\tfrac13$; $\nu,e=-1$); $\Delta Q,\Delta B,\Delta L,\Delta(B{-}L)$ over ℚ | charge registry, conservation | `charged_current.py:L214-258 charge()/conservation_residuals()` | unknown (inferred: exact) |
| 5 | $W^\pm=(W^1\mp iW^2)/\sqrt2$ | charged mass eigenstates | `charged_current.py:L278-279 w_charged_components()` | unknown (inferred: exact) |
| 6 | $E^a\leftarrow R(E^a)+g\,J^a\,dt\ \Rightarrow\ \Delta E(W^-)=(g/\sqrt2)J^+dt$ | W⁻ emission by the quark raising current | `charged_current.py:L305-308 emit_w_minus()` | unknown (inferred: exact (definition)) |
| 7 | $G_F/\sqrt2=g^2/(8m_W^2)$; $A(q^2)=g^2/[8(m_W^2+q^2)]$; deviation $-q^2/(m_W^2+q^2)$ | Fermi limit | `charged_current.py:L318, L331, L336-338` | unknown (inferred: exact) |
| 8 | Gaussian quark doublet at A → emit → $n_\text{prop}$ Proca ticks → $\lvert E(W^-)\rvert$ at B; lepton response $=\lvert E(W^-)\rvert g/\sqrt2$ | end-to-end β-decay driver | `charged_current.py:L357-434 run_beta_decay_pipeline()` | unknown (inferred: quantitative (diagnostic)) |

**Inputs → outputs:** doublet amplitudes, W triplet $(E_W,B_W)$ of shape (3,L,L,L) → currents, updated W, amplitudes and diagnostics. **Depends on:** `gauge.weak_wmu` (`fermion_isospin_current`, `w_sourced_propagation_step`, `w_massive_propagation_step_spectral`; see 05b). **Flags:** (a) **LAW vs F91.** CLAUDE.md decision 5 / F91 classifies W± as *chiral (forced)*. The β-decay pipeline propagates W⁻ with the massive **even** law $\sqrt{m_W^2+\Omega_\text{even}^2}$ (`weak_wmu.py:L1966-1969`), and `w_sourced_propagation_step` uses `w_propagation_step_spectral`, whose law is mapped in 05b. (b) `sys.path.insert(0, dirname(__file__))` (L71) is a pre-C9 import hack. (c) Registry records no findings or exactness for a 19-channel driven module. (d) `run_beta_decay_pipeline` builds right-handed `chi_u, chi_d` (L385-386) that are never used, so "must NOT couple" is asserted in a comment, not tested.

---

### `engine/gauge/chiral_anomaly.py` — ABJ anomaly and Nielsen–Ninomiya consistency (F264 part 2)
**Status:** live · test-only · **Findings:** registry none; code/inventory: F264 (with F250, F68/F87, F27/F46, F75) · **Lattice:** continuum Dirac algebra (sympy); BCC walk in the scaled momentum $q=k/\sqrt3$ for the Weyl-point census · **Law:** both BCC branches $u^\pm$ (census only; no propagator) · **Units:** natural; π⁰ width in MeV/eV

**Does:** derives exactly, over two independent routes, that the vector current is conserved while the axial current carries $\lvert\text{coefficient}\rvert=1/16\pi^2$. It counts the BCC Weyl points in the true FCC Brillouin zone (2 per branch, chirality sum 0), shows the mirror point is gapped at the band top, and compares the π⁰→γγ width with PDG.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\gamma^0=\operatorname{diag}(I,-I)$, $\gamma^i=\begin{pmatrix}0&\sigma^i\\-\sigma^i&0\end{pmatrix}$; $\gamma_5=i\gamma^0\gamma^1\gamma^2\gamma^3$ | Dirac basis, $\gamma_5$ | `chiral_anomaly.py:L157-160 _dirac_gammas()`, `L167 _gamma5()` | unknown (inferred: exact) |
| 2 | $\operatorname{Tr}[\gamma_5\gamma\gamma]=0$; $\operatorname{Tr}[\gamma_5\gamma^\mu\gamma^\nu\gamma^\rho\gamma^\sigma]=-4i\epsilon^{\mu\nu\rho\sigma}$; $\operatorname{Tr}[\gamma_5\sigma^{\mu\nu}\sigma^{\rho\sigma}]=+4i\epsilon$ ($\epsilon^{0123}=+1$) | trace identities over all index combinations | `chiral_anomaly.py:L240-270 gamma5_basis_symbolic()` | unknown (inferred: exact) |
| 3 | $\partial_\mu\bar\psi\gamma^\mu\psi=0$; $\partial_\mu\bar\psi\gamma^\mu\gamma_5\psi=2im\bar\psi\gamma_5\psi$ (from $\{\gamma_5,\not p\}=0$, $[\gamma_5,m]=0$) | classical divergences | `chiral_anomaly.py:L341-357 current_divergences_symbolic()` | unknown (inferred: exact) |
| 4 | $\int\!\frac{d^4k_E}{(2\pi)^4}e^{-k^2/\Lambda^2}=\frac{\Lambda^4}{16\pi^2}$; $\tfrac12(\tfrac e2)^2\Lambda^{-4}(4i)\times\frac{\Lambda^4}{16\pi^2}$; coeff $=-2(\cdot)/i$; gate on $\lvert\text{coeff}/e^2\rvert=1/16\pi^2$ | Fujikawa route | `chiral_anomaly.py:L469-499 fujikawa_anomaly_symbolic()` | unknown (inferred: exact (sympy; magnitude only)) |
| 5 | $\partial_\mu j_5^\mu\big\rvert_\text{anom}=\tfrac{2\alpha}{\pi}E\cdot B$ (using $\epsilon FF=-8E\cdot B$, $e^2=4\pi\alpha$) | equivalent normalisation | `chiral_anomaly.py:L503-511` | unknown (inferred: exact) |
| 6 | $\int\!\frac{d^4k}{(2\pi)^4}[f^\mu(k{+}a)-f^\mu(k)]=\frac{a^\mu}{32\pi^2}$, $f=k/(k^2+D)^2$; radial integral $\tfrac12$, $D$-independent | shift / surface-term route; ratio 2 = two chiralities | `chiral_anomaly.py:L609-633 shift_surface_term_symbolic()` | unknown (inferred: exact) |
| 7 | $\gamma^\mu=\gamma^\mu(P_L+P_R)$, $\gamma^\mu\gamma_5=\gamma^\mu(P_R-P_L)$; $A_V=0$, $A_A=-2A_0$; $P=e^{i\theta}I_2$ branch-blind | vector safe / axial anomalous | `chiral_anomaly.py:L711-736 gauge_vs_axial_weighting_symbolic()` | unknown (inferred: exact) |
| 8 | $u^\pm=c_xc_yc_z\pm s_xs_ys_z$, $n$ as `lattice.bcc._bcc_uvec` (spot-checked equal) at $q=k/\sqrt3$ | symbolic Bloch data | `chiral_anomaly.py:L774-778 _bcc_u_n()` | unknown (inferred: exact) |
| 9 | FCC reciprocal lattice $\pi(1,1,0),\pi(1,0,1),\pi(0,1,1)$, BZ volume $2\pi^3$ = cube/4; Weyl points Γ (χ=−1) and $R=\tfrac\pi2(1,1,\pm1)$ (χ=+1), χ = sign $\det(\partial n_i/\partial q_j)$; partner $u=-1$ at $R$ | Weyl-point census, NN sum = 0 | `chiral_anomaly.py:L825-911 weyl_point_census()` | unknown (inferred: exact) |
| 10 | zeros of $\omega^\pm$ on the $n^3$ cube, folded mod $2\pi$ then mod FCC: $8\to2$ | numerical census confirmation | `chiral_anomaly.py:L940-1009 weyl_point_scan()` | unknown (inferred: machine) |
| 11 | $\Gamma=\dfrac{\alpha^2m_\pi^3}{64\pi^3f_\pi^2}\,(N_c/3)^2$ | π⁰→γγ width vs PDG 7.80±0.12 eV | `chiral_anomaly.py:L1179-1185 pi0_to_gamma_gamma()` | unknown (inferred: quantitative (spot-check 7.749 eV, −0.65%)) |

**Inputs → outputs:** none / $(m_\pi,f_\pi,\alpha,N_c)$ → exact-gate dicts and the width. **Depends on:** `constants.f_pi_gamma_convention_MeV` $=92.28$ MeV (external, PDG; see 01-constants.md); sympy. **Flags:** (a) **Docstring sign mismatch.** `gamma5_basis_symbolic` (L207) and the A3 docstring (L404) state $\operatorname{Tr}[\gamma_5\sigma\sigma]=-4i\epsilon$; the code asserts $+4i\epsilon$ (L267, L462), as does the module header (L34). (b) The Fujikawa gate tests only the magnitude. The "−2/i" Euclidean step (L486) is written in by hand, not derived, and the sign is declared a convention. (c) Some legs are tautological by construction: `vector_div_cancels` compares $\gamma^a-\gamma^a$ (L351-352); $A_V$/$A_A$ are arithmetic on a hand-set $\pm A_0$ (L718-719); the charge cube is $q^3-q^3$ (L725). (d) Unregistered literals: `M_PI0_MEV`, `ALPHA_EM=1/137.035999`, `GAMMA_PI0_PDG_EV`/`ERR` (L139-143). (e) The registry has no findings or exactness, but inventory F264 rows (#323ff) list these as exact.

---

### `engine/gauge/colour_condensate.py` — colour-magnetic condensate: Nielsen–Olesen, Savvidy, DeGrand–Toussaint monopoles (F88)
**Status:** live · driven (15 ch) · **Findings:** registry none; code/inventory: F88 (with F26, F43, F70, F86); inventory rows F88-CC1…CC7, F88-D3 · **Lattice:** 2-D square torus and 3-D simple-cubic compact U(1) (**reference lattices, not BCC**, D1) · **Law:** n/a (spectra and Monte Carlo; "Ω²" is used in the F26 sense of a rotation rate squared) · **Units:** lattice ($e^2=1/\beta$ in 3-D)

**Does:** Route 1 shows the uniform-chromomagnetic perturbative vacuum is unstable: a tachyonic spin-aligned charged mode, and a lower one-loop (Savvidy) energy. Route 2 counts DeGrand–Toussaint monopoles on compact links, checks the Villain/Poisson and Coulomb-gas↔sine-Gordon identities, and measures the monopole density by 3-D compact-U(1) Metropolis. It then chains $\rho\to z\to m_D\to v$ into F86's $\sigma=2\pi v^2$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\phi=2\pi q/L^2$; $U_y(n)=e^{i\phi n_x}$, seam $U_x(L{-}1,n_y)=e^{-i\phi Ln_y}$ | uniform-flux compact links on the torus | `colour_condensate.py:L70-76 flux_links_2d()` | unknown (inferred: exact) |
| 2 | $(-D^2\psi)(n)=4\psi-\sum_\mu\big[U_\mu(n)\psi(n{+}\mu)+U_\mu^*(n{-}\mu)\psi(n{-}\mu)\big]$ | gauge-covariant lattice Laplacian (dense) | `colour_condensate.py:L99-105 charged_laplacian_matrix()` | unknown (inferred: exact (matrix)) |
| 3 | $\Omega^2=\lambda_i-2\sin\phi$; certificate $\min\Omega^2<0$, $\min\Omega^2/\phi\to-1$ | Nielsen–Olesen tachyon | `colour_condensate.py:L121-123 tachyon_certificate()` | unknown (inferred: machine (eigvalsh)) |
| 4 | $\omega^2=\lambda_i+2-2\cos k_z\pm2\sin\phi$; $E=\tfrac12\sum\operatorname{Re}\omega$ (tachyons → 0); $\Delta E(B)=E(B)-E(0)$ | one-loop Savvidy energy (lattice-regulated) | `colour_condensate.py:L143-151 one_loop_energy_2plus1()`, `L158-163 savvidy_scan()` | unknown (inferred: quantitative) |
| 5 | $\theta_P=\theta_\mu+\theta_\nu(n{+}\mu)-\theta_\mu(n{+}\nu)-\theta_\nu$; $n_P=\operatorname{rint}\big((\theta_P-\bar\theta_P)/2\pi\big)$; $m=\sum\pm\Delta n_P$ | DeGrand–Toussaint monopole number | `colour_condensate.py:L172-205 _plaq_angle_3d()/dgt_monopole_field()` | exact (integer) (inventory F88-CC5) |
| 6 | $A=\frac{1-z/r}{2\rho^2}(-y,x,0)$ pair, midpoint link angles | Dirac monopole–antimonopole test pair | `colour_condensate.py:L236-254 dirac_pair_config()` | unknown (inferred: exact (topological)) |
| 7 | $\theta_i=\arg U_{ii}$, $i=1,2$ | naive Abelian (Cartan) projection of SU(3) | `colour_condensate.py:L267-269 su3_diag_phases()` | unknown (inferred: exact (definition)) |
| 8 | $\sum_ne^{-\frac\beta2(\theta-2\pi n)^2}=\frac1{\sqrt{2\pi\beta}}\sum_me^{-m^2/2\beta}e^{im\theta}$ | Villain/Poisson identity | `colour_condensate.py:L299-303 villain_poisson_residual()` | unknown (inferred: machine) |
| 9 | $\langle e^{iq\cdot\chi}\rangle=e^{-\frac12q^{\mathsf T}Gq}$, $G=(\kappa(-\Delta)+m^2)^{-1}$ | Coulomb-gas ↔ sine-Gordon Gaussian identity | `colour_condensate.py:L316-338 coulomb_gas_gaussian_residual()` | unknown (inferred: machine) |
| 10 | $\kappa=\beta/4\pi^2$, $z=\rho/2$, $m_D=\sqrt{2z/\kappa}=2\pi\sqrt{\rho/\beta}$ | Polyakov Debye mass | `colour_condensate.py:L344-346 debye_mass()` | unknown (inferred: exact (formula)) |
| 11 | $v=m_D\sqrt\beta$ ($e^2=1/\beta$), $\sigma_{F86}=2\pi v^2$ | F86 hand-off | `colour_condensate.py:L352-354 f86_vev_from_density()` | unknown (inferred: exact (formula)) |
| 12 | $S=-\beta\sum_P\cos\theta_P$; checkerboard Metropolis with $\Delta S=-\beta[(\cos\theta'-\cos\theta)S_x+(\sin\theta'-\sin\theta)S_y]$; $\rho=\sum\lvert m\rvert/L^3$ | 3-D compact U(1) MC, monopole density | `colour_condensate.py:L400-406 u1_metropolis_3d()`, `L373-379 _staple_sum_3d()` | unknown (inferred: quantitative (stochastic)) |

**Inputs → outputs:** $(L,q)$ or link-angle fields → spectra, $\Delta E$, integer monopole fields, $\rho(\beta)$, $(v,\sigma)$. **Depends on:** numpy only (direct import, D8). Consumed by `colour_dielectric` Part D. **Flags:** (a) In `u1_metropolis_3d` the staple sums are computed once per direction $\mu$ (L397) and reused for **both** checkerboard parities (L398-403). Same-direction links in the other parity share plaquettes (via $\theta_\mu(n{\pm}\nu)$), so the second half-sweep uses stale staples, which breaks detailed balance. `bcc_action._update_field` guards against exactly this defect and gates it as a control. $\rho(\beta)$, and everything chained from it ($m_D$, $v$, $\sigma_{F86}$), inherits the defect. (b) The model runs on 2-D square / 3-D cubic reference lattices, not BCC. (c) The registry records no findings or exactness.

---

### `engine/gauge/colour_dielectric.py` — confinement as a colour dielectric / dual superconductor (P1 Option C)
**Status:** live · driven (15 ch) · **Findings:** registry none; code/inventory: F86 (CD1…CD6), F43, F64, F70, F88, F91 · **Lattice:** Part B and D-iv (2-D) on the 2-D square (reference); Part D-i/D-iii/D-iv (3-D) on BCC · **Law:** **even** $\Omega_\text{even}=\omega^+(k/2)+\omega^-(k/2)$ for BCC gluon steps (F91, gluon even, forced); 2-D steps use `bilinear_2d.rotation_omega_2d` · **Units:** lattice; Part A dimensionless $x=evr$

**Does:** Part A solves the BPS (κ=1) ANO vortex by RK4 shooting, with $\sigma=2\pi v^2n$ exact. Part B maps the condensate to a dielectric $\varepsilon_c=1-f^2$ and rescales the gluon rotation rate by $\sqrt{\varepsilon_c}$. Part C covers dual-London screening and the linear potential. Part D wires the dielectric and the F88 gap into the time-evolved even-law BCC gluon propagator.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\sigma=2\pi v^2\lvert n\rvert$ | exact BPS tension | `colour_dielectric.py:L101 bps_string_tension()` | exact (inventory F86-CD1) |
| 2 | $\lambda=1/(ev)$, $\xi=1/(\kappa ev)$ | penetration depth, coherence length | `colour_dielectric.py:L111, L120-121` | unknown (inferred: exact) |
| 3 | $f_x=nf(1-a)/x,\ a_x=(x/n)(1-f^2)$; seed $f\sim cx^n$, $a\sim x^2/2n$; RK4 + bisection on $c$ | Bogomolny profile by shooting | `colour_dielectric.py:L128-130 _bps_rhs()`, `L149-156 _integrate_bps()`, `L183-203 solve_bps_profile()` | unknown (inferred: quantitative (ODE)) |
| 4 | $\frac{\sigma}{2\pi v^2}=\int x\,dx\big[f_x^2+\frac{n^2f^2(1-a)^2}{x^2}+\frac{n^2a_x^2}{2x^2}+\tfrac12(f^2-1)^2\big]$ | numerical tension check | `colour_dielectric.py:L222-227 string_tension_numeric()` | unknown (inferred: quantitative) |
| 5 | $\Phi=2\pi n\,a(x_\text{max})/e$ | quantised colour-electric flux | `colour_dielectric.py:L240 colour_electric_flux()` | unknown (inferred: quantitative) |
| 6 | $\varepsilon_c=1-f^2$, $n_c=\varepsilon_c^{-1/2}$ | condensate → dielectric → refractive factor | `colour_dielectric.py:L268, L273-274` | unknown (inferred: exact (definition)) |
| 7 | $\Omega\to\Omega_\text{2D}(k)\sqrt{\varepsilon_c}$ (uniform), per-octet spectral rotation; $\varepsilon_c=1$ → free 2-D gluon step bit-for-bit | 2-D dielectric gluon step | `colour_dielectric.py:L319-328 gluon_dielectric_rotation_step_2d()` | exact (inventory F86-CD4) |
| 8 | $c_\text{eff}=c_\text{lat}\sqrt{\varepsilon_c}$, $c_\text{lat}=1/\sqrt3$ (F26) | renormalised speed | `colour_dielectric.py:L339-340 effective_lattice_c()` | unknown (inferred: exact) |
| 9 | $(-\nabla^2_\text{lat}+m^2)E=\rho$, $-\nabla^2_\text{lat}\to\sum(2-2\cos k_i)$ | dual-London screened field | `colour_dielectric.py:L372-374 london_screened_field_2d()` | unknown (inferred: machine) |
| 10 | fit slope of $\ln(\lvert E\rvert\sqrt r)$ vs $r$ → $-1/\lambda$ ($K_0$ prefactor removed) | penetration-depth fit | `colour_dielectric.py:L395-398 fit_penetration_depth()` | unknown (inferred: quantitative) |
| 11 | $V(R)=\sigma R+\mu$; $E(R)=\sigma_\text{num}R$ | linear potential from a constant cross-section | `colour_dielectric.py:L405, L417-418` | exact (inventory F86-CD6: 1e-14) |
| 12 | $\Omega\to\Omega_\text{even}(k)\sqrt{\varepsilon_c}$ on BCC; $\varepsilon_c=1$ → `gluon_rotation_step_spectral_bcc` bit-for-bit | BCC even-law dielectric gluon step (D-i) | `colour_dielectric.py:L503-516 gluon_dielectric_rotation_step_bcc()` | unknown (inferred: exact (orthogonal per mode)) |
| 13 | $m_V=m_D=2\pi\sqrt{\rho/\beta}$; $\omega_\text{eff}=\sqrt{m_V^2+\Omega_\text{even}^2}$ | gap-massive gluon step (D-ii/iii) | `colour_dielectric.py:L529-531, L565-566 gluon_gap_massive_step_bcc()` | unknown (inferred: exact (given ρ)) |
| 14 | $(E,B)\leftarrow(E,B)+s(x)\big[R_\text{free}(\Omega\,dt)(E,B)-(E,B)\big]$, $s=\sqrt{\varepsilon_c(x)}$ | spatially varying dielectric split-step (flux expulsion, D-iv) | `colour_dielectric.py:L643-650 gluon_dielectric_evolve_2d()`, `L660-667 _bcc()` | unknown |
| 15 | $\mathcal E=\sum(E^2+B^2)$ | field energy | `colour_dielectric.py:L673 field_energy()` | unknown (inferred: exact (definition)) |

**Inputs → outputs:** $(v,n,e,\kappa)$; octet fields $(8,\dots)$; $\varepsilon_c$ (uniform or a field); $(\beta,\rho)$ → profiles, tensions, stepped fields. **Depends on:** `gauge.gluon` (`gluon_rotation_step_spectral_2d/_bcc`, `gluon_massive_step_spectral_bcc`), `gauge.weak_wmu` (`_kgrid3d`, `_omega_even`) (05b); `gauge.colour_condensate` (above); `gauge.bilinear_2d.rotation_omega_2d` (above; a 2-D rate only, **not** a σ-bilinear photon); `constants.c_lat`. **Flags:** (a) The `string_tension_numeric` docstring (L210-211) gives the potential term as $\tfrac14(f^2-1)^2$; the code (L225) and the Part-A comment (L87) use $\tfrac12(f^2-1)^2$. (b) The D-iv docstring claims a "2nd-order-in-dt split-step" (L630-632), but the scheme $X+s(RX-X)$ is a local convex blend. It is not norm-preserving for $0<s<1$, and its order was never verified in code, hence exactness `unknown`. (c) The module frames confinement as parallel to "F64's gravitational dielectric". CLAUDE.md decision 4 / F178 reclassifies F64's dielectric as the vacuum/weak-field representation of the induced Einstein equation, so the framing rests on a reclassified finding. The code does not depend on F64. (d) The Part-B docstring calls the 2-D rate "F43 gluon rotation rule"; on the 2-D square the rate is the single-rate `rotation_omega_2d`, with no even/chiral distinction. (e) The `u1_metropolis_3d` staple-reuse defect propagates into `condensate_vev_from_mc` (see `colour_condensate` flag (a)).

---

### `engine/gauge/colour_theta.py` — θ_QCD on the rule's own gauge sector (strong CP, B11)
**Status:** live · standalone · **Findings:** F321 F53 F43 F305 F307 F265 F91 F27 F162 F337 F340 F308 · **Lattice:** $\mathrm{BCC}_3\times\mathbb Z$ (4 ⟨111⟩ axes + time, 20 oriented minimal loops); hypercubic reference loop set as control · **Law:** T4 compares even $\omega^+(k)+\omega^-(k)$ (P-even) vs the single chiral branch (not P-even) · **Units:** lattice

**Does:** shows the rule's Euclidean gauge action is real. The reasons: the loop set is closed under reversal, $\mathrm{hol}(\bar w)=\mathrm{hol}(w)^\dagger$, and every vertex coefficient is real at every leg count. Since the θ-term is the unique imaginary gauge invariant, $\theta_\text{QCD}=0$ in the rule. The strong-CP question is thereby relocated to $\arg\det M_q$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | every oriented loop's reverse is in the set (20 BCC, 12 hypercubic) | reversal closure (premise) | `colour_theta.py:L177-184 loop_set_reversal_closure()` | exact (reg) |
| 2 | $P_w=\prod_{\text{steps}}U$, reverse step $U_{-d}(x)=U_d(x-d)^\dagger$ | based holonomy of a loop word | `colour_theta.py:L229-247 _link()/holonomy()` | exact (reg) |
| 3 | $S=-\sum_\text{loops}\operatorname{Tr}U_\text{loop}$ (complex, never Re-projected); control: $S-i\theta\sum Q$ | Euclidean loop action | `colour_theta.py:L261-270 loop_action()` | machine (Im S < 1e-10) (reg: exact; row is weaker — see flags) |
| 4 | $\Phi^a=\operatorname{Im}\operatorname{tr}(T^aP)/c$; clover $\tfrac14[\Phi(x)+\Phi(x{-}a)+\Phi(x{-}b)+\Phi(x{-}a{-}b)]$ | loop phases centred on sites | `colour_theta.py:L279-281 _phases()`, `L297-299 _clover()` | machine (reg: exact; row is weaker — see flags) |
| 5 | $E=\tfrac14\sum_id_i\Phi_{(d_i,t)}$, $B=\tfrac14\sum_pm_p\Phi_p$ (from $\sum dd^{\mathsf T}=M^{\mathsf T}M=4I$), $Q=\sum_aE^a\cdot B^a$ | topological density on rhombi | `colour_theta.py:L313-332 topological_density()` | machine (normalisation is a convention) (reg: exact; row is weaker — see flags) |
| 6 | $(PU)_i(x)=U_i(-x-d_i)^\dagger$; CP $=$ conj∘P; $U\to U^*$ | discrete maps | `colour_theta.py:L344-354, L359, L371` | exact (reg) |
| 7 | $\operatorname{Im}S(\theta)=\operatorname{Im}S(0)-\theta\sum Q$ | θ sensitivity (non-vacuity) | `colour_theta.py:L388-396 theta_sensitivity()` | machine (reg: exact; row is weaker — see flags) |
| 8 | all position-space vertex coefficients real ⇔ $V(-k)=\overline{V(k)}$, sampled over colour indices, 2/3/4 legs | vertex reality | `colour_theta.py:L434-459 _terms_colour()`, `L476-485 vertex_reality_defect()` | exact (reg) |
| 9 | $\omega^+(-k)+\omega^-(-k)=\omega^+(k)+\omega^-(k)$; $\omega^+(-k)\neq\omega^+(k)$ | even law P-even, chiral not | `colour_theta.py:L503-511 even_law_parity_defect()` | exact (reg) |
| 10 | $M=\begin{pmatrix}0&ime^{i\theta}\\ime^{-i\theta}&0\end{pmatrix}$, $\det M=+m^2$, $\arg\det M=0$ | one-generation θ̄ second term | `colour_theta.py:L531-538 thetabar_one_generation()` | exact (reg) |
| 11 | $\mathrm{hol}(U,\bar w)=\mathrm{hol}(U,w)^\dagger$ for all 20 words ⇒ $S=-\sum_\text{pairs}2\operatorname{Re}\operatorname{Tr}$ for every $U$ | configuration-independent reality proof (F340) | `colour_theta.py:L805-815 reversal_holonomy_identity()` | exact (reg) |
| 12 | loop-word set equals `lpt_bcc_vertex._loops_bcc()` (20 = 20) | action identity with the LPT vertex action (F337 L6) | `colour_theta.py:L754-770 action_matches_lpt_bcc_vertex()` | exact (reg) |

**Inputs → outputs:** SU(3) link fields `U[5]` of shape (4,4,4,4,3,3) → $S$, $Q$, defects, gates (`check_strong_cp` T0–T5 with controls; `check_strong_cp_nonperturbative` U1–U3). **Depends on:** `core.lpt_generator.T_GEN` (04-core.md); `gauge.lpt_bcc_vertex` (05b/05c); `lattice.bcc.bcc_dispersion` and `lattice.geometry` BCC constants (03-lattice.md); `numerics.xp`, `numerics.rng`. **Flags:** (a) `random_su3_links_4d` describes the `scale<1` pull as a "geodesic pull towards the identity" (L209). The code is a linear interpolation $(1-s)I+sU$ followed by QR re-unitarisation, not a geodesic. (b) On import, `_register_one_sense_action()` (L420) mutates `lpt_bcc_vertex.ACTIONS`. It is additive, but it is an import-time side effect on another module. (c) The docstring discloses that the clover $Q$ is **not** a parity eigenstate at finite $a$ (defect 0.42–0.83, L71-79). Every P-oddness statement about $E\cdot B$ is continuum-only.
