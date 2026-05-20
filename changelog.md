# Changelog

Non-trivial software changes and decisions for the Physics Notes simulation work.

## 2026-05-19 - 23:30 — SR-2 β_LV coefficient derived in closed form

Closed the "no closed-form $\beta_\text{LV}$ extracted" open item from Finding 12 (`findings.md` §"What this does *not* close"). The leading Lorentz-violation coefficient that controls the SR-2 ratio's departure from the continuum-SR $1/\gamma$ is now an exact analytic function of the dimensionless mass $m$.

**Derivation method.** Implicit-differentiate $\cos\omega(k) = \sqrt{1-m^2}\cos(k/\sqrt 2)$ at $k=0$:

- $\omega(0) = \arcsin m$
- $\omega''(0) = \sqrt{1-m^2}/m$
- $\omega''''(0) = -(\sqrt{1-m^2}/m^3)(3 - 2m^2)$
- All odd derivatives vanish by parity.

Form $\omega_\text{moving}(u) = \omega(u) - u\,\omega'(u)$, divide by $\omega_0 = \arcsin m$, then re-express the resulting series in $\beta = c_\text{lat}^{-1} v_g = \omega'(u)$ via series inversion. Subtracting the Taylor expansion of $1/\gamma_\text{SR} = \sqrt{1-\beta^2}$ extracts the coefficients

$$\beta_\text{LV}(m) = \tfrac{1}{2}\!\left(1 - \tfrac{m}{\sqrt{1-m^2}\,\arcsin m}\right) = -\tfrac{m^2}{6} - \tfrac{11 m^4}{90} + \mathcal O(m^6).$$

$$\gamma_\text{LV}(m) = \tfrac{1}{8} - \tfrac{m\,(3 - 2m^2)}{24\,(1-m^2)^{3/2}\,\arcsin m}.$$

**Sign correction.** Finding 12 stated $\beta_\text{LV}$ is "positive" — that was wrong. $\beta_\text{LV}(m) < 0$ for every $m \in (0,1)$ because $\sqrt{1-m^2}\arcsin m < m$. The magnitudes Finding 12 reported are correct; only the sign was misread from an unsigned $|\Delta|$ column. Finding 12 has been amended in place; Finding 15 (new) holds the full derivation.

**Files added.**

| File | Role |
|---|---|
| `ca-simulation/derive_beta_LV.py` | Symbolic (sympy) re-derivation + numerical scan against the SR-2 (m, k) grid. Confirms the closed-form match (`>>> Closed-form formulas confirmed symbolically. <<<`). |

**Files updated.**

- `findings.md` — new Finding 15 (~5 pages); Finding 12 amended in two places (sign of $\beta_\text{LV}$; "open item" struck through with pointer to Finding 15).
- `ca-reference.md` — new section recording the closed forms and adding two rows to the exact-algebraic ledger (running total: 15).
- `exactness-inventory.md` — two new Tier-1 entries (#20 $\beta_\text{LV}$, #21 $\gamma_\text{LV}$); tally bumped from 19 to 21 exact algebraic results.
- `lattice-vs-spacetime-tests.md` — SR-2 status updated to "**LV CURVE CHARACTERISED ANALYTICALLY**"; gate revised to a three-reading split (dispersion-identity, continuum-SR, closed-form-LV-coefficient).
- `project-status.md` — new progress row dated 2026-05-19.

**Verification.** At each (m, k) point on the SR-2 grid, the measured $\Delta = R - 1/\gamma_\text{SR}$ matches $\beta_\text{LV}(m)\beta^2 + \gamma_\text{LV}(m)\beta^4$ to:

| $\beta = v_g/c_\text{lat}$ | rel.err of $\beta^2$ truncation | rel.err of $\beta^4$ truncation |
|---|---|---|
| 0.001 – 0.01 | $10^{-5}$ – $10^{-3}$ | $10^{-9}$ – $10^{-7}$ |
| 0.01 – 0.1 | $10^{-3}$ – $10^{-1}$ | $10^{-6}$ – $10^{-4}$ |
| 0.1 – 0.3 | $10^{-1}$ – $10^{0}$ | $10^{-3}$ – $10^{-1}$ |

The $\beta^4$ truncation is sufficient for any working point of the SR-2 / QG-2 tests; higher orders are mechanically obtainable from the same recursion.

**Bottom-line interpretation.** The lattice's predicted Planck-scale Lorentz violation is not a single dimensionless number but a function $\beta_\text{LV}(m)$ that vanishes as $m\to 0$. The Weyl sector is exactly Lorentz-invariant at this order; only the Dirac sector picks up the deformation, and it is suppressed by $m^2$ at small mass. This sharpens the falsifiability question for QG-2.

## 2026-05-19 - 22:53 — Top-10 priority test sweep complete

Built and executed all ten tests from the priority ranking in
`lattice-vs-spacetime-tests.md`.  Detailed write-up: Finding 14
(§14.1 – §14.14) in `findings.md`.

**New files:**

- `ca-simulation/tests-priority/test_01_GR1_light_deflection.py` — eikonal
  ray tracer through 3D EMQG potential, scans $M$, $b$, $L$.  Pure-numpy
  (no scipy needed).
- `ca-simulation/tests-priority/test_02_QM1_CHSH.py` — pure-state CHSH +
  12-tick Weyl lattice propagation with singlet encoded on two separated
  Gaussian packets.
- `ca-simulation/tests-priority/test_04_GR3_pound_rebka.py` — phase-tick
  redshift via $c(x)$ sampled at near/far cells of a Gaussian-mass potential.
- `ca-simulation/tests-priority/test_05_GR2_shapiro.py` — line integral of
  $1/c(x)$ vs analytic GR Shapiro
  $(2GM/c^3)\log[(r_1+r_2+r_{12})/(r_1+r_2-r_{12})]$.
- `ca-simulation/tests-priority/test_06_QG2_planck_LV.py` — direct evaluation
  of BCC dispersion at small $k$ along axis vs diagonal, power-law fit to
  $E_\text{LV}$, SI conversion across $a \in [10^{-35}, 10^{-32}]$ m.
- `ca-simulation/tests-priority/test_07_QFT5_neutrino.py` — 2- and 3-flavour
  PMNS matrix evolution with relative-phase factoring to avoid float64
  overflow at $E\cdot L \sim 10^{21}$ rad.
- `ca-simulation/tests-priority/test_08_QM2_tunneling.py` — Gaussian Dirac
  packet on a rectangular $A_0$ barrier; sweet-spot vs Klein-regime scans.
- `ca-simulation/tests-priority/test_09_GR4_mercury.py` — velocity-Verlet
  integration of the Will/Soffel 1PN equation of motion; perihelion
  detection by parabolic interpolation.
- `ca-simulation/tests-priority/test_10_QG4_charge.py` — U(1) charge over
  1000 steps at $L=256$; chiral charge at $m=0$ and $m=0.5$; per-step
  discrete continuity check.

**Result files:**

- `test-results/top10_T0{1,2,4,5,6,7,8,9,10}_*.json` — full JSON dumps of
  every run, including scan parameters, per-config values, gate verdicts.

**Methodology notes:**

- All scripts work in the scipy-free sandbox.  The Cayley sparse-LU stepper
  (`ca_curved.CayleyVarcSolver2D`) is *not* used; instead each test uses
  a pure-numpy substitute (FFT-Poisson + eikonal ray, 1PN Verlet, direct
  dispersion evaluation, etc.).  Where the substitute loses information,
  the loss is annotated in the test docstring.
- For QFT-5, *relative*-phase evolution (factor out the common $e^{-iEL}$
  phase) is mandatory; direct $E\cdot L$ at km-scale baselines and GeV
  energies overflows complex128.  This idiom is worth keeping for future
  flavour-mixing or long-baseline propagation code.

**Documentation updates:**

- `findings.md` — Finding 14 §14.1 through §14.14 added.
- `lattice-vs-spacetime-tests.md` — status rows updated for GR-1, GR-2,
  GR-3, GR-4, QM-1, QM-2, QFT-5, QG-2, QG-4; checkpoint summary table
  inserted at top of priority-ranking section.
- `exactness-inventory.md` — 5 new Tier-1 results (CHSH Tsirelson, PMNS
  unitarity, 2-flavour propagator, chiral $m=0$ conservation, BCC axis
  dispersion); 8 new Tier-3 results (GR-1, GR-3, GR-2, QG-2, QFT-5 peak,
  QM-2 sweet spot, GR-4 perihelion, QG-4 U(1) FFT floor).
- `project-status.md` — Sweep summary appended.
- `ca-reference.md` — Eight new measurement observations folded in.

## 2026-05-19 - 17:45 — SR-2 expanded to 3D using the BCC lattice

Built the 3D BCC Dirac stepper and the 3D analog of `test_SR2_time_dilation.py`.  Mirrors the 2D test (Finding 12) one-for-one but uses Paper 1 Eq. 15 (BCC Weyl QCA) as the kinetic block instead of Eq. 16 (2D square QCA), so the lattice light speed becomes $c_\text{lat} = 1/\sqrt{3}$ instead of $1/\sqrt 2$.

**Files added.**

| File | Role |
|---|---|
| `ca-simulation/ca_dirac_bcc.py` | Exact-QCA 3D Dirac propagator on the BCC lattice — `dirac_step_3d_bcc_splitstep`, `bcc_dirac_dispersion`, `build_D_k_matrix`, plus dispersion/unitarity/norm-drift verifiers |
| `ca-simulation/test_SR2_3D_time_dilation.py` | 3D analog of `test_SR2_time_dilation.py`.  Part A scans (m, k) algebraically; Part B propagates 4-spinor plane waves on $L^3$ lattices and extracts phase rates via FFT-based sub-pixel sampling |
| `ca-simulation/_sr2_3d_scan.py` | One-off on-grid k characterisation utility — caches static phase rate per (L, m); reproduces the residual table in `findings.md` Finding 13 |

**Stepper design — the 4×4 unitarity closure on BCC.**  The Dirac single-tick unitary is

$$D_k = \begin{pmatrix} n\,A_k & im\,I \\ im\,I & n\,A_k^\dagger \end{pmatrix},\qquad n = \sqrt{1-m^2},\ n^2+m^2=1$$

where $A_k$ is the 3D BCC Weyl-QCA unitary (`ca_bcc.bcc_unitary`).  The choice $A_-^\text{block} = A_k^\dagger$ (rather than the literature's "$A_+$ with sign-flipped helicity") is forced by unitarity of the full 4×4 $D_k$, exactly as in the 2D case — the off-diagonal $(D^\dagger D)_{12}$ block reads $imn(A^\dagger - A_-^\text{block})$ which must vanish.  Verified numerically: $\|D^\dagger D - I\|_F = 8.9\times 10^{-16}$ across 64 random k's at $m=0.3$.

**Dispersion.**  $\omega_k = \arccos(n\cdot u(k))$ with $u(k) = c_xc_yc_z + s_xs_ys_z$, $c_i=\cos(k_i/\sqrt 3)$, $s_i=\sin(k_i/\sqrt 3)$.  At $k_y=k_z=0$ this collapses to $\omega_k = \arccos(n\cos(k_x/\sqrt 3))$ — direct 3D analog of the 2D $\arccos(n\cos(k_x/\sqrt 2))$.  Along the $x$-axis the group velocity is $v_g = (n\sin(k_x/\sqrt 3)/\sqrt 3)/\sin(\omega_k)$.

**Stepper sanity floors.**  $L=16^3$ smoke test: unitarity $8.9\times 10^{-16}$, dispersion residual $2.2\times 10^{-16}$, norm drift over 200 steps $2.2\times 10^{-14}$, $A_0 = I$ at $k=0$ with $m=0$ exact.

**SR-2 readings — two-gate structure carries over from 2D.**

*Dispersion-identity gate.* `ratio_num = (ω_k − k v_g)/arcsin(m)` lands at FFT round-off everywhere in the on-grid scan.  Numerical-vs-dispersion residual range across $L\in\{32, 48\}$, $n_\text{mode}\in\{1, 2, 3\}$, $m\in\{0.1, 0.3, 0.5\}$: $1.1\times 10^{-16}$ to $1.9\times 10^{-15}$.  Single Part B reading at $L=32, m=0.1, k=0$ (static-only): residual $1.1\times 10^{-15}$.  All configs pass the roadmap $10^{-12}$ gate by 3 orders of magnitude.

*Continuum-SR gate.* `ratio_num` vs $1/\gamma_\text{SR} = \sqrt{1-(v_g/c_\text{lat})^2}$, $c_\text{lat}=1/\sqrt 3$.  Scales cleanly as $(v_g/c_\text{lat})^2$ at small $k$ — the predicted lattice Lorentz-violation curve.  Algebraic Part A: smallest residual $5.1\times 10^{-8}$ at $(m=0.5, k=0.001)$; largest $1.13\times 10^{-2}$ at $(m=0.5, k=0.5)$.

**New physics observation — BCC LV coefficient is structurally larger than 2D square.**  At $v_g/c_\text{lat}\approx 0.5$ the 2D test (Finding 12) measured continuum-SR gap $\sim 10^{-3}$; the 3D BCC test measures $\sim 1.5\times 10^{-2}$ at the same fractional velocity.  Roughly an order of magnitude larger.  Consistent with the BCC's known leading dispersion correction $\omega(k) - |k|/\sqrt 3 \sim k/18$ along $(1,1,1)$ (Paper 1, verified during the v2 build), whereas the 2D arccos correction is $O(k^2)$.  Documented in `findings.md` Finding 13.

**Roadmap update.**  `lattice-vs-spacetime-tests.md` SR-2 entry left as-is for now (Finding 12 statement is correct for 2D); a 3D extension row should be added on the next pass.

**No regressions.**  Existing 2D test files (`test_SR2_time_dilation.py`, etc.) untouched.  `ca_dirac.py` and `ca_bcc.py` untouched.

## 2026-05-18 (Test roadmap and exactness inventory added)

Drafted two new top-level project documents in response to `next-steps.md` line 13 ("begin drafting a series of tests… how well does the lattice hold up against current data we have about spacetime?"):

- **`lattice-vs-spacetime-tests.md`** — full-sweep test roadmap covering SR, GR, QM, QFT, QG, and cosmology. ~40 tests total, each with target formula, current status (`PASS` / `RATIO PASS` / `PROPOSED` / `BLOCKED`), quantitative pass/fail gate, lattice cost, and discriminating power. Closes with a top-10 priority ranking; highest-value next builds are GR-1 (absolute Eddington deflection coefficient, Stage A), QM-1 (CHSH Bell test), and SR-2 (moving-clock time dilation via the phase-tick framework). All gates are quantitative as requested.
- **`exactness-inventory.md`** — short three-tier table sorting the existing test corpus into exact algebraic (14 results), machine precision (6 results), and quantitative-within-tolerance (14 results), plus 7 open/blocked items. Per CLAUDE.md guidance to keep a short exact-vs-machine-precision table. Sources every cell back to `findings.md`, `project-status.md`, `ca-reference.md`, or `test-results/qca-verifications-results.md`.

**Decision recorded.** The roadmap is written against measured data, not against competing theories. Where multiple theories make the same prediction, the lattice is compared to the measurement. Strong-field GR, lattice QCD, and a first-principles derivation of $(a, \tau)$ are explicitly out of scope for this roadmap. The SI-unit identification (Finding 10) is a documented blocker for absolute-magnitude GR tests; ratio-form GR tests can proceed without it.

No code changes in this entry; both files are markdown only.

## 2026-05-18 (Emergent-time roadmap — T0 + T1 + T2 + T4 + T5 landed)

Implemented Phases T0, T1, T2, T4, and T5 of `ca-emergent-time-plan.md`.  T3 (partitioned / Margolus async update) explicitly skipped per direction; T1+T2 demonstrate that the tick reading is consistent with v2 in the synchronous regime, so the asynchronous re-architecting in T3 is optional for the *interpretation* claim.

**Files added.**

| File | Role |
|---|---|
| `ca-simulation/ca_lazy.py` | T1.A wrapper — `TickCounter`, `lazy_step`, sync-vs-lazy regression utility |
| `ca-simulation/tick_heatmap.py` | T1.B visualization — `tick_heatmap`, `tick_heatmap_with_phi` |
| `ca-simulation/test_emergent_time_T1.py` | T1 regression tests (4/4 PASS) |
| `ca-simulation/test_emergent_time_shapiro.py` | T2.A/B/C tests (3/3 PASS) — Shapiro / redshift / group velocity in ticks |
| `ca-simulation/test_emergent_time_T5.py` | T5.A/B/C tests (3/3 PASS) — vacuum cells exact, lazy benchmark, asymmetric tick clocks |

**T1.A — lazy-update propagator.**  Wraps any v2 propagator step and increments a per-cell `int64` counter at cells whose pre/post residual exceeds $\varepsilon = 10^{-13}$.  Bookkeeping-only laziness: FFT-based propagators touch every cell by construction, so the lazy run is bit-for-bit identical to the synchronous run (verified at max diff = 0.00e+00 for Weyl free, Higgs Mexican-hat, and unified F1 step).  Vacuum-cell ε calibration: max per-step residual on $\Phi = v$ pure-vacuum state is $1.18\times 10^{-16}$ (Higgs $1.11\times 10^{-16}$; Weyl $\psi = 0$ exactly zero); $\varepsilon = 10^{-13}$ sits 849× above the floor.

**T1.B — tick-field heatmap.**  Renders $N(\mathbf x)$ as a `viridis` heatmap on $\log_{10}(1 + N)$ scale, with optional $|\psi|^2$ contour overlay and a vacuum-red overlay flag.  Three heatmaps generated: `ticks_heatmap_weyl.png`, `ticks_heatmap_higgs.png`, `ticks_heatmap_F1_unified.png`.

**T2.A — group velocity in tick units.**  Re-derived the B1 measurement using $\bar N$ (tick-weighted average over $|\psi|^2$ support) instead of global $n$ as the time axis.  Both readings give the same group velocity to FFT round-off — relative difference $5.75\times 10^{-16}$ between $|\mathbf v_g|$ measured against $n$ vs against $\bar N$.  Lattice-dispersion gap to the small-$\mathbf k$ analytic $c\hat{\mathbf k}$ is the usual L=64 finite-size 3.5% (same as existing B1).

**T2.B — Shapiro delay tick-ratio (load-bearing T2 gate).**  Phase-accumulation (not binary tick count) is the right tick metric for this — see *Findings* below.  For a plane wave at on-grid $k = 2\pi\cdot 6/L$ on a 128×128 lattice with a Gaussian-mass-sourced $\phi$:

- $N_{\text{phase}}(\text{in}) / N_{\text{phase}}(\text{out}) = 0.8141643534$
- $c_{\text{in}} / c_{\text{out}}              = 0.8141643534$
- Relative difference $|\Delta\text{ratio}|/\text{ratio} = 2.73\times 10^{-16}$ — **EXACT to FFT round-off, and algebraically exact under $c(\phi) = c_0/(1-2\phi/c_0^2)$ and $\omega = c\cdot k$.**

T2.B passes with three orders of headroom on the $10^{-12}$ gate.

**T2.C — Redshift from ticks.**  Algebraic substitution:

$$z_{\text{tick}} = \frac{1}{r_s} - 1 = \left(1 - \frac{2\phi_s}{c_0^2}\right) - 1 = -\frac{2\phi_s}{c_0^2} \quad\text{EXACTLY}.$$

For $\phi_s = -1.416\times 10^{-2}$, $c_0 = 0.4$: $z = 0.177045$ from both readings, residual $4.7\times 10^{-16}$.

**T4.A, T4.B — documentation in `ca-emergent-time-proposition.md` §6, §7.**  Conservation of update-rule-shift generator + DSR boost on tick-foliated frames.  In the synchronous (T1, T2) regime the tick foliation coincides with the constant-$n$ foliation, so the Paper 4 deformation map $\mathcal D$ is unchanged.

**T5.A — vacuum cells have $N(\mathbf x) = 0$ exactly.**  L=256, n=40, $\sigma$=4: 80.4% of the lattice is outside the Dirac packet's causal cone, and every one of those cells has $N(\mathbf x) = 0$ — bit-exact zero, not "small."

**T5.B — lazy-wrapper overhead benchmark.**  Wall-clock for Weyl 2D split-step at L ∈ {64, 128, 256}: lazy wrapper adds 9.3% / 10.3% / 13.0% overhead over the synchronous run.  Bounded constant factor, as predicted.  The lazy wrapper *cannot* speed up the FFT sub-step (Risk #1 of T1.A); the position-space sub-step laziness for T5.B's predicted $(L/\sigma_x)^d$ speed-up is left as a follow-up.

**T5.C — asymmetric tick clocks probe $\phi$.**  Riding on T2.B: ratio $N(\mathbf x_1)/N(\mathbf x_2)$ in a $\phi$-well equals $c_{\text{in}}/c_{\text{out}}$ to FFT round-off, and *algebraically exactly* — tagged EXACT in `findings.md`.

**Decision point — proceed past T2.B PASS.**  The plan's primary gate (Shapiro tick-ratio matches global reading at $10^{-12}$) cleared at $10^{-16}$.  The emergent-time reading is consistent with v2 in the synchronous regime; T3 (Margolus async) remains optional and is currently parked.

**Findings.**

1. **Binary tick count vs phase-accumulation.**  The proposition's binary $\|\psi^{n+1} - \psi^n\| > \varepsilon$ counter is correct for vacuum freezing (T5.A) but cannot resolve the c(x) ratio for a wave-packet that touches every cell (FFT propagator with periodic BC).  The finer-grained operational tick — unwrapped phase advance / $2\pi$ — is what reproduces the c-ratio.  Both are consistent with the proposition's $N(\mathbf x)$ definition; the phase form is the *frequency-scale* count, the binary form is the *coarse-grained* count.  Recorded in `findings.md` as Finding 11.

2. **k_probe must be on the FFT grid.**  A plane wave at off-grid $k$ has spectral leakage across multiple Fourier bins; only on-grid $k = 2\pi m/L$ for integer $m$ gives a single-mode propagator action and exact phase advance $-c\cdot k$ per step.  T2.B fails by 0.66% off-grid; passes at $10^{-16}$ on-grid.

3. **`kg_step_free_2d_splitstep` is *not* the vacuum-fixed-point propagator.**  Φ=v is a fixed point of the full Mexican-hat propagator (`kg_step_strang` at `phase='broken'`) but *not* of the free KG step — free KG treats Φ as an oscillator at $\omega = m_h$, so the constant-v mode rotates.  T1's vacuum-freezing test must use the nonlinear Higgs stepper.

**Affected docs.**  `ca-emergent-time-proposition.md` (already had T4.A/T4.B sections from the T0 draft); `findings.md` (Finding 11 new); `project-status.md` (T0–T5 row added); `ca-reference.md` (T1/T2/T5 exactness rows added).

## 2026-05-18 (Dirac stepper — exact-QCA refactor, Finding 9)

Refactored `ca_dirac.py` from the linearized continuum Hamiltonian form $H_D = c\,\boldsymbol\alpha\cdot\mathbf k + m\,\beta$ to the exact QCA single-tick unitary of Paper 1 Eq. 23 combined with the 2D Weyl QCA of Paper 1 Eq. 16.  The `c` argument has been removed from every Dirac stepper signature — the kinetic coefficient is fixed at $n = \sqrt{1 - m^2}$ by the QCA admissibility constraint $n^2 + m^2 = 1$.

**Construction.**  Single-tick 4×4 unitary

$$D_k = \begin{pmatrix} n\,W_k & im\,I \\ im\,I & n\,W_k^\dagger \end{pmatrix},\qquad n^2 + m^2 = 1$$

where $W_k$ is `ca_core_exact.exact2d_unitary` and the lower-right block is $W_k^\dagger$ (not $W_{-k}$ as Finding 9 paraphrased — the $W^\dagger$ form is the one that closes the unitarity algebra; cross-block cancellations require $W' = W^\dagger$).  Eigenvalues $e^{\pm i\omega_k}$ with $\omega_k = \arccos(n\,c_x\,c_y)$, $c_i = \cos(k_i/\sqrt 2)$.  Arbitrary $dt$ via spectral interpolation $U_D(dt) = \cos(\omega\,dt)\,I + (\sin(\omega\,dt)/\sin\omega)\,(D_k - \cos\omega\,I)$.

**API surface removed.**  `c=` argument deleted from `dirac_step_2d_splitstep`, `dirac_step_u1_2d_splitstep`, `dirac_step_2d_varm_splitstep`, `dirac_step_2d_varm_complex_splitstep`, `verify_dirac_dispersion_2d`, `measure_zitterbewegung_freq_2d`, `aharonov_bohm_test`.  In `ca_unified.py` the `c` and `c_energy_unit` parameters are removed from `unified_step`, and `total_energy` derives $n_0 = \sqrt{1 - m_0^2}$ from $m_0 = y\,\text{mean}(\text{Re}\,\Phi)$ internally.

**Observable shifts.**  Zitterbewegung target moves from $2m$ to $2\arcsin(m)$.  At $m = 0.5$ that is $\pi/3 \approx 1.04720$ instead of $1.000$ — a 4.7% shift, easily resolvable above the FFT-bin floor.  Dirac dispersion at finite $|\mathbf k|$ is now BZ-periodic (bounded by $\pi$) instead of the unbounded continuum $\sqrt{(c k)^2 + m^2}$.

**Test results (all PASS at machine precision unless noted).**

| Check | Result | Tolerance |
|---|---|---|
| Unitarity $\|D^\dagger D - I\|_\infty$ across BZ | $1.11\times10^{-16}$ | machine ε |
| D1 dispersion residual (L=64, n_steps=20, m=0.3) | $3.94\times10^{-16}$ | $<10^{-13}$ |
| Norm drift (L=64, m=0.3, 200 steps) | $5.68\times10^{-14}$ | $<10^{-12}$ |
| D1 zitterbewegung (L=256, n_steps=2000, m=0.5) | $\omega = 1.04877$ vs $\pi/3 = 1.04720$ (0.15%, within FFT bin) | within FFT bin |
| D1 Weyl regression at $m=0$ (vs `weyl_step_2d_arccos_splitstep`) | bit-for-bit zero | machine ε |
| F1 vacuum regression ($\Phi=v$, η_diff vs constant-m Dirac) | $1.43\times10^{-15}$ | $<10^{-12}$ |
| F4 symmetric regression ($\Phi=0$, η vs exact-QCA Weyl) | bit-for-bit zero | machine ε |
| E1 Aharonov-Bohm phase pickup (L=128, π flux) | $4.44\times10^{-16}$ | machine ε |
| `varm_complex` at $m=0$ vs constant-m at $m=0$ | bit-for-bit zero | machine ε |

**Reference updates.**

- `run_phase_tests.py::test_D1` — Weyl regression at $m=0$ now compares against `ca_core_exact.weyl_step_2d_arccos_splitstep` (exact-QCA Weyl).  Zitterbewegung target updated to $2\arcsin(m)$.  Plot title now reads "$2\arcsin(m)$" rather than "$2mc^2$".
- `run_phase_tests.py::test_E3_continuity` — kinetic coefficient renamed `n_kin = 1.0` (was `c = 0.5`).  Added a note that the bilinear $\Psi^\dagger\alpha\Psi$ is the continuum current; under the exact-QCA the conserved current involves QCA-link bilinears, so Richardson convergence at $\mathcal O(dt^2)$ is not guaranteed and Richardson ratios will flag any breakage for follow-up.
- `run_phaseF_tests.py::test_F1` — drop `c=0.5` from reference Dirac and from `unified_step`.
- `run_phaseF_tests.py::test_F3` — drop `c_dirac` local; `total_energy` and `unified_step` no longer take `c`.
- `run_phaseF_tests.py::test_F4` — reference now uses `weyl_step_2d_arccos_splitstep` (Paper 1 Eq. 16) instead of `weyl_step_2d_splitstep`.
- `run_phaseF_tests.py::test_F_dt` — drop `c=0.5` from `unified_step` calls.

**Closes.**  Finding 9 (open since 2026-05-17).  V1 (exact-QCA dispersion, Dirac sector) and V3 (mass-parameter $n^2 + m^2 = 1$ audit) in `qca-papers-1-4-overview.md` follow once the doc is re-tightened.

**Does *not* close.**  3D-BCC Dirac stepper (no 3D code path touched).  Composite-photon / Paper 1 Eq. 35 derivation (V4).  DSR / Paper 4 boost map (V8) — that needs the deformation map $\mathcal D$ in addition to the exact dispersion that this refactor lands.

**Files changed.**  `ca-simulation/ca_dirac.py` (full rewrite), `ca-simulation/ca_unified.py` (drop `c` / `c_energy_unit` from `unified_step`; rebuild `total_energy` with $n_0$ derived from $m_0$), `ca-simulation/run_phase_tests.py` (D1, E1, E3), `ca-simulation/run_phaseF_tests.py` (F1, F3, F-dt, F4).

## 2026-05-17 (new design note — emergent-time roadmap)

Added `ca-emergent-time-plan.md`. Proposes a reinterpretation of the v2 stack in which the global update index $n$ is bookkeeping and physical time is the per-cell tick counter $N(\mathbf{x})$ of nontrivial state transitions. No code changes; design-only entry.

Six phases T0–T5. T0 is a proposition file; T1 is a lazy-update wrapper that increments $N$ only on cells whose state changes above an FFT-floor threshold; T2 re-derives group velocity, Shapiro delay, and redshift in tick language and checks equality against the global-$n$ derivation; T3 is the large optional item — partitioned (Margolus-style) BCC update with unitarity proven along causal sequences; T4 reformulates energy conservation and the Paper 4 DSR boost on tick-foliated frames; T5 lists falsifiable predictions unique to the tick reading (vacuum cells experiencing zero proper time exactly, lazy-run scaling with packet volume, asymmetric tick clocks as a direct probe of $\phi$).

First decision point is **after T2.B (Shapiro tick-ratio)**: if $|\Delta\tau_{\text{global}} - \Delta\tau_{\text{tick}}|/\Delta\tau_{\text{global}} < 10^{-12}$, the emergent-time reading is consistent with v2 and the rest proceeds. Otherwise the discrepancy itself is the new finding.

Preservation contract: every F-phase gate and every dimensionless lattice test must still pass at its current residual floor — the roadmap is additive, layering a second reading on the same propagator rather than replacing it. T3 is the only item that would touch the propagator itself, and is explicitly gated on T1+T2 succeeding first.

Affected docs (this entry only): `ca-emergent-time-plan.md` added; `project-status.md` Progress table extended.

## 2026-05-17 (decision point — SI identification of $(a,\tau)$ is currently undefined)

No code or test changes. Documents a decision the project has so far left implicit: the Weyl-QCA lattice light speed $c_\text{lat} = 1/\sqrt d$ is dimensionless (cells per tick), and converting any lattice quantity to SI requires committing to a specific lattice spacing $a$ in metres and tick duration $\tau$ in seconds. The naive choice $a = \ell_P$, $\tau = t_P$ predicts a measured speed of light $c_\text{physical} = c/\sqrt d$ — in 3D, that is $1.732 \times 10^{8}$ m/s, **0.5774× the observed $c$**, an exact $\sqrt 3$ shortfall.

Full analysis in `findings.md` Finding 10. The mismatch traces to a definitional consequence of Planck units ($\ell_P/t_P = c$ exactly), not to any numerical residual. Three internally consistent resolutions, mutually exclusive:

1. Keep $a = \ell_P$, set $\tau = t_P/\sqrt d$ (tick smaller than Planck time by $\sqrt d$).
2. Keep $\tau = t_P$, set $a = \ell_P\sqrt d$ (cell larger than Planck length by $\sqrt d$).
3. Reinterpret $a/\tau$ as the lattice lightcone (maximum signal speed = $c\sqrt d$), with physical $c \equiv (a/\tau)/\sqrt d$ being what particles propagate at. Retires the convention $\ell_P/t_P = c$.

Status of existing tests: **all 30/30 dimensionless lattice tests are unaffected** — they live in lattice units and never invoke $a$ or $\tau$. The $\sqrt d$ factor enters only at the SI conversion boundary. Specifically: L1–L4 unitarity, dispersion residuals, norm drift; F1–F4 unification gates; D1/E1/E2 phase tests; and the 8-row exact-algebraic inventory in `ca-reference.md` are all dimensionally pure.

What this rules in / out for future work:

- Any future lattice-to-SI absolute-magnitude calculation must declare which of the three resolutions is in force.
- Finding 8's L4 lensing absolute-coefficient extension (currently checking only the ratio $\Delta(2M)/\Delta(M) \to 2$ within $3.5\times 10^{-3}$) acquires an explicit $\sqrt d$ factor when implemented.
- F3b deflection magnitude in cells does not need an immediate decision; the $1/b$ scaling test (item 12) is dimensionally pure.
- No code change is required *now*; the decision is logged so the next person mapping a lattice number to a SI prediction does not silently pick a resolution.

Affected docs (this entry only): `findings.md` Finding 10 added; `ca-reference.md` exactness table updated with $c_\text{lat} = 1/\sqrt d$ and the SI-mapping $\sqrt d$ factor; `ca-reference.md` "Current limitations" extended with the SI-identification flag.

## 2026-05-17 (new design note — electroweak mass-generation paths)

Added `ca-electroweak-design.md`. Re-organizes content already in `ca-unified-v2.md` into three named mass-generation paths and compares each against the three-mass framework in `ostoma-trushyk-1999-summary.md` §7. No code or test changes.

Three v2 paths identified: **A** = Yukawa $m_{\text{eff}} = y\,\text{Re}(\Phi)$ (S4, F1/F2/F4 gates, zero new engineering); **B** = total stress-energy sourcing the EMQG potential $\phi$ via Paper 6 Eq. 19.7 (S1, V11/V12/F3b gates, ~1 week engineering on a time-dependent Poisson solver — flagged as v2's largest implementation risk); **C** = composite-photon $E/c^2$ effective mass via Paper 1 Eq. 35 (S3, V4/E1 gates, ~4–6 days for new `ca_maxwell.py`).

Mapping to OT: Path B ↔ OT gravitational mass $m_g$ (direct correspondence — same modified Poisson equation). Path C ↔ OT inertial mass $m_i$ (partial — same observables, but v2 has lattice photons without the masseon/charged-virtual-vacuum that QI requires). Path A ↔ no OT analog (OT has no Higgs scalar; rest mass in OT emerges from EM-vacuum coupling, not a fundamental scalar). OT's low-level "mass charge" has no v2 analog — v2 has no gravitons, so the subdominant gravity channel and the predicted $10^{-40}$ WEP violation are absent. v2 collapses OT's "$m_g$ = photon-vacuum part + graviton-mass-charge part" into a single stress-energy → $\phi$ source.

## 2026-05-16 (model-observations items 1–5 — substantive fixes)

Substantive items from `model-observations.md` cleared.

**Item 1 — `ca-unified-v2.md` lines 46–50: c(φ) sign.** Replaced $c = c_0(1+\phi/c_0^2)^{-1}$ "Paper 6 Eq. 18.31 reduction" with the GR-Shapiro form $c = c_0/(1-2\phi/c_0^2)$ that the working `ca_emqg.py::c_field_from_phi` already uses. Added an inline note explaining the wrong-sign / wrong-citation history so the doc can no longer mislead anyone re-implementing from it.

**Item 2 — `ca-unified-proposition.md` line 69: $(-\alpha)$ exponent retired.** Marked the entire Coupling-2 section RETIRED with a callout pointing readers to `ca-unified-v2.md` §S1 (the Poisson-sourced EMQG replacement). Kept the historical formula in-place but explicitly tagged "v1 — RETIRED."

**Item 3 — Dirac mass-convention refactor: c into the kinetic generator only.** Changed `H_D = c·α·k + m·c²·β` → `H_D = c·α·k + m·β` everywhere in the code:
- `ca_dirac.py`: `dirac_step_2d_splitstep`, `verify_dirac_dispersion_2d`, `_dirac_helicity_plus_eigenvector`, `measure_zitterbewegung_freq_2d`, `dirac_step_2d_varm_splitstep`, `dirac_step_2d_varm_complex_splitstep`. Eigenvalue formula now $E = \sqrt{(c|k|)^2 + m^2}$; per-cell mass-mode mix angle is $m\cdot dt$ (was $m\cdot c^2\cdot dt$).
- `ca_weak.py::step_weak_2d`: electron mass mixing phase is now $m_e\cdot dt$.
- `ca_unified.py`: symplectic Yukawa Pi-kick is now $-y\cdot \chi^\dagger\eta\cdot dt$ (no $c^2$). `total_energy` drops the $c^2$ from $H_Y$. Docstring updated.

The `m` parameter user-meaning is now **rest energy** (was implicitly $m\cdot c^2$ before). F1 and F4 still pass at machine precision because they are consistency tests — both reference and unified paths use the new convention. D1 dispersion test now matches numerical to the new analytic $E$ formula at $1.2\times 10^{-16}$. Zitterbewegung frequency is now $2m$ (was $2mc^2$), with the analytic comparison updated correspondingly. Variable-mass equivalence (`dirac_step_2d_varm_splitstep` and `_complex_splitstep` reduce to constant-m bit-for-bit when m_field is uniform) verified.

Practical impact for users comparing to SM Yukawa: the lattice coupling $y$ no longer requires a $c^2$ rescaling to compare to published values; with $c=1$ (natural units) it is directly the SM coupling.

**Item 4 — 3-D Newtonian lensing test (replaces 2-D log-potential).** Added `solve_poisson_3d` and `gaussian_mass_3d` to `ca_emqg.py`, plus `test_lensing_deflection_3d` (and `test_point_source_potential_3d`). The 3-D solver produces the true $1/r$ Green's function; slicing at $z=L/2$ gives a planar $\phi(x,y)$ that the existing Cayley variable-c stepper can propagate through. The new pass criterion is the dimensionally consistent **linear-in-M** Newtonian scaling: $|\Delta(2M)/\Delta(M) - 2| < 0.10$. Measured at L=64: $3.5\times 10^{-3}$ — within 0.35% of the Newtonian benchmark, **a 26× improvement** over the prior 8.5% 2-D number (which was scoring a logarithmic potential against a linear-M benchmark). The old `test_lensing_deflection` is kept as L4.c INFO for backward reference; L4.d is now the headline lensing pass. L4.e adds the 3-D Poisson discrete contract $\nabla^2\phi=4\pi G\rho$ check (rel err $1.3\%$ at L=64 with $\sigma=4$).

**Item 5 — L3 split into L3a (kinematic) and L3b (curl, PARTIAL).** Refactored `run_L_tests.py::test_L3` into:
- `test_L3a` — dispersion + transversality + anisotropy. Reports PASS/FAIL normally. All three sub-tests pass cleanly.
- `test_L3b` — Maxwell curl residual. Reports INFO/PARTIAL; the residual is $O(k)$ rather than $O(k^3)$ because the smeared-photon construction has not landed. Not part of the PASS/FAIL totals.

The legacy `test_L3` is kept as an alias to `test_L3a` so external callers don't break. The driver now prints `L3a STATUS: PASS (kinematic)` and `L3b STATUS: PARTIAL (Maxwell curl residual is O(k))`. This ends the misleading "3/3 PASS + 1 INFO" framing that hid the central Maxwell identity failure.

| Item | Files touched | Result |
|---|---|---|
| 1 | `ca-unified-v2.md` | Doc back-fix; code already correct |
| 2 | `ca-unified-proposition.md` | v1 §Coupling-2 retired; pointer added to v2 §S1 |
| 3 | `ca_dirac.py`, `ca_weak.py`, `ca_unified.py` | F1/F4 machine-precision unchanged; SM-clean H_Y |
| 4 | `ca_emqg.py`, `run_L_tests.py` | L4.d: linear-M scaling 0.35% (was 8.5%) |
| 5 | `run_L_tests.py` | L3a PASS 3/3; L3b PARTIAL INFO |

## 2026-05-16 (model-observations items 8–14 — clarifying refactors + new tests)

Worked through items 8 through 14 of `model-observations.md` as clarifying improvements (no physics change to the existing passing tests).

**Item 8 — Higgs API: explicit `phase` flag.** `ca_higgs.py::kg_step_strang`, `kg_nonlinear_kick`, and `_force` now take a `phase ∈ {'broken','symmetric'}` keyword.  `mu2` is the *magnitude* μ²≥0 in both cases; the sign of the quadratic term is set by `phase`.  `ca_unified.py::unified_step` propagates `phase` through and accepts the explicit kwarg.  F4 was migrated from the `mu2=-0.5` sign-flip kludge to `mu2=0.5, phase='symmetric'`.  Legacy callers passing negative mu2 still work (negative mu2 + default phase is auto-interpreted as symmetric).  Validated: F1-like (broken), F4-like (symmetric), and legacy paths all match at machine precision at L=32.

**Item 9 — `ca_maxwell.py` placeholder removed.** Deleted the immediately-overwritten `bcc.bcc_unitary(...)` assignment at line 171 in `maxwell_curl_residual`.  Residual at k=0.05 unchanged: 2.05e-2.

**Item 10 — Paper 1 Eq. 15 sign typo back-fixed in overview doc.** `qca-papers-1-4-overview.md` line 53: second term of $\tilde n_y$ flipped from `-` to `+` to match the corrected sign verified in `ca_bcc.py::_bcc_uvec`.  Inline note added pointing to `findings.md` Finding 1.  `ca_bcc.py` module docstring also corrected to match the working code.

**Item 11 — Overloaded `c` disambiguated via parameter aliases.** Added non-breaking kwargs so call sites can be explicit about which of the three meanings of "c" is intended: `weyl_step_2d_splitstep(..., c_unitary=…)` (unitary rotation per tick), `c_field_from_phi(..., c_macro=…)` (macroscopic light-speed), `unified_step(..., c_energy_unit=…)` (energy unit in H_Y).  Legacy `c=` / `c_0=` continue to work; aliases are documented in each docstring.  Verified all three aliases match the legacy form at machine precision.

**Item 12 — F3b 1/b deflection scan.** New `test_F3b_scan` in `run_phaseF_tests.py` runs `_f3b_run_at_offset` at impact parameter $b\in\{40,60,80,110,150\}$ on a lean lattice (L=192, n_steps=160, σ_phi=15, σ_pk=14) all comfortably in the far-field $b > 2\sigma_\Phi$.  Pass criteria: deflection negative at every $b$, power-law slope $m$ in $\log|\Delta y|$ vs $\log b$ within $\pm 0.4$ of $-1$, norm preserved to machine precision.  Single-run sanity check at L=192 gives Δy=−0.376 cells, norm drift 1.0e-14.

**Item 13 — Strang-composition O(dt²) convergence test.** New `test_dt_convergence` in `run_phaseF_tests.py` runs `unified_step` over fixed total time T=8 at dt ∈ {1.0, 0.5, 0.25}, measures the Richardson ratio
$$r = \frac{\|\Psi(\Delta t)-\Psi(\Delta t/2)\|}{\|\Psi(\Delta t/2)-\Psi(\Delta t/4)\|}$$
and passes if $r \in [3.0, 5.5]$.  Measured $r = 4.07$ — clean second-order convergence.  This is the first dt-scan in the suite; targets the order-of-accuracy bug class that the unconditionally-stable propagator otherwise masks.

**Item 14 — Discrete Noether current conservation (U(1) and SU(2)).** New `test_E3_continuity` in `run_phase_tests.py`.  Two sub-tests:

  (a) U(1)-coupled stepper: compute $\rho(x)$ and $J^i(x)$ from the Dirac chiral-basis bilinears, take the lattice central-difference divergence, and check the residual $\rho(t+\Delta t) - \rho(t) + \Delta t\cdot c\cdot\nabla\!\cdot\!J$ at three dt's (0.20, 0.10, 0.05).  Richardson ratios 4.05 and 4.01 — residual is exactly $O(\Delta t^2)$, i.e. the Dirac CA satisfies the discrete continuity identity at the order of the integrator.

  (b) SU(2)-coupled stepper: the isospin rotation moves charge between ν and e components.  Total local $\rho = |\eta_\nu|^2 + |\eta_e|^2 + |\chi_e|^2$ should be invariant pointwise.  Measured drift 4.4e-16 — exact at machine precision.

Combined, (a) and (b) verify the *local* (per-cell) discrete Noether identity that previous tests only verified in *integrated* form.

| Item | Files touched | Tests added/changed |
|---|---|---|
| 8  | `ca_higgs.py`, `ca_unified.py`, `run_phaseF_tests.py` | F4 migrated to explicit API |
| 9  | `ca_maxwell.py` | curl residual unchanged |
| 10 | `qca-papers-1-4-overview.md`, `ca_bcc.py` | none |
| 11 | `ca_core.py`, `ca_emqg.py`, `ca_unified.py` | none |
| 12 | `run_phaseF_tests.py` | + `test_F3b_scan` |
| 13 | `run_phaseF_tests.py` | + `test_dt_convergence` |
| 14 | `run_phase_tests.py` | + `test_E3_continuity` |

## 2026-05-16 (1/√6 origin — 2D-square test resolves the candidate question)

### New module: `ca_maxwell_2d.py` (composite-photon bilinear on the 2D Paper 1 Eq. 16 QCA)

Built to discriminate between three hypotheses for the leading curl-residual constant $1/\sqrt 6$ measured on the BCC lattice (`findings.md` Finding 7):

- Candidate A — neighbour-pair counting: $1/\sqrt{C(z,2)}$ with $z=4$ → predicts $1/\sqrt 6 = 0.408$ on **both** BCC and 2D-square (both have $z=4$ neighbours).
- Candidate B — dimensionality $\times$ bilinear norm: $1/\sqrt{2d}$ → predicts $1/\sqrt 6 = 0.408$ on BCC ($d=3$) and $1/2 = 0.500$ on 2D-square ($d=2$).
- Candidate C — tetrahedral half-angle: $\cos(\theta_\text{tet}/2)/\sqrt 2$ → predicts $1/\sqrt 6$ on BCC; not applicable on 2D-square.

`ca_maxwell_2d.py` ports the BCC composite-photon construction (`weyl_eigenmodes_*`, `bilinear_G`, `EM_bilinears`, `maxwell_curl_residual_*`) to 2D-square. The 2D Weyl unitary has a nonzero $\sigma_z$ component ($n_z = s_x s_y$), so the bilinear $G^i = \psi^T \sigma^i \psi$ is still a 3-vector and the cross-product structure of the Maxwell curl equation is unchanged. Only the lattice and the $n(k/2)$ profile differ.

**Measured 2D-square curl/k over $|k| \in \{10^{-5},10^{-4},10^{-3},10^{-2}\}$:**

| $\|k\|$ | curl/k (2D) | $\Delta$ vs $1/2$ |
|---|---|---|
| $10^{-5}$ | $0.5000000000$ | $+3.2\times 10^{-11}$ |
| $10^{-4}$ | $0.5000000000$ | $-4.7\times 10^{-11}$ |
| $10^{-3}$ | $0.4999999896$ | $-1.04\times 10^{-8}$ |
| $10^{-2}$ | $0.4999989580$ | $-1.04\times 10^{-6}$ |

Resolution: **curl/k → 1/2 to 10 decimal places**, 22% off the Candidate A prediction. **Candidate A is falsified; Candidate B is confirmed.** The constant is $1/\sqrt{2d}$ where $d$ is the lattice dimensionality, not a neighbour-pair-counting quantity.

The BCC measurement's apparent match to Candidate A was a numerical coincidence: $C(4,2) = 6 = 2\cdot d$ when $d=3$, and the regular tetrahedron's half-angle cosine is $1/\sqrt 3 = c_\text{lat,3D}$. None of these are causal — moving to $d=2$ with the same $z=4$ moves the constant cleanly to $1/2$.

**Subleading coefficient also dimensionality-driven:**

- 3D BCC: $\text{curl}/k = 1/\sqrt 6 + 0.01883\,k + \mathcal O(k^2)$ (linear-in-k correction)
- 2D square: $\text{curl}/k = 1/2 - 0.0104\,k^2 + \mathcal O(k^3)$ (quadratic-in-k correction)

The k-power of the correction mirrors the lattice dispersion's k-power: BCC has an $\mathcal O(k)$ dispersion correction along $(1,1,1)$ (Paper 4 Eq. 23); 2D arccos has only $\mathcal O(k^2)$ corrections in all directions. So the curl-correction starts at $k$ in 3D BCC and at $k^2$ in 2D square. Algebraic origins of $0.01883$ and $-0.0104$ are open.

**Sanity checks on 2D-square pass:**
- Dispersion residual: $4.71\times 10^{-9}$ at $k=10^{-3}$, scales as $\mathcal O(k^2)$.
- Transversality: $5\times 10^{-19}$ to $1.8\times 10^{-17}$ — machine zero.

**Exactness inventory updated** with new exact-algebraic line: *Composite-photon curl-residual leading coefficient = $1/\sqrt{2d}$*. Validated on $d=2$ (2D-square) to 10 decimals and $d=3$ (BCC) to 7 figures. New lattice tests (FCC, 4D hyperdiamond, 2D triangular) would add data points but are not currently scoped.

### Files updated
- `ca-simulation/ca_maxwell_2d.py` — new (~170 lines).
- `findings.md` — Finding 7 gets a "Resolution" section with the measurement table and verdict.
- `ca-reference.md` — exactness inventory entry promoted from open question to closed-form $1/\sqrt{2d}$.
- `changelog.md` — this entry.

## 2026-05-16 (10× test execution pass)

### Fresh runs at 10× scaled parameters — data and matches to existing formulas

Per CLAUDE.md preference for exact equations vs machine-precision results, the 10× lattice/parameter bumps applied earlier today (see "10× lattice-resolution bump across the test suite") were executed for the tests that fit in memory, plus a 10× scan of the L3 curl residual in $|k|$ and a 10× bump on the D1 zitterbewegung step count. Outcomes:

**L1 — BCC unitarity, dispersion, small-k Weyl regression.** Survives the 10× bump bit-for-bit:
- L1.a unitarity: $\max |u^2+|n|^2 - 1| = 6.34\times 10^{-16}$ both helicities.
- L1.b $A_0 = I$ at $k=0$: exact ($U_+[0]=U_-[0]=1.0$).
- L1.c analytic vs measured dispersion: $7.22\times 10^{-16}$.
- L1.e small-k Weyl regression at $|k|=0.005$: $4.96\times 10^{-4}$ (unchanged; residual is a property of k, not L).
- L1.d norm drift scanned at $L\in\{40,80,120\}$, 200 steps: 8.6e-14, 4.7e-14, 6.2e-14 — all at the FFT round-off floor. Full $L=160$ run requires ~5 min wall time per direction; not completed in the available budget but the trend is established.

**L2 — Exact-arccos 2D Weyl.** Norm drift at L=320, n=200: $7.64\times 10^{-14}$; at n=2000 (extra 10× on steps): $7.63\times 10^{-13}$. Ratio = $9.985$ — **exact 10× per-step linear scaling**, confirming per-step drift = 1 ulp of complex128 with no algorithmic growth.

**L3 — composite-photon curl-residual 10× k-scan.** $|k| \in \{10^{-5},10^{-4},10^{-3},10^{-2}\}$. The curl/k constant converges to $1/\sqrt 6 = 0.408248290\ldots$ to 7 significant figures at $k=10^{-5}$, with leading correction $\Delta \approx 1.883\times 10^{-2}\cdot k$. The constant $1/\sqrt 6$ is now the **exact algebraic leading coefficient** of the BCC pointwise-bilinear Maxwell-curl residual (Findings 2 update).

**L4 — EMQG modified Poisson.** L4.a rel err: $1.39\%$ at L=640, σ=30 (prior $2.75\%$ at L=64, σ=3 with the same σ/L ratio) — modest 2× improvement from the finer k-grid. L4.b vacuum c=c_0 exact. L4.c at L=1280 requires ~10 GB Cayley LU; not executed.

**Phase D1 — Dirac CA.**
- Weyl regression at m=0, L=320: $1.55\times 10^{-15}$ (prior L=32: $5.10\times 10^{-16}$; 3× looser, consistent with $\sqrt{N_\text{cells}}$ scaling).
- Norm drift 1000 steps, m=0.3, L=320: $3.98\times 10^{-13}$ (prior L=32: $3.42\times 10^{-14}$; 11.6× looser).
- Dispersion residual at L=320: $1.28\times 10^{-17}$ (machine zero; slightly tighter than prior $8.88\times 10^{-17}$).
- **Zitterbewegung at 10× n_steps (5000→50000), L=48 σ=10**: rel err drops 3.53% → **0.026%**, FFT bin drops 5×. 135× improvement in error from 10× more steps confirms prior 3.53% was FFT-bin-limited, not physical (Findings 6).

**Phase B1 — group velocity at L=640, σ=80.** speed_ratio at k0=(0.3,0): 0.99946; at k0=(0.6,0): 0.99987. Prior L=128 σ=8: 0.92–0.98. Wider packet sharpens the centroid measurement; $v_g = c\hat k$ holds tighter at 10× σ.

**Phase E1 — Aharonov-Bohm at L=640.** Phase pickup err = $4.44\times 10^{-16}$ (identical to prior; eigenvalue-phase floor). |overlap| = 1.0 to 12 decimals. Norm drift with A0: $4.29\times 10^{-10}$ (prior $3.58\times 10^{-12}$; 120× looser, consistent with $\sqrt N$ FFT roundoff over 100 steps).

**Phase E2 — SU(2) parity at L=320.** measured left_e_pop = 0.35528551 vs analytic 0.35528551 — 8 decimals. Right leakage = 0.0 exact.

**Phase F1 — vacuum regression at L=320: DIVERGES with default n_phi_sub=1, PASSES with n_phi_sub=2.** New finding documented in `findings.md` Finding 4. The KG velocity-Verlet stepper is CFL-bounded: $dt_\text{sub} < 2/\sqrt{8+2\mu^2} \approx 0.667$ in 2D with $\mu^2 = 0.5$. With `dt=1.0, n_phi_sub=1` the effective sub-step violates the bound; at L=32 the noise doesn't grow fast enough to show, but at L=320 the dense spectrum diverges within 100 steps. With `n_phi_sub=2` (dt_sub=0.5), $\|\Phi-v\|=1.44\times 10^{-15}$, fermion diff $=2.16\times 10^{-15}$ — F1 passes at machine precision. Empirical critical dt at L=320 lies between 0.85 and 0.95 (CFL is the safe lower bound).

**Phase F2 — Higgs+Goldstone at L=640.** Higgs radial residual: $1.00\times 10^{-3}$ (prior $1.06\times 10^{-3}$; O(dt²) Verlet error, not L-limited). **Goldstone residual scales as exactly machine epsilon times $|k|$**: residual/(|k|·ε) ≤ 0.88 for every mode — promotes Goldstone-massless from "0.04% precision" to **exact algebraic result** (`findings.md` Finding 3). New entry to the exactness inventory.

**Phase F3 — symplectic Yukawa back-reaction at L=320 (sub-scaled, n_phi_sub=2).** $\|\Phi-v\| \in [0.59, 0.74]$ in 200 steps (prior L=64: 0.66–0.73). Total energy drift $H_\text{rel} = 0.0002\%$. Symplectic contract holds at 10× lattice.

**Phase F4 — symmetry restored at L=320.** $|\Phi|_\text{max} = 0.0$ exact, η match diff = $2.33\times 10^{-15}$, χ max = $0.0$. Bit-for-bit identity test survives the bump.

**Not executed (sandbox memory ~3.4 GB):** F3b at L=960 (Cayley LU ≈ 5 GB), L4.c lensing at L=1280 (≈ 10 GB), C1 Cayley arm at L=1280, L1.d 3D L=160 full run.

### Match to existing formulas

The "match to a known formula or data point" results from the 10× variation:

| Result | Existing formula matched | Match quality |
|---|---|---|
| Curl residual / k → $1/\sqrt 6$ | $1/\sqrt 6 = 0.408248290\ldots$ (BCC geometry constant) | 7 significant figures at $k=10^{-5}$ |
| Goldstone residual ≤ $|k|\cdot\varepsilon$ | Goldstone theorem (exactly massless) | sub-ulp per |k| at L=640 |
| D1 / L2 norm-drift / step ≈ $\varepsilon_\text{double}$ | FFT round-off floor (standard error analysis) | 1 ulp/step, linear in n |
| F1 stability boundary at $dt_\text{sub} \approx 2/\sqrt{8+2\mu^2}$ | Explicit-Verlet CFL on 5-point Laplacian | empirical critical dt is the safe upper bound; CFL is a conservative lower bound |
| Zitterbewegung freq → $2mc^2$ at 10× steps | Dirac equation prediction | 0.026% at 50000 steps; converges as FFT bin width allows |

No data matched an imaginary-number approximation in the sense suggested by the prompt example. All matches that emerged are real-valued algebraic constants ($1/\sqrt 6$, $\varepsilon_\text{double}$, the CFL bound, $2mc^2$).

### Files updated
- `findings.md` — added Findings 3–6; updated Finding 2 with 10× k-scan.
- `changelog.md` — this entry.
- `ca-reference.md` — exactness inventory gains Goldstone-massless and CFL-bound rows.
- `project-status.md` — appended a "10× test execution pass" subsection.

## 2026-05-15 (v2 layered build)

### L1–L4 v2 layered build implemented and tested
- **New files:** `ca-simulation/ca_bcc.py` (L1, ~210 lines), `ca-simulation/ca_core_exact.py` (L2, ~150 lines), `ca-simulation/ca_maxwell.py` (L3, ~220 lines), `ca-simulation/ca_emqg.py` (L4, ~165 lines), `ca-simulation/run_L_tests.py` (~210 lines, gates between layers).
- **What:** the four-layer v2 stack from `ca-unified-v2.md` landed end-to-end in one session, with explicit pass gates between layers.

#### L1 — BCC + exact arccos dispersion (Paper 1 Eq. 15)
- Implemented as a Fourier-space diagonal unitary `U(k) = u(k)·I − iσ·ñ(k)` per Paper 1 Eq. 15. One CA tick = one application of `U`; norm is conserved by construction (FFT round-off floor only).
- **Discovery:** the formula transcribed in `qca-papers-1-4-overview.md` line 53 had a sign typo on the second term of `ñ_y`. Direct verification: `u² + |n|² = 0.47` off unity at finite k with the transcribed sign; `4.4e-16` off with the corrected sign `ñ_y^± = ∓ c_x s_y c_z + s_x c_y s_z`. Code carries the fix with an inline note; reference doc still needs back-fixing.
- **Tests:** unitarity 7.9e-16 across BZ; A_0=I exact at k=0 (Paper 2's V7 constraint); analytic ω=measured eigenvalue phase to 7.2e-16; norm drift 3.7e-14 over 200 steps on a 16³ random spinor; small-k Weyl regression rel err 5e-4 at |k|=0.005 (scales as O(|k|²)).

#### L2 — Exact arccos in 2D (Paper 1 Eq. 16)
- `ca_core_exact.py::weyl_step_2d_arccos_splitstep` — the 2D square-lattice analog. Coexists with the existing linearized `weyl_step_2d_splitstep`; the new module is opt-in. 2D form is unitary by inspection: u² + |n|² = c_x²c_y² + s_x²c_y² + c_x²s_y² + s_x²s_y² = (c_x²+s_x²)(c_y²+s_y²) = 1 — no typo to fix.
- **Tests:** unitarity 3.2e-16 across BZ, A_0=I at k=0, norm drift 8.4e-15 over 200 steps on 32×32. **Frequency-dependent c measured:** Δc/c = −1.13% at |k|=0.5 along the (1,1) diagonal, machine zero along (1,0) — confirms Paper 4 Eq. 23's anisotropic prediction (V5 test in the literature reference).

#### L3 — Composite photon (Paper 1 Eq. 35)
- `ca_maxwell.py::weyl_eigenmodes_3d_bcc` extracts the two energy eigenmodes of `U(k)` at a chosen k by direct diagonalisation. `bilinear_G(psi, phi) = φ^T σ ψ` builds the σ^i bilinears (note: `φ^T`, transpose-not-conjugate, per the De Broglie photon construction). `EM_bilinears` computes `E_G = |n|(G_T + G_T†)`, `B_G = i|n|(G_T† − G_T)` after projecting out the longitudinal-to-2n̂ component.
- **Tests passing:** composite-photon dispersion `Ω_γ = 2ω(k/2) → |k|/√3` to 0.21% at |k|=0.05; transversality `2ñ·E_G = 2ñ·B_G = 0` to 4.6e-17.
- **Anisotropy verified analytically:** along (1,0,0) the dispersion is exactly `Ω_γ = k/√3` (residual 3.8e-15 — machine zero); along (1,1,1) the leading correction is `k/18` from the `sin·sin·sin` term in u(k/2), giving rel err 2.79e-3 at k=0.05. Both match the closed-form expansion.
- **Curl-equation residual is INFO only.** Paper 1 Eq. 35's `∂_t E_G = i·2ñ × B_G` holds for the *smeared* photon construction (Paper 1 lines 84-90, smearing function f_k(q)). For the pointwise bilinear used here, the curl residual scales as O(k) rather than the O(k³) expected for the smeared form — 2% at k=0.05, 0.04% at k=0.001. Documented as a known limitation; the full smeared-photon test is deferred research.

#### L4 — EMQG modified Poisson + c(φ) (Paper 6 Eq. 19.7)
- `ca_emqg.py::solve_poisson_2d` solves `∇²φ = 4πGρ` on the periodic lattice via FFT (`φ(k) = −4πGρ(k)/|k|²`, gauge `φ(k=0) = 0`). Static only; time-dependent retarded Poisson is future work.
- `c_field_from_phi` builds the position-dependent light speed. **Sign correction vs the v2 proposition:** the doc had `c = c_0/(1 + φ/c_0²)`, which with φ<0 in a well gives c>c_0 — light speeds up in the gravity well, opposite to GR lensing direction. Corrected to the GR-effective-medium form `c = c_0/(1 − 2φ/c_0²)`, which gives c<c_0 in the well and the right deflection direction. At |φ| ≪ c_0² this is `c ≈ c_0(1 + 2φ/c_0²)`, the leading-order Shapiro form, giving 4GM/(bc²) deflection.
- **Tests passing:** static Poisson recovers `∇²φ = 4πGρ` to 2.75% at L=64; vacuum ρ=0 → c=c_0 exactly (0.0 residual); **lensing demo** — Weyl probe at impact parameter b=18 deflects 0.6 cells toward a mass at the lattice centre, and doubling the mass gives 1.83× the deflection (8.5% off the expected 2.0 — within tolerance for a 128×128 grid at finite Δt).

#### Fresh full-suite regression (2026-05-15)
- `run_phase_tests.py`: **8/8 PASS**. All residuals identical to the 2026-05-14 baseline. D1 dispersion 8.88e-17, E1 phase pickup 4.44e-16, E2 right leakage = 0.0.
- `run_phaseF_tests.py`: **5/5 PASS**. All residuals identical. F1 fermion diff 8.41e-16, F2 dispersion 0.106%, F3 bounded |Φ−v| ≤ 0.73, F3b deflection −6.6 cells with norm drift 1.1e-15, F4 η match 7.57e-16.
- `run_L_tests.py`: **L1 6/6, L2 5/5, L3 3/3 + 1 info, L4 3/3 — all four layers PASS.**
- **Total across all three runners: 30/30 hard tests pass, 0 fail, 1 info note (L3 curl).**

#### What this *does* and *doesn't* establish
- ✓ The BCC lattice + exact arccos dispersion is a working substrate. The Paper 1 / Paper 2 small-k Weyl regression holds at machine precision; the lattice corrections at higher |k| are the published Paper 4 Eq. 23 ones.
- ✓ Frequency-dependent c is now an *observed* lattice property in the test suite, not just a theoretical claim.
- ✓ A photon-like composite object with the correct dispersion ω = |k|/√3 and transverse polarization exists on the BCC lattice as a Weyl-pair bilinear.
- ✓ A static Poisson solver coupled to the existing Cayley variable-c stepper produces qualitative Newtonian-style lensing with correct sign and approximately-linear mass-scaling.
- ✗ The composite photon's full Maxwell curl-equation closure is *not* established at the published O(k³) bound; only the dispersion and transversality pieces are. The smeared-photon construction needed for the curl is research-grade work, deferred.
- ✗ The Poisson solver is static; time-dependent retarded gravity (Paper 6 Eq. 19.6 / 19.7 with the ∂_t² term) is not implemented. F3b's static depression demo and L4's static-mass lensing are consistent in that they both ignore the retardation term.
- ✗ The L4 lensing scaling 1.83 vs 2.0 (8.5% error) is good enough to confirm direction and approximate magnitude, but not precise enough to claim a published Newtonian Δθ = 2GM/bc² match — that would need a higher-resolution lattice and a more careful integration of the photon trajectory.

## 2026-05-15 (latest)

### Drafted unification proposition v2
- **Files:** `ca-unified-v2.md` (new); `project-status.md` (progress table row + Next-Steps bullet); this changelog entry.
- **What v2 changes from v1:** v1 (`ca-unified-proposition.md`) had one scalar Φ doing two jobs — Yukawa fermion mass *and* metric coupling $c \propto |\Phi|^{-\alpha}$. v2 keeps the v1 per-cell phase / Strang architecture and the Higgs Yukawa unchanged, but routes the metric coupling through a second field: the EMQG vacuum potential $\phi$ that solves Paper 6 Eq. 19.7 ($\nabla^2\phi - c_0^{-2}\partial_t^2\phi = 4\pi G\rho_{\text{tot}}$) with $\rho_{\text{tot}}$ summing Φ stress-energy and fermion stress-energy. Then $c(\mathbf{x}) = c_0(1 + \phi/c_0^2)^{-1}$ feeds the existing Cayley variable-$c$ stepper.
- **Four-layer stack:** L1 BCC substrate + exact arccos dispersion (Papers 1, 2); L2 Weyl/Dirac with exact $\omega_\mathbf{k}$ option (Papers 1, 4); L3 composite-photon U(1) (Paper 1 Eq. 35) + existing SU(2) and Φ; L4 EMQG modified Poisson sourcing $c(\mathbf{x})$ (Paper 6).
- **Why this is an improvement over v1:** (i) the v1 free parameter $\alpha$ is replaced by the measured Newton constant $G$; (ii) the v1 sign inconsistency between the published $c \propto |\Phi|^{-\alpha}$ and the F3b lensing demo (which needed the flipped exponent) goes away — the EMQG sign is unambiguous; (iii) fermion density couples directly to $\phi$ rather than only indirectly through Φ shifting first; (iv) closes the largest v1 architectural gap by adding a genuine composite-photon Maxwell sector (current v1 has only an external classical $A_\mu$).
- **Preservation contract:** every existing passing test (8 Phase A–E + 5 Phase F including F3b) is the gate for a specific limit of v2 (Φ=v, $\rho_{\text{tot}}=0$, $|\mathbf{k}|\to 0$, photon coherence enforced by hand). Nothing breaks; new tests are gained.
- **Build sequence recommended:** V4 composite photon (Paper 1 Eq. 35; new `ca_maxwell.py`, 4–6 days); V11 EMQG modified Poisson + Cayley $c(\phi)$ (1 week); V12 gravitational redshift from linear $c(z)$ (2–3 days); V6 BCC 3D substrate (1–2 weeks); V1/V5 exact arccos in 2D (2–3 days); V2 Klein paradox (2 days); V3/V7 audits (½ day).
- **Caveats called out:** EMQG is a physics essay, not a derivation (Paper 6 motivates Eq. 19.7 from the Fizeau analog, not from informational axioms); the time-dependent lattice Poisson solver is new engineering and is the largest implementation risk; composite-photon coherence under interactions is non-trivial; WEP violation at $10^{-40}$ remains unfalsifiable in float64.

## 2026-05-15 (later in day)

### Added Paper 6 (Ostoma & Trushyk full treatise) to research overview
- **Files:** `qca-papers-1-4-overview.md` (Paper 6 section added; synthesis table rows for inertia / gravity / equivalence / redshift / field equation / cosmology added; comparison section's variable-$c$ paragraph extended with Paper-6 link; tests V11 EMQG modified-Poisson regression, V12 gravitational redshift from variable-$c$, V13 WEP-violation order-of-magnitude added; closing paragraph updated; honest-caveats expanded); `ca-reference.md` (new EMQG-specific cross-reference block covering modified Poisson, three mass definitions, Fizeau analog, Milne cosmology).
- **Source:** `Reference Research/6 - CA Theory and Physics.pdf` (100 pages, Ostoma & Trushyk, 7 July 1999) — the full version of which Paper 3 is the SR-only ~50-page excerpt. Same authors as Paper 3; same structural-CA claims; Paper 6 adds §§8–20 (Quantum Inertia, three mass definitions, gravity-as-Fizeau-scattering, EMQG field equations, Milne kinematic cosmology, two CA wavefunction models). A detailed structured summary already exists in `ostoma-trushyk-1999-summary.md` (originally written from the duplicate copy `Cellular Automata Theory.pdf` on 2026-05-15).
- **Why:** Paper 6 supplies the first **external published** justification for the variable-$c$ ansatz used in `ca_curved.py` / F3b — the modified Poisson equation $\nabla^2\phi - c^{-2}\partial_t^2\phi = 4\pi G\rho$ (Paper 6 Eq. 19.7) and the gravitational variable-$c$ formula $c(t)=c(1\pm gt/c)$ (Eqs. 18.51–18.52) are the closest published lineage for the project's gravity-by-refraction approach. Previously F3b's $\alpha=1.5$ depth-exponent was project-internal heuristic; with Paper 6 it gains a published target.
- **Tests proposed:** V11 EMQG modified-Poisson regression (solve Paper 6 Eq. 19.7 on lattice for spherical mass, feed $|\nabla\phi|$ into `ca_curved.py`, regress on Newtonian deflection $\Delta\theta \approx 2GM/(bc^2)$); V12 gravitational redshift from a linear $c(z)$ profile, pass criterion $\Delta\nu/\nu \approx -|\nabla c|\,L/c$; V13 WEP-violation at $10^{-40}$ is unfalsifiable at float64 precision and documented as such.

## 2026-05-16 (later)

### 10× lattice-resolution bump across the test suite

Every test runner had its lattice-spacing parameters scaled up by a factor of ten in each spatial dimension. The intent is to expose any artifact that has been hiding under coarse discretization, and to give the v2-build L3/L4 sectors a finer substrate to verify against.

**What was changed.** Linear lattice sizes `L` and proportionally-scaled spatial-feature parameters (Gaussian widths `σ`, impact parameters `b`, depression widths `σ_phi`, packet starting offsets) were all multiplied by 10. Step counts that index *time* resolution were either left unchanged (where the test measures a frequency or phase that the FFT bin already resolves) or scaled with `L` (where the test measures a path length).

| File | Test | Old | New | Notes |
|---|---|---|---|---|
| `run_L_tests.py` | L1.d (3D BCC norm drift) | $L=16$ | $L=160$ | $\sim 4.1\text{M}$ cells; FFT working memory $\sim 250\,\text{MB}$ per spinor component. |
| `run_L_tests.py` | L1.f (3D BCC single step) | $L=12$ | $L=120$ | Trivial. |
| `run_L_tests.py` | L2.e (2D exact-arccos norm drift) | $L=32$ | $L=320$ | Trivial. |
| `ca_emqg.py` | L4.a (test_point_source_potential) | $L=64$, $\sigma=3$ | $L=640$, $\sigma=30$ | 2D Poisson, source width scales with L. |
| `ca_emqg.py` | L4.b (test_vacuum_c_uniform) | $L=32$ | $L=320$ | Trivial. |
| `ca_emqg.py` | L4.c (test_lensing_deflection) | $L=128$, $b=18$, $\sigma=6$ | $L=1280$, $b=180$, $\sigma=60$ | Cayley LU memory at L=1280 is $\sim 10\,\text{GB}$ (O(L³) for 2D nested-dissection). Fallback to $L=384$ or Krylov solver if RAM-bound. |
| `run_phase_tests.py` | A1 (Bloch coloring) | $L=32$ | $L=320$ | Visualization only. |
| `run_phase_tests.py` | A2 (visualization frames) | $L=64$, $N_1=96$, $\sigma=5$, snap=240 | $L=640$, $N_1=960$, $\sigma=50$, snap=2400 | Bump on the propagation arms; 8×8 graph plot kept (display scale, not physics). |
| `run_phase_tests.py` | B1 (group velocity) | $L=128$, $n_{\text{steps}}=60$, $\sigma=8$ | $L=1280$, $n_{\text{steps}}=600$, $\sigma=80$ | FFT propagator. |
| `run_phase_tests.py` | B2 (size sweeps) | $L\in\{8\dots64\}$, $\sigma\in\{0.5\dots5\}$, $L_\sigma=32$ | $L\in\{80\dots640\}$, $\sigma\in\{5\dots50\}$, $L_\sigma=320$ | Pass criterion bumped (`L≥320`, `σ≥30`). Log-x axis added so the plot stays readable. |
| `run_phase_tests.py` | C1 (refraction, 3 arms) | $L=128$, $\sigma=8$, $n_{\text{steps}}=200$ | $L=1280$, $\sigma=80$, $n_{\text{steps}}=2000$ | Cayley arm has the same LU memory caveat as L4.c. |
| `run_phase_tests.py` | D1 (Dirac CA: Weyl regression, norm, dispersion, zitterbewegung) | $L\in\{32, 96\}$, $\sigma\in\{3, 14\}$ | $L\in\{320, 960\}$, $\sigma\in\{30, 140\}$ | Zitterbewegung `n_steps=5000` and `dt=0.5` are *time* params unchanged. |
| `run_phase_tests.py` | E1 (Aharonov–Bohm) | $L=64$, $\sigma=8$ | $L=640$, $\sigma=80$ | Flux $\pi$ is a topological invariant — unchanged. |
| `run_phase_tests.py` | E2 (parity violation) | $L=32$, $\sigma=4$ | $L=320$, $\sigma=40$ | `c=0` disables propagation; `n_steps=63` measures isospin angle only. |
| `run_phaseF_tests.py` | F1 (vacuum regression) | $L=32$, $\sigma=3$ | $L=320$, $\sigma=30$ | Bit-for-bit identity test; should still hit machine precision. |
| `run_phaseF_tests.py` | F2 (Higgs/Goldstone dispersion) | $L=64$ | $L=640$ | dt parameters unchanged. |
| `run_phaseF_tests.py` | F3 (Yukawa back-reaction) | $L=64$, $\sigma=5$ | $L=640$, $\sigma=50$ | dt, n_steps, μ², λ, y all unchanged. |
| `run_phaseF_tests.py` | F3b (Cayley gravity demo) | $L=96$, $\sigma_\phi=12$, $\sigma_{\text{pk}}=8$, $\Delta y=18$, $n_{\text{steps}}=120$ | $L=960$, $\sigma_\phi=120$, $\sigma_{\text{pk}}=80$, $\Delta y=180$, $n_{\text{steps}}=1200$ | Pass threshold on `deflection` rescaled from −0.05 cells to −0.5 cells. |
| `run_phaseF_tests.py` | F4 (symmetry restored) | $L=32$, $\sigma=3$ | $L=320$, $\sigma=30$ | Bit-for-bit identity test. |

**What is *not* changed.** Brillouin-zone *sampling density* in L1.a / L2.a (the $K = \text{linspace}(\ldots, 16, \ldots)$ k-grids used for unitarity sweeps) is left at 16 per axis — that is a verification-fineness, not a lattice resolution. Dimensionless wavevectors (`k_in=(0.5, 0.15)`, `k0=0.5`, flux $\pi$) are unchanged. Mexican-hat parameters $\mu^2, \lambda$, Yukawa $y$, Newton-analog $G$, c values, dt and n_steps for time-domain frequency tests are all unchanged.

**Tests not yet re-run at the new size.** The runners are updated but a regression pass at the new sizes has not yet been executed. The most likely failure mode is the Cayley arm of C1 and the L4.c lensing test running out of RAM on the LU factorization; the runners now carry inline notes pointing to feasible fallbacks ($L=384$–$512$) if that happens. Bit-for-bit regression tests (F1, F4, D1 Weyl-regression-at-m=0) should still hit machine precision because they are pure equality checks on identical update rules at a larger array shape.

##
**Summary table — exactness of the model claims:**

| Construct | Status | Justified by |
|---|---|---|
| Norm conservation in `weyl_step_*_splitstep` | Exact-by-construction; machine precision in floating point | $U(\mathbf k)$ unitary by Pauli identity |
| BCC unitarity (`u² + \|n\|² = 1`) with corrected $\tilde n_y$ sign | Exact algebraic identity | `(c_x²+s_x²)(c_y²+s_y²)(c_z²+s_z²) = 1` (Finding 1) |
| 2D exact-arccos unitarity | Exact algebraic identity | $(c_x^2+s_x^2)(c_y^2+s_y^2) = 1$ |
| BCC dispersion $\omega = \arccos(u(\mathbf k))$ | Exact at every $\mathbf k$ | Paper 1 Eq. 15 |
| Composite-photon dispersion along (1,0,0) | Exact: $\Omega_\gamma = k/\sqrt 3$ | Algebraic identity $2\arccos(\cos(k/2/\sqrt3))$ |
| Composite-photon Maxwell curl | **Approximate, $O(k)$ residual** | Pointwise bilinear; smeared form needed for $O(k^3)$ (Finding 2) |
| v1 $c \propto \|\Phi\|^{-\alpha}$ exponent $\alpha$ | **Free fitting parameter** | No derivation; α=1.5 is heuristic |
| v2 $c = c_0/(1 - 2\phi/c_0^2)$ | Implemented form is GR-Shapiro; doc has wrong sign | Implementation matches GR weak-field |
| 2D EMQG Poisson against 3-D Newtonian target | **Dimensionally mismatched** | Item 4 above |
| Yukawa $c^2$ factor in $H_Y$ | Lattice-internal units kludge | Matches Dirac mass-Hamiltonian convention; not in SM |
| F3 back-reaction $|\Phi - v|$ magnitude | Qualitative; pass band is 7 orders wide | Sketch, not derived target |

## 2026-05-16

### P1 — symplectic Yukawa back-reaction (corrected c² factor)
- **Files:** `ca-simulation/ca_unified.py` (`unified_step` gains `back_react=True` Strang-symmetric half-kicks; new `total_energy` helper); `ca-simulation/run_phaseF_tests.py::test_F3` rewritten to use the symplectic API and a 200-step run with a bounded-energy check.
- **Derivation:** the Yukawa Hamiltonian density is `H_Y = c²·y·(Φ·η†χ + Φ*·χ†η)`. The factor `c²` is essential because the Dirac stepper uses `m·c²·β` for the mass-Hamiltonian — without it, the Π update is too small to balance the Ψ rotation, leaving a constant Strang offset (1.85% drift independent of dt). With `c²` included, Hamilton's equation `δΠ/δt = -∂H_Y/∂Φ* = -c²·y·χ†η` matches the Ψ rotation generator and the symplectic split is exact.
- **Test result:** `max|H − H₀| / |H₀|` over 200 steps with dt=0.5 is **3 ppm** (was 1.85% before the correction). Drift scales as O(dt²) exactly: dt=0.5 → 3.0e-6, dt=0.25 → 7.4e-7, dt=0.125 → 1.8e-7, dt=0.0625 → 4.6e-8 (every factor-2 dt drop reduces drift by 4×).
- **|Φ−v| range** dropped from 0.012–1.247 (old divergent sketch, 30 steps) to 0.66–0.73 (200 steps), confirming the back-reaction stays in a bounded oscillation around vacuum instead of running away. F1/F2/F4 unchanged with the default `back_react=False`.

### P3 — Cayley/Crank–Nicolson exact-unitary variable-c kinetic step
- **Files:** `ca-simulation/ca_curved.py` (added `_build_cayley_matrix_2d`, `CayleyVarcSolver2D`, `weyl_step_2d_varc_cayley`, `method='cayley'` option in `measure_refraction`); `ca-simulation/run_phase_tests.py::test_C1` extended with a Cayley arm; new `test_F3b` Newtonian-gravity demo in `run_phaseF_tests.py`.
- **What:** solves `(I + i·dt/2·H_disc)·ψ_new = (I − i·dt/2·H_disc)·ψ_old` where `H_disc` is the Hermitized variable-c Weyl operator with face-averaged c (`c_face(i+½,j) = (c(i,j)+c(i+1,j))/2`). Sparse 10-nonzero/row matrix; LU-factored once per c-field change via `scipy.sparse.linalg.splu`. Sub-stepping (`n_sub`) inside the solver reduces O(dt²) Crank–Nicolson dispersion without giving up exact unitarity.
- **Norm conservation:** drift 5.5e-15 over 200 steps on variable c (range 0.2–0.6) vs **32.6%** for the existing Strang-split stepper. That's a 6×10¹³ improvement — Cayley is at the complex128 machine-precision floor.
- **C1 refraction:** Cayley measures the right qualitative refraction direction but is 5.4° off the continuum Snell prediction at |k|≈0.5. This is the **lattice dispersion** of centered first-differences (ω(k)=c·sin(k) instead of c·|k|), not a bug. The existing Strang+FFT path avoids it for the c₀ baseline because the FFT propagator gives exact-k dispersion. Closing the gap requires a higher-order spatial stencil — flagged as future work.
- **F3b — gravitational lensing demo:** static |Φ| depression at the lattice centre (sigma=12, depth 0.35); `c(x) = c₀·(|Φ|/v)^α` with α=1.5 so the depression makes c *slower* at the centre (the proposition's published sign `(-α)` is inconsistent with F3's depression direction; the `+α` form is what produces attraction). A Weyl probe packet at impact parameter +18 cells is deflected an extra 6.6 cells **toward** the depression vs the flat-c baseline. Norm drift 1.1e-15.
- **Test totals:** 13/13 phases pass (A1–E2 + F1–F4 + F3b). Full Phase A–E suite still 8/8 unchanged.

## 2026-05-15

### Added overview of Reference Research papers 1–4 (QCA literature)
- **File:** `qca-papers-1-4-overview.md` (new).
- **Sources:** `Reference Research/1 - Free QFT from Quantum Cellular Automata.pdf` (Bisio/D'Ariano/Perinotti/Tosini 2015, *Found. Phys.* 45, 1137); `2 - Simple Derivation of the Weyl and Dirac Quantum CA.pdf` (Raynal 2017, arXiv:1703.05890v2); `3 - Special Relativity Derived from Cellular Automata Theory.pdf` (Ostoma & Trushyk 1999); `4 - Weyl Dirac and Maxwell Quantum CA.pdf` (Bisio/D'Ariano/Perinotti/Tosini 2016, arXiv:1601.04842).
- **Why:** Papers 1, 2, 4 together establish the rigorous QCA framework (Cayley graph from informational principles → BCC lattice in 3D / square in 2D → Weyl, Dirac, Maxwell in the small-wavevector limit) that the project's `ca_core.py`/`ca_dirac.py` implementations are *closely related to but not identical to*. The overview maps the agreements (machine-precision Weyl/Dirac dispersion, Zitterbewegung at 2mc², per-cell U(1) phase structure), divergences (our 3D code uses a simple-cubic lattice; Papers 1–2 prove BCC is the unique non-trivial 3D choice; our split-step uses linearized $\omega = c|\mathbf{k}|$, the QCAs use the exact $\arccos$ dispersion), and absent components (composite-photon Maxwell construction not implemented; mass-parameter $n^2+m^2=1$ constraint not enforced). Paper 3 is qualitatively different — physically motivated rather than formally derived — and contributes the mass-vs-force reinterpretation that is observationally indistinguishable from standard SR.
- **Tests proposed:** V1 exact QCA dispersion (group velocity at non-trivial $|\mathbf{k}|$ matches $\nabla_{\mathbf{k}}\arccos(c_x c_y)$); V2 Klein paradox plateau matching Paper 4 Fig. 3; V3 $n^2+m^2=1$ constraint audit; **V4 composite photon construction** (biggest physics value — implement Paper 1 Eq. 35 as a Maxwell sector derived from Weyl bilinears); V5 frequency-dependent $c(\mathbf{k}) \approx 1 \pm k/\sqrt 3$; V6 BCC vs simple-cubic in 3D; V7 $A_0=0$ audit (Paper 2's central proof); V8 deformed-Lorentz (DSR) signature; V9 cosmic-ray spreading numeric spot-check; V10 mass-as-force-decrease is undecidable, no test arises.

### Added structured summary of Ostoma & Trushyk (1999) *Cellular Automata Theory*
- **File:** `ostoma-trushyk-1999-summary.md` (new).
- **Source:** `Cellular Automata Theory.pdf` (108 pages, July 7 1999).
- **Method:** extracted via `pdftotext -layout` to a working text file; structured into 18 sections covering CA postulates, two-layer space-time, Lorentz derivation, quantum vacuum, Quantum Inertia, EMQG, three-mass framework, the EMQG field equations, Fizeau-like photon scattering account of 4D curvature, two CA wavefunction proposals, Milne kinematic cosmology re-read of the Big Bang, and a section mapping the paper's claims onto this project's existing files (`ca-reference.md`, `cellular-automata-research.md`, `ca-forces-integration.md`, `fredkin-correlation.md`).
- **Why:** the paper sits in the same lineage as Fredkin's *Digital Mechanics* (already in the project) and is the most CA-physics-aligned external source in the workspace. Captured the postulates, equations, and falsifiable predictions in math-mode markdown per project conventions.

### P4 — replaced `m_eff = y·|Φ|` with `m_eff = y·Re(Φ)`
- **File:** `ca-simulation/ca_unified.py::unified_step`.
- **Why:** `|Φ|` is non-analytic at Φ=0 (the F4 vacuum). For the F1 vacuum at `Φ = v` real, `Re(Φ) = |Φ| = v`, so F1 regression is preserved at machine precision (`|Φ−v|=1.11e-16`, `max fermion diff=8.41e-16`). For F2/F3 Φ stays close to real so Re(Φ) and |Φ| agree numerically; F2 dispersion residuals unchanged (max 1.06e-3 radial, 4.42e-4 Goldstone); F3 sketch range `max|Φ−v|=6.97e-01` vs 6.95e-01 previously (within sketch noise). F4 unchanged at exact zero.
- **Tests:** `run_phaseF_tests.py` → 4/4 pass.

### P2 — complex Yukawa bilinear
- **Files:** `ca-simulation/ca_dirac.py` (added `_mix_eta_chi_complex` and `dirac_step_2d_varm_complex_splitstep`), `ca-simulation/ca_unified.py::unified_step` (rewired to pass `Re(Φ)` and `Im(Φ)` separately).
- **What:** the Standard-Model Yukawa Lagrangian `L_Y = -y·(Φ·η†χ + Φ*·χ†η)` produces a *complex* mass `M(x) = y·Φ(x)` coupling η→χ with `y·Φ` and χ→η with `y·Φ*`. The new per-cell rotation `exp(-i·c²·dt·[[0, M·I],[M*·I, 0]])` is exactly unitary; eigenvalues are `±|M|·c²·dt` with eigenvectors `(1, ±M*/|M|)/√2`. Handles `|M|=0` via the well-defined limit `sin(θ)/|M| → factor`.
- **Strang structure:** kinetic step at the real baseline `m_0 = mean(m_R)` (existing `dirac_step_2d_splitstep`), per-cell complex δ-rotation for `(M−m_0)`. Reduces exactly to `dirac_step_2d_varm_splitstep` when `m_I ≡ 0` (verified bit-for-bit, `diff = 0.000e+00`).
- **Unit tests added inline (one-shot):**
  1. `m_I=0` reduction → 0.0 difference vs real stepper.
  2. `m_I≠0` norm conservation over 500 steps → drift 6.8e-14.
  3. Sensitivity: toggling `m_I` from 0 to 0.5 changes the output by 8e-2 after one step (proves the code path is exercised).
- **Tests:** Phase F suite 4/4 pass; full Phase A–E suite still 8/8. **Total 12/12.**
- **F1 regression preserved** because vacuum Φ=v is real → m_I≡0 → complex rotation reduces to identity-after-subtraction → kinetic step matches reference Dirac CA at constant `m = y·v` bit-for-bit.

## 2026-05-14

### F3 propositions document
- Added `ca-f3-propositions.md`. Five ranked candidates (P1 symplectic joint Hamiltonian, P2 complex Yukawa bilinear, P3 Cayley/Padé for variable-c, P4 use Re/Im(Φ) instead of |Φ|, P5 viscous damping as diagnostic only).
- Root-cause: the current F3 test in `run_phaseF_tests.py::test_F3` bolts the Yukawa source onto `state.Pi` outside the Strang split, so the (Φ, Ψ) pair are not conjugate variables of a single Hamiltonian. Energy is not conserved, and the test guards against this with an explicit `> 100.0` early-stop.

### Double-precision regression run
- Re-ran `run_simulation.py` (stages 1–6), `run_phase_tests.py` (Phases A–E, 8 phases), and `run_phaseF_tests.py` (Phase F, 4 phases). Total 12/12 phases + 6 Weyl stages still pass.
- Verified the codebase already runs at native float64/complex128 under NumPy 2.2.6. Cleared `__pycache__` via `PYTHONDONTWRITEBYTECODE=1` so no stale bytecode could mask a regression.
- **No variation** vs. the values tabulated in `project-status.md`. Residuals are at the same 1e-16 floor; Stage 5's reversibility residual scales linearly with run length at ~6e-16/step, confirming it is precision-bound rather than a structural bug.
- New numeric data points captured: Stage 5 residual scaling (n=100..5000 → 5.8e-14..3e-12), Stage 6 3D norm constant at 150.3449 across t=0..5000, and F3 `max|Φ−v|=6.95e-01` over 30 steps (informational baseline for the eventual symplectic fix).

## Earlier (pre-2026-05-14)

Earlier non-trivial decisions live in `project-status.md` under the "Corrections Log" and `ca-unified-proposition.md`. Notable:

- Page-38 boxed FD equations corrected to include `i` on y-derivative terms (2026-05-13).
- Phase F suite (F1–F4) added on top of Phases A–E; F3 ships as a sketch only, with the open engineering item flagged in `ca-unified-proposition.md` line 159.
- Split-step FFT propagator adopted everywhere for production runs; explicit Euler steppers retained only to reproduce the page-39 instability observation.
