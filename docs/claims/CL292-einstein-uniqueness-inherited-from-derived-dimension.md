---
id: CL292
title: Given an emergent local diffeomorphism-invariant metric-only theory with second-order field equations, the two-derivative left-hand side is forced to aG+bg by Lanczos-Bach in the model's derived d=4 and the source is the full ten-component stress-energy tensor by construction; a is adopted rather than derived, and the scalar-tensor and f(R) families are absent for want of a parameter rather than excluded
slug: einstein-uniqueness-inherited-from-derived-dimension
tier: supporting
kind: derivation
status: contingent
domain: [GR, QFT]
exactness: quantitative
findings: [F345, F178, F297, F59, F319, F288, F291, F326, F79, F107, F64, F106]
tests: [F345-field-equation-uniqueness]
modules: [casim.engine.interactions.gravity_field_equation_uniqueness]
constants: [a_over_ellP, ell_P_m, G_CODATA, c_SI, hbar_SI]
supersessions: []
reviews: [F345-review-2026-09-01, F345-review-2026-09-01-b]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-01'
last_verified: '2026-09-01'
provenance: authored
review_state: authored
confidence: medium
---

# CL292 — Einstein uniqueness inherited from the model's derived spacetime dimension

## Statement

**Granted one named hypothesis** — that the long-wavelength description of the lattice is a
*local, diffeomorphism-invariant metric* theory — the model's gravitational field equation is
**not a further choice**. Four things follow, three of them exactly:

1. the source is a **conserved symmetric 2-tensor**, forced by $\nabla^\mu G_{\mu\nu}\equiv0$
   and $\nabla^\mu g_{\mu\nu}\equiv0$ (sympy literal zeros on a four-function inhomogeneous
   metric with non-trivial curvature);
2. it is the **full** $T_{\mu\nu}$, all **ten** components, *by construction* — the metric
   variation of a local matter action is a symmetric rank-2 object, verified for the massless
   scalar and for Maxwell, with the determinant identity
   $\partial\sqrt{-g}/\partial g^{\mu\nu}=-\tfrac12\sqrt{-g}\,g_{\mu\nu}$ checked brute-force
   on all ten components; and its conservation *is* the matter field equation
   ($\nabla^\mu T_{\mu\nu}\equiv(\Box\phi)\partial_\nu\phi$, non-zero off-shell);
3. the left side is $aG_{\mu\nu}+bg_{\mu\nu}$ and nothing else, because the Lanczos–Lovelock
   tensor vanishes **identically in $d=4$** and does **not** in $d=5$ — verified in exact
   rationals on *generic algebraic curvature tensors* (Kulkarni–Nomizu / Fiedler, strictly
   more general than any metric ansatz), with the Gauss–Bonnet **scalar** non-zero in the same
   call. The model does not assume $d=4$: F291 fixes $d_\text{space}=3$ and F326 closes the
   "+1", so **Einstein uniqueness here is inherited from the already-derived spacetime
   dimension**;
4. the two-derivative truncation is an **order of magnitude, not a bound**:
   $\sim10^{-76}$ times an **uncomputed** $O(1)$ gravitational Wilson coefficient (worst proxy
   $6.68\times10^{-76}$, $\sqrt{\text{Kretschmann}}$ at the lightest compact remnant), with the
   F107 cell $a=1.0664\times10^{-34}$ m. **F319 does not supply that coefficient** — its exact
   rational dimension-6 coefficient is the photon-dispersion one and it explicitly declines the
   others. This leg is **not independent** of point 3: it is the size of the at-most-second-order
   assumption point 3 needs.

Two further alternative families are **absent from the model's parameter content** — which is a
*different* thing from being excluded, not a stronger one. **Scalar-tensor / Brans–Dicke**: no
finite $\omega$ solves $\gamma_\text{BD}=(1+\omega)/(2+\omega)=1$, and the model has no
independent gravitational scalar at all (by F79 S3 the source-free EM stress tensor is traceless
in 3+1D, so the conformal factor that would play $\varphi$ has no source and no tree action).
**$f(R)$**: unscreened $\Rightarrow\gamma=\tfrac12$, $2.17\times10^4\times$ Cassini, and the
chameleon escape needs a $k$-dependent $\mu$ that F288 S2 proves is a literal zero.

**Three limits on that pair, all required by the completed review.** (i) The premise supplying
$\gamma=1$, zero slip and $\mu\equiv1$ is $AB\equiv1$ (F64) and the F106 reduction, **both
reclassified by `S4-F178-full-stress-energy`** as the weak-field representation of the very
equation under question — so this is not an independent exclusion of a rival field equation, and
only $\dot G/G$ is independent of that pair. (ii) **Neither family is refuted**: a Brans–Dicke
theory with $\omega=10^{40}$, or an $f(R)$ with a Planckian scalaron, is observationally
identical and internally consistent. (iii) The metric-only premise is closed for Brans–Dicke and
metric $f(R)$ **only** — Vainshtein-screened Horndeski (F288's $\partial_k\mu=0$ is a *linear*
statement), vector-tensor and bimetric theories are not addressed.

## What it extends

