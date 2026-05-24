# Project Review — Summary of All Findings (F1–F22)

*2026-05-22. Findings are the project's documented physics discoveries, confirmations, falsifications, and characterisations. F1–F15 live in `findings.md`; F16–F22 live as individual files in `findings/`.*

---

## F1 — BCC Weyl Unitarity Confirmation and Paper 1 Sign Correction

**Date:** 2026-05-13  
**Status:** Closed — Tier 1 exact.

The BCC kernel from Paper 1 (Bisio et al., Eq. 15) contains a sign error: the second term of $\tilde{n}_y$ was written as $-s_xc_ys_z$ but must be $+s_xc_ys_z$ (the sign is also positive by the same pattern as $\tilde{n}_x$ and $\tilde{n}_z$).

**Effect of error:** With the wrong sign, $|u^2 + |\tilde{n}|^2 - 1| = 0.47$ — the propagator is not even approximately unitary. With the correction the residual is $4.4\times10^{-16}$ — machine precision.

**Fix:** `ca_bcc.py::_bcc_uvec` uses the corrected sign. This is the primary BCC Weyl QCA kernel used throughout the project.

---

## F2 — Composite Photon Curl Residual is $O(k)$, Not $O(k^3)$

**Date:** 2026-05-13  
**Status:** Open — curl$/$k coefficient is known (Finding 21 extends this); smearing function not yet implemented.

The pointwise bilinear construction $G^i = \phi^T\sigma^i\psi$ (Paper 1 Eq. 35) satisfies the Maxwell curl equation only to $O(k)$. Paper 1 implies $O(k^3)$ accuracy would require a smearing function $f_\mathbf{k}(\mathbf{q})$.

The $O(k)$ coefficient was initially measured as $1/\sqrt{2d} = 1/\sqrt{6}$ on the 3D BCC lattice. The geometry-independent law was later determined to be $c_\text{lat}/\sqrt{2}$ (Finding 21).

---

## F3 — Goldstone Dispersion is Exact; CFL Constraint Identified

**Date:** 2026-05-14  
**Status:** Closed.

