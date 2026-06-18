# F148 — The modular element assembler: any element as NUCLEUS(Z,N) + ELECTRON CLOUD(Z), verified stable on hydrogen

**Date:** 2026-06-12 - 15:35
**Status:** Confirmed — 13/13 checks PASS. Hydrogen (¹H) is assembled from the model's own building blocks and comes out a stable, neutral, bound atom with every number traceable to the model's constants (no new fitted parameters); the framework composes arbitrary (Z, N) and its heavier-element paths are wired-but-not-faked.
**Roadmap:** completes the composition layer above `docs/roadmaps/roadmap-matter-binding.md` P2 (baryon) / P4 (nuclei) / P5 (atoms) — one entry point that puts a nucleus and an electron cloud together into an element.
**Module:** `ca-simulation/ca_element.py`
**Test:** `tests/findings/test_F148_modular_element_assembler.py` (13/13, ~90 s; numpy + scipy)
**Results:** `test-results/F148_modular_element_assembler.json`
**Cross-references:** [[F122-p2-dynamical-baryon-three-body]] (the confinement-bound proton/neutron the nucleus is made of), [[F125-p5-hydrogen-atom-em-bound-state]] (the Coulomb/Dirac electron solver), [[F104-p4-deuteron-tensor-bound-nucleus]] / [[F128-nn-short-range-omega-repulsion]] / [[F126-nn-intermediate-range-sigma-attraction]] / [[F113-nn-short-range-repulsive-core]] (the model-native NN one-boson-exchange that binds A≥2), [[F120-electron-calibrated-spectrum]] (the electron mass anchor).

---

## Goal

The matter-binding roadmap delivered the parts in isolation: a dynamical proton/neutron (P2), the deuteron (P4), and hydrogen (P5). This finding builds the **composition layer** the user asked for — a single modular entry point, `build_element(Z, N)`, that assembles *any* element out of those parts:

$$\text{atom}(Z, N)\;=\;\text{NUCLEUS}(Z\text{ protons}+N\text{ neutrons})\;+\;\text{ELECTRON CLOUD}(Z\,e^-),$$

so that light or heavy elements differ only by two integers, while the concrete numerical verification target right now is **hydrogen**.

## The design constraint: strictly model-only

The assembler introduces **zero new parameters**. Every quantity it uses is *imported* from an already-published model module — no fitted semi-empirical (liquid-drop) coefficients, no tuned shell gaps, no screening constants:

| ingredient | provenance |
|---|---|
| electron mass $m_e$, proton mass $m_p$, EM coupling $\alpha$ | `ca_atom` (F120 anchor / F122–F123 / F125; $\alpha$ is the one EM input) |
| colour-singlet baryon (proton $uud$, neutron $udd$) | `ca_baryon_dynamics` (F122: confinement-bound, non-dispersing) |
| nucleon–nucleon force (one-boson exchange) | `ca_nuclear` (π F103/F104, σ F126, ω F128, quark-Pauli core F113) |
| Coulomb / Dirac radial electron solver | `ca_atom` (F125) |

So the *framework* is general; the *content* is the model's. Check F certifies this directly: the assembler's $m_e, m_p, \alpha$ are bit-identical to the imported module values.

## Construction

**`Nucleus(Z, N)`** — $A=Z+N$ nucleons, each a model baryon.
- $A=1$: a single confinement-bound baryon (F122). Self-bound; no inter-nucleon force exists to form, so the *nuclear* binding energy is $0$ by definition. The baryon's own boundness is certified by solving the three-quark relative problem (ECG, F122 engine) and confirming a finite discrete ground level with the constituent-quark-mass sum a *minority* of $M$ — the "mass is the string" signature.
- $A=2$ (pn): the full model-native one-boson exchange — π tensor (F104) + bare three-quark σ attraction $g_\sigma^2/4\pi=8.18$ (F126) + isoscalar-vector ω repulsion $g_\omega^2/4\pi=5.39$ (F128, empirical OBE/SU(6) window) + the F113 quark-Pauli derived core, at the model quark size $b=0.55$ fm. **No coupling tuned to the binding.**
- $A\ge3$: the *same* NN OBE potential fed to an $A$-body Jacobi/cluster solver (exactly as F122 generalised the two-body F74 engine to three quarks). Implemented as an honest extension hook — `binding_energy` raises `NotImplementedError` carrying the precise recipe rather than returning an unverified number.

