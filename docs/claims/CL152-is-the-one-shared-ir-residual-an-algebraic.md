---
id: CL152
title: 'Is the one shared IR residual an *algebraic connection* or a *computed number*? A wide review: the \"one number\" is one IR fixed-point coupling dressed by exact '
slug: 'is-the-one-shared-ir-residual-an-algebraic'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: exact
findings: [F172]
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

# CL152 — Is the one shared IR residual an *algebraic connection* or a *computed number*? A wide review: the "one number" is one IR fixed-point coupling dressed by exact 

## Statement

Is the one shared IR residual an *algebraic connection* or a *computed number*? A wide review: the "one number" is one IR fixed-point coupling dressed by exact lattice geometry, and the algebraic hypothesis splits cleanly — **well-motivated for the SHAPE residual** ($3\delta^*=Q$, with an exact $\pi/4$ anchor and a self-consistency structure), **weak for the SCALE/scheme residual** (which matches computed nonperturbative QCD quantities)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F172-residual-algebraic-or-computed.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F172-residual-algebraic-or-computed.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Analysis / reframing (no new physics input; a structural verdict on an open problem) — 4/4 checks PASS. **What this establishes:** (i) the recurring "one nonperturbative residual" is **not one number** — its members are manifestly distinct values that are different *functions* of one IR fixed-point coupling $\alpha_\text{eff}^*$ plus **exact** lattice geometry; (ii) the algebraic-connection question therefore separates into a **SHAPE** residual (the lepton-condensate angle $3\delta^*$ / $\lambda_6$) and a **SCALE/scheme** residual ($\Lambda$ ratio, $q_\ast$, $d_1$, $\sqrt\sigma/f_\pi$), with **opposite** prospects; (iii) the shape residual has a genuine path to an exact algebraic value — an **exact $\pi/4$ anchor** at $m_e=0$ (F96), a **self-consistency** structure (the F92 method that already derived $45°$, $Q=2/3$, $\sqrt2$ exactly), and the target $3\delta^*=Q=\tfrac23$ rad (F150/F164); (iv) the scale/scheme residual looks **computed/transcendental** — it matches real-QCD quantities ($\hat\alpha(0)/\pi=0.97$, Deur–Brodsky–Roberts) that are measured, not algebraic, and its residual digit lives in the action-specific finite vertex constant $d_1$ that the F155 moment-insensitivity theorem makes non-algebraic. **Recommendation: stop treating them as "one number"; attack the shape angle as a self-consistency fixed point and the scheme constant as a separate computed integral.**

**Date:** 2026-06-29 - 21:40

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F172-residual-algebraic-or-computed.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
