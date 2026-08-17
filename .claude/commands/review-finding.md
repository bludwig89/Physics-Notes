# /review-finding — Independent third-party review of a finding

Run an **adversarial, cold-context review** of one finding and write a dated report to
`docs/reviews/`. The point is not to summarise the finding. The point is to try to break it,
starting from an independent re-derivation done by someone who has not read it.

Argument: the finding number (`F253`, or `253`). Optional flags:

- `--inline` — run in the current session instead of spawning subagents (cheaper, much weaker;
  the session that built the finding then reviews its own work — say so in the report header).
- `--fast` — skip Attack 7 (the perturbation sweep) and Attack 12 (robustness), which are the
  two slow ones. Record them as `NOT RUN`, never as `PASS`.

---

## The contract

> **A review changes nothing except two files.** It writes
> `docs/reviews/F{N}-review-{yyyy-mm-dd}.md` and adds **one** `**Reviewed:**` line to the
> finding's header block. That is the complete write set.
>
> Do **not** open a claim in `docs/design/session-claims.yaml`. Do **not** take a finding
> number. Do **not** edit the finding's body, its script, its tests, `open-derivations.md`,
> `exactness-inventory.md`, `supersessions.yaml`, or any physics module. If the review turns
> up a fix, the report *recommends* it and a later research session does it under its own
> claim. A reviewer who patches the thing under review has destroyed the evidence.

> **Independence is the deliverable.** Everything below exists to keep the reviewer from
> re-tracing the author's path. If you find yourself reasoning "the finding says X, and that
> follows because…", you are auditing, not reviewing. Stop and go back to Step 2.

---

## Step 0 — Timestamp and target

```bash
date "+%Y-%m-%d - %H:%M"
ls findings/ | grep -i "F{N}-"
```

Report file: `docs/reviews/F{N}-review-{yyyy-mm-dd}.md`. If one exists for today, append
`-b`, `-c`, … — never overwrite a prior review, including your own from an hour ago.

Create `docs/reviews/` if it does not exist.

---

## Step 1 — Extract the claim *without* absorbing the argument

Read **only** the finding's header block and its `## Summary` / opening statement — enough to
know what is being claimed, not how. Then write, in your own words, a **neutral claim card**:

```
TARGET      the quantity, relation or structural statement being claimed
VALUE       the number(s) claimed, with the exactness class claimed for each
INPUTS      what the finding says it is allowed to assume (constants, prior findings, anchors)
CLASS       EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | EXCLUDED  (as claimed)
FORBIDDEN   the finding file, its script, its test, its results JSON, its findings-index line
```

The claim card is what the blind agent gets. It must be *sufficient* (a competent physicist
could attempt the derivation from it) and *non-leading* (it must not contain the finding's
mechanism, its key substitution, or its punchline). Getting this card right is most of the
value of the whole command — a leaked mechanism turns Step 2 into a confirmation exercise.

Sanity test before proceeding: **could the claim card be written by someone reading only the
open-problem statement, before the finding existed?** If not, cut more out of it.

---

## Step 2 — Blind re-derivation (cold subagent A)

Spawn a fresh `general-purpose` agent. It has no memory of this session or of how the finding
was built. Give it, verbatim in the prompt:

- the claim card;
- the repo path and permission to read `CLAUDE.md`, `INDEX.md`, `docs/theory/key-decisions.md`,
  `src/casim/constants/`, and any **prerequisite** findings named in `INPUTS`;
- an explicit **forbidden list**: `findings/F{N}-*.md`, the finding's script and test module,
  its `test-results/*.json`, and its line in `findings-index.md`. Tell it that reading any of
  these invalidates the run and it must say so rather than continue;
- permission to write scratch scripts under the session outputs directory and run them
  (`source "$PWD/.vendor/activate.sh"` first — never `pip install`), and to use web search for
  measured values, group-theory facts, and standard results;
- the instruction: **derive the target independently, or report that you cannot.** "Cannot
  derive" is a first-class, useful answer. Do not reverse-engineer a path to the stated number.
- ask it to return: the derivation, its own number(s), the assumptions it had to add that the
  claim card did not license, and where it got stuck.

Two outcomes matter and they are graded differently:

| Blind agent outcome | Reading |
|---|---|
| Reaches the same value by a **different** route | Strongest possible support. Say which route. |
| Reaches the same value by the **same** route | Support, but the route may simply be forced — note it, do not oversell |
| Reaches a **different** value | Live discrepancy. Chase it in Step 3 before grading anything |
| **Cannot** derive without an extra assumption | The finding almost certainly carries that assumption implicitly. Name it — this is the single most common real finding of this command |

If the agent reports it read a forbidden file, discard its output and re-run with a tightened
prompt. Record the re-run in Method notes.

---

## Step 3 — Adversarial referee (cold subagent B)