**`ElectronCloud(Z, nuclear_charge)`** — $Z$ electrons in the nuclear field.
- $Z=1$: the F125 exact Coulomb/Dirac solve → ground state $=-\mathrm{Ry}$.
- $Z\ge2$: the same radial Coulomb solver in a self-consistent screened mean field (effective $Z$ per shell) with Pauli/Aufbau filling — model-only (Coulomb + Fermi statistics, no fitted screening). Honest hook (raises with the SCF recipe). The Aufbau configuration itself (Madelung order, Pauli capacities $2,6,10,14$) *is* computed for any $Z$.

**`Element` / `build_element(Z, N)`** — composes the two layers, checks electrical neutrality ($Z-Z=0$), nuclear binding, electronic binding, and returns a structured stability verdict.

## Results (hydrogen, ¹H)

| check | result | tier |
|---|---|---|
| A — net charge $=0$ exactly (1 proton − 1 electron) | $0\,e$ | exact (integer) |
| B1 — proton is a finite, discrete (bound) baryon level | $E_\text{rel}=5.74$ (string units) | structural |
| B2 — mass is the string: constituent-mass fraction $<50\%$ | $29.1\%$ | structural |
| B3 — single-nucleon nuclear binding $=0$ (no bond to form) | $0.0$ MeV | exact |
| C1 — electron 1s level is bound ($E<0$) | $-13.598$ eV | structural |
| C2 — $=-\tfrac12\mu c^2\alpha^2$ from imported $m_e,m_p,\alpha$ | rel $2.5\times10^{-5}$ | machine/grid |
| D — ionization $=+13.598$ eV (measured H) | rel $3.6\times10^{-5}$ | quantitative |
| E — composed verdict: **STABLE** (neutral & nucleus bound & e⁻ bound) | ✓ | structural |
| F — zero new parameters (all constants imported) | bit-identical | exact |
| G1 — `build_element` correct $A$ + exact neutrality across H…U | ✓ | exact |
| G2 — Aufbau noble-gas closures: He 1s², Ne 2p⁶, Ar 3p⁶ | ✓ | structural |
| G3 — $A\ge3$ / $Z\ge2$ paths raise model-only recipes (no fake numbers) | ✓ | structural |
| G4 — $A=2$ deuteron (pn) binds via model NN OBE | $E_b=2.234$ MeV | quantitative |

**The headline.** Hydrogen assembles into a stable, neutral atom from nothing but the model's own pieces: the proton is a confinement-bound baryon (71% of its mass is the colour string, F97/F122), the electron binds at the reduced-mass Rydberg $-13.598$ eV (reconstructed independently from the imported $m_e, m_p, \alpha$ to $2.5\times10^{-5}$), and the atom is electrically neutral by integer construction. The ionization energy $+13.598$ eV matches the measured hydrogen value to $3.6\times10^{-5}$.

**Modularity, certified honestly.** `build_element(Z, N)` composes He, Ne, Ar, Fe, U with the correct mass number, exact neutrality, and correct Aufbau noble-gas closures — the framework demonstrably extends to large elements at the *instantiation* level. The numerical solvers for the heavier paths ($A\ge3$ nuclear binding, $Z\ge2$ electronic SCF) are wired in with their exact model-only recipes but deliberately raise rather than return unverified numbers (G3), so the finding never claims more than it has solved.

## Verdict

The modular multi-nucleon / multi-electron construct requested is delivered: a single entry point that builds an element as a nucleus plus an electron cloud, grounded strictly in the model's existing certified constituents with no new parameters. Hydrogen is verified stable end-to-end (13/13). The same framework composes any element by changing $(Z, N)$; the worked bound states are the $A=1$ baryon nucleus, the $A=2$ deuteron (model-native OBE, $E_b=2.234$ MeV), and the $Z=1$ electron cloud, with the heavier $A$ and $Z$ paths present as honest, model-only extension hooks.

- **Predicted/derived by the model:** the *existence and stability* of neutral hydrogen from the model's own $m_e, m_p, \alpha$; the electron binding (F125); the proton boundness (F122); the deuteron bond (F104/F126/F128/F113); exact neutrality and Aufbau structure for any $Z$.
- **External / flagged:** $\alpha$ (the one EM input, as in F125); the absolute QCD/nucleon scale stays P6-gated (the baryon is reported in string units); the $A\ge3$ many-body solve and $Z\ge2$ electronic SCF are wired but not executed in this build (verification target = hydrogen).

## Scope / next

- Run the $A\ge3$ Jacobi/cluster solver on the wired NN OBE potential → first light nucleus beyond the deuteron (⁴He), then the chart.
- Run the $Z\ge2$ self-consistent screened mean field → helium electronic energy, then ionization-energy trend across a period.
- Tie the nuclear binding to absolute MeV once P6 closes, so binding energies and the valley of β-stability become quantitative across the chart.