The Goldstone mode from the $U(1)$-broken Higgs has $\omega = |k|$ exactly, confirmed to residual $\le 0.88\,\varepsilon$ at $L=640$ (Tier 1 #6).

Additionally, the Higgs stepper with $\phi_{sub}=1$, `dt=1.0` violates the CFL stability bound $dt_\text{sub} < 2/\sqrt{8+2\mu^2} \approx 0.667$, causing NaN divergence at $L=320$. Fix: $\phi_{sub}=2$.

---

## F4 — Symmetry-Restored Regime (Φ = 0) is Exact

**Date:** 2026-05-14  
**Status:** Closed — Tier 1 exact.

In the symmetry-restored phase ($\Phi = 0$, $\eta$ = pure Weyl): $\Phi = 0$ exactly; fermion diff $7.6\times10^{-16}$ (bit-for-bit identity). This regression confirms the Higgs/fermion coupling turns off cleanly.

---

## F5 — FFT Round-Off Floor Characterisation

**Date:** 2026-05-14  
**Status:** Closed — systematic understanding.

The per-step norm drift from FFT round-off is $\sim 1$ ulp of complex128, scaling:

- Linearly in number of steps $n$.
- As $\sqrt{N_\text{cells}}$ in the lattice volume.

Measured concretely: D1 at $L=32$ gives drift $4.0\times10^{-14}$ over 1000 steps; at $L=320$ gives $10\times$ more ($= \sqrt{(320/32)^2} = 10$). L2 at $n=200$ and $n=2000$ gives a factor of $9.985\times$ (expected 10) — linear to 4 figures.

This sets the fundamental precision floor for all long-time or large-lattice simulations. Upgrading from complex128 to long-double would improve by ~1 decimal.

---

## F6 — Group Velocity Confirms $v_g = c\hat{k}$ to 0.05%

**Date:** 2026-05-14  
**Status:** Closed — Tier 3 quantitative.

On a $10\times$-oversampled lattice ($L=640$ for a nominal $L=64$ test), the group velocity magnitude $|v_g|/c = 0.9995$–$0.9999$, confirming $v_g = c\hat{k}$ to $<0.05\%$.

---

## F7 — Composite-Photon Curl Coefficient Derivation

**Date:** 2026-05-14  
**Status:** Closed for the BCC case; generalised in F21.

The leading curl residual coefficient on the BCC lattice is $1/\sqrt{6}$ (the $d=3$ special case of $1/\sqrt{2d}$). Verified to 10 decimal places in 2D ($d=2$: coefficient $1/\sqrt{4} = 1/2$) and 7 figures in 3D BCC.

This is an exact result of the bilinear construction: the smearing function $f_\mathbf{k}(\mathbf{q})$ from Paper 1 is required to push the residual toward $O(k^3)$.

---

## F8 — 3D Poisson Lensing is Self-Consistent; 2D Poisson is Wrong

**Date:** 2026-05-14  
**Status:** Closed.

A 2D Poisson solver gives $\phi \sim \ln r$ (logarithmic), not $1/r$ (Newtonian). This is dimensionally inconsistent with 3D Newtonian gravity. The EMQG lensing tests must use a 3D Poisson solver sliced at the equatorial plane. After switching to 3D: Newtonian lensing linear-in-$M$ ratio is $1.99647$ at $L=64$ (0.35% off the factor-2, Tier 3 #8).

---

## F9 — Dirac Dispersion Exact; Zitterbewegung at $2\arcsin(m)$

**Date:** 2026-05-16  
**Status:** Closed — Tier 1 and Tier 3.

The exact-QCA Dirac dispersion $\omega = \arccos(\sqrt{1-m^2}\cos k_x\cos k_y)$ is confirmed to $3.9\times10^{-16}$ residual (Tier 1 #13).

The zitterbewegung frequency is $2\arcsin(m)$ at $m=0.5$: predicted $\pi/3 = 1.04720$, measured $1.04877$, difference 0.15% (FFT-bin-limited, Tier 3 #3).

---

## F10 — SI Unit Identification: $c_\text{physical} = c/\sqrt{d}$

**Date:** 2026-05-16  
**Status:** Open — project has not committed to a resolution.

Setting $a = \ell_P$, $\tau = t_P$ gives $c_\text{physical} = a/(\tau\sqrt{d}) = c/\sqrt{d}$ — off by $\sqrt{d}$ from the physical speed of light. Three internally consistent resolutions are identified:

1. Adjust $\tau$ downward by $\sqrt{d}$ (absorb into the time unit).
2. Adjust $a$ upward by $\sqrt{d}$ (non-Planck lattice spacing).
3. Reinterpret $a/\tau$ (not $a/(\tau\sqrt{d})$) as the lightcone speed.

This remains an open foundational question before absolute-magnitude GR tests can be made.

---

## F11 — Phase-Tick Ratio = $c_\text{in}/c_\text{out}$: Exact Shapiro-Delay Relation

**Date:** 2026-05-16  
**Status:** Closed — Tier 1 exact (#11).

In the variable-$c$ Cayley stepper, the ratio of phase-tick counts inside vs outside a gravitational well satisfies:

$$\frac{N_\text{phase,in}}{N_\text{phase,out}} = \frac{c_\text{in}}{c_\text{out}},$$

to residual $2.7\times10^{-16}$. This is the lattice's version of the Shapiro time delay / gravitational time dilation, derived from local rules alone.

---

## F12 — SR-2 Time Dilation Passes; $\beta_\text{LV}(m)$ Characterised Numerically

**Date:** 2026-05-16  
**Status:** Closed as a passing test; exact closed form derived in F15.

The SR-2 test measures the ratio $R(k) = \omega_\text{moving}/\omega_\text{static}$ vs $1/\gamma_\text{SR}$. The dispersion identity $(R - 1/\gamma_\text{SR}) = \beta_\text{LV}(m)\beta^2 + O(\beta^4)$ is satisfied, with the lattice ratio always below the SR prediction ($\beta_\text{LV} < 0$).

**Correction note:** Finding 12 originally stated $\beta_\text{LV}$ is "positive" — this was a sign error from reading unsigned $|\Delta|$ values. The correct sign is negative (over-dilation, confirmed in F15).

---

## F13 — 3D BCC $\beta_\text{LV}$ is $\sim 10\times$ Larger than 2D-Square

**Date:** 2026-05-16  
**Status:** Documented; 3D closed-form derivation not yet done.

At matched $v_g/c_\text{lat}$, the 3D BCC lattice gives a Lorentz-violation coefficient approximately $10\times$ larger than the 2D-square case. This is expected from the more complex BCC dispersion relation (the $u_\text{BCC}$ kernel has a $\hat{k}$-dependent structure absent in the simple product $\cos k_x\cos k_y$). The 3D closed-form $\beta_\text{LV}^\text{(3D)}(m, \hat{k})$ is a clean follow-up using the same implicit-differentiation method.

---

## F14 — Priority Test Sweep: 10 Tests Run; Mixed Results

**Date:** 2026-05-19  
**Status:** Closed (summary result).

A sweep of 10 priority tests produced the following scoreboard:

| # | Test | Result |
|---|---|---|
| 1 | GR-1 light deflection | EINSTEIN-LEANING (PBC); 12.5% off; later fixed by F14.15 |
| 2 | QM-1 CHSH | PASS — $4.4\times10^{-16}$ pure; $2.2\times10^{-9}$ propagated |
| 3 | SR-2 time dilation | PASS — $4.4\times10^{-15}$ (dispersion identity) |
| 4 | GR-3 Pound-Rebka | FAIL — matches $2\Delta\phi/c^2$, factor-2 off; fixed by F16 |
| 5 | GR-2 Shapiro | PBC-limited (38% off); later fixed by F14.16 |
| 6 | QG-2 Planck LV | PASS — $E_\text{LV} = 1.87\times10^{20}$ GeV |
| 7 | QFT-5 neutrino oscillations | PASS (mechanism + peak within 12%) |
| 8 | QM-2 tunneling | Narrow-window PASS at sweet spot; Klein paradox confirmed |
| 9 | GR-4 Mercury perihelion | PASS — 1.5% off Schwarzschild 1PN |
| 10 | QG-4 Noether charge | PASS at FFT floor — U(1) $1.8\times10^{-13}$/1000 steps; chiral at machine zero |

**Subtests (F14.x):** The finding covers 16 sub-findings (14.1–14.16), including the GR-1 open-BC retest (14.15) and GR-2 open-BC retest (14.16) which both upgraded failing tests to passing.

---

## F15 — Closed-Form $\beta_\text{LV}(m)$: All Four LV Coefficients Derived

**Date:** 2026-05-19; amended 2026-05-22  
**Status:** Closed — four Tier 1 exact algebraic results.

Using implicit-function expansion of $\omega(u) = \arccos(n\cos u)$ and series inversion, four Lorentz-violation coefficients are derived in closed form:

$$\beta_\text{LV}(m) = \tfrac{1}{2}\!\left(1 - \frac{m}{\sqrt{1-m^2}\arcsin m}\right), \quad \beta_\text{LV} < 0 \text{ for all } m \in (0,1).$$

$$\gamma_\text{LV}(m) = \tfrac{1}{8} - \frac{m(3-2m^2)}{24(1-m^2)^{3/2}\arcsin m}.$$

$$\delta_\text{LV}(m) = \tfrac{1}{16} - \frac{m(8m^4-20m^2+15)}{240(1-m^2)^{5/2}\arcsin m}.$$

$$\varepsilon_\text{LV}(m) = \tfrac{5}{128} - \frac{m(35-70m^2+56m^4-16m^6)}{896(1-m^2)^{7/2}\arcsin m}.$$

All four confirmed by sympy to **bit-zero residual**. Leading small-$m$ expansion: $\beta_\text{LV} = -m^2/6 + O(m^4)$, so Lorentz violation is **zero in the massless limit** (Weyl sector is exactly Lorentz-invariant at this order).

The coefficients form an infinite tower; the pattern continues indefinitely with the recursion mechanical. At $m=0.5$, $k=0.05$: adding $\gamma_\text{LV}\beta^4$ improves fit by $6.3\times10^{-6}\to2.2\times10^{-8}$ (3 extra decimal places).

---

## F16 — GR-3 Fork Resolution: All Three Forks Fix the Factor-2; GR-4 Falsifies Fork C

**Date:** 2026-05-21  
**Status:** Closed for Fork C (falsified); Forks A and B remain viable.

All three proposed resolutions of the GR-3 Pound-Rebka factor-2 discrepancy work:

- **Fork A** (separate clock field): Pound-Rebka ratio $= 1.0001 \pm 2.3\times10^{-5}$.
- **Fork B** (anisotropic metric): ratio $= 1.0002 \pm 6.3\times10^{-5}$.
- **Fork C** (restricted-c): ratio $= 0.9998 \pm 5.7\times10^{-5}$.

However, Fork C predicts only **half the Mercury perihelion advance** ($\Delta\omega_\text{lat}/\Delta\omega_\text{GR} = 1.0006$ for A/B, but $0.4995$ for C). Fork C is therefore **falsified** by GR-4. GR-1 and GR-2 are unaffected by any fork ($|K|\approx3.85$, Shapiro ratio $\approx1.002$ identical across all).

The factor-2 problem is intrinsic to the single-scalar $c(\mathbf{x})$ ansatz; any decoupling mechanism (A, B, or C) removes it.

---

## F17 — Poynting Energy $\|E_G\|^2 + c^2\|B_G\|^2$ is Exactly Conserved

**Date:** 2026-05-21  
**Status:** Closed — Tier 1 exact algebraic + Tier 2 machine precision.

The Poynting energy density in the Mohr form (Eq. 55):

$$\|E_G\|^2 + c^2\|B_G\|^2 = \text{const}$$

is conserved for composite-photon propagation to machine precision. Derived analytically from the bilinear circularity identities $\mathbf{A}\cdot\mathbf{C} = 0$ and $\|\mathbf{A}\|^2 = \|\mathbf{C}\|^2$, which hold for helicity eigenmodes (Tier 1 #44). Per-step drift: $1.82\times10^{-16} \approx \varepsilon_\text{machine}$; over 10,000 steps: $1.82\times10^{-12}$ (linear accumulation, Tier 2 #10).

---

## F18 — Mohr C5/C6 Build: Nine New Tier-1 Identities, Three New Tier-2

**Date:** 2026-05-21  
**Status:** Closed.

Completed the remaining two Mohr (2010) gaps:

**C5 — Vector Spherical Harmonics (Mohr §8).** Built `_clebsch_gordan`, `_scalar_sph_harm`, `vector_spherical_harmonic`, `photon_ang_mom_eigenstate`. Tests:
- VSH orthonormality (Gauss-Legendre quadrature): $1.6\times10^{-15}$ — Tier 1 #35.
- Magnetic VSH transversality: $3.7\times10^{-17}$ — Tier 1 #36.
- Electric VSH transversality: $1.7\times10^{-16}$ — Tier 1 #37.
- $J_z$ eigenvalue (finite-difference): $1.1\times10^{-8}$ ($O(h^2)$ floor) — Tier 2 #12.

**C6 — Maxwell Green Function and Source Coupling (Mohr §C6).** Built `maxwell_hamiltonian_k`, `maxwell_green_function_k`, `maxwell_source_term`, `dirac_current_at_momentum`. Tests:
- Off-shell Green function inverse $(H-(\omega+i\varepsilon)I)\cdot G = I$: $5.2\times10^{-16}$ — Tier 1 #38.
- Weyl current $J^0 = 1$: $4.4\times10^{-16}$ — Tier 1 #39.
- Weyl current $|\vec{J}| = 1$: $2.2\times10^{-16}$ — Tier 1 #40.
- Weyl current $\vec{J} = \hat{n}$: $1.5\times10^{-15}$ — Tier 1 #41.

Two failures found and fixed: bilinear V6 packaging incompatibility (resolved by extracting $\hat\varepsilon_G = G_T/\|G_T\|$); $k_\mu J^\mu = 0$ is a continuum identity not satisfied on the QCA lattice (replaced by three structural identities).

---

## F19 — Area vs Volume Tick Scaling (Stub — No Run Data)

**Date:** 2026-05-21  
**Status:** Open — test specification only; no results.

This finding poses the question: does the number of ticking lattice cells inside a gravitational radius scale as $R^2$ (area law, 't Hooft CAI §9.4 Bekenstein bound) or $R^3$ (volume law, expected in flat space)?

The three hypotheses to test: H_vol ($\propto R^3$), H_area ($\propto R^2$), H_mixed (crossover). A run using `ca_curved.py` (Cayley exact-unitary) with the open-BC Poisson solver and binary tick counter $N_\text{binary}$ in the strong-field regime ($|\phi|/c_0^2 \in [10^{-2}, 0.5]$) would settle the question. **No run has been executed.**

---

## F20 — Photon-Fermion Propagation Demo

**Date:** 2026-05-21 (or nearby)  
**Status:** Closed — demonstration result.

A joint photon (composite bilinear) and fermion (Dirac 4-spinor) propagation demo confirms that the two sectors evolve correctly in tandem: the photon bilinear propagates at $c_\text{lat}$, the fermion wavepacket propagates at $v_g < c_\text{lat}$, and both maintain their respective norm conservation laws independently.

---

## F21 — Composite-Photon Curl Coefficient is Geometry-Independent: $c_\text{lat}/\sqrt{2}$

**Date:** 2026-05-22  
**Status:** Closed — Tier 1 exact algebraic (#49).

Testing five lattice geometries (BCC, simple-cubic, scaled-cubic $\alpha\in\{0.5,1,2\}$) the leading curl residual obeys the universal law:

$$\frac{\|\partial_t\mathbf{E}_G - i\,2\tilde{\mathbf{n}}\times\mathbf{B}_G\|}{(\|\mathbf{E}_G\|+\|\mathbf{B}_G\|)\,|k|} = \frac{c_\text{lat}}{\sqrt{2}},$$

to 6 figures across all geometries for $c_\text{lat} \in [0.5, 2]$.

**Key result:** Simple-cubic geometry gives $c_\text{lat} = 1$ but the curl residual coefficient is *larger* ($1/\sqrt{2} > 1/\sqrt{6}$), and the simple-cubic lattice has 8 Nielsen-Ninomiya doublers vs 1 for BCC. Geometry cannot fix the curl equation; the $O(k)$ residual is intrinsic to the **pointwise unsmeared bilinear**. The BCC is still the preferred geometry (fewest doublers, best isotropy).

---

## F22 — QCA Velocity Addition: Exact Deformed Formula from the Arccos Dispersion

**Date:** 2026-05-22  
**Status:** Closed — Tier 1 exact (four sympy bit-zero results) + Tier 2 machine precision.

The ratio of phase-momentum velocity to group velocity at $k\to0$:

$$\rho(m) = \frac{u_p}{u_g} = \frac{m}{\sqrt{1-m^2}\arcsin m} = 1 - 2\beta_\text{LV}(m),$$

confirmed symbolically (residual **0**) and numerically to $3.4\times10^{-14}$ (Tier 2 #13).

The deformed velocity-addition formula:

$$u'_\text{QCA} = \frac{u_g + v_g}{1 + 2\rho^2(m)\,u_g v_g},$$

with deviation from SR:

$$\delta u' \approx 8\beta_\text{LV}(m)\cdot u\cdot v\cdot(u+v) < 0.$$

The QCA **always predicts less velocity addition than SR** at finite mass. In the massless limit $\rho\to1$, $\delta u' = 0$: standard SR velocity addition recovered exactly. The leading LV coefficient is $8\beta_\text{LV}(m) \approx -4m^2/3$ at small $m$ (exact, sympy-confirmed).

---

## Cross-Cutting Observations

### The $\arccos$ dispersion resolves 't Hooft's Hamiltonian branch-cut ambiguity

't Hooft (CAI §5, Eq. 5.5) notes that the CA Hamiltonian $H_\text{op}$ is defined only modulo $2\pi/\delta t$ — this is an open obstruction in the CAI framework. The QCA arccos dispersion $\omega = \arccos(\cdot)$ is the **concrete resolution** for the class of propagators consistent with the five informational principles: it picks the principal branch $\omega \in [0,\pi]$, which is analytic near $\mathbf{k}=0$ and gives the well-defined LV expansion.

### The LV tower is the implicit-function expansion of $\arccos(n\cos u)$

The four closed-form LV coefficients are the first four terms of an infinite series whose $n$-th term is a rational function of $\arcsin m$ and $\sqrt{1-m^2}$, with $\arcsin m$ entering linearly in the denominator at every order. The series does not truncate; extending to $\beta^{10}$ requires only raising the series order in `derive_beta_LV.py`.

### Periodic-BC Poisson was the single largest GR accuracy bottleneck

Switching from the periodic-BC to the open-BC James/Hockney solver improved GR-1 from 12.5% off (FAIL) to 3.0% off (PASS) and GR-2 from 38% off (FAIL) to 0.06% off (PASS). The finding that "PBC is the bottleneck" (F14.9) was quantitatively confirmed by the controlled before/after comparison.

---

*End of Findings Summary. Cross-reference: `findings.md` (F1–F15), `findings/F16-F22.md` (F16–F22), `exactness-inventory.md`.*
