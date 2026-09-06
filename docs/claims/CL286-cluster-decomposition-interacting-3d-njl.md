---
id: CL286
title: The interacting, 3-D BCC Dirac theory obeys cluster decomposition — an NJL-generated dynamical mass gives an exponentially decaying (100)-axis correlator matching a genuine 3-D closed-form pole rate
slug: cluster-decomposition-interacting-3d-njl
tier: headline
kind: derivation
status: live
domain: [QFT]
exactness: quantitative
findings: [F331, F290, F267, F77]
tests: [F331-cluster-interacting-3d]
modules: [casim.engine.interactions.qi_cluster_interacting_3d]
constants: [c_lat]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-27'
last_verified: '2026-08-27'
provenance: authored
review_state: authored
confidence: medium
---

# CL286 — Cluster decomposition, interacting 3-D BCC theory

## Statement

The free massive BCC Dirac field's equal-time (100)-axis correlator decays as
$e^{-\kappa_{100}(m) r}$ with $\kappa_{100}(m)=\sqrt3\,\operatorname{arccosh}(1/\sqrt{1-m^2})$, an
exact closed form derived from a genuine 3-D extremisation of the dispersion's complex-momentum
pole (not a 1-D slice). Validated against the model's own `bcc_dirac_dispersion` using the correct
BCC reciprocal lattice (F267), to a residual that shrinks monotonically with mass (best measured $pprox5\%$ at $m=0.95$, worst $pprox53\%$ at $m=0.05$; not machine precision at any mass or window tested). Separately, a lattice-native self-consistent NJL gap
equation, regulated by the model's own finite Brillouin zone, dynamically generates a mass
$m^*>0$ from a bare-massless starting point for couplings $g\in(g_c,\pi)$ ($g_c\approx2.637$
measured, $\pi$ exact); evaluating the same closed form at $m^*$ and measuring it numerically
confirms cluster decomposition holds in this interacting (mean-field) 3-D theory.

## What it extends

Extends the cluster decomposition principle — a standard QFT locality axiom, and the specific
result F290 already proved exactly for no-signalling and the free-field causal cone but left
open (its own named residual) for the interacting, 3-D case — from F290's 1-D free-fermion
demonstration to a genuine 3-D, interacting (NJL mean-field) one.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F331-cluster-decomposition-interacting-3d.md` | Exact 3-D closed-form $\kappa_{100}(m)$, $\kappa_{110}(m)$; numerical validation against the model's own dispersion on the correct BZ; lattice-native NJL gap equation; interacting-theory clustering at $m^*$ | quantitative (residual quoted, shrinks with window; not machine) |
| `findings/F290-cluster-decomposition-strict-cone.md` | The 1-D free-fermion precedent this extends; no-signalling and the causal cone, both exact, untouched by this card | exact / machine (those two legs only) |
| `findings/F267-walk-bz-measure-not-the-fft-cube.md` | The correct-BZ sampling method (`WALK_RECIPROCAL_GENERATORS`) this claim's numerics depend on | exact (the generators); the observable-dependence question F267 itself leaves open is resolved *for this observable* by F331 (a real-space transform needs the true domain, not the cube — demonstrated, not assumed) |
| `findings/F77-njl-gap-rpa-selfconsistent.md` | The continuum NJL gap-equation form this reuses, lattice-natively regulated here | quantitative (F77's own scope) |
| `test-results/F331_cluster_interacting_3d.json` | Registry record numbers, both controls verified red-and-only-there | — |

## Falsifier

A more careful multi-dimensional saddle-point analysis finding a genuinely dominant complex
singularity elsewhere in the Brillouin zone, giving a smaller decay rate than $\kappa_{100}(m)$,
would falsify the closed form as the true asymptotic rate (the bilinear-corner extremisation in
F331 §1 is independently checkable in sympy). If the measured/exact ratio failed to converge
toward 1 with increasing fit-window depth and lattice size — i.e. were a real deviation rather
than an ordinary lattice correction — that would falsify the closed form's validity as stated.

## Status & history

Newly issued, 2026-08-27, closing F290's own "what remains" item 1 (completeness row A10,
`docs/status/completeness-2026-08-20.md`). `status: live`: rests on F331 (new), F290, F267, F77,
none superseded. Explicitly does not extend to F290's item 2 (the 1-D exponent shortfall) or to
$S$-matrix-level cluster decomposition — both remain open, as stated in F331 §"What remains."

## Sources

- `findings/F331-cluster-decomposition-interacting-3d.md`
- `findings/F290-cluster-decomposition-strict-cone.md`
- `findings/F267-walk-bz-measure-not-the-fft-cube.md`
- `findings/F77-njl-gap-rpa-selfconsistent.md`
- `docs/status/completeness-2026-08-20.md` row A10
