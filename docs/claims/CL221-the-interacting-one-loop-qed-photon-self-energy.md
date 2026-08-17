---
id: CL221
title: 'The interacting one-loop QED photon self-energy Π^μν(q) and the running coupling α(q²)'
slug: 'the-interacting-one-loop-qed-photon-self-energy'
tier: supporting
kind: derivation
status: open
domain: [QFT]
exactness: exact
findings: [F251]
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

# CL221 — The interacting one-loop QED photon self-energy Π^μν(q) and the running coupling α(q²)

## Statement

The interacting one-loop QED photon self-energy Π^μν(q) and the running coupling α(q²)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F251-qed-vacuum-polarization-running-alpha.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F251-qed-vacuum-polarization-running-alpha.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Ward transversality $q_\mu\Pi^{\mu\nu}=0$ and the QED beta coefficient $b_0^{\text{QED}}=\tfrac43$ are **algebraically exact** (sympy, literal 0 / exact rational); lattice $b_0$ = continuum $b_0$ after subtraction (q-flat); leptonic $\Delta\alpha(M_Z)$ matches PDG to $0.24\%$.

**Date:** 2026-07-16 - 11:20

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F251-qed-vacuum-polarization-running-alpha.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
