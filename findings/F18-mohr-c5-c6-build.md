# Finding 18 — Mohr §C C5/C6 build lands at machine precision; nine new Tier 1 identities, three new Tier 2

*Recorded 2026-05-21 - 20:08. Run: `ca-simulation/ca_maxwell.py`. Captured output: `test-results/mohr_c1_c6_results_2026-05-21.txt`. Doc: `mohr-c5-c6-build-plan.md`.*

## Background

The Mohr 2010 summary (`reference-research/mohr-2010-maxwell-photon-wf-summary.md` §C) listed six "gaps" — items in Mohr's continuum photon framework that our composite-photon construction lacked. C1–C4 had previously been implemented as `polarization_basis`, `longitudinal_mode`, `lorentz_boost_covariance`, and `composite_photon_energy_conservation` (Exactness Inventory Tier 1 #22–30, Tier 2 #7). C5 (angular-momentum eigenstates via matrix spherical harmonics, Mohr §8) and C6 (Maxwell Green function + source coupling, Mohr §C6) were still open. The Mohr summary also recommended refinements to C1–C4 — most notably the `c²` factor on the Poynting density and a direct bilinear-level V6 covariance test.

## Method

`ca_maxwell.py` gained four new sections in one build pass:

- **C1–C4 refinements.** A `c²`-weighted Poynting test (`composite_photon_energy_conservation_c2`) and a bilinear V6 transversality test using the polarization vector $\hat\varepsilon_G \equiv G_T / \|G_T\|$ extracted from the bilinear (`lorentz_boost_covariance_bilinear_transversality`).
- **C5 build.** `_clebsch_gordan` (sympy-backed, `lru_cache`'d), `_scalar_sph_harm` (closed-form Legendre recurrence), `vector_spherical_harmonic(j, m, l, θ, φ)` (CG-coupled VSH), the three transverse/longitudinal combinations `vsh_magnetic / vsh_electric / vsh_longitudinal`, and `photon_ang_mom_eigenstate(j, m, kind, θ, φ)` packaging the VSH into the 6-component Mohr spinor.
- **C5 tests.** `test_vsh_orthonormality` (Gauss-Legendre × uniform-φ quadrature), `test_vsh_transversality` (both magnetic and electric multipoles), `test_vsh_Jz_eigenvalue` (central finite difference on $L_z + S_z$).
- **C6 build.** `maxwell_hamiltonian_k`, `maxwell_green_function_k(ω, k, ε)`, `maxwell_source_term(J)` packaging Mohr's $\Xi = (-\mu_0 c J_s, 0)^T$, `dirac_current_at_momentum(k)` returning $J^\mu = (1, \hat n)$ for the BCC + Weyl eigenmode.
- **C6 tests.** Off-shell Green-function inverse $(H - (\omega + i\varepsilon)I)\cdot G = I$, structural identities for the Weyl current ($J^0 = 1$, $\|\vec J\| = 1$, $\vec J = \hat n$), and the source-term packaging shape check.

Two early failures forced spec changes:

1. The first cut of the bilinear V6 covariance test packaged `(E_G, ic\,B_G)` directly. The bilinear E/B carry a $G_T + G_T^\dagger$ structure that mixes positive- and negative-frequency modes, while V6 was constructed for single-frequency Mohr spinors $(ε, τ\cdot\hat k\, ε)$. The packaging is structurally incompatible. **Fix:** extract the polarization vector $\hat\varepsilon_G = G_T/\|G_T\|$ from the bilinear's transverse part, then run the standard Mohr V6 test on $\hat\varepsilon_G$. Residual dropped from 1.1 → $2.9 \times 10^{-15}$.

2. The first cut of the C6 current-conservation test computed $k_\mu J^\mu = \omega J^0 - \vec k \cdot \vec J$ and expected $= 0$. This is a continuum statement and does not carry over: the QCA has $c_\text{lat} = 1/\sqrt{3} \ne 1$, so $\omega = c_\text{lat}|k| < |k| = \vec k \cdot \hat n$. **Fix:** replace with three structural identities that hold exactly on the lattice for the helicity-+ Weyl eigenmode — $J^0 = 1$, $\|\vec J\| = 1$, $\vec J = \hat n$ (the BCC eigenmode's spin axis, $\to \hat k$ in the continuum limit). All three land at $\le 1.5 \times 10^{-15}$.

## Results

Complete run (`test-results/mohr_c1_c6_results_2026-05-21.txt`):

| Test | Residual | Tier |
|---|---|---|
| C1 polarization transversality | $1.6\times 10^{-16}$ | Tier 1 #22 (pre-existing) |
| C1 polarization orthonormality | $5.5\times 10^{-16}$ | Tier 1 #23 |
| C1 polarization completeness | $4.4\times 10^{-16}$ | Tier 1 #24 |
| C2 longitudinal H ψ_L = 0 | $5.5\times 10^{-17}$ | Tier 1 #28 |
| C2 longitudinal ψ_T†ψ_L overlap | $1.1\times 10^{-16}$ | Tier 1 #29 |
| C2 longitudinal Π^T ψ_L = 0 | $3.7\times 10^{-17}$ | Tier 1 #30 |
| C3 V6 covariance transversality | $1.3\times 10^{-15}$ | Tier 1 #25 |
| C3 V6 covariance form | $5.1\times 10^{-16}$ | Tier 1 #26 |
| C3 V6 covariance xi magnitude | $6.7\times 10^{-16}$ | Tier 1 #27 |
| C4 Poynting drift (200 steps) | $4.5\times 10^{-14}$ | Tier 2 #7 |
| **C4 refinement: Poynting with c² (200 steps)** | $4.8\times 10^{-14}$ | **Tier 2 #10** (new) |
| **C3 refinement: V6 transversality of ε_G** | $2.9\times 10^{-15}$ | **Tier 2 #11** (new) |
| **C5 VSH orthonormality (j ≤ 2)** | $1.6\times 10^{-15}$ | **Tier 1 #35** (new) |
| **C5 magnetic VSH transversality** | $3.7\times 10^{-17}$ | **Tier 1 #36** (new) |
| **C5 electric VSH transversality** | $1.7\times 10^{-16}$ | **Tier 1 #37** (new) |
| **C5 VSH J_z eigenvalue (finite-diff)** | $1.1\times 10^{-8}$ | **Tier 2 #12** (new, $O(h^2)$ floor) |
| **C6 Green function inverse off-shell** | $5.2\times 10^{-16}$ | **Tier 1 #38** (new) |
| **C6 Weyl current J⁰ = 1** | $4.4\times 10^{-16}$ | **Tier 1 #39** (new) |
| **C6 Weyl current \|\vec J\| = 1** | $2.2\times 10^{-16}$ | **Tier 1 #40** (new) |
| **C6 Weyl current $\vec J = \hat n$** | $1.5\times 10^{-15}$ | **Tier 1 #41** (new) |
| **C6 source-term lower half = 0** | $0.0$ exact | **Tier 1 #42** (new) |
| **C6 source-term upper half = $-\mu_0 c M J$** | $0.0$ exact | **Tier 1 #43** (new) |

Inventory tally moves from 34 → **43 exact algebraic** results and 9 → **12 machine-precision** results.

## What this shows

1. **The Mohr §C gap is closed at the primitive level.** Six items, all six now have working implementations with passing tests at the appropriate exactness tier. The two refinements to C1–C4 (Poynting with $c^2$; bilinear-derived ε V6 covariance) extend the existing C1–C4 coverage to the form Mohr explicitly recommends.

2. **VSH orthonormality at $1.6 \times 10^{-15}$ over a $20 \times 20$ quadrature** establishes that our CG coefficients + scalar spherical harmonics are correct to the linear-algebra round-off floor. The standard textbook decomposition $Y^m_E = \sqrt{(j+1)/(2j+1)} Y_{j,j-1} + \sqrt{j/(2j+1)} Y_{j,j+1}$ (Varshalovich §7.3) is what passes; the alternate sign/coefficient convention I first tried (and which appears in some references) fails transversality by $\mathcal O(0.5)$. Recorded here to save the next person the bug hunt.

3. **The continuum $k_\mu J^\mu = 0$ current conservation does not hold on the BCC QCA.** The dispersion $\omega = \arccos(u(k)) \approx |k|/\sqrt 3$ guarantees $\omega \ne |k|$, so the naive Lorentz-form conservation is violated by $\mathcal O(1)$ even at small $k$. The lattice-native exact form is the three structural identities $J^0 = 1$, $\|\vec J\| = 1$, $\vec J = \hat n$. This is consistent with [[finding-14-7-qg2-planck-LV]]: the lattice has Lorentz-violation residuals of size $\beta_\text{LV}(m), \gamma_\text{LV}(m)$, and naive current conservation is one place where they manifest.

4. **Bilinear-derived polarization vectors are equivalent to abstract polarization vectors under V6.** Once $\hat\varepsilon_G \equiv G_T/\|G_T\|$ is extracted from the bilinear, the V6 boost test passes at $2.9 \times 10^{-15}$ — same precision as the original `lorentz_boost_covariance` on abstract $\hat\varepsilon$. The bilinear and Mohr's continuum polarization are interchangeable for the purposes of Lorentz-covariance testing.

## Caveats and what this does NOT establish

- **The deferred §C6 application** — actually computing a radiation field from a localized Dirac current via $G(\omega, k)$ — is not done. The primitives are in place; the coupled-sector run is parked under "future Phase G" in the Mohr summary.
- **C5 radial wave functions** (Mohr Eqs. 391–393) are not built. Only the angular part (VSH) is here. The radial extension is gated on needing an atomic transition matrix element.
- **$J_z$ eigenvalue test uses a central finite difference at $h = 10^{-4}$.** The $1.1 \times 10^{-8}$ residual is the expected $O(h^2)$ truncation floor, not algebraic exactness. The identity is exact by CG construction; the test confirms the construction implements it.
- **The Mohr $V6$ matrix and our Weyl QCA boost are not algebraically identified.** We verified $V6$ preserves transversality on bilinear-derived polarization vectors, but did not implement the Weyl SL(2,$\mathbb C$) boost and verify it produces the same boosted bilinear. That would be the cleanest test of "the composite photon is Lorentz-covariant *as a composite object*"; it is a future extension.

## Status against the theory's bar

Per the project standard (a theory must reproduce existing measurements and either explain them better or extend them): this build does not extend physical scope but consolidates the photon sector to match Mohr's continuum framework at machine precision, closes six gap items, and adds nine algebraic identities to the exactness inventory. It also surfaces one falsifiable continuum claim that fails on the lattice (current conservation), which is consistent with the model's documented Lorentz-violation structure (Finding 15).

## Cross-references

- Predecessor: Mohr 2010 §C, summarised in `reference-research/mohr-2010-maxwell-photon-wf-summary.md`.
- Build plan: `mohr-c5-c6-build-plan.md` (status table for C1–C6).
- Code: `ca-simulation/ca_maxwell.py` — sections "C1–C4 refinements", "C5 — Photon angular-momentum eigenstates", "C6 — Source coupling and Maxwell Green function".
- Inventory entries: `exactness-inventory.md` Tier 1 #35–43, Tier 2 #10–12.
- Captured run: `test-results/mohr_c1_c6_results_2026-05-21.txt`.
- Related findings: Finding 7 (composite-photon curl), Finding 15 (closed-form Lorentz-violation coefficients $\beta_\text{LV}, \gamma_\text{LV}$).
