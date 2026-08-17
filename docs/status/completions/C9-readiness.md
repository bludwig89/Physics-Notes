# C9 readiness — what is done, and what blocks deletion

> **CLOSED 2026-07-31 - 18:20 — C9 is executed.** All three blockers below are
> fixed, the 171 shims and the legacy directory are deleted, and the
> documentation debt is paid. The assessment is kept as written for the record;
> see the changelog entry of the same date for what actually happened, and
> `docs/theory/key-decisions.md` §"Engineering decisions" for D1–D11.
>
> Three things this assessment got wrong, worth knowing next time:
>
> - **The 268-file rewrite had judgment in it after all** — not about *where* a
>   module went (that was the table lookup this doc promised) but about *which
>   statements were plumbing*. A text-level rule deleted two enclosing `def`/`try`
>   blocks and unbound the name `casim` in ten files. The rewrite had to be
>   structural, off the AST.
> - **Blocker 2 was two lines, but three more breakages only appeared on
>   execution**: 28 tests import a fork by bare name, 4 launch a fork as a
>   subprocess with no inherited `PYTHONPATH`, and 2 drive a sibling test module
>   by bare name. Compiling all 347 files found none of them.
> - **The `import_time_work` adjacency does not hold.** The `sys.path` preamble
>   and the module-scope physics are different things; bundling them would have
>   put judgment back into a rewrite whose safety argument was that it had none.
>
> Two items this doc did not list also had to go: the **nine intra-package C3
> shims** under `casim.engine.` (each already warning "removed at C9"), and the
> five remaining `_c5_*` tools, which imported the retired migration tool.

*2026-07-31 - 11:45. Measured against `docs/roadmaps/roadmap-casim-consolidation.md` §C9 (deliverables and acceptance gate). C9 deletes `ca-simulation/`, so the question is not "is the migration finished" — it is **"what still needs that directory to exist".***

## Verdict

**One blocker, and it is large but entirely mechanical: 268 test files still import the legacy kernels.** Everything else on the C9 list is either already true or is an afternoon of doc-writing.

| C9 requirement | State |
|---|---|
| `ca-simulation/` contains only shims | ✅ **171 of 171 are shims** — every file carries the `DEPRECATED shim` banner. Nothing left to migrate |
| `deprecated/code/` holds every pre-clean original | ✅ **171 backups for 171 migrated records**, zero missing; README enumerates all 171 in a table |
| `deprecated/tests/` holds retired tests with a reason each | ✅ one file (`test_F114_…`), ledger-backed, table populated |
| No `src/` code imports a shim path (C3.4) | ✅ **0** — C6 closed this |
| `casim index` / registries / gate | ✅ green, idempotent, 0 duplicate finding numbers |
| **Tests import from `casim.engine`, not `ca_*`** | ❌ **268 files still reference `ca-simulation`** |
| `casim` imports without `ca-simulation/` present | ❌ `src/casim/__init__.py` **raises ImportError** if the directory is absent |
| Docs updated (INDEX, README, CLAUDE, src README) | ❌ not started |
| D6–D11 in `key-decisions.md`; D2 reversal in the ledger | ❌ not started; `key-decisions.md` has **zero** D6–D11 hits and the ledger has no `methodology` kind |
| C3.4 gate check removed | ❌ trivial, do it last |

---

## Blocker 1 — the test tree (the whole job)

| Suite | Files referencing `ca-simulation` |
|---|---|
| `tests/findings` | **208 of 272** |
| `tests/runners` | 38 of 45 |
| `tests/priority` | 14 of 16 |
| `tests/casim` | 7 of 14 |
| **Total** | **268** |

Two patterns, usually together: a module-level `sys.path.insert(…, 'ca-simulation')` preamble (262 files) and `import ca_bcc as bcc` (218 files). Delete the directory and every one of them fails with `ModuleNotFoundError` — which is why C9's gate says *"full battery runs"* rather than just *"make gate green"*.

**The good news is that this is a pure rewrite with no judgment in it.** 221 test files import **106 distinct** legacy module names, and **all 106 have a manifest `target:`** — so `ca_bcc` → `casim.engine.lattice.bcc` is a table lookup, not a decision. The repo has already done this three times: `tools/route_numerics.py` (C1), `tools/_c5_repoint_sites.py` (C5) and C6's import re-router. A fourth, aimed at `tests/`, is the same shape.

Three specific hazards worth knowing before starting, all learned in earlier phases:

- **The alias must be preserved.** `import ca_bcc as bcc` → `import casim.engine.lattice.bcc as bcc`, not a `from` import — C5 and C6 both kept aliases for exactly this reason, and 218 files use them.
- **String-loaded imports are invisible to a rewriter.** C6 found five (`importlib`/`__import__` with a name in a variable) and fixed them by hand; two of those failed *silently* inside `try/except → None`. Expect a handful in `tests/` too, and grep for them separately.
- **`__file__` arithmetic breaks on depth change** — C6's 19 forks wrote their artifacts into the wrong directory because a `".."` run was two levels from `ca-simulation/forks/` and five from `engine/forks/<sector>/`. Tests are not moving, so this does *not* apply here; noted so nobody re-derives the worry.

