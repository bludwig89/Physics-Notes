# F271 — The k-resolved dielectric photon propagator: Weyl ordering and the second-order half-step

*2026-08-01 - 01:40. Roadmap **P3.6** follow-through. Supersedes the eikonal `dielectric_mix_half` (F270 §4) for the photon channel.*
*Status: **established** for the operator's exactness, convergence and norm behaviour; the deflection **coefficient** against GR is explicitly not claimed.*

**Test record:** record `P3.4-P3.6-total-energy-and-gravity-loop` (tier gate) — `tests/casim/test_total_energy_and_gravity_loop.py` T8b–T8d, T9, T10: uniform $K$ exact with no free parameter (E2/E8), second-order convergence and converging norm drift (E3/E4), and the bend's exact-zero baseline, linearity and direction (E5–E7); record `F276-curved-weyl-ordering-second-order` (tier gate) — the same two corrections carried into the 2-D reference this finding handed back. Declared 2026-08-19.

## 1. The problem F270 left open

F270 closed the gravity loop on the gauge side, but only at **eikonal** order: the
dielectric was applied as a rotation by $\delta = \tfrac{\Delta t}{2}\omega_0(1/K-1)$
about a single, *stated* central rate $\omega_0$. That is a free parameter, and its
error is $O(1)$ and does not converge to anything.

The obstruction was real. For the impedance-matched F64 dielectric ($A=1/K$, $B=K$,
$AB\equiv1$) the metric is $ds^2=-Ac^2dt^2+B\,dx^2$, so the local coordinate light
speed is $c\sqrt{A/B}=c/K$, and F64 states the mechanism as a renormalisation of the
rotation *rate*:

$$\Omega_K(x,k)=\Omega_\text{pair}(k)\,/\,K(x)$$

This is **position-dependent and momentum-dependent at once**, so it is diagonal in
neither basis and no single homogeneous FFT can apply it. That is why deflection had
lived only in `forks/gravity/gr_fork_F64_em_connection.py`.

## 2. The resolution is lifted, not invented

`lattice.curved.weyl_step_2d_varc_strang` already solves exactly this structure for
the variable-$c$ 2-D Weyl walk, and already reproduces Snell's law in this codebase.
Its construction splits the generator about its mean:

$$s(x)\equiv 1/K(x) = s_0 + \delta(x),\qquad s_0=\langle s\rangle$$

* $s_0\,\Omega(k)$ — diagonal in $k$, applied as an **exact unitary** rotation;
* $\delta(x)\,\Omega(k)$ — applied perturbatively, $\Omega$ in Fourier space and
  $\delta$ in position space, Strang-symmetrised and sub-cycled.

Lifted from the 2-spinor to the 3-D $(E,B)$ pair this is `photon_step_dielectric`.
**Nothing new is posited.**

## 3. Two corrections the 2-D reference does not have

Lifting it verbatim gave a scheme that was **first order and did not conserve norm**.
Both defects are derivable, and so are both fixes.

### 3.1 Weyl (symmetric) ordering — the norm defect

The classical quantity being promoted to an operator is the product
$\delta(x)\Omega(k)$. Position and momentum do not commute, so *the* operator is not
defined until an ordering is chosen — and the choices are not equivalent.

The asymmetric $\delta\,\Omega$ (what `_half_step_dH` uses) is **not self-adjoint**,
so $\delta\Omega J$ is not antisymmetric and the evolution is **not orthogonal at any
step size**. Measured: norm drift **plateaus at $1.1\times10^{-5}$** and stops
improving. Sub-stepping reduces the Trotter error but cannot remove a non-unitarity
present in the generator itself.

The symmetric product $M=\tfrac12(\delta\Omega+\Omega\delta)$ is self-adjoint by
construction; $J$ is real antisymmetric with $J^2=-\mathbb{I}$; so $MJ$ is real
antisymmetric on the doubled $(E,B)$ space and $e^{MJ}$ is **exactly orthogonal**.
The only residual is then truncation, which converges: measured norm drift falls like
$1/n_\text{sub}^3$, reaching $2\times10^{-10}$ at $n_\text{sub}=64$.

Cost: one extra FFT round trip. It is the difference between an error that converges
and one that does not.

### 3.2 The $h^2$ term — the order defect

Because $J$ commutes with $M$ and $J^2=-\mathbb{I}$, exactly