Spawn a second fresh agent. This one reads **everything**: the finding, its script, its tests,
its results JSON, the cited prerequisites, `docs/theory/supersessions.yaml`. Hand it subagent
A's report and this attack list. Tell it its job is to **find the failure**, and that
"no failure found on attacks 1–13" is an acceptable and valuable result — but that returning a
sympathetic summary of the finding is a failed run.

Each attack returns `PASS` (attack failed to break it), `FAIL` (broke it — describe how),
`WEAKENS` (survives, but the claim must be narrowed) or `NOT RUN` (with a reason).

**1 — Circularity.** Does the test assert what the script computed, rather than what the physics
predicts? Trace the asserted number back: is it an *independent* target (measurement, exact
group-theory value, closed form) or the script's own output frozen into a baseline? Check the
constants registry: if the module imports a registered constant it is supposedly *deriving*,
that is circular unless declared as a `MeasuredConstant` with a `reason`.

**2 — Input laundering.** Count the free inputs actually consumed, not the ones claimed. A
result "derived given one anchor" is `FIT` with N=1. If the *shape* is derived and the *scale*
is anchored, the claim covers two different things and must be split. Does the finding's own
input count match the one in `Claims-and-Falsifiers-Summary.md`?

**3 — Exactness inflation.** Propagate the weakest input. An exact *method* applied to a fitted
*input* is not `EXACT`. Check the claimed class against `docs/status/exactness-inventory.md` and
against what the test actually asserts (tolerance, not adjective).

**4 — Tolerance shopping.** Was the tolerance set after seeing the residual? Is a `1e-12` gate
being claimed where the test asserts `1e-6`? Is a "machine precision" claim resting on a value
that is machine-precision *zero by construction* (a symmetry the code enforces, so it could not
have come out otherwise)?

**5 — Numerology / look-elsewhere.** For any claimed coincidence, estimate how many comparably
simple expressions from the same ingredient pool land within the same tolerance of the target.
The repo's own rule — *values that coincide stay separate constants* — exists because 2/9 is
three unrelated constants. Ask whether this finding merges two of them and calls it a
prediction. Quote the look-elsewhere estimate as a number, not a feeling.

**6 — External data currency.** Web-search the measured value being matched: PDG for particle
data, CODATA for constants, Planck/DESI/ACT for cosmology, the primary paper for anything else.
Check (a) the value is current, (b) its **uncertainty** is quoted, (c) agreement is stated in σ
or as a residual with a denominator, not as "excellent agreement". A finding that matches a
superseded measurement to 0.01% has a problem the finding cannot see.

**7 — Perturbation sweep (the test-has-a-failure-mode check).** Re-run the finding's registry
record at a perturbed input and confirm the assertion *moves*:

```bash
casim test --id {record-id}
casim test --param {key}={perturbed value}
```

If the verdict is identical under a perturbation that should change the physics, the test is not
testing. This is the sharpest single check in the list. A sweep never writes a baseline; if you
ran anything that armed one, restore with `python3 tools/arm_test_registry.py --restore` then `--apply`.

**8 — Test-record integrity.** Does a registry record exist at all (`tests-index.md`)? Does it
have a real `kind` and `expect.exactness`, or is it `legacy_script` (declared debt)? Does
`validate()` accept it — i.e. can it fail? A finding cited as settled with **no test record** is
a specific, reportable defect.

**9 — Supersession hygiene.** Every finding cited: does it still exist, and is it live? Check
`docs/theory/supersessions.yaml`. A citation to a superseded finding must carry the
supersession, and a result that *depends* on superseded physics is not merely mis-cited.

**10 — Scope creep.** Compare three statements of the claim: the finding body, its
`findings-index.md` one-liner, and any entry in `papers/Claims-and-Falsifiers-Summary.md` or
`docs/status/*.md`. They drift, and they drift in one direction. Report the widest version and
whether the body supports it.

**11 — Prior art and novelty.** Web-search the result. Is it a known theorem, a standard
identity, or already published? A rediscovery is still correct — but "derived" and "novel" are
different claims and the finding may be making both. Also check the negative case: has the
approach been tried and *excluded* in the literature?

**12 — Robustness.** Lattice size, discretisation, boundary conditions, seed. Does the result
survive a change that should be irrelevant? Cheap version: find the largest and smallest
parameter values the finding reports and ask whether the trend is stated or just the endpoint.

**13 — Falsifiability.** Is there a named experiment or measurement, with a threshold, that
would kill this? "Consistent with everything" is a defect, not a strength. If the finding is a
closed-negative (`EXCLUDED`), the corresponding question is: is the no-go **proved** for the
stated class, or demonstrated for the cases tried? Those are very different and get conflated.

---

## Step 4 — Grade

Merge A and B. Assign **one** overall verdict from this closed vocabulary:

