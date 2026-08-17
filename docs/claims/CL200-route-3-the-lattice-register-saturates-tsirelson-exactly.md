---
id: CL200
title: 'Route 3: the lattice register saturates Tsirelson $S_\text{CHSH}=2\sqrt2$ **exactly**, so it is **Bell-indistinguishable** from QM; the only discreteness entry '
slug: 'route-3-the-lattice-register-saturates-tsirelson-exactly'
tier: supporting
kind: derivation
status: withdrawn
domain: [QM]
exactness: exact
findings: [F226]
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

# CL200 — Route 3: the lattice register saturates Tsirelson $S_\text{CHSH}=2\sqrt2$ **exactly**, so it is **Bell-indistinguishable** from QM; the only discreteness entry 

## Statement

Route 3: the lattice register saturates Tsirelson $S_\text{CHSH}=2\sqrt2$ **exactly**, so it is **Bell-indistinguishable** from QM; the only discreteness entry (analyzer-angle granularity) is quadratic and Planck-suppressed to $\sim10^{-54}$

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F226-bell-tsirelson-indistinguishable.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F226-bell-tsirelson-indistinguishable.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`withdrawn`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Tsirelson saturation is **machine-precision exact** ($\lvert S\rvert=2\sqrt2$ to $1.8\times10^{-15}$, convention-free Horodecki-optimal); the discreteness-correction curvature $-3\sqrt2$ and its quadratic scaling are **exact-algebraic** (verified to $<10^{-2}$); the Planck-suppression magnitude and the Bell-data confrontation are quantitative.

**Date:** 2026-07-02 - 14:05

**A supersession/withdrawal banner appears in this finding's header**, which is why the card reads `withdrawn`. The specific ledger record has not been attached — do that before relying on this status.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F226-bell-tsirelson-indistinguishable.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
