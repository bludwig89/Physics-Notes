# F160 — U4 LIVE: the two-grid multigrid hydrogen atom as one engine run

**Date:** 2026-06-17 - 20:23
**Status:** Confirmed — 5/5 checks PASS (`test_F160_live_two_grid_atom.py`).
**Roadmap:** `roadmap-unified-real-space.md` U4 — closes the last U4 item (the LIVE two-grid engine run; F159 did the staged version).
**Modules:** `src/casim/particles/channel.py` (`TwoGridAtomChannel`, type `two_grid_atom`; `TwoGridReadout` observer); `ca-simulation/ca_multigrid.py` (single-tick `schrodinger_step` / `coarse_point_potential` helpers); scenario `unified_hydrogen_multigrid.yaml`.
**Cross-references:** [[F159-u4-blockspin-multigrid-scale-separation]] (the staged multigrid this makes live), [[F158-realspace-neutral-hydrogen-atom]] (single-grid compressed atom), [[F136-colour-quark-confinement]] (the fine proton kernel), [[F156-realspace-em-bound-electron]] (the coarse electron), [[F133-blockspin-casim-engine]] (R_b).

## Result

A single CASIM channel (`two_grid_atom`) co-evolves **both grids in one
`Simulation.run()`**:

- **fine patch** — three colour Dirac quarks (uud) confined by the F135 scalar
  Y-string (the audited `quark_dirac` kernel), resolving the proton;
- **coarse grid** — the F156 non-relativistic electron orbital (the Bohr orbit).

Every tick: step the fine proton → block-spin (R_b) reduce its charge to a
point source on the coarse grid (charge-conserving, F133/F159) → step the
electron in that well. The block factor **b = 30 000** carries the
proton:orbit scale ratio that no single tractable lattice can hold; both grids
are tiny (12 fine, 32 coarse cells) yet the run represents the true separation.

Over 80 ticks (`unified_hydrogen_multigrid.yaml`):

- **net EM charge = 0** for the whole run (uud +1, e −1);
- **norms conserved** to ~3×10⁻¹⁴ (both sub-evolutions exactly unitary);
- **electron orbit resolved + stable** on the coarse grid (RMS ≈6.2 cells,
  flat — not collapsed sub-cell, not dispersing);
- **proton confined** on the fine grid (RMS ≈2.6→3.3, bounded);
- **represented a₀/r_p ≈ 6×10⁴ (≈4.8 decades)** — physical hydrogen's ratio —
  produced *live*, in one run, on tractable lattices.

This is the literal "universe in a bottle" milestone made dynamical: the proton
and the orbit co-evolve at their TRUE relative scale (not the U3 compressed
scale), bridged by the RG-exact R_b coupling applied every tick.

## How it sidesteps the one-lattice engine

The engine advances all channels on one shared lattice (one cell size).  The
two-grid atom is therefore encapsulated in a **single channel** that owns both
sub-grids and the per-tick R_b bridge — the fine proton states live under
`fine::*` keys, the coarse electron under `psi`.  The audited kernels are reused
verbatim (`ColourDiracQuarkChannel.step` for the proton, the F156 split-step for
the electron); the channel is wiring, not new physics.  A future engine-level
generalisation (per-channel lattices + an explicit R_b coupling op) could lift
this out of one channel, but the physics is identical.

## Exactness tier

Neutrality + norm conservation: exact / machine-precision.  Confinement,
orbit-resolution, scale ratio: Tier-3 (bounded/stable + represented decades).
Absolute fm/eV remain P6/scale-gated (F123); U4's deliverable is the live scale
ratio, which b carries faithfully (the accurate absolute a₀/E₀ sweep is
`tests/runners/run_u4_multigrid.py`).

## Reproduce

```
PYTHONPATH=src:ca-simulation python -m casim.cli run scenarios/unified_hydrogen_multigrid.yaml
```
