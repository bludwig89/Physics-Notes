---
id: CL226
title: 'The infrared sector of QED: soft bremsstrahlung and the Bloch–Nordsieck cancellation of IR divergences'
slug: 'the-infrared-sector-of-qed-soft-bremsstrahlung-and'
tier: supporting
kind: derivation
status: live
domain: [QFT]
exactness: exact
findings: [F259]
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

# CL226 — The infrared sector of QED: soft bremsstrahlung and the Bloch–Nordsieck cancellation of IR divergences

## Statement

The infrared sector of QED: soft bremsstrahlung and the Bloch–Nordsieck cancellation of IR divergences

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F259-ir-bremsstrahlung.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F259-ir-bremsstrahlung.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 6/6 checks PASS. The eikonal factor, the current-conservation $k\cdot J=0$ / transverse-projector collapse, the soft IR-log $\int d\omega/\omega=\ln(\Delta E/\mu)$, and the Bloch–Nordsieck $\mu$-cancellation are **algebraically exact** (sympy, literal 0); the shared IR coefficient $f_{IR}(q^2)$ and the finite Sudakov observable are quantitative.

**Date:** 2026-07-22 - 14:10

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F259-ir-bremsstrahlung.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