Established GR takes $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ as a postulate (or derives it from an
Einstein–Hilbert action postulated by hand), and treats $d=4$ as an empirical input. This claim
asserts that in **this** model neither is a free choice at the field-equation level: the source
structure is forced by the variational principle plus the Bianchi identity, and the left side is
forced by Lovelock's theorem *at the dimension the model itself derives*. It also asserts a
stronger-than-experimental exclusion of the scalar-tensor and $f(R)$ families: where Cassini and
LLR give bounds with room left ($\omega>4.35\times10^4$), this model gives structural exact
zeros with **no dial** that could restore the alternative.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F345-field-equation-uniqueness-lovelock.md` L1 | $\nabla^\mu G_{\mu\nu}\equiv0$, $\nabla^\mu g_{\mu\nu}\equiv0$; curvature checked non-trivial | exact |
| F345 L2 | determinant identity, all 10 components; $T_{\mu\nu}$ for scalar and Maxwell; 10 independent components | exact |
| F345 L2b | $\nabla^\mu T_{\mu\nu}\equiv(\Box\phi)\partial_\nu\phi$; non-zero off-shell | exact |
| F345 L3 | $H_{\mu\nu}\equiv0$ in $d=4$ (2 seeds), 25 non-zero components in $d=5$; GB scalar non-zero | exact (rational) |
| F345 L4 | $\varepsilon\le1.45\times10^{-76}$ over six regimes | computed |
| F345 L5 / L6 | scalar-tensor and $f(R)$ closed on the model's own structure | exact |
| `findings/F291-why-three-plus-one-dimensions.md`, `findings/F326-the-plus-one-closes-no-second-generator.md` | the derived $d=3+1$ that L3 inherits from | 9/9, 2/2 |
| `findings/F288-structure-formation-zero-free-functions.md` S1/S2/S3 | zero slip, $\mu\equiv1$ with $\partial_k\mu\equiv0$, $\dot G/G\equiv0$ — the three structural sources | exact |
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` | physical BZ cutoff, dimension-6 leading irrelevant operator | 21/21 |
| `findings/F59-induced-eh-prefactor-and-f10-selection.md`, F79/F107 | the induced-EH coefficient and structural $G$ that fix $a$ | partial / exact |

Test record `F345-field-equation-uniqueness` (`tests/registry/interactions.yaml`, `assertion`,
tier `gate`), 8/8 legs PASS; results `test-results/F345_field_equation_uniqueness.json`.
Three declared controls verified RED with no spill: `lovelock_dim=5` and `gb_ricci_coeff=-3`
redden L3, `model_gamma=0.999999` reddens L5.

## Falsifier

Three, each of which fires independently:

1. **The dimension.** If $d_\text{space}=3$ ceases to be derived model content — F291's two
   selectors or F326's single-generator closure withdrawn — then point (3) loses its premise and
   Einstein–Gauss–Bonnet becomes admissible again. This claim is *downstream* of F291/F326 and
   fails with them.
2. **A measured PPN $\gamma\neq1$ or $\dot G/G\neq0$.** The model's values are exact structural
   zeros with no parameter to move, so any detection at any precision — not merely tension —
   falsifies the L5/L6 closures. Current anchors: Cassini $|\gamma-1|<2.3\times10^{-5}$, LLR
   $|\dot G/G|<1.5\times10^{-13}\,\text{yr}^{-1}$.
3. **A detected linear-order gravitational slip or a scale-dependent growth coupling
   $\partial\mu/\partial k\neq0$.** F288 already records these as exact zeros with no dial;
   detecting either would mean the model does host a scalar degree of freedom, reopening the
   family this card closes.

The **contingency itself** — that an emergent local diff-invariant metric exists — is not
falsifiable by observation and is not claimed to be derived; see below.

## Status & history

`status: contingent`, and the named hypothesis is stated once, in one sentence: *that the
long-wavelength description of the lattice is a local, diffeomorphism-invariant metric theory at
all.* This card asserts everything downstream of that premise and asserts **nothing** about the
premise. Rubric row **E1** therefore stays `POSIT` — this is a narrowing of what is posited, not
a derivation of the field equation from nothing.

Two things this card deliberately does **not** do:

- It does **not** re-close the energy-only law. That alternative was closed by the 2026-06-29
  decision (F178: Lorentz covariance, no neutron-star maximum mass) and independently by F297's
  BBN ($Y_p=0.1856$, $-17.6\sigma$). F345's L1 gives a third, structurally different reason —
  the Bianchi identity refuses any non-conserved-tensor source — but it is stated as a *family*
  constraint and the specific alternative is carried, not re-attacked.
- It does **not** narrow $\Lambda$. Lovelock *permits* the $bg_{\mu\nu}$ term; it does not fix
  it. **CL021** ("the cosmological constant is not derived") stands unchanged, and nothing here
  should be read as bearing on it.

What would finish E1, and is not claimed here: a derivation that the model's blockspin /
coarse-graining flow (F130) *drives* the long-wavelength effective action to a local
diff-invariant metric functional, rather than that form being assumed.

## Sources

- `findings/F345-field-equation-uniqueness-lovelock.md`
- `docs/status/open-derivations.md` Part C row **E1g**; rubric row **E1** in `docs/status/completeness-2026-08-20.md`
- `docs/theory/key-decisions.md`, 2026-06-29 entry (the decision this narrows)
- `docs/claims/CL021-cosmological-constant-not-derived.md` (explicitly untouched)
- D. Lovelock, Arch. Rational Mech. Anal. **33**, 54 (1969); J. Math. Phys. **12**, 498 (1971)
- T. Padmanabhan & D. Kothawala, arXiv:1302.2151
- M. Visser, *Sakharov's induced gravity: a modern perspective*, hep-th/0204062
- B. Bertotti, L. Iess & P. Tortora, Nature **425**, 374 (2003)
