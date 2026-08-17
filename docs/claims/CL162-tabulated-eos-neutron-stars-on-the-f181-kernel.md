---
id: CL162
title: 'Tabulated-EoS neutron stars on the F181 kernel: SLy gives M_max=2.08 M⊙ and R(1.4)=11.1 km, consistent with PSR J0740 and NICER (scenario S1)'
slug: 'tabulated-eos-neutron-stars-on-the-f181-kernel'
tier: supporting
kind: derivation
status: live
domain: [GR]
exactness: exact
findings: [F184]
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

# CL162 — Tabulated-EoS neutron stars on the F181 kernel: SLy gives M_max=2.08 M⊙ and R(1.4)=11.1 km, consistent with PSR J0740 and NICER (scenario S1)

## Statement

Tabulated-EoS neutron stars on the F181 kernel: SLy gives M_max=2.08 M⊙ and R(1.4)=11.1 km, consistent with PSR J0740 and NICER (scenario S1)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F184-tabulated-eos-neutron-stars.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F184-tabulated-eos-neutron-stars.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 3/3 checks PASS. The machinery (piecewise-polytrope EoS + two-function TOV) is exact; absolute M–R values inherit the published EoS digits and a single-crust simplification (R good to ~5%).

**Date:** 2026-06-30 - 04:00

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F184-tabulated-eos-neutron-stars.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
