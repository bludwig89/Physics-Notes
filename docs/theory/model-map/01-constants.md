# 01 — Constants (`src/casim/constants/`, decision D7)

**Scope.** Every file in `src/casim/constants/`: the registry machinery (`__init__.py`), the five sector modules (`geometry`, `gravity`, `lepton`, `strong`, `electroweak`) that register **51 constants**, and `measured.py`, which declares **16 `MeasuredConstant` records** (sites that legitimately compute or carry a number equal to a registry value). This package is the D7 value owner. It is **not** in the engine module registry (`casim.engine.registry` covers `engine/` only), so it has no registry `status`/`reach` line. Each constant's exactness class below is the one the constant **declares on itself** (`Constant.exactness`), which is the D7 registry's own field. The vocabulary is `exact | machine | quantitative | bracketed | external` (`__init__.py:L92`).

**Conventions.** Lattice constants are in lattice natural units ($a=\tau=\hbar=1$). On the canonical **BCC** lattice (D1) the light speed is $c_\text{lat}=1/\sqrt3$ cells/tick. SI anchors are CODATA/SI and are `external` (or `exact` only where SI *defines* them). A rational constant exports the `Fraction` under its symbol and a float twin `<symbol>_f` (`__init__.py:L392-394`). A bracketed constant exports **no scalar**. `hypercharge` uses $Y=2y$, $Q=T_3+Y/2$ (`electroweak.py:L109`).

**Modules covered:** `constants/__init__.py`, `constants/geometry.py`, `constants/gravity.py`, `constants/lepton.py`, `constants/strong.py`, `constants/electroweak.py`, `constants/measured.py`.

---

### `constants/__init__.py` — registry machinery (plumbing)
**Status:** D7 package (not in engine registry) · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

**Does:** Defines the typed registry and the import surface. It holds no physics.

- `Site(path, name, kind, expected, note)` (`L133`): records where a constant is bound. `kind` ∈ {`import`, `literal`, `reexport`, `runtime`} (`L103`). `expected` is allowed only on `literal` sites (a rounded local copy, `L156`).
- `Constant` (`L162`): `symbol, units, exactness, provenance, derivation, sector, value | bracket, supersedes, sites, tol, sweep, sweep_reason, notes`. `__post_init__` (`L179`) raises on:
  - an unknown exactness class or sector;
  - an empty provenance;
  - both a value and a bracket, or neither;
  - an inverted bracket;
  - a non-identifier symbol;
  - `sweep=False` with no reason.
- `float_value` (`L216`) returns the bracket **midpoint** for bracketed constants. This is a display convenience only; the docstring says so.
- `contains(x)` (`L238`): the relative-tolerance match, with a $10^{-9}$-padded bracket test.
- `MeasuredConstant(path, name, compares_to, reason, kind, value, provenance, tol)` (`L253`): `kind` ∈ {`measured`, `coincidence`} (`L111`). A reason is mandatory (`L294`).
- `register` (`L300`, raises on a duplicate symbol) and `register_measured` (`L307`). Queries: `get`, `value`, `exact`, `all_constants`, `sweepable_constants`, `by_finding`, `sites_for`, `all_measured`, `measured_at` (`L312-364`).
- `_is_diagnostic_value(v)` (`L126`) decides whether finding a number is evidence. Small integers with $\lvert v\rvert\le100$ and $\{0.25, 0.5, 0.75, 1.5, 2.5\}$ are not diagnostic, which is why several constants carry `sweep=False`.
- `_export()` (`L385`) sets `globals()[symbol] = value` for every non-bracketed constant. For each `Fraction` it also sets `<symbol>_f = float(value)` (`L392-394`).
- `bracket(symbol)` (`L400`) and `endpoint(symbol, 'lo'|'hi')` (`L409`) are the only access to a bracketed constant.

**Inputs → outputs:** sector modules → `_REGISTRY` / `_MEASURED` → module-level names. **Depends on:** nothing. **Flags:** none.

---

