# Deprecated Files & Tests

Stuff that has been avoided or abandoned due to model falsification, user choices, or stale data.

## Layout

| Directory | Contents | Acceptance rule |
|---|---|---|
| *(this level)* | superseded docs, plans, and roadmaps | a dated entry below saying why |
| `code/` | pre-clean originals of migrated modules, and retired code | a `docs/design/module-migration-manifest.yaml` record, or a `docs/theory/supersessions.yaml` record |
| `tests/` | fully-superseded tests | a `supersessions.yaml` record with `status: fully_superseded` — nothing else qualifies |
| `findings/` | retired finding files | a `supersessions.yaml` record naming the file, **and** a `status: retired` entry for its number in `docs/design/finding-numbers.yaml` — both, or the number audit fails |
| `papers-v1/` | the superseded first-generation paper series | — |

`code/` and `tests/` each carry their own README with the rule stated in full
and the reasoning behind it. Both are enforced by `make gate`, so a file cannot
be quietly parked in either one.

**The standing caution, learned the hard way in P0.4:** of 14 test files an
audit called superseded, exactly one was superseded wholesale and eleven were a
dead verdict wrapped around live, load-bearing algebra. Before moving anything
here, check whether what is dead is one *check* inside the file rather than the
file.

## 2026-08-03 - 13:27 — `findings/` created; F16, F17, F18, F19 retired
Four findings retired after independent review (`docs/reviews/F1{6,7,8,9}-review-2026-08-03.md`; verdicts OVERSTATED ×3 and CIRCULAR). All four were written 2026-05-21 against structures the model has since replaced, and none carried a banner or a ledger entry until now.

- `findings/F16-gr3-fork-resolution.md` — the A/B/C fork trichotomy for the Paper-6 redshift. Closed by F64 → F178: at $O(u)$ the canonical $A=1/K$, $B=K$ dielectric **is** Fork B. Ledger `S16-F16-gr3-fork-space-closed`.
- `findings/F17-poynting-energy-conservation.md` and `findings/F18-mohr-c5-c6-build.md` — both built on the σ-bilinear composite photon that F69 retired. Ledger `S1-F69-sigma-bilinear-photon`, which gained a `findings:` block for them.
- `findings/F19-tick-area-vs-volume.md` — an unrun test spec whose statistic is bi-Lipschitz-invariant and so cannot respond to the field it probes. Ledger `S17-F19-tick-count-not-a-state-count`; answered properly by F183 + F190.

Three of the four are `partially_superseded` and the ledger records what stays live in each — per the standing caution above, none was blanket-marked. Numbers 16–19 are declared `status: retired` gaps in `docs/design/finding-numbers.yaml`.

Three things the retirement does **not** clear, left for a research session:

- **F18's twelve exactness-inventory rows are still live and unflagged**, including six with no failure mode and one double-booked with F17. That is the largest single item in the four reviews.
- **F16 is still named as provenance** by `tests/falsification/FC01-mercury-perihelion.md`, `FC03-pound-rebka-redshift.md` and their two runners. Those citations are to the *question*, which is live; the answers are in the ledger.
- **Four live findings still cross-reference F17 or F18 by name** — F20, F25, F26 and F171 (plus a prose reference in F29). The links still resolve by filename, but a reader following them now lands on a bannered, retired file, which is the intended behaviour rather than a defect. Separately, `references/special-relativity-derived-from-ca-summary.md:187` proposes creating `findings/F18-flux-rate-relativistic-mass.md`; that number is now retired and a successor must take a fresh one from the claim board.

## 2026-07-30 - 09:30 — `code/` and `tests/` created (roadmap C0.5)
Scaffolding for the CASIM consolidation arc (`docs/roadmaps/roadmap-casim-consolidation.md`). Nothing migrated yet; both directories hold only their READMEs.

## 2026-07-01 - 00:00 — Paper VIII (Dielectric Black Hole) deprecated
`Paper-08-Dielectric-Black-Hole.md` (+ its PDF) moved here: the horizon-free dielectric black hole was reclassified as a PPN-order representation artifact, not the canonical strong-field object, following adoption of the full-tensor induced Einstein equation (F178) — the exact strong-field object is Schwarzschild/Kerr (F183). Papers IX–XIII in `papers/` were renumbered consecutively to VIII–XII; see `docs/theory/key-decisions.md` for the decision record.

## 2026-06-10 - 23:01 — Repository reorganization sweep
Moved here during the docs/tests restructure (see docs/status/changelog.md, same date):
- `roadmap-P1-binding-force-options.md` — P1 decided (Option C, F86 colour-dielectric) and built; superseded by `docs/roadmaps/roadmap-matter-binding.md`.
- `si-units-options.md` — SI-scale options memo; superseded by the canonical-cell decision (F107) and `F112` SI predictions.
