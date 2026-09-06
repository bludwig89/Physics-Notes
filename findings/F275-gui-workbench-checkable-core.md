# F275 — GUI workbench: one viz implementation and two runs diffable, headlessly

*2026-07-31 - 23:00. Roadmap **P5** (checkable core). Software/engineering finding.*
*Status: **established** for the headless half; interactive half handed forward. Tests: `tests/casim/test_viz_api.py` (5/5), `tests/casim/test_results_compare.py` (5/5).*

**Test record:** record `viz-api` (tier gate) — `tests/casim/test_viz_api.py`, 5/5: the API is populated rather than `None` and its `density_to_rgba` **is** `casim.gui.render`'s, so the `_viz_live_display` duplicate cannot be the one picked up; record `results-compare` (tier gate) — `tests/casim/test_results_compare.py`, 5/5: the headless run-diff reuses `casim.baselines.compare` and classifies a sub-1e-12 difference as noise, not drift. Declared 2026-08-19.
**Claim:** none — software/engineering; one viz API and a headless run-diff that reuses the project's existing numeric comparison. Declared 2026-08-19.

## 1. Claim

P5's acceptance gate is "one viz implementation; a full experiment (place matter
→ run → observe → export figure) without touching a YAML; two runs diffable side
by side." Two of the three clauses are achievable and verifiable without a
display and are now done; the middle clause needs a live vispy/Qt window (and
`casim[gui]`, not installed in the sandbox) and is specified for hand-back.

## 2. What was built (P5.1, P5.4, CLI)

* **P5.1 — one viz implementation.** `casim.viz` was a 13-line shim that
  imported two flat modules deleted at C9, so it re-exported `None` and nothing
  imported it. It is now the single static-figure / colour-map API: the numpy-
  only production colour maps from `casim.gui.render` (`density_to_rgba`,
  `bloch_rgb`, `point_cloud*`, `tinted_rgba`, `lattice_medium`), the
  15-channel-driven `spinor_to_rgb`/`make_bloch_legend`, and the matplotlib
  `tick_heatmap` (guarded — headless installs still get every colour map). A
  test pins `casim.viz.density_to_rgba is casim.gui.render.density_to_rgba`, so
  the duplicate implementation in `engine/core/_viz_live_display` (imported by
  nothing; registry `dead_candidate`) cannot silently be the one picked up. That
  module is banner-retired pointing at the canonical one; its physical move to
  `deprecated/code/` needs `git mv` (an `unlink` this mount refuses) and is
  handed back.
* **P5.4 — two runs diffable (headless half).** `casim compare A.json B.json`
  and `casim.analysis.compare.compare_runs` diff two arbitrary result JSONs over
  `casim.baselines.compare` — the *same* numeric diff behind
  `tests/runner._diff_against_head` and `tools/check_result_drift`, reused rather
  than reinvented. So a user-facing compare inherits the project's own notion of
  "moved": volatile keys (timestamps, paths) ignored, only numbers compared, a
  difference below the 1e-12 machine floor classified as noise not drift.
* **CLI.** `cli.py:8`'s "Phase E (not yet implemented)" is gone; `gui`,
  `scenario-check` and `compare` are documented and wired.

## 3. Acceptance gate (roadmap §P5) — status

| Criterion | Verdict |
|---|---|
| One viz implementation | **MET** — `casim.viz`, single canonical `density_to_rgba` |
| Place matter → run → observe → export figure, no YAML | **NOT MET in sandbox** — needs a window; specified in the hand-back (`docs/roadmaps/p5-gui-workbench-handback.md`, P5.2) |
| Two runs diffable side by side | **MET headlessly** — `casim compare`; the GUI compare *view* is the P5.4 hand-back |

## 4. Handed forward (needs a display)

`docs/roadmaps/p5-gui-workbench-handback.md` specifies the display-dependent
items so a session on Ben's machine can pick them up: P5.2 click-to-place (reuse
the P4 templates), live parameter edits with cache invalidation,
`view.steps_per_frame` wiring, slice + movie export; P5.3 a ring-buffer rewind
(blocked on per-channel RNG determinism — P4's un-wired seed streams); the P5.4
GUI compare view over `test-results/manifest.json` on top of the headless
`compare_runs`.

## 5. Files

`src/casim/viz/__init__.py`, `src/casim/analysis/compare.py`,
`src/casim/gui/render.py` (canonical banner), `src/casim/engine/core/_viz_live_display.py`
(retirement banner), `src/casim/cli.py` (`compare`, docstring),
`docs/roadmaps/p5-gui-workbench-handback.md`. Tests: `tests/casim/test_viz_api.py`,
`tests/casim/test_results_compare.py`.
