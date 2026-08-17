---
id: CL010
title: 'Charge quantisation is derived, not assumed'
slug: 'charge-quantisation-derived'
tier: headline
kind: derivation
status: live
domain: [SM]
exactness: exact
findings: [F165, F279, F47, F27, F41]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-08-02'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL010 — Charge quantisation is derived, not assumed

## Statement

Given the lattice-fixed representation content, the generation hypercharges are the **unique** solution — up to a single overall normalisation — of two anomaly rows, the three F27/F41 mass-step rows, and the **F47 Higgs-free Majorana step**. That last row closes the system: $\nu_R^{\mathsf T}C\nu_R$ carries hypercharge $2y_\nu$, so gauge invariance forces $y_\nu=0$ exactly, and a Majorana mass is available only to a field of exactly zero hypercharge. The solution is
$$y_Q:y_u:y_d:y_L:y_e:y_\nu=1:4:-2:-3:-6:0,\qquad y_\phi=3y_Q,$$
and normalising $y_Q=\tfrac16$ gives the SM assignment and the measured electric charges $(\tfrac23,-\tfrac13,0,-1)$, **exactly over ℚ**.

## What it extends

The Standard Model, which takes hypercharge assignment as input, and the SM theorems this parallels (Minahan–Ramond–Warner; Geng–Marshak) — where the closing constraint here is **Higgs-free structure the model already needed for the see-saw**, not an added assumption. Both the gravitational and the cubic $U(1)^3$ anomalies are identically zero on that line: consistency checks, not constraints.

**Two inputs remain and are named:** the overall charge unit (the $\alpha$ / $\sin^2\theta_W$ question, F49), and $N_c=3$ — commensurability holds for any $N_c$ (ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$), so colour supplies the *value* of the fraction, not the *fact* of quantisation.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md` | The hypercharge assignment derived up to one overall normalisation | exact |
| `findings/F279-hypercharge-constraint-attribution.md` | Independent re-derivation of the constraint system; upholds F165's conclusion and **corrects its attribution** — the closing constraint is the F47 Majorana step, not the gravitational anomaly | exact |
| `findings/F47-majorana-seesaw-higgs-free.md` | The Higgs-free Majorana step that supplies the closing row | exact |

## Falsifier

**Not stated.** The claims summary gives no observational threshold: the result is an algebraic uniqueness statement over ℚ, and its falsification is a demonstrated second solution of the constraint system, not a measurement. That is arguably a `none` with a structural reason, but the structure has not been argued in the finding, so it is recorded as `unset` (debt) rather than upgraded here. See `docs/audits/consolidation-plan-2026-08-04.md`.

## Status & history

`live` since **revision 3 (2026-08-02)**. This claim's history is the reason the claims layer exists. Revision 2 listed charge quantisation under **Scope — what is not claimed**, calling it an input. That was **wrong**, and understated a result the tree already had (F165, 2026-06-29). F279 adjudicated the contradiction, upheld F165 and re-attributed the closing constraint. Revision 3 moved it from Scope to core claim 10. **A prose document could only record that correction as a blockquote; this card records it as a status.**

## Sources

- `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md`
- `findings/F279-hypercharge-constraint-attribution.md`
- `findings/F47-majorana-seesaw-higgs-free.md`
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 10 and the revision-3 note
