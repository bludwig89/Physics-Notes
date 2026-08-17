# F205 — The full Boltzmann (quantum-kinetic) computation of keV sterile-neutrino dark matter: momentum-resolved active→sterile production (non-resonant Dodelson-Widrow + resonant Shi-Fuller via a lepton asymmetry) + free-streaming→thermal-equivalent-mass mapping, built to narrow the order-of-magnitude F203 T1/T2 margins to computed numbers — DW is X-ray excluded by **2.55 dex**, the Lyman-α mass floor is **~41 keV (non-resonant) → ~9–15 keV (coldest resonant)**, and the model's 5.6–7.1 keV keV sterile sits below all of them, so the T1/T2 pressure is **confirmed and quantified, not removed**

**Date:** 2026-06-30 - 23:40
**Numbering:** **F205** (re-checked; F204 = Alcubierre exclusion).
**Status:** **Built and validated.** Momentum-resolved QKE production solved on a converged (ε,T) grid; abundance reproduces the Dodelson-Widrow benchmark to within the known ~factor-2 QCD normalisation; free-streaming → Viel thermal-equivalent mapping reproduces the cited ~41 keV combined bound. 8/8 validation checks PASS. Honest scope: absolute normalisation carries the standard QCD-epoch uncertainty (robust outputs are ratios); resonant pass uses fixed lepton number (no back-reaction depletion); no 3D hydro is run — linear free-streaming is matched to published simulated Lyman-α flux-power bounds, as scoped.
**Module:** `ca-simulation/forks/dm_fork_F205_sterile_qke_boltzmann.py` (numpy + stdlib, real arithmetic — no chiral transforms).
**Tests / results:** `tests/findings/test_F205_sterile_qke_boltzmann.py` → `test-results/F205_sterile_qke_boltzmann_test.json` (8/8); fork dump `test-results/F205_sterile_qke_boltzmann.json`.
**Cross-references:** [[F203-dark-sector-falsifiability-battery]] (the T1/T2 margins this narrows), [[F266-sterile-neutrino-dark-matter]] (the relic identity + the order-of-magnitude `dw_abundance` this replaces), [[F201-kev-sterile-from-eg-texture]] (the 5.6 keV texture landing tested against the floor), [[F202-leptogenesis-sakharov]] (the lepton asymmetry resonant production needs). External: Dodelson–Widrow 1994; Shi–Fuller 1999; Asaka–Laine–Shaposhnikov 2007 (production); Notzold–Raffelt 1988 (finite-T potential); Viel et al. 2005/2013 (Lyman-α thermal WDM bound); XRISM Collaboration 2025 (X-ray line limit); combined X-ray+Lyman-α ~41 keV floor.

---

## What this replaces

F203 flagged its keV-sterile tests (T1 abundance/X-ray, T2 warm-structure) as *order-of-magnitude parametrisations*. F200 used a one-line Dodelson-Widrow abundance fit and F203 T2 used a `0.3 Mpc (keV/m_s)` free-streaming estimate. This finding does the actual momentum-resolved Boltzmann computation and the free-streaming → thermal-equivalent-mass mapping, turning those into computed numbers with stated residual uncertainties.

## Method

Active ($\nu_a$) → sterile ($\nu_s$) conversion via in-medium oscillations damped by collisions. The momentum-resolved production rate (one generation, small vacuum angle) is

$$\frac{df_s}{dt}(p,T)=\tfrac14\,\Gamma_a\,\frac{(\Delta\sin2\theta)^2}{(\Delta\sin2\theta)^2+(\Delta\cos2\theta-V)^2+(\Gamma_a/2)^2}\,f_\text{eq},$$

with $\Delta=m_s^2/2p$, collision rate $\Gamma_a=d_a G_F^2 p T^4$, and the finite-$T$ potential $V=V_T+V_D$: the asymmetry-free thermal part $V_T=-b_a G_F^2 p T^4$ (Notzold–Raffelt) and the lepton-asymmetry part $V_D=\sqrt2\,G_F(2\zeta_3/\pi^2)T^3\,L$. $L=0$ is non-resonant Dodelson-Widrow; $L>0$ produces an MSW level crossing ($\Delta\cos2\theta=V$) that sweeps through momentum as $T$ drops — resonant Shi-Fuller production, more efficient and (at its sweet spot) colder. The comoving relic is accumulated entropy-normalised, $Y_s=n_s/s$ (which folds in the QCD-to-today $g_*$ dilution):

