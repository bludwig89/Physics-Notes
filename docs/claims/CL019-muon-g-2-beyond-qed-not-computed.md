---
id: CL019
title: 'Muon g-2 beyond the QED piece is not computed and not claimed'
slug: 'muon-g-2-beyond-qed-not-computed'
tier: headline
kind: non_claim
status: not_claimed
domain: [QFT, SM]
exactness: machine
findings: [F261, F249]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: none
first_issued: '2026-08-02'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL019 — Muon g-2 beyond the QED piece is not computed and not claimed

## Statement

The QED piece is computed through two loops: $A_2(\mu)=0.765857$ against the known $0.765857410$. **Hadronic vacuum polarisation, hadronic light-by-light and electroweak contributions are not computed and not claimed.**

## What it extends

Recorded so that **absence is not read as a prediction**. This is a scope boundary, not a result: the project does not assert it, and `status: not_claimed` is the assertion that it does not assert it. The muon anomaly is the Standard Model's most-watched precision tension; a model silent on the hadronic pieces has said nothing about that tension, and this card says so explicitly.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F261-twoloop-qed-ae-amu.md` | Two-loop QED $a_e$ and $a_\mu$; $A_2(\mu)=0.765857$ | machine |
| `findings/F249-qed-comparison-battery.md` | The QED comparison battery this sits in | machine |

## Falsifier

None on the omitted pieces. The **computed** QED piece is falsifiable and is a separate, live supporting claim carried by the F261 backfill card.

## Status & history

`not_claimed`. Recorded in the summary's Scope section from revision 2 (2026-08-02).

## Sources

- `findings/F261-twoloop-qed-ae-amu.md`
- `papers/Claims-and-Falsifiers-Summary.md` — Scope
