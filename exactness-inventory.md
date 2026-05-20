# Exactness Inventory

*A short tally of which lattice results are exact in the algebraic sense (identity, closed form, or bit-for-bit), which are at machine precision (FFT round-off floor, ≲ 1 ulp of complex128 per step), and which are quantitative matches inside a stated tolerance. Pulled from `project-status.md`, `findings.md`, `ca-reference.md`, and `test-results/qca-verifications-results.md`. Last updated 2026-05-18.*

---

## Reading the table

| Tier | What it means | Numerical signature |
|---|---|---|
| **Exact algebraic** | Identity that holds at the symbolic level; residual bounded by ε per quantity, with no growth in $N$, $L$, or $n_\text{steps}$ | residual / (relevant scale · ε) < 1 |
| **Machine precision** | Holds to FFT / linear-algebra round-off floor; residual grows as $\sqrt{N_\text{cells}}$ per step or $n$ per step | residual ~ 10⁻¹⁵ – 10⁻¹² over the run, scales as predicted |
| **Quantitative** | Numerical match inside a declared tolerance; finer than published-target precision in most cases | residual in declared % band, no claim of analytic identity |

---

## Tier 1 — Exact algebraic results

| # | Construct | Predicted form | Measured residual | Source |
|---|---|---|---|---|
| 1 | BCC unitarity $u^2 + \|\tilde{\mathbf{n}}\|^2 = 1$ (Paper 1 Eq. 15, sign-corrected) | $= 1$ | $4.4 \times 10^{-16}$ over 100 random $k$ | Finding 1; `ca_bcc.py` |
| 2 | Vacuum freezing $N_\text{binary}(\mathbf x_\text{vac}) = 0$ | $= 0$ bit-for-bit | $= 0$ on 80% of $L=256$ lattice | T5.A; `test_emergent_time_T5.py` |
| 3 | F1 vacuum regression ($\Phi = v$ fixed; fermion = constant-$m$ ref) | bit-for-bit identity | $1.1 \times 10^{-16}$ (Φ), $8.4 \times 10^{-16}$ (fermion) | F1; `run_phaseF_tests.py` |
| 4 | F4 symmetry-restored regression ($\Phi = 0$ fixed; η = pure Weyl) | bit-for-bit identity | $\Phi = 0$ exact; η diff $7.6 \times 10^{-16}$ | F4; `run_phaseF_tests.py` |
| 5 | A₀ = 0 audit (Paper 2 central result) | $U(k=0) = I$ | $= 0$ (exact) | V7; `run_qca_verifications.py` |
| 6 | Goldstone dispersion $\omega = \|k\|$ on lattice | massless | residual / ($\|k\|\cdot\varepsilon$) ≤ 0.88 at $L=640$ | Finding 3; `ca_higgs.py` |
| 7 | Composite-photon curl-residual leading coefficient | $\frac{1}{\sqrt{2d}}$ | $d=2$: 10 decimals at $k=10^{-5}$; $d=3$: 7 figures | Finding 7; `ca_maxwell{,_2d}.py` |
| 8 | Composite-photon transversality $2\tilde{\mathbf n}\cdot\mathbf E_G = 2\tilde{\mathbf n}\cdot\mathbf B_G = 0$ | $= 0$ | $4.6 \times 10^{-17}$ (3D), $5 \times 10^{-19}$ – $1.8 \times 10^{-17}$ (2D) | L3; `ca_maxwell.py` |
| 9 | Lattice speed of light $c_\text{lat} = 1/\sqrt d$ | dimensionless | algebraic — Bisio *et al.* unique-QCA result | Finding 7 / Finding 10; `ca-reference.md` |
| 10 | SU(2) parity violation — right-chirality leak under left-only rotation | $= 0$ | $= 0.0$ (machine zero) | E2; `ca_weak.py` |
| 11 | Phase-tick / proper-time ratio $N_\text{phase,in}/N_\text{phase,out} = c_\text{in}/c_\text{out}$ | $= c_\text{in}/c_\text{out}$ | $2.7 \times 10^{-16}$ at T2.B Shapiro gate | Finding 11; T2.B / T5.C |
| 12 | Exact 2D QCA dispersion $\omega = \arccos(c_x c_y)$ | $= \arccos(c_x c_y)$ | max $\|\Delta\omega\| = 3.3 \times 10^{-16}$ across 6 modes | V1; `run_qca_verifications.py` |
| 13 | Exact-QCA Dirac dispersion $\omega = \arccos(\sqrt{1-m^2}\,c_x c_y)$ | $\arccos(\sqrt{1-m^2}\,c_x c_y)$ | $3.9 \times 10^{-16}$ residual | Finding 9; `ca_dirac.py` (2026-05-18) |
| 14 | U(1) Aharonov–Bohm phase pickup | $\exp(i\oint A)$ exact | $4.4 \times 10^{-16}$ | E1; `ca_dirac.py` |
| 15 | CHSH Tsirelson saturation on lattice singlet | $|S| = 2\sqrt 2$ exact | $4.4\times 10^{-16}$ pure; $2.2\times 10^{-9}$ after 12 Weyl ticks | Finding 14.3 / QM-1; `tests-priority/test_02_QM1_CHSH.py` |
| 16 | PMNS 3-flavour unitarity $U U^\dagger = I$ | identity | $7.7\times 10^{-17}$ | Finding 14.8 / QFT-5; `tests-priority/test_07_QFT5_neutrino.py` |
| 17 | 2-flavour PMNS oscillation propagator vs analytic $\sin^2(2\theta)\sin^2(\Delta m^2 L/(4E))$ | identity | $4.4\times 10^{-16}$ across $L \in [0, 2000]$ km | Finding 14.8 / QFT-5; ibid. |
| 18 | Chiral charge $Q_\chi$ conservation at $m=0$ (Weyl regression on Dirac stepper) | $\Delta Q_\chi = 0$ | $2.2\times 10^{-16}$ over 500 steps at $L=128$ | Finding 14.13 / QG-4; `tests-priority/test_10_QG4_charge.py` |
| 19 | BCC dispersion exactly linear along $(1,0,0)$ axis ($\omega = k/\sqrt 3$) | identity | $5.7\times 10^{-16}$ (FFT floor) over the small-$k$ band | Finding 14.7 / QG-2; `tests-priority/test_06_QG2_planck_LV.py` |
| 20 | SR-2 Lorentz-violation coefficient $\beta_\text{LV}(m) = \tfrac12(1 - m/(\sqrt{1-m^2}\arcsin m))$ — 2D-square QCA | closed-form analytic function of $m$ | sympy-confirmed; matches numerical SR-2 grid to FFT floor at small $k$ | Finding 15; `ca-simulation/derive_beta_LV.py` |
| 21 | SR-2 next-order coefficient $\gamma_\text{LV}(m) = \tfrac18 - m(3-2m^2)/(24(1-m^2)^{3/2}\arcsin m)$ — 2D-square QCA | closed-form analytic function of $m$ | sympy-confirmed; sharpens the $\beta_\text{LV}\beta^2$ fit by 2–4 orders | Finding 15; `ca-simulation/derive_beta_LV.py` |

