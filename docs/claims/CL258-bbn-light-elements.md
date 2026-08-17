---
id: CL258
title: 'The model reproduces the primordial light elements on a structurally derived G with a zero-freedom N_eff, and BBN independently excludes the demoted energy-only gravitational law at 17.6 sigma'
slug: bbn-light-elements
tier: supporting
kind: derivation
status: contingent
domain: [cosmology, GR, SM]
exactness: quantitative
findings: [F297, F178, F182, F284, F79, F202]
tests: [F297-bbn-light-elements]
modules: [src/casim/engine/interactions/cosmology_bbn.py]
constants: [G_CODATA, g_A]
supersessions: []
reviews: []
rolls_up_to: CL008
falsifier: stated
first_issued: '2026-08-05'
last_verified: '2026-08-05'
provenance: authored
review_state: authored
confidence: medium
---

# CL258 — Primordial nucleosynthesis on the model's own expansion law

## Statement

Run at the Planck baryon-to-photon ratio $\eta_{10}=6.137$, with the Hubble rate set by the model's
**structurally derived** $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (F79/F107), the **adopted full-tensor
source law** (F178), $\dot G/G$ **identically zero** (F284), and $N_\text{eff}=3.044$ **forced by
the model's own particle content**, the model produces $Y_p=0.2449$ and
$\mathrm{D/H}=2.47\times10^{-5}$ — within $0.11\sigma$ of Aver et al. 2021 and $1.8\sigma$ of
Cooke et al. 2018.

The **demoted energy-only law** (F106), read as a dynamical law, expands at
$S=\sqrt{\kappa/2}=1/\sqrt2$ of that rate at fixed temperature and gives $Y_p=0.1856$ —
$-17.6\sigma$.

## What it extends

Standard BBN takes $G$, $N_\text{eff}$ and $m_n-m_p$ as measured inputs. Here $G$ is derived with
zero free parameters, $N_\text{eff}=3.044$ is forced (there is no light degree of freedom the model
could add: $\nu_R$ is a total singlet with $Y=0$ by F165/F279 and carries the heavy see-saw mass by
F47, the model is Higgs-free so there is no light scalar, and the dark candidate is a Planck-mass
geon), and the constancy of $G$ is structural rather than a bound that happens to be met.

It also supplies an **independent** test of the F178 adoption. That decision was made on Lorentz
covariance and the neutron-star maximum mass (F174/F176); BBN sits three decades of redshift away
and tests it on an unrelated observable, and agrees.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F297-bbn-light-element-abundances.md` | the full derivation and the 12-check battery | quantitative |
| `tests/registry/interactions.yaml` → `F297-bbn-light-elements` | gate-tier record, 12/12 PASS, two declared red controls | quantitative |
| `test-results/F297_bbn_light_elements.json` | the numbers | quantitative |
| `src/casim/engine/interactions/cosmology_bbn.py` | `validate_network()` measures the network's own offset against published reference values | quantitative |

## Falsifier

Three, each with a threshold:

1. **$N_\text{eff}$.** The claim admits no freedom in the relativistic budget. A measured
   $N_\text{eff}$ differing from 3.044 by more than $\pm0.35$ ($2\sigma$ of Planck) kills it; there
   is no dial to turn, because any thermalised $\nu_R$ would add $\Delta N_\text{eff}=1.71$, not a
   tunable fraction.
2. **$Y_p$ at fixed $\eta_b$.** With $\eta_{10}$ pinned by the CMB, a primordial helium mass
   fraction outside $0.2453\pm0.0034$ by more than the network's measured $0.9\%$ offset plus
   $2\sigma$ falsifies the expansion side.
3. **The law control is itself the falsifier for the alternative.** If the energy-only reading were
   ever readopted, $Y_p=0.1856$ is what it must produce.

## Status & history

`contingent`, and the condition is named: **$\eta_b$ is an external input.** F202 leaves its magnitude
free and inherited -- the Sakharov conditions are met structurally but no asymmetry number is
derived (rubric K6), so this is a consistency test at
fixed $\eta$ — exactly what standard BBN is, and no stronger.

Three further limits are on the card deliberately rather than in a footnote:

- The network carries a **measured $\sim0.9\%$ absolute offset** against published reference values.
  Every model-level conclusion is stated as a *difference computed inside the same network*, so the
  offset cancels; the absolute abundances quoted above carry it.
- **No lithium claim is made.** The $A=7$ chain in this implementation is $92\%$ low against the same
  reference, so four of the twelve rate fits are wrong or incomplete. Li7 is returned by the module
  and excluded from the battery, and the standing lithium problem is untouched in either direction.
- The energy-only exclusion is **conditional on a reading**. F182 A1 showed that law is internally
  inconsistent for $p\ne0$, so evaluating it requires choosing which equation survives; this control
  keeps the dynamical equation. Under the other reading the expansion history is identical and BBN
  says nothing. It is a strong exclusion of one reading, not a proof covering both.
- **$B_d$ is invisible here.** The model's deuteron binding differs from the measured value by
  $0.026\%$ and moves D/H by $0.078\sigma$. BBN does *not* confirm the derived deuteron binding, and
  this card does not say it does.

Rolls up to CL008 (gravity sourced by the full stress-energy tensor), which this is a second and
independent observational leg of.

## Sources

- `findings/F297-bbn-light-element-abundances.md`
- `findings/F178-gravity-full-tensor-adoption.md`, `findings/F182-friedmann-pressure-cosmology.md`
- `findings/F284-rigid-lattice-expansion-and-primordial-state.md`, `findings/F202-leptogenesis-from-intrinsic-L-violation.md`
- `docs/status/completeness-2026-08-04.md` — rubric row K2
- Aver et al. 2021 JCAP 03, 027; Cooke, Pettini & Steidel 2018 ApJ 855, 102; Planck 2018 VI;
  Smith, Kawano & Malaney 1993 ApJS 85, 219; Pitrou et al. 2018 (PRIMAT)
