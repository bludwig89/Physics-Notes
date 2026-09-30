---
id: CL317
title: 'The charged-lepton frame is the E_g-diagonal one provided the off-diagonal crystal field is stiff (as F118 read per axis gives); the [111]-circulant reading splits into three inequivalent vacua, and the one giving TM1 is not the one carrying delta* = 2/9 as the axial/polar ratio, so the model does not predict TM1'
slug: 'lepton-frame-fork-trimaximal-reading-splits'
tier: supporting
kind: no_go
status: open
domain: [SM]
exactness: quantitative
findings: [F406]
tests: [F406-lepton-frame-fork]
modules: [casim.engine.particles.derive_lepton_frame_fork]
constants: [delta_star]
supersessions: []
reviews: [docs/reviews/F406-review-2026-09-24.md]
rolls_up_to: CL223
falsifier: stated
first_issued: '2026-09-24'
last_verified: '2026-09-24'
provenance: authored
review_state: authored
confidence: medium
---

# CL317 — The lepton frame fork: the trimaximal reading splits, and the model does not predict TM1

## Statement

The Koide charged-lepton spectrum at $\delta^*=\tfrac29$ has an $E_g$-diagonal realisation (cube-axis eigenstates, residual $D_{2h}$) and Hermitian [111]-circulant realisations (trimaximal eigenstates, residual $C_3$). (i) The derived 3-generation BCC Dirac sea, and the F118 Landau functional read spectrally, are exactly degenerate over every orientation of the spectrum. F118 read per axis (its own E_g-channel identification of $\kappa_E$, $c$ and the clock) favours the $E_g$-diagonal frame: $E(b)-E(a)=+0.27$, with off-diagonal stiffness $\alpha=\beta=-\kappa_E=2.16>0$. (ii) There are three $O_h\times T$-inequivalent circulants, $\arg b=\tfrac29+2\pi j/3$, with τ, e and μ respectively on the $C_3$-invariant direction $(1,1,1)$. TM1 ($\lvert U_{e1}\rvert^2=\tfrac23$) arises only on $j=1$, whose [111] axial/polar angle is $\pi/3-\tfrac29$. The reading "δ* is $\arctan(T_{1g}/T_{2g})$" holds only on $j=0$, where no $O$ residual is viable once the JUNO $\sin^2\theta_{12}$ band is used. (iii) At quadratic crystal-field order ($\alpha R+\beta I$) neither of those two circulants is ever the unique ground state, and the $E_g$-diagonal frame is the ground state iff $\alpha,\beta>0$. That is one of four regions, not the generic case. The model's charged-lepton frame is therefore the $E_g$ one **provided $\alpha,\beta>0$**, which F118's per-axis reading supplies but no first-principles calculation yet does (decision 7 stands on that basis). TM1 with $\sin^2\theta_{12}=0.318$ is not a model prediction.

## What it extends

The residual-symmetry approach to lepton mixing in the Standard Model extended by an $S_4$ flavour symmetry, where TM1 arises from a trimaximal charged-lepton frame plus a $C_2$ neutrino residual (Lam arXiv:0809.1185; King arXiv:1512.07531). The claim closes the one route by which the model's lattice group could have fixed PMNS, narrowing CL315's TM1 opening from "the trimaximal frame admits TM1" to "the trimaximal vacuum that gives TM1 is not the model's".

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F406-lepton-frame-fork-energetics.md` | Exact tie (K1, K2); three branches and their lepton on (1,1,1) (K3); TM1 only on b2 (K4); axial/polar angles (K5); Michel criticality (K6); crystal-field kernel 2 / 6 (K7); exact quadratic phase diagram (K8); cubic indicative (K9) | exact / machine / quantitative |
| record `F406-lepton-frame-fork` → `test-results/F406_lepton_frame_fork.json` | 10/10 legs; controls `sea_generation_blind=false` (K2, V red) and `s12sq_band=nufit60` (K4, V red) verified | quantitative |
| `findings/F403-oh-residual-symmetry-pmns-no-go.md` (CL315) | The TM1 opening this narrows (row assignment free there, fixed here) | exact + quantitative |

## Falsifier

(i) A first-principles off-diagonal crystal-field stiffness with $\alpha\le0$ or $\beta\le0$ (any of the three non-$E_g$ regions). That overturns "the frame is $E_g$"; $\beta<\alpha<0$ in particular gives the μ-on-$(1,1,1)$ circulant. A derived cubic crystal field that selects $j=1$ would reopen TM1. (ii) Observationally, the card is a non-prediction of TM1. If JUNO measures $\sin^2\theta_{12}\in[0.3170,0.3195]$ **and** DUNE/Hyper-K measure $\delta_{CP}\in[252°,293°]$ with θ23 on the TM1 correlation, the model's missing TM1 becomes a failure to explain, and the $j=1$ vacuum would have to be derived. (iii) A lattice mechanism that makes the Dirac sea generation-non-blind (the K2 control) would break the exact tie and could decide the fork differently.

## Status & history

2026-09-24 - 15:20: `open`, first issued with F406, answering next-derivation #2 of the 2026-09-24 flavour report and F403's open step (i).

2026-09-24 - 15:40: narrowed by the independent review (CONFIRMED-NARROWER). "F118 cannot choose" is corrected: that holds only for the spectral reading; the per-axis reading chooses $E_g$. The frame claim is made conditional on $\alpha,\beta>0$, and the falsifier widened to any derived $\alpha\le0$ or $\beta\le0$.

## Sources

- `findings/F406-lepton-frame-fork-energetics.md`; `findings/F403-oh-residual-symmetry-pmns-no-go.md`; `findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md`
- `reports/Quark neutrino hierarchy lattice fit.md` (2026-09-24), §"Residual-symmetry mismatch"
- NuFIT 6.0, arXiv:2410.05380; NuFIT 6.1 + JUNO, arXiv:2601.09791; L. Michel, Rev. Mod. Phys. 52 (1980) 617
