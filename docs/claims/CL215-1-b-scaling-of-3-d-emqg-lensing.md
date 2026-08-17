---
id: CL215
title: '1/b scaling of 3-D EMQG lensing (isolated Green''s function, no free α)'
slug: '1-b-scaling-of-3-d-emqg-lensing'
tier: supporting
kind: derivation
status: live
domain: [GR]
exactness: exact
findings: [F244]
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

# CL215 — 1/b scaling of 3-D EMQG lensing (isolated Green's function, no free α)

## Statement

1/b scaling of 3-D EMQG lensing (isolated Green's function, no free α)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F244-emqg-1overb-3d-lensing.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F244-emqg-1overb-3d-lensing.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Closes open-derivation **F2** (prompt #17; exactness-inventory not-yet-met #2). The F3b deflection scan (`run_phaseF_tests.py::test_F3b_scan`) verified $\Delta y(b)\propto1/b$ only for the **phenomenological** metric $c=c_0(\lvert\Phi\rvert/v)^\alpha$ with a **free fit exponent** $\alpha=1.5$. This finding re-runs the scan on the **genuine 3-D EMQG Newtonian potential** (`ca_emqg.solve_poisson_3d`, true $1/r$ Green's function) with the parameter-free GR-Shapiro coupling $c=c_0/(1-2\phi/c_0^2)$. The lensing obeys $\Delta\theta\propto1/b$: the **exact continuum thin-lens closed form** gives slope $-0.9959$ (machine $1/b$), the lattice isolated-slice line integral $-1.074$, the periodic-FFT slice $-1.062$, and the Cayley exact-unitary stepper reproduces the deflection **toward the mass** with norm conserved to $10^{-15}$. The free $\alpha$ is eliminated.

**Date:** 2026-07-03 - 14:35

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F244-emqg-1overb-3d-lensing.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