### `constants/geometry.py` — lattice ruler, lattice light speed, SI anchors
**Status:** D7 package · **Findings:** F26 F79 F107 F327 · **Lattice:** BCC (for `c_lat`) · **Law:** n/a · **Units:** mixed (lattice + SI)

**Does:** Owns $a/\ell_P$, $c_\text{lat}$ and the SI/CODATA bridges and LIV bounds used to put lattice results into physical units.

| # | Symbol | Closed form (as computed) | `_f` | Exactness | Provenance | Where |
|---|---|---|---|---|---|---|
| 1 | `a_over_ellP` | $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (so $(a/\ell_P)^2=8\pi\sqrt3$) | — | exact | F79, F107 (supersedes the `F83-ceiling-anchor`) | `geometry.py:L23` `A_OVER_ELLP` (registered L25) |
| 2 | `c_lat` | $c_\text{lat}=1/\sqrt3$ | — | exact | F26 | `geometry.py:L90` `C_LAT_BCC` (registered L92) |
| 3 | `ell_P_m` | $1.616255\times10^{-35}$ m (CODATA) | — | external | CODATA | `geometry.py:L190` |
| 4 | `c_SI` | $299\,792\,458$ m/s (SI definition) | — | external | SI | `geometry.py:L209` |
| 5 | `hbar_SI` | $1.054571817\times10^{-34}$ J s (CODATA 10-digit quote) | — | external | CODATA | `geometry.py:L230` |
| 6 | `hbar_SI_from_h` | $h/(2\pi)$, $h=6.62607015\times10^{-34}$ J s (exact by SI) | — | exact | SI | `geometry.py:L242` |
| 7 | `G_CODATA` | $6.67430\times10^{-11}$ m³ kg⁻¹ s⁻² (comparison target) | — | external | CODATA | `geometry.py:L265` |
| 8 | `J_per_GeV` | $10^9\,e$, $e=1.602176634\times10^{-19}$ C → $1.602176634\times10^{-10}$ J/GeV | — | exact | SI | `geometry.py:L291` |
| 9 | `E_LV_e_sup_min_GeV` | $9.4\times10^{25}$ GeV: lower bound on the superluminal $n=1$ electron LIV scale (Li & Ma 2022, arXiv:2204.02956) | — | external | F327 | `geometry.py:L340` |
| 10 | `E_LV_e_sub_min_GeV` | $1.0\times10^{24}$ GeV: the subluminal $n=1$ bound (same source) | — | external | F327 | `geometry.py:L362` |
| 11 | `m_e_GeV` | $0.51099895000\times10^{-3}$ GeV (CODATA/PDG) | — | external | CODATA | `geometry.py:L381` |
| 12 | `E_crab_photon_max_GeV` | $1.12\times10^{6}$ GeV (LHAASO Crab, Cao et al. 2021) | — | external | F327 | `geometry.py:L420` |

**Notes.**
- #1 and #2 are computed as `math` float expressions, not decimals.
- The `c_lat` derivation string defines it as $d\Omega/d\lvert\mathbf k\rvert$ at $\lvert\mathbf k\rvert\to0$ with $\Omega=2\omega(\lvert\mathbf k\rvert/2)$. The code does not compute that; it hard-codes the BCC result $1/\sqrt3$. That is consistent with the D1 BCC choice. The measured versions on other lattices are in `measured.py` (1/√2 on the 2-D square lattice, 1.0 on the simple-cubic fork).
- `hbar_SI` and `hbar_SI_from_h` differ by about $6\times10^{-11}$ relative. They are kept apart on purpose.
- `G_CODATA` is kept apart from `G_LATTICE` (gravity) so that F79's prediction of G is not turned into an input.
- #9 and #10 are **bounds** (the model passes only if its own $E_\text{LV}$ exceeds them), not measurements.

**Inputs → outputs:** none → registry values. **Depends on:** `__init__`. **Flags:** none.

---

