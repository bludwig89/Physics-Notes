# F58 — Does the clock-rate ↔ rest-mass coupling 4πG follow from the neighbour rule?

**Date:** 2026-05-30 - 13:40
**Status:** Confirmed (scope-limited) — 5/5 tests PASS; Q0 exact (residual $2\times10^{-16}$), Q3a lock exact ($1\times10^{-16}$), Q1/Q2/Q3b quantitative. Answers the open follow-up named verbatim in **F52** and **F55**.
**Module:** new `ca-simulation/forks/gr_fork_F58_clockrate_coupling_derivation.py` (additive; reuses `ca_bcc` F26 dispersion).
**Tests:** `model-tests/test_F58_clockrate_coupling_derivation.py`; results `test-results/F58_clockrate_coupling_derivation.json`.

## The question

F52 *posited* that the local clock-rate deficit Poisson-couples to rest-mass density,

$$\nabla^2_\text{lat}\,\Phi(x)=4\pi G\,\rho(x),\qquad \text{clock rate }s(x)=\sqrt{A(\Phi)}=1-\tfrac{|\Phi|}{c^2}+\dots,$$

and left open whether this coupling "follows from the CA neighbour-coupling rule (the $c_\text{lat}=d\Omega/d|\mathbf k|$ phase-matching of F25/F26) rather than being posited." F58 isolates the **rest-leg / clock-rate channel specifically** (vs. F56's generic Einstein-coupling factorisation) and splits the coefficient $4\pi G$ into the pieces that *are* fixed by the neighbour rule and the one piece that provably is not.

## The decomposition

$$\underbrace{\nabla^2}_{\text{Q2: form}}\Phi=\underbrace{4\pi}_{\text{Q1}}\,\underbrace{G}_{\text{Q3}}\,\rho,\qquad\text{prerequisite }\underbrace{\text{Q0: universality}}_{\text{a single }G\text{ can exist}}.$$

## Results

| Test | What it checks | Result |
|---|---|---|
| **Q0** universality (WEP) | fractional clock slowing $1-\sqrt A$ is mass-independent | max spread over $m\in[0.01,0.9]$ = $2.2\times10^{-16}$ — **bit-for-bit** ($\sqrt A$ is a common factor on $\arcsin m$) |
| **Q1** the $4\pi$ | bare 6-neighbour Laplacian point-source far field $\to-1/(4\pi\,r)$ | $4\pi\,C=1.0004$, fit $r^2=0.99994$ — the $4\pi$ is lattice solid angle, **not inserted** |
| **Q2** the Laplacian form | small-$k$ neighbour symbol is isotropic $\text{stiff}\cdot|\mathbf k|^2$ | anisotropy spread $5.6\times10^{-8}$ across 100/110/111 — the field equation **must** be $\nabla^2\Phi\propto\rho$ |
| **Q3a** the F25/F26 lock | sweep hopping $J$: $c_\text{lat}\propto J$, stiffness $\propto J^2$ | $\text{stiffness}/c_\text{lat}^2$ spread $1.1\times10^{-16}$ (=1, exact); measured BCC $c_\text{lat}=0.57733\approx1/\sqrt3$ |
| **Q3b** dimensionful $G$ | Sakharov BZ integral $1/G\propto\Lambda^p$ | $p=2.014$ ⇒ $G\propto\ell^2$ — the lattice spacing in metres is the one irreducible input |

Overall **PASS**.

## Interpretation — the verdict, piece by piece

1. **Q0 — a single coupling $G$ can exist at all (exact).** For "clock-rate slowing per unit potential" to be one constant, it must be the *same* for every clock. In the model the renormalised rest leg is $\Omega_\text{rest}(x)=\sqrt{A(x)}\arcsin m$, so the fractional deficit $1-\Omega_\text{rest}(x)/\Omega_\text{rest}(\infty)=1-\sqrt A$ is **independent of $m$** — bit-for-bit, because $\sqrt A$ multiplies $\arcsin m$ as a common factor. This is the weak equivalence principle, and it is a structural identity of the F46/F50 rest leg, not an assumption. Without it the question would be ill-posed.

2. **Q1 — the $4\pi$ is the lattice solid angle (derived).** If the clock-rate field obeys a neighbour-coupling (lattice-Laplacian) equation, a point rest-mass sources $\Phi(r)\to-(\text{coupling})/(4\pi r)$: the bare 6-neighbour stencil, with **no $4\pi$ put in by hand**, already has $4\pi C=1.0004$. So the $4\pi$ in $\nabla^2\Phi=4\pi G\rho$ is the solid angle of 3-D space as the neighbour rule's long-wavelength modes resolve it — the *same* isotropy that makes $c_\text{lat}=d\Omega/d|\mathbf k|$ direction-independent. (Re-confirms F56-C2 in the clock-rate channel.)

3. **Q2 — the Laplacian *form* is forced (derived).** The neighbour-coupling symbol's leading small-$k$ term is the isotropic $\text{stiffness}\cdot|\mathbf k|^2$ (anisotropy $5.6\times10^{-8}$). The unique local, isotropic, second-order operator is $\nabla^2$, so the equilibrium clock-rate field equation *must* be $\nabla^2\Phi\propto\rho$ — the Poisson form is not a modelling choice.

4. **Q3a — the coupling's $c_\text{lat}$-dependence is locked by the neighbour rule (exact).** The light-cone speed $c_\text{lat}$ and the clock-rate field's gradient stiffness are **not independent**: both descend from the single neighbour-hopping amplitude $J$. Sweeping $J$, $c_\text{lat}\propto J$ while the Green's-function stiffness $\propto J^2$, so $\text{stiffness}/c_\text{lat}^2$ is exactly hopping-independent ($1.1\times10^{-16}$). Hence the inverse coupling carries the light-cone speed, $1/G\propto\text{stiffness}\propto c_\text{lat}^2$, and with the measured $c_\text{lat}=1/\sqrt3$ the coupling inherits the $\sqrt d$ that F56-Part B saw in $1/G\propto\sqrt d\,\Lambda^2$. **This is the F25/F26 link the question asked for**: the gravitational coupling's dependence on the phase-matching speed is fixed by the neighbour rule.

5. **Q3b — the dimensionful magnitude is irreducible (Sakharov).** A *dimensionless* lattice cannot manufacture a dimensionful constant. The induced $1/G$ from the BZ integral of the F26 dispersion scales as $\Lambda^2$ ($p=2.014$), so $G\propto\ell^2$ — Newton's constant is locked to the lattice spacing (the Planck length, Finding 10, up to $\sqrt d$). **Choosing the lattice spacing in metres *is* choosing $G$.** This single number does not, and provably cannot, follow from the neighbour rule.

## Headline answer

> **The $4\pi$ and the *form* of the clock-rate coupling follow from the neighbour-coupling rule exactly; its *dependence* on the light-cone speed ($1/G\propto c_\text{lat}^2\propto\sqrt d$) is fixed by the same rule via the F25/F26 phase-matching; but the dimensionful *magnitude* of $G$ does not follow from the rule and cannot — it is the lattice spacing (Planck length).** So clock-rate slowing $\propto$ rest-mass density is *structurally forced* by the CA, and is *universal* (WEP) by the rest-leg identity; only the overall scale is an input, and that input is exactly the one Finding 10 already identified.

## What is derived vs what remains an input

| Piece of $4\pi G$ | Status |
|---|---|
| universality (same $G$ for all clocks, WEP) | **Derived exactly** — $1-\sqrt A$ is $m$-independent, residual $2\times10^{-16}$ (Q0) |
| $4\pi$ (solid angle) | **Derived** — bare neighbour-Laplacian far field, $4\pi C=1.0004$ (Q1) |
| Poisson form $\nabla^2\Phi\propto\rho$ | **Derived** — unique isotropic local 2nd-order operator (Q2) |
| $c_\text{lat}$-dependence of $G$ ($1/G\propto c_\text{lat}^2\propto\sqrt d$) | **Derived exactly** — stiffness $/c_\text{lat}^2$ hopping-independent, residual $1\times10^{-16}$ (Q3a) |
| dimensionful magnitude of $G$ | **Not derivable** — $G\propto\ell^2$ (Q3b); the lattice spacing in metres is the irreducible input |

## New exact results (exactness inventory)

- **F58-Q0** weak equivalence principle: fractional clock-rate deficit $1-\sqrt A$ is mass-independent — residual $2.2\times10^{-16}$ (Tier-2 machine precision; algebraically exact since $\sqrt A$ factors out of $\arcsin m$).
- **F58-Q3a** stiffness/$c_\text{lat}^2$ hopping-independence (the F25/F26 lock) — residual $1.1\times10^{-16}$ (Tier-2 machine precision; algebraically exact, both $\propto$ the single hopping amplitude).

## Caveats

- Q1/Q2 use the simple-cubic 6-neighbour stencil for an unambiguous demonstration of the solid-angle $4\pi$ and isotropy; the BCC stencil shares the same isotropic continuum limit (F30/F37 anisotropy is higher order), so the far-field $4\pi$ and leading Laplacian are unchanged. Q3a/Q3b use the actual F26 BCC dispersion.
- Q3a establishes that $1/G$ *scales as* $c_\text{lat}^2$ (both descend from one hopping amplitude); it does not fix the absolute O(1) prefactor — that is the scheme/mode-count issue inherited from F56/F57 (and the log-running correction F57 found in this very density channel).
- "Derived" for Q1/Q3b is quantitative (fit / scaling), not bit-for-bit; only Q0 and Q3a are machine-precision identities.

## Follow-ups

- Combine with **F57**: the log-running of the density-channel $\Pi_2$ means the clock-rate $G$ runs; Q3a's $c_\text{lat}^2$ lock should set the *coefficient* of that running. Compute $1/G=\Pi_2$ in units of $c_\text{lat}^2$ and check it is O(1).
- Promote Q3a from a scaling lock to an absolute statement by summing the BCC gravitating mode count $g_*$ (the open factor from F57).
- Check whether $G\propto\ell^2$ + $c_\text{lat}=1/\sqrt d$ selects one of Finding 10's three $(a,\tau)$ resolutions (shared open item with F56).

## Relation to other findings

Closes the explicit open follow-up of **F52** (the $4\pi G$ question) and **F55** (the coupling-from-phase-matching question), for the rest-leg/clock-rate channel. Builds on **F46/F50** (rest leg = clock, $\Omega_\text{rest}=\sqrt A\arcsin m$ — the source of Q0's universality), **F25/F26** ($c_\text{lat}=d\Omega/d|\mathbf k|=1/\sqrt3$ — the speed Q3a locks the coupling to), **F56** (the $4\pi$ Green's function and the Sakharov $G\propto\ell^2$, reused in Q1/Q3b), and **F57** (the density-channel polarization whose log-running refines Q3a's absolute coefficient). Consistent with **Finding 10** (lattice spacing ↔ Planck length, the irreducible input Q3b lands on).
