# C0 Complete — Migration Instrumentation

*2026-07-30 - 11:40. Phase C0 of `docs/roadmaps/roadmap-casim-consolidation.md`.
Follows `docs/status/P0-completion-overview.md` and `P1-completion-overview.md`.*

`make gate` — 14 checks, 14.9 s. `make c0` rebuilds the whole readiness layer.

C0 moved no physics. It built the four instruments that phases C1–C9 execute
against, and the rule that stops any of them from moving a file the tooling
cannot account for.

---

## What existed before

| | Before C0 | After C0 |
|---|---|---|
| Where a module belongs after migration | prose in a roadmap | **171 declared target paths**, one per file, validated |
| Import/reachability map | an audit's prose claim | `docs/design/module-graph.json` — 571 files, edges, three reachability criteria |
| Dead-code evidence | keyword grep | 3 independent signals, reported separately, **never applied** |
| Moving a module | manual copy + hope | atomic, journalled, **rolls back on baseline drift** |
| `deprecated/code`, `deprecated/tests` | did not exist | exist, with enforced acceptance rules |
| Gate checks | 10 | 14 |

---

## Deliverables

### C0.1 — Module graph (`tools/gen_module_graph.py`)

AST inspection, never import — P0.2's rule, for the same reason: importing a
`tests/findings` module executes its physics and rewrites JSON, which would
corrupt the very baselines C0.4 depends on.

571 files scanned: 171 migratable (107 kernels, 47 forks, 12 derivations, 5
support), 47 package modules, 344 tests.

**Four things a naive import scan gets wrong, and what each was worth:**

- **The `casim.fields.*` shims import by string.** They call
  `importlib.import_module(_m)` over a list of literals, so an `ast.Import`
  walk sees nothing at all. String literals matching a known module name are
  collected as a separate, weaker `dynamic` evidence class — **27 edges** that
  would otherwise not exist. `ca_maxwell` is reachable *only* through one of
  them.
- **Forks are imported under two names.** `tests/findings` uses both
  `import forks.lgt_fork_A_mc` and bare `import lgt_fork_A_mc`, depending on
  which directory the file put on `sys.path`. Without the alias, **46 of 47
  forks scanned as unreferenced** — a wrong answer that would have proposed
  deleting the project's negative results.
- **A `derive_*.py` is not a library.** Ten derivation scripts plus the
  `run_*`/`benchmark_*` entry points are meant to be executed. "Nothing imports
  it" is their normal state, so they carry role `derivation` and are counted
  apart; that is what keeps the `unreferenced` bucket down to genuine suspects.
- **Reachability has three defensible definitions.** All three are reported and
  the least flattering is the headline.

**The number, and an independent check on it.** Of 107 kernels, **39 are driven
by a registered channel and 68 are not**. `ca_bcc_gauge.py` was added on
2026-07-29 and is driven; at the tree the `2026-07-29` kernel-coverage addendum
measured, that is **67 of 106** — reproducing the addendum's figure exactly, by
a different method. `ca_cooling` resolves correctly as *driven*: it reaches a
channel only transitively through `forks/lgt_fork_A_mc`, which is the case the
addendum flagged as invisible to a direct-reference scan.

### C0.2 — Dead-code proposer (`tools/find_dead_code.py`)

**Proposes; never acts.** Nothing writes to a source file, and nothing enters
`dead_symbols` without a human. Three signals, reported separately and never
summed.

| Signal | Result |
|---|---|
| 1. unreferenced files | 17 |
| 1. unreferenced symbols **(proposed)** | 81 |
| 1. module-private helpers (used internally — *not* proposed) | 957 |
| 1. ambiguous (name defined in >1 module — *not* proposed) | 577 |
| 2. ledger-named paths | 9 |
| 2. candidate dead symbols | 2 |
| 2. protected symbols (from `retained:`) | 4 |
| 3. modules reachable only from tombstoned tests | 0 |

**The first version of signal 2 was wrong in an instructive way.** It matched
any word that was also an identifier somewhere in the tree, and proposed
`Omega`, `energy`, `metric`, `shape`, `delta`, `weight`, `series` and `order`
as dead — every one an ordinary English word in a ledger sentence colliding
with a local variable in some test. That is exactly the false-positive class
P1 named when `total_elapsed_s` was flagged as physics drift: the kind that
trains people to ignore the checker. A token now has to look like a deliberate
code reference (dotted, or ≥2 underscores) *and* be defined in a migratable
file. Candidates fell from 24 to 2, and both survivors are real.

