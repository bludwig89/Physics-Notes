# C6 completion overview — sector migration: interactions, gravity, and the long tail

*2026-07-30 - 21:35. Phase C6 of `docs/roadmaps/roadmap-casim-consolidation.md`. Entry state: C3 complete, `make gate` green (24 checks), tree drift limited to the two documented pre-existing artifacts (`F233`, `wmu_phase3`). Verified with the vendored scipy/pytest env (`source .vendor/activate.sh`). Ran concurrently with a live C5 (particles) session — see "Cross-sector" below.*

## Sector claim

Claimed **before any file moved**, per the roadmap's concurrency rule: `claims.interactions` and `claims.forks`, both `{session: nifty-great-volta, phase: C6, claimed: 2026-07-30 - 21:02}`. C6 owns two of the manifest's seven sectors, so both are claimed together and named as such in the claim note. `gen_migration_manifest.py` preserved them across four regenerations.

## What landed

**All 98 C6 records migrated — 51 `sector: interactions` into `engine/interactions/`, 47 `sector: forks` into `engine/forks/<subsector>/`.** Each is D10: pre-clean original in `deprecated/code/` under the generated header, cleaned copy at the target, `DeprecationWarning` shim at the `ca-simulation/` source, manifest stamped, `deprecated/code/README.md` indexed. `ca-simulation/` now holds **169 shims and 2 non-shim files** — `benchmark_jax.py` and `ca_lazy.py`, both `phase: C1, sector: numerics`, which C1 left behind and which are not C6's to move.

Migrations were done **overwrite-only and byte-faithful to `migrate_module.py`'s own `BACKUP_HEADER`/`SHIM` templates**, which the driver imports rather than copies, because this sandbox mount blocks `unlink` (verified: `rm` returns `Operation not permitted`), so the canonical tool's rollback would fail halfway and orphan files. This is C4's precedent, unchanged.

**Sector map.** `interactions/` is prefixed by subsector so the flat directory stays readable: `gravity*`, `blackhole`/`qnm`/`inspiral`/`horizon_entropy`/`interior_metric`/`tolman`/`ns_eos`/`stellar`/`cosmology`/`darkmatter`/`raytrace`, `qed_*` (13 modules), `running_*` (7), `qi_*` (5), plus `derive_*`/`run_*` entry scripts. Forks split into `forks/{gravity,darkmatter,gauge,electroweak,lattice,particles}/`.

## The one thing a byte-identical move breaks: `__file__` arithmetic

A byte-identical copy is only behaviour-preserving if the file does not ask where it is. Nineteen forks did:

**20 repo-root walks were two levels (`ca-simulation/forks/` → repo) and are now five.** Left alone, `gr_fork_F216`, `F223`, `F228`, `F238`, `F248`, `gr3_fork_harness`, `gr_tensor_stub`, `F164`, `F193`, `F196`, `F197`–`F203`, `dm_fork_F205` and `dm_fork_F237` would have written their finding JSON into `src/casim/engine/test-results/` — wrong directory, and an artifact the results manifest would never see. The transform expands the `".."` run from 2 to 5 and touches nothing else, so each expression resolves to the **same absolute directory** as before; every edited assignment carries a two-line comment saying the count is a consequence of the module's depth. Verified mechanically (5 levels up == repo root for all 19; no 2-step run left; all parse) and then empirically — importing the forks wrote `test-results/F228_geon_production_stability.json` and `test-results/F238_geon_relic_abundance.json` at the repo root.

This is the C3 lesson (relative *imports* broke on depth) in its path-arithmetic form, and it is the reason a "byte-identical target ⇒ no drift" argument needs a `__file__` audit attached. Two related patterns were deliberately **not** changed: sibling-directory `sys.path` self-inserts (still correct — fork families moved together into one subsector directory) and the four `OUT = dirname(__file__)` forks that write `f59/f60/f61/f63_results.json` next to themselves (unchanged semantics; they polluted their own directory before and still do — a C7 registry question, not a move question).

`ca_vacuum_energy`'s `_FORKS = <my dir>/forks` sys.path injection was the same class of breakage in the interactions sector; it is now a package import of `casim.engine.forks.gravity.gr_fork_F164_cosmological_constant`. F192 re-runs 3/3 with physics values identical.

**C5 independently hit the same hazard** and solved its (different, cwd-relative) version with a helper module, `engine/particles/_results_path.py`. Two sessions converging on the same class of bug from opposite ends is worth a note for C7/C8: unifying on one results-path helper would retire both fixes.

