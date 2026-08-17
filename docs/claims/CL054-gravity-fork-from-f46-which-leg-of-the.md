---
id: CL054
title: 'Gravity fork from F46: which leg of the spherical triangle carries gravitational redshift'
slug: 'gravity-fork-from-f46-which-leg-of-the'
tier: supporting
kind: derivation
status: open
domain: [GR]
exactness: exact
findings: [F50]
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

# CL054 — Gravity fork from F46: which leg of the spherical triangle carries gravitational redshift

## Statement

Gravity fork from F46: which leg of the spherical triangle carries gravitational redshift

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F50-gravity-fork-f46-tetrad-dirac.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F50-gravity-fork-f46-tetrad-dirac.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 8/8 tests PASS (G1 slope-4 lattice correction; G2–G4, G6 algebraic/machine-ε; G5 exactly norm-conserving prototype stepper; G7 boundedness + slope; G8 bit-for-bit QCA stepper phase match)

**Date:** 2026-05-28 - 23:55 (updated 2026-05-29 - 00:30 — kinetic leg promoted to the bounded exact-QCA form)

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F50-gravity-fork-f46-tetrad-dirac.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
