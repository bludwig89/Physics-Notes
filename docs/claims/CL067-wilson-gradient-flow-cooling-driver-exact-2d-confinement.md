---
id: CL067
title: 'Wilson gradient flow / cooling driver + exact 2D confinement (static potential, string tension)'
slug: 'wilson-gradient-flow-cooling-driver-exact-2d-confinement'
tier: supporting
kind: derivation
status: live
domain: [QCD]
exactness: exact
findings: [F70]
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

# CL067 — Wilson gradient flow / cooling driver + exact 2D confinement (static potential, string tension)

## Statement

Wilson gradient flow / cooling driver + exact 2D confinement (static potential, string tension)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F70-gradient-flow-confinement-string-tension.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F70-gradient-flow-confinement-string-tension.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 6/6 (flow driver) + 8/8 (confinement) PASS; 7 results at machine ε / bit-for-bit, Creutz ratio & linear potential algebraically exact

**Date:** 2026-06-01 - 16:35

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F70-gradient-flow-confinement-string-tension.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
