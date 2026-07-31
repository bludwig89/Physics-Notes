# `deprecated/code/` — pre-clean originals

*Created 2026-07-30 - 09:30. Roadmap C0.5 (`docs/roadmaps/roadmap-casim-consolidation.md`).*

## What lands here

The **unmodified original** of every file migrated out of `ca-simulation/` into
`src/casim/engine/` under decision **D10**. The migration copies the file here
first, then writes a *cleaned* copy to its new engine path — dead symbols
stripped, numerics routed through `casim.numerics`, constants imported from
`casim.constants`.

Also: files retired outright (dead, or superseded wholesale) rather than
migrated.

## The acceptance rule

**Nothing lands here without one of two things:**

1. a record in `docs/design/module-migration-manifest.yaml` whose `source` is
   this file, or
2. a record in `docs/theory/supersessions.yaml` naming this file.

`tools/migrate_module.py` enforces (1) and refuses to overwrite an existing
backup. `make gate` asserts that every file in this directory satisfies one of
the two.

## Why a copy at all, when git has the history

Because the risk this guards against is a **bad clean**, not a lost file. If
`migrate_module.py` strips a symbol that turns out to be load-bearing three
phases later, the question is "what did this file look like before we touched
it", and answering that from a diff across an intervening reorganisation is
slower and more error-prone than opening the file. P0 found that of 14 files an
audit called superseded, exactly one was superseded wholesale — eleven were a
dead verdict wrapped around live, load-bearing algebra. That failure mode is
the reason this directory exists.

The copies are removed only when `ca-simulation/` itself is deleted at C9 —
and not even then, since by that point the originals exist nowhere else in the
working tree.

## Reading a file here

Every backup carries a header block prepended by the migration tool:

```
# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_foo.py
# migrated   : 2026-08-04 - 11:20
# target     : src/casim/engine/gauge/foo.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_foo.py)
# stripped   : _legacy_helper, OLD_TABLE
# reason     : F91 — chiral gluon step superseded by the even law
# ==================================================================
```

The header is prepended, never substituted into the body — the code below it is
byte-identical to what was there before.

## Index

*(populated by `tools/migrate_module.py` as files land)*

