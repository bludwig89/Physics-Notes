---
id: CL109
title: 'P2: the dynamical baryon — a real-time, non-dispersing, mass-measured three-quark bound state (proton, then neutron)'
slug: 'p2-the-dynamical-baryon-a-real-time-non'
tier: supporting
kind: prediction
status: live
domain: [QCD]
exactness: exact
findings: [F122]
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

# CL109 — P2: the dynamical baryon — a real-time, non-dispersing, mass-measured three-quark bound state (proton, then neutron)

## Statement

P2: the dynamical baryon — a real-time, non-dispersing, mass-measured three-quark bound state (proton, then neutron)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F122-p2-dynamical-baryon-three-body.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F122-p2-dynamical-baryon-three-body.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 11/11 checks PASS. S0/S1/S4 machine-precision/exact (analytic harmonic ground state; two solve routes; S₃-symmetric pair radii); S2/S3/S5/S6 quantitative (variational convergence, discrete spectrum, confinement dominance, Casimir-scaling invariance); S7/S8 Tier-B (m_p/√σ ratio P6-gated; n–p splitting). Independently re-verified: the ⟨r⟩/⟨1/r⟩ kernels vs direct radial quadrature (6 digits) and the full 6-D pair matrix element vs Monte-Carlo.

**Date:** 2026-06-09 - 16:54

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

**2026-08-05 — one of the quoted sub-results is now excluded, and this card is deliberately NOT
narrowed.** F297 computes primordial nucleosynthesis on the model's own expansion law and, with it,
bounds $m_n-m_p$ to $1.293\pm0.0056$ MeV. F122's S8 n–p splitting — the "Tier-B" clause in the
status line quoted above — gives $+1.51$ MeV, excluded at $36.6\sigma$ in $Y_p$ and by a factor 2.7
in the free-neutron lifetime. See `docs/claims/CL259-bbn-bounds-np-splitting.md`.

This card's `Statement` is the finding's *title* and asserts a bound state, not a splitting value,
so the claim as written does not overreach and `status` stays `live`. The note exists so that the
next reader — or the promotion of this card out of `unreviewed-seed` — starts from the fact that
S8's number is dead while S0–S7 are not. Nothing in `findings/F122-p2-dynamical-baryon-three-body.md` was edited.

## Sources

- `findings/F122-p2-dynamical-baryon-three-body.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
