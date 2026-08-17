# C7 completion overview — the test registry (D9)

*2026-07-30 - 19:30. Phase C7 of `docs/roadmaps/roadmap-casim-consolidation.md`. Entry state: C0–C6 complete; gate red at entry on one pre-existing check; 345 test files, 321 doing physics at import, 232 with no `assert`, 70 with no failure mode by any mechanism. Verified in FULL mode with the vendored scipy/pytest env (`source .vendor/activate.sh`).*

## Sector claim

Claimed **before anything was touched**, per C3's handoff rule:

```yaml
claims:
  tests:
    session: vibrant-charming-cannon
    phase: C7
    claimed: 2026-07-30 - 22:49        # UTC
```

The claim states plainly that `tests` is **not a module sector** — it covers `tests/**`, `tests/registry/`, `src/casim/tests/`, `tools/audit_tests.py` and the pytest collector, and touches no `modules:` record. That mattered: two other sessions were live in this repo during C7 (`nifty-great-volta`, whose C6 `interactions`/`forks` claim is still open, and `bold-sweet-turing`), and their compiled `.pyc` paths kept surfacing in pytest warnings. **No file inside a claimed sector was written.** The claim survived a full `tools/gen_migration_manifest.py` regeneration, which is the property C0 built for.

## What landed

### C7.1 — the record format and the loader

`src/casim/tests/registry.py` + `runner.py`, and `tests/registry/{core,lattice,gauge,particles,interactions,forks,suite}.yaml`.

| | count |
|---|---|
| test files on disk | 346 |
| registry records | **349** (346 files + 3 registry-only scenarios) |
| files with no record | **0** |
| `assertion` | 82 |
| `result_dump` | 226 |
| `scenario` | 3 |
| `legacy_script` (declared debt) | **38** |
| `gate` tier | 16 |

Field ownership copies the migration manifest's convention exactly: `evidence:` is generated and rewritten on every run; every other field is human-owned and preserved across regeneration, keyed by `path:`. `make registry-gen` is safe to re-run at any time.

**The teeth are in `validate()`, not in a convention.** A record that claims `assertion`, `result_dump` or `scenario` while having no way to fail does not load — the gate goes red and names it. A test may be falsifiable, or it may be *labelled* debt. There is no third state a record can express, which is the structural closure of P1's honest PARTIAL on "zero tests in RAN limbo".

### C7.5 — where the 70 unfalsifiable tests actually went

This is the phase's real finding, and it was not what the roadmap expected.

P1 measured 70 tests with **no failure mode by any mechanism**. But 57 of them *do* write numbers into `test-results/`, and those files are *already committed*. The results manifest could not see it because its strongest signal is filename-stem identity (`F107_x.json` ↔ `test_F107_x.py`), and these files write under unrelated names:

```
tests/priority/test_09_GR4_mercury.py   ->   test-results/top10_T09_GR4_mercury.json
tests/findings/test_FG7d_baryon_singlet.py -> test-results/FG10_baryon_singlet.json
```

Reading the artifact path **out of the source** turns an inference into a declaration, and a declared, committed artifact is a baseline diff — a real failure mode, with no edit to the test. Two acceptance rules, recorded per artifact in `evidence.artifact_rule` so the call is auditable:

- `local` — a write call sits within 8 lines of the literal;
- `file` — the literal is a module constant (`RESULTS = os.path.join(..., "F106_psi_K_sourcing.json")`, dumped 90 lines later) and the file writes *something*.

Rule `file` is only safe because of the **mtime guard**: if a run does not actually rewrite an artifact the record names, the result is `SKIP` ("nothing was actually compared"), never `PASS`. Without that guard a wrongly-declared baseline would read as green forever — the working-tree copy simply *is* the committed one. A wrong guess now costs a skipped record, not a false pass. `su3-noether` is the live example: it declares `V13_su3_noether.json`, does not rewrite it on a plain run, and reports `SKIP` with the reason.

Net: **declared debt 68 → 38**, and `no_assert` 232 → 231, `import_time_work` 321 → 320.

### C7.2 — selectors, and `--param` as a first-class operation

