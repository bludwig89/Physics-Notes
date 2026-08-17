# /remediate-finding — Act on an independent review

Take the verdict of an independent review and **make the repo true to it**. `/review-finding`
deliberately changes nothing; this command is its other half. It reads the review, turns every
recommendation and every `FAIL`/`WEAKENS` attack row into a disposed line item, does the physics and
the code, corrects the finding, and propagates the correction through the indexes, the registries,
the tests and the CASIM modules — then proves it with `make gate`.

Argument: the finding number (`F253`, or `253`). Optional flags:

- `--review <path>` — use a specific review file instead of the newest one for that finding.
- `--no-chain` — fail if no review exists rather than running `/review-finding` first.
- `--dry-run` — build the ledger and the plan, write the report with every item marked
  `PROPOSED`, change nothing else. Useful for sizing a batch.
- `--allow-hard` — pre-authorise the hard-verdict path (see Step 3). Only Ben sets this, and only
  in the invocation itself; never infer it.

---

## The contract

> **This command is the inverse of `/review-finding`.** The review's contract is *"a review changes
> nothing except two files."* This one's is:
>
> **Every recommendation and every `FAIL` or `WEAKENS` attack row gets exactly one disposition, and
> the disposition is written down.** There is no fourth state where an item quietly does not appear.
> That silent drop is the failure mode this command exists to close — the reviews are already
> written and their recommendations are already sitting there unactioned.

> **A recommendation is a hypothesis, not an instruction.** The reviewer was cold and adversarial by
> design, which is exactly why it is sometimes wrong: it lacked context the finding had. Verify each
> problem yourself (Step 4) before you implement the fix. `REJECTED` is a first-class outcome and
> needs the same rigour as `APPLIED`.

> **The finding's history is append-only.** You may correct a claim; you may never erase that it was
> made. The superseded statement stays visible, quoted, dated. A finding whose body silently now
> says the narrowed thing has destroyed the evidence that it once said the wide thing — which is the
> only way anyone can tell the review worked.

> **Two things always stop and ask Ben:** a hard verdict (`REFUTED`, `CIRCULAR`), and any change
> that would touch a canonical decision (CLAUDE.md "Core Design Decisions",
> `docs/theory/key-decisions.md`, or a new entry in `docs/theory/supersessions.yaml`). See Step 3.

---

## Step 0 — Claim, timestamp, target

Unlike a review, this **is** a research session. It writes physics. So it takes numbers.

```bash
date "+%Y-%m-%d - %H:%M"
ls findings/ | grep -iE "F0*{N}-"
ls docs/reviews/ | grep -iE "F0*{N}-review-"
```

Open a claim in `docs/design/session-claims.yaml` **now**, before any derivation — session handle,
`status: open`, the finding's sector, topic `remediate F{N} per review {date}`. **No finding
numbers.** A claim reserves none (revision 2, 2026-08-05), and this command is the case that made
the old rule indefensible: most remediations correct an existing finding rather than writing a new
one, so it reserved 3–5 numbers to spend zero, and every one of those blocks became a gap somebody
later had to hand-declare.

If the remediation *does* turn out to need a successor finding, take the number **then**: run
`casim index`, read `NEXT FREE NUMBER`, and in one edit create the file, add it to `used:`, and
delete that number's `status: free` entry from `docs/design/finding-numbers.yaml`. Holding a number
in advance was never what made it yours — writing the file is. Full protocol: CLAUDE.md
"Concurrency".

Also load the minimum context: `findings-index.md`, `tests-index.md`, `code-index.md`,
`tail -n 150 docs/status/changelog.md`, and the finding itself. Not the whole of anything else.

---

## Step 1 — Locate or produce the review

Use the **newest** `docs/reviews/F{N}-review-{yyyy-mm-dd}.md` unless `--review` names another. If
several reviews exist, read them all — the verdict sequence is the record, and an item marked
`APPLIED` by an earlier remediation that a later review still flags is itself a finding.

If no review exists and `--no-chain` was not passed, run `/review-finding F{N}` to completion first,
then continue here against its output. Do not blend the two: the review must be written, dated and
stamped before any remediation edit happens, or the independence it was built to protect is gone.