**And it got the one pair that matters backwards.** `scope:` and `code:` notes
in ledger record S2 name `gluon_rotation_step_spectral_bcc` (canonical, even,
F91) and `..._bcc_chiral` (retained for comparison) in the *same sentence*; the
extractor proposed the **canonical** propagator as dead. That cannot be
resolved from prose, so it is now flagged — a `sibling_of_protected` field
fires when a candidate shares a prefix with a `retained:` symbol, and the
report says **DO NOT GUESS** rather than picking.

Signal 3 is empty, and that is the expected answer: exactly one test in the
project is fully superseded and no kernel depends solely on it.

### C0.3 — The migration manifest (`docs/design/module-migration-manifest.yaml`)

**171 records, full coverage, validated.** The roadmap's real product; C1–C9
execute it and a file with no record does not move.

Split deliberately in two:

- **Classification is hand-authored** in the `SECTOR` table of
  `tools/gen_migration_manifest.py`. Which subpackage a module belongs to is a
  judgement about physics, and the roadmap requires it be settled "once, on
  paper, not 40 files into a migration."
- **Evidence is generated** — reachability, tests, baselines, np/scipy/FFT call
  sites, constants, dead-code proposals, ledger records — so it cannot drift
  from the tree without `--check` noticing.

| | |
|---|---|
| by phase | C1 3 · C3 18 · C4 31 · C5 21 · C6 98 |
| by sector | interactions 51 · forks 47 · gauge 31 · particles 21 · lattice 12 · core 6 · numerics 3 |
| by status | live 113 · fork_live 24 · fork_unclaimed 23 · partial 8 · dead_candidate 3 |
| accepted dead symbols | **0** (81 proposed, awaiting a human) |

**Two data-model decisions carry the P0.4 lesson rather than restating it.**

`dead_symbols` is human-accepted and starts empty; `dead_symbols_proposed` is
advisory and `migrate_module.py` never reads it. And **forks are classified
before the structural signal runs**, so a fork can never be labelled
`dead_candidate` — a fork nothing imports is the normal end state of a fork,
because it was an alternative that got tested and rejected, and that rejection
*is* the falsification record.

`status: partial` is the common case, not an edge case: the ledger names the
file but did not kill it. `derive_generator_norm_from_F118.py` lands there
rather than in `dead_candidate`, despite having no `__main__` and no importers
— which is the outcome the roadmap named as its worked example.

### C0.4 — Atomic migration (`tools/migrate_module.py`)

Seven journalled steps; every filesystem effect is undone in reverse on any
failure, including a baseline drift.

Two bugs found by running it rather than reading it:

- **It reported "no drift" having run zero tests.** The test was skipped
  (pytest absent), the artifacts were therefore unchanged, and the summary line
  said clean. That is the P0.5 failure mode verbatim — `casim test` skipping
  every pytest file and still reporting success. A skip now aborts the
  migration unless `--allow-no-tests` is passed explicitly.
- **`"__main__" not in src` is the wrong test for how to run a file.** P1.3
  measured that 320 of 344 test files do their physics at module level, and
  many end in a bare `sys.exit(0 if PASS else 1)` with no guard.
  `test_P6_si_scale.py` is one; handing it to pytest gives
  `INTERNALERROR ... caught unexpected SystemExit`, which the migration read as
  a failed physics test. Runner selection is now AST-based: any top-level
  statement that is not an import, a definition, or a constant is module-level
  work, and a file with module-level work is a script.

### C0.5 — `deprecated/code/` and `deprecated/tests/`

Both created with their rule stated, and the rule **enforced** by
`tools/check_deprecated.py` in the gate — a README is a suggestion otherwise,
and the entire point of those directories is that a file cannot be quietly
parked in one.

`deprecated/tests/` has the higher bar: a file moves there only with
`status: fully_superseded` in the ledger. Today exactly one file in the project
qualifies.

---

## Acceptance gate — verified

