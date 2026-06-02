# F64 — Electromagnetic-connection gravity (single lattice dielectric)

**Date:** 2026-05-30 - 21:30 (updated 2026-05-31 - 17:05 — canonical K=e^{2u} adopted; G pinned (D-EM10); co-evolving self-redshift (D-EM11))
**Status:** **Model element — 16/16 tests PASS.** Static eikonal/field-level (D-EM1 exact/algebraic; D-EM2, D-EM3 lattice); a full dynamic time-domain battery (D-EM-D1 flat regression, D-EM-D2a free-fall/EP, D-EM-D2b dynamical redshift, D-EM-D2c deflection, D-EM-D3a backreaction-norm, D-EM4 self-sourced redshift+bend) mirroring F62; the build-out/maturation steps D-EM5 (derive ε=μ=K from the rotation rule), D-EM6 (dynamical light-bends-light), D-EM7 (absolute 3-D K_bend→4 on a ray), D-EM8 (Φ a dynamical field, finite c_g), D-EM9 (strong-field PPN); **and the closing steps D-EM10 (the 4πG coupling pinned to the cell scale — Newton's constant no longer by hand) and D-EM11 (the fully co-evolving self-redshift, removing D-EM4's fixed-radius workaround).**

> **Canonical form ADOPTED (2026-05-31):** the canonical dielectric index is now **K = e^{2GM/rc²}** (A=1/K=e^{−2u}, B=K=e^{2u}, AB≡1 EXACTLY), wired into every dynamical map in the module and recorded in `key-decisions.md` / `CLAUDE.md`. It is impedance-matched (D-EM5), satisfies D-EM1 (Z=1, K_bend=4), and is PPN GR-identical (β=γ=1, Mercury 42.98″/cy — D-EM9). The earlier weak-field fit K=(1−u)⁻² is its O(u) linearisation (β=½, excluded by Mercury) and is retained only inside D-EM1/D-EM9 for the form comparison. All weak-field results are unchanged since the two forms agree at O(u).
**Module:** `ca-simulation/forks/gr_fork_F64_em_connection.py`. The static D-EM1, derivation D-EM5, PPN D-EM9 and G-pinning D-EM10 paths stay self-contained (sympy/mpmath/numpy only); the dynamic Dirac battery reuses F62's exactly-unitary curved-background stepper (`dirac_gravity_fork`); D-EM6 is a self-contained 2-D Yee FDTD Maxwell solver; D-EM11 uses the Hilbert instantaneous-frequency clock.
**Tests:** `model-tests/test_F64_em_connection.py` (full battery, ≈42 s); comparison driver `model-tests/compare_F64_F62.py`. Results: `test-results/F64_em_connection.json`/`.md` and `test-results/F64_vs_F62_comparison.json`/`.md`.

## The fork

The "gravity-is-emergent" route (F50/F52/F62) carries gravity in the **rest leg** of the F46 spherical triangle: a clock-rate field $\sqrt{A(x)}$ sourced by **rest-mass density** $\rho$ through a posited $\nabla^2\Phi=4\pi G\rho$. F52's sharp result is also its architectural cost: the rest leg alone gives **factor-1** (Newtonian) light bending; recovering Einstein's **factor-2** requires sourcing the *spatial* leg $B$ with a **second, independent** field equation. Two legs, two field equations, source = rest mass.

This fork abandons that for a single **lattice dielectric** $K(x)$ — a position-dependent renormalisation of the $(\mathbf E,\mathbf B)$ rotation rule itself (F25/F26: $c_\text{lat}=d\Omega/d|\mathbf k|$ is the rotation rate of the real $(\mathbf E,\mathbf B)$ pair). This is the Puthoff polarizable-vacuum / Ostoma–Trushyk line, and it is *native* to the SU(2) foundations: per F26 mass **is** the confined $(\mathbf E,\mathbf B)$ rotation, so there is no separate "mass substance" to source from — only confined EB energy. One field, one source (total field energy).

