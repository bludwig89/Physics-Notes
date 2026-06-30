# F182 — Cosmology under the F178 full-tensor source: pressure gravitates, so radiation enters the acceleration equation as ρ+3p=2ρ → standard Friedmann; the demoted energy-only law would have mis-weighted the early universe by exactly a factor 2

**Date:** 2026-06-30 - 02:45
**Numbering:** max existing F-number was F180 (`F180-gw-speed`); concurrently with `F181-covariant-interior-kernel-battery` (same session). This is **F182** (re-checked per CLAUDE.md).
**Status:** Confirmed — 6/6 checks PASS. Closes the third scoped follow-up of [[F178-gravity-full-tensor-adoption]] ("confirm cosmology: radiation now gravitates with pressure → standard Friedmann"). The field-equation/consistency statements (A1, A2) are **exact (sympy, zero residual)**; the textbook power-law solutions (N1, N2) and the consistency ratio (N4) run to numerical precision.
**Module:** `ca-simulation/ca_cosmology.py`
**Script:** `tests/findings/test_F182_friedmann_pressure.py` (~5 s; numpy + local RK4 + sympy)
**Results:** `test-results/F182_friedmann_pressure.json`
**Cross-references:** [[F178-gravity-full-tensor-adoption]] (the decision this confirms), [[F173-pressure-tolman-discriminator]] (the same omitted fraction $3w/(1+3w)$, here in cosmology), [[F180-gw-speed]] (the other full-tensor consequence — $c_{\rm grav}=c_{\rm lat}$), [[F106-psi-K-sourcing-derivation]] (the energy-only law now confined to the static weak field), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the $\Lambda$ sector). Papers: `Paper-07-Gravity.md`, `Paper-12-Unification-Rotation-Currency.md`.

---

## What F178 forced in cosmology

For a flat FLRW metric $ds^2=-c^2dt^2+a(t)^2\,d\mathbf x^2$, the induced Einstein equation gives the standard Friedmann pair
$$H^2=\Big(\frac{\dot a}{a}\Big)^2=\frac{8\pi G}{3}\rho\quad(G^0{}_0),\qquad
\frac{\ddot a}{a}=-\frac{4\pi G}{3}\Big(\rho+\frac{3p}{c^2}\Big)\quad(G^i{}_i),$$
with continuity $\dot\rho+3H(\rho+p/c^2)=0$. The acceleration equation carries the **$\rho+3p$** combination — pressure gravitates (the Tolman term). The *energy-only* law that F178 demotes would read $\ddot a/a=-(4\pi G/3)\rho$, dropping $3p$ — exactly the same omission F173 found in the neutron-star interior, now in the early universe.

## Checks (6/6)

| # | Check | Result | Tier |
|---|---|---|---|
| A1 | Friedmann I + continuity **force** $\ddot a/a=-(4\pi G/3)(\rho+3p/c^2)$: differentiating $H^2=(8\pi G/3)\rho$ and substituting continuity yields $\ddot a/a=-4\pi G\rho(1+3w)/3$ exactly. The energy-only form $-(4\pi G/3)\rho$ is consistent **only if $p=0$** (Bianchi identity rejects it for $w\neq0$). | PASS | exact (sympy) |
| A2 | Energy-only law omits the source fraction $3w/(1+3w)$ — **$\tfrac12$ for radiation** ($w=\tfrac13$), $0$ for dust — identical to the F173 interior result. | PASS | exact (sympy) |
| N1 | **Radiation** ($w=\tfrac13$): $a\propto t^{1/2}$ (fitted exponent $0.49999$) and $\rho\propto a^{-4}$ (slope $-4.0000$). | PASS | numeric |
| N2 | **Matter** ($w=0$): $a\propto t^{2/3}$ (fitted exponent $0.66666$) and $\rho\propto a^{-3}$ (slope $-3.0000$). | PASS | numeric |
| N3 | Deceleration parameter $q=-\ddot a a/\dot a^2$: full-tensor gives $q=\tfrac12(1+3w)$ — **radiation $q=1$**, matter $q=\tfrac12$; the energy-only law gives $q=\tfrac12$ for both → radiation mis-weighted (1 vs $\tfrac12$). | PASS | exact |
| N4 | Numerical $\ddot a/a$ of the Friedmann-I solution in the radiation era matches the full-tensor $-(4\pi G/3)(\rho+3p)$ to $3\times10^{-7}$, and equals **exactly $2\times$** the energy-only $-(4\pi G/3)\rho$. | PASS | numeric |

**Overall 6/6 PASS.**

## Why this matters — the mis-weighting is real and quantified

The deceleration of the radiation-dominated universe is set by $\rho+3p=2\rho$, twice the energy density alone. The demoted energy-only law (the literal F106 reduction) would have used $\rho$ only, halving the source: it predicts $q=\tfrac12$ in the radiation era where the correct value is $q=1$ (N3), and its acceleration is a factor $(\rho+3p)/\rho=2$ too small (N4). Because the radiation era sets the expansion rate during Big-Bang nucleosynthesis and the radiation–matter transition, this factor-2 error would have mis-timed the early universe. The full-tensor source removes it automatically: A1 shows the $\rho+3p$ term is **not optional** — it is forced by the Bianchi identity (consistency of Friedmann I with energy conservation), so the energy-only law is not merely disfavoured but internally inconsistent for any $p\neq0$.

This is the cosmological counterpart of F173 (neutron-star interior) and F180 (gravitational-wave speed): three independent sectors in which committing to the full stress-energy source gives the standard, observationally-correct result, whereas the energy-only single-scalar reduction would have departed by an $O(3p/\rho c^2)$ — here exactly factor 2.

## Honest scope

The Friedmann pair itself is textbook GR; what this finding establishes is that the **model's adopted source** (F178) reproduces it, including the pressure weighting, and that the *previous* energy-only law would not have — quantified exactly ($q$, the factor 2, the omitted fraction $3w/(1+3w)$). The dark-energy/$\Lambda$ magnitude is a separate, unsolved problem (F164) and is not addressed here; this finding sets $\Lambda=0$ and treats single-component flat universes.

## Open / next

- **Multi-component + $\Lambda$:** radiation→matter→$\Lambda$ transition redshifts $z_{\rm eq}$, $z_{\rm acc}$ on the same integrator (mechanical given N1–N4).
- **Perturbations:** the pressure term also enters the growth equation; a Jeans/growth check is the next rung.
- Tie-in with [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] for the vacuum-energy sign and magnitude.

## Files
- Module: `ca-simulation/ca_cosmology.py`
- Test: `tests/findings/test_F182_friedmann_pressure.py`
- Results: `test-results/F182_friedmann_pressure.json`
