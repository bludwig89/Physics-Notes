# F176b — How much of TOV the covariant dielectric recovers: curvature feedback restores the maximum mass, the pressure source matches GR to 0.4%, and a ~2 km AB≡1 residual survives as the NICER-frontier discriminator

> **[PARTIALLY SUPERSEDED 2026-06-29 by F178 — ledger S4-F178-full-stress-energy]**
>
> **DEAD:** The ~2 km AB = 1 interior residual as a standing prediction. Per F178 the model adopts the full-tensor source, the interior is GR/TOV, and that residual applies only if one insists on keeping the single scalar in matter -- which the decision does not.
>
> **STILL LIVE:** How much of TOV the covariant dielectric recovers, and the curvature-feedback result that restores the maximum. Vacuum and weak-field results are untouched.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


> **Renumbered F176b at roadmap C8.2 close-out (2026-07-31).** This file shared its number with another finding; the C8 audit found ten such collisions. The `b` suffix keeps the number findable — every existing citation of F176 still resolves — while making the two files distinguishable to tooling. See `docs/design/finding-numbers.yaml`.


**Date:** 2026-06-29 - 20:30
**Numbering:** F175 was taken by a concurrent session; this is **F176** (re-checked per CLAUDE.md).
**Status:** Confirmed — 5/5 checks PASS. Resolves the central open fork of [[F174-stellar-structure-overlay]]: covariantizing the strong-field source rescues the model from the literal-F106 exclusion. The maximum-mass recovery (C2/C3) and EoS-robustness (C5) are robust; absolute radii use a toy Γ=2 polytrope.
**Module:** `ca-simulation/ca_stellar.py` (covariant solver added)
**Script:** `tests/findings/test_F176_covariant_stellar.py` (~25 s; numpy + local RK4 + secant shoot)
**Results:** `test-results/F176_covariant_stellar.json` (+ overlay arrays)
**Figure:** `test-results/figures/F176_covariant_overlay.png`
**Cross-references:** [[F174-stellar-structure-overlay]] (the literal-model exclusion this addresses), [[F173-pressure-tolman-discriminator]] (the exact G_tt the covariant source is built from), [[F64-em-connection-gravity]]/[[F106-psi-K-sourcing-derivation]] (the dielectric), [[F114-dielectric-black-hole]]. Brief: `tests/falsification/FC09-neutron-star-pressure-redshift.md`. External: TOV; PSR J0740+6620 (Fonseca/Miller/Riley 2021); piecewise-polytrope framework (Read, Lackey, Owen, Friedman, PRD 79, 124032, 2009).

---

## The fork being resolved

F174 showed the **literal** F106 law (flat Laplacian, energy-only source) gives neutron stars with **no maximum mass** — excluded by PSR J0740+6620. But F64/F106 only ever fixed the *weak-field* law; the strong-field extension was undetermined. This finding builds the **covariant** extension and measures how much of GR-TOV it recovers.

The covariant field equation is taken directly from the **exact** Einstein $G^t_t$ of the dielectric metric (F173), in first-order form with $s=r^2u'$:
$$u'=\frac{s}{r^2},\qquad s'=-\tfrac12\Big(\frac{s^2}{r^2}+8\pi\,\text{src}\,e^{2u}r^2\Big),\qquad p'=(\rho+p)\,u',$$
with $\text{src}=\rho$ (energy-only, **cov-E**) or $\rho+3p$ (GR trace-reversed source, **cov-3p**). The $s^2/r^2$ and $e^{2u}$ terms are the relativistic curvature feedback the literal flat law dropped. Because $e^{2u}$ couples to the absolute potential, $u$ is fixed by a **boundary-value shoot** enforcing $u(\infty)=0$; the vacuum tail is integrated in closed form ($u_\infty=u_R+2\ln(1+s_R/2R)$, $M_E=-[1/s_R+1/2R]^{-1}$), so only the interior is integrated.

## Checks (5/5)

