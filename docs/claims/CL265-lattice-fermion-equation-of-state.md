---
id: CL265
title: 'The lattice corrections to a relativistic Fermi gas are closed-form pure numbers exactly 31/4 times the photon''s, 3/7 of the coefficient is carried by a branch-odd term the photon cancels, and C_u/C_w = 15/2 holds for both because it is a homogeneity theorem'
slug: lattice-fermion-equation-of-state
tier: supporting
kind: derivation
status: live
domain: [QFT, SM]
exactness: exact
findings: [F309, F300, F26, F67, F107]
tests: [F309-gstar-model-content]
modules: [casim.engine.interactions.thermodynamics_gstar]
constants: [c_lat, a_over_ellP]
supersessions: []
reviews: []
rolls_up_to: CL260
falsifier: stated
first_issued: 2026-08-11
last_verified: 2026-08-11
provenance: authored
review_state: authored
confidence: high
---

# CL265 — The lattice equation of state of a relativistic Fermi gas

## Statement

On the model's own single-branch BCC Weyl dispersion
$\omega^\pm(\mathbf k)=c_\text{lat}|\mathbf k|\bigl[1\mp b(\hat n)|\mathbf k|-a(\hat n)|\mathbf k|^2\bigr]+O(|\mathbf k|^4)$
with $b(\hat n)=\hat n_x\hat n_y\hat n_z/\sqrt3$ and $a(\hat n)=4A(\hat n)$ ($A$ being CL260's
photon anisotropy), the equilibrium Fermi gas of a branch-balanced Weyl pair obeys $w=1/3$ in
the infrared and carries leading corrections that are closed-form pure numbers times
$\Theta^2$, $\Theta=k_BT\tau/\hbar$:

$$\frac{u}{u_\text{SB}}-1=\frac{310\pi^2}{441}\Theta^2,\qquad \frac13-w=\frac{124\pi^2}{1323}\Theta^2,\qquad \frac{s}{s_\text{SB}}-1=\frac{31\pi^2}{49}\Theta^2,\qquad \frac{C_u}{C_w}=\frac{15}{2}.$$

Three exact statements follow, and the project asserts all three:

1. **Each fermionic coefficient is exactly $31/4$ times CL260's photonic one**, and $31/4$
   factors as $7$ (geometry: $(\langle a\rangle+3\langle b^2\rangle)/\langle A\rangle$ with
   $\langle a\rangle=4/315$, $\langle b^2\rangle=1/315$, $\langle A\rangle=1/315$) times
   $31/28$ (statistics: $(1-2^{-5})/(1-2^{-3})$, the Fermi/Bose ratio of the $y^5$ moment
   over that of the $y^3$ moment).
2. **The branch-odd term $b(\hat n)$ carries $3/7=42.857\,\%$ of the coefficient, exactly.**
   It is the term the paired photon cancels (F67/F68 non-birefringence); a single Weyl branch
   keeps it. Its angular mean is zero by parity, so it contributes only through
   $\langle b^2\rangle$ — at second order, at exactly the order the anisotropic term enters.
3. **$C_u/C_w=15/2$ is a theorem of degree-3 homogeneity**, not a photon fact and not a
   statistics fact: $\delta p/\delta u=3/5$ separately for the $\langle a\rangle$ and the
   $\langle b^2\rangle$ channel, so the ratio is invariant under deleting either.

Zero free parameters.

## What it extends

Continuum QFT gives the relativistic Fermi gas $\rho=(7/8)(\pi^2/30)gT^4$ and $p=\rho/3$ with
no correction of any kind — the discreteness that would produce one does not exist in it.
This claim derives both from a discrete walk and supplies the correction the continuum theory
has no way to generate, for **matter** rather than radiation. It also strengthens CL260's own
$C_u/C_w=15/2$ from a measured photon coincidence to a statistics-independent theorem, and it
corrects the natural expectation that the branch-odd term — which vanishes on angular average
and cancels for the photon — drops out: it does not, and it is the larger of the two lattice
channels after the isotropic one.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F309-gstar-from-model-content.md` §2 | closed forms $b=\hat n_x\hat n_y\hat n_z/\sqrt3$, $a=4A$ against `bcc_dispersion`; $\langle a\rangle=4/315$, $\langle b^2\rangle=1/315$ | exact / $7.5\times10^{-15}$ |
| `findings/F309-gstar-from-model-content.md` §3 | the three coefficients against Brillouin-zone quadrature | exact vs $\le1.7\times10^{-4}$ |
| `findings/F309-gstar-from-model-content.md` §3.1 | the $31/4=7\times31/28$ factorisation and the $15/2$ invariance | exact identity |
| record `F309-gstar-model-content` (gate) | GS-2, GS-2a, GS-3, GS-4, GS-5, GS-6, GS-7 | — |
| `test-results/F309_gstar_model_content.json` | the artifact | — |

The residual between closed form and quadrature scales as $\Theta^2$ across the fit window
($1.4\times10^{-4}$ at $\Theta=0.002$, $1.4\times10^{-2}$ at $\Theta=0.02$), i.e. it is the
next term in the series and not numerical error.

## Falsifier

**Computational, with a threshold, and it fires every gate run.** Any Brillouin-zone
evaluation of the model's own `bcc_dispersion` that returns one of the three coefficients
differing from its closed form by more than $5\times10^{-3}$ relative at $\Theta\le0.02$, or
a $C_u/C_w$ differing from $15/2$ by more than $5\times10^{-3}$, kills the claim as stated —
records GS-3, GS-4, GS-5, GS-7.

The declared control `branch_odd_control=True` replaces both branches by their average,
deleting $b(\hat n)$ and nothing else, and is the sharpest instrument on the card: GS-3/4/5
must go red (every coefficient falls to $4/7$ of its closed form, which *is* statement 2
measured) while **GS-7 must survive** (statement 3). A run in which the control reddens GS-7,
or fails to redden GS-3/4/5, falsifies a different half of the claim in each case.

The claim is hostage to two upstream results, as CL260 is: a change to $a$ (F107) rescales
$\Theta$ and every margin, and a change to the BCC walk changes $b$ and $a$ and therefore all
three coefficients.

**Observationally it is not falsifiable, and that is said rather than dressed up.** At the BBN
bottleneck $\Theta=3.1\times10^{-22}$ and the fermionic correction is $6.8\times10^{-43}$
relative — 40 orders below anything measurable. The fireable falsifier is the computation.

## Status & history

`live` as stated, with CL260's two scope boundaries carried over verbatim because they apply
unchanged: this is the **Gibbs measure on the derived dispersion**, not a demonstration that
the lattice dynamically reaches it (F300 §4.1 shows the free sector reaches a generalised
Gibbs ensemble instead), and it is an **equilibrium** statement.

One boundary of its own: "branch-balanced" is a property of the model's content, not of the
dispersion. F309 §4 checks it — 24 left-handed and 24 right-handed Weyl fields, imbalance
exactly zero — and the claim is stated for that content. It would not hold verbatim for a
chirally imbalanced spectrum.

## Sources

- `findings/F309-gstar-from-model-content.md`
- `findings/F300-lattice-native-thermodynamics.md` (the photon coefficients this is $31/4$ times)
- `findings/F26-speed-of-light-as-rotation-rate.md` (the walk)
- `findings/F67-even-law-photon-vs-bilinear-mutually-exclusive.md` (the branch-odd term the photon cancels)
- `findings/F107-canonical-a-adoption-L4-grb-gate.md` (the ruler that sets $\Theta$)
