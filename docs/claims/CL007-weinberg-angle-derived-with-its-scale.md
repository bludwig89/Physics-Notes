---
id: CL007
title: 'The Weinberg angle is derived, with its scale'
slug: 'weinberg-angle-derived-with-its-scale'
tier: headline
kind: derivation
status: live
domain: [SM]
exactness: exact
findings: [F41, F49, F138]
tests: []
modules: []
constants: [sin2_thetaW_onshell]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL007 — The Weinberg angle is derived, with its scale

## Statement

$\sin^2\theta_W=\tfrac14$ is the **matching value at the compositeness scale** $\mu_\star=4\pi v=3.09$ TeV, forced by hypercharge having no lattice kinetic term. Running Higgs-free to $M_Z$ gives $0.23173$ (**+0.22%** vs MS-bar $0.23122$); the on-shell endpoint is $\sin^2\theta_W^\text{os}=\tfrac29\Leftrightarrow m_Z/m_W=3/\sqrt7$. **Zero new parameters** — the model's two existing rulers only.

## What it extends

The Standard Model, in which the weak mixing angle is a free input. The model predicts the **ratio** $m_Z/m_W$, not $m_W$ and $m_Z$ in absolute terms — see **CL016**.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F41-hypercharge-higgs-free-su2.md` | Hypercharge compatible with the Higgs-free chiral $SU(2)$; no lattice kinetic term | exact |
| `findings/F49-bcc-finite-k-weinberg-angle.md` | BCC bond/sublattice counting reproduces $\sin^2\theta_W=\tfrac29$ (partial derivation) | exact |
| `findings/F138-weinberg-gap-closure-4piv-matching.md` | $\sin^2\theta_W=\tfrac14$ as the compositeness-scale matching condition at $\mu_\star=4\pi v$ | exact |

Headline numbers: $\sin^2\bar\theta_W(M_Z)=0.23173$ vs $0.23122$ (+0.22%); $m_Z/m_W=3/\sqrt7=1.133893$ vs $91.1880/80.3692=1.134614$ (**−0.064%**). Both zero-free-parameter, against **PDG 2025 / CODATA 2022**.

**Open:** F49's title says *partial derivation*; the 8/7 closure is a named open item (`docs/roadmaps/completed/prompt-weinberg-8over7-closure.md`, F141, F147). This card states what is closed.

## Falsifier

A precision $m_W$ that moved $m_Z/m_W$ off $3/\sqrt7$ by more than the running uncertainty. **CL014 carries the threshold**, and records why the PDG 2025 re-analysis is a passed test rather than a retrofit.

## Status & history

`live`. **Revision 2 (2026-08-02) moved the headline** from the UV value $2/\sqrt3$ (1.77%) to the on-shell endpoint $3/\sqrt7$ (−0.064%) — the number the tree actually computes. The UV value is **not withdrawn**; it is the matching value at $\mu_\star$, and quoting it as the headline residual was the error.

## Sources

- `findings/F49-bcc-finite-k-weinberg-angle.md`
- `findings/F138-weinberg-gap-closure-4piv-matching.md`
- `findings/F41-hypercharge-higgs-free-su2.md`
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 7, revision-2 note (ii)
