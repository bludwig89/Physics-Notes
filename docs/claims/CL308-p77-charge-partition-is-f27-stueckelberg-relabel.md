---
id: CL308
title: 'The notebook p.77 charge partition (W± as the non-intrinsic half of charge, mass as its residue) is not an independent alternative to F27: it is the F27 Stueckelberg Ward identity relabelled, and the strong form in which W± absorbs the mass step''s missing charge finds no support in the model'
slug: p77-charge-partition-is-f27-stueckelberg-relabel
tier: supporting
kind: reinterpretation
status: live
domain: [SM]
exactness: machine
findings: [F396, F27, F41, F54, F143]
tests: [F396-charge-partition-p77]
modules: [casim.engine.gauge.derive_charge_partition]
constants: []
supersessions: []
reviews: [docs/reviews/F396-review-2026-09-21.md]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-21'
last_verified: '2026-09-21'
provenance: authored
review_state: authored
confidence: low
---

# CL308 — The p.77 charge partition is F27's Stueckelberg Ward identity, not a rival to it

## Statement

In the model's kernels the β-gauged mass step conserves electric charge Q = T₃ + Y/2 exactly (2×10⁻¹⁶) in the unitary-gauge frame and violates T₃ and Y by opposite amounts (ΔT₃ = −ΔY/2 ≠ 0); the missing T₃ is balanced by the neutral hypercharge direction, not by a charged W± carrier (a consequence of the Q-neutral F27 coupling, as in the SM). The p.77 statement "charge is intrinsic plus a field leg" is therefore exactly F27's Ward identity (ψ and the pure-gauge U transform together), with no new content and no prediction about mass. The strong reading — W± is the physical sink for the mass step's missing charge, and the mass step is forbidden without it — is not supported: the mass step is allowed at U = I. The p.77 analogy's own premise is also false here: the mass step conserves ⟨Σ_z⟩ exactly; it flips chirality.

## What it extends

Standard-Model electroweak symmetry breaking (mass step breaks T₃ and Y, preserves Q; W± as eaten Goldstone directions) and the angular-momentum analogy J = L + S (Greiner, Rel. QM pp.216–217). It contradicts the notebook's p.77 premise that the free-Dirac mass term flips spin.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F396-p77-charge-partition-relabel.md` | Legs A and B, all numbers | machine |
| record `F396-charge-partition-p77` | 14/14 legs, two controls verified red | machine |

## Falsifier

A kernel in which the mass step, in unitary gauge, transfers T₃ to a charged (Q = ±1) field mode rather than to Y — i.e. ΔQ_ψ ≠ 0 at U = I with a charged compensator carrying it — or an induced kinetic term for U with non-zero transverse stiffness (which would contradict F143) making the field leg dynamical, would revive the strong form.

## Status & history

`live` as a relabel of the weak form and a non-support of the strong form (2026-09-21); narrowed at review from a `no_go` wording. Not a claim that W± is unphysical: the kinetic sector of W remains F41's open problem. Does not touch F27's Ward identity, F320's masses, or the Weinberg angle (F138).

## Sources

- `findings/F396-p77-charge-partition-relabel.md`
- `references/physics-notes-complete.md` pp.76–77, 90–91
