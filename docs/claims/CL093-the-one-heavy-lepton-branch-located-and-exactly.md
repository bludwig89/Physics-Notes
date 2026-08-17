---
id: CL093
title: 'The one-heavy lepton branch located and exactly fitted: the sea cliff pins $m_\tau$ at saturation, the closed-form coupling family carries the exact spectrum, F'
slug: 'the-one-heavy-lepton-branch-located-and-exactly'
tier: supporting
kind: derivation
status: open
domain: [QFT]
exactness: exact
findings: [F101b]
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

# CL093 — The one-heavy lepton branch located and exactly fitted: the sea cliff pins $m_\tau$ at saturation, the closed-form coupling family carries the exact spectrum, F

## Statement

The one-heavy lepton branch located and exactly fitted: the sea cliff pins $m_\tau$ at saturation, the closed-form coupling family carries the exact spectrum, F95's angle requirement and the spectrum fit select the same $W\approx1.5$ — and two sharp negatives (metastability; static RPA has the wrong sign)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F101b-one-heavy-branch-fit-W.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F101b-one-heavy-branch-fit-W.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (located + fitted + cross-validated, with two honest negatives) — 6/6 checks PASS. **New exact structure:** (A0) the BCC sea has a **cliff** at saturation — $f'(m)\to-\infty$ as $m\to1$ (the arccos edge of the F46 dispersion) — so an interior heavy flavor is *always* a saddle: the heavy generation is **forced onto the wall exactly**, $y_\tau=1$. The τ mass *is* the saturation scale — the sharpest scale statement the chain has produced. (A1) With the τ wall-pinned, the inverse problem is **linear**: the two light-flavor stationarity equations give $(\kappa_E,\mu)(W)$ in closed form — the exact measured spectrum $(1,\sqrt{m_\mu/m_\tau},\sqrt{m_e/m_\tau})$ is a genuine KKT local vacuum of the $W$-completed gap theory along a one-parameter family, $W\in[0.10,21.6]$, with $W>0$ **emergent** and $r=\kappa_E/\kappa_0\approx0.986$ (a near-pure per-flavor contact). (B) **Two independent routes meet:** F95's Landau localization $C=0.636|B|$ selects $W^*=6C/e^6=1.46$ — *inside* the admissible window, with all KKT conditions holding at exactly that point. **The honest negatives:** (A2) along the minimal 3-coupling family the lepton point is **metastable** — squeezed between the all-saturated $(1,1,1)$ vacuum (small $W$) and the empty $(0,0,0)$ vacuum (large $W$), closest gap $2.5\times10^{-2}$ at $W\approx0.69$; (C) the static uniform-mode RPA gives a **negative** sextic (an anti-brake) and loses positivity near the wall — $W$ is *not* derivable at static one-loop. See §6.

**Date:** 2026-06-05 - 14:20

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F101b-one-heavy-branch-fit-W.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
