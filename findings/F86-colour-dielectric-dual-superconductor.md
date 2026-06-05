# F86 — Confinement as a colour-dielectric / dual superconductor (P1, Option C)

**Date:** 2026-06-03 - 23:58
**Status:** Confirmed — 6/6 PASS; CD1 algebraically exact (sympy), CD4 bit-for-bit, CD6 machine-ε, CD3 ODE-exact to 5e-6, CD2/CD5 quantitative.
**Modules:** `ca-simulation/ca_colour_dielectric.py` (new)
**Tests:** `model-tests/test_FG7d_colour_dielectric.py`
**Results:** `test-results/FG7d_colour_dielectric.json`
**Cross-refs:** F43 (dynamical SU(3) gluons + Wilson primitives), F64 (gravity dielectric — the structural template), F70 (2D-exact area-law σ — the complementary anchor), F26 (c = rotation rate), F71/F74 (baryon, downstream P2).

---

## What this closes

This is the build of **P1 Option C** from `roadmap-P1-binding-force-options.md`: the binding force as the **model-native** mechanism — the dual superconductor — recast in the model's own rotation-rate language as a **colour-dielectric** $\varepsilon_c(x)$ that renormalises the F43 gluon $(\mathbf E,\mathbf B)$-rotation rule, exactly parallel to F64's gravitational dielectric $K(x)$.

It does **not** replace F70 (2D-exact area law) or Option A/B (3+1D Monte-Carlo / Hamiltonian); it is the third, complementary route — the one that **unifies confinement with the F64 gravity mechanism under a single idea**: *a position-dependent renormalisation of the $(\mathbf E,\mathbf B)$ rotation rule*. The roadmap explicitly flagged this as "most novel and most consistent with the model's existing gravity/EM treatment … directly answers the notebook's BCS questions; no string theory."

## The one-paragraph physics

The QCD vacuum is a **colour-magnetic condensate**. By the **dual Meissner effect** it expels colour-**electric** flux, squeezing the field between a $q\bar q$ pair into a tube of fixed energy-per-length $\sigma$ → linear potential $V(R)=\sigma R$ → confinement. In the model's language the condensate is a **colour-dielectric** $\varepsilon_c(x)$: $\varepsilon_c\to 0$ in the condensed vacuum (flux expelled) and $\varepsilon_c\to 1$ in the normal tube core. This is the same object as F64's gravitational index $K(x)$ — both are a local renormalisation of the gluon/EM rotation rate — but in the **opposite impedance regime**:

| | F64 gravity dielectric | F86 confining dielectric |
|---|---|---|
| placement | $\varepsilon=\mu=K$, impedance-**matched** ($AB\equiv1$) | $\varepsilon_c$ only, impedance-**broken** |
| effect on field | transparent — **bends** light | **expels** colour-electric flux |
| consequence | GR lensing, redshift | flux tube, linear $V(R)$, confinement |

One mechanism, two regimes: the sign of the impedance mismatch separates "bend" from "confine".

## The mechanism is exactly solvable at the BPS point

The flux tube is the Abelian-Higgs / dual-Ginzburg–Landau (Abrikosov–Nielsen–Olesen) vortex in the transverse plane. Writing $\phi = v f(x)e^{in\theta}$ and the dual gauge profile $a(x)$ with $x=evr$, the energy per unit length at the **critical (BPS) coupling** completes to a sum of squares plus a total derivative:

$$\sigma = 2\pi v^2\!\int_0^\infty\! x\,dx\left[f_x^2 + \frac{n^2f^2(1-a)^2}{x^2} + \frac{n^2}{2x^2}a_x^2 + \tfrac12(f^2-1)^2\right].$$

The squares vanish on the **first-order Bogomolny equations**

$$f_x = \frac{n f(1-a)}{x},\qquad a_x = \frac{x}{n}\,(1-f^2),$$

leaving the **profile-independent topological result**

$$\boxed{\;\sigma_\text{BPS} = 2\pi v^2\, n\;}\qquad\text{(exact)},$$

because the cross terms integrate to $n\big[(1-a)(f^2-1)\big]_0^\infty = n$. The condensate VEV $v$ — the colour-magnetic order parameter — **sets the string tension**, which is precisely the roadmap's ask ("connect σ to the dielectric/condensate parameter").

Supporting scales, both verified:

- **Dual-London penetration depth** (tube radius / dual Meissner length): $\lambda = 1/(ev) = 1/m_V$.
- **Coherence length** (condensate healing): $\xi = 1/(\kappa e v)$.

## Test battery (6/6)

