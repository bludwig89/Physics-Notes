# docs/reviews/ — independent third-party reviews of findings

One file per review: `F{N}-review-{yyyy-mm-dd}.md`. Written by the `/review-finding` command
(`.claude/commands/review-finding.md`), which runs an **adversarial, cold-context** review — a
blind re-derivation by an agent that has not read the finding, followed by a referee that reads
everything and tries thirteen named attacks.

## Why this is separate from `docs/audits/`

`docs/audits/` grades the *project* — sweeps across sectors, kernel coverage, the physics audit.
This folder grades **one finding at a time**, against the question a referee would ask: *does the
evidence offered reach the class claimed, and could someone who did not build it get there?*

`docs/status/completeness-*.md` (from `/state-of-model`) asks a third question — what a complete
theory owes that the model has no sector for. The three do not overlap and none substitutes for
the others.

## What a review may change

Exactly two files: the report in this folder, and **one** `**Reviewed:**` line in the finding's
header block. A review takes no finding number, opens no claim in
`docs/design/session-claims.yaml`, and never edits a physics module, a test, `open-derivations.md`,
`exactness-inventory.md` or `supersessions.yaml`. Where it finds a defect it *recommends* a fix; a
later research session does the fix under its own claim.

## The other half — `/remediate-finding`

A recommendation that nobody actions is a review that did not happen. `/remediate-finding`
(`.claude/commands/remediate-finding.md`) is the inverse command: it reads a review and makes the
repo true to it. Its contract is the mirror image — **every recommendation and every `FAIL`/
`WEAKENS` attack row gets exactly one disposition, written down**, from the closed vocabulary
`APPLIED · APPLIED-PARTIAL · REJECTED · DEFERRED · ESCALATED · NOT-APPLICABLE`. There is no state
where an item quietly does not appear.

It *is* a research session, so it opens a claim, takes finding numbers, edits the physics modules,
the constants and test registries, the finding itself and every index, and it has to leave
`make gate` green. Two things it never does alone: act on a `REFUTED` or `CIRCULAR` verdict, or
touch a canonical decision (`CLAUDE.md` "Core Design Decisions", `docs/theory/key-decisions.md`,
`supersessions.yaml`) — those stop and ask Ben with the salvage and the options laid out.

It writes `F{N}-remediation-{yyyy-mm-dd}.md` alongside the review, stamps the finding header with
`**Remediated:**`, and stamps the **review file** too. That last stamp is the sweep marker:

```bash
grep -L '^\*\*Remediated:\*\*' docs/reviews/F*-review-*.md   # reviews not yet actioned
```

Reviews and remediations both accumulate. A finding may carry several of each, and the sequence —
verdict, fix, re-review — is the record that shows whether the fix held.

## Verdict vocabulary (closed)

| Verdict | Meaning |
|---|---|
| `CONFIRMED` | Independently re-derived, attacks survived, claim as stated is supported |
| `CONFIRMED-NARROWER` | The result holds, the claim must be narrowed — the narrowed claim is stated |
| `SUPPORTED-NOT-INDEPENDENT` | Attacks survived, but the claim rests on the author's route alone |
| `UNDER-EVIDENCED` | Plausible; the evidence does not reach the claimed exactness class or input count |
| `CIRCULAR` | The result is assumed somewhere in its own derivation or its test |
| `OVERSTATED` | The computation is right; the claim built on it is not |
| `REFUTED` | A named attack breaks it |
| `INCONCLUSIVE` | The review could not be completed — what blocked it is stated |

A finding may be reviewed more than once. Verdict lines **accumulate** in the finding header
rather than being overwritten, because the sequence is what shows a regression.

## Reading the reports

The most useful sections are **Independent re-derivation** (did a cold agent get there, and by
which route) and the `FAIL` / `WEAKENS` rows of the **Attacks** table. A review whose attack table
is all `PASS` and whose re-derivation is `independent` is the strongest support any finding in this
repo can carry; one where the blind agent needed an assumption the claim card did not license has
named an implicit posit, which is usually the real result.
