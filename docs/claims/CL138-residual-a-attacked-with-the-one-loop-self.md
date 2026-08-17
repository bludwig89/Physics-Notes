---
id: CL138
title: 'Residual A attacked with the one-loop self-energy machinery: the tadpole sector is **exactly empty** (the Wilson 28.81 is structurally absent), the lattice−cont'
slug: 'residual-a-attacked-with-the-one-loop-self'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: exact
findings: [F155]
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

# CL138 — Residual A attacked with the one-loop self-energy machinery: the tadpole sector is **exactly empty** (the Wilson 28.81 is structurally absent), the lattice−cont

## Statement

Residual A attacked with the one-loop self-energy machinery: the tadpole sector is **exactly empty** (the Wilson 28.81 is structurally absent), the lattice−continuum **subtraction** machinery is built and convergent, and the matching scale is **bracketed** $q_\ast a\in[1/\sqrt3,\,\sim0.97]$ (implied $0.733$ inside, $\Lambda$-ratio $O(1)$ — not Wilson) — with the Residual-B freeze value $\approx0.39$ now **bracketed anchor-free** to a narrow window $[0.31,0.38]$ by the L-stable χSB onset

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F155-qstar-self-energy-and-freeze-bracket.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F155-qstar-self-energy-and-freeze-bracket.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (Residual A **sharpened to a convergent bracket**, not pinned to the digit; the B freeze **bracketed anchor-free**) — 5/5 checks PASS. A0 exact (tadpole empty, gluon luminal — machine precision); A3 convergent (the $d_1$ subtraction machinery, n-stable); A5 bracket (subtracted LM moment converges to the band top, $q_\ast$ bracketed, $\Lambda$-ratio $O(1)$); Bf anchor-free (L-stable onset window); C falsification-sharp. **Honest headline:** the moment/abelian routes pin $q_\ast$ to the *upper* edge of F151's band (the near-perfect-action signature); the remaining pull-down to the implied $0.733$ is the **gluonic 3-gluon + ghost finite part**, which is the one production computation still open (or, gauge-fixing-free, the high-resolution static-potential measurement — Route A-NP, whose machinery is built here).

**Date:** 2026-06-13 - 11:30

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F155-qstar-self-energy-and-freeze-bracket.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
