---
id: CL115
title: 'Block-spin RG for the free paired-photon: c_lat is an exact RG fixed point and the lattice-artifact (LIV) operators are irrelevant ($\lambda_n=b^{-n}$), so a co'
slug: 'block-spin-rg-for-the-free-paired-photon'
tier: supporting
kind: derivation
status: live
domain: [QCD]
exactness: exact
findings: [F129]
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

# CL115 — Block-spin RG for the free paired-photon: c_lat is an exact RG fixed point and the lattice-artifact (LIV) operators are irrelevant ($\lambda_n=b^{-n}$), so a co

## Statement

Block-spin RG for the free paired-photon: c_lat is an exact RG fixed point and the lattice-artifact (LIV) operators are irrelevant ($\lambda_n=b^{-n}$), so a coarse photon simulation reproduces the fine one

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F129-blockspin-free-photon.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F129-blockspin-free-photon.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Part A is **Tier-1 exact** (sympy, symbolic in $b$); T1/T2/K/RS/V are **machine-precision** (FFT/round-off floor). This is the free-photon half of Phase 1 of `docs/roadmaps/roadmap-scale-to-real-space.md`; the gauge + gravity + confinement half is [[F130-blockspin-gauge-gravity]] (`ca_blockspin.py`).

**Date:** 2026-06-11

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F129-blockspin-free-photon.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
