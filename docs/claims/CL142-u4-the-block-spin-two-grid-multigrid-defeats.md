---
id: CL142
title: 'U4: the block-spin two-grid multigrid defeats the scale-separation wall'
slug: 'u4-the-block-spin-two-grid-multigrid-defeats'
tier: supporting
kind: derivation
status: live
domain: [SM]
exactness: unset
findings: [F159]
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

# CL142 — U4: the block-spin two-grid multigrid defeats the scale-separation wall

## Statement

U4: the block-spin two-grid multigrid defeats the scale-separation wall

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F159-u4-blockspin-multigrid-scale-separation.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F159-u4-blockspin-multigrid-scale-separation.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (first build) — 4/4 checks PASS (`test_F159_multigrid_scale_separation.py`); accurate large-L sweep via `tests/runners/run_u4_multigrid.py`.

**Date:** 2026-06-17 - 20:23

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F159-u4-blockspin-multigrid-scale-separation.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
