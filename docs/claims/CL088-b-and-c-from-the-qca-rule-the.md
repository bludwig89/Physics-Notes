---
id: CL088
title: 'B and C from the QCA rule: the Dirac-sea loop derives the cubic invariant completely (form, origin, sign, closed form $B=-3\sqrt2\,I_2\,\bar y^4$) and proves th'
slug: 'b-and-c-from-the-qca-rule-the'
tier: supporting
kind: no_go
status: open
domain: [QFT]
exactness: unset
findings: [F95]
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

# CL088 — B and C from the QCA rule: the Dirac-sea loop derives the cubic invariant completely (form, origin, sign, closed form $B=-3\sqrt2\,I_2\,\bar y^4$) and proves th

## Statement

B and C from the QCA rule: the Dirac-sea loop derives the cubic invariant completely (form, origin, sign, closed form $B=-3\sqrt2\,I_2\,\bar y^4$) and proves the sextic brake cannot come from any per-axis energy — C is localized to the second-shell condensate's own self-interaction

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F95-B-derived-C-localized.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F95-B-derived-C-localized.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (half derived, half a sharp no-go) — 7/7 checks PASS. **Derived from the QCA rule:** (i) the F93 Landau *angular form* itself ($B\cos3\delta+C\cos^23\delta$ — only $\cos3n\delta$ harmonics can occur, a roots-of-unity theorem); (ii) the **origin** of $B$ — it is $A_{1g}\times E_g$ interference, coefficient exactly $3\bar yA^3$, vanishing iff the democratic background vanishes; (iii) its **closed form** $B=-\tfrac{3}{2}I_2\,\bar yA^3=-3\sqrt2\,I_2\,\bar y^4$ with $I_2=\langle\cot\omega_\text{kin}\rangle_\text{BCC}=0.2202$ a pure lattice constant (verified against the full nonperturbative BZ computation to $1.4\times10^{-4}$); (iv) its **sign** — $B<0$, so the loop drives the condensate to the *hierarchical* side ($0\le\delta<30°$), exactly where the data sit ($12.73°$). **The no-go:** the same loop's sextic coefficient scales as $\bar y^{\sim7}$ vs $B\sim\bar y^4$; at the physical lattice amplitudes (F83) the angle is tetragonally locked by **31 decades**, and even at the unitarity cap the lock never opens. Since *any* per-axis energy $\sum_a u(m_a)$ has the same scaling, the brake $C$ **cannot** come from a second loop of this type: it must be a direct $O(1)$-strength function of the $E_g$ invariants — the second-shell condensate's self-interaction at saturation-scale amplitude. The data demand $C=|B|/(2\times0.785874)=0.636\,|B|$. The F93 open problem is now half-closed and half-localized. See §7.

**Date:** 2026-06-04 - 21:25

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F95-B-derived-C-localized.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