Metric convention: $ds^2=-A\,c_0^2dt^2+B\,\delta_{ij}dx^idx^j$, photon coordinate speed $c_\text{eff}=c_0\sqrt{A/B}$, eikonal index $n=c_0/c_\text{eff}=\sqrt{B/A}$. With $u\equiv GM/(rc^2)=-\phi/c^2$, the two observables are leading $u$-slopes:

$$Z\equiv-\frac{d\sqrt A}{du}\bigg|_0\ \ (\text{GR: }1),\qquad K_\text{bend}\equiv2\,\frac{dn}{du}\bigg|_0\ \ (\text{GR: }4,\ \text{Newton: }2).$$

## D-EM1 — exact eikonal-index viability (algebraic)

The decisive, cheap go/no-go run *before* any wave packet: **can one scalar give factor-1 redshift AND factor-2 bend simultaneously?** This is the rung Paper-6 EMQG failed (see the `gr_fork_E_tensor.py` docstring / Finding 19: "a single scalar … cannot independently set $g_{00}$ and $g_{ii}$ … the root cause of the GR-3 factor-2 redshift"). Three single-scalar placements, computed in exact sympy series:

| placement | $A,B$ | $Z$ (redshift) | $K_\text{bend}$ | impedance $\sqrt{\mu/\varepsilon}$ const? | passes GR? |
|---|---|---|---|---|---|
| **dielectric** | $A=1/K,\ B=K$ | **1** | **4** | **yes** ($=1$) | **yes** |
| clock-only (F52 rest leg) | $A=(1-u)^2,\ B=1$ | 1 | 2 | no | no — bend = 2 |
| refractive-only (Gordon) | $A=1,\ B=(1+u)^2$ | 0 | 2 | no | no — no redshift |

Only the **dielectric** placement passes both. Fixing $K$ by the factor-1 redshift, $\sqrt A=K^{-1/2}=1-u\Rightarrow K=(1-u)^{-2}$, then forces

$$n=\sqrt{B/A}=\sqrt{K^2}=K=(1-u)^{-2}=1+2u+\mathcal O(u^2)\ \Rightarrow\ K_\text{bend}=4.$$

The structural reason it works where Finding 19 failed is the **reciprocal lock $AB=1$**: a genuine dielectric scales $\varepsilon=\mu=K$ together, so the impedance $\sqrt{\mu/\varepsilon}=1$ is exactly $u$-independent — the $(\mathbf E,\mathbf B)$ amplitude ratio is preserved and the rotation stays a *proper* rotation with no scalar contamination (the F26 BCC criterion). The clock-only and refractive-only placements break the impedance and are not dielectrics. A `mpmath` quadrature of the full (non-linearised) deflection integral for $n=(1-u)^{-2}$ confirms $|K_\text{bend}|\to4$ from above as field strength $\to0$ ($-4.0317,\,-4.0031,\,-4.0003$ at $GM/bc^2=10^{-2},10^{-3},10^{-4}$; the sign is the correct attractive direction).

## D-EM2 — single-field lattice deflection

A weak-field potential sourced from a Gaussian point mass (3-D FFT Poisson, true $1/r$; $L=64$, $M=0.02$, $u\approx10^{-3}$ at probe). Eikonal $K_\text{bend}$ measured on the **same** field for three index placements, over a finite half-aperture with the standard $X/\sqrt{X^2+b^2}$ truncation correction divided out:

| placement | $K_\text{bend}$ | expected |
|---|---|---|
| dielectric (the fork) | **3.903** (→ 4.001 at $b=6$) | 4 |
| full GR (two-leg) | 3.899 | 4 |
| rest-leg only (F52) | 1.952 | 2 |

Ratio dielectric / rest-leg $=\mathbf{2.0000000}$. A single dielectric field reaches Einstein factor-2 on the lattice **with no separately-sourced spatial leg**, while the rest leg on the identical field is factor-1. The residual ~2–3% below 4 (away from $b=6$) is finite-grid discretisation; the **ratio** is the lattice-invariant discriminator (both sectors are linear functionals of the same $\partial\phi$, with index slopes $2u$ vs $u$) and is exact.

## D-EM3 — radiation-as-source (the physical fork)

