---
id: CL217
title: 'Subleading coefficients of the F26 even-rotation curl law: closed form + exact even-power vanishing (L2)'
slug: 'subleading-coefficients-of-the-f26-even-rotation-curl'
tier: supporting
kind: derivation
status: live
domain: [cosmology]
exactness: exact
findings: [F246]
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

# CL217 — Subleading coefficients of the F26 even-rotation curl law: closed form + exact even-power vanishing (L2)

## Statement

Subleading coefficients of the F26 even-rotation curl law: closed form + exact even-power vanishing (L2)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F246-f26-even-dispersion-subleading.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F246-f26-even-dispersion-subleading.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — closes open-derivation **L2** (`open-derivations-prompts-v2.md` Part 3; exactness-inventory "not-yet-met" #3 reframed / Tier-3 #5). The subleading coefficient of the F26 exact real-rotation EM propagator (`ca_wmu._f26_rotation_step`) is derived in closed form and verified to $4\times10^{-19}$. A stronger structural result comes for free: **all even-power dispersion corrections vanish identically**, so the leading Lorentz-violation signature is the CPT-even cubic $\lvert k\rvert^3$ term. Positive result, not a no-go.

**Date:** 2026-07-15 - 19:40

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F246-f26-even-dispersion-subleading.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