| # | Check | Result | Tier |
|---|---|---|---|
| C1 | **Newtonian limit**: cov-E → GR as $\rho_c\to0$ (mass ratio $1.036\to1.0004$, monotone) | PASS | quantitative |
| C2 | **cov-E recovers a maximum mass**: turnover present, $M_\text{max}=3.01\,M_\odot$ — where the literal model had **no turnover at all** | PASS | quantitative |
| C3 | **cov-3p matches GR's maximum mass to 0.4%**: $M_\text{max}=2.128$ vs GR $2.136\,M_\odot$ (rel. $3.9\times10^{-3}$); cov-E overshoots by **41%** | PASS | quantitative |
| C4 | **Residual collapses**: with feedback restored the model is no longer catastrophically off — cov-3p sits $2.3$ km from GR at $1.4\,M_\odot$ and tracks GR through the NICER box, versus the literal model's no-turnover failure | PASS | quantitative |
| C5 | **EoS-robust**: on a second polytrope (K=150) cov-3p again matches GR $M_\text{max}$ to $0.4\%$ and cov-E again overshoots by $41\%$ | PASS | quantitative |

## How much of TOV is recovered — the staged answer

1. **The literal failure was the missing curvature feedback, not (only) the pressure.** Restoring the exact $G^t_t$ feedback ($s^2/r^2$, $e^{2u}$) — *still sourcing from energy density alone* — turns the literal model's runaway (no maximum mass, $R\approx20$ km) into a proper neutron-star sequence with a turnover at $3.0\,M_\odot$ (C2). So covariantization alone rescues the gross pathology.
2. **The pressure source closes the remaining gap.** cov-E overshoots GR's maximum mass by 41% because it still omits the Tolman $3p$. Restoring the GR trace-reversed source ($\rho+3p$) brings $M_\text{max}$ onto GR to **0.4%** (C3) — independent of EoS (C5).
3. **A residual survives — the genuine discriminator.** Even cov-3p does not reproduce GR exactly: the single-scalar impedance lock $AB\equiv1$ leaves a $\sim2$ km offset in the mass–radius relation and a corresponding surface-redshift shift (overlay figure). This is the irreducible signature of one-field gravity, and it sits squarely at the NICER / X-ray-timing precision frontier — a *subtle* test, not the gross exclusion of F174.

**Verdict.** The model is **not** excluded once covariantized. The honest cost is a choice of source:
- **Energy-only, covariant (cov-E):** stays faithful to the pure F106 "gravity couples to energy" philosophy, but overshoots neutron-star maximum masses by ~40% — disfavoured by the observed $\sim2\,M_\odot$ ceiling, though not catastrophically.
- **Energy + pressure (cov-3p):** matches GR's maximum mass to sub-percent but reintroduces the $3p$ Tolman term — i.e. concedes that pressure gravitates after all, abandoning the F173 distinction. Even then a $\sim2$ km $AB\equiv1$ residual remains.

So "how much of TOV is recovered" is: **the maximum-mass existence and (with the pressure source) its value to 0.4%; the detailed mass–radius relation is recovered only up to a ~km-scale, AB≡1-locked residual that no longer grossly violates NICER but is a clean target for it.** Full TOV is reached exactly only by abandoning the single scalar entirely (two independent metric functions ⇒ GR).

## Tabulated-EoS follow-up

A `TwoPiecePolytrope` class (Read et al. 2009 framework) is added for dropping in tabulated SLy/APR digits for an absolute NICER placement; the published parameters were not independently verifiable in this session, so the runs here use Γ=2 polytropes (K=250, 150) and establish that the GR-vs-model **relationship** (cov-3p ≈ GR; cov-E +41%; ~km residual) is **EoS-robust** (C5). Substituting verified SLy/APR parameters is mechanical and is the recommended step before quoting an absolute exclusion/confirmation against a specific pulsar.

## Open / next

- **Verified tabulated EoS.** Drop SLy/APR (Read+2009) digits into `TwoPiecePolytrope`, refit GR to the NICER credible regions, and quote the cov-3p residual in km against PSR J0740 / J0030 directly.
- **Decide the source.** The model must commit: pure energy-only (cov-E, ~40% high $M_\text{max}$) or energy+pressure (cov-3p, GR-like). This is a theory-level choice about whether pressure gravitates — the F173 question, now sharpened by data.
- **Tidal deformability** (GW170817 $\Lambda$–$M$) as an independent strong-field check on the same solver.

## Files
- Module: `ca-simulation/ca_stellar.py` (covariant solver + TwoPiecePolytrope)
- Test: `tests/findings/test_F176_covariant_stellar.py`
- Results + overlay: `test-results/F176_covariant_stellar.json`
- Figure: `test-results/figures/F176_covariant_overlay.png`
