# `docs/claims/` — the claim cards (**D12**)

*Created 2026-08-04 - 21:06. One file per claim. `registry.yaml` and `claims-index.md`
are generated from these files; `tools/check_claims.py` is wired into `make gate`.*

## What a claim is, and why it is not a finding

A **finding** is a research record: what a session did, how it did it, and what came out.
It is written once and is thereafter a historical artifact — findings do not get rewritten
when the model moves, they get superseded, and that is correct.

A **claim** is the assertion the project is currently willing to defend. It has a *present
tense*. It can be narrowed, made contingent, or withdrawn without touching the finding that
produced it, and the card is where that change gets written down.

The two are different objects and the project was carrying only one of them. The symptom was
`papers/Claims-and-Falsifiers-Summary.md`: a prose document whose revision 2 had to withdraw a
core claim and four falsifiers in a blockquote, and whose revision 3 had to say *revision 2 was
wrong about charge quantisation* in a second blockquote. Both corrections were right. Neither
was checkable, discoverable from the finding, or countable. A claim with no record of its own
can only be corrected by editing the paragraph that states it.

## The standing rule

> **Any algebraic or physics-tested claim or element that extends, derives, or contradicts
> anything in quantum mechanics, the Standard Model, general relativity, or special relativity
> gets a card here and a row in the registries it touches.**

Stated in `CLAUDE.md` under "Project Structure". The bar is *extends established physics*, not
*is interesting* — an engine-wiring result, a numerical technique, a refactor, or a status
record does not get a card. Where a finding is judged not to clear the bar, that judgement is
itself recorded (in `docs/audits/consolidation-plan-2026-08-04.md` §"No card"), so "no card"
is a decision rather than an omission.

## File layout

```
docs/claims/
  README.md              this file — the contract
  TEMPLATE.md            the card skeleton; `/claim` copies it
  registry.yaml          GENERATED from the cards. Do not hand-edit.
  CL001-....md           the cards
```

Cards are `CL{NNN}-{slug}.md`. **`CL` is a new ID namespace** and deliberately does not
overlap `F<N>` findings, `D<N>` engineering decisions, `S<N>` supersession-ledger records, or
the `C0`–`C9` roadmap phases.

## Direction of generation — and why it runs backwards from the other registries

Everywhere else in this repo the registry is the hand-owned source and the index is generated:
`_SPINE` → `code-index.md`, `tests/registry/*.yaml` → `tests-index.md`. Here it is inverted.
**The card's YAML front-matter is the record. `registry.yaml` is generated from the cards, and
`claims-index.md` is generated from the registry.**

The reason is that a module cannot carry its own metadata — the code is the artifact and the
registry has to live beside it — whereas a claim's prose and its metadata are the same object.
Splitting them would create exactly one thing: a card whose status line disagrees with its
registry row. Since nothing can be true in two places, the card wins and the registry is a
projection.

Regenerate with `make claims` (= `casim index --only claims`); `make gate` fails on a stale one.

## Front matter must be SINGLE-quoted

Claim titles carry LaTeX. A **double**-quoted YAML scalar processes escape
sequences, so `title: "…\dim(E_g)…"` is an *invalid-escape parse error*, not a
string. A **single**-quoted scalar is literal and its only escape is `''` for a
quote — which is the right container for arbitrary maths and needs no escaping
table to get right.

This is not hypothetical. 28 of the first 251 cards shipped with double-quoted
LaTeX titles: unreadable by PyYAML, and by every editor and tool that uses it,
while `check_claims.py`'s own small hand-rolled reader accepted them happily.
The reader is deliberately forgiving so the gate can run without the vendored
path active — and forgiving was exactly the failure mode. `check_claims.py` now
*also* parses the front matter with PyYAML when it is importable, and fails if
the two disagree. A negative control confirms the check bites.

## Vocabularies (closed — `check_claims.py` enforces every one)

### `tier`

| Value | Meaning |
|---|---|
| `headline` | A claim the project makes publicly. These are the rows of `Claims-and-Falsifiers-Summary.md`. |
| `supporting` | A claim that stands on its own but is not part of the public headline set. Usually `rolls_up_to` a headline card. |

### `kind`

