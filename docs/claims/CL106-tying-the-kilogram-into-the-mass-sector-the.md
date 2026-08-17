---
id: CL106
title: 'Tying the kilogram into the mass sector: the overall scale $N$ factorises cleanly out of the derived spectrum, but all three closure routes converge on the same'
slug: 'tying-the-kilogram-into-the-mass-sector-the'
tier: supporting
kind: no_go
status: open
domain: [GR]
exactness: machine
findings: [F119]
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

# CL106 — Tying the kilogram into the mass sector: the overall scale $N$ factorises cleanly out of the derived spectrum, but all three closure routes converge on the same

## Statement

Tying the kilogram into the mass sector: the overall scale $N$ factorises cleanly out of the derived spectrum, but all three closure routes converge on the same verdict — $N$ is the fermion-mass hierarchy, the 3D gap mechanism cannot generate it from $O(1)$ inputs (a sharp no-go), $W$ is $O(1)$-localised but its value still fitted, and gravity pins the cell $a$ rather than the mass scale

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F119-kg-scale-three-routes.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F119-kg-scale-three-routes.md` | The finding, in full | machine |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (one clean factorisation + one sharp no-go + one $O(1)$ localisation + one consistency cross-check) — 8/8 checks PASS (`test_F119_kg_scale_three_routes.py`, <1 s). Pure numpy/math (no scipy, per CLAUDE.md). The headline: **the kilogram is already tied in *as a unit*** — once $a$ is locked (F107), $\hbar$ carries the kg and $m_\text{phys}=\hbar\arcsin(m_\text{lat})/(\tau c^2)$ returns kg with no free parameter. What is *not* derived is the single dimensionless overall scale $N\equiv m_\text{lat}(\tau)=5.54\times10^{-19}$ (since the condensate pins $m^\text{cond}_\tau\equiv1$). The condensate gives the *shape* (ratios, Koide, angle) to $10^{-12}$; $N$ is a clean multiplicative scale on top. **The three attempted closures all fail in the same instructive way:** $N$ *is* the fermion-mass hierarchy.

**Date:** 2026-06-09 - 15:40

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F119-kg-scale-three-routes.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
