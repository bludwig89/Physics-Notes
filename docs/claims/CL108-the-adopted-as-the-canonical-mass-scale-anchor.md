---
id: CL108
title: 'The τ adopted as the canonical mass-scale anchor: wall-pinned ⇒ exactly δ-stable, so it contributes zero anchor error and gives the standard lepton/kg readout ('
slug: 'the-adopted-as-the-canonical-mass-scale-anchor'
tier: supporting
kind: derivation
status: live
domain: [SM]
exactness: unset
findings: [F121]
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

# CL108 — The τ adopted as the canonical mass-scale anchor: wall-pinned ⇒ exactly δ-stable, so it contributes zero anchor error and gives the standard lepton/kg readout (

## Statement

The τ adopted as the canonical mass-scale anchor: wall-pinned ⇒ exactly δ-stable, so it contributes zero anchor error and gives the standard lepton/kg readout (m_μ to −0.00 %, m_e to −0.06 %)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F121-tau-anchored-canonical-spectrum.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F121-tau-anchored-canonical-spectrum.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS (`test_F121_tau_anchored_canonical_spectrum.py`, <1 s). Pure math (no scipy, per CLAUDE.md). Adopts the τ as the standard mass-scale anchor in place of the electron, per the F120 robustness lesson.

**Date:** 2026-06-09 - 17:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F121-tau-anchored-canonical-spectrum.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
