# Model Map — Flags and Follow-ups

*2026-09-29 - 00:00. This file collects every flag raised while mapping the code, with its file:line: `⚠ DOC/CODE MISMATCH`, `SUPERSEDED`, `UNREGISTERED`, exactness `unknown`, and equations that couldn't be pinned down. **Nothing here has been fixed in code.** This task maps the model; it does not change it. Each item still needs its own triage, and where it touches physics, its own finding.*

The kinds were normalised when the per-section flag files were merged:

- **UNREGISTERED module** is a `.py` with no module-registry record.
- **UNREGISTERED constant (D7)** is a numeric literal that bypasses `casim.constants` or has no recorded `Site`/`MeasuredConstant`.
- **REGISTRY GAP** is a registered module whose `findings`/`exactness` fields are empty or stale.
- **EXACTNESS unknown** means the module registry has no `exactness` and no inventory row covers the equation. About half the registry's modules are in this state. The equation tables mark these rows `unknown (inferred: …)`, keeping the mapper's reading as information only.

## Priority follow-ups (likely defects, not documentation drift)

These are the items where the mapper judged the **code** probably wrong, or where a check cannot fail. They are unconfirmed; each needs a look before anything is changed.

| # | Where | What |
|---|---|---|
| 1 | `src/casim/particles/channel.py:L1438` | `min(rms_c, 0.0)` is always ≤ 0, so the photon source is always a point and `rms_c` is dead. Probably meant `max`. (09-shims) |
| 2 | `engine/gauge/colour_condensate.py` `u1_metropolis_3d` | The checkerboard update reuses staples that are stale across parities, which breaks detailed balance. ρ(β) → m_D → v → σ_F86 inherit the error. (05a) |
| 3 | `engine/particles/dirac_bcc.py` / `dirac.py` variable-mass step | The mass-correction rotation has the opposite sense to the main Dirac step, so a local δm enters with the wrong sign. Confined quarks run on this step. (06b) |
| 4 | `engine/core/observers.py` `Momentum` | Raises `TypeError` on a colour-stacked spinor (reproduced). (04) |
| 5 | `engine/gauge/em_photon_sourcing.py:L217/L223` | The transverse E is sourced with $+g\,J$; the longitudinal E is solved from $+\rho$ with no $g$. The coupling is inconsistent between the two sectors. (05b) |
| 6 | `engine/gauge/weak_wmu.py` `w_self_interaction_step` | The sign of the W² term disagrees with the rest of the module. (05c) |
| 7 | F91 classification versus code | The Z has no vector/axial split; the massive W is even; the β-decay pipeline propagates W⁻ with the even law; `charge_coupling.maxwell_curl_step` is labelled "even" but rotates by $\lvert C_\text{odd}\rvert$ (they agree only at $O(k^3)$). (05a, 05c) |
| 8 | `constants/lepton.py:L117` · `derive_lambda6_sextic.py:L132` | $\lambda_6=\lvert B\rvert/(2e^6\cos\tfrac23)$ evaluated with the registry's own $B$ and $e$ gives 0.2334, not the registered 0.243. The code reaches 0.2433 only with $e=\sqrt3\,\bar y$ from PDG. Separately, `derive_generator_norm.py` imports $\lambda_6$ as an **input**. (01, 06a) |
| 9 | `derive_higgs_bhl_compositeness.py` vs `derive_M_R_scale_link.py` | Two "model cutoff" definitions, both citing F107, differ by exactly $\sqrt{8\pi}$ (1.85e18 vs 9.28e18 GeV). (06a) |
| 10 | `interactions/qed_euler_heisenberg.py`, `qed_ir_bremsstrahlung.py` | The returned $n_\parallel-1$ is a factor 2 below the textbook value. Bremsstrahlung uses α/π where its docstring says α/2π. (07c) |
| 11 | `forks/gravity/dirac_gravity_fork.py`, `gr_fork_F46_dirac.py` | The rest leg rotates by $\sqrt A\,m$, not the documented $\sqrt A\arcsin m$. The tests pass only because a near/far ratio hides the ~1% difference. (08a) |
| 12 | `forks/gravity/gr_fork_F64_em_connection.py` | The D-EM1 impedance check is True for all three placements, so it cannot discriminate. D-EM1/5/7 still run on the excluded $K=(1-u)^{-2}$. (08a) |
| 13 | `forks/gravity/gr_fork_F216/F223/F228/F238_*.py` | These run physics and **write `test-results` JSON at import**, with no `__main__` guard. That breaks the CLAUDE.md §5 rule. (08b) |
| 14 | `interactions/running_ir_coupling.py`, `running_gap_solve.py` | Both use the midpoint of the bracketed `alpha_eff_star` as a result, which breaks the D7 bracket rule. (07e) |
| 15 | `interactions/superconductivity.py:L636, L723` | The literal 6.0299 is used where the module's own derivation gives 6.02921 (relative difference 1.1e-4). (07e) |
| 16 | `cosmology_lattice_elasticity.py` vs `cosmology_lambda_dynamics.py` | The two modules use SI tick conventions that differ by $\sqrt3$. (07a) Related: the walk-hop and geometry-hop units also differ by $\sqrt3$ (03). |
| 17 | `lattice/time_generator_axiom_independence.py` (F377) | The default packet wraps the periodic box (~20% of its weight sits at the edge by t=40), which contaminates the fitted exponent. (03) |
| 18 | `numerics/benchmark.py`; `numerics/backends.py` | The benchmark runs when the module is imported. The float32 guard (MLX/JAX) is bypassed when the backend is chosen via `use()`/`set_backend`. (02) |
| 19 | `interactions/qed_uv_completion.py` | Registered `exact`, but most of its legs are quadratures or solves with tolerances. (07c) |
| 20 | `CLAUDE.md` decision 2 table | It names `ca_wmu._f26_rotation_step` → `gauge.wmu`; the module is `gauge.weak_wmu`. (05c; CLAUDE.md is not edited by this task) |

## ⚠ DOC/CODE MISMATCH (147)

