---
id: CL085
title: 'E2E certification of the non-Abelian W/Z/gluon couplings on the σ-bilinear + the full fermion/radiation back-reaction loop; chiral-Proca birefringence is mass-s'
slug: 'e2e-certification-of-the-non-abelian-w-z'
tier: supporting
kind: derivation
status: live
domain: [QCD]
exactness: unset
findings: [F90]
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

# CL085 — E2E certification of the non-Abelian W/Z/gluon couplings on the σ-bilinear + the full fermion/radiation back-reaction loop; chiral-Proca birefringence is mass-s

## Statement

E2E certification of the non-Abelian W/Z/gluon couplings on the σ-bilinear + the full fermion/radiation back-reaction loop; chiral-Proca birefringence is mass-suppressed

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F90-e2e-nonabelian-bilinear-backreaction.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F90-e2e-nonabelian-bilinear-backreaction.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 14/14 PASS (new suite) + the repaired Phase-7 suite 5/5 PASS. Primarily an **integration / certification** finding (the F85-style kind): it certifies that the sector design decision #5 retains on the σ-bilinear — W, Z, gluon — works *end-to-end* (fermion current → source kick → causal propagation → back-action on the fermion), with the energy bookkeeping closed. One small new algebraic result: the chiral-Proca birefringence closed form and its mass suppression.

**Date:** 2026-06-04 - 01:59

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F90-e2e-nonabelian-bilinear-backreaction.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
