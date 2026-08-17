---
id: CL092
title: 'The $\gamma(\Omega)$ map from the QCA rule''s transfer operator: the centre-weight disorder is the vacuum flux variance, a Brillouin-zone average of the inverse '
slug: 'the-map-from-the-qca-rule-s-transfer'
tier: supporting
kind: derivation
status: live
domain: [SM]
exactness: exact
findings: [F100]
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

# CL092 — The $\gamma(\Omega)$ map from the QCA rule's transfer operator: the centre-weight disorder is the vacuum flux variance, a Brillouin-zone average of the inverse 

## Statement

The $\gamma(\Omega)$ map from the QCA rule's transfer operator: the centre-weight disorder is the vacuum flux variance, a Brillouin-zone average of the inverse rotation rate

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F100-gamma-from-transfer-operator.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F100-gamma-from-transfer-operator.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. T1 machine-precision (oscillator vacuum moment, number-basis); T2 convergent BZ quadrature (Richardson, $r=0.499$); T3 exact clock inversion (round-trip $10^{-16}$); T4 exact limits; T5 reconciliation (consistency, explicitly not an identity). **Closes the last gap flagged in F99 §5** — the exact $\gamma(\Omega)$ map.

**Date:** 2026-06-05 - 15:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F100-gamma-from-transfer-operator.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
