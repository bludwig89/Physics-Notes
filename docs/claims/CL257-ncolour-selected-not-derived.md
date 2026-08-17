---
id: CL257
title: N_c is not derived here — two routes are closed exactly, one is circular, the C7 identity supplies a structural N_c <= 3 bound that consumes no measured number, and the 28-decade Lambda-scale selector that picks 3 rests on a bare-coupling normalisation the model's own confinement engine contradicts
slug: ncolour-selected-not-derived
tier: supporting
kind: derivation
status: narrowed
domain: [QCD, SM]
exactness: bracketed
findings: [F293, F294, F298, F299, F303]
tests: [F293-why-three-colours, F298-casimir-ladder, F299-casimir-scaling, F303-coupling-normalisation]
modules: [casim.engine.gauge.derive_ncolour, casim.engine.gauge.casimir_ladder, casim.engine.gauge.casimir_scaling]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-05
last_verified: 2026-08-06
provenance: authored
review_state: authored
confidence: low
---

# CL257 — N_c = 3 is selected, not derived, and the selector's premise is now contradicted

## Statement

**$N_c=3$ is not derived in this model, and this card does not claim it is.** What is claimed is
four-fold, and **the fourth leg replaced the third as the load-bearing one on 2026-08-06** — see
`## Status & history`.

**(a) Two routes are closed.** Anomaly cancellation *cannot* select $N_c$ here: the full
six-constraint hypercharge system (two anomaly rows, three mass-step rows, the F47 Majorana row)
has rank 6 and nullspace dimension 1 for **every** $N_c$, with ratios
$y_Q:y_u:y_d:y_L:y_e:y_\nu = 1:(N_c{+}1):(1{-}N_c):-N_c:-2N_c:0$, and the gravitational and cubic
$U(1)^3$ anomalies are identically zero as polynomials in $N_c$. The usual Standard-Model argument
($N_cY_Q+Y_L=0$ with $Y_Q=\tfrac16$ forcing 3) is unavailable *here* because $Y_Q$ is not
independently given — it comes out of the same nullspace, proportional to $N_c$. Separately, colour
is **not** the three spatial axes: the $O_h$ 3-cycle about $[111]$ is an even permutation
($\det=+1$), hence an $SU(3)$ element, and $\max_a\lVert[C_3,\lambda^a]\rVert = 2.449 \ne 0$, so an
axis-identified colour would be rotated by a lattice rotation; the internal-index control commutes
at literal `0.0`.

**(b) One route is circular.** The $\mathbb Z_3$ that F97/F99/F110 make load-bearing for
confinement is introduced *as the centre of $SU(3)$*, so it cannot select $SU(3)$.

