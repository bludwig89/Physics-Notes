---
id: CL101
title: 'The SI prediction registry: every measurable the canonical cell now produces, gated against current data'
slug: 'the-si-prediction-registry-every-measurable-the-canonical'
tier: supporting
kind: prediction
status: live
domain: [QCD]
exactness: unset
findings: [F112]
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

# CL101 — The SI prediction registry: every measurable the canonical cell now produces, gated against current data

## Statement

The SI prediction registry: every measurable the canonical cell now produces, gated against current data

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F112-si-predictions-from-canonical-a.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F112-si-predictions-from-canonical-a.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 18/18 checks PASS (`test_F112_si_predictions.py`, 0.16 s). **Numbering note:** drafted as F111; renumbered to F112 — F111 was already taken (2026-06-07) by the concurrent second-order-deflection and F110 tree-gauge SU(3) test scripts. Real arithmetic + sympy only (no chiral transforms). Two headline numbers independently re-derived outside the harness. This finding is a *registry*, not a new derivation: it collects what F107's SI lock unlocked and scores each item against the best current measurement.

**Date:** 2026-06-08 - 14:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F112-si-predictions-from-canonical-a.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
