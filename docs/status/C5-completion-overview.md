# C5 completion overview — sector migration: particles

*2026-07-30 - 21:40. Phase C5 of `docs/roadmaps/roadmap-casim-consolidation.md`. Entry state: C0–C4 complete, gate 17/18 with one pre-existing failure, drift limited to the two files C4 handed off. Verified in FULL mode with the vendored scipy/pytest env (`source .vendor/activate.sh`).*

## Sector claim, and a live collision that did not happen

The particles sector was claimed in the manifest's `claims:` block **before any file moved**, per C3's handoff rule — `claims.particles = {session: gifted-nifty-euler, phase: C5, claimed: 2026-07-30 - 20:59}`.

Three minutes later a second session (`nifty-great-volta`) claimed **`interactions` and `forks` for C6** and began writing `src/casim/engine/interactions/` and `src/casim/engine/forks/`. The concurrency rule earned its place here: this session's import-rewiring pass wanted to touch 65 files, 48 of them in C6's live trees. The rewiring tool was given an ownership rule read from the manifest rather than a hardcoded list:

- **inside `engine/particles/`** — this session owns the file, so every migrated kernel it imports is repointed;
- **everywhere else** — only imports *of* a particles kernel are repointed, and any directory claimed by a different live session is skipped outright.

Result: 11 files inside the sector plus 12 shared consumers, and **zero writes into C6's trees**. The residual C3.4 gate failure (52 shim imports) is entirely theirs — 23 in `interactions/`, 29 in `forks/`, none anywhere else.

## What landed

**All 21 `sector: particles` records migrated into `engine/particles/`** — the Dirac walk (cubic + BCC), second quantization, baryon/meson/nuclear/atom/element, positronium and hyperfine, Majorana, Higgs, the E_g sextic coupling, induced stiffness, and the five `derive_*` lepton-shape and PMNS derivations. Each is D10: pre-clean original backed up under `deprecated/code/` with a header, cleaned copy at the new path, `DeprecationWarning` shim at the old path, manifest stamped, registry record generated.

Migrations were done **overwrite-only and byte-faithful to `migrate_module.py`'s own `BACKUP_HEADER`/`SHIM` templates, imported rather than copied** (`tools/_c5_migrate_particles.py`). The reason is C4's: the sandbox mount refuses `unlink`, so the tool's journal cannot roll back, and an abort would orphan the backup and target and leave the retry refusing on "target already exists". The driver asserts byte-identity per file and refuses any record that accepts a dead symbol — such a record has to go through `migrate_module.py` so its baselines get diffed.

**Zero dead symbols accepted, and that is a decision, not an omission.** All nine `dead_symbols_proposed` in the sector are genuinely unreferenced — verified, including no intra-module callers — and every one was still kept:

| Proposed | Why it stays |
|---|---|
| `dirac_step_2d_varm_splitstep` | **F62 has an open follow-up on it** ("fix the sign in `ca_dirac.dirac_step_2d_varm_splitstep` itself once a gradient-mass production test exists"). Two live docstrings cite it as the sign-convention counterexample. Deleting it silently closes a finding's action item. |
| `dirac_chi_diamagnetic` | Named in F153's Module line and method section — the diamagnetic charge-blind result. It *is* the falsification record. |
| `proton_colour_field` | Its docstring is the ε_abc argument for why the spin-flavour wavefunction must be symmetric. Explicitly "provided for completeness/illustration" — a recorded negative result. |
| `kg_nonlinear_kick`, `kg_step_free_2d_splitstep`, `verify_vacuum_fixed_point` | Exact K-G split-step propagator + F1's vacuum-stability check. |
| `chi_sweep`, `log_fit` | The χ(q̃)/q̃² log-fit machinery behind F147's C coefficient. |
| `_sigma_dot_n` | Spin-operator helper in the two-nucleon basis. |

This is P0.4's measured lesson applied (of 14 files an audit called superseded, one was superseded wholesale), and it matches the roadmap's own named C5 cleanup: **`derive_generator_norm_from_F118.py` migrated with its `PRE-DECISION FRAMING` banner intact**, because its Schur-isotropy R=1 proof *is* the F255 content. The supersession ledger's `code:` path for the S6-F253 record was repointed at the new location, which is what turned the banner from an orphan back into a ledger-backed one.

**The C5 gate item on δ\* and λ₆ was already satisfied by C2** and is now verified: all three derivations import `delta_star`, `delta_star_f`, `lambda_6` and `B_sea_cubic` from `casim.constants`. The surviving textual `2/9` in `derive_weight_as_phase.py` is `sp.Rational(dims["E"]*mult["E"], total)` — the O_h projection that *computes* the E_g weight and compares it to the registry value. That is the F175/F255 check itself, not a redefinition, and removing it would delete the derivation.

**15 `Site()` records in `casim.constants` repointed** at the migrated targets. A `Site(path, symbol, kind="import")` asserts *that file imports that symbol from the registry*; after migration the assertion is false at the shim and true at the target, which is why the D7 gate check went red until the paths moved.

## Two defects the move exposed, and one it created

