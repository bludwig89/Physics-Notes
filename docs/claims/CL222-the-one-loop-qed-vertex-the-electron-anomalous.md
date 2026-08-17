---
id: CL222
title: 'The one-loop QED vertex Λ^μ: the electron anomalous moment a_e = α/2π and the hydrogen Lamb shift'
slug: 'the-one-loop-qed-vertex-the-electron-anomalous'
tier: supporting
kind: derivation
status: live
domain: [QFT]
exactness: exact
findings: [F252]
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

# CL222 — The one-loop QED vertex Λ^μ: the electron anomalous moment a_e = α/2π and the hydrogen Lamb shift

## Statement

The one-loop QED vertex Λ^μ: the electron anomalous moment a_e = α/2π and the hydrogen Lamb shift

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F252-qed-vertex-ae-lamb-shift.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F252-qed-vertex-ae-lamb-shift.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 4/4 checks PASS. The Ward–Takahashi identity and $a_e=F_2(0)=\alpha/2\pi$ (Schwinger term) are **algebraically exact** (sympy; the Feynman-parameter integral evaluates to exactly 1); the Uehling coefficient $-\tfrac{4}{15}$ is derived from the F251 bubble; the $2s_{1/2}$–$2p_{1/2}$ Lamb shift is lifted to $1052.2$ MHz $=99.5\%$ of the measured $1057.845$ MHz.

**Date:** 2026-07-16 - 11:35

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F252-qed-vertex-ae-lamb-shift.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
