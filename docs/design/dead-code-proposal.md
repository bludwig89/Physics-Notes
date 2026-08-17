# Dead-code proposal

*Generated 2026-07-31 23:03 UTC by `tools/find_dead_code.py` (roadmap C0.2) at graph `5b5c307`. **Do not edit by hand** — regenerate.*

> **This is a proposal, not a verdict.** Nothing here has been applied.
> A human accepts a line by moving it into `dead_symbols` in
> `docs/design/module-migration-manifest.yaml`; only accepted lines are
> stripped by the C0.4 migration tool. The three signals below are
> independent and must not be summed — P0.4 found that of 14 files an
> audit called superseded, exactly **one** was superseded wholesale.

| Signal | Count |
|---|---|
| 1. unreferenced files | 19 |
| 1. unreferenced symbols **(proposed)** | 95 |
| 1. module-private helpers (used internally — NOT dead) | 941 |
| 1. ambiguous (name defined in >1 module — NOT dead) | 586 |
| 2. ledger-named paths | 30 |
| 2. candidate dead symbols (from `scope:`) | 2 |
| 2. PROTECTED symbols (from `retained:`) | 2 |
| 3. modules reachable only from tombstoned tests | 0 |

---

## Signal 1 — structurally unreachable

### Files nothing imports, with no `__main__`

