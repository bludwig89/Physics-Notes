# `deprecated/tests/` — retired tests

*Created 2026-07-30 - 09:30. Roadmap C0.5 / C7.6 (`docs/roadmaps/roadmap-casim-consolidation.md`).*

## What lands here

Test files that are **fully superseded** — every check they contain has been
replaced — or that test code which no longer exists.

## The acceptance rule

**A test moves here only if `docs/theory/supersessions.yaml` records it with
`status: fully_superseded`.** Nothing else qualifies. `make gate` asserts this.

Today exactly **one** file in the whole project meets that bar:
`tests/findings/test_F114_dielectric_black_hole.py` (replaced by
`test_F183_blackhole.py`; its one non-black-hole check, D1, is duplicated by the
live `test_F111_second_order_deflection.py` D3, so no unique coverage is lost).

## Why the bar is this high

P0.4 inherited an audit claim that ~14 test files covered superseded physics.
On inspection:

- **1** was superseded wholesale;
- **11** were *partially* superseded — a dead verdict wrapped around live,
  load-bearing algebra (F62's lapse-mix *sign convention* is production code;
  F52's factor-2 discriminator is still canonical under F178; F179's
  $3\delta^* = Q$ check is now the model's falsification handle);
- **1** was a deliberate historical baseline;
- and several were keyword false positives — `test_F91_pairing_classification.py`,
  flagged as superseded, *is* the supersession authority.

Moving those twelve would have silently retired working coverage **while
looking tidy**. So the unit of supersession is a **check**, not a file:
partially-superseded files stay in `tests/` and carry a docstring banner naming
their DEAD and STILL LIVE checks, generated from the ledger by
`tools/apply_supersession_banners.py`.

If you are about to move a file here, first ask whether what is actually dead
is one check inside it. Usually it is.

## Index

| Date | Test | Ledger record | Replacement |
|---|---|---|---|
| 2026-07-30 - 18:55 | `test_F114_dielectric_black_hole.py` | `S4-F178-full-stress-energy` (`fully_superseded`) | `tests/findings/test_F183_blackhole.py` |

**One file, out of 347.** That ratio is the C7.6 result, not an oversight: the
ledger records 14 classified test files and exactly one is superseded wholesale.
The other thirteen stay in `tests/` — eleven partially superseded (live algebra
inside a dead verdict), one a deliberate `historical_baseline`, and
`test_F91_pairing_classification.py`, which *is* the supersession authority for
the chiral→even gluon migration and would have been the most expensive possible
thing to retire.

The ledger's `path:` for a retired file is rewritten to point here, so
`make supersessions` (which asserts every ledger path exists) and
`tools/apply_supersession_banners.py --check` keep covering it after the move.
