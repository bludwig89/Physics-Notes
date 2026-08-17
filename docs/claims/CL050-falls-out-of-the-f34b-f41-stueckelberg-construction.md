---
id: CL050
title: '$m_A = 0$ falls out of the F34b+F41 Stueckelberg construction as a rank-deficient mass matrix; the notebook''s \"anomalous\" cross term is the off-diagonal entry t'
slug: 'falls-out-of-the-f34b-f41-stueckelberg-construction'
tier: supporting
kind: derivation
status: live
domain: [SR]
exactness: unset
findings: [F44]
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

# CL050 — $m_A = 0$ falls out of the F34b+F41 Stueckelberg construction as a rank-deficient mass matrix; the notebook's "anomalous" cross term is the off-diagonal entry t

## Statement

$m_A = 0$ falls out of the F34b+F41 Stueckelberg construction as a rank-deficient mass matrix; the notebook's "anomalous" cross term is the off-diagonal entry that W6.1 diagonalises

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F44-higgs-free-mA-zero-from-rank1-stueckelberg.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F44-higgs-free-mA-zero-from-rank1-stueckelberg.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 tests PASS; the covariant Stueckelberg operator now lives in `ca_wmu.py` and the rank-1 verification calls it directly

**Date:** 2026-05-27 - 23:55 (proposed); 2026-05-28 - 00:05 (W6.6–W6.8 Confirmed); 2026-05-28 - 00:20 (W6.9 lattice Confirmed); 2026-05-28 - 00:40 (operator promoted to `ca_wmu.py`, W6.10 sanity added)

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F44-higgs-free-mA-zero-from-rank1-stueckelberg.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
