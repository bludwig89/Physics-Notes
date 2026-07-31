# Dead-code proposal

*Generated 2026-07-31 05:39 UTC by `tools/find_dead_code.py` (roadmap C0.2) at graph `975ff21`. **Do not edit by hand** — regenerate.*

> **This is a proposal, not a verdict.** Nothing here has been applied.
> A human accepts a line by moving it into `dead_symbols` in
> `docs/design/module-migration-manifest.yaml`; only accepted lines are
> stripped by `tools/migrate_module.py`. The three signals below are
> independent and must not be summed — P0.4 found that of 14 files an
> audit called superseded, exactly **one** was superseded wholesale.

| Signal | Count |
|---|---|
| 1. unreferenced files | 36 |
| 1. unreferenced symbols **(proposed)** | 5 |
| 1. module-private helpers (used internally — NOT dead) | 15 |
| 1. ambiguous (name defined in >1 module — NOT dead) | 338 |
| 2. ledger-named paths | 9 |
| 2. candidate dead symbols (from `scope:`) | 5 |
| 2. PROTECTED symbols (from `retained:`) | 2 |
| 3. modules reachable only from tombstoned tests | 0 |

---

## Signal 1 — structurally unreachable

### Files nothing imports, with no `__main__`

| Path | Role | Lines | Why | Ledger |
|---|---|---|---|---|
| `ca-simulation/benchmark_jax.py` | derivation | 128 | nothing imports it and it has no __main__ | — |
| `ca-simulation/ca_casimir_materials.py` | kernel | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/ca_lpt_generator.py` | kernel | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_beta_LV.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_curl_subleading.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_dielectric_noconfine.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_f26_dispersion.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_generator_norm_from_F118.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_lambda6_sextic.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_velocity_addition.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/derive_weight_as_phase.py` | derivation | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/__init__.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/complex_mass_fork.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/curl_fork_baseline_bcc.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/curl_fork_cubic.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/curl_fork_harness.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr3_fork_A_phase_tick.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr3_fork_B_anisotropic.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr3_fork_C_restricted_c.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr3_fork_baseline.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr3_fork_harness.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr3_forks_AB_extended.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F164_cosmological_constant.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F216_massive_spin2.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F223_spin2_binding_relic.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F228_geon_production_stability.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F238_geon_relic_abundance.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F248_tt_graviton_bcc.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F59_induced_eh_prefactor.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F60_channel_reconciliation.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F61_weyl_eta_gstar.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_fork_F63_spin_torsion_estimate.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/gr_tensor_stub.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/forks/smearing_fork_harness.py` | fork | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/live_display.py` | support | 48 | nothing imports it and it has no __main__ | — |
| `ca-simulation/run_Q3_omega_degeneracy.py` | derivation | 48 | nothing imports it and it has no __main__ | — |

Two entries here are the roadmap's own worked example. `derive_generator_norm_from_F118.py` has no `__main__` and nothing imports it, so it lands in this table — and it must **not** be deleted: P0.4 gave it a `PRE-DECISION FRAMING` banner because its Schur-isotropy proof *is* the F255 content, and its circularity argument is precisely *why* the F234 arrow was reversed. It migrates with the banner intact (roadmap C5). This is what "a signal is not a verdict" looks like in practice.

### Top-level symbols nothing in the tree references

**5 proposed.** A separate **15** are referenced inside their own module and are therefore private helpers, not dead code — removing one means removing its callers too, which is a refactor. Those are in the JSON under `module_private` and are NOT proposed.

| Path | Symbol |
|---|---|
| `ca-simulation/ca_lazy.py` | `extract_dirac_2d` |
| `ca-simulation/ca_lazy.py` | `lazy_position_space_kick` |
| `ca-simulation/ca_lazy.py` | `per_cell_residual_scalar` |
| `ca-simulation/ca_lazy.py` | `sync_vs_lazy_residual` |
| `ca-simulation/ca_lazy.py` | `time_loop` |

### Ambiguous — name defined in more than one module

These are **not** proposed as dead. A reference to the name cannot be attributed to one definition, so calling it unused would be a guess. Same discipline as `gen_manifest.py`'s evidence ranking.