| Test | What it checks | Residual | Tier |
|------|----------------|----------|------|
| CD1 | Bogomolny completion: density $=$ squares $+\,ev^2B$ at $\lambda=e^2$ ⇒ $\sigma=2\pi v^2 n$ | $0.0$ (sympy, exact) | 1 |
| CD2 | ANO/DGL profile BCs ($f,a:0\to1$, monotone) + quantised flux $\Phi=2\pi n/e$ | $1.5\times10^{-4}$ | 3 |
| CD3 | numeric $\int(\text{energy density})$ on BPS profile $=2\pi v^2 n$ ($n=1,2$) | $4.6\times10^{-6}$ | 3 (ODE-exact) |
| CD4 | dielectric gluon step $\to$ free F43 step **bit-for-bit** at $\varepsilon_c=1$; renorm $c_\text{eff}=c\sqrt{\varepsilon_c}$ | $0.0$ bit-for-bit | 1 |
| CD5 | dual Meissner: London field decays with $\lambda=1/(ev)$ (2D $K_0$ prefactor removed) | $1.3\times10^{-2}$ | 3 |
| CD6 | constant cross-section ⇒ linear $V(R)=\sigma R$; isolated charge ($R\to\infty$) costs $\infty$ | $1.0\times10^{-14}$ | 1 |

**CD1** is the algebraic heart: the energy density rearranges, at the critical coupling $\lambda=e^2$, to $\tfrac12(B+e(|\phi|^2-v^2))^2 + |(D_1+iD_2)\phi|^2 + ev^2B$, so the tension is the topological $ev^2\Phi = ev^2(2\pi n/e)=2\pi v^2 n$ regardless of the detailed profile — done in exact symbolic arithmetic, not machine precision.

**CD4** is the F64-parallel certificate: with a trivial dielectric the gluon rotation step is *bit-for-bit* the free F43 propagator (`ca_gluon.gluon_rotation_step_spectral_2d`); a non-trivial $\varepsilon_c$ rescales the rotation angle $\Omega\to\Omega/\sqrt{\varepsilon_c}$, i.e. the lattice colour speed $c_\text{eff}=c_\text{lat}\sqrt{\varepsilon_c}$, the same renormalisation F64 applies to the EM rotation rule. As $\varepsilon_c\to 0$ the rotation freezes — the colour field cannot propagate into the condensed vacuum (confinement).

**CD6** is the confinement statement: the DGL solution is $z$-independent, so the tube cross-section (RMS radius) is $R$-independent and the energy is exactly proportional to length — $V(R)=\sigma R$, linear to $10^{-14}$, diverging as $R\to\infty$.

## How this sits against F70 and the other P1 options

- **F70** gives $\sigma$ from the **2D-exact area law** (Schur/Weyl-torus, strong-coupling, all $\beta$). **F86** gives $\sigma$ from the **dual-superconductor flux-tube tension** ($\sigma=2\pi v^2 n$, weak-coupling/condensate side). Two independent mechanisms, same observable (linear $V(R)$) — they bracket the confining regime from opposite couplings.
- **vs Option A (MC + multilevel):** F86 does **not** resolve the `run_confinement_mc.py` signal-to-noise wall — it *replaces* the Wilson-loop observable with the dielectric/flux-tube order parameter, sidestepping the wall rather than beating it. A is still the route if a rigorous 3+1D $\sigma$ from the gauge-loop ensemble is wanted.
- **vs Option B (Hamiltonian):** complementary; B's real-time flux tube and F86's dual-SC flux tube are the same colour-electric object from two formulations.
- **Feeds P2 (F71/F74 baryon):** supplies a concrete $\sigma(v)$ and a finite-energy binding argument — separating one quark costs $\sigma R\to\infty$ — exactly what Option D would borrow.

## Honest scope / open items

- **Critical (BPS) coupling.** The exact $\sigma=2\pi v^2 n$ is the type-I/II boundary value; for general $\kappa$ the tension is $\sigma=2\pi v^2 n\,\epsilon(\kappa)$ with $\epsilon(1)=1$, $\epsilon$ to be mapped numerically (the confinement statement $\sigma>0$ holds for all $\kappa$).
- **Colour-magnetic condensate assumed, not derived.** The dual-superconductor premise (monopole condensation) is **input**, as the roadmap warned ("needs the colour-magnetic condensate to be demonstrated, not assumed; highest research risk"). What F86 demonstrates is that *given* the condensate, the model's rotation-rate dielectric reproduces the flux tube, the exact tension, and the dual Meissner length — and unifies them with F64. **[Closed by F88, 2026-06-04]:** the condensate is now derived from the model — forced (Nielsen–Olesen instability of the trivial vacuum, sympy-exact, driven by the F43 structure constants; Savvidy minimum $B_\text{min}>0$ for all $g>0$) and identified (compact links ⇒ DeGrand–Toussaint monopoles ⇒ dual Meissner, with $v = m_D/e$ measured by MC). See `findings/F88-colour-condensate-from-model.md`.
- **Abelian projection.** The DGL vortex is the Abelian (dual-photon) reduction of SU(3); the full non-Abelian condensate is not solved here.
- **Uniform-$\varepsilon_c$ lattice step.** Part B's renormalised gluon tick is demonstrated for a *uniform* $\varepsilon_c$ (keeps it spectral and exactly unitary); the spatially-varying flux-expelling tick is represented analytically by the DGL profile (Part A) + London screening (Part C), not by a single variable-coefficient spectral step.

## Exactness-inventory additions

Tier 1 (algebraic / bit-for-bit): CD1, CD4, CD6 — 3 entries.
Tier 3 (numeric ODE / quantitative): CD2, CD3, CD5 — 3 entries (CD3 ODE-exact to $5\times10^{-6}$).
