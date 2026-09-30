---
id: CL315
title: 'In the cube-axis (E_g) charged-lepton frame no residual symmetry drawn from O_h fixes PMNS; the only surviving O_h constraint is CP-type mu-tau reflection, and the [111]-trimaximal frame instead admits TM1'
slug: 'no-oh-residual-fixes-pmns-in-cube-frame'
tier: supporting
kind: no_go
status: open
domain: [SM]
exactness: quantitative
findings: [F403]
tests: [F403-oh-residual-pmns]
modules: [casim.engine.particles.derive_oh_residual_pmns]
constants: []
supersessions: []
reviews: [docs/reviews/F403-review-2026-09-24.md]
rolls_up_to: CL223
falsifier: stated
first_issued: '2026-09-24'
last_verified: '2026-09-24'
provenance: authored
review_state: authored
confidence: high
---

# CL315 — No O_h residual symmetry fixes PMNS in the cube-axis frame

## Statement

With the charged leptons exactly diagonal on the cube axes (the adopted E_g reading, F76/F93), every non-identity rotation of $O$ acting on the $T_{1u}$ generation triplet, imposed as a residual symmetry of the neutrino mass matrix, pins a PMNS column to $(1,0,0)$, $(0,\tfrac12,\tfrac12)$ or the all-$\tfrac13$ trimaximal matrix, all excluded by NuFIT 6.0 NO at 3σ: the first two contain a zero while no PMNS element in the box is below $0.0203$, and the all-$\tfrac13$ matrix needs $\sin^2\theta_{13}=\tfrac13$ against a 3σ upper edge of $0.0239$. The only $O_h$ residuals compatible with data are generalised-CP ones: diagonal $X$ ($J=0$), or the $y\leftrightarrow z$ mirror (μ–τ reflection: $\theta_{23}=45°$, $\delta=\pm90°$). In the [111]-trimaximal frame, which writes the same Koide spectrum as a circulant, the like-sign face-diagonal $C_2'$ give TM1, $\sin^2\theta_{12}=1-2/(3\cos^2\theta_{13})\in[0.3170,0.3195]$ with $\delta\in[252.4°,293.4°]$. Enumerated over the whole subgroup lattice (98 subgroups of $O_h$, of which the 49 elementary abelian 2-groups are the only ones admitting non-degenerate masses), the cube-frame no-go holds for every subgroup, and it also holds in the face-diagonal ($C_2'$-eigenbasis) frame. No three-column ($Z_2\times Z_2$) residual is viable in any frame. The BCC reading adds nothing new: its $[111]$ directions are non-orthogonal, so the trimaximal ($C_3[111]$-eigenbasis) frame is the only $O_h$ frame that opens. The group theory is exact; the viability verdicts rest on data, so the card's class is quantitative.

## What it extends

The residual-symmetry ("direct") approach to lepton mixing in the Standard Model extended by flavour symmetry, where $S_4$ is the minimal group giving tribimaximal mixing (Lam, arXiv:0809.1185). Here $S_4\cong O$ is the lattice's own rotation group, and the model's charged-lepton frame is fixed by its E_g condensate. The claim is that this frame is incompatible with *every* $O$ residual in the neutrino sector, so the model cannot use lattice symmetry to predict θ12 or θ13 unless it adopts the trimaximal reading.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F403-oh-residual-symmetry-pmns-no-go.md` | Class-by-class fixed columns in both frames; gCP classification; data verdicts | exact (group, columns, gCP) + quantitative (data box) |
| record `F403-oh-residual-pmns` → `test-results/F403_oh_residual_pmns.json` | 15/15 legs incl. subgroup lattice S1–S4; controls `frame=trimaximal` (N1, S2 red) and `theta13_lo_deg=0` (N1, N2, B2, B4, S2–S4 red) verified | exact / quantitative |
| `findings/F254-t2g-pmns-selector-nogo.md` (CL223) | The $T_{2g}$ mixing amplitudes are free under $D_{2h}$ — this card strengthens that to "no $O_h$ residual fixes them" | exact |

## Falsifier

The no-go half is a theorem given its inputs, so it falls only if an input falls: (i) a measurement consistent with $\theta_{13}=0$ (already excluded at >30σ), (ii) the model abandoning the cube-axis charged-lepton frame, or (iii) a charged-lepton rotation of order $\theta_{13}\approx0.15$ rad appearing in the model, which would evade it (the standard charged-lepton-correction rescue). The TM1 half is observational: if the trimaximal reading is adopted, a JUNO measurement placing $\sin^2\theta_{12}$ outside $[0.3170,0.3195]$ at >3σ kills it (JUNO's projected precision is about ±0.003), and so does $\delta_{CP}$ measured outside $[252.4°,293.4°]$ at >3σ (DUNE/Hyper-K). The μ–τ reflection option dies if $\theta_{23}=45°$ or $\delta=270°$ is excluded at 3σ.

## Status & history

2026-09-24 - 15:20: TM1 half narrowed by F406 / CL317. This card's trimaximal-frame check left the charged-lepton row assignment free. A fixed Koide circulant pins it, and there are three inequivalent circulants (τ, e, μ on $(1,1,1)$). TM1 needs the e-branch ($\arg b=\tfrac29+\tfrac{2\pi}3$), which is not the branch carrying δ* as the [111] axial/polar ratio and is never a quadratic-order crystal-field ground state. The cube-frame no-go is unchanged.

2026-09-24 - 14:16: extended from element-wise to an explicit enumeration of all 98 $O_h$ subgroups, plus the face-diagonal and BCC frame check (F403 addendum). The claim's scope widens (cube and face-diagonal frames); its status is unchanged.


`open`, first issued 2026-09-24 with F403. Narrowed the same day by the independent review (CONFIRMED-NARROWER): the exactness class was lowered from exact to quantitative, the C₃ exclusion reason was corrected (upper edge of θ13, not the zero-entry bound), and the no-go was made explicitly conditional on an exactly cube-diagonal charged-lepton frame. The no-go is exact; the trimaximal alternative is recorded as a group-theory opening only and is **not** adopted, because it would reopen key decision 7 (the E_g-plane reading of δ*=2/9) and F93's uniqueness of E_g as the non-mixing splitter.

## Sources

- Prior art for the group theory: Lam arXiv:0809.1185; Hernandez–Smirnov arXiv:1204.0445, arXiv:1212.2149; Feruglio–Hagedorn–Ziegler arXiv:1211.5560 (S4 + generalised CP); King–Luhn arXiv:1301.1340

- `findings/F403-oh-residual-symmetry-pmns-no-go.md`
- `reports/Quark neutrino hierarchy lattice fit.md` (2026-09-24), §"Residual-symmetry mismatch"
- NuFIT 6.0, arXiv:2410.05380; NuFIT 6.1 + JUNO, arXiv:2601.09791