## Cleanups

**F114 — resolved by relabelling, not by cutting.** The ledger flagged `ca_raytrace.py` as `STALE: still computes F114_enlargement_pct`, deferred P0 → P6 → C6. It is *not* a strippable top-level symbol; it is a dict key inside the live `eht_predictions()`, `tests/findings/test_F186_shadow_raytrace.py` T2 **asserts on it** (GR shadow < F114 shadow, enlargement pinned to +4.63%), and it is a key in a committed baseline. So the honest resolution is the one roadmap §8 asks for — "F114 stays checkable, that is how the supersessions stay honest": `eht_predictions()`'s docstring now states outright that the two `*_F114` fields are the standing **exclusion record** and never a prediction, the inline comment says `EXCLUDED (F178)`, and the ledger note changes from `STALE … Flagged for P6` to `RESOLVED at roadmap C6` with the three reasons. Deleting it would have removed a live falsification gate and drifted a baseline key for no gain.

**F50/F52/F62 — nothing to strip, and that is the finding.** `ca_gravity.py` implements only the canonical F64 dielectric, F106 `T⁰⁰` sourcing and the **retained** F62 lapse-mix sign convention (`lapse_mix_half`, a ledger-`protected` symbol). The superseded rest-mass-sourced mechanism does not live here — it lives in the gravity forks, which C6 migrates precisely because a rejected alternative is the falsification record. The ledger's `code:` note now says so, so the next reader does not go hunting. Same shape as C4's σ-bilinear finding: the code-level cleanup had already happened at F64/F106/F178.

## Wiring

**46 import statements in 27 `src/` files** rewired from bare kernel names to engine paths, alias always preserved so no downstream reference changed. **Five string-loaded references** were fixed by hand, because neither the import rewriter nor the C3.4 shim checker can see a string: `fields/entanglement.py` (the item C4 handed to C6), `fields/strong.py`'s `_PATHS` (`ca_dual_gl_backreaction`, the last bare name C4 left), `engine/core/entanglement_register.py::_QN`, and both lazy loaders in `casim/gravity/__init__.py`. The gravity ones mattered most: they resolve inside `try/except → None`, so at C9 they would have failed **silently** into a `None` module rather than raising. All five verified to resolve to their engine module. `ca_curved` (C3's) was fixed in the same statement as `ca_emqg` since they share the loader.

**Constants provenance repointed — 49 `Site`/`MeasuredConstant` paths** in `constants/{geometry,gravity,measured,strong}.py`. This was a real C6 obligation: a `Site(kind='import')` records *which file imports the constant*, and after migration that file is a shim that imports nothing, so the registry was describing a migration that had un-happened. C2's gate caught it exactly as designed — 15 unverified import sites and 5 rogue literals (the literals had been *exempted* by path-matched `MeasuredConstant` records, and the exemption stopped matching when the path changed). After repointing: **rogue literals 5 → 0, and every remaining unverified site belongs to C5.**

## Registry (D11) and reachability

- `engine_module_files()` now **walks** the sector tree instead of listing one level. Forks land a level deeper, and a one-level listing would have reported full coverage while seeing none of the 46 forks. Coverage that cannot see a file cannot vouch for it.
- `Module` gains **`status`**, carried from the manifest, so a fork's standing (`fork_live` 24 / `fork_unclaimed` 23) is a query rather than a footnote. Every fork carries one.
- **`reachable_from` is populated** — the field the dataclass has had marked "filled at C6" since C3. `gen_module_graph.py` now runs one closure **per channel module** and credits the channel *types* it registers to everything in that closure, so the graph answers *which* channels reach a module and not merely *whether* any does.
- Both `reach` and `reachable_from` are the **union of a module's two graph nodes** — the shim (still carrying unmigrated tests' references under the old name) and the target (carrying every rewired import). Reading either alone makes a module look *less* connected after migration than before, which is backwards. `lgt_fork_A_mc` is the clean case: the shim node says `test-only`, the target is `driven` from `engine/core/tier3.py`, and `driven` is the true answer.

**P6's kernel-coverage question now has a value, not a survey:** `47 of 177` registered engine modules are channel-driven (gauge 16, core 11, lattice 8, particles 6, interactions 5, forks 1), queryable as `[m.name for m in reg.all_modules() if m.reach != "driven"]`.

One more ledger-integrity fix fell out of repointing `code:` paths: `gen_migration_manifest.py` now **aliases target → source** when indexing the ledger and the dead-code signals, so citing a module's new path cannot silently downgrade its record from `partial` to `live` or drop its `protected_symbols`. Verified: `ca_gravity` keeps `partial` + `lapse_mix_half` with the ledger pointing at the engine path.