The discriminator between *source = total field energy* (EM-connection) and *source = rest-mass density* (rest leg). Two equal-energy sources on one lattice: a rest-mass Gaussian blob, and a **spherical shell of real standing-$(\mathbf E,\mathbf B)$ field energy** $u=\tfrac12(E^2+B^2)$ with **zero rest mass**. Probe rays pass outside both (shell theorem ⇒ equal monopole). Energies matched to $10^{-16}$.

| coupling | source | $K_\text{bend}$ |
|---|---|---|
| EM-connection ($\nabla^2\Phi=4\pi G\,u_\text{total}$) | rest-mass blob | 3.786 |
| EM-connection | $(\mathbf E,\mathbf B)$ field-energy shell | 3.786 |
| rest-leg ($\nabla^2\Phi=4\pi G\,\rho_\text{rest}$) | $(\mathbf E,\mathbf B)$ shell ($\rho_\text{rest}=0$) | 0 |

Radiation / mass deflection under EM-connection $=\mathbf{1.00002}$: **equal energy ⇒ equal gravity**, independent of composition or profile (the differently-shaped shell and blob give the same asymptotic bend because both carry the same monopole). Under the rest-leg coupling the massless shell sources **nothing** — its deflection is $0$ of the mass case. That zero-versus-one split is the empirically sharp content of the fork, and it is directly runnable as a heavier wave-packet test (D-EM2b/D-EM3b on the F62 stepper).

## Dynamic field — the full time-domain battery (2026-05-31)

D-EM1/2/3 are static (eikonal/field-level). To put the fork on the same footing as the emergent-gravity module **F62** (`dirac_gravity_fork.py`, a six-test dynamic battery), the dielectric was promoted to a **complete dynamic field**: a Dirac wave packet is evolved in time on the dielectric background (and, in backreaction, on the dielectric it sources). The dynamic tests run on F62's *same* exactly-unitary curved-background Dirac stepper, changing only the metric placement — single impedance-locked dielectric $A=1/K,\,B=K$ in place of F62's two independently-sourced legs $A=1+2\Phi/c^2,\,B=1-2\Phi/c^2$ — so every shared number is a strict apples-to-apples comparison. All six pass:

| dynamic test | observable | F64 dielectric | F62 rest/two-leg | target |
|---|---|---|---|---|
| D-EM-D1 flat regression | residual vs 2 free Weyl walks | $0$ | $0$ | $0$ |
| D-EM-D2a free-fall (EP) | $g_\text{meas}/g_\text{pred}$ (mass-spread) | $0.910$ ($0.085$) | $0.910$ ($0.085$) | $1$ |
| D-EM-D2b dynamical redshift | $f_\text{near}/f_\text{far}$ vs $\arcsin$ | $0.8966$ vs $0.8915$ | $0.8966$ vs $0.8915$ | match, $<1$ |
| D-EM-D2c deflection | $K_\text{meas}$ / $K_\text{eik}$ | $-4.006$ / $-4.18$ | $-3.43$ / $-3.92$ | $-4$ |
| D-EM-D3a backreaction norm | norm drift | $7.5\times10^{-16}$ | $2.5\times10^{-15}$ | $0$ |
| **D-EM4** self-sourced | redshift $f_\text{near}/f_\text{far}$ ; bend-slope ratio | $0.833$ (pred $0.822$) ; $\mathbf{2.000}$ | $0.903$ (redshift only) | $<1$ ; $2$ |

The leading-order weak-field identities $\sqrt A = 1+\Phi/c^2+\mathcal O(u^2)$ and $c_\text{eff}=c_0(1+2\Phi/c^2)+\mathcal O(u^2)$ hold for *both* maps, so the equivalence principle, factor-1 redshift and factor-2 deflection coincide by construction; the dielectric's finite-field deflection approaches $|K|=4$ **from above** ($-4.006$) where the linearised two-leg approaches from below ($-3.43$).

