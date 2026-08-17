# /derive — Physics analysis, derivation, or test design

Load the right context, work through the physics, produce tests.

## Step 0 — Claim your TOPIC (before any physics). Not numbers.

A question has been posed, so say so on the board now: append a claim to
`docs/design/session-claims.yaml` with your session handle, `status: open`, sector and a one-line
topic. **No finding numbers** — a claim reserves none (revision 2, 2026-08-05). This is one small
append and it is the whole collision-avoidance mechanism: its value is warning a parallel session
off your question before either of you has done the work.

Numbers come later and one at a time. When you actually write a finding, run `casim index`, take
the **`NEXT FREE NUMBER`**, and in the same edit create the file, add it to your claim's `used:`
map, and delete that number's `status: free` entry from `docs/design/finding-numbers.yaml`. Full
protocol: CLAUDE.md "Concurrency".

Why not reserve up front: nobody knows at Step 0 how many findings a question will produce, so
reserving guesses — and the guess used to be 3–5 while most sessions land one. The remainder
stranded as gaps. Reading the current max finding number is still not a reservation, and taking
max+1 by hand is still wrong; the allocator hands out the lowest free number, which is usually
below the maximum.

## Step 1 — Load minimal context

Always read these (small, always relevant):
- `findings-index.md` — one-line summary of all findings (~3k tokens)
- `project-status-index.md` — one-line per milestone, recent-first (~1.4k tokens)
- `tail -n 150 docs/status/changelog.md` — recent changes only (not the whole file)

Do NOT load `docs/status/project-status.md`, `physics-notes-complete.md`, or all findings files upfront.

## Step 2 — Find relevant findings

Search for findings related to $ARGUMENTS:
```
grep -i "KEYWORD" findings-index.md
grep -i "KEYWORD" project-status-index.md
```
Then read only the specific `findings/F{N}-*.md` files that appear relevant (2–5 max).

If the question involves a specific module, also locate the source:
```
grep -rn "KEYWORD" src/casim/engine/ --include="*.py" -l
```

If the question requires foundational derivations not in a finding file, read the relevant section of `references/physics-notes-complete.md` — but only after the index search comes up short.

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

`{N}` is a number you hold on the claim board — claiming `F{N}` claims the `F{N}-*` test-ID
namespace with it. A registry ID that does *not* derive from a number you hold (`run-*`, `fork-*`,
`scenario-*`) must be listed explicitly in your claim's `tests:`.
## Step 6 — After passing tests

Remind user to run:
- `/finding` to document the result (also regenerates `findings-index.md`)
- `/exactness` to log the new rows
- Add a one-paragraph entry to `docs/status/changelog.md` with timestamp
- Add a `## {date} — {summary}` entry to `docs/status/project-status.md` (regenerate `project-status-index.md` afterward)