**Range reviews.** Some reports cover a block — `docs/reviews/F01-F15-review-2026-08-03.md`. One
invocation still remediates **one** finding: take only the rows that name your `F{N}`, and leave the
review's `**Remediated:**` stamp off until every finding in the range has been done, adding instead
a per-finding line `**Remediated F{N}:** {date} — …`. Stamping a range review after one finding
hides the other fourteen from the sweep.

To find the next unremediated review (this command handles one finding, but the sweep is the goal):

```bash
grep -L '^\*\*Remediated:\*\*' docs/reviews/F*-review-*.md
```

---

## Step 2 — Build the remediation ledger

Extract three lists from the review, in its own words, with a pointer back to the section each came
from. This is a **transcription** step — do not judge yet, and do not fix anything yet.

**Highlights.** What the review *confirmed*, especially anything it confirmed by an independent
route. These matter for two reasons: they are the part of the finding you must not damage while
fixing the rest, and an attack that `PASS`ed is a claim the finding is now entitled to make more
strongly than it does. Under-claiming is a defect too — if the blind agent got there by a different
route and the finding does not say so, that goes in the ledger as an improvement.

**Problems.** Every `FAIL`, every `WEAKENS`, every axis grade below `as-claimed`, every `NOT RUN`
that a `--fast` review skipped, and the verdict itself if it is not `CONFIRMED`. One row each. Also
sweep any section the reviewer wrote to enumerate defects outside the attack table — reports vary,
and `## Defects, worst first`, `## Corrected count, row by row` and `## Supersession` have all
carried items that appear nowhere else. Grep the report's own `## ` headers rather than assuming
the template.

**Improvements.** Everything in the review's `## Recommendations` section, plus anything in
`## Method notes` flagged as unverifiable this run.

Write the ledger as a table before doing anything else:

| # | Source | Item | Kind | Severity |
|---|---|---|---|---|

`Kind` ∈ `physics · module · test · constant · claim · citation · doc`.
`Severity` ∈ `verdict-changing · class-changing · cosmetic` — the review was asked to rank its
recommendations by whether they change the verdict, so use its ranking and say if you disagree.

---

## Step 3 — The hard-verdict gate (stop and ask)

**Before any edit**, check whether this remediation is one Ben decides rather than one you execute.

Stop and ask if **any** of these hold:

- the verdict is `REFUTED` or `CIRCULAR`;
- the fix requires retiring a finding number, or adding an entry to
  `docs/theory/supersessions.yaml`;
- the fix would change a "Core Design Decision" in `CLAUDE.md` or an entry in
  `docs/theory/key-decisions.md`;
- the fix would move a *headline* claim's exactness class down by two or more, or turn a derived
  quantity into an anchored one (`EXACT`/`MACHINE` → `FIT`/`POSIT`);
- the fix needs a physics run longer than the sandbox will bear, so the work has to move to Ben's
  machine.

When you stop, present it compactly and completely — this is the one place a wall of options is
warranted, because Ben cannot make the call without them:

1. The verdict and the single attack that produced it, in two sentences.
2. What in the finding is **salvageable** — the `PASS` rows and any independently confirmed
   algebra. F19's review is the model here: it graded `CIRCULAR` and still recorded that attacks 3
   and 10 passed and that the finding was honestly labelled everywhere it appeared.
3. Three named options, with what each costs and what each destroys. Typically: *repair* (the defect
   is in the evidence, the claim survives narrowed), *supersede* (the defect is at the root; write
   the banner, the `supersessions.yaml` entry, and a successor finding for the salvage), *retire*
   (nothing survives; the number is declared in `docs/design/finding-numbers.yaml`).
4. Your recommendation, and why.

Then wait. Do not proceed on a hard verdict without an explicit answer, and do not treat silence or
a general "go ahead" from earlier in the session as authorisation.

Everything **not** on that list you do autonomously: exactness downgrades of one class, missing or
unfalsifiable test records, stale external data, uncited prior art, scope creep between the finding
and its index line, look-elsewhere estimates, module and constant-registry defects.

---

## Step 4 — Verify each problem before acting

For every `Problem` row, reproduce the reviewer's claim yourself. Cheapest sufficient check, in
order:

- **numeric** — re-run the record (`casim test --id {id}`) and the perturbation
  (`casim test --param k=v`) and see the number the reviewer saw;
