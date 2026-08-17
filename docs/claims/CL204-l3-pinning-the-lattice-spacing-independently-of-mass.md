---
id: CL204
title: 'L3: pinning the lattice spacing $a$ independently of mass — the light-deflection route is **degenerate** (a scale-invariance theorem), and the mass-independent '
slug: 'l3-pinning-the-lattice-spacing-independently-of-mass'
tier: supporting
kind: derivation
status: live
domain: [GR]
exactness: unset
findings: [F232]
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

# CL204 — L3: pinning the lattice spacing $a$ independently of mass — the light-deflection route is **degenerate** (a scale-invariance theorem), and the mass-independent 

## Statement

L3: pinning the lattice spacing $a$ independently of mass — the light-deflection route is **degenerate** (a scale-invariance theorem), and the mass-independent pin is the F79 $G$-match, not lensing

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F232-lattice-spacing-degeneracy-scale-invariance.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F232-lattice-spacing-degeneracy-scale-invariance.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (negative / degeneracy result) — 5/5 checks PASS. Executes the F83 open follow-up #1 (open line 141 of `docs/roadmaps/next-steps.md`): combine the F46 rest-leg relation with the absolute light-deflection coefficient to pin $a$ without a mass. The attempt **closes negative**: the deflection coefficient is exactly $-4$, dimensionless and $a$-independent (F107 L4a), so it supplies **zero** constraint on $a$ — the F83 $(a,m_\text{lat})$ ray is unbroken. The general reason is a **scale-invariance theorem**: no dimensionless, mass-independent lattice observable can fix a length. The third input that *does* break the degeneracy is the **dimensionful** gravitational coupling $G$ (equivalently $\ell_P$), which pins $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ via F79 — a mass-independent pin, but the $G$-match, not the lensing route the follow-up proposed.

**Date:** 2026-07-02 - 16:20

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F232-lattice-spacing-degeneracy-scale-invariance.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
