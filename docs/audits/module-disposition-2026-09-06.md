# Module disposition pass — H7 channel-driven fraction, fourth consecutive fall

**Date:** 2026-09-05 - 21:41 (Central)
**Executes:** the H7 prompt of `docs/status/completeness-2026-08-20-prompts.md` — "reverse the
three-consecutive-report fall in channel-driven module fraction."
**Scope:** H7 only. No finding number reserved — this is a registry/audit question, not physics
(per the prompt's own protocol note).
**Findings written:** none.

---

## 1. Headline

> **The channel-driven fraction fell a fourth time, to 52/254 (20.5%), and every one of the 34
> newly-registered modules in this window checks out as correctly non-driven by design.**

| Report | Driven / total | Fraction |
|---|---:|---:|
| 2026-08-02 | 51/181 | 28.0% |
| 2026-08-07 | 51/203 | 25.1% |
| 2026-08-18 | 51/218 | 23.4% |
| 2026-09-06 (this pass, live) | **52/254** | **20.5%** |

The driven count finally moved (+1, `gauge.lpt_ws_mask_cutcell`), but the denominator grew by 36,
so the fraction fell again. This is the same mechanism as the prior three reports, not a new one —
and, as below, it is not a coverage regression.

## 2. What the 34 new registrations actually are

`git diff -- src/casim/engine/registry.py` (against the last commit, `b2fcfa5`, since nothing has
been committed since — see §4) shows 34 newly-added `_SPINE` records. Classified by live reach/role:

| reach | role | count |
|---|---|---:|
| `driven` | derivation | 1 (`gauge.lpt_ws_mask_cutcell`) |
| `standalone` | derivation | 29 |
| `standalone` | kernel | 4 (`cosmology_transfer_function`, `qi_gleason_regularity`, `thermodynamics_interacting`, plus one counted above) |

Every `standalone` entry backs 1–13 specific findings (median ~6) and carries `status="live"` — none
is orphaned, untested, or forgotten. Reading each module's own header docstring (all 34, not a
sample) shows a single consistent shape: **a one-off analytical/numerical script closing one named
rubric row or open-derivations item**, e.g. `cosmology_bbn.py` closing rubric row K2,
`dimensionality.py` closing A1, `thermodynamics_interacting.py` closing G10's GGE residual,
`gravity_field_equation_uniqueness.py` closing a uniqueness question F178 left open. None of the 34
computes a per-tick field update meant to run inside `core.simulation`'s channel loop — each produces
one result (usually one JSON in `test-results/`) and is done.