$$e^{hMJ}=\cos(hM)\,\mathbb{I}+\sin(hM)\,J
=\mathbb{I}-\tfrac{h^2M^2}{2}+hMJ+O(h^3)$$

Keeping only $\mathbb{I}+hMJ$ — the first-order Taylor the 2-D reference uses — leaves
an $O(h^2)$ local error that Strang symmetrisation does **not** cancel, so the scheme
is globally *first* order. Measured convergence exponent: **1.0**. Carrying
$-h^2M^2/2$ restores the second order Strang is supposed to deliver: exponent
**2.00**, and the error at $n_\text{sub}=8$ falls from $3.0\times10^{-2}$ to
$3.7\times10^{-4}$ — a factor of 80.

**Both defects are present in `lattice.curved._half_step_dH` and therefore in every
F64-fork variable-$c$ result.** That is a genuine, unscheduled item this finding
hands back to the gravity fork; it is not fixed here.

## 4. Evidence

| # | Property | Result |
|---|---|---|
| E1 | $K\equiv1$ reproduces `photon_step_spectral` | **bit-identical** |
| E2 | uniform $K$ = exact rotation at $\Omega(k)/K$ | $4\times10^{-15}$ |
| E3 | Trotter convergence, inhomogeneous $K$ | exponent **2.00** |
| E4 | norm drift, inhomogeneous $K$ | $7.6\!\times\!10^{-6}\to1.9\!\times\!10^{-9}$ over $n_\text{sub}\,2\to32$; **converges** |
| E5 | zero gradient | bend **exactly 0** |
| E6 | response to $\nabla K$ | **linear** (factor 1.9973 for a factor 2) |
| E7 | direction | toward higher $K$ (slower medium) ✓ |
| E8 | free parameters | **none** ($\omega_0$ eliminated) |

**E2 is the sharp one.** A uniform dielectric is *exact*: $\delta\equiv0$, every mode
is slowed by exactly $1/K$, the step is exactly unitary. The eikonal cannot reproduce
this at any $\omega_0$ — it would need $\omega_0=\Omega(k)$, which is precisely the
$k$-dependence it replaces with a number.

## 5. What is deliberately **not** claimed

**The deflection coefficient.** A gradient-index test gave a bend whose ratio to the
continuum ray equation $d^2y/dx^2=(1/K)\partial_yK$ was 1.25 — which looked like a
25% error. It is not:

* the closed form for the finite-$k$ dispersion correction,
  $R=\Omega''_\perp\Omega/\Omega'^2$, evaluates to **0.9957** at the test's
  wavenumber, so dispersion does **not** explain 1.25;
* the ratio is **strongly packet-width dependent** — 1.455, 1.092, 0.959 at
  $\sigma=2.5,4.0,6.0$ — i.e. it converges toward 1 as the packet widens into the
  geometric-optics regime.

So 1.25 was a **narrow-packet artifact**: a finite packet in a varying medium is not
a ray, and its intensity centroid moves for reasons other than ray bending. The
operator is consistent with the ray equation to a few percent once geometric optics
applies. **A tight assertion on that number would be pinning an artifact**, so the
test asserts only direction, linearity and the exact-zero baseline.

Confronting the deflection against GR's $4GM/c^2b$ needs open boundaries, a weak
field and a large lattice — the F64 fork's battery, not a gate-tier test. **Unstarted.**

**Exact unitarity.** The half-step is a truncated exponential, so the step is
*convergently* unitary, not machine-unitary at finite $n_\text{sub}$. The closed form
$e^{hMJ}=\cos(hM)+\sin(hM)J$ with self-adjoint $M$ exists but needs operator functions
of a non-diagonal $M$. That is the remaining refinement.

**Block-spin.** A gravitating photon on a coarse lattice now **raises**. The
renormalised rule $\Omega_b(\kappa)=\Omega(\kappa/b)$ and the dielectric's own
coarse-graining have not been shown to commute (F133 covers the free rule only), and
guessing would put an unverified factor inside a gravity result.

## 6. Cross-references

`src/casim/engine/gauge/photon.py` (`photon_step_dielectric`, `_M_weyl`,
`_dielectric_half`) · `src/casim/engine/lattice/curved.py` (the 2-D reference, which
carries both defects) · [[F270]] (the eikonal this supersedes) · F64 (D-EM5/8/9) ·
F26/F69 (the even rotation law) · `tests/casim/test_total_energy_and_gravity_loop.py`
T8b–T8d, T9, T10
