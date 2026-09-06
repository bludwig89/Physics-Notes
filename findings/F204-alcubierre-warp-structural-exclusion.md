# F204 — The Alcubierre warp family under the model's induced-gravity / beable source: the superluminal branch is **structurally excluded** (stronger than the quantum-inequality bound), the subluminal positive-energy branch is allowed but FTL-less and capped at $c_\text{lat}=1/\sqrt3$

**Date:** 2026-06-30 - 20:55
**Numbering:** **F204** (re-checked; existing max was F203, with F202 a gap left by concurrent sessions — took the next number above the max to avoid a collision). Promotes the brief `docs/design/alcubierre-warp-structural-test.md` from a first-pass synthesis to an in-repo computation.
**Status:** Confirmed — 5/5 checks PASS. The energy-density result (G1) is **exact (sympy, zero residual)**; the integrated-energy, kernel-control, co-support and speed-limit results (G2/PA1/PA3/PC1) are numeric. **No new physics** is introduced: a known GR solution is confronted with the model's already-derived constraints (M1–M5 of the brief).
**Module:** reuses `ca-simulation/ca_interior_metric.py` (F181) — no new module.
**Test:** `tests/findings/test_F200_alcubierre_structural.py` (~7 s; numpy + sympy + F181 kernel). *(filename retains the working `F200` tag; the finding is F204.)*
**Results:** `test-results/F200_alcubierre_structural.json`
**Test record:** record `F200-alcubierre-structural` (tier battery) — the record for the test above; its id and filename keep the working `F200` tag, and its `findings:` now names **F204** rather than F200 (a different finding, the E_g sextic-coupling computation). The finding's other record, `run-warp-openitems-explore`, is a `legacy_script` with no failure mode and remains declared debt. Declared 2026-08-19.
**Cross-references:** [[F193-ontic-vacuum-gravitates-as-zero]] (M2: beable $T^{00}\ge0$, the fatal bound), [[F178-gravity-full-tensor-adoption]] (M1: induced full-tensor source), [[F181-covariant-interior-kernel-battery]] (M3: the two-function kernel, reused as control), [[F64-em-connection-gravity]] (the enclosed-mass dielectric), [[F107-canonical-a-adoption-L4-grb-gate]] / Findings 25/26 (M4: $c_\text{lat}=1/\sqrt3$). Brief: `docs/design/alcubierre-warp-structural-test.md`. External: Alcubierre 1994; Pfenning–Ford 1997 (gr-qc/9702026); Bobrick–Martire 2021 (2102.06824); Fuchs et al. 2024 (2404.03095).

---

## The question

Can any member of the Alcubierre warp-drive family be realized as an actual field configuration on the model's BCC lattice, given that here gravity is **induced** (sourced forward from beable matter, F178) rather than a freely specifiable geometry? This is the brief's hypothesis. It is *not* "does GR admit the metric" — GR admits any metric for *some* $T_{\mu\nu}$. It is "can the lattice **produce** the $T_{\mu\nu}$ the warp metric needs."

## What was computed (5/5 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | **Exact Eulerian energy density of the Alcubierre metric.** Full Einstein tensor of $ds^2=-dt^2+(dx-v_s f\,dt)^2+dy^2+dz^2$, contracted with the Eulerian normal $n^\mu=(1,v_s f,0,0)$, gives $\rho=-\tfrac{1}{8\pi}\tfrac{v_s^2}{4}\tfrac{(y^2+z^2)}{r_s^2}\,f'(r_s)^2$ — matching the closed form with **residual exactly 0**. Since the WEC demands $\rho\ge0$ for the Eulerian observer, and $\rho<0$ wherever $f'\neq0$, the WEC is violated in the bubble wall for **any** smooth bump. (Pfenning–Ford, reproduced symbolically in-repo.) | PASS | exact (sympy) |
| G2 | **Integrated slice energy is negative for every $v_s$ and scales as $-v_s^2$.** $E(v_s)=\int\rho\,d^3x<0$ at $v_s=\{0.25,0.5,1.0,3.0\}\,c_\text{lat}$, with $E(v_s)/(E(1)v_s^2)=1$ to $10^{-9}$. The sign is **velocity-independent**: even a *subluminal* $v_s<c_\text{lat}$ Alcubierre bubble needs negative energy in the wall. | PASS | numeric |
| PA1 | **Control (M3):** the F181 two-function kernel faithfully carries a *positive* source — a $1.06\,M_\odot$ star integrates to a valid metric with $\rho\ge0$, $\max\lvert AB-1\rvert=0.58$ inside ($\to0$ at the surface), and a monotone attractive lapse well. The kernel is **not** the obstruction. | PASS | numeric |
| PA3 | **Momentum density is co-supported with the negative wall.** Both $T^{0x}$ and $\rho<0$ are $\propto f'(r_s)^2$; support overlap $98.5\%$ on a test line. One cannot keep the warp momentum flux while discarding the negative-energy wall. | PASS | numeric |
| PC1 | **Speed limit (M4).** The induced isotropic field from a static positive source is well-posed ($A,B>0$, finite) with local propagation $c_\text{eff}=c_0\sqrt{A/B}\le c_\text{lat}$. The model's warp ceiling is $c_\text{lat}=1/\sqrt3\approx0.577$, and because $\rho_\text{wall}\propto-v_s^2$ only deepens with $v_s$, **no** $v_s$ opens a positive-source bubble. | PASS | numeric |

