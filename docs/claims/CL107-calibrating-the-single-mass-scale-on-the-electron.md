---
id: CL107
title: 'Calibrating the single mass scale on the electron: the locked-cell shape predicts the charged-lepton spectrum to 0.1 % from one mass and reads every fermion out'
slug: 'calibrating-the-single-mass-scale-on-the-electron'
tier: supporting
kind: prediction
status: live
domain: [SM]
exactness: unset
findings: [F120]
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

# CL107 — Calibrating the single mass scale on the electron: the locked-cell shape predicts the charged-lepton spectrum to 0.1 % from one mass and reads every fermion out

## Statement

Calibrating the single mass scale on the electron: the locked-cell shape predicts the charged-lepton spectrum to 0.1 % from one mass and reads every fermion out in kg — with the sharp lesson that the electron is the *worst* anchor (it sits at the condensate node) and the τ is the ideal one (exactly δ-stable at the wall)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F120-electron-calibrated-spectrum.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F120-electron-calibrated-spectrum.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 7/7 checks PASS (`test_F120_electron_calibrated_spectrum.py`, <1 s). Pure math/numpy (no scipy, per CLAUDE.md). Executes the F119 follow-up: fix the one open scale $N$ with the electron and turn the model's dimensionless shape into absolute masses (MeV and kg).

**Date:** 2026-06-09 - 16:30

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F120-electron-calibrated-spectrum.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
