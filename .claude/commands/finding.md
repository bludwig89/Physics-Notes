# /finding — Scaffold a new Finding file

You are creating a new finding file for the Physics CA project.

## Steps

1. **Take the number from `casim index`; do not compute it, and take exactly one.** Run `casim index`
   and read the **`NEXT FREE NUMBER`** line. That is the lowest number declared `status: free` in
   `docs/design/finding-numbers.yaml` — one nobody ever wrote at. Claims reserve no numbers
   (`session-claims.yaml` revision 2, 2026-08-05); you take one at the moment you write the file.

   - **Never** derive the number by listing `findings/` and adding one, and never take max+1 by
     hand. Listing-and-adding is the move that collided at F110, F129, F219, F229–F232 and F262;
     max+1 is what left seventeen interior gaps between F291 and F314.
   - **Expect a number well below the maximum.** The allocator drains the backlog the old
     block-reservation scheme left behind, so a finding written today lands in the F280s while
     `max` reads F314. That is correct — spending it *closes* a gap rather than opening one.
   - No open claim for this session? Open one *now* (see CLAUDE.md "Concurrency"): session handle,
     `status: open`, sector, one-line topic. **No numbers** — there is no block to size.
   - Writing a second finding? Re-read `NEXT FREE NUMBER` then. Do not take two now.

   **One edit does all three things:** create `findings/F{N}-{slug}.md`, add
   `{N}: findings/F{N}-{slug}.md` to your claim's `used:` map, and **delete that number's
   `status: free` entry from `docs/design/finding-numbers.yaml`**. Deleting the entry *is* the act
   of spending the number — leave it and `casim index --check` fails, correctly, because the entry
   is then advertising a spent number as available.

1. Ask the user (if not already provided in $ARGUMENTS):
   - **Title**: short kebab-case name for the file slug and a human-readable title
   - **Summary**: one-sentence description of what was found

2. Get the current date/time with `date "+%Y-%m-%d - %H:%M"`.

> **Note — pipes in tables:** a literal `|` (e.g. `|k|`, `|ψ|²`, absolute-value bars) breaks
> Markdown tables and the auto-generated `findings-index.md`. In the **title** and any **table cell**,
> escape it as `\|` (`\|k\|`) or use `\lvert k\rvert` / `\lVert k\rVert`.

4. Create the file `findings/F{N}-{slug}.md` with this template:

```markdown
# F{N} — {Human Title}

**Date:** {yyyy-mm-dd - hh:mm}
**Test record:** record `{record-id}`
**Claim:** {CL###, or `none — <reason>`}

## Summary

{One-paragraph summary of the finding.}

## Physics

*Describe the physics result, equation, or structural insight.*

## Derivation / Evidence

*Steps, code references, or test results supporting the finding.*

## Exactness

| Result | Type | Residual |
|--------|------|---------|
| | | |

## Tests

*List test files and pass/fail counts.*

## Status

Open questions or next steps.
```

4b. **Fill in `**Test record:**` and `**Claim:**` — both are checked, and both
   accept "there isn't one" as long as you say why.** `make coverage` reads them.

   **Test record.** Name the registry record that goes red if this finding is
   wrong. Not a record that mentions the finding — one that *fails* on it. If
   none exists, declare it with a reason from the closed list:

   ```markdown
   **Test record:** none — no-test (analysis-only)
   ```

   | Reason | When |
   |---|---|
   | `analysis-only` | closed-form arithmetic contained in the finding; nothing to run |
   | `narrative-bundle` | a bundle/index file, not one testable finding |
   | `superseded` | fully superseded per `docs/theory/supersessions.yaml` |
   | `awaiting-test` | **DEBT.** A test is owed. |

   Anything outside that list fails, and so does a bare `none` with no reason.

   **Claim.** Name the `CL###` card this finding supports, if it has one.
   Findings and cards are **not** 1:1 — one card often rests on six findings, and
   plenty of findings assert nothing a card should carry. That is a normal
   outcome; it just has to be declared:

   ```markdown
   **Claim:** none — infrastructure; asserts no physics a card would carry
   **Claim:** pending — card owed; the physics is real and uncarded
   ```

   A reason is required after the dash in both cases.

   **`awaiting-test` and `pending` are debt, not exits.** They clear the
   "is it silent?" counters because you have answered the question, but the
   `untested` and `unclaimed` totals hold them, so relabelling never reduces the
   work. See `docs/roadmaps/finding-coverage-rollout.md`.

