---
id: CL182
title: 'Relativistic (F125 Dirac–Coulomb) ionization energies in the multi-electron SCF, and the light-element accuracy map'
slug: 'relativistic-f125-dirac-coulomb-ionization-energies-in-the'
tier: supporting
kind: derivation
status: live
domain: [SR]
exactness: unset
findings: [F208, F371]
tests: [F208-relativistic-scf-ie, F371-medium-z-scf-ionization-energies]
modules: [src/casim/engine/core/manybody.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-08-04'
last_verified: '2026-09-05'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL182 — Relativistic (F125 Dirac–Coulomb) ionization energies in the multi-electron SCF, and the light-element accuracy map

## Statement

Relativistic (F125 Dirac–Coulomb) ionization energies in the multi-electron SCF, and the light-element accuracy map

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F208-relativistic-scf-ionization-energies.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F208-relativistic-scf-ionization-energies.md` | The finding, in full (Z=1-20 sweep) | unset |
| `findings/F371-medium-z-relativistic-scf-ionization-energies.md` | Extension to the full 3d series (Z=21-30, Sc-Zn, incl. Fe); confirms the exchange-correlation underbinding (33-48%) and sub-meV relativistic valence shift persist, and documents a previously-unflagged fixed-grid numerical caveat that grows with Z | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

**2026-09-05 (F371):** extended, not re-derived. F371 ran the same, unmodified machinery over Z=21-30 (the full first transition-metal row) and confirms the same physical conclusion (Hartree/no-exchange underbinding, not relativity) at every new Z checked, including Fe. It also surfaces a second limitation this card's evidence did not previously carry: `electron_cloud_hartree`'s fixed-N=900 uniform radial grid is not grid-converged above roughly Z~20, with a numerical uncertainty (checked at N=1200) that grows with Z and is not yet separated from the physical error above Z~25. `exactness: unset` and `review_state: unreviewed-seed` are both still accurate -- this update only extends the evidence table and findings list per D12's narrowed-not-rewritten precedent; promoting the card itself to `authored` remains future work.

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 7/7 checks PASS (`test_F208_relativistic_scf_ie.py`). The F125 scalar Dirac–Coulomb shift is now wired into the Hartree SCF; a Z=1–20 sweep quantifies where the multi-electron accuracy breaks down.

**Date:** 2026-07-01 - 00:30

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F208-relativistic-scf-ionization-energies.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
