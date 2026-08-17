---
id: CL210
title: 'The $g_s=\tfrac12$ lattice$\to\overline{\rm MS}$ **scheme** conversion factorises **exactly** into a derived piece and one open piece: $\Lambda_{\overline{\rm M'
slug: 'the-lattice-scheme-conversion-factorises-exactly-into-a'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: exact
findings: [F239]
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

# CL210 — The $g_s=\tfrac12$ lattice$\to\overline{\rm MS}$ **scheme** conversion factorises **exactly** into a derived piece and one open piece: $\Lambda_{\overline{\rm M

## Statement

The $g_s=\tfrac12$ lattice$\to\overline{\rm MS}$ **scheme** conversion factorises **exactly** into a derived piece and one open piece: $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=1.773=\underbrace{1.299}_{\text{EXACT }V\to\overline{\rm MS}\text{ via }a_1=\tfrac{11}3}\times\underbrace{1.365}_{\text{open rule}\to V\ =\ 1/q_\ast a}$ — so Q2 is **not** wholly the shared $d_1$: its true *scheme* leg is closed, only the lattice$\to V$ match is the shared open number

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Honest partial (one leg closed exact, one leg the shared open $d_1$) — 3/3 checks PASS (`test_F239_scheme_factor_factorization.py`, <30 s, stdlib+numpy). **This executes open-derivations prompt Q2 (#9).** The prompt asks to derive the lattice$\to\overline{\rm MS}$ **scheme** conversion for the $g_s=\tfrac12$ lock from the rotor/dielectric structure (F115/F117), acceptance $\alpha_s(M_Z)$ to $<1\%$ with the factor derived, *or* a clear statement of the remaining perturbative-matching input. **Result:** the scheme conversion $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=1.773$ **factorises exactly** as $1.299\times1.365$: the first factor — the true $V\!\to\!\overline{\rm MS}$ **scheme** conversion — is **derived exactly** ($a_1(6)=\tfrac{11}3$, on the exact V-scheme identification of the lock, a rotor-structure fact); the second — the rule$\to V$ one-loop lattice matching $=1/q_\ast a$ — is the **shared open $d_1$** (the F162 vertex form-factor integral). So $\alpha_s(M_Z)=0.1180$ is reproduced *the instant $q_\ast$ is pinned*, and the residual is **one integral**: the lattice 3-gluon+ghost vertex form factors, Wilson-$28.81$-gated. **This sharpens F235's "Q1=Q2=E3=$d_1$":** only the lattice$\to V$ leg is $d_1$; Q2's *scheme* leg is closed.

**Date:** 2026-07-03 - 08:48

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
