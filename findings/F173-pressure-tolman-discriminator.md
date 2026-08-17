# F173 — The pressure/Tolman discriminator: the single-scalar dielectric sources gravity from energy density only, omitting GR's 3p term — null in the solar system, but a 2–42% departure inside neutron stars

> **[PARTIALLY SUPERSEDED 2026-06-29 by F178 — ledger S4-F178-full-stress-energy]**
>
> **DEAD:** The energy-only vs rho + 3p departure read as a physical DISCRIMINATOR between the model and GR. Under the full-tensor source it is a weak-field- reduction artifact of the demoted single-scalar law.
>
> **STILL LIVE:** The exact tensor algebra, in full -- it is what MOTIVATED F178, and the anisotropic-stress result is the reason the interior carries a second metric function.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-06-29 - 19:10
**Numbering:** drafted as F170→F171→F172 all collided with concurrent sessions (`F170-lepton-colour-scale-link`, `F172-residual-algebraic-or-computed`); this is **F173** (re-checked max F-number per CLAUDE.md).
**Status:** Confirmed — 4/4 checks PASS. The mechanism (Parts A/P1–P2) is **exact** (sympy zero residual); the field-equation statement (P3) is exact algebra; the strong-field magnitude (P4) has an **exact** leading coefficient (−15/4) with the neutron-star percentages quoted as illustrative (uniform-sphere model, full nonlinear stellar solve open).
**Discriminator:** this is the **first identified place the model departs from general relativity itself** (not merely from the Standard Model) — a sharp, potentially-falsifiable prediction.
**Module:** `ca-simulation/ca_tolman.py`
**Script:** `tests/findings/test_F173_tolman_pressure.py` (~5 s, sympy + mpmath)
**Results:** `test-results/F173_tolman_pressure.json`
**Falsification brief:** `tests/falsification/FC09-neutron-star-pressure-redshift.md`
**Cross-references:** [[F64-em-connection-gravity]] (the dielectric metric A=1/K, B=K, AB≡1), [[F106-psi-K-sourcing-derivation]] (the ∇²lnK = −(8πG/c⁴)T⁰⁰ law this probes), [[F114-dielectric-black-hole]] (the O(1) strong-field departure in the exterior; this is its interior counterpart), [[FA09-light-deflection-coefficient]] / PPN β=γ=1 (the exterior agreement preserved). External: Tolman 1930 / Whittaker 1935 (pressure gravitates); MICROSCOPE & LLR (the EP confirmations, FC08).

---

## The question (the open item from FC08)

In general relativity the source of the **time** potential — the one that sets clock rate, gravitational redshift, and slow-particle orbits — is the trace-reversed stress-energy:

$$\nabla^2\Phi = \frac{4\pi G}{c^2}\big(\rho + 3p/c^2\big)\qquad(\text{GR, static weak field}).$$

Pressure gravitates: the "3p" Tolman term. The F64/F106 dielectric instead sources a **single scalar** K from the energy density alone, ∇²ln K = −(8πG/c⁴)T⁰⁰. A single scalar cannot independently carry GR's two interior metric functions, so the question is sharp: **does the dielectric reproduce the +3p Tolman source, or omit it?** FC08 left this as the one place a GR-vs-model discriminator could live. This finding computes it.

## Part A — what source the dielectric metric actually carries (exact)

The exact Einstein tensor of the isotropic dielectric metric

$$ds^2 = -\tfrac1K\,dt^2 + K\,(dr^2 + r^2 d\Omega^2),\qquad K=e^{2u(r)},$$

has mixed components (sympy, zero residual):

$$8\pi\rho_\text{eff} = -e^{-2u}\Big(u'^2 + 2u'' + \tfrac{4}{r}u'\Big),\qquad
8\pi p_r = -e^{-2u}u'^2,\qquad 8\pi p_t = +e^{-2u}u'^2.$$

Two exact facts follow:

1. **Leading order = F106 (P1).** $8\pi\rho_\text{eff} = -\nabla^2(\ln K) + O(u'^2)$: the remainder vanishes identically when $u'=0$, so the F106 law ∇²ln K = −8πρ is the leading term, dressed by second-order $e^{-2u}u'^2$ field-energy corrections.
2. **Only anisotropic field stress; no matter pressure (P2).** The single scalar carries $p_r=-p_t=-e^{-2u}u'^2/8\pi$ — an *anisotropic* stress quadratic in the field gradient (the gravitational field's own stress, present in vacuum too). It carries **no isotropic matter-pressure source**. A perfect fluid has $p_r=p_t$; the dielectric forces $p_r=-p_t$. Matter pressure $p$ is therefore **absent from the source**.

## Part B — the field-equation statement and its magnitude

