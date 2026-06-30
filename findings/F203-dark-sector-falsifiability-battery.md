# F203 — The dark-sector falsifiability battery: the six observational tests of `dark-sector-overview.md` §4, built out as quantified, currently-evaluable falsifiers — none falsified, three under genuine 2025 pressure (keV sterile vs XRISM + Lyman-α; $w=-1$ vs DESI DR2), three consistent (Bullet lensing, WIMP/axion nulls, $a_0=cH_0/6$)

**Date:** 2026-06-30 - 22:45
**Numbering:** **F203** (re-checked; F202 taken by the leptogenesis/Sakharov fork). Concurrent lepton-sector sessions hold a separate `F199-angular-self-duality` and `F200-eg-sextic-coupling` — unrelated to the dark sector.
**Status:** **Battery built and evaluated.** Each test carries a model prediction, a current observation (sourced + dated), a quantified margin, a status, and an explicit falsifier. 7/7 checks PASS (six tests + one internal-consistency meta-check). Abundance/structure numbers are order-of-magnitude parametrisations calibrated to the 2025 literature, *not* full Boltzmann/Lyman-α computations — the *directions* and *status classifications* are robust, the *exact* margins are not.
**Module:** `ca-simulation/forks/gr_fork_F203_dark_sector_falsifiers.py` (self-contained, real arithmetic; math + stdlib only, no numpy, no chiral transforms).
**Tests / results:** `tests/findings/test_F203_dark_sector_falsifiers.py` → `test-results/F203_dark_sector_falsifiers_test.json` (7/7); fork dump `test-results/F203_dark_sector_falsifiers.json`.
**Cross-references:** [[F191-dark-matter-rotation-curves-bullet]] (T4 Bullet), [[F194-emergent-gravity-bullet-falsification]] (T4 emergent-gravity exclusion + T6 $a_0$), [[F192-vacuum-energy-full-tensor]] / [[F196-dilution-exponent-derived]] / [[F197-first-excitation-dark-source]] (T3 $w=-1$ identity), [[F198-angular-mode-relic-misalignment]] / [[F199-amplitude-mode-stability-nogo]] (T5 not-axion / not-WIMP), [[F200-sterile-neutrino-dark-matter]] / [[F201-kev-sterile-from-eg-texture]] (T1/T2 keV sterile). Overview: `docs/theory/dark-sector-overview.md` §4. External: XRISM Collaboration 2025 (ApJL 994 L28; arXiv:2510.24560); DESI DR2 2025 (Nature Astronomy s41550-025-02669-6; desi.lbl.gov 2025-03-19); Clowe et al. 2006 (Bullet Cluster); Milgrom 1983 ($a_0$).

---

## What this finding does

`dark-sector-overview.md` §4 listed six falsifiable points but stated them in prose. This finding turns each into a **quantified, currently-evaluable test**: model prediction → current datum/bound → margin → status → falsifier. The deliverable is the honest classification, not a pass: three of the six are under genuine 2025 observational pressure, and the battery reports that rather than rubber-stamping the model.

**Status vocabulary:** `consistent` (data agree), `under_pressure` (tension, not decisive), `falsified` (decisive contradiction). Current tally: **0 falsified, 3 under_pressure, 3 consistent.**

## The six tests

| # | Prediction | Current datum (2025) | Status | Falsifier |
|---|---|---|---|---|
| **T1** | keV sterile → monochromatic X-ray line at $E_\gamma=m_s/2$ (2.8 keV for $m_s{=}5.6$, 3.55 keV for 7.1) | Predicted radiative rate $1.23\times10^{-29}\,\mathrm{s^{-1}}$ sits **1.9 dex below** the XRISM 3σ line limit ($10^{-27}\,\mathrm{s^{-1}}$) — but the combined X-ray+Lyman-α floor for 100% DM is **~41 keV**, above the model's 5.6–7.1 keV | **under_pressure** | clean line non-detection across 2–15 keV at the resonant mixing, or a confirmed line pinning $m_s$ outside the texture's reach |
| **T2** | warm DM → halo-mass-function / satellite / Lyman-α power cutoff at the free-streaming scale (~0.05 Mpc at 5.6 keV) | Non-resonant Lyman-α floor ~28 keV (model **excluded** non-resonant); resonant floor ~7 keV (model survives **at the edge**) | **under_pressure** | structure data pushing the warm cutoff above the X-ray-allowed mass window — closes the overlap |
| **T3** | dark energy strictly $w=-1$, $(w_0,w_a)=(-1,0)$, no evolution | DESI DR2 rejects the cosmological constant at **2.8–4.2σ** (best-fit $w_0\approx-0.75$, $w_a\approx-0.86$); dataset-dependent, $<5σ$ | **under_pressure** | a robust, dataset-independent $w\neq-1$ at $\ge5σ$ kills the pure-VEV identity |
| **T4** | lensing mass tracks the **collisionless** component, offset from the gas | Clowe 2006: offset 0.189 Mpc on the galaxies at 8σ; emergent gravity mispredicts by the full 0.19 Mpc (lensing on gas) | **consistent** | a merger with lensing demonstrably **on the gas** |
| **T5** | relic is a keV sterile — **not** a GeV–TeV WIMP, **not** a QCD axion | direct-detection (LZ/XENONnT) and axion (ADMX) searches null | **consistent** (soft) | a confirmed WIMP/axion carrying the **full** relic abundance (sub-dominant survivable) |
| **T6** | $a_0 = cH_0/6$ — DE scale sets the galactic acceleration scale | $a_0^\text{model}=1.09\times10^{-10}\,\mathrm{m/s^2}$, ratio **0.91** to empirical $1.2\times10^{-10}$ | **consistent** (diagnostic) | none clean — mechanism falsified in F194; retained as a shared-scale hint |

