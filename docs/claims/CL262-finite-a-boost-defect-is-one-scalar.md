---
id: CL262
title: At finite lattice spacing the entire failure of Poincare covariance is the gradient of one scalar, the off-shell invariant mass, and it is exact on the cubic axes, O(k^3) for the paired-spinor photon and O(k^2) on a chiral branch
slug: finite-a-boost-defect-is-one-scalar
tier: headline
kind: deviation
status: narrowed
domain: [SR, QFT]
exactness: machine
findings: [F301, F327]
tests: [F301-boost-covariance-defect, F327-chiral-liv-bound]
modules: [casim.engine.interactions.derive_boost_covariance, casim.engine.interactions.derive_chiral_liv_bound]
constants: [c_lat]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-06
last_verified: 2026-08-26
provenance: authored
review_state: authored
confidence: high
---

# CL262 — The finite-$a$ Poincaré defect is one scalar, and its order is set by the channel's branch structure

## Statement

On the canonical BCC lattice, with $H=\Omega(\mathbf k)$, $P_i=k_i$, $x_i=i\partial_{k_i}$ and
$K_i=\tfrac1{2c^2}\{x_i,\Omega\}$, the **entire** failure of the Poincaré algebra is

$$D_i(\mathbf k)=\frac1{2c^2}\partial_i\bigl(\Omega^2\bigr)-k_i=\partial_i\Phi,
\qquad \Phi=\frac{\Omega^2-c_\text{lat}^2\lvert\mathbf k\rvert^2}{2c_\text{lat}^2},$$

so **finite-$a$ boost covariance is exactly the statement that the off-shell invariant mass does
not run with momentum.** $[K_i,P_j]=i\delta_{ij}\Omega/c^2$ holds for arbitrary $\Omega$ with no
defect, and the $[K_i,K_j]$ defect equals $\tfrac{i}{c^2}(D_ix_j-D_jx_i)$ — the same $D_i$, not a
second obstruction. $D_i$ is unchanged by $K_i\to K_i+f(\mathbf k)$ for any real $f$.

The defect is **zero to all orders in $ka$** along the three cubic axes, where
$\omega=c_\text{lat}\lvert k\rvert$ identically on both chiral branches and on the F26 even law.
Off the axes it is

$$\mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)\,\lvert k\rvert^3 \quad\text{(F26 even law, }O(\lvert k\rvert^3)\text{)},$$
$$\mathbf D^{(s)}=-s\,c_\text{lat}\,\bigl(k_yk_z,\;k_zk_x,\;k_xk_y\bigr) \quad\text{(chiral branch }s=\pm1,\ O(\lvert k\rvert^2)\text{)},$$

with $p=\hat k_x^2\hat k_y^2+\hat k_y^2\hat k_z^2+\hat k_z^2\hat k_x^2$ and
$q=\hat k_x^2\hat k_y^2\hat k_z^2$; radial values $-2/81$ on $\langle111\rangle$, $-1/72$ on
$\langle110\rangle$, $-11/648$ on $\langle211\rangle$, $0$ on $\langle100\rangle$. The even law's
extra order is the **chirality-oddness** of $b_2(\hat k)=-\tfrac13\hat k_x\hat k_y\hat k_z$, so
$\mathbf D^{(+)}=-\mathbf D^{(-)}$ at leading order and the paired channel cancels it — the same
helicity symmetrisation that makes the paired-spinor photon non-birefringent. Zero free inputs.

Operationally, for a boost of velocity $v$ along $\hat v$ the off-shell residual of the linear
Lorentz boost is $\Omega'-\Omega(\mathbf k')=v(\mathbf D\cdot\hat v)+O(v^2)$; in the 1D reduction
this is $D/k=1/\rho(m)-1=2\beta_\text{LV}/(1-2\beta_\text{LV})$, and on the BCC massive branch
$D_i\to(1/\rho(m)-1)k_i$ with the same $\rho(m)=m/(\sqrt{1-m^2}\arcsin m)$.

## What it extends

**Special relativity's kinematics, and the Poincaré algebra of relativistic quantum mechanics.**
Exact Lorentz covariance requires $\Omega^2-c^2\lvert k\rvert^2$ constant; the lattice does not
supply that, and this claim states precisely how much it fails by and in what direction. It is a
`deviation` from SR, not a derivation of it. It also extends F246: that finding gave the *dispersion*
coefficient $c_3(\hat k)=-(\sqrt3/216)(p+3q)$ and proved the even-power terms vanish; this converts
the same structure into a **covariance order** and supplies the chiral $k^2$ coefficient
$b_2(\hat k)$ that F246 left as two numbers.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §2 | $[K,P]$ exact; $[K,H]$ defect $=iD_i$; $[K,K]$ defect reduces to $D_i$; $D_i$ invariant under $K\to K+f(k)$ — all for arbitrary $\Omega$ | exact (sympy $0$) |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.2 | $\omega=c_\text{lat}\lvert k\rvert$ and $\mathbf D=0$ on $\langle100\rangle$, all orders, both branches and the even law | exact, $3.5\times10^{-46}$ |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.3 | $\mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)\lvert k\rvert^3$ over four directions | machine, $1.7\times10^{-17}$ |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.4–3.5 | $\mathbf D^{(s)}=-sc_\text{lat}(k_yk_z,\dots)$; $b_2=-\tfrac13\hat k_x\hat k_y\hat k_z$; chirality-odd cancellation | machine, $7.4\times10^{-18}$ / $7.9\times10^{-14}$ |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.6 | $D/k=1/\rho-1$ (1D, 12 figures) and $D_i\to(1/\rho-1)k_i$ (BCC massive) | machine, $4.7\times10^{-15}$ |
| record `F301-boost-covariance-defect` → `test-results/F301_boost_covariance.json` | 10/10, gate tier, `machine`, tol $10^{-12}$; six declared controls all verified red | machine |
| `docs/status/exactness-inventory.md` §F301 | twenty rows, per-leg class | — |

