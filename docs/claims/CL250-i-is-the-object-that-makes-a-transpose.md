---
id: CL250
title: 'ε = iσ₂ is the object that makes a transpose bilinear a 3-vector; and no live gauge sector was ever on the form that lacks it'
slug: 'i-is-the-object-that-makes-a-transpose'
tier: supporting
kind: derivation
status: withdrawn
domain: [SR]
exactness: exact
findings: [F302]
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

# CL250 — ε = iσ₂ is the object that makes a transpose bilinear a 3-vector; and no live gauge sector was ever on the form that lacks it

## Statement

ε = iσ₂ is the object that makes a transpose bilinear a 3-vector; and no live gauge sector was ever on the form that lacks it

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F302-sigma-bilinear-so3-covariance.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F302-sigma-bilinear-so3-covariance.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`withdrawn`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 6/6 checks PASS (`tests/findings/test_F302_bilinear_so3.py`, registry record `F302-bilinear-so3-covariance`, gate tier). The algebraic core is **Tier-1 exact** (sympy, six residuals identically zero); the covariance and amplitude measurements are machine precision on this tree's own modules.

**Date:** 2026-08-03 - 14:45

**A supersession/withdrawal banner appears in this finding's header**, which is why the card reads `withdrawn`. The specific ledger record has not been attached — do that before relying on this status.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F302-sigma-bilinear-so3-covariance.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
