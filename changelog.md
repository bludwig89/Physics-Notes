# Changelog

Non-trivial software changes and decisions for the Physics Notes simulation work.

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

### Model review — nonsensical or self-inconsistent constructs flagged

Per CLAUDE.md's request to keep the proposition honest about which equations are exact, which are machine-precision, and which are heuristic. The list below is the residue after reading `ca-unified-proposition.md` (v1), `ca-unified-v2.md`, `ca-f3-propositions.md`, `ca_emqg.py`, `ca_curved.py`, `ca_unified.py`, `ca_maxwell.py`, `ca_bcc.py`, and the run-tests. Items are ranked by how much they actually distort a result vs how cosmetic they are.

**Substantive (the result is wrong or unsupported as currently stated):**

1. **`ca-unified-v2.md` line 48 publishes the wrong-sign `c(φ)` formula.** The document writes
   $$c(\mathbf{x}, t) = c_0\left(1 + \frac{\phi(\mathbf{x}, t)}{c_0^2}\right)^{-1}$$
   and labels it "Paper 6, Eq. 18.31 reduction." For $\phi<0$ in a gravitational well this gives $c > c_0$ — light *speeds up* near a mass, the opposite of GR lensing. The working code in `ca_emqg.py::c_field_from_phi` uses the GR-Shapiro form $c = c_0/(1 - 2\phi/c_0^2)$ which gives the correct direction, and the changelog 2026-05-15 records the fix. The v2 *proposition document* was never back-fixed, so anyone re-implementing from the doc will hit the same bug. Also, Paper 6 Eq. 18.31 is the Fizeau additive-velocity formula for a *moving* refractive medium — not the static gravity case — so the citation is wrong even after the sign is fixed. The relevant Paper-6 expression is closer to Eq. 18.51–18.52 ($c(t) = c_0(1 \pm gt/c_0)$). **Action:** back-fix `ca-unified-v2.md` lines 46–50.

2. **F3b uses `c(x) = c₀·(|Φ|/v)^(+α)` but `ca-unified-proposition.md` line 69 publishes `(-α)`.** The two are off by a sign and have been since 2026-05-16's P3 commit. F3b passes only because the test code carries the corrected `+α`; the v1 proposition document still has `(-α)`, which would give *repulsion* away from a |Φ| depression. The exponent $\alpha = 1.5$ itself is a free fitting parameter with no derivation — distinct from the sign question. **Action:** either back-fix v1 to `(+α)` (recommended; it is what the test exercises) and document that v2's EMQG-Poisson route is the supersession, or mark v1 line 69 as retired with a pointer to v2 S1.

3. **The Yukawa Hamiltonian density carries a `c²` factor that has no Standard-Model counterpart.** `ca_unified.py::total_energy` and the symplectic kick in `unified_step` both use
   $$H_Y = c^2 \cdot y \cdot (\Phi\,\eta^\dagger\chi + \Phi^*\,\chi^\dagger\eta)$$
   whereas the SM Lagrangian is $\mathcal L_Y = -y\,(\Phi\,\bar\eta\chi + \Phi^*\,\bar\chi\eta)$ with no $c^2$. The internal justification ("matches the Dirac stepper's $m c^2 \beta$ mass-Hamiltonian convention") is a units kludge: the Dirac stepper folds $c$ into the mass-rotation generator rather than into the kinetic operator, so the Yukawa coupling must absorb the same factor to keep the joint Hamiltonian self-consistent. The factor is not wrong *within this code*, but it means the value of the Yukawa coupling reported (e.g. `y=0.2` in F3, `y=0.6` in F1/F4) is not a physical coupling — it is a lattice coupling that has to be re-scaled by $c^2$ to compare to anything published. **Action:** rename `yukawa` parameter to `yukawa_lattice` in the API, or refactor the Dirac stepper to keep $c$ in the kinetic generator so $H_Y$ is sign-clean.

4. **The L4 EMQG Poisson is 2-D but is being scored against a 3-D Newtonian deflection target.** `ca_emqg.py::solve_poisson_2d` solves $\nabla^2\phi = 4\pi G\rho$ on a 2D periodic lattice. In 2D the Green's function of $\nabla^2$ is *logarithmic* ($\phi \sim 2GM \ln(r/r_0)$), not $1/r$. The lensing test then reports "Δ(2M)/Δ(M) = 1.83, 8.5% off the expected 2.0" — and labels 2.0 as the Newtonian target. But the Newtonian $\Delta\theta = 2GM/(bc^2)$ scaling that delivers a clean linear-in-M ratio is a 3-D result. In 2D the deflection through a logarithmic potential depends on the long tail of $\ln(R/b)$ where R is the box edge, and the M-scaling depends on whether the test is weak-field (linear) or finite (sublinear). The 1.83 figure is therefore not a 8.5% miss on a 3-D Newtonian benchmark; it is a measurement of how close a 2-D log-potential deflection happens to be to a 3-D linear-M scaling for one specific source profile, box size, and impact parameter. **Action:** either go to 3-D (`solve_poisson_3d` would be a few lines of additional code on the FFT spine), or change the pass criterion to one that is right for 2-D logarithmic gravity (e.g., $\Delta\theta \propto \ln(R/b) - \ln(R/b')$ at fixed mass).

