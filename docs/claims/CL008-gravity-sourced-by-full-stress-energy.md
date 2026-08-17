---
id: CL008
title: 'Gravity is sourced by the full stress-energy tensor, and Newton''s constant is structural'
slug: 'gravity-sourced-by-full-stress-energy'
tier: headline
kind: derivation
status: live
domain: [GR]
exactness: exact
findings: [F64, F79, F106, F107, F178]
tests: []
modules: [casim.engine.interactions.gravity]
constants: [G_LATTICE]
supersessions: [S4-F178-full-stress-energy]
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL008 — Gravity is sourced by the full stress-energy tensor, and Newton's constant is structural

## Statement

The canonical law is the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$. The impedance-matched lattice dielectric $K=e^{2GM/rc^2}$ (reciprocal lock $AB\equiv1$) is its **vacuum/weak-field representation**: GR-identical PPN ($\beta=\gamma=1$), plus the rotation-rate origin story. **Newton's constant is structural**, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, fixing $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$.

## What it extends

General relativity — which the model **reproduces in vacuum rather than deviating from** — and Newton's constant, which GR takes as an input and the model derives from the lattice cell: $G=6.6743\times10^{-11}$, matching CODATA to $3\times10^{-8}$.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F178-gravity-full-tensor-adoption.md` | The decision: full-tensor source canonical; single-scalar dielectric demoted to the weak-field representation | — |
| `findings/F79-structural-newton-constant.md` | $G$ from the lattice structure itself; the closed form | exact |
| `findings/F107-canonical-a-adoption-L4-grb-gate.md` | Adoption of $a=\sqrt{8\pi}3^{1/4}\ell_P$ as the canonical SI ruler; L4 lensing confirms the $G$-match | exact / quantitative |
| `findings/F106-psi-K-sourcing-derivation.md` | The $\psi\to K$ sourcing law, no free coupling | exact (coefficient) |
| `findings/F64-em-connection-gravity.md` | The EM-connection dielectric route | — |

Founding decision 4 in `CLAUDE.md`.

## Falsifier

PPN $\beta=\gamma=1$ (Mercury 42.98″/cy); the naive **linear** dielectric ($\beta=\tfrac12$, 50.1″/cy) is excluded. Under F178 this is a **consistency requirement rather than a distinctive prediction**: in vacuum the model *is* GR, so a confirmed PPN deviation falsifies it exactly as it would falsify GR. **CL015 carries the threshold.**

## Status & history

`live`, and materially **reclassified** by F178 (ledger `S4-F178-full-stress-energy`). Before F178 the exponential metric was read as fundamental; it is now PPN-order only, the exact vacuum solution is Schwarzschild, and the energy-only $\nabla^2\ln K=-8\pi T^{00}$ (F106) is the static weak-field reduction. Inside matter a single scalar forces anisotropic stress (F173), so the interior dynamics are GR/TOV. The rest-mass-sourced route (F50/F52/F55/F62) was superseded by F64 in May, **partially** — F62's lapse-mix sign convention is still production code. **The withdrawn consequences of the pre-F178 reading are CL023–CL027.**

## Sources

- `findings/F178-gravity-full-tensor-adoption.md`
- `findings/F79-structural-newton-constant.md`
- `findings/F107-canonical-a-adoption-L4-grb-gate.md`
- `findings/F106-psi-K-sourcing-derivation.md`
- `docs/theory/supersessions.yaml` — S3, S4
- `CLAUDE.md` — Core Design Decision 4
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 8
