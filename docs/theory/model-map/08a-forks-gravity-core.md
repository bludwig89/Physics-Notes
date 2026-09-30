# Forks — gravity core (GR-3 trichotomy, tetrad Dirac, induced-G chain, dielectric K)

Scope: the package `__init__` files for `engine/forks/` and `engine/forks/gravity/`, plus the 21 "core" gravity forks — the GR-3 A/B/C/baseline trichotomy and its harnesses (F16, now deprecated), Fork E (tensor metric) and its stub, the F46→F50→F52→F55 tetrad-Dirac / rest-leg line, the F56→F61/F63/F79 induced-Newton-constant chain, the F62 dynamical Dirac-gravity fork, and the F64 EM-connection (dielectric $K$) fork. The later gravity forks (F164–F248) are in 08b.

**Shared conventions.**
- **Forks are the falsification record, not dead code.** Every module here has registry `sector=forks`, `role=fork`, `origin=manifest`, `exactness=None` → all equations default to `unknown` unless `docs/status/exactness-inventory.md` names the specific result. Registry `findings` is empty for most of them even where the docstring names a finding; the finding named in the header is from the docstring/test, not from the registry.
- **Metric convention** (all forks): static diagonal $ds^2=-A\,c_0^2dt^2+B\,\delta_{ij}dx^idx^j$, so $g_{00}=-A$, $g_{ii}=B$. Weak-field potential $\phi<0$ in a well; $u\equiv-\phi/c_0^2=GM/(rc_0^2)\ge0$. Linearised GR (isotropic Schwarzschild) is $A=1+2\phi/c^2=1-2u$, $B=1-2\phi/c^2=1+2u$.
- **Canonical status (for orientation).** The canonical law is the induced Einstein equation (F178); its vacuum/weak-field representation is the single impedance-matched dielectric $K=e^{2u}$, $A=1/K$, $B=K$, $AB\equiv1$ (F64; CLAUDE.md decision 4). Supersession records that touch this batch: **S3-F64-dielectric-gravity** (supersedes F50/F52/F55/F62 rest-mass sourcing, partially), **S4-F178-full-stress-energy** (reclassifies F64 as vacuum representation; supersedes F114), **S16-F16-gr3-fork-space-closed** (A/B/C trichotomy and all its GR-4 numbers superseded by F64+F178), **S10-F271** (flags a defect in `lattice.curved._half_step_dH` that affects every F64-fork variable-c result), **S25** (F193 Part A exclusion — touches F59 Part C's ½-per-mode).
- **Lattice.** Most forks are **not BCC**: the Dirac steppers are the 2D square exact-QCA walk (Paper-1 Eq. 16/23, $c_i=\cos(k_i/\sqrt2)$, $c_\text{lat}=1/\sqrt2$) — a D1 reference lattice, not canonical. The GR-3 harnesses use a 3D simple-cubic open-BC Poisson potential. The induced-G forks (F56/F57/F59/F61) integrate the canonical BCC dispersion $\omega^+(\mathbf k)=\arccos u^+(\mathbf k)$ (chiral '+' branch, see 03-lattice.md § bcc.py) or a linear control $\omega=c\lvert k\rvert$.
- **Law.** No gauge propagator (even/chiral F91) is used anywhere in 08a except where noted in F64; Dirac steppers use the Weyl walk.
- **Units.** Lattice units throughout ($a=\tau=1$, $c_0$ a free parameter, typically 0.4–0.5 — not $c_\text{lat}$), except F79 S6 / F63 which convert to SI through CODATA anchors.

Modules covered: `forks/__init__.py`, `forks/gravity/__init__.py`, `dirac_gravity_fork.py`, `gr3_fork_A_phase_tick.py`, `gr3_fork_B_anisotropic.py`, `gr3_fork_C_restricted_c.py`, `gr3_fork_baseline.py`, `gr3_fork_harness.py`, `gr3_forks_AB_extended.py`, `gr_fork_E_tensor.py`, `gr_fork_F46_dirac.py`, `gr_fork_F52_restleg_backreaction.py`, `gr_fork_F55_spatial_metric_backreaction.py`, `gr_fork_F56_einstein_coupling_derivation.py`, `gr_fork_F57_induced_eh_from_backreaction.py`, `gr_fork_F58_clockrate_coupling_derivation.py`, `gr_fork_F59_induced_eh_prefactor.py`, `gr_fork_F60_channel_reconciliation.py`, `gr_fork_F61_weyl_eta_gstar.py`, `gr_fork_F63_spin_torsion_estimate.py`, `gr_fork_F64_em_connection.py`, `gr_fork_F79_structural_G.py`, `gr_tensor_stub.py`.

---

### `engine/forks/__init__.py` — forks package marker
**Status:** fork_unclaimed · unreferenced · **Findings:** — · **Lattice:** n/a · **Law:** n/a · **Units:** n/a

Plumbing: docstring only (the GR-3 fork interface description `c_photon / c_matter / tau_rate`, copied from the legacy GR-3 directory). No code. **Flags:** the package docstring describes only the GR-3 gravity trichotomy although the package now holds six sectors of forks (stale, OTHER).

### `engine/forks/gravity/__init__.py` — gravity-fork subpackage marker
**Status:** (not in registry dump as a separate row) · **Lattice/Law/Units:** n/a

Plumbing: docstring only, states forks are recorded alternatives and that status lives in the manifest/registry. **Flags:** no registry row for `forks/gravity/__init__.py` (UNREGISTERED — likely deliberate for `__init__`s, but `forks/__init__.py` has one).

---

### `engine/forks/gravity/dirac_gravity_fork.py` — F62 dynamical Dirac CA on a curved background + D3a backreaction
**Status:** fork_live · test-only · **Findings:** (registry none; docstring/test F62, builds on F46/F50/F52) · **Lattice:** 2D square exact-QCA (D1 reference) · **Law:** n/a (Weyl walk, not a gauge propagator) · **Units:** lattice
**Supersession:** partially SUPERSEDED by F64 (S3-F64-dielectric-gravity): D3a self-sourcing from rest-mass $\rho=\lvert\Psi\rvert^2$ is dead; D1 flat-Weyl regression, D2a Rindler sign convention (cited by production `interactions.gravity.lapse_mix_half`), D2b $\sqrt A$ redshift and D2c eikonal $K\approx4$ are live. Baseline `test-results/F62_dirac_gravity_fork.json` is `stale_by_design`.

**Does:** evolves a 4-component Weyl-pair Dirac field $(\eta_\uparrow,\eta_\downarrow,\chi_\uparrow,\chi_\downarrow)$ on a fixed or self-sourced static metric $(A,B)$ by a Strang split rest-leg-mix ∘ kinetic ∘ rest-leg-mix, and measures free fall, redshift, deflection and self-redshift.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $s(x)=\sqrt{\lvert A\rvert}$ | lapse (rest-leg clock factor) | `dirac_gravity_fork.py:L81 lapse()` | unknown |
| 2 | $c_\text{eff}=c_0\sqrt{\lvert A\rvert/\lvert B\rvert}$ | kinetic-leg speed | `:L86 c_eff_from_AB()` | unknown |
| 3 | $A=(1+a\xi)^2,\ B=1$, $\xi=x-x_0$ | Rindler background | `:L102–104 rindler_background()` | unknown |
| 4 | $\phi=-GM/\sqrt{r^2+r_\text{soft}^2}$; $A=1+2\phi/c_0^2$, $B=1-2\phi/c_0^2$ | softened linearised isotropic Schwarzschild (2D) | `:L123–125 schwarzschild_weak_background()` | unknown |
| 5 | $A=1+2\Phi/c_0^2,\ B=1-2\Phi/c_0^2$ | weak-field map $\Phi\to(A,B)$ | `:L135–136 AB_from_phi()` | unknown |
| 6 | $M(x)=\sqrt A\,m$, $m_0=\langle M\rangle$, $\delta m=M-m_0$; tick $=\text{Mix}(\theta)\circ U_\text{QCA}(m_0,dt)\circ\text{Mix}(\theta)$ with $\theta=-\delta m\,dt/2$ | massive Strang tick (mass inside exact-QCA kinetic, gradient in mix) | `:L175–184 gravity_dirac_step_massive()` | unknown |
| 7 | $\text{Mix}(\theta):\ \eta'=\cos\theta\,\eta-i\sin\theta\,\chi,\ \chi'=\cos\theta\,\chi-i\sin\theta\,\eta$ | per-cell $\eta\leftrightarrow\chi$ unitary (helper, `particles/dirac.py:L440 _mix_eta_chi`) | `particles/dirac.py:L447–450` | unknown |
| 8 | $\theta_{1/2}(x)=\sqrt{A(x)}\,m\,dt/2$; tick $=\text{Mix}(\theta_{1/2})\circ K\circ\text{Mix}(\theta_{1/2})$, $K$ = massless Weyl kinetic step on each chirality (Cayley variable-$c$ CN solver on $c_\text{eff}(x)$, or exact-QCA walk with rate $dt_\text{eff}=r_\text{kin}\,dt$) | curved-background Strang tick | `:L212–234 gravity_dirac_step()` | unknown |
| 9 | $c_\text{lat}^2=\tfrac12$ (2D exact-QCA, $c_\text{lat}=1/\sqrt2$) | Rindler fall prediction scale | `:L188 C_LAT_SQ` | unknown |
| 10 | $\ddot\xi\to-a\,c_\text{lat}^2$ ; $g_\text{meas}=-2\times$(quadratic coeff of early-window $\xi(t)$ fit) | D2a equivalence principle | `:L394 g_pred`, `:L414 g_meas` in `test_rindler_freefall()` | unknown (inferred: quantitative (20 % gate, universality < 12 %)) |
| 11 | $f_\text{near}/f_\text{far}\to\arcsin(\sqrt{A_n}m)/\arcsin(\sqrt{A_f}m)$ (code's reference), also $\sqrt{A_n/A_f}$ | D2b redshift of zitterbewegung frequency from chirality-imbalance FFT peak | `:L472,475–477 test_dynamical_redshift()` | unknown (inferred: quantitative (3 %)) |
| 12 | $\Delta\theta_\text{eik}=-\sum_x\partial_y\ln c_\text{eff}$ (central diff); $K=\Delta\theta\,b\,c_0^2/GM$ | D2c eikonal line integral vs centroid bend | `:L540–544 test_schwarzschild_deflection()` | unknown (inferred: quantitative ($3<\lvert K_\text{eik}\rvert<5$, ratio 25 %)) |
| 13 | $\hat\Phi(\mathbf k)=-4\pi G\,\widehat{(\rho-\bar\rho)}/k^2$, continuum $k^2$ symbol, zero mode 0 | 2D periodic Poisson (log Green fn) | `:L575–584 poisson_2d_fft()` | unknown |
| 14 | loop: $\rho=\lvert\Psi\rvert^2(+w\rho_s)\to\Phi\to(A,B)\to c_\text{eff}\to$ tick (refresh every $n$) | D3a co-evolution | `:L603–614 run_backreaction()` | machine (norm drift, inventory #58: $2.5\times10^{-15}$/60 ticks) |
| 15 | $\rho=\sum\lvert\psi_i\rvert^2$; $(\rho_\eta-\rho_\chi)/\rho$ | density, clock signal | `:L273, L294` | n/a (observable) |
| 16 | flat $m=0$, $A=B=1$, qca engine ⇒ tick $\equiv$ two exact Weyl walks | D1 regression | `:L337–346 test_d1_flat_weyl_regression()` | unknown (inferred: exact (bit-for-bit, gate $10^{-12}$)) |

**Inputs → outputs:** Weyl 4-spinor fields $(L_x,L_y)$ complex, $A$, $c_\text{eff}$ or $\phi$/$\rho$, $m\le1$ → evolved spinor, pass dicts. **Depends on:** `particles/dirac.py` (`_mix_eta_chi`, `_weyl_half_step_2c`, `dirac_step_2d_splitstep`, `_dirac_plus_eigenvector`; see 06b), `lattice/curved.CayleyVarcSolver2D` (03-lattice.md), `casim.numerics.fft` (02).
**Flags:**
- ⚠ DOC/CODE MISMATCH (rest-leg rate): docstrings (L29, L446–448, L657) state the rest leg as $\sqrt A\cdot m$ in the Hamiltonian but the reference frequency as $2\arcsin(\sqrt A m)$; the stepper (#8) applies total mix angle $\sqrt A\,m\,dt$ per tick with a *massless* kinetic step, so the $k=0$ rotation is $\sqrt A\,m$ per tick — spot-checked: $A=0.81,m=0.5$ gives $0.4500$ vs $\sqrt A\arcsin m=0.4712$, $\arcsin(\sqrt A m)=0.4668$. The D2b/D3a tests pass only because the near/far *ratio* differs by ~1 % at their parameters.
- OTHER: two sign conventions coexist in one file — #6 uses $\theta=-\delta m\,dt/2$ (matching exact-QCA $+im_0$), #8 uses $\theta=+\sqrt A m\,dt/2$; the docstring (L160–168) explains #6's sign and says `dirac_step_2d_varm_splitstep` has the wrong relative sign (a live, not-superseded item per S3).
- OTHER: `C_LAT_SQ = 0.5` literal (2D walk's $c_\text{lat}^2$), not the registered BCC $c_\text{lat}=1/\sqrt3$ — correct for this lattice but unregistered.
- OTHER: `np.fft.fftfreq` used directly (allowed by D8), all transforms via `casim.numerics.fft`; complex spinor arithmetic is explicit, no real-cast hazard found.
- EXACTNESS unknown: #1–9, #13.

---

### `engine/forks/gravity/gr3_fork_A_phase_tick.py` — GR-3 Fork A (separate phase-tick clock)
**Status:** fork_unclaimed · unreferenced · **Findings:** (docstring "Finding 14.5(a)" = F16) · **Lattice:** n/a (pointwise maps on a potential array) · **Law:** n/a · **Units:** lattice
**SUPERSEDED by F64, F178** (S16-F16-gr3-fork-space-closed); Fork A explicitly retired by Fork E's docstring (`gr_fork_E_tensor.py:L43–44`).

**Does:** keeps the Paper-6 single-scalar refractive speed for propagation but reads the clock from a separate linear field.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c_\gamma=c_m=c_0/(1-2\phi/c_0^2)$ | Paper-6 propagation speed | `gr3_fork_A_phase_tick.py:L43, L49` | unknown |
| 2 | $\tau=1+\phi/c_0^2$ | hand-set clock rate (factor 1) | `:L59 tau_rate()` | unknown |
| 3 | $A=1+2\phi/c_0^2,\ B=1-2\phi/c_0^2$ | metric for GR-4 | `:L72–74 metric()` | unknown |

**Inputs → outputs:** $\phi$ array, $c_0$ → arrays. **Depends on:** nothing. **Flags:** SUPERSEDED; `metric()` is the same linearised Schwarzschild pair as every other fork (S16: GR-4 integrates no fork's own metric); EXACTNESS unknown #1–3.

### `engine/forks/gravity/gr3_fork_B_anisotropic.py` — GR-3 Fork B (anisotropic $(A,B)$)
**Status:** fork_unclaimed · unreferenced · **Findings:** (F16) · **Lattice:** n/a · **Law:** n/a · **Units:** lattice
**SUPERSEDED by F64, F178** (S16) — but S16 records that the canonical $A=e^{-2u},B=e^{2u}$ linearises to **exactly and only Fork B**, so Fork B's content survives as the O(u) limit.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A=1+2\phi/c_0^2,\ B=1-2\phi/c_0^2$ | linearised isotropic Schwarzschild | `gr3_fork_B_anisotropic.py:L45–47 _AB()` | unknown |
| 2 | $c_\gamma=c_m=c_0\sqrt{\lvert A\rvert/B}$ | photon/matter scalar speed | `:L58, L66` | unknown |
| 3 | $\tau=\sqrt{\lvert A\rvert}$ | clock rate | `:L75 tau_rate()` | unknown |

**Flags:** SUPERSEDED (S16); docstring L14 "$c_\gamma\approx c_0(1+2\phi/c_0^2)$" — for $\phi<0$ this is $<c_0$, consistent; EXACTNESS unknown #1–3.

### `engine/forks/gravity/gr3_fork_C_restricted_c.py` — GR-3 Fork C (sector-dependent coupling)
**Status:** fork_unclaimed · unreferenced · **Findings:** (F16) · **Lattice:** n/a · **Law:** n/a · **Units:** lattice
**SUPERSEDED by F64, F178** (S16); S16 also records Fork C's `tau_rate` and `metric` as mutually inconsistent.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c_\gamma=c_0/(1-2\phi/c_0^2)$ | photon coupling 2 | `gr3_fork_C_restricted_c.py:L47` | unknown |
| 2 | $c_m=c_0/(1-\phi/c_0^2)$ | matter coupling 1 | `:L51` | unknown |
| 3 | $\tau=c_m/c_0=1/(1-\phi/c_0^2)$ | clock | `:L56` | unknown |
| 4 | $A=1+\phi/c_0^2,\ B=1-\phi/c_0^2$ | halved matter metric | `:L71–73 metric()` | unknown |

**Flags:** SUPERSEDED; OTHER: $\tau$ (#3, from $c_m$) and $\sqrt A$ from #4 agree only at O(φ) — the inconsistency S16 names; EXACTNESS unknown.

### `engine/forks/gravity/gr3_fork_baseline.py` — Paper-6 isotropic-$c$ baseline
**Status:** fork_unclaimed · unreferenced · **Findings:** (F16 / "Finding 14.5") · **Lattice:** n/a · **Law:** n/a · **Units:** lattice
**SUPERSEDED** (S16; the ansatz $c=c_0/(1-2\phi/c_0^2)$ is the linearisation family F64/F178 exclude, cf. S17).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $c_\gamma=c_m=c_0/(1-2\phi/c_0^2)$ | single-scalar speed | `gr3_fork_baseline.py:L27, L32` | unknown |
| 2 | $\tau=c/c_0=1/(1-2\phi/c_0^2)$ | clock ⇒ factor-2 Pound–Rebka | `:L37 tau_rate()` | unknown |
| 3 | $A=1+2\phi/c_0^2,\ B=1-2\phi/c_0^2$ | GR-4 metric (not the baseline's own) | `:L52–54 metric()` | unknown |

**Flags:** SUPERSEDED; ⚠ DOC/CODE MISMATCH: docstring L44 describes the baseline's own metric as $A=B=(1-2\phi/c_0^2)^{-2}$, but `metric()` returns the isotropic-Schwarzschild pair (#3) — the docstring then admits the substitution (L49–50); EXACTNESS unknown.

### `engine/forks/gravity/gr3_fork_harness.py` — GR-1…GR-4 cross-fork harness
**Status:** fork_unclaimed · unreferenced · **Findings:** (F16) · **Lattice:** 3D simple-cubic periodic-index slice of an open-BC Poisson potential (reference) · **Law:** n/a · **Units:** lattice
**SUPERSEDED by F64, F178** (S16): retained "as the falsification record, NOT as a working GR-4 instrument. FC01 is the correct instrument." Artifact `test-results/gr3_fork_comparison.json` is `stale_by_design`.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Delta\theta=-\sum_x\tfrac12[\ln c_\gamma(y{+}1)-\ln c_\gamma(y{-}1)]$ at $y=L/2+b$, $z=L/2$; $K=\Delta\theta\,b\,c_0^2/(G_NM)$ | GR-1 eikonal deflection coefficient | `gr3_fork_harness.py:L68–72 gr1_K()` | quantitative (inventory row 23 family) |
| 2 | $\Delta t_\text{lat}=\sum 1/c_\gamma-N/c_0$; $\Delta t_\text{GR}=\tfrac{2G_NM}{c_0^3}\ln\tfrac{r_1+r_2+r_{12}}{r_1+r_2-r_{12}}$ | GR-2 Shapiro ratio | `:L90–103 gr2_ratio()` | unknown (inferred: quantitative) |
| 3 | $(\Delta\nu/\nu)=\tau_n/\tau_f-1$; $\text{pred}=-(\phi_f-\phi_n)/c_0^2$; ratio | GR-3 Pound–Rebka ratio | `:L134–136 gr3_ratio_GR()` | quantitative (inventory row 23: A 1.0001, B 1.0002, C 0.9998, baseline 1.9991) |
| 4 | $\alpha_A=(A-1)/(2\phi/c^2)$, $\alpha_B=(1-B)/(2\phi/c^2)$ at $\phi=-10^{-6}c^2$ | linearised metric coefficients | `:L184–185 _alpha_AB()` | unknown |
| 5 | $\ddot{\mathbf r}=-\tfrac{GM}{r^2}\hat r+\tfrac{GM}{c^2r^2}\big[2(\alpha_A{+}\alpha_B)\tfrac{GM}{r}\hat r-\alpha_B v^2\hat r+2(\alpha_A{+}\alpha_B)(\hat r\!\cdot\!\mathbf v)\mathbf v\big]$ | hand-written 1PN force law | `:L217–223 accel()` in `gr4_mercury_advance()` | unknown |
| 6 | $\Delta\omega_\text{pred}=(2\alpha_A+2\alpha_B-\alpha_A\alpha_B)\pi GM/(a(1-e^2)c^2)$; $\Delta\omega_\text{GR}=3\pi GM/(a(1-e^2)c^2)$ | closed-form advance and normaliser | `:L202–204` | unknown |
| 7 | velocity-Verlet; perihelion = $r$ minimum; mean wrapped angle difference | GR-4 measurement | `:L232–274` | quantitative (inventory row 24) |

**Inputs → outputs:** open-BC $\phi$ from `gaussian_mass_3d` + `solve_poisson_3d_open` (03-lattice.md § poisson_open) → JSON/MD comparison table (written only under `__main__`). **Flags:**
- SUPERSEDED (S16).
- ⚠ DOC/CODE MISMATCH: comment L173–175 says $3\pi$ is "same as the standard $6\pi$ formula (factor-of-2 … per-half-orbit convention)"; the correct GR per-orbit advance is $6\pi GM/(a(1-e^2)c^2)$, so the normaliser is wrong by 2 (S16 and `gr3_forks_AB_L192.md` say so).
- OTHER: #5 hard-codes Schwarzschild-form PN coefficients driven only by $(\alpha_A,\alpha_B)$ from `metric()`, and every fork's `metric()` returns the same pair except C ⇒ GR-4 does not integrate any fork's own spacetime (S16 NUMERICAL).
- OTHER: velocity-Verlet evaluates `a2 = accel(r, v)` with the *old* $v$ for a velocity-dependent force (L236).
- EXACTNESS unknown: #4–6.

### `engine/forks/gravity/gr3_forks_AB_extended.py` — Forks A & B at $L=192$, 12 orbits
**Status:** fork_unclaimed · unreferenced · **Findings:** (F16) · **Lattice:** 3D SC reference · **Law:** n/a · **Units:** lattice
**SUPERSEDED** (S16).

**Does:** self-contained copy of the harness equations for Forks A and B only. Equations identical to `gr3_fork_harness.py` #1–#7: GR-1 `:L68–74 gr1_K()`, GR-2 `:L81–96 gr2_ratio()`, GR-3 `:L106–111 gr3_ratio_GR()`, $\alpha$ extraction `:L125–129 _alpha_AB()`, 1PN force `:L155–166 accel()`, normaliser $3\pi GM/(a(1-e^2)c^2)$ `:L147`. Exactness: quantitative (measurement) / unknown (closed forms).
**Flags:** SUPERSEDED; OTHER (bug): `gr1_K`/`gr2_ratio`/`gr3_ratio_GR` index with the module-global `L=192`, not the `L_` passed to `run()`, so `--L` other than 192 slices the wrong row; OTHER: output dir `SIM_ROOT/test-results` resolves to `src/casim/engine/forks/test-results` (stale relative path after the C6 move; `__main__`-guarded); docstring L137–141 acknowledges the 3π-vs-6π normaliser (ratio ≈ 2 expected).

---

### `engine/forks/gravity/gr_fork_E_tensor.py` — Fork E, tensor metric (linearised = Fork B; exact isotropic Schwarzschild)
**Status:** fork_live · test-only · **Findings:** (registry none; docstring "Finding 19") · **Lattice:** n/a · **Law:** n/a · **Units:** lattice
**Supersession:** named by S16 as "the successor fork; its docstring is where the closure is stated". The exact-isotropic mode is GR (Schwarzschild in isotropic coordinates), which F178 makes the canonical exact vacuum solution; not itself superseded.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u=\min(-\phi/c_0^2,\ 2(1-10^{-9}))$ | clipped $GM/(rc^2)$ outside isotropic horizon | `gr_fork_E_tensor.py:L86–87 _u_of_phi()` | unknown |
| 2 | $A=1-2u,\ B=1+2u$ | linearised (== Fork B, docstring-derived from $\Box\bar h_{\mu\nu}=-16\pi G T_{\mu\nu}/c^4$ trace reversal) | `:L96–97 _AB_linearized()` | unknown |
| 3 | $A=\big(\tfrac{1-u/2}{1+u/2}\big)^2,\ B=(1+u/2)^4$ | exact isotropic Schwarzschild | `:L108–109 _AB_exact()` | unknown |
| 4 | $c_\gamma=c_m=c_0\sqrt{\lvert A\rvert/B}$, $\tau=\sqrt{\lvert A\rvert}$ | harness interface | `:L130, L137, L141 make_fork()` | unknown |

**Inputs → outputs:** $\phi$, $c_0$, mode → `SimpleNamespace` fork (module default = exact mode). **Flags:** OTHER (stale citation): docstring cites "Finding 19", but `findings/F19` is now the tick area-vs-volume test (`deprecated/findings/F19-tick-area-vs-volume.md`); the tensor-metric content belongs to the F16 era; registry findings empty. EXACTNESS unknown #1–4 (the closed forms are algebraically exact but no registry/inventory row covers them). The $u$-clip is a numerical guard, not physics.

### `engine/forks/gravity/gr_fork_F46_dirac.py` — F46/F50 covariant spherical-triangle (tetrad Dirac, Fork E3)
**Status:** fork_live · test-only · **Findings:** F46 (registry); docstring/test F50 · **Lattice:** 2D square exact-QCA (reference) · **Law:** n/a · **Units:** lattice
**Supersession:** F50 partially SUPERSEDED by F64 (S3): which leg carries redshift *and* rest-mass sourcing are dead; G2 ($\Omega=\sqrt A\arcsin m$, = production `lapse_mix_half`) and G3 ($c_\text{eff}=c_0\sqrt{A/B}$ = dielectric $c/K$ under $A=1/K,B=K$) are live regressions.

**Does:** puts the F46 identity $\cos\Omega=\cos\Omega_\text{rest}\cos\omega_\text{kin}$ on a static curved background with the lapse on the rest leg and $\sqrt{A/B}$ on the kinetic leg; also a prototype Strang stepper.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $(A,B)$ = Fork E metric (default exact isotropic) | background | `gr_fork_F46_dirac.py:L120–121 _AB()` | unknown |
| 2 | $c_\text{eff}=c_0\sqrt{\lvert A\rvert/B}$; $r_\text{kin}=\sqrt{\lvert A\rvert/B}$ | kinetic-leg speed / rate | `:L131 c_eff_matter()`, `:L142 r_kin()` | unknown (inferred: exact (F50-G3: equals Fork-E $c_\gamma$ bit-for-bit)) |
| 3 | $\tau=\sqrt{\lvert A\rvert}$ | clock | `:L157 tau_rate()` | unknown |
| 4 | $\Omega_\text{rest}(x)=\sqrt{A}\arcsin m$ | redshifted rest leg | `:L166 rest_leg()` | unknown (inferred: exact (F50-G2, $1.67\times10^{-16}$)) |
| 5 | $\omega^0_\text{kin}=\arccos(\cos\tfrac{k_x}{\sqrt2}\cos\tfrac{k_y}{\sqrt2})$ (scalar $k$ → diagonal) | flat 2D exact-QCA kinetic leg | `:L182–183 omega_kin_qca_flat()` | unknown (inferred: exact (F46-P1 family)) |
| 6 | $\omega_\text{kin}=r_\text{kin}\,\omega^0_\text{kin}$ (exact_qca) or $c_\text{eff}\lvert k\rvert$ (continuum) | site-dependent kinetic leg | `:L204, L206 kinetic_leg()` | unknown (inferred: exact (F50-G6 at $A=B$: $4.4\times10^{-16}$)) |
| 7 | $\cos\Omega^\text{coord}=\cos\Omega_\text{rest}\cos\omega_\text{kin}$ | covariant F46 identity | `:L221–222 dirac_omega_coord()` | unknown (identity by construction) |
| 8 | $\Omega^2=\Omega_\text{rest}^2+\omega_\text{kin}^2=A(\arcsin m)^2+(A/B)c_0^2k^2$ | continuum reference | `:L233–235 dirac_omega_continuum()` | unknown |
| 9 | $\theta_{1/2}=\sqrt{\lvert A\rvert}\,m\,dt/2$; Mix∘Kinetic∘Mix | prototype stepper (same as `dirac_gravity_fork` #8) | `:L303–325 gravity_dirac_step_2d()` | unknown (inferred: machine (F50-G5 norm drift 0.0, Tier-2)) |

**Depends on:** `gr_fork_E_tensor` (metric), `particles/dirac.py` helpers, `lattice/curved.CayleyVarcSolver2D`.
**Flags:** ⚠ DOC/CODE MISMATCH: the analytic rest leg is $\sqrt A\arcsin m$ (#4) but the stepper (#9) rotates by $\sqrt A\,m$ per tick (block comment L247 says "θ(x)=√A·m·dt"); at $k=0$ the stepper realises $\sqrt A\,m$, not $\sqrt A\arcsin m$ (spot-checked, see dirac_gravity_fork). ⚠ DOC/CODE MISMATCH: docstring L34 Hamiltonian rest term $\sqrt A\,m c_0^2\beta$ vs code's $c_0$-free angle. OTHER: `continuum` form on the kinetic leg takes $\lvert k\rvert$ via `np.sum(kk**2)` (scalar only — arrays of k-vectors collapse to one norm). SUPERSEDED (partial, S3). EXACTNESS unknown #1, #3, #7, #8.

### `engine/forks/gravity/gr_fork_F52_restleg_backreaction.py` — F52 gravity as a self-consistent rest-leg field
**Status:** fork_live · test-only · **Findings:** F52 · **Lattice:** 3D SC (FFT Poisson / 6-neighbour Jacobi) reference · **Law:** n/a · **Units:** lattice
**SUPERSEDED (partially) by F64/F106/F178** (S3): Poisson sourced by rest-mass density (H1/H1b/H2) is dead; H3/H3b factor-2 discriminator ($K=4$ isotropic vs $K=2$ rest-only) is still canonical.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\nabla^2\Phi=4\pi G\rho$ (FFT, continuum $-k^2$ symbol, zero mean) | spectral rest-leg potential (via `interactions.gravity_emqg.solve_poisson_3d`) | `gr_fork_F52_restleg_backreaction.py:L89 restleg_potential_fft()` | unknown |
| 2 | $\Phi^{n+1}=\tfrac16\big(\sum_{6\text{ nbrs}}\Phi^n-4\pi G\rho\big)$, Dirichlet $\Phi=0$ on faces | Jacobi relaxation to the fixed point | `:L103, L109–116 relax_restleg_potential()` | unknown (inferred: quantitative (tol $10^{-8}$)) |
| 3 | $s=\sqrt{\lvert A(\Phi)\rvert}$ (Fork E metric); $\Omega_\text{rest}=s\arcsin m$ | clock field, rest leg | `:L134, L139` | unknown |
| 4 | rest-only: $c_\text{eff}=c_0\sqrt A$, $n=1/\sqrt A$; full: $n=\sqrt{B/A}$ | refractive index per sector | `:L153–159 refractive_index()` | unknown |
| 5 | $\alpha=-\sum_\text{line}\partial_\perp n$ (`np.gradient`); for $n-1=\kappa u$, $K=2\kappa$ | eikonal deflection (H3) | `:L177, L191 eikonal_deflection()` | unknown |

**Flags:** SUPERSEDED (partial). Posited coupling $4\pi G$ is stated as input (docstring L51). EXACTNESS unknown #1, #3–5.

### `engine/forks/gravity/gr_fork_F55_spatial_metric_backreaction.py` — F55 spatial metric from trace reversal
**Status:** fork_live · test-only · **Findings:** F55 · **Lattice:** 3D SC reference (via F52 Poisson) · **Law:** n/a · **Units:** lattice
**SUPERSEDED (partially) by F64** (S3): the trace-reversal route to factor-2 *from rest mass* is dead; J1 (trace-reversal identity) and J3 (factor-2 deflection) live; $K=(1-u)^{-2}$ survives only as the excluded β=½ control.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\bar h_{00}=-4\phi/c_0^2$, $\bar h=-\bar h_{00}$, $h_{00}=\bar h_{00}+\tfrac12\bar h=-2\phi/c_0^2$, $h_{ij}=-\tfrac12\bar h=-2\phi/c_0^2$ | static-dust trace reversal ($\eta=\text{diag}(-1,1,1,1)$) | `gr_fork_F55_spatial_metric_backreaction.py:L107–111 trace_reversed_perturbation()` | unknown (algebraic identity) |
| 2 | $A=1-h_{00}=1+2\phi/c_0^2$, $B=1+h_{ij}=1-2\phi/c_0^2$ | metric from trace reversal | `:L123–124 metric_trace_reversed()` | unknown |
| 3 | $B_\lambda=1+\lambda(B-1)$, $K(\lambda)=2(1+\lambda)$ | uniqueness knob | `:L137–138 metric_spatial_fraction()` | unknown |
| 4 | $n=\sqrt{B/\lvert A\rvert}$; $\alpha=-\sum\partial_\perp n$ | eikonal deflection | `:L150, L174` | unknown |

**Flags:** ⚠ DOC/CODE MISMATCH (cosmetic): docstring of `metric_trace_reversed` (L117) contains an unfinished "A = 1 + h₀₀ ... wait:" line before the correct derivation; code is consistent. Note $A=1-h_{00}$ uses $g_{00}=-1+h_{00}$ with $h_{00}=-2\phi/c^2$ — sign-consistent. SUPERSEDED (partial). EXACTNESS unknown #1–4.

### `engine/forks/gravity/gr_fork_F56_einstein_coupling_derivation.py` — F56 16πG/c⁴ factorisation attempt
**Status:** fork_live · test-only · **Findings:** F56 · **Lattice:** SC Green's function (reference) + BCC dispersion ('+' branch) · **Law:** chiral '+' Weyl branch (dispersion only) · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\xi=4\,c_N\,G/c^4$ ($c_N=4\pi\Rightarrow\xi=16\pi G/c^4$); Einstein-tensor coupling $\xi/2=8\pi G/c^4$ | Part A: tensor coupling forced by Newton + $\bar h_{00}=2h_{00}$ | `gr_fork_F56_einstein_coupling_derivation.py:L78–79 derive_tensor_coupling()` | unknown (algebraic) |
| 2 | $\hat G(\mathbf k)=\hat\delta/\hat\Delta$, $\hat\Delta=-4\sum_i\sin^2(k_i/2)$, zero mode removed | bare SC lattice Green's function | `:L99, L104–106 lattice_green_function_sc()` | unknown |
| 3 | fit $G(r)\approx-C/r+a+br^2$; report $4\pi C$ (→1) | far-field solid angle | `:L120–125 fit_green_far_field_coefficient()` | unknown (inferred: quantitative (fit)) |
| 4 | $c_\text{lat}=d\omega^+/d\lvert k\rvert$ (linear fit, $k\le3\times10^{-4}$) | BCC light-cone slope (expect $1/\sqrt3$, F26) | `:L136–137 lightcone_slope()` | unknown (inferred: quantitative) |
| 5 | $I(\Lambda)=\int_{\lvert k\rvert<\Lambda}\tfrac{d^3k}{(2\pi)^3}\,\tfrac1{\omega^+(k)}$ (cube Riemann sum); continuum $\Lambda^2/(4\pi^2c_\text{lat})$ | Sakharov weight | `:L151–159 induced_inverse_G_integral()` | unknown (inferred: quantitative) |
| 6 | fit $p$ in $I\propto\Lambda^p$ (expect 2) | $G\propto\ell^2$ scaling | `:L166 sakharov_scaling()` | unknown (inferred: quantitative) |

**Flags:** OTHER: docstring's "PART B/PART C" labels are swapped relative to the code sections (docstring's Part B = G scaling says "(PART C test)"). OTHER: #5 integrates $1/\omega$, whereas F59/F60 use $1/(2\omega)$ — factor-2 convention differs across the chain (both "continuum" formulas are internally consistent: $\Lambda^2/(4\pi^2c)$ vs $\Lambda^2/(8\pi^2c)$). EXACTNESS unknown #1, #2.

### `engine/forks/gravity/gr_fork_F57_induced_eh_from_backreaction.py` — F57 density-channel polarization Π(q)
**Status:** fork_live · test-only · **Findings:** F57 · **Lattice:** BCC ('+' branch dispersion) · **Law:** chiral '+' branch · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Pi(\mathbf q)=\int\tfrac{d^3k}{(2\pi)^3}\,\tfrac1{\omega(\mathbf k)+\omega(\mathbf k+\mathbf q)}$ (midpoint cube grid $[-\Lambda,\Lambda)^3$, optional sphere) | static density polarization | `gr_fork_F57_induced_eh_from_backreaction.py:L92–102 static_polarization()` | unknown (inferred: quantitative) |
| 2 | fit $\Pi(q)=\Pi_0-\Pi_2q^2$ | EH kinetic coefficient $\Pi_2$ | `:L118–121 polarization_gradient_coefficient()` | unknown (inferred: quantitative (fit)) |
| 3 | exponents of $\Pi(0;\Lambda)$ (expect 2) and $\Pi_2(\Lambda)$ (expect ≪2, log) | cutoff scaling of the two sectors | `:L143–145 cutoff_scaling()` | unknown (inferred: quantitative) |

**Flags:** OTHER: the "full BZ" is the cube $[-\pi,\pi)^3$ in Cartesian $k$ ("BZ proxy", L90), not the BCC Brillouin zone — the integrand is periodic in the BCC reciprocal lattice with scale $\sqrt3$ (arguments $k/\sqrt3$ in `_bcc_uvec`), so the domain choice is a cutoff, not the true zone. EXACTNESS: none unknown (all numerical fits → quantitative by the brief's rule).

### `engine/forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py` — F58 does 4πG follow from the neighbour rule?
**Status:** fork_live · test-only · **Findings:** F58 · **Lattice:** SC 6-neighbour symbol (reference) + BCC dispersion · **Law:** chiral '+' (dispersion only) · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\Omega_\text{rest}=\sqrt A\arcsin m$ | rest-leg clock rate | `gr_fork_F58_clockrate_coupling_derivation.py:L75 restleg_rate()` | machine (inventory #56 Q0) |
| 2 | $\delta=1-\Omega(m,A)/\Omega(m,1)=1-\sqrt A$, spread over $m$ | Q0 weak-equivalence universality | `:L88–89 universality_residual()` | unknown (inferred: machine (#56: $2.2\times10^{-16}$)) |
| 3 | $J\hat\Delta\,\hat\Phi=\hat\delta$, $\hat\Delta=-4J\sum\sin^2(k_i/2)$ | Q1 clock-rate Green's fn (no 4π) | `:L112, L117–119 clockrate_green_function()` | unknown |
| 4 | fit $\Phi\approx-C/r+a+br^2$ | far-field coefficient | `:L132–136 fit_far_field()` | unknown (inferred: quantitative) |
| 5 | $S=\partial_{k^2}[4J\sum\sin^2(k_iv_i/2)]$ per direction; anisotropy spread | Q2 Laplacian form forced | `:L153–160 neighbour_symbol_small_k()` | unknown (inferred: quantitative) |
| 6 | $c_\text{lat}=\sqrt S$; $S/c_\text{lat}^2$ over $J$ | Q3a "stiffness–light-cone lock" | `:L177–178 clat_from_symbol()`, `:L191–197 stiffness_clat_lock()` | unknown (inferred: machine (#57: $1.1\times10^{-16}$)) |
| 7 | $c_\text{lat}=d\omega^+/d\lvert k\rvert$ along (111) | measured BCC $c_\text{lat}$ (→$1/\sqrt3$) | `:L205–206 measured_clat_bcc()` | unknown (inferred: quantitative) |
| 8 | $I(\Lambda)=\int_{\lvert k\rvert<\Lambda}\tfrac{d^3k}{(2\pi)^3}\omega^{-1}$; exponent fit | Q3b Sakharov | `:L218–225, L232` | unknown (inferred: quantitative) |

**Flags:**
- ⚠ DOC/CODE MISMATCH: docstrings (L165–167, L182–183) say "$c_\text{lat}\propto J$ and stiffness $\propto J^2$"; the code's symbol is linear in $J$, so $S\propto J$ and $c_\text{lat}=\sqrt S\propto\sqrt J$.
- OTHER (circular test): #6 defines $c_\text{lat}\equiv\sqrt S$, so $S/c_\text{lat}^2=1$ identically for any operator — inventory #57's "hopping-independent" result is a tautology of the definition (F60 re-reads it as the tree-level kinematic identity).
- ⚠ DOC/CODE MISMATCH: `restleg_rate` docstring (L74) says $A=1-2\Phi/c^2$; the rest of the chain (and this file's own L93 comment) uses $A=1+2\Phi/c^2$.
- ⚠ DOC/CODE MISMATCH (algebra in prose): docstring/DESCRIPTION "1/G ∝ c_lat² ∝ √d" — with $c_\text{lat}=1/\sqrt d$, $c_\text{lat}^2=1/d$ (F60 L3 states $1/d$ correctly).
- EXACTNESS unknown: #3.

### `engine/forks/gravity/gr_fork_F59_induced_eh_prefactor.py` — F59 induced-EH prefactor, spatial-stress channel
**Status:** fork_unclaimed · unreferenced · **Findings:** F59 · **Lattice:** BCC '+' branch (local mirror of `bcc_dispersion`) + linear control · **Law:** chiral '+' (dispersion) · **Units:** lattice → Planck (assembly)
**Supersession:** S25 notes F59 Part C builds $1/16\pi G$ from the ½-per-mode zero-point term that F193 Part A tried to delete (deletion excluded, so F59 stands).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $u^+=c_xc_yc_z+s_xs_ys_z$, $c_i=\cos(k_i c_\text{lat})$, $\omega=\arccos u^+$, $c_\text{lat}=1/\sqrt3$ (F26, registry `c_lat`) | local BCC dispersion copy | `gr_fork_F59_induced_eh_prefactor.py:L37–43 bcc_u(), bcc_omega()` | unknown (closed form identical to `lattice/bcc.py`) |
| 2 | $v_i=\partial\omega/\partial k_i$ (central diff, $h=10^{-5}$) | group velocity | `:L46–50 bcc_velocity()` | unknown (inferred: quantitative) |
| 3 | $\int\tfrac{d^3k}{(2\pi)^3}\tfrac1{2\omega}$ (Newton sector, $\sim\Lambda^2$); $\int\tfrac{d^3k}{(2\pi)^3}\tfrac{\omega}2$ (CC sector, $\sim\Lambda^4$) | two Sakharov sectors | `:L77–78 sector_invw()`, `:L86 sector_w()` | unknown (inferred: quantitative) |
| 4 | $I\cdot c$ constant for $\omega=c\lvert k\rvert$ | $1/c_\text{lat}=\sqrt d$ factor | `:L103–104 sqrt_d_factor()` | unknown (inferred: quantitative) |
| 5 | $\Pi_{xy,xy}(q\hat z)=\int\tfrac{d^3k}{(2\pi)^3}\tfrac{\bar V^2}{\omega(k)+\omega(k+q)}$, $\bar V=\tfrac12(T_{xy}(k)+T_{xy}(k+q))$, $T_{xy}=\tfrac12(k_xv_y+k_yv_x)$ | TT spatial-stress bubble | `:L119–124 stress_bubble_xyxy()` | unknown (inferred: quantitative) |
| 6 | fit $\Pi=P_0+Cq^2$ ; exponent of $C(\Lambda)$ | $C$ = "induced $1/16\pi G$" (negative control: not $\Lambda^2$) | `:L130–132 C_eh()`, `:L145 scaling()` | unknown (inferred: quantitative) |
| 7 | $P_\text{pre}=\sqrt{2\pi\eta g_*}$; $a/\ell_P=P_\text{pre}d^{1/4}$; $\tau/t_P=P_\text{pre}d^{-1/4}$; $\sqrt{a\,c\tau}/\ell_P=P_\text{pre}$ (with $a/\tau=c\sqrt d$) | assembly (placeholder $\eta=1/12$, $g_*=2$) | `:L170–177 assemble()` | unknown |

**Flags:** OTHER: `__main__` writes `f59_results.json` *into the source directory* (`OUT = dirname(__file__)`); guarded, but not the `_results_path` pattern. OTHER: the docstring's step (3) promises that $C$ from the stress bubble is the induced $1/(16\pi G)$, but `__main__` step [4] labels it a "NEGATIVE control: UV-dominated … BZ-edge junk" — the assembly (#7) does not use $C$ at all (docstring L166–168 says $P_\text{pre}$ is independent of the BZ integral). EXACTNESS unknown: #1, #7.

### `engine/forks/gravity/gr_fork_F60_channel_reconciliation.py` — F60 tree vs loop induced-G channel
**Status:** fork_unclaimed · unreferenced · **Findings:** F60 · **Lattice:** SC symbol + linear dispersion · **Law:** n/a · **Units:** lattice

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $S_\text{bare}=\partial_{k^2}[4J\sum\sin^2(k_iv_i/2)]$, $c_\text{lat}=\sqrt{S}$ | tree stiffness (identity $S=c_\text{lat}^2$) | `gr_fork_F60_channel_reconciliation.py:L45–47 bare_stiffness_and_clat()` | unknown (inferred: quantitative) |
| 2 | $B(c)=\int_{\lvert k\rvert<\Lambda}\tfrac{d^3k}{(2\pi)^3}\tfrac1{2c\lvert k\rvert}$; analytic $\Lambda^2/(8\pi^2c)$ | induced loop stiffness | `:L54–60 induced_stiffness()` | unknown (inferred: quantitative) |
| 3 | $B/S_\text{bare}\propto c^{-3}$ (at $J=c^2$) | tree-vs-loop gap | `__main__` `:L96–103` | unknown (inferred: quantitative) |
| 4 | induced $a/\ell_P=\sqrt{2\pi\eta g_*}d^{1/4}$ vs bare $\propto d^{-1/4}$ | selection argument | `__main__` `:L111–117` | unknown |

**Flags:** OTHER: all physics results live in `__main__` (no callable for #3/#4); writes `f60_results.json` into the source dir. OTHER: #1 is circular by construction (same as F58 #6). Registry `c_lat` site is `kind="import"` with name None; the value appears in a deliberate $c$-scan. EXACTNESS unknown: #4.

### `engine/forks/gravity/gr_fork_F61_weyl_eta_gstar.py` — F61 Weyl heat-kernel η and mode count $g_*$
**Status:** fork_unclaimed · unreferenced · **Findings:** F61 · **Lattice:** BCC (eigenphase check) · **Law:** chiral (`bcc_unitary` '+' branch) · **Units:** lattice → Planck

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $a_1/R=\tfrac16\operatorname{tr}1-\operatorname{tr}(E/R)$ | Seeley–DeWitt $a_1$ for $-\Box+E$ | `gr_fork_F61_weyl_eta_gstar.py:L50 a1_over_R()` | unknown (exact Fraction arithmetic; no inventory row) |
| 2 | scalar: $c=\tfrac16,\eta=\tfrac1{12}$; Dirac ($\operatorname{tr}1=4$, $E=R/4$ Lichnerowicz, fermion sign −): $a_1/R=-\tfrac13$, $c=\tfrac13$; Weyl $c=\tfrac16$, $\eta_\text{Weyl}=\tfrac1{12}$ | η table | `:L55–62 heat_kernel_table()` | unknown (Fraction, asserted L129; value $\eta_\text{Weyl}=1/12$ is inventory #165 via F79) |
| 3 | $\max\big\lvert\,\lvert\arg\lambda_1\rvert-\lvert\arg\lambda_2\rvert\,\big\rvert$ over $U_\text{BCC}(\mathbf k)$ | both Weyl components share $\lvert\omega\rvert$ | `:L83–86 eigenphase_symmetry()` | unknown (inferred: machine) |
| 4 | $\int_{\lvert k\rvert<0.8\pi}\tfrac{d^3k}{(2\pi)^3}\tfrac1{2\omega^+}$ | per-component BCC phase-space number | `:L92` | unknown (inferred: quantitative) |
| 5 | $g_*$: per generation $2+1+6+3+3=15$, $+\nu_R=16$, three generations $48$ | gravitating Weyl count | `:L100–111 gstar_table()` | unknown (integer count) |
| 6 | $P_\text{pre}=\sqrt{2\pi\eta g_*}$, $a/\ell_P=P_\text{pre}3^{1/4}$ ($g_*=48$: $\sqrt{8\pi}\,3^{1/4}$ = registry `a_over_ellP`, F79/F107) | assembly | `:L116–119 assemble()` | exact at $g_*=48$ (inventory #165) |

**Flags:** EXACTNESS unknown: #1, #2, #5 (Fraction/integer arithmetic, no inventory row). OTHER: writes `f61_results.json` into the source dir from `__main__`. OTHER: $\sqrt{8\pi}3^{1/4}$ recomputed from `eta`,`g_star` rather than imported — acceptable as the derivation under test (compare F79's `MeasuredConstant`), but F61 has no `MeasuredConstant` declaration (UNREGISTERED site; F79 has one). S25: the $\tfrac12$-per-mode in #4 is the object F193 Part A tried to delete (excluded) — F61 stands.

### `engine/forks/gravity/gr_fork_F63_spin_torsion_estimate.py` — F63 Einstein–Cartan spin-torsion magnitude estimate
**Status:** fork_unclaimed · unreferenced · **Findings:** F63 · **Lattice:** 2D Gaussian envelopes (mirrors F62 configs) · **Law:** n/a · **Units:** Planck ($\hbar=c=1$, $G=\ell_P^2$) / lattice occupation

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $\mathcal L_{4f}=-\tfrac3{16}\kappa\,(\bar\psi\gamma^5\gamma^\mu\psi)^2$, $\kappa=8\pi G$ | EC contact term (prefactor only; Hehl et al. 1976 imported) | `gr_fork_F63_spin_torsion_estimate.py:L68–69 ec_four_fermion_coefficient()` | unknown (Fraction 3/16, imported literature coefficient) |
| 2 | $a/\ell_P=\sqrt{2\pi\eta g_*}\,d^{1/4}$ with default $g_*=16$ | F61 cell (one generation) | `:L75–76 cell_size_over_ellP()` | unknown |
| 3 | $r_\text{cutoff}=\tfrac{3\pi}2 f(\ell_P/a)^2$, $r_\text{rest}=r_\text{cutoff}/m$ | torsion/Dirac energy ratio (polarised upper bound $\lvert j_5\rvert\le n$) | `:L101, L105 torsion_dirac_ratio()` | unknown |
| 4 | $f=\max\rho/\sum\rho$, $\rho=e^{-r^2/\sigma^2}$ (≈ $1/\pi\sigma^2$) | peak occupation of F62 packets | `:L125–126 _gaussian_peak_fraction()` | unknown |
| 5 | $f^*=\tfrac2{3\pi}(a/\ell_P)^2$ | Cartan occupation ($r_\text{cutoff}=1$) | `:L158 cartan_occupation()` | unknown |

**Flags:** ⚠ DOC/CODE MISMATCH: docstring L24 says it uses F61's pinned cell; default `g_star=16` gives $a\approx3.8\,\ell_P$ (printed at L200), not the adopted canonical $a=\sqrt{8\pi}3^{1/4}\ell_P\approx6.60\,\ell_P$ ($g_*=48$, F79/F107; S5 demotes $a_{F61}\approx3.81$). The conclusion (negligible torsion) strengthens with the larger cell, but the numbers are at the superseded ruler. OTHER: the step from $\ell_P^2/a^3$ to $(\ell_P/a)^2$ (docstring L91–97) replaces $m$ by the cutoff $1/a$ by fiat; $r_\text{rest}=r_\text{cutoff}/m$ mixes units (m dimensionless in $1/a$). OTHER: writes `f63_results.json` into the source dir. EXACTNESS unknown: #1–5.

### `engine/forks/gravity/gr_fork_F64_em_connection.py` — F64 EM-connection gravity: the single lattice dielectric $K$
**Status:** fork_live · test-only · **Findings:** F64 (D-EM1…D-EM11) · **Lattice:** mixed — sympy/mpmath closed forms (D-EM1, D-EM5, D-EM9); 3D periodic continuum-symbol FFT Poisson + eikonal slice (D-EM2/3, D-EM10); 2D square exact-QCA Dirac stepper reused from `dirac_gravity_fork` (D-EM-D*, D-EM4, D-EM11); 1D/2D Yee FDTD (D-EM5, D-EM6); continuous RK4 ray (D-EM7); 2D leapfrog wave (D-EM8). **None of it is the BCC photon.** · **Law:** n/a (no F91 propagator; FDTD is the small-$k$ Maxwell limit, not the paired-spinor photon) · **Units:** lattice ($G=1$, $c_0$ free, $c_\text{lat}^2=\tfrac12$ of the 2D walk in D-EM-D2a)
**Supersession / decision status:** **ADOPTED** as the canonical gravity route on 2026-05-31 (S3 supersedes F50/F52/F55/F62 rest-mass sourcing), then **RECLASSIFIED** by F178 (S4): the dielectric is the *vacuum/weak-field representation* of the induced Einstein equation, not the field equation inside matter. Live in vacuum and for $p\ll\rho c^2$ (factor-2 bending, $\beta=\gamma=1$, Mercury, Shapiro, redshift, D-EM9). Dead: "one field, one source (energy)" as fundamental (weakened to full $T_{\mu\nu}$), and the $T^{00}$-only sourcing as the law (F106 reclassified). S10-F271: the asymmetric operator ordering and first-order half-step in `lattice.curved._half_step_dH` are present in every F64-fork variable-$c$ (Cayley) result — handed back to this fork, not fixed. The canonical production implementation is `engine/interactions/gravity.py` (see 07b).

**Does:** tests whether ONE scalar placed as an impedance-matched dielectric $\varepsilon=\mu=K$ ($A=1/K$, $B=K$) reproduces both factor-1 redshift and factor-2 light bending; derives the placement; runs it statically, on the Dirac stepper, on Maxwell FDTD, on rays and as a wave field; fixes the nonlinear completion $K=e^{2u}$ by PPN $\beta$.

**Two dielectric forms coexist in this file — read the form column.** $K_\text{lin}=(1-u)^{-2}$ (the original "redshift-fixed" form, PPN $\beta=\tfrac12$, excluded by D-EM9 and retained per S3 only as the D-EM1/D-EM9 comparison control) vs $K=e^{2u}$ (canonical, D-EM9, adopted 2026-05-31).

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | clock_only $A=(1-u)^2,B=1$; refractive_only $A=1,B=(1+u)^2$; dielectric $K=(1-u)^{-2}$, $A=1/K,B=K$; with assigned $(\varepsilon,\mu)$ | D-EM1 single-scalar placements (sympy) | `gr_fork_F64_em_connection.py:L106–124 _maps()` | unknown (sympy; no inventory row) |
| 2 | $n=\sqrt{B/A}$ | eikonal index | `:L130 eikonal_index()` | unknown (sympy) |
| 3 | $Z=-\partial_u\sqrt A\rvert_0$, $K_\text{bend}=2\,\partial_un\rvert_0$, impedance $\sqrt{\mu/\varepsilon}$ | redshift and bend coefficients | `:L152–160 coefficients()` | unknown (sympy-exact; no inventory row) — spot-checked: clock (Z,K)=(1,2), refractive (0,2), dielectric (1,4) |
| 4 | $\alpha=\int_{-\infty}^{\infty}\partial_y\ln n\,dx$ at $y=b$ (mpmath, 40 dps, $n=(1-u)^{-2}$); $K_\text{bend}=\alpha b c^2/GM$ | full non-linearised deflection guard | `:L194–205 deflection_coeff_numeric()` | unknown (inferred: machine/quantitative — spot-check $-4.00031$ at $GM/bc^2=10^{-4}$ (signed, attractive)) |
| 5 | $\nabla^2\phi=4\pi G\rho$, $\hat\phi=-4\pi G\hat\rho/k^2$ (continuum symbol, periodic) | 3D Poisson (inlined copy of `gravity_emqg.solve_poisson_3d`) | `:L285–289 _solve_poisson_3d()` | unknown |
| 6 | dielectric $n=e^{2u}$; rest_only $n=e^{u}$; full_GR $n=\sqrt{(1+2u)/\lvert1-2u\rvert}$ | lattice index placements (canonical exp) | `:L311–318 _index_from_u()` | unknown |
| 7 | $\alpha=-\sum_{\lvert x\rvert<W}\partial_\perp\ln n$; $K=\alpha bc_0^2/GM\,/\,[W/\sqrt{W^2+b^2}]$ | windowed eikonal coefficient with finite-aperture correction | `:L341–353 _eikonal_K()` | unknown (inferred: quantitative) |
| 8 | $u_\text{em}=\tfrac12(E_x^2+B_y^2)$, $E_x=e^{-((r-R)/w)^2}\cos kx$, $B_y=\ldots\sin kx$ ⇒ $u_\text{em}=\tfrac12\text{env}^2$, normalised to $E_\text{tot}$ | massless field-energy shell source | `:L373–378 _em_energy_shell_3d()` | unknown |
| 9 | D-EM2: $K_\text{diel}\approx4$, $K_\text{rest}\approx2$, ratio $\approx2$ (10 %/10 %/0.05) | single-field lattice deflection | `:L418–430 test_dem2_single_field_deflection()` | unknown (inferred: quantitative) |
| 10 | D-EM3: $\nabla^2\Phi=4\pi G\,u_\text{tot}$ ⇒ $K_\text{rad}/K_\text{mass}\to1$; rest-leg $\rho_\text{rest}=0\Rightarrow\Phi=0$ | radiation-as-source discriminator | `:L489–513 test_dem3_radiation_as_source()` | unknown (inferred: quantitative (12 %); rest-leg leg is identically 0 by construction) |
| 11 | $K=e^{2u}$ | canonical dielectric | `:L568 K_canonical()` | unknown (registry); canonical closed form |
| 12 | $\omega=\operatorname{median}\,d(\text{unwrap}\arg a)/dt$, $a=\mathcal F^{-1}[\hat s\,h]$ (Hilbert) | resolution-free clock estimator (real 1D signal; plumbing) | `:L582–594 _inst_freq_hilbert()` | n/a |
| 13 | $u=-\Phi/c_0^2$, $K=e^{2u}$, $A=1/K$, $B=K$ ($AB\equiv1$) | canonical weak-field map | `:L609–611 AB_from_phi_dielectric()` | unknown ($AB=1$ by construction; inventory #191 covers $AB=1$ under block-spin) |
| 14 | $\sqrt A=1+a\xi$, $A=(1+a\xi)^2$, $B=1/A$ | dielectric Rindler | `:L630–633 dielectric_rindler_background()` | unknown |
| 15 | $\phi=-GM/\sqrt{r^2+r_s^2}\mapsto$ #13 | dielectric point mass (2D) | `:L652–654 dielectric_schwarzschild_background()` | unknown |
| 16 | $K=1\Rightarrow$ `gravity_dirac_step` (qca, $m=0$) $\equiv$ two exact Weyl walks | D-EM-D1 flat regression | `:L674–691 test_demD1_flat_regression()` | exact (inventory #150, 0.0) |
| 17 | $\lvert g\rvert\to a\,c_\text{lat}^2$, $c_\text{lat}^2=\tfrac12$; mass-independent | D-EM-D2a free fall (via `gravity_dirac_step_massive`) | `:L713, L746 test_demD2a_dielectric_freefall()` | unknown (inferred: quantitative (20 %)) |
| 18 | $A=e^{-2u}$, $r_\text{kin}=e^{-2u}$, qca rate $=c_0r_\text{kin}$; ratio vs $\arcsin(\sqrt A m)$ | D-EM-D2b redshift | `:L778–797 test_demD2b_dynamical_redshift()` | unknown (inferred: quantitative (3 %)) |
| 19 | $c_\text{eff}=c_0\sqrt{A/B}=c_0/K$; $\Delta\theta_\text{eik}=-\sum\partial_y\ln c_\text{eff}$ | D-EM-D2c deflection | `:L834, L859–863 test_demD2c_dielectric_deflection()` | unknown (inferred: quantitative ($3<\lvert K\rvert<5$, 25 %)) |
| 20 | $\rho=\lvert\Psi\rvert^2\to\Phi$ (2D) $\to(A,B)$ #13 $\to$ Cayley tick | D-EM-D3a self-gravitating dielectric | `:L891–903 run_backreaction_dielectric()` | machine (inventory #59: norm drift $7.5\times10^{-16}$/60 ticks) |
| 21 | bend ratio $\sum\partial\ln e^{2u}/\sum\partial\ln e^{u}\to2$; redshift ratio vs $\arcsin(\sqrt{A_n}m)/\arcsin(\sqrt{A_f}m)$ with $r_\text{kin}=A$ | D-EM4 one self-sourced $K$ gives both | `:L990–1000, L1006–1029 test_dem4_redshift_bend_consistency()` | unknown (inferred: quantitative (ratio ±0.30, redshift 4 %)) |
| 22 | $\varepsilon^{ij}=\mu^{ij}=\sqrt{-g}\,g^{ij}/(-g_{00})\to\sqrt{B/A}$ | Plebanski equivalent medium | `:L1077 _plebanski_eps_mu()` | unknown (sympy) |
| 23 | (A) $\varepsilon=\mu=K$ for both $(1/K,K)$ and $(1,K^2)$; (B) $\text{diag}(-1,K^2,K^2,K^2)=K\,\text{diag}(-1/K,K,K,K)$; (C) $\sqrt{\mu/\varepsilon}=1\wedge\sqrt{\varepsilon\mu}=K\Rightarrow\varepsilon=\mu=K$ unique; (D) $A=(1-u)^2$, $K=(1-u)^{-2}\Rightarrow AB=1$ | D-EM5 derivation of the dielectric placement | `:L1111–1134 dem5_derive_dielectric()` | unknown (sympy-exact; no inventory row) |
| 24 | 1D Yee: $H\mathrel{+}=dt\,\Delta E/\mu$, $E\mathrel{+}=dt\,\Delta H/\varepsilon$; reflected energy fraction for $(\varepsilon,\mu)=(K,K),(K^2,1),(1,K^2)$; Fresnel $((1/K-1)/(1/K+1))^2$ | D-EM5 lattice impedance check | `:L1197–1211 _dem5_fdtd_reflection()` | unknown (inferred: quantitative) |
| 25 | $u_\text{em}\to\nabla^2\Phi=4\pi G u_\text{em}$ (2D) $\to K=e^{2u}$ | EM-energy-sourced 2D lens | `:L1227–1231 _dielectric_from_em_energy_2d()`, `:L1237–1246 _solve_poisson_2d()` | unknown |
| 26 | 2D TM Yee on $\varepsilon=\mu=K$: $H_x\mathrel{-}=dt\,\partial_yE_z/\mu$, $H_y\mathrel{+}=dt\,\partial_xE_z/\mu$, $E_z\mathrel{+}=dt(\partial_xH_y-\partial_yH_x)/\varepsilon$; energy-centroid track | D-EM6 light-bends-light | `:L1270–1273 _fdtd_TM_beam_2d()`; verdict `:L1314–1336 test_dem6_light_bends_light()` | unknown (inferred: quantitative (ratio $2\pm0.05$, ≥65 % of eikonal)) |
| 27 | ray: $\dot{\mathbf x}=\mathbf p$, $\dot{\mathbf p}=n\nabla n$ (RK4), $H=\tfrac12(p^2-n^2)$; $n=(1-u)^{-2}$ or $e^{2u}$; $\alpha=-\arg(p_x,p_y)$ | D-EM7 absolute deflection on a ray | `:L1373–1404 _ray_deflection()`; `:L1424–1432 test_dem7_absolute_deflection_3d()` | unknown (inferred: quantitative ($\lvert K-4\rvert<4\times10^{-3}$ at $10^{-4}$)) |
| 28 | $\Phi^{n+1}=2\Phi^n-\Phi^{n-1}+(c_g\,dt)^2(\nabla^2_5\Phi^n-4\pi G\rho)$; $E=\tfrac12\sum\dot\Phi^2+\tfrac12c_g^2\sum\lvert\nabla\Phi\rvert^2$ | D-EM8 dynamical $\Phi$ (leapfrog, 5-point Laplacian) | `:L1460–1461 _lap2d()`, `:L1499, L1508–1512 test_dem8_dynamical_field()` | unknown (inferred: quantitative (static 5e-3, speed 5 %, energy 2 %)) |
| 29 | $A=1-2U+2\beta U^2$, $B=1+2\gamma U$ ⇒ $(\beta,\gamma)$; bending $(1+\gamma)/2$, perihelion $(2+2\gamma-\beta)/3$ | D-EM9 PPN extraction | `:L1550–1553 _ppn_beta_gamma()`, `:L1597–1599 test_dem9_strong_field_ppn()` | unknown (sympy-exact; no inventory row) — spot-checked $(1-u)^{-2}$: $(\beta,\gamma)=(\tfrac12,1)$, perihelion $7/6$; $e^{2u}$: $(1,1)$ |
| 30 | co-evolving probe clocks on the full $K(x)$ (Cayley), Hilbert frequency, ratio vs $\arcsin(\sqrt A m)$ | D-EM11 co-evolving self-redshift | `:L1673–1698 test_dem11_coevolving_self_redshift()` | unknown (inferred: quantitative (15 %)) |
| 31 | (1) fit $\phi=-GM/r+c$ on shell 8<r<20 ⇒ $GM\approx1$; (2) $a/\ell_P=\sqrt{2\pi\eta g_*}\,3^{1/4}$, $\eta=1/12$; (3) MC $\int\tfrac{d^dk}{(2\pi)^d}\tfrac1{2c\lvert k\rvert}$ ratio $\to\sqrt d$ | D-EM10 pinning $4\pi G$ to the cell | `:L1764–1795 test_dem10_pin_G_to_cell_scale()` | unknown (inferred: quantitative (3 % / 0.5 % / 2 %)) |
| 32 | $A=e^{-2u}$, $B=e^{2u}$, $c_\gamma=c_m=c_0\sqrt{A/B}=c_0e^{-2u}$, $\tau=\sqrt A=e^{-u}$ | harness fork object (canonical) | `:L1824–1835 make_fork()` | unknown |

**Inputs → outputs:** potentials/densities/field arrays or none (closed-form tests) → pass dicts; `__main__` prints D-EM1 only (no artifact write). **Depends on:** `dirac_gravity_fork` (this file, above), `particles/dirac.py` helpers (06b), `lattice/curved.CayleyVarcSolver2D` (03), `casim.numerics.fft` (02), sympy, mpmath. Canonical successor: `engine/interactions/gravity.py` (07b).
**Flags:**
- ⚠ DOC/CODE MISMATCH (D-EM1 impedance discriminator): the docstring (L57–61) says the two non-dielectric placements "break the impedance and are not dielectrics", but `_maps()` assigns clock_only $\varepsilon=1/\sqrt{AB}=\mu=\sqrt{B/A}$ and refractive_only $\varepsilon=\mu=\sqrt{B/A}$ — spot-checked: `impedance_constant` is **True for all three**. The D-EM1 verdict therefore rests only on $(Z,K_\text{bend})$; the impedance leg discriminates nothing. D-EM5's FDTD (#24) uses a *different* assignment for the same names (clock_only $\varepsilon=1,\mu=K^2$).
- ⚠ DOC/CODE MISMATCH ($K$ form): docstrings still describe the superseded $K=(1-u)^{-2}$ where the code uses $e^{2u}$ — `dielectric_schwarzschild_background` (L638 "A=(1−u)², B=(1−u)⁻²"), `test_demD2b` (L769–771 "√A=(1−u)"), `test_dem4` (L946, L987–988, L1048 "n = K = (1−u)⁻²"), `_dielectric_from_em_energy_2d` (L1223 "K=(1−u)⁻²"), D-EM8 docstring (L1453, L1466), block comment L541–545. Code at those sites is canonical $e^{2u}$.
- ⚠ DOC/CODE MISMATCH (D-EM1/D-EM5/D-EM7 still test the β=½ form): D-EM1 (#1, #4), D-EM5 step (D) (#23) and D-EM7's pass criterion (#27, `form="dielectric"`) run on $K=(1-u)^{-2}$, the form D-EM9 excludes. D-EM7 does also integrate `exp`, but its PASS gate is on the excluded form. The D-EM5 "derivation" thus derives the conformal factor only to $O(u)$ — stated honestly in D-EM9's docstring.
- SUPERSEDED (partial, S4-F178): the dielectric is the vacuum/weak-field representation only; D-EM3's "equal energy ⇒ equal gravity" is $T^{00}$ sourcing, reclassified as the static weak-field reduction of full-$T_{\mu\nu}$ sourcing.
- OTHER (S10-F271): D-EM-D2c, D-EM-D3a, D-EM11 run the Cayley variable-$c$ solver whose half-step ordering/first-order defect F271 found; results carry that defect.
- ⚠ DOC/CODE MISMATCH (rest-leg rate): as in `dirac_gravity_fork`, the D2b/D-EM4/D-EM11 prediction is $\arcsin(\sqrt A m)$ but the stepper rotates by $\sqrt A\,m$ per tick at $k=0$.
- OTHER: D-EM-D2b and D-EM4 pass `r_kin_scalar = c0·r_kin` (rate $c_0e^{-2u}$ or $c_0A$), whereas F62 D2b used $\sqrt A$ — the kinetic rate convention changes between the "same" tests (irrelevant at $k=0$ but not documented).
- OTHER: D-EM-D2a uses `gravity_dirac_step_massive`, which reads only $\sqrt A$ — the "dielectric" $B=1/A$ of #14 is never used, so D-EM-D2a is identical to F62 D2a (the docstring admits the rest leg is shared).
- ⚠ DOC/CODE MISMATCH (D-EM10): pins the cell at $g_*=16$ ⇒ $a\approx3.81\,\ell_P$ (L1729, L1813); the adopted canonical ruler is $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ at $g_*=48$ (F79/F107; S5 demotes $a_{F61}$). The table includes 48→6.598 but the verdict uses 16.
- OTHER: D-EM10 (1) fits $\phi$ with the continuum $k^2$ symbol, not the exact stencil (the production F106 identity uses $-4\sum\sin^2(k_i/2)$, inventory #182); the 4π check is therefore of the continuum Green's function.
- OTHER: several `import numpy as np` inside functions and direct `np.fft.fftfreq` (allowed); all transforms via `casim.numerics.fft`; FDTD and Hilbert are real-valued — no chiral-transform hazard. Seven blank lines after `import numpy as np` in D-EM2/D-EM3 (cosmetic, removed code).
- EXACTNESS unknown: #1–3, #5, #6, #8, #11, #13–15, #22, #23, #25, #29, #32 (the sympy ones are algebraically exact in fact but have no registry/inventory row).

### `engine/forks/gravity/gr_fork_F79_structural_G.py` — F79 Newton's constant from lattice structure
**Status:** fork_live · test-only · **Findings:** F79 · **Lattice:** n/a (radial quadrature, algebra) · **Law:** n/a · **Units:** lattice → SI (CODATA anchors)
**Decision status:** ADOPTED — the structural $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ and $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ are canonical (F79/F107; retained by S4; ruler adoption S5). Registry constants `a_over_ellP` (exact, F79/F107) and `G_LATTICE` $=c_\text{lat}^4/(8\pi)=1/(72\pi)$ (exact, F79/F107) descend from this. This file carries a `MeasuredConstant` (kind `measured`, `constants/measured.py:L130`) because it *derives* $a/\ell_P$.

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $I(c)=\int_0^\Lambda\tfrac{4\pi k^2dk}{(2\pi)^3}\tfrac1{2ck}=\tfrac{\Lambda^2}{8\pi^2c}$; $I\cdot c$ constant (trapezoid) ⇒ $1/G\propto1/c_\text{lat}=\sqrt d$ | S1 loop-channel scaling | `gr_fork_F79_structural_G.py:L94–100 s1_clat_and_inverse_G_scaling()` | unknown (inferred: quantitative (spread $<10^{-6}$, analytic match $<10^{-3}$)) |
| 2 | $c_\text{lat}=1/\sqrt d$ (dict, hard-coded) | structural light speed (F26: $1/\sqrt3$ at $d=3$) | `:L102` | unknown (inferred: exact (registry `c_lat`, F26) — but recomputed as literal, not imported) |
| 3 | $\eta_\text{scalar}=\tfrac1{12}$; Dirac $a_1/R=\tfrac46-1=-\tfrac13$, $c_D=\tfrac13$, $\eta_D=\tfrac16$; $\eta_\text{Weyl}=\tfrac1{12}$ | S2 heat-kernel η (Fraction) | `:L127–135 s2_eta_weyl_exact()` | exact (inventory #165 carries $\eta=1/12$) |
| 4 | $T^\mu{}_\mu=-\tfrac12(E^2+B^2)+\operatorname{tr}\big[-(EE^T+BB^T)+\tfrac12(E^2+B^2)I\big]=0$ | S3 EM stress tensor traceless in 3+1D | `:L153–158 _em_stress_tensor()` | exact (inventory #164; identity, verified to <1e-12) |
| 5 | control: $m^2\langle\phi^2\rangle>0$ | S3 massive-scalar trace sources $K$ | `:L182 s3_…()` | unknown |
| 6 | $S_\text{bare}=c^2$, $B=0.08/c$, exponents +2, −1, gap −3 | S4 tree-vs-loop gap | `:L205–209 s4_channel_gap()` | unknown (see flag) |
| 7 | per generation $2+1+6+3+3+1=16$; $n_\text{gen}=\dim T_{1u}=3$; $g_*=48$ | S5 mode count | `:L233–237 s5_gstar_structural()` | exact (inventory #165 carries $g_*=48$) |
| 8 | $2\pi\eta g_*=8\pi$; $P_\text{pre}=\sqrt{8\pi}$; $1/G$ coeff $2\pi\eta g_*\sqrt d=8\pi\sqrt3$; $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$; $\tau/t_P=\sqrt{8\pi}\,3^{-1/4}$ | S6 assembly | `:L264–269 s6_assemble()` | exact (inventory #165) |
| 9 | $G=a^2c^3/(2\pi\eta g_*\sqrt d\,\hbar)=a^2c^3/(8\pi\sqrt3\,\hbar)$ at $a=(a/\ell_P)\ell_P$; residual vs $G_\text{CODATA}$ | SI closed form and consistency | `:L273–274` | quantitative — spot-checked residual $2.96\times10^{-8}$ (inventory: $3\times10^{-8}$, F112) |

**Inputs → outputs:** none → dict of S1–S6 with `passed`. Constants: `G_CODATA`, `c_SI` (external, SI), `ell_P_m`, `hbar_SI` (external, CODATA) from `constants/geometry.py`.
**Flags:** OTHER: S4 (#6) fits exponents of arrays it *constructed* as $c^2$ and $0.08/c$ — it re-states F60, it does not compute either channel (tautological check). OTHER: `T_P = 5.391247e-44` is an unregistered literal (L255; no `t_P` in the registry — UNREGISTERED). OTHER: the residual in #9 is the self-consistency of $a/\ell_P$ with CODATA's $\ell_P$ vs $G$ (i.e. CODATA's own internal consistency), not an independent prediction of $G$ — as F79's "Honest scope" says. S5's "$n_\text{gen}=\dim T_{1u}$" is asserted as an integer, not derived here. EXACTNESS unknown: #5, #6.

### `engine/forks/gravity/gr_tensor_stub.py` — runnable Fork E demonstration + exact-metric geodesic GR-4
**Status:** fork_unclaimed · unreferenced · **Findings:** (docstring "Finding 19"; F16 era) · **Lattice:** 3D SC open-BC potential (field sector) / continuum quadrature (GR-4) · **Law:** n/a · **Units:** lattice
**Supersession:** field-sector part SUPERSEDED with the GR-3 trichotomy (S16); the geodesic integrator on the exact isotropic Schwarzschild metric is plain GR (consistent with F178's "exact vacuum solution is Schwarzschild").

| # | Equation | What it does | Where | Exactness |
|---|----------|--------------|-------|-----------|
| 1 | $A=\big(\tfrac{1-u/2}{1+u/2}\big)^2$, $B=(1+u/2)^4$, $u=GM/(rc^2)$ | exact isotropic Schwarzschild (radial) | `gr_tensor_stub.py:L74–82 _A_exact(), _B_exact()` | unknown |
| 2 | turning points: $P/(A_ic^2)-Q/(B_ir_i^2)=c^2$, $i=1,2$ ⇒ $E^2=P$, $L^2=Q$ | conserved energy/angular momentum | `:L97–102 geodesic_perihelion_advance()` | unknown (inferred: machine (linear solve)) |
| 3 | $\dot r^2=\tfrac1B\big[\tfrac{E^2}{Ac^2}-c^2-\tfrac{L^2}{Br^2}\big]$, $d\varphi/dr=\tfrac{L/(Br^2)}{\sqrt{\dot r^2}}$, $r=c_0-c_1\cos\chi$ | timelike equatorial geodesic, singularity-removing substitution | `:L109–117` | unknown (inferred: quantitative) |
| 4 | $\Delta\omega=2\int_{r_1}^{r_2}\tfrac{d\varphi}{dr}dr-2\pi$ (open midpoint rule, $n=20000$); ref $6\pi GM/(pc^2)$ | GR-4 advance, all PN orders | `:L118–124` | unknown (inferred: quantitative (self-check $\lvert r-1\rvert<2\times10^{-3}$ at $GM=10^{-5}$)) |
| 5 | field sector: GR-1/2/3 from `gr3_fork_harness` on baseline, B, E-linearized, E-exact | column comparison | `:L155–164 run_field_sector()` | unknown (inferred: quantitative) |
| 6 | checks: E-lin ≡ B ($<10^{-9}$); E-exact GR-3 $\approx1$; baseline $\approx2$; geodesic/1PN $\approx1$ | self-checks | `:L178–196 self_checks()` | unknown (inferred: quantitative) |

**Flags:** SUPERSEDED (field sector, S16). OTHER: stale citation "Finding 19" (see Fork E). OTHER: `__main__` writes `test-results/gr_tensor_stub.{json,md}` (five-`..` path, correct after C6). The claim "the 1.5 % cap on GR-4 is a 2PN truncation" (docstring L25–26) is superseded by S16's diagnosis (the harness normaliser is wrong by 2 and integrates no fork's metric). EXACTNESS unknown: #1.