Order that keeps the tree runnable throughout: rewrite → `pytest tests/casim` → `casim test --tier gate` → one battery pass → only then delete.

## Blocker 2 — `casim` cannot be imported without the directory

`src/casim/__init__.py:50` raises `ImportError("casim could not locate the legacy 'ca-simulation' directory")` when the walk-up finds nothing, then puts it on `sys.path` unconditionally. **The moment C9 deletes the directory, `import casim` fails and the entire package is unusable** — every tool, the CLI, the gate.

Two lines to fix, but it must happen *with* the deletion, not before (the shims themselves rely on it: each one bootstraps `src/` onto `sys.path` so unmigrated tests keep working). The `casim.lattice` / `casim.fields` / `casim.gravity` compatibility packages are already fine — their `ca_*` names bind to engine modules — **with one exception**: `casim.gravity.ca_curved` still resolves to the shim module rather than `casim.engine.interactions.gravity_curved`. One line.

## Blocker 3 — the tools that legitimately scan `ca-simulation/`

Eleven `tools/*.py` reference the directory. They split three ways:

- **retire with it** — `migrate_module.py`, `gen_migration_manifest.py`, `check_shim_imports.py`, `_c5_repoint_sites.py`, `_c5_run_tests.py`, `route_numerics.py`: their subject stops existing. C9 already plans the C3.4 check's removal; the others follow the same logic and should go to `deprecated/code/` rather than be left to fail.
- **update the scope** — `gen_module_graph.py`, `audit_numerics.py`, `audit_constants.py`: they walk both trees and should walk one.
- **one real bug waiting** — `tools/run_gate.py` probes the FFT backend with `sys.path.insert(0,'ca-simulation'); import ca_fft`. After deletion the probe fails; it should import `casim.numerics.fft`. The gate would still pass (the probe's return code is not checked) which is worse than failing, because the gate would silently stop reporting which backend is live — the exact defect P2.1 existed to fix.

## Documentation debt (real, but small)

- **`key-decisions.md` has no D6–D11.** Six decisions this roadmap took — CASIM is the program, constants own values, one numerics surface, declarative tests, cleanup-and-migration as one operation, every module registered — exist only in the roadmap and the completion overviews. C9's deliverable list is right to name this.
- **The ledger needs a `methodology` kind** for the D2 reversal. Its `kind_vocabulary` is currently `superseded | reclassified | demoted | deprecated`, all physics. C9 says *extend the schema rather than overload it* — and `tests/casim/test_supersession_ledger.py` asserts `kind in KINDS`, so the test moves with it.
- **CLAUDE.md's §Project Structure and §Context change materially** — the "always load" list and the `ca-simulation/` description are both wrong after C9. §"Index maintenance" is already C8-correct, so that part is done.
- INDEX.md, README.md, `src/casim/README.md`: one or two mentions each.

## Not blockers, but they will be visible at C9

These are C7 residue. C9's gate says "full battery runs" and "`make drift` clean", so decide deliberately whether they are allowed to be red:

- **26 armed records fail on drift**, of which 11 are supersession candidates awaiting a decision and 18 are regression candidates (`docs/status/baseline-provenance.md`). One is already `stale_by_design` and reports STALE.
- **2 timeouts + 10 errors** in the arming journal — five of the errors are memory kills (`poisson_open`, `ca_lattice`), not logic.
- **47 debt records** (`legacy_script`), each carrying its measured category.
- **`import_time_work` at 320.** Worth noting: the test rewrite touches all 268 files anyway, so converting the `sys.path` preamble into a real import is the *same edit* that drops this counter. Doing them together is far cheaper than doing them apart.

## Suggested order

1. **Test-tree rewrite** (268 files, table-driven) + fix the string-loaded stragglers by hand. Combine with the import-time-work cleanup.
2. Verify: `pytest tests/casim`, `casim test --tier gate`, one battery pass, `make drift`.
3. `casim/__init__.py` — stop requiring the directory; fix `casim.gravity.ca_curved`.
4. `tools/` — retire six, rescope three, fix `run_gate.py`'s backend probe.
5. Docs — D6–D11 in `key-decisions.md`, `methodology` kind + D2 reversal in the ledger, then CLAUDE.md / INDEX / READMEs.
6. **Delete the 171 shims and `ca-simulation/`.** Remove the C3.4 check.
7. Final gate: `grep -rn "ca-simulation" --include=*.py --include=*.md .` should return only `deprecated/` and historical changelog entries.

Steps 1–2 are the phase. Steps 3–7 are a session.
