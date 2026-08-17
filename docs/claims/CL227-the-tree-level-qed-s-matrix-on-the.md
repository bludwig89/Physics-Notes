---
id: CL227
title: 'The tree-level QED S-matrix on the model''s fields, and the positron / charge-conjugation + crossing sector'
slug: 'the-tree-level-qed-s-matrix-on-the'
tier: supporting
kind: derivation
status: live
domain: [QFT]
exactness: exact
findings: [F260]
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

# CL227 — The tree-level QED S-matrix on the model's fields, and the positron / charge-conjugation + crossing sector

## Statement

The tree-level QED S-matrix on the model's fields, and the positron / charge-conjugation + crossing sector

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F260-qed-scattering-smatrix.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F260-qed-scattering-smatrix.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 11/11 gates PASS. Charge conjugation ($C\gamma^\mu C^{-1}=-(\gamma^\mu)^\top$), the crossing relations, and the Ward identities are **algebraically exact** (sympy, literal 0); every spin-averaged $\lvert\mathcal M\rvert^2$ equals the textbook Mandelstam closed form to **machine precision**; the Klein–Nishina, Møller/Bhabha, Dirac-annihilation and $\mu$-pair cross sections reproduce the closed-form textbook results by phase-space integration; Compton reduces to Thomson.

**Date:** 2026-07-22 - 16:20

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F260-qed-scattering-smatrix.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
