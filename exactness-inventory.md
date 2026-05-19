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

**Count: 14 exact algebraic results.**

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

---

## Currently failing / not-yet-met

| # | Construct | Where it sits | What blocks it |
|---|---|---|---|
| 1 | Absolute coefficient of light deflection $\Delta\theta = 4GM/(bc^2)$ (Einstein) or $2GM/(bc^2)$ (Newtonian) | F8 follow-on | Test only checks the ratio; the absolute lattice coefficient has not been compared to GR/Newton. Open. |
| 2 | $1/b$ scaling of 3-D EMQG lensing | F8 follow-on | F3b scan exercises $\|\Phi\|^\alpha$ metric, not 3-D EMQG potential. Open. |
| 3 | Pointwise composite-photon curl matches free Maxwell at $O(k^3)$ | Finding 2 | Pointwise bilinear gives $O(k)$ residual with leading $1/\sqrt{2d}$; Paper 1's smearing function $f_{\mathbf k}(\mathbf q)$ not yet implemented. |
| 4 | F3 lensing prediction failure at low fermion density | next-steps line 5 | Open falsification target. |
| 5 | Subleading coefficient $\beta \approx 0.01883$ (3D) / $\alpha \approx -0.0104$ (2D) | Finding 7 | No derived closed form yet. |
| 6 | Cayley arm of C1 / F3b / L4.c at $L=1280$ or $L=960$ | 10× bump (2026-05-16) | Sparse-LU memory ≈ 5–10 GB exceeds sandbox. Run at $L=384$–$512$ fallback. |
| 7 | SI-unit identification for $a$ and $\tau$ | Finding 10 | Project hasn't picked one of the three resolutions (adjust $\tau$, adjust $a$, or reinterpret $a/\tau$ as the lightcone). Required before any absolute-magnitude GR test. |

---

## Tally

- **14 exact algebraic** results.
- **6 machine-precision** results that hit the FFT round-off floor.
- **14 quantitative** matches inside their declared tolerances.
- **7 open/blocked** items requiring code or judgment.

This is the inventory the test roadmap (`lattice-vs-spacetime-tests.md`) is written against. Every PASS already on the books is in tiers 1–3 above; every test in the roadmap is either a new gate that has not yet been built, or an extension of an existing gate (e.g., the absolute-coefficient version of an existing ratio test).
