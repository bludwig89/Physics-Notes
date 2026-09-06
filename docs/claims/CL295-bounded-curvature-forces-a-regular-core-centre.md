---
id: CL295
title: 'Bounded curvature alone forces a regular centre in the lattice core: the Kretschmann scalar is a sum of squares, so K <= 1/a^4 makes the centre a C^{1,1} manifold interior point rather than a boundary'
slug: bounded-curvature-forces-a-regular-core-centre
tier: supporting
kind: derivation
status: contingent
domain: [GR]
exactness: exact
findings: [F354, F183]
tests: [F354-core-geodesic-completeness]
modules: [casim.engine.interactions.gravity_core_completeness]
constants: []
supersessions: []
reviews: [docs/reviews/F354-review-2026-09-03.md]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-03'
last_verified: '2026-09-03'
provenance: authored
review_state: authored
confidence: medium
---

# CL295 — Bounded curvature forces a regular centre; the point-group route does not

## Statement

For the general **two-function** static spherically symmetric metric
$ds^2=-A\,dt^2+dr^2/B+r^2d\Omega^2$, the Kretschmann scalar is an exact **sum of squares** of
orthonormal-frame Riemann components,

$$K=4R_{\hat t\hat r\hat t\hat r}^2+8R_{\hat t\hat\theta\hat t\hat\theta}^2+8R_{\hat r\hat\theta\hat r\hat\theta}^2+4R_{\hat\theta\hat\phi\hat\theta\hat\phi}^2,\qquad R_{\hat\theta\hat\phi\hat\theta\hat\phi}=\frac{1-B}{r^2},$$

so a single global bound $K\le a^{-4}$ constrains **each term independently** and forces $B(0)=1$
(no mass or solid-angle defect), $B'(0)=0$ and $A'(0)=0$. The metric is $\eta_{\mu\nu}+O(r^2)$ in
Cartesian coordinates: $C^{1,1}$, Lorentzian, and the centre is an **interior point of the
manifold**, not a boundary at finite affine distance. Geodesics exist and are unique there
(Chruściel–Grant), so the $E>1$ and null rays that reach $r=0$ pass through and continue. Beneath
the metric the automaton is tick-complete (Grant–Kunzinger–Sämann property (TC)), which covers the
sub-cell regime where no metric applies.

This closes the gap F183 §L1 left open, since **bounded curvature does not by itself imply geodesic
completeness** (Zhou & Modesto, PRD **107** 044016). It does so **without** parity, point-group
input, saturation, or the one-function condition $AB=1$ — and it holds in the two-function class
F178/F181 say the interior actually requires.

**The claim explicitly does not include** the attractive proposition that the BCC site group forces
the parity condition. That is **false in both directions** and is recorded as a no-go: Hayward's own
density is a function of $r$ alone (hence $O(3)$- hence $O_h$-invariant) yet carries an odd $r^3$
term, because $r^{2k+1}$ is a *non-polynomial* $O_h$ invariant; and every odd $T_d$ invariant
carries $xyz$, whose spherical average vanishes, so a non-centrosymmetric lattice yields the same
regular centre in the monopole channel. The real hypothesis is **smoothness of the coarse-grained
core density at the centre**.

## What it extends

**The Penrose–Hawking singularity theorems, at the point where they bite.** They guarantee geodesic
incompleteness for collapse under an energy condition; this model evades the conclusion by bounding
curvature at the lattice cutoff, and the sum-of-squares structure is what converts that bound into a
statement about the manifold rather than merely about an invariant.

Against the comparison programmes: Ashtekar–Olmedo–Singh (LQG) claim bounded curvature and a maximal
extension but, as far as we can find, **no explicit geodesic-completeness statement**; the
Bonanno–Reuter RG-improved metric of asymptotic safety carries an odd $r^3$ from the linear $\alpha r$
in its denominator and so sits in Zhou–Modesto's *incomplete* class (our screen's output; no priority
claimed).