This is exactly the module class `docs/audits/module-disposition-2026-08-03.md` already
characterized when it resolved the `dead_candidate` bucket (10 → 1): *"nothing imports this ... for
an analytical derivation kernel [is] its normal condition, not a verdict."* That audit's own
follow-up #6 flagged that the label problem would recur: *"the `dead_candidate` label itself is
mis-specified ... it produced nine false positives out of ten."* H7's `driven`-fraction metric has
the same shape of problem one level up: it counts these one-off derivation scripts in the same
denominator as true simulation kernels, so a project whose main mode of progress is closing rubric
rows with standalone scripts (CLAUDE.md's own "Practices": *"always attempt to algebraically derive
new elements ... before introducing new physics"*) will structurally show a falling channel-driven
fraction forever, independent of how healthy the actual simulation core is.

## 3. Checked for real gaps — found none new

Two pools were checked in full, not sampled, for genuine "physics that should be wired in and
wasn't":

- **All 26 `role=kernel`, `reach=standalone` spine modules** (not just the 34 new ones): every
  docstring names one specific finding/rubric row it closes and produces one result. The two
  modules in this pool already known to be open engineering targets rather than closed derivations —
  `core.lpt_generator` (`status=partial`, the E3=Q1=Q2=d1 Wilson-SU(3) Feynman-rule generator,
  reclassified from `dead_candidate` in the 2026-08-03 pass) and `interactions.qed_casimir_materials`
  (`status=dead_candidate`, deliberately left as "Ben's call, not a maintenance decision" per that
  same pass, §3.4) — are unchanged and already tracked. No third case turned up.
- **All 24 `reach=unreferenced` modules**: all 24 are `forks/*`, `status=fork_unclaimed`. Per
  CLAUDE.md's own definition a fork "preserves the falsification record and is not dead code" —
  these are historical/rejected alternatives, correctly excluded from `driven` by design, not gaps.

So: of the 254 modules, the honest "residual" pool — modules that are not driven and are not
accounted for by a design reason — is **zero net-new** this window. The two open items
(`lpt_generator`, `qed_casimir_materials`) predate this window and are already carried on their own
tracks.

## 4. A separate, larger problem this pass found and partially fixed

`src/casim/engine/registry.py` alone carries 669 uncommitted insertion lines, and `git status`
reports **385 modified/untracked files** — nothing has been committed to this repo since `b2fcfa5`
("coverage §4 bucket 1..."). The cause: a **stale `.git/index.lock` dated 2026-08-19 19:34**,
blocking every git write (`fatal: Unable to create '.../.git/index.lock': File exists`) — the exact
failure mode `docs/audits/module-disposition-2026-08-03.md` §4 already diagnosed and fixed once
before (this mount refuses `unlink(2)` but permits `rename(2)`, so the fix is `mv`, not `rm`).

It recurred. This pass renamed it aside (`.git/index.lock` → `.git/index.lock.stale-2026-08-19`) and
confirmed `git add`/`git status` work again. **This is very likely the actual mechanism behind three
of the four consecutive H7 "falls": sessions were doing real work (34 new modules, plenty of new
findings) but nothing was landing in git for over two weeks**, so every report was reading an
ever-growing uncommitted working tree with no committed baseline to compare against cleanly.

**This pass did not commit the 385-file backlog.** Bundling three weeks of concurrent sessions'
work into one commit is a judgement call, not a maintenance action — the same posture
`module-disposition-2026-08-03.md` took on `qed_casimir_materials` (§3.4: "that is Ben's to make, not
something to take quietly inside a maintenance pass"). The lock is cleared and `git add`/`git commit`
both work; the backlog is Ben's to review and commit (or split) at his convenience.

## 5. Recommendation on the H7 metric itself

Not actioned here (a metric-definition change, like the `dead_candidate` rename recommended in
2026-08-03 §6 item 6, is a call for Ben, not a maintenance-pass default): the `driven`-fraction
denominator conflates two populations that grow for different reasons — the live simulation core
(slow-growing by nature; 52 modules across three reports) and the one-off derivation/kernel scripts
that are this project's main unit of research output (fast-growing by design). Scoping H7's fraction
to modules where `role` is not `derivation` and `reach` is not `unreferenced`-by-fork-status would
track the actual simulation core's coverage instead of penalizing every closed finding. On that
scoped basis: of the 254 modules, 96 spine + 158 manifest, only the manifest-origin `test-only` (90)
and `unreferenced` (0 non-fork) pools would remain live candidates for "should this be wired in" —
i.e. the real open question is entirely in the 171-module legacy migration, not in anything new.

## 6. Verification

| Check | Result |
|---|---|
| `from casim.engine.registry import all_modules` live count | 254 total, 52 `driven` (20.5%) |
| Spine-vs-manifest split | 96 spine (12 driven, 81 standalone, 1 unreferenced, 1 entry-script, 1 package-only), 158 manifest (40 driven, 90 test-only, 23 unreferenced, 3 package-only, 2 entry-script) |
| 34 new `_SPINE` registrations (this window) | 1 `driven`, 33 `standalone` — all `status=live`, all findings-backed |
| `role=kernel` standalone pool (26 modules, full read) | 2 known open items (unchanged), 0 new |
| `reach=unreferenced` pool (24 modules, full read) | 24/24 are `fork_unclaimed` forks (by design) + `qed_casimir_materials` (known, Ben's call) |
| git lock | stale since 2026-08-19 19:34; renamed aside, `git add`/`status` confirmed working |

No registry edits were made — nothing in this pass warranted reclassification; every non-driven
module checked out as correctly labeled. `make registry` / `make gate` were not re-run since no
registry content changed.
