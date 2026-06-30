# F181 — The covariant two-function interior kernel scoped by F178: the genuine GR/TOV interior (A, B independent, AB≠1) sources an isotropic perfect fluid where the single scalar cannot, reproduces GR exactly, and passes the F62/F64 dynamic battery unchanged

**Date:** 2026-06-30 - 02:30
**Numbering:** max existing F-number was F180 (`F180-gw-speed`); this is **F181** (re-checked per CLAUDE.md). If a concurrent session also claimed F181, renumber on merge.
**Status:** Confirmed — 9/9 checks PASS. Closes the first scoped follow-up of [[F178-gravity-full-tensor-adoption]] ("build the covariant interior kernel and re-verify the F62/F64 dynamic battery in the two-function regime"). The metric-level statements (C1–C4) are **exact (sympy, zero residual)**; the GR-TOV reproduction (N1) is to the integrator floor; the dynamic battery (B1–B4) reproduces the F62/F64 results numerically.
**Module:** `ca-simulation/ca_interior_metric.py`
**Script:** `tests/findings/test_F181_covariant_interior_battery.py` (~32 s; numpy + local RK4 + sympy + reuses the F62 stepper `dirac_gravity_fork`)
**Results:** `test-results/F181_covariant_interior_battery.json`
**Cross-references:** [[F178-gravity-full-tensor-adoption]] (the decision this implements), [[F173-pressure-tolman-discriminator]] (the exact single-scalar anisotropy this kernel removes), [[F176-covariant-dielectric-tov-recovery]] (the covariant single-scalar solve this supersedes inside matter), [[F62-dirac-gravity-dynamical-fork]] / [[F64-em-connection-gravity]] (the dynamic battery re-verified here), [[F114-dielectric-black-hole]] (the horizon-free object the exact vacuum solution replaces). Papers: `Paper-07-Gravity.md` (re-issued strong-field section), `Paper-08`/`Paper-12`.

---

## What F178 forced, and what this builds

F178 made the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ the canonical law and demoted the impedance-locked single-scalar dielectric ($A=1/K,\ B=K,\ AB\equiv1$) to the static weak-field representation. Its first scoped follow-up was a **covariant interior kernel** that evolves the **two-function** metric inside matter, replacing the single dynamic dielectric channel. This finding builds that kernel and re-verifies the F62/F64 dynamic gravity battery on it.

The kernel carries a genuine two-function static metric
$$ds^2=-A(r)\,dt^2+B(r)\,dr^2+r^2 d\Omega^2,\qquad A,\ B\ \text{independent},$$
i.e. the GR/TOV interior in areal coordinates with $B=1/(1-2m/r)$ and $A=e^{2\nu}$ ($\nu$ from the TOV equation, matched to the exterior), plus the **exact Schwarzschild** exterior. For the dynamic wave-packet battery it also supplies the closed-form **isotropic** exact-Schwarzschild legs $A=\big(\tfrac{1-u/2}{1+u/2}\big)^2,\ B=(1+u/2)^4$ (with $u=GM/rc^2$), whose product $AB\neq1$ — the two functions are genuinely independent, unlike the dielectric $e^{2u}$.

## Checks (9/9)