### `constants/gravity.py` — Newton's constant in lattice units, F106 coefficient
**Status:** D7 package · **Findings:** F79 F106 F107 F178 · **Lattice:** BCC · **Law:** n/a · **Units:** lattice

| # | Symbol | Closed form (as computed) | `_f` | Exactness | Provenance | Where |
|---|---|---|---|---|---|---|
| 1 | `G_LATTICE` | $G=1/(72\pi)$ $\bigl(=c_\text{lat}^4/(8\pi)=a^2c^3/(8\pi\sqrt3\hbar)$ at $a=\hbar=1,\ c=1/\sqrt3\bigr)$ | — | exact | F79, F107 | `gravity.py:L18` (registered L20) |
| 2 | `F106_COEFF_LATTICE` | $8\pi G/c^4=1$ exactly in lattice units, so $\nabla^2\ln K=-T^{00}$ | — | exact | F106, F178 | `gravity.py:L48` |

**Notes.**
- Row 1: the code writes `1.0/(72.0*math.pi)` directly. It does not compute it from `c_lat`. Algebra check: $(1/\sqrt3)^4/(8\pi)=1/(72\pi)$ ✓, and $8\pi\cdot\tfrac{1}{72\pi}\cdot 9=1$ ✓.
- Row 2 is the literal `1.0` with `sweep=False`.
- **F106 law reclassified by F178.** Per `supersessions.yaml` L440-446 the energy-only law $\nabla^2\ln K=-T^{00}$ is the *static weak-field reduction* of $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$. The coefficient's value is unchanged; the law it belongs to is no longer fundamental. Mark: **SUPERSEDED-as-fundamental by F178 (reclassified, value live)**.

**Depends on:** `__init__`. **Flags:** reclassification (see flags file).

---

### `constants/lepton.py` — weight-as-phase constants (E_g sector)
**Status:** D7 package · **Findings:** F92 F93 F95 F101 F108 F118 F175 F234 F253 F255 F256 · **Lattice:** BCC (O_h rep theory) · **Law:** n/a · **Units:** dimensionless

**Does:** Carries the charged-lepton canon: $\delta^*=2/9$ is **primary** (key decision 7), and $\lambda_6$ and $W$ are **outputs** via the F234 arrow.

| # | Symbol | Closed form (as computed) | `_f` | Exactness | Provenance | Where |
|---|---|---|---|---|---|---|
| 1 | `delta_star` | `Fraction(2, 9)`: $\delta^*=\dim E_g/\dim(T_{1u}\otimes T_{1u})=2/9$ rad | `delta_star_f` | exact | F175, F253, F255, F256 (supersedes F179-CN3) | `lepton.py:L28` (registered L30) |
| 2 | `cos3_delta_star` | $\cos(3\delta^*)=\cos(2/3)$, computed as `math.cos(3*float(DELTA_STAR))` | — | exact | F175, F253 | `lepton.py:L71` |
| 3 | `cos3_delta_data` | $0.785874$ (empirical, from F93-O7 lepton masses) | — | quantitative | F93, F95 | `lepton.py:L84` |
| 4 | `lambda_6` | literal $0.243$. The derivation string gives $\lambda_6=\lvert B\rvert/(2e^6\cos\tfrac23)$ | — | quantitative | F234, F253, F256 (supersedes F179-CN3) | `lepton.py:L117` |
| 5 | `W_star` | $6\times0.243=1.458$ (literal product; the derivation string says $W=6\lambda_6$) | — | quantitative | F101, F108, F118, F234 | `lepton.py:L145` |
| 6 | `B_sea_cubic` | $B=-5.69\times10^{-2}$ (F95 full-BZ Dirac-sea cubic) | — | quantitative | F95 | `lepton.py:L168` |
| 7 | `e_saturation` | $e=0.733$ (F92/F118 saturation amplitude) | — | quantitative | F92, F118, F234 | `lepton.py:L188` |

