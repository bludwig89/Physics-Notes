# F142 — The dielectric tube cannot carry $2\pi v^2 n$ exactly (it has no winding); the exact map is the centre route, and the non-Abelian condensate is solvable only in its centre content

**Date:** 2026-06-11 - 21:30
**Status:** Theoretical (no-go proven) + numerical demonstration — Q1 answered with an exact obstruction, Q2 answered as a scope theorem. T1 algebraic (bag dictionary + prefactor $1/\sqrt2$, exact); T2 the spreading no-go ($\sigma\propto A^{-1/3}\to0$) analytic + numeric ($\sigma\propto L^{-2/3}$, matches to <2%); T3 SU(3) Casimir/$k$-string ratios exact group theory.
**Module:** `ca-simulation/derive_dielectric_noconfine.py` (new; self-checking).
**Cross-references:** [[F139-self-consistent-dual-gl-backreaction]] (the §6 open edge this resolves), [[F86-colour-dielectric-dual-superconductor]] ($\sigma=2\pi v^2 n$, the ANO/BPS target), [[F99-sigma-as-centre-lagrange-multiplier]] (the *exact* map that already exists — $\sigma_k=-\ln s_k$), [[F88-colour-condensate-from-model]] (the condensate is forced — Savvidy/Nielsen–Olesen), [[F94-lattice-gauge-mc-confinement-vs-F86]] (the 3+1D $\sigma$ that still needs MC), [[F70-gradient-flow-confinement-string-tension]] (2D-exact area law).

---

## 1. The two questions (from F139 §6)

F139 closed the self-consistent dual-GL back-reaction but left two threads explicitly open:

> *"mapping the dielectric-model tension onto $2\pi v^2 n$ is the natural next sharpening … The full non-Abelian condensate (beyond the Cartan-dominated octet projection) is likewise not solved here."*

**Q1.** Can the F139 colour-dielectric (Friedberg–Lee) tube — $\varepsilon_c(f)=1-f^2$, quartic bag $\tfrac1{4\xi^2}(f^2-1)^2$ — be mapped onto F86's exact $\sigma=2\pi v^2 n$ with **algebraic exactness**?

**Q2.** Can the **full non-Abelian** condensate be solved / algebraically derived?

The answers are sharp: **Q1 — no, not through the dielectric tube** (a structural obstruction, proved below); the exact map already exists by a *different* route (F99). **Q2 — the condensate is solvable exactly only in its centre-projected (N-ality) content**; its dynamical magnitude in 3+1D is the open confinement problem.

---

## 2. Q1 — the dielectric tube has the right scaling but cannot reach $2\pi v^2 n$

### T1 — the dual-superconductor dictionary and the bag prefactor (algebraic)

Map the F86 dual-superconductor parameters onto the F139 dielectric bag at the BPS point ($\kappa=1$, $\lambda_{\rm pen}=\xi=1/ev$):

$$B=\frac{e^2v^4}{4}\ \ (\text{bag constant} = \text{potential at the melted core}),\qquad \Phi=\frac{2\pi n}{e}\ \ (\text{quantised colour-electric flux}).$$

The longitudinal electric tube's transverse profile balances core field energy against bag pressure. Its thin-wall (sharp-bag) tension is the standard MIT result

$$\sigma_{\rm FL}=\Phi\sqrt{2B}=\frac{2\pi n}{e}\cdot\frac{ev^2}{\sqrt2}=\frac{1}{\sqrt2}\,\big(2\pi v^2 n\big).$$

So the dielectric tube reproduces the **scaling** $\sigma\propto v^2 n$ exactly, but with prefactor $1/\sqrt2\approx0.707$, **not** $1$. The wall (gradient) energy raises this, but there is no algebraic reason it lands on exactly $2\pi v^2 n$ — and, worse, the next result shows there is no fixed continuum value at all.

### T2 — the no-go: the continuum $\varepsilon_c=1-f^2$ electric tube does not confine

Consider the "spread-thin" configuration: a uniform $f=1-\delta$ over transverse area $A$ (instead of a localised tube). With $\varepsilon_c=1-f^2\simeq2\delta$ and the flux fixed,

$$\sigma_{\rm spread}(A)=\underbrace{\frac{\Phi^2}{4A\delta}}_{\text{field}}+\underbrace{4B\delta^2 A}_{\text{bag}},\qquad \text{minimised at } \delta^3=\frac{\Phi^2}{32BA^2}\ \Rightarrow\ \boxed{\;\sigma_{\rm spread}\propto A^{-1/3}\to0\;}.$$

The flux escapes by spreading infinitely thin: buying conductivity $\varepsilon_c\sim2\delta$ costs only $\sim4B\delta^2$, so the cost-per-conductivity $\sim2B\delta\to0$. **There is no finite continuum tension to match.** F139's "constant tension to a factor 1.23" is therefore a **regulator artifact** — it survives only because F139 runs in a finite box ($L=16$) with a dielectric floor ($\varepsilon_{\rm floor}=10^{-2}$); remove the regulators and the tension bleeds to zero.