**(c) One route selects 3 empirically, and its premise is contradicted by the model's own
confinement engine.** The claim *as first issued* was that the model's bare colour coupling
$\alpha_s(\mu_0)=g_s^2/4\pi=1/(16\pi)$ carries **no $N_c$**, so $N_c$ enters only through $\beta_0$,
and dimensional transmutation then makes the confinement scale depend on $N_c$ exponentially:
$\Lambda = 1.3\times10^{-23}$, $4.7\times10^{-2}$, $2.6\times10^{5}$ GeV at $N_c=2,3,4$ — a span of
**28.3 decades**, of which only $N_c=3$ lands at the observed hadronic scale. That arithmetic
stands. What no longer stands is its premise. The $N_c$-free reading (F294's **H1**) requires the
C7 matching to be normalised on the **centre**; F298 showed that where the C7 identity exists
against a genuine $SU(N)$ ladder it carries $1/C_F$ (**H2**), and F299 measured which law the
model's own confinement sector obeys: at the model's own coupling $\beta=2N/g_s^2=24$ the exactly
solvable 2D SU(3) engine gives $\sigma_6/\sigma_3=2.4911511$ against $5/2$ (Casimir) and $1$
(centre), Casimir scaling on all seven rungs to $\le1.4\%$ and exactly in the continuum limit.
**Under H2 the selector returns $N_c=1.28$, and it cannot be rescued by moving the lattice scale:
H2 needs $\mu_0\approx6.06\times10^{24}$ GeV, 5.7 decades above the Planck mass.** So this leg is
retained as a **recorded near-coincidence** — $1/(16\pi)$ agrees with the bare coupling the data
demands to $0.08\%$ — and **not** as a selector.

**(d) One leg is structural, and it is now the load-bearing one.** The C7 identity — a single
level-independent stiffness $\chi$ matching the gauge ladder — **exists only for $N_c\le3$**.
$C_2(\text{antisym }k)=\tfrac{k(N-k)(N+1)}{2N}$ is proportional to the model's own $\mathbb Z_N$
level $s(k)^2$ at $N=2$ (trivially, one level) and $N=3$ (non-trivially: $k=1$ and $k=2$ are
conjugate and carry the same Casimir $4/3$, matching $s(1)^2=s(2)^2=1$), and **fails for every
$N\ge4$**, where $\chi$ comes out level-dependent and no identity exists at all. This **consumes no
measured number** and is **independent of the H1/H2 dispute** — the identity exists for $N\le3$
under both readings and for $N\ge4$ under neither. It is a **bound, not a derivation**: it admits
$N_c=2$, which is excluded only by the empirical $\Lambda$-scale argument of (c).

## What it extends

The Standard Model takes $N_c=3$ as an input and fits the coupling. This model takes $N_c=3$ as an
input too, but its bare coupling is derived, so the integer becomes something the structure
constrains: the C7 identity that the whole $g_s=\tfrac12$ derivation rests on is **not available**
above $N_c=3$. No such statement is available in the Standard Model, where nothing about the gauge
group's rank is constrained by the coupling's derivation, because there is no derivation.

It does **not** extend the derivation of $N_c$. Nothing here produces 3 from lattice structure with
no empirical input: the structural leg gives $N_c\le3$ and the exclusion of $N_c=2$ remains
empirical.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F293-why-three-colours.md` §1 | nullspace dim 1 for every $N_c$; grav and cubic identically 0 in $N_c$ | exact (ℚ, symbolic $N_c$) |
| `findings/F293-why-three-colours.md` §2 | $[C_3,\lambda^a]=2.449$; internal-index control `0.0` | exact |
| `findings/F293-why-three-colours.md` §4.2 | $\Lambda$ spans 28.3 decades over $N_c=2..4$; only 3 in window | quantitative |
| `findings/F293-why-three-colours.md` §4.3 | $N_c=2.998$ (2.995 thresholded) | quantitative |
| `findings/F293-why-three-colours.md` §4.5 | F280 scheme band ⇒ $N_c\in[2.90,3.11]$ | bracketed |
| `findings/F294-c7-chi-map-ncolour-audit.md` §3 | the C7 $\chi$-map is $N$-free across 7 groups, deviation literal `0.0` | exact |
| `findings/F294-c7-chi-map-ncolour-audit.md` §4 | H1 $\to$ 2.998, H2 $\to$ 1.28, H3 $\to$ no root | quantitative |
| `findings/F298-casimir-ladder-c7-rerun.md` §2 | the C7 identity exists **only for $N_c\le3$**; $\chi_k$ level-dependent for $N\ge4$ | exact (ℚ) |
| `findings/F298-casimir-ladder-c7-rerun.md` §3 | where it exists $\chi=1/(4g^2C_F)$ — structurally H2 | exact (ℚ) |
| `findings/F299-casimir-scaling-discriminator-reinstated.md` §2 | the sextet shares the antitriplet's triality with $5/2$ its Casimir, so the discriminator is **not** degenerate at $N=3$ | exact (ℚ) |
| `findings/F299-casimir-scaling-discriminator-reinstated.md` §3 | the model's own 2D SU(3) engine measures Casimir scaling at $\beta=24$: $\sigma_6/\sigma_3=2.4911511$ vs $2.5$ and $1$; residual $\to1.7\times10^{-4}$ by $\beta=192$ | quantitative |
| `findings/F299-casimir-scaling-discriminator-reinstated.md` §5 | H2 needs $\mu_0=6.06\times10^{24}$ GeV, 5.7 decades above Planck; H1 needs $1.78\times10^{18}$, $-1.6\%$ from the model's own | quantitative |
| Record `F293-why-three-colours` (tier gate) | 17/17 (B6/B6b added by F294), three controls verified red | bracketed |
| Record `F298-casimir-ladder` (tier gate) | 8/8, two controls verified red | exact |
| Record `F299-casimir-scaling` (tier gate) | 10/10, two controls verified red | quantitative |

## Falsifier

1. **The translation hypothesis — DECIDED against H1 on model-internal evidence, 2026-08-06 (F299).**
   This entry has now been rewritten twice, and the direction of travel is the point. *Original
   (F293):* "a 25% coupling factor takes it to 2.54" — a graceful degradation. *First rewrite
   (F294):* not a shift but a destruction — H2 gives $N_c=1.28$ and H3 has no root. *Second rewrite
   (F299):* it is no longer a hypothesis. F298 built the $SU(N)$ ladder F110 deferred and found the
   C7 identity carries $1/C_F$ where it exists; F299 reinstated the physical discriminator F298 had
   withdrawn — the withdrawal was scoped to the antisymmetric tower, where at $N=3$ irrep and
   triality are in bijection so no centre law *can* disagree with any Casimir law — and ran it on
   the model's own exactly solvable 2D SU(3) engine at the model's own $\beta=24$. **Casimir
   scaling, to $\le1.4\%$ on seven rungs, exact in the continuum limit, with centre dominance
   missing the sextet by 1.49 absolute.** So leg (c) is falsified as a *selector* unless someone
   supplies the argument the tree does not contain: why the model's coupling would be normalised on
   the centre while its running uses the $SU(N_c)$ $\beta$-function. **The remaining escape is
   named and narrow, and it is an argument about F144, not about F110.**
   **Narrowed further 2026-08-06 (F303): that escape was searched and is not
   there.** Three candidate arguments for centre normalisation are closed exactly
   — the Casimir shift is $26\times$ F144's measured A4 residual (not a scheme
   constant); the three-link plaquette that would reconcile both readings does not
   exist on the BCC graph (no closed 3-bond loop, by parity and by exhaustive
   enumeration — and it would have forced $N_c=3$ uniquely, which is why it is
   recorded as closed rather than left unsaid); and the Cartan reading gives a
   Landau pole above $M_Z$. What survives is a **fork**, not a hedge: either
   F144's $0.083\%$ is a coincidence, or the colour sector is not
   $SU(N_c)$-normalised and the running must be rebuilt. F303 names the single
   computation that separates them by six decades.
2. **The $d=2$ escape, and why it is not one.** F299's engine is two-dimensional, and $d=2$ has no
   transverse gluons, hence no string breaking, hence centre dominance cannot appear there even in
   principle. Anyone defending H1 will reach for this. It fails because **C7 is a single-plaquette
   bare-normalisation identity** — it fixes what one link in irrep $R$ costs, not what an infinitely
   long string costs — and screening is an infrared effect that cannot renormalise a UV link cost.
   A live version of this objection would have to show that the *bare* link normalisation differs
   between $d=2$ and $d=4$, which is a computation nobody has done. F94's 3+1D SU(3) engine could
   do it and F299 shows it is free to ask (higher-rep loops are polynomials in the fundamental loop
   matrix already measured), so this is a **falsifier with a costed test**, not a hedge.
3. **Leg (d) falls if the $N\le3$ scan is wrong.** `casim test --id F298-casimir-ladder --param
   n_max=3` must go red: a scan that never tests $N\ge4$ cannot claim to have excluded it.
   `--param tower=symmetric` must also go red — the symmetric tower is uniform at *no* $N$, which
   is what makes the $N\le3$ result a property of the k-string sector rather than of a conveniently
   chosen ladder.
4. `--param alpha_s_MZ=0.05` — leg (c)'s arithmetic must follow the data ($N_c\to2.47$). A selector
   that returned 3 for any input would not be measuring anything, and this is the check that it is.
5. `--param mu0_factor=100.0` — a two-decade scale error still leaves 3 the nearest integer
   ($N_c\to2.79$); it reds only the 1% check.
6. If $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ (F280, currently bracketed in $[1,7.980]$)
   were measured outside that band by more than ~2 orders of magnitude, leg (c)'s $N_c$ band would
   widen past the neighbouring integers.

## Status & history

Issued 2026-08-05 from F293, written against completeness row **B10** ("why 3 colours"), recorded
`ABSENT` and described by that report as *"a single load-bearing integer"*. The row moved
`ABSENT` → `PARTIAL` and **stays** `PARTIAL`.

**`status: narrowed` as of 2026-08-06 (was `contingent`).** The broad form, retained here as the
retraction record: *"the model's $N_c$-free bare coupling makes $N_c$ a 28-decade lever on the
confinement scale, and only $N_c=3$ lands at the observed hadronic scale."* The narrow form is the
Statement above: the 28-decade arithmetic is intact, but its premise — an $N_c$-free bare coupling
— is the reading the model's own confinement sector does **not** implement, so leg (c) is a
recorded coincidence and leg (d) is what carries the card.

**`confidence: low` as of 2026-08-06 (was `medium`, twice).** The history of this field is the
honest summary of the card. On 2026-08-05 it was `medium` because "the fragile direction is real
and quantified" (F293). Later the same day it was **held** at `medium` with the reason changed to
"the selector is contingent on an unvalidated modelling choice, and the alternative destroys it"
(F294) — held rather than lowered because F294 had also *verified* the $N$-independence of the
reading the model implements. That verification is now known to have covered only the $\mathbb Z_N$
and $U(1)$ groups, i.e. the centre truncation, not the $SU(3)$ the running uses. **F298 and F299
closed that gap and it closed against the card.** `low` reflects that the distinctive content — a
measurement reading $N_c$ back off the confinement scale — rests on a premise contradicted by the
model's own engine. What is *not* low-confidence: the exact no-gos of (a), the circularity of (b),
and the structural $N_c\le3$ bound of (d).

**The circularity is audited on the card, not just in the finding.** The PDG $\alpha_s(M_Z)$ is
extracted from data *inside QCD with $N_c=3$* — every determination uses an $\overline{\rm MS}$ beta
function carrying $N_c=3$ — so the $N_c=2.998$ inversion is **partly circular**. That is why leg (c)
leads with the $\Lambda$-scale argument, which uses only the observed hadronic mass scale, not an
$N_c$-dependent extraction. Anyone quoting "2.998" without the scale argument behind it is quoting
the contaminated half.

**What would upgrade this card.** F299 reordered the list again, and shortened it.
*First*, the open item is now **F144's, not F110's**: either an argument for why the model's bare
coupling is normalised on the centre while its running is $SU(N_c)$, or acceptance that
$1/(16\pi)$'s $0.08\%$ agreement is a coincidence. There is no third option left — the structural
reading (F298) and the model's own measured confinement law (F299) both say $C_F$ is there, and
rescaling $\mu_0$ is excluded by 5.7 decades.
*Second*, a **structural exclusion of $N_c=2$** would turn leg (d) from a bound into a derivation
and would make this card's headline non-empirical for the first time. The natural candidate, named
but untested in F298: $SU(2)$'s fundamental is pseudo-real, so $k=1$ and $k=2$ are not distinct
rungs.
*Third*, a $\mathbb Z_3$ derived from BCC/$O_h$ structure with no reference to the colour group
would make the centre route of (b) non-circular. The lattice does have 3-fold structure (four $C_3$
body-diagonal axes; the $2\pi/3$ holonomy of F253); whether any of it carries triality
independently is untested.

## Sources

- `findings/F293-why-three-colours.md`
- `findings/F294-c7-chi-map-ncolour-audit.md` — the C7 audit that first rewrote falsifier 1
- `findings/F298-casimir-ladder-c7-rerun.md` — the $SU(N)$ ladder; the $N_c\le3$ leg and the $1/C_F$
- `findings/F299-casimir-scaling-discriminator-reinstated.md` — the discriminator reinstated and run; the measurement that decided falsifier 1
- `findings/F303-no-centre-normalisation-argument.md` — the search for a centre-normalisation argument, and the three candidates it closes
- `findings/F279-hypercharge-constraint-attribution.md` — the anomaly no-go, re-verified on the full system
- `findings/F144-route-a-alpha-s-dimensional-transmutation.md` — $g_s=\tfrac12$ derived, and the running; now the location of the open item
- `findings/F110-realtime-link-hamiltonian-confinement.md` — the C7 $\chi$ map
- `findings/F280-d1-subtracted-against-wilson.md` — the scheme band propagated into the $N_c$ band
- `findings/F291-why-three-plus-one-dimensions.md` — $d=3$; states it does not touch B10
- `src/casim/engine/gauge/derive_ncolour.py`
- `src/casim/engine/gauge/casimir_ladder.py`
- `src/casim/engine/gauge/casimir_scaling.py`
- `src/casim/engine/gauge/derive_coupling_normalisation.py`
- `docs/status/completeness-2026-08-04.md` — row B10, ABSENT, the gap this narrows