| Section | Module | Where | Detail |
|---|---|---|---|
| 01-constants / 02-numerics | constants/lepton.py | lepton.py:L117 (lambda_6) | Derivation string λ6 = \|B\|/(2e⁶cos(2/3)) evaluated with the registry's own B_sea_cubic=-0.0569 (L168) and e_saturation=0.733 (L188) gives 0.2334, not the registered 0.243 (4% off, 8× its tol 5e-3). 0.243 needs e≈0.728. F234 L39 quotes 0.243 from the same inputs. Not settled. |
| 01-constants / 02-numerics | constants/strong.py | strong.py:L212-219 (alpha_eff_star) | Registered bracket (0.376, 0.411) is the F88/F117 scale choices; the same derivation string also says F154 brackets it to [0.31, 0.38] with 0.39 at the top, which excludes the registered hi endpoint 0.411. |
| 01-constants / 02-numerics | numerics/backends.py | backends.py:L71 use(), L276-278 MlxBackend docstring | Float32 gate (precision.require_float64) runs only on the CASIM_BACKEND env path (L353-357). backends.use("mlx") / fft.set_backend("mlx") activate MLX (and a non-x64 JAX) with no check, contrary to the docstring and CLAUDE.md "refuses to activate unless CASIM_ALLOW_FLOAT32=1". |
| 01-constants / 02-numerics | numerics/backends.py | backends.py:L16 | The docstring says the protocol is 7 methods (6 FFTs + chiral_transform); fft.py also requires rfftn/irfftn/rfft/irfft on every backend. No backend implements chiral_transform (_Base raises, L114). |
| 01-constants / 02-numerics | numerics/fft.py | fft.py:L22-24 vs L190 fft_floor_estimate() | The docstring floor is "~eps×log2(N)", ≈5e-14 at 64³. The function returns eps·log2N·√N = 2.05e-12 at 64³, and the docstring's own formula gives 4.0e-15. |
| 03-lattice | lattice.bcc | bcc.py:L52 vs L235 | The docstring advertises `weyl_step_3d_bcc(f, g, c=1.0/√3, sign)`, but the function takes no `c` argument. |
| 03-lattice | lattice.bcc | bcc.py:L137–140 vs L109 | The continuum limit n̂→(kx,−ky,kz)/\|k\| holds only for sign '+'. For '−' the code gives (kx,+ky,kz)/\|k\| (spot-checked). |
| 03-lattice | lattice.blockspin | blockspin.py:L447 | The docstring names `ca_wmu._f26_rotation_step`, but the code imports `gauge.weak_wmu._f26_rotation_step`. Only the name is stale. |
| 03-lattice | lattice.poisson_open | poisson_open.py:L28–29, L39–40 vs L115–135 | The docstring claims free-space 1/r is recovered "to machine precision". The code is a discrete Green's convolution with an r_min=0.5 cutoff, so the far field is only discretisation-accurate. |
| 03-lattice | lattice.time_signature | time_signature.py:L859–866 vs L141–153 | The `report()` verdict still states "d_time = rank su(2), d_space ≤ dim su(2), 3+1 rests on ONE input". The banner withdraws that identity as numerology. |
| 03-lattice | lattice.time_signature | time_signature.py:L858 | `imported_step: "Abel's theorem"` is stale. The banner corrects the source to Dubickas–Steuding, and F316 (laurent_pell.py) discharges the import. |
| 04-core | core.channel / core.coupled | channel.py:L19-39 vs coupled.py:L198, L252 | The `field_energy` docstring says the engine now has one ½ convention, but `ChargePhotonChannel.energy` and `BetaDecayChannel.energy` still return Σ(E²+B²) without the ½. |
| 04-core | core.coupled | coupled.py:L163 vs L194 → charge_coupling.py:L238-289 | `charge_photon` is labelled "paired photon (F69)" / even, but it rotates at the curl-symbol rate dt·\|C(k)\|, not Ω_pair (F387 treats these as different functions). |
| 04-core | core.channel | channel.py:L92-106 | The `Channel.step` docstring still says channels are stepped in "registration order"; since P3.3 the order is the bus-resolved `applied_order` (simulation.py:L220-228). |
| 04-core | core.channel / core.graph | channel.py:L133-141 | The `provides()` docstring says channels publish named quantities (J_em, T00, A_mu, sqrt_A); no channel overrides it, so the bus resolves channel names only and the exchanged keys are never type-checked. |
| 04-core | core.lpt_generator | lpt_generator.py:L78-80 vs L243, L130 | A comment says the gauge field sits at the link BASE site; the expansion uses the MIDPOINT s+ρ̂/2. |
| 04-core | core.lpt_generator | lpt_generator.py:L411 vs L398-405 | The 3-gluon statement string says "Bose-antisymmetric"; the check and comment test symmetry (v1−v2=0). |
| 04-core | core.manybody | manybody.py:L4 | The module docstring still names the file `ca_manybody.py`. |
| 05a-gauge | gauge.charge_coupling | charge_coupling.py:L267-288 maxwell_curl_step(); src/casim/README.md:L110,L113; charge_coupling.py:L27-30 | README labels charge_photon / photon_sourced channels "even", and the docstring says the paired photon propagates by the even law. The step actually rotates by θ=\|C_odd(k)\| (odd part of the branch-'+' n(k/2)), not Ω_even=ω⁺(k/2)+ω⁻(k/2). They agree only at O(k³); on the x-axis 2sin(k/2√3) vs k/√3 (1.0916 vs 1.1547 at k=2). |
| 05a-gauge | gauge.bilinear | bilinear.py:L2109 vs L2153 planck_correction_prediction() | Docstring gives δv/c ≈ −c_lat²k²/6 = −k²/18 (quadratic). Code uses −k/18 (linear), and a spot-check confirms linear −k/18 for branch '+' on (1,1,1). The dispersion_nonlinearity return doc also calls it "O(k²)". |
| 05a-gauge | gauge.bilinear | bilinear.py:L1535 vs L1615 real_rotation_vs_maxwell_curl() | C8 header writes E(t+1)=cosΩ E + sinΩ (k̂×B); code has no cross product (cosΩ E + sinΩ B), and an inline comment admits it. |
| 05a-gauge | gauge.bilinear | bilinear.py:L497-498 vs L528-530 maxwell_curl_residual() | Docstring step 4: ψ→e^{−iω}ψ, φ→e^{+iω}φ. Code evolves both by e^{−iω}, per its own inline correction. |
| 05a-gauge | gauge.bilinear | bilinear.py:L72 (module docstring) | rotation_step_em_spectral is still listed as the "EXACT EM propagator (rotation law) ← primary"; it is the retired single-branch chiral σ-bilinear law (F67–F69; F306 inventory #49/#51). |
| 05a-gauge | gauge.chiral_anomaly | chiral_anomaly.py:L207 and L404 vs L267, L462 | Docstrings of gamma5_basis_symbolic and fujikawa_anomaly_symbolic say Tr[γ5 σσ] = −4iε; code (and module header L34) assert +4iε. |
| 05a-gauge | gauge.colour_dielectric | colour_dielectric.py:L210-211 vs L225 string_tension_numeric() | Docstring potential term ¼(f²−1)²; code and Part-A comment use ½(f²−1)². |
| 05a-gauge | gauge.colour_dielectric | colour_dielectric.py:L630-632 vs L643-650 gluon_dielectric_evolve_2d()/_bcc() | Claims a "2nd-order-in-dt split-step"; the update X+s(RX−X) is a convex blend, not norm-preserving for 0<s<1, and its order is never verified. |
| 05a-gauge | gauge.casimir_ladder | casimir_ladder.py:L20-49 vs L219-323 operator_consistency() | Module header presents "C7 carries 1/C_F" and "identity only for N≤3" as results; the later operator-consistency audit (L6 leg) shows both come only from the mixed Z_N-vs-C₂ matching (χ=1/(4g²) for all N when one operator is used). The header was not revised. |
| 05a-gauge | gauge.casimir_scaling | casimir_scaling.py:L361-366, S4 labels vs L73-91 | F325 re-characterisation (in-file) says Casimir scaling measures representation content, not H2; the engine_verdict string and gate labels still read "excludes centre dominance / says H2". |
| 05a-gauge | gauge.colour_theta | colour_theta.py:L209-215 random_su3_links_4d() | "Geodesic pull towards the identity" is actually linear interpolation (1−s)I+sU plus QR re-unitarisation. |
| 05a-gauge | gauge.bilinear_2d | bilinear_2d.py:L184 | maxwell_dispersion_residual_2d docstring calls the deviation "the BCC lattice's nonlinear dispersion"; the module is the 2-D square lattice. |
| 05a-gauge | gauge.bcc_action | bcc_action.py:L377-384 vs L1400-1427 | Section comment says β_t=β_s is "a convention, flagged, not a result"; the same file later derives β_t/β_s=4/(3c_lat²)=4 (inventory #233). Stale comment. |
| 05b-gauge | derive_coupling_normalisation | derive_coupling_normalisation.py:L134–136 | Comment says the F280 target is "not written as a literal", but `F280_TARGET_LAMBDA_RATIO = 1.773444` is a literal. The "band rebuilt here" rests on literal inputs (L128–133). |
| 05b-gauge | derive_gauge_boson_masses | derive_gauge_boson_masses.py:L76, L81 vs L398–409 | Docstring quotes +0.222 %/+0.158 %; code checks 0.221/0.157. Docstring calls the c²/s²-in-Δr leg "B4c"; in code it is B4d. |
| 05b-gauge | derive_ncolour | derive_ncolour.py:L210 vs L214 | Comment says ratios are normalised to y_Q = 1/6; code normalises y_Q = 1 (v/v[0]). |
| 05b-gauge | derive_ncolour | derive_ncolour.py:L104 vs L770–777 | Docstring says the F280 band keeps N_c in [2.90, 3.00]; in-code comment records measured [2.898, 3.110]. |
| 05b-gauge | derive_premise_a_irreducibility | derive_premise_a_irreducibility.py:L67–71 vs L129–138 | Docstring S1 lists "constituent" as a scanned token; `_COLOUR_TOKENS` excludes it. |
| 05b-gauge | derive_x1_branch | derive_x1_branch.py:L472 | branch_verdict hardcodes branch-B α_s(M_Z) = 0.11954; docstring L11 says 0.1186, and `_run_to_mz(1/16π)` = 0.11858. |
| 05b-gauge | em_current | em_current.py:L75, L410 vs L467, L474 | Docstring claims continuity / longitudinal sector unchanged "bit-identical, to the last ULP"; gate tolerances are 1e-12 and 1e-10. |
| 05b-gauge | hypercharge | hypercharge.py:L204–205 vs L236–241 | Docstring says E_phase acts "on the isospin index AFTER U"; code applies D(α) to χ before U (U·D). The matrix is consistent; the wording is reversed. |
| 05c-gauge | weak_wmu | weak_wmu.py:L682 _f26_rotation_step() | Docstring: "Ω_even → 2c\|k\| = Ω_+ = Ω_-" in the continuum; code Ω = ω⁺(k/2)+ω⁻(k/2) → c_lat\|k\| (spot-check slope 0.57735). |
| 05c-gauge | weak_wmu | weak_wmu.py:L1934, L1939–1940 w_massive_propagation_step_spectral() | Docstring: at m_W=0 reduces to `w_propagation_step_spectral` — that name is now the chiral alias (L926); massive step reduces to the even `_f26_rotation_step`. Also "Ω_even → 2c_lat\|k\|, ω² → m²+4c²k²" (code: c_lat\|k\|). |
| 05c-gauge | CLAUDE.md / weak_wmu | CLAUDE.md "Physics decisions in code" table | Names `casim.engine.gauge.wmu._f26_rotation_step`; no `wmu.py` exists — the function is `casim.engine.gauge.weak_wmu._f26_rotation_step` (weak_wmu.py:L657). |
| 05c-gauge | weak_z | weak_z.py:L98–101 (docstring Z10) vs L203–221 z_couplings() | Docstring: g_V=T₃−2Qs², g_A=T₃ "for all 7 species"; code sets g_L=0 for R species, giving e_R (g_V,g_A)=(1/4,−1/4) at s²=1/4 (spot-check), not (1/2,0). |
| 05c-gauge | weak_z (vs CLAUDE.md decision 5 / F91) | weak_z.py:L391, L408–416 | Decision 5: "Z even for its vector part with a mass-suppressed axial split". Code: one even rotation for the entire (scalar-per-site) Z field; no vector/axial split in the propagator anywhere. |
| 05c-gauge | weak_wmu (vs CLAUDE.md decision 5 / F91) | weak_wmu.py:L926, L1296–1306 | Decision 5: "W± chiral (forced; left-projector coupling, right-branch weight ≡ 0)". Code: massless W propagator is the chiral F^±↔Ω^± law on all 3 isospin components; left coupling is structural (χ stepped with identity links); no explicit projector / right-branch-weight parameter; massive W uses the even law. |
| 05c-gauge | strong | strong.py:L994–1001 vs L1036–1052 step_strong_2d_complex_mass() | Docstring describes a parallel_transport Strang split; code uses Cayley kinetic half-steps. |
| 05c-gauge | lpt_d1_action_consistent | lpt_d1_action_consistent.py:L45–59 | Docstring says the refold "survives in lpt_selfenergy._pi_bgfield"; lpt_selfenergy now defaults refold=False (F308 repair). Stale present tense. |
| 05c-gauge | lpt_wilson / lpt_wilson_selfenergy | lpt_wilson.py:L14; lpt_wilson_selfenergy.py:L47 | "Z0 validated to machine precision" — midpoint quadrature of an integrable 1/K̂ singularity; quantitative, not machine. |
| 05c-gauge | su3_ladder | su3_ladder.py:L145–150 singlet_in_product() | Docstring says it verifies via torus orthogonality; code returns δ_{B,Ā} by fiat (verification is the separate singlet_multiplicity_torus). |
| 05c-gauge | photon | photon.py:L39–42 vs L53, L88–107 | Docstring: the photon step "IS ca_wmu._f26_rotation_step"; the import is unused and the formula is re-implemented (numerically identical, 8.9e-16). |
| 06a-particles | particles.baryon_dynamics | baryon_dynamics.py:L41-42 vs L195,L211-212 | Module docstring gives per-pair V_p=(σ/2)r−(α_s/3)/r; build_HS defaults compute σr−(2α_s/3)/r (½-rule only via non-default args). |
| 06a-particles | particles.derive_generator_norm | derive_generator_norm.py:L51,L150,L161 vs constants/lepton.py:L128-132 | Registry Site note says lam6_F234 is COMPUTED, never imported ("importing the answer would make it circular"); code imports registry lambda_6=0.243 and uses it as an input (backs out e, runs route-I minimiser). |
| 06a-particles | particles.derive_lambda6_sextic | derive_lambda6_sextic.py:L63,L132-133 vs constants/lepton.py:L116-123 | Registry lambda_6 derivation cites e≈0.733 (e_saturation); \|B\|/(2e^6 cos 2/3) at e=0.733 is 0.2334, not 0.243 (4%, outside tol 5e-3). Code uses e=√3·ȳ_PDG=0.7279 → 0.2433. |
| 06a-particles | particles.derive_lambda6_sextic | derive_lambda6_sextic.py:L121,L171 vs L49 | Text calls 3δ=Q a "1.7e-5 near-coincidence"; code's \|3δ−Q\|=2.84e-5 (1.76e-5 is the cos residual). |
| 06a-particles | particles.derive_t2g_pmns | derive_t2g_pmns.py:L35-36,L236 vs L188-193,L207 | Docstring: full fit has "exactly 3 inputs for 3 angles"; fit_full fits 4 parameters (δ_ν, t_xy, t_yz, t_zx). Docstring also names file derive_t2g_pmns_selector.py. |
| 06a-particles | particles.derive_quark_shape_probe | derive_quark_shape_probe.py:L18-20 vs L121,L140,L408-409 | Docstring ansatz 1+2√η² cos with η²=1/2; code fits 1+η cos and checks η²=2. |
| 06a-particles | particles.derive_quark_mixed_koide_probe | derive_quark_mixed_koide_probe.py:L9 vs L104 | Docstring cites "F92's eta^2=1/2"; code target η²=2 (different parametrisation). |
| 06a-particles | particles.derive_composite_scalar_fermion_coupling | derive_composite_scalar_fermion_coupling.py:L20-27,L201 vs L136,L250 | Docstring: g_sigma_qq(M,G,Lam) (function takes M,Lam); ratio varies ">6x"/">5x" vs check spread>0.5. |
| 06b-particles | particles/dirac.py | dirac.py:L1001–1018 su2_casimir_left() | Docstring says it returns the Casimir T(T+1)=3/4 for a pure doublet state. The code returns T3²+\|T+\|², which is 1/4 for pure ν_L (a Bloch-vector length, not the Casimir). |
| 06b-particles | particles/eg_sextic.py | eg_sextic.py:L20–24 vs L208 induced_lambda6() | Docstring: λ6=(2/9)(g²/2)J_sat/M_g². Code: λ6=(2/9)·c_quartic with c=1.10 (an F118 fit); J moments are "not used". |
| 06b-particles | particles/element.py | element.py:L41–46, L50–53, L173, L287 vs L200–203, L300–303 | Docstring says A≥3 nuclei and Z≥2 electrons raise NotImplementedError. The code runs manybody.nuclear_binding_Abody / electron_cloud_hartree. |
| 06b-particles | particles/element.py | element.py:L20 vs L140–141, L186–188 | "Zero new parameters", but the code hard-codes ω g²/4π=5.39 (nuclear.py default 11.0), b=0.55 fm, m_q=0.785, α_s=0.50, σ=1.0. |
| 06b-particles | particles/higgs.py | higgs.py:L19–24 vs L192–199 kg_step_strang() | Docstring: Strang split (FFT-exact linear m0²=2μ² + nonlinear kick). Code: plain velocity-Verlet with the full spectral force; kg_nonlinear_kick is unused. |
| 06b-particles | particles/hyperfine.py | hyperfine.py:L74–77 a_e_schwinger() | Docstring says a_e is "pulled from the model's own vertex loop if available"; the code always returns α/2π. |
| 06b-particles | particles/positronium.py | positronium.py:L267–279 para_2gamma_rate(); L329–337 | The rate is said to be "built from the model's annihilation cross section", but (σv)=πα² is hard-coded. The F260 comparison is a separate function, and the ortho factor is a literal (the quadrature is a side check only). |
| 06b-particles | particles/positronium.py | positronium.py:L296–306 ore_powell_factor() | Docstring states F=2(π²−9)/9 and then gives the rate factor 2(π²−9)/(9π). |
| 06b-particles | particles/majorana.py | majorana.py:L16 vs L73–74 eg_diagonal_matrix() | Docstring: √M_a = M_R0[1+√2cos(·)]. Code: M_a = M_R0·s_a², i.e. √M_a = √M_R0·s_a. |
| 06b-particles | particles/nuclear.py | nuclear.py:L117 vs L125 | Comment says g_σNN²/4π=8.09; the code value is 9(311.2/92.07)²/4π = 8.182. |
| 07a-cosmology | cosmology_bbn | cosmology_bbn.py:L307-L316 hubble_rate() | docstring: Planck mass from model's structural G "by default"; signature default is `G=G_CODATA`. Structural G only supplied by np_freezeout (L443-L444) |
| 07a-cosmology | cosmology_geon_domain_wall_reopening | cosmology_geon_domain_wall_reopening.py:L140, L171 | docstring says V reused verbatim from `eg_clock_coefficient`; V is re-typed locally, only amplitude A read back for display |
| 07a-cosmology | cosmology_horizon_thermodynamics | cosmology_horizon_thermodynamics.py:L66-L73 | docstring: Unruh T from model light cone (c_lat, F26/F180) and model's induced G (F79); code imports neither (c=1, G free symbol) |
| 07a-cosmology | cosmology_lambda_sequestering_consistency | cosmology_lambda_sequestering_consistency.py:L192-L201 flat_open_matter_only_v4_diverges() | name/docstring claim flat and open matter-only checked; only flat $a\propto t^{2/3}$ computed |
| 07a-cosmology | darkmatter | darkmatter.py:L59-L60 v_mond() | comment: simple μ(x)=x/(1+x); code uses $g=\sqrt{g_Na_0+g_N^2}$ (simple μ gives $g_N/2+\sqrt{g_N^2/4+g_Na_0}$) |
| 07a-cosmology | cosmology_blockspin_fluctuation | cosmology_blockspin_fluctuation.py:L46-L55 vs L270-L308 | docstring calls C2 "exact power counting"; C2 check is a 2 % small-λ numerical comparison; only term_eigenvalue (L175) is exact |
| 07b-gravity | gravity_emergent.py | gravity_emergent.py:L28 vs L192 | Docstring: phantom density $+\tfrac1{4\pi G}\nabla\cdot[(\nu-1)g_N]$; code computes total $-\tfrac1{4\pi G}\nabla\cdot(\nu g_N)$ (opposite sign, total not phantom; code form is the correct one for $g=-\nabla\Phi$). |
| 07b-gravity | gravity_emqg.py | gravity_emqg.py:L8 vs L133 | Module docstring $c=c_0/(1+\phi/c_0^2)$; code $c=c_0/(1-2\phi/c_0^2)$. |
| 07b-gravity | gravity_backreaction.py | gravity_backreaction.py:L61 vs L85–108 | Docstring says 3D "BCC box"; all stencils are simple-cubic/square. |
| 07b-gravity | gravity.py | gravity.py:L140–142 vs L161–170 | `T00_dirac_kinetic` claims "the same centred difference the lattice Laplacian uses"; `lap_nd` is a nearest-neighbour second difference, not the square of the centred gradient (minor). |
| 07b-gravity | gravity_band_cutoff.py | gravity_band_cutoff.py:L56, L332 vs L243 | Docstring/title quote $E_\text{max}/E_P=0.82479$ / 0.8248; the computed closed form $\sqrt{\pi\sqrt3/8}=0.824727$ (L302 has the correct 0.82473). |
| 07b-gravity | gravity_field_equation_uniqueness.py | gravity_field_equation_uniqueness.py:L353 vs L379, L385 | `leg_L2b` docstring $\nabla^\mu T_{\mu\nu}=-(\Box\phi)\partial_\nu\phi$; code and claim string test $+(\Box\phi)\partial_\nu\phi$ (code correct). |
| 07b-gravity | inspiral.py | inspiral.py:L15 vs L74 | Docstring strain $h\sim(4/D)(\pi f)^{2/3}\mathcal M_c^{5/3}$; code omits $4/D$ (and $c$), so `h` is an un-normalised shape in seconds. |
| 07b-gravity | interior_metric.py | interior_metric.py:L32 vs L161–162 | Docstring $AB=(1-u^2/4)^2(1+u/2)^2$; the code's legs give $AB=(1-u^2/4)^2$ (conclusion $AB\neq1$ unaffected). |
| 07b-gravity | derive_curl_subleading.py | derive_curl_subleading.py:L185–191 vs L209 | Leg A2 docstring says it compares the *measured* on-axis value to $-1/96$; code compares the closed form `alpha_2d(pi/2)` — tautological except under the override control. Also L236–242: F245 reports B1 worst 9e-15, code measures 4.0e-12. |
| 07b-gravity | derive_f26_dispersion.py | derive_f26_dispersion.py:L143–149 vs L197 | Leg C3 docstring says it replaces "the measured C3 body-diagonal value"; code compares the closed form `c3_closed((1,1,1))` with $-\sqrt3/486$ (arithmetic identity). |
| 07b-gravity | derive_velocity_addition.py | derive_velocity_addition.py:L26–30 vs L592–605 | Docstring derives the deformed addition law from "SR boost acts on (ω,k) exactly"; the module's own gate `offshell_boost_coefficient` shows the linear boost is off-shell at leading order ($\Delta/vk\to1/\rho-1$). `numerical_scan` compares the formula with itself (L373). |
| 07b-gravity | derive_gap5_adjudication.py | derive_gap5_adjudication.py:L162–163 vs L275–297 | Docstring says the module "fixes" the `_seconds` volatile-regex hole; code only tests `casim.baselines._VOLATILE_RE`. |
| 07c-qed | qed_casimir | qed_casimir.py:L306–324 weight_beable()/weight_sep_buoyancy() | Docstring and inventory #229 say the beable and SEP weights are computed by "INDEPENDENT formulas" that coincide; the code evaluates the same expression g·E_C(η)/c² twice, so the zero residual (L341–342) holds by construction. Same for dce_* (L371–388) and homogeneous_offset_differential (L354: x−x). |
| 07c-qed | qed_electron_self_energy | qed_electron_self_energy.py:L247 z2_coefficient_symbolic() | "Z1 = Z2 between the two computed loop objects" (docstring S3, inventory #280): the Z1 log coefficient −1/4π is a hard-coded literal, not computed from a vertex loop. |
| 07c-qed | qed_euler_heisenberg | qed_euler_heisenberg.py:L57–58, L307, L338–339 birefringence_ratio_symbolic() | Returned strings give n∥−1=(7/2)(2α²/45)B²/m⁴ via "n−1=ΔL/2e²". From the Lagrangian the code uses, δε∥=14κB² so n∥−1=7κB²=(14α²/45)B²/m⁴ (textbook HL, =7α/90π·(B/B_c)²); strings are a factor 2 low. Only the 7:4 ratio is computed. |
| 07c-qed | qed_euler_heisenberg | qed_euler_heisenberg.py:L156–159 | Statement "7 = 2/45 + 5/45 over the 2/45" evaluates to 7/2; the code's decomposition is (4/45+10/45)/(2/45)=7. |
| 07c-qed | qed_ir_bremsstrahlung | qed_ir_bremsstrahlung.py:L68–72 vs L340–349, L383 | Module docstring Q2: σ/σ0 = 1−(α/2π) f_IR ln(−q²/ΔE²) and double log with α/2π; the code uses α/π throughout. |
| 07c-qed | qed_scattering | qed_scattering.py:L35 vs L293–323 compton_ward_symbolic() | Header says the Ward identities are "sympy-exact (literal 0)"; the Compton and annihilation Ward checks are numeric (tol 1e-12). |
| 07c-qed | qed_twoloop_ae | qed_twoloop_ae.py:L15–29 vs L117–126, L148–154 | Docstring: VP group (I) "computed HERE FROM THE MODEL'S OWN Pi" (F251). The spectral function is the textbook continuum (α/3π)(1+2m²/s)√(1−4m²/s) typed in (and inlined in A2_vp_dispersive); qed_vacuum_polarization never computes Im Π. |
| 07c-qed | qed_twoloop_vacuum_polarization_nonlog | qed_twoloop_vacuum_polarization_nonlog.py:L29, L44–49 | Header calls the leading-log result "genuinely NEW model-internal content ... independent confirmation"; the in-docstring review note (2026-08-30) says it is "largely RG-forced". Code: (1/3)·(3/4)=1/4 with R^(1)=3/4 cited. |
| 07c-qed | qed_vacuum_polarization | qed_vacuum_polarization.py:L21–26, L251–253 ward_identity_symbolic() | Π1 claims q_μΠ^{μν}=0 "over the whole BZ". Code contracts q with the assumed transverse tensor (a tautology); the real transversality check (L165) is on the continuum UV-log piece, not on the lattice Π. |
| 07c-qed | qed_vacuum_polarization | qed_vacuum_polarization.py:L331–332 _dalpha_lepton() docstring | "d(1/α)/dln s = −1/3π = −(b0/4)(α/π)": the second equality is off by a factor α. |
| 07c-qed | qed_vertex_loop | qed_vertex_loop.py:L17–24, L115–118 wt_identity_symbolic() | Inventory #276 says "one-loop QED vertex Λ^μ. Ward–Takahashi ... EXACT (fixes Z1=Z2)"; code verifies only the tree identity q̸ = S⁻¹(p')−S⁻¹(p) (Λ=γ). |
| 07c-qed | qed_vertex_loop | qed_vertex_loop.py:L178 uehling_coefficient_symbolic() | Uehling S-state coefficient −4/15 is described as "DERIVED" (docstring, inventory #276) but is a typed Rational(-4,15); only the 1/30 moment is computed. The docstring's low-q line flips sign relative to its own first line (textbook Π₂→−(α/15π)q²/m²). |
| 07d-qi | qi_bell_tsirelson | qi_bell_tsirelson.py:L131-L134 chsh_singlet_of_phi() | Docstring says $S(\varphi)=3\cos\varphi-\cos3\varphi$, max $2\sqrt2$. The code returns the negative ($S(\pi/4)=-2\sqrt2$, singlet sign). Magnitude and curvature are unaffected. |
| 07d-qi | qi_belt_trick | qi_belt_trick.py:L218-L219 triplet_scalar_deviation() | Docstring says the deviation at $\theta=\pi$ is "$2/\sqrt3$ × scale". The code's Frobenius norm is $2\sqrt6/3=1.633$. |
| 07d-qi | qi_cluster | qi_cluster.py:L39-L41 vs L352-L364 | The header says $\xi\Delta\sim v$, "not fitted, it is the gap". The code fits a log–log exponent (−0.93) and reports the $\xi\Delta/v$ drift as ~30%. |
| 07d-qi | qi_cluster | qi_cluster.py:L430-L431 check_cluster() | The `cone_slack=-1` docstring says it "pins the cone radius to 2t". `cone_radius()` is $r\le t$ per layer (L180). |
| 07d-qi | qi_cluster_interacting_3d | qi_cluster_interacting_3d.py:L86-L90 vs L472-L475 | The C3 control is said to show "the correlator does NOT decay exponentially" below $g_c$. The code sets `ok3=False` without computing a correlator. |
| 07d-qi | qi_entanglement | qi_entanglement.py:L391-L396 native_zz_quarter() | Docstring says $e^{i\pi/4\,ZZ}$. It returns $-e^{i\pi/4\,ZZ}$ (global phase, spot-checked), later removed by phase alignment in `native_cz`. |
| 07d-qi | qi_gleason_regularity | qi_gleason_regularity.py:L60-L61 vs L183 | Docstring lists dimensions "4, 8, 9, 16, 64, 96". `MODEL_DIMENSIONS=(3,4,6,64,96)`. |
| 07d-qi | qi_gleason_regularity | qi_gleason_regularity.py:L269-L276 vs L300-L302 | `p3_harmonic` says the $P_3$ mode "is annihilated by the frame condition" at $d\ge3$. `frame_condition_across_bases` says it "is NOT annihilated". The code breaks the frame sum. |
| 07d-qi | qi_measurement | qi_measurement.py:L725-L744 finegrain_state() | Docstring says the fine-graining is done by native controlled-copy/CNOT. The code writes $1/\sqrt M$ directly on the diagonal, so M2f/M2g ($p_k=\mu_k/M$) are true by construction. |
| 07d-qi | qi_measurement | qi_measurement.py:L848-L852 cone_capacity() | Says "a BCC ball of radius R holds $2R^3$ cells". $2R^3$ is a cube of edge R. |
| 07d-qi | qi_so3_kinematic_gap | qi_so3_kinematic_gap.py:L78-L84 vs L232-L270 | Module docstring says K2 sweeps "a family of generic axes and angles". The code uses one fixed axis/angle. |
| 07d-qi | qi_born_nonabelian | qi_born_nonabelian.py:L364-L369 schur_reduction() | Docstring calls $C_2\propto\mathbb 1$ "the whole general theorem" (frame-function factorisation). Only the Casimir scalar is computed; the factorisation is not. |
| 07e-running-thermo-astro | superconductivity.py | superconductivity.py:L633–637, L723 | Docstring derives $(2k_F/k_{TF})^2=\pi(9\pi/4)^{1/3}/r_s=6.02921/r_s$, but the code hard-codes 6.0299 (relative error $1.1\times10^{-4}$), also in `mu_coulomb_real_dos` |
| 07e-running-thermo-astro | thermodynamics_interacting.py | thermodynamics_interacting.py:L124, L350 | Entry point is named `check_f375()`, but the registry finding and artifact are F376 (F375 is the Nb real-DOS finding) |
| 07e-running-thermo-astro | slowlight.py | slowlight.py:L206–217 | Docstring and code take the lattice term as $(ak)^2$ with $C=O(1)$, but the derived BCC coefficient is $\langle A\rangle=1/315$ (F300), so the bound overstates the term by ~300× |
| 07e-running-thermo-astro | running_scale_ratio.py | running_scale_ratio.py:L22–23, L80–94 | Chiral factor $\Lambda/f_\pi=7.04$ is called "EXACT" but is a numerical NJL solve on fitted inputs ($G\Lambda^2$, $\Lambda$, $m_0$) |
| 07e-running-thermo-astro | running_alpha_s.py | running_alpha_s.py:L35–40 | STEP-4 docstring formula for $d_1$ is garbled; the code computes only the implied shift $\Delta(1/\alpha)$ (L252) |
| 07e-running-thermo-astro | tolman.py | tolman.py:L25–27 | Module docstring still says "the model uses rho only, GR uses rho + 3p" as the model's law; per F178 the energy-only law is a weak-field reduction |
| 07e-running-thermo-astro | thermodynamics_interacting.py | thermodynamics_interacting.py:L25–28 | Docstring calls the toy t–V chain "the model's own … the L^3 BCC walk collapsed", but it is a generic 1-D OBC chain with undetermined couplings |
| 08a-forks | forks/gravity/dirac_gravity_fork.py | dirac_gravity_fork.py:L212 gravity_dirac_step(); docstrings L29, L446–448, L657 | Stepper rotates the rest leg by √A·m per tick (massless kinetic + mix angle √A·m·dt); docs/tests predict 2·arcsin(√A·m) / √A·arcsin(m). Spot-check A=0.81,m=0.5: 0.4500 vs 0.4668/0.4712. Tests pass only on the near/far ratio (~1 % effect). |
| 08a-forks | forks/gravity/gr_fork_F46_dirac.py | gr_fork_F46_dirac.py:L166 rest_leg() vs L303 gravity_dirac_step_2d() | Analytic rest leg √A·arcsin(m) vs stepper angle √A·m (block comment L247 says θ=√A·m·dt); docstring L34 has m c0² in the Hamiltonian, code is c0-free. |
| 08a-forks | forks/gravity/gr3_fork_baseline.py | gr3_fork_baseline.py:L44 vs L52–54 metric() | Docstring gives the baseline metric A=B=(1−2φ/c²)⁻²; metric() returns isotropic-Schwarzschild (1+2φ/c², 1−2φ/c²). |
| 08a-forks | forks/gravity/gr3_fork_harness.py | gr3_fork_harness.py:L173–175, L204 | Comment says 3π normaliser "same as the standard 6π formula"; true GR per-orbit advance is 6π GM/(a(1−e²)c²) — normaliser wrong by 2 (S16). |
| 08a-forks | forks/gravity/gr_fork_F55_spatial_metric_backreaction.py | gr_fork_F55_spatial_metric_backreaction.py:L117 | Docstring of metric_trace_reversed contains an unfinished "A = 1 + h₀₀ ... wait:" line; code consistent. |
| 08a-forks | forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py | gr_fork_F58_clockrate_coupling_derivation.py:L165–167, L182–183 vs L190–192 | Docs: c_lat ∝ J, stiffness ∝ J²; code symbol linear in J ⇒ stiffness ∝ J, c_lat=√stiffness ∝ √J. |
| 08a-forks | forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py | gr_fork_F58_clockrate_coupling_derivation.py:L74 restleg_rate() | Docstring A = 1 − 2Φ/c²; chain and L93 comment use A = 1 + 2Φ/c². |
| 08a-forks | forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py | gr_fork_F58_clockrate_coupling_derivation.py:L39–40, L241 | "1/G ∝ c_lat² ∝ √d": with c_lat = 1/√d, c_lat² = 1/d (F60 L3 has it right). |
| 08a-forks | forks/gravity/gr_fork_F63_spin_torsion_estimate.py | gr_fork_F63_spin_torsion_estimate.py:L73 cell_size_over_ellP(g_star=16) | Uses a ≈ 3.81 ℓP (g*=16, F61 one generation), not the adopted canonical a = √(8π)·3^(1/4) ℓP (g*=48, F79/F107; S5). |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | gr_fork_F64_em_connection.py:L57–61 vs L119–124 _maps() | Docstring says clock_only/refractive_only break impedance; code assigns ε=μ for both ⇒ impedance_constant True for all three (spot-checked). D-EM1 impedance leg discriminates nothing; D-EM5 FDTD (L1208–1210) uses a different (ε,μ) assignment for the same names. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L541–545, L638, L769–771, L946, L987–988, L1048, L1223, L1453, L1466 | Docstrings/comments describe K=(1−u)⁻² (A=(1−u)²) where code uses canonical K=e^{2u}. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L115 _maps(), L192 deflection_coeff_numeric(), L1131–1132 dem5, L1432 test_dem7 | D-EM1, D-EM5(D) and D-EM7's PASS gate still run on K=(1−u)⁻² (PPN β=½), the form D-EM9 excludes. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L793, L1026, L1695 (D-EM-D2b, D-EM4, D-EM11) | Predictions 2·arcsin(√A·m) vs stepper rest rate √A·m (inherited from dirac_gravity_fork). |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L1729, L1779, L1813 test_dem10 | Pins a at g*=16 ⇒ 3.81 ℓP; canonical ruler is g*=48 ⇒ 6.598 ℓP (F79/F107, S5). |
| 08b-forks | gr_fork_F180_gw_speed | gr_fork_F180_gw_speed.py:L197 vs L211/L222 | Check-D comment says residual "~1e-40"; code bound (f/f_Pl)^2 ≈ 2.9e-83 (note at L222 agrees with code) |
| 08b-forks | gr_fork_F197_first_excitation_dark | gr_fork_F197_first_excitation_dark.py:L211 vs L218 | Comment: σ/m ~ λ6²/m³; code: λ6²·1e-2 with no mass dependence |
| 08b-forks | gr_fork_F200_sterile_neutrino_dm | gr_fork_F200_sterile_neutrino_dm.py:L63 vs L59/L65 | Docstring Γγ/Γ3ν ≈ 1/128; coded coefficients give 27α/(4π) ≈ 1/64 (factor 2) |
| 08b-forks | gr_fork_F200_sterile_neutrino_dm | gr_fork_F200_sterile_neutrino_dm.py:L166 vs L70 | Verdict "tau ~ 1e25-26 s, ~8 orders"; code gives 1.26e27 s (~9.5 orders) at 7.1 keV, sin²2θ=5e-12 |
| 08b-forks | gr_fork_F223_spin2_binding_relic | gr_fork_F223_spin2_binding_relic.py:L79 vs L104–L130 | Comment says np.linalg.eigh; code uses hand-rolled shifted inverse iteration |
| 08b-forks | gr_fork_F228_geon_production_stability | gr_fork_F228_geon_production_stability.py:L51, L387 vs L201 | Docstring/summary say β~1e-4..1e-2; code gives β=6.6e-15, 6.6e-12, 6.6e-9 (header L30 and inventory row 257 agree with code) |
| 08b-forks | gr_fork_F238_geon_relic_abundance | gr_fork_F238_geon_relic_abundance.py:L23 vs L168/L175 | Header β=erfc(δc/√2σ); code uses ½·erfc |
| 08b-forks | gr_fork_F248_tt_graviton_bcc | gr_fork_F248_tt_graviton_bcc.py:L26, L43 vs L130 | Module docstring states even law Ω=2ω+(k/2); code (and its own L128 docstring) uses ω+(k/2)+ω−(k/2) |
| 08b-forks | gr_fork_F248_tt_graviton_bcc | gr_fork_F248_tt_graviton_bcc.py:L50 vs L394 | Docstring: h(k,t)=h(k,0)cos(Ωt); code evolves a one-way e^{-iΩt} packet |
| 08b-forks | complex_mass_fork | complex_mass_fork.py:L529 vs L539–L548 | su2_casimir_left docstring says 3/4 for a pure doublet; code returns ⟨T3⟩²+\|⟨T+⟩\|² ≤ 1/4 (not the Casimir ⟨T²⟩) |
| 08b-forks | complex_mass_fork | complex_mass_fork.py:L241 vs L262 | 'plane' mode docstring b=sin(π/4)e^{ikx}; code uniform b=sin(π/4) |
| 08b-forks | hypercharge_fork | hypercharge_fork.py:L6, L16, L22 | Majorana branch labelled "F43"; F43 is now dynamical gluons, content is F47 (registry findings empty) |
| 09-shims | lattice/chiral_core.py | docs/status/exactness-inventory.md row #76 vs chiral_core.py:L24-35 | Inventory says hand-rolled core matches kernels "bit-for-bit"; code/docstring say a few ULP (1.4e-15 / 1.8e-15 at L=32); measured 1.3e-15 / 8.9e-16 at L=8 |
| 09-shims | particles/spec.py | spec.py:L149 anomaly_traces() | Docstring says "All six vanish"; code returns five traces |
| 09-shims | particles/channel.py | channel.py:L1952 vs L1819-1833 | Comment says NN OBE applied as "unitary momentum kick"; _apply_nn_binding applies a scalar-mass η↔χ rotation from V (not force); _nn_Vprime (L1800) unused |
| 09-shims | particles/channel.py | channel.py:L4-5 | Docstring: "wiring, not physics"; module computes confining potentials, source kicks, bag map, Hartree, Gram–Schmidt, fitted NN potential |

## SUPERSEDED (52)

| Section | Module | Where | Detail |
|---|---|---|---|
| 01-constants / 02-numerics | constants/gravity.py | gravity.py:L48 (F106_COEFF_LATTICE) | The law ∇²lnK = -T⁰⁰ is RECLASSIFIED by F178 (supersessions.yaml L440-446) as the static weak-field reduction of G_μν = 8πG T_μν. The coefficient value is live; the law is no longer fundamental. |
| 03-lattice | lattice.curved | curved.py:L179–186, L211–218 | `ordering='asymmetric'` and `order=1` are the pre-F276 scheme (SUPERSEDED by F276), kept only as negative controls. |
| 03-lattice | lattice.dimensionality | dimensionality.py:L528–529 | `time_dim=1` as "structural, not proved". It is superseded in substance by F313/F326 (time_signature, time_single_generator). |
| 04-core | core.channels (gravity_dielectric) | channels.py:L283-296, L364-376 | Implements ∇²lnK=−(8πG/c⁴)T⁰⁰ (F106), which S4-F178-full-stress-energy RECLASSIFIES as the static weak-field reduction of G_μν=8πG T_μν; the exponential K is PPN-order only. |
| 04-core | core.channels (photon_pair) | channels.py:L93-100 | The eikonal ω₀ mix was SUPERSEDED by F271 (S10-F271-eikonal-dielectric-photon); the code now uses `photon_step_dielectric` (current). Mapped for the record. |
| 04-core | core.tier3 (gauge_mc) | tier3.py:L30-83 | Runs F94's simple-hypercubic Wilson ensemble; SUPERSEDED by F323/F265 (S21-F94-hypercubic-action-not-the-model-lattice). |
| 05a-gauge | gauge.bilinear | bilinear.py:L5-22, L1907-1985 rotation_step_em_spectral(), L487-593 | σ-bilinear composite photon SUPERSEDED as the photon by F67/F68/F69 (paired-spinor photon, even law). The curl-residual coefficient c_lat/√2 was WITHDRAWN by F306 (inventory #7, #49). Audit: no live photon channel imports bilinear.py; its engine consumers are derive_bilinear_so3.py, forks/lattice/smearing_fork_harness.py and forks/gauge/curl_fork_harness.py. |
| 05a-gauge | gauge.bilinear_2d | bilinear_2d.py:L127-161 maxwell_curl_residual_2d() | The curl-residual constant this module was built to discriminate (1/√6 vs 1/2, F7) was WITHDRAWN by F306. Only rotation_omega_2d is live, used by gluon.py and colour_dielectric.py as a 2-D gluon rate (not a photon). |
| 05a-gauge | gauge.colour_dielectric | colour_dielectric.py:L10-33 (framing) | Built as the colour analogue of the "F64 gravitational dielectric"; F64's dielectric was reclassified by F178 (CLAUDE.md decision 4) to the vacuum/weak-field representation. The code does not depend on F64, so only the framing is affected. |
| 05b-gauge | derive_coupling_normalisation | derive_coupling_normalisation.py (whole; Casimir-branch framing) | Partially superseded by F325 (supersessions S22: F298/F299/F303). The arithmetic stands; branch A is closed. |
| 05b-gauge | derive_ncolour_bracket | derive_ncolour_bracket.py:L409–413, L509–519 | The C7 upper leg (support {2,3}) is withdrawn by F325/S22. The code and summary() still return N_c = {3}; the current bracket is odd N_c ≥ 3. |
| 05b-gauge | derive_ncolour | derive_ncolour.py:L568–575 | The H2/H3 Casimir translation hypotheses are moot after F325 (the Casimir reading is a mixed-matching artefact). |
| 05b-gauge | derive_su3_structure | derive_su3_structure.py:L78, L961–965 | Docstring/summary cite "F298's structural N_c ≤ 3" as agreeing; withdrawn by F325 (CN19 falls). |
| 05b-gauge | gluon | gluon.py:L215–244 gluon_rotation_step_spectral_bcc_chiral | Retired chiral BCC gluon step, superseded by F91 (S2-F91-gluon-chiral-to-even). Retained for comparison only; the canonical even step is verified. |
| 05b-gauge | gluon | gluon.py:L564–600 _plaquette_field_strength_su3_composite_sc | Composite simple-cubic plaquette deprecated by F265; the live path delegates to bcc_action. |
| 05c-gauge | weak_wmu | weak_wmu.py:L1039–1137 _plaquette_field_strength_composite_sc() | SUPERSEDED by F265 (composite-SC plaquette blind to 1/3 of curvature); retained for the no-go. |
| 05c-gauge | lpt_vertex | lpt_vertex.py:L10–16 | Premise "rule and Wilson share the plaquette vertex" invalidated by F265; rule vertices now from lpt_bcc_vertex (F305). |
| 05c-gauge | strong | strong.py:L309–342 parallel_transport() | Deprecated (gauge-variant), retained as a warning alias. |
| 05c-gauge | lpt_selfenergy | lpt_selfenergy.py:L137–204 | `_pi_gluon_loop` / `_pi_ghost_loop` (no gauge-fixing vertex) superseded in use by `_pi_bgfield` (Abbott lattice vertex). |
| 06a-particles | particles.derive_generator_norm | derive_generator_norm.py:L194-208 | VERDICT framing ("E1 does not close", derive λ₆ independently) superseded by decision 7 / F256 (own banner L2-25); PART (a) Schur R=1 remains live. |
| 06b-particles | particles/dirac.py | dirac.py:L389–414, L1021–1034 | Stale comments justify removing U(1) minimal coupling by the σ-bilinear composite photon of ca_maxwell.py. That photon is SUPERSEDED by F69 (S1); the photon is the paired-spinor gauge/photon.py. |
| 06b-particles | particles/eg_sextic.py | eg_sextic.py:L183–211, L228–284 | De facto SUPERSEDED by F253/F255/F256 (S6, Core decision 7). λ6 is an output of δ*=2/9 via F234, and F256 proves the dynamical route cannot lock 3δ*=Q; c_fierz_colour provenance names 2/9 as a value λ6 is proved not to take. The module is not listed in supersessions.yaml. |
| 07a-cosmology | blackhole | blackhole.py:L262-L276 f114_dielectric_contrast() | F114 horizon-free dielectric BH (photon sphere $2\sqrt e M$, shadow $2eM$, +4.63 %) SUPERSEDED by F178/F183 (supersessions S4-F178-full-stress-energy); kept as exclusion record |
| 07a-cosmology | cosmology_primordial | cosmology_primordial.py:L211-L231 eg_radial_coefficient() | $V_0=-\hat V(e_\min)$ "forced by F193" = F193 Part A (ontic vacuum gravitates as zero), EXCLUDED per supersessions S25 (F319 U8 / CL275); radial-direction K rests on it |
| 07a-cosmology | cosmology_initial_conditions | cosmology_initial_conditions.py:L116-L120 MEASURE_SLOPES / docstring D1 | "critical Gaussian field squared gives $n_s=0$" corrected by F310 C2 ($n_s=-1$); prose correction, not a ledger entry |
| 07b-gravity | gravity.py | gravity.py:L207–270 dielectric_mix_half() | Eikonal $(E,B)$ dielectric mix SUPERSEDED by F271 (`gauge.photon.photon_step_dielectric`); retained as control. |
| 07b-gravity | derive_curl_subleading.py | derive_curl_subleading.py:L1–39, L66–98 | Closes subleading terms of the σ-bilinear composite-photon curl residual that S18/F306 declares a representation artifact (F21/F23/F25 superseded; inventory #49 withdrawn); docstring still presents $c_\text{lat}/\sqrt2$ as Tier-1. σ-bilinear applied to the photon (F65–F69 hazard) — legitimate only as a record of the superseded construction. |
| 07b-gravity | horizon_entropy.py | horizon_entropy.py:L57–59 | Posits $s_\text{cell}=2\pi\sqrt3$; the computing route is F300/F355 (`horizon_entanglement.py`). Not a ledger supersession — informational. |
| 07c-qed | qed_vacuum_polarization | qed_vacuum_polarization.py:L275–300 _fermion_B() | S12 (by F277, 2026-08-02): refold removed; F251 partially superseded (numbers only; Δ changed sign). Code mapped is post-fix. |
| 07c-qed | qed_electron_self_energy | qed_electron_self_energy.py:L414–439 _selfenergy_AB() | S12 (by F277): refold removed; F258 partially superseded (numbers only). Code mapped is post-fix. |
| 07e-running-thermo-astro | raytrace.py | raytrace.py:L116–118 | `*_F114` shadow fields (b_c = 2eM, +4.63%): SUPERSEDED by F178. Kept as a live exclusion gate (test_F186 T2) |
| 07e-running-thermo-astro | stellar.py | stellar.py:L66–70, L140–195 | Energy-only `_model_rhs` and the covariant dielectric variant: SUPERSEDED by F178 (F106 reclassified; F173/F174 departures are artifacts). Only theory='gr' is canonical |
| 07e-running-thermo-astro | tolman.py | tolman.py:L97–128 | Pressure-omission fraction and uniform-sphere departure read as a discriminator: SUPERSEDED by F178 (F173 P3/P4 dead). The tensor algebra L46–91 is live |
| 07e-running-thermo-astro | superconductivity.py | superconductivity.py:L426–466, L756–769 | F211 McMillan/Allen–Dynes $T_c$ fit is superseded by the F215 Eliashberg solver; the F213 fit formula by F218b (per exactness-inventory prose, not supersessions.yaml) |
| 08a-forks | forks/gravity/gr3_fork_A_phase_tick.py | whole module | S16-F16-gr3-fork-space-closed (by F64, F178); Fork A retired by gr_fork_E_tensor.py:L43–44. |
| 08a-forks | forks/gravity/gr3_fork_B_anisotropic.py | whole module | S16 (by F64, F178); content survives as the O(u) limit of canonical A=e^{-2u}, B=e^{2u}. |
| 08a-forks | forks/gravity/gr3_fork_C_restricted_c.py | whole module | S16; tau_rate (L56) and metric (L71–73) mutually inconsistent beyond O(φ). |
| 08a-forks | forks/gravity/gr3_fork_baseline.py | whole module | S16 (and S17: c=c0/(1−2φ/c0²) is the linearisation family F64/F178 exclude). |
| 08a-forks | forks/gravity/gr3_fork_harness.py | whole module | S16: retained as falsification record, not a GR-4 instrument (FC01 is); baseline gr3_fork_comparison.json stale_by_design. |
| 08a-forks | forks/gravity/gr3_forks_AB_extended.py | whole module | S16. |
| 08a-forks | forks/gravity/gr_tensor_stub.py | field sector L142–168 | S16 (GR-3 trichotomy); geodesic GR-4 integrator is plain GR and not superseded. |
| 08a-forks | forks/gravity/dirac_gravity_fork.py | D3a L587–721 | S3-F64-dielectric-gravity: rest-mass-sourced self-redshift dead; D1/D2a sign/D2b/D2c live; F62 baseline stale_by_design. |
| 08a-forks | forks/gravity/gr_fork_F46_dirac.py | whole module (F50 content) | S3 partial: which-leg-carries-redshift + rest-mass sourcing dead; G2/G3 live. |
| 08a-forks | forks/gravity/gr_fork_F52_restleg_backreaction.py | L84–124 Poisson from ρ_rest | S3 partial: H1/H1b/H2 dead; H3/H3b factor-2 discriminator live. |
| 08a-forks | forks/gravity/gr_fork_F55_spatial_metric_backreaction.py | whole module | S3 partial: trace-reversal-from-rest-mass dead; J1/J3 live; K=(1−u)⁻² kept as β=½ control. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | fundamental-law reading; D-EM3 L450–526 T^00 sourcing | S4-F178 reclassification: dielectric = vacuum/weak-field representation; energy-only sourcing = static weak-field reduction. |
| 08b-forks | gr_fork_F193_ontic_vacuum | gr_fork_F193_ontic_vacuum.py:L92–L144 (Part A), L150–L183 (Part B) | S25: Part A (bare CC=0) excluded by F319/CL275; Section B not the residual (F408); test legs A1/A2 dead |
| 08b-forks | gr_fork_F196_dilution_exponent | gr_fork_F196_dilution_exponent.py:L122–L123 | S25 sub-claim: reading p=2 as a dilution law of ρ_vac is dead; the ceiling computations are live (F408) |
| 08b-forks | lgt_fork_A_mc | lgt_fork_A_mc.py:L37–L39 | S21 (F323/F265): the simple-hypercubic Wilson ensemble is not the model's BCC lattice (F94 superseded) |
| 08b-forks | curl_fork_harness | curl_fork_harness.py:L57–L70 | Tests the σ-bilinear composite photon (EM_bilinears), excluded for the photon by F65–F69 (key decision 5) |
| 08b-forks | smearing_fork_harness | smearing_fork_harness.py:L118–L128 | Smears the σ-bilinear composite photon, excluded for the photon by F65–F69 |
| 08b-forks | derive_weight_as_phase | derive_weight_as_phase.py:L1–L17 | S15: F230 superseded by F253/F255/F256; weight-as-phase adopted as a principle (key decision 7), so this derivation attack is a fork |

## UNREGISTERED module (7)

| Section | Module | Where | Detail |
|---|---|---|---|
| 04-core | particles.channel | src/casim/particles/channel.py (2075 lines) | Registers 9 live engine channels (particle, quark_dirac, nr_electron, composite, photon_sourced, gluon_sourced, colour_bag, two_grid_atom, element_atom) but is absent from the module registry dump (it lives outside engine/), and it is not assigned to any map part. Its bus behaviour is mapped in 04-core §"Channel coupling order and data flow". |
| 08a-forks | forks/gravity/__init__.py | whole file | No row in the module registry dump (forks/__init__.py has one). |
| 09-shims | lattice/backend.py | src/casim/lattice/backend.py:L1 | No engine module-registry record (all of src/casim/{fields,gravity,lattice,particles}/ are outside registry.tsv) |
| 09-shims | lattice/chiral_core.py | src/casim/lattice/chiral_core.py:L1 | Hand-rolled chiral core, real code, no registry record |
| 09-shims | particles/spec.py | src/casim/particles/spec.py:L1 | Exact particle quantum numbers + anomaly traces, no registry record |
| 09-shims | particles/composite.py | src/casim/particles/composite.py:L1 | Composite baryons + β-decay ledger, no registry record |
| 09-shims | particles/channel.py | src/casim/particles/channel.py:L1 | ~2075-line live module (imported at engine/__init__.py:L19, 9 channel types + 4 observers), no registry record; manifest L79 says it still needs one |

## UNREGISTERED constant (D7) (15)

| Section | Module | Where | Detail |
|---|---|---|---|
| 05c-gauge | lpt_wilson, lpt_wilson_selfenergy, lpt_d1_subtracted, weak_z | lpt_wilson.py:L43–45; lpt_wilson_selfenergy.py:L78–79; lpt_d1_subtracted.py:L122–123; weak_z.py:L174 | Literal constants not in casim.constants: Z0=0.154933390231, 28.8086, C_MSbar=131/66, F163 C_lat=6.138642608418188, θ_W=π/6 (F45). |
| 07d-qi | qi_qc_si | registry (findings empty); qi_qc_si.py:L38-L43 | F224/F225 not registered. The `a_over_ellP`, `c_SI`, `ell_P_m`, `hbar_SI` imports are not recorded as constants `Site`s. |
| 07e-running-thermo-astro | superconductivity.py | superconductivity.py:L49–53, L517–518, L573, L614 | SI constants h, e, k_B, m_e, eV, amu and a_0 are module literals, not D7 registry symbols |
| 07e-running-thermo-astro | thermodynamics.py | thermodynamics.py:L94 | K_B_SI literal (declared in the docstring as a named follow-up) |
| 07e-running-thermo-astro | thermodynamics_gstar.py | thermodynamics_gstar.py:L394–402, L642 | Model m_e=0.51069, m_mu and m_tau (F121) and kelvin_per_MeV are module literals, not D7 constants |
| 07e-running-thermo-astro | running_njl.py | running_njl.py:L73–81 | G_S2_BARE=0.25, LAMBDA3_1L=0.272, GGC_F77=1.277 and GC_LAM2=π²/6 are literals |
| 07e-running-thermo-astro | running_scale_ratio.py | running_scale_ratio.py:L68–73 | V_F88=0.713, SIGMA_ROTOR=0.2015 and F_PI_PHYS=0.09207 are literals |
| 07e-running-thermo-astro | running_alpha_s.py | running_alpha_s.py:L60–70 | E_Planck, m_t, m_b, m_c, M_Z, alpha_s(M_Z) PDG, Lambda3 FLAG and N_F119 are literals (labelled as targets) |
| 07e-running-thermo-astro | running_qstar_logmoment.py / running_scheme_constant.py | running_qstar_logmoment.py:L42; running_scheme_constant.py:L78 | Geometric-mean band $3^{-1/4}$ is duplicated as an unregistered literal in two modules |
| 07e-running-thermo-astro | running_alpha_lattice_bound.py | running_alpha_lattice_bound.py:L101–104, L369–384 | PDG/EW references (127.951, 0.23122, 246.22, 91.1876, DHMZ 0.02760, Γee 7.04e-3) are bare literals, declared as external anchors |
| 07e-running-thermo-astro | run_q3_omega_degeneracy.py | run_q3_omega_degeneracy.py:L27–30 | TARGET 2.224 MeV, b=0.55 fm and R_MAX are literals |
| 07e-running-thermo-astro | raytrace.py / vacuum_energy.py / stellar.py / running_ir_coupling.py | raytrace.py:L77; vacuum_energy.py:L29; stellar.py:L38; running_ir_coupling.py:L56–59 | M_sun, Mpc, RHO_LAMBDA_OBS, MSUN_KM, M_G_ERR and the continuum frozen range 0.30/0.50 are literals |
| 08a-forks | forks/gravity/gr_fork_F79_structural_G.py | gr_fork_F79_structural_G.py:L255 | T_P = 5.391247e-44 literal; no t_P constant in the registry. |
| 08a-forks | forks/gravity/gr_fork_F61_weyl_eta_gstar.py | gr_fork_F61_weyl_eta_gstar.py:L116–118 assemble() | Recomputes a/ℓP = √(8π)·3^(1/4) (at g*=48) with no MeasuredConstant declaration (F79 has one, measured.py:L130). |
| 08a-forks | forks/gravity/dirac_gravity_fork.py | dirac_gravity_fork.py:L188 | C_LAT_SQ = 0.5 (2D exact-QCA c_lat²) literal; correct for the 2D walk but not a registered constant/MeasuredConstant. |

## REGISTRY GAP (10)

| Section | Module | Where | Detail |
|---|---|---|---|
| 05c-gauge | photon, weak_wmu, weak_z, weak, minimal_coupling, strong, link_hamiltonian, lpt_selfenergy, lpt_vertex, lpt_ward, lpt_wilson, lpt_wilson_selfenergy, photon_bound_state, propagator, rotation, su3_ladder | registry.tsv | Manifest modules with empty `findings` and exactness None; e.g. lpt_selfenergy hosts the F308 gate entry `check_refold_repaired`, link_hamiltonian backs inventory F110-C2/C7, photon backs F67–F69/F300. |
| 07a-cosmology | blackhole | registry row | module findings empty (code is F183), exactness None |
| 07a-cosmology | cosmology | registry row | module findings empty (code is F182/F188 S5), exactness None |
| 07a-cosmology | darkmatter | registry row | module findings empty (code is F191), exactness None |
| 07a-cosmology | cosmology_bbn | registry row | findings list only F297; code also carries F361 (A=7 repair, K2-13) and F372 (K2-14/15) legs |
| 07d-qi | qi_algorithms | registry (findings empty) | The docstring cites F218/F219 (and F222 exercises it); the registry lists no findings, and `exactness` is None. |
| 07d-qi | qi_bell_tsirelson | registry (findings empty) | F226 not registered; `exactness` None. |
| 07d-qi | qi_decoherence_floor | registry (findings empty) | F227 not registered; `exactness` None. |
| 07d-qi | qi_entanglement | registry (findings empty) | F212/F214/F218 not registered; `exactness` None. |
| 07d-qi | qi_noise | registry (findings empty) | F221 not registered; `exactness` None. |

## UNPINNED (3)

| Section | Module | Where | Detail |
|---|---|---|---|
| 07c-qed | qed_uv_completion | qed_uv_completion.py:L445 two_sector_solve() | ρ0 = λ·g*·√3·I_cc·ħc/a0⁴: the √3 and g*=2 factors are not explained in code (presumably k-convention Jacobian and two polarisations). |
| 07e-running-thermo-astro | vacuum_energy.py | vacuum_energy.py:L48–49 | Zero-point integral and ρ_vac formula live in the F164 fork (see 08a); not re-derived here |
| 07e-running-thermo-astro | raytrace.py | raytrace.py:L127 | Kerr shadow outline delegated to blackhole.kerr_shadow_outline (see 07b) |

## EXACTNESS unknown (136)

| Section | Module | Where | Detail |
|---|---|---|---|
| 01-constants / 02-numerics | numerics/benchmark.py | benchmark.py:L41-46, L102-109 | Reference chiral and massive W steps are timing baselines only; no exactness class. |
| 03-lattice | lattice.bcc | registry (None) | #1–12 were tagged from the exactness inventory (#1, #3, #19, #59) and by construction; the registry has no class. |
| 03-lattice | lattice.geometry | registry (None) | #1–9 are construction-exact; there is no registry class. |
| 03-lattice | lattice.core | registry (None) | #1–3 are unknown (explicit Euler / scalar wave). #4 is machine from the docstring. |
| 03-lattice | lattice.core_exact | registry (None) | #1–6 were tagged from inventory #4 and by construction. |
| 03-lattice | lattice.curved | registry (None) | #2 (blend) is unknown; the others were tagged from F276/inventory #2. |
| 03-lattice | lattice.blockspin | registry (None) | #7–#13 are unregistered. #5/#6 come from the inventory (F129-A, #188). |
| 03-lattice | lattice.blockspin_baryon | registry (None) | #1–7 are construction-based; #3–4 are fit. |
| 03-lattice | lattice.blockspin_binding | registry (None) | #1–5 are construction-based. |
| 03-lattice | lattice.blockspin_dynamical | registry (None) | #1–5 are construction-based. |
| 03-lattice | lattice.multigrid | registry (None) | #1–6 are construction-based. |
| 03-lattice | lattice.poisson_open | registry (None) | #1–3 are construction-based. |
| 03-lattice | lattice.si_scale | registry (None) | #1–7 are construction-based. |
| 04-core | core.channel | channel.py eqs 1–4 | field_energy, energy_density, T_munu: the registry has no exactness. |
| 04-core | core.channels | channels.py eqs 1, 3–16 (except 12) | The registry has no exactness; only the block-spin paths are covered by inventory #74/#75. |
| 04-core | core.coupled | coupled.py eqs 1, 3–18 | The registry has no exactness; the F388/F389 gate thresholds are quantitative. |
| 04-core | core.entanglement_register | eqs 3, 4, 6, 7 | Eqs 1/2/5 are covered by inventory rows 240–248. |
| 04-core | core.manybody | eqs 1, 2, 4–9 | The registry has neither exactness nor findings. |
| 04-core | core.observers | eqs 1, 2, 4, 5, 6 | These declare an observer-level class (machine/exact) that the registry and inventory do not confirm. |
| 04-core | core.spectral_matter | eqs 1, 3, 4 | The registry has no exactness. |
| 04-core | core.tier3 | eqs 2, 4 | The registry has no exactness. |
| 05a-gauge | gauge.bilinear | bilinear.py:L227-243 (#4) | Same-helicity identity ‖G_T‖=√2\|n̂_y\| stated in the docstring only; no function computes it. |
| 05a-gauge | gauge.colour_dielectric | colour_dielectric.py:L643-667 (#14) | Spatially varying dielectric split-step: order and norm behaviour unverified. |
| 05b-gauge | confinement | confinement.py all (#1–10) | Registry exactness None; docstring claims machine/exact for w(β), σ, χ, V. |
| 05b-gauge | cooling | cooling.py all (#1–10) | Registry exactness None. |
| 05b-gauge | em_photon_sourcing | em_photon_sourcing.py all (#1–8) | Registry exactness None; the gates test at machine precision. |
| 05b-gauge | emission | emission.py all (#1–4) | Registry exactness None. |
| 05b-gauge | gluon | gluon.py all (#1–16) | Registry exactness None (status partial). The even law was spot-checked here at 2.2e-14. |
| 05b-gauge | gluon_self_energy | gluon_self_energy.py #1–3 | Registry exactness None; docstring says A0 exact and A1 machine. |
| 05b-gauge | hypercharge | hypercharge.py all (#1–5) | Registry exactness None; the kinetic-wrap covariance is exact by algebra. |
| 05c-gauge | photon | photon.py rows 1–5, 9 | registry None; only on-axis identity (inventory #220) and momentum conservation are pinned. |
| 05c-gauge | weak_wmu | rows 1–9, 12–13, 15–22, 24–25, 27 | registry None; only F37 chiral (machine) and Proca (machine) pinned by inventory. |
| 05c-gauge | weak_z | rows 1, 3–7 | registry None. |
| 05c-gauge | weak | rows 1–4 | registry None. |
| 05c-gauge | minimal_coupling | rows 1–5 | registry None. |
| 05c-gauge | photon_bound_state | rows 1–6 | registry None (inventory #215 pins only the k=0 secular root). |
| 05c-gauge | propagator | rows 1–4 | registry None. |
| 05c-gauge | strong | rows 8–9, 13, 15–16 | registry None. |
| 05c-gauge | rotation | row 1 | registry None. |
| 06a-particles | particles.derive_generator_norm | registry exactness None | Eqs 1–8 tagged from exactness-inventory #278 or by content; registry silent. |
| 06a-particles | particles.derive_lambda6_sextic | registry exactness None | Eqs 1–7 tagged by content / inventory #279; registry silent. |
| 06a-particles | particles.derive_t2g_pmns | registry exactness None | Eqs 1–6 tagged by content; registry silent. |
| 06a-particles | particles.derive_colour_condensate | registry exactness None | Eqs 1–7 tagged from inventory F88 rows; registry silent. |
| 06a-particles | particles.atom | registry exactness None | Eqs 1–11 tagged from inventory F125-P5 rows; registry silent (also no findings). |
| 06a-particles | particles.baryon | registry exactness None | Eqs 1–8 tagged from inventory F71 rows; registry silent (also no findings). |
| 06a-particles | particles.baryon_dynamics | registry exactness None | Eqs 1–13 tagged from inventory F122 rows; registry silent (also no findings). |
| 06b-particles | particles/dirac.py | eqs 9, 12, 16 | Registry exactness None; not named in the inventory. |
| 06b-particles | particles/eg_sextic.py | eqs 1, 2 | Registry exactness None. |
| 06b-particles | particles/higgs.py | eq 4 | Registry exactness None. |
| 06b-particles | particles/second_quant.py | eq 10 | Registry exactness None. |
| 06b-particles | particles/{dirac_bcc, element, hyperfine, induced_stiffness, majorana, meson, nuclear, nuclear_core, positronium} | module level | Registry exactness None for all manifest-origin modules. Per-equation tags come from the inventory or from the closed-form/solver nature of each equation (see the section file). |
| 07a-cosmology | blackhole | whole module | registry exactness None; rows 1-13 tagged from inventory row 219 where possible, else by construction |
| 07a-cosmology | cosmology | whole module | registry exactness None; rows 1-10 tagged by construction (row 3 from inventory row 218) |
| 07a-cosmology | darkmatter | whole module | registry exactness None; rows 1-5 tagged by construction/toy |
| 07b-gravity | gravity.py | eqs #5, #6, #7, #13, #14 | Registry exactness None; inventory #181–182 cover only the constants, Poisson identity and flat reduction. |
| 07b-gravity | gravity_emergent.py | eqs #1, #3, #4, #5 | Registry exactness None. |
| 07b-gravity | gravity_emqg.py | eqs #1, #2, #4 | Registry exactness None. |
| 07b-gravity | horizon_entropy.py | eqs #1, #2, #3, #5 | Registry exactness None. |
| 07c-qed | qed_amu | qed_amu.py | registry exactness None; inventory rows #300–302 used for eq. 1–5 (none left unknown). |
| 07c-qed | qed_bethe_log | qed_bethe_log.py | registry None; eq. 1–9 tagged from definitions/inventory #277; the module as a whole has no registry class. |
| 07c-qed | qed_casimir | qed_casimir.py | registry None; eq. 1–18 tagged from inventory #228/#229 or by kind; no registry class. |
| 07c-qed | qed_casimir_materials | qed_casimir_materials.py | registry None and no inventory row: eq. 1, 2, 4–8 unknown. |
| 07c-qed | qed_electron_self_energy | qed_electron_self_energy.py | registry None; eq. 1–9 tagged via inventory #280 or by kind. |
| 07c-qed | qed_euler_heisenberg | qed_euler_heisenberg.py | registry None; eq. 1–9 tagged via inventory #306–309. |
| 07c-qed | qed_ir_bremsstrahlung | qed_ir_bremsstrahlung.py | registry None; eq. 1–8 tagged via inventory #281–286. |
| 07c-qed | qed_renormalization | qed_renormalization.py | registry None; eq. 1–11 tagged via inventory #313–320, #332. |
| 07c-qed | qed_scattering | qed_scattering.py | registry None; eq. 1–15 tagged via inventory #287–295. |
| 07c-qed | qed_schwinger_pair | qed_schwinger_pair.py | registry None; eq. 1–5 tagged via inventory #310–312. |
| 07c-qed | qed_twoloop_ae | qed_twoloop_ae.py | registry None; eq. 1–6 tagged via inventory #296–299. |
| 07c-qed | qed_vacuum_polarization | qed_vacuum_polarization.py | registry None; eq. 1–11 tagged via inventory #275 or by kind. |
| 07c-qed | qed_vertex_loop | qed_vertex_loop.py | registry None; eq. 1–9 tagged via inventory #276/#277/#161. |
| 07d-qi | qi_algorithms | qi_algorithms.py | Eqs 1–5 (registry None, no inventory row). |
| 07d-qi | qi_bell_tsirelson | qi_bell_tsirelson.py | Eqs 7–8 ($E_\text{lat}$ bridge, $\delta S$ bound). |
| 07d-qi | qi_cluster_interacting_3d | qi_cluster_interacting_3d.py:L173 | Eq 4 ($\kappa_{110}$, not validated). |
| 07d-qi | qi_decoherence_floor | qi_decoherence_floor.py | Eqs 1–3, 6–7. |
| 07d-qi | qi_entanglement | qi_entanglement.py | Eqs 8, 9, 11 ($t(m)$, $U(m)$, $\theta_\text{tick}$, $\tau_\text{Bell}$). |
| 07d-qi | qi_measurement | qi_measurement.py | Eqs 15, 21 (cone capacity, macroscopic suppression). |
| 07e-running-thermo-astro | qnm.py | rows 1–5 | Manifest record, exactness=None (inventory grades F187 WKB as quantitative <7%) |
| 07e-running-thermo-astro | raytrace.py | rows 1–3 | exactness=None |
| 07e-running-thermo-astro | running_alpha_s.py | none beyond the default (rows tagged from structure) | exactness=None for the module; rows 1–8 tagged by kind of computation only |
| 07e-running-thermo-astro | running_gap_solve.py | rows 1, 4, 5 | exactness=None |
| 07e-running-thermo-astro | running_ir_coupling.py | rows 3, 5 | exactness=None |
| 07e-running-thermo-astro | running_njl.py | rows 4, 7 | exactness=None |
| 07e-running-thermo-astro | running_qstar_logmoment.py | row 2 | exactness=None |
| 07e-running-thermo-astro | running_scale_ratio.py | rows 1, 3, 4 | exactness=None |
| 07e-running-thermo-astro | slowlight.py | row 7 | exactness=None |
| 07e-running-thermo-astro | stellar.py | rows 2, 3, 5 | exactness=None |
| 07e-running-thermo-astro | unified.py | rows 2–6 | exactness=None |
| 08a-forks | forks/gravity/dirac_gravity_fork.py | table #1–9, #13 | registry exactness None. |
| 08a-forks | forks/gravity/gr3_fork_A_phase_tick.py | #1–3 | registry None. |
| 08a-forks | forks/gravity/gr3_fork_B_anisotropic.py | #1–3 | registry None. |
| 08a-forks | forks/gravity/gr3_fork_C_restricted_c.py | #1–4 | registry None. |
| 08a-forks | forks/gravity/gr3_fork_baseline.py | #1–3 | registry None. |
| 08a-forks | forks/gravity/gr3_fork_harness.py | #4–6 | registry None. |
| 08a-forks | forks/gravity/gr3_forks_AB_extended.py | closed forms (α extraction, 1PN force, normaliser) | registry None. |
| 08a-forks | forks/gravity/gr_fork_E_tensor.py | #1–4 | registry None (closed forms algebraically exact). |
| 08a-forks | forks/gravity/gr_fork_F46_dirac.py | #1, #3, #7, #8 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F52_restleg_backreaction.py | #1, #3–5 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F55_spatial_metric_backreaction.py | #1–4 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F56_einstein_coupling_derivation.py | #1, #2 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py | #3 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F59_induced_eh_prefactor.py | #1, #7 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F60_channel_reconciliation.py | #4 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F61_weyl_eta_gstar.py | #1, #2, #5 | registry None; Fraction arithmetic without inventory row. |
| 08a-forks | forks/gravity/gr_fork_F63_spin_torsion_estimate.py | #1–5 | registry None. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | #1–3, #5, #6, #8, #11, #13–15, #22, #23, #25, #29, #32 | registry None; sympy results exact in fact but no inventory row. |
| 08a-forks | forks/gravity/gr_fork_F79_structural_G.py | #5, #6 | registry None. |
| 08a-forks | forks/gravity/gr_tensor_stub.py | #1 | registry None. |
| 08b-forks | gr_fork_F164_cosmological_constant | gr_fork_F164_cosmological_constant.py | eq 1–6 (registry None, no inventory row) |
| 08b-forks | gr_fork_F193_ontic_vacuum | gr_fork_F193_ontic_vacuum.py | eq 3, 5, 6 |
| 08b-forks | gr_fork_F196_dilution_exponent | gr_fork_F196_dilution_exponent.py | eq 5 |
| 08b-forks | gr_fork_F197_first_excitation_dark | gr_fork_F197_first_excitation_dark.py | eq 1–6 |
| 08b-forks | gr_fork_F198_angular_misalignment | gr_fork_F198_angular_misalignment.py | eq 1–6 |
| 08b-forks | gr_fork_F199_amplitude_mode_stability | gr_fork_F199_amplitude_mode_stability.py | eq 1–5 |
| 08b-forks | gr_fork_F200_sterile_neutrino_dm | gr_fork_F200_sterile_neutrino_dm.py | eq 1–7 |
| 08b-forks | gr_fork_F201_kev_from_eg_texture | gr_fork_F201_kev_from_eg_texture.py | eq 1–5 |
| 08b-forks | gr_fork_F202_leptogenesis_sakharov | gr_fork_F202_leptogenesis_sakharov.py | eq 1–2 |
| 08b-forks | gr_fork_F203_dark_sector_falsifiers | gr_fork_F203_dark_sector_falsifiers.py | eq 1–4 |
| 08b-forks | gr_fork_F216_massive_spin2 | gr_fork_F216_massive_spin2.py | eq 1–8 |
| 08b-forks | gr_fork_F223_spin2_binding_relic | gr_fork_F223_spin2_binding_relic.py | eq 2, 7 |
| 08b-forks | gr_fork_F228_geon_production_stability | gr_fork_F228_geon_production_stability.py | eq 4, 8, 9 |
| 08b-forks | gr_fork_F238_geon_relic_abundance | gr_fork_F238_geon_relic_abundance.py | eq 1–6 |
| 08b-forks | gr_fork_F248_tt_graviton_bcc | gr_fork_F248_tt_graviton_bcc.py | eq 1 |
| 08b-forks | dm_fork_F205_sterile_qke_boltzmann | dm_fork_F205_sterile_qke_boltzmann.py | eq 1–10 |
| 08b-forks | dm_fork_F237_kev_sterile_resolution | dm_fork_F237_kev_sterile_resolution.py | eq 1–5 |
| 08b-forks | hypercharge_fork | hypercharge_fork.py | eq 1–6 |
| 08b-forks | curl_fork_baseline_bcc | curl_fork_baseline_bcc.py | eq 1 |
| 08b-forks | curl_fork_cubic | curl_fork_cubic.py | eq 1–3 |
| 08b-forks | curl_fork_harness | curl_fork_harness.py | eq 1–5 |
| 08b-forks | lgt_fork_A_mc | lgt_fork_A_mc.py | eq 1, 2, 4, 5, 7–11 |
| 08b-forks | smearing_fork_harness | smearing_fork_harness.py | eq 1–5 |
| 08b-forks | complex_mass_fork | complex_mass_fork.py | eq 1–7 |
| 08b-forks | derive_weight_as_phase | derive_weight_as_phase.py | eq 1–7 |
| 09-shims | particles/spec.py | spec.py:L52-168 | #1–5 (registry silent; exact Fraction arithmetic) |
| 09-shims | particles/composite.py | composite.py:L48-171 | #1–3, #5 (registry silent; exact Fraction arithmetic) |
| 09-shims | particles/channel.py | channel.py:L75-2058 | #1–34, #36–43 (registry silent; observers self-declare quantitative; #41 tagged fit) |

## OTHER (251)

| Section | Module | Where | Detail |
|---|---|---|---|
| 01-constants / 02-numerics | constants/lepton.py | lepton.py:L145 (W_star) | Value is the literal 6*0.243 rather than 6*lambda_6, so it can drift from lambda_6. Tree sites expect 1.46 vs computed 1.458. |
| 01-constants / 02-numerics | constants/strong.py | strong.py:L135-139 (GeV_per_lattice_unit) | Class `exact`, but the value is Λ_NJL/π with Λ_NJL a fit (L134/L319); exact only as a conversion. |
| 01-constants / 02-numerics | constants/strong.py | strong.py:L319, L341, L359 (Lambda_NJL_GeV, G_Lambda2_NJL, m0_current_quark_MeV) | Classed `external` but the derivation strings say FITTED. Map tag `fit` applies. |
| 01-constants / 02-numerics | constants/strong.py | strong.py:L424 (r_c_hardcore_fm) | Classed `quantitative` but it is the tuned knob of F104 (fit to the deuteron binding). |
| 01-constants / 02-numerics | constants/measured.py | measured.py:L144-155 | The W_star coincidence record (A–S erfc coefficient) has provenance=() (allowed, but the only empty one). |
| 01-constants / 02-numerics | numerics/fft.py | fft.py:L3-4 | Stale docstring: "deprecation shim remains until C9", but C9 has deleted the shims. |
| 01-constants / 02-numerics | numerics/benchmark.py | benchmark.py:L60-127 | The benchmark runs at import (no __main__ guard); a package walk importing it runs the FFT timing loop. Also: sys.path insert (L12), stale name benchmark_jax.py, unregistered m_W=0.3 literal (L103, L114). |
| 01-constants / 02-numerics | numerics/lazy.py | lazy.py:L1-2 | Stale self-name ca_lazy.py. It is emergent-time bookkeeping rather than a numerics primitive. |
| 03-lattice | lattice.bcc | bcc.py:L263–269 | The FFT-grid symbol U(k) is not 2π-periodic (shifting k_x by 2π changes U by 1.41; √3π(110) is a period to 3e-16). So the stepper is F267's band-limited fractional walk, not a nearest-neighbour hop on the array. Two unit conventions coexist: (W) bcc.py uses hop d/√3; (G) geometry.py uses hop d and cube side 2. |
| 03-lattice | lattice.geometry | geometry.py:L259 | The BZ weight 1/4 (`make_kgrid_bcc`) is valid for the gauge convention (G) only. It does not transfer to the walk (F267). |
| 03-lattice | lattice.bcc | bcc.py:L328 | `measure_bcc_dispersion` uses np.linalg.eig on a chiral 2×2 (CLAUDE.md hazard). This is a verifier only. |
| 03-lattice | lattice.time_generator_axiom_independence | time_generator_axiom_independence.py:L201 | The wavepacket polarisation comes from xp.linalg.eig of a chiral 2×2 unitary (eig-on-chiral hazard). |
| 03-lattice | lattice.time_generator_axiom_independence | time_generator_axiom_independence.py:L219–249 | The default run (L=48, σ=4, k0=(0.3,0.2,0.1), 60 ticks) wraps the periodic box. In the re-run baseline, edge weight is 0.19 at t=40 and 0.23 at t=60, and the centroid x̄ goes from +8.8 to −2.8. The fitted variance exponents include wrap contamination (the failure mode wavepacket.py/F20 names). Not settled. |
| 03-lattice | lattice.bcc_point_symmetry | bcc_point_symmetry.py:L322–331 | The shipped walk's exact symmetry is D4h (order 16); O_h holds only in the IR (F344). Cross-reference for any text calling the walk O_h-symmetric (F75). |
| 03-lattice | lattice.blockspin | blockspin.py:L365–433 | T3b uses the exponential dielectric K=e^{2u} and the F106 energy-only Poisson law. Under decision 4/F178 these are the static weak-field reduction only. |
| 03-lattice | lattice.cell_internal_index | cell_internal_index.py:L197–203 | `walk()` uses u·I + iσ·ñ, the adjoint of the engine's u·I − iσ·ñ (sign convention). Ranks are unaffected. `_bloch`/`_u` re-type the walk with `math.sqrt(3.0)` instead of c_lat/_bcc_uvec (D7). |
| 03-lattice | lattice.core | core.py:L239–298 | The split-step is the continuum propagator e^{-icσ·k} (linear ω=c\|k\|), not a lattice QCA. `c` is `c_unitary`, not c_lat. |
| 03-lattice | lattice.core_exact | core_exact.py:L39 | `SQRT2 = np.sqrt(2.0)` is an unregistered literal (D7). |
| 03-lattice | lattice.curved | curved.py:L490–512, L397 | The `measure_refraction` angle is invalid under periodic wrap (docstring). The Strang stepper hard-codes external dt=1. |
| 03-lattice | lattice.derive_walk_bz_measure | derive_walk_bz_measure.py:L211–212, L99 | The verdict flags `fermion_sector_needs_a_measure_correction=True` and `correction_is_the_gauge_factor_4=False` are hard-coded, not computed. `CUBE_OVER_ZONE` uses `np.sqrt(3.0)`, while `ROOT3` uses 1/c_lat. |
| 03-lattice | lattice.derive_walk_bz_measure | derive_walk_bz_measure.py:L154–175 | Exactness tension: the registry says `exact`, but S4 is Monte Carlo (quantitative). |
| 03-lattice | lattice.blockspin_baryon | blockspin_baryon.py:L69 | The fitted calibration κ=2.0006 is a hard-coded literal, registered neither as a constant nor as a MeasuredConstant. |
| 03-lattice | lattice.blockspin_dynamical | blockspin_dynamical.py:L58 | `WATSON3 = 0.5054620197` is an unregistered literal (D7). |
| 03-lattice | lattice.multigrid | multigrid.py:L51–53, L67–74 | The sys.path insert is a legacy flat-import shim, and the bare `except Exception` silently falls back to a local reshape. |
| 03-lattice | lattice.si_scale | si_scale.py:L81, L82–83, L152–167 | Symbol clash: here `a` is the walk unit length, while in F278/bcc.py `a=2c_lat` is the cube edge. np.sqrt(3.0) is used rather than 1/c_lat. Unregistered literals: m_p=938.272, Δm=1.293, m_u=2.16, m_d=4.67, δ_em=1.00, m_q=0.785, α_s=0.5. |
| 03-lattice | lattice.time_signature | time_signature.py:L504, L544 | `is_a_square: False` and `d_space_from_commutant: 3` are hard-coded. Open: the ring is C[Z^3] in w_j, while the walk lives in the BCC sublattice ring (docstring input 3: locality w.r.t. Λ, index 4). Whether C3's shift group is Z^3 or Λ is unsettled. |
| 03-lattice | lattice.time_signature_interacting | time_signature_interacting.py:L195–206 | The momentum grid is the walk-variable torus θ=2πn/L (θ=k/√3), not bcc.py's FFT convention. For even L it holds 4 copies of the walk zone; the default L=3 avoids this. |
| 03-lattice | lattice.time_single_generator | time_single_generator.py:L109–122 | The docstring concedes that G2's residual is near-tautological (both paths share bcc_unitary/_kinetic_n). Only the signature leg is independent. |
| 03-lattice | lattice.wavepacket | wavepacket.py:L111 | `np.sqrt(3.0)` literal in the off-axis control. The registry says `exact`, while #2 and #8 are machine-class (the module labels them correctly). |
| 03-lattice | lattice.bcc, lattice.geometry, lattice.core, lattice.core_exact, lattice.curved, lattice.poisson_open, lattice.multigrid, lattice.si_scale, lattice.blockspin* | registry.tsv | Manifest-origin modules carry no `findings` and no `exactness` in the registry. |
| 04-core | core.tier3 (refraction_2d) | tier3.py:L129 → lattice/curved.py:L189 | The S10 note says F271's ordering/half-step defects sit in `curved._half_step_dH` and affect every variable-c result. The code now defaults to ordering='weyl', order=2, which suggests it is fixed but the ledger does not say so. Needs 03-lattice confirmation. |
| 04-core | core.observers (Momentum) | observers.py:L398-399 | Verified crash: `Momentum().observe()` on any channel with a colour-stacked (3,L,L,L) spinor (`composite`, Weyl quark `particle`, `quark_dirac`) raises TypeError (`make_kgrid_3d` gets 4 args). |
| 04-core | core.coupled | coupled.py:L96, L132, L389, L486 | Default partner names live inside `step()`; if a scenario omits `fermion:`/`w_field:`/`photon:`, the bus sees no edge, strict mode cannot catch a missing or misordered partner, and the step raises KeyError at runtime. |
| 04-core | core.coupled / particles.channel | coupled.py:L194 (charge_coupling.py:L289) vs coupled.py:L101, L417; particles/channel.py:L987; gluon.py:L779 | The source-term sign is inconsistent: `charge_photon` uses E −= dt·J (Ampère), while w_sourced/em_photon/photon_sourced/gluon_sourced use E += g·J. |
| 04-core | particles.channel (consumer of the core bus) | particles/channel.py:L343-345, L646-648 vs L347, L362-386, L419 | The EM coupling form is inconsistent: confined-Dirac and `quark_dirac` apply a bare per-tick phase e^{−iqα} with α the ACCUMULATED ∫φ_em dt, while the other paths use the wrap e^{+iqα}·W·e^{−iqα}. |
| 04-core | core.blockspin / core.simulation | blockspin.py:L69-99; channels.py:L231-234, L259-262; coupled.py (all step()) | Only photon_pair, weyl_bcc and w_chiral have renormalised coarse rules. z_even, gluon_bcc, every coupled.py channel and every particle channel keep stepping the fine rule after an R_b event with no guard (photon_pair+gravity does raise). `block_state` also averages non-field arrays such as em_photon `rho`/`A`. |
| 04-core | core.simulation | simulation.py:L96, L254 | The `LatticeSpec.topology` default is "cubic" although BCC is canonical (D1). |
| 04-core | core.clock | clock.py:L320-332 | The default `auto` mode resolves to `legacy` for any mixed-dt scenario, which leaves those channels desynchronised (F268: 18/46 scenarios). It is recorded in results but not corrected. |
| 04-core | core.entanglement_register | entanglement_register.py:L76 → qi_entanglement.py:L316-331 | The hopping t(m) behind θ=J/4 is measured on the 2-D square `dirac_step_2d_splitstep`, not the BCC 3-D kernel (lattice-convention question). |
| 04-core | core.manybody | manybody.py:L81-82, L242, L42-44 | Unregistered literals M_E_MEV=0.51099895, ALPHA=1/137.035999084 and omega_g2_4pi=5.39 bypass the D7 registry; there is a sys.path hack. |
| 04-core | core.* (all except photon_fermion_push) | module imports | Direct `import numpy` (np.linalg.eigh, np.einsum, np.exp) outside the casim.numerics façade (D8); FFTs are routed through numerics.fft. |
| 04-core | core.spectral_matter | spectral_matter.py:L112-113, L163-164, L204-205 | `energy()` returns f_π / m_p / a ratio (not an energy), so `norm_conservation` is trivially 0 for these channels. |
| 04-core | core.photon_fermion_push | photon_fermion_push.py:L47 | `c_lat` is imported and unused. |
| 05a-gauge | gauge.charged_current | charged_current.py:L406 run_beta_decay_pipeline(); weak_wmu.py:L1966-1969 | Law vs F91: W± is classified chiral (forced), but the β-decay pipeline propagates W⁻ with the massive EVEN law ω_eff=√(m_W²+Ω_even²). |
| 05a-gauge | gauge.colour_condensate | colour_condensate.py:L396-403 u1_metropolis_3d() | Staples computed once per direction μ and reused for both checkerboard parities. Same-direction links of the other parity share plaquettes, so the second half-sweep uses stale staples (detailed balance broken). The monopole density ρ(β) and the chained m_D, v, σ_F86 (and colour_dielectric.condensate_vev_from_mc) inherit this. bcc_action guards against the same defect. |
| 05a-gauge | gauge.charge_coupling | charge_coupling.py:L472-582 check_curl_grad_identity_diagnostic() | bcc_curl_symbol fails curl(grad)=0 maximally (mean 0.74/0.71); gated as a known defect (F393), not fixed. C is built from branch '+' only. |
| 05a-gauge | gauge.bilinear | bilinear.py:L1980-1985 rotation_step_em_spectral() | Chiral-transform hazard: the single-branch law breaks Hermitian symmetry, so real (E,B) inputs return complex output (acknowledged in a comment; no real-pair split). |
| 05a-gauge | gauge.bilinear_2d | bilinear_2d.py:L256-259 rotation_step_em_spectral_2d() | Takes .real of the IFFT when inputs are real. Safe here (the 2-D rate is even in k), but this is the pattern CLAUDE.md flags for chiral laws. |
| 05a-gauge | gauge.chiral_anomaly | chiral_anomaly.py:L351-352, L718-719, L725 | Tautological legs: vector_div_cancels compares γ^a−γ^a; A_V/A_A are arithmetic on a hand-set ±A₀; the charge cube is q³−q³. The Fujikawa gate tests magnitude only, with a hand-inserted −2/i (L486). |
| 05a-gauge | gauge.chiral_anomaly | chiral_anomaly.py:L139-143 | Unregistered literals M_PI0_MEV=134.9768, ALPHA_EM=1/137.035999, GAMMA_PI0_PDG_EV=7.80±0.12 (D7). |
| 05a-gauge | gauge.bgfield_loop | bgfield_loop.py:L55-57, L304-306, L322 | Unregistered literals C_A=3.0, 11/3·C_A, 0.97, 28.81, 1.78, and 0.733 (the last duplicates registered q_star_a_implied=0.7327). |
| 05a-gauge | gauge.casimir_scaling | casimir_scaling.py:L452-455 | Unregistered literals m_Planck=1.220890e19 GeV, 16π, 11·3. |
| 05a-gauge | gauge.bcc_action | bcc_action.py:L1410 | c_lat² hard-coded as Fraction(1,3) instead of importing c_lat from casim.constants. |
| 05a-gauge | gauge.bilinear_2d | bilinear_2d.py:L288 | c_analytic=1/√2 literal; a MeasuredConstant 1/√2 (F26) exists in constants/measured.py. |
| 05a-gauge | gauge.bcc_action, bgfield_loop, bilinear, bilinear_2d, charge_coupling, charged_current, colour_condensate, colour_dielectric | module imports | Direct `import numpy as np` (D8 façade bypassed). |
| 05a-gauge | gauge.charged_current | charged_current.py:L71 | sys.path.insert(0, dirname(__file__)) pre-C9 import hack. |
| 05a-gauge | gauge.charged_current | charged_current.py:L385-386 | Right-handed chi_u/chi_d built "that must NOT couple" but never used, so the claim is asserted, not tested. |
| 05a-gauge | gauge.colour_theta | colour_theta.py:L420 | Import-time mutation of lpt_bcc_vertex.ACTIONS (adds "bcc_1sense"). |
| 05a-gauge | gauge.a_field_convention | a_field_convention.py:L212-222 | Disclosed inconsistency: sourcing a longitudinal E under the paired-photon scalar rotation produces a nonzero C-longitudinal B ("monopole" artifact), because Ω_pair ≠ \|C_odd\| beyond small k. |
| 05a-gauge | gauge.bcc_action, bgfield_loop, bilinear, bilinear_2d, charge_coupling, charged_current, chiral_anomaly, colour_condensate, colour_dielectric | registry.tsv | Registry records no findings and no exactness (manifest-origin records), although inventory rows cite several of these modules by name (e.g. bcc_action #231–238, charge_coupling #179–180, chiral_anomaly F264, colour_dielectric F86-CD*). |
| 05b-gauge | derive_charge_partition | derive_charge_partition.py:L265 | tan θ_W at sin²θ_W = 1/4 is compared against `c_lat` (a speed constant). This merges the coincident 1/√3 constants against the constants rule. |
| 05b-gauge | derive_bilinear_so3 | derive_bilinear_so3.py:L281–313, L409–414 | Check C6 reads a hand-written static sector list and cannot detect code changes in the sectors it names. |
| 05b-gauge | derive_internal_index_existence | derive_internal_index_existence.py:L294 | S5 "matches F324 bracket" compares against a list built with equivalent logic in the same function, so it is tautological. |
| 05b-gauge | derive_su3_structure | derive_su3_structure.py:L451 vs lattice/bcc.py:L133 | Re-typed walk uses u·1 + i n·σ; bcc.py documents U = u·1 − i n·σ. Sign convention differs (unitarity and commutant unaffected). L136–137 are dead duplicate code. |
| 05b-gauge | derive_x1_branch | derive_x1_branch.py:L136, L497 | Direct `import numpy` in a spine module (D8). The `n_links` parameter of check_x1_branch is unused. |
| 05b-gauge | em_current | em_current.py:L152–165 | The naive/transverse current uses σ, while the BCC walk block is in the conjugate representation σ* (see derive_charge_partition L14, L123). The y-sign is not addressed. |
| 05b-gauge | em_photon_sourcing | em_photon_sourcing.py:L217 vs L223 | Transverse sector sourced with +g·J_T, but E_L solves iC·E_L = +ρ with no g. The naive longitudinal accumulation would give iC·E_L = −gρ, so the relative sign and coupling of the two sectors is inconsistent (open, not settled). |
| 05b-gauge | emission | emission.py:L84–85, L100 | Radial solver eigenvalues Ei/Ef are computed and discarded; ω uses exact Bohr levels. Unregistered literals t_au and hc; sys.path hack. |
| 05b-gauge | confinement | confinement.py:L93 | plaquette_mean hardcodes /3.0 and an SU(3) torus while exposing an n_c argument. |
| 05b-gauge | gluon | registry | Registry lists no findings for gluon (F43/F91/F265 are not linked); status partial. |
| 05b-gauge | gluon_self_energy | registry; gluon_self_energy.py:L80–82, L344–345 | Registry lists no findings (F155 not linked). Unregistered literals GEOM_MEAN_BAND, C_A, 1.78, 28.81, 0.348. |
| 05b-gauge | hypercharge | hypercharge.py:L334–336; registry | Quark hypercharges 1/3, 4/3, −2/3 are unregistered float literals (deliberate, N_c-dependent). Registry lists no findings. α(x) is pure gauge, with no U(1)_Y field dynamics. |
| 05b-gauge | derive_ncolour | derive_ncolour.py:L162, L348 | μ0 = 1.850e18 GeV and g_s = 0.5 are module literals, not registry constants. |
| 05c-gauge | weak_wmu | weak_wmu.py:L1176–1177 w_self_interaction_step(); L1469–1470 wmu_mass_stueckelberg() | R_b=(δW²+iδW¹)·sin(θ/2)/θ corresponds to exp(i(θ/2)(n₁σ₁−n₂σ₂+n₃σ₃)); make_su2_link_uniform (L1604) and extract_EW_BW (L645–647) use b=sin·(in₁−n₂). W² sign inconsistent — not settled. |
| 05c-gauge | weak_wmu | weak_wmu.py:L2040–2045 measure_photon_dispersion_from_mix() | Evolves with even Ω_even but predicts 2ω⁺(k/2); differs at O(k³) off-axis. |
| 05c-gauge | weak_wmu | weak_wmu.py:L1403–1420, L1448–1456 | Stueckelberg "mass" is a heuristic: m_W from ⟨\|∇U_st\|²⟩ (not g·f), U_st evolved by heat flow e^{−k²dt}, not a wave equation. |
| 05c-gauge | lpt_wilson_selfenergy | lpt_wilson_selfenergy.py:L214, L222 _pi_chunked() | k+q wrapped into [−π,π) while the ghost/Abbott factor k̂(k)+k̂(k+q) is a sum of 4π-periodic terms — the F307 refold defect, repaired only in lpt_selfenergy (F308); F277's supersession record calls lpt_* Wilson wraps exact no-ops. Bites when Q>π/n. |
| 05c-gauge | lpt_wilson_selfenergy | lpt_wilson_selfenergy.py:L309–313 transversality_check() | Near-tautological: f₀ is defined as −Π₀₀, q̂ has one nonzero component, so it only tests Π₀ₙ=0. |
| 05c-gauge | lpt_bcc_vertex | lpt_bcc_vertex.py:L396–401 gate_ward(); L487–513 propagator_split() | G5 checks the closed-form Γ (not generated vertex2) — tautological; propagator_split always pass=True. |
| 05c-gauge | lpt_bcc_vertex vs lattice.bcc | lpt_bcc_vertex.py:L89 | Gauge link axes are integer ⟨111⟩ (length √3); the Weyl walk hops d/√3 — two different BCC scalings coexist. |
| 05c-gauge | photon_bound_state | photon_bound_state.py:L63–65 _grid() | BZ average over p∈[0,2π)³; the walk dispersion at k/√3 has period 2√3π, and other kernels use fftfreq [−π,π). Domain choice unjustified in code. `bound_state_secular` (L233–235) has no closed-threshold option. |
| 05c-gauge | strong | strong.py:L443, L525–545 _cov_cayley_1dir() | Non-cold Cayley kinetic step uses σ_x for both x and y (H_μ=σ_x p_μ), whereas the cold-link path is the exact 2-D Weyl QCA — different Hamiltonians on the two branches. Not settled. |
| 05c-gauge | strong | strong.py:L1413–1422 covariant_quark_doublet_step_2d() | Wraps the unitary doublet step in `covariant_half_step`, which its own docstring (L370–374) says is non-unitary. |
| 05c-gauge | su3_ladder | su3_ladder.py:L266–269 | Returns the slope λ/(2g²) whose "same log law as U(1) rotor" reading the module's own F325 note (L65–81) calls link-count inconsistent. |
| 05c-gauge | rotation | rotation.py (whole module) | Hartle frame-dragging / NS moment of inertia (astrophysics) filed under engine/gauge/; belongs with interactions (interior_metric). |
| 05c-gauge | photon_packet, lpt_ws_mask_cutcell | registry.tsv | Registry exactness `exact` but key outputs are machine (packet drift 1e-12) / quantitative (octree mask bias); mixed modules. |
| 05c-gauge | propagator | propagator.py:L434 phase_rate_zeropad() | Peak search only over the first half of the padded spectrum; negative frequencies of a complex signal not seen. |
| 06a-particles | particles.derive_higgs_bhl_compositeness / particles.derive_M_R_scale_link | derive_higgs_bhl_compositeness.py:L117 vs derive_M_R_scale_link.py:L51-54,L64 | Two definitions of the model UV cutoff, both citing F107: E_P/(a/ℓ_P)=1.850e18 GeV vs 3^{-1/4}·M_Pl(non-reduced)=9.277e18 GeV; differ by exactly √(8π). |
| 06a-particles | particles.derive_lepton_frame_fork | derive_lepton_frame_fork.py:L337-358 | Engine module exec's the source of a test file (tests/findings/test_F118_self_consistent_Wvc_and_C.py, sliced at "def constrained_H2"); K1b rests on F118's fitted (v,c)=(0.16,1.10). |
| 06a-particles | particles.derive_generator_norm | derive_generator_norm.py:L102,L139,L177,L220 | Script body (computation + prints) runs at import; only the JSON write is __main__-guarded. |
| 06a-particles | particles.derive_lambda6_sextic | derive_lambda6_sextic.py:L53,L73,L98,L125,L197-198 | Script body (computation + prints) runs at import; only the JSON write is __main__-guarded. |
| 06a-particles | particles.derive_composite_scalar_fermion_coupling | derive_composite_scalar_fermion_coupling.py:L214-216 | NJL triple (0.6515, 2.10, 0.0055) re-typed as literals matching registered Lambda_NJL_GeV, G_Lambda2_NJL, m0_current_quark_MeV (D7 rogue literal); own _results_dir duplicates _results_path. |
| 06a-particles | particles.derive_lepton_shape_precision_floor | derive_lepton_shape_precision_floor.py:L63 | η²=1/2 (derived exact, F92) is a local literal, not a registered constant. |
| 06a-particles | particles.derive_M_R_scale_link / particles.derive_t2g_pmns | derive_M_R_scale_link.py:L184 vs derive_t2g_pmns.py:L118 | M_R0 multiplies the √-amplitude in F343 C4 but the squared amplitude in derive_t2g_pmns — inconsistent scale convention. |
| 06a-particles | particles.derive_delta_cp_t2g | derive_delta_cp_t2g.py:L40-67 | Complex-hazard record: takagi T5 (allclose default atol dropped imaginary part at m_ν~1e-9) and T6 (sign) — fixes live in majorana.py, not here as docstring implies. |
| 06a-particles | particles.baryon | baryon.py:L294-302 | Total exchange sign set equal to colour sign; spatial symmetry asserted +1, not computed. |
| 06a-particles | particles.baryon_dynamics | baryon_dynamics.py:L467-489 | neutron_minus_proton takes EM self-energies as external args; model-native em_self_energy_pairwise (F372) not wired in. |
| 06a-particles | particles.derive_quark_B_colour_charge | derive_quark_B_colour_charge.py:L82,L318 | m_τ=1776.93 here vs 1776.86 elsewhere; variable k2l holds k²−1. |
| 06a-particles | particles.derive_colour_condensate | derive_colour_condensate.py:L190-193 | Exactness-inventory F88-CC2 states each zeta sum = −11/12; code checks only the total −11/6. |
| 06a-particles | particles.derive_M_R_scale_link, particles.derive_delta_cp_t2g | registry exactness=exact | Registry tags module `exact` but content includes numeric scans / random-phase statistics (quantitative). |
| 06b-particles | particles/dirac.py | dirac.py:L447–450 vs L139–142 | Sign convention. D_k carries +imβ (at k=0, exp(+iβ arcsin m)), but the varm mix applies exp(−iβ δm dt). The Strang composite rotates by arcsin m0 − δm, so the local mass perturbation enters with the opposite sign and linearly. The same applies to dirac_bcc.py:L207–210 / L238–242. |
| 06b-particles | particles/dirac_bcc.py | dirac_bcc.py:L123–126 vs gauge/weak_wmu | Two inequivalent massive-Dirac discretisations. dirac_bcc pairs A⁺ with A⁺†, un-split, with n/m weights. weak_wmu.covariant_dirac_doublet_step pairs A⁺ with A⁻ as a K·Mass·K sandwich with cos m/sin m weights. F378 leg E1 shows only dirac_bcc has the CPT theorem. Unresolved. |
| 06b-particles | particles/induced_stiffness.py | induced_stiffness.py:L572, L584 dirac_bands() | np.linalg.eig/inv act on the 4×4 chiral Dirac matrix (chiral-transform hazard). It is guarded by an analytic arccos(n·u) residual; the docstring's "no np.linalg on chiral structure" holds only for the Weyl path. |
| 06b-particles | particles/eg_sextic.py | eg_sextic.py:L167, L179–180 | Magic literals: 24.0 in the gap update (with dead `M0_TARGET * 0 +`), C_QUARTIC_F118=1.10 and its band. |
| 06b-particles | particles/higgs.py | whole module | A Higgs scalar module sits against Core decision 3 (hypercharge on U(x), no Higgs field). It is package-only, unreached, and not recorded in supersessions.yaml. |
| 06b-particles | particles/hyperfine.py | hyperfine.py:L51–66 | D7: CODATA/PDG literals (α, m_e, m_p, h, ħc, g_p, r_p) are hard-coded, not taken from casim.constants. |
| 06b-particles | particles/positronium.py | positronium.py:L67–72 | D7: CODATA literals (α, m_e, h, ħ) are hard-coded, not taken from casim.constants. |
| 06b-particles | particles/meson.py | meson.py:L65, L196 | Unregistered literals: m0=0.0055 GeV, WATSON3=0.5054620197. The real-space demo is simple-cubic (D1 reference). |
| 06b-particles | particles/nuclear.py | nuclear.py:L70–73, L90–91, L124, L167–168 | Unregistered literals: HBARC, M_PI_DEFAULT=138.039, GCM_DEFAULT=18.31, B_QUARK_DEFAULT=0.55, M_SIGMA_DEFAULT=622.4, M_OMEGA_DEFAULT=782.66, OMEGA_G2_4PI_OBE=11.0. The module docstring still calls r_c "the one tuned knob". |
| 06b-particles | particles/second_quant.py | registry row | reach=driven but n_reachable_from=0 (inconsistent labelling). |
| 06b-particles | several (dirac, dirac_bcc, eg_sextic, element, higgs, induced_stiffness, majorana, meson, nuclear, second_quant) | top-of-file imports | D8: `import numpy as np` directly (only FFTs routed via casim.numerics). |
| 07a-cosmology | cosmology_second_scale | cosmology_second_scale.py:L140-L159 classification_theorem() | F286's reading of $p=0$ as trivial corrected by F295 A1 (prose correction; no ledger entry) |
| 07a-cosmology | cosmology_growth | cosmology_growth.py:L423-L931 | registry `exact` but D3a/D3b/D4/D5/B2 are RK4/Simpson/χ² numerics (quantitative per inventory F288) |
| 07a-cosmology | cosmology_blockspin_fluctuation | cosmology_blockspin_fluctuation.py:L299-L307 | registry `exact` but C2 leg is quantitative (2 % tol) |
| 07a-cosmology | cosmology_critical_measure | cosmology_critical_measure.py:L248-L251 critical_gaussian_squared() | integral $\int_0^1\frac{dx}{x}\ln\frac{1+x}{1-x}$ never evaluated; series computed and `upper_half = lower_half` asserted by $x\to1/x$ |
| 07a-cosmology | cosmology_critical_measure | cosmology_critical_measure.py:L280 gapped_measure_is_white_noise() | vacuous check: limit in k of an expression with no k |
| 07a-cosmology | cosmology_critical_measure / cosmology_holographic | cosmology_critical_measure.py:L168; cosmology_holographic.py:L106 | BK18 r bound 0.034 vs 0.036 in the two modules |
| 07a-cosmology | cosmology_geon_domain_wall_reopening | cosmology_geon_domain_wall_reopening.py:L139 | symbol A declared positive=False while cos6δ=-1 are minima only for A>0; sign of reused amplitude never checked |
| 07a-cosmology | cosmology_lattice_elasticity / cosmology_lambda_dynamics | cosmology_lattice_elasticity.py:L249; cosmology_lambda_dynamics.py:L155 | two SI tick conventions differ by √3: t_min = a/(c_lat c) (tick = a/c) vs τ = a/(√3 c) (c_lat a/τ = c); F284's 11.43 t_P rests on the first |
| 07a-cosmology | cosmology_lambda_dynamics / cosmology_lambda_sign_split | qed_uv_completion.py:L416 via sakharov_moments; cosmology_lambda_dynamics.py:L248 | zero-point moments use single chiral branch ω⁺ (sign '+') of BCC Weyl dispersion; branch choice undeclared in these modules |
| 07a-cosmology | cosmology_lambda_dynamics | cosmology_lambda_dynamics.py:L225-L244 | bcc_dispersion(κ/b) underflows silently for b ≳ 3e8; guarded at b ≤ 1e6; K4 extrapolates a fitted power law to b* ~ 1e30 |
| 07a-cosmology | cosmology_bbn | cosmology_bbn.py:L1000 bd_sensitivity() | mutates module-global BINDING_MEV["d"] outside run_bbn's save/restore |
| 07a-cosmology | cosmology | cosmology.py:L159 age_of_universe_gyr() | np.trapz removed in NumPy ≥ 2.0 |
| 07a-cosmology | blackhole, cosmology, darkmatter | module imports | direct `import numpy` (D8 façade not used; pre-C9 manifest modules) |
| 07a-cosmology | blackhole | blackhole.py:L238-L256 lattice_core_radius() | lattice-core cap $\mathcal K_\max=a^{-4}$ is a posited criterion, not derived |
| 07a-cosmology | cosmology_lambda_sequestering | cosmology_lambda_sequestering.py:L239 | F319 selectivity 1.27e116 hard-coded; several unused imports; control sets check False by assignment (L263) |
| 07a-cosmology | cosmology_lambda_sequestering_consistency | cosmology_lambda_sequestering_consistency.py:L285, L295-L296 | finite_time_only control assigns False; DESI w0/wa are "illustrative" literals |
| 07a-cosmology | cosmology_anomalous_dimension | cosmology_anomalous_dimension.py:L184, L222 | cutoff uses non-reduced M_Pl·3^{-1/4}; 2/9 compared as a bare literal; c_lat imported unused |
| 07a-cosmology | cosmology_transfer_function | cosmology_transfer_function.py:L273-L290 | transfer_eh98_with_sound_horizon duplicates cosmology_growth.transfer_eh98 line-for-line (drift risk) |
| 07a-cosmology | cosmology_second_scale | cosmology_second_scale.py:L119 | DECADES_PIVOT_TO_BZ transcribed float, not recomputed from a_over_ellP |
| 07a-cosmology | darkmatter | darkmatter.py:L50-L51, L82-L99 | v_total ignores **kw; Bullet offset set by hand-placed Gaussians (illustrative) |
| 07b-gravity | gravity_backreaction.py | whole file | Misnamed/misfiled: dual-Ginzburg–Landau colour confinement (F86/F137, legacy `ca_dual_gl_backreaction.py`), not gravity; registry findings empty. |
| 07b-gravity | derive_dielectric_noconfine.py | derive_dielectric_noconfine.py:L63–79 vs L94–118 | Colour-sector module in the gravity batch; `spread_tension` bag $4B\delta^p$ ($\delta=(1-f^2)/2$) equals `tube_tension_box`'s $B(1-f^2)^p$ only at $p=2$, so the $p=1$ control uses different normalisations in its two legs. |
| 07b-gravity | gravity.py | registry row | Registry `findings` empty and `exactness` None despite F64/F79/F106/F178 provenance and inventory rows #181–182; Laplacian is simple-cubic (D1 reference), not BCC; D-EM8 wave speed $c_g$ is a free argument. |
| 07b-gravity | gravity_emqg.py | gravity_emqg.py:L129–133, L41–92 | Default $c_0=0.5\neq c_\text{lat}=1/\sqrt3$; $G$ is a free knob, not $G_\text{lat}=1/(72\pi)$; index $1-2\phi/c^2$ matches the canonical $K=e^{-2\Phi/c^2}$ only at $O(\phi)$ and this parallel EMQG route (29 driven channels) declares no relation to F64/F178. `test_*` functions live in the kernel. |
| 07b-gravity | gravity_emergent.py | gravity_emergent.py:L50–59 | $G$ (SI and astro units), $\rho_\Lambda$, $\Omega_\Lambda$, $a_0$ literals; model's structural $G$ not used. |
| 07b-gravity | gravity_field_equation_uniqueness.py | gravity_field_equation_uniqueness.py:L559–560, L733, L542–608 | $g_*=10.749339$ and eV→J literals; "1.4e-76" hard-coded string; L4 is numerical (`"computed"`) under a registry `exact` tag; L5 concedes three of four signatures share the S4-reclassified F64/F106 premise. |
| 07b-gravity | gravity_four_derivative_locality.py | gravity_four_derivative_locality.py:L99–111 | BZ integral over the cubic box $[-\pi,\pi)^3$ (F57 proxy) with the single chiral branch, not the BCC zone / even law; magnitudes are fit-order artifacts (sign only survives); M4 jump at Λ=2.8 undiagnosed. |
| 07b-gravity | gravity_band_cutoff.py | gravity_band_cutoff.py:L178–285 | Grid-sweep legs C/E/F are tolerance checks (5e-4) under registry `exact`. |
| 07b-gravity | gravity_core_completeness.py | gravity_core_completeness.py:L566–570, L174 | Ceiling convention ($\mathcal K_\text{max}=1/a^4$ F183 vs $24/a^4$ F284) recorded as open decision. Metric function $B=1/g_{rr}$ here vs $B=g_{rr}$ in `interior_metric.py` — same letter, opposite meaning. |
| 07b-gravity | horizon_entanglement.py | horizon_entanglement.py:L467–488, L511–512, L615–626 | Registry `quantitative`, module says the per-cell result is `bracketed` (node-counting 48/24/12); `C_REQUIRED`, `ETA_WEYL`, `N_WEYL`, reference values are literals; local `_results_path` duplicates `particles._results_path`. |
| 07b-gravity | derive_chiral_liv_bound.py | derive_chiral_liv_bound.py:L558, L569 | C5 hard-codes `E_crab=1.12e6` GeV although `E_crab_photon_max_GeV` is imported; F246 $c_3$ re-typed. |
| 07b-gravity | derive_gap5_adjudication.py | derive_gap5_adjudication.py:L149–160, L331–366 | Registry `exact`, but A2/A3/C3 are numerical and B/C1/C2 assert hard-coded tables/booleans (cannot fail short of editing the table). |
| 07b-gravity | derive_velocity_addition.py | registry row | Registry findings list only F15; the code and inventory rows #45–48 are F22's. |
| 07b-gravity | graviton_collapse_threshold.py | graviton_collapse_threshold.py:L164–167 | Band top enters as typed $\pi\sqrt3/A$ (not recomputed from the dispersion); `chiral_double` control is a typed factor 2. |
| 07b-gravity | ns_eos.py | ns_eos.py:L28–58 | cgs $G$, $c$, $M_\odot$ and the Read et al. table are literals (D7); CODATA-GR, not the structural $G$. |
| 07c-qed | qed_uv_completion | qed_uv_completion.py (whole module) | Registry says exactness=exact, but U1–U4, U7, U8 and the engine-float U5 leg are quadratures with tolerances (quantitative). Only U5 closed form / mpmath and U9 are exact. |
| 07c-qed | qed_uv_completion | qed_uv_completion.py:L161–180 bz_factor() | U1–U4 "lattice" is the 4-D simple-cubic Wilson/Symanzik symbol 4sin²(k/2) (reference, D1), not the BCC walk. |
| 07c-qed | qed_uv_completion | qed_uv_completion.py:L555–558 | PV and dim-reg "closed forms" are typed expressions whose L-derivative is 1/16π² by construction. |
| 07c-qed | qed_casimir | qed_casimir.py:L99–125 | Headline "EXACT" Casimir law (C2) never calls pair_dispersion: it is the continuum ω=c \| k \| formula with c=c_lat. The lattice enters only in disp_1d('axis'), casimir_energy_3d_naive('pair') and pair_bending_coeff. |
| 07c-qed | qed_casimir | qed_casimir.py:L276 two_mode_squeezing() | n_b is set to the same list as n_a, so max \| n_a−n_b \| =0 by construction. |
| 07c-qed | qed_casimir | qed_casimir.py:L196–202 pair_bending_coeff() | Along ⟨100⟩ it returns −1.5e-4 instead of 0: arccos round-off (~3e-13) at k=1e-3 divided by c k³. The dispersion itself is linear to 3e-13 (spot-checked). |
| 07c-qed | qed_casimir_materials | qed_casimir_materials.py:L104 | β=6.6e-3 is a typed copy of the off-axis pair_bending_coeff (−6.57e-3, sign dropped). Module is dead_candidate/unreferenced. |
| 07c-qed | qed_bethe_log | qed_bethe_log.py:L88–96 | "The model's own hydrogen spectrum" is a generic nonrelativistic finite-difference Coulomb Hamiltonian, not the CA walk or F125 Dirac–Coulomb. Uses numpy directly (D8). |
| 07c-qed | qed_electron_self_energy | qed_electron_self_energy.py:L368–383 renormalized_propagator_symbolic() | On-shell subtraction is zero by construction (Σ_R = Σ minus its first two Taylor terms). L295–322 checks generic derivative-of-inverse identities, not the loop. |
| 07c-qed | qed_ir_bremsstrahlung | qed_ir_bremsstrahlung.py:L240, L340–346 | "c_lat cancels" is x/x=1; Bloch–Nordsieck virtual and real terms share a typed symbol f_IR, so the μ-cancellation holds by construction (neither is computed from F252/F258). |
| 07c-qed | qed_renormalization | qed_renormalization.py:L697–699, L375–424 | One-loop Z1 and Z2 are the same typed expression; the counterterm operator census is a hand-flagged lookup table. |
| 07c-qed | qed_schwinger_pair | qed_schwinger_pair.py:L23–25 docstring | w=2 Im L is called "the vacuum pair-creation probability per unit volume-time"; that is the vacuum-decay rate. The mean pair-production rate is the n=1 term (Nikishov). Code does not depend on this reading. |
| 07c-qed | qed_twoloop_ae | qed_twoloop_ae.py:L230, L276–278 | The A2 used for a_e/a_μ is the typed closed form, not the dispersive number; b1=1 is typed; beta_alpha is computed then overwritten (dead code). |
| 07c-qed | all qed_* | e.g. qed_vacuum_polarization.py:L72, qed_renormalization.py:L126, qed_casimir.py:L47, qed_casimir_materials.py:L33 | α is not in casim.constants: 137.035999177 is typed in 12 modules, and 137.035999 in qed_renormalization. Also unregistered: lepton masses, ħc (two forms), h, e, k_B, m_e(kg), F107 cell a=1.06638e-34 m (twice), g=9.81, ρ_Λ, and literature targets. |
| 07d-qi | qi_bell_tsirelson | qi_bell_tsirelson.py:L60-L63 | Hard-coded SI literals $\tau=2.05366\times10^{-43}$ s, $a=1.06638\times10^{-34}$ m, $\hbar$ [eV s] instead of `casim.constants` (F79/F107 ruler). |
| 07d-qi | qi_decoherence_floor | qi_decoherence_floor.py:L60-L64 | Same hard-coded SI literals ($\tau$, $a$, $\hbar$, $E_P$), unregistered duplicates of registry values. |
| 07d-qi | qi_decoherence_floor | qi_decoherence_floor.py:L105-L109 fundamental_dispersion_slope() | Tautological. It differentiates the literal $k/\sqrt3$, not the model's dispersion, and uses `math.sqrt(3.0)`, not `c_lat`. It backs exactness-inventory row 15c. |
| 07d-qi | qi_entanglement | qi_entanglement.py:L316-L331 hopping_amplitude() | Uses the 2-D square `dirac_step_2d_splitstep` (D1 reference, not BCC). $t$ is a sum of absolute values of 4 components, a heuristic amplitude; the derived $J$ and $\tau_\text{Bell}$ inherit this. |
| 07d-qi | qi_measurement | qi_measurement.py:L941-L961 coherence_exponent() | Fits the log of its own closed-form envelope, so the exponent $-2\,\text{dims}$ cannot fail. |
| 07d-qi | qi_measurement | qi_measurement.py:L1125-L1128 check_measurement() | M1f is `… and (coupling == "minimal")`: the control is hardwired, and the commutant does not depend on `coupling`. |
| 07d-qi | qi_born_gleason | qi_born_gleason.py:L903-L918 born_value_on_lattice_state() | B6a is true by construction: $[H_\text{int},\hat n]=0$ conserves the slot-0 population, which is $\lvert\langle v\vert\psi\rangle\rvert^2$. |
| 07d-qi | qi_born_gleason | qi_born_gleason.py:L253-L260 record_requires_environment() | `min_measurement_dim=4` and `gleason_dimension_premise_met=True` are literals. |
| 07d-qi | qi_born_gleason | qi_born_gleason.py:L322, L453, L522, L546, L614, L784 | D8: `np.random.default_rng` used directly instead of `casim.numerics.rng`. |
| 07d-qi | qi_born_nonabelian | qi_born_nonabelian.py:L417, L564 | G7's `d2_hole_reachable_in_a_charged_sector: False` is a literal, so the `G7-no-hole` check cannot fail. |
| 07d-qi | qi_born_nonabelian | qi_born_nonabelian.py:L483-L490 | G9 is vacuous: the record operator is $\mathbb 1$, so it only tests norm preservation. |
| 07d-qi | qi_born_nonabelian | qi_born_nonabelian.py:L527-L571 | The gate uses `assert`, so declared controls raise AssertionError instead of returning red rows. |
| 07d-qi | qi_cluster | qi_cluster.py:L493-L500 | The `mass=0` control appends C3b/C3d as literal `False`. The `locality=nonlocal` branch reuses the C1b control rather than perturbing C1. |
| 07d-qi | qi_cluster_asymptotic_series | qi_cluster_asymptotic_series.py:L146 | The theoretical power $p=3/2$ is a literal; the branch-point derivation is prose only (the module says PARTIAL). |
| 07d-qi | qi_gleason_regularity | qi_gleason_regularity.py:L199-L230 | H1 is tautological: the Gram of standard basis vectors is exactly $\mathbb 1$ for every $d\ge3$. D8: `np.random.default_rng` (L304, L343). |
| 07d-qi | qi_noise | registry | `reach=driven` with `n_reachable_from=0`, which is inconsistent. |
| 07d-qi | qi_so3_kinematic_gap | qi_so3_kinematic_gap.py:L255-L260 | K2 is degenerate. $\mathbf k$ lies along the rotation axis, so $R\mathbf k=\mathbf k$ (spot-checked $10^{-16}$); it does not test covariance under a generic rotation of $\mathbf k$. |
| 07d-qi | qi_spin_statistics | qi_spin_statistics.py:L408-L409 | The `jw_string=false` control is hardwired (`… if jw_string else False`); no string-less operators enter S4. |
| 07d-qi | qi_algorithms, qi_bell_tsirelson, qi_decoherence_floor, qi_entanglement, qi_noise, qi_qc_si | module imports | D8: bare `import numpy` in manifest-origin modules. |
| 07d-qi | qi_belt_trick, qi_born_gleason, qi_gleason_regularity, qi_measurement, qi_so3_kinematic_gap, qi_spin_statistics | registry `exactness=exact` | Registered exact, but most legs are float residuals with $10^{-9}$–$10^{-12}$ tolerances (machine). qi_so3 K2 and qi_measurement's recurrence are quantitative/fit. |
| 07e-running-thermo-astro | running_ir_coupling.py | running_ir_coupling.py:L66, L101–107 | Midpoint of the bracketed alpha_eff_star (0.376, 0.411) is formed and used as a result in the J3 range test; brackets have endpoints only |
| 07e-running-thermo-astro | running_gap_solve.py | running_gap_solve.py:L221 | `freeze_midpoint` = midpoint of a bracket, reported in output |
| 07e-running-thermo-astro | running_ir_coupling.py | running_ir_coupling.py:L81 | Dual-Meissner scale m_D set equal to sqrt(sigma)=0.42 GeV by assignment, not derived |
| 07e-running-thermo-astro | running_njl.py / running_gap_solve.py / running_scheme_constant.py / running_qstar_logmoment.py | running_njl.py:L178–181; running_gap_solve.py:L56–57; running_scheme_constant.py:L211–213; running_qstar_logmoment.py:L45–50 | Strong-sector gap kernel is the simple-cubic $\sum2(1-\cos k_i)$ (D1 reference), not BCC |
| 07e-running-thermo-astro | running_scheme_constant.py | running_scheme_constant.py:L208–235 | `ir_alpha_eff` duplicates the gap iteration of running_gap_solve.gap_solve (a separate copy that can drift) |
| 07e-running-thermo-astro | running_alpha_lattice_bound.py | running_alpha_lattice_bound.py:L316–596 | F334 hadronic-VMD section is live, but F334 is absent from the registry findings; ρ and ω both use M_OMEGA_DEFAULT as m_V (m_ρ never used) |
| 07e-running-thermo-astro | running_alpha_s.py | running_alpha_s.py:L85 | Imports `casim.engine.gauge.weak_wmu`, while CLAUDE.md's table names `casim.engine.gauge.wmu` (stale doc table) |
| 07e-running-thermo-astro | slowlight.py | slowlight.py:L171–179 | "Real (E,B) rotation": Φ(ω) is not odd, so E', B' come out complex after the inverse FFT; equality with the phase route holds by linearity only (chiral-transform hazard in name) |
| 07e-running-thermo-astro | unified.py | unified.py (whole module) | Higgs-field Φ–Dirac stepper conflicts with Core Design Decision 3 (Higgs-free); no supersession record |
| 07e-running-thermo-astro | unified.py | unified.py:L260, L250 | phi_energy always uses −μ² even for phase='symmetric' (+μ²); `grad_Phi` computed and unused |
| 07e-running-thermo-astro | vacuum_energy.py | vacuum_energy.py:L48–53 | Overshoot uses g_*=2 vs a G induced at 48 Weyl fields; S25 (F319/F408) flags this content mismatch and the negative fermionic zero-point sign. Module not named in S25 |
| 07e-running-thermo-astro | thermodynamics_gstar.py | thermodynamics_gstar.py:L672–693 | Plateau g_* table is hard-coded data, not computed; GS-12 tests the table against itself |
| 07e-running-thermo-astro | thermodynamics.py / thermodynamics_gstar.py | registry exactness=exact | Quadrature/tolerance legs (EoS measurement, g_* sums, BBN rerun) are quantitative; exact applies only to the closed forms |
| 07e-running-thermo-astro | qnm.py / raytrace.py / tolman.py / stellar.py / superconductivity.py / unified.py / slowlight.py / vacuum_energy.py / running_alpha_s.py / running_gap_solve.py / running_ir_coupling.py / running_njl.py / running_qstar_logmoment.py / running_scale_ratio.py / running_scheme_constant.py | registry.tsv | Manifest records carry no findings although the docstrings and exactness-inventory cite them (F183–F192, F173–F175, F210–F375, F144–F155) |
| 08a-forks | forks/gravity/gr3_forks_AB_extended.py | gr3_forks_AB_extended.py:L69–72, L82–86, L103 | Bug: helpers index with module-global L=192, not run(L_=…); `--L` ≠192 slices the wrong row. |
| 08a-forks | forks/gravity/gr3_forks_AB_extended.py | gr3_forks_AB_extended.py:L275 | Output dir SIM_ROOT/test-results resolves to src/casim/engine/forks/test-results (stale after C6; __main__-guarded). |
| 08a-forks | forks/gravity/gr3_fork_harness.py | gr3_fork_harness.py:L234–237 | Velocity-Verlet evaluates a2 with the old v for a velocity-dependent 1PN force. |
| 08a-forks | forks/gravity/gr3_fork_harness.py | gr3_fork_harness.py:L196, L217–223 | GR-4 hard-codes Schwarzschild-form PN coefficients from (α_A, α_B); all forks' metric() return the same pair except C ⇒ integrates no fork's own spacetime (S16). |
| 08a-forks | forks/gravity/gr_fork_E_tensor.py | gr_fork_E_tensor.py:L4 (and gr_tensor_stub.py:L4, gr_fork_F64 L31–32) | Cites "Finding 19"; F19 is now the tick area-vs-volume finding (deprecated). Stale numbering. |
| 08a-forks | forks/__init__.py | forks/__init__.py:L1–24 | Package docstring describes only the GR-3 trichotomy; package holds six sectors. |
| 08a-forks | forks/gravity/dirac_gravity_fork.py | L178 vs L212 | Two opposite mix-angle sign conventions in one file (massive: θ=−δm·dt/2; curved: θ=+√A·m·dt/2); L160–168 records that particles.dirac.dirac_step_2d_varm_splitstep has the wrong relative sign (live item). |
| 08a-forks | forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py | L177–178, L191–197 | Q3a circular: c_lat defined as √stiffness, so stiffness/c_lat² = 1 identically (inventory #57 records it as a machine-precision result). |
| 08a-forks | forks/gravity/gr_fork_F60_channel_reconciliation.py | L45–47; L67–125 | (A) same circularity as F58 Q3a; all physics results computed only in __main__ (no callable). |
| 08a-forks | forks/gravity/gr_fork_F79_structural_G.py | L204–209 s4_channel_gap() | S4 fits exponents of arrays constructed as c² and 0.08/c — restates F60, computes neither channel. |
| 08a-forks | forks/gravity/gr_fork_F59_induced_eh_prefactor.py | L197–199 vs docstring L14–19 | Docstring presents the TT stress-bubble q² coefficient C as the induced 1/(16πG); __main__ labels it a negative control and the assembly never uses it. |
| 08a-forks | forks/gravity/gr_fork_F59/F60/F61/F63 | F59 L209, F60 L123, F61 L158, F63 L208 | __main__ writes *_results.json into the source directory (OUT = dirname(__file__)), not via _results_path. |
| 08a-forks | forks/gravity/gr_fork_F56_einstein_coupling_derivation.py | L151–159 vs F59 L77 / F60 L58 | Sakharov weight convention ∫1/ω (F56, F58) vs ∫1/(2ω) (F59, F60, F61) differs by 2 across the chain. |
| 08a-forks | forks/gravity/gr_fork_F57_induced_eh_from_backreaction.py | L92 static_polarization() | "Full BZ" is the Cartesian cube [−π,π)³, not the BCC Brillouin zone (dispersion argument is k/√3). |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | Cayley-solver tests L835, L899, L1676 | S10-F271: lattice.curved._half_step_dH ordering/first-order defect present in every F64-fork variable-c result; not fixed here. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L731–732 test_demD2a | Uses gravity_dirac_step_massive, which reads only √A — the dielectric B=1/A is never used, so D-EM-D2a ≡ F62 D2a. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L791, L1021 | Kinetic rate passed as c0·r_kin (D-EM-D2b, D-EM4) vs √A in F62 D2b — undocumented convention change. |
| 08a-forks | forks/gravity/gr_fork_F64_em_connection.py | L1761–1765 test_dem10 | 4π check uses the continuum k² Poisson symbol, not the exact stencil −4Σsin²(k_i/2) of the production F106 identity. |
| 08a-forks | forks/gravity/gr_fork_F63_spin_torsion_estimate.py | L91–105 | ℓP²/a³ → (ℓP/a)² step replaces m by the 1/a cutoff by fiat; r_rest = r_cutoff/m mixes units. |
| 08b-forks | gr_fork_F216_massive_spin2 | gr_fork_F216_massive_spin2.py:L247–L255 | Runs the whole battery AND writes test-results/F216_massive_spin2.json at import (no __main__ guard; CLAUDE.md §5) |
| 08b-forks | gr_fork_F223_spin2_binding_relic | gr_fork_F223_spin2_binding_relic.py:L297–L304 | Import-time physics + JSON write (no __main__ guard) |
| 08b-forks | gr_fork_F228_geon_production_stability | gr_fork_F228_geon_production_stability.py:L402–L409 | Import-time physics (incl. 400k-step RK4) + JSON write (no __main__ guard) |
| 08b-forks | gr_fork_F238_geon_relic_abundance | gr_fork_F238_geon_relic_abundance.py:L337–L344 | Import-time physics + JSON write (no __main__ guard) |
| 08b-forks | derive_weight_as_phase | derive_weight_as_phase.py:L28–L269, L287 | Derivation runs and prints at import (the write is guarded) |
| 08b-forks | gr_fork_F199_amplitude_mode_stability | registry + filename | Finding-number collision resolved: topic is now F199b (finding-numbers.yaml); registry findings=F199 is stale |
| 08b-forks | gr_fork_F200_sterile_neutrino_dm | registry + filename | Finding-number collision resolved by moving the topic to F266; registry findings=F200 is stale |
| 08b-forks | gr_fork_F180_gw_speed | gr_fork_F180_gw_speed.py:L213, L238 | Check D assigns slope_residual=0.0 (not computed); check E's speed is the imported c_lat put in the stencil (a leapfrog check, not a derivation) |
| 08b-forks | gr_fork_F216_massive_spin2 | gr_fork_F216_massive_spin2.py:L150 | B1 posits Π=A·Q² then "verifies" Π(0)=0 (circular); dead dof expression L80 overwritten at L82 |
| 08b-forks | gr_fork_F248_tt_graviton_bcc | gr_fork_F248_tt_graviton_bcc.py:L320, L396 | Birefringence check abs(Om-Om) is tautologically 0; check D applies the same density to both polarisations (speed difference 0 by construction) |
| 08b-forks | gr_fork_F202_leptogenesis_sakharov | gr_fork_F202_leptogenesis_sakharov.py:L63–L80 | All Sakharov "met" flags hard-coded True; nothing evaluated |
| 08b-forks | gr_fork_F203_dark_sector_falsifiers | gr_fork_F203_dark_sector_falsifiers.py:L108, L163, L210, L252 | Test statuses are hard-coded strings, not derived from the computed margins |
| 08b-forks | gr_fork_F193_ontic_vacuum | gr_fork_F193_ontic_vacuum.py:L106, L134, L163 | beable_energy_density returns J (no 1/a³) stored as "_J_per_m3"; dead assignment L163 |
| 08b-forks | gr_fork_F196_dilution_exponent | gr_fork_F196_dilution_exponent.py:L69 | RHO_VAC=3.456e111 is a hard-coded copy of the F164 output (unregistered literal) |
| 08b-forks | gr_fork_F197_first_excitation_dark | gr_fork_F197_first_excitation_dark.py:L216 | λ6=0.05 illustrative; conflicts with the registered λ6=0.243 (key decision 7/F234); also used in F198 L119, F199 L101 |
| 08b-forks | gr_fork_F201_kev_from_eg_texture | gr_fork_F201_kev_from_eg_texture.py:L35 | DELTA_E_DEG=12.7328 unregistered literal near δ*=2/9 rad=12.7324° (founding constant not imported) |
| 08b-forks | gr_fork_F228_geon_production_stability | gr_fork_F228_geon_production_stability.py:L273 | Integrator gate is rel<5e-3 while exactness-inventory row 256 quotes 1e-12; inventory rows 255–257 are labelled "F226" |
| 08b-forks | gr_fork_F238_geon_relic_abundance | gr_fork_F238_geon_relic_abundance.py:L262–L273 | Check S6 is a filesystem keyword search (result depends on repo state, not physics); A&S erfc has ~1% relative error in the inverted tail |
| 08b-forks | dm_fork_F205_sterile_qke_boltzmann | dm_fork_F205_sterile_qke_boltzmann.py:L220, L231, L365, L373 | Module global MEAN_EPS_NRP_REF mutated by run() and by F237 (comment says "filled at import"); verdict hard-codes "2.5 dex" |
| 08b-forks | dm_fork_F237_kev_sterile_resolution | dm_fork_F237_kev_sterile_resolution.py:L173, L130 | X-ray slope is tautological (log_sin2 = log10 S fits the input +1); me_cold=1.57 hard-coded copy of an F205 output |
| 08b-forks | dm_fork_F364_baryogenesis_boltzmann | dm_fork_F364_baryogenesis_boltzmann.py:L72–L73, L98 | Direct scipy imports (D8 deviation, acknowledged); status 'live' inside forks/; δν=134.86° literal gives M1=5.99 keV, not the 5.6 keV used by F203/F205/F237; findings-index says "no test record" but tests/registry/forks.yaml:756 has one |
| 08b-forks | u1_link_unitarity_forks | registry | status 'live' (spine) although it sits in forks/ |
| 08b-forks | lgt_fork_A_mc | registry | findings field empty; natural finding F94 |
| 08b-forks | complex_mass_fork | registry | findings field empty (content is F27); 2-D square reference lattice (D1), sys.path insert L88–L90 |
| 08b-forks | koide_pseudomass_minimal | koide_pseudomass_minimal.py:L278–L283 | ms_profile temporarily mutates the shared QUARK_MASSES_MEV dict imported from koide_pseudomass_fork |
| 08b-forks | curl_fork_harness / smearing_fork_harness | curl_fork_harness.py:L20; smearing_fork_harness.py:L57, L85 | Stale run paths "python3 forks/…"; the 1/√6 baseline is attributed to Finding 2 in one file and Finding 21 in the other |
| 09-shims | lattice/backend.py | backend.py:L11-12 | Docstring says file "is deleted at C9"; it still exists post-C9 and is imported by gate test test_backend.py and chiral_core.register() |
| 09-shims | lattice/chiral_core.py | chiral_core.py:L81-101 | cmul/su2_apply duplicated verbatim in casim.numerics.chiral rather than imported; direct `import numpy` (D8) |
| 09-shims | lattice/chiral_core.py | chiral_core.py:L2 | Cites F134; finding file is F134b-phase4-chiral-blockspin-completion.md (F134 = unified real-space integration) |
| 09-shims | particles/spec.py | spec.py:L163-166 | SU(2)²Y trace has stray 1/2; SU(3)³ "trace" is triplet-minus-antitriplet count, not a cubic-anomaly coefficient (zero result unaffected) |
| 09-shims | particles/channel.py | channel.py:L1434-1438 _coarse_well() | src_rms_cells=min(rms_c, 0.0) is always ≤0 → always point source; rms_c dead (likely meant max) |
| 09-shims | particles/channel.py | channel.py:L343-345, L646-648 vs L347-348, L419 | U(1) coupling inconsistent: two-sided Stueckelberg wrap on most paths, one-sided e^{-iqα} with ACCUMULATED α re-applied each tick on scalar-confined Dirac and quark_dirac paths |
| 09-shims | particles/channel.py | channel.py:L987, L999, L1872, L1045 | Photon kick E+=gJdt (opposite sign to usual Ampère −J), B not kicked, no Gauss constraint; Coulomb normalisation differs (∇²φ_em=−g_cρ vs ∇²φ=4πkρ in element_atom); gluon A+=E without dt |
| 09-shims | particles/channel.py | channel.py:L341 vs L637 | ParticleChannel omits confine.dt in varm Dirac step; quark_dirac passes it |
| 09-shims | particles/channel.py | channel.py:L339, L1411 etc. | Cites "F135" for scalar confinement; file is F135b-realspace-scalar-confinement.md (F135 = block-spin wavepacket) |
| 09-shims | particles/channel.py | channel.py:L48 | Direct numpy use (einsum, vdot, gradient, interp) outside casim.numerics (D8) |
| 09-shims | fields/electroweak.py | electroweak.py:L36-40 | _f26_rotation_step / w_propagation_step_chiral in __all__ but undefined if weak_wmu import fails; CLAUDE.md names home gauge.wmu, code uses gauge.weak_wmu |
| 09-shims | fields/strong.py | strong.py:L28 | ca_dual_gl_backreaction (colour dual-GL, F139) re-exported from the gravity-prefixed interactions.gravity_backreaction — misleading name |

## Verification

*Independent pass, 2026-09-29, by a subagent that had not seen the map being written. It sampled rows across all 17 section files, weighted toward `gauge/` and `interactions/`, checked each against the cited line, and ran a numeric comparison where cheap. Both non-PASS rows have been corrected in the map.*

**Result: 68 rows sampled — 66 PASS, 1 CITATION, 1 MINOR, 0 FAIL. PASS 97.1 %; PASS+MINOR 98.5 %. Sixteen numeric checks, all agreeing (most to machine precision). Fixed: 05b `cooling.py` #5 citation (L233 → L217–231); 08b `koide_pseudomass_minimal` #1 (the $i\phi$ term applies to one optional slot, not the whole sum).**

The verifier also independently confirmed priority item 2 (the stale-staple checkerboard in `colour_condensate.u1_metropolis_3d`, L396–406), as a code issue, not a map error.

### Sample

2026-09-29 - independent verifier. Sample drawn pseudo-randomly: evenly spaced rows with a seeded random offset per file (seed 20260929), weighted 4/file for 05a–05c and 07a–07e and 2–3/file elsewhere. Three pure-plumbing hits were swapped for the nearest physics rows: 02 `memory_estimate` became `cmul` and `per_cell_residual`, and 04 `graph.build_graph` and the `tier3` table row became `channels` #14 and `coupled` #1. Two extra G/sin²θ rows were added to 01. A second seeded draw (seed 7) added one more row per heavy file. The duplicate 07c draw was replaced with `qed_renormalization` #1. Every citation was opened at the cited line, with helpers and constants followed. No `__main__` was run. The four forbidden gr_fork modules were not imported.

| # | Map file | Row (module #n) | Cited where | Verdict | Numeric check? | Note |
|---|---|---|---|---|---|---|
| 1 | 01-constants | geometry #9 `E_LV_e_sup_min_GeV` | geometry.py:L340 | PASS | — | 9.4e25 GeV, external, F327 (register at L338) |
| 2 | 01-constants | strong #10 `Lambda_QCD_nf3_GeV` | strong.py:L237 | PASS | — | 0.347, quantitative, F151 |
| 3 | 01-constants | measured #3 curl_fork_cubic C_LAT | measured.py:L69 | PASS | — | value 1.0, kind measured; fork L48 C_LAT=1.0 |
| 4 | 01-constants | electroweak #1 `sin2_thetaW_uv` | electroweak.py:L56 | PASS | — | Fraction(1,4) = (1/3)/(4/3) |
| 5 | 01-constants | gravity #1 `G_LATTICE` | gravity.py:L18 | PASS | hand | a²c³/(8π√3ħ) at c=1/√3 → 1/(72π) = c⁴/(8π) ✓ |
| 6 | 02-numerics | chiral #1 cmul | chiral.py:L31 | PASS | — | return is at L30 (±1) |
| 7 | 02-numerics | lazy #1 per-cell residual | lazy.py:L138-139 | PASS | — | Σ(d_r²+d_i²), sqrt |
| 8 | 02-numerics | lazy #3 proper time | lazy.py:L88 | PASS | — | N·τ₀ |
| 9 | 03-lattice | blockspin_baryon #2 hyperangular | blockspin_baryon.py:L63–65 | PASS | hand | Γ(3)/(√πΓ(7/2)) = 16/(15π); 15/4 = 5·3/4 |
| 10 | 03-lattice | dimensionality #1 Bloch vector per d | dimensionality.py:L188–209 | PASS | — | d=2 (s_xc_y, c_xs_y, s_xs_y), d=1 (0,0,sin k), d=3 equals bcc #2 (sign-corrected n_y) |
| 11 | 03-lattice | time_signature #7 Pell | time_signature.py:L577–588 | PASS | — | `_update_pair` = (u, −i); deg b = 0 ⇒ fundamental |
| 12 | 04-core | channel #1 field_energy | channel.py:L43 | PASS | — | ½(ΣE²+ΣB²) |
| 13 | 04-core | channels #14 K rebuild | channels.py:L376 | PASS | — | K = exp(−2φ/c²) |
| 14 | 04-core | coupled #1 su2_expmap | coupled.py:L51-57 | PASS | yes (2e-16 vs scipy expm) | U_a, U_b and matrix embedding verified |
| 15 | 05a | bcc_action #4 Wilson density | bcc_action.py:L250-252 | PASS | — | 1 − Re tr P/N, BCC-site mask, 6 orientations |
| 16 | 05a | bilinear #11 δv_φ, −k/18 | bilinear.py:L2089-2091, L2151-2153 | PASS | yes | code at k=0.05 gives −2.793e-3; independent 2ω⁺(k/2) along (111) gives the same; −k/18 = −2.778e-3 |
| 17 | 05a | charge_coupling #6 exact curl step | charge_coupling.py:L267-288 | PASS | — | G sign, P_T, sinθ Ĝ, −dt J all match |
| 18 | 05a | colour_condensate #12 U(1) Metropolis | colour_condensate.py:L400-406, L373-379 | PASS | — | ΔS and staple convention match. Code note (not a map error): staples are computed once per μ before both checkerboard halves, so the second half uses stale staples (the same-μ links at n±ν̂ are opposite parity). This is a detailed-balance issue in the code. |
| 19 | 05a | bilinear #13 rotation vs curl | bilinear.py:L1615-1622, L2218-2222 | PASS | — | E + i(2n)×B |
| 20 | 05b | cooling #5 staple sum | cooling.py:L233 | CITATION | — | equation matches the code. L233 is the `return` line; the formulas are at L217-231 (def at L200) |
| 21 | 05b | derive_gauge_boson_masses #9 Δρ_t, Δr | L292, L298–299 | PASS | yes | Δρ_t = 0.0093323, same as the independent formula |
| 22 | 05b | derive_su3_structure #12 f^{abc} | L761–763 | PASS | hand | −2i Tr([T^a,T^b]T^c) with Tr(TT) = δ/2 |
| 23 | 05b | gluon #3 2D step | gluon.py:L134–140 | PASS | — | Ω = 2·arccos(c_xc_y) at k/2, c_i = cos(k_i/√2) (via bilinear_2d → core_exact) |
| 24 | 05b | derive_bilinear_so3 #5 | L245–249 | PASS | — | law = 2·n̂_y² |
| 25 | 05c | photon #3 photon_step_spectral | photon.py:L105–106 | PASS | yes | identical to `_f26_rotation_step` to 1.3e-15 |
| 26 | 05c | propagator #2 D_k | propagator.py:L203–209 | PASS | — | n = √(1−m²), im = i·m, A′ = A† (L178-181) |
| 27 | 05c | weak_wmu #9 even law | weak_wmu.py:L688–695 | PASS | — | ω⁺(k/2)+ω⁻(k/2), rotation signs ✓ |
| 28 | 05c | weak_z #4 per-species J^Z | weak_z.py:L331–334 | PASS | — | |
| 29 | 05c | weak_wmu #4 covariant Weyl step | weak_wmu.py:L331–339 | PASS | — | U_eff applied, then spectral BCC step per flavour |
| 30 | 06a | atom #7 κ | atom.py:L169 | PASS | — | |
| 31 | 06a | baryon #8 V(R) = σR | baryon.py:L318-319 | PASS | — | |
| 32 | 06a | derive_lepton_shape_precision_floor #1 | L73-76 | PASS | yes | (206.7703, 3477.473) at δ=2/9, η²=½, same as the independent value |
| 33 | 06b | dirac #15 ⟨T₃⟩ | dirac.py:L998 | PASS | — | L998 is the return line (def L985); within tolerance |
| 34 | 06b | higgs #6 dispersions | higgs.py:L259, L270, L274 | PASS | — | m_h² = 2μ², radial √(κ²+m_h²), Goldstone κ |
| 35 | 06b | nuclear #6 OPEP Y, T | nuclear.py:L294, L298 | PASS | — | x = r/comp (L339) |
| 36 | 07a | blackhole #7 Kerr | blackhole.py:L136-139 | PASS | yes | a=0.6: r± = 1.8/0.2, Ω_H = 1/6 ✓ |
| 37 | 07a | cosmology #6 RK4 + fit | cosmology.py:L100-107, L115 | PASS | — | |
| 38 | 07a | cosmology_holographic #1 HC tilt | L129-140 | PASS | yes | n_s−1 = −0.022296, dln/dlnq = −0.67538, running +0.015058. The exactness cell quotes "0.6754" without its sign (cosmetic, not counted) |
| 39 | 07a | darkmatter #1 v_disk | darkmatter.py:L37-38 | PASS | yes | 160.0504 km/s at r=5, same as the independent value |
| 40 | 07a | blackhole #4 t_evap | blackhole.py:L98 | PASS | — | 5120πG²M³/(ħc⁴) |
| 41 | 07b | derive_boost_covariance #12 | L569–623 | PASS | — | all four brackets and the K→K+f invariance match the sympy asserts |
| 42 | 07b | derive_velocity_addition #7 | L592–605 | PASS | — | the code uses c² = ½ (1-D walk); the row does not state c², which is acceptable |
| 43 | 07b | gravity_core_completeness #3 | L233–238 | PASS | — | B = 1−δ (with A = 1), lim r⁴K ≠ 0 |
| 44 | 07b | horizon_entanglement #9 | L481–488, L511–537 | PASS | yes | ratio(c=0.1) = 0.441063, same as 24c/(π√3) |
| 45 | 07b | gravity_backreaction #10 meanfield_bag | L248–255 | PASS | — | ρ = L2 octet norm (the code docstring says Σ\|J\|; the map follows the code) |
| 46 | 07c | qed_bethe_log #1 H_l | L89, L94 | PASS | — | |
| 47 | 07c | qed_euler_heisenberg #1 | L114–120 | PASS | — | −1/45, −1/45, −1/9 |
| 48 | 07c | qed_schwinger_pair #1 | L82–87 | PASS | hand | −π·Res = (eE)²/(8π³n²)e^{−nπm²/eE} ✓ |
| 49 | 07c | qed_uv_completion #1 bz_factor | L171–180 | PASS | yes | Wilson D(t) = e^{−2t}I₀(2t) to all digits at t = 0.3 and 2 |
| 50 | 07c | qed_renormalization #1 superficial degree | L193–211 | PASS | — | |
| 51 | 07d | qi_born_gleason #18 | L930-941 | PASS | — | |
| 52 | 07d | qi_decoherence_floor #5 LR cone | L141-155 | PASS | — | θ = π/16 default, Néel start, cone 4t |
| 53 | 07d | qi_measurement #11 native gate vs SWAP | L640-646 | PASS | — | θ = π/8 default |
| 54 | 07d | qi_spin_statistics #8 | L346-350; L433-434 | PASS | — | kron(R2π, R2π) = +1 |
| 55 | 07d | qi_bell_tsirelson #4 | L118 | PASS | — | U_exch(π/8) on \|01⟩ |
| 56 | 07e | qnm #4 ringdown | qnm.py:L84–86 | PASS | — | |
| 57 | 07e | run_q3_omega_degeneracy #1 | L31 | PASS | yes | 25.8769 (the map says 25.88) |
| 58 | 07e | running_scale_ratio #1 | L80–94 | PASS | yes | f_π/M = 0.297491 = 2√(N_cK₀) |
| 59 | 07e | thermodynamics_interacting #1 build_H | L175–201 | PASS | — | c = (L−1)/2 |
| 60 | 07e | running_ir_coupling #1 α_eff* bracket | L48–49 | PASS | yes | endpoints 0.376 / 0.411 |
| 61 | 08a | gr3_fork_C #1 c_γ | L47 | PASS | — | |
| 62 | 08a | gr_fork_F56 #1 ξ | L78–79 | PASS | — | |
| 63 | 08a | gr_fork_F64 #1 _maps | L106–124 | PASS | — | |
| 64 | 08b | gr_fork_F202 #1 CP phases | L53–54 | PASS | — | |
| 65 | 08b | hypercharge_fork #1 Majorana step | L163–164 | PASS | — | |
| 66 | 08b | koide_pseudomass_minimal #1 amplitude_matrix | L140–147 | MINOR | — | the T₁g term is written as if inside the Σ over a<b. The code applies iφ to one optional slot `_OFF[t1g_index]` |
| 67 | 09-shims | particles/channel #4 r_rms | channel.py:L1205, L1211 | PASS | — | |
| 68 | 09-shims | particles/channel #34 coarse electron | channel.py:L1474 | PASS | — | multigrid.schrodinger_step is Strang with continuum k² (2π fftfreq/a) |
