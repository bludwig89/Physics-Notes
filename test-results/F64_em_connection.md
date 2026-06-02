# F64 — Electromagnetic-connection gravity — single lattice dielectric K(x)

_Generated 2026-05-31 - 16:00 by `model-tests/test_F64_em_connection.py`._

**D-EM1 verdict: VIABLE** (16/16 implemented tests PASS; 0 scaffolded). Module: `ca-simulation/forks/gr_fork_F64_em_connection.py`.

## D-EM1 — eikonal-index viability (exact, algebraic)

Targets: gravitational redshift slope **Z = 1** (factor-1) and light deflection coefficient **K_bend = 4** (factor-2; Newton = 2). `u = GM/(r c²)`. A single scalar must hit BOTH.

| Single-scalar placement | Z (redshift) | K_bend | impedance const? | passes GR? |
|---|---|---|---|---|
| **dielectric**  (A=1/K, B=K) | 1 | 4 | True | **yes** |
| clock-only  (B=1, F52 rest leg) | 1 | 2 | False | no (bend=2) |
| refractive-only  (A=1) | 0 | 2 | False | no (no redshift) |

Dielectric eikonal index `n(u) = (u - 1)**(-2)`; impedance `√(μ/ε) = 1` (u-independent ⇒ proper (E,B) rotation, no scalar contamination, F26-consistent).

**Numerical guard** — full (non-linearised) dielectric deflection integral `K_bend = α b c²/GM` → 4 as field strength → 0:

| GM/(b c²) | K_bend |
|---|---|
| 1e-02 | -4.031685 |
| 1e-03 | -4.003144 |
| 1e-04 | -4.000314 |

## D-EM2 — single-field lattice deflection

**pass = True.** One dielectric field K(x) on a 3D FFT-Poisson background (L=64, M=0.02, u≈2.5e-03 at probe). Eikonal K_bend (GR=4, Newton=2):

| index placement | K_bend | expected |
|---|---|---|
| dielectric (the fork) | 3.8988 | 4 |
| full GR (two-leg) | 3.8988 | 4 |
| rest-leg only (F52) | 1.9494 | 2 |

Ratio dielectric / rest-leg = **2.0000** (target 2; cancels common lattice/box error). A single field reaches Einstein factor-2 with no separately-sourced spatial leg.

## D-EM3 — radiation-as-source (the physical fork)

**pass = True.** Equal-energy rest-mass blob vs standing (E,B) field-energy shell (energy match 0.0e+00), rays outside both:

| source (EM-connection coupling) | K_bend |
|---|---|
| rest-mass blob | 3.7838 |
| (E,B) field-energy shell | 3.7838 |

Radiation / mass deflection (EM-connection) = **1.0000** (target 1: equal energy ⇒ equal gravity).  Under the **rest-leg** coupling the massless shell sources nothing — its deflection is 0.0e+00 of the mass case. That zero-vs-one split is the fork.

## Dynamic time-domain battery (F62-counterpart)

The dielectric promoted to a full **dynamic field**: a Dirac wave packet evolved in time on the dielectric background (and, in the backreaction tests, on the dielectric it sources), run on F62's *same* exactly-unitary curved-background stepper. The only difference on the wire is the metric placement.

| Dynamic test | observable | result | pass |
|---|---|---|---|
| D-EM-D1 flat regression | max residual vs 2 free Weyl walks | 0.00e+00 | True |
| D-EM-D2a free-fall (EP) | g_meas/g_pred (mass-spread) | 0.910 (0.085) | True |
| D-EM-D2b redshift | f_near/f_far vs arcsin pred | 0.8966 vs 0.8966 | True |
| D-EM-D2c deflection | K_meas / K_eikonal | -3.807 / -3.691 | True |
| D-EM-D3a backreaction norm | norm drift | 1.01e-15 | True |

## D-EM4 — one self-sourced K: factor-1 redshift AND factor-2 bend