**The clean statement (P3).** GR sources Φ by $\rho+3p/c^2$; the dielectric by $\rho$. For an equation of state $p=w\rho c^2$ the model **omits the fraction**

$$\frac{3w}{1+3w}\quad\text{of GR's time-potential source:}\quad
\begin{cases} w=0\ (\text{dust}) & 0\ \ (\text{model}=\text{GR})\\ w=0.1\ (\text{NS}) & 0.23\\ w=\tfrac13\ (\text{radiation}) & 0.50\\ w=1 & 0.75.\end{cases}$$

**Exterior fields agree — so every solar-system test is untouched.** Both theories give exterior mass $M=\int\rho\,dV$ (pressure does not enter the exterior of a bounded static body in either; the Tolman 3p is cancelled by the binding/wall stresses). Hence β=γ=1, light bending, Shapiro delay, perihelion (FA09/FC01) are **identical**. The departure is purely **interior / strong-field**.

**The magnitude (P4).** For a uniform-density sphere the central time-dilation $\sqrt{-g_{tt}(0)}$ diverges from GR at second order in the compactness $s\equiv GM/Rc^2$, with the **exact** leading coefficient

$$g_{tt}^\text{model}(0)-g_{tt}^\text{GR}(0) = -\tfrac{15}{4}\,s^2 + O(s^3).$$

The fractional difference in central time-dilation:

| object | $s=GM/Rc^2$ | (model−GR)/GR |
|---|---|---|
| Sun | $2.1\times10^{-6}$ | $8.4\times10^{-12}$ (null) |
| white dwarf | $3\times10^{-4}$ | $1.7\times10^{-7}$ |
| neutron star (low) | $0.1$ | $2.3\%$ |
| neutron star | $0.2$ | $11.9\%$ |
| neutron star (high) | $0.3$ | $42\%$ |

## Checks (4/4)

| # | Check | Result | Tier |
|---|---|---|---|
| P1 | $8\pi\rho_\text{eff}=-\nabla^2\ln K + O(u'^2)$; remainder vanishes at $u'=0$ | PASS | exact (sympy) |
| P2 | $p_r+p_t=0$ and $p_r=-e^{-2u}u'^2/8\pi$ exactly; no isotropic matter-pressure source | PASS | exact (sympy) |
| P3 | omitted source fraction $=3w/(1+3w)$ (dust 0, radiation 0.5) | PASS | exact algebra |
| P4 | leading coefficient $=-15/4$ exactly; Sun $8\times10^{-12}$ (null), NS$_{0.2}$ $11.9\%$ | PASS | exact coeff + quantitative |

## Verdict

A single impedance-locked scalar reproduces GR **exactly in the exterior** (preserving β=γ=1 and all weak-field/solar-system tests) but **cannot** carry the matter-pressure (Tolman) source. The dielectric gravity is therefore **not** globally GR-identical: it sources the time potential from energy density alone, omitting $3p$. The departure is:

- **null** wherever $p\ll\rho c^2$ — the solar system ($\sim10^{-11}$), explaining why every classical test passes;
- **order $3p/\rho c^2$** inside relativistic matter — **2–42% for neutron-star interiors**, order-unity for radiation-dominated matter.

This is the first concrete prediction on which the model and GR **diverge**, and it is confrontable with neutron-star data (surface-redshift–vs–mass, mass–radius, moment of inertia). It is a genuine falsifier in both directions: if NS observables match GR's pressure-sourced structure to better than the predicted $O(3p/\rho c^2)$, the single-scalar dielectric is falsified; if a systematic, compactness-correlated departure of the predicted sign appears, it is striking support.

## Open / next

- **Self-consistent stellar structure.** The uniform-sphere number combines the missing-pressure source with the exponential-vs-Schwarzschild interior form. A fully self-consistent comparison needs each theory's own hydrostatic equation (GR-TOV vs the dielectric's ∇²Φ=4πρ with $dp/dr=-\rho\,d\Phi/dr$) solved for a realistic EoS, giving a mass–radius curve to overlay on NICER data. This converts the illustrative 2–42% into a quantitative observable. High value.
- **Possible rescue / refinement.** Whether the model can recover the 3p term by promoting the source to the full induced $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$ (abandoning the single-scalar AB≡1 lock inside matter) is the theoretical fork — but that would sacrifice the parsimony that motivated F64. Either the model accepts a falsifiable NS departure, or it gives up one-field gravity in the interior.
- **Cosmology.** Radiation domination ($w=1/3$) omits half the source — the early-universe / Friedmann sector is the other regime where $O(1)$ departures would appear; worth a separate finding.

## Files
- Module: `ca-simulation/ca_tolman.py`
- Test: `tests/findings/test_F173_tolman_pressure.py`
- Results: `test-results/F173_tolman_pressure.json`
- Brief: `tests/falsification/FC09-neutron-star-pressure-redshift.md`
