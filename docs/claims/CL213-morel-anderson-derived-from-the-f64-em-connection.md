---
id: CL213
title: 'Morel–Anderson μ* derived from the F64 EM-connection dielectric'
slug: 'morel-anderson-derived-from-the-f64-em-connection'
tier: supporting
kind: derivation
status: live
domain: [condensed-matter]
exactness: machine
findings: [F242]
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

# CL213 — Morel–Anderson μ* derived from the F64 EM-connection dielectric

## Statement

Morel–Anderson μ* derived from the F64 EM-connection dielectric

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F242-mustar-from-f64-dielectric.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F242-mustar-from-f64-dielectric.md` | The finding, in full | machine |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. Closes open-derivation **S1** (prompt #15). The F64 lattice EM dielectric $K$, in its static long-wavelength limit for the conduction-electron medium, **is** the Thomas–Fermi / RPA screening function $\varepsilon(q)=1+k_{TF}^2/q^2$ — the same F64 dielectric already invoked by `deformation_potential_bare` (D=⅔E_F) and `bohm_staver_cs` for the phonon side (F211/F213). Screening the bare Coulomb with it and Fermi-surface averaging gives a **parameter-free** repulsion $\mu(r_s)$, and the Morel–Anderson (1962) retardation reduction — evaluated at the solver's own Coulomb cutoff — gives $\mu^*$. The derived $\mu^*$ lands at **0.10–0.12**, matching the tabulated empirical values with no fit, and cuts the Allen–Dynes 7-element mean $T_c$ error from **14.3% → 6.3%** (simple metals 17.7% → 6.7%). The last empirical input in the SC sector is now derived.

**Date:** 2026-07-03 - 14:35

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F242-mustar-from-f64-dielectric.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
