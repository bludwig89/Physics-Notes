---
id: CL299
title: 'A Jacobson/Cai-Kim Clausius-relation argument at the flat-FRW apparent horizon reproduces the model''''s own exact Friedmann pair from local horizon thermodynamics, without positing the covariant Einstein field equation -- though the step making it exact is a convention (bracketed -3(1+w)/4, not small) rather than a controlled approximation'
slug: horizon-thermodynamics-reproduces-frw-friedmann
tier: supporting
kind: derivation
status: open
domain: [GR, cosmology]
exactness: exact
findings: [F360, F182, F188, F284, F178, F180, F79, F190, F355]
tests: [F360-horizon-thermodynamics-frw]
modules: [casim.engine.interactions.cosmology_horizon_thermodynamics]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-03'
last_verified: '2026-09-03'
provenance: authored
review_state: authored
confidence: low
---

# CL299 — A Jacobson/Cai-Kim Clausius-relation argument at the flat-FRW apparent horizon reproduces the model's own exact Friedmann pair from local horizon thermodynamics, without positing the covariant Einstein field equation

## Statement

Applying the Clausius relation $\delta Q=T\,dS$ at the flat-FRW apparent horizon $\tilde r_A=1/H$ -- with temperature set by the model's own light cone ($c_\text{grav}=c_\text{lat}$, F180) and entropy $S=A/4G$ built from the model's own induced $G$ (F79) -- reproduces $\dot H=-4\pi G(\rho+p)$ and, on integration via continuity, $H^2=(8\pi G/3)\rho$: F182/F188's own Friedmann pair, exactly, without ever writing down or solving $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ (F178). The "quasi-static" surface-gravity step this needs is itself shown, in closed form, to drop a term of ratio $-3(1+w)/4$ relative to the kept one -- $O(1)$ for radiation and matter, not small -- so the derivation's exactness rests on a specific convention, not a controlled expansion.

## What it extends

Standard FRW cosmology derives the Friedmann equations by solving the (posited) Einstein field equation with a given stress-energy tensor. This claim asserts an independent derivation route to the *same* equations from horizon thermodynamics (Jacobson 1995; Cai & Kim 2005) -- a recognised alternative foundation for GR's dynamics in the literature, applied here using this model's own structural inputs ($c_\text{lat}$, induced $G$) in place of externally supplied ones.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F360-horizon-thermodynamics-frw.md` | Sympy-exact match of the quasi-static Clausius-relation derivation to F182/F188's Friedmann pair (check Q1); closed-form, exact quantification that the dropped term is $-3(1+w)/4$, not small (check Q2) | `exact` |
| `findings/F182-friedmann-pressure-cosmology.md`, `findings/F188-multicomponent-lcdm-cosmology.md` | The Friedmann pair this reproduces, via the (different, field-equation) route already in the tree | `exact` / `machine` |
| `findings/F284-rigid-lattice-expansion-and-primordial-state.md` | Confirms (its own §7) that F182/F188's numbers are unchanged and that the ontological reading there is a different question from the dynamical-derivation one this card addresses | `structural` |
| `findings/F79-structural-newton-constant.md`, `findings/F180-gravitational-wave-speed.md` | The model's own induced $G$ and light-cone identity $c_\text{grav}=c_\text{lat}$ used as this derivation's ingredients | `exact` |
| `findings/F190-horizon-entropy-lattice-microstates.md`, `findings/F355-horizon-entanglement-vs-2pi-root3.md` | The $S=A/4G$ coefficient this derivation's *numeric* content depends on is not independently pinned by the lattice, and the model's own two attempts to compute it disagree by a bracketed factor $[0.79,3.18]$ | `bracketed` |

## Falsifier

A correct, sign-verified reconstruction of the fully exact ("unified first law", Misner-Sharp + work-term) treatment that reproduces Friedmann II with the *opposite* sign or a materially different coefficient from the quasi-static result reported here would falsify the specific claim that the quasi-static convention used is a legitimate route to F182/F188's equations (as opposed to an artifact of a sign choice) -- this finding's own §6.4 reports an unresolved attempt at exactly this reconstruction and flags it as open, not closed either way. Independently: any resolution of F355's entropy-coefficient tension that makes $S=A/4G$'s lattice-native value differ from what F79 requires by more than an $O(1)$ factor would mean this route's *numeric* content (though not its *form*) fails for this specific model.

## Status & history

`status: open` because (1) the claim's numeric content (the value of $G$ entering $S=A/4G$) rests on the still-unresolved F355 vs F79 tension, named explicitly and not resolved by this card or its finding; (2) the fully exact (no quasi-static step) version of the argument was attempted and did not close with confidence (F360 §6.4); (3) confidence is set `low` to reflect both of these open dependencies -- this is a genuine, sympy-verified alternate derivation route (the `exact` tag applies to the specific sympy identities in F360, checks Q1-Q2), but the claim that it constitutes a *complete, lattice-native* replacement for "solve GR with the source" is explicitly not made (see F360 §6-7, which holds rubric row K1 at `QUANT`).

## Sources

- `findings/F360-horizon-thermodynamics-frw.md`
- `tests/registry/interactions.yaml` id `F360-horizon-thermodynamics-frw`
- `test-results/F360_horizon_thermodynamics.json`
- Jacobson, T. (1995). "Thermodynamics of Spacetime: The Einstein Equation of State." *Phys. Rev. Lett.* **75**, 1260.
- Cai, R.-G. & Kim, S. P. (2005). "First Law of Thermodynamics and Friedmann Equations of Friedmann-Robertson-Walker Universe." *JHEP* **0502**, 050 [hep-th/0501055].
