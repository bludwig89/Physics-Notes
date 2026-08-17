---
id: CL193
title: 'First-principles α²F(ω) and the dynamic strong-coupling gap ratio via Padé continuation'
slug: 'first-principles-f-and-the-dynamic-strong-coupling'
tier: supporting
kind: derivation
status: withdrawn
domain: [GR]
exactness: exact
findings: [F218b]
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

# CL193 — First-principles α²F(ω) and the dynamic strong-coupling gap ratio via Padé continuation

## Statement

First-principles α²F(ω) and the dynamic strong-coupling gap ratio via Padé continuation

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F218b-alpha2F-firstprinciples-and-pade-gap-ratio.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F218b-alpha2F-firstprinciples-and-pade-gap-ratio.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`withdrawn`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 7/7 checks PASS. Part A derives the Eliashberg spectral function α²F(ω)=λω²/ω_max² from the F213 deformation potential on a Debye acoustic band (weight normalizes to λ exactly; ω_log=ω_max/√e exact), and shows T_c is nearly **shape-insensitive** at fixed ω_log — the reason F215's single Einstein mode already reproduced the data. Part B analytically continues Δ(iω_n) to the real axis (Vidberg-Serene Padé, mpmath), giving the strong-coupling reduced gap **2Δ₀/kT_c dynamically**: it rises from 3.56 (Al) to 4.6–4.7 (Pb, Hg), correlates with measured at r=0.988, and the first-principles Debye spectrum tightens it (mean error 6.4%→5.2%) because the gap ratio — unlike T_c — is shape-sensitive.

**Date:** 2026-07-01 - 03:20

**A supersession/withdrawal banner appears in this finding's header**, which is why the card reads `withdrawn`. The specific ledger record has not been attached — do that before relying on this status.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F218b-alpha2F-firstprinciples-and-pade-gap-ratio.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