**Count: 21 exact algebraic results.**

---

## Tier 2 — Machine-precision results (FFT round-off floor)

| # | Construct | Predicted form | Measured residual | Scaling | Source |
|---|---|---|---|---|---|
| 1 | Weyl regression at $m=0$ from Dirac stepper | exact identity in the $m \to 0$ limit | $1.55 \times 10^{-15}$ at $L=320$ | $\sqrt{N_\text{cells}}$ floor | D1; `ca_dirac.py` |
| 2 | Norm drift, Cayley variable-$c$ stepper | unitary | $5.5 \times 10^{-15}$ | exact-unitary (vs 32.6% Strang drift) | F3b / C1; `ca_curved.py` |
| 3 | Norm drift, BCC 200-step | unitary | $3.7 \times 10^{-14}$ | $\sqrt{N}$ per step | L1; `ca_bcc.py` |
| 4 | Norm drift, 2D arccos QCA 200-step | unitary | $8.4 \times 10^{-15}$ | $\sqrt{N}$ per step | L2; `ca_core_exact.py` |
| 5 | Per-step FFT round-off floor — D1 norm over 1000 steps | unitary | $4.0 \times 10^{-13}$ at $L=320$ | exact 10× ratio from $L=32 \to 320$ (Finding 5) | D1; `ca_dirac.py` |
| 6 | Per-step FFT round-off floor — L2 norm over 200 vs 2000 steps at $L=320$ | unitary | $7.6 \times 10^{-13}$ at $n=2000$ | $= 9.985\times$ that at $n=200$ (linear-in-$n$ to 4 figures) | Finding 5; L2 |

**Pattern (Finding 5):** norm drift per FFT round-trip is ~1 ulp of complex128. The codebase is already at native double precision; upgrading to long-double would shave ~1 decimal of error per step at significant speed cost.

---

## Tier 3 — Quantitative matches (within declared tolerance)

