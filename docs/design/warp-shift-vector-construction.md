# Exploration: constructing the F204 open items (warp shift vector & forward Bobrick–Martire)

**Date:** 2026-06-30 - 21:40
**Type:** construction-exploration (follow-up to [[F204-alcubierre-warp-structural-exclusion]] §Open). Not yet a finding — this records the construction *paths*, a reusable kernel, and the **first computations** for each open item, plus exactly what remains before either could be promoted.
**Runner:** `tests/runners/run_warp_openitems_explore.py` (numpy-only + F181 kernel; ~3 s)
**Cross-references:** [[F204-alcubierre-warp-structural-exclusion]] (the verdict these extend), [[F185-slow-rotation-moment-of-inertia]] (`ca_rotation.py` — the rotational g₀ᵢ kernel reused conceptually), [[F181-covariant-interior-kernel-battery]] (static lapse leg), [[F180-gravitational-wave-speed]] (induced-metric signal speed = c_lat), [[F193-ontic-vacuum-gravitates-as-zero]] (beable non-negativity), Findings 25/26 (c_lat).

---

## The two open items (restated)

F204 closed the **superluminal** Alcubierre family by a beable-source argument (M2) and an exact symbolic energy-density gate, and left the **subluminal** positive-energy class open. Its two named next-rungs were:

1. A **dynamically/structurally** evaluated *superluminal shift vector* (g₀ᵢ) through a gravitomagnetic T⁰ⁱ kernel — F204's PC1 only checked the static diagonal field, not the off-diagonal shift that actually carries the bubble.
2. A genuine **forward** Bobrick–Martire construction: build a positive-T⁰⁰, momentum-carrying beable shell and read off the induced subluminal geometry.

The key realization that makes both tractable: **the warp shift vector N^i = g₀ᵢ is the translational analogue of Hartle's rotational frame-drag ω(r)** already built in `ca_rotation.py` (F185). Both are the off-diagonal metric component sourced by momentum density. In the weak field (Lorenz gauge) the off-diagonal Einstein equation is a vector Poisson equation,

$$\nabla^2 N_i = -16\pi\,T^{0i},$$

which the exploration solves in **free space** (Hockney zero-padded FFT, kernel $4/\lvert r\rvert$) so a moving positive mass produces a finite, localized drag field — exactly what a warp shift vector is. This is the shared `gem_shift()` kernel.

## Item 1 — superluminal shift vector: two computed obstructions

The shift vector itself is benign (it is just a frame-drag field). The obstruction to a *superluminal* one is structural, and the exploration pins down **two independent, computed** reasons — both sharper on the lattice than in continuum GR.

**(1a) The lattice rest frame goes spacelike at exactly v_s = c_lat.** The beable cells are the physical substrate; they sit at fixed spatial position, so their worldline is $x=\text{const}$ with proper interval $ds^2=g_{00}\,dt^2$, and for the Alcubierre form $g_{00}=-(c_\text{lat}^2-v_s^2 f^2)$. Inside the bubble $f=1$:

| $v_s/c_\text{lat}$ | $g_{00}$ | cell worldline |
|---|---|---|
| 0.50 | $-0.250$ | timelike (beable OK) |
| 0.90 | $-0.063$ | timelike (beable OK) |
| 1.00 | $0.000$ | **null (boundary)** |
| 1.10 | $+0.070$ | **spacelike — no beable rest frame** |
| 1.50 | $+0.417$ | **spacelike — no beable rest frame** |

In continuum GR one escapes this by choosing the Eulerian (freely-falling, geodesic) slicing, whose observers thread the bubble wall without their worldlines going spacelike. **On the lattice that escape is unavailable**: the cells are fixed physical beables, not free to fall through the wall, so when the cell worldline goes null at $v_s=c_\text{lat}$ there is simply *no lattice description of the bubble interior*. This is a model-specific sharpening of the SR objection (M2/M4).

**(1b) The induced-metric signal cone is c_lat.** F180 derived that the metric perturbation (the $\ln K$ / gravitational-wave field) obeys $(\nabla^2-c_\text{lat}^{-2}\partial_t^2)=\text{source}$, i.e. it propagates at $c_\text{lat}$ ($v_\text{ph}=\omega/k=c_\text{lat}=0.57735$, reproduced). The field that would have to *carry and steer* the bubble therefore cannot itself outrun $c_\text{lat}$: a $v_s>c_\text{lat}$ bubble has no causal assembly or maintenance. This is independent of the energy-condition problem and closes F204's open problem #3 in the structural sense (a *dynamical* well-posedness proof — evolving an off-diagonal source through a hyperbolic kernel and watching the IVP fail — remains the harder next step).

