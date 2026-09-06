---
id: CL120
title: 'Real-time wave-packet dynamics survive block-spin: a moving, spreading massive Dirac packet coarse-grains faithfully, and mass is the matter sector''s one releva'
slug: 'real-time-wave-packet-dynamics-survive-block-spin'
tier: supporting
kind: derivation
status: live
domain: [SM]
exactness: machine
findings: [F135]
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

# CL120 — Real-time wave-packet dynamics survive block-spin: a moving, spreading massive Dirac packet coarse-grains faithfully, and mass is the matter sector's one releva

## Statement

Real-time wave-packet dynamics survive block-spin: a moving, spreading massive Dirac packet coarse-grains faithfully, and mass is the matter sector's one relevant operator (rest-gap eigenvalue $b$)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F135-blockspin-wavepacket-realtime.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F135-blockspin-wavepacket-realtime.md` | The finding, in full | machine |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. RT1 faithfulness and RT4 mass-eigenvalue are **machine-precision**; RT2/RT3 are quantitative (velocity/width agree fine-vs-coarse); RT5 unitarity at the FFT floor. Closes the dynamical check left open by [[F132-blockspin-dynamical-bound-states]] §6 (RG commutes with binding was shown only for static eigenstates). Phase-2 item "real-time wave-packet dynamics under $R_b$" of `docs/roadmaps/completed/roadmap-scale-to-real-space.md`.

**Date:** 2026-06-11

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F135-blockspin-wavepacket-realtime.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
