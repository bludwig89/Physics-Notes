# F130 — A proven block-spin RG scheme (gauge + gravity sectors)

`2026-06-11 - 04:17`

**Status.** Phase-1 gate of `docs/roadmaps/roadmap-scale-to-real-space.md`.
Gauge + gravity half complete; the free-photon half is the concurrent **F129**.
Module `ca-simulation/ca_blockspin.py`; tests
`tests/findings/test_F130_blockspin_gauge_gravity.py` (30/30 PASS).

---

## 1. Why this is the gate

The canonical cell is $a = 1.066\times10^{-34}$ m (F107). A literal cell-by-cell
fill of one proton is $\sim4\times10^{57}$ cells — permanently off the table.
"Analogous to real space" must therefore mean a **renormalised / coarse-grained**
lattice in which one super-cell stands in for $b^d$ physical cells, *provided the
emergent dynamics is provably preserved*. F130 supplies that proof for the
electric (gauge) and gravitational (dielectric) sectors; without it every later
phase is a bigger toy, not a smaller universe.

## 2. The transform $R_b$

The Kadanoff block average groups $b^d$ fine cells into one super-cell. For a
scalar / EM field on a periodic fine lattice (spacing 1),

$$(R_b f)(X) = b^{-d}\!\!\sum_{r\in[0,b)^d}\! f(b\,X + r).$$

Two fields block differently, and *that distinction is the physics*:

- **Electric flux** (a 1-form) blocks by **sum** across the coarse face
  (Migdal–Kadanoff bond-moving), so Gauss's law telescopes — §4.
- **The gravity dielectric** blocks in its **log** $u=\tfrac12\ln K$ (the linear
  Poisson potential), so the reciprocal lock $A\!\cdot\!B\equiv1$ survives — §5.

The dispersion is a property of the *rule*, not the field. Blocking attenuates
each mode by a real, helicity-blind form factor $D_b(k)=\sin(bk/2)/[b\sin(k/2)]$
($D_b(0)=1$) and rescales the Brillouin zone by $b$. The coarse rule, written in
coarse lattice units (coarse spacing $=b$), is therefore

$$\boxed{\;\Omega_\text{coarse}(\kappa) = \Omega(\kappa/b),\qquad \kappa\in(-\pi,\pi]^d.\;}$$

Everything below follows from this one substitution.

## 3. Dispersion theorems

### T1 — $c_\text{lat}$ is an RG fixed point (exact)

The physical speed is $c_\text{phys} = (b/\tau)\,d\Omega_\text{coarse}/d\kappa\big|_0$.
With $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$,

$$c_\text{phys} = \frac{b}{\tau}\cdot\frac1b\,\frac{d\Omega}{dk}\Big|_0 = \frac1\tau\,\frac{d\Omega}{dk}\Big|_0,$$

independent of $b$. Measured: $b\cdot c_\text{coarse}(b) = 1/\sqrt3$ for
$b\in\{1,2,3,4,5\}$ along the axis, face-diagonal and body-diagonal alike, to the
fit floor $<10^{-9}$. The continuum light speed is a marginal (eigenvalue $b^0=1$)
direction — the fixed point itself.

### T2 — lattice-artifact (LIV) operators are irrelevant (exact)

Write the velocity correction at physical momentum $q$ on a lattice of spacing
$s$ as $v(q)/c = 1 + \sum_{n\ge2} g_n\,(q\,s)^n$. Demanding the *physical* velocity
be the same whether represented on the fine ($s=1$) or coarse ($s=b$) lattice
forces the coarse coupling

$$g_n^{(b)} = b^{-n}\,g_n,\qquad \lambda_n = b^{-n} < 1 \quad(n\ge2).$$

Every artifact operator shrinks under coarse-graining, so $\Omega = c\lvert k\rvert$
is the **attractive IR fixed point**. (In the roadmap's $\Omega$-power index
$m=n+1$ this reads $\lambda = b^{1-m}$, $m\ge2$ — the same statement.)

The leading even-law operator is anisotropic (F30): identically zero on a cubic
axis, maximal on the body diagonal where

$$\Omega(k) = \tfrac1{\sqrt3}\lvert k\rvert\Big(1 - \tfrac{\lvert k\rvert^2}{162} + O(k^4)\Big)
\;\Longleftrightarrow\; \frac{\delta v_g}{c} = -\frac{k^2}{54},$$

i.e. $g_2=-1/162$, reproducing F30 / $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$. Measured
$g_2 = -0.00617284$ (vs $-1/162=-0.00617284$). The eigenvalue is verified to
$<10^{-10}$ at $n=2$ by **matched sampling**: the coarse fit samples $\kappa_i=b\,k_i$,
so both fits share the same right-hand side and differ only by the $b^{2j}$ column
rescale — making $\lambda_n=b^{-n}$ a round-off-floor identity, independent of fit
quality.

## 4. Gauge sector — Gauss's law survives blocking (T3a)

On a periodic lattice the electric field lives on links, $E_a[x]$, with site
divergence $(\text{div}\,E)(x)=\sum_a\big(E_a[x]-E_a[x-\hat e_a]\big)$ — the F110
Kogut–Susskind convention. Block the flux as coarse-face sums (a coarse $+a$ link
carries the sum of the $b^{d-1}$ fine $+a$ links piercing the coarse face) and the
charge as block-sums. Then summing the fine divergence over a $b^d$ block
telescopes — interior fine fluxes cancel, only the coarse-face fluxes survive — so

$$\text{div}_\text{coarse}\,E_\text{coarse}(X) = \sum_{x\in\text{block}\,X}(\text{div}\,E)(x) = Q(X),$$

