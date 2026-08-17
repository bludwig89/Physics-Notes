---
id: CL086
title: 'Pairing classification theorem: the branch structure of each coupling forces its channel — γ even (forced), W± chiral (forced), Z mixed (derived), gluon even (f'
slug: 'pairing-classification-theorem-the-branch-structure-of-each'
tier: supporting
kind: derivation
status: live
domain: [QCD]
exactness: exact
findings: [F91, F317]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-08-04'
last_verified: '2026-08-16'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL086 — Pairing classification theorem: the branch structure of each coupling forces its channel — γ even (forced), W± chiral (forced), Z mixed (derived), gluon even (f

## Statement

Pairing classification theorem: the branch structure of each coupling forces its channel — γ even (forced), W± chiral (forced), Z mixed (derived), gluon even (forced; the chiral BCC gluon assignment is unforced)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F91-pairing-classification-theorem.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F91-pairing-classification-theorem.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 13/13 checks (5 exact over ℚ / structural-zero, 6 machine ≤ 2×10⁻¹³, 2 quantitative/contrast). Completes the F68→F89 chain: the chiral pairing is now *derived* where it holds (W±) and shown *unforced* where it was assumed (gluon BCC).

**Date:** 2026-06-04 - 14:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F91-pairing-classification-theorem.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract

## Amendment 2026-08-16 — the one unforced assignment is closed (F317)

F91's gluon row concluded that the BCC even law is *"unforced, and the F68-mirror argument + the
elegant-design philosophy select the even law"*, and its G1 leg recorded colour's vector-like
coupling as **`by construction`**. [[F317-su3-structure-derived]] supplies the missing premise:
all 27 symmetric anomaly coefficients of $su(2)$ are **exactly** zero while $su(3)$ carries
$A^{888}=-1/\sqrt3$, so of $\{$vector-like, chiral, conjugate$\}$ exactly one colour assignment
is anomaly-free. Vector-like is therefore **forced**, the branch-space coupling's traceless part is
`0.0`, and F91 G1's chain to the even law runs with no free step.

**Nothing in F91 is retracted and F91 is left bit-unchanged** (D12): its classification stands
exactly as written, and only the *status* of one of its four rows moves from selected-on-elegance
to forced. The contrast F91 measured — that a chiral colour would split the branches by
$\lvert\Delta\Omega\rvert/2$ — is re-measured in F317 §2 at $5.137\times10^{-3}$ on the body
diagonal, so the statement is not vacuous. See also **CL271**.