5. **`maxwell_curl_residual` is labeled L3 INFO but the residual is $O(k)$, not $O(k^3)$.** Paper 1 Eq. 35 says the composite-photon bilinear obeys the free Maxwell curl equations; the implementation gives a normalized residual of $0.408\,k$ — a *fractional* deviation that does not go to zero as $k \to 0$. `findings.md` Finding 2 already captures this carefully. The substantive worry is that L3 is reported as "3/3 PASS + 1 INFO" — the INFO note carries the failure of the central Maxwell identity, so labeling the layer "PASS" is generous. The dispersion ($\Omega_\gamma = |\mathbf{k}|/\sqrt 3$ at 0.21%) and transversality ($2\tilde{\mathbf{n}}\cdot\mathbf{E} = 0$ at $4.6 \times 10^{-17}$) tests *do* pass cleanly, but they are kinematic — they would hold for any anisotropic-dispersion construction with the right symmetry, not just for one obeying Maxwell. **Action:** demote L3 to "L3 partial — dispersion + transversality only" until the smeared-photon construction lands, or split into L3a (kinematic) and L3b (Maxwell curl).

6. **The legacy 3-D simple-cubic Weyl/Dirac code in `ca_core.py` is structurally trivial as a QCA.** Papers 1 and 2 prove that on a 3-D simple-cubic lattice with $s=2$ (2-spinor cells), only the identity-shift automaton satisfies the QCA axioms (linearity, locality, unitarity, homogeneity, isotropy). What `ca_core.py::weyl_step_3d_splitstep` actually computes is the FFT propagator of the *continuum* linearized Weyl equation tabulated on a simple-cubic grid — a finite-difference / spectral method, not a CA. That is fine numerically (it converges to the right small-$k$ Weyl dynamics), but the documentation calling it "the 3-D Weyl CA" is overstated. v2 introduces `ca_bcc.py` as the actual non-trivial 3-D QCA. The legacy 3-D code is still in the test pipeline. **Action:** retitle the 3-D simple-cubic functions to `weyl_propagator_3d_splitstep` (no "CA"), keep them in the suite as the linearized-Weyl reference, and route any "is this a QCA?" claim through `ca_bcc.py`.

**Cosmetic (the result is right but the framing is misleading):**

7. **F3's pass criterion is `1e-6 < max|Φ−v| < 10`** — a 7-orders-of-magnitude band. Calling F3 "PASS" tells a casual reader that something specific was verified; the actual claim is only that "the back-reaction is non-trivial and does not diverge." The latter framing is what `run_phaseF_tests.py` line 219–230 actually exercises, and the comments are honest about it ("Φ deflection observed at fermion location"). The PASS/FAIL surface above the comments is the cosmetic miscue.

8. **`mu2_neg = -0.5` in F4 is a convention-flip trick**, not a separate parameter. The Mexican-hat stepper takes a single `mu2` arg and the potential is hard-coded as $V = -\mu^2|\Phi|^2 + \lambda|\Phi|^4$. F4 passes a *negative* value to flip the sign of the quadratic term and recover the symmetric vacuum. This works but is brittle: anyone who reads the stepper signature and then runs F4 will see `mu2=-0.5` and wonder why $\mu^2$ is negative. **Action:** split the Higgs API into separate `mu2_squared` and `quartic_coefficient` arguments with explicit signs, or expose a `phase='broken' | 'symmetric'` flag.

9. **`maxwell_curl_residual` carries an unused placeholder assignment** at `ca_maxwell.py` line 171:
   ```python
   psi, phi_eig, omega_half = bcc.bcc_unitary(kx_h, ky_h, kz_h, sign='+'), 0, 0  # placeholder
   psi_p, psi_m, omega_half = weyl_eigenmodes_3d_bcc(kx_h, ky_h, kz_h, sign='+')
   ```
   The first line is immediately overwritten by the second. Iteration leftover.

10. **`qca-papers-1-4-overview.md` line 53 still has the Paper 1 Eq. 15 sign typo on the second term of $\tilde n_y$.** `ca_bcc.py::_bcc_uvec` carries the corrected sign inline; `findings.md` Finding 1 documents the derivation. The reference doc has not been back-fixed, so anyone reading the doc and re-implementing will hit the same unitarity failure (max $|u^2 + |n|^2 - 1| = 0.47$ at finite $\mathbf{k}$).

11. **"Speed of light" `c` is overloaded across three meanings.** In `weyl_step_2d_splitstep` it is the unitary-rotation magnitude per tick (dimensionless, free in $[0, 1]$). In `c_field_from_phi(phi, c_0=0.5)` it is the *macroscopic* lattice light-speed parameter. In `H_Y = c²·y·…` it is an *energy unit*. The same Python variable `c` is reused for all three. Dimensionally fine in natural units, but mixed up enough that a reader cannot tell from `c=0.5` which interpretation is meant. **Action:** rename to `c_unitary`, `c_macro`, `c_energy_unit` in the three locations.

12. **F3b reports a single "deflection observed" pass/fail.** A quantitative Newtonian check would scan over impact parameter $b$ and verify $\Delta y \propto 1/b$. The current test only confirms the *sign* of the deflection at one $b$. The 10× lattice bump is a natural occasion to add the $1/b$ scan, since the new lattice can resolve $b \in \{60, 120, 180, 240, 300\}$ cleanly.

13. **`dt=1.0` is the implicit time step almost everywhere.** Because the split-step FFT propagator is unconditionally stable, the choice does not threaten correctness, but it means the test suite has zero coverage of `dt → 0` convergence. Anywhere the propagator's spatial dispersion is anisotropic (BCC, exact-arccos), checking that residuals scale as $\mathcal O(dt^2)$ when `dt` is halved would catch a class of order-of-accuracy bugs that the current suite cannot see.

14. **No discrete-current-conservation check** for the U(1) or SU(2) gauge sectors. E1 verifies the Aharonov–Bohm phase pickup at $4.4 \times 10^{-16}$ and E2 verifies parity-violation populations, but neither tests the discrete Noether identity $\partial_\mu J^\mu = 0$ on the lattice. The total-norm conservation tests are weaker — they verify that *integrated* charge is conserved, not that the local current is. For a CA claiming to realize gauge dynamics, the local conservation is the more characteristic check.

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