**Notes.**
- Rows 2 and 3 are **two different objects**, about $1.7\times10^{-5}$ apart. That gap is the F256 near-coincidence. They are kept separate on purpose.
- ⚠ **DOC/CODE MISMATCH (row 4).** Evaluating the derivation string with the registry's own inputs (rows 6 and 7) gives
  $$\lvert B\rvert/(2e^6\cos\tfrac23)=0.0569/(2\cdot0.733^6\cdot0.78589)=0.2334,$$
  not the registered 0.243. That is a 4 % gap, 8× the constant's own `tol=5e-3`. F234 L39 reaches 0.243 as $C/e^6$ with the same $C=0.0362$ and $e\approx0.733$. To get 0.243 you need $e^6=0.149$, i.e. $e\approx0.728$. Not settled here.
- Row 5 repeats the literal 0.243 instead of resolving from `lambda_6`, so the two could drift apart. Tree sites quote $W=1.46$ (`expected=1.46`).

**Depends on:** `__init__`. **Flags:** lambda_6 arrow mismatch; W_star duplicated literal.

---

### `constants/strong.py` — QCD anchor, IR bracket, scales, calibration block
**Status:** D7 package · **Findings:** F77 F88 F104 F116 F117 F122 F123 F124 F145 F146 F151 F152 F154 F155 · **Lattice:** n/a (NJL / lattice-unit bridge) · **Law:** n/a · **Units:** mixed (MeV/GeV/lattice/fm)

**Does:** Registers the strong sector's one dimensionful anchor, the fitted NJL triple, the IR-coupling bracket and its two scale choices, the unit bridges, and the external comparison targets.

| # | Symbol | Closed form / value (as computed) | `_f` | Exactness | Provenance | Where |
|---|---|---|---|---|---|---|
| 1 | `c_fierz_colour` | `Fraction(2, 9)`: colour-Fierz coefficient, OGE → NJL scalar channel ($G_S=\tfrac29\,\tfrac{g^2}{2}/(\epsilon_cK+M_g^2)$) | `c_fierz_colour_f` | exact | F77, F116, F256 | `strong.py:L45` |
| 2 | `f_pi_anchor_MeV` | 92.07 MeV: **the** model anchor, an input | — | external | F77, F123 | `strong.py:L78` |
| 3 | `f_pi_pdg_target_MeV` | 92.4 MeV: PDG comparison target, never an input | — | external | PDG | `strong.py:L99` |
| 4 | `f_pi_gamma_convention_MeV` | 92.28 MeV: the $\Gamma=a^2m^3/(64\pi^3f_\pi^2)$ convention (string writes `a^2`, read as $\alpha^2$) (π⁰→γγ only) | — | external | PDG | `strong.py:L117` |
| 5 | `GeV_per_lattice_unit` | $\Lambda_\text{NJL}/\pi$, with `LAMBDA_NJL_GEV = 0.6515` | — | exact (relative to a fitted Λ) | F77 | `strong.py:L135` `GEV_PER_UNIT` (registered L137) |
| 6 | `M0_constituent_MeV` | 311.2 MeV | — | quantitative | F77 | `strong.py:L154` |
| 7 | `M0_constituent_lattice` | 1.50 (lattice units) | — | quantitative | F77 | `strong.py:L170` |
| 8 | `M0_constituent_GeV` | $1.50\cdot\Lambda_\text{NJL}/\pi$ (≈ 0.31107 GeV; differs from 0.3112 in the last digit by design) | — | quantitative | F77 | `strong.py:L192` |
| 9 | `alpha_eff_star` | **bracket** $(0.376,\ 0.411)$, no scalar. `endpoint('alpha_eff_star','lo')`=0.376 (at $m_D$, F88); `'hi'`=0.411 (at $m_V$, F117) | — | bracketed | F88, F117, F145, F151, F152, F154 | `strong.py:L212` |
| 10 | `Lambda_QCD_nf3_GeV` | 0.347 GeV (V-scheme, $a_1=11/3$) | — | quantitative | F151 | `strong.py:L237` |
| 11 | `m_D_F88_lattice` | 0.532 (dual-Meissner/Debye gluon mass, F88 CC8 8³) | — | quantitative | F88 | `strong.py:L267` |
| 12 | `m_V_F117_lattice` | 0.727 (same chain, F117 L=6) | — | quantitative | F117 | `strong.py:L288` |
| 13 | `Lambda_NJL_GeV` | 0.6515 GeV: BZ-edge NJL cutoff, **fitted** | — | external | F77, F116 | `strong.py:L134` / L319 |
| 14 | `G_Lambda2_NJL` | 2.10: NJL $G\Lambda^2$, fitted | — | external | F77, F116 | `strong.py:L341` |
| 15 | `m0_current_quark_MeV` | 5.5 MeV: fitted current quark mass | — | external | F77, F116 | `strong.py:L359` |
| 16 | `g_A` | 1.2723 (nucleon axial charge) | — | external | PDG | `strong.py:L378` |
| 17 | `M_N_isoaveraged_MeV` | 938.918 MeV | — | external | PDG | `strong.py:L394` |
| 18 | `M_n_neutron_MeV` | 939.56542052 MeV | — | external | CODATA | `strong.py:L411` |
| 19 | `r_c_hardcore_fm` | 0.448 fm: deuteron hard core, **tuned** to the binding energy | — | quantitative | F104 | `strong.py:L424` |
| 20 | `g_rho_pi_pi` | 6.0 (KSRF $m_\rho^2=2g^2f_\pi^2$ contrast only) | — | external | PDG | `strong.py:L445` |
| 21 | `alpha_hat0_over_pi_CZBR` | 0.97 (Cui–Zhang–Binosi–Roberts arXiv:1912.08232; target) | — | external | PDG | `strong.py:L470` |
| 22 | `m_g_continuum_GeV` | 0.50 GeV (continuum Landau-gauge gluon mass, ±0.20 carried at the site) | — | external | FLAG | `strong.py:L485` |
| 23 | `q_star_a_band_lo` | $1/\sqrt3$ (inverse lattice spacing): lower edge of the F151 q* band | — | exact | F151, F155 | `strong.py:L505` |
| 24 | `q_star_a_implied` | 0.7327 (PDG-implied q*a) | — | quantitative | F151, F155 | `strong.py:L528` |
| 25 | `sqrt_sigma_GeV` | 0.42 GeV (string-tension anchor) | — | quantitative | F122, F124, F146 | `strong.py:L554` |

