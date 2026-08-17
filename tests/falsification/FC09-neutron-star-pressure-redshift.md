# FC09 — Neutron-star interior: the pressure/Tolman departure from GR

**Tier:** C → **B** candidate (the first model-vs-GR discriminator, not just model-vs-SM)
**Falsification power:** ★★★★ (sharp, two-sided, confrontable with NICER/NS data; null in the solar system so it survives all classical tests by construction)
**Model element under test:** the F64/F106 single-scalar dielectric sourced by energy density, ∇²ln K = −(8πG/c⁴)T⁰⁰ — which (F173) omits GR's matter-pressure (3p) Tolman source.

## Hypothesis (parameter-free prediction)
GR sources the time potential by ρ + 3p/c²; the dielectric by ρ alone. For an equation of state p = wρc² the model **omits the fraction 3w/(1+3w)** of GR's source. Consequences:

- **Exterior:** identical to GR (M = ∫ρ, β = γ = 1) — all solar-system tests pass.
- **Interior / strong field:** the central time-dilation diverges from GR at O(s²), s = GM/Rc², with exact leading coefficient **−15/4**. Fractional departure in central √(−g_tt): **~2% at s = 0.1, ~12% at s = 0.2, ~42% at s = 0.3** (uniform-sphere illustration).

## Measured target + source
- Neutron-star **mass–radius** and **surface gravitational redshift** from NICER (PSR J0030+0451, J0740+6620) and X-ray burst / spectral-line redshift measurements. Typical NS compactness s ≈ 0.15–0.30.
- Surface redshift z_surf = (1 − 2s)^(−1/2) − 1 in GR; the model predicts a compactness-correlated offset of order 3⟨p⟩/ρc².

## Falsification criterion
Falsified if neutron-star interior observables (mass–radius curve, surface redshift vs mass, moment of inertia) match **GR's pressure-sourced structure** to better than the predicted O(3p/ρc²) ~ tens of % at NS compactness, with no compactness-correlated residual of the predicted sign. Conversely, a systematic departure of the predicted magnitude and sign would be striking support for energy-only sourcing.

## CASIM / numerical build & run
1. **Done (F173):** exact Einstein tensor of the dielectric metric → source carries ρ only + anisotropic field stress p_r = −p_t; omitted fraction 3w/(1+3w); leading divergence coefficient −15/4. `tests/findings/test_F173_tolman_pressure.py` (4/4 PASS).
2. **Done (F174):** solved both hydrostatic structures (`casim.engine.interactions.stellar`, 5/5 PASS) and overlaid on NICER. Result is **stronger than the uniform-sphere estimate**: the literal energy-only dielectric has **no maximum mass** and predicts R ≈ 19.6 km at the J0740 mass 2.08 M⊙ (NICER 12.4 ± 0.75 km) — observationally excluded in the strong-field interior unless the strong-field law is covariantized to the full G_μν = 8πG T_μν. Overlay figure: `test-results/figures/F174_stellar_overlay.png`.
3. **Done (F176):** the covariant variant was built (`solve_covariant` in `ca_stellar.py`). Result: covariantizing the field equation (exact G_tt curvature feedback) **restores the maximum-mass turnover** the literal model lacked; energy-only overshoots GR's M_max by ~41%, while adding the pressure source (ρ+3p) matches GR M_max to **0.4%**, leaving a ~2 km AB≡1 residual in the M–R relation. So the model is **not grossly excluded once covariantized** — the discriminator becomes a subtle ~km-scale M–R / redshift residual at the NICER frontier, and a theory-level choice of whether pressure gravitates. Figure: `test-results/figures/F176_covariant_overlay.png`.
4. **Open (refinement):** drop verified tabulated SLy/APR digits (Read+2009) into the provided `TwoPiecePolytrope` to quote the cov-3p residual in km against a specific pulsar; GW170817 tidal-deformability cross-check.

## Pass/fail gate
- PASS (model viable): NS data show a compactness-correlated departure from GR-TOV consistent with energy-only sourcing, or current data lack the precision to distinguish (model survives as not-yet-tested).
- FALSIFIED: NS structure confirmed GR-pressure-sourced to better than the predicted O(3p/ρc²); single-scalar dielectric excluded in the interior (forcing the full-tensor G_μν = 8πG T_μν and abandoning one-field gravity inside matter).

## Provenance
F173 (the discriminator + exact coefficients), F64/F106 (the sourcing law), F114 (the exterior strong-field counterpart, +4.6% shadow), FC08 (the EP confirmations that pin R = 1 for energy but leave the pressure sector open).
