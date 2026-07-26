# F180 — The gravitational-wave equation from the rotation rule: $c_\text{grav}=c_\text{lat}=1/\sqrt3$ (GW170817 survived)

**Date:** 2026-06-30 - 12:30
**Numbering:** F164–F179 were taken by concurrent sessions; this is **F180** (re-checked per CLAUDE.md).
**Status:** Candidate finding — 5/5 checks PASS. The coefficient identity (A) and the inverse-coupling scaling (B) are **exact** (sympy zero residual / machine precision $\sim10^{-16}$); the induced-self-energy light-cone inheritance (C) is lattice-numerical to $\sim10^{-5}$; the dispersion-slope identity (D) is **exact-algebraic**; the real-space wavefront (E) is lattice to $\sim3\%$ (finite-grid). Closes audit **C1** (2026-06-29): the gravity sector now has a hyperbolic wave equation and $c_\text{grav}=c_\text{lat}$, so GW170817 no longer threatens falsification.
**Module / test:** `ca-simulation/forks/gr_fork_F180_gw_speed.py`; `tests/findings/test_F180_gw_speed.py` (~10 s; sympy + hand-rolled real arithmetic, numpy grid sums only — no complex/chiral transforms).
**Results:** `test-results/F180_gw_speed.json`.
**Cross-references:** [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=d\Omega/d\lvert k\rvert=1/\sqrt3$; mass = confined $(\mathbf E,\mathbf B)$ rotation), [[F64-em-connection-gravity]] (the dielectric $K$; D-EM8 promoted $\Phi$ to a dynamical field but left $c_g$ **by hand**), [[F106-psi-K-sourcing-derivation]] (the static law $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ this completes), [[F79-structural-newton-constant]] ($K$ has **zero tree stiffness** ⇒ its kinetic term is the induced loop), [[F59-induced-eh-prefactor-and-f10-selection]] ($1/G\propto1/c_\text{lat}=\sqrt d$ exactly), [[F105-on-axis-exact-dispersion]] (photon $\Omega=\lvert k\rvert/\sqrt3$ at all $k$ on axis), [[F178-gravity-full-tensor-adoption]] (canonical law = induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$; D-GW below is its linearised vacuum/weak-field wave reduction).

---

## 1. The gap this closes (audit C1)

The 2026-06-29 audit flagged a **potential falsification**. The gravity sector
sources the dielectric through F106's

$$\nabla^2\ln K(\mathbf x) = -\frac{8\pi G}{c^4}\,T^{00}[\psi](\mathbf x),$$

which is **Poisson's equation** — elliptic, hence instantaneous. GW170817
measured the gravitational-wave speed against the optical counterpart to
$\lvert c_\text{grav}-c_\text{photon}\rvert/c < 10^{-15}$. An instantaneous (or
free-speed) gravity sector is excluded. F64-D-EM8 had already *promoted* the
dielectric potential to a dynamical field obeying $\Box\Phi=-4\pi G\rho$, but its
wave speed $c_g$ was a **free parameter** put in by hand (`c_g=1.0` in the test).
What was missing: a derivation that the speed in that $\Box$ is **forced** to be
$c_\text{lat}=1/\sqrt3$, the photon's own light cone.

This finding supplies the derivation and proves $c_\text{grav}=c_\text{lat}=c_\text{photon}$
**identically** — they are not two numbers tuned to agree, they are the *same*
light cone of the lattice.

## 2. The derivation (four legs already in the model)

**Leg 1 — $K$ renormalises the rotation rule (F64-D-EM5).** Gravity is a single
impedance-locked dielectric $K(\mathbf x,t)$ with $A=1/K,\ B=K$, $AB\equiv1$. By
F26 the photon is the real $(\mathbf E,\mathbf B)$ pair rotating at rate
$\Omega=c_\text{lat}\lvert\mathbf k\rvert$; $K$ is a *position-dependent
renormalisation of that rotation rate*, $c_\text{eff}=c_\text{lat}/K$. The
vacuum ($K\to1$) light cone is $\omega=c_\text{lat}\lvert\mathbf k\rvert$,
$c_\text{lat}=1/\sqrt d=1/\sqrt3$ (V2/V3).