## The crux

The brief's fatal problem (its ranked #1) is confirmed exactly. Every genuinely **superluminal** member of the family (Alcubierre, Natário, contested-Lentz) requires a region of negative Eulerian energy density in the bubble wall — G1 derives this as an algebraic identity, $\rho\propto-f'^2$, not an order-of-magnitude estimate. The model's **M2** (F193: the gravitating source is the *beable* energy density, a sum of non-negative quadratic per-cell terms, with the $+\tfrac12\hbar\omega$ zero-point piece an explicitly non-gravitating superimposable) removes the one ingredient such a source needs — and removes it **more completely than standard QFT**, which permits bounded local negative energy (Casimir, squeezed states) under the Ford–Roman quantum inequalities. Here there is no negative-beable channel **at all**: the exclusion is "the sourcing mechanism does not exist," strictly stronger than the literature's "energetically prohibitive."

Two independent reinforcements: G2 shows the negative wall does not go away by dropping below $c$ (the sign is $\propto-v_s^2$, present for all $v_s$), so subluminality does not rescue the *Alcubierre* metric specifically; and PA1 establishes that the obstruction is the source **sign**, not the kernel — F181 carries positive/exotic (anisotropic) stress without complaint, so the model is flexible enough to represent the geometry, it simply cannot manufacture the required negative source.

## Verdict

- **Superluminal Alcubierre / Natário / contested-Lentz: STRUCTURALLY EXCLUDED** in this model — on grounds *stronger* than mainstream GR+QFT (no beable negative-energy or zero-point channel exists, M2/F193), in addition to the standard Ford–Pfenning quantum-inequality exclusion the model inherits for free.
- **Subluminal positive-energy family (Bobrick–Martire / Fuchs 2024): NOT EXCLUDED.** No model commitment forbids a $T^{00}\ge0$ source; PA1/PC1 show the kernel and the induced field handle it and remain well-posed. But these carry **no FTL utility** (subluminal by construction) and are capped at $c_\text{lat}=1/\sqrt3$ — because here the metric is *induced* from $c_\text{lat}$-bounded fields (M4), not an independently dynamical object, so there is no continuum-style "metric carries the ship FTL" loophole.

The net statement: the model is *more* hostile to warp-drive FTL than GR+QFT, for a clean and derived reason (M2), while still admitting the exotic-but-physical subluminal class as a statement about metric-engineering flexibility (inertial-shielding-type geometries), not faster-than-light travel.

## Open / next

**First construction of both open items done (2026-06-30 - 21:40, exploration `docs/design/warp-shift-vector-construction.md`, runner `tests/runners/run_warp_openitems_explore.py`).** The key move: the warp shift vector $N^i=g_{0i}$ is the *translational* analogue of Hartle's rotational frame-drag $\omega(r)$ (F185), so both items ride a single weak-field gravitomagnetic kernel $\nabla^2 N_i=-16\pi T^{0i}$ (free-space FFT). Results below; both remain pre-finding pending a nonlinear forward solve + dynamical IVP-break.

- **Problem #3 (superluminal shift well-posedness)** — two *computed* obstructions, both sharper than continuum GR: (1a) the beable lattice cell worldline $g_{00}=-(c_\text{lat}^2-v_s^2f^2)$ goes **null at exactly $v_s=c_\text{lat}$** and spacelike beyond, so no lattice rest frame exists inside a $\ge c_\text{lat}$ bubble (continuum GR's Eulerian-slicing escape is unavailable — the cells are fixed beables); (1b) the induced-metric signal cone is $c_\text{lat}$ (F180), so a $>c_\text{lat}$ bubble has no causal assembly. Still open: a *dynamically evolved* off-diagonal source through a hyperbolic kernel showing the IVP break live (the F181 "live two-grid" rung).
- **Forward Bobrick–Martire construction** — first (linearized) build done: a positive-$T^{00}$ shell translated at $v$ produces a real shift vector via the gravitomagnetic kernel, with **WEC holding everywhere** ($\min T^{00}=+2.4\times10^{-37}$, no negative wall) and a **partial** carry-along drag fraction $N_x/v\approx4(M/R_0)$ that reaches full co-motion only at strong field $M/R_0\sim O(1)$ — where the F204 nonlinear $-v_s^2$ wall returns. Confirms the subluminal class is realizable and FTL-less, consistent with F204. Still open: the *nonlinear* forward solve (full $G_{\mu\nu}$) and a quantitative match to the Fuchs "Warp Factory" target.

## Files
- Reuses module: `ca-simulation/ca_interior_metric.py` (F181)
- Test: `tests/findings/test_F200_alcubierre_structural.py`
- Results: `test-results/F200_alcubierre_structural.json`
- Brief: `docs/design/alcubierre-warp-structural-test.md`
- Open-items exploration: `docs/design/warp-shift-vector-construction.md` · runner `tests/runners/run_warp_openitems_explore.py`
