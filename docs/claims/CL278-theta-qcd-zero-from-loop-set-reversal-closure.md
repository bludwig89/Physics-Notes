---
id: CL278
title: The rule contains no theta-term, and no loop generates one — theta_QCD = 0 because the minimal-loop set is closed under reversal
slug: theta-qcd-zero-from-loop-set-reversal-closure
tier: supporting
kind: derivation
status: live
domain: [QCD, SM, QFT]
exactness: exact
findings: [F321, F53, F43, F305, F307, F265, F91, F337, F340]
tests: [F321-strong-cp, F340-strong-cp-nonperturbative]
modules: [casim.engine.gauge.colour_theta, casim.engine.gauge.lpt_bcc_vertex]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-17
last_verified: 2026-08-31
provenance: authored
review_state: authored
confidence: high
---

# CL278 — theta_QCD = 0 from reversal closure of the minimal-loop set

## Statement

The model's QCD vacuum angle is **not a free parameter**: it is fixed at zero by the structure of
the rule's gauge sector, and no loop correction of any order can move it.

In Euclidean signature the $\theta$-term is the unique purely imaginary gauge invariant — the
weight is $e^{-S_\text{YM}+i\theta Q}$ — so *"the rule's Euclidean action is real"* and *"the rule
contains no $\theta$-term"* are the same statement. The rule's 20 oriented minimal rhombi (6
spatial $\times2$, 4 temporal $\times2$) are **closed under reversal** (0 missing, exact
combinatorics), so $\sum_\text{loops}\operatorname{Tr}U=2\operatorname{Re}\sum\operatorname{Tr}U$
for every configuration. Measured on Haar-random SU(3) configurations on a 4-D BCC$\times$time
lattice at 99.7 % disorder: $\operatorname{Im}S = 1.2\times10^{-14}$; $S$ is invariant under
$U\to U^*$ ($2.5\times10^{-14}$) while the one-sense loop functional is odd under it at literal
`0.0`. Every position-space vertex coefficient is real at literal `0.0` at 2, 3 and 4 legs with
colour indices sampled, and that class of functions is closed under products and under $q\to-q$
symmetric loop integration — so the effective action is real at **every** order.

The measurement has full sensitivity: injecting $\theta$ by hand gives
$\operatorname{Im}S = -\theta\sum Q$ exactly (literal `0.0` residual) with $\sum Q = 2.078 \ne 0$,
so the zero is a measurement and not the absence of an operator.

## What it extends

In continuum and lattice QCD, $\theta$ is an **independent input** — the strong CP problem is that
experiment bounds it at $\lvert\bar\theta\rvert\lesssim10^{-10}$ with no principle in the Standard
Model requiring it. On a lattice the $\theta$-term is *added by hand*; every standard plaquette
action is real for exactly the reason above. What is different here is that there is no "by hand":
the rule fixes the action, so $\theta$ has no slot to occupy, and the 2026-06-29 audit's open
question — whether $\theta_\text{QCD}=0$ survives loops — is answered by a closure property rather
than order by order.