Confirmed two ways in `derive_dielectric_noconfine.py`:
- the analytic decade ratio $\sigma(A)/\sigma(10A)=10^{1/3}=2.1544$ to machine precision;
- a direct gradient-flow minimisation at fixed $\Phi=12$ in a growing box, whose tension **falls** as $L^{-2/3}$: $\sigma(L{=}61,91,141,201)=1.37,1.04,0.77,0.61$, matching the $L^{-2/3}$ law $1.37,1.05,0.79,0.62$ to $<2\%$. A confining functional would give an $L$-independent $\sigma$; this one does not.

### T3 — why: the exactness lives in a winding the dielectric model does not have

$\sigma=2\pi v^2 n$ is the **topological charge of the magnetic ANO vortex**: the condensate phase $\phi=vf\,e^{in\theta}$ winds $n$ times, the Bogomolny cross-terms integrate to the boundary value $n\big[(1-a)(f^2-1)\big]_0^\infty=n$ (F86 CD1), and $f\to v$ is **pinned at infinity by topology** — the field *cannot* spread. The F139 tube carries its flux as a **source charge** with no winding; $f$ is not topologically pinned, so the spreading mode of T2 is open. The integer $n$ in $2\pi v^2 n$ is a *winding number*; the dielectric tube's flux is a *continuous* $\Phi$ with no quantisation. **The exactness is structurally absent from the electric formulation.**

### T4 — the map that IS algebraically exact already exists (F99)

The exact bridge to $2\pi v^2 n$ does not run through the dielectric tube at all — it runs through the **centre algebra**. F99 derived (sympy-exact)

$$\sigma_k=-\ln s_k,\qquad s_k=\frac{z(2\pi k/N)}{z(0)},$$

as the constrained free energy whose Lagrange multiplier is the ’t Hooft centre twist $\theta_k=2\pi k/N$. In the small-$\sigma$ / Abelian-BPS limit $s_k=1-\varepsilon_k$, $\sigma_k=-\ln(1-\varepsilon_k)\simeq\varepsilon_k$, and with only the unit centre charge excited $\varepsilon_k\propto k$:

$$\sigma_k=2\pi v^2\,k,\qquad 2\pi v^2:=\sigma_1.$$

This **is** F86's $\sigma=2\pi v^2 n$, recovered exactly — but as the **linearisation of the centre free energy**, with $2\pi v^2$ the *definition* of the unit-charge tension, not as the saturated tension of an electric dielectric tube. The dielectric tube (F86/F137/F139) is the **regulated, qualitative real-space picture** of confinement; the centre weight (F99) is the **exact** one.

**Q1 verdict.** The dielectric-model tension **cannot** be mapped onto $2\pi v^2 n$ with algebraic exactness — the continuum functional does not confine, and the topological winding that makes $2\pi v^2 n$ exact is absent. The exact map is F99's $\sigma_k=-\ln s_k$, whose Abelian-BPS limit reproduces $2\pi v^2 n$ by construction. F139's tube remains the correct *dynamical real-space realisation* (it cures the pinch, gives the right scaling), regulated by box + floor.

---

## 3. Q2 — the full non-Abelian condensate: a scope theorem

"Solved in closed form" — **no**: the dynamical magnitude of the SU(3) condensate (the VEV $v$, the absolute $\sigma$ in 3+1D) is the confinement mass-gap problem and has no algebraic solution in this (non-supersymmetric) model; it needs the gauge Monte-Carlo (F94, Option A). What **is** algebraically derivable is precisely the **centre-projected content**, and it is rep- and dimension-independent:

**N1 — existence is forced (exact).** F88 proved (sympy, SU(2)) that the trivial gluon vacuum is unstable — the Savvidy/Nielsen–Olesen tachyon $\gamma^2=+gB$ from the $f^{abc}$ self-coupling — with a condensation minimum $B_{\min}>0$ for **every** $g>0$. The same mechanism forces the SU(3) condensate; condensation is not optional.

**N2 — the centre/N-ality classification is exact (F99, rep- and $D$-independent).** Asymptotic $\sigma$ depends **only** on N-ality: $\sigma_0=0$ (closure ⇒ no price), $\sigma_k>0$ off closure, and $\sigma_k=\sigma_{N-k}$ ($k\leftrightarrow N-k$ string degeneracy). This is the $\mathbb Z_N$ centre algebra of the update rule, not a dynamical input.

**N3 — Casimir scaling at intermediate distance (exact group theory).** $\sigma_R/\sigma_F=C_2(R)/C_2(F)$ with the SU(3) quadratic Casimirs ($C_2(\mathbf3)=4/3$):

| rep $R$ | $C_2(R)$ | $\sigma_R/\sigma_F$ |
|---|---|---|
| $\mathbf 3,\ \bar{\mathbf 3}$ (fund) | $4/3$ | $1$ |
| $\mathbf 8$ (adj) | $3$ | $9/4$ |
| $\mathbf 6$ | $10/3$ | $5/2$ |
| $\mathbf{10}$ | $6$ | $9/2$ |

