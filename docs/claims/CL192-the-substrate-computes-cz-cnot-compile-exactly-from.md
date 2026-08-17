---
id: CL192
title: 'The substrate **computes**: CZ/CNOT compile **exactly** from the lattice exchange interaction ($\boldsymbol\sigma\!\cdot\!\boldsymbol\sigma$ commutes with $ZZ$;'
slug: 'the-substrate-computes-cz-cnot-compile-exactly-from'
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F218]
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

# CL192 — The substrate **computes**: CZ/CNOT compile **exactly** from the lattice exchange interaction ($\boldsymbol\sigma\!\cdot\!\boldsymbol\sigma$ commutes with $ZZ$;

## Statement

The substrate **computes**: CZ/CNOT compile **exactly** from the lattice exchange interaction ($\boldsymbol\sigma\!\cdot\!\boldsymbol\sigma$ commutes with $ZZ$; two exchange gates + a $\sigma_z$ give $e^{i\pi/4\,ZZ}$), and 2-qubit Grover + Deutsch–Jozsa run **live through the `casim` engine** — Grover finds every marked item with probability 1, checkpoint/resume mid-algorithm bit-identical

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F218-algorithm-through-the-engine.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F218-algorithm-through-the-engine.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Native gate compilation **exact-algebraic** (CZ/CNOT to $<10^{-12}$; $6\times10^{-16}$); Grover/DJ deterministic (probabilities exactly $0$/$1$); checkpoint/resume bit-identical.

**Date:** 2026-07-01 - 17:45

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F218-algorithm-through-the-engine.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
