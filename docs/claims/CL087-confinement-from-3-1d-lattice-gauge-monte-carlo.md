---
id: CL087
title: 'Confinement from 3+1D lattice-gauge Monte-Carlo (P1 Option A), tested against Option C (F86)'
slug: 'confinement-from-3-1d-lattice-gauge-monte-carlo'
tier: supporting
kind: derivation
status: live
domain: [QCD]
exactness: machine
findings: [F94]
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

# CL087 — Confinement from 3+1D lattice-gauge Monte-Carlo (P1 Option A), tested against Option C (F86)

## Statement

Confinement from 3+1D lattice-gauge Monte-Carlo (P1 Option A), tested against Option C (F86)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F94-lattice-gauge-mc-confinement-vs-F86.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F94-lattice-gauge-mc-confinement-vs-F86.md` | The finding, in full | machine |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — engine 6/6 PASS (correctness), comparison 4/4 PASS; FA2/FA3 machine-ε, FA1 machine-ε, FA4/FA5 statistical, multilevel 84× variance reduction. Production σ is user-run.

**Date:** 2026-06-04 - 14:33

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F94-lattice-gauge-mc-confinement-vs-F86.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
