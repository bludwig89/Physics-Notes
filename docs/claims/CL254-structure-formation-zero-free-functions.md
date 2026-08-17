---
id: CL254
title: The model's gravity law fixes linear structure formation with zero free functions where the EFT of dark energy has two, giving mu = Sigma = 1 with no scale or time dependence, the growth index 6/11 exactly, and no screening mechanism with which to relieve the S8 tension
slug: structure-formation-zero-free-functions
tier: headline
kind: derivation
status: live
domain: [cosmology, GR]
exactness: exact
findings: [F288]
tests: [F288-structure-formation-growth]
modules: [casim.engine.interactions.cosmology_growth]
constants: [a_over_ellP]
supersessions: []
reviews: []
rolls_up_to: CL008
falsifier: stated
first_issued: 2026-08-05
last_verified: 2026-08-05
provenance: authored
review_state: authored
confidence: high
---

# CL254 — Linear growth has zero free functions, and therefore no dial for S8

## Statement

In the linear, sub-horizon, quasi-static regime the model's gravity law fixes both functions of the
standard modified-gravity parametrisation to unity — $\mu(a,k)\equiv1$ and $\Sigma(a,k)\equiv1$ —
with no scale dependence and no time dependence, from three structurally independent sources:
$\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ collapsing to Poisson with coefficient exactly $4\pi G$ and
$\partial\mu/\partial k\equiv0$ (F106/F178); $G$ structural on a rigid substrate so
$\dot G/G\equiv0$ exactly (F79/F284); and the impedance match $AB\equiv1$ forcing the linear-order
gravitational slip coefficient to a **literal zero** (F64 D-EM9). Consequently the growth index is
$\gamma_g=6/11$ **exactly**, the radiation-era Meszáros solution is $D(y)=1+\tfrac32y$ with a
literal-zero residual, and — because $\mu=1$ is $k$-independent by derivation — **the model has no
screening mechanism and therefore no way to lower late-time growth relative to the CMB prediction.**

$\sigma_8$ is **not** claimed. It is linear in $\sqrt{A_s}$ and $A_s$ is a free initial condition
(CL-level: K5 `EXCLUDED`). Reported: $\sigma_8=0.8204$, $S_8=0.8410$, $+1.15\%$ against Planck's
$0.8111$, with $A_s$, $n_s$, the Eisenstein–Hu 1998 no-wiggle $T(k)$ and $\sum m_\nu$ all declared
as imports.

## What it extends

