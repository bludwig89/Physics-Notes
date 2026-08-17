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
| Always | `claims-index.md` | **what the project asserts right now** (D12) — status + falsifier per claim. Read before writing that the model "predicts" or "shows" anything |
| Always | `docs-index.md` | locate theory docs, papers, reference summaries |
| Always | `tail -n 150 docs/status/changelog.md` | recent changes (never the whole ~100k-token file) |
| As needed | `src/casim/README.md`, `scenarios/RUN-GUIDE.md` | running CASIM |
| Rarely | `references/physics-notes-complete.md` (~44k tokens) | foundational derivations only |

## Directories

| Path | Contents | Index |
|------|----------|-------|
| `src/casim/` | **The whole program** (D6, C9). `numerics/` (D8 façade), `constants/` (D7, owns values), `engine/{core,lattice,gauge,particles,interactions,forks}/` (all physics, by sector), `suite/ analysis/ io/ gui/ viz/ index/ tests/`, `cli.py` (`casim` console script). | `code-index.md`, its `README.md` |
| `src/casim/engine/forks/<sector>/` | The 47 recorded alternatives — tested-and-rejected or live-exploratory branches. Loaded by file path or bare name, not as package submodules. | `code-index.md` |
| `tests/registry/` | **D9**: `*.yaml`, one declarative record per test — the single specification `casim test` and `pytest` both read. | `tests-index.md` |
| `tests/findings/` | `test_F*.py` — one verification script per finding. Run individually. | `tests-index.md` |
| `tests/priority/` | Numbered GR/QM/QFT priority battery (being superseded by `tests/falsification/`). | `tests-index.md` |
| `tests/casim/` | casim package suite — the default `pytest` target (`testpaths` in `pyproject.toml`). | `tests-index.md` |
| `tests/runners/` | Standalone `run_*.py` drivers, comparisons, scans. | `tests-index.md` |
| `tests/falsification/` | FA/FB/FC spec briefs + ROADMAP: tiered confrontations with measured data; one brief = one sub-agent = one result JSON. | its `ROADMAP.md` |
| `test-results/` | All result JSONs, markdown summaries, and `figures/` (single merged location — tests write here). | `tests-index.md` (Results column) |
| `findings/` | One markdown file per physics finding, `F{N}-name.md`. **Past tense** — a finding records what a session concluded and is not rewritten when the model moves. | `findings-index.md` |
| `docs/claims/` | **D12**: one card per claim, `CL{NNN}-slug.md`, + `README.md` (the contract), `TEMPLATE.md`, generated `registry.yaml`. **Present tense** — what the project asserts *now*, and what would kill it. A finding may be superseded without any claim changing, and vice versa. | `claims-index.md` |
| `papers/` | Paper series 01–11 + Claims-and-Falsifiers summary + `pdf/`. | `docs-index.md` |
| `docs/theory/` | Internal theory: `ca-reference.md`, `ca-unified-v2.md`, EOM derivation, F64 gravity explainer, `key-decisions.md`. | `docs-index.md` |
| `docs/roadmaps/` | Active planning: `roadmap-matter-binding.md`, `next-steps.md`. | `docs-index.md` |
| `docs/roadmaps/completed/` | Spent one-off prompts. The finding that closed each is in `docs/audits/consolidation-plan-2026-08-04.md` §3.1. | `docs-index.md` |
| `docs/status/` | What is **current**: `project-status.md` (narrative), `changelog.md` (append-only), `exactness-inventory.md`, `baseline-provenance.md`. | `project-status-index.md` |
| `docs/status/completions/` | Finished engineering phases (P0–P1, C0–C9). **Complete, not superseded** — `deprecated/` is for the latter. | `docs-index.md` |
| `docs/audits/` | One-off reviews, audits, verdicts. | `docs-index.md` |
| `docs/design/` | Internal design docs (electroweak, strong, software plan, …). | `docs-index.md` |
| `references/` | External papers (PDFs), our markdown summaries of them, `diagrams/`, `physics-notes-transcription/`, `physics-notes-complete.md`. | `docs-index.md` |
| `scenarios/` | CASIM scenario YAMLs; `RUN-GUIDE.md` has handles + benchmark speeds. | its `RUN-GUIDE.md` |
| `tools/` | Maintenance scripts: `regen_indexes.py`, `verify_tier3_gravity.py`. | — |
| `checkpoints/` | CASIM run checkpoints (`.npz`, gitignored/transient). | — |
| `deprecated/` | Superseded docs, plans, and old papers; its `README.md` says why each item is there. | its `README.md` |

## Conventions

- New finding → `findings/F{N}-name.md`, then `make indexes`.
- New **claim** (anything extending QM / SM / GR / SR) → `docs/claims/CL{N}-slug.md` via `/claim`, then `make claims`. See CLAUDE.md §"Claims" for the standing rule (**D12**).
- New test → `tests/findings/test_F{N}_*.py`; results JSON → `test-results/`; figures → `test-results/figures/`.
- Non-trivial change → one-paragraph entry in `docs/status/changelog.md` with `yyyy-mm-dd - hh:mm` stamp.
- Default `pytest` runs only `tests/casim/`; finding/priority tests are invoked explicitly.
