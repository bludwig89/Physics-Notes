---
id: CL105
title: 'The self-consistent $(W,v,c)$ derivation closes on the spontaneous-$E_g$ (Mexican-hat) branch, the $\kappa_E>0$ branch is excluded, and the brake $C$ is localiz'
slug: 'the-self-consistent-derivation-closes-on-the-spontaneous'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F118]
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

# CL105 — The self-consistent $(W,v,c)$ derivation closes on the spontaneous-$E_g$ (Mexican-hat) branch, the $\kappa_E>0$ branch is excluded, and the brake $C$ is localiz

## Statement

The self-consistent $(W,v,c)$ derivation closes on the spontaneous-$E_g$ (Mexican-hat) branch, the $\kappa_E>0$ branch is excluded, and the brake $C$ is localized to the $E_g$ condensate's own clock self-interaction at $O(1)$ strength ($\lambda_6=0.243\approx\tfrac14$, equivalently $W=1.46$) — with the sea loop now ruled out for $C$ by *sign* as well as scaling

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial-positive (an existence closure on the physical branch + a sign no-go + an $O(1)$ localization; the first-principles value of $\lambda_6$ remains the residual) — 8/8 checks PASS. **The headline:** the $(W,v,c)$ triple that F108-T5 left open *does* have a self-consistent solution — but **only** on the $\kappa_E<0$ (attractive-$E_g$, Mexican-hat) branch, which is precisely the **spontaneous** $E_g$ condensation sign F93 already demands. On that branch the exact PDG lepton spectrum is the **global** ground state to grid resolution (gap $=-2\times10^{-6}$ under a $121^3$ brute search), with wall-KKT $<0$, PD constrained Hessian, and **all completion couplings $O(1)$** ($\kappa_E\approx-2.2,\ c\approx1.1,\ v\approx0.16,\ W=W^*(v)\approx0.44$). The $\kappa_E>0$ (repulsive) branch is **excluded** everywhere on the angle-locked line $W=W^*(v)$ (best global gap $0.066$; the empty $(0,0,0)$ always wins) — F108-T5 is sharpened from one point to the whole $(v,c)$ plane and then *closed* on the correct branch. **For $C$:** the brake is the unique symmetry-allowed $E_g$ "clock" self-interaction $C=\lambda_6\,e^6$ (the $e^6\cos^23\delta$ invariant); the **derived** cubic $B$ (F95) and the data ratio fix $\lambda_6=0.636|B|/e^6=0.243=O(1)$ — strikingly close to $\tfrac14$ — i.e. the equivalent brake $W=6\lambda_6=1.46$ (reproducing F101-B). And the sea loop is now **doubly excluded** as the source of $C$: beyond F95's wrong *scaling* ($C_\text{loop}\sim\bar y^7$ at small amplitude), the clip-free projection at saturation shows the loop's own sextic is **wrong-sign** ($C_\text{loop}=-0.018<0$, an anti-brake). See §6.

**Date:** 2026-06-09 - 12:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
