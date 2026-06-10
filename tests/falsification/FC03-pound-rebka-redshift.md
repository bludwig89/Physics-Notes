# FC03 — Gravitational redshift (Pound–Rebka, GR-3)

**Tier:** C — consistency regression
**Falsification power:** ★★★ (the factor-2/clock-rate sector; F16 fork resolution)
**Model element under test:** the clock-rate (g_tt) leg of the F64 dielectric.
**Supersedes:** `tests-priority/test_04_GR3_pound_rebka.py`

## Hypothesis (GR-identical)
The dielectric clock-rate gives the equivalence-principle redshift

  `Δν/ν = gh/c² = GMΔr/(r²c²)` (PPN, exact at O(φ/c²)).

## Measured target + source
- Pound-Rebka / Pound-Snider: redshift confirmed to ~1%; modern clocks to ~10⁻⁵ and better.

## Falsification criterion
Falsified if the dielectric redshift departs from `gh/c²` at leading order (the GR-3 fork was shown resolvable by all three F14.5 forks; Mercury/FC01 is the discriminator — a redshift departure here would break the clock-rate leg).

## CASIM build & run
Static clock-rate readout on the dielectric.
1. Compute `1+z` from `g_tt=−e^(−2u)` between two radii; confirm `Δν/ν=gΔr/c²` at O(φ/c²) to grid floor.
2. Confirm the exact exponential form gives a finite, monotonic redshift (no horizon — links FA10).

## Pass/fail gate
- PASS: redshift matches `gΔr/c²` at leading order.
- FALSIFIED: leading-order departure from the EP redshift.

## Provenance
F16 (GR-3 fork resolution), F64 (dielectric clock rate), F62 (self-redshift loop), F112 §B (CONSISTENCY).
