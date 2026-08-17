---
id: CL275
title: A uniform reweighting of the zero-point sum cannot solve the cosmological-constant problem, because the Lambda^4 and Lambda^2 Sakharov sectors are two moments of one measure
slug: uniform-zero-point-reweighting-excluded
tier: headline
kind: no_go
status: live
domain: [GR, QFT, cosmology]
exactness: quantitative
findings: [F319, F164, F59, F79, F107]
tests: [F319-uv-completion]
modules: [casim.engine.interactions.qed_uv_completion]
constants: [a_over_ellP, ell_P_m, c_lat]
supersessions: []
reviews: []
rolls_up_to: CL273
falsifier: stated
first_issued: 2026-08-16
last_verified: 2026-08-16
provenance: authored
review_state: authored
confidence: high
---

# CL275 — The uniform zero-point channel is excluded

## Statement

F59 assembles $1/(16\pi G)$ from $\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{1}{2\omega}$ and F164
assembles $\rho_\text{vac}$ from $\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{\omega}{2}$ — the same
modes, the same measure and the same factor of $\tfrac12$. They are two moments of one
zero-point sum, the $a_0$ and $a_1$ coefficients of one heat-kernel expansion, with
$I_\text{cc}=4.0810486$ and $I_g=1.9807020$. Any mechanism that reweights that sum uniformly by
$\lambda$ therefore moves **both**, and because the two sectors carry different powers of the
cell ($1/16\pi G\sim\lambda/a^2$, $\rho_\text{vac}\sim\lambda/a^4$), requiring the model to
reproduce the measured $G$ **and** the measured $\rho_\Lambda$ is a $2\times2$ system with the
unique solution

$$a^\star=a_0\sqrt{\rho_\text{vac}/\rho_\Lambda}=2.559\times10^{26}\ \text{m}\ (8.29\ \text{Gpc}),
\qquad \lambda^\star=5.76\times10^{120}.$$

A lattice cell $0.58\times$ the comoving radius of the observable universe, and a zero-point
weight 121 orders *above* the canonical $\tfrac12$ rather than below it. **F164's own leading
candidate — channel (i), "the CA ontic vacuum has zero zero-point energy, so the bare CC is
0" — is therefore excluded**, because deleting the zero-point sum deletes F79's successful $G$
with it. Any surviving mechanism must be order-selective in the heat-kernel expansion:
suppress $a_0$ by $\ge120.76$ decades while perturbing $a_1$ by $\le2.2\times10^{-5}$ (CODATA's
relative uncertainty on $G$), a required relative selectivity between two *adjacent* heat-kernel
coefficients of $\ge1.27\times10^{116}$. F164's channel (ii) (sequestering through the
$AB\equiv1$ dielectric) is order-selective by construction and is the only one of the three with
the right shape.

## What it extends

The cosmological-constant problem is standardly stated as a fine-tuning: a vacuum energy
$\sim10^{120}$ too large, with the regulator-dependence of the $\Lambda^4$ term leaving room for
the answer to be a subtraction. F164 already sharpened that here — the BZ edge is physical, so
$\rho_\text{vac}$ is a definite number with nothing to renormalise away. This card adds the
constraint that Sakharov induced gravity imposes on the *solution space*: the CC and Newton
sectors are not independently tunable, so the class of "the vacuum simply does not gravitate"
resolutions is closed for any model that also derives $G$ from the same vacuum. That coupling
is generic to induced-gravity frameworks and is stated here in the model's own numbers.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §6 (U8) | the shared measure, the $2\times2$ solve, $a^\star$ and $\lambda^\star$ | exact in form, computed in value |
| `findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md` Part A/B/C | $I_\text{cc}=4.081$, the $10^{120.76}$ overshoot, and channel (i) as stated | computed |
| `findings/F59-induced-eh-prefactor-and-f10-selection.md` Part A | $\int d^3k/2\omega$ is the $\Lambda^2$ Newton sector, $\int\omega/2$ the $\Lambda^4$ CC sector | derived |
| `findings/F79-structural-newton-constant.md` | $G=a^2c^3/(8\pi\sqrt3\hbar)$ structural — what channel (i) would destroy | exact |
| record `F319-uv-completion`, legs `U8-reproduces-F164`, `U8-uniform-channel-excluded`, `U8-selectivity-required` | 21/21 PASS; control `zero_point_weight` reddens exactly these three | computed |

`sakharov_moments` computes both moments in one function over one grid, and reproduces F164's
$I_\text{cc}=4.081$ independently.

## Falsifier

1. **A uniform-$\lambda$ mechanism that fixes the CC without moving $G$.** It cannot exist as
   stated, because the two sectors carry different powers of $a$; so a claimed counterexample is
   really a claim that F59's $\Lambda^2$ assignment or F164's $\Lambda^4$ assignment is wrong,
   and that is where it should be attacked.
2. Showing $1/G$ is **not** sourced by the zero-point sum in this model — i.e. superseding
   F59/F79's induced route with a non-vacuum origin for $G$. That would free channel (i)
   and withdraw this card.
3. An order-selective mechanism delivering $\ge1.27\times10^{116}$. That would *close* the
   problem rather than falsify this no-go, and this card would then be narrowed to "the uniform
   subclass is excluded", which is what it already says.

## Status & history

Issued 2026-08-16 with F319, against F164's §C candidate list. This card **reorders** that list:
channel (i) was labelled there as "the most model-consistent route" and "the leading candidate
(elegant-design preferred)", stated openly as "a position, not a calculation". Doing the
calculation excludes it. Channel (iii) was already labelled a consistency statement rather than
a cancellation. Channel (ii) survives on shape and is unevidenced.

F164 itself is **not** superseded — its computation of $\rho_\text{vac}$ and its statement of the
problem stand unchanged, and are reproduced here independently. What moves is the disposition of
one of its three candidate resolutions, which is exactly the finding/claim split D12 exists for.

## Sources

- `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §6
- `findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md` §C
- `src/casim/engine/interactions/qed_uv_completion.py` (`sakharov_moments`, `two_sector_solve`)