**No priority is claimed for the regularity criterion itself.** Antonelli & Sebastianutti
(arXiv:2509.15477, PRD 10.1103/hf4r-19xh) publish it in stronger *iff* form in the two-function
class, with differentiability classes. This card's content is the substrate reading, the no-go, and
the scales.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F354-lattice-core-geodesic-completeness.md` | the argument, the no-go, the contingencies | — |
| B1 | `K - (sum of squares) = 0` verified against a full Riemann contraction | exact |
| B1 control | a solid-angle deficit is **detected**: $Kr^4\to4\delta^2$, measured 0.0400 at $\delta=0.1$ | exact |
| B2 | the no-go, both legs: Hayward's odd $r^3$ coefficient $-3M/(2\pi L^6)$; $T_d$ odd invariants integrate to zero | exact |
| B4 | geodesic regimes; completeness carried by $E>1$ and null | exact, local $r\to0$ |
| B5 | screen reproduces ZM's published Hayward $r^5$ coefficient $2M/L^6$ | exact, calibrated |
| B6 | $L=24^{1/4}a$ profile-independent; the ratio to F183's proxy is not | exact, contingent |
| `test-results/F354_core_geodesic_completeness.json` | 7/7 PASS | — |
| `docs/reviews/F354-review-2026-09-03.md` | the attack pass that refuted the first draft and supplied this one | — |

## Falsifier

1. **The computable one.** Measure the $r^3$ coefficient of the coarse-grained core density from a CA
   run. Nonzero at leading order puts the core in Hayward's class and makes it geodesically
   incomplete. The no-go removed the symmetry argument that would have forbidden this, so it is now
   an open empirical question about the substrate. **Cheap, decisive, and unrun.**
2. **A demonstration that no coarse-grained metric is $C^{1,1}$ at the centre** in a sense making B1
   applicable — the regular centre is only $\sim2.2$ cells across.
3. **A proof that the BCC update rule is not total or not norm-preserving** in some reachable
   configuration. Breaks the substrate tier.
4. **A mass-inflation result showing the inner horizon at $r\sim L$ destroys the static core.** Would
   not falsify the theorem but would make it irrelevant.

## Status & history

`contingent`, issued 2026-09-03, moving rubric row **E10** off PARTIAL.

**Issued at `tier: headline`, `status: live`, `exactness: exact` and reclassified the same day**, on
the session's own attack pass. The withdrawn broad form was: *"the lattice core is geodesically
complete, and the parity that makes it so is forced by inversion symmetry of the BCC site group
rather than imposed by hand."* The mechanism half of that is refuted (see the no-go above); the
completeness half survives on a different and more robust argument, which is what this card now
states.

`contingent` names three inputs, each quantified in F354 §7:

- **saturation as an equality** — F183 licenses *bounded*, not *saturated*; without it the scales are
  one-sided bounds ($L\ge24^{1/4}a$);
- **the curvature-ceiling convention** — F183's $K\le a^{-4}$ against F284's $H\le1/a$ (i.e.
  $K\le24/a^4$); under the latter $L=a$ exactly and the e-folding is $\sqrt3$ ticks, one cell
  crossing. Only one can be fundamental; **open decision**, flagged in F354 §8;
- **the core profile** — $L$ is profile-independent, but the ratio to F183's proxy moves from
  $2^{1/6}=1.1225$ (Bardeen) to $0.7218$ (Gaussian), so that comparison is not a model statement.

Scope boundaries: the argument is **local** ($r\to0$), not a completeness proof for the maximal
extension; static and non-rotating; inner-horizon stability untouched. `confidence: medium` records
these together with the 2.2-cell caveat.

## Sources

- `findings/F354-lattice-core-geodesic-completeness.md`
- `docs/reviews/F354-review-2026-09-03.md`
- `findings/F183-blackhole-under-full-tensor.md` §L1 (the saturation estimate this builds on)
- `findings/F284-rigid-lattice-expansion-and-primordial-state.md` §5 (and the ceiling conflict, F354 §8)
- Zhou & Modesto, PRD **107** 044016 (2023), arXiv:2208.02557
- Antonelli & Sebastianutti, arXiv:2509.15477, PRD 10.1103/hf4r-19xh — prior art, stronger *iff* form
- Grant, Kunzinger & Sämann, arXiv:1804.10423 — property (TC)
- Whitney, Duke Math. J. **10** (1943) 159
- Bonanno & Reuter, PRD **62** 043008 (2000); Ashtekar, Olmedo & Singh, PRL **121** 241301 (2018)
