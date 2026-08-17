---
id: CL090
title: 'The enforcer of the centre-phase budget is itself the binder (closing the F97 §4/§8 bridge)'
slug: 'the-enforcer-of-the-centre-phase-budget-is'
tier: supporting
kind: derivation
status: live
domain: [SM]
exactness: exact
findings: [F98]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-08-04'
last_verified: '2026-08-04'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL090 — The enforcer of the centre-phase budget is itself the binder (closing the F97 §4/§8 bridge)

## Statement

The enforcer of the centre-phase budget is itself the binder (closing the F97 §4/§8 bridge)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F98-enforcer-is-binder.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F98-enforcer-is-binder.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. E1/E3/E5 algebraically exact (sympy/integer), E2 exact (BPS Tier-1, F86), E4 machine-precision round-trip (Tier-2). Builds the quantitative bridge that F97 §4 *theorized* and §8 flagged as open.

**Date:** 2026-06-05 - 14:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F98-enforcer-is-binder.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
