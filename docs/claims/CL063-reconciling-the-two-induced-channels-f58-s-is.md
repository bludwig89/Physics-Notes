---
id: CL063
title: 'Reconciling the two induced-$G$ channels: F58''s $c_\text{lat}^2$ is tree-level, F59''s $1/c_\text{lat}$ is loop-induced, gap $=c_\text{lat}^3$'
slug: 'reconciling-the-two-induced-channels-f58-s-is'
tier: supporting
kind: derivation
status: live
domain: [GR]
exactness: machine
findings: [F60]
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

# CL063 — Reconciling the two induced-$G$ channels: F58's $c_\text{lat}^2$ is tree-level, F59's $1/c_\text{lat}$ is loop-induced, gap $=c_\text{lat}^3$

## Statement

Reconciling the two induced-$G$ channels: F58's $c_\text{lat}^2$ is tree-level, F59's $1/c_\text{lat}$ is loop-induced, gap $=c_\text{lat}^3$

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F60-induced-G-channel-reconciliation.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F60-induced-G-channel-reconciliation.md` | The finding, in full | machine |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 4/4 checks, three at machine precision (exponents $2.0000$, $-1.0000$, $-3.0000$; lock spread $1.1\times10^{-16}$). Resolves the F58↔F59 channel fork flagged in F59. The emergent-gravity ontology the project already uses (F52/F55/F57) selects the loop channel, so $1/G\propto\sqrt d$ and the F59 selection power $d^{1/4}$ stands.

**Date:** 2026-05-30 - 15:25

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F60-induced-G-channel-reconciliation.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