## The two real pressure points (highest-value to watch)

1. **The keV sterile (T1+T2) is squeezed from both sides.** X-ray non-detections bound the mixing from above; Lyman-α bounds the mass from below. The direct XRISM line limit still leaves the resonant benchmark alive (1.9 dex of headroom), but the 2025 *combined* X-ray+Lyman-α statement — that sterile neutrinos cannot be 100% of dark matter below ~41 keV — sits **above** the model's texture-preferred 5.6 keV (F201). The model is not falsified (resonant production with a cooler momentum spectrum + the possibility of a sub-dominant component keep it alive), but the window is narrow and shrinking. **A next-generation X-ray line search or a tightened Lyman-α bound that closes the overlap would falsify the keV-sterile relic.**

2. **Dark energy $w=-1$ (T3) vs DESI DR2.** The model's dark energy is the homogeneous holographic-vacuum VEV (F192/F196/F197), so it predicts $w=-1$ with **no** evolution. DESI DR2 (2025) prefers dynamical dark energy and rejects the cosmological constant at 2.8–4.2σ depending on the supernova sample. This is the model's most observationally active tension. It is **not** a falsification: the DESI preference is dataset-dependent (CMB/BAO/SNe tensions) and below 5σ. **A robust, dataset-independent $w\neq-1$ at $\ge5σ$ would falsify the pure-VEV dark-energy identity** and force a dynamical component the current chain lacks.

## What is computed vs cited

| Piece | Status |
|---|---|
| radiative line rate $\Gamma_\gamma(m_s,\sin^22\theta)$, line energy $m_s/2$ | **Computed** (standard sterile-ν radiative width) |
| $a_0=cH_0/6=1.09\times10^{-10}$, ratio 0.91 | **Computed** (from Planck $H_0$) |
| Bullet offsets (model on galaxies, EG on gas) | **Computed** (toy geometry, reuses F191/F194) |
| XRISM line limit $10^{-27}\,\mathrm{s^{-1}}$; 41 keV 100%-DM floor; Lyman-α floors | **Cited** (2025 literature inputs) |
| DESI DR2 $(w_0,w_a)$ + 2.8–4.2σ CC rejection | **Cited** (2025 DESI DR2) |
| status classifications | **Derived** from the computed margins vs the cited thresholds |

## Caveats (honest scope)

- The abundance, free-streaming, and X-ray/Lyman-α numbers are order-of-magnitude parametrisations calibrated to the 2025 literature, not full Boltzmann or hydrodynamic computations. The status *classifications* (which side of each threshold the model sits on) are robust; the exact dex margins are not.
- T3 encodes representative DESI DR2 best-fit values; the headline metric is the cited 2.8–4.2σ CC rejection, which is the robust statement.
- T5 and T6 are flagged `soft` and `diagnostic` respectively — a positive WIMP/axion detection or an $a_0$ mismatch does not by itself kill the model.
- This is a *battery*, not new physics: it makes the F191–F201 predictions sharp and confronts them with current data. The value is the honest tension accounting.

## Test summary

| Check | Statement | Result |
|---|---|---|
| T1 | X-ray line at $E=m_s/2$; rate below XRISM limit but $m_s$ below the 41 keV 100%-DM floor → under_pressure | PASS |
| T2 | warm-DM cutoff; non-resonant excluded, resonant survives at the edge → under_pressure | PASS |
| T3 | $(w_0,w_a)=(-1,0)$ vs DESI DR2 2.8–4.2σ CC rejection ($<5σ$) → under_pressure | PASS |
| T4 | lensing on collisionless component matches Clowe; emergent gravity falsified → consistent | PASS |
| T5 | keV-sterile identity; WIMP/axion nulls consistent (soft) → consistent | PASS |
| T6 | $a_0=cH_0/6$ within ~10% (diagnostic) → consistent | PASS |
| T7 | battery internally consistent: 6 tests, 0 falsified, 3 under_pressure, 3 consistent | PASS |

**Overall 7/7 PASS** (~0 s, math + stdlib only — numpy-free, no chiral transforms).

## Relation to other findings

Operationalises the §4 falsifiers of `dark-sector-overview.md`, drawing predictions from the full dark chain: dark energy = the $w=-1$ holographic residual (F192/F196/F197), dark matter = the F47 keV sterile neutrino (F200/F201) with the $E_g$ WIMP/axion routes excluded (F198/F199), and the Bullet/emergent-gravity verdicts (F191/F194). Converts each into a sharp, dated, currently-evaluable test. The net: the dark sector is **not** falsified, but the keV sterile and the $w=-1$ dark energy are both under real 2025 pressure — the two places where a near-term measurement could decide the model.
