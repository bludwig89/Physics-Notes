# F111 — Second-order light deflection: the canonical dielectric $K=e^{2u}$ vs GR

*2026-06-07. **Recovered 2026-07-31** at the roadmap C8.2 close-out: the C8 audit found F111 had no finding file while two tests claimed the number. The write-up already existed — in the test's own docstring — so this file records it where the index can see it. **`tests/findings/test_F111_second_order_deflection.py` remains the primary record**; nothing here is new physics, and every number below is quoted from that test and its committed artifact `test-results/F111_second_order_deflection.json`.*

## Summary

F107/L4a proved the straight-ray deflection is exactly $-4u_b$ at all field strengths. This finding computes the **next** order — the $O(u^2)$ ray-bending term, which is the first place the exponential lattice index can differ from GR.

A spherically symmetric index $n(r)$ in flat space bends a ray of asymptotic impact parameter $b$ by the Bouguer/eikonal integral, with $w = b/r$:

$$\Delta\phi = 2\int_0^{w_0}\frac{dw}{\sqrt{n(w)^2 - w^2}},\qquad \alpha = \Delta\phi - \pi,\qquad n(w_0) = w_0 .$$

For any index expanding as $n = 1 + 2\varepsilon w + \sigma\varepsilon^2 w^2$ with $\varepsilon = GM/(bc^2)$, truncating at $O(\varepsilon^2)$ makes $n^2 - w^2$ **quadratic** in $w$, so the integral is an exact arcsine and the series closes:

$$\alpha = 4\varepsilon + \pi(2+\sigma)\,\varepsilon^2 + O(\varepsilon^3).$$

| Index | $\sigma$ | $\alpha_2$ |
|---|---|---|
| GR (isotropic Schwarzschild, $n=(1+x)^3/(1-x)$, $x=m/2r$) | $7/4$ | $15\pi/4$ — the textbook coefficient, so this validates the machinery |
| **Lattice canonical (F64/F107), $n = K = e^{2u} = 1 + 2u + 2u^2 + \dots$** | $2$ | $\mathbf{4\pi}$ |
| Deprecated weak-field map $(1-u)^{-2} = 1 + 2u + 3u^2$ | $3$ | $5\pi$ (informational) |

So the canonical dielectric's second-order excess over GR is $\alpha_2^{\text{lat}} - \alpha_2^{\text{GR}} = \pi/4\,\varepsilon^2$.

## Checks (from the test)

| ID | Claim | Class |
|---|---|---|
| D1 | general closed form $\alpha_2(\sigma) = \pi(2+\sigma)$ | Tier 1, sympy |
| D2 | GR cross-check $\sigma = 7/4 \Rightarrow 15\pi/4$ | Tier 1 |
| D3 | lattice $\sigma = 2 \Rightarrow 4\pi$; difference vs GR $= \tfrac{\pi}{4}\varepsilon^2$ | Tier 1 |
| D4 | deprecated map $\sigma = 3 \Rightarrow 5\pi$ | informational |
| N1 | mpmath quadrature of the **full** exponential index recovers the $4\pi$ coefficient | numerical |

## Why this file exists

The C8.2 audit reported F111 as a *gap* — a number with no finding file — while `tests/findings/` held **two** tests claiming it. That is a collision in the test tree with no finding on either side, which no index could show. This file and its sibling [[F111b-tree-gauge-su3-ladder]] close the gap; the sibling carries the F110 scope items and took the `b` suffix under the C8.2 close-out rule (the less-cited of a colliding pair takes `b`, keeping the number findable).

D3 is also the check the supersession ledger relies on: S4's F114 record notes that the retired `test_F114_dielectric_black_hole.py`'s one non-black-hole check is duplicated here, which is why no unique coverage was lost when that file was retired at C7.6.

**Status:** live. Artifact `test-results/F111_second_order_deflection.json`; registry record `F111-second-order-deflection`.
