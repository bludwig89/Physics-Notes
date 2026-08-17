---
id: CL207
title: 'The full 3×3 Higgs-free see-saw: the F93/F76/F201 $E_g$ generation texture fixes the three light active masses (reducing exactly to F47 per generation), but for'
slug: 'the-full-3-3-higgs-free-see-saw'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F236]
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

# CL207 — The full 3×3 Higgs-free see-saw: the F93/F76/F201 $E_g$ generation texture fixes the three light active masses (reducing exactly to F47 per generation), but for

## Statement

The full 3×3 Higgs-free see-saw: the F93/F76/F201 $E_g$ generation texture fixes the three light active masses (reducing exactly to F47 per generation), but forces PMNS $=\mathbb 1$ — a structural no-go that pins lepton mixing to the second-shell $T_{2g}$ channel, whose three amplitudes remain free inputs

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F236-three-generation-seesaw-pmns.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F236-three-generation-seesaw-pmns.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Derivation + honest negative result — 5/5 checks PASS (`test_F236_three_generation_seesaw.py`, ~15 s, numpy real/complex arithmetic with hand-rolled residual checks). **What is derived (exact/machine-precision):** the 3×3 see-saw $[[0,M_D],[M_D^\top,M_R]]$ generalises F47 and reduces to three copies of the F47 $M_D^2/M_R$ block at machine precision; with $M_D$ and $M_R$ both carrying the $E_g$ texture (the F93 O1 diagonal-traceless channel) the light matrix $m_\nu=-M_D M_R^{-1}M_D^\top$ is **diagonal**, so **PMNS $=\mathbb 1$** exactly. **What is a free input (the honest core):** large lepton mixing cannot come from $E_g$ alone — it is forced onto the second-shell $T_{2g}$ (axis-mixing) channel (F93 falsifiable commitment #1), whose three amplitudes are **not pinned** by the texture. All five oscillation observables ($\theta_{12},\theta_{13},\theta_{23},\Delta m^2_{21},\Delta m^2_{31}$) are reproducible, but with **6 inputs for 5 observables** — the *masses/hierarchy* are derived (F201 node), the *mixing angles* are free.

**Date:** 2026-07-03 - 15:20

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F236-three-generation-seesaw-pmns.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