- **algebraic** — redo the step in sympy;
- **documentary** — open the file and the line; citations, exactness rows and index drift are
  settled by looking, not by reasoning;
- **external** — re-fetch the measured value with its uncertainty and date.

Assign the disposition now, from this closed vocabulary:

| Disposition | Meaning | What it requires |
|---|---|---|
| `APPLIED` | Verified, fixed, fix proved | The proof: a test that fails without it, or the re-run number |
| `APPLIED-PARTIAL` | Fixed as far as it goes | What remains, and where it is now tracked |
| `REJECTED` | The reviewer is wrong | A written counter-argument at review rigour, with the evidence |
| `DEFERRED` | Real, but its own piece of work | A **landing site** — a `docs/roadmaps/next-steps.md` entry. (It used to be legal to name a claimed finding number instead; numbers are no longer claimable in advance, so the roadmap entry is now the only landing site.) A deferral with no landing site is a silent drop |
| `ESCALATED` | Ben's call (Step 3), or needs a long run | The question asked, and the options put |
| `NOT-APPLICABLE` | The premise does not hold | Which premise, and why |

`REJECTED` is the disposition most likely to be reached for the wrong reason — because the fix is
tedious. The test: could you defend the rejection to the reviewer's own attack list? If not, it is
`DEFERRED`.

---

## Step 5 — Do the work

Order matters: **physics → module → constants → tests → finding → propagation.** Fixing the
finding's prose first and the physics after is how a corrected claim gets written that the code does
not support.

Every module, constant and test change follows the standard repo rules — CLAUDE.md
"Building or changing a module — the five registries". Nothing here overrides them: no literals
(import from `casim.constants`), no bare `numpy`/`scipy` (D8, `casim.numerics`), a `Module(...)` in
`_SPINE` for anything new, `Site(...)` entries for constants bound, a real registry record for every
test, and no artifact write outside `__main__`.

This is the attack-to-remedy map. It is the working core of the command:

| Attack | The defect | Remedy | Files that must move together |
|---|---|---|---|
| **1 Circularity** | Test asserts the script's own output | Re-point the assertion at an independent target (measurement, exact group-theory value, closed form). If the module must compute a registered constant *because that derivation is the physics*, declare a `MeasuredConstant` with a mandatory `reason` — do **not** rewrite the site to import the registry, that deletes the result | module · `constants/` · test record `expect` · finding `## Exactness` · `exactness-inventory.md` |
| **2 Input laundering** | Free inputs undercounted | Split the claim: derived *shape* and anchored *scale* are two claims with two classes. State the true input count | finding · `findings-index.md` line · `papers/Claims-and-Falsifiers-Summary.md` |
| **3 Exactness inflation** | Class higher than the weakest input | Downgrade. Propagate the weakest input through, and move the row between tiers in the inventory | finding `## Exactness` · `expect.exactness` in the record · `Module(exactness=…)` in `registry.py` · `exactness-inventory.md` |
| **4 Tolerance shopping** | Tolerance set after seeing the residual; or a zero that is zero by construction | Pre-register the tolerance from the physics. If the quantity is zero because the code enforces a symmetry, say so in the finding and add a test that *could* come out nonzero | test record · finding |
| **5 Numerology** | Coincidence, unquantified | Put the look-elsewhere estimate in the finding **as a number**. If the finding merged two registry constants that merely share a value, split them back — the repo rule is that values which coincide stay separate constants, and 2/9 is three of them | finding · `constants/` · the test asserting the split |
| **6 External data** | Stale or σ-free comparison | Update value, uncertainty, source and access date; restate agreement in σ or as a residual with a denominator | finding · results JSON if the comparison is computed · `exactness-inventory.md` |
| **7 Perturbation** | Verdict does not move under a perturbation that should change the physics | Rewrite the record so it can fail: real `module`/`entry`/`params`/`expect`. Then re-run the sweep and show the assertion moving. **A sweep never writes a baseline** — if anything armed one, `--restore` then `--apply` | `tests/registry/*.yaml` · possibly the module's entry signature |
| **8 Test-record integrity** | No record, or `legacy_script` | Write the record: real `kind`, `tier`, `sector`, `findings`, `module`, `entry`, `params`, `expect.exactness`. `legacy_script` is ratcheted debt — never add to it | `tests/registry/*.yaml` · `tests-index.md` (regenerated) |
| **9 Supersession hygiene** | Cites a dead or superseded finding | Fix the citation and carry the supersession. A result that *depends* on superseded physics is Step 3 territory, not a citation fix | finding · `supersessions.yaml` (**escalate first**) |
| **10 Scope creep** | Body, index line and summary disagree | Make all three say the narrowest supported version | finding · `findings-index.md` · `papers/Claims-and-Falsifiers-Summary.md` · `docs/status/*.md` |
| **11 Prior art** | Rediscovery presented as novel | Add a `## Prior art` section with the citation, and separate the two claims — "derived here" and "novel" are different and both can be true or false independently | finding |
| **12 Robustness** | Endpoint reported, trend not stated | Run the variation (size, discretisation, BCs, seed) and report the trend. If it does not survive, narrow the stated domain of validity | module run · results JSON · finding |
| **13 Falsifiability** | No named threshold | Add the experiment, the observable and the number that would kill it. For a closed-negative, state whether the no-go is *proved for the class* or *demonstrated for the cases tried* — that conflation is the standard defect | finding · `papers/Claims-and-Falsifiers-Summary.md` |

