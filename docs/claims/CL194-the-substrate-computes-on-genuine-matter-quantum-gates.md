---
id: CL194
title: 'The substrate computes on **genuine matter**: quantum gates and a full Deutsch–Jozsa run directly on the second-quantized fermionic Fock sector — single-qubit g'
slug: 'the-substrate-computes-on-genuine-matter-quantum-gates'
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F220]
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

# CL194 — The substrate computes on **genuine matter**: quantum gates and a full Deutsch–Jozsa run directly on the second-quantized fermionic Fock sector — single-qubit g

## Statement

The substrate computes on **genuine matter**: quantum gates and a full Deutsch–Jozsa run directly on the second-quantized fermionic Fock sector — single-qubit gates are exact fermionic operators $\exp(-i\,2\theta\,\hat n\!\cdot\!\mathbf S_s)$ (zero leakage), the two-qubit entangler is the **real Hubbard time-evolution** whose emergent super-exchange becomes the exact exchange gate as $U/t\to\infty$, and the algorithm's threshold verdict is correct despite sub-percent doublon leakage

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F220-field-native-execution.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F220-field-native-execution.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Single-qubit fermionic gates **exact-algebraic** (match to $8.3\times10^{-16}$, occupation conserved to $10^{-12}$); entangler fidelity $\to1$ and spin entropy $\to\ln2$ as $U/t$ grows; field-native CNOT correct to $<1\%$ (leakage-limited); Deutsch–Jozsa verdict correct on all four oracles; live channel + checkpoint bit-identical.

**Date:** 2026-07-01 - 19:30

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F220-field-native-execution.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
