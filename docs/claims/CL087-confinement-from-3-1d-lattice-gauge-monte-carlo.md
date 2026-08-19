---
id: CL087
title: 'Confinement from 3+1D lattice-gauge Monte-Carlo: the engine and the Option-A/Option-C bridge, narrowed off the hypercubic ensemble'
slug: 'confinement-from-3-1d-lattice-gauge-monte-carlo'
tier: supporting
kind: derivation
status: narrowed
domain: [QCD]
exactness: machine
findings: [F94, F323, F265, F311]
tests: [gauge-bcc-mc-d4, FA-lgt-mc, FA-vs-FC-comparison]
modules: [src/casim/engine/gauge/bcc_action.py, src/casim/engine/forks/gauge/lgt_fork_A_mc.py]
constants: []
supersessions: [S21-F94-hypercubic-action-not-the-model-lattice]
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-04'
last_verified: '2026-08-17'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL087 — Confinement from 3+1D lattice-gauge Monte-Carlo, narrowed

> **NARROWED 2026-08-17.** This card was seeded on F94 alone, and F94's ensemble
> is now `partially_superseded` (ledger `S21`). What the card may still assert is
> below; what it may not is stated with it.

## Statement

**Narrowed to two things, both of which survive S21.**

1. **The engine is certified.** A Cabibbo–Marinari SU(3) pseudo-heat-bath with
   SU(2)-subgroup over-relaxation and a Lüscher–Weisz two-level estimator is
   implemented and verified: SU(3) closure at `1.1e-15`, over-relaxation action
   invariance at `1.2e-16`, the staple/action-gradient ratio-4 identity at
   `8.9e-16`, and a measured 84× variance reduction. These are properties of the
   sampler, not of the lattice it runs on, which is why S21 keeps them live.
2. **Option A and Option C are the same physics re-parametrised.** The CMP2
   bridge — a measured string tension fixes Option C's only free parameter via
   `v* = sqrt(sigma_A / 2 pi)`, reproducing `sigma_A` to `1e-16` — is an
   algebraic identity independent of the ensemble's lattice, and F311 leg B
   re-verified it at `1.2e-16` across five seeds.

**What this card no longer asserts.** That the 3+1D confinement measurement was
performed *on the model's lattice*. It was not: F94 samples a simple-hypercubic
Wilson action, which F265 proved has an exact kernel freeing one of the four
`<111>` link axes and missing asymptotically 1/3 of the curvature-carrying link
content. Both actions share a classical continuum limit, so F94's normalisation
anchors (FA4, FA5) could pass on a blind action and their passing is not evidence
the ensemble was right. Any `sigma` or `V(R)` read off that ensemble is a number
about the wrong lattice. The replacement measurement is F323's, on the genuine
BCC action as `BCC_3 spatial x Z` Euclidean time.

**What nobody has claimed, before or after.** An area law. Completeness row B7's
residual is a missing transfer matrix with positivity, and no amount of sampling
supplies one.

## What it extends

Narrowly and honestly: nothing in QCD that was not already standard. The engine
is the textbook Cabibbo–Marinari/Lüscher–Weisz apparatus, correctly implemented;
the card's non-trivial content is internal — the CMP2 bridge, which relates two
of *this model's* routes to binding (F94's Option A and F86's dual-superconductor
Option C) and shows they are not independent evidence for each other. The
original seed text asserted that the `docs/claims/README.md` bar was not met;
that is still true, and this narrowing does not meet it either. It only makes the
card's scope correct.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F94-lattice-gauge-mc-confinement-vs-F86.md` | The engine certificates FA1–FA3 and the CMP2/CMP3 comparison. Carries a `PARTIALLY SUPERSEDED` banner; read the banner before the body | machine |
| `docs/theory/supersessions.yaml` `S21` | Which half is dead (the ensemble as a model-lattice measurement) and which is live (the sampler, the bridge, the estimator) | — |
| `findings/F265-bcc-gauge-action-blindness.md` | Why the hypercubic action is blind: the exact simple-cubic kernel, and the 1/3 content loss | exact |
| `findings/F323-anisotropy-derived-and-d4-casimir.md` | The replacement d=4 leg on the BCC action, 28/28 with 5/5 controls `CONTROL`; the staple identity at `2.3e-16` and gauge invariance at `3.8e-17` | machine |
| `findings/F311-gap5-three-numbers-adjudicated.md` | CMP2's identity re-verified at `1.2e-16` over five seeds; also why `FA_vs_FC_comparison.json`'s baseline drift is an undeclared input and **not** a supersession | machine |

The card is still `review_state: unreviewed-seed`: its classification was
inferred mechanically in 2026-08-04 and has not been confirmed by hand. The
narrowing above changes its *scope*, not its review state, and it may still not
be cited as independent support.

## Falsifier

`falsifier: stated`, replacing `unset`. Two routes, both runnable: a
non-confining BCC-ensemble potential from `run-bcc-confinement-d4`, or a failure
of the CMP2 identity when `sigma_A` is taken from the BCC action instead of the
hypercubic one. The second is the sharper test, because CMP2 is the only
quantitative content the card retains and it has never been evaluated on the
correct ensemble.

## Status & history

- **2026-08-04** — seeded `live` from F94's own status line as part of standing
  up the claims layer (D12). `findings: [F94]`, no tests, no modules, no
  falsifier. No physics was read or judged in creating it.
- **2026-08-17** — **narrowed.** S21 put `F94` in a `superseded:` list, which is
  the condition `tools/check_claims.py` fires on for a `live` card resting on
  wholly superseded ground. That fire was correct: the card's statement was about
  a measurement on the wrong lattice. Rather than withdraw it, the two parts that
  survive S21 are stated explicitly and the ensemble claim is removed; F323,
  F265 and F311 are added as the surviving support, along with the test records
  and modules the original seed left empty, and a falsifier replaces `unset`.

## Sources

- `findings/F94-lattice-gauge-mc-confinement-vs-F86.md`
- `findings/F323-anisotropy-derived-and-d4-casimir.md`
- `findings/F265-bcc-gauge-action-blindness.md`
- `findings/F311-gap5-three-numbers-adjudicated.md`
- `docs/theory/supersessions.yaml` — record `S21`
- `docs/claims/README.md` — the `unreviewed-seed` contract