| Date | Source | Target | Reason |
|---|---|---|---|
| 2026-07-30 - 13:47 | `ca-simulation/ca_si_scale.py` | `src/casim/engine/lattice/si_scale.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_lattice.py` | `src/casim/engine/lattice/geometry.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_core.py` | `src/casim/engine/lattice/core.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_core_exact.py` | `src/casim/engine/lattice/core_exact.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_bcc.py` | `src/casim/engine/lattice/bcc.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_multigrid.py` | `src/casim/engine/lattice/multigrid.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_blockspin.py` | `src/casim/engine/lattice/blockspin.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_manybody.py` | `src/casim/engine/core/manybody.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_lpt_generator.py` | `src/casim/engine/core/lpt_generator.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/poisson_open.py` | `src/casim/engine/lattice/poisson_open.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/live_display.py` | `src/casim/engine/core/_viz_live_display.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/spinor_color.py` | `src/casim/engine/core/_viz_spinor_color.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/tick_heatmap.py` | `src/casim/engine/core/_viz_tick_heatmap.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/viz.py` | `src/casim/engine/core/_viz_legacy.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_baryon_blockspin.py` | `src/casim/engine/lattice/blockspin_baryon.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_blockspin_binding.py` | `src/casim/engine/lattice/blockspin_binding.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_blockspin_dynamical.py` | `src/casim/engine/lattice/blockspin_dynamical.py` | moved unchanged |
| 2026-07-30 - 13:53 | `ca-simulation/ca_curved.py` | `src/casim/engine/lattice/curved.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_bcc_gauge.py` | `src/casim/engine/gauge/bcc_action.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_bgfield_loop.py` | `src/casim/engine/gauge/bgfield_loop.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_charge_coupling.py` | `src/casim/engine/gauge/charge_coupling.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_charged_current.py` | `src/casim/engine/gauge/charged_current.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_chiral_anomaly.py` | `src/casim/engine/gauge/chiral_anomaly.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_colour_condensate.py` | `src/casim/engine/gauge/colour_condensate.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_colour_dielectric.py` | `src/casim/engine/gauge/colour_dielectric.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_confinement.py` | `src/casim/engine/gauge/confinement.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_cooling.py` | `src/casim/engine/gauge/cooling.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_emission.py` | `src/casim/engine/gauge/emission.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_gluon.py` | `src/casim/engine/gauge/gluon.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_gluon_self_energy.py` | `src/casim/engine/gauge/gluon_self_energy.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_hypercharge.py` | `src/casim/engine/gauge/hypercharge.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_link_hamiltonian.py` | `src/casim/engine/gauge/link_hamiltonian.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_lpt_selfenergy.py` | `src/casim/engine/gauge/lpt_selfenergy.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_lpt_vertex.py` | `src/casim/engine/gauge/lpt_vertex.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_lpt_ward.py` | `src/casim/engine/gauge/lpt_ward.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_lpt_wilson.py` | `src/casim/engine/gauge/lpt_wilson.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_lpt_wilson_selfenergy.py` | `src/casim/engine/gauge/lpt_wilson_selfenergy.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_maxwell.py` | `src/casim/engine/gauge/bilinear.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_maxwell_2d.py` | `src/casim/engine/gauge/bilinear_2d.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_minimal_coupling.py` | `src/casim/engine/gauge/minimal_coupling.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_photon_bs.py` | `src/casim/engine/gauge/photon_bound_state.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_photon_pair.py` | `src/casim/engine/gauge/photon.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_propagator.py` | `src/casim/engine/gauge/propagator.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_rotation.py` | `src/casim/engine/gauge/rotation.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_strong.py` | `src/casim/engine/gauge/strong.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_su3_ladder.py` | `src/casim/engine/gauge/su3_ladder.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_weak.py` | `src/casim/engine/gauge/weak.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_wmu.py` | `src/casim/engine/gauge/weak_wmu.py` | moved unchanged |
| 2026-07-30 - 14:48 | `ca-simulation/ca_z_field.py` | `src/casim/engine/gauge/weak_z.py` | moved unchanged |
| 2026-07-30 - 16:06 | `ca-simulation/ca_atom.py` | `src/casim/engine/particles/atom.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/ca_baryon.py` | `src/casim/engine/particles/baryon.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/ca_baryon_dynamics.py` | `src/casim/engine/particles/baryon_dynamics.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/ca_dirac.py` | `src/casim/engine/particles/dirac.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/ca_dirac_bcc.py` | `src/casim/engine/particles/dirac_bcc.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/ca_eg_sextic_coupling.py` | `src/casim/engine/particles/eg_sextic.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity); results path made location-independent + `__main__`-guarded |
| 2026-07-30 - 16:06 | `ca-simulation/ca_element.py` | `src/casim/engine/particles/element.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity); results path made location-independent + `__main__`-guarded |
| 2026-07-30 - 16:06 | `ca-simulation/ca_higgs.py` | `src/casim/engine/particles/higgs.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/ca_hyperfine.py` | `src/casim/engine/particles/hyperfine.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/ca_induced_stiffness.py` | `src/casim/engine/particles/induced_stiffness.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity); results path made location-independent + `__main__`-guarded |
| 2026-07-30 - 16:06 | `ca-simulation/ca_majorana.py` | `src/casim/engine/particles/majorana.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/ca_meson.py` | `src/casim/engine/particles/meson.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/ca_nuclear.py` | `src/casim/engine/particles/nuclear.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/ca_nuclear_core.py` | `src/casim/engine/particles/nuclear_core.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/ca_positronium.py` | `src/casim/engine/particles/positronium.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/ca_second_quant.py` | `src/casim/engine/particles/second_quant.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/derive_colour_condensate.py` | `src/casim/engine/particles/derive_colour_condensate.py` | copied byte-identically; no symbols stripped |
| 2026-07-30 - 16:06 | `ca-simulation/derive_generator_norm_from_F118.py` | `src/casim/engine/particles/derive_generator_norm.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity); results path made location-independent + `__main__`-guarded |
| 2026-07-30 - 16:06 | `ca-simulation/derive_lambda6_sextic.py` | `src/casim/engine/particles/derive_lambda6_sextic.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity); results path made location-independent + `__main__`-guarded |
| 2026-07-30 - 16:06 | `ca-simulation/derive_t2g_pmns_selector.py` | `src/casim/engine/particles/derive_t2g_pmns.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity) |
| 2026-07-30 - 16:06 | `ca-simulation/derive_weight_as_phase.py` | `src/casim/engine/particles/derive_weight_as_phase.py` | no symbols stripped; imports repointed to their `casim.engine` paths (same objects — the shim re-exports by identity); results path made location-independent + `__main__`-guarded |
| 2026-07-30 - 16:09 | `ca-simulation/ca_alpha_s_running.py` | `src/casim/engine/interactions/running_alpha_s.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_amu.py` | `src/casim/engine/interactions/qed_amu.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_bell_tsirelson.py` | `src/casim/engine/interactions/qi_bell_tsirelson.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_bethe_log.py` | `src/casim/engine/interactions/qed_bethe_log.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_blackhole.py` | `src/casim/engine/interactions/blackhole.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_casimir.py` | `src/casim/engine/interactions/qed_casimir.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_casimir_materials.py` | `src/casim/engine/interactions/qed_casimir_materials.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_cosmology.py` | `src/casim/engine/interactions/cosmology.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_darkmatter.py` | `src/casim/engine/interactions/darkmatter.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_decoherence_floor.py` | `src/casim/engine/interactions/qi_decoherence_floor.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_dual_gl_backreaction.py` | `src/casim/engine/interactions/gravity_backreaction.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_electron_self_energy.py` | `src/casim/engine/interactions/qed_electron_self_energy.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_emergent_gravity.py` | `src/casim/engine/interactions/gravity_emergent.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_emqg.py` | `src/casim/engine/interactions/gravity_emqg.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_entanglement.py` | `src/casim/engine/interactions/qi_entanglement.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_euler_heisenberg.py` | `src/casim/engine/interactions/qed_euler_heisenberg.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_gap_solve.py` | `src/casim/engine/interactions/running_gap_solve.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_gravity.py` | `src/casim/engine/interactions/gravity.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_horizon_entropy.py` | `src/casim/engine/interactions/horizon_entropy.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_inspiral.py` | `src/casim/engine/interactions/inspiral.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_interior_metric.py` | `src/casim/engine/interactions/interior_metric.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_ir_bremsstrahlung.py` | `src/casim/engine/interactions/qed_ir_bremsstrahlung.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_ir_coupling.py` | `src/casim/engine/interactions/running_ir_coupling.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_njl_induced_coupling.py` | `src/casim/engine/interactions/running_njl.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_ns_eos.py` | `src/casim/engine/interactions/ns_eos.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_qc_si.py` | `src/casim/engine/interactions/qi_qc_si.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_qcd_scale_ratio.py` | `src/casim/engine/interactions/running_scale_ratio.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_qed_renormalization.py` | `src/casim/engine/interactions/qed_renormalization.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_qed_scattering.py` | `src/casim/engine/interactions/qed_scattering.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_qnm.py` | `src/casim/engine/interactions/qnm.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_qstar_logmoment.py` | `src/casim/engine/interactions/running_qstar_logmoment.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_quantum_algorithms.py` | `src/casim/engine/interactions/qi_algorithms.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_quantum_noise.py` | `src/casim/engine/interactions/qi_noise.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_raytrace.py` | `src/casim/engine/interactions/raytrace.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_scheme_constant.py` | `src/casim/engine/interactions/running_scheme_constant.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_schwinger_pair.py` | `src/casim/engine/interactions/qed_schwinger_pair.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_slowlight.py` | `src/casim/engine/interactions/slowlight.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_stellar.py` | `src/casim/engine/interactions/stellar.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_superconductivity.py` | `src/casim/engine/interactions/superconductivity.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_tolman.py` | `src/casim/engine/interactions/tolman.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_twoloop_ae.py` | `src/casim/engine/interactions/qed_twoloop_ae.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_unified.py` | `src/casim/engine/interactions/unified.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_vacuum_energy.py` | `src/casim/engine/interactions/vacuum_energy.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_vacuum_polarization.py` | `src/casim/engine/interactions/qed_vacuum_polarization.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/ca_vertex_loop.py` | `src/casim/engine/interactions/qed_vertex_loop.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/derive_beta_LV.py` | `src/casim/engine/interactions/derive_beta_LV.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/derive_curl_subleading.py` | `src/casim/engine/interactions/derive_curl_subleading.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/derive_dielectric_noconfine.py` | `src/casim/engine/interactions/derive_dielectric_noconfine.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/derive_f26_dispersion.py` | `src/casim/engine/interactions/derive_f26_dispersion.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/derive_velocity_addition.py` | `src/casim/engine/interactions/derive_velocity_addition.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/run_Q3_omega_degeneracy.py` | `src/casim/engine/interactions/run_q3_omega_degeneracy.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/__init__.py` | `src/casim/engine/forks/__init__.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/complex_mass_fork.py` | `src/casim/engine/forks/particles/complex_mass_fork.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/curl_fork_baseline_bcc.py` | `src/casim/engine/forks/gauge/curl_fork_baseline_bcc.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/curl_fork_cubic.py` | `src/casim/engine/forks/gauge/curl_fork_cubic.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/curl_fork_harness.py` | `src/casim/engine/forks/gauge/curl_fork_harness.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/dirac_gravity_fork.py` | `src/casim/engine/forks/gravity/dirac_gravity_fork.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/dm_fork_F205_sterile_qke_boltzmann.py` | `src/casim/engine/forks/darkmatter/dm_fork_F205_sterile_qke_boltzmann.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/dm_fork_F237_kev_sterile_resolution.py` | `src/casim/engine/forks/darkmatter/dm_fork_F237_kev_sterile_resolution.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr3_fork_A_phase_tick.py` | `src/casim/engine/forks/gravity/gr3_fork_A_phase_tick.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr3_fork_B_anisotropic.py` | `src/casim/engine/forks/gravity/gr3_fork_B_anisotropic.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr3_fork_C_restricted_c.py` | `src/casim/engine/forks/gravity/gr3_fork_C_restricted_c.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr3_fork_baseline.py` | `src/casim/engine/forks/gravity/gr3_fork_baseline.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr3_fork_harness.py` | `src/casim/engine/forks/gravity/gr3_fork_harness.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr3_forks_AB_extended.py` | `src/casim/engine/forks/gravity/gr3_forks_AB_extended.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_E_tensor.py` | `src/casim/engine/forks/gravity/gr_fork_E_tensor.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F164_cosmological_constant.py` | `src/casim/engine/forks/gravity/gr_fork_F164_cosmological_constant.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F180_gw_speed.py` | `src/casim/engine/forks/gravity/gr_fork_F180_gw_speed.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F193_ontic_vacuum.py` | `src/casim/engine/forks/gravity/gr_fork_F193_ontic_vacuum.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F196_dilution_exponent.py` | `src/casim/engine/forks/gravity/gr_fork_F196_dilution_exponent.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F197_first_excitation_dark.py` | `src/casim/engine/forks/gravity/gr_fork_F197_first_excitation_dark.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F198_angular_misalignment.py` | `src/casim/engine/forks/gravity/gr_fork_F198_angular_misalignment.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F199_amplitude_mode_stability.py` | `src/casim/engine/forks/gravity/gr_fork_F199_amplitude_mode_stability.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F200_sterile_neutrino_dm.py` | `src/casim/engine/forks/gravity/gr_fork_F200_sterile_neutrino_dm.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F201_kev_from_eg_texture.py` | `src/casim/engine/forks/gravity/gr_fork_F201_kev_from_eg_texture.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F202_leptogenesis_sakharov.py` | `src/casim/engine/forks/gravity/gr_fork_F202_leptogenesis_sakharov.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F203_dark_sector_falsifiers.py` | `src/casim/engine/forks/gravity/gr_fork_F203_dark_sector_falsifiers.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F216_massive_spin2.py` | `src/casim/engine/forks/gravity/gr_fork_F216_massive_spin2.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F223_spin2_binding_relic.py` | `src/casim/engine/forks/gravity/gr_fork_F223_spin2_binding_relic.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F228_geon_production_stability.py` | `src/casim/engine/forks/gravity/gr_fork_F228_geon_production_stability.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F238_geon_relic_abundance.py` | `src/casim/engine/forks/gravity/gr_fork_F238_geon_relic_abundance.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F248_tt_graviton_bcc.py` | `src/casim/engine/forks/gravity/gr_fork_F248_tt_graviton_bcc.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F46_dirac.py` | `src/casim/engine/forks/gravity/gr_fork_F46_dirac.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F52_restleg_backreaction.py` | `src/casim/engine/forks/gravity/gr_fork_F52_restleg_backreaction.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F55_spatial_metric_backreaction.py` | `src/casim/engine/forks/gravity/gr_fork_F55_spatial_metric_backreaction.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F56_einstein_coupling_derivation.py` | `src/casim/engine/forks/gravity/gr_fork_F56_einstein_coupling_derivation.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F57_induced_eh_from_backreaction.py` | `src/casim/engine/forks/gravity/gr_fork_F57_induced_eh_from_backreaction.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F58_clockrate_coupling_derivation.py` | `src/casim/engine/forks/gravity/gr_fork_F58_clockrate_coupling_derivation.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F59_induced_eh_prefactor.py` | `src/casim/engine/forks/gravity/gr_fork_F59_induced_eh_prefactor.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F60_channel_reconciliation.py` | `src/casim/engine/forks/gravity/gr_fork_F60_channel_reconciliation.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F61_weyl_eta_gstar.py` | `src/casim/engine/forks/gravity/gr_fork_F61_weyl_eta_gstar.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F63_spin_torsion_estimate.py` | `src/casim/engine/forks/gravity/gr_fork_F63_spin_torsion_estimate.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F64_em_connection.py` | `src/casim/engine/forks/gravity/gr_fork_F64_em_connection.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_fork_F79_structural_G.py` | `src/casim/engine/forks/gravity/gr_fork_F79_structural_G.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/gr_tensor_stub.py` | `src/casim/engine/forks/gravity/gr_tensor_stub.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/hypercharge_fork.py` | `src/casim/engine/forks/electroweak/hypercharge_fork.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/lgt_fork_A_mc.py` | `src/casim/engine/forks/gauge/lgt_fork_A_mc.py` | moved unchanged |
| 2026-07-30 - 16:09 | `ca-simulation/forks/smearing_fork_harness.py` | `src/casim/engine/forks/lattice/smearing_fork_harness.py` | moved unchanged |