| Path | Role | Lines | Why | Ledger |
|---|---|---|---|---|
| `src/casim/engine/forks/__init__.py` | fork | 26 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/darkmatter/__init__.py` | fork | 11 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/electroweak/__init__.py` | fork | 11 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gauge/curl_fork_baseline_bcc.py` | fork | 42 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gauge/curl_fork_cubic.py` | fork | 95 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/__init__.py` | fork | 11 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr3_fork_A_phase_tick.py` | fork | 75 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr3_fork_B_anisotropic.py` | fork | 84 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr3_fork_C_restricted_c.py` | fork | 74 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr3_fork_baseline.py` | fork | 55 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr_fork_F216_massive_spin2.py` | fork | 256 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr_fork_F223_spin2_binding_relic.py` | fork | 305 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr_fork_F228_geon_production_stability.py` | fork | 410 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/gravity/gr_fork_F238_geon_relic_abundance.py` | fork | 345 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/lattice/__init__.py` | fork | 11 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/particles/__init__.py` | fork | 11 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/forks/particles/complex_mass_fork.py` | fork | 550 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/interactions/qed_casimir_materials.py` | kernel | 108 | nothing imports it and it has no __main__ | — |
| `src/casim/engine/particles/_results_path.py` | kernel | 60 | nothing imports it and it has no __main__ | — |

Two entries here are the roadmap's own worked example. `derive_generator_norm_from_F118.py` has no `__main__` and nothing imports it, so it lands in this table — and it must **not** be deleted: P0.4 gave it a `PRE-DECISION FRAMING` banner because its Schur-isotropy proof *is* the F255 content, and its circularity argument is precisely *why* the F234 arrow was reversed. It migrates with the banner intact (roadmap C5). This is what "a signal is not a verdict" looks like in practice.

### Top-level symbols nothing in the tree references

**95 proposed.** A separate **941** are referenced inside their own module and are therefore private helpers, not dead code — removing one means removing its callers too, which is a refactor. Those are in the JSON under `module_private` and are NOT proposed.

| Path | Symbol |
|---|---|
| `src/casim/engine/core/_viz_legacy.py` | `save_scalar_instability` |
| `src/casim/engine/core/_viz_live_display.py` | `on_key` |
| `src/casim/engine/core/coupled.py` | `BetaDecayChannel` |
| `src/casim/engine/core/coupled.py` | `ChargePhotonChannel` |
| `src/casim/engine/core/coupled.py` | `FermionDoubletChannel` |
| `src/casim/engine/core/coupled.py` | `WSourcedChannel` |
| `src/casim/engine/core/entanglement_register.py` | `CircuitReadoutObserver` |
| `src/casim/engine/core/entanglement_register.py` | `EntanglementEntropyObserver` |
| `src/casim/engine/core/entanglement_register.py` | `ErrorCorrectionObserver` |
| `src/casim/engine/core/entanglement_register.py` | `FermionAlgorithmObserver` |
| `src/casim/engine/core/entanglement_register.py` | `FermionEntanglementObserver` |
| `src/casim/engine/core/lpt_generator.py` | `four_gluon` |
| `src/casim/engine/core/lpt_generator.py` | `gluon_propagator_inverse_full` |
| `src/casim/engine/core/lpt_generator.py` | `three_gluon` |
| `src/casim/engine/core/observers.py` | `BeamTrack` |
| `src/casim/engine/core/observers.py` | `EnergyTrace` |
| `src/casim/engine/core/observers.py` | `FieldDump` |
| `src/casim/engine/core/observers.py` | `FieldSnapshot` |
| `src/casim/engine/core/observers.py` | `UnitarityResidual` |
| `src/casim/engine/core/spectral_matter.py` | `NJLMesonChannel` |
| `src/casim/engine/core/spectral_matter.py` | `NJLNucleonChannel` |
| `src/casim/engine/core/spectral_matter.py` | `StringTensionFpiChannel` |
| `src/casim/engine/core/tier3.py` | `DynamicalRefractionChannel` |
| `src/casim/engine/core/tier3.py` | `GaugeMonteCarloChannel` |
| `src/casim/engine/forks/darkmatter/dm_fork_F205_sterile_qke_boltzmann.py` | `thermal_equiv_mass_keV` |
| `src/casim/engine/forks/gravity/dirac_gravity_fork.py` | `rindler_background` |
| `src/casim/engine/forks/gravity/gr_fork_F198_angular_misalignment.py` | `H_rad` |
| `src/casim/engine/forks/gravity/gr_fork_F199_amplitude_mode_stability.py` | `f73_composite_mass` |
| `src/casim/engine/forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py` | `clat_from_symbol` |
| `src/casim/engine/forks/gravity/gr_fork_F59_induced_eh_prefactor.py` | `cfactor` |
| `src/casim/engine/forks/gravity/gr_fork_F64_em_connection.py` | `dielectric_rindler_background` |
| `src/casim/engine/gauge/bilinear.py` | `photon_ang_mom_eigenstate` |
| `src/casim/engine/gauge/charge_coupling.py` | `gauss_residual` |
| `src/casim/engine/gauge/charge_coupling.py` | `maxwell_curl_step_euler` |
| `src/casim/engine/gauge/colour_dielectric.py` | `gluon_dielectric_evolve_bcc` |
| `src/casim/engine/gauge/colour_dielectric.py` | `refractive_factor` |
| `src/casim/engine/gauge/cooling.py` | `near_identity_links_2d` |
| `src/casim/engine/gauge/gluon.py` | `_plaquette_field_strength_su3_composite_sc` |
| `src/casim/engine/gauge/gluon.py` | `gluon_rotation_step_spectral_bcc_chiral` |
| `src/casim/engine/gauge/gluon.py` | `wilson_loop_area_law_data` |
| `src/casim/engine/gauge/link_hamiltonian.py` | `plaquette_cos_expect` |
| `src/casim/engine/gauge/lpt_selfenergy.py` | `gluon_finite_constant` |
| `src/casim/engine/gauge/lpt_wilson.py` | `qstar_validation_highres` |
| `src/casim/engine/gauge/lpt_wilson_selfenergy.py` | `lambda_ratio_from_finite` |
| `src/casim/engine/gauge/lpt_wilson_selfenergy.py` | `self_energy_loops` |
| `src/casim/engine/gauge/lpt_wilson_selfenergy.py` | `transverse_scalar` |
| `src/casim/engine/gauge/propagator.py` | `_safe_sinc` |
| `src/casim/engine/gauge/propagator.py` | `make_propagator` |
| `src/casim/engine/gauge/strong.py` | `_quark_color_matrix` |
| `src/casim/engine/gauge/strong.py` | `parallel_transport` |
| `src/casim/engine/gauge/strong.py` | `w_link_unitarity_residual_2d` |
| `src/casim/engine/gauge/su3_ladder.py` | `fuse_Fbar` |
| `src/casim/engine/gauge/su3_ladder.py` | `su3_rotor_strong_coupling_slope` |
| `src/casim/engine/gauge/weak.py` | `weak_norm` |
| `src/casim/engine/gauge/weak_wmu.py` | `_plaquette_field_strength_composite_sc` |
| `src/casim/engine/gauge/weak_wmu.py` | `make_hypercharge_link_field` |
| `src/casim/engine/gauge/weak_wmu.py` | `measure_w_dispersion` |
| `src/casim/engine/interactions/blackhole.py` | `kretschmann_schwarzschild` |
| `src/casim/engine/interactions/cosmology.py` | `omitted_source_fraction` |
| `src/casim/engine/interactions/interior_metric.py` | `dielectric_field` |
| `src/casim/engine/interactions/interior_metric.py` | `metric_AB_areal` |
| `src/casim/engine/interactions/qed_casimir.py` | `fit_coeff_3d_naive` |
| `src/casim/engine/interactions/qed_casimir_materials.py` | `lattice_fractional_deviation` |
| `src/casim/engine/interactions/qed_casimir_materials.py` | `sphere_plate_force_realistic` |
| `src/casim/engine/interactions/qed_ir_bremsstrahlung.py` | `_four_dot` |
| `src/casim/engine/interactions/qed_scattering.py` | `v_spinor_direct` |
| `src/casim/engine/interactions/qed_twoloop_ae.py` | `vp_spectral` |
| `src/casim/engine/interactions/qi_bell_tsirelson.py` | `sigma_ndir` |
| `src/casim/engine/interactions/qi_noise.py` | `bitflip_uncorrected_fidelity` |
| `src/casim/engine/interactions/qi_noise.py` | `embed2` |
| `src/casim/engine/interactions/qi_qc_si.py` | `leakage_leading` |
| `src/casim/engine/interactions/slowlight.py` | `phase_velocity` |
| `src/casim/engine/interactions/stellar.py` | `TwoPiecePolytrope` |
| `src/casim/engine/interactions/superconductivity.py` | `_einstein_lambda_matrix` |
| `src/casim/engine/interactions/superconductivity.py` | `bohm_staver_cs` |
| `src/casim/engine/interactions/superconductivity.py` | `frohlich_kernel` |
| `src/casim/engine/interactions/superconductivity.py` | `gap_ratio_dynamic` |
| `src/casim/engine/interactions/superconductivity.py` | `meissner_profile` |
| `src/casim/engine/interactions/unified.py` | `fermion_norm` |
| `src/casim/engine/interactions/unified.py` | `phi_norm` |
| `src/casim/engine/interactions/unified.py` | `setup_higgs_perturbation` |
| `src/casim/engine/lattice/core.py` | `verify_dispersion_2d` |
| `src/casim/engine/lattice/core.py` | `verify_dispersion_3d` |
| `src/casim/engine/lattice/curved.py` | `weyl_step_2d_varc_cayley` |
| `src/casim/engine/lattice/geometry.py` | `next_good_fft_size` |
| `src/casim/engine/lattice/multigrid.py` | `rms_about_center` |
| `src/casim/engine/particles/baryon.py` | `proton_colour_field` |
| `src/casim/engine/particles/dirac.py` | `dirac_step_2d_varm_splitstep` |
| `src/casim/engine/particles/higgs.py` | `kg_nonlinear_kick` |
| `src/casim/engine/particles/higgs.py` | `kg_step_free_2d_splitstep` |
| `src/casim/engine/particles/higgs.py` | `verify_vacuum_fixed_point` |
| `src/casim/engine/particles/induced_stiffness.py` | `chi_sweep` |
| `src/casim/engine/particles/induced_stiffness.py` | `dirac_chi_diamagnetic` |
| `src/casim/engine/particles/induced_stiffness.py` | `log_fit` |
| `src/casim/engine/particles/nuclear.py` | `_sigma_dot_n` |

### Ambiguous — name defined in more than one module

These are **not** proposed as dead. A reference to the name cannot be attributed to one definition, so calling it unused would be a guess. Same discipline as `gen_manifest.py`'s evidence ranking.

*586 symbols — see the JSON.*

---

## Signal 2 — named by the supersession ledger

### Paths

| Path | Record | Kind | Note |
|---|---|---|---|
| `src/casim/engine/gauge/bilinear.py` | S1-F69-sigma-bilinear-photon | superseded | retained for W/Z/gluon; no longer the photon |
| `src/casim/engine/gauge/photon.py` | S1-F69-sigma-bilinear-photon | superseded | the canonical photon |
| `src/casim/engine/gauge/gluon.py` | S2-F91-gluon-chiral-to-even | superseded | gluon_rotation_step_spectral_bcc is even (canonical); ..._bcc_chiral retained for comparison |
| `src/casim/engine/interactions/gravity.py` | S3-F64-dielectric-gravity | superseded | canonical dielectric; cites 'F62 sign-corrected local lapse mix'. Migrated from the legacy ca_gravity.py at ro |
| `src/casim/engine/interactions/gravity.py` | S4-F178-full-stress-energy | reclassified | canonical in vacuum / weak field (lensing, PPN). Migrated from the legacy ca_gravity.py at roadmap C6. |
| `src/casim/engine/interactions/stellar.py` | S4-F178-full-stress-energy | reclassified | strong-field/interior canonical solver, theory='gr'. Migrated from the legacy ca_stellar.py at roadmap C6. |
| `src/casim/engine/interactions/raytrace.py` | S4-F178-full-stress-energy | reclassified | RESOLVED at roadmap C6 (was: 'STALE: still computes F114_enlargement_pct. Flagged for P6.'). The quantity is K |
| `src/casim/engine/particles/derive_generator_norm.py` | S6-F253-weight-as-phase | superseded | Pre-decision framing. Its R=1 derivation is the F255 content and stands; its VERDICT ('E1 does not close') is  |
| `src/casim/engine/particles/derive_lambda6_sextic.py` | S6-F253-weight-as-phase | superseded | Already carries the weight-as-phase section (S4). Migrated from the legacy derive_lambda6_sextic.py at roadmap |
| `deprecated/code/migrate_module.py` | S8-D2-reversed-casim-is-the-program | methodology | The C0.4 migration tool. Retired with its subject at C9 — it copies a file out of ca-simulation/ into casim.en |
| `deprecated/code/gen_migration_manifest.py` | S8-D2-reversed-casim-is-the-program | methodology | Generated the 171-record migration manifest by walking ca-simulation/. The manifest itself stays live as the m |
| `deprecated/code/check_shim_imports.py` | S8-D2-reversed-casim-is-the-program | methodology | The C3.4 gate check — "no src code imports a ca-simulation shim path". Removed from `make gate` at C9: there a |
| `deprecated/code/route_numerics.py` | S8-D2-reversed-casim-is-the-program | methodology | C1 one-shot — routed numpy/scipy call sites onto casim.numerics. |
| `deprecated/code/_c5_repoint_sites.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — repointed src/ imports of migrated particles kernels. |
| `deprecated/code/_c5_run_tests.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — ran the particles sector's tests during migration. |
| `deprecated/code/engine_shim_channel.py` | S8-D2-reversed-casim-is-the-program | methodology | C3 moved the flat engine modules into `casim.engine.core/` and left nine intra-package `DeprecationWarning` sh |
| `deprecated/code/engine_shim_channels.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_observers.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_coupled.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_simulation.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_manybody.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_spectral_matter.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_tier3.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/engine_shim_blockspin.py` | S8-D2-reversed-casim-is-the-program | methodology | see engine_shim_channel.py |
| `deprecated/code/_c5_rewire_imports.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — rewrote import statements onto engine paths and proved each rewrite still bound the same local n |
| `deprecated/code/_c5_migrate_particles.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — drove the particles sector's migration using the migration tool's own templates, because the san |
| `deprecated/code/_c5_verify_sector.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — the migration tool's step 6 (baseline re-run), per sector. |
| `deprecated/code/_c5_fix_backup_index.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — corrected `deprecated/code/README.md`'s backup index. |
| `deprecated/code/_c5_drift_triage.py` | S8-D2-reversed-casim-is-the-program | methodology | C5 one-shot — triaged the sector's baseline drift. |
| `deprecated/code/repoint_tests.py` | S8-D2-reversed-casim-is-the-program | methodology | C9 one-shot — repointed all 259 test files off the legacy kernels (imports, fork file-path loads, sys.path pre |

### Candidate dead symbols

Extracted from each record's `scope:`, `also_superseded:` and `code:` notes. The **From** column matters: `scope` states what died, whereas a `code-note` routinely names the survivor and the casualty in one sentence, so it is weaker evidence. The **Conflict** column is the safety rail — it fires when the same record's `retained:` field names the identifier, or names a prefix-sibling of it. Read the record before accepting either.

| Symbol | Record | From | Defined in | Conflict |
|---|---|---|---|---|
| `gluon_rotation_step_spectral_bcc` | S2-F91-gluon-chiral-to-even | `code-note` | `src/casim/engine/gauge/gluon.py` | **sibling of protected `gluon_rotation_step_spectral_bcc_chiral` — DO NOT GUESS** |
| `derive_lambda6_sextic` | S6-F253-weight-as-phase | `code-note` | — | — |

**On the sibling flag.** A superseded symbol and its replacement almost always share a prefix here. `gluon_rotation_step_spectral_bcc` (canonical, even, F91) and `gluon_rotation_step_spectral_bcc_chiral` (retained for historical comparison) are named in the *same* ledger sentence, and the first version of this tool extracted them the wrong way round — proposing the canonical propagator as dead. It cannot be resolved from prose, so it is flagged, not guessed.

### Protected symbols (named in `retained:`)

Explicitly survived a supersession. **Never strip these** without re-reading the ledger record.

| Symbol | Record | Defined in |
|---|---|---|
| `gluon_rotation_step_spectral_bcc_chiral` | S2-F91-gluon-chiral-to-even | `src/casim/engine/gauge/gluon.py` |
| `lapse_mix_half` | S3-F64-dielectric-gravity | `src/casim/engine/interactions/gravity.py` |

---

## Signal 3 — reachable only from tombstoned tests

Tombstoned tests (`status: fully_superseded` in the ledger): 1.

*(none — no module depends solely on a fully-superseded test.)*

That is the expected result today: exactly one test in the project is fully superseded, and it tests a fork, not a kernel.