## Verification

- **Every one of the 91 importable C6 targets imports cleanly** (the 7 `derive_*`/`run_*` entry scripts excluded). No import failures, no missing modules.
- **No C6 target contains a physics change.** Each target's diff against `git HEAD`'s source was enumerated line by line: every difference is a C1 numerics substitution (`np.fft.*` → `_fft.*`), a C2 constants substitution (literal → registry import), a C6 import re-route, a C6 depth comment, or the raytrace docstring. Nothing else. 31 of 98 are byte-identical to HEAD outright; the other 67 differ only by C1/C2 edits that were already in the working tree before C6 touched them.
- **`casim list-channels`** runs clean, 48 lines, 29 channel types — unchanged count, and the graph still finds the same 6 channel modules / 29 types.
- **`make gate`**: every check green **except four, none of which is a C6 code change** —
  - *module registry coverage* and *supersession orphan banner* → both name **C5 files** (`engine/particles/_results_path.py` has no record; `engine/particles/derive_generator_norm.py` carries a banner the ledger no longer points at, because its ledger path still says `ca-simulation/`). C5 was live in the same repo throughout this session and these are its two remaining items — the same repointing C6 did for its own ledger and constants paths.
  - *constants ratchet / unverified import sites* → 11 remaining, **all C5's** (`ca_nuclear`, `ca_meson`, `ca_element`, `ca_dirac_bcc`, `ca_eg_sextic_coupling`, the two `derive_*` scripts). C6's own 15 are fixed and the gate's rogue-literal count is 0.
  - *`test_backend::test_ca_fft_alias_delegates_to_the_active_library`* → the pre-existing failure C2, C3 and C4 all recorded: it asserts `ca_fft == np.fft` bit-for-bit, which only holds when numpy is the active FFT library, and the vendored env makes scipy active. Still the numerics seam's to decide.
- **Result artifacts.** Verification runs rewrote a number of JSONs; classified against HEAD with the project's own machine floor: 5 timing-only, 5 round-off-floor, and **4 with real numeric movement**. Two are the documented pre-existing pair (`F233`, `wmu_phase3`). The third, `F144_route_a_alpha_s`, moves by 6.7 × 10⁻⁸ and is **C2's**, not C6's: `running_alpha_s.py`'s `A_OVER_LP` is now the exact closed form where HEAD had the 6-significant-figure `6.59782`, which is precisely the discrepancy C2's own acceptance gate flagged in advance. It is deterministic (run twice, identical), so it is a baseline that C2 changed and did not regenerate. Same origin for the five floor-level moves.

## The one red flag that is not C6's

**`test_FG3_quark_electroweak` is 3/6 and its committed baseline says 6/6** — `QE1_cold_w_regression`, `QE4_norm_conservation` (norm drift 0.99) and `QE6_colour_charge` now fail. This is not round-off; it is a structural break, and it is worth someone's immediate attention. It is **provably not C6's**: the test imports only `ca_dirac` and `ca_strong`, and a transitive-closure query over the module graph returns **no C6 module** in its import closure. Owners are `ca_dirac` (C5, migrated 16:06 today) and `ca_strong` (C4). Reproduced twice from a clean checkout attempt.

## For Ben / handoff

- **C7 (test registry) is next on the critical path** and is now unblocked: all physics is in `casim.engine`. C8 needs C3+C6+C7.
- **Two C5 items** are still open in the shared gate (`_results_path.py` registration, `derive_generator_norm.py` ledger path). If C5's session ended before doing them, they are two small edits — the pattern is in this document.
- **`FG3` 3/6.** Please look at this one first. Not C6's, but it is the most serious thing visible in the tree.
- **`F144` and the five floor-level baselines** need a decision from C2's owner: re-baseline to the exact closed forms, or record the truncation deltas as expected.
- **C1 left two files** in `ca-simulation/` (`benchmark_jax.py`, `ca_lazy.py`, both `sector: numerics`). C9's "only shims" precondition needs them moved.
- **For C9:** the four `OUT = dirname(__file__)` forks still write JSON beside themselves inside `src/`, and 20 `"..'"`-counted repo-root walks are depth-coupled. Both are documented above and neither blocks C7.
- The git index was locked by the concurrent session for most of this session, so **result-artifact noise could not be fully restored to HEAD**. `git checkout -- test-results/` once no other session is running; nothing there is a C6 change.
