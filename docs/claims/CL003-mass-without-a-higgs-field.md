---
id: CL003
title: 'Mass without a Higgs field: a chiral SU(2) complex-mass step carries weak isospin exactly'
slug: 'mass-without-a-higgs-field'
tier: headline
kind: derivation
status: live
domain: [SM]
exactness: machine
findings: [F27, F41]
tests: []
modules: [casim.engine.particles.dirac, casim.engine.gauge.hypercharge]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL003 — Mass without a Higgs field: a chiral SU(2) complex-mass step carries weak isospin exactly

## Statement

Fermion mass arises from a chiral-$SU(2)$ complex-mass step that carries weak isospin as an **exact** gauge symmetry — the Ward identity holds to $1.1\times10^{-17}$ — and the would-be Higgs direction is pure gauge. Hypercharge rides the same field.

## What it extends

The Standard Model's Higgs mechanism. The model reproduces the mass term and the weak-isospin gauge structure **without a Higgs field**, so the Higgs direction is not a physical scalar degree of freedom but a gauge artifact.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F27-complex-mass-chiral-su2.md` | Chiral $SU(2)$ from β-gauging; the Higgs-free mass coupling | machine |
| `findings/F41-hypercharge-higgs-free-su2.md` | $U(1)_Y$ is exactly compatible with the Higgs-free F27 chiral $SU(2)$ mass model | exact |

Ward identity residual $1.1\times10^{-17}$ as recorded in the claims summary. Founding decision 3 in `CLAUDE.md`.

## Falsifier

**Not stated.** The claims summary gives no observational threshold for this claim, and this card does not invent one. A discovered scalar degree of freedom in the would-be Higgs direction would bear on it; what measurement would establish that, and at what precision, is an open item recorded in `docs/audits/consolidation-plan-2026-08-04.md`. Recorded as `falsifier: unset` (debt) rather than `none`, because a structural reason has **not** been argued.

## Status & history

`live` since F27 (2026-05-22), extended by F41. Not named in any supersession record. This is the model's largest single departure from the Standard Model's field content and the one with no stated falsifier — the gap is deliberate and countable rather than papered over.

## Sources

- `findings/F27-complex-mass-chiral-su2.md`
- `findings/F41-hypercharge-higgs-free-su2.md`
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 3
- `CLAUDE.md` — Core Design Decision 3
