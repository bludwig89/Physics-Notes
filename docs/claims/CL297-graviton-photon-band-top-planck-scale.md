---
id: CL297
title: 'The paired photon/graviton dispersion law is bounded above by pi radians per CA tick exactly, giving a computed, zero-free-parameter maximum propagating energy of 0.8247 E_Planck -- a kinematic UV-completion number for rubric row E12, distinct from A11/K9''s rho_vac EFT-coefficient residual'
slug: graviton-photon-band-top-planck-scale
tier: supporting
kind: derivation
status: live
domain: [GR, QFT]
exactness: exact
findings: [F357, F248, F69, F79, F352]
tests: [F357-graviton-band-top]
modules: [casim.engine.interactions.gravity_band_cutoff]
constants: [a_over_ellP, c_lat]
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

# CL297 — The photon/graviton band top is exactly pi, and it sits at 0.8247 Planck energies

## Statement

The model's photon/graviton "even" paired dispersion law $\Omega_\text{even}(\mathbf K)=\omega_+(\mathbf K/2)+\omega_-(\mathbf K/2)$ (F69, F248) is bounded above by $\pi$ radians per CA tick **exactly**, throughout the BCC Brillouin zone, with equality attained on the whole zone boundary. Converted to physical units through F79/F107's registered structural ruler $a/\ell_P$ (zero new free parameters), the maximum propagating photon/graviton energy is $E_\text{max}=\sqrt{\pi\sqrt3/8}\,E_\text{Planck}=0.824727\,E_\text{Planck}$, and it relates to the model's existing cruder cutoff estimate (F352's $\Lambda_\text{model}=E_\text{Planck}/(a/\ell_P)$) by the exact closed form $E_\text{max}=\pi\sqrt3\,\Lambda_\text{model}$.

## What it extends

**Rubric row E12 (quantum-gravity sector)**, which read "Graviton massless, 2 dof; UV completion beyond 'lattice is the cutoff' undeveloped" — this replaces the qualitative slogan with a computed, closed-form energy ceiling. Against the standard EFT-of-gravity literature (e.g. Donoghue, gr-qc/9512024), continuum quantized GR is understood to require new UV physics near $E\sim M_\text{Planck}$ (graviton-graviton scattering unitarity violation, cited here for scale only — no numeric coefficient is imported); this claim shows the model's own lattice cutoff for the propagating photon/graviton line sits at exactly this parametric scale ($O(1)\times E_\text{Planck}$, not off by orders in either direction), supplied structurally by the same pairing law (F69) that already forces non-birefringence, with no additional input.

**This claim explicitly does not extend, narrow, or touch rubric row A11 or K9** (the $\rho_\text{vac}$ EFT-operator-coefficient residual, ledger row G1). A11/K9 are a Wilsonian operator-coefficient-matching question; this claim is a single-particle kinematic bound on the propagating dispersion relation. See F357 §1 for the explicit scoping argument.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F357-graviton-photon-band-top-uv-scale.md` | the theorem, the closed form, the F352 relation, the honest scope limit | — |
| A | $\arccos(a)+\arccos(b)\le\pi\iff a+b\ge0$ (exact trig identity + strict monotonicity, sympy) | exact |
| B | domain fact $c_i\ge0$ on $\theta_i\in[-\pi/2,\pi/2]$ | exact by construction |
| C | dense $161^3$ zone sweep confirms $\max\Omega_\text{even}=\pi$ | lattice-numeric, $5\times10^{-13}$ |
| D | boundary saturation $u_++u_-=0$ identically, sympy | exact |
| E | $E_\text{max}/E_\text{Planck}=\sqrt{\pi\sqrt3/8}=0.824727$, symbolic vs. registered `a_over_ellP` | exact-algebraic, $<10^{-9}$ |
| F | $E_\text{max}=\pi\sqrt3\,\Lambda_\text{model}$ | exact-algebraic, $<5\times10^{-13}$ |
| control | the un-paired doubled law $2\omega_+(\mathbf K/2)$ measures exactly $2\pi$, $1.6495$, $2\pi\sqrt3$ — double in every case | exact |
| `test-results/F357_graviton_band_cutoff.json` | 6/6 PASS | — |

## Falsifier

1. **The computable one.** A demonstration that F248's paired "even" law is not in fact the model's physical photon/graviton dispersion (i.e. that F69's pairing argument is wrong) would remove the domain restriction this bound relies on and reopen the question. F357's own control shows exactly what changes if the wrong (un-paired) law is used: the ceiling doubles to $2\pi$.
2. **A revision of F79/F107's structural ruler** $a/\ell_P$ (e.g. from a future correction to $\eta_\text{Weyl}$, $g_*$, or the loop-channel argument) would move $E_\text{max}/E_\text{Planck}$ with it — this claim inherits F79's own falsifiers rather than adding new ones, since it introduces no independent length scale.
3. **This claim is not falsified by, and does not bear on, any future resolution of K9/A11.** A change to $\rho_\text{vac}$'s matching is a different EFT-operator-coefficient question; nothing in this claim's derivation reads $\rho_\text{vac}$, $T^{\mu\nu}$, or any cosmological quantity.

## Status & history

`live`, issued 2026-09-03, sharpening rubric row **E12** with a computed number in place of the qualitative "lattice is the cutoff" note. Explicitly scoped away from A11/K9 (open concurrent sessions `lucid-candid-wheeler` and `careful-lucid-lemaitre` respectively, per `docs/design/session-claims.yaml`) rather than duplicating that work — see F357 §1.

**Scope boundary, stated plainly (not a narrowing, an as-issued limit):** this is a **kinematic** result (a bound on a single propagating line's energy), not a **dynamical** one (a graviton-graviton scattering amplitude or a partial-wave unitarity calculation). It answers "can a super-Planckian photon/graviton mode exist on this lattice at all" (no) but not "what happens dynamically as two near-band-top gravitons collide" — that calculation is not attempted here and would be the natural next step if E12 is to close further in the "self-interaction/scattering" sense the completeness-report prompt names.

## Sources

- `findings/F357-graviton-photon-band-top-uv-scale.md`
- `findings/F248-tt-graviton-bcc-explicit.md` (the parent — builds the paired "even" law)
- `findings/F69-paired-spinor-photon.md` (why the law is a pair sum, not a single branch)
- `findings/F79-structural-newton-constant.md` §5 (the ruler $a/\ell_P$, $a/\tau=c\sqrt3$)
- `findings/F352-higgs-bhl-compositeness-rg-negative.md` (the cruder $\Lambda_\text{model}$ this relates to)
- Donoghue, "General Relativity as an Effective Field Theory: The Leading Quantum Corrections", gr-qc/9512024 — cited for the standard parametric ($\sim M_\text{Planck}$) scale of continuum graviton-scattering unitarity violation, no coefficient imported
- `docs/design/session-claims.yaml`, session `quiet-precise-regge` — the collision-avoidance record against the open K9/A11 sessions