The binding tolerance is $8.3\times10^{-13}$ (the leading-order full-vector comparison), which is
why the card is `machine` and not `exact` even though seven legs are sympy zeros or $10^{-46}$.
Every numeric residual is truncation-limited **with its order separately verified** — the $b_2$
residual is checked to scale as $O(\lvert k\rvert^2)$ to $2.1\times10^{-5}$, and the off-shell
residual to scale as $O(v^2)$.

## Falsifier

Three independent kills, in decreasing order of reach:

1. **Observational — THIS HAS NOW FIRED (F327, 2026-08-26).** The stated test was: a measured
   dispersion for a chiral fermion channel excluding an $O(\lvert k\rvert^2)$ anisotropic term of
   the form $\propto\hat k_x\hat k_y\hat k_z$ at the model's coefficient, once converted through
   the F107 ruler. F327 did the conversion — $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}3^{1/4}/9=1.4662$,
   $E_\text{LV}=\tfrac92E_a=8.327\times10^{18}$ GeV — and the LHAASO/Crab electron limits exclude it
   by **7.05 decades** superluminal and **5.08 decades** subluminal. What the firing kills is the
   **physical assignment** (that an elementary fermion of this model rides a single chiral branch),
   recorded as **CL284**; the algebra of this card is untouched. That is why this card is `narrowed`
   rather than `withdrawn`. The front matter keeps `falsifier: stated` (the closed
   vocabulary has no `fired` value); that it has fired is recorded here and in `## Status & history`.
2. **Internal, structural.** Any $\Omega$ used by a live channel of this model for which
   $\Omega^2-c_\text{lat}^2\lvert k\rvert^2$ is *constant* off the cubic axes would contradict the
   claim that covariance is broken; conversely, a channel whose defect appears at an order other
   than the one its branch structure predicts (even $\Rightarrow O(\lvert k\rvert^3)$,
   chiral $\Rightarrow O(\lvert k\rvert^2)$) falsifies the mechanism.
3. **Algebraic.** A boost generator, of any form, for which the $[K,H]$ defect is *not* $\partial_i\Phi$
   — i.e. any $K$ outside $\tfrac1{2c^2}\{x_i,\Omega\}+f(\mathbf k)$ that still satisfies
   $[K_i,P_j]=i\delta_{ij}\Omega/c^2$ and closes the algebra on the canonical $P=k$. The claim that
   $D_i$ is the *complete* obstruction is the part most exposed here, and it is asserted only for
   generators linear in $x$.

## Status & history

`live` as stated. First issued with F301, 2026-08-06.

Two scope limits are part of the claim rather than caveats on it. **(a) Domain:** $x_i=i\partial_{k_i}$
is the position operator on the BZ torus, so every statement is for smooth wavepackets in the interior
of the zone, away from $\mathbf k=0$ and away from the edge. **(b) One-particle and free:** this is the
free one-particle algebra; interacting and multi-particle statements are not made.

**NARROWED 2026-08-26 (F327).** The broad form this card carried until then was that its whole
content — including the chiral $O(\lvert k\rvert^2)$ branch — was a `live` description of how the
model's channels propagate. F327 converted the chiral coefficient into physical units and confronted
it with the LHAASO/Crab electron limits; it is **outside them by 7.05 decades**. So the card is
narrowed to its **structural, per-channel** content:

> *Given a channel and its branch structure, the finite-$a$ Poincaré defect is $\partial_i\Phi$ and
> its order follows — even $\Rightarrow O(\lvert k\rvert^3)$, chiral $\Rightarrow O(\lvert k\rvert^2)$.*

Which channels the model may **use** is no longer part of this card. The chiral branch is now known
to be unavailable to any elementary matter field, and that exclusion is **CL284**. Everything the
evidence table above certifies is unchanged: no leg was re-run, no residual moved, and F301 is not
superseded.

**Superseded within this card:** the paragraph that read *"Nothing in this card should be read as
saying the chiral defect is observationally allowed or excluded — it is unconstrained by anything in
the tree."* It is now constrained, and excluded. F28's GRB/AGN limit is still structurally
inapplicable here (it constrains the *photon* $\lvert k\rvert^3$ term, F246) — the confrontation that
fired came from the electron sector instead, exactly as F301 §7 recommended.

Row A2 of the completeness rubric stays `PARTIAL` on the strength of this card and CL284 together;
ledger row **L8** closes with F327 and **L9** opens for the repair.

## Sources

- `findings/F301-finite-a-boost-covariance-poincare-defect.md`
- `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` (the confrontation that fired falsifier 1)
- `docs/claims/CL284-elementary-single-branch-fermion-excluded.md` (what the firing excludes)
- `findings/F246-f26-even-dispersion-subleading.md` (the $c_3$ closed form and even-power vanishing this builds on)
- `findings/F22-velocity-addition-deformed-formula.md` and `docs/reviews/F22-review-2026-08-04.md` (the $\rho(m)$ this reproduces)
- `docs/reviews/F24-remediation-2026-08-04.md` item 10 (the deferral this discharges)
- `docs/status/exactness-inventory.md` §F301