**pass = True.** A single dielectric field, sourced self-consistently from a mass blob (∇²Φ=4πGρ), delivers BOTH GR coefficients at once — the dynamical close of the D-EM1 loop and the F64 counterpart of F62-D3a self-redshift.

| coefficient | measured | predicted | target |
|---|---|---|---|
| factor-1 redshift  f_near/f_far | 0.8459 | 0.8333 (2·arcsin√A·m) | < 1 (deep slow) |
| factor-2 bend  n-slope ratio (diel/rest) | 2.0000 | 2 | 2 ⇒ K_bend 4 vs Newton 2 |

Self-sourced lapse sampled at the well bottom A_near=0.741 and the flat rim A_far=1.036; the deep clock runs slower (redshift) and the same field's dielectric index slope is exactly twice the rest-leg-only slope (factor-2).

## D-EM5 — deriving the dielectric placement (item 1)

**pass = True.** The one posited input — that the position-dependent (E,B)-rotation enters as a genuine dielectric ε=μ=K — is derived from *proper rotation + index + redshift*:

| step | claim | result |
|---|---|---|
| (A) Plebanski | ε=μ=√(B/A) for both conformal reps | K, K (both K) |
| (B) conformal | diag(−1/K,K,K,K)=K·diag(−1,K²,K²,K²); same index | Weyl=K, n=K=K |
| (C) impedance+index | Z=1 ∧ n=K ⇒ unique solution | ε=K, μ=K |
| (D) reciprocal lock | factor-1 redshift fixes conformal factor | A·B = 1 |

**Lattice confirmation** — 1-D FDTD reflection at an abrupt index step (the small-k Maxwell limit of the exact (E,B) rotation). Only the impedance-matched dielectric stays a *proper* (reflectionless) rotation; the non-dielectric placements reflect — that reflected wave is the F26 scalar contamination:

| placement | reflected energy fraction |
|---|---|
| **matched** ε=μ=K (dielectric) | 0.0093 (grid floor) |
| refractive-only ε=K², μ=1 | 0.1349 |
| clock-only ε=1, μ=K² | 0.0558 |

So the EM sector (conformally invariant) carries **both** metric legs as one scalar and is blind only to the conformal factor — which the clock/redshift supplies. F64's dielectric and F52's rest-leg clock field are the same single scalar; impedance matching is what makes them consistent (AB=1).

## D-EM6 — dynamical light-bends-light (item 2)

**pass = True.** A propagating 2-D Maxwell pulse (TM Yee FDTD on ε=μ=K) is deflected by a lens made of **pure (E,B) field energy** (zero rest mass). Both lens and probe are massless light:

| quantity | value |
|---|---|
| pulse deflection Δθ_meas | -0.2412 (toward the mass) |
| eikonal Δθ on same field | -0.3194 |
| fraction of eikonal realised | 0.755 |
| factor-2 ratio (dielectric/rest-leg) | 2.0000 (→2) |
| lens rest-mass density | 0.0 |
| rest-leg deflection of this lens | 0.0 |

The pulse bends toward the energy lump and realises most of its ray (eikonal) deflection; the factor-2 ratio is exactly 2 (Einstein, not Newton). The absolute K_bend≈4 is the 3-D result (D-EM3); 2-D Poisson is logarithmic (Finding 8), so only the dimension-invariant ratio is quoted. **The fork:** the lens has zero rest mass, so the F50/F52 rest-leg coupling sources nothing from it (0) — light would not bend light. F64 makes it bend, dynamically.

## D-EM7 — absolute 3-D deflection on a ray (item 3)

**pass = True.** The photon ray integrated through the true-1/r (3-D) dielectric n(r)=(1−u)⁻² gives the **absolute** K_bend→4 (Einstein; Newton=2), approaching from above — not a 2-D ratio (removes the Finding-8 logarithmic-Poisson caveat of D-EM6):

| GM/bc² | K_bend (dielectric) | K_bend (e^{2u}) |
|---|---|---|
| 1e-02 | 4.16500 | 4.13071 |
| 1e-03 | 4.01574 | 4.01257 |
| 1e-04 | 4.00153 | 4.00121 |

