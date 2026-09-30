---
id: CL286
title: The interacting, 3-D BCC Dirac theory obeys cluster decomposition — an NJL-generated dynamical mass gives an exponentially decaying (100)-axis correlator matching a genuine 3-D closed-form pole rate
slug: cluster-decomposition-interacting-3d-njl
tier: headline
kind: derivation
status: live
domain: [QFT]
exactness: quantitative
findings: [F331, F290, F267, F77, F380]
tests: [F331-cluster-interacting-3d, F380-cluster-asymptotic-series-K]
modules: [casim.engine.interactions.qi_cluster_interacting_3d, casim.engine.interactions.qi_cluster_asymptotic_series]
constants: [c_lat]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-27'
last_verified: '2026-09-10'
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

F380 (2026-09-10, mechanism corrected same day by its own review-finding pass) named the residual:
the measured/exact ratio's mass-dependence (F331's table) is the finite-window fit bias of a
*plain*-exponential fit against a function that carries an algebraic $r^{-3/2}$ prefactor — $r^{-1}$
from 2-transverse-dimension stationary phase around the dominant saddle, **plus** an extra $r^{-1/2}$
from an axial *branch point* in the dispersion $\omega=\arccos(n\,u)$ (which vanishes as $\sqrt{\cdot}$
at the pole, not linearly — this is *not* the continuum Yukawa propagator's simple-pole case).
Re-expressed via the exact OLS regression-bias formula as an implied power
$p_\text{eff}=(\kappa_\text{measured}-\kappa_{100})/(S_{r,\ln r}/S_{rr})$, the residual is
mass-independent to $2.65\%$ ($p_\text{eff}=1.489\pm0.039$) across the whole admissible range
$0.05\le m\le0.90$ — matching the independently-derived theoretical power $3/2$ to $<1\%$ — and
*including* at the dynamically NJL-selected $m^*$ ($p_\text{eff}(m^*)$ at $z=-0.62\sigma$ from the
scan mean) — one named, theoretically-anchored object, not a per-mass tolerance table.

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
| `findings/F380-cluster-asymptotic-series-residual-named.md` | Names F331's residual as one theoretically-anchored object $p_\text{eff}=1.489\pm0.039$ (2.65% relative spread, matching the derived $p=3/2$ to <1%), measured mass-independent across the whole admissible range including $m^*$; control (wrong-axis reference) verified red; reviewed and its original ($p=1$) mechanism corrected same day | quantitative ($p_\text{eff}$ measured against a derived target, not yet closed-form to the numerical floor) |
| `test-results/F380_cluster_asymptotic_series.json` | Registry record numbers, control verified red-and-only-there | — |

## Falsifier

A more careful multi-dimensional saddle-point analysis finding a genuinely dominant complex
singularity elsewhere in the Brillouin zone, giving a smaller decay rate than $\kappa_{100}(m)$,
would falsify the closed form as the true asymptotic rate (the bilinear-corner extremisation in
F331 §1 is independently checkable in sympy). If the measured/exact ratio failed to converge
toward 1 with increasing fit-window depth and lattice size — i.e. were a real deviation rather
than an ordinary lattice correction — that would falsify the closed form's validity as stated.
F380 checked exactly this at $m^*$ (L-converged from $L=128$ to $512$ at ratio $1.1096$, stable)
and found the residual does *not* vanish with $L$ at fixed $m$ — but showed this is expected: it
is the known algebraic-prefactor bias of a plain-exponential fit, not a deviation of the closed
form itself, evidenced by $p_\text{eff}$'s $2.65\%$ mass-independence and its $<1\%$ match to the
independently-derived theoretical power $3/2$. A future full symbolic derivation of the sub-leading
term disagreeing with the measured $p_\text{eff}=1.489\pm0.039$ band would reopen this falsifier.

## Status & history

Newly issued, 2026-08-27, closing F290's own "what remains" item 1 (completeness row A10,
`docs/status/completeness-2026-08-20.md`). `status: live`: rests on F331 (new), F290, F267, F77,
none superseded. Explicitly does not extend to F290's item 2 (the 1-D exponent shortfall) or to
$S$-matrix-level cluster decomposition — both remain open, as stated in F331 §"What remains."

**2026-09-10** — F380 names F331's mass-dependent residual as one theoretically-anchored object
($p_\text{eff}=1.489\pm0.039$, matching the derived power $3/2$ to <1%, not yet closed-form to the
numerical floor); row A10 promoted QUANT→PARTIAL. F380's own review-finding pass (same day) caught
and corrected a wrong initial mechanism ($p=1$, "same as Yukawa") — see F380's "Reviewed &
corrected." Does not change this card's exactness class (still `quantitative`) or falsifier;
`status: live` unchanged.

## Sources

- `findings/F331-cluster-decomposition-interacting-3d.md`
- `findings/F290-cluster-decomposition-strict-cone.md`
- `findings/F267-walk-bz-measure-not-the-fft-cube.md`
- `findings/F77-njl-gap-rpa-selfconsistent.md`
- `findings/F380-cluster-asymptotic-series-residual-named.md`
- `docs/status/completeness-2026-08-20.md` row A10
- `docs/status/completeness-2026-09-08.md` row A10
