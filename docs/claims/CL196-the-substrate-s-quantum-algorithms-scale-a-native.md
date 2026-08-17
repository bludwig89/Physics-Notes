---
id: CL196
title: 'The substrate''s quantum algorithms **scale**: a native controlled-phase + fully-compiled native CCZ extend the exact universality proof to 3-qubit controlled ga'
slug: 'the-substrate-s-quantum-algorithms-scale-a-native'
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F222]
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

# CL196 — The substrate's quantum algorithms **scale**: a native controlled-phase + fully-compiled native CCZ extend the exact universality proof to 3-qubit controlled ga

## Statement

The substrate's quantum algorithms **scale**: a native controlled-phase + fully-compiled native CCZ extend the exact universality proof to 3-qubit controlled gates, and multi-controlled Z/X (the exact action of the native Barenco ladder) let $n$-qubit Grover, Bernstein–Vazirani, QFT and GHZ run to $n\approx12$ with the $2^n$ register staying stable to machine precision (norm, unitarity, correct answers, bit-identical checkpointing)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F222-scaled-quantum-algorithms.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F222-scaled-quantum-algorithms.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Native CCZ/controlled-phase **exact-algebraic** ($<10^{-12}$; $2.2\times10^{-15}$); Grover matches the analytic success probability to $<10^{-6}$; QFT matches the DFT to $<10^{-10}$; BV deterministic; checkpoint bit-identical.

**Date:** 2026-07-01 - 18:40

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F222-scaled-quantum-algorithms.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