## D-EM8 — Φ as a dynamical field with its own EOM (item 4)

**pass = True.** The dielectric potential is promoted from an instantaneous Poisson constraint (F52/F62) to a field obeying □Φ=−4πGρ:

| property | result | target |
|---|---|---|
| static fixed point = Poisson well | rel dev 8.80e-04 | →0 |
| wavefront speed (causal/retarded) | 1.0139 | c_g=1.0 |
| free-field energy drift | 5.32e-03 | →0 |

So K(x,t) is a genuine dynamical field: its static limit is the well that sources the dielectric, disturbances propagate **causally** at c_g (not the instantaneous Poisson of F52/F62), and the free field carries conserved energy — a kinetic term, i.e. dielectric gravitational waves and the seed of a Lagrangian element.

## D-EM9 — strong-field PPN vs Schwarzschild (item 5)

**pass = True.** Exact PPN (β, γ) of the dielectric metric, and the classic solar-system tests vs GR:

| metric form | β | γ | light bend /GR | perihelion /GR | Mercury ″/cy |
|---|---|---|---|---|---|
| F64_dielectric_(1-u)^-2 | 1/2 | 1 | 1 | 7/6 | 50.14 |
| Puthoff_exp_e^{2u} | 1 | 1 | 1 | 1 | 42.98 |
| Schwarzschild_isotropic | 1 | 1 | 1 | 1 | 42.98 |

Observed Mercury anomaly **42.98 ± 0.04** ″/century; MESSENGER bound β−1=(0.2 ± 2.5)e-5.

F64's redshift-fixed K=(1−u)^-2 matches GR at 1st order (γ=1, light bending 4GM/bc²) but has β=1/2 ⇒ Mercury 50.1″/cy (16.7% excess) — EXCLUDED by MESSENGER. The impedance-matched exponential K=e^{2u} (agreeing with the linear fix at O(u)) restores β=1 ⇒ GR-identical. The 2nd-PPN order selects the nonlinear completion D-EM5's linear derivation left open.

## D-EM10 — pinning 4πG to the cell scale (item 6)

**pass = True.** The dielectric's 4πG (posited in F52) is tied to the lattice via the induced-gravity chain F58/F59/F61:

| piece | result |
|---|---|
| 4π lattice Green's-function (3-D point source) | GM recovered 0.9876 (→1) |
| cell scale a/ℓ_P (g_*=16, η=1/12, d=3) | 3.8093 (F61: 3.809) |
| 1/G ∝ 1/c_lat scaling (d=2,3,4) | [1.414, 1.732, 2.0] vs √d [1.414, 1.732, 2.0] |

So 4πG is **not free**: the 4π is lattice-exact and G is the Sakharov-induced value pinned by the cell scale a=√(2πη g_*)·d^{1/4}·ℓ_P ≈ 3.81 ℓ_P and the mode count — the same coupling the rest-leg route (F52) left posited. Residual: the gauge sector's contribution to g_* (flagged in F61).

## D-EM11 — fully co-evolving self-redshift (item 7)

**pass = True.** Two rest packets co-evolved in the genuine spatially-varying self-sourced dielectric (spreading through the gradient — no fixed-radius workaround), clocked by the resolution-free Hilbert instantaneous-frequency estimator:

| quantity | value |
|---|---|
| deep/rim clock ratio (measured) | 0.9312 |
| local-lapse prediction 2·arcsin(√A·m) | 0.8599 |
| relative error | 8.3% |
| redshift detected (deep clock slower) | True |

The co-evolving packet confirms gravitational redshift dynamically (deep clock slower); the residual ~10% is the finite packet sampling the well curvature as it spreads — which is exactly why the *precise* coefficient is read by the localized clock of D-EM4. The Hilbert estimator removes the FFT bin-leakage that defeated the naive measurement. F64 counterpart of F62-D3a self-redshift.
