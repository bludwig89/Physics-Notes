# /claim — Write or update a claim card (decision D12)

**Argument:** a `CL###` (update that card), an `F###` (write the card for that finding), or free text describing the assertion.

---

## What you are producing

One file, `docs/claims/CL{NNN}-{slug}.md`, from `docs/claims/TEMPLATE.md`.

**A claim is not a finding.** A finding is a research record — past tense, written once, superseded rather than rewritten, and *correct to keep saying what it concluded*. A claim has a **present tense**: it is what the project is willing to defend right now, and it can be narrowed, made contingent or withdrawn without touching the finding that produced it.

Read `docs/claims/README.md` before writing. It holds every closed vocabulary with its meaning and the reasoning behind each.

## Hard constraints

1. **A card never edits a finding, a physics module, a test record, `docs/status/exactness-inventory.md`, or `docs/theory/supersessions.yaml`.** If the position changed because the *physics* changed, that is a research session with its own claim on `docs/design/session-claims.yaml` and its own finding number. Do that first; update the card after.
2. **Numbers verbatim from the source.** No rounding, no "approximately" the source did not say, no upgrading a `quantitative` residual to `exact` because it looks tight.
3. **`falsifier: none` requires the structural reason to be *named* in the `## Falsifier` section.** "It is structural" is a reason only when the structure is named. If you cannot name it, the honest value is `unset`, which is ratcheted debt.
4. **There is no `unknown` status.** A claim whose status you cannot determine is `open` **with the gap written down** — that is a state someone can act on.
5. **Never delete a `withdrawn` or `no_go` card.** They are the retraction and falsification record. A withdrawn claim that is deleted is a claim that gets re-made.

## Procedure

1. **Take the id** from `next_claim` in `docs/claims/registry.yaml`. `CL` does not overlap `F<N>`, `D<N>`, `S<N>` or `C0`–`C9`, so it needs no reservation on the session-claims board — but if you are also doing physics, open a board claim for *that*.
2. **Check the bar.** Does this extend, derive, or contradict something in QM / SM / GR / SR / QFT? If the honest answer is "nothing established — this is internal", **the card should not exist.** Record the judgement in `docs/audits/consolidation-plan-2026-08-04.md` §5 instead, so "no card" is a decision rather than an omission.
3. **Check whether it is already carried.** `grep` `claims-index.md`. One authored card often rests on five or six findings, and a second card for one of those findings double-counts the same assertion.
4. **Write the statement first**, in one or two sentences, so a reader who disagrees knows exactly what they are disagreeing with. Everything else is supporting.
5. **Fill `## Evidence` with test-registry records and result artifacts**, not just the finding's prose. *A claim whose only evidence is the prose of its own finding is `review_state: unreviewed-seed`, not `authored`* — that is the promotion criterion, and it is the whole difference between the 28 authored cards and the 223 seeds.
6. **`## Status & history` carries the reason the `status` field says what it says.** If `narrowed`, the broad form that was withdrawn goes here with the date and what narrowed it. If `withdrawn`, this section *is* the retraction record and is the most important part of the card.
7. **`make claims && make gate`.** Then a one-paragraph entry in `docs/status/changelog.md`.

## Promoting a seed

`review_state: unreviewed-seed` means the finding is the evidence and the card is **not yet independent of it** — the classification was extracted mechanically and no reviewer has confirmed it. Promotion to `authored`, in order:

1. Confirm or correct `domain`, `kind` and `exactness` by reading the finding, not its title.
2. Name the specific established result it extends, in `## What it extends`.
3. Name the test-registry records and result artifacts in `## Evidence`.
4. State a falsifier, or set `falsifier: none` **with the structure named**.
5. Set `review_state: authored`, then `python3 tools/check_claims.py --ratchet-update` so the debt ceiling falls.

If the finding is thin enough that you cannot do (2) or (3), that is a `/review-finding` job, not a card edit.

## When a review comes back OVERSTATED or REFUTED

That verdict has, by definition, found a claim card whose `status` is wrong. The handoff is `/review-finding` → `/remediate-finding` → **the card's status moves**. A review that corrects a finding and leaves the claim standing has fixed the record and not the assertion.