Two standing cautions while doing this work: check chiral/spinor quantities for dropped real or
imaginary parts before blaming the physics (that is what `casim.numerics.chiral` exists for), and
do not diff a result artifact you did not re-run — it proves nothing.

---

## Step 6 — Rewrite the finding

Correct the claim in place **and** leave the record of the correction. Both, always.

1. **Header** — add the `**Remediated:**` stamp (Step 9). Leave every prior `**Reviewed:**` line.
2. **Summary / Physics / Exactness** — state the corrected claim, at the corrected class, with the
   corrected input count. This is the version a reader acts on, so it must be clean, not
   caveat-laced.
3. **New `## Corrections` section**, after the body, before `## Status`:

```markdown
## Corrections

**{yyyy-mm-dd - hh:mm}** — per [independent review {date}](../docs/reviews/F{N}-review-{date}.md),
verdict **{VERDICT}**.

| Was | Now | Why | Attack |
|---|---|---|---|
| {the original statement, quoted} | {the corrected one} | {one line} | {#} |

Confirmed unchanged: {the highlights — what the review verified, and by which route}.
Rejected: {any recommendation not taken, one line each, with the counter-argument}.
```

4. **`## Status`** — carry the deferred items forward as the open questions they are.
5. **Pipes.** Escape literal `|` as `\|` in the title and every table cell — `findings-index.md` is
   generated from this file and an unescaped bar breaks the row.

If a successor finding is needed (Step 3 authorised it), it takes the lowest unused number in your
claim block, records `{N}: findings/F{N}-{slug}.md` in the claim's `used:` map in the same edit that
creates it, and links back to both the original and the review.

---

## Step 7 — Propagate

```bash
make indexes          # = casim index — all seven targets, from the registries
casim index --check   # exit 1 if anything is stale
```

Then check by hand the things the generators cannot know:

- `docs/status/exactness-inventory.md` — the row moved tiers if the class changed;
- `papers/Claims-and-Falsifiers-Summary.md` — input count and falsifier match the finding;
- `docs/roadmaps/next-steps.md` — every `DEFERRED` item has landed;
- `docs/design/session-claims.yaml` — `used:` reflects any number actually spent;
- the finding's regenerated `findings-index.md` line still renders (you edited tables — check the
  pipes).

---

## Step 8 — Verify

The barrier is `make gate`, not `pytest`. A green bare `pytest` has skipped the three `scenario`
records — `scenario-bcc-weyl`, `scenario-gluon-bcc`, `scenario-photon-pair` — which are precisely
the gates that run the engine on a lattice.

```bash
make gate                       # the barrier. Green before AND after.
make drift                      # only after re-running physics
casim test --finding F{N}       # every record verifying this finding
```

A single bash call dies at about 45 s, so run gate targets one at a time (`make health`,
`make registry`, `make numerics`, `make constants`, `make structure`) rather than through one
`run_gate.py` invocation. `source "$PWD/.vendor/activate.sh"` first; never `pip install`.
`git checkout -- <path>` may fail on this mount — restore with `git show HEAD:<path> > <path>`.