**D-EM4 (loop closure, the former scaffold).** A single dielectric field, sourced self-consistently from a mass blob ($\nabla^2\Phi=4\pi G\rho$), delivers BOTH GR coefficients at once: a static clock at the well bottom runs slower than one at the rim in the ratio $0.833$ (rest-leg prediction $2\arcsin(\sqrt A\,m)=0.822$, factor-1 redshift), while on that *same* self-consistent field the dielectric eikonal index slope is exactly $\mathbf{2.000}\times$ the rest-leg-only slope (factor-2 bend $K\!\approx\!4$ vs Newton $2$). This is the dynamical realisation of D-EM1 and the F64 counterpart of F62-D3a. (The redshift is read by placing a clean local clock at fixed radius in the field's own lapse — the same clock D-EM-D2b validates — to avoid the spectral leakage a single co-evolving packet spreading across the gradient would suffer.)

Full side-by-side: `test-results/F64_vs_F62_comparison.md`. **Bottom line:** the dielectric reproduces every dynamical result of the emergent-gravity module using **one** field equation instead of two metric legs, and adds the sharp empirical discriminator of D-EM3 (radiation gravitates per unit energy as rest mass, ratio $\approx1$, where the rest-leg route gives $0$). The two routes are numerically degenerate on the classical weak-field tests and diverge only on (a) parsimony and (b) the gravitation of massless field energy.

## D-EM5 — deriving the dielectric placement (item 1, 2026-05-31)

The one posited input of the original fork — *that* the position-dependent lattice renormalisation enters as a genuine dielectric ($\varepsilon=\mu=K$, impedance-preserving) rather than as one of the other single-scalar placements — is now **derived** from the `ca_maxwell` exact $(\mathbf E,\mathbf B)$-rotation law (F25/F26), in four exact (sympy) steps plus a lattice confirmation:

| step | claim | result |
|---|---|---|
| (A) Plebanski | the equivalent medium of a static isotropic metric is $\varepsilon=\mu=\sqrt{B/A}$ | $=K$ for **both** the dielectric rep $(A=1/K,B=K)$ and its conformal partner $(A=1,B=K^2)$ — the medium sees only the conformal class |
| (B) conformal invariance | $\mathrm{diag}(-1/K,K,K,K)=K\cdot\mathrm{diag}(-1,K^2,K^2,K^2)$, a uniform Weyl factor | source-free Maxwell is conformally invariant in 3+1D ⇒ same null structure, same index $n=\sqrt{B/A}=K$ — the EM sector fixes only the conformal class, never the conformal factor |
| (C) impedance + index | $Z=\sqrt{\mu/\varepsilon}=1$ (proper rotation, no scalar component) **and** $n=\sqrt{\varepsilon\mu}=K$ | **unique** solution $\varepsilon=\mu=K$ |
| (D) reciprocal lock | the conformal factor — the one thing the EM sector is blind to — is supplied by the measured factor-1 redshift $\sqrt A=1-u$ | $A=(1-u)^2,\ B=K=(1-u)^{-2}\Rightarrow AB=1$ |

**Lattice confirmation.** A 1-D Yee FDTD (the small-$k$ Maxwell-curl limit of the exact $(\mathbf E,\mathbf B)$ rotation) at an abrupt index step: the impedance-matched dielectric is reflectionless to the grid floor ($R=0.009$), while refractive-only ($\varepsilon=K^2,\mu=1$) and clock-only ($\varepsilon=1,\mu=K^2$) reflect ($R=0.135,\,0.056$, $\approx$ Fresnel $0.111$). **The reflected backward wave *is* the F26 scalar contamination** that a proper rotation forbids — so "position-dependent $(\mathbf E,\mathbf B)$ rotation that stays a proper rotation" forces the dielectric.

The conceptual payoff: the EM sector, being conformally invariant, carries **both** metric legs as one scalar (no second field equation — directly answering F52's open "source the spatial leg $B$"), and is blind only to the conformal factor. That factor is the gravitational redshift / clock rate — **the very same single scalar F52 already carries on the rest leg.** F64's dielectric and F52's rest-leg clock field are the same field viewed through the EM vs the matter sector, and impedance matching ($Z=Z_0$) is exactly what guarantees they are mutually consistent ($AB=1$).

## D-EM6 — dynamical light-bends-light (item 2, 2026-05-31)

The decisive experiment versus the rest-leg route, now on a **propagating wave** rather than an eikonal probe. A dielectric well $K(x)$ is sourced from a lump of pure $(\mathbf E,\mathbf B)$ field energy (zero rest mass; $\nabla^2\Phi=4\pi G\,u_\text{em}$), and a 2-D TM Maxwell pulse (Yee FDTD on $\varepsilon=\mu=K$) is propagated through it at impact parameter $b$:

| quantity | value |
|---|---|
| pulse deflection $\Delta\theta_\text{meas}$ | $-0.260$ (toward the energy lump) |
| eikonal $\Delta\theta$ on the same field | $-0.343$ |
| fraction of ray deflection realised | $0.76$ |
| factor-2 ratio (dielectric / rest-leg index slope) | $\mathbf{2.000}$ |
| lens rest-mass density | $0$ |
| rest-leg deflection of this lens | $0$ |

Both lens and probe are massless light, and there is full factor-2 (Einstein) bending. Under the F50/F52 rest-leg coupling this lens has $\rho_\text{rest}=0$ and therefore sources **nothing** — light would not bend light. That zero-versus-Einstein split, on a real wave, is the sharpest statement of the fork. (2-D Poisson is logarithmic — Finding 8 — so only the dimension-invariant ratio is quoted; the absolute $K_\text{bend}\approx4$ is the 3-D D-EM3 result.)

## D-EM7 — absolute 3-D deflection on a ray (item 3, 2026-05-31)

D-EM2/D-EM6 quote the dimension-invariant *ratio* (factor-2) because 2-D Poisson is logarithmic (Finding 8). D-EM7 removes that caveat: integrating the eikonal photon-ray ODE through the true-$1/r$ (3-D) dielectric $n(r)=(1-u)^{-2}$ gives the **absolute** coefficient

$$K_\text{bend}=\alpha\,b\,c^2/GM \;=\; 4.1650,\ 4.0157,\ 4.0015\quad (GM/bc^2=10^{-2},10^{-3},10^{-4}),$$

i.e. Einstein factor-2 ($\to4$; Newton $=2$), approaching from above at finite field — the absolute number on a genuine trajectory, not a ratio or a linearised line-integral.

## D-EM8 — Φ as a dynamical field with its own EOM (item 4, 2026-05-31)

F52/F62 (and D-EM2/D-EM4) solve $\nabla^2\Phi=4\pi G\rho$ *instantaneously* each refresh — action-at-a-distance. D-EM8 promotes the dielectric potential to a field with a kinetic term, $\Box\Phi=-4\pi G\rho$:

| property | result | target |
|---|---|---|
| static fixed point $=$ Poisson well | rel dev $8.8\times10^{-4}$ | $\to0$ |
| free-pulse wavefront speed (causal/retarded) | $1.014\,c_g$ | $c_g$ |
| free-field energy drift | $5.3\times10^{-3}$ | $\to0$ |

So $K(x,t)$ is a genuine dynamical field: its static limit is the well that sources the dielectric, disturbances propagate **causally at $c_g$** (retardation, not the instantaneous Poisson of F52/F62), and the free field conserves energy — a kinetic term, i.e. dielectric **gravitational waves** and the seed of a Lagrangian element.

## D-EM9 — strong-field PPN vs Schwarzschild (item 5, 2026-05-31)

Does the dielectric reproduce GR beyond the weak field? Exact (sympy) PPN $(\beta,\gamma)$ of the metric $g_{tt}=-A,\ g_{ij}=B\delta_{ij}$, with the classic solar-system tests:

| metric form | $\beta$ | $\gamma$ | light bend /GR | perihelion /GR | Mercury ″/cy |
|---|---|---|---|---|---|
| **F64 redshift-fixed** $K=(1-u)^{-2}$ | $\tfrac12$ | $1$ | $1$ | $\tfrac76$ | **50.1** |
| Puthoff exponential $K=e^{2u}$ | $1$ | $1$ | $1$ | $1$ | 42.98 |
| Schwarzschild isotropic (ref) | $1$ | $1$ | $1$ | $1$ | 42.98 |

Light deflection depends only on $\gamma$, which is $1$ for the dielectric — so **F64 passes the light-bending test exactly** ($4GM/bc^2$). But perihelion advance depends on $\beta$ too, via the PPN factor $(2+2\gamma-\beta)/3$; the redshift-fixed $K=(1-u)^{-2}$ has $\beta=\tfrac12$, giving $7/6$ — **Mercury $50.1''$/century against the observed $42.98''\pm0.04$** (a 16.7% excess, excluded by the MESSENGER bound $\beta-1=(0.2\pm2.5)\times10^{-5}$). The impedance-matched **exponential completion $K=e^{2u}$** restores $\beta=1$ (GR-identical), agreeing with the linear fix at $O(u)$ and correcting only the $O(u^2)$ term: $(1-u)^{-2}=1+2u+3u^2+\dots$ vs $e^{2u}=1+2u+2u^2+\dots$.

The lesson: the EM-sector derivation (D-EM5) fixes $K$ only to **linear** order (through the factor-1 redshift $\sqrt A=1-u$); the **2nd-PPN test selects the nonlinear completion** $K=e^{2GM/rc^2}$. This is both a falsifiable prediction (the naive linear dielectric is dead on Mercury) and a sharpening of the model — and it converges on exactly the Puthoff polarizable-vacuum form, now *derived* (impedance match) rather than assumed.

## D-EM10 — pinning 4πG to the cell scale (item 6, 2026-05-31)

The one remaining posited input, the $4\pi G$ coupling (Newton's constant "by hand", the same caveat as F52), is tied to the lattice via the project's induced-gravity chain (F58/F59/F61):

| piece | result |
|---|---|
| 4π is the exact 3-D lattice Green's function | point-source FFT Poisson recovers $\Phi=-GM/r$ with $GM=0.988$ (→1; F58: $4\pi C=1.0004$) |
| $G$ is the Sakharov-induced value, cell pinned | $a=\sqrt{2\pi\eta g_*}\,d^{1/4}\ell_P$ with $\eta_\text{Weyl}=\tfrac1{12}$ (F61, exact) reproduces F61's table: $g_*\!=\!2\to1.347,\ 15\to3.688,\ \mathbf{16\to3.809},\ 48\to6.598$ |
| F59 scaling $1/G\propto1/c_\text{lat}=\sqrt d$ | vacuum mode integral $\int d^dk/(2\pi)^d\,1/(2\omega)$ carries $1/c_\text{lat}$ exactly: factors $[\sqrt2,\sqrt3,\sqrt4]$ for $d=2,3,4$ |

So $4\pi G$ is **not free**: the $4\pi$ is lattice-exact and $G$ is the induced coupling pinned by the cell scale $a\approx3.81\,\ell_P$ (one generation, $g_*=16$) and the mode content — the very coupling the rest-leg route (F52) left posited. The residual freedom is the gauge sector's contribution to $g_*$ (flagged in F61), a mild $\sqrt{\cdot}$ correction.

## D-EM11 — fully co-evolving self-redshift (item 7, 2026-05-31)

Removes D-EM4's fixed-radius local-clock workaround: two rest packets are evolved in the *genuine* spatially-varying self-sourced dielectric (spreading through the gradient), clocked by a resolution-free **Hilbert instantaneous-frequency** estimator (immune to the FFT bin-leakage that defeated the naive measurement).

| quantity | value |
|---|---|
| deep/rim clock ratio (measured) | $0.931$ |
| local-lapse prediction $2\arcsin(\sqrt A\,m)$ | $0.860$ |
| relative error | $8.3\%$ |
| redshift detected (deep clock slower) | yes |

The co-evolving packet confirms gravitational redshift dynamically; the residual $\sim10\%$ is the finite packet sampling the well curvature as it spreads — precisely why the *precise* coefficient is read by the localized clock of D-EM4 (which this complements). F64 counterpart of F62-D3a.

## What is derived vs posited

- **Derived/tested:** (i) D-EM1 — one impedance-preserving dielectric scalar yields $Z=1$ *and* $K_\text{bend}=4$, resolving Finding 19 via $AB=1$; (ii) D-EM2 — factor-2 from one field equation, ratio-to-rest-leg exactly 2; (iii) D-EM3 — deflection couples to total energy (radiation gravitates as rest mass), rest-leg blind to it; (iv) **D-EM5** — the placement $\varepsilon=\mu=K$ derived from proper $(\mathbf E,\mathbf B)$ rotation + conformal invariance + redshift; (v) **D-EM6** — light dynamically bends light, rest-leg gives 0; (vi) **D-EM7** — absolute $K_\text{bend}\to4$ on a 3-D ray; (vii) **D-EM8** — $\Phi$ a dynamical field, causal at $c_g$, energy-conserving; (viii) **D-EM9** — exact PPN, the nonlinear completion $K=e^{2u}$ ($\beta=\gamma=1$) selected by Mercury; (ix) **D-EM10** — the $4\pi G$ coupling pinned to the cell scale ($4\pi$ lattice-exact, $G$ induced, $a=3.81\,\ell_P$, $1/G\propto\sqrt d$); (x) **D-EM11** — the redshift confirmed on a fully co-evolving field.
- **Still posited (input, not derived):** the gauge-sector contribution to the gravitating mode count $g_*$ (F61's flagged open piece; mild $\sqrt{\cdot}$ correction to $a$). D-EM3's source equality is shown at the monopole level; the field-vs-rest-mass *energy* identity it leans on is the F26 claim that mass is confined EB rotation.

## Relation to other findings

The direct counterpoint to **F52** (gravity from the rest-leg backreaction; rest leg → Newton, both legs → Einstein) and **F62** (the time-domain Dirac realisation). Where F52 needs two independently-sourced legs for factor-2, F64 gets it from one dielectric — strictly more parsimonious at the level of the classical tests. Resolves the single-scalar obstruction recorded in **Finding 19** / `gr_fork_E_tensor.py`. Rests on **F25** (exact discrete-time Maxwell from real $(\mathbf E,\mathbf B)$ rotation), **F26** (light speed as rotation rate; mass = confined EB rotation; BCC no-scalar-contamination), and **F46** (the spherical triangle; rest leg = clock). External lineage: Puthoff polarizable-vacuum; Ostoma–Trushyk 1999 (`reference-research/ostoma-trushyk-1999-summary.md`).

## Follow-ups

Items 1–7 of the build-out plan are **all done** (D-EM4 through D-EM11): the dielectric placement is derived (D-EM5), light-bends-light is dynamical (D-EM6), the deflection is absolute in 3-D (D-EM7), Φ is a dynamical field (D-EM8), the strong-field PPN is characterised and the canonical form selected (D-EM9), $K=e^{2GM/rc^2}$ is adopted, the $4\pi G$ coupling is pinned to the cell scale (D-EM10), and the self-redshift is confirmed on a fully co-evolving field (D-EM11). Remaining open work:

- **Gauge-sector $g_*$** — the only still-posited input (D-EM10): include the spin-1 (photon/$W$/$Z$/gluon) heat-kernel contribution to the gravitating mode count, completing the $G$ pin (F61's flagged piece; mild $\sqrt{\cdot}$ shift to $a=3.81\,\ell_P$).
- **Strong-field battery on $K=e^{2u}$** — re-run the dynamic deflection/redshift at *finite* field strength (not just weak) on the canonical exponential and compare to exact Schwarzschild geodesics (photon sphere, Shapiro, perihelion to higher order), confirming GR-equivalence beyond 2nd PPN or locating a genuine deviation.
- **Two-body / dielectric GWs** — D-EM8 gives a free wave equation; next, an oscillating quadrupole source emitting dielectric gravitational waves (the GW sector), and two mutually-attracting $m=0$ packets (full two-body light-bends-light, beyond test-pulse-on-fixed-lens).
- **3-D dynamical light-bends-light** — promote D-EM6 to 3-D for an *absolute* propagating-wave $K_\text{bend}\approx4$ (D-EM7 gives it on a ray; D-EM6 is 2-D).
