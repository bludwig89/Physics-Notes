# F157 — Phase 2(iii): multi-nucleon nuclei and multi-electron clouds

**Date:** 2026-06-17 - 20:23
**Status:** Confirmed — 5/5 checks PASS (`test_F157_manybody_atoms.py`).
**Roadmap:** `roadmap-scale-to-real-space.md` Phase 2(iii) — closes "multi-electron / multi-nucleon (helium needs the Pauli antisymmetriser) and their coarse-graining", the last un-started Phase-2 item on the spectral/composition side.
**Modules:** `ca-simulation/ca_manybody.py` (new); `ca-simulation/ca_element.py` (A≥3 and Z≥2 hooks now compute); `ca-simulation/ca_atom.py` (numpy fallback for `eigh_tridiagonal`).
**Cross-references:** [[F148-modular-element-assembler]] (the assembler this completes), [[F122-p2-dynamical-baryon-three-body]] (the bound nucleons), [[F104-p4-deuteron-tensor-bound-nucleus]] / [[F126-nn-intermediate-range-sigma-attraction]] / [[F128-nn-short-range-omega-repulsion]] / [[F113-nn-short-range-repulsive-core]] (the model NN one-boson exchange), [[F125-p5-hydrogen-atom-em-bound-state]] (the one-electron Coulomb anchor).

## Result

The F148 element assembler is lifted from "A=1 / Z=1 verified, A≥3 / Z≥2
wired-but-not-run" to actually **computing** multi-nucleon nuclei and
multi-electron clouds, strictly from the model's own building blocks (no fitted
semi-empirical coefficients). Both solvers are numpy-only (the sandbox has no
scipy; the dense tridiagonal eigenproblem is small).

**Multi-electron — Hartree self-consistent field** (`electron_cloud_hartree`).
A Coulomb + Pauli/Aufbau mean field: each occupied subshell is solved in the
field of the nucleus plus all *other* electrons, iterated to self-consistency;
screening is computed from the actual electron density, not tabulated. Only
m_e and α enter (the F125 anchors). Validated: helium Koopmans ionization
**24.0 eV** (CODATA 24.59), total −76.5 eV (the Hartree limit). Generalises by
Aufbau to Li, C (bound, ionizable valence). Tier: Hartree (no
exchange/correlation) — light-atom ionization to a few %.

**Multi-nucleon — A-body variational cluster** (`nuclear_binding_Abody`). A
translationally-invariant 0s Gaussian (one width) fed the model NN interaction:
the central one-boson exchange (σ F126 + ω F128 + quark-Pauli core F113) plus an
effective S=1,T=0 attraction of range ħc/m_π whose depth is fixed so the A=2
variational reproduces the model's **own** deuteron binding
(`solve_deuteron` = 2.234 MeV) — pionless-EFT style, no experimental nucleus
used. Validated: the alpha particle (A=4) binds at **−30.1 MeV** (exp −28.3,
within 6 %); A=3 binds (−12 MeV). Tier: light-nucleus variational (good to
A~4); heavier A overbinds because the spin-isospin/Pauli saturation is not yet
enforced (the remaining frontier).

The assembler now composes a full neutral, stable multi-nucleon/multi-electron
atom (He-4) end to end: nucleus bound (30.1 MeV), electron cloud bound
(−76.5 eV, IP 24.0 eV), net charge 0, `stable = True`.

## Notes

- **Central OBE alone does not bind** (verified: positive ⟨V⟩ for A=2…16). This
  is faithful to the model, where the deuteron binds *only* via the pion tensor
  force (F104); the effective S=1,T=0 attraction carries that physics into the
  A-body solve, anchored to the model deuteron.
- `ca_atom`'s scipy dependency (`eigh_tridiagonal`) is now optional with a
  numpy dense fallback, so the assembler loads and runs without scipy (per the
  CLAUDE.md scipy caveat). Hydrogen levels reproduce (1s −13.6 eV).

## Exactness tier

Electron IPs: Tier-3 quantitative (Hartree, few-%). Nuclear binding: Tier-3
variational (light nuclei good, heavy overbinds — saturation open). Absolute
scales inherit the F123 P6 anchors.
