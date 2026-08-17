---
id: CL198
title: 'Route 1 to a real-world test: the derived super-exchange is **SI-anchored** and confronts measured cold-atom data. The sector reduces exactly to the two-site Hu'
slug: 'route-1-to-a-real-world-test-the'
tier: supporting
kind: no_go
status: live
domain: [GR]
exactness: exact
findings: [F224]
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

# CL198 — Route 1 to a real-world test: the derived super-exchange is **SI-anchored** and confronts measured cold-atom data. The sector reduces exactly to the two-site Hu

## Statement

Route 1 to a real-world test: the derived super-exchange is **SI-anchored** and confronts measured cold-atom data. The sector reduces exactly to the two-site Hubbard gap $J=\tfrac12(\sqrt{U^2+16t^2}-U)$ (verified vs diagonalisation to $10^{-16}$), reproduces Trotzky et al.'s confirmed $4t^2/U$ scaling and its millisecond coherent-oscillation timescale (entangling time $1/4J=0.25$–$50$ ms across the measured 5 Hz–1 kHz), and makes one falsifiable refinement — at the measured symmetric-well point $J/U=0.08$ the **exact** gap is $6.93\%$ below the textbook leading order

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F224-qc-si-coldatom.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F224-qc-si-coldatom.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 4/4 checks PASS. Exact-gap identity **exact-algebraic** ($2.7\times10^{-16}$ vs Hubbard diagonalisation); $4t^2/U$ scaling reproduced to machine zero; dimensionful timescales reproduce the measured millisecond band; predicted exact-gap refinement $-6.93\%$ at $J/U=0.08$.

**Date:** 2026-07-01 - 21:10

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F224-qc-si-coldatom.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