**The three lepton-shape derivations wrote to `"../test-results/<name>.json"`** — relative to the *working directory*, so they only ever resolved when run from inside `ca-simulation/`, and from four levels deeper they raised `FileNotFoundError` on import. Replaced with `engine/particles/_results_path.py`, which walks up from its own location (lazily, and cached — resolving at module scope would make an installed `casim` unable to import these three at all). It deliberately does not call `casim.suite.runner.find_repo_root`: an engine kernel importing the suite layer inverts the dependency direction this roadmap exists to establish.

**Those same three ran their full derivation *and wrote the result file* at import, with no `__main__` guard.** Harmless as `ca-simulation/` scripts. Not harmless inside the package: any recursive import — `pkgutil.walk_packages`, pytest collecting `src/`, coverage, plausibly `casim index` at C8 — would silently overwrite a **committed baseline artifact** that `make drift` compares against HEAD. The write is now guarded; the derivation still runs on import as before, and `python3 -m casim.engine.particles.derive_weight_as_phase` still reproduces its committed JSON byte-for-byte. C5 widened the blast radius of this one, so C5 closes it.

**`migrate_module.run_tests` overwrote `PYTHONPATH` instead of prepending it**, dropping `.vendor/py310-linux-aarch64` from every child process. Under the vendored env that turns each pytest-only test into `ModuleNotFoundError: No module named 'pytest'` — which the function reports as a **test failure**, i.e. a migration would abort and blame the physics for a broken environment. Found because it produced exactly that false failure here on `test_F140_coarse_grained_baryon.py`, which passes 9/9. Fixed in the C0 tool, not just in this phase's driver, because C6 and C7 depend on it.

Also removed: vestigial `sys.path.insert(0, dirname(__file__))` in `element.py`, `eg_sextic.py` and `induced_stiffness.py`. Those served bare `import ca_bcc` / `import ca_atom`; after the rewrite they were dead **and inverted into a hazard** — from the new directory they put `atom`, `dirac`, `element`, `nuclear`, `meson`, `higgs`, `positronium` on `sys.path[0]` as *top-level* names, shadowing anything of the same name for the rest of the process.

## Verification (full mode, vendored scipy + pytest)

**`make gate`: 16 of 18 green, and neither red is C5's.** All 3 provenance, all 5 test-suite-health, all 5 migration-readiness checks and all 3 scenario smokes pass. The two failures:

- **C3.4 shim imports** — every flagged file is in the C6 session's live trees (as of this writing 38: 23 in `interactions/`, 15 in `forks/`; the count moves as they work). **Zero in `engine/particles/` or anywhere else.**
- **`pytest tests/casim`** — 112 passed, 1 failed, and the failure is the pre-existing `test_backend.py::test_ca_fft_alias_delegates_to_the_active_library` that C2, C3 and C4 each recorded: it asserts `ca_fft` equals `np.fft` bit-for-bit and fails only because the vendored env makes **scipy** the active FFT library. It touches no C5 module.

**Sector tests: 57 of 64 ran and passed.** Four exceed the sandbox's per-call wall-clock cap and were not run to completion — `test_FB08_nn_repulsive_core.py` (>43 s, user 53 s), `run_L192_tests.py`, `run_phaseF_tests.py`, `run_phase_tests.py`. Recorded as **not run**, not as passing: a clean diff over zero executions is not evidence. Their modules are covered by tests that did pass (nuclear/nuclear_core by F113 7/7, F126, F128, F240, FB07, P4; the phaseF battery by `run_L192_phaseF_tests.py`).

Three test files fail, **all three pre-existing and all three path defects, unmodified from HEAD**:

| Test | Cause |
|---|---|
| `test_08_QM2_tunneling.py` | Calls `ca_dirac.dirac_step_u1_2d_splitstep`, which does not exist at HEAD either (`git show HEAD:… \| grep -c` → 0). |
| `test_FG9_C_CP_per_species.py` | Its own two `sys.path.insert` targets are `<repo>/tests/ca-simulation` and `<repo>/../ca-simulation` — neither exists (off-by-one `dirname`). Passes 6/6 with `ca-simulation` on the path. Its `RESULTS_DIR` has the same off-by-one, so it writes to `tests/test-results/` and its committed baseline is never actually refreshed. |
| `run_phase2_f26_tests.py` | 16/17; the one failure looks for `tests/runners/test_su2_photon_bridge.py`, which lives at `tests/findings/`. |
| `run_propagation_demo.py` | Its locator's third candidate is the hardcoded absolute path `/sessions/blissful-epic-faraday/mnt/Physics Notes/ca-simulation` — a different session's mount. |

**Drift: C5 introduces none, and the attribution is measured rather than asserted.** Two independent arguments:

