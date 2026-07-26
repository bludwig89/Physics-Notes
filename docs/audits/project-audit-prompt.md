# Project Audit — Methodology & Rerunnable Prompt

*Standalone companion to the `/project-audit` slash command (`.claude/commands/project-audit.md`).*
*Purpose: a copy-pasteable prompt + the reasoning behind it, so the full project review can be
rerun from any session — with or without the slash command — as the build progresses.*

*Last revised: 2026-07-15 - 19:15.*

---

## What this audit produces

A single authoritative deliverable: **`docs/status/project-status-guide.md`** — a
"status of the project" guide written for a mixed audience (executive summary any
technical reader can follow, then dense sector-by-sector detail for the author and
future Claude sessions). Rerunning the audit overwrites that guide from the current
repo state.

## Why it is built the way it is

The repo already maintains the raw material for a status review — six auto-generated
indexes, an append-only changelog, an exactness inventory, and the open-derivations
ledger. The audit does **not** recompute any of that; it **reads the live artifacts**,
fans out to confirm module/test health, and synthesizes. Consequences:

- **It stays correct as the build grows.** Numbers come from `ls | wc -l` and the
  regenerated indexes, never from a prose figure that goes stale.
- **It respects the existing ledger.** `docs/status/open-derivations.md` is the source
  of truth for what is open vs closed-negative; the guide mirrors it rather than
  re-deriving the frontier. If the ledger's own "Last audit" date lags the changelog,
  the audit flags it and points at the ledger's Master Audit Prompt
  (`docs/roadmaps/open-derivations-prompts*.md`) instead of guessing.
- **It preserves honest negatives.** A proven free parameter or an exact no-go is a
  *result*, not a gap; the guide keeps them in a distinct catalogue.

## The prompt (copy-paste this to rerun without the slash command)

> Run a complete review of this Physics CA project and regenerate
> `docs/status/project-status-guide.md`. Steps:
>
> 1. **Refresh & count.** Run `python3 tools/regen_indexes.py`. Get `date "+%Y-%m-%d - %H:%M"`.
>    Count files (never trust prose numbers): findings (`ls findings/F*.md | wc -l`
>    and the max F-number), `ca-simulation/ca_*.py`, `derive_*.py`, `forks/*.py`,
>    `src/casim/**/*.py`, `tests/**/*.py`, `scenarios/*.y*ml`, `papers/Paper-*.md`.
> 2. **Read the spine (not from memory):** `CLAUDE.md`, `INDEX.md`,
>    `docs/theory/key-decisions.md`, `docs/status/open-derivations.md`,
>    `findings-index.md`, `project-status-index.md`, `head -n 60 docs/status/changelog.md`,
>    `code-index.md`, `tests-index.md`, the headers + "not-yet-met" table of
>    `docs/status/exactness-inventory.md`, and `papers/README.md`.
> 3. **Fan out** (parallel sub-agents): (a) module audit — group `ca_*.py` by sector,
>    flag superseded modules, inventory `derive_*`/`forks/`/`src/casim/`, verify the
>    live engine-channel count; (b) test + finding-arc audit — per-subdir test totals,
>    the pass picture, any failing/open/retired rows, and the ~5–10 landmark findings
>    per sector.
> 4. **Write** `docs/status/project-status-guide.md` with the fixed skeleton: header +
>    scope counts; executive summary with a maturity-by-sector table; the theory in one
>    page (the 6 core design decisions); sector-by-sector status (established / exact vs
>    quantitative / open, with finding numbers); code & infrastructure; tests & exactness;
>    open frontier (mirroring the ledger, incl. the deepest open number $d_1$ and the
>    closed-negatives); papers; how-to-rerun. Prose + tables, no bullet walls, Markdown
>    math, escape `\|` in tables, and never inflate a quantitative match to "exact".
> 5. **Verify:** every cited F-number exists as a file; the open-frontier section matches
>    `open-derivations.md`; scope counts match the file counts; nothing labelled "exact"
>    that the exactness inventory calls quantitative/open. For a rigorous run, dispatch a
>    sub-agent to re-read the finished guide against `open-derivations.md` +
>    `key-decisions.md` for contradictions.
> 6. **Record:** append a one-paragraph, timestamped entry to `docs/status/changelog.md`
>    noting the audit ran and what changed since the last guide.

## Guide skeleton (keep headings stable across reruns)

Stable headings make each rerun a meaningful `git diff`:

1. Header (timestamp, scope counts, how-generated pointer)
2. Executive summary (+ maturity-by-sector table)
3. The theory in one page (6 core design decisions + master identities)
4. Sector-by-sector status
5. Code & infrastructure
6. Tests & exactness
7. Open frontier (mirrors `open-derivations.md`)
8. Papers
9. How to rerun

## Relationship to the other audit tools

| Tool | Scope | Output |
|------|-------|--------|
| `/project-audit` (this) | **Whole project** — modules, findings, tests, papers, status | `docs/status/project-status-guide.md` |
| Master Audit Prompt (`docs/roadmaps/open-derivations-prompts*.md`) | **Open derivations only** | `docs/status/open-derivations.md` |
| `/finding`, `/exactness` | Single finding / single exactness row | one file each |
| `tools/regen_indexes.py` | The six machine indexes | `*-index.md` |

Run the Master Audit Prompt first if the ledger is stale; then `/project-audit` for the
whole-project picture.
