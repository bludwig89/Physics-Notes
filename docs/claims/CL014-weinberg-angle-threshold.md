---
id: CL014
title: 'The chain is committed to sin^2(theta_W) = 1/4 at 4*pi*v and 2/9 on shell'
slug: 'weinberg-angle-threshold'
tier: headline
kind: prediction
status: live
domain: [SM]
exactness: exact
findings: [F49, F138, F231]
tests: []
modules: []
constants: [sin2_thetaW_onshell]
supersessions: []
reviews: []
rolls_up_to: CL007
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL014 — The chain is committed to sin^2(theta_W) = 1/4 at 4*pi*v and 2/9 on shell

## Statement

The chain is committed to $\sin^2\theta_W=\tfrac14$ at $\mu_\star=4\pi v$ and $\sin^2\theta_W^\text{os}=\tfrac29$ on shell, i.e. $m_Z/m_W=3/\sqrt7$.

## What it extends

The Standard Model's free mixing angle. Because both the UV matching value and the on-shell endpoint are fixed rationals, the model has **no** parameter with which to absorb a shifted $m_W$.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F49-bcc-finite-k-weinberg-angle.md` | $\sin^2\theta_W=\tfrac29$ from BCC bond/sublattice counting | exact |
| `findings/F138-weinberg-gap-closure-4piv-matching.md` | $\tfrac14$ as the matching condition at $\mu_\star=4\pi v$ | exact |
| `findings/F231-weinberg-2over9-onshell-face-of-1over4.md` | $\tfrac29$ is the on-shell face of the same $\tfrac14$, not a second number | exact |

## Falsifier

**A precision $m_W$ that moved $m_Z/m_W$ off $3/\sqrt7$ by more than the running uncertainty** falsifies it.

This makes the **PDG 2025 re-analysis a passed test rather than a retrofit**: $3/\sqrt7$ was fixed *before* PDG excluded the CDF-II $m_W$ measurement for low compatibility. Against the resulting $m_W=80.3692\pm0.0133$ the model gives $-0.064\%$ (implied $m_W=80.4203$). Had it been tuned to CDF it would now look worse; it was not, and it survives the exclusion cleanly.

## Status & history

`live`. This is the register's one **out-of-sample survival** and is recorded as such: the prediction pre-dated the measurement revision that could have killed it.

## Sources

- `findings/F49-bcc-finite-k-weinberg-angle.md`
- `findings/F138-weinberg-gap-closure-4piv-matching.md`
- `papers/Claims-and-Falsifiers-Summary.md` — falsifiable predictions and headline numbers