**General relativity, in the one place a gravity theory can differ from GR without differing in the
background.** The effective field theory of dark energy carries two free functions of $(a,k)$;
every modified-gravity constraint in the $S_8$ literature is a bound on them. This claim asserts the
model has zero, from three named and independently derived structural facts, and is therefore
**more constrained than GR-as-an-EFT in this sector**. It also asserts the model reproduces the
standard results — the $\gamma_g=6/11$ growth index, the Meszáros stagnation, the ΛCDM $f\sigma_8$
history — which is a *consistency* result and is labelled as one.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F288-structure-formation-zero-free-functions.md` | 13/13 checks; the full argument | mixed |
| S1 (`slip_from_impedance_match`) | $AB\equiv1\Rightarrow$ linear slip coefficient is sympy `0`; $\eta-1=2\Phi\approx2\times10^{-5}$ | exact |
| S2 (`mu_from_f106_poisson`) | $\mu=1$ and $\partial_k\mu=0$, both sympy `0` | exact |
| D1 (`growth_index_exact`) | $\gamma_g=6/11$; and $c=1$ iff $\mu=1$ | exact |
| D2 (`meszaros_exact`) | $D(y)=1+\tfrac32y$, residual literal `0`, both modes | exact |
| D3a | $D(1)$ vs Carroll–Press–Turner $+0.10\%$; radiation-convention sensitivity $3.8\times10^{-5}$ | quantitative |
| D3b | $f\sigma_8$ vs 7 RSD points (DESI DR1 PV, BOSS DR12, eBOSS DR16), $\chi^2/N=1.012$ **diagonal only** | quantitative |
| D5 | $\mu\in[0.986,1.008]$ at 1σ — the structural claim is *tested* at 1.1%, not merely asserted | quantitative |
| B1 | Lattice discreteness $\le1.3\times10^{-112}$ even at the Lyman-α scale | bound |
| C1 (`control_goes_red`) | $\mu=0.90$ turns three legs red; $\sigma_8$ moves $-32.0\%$, $\Delta\chi^2=+86.0$ | control |

Registry record `F288-structure-formation-growth` (gate tier, `entry: run`); artifact
`test-results/F288_structure_formation.json`. Sweep:
`casim test --id F288-structure-formation-growth --param mu=0.90` returns `pass=False`.

## Falsifier

**Stated, and it can fire today.** The model predicts the combined-CMB $S_8$ propagated forward by
GR growth, with nothing to tune. Against the 2026 landscape:

| Probe | $S_8$ | vs model ($0.8410$) |
|---|---|---|
| Combined CMB (Planck18+ACT DR6+SPT-3G) | $0.836^{+0.012}_{-0.013}$ | $0.29\sigma$ |
| KiDS-Legacy 2025 | $0.815^{+0.016}_{-0.021}$ | $1.17\sigma$ |
| **DES Y6 $3\times2$pt** | $0.789\pm0.012$ | **$3.00\sigma$** |

> **If the DES Y6 direction consolidates as physical rather than as photo-$z$ or baryonic-feedback
> systematics, this claim is dead and the model's gravity sector with it.** The usual escape —
> modified gravity confined to nonlinear scales by screening, which evades linear-scale bounds — is
> unavailable, because $\mu=1$ is $k$-independent by derivation rather than by choice. There is no
> parameter to move.

Secondary thresholds, each independently sufficient: a measured $|\mu-1|>0.011$ (1σ, D5); a
detected linear-order gravitational slip $|\eta-1|\gg2\times10^{-5}$; a measured $\dot G/G\neq0$
(which kills the time-independence leg via CL-level F284); or a measured
$\gamma_g$ inconsistent with $6/11$ in the $\Omega_m\to1$ limit.

## Status & history

`live`, first issued 2026-08-05. Attacks `docs/status/completeness-2026-08-04.md` row **K11**,
graded `ABSENT` on four separate keyword sweeps — one of only two cosmology rows with no entry point
at all. The row should move `ABSENT → PARTIAL`.

**Deliberately narrower than it could have been written.** Three restrictions are load-bearing and
must survive any future edit of this card:

1. **$\sigma_8$ is reported, never claimed.** It is linear in $\sqrt{A_s}$ and $A_s$ is provably
   free (F282/F284/F285, K5 `EXCLUDED`). The $\approx1\%$ residual after the neutrino correction is
   the imported EH98 no-wiggle fit, not a model residual.
2. **Zero slip is a statement about the gravity sector only.** Free-streaming neutrinos carry
   genuine anisotropic stress and source the usual GR slip in the radiation era; the lattice removes
   the gravitational dial, not the matter source (F173).
3. **The regime is named.** F178 demoted F106's energy-only law to the static weak-field reduction,
   which is exactly the quasi-static sub-horizon regime linear CDM growth needs. It is **not** valid
   super-horizon or for relativistic radiation-era modes.

**What this does not claim.** It does not settle the dark-matter identity: $\sigma_8$ is blind to
the difference between the Planck-mass geon remnant and the F266 5.6 keV sterile at the
$2.7\times10^{-6}$ level, because the sterile's half-mode ($45.9\,h\,$Mpc$^{-1}$) sits ~2.6 decades
above the $\sigma_8$ scale. The probe that is not blind is the Lyman-α forest, where F203's
9–15 keV floor already applies. K11 redirects K7; it does not close it.

## Sources

- `findings/F288-structure-formation-zero-free-functions.md`
- `docs/roadmaps/k11-structure-formation-prompt.md`
- `docs/status/completeness-2026-08-04.md` (row K11, ABSENT table)
- `src/casim/engine/interactions/cosmology_growth.py`
- Planck Collaboration 2020 (Planck 2018 VI); Alam et al. 2021 (eBOSS DR16); DESI DR1
  peculiar-velocity survey 2025; Abbott et al. 2026 (DES Y6 + combined CMB); KiDS-Legacy 2025;
  *Status of the $S_8$ Tension: A 2026 Review of Probe Discrepancies*; Eisenstein & Hu 1998;
  Viel et al. 2005; Carroll, Press & Turner 1992
