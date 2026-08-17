---
id: CL020
title: '\"No doublers\" holds on the cubic FFT grid; on the true BCC zone the omega = pi mode sits at corner H'
slug: 'no-doublers-has-a-domain'
tier: headline
kind: non_claim
status: narrowed
domain: [QFT, SM]
exactness: exact
findings: [F278]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-02'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL020 — "No doublers" holds on the cubic FFT grid; on the true BCC zone the omega = pi mode sits at corner H

## Statement

The BCC Weyl walk has exactly one zero, at $k=0$, and no $\omega=\pi$ point **on the cubic FFT grid** ($L$ up to 128, both branches). On the **true BCC zone** the $\omega=\pi$ mode sits exactly at the corner H, $\lvert\mathbf k\rvert=2\pi/a=\pi\sqrt3$. Every observable in the tree is computed on the grid, so no result depends on the distinction — but **the unqualified form of the claim overstates it**.

## What it extends

The fermion-doubling problem (Nielsen–Ninomiya), which the model's single-zero dispersion is claimed to evade. The evasion is real on the computational grid and **qualified** on the true zone; both halves are stated.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F278-bcc-lattice-constant-two-over-root-three.md` | $a=2/\sqrt3$ in closed form, and the location of the $\omega=\pi$ mode at corner H on the true BCC zone | exact |

## Falsifier

**The discriminating test is not yet built.** An observable that distinguishes the cubic FFT grid from the true BCC zone would decide whether the corner-H mode is physical. Constructing it is a named open item; until then this card states the qualified form and nothing stronger.

## Status & history

`narrowed`, 2026-08-02 by revision 2, on F278. The broad form — "the BCC Weyl walk has no doublers" — is the one that overstates. This is the clearest example in the register of a claim that is **true as computed and false as stated**, which is why it is kept as a card rather than folded into a footnote.

## Sources

- `findings/F278-bcc-lattice-constant-two-over-root-three.md`
- `papers/Claims-and-Falsifiers-Summary.md` — Scope
