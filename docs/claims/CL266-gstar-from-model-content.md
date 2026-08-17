---
id: CL266
title: 'The relativistic degree-of-freedom count is derived from the model''s own content, not imported: it reproduces g_* = 10.75 through the BBN window, and above the top threshold it differs from the Standard Model by exactly one degree of freedom in either direction, so 106.75 is unavailable to it'
slug: gstar-from-model-content
tier: supporting
kind: derivation
status: live
domain: [SM, cosmology]
exactness: quantitative
findings: [F309, F297, F47, F165, F279, F121]
tests: [F309-gstar-model-content]
modules: [casim.engine.interactions.thermodynamics_gstar, casim.engine.interactions.cosmology_bbn]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-11
last_verified: 2026-08-11
provenance: authored
review_state: authored
confidence: high
---

# CL266 — $g_*(T)$ from the model's own field content

## Statement

The model's relativistic content — 48 Weyl fields in 24 left-handed and 24 right-handed
(F47/F165/F279), 12 gauge bosons, and 2 real $E_g$ scalars in place of the Standard Model's
Higgs doublet (founding decision 3, F253/F255) — determines $g_*(T)$ and $g_{*s}(T)$ with no
imported degree-of-freedom count. Three assertions:

1. **Through the BBN window the derived content is exactly $\{\gamma,\ e^\pm,\ 3\nu_L\}$**, so
   $g_*(10\ \text{MeV})=10.749339$ against $10.75$ and, on the $T_\nu/T_\gamma$ that entropy
   conservation produces rather than imposes, $g_*\to3.362971$ against
   $2+\tfrac{21}{4}(4/11)^{4/3}=3.362644$ and $g_{*s}\to3.909435$ against
   $2+\tfrac{21}{4}(4/11)=3.909091$. Every exclusion carries a model reason, and two carry
   numbers: thermalising $\nu_R$ would add $\Delta g_*=+5.25$ (48.8 %), and the muon residual
   at 10 MeV is $9.2\times10^{-4}$ of $g_*$.
2. **The $E_g$ doublet's exclusion is a bound, not an assumption.** Its mass is not derived
   anywhere in the tree, so BBN supplies one: $m_{E_g}>125.5$ MeV for $\Delta g_*<10^{-3}$ at
   $T=10$ MeV.
3. **Above the top threshold the model's $g_*$ is $105.75$ if the $E_g$ modes are heavy and
   $107.75$ if they are light. The Standard Model's $106.75$ is not available to it** — the
   SM's single physical Higgs scalar is traded for the $E_g$ doublet's two real components, so
   the difference is exactly one degree of freedom, in a direction fixed by $m_{E_g}$.

Re-running F297's BBN on the model's own electron mass ($m_e=0.51069$ MeV, F121) rather than
the PDG value shifts $Y_p$ by $+1.080\times10^{-4}$ ($+0.032\sigma$) and D/H by
$+1.057\times10^{-4}$ relative ($+0.009\sigma$), both toward the observations.

## What it extends