This card asserts the **first** term of $\bar\theta = \theta + \arg\det M_q$ only. See
[CL279](CL279-theta-bar-not-predicted-strong-cp-not-solved.md) for the scope boundary, which is
the more important half of the pair.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F321-strong-cp-theta-zero-and-loop-stable.md` | 20/20 checks, 3/3 controls CONTROL over disjoint red sets | exact / machine |
| record `F321-strong-cp` (tier gate) | T0a-b reversal closure; T1a $\operatorname{Im}S$; T2a-e vertex coefficient reality; T3c $\theta$-sensitivity | literal `0.0` where stated |
| `test-results/F321_strong_cp.json` | the result artifact | — |
| `findings/F305-bcc-rhombic-lpt-vertices.md`, `findings/F307-action-consistent-d1-and-a-live-refold.md`, `findings/F265-bcc-gauge-action-blindness.md` | the rhombic BCC gauge action and its true vertices, which this rests on | exact gates |
| `findings/F91-pairing-classification-theorem.md` | gluon propagator **even** (forced) — puts the rule on the P-even branch, so the conclusion also holds on the other side of `lpt_bcc_vertex`'s declared action fork (F321 T4a/T4b) | exact |

## Falsifier

Three independent computational kills, all cheap:

1. **Exhibit one SU(3) configuration with $\operatorname{Im}S \ne 0$** at the gate tolerance
   ($10^{-10}$) on the rule's full 20-loop set. One counterexample ends the claim.
2. **Exhibit one vertex coefficient with $\operatorname{Im}c\ne0$** at any leg count and any
   colour assignment on the rhombic action. The claim asserts literal `0.0`.
3. **Show the rule's minimal-loop set is *not* reversal-closed** — i.e. that the physical rule
   selects one sense per rhombus and `lpt_bcc_vertex._loops_bcc`'s both-senses enumeration is a
   coding convention rather than the rule's content. This is the load-bearing input, and it is the
   one this card is least sure of: F321's control 1 shows exactly this perturbation destroys the
   result.

The claim does **not** have an observational falsifier, because a neutron-EDM measurement bounds
$\bar\theta$, not $\theta$. That is CL279's subject.

## Status & history

`live`, `confidence: high` as of F340 (2026-08-31), upgraded from `medium`. The two reasons for
`medium` recorded at first issue are resolved or narrowed:

1. **The action fork is closed, not merely survived.** F337 (2026-08-30) decided ledger row L6:
   the rule's gauge action at finite $a$ is the rhombic action's **own** quadratic form, not the
   F26/$\Omega_\text{even}$ alternative — the latter independently disqualified (F308 §3: not
   periodic under $2\pi$, $4\pi$, or $8\pi$ axis shifts, i.e. not a well-defined function on the
   Brillouin zone the vertices live on). F340 checks — rather than assumes — that this claim's
   construction already sits on that decided branch: `colour_theta`'s loop-word action is exactly
   `lpt_bcc_vertex`'s rhombic action (exact set-equality of all 20 loop words). So F321 §3–4 were
   never on an undecided branch; T4's "survives both branches" is superseded by "was always on the
   one branch that is now known correct".
2. **Non-perturbative $\theta$-sectors are addressed as far as reality-per-configuration can
   address them.** F340 upgrades F321 T1a from a measurement (three sampled configurations) to an
   exact proof: the identity $\text{holonomy}(U,\text{reverse}(w)) = \text{holonomy}(U,w)^\dagger$
   holds for every word and every configuration (checked to $4.97\times10^{-16}$, floating-point
   roundoff), which combined with reversal closure (T0a) and the trivial trace identity proves
   $\operatorname{Im}S=0$ for the **full** non-perturbative configuration space, any topological
   content included — not a sampled subset. F340 §3 further shows the model's partition function,
   as literally constructed (an unrestricted sum over all link configurations with a real,
   $\theta$-independent-in-phase weight), **is** the $\theta=0$ member of the standard
   $Z(\theta)=\sum_Q e^{i\theta Q}Z_Q$ family by direct comparison to the definition — there is no
   room for a hidden $\theta$ between sectors, because the construction never introduces the
   $e^{i\theta Q}$ grading for any $Q$. Cross-checked (not verified in full) against Vafa & Witten
   (1984), whose hypothesis is exactly this reality property. What is **not** addressed, and is
   genuinely separate: whether this lattice's naive clover-based $Q$ is a properly quantized
   topological invariant in the continuum-limit sense — a standard, well-documented lattice-QCD
   subtlety (F321 §7 already found the clover does not flip sign under the model's own parity map
   at finite $a$), unrelated to whether $\theta$ is zero.

Separately recorded because it corrects a live citation: completeness row **B11**'s residual
quoted $3.3\times10^{-16}$ against F53, but F53 P5 measures the F27 **complex-mass** phase and
F53's own Remaining section says strong CP *"is a separate phase in the gluon sector (F43),
untouched here"*. The number was attached to the wrong object for three reports. F321 T5a/T5b
record it under the quantity it measures.

## Sources

- `findings/F321-strong-cp-theta-zero-and-loop-stable.md`
- `findings/F340-strong-cp-l6-bridge-and-nonperturbative-reality.md` — the action-fork closure and
  the non-perturbative reality proof this Status section rests on
- `findings/F337-l6-decided-native-sweep-outside-bracket.md` — closes ledger row L6, the object F340 confirms F321 already used
- `findings/F53-fg9-C-CP-per-species.md`
- `findings/F305-bcc-rhombic-lpt-vertices.md`
- `findings/F265-bcc-gauge-action-blindness.md`
- `findings/F91-pairing-classification-theorem.md`
- `src/casim/engine/gauge/colour_theta.py`
- `docs/status/completeness-2026-08-07.md` — row B11
- `docs/audits/physics-audit-report-2026-06-29.md` — the G1 caveat and the "Strong CP at loop level" row
- Vafa, C. & Witten, E., *Phys. Rev. Lett.* **53**, 535 (1984); *Nucl. Phys. B* **234**, 173 (1984)
  — cross-check cited by F340 §3, not verified against this model's full hypothesis set
