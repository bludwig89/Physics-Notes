# F139 — The self-consistent dual-Ginzburg-Landau back-reaction: the flux that the condensate confines is what melts it

**Date:** 2026-06-11 - 20:05
**Status:** Confirmed — 4/4 checks PASS. G1 ODE-exact (GL domain wall to mesh floor); G2 machine (fixed-point residual $<10^{-6}$, monotone); G3/G4 quantitative (pinch-off cured; ~constant string tension).
**Module:** `ca-simulation/ca_dual_gl_backreaction.py` (new); `src/casim/particles/channel.py` (`ColourBagChannel` gains a `backreaction: true` self-consistent mode).
**Scenario:** `scenarios/proton_bag_sc.yaml`.
**Test:** `tests/findings/test_F139_dual_gl_backreaction.py` (4/4, ~39 s).
**Results:** `test-results/F139_dual_gl_backreaction.json`.
**Cross-references:** [[F137-live-colour-dielectric-flux-tube]] (the mean-field bag this completes — its §5 open edge), [[F86-colour-dielectric-dual-superconductor]] (the dual-superconductor mechanism and the exact BPS $\sigma=2\pi v^2 n$ this realises dynamically), [[F88-colour-condensate-from-model]] (the condensate VEV that sets the scale), [[F122-p2-dynamical-baryon-three-body]] (the dynamical baryon whose confining field this is), [[F64-gravity-dielectric]] (the parallel impedance-matched dielectric).

---

## 1. What this closes

F137 made the proton's confining bag **live** — the colour-magnetic condensate $f(x)$ melted where the quark colour charge sits — but only as a **mean-field** dielectric: the condensate responded to the colour-charge density through a *fixed* Gaussian smear $\lambda$ (a one-way map $\rho\to\phi=G_\lambda*\rho\to f^2=e^{-\phi/\phi_0}$). Its honest open edge (F137 §5): *"the condensate responds to the colour-charge density through a fixed smear, not a self-consistent dual-Ginzburg-Landau back-reaction. Consequently the flux tube is connected and linear only out to $\sim2\lambda$, then pinches."*

This finding closes that loop. It implements the genuine **self-consistent dual-Ginzburg-Landau (dual-GL) back-reaction**: the colour-electric flux that the condensate confines is *itself* what melts the condensate, and the two fields are solved to **mutual consistency**. The condensate digs the channel; the channel's expelled flux re-shapes the condensate; iterate to a fixed point. The pinch-off is cured — the tube stays connected and linear to arbitrary separation.

## 2. The coupled system

Order parameter $f(x)\in[0,1]$ (normalised condensate $|\phi|/v$: $f\to1$ vacuum, $f\to0$ melted core); colour-dielectric $\varepsilon_c(f)=1-f^2$ (F86: $\varepsilon_c\to0$ in the condensed vacuum expels flux, $\varepsilon_c\to1$ in the melted core conducts it); quark colour charge $\rho^a(x)$ (octet, each colour-singlet so $\int\rho^a=0$). The dual-GL free energy — the **real-space, charge-sourced (Friedberg–Lee) partner** of F86's gauge-vortex BPS functional — is

$$F[f]=\int d^dx\Big[(\nabla f)^2+\tfrac{1}{4\xi^2}(f^2-1)^2+\tfrac12\sum_a\frac{\lVert\mathbf D^a\rVert^2}{\varepsilon_c(f)}\Big],$$

with the colour-electric displacement $\mathbf D^a=\varepsilon_c\mathbf E^a$, $\mathbf E^a=-\nabla\psi^a$ fixed by the **dielectric Gauss law** (the dual-superconductor constraint — the quarks pin the flux, the condensate must let it pass):

$$\nabla\!\cdot\!(\varepsilon_c\nabla\psi^a)=-\rho^a.$$

The condensate Euler–Lagrange / gradient flow (flux frozen during each $f$-substep, $\psi^a$ re-solved each outer sweep) is

$$\frac{\partial f}{\partial\tau}=-\frac{\delta F}{\delta f}=2\nabla^2 f-\frac{1}{\xi^2}(f^2-1)f-\boxed{f\sum_a\frac{\lVert\mathbf D^a\rVert^2}{\varepsilon_c^2}}.$$

The boxed term is the **back-reaction** F137 lacked: where the confined flux $\lVert\mathbf D\rVert^2$ is large it drives $f\to0$ (melts the condensate), which raises $\varepsilon_c$ there, which lets more flux through — the self-consistent feedback. Because $\varepsilon_c\to0$ would force $\lVert\mathbf E\rVert\to\infty$ to satisfy $\nabla\!\cdot\!\mathbf D=\rho$, the flux **cannot** be expelled from its own path: it digs a channel of finite $\varepsilon_c$ whose cross-section is set by the balance of bag pressure ($\tfrac1{4\xi^2}$) against field energy — a flux tube. The mean-field smear $\lambda$ is no longer posited; it **emerges** from the coherence length $\xi$.

Everything is pure numpy (CLAUDE.md): a matrix-free CG solve of the variable-coefficient Gauss law and a hand-rolled GL gradient flow; works in 2D (transverse / $q\bar q$ plane) and 3D (BCC box).

## 3. The results (G1–G4)

**G1 — the condensate sector is exact.** With zero field the $f$-flow relaxes, from a crude step seed, to the **analytic GL domain wall** $f(x)=\tanh(x/2\xi)$ (the kink of $2f''=\xi^{-2}(f^2-1)f$) to $5.6\times10^{-4}$ (mesh-floor; ODE-exact). The GL machinery is correct independently of the back-reaction.

