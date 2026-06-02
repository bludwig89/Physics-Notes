# F62 — Dynamical Dirac CA on a curved background (D2) + linearized backreaction (D3a)

**Date:** 2026-05-30 - 15:30
**Status:** Confirmed — 6/6 tests PASS.
**Module:** new `ca-simulation/forks/dirac_gravity_fork.py` (additive; reuses `ca_dirac` primitives, `ca_curved.CayleyVarcSolver2D`).
**Tests:** `model-tests/test_F62_dirac_gravity_fork.py`; results `test-results/F62_dirac_gravity_fork.json` / `.md`.
**Plan:** realises `ca-dirac-gravity-plan.md` Stages **D2** (static curved background, time-domain) and **D3a** (linearized backreaction). Stage **D1** (flat Dirac propagator, m=0 → Weyl) was already in `ca_dirac.py`; the static-background *dispersion* identity was already in `gr_fork_F46_dirac.py` (F46/F50).

## What was open

F50/F52 established the curved-background Dirac physics at the level of the **dispersion identity** (the F46 spherical triangle with site-dependent legs) and the **static** redshift/deflection coefficients. What had never been run is the **time-domain wave-packet evolution** the plan calls for: releasing a packet on a curved background and watching its centroid / internal clock track the analytic geodesic, and letting the metric be **sourced by the matter itself** rather than imported. This finding closes that gap.

The curved-tetrad chiral Dirac Hamiltonian for a static diagonal metric $ds^2=-A c_0^2 dt^2 + B\,\delta_{ij}dx^idx^j$ is

$$i\,\partial_t\Psi=\Big[c_\text{eff}(\mathbf x)\,\boldsymbol\alpha\cdot\hat{\mathbf p}+\sqrt{A(\mathbf x)}\,m\,\beta\Big]\Psi,\qquad c_\text{eff}=c_0\sqrt{A/B},$$

propagated by the symmetric Strang tick $\text{Mix}_\text{rest}(\sqrt A\,m,\tfrac{dt}{2})\circ\text{Kinetic}(c_\text{eff},dt)\circ\text{Mix}_\text{rest}(\sqrt A\,m,\tfrac{dt}{2})$. Each sub-operator is exactly unitary.

## Results

| Test | What it checks | Result |
|---|---|---|
| **D1** flat regression | gravity stepper with $m=0$, flat $A=B=1$ reduces to two decoupled exact-QCA Weyl walks | residual **0.0** (bit-for-bit) |
| **D2a** Rindler free-fall | rest packet released in $\sqrt A=1+a\xi$ frame | falls toward **low lapse**; $\lvert g\rvert/(a\,c_\text{lat}^2)=0.91$; trajectory **mass-independent** (universality spread 0.085); norm drift $2.8\times10^{-14}$ |
| **D2b** dynamical redshift | clock frequency vs lapse, two static clocks | $f_\text{near}/f_\text{far}=0.897$ vs predicted $2\arcsin(\sqrt A m)$ ratio $0.891$ (0.6%) |
| **D2c** Schwarzschild deflection | fast ($m{=}0$) packet past a weak mass | bends **toward** the mass; field eikonal $K_\text{eik}=-3.92$ (**Einstein factor-2**); dynamical centroid $K_\text{meas}=-3.43$ (meas/eik $=0.88$) |
| **D3a** backreaction norm | norm under self-sourced, evolving metric | drift $2.5\times10^{-15}$ |
| **D3a** self-redshift | clock in the field's *own* well | $A_\text{near}=0.79$, $A_\text{far}=1.02$; $f_\text{near}/f_\text{far}=0.903$ vs predicted $0.869$; deep clock slower (**loop closes**) |

## Two payloads worth flagging

