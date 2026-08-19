# F274 — Scenario language v2: a scenario that mis-spells a key fails at load, not at tick 400

*2026-07-31 - 22:55. Roadmap **P4**. Software/engineering finding, no physics decision reversed.*
*Status: **established** (built, gated; `tests/casim/test_scenario_schema_v2.py`, 12/12).*

**Claim:** none — software/engineering; a scenario-loader schema and template mechanism, and the finding's own header records that no physics decision is reversed. Declared 2026-08-19.

## 1. Claim

Before P4, `casim.io.load_scenario` validated exactly two things: that the file
parsed to a mapping and that `channels` was non-empty. A misspelled key was
silently ignored (`withd: 1.5` for `width`), and **0 of 46** scenarios carried
any `units:`, `events:`, `expect:`, `boundaries:`, `view:`, `extends:`, `sweep:`
or `compute:` block because none of those keys existed. P4 makes a scenario a
*checked* object: a `version: 2` scenario is validated against a strict schema at
load, an unknown key is an error (with a typo suggestion), and dangling
channel/observer cross-references are caught before the engine runs.

## 2. What was built

* **`casim.io.schema`** — the strict v2 schema. Every top-level and nested block
  declares its allowed keys; an unlisted key is reported against the block it
  appeared in. Channel/observer **parameters are deliberately not whitelisted**
  — a channel type owns its own parameter names, and duplicating that list at
  the schema layer is exactly the curated-key-list mistake
  `casim.engine.core.graph._config_channel_refs` documents (F269). What *is*
  checked per channel/observer: a **registered** `type`, typed `name`/`seed`,
  and every cross-reference (observer→channel, `sources:` list or `{channel:
  weight}` mapping). `compute.dtype: complex64` is rejected unless
  `allow_float32: true` — the schema-level mirror of the 1e-12 gate that bars a
  device backend from auto-activating.
* **`casim.io.templates`** — the `extends:` mechanism. A `hydrogen` template
  supplies the seven hand-matched channels + three observers of
  `unified_hydrogen.yaml`; `scenarios/hydrogen.yaml` is then **13 lines** (P4
  target: <20). Merge semantics: the scenario wins, its `lattice` merges
  key-by-key, its channels/observers replace.
* **`events:` timeline** — validated generically; the engine consumes the one
  action it already has native machinery for, a timed block-spin (`do: blockspin`
  → the F133 `blockspin_schedule`), so `scenarios/photon_pair_timed.yaml` fires
  R_b at tick 20 (L 16→8) from the timeline. Other actions (`inject`, `pulse`,
  `measure`, `ramp`) validate now and are left for the engine's dispatch to grow
  into rather than silently dropped.
* **Migration** — `tools/upgrade_scenarios.py` inserts `version: 2` comment-
  preservingly and idempotently; **all 46** shipped scenarios migrated and
  validate strictly, plus the 2 new demonstration scenarios (48/48 via
  `casim scenario-check`). v1 files still load behind a `DeprecationWarning`
  for one cycle.
* **CLI** — `casim scenario-check [path]` validates one file or all of them
  (exit 1 on any failure — the acceptance-gate check).

## 3. Acceptance gate (roadmap §P4) — status

| Criterion | Verdict |
|---|---|
| Every shipped scenario validates strictly | **MET** — 48/48, asserted in the gate test and `casim scenario-check` |
| A deliberately misspelled key fails at load | **MET** — top-level and `lattice` typos raise `ScenarioError`; `withd` is caught |
| `hydrogen.yaml` under 20 lines via templates | **MET** — 13 lines via `extends: hydrogen` |
| One scenario expresses a timed event and a pass/fail expectation | **MET** — `photon_pair_timed.yaml` (events + `expect:` block); the event *fires* in the engine |

## 4. What is deliberately not yet wired (handed forward)

The schema **validates and stores** `units:`, `boundaries:`, `view:`, `compute:`,
`sweep:` and `expect:`, but the engine does not yet *act* on all of them: per-
channel `seed` is validated but not plumbed into `casim.numerics.rng` (doing so
would move every random-init baseline, so it is opt-in only and unused by the 46
files); `expect:` gates are declared but not enforced as a run verdict (the D9
test registry is where enforcement lives today); `boundaries:` other than
periodic are recognised but the engine is still periodic. These are P4-schema-
complete and P4-engine-incomplete by design — wiring each is a separate change
with its own baseline exposure. See `docs/roadmaps/roadmap-unified-program.md`
§P4 and the P5 hand-back for the remainder.

## 5. Files

`src/casim/io/schema.py`, `src/casim/io/templates.py`, `src/casim/io/__init__.py`
(load path), `src/casim/engine/core/simulation.py` (events→blockspin merge),
`src/casim/cli.py` (`scenario-check`), `tools/upgrade_scenarios.py`,
`scenarios/hydrogen.yaml`, `scenarios/photon_pair_timed.yaml`, all 46 migrated
scenarios. Test: `tests/casim/test_scenario_schema_v2.py`.
