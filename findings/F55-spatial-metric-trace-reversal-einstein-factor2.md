# F55 — Spatial metric from trace reversal: Einstein's factor-2 from mass

**Date:** 2026-05-29 - 17:40
**Status:** Confirmed — 5/5 tests PASS (J1, J5 bit-for-bit exact; J2–J4 quantitative).
**Module:** new `ca-simulation/forks/gr_fork_F55_spatial_metric_backreaction.py` (additive; reuses `gr_fork_F52_restleg_backreaction` Poisson + `gr_fork_E_tensor` for the consistency check).
**Tests:** `model-tests/test_F55_spatial_metric_backreaction.py`; results `test-results/F55_spatial_metric_backreaction.json`.

## Where F52 left off

F52 closed the F50 loop for the **rest leg**: a clock-rate field sourced directly by rest-mass density reproduces the lapse √A and the factor-1 redshift. But it proved that sourcing *only* the rest leg (spatial metric $B\equiv1$) gives the Newtonian deflection $2GM/(bc^2)$ — factor 1. The missing half of the bending is the spatial metric $B$ (the kinetic-leg renormalisation $c_\text{eff}=c_0\sqrt{A/B}$), which the rest leg never touches.

## The mechanism: trace reversal

F55 sources $B$ from the **same** mass density via the linearised Einstein equation $\Box\bar h_{\mu\nu}=-(16\pi G/c^4)T_{\mu\nu}$. The principled content is the **trace reversal**. A static dust source has only $T_{00}=\rho c^2$ — its spatial stress $T_{ij}=0$, so naïvely the spatial metric should not be sourced. But trace-reversing feeds the temporal source into the spatial components:

$$\nabla^2\bar h_{00}=-\frac{4}{c^2}\nabla^2\phi\;\Rightarrow\;\bar h_{00}=-\frac{4\phi}{c^2},\qquad \bar h=-\bar h_{00},$$
$$h_{00}=\bar h_{00}-\tfrac12\eta_{00}\bar h=-\frac{2\phi}{c^2},\qquad h_{ij}=\bar h_{ij}-\tfrac12\eta_{ij}\bar h=-\frac{2\phi}{c^2}\,\delta_{ij}.$$

So **$h_{ij}=h_{00}$ even though $T_{ij}=0$** — the spatial perturbation equals the temporal one. Reading off the metric ($u\equiv-\phi/c^2=GM/rc^2$):

$$A\equiv-g_{00}=1-2u,\qquad B\equiv g_{ii}=1+2u,$$

which is the `gr_fork_E_tensor` *linearised* metric — but here **derived** from one mass-sourced scalar plus the trace-reversal identity, not posited. The equality $|B-1|=|A-1|$ is exactly the extra factor-1 that promotes Newton to Einstein.

## Results

| Test | What it checks | Result |
|---|---|---|
| **J1** trace-reversal identity | static dust ($T_{ij}=0$) yields $h_{ij}=h_{00}$ | $\max|h_{ij}-h_{00}|=0.0$ **bit-for-bit**; $h_{00}=-2\phi/c^2$ exactly |
| **J2** redshift unchanged | sourcing $B$ leaves the rest leg alone | mean ratio $1.010$ (factor-1, target 1) |
| **J3** deflection → factor-2 | eikonal $K\equiv\alpha bc^2/GM$ with trace-reversed $(A,B)$ | $K_\text{full}=4.021$ (Einstein), $K_\text{rest}=2.022$; self-consistent lattice ratio $1.99$ |
| **J4** uniqueness | sweep spatial fraction $\lambda$: $B=1+\lambda(B_\text{GR}-1)$ | $K(\lambda)=2(1+\lambda)$ — slope $1.993$, intercept $2.022$, $K(1)=4.017$ |
| **J5** consistency | trace-reversed $(A,B)$ vs `gr_fork_E_tensor` linearised | $\max|\Delta A|=\max|\Delta B|=0.0$ **bit-for-bit** |

Overall **PASS**.

## Interpretation

The loop is now Einsteinian, not Newtonian. From a single mass-sourced potential plus the trace reversal, **both** legs of the F46 triangle are sourced: the rest leg gives factor-1 redshift (J2, unchanged from F52), and the spatial metric — forced equal to the temporal by trace reversal (J1) — supplies the second half of the light bending, so $K\to4$ emerges self-consistently (J3).

**The factor-2 is not free.** The uniqueness sweep (J4) shows the eikonal coefficient is exactly $K(\lambda)=2(1+\lambda)$, linear in the fraction $\lambda$ of the spatial perturbation that is sourced. Only $\lambda=1$ — the trace-reversal value — gives Einstein's factor-2; $\lambda=0$ recovers F52's Newtonian factor-1. The model is pinned: Einstein's coefficient is selected by the trace reversal, not by a tunable knob.

Together F52+F55 answer the original question fully: gravity is an effect of the mass/time element, the rest leg alone gives Newton, and the trace-reversed spatial metric — sourced by the same mass — upgrades it to Einstein.

## What is derived vs posited

- **Posited (stronger than F52's scalar):** the linearised Einstein equation with the $16\pi G/c^4$ tensor coupling in Lorenz gauge. This is essentially assuming GR's field equation at linear order — F55 does *not* derive GR.
- **Derived/tested:** that this, applied to a static-dust source, forces $h_{ij}=h_{00}$ by trace reversal (J1, exact); keeps redshift at factor-1 (J2); makes deflection factor-2 emerge *uniquely* at the trace-reversal coefficient (J3, J4); and is bit-for-bit consistent with the project's existing linearised metric (J5).

## New exact results (exactness inventory)

- **J1** $h_{ij}=h_{00}$ for static dust — trace-reversal identity, residual $0.0$ (Tier-1 algebraic).
- **J5** trace-reversed $(A,B)$ $\equiv$ `gr_fork_E_tensor` linearised — residual $0.0$ (Tier-1 algebraic).

## Follow-ups

- **Full (non-linear) spatial source.** Promote the linearised trace reversal to the exact isotropic-Schwarzschild $B=(1+u/2)^4$ via an iterated/non-linear field equation, and check the post-Newtonian deflection corrections (the $\mathcal O(u^2)$ terms F52-H3b saw at strong field).
- **Derive the $16\pi G/c^4$ coupling** from the lattice (the kinetic-leg phase-matching $c_\text{lat}=d\Omega/d|\mathbf k|$ of F25/F26), the analogue of F52's open $4\pi G$ question — this is the step that would make the spatial source genuinely emergent rather than assumed.
- **Dynamical co-evolution** of both leg-fields with the Dirac matter that sources them, tested against the F50 Strang stepper.

## Relation to other findings

Direct sequel to **F52** (rest-leg back-reaction, factor-1) and **F50/F46** (the triangle and its gravitational renormalisation). Resolves the factor-1-vs-2 discriminator named in **Finding 8** and the geodesic-stage work, on the eikonal/weak-field side, by identifying the trace reversal as the source of Einstein's extra factor. Consistent with `gr_fork_E_tensor` (J5).