**Leave no modified baselines.** If a sweep or arming run rewrote one: `--restore`, then `--apply`.
A baseline that is out of date *because the physics improved* is a `stale_by_design` entry in
`supersessions.yaml`'s `baselines:` block with a `clears_by:` — and that is a supersession edit, so
it is Step 3 territory.

If `make gate` will not go green, **stop and report**. Do not disable a check, widen a tolerance to
pass, or mark a record `legacy_script` to get past it. A red gate at the end of a remediation is a
result: the fix is not yet right.

---

## Step 9 — Write the remediation report and the stamps

`docs/reviews/F{N}-remediation-{yyyy-mm-dd}.md` (append `-b`, `-c` … rather than overwrite):

```markdown
# Remediation — F{N}: {title}

**Remediated:** {yyyy-mm-dd - hh:mm}
**Against:** [independent review {date}](F{N}-review-{date}.md) — verdict **{VERDICT}**
**Outcome:** {n} APPLIED · {n} PARTIAL · {n} REJECTED · {n} DEFERRED · {n} ESCALATED
**Gate:** green \| red ({what}) · **Claim:** {session handle}, numbers {block}, used {list}

## What changed

{Three sentences. The corrected claim, and the one fix that mattered most.}

## Ledger

| # | Item | Kind | Disposition | Evidence / landing site |
|---|---|---|---|---|

## Confirmed by the review — and now stated

{The highlights. Where the finding was under-claiming and now is not.}

## Rejected recommendations

{One subsection each, with the counter-argument. If there are none, say so.}

## Physics and code changed

| File | Change | Why | Verified by |
|---|---|---|---|

## Exactness movement

| Result | Was | Now | Cause |
|---|---|---|---|

## Still open

{DEFERRED and ESCALATED items, each with where it now lives.}

## Method notes

{What could not be verified this run; anything that needed Ben's machine; the judgements you
were least sure of.}
```

Then two stamps.

**On the finding**, in the header block, under the `**Reviewed:**` line(s):

```markdown
**Remediated:** {yyyy-mm-dd} — {n} applied · {n} rejected · {n} deferred ([remediation](../docs/reviews/F{N}-remediation-{yyyy-mm-dd}.md))
```

**On the review file**, in its header block — this is the marker the sweep greps for, so it is not
optional:

```markdown
**Remediated:** {yyyy-mm-dd} — see [F{N}-remediation-{yyyy-mm-dd}.md](F{N}-remediation-{yyyy-mm-dd}.md)
```

Stamps accumulate. Never replace one.

---

## Step 10 — Close out

1. One dated paragraph in `docs/status/changelog.md`: the finding, the verdict acted on, what moved
   (class, inputs, tests, modules), and what was escalated.
2. `docs/status/project-status.md` only if a headline claim changed — then regenerate
   `project-status-index.md`.
3. Release the claim in `docs/design/session-claims.yaml`: `released:` timestamp and a
   `release_note:` saying what landed. There are no unused reserved numbers to report — a
   remediation that wrote no finding simply releases with an empty `used:` map, which now means
   exactly what it says.
4. `make indexes && casim index --check` one final time (the report and stamps are new docs).
5. Report to Ben: the corrected claim in one sentence, the disposition counts, the gate state, and
   anything escalated. Not a walkthrough — he has the report.

---

## Anti-patterns

- Applying a recommendation without reproducing the problem it names. The reviewer was cold on
  purpose; sometimes that means it was wrong.
- Rewriting the finding's body so the corrected claim is the only claim ever visible. The
  `## Corrections` table is the evidence the process worked.
- `REJECTED` because the fix is tedious. That is `DEFERRED`, with a landing site.
- A `DEFERRED` item with nowhere to land. It will not be picked up, and the ledger will say it was
  handled.
- Superseding or retiring a finding without asking. Always Step 3.
- Widening a tolerance, skipping a check, or relabelling a record `legacy_script` to get a green
  gate.
- Fixing the prose before the physics.
- Leaving a modified baseline behind after a sweep — next session reads it as a physics change.
- Chaining `/review-finding` and then editing the finding *while* the review is being written. The
  review must be finished, dated and stamped first, or its independence is fiction.
- Doing the whole thing and forgetting the stamp on the review file, so the sweep re-does it.
