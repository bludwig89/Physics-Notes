# P5 GUI workbench — hand-back for the display-dependent items

*Created 2026-07-31 - 22:50. Companion to `roadmap-unified-program.md` §P5. The
headless-checkable P5 items (P5.1 viz consolidation, the P5.4 results-compare,
the CLI fix) were built this session and are gated; the items below need a live
vispy/Qt window and cannot be built or verified in the sandbox (no display, and
`casim[gui]` — vispy + PyQt6 — is not installed). This is their spec, so a
session on Ben's machine can pick them up without re-deriving the design.*

## What already landed (headless, this session)

- **P5.1 — viz consolidation.** `casim.viz` is now the single static-figure /
  colour-map API (re-exports `casim.gui.render` + `_viz_spinor_color` +
  `_viz_tick_heatmap`), replacing the 13-line shim that imported two modules
  which no longer exist. `engine/core/_viz_live_display` is banner-retired and
  documented as duplicating `gui.render.density_to_rgba`; its physical move to
  `deprecated/code/` needs `git mv` (an `unlink` this mount refuses) and is
  handed back — one line on Ben's machine:
  `git mv src/casim/engine/core/_viz_live_display.py deprecated/code/`, then drop
  its `_SPINE`/manifest record.
- **P5.4 (headless half) — results compare.** `casim compare A.json B.json`
  diffs two arbitrary run JSONs over `casim.baselines.compare` (the same numeric
  diff behind `tests/runner._diff_against_head` and `tools/check_result_drift`),
  reporting which observables moved and classifying sub-1e-12 deltas as noise.
- **CLI.** `cli.py`'s "Phase E (not yet implemented)" line is gone; `gui`,
  `scenario-check` and `compare` are documented.

## P5.2 — Interaction (needs a window)

Target file: `src/casim/gui/app.py` (vispy canvas + Qt sidebar in
`gui/sidebar.py`).

1. **Place matter by clicking.** Map a canvas click → lattice cell (invert the
   point-cloud camera transform vispy already holds), then instantiate the
   selected channel's init at that centre via the existing `extends`/template
   machinery (P4 `casim.io.templates`), so "click to drop a hydrogen atom" reuses
   the same template the YAML does. Acceptance: a placed atom appears in the
   cloud and is a real channel in `sim.channels`, not a decal.
2. **Live parameter edits without rebuild-from-tick-0.** The engine already
   keeps per-channel `config`; add a `Channel.set_param(key, value)` that rev:
   mass, couplings, thresholds — mutating `config` and any derived cached
   operator — without touching `state`. Wire the sidebar sliders to it. The
   trap to avoid: several channels cache k-space unitaries keyed on parameters
   (`_weyl_cache`/`_disp_cache`); a live edit must invalidate that cache.
3. **`steps_per_frame`** is hard-coded to 2 at `gui/app.py:170`. Read it from
   the P4 `view:` block (`view.steps_per_frame`, already in the schema) and from
   a sidebar spinner.
4. **Volume slicing + frame/movie export.** A slice plane (already a `view.slice`
   schema key) and a frame dump to PNG/MP4. `casim.viz.tick_heatmap` is the
   headless figure primitive to reuse for single-frame export.

## P5.3 — Time (needs a window)

A ring buffer of recent `sim.states` snapshots enabling rewind/scrub; today time
only moves forward.

- Store the last *N* checkpoints in memory (reuse `Simulation.checkpoint`'s
  serialisation, not a second format). A scrub sets the display to a buffered
  state without advancing the engine; stepping forward from a scrubbed point
  discards the newer buffer (standard undo semantics).
- Bound *N* by memory: one `L^3` complex128 field is `16·L³` bytes; the buffer
  cap belongs in the P4 `compute.mem_gb` budget.
- **Determinism caveat:** rewind + re-run must reproduce the trajectory. That
  needs the per-channel RNG streams (P4 `casim.numerics.rng`, still not wired
  into the engine — `simulation.py:109` is one global `default_rng`). Do P4's
  per-channel-seed wiring first, or rewind-then-replay will diverge on any
  channel that draws random numbers per step.

## P5.4 — Results browser (GUI half)

The headless `casim compare` is the data layer. The GUI half:

- A compare view over the P1.4 manifest (`test-results/manifest.json`): pick two
  runs from a list, call `casim.analysis.compare.compare_runs`, render the moved
  observables as a table and a per-observable time-series plot (matplotlib via
  `casim.viz`, or vispy line visuals for live overlay).
- "Click a finding → its test → its result → its exactness class" is now a join
  over declared registry fields (`code-index.md`, `tests-index.md`,
  `findings-index.md` are generated from the registries), not a heuristic — so
  the browser reads those, it does not re-scan the tree.

## Acceptance gate (unchanged from roadmap §P5)

> one viz implementation; a full experiment (place matter → run → observe →
> export figure) without touching a YAML; two runs diffable side by side.

Two of three are now met headlessly: **one viz implementation** (`casim.viz`),
and **two runs diffable** (`casim compare`). The middle clause — the
click-to-place experiment loop — is the P5.2 work above and is the reason this
gate is not yet closable in the sandbox.