$$Y_s=\int_{T_\text{lo}}^{T_\text{hi}}\frac{45}{4\pi^4 g_{*s}(T)}\left[\int \varepsilon^2\,\tfrac14\Gamma_a\langle\sin^2 2\theta_M\rangle f_\text{eq}\,d\varepsilon\right]\frac{dT}{H(T)\,T},\qquad \Omega_s h^2=\frac{m_s\,s_0\,Y_s}{\rho_\text{crit}/h^2}.$$

$\Omega_s h^2$ is **exactly linear** in $\sin^2 2\theta$ at fixed $L$ here (the $(\Delta\sin2\theta)^2$ term is negligible in the denominator), verified to $<10^{-6}$ — so one reference run rescales to the $\Omega_\text{DM}$-matching mixing without bisection.

## Results — the narrowed margins

### 1. Non-resonant (Dodelson-Widrow) abundance and X-ray exclusion
For 100% DM at $m_s=7.1$ keV the computation needs

$$\sin^2 2\theta_\text{DW}=6.1\times10^{-9},$$

reproducing the literature $\sim3$–$4\times10^{-9}$ to within the known factor-2 QCD normalisation. Against the aggregate current X-ray bound ($\sim1.7\times10^{-11}$ at 7.1 keV) this is **2.55 dex above** → **non-resonant DM is X-ray excluded** — F203 T1's "order-of-magnitude" statement is now a 2.55-dex number.

