# F52 — Gravity as a self-consistent rest-leg (clock-rate) field

**Date:** 2026-05-29 - 17:05
**Status:** Confirmed — 5/5 tests PASS (H1/H1b loop closure, H2 redshift factor-1, H3/H3b deflection discriminator).
**Module:** new `ca-simulation/forks/gr_fork_F52_restleg_backreaction.py` (additive; reuses `gr_fork_E_tensor` metric map and `ca_emqg.solve_poisson_3d`).
**Tests:** `model-tests/test_F52_restleg_backreaction.py`; results `test-results/F52_restleg_backreaction.json`.

## The open loop in F50

F46 established that the exact lattice Dirac dispersion is a right spherical triangle,

$$\cos\Omega_\text{Dirac}(\mathbf k,m)=\cos\Omega_\text{rest}(m)\cdot\cos\omega_\text{kin}(\mathbf k),\qquad \Omega_\text{rest}=\arcsin m,$$

so the **rest leg is simultaneously the mass term and the local proper-time clock rate** (the zitterbewegung rotation $2\arcsin m$ per tick at $\mathbf k=0$). F50 then showed gravity enters *entirely* through that rest leg in a static background, $\Omega_\text{rest}(x)=\sqrt{A(x)}\,\arcsin m$, with the lapse $\sqrt A$ carrying the redshift and $c_\text{eff}=c_0\sqrt{A/B}$ carrying deflection/Shapiro.

But F50 **imports** the lapse: it feeds an analytic Newtonian potential $\phi=-GM/r$ through the `gr_fork_E_tensor` metric map $\phi\mapsto(A,B)$. The coupling runs one way (mass → potential → leg renormalisation) and the potential is hand-supplied. F52 asks whether the lapse can instead be a *result* of mass.

## Hypothesis

Posit that the clock-rate field is the **equilibrium of a local lattice field equation** in which the rest-leg rotation-rate deficit is sourced directly by rest-mass density:

$$\nabla^2_\text{lat}\,\Phi(x)=4\pi G\,\rho(x),\qquad s(x)\equiv\sqrt{A(\Phi(x))}=\text{clock-rate field}.$$

No imported $-GM/r$; the source is $\rho$. "A clock at a site slows in proportion to the rest-mass it is phase-coupled to," relaxed to a fixed point.

## Results

| Test | What it checks | Result |
|---|---|---|
| **H1** loop closure (spectral) | $\Phi_\text{sc}$ from $\rho$ reproduces the imported $-GM/r$ outside the source | slope $\Rightarrow M_\text{eff}/M=0.973$, fit $r^2=0.99994$ — **same $1/r$ shape and amplitude** F50 imports |
| **H1b** loop closure (literal fixed point) | hand-rolled Jacobi relaxation of $\nabla^2\Phi=4\pi G\rho$ (6-neighbour, Dirichlet) converges to the same field | $M_\text{eff}/M=0.9995$, $r^2=0.998$, residual $1.0\times10^{-8}$ in 4315 iters |
| **H2** redshift (factor 1) | rest leg on $\Phi_\text{sc}$ gives $\Delta\nu/\nu=\Delta\phi/c^2$ | mean ratio $0.997$ (target 1, **not** baseline 2); rest-leg residual $0.0$ |
| **H3** deflection discriminator | eikonal deflection coefficient $K\equiv\alpha b c^2/GM$ | rest-leg-only $K=1.999$ (factor-1); full isotropic $K=4.015$ (factor-2); **ratio $2.009$** |
| **H3b** discriminator on the self-consistent field | same ratio on the mass-sourced lattice slice, not the analytic $\phi$ | ratio $2.007$ |

Overall **PASS**.

## Interpretation

1. **The loop closes.** F50's imported lapse is recoverable from mass alone: a field sourced by $\rho$ — solved either spectrally (H1) or as a literal real-space fixed point (H1b) — reproduces the very $-GM/r$ that F50 fed in by hand. Gravitational time dilation in this model is genuinely *an effect of the rest/mass element*, not a separately-imposed background.

2. **The rest leg alone gives only Newtonian gravity.** This is the sharp, falsifiable payload (and the factor-1-vs-2 question flagged in Finding 8 and the geodesic work). If gravity is sourced *only* as the rest/clock leg, leaving the spatial metric flat ($B=1$), the eikonal index is $n=1/\sqrt A$ and the deflection coefficient is exactly the Newtonian $2GM/(bc^2)$ — **factor 1**. Recovering Einstein's $4GM/(bc^2)$ — **factor 2** — *requires the spatial metric $B$ to also be sourced by mass*. The clean discriminator is the ratio $K_\text{full}/K_\text{rest}=2$, which cancels common lattice/window error and lands at $2.01$ on both the analytic and the self-consistent field.

So: **gravity can be an effect of the mass/time element — but the rest leg by itself yields Newton, not Einstein.** The missing half of the bending is precisely the part of the metric the rest leg does not touch.

## What is derived vs posited

- **Posited (input, not derived):** that the clock-rate deficit Poisson-couples to $\rho$ with coefficient $4\pi G$ — Newton's constant enters by hand, not from the CA update rule.
- **Derived/tested here:** (i) that this single mass-sourced field reproduces F50's imported lapse (loop closure, two independent solvers); (ii) that the rest leg on it yields factor-1 redshift; (iii) that a rest-leg-only source is *necessarily* factor-1 in deflection, identifying exactly the extra structure (a mass-sourced spatial metric $B$, i.e. a kinetic-leg field equation) that Einstein's factor-2 demands.

## Follow-ups

- **Source the spatial metric $B$.** A companion field equation for $B$ (the kinetic-leg renormalisation) sourced by mass — candidate: the same $\rho$ with a tensor/anisotropic stencil — and a check that $K_\text{full}\to4$ then emerges self-consistently rather than being imposed via `gr_fork_E_tensor`. This would promote the loop from Newtonian to Einsteinian.
- **Derive the $4\pi G$ coefficient.** Whether the coupling constant between local clock-rate slowing and rest-mass density follows from the CA neighbour-coupling rule (the $c_\text{lat}=d\Omega/d|\mathbf k|$ phase-matching of F25/F26) rather than being posited.
- **Dynamical back-reaction.** Replace the static Poisson equilibrium with a time-dependent rest-leg field co-evolving with the Dirac matter that sources it, and test against the F50 Strang stepper.

## Relation to other findings

Builds directly on **F46** (the triangle; rest leg = clock) and **F50** (gravity on the rest leg, but imported). Uses the **Finding 8** result that 3-D Poisson gives the true $1/r$ potential (the 2-D log potential would invalidate H1). The factor-1/factor-2 discriminator is the same one named in Finding 8 ("does not yet check the absolute deflection magnitude") and the geodesic-stage work (factor-1 Newtonian vs factor-2 Einstein control).