| Value | Meaning |
|---|---|
| `derivation` | The model derives something established theory takes as an input. |
| `deviation` | The model predicts something numerically different from established theory. |
| `reinterpretation` | Same numbers, different underlying ontology. The strongest form of "no new prediction, new explanation". |
| `prediction` | A falsifiable forecast with a stated threshold. |
| `no_go` | An exclusion: an option the model has closed. **These are the falsification record and are the last thing that should ever be archived.** |
| `non_claim` | An explicit scope boundary — something deliberately *not* asserted, recorded so that absence is not read as a prediction. |

### `status`

| Value | Meaning |
|---|---|
| `live` | Supported as stated. |
| `narrowed` | The result holds; the claim as first stated was too broad. **The card states the narrow form**, and the broad form goes in `## Status & history`. |
| `contingent` | Holds granted a named hypothesis or input. The card must name it. |
| `open` | Asserted, evidence incomplete. The gap must be named. |
| `withdrawn` | Retracted. **The card stays** — it is the retraction record, and a withdrawn claim that is deleted is a claim that gets re-made. |
| `not_claimed` | A scope boundary; the project does not assert this. |

There is no `unknown`. A claim whose status cannot be determined is `open` with the reason
written down, which is a state someone can act on.

### `domain`
`QM` · `SM` · `GR` · `SR` · `QFT` · `QCD` · `cosmology` · `condensed-matter` · `none`

### `exactness`
The same closed set as `casim.constants.EXACTNESS_CLASSES` and
`docs/status/exactness-inventory.md`: `exact` · `machine` · `quantitative` · `bracketed` ·
`external`, plus `unset` for a card that has not yet been classified. **`unset` is ratcheted
down; do not add to it.**

### `falsifier`
`stated` (a `## Falsifier` section exists and is non-empty) · `none` (the claim is structural
and admits no observational falsifier — the card must say *why*) · `unset` (debt; ratcheted).

### `review_state`
`authored` (a human or a session wrote the physics into the card) ·
`unreviewed-seed` (mechanically extracted from the finding text; the statement is the
finding's own words and **no reviewer has confirmed the classification**).

`unreviewed-seed` is not a synonym for "probably fine". It means the *finding* is the evidence
and the *card* is not yet independent of it.

## The rule that does real work

`check_claims.py` fails a card that is `status: live` when **every** finding it rests on is
named in a `superseded:` list in `docs/theory/supersessions.yaml`. That is the machine-checkable
form of "overstated", and it is the check the Claims-and-Falsifiers revisions 2 and 3 would have
tripped months before a human noticed.

It deliberately does **not** fire on a *partial* supersession. The standing lesson of this repo —
recorded in `deprecated/README.md` and re-confirmed by the 2026-08-04 header triage — is that
almost nothing here is superseded wholesale: of 14 test files one audit called superseded,
exactly one was. A check that flagged partials would train people to ignore it.

## What a claim card may and may not change

A card is a *statement of position*. Writing or editing one **never** edits a finding, a physics
module, a test record, the exactness inventory, or the supersession ledger. If the position
changes because the physics changed, the physics change is a research session with its own claim
on `docs/design/session-claims.yaml` and its own finding number; the card is updated to match
afterwards.

The inverse also holds and is the point of the layer: **a finding may be superseded without any
claim changing**, and a claim may be narrowed without any finding changing. Neither event is
visible in the other object.

## Relationship to the neighbours

| Object | Question it answers |
|---|---|
| `findings/F{N}-*.md` | What did we do, and what came out? |
| `docs/claims/CL{N}-*.md` | What do we assert, right now, and what would kill it? |
| `docs/theory/supersessions.yaml` | What replaced what, and what survived? |
| `docs/reviews/F{N}-review-*.md` | Does the evidence reach the class claimed? |
| `docs/status/exactness-inventory.md` | To what precision does each result hold? |
| `docs/audits/` | How is the project as a whole doing? |
| `deprecated/` | What is out of the tree, and by what rule? |

A review that returns `OVERSTATED` or `REFUTED` has, by definition, found a claim card whose
`status` is wrong. That is the intended handoff: `/review-finding` → `/remediate-finding` →
the card's status moves.
