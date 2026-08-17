---
id: CL078
title: 'Fixing the lattice spacing $a$ from a measured fermion mass: the F46/F12 map gives a relation, not a value; the heaviest fermion sets the ceiling'
slug: 'fixing-the-lattice-spacing-from-a-measured-fermion'
tier: supporting
kind: derivation
status: live
domain: [SM]
exactness: exact
findings: [F83]
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

# CL078 — Fixing the lattice spacing $a$ from a measured fermion mass: the F46/F12 map gives a relation, not a value; the heaviest fermion sets the ceiling

## Statement

Fixing the lattice spacing $a$ from a measured fermion mass: the F46/F12 map gives a relation, not a value; the heaviest fermion sets the ceiling

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F83-fix-lattice-spacing-from-fermion-mass.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F83-fix-lattice-spacing-from-fermion-mass.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (negative/conditional result) — 5/5 checks PASS, round-trip at machine precision ($2.5\times10^{-16}$). The algebra is exact; the headline is that a single measured mass **cannot** fix $a$, but it imposes an exact ceiling and, once $a$ is pinned elsewhere, an exact $m_\text{lat}$.

**Date:** 2026-06-02 - 20:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F83-fix-lattice-spacing-from-fermion-mass.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