**G2 — the coupled loop converges to a true fixed point.** For a static $q\bar q$ pair the self-consistency residual is driven **monotonically** to $9.5\times10^{-7}$ in 313 iterations — a genuine stationary point of the coupled $(f,\text{flux})$ system, not a one-shot map.

**G3 — the pinch-off is cured (the headline).** For two static colour charges, midpoint $\varepsilon_c$ (tube depth) vs separation $R$:

| $R$ | mean-field $\varepsilon_c^{\text{mid}}$ (F137) | self-consistent $\varepsilon_c^{\text{mid}}$ (F139) |
|---|---|---|
| 2 | 0.71 | 0.98 |
| 5 | 0.72 | 1.00 |
| 8 | 0.38 (pinching) | 1.00 |
| 11 | 0.12 (**pinched**) | 0.99 |

The mean-field channel collapses beyond $\sim2\lambda$ (the F137 limitation, reproduced here as the control); the self-consistent tube stays **connected** ($\varepsilon_c^{\text{mid}}>0.97$) at every separation. The back-reaction is the cause: at $R=11$ the self-consistent depth is $8\times$ the mean-field's.

**G4 — linear confinement with a constant string tension.** The bag/string energy $E_{\text{bag}}=\int\tfrac1{4\xi^2}(f^2-1)^2$ rises monotonically and **linearly** in $R$ (10.6, 29.4, 50.9, 74.1), with a tension $dE_{\text{bag}}/dR$ flat to within a factor 1.23 (6.3 → 7.7) — i.e. an $R$-independent tube cross-section, the defining property of a flux tube and the **dynamical realisation of F86's exact $\sigma=2\pi v^2 n$**. The vacuum limit is clean: zero colour charge leaves the condensate full, $f_{\min}=1.0000$ (no spurious melting).

## 4. The live channel

`ColourBagChannel` gains a `backreaction: true` mode: each tick it assembles the net signed octet source $\rho^a=\sum_{\text{quarks}}J^a_{\text{colour}}$ (scaled by the colour coupling `g_src`), solves only the non-trivial (Cartan-dominated) octet directions for speed, and runs a **warm-started** dual-GL relaxation seeded from the previous tick's $f$ — so the quasi-static bag tracks the slowly-moving quarks in $\sim$10–16 sweeps/tick. The quarks read the same scalar wall $S(x)=M_{\text{bag}}f^2(x)$ via `confine.field` (F135 mechanism), so nothing on the quark side changes; only the bag is now self-consistent. On the `uud` proton (`proton_bag_sc.yaml`, $L=16$ BCC) the live self-consistent bag melts to $\varepsilon_c^{\text{core}}\approx0.50$ with a non-flat wall ($S$: 3.97 → 7.96), matching F137's melt depth but now closing the loop. Default mode is unchanged (mean-field), so the F137 suite still passes 3/3.

## 5. Checks

| # | Check | Tier | Residual |
|---|---|---|---|
| G1 | $f$-flow (zero field) $=$ analytic GL kink $\tanh(x/2\xi)$ | ODE-exact | $5.6\times10^{-4}$ (mesh) |
| G2 | coupled $(f\leftrightarrow$ flux$)$ loop converges to a fixed point | machine | res $9.5\times10^{-7}$, monotone |
| G3 | pinch-off cured: SC tube connected where mean-field pinches | quantitative | $\varepsilon_c^{\text{mid}}>0.97$ vs $0.12$ at $R=11$ |
| G4 | linear $E_{\text{bag}}(R)$, ~constant tension; vacuum $f=1$ | quantitative | tension flat to $1.23$; $f_{\min}=1.0000$ |

## 6. Honest scope / open edge

The flux sector is the **Abelian (colour-dielectric / Friedberg–Lee) reduction**: an electrostatic dual-Meissner model with $\varepsilon_c(f)$, the real-space dynamical partner of F86's gauge-vortex BPS vortex. The two formulations give the same physics (connected tube, linear $E(R)$, constant tension) but the *exact topological* value $\sigma=2\pi v^2 n$ remains F86's analytic gauge-vortex result, which this real-space tube reproduces qualitatively (constant tension), not yet to algebraic exactness — mapping the dielectric-model tension onto $2\pi v^2 n$ is the natural next sharpening. The full non-Abelian condensate (beyond the Cartan-dominated octet projection) is likewise not solved here. Scale separation (F134 §6) still gates physical fm/eV (U4). What is robustly established: the **self-consistent back-reaction exists, converges, and cures the F137 mean-field pinch**, restoring the asymptotic connected-and-linear flux tube of confinement.

## 7. Ledger

New module `ca-simulation/ca_dual_gl_backreaction.py` (variable-coefficient dielectric Poisson CG, GL gradient flow, the self-consistent loop, the analytic kink anchor); `ColourBagChannel` `backreaction` mode + `proton_bag_sc.yaml`; suite `tests/findings/test_F139_dual_gl_backreaction.py` (4/4). With F139, the dynamical baryon's confining field (F122/F137) is closed at the dual-GL level: the proton digs its own bag *and* the bag is held open by the very flux it confines. Exactness rows: Tier-3 #85 (pinch-off cured, A/B vs F137 mean-field), #86 (linear $E_{\text{bag}}(R)$ / constant tension, dynamical F86 $\sigma$).