| Roadmap criterion | Result |
|---|---|
| Manifest covers 171 of 171 files; assertion in `make gate` | **PASS** |
| Every target unique, every sector/phase known | **PASS** |
| One trivial leaf module migrates end-to-end, gate green, drift clean | **PASS** — `ca_si_scale.py`; shim re-exports all 15 symbols; `test_P6_si_scale.py` 10/10 through the shim; zero deltas vs git HEAD |
| `--rollback` restores the tree exactly | **PASS** — source back to md5 `6fd1767a…`, target and backup removed, manifest stamp cleared |
| A corrupted clean aborts rather than landing | **PASS** — see below |

**Five negative tests, all run against the live tree, tree restored after each.**

| Test | Result |
|---|---|
| Accept a live symbol (`canonical_cell`) as dead | `NameError` at test time → **abort + rollback of all 5 actions** |
| Accept a ledger-`retained:` symbol (`gluon_rotation_step_spectral_bcc_chiral`) | **refused before touching anything** |
| Perturb a physics constant (`F_PI_PHYS` 92.07 → 92.40) | **BASELINE DRIFT**, six quantities named, rolled back |
| Add a file with no `SECTOR` entry | manifest `--check` exit 1, names the file |
| Point two sources at one target | manifest `--check` exit 1, names both |
| Park an unaccounted file in `deprecated/code/` | `check_deprecated` exit 1 |

---

## Two pre-existing bugs fixed in passing

Both surfaced because C0's work made the gate run in a second environment.

- **`test_resume_bit_identical(tmp_path="/tmp")`** — pytest does *not* inject a
  fixture for a parameter carrying a default, so the default silently defeated
  the `tmp_path` fixture and every run in the project's history wrote its
  checkpoint to a shared, world-writable `/tmp` under a fixed name. Now `None`,
  with a private temp dir for the standalone path.
- **`run_gate.py` wrote scenario smoke output to fixed `/tmp/gate_<name>.json`.**
  Two users or two sessions on one machine collide, and the second gets
  `PermissionError` from the gate rather than from anything real. Now a private
  `mkdtemp`, removed after.

---

## Files

**New**

```
tools/gen_module_graph.py            C0.1  imports, reachability, sizing
tools/find_dead_code.py              C0.2  3-signal proposal (never applied)
tools/gen_migration_manifest.py      C0.3  hand-authored SECTOR table + evidence
tools/migrate_module.py              C0.4  atomic 7-step migration + rollback
tools/check_deprecated.py            C0.5  enforces the deprecated/ rules
docs/design/module-graph.json
docs/design/dead-code-proposal.{json,md}
docs/design/module-migration-manifest.yaml
deprecated/code/README.md
deprecated/tests/README.md
docs/status/C0-completion-overview.md
```

**Modified**

```
Makefile                                     c0 / graph / deadcode /
                                             migration-manifest / migrate
tools/run_gate.py                            4 migration-readiness checks;
                                             private smoke temp dir
deprecated/README.md                         layout + acceptance rules
tests/casim/test_engine_reproduces_kernels.py  tmp_path fixture fix
```

Indexes regenerated. **No physics module's behaviour changed; no file moved.**

---

## Known limitations

- **81 proposed dead symbols are unreviewed**, by design. They are evidence for
  C4–C6 to work through file by file, not a backlog C0 was meant to clear.
- **The `SECTOR` table is a first pass.** 171 placements were made from
  `code-index.md`, the roadmap's scope lists, and the kernel-coverage addendum.
  Disagreement is cheap to fix now (edit one line, regenerate) and expensive
  later; it is worth a read before C3 starts.
- **np/scipy/FFT site counts are regex**, labelled as such in the output. They
  size C1; they are not correctness claims. Total 13,626 `np.` sites and 407
  FFT sites across the tree.
- **577 ambiguous symbols are not analysed.** A name defined in more than one
  module cannot have its references attributed, so C0 records the collision and
  stops. Resolving them needs per-module scope analysis, which is C4–C6 work.
- **Step 5 (registry registration) is staged**, not implemented — the module
  registry does not exist until C3. `migrate_module.py` says so on every run
  rather than silently skipping.

---

## Next

**C1 (numerics façade)** or **C2 (constants inversion)** — independent of each
other, both independent of C3. C1 first is marginally better: it touches every
file anyway, so C2's literal deletion rides along.

Before either, the cheap high-value read is the `SECTOR` table in
`tools/gen_migration_manifest.py`. It is the one thing in C0 that is a judgement
rather than a measurement, and every later phase inherits it.
