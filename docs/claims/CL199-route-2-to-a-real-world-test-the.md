---
id: CL199
title: 'Route 2 to a real-world test: the model''s native **doublon leakage** reproduces measured semiconductor exchange-qubit leakage. The closed-form leakage $d=\tfrac'
slug: 'route-2-to-a-real-world-test-the'
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F225]
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

# CL199 — Route 2 to a real-world test: the model's native **doublon leakage** reproduces measured semiconductor exchange-qubit leakage. The closed-form leakage $d=\tfrac

## Statement

Route 2 to a real-world test: the model's native **doublon leakage** reproduces measured semiconductor exchange-qubit leakage. The closed-form leakage $d=\tfrac12(1-1/\sqrt{1+(4t/U)^2})$ equals the second-quantized ground-state double occupancy to $10^{-17}$, scales as $(2t/U)^2$ (log-log slope $1.9997$), and its magnitude matches the GaAs singlet–triplet qubit's measured $0.13\%$ leakage at $t/U\approx0.018$ — a standard exchange-qubit operating regime

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F225-doublon-leakage-spinqubit.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F225-doublon-leakage-spinqubit.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 4/4 checks PASS. Closed-form leakage **exact-algebraic** vs diagonalisation ($5.6\times10^{-17}$); $(2t/U)^2$ scaling (log-log slope $1.9997$); magnitude matches the measured $0.13\%$ GaAs leakage at $t/U=0.0181$; consistent with the F220 field-native gate leakage.

**Date:** 2026-07-01 - 21:45

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F225-doublon-leakage-spinqubit.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
