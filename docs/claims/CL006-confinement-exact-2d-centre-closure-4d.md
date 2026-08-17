---
id: CL006
title: 'Confinement: exact in 2D, and a Z3 centre-phase colour-dielectric dual superconductor in 3+1D'
slug: 'confinement-exact-2d-centre-closure-4d'
tier: headline
kind: derivation
status: narrowed
domain: [QCD]
exactness: exact
findings: [F97, F101, F110, F142]
tests: []
modules: [casim.engine.gauge.confinement, casim.engine.gauge.link_hamiltonian]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: medium
---

# CL006 — Confinement: exact in 2D, and a Z3 centre-phase colour-dielectric dual superconductor in 3+1D

## Statement

Confinement is **exact in 2D** — an area law with $\sigma=-\ln w(\beta)>0$ for all $\beta$. In 3+1D it is a colour-dielectric dual superconductor, cross-checked against gauge Monte-Carlo, governed by $\mathbb Z_3$ centre-phase closure.

## What it extends

QCD confinement, which has no analytic proof in 3+1D. The model's 2D result is exact; the 3+1D result is a mechanism plus a numerical cross-check, and the card states the two at different strengths **deliberately**.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F101-strong-coupling-sigma-compact-rotor.md` | Full strong-coupling $\sigma$ from the compact-rotor transfer operator; the non-perturbative log law | exact (2D) |
| `findings/F97-baryon-phase-closure-no-go.md` | Baryon stability and binding are both centre-phase closure; the F92 fixed point provably fails for $N=3$ | exact (no-go) |
| `findings/F110-realtime-link-hamiltonian-confinement.md` | Real-time link Hamiltonian, Gauss's law exact by construction; flux tube persists and melts in real time | machine |
| `findings/F142-dielectric-tension-no-go-and-nonabelian-scope.md` | A colour-dielectric tube cannot carry $2\pi v^2n$; the exact map is the centre route | exact (no-go) |

The dynamical non-Abelian condensate VEV is **open**.

## Falsifier

**Not stated as a single threshold.** The claims summary gives no falsification threshold for confinement. The honest open item is the dynamical non-Abelian condensate VEV (F142); until that closes, the 3+1D half is a mechanism rather than a derivation. `falsifier: unset` is debt and is recorded as such rather than dressed as `none`.

## Status & history

`narrowed`. **The broad form** — "confinement is derived" as a single sentence — overstates the 3+1D half. The narrow form above splits it: exact in 2D, mechanism-plus-cross-check in 3+1D. Narrowed 2026-08-04 by this card; **no finding changed**, which is the point of the layer.

## Sources

- `findings/F101-strong-coupling-sigma-compact-rotor.md`
- `findings/F97-baryon-phase-closure-no-go.md`
- `findings/F110-realtime-link-hamiltonian-confinement.md`
- `findings/F142-dielectric-tension-no-go-and-nonabelian-scope.md`
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 6
