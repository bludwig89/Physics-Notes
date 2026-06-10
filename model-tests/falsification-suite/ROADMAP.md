# Falsification Suite — Roadmap & Run Protocol

`2026-06-10 - 22:11`

**Purpose.** A tiered battery of confrontations between the model and *measured scientific data*, designed to **falsify** the model or specific model elements. This suite **supersedes `model-tests/tests-priority/`** — every test in that suite is either ported here (Tier C) or upgraded into a sharper confrontation (Tiers A/B).

**How to use this file (sub-agent protocol).** Each row below points to one self-contained spec brief (`FA*/FB*/FC*.md`). A Claude Code sub-agent picks up **one brief**, reads it, **builds** the test from the brief (symbolic check and/or a CASIM scenario run), **runs** it, and reports PASS / FALSIFIED / FLAGGED against the brief's pass-fail gate. One brief = one agent = one result JSON in `test-results/`. Briefs are independent; run in any order, but the roadmap is **ordered by falsification power** (run Tier A first — those are the ones that can actually kill the model).

Each brief contains: **Hypothesis** (the parameter-free or calibrated prediction), **Measured target + source**, **Falsification criterion** (what result kills the element), **CASIM build & run** (commands), **Pass/fail gate**, **Provenance** (findings).

---

## Honesty tiers (what "falsify" means per tier)

- **Tier A — sharp falsifiers.** Parameter-free outputs of the lattice rule (inputs are only the cell `a` and `c, ħ`). A clean disagreement with data kills the named element. These are the real risk surface.
- **Tier B — quantitative confrontations.** The *structure* (ratios, shapes, signs) is predicted; one overall scale is calibrated (a single mass or `f_π` anchor). Falsified if the predicted structure misses beyond its stated budget.
- **Tier C — consistency regressions.** The model is GR-identical (PPN β=γ=1) / QM-identical by construction, so these are *checks* not predictions — but a failure would expose an internal break. Ports + consolidates `tests-priority`.

---

## Tier A — sharp falsifiers (run first)