| Verdict | Meaning |
|---|---|
| `CONFIRMED` | Independently re-derived, attacks survived, claim as stated is supported |
| `CONFIRMED-NARROWER` | The result holds, but the claim must be narrowed. State the narrowed claim in one sentence |
| `SUPPORTED-NOT-INDEPENDENT` | Attacks survived, but the blind route could not be made independent — the claim rests on the author's route alone |
| `UNDER-EVIDENCED` | Plausible, but the evidence offered does not reach the claimed class (usually an exactness or input-count problem) |
| `CIRCULAR` | The result is assumed somewhere in its own derivation or test |
| `OVERSTATED` | The computation is right; the claim built on it is not |
| `REFUTED` | A specific attack breaks it. Name the attack and the number |
| `INCONCLUSIVE` | The review could not be completed. Say exactly what blocked it |

Then per-axis grades, each with a one-line justification:

| Axis | Grades |
|---|---|
| Derivation | independent / forced-route / author-only / not-reproduced |
| Exactness class | as-claimed / one class lower / two or more lower |
| Free inputs | matches claim / undercounted by N |
| Test strength | fails-if-wrong / cannot-fail / no record |
| External data | current + σ quoted / stale / not compared |
| Novelty | novel / rediscovery / prior art exists |
| Falsifiability | named threshold / vague / none |

**A downgrade is a result.** Do not soften a verdict because the finding is well written or the
model is elegant elsewhere. Equally, do not manufacture a downgrade to look rigorous — if
thirteen attacks found nothing, `CONFIRMED` is the honest answer and saying so is the whole
value of an independent review.

---

## Step 5 — Write the report

`docs/reviews/F{N}-review-{yyyy-mm-dd}.md`:

```markdown
# Independent review — F{N}: {title}

**Reviewed:** {yyyy-mm-dd - hh:mm}
**Verdict:** {VERDICT}
**Mode:** cold subagents (blind re-derivation + adversarial referee) \| inline
**Attacks:** {p} PASS · {w} WEAKENS · {f} FAIL · {n} NOT RUN

## Verdict

{Two or three sentences. If not CONFIRMED, the narrowed or corrected claim in one sentence.}

## The claim, as the reviewer understands it

{The claim card, plus any place the finding's own statement of it was ambiguous.}

## Independent re-derivation

{What subagent A did, what it got, which route, what it had to assume that the claim card did
not license, where it stopped. Quote its number next to the finding's number.}

## Grades

| Axis | Grade | Why |
|---|---|---|

## Attacks

| # | Attack | Result | What it found |
|---|---|---|---|

## Numbers checked against external data

| Quantity | Finding | External value ± unc | Source | Residual / σ |
|---|---|---|---|---|

## What would falsify this

## Recommendations

{For a future research session, which will do them under its own claim. This review does none
of them. Rank by whether they change the verdict.}

## Method notes

{What could not be verified this run and why; any forbidden-file leak and re-run; commands that
timed out; the three judgements you were least sure of.}
```

Prose rules: no cheerleading, no restating the finding's strengths as though they were review
output. Escape literal pipes as `\|` — this file gets pulled into `docs-index.md`.

---

## Step 6 — Stamp the finding (the only edit permitted)

Add exactly one line to the finding's **header block** (after `**Status:**`, or after `**Date:**`
if there is no status line). Do not touch anything else in the file:

```markdown
**Reviewed:** {yyyy-mm-dd} — **{VERDICT}** ([independent review](../docs/reviews/F{N}-review-{yyyy-mm-dd}.md))
```

If a `**Reviewed:**` line already exists, **append** the new verdict on its own line rather than
replacing it. The sequence of verdicts over time is the useful record; a single overwritten line
hides a regression.

---

## Step 7 — Close out

1. `make indexes` then `casim index --check`. Confirm the review file appears in `docs-index.md`
   and that the finding's index line still renders (you edited its header — check the pipes).
2. `make gate` if anything was run that could have touched a baseline. If a sweep armed one:
   `--restore`, then `--apply`. **Never leave modified baselines behind** — the strict drift
   checker will flag them for the next session and it will look like a physics change.
3. One dated paragraph in `docs/status/changelog.md`: which finding, which verdict, the one
   attack that mattered.
4. Report to the user: verdict, the single most important finding of the review, and the top
   recommendation. Not a walkthrough.

---

## Anti-patterns

- Writing the claim card with the mechanism in it, so the blind agent confirms rather than derives.
- Letting subagent A read the finding "just for context". That is the entire experiment.
- Grading `CONFIRMED` on the strength of the finding's own test passing.
- Reporting attack 7 as `PASS` without having run the perturbation.
- "Excellent agreement" with no σ, no uncertainty, and no denominator.
- Fixing the problem you found. Recommend it; a research session with a claim does it.
- Reviewing a finding you wrote earlier in the same session inline and calling it independent.
- Editing `open-derivations.md` or `exactness-inventory.md` from a review run.
