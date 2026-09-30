---
id: CL314
title: 'The model supports the quark-mass term and the trace sector of the Ji nucleon-mass decomposition (sigma_N = 46 MeV, 22% below measurement) but not the quark-energy / gluon-energy split (gluon momentum fraction 0.18-0.25 vs lattice 0.43-0.49)'
slug: 'nucleon-mass-ji-decomposition-model-support'
tier: supporting
kind: derivation
status: live
domain: [SM, QFT]
exactness: quantitative
findings: [F402, F122, F123, F77, F144, F152]
tests: [F402-baryon-mass-decomposition]
modules: [casim.engine.particles.baryon_mass_decomposition]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-24'
last_verified: '2026-09-24'
provenance: authored
review_state: authored
confidence: medium
---

# CL314 — The model supports the quark-mass term and the trace sector of the Ji nucleon-mass decomposition, but not the quark-energy / gluon-energy split

## Statement

The lattice-QCD nucleon-mass decomposition $M=H_E+H_m+H_g+H_a$ (Ji 1995; Yang et al. 2018: $33(6),\,9(2),\,37(6),\,23(1)\%$) reduces, for a nucleon at rest, to two model-supplied inputs: the mass term $H_m=m\,\partial M/\partial m$ and the quark momentum fraction $x_q$, via $H_a=\tfrac14(M-H_m)$, $H_E=\tfrac34(x_qM-H_m)$, $H_g=\tfrac34x_gM$. Built in the model's own sectors: **(i)** the NJL constituent nucleon ($M_N=3M_c$, F77/F123) gives an exact Feynman–Hellmann nucleon sigma term $\sigma_N=3m_0\,dM_c/dm_0=46.2$ MeV ($4.95\%$ of $M_N$), $-3.7\sigma$ / $-2.3\sigma$ below the measured $59.1(3.5)$ / $60.9(6.5)$ MeV (valence mean-field, binding neglected, $u+d$ only; reference-dependent, since individual lattice determinations span $\sim40$–$60$ MeV), together with an exact dilatation identity whose contact and regulator pieces cancel at $5$–$6\times M_N$ and each depend on the held-fixed variable — their sum $M_N-H_m$ is an Euler-theorem identity, not a model result. **(ii)** The quarter rule $H_a=\tfrac14(M-H_m)$ and $H_E+H_g=\tfrac34(M-H_m)$ are structural identities (the virial theorem, derived exactly in the Cornell sector) and are **not** independent tests. **(iii)** The $H_E:H_g$ split is **not supported**: the model's gluon momentum fraction at 2 GeV is $x_g=0.18$–$0.25$ (LO evolution from $\Lambda_\text{NJL}$ with the F144 $\alpha_s$ and the F152 frozen IR coupling) and $0.19$–$0.21$ (the F122 string, non-relativistic), against the lattice $0.427(92)$ (ETMC) to $0.49(9)$ (chiQCD-derived) — $2.0$–$2.9\sigma$ low, needing $2.3$–$3.0\times$ more evolution (mean $\alpha_s\approx1.1$–$1.5$) or a $0.29$–$0.40$ gluon share already present at $\Lambda_\text{NJL}$; the deficit is a statement about the non-derived $x_g=0$ start. **(iv)** The non-relativistic Cornell string solver cannot supply the mass term at all: $H_m=3m-\langle T\rangle<0$ at the F122 baseline. The operator-level $\langle N|F^2|N\rangle$ separation of $H_g$ from $H_a$ is not built.

## What it extends

The Ji nucleon-mass decomposition and its lattice determination (Yang et al., PRL 121, 212001, 2018) and the nucleon sigma term (Hoferichter et al. 2015; FLAG 2024). This card tests which of its four terms a specific constituent-quark / string / NJL model can reproduce and names the exact algebraic reason two of them cannot discriminate any model.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F402-ji-nucleon-mass-decomposition-model-support.md` | The construction, the three sector verdicts, the comparison table | machine (identities) / quantitative |
| `findings/F122-p2-dynamical-baryon-three-body.md`, `F123-p6-si-scale-matter-sector.md`, `F77-njl-gap-rpa-selfconsistent.md` | The Cornell ECG solver and the NJL gap equation / nucleon whose derivatives are taken | quantitative |
| `findings/F144-route-a-alpha-s-dimensional-transmutation.md`, `F152-ir-coupling-the-irface.md` | The model's $\alpha_s(\mu)$ and frozen IR coupling used for the evolution | quantitative |

## Falsifier

1. A relativistic (Salpeter-kinetic) three-body string baryon with $H_g\gtrsim30\%$, $H_m>0$ and $\lesssim7\%$ — repairs the NR sector and could close the deficit within the model's own string dynamics.
2. A model-native $\alpha_s(\mu)$ below $\approx1$ GeV giving $\tau\gtrsim0.4$–$0.53$ from $\Lambda_\text{NJL}$ to 2 GeV, or a derived $x_g(\Lambda_\text{NJL})\gtrsim0.3$ — kills the evolution deficit.
3. A beyond-mean-field NJL nucleon moving $\sigma_N$ to $\ge56$ MeV — kills the $\sigma_N$ undershoot.
4. A dynamical baryon in the gauge sector yielding $\langle N|F^2|N\rangle$ — permits the operator-level split.

## Status & history

First issued 2026-09-24 from `findings/F402-ji-nucleon-mass-decomposition-model-support.md`, answering `docs/theory/notebook-v2/NB2-004-nucleon-mass-field-energy.md` open question 2. Independent review (2026-09-24, CONFIRMED-NARROWER) narrowed the deficit from $2.9\sigma$ to $2.0$–$2.9\sigma$ (second lattice target), the NJL anomaly-analogue to an identity, and the sigma-term undershoot to reference-dependent. `confidence: medium` because the evolution start scale ($\Lambda_\text{NJL}$, $x_g=0$) and the frozen IR coupling are model motivated but not derived. No prior status to narrate.

## Sources

- `findings/F402-ji-nucleon-mass-decomposition-model-support.md`
- Yang et al., PRL 121, 212001 (2018), arXiv:1808.08677; Ji, PRL 74, 1071 (1995); Hoferichter et al. 2015; FLAG Review 2024, arXiv:2411.04268
- `docs/theory/notebook-v2/NB2-004-nucleon-mass-field-energy.md` — the question this card answers