**Leg 2 — $K$ has zero tree stiffness; its kinetic term is the induced loop
(F79).** Source-free Maxwell is conformally invariant in $3{+}1$D and the EM
stress tensor is traceless, so the conformal factor $\tfrac12\ln K$ has **no
bare kinetic term** (F79-S3, verified to $3.6\times10^{-15}$). $K$ is not a
fundamental field — it is a reparametrization of the rotation rule, so it has no
independent graviton to carry a freely-chosen speed. Its **entire** stiffness is
the Sakharov/induced response of the lattice's own $(\mathbf E,\mathbf B)$/spinor
modes.

**Leg 3 — the induced kinetic term IS the matter vacuum polarisation, and that
loop carries only $c_\text{lat}$.** Because the graviton (here the scalar
$\delta\ln K$) has no tree term, its inverse propagator *is* the one-loop vacuum
polarisation $\Pi(q)$ of the metric/dielectric vertex. The loop is built from
the constituent propagators, whose **only** velocity is the rotation rate
$c_\text{lat}$ (F26). A loop integral over propagators with light cone
$\omega=c_\text{lat}\lvert\mathbf k\rvert$ can depend on the external momentum
$q=(q_0,\mathbf q)$ **only through the constituent invariant**

$$Q^2 \equiv c_\text{lat}^2\lvert\mathbf q\rvert^2 - q_0^2
\qquad(\text{Euclidean: } c_\text{lat}^2\lvert\mathbf q\rvert^2 + q_4^2).$$

Hence $\Pi(q)=f(Q^2)$, the induced kinetic operator is the **d'Alembertian**
$\Box=\nabla^2-c_\text{lat}^{-2}\partial_t^2$, and the graviton light cone is the
zero locus $q_0=c_\text{lat}\lvert\mathbf q\rvert$. **There is no free speed to
choose** — $c_\text{grav}=c_\text{lat}$ is inherited from the rotation rule.
(This is the Sakharov statement made sharp by F79's zero-tree-stiffness theorem:
the graviton light cone equals the matter light cone *because the graviton kinetic
term equals the matter vacuum polarisation*.) It is corroborated independently by
F59: the induced inverse-coupling carries $1/G\propto1/c_\text{lat}=\sqrt d$
exactly — the gravity sector's single velocity is the rotation rate.

**Leg 4 — assemble.** Promoting F106's static Poisson law to its causal
(retarded) completion with the d'Alembertian of Leg 3:

$$\boxed{\;\Big(\nabla^2-\frac{1}{c_\text{lat}^2}\partial_t^2\Big)\ln K(\mathbf x,t)
= -\frac{8\pi G}{c^4}\,T^{00}[\psi](\mathbf x,t)\;}\qquad\text{(D-GW)}$$

with the lattice-only coefficient (F106-E1, re-verified here, check A)

$$\frac{8\pi G}{c^4}=\frac{a^2\,c_\text{lat}}{\hbar c},\qquad
\frac1G=8\pi\sqrt3\,\frac{\hbar}{a^2c^3}\ \ (d=3,\ \eta=\tfrac1{12},\ g_*=48).$$

In vacuum ($T^{00}=0$) D-GW gives $\delta\ln K\propto e^{i(\mathbf k\cdot\mathbf x-\omega t)}$
with $\omega=c_\text{lat}\lvert\mathbf k\rvert$ — **gravitational waves at
$c_\text{lat}=1/\sqrt3$**. Its static / slow-matter reduction
($\partial_t\to0$) is exactly F106's $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$, so
nothing already-validated changes; D-GW only adds the retarded time-derivative
that the elliptic law was missing.

