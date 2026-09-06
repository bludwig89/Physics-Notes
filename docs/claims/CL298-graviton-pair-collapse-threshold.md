---
id: CL298
title: 'Two of the model''s own maximum-energy photons/gravitons collide head-on with exactly sqrt(pi) times the rest-mass energy of the model''s own minimal Planck-mass black-hole remnant -- an exact kinematic THRESHOLD on the necessary energetic precondition of self-completeness via classicalization (not the geometric hoop criterion itself, and not a scattering-amplitude computation) -- narrower than E12''s still-open dynamical residual (F357 sec.7)'
slug: graviton-pair-collapse-threshold
tier: supporting
kind: derivation
status: live
domain: [GR, QFT]
exactness: exact
findings: [F359, F357, F228, F223, F79, F107]
tests: [F359-graviton-collapse-threshold]
modules: [casim.engine.interactions.graviton_collapse_threshold]
constants: [a_over_ellP]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-03'
last_verified: '2026-09-03'
provenance: authored
review_state: authored
confidence: medium
---

# CL298 — A head-on collision of two band-top quanta clears an exact energetic threshold, sqrt(pi) above the model's own minimal black hole (a necessary precondition, not the dynamical calculation itself)

## Statement

Write $A\equiv a_\text{over\_ellP}=\sqrt{8\pi}\,3^{1/4}$ (registered, F79/F107). F357's single-particle energy ceiling $E_\text{max}/E_\text{Planck}=\pi\sqrt3/A$ and F228's one-cell Planck-mass black-hole remnant mass, re-derived here from the same ruler as $M_\text{rem}/M_\text{Pl}=A/(4\sqrt\pi)$ (symbolically identical to F228's own published closed form $3^{1/4}/\sqrt2$), combine to give, with $A$ cancelling completely,

$$\frac{\sqrt{s_\text{max}}}{M_\text{rem}c^2}=\frac{2E_\text{max}}{M_\text{rem}c^2}=\sqrt\pi\approx1.77245\qquad\text{(exact, closed form)},$$

the CM energy of two head-on band-top quanta colliding. A single quantum alone gives $E_\text{max}/M_\text{rem}c^2=\sqrt\pi/2\approx0.886$ — sub-threshold. Both ratios are exact-algebraic and independent of the numeric value of $A$ (it drops out of the ratio identically).

## What it extends

**Rubric row E12 (quantum-gravity sector)**, specifically the residual F357 (CL297) explicitly left open: "a graviton-graviton scattering amplitude, interaction vertex, or partial-wave unitarity bound... this finding does not compute [it]... the natural next attack if E12 is to close further." This claim does not compute that amplitude, and does not close that residual — it answers a narrower, purely kinematic question: is the naive perturbative-unitarity-violation energy regime even reachable inside this model at all? Yes, by an exact, closed-form, parameter-free margin ($\sqrt\pi$ above the model's own minimal black-hole threshold). Note precisely what this is *not*: the self-completeness/classicalization literature (Dvali & Gomez, arXiv:1005.3497; 't Hooft 1987) states a **geometric** hoop/impact-parameter criterion for black-hole formation, which this claim does not compute — what is established here is only the weaker, *necessary* energetic precondition (CM energy exceeding a rest-mass threshold) that any such geometric criterion would first require. No external coefficient is imported (unlike a direct import of a continuum EFT partial-wave bound would require), but the geometric criterion itself is not reproduced.

**This claim explicitly does not compute a scattering amplitude, a black-hole-formation cross-section, or a partial-wave unitarity bound.** It is a relativistic two-body CM-energy threshold comparison only. It does not touch A11 or K9's $\rho_\text{vac}$ residual (no cosmology or EFT-operator-counting file is read).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F359-graviton-collapse-threshold.md` | the theorem, the closed forms, the honest scope limit | — |
| A | $A^2=8\pi\sqrt3$ (F79/F107's canonical-cell identity, reused), sympy + numeric vs. live registry | exact-algebraic, $<10^{-9}$ |
| B | $M_\text{rem}/M_\text{Pl}=A/(4\sqrt\pi)$ symbolically $=3^{1/4}/\sqrt2$ (F228's own closed form); numeric match to F228's published $0.93060$ | exact-algebraic, $<5\times10^{-5}$ |
| C | $\sqrt{s_\text{max}}/M_\text{rem}c^2=\sqrt\pi$, sympy symbolic simplification, $A$ cancels | exact-algebraic |
| D | $E_\text{max}/M_\text{rem}c^2=\sqrt\pi/2$, sympy symbolic simplification | exact-algebraic |
| E | vs. F223's $\mu_\text{geon}=\sqrt2\,M_\text{Pl}$: $E_\text{max}/\mu\approx0.583$, $\sqrt{s_\text{max}}/\mu\approx1.166$ — same direction, F223's own weaker tier | order-of-magnitude |
| control | `pairing_law="chiral_double"` reddens C, D, E exactly (measured $2\sqrt\pi$, $\sqrt\pi$ in place of $\sqrt\pi$, $\sqrt\pi/2$) | exact |
| `test-results/F359_graviton_collapse_threshold.json` | 5/5 PASS, control verified live | — |

## Falsifier

1. **The computable one.** A demonstration that F357's paired "even" dispersion law is not the model's physical photon/graviton law (i.e. F69's pairing argument is wrong) removes the $E_\text{max}$ this claim is built on and reopens the question — F359's own control shows exactly what changes if the wrong law is used: both ratios exactly double.
2. **A revision of F228's one-cell remnant derivation** (e.g. a correction to F190's $S=A/4$ per-cell entropy, currently itself flagged "open" for its own microstate count, or to F107's canonical cell) would move $M_\text{rem}/M_\text{Pl}$ and hence this ratio with it — this claim inherits F228's own falsifiers rather than adding new ones.
3. **Scope note, not a falsifier.** This claim is not a scattering-amplitude or partial-wave computation and is not falsified by, nor does it pre-empt, any future direct computation of one; a future dynamical result could show a *different*, smaller or larger, effective collapse cross-section without contradicting this purely kinematic threshold statement.

## Status & history

`live`, issued 2026-09-03, addressing the dynamical residual rubric row **E12**'s F357/CL297 explicitly left open. Session `e12-graviton-collapse-threshold` (`docs/design/session-claims.yaml`) opened after checking F357/CL297 and confirming the topic was not duplicated by any open session.

**Scope boundary, stated plainly (an as-issued limit, not a narrowing):** this is a **kinematic threshold** result (a CM-energy comparison against an independently-derived rest-mass threshold), not a **dynamical** one (no scattering amplitude, cross-section, or partial-wave unitarity bound is computed). It answers "is the collapse-threshold energy regime reachable, and exceeded, at this model's own cutoff" (yes, by $\sqrt\pi$) but not "what does the collision dynamically produce, at what rate, or with what cross-section" — that calculation remains open.

## Sources

- `findings/F359-graviton-collapse-threshold.md`
- `findings/F357-graviton-photon-band-top-uv-scale.md` (the parent — $E_\text{max}$ and the residual this claim addresses)
- `findings/F228-geon-production-and-stability.md` (the parent — $M_\text{rem}$, exact-algebraic)
- `findings/F223-spin2-bound-state-binding-and-relic.md` (the order-of-magnitude cross-check, $\mu_\text{geon}$)
- `findings/F79-structural-newton-constant.md`, `findings/F107-canonical-a-adoption-L4-grb-gate.md` (the shared registered ruler $a_\text{over\_ellP}$)
- Dvali & Gomez, "Self-Completeness of Einstein Gravity", arXiv:1005.3497 — the classicalization argument this claim's kinematic precondition matches
- 't Hooft, *Phys. Lett. B* 198 (1987) 61 — trans-Planckian gravitational scattering
- `docs/design/session-claims.yaml`, session `e12-graviton-collapse-threshold`