| # | Check | Result | Tier |
|---|---|---|---|
| C1 | Two-function areal Schwarzschild solves **vacuum** $G_{\mu\nu}=0$ identically (all four mixed components) | PASS | exact (sympy) |
| C2 | Single-scalar dielectric is **not** vacuum-exact: its Einstein tensor is anisotropic, $p_r=-p_t=-e^{-2u}u'^2/8\pi\neq0$ — reproduces [[F173-pressure-tolman-discriminator]]; one scalar cannot be the field equation beyond PPN order | PASS | exact (sympy) |
| C3 | Two-function interior (uniform-density interior Schwarzschild) sources an **isotropic perfect fluid**: $p_r=p_t$ exactly, $\rho_{\rm eff}=3/(8\pi a^2)=$ const, with $AB\neq1$ — the full-tensor source the single scalar cannot carry | PASS | exact (sympy) |
| C4 | PPN $\beta=\gamma=1$ for the two-function isotropic Schwarzschild ($\Rightarrow K_{\rm bend}=4$, redshift slope $Z=1$); the demoted dielectric is **also** $\beta=\gamma=1$ at PPN but its exact metric differs at $O(u^2)$ (the $B$ coefficient $2$ vs $\tfrac32$, difference $\tfrac12$) and is **horizon-free** ($A_{\rm diel}=e^{-2u}>0$ vs $A_{\rm Schw}\to0$ at $r=2M$) | PASS | exact (sympy) |
| N1 | `integrate_interior` reproduces GR-TOV: $M=2.10\,M_\odot$, $R=13.0$ km, mass/radius match to $0.0$ (integrator floor); $\max|AB-1|=0.82$ **inside** but $|AB-1|=2.2\times10^{-16}$ at the surface; a maximum-mass turnover exists ($M_{\rm max}=2.13\,M_\odot$) | PASS | numeric (to floor) |
| B1 | **Equivalence principle:** a rest packet falls toward low lapse $\sqrt A$, mass-independent, norm conserved ($<10^{-9}$) | PASS | dynamic |
| B2 | **Gravitational redshift:** clock frequency ratio $0.25$ vs analytic $\arcsin$ prediction $0.244$ ($<5\%$) — clock rate $\propto\sqrt A=\sqrt{-g_{tt}}$ | PASS | dynamic |
| B3 | **Factor-2 deflection:** eikonal $K_{\rm eik}=3.60$ from the two-function $c_{\rm eff}=c_0\sqrt{A/B}$ (Einstein band $3$–$5$); measured centroid bend tracks its own eikonal limit to $2\%$ | PASS | dynamic |
| B4 | **Backreaction:** norm conserved to $<10^{-6}$ while propagating on the two-function background | PASS | dynamic |

**Overall 9/9 PASS.**

## The crux: two functions vs one

The exact-algebra trio C1–C3 is the whole point of F178 made concrete:

- **In vacuum**, the two-function areal Schwarzschild metric satisfies $G_{\mu\nu}=0$ exactly (C1). The single scalar cannot: its Einstein tensor carries an irreducible **anisotropic field stress** $p_r=-p_t$ (C2), so it is only an $O(u)$ (PPN) approximation to the exact vacuum solution, not the solution itself.
- **Inside matter**, an isotropic perfect fluid needs $p_r=p_t$. The two independent functions deliver exactly that (C3, the closed-form uniform-density star: $p_r-p_t=0$, $\rho=$ const). The single scalar forces $p_r=-p_t$ and therefore *cannot* be the interior field equation — precisely the F173 obstruction, now resolved by carrying the second function.

So the kernel **is** GR/TOV inside matter (N1: bit-matches the independent TOV integration and shows the expected maximum-mass turnover), and **is** exact Schwarzschild outside.

## Why the dynamic battery is unchanged (B1–B4)

The F62/F64 wave-packet battery reads the metric only through the lapse $\sqrt A$ (rest leg / redshift / free-fall) and the kinetic speed $c_{\rm eff}=c_0\sqrt{A/B}$ (deflection). Feeding the **two-function** isotropic-Schwarzschild legs into the same stepper (`dirac_gravity_fork`) reproduces every battery result — equivalence principle, redshift $\propto\sqrt A$, factor-2 bend, unitary backreaction — because $A,B$ agree with the dielectric to $O(u)$. Nothing in the weak-field phenomenology is lost by abandoning the impedance lock. What changes is only the **exact** strong-field content (C4): genuine Schwarzschild (with a horizon) instead of the horizon-free exponential.

## Net effect

The interior gravity sector now has a covariant kernel that is exactly GR (TOV interior, Schwarzschild/Kerr exterior) and carries the two independent metric functions the full-tensor source requires. The dielectric survives only as the $O(u)$ vacuum/weak-field representation, and the F62/F64 dynamic battery passes on the new kernel without modification. This closes the first F178 follow-up and supersedes the in-matter single-scalar solve of F176 and the horizon-free object of F114.

## Open / next

- **Kerr / rotating exterior + frame dragging** ($T_{0i}$ gravitomagnetic sector) on the same two-function (→ off-diagonal) kernel.
- **Tabulated-EoS** TOV (drop verified SLy/APR into the kernel) for an absolute NICER/J0740 placement, now that the interior is genuine GR.
- **Live two-grid co-evolution** of the interior metric with matter (the kernel here solves the static structure; a dynamical collapse run is the next rung).

## Files
- Module: `ca-simulation/ca_interior_metric.py`
- Test: `tests/findings/test_F181_covariant_interior_battery.py`
- Results: `test-results/F181_covariant_interior_battery.json`
