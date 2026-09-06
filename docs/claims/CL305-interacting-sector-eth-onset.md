---
id: CL305
title: 'A next-nearest-neighbour interaction breaks a quadratic lattice-fermion sector''s generalised Gibbs ensemble toward genuine eigenstate thermalisation; a nearest-neighbour interaction alone does not'
slug: interacting-sector-eth-onset
tier: supporting
kind: derivation
status: live
domain: [QM, condensed-matter]
exactness: quantitative
findings: [F300, F309, F376]
tests: [F376-interacting-sector-eth-onset]
modules: [src/casim/engine/interactions/thermodynamics_interacting.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-09-06
last_verified: 2026-09-06
provenance: authored
review_state: authored
confidence: medium
---

# CL305 — A next-nearest-neighbour interaction breaks a quadratic lattice-fermion sector's generalised Gibbs ensemble toward genuine eigenstate thermalisation; a nearest-neighbour interaction alone does not

## Statement

F300/F309 showed, exactly, that this project's free (quadratic) lattice-fermion sector has an
extensive tower of conserved single-particle-mode occupations and reaches a generalised Gibbs
ensemble (GGE), never a Gibbs state. F376 measures, on the smallest interacting extension of that
same conserved-charge structure (an open spinless-fermion chain, exact diagonalisation, no
truncation), that a nearest-neighbour density-density interaction ALONE does not break this —
it is Jordan-Wigner-dual to the integrable XXZ chain — while adding a next-nearest-neighbour
term does: three independent standard diagnostics (level-spacing-ratio separation from Poisson
toward GOE, an entanglement-plateau/volume-law-ceiling fraction that stays $L$-independent for
the generic case while falling for the integrable one, and an eigenstate-to-eigenstate
entanglement-fluctuation spread that shrinks with $L$ only for the generic case) agree, with the
expected finite-size flow across $L=10,12,14$.

## What it extends

This applies the standard eigenstate thermalisation hypothesis (ETH) framework of many-body
quantum mechanics — established in Srednicki 1994, Deutsch 1991, and reviewed comprehensively in
D'Alessio, Kafri, Polkovnikov & Rigol, Adv. Phys. **65**, 239 (2016) — to this project's own
lattice-fermion sector for the first time. It is not a new theorem of quantum mechanics; it is a
measurement that this project's specific lattice construction reproduces the established
integrable-vs-generic dichotomy (Poisson vs. GOE level statistics; GGE vs. Gibbs relaxation)
rather than doing something exotic. Extends [[F300-lattice-native-thermodynamics]] (sec4.1, the
GGE result for the model's free sector) and [[F309-gstar-from-model-content]] (sec7.2, the same
caveat reaffirmed for the fermionic content) by giving their first interacting-sector datum.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F376-interacting-sector-eth-onset.md` | full derivation, three diagnostics, three system sizes, one verified control | quantitative |
| `test-results/F376_interacting_sector_eth_onset.json` | raw measured numbers for all three regimes, all three $L$, and the control run | quantitative |
| `tests/registry/interactions.yaml` (`F376-interacting-sector-eth-onset`) | gate-tier registry record, declared control `v2_control=True` verified red at exactly C3-C6 | — |

## Falsifier

A re-run at larger $L$ (16-20) that shows `integrable_V1`'s level-spacing ratio failing to
continue converging toward the Poisson value 0.3863, or `generic_V1V2`'s eigenstate-to-eigenstate
entanglement-entropy fluctuation failing to continue shrinking, would directly contradict this
claim — it would mean the two-tier separation measured at $L\le14$ was a finite-size coincidence
rather than the onset of the expected thermodynamic-limit behaviour. Concretely: `casim test --id
F376-interacting-sector-eth-onset --param Ls=[16,18,20]` (after porting the module to a sparse/
Lanczos eigensolver, since the current dense `numpy.linalg.eigh` implementation does not scale
past $L\approx14$ on the available hardware — see the finding sec9).

## Status & history

Issued live at first writing (2026-09-06); no prior broader form to narrow. The claim is
deliberately scoped to what was measured: a 1D single-band open-boundary toy reduction of the
free-fermion machinery, not the model's own 3D two-branch BCC lattice, and not F110's link
Hamiltonian coupled to dynamical matter (that coupling remains unbuilt — F110 sec5). `confidence:
medium` reflects this scope, and the finite range of system sizes (three points, $L\le14$),
rather than any doubt about the individual measurements, which are validated to machine precision
against an independent full-Fock-space construction (finding sec3).

## Sources

- `findings/F376-interacting-sector-eth-onset.md`
- `findings/F300-lattice-native-thermodynamics.md` (sec4.1)
- `findings/F309-gstar-from-model-content.md` (sec7.2)
- `findings/F110-realtime-link-hamiltonian-confinement.md` (sec5)
- Oganesyan & Huse, Phys. Rev. B 75, 155111 (2007) — the level-spacing ratio statistic
- Atas, Bogomolny, Giraud & Roux, Phys. Rev. Lett. 110, 084101 (2013) — Poisson/GOE mean ratio values
- Santos & Rigol, Phys. Rev. E 81, 036206 (2010), arXiv:0910.2985 — the t-V-V' integrability-breaking model
- D'Alessio, Kafri, Polkovnikov & Rigol, Adv. Phys. 65, 239 (2016) — the ETH review this finding's third diagnostic follows