```
casim test --tier gate            --kind scenario   --sector particles
casim test --finding F234         --exactness exact --id <record-id>
casim test --id F234-Wvc-triple-closed --param delta_star=0.2
```

The sweep is the ask's core, and it works end to end:

```
[SWEEP] F234-Wvc-triple-closed   — 1 drifted artifact(s) vs HEAD
   15 delta(s) — ~ all_pass: 1.0 -> 0.0; ~ checks.C1_derived_cos3delta.cos_3delta_star …
```

Perturbing δ\* from 2/9 to 0.2 flips the closure's own verdict and moves 15 numbers — a sensitivity statement about a founding principle, produced by a CLI flag rather than a copy-pasted script. `--param delta_star=2/9` reports **no drift**, so the exact-rational path round-trips.

**A sweep never writes a baseline.** Swept output lands in a temp dir and is diffed in memory; `test-results/F234_Wvc_triple_closed.json` was verified untouched after the sweep. A tool that let a perturbed run overwrite the accepted values would quietly move the project's numbers.

To make that record sweepable, `tests/findings/test_F234_Wvc_triple_closed.py` lost its two module-level literals (`DELTA_STAR = 2.0/9.0`, `B_F95 = -5.69e-2`) in favour of `casim.constants` + keyword arguments. That was **the third local redefinition of δ\*=2/9**, named explicitly in the roadmap's C5 scope. The unparametrised run reproduces its committed artifact exactly, so the refactor moved no number.

### C7.3 — pytest delegates, structurally