*338 symbols — see the JSON.*

---

## Signal 2 — named by the supersession ledger

### Paths

| Path | Record | Kind | Note |
|---|---|---|---|
| `ca-simulation/ca_maxwell.py` | S1-F69-sigma-bilinear-photon | superseded | retained for W/Z/gluon; no longer the photon |
| `ca-simulation/ca_photon_pair.py` | S1-F69-sigma-bilinear-photon | superseded | the canonical photon |
| `ca-simulation/ca_gluon.py` | S2-F91-gluon-chiral-to-even | superseded | gluon_rotation_step_spectral_bcc is even (canonical); ..._bcc_chiral retained for comparison |
| `src/casim/engine/interactions/gravity.py` | S3-F64-dielectric-gravity | superseded | canonical dielectric; cites 'F62 sign-corrected local lapse mix'. Migrated from ca-simulation/ca_gravity.py at |
| `src/casim/engine/interactions/gravity.py` | S4-F178-full-stress-energy | reclassified | canonical in vacuum / weak field (lensing, PPN). Migrated from ca-simulation/ca_gravity.py at roadmap C6. |
| `src/casim/engine/interactions/stellar.py` | S4-F178-full-stress-energy | reclassified | strong-field/interior canonical solver, theory='gr'. Migrated from ca-simulation/ca_stellar.py at roadmap C6. |
| `src/casim/engine/interactions/raytrace.py` | S4-F178-full-stress-energy | reclassified | RESOLVED at roadmap C6 (was: 'STALE: still computes F114_enlargement_pct. Flagged for P6.'). The quantity is K |
| `src/casim/engine/particles/derive_generator_norm.py` | S6-F253-weight-as-phase | superseded | Pre-decision framing. Its R=1 derivation is the F255 content and stands; its VERDICT ('E1 does not close') is  |
| `src/casim/engine/particles/derive_lambda6_sextic.py` | S6-F253-weight-as-phase | superseded | Already carries the weight-as-phase section (S4). Migrated from ca-simulation/derive_lambda6_sextic.py at road |

### Candidate dead symbols

Extracted from each record's `scope:`, `also_superseded:` and `code:` notes. The **From** column matters: `scope` states what died, whereas a `code-note` routinely names the survivor and the casualty in one sentence, so it is weaker evidence. The **Conflict** column is the safety rail — it fires when the same record's `retained:` field names the identifier, or names a prefix-sibling of it. Read the record before accepting either.

| Symbol | Record | From | Defined in | Conflict |
|---|---|---|---|---|
| `ca_maxwell` | S1-F69-sigma-bilinear-photon | `scope` | — | — |
| `ca_gravity` | S3-F64-dielectric-gravity | `code-note` | — | **PROTECTED — also in `retained:`** |
| `ca_gravity` | S4-F178-full-stress-energy | `code-note` | — | **PROTECTED — also in `retained:`** |
| `ca_stellar` | S4-F178-full-stress-energy | `code-note` | — | — |
| `derive_lambda6_sextic` | S6-F253-weight-as-phase | `code-note` | — | — |

**On the sibling flag.** A superseded symbol and its replacement almost always share a prefix here. `gluon_rotation_step_spectral_bcc` (canonical, even, F91) and `gluon_rotation_step_spectral_bcc_chiral` (retained for historical comparison) are named in the *same* ledger sentence, and the first version of this tool extracted them the wrong way round — proposing the canonical propagator as dead. It cannot be resolved from prose, so it is flagged, not guessed.

### Protected symbols (named in `retained:`)

Explicitly survived a supersession. **Never strip these** without re-reading the ledger record.

| Symbol | Record | Defined in |
|---|---|---|
| `ca_gluon` | S2-F91-gluon-chiral-to-even | — |
| `ca_gravity` | S3-F64-dielectric-gravity | — |

---

## Signal 3 — reachable only from tombstoned tests

Tombstoned tests (`status: fully_superseded` in the ledger): 1.

*(none — no module depends solely on a fully-superseded test.)*

That is the expected result today: exactly one test in the project is fully superseded, and it tests a fork, not a kernel.
