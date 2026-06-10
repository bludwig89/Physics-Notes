# Repository Map

*Hand-maintained master index. Last updated: 2026-06-10 - 23:05 (repository reorganization).*
*Auto-generated indexes are rebuilt with `python3 tools/regen_indexes.py`.*

## AI session loading order

| Priority | Load | Why |
|----------|------|-----|
| Always | `CLAUDE.md`, this file | role, design decisions, map |
| Always | `findings-index.md` | locate findings, then read only the `findings/F{N}-*.md` you need |
| Always | `project-status-index.md` | milestone history at a glance |
| Always | `tests-index.md` | test ↔ finding ↔ results map; check before writing/hunting a test |
| Always | `code-index.md` | what each kernel module / casim subpackage does |
| Always | `docs-index.md` | locate theory docs, papers, reference summaries |
| Always | `tail -n 150 docs/status/changelog.md` | recent changes (never the whole ~100k-token file) |
| As needed | `src/casim/README.md`, `scenarios/RUN-GUIDE.md` | running CASIM |
| Rarely | `references/physics-notes-complete.md` (~44k tokens) | foundational derivations only |

## Directories

| Path | Contents | Index |
|------|----------|-------|
| `ca-simulation/` | Core model kernels: `ca_*.py` physics modules, `derive_*.py` derivations, `forks/` variants. Import root for all finding tests. | `code-index.md` |
| `src/casim/` | CASIM package — engine/channels/observers/CLI layer over the kernels (`casim` console script). | `code-index.md`, its `README.md` |
| `tests/findings/` | `test_F*.py` — one verification script per finding. Run individually. | `tests-index.md` |
| `tests/priority/` | Numbered GR/QM/QFT priority battery (being superseded by `tests/falsification/`). | `tests-index.md` |
| `tests/casim/` | casim package suite — the default `pytest` target (`testpaths` in `pyproject.toml`). | `tests-index.md` |
| `tests/runners/` | Standalone `run_*.py` drivers, comparisons, scans. | `tests-index.md` |
| `tests/falsification/` | FA/FB/FC spec briefs + ROADMAP: tiered confrontations with measured data; one brief = one sub-agent = one result JSON. | its `ROADMAP.md` |
| `test-results/` | All result JSONs, markdown summaries, and `figures/` (single merged location — tests write here). | `tests-index.md` (Results column) |
| `findings/` | One markdown file per physics finding, `F{N}-name.md`. | `findings-index.md` |
| `papers/` | Paper series 01–11 + Claims-and-Falsifiers summary + `pdf/`. | `docs-index.md` |
| `docs/theory/` | Internal theory: `ca-reference.md`, `ca-unified-v2.md`, EOM derivation, F64 gravity explainer, `key-decisions.md`. | `docs-index.md` |
| `docs/roadmaps/` | Active planning: `roadmap-matter-binding.md`, `next-steps.md`. | `docs-index.md` |
| `docs/status/` | `project-status.md` (narrative), `changelog.md` (append-only), `exactness-inventory.md`. | `project-status-index.md` |
| `docs/audits/` | One-off reviews, audits, verdicts. | `docs-index.md` |
| `docs/design/` | Internal design docs (electroweak, strong, software plan, …). | `docs-index.md` |
| `references/` | External papers (PDFs), our markdown summaries of them, `diagrams/`, `physics-notes-transcription/`, `physics-notes-complete.md`. | `docs-index.md` |
| `scenarios/` | CASIM scenario YAMLs; `RUN-GUIDE.md` has handles + benchmark speeds. | its `RUN-GUIDE.md` |
| `tools/` | Maintenance scripts: `regen_indexes.py`, `verify_tier3_gravity.py`. | — |
| `checkpoints/` | CASIM run checkpoints (`.npz`, gitignored/transient). | — |
| `deprecated/` | Superseded docs, plans, and old papers; its `README.md` says why each item is there. | its `README.md` |

## Conventions

- New finding → `findings/F{N}-name.md`, then `python3 tools/regen_indexes.py`.
- New test → `tests/findings/test_F{N}_*.py`; results JSON → `test-results/`; figures → `test-results/figures/`.
- Non-trivial change → one-paragraph entry in `docs/status/changelog.md` with `yyyy-mm-dd - hh:mm` stamp.
- Default `pytest` runs only `tests/casim/`; finding/priority tests are invoked explicitly.