**Notes.**
- **Row 5** is tagged `exact`, but it is $\Lambda_\text{NJL}/\pi$ and $\Lambda_\text{NJL}$ (row 13) is a fit. So it is exact only as a conversion; every lattice→MeV number in the strong sector inherits the fit.
- **Row 9** ⚠ **DOC/CODE MISMATCH.** The derivation string also says "F154 … brackets it anchor-free to [0.31, 0.38], with 0.39 at the top". That is a different interval, and it does not contain the registered upper endpoint 0.411. The registered bracket is F88/F117's two **scale choices** (rows 11 and 12), and that is what the code carries.
- **Row 13** is registered as `external` although it is a fit, not a measurement. The derivation string says "FITTED".
- **Row 19** is a tuned knob but is classed `quantitative`, not `fit`. The map's `fit` tag applies.

**Depends on:** `__init__`. **Flags:** row 9 bracket prose; rows 5/13/19 exactness-class tension.

---

### `constants/electroweak.py` — Weinberg-angle faces and lepton hypercharges
**Status:** D7 package · **Findings:** F45 F47 F49 F138 F141 F165 F231 F266 F279 · **Lattice:** BCC (F141 Wigner–Seitz count) · **Law:** n/a · **Units:** dimensionless

| # | Symbol | Closed form (as computed) | `_f` | Exactness | Provenance | Where |
|---|---|---|---|---|---|---|
| 1 | `sin2_thetaW_uv` | `Fraction(1, 4)` $=\frac{g'^2/g^2}{1+g'^2/g^2}$ at $g'^2/g^2=1/3$ (UV/bare face) | `sin2_thetaW_uv_f` | exact | F45, F231 | `electroweak.py:L56` |
| 2 | `sin2_thetaW_onshell` | `Fraction(2, 9)` $=1-m_W^2/m_Z^2$ with $m_W^2:m_Z^2=7:9$ (BCC WS facet-axis count) | `sin2_thetaW_onshell_f` | exact | F49, F138, F141, F231 | `electroweak.py:L80` |
| 3 | `Y_LEPTON_L` | `Fraction(-1)`: the one free normalisation (unit of charge). Equivalently $y_Q=1/6$ ⇒ $y_L=-3y_Q=-1/2$, $Y_L=2y_L=-1$ | `Y_LEPTON_L_f` | exact (a choice of unit) | F165, F279 | `electroweak.py:L116` (registered L118) |
| 4 | `Y_E_R` | $2\,Y_L=-2$, resolved from row 3, not typed | `Y_E_R_f` | exact | F165, F279 | `electroweak.py:L155` |
| 5 | `Y_NU_R` | `Fraction(0)`: forced by $U(1)_Y$ invariance of the F47 Majorana term ($2y_\nu=0$) | `Y_NU_R_f` | exact | F279, F47, F266 | `electroweak.py:L183` |

