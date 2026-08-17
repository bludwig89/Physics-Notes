# Slash-command patches for the claim board

> **SUPERSEDED 2026-08-05 - 09:30 — do not apply the patches below.** Both were applied, and both
> have since been *replaced*: `session-claims.yaml` reached revision 2, in which a claim reserves
> **no finding numbers at all**. The patch text on this page still tells a session to take "a 3–5
> number block starting at `next_finding`" and to bump `next_finding` — that block is gone, and so
> is `next_finding`. A number is now taken one at a time, at the moment the finding file is written,
> and it is the lowest number declared `status: free` in `docs/design/finding-numbers.yaml`
> (`casim index` prints it as `NEXT FREE NUMBER`).
>
> The page is kept, not deleted, because it is the record of *why* `/finding` stopped saying "find
> the highest F-number and add one" — a move that had collided six times. That diagnosis is still
> correct and is still the reason the allocator is a tool rather than a habit. What revision 2
> changed is the second half: reserving a block fixed the collisions and bought gaps instead, which
> is a different failure with the same root cause — an allocation decision made before anyone knew
> what was being allocated. Live protocol: CLAUDE.md "Concurrency".

*Created 2026-08-02 - 10:25. Companion to `docs/design/session-claims.yaml` and the CLAUDE.md
"Concurrency" section. **This file is a to-do — delete it once both patches are applied.***

`.claude/` is outside the folder this session can write to, so the two command files that pick
finding numbers could not be edited directly. Both need the change below, because `/finding` step 1
currently instructs exactly the move that has collided six times: *"find the highest F-number
currently used… the next number is that + 1."* Two parallel sessions read the same max and both
write it.

---

## 1. `.claude/commands/finding.md` — replace step 1

Replace:

```markdown
1. List the files in `findings/` and find the highest F-number currently used (e.g. `F126-*.md` → 126). The next number is that + 1.
```

with:

```markdown
1. **Take the number from your claim; do not compute it.** Open `docs/design/session-claims.yaml`,
   find your session's `status: open` claim, and use the **lowest number in your `findings:` block
   that is not yet in `used:`**.

   - No open claim for this session? Open one *now* (see CLAUDE.md "Concurrency"): append an entry
     with your session handle, sector, topic and a 3–5 number block starting at `next_finding`, and
     bump `next_finding`. Then take your first number.
   - Out of numbers? Extend your own claim on the board first, then write the file.
   - **Never** derive the number by listing `findings/` and adding one. That is the move that
     collided at F110, F129, F219, F229–F232 and F262.

   In the same edit that creates the finding file, add `{N}: findings/F{N}-{slug}.md` to your
   claim's `used:` map. A reserved number is a placeholder; a `used:` entry is the number spent.
```

---

## 2. `.claude/commands/derive.md` — insert a new Step 0

Insert before "## Step 1 — Load minimal context":

```markdown
## Step 0 — Claim your numbers (before any physics)

A question has been posed, so the numbers get reserved now, not at write-up time. Append a claim to
`docs/design/session-claims.yaml`: your session handle, `status: open`, sector, a one-line topic,
and a block of 3–5 finding numbers starting at `next_finding` — then bump `next_finding` by the
size of the block. Fill the claim's `used:` map in as you write each finding, and release the claim
at the end of the session. Full protocol: CLAUDE.md "Concurrency".

This is one small append and it is the whole mechanism. Reading the current max finding number is
not a reservation.
```

And in "## Step 5 — Write tests", the line

```markdown
Save to `tests/findings/test_F{N}_name.py`.
```

can gain:

```markdown
`{N}` is a number you hold on the claim board — claiming `F{N}` claims the `F{N}-*` test-ID
namespace with it. A registry ID that does *not* derive from a number you hold (`run-*`, `fork-*`,
`scenario-*`) must be listed explicitly in your claim's `tests:`.
```