the total enclosed charge. The coarse run sees exactly the right number of charges
in each super-cell. For integer ($\mathbb Z$-flux, F110 dual basis) fields the
residual is **identically 0**; for continuous fields it is the round-off floor
$<10^{-12}$ ($b\in\{2,3,4\}$).

**Confinement is the one relevant direction (C1).** The string tension is the
F110 static-potential slope; in the strong-coupling (confined) phase
$\hat\sigma = g^2/2$ exactly ($\lambda=0$). Block-spin merges $b$ parallel fine
links into one coarse link (bond-moving), so the coarse link carries $b\times$ the
energy per unit coarse length: $g^2_\text{coarse}=b\,g^2_\text{fine}$,
$\hat\sigma_\text{coarse}=b\,\hat\sigma_\text{fine}$, **RG eigenvalue
$\lambda_\sigma=b>1$ (relevant)** — the lone IR scale, in sharp contrast to the
irrelevant LIV operators ($b^{-n}<1$). The physical confining energy
$V(R_\text{phys})=\sigma_\text{phys}R_\text{phys}$ is therefore invariant: a coarse
F110 run on $b\times$ fewer plaquettes (bond-moved coupling) reproduces the fine
$V(b\cdot R)$ to machine precision ($<10^{-12}$, $b\in\{2,3\}$). The would-be
deconfining magnetic coupling $\lambda$ deforms $\hat\sigma$ only by a fraction
$r(\lambda)\propto\lambda^2/g^4$ that shrinks as $b^{-2}$ (since $\hat\sigma$ grows
by $b$ and $c_2\propto1/g^2$): $\lambda$ is **irrelevant**, so the $\lambda=0$ area
law is the attractive IR fixed point. One relevant scale (confinement),
everything else irrelevant.

## 5. Gravity sector — the dielectric survives blocking (T3b)

Gravity is the impedance-matched dielectric $K=e^{2u}$, $u=-\Phi/c^2$, $A=1/K$,
$B=K$, with the reciprocal lock $AB\equiv1$ (F64, PPN $\beta=\gamma=1$) and the
linear source law $\nabla^2\ln K = -T^{00}$ (F106, $G_\text{lat}=1/72\pi$).

**The RG-covariant variable is $u$, not $K$.** Averaging $u$ keeps
$A\cdot B = e^{-2\bar u}e^{+2\bar u}=1$ pointwise — the impedance match (hence
non-birefringence) is preserved to $1.1\times10^{-16}$. Averaging $K$ *directly*
breaks the lock by the Jensen gap $\langle e^{2u}\rangle \ge e^{2\langle u\rangle}$
(measured max gap $1.8\times10^{-3}$ on a smooth potential, zero for a constant) —
it over-stiffens the lattice. Because $\Phi$ obeys a **linear** Poisson equation,
$u$ is also the natural superposition variable; the two facts are the same fact.

The source law is form-invariant in the IR: the physical coarse Laplacian
$\tfrac1{b^2}\nabla^2_\text{coarse}(R_b u)$ converges to $R_b(\nabla^2 u)$ as the
potential's wavelength grows, with a residual that **itself coarse-grains away as
$b^{-2}$** (relative error halves to $\div4$ per length-doubling, → exactly
$1/b^2$). The gravity discretisation error is, like the LIV operators of T2, an
irrelevant operator — a small unification.

## 6. Propagator class is preserved (T3c)

$D_b(k)$ is a real scalar per mode, so it commutes with the even (real $2\times2$)
rotation $R(\Omega)$: $[R_b,R(\Omega)] = 0$ to $2.9\times10^{-14}$. A real,
helicity-blind block kernel cannot mix the F91 even/chiral propagator classes —
the $\gamma$/gluon even law and the $W^\pm$ chiral law keep their branch structure
under coarse-graining.

## 7. What is and isn't established

| Claim | Status |
|---|---|
| $c_\text{lat}$ fixed point, all $b$, all directions | exact (T1) |
| LIV operators irrelevant, $\lambda_n=b^{-n}$ | exact (T2) |
| Leading $g_2=-1/162$ reproduces F30 / $E_{\text{QG},2}$ | machine (T2num) |
| Gauss's law under blocking (integer flux) | exact, residual $0$ (T3a) |
| Dielectric lock $AB=1$ under log-averaging | exact (T3b) |
| $u$ (not $K$) is the covariant variable (Jensen gap) | exact (T3b) |
| Poisson source law IR form-invariance | machine, $O(b^{-2})$ (T3b) |
| Even/chiral propagator class preserved | machine (T3c) |
| Confinement σ relevant, $\lambda_\sigma=b$; coarse V invariant | exact / machine (C1) |
| Deconfining $\lambda$ irrelevant ($\approx b^{-2}$) | quantitative (C1) |

**Scope / honest limits.** This proves the *kinematic* RG — the rule, the
constraints (Gauss, $AB=1$), the propagator classes and the confining scale all
survive $R_b$. The Phase-2 question (does a *coarse-grained bound state* reproduce
the fine spectrum?) is answered separately in **F131**. It does **not** yet run
the block-spin kernel as a first-class CASIM engine operation (Phase 4). The
free-photon dispersion RG is the concurrent **F129**; F130 consumes its dispersion
read-only and does not re-derive it.

## 8. Files

- `ca-simulation/ca_blockspin.py` — $R_b$, the dispersion RG, and the gauge /
  gravity / propagator-class / confinement checks. Pure numpy for the field
  sectors; consumes `ca_photon_pair.pair_dispersion`,
  `ca_wmu._f26_rotation_step`, `ca_gravity`, and the F110 link Hamiltonian
  (`ca_link_hamiltonian`) read-only for confinement.
- `tests/findings/test_F130_blockspin_gauge_gravity.py` — 38 tests (T1–T3c, C1).
- Exactness inventory rows #188–191 + #192 (exact), #66–67 (machine).