| # | Construct | Predicted form | Measured | Tolerance / threshold | Source |
|---|---|---|---|---|---|
| 1 | C1 Snell refraction (Strang) | exit angle from Snell's law | 0.51° error | qualitative pass | C1; `ca_curved.py` |
| 2 | C1 Cayley refraction at $\|k\|\approx 0.5$ | exit angle from Snell's law | 5.4° error | lattice-dispersion limited | Phase F3 update; `ca_curved.py` |
| 3 | D1 zitterbewegung at $2\arcsin(m)$, $m=0.5$ | $\pi/3 = 1.04720$ | $1.04877$ | 0.15% (FFT-bin-limited) | Finding 9 closeout; `ca_dirac.py` |
| 4 | Group velocity $v_g = c\hat k$ (B1) | $\|v_g\|/c = 1$ | $0.9995$ – $0.9999$ at $L=640$ | <0.05% at the 10× lattice | Finding 6 / B1; `run_phase_tests.py` |
| 5 | Composite-photon dispersion $\Omega_\gamma = \|k\|/\sqrt 3$ (BCC) | $\|k\|/\sqrt 3$ | 0.21% at $k = 0.05$ | published-target precision | L3; `ca_maxwell.py` |
| 6 | F2 Higgs radial dispersion $\omega = \sqrt{k^2 + 2\mu^2}$ | $\sqrt{k^2 + 2\mu^2}$ | max res $1.0 \times 10^{-3}$ | O(dt²) Verlet-limited | F2; `ca_higgs.py` |
| 7 | EMQG static Poisson rel err | $\nabla^2\phi = 4\pi G\rho$ | 2.75% at $L=64$ → 1.39% at $L=640$ | qualitative | L4.a; `ca_emqg.py` |
| 8 | 3-D Newtonian lensing linear-in-M ratio | $\Delta(2M)/\Delta(M) = 2$ | $1.99647$ at $L=64$ | 0.35% (Newtonian); threshold 10% | Finding 8; `ca_emqg.py` |
| 9 | Klein paradox plateau location (Paper 4 Fig. 3) | reflection plateau in $\varphi \in [m, 2-2m]$ shifted | max $R = 0.91$ in $\varphi \in [1.4, 2.0]$ | qualitative shape match | V2; `run_qca_verifications.py` |
| 10 | Frequency-dependent $c$ at $\|k\|=0.5$ along $(1,1)$ | $\Delta c/c$ per Paper 4 Eq. 23 | $-1.1\%$ | qualitative | L2; `ca_core_exact.py` |
| 11 | Frequency-dependent $c$ off-axis (V5) | sign and magnitude per Paper 4 | dev at $\|k\|=1.0$ = $-6.7\%$ | qualitative | V5; `run_qca_verifications.py` |
| 12 | BCC vs simple-cubic regression (V6) | grow from 0 toward Paper 1 unique-QCA | dev grows 0 → 7.5% across range | qualitative | V6; `run_qca_verifications.py` |
| 13 | DSR Lorentz-deformation signature (V8) | standard-Lorentz residual $\sim k^2$ | qualitative match | qualitative | V8; `run_qca_verifications.py` |
| 14 | F3 symplectic-Yukawa energy drift (200 steps, dt=0.5) | drift bounded $O(dt^2)$ | 3 ppm | qualitative | F3 follow-up; `ca_unified.py` |
| 15 | GR-1 absolute light deflection coefficient $K = \Delta\theta\cdot b\cdot c^2/(GM)$ | $K = 4$ (Einstein) | $|K| = 3.499$ at $L=160$ (linear-in-$M$ to machine zero) | 12.5% off Einstein, 75% off Newtonian — PBC-limited | Finding 14.2 / GR-1; `tests-priority/test_01_GR1_light_deflection.py` |
| 16 | GR-3 phase-tick redshift ratio vs Paper 6 ansatz $\Delta\nu/\nu = 2\Delta\phi/c^2$ | match Paper 6 form | $-0.998$ (signed) across 4 (near, far) pairs | 0.2% (matches the *ansatz*; falsifies vs measured GR by factor 2) | Finding 14.5 / GR-3; `tests-priority/test_04_GR3_pound_rebka.py` |
| 17 | GR-2 absolute Shapiro $\Delta t_\text{lat}/\Delta t_\text{GR}$ at $L=192$, $b=12$ | $\to 1$ as $L \to \infty$ | $0.62$ (monotonic in $L$: $0.47, 0.54, 0.62$ at $L=96, 128, 192$) | within an extrapolation; absolute 0.1% gate not met at accessible $L$ | Finding 14.6 / GR-2; `tests-priority/test_05_GR2_shapiro.py` |
| 18 | QG-2 $E_\text{LV}$ from BCC dispersion (diagonal $(1,1,1)$) | $\ge 1.2\times 10^{19}$ GeV (Fermi GRB) | $1.87\times 10^{20}$ GeV at $a = 1.616\times 10^{-35}$ m | $\sim 10\times$ Fermi bound — PASS up to $a \le 1.5\times 10^{-34}$ m | Finding 14.7 / QG-2; `tests-priority/test_06_QG2_planck_LV.py` |
| 19 | QFT-5 3-flavour PMNS atmospheric peak location | $\sim 495$ km/GeV | $553$ km/GeV (lattice 3-flavour with $\theta_{13}=8.6°$, solar mixing) | 11.85% off 2-flavour analytic; consistent with 3-flavour multi-$\Delta m^2$ interference | Finding 14.8 / QFT-5; `tests-priority/test_07_QFT5_neutrino.py` |
| 20 | QM-2 sub-threshold tunneling at $V_0 = 0.15$, width 6, $m=0.1$, $k_x=0.2$ | match Schrödinger $T = (1 + V_0^2\sinh^2(\kappa a)/(4E(V_0-E)))^{-1}$ | $T_\text{lat}/T_\text{QM} = 0.982$ | 1.8% (in-window sweet spot; Klein paradox dominates broader scan) | Finding 14.11 / QM-2; `tests-priority/test_08_QM2_tunneling.py` |
| 21 | GR-4 Mercury perihelion at $v^2/c^2 = 5.6\times 10^{-3}$ | $\Delta\omega = 6\pi GM/(a(1-e^2)c^2)$ | $0.0612$ rad/orbit vs analytic $0.0621$; per-orbit std $1.6\times 10^{-5}$ | 1.5% (1PN truncation, scales as $v^2/c^2$ to expected) | Finding 14.12 / GR-4; `tests-priority/test_09_GR4_mercury.py` |
| 22 | QG-4 U(1) charge conservation at $L=256$, 1000 steps | drift at FFT floor | $|\Delta Q|/Q = 1.83\times 10^{-13}$ (linear in step at $1.8\times 10^{-16}$/step) | FFT-floor (Finding 5) limited; strict 1e-13 gate missed by 1.8× | Finding 14.13 / QG-4; `tests-priority/test_10_QG4_charge.py` |