## Item 2 — forward Bobrick–Martire: positive moving shell → induced shift (first build)

Forward direction (matter → metric), the model's committed causal order (M1). A positive-energy spherical shell (beable $T^{00}=\rho\ge0$), normalized to a chosen weak-field compactness $M/R_0$, is translated at velocity $v$; its momentum density $T^{0x}=\rho v$ is fed through `gem_shift()`; the induced shift vector $N_x=g_{0x}$ is read off. Results (weak field, $M/R_0=0.02$):

- **A real shift vector is produced.** $\max\lvert N_x\rvert\approx0.009$–$0.040$ for $v=0.2$–$0.9\,c_\text{lat}$ (weak-field valid, $\lvert N\rvert\ll1$).
- **The interior is carried along — partially.** The frame-drag (carry-along) velocity at the bubble centre is a *velocity-independent fraction* $N_x/v\approx0.078\approx4(M/R_0)$ of the source velocity. This is genuine frame dragging, the translational Lense–Thirring effect.
- **WEC holds by construction.** Total energy density (matter $\rho\ge0$ plus gravitomagnetic field energy $\sim\lvert\nabla\times\mathbf N\rvert^2/16\pi\ge0$) has $\min T^{00}=+2.4\times10^{-37}\ge0$ everywhere — **no negative wall**, in direct contrast to the Alcubierre case (F204 G1).
- **Full carry-along needs strong field, where F204 returns.** The drag fraction scales ~linearly with compactness ($0.02\to0.078$, $0.10\to0.39$), so reaching $N_x/v\to1$ (a true co-moving bubble) requires $M/R_0\sim O(1)$ — the strong-field regime where the linear positive-source picture fails and F204's nonlinear $-v_s^2$ negative wall reappears:

| $M/R_0$ | drag fraction $N_x/v$ | $\max\lvert N\rvert$ | regime |
|---|---|---|---|
| 0.02 | 0.078 | 0.022 | weak-field OK |
| 0.10 | 0.388 | 0.112 | weak-field OK |
| 0.50 | 1.94 *(extrapolated)* | 0.56 | strong field — F204 wall returns |

**Reading:** the subluminal Bobrick–Martire class is *realizable forward on the lattice* with positive beable matter — the kernel and the field are well-behaved and the WEC is respected — but the carry-along is **partial** and the configuration is **subluminal**, so there is **no FTL payoff**. This is fully consistent with F204 and with the standard literature floor (positive-energy ⇒ subluminal).

## What is done vs what remains (promotion gate)

| Piece | Status |
|---|---|
| Gravitomagnetic shift-vector kernel `gem_shift()` (forward $T^{0i}\to g_{0i}$, free-space) | **Built + sanity-checked** (frame-drag fraction $\approx4M/R_0$, velocity-independent, weak-field) |
| Item 1a — lattice cell worldline spacelike at $v_s=c_\text{lat}$ | **Computed** (exact sign-flip at $c_\text{lat}$) |
| Item 1b — induced-metric signal cone $=c_\text{lat}$ | **Reproduced** from F180 (not a new derivation) |
| Item 2 — forward positive shell → shift vector, WEC$\ge0$, partial drag | **Computed (linearized/weak-field)** |
| **Remaining for a finding:** *nonlinear* forward solve (full $G_{\mu\nu}$, not GEM-linear) of the moving shell; a *dynamically evolved* off-diagonal source through a hyperbolic kernel showing the IVP break at $c_\text{lat}$; a quantitative match to the Fuchs/"Warp Factory" subluminal target metric | **Open** |

The exploration is enough to upgrade F204's two open items from "named" to "first construction complete, with a reusable kernel and definite numbers." It does **not** yet warrant a new finding: Item 1b reproduces F180, and Item 2 is linearized (the genuine nonlinear forward solve the brief ultimately wants is still pending). When the nonlinear forward solve and the dynamical IVP-break are added, this becomes a publishable rung (provisional tag **F2xx-warp-shift-vector-construction**).

## Files
- Runner: `tests/runners/run_warp_openitems_explore.py`
- Reuses: `ca-simulation/ca_interior_metric.py` (F181), conceptually `ca-simulation/ca_rotation.py` (F185)
