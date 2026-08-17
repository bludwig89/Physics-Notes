---
id: CL263
title: No single momentum reparametrisation can restore exact Lorentz covariance for both the photon and the fermion on this lattice, and the obstruction is the chiral k^2 dispersion term with coefficient one third of kx ky kz
slug: no-universal-momentum-map
tier: supporting
kind: no_go
status: live
domain: [SR, QFT]
exactness: machine
findings: [F301]
tests: [F301-boost-covariance-defect]
modules: [casim.engine.interactions.derive_boost_covariance]
constants: [c_lat]
supersessions: []
reviews: []
rolls_up_to: CL262
falsifier: stated
first_issued: 2026-08-06
last_verified: 2026-08-06
provenance: authored
review_state: authored
confidence: high
---

# CL263 — The DSR repair is per-channel, therefore not a spacetime symmetry

## Statement

A nonlinear (doubly-special-relativity type) momentum map **does** restore an exact Minkowski mass
shell on this lattice at finite $a$. For a chiral branch with mass $m$ and $n=\sqrt{1-m^2}$,

$$\sin^2\omega(\mathbf k,m)-(1-m^2)\sin^2\omega_0(\mathbf k)=m^2\quad\text{identically},$$

$\omega_0=\arccos u_s$ the massless branch of the same chirality, so $E=\sin\omega$,
$c\lvert\mathbf P\rvert=n\sin\omega_0(\mathbf k)$, $\hat{\mathbf P}=\hat{\mathbf k}$ gives
$E^2-c^2\lvert\mathbf P\rvert^2=m^2$ for every $m$ and every $\mathbf k$ in the zone, and the induced
boost closes as a group. **Mass therefore enters exactly relativistically**: all lattice deformation
sits in the mass-*independent* map $\mathbf k\mapsto\sin\omega_0(\mathbf k)$.

**This is nevertheless not Lorentz covariance**, because a spacetime symmetry must act through one
map for every channel and this one does not. Universality requires the channels' dispersions to
coincide, and

$$\Omega_\text{even}(\mathbf k)-\omega_+(\mathbf k)=+\tfrac13\,\hat k_x\hat k_y\hat k_z\,\lvert k\rvert^2+O(\lvert k\rvert^3),$$

which is non-zero except on the three coordinate planes $\hat k_x\hat k_y\hat k_z=0$. So the DSR
loophole is **closed** for the multi-channel model, and the obstruction is the *same* chiral $k^2$
term that gives the chiral branch its worse covariance order in CL262.

## What it extends

**Doubly special relativity as applied to quantum cellular automata** — specifically the nonlinear
realisation of Bibeau-Delisle *et al.* (EPL 101, 60005, 2013; arXiv:1310.6760) and Bisio, D'Ariano
and Perinotti (Phil. Trans. R. Soc. A 374, 2016; arXiv:1503.01017), which F22's review identified as
the correct repair of F22's failed linear-boost claim. Those results are single-channel. This claim
says the repair does not survive the step to a model with more than one propagating channel, and
gives the coefficient at which it fails. It also supplies the BCC analogue of the 1D
$\sin^2\omega-n^2\sin^2u=m^2$ identity, which F22 recorded as not existing.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.1 | $\sin^2\omega-(1-m^2)\sin^2\omega_0=m^2$ identically, 3 masses × 5 directions × 3 $\lvert k\rvert$ out to 1.7 | exact, $1.3\times10^{-46}$ |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.1 | boosted state re-inverted onto the branch lands on the lattice shell; two boosts equal the velocity-composed single boost | machine, $1.3\times10^{-46}$ / $4.4\times10^{-47}$ |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.7 | $\Omega_\text{even}-\omega_+=\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2$ over three directions | machine, $7.9\times10^{-14}$ |
| record `F301-boost-covariance-defect`, control B9 | the gap **vanishes** on a coordinate plane ($4.8\times10^{-8}$), so it is a real angular function and not a fit artifact | control |
| record `F301-boost-covariance-defect`, control B8 | the canonical $\mathbf k$ does **not** sit on the deformed shell ($2.1\times10^{-2}$) — the two momenta are genuinely different objects | control |

## Falsifier

1. A momentum map $\mathbf k\mapsto\mathbf P$, single-valued on the zone interior, under which the
   F26 even photon law **and** a chiral Weyl branch are *both* exactly Minkowski. Because both maps
   are forced to the radial form $\lvert\mathbf P\rvert=\sin\Omega_\text{ch}(\mathbf k)/c$, this
   requires $\Omega_\text{even}(\mathbf k)=\omega_+(\mathbf k)$, which the measured
   $\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2$ gap excludes off the coordinate planes.
   A map *not* of the radial form — one that rotates $\hat{\mathbf P}$ away from $\hat{\mathbf k}$
   — is the honest gap in this argument and is not excluded here.
2. A demonstration that the physical fermion channel is **not** on a single chiral branch — e.g. that
   the F91 classification's chiral assignment is wrong and the fermion propagator is even-law like
   the photon. That would remove the gap by making the two channels coincide, and would falsify this
   claim by falsifying its premise rather than its algebra.
3. Any $(m,\mathbf k)$ inside the accessible domain where the massive shell identity of §3.1 fails.

## Status & history

`live` as stated, first issued with F301, 2026-08-06. Recorded as `kind: no_go`: it is an exclusion,
and per `docs/claims/README.md` it is part of the falsification record.

**The narrow form matters and is the form stated.** What is excluded is a *universal radial*
momentum map. What is **not** excluded: (a) a per-channel DSR realisation, which exists and is exact
— that is the first half of this card, not a concession; (b) a non-radial map; (c) any statement about
multi-particle additivity of the deformed $\mathbf P$ (the "soccer-ball" problem), which is untouched
here and would be a second, independent obstruction if it fails.

## Sources

- `findings/F301-finite-a-boost-covariance-poincare-defect.md` §3.1, §3.7, §4
- `findings/F22-velocity-addition-deformed-formula.md` §"Corrections" and §"Prior art"
- `docs/reviews/F22-review-2026-08-04.md`
- `findings/F91-pairing-classification-theorem.md` (even-vs-chiral propagator classification — the premise this rests on)
- A. Bibeau-Delisle *et al.*, EPL **101**, 60005 (2013), arXiv:1310.6760
- A. Bisio, G. M. D'Ariano, P. Perinotti, Phil. Trans. R. Soc. A **374** (2016), arXiv:1503.01017