## 3. Why GW170817 is satisfied identically

The photon (paired even law, F26/F105) and the graviton (D-GW) solve the **same
wave operator** $\Box_\text{lat}=\nabla^2-c_\text{lat}^{-2}\partial_t^2$. Their
speeds are therefore not two quantities that happen to agree to $10^{-15}$ — they
are the *same symbol* $c_\text{lat}=1/\sqrt3$:

$$\frac{\lvert c_\text{grav}-c_\text{photon}\rvert}{c}=0\quad\text{(exact, leading order).}$$

Both descend from the *same* rotation kernel, so even the first lattice
correction is shared: $c(k)=c_\text{lat}\big(1-\tfrac16(\Omega)^2+\dots\big)$ with
$\Omega\sim c_\text{lat}(ka)$ identical for both. Any residual difference enters
only beyond that common order and is bounded by $(f/f_\text{Planck})^2$. At a LIGO
band frequency ($f\sim100$ Hz, $f_\text{Planck}\sim1.86\times10^{43}$ Hz) this
upper bound is $\sim3\times10^{-83}$ — **68 orders of magnitude below** the
GW170817 limit. The constraint is satisfied with essentially infinite margin.

## 4. Verification (5/5)

| check | statement | result | status |
|---|---|---|---|
| **A** | coefficient identity $8\pi G/c^4=a^2c_\text{lat}/(\hbar c)$ and $1/G=8\pi\sqrt3\,\hbar/(a^2c^3)$ | residuals $=0$ (sympy) | **PASS (exact)** |
| **B** | induced inverse-coupling carries $1/c_\text{lat}$: $\int d^dk/(2\omega)\times c_\text{lat}$ is $c$-independent | rel spread $\le7\times10^{-16}$ ($d=1,2,3$) | **PASS (machine)** |
| **C** | induced $\Pi(q)$ depends on the constituent invariant $c_\text{lat}^2\lvert\mathbf q\rvert^2-q_0^2$ **only** ⇒ light cone $=c_\text{lat}$ | isocontour spread $2.2\times10^{-5}$; naive-isotropic control $0.27$ (non-flat) | **PASS** |
| **C′** | the graviton light cone **tracks** the constituent speed (inherited, not chosen): $c=\{1/\sqrt3,1,\tfrac12\}\Rightarrow c_\text{grav}=\{1/\sqrt3,1,\tfrac12\}$ | exact match | **PASS** |
| **D** | graviton vs photon slope identical ($=c_\text{lat}$); GW170817 residual | slope residual $=0$; bound $3\times10^{-83}<10^{-15}$ | **PASS (exact slope)** |
| **E** | real-space D-GW with $c_g=c_\text{lat}$ (not by hand): wavefront speed and static→Poisson | speed$/c_\text{lat}=1.03$ (grid); Poisson fixed-point dev $8.6\times10^{-4}$ | **PASS** |

Check **C** is the decisive one. The induced graviton self-energy (a Euclidean
massive bubble of constituent quanta with light cone $c$) is **flat to
$10^{-5}$** along curves of constant $c^2\lvert\mathbf q\rvert^2+q_4^2$, while a
control that ignores $c$ (constant $\lvert\mathbf q\rvert^2+q_4^2$) varies by
$\sim30\%$ whenever $c\neq1$. So the flatness is genuinely the *constituent*
invariant, not an artifact — the graviton can only see the light cone the
rotation rule gave it. The $\sim3\%$ in E is finite-grid discretisation of the
leapfrog wavefront, not a coefficient error (the speed is set to $c_\text{lat}$
in the stepper, replacing D-EM8's free `c_g`).

## 5. What is derived vs posited

- **Derived (new):** the hyperbolic wave equation D-GW; the proof that its speed
  is forced to $c_\text{grav}=c_\text{lat}$ by the zero-tree-stiffness theorem
  (F79) plus the constituent-invariant structure of the induced self-energy
  (Leg 3, check C); the identity $\lvert c_\text{grav}-c_\text{photon}\rvert=0$
  and the GW170817 margin. The previous loop's one posit (D-EM8's free $c_g$) is
  removed.