Every standard BBN and thermal-history calculation takes $g_*(T)$ from the Standard Model's
particle table as an input. Here the table is an *output* of the model's own field content,
and the two agree through the BBN window only after four model-specific exclusions —
$\nu_R$ (total singlet, $Y=0$ forced, plus a heavy Majorana mass), the $E_g$ doublet (the
model is Higgs-free), the hadronic sector (Boltzmann-suppressed), and the dark sector (a
Planck-mass geon remnant). Above the electroweak scale the agreement ends, and the model makes
a content-level prediction the Standard Model contradicts by exactly one degree of freedom.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F309-gstar-from-model-content.md` §4 | the 48-Weyl content, branch balance exactly zero, and every exclusion with its reason | exact count |
| `findings/F309-gstar-from-model-content.md` §4 | the exclusion prices: $\nu_R$ $+5.25$, muon $9.2\times10^{-4}$, $m_{E_g}>125.5$ MeV | quantitative |
| `findings/F309-gstar-from-model-content.md` §5 | the $g_*$/$g_{*s}$ table on the emergent $T_\nu/T_\gamma$ | quantitative, $10^{-4}$ |
| `findings/F309-gstar-from-model-content.md` §5.1 | the $m_e$ substitution and the $Y_p$/D/H shift | quantitative |
| `findings/F309-gstar-from-model-content.md` §5.2 | the plateau table and the one-degree-of-freedom difference | exact count |
| record `F309-gstar-model-content` (gate) | GS-1, GS-8, GS-9, GS-10, GS-12, GS-13 | — |
| `test-results/F309_gstar_model_content.json` | the artifact | — |

## Falsifier

**Computational and observational, both with thresholds.**

*Computational, and it fires every gate run.* $g_*(10\ \text{MeV})$ departing from $10.75$ by
more than $10^{-3}$ relative, or $g_{*s}$ missing the $2+\tfrac{21}{4}(4/11)$ endpoint by more
than $10^{-3}$, kills assertion 1 — records GS-8 and GS-9. The declared control
`sm_content_control=True` thermalises $\nu_R$ and reddens both, which is what proves those
checks measure *content* rather than restating a textbook number.

*Observational, assertion 1.* Any measurement establishing $\Delta N_\text{eff}\ge1$ at BBN
falsifies the $\nu_R$ exclusion and therefore the derived content; F297 already records that
$\nu_R$ thermalisation would give $\Delta N_\text{eff}=1.71$, excluded by Planck at more than
$10\sigma$.

*Observational, assertion 2.* A measurement of any $E_g$-sector state below 125.5 MeV would
put the BBN $g_*$ out of range and falsify either the bound or the Higgs-free structure that
produces the doublet.

*Assertion 3 has no fireable observational falsifier today, and the card says so rather than
inventing a threshold.* The observable that carries $g_*$ at that epoch is the primordial
gravitational-wave background, $\Omega_\text{GW}\propto g_*g_{*s}^{-4/3}$, and a one-degree-
of-freedom shift moves it by $0.31\,\%$ — below any current or planned sensitivity. It is
recorded as a labelled prediction, not published as a falsifier (F300's discipline; the
2026-08-04 report had to strike F282's falsifier 5 for exactly this).

*The $m_e$ substitution is likewise not a test at present precision.* Seeing it requires
$\sigma(Y_p)\lesssim1.08\times10^{-4}$, a $31\times$ improvement on Aver et al. 2021, and that
number is quoted so nobody has to guess.

## Status & history

`live` as stated. Three scope boundaries, each of which a later citation is likely to blur:

* **One import closed, not the ledger.** $\eta_{10}$, $V_{ud}$, $G_F$ and the reaction network
  remain external (F297's input ledger, unchanged). K2 is not parameter-free.
* **Plateau boundaries above the QCD crossover are imported.** The plateau *values* follow from
  content, which is what the model supplies; $m_c$, $m_b$, $m_t$, $m_W$ and a crossover
  temperature are not derived in this tree and the card claims nothing about them.
* **$m_n-m_p$ is untouched.** F297's regression — the model's $+1.51$ MeV excluded at
  $36.6\sigma$ — is orthogonal to $g_*$, and both runs behind assertion 1 use the PDG
  $\Delta m$, exactly as F297's headline does. This card neither helps nor worsens it.

## Sources

- `findings/F309-gstar-from-model-content.md`
- `findings/F297-bbn-light-element-abundances.md` (the input this grades)
- `findings/F47-majorana-seesaw-higgs-free.md`, `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md`, `findings/F279-hypercharge-constraint-attribution.md` (the content, and the two reasons $\nu_R$ never thermalises)
- `findings/F121-tau-anchored-canonical-spectrum.md` (the model's own $m_e$)
- `findings/F253-weight-as-phase-scale-nogo.md` (the $E_g$ doublet that replaces the Higgs)
- `docs/status/completeness-2026-08-07.md` §"gap #4"
