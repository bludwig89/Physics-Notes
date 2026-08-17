---
id: CL230
title: 'All-orders QED: renormalizability closure, Ward–Takahashi $Z_1=Z_2$ and charge universality, the Callan–Symanzik equation, and the ABJ anomaly with Nielsen–Nino'
slug: 'all-orders-qed-renormalizability-closure-ward-takahashi-and'
tier: supporting
kind: derivation
status: live
domain: [QFT]
exactness: exact
findings: [F264]
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

# CL230 — All-orders QED: renormalizability closure, Ward–Takahashi $Z_1=Z_2$ and charge universality, the Callan–Symanzik equation, and the ABJ anomaly with Nielsen–Nino

## Statement

All-orders QED: renormalizability closure, Ward–Takahashi $Z_1=Z_2$ and charge universality, the Callan–Symanzik equation, and the ABJ anomaly with Nielsen–Ninomiya consistency

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F264-qed-allorders-renormalizability-anomaly.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F264-qed-allorders-renormalizability-anomaly.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 17/17 checks PASS. Fourteen of the seventeen gates are **algebraically exact** (sympy, literal 0 / exact rational): the power-counting formula $D=4-\tfrac32E_f-E_\gamma$ with its order-independence, the counterterm closure to exactly $\{Z_1,Z_2,Z_3,\delta m\}$, the photon-insertion identity that makes Ward–Takahashi hold at every order, $Z_1=Z_2$ as the *unique* solution of the differential WT identity, charge universality, $\beta=e\gamma_3$ and $\beta=e^3/12\pi^2$ from F251's $b_0=\tfrac43$, the $\gamma_5$ trace identities over all 512 index combinations, **two independent exact routes to the ABJ coefficient $\tfrac{1}{16\pi^2}$** (Fujikawa heat kernel and the shift surface term $\tfrac{1}{32\pi^2}$), the vector-safe/axial-anomalous dichotomy, and the Weyl-point census. The remaining three are one numerical scan and two quantitative comparisons ($\pi^0\to\gamma\gamma$ at 0.65%, $0.4\sigma$; the Landau pole).

**Date:** 2026-07-26 - 14:10

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F264-qed-allorders-renormalizability-anomaly.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
