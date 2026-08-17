---
id: CL159
title: 'The $E_g$ sextic brake $\lambda_6$: the first-principles derivation attempt closes **negative**, so the charged-lepton spectrum is honestly relabelled as a **on'
slug: 'the-sextic-brake-the-first-principles-derivation-attempt'
tier: supporting
kind: derivation
status: open
domain: [cosmology]
exactness: exact
findings: [F179]
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

# CL159 — The $E_g$ sextic brake $\lambda_6$: the first-principles derivation attempt closes **negative**, so the charged-lepton spectrum is honestly relabelled as a **on

## Statement

The $E_g$ sextic brake $\lambda_6$: the first-principles derivation attempt closes **negative**, so the charged-lepton spectrum is honestly relabelled as a **one-angle consistency fit** — but the fitted object is the *convention-independent* condensate angle $\delta^*$ (not the convention-laden $\lambda_6$), which is Koide-locked to $\delta^*=\tfrac29$ rad ($3\delta^*=Q=\tfrac23$) at $<1\sigma$, and granting that one relation fixes the whole spectrum to $0.01\%$

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F179-lambda6-derivation-attempt-and-relabel.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F179-lambda6-derivation-attempt-and-relabel.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Resolved-as-relabel (audit C2 addressed; derivation **not** achieved, epistemic status corrected and sharpened) — 5/5 checks PASS. **What this finding does:** it answers the audit-2026-06-29 priority item C2 ("derive the sextic brake $C$ / $\lambda_6$ from the $E_g$ condensate dynamics, **or** honestly relabel the lepton spectrum as a one-parameter fit"). The derivation is attempted along the only open route (the F145 induced-coupling / F150 saturated-condensate solve) and **closes negative**: $\lambda_6$ cannot be reduced to a first-principles number in this work. The honest outcome is therefore the **relabel** — but a sharper one than the audit proposed, on three decisive numerical facts: **(i)** $\lambda_6$ is **not** a clean rational — the two recurring binding-block rationals that bracket the F118 fit, $\tfrac29$ (Fierz, F145) and $\tfrac14$ (rotor, F115), give condensate angles $10.25°$ and $13.40°$, **missing** the data $\delta^*=12.7328°$ by $2.48°$ and $0.67°$ respectively; so the "$\lambda_6\approx\tfrac14$" framing of F118/F119/F120 is misleading and the bare induced rational does **not** deliver the angle. **(ii)** The *convention-independent* invariant $\delta^*=\tfrac29$ rad (equivalently $3\delta^*=Q=\tfrac23$, F150) **is** satisfied — to $<1\sigma$ of the $m_\tau$ experimental error, the **same confidence class as the Koide relation itself** — but it equates a radian-valued angle to a dimensionless ratio, which can only be confirmed by the saturated-condensate solve, so it remains a **target with a rationale, not a derivation**. **(iii)** If the two candidate-exact condensate relations ($Q=\tfrac23$, derived F92; and $\delta^*=\tfrac29$ rad, the target) are *granted*, one mass anchor ($m_\tau$) fixes the **entire** charged-lepton spectrum ($m_\mu/m_\tau$, $m_e/m_\tau$) to $0.01\%$ — quantifying the spectrum as a **one-angle fit**, not a zero-parameter prediction. See §6.

**Date:** 2026-06-29 - 15:40

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F179-lambda6-derivation-attempt-and-relabel.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