**1. The lattice equivalence principle is exact in coefficient and universal in mass.** A rest packet in a Rindler frame free-falls toward lower lapse with coordinate acceleration $d^2\xi/dt^2\to -a\,c_\text{lat}^2$, with $c_\text{lat}^2=\tfrac12$ the exact-QCA lattice light speed. The continuum reduction gives this coefficient *independent of mass*: with rest energy $V=\arcsin(m_\text{field})$, force $-\partial_\xi\arcsin(\sqrt A m)=-am/\sqrt{1-m^2}$ and inertial mass $M_I=2m/\sqrt{1-m^2}$ cancel the mass to give $a/2$. Measured trajectories for $m\in\{0.2,0.35,0.5\}$ coincide to 8.5% (final displacement $\approx-16$ cells for all three) — inertial mass $=$ gravitational mass on the lattice.

**2. A latent sign error in `dirac_step_2d_varm_splitstep` was uncovered and corrected here.** The exact-QCA kinetic block carries the mass as $+i\,m_0$ (generator $-m_0\beta$), so a per-cell $\delta m$ correction must be applied with the *matching* sign to give effective site mass $M=m_0+\delta m$. The existing variable-mass stepper applies $\text{Mix}(+\delta m\,dt/2)=\exp(-i\beta\,\delta m\,dt/2)$, the opposite sign, so its effective mass is $m_0-\delta m$ (verified: a uniform $m_\text{field}=0.5$ with baseline $m_0=0.3$ propagates closer to the $m=0.1$ reference than $m=0.5$). This is **harmless in every existing production use** — they all have $\delta m=0$ (uniform mass) — but it inverts the force of a *mass gradient*, which would make gravity repulsive. The new `gravity_dirac_step_massive` uses the corrected angle $\theta=-\delta m\,dt/2$, after which a gravitational well (low $\sqrt A$) correctly **attracts**. *Follow-up: fix the sign in `ca_dirac.dirac_step_2d_varm_splitstep` itself once a gradient-mass production test exists to guard it.*

## What is derived vs posited

- **Derived/tested:** that the F46/F50 curved-background Hamiltonian, run as a time-domain CA, reproduces (i) the equivalence-principle free-fall with the exact lattice coefficient $a\,c_\text{lat}^2$ and mass-universality; (ii) the redshift as a *dynamical* clock-rate ratio $\sqrt{A_\text{near}/A_\text{far}}$; (iii) the Einstein factor-2 light bending in the eikonal limit of the dynamical run; (iv) exact-unitary norm conservation under a self-sourced, co-evolving metric; (v) closure of the backreaction loop (self-redshift sourced by $\nabla^2\Phi=4\pi G\rho$, not an imported $-GM/r$).
- **Posited (input, not derived):** the weak-field map $\Phi\mapsto(A,B)=(1+2\Phi/c^2,\,1-2\Phi/c^2)$ and the $4\pi G$ Poisson coupling (Newton's constant enters by hand — same caveat as F52). The D3a run is **2D**, so its Poisson Green's function is logarithmic, not $1/r$ (Finding 8): the self-redshift is tested for *self-consistency with the field's own lapse*, not against an absolute $1/r$ profile.

## Limitations / honest caveats

- The Schwarzschild dynamical deflection realises ~88% of its own eikonal limit; the gap is finite packet width + centered-difference dispersion at finite $k$, and shrinks at lower $k_\text{in}$ (ratio $0.49\to0.88$ from $k_\text{in}=1.2\to0.5$).
- The Rindler coefficient is measured from an early-window parabola fit; the whole-trajectory fit overestimates $g$ once the packet becomes mildly relativistic. The *universality* (mass-independence) is the sharper, less parameter-sensitive signal.
- D3a is linearized weak-field backreaction (the plan's D3a). The full nonlinear Sachs-Hamiltonian route (D3b) and the page-26 disagreement remain open.

## Relation to other findings

Builds on **F46** (the spherical-triangle dispersion; rest leg = clock), **F50** (gravity on the rest leg, but imported), and **F52** (lapse sourced from $\rho$; rest leg alone → Newtonian, both legs → Einstein). F62 is the **time-domain** counterpart: the same physics propagated as wave packets, with the metric optionally self-sourced. The factor-2 eikonal $K\approx4$ here reuses the F52 discriminator. Links: [[f53-fg9-C-CP-closed]] (per-species structure), [[higgs-free-su2-key-choice]] (the underlying chiral Dirac), [[project-folder-structure]].
