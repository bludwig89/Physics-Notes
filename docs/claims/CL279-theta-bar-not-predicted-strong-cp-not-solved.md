---
id: CL279
title: The model does not predict theta-bar and does not solve the strong CP problem — the residual is arg det M_q
slug: theta-bar-not-predicted-strong-cp-not-solved
tier: supporting
kind: non_claim
status: not_claimed
domain: [QCD, SM]
exactness: exact
findings: [F321, F53]
tests: [F321-strong-cp]
modules: [casim.engine.gauge.colour_theta]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: none
first_issued: 2026-08-17
last_verified: 2026-08-17
provenance: authored
review_state: authored
confidence: high
---

# CL279 — theta-bar is not predicted, and the strong CP problem is not solved

## Statement

The project does **not** assert that it solves the strong CP problem, and does **not** predict a
value for $\bar\theta$.

The physical, basis-independent invariant is $\bar\theta = \theta_\text{QCD} + \arg\det M_q$.
[CL278](CL278-theta-qcd-zero-from-loop-set-reversal-closure.md) closes the **first** term exactly.
The second term is set by the quark mass texture, which is open-derivations **E6** (6 quark masses)
and **E7** (4 CKM parameters), and nothing in the tree closes it. At one generation it is zero
(F321 T5a/T5b, literal `0.0`) — but one generation carries no CKM phase, so that is a statement
about a sector where the question does not arise.

Two distinctions this card exists to hold:

1. **"No slot for the parameter" is not Peccei–Quinn.** Peccei–Quinn asks why a *free* parameter
   is tiny and answers with a dynamical relaxation mechanism plus a new particle. This model
   removes $\theta$ from the input list because the rule fixes the action; there is no relaxation
   mechanism, no axion, and no explanation of smallness — smallness is not the shape of the
   statement. The result is *contingent on the rule being the right rule*, which a PQ mechanism
   is not.
2. **A neutron-EDM bound does not test CL278.** Experiment bounds $\bar\theta$, so any EDM
   comparison tests the **sum**, and the sum's second term is open. Quoting CL278 against an EDM
   limit would be an error.

## What it extends

Nothing. This card is a scope boundary, recorded so that the absence of a $\bar\theta$ prediction
is not read as one — the same role CL016's non-claim rows played for the absolute boson masses
before F320 narrowed them. It exists because CL278 is unusually easy to over-read: "the model has
no $\theta$-term" reads at a glance like "the model solves strong CP", and it does not.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F321-strong-cp-theta-zero-and-loop-stable.md` | §5-§6: the first term of theta-bar closes, the second does not; the ledger consequence stated narrowly | exact |
| record `F321-strong-cp`, leg T5c | records theta-bar = theta_QCD + arg det M_q with the second term marked open (E6/E7) | — |
| `docs/status/open-derivations.md` | E6, E7 open; E9 is the row this narrows | — |

*This is a non-claim, so the "evidence" is evidence that the boundary is where the card says it
is — not evidence for an assertion.*

## Falsifier

`none`, and the structure is named: a non-claim asserts nothing, so no observation can contradict
it. What *changes* this card is not a falsification but a derivation — if E6/E7 close and
$\arg\det M_q$ becomes computable, this card is superseded by a card that states $\bar\theta$ with
its residual, and the neutron-EDM bound becomes a live test at that moment.

## Status & history

`not_claimed`, first issued 2026-08-17 alongside F321 and CL278.

The parameter-ledger consequence is narrower than "strong CP solved" and is the accurate reading:
$\theta_\text{QCD}$ was ledger parameter **#19**, an independent input, and it stops being
independent — one input removed, none added, and the strong-CP question becomes a *function of*
the quark mass texture rather than a separate unknown. Open-derivations **E9** should be read as
closed in that sense and in no other.

## Sources

- `findings/F321-strong-cp-theta-zero-and-loop-stable.md`
- `findings/F53-fg9-C-CP-per-species.md`
- `docs/claims/CL278-theta-qcd-zero-from-loop-set-reversal-closure.md`
- `docs/status/open-derivations.md` — E6, E7, E9
- `docs/status/completeness-2026-08-07.md` — row B11
