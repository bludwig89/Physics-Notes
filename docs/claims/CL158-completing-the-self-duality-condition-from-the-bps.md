---
id: CL158
title: 'Completing the self-duality condition from the BPS structure: the **radial** half *is* derived (the 45° self-dual pair rotation $\Rightarrow Q=\tfrac23$), but t'
slug: 'completing-the-self-duality-condition-from-the-bps'
tier: supporting
kind: derivation
status: live
domain: [GR]
exactness: quantitative
findings: [F177]
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

# CL158 — Completing the self-duality condition from the BPS structure: the **radial** half *is* derived (the 45° self-dual pair rotation $\Rightarrow Q=\tfrac23$), but t

## Statement

Completing the self-duality condition from the BPS structure: the **radial** half *is* derived (the 45° self-dual pair rotation $\Rightarrow Q=\tfrac23$), but the **angular** half ($3\delta=Q$) is **not** a standard-Bogomolny theorem — it governs walls, not the vacuum angle — and reduces *exactly* to the one shared nonperturbative residual $C/|B|=1/(2\cos\tfrac23)=0.636$ (the F150 saturated-condensate solve)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F177-bps-self-duality-completion.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F177-bps-self-duality-completion.md` | The finding, in full | quantitative |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (honest terminus) — 4/4 checks PASS. **What this resolves:** the request to derive the self-duality principle (F176, $3\delta^*=Q$) from the model's BPS structure. The answer is **half yes, half no, both rigorous:** (i) the **radial** self-duality — $Q=\tfrac23$ — *is* derived from BPS/saturation: the pair rotation peaks at $\phi=45°$ (F82), the **self-dual** point ($\sin\phi=\cos\phi$, the Bogomolny condition), giving the $\sqrt2$/$y=1$ saturation wall (F73/F101), $\eta^2=\tfrac12$, $Q=\tfrac23$, and $\sqrt m$ at $45°$ to $(1,1,1)$ (Foot) — "$45°$ everywhere"; (ii) the **angular** self-duality $3\delta=Q$ is **not** a standard-Bogomolny consequence — the Bogomolny first-order condition fixes domain-**wall** tensions, not the vacuum angle, which remains the brake minimiser $\cos3\delta^*=-B/2C$; and no clean *second* geometric self-duality fixes it ($\sqrt m$ is not at $45°$ to any natural second reference). The angular condition is **equivalent** to the brake ratio $C/|B|=1/(2\cos\tfrac23)=0.636$ — i.e. the **F150 saturated-condensate solve, the one shared residual** (F172). **Net:** the self-duality principle is half-derived; its angular half *is* the single nonperturbative number the whole program shares, now with a sharp target ($0.636$) and a physical meaning (angular invariant = radial invariant). No false closure.

**Date:** 2026-06-30 - 01:30

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F177-bps-self-duality-completion.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
