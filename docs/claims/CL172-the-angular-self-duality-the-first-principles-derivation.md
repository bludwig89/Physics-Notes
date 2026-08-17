---
id: CL172
title: 'The angular self-duality $C/\lvert B\rvert=1/(2\cos\tfrac23)=0.63622$: the first-principles derivation is attempted along the full F176→F177→F179 program and **'
slug: 'the-angular-self-duality-the-first-principles-derivation'
tier: supporting
kind: no_go
status: live
domain: [cosmology]
exactness: exact
findings: [F199]
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

# CL172 — The angular self-duality $C/\lvert B\rvert=1/(2\cos\tfrac23)=0.63622$: the first-principles derivation is attempted along the full F176→F177→F179 program and **

## Statement

The angular self-duality $C/\lvert B\rvert=1/(2\cos\tfrac23)=0.63622$: the first-principles derivation is attempted along the full F176→F177→F179 program and **closes negative on three independent structural grounds** — there is no F92-analogue second relation ($Q$ is $\delta$-blind), the IR coupling does **not** cancel in the ratio (cubic = sea loop $O(\alpha^0)$, sextic = induced $O(\alpha^{\ge1})$), and the BPS wall degeneracy lands at $C/\lvert B\rvert=\tfrac12$ not $0.636$; with the exact $3\delta=\pi/4$ massless anchor recovered, the self-duality is a **forced posit**, not a theorem

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F199-angular-self-duality-derivation-forced-posit.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F199-angular-self-duality-derivation-forced-posit.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (honest terminus, negative) — 5/5 checks PASS. **What this does:** it executes the deferred *angular* half of the saturation self-duality (the "$3\delta^*=Q$" of F176, the open angular budget of F177, the un-performed sextic solve of F179) and reports the outcome without overclaiming. The headline is a **three-way structural no-go** that pins down *why* the angle is not derivable, each part sharper than the prior record: **(S1)** the F92 *radial* derivation worked because two independently-derived mass laws intersect at a unique angle; the angular problem has **no such second relation** — the Koide ratio $Q=\tfrac13+\tfrac16 r^2$ is **exactly $\delta$-independent** (radial), so nothing kinematic forces $3\delta=Q$ (sympy-exact, $\partial Q/\partial\delta\equiv0$). **(S2)** The decisive algebraic question of the program — does the IR coupling $\alpha_\text{eff}^*$ **cancel** in $C/\lvert B\rvert$? — is answered **no**, and structurally: the cubic $B$ is a **parameter-free Dirac-sea loop** ($O(\alpha^0)$, F95), the sextic $C=\lambda_6e^6$ is an **induced** condensate self-coupling ($O(\alpha^{\ge1})$, F145/F118), so their ratio carries $\alpha_\text{eff}^*$ undiluted and is a **computed nonperturbative number**, never an $\alpha$-independent theorem. The bare Fierz rational $\lambda_6=\tfrac29$ gives $C/\lvert B\rvert=0.582$ (not $0.636$), requiring a $1.094\times$ uncomputed IR enhancement. **(S3)** Standard BPS (F177-B2) is made **quantitative**: the only ratio the wall/bulk structure selects is the tetragonal→orthorhombic vacuum-existence threshold $C/\lvert B\rvert=\tfrac12$ (degeneracy $V_0-V_\text{int}=(2C-\lvert B\rvert)^2/4C$), and $\tfrac12\neq0.636$. **The necessary boundary condition passes exactly:** $m_e\to0$ + Koide $\Rightarrow3\delta=\pi/4$ (sympy-exact). **Value discrimination:** the data invariant sits at the self-dual $0.63622$ to $1\times10^{-5}$ ($0.89\sigma$, Koide-class) and *not* at $2/\pi$; but the **derivation** lands off **both** by $\sim9\%$, so it cannot discriminate — confirming the value is computed and the self-duality must be **posited**. **No new physics introduced to close the angle; the negative result is the deliverable.**

**Date:** 2026-06-30 - 18:55

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F199-angular-self-duality-derivation-forced-posit.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
