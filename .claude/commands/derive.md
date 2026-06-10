# /derive — Physics analysis, derivation, or test design

Load the right context, work through the physics, produce tests.

## Step 1 — Load minimal context

Always read these (small, always relevant):
- `findings-index.md` — one-line summary of all findings (~3k tokens)
- `project-status-index.md` — one-line per milestone, recent-first (~1.4k tokens)
- `tail -n 150 changelog.md` — recent changes only (not the whole file)

Do NOT load `project-status.md`, `physics-notes-complete.md`, or all findings files upfront.

## Step 2 — Find relevant findings

Search for findings related to $ARGUMENTS:
```
grep -i "KEYWORD" findings-index.md
grep -i "KEYWORD" project-status-index.md
```
Then read only the specific `findings/F{N}-*.md` files that appear relevant (2–5 max).

If the question involves a specific module, also locate the source:
```
grep -rn "KEYWORD" ca-simulation/ --include="*.py" -l
```

If the question requires foundational derivations not in a finding file, read the relevant section of `reference-research/physics-notes-complete.md` — but only after the index search comes up short.

## Step 3 — State the question clearly

Before deriving anything, write out:
- **What we want to show** (one sentence)
- **Which findings it connects to** (F-numbers)
- **Exactness target**: algebraic identity / machine precision / quantitative match

## Step 4 — Derive

Work symbolically first. Use sympy if needed to verify algebra — write the check as a standalone block before running it.

Flag every step as:
- ✓ **Exact** — follows from algebra/symmetry alone
- ~ **Numerical** — requires lattice evaluation
- ? **Assumption** — posited, not yet derived

## Step 5 — Write tests

One test per claim. Each test must:
- Print the residual, not just pass/fail
- Be labelled with the finding number and tier (Exact/Machine/Quantitative)
- Use only `stdlib + numpy` — no scipy on chiral/spinor quantities without checking first
- Verify rotation laws match F91 classification (even vs chiral) for any propagator

Save to `model-tests/test_F{N}_name.py`.

## Step 6 — After passing tests

Remind user to run:
- `/finding` to document the result (also regenerates `findings-index.md`)
- `/exactness` to log the new rows
- Add a one-paragraph entry to `changelog.md` with timestamp
- Add a `## {date} — {summary}` entry to `project-status.md` (regenerate `project-status-index.md` afterward)
