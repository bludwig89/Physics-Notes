---
id: CL311
title: 'The F73 Cooper-pair Higgs candidate''s fermion coupling is real, computable and non-universal within its own species, and structurally species-local across species'
slug: 'cooper-pair-higgs-coupling-species-local-not-universal'
tier: supporting
kind: no_go
status: live
domain: [SM, QFT]
exactness: quantitative
findings: [F399, F73, F74, F77]
tests: [F399-composite-scalar-fermion-coupling]
modules: [casim.engine.particles.derive_composite_scalar_fermion_coupling]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL070
falsifier: stated
first_issued: '2026-09-23'
last_verified: '2026-09-23'
provenance: authored
review_state: authored
confidence: high
---

# CL311 — The F73 Cooper-pair Higgs candidate's fermion coupling is real, computable and non-universal within its own species, and structurally species-local across species

## Statement

The F73 Cooper-pair Higgs candidate, bound by the F74/F77 contact/NJL dynamics, has a genuine, finite, computable coupling to its own constituent fermion species — $g_{\sigma qq}=1/\sqrt{2N_cN_fK(4M^2)}$, the same standard NJL residue-at-the-pole formula that gives the pion's Goldberger–Treiman coupling, evaluated at the model's own $m_\sigma=2M$ marginal-binding pole (finite there, no threshold singularity). Unlike the pion's coupling, this scalar coupling carries no protecting symmetry: the analogue of the Goldberger–Treiman ratio, $g_{\sigma qq}f_\pi/M$, is **not** a coupling-independent constant (an $81\%$ spread measured across a five-point coupling sweep, against the pion ratio's exact, symmetry-protected constancy). More consequentially, this coupling is **structurally confined to the species it was built from**: in a general multi-flavor NJL Lagrangian, the RPA-resummed meson propagator matrix is exactly block-diagonal whenever the cross-species contact matrix element $G_{ab}=0$ for $a\ne b$ (proven here as an exact $2\times2$ linear-algebra fact, not an approximation), so a composite built from one fermion species' own condensate has identically zero coupling to any other species absent an explicit new 4-fermion vertex — which this model supplies nowhere.

## What it extends

The $\kappa$-framework parametrization of Higgs-like couplings (the empirical signature that every SM fermion's coupling to the 125 GeV resonance tracks its own mass, confirmed to high precision since 2022 — *Nature* 607, 52-59) and the standard theory of composite/dynamical electroweak symmetry breaking (Nambu–Jona-Lasinio dynamical mass generation; the extended-technicolor program's answer to how a strongly-coupled condensate can source *every* SM fermion's mass and coupling from one sector, via a lattice of cross-generation 4-fermion operators). This card computes, for this model specifically, why the NJL machinery it already has (F74/F77) cannot reach that signature on its own, and names precisely the missing ingredient (an extended-technicolor-style cross-species operator) in the model's own vocabulary.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F399-composite-scalar-fermion-coupling.md` | $g_{\sigma qq}$ derived, finite, and computed ($2.105$ at F77's canonical fit); the GT-type ratio's $81\%$ non-universal spread vs. the pion's $6.2\times10^{-12}$ spread; species locality proven exact ($0.0$ off-diagonal residual) on a two-flavor toy model, with a control ($G_{ab}=0.01$) confirming a real cross-species term would break it | quantitative (the coupling formula and species-locality proof are exact/machine; the non-universality spread is a measured quantitative result) |
| `findings/F77-njl-gap-rpa-selfconsistent.md` | The gap equation + RPA ladder this card's coupling formula is extracted from, validated against measured QCD data (M, $f_\pi$, $m_\pi$, $\langle\bar qq\rangle$ to $0.2$–$4\%$) | quantitative |
| `findings/F73-spin0-bound-pair-scalar.md`, `findings/F74-two-constituent-bound-state-binding.md` | The Cooper-pair channel and its binding machinery this coupling is built on | exact / quantitative |

## Falsifier

Two, at different depths:

1. **The non-universality measurement, directly.** A denser or wider coupling sweep finding the scalar GT-type ratio $g_{\sigma qq}f_\pi/M$ *does* converge to a coupling-independent constant (analogous to the pion's) would falsify the "no protecting symmetry" reading. Threshold: spread below the same $50\%$ bar this card's own gate check uses, checked over an extended range.
2. **The species-locality claim, structurally.** This is falsified only by exhibiting an explicit cross-species 4-fermion contact operator ($G_{ab}\ne0$ for two distinct SM fermion species) already present, or forced, by some other part of the model's structure — not asserted by hand, the way this card's own toy-model control does it. No such operator is currently named anywhere in the tree (cross-checked against NB2-001's "no Yukawa mechanism anywhere" finding); finding one would be a genuinely new structural result, not a numerical tuning.

## Status & history

First issued 2026-09-23, from `findings/F399-composite-scalar-fermion-coupling.md`. Rolls up to `CL070` (F73's own, currently `unreviewed-seed`, `status: open` card) as the specific coupling-construction half of that broader claim; this card is `authored` and independent of CL070's own review state. No prior status to narrate.

## Sources

- `findings/F399-composite-scalar-fermion-coupling.md`
- `findings/F73-spin0-bound-pair-scalar.md`
- `findings/F74-two-constituent-bound-state-binding.md`
- `findings/F77-njl-gap-rpa-selfconsistent.md`
- `docs/theory/notebook-v2/NB2-001-cooper-pair-higgs-vs-stueckelberg.md` (the question this card answers)
- *Nature* 607, 52-59 (2022) — the $\kappa$-framework mass-proportional-coupling measurement this card's result is checked against
