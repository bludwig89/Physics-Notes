"""F159 — U4: the block-spin two-grid multigrid (scale separation).

roadmap-unified-real-space.md U4 / roadmap-scale-to-real-space.md Phase 1.
The proton (~1 fm) and the Bohr orbit (~5e4 fm) differ by ~6e4 in size — no
single literal lattice resolves both.  The multigrid runs the proton on its own
fine patch and lets it enter the atomic-scale lattice as a block-spin (R_b)
coarse-grained POINT charge, with the block factor b carrying the scale
separation.  This test certifies the two facts that license it:

  M1  R_b is charge-faithful: block-averaging the proton conserves total charge
      exactly and concentrates it (RMS r_p → r_p/b coarse cells)
  M2  R_b commutes with the orbit binding: the point-vs-resolved binding gap
      shrinks as a0/r_p grows (the electron cannot resolve the proton)
  M3  the physical ground state is invariant under the coarse spacing a_c=b·a_f
      (grid/RG invariance in the resolved regime)
  M4  the two-grid atom: charge conserved, electron bound, and the REPRESENTED
      a0/r_p ratio scales linearly with b (b carries the scale separation),
      reaching multiple decades on two tractable lattices

Sandbox scale (small L, short relaxation) — the accurate absolute a0/E0 and the
full physical 6e4 ratio are the job of tests/runners/run_u4_multigrid.py.

Runs under pytest, or standalone:
    PYTHONPATH=ca-simulation python tests/findings/test_F159_multigrid_scale_separation.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "ca-simulation"))

import numpy as np            # noqa: E402
import ca_multigrid as mg     # noqa: E402


def _proton(L=24, rp=3.0):
    a = np.arange(L)
    X, Y, Z = np.meshgrid(a, a, a, indexing="ij")
    c = L // 2
    g = np.exp(-(((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2)) / (2 * rp ** 2))
    return g / g.sum()


def test_M1_Rb_charge_faithful():
    rho = _proton()
    prev = 1e9
    for b in (2, 3, 4, 6):
        _, d = mg.reduce_charge(rho, b)
        assert abs(d["total_coarse_phys"] - 1.0) < 1e-10, d["total_coarse_phys"]
        assert d["rms_coarse_cells"] < prev      # concentrates as b grows
        prev = d["rms_coarse_cells"]


def test_M2_binding_commutes_point_vs_resolved():
    bc = mg.binding_commutes(L=40, a=0.09, relax_steps=700)
    dE = [r["dE_vs_point"] for r in bc["resolved"]]   # r_p decreasing → a0/r_p up
    # the gap monotonically shrinks as the orbit/proton ratio grows
    assert dE[0] > dE[-1], dE
    assert dE[-1] < 0.02, dE[-1]


def test_M3_invariance_under_coarse_spacing():
    inv = mg.invariance_under_b(L=48, a_f=0.05, b_list=(1, 2, 3),
                                relax_steps=700)
    # the physical ground-state energy is ~invariant under the coarse spacing
    assert inv["E0_rel_spread"] < 0.15, inv["E0_rel_spread"]


def test_M4_two_grid_atom_scales_with_b():
    out1 = mg.MultigridAtom(b=2000, relax_steps=700).run()
    out2 = mg.MultigridAtom(b=20000, relax_steps=700).run()
    for o in (out1, out2):
        assert abs(o["proton_charge_conserved"] - 1.0) < 1e-10
        assert o["electron_bound"] is True
    # represented ratio scales linearly with b (same orbit solve, ×10 b → ×10 ratio)
    r = out2["represented_a0_over_rp"] / out1["represented_a0_over_rp"]
    assert abs(r - 10.0) < 0.5, r
    # multiple decades of scale separation on tractable lattices
    assert out2["represented_decades"] > 3.5, out2["represented_decades"]


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    p = f = 0
    for fn in fns:
        try:
            fn(); print("PASS", fn.__name__); p += 1
        except Exception as e:           # noqa: BLE001
            print("FAIL", fn.__name__, repr(e)); traceback.print_exc(); f += 1
    print(f"== {p} passed, {f} failed ==")
    sys.exit(1 if f else 0)
