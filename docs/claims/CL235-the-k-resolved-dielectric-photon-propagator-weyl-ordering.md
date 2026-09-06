---
id: CL235
title: 'The k-resolved dielectric photon propagator: Weyl ordering and the second-order half-step'
slug: 'the-k-resolved-dielectric-photon-propagator-weyl-ordering'
tier: supporting
kind: derivation
status: live
domain: [QFT]
exactness: unset
findings: [F271]
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

# CL235 — The k-resolved dielectric photon propagator: Weyl ordering and the second-order half-step

## Statement

The k-resolved dielectric photon propagator: Weyl ordering and the second-order half-step

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F271-k-resolved-dielectric-photon-propagator.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F271-k-resolved-dielectric-photon-propagator.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, quoted from the finding's own status line — which the seed missed because F271 writes it in
italics (`*Status: ...*`) rather than `**Status:**`:

> *Status: **established** for the operator's exactness, convergence and norm behaviour; the deflection **coefficient** against GR is explicitly not claimed.*

**Corrected from `withdrawn` on 2026-08-19** (finding-coverage rollout section 4 bucket 2). The seed read
`withdrawn` off the word *Supersedes* in F271's header, but the direction is the other way: F271 is the
**superseder** in ledger entry `S10-F271-eikonal-dielectric-photon`, which retires F270 §4's eikonal
`dielectric_mix_half` for the photon channel. F271 appears in no `superseded:` list. Evidence is now
carried by a record: `P3.4-P3.6-total-energy-and-gravity-loop` (gate tier), legs T8b–T8d, T9, T10.
Still `review_state: unreviewed-seed`: the statement is the finding's title, and the finding's own
explicit non-claim — the deflection coefficient against GR — is not yet written into this card.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F271-k-resolved-dielectric-photon-propagator.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