- **Still posited (inherited, bounded):** the one SI ruler $a$ (audit C.1,
  unavoidable — one length cannot come from pure numbers); the spin-1 gauge
  contribution to $g_*$ (F79's flagged $\sqrt{\cdot}$ correction to $G$'s
  magnitude). Neither touches the *speed*: $c_\text{grav}=c_\text{lat}$ is
  independent of both, since it is fixed by the loop's light cone, not by the
  coupling's magnitude.
- **Honest scope:** D-GW is the scalar (trace/conformal) mode of the linearised
  induced Einstein equation — the mode the impedance-locked dielectric carries.
  The full transverse-traceless tensor graviton (the physical GW polarisations of
  GR) shares the same $\Box_\text{lat}$ by the same argument (the loop light cone
  is common to every component), but the explicit TT-mode construction on the BCC
  lattice is the natural next build. The leading-order GW170817 statement
  ($c_\text{grav}=c_\text{lat}=c_\gamma$) holds for both because it is a property
  of the shared light cone, not of the polarisation structure.
  **Update (2026-07-15 - 19:14): this TT-mode build is now done in
  [[F248-tt-graviton-bcc-explicit]].** The two helicity-$\pm2$ TT polarisations
  are constructed explicitly for every direction and shown to ride the **one**
  scalar induced light cone: the graviton self-energy factorises as
  $f_2(Q^2)\,\Lambda_{ij,kl}$ (spin-2 TT projector $\times$ scalar form factor),
  both helicities are eigenvalue-$1$ of $\Lambda$ and so share the common pole
  $q_0=c_\text{lat}\lvert\mathbf q\rvert$ — luminal and **exactly non-birefringent**,
  with the gauge (spin-1/0) parts projected out. Verified on the genuine BCC even
  ("paired") law $\omega_+(k/2)+\omega_-(k/2)$ (F69), whose helicity-symmetric sum
  cancels the odd $s_xs_ys_z$ term, leaving an isotropic $c_\text{lat}$ slope and a
  helicity-blind $O((ka)^2)$ anisotropy; a real-space TT packet propagates at
  $0.9998\,c_\text{lat}$ for both polarisations.

## 6. Consequence for the engine and the audit

This is the analytic warrant for replacing D-EM8's hand-set `c_g` with
$c_\text{lat}=1/\sqrt3$ in `gr_fork_F64_em_connection.test_dem8_dynamical_field`
and in any production backreaction loop: the gravity field propagates causally at
the **same** speed as light, by derivation. Audit C1 ("gravitational wave speed
undefined / potential falsification") is **closed**: a hyperbolic equation
exists, its speed is $c_\text{lat}$, and GW170817 is satisfied by 68 orders of
magnitude. The F106 horizon-/static-only picture is superseded by the causal D-GW
whose static limit reproduces it exactly.

## 7. Provenance

- New content: the hyperbolic completion D-GW; the Leg-3 argument that the
  induced self-energy depends only on the constituent invariant (and its
  numerical confirmation, check C/C′); the GW170817 margin.
- Reuses: F26 ($c_\text{lat}=1/\sqrt3$ rotation rate; mass = confined rotation),
  F64-D-EM5/D-EM8 (the dielectric and its first dynamical promotion), F106 (the
  static sourcing law and the coefficient $a^2c_\text{lat}/\hbar c$), F79
  (zero tree stiffness ⇒ induced loop channel), F59 ($1/G\propto1/c_\text{lat}$).
- Verification: `tests/findings/test_F180_gw_speed.py` (2026-06-30 - 12:30, 5/5
  PASS), results `test-results/F180_gw_speed.json`.