**N4 — the SU(3) $k$-string spectrum is fixed, the universal law is not (exact where it bites).** Both candidate asymptotic laws — Casimir $\sigma_k\propto k(N-k)$ and sine $\sigma_k\propto\sin(k\pi/N)$ — give $\sigma_2/\sigma_1=1$ for SU(3), because the $k{=}2$ string is the antifundamental (N-ality $-1$). So the model fixes the SU(3) $k$-spectrum **exactly** ($\sigma_2=\sigma_1$), consistent with everything F97/F98/F99's closure principle needs, but cannot distinguish the two laws — they split only for $N\ge4$. (This is exactly F99's "A-vs-C $k$-dependence persists" caveat, now placed: it is a degeneracy of SU(3), not a gap in the derivation.)

**N5 — Abelian dominance legitimises the Cartan projection.** The **fundamental** colour-electric flux is carried by the Cartan (maximal-Abelian) subalgebra; the off-diagonal gluons renormalise the VEV magnitude but **cannot change the N-ality**. This is *why* the Cartan-projected F86/F139 captures the fundamental string tension (empirically $\sim$92% of $\sigma$ in lattice QCD). The "full non-Abelian condensate beyond Cartan" that F139 flagged affects only N3's *magnitude* (the unsolved dynamical scale), not N2's *classification*.

**Q2 verdict.** The full non-Abelian condensate is **algebraically derivable only in its centre content** (existence N1, N-ality classification N2, Casimir/$k$-string ratios N3–N4, Abelian-dominance legitimacy N5 — all exact group theory / centre algebra). Its **dynamical magnitude** (VEV, absolute 3+1D $\sigma$, and the universal $k$-law for $N\ge4$) is the open non-perturbative problem and remains MC-only (F94). It is not "solved"; what is exactly derived is the part that the centre symmetry makes representation- and dimension-independent.

---

## 4. Checks

| # | Check | Tier | Residual |
|---|---|---|---|
| T1 | bag dictionary $B=e^2v^4/4$, $\Phi=2\pi n/e$ ⇒ $\sigma_{\rm FL}=\Phi\sqrt{2B}=\tfrac1{\sqrt2}\,2\pi v^2 n$ | 1 (algebraic) | prefactor $1/\sqrt2$ to $10^{-12}$ |
| T2a | spread-thin tension $\sigma\propto A^{-1/3}$: decade ratio $=10^{1/3}$ | 1 (algebraic) | $<10^{-6}$ |
| T2b | direct minimisation: $\sigma(L)$ falls as $L^{-2/3}$ (non-confining) | 3 (numeric) | $<2\%$ vs $L^{-2/3}$ |
| T3 | SU(3) Casimir ratios $\sigma_R/\sigma_F=C_2(R)/C_2(F)$ | 1 (group theory) | exact |
| T4 | SU(3) $k$-strings: Casimir and sine both give $\sigma_2/\sigma_1=1$ | 1 (group theory) | exact |

All assertions in `derive_dielectric_noconfine.py` pass.

## 5. Honest scope / what this does and does not claim

- **Q1 is a no-go for the *electric dielectric* route, not for the model's confinement.** Confinement is exact via F70 (2D area law), F99 (centre Lagrange multiplier), and F86 (magnetic ANO vortex, $\sigma=2\pi v^2 n$). What fails is the specific hope of reading $2\pi v^2 n$ off the F139 *longitudinal dielectric tube* — that functional is non-confining in the continuum and confines only under regulators.
- A genuinely confining dielectric *would* need a $\varepsilon_c(f)$ / potential pair whose cost-per-conductivity stays bounded below (e.g. a linear-in-conductivity potential, or a hard MIT bag), or the topological pinning of the magnetic dual. Constructing such a BPS-dual dielectric that saturates $2\pi v^2 n$ is a possible future sharpening, but it is **not** the $\varepsilon_c=1-f^2$ model in use.
- **Q2:** N1–N5 are exact; the dynamical scale is not derived here and is not claimed to be. SUSY (Seiberg–Witten) is where non-Abelian flux tubes are solved exactly — outside this model's scope.

## 6. Ledger

New module `ca-simulation/derive_dielectric_noconfine.py` (dual-SC dictionary, the $A^{-1/3}$ spreading law, the growing-box minimisation, SU(3) Casimir/$k$-string ratios; self-checking `main()`). Findings: this file. Resolves F139 §6's two open edges — Q1 with an exact structural obstruction (and a pointer to F99 as the map that already works), Q2 with a scope theorem separating the exactly-derivable centre content from the open dynamical magnitude. Exactness rows: Tier-1 #89 (bag prefactor $1/\sqrt2$), #90 (spreading $A^{-1/3}$ / SU(3) $k$-string degeneracy); Tier-3 #91 (non-confining $L^{-2/3}$ tension).
