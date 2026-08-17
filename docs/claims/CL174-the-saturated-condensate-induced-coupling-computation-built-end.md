---
id: CL174
title: 'The saturated-condensate induced-coupling computation, built end-to-end: $C/\lvert B\rvert$ assembled from the full-BZ sea cubic $B$, the saturation amplitude $'
slug: 'the-saturated-condensate-induced-coupling-computation-built-end'
tier: supporting
kind: no_go
status: live
domain: [QCD]
exactness: exact
findings: [F200]
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

# CL174 — The saturated-condensate induced-coupling computation, built end-to-end: $C/\lvert B\rvert$ assembled from the full-BZ sea cubic $B$, the saturation amplitude $

## Statement

The saturated-condensate induced-coupling computation, built end-to-end: $C/\lvert B\rvert$ assembled from the full-BZ sea cubic $B$, the saturation amplitude $e^6$, the recomputed IR coupling $\alpha_\text{eff}^*$, and the induced sextic $\lambda_6=\tfrac29\,c$ — landing at $0.69$ (central), with the residual collapsed to the **single $O(1)$ quartic $c$**; the sextic/quartic ratio of the $E_g$ composite **is** the F145 Fierz rational $\tfrac29$ (matches F118's independent fit to $0.6\%$), and the calculation confirms F199 quantitatively: $\alpha_\text{eff}^*$ does not cancel and the value cannot be discriminated from $2/\pi$

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F200-eg-sextic-coupling-computed.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F200-eg-sextic-coupling-computed.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (the calculation is built and runs) — 5/5 checks PASS. **What this delivers:** the end-to-end machine computation that F199 pointed to as the open object. It assembles $C/\lvert B\rvert$ from four pieces, three of them computed from first principles with the validated kernels: **(1)** $B$ — the **full nonperturbative** Dirac-sea cubic on the BCC Brillouin zone at the saturation amplitude ($\lvert B\rvert=0.0486$, $1.78\times$ the leading closed form, $B<0$ = hierarchical side); **(2)** $e^6$ — the saturated $E_g$ amplitude (unitarity cap $\bar y=\sqrt2-1$, $e^2=3\bar y^2$, $e^6=0.1364$); **(3)** $\alpha_\text{eff}^*$ — the IR coupling **recomputed end-to-end** from the full nonlinear $\chi$SB gap solve $M(k)$ (band $[0.376,0.411]$, mean $0.394$ — reproduces F152/F154 with no imported value); **(4)** $\lambda_6$ — the induced sextic clock coupling, computed as the **per-order Fierz relation** $\lambda_6=\tfrac29\,c$, where $c$ is the $E_g$ quartic and $\tfrac29$ is the F145 colour-blind rational carried up one order. **The headline derivation content:** the **sextic/quartic ratio of the $E_g$ composite is exactly the Fierz $\tfrac29$** — with the F118 self-consistent quartic $c=1.10$ this gives $\lambda_6=0.244$, matching F118's *independent* fit $0.243$ to $0.6\%$; so the open sextic $\lambda_6$ is **reduced to the already-$O(1)$-pinned quartic $c$** via an exact rational. **The assembled number:** $C/\lvert B\rvert=\tfrac29\,c\,e^6/\lvert B\rvert=0.69$ (central), with the residual band over the F118 quartic range $c\in[0.75,1.20]$ equal to $[0.47,0.75]$ — which **brackets both** the self-dual $0.63622$ and $2/\pi=0.63662$. **The verdict (F199 quantified):** $\alpha_\text{eff}^*$ does **not** cancel (it enters $C$ through $c$, while $B$ is the parameter-free sea loop), so $C/\lvert B\rvert$ is a **computed nonperturbative number**, and the $\sim20\%$ residual in the single quartic $c$ means the calculation **cannot discriminate** the self-dual value from $2/\pi$ (split $4\times10^{-4}$). The residual is no longer "all of $\lambda_6$" — it is one $O(1)$ coupling, the same shared IR/saturation normalisation.

**Date:** 2026-06-30 - 20:40

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F200-eg-sextic-coupling-computed.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
