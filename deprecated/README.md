# Deprecated Files & Tests

Stuff that has been avoided or abandoned due to model falsification, user choices, or stale data.

## Layout

| Directory | Contents | Acceptance rule |
|---|---|---|
| *(this level)* | superseded docs, plans, and roadmaps | a dated entry below saying why |
| `code/` | pre-clean originals of migrated modules, and retired code | a `docs/design/module-migration-manifest.yaml` record, or a `docs/theory/supersessions.yaml` record |
| `tests/` | fully-superseded tests | a `supersessions.yaml` record with `status: fully_superseded` — nothing else qualifies |
| `papers-v1/` | the superseded first-generation paper series | — |

`code/` and `tests/` each carry their own README with the rule stated in full
and the reasoning behind it. Both are enforced by `make gate`, so a file cannot
be quietly parked in either one.

**The standing caution, learned the hard way in P0.4:** of 14 test files an
audit called superseded, exactly one was superseded wholesale and eleven were a
dead verdict wrapped around live, load-bearing algebra. Before moving anything
here, check whether what is dead is one *check* inside the file rather than the
file.

## 2026-07-30 - 09:30 — `code/` and `tests/` created (roadmap C0.5)
Scaffolding for the CASIM consolidation arc (`docs/roadmaps/roadmap-casim-consolidation.md`). Nothing migrated yet; both directories hold only their READMEs.

## 2026-07-01 - 00:00 — Paper VIII (Dielectric Black Hole) deprecated
`Paper-08-Dielectric-Black-Hole.md` (+ its PDF) moved here: the horizon-free dielectric black hole was reclassified as a PPN-order representation artifact, not the canonical strong-field object, following adoption of the full-tensor induced Einstein equation (F178) — the exact strong-field object is Schwarzschild/Kerr (F183). Papers IX–XIII in `papers/` were renumbered consecutively to VIII–XII; see `docs/theory/key-decisions.md` for the decision record.

## 2026-06-10 - 23:01 — Repository reorganization sweep
Moved here during the docs/tests restructure (see docs/status/changelog.md, same date):
- `roadmap-P1-binding-force-options.md` — P1 decided (Option C, F86 colour-dielectric) and built; superseded by `docs/roadmaps/roadmap-matter-binding.md`.
- `si-units-options.md` — SI-scale options memo; superseded by the canonical-cell decision (F107) and `F112` SI predictions.
