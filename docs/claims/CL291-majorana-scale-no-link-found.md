---
id: CL291
title: 'Neither of ledger row D4''s two named candidates -- the F183/F107 lattice cutoff or the E_g/Z3 condensate -- supplies a scale link for the absolute Majorana mass M_R; M_R joins the model''s existing E5-E7 scale-anchoring cluster'
slug: majorana-scale-no-link-found
tier: supporting
kind: no_go
status: live
domain: [SM]
exactness: exact
findings: [F343, F47, F79, F107, F201, F236, F253, F282, F341]
tests: [F343-majorana-scale-no-link-found]
modules: [casim.engine.particles.derive_M_R_scale_link, casim.engine.particles.majorana]
constants: [a_over_ellP, delta_star_f, lambda_6]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-31'
last_verified: '2026-08-31'
provenance: authored
review_state: authored
confidence: medium
---

# CL291 -- Neither named candidate fixes M_R; the residual joins the E5-E7 cluster

## Statement

Ledger row D4 (`docs/status/open-derivations.md`) states plainly that "nothing in the model fixes
$M_R$" -- the see-saw plus the $E_g/\mathbb Z_3$ texture (F236/F254) derive the three light-neutrino
masses' *shape* (ratios, hierarchy) at machine precision, but the overall Majorana scale $M_{R0}$ is
an unfixed anchor. This claim is the checked, not merely asserted, version of that residual: it runs
D4's own named first check -- does the F183/F107 canonical lattice cutoff, or the $E_g$ condensate
already used for the mass shape (F201), offer *any* scale link -- and finds, on three independent
mechanical legs, that neither does.

**Leg 1 (cutoff).** $\Lambda/M_{R0}\sim10^{19}$ at F201's own benchmark, a genuine ~19-decade
hierarchy, not a rounding-level gap. An exhaustive scan of small integer powers of every
already-registered lattice-fixed dimensionless ratio finds no near-exact match to that suppression
-- the closest, $(1/(72\pi))^8$, misses by $0.13$ dex (factor $1.35$) and is flagged as an unclaimed
numerical coincidence (the project's own sense, cf. F332's `reciprocal_cube_coincidence`), not
adopted as a structural link: the exponent is unmotivated and a comparable near-hit among 72 scanned
combinations is not, on its own, statistically surprising.

**Leg 2 (condensate).** The $E_g/\mathbb Z_3$ texture
(`casim.engine.particles.majorana.z3_sqrt_texture`, F201) provably factors the overall prefactor
$M_{R0}$ out of its defining relation identically -- sympy-exact, $\partial(\text{bracket})/\partial
M_{R0}=0$ for every generation and every phase -- and is numerically confirmed blind to it (rescaling
$M_{R0}$ over six decades leaves every ratio, every angle, and F201's cancellation-node location
unchanged to better than $10^{-10}$). This generalises F253's POSIT-N no-go (the same representation
machinery supplies a dimensionless weight/angle but not an absolute scale, without an unmotivated
normalisation) one further dimensional category, from a radian to a mass.

**Leg 3 (dynamics).** $\nu_R$'s total gauge-singlet status ($Y=0$ structurally forced, F47;
reaffirmed F341) forecloses the model's only mechanism for generating a hierarchically small scale
from the cutoff -- asymptotic-freedom running of a confining gauge coupling, implemented in this tree
only for $SU(3)_c$. Mechanically confirmed by source inspection:
`casim.engine.particles.majorana` imports nothing beyond numpy, i.e. zero coupling to any gauge,
running, or confinement module.

**M_R is therefore not an isolated gap.** It is a named 5th member of the pattern already implicit in
ledger rows E5-E7: the model derives dimensionless mass *shapes* exactly via lattice representation
theory, but has never derived an absolute mass *scale* ($v$, the quark masses, $m_{E_g}$) from the
Planck-derived cutoff. D4 does not close; it is reclassified from an unexamined gap into a checked
instance of that existing cluster.

## What it extends

