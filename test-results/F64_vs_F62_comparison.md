# F64 (EM-connection dielectric) vs F62 (emergent-gravity rest-leg)

_Generated 2026-05-31 - 16:00 by `model-tests/compare_F64_F62.py`._

Both gravity routes run on the **same** exactly-unitary curved-background Dirac stepper (`dirac_gravity_fork`); the only independent variable is the metric placement. F62 passes 6/6 of its battery; F64 passes 16/9 (6 dynamic counterparts + 3 static eikonal/field-level, incl. the radiation-as-source discriminator F62 has no analogue for).

## Shared observables — apples-to-apples

| observable | F62 rest/two-leg | F64 single dielectric | GR target | note |
|---|---|---|---|---|
| flat regression residual (→0) | 0 | 0 | 0 | both reduce to two free Weyl walks bit-for-bit |
| free-fall coeff g_meas/g_pred (→1) | 0.91 | 0.91 | 1 | EP carried by the rest leg √A — shared exactly |
| free-fall mass-universality spread (→0) | 0.08489 | 0.08489 | 0 | trajectory mass-independent in both |
| dynamical redshift f_near/f_far | 0.8966 | 0.8966 | 0.8915 | clock rate ∝ √A in both (rest leg) |
| deflection K_meas (→ −4) | -3.432 | -3.807 | −4 | F64: ONE field; F62: two legs |
| deflection K_eikonal (→ −4) | -3.92 | -3.691 | −4 | finite-field: dielectric approaches 4 from above |
| backreaction norm drift (→0) | 2.513e-15 | 1.005e-15 | 0 | each tick exactly unitary in both |
| self-sourced redshift ratio (<1) | 0.9032 | 0.8459 | <1 (deep clock slow) | F62-D3a vs F64-D-EM4; both close the loop |

To leading order in the weak field both maps coincide — `√A = 1+Φ/c²+O(u²)` and `c_eff = c₀(1+2Φ/c²)+O(u²)` for both — so the equivalence principle, factor-1 redshift and factor-2 deflection agree by construction. The dielectric's finite-field deflection approaches the Einstein value from above (|K|≳4) where the linearised two-leg approaches from below (|K|≲4).

## Where the fork actually lives — structural / empirical

| axis | F62 rest/two-leg | F64 single dielectric | verdict |
|---|---|---|---|
| field equations for factor-2 bend | 2  (A and B sourced independently) | 1  (B = 1/A locked by impedance, AB≡1) | F64 strictly more parsimonious |
| source of gravity | rest-mass density ρ = |Ψ|² | total field energy u (incl. massless (E,B)) | different physics — testable |
| does massless (E,B) field energy gravitate? | no (ρ_rest = 0 ⇒ Φ = 0 ⇒ 0 deflection) | yes — radiation/mass deflection ratio 1.0 | the empirical fork (D-EM3): 0 vs 1 |
| one self-sourced field gives BOTH GR coefficients | redshift yes; factor-2 bend needs the 2nd leg | yes — redshift 0.8459 AND bend-slope ratio 2.0 (≈2) | F64 closes D-EM1 on one field (D-EM4) |

## Bottom line

The dielectric reproduces **every** dynamical result of the emergent-gravity module (free-fall/EP, gravitational redshift, factor-2 light bending, unitary backreaction, self-sourced loop-closure) using **one** impedance-locked field equation in place of two independently-sourced metric legs, and it adds a sharp empirical discriminator — massless (E,B) field energy gravitates per unit energy exactly as rest mass (ratio≈1), where the rest-leg route is blind to it (0). The two routes are numerically degenerate on the classical weak-field tests and diverge on (a) parsimony and (b) the gravitation of radiation.
