---
id: CL004
title: 'Exactly three fermion generations'
slug: 'exactly-three-fermion-generations'
tier: headline
kind: derivation
status: contingent
domain: [SM]
exactness: exact
findings: [F75, F292, F342]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-31'
provenance: authored
review_state: authored
confidence: high
---

# CL004 — Exactly three fermion generations

## Statement

The group theory is a **theorem** about the cubic point group $O_h$: from $\sum d^2=\lvert O_h\rvert=48$ the maximal single-valued irrep dimension is 3, and the parity-odd triplet $T_{1u}$ is unique. The **physical identification** — that a generation *is* that triplet, realised by the scalar mass selecting the odd-parity shell — is a **stated hypothesis**, not a theorem. Granting the hypothesis, a fourth generation is forbidden.

## What it extends

The Standard Model, which takes the generation count as an input. The model derives the *bound* from point-group representation theory and derives the *count* only under a named hypothesis. The contingency is stated because F79's structural $G$ (CL008) inherits the same status.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F75-three-generations-from-bcc-irrep-selection.md` §7 | The $O_h$ theorem is exact; the physical identification is stated as a hypothesis in the finding's own status line | exact (group theory) |
| `findings/F292-no-higher-multiple-of-three.md` §6 | The model's *other* instance of a "3" (frozen $d=3n$ copies) is explicitly declined as a generations reading, because those directions carry no dynamics — shown not to be the reason F75 §7 stays open (that objection does not transfer to the $T_{1u}$ shell states, which do carry real dispersion) | exact |
| `findings/F342-generation-identification-condition-i-vacuous.md` | F75's own operational condition (i) ("identical gauge quantum numbers") is shown to supply **zero selecting power** between $T_{1u}$ and $T_{2g}$ under the charge structure the adopted engine actually implements (a scalar, diagonal in the site basis) — forced by the shell's 8 vertices forming a single $O_h$ orbit. Exhibits exactly what *would* supply selecting power (a non-diagonal, irrep-block-dependent coupling) and confirms none exists outside three exploratory fork files | exact, 11/11 PASS, 2 controls |

F75 is a **Candidate** finding. F342 sharpens *why* CL004 stays `contingent`: not merely "unproven," but shown not to be forced by anything currently in the model's dynamics.

## Falsifier

Discovery of a fourth sequential fermion generation falsifies the claim outright. Non-discovery does **not** confirm it, because the physical identification is a hypothesis rather than a theorem.

## Status & history

`contingent`, on the physical identification of a generation with the $T_{1u}$ triplet. This is the status the claims summary reached in **revision 2 (2026-08-02)**, correcting revision 1's "three generations is a theorem", which overstated F75's own status line. The card records the correction, not merely the corrected text.

**Narrowed, not promoted (2026-08-31, F342).** F292 independently found and explicitly declined a *different*, weaker candidate identification (frozen $d=3n$ copies) — that decline does not bear on F75's mechanism, which carries genuine dispersion. What does keep CL004 `contingent` is sharper than "the group theory doesn't fix the physical read": F75's own condition (i) is the only part of its operational definition that could in principle discriminate a physical reading, and F342 shows it is guaranteed, by the model's founding homogeneity posit, to do no such work under the gauge structure actually implemented — for $T_{1u}$ or for any other subspace of the shell. Rubric row **C1** stays `PARTIAL` for this reason; **B10**'s dependence on the generation-count *parity* (F324) is unaffected, since F324 never invokes condition (i).

## Sources

- `findings/F75-three-generations-from-bcc-irrep-selection.md`
- `findings/F292-no-higher-multiple-of-three.md`
- `findings/F342-generation-identification-condition-i-vacuous.md`
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 4 and revision-2 note (iii)