**Notes.**
- Row 1 is written as a literal `Fraction(1, 4)`. Its $(1/3)/(4/3)$ computation happens at the runtime site `tests/runners/FA07_weinberg_angle.py`.
- The F279 ratio line is $y_Q:y_u:y_d:y_L:y_e:y_\nu=1:4:-2:-3:-6:0$ (derivation string, `L128`).
- The quark hypercharges are deliberately **not** registered: they need $N_c=3$, which is underived. They stay in `engine/gauge/hypercharge.py` (see 05a/05b gauge map).

**Depends on:** `__init__`. **Flags:** none.

---

### `constants/measured.py` — typed `MeasuredConstant` declarations (plumbing / provenance)
**Status:** D7 package · **Findings:** F26 F43 F77 F79 F151 F155 F205 F286 F295 F346 F355 F368 F369 · **Lattice:** mixed (square, cubic, BCC) · **Law:** n/a · **Units:** n/a

**Does:** Lists the 16 sites that carry a number equal to a registry value without importing it. Each record is either `measured` (the same quantity in a different regime) or `coincidence` (a different quantity that happens to have the same number).

| # | Site (path : name) | Compares to | Kind | Value (as computed) | Where |
|---|---|---|---|---|---|
| 1 | `interactions/derive_velocity_addition.py : C_LAT` | `c_lat` | measured | $1/\sqrt2$ (2-D square lattice, $1/\sqrt{2d}$ with $d=2$) | `measured.py:L44` |
| 2 | `tests/findings/test_SR5_photon_frame_invariance.py : C_LAT` | `c_lat` | measured | $1/\sqrt2$ | `measured.py:L57` |
| 3 | `forks/gauge/curl_fork_cubic.py : C_LAT` | `c_lat` | measured | $1$ (simple-cubic fork, D1) | `measured.py:L69` |
| 4 | `interactions/running_njl.py` | `c_lat` | coincidence | $1/\sqrt3$ (Gell-Mann $\lambda_8$ normalisation) | `measured.py:L85` |
| 5 | `gauge/strong.py` | `c_lat` | coincidence | $1/\sqrt3$ ($\lambda_8$ in `_LAMBDA[7]`) | `measured.py:L97` |
| 6 | `gauge/bgfield_loop.py` | `alpha_hat0_over_pi_CZBR` | coincidence | 0.97 (top of the q* band) | `measured.py:L108` |
| 7 | `gauge/bgfield_loop.py` | `e_saturation` | coincidence | 0.733 (q*a rounded) | `measured.py:L121` |
| 8 | `forks/gravity/gr_fork_F79_structural_G.py` | `a_over_ellP` | measured | $\sqrt{8\pi}\,3^{1/4}$ (derived in the fork, checked to $10^{-12}$) | `measured.py:L135` |
| 9 | `forks/gravity/gr_fork_F238_geon_relic_abundance.py` | `W_star` | coincidence | 1.453152027 (Abramowitz–Stegun erfc coefficient). Record has `provenance=()` | `measured.py:L149` |
| 10 | `forks/darkmatter/dm_fork_F205_sterile_qke_boltzmann.py : V_D` | `lambda_6` | coincidence | $2\zeta(3)/\pi^2$ | `measured.py:L162` |
| 11 | `interactions/cosmology_anomalous_dimension.py : two_ninths` | `delta_star` | coincidence | $2/9$ ($g_\text{eff}=2\pi(1-n_s)$; deliberately not tied to any of the three registered 2/9s) | `measured.py:L184` |
| 12 | `particles/derive_quark_shape_probe.py` | `e_saturation` | coincidence | 0.731 (F80 down-type Koide Q) | `measured.py:L204` |
| 13 | `interactions/horizon_entanglement.py : C_PLANE_REF` | `e_saturation` | coincidence | 0.734202 (measured (111)-plane entanglement coefficient) | `measured.py:L234` |
| 14 | `interactions/horizon_entanglement.py` | `m0_current_quark_MeV` | coincidence | 5.5 (a ball radius in units of $a$) | `measured.py:L249` |
| 15 | `interactions/cosmology_transfer_function.py` | `lambda_6` | coincidence | $2\zeta(3)/\pi^2$ (photon number density prefactor) | `measured.py:L262` |
| 16 | `interactions/cosmology_lambda_sequestering_consistency.py : w0` | `m_V_F117_lattice` | coincidence | −0.727 (DESI $w_0$, illustrative) | `measured.py:L276` |