---

## Currently failing / not-yet-met

| # | Construct | Where it sits | What blocks it |
|---|---|---|---|
| 1 | Absolute coefficient of light deflection $\Delta\theta = 4GM/(bc^2)$ (Einstein) | GR-1 (Finding 14.2) | **Resolved as Tier 3 #15**: $|K| = 3.499$ — Einstein-leaning, 12.5% off 4, PBC-limited. Closing the gate needs open-BC Poisson. |
| 2 | $1/b$ scaling of 3-D EMQG lensing | F8 follow-on | F3b scan exercises $\|\Phi\|^\alpha$ metric, not 3-D EMQG potential. Open. |
| 3 | Pointwise composite-photon curl matches free Maxwell at $O(k^3)$ | Finding 2 | Pointwise bilinear gives $O(k)$ residual with leading $1/\sqrt{2d}$; Paper 1's smearing function $f_{\mathbf k}(\mathbf q)$ not yet implemented. |
| 4 | F3 lensing prediction failure at low fermion density | next-steps line 5 | Open falsification target. |
| 5 | Subleading coefficient $\beta \approx 0.01883$ (3D) / $\alpha \approx -0.0104$ (2D) | Finding 7 | No derived closed form yet. |
| 6 | Cayley arm of C1 / F3b / L4.c at $L=1280$ or $L=960$ | 10× bump (2026-05-16) | Sparse-LU memory ≈ 5–10 GB exceeds sandbox. Run at $L=384$–$512$ fallback. |
| 7 | SI-unit identification for $a$ and $\tau$ | Finding 10 | Project hasn't picked one of the three resolutions (adjust $\tau$, adjust $a$, or reinterpret $a/\tau$ as the lightcone). Required before any absolute-magnitude GR test. |

---

## Tally (updated 2026-05-19 - 23:30 after Finding 15 β_LV closed form)

- **21 exact algebraic** results (19 prior + 2 new: SR-2 $\beta_\text{LV}(m)$, SR-2 $\gamma_\text{LV}(m)$ closed forms).
- **6 machine-precision** results that hit the FFT round-off floor.
- **22 quantitative** matches inside their declared tolerances (14 prior + 8 new: GR-1, GR-2, GR-3, GR-4, QG-2, QFT-5 peak, QM-2 sweet spot, QG-4 U(1)).
- **7 open/blocked** items requiring code or judgment.

This is the inventory the test roadmap (`lattice-vs-spacetime-tests.md`) is written against. Every PASS already on the books is in tiers 1–3 above; every test in the roadmap is either a new gate that has not yet been built, or an extension of an existing gate (e.g., the absolute-coefficient version of an existing ratio test).
