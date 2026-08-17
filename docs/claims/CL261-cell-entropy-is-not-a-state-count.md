---
id: CL261
title: 'The Bekenstein-Hawking per-cell entropy 2 pi sqrt3 cannot be a microstate count of any finite cell Hilbert space'
slug: cell-entropy-is-not-a-state-count
tier: supporting
kind: no_go
status: live
domain: [GR, QM]
exactness: exact
findings: [F300, F190]
tests: [F300-lattice-thermodynamics]
modules: [casim.engine.interactions.thermodynamics]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: none
first_issued: 2026-08-06
last_verified: 2026-08-06
provenance: authored
review_state: authored
confidence: high
---

# CL261 — The per-cell entropy is not a state count

## Statement

F190 reproduces $S=A/4$ by giving each F107 horizon cell exactly $s_\text{cell}=2\pi\sqrt3=10.882796$ nats, and names its open step as *"show a boundary cell carries $e^{2\pi\sqrt3}$ states from the BCC/Weyl content."* That step cannot be discharged, for a reason that needs no model input at all: **a dimension count of a finite Hilbert space is $\ln W$ with $W$ a positive integer, and a count of two-state modes is $n\ln2$ with $n$ an integer, and $2\pi\sqrt3$ is neither.**

$$e^{2\pi\sqrt3}=53252.295\ \ (0.295\ \text{from the nearest integer}),\qquad \frac{2\pi\sqrt3}{\ln2}=15.7006\ \ (0.299).$$

The nearest integer mode count, $n=16$, gives $16\ln2=11.0904$ nats and overshoots by **1.91%**.

Separately, and in the other direction, the *necessary* capacity condition passes: the model's 48 Weyl fields (F47/F279), each two-component, give 96 fermionic modes per site and a capacity of $96\ln2=66.542$ nats against a requirement of 10.883 — a surplus of $6.11\times$, with the horizon occupying 16.4% of it.

## What it extends

Bekenstein–Hawking entropy is routinely glossed as "counting horizon microstates". This claim states, inside a model that supplies a specific cell and a specific field content, that the counting reading is arithmetically unavailable at the level of a single cell: the required entropy is not the logarithm of any integer. The object has to be an **entanglement** entropy, whose spectrum is continuous and carries no integrality constraint.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F300-lattice-native-thermodynamics.md` §5 | the no-go and the capacity condition | exact |
| `findings/F190-horizon-entropy-lattice-microstates.md` E1 | the target: $s_\text{cell}=a^2/(4\ell_P^2)=2\pi\sqrt3$, matched to $10^{-9}$ | exact |
| record `F300-lattice-thermodynamics` (gate), G10-12 / G10-13 | $0.295$ / $0.299$ from integrality; capacity $6.11\times$ | exact / quantitative |

## Falsifier

`none`, and the structure is named: the claim is a statement of arithmetic about a transcendental number, not about the model. $2\pi\sqrt3$ is irrational, so it is not $n\ln2$ for integer $n$; $e^{2\pi\sqrt3}$ is measured here to sit $0.295$ from the nearest integer, far outside any numerical doubt. No observation bears on it. What *can* change is the target: if F107's $a$ moved, $s_\text{cell}=a^2/(4\ell_P^2)$ would move with it and the integrality question would have to be asked again of the new number.

## Status & history

`live`. Two things this card deliberately does **not** say.

1. **It does not move rubric row E9.** E9 grades `PARTIAL` on F190's posit and continues to. This claim kills one route to discharging it and passes a necessary condition on another; it derives nothing. A later reader must not cite CL261 as progress on the value of $s_\text{cell}$.
2. **It does not refute F190.** F190's consistency relation stands exactly as written; what is refuted is the *method* F190 named for closing it. The replacement route — compute the boundary entanglement entropy under the constraint, using the correlation-matrix machinery F300 §4 builds — is named in F300 §8.

A numerical coincidence is recorded alongside and explicitly **not** claimed: in the same lattice units the BCC reciprocal (fcc) conventional cube side is $4\pi/(2/\sqrt3)=2\pi\sqrt3$, identical to $s_\text{cell}$ in nats. Both trace to $a^2=8\pi\sqrt3\,\ell_P^2$; one is a reciprocal length and the other an entropy, and no derivation connects them. See `thermodynamics.reciprocal_cube_coincidence()`.

## Sources

- `findings/F300-lattice-native-thermodynamics.md` §5
- `findings/F190-horizon-entropy-lattice-microstates.md`
- `findings/F47-majorana-seesaw-higgs-free.md`, `findings/F279-hypercharge-constraint-attribution.md` (the 48-Weyl content)
- `docs/status/completeness-2026-08-04.md` row E9
