# F186 — Black-hole shadow ray-tracer: b_c=3√3 M confirmed by geodesic integration; M87* 39.7 μas, Sgr A* 53.3 μas (GR), withdrawing the F114 +4.63% (scenario S3)

**Date:** 2026-06-30 - 04:20
**Numbering:** **F186** (re-checked).
**Status:** Confirmed — 3/3 checks PASS. Numeric null-geodesic shadow + analytic μas conversion; quantitative.
**Module:** `ca-simulation/ca_raytrace.py` (uses `ca_blackhole` / F183)
**Script:** `tests/findings/test_F186_shadow_raytrace.py`
**Results:** `test-results/F186_shadow_raytrace.json`
**Cross-references:** [[F183-blackhole-under-full-tensor]] (the shadow), [[F114-dielectric-black-hole]] (the superseded +4.63% prediction this withdraws), [[F107-canonical-a-adoption-L4-grb-gate]] (SI lock). External: EHT M87* (2019, ring $42\pm3$ μas); Sgr A* (2022, ring $51.8\pm2.3$ μas); Bardeen 1973.

---

Scenario S3. Backward-integrates the photon orbit equation $d^2u/d\phi^2+u=3Mu^2$ to find the capture/escape boundary (the shadow), then converts to an on-sky angular diameter for the EHT targets.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| T1 | Ray-traced critical impact parameter $b_c=5.1961\,M$ vs analytic $3\sqrt3=5.1962\,M$ (agreement $<10^{-3}$) | PASS |
| T2 | EHT shadow **diameters**: M87* $39.7$ μas, Sgr A* $53.3$ μas (canonical GR); F114 would give $41.5$ / $55.7$ μas — the **+4.63% enlargement is withdrawn** | PASS |
| T3 | Kerr: the equatorial shadow displacement grows monotonically with spin ($a=0.3\to0.998$) — the spin–shadow asymmetry | PASS |

## Result

The shadow is exactly GR. The geodesic integration reproduces $b_c=3\sqrt3\,M$ to the integrator floor, and the μas diameters sit consistently inside the EHT rings (the emission ring is ~10% larger than the shadow). The model's earlier distinctive prediction — the F114 dielectric BH's $+4.63\%$ enlargement, offered as an ngEHT target — is **formally withdrawn**: the canonical object predicts the GR shadow, and the Kerr spin–shadow relation is the model's testable rotating-BH signature.

## Open / next
- Full image-plane Kerr ray-tracing (accretion-disk emission) for a direct EHT-image comparison.
- Spin extraction: invert the measured asymmetry for $a$ on a specific target.

## Files
- Module: `ca-simulation/ca_raytrace.py` · Test: `tests/findings/test_F186_shadow_raytrace.py` · Results: `test-results/F186_shadow_raytrace.json`