`ζ(3)` is written as the decimal `1.2020569031595943` (L162, L262); no closed-form alternative exists in `math`.

**Depends on:** `__init__`. **Flags:** none beyond #9's empty provenance (by design: not a physics quantity).

---

## Value coincidences the code keeps separate (C2.2)

| Number | Separate constants / records | Why they are not merged |
|---|---|---|
| $2/9$ | `delta_star` (lepton, E_g weight F175), `sin2_thetaW_onshell` (electroweak, 7:9 count F141), `c_fierz_colour` (strong, OGE Fierz F77), plus the `coincidence` record for the F295 tilt coupling | Three unrelated derivations. Importing one symbol at a 2/9 site would assert a link |
| $1/\sqrt3$ | `c_lat` (a speed, cells/tick), `q_star_a_band_lo` (a momentum scale, 1/a), and the `coincidence` records for $\lambda_8$ | Different units and meaning |
| $f_\pi$ | 92.07 anchor, 92.4 PDG target, 92.28 Γ-convention | Input vs comparison target vs convention |
| $\cos3\delta^*$ | `cos3_delta_star` $=\cos(2/3)$ vs `cos3_delta_data` 0.785874 | Their $1.7\times10^{-5}$ gap is the F256 result |
| $\hbar$ | `hbar_SI` (CODATA quote) vs `hbar_SI_from_h` (exact $h/2\pi$) | $6\times10^{-11}$ relative apart |
| $G$ | `G_LATTICE` $1/(72\pi)$ vs `G_CODATA` | Prediction vs comparison target |
| $M(0)$ | `M0_constituent_MeV` 311.2, `_lattice` 1.50, `_GeV` $1.5\Lambda_\text{NJL}/\pi$ | One physics in three units, 0.03 % rounding gap left visible |
| $\approx0.733$ | `e_saturation` 0.733 vs `q_star_a_implied` 0.7327 (plus coincidence records #7, #12, #13) | Different sectors; they collide only through the 5e-3 tolerance |
| $\approx0.243$ | `lambda_6` vs $2\zeta(3)/\pi^2=0.24359$ (records #10, #15) | Arithmetic collision |
| $M_N$ | `M_N_isoaveraged_MeV` 938.918 vs `M_n_neutron_MeV` 939.565 | Isospin average vs neutron |
