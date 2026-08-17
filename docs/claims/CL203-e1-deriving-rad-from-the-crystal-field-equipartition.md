---
id: CL203
title: 'E1: deriving $\delta^*=\tfrac29$ rad from the crystal-field / equipartition geometry closes **negative** — geometry fixes only the phase-coordinate **endpoints*'
slug: 'e1-deriving-rad-from-the-crystal-field-equipartition'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F230]
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

# CL203 — E1: deriving $\delta^*=\tfrac29$ rad from the crystal-field / equipartition geometry closes **negative** — geometry fixes only the phase-coordinate **endpoints*

## Statement

E1: deriving $\delta^*=\tfrac29$ rad from the crystal-field / equipartition geometry closes **negative** — geometry fixes only the phase-coordinate **endpoints** (democratic $0$, massless-Koide $3\delta=\pi/4$, equipartition $45°$); the **interior** stopping point is dynamics ($\lambda_6$), and a radian cannot equal a ratio without a scale

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F230-lepton-angle-geometric-nogo.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F230-lepton-angle-geometric-nogo.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (negative / sharpened no-go) — 6/6 checks PASS. Attempts the E1 target — derive the charged-lepton spectrum angle $\delta^*=\tfrac29$ rad ($3\delta^*=Q=\tfrac23$) from the F75/F76 $T_{1u}$ crystal-field geometry + F78/F80 Cooper-pair equipartition ($45°$) — along the **geometric** route (distinct from F179's induced-coupling route and F199's BPS route). It **closes negative**, and sharpens the reason: the geometry produces only the **endpoints** of the phase coordinate $3\delta$ (democratic $3\delta=0$; massless-Koide $3\delta=\pi/4$, *exact*; equipartition $\phi=45°$), while the physical **interior** value $3\delta^*=\tfrac23$ rad is fixed by the brake ratio $B/C$ (cubic crystal-field vs sextic self-coupling), a dynamical number. The **dimensional no-go**: $3\delta^*$ is a radian, $Q$ is a pure ratio; crystal-field geometry yields only trig ratios and rational irrep multiplicities and cannot force radian $=$ ratio without a dynamical scale. This is consistent with, and subsumed by, **F199**'s three-way structural no-go; $\delta^*=\tfrac29$ rad remains a Koide-confidence **target**, not a derivation.

**Date:** 2026-07-02 - 16:35

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F230-lepton-angle-geometric-nogo.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
