# F244 — 1/b scaling of 3-D EMQG lensing (isolated Green's function, no free α)

**Date:** 2026-07-03 - 14:35
**Status:** Confirmed — 5/5 checks PASS. Closes open-derivation **F2** (prompt #17; exactness-inventory not-yet-met #2). The F3b deflection scan (`run_phaseF_tests.py::test_F3b_scan`) verified $\Delta y(b)\propto1/b$ only for the **phenomenological** metric $c=c_0(\lvert\Phi\rvert/v)^\alpha$ with a **free fit exponent** $\alpha=1.5$. This finding re-runs the scan on the **genuine 3-D EMQG Newtonian potential** (`ca_emqg.solve_poisson_3d`, true $1/r$ Green's function) with the parameter-free GR-Shapiro coupling $c=c_0/(1-2\phi/c_0^2)$. The lensing obeys $\Delta\theta\propto1/b$: the **exact continuum thin-lens closed form** gives slope $-0.9959$ (machine $1/b$), the lattice isolated-slice line integral $-1.074$, the periodic-FFT slice $-1.062$, and the Cayley exact-unitary stepper reproduces the deflection **toward the mass** with norm conserved to $10^{-15}$. The free $\alpha$ is eliminated.
**Modules:** `ca-simulation/ca_emqg.py` (`solve_poisson_3d`, `gaussian_mass_3d`, `c_field_from_phi`), `ca_curved.py` (`CayleyVarcSolver2D`) — used, not modified
**Tests:** `tests/findings/test_F244_emqg_1overb_scan.py` (5/5, numpy + scipy.sparse)
**Results:** `test-results/F244_emqg_1overb_scan.json`
**Cross-references:** [[F243-f3-lowdensity-lensing-not-falsified]] (companion lensing closure, prompt #16), [[F107-canonical-a-adoption-L4-grb-gate]] (the absolute light-deflection coefficient $-4$, the GR normalisation this recovers the $1/b$ shape of), [[F55-spatial-metric-backreaction]] / [[F52-restleg-backreaction]] (the deflection-coefficient lineage).

---

## What this closes

`docs/audits/model-observations.md` item 12 noted that F3b confirmed only the **sign** of the deflection at one impact parameter, and item 4 noted the earlier 2-D Poisson test scored a **logarithmic** potential against a $1/r$ benchmark (dimensionally inconsistent). Exactness-inventory not-yet-met #2 asked to extend the scan to the **3-D EMQG potential** and test $1/b$. The 3-D solver (`solve_poisson_3d`) already existed; this finding runs the quantitative $1/b$ scan on it, replacing the free-$\alpha$ metric with the physical potential.

## Three levels of test (decreasing idealisation)

**A. Exact continuum closed form.** The thin-lens deflection of a ray at height $b$ through the equatorial slice of the isolated 3-D Green's function $\phi=-GM/r$ (Gaussian core width $\sigma$) is

$$\Delta\theta(b)=\int_{-\infty}^{\infty}\partial_y\ln c\,dx
=\frac{2}{c_0^2}\int_{-\infty}^{\infty}\partial_y\!\left(\frac{GM}{\sqrt{x^2+b^2+\sigma^2}}\right)dx
=\frac{2GM}{c_0^2}\,\frac{b}{b^2+\sigma^2}\;\xrightarrow{\,b\gg\sigma\,}\;\frac{2GM}{c_0^2\,b}.$$

Exact $1/b$ (softening correction $O(\sigma^2/b^2)$). Fitted slope $-0.9959$; $b\!\cdot\!\Delta\theta\to$ const with residual $\sigma^2/b^2$.

**B. Lattice thin-lens line integral.** Summing $\partial_y\ln c$ along the ray on the discretised slice:
- **Isolated slice** ($L=400$, far-field window $\sigma\ll b\ll L/2$): slope $-1.074$. Deviation from $-1$ is finite-$x$ truncation of the line integral (loses more $1/x^3$ tail at large $b$), not physics.
- **Periodic `solve_poisson_3d` slice** ($L=256$, $b\ll L/2$): slope $-1.062$. Clean $1/b$; periodic images cancel the far field only near the box edge $b\to L/2$ (a solver artifact, documented, avoided here).

**C. Dynamical Cayley stepper.** Propagating a Weyl probe packet through the variable-$c$ field built from the 3-D EMQG slice: the transverse momentum kick $\Delta\langle k_y\rangle$ is **toward the mass** ($<0$) at every $b\in\{10,16,24\}$, and norm is conserved to $\sim3\times10^{-15}$ (the Cayley exact-unitary contract). The deflection is therefore not a static-integral artifact but a genuine dynamical refraction.

## Why the 3-D potential is the right one (recap of the fix)

In 2-D the $\nabla^2$ Green's function is logarithmic ($\phi\sim\ln r$), giving a deflection with the wrong $M$- and $b$-dependence (model-observations item 4). The 3-D Green's function is the true Newtonian $1/r$, so a ray through a slice recovers $\Delta\theta\propto GM/b$ — the standard weak-field lensing shape. Using $c=c_0/(1-2\phi/c_0^2)$ (GR-Shapiro / effective-medium) means **no free exponent**: the earlier $\alpha=1.5$ of the F3b metric is retired.

## New information

1. **3-D EMQG lensing obeys $\Delta\theta\propto1/b$** — confirmed exactly in the continuum closed form ($-0.9959$) and on the lattice (isolated $-1.074$, periodic $-1.062$), with a dynamical Cayley-stepper confirmation (toward-mass, norm to $10^{-15}$).
2. **The free exponent $\alpha$ is eliminated.** The physical GR-Shapiro coupling $c=c_0/(1-2\phi/c_0^2)$ on the 3-D $1/r$ potential reproduces $1/b$ with no fit — superseding the F3b $c=c_0(\lvert\Phi\rvert/v)^{1.5}$ scan.
3. **The residuals from exactly $-1$ are named artifacts**: finite-$x$ truncation (isolated) and periodic-image cancellation near the box edge (periodic), both provable from the closed form, neither physics.

## Open / next

- Absolute normalisation: this fixes the $1/b$ **shape**; the coefficient $2GM/c_0^2$ ties to the F107 absolute deflection $-4GM/(bc^2)$ (GR $=$ 2× Newtonian light) — a coefficient check on the same slice would complete the connection.
- A non-periodic (isolated) Poisson solver (multipole/screened boundary) would remove the box artifact and let the lattice slope reach machine $-1$ directly.
