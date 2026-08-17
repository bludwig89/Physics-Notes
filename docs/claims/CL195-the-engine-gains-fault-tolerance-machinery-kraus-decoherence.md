---
id: CL195
title: 'The engine gains **fault-tolerance machinery**: Kraus decoherence channels + stabilizer codes built on the native gate set. The 3-qubit code''s corrected fidelit'
slug: 'the-engine-gains-fault-tolerance-machinery-kraus-decoherence'
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F221]
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

# CL195 — The engine gains **fault-tolerance machinery**: Kraus decoherence channels + stabilizer codes built on the native gate set. The 3-qubit code's corrected fidelit

## Statement

The engine gains **fault-tolerance machinery**: Kraus decoherence channels + stabilizer codes built on the native gate set. The 3-qubit code's corrected fidelity matches the exact closed form $F=(1-3p^2+2p^3)+(3p^2-2p^3)(2ab)^2$ to machine precision with logical infidelity suppressed to $O(p^2)$ (vs uncorrected $O(p)$); the 9-qubit Shor code corrects an **arbitrary** single-qubit error (all $27=\{X,Y,Z\}\times9$) to $<10^{-12}$; and a live `error_correction` channel holds a logical qubit at $F=0.995$ over 8 noise rounds while the uncorrected control decays to $0.27$

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F221-noise-error-correction.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F221-noise-error-correction.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Channels are exact CPTP ($\sum E^\dagger E=I$ to $10^{-16}$); 3-qubit code fidelity **exact-algebraic** ($4.4\times10^{-16}$ vs closed form); Shor arbitrary single-error correction to $4.4\times10^{-16}$; pseudo-threshold and live decay/hold demonstrated; checkpoint bit-identical.

**Date:** 2026-07-01 - 20:15

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F221-noise-error-correction.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
