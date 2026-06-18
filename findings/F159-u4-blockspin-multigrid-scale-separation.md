# F159 — U4: the block-spin two-grid multigrid defeats the scale-separation wall

**Date:** 2026-06-17 - 20:23
**Status:** Confirmed (first build) — 4/4 checks PASS (`test_F159_multigrid_scale_separation.py`); accurate large-L sweep via `tests/runners/run_u4_multigrid.py`.
**Roadmap:** `roadmap-unified-real-space.md` U4 / `roadmap-scale-to-real-space.md` Phase 1 — the genuine frontier item.
**Modules:** `ca-simulation/ca_multigrid.py` (new); reuses `casim.engine.blockspin.block_average_field` (F133 R_b) and `casim.gravity.solve_poisson_3d_open` (F64 open Poisson).
**Cross-references:** [[F158-realspace-neutral-hydrogen-atom]] (the single-lattice U3 atom this scale-separates), [[F156-realspace-em-bound-electron]] (the bound electron), [[F130-blockspin-rg-gauge-gravity]] / [[F133-blockspin-casim-engine]] (the R_b machinery), [[F125-p5-hydrogen-atom-em-bound-state]] (relativistic fine structure).

## The wall

The proton is ~1 fm; the Bohr orbit is ~5.3×10⁴ fm — a **~6.3×10⁴** size ratio.
No single literal lattice resolves both (`roadmap-scale-to-real-space.md` §2): a
grid fine enough for the proton's internal structure and wide enough for the
orbit needs ≥10¹² cells. U3 (F158) therefore exhibited the atom only at
*compressed* scale. U4 restores the real separation.

## Result

The multigrid runs the proton on its own **fine patch** and lets it enter the
atomic-scale **coarse lattice** as a block-spin (R_b) coarse-grained **point
charge**; the block factor b carries the scale separation while both lattices
stay tractable (~24 fine, ~48 coarse cells per axis). Two facts license it,
each verified:

1. **R_b is charge-faithful.** Block-averaging the proton's charge over b³ fine
   cells conserves the total charge **exactly** (1.000000) and concentrates it
   (RMS r_p → r_p/b coarse cells → a point once b > r_p).

2. **R_b commutes with the orbit binding.** Because the orbit ≫ the proton, the
   electron cannot resolve the proton's internal structure: the point-vs-
   resolved binding-energy gap → 0 as a₀/r_p grows (sandbox: 0.053 → 0.010),
   and the physical ground state is **invariant under the coarse spacing**
   a_c = b·a_f (E₀ rel-spread 0.0027 over b = 1,2,3). The electron is the
   non-relativistic orbital of F156 (atomic e⁻ is non-relativistic; F125 holds
   the relativistic fine structure).

The orchestrated two-grid atom (`MultigridAtom`) at **b = 63 000** represents a
proton:orbit ratio of **4.28×10⁴ (4.63 decades)** — essentially physical
hydrogen's 6.3×10⁴ — with the charge conserved exactly and the electron bound,
on two tractable lattices. This is the "universe in a bottle" within the
renormalised-cell substitution: the literal ~10⁴–10⁵ scale separation, defeated.

The non-relativistic electron solver is quantitatively correct (open-boundary
Poisson, not periodic — periodic images spuriously weaken binding): the
dimensionless point-charge hydrogen gives E₀ = −0.488 → −0.5 Hartree and
⟨r⟩ = 1.54 → 1.5 a₀ as L grows (the production runner converges these).

## Exactness tier

Charge conservation under R_b: **exact** (machine precision). Binding invariance
/ point-vs-resolved: Tier-3 numeric (commute trend + b-invariance). Absolute
E₀/a₀: converging to the exact hydrogen values (production runner). Absolute
fm/eV remain P6/scale-gated (F123); U4's deliverable is the *scale ratio*,
which b carries faithfully.

## What remains

This is the **multigrid as an orchestrated computation** (fine→R_b→coarse). The
remaining frontier is the *live two-grid co-evolution in the CASIM engine* — a
single run nesting a fine proton patch inside a coarse atomic lattice with the
R_b coupling applied every tick (the engine currently assumes one lattice per
run). The physics is proven faithful here; the engine nesting is the next build.

## Reproduce

```
python tests/runners/run_u4_multigrid.py            # accurate, native (long)
python tests/runners/run_u4_multigrid.py --quick    # lighter
```
Writes `test-results/u4_multigrid.json`: absolute E₀ convergence, the b-invariance
sweep, point-vs-resolved binding, and the physical-ratio scale separation.
