---
id: CL106
title: 'Tying the kilogram into the mass sector: the overall scale $N$ factorises cleanly out of the derived spectrum, but all three closure routes converge on the same'
slug: 'tying-the-kilogram-into-the-mass-sector-the'
tier: supporting
kind: no_go
status: open
domain: [GR]
exactness: machine
findings: [F119, F233, F351]
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
| `findings/F233-mass-scale-N-transmutation-supersedes-F119.md` | **Partially supersedes this card's Route 1.** F119's "no marginal/running channel exists" no-go is not airtight: QCD asymptotic freedom is such a channel, and it reproduces $N$ to a factor $1.9$ with zero free parameters, contingent on the shared scheme constant $d_1$. | machine |
| `findings/F351-electroweak-scale-v-not-second-pin-collapses-to-d1.md` | Extends this card's question to the electroweak scale $v$ (ledger parameter #17): checks the two known generation mechanisms against $v$ specifically (Sakharov/loop-induction: negligible, F143; NJL/dynamical-transmutation: not absent, contra a literal reading of F119, per F233) and flags — honestly, as unproven — that $v$'s residual is plausibly the SAME $d_1$ residual this card's $N$ reduces to. | machine |

**This card's evidence is no longer only the prose of its own finding** — F233 and F351 are independent test records with their own result artifacts (`test-results/F233_mass_scale_N_transmutation.json`, `test-results/F351_v_second_pin_scope.json`). Full promotion to `review_state: authored` still requires a dedicated review pass confirming the `domain`/`kind`/`exactness` classification by hand; not done here.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (one clean factorisation + one sharp no-go + one $O(1)$ localisation + one consistency cross-check) — 8/8 checks PASS (`test_F119_kg_scale_three_routes.py`, <1 s). Pure numpy/math (no scipy, per CLAUDE.md). The headline: **the kilogram is already tied in *as a unit*** — once $a$ is locked (F107), $\hbar$ carries the kg and $m_\text{phys}=\hbar\arcsin(m_\text{lat})/(\tau c^2)$ returns kg with no free parameter. What is *not* derived is the single dimensionless overall scale $N\equiv m_\text{lat}(\tau)=5.54\times10^{-19}$ (since the condensate pins $m^\text{cond}_\tau\equiv1$). The condensate gives the *shape* (ratios, Koide, angle) to $10^{-12}$; $N$ is a clean multiplicative scale on top. **The three attempted closures all fail in the same instructive way:** $N$ *is* the fermion-mass hierarchy.

**Date:** 2026-06-09 - 15:40

**Update, 2026-09-02 (F233, F351).** The "3D gap mechanism cannot generate $N$" no-go (Route 1)
is qualified, not overturned: F233 (2026-07-02) found that QCD asymptotic freedom — a channel
F119 did not consider, distinct from the 3D NJL gap equation it excluded — reduces $N$'s gap to a
factor $1.9$ across 19 decades with no free parameter, with the entire residual collapsing to one
shared one-loop matching constant $d_1$ (also owning the lepton brake $\lambda_6$, F150, and the
QCD scale-setting residuals Q1/Q2). F351 (2026-09-02) checks the SAME two mechanisms against the
electroweak scale $v$ (ledger parameter #17, a sibling anchor): Sakharov/loop-induction is
checked directly and found negligible (F143, $\le0.36\%$ of $v^2$); dynamical transmutation is
not absent (correcting a literal reading of this card's own F119 citation); and $v$'s residual is
plausibly — not yet provably — the same $d_1$ cluster $N$ and $\lambda_6$ collapse to. $N$ (and
now, plausibly, $v$) remain FIT — this update does not close either — but the mechanism-space is
now documented rather than merely absent.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F119-kg-scale-three-routes.md`
- `findings/F233-mass-scale-N-transmutation-supersedes-F119.md` — partial supersession of Route 1
- `findings/F351-electroweak-scale-v-not-second-pin-collapses-to-d1.md` — extension to $v$
- `docs/claims/README.md` — the `unreviewed-seed` contract
