# F56 — Deriving the Einstein coupling 16πG/c⁴ from the lattice + F25/F26 phase-matching

**Date:** 2026-05-29 - 18:20
**Status:** Partial — derivation attempt; 3/3 tests PASS. The geometric factor (16π) is derived exactly; the dimensionful G is reduced to the lattice spacing (Sakharov), which remains the one irreducible input. Full module reasoning in `gr_fork_F56_einstein_coupling_derivation.py`.
**Module:** new `ca-simulation/forks/gr_fork_F56_einstein_coupling_derivation.py` (additive; reuses `ca_bcc` for the F26 dispersion).
**Tests:** `model-tests/test_F56_einstein_coupling_derivation.py`; results `test-results/F56_einstein_coupling_derivation.json`.

## The question

F55 had to *posit* the linearised-Einstein coupling $16\pi G/c^4$. Can it be derived from the lattice and the F25/F26 phase-matching definition of $c_\text{lat}=d\Omega/d|\mathbf k|$? The coupling factors as

$$\frac{16\pi G}{c^4}=\underbrace{(16\pi)}_{\text{geometry}}\times\underbrace{G}_{\text{dimensionful}}\times c^{-4},$$

and each factor is examined separately.

## Part A — the 16π is pure lattice geometry (derived, exact)

**The 4π is the lattice solid angle.** The *bare* simple-cubic 6-neighbour Laplacian — with **no $4\pi$ inserted by hand** — has a point-source Green's function whose far field is $G(r)\to-1/(4\pi r)$. Measured: fitting $G(r)=-C/r+a+br^2$ on an intermediate shell gives $4\pi C=1.0002$ ($r^2=0.99999$, C2). The $4\pi$ in Newton's $\nabla^2\phi=4\pi G\rho$ is therefore not a choice — it is the solid angle of 3-D space as the lattice's long-wavelength modes resolve it.

**This is the same isotropy F25/F26 used for the light cone.** The small-$k$ rotational symmetry that makes the Green's-function coefficient exactly $4\pi$ is the same symmetry that makes $c_\text{lat}=d\Omega/d|\mathbf k|$ direction-independent. Measured light-cone slope along four directions: $c_\text{lat}=0.57734$ with isotropy spread $2.4\times10^{-5}$ — i.e. $1/\sqrt3$ in every direction (C2). The $4\pi$ of gravity and the isotropic light cone are one lattice fact.

**The step $4\pi\to16\pi$ is the trace reversal (F55), and it is forced.** Given Newton's $4\pi$, the weak-field relation $h_{00}=-2\phi/c^2$, and the static-dust trace reversal $\bar h_{00}=2h_{00}$ (F55), the tensor coupling $\xi$ in $\Box\bar h_{\mu\nu}=-\xi T_{\mu\nu}$ is uniquely $\xi=4\times(4\pi)\,G/c^4=16\pi G/c^4$, and the Einstein-tensor coupling is $\xi/2=8\pi G/c^4$ (C1, residual $0.0$, bit-for-bit). There is no freedom once $4\pi$ and the trace reversal are fixed.

## Part B — the dimensionful G is the lattice spacing (Sakharov)

A dimensionless lattice cannot manufacture a dimensionful constant. What it *can* fix (Sakharov / induced gravity) is $G$ in terms of the lattice cutoff. Integrating out the lattice's propagating modes induces an Einstein–Hilbert term whose coefficient is a Brillouin-zone integral over the F26 dispersion:

$$\frac{1}{16\pi G_\text{ind}}\ \propto\ \int_{\text{BZ}(\Lambda)}\frac{d^3k}{(2\pi)^3}\,\frac{1}{\omega(\mathbf k)}\ \propto\ \frac{\Lambda^2}{c_\text{lat}},\qquad \Lambda=\pi/\ell.$$

Measured (C3): the integral over the actual BCC dispersion scales as $\Lambda^{p}$ with $p=2.0008$ (target 2), and its coefficient matches the continuum estimate $\sqrt d\,\Lambda^2/(4\pi^2)$ to $0.03\%$. So:

- $G_\text{ind}\propto\ell^2$ — **the lattice spacing is the Planck length** ($\ell=\ell_P\sqrt d$ per Finding 10's identification).
- The phase-matching speed $c_\text{lat}=1/\sqrt d$ **enters the coupling's O(1) coefficient** ($1/G\propto\Lambda^2/c_\text{lat}=\sqrt d\,\Lambda^2$) — the F25/F26 link the question asked for.

## What is derived vs what remains an input

| Piece of $16\pi G/c^4$ | Status |
|---|---|
| $4\pi$ (Newton's solid angle) | **Derived** — bare lattice Green's-function far field, $4\pi C=1.0002$; same isotropy as F25/26 $c_\text{lat}$ |
| $4\pi\to16\pi$ (and $8\pi$ for $G_{\mu\nu}$) | **Derived exactly** — trace reversal (F55), residual $0.0$ |
| $G\propto\ell^2$ scaling | **Derived** — Sakharov BZ integral of F26 $\omega(k)$, exponent $2.0008$ |
| $c_\text{lat}=1/\sqrt d$ in the coefficient | **Derived** — phase-matching enters as $\sqrt d/(4\pi^2)$, matched to $0.03\%$ |
| absolute O(1) prefactor of $G$ | **Not derived** — scheme-dependent (one-loop induced-EH coefficient) |
| lattice spacing in metres | **Not derivable** — a dimensionless lattice cannot set it; choosing it *is* choosing $G$ |

**Honest headline:** everything in $16\pi G/c^4$ except the choice of lattice spacing is derivable — the $16\pi$ from lattice isotropy (F25/F26) plus trace reversal (F55), exactly; and the $\ell^2$-scaling of $G$, with its $c_\text{lat}=1/\sqrt d$ coefficient, from the F26 phase-matching dispersion via Sakharov. The single irreducible input is the lattice spacing in physical units — and Finding 10 already showed that is the Planck length (up to $\sqrt d$). The model does not derive Newton's constant as a pure number, but it shows $G$ is not *independent* of $c$ and $\ell$: it is locked to them by $G=\ell^2c^3/\hbar$.

## Caveats

- Part B *assumes* the Sakharov mechanism (a one-loop Einstein–Hilbert term induced by the lattice modes) rather than deriving it from the CA update rule. What is computed is the scaling and the $c_\text{lat}$-dependence of that induced term, not its existence.
- The absolute induced-$G$ prefactor is famously scheme/field-content dependent (the same ambiguity as the induced cosmological constant); only the $\Lambda^2$ exponent and the $\sqrt d$ factor are scheme-independent.
- Part A's $4\pi$ uses the simple-cubic stencil for an unambiguous demonstration; the BCC stencil shares the same isotropic continuum limit (F30/F37 anisotropy is higher-order), so the far-field $4\pi$ is unchanged.

## New exact result (exactness inventory)

- **C1** coupling lock $\xi=16\pi G/c^4$ (and $8\pi G/c^4$ for $G_{\mu\nu}$) forced by Newton-$4\pi$ + trace reversal — residual $0.0$ (Tier-1 algebraic).

## Follow-ups

- Derive the induced Einstein–Hilbert term *from the CA update rule* (the back-reaction of the F52/F55 leg-fields on the propagating modes), turning Part B's assumed Sakharov mechanism into a derivation and pinning the O(1) prefactor.
- Connect to Finding 10's three $(a,\tau)$ resolutions: the Sakharov $G\propto\ell^2$ plus $c_\text{lat}=1/\sqrt d$ may select one of them, fixing the tick/cell convention.

## Relation to other findings

Closes the open coupling question left by **F55** (and F52's $4\pi G$). Builds on **F25/F26** (the rotation-rate $c_\text{lat}=1/\sqrt d$ and its small-$k$ isotropy), **F55** (trace reversal), and **Finding 10** (lattice spacing ↔ Planck length, with the $\sqrt d$ factor that reappears here in the Sakharov coefficient).