| # | Test | Element under test | Prediction | Measured | Kills it if | Power |
|---|------|--------------------|------------|----------|-------------|-------|
| FA01 | [LIV time-of-flight](FA01-liv-time-of-flight.md) | canonical cell `a` (F30/F79) | `E_QG,2=√54·ħc/a=1.36×10¹⁹ GeV`, subluminal n=2 | `>7×10¹¹ GeV` (LHAASO) | subluminal n=2 bound above 1.4×10¹⁹ GeV, OR any superluminal/linear ToF | ★★★★★ |
| FA02 | [Vacuum birefringence](FA02-vacuum-birefringence.md) | even-law paired photon (F69) | `η=0` exact | `<10⁻¹⁵` | any birefringence detection | ★★★★★ |
| FA03 | [Newton's constant](FA03-newton-constant.md) | structural G (F79) + dielectric (F64) | `G=a²c³/(8π√3ħ)=6.6743×10⁻¹¹`, β=γ=1 | CODATA (3×10⁻⁸) | confirmed G shift / PPN β,γ≠1 / fifth force | ★★★★★ |
| FA04 | [Z/W mass ratio](FA04-mz-mw-ratio.md) | σ↔τ swap (F45) | `m_Z/m_W=2/√3=1.1547` | `1.1346` (PDG, +1.77%) | ratio drifts off 2/√3 beyond running | ★★★★ |
| FA05 | [Koide relation](FA05-koide-relation.md) | E_g condensate (F46/F80) | `Q=2/3` | `0.666661` (1×10⁻⁵) | measured Q drifts off 2/3 | ★★★★★ |
| FA06 | [n−p mass splitting](FA06-neutron-proton-splitting.md) | down–up gap vs EM self-energy (F40/F123) | `+1.51 MeV` (sign +) | `+1.293 MeV` | wrong sign, or magnitude off beyond EM uncertainty | ★★★★★ |
| FA07 | [Weinberg angle](FA07-weinberg-angle.md) | BCC swap/bond geometry (F45/F49) | `sin²θ_W=1/4` bare | `0.2230` (+12%) | residual not RG/matching-shaped | ★★★★ |
| FA08 | [Three generations](FA08-three-generations.md) | BCC irrep selection (F75) | exactly 3 | `N_ν=2.984` | a 4th generation / 4th active ν | ★★★★ |
| FA09 | [Light-bending coefficient](FA09-light-deflection-coefficient.md) | dielectric eikonal (F64) | `K_bend=−4` exact; `1.751190″` | VLBI `1.7510″` | coefficient ≠ −4 (γ≠1) / strong-field departure where GR holds | ★★★★ |
| FA10 | [Black-hole shadow](FA10-black-hole-shadow.md) | exponential metric (F114) | `b_c=2e`, +4.63%, horizon-free | EHT (~10%) | shadow confirmed at `3√3` to <4%, or a true horizon | ★★★★ |

## Tier B — quantitative confrontations

| # | Test | Element | Prediction | Measured | Power |
|---|------|---------|------------|----------|-------|
| FB01 | [Charged-lepton spectrum](FB01-charged-lepton-spectrum.md) | condensate shape, τ-anchored (F121) | m_μ,m_e to ≤0.06% | PDG | ★★★★ |
| FB02 | [Nucleon mass](FB02-nucleon-mass.md) | dynamical constituent mass (F97/F123) | `3m_c=928.5 MeV` (−1.05%) | `938.27` | ★★★★ |
| FB03 | [Pion sector](FB03-pion-sector.md) | NJL Goldstone (F77/F103) | m_π,f_π,⟨q̄q⟩, GMOR | PDG/lattice | ★★★★ |
| FB04 | [Hydrogen Rydberg](FB04-hydrogen-rydberg.md) | EM 1/r bound state (F125) | `13.598 eV` from m_e+α | CODATA | ★★★★ |
| FB05 | [Hydrogen fine structure](FB05-hydrogen-fine-structure.md) | radial Dirac (F125) | `10.95 GHz`, α⁴ | `10.969 GHz` | ★★★★ |
| FB06 | [Positronium](FB06-positronium.md) | two-body reduction (F125) | ratio = ½ | `−6.8 eV` | ★★★ |
| FB07 | [Deuteron binding](FB07-deuteron-binding.md) | pion tensor + σ − ω + core (F104/F126) | binds only via tensor; `E_b=2.224` | `2.2246 MeV` | ★★★★ |
| FB08 | [NN repulsive core](FB08-nn-repulsive-core.md) | quark Pauli + chromomagnetic (F113) | `+341.8 MeV` | Argonne-class | ★★★ |
| FB09 | [√σ/f_π](FB09-string-tension-fpi.md) | two QCD calibrations (F124) | `4.00`/`3.23` | `4.56` | ★★★ |
| FB10 | [Lamb-shift boundary](FB10-lamb-shift-2s-2p.md) | Dirac 2s==2p (F125) | degenerate; Lamb is QED-beyond-sector | `1057 MHz` | ★★★ |
| FB11 | [Condensate angle](FB11-condensate-angle.md) | E_g angle δ (F93/F118) | `15°` chiral limit | `12.733°` | ★★★ |

## Tier C — consistency regressions (supersede tests-priority)

| # | Test | Supersedes | Prediction | Measured | Power |
|---|------|-----------|------------|----------|-------|
| FC01 | [Mercury perihelion](FC01-mercury-perihelion.md) | test_09 | `42.98″/cy` (β=γ=1) | `43.0″/cy` | ★★★ |
| FC02 | [Shapiro delay](FC02-shapiro-delay.md) | test_05/05b | GR log form, γ=1 | Cassini 2.3×10⁻⁵ | ★★★ |
| FC03 | [Pound–Rebka redshift](FC03-pound-rebka-redshift.md) | test_04 | `gΔr/c²` | ~1% / clocks 10⁻⁵ | ★★★ |
| FC04 | [Light deflection (dynamical)](FC04-light-deflection-dynamical.md) | test_01/01b | `4GM/bc²`, open-BC | VLBI `1.7510″` | ★★★ |
| FC05 | [QM battery](FC05-quantum-battery.md) | test_02/08/12/14/15 | CHSH 2√2, tunneling, Δx·Δp≥ħ/2, Zeno, two-slit | textbook QM | ★★★ |
| FC06 | [CPT + Lorentz](FC06-cpt-lorentz.md) | test_13/11 | CPT preserved, SL(2,ℂ) covariant, SR Doppler | kaon/Ives-Stilwell | ★★★★ |
| FC07 | [Charge + anomalies + β-decay](FC07-charge-quantization-beta-decay.md) | test_10/07 | anomalies=0, exact Q, left-chiral β-decay, see-saw | atom neutrality 10⁻²¹ | ★★★★ |

---

## tests-priority → falsification-suite migration map

| old (tests-priority) | new |
|---|---|
| test_01 / 01b GR1 light deflection | FA09 (eikonal) + FC04 (dynamical) |
| test_02 QM1 CHSH | FC05 |
| test_04 GR3 Pound-Rebka | FC03 |
| test_05 / 05b GR2 Shapiro | FC02 |
| test_06 QG2 Planck LV | **FA01** (upgraded to sharp falsifier) |
| test_07 QFT5 neutrino | FC07 (folded in) |
| test_08 QM2 tunneling | FC05 |
| test_09 GR4 Mercury | FC01 |
| test_10 QG4 charge | FC07 |
| test_11 SR4 Doppler | FC06 |
| test_12 QM3 Heisenberg | FC05 |
| test_13 QFT8 CPT | FC06 |
| test_14 QM4 Zeno | FC05 |
| test_15 QM6 two-slit | FC05 |
| — (new sharp predictions, no old equivalent) | FA02–FA08, FA10, FB01–FB11 |

Net: 14 priority tests → 28 falsification tests (10 A + 11 B + 7 C). The matter-binding sector (FB01–FB11) and the strong-field/EW falsifiers (FA02, FA04–FA08, FA10) are entirely new confrontations unlocked by F75–F126.

---

## Matter-sector scenarios (added 2026-06-10)

Three briefs that lean on the momentum-space matter solvers now have dedicated one-command CASIM scenarios, via compute-once channels (`njl_meson` / `njl_nucleon` / `string_tension`, registered in `casim.engine.spectral_matter`) that wrap `ca_meson` / `ca_si_scale` / `ca_qcd_scale_ratio`. All are pure-numpy and sandbox-fast (ticks=1):

| brief | scenario | verified output |
|---|---|---|
| FB03 | `scenarios/njl_pion.yaml` | m_c=311.2, m_π=140.5, f_π=92.6 MeV; m_σ/2m_c=1.0; GMOR 0.39%; chiral m_π=1.6×10⁻⁴ MeV (Goldstone) |
| FB02 / FA06 | `scenarios/njl_nucleon.yaml` | m_c=309.5, m_p=928.5 MeV (−1.05%); n−p=+1.51 MeV (sign +; strong +2.51, EM −1.00) |
| FB09 | `scenarios/string_tension_fpi.yaml` | √σ/f_π axis 4.00 / sphere 3.23 vs empirical 4.56; Λ/f_π=7.04 |

The FB09 confinement cross-check (σ from a 3+1D SU(3) lattice) stays on `scenarios/gauge_mc.yaml` (the only run that hits the sandbox cap → production native).

## Standard run loop (per CLAUDE.md / RUN-GUIDE.md)

1. **Sandbox smoke (Claude):** run the brief's CASIM command at the shipped/reduced `--L` to confirm PASS and time it (≤45 s).
2. **Production (Ben, native):** for any brief whose run hits the cap (only FB09's `gauge_mc` at L≥10), run the full size natively, checkpoint/resume, hand the JSON back.
3. **Symbolic checks:** use real arithmetic + sympy only — **no chiral transforms through numpy/scipy** (CLAUDE.md caveat); verify numpy/scipy first if a chiral/Dirac result looks wrong, and hand-roll the integrator if needed (FB05).
4. **Record:** each brief writes `test-results/<ID>_*.json`; log a one-line `changelog.md` entry; if a run produces a new finding, file `findings/F{N}-*.md` and regenerate `findings-index.md`.

## Falsification surface (one place to look — the three live edges, per F112 §4)

1. **n=2 time-of-flight above 1.4×10¹⁹ GeV** (FA01) — kills the cell directly. Current best is 7 decades short.
2. **Any vacuum birefringence detection** (FA02) — excludes the even-law paired photon.
3. **A confirmed G shift / PPN deviation / fifth force** (FA03) — breaks the dielectric.

Plus the model's two boldest *positive* divergences from GR/SM, which data could confirm or kill: the **+4.63% black-hole shadow / horizon-free object** (FA10), and the **bare sin²θ_W=1/4 → measured running** story (FA07).