`tests/conftest.py` gained `pytest_ignore_collect`: a record at `tier: archive` is not collected (replacing P0's `superseded` marker with a registry field), and a record naming an `entry:` is not collected *as a file* — it is executed as an entry point by `tests/casim/test_registry_entries.py`. So nothing can run twice under two contracts, and `tests/casim/test_registry_integrity.py` asserts the converse: every file pytest collects has a record, and the registry's `gate` tier **is** the default pytest scope.

Verified as identical sets, not as similar numbers:

| | result |
|---|---|
| `pytest tests/casim -m "not superseded and not slow"` | 121 passed, 1 skipped |
| `casim test --tier gate` (16 records) | 15 PASS + the same 1 skip inside `registry-entries`; per-file pass counts sum to 121 |

`tools/run_gate.py`'s three hand-coded scenario smoke runs are now `kind: scenario` records; the gate calls `casim test --tier gate --kind scenario`, so the tick counts live where every other test parameter lives, and `casim test` exits 1 on an empty selection — deleting the records cannot quietly stop the smoke test.

### C7.6 — retirement: one file, and that is the answer

`tests/findings/test_F114_dielectric_black_hole.py` → `deprecated/tests/`, with the ledger `path:` repointed (so `make supersessions`, which asserts every ledger path exists, and `apply_supersession_banners.py --check` both keep covering it) and its banner restamped in place.

**One of 347.** The ledger classifies 14 test files; exactly one is `fully_superseded`. The other thirteen stayed: eleven partially superseded — a dead verdict wrapped around live, load-bearing algebra — one deliberate `historical_baseline`, and `test_F91_pairing_classification.py`, which *is* the supersession authority for the chiral→even gluon migration and would have been the most expensive possible thing to retire. P0.4's measured lesson, applied rather than restated.

### C7.4 — import-time physics, by construction

A registry entry names a module *and* a function, so physics at import is impossible for a migrated record. The two new gate-tier test files were written to that standard themselves (no module-level calls or comprehensions), which is why `import_time_work` **fell** by one instead of rising by two — the ratchet's own documented blunt edge (every test needs a `sys.path` preamble) was not fed.

## Two defects found, one fixed and one recorded

**Fixed — `test_backend.py::test_ca_fft_alias_delegates_to_the_active_library` was red at entry.** It asserted `array_equal(backend.fftn(a), np.fft.fftn(a))`: bit-identical agreement with **numpy**, on a repo where P2.1 made `pyfftw` installable and C1 routed the `ca_fft` alias through `casim.numerics`. FFTW and numpy differ in the last bits by construction — `casim backend --bench` prints that difference — so the assertion tested "the alias resolves to numpy", the opposite of both its name and of what C1.1 built. It now asserts bit-identity against `casim.numerics.fft` (which *is* exact — same object) and agreement with numpy to the `machine` bound of 1e-12. This is C1's own risk row arriving as a red test.

**Recorded — the baseline diff had to adopt the machine floor.** The first real `result_dump` run reported drift on `F91_pairing_classification.json`: `S_even 4.44e-16 → 0.0`, `norm_drift 6.0e-15 → 4.9e-15`. Both sides are below 1e-12, i.e. indistinguishable by this project's own `machine` class, and `casim.baselines` documents exactly this trap ("a residual moving 2.1e-14 → 2.9e-14 is a 27% relative change and pure noise"). The runner now passes `floor=MACHINE_FLOOR` by default and **reports sub-floor deltas separately instead of dropping them**; a record that genuinely cares sets `expect: {strict_floor: true}`. The rewritten artifact was restored to HEAD rather than accepted.

## Acceptance gate C7 — item by item

| Criterion | Verdict |
|---|---|
| Every test file has a registry record; coverage assertion in `make gate` | **MET** — 0 unregistered; `tools/check_test_registry.py` + `gen_test_registry.py --check` wired into the gate |
| `pytest` and `casim test --tier gate` produce identical pass/fail sets | **MET** — verified as sets, and enforced by `test_registry_integrity.py` rather than re-checked by hand |
| `casim test --param k=v` runs a record at a perturbed value and reports the drift | **MET** — demonstrated on F234; baseline verified untouched |
| `legacy_script` count recorded and falling | **MET** — new fourth ratchet key at **38** (from 68 at scaffold) |
| `unfalsifiable` at 0 for migrated entries | **MET structurally** — `validate()` refuses a migrated record with no failure mode; the manifest-derived counter is deliberately left at 70 (see below) |
| `import_time_work` strictly below 320 | **NOT MET — 320, not below it.** The count fell 321 → 320 (one retired file). The structural fix exists; converting the remaining ~300 files is the second C7 session's work, exactly as P1 chose the ratchet over a rushed 320-file refactor |
| Perturbing a registry constant fails a named, countable set of registry IDs | **MET** — reported by ID |
| Dead tests in `deprecated/tests/` with a ledger reason each | **MET** — one file, one reason, index table populated |
| `make gate` green before and after | **NOT MET, and not C7's** — see below |

**On the gate.** 18 checks; 17 pass. Verified **check by check rather than in one `tools/run_gate.py` run**, because this sandbox kills any single command at 45 s and the full gate takes longer — including the two new registry checks, `pytest tests/casim` (121 passed, 1 skipped), and the literal command the gate now issues for the scenario tier (`casim test --tier gate --kind scenario` → rc 0; an empty selection → rc 1, so the smoke test cannot vanish silently). The failure is `no src code imports a ca-simulation shim path (C3.4)`: **52 shim imports, 23 in `engine/interactions/` and 29 in `engine/forks/`** — both sectors claimed by the *still-open* C6 session. The count was 52 at entry and 52 at exit; C7 added none and deliberately did not touch those files, because fixing them would mean writing inside another live session's claim, which is the one thing the concurrency rule forbids. The two staleness failures that *were* C7's (`manifest.json`, `module-graph.json`) are regenerated and green.

**On `unfalsifiable` staying at 70.** It would have been easy to redefine the counter against the registry and report 70 → 38 as progress. That would make the number improve without any test improving. The P1 counter keeps its manifest-derived definition; the registry's number is printed beside it, and `tools/gen_manifest.py`'s stem heuristic is scheduled for deletion at **C8.1**, where the declared mapping replaces it and the drop becomes real.

## Deviations from the roadmap sketch, recorded

1. **`sector` uses the module-sector vocabulary** (`core|lattice|gauge|particles|interactions|forks|numerics|suite`), not the sketch's `sector: lepton`. C8 joins this registry to the module registry (D11); two meanings of "sector" would break both queries. The physics grouping the sketch wanted is `--finding`, which is exact rather than inferred. Records with no import evidence at all (96 files are self-contained sympy/numpy derivations) get their sector from **the sector of the modules that own their finding** — a D11 join, not a guess.
2. **`expect: {gates: all}`** was added as an explicit sentinel for the scenario kind, meaning "every observable this scenario declares a tolerance for". An empty `gates: []` gates nothing, and validation rejects it — which it did, on the first attempt.
3. **`DEBT` and `SWEEP` are status values**, not variations of PASS. A `legacy_script` record that exits 0 is `DEBT`: P1's `RAN` limbo, renamed to what it is and counted.

## Handoff

*Updated 2026-07-31 - 09:45 by the C7 close-out pass (same session). The three items below were the open list; two are now done and one is measured. See the "C7 close-out" section at the end of this document.*

- ~~**Arm the promotions.**~~ **DONE** — all 226 run and decided: 164 armed, 9 demoted, 44 undecided (too slow for this sandbox), 9 environmental errors.
- ~~**The 38 remaining debt records.**~~ **DONE as a decision, not as work** — every debt record now carries its measured category and the action that clears it.
- **`import_time_work` 320 → 0** — still open, still mechanical: give each file an entry function and name it in its record.

---

# C7 close-out — the arming pass

*2026-07-31 - 09:45. Executes the three handoff items above; `tools/arm_test_registry.py` is the new tool.*

## The promotions are now tested, not inferred

C7 promoted 226 records to `result_dump` on *evidence* — the artifact path appears in the source and the file writes something. Evidence is not proof: a record is armed only when a run actually rewrites the baseline it declares, and the runner's mtime guard reports the rest as `SKIP` rather than a false `PASS`.

`tools/arm_test_registry.py` runs each record and writes the verdict to a journal after every single one, so the pass survives a sandbox that kills any command at 45 s. **All 226 are decided:**

| Verdict | Count | Meaning |
|---|---:|---|
| `armed` | **164** | a run rewrote the declared baseline and the numbers were diffed against HEAD |
| `unarmed` | **9** | the run never touched it — the promotion was wrong, demoted back to `legacy_script` |
| `timeout` | **44** | this sandbox could not wait. **Not a verdict about the record** |
| `error` | **9** | crashed or environmental (5 are `poisson_open`/`ca_lattice` imports killed with exit −9, i.e. memory) |

`timeout` is deliberately a fourth state rather than folded into `error`, and retries are opt-in (`--retry-timeouts`), because re-attempting the same two slow scripts every sitting consumed the whole budget and decided nothing.

**`legacy_script` went 38 → 47, and that is a retraction, not a regression.** The ratchet refused the raise until a reason was supplied — a new `--reason` requirement on `--update-baseline`, stored in the baseline file's `history`, because a ratchet whose high-water mark can be raised silently is not a ratchet. The count went up because it is now *measured* rather than inferred from a source-text heuristic.

## What the arming pass found

**12 armed records FAIL on drift against their committed baseline** — a real failure mode doing its job on the first run it ever had:

`F111-tree-gauge-su3-ladder`, `F182-friedmann-pressure`, `F185-rotation`, `F186-shadow-raytrace`, `F192-vacuum-energy`, `F205-sterile-qke-boltzmann`, `F241-omega-lambda-residual`, `F87-charge-coupling-paired-photon`, `FA-vs-FC-comparison`, `FB11-condensate-angle`, `FG2-quark-complex-mass`, `FG3-quark-electroweak`.

Only `F192` was previously known. **Eleven of these were invisible before C7**: no assertion, no linked artifact, exit 0, scored `RAN`. `FG2` and `FG3` are the pair C5 identified as having stale committed baselines by re-running against a pristine `git archive` — this reproduces that conclusion from the other direction.

**And six of the seven artifacts the C5/C6 changelogs recorded as "pre-existing drift" turn out to be stale working-tree copies, not physics changes.** Their own records ran and reproduced HEAD byte-for-byte (`F144-route-a-alpha-s`, `F233-mass-scale-N-transmutation`, `wmu-phase3` PASS; the three `casim_*` scenario JSONs likewise). `make drift` is now **clean** — 0 files with numeric drift, from 7 at session start. That is the first time this repo's drift check has been green.

**The tree is left as it was found.** An arming run rewrites the committed baseline in place — that is how the P1.2 diff works — so `--restore` puts every artifact the pass touched back to its HEAD content and the drift lives in `test-results/arming-journal.json` instead. That mattered more than expected: restoring only the *failures* left **14 files** modified by sub-floor rewrites, because the runner calls a change below 1e-12 noise (correctly) while `tools/check_result_drift.py` runs strict and calls the same file drifted. Restoring everything the pass touched is the only consistent rule, and finding that took a second look at `git status`.

## The 47 debt records are now three decisions, not one backlog

`tools/gen_test_registry.py --classify-debt` writes a measured category into every record, one-way:

| Category | Count | What clears it |
|---|---:|---|
| demoted by arming | 9 | needs a real entry function, or accept it as exploratory |
| `absent_artifact` | 11 | run once, review, `git add` the artifact, then `--promote`. **Cheapest** |
| `emits_nothing` | 27 | needs an `assert`, or an entry function returning a dict |

## Still open after this pass

- **40 timeouts + 9 errors** — undecided arming verdicts. Resume on a machine without a 45-second ceiling: `python3 tools/arm_test_registry.py --budget 36000 --timeout 900 --retry-timeouts`, then `--restore`, then `--apply`. The 5 exit−9 errors need memory, not patience.
- **The 15 drift FAILs** need a physics owner each: accept the new number (`git add`) or find the regression. `FG2`/`FG3` already have C5's analysis pointing at stale baselines.
- **`import_time_work` 320 → 0**, unchanged and mechanical.

## Update — 2026-07-31 - 09:55: the gate is green

Two things landed after the close-out was written.

**C6 released its claim and the shim imports are gone.** `tools/check_shim_imports.py` reports *"no src/casim file imports a migrated shim path (C3.4)"* — 52 → 0. `claims.interactions`, `claims.forks` and a late `claims.numerics` are all released (2026-07-31 - 14:30 UTC). **Every gate check now passes**: provenance 3/3, test-suite health 6/6 (including `casim index --check`), migration readiness 6/6, `pytest tests/casim` 128 passed / 1 skipped, gate-tier scenario records 3/3. The one red that C4 through C8 each recorded is closed, and it was never any of theirs.

**The arming pass was continued off-sandbox**, which is what the tool was built for: `F184-tabulated-ns` (14 s) and `run-bgfield-loop` (145 s) — both `timeout` here — came back **armed and FAILing on drift**. That takes the journal to 168 armed / 9 unarmed / 40 timeout / 9 error and the drift-FAIL list to **15**. Both runs left their rewritten artifacts in the tree; `--restore` put all 233 touched baselines back to HEAD, and `make drift` reports *"no tracked result JSONs differ from HEAD"* — a stronger statement than the earlier "clean", because now not even a formatting-only change remains.

The lesson worth keeping: **`--restore` is not optional and is easy to forget.** A continued sitting on another machine armed two records and left two modified baselines behind; the drift checker caught them within minutes because it runs strict. Run `--restore` after every sitting, before `--apply`.

**C8** consumes both registries and is unblocked: `tests-index.md`'s prefix heuristic can be deleted outright (the mapping is declared, and `evidence.artifacts_written` covers the secondary artifacts the heuristic capped at two), `code-index.md` gains the join, and `expect.exactness` standardises the class vocabulary that blocked P1.5.

*Correction (added during C8, 2026-07-31): this section originally claimed "84 records currently declare one". **The true figure at C7 exit was 4** — the F234 record and the three scenario records, i.e. only the ones C7 hand-authored. The number was written from memory and not measured, and C8 measured it at 4 on the first query. C8.4 therefore could not lean on `expect.exactness` alone and added two further classification rules (see `docs/status/C8-completion-overview.md`); the field's value is that a declared class **cannot be outside the closed vocabulary**, not that many records had one yet.*

**Not done, and needing its own owner:** the 52 C3.4 shim imports in `interactions/` and `forks/`. They belong to C6's claim and block the gate for everyone until that session releases.

*Cross-references: `docs/roadmaps/roadmap-casim-consolidation.md` §C7, `docs/status/P1-completion-overview.md`, `docs/status/C6-completion-overview.md`, `docs/theory/supersessions.yaml`, `deprecated/tests/README.md`, `src/casim/tests/registry.py`.*
