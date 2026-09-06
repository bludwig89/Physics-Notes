---
id: CL302
title: 'CL209''s "the geon relic abundance is a genuinely free input" is scoped to the inflaton/Press-Schechter production route: it is not a claim that every conceivable geon-production mechanism is foreclosed, and a structurally distinct, non-inflationary domain-wall-collapse channel remains open with its Kibble-mechanism precondition already exactly satisfied by the model''s own E_g clock potential'
slug: geon-domain-wall-reopening-scope-boundary
tier: supporting
kind: non_claim
status: open
domain: [cosmology]
exactness: bracketed
findings: [F366, F238, F228, F282, F285, F150, F175, F234]
tests: [F366-geon-domain-wall-reopening]
modules: [src/casim/engine/interactions/cosmology_geon_domain_wall_reopening.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL209
falsifier: stated
first_issued: '2026-09-04'
last_verified: '2026-09-04'
provenance: authored
review_state: authored
confidence: medium
---

# CL302 — CL209's abundance exclusion is scoped to the inflaton/Press-Schechter route; a distinct domain-wall channel remains open

## Statement

CL209 (from F238) proves the geon's relic-formation fraction $\beta(M_\text{form})$ cannot be
derived via the standard chain $\Omega_\text{DM}\leftarrow\beta\leftarrow\sigma(k_\text{PBH})
\leftarrow$ primordial $P(k)\leftarrow$ inflaton, and F282/F285 upgrade that from "not built" to
"cannot be built" (no slow-roll inflaton can exist on this lattice; no principled measure on the
$t=0$ state reproduces $n_s=0.9649$ either). **This card records what that chain does and does not
cover.** It does not, and — per F282 §6's own acoustic-peak-coherence scope, which excludes causal
sub-horizon mechanisms only as explanations of the *large-scale* (CMB) power spectrum — cannot,
exclude a structurally different, non-inflationary production channel: collapse of a $\mathbb{Z}_6$
domain-wall network sourced locally and causally by the model's own already-derived $E_g$ clock
potential $V(\delta)=\frac{A}{2}(1+\cos6\delta)$ (F150/F175/F234), rather than inherited from any
primordial curvature spectrum. This channel's Kibble-mechanism precondition — the potential's exact
discrete $\mathbb{Z}_6$ symmetry and exactly 6 degenerate global minima per period — is confirmed
exact-algebraically (F366) using the model's own existing constants, at zero cost in new physics.
No abundance is computed; four named pieces (causally-early settling dynamics, transition order,
wall tension in physical units, and a network-collapse/overclosure resolution) remain open.

## What it extends

Nothing established in QM/SM/GR/SR is derived or contradicted here. This card exists to prevent
CL209 — an `unreviewed-seed`, mechanically-extracted card whose title is scoped correctly but whose
`kind: no_go` invites over-reading as "no mechanism, of any kind, could ever fix this abundance" —
from being cited that way. It is a scope boundary on an existing model-native claim, recorded so
that CL209's silence on non-inflationary channels is not read as their exclusion (`README.md`'s
own reason for the `non_claim` kind).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F366-geon-domain-wall-reopening.md` | Full analysis: the reopening is real, the precondition is exact, four pieces remain open | mixed: exact (precondition) / open (abundance) |
| `tests/registry/interactions.yaml` → `F366-geon-domain-wall-reopening` | 4/4 checks PASS (tier: battery) | exact |
| `test-results/F366_geon_domain_wall_reopening.json` | Numeric/symbolic results: 6 exact vacua at $\delta=\pi/6+n\pi/3$, exact $\mathbb{Z}_6$ symmetry, zero prior discussion of the channel in the six framing findings | exact |
| `findings/F238-geon-relic-abundance.md`, `findings/F282-no-slow-roll-inflaton-sub-planckian-cutoff.md`, `findings/F285-initial-condition-measure-cannot-tilt.md` | The chain this card scopes | quantitative / exact |
| `findings/F150-eg-sextic-brake-from-architecture.md`, `findings/F175-lattice-2-9-eg-weight.md`, `findings/F234-Wvc-triple-closed-delta-2-9-pins-brake.md` | The $E_g$ clock potential reused verbatim, unmodified | exact/quantitative (unchanged) |

## Falsifier

`falsifier: stated`, though this card is a scope boundary rather than a numerical prediction, so
its "falsifier" is a closure condition:

1. **The reopening closes** if a future finding shows the domain-wall channel is *also* excluded —　
   e.g. if the $E_g$ condensate provably never passes through a symmetric/undecided phase (so
   $\delta$ is pinned identically everywhere from $t=0$, contradicting F285's own generic-measure
   argument) or if the wall network provably cannot avoid the standard overclosure problem for any
   value of the (currently unfixed) wall tension.
2. **The reopening is spent** (converted from "open" to a real result, positive or negative) when
   the four items `open_derivation_items()` names are actually computed and either produce a
   $\beta(M_\text{form})$ in the required F228 band or rule it out quantitatively.

## Status & history

`status: open` because the channel is genuinely untested past its precondition — this card asserts
neither that it succeeds nor that it fails. `rolls_up_to: CL209` because this is a scope note on
that card's reach, not an independent headline result.

## Sources

- `findings/F366-geon-domain-wall-reopening.md`
- `docs/claims/CL209-the-geon-relic-abundance-is-a-genuinely-free.md`
- `findings/F238-geon-relic-abundance.md`, `F228-geon-production-and-stability.md`,
  `F282-no-slow-roll-inflaton-sub-planckian-cutoff.md`,
  `F285-initial-condition-measure-cannot-tilt.md`
