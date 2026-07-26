# QED-completeness buildout — concurrent-session prompt set

The one-loop QED headline is built: photon self-energy Π (F251), vertex Λ → $a_e=\alpha/2\pi$ (F252), running $\alpha$, Lamb shift, and the Bethe log from the model's own spectrum (F257). This directory holds **seven standalone prompts** that finish the QED sector. Each is written to be copied whole into a fresh session in this project (it assumes `CLAUDE.md` and the compact indexes load automatically).

## The prompts

| # | Prompt file | Builds | Suggested finding |
|---|-------------|--------|:-----------------:|
| 1 | `01-electron-self-energy-prompt.md` | electron self-energy Σ(p) → δm, Z₂; completes the one-loop 1PI set {Π,Σ,Λ} and the Ward identity Z₁=Z₂ between *computed* objects | F258 |
| 2 | `02-infrared-bremsstrahlung-prompt.md` | soft real-photon emission + IR-divergence cancellation (Bloch–Nordsieck / KLN); makes loop cross sections finite | F259 |
| 3 | `03-scattering-processes-prompt.md` | tree S-matrix: Compton (Klein–Nishina), Møller, Bhabha, pair annihilation, e⁺e⁻→μ⁺μ⁻; the positron/crossing sector | F260 |
| 4 | `04-two-loop-precision-muon-prompt.md` | two-loop $a_e$ (the −0.328(α/π)² term), two-loop running, muon $a_\mu$ (lepton universality) | F261 |
| 5 | `05-bound-state-positronium-prompt.md` | positronium (Bethe–Salpeter two-body), hyperfine structure (21 cm), Lamb recoil/finite-size | F262 |
| 6 | `06-nonlinear-strong-field-prompt.md` | Euler–Heisenberg light-by-light, Schwinger pair production | F263 |
| 7 | `07-structural-renormalizability-anomaly-prompt.md` | renormalizability closure, WT all-orders / charge universality, RG (Callan–Symanzik), chiral-anomaly & lattice-doubling consistency | F264 |

## Ordering and dependencies (soft)

These are designed to run **concurrently**. Real dependencies are light:

- **Prompt 1 (self-energy)** is foundational — it produces δm, Z₂ that Prompts 4 and 7 lean on. Start it first if serializing.
- **Prompt 2 (IR)** and **Prompt 3 (processes)** pair naturally: radiatively-corrected cross sections in 3 need the IR cancellation from 2. Tree-level 3 is independent.
- **Prompt 4 (two-loop/muon)** wants the one-loop set complete (Prompt 1 done) for its renormalization inputs.
- **Prompts 5, 6** are essentially independent of the others (reuse F251/F252/F257 and the tree machinery).
- **Prompt 7 (structural)** — the renormalizability/WT parts want Prompt 1's Σ; the anomaly/doubling part is independent and builds on F250.

## F-numbering (read before assigning)

Highest finding on disk was **F257** when this set was written, but **concurrent sessions cause collisions** (see `CLAUDE.md`). Each session must `grep` `findings/` and `findings-index.md` for the true max **immediately before** claiming a number, then take the next free one. The suggested numbers above are hints, not reservations.

## Shared method + hygiene (every prompt)

- **Exactness ladder** (CLAUDE.md): algebraic/exact first (Ward/WT identities, $b_0$, anomaly coefficients via sympy), then machine precision (form factors, integrals), then quantitative vs measured. Record each in `docs/status/exactness-inventory.md`.
- **No `np.linalg.eig` on chiral matrices.** Build BZ quadrature and matrix routines explicitly; numpy/scipy may silently drop imaginary parts on chiral transforms — check first.
- **Reuse, don't reinvent.** The abelian loop template is `ca_vacuum_polarization.py` (F251) and `ca_vertex_loop.py` (F252); the non-abelian analogue is `ca_bgfield_loop.py` (F162) / `ca_gluon_self_energy.py` (F155). The vertex is the F87/F68 identity-channel Peierls phase; the internal photon is the F69 even-law paired photon (F250 gauge pole); the internal electron is the F27/F46 Weyl fermion. Do **not** use the chiral σ-bilinear propagator (that is W/Z/gluon, F72).
- **Deliverables per finding:** new `ca-simulation/ca_*` module(s), `tests/findings/test_F{N}_*.py`, `test-results/F{N}_*.json`, `findings/F{N}-*.md`. Extend the F249 battery where a new observable belongs there.
- **Finish:** `python3 tools/regen_indexes.py`, one-paragraph `docs/status/changelog.md` entry with a `yyyy-mm-dd - hh:mm` stamp, update `docs/status/exactness-inventory.md`.

## Reference constants

CODATA 2022 / PDG throughout (already collected in `test_F249_qed_comparison_battery.py` `REFERENCES` and the F251/F252 module headers). Reuse those rather than re-entering values.