Nothing in the Standard Model or its usual seesaw extensions fixes $M_R$ either -- the absolute
right-handed neutrino scale is a free input there too, constrained only indirectly (leptogenesis,
$0\nu\beta\beta$ non-observation). This claim does not extend or contradict that; it is a purely
internal, model-structural statement that *this* model's own scale-fixing machinery (the lattice
cutoff and the $E_g$ condensate, both load-bearing elsewhere) does not reach $M_R$ either, for three
independently checked and named reasons rather than by default.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F343-majorana-scale-no-link-found.md` §1-3 | The three-legged null result (cutoff scan, texture factorisation, dynamics foreclosure) | exact / machine |
| `casim.engine.particles.derive_M_R_scale_link.c1_cutoff_hierarchy` / `c2_ratio_scan` | $\Lambda/M_{R0}\sim10^{19}$; closest scanned ratio-power hit $0.13$ dex away, flagged not claimed | quantitative |
| `casim.engine.particles.derive_M_R_scale_link.c3_G_has_no_hierarchy` | F79's $G$-from-cutoff prefactor is $O(10^{-2})$, not a precedent for a $10^{-19}$ suppression | exact |
| `casim.engine.particles.derive_M_R_scale_link.c4_texture_factors_out_M_R0_symbolically` | sympy-exact: $M_{R0}$ factors out of the $E_g/\mathbb Z_3$ bracket identically | exact |
| `casim.engine.particles.derive_M_R_scale_link.c5_texture_blind_to_M_R0_numerically` | Numerically confirms C4: max residual $<10^{-10}$ over six decades of $M_{R0}$ | machine |
| `casim.engine.particles.derive_M_R_scale_link.c6_no_dynamical_scale_route_for_nu_R` | `majorana.py` imports nothing beyond numpy; no gauge/running coupling to $\nu_R$ | exact (mechanical) |
| `tests/registry/particles.yaml` record `F343-majorana-scale-no-link-found` | 8/8 pytest checks PASS; registry entry PASS via `casim.tests.runner` | exact |

## Falsifier

This is a null result about the model *as it exists today*, not a claim that $M_R$ is provably
unfixable in any future extension. Three things, named in F343, would void a leg without needing new
observation:

1. **A new gauge coupling for $\nu_R$** -- if a future finding gives $\nu_R$ a nonzero charge under
   some confining or running gauge symmetry, leg 3 is voided and the model's existing dimensional-
   transmutation machinery becomes available for $M_R$.
2. **A general solution to the E5-E7 scale-anchoring cluster** -- since M_R is now grouped with $v$,
   the quark masses, and $m_{E_g}$ as the same open problem, a mechanism that fixes any one of them
   from the cutoff would need to be checked against $M_R$ as well, and might carry it along.
3. **An $M_D/M_R$ prefactor-sharing argument** -- not attempted in F343: whether the Dirac mass
   $M_D$'s own scale (itself unfixed, tied to $v$) shares a hidden normalisation with $M_{R0}$ that
   the see-saw ratio could expose. Named as the most promising untried route, not evidence against
   this claim.

The Leg-1 numerical coincidence, $(1/(72\pi))^8$, is explicitly *not* a falsifier candidate: it is
reported and flagged, not adopted, and finding a comparably close hit under a different scan
parameterisation would not on its own promote it to a structural link.

## Status & history

`status: live` -- this is F343's own stated verdict, not contingent on another finding remaining
correct (contrast CL290, which is `contingent` on F165/F279). Ledger row D4 stays `OPEN`, now with a
checked rather than asserted status. First issued 2026-08-31 from F343; not narrowed or superseded.

## Sources

- `findings/F343-majorana-scale-no-link-found.md`
- `findings/F47-majorana-seesaw-higgs-free.md`
- `findings/F79-structural-newton-constant.md`
- `findings/F107-canonical-a-adoption-L4-grb-gate.md`
- `findings/F201-kev-sterile-from-eg-texture.md`
- `findings/F236-three-generation-seesaw-pmns.md`
- `findings/F253-weight-as-phase-scale-nogo.md`
- `findings/F341-majorana-forced-by-hypercharge-closure.md`
- `docs/status/open-derivations.md` row D4
- `tests/registry/particles.yaml` record `F343-majorana-scale-no-link-found`