### 2. Resonant (Shi-Fuller) enhancement
A lepton asymmetry drives resonant production **up to ~580× more efficient** than DW, reaching $\Omega_\text{DM}$ at $\sin^2 2\theta$ that **clears the aggregate X-ray bound for $L\gtrsim2\times10^{-3}$** (this code's asymmetry convention). So resonant production is the X-ray-viable channel — quantified.

### 3. The 7.1 keV edge tension (the honest new result)
The frozen spectrum's mean momentum $\langle\varepsilon\rangle$ (grid-converged to $<0.1\%$) depends on $L$: a cold sweet spot at $L\approx2\times10^{-4}$ gives $\langle\varepsilon\rangle=1.57$ (vs the DW $3.29$, a factor $0.48$), but **that $L$ requires X-ray-excluded mixing** to reach $\Omega_\text{DM}$, while the X-ray-*allowed* larger-$L$ points are **warm** ($\langle\varepsilon\rangle\approx3.0$). In the fixed-$L$ pass the cold-spectrum and X-ray-allowed regimes **do not coincide** — precisely the known "7.1 keV sterile at the X-ray/Lyman-α edge."

### 4. Free-streaming → Lyman-α mass floor
Mapping $\langle\varepsilon\rangle$ to a thermal-equivalent WDM mass (Viel relation) and onto the simulated Lyman-α thermal bound:

| spectrum | $\langle\varepsilon\rangle$ | Lyman-α mass floor on $m_s$ |
|---|---|---|
| non-resonant (DW) | 3.29 | **~41 keV** (reproduces the cited combined bound) |
| X-ray-allowed resonant (warm) | ~3.0 | ~37 keV |
| coldest resonant (Viel 5.3 keV bound) | 1.57 | **~15 keV** |
| coldest resonant (conservative 3.5 keV bound) | 1.57 | **~9 keV** |

The model's **5.6 keV** (F201) and the **7.1 keV** benchmark sit **below every one of these floors**. So the keV sterile is under **quantified** pressure as 100% dark matter — viable only as a sub-dominant component, or if the full lepton-number-depletion QKE threads the cold + X-ray-allowed corner that the fixed-$L$ pass cannot.

## What is computed vs anchored vs out-of-scope

| Piece | Status |
|---|---|
| momentum-resolved production $\Omega_s h^2(m_s,\sin^2 2\theta,L)$ | **Computed** (converged QKE quadrature) |
| $\Omega$ linear in $\sin^2 2\theta$ (rescale valid) | **Verified** ($<10^{-6}$) |
| DW $\sin^2 2\theta=6.1\times10^{-9}$ for $\Omega_\text{DM}$ | **Computed**, matches literature within factor ~2 |
| DW X-ray exclusion = 2.55 dex | **Computed** |
| resonant enhancement ~580×, X-ray-clearing $L$ | **Computed** (fixed-$L$) |
| frozen-spectrum $\langle\varepsilon\rangle$, grid-converged | **Computed** |
| non-resonant Lyman-α floor ~41 keV | **Anchored** (Viel mapping calibrated to the cited combined bound) |
| coldest-resonant floor 9–15 keV | **Computed** from $\langle\varepsilon\rangle$, given the Viel bound |
| absolute production normalisation | **±factor ~2** (QCD-epoch $g_*$; standard) |
| single $(L,\sin^2 2\theta)$ threading cold + X-ray-allowed | **Out of scope** (needs L-depletion QKE, sterile-dm-class) |
| 3D hydrodynamic Lyman-α flux-power | **Out of scope** (matched to published sims, as scoped) |

## Caveats (honest scope)

- **Normalisation.** The absolute DW/resonant amplitude carries the well-known ~factor-2 QCD-epoch $g_*(T)$ / hadronic-scattering uncertainty. The robust outputs are ratios (X-ray-exclusion dex, coldness, floor), and the DW anchor sits within the literature band.
- **Fixed lepton number.** The resonant pass holds $L$ constant (no back-reaction depletion). It captures the resonant enhancement and the *existence* of cold spectra, but the cold↔X-ray-excluded anti-correlation is likely sharper than in the self-regulating full QKE; whether a single $(L,\sin^2 2\theta)$ threads both X-ray and Lyman-α needs a depletion-tracking code. This is the one place the "edge" could soften.
- **No hydro.** As scoped with the user: no 3D N-body+hydro Lyman-α simulation is run; the linear free-streaming $\langle\varepsilon\rangle$ is matched onto published simulated flux-power bounds (Viel 2005/2013) — the standard field methodology.

## Consequence for F203 / the overview

F203 T1 and T2 are updated from *order-of-magnitude* to *computed*: DW X-ray exclusion is **2.55 dex** (not "~order of magnitude"), and the warm-structure floor is a **~41 keV non-resonant / ~9–15 keV coldest-resonant** number against a 5.6 keV model. The status of both stays **under_pressure** — the narrowing *confirms* the pressure rather than relieving it. The single remaining softener is the full L-depletion QKE (the F202 lepton-asymmetry sector), now the sharp next step for the dark-matter half.

## Test summary

| Check | Statement | Result |
|---|---|---|
| V1 | $\Omega$ linear in $\sin^2 2\theta$ (doubling → ×2 to $<10^{-3}$) | PASS |
| V2 | DW $\sin^2 2\theta$ for $\Omega_\text{DM}$ in literature band [2e-9, 1.2e-8] | PASS |
| V3 | DW X-ray excluded by $>2$ dex (2.55) | PASS |
| V4 | resonant enhancement $>100×$ (~580); clears X-ray bound for scanned $L$ | PASS |
| V5 | non-resonant Lyman-α floor reproduces cited ~41 keV (35–48) | PASS |
| V6 | coldest resonant spectrum $\langle\varepsilon\rangle$ ratio $<0.7$ (0.48); relaxes floor | PASS |
| V7 | 5.6/7.1 keV below the coldest+conservative floor → pressure confirmed | PASS |
| V8 | $\langle\varepsilon\rangle$ converged under grid refinement ($<1\%$) | PASS |

**Overall 8/8 PASS** (~1 s, numpy + stdlib, real arithmetic — no chiral transforms).

## Relation to other findings

Narrows the **F203** T1/T2 dark-matter margins from order-of-magnitude to computed, replacing the **F200** one-line abundance fit with a momentum-resolved QKE solve and adding the free-streaming → Lyman-α mapping F203 T2 lacked. Tests the **F201** 5.6 keV texture landing against the computed floor (it fails as 100% DM in the fixed-$L$ pass). Points at **F202** (the lepton asymmetry) as the sector whose full depletion dynamics would decide whether the 7.1 keV sterile threads the cold + X-ray-allowed corner. Net: the dark-matter half of the sector is now quantified — under real pressure as 100% DM, with one honest computational door (L-depletion QKE) still open.
