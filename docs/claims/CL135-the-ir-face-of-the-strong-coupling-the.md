---
id: CL135
title: 'The **IR face** of the strong coupling: the $\alpha_\text{eff}^\ast\approx0.39$ that F151-S5 split off is the gap-saturated frozen coupling — its scale is the d'
slug: 'the-ir-face-of-the-strong-coupling-the'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: exact
findings: [F152]
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

# CL135 — The **IR face** of the strong coupling: the $\alpha_\text{eff}^\ast\approx0.39$ that F151-S5 split off is the gap-saturated frozen coupling — its scale is the d

## Statement

The **IR face** of the strong coupling: the $\alpha_\text{eff}^\ast\approx0.39$ that F151-S5 split off is the gap-saturated frozen coupling — its scale is the dual-Meissner gluon mass, it sits on QCD's decoupling/saturating branch ($\hat\alpha(0)/\pi=0.97$, $m_g\approx0.5$ GeV), and it is the normalization F150's $\lambda_6$ inherits

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F152-ir-coupling-the-irface.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F152-ir-coupling-the-irface.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (an interpretation + a scale derivation + a branch identification; the value $\alpha_\text{eff}^\ast$ is *imported* from F151-S5/F145, not newly computed) — 5/5 checks PASS. **Setting:** the concurrent F151 (`scheme-constant-determined`, 13:55) determined the **UV face** of the shared strong-sector constant — the rule's coupling is the **V-scheme** coupling (tree-exact, from F110's static energy), the one-loop conversion to $\overline{\rm MS}$ is the *known* $a_1=(93-10n_f)/9$, and the residual is a matching scale $q_\ast$ inside a derived $\sqrt3$ band ($\Lambda^{(3)}=347$ MeV, FLAG to $1.1\%$). Its **S5 explicitly split off the IR face** as a *distinct* object: the self-consistent chiral-SB gap fixes $\alpha_\text{eff}^\ast=0.376$ ($m_D{=}0.532$) $/\,0.411$ ($m_V{=}0.727$) $\approx0.39$, "connected through the full running but not identical" to the UV constant. **This finding develops that IR face.** (J1) The IR coupling value is $\alpha_\text{eff}^\ast\approx0.39$, sharp ($\pm$few %). (J2) Its **scale** is the model's dual-Meissner gluon mass $m_D$: the gap-massive propagator freezes the running at $m_D$, with $m_D/\Lambda=O(1)$, so $\alpha(0)$ is **finite** — the model is on the **saturating/decoupling branch**, not the Landau-pole branch. (J3) That is the branch real QCD occupies: the process-independent charge saturates at $\hat\alpha(0)/\pi=0.97(4)$ *because* of a gluon mass gap $m_g=0.50(20)$ GeV, and the model **generates** that gap by mechanism (the dual superconductor *is* the IR saturation); $\alpha_\text{eff}^\ast\approx0.39$ lies in the continuum frozen-coupling range ($\sim0.3$–$0.5$, MOM/V/APT). (J4) **Correcting the F150/F145 "one shared number" framing** per F151-S5: $\lambda_6$ (F150) and χSB (F145/F77) both belong to **this** (IR) face, *not* to the UV scheme constant. (J5) The IR face is **not identical** to the UV constant; the residual is the full nonperturbative crossover solve that would yield $\alpha_\text{eff}^\ast$ without the F77 fit. See §7.

**Date:** 2026-06-12 - 18:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F152-ir-coupling-the-irface.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