5. Regenerate `findings-index.md` by running this script from the project root:

```python
import os, re

findings_dir = "findings"
entries = []

CAP = 160  # max summary length; keeps the index to one compact line per finding

def clean(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)   # [txt](url) -> txt
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)         # [[link]] -> link
    return re.sub(r'\s+', ' ', text).strip()

def truncate(text, n=CAP):
    # Cut on a word boundary and add an ellipsis so summaries never break mid-word.
    text = text.strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip(' ,;:.—–-')
    return (cut or text[:n]) + '…'

def extract_summary(content, fname):
    # 1) Descriptive part of the title (after the "F123 —"/"F123:" separator).
    #    Present and clean in nearly every finding; this is the primary source.
    title_m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if title_m:
        title = clean(title_m.group(1))
        parts = re.split(r'\s*[—–]\s*|:\s+', title, maxsplit=1)
        if len(parts) > 1 and parts[1].strip():
            return truncate(parts[1].strip())
        if title:
            return truncate(title)
    # 2) First sentence of a `## Summary` section, if the title had no separator.
    sum_m = re.search(r'##\s+Summary\s*\n+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if sum_m:
        text = clean(sum_m.group(1))
        if text:
            return truncate(re.split(r'(?<=[.!?])\s', text)[0])
    # 3) First real prose line - skip metadata (**Date:**, dates, `code`, lists, etc.)
    for l in content.splitlines():
        l = l.strip()
        if not l or l.startswith(('#','**','`','>','-','|','$','!','*','=','[')):
            continue
        if re.match(r'^\d{4}-\d{2}-\d{2}', l):
            continue
        return truncate(clean(l))
    return fname

for fname in sorted(os.listdir(findings_dir)):
    if not fname.endswith(".md"):
        continue
    fpath = os.path.join(findings_dir, fname)
    with open(fpath, encoding="utf-8", errors="replace") as f:
        content = f.read(2000)

    m = re.match(r'(F\d+)', fname)
    fnum = m.group(1) if m else "?"

    summary = extract_summary(content, fname)

    test_m = re.search(r'(\d+)/(\d+)\s*PASS', content)
    tests = f"{test_m.group(1)}/{test_m.group(2)} PASS" if test_m else ""

    entries.append((fnum, fname.replace('.md',''), summary, tests))

with open("findings-index.md", "w") as out:
    out.write("# Findings Index\n\n")
    out.write("*Auto-generated compact index — one line per finding. Read individual files for full content.*\n")
    out.write("*Pipes in summaries are escaped (`|`->`\\|`) so `|k|`-style notation doesn't break the table.*\n\n")
    out.write("| # | File | Summary | Tests |\n")
    out.write("|---|------|---------|-------|\n")
    for fnum, slug, summary, tests in entries:
        safe = summary.replace("|", "\\|")  # escape so |k|, |psi|^2 etc. don't break the table
        out.write(f"| {fnum} | `{slug}` | {safe} | {tests} |\n")

print(f"findings-index.md updated ({len(entries)} entries)")
```

6. **Automatically run `/exactness` for this finding.** Do not stop and wait — chain straight into it:
   - Read `.claude/commands/exactness.md` and follow its steps using the results from the finding you just created (the `## Exactness` table and `## Tests` section are the source rows).
   - For each confirmed result in the finding, append a row to the correct tier section of `docs/status/exactness-inventory.md` (Exact algebraic / Machine precision / Quantitative), set **Source** to this finding's number and test file, and update the "Last updated" line.
   - If the finding has no confirmed numerical results yet (results still open/pending), skip the append and tell the user `/exactness` was deferred until results are confirmed.

7. Remind the user to:
   - Add an entry to `docs/status/changelog.md` if code was written
   - Update `docs/status/project-status.md` if this is a major milestone