1. *Structural.* Every target is byte-identical to its pre-migration original (SHA-verified per file), and the only subsequent edits are import rewrites — proven to be a **semantic no-op by object identity**: for all eight rewired module pairs, every public callable satisfies `old.fn is new.fn`, because the shim re-exports by `globals().update`. 148 callables checked, zero differ. A rewrite that cannot change which function object is called cannot change a number.
2. *Empirical.* Running the sector rewrote 36 artifacts; 14 showed drift above the project's own `machine` floor (1e-12 — `tools/check_result_drift.py`'s 1e-15 default reports round-off as drift, which cannot distinguish "physics changed" from "float work was reordered"; `tools/_c5_drift_triage.py` splits it three ways). Every one was then attributed by **re-running the same test against a pristine `git archive HEAD` extract**:
   - `FG2_quark_complex_mass` (n_pass 11→10) and `FG3_quark_electroweak` (n_pass 6→3, `results[3].norm1` 102.98→0.82) — **HEAD's own code reproduces the identical deltas to 1e-15. Both committed baselines were already stale before any C-phase.** These are result-dump tests with no assert, so they exit 0 while their numbers move; the drift *is* the failure signal and nothing was watching it.
   - `figures/T1_results.json` (`pkt_ticks` 75270→75273, deterministic across reruns) and `figures/T5_results.json` (`occupied_cells` 14567→14565) — HEAD reproduces the baselines exactly, so this drift is real and comes from the working tree. `ca_higgs` was changed by **C1.3's FFT routing (9 lines) before C5 touched it**, versus C5's 2 lines of provably-inert import rewrite. C1's verification diffed artifacts but never re-ran T1/T5, so a threshold-crossing tick count amplified a last-bits FFT difference into an integer change that no gate saw.
   - `F144_route_a_alpha_s` — HEAD reproduces its baseline exactly; the working-tree delta is the same `a/ℓ_P` 6.59782→closed-form change C1 already recorded as **C2's, and correct**, in `F233`. F144 simply shares `ca_alpha_s_running` and was never re-run.
   - `top10_T10_QG4_charge`, `phase2_f26_results`, `FB07_deuteron` — round-off at 1e-13/1e-14 in quantities whose own gate is machine ε, plus the pre-existing F29 path failure above.

   All 36 were then restored, except the seven belonging to other phases. Working-tree drift now stands at **four files, none of them this sector's**: `F144`, `F192`, `F233` (interactions — C2-accepted or C6's re-runs) and `wmu_phase3` (pre-existing uncommitted work, flagged since P1).

**Module registry 178/178 covered** (D11), including a hand-declared `spine` record for `particles._results_path`. `casim list-channels` runs. Supersession ledger 19 PASS / 0 FAIL after the path repoint. Manifest, module graph, results manifest and exactness inventory regenerated and current.

## For Ben / handoff

- **C6 (interactions + forks) is live in another session right now** and has already stamped all 98 of its records. Its C3.4 shim imports and its result drift (`F107`, `F144`, `F145`, `F192`) are its to close. Do not read the single red gate check as C5's.
- **One roadmap scope line was deliberately not executed.** C5's scope says "plus `src/casim/particles/*` reorganised under `engine/particles/`". That directory has **no manifest record**, and C0.3's rule is that a file with no record does not move. So `casim.particles` (`channel.py`, `composite.py`, `spec.py`) still exists alongside `casim.engine.particles`, which is exactly the two-layer seam D6 exists to remove. It needs a manifest record before it can move — three tests import it (`test_particle_layer`, `test_F136`, `test_F137`) and it is a genuine package-layer reorganisation, not a kernel migration. Flagging it rather than doing it unrecorded.
- **Four things this phase found that outlive it**, all worth a decision from you:
  1. `FG2` and `FG3` committed baselines do not reproduce at HEAD. Two live findings' result files are stale by 1 and 3 checks respectively. Someone should decide whether the code regressed or the baselines were committed from a different configuration.
  2. C1.3's FFT routing moved `T1`/`T5` integer observables. Real, small, and invisible to C1's gate because artifacts were diffed but not regenerated. The general lesson — *diffing an artifact you did not re-run proves nothing* — is exactly what C7's registry is meant to make structural.
  3. `test_FG9` writes its results to `tests/test-results/`, so its committed baseline has never been refreshed by the test that owns it. Same off-by-one `dirname` as its import path.
  4. Four sector tests cannot run to completion inside the sandbox's wall-clock cap. C7's `tier` field (`gate | battery | archive`) is the right home for that fact.
- **`migrate_module.py`'s `PYTHONPATH` fix matters for you before C6/C7 finish.** Any migration run under the vendored env before this fix would have reported pytest-only tests as failures or silently skipped them.
- Five imports in this sector now point at C6-owned modules (`eg_sextic` → `running_gap_solve`/`running_njl`, `hyperfine` → `qed_vertex_loop`, `positronium` → `qed_scattering`, `second_quant` → `qi_entanglement`). All five resolve, but they were written against names C6 had not landed yet — a cross-sector dependency the "one session, one sector" rule cannot express, and worth a note in C7.
- The phase's own drivers are `tools/_c5_migrate_particles.py`, `_c5_rewire_imports.py`, `_c5_run_tests.py`, `_c5_verify_sector.py`, `_c5_drift_triage.py`, `_c5_repoint_sites.py`, `_c5_fix_backup_index.py`. The triage tool is the reusable one — C6 and C7 will want a floor-aware, HEAD-attributing drift report rather than the 1e-15 default.
