---
id: CL214
title: 'F3 low-density lensing: falsification attempt fails (prediction survives)'
slug: 'f3-low-density-lensing-falsification-attempt-fails-prediction'
tier: supporting
kind: no_go
status: live
domain: [GR]
exactness: unset
findings: [F243]
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

# CL214 — F3 low-density lensing: falsification attempt fails (prediction survives)

## Statement

F3 low-density lensing: falsification attempt fails (prediction survives)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F243-f3-lowdensity-lensing-not-falsified.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F243-f3-lowdensity-lensing-not-falsified.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 6/6 checks PASS. Closes open-derivation **F1** (prompt #16; exactness-inventory not-yet-met #4 / next-steps line 5). The standing concern was that the **F3 lensing prediction fails at low fermion density**. Running the F3 symplectic Yukawa back-reaction at a ladder of fermion densities from $\rho=1$ down to $\rho=10^{-3}$, the $\lvert\Phi\rvert$-depression (the lensing source) **stays a correct-sign depression, remains positive-definite, never diverges, survives to the lowest density, and scales linearly** with density (weak-field log-log slope **1.012**, ideal 1.000). The prediction therefore **degrades gracefully as (source × coupling); it does not "fail" at low density**. Falsification attempt → **NOT FALSIFIED**.

**Date:** 2026-07-03 - 14:35

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F243-f3-lowdensity-lensing-not-falsified.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
