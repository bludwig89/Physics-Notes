# F185 — Slow-rotation frame dragging and moment of inertia on the F181 kernel: I/MR²≈0.31, I≈0.6×10⁴⁵ g cm², Lense-Thirring drag recovered (scenario S2)

**Date:** 2026-06-30 - 04:15
**Numbering:** **F185** (re-checked; sequential after F184).
**Status:** Confirmed — 3/3 checks PASS. Hartle slow-rotation theory on the two-function background; quantitative.
**Module:** `ca-simulation/ca_rotation.py` (uses `ca_interior_metric` / F181)
**Script:** `tests/findings/test_F185_rotation.py`
**Results:** `test-results/F185_rotation.json`
**Cross-references:** [[F181-covariant-interior-kernel-battery]] (static background), [[F184-tabulated-eos-neutron-stars]] (the M–R sequence this rotates), [[F183-blackhole-under-full-tensor]] (the strong-field frame dragging $\Omega_H$). External: Hartle, ApJ 150, 1005 (1967); I-Love-Q (Yagi & Yunes 2013).

---

Scenario S2. Extends the interior to first order in spin: the dragging of inertial frames $\varpi(r)=\Omega-\omega(r)$ obeys Hartle's linear ODE on the F181 background, $\frac{d}{dr}(r^4 j\,\varpi')+4r^3 j'\varpi=0$ with $j=(AB)^{-1/2}$; the moment of inertia is read off the surface, $I=J/\Omega$ with $J=\tfrac16 R^4\varpi'(R)$.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| R1 | Moment of inertia of a representative star ($M=0.95\,M_\odot$, $R=10.4$ km): $I/MR^2=0.313$, dimensionless $\bar I=I/M^3=17.2$, surface frame-drag $\omega/\Omega=0.084$ — all in the physical NS band | PASS |
| R2 | Monotonicity: more compact stars drag frames more strongly ($\omega/\Omega\uparrow$) and have smaller $\bar I$ — the correct trend with compactness | PASS |
| R3 | SI value: $I=6.3\times10^{37}$ kg m² $=0.63\times10^{45}$ g cm² — the pulsar moment-of-inertia range | PASS |

## Result

Frame dragging and the moment of inertia come out of the two-function interior with no extra input: $I/MR^2\approx0.3$ and $\omega/\Omega$ increasing with compactness are the standard GR results. This is the rotating-compact-object rung — the $I$ that enters pulsar spin-down, the I-Love-Q relations, and (with the F184 sequence) a future moment-of-inertia measurement for a double pulsar.

## Open / next
- Tidal Love number $k_2$ on the same kernel → the full I-Love-Q triple.
- Second-order Hartle (oblateness, quadrupole moment) for rapidly spinning stars.

## Files
- Module: `ca-simulation/ca_rotation.py` · Test: `tests/findings/test_F185_rotation.py` · Results: `test-results/F185_rotation.json`
