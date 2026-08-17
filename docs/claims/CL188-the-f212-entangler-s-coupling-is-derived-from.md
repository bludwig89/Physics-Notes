---
id: CL188
title: 'The F212 entangler''s coupling is **derived** from the `ca_dirac` hopping (antiferromagnetic super-exchange $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, $t$ measured from o'
slug: 'the-f212-entangler-s-coupling-is-derived-from'
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F214]
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

# CL188 — The F212 entangler's coupling is **derived** from the `ca_dirac` hopping (antiferromagnetic super-exchange $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, $t$ measured from o

## Statement

The F212 entangler's coupling is **derived** from the `ca_dirac` hopping (antiferromagnetic super-exchange $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, $t$ measured from one tick of the exact-QCA stepper, $U=2\arcsin m$), and multi-cell entanglement is wired **live** into the `casim` engine as a genuine $2^n$ register channel that generates entropy $0\to\ln 2$ at the derived rate — checkpoint/resume bit-identical

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F214-superexchange-and-live-entanglement-channel.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F214-superexchange-and-live-entanglement-channel.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 6/6 checks PASS. J derivation **exact-algebraic** (closed-form $=$ exact two-site Hubbard diagonalisation to $<10^{-12}$); live-channel entropy reaches $\ln 2$ to the discrete-tick error ($3.3\times10^{-7}$ at integer tick 7; continuous peak $\ln 2$ to $3\times10^{-7}$); checkpoint/resume bit-identical.

**Date:** 2026-07-01 - 16:10

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F214-superexchange-and-live-entanglement-channel.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
