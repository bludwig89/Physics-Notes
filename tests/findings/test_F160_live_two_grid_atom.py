"""F160 — U4 LIVE: the two-grid multigrid hydrogen atom as ONE engine run.

roadmap-unified-real-space.md U4.  F159 proved the *staged* multigrid faithful
(fine→R_b→coarse, offline).  F160 makes it a single live `Simulation.run()`:
one `two_grid_atom` channel co-evolves the FINE confined proton (audited
quark_dirac uud + F135 scalar string) and the COARSE non-relativistic electron
(F156), R_b-reducing the proton charge to a coarse point source every tick.
The block factor b carries the proton:orbit scale ratio (~6e4 — physical
hydrogen) that no single tractable lattice can hold.

  L1  one run, two grids: net EM charge = 0 for the whole run (uud + e)
  L2  norms conserved to machine precision (both sub-evolutions unitary)
  L3  the electron orbit is RESOLVED on the coarse grid (RMS several cells) and
      bounded/stable (not collapsed sub-cell, not dispersing)
  L4  the proton stays CONFINED on the fine grid (bounded fine RMS)
  L5  the represented proton:orbit ratio is ~physical hydrogen (>4.5 decades)
      on tractable lattices — the live scale separation

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/findings/test_F160_live_two_grid_atom.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import casim  # noqa: E402,F401
from casim.engine import Simulation, LatticeSpec  # noqa: E402
from casim.engine.core.channel import build_channel     # noqa: E402
from casim.engine.core.observers import build_observer   # noqa: E402

_CACHE = {}


def _run(ticks=40):
    if ticks in _CACHE:
        return _CACHE[ticks]
    ch = build_channel({"type": "two_grid_atom", "name": "atom", "b": 30000,
                        "fine": {"L": 12, "sigma": 0.5, "dt": 0.5, "mass": 0.9},
                        "coarse": {"L": 32, "m": 1.0, "k": 0.3, "dt": 0.5,
                                   "relax_steps": 500}})
    sim = Simulation(LatticeSpec(L=32, topology="bcc"), [ch],
                     observers=[build_observer({"type": "two_grid_readout",
                                                "every": 10}),
                                build_observer({"type": "norm_conservation",
                                                "every": 10,
                                                "channels": ["atom"]})],
                     seed=11)
    res = sim.run(ticks)
    out = (res["observers"]["two_grid_readout"]["records"],
           res["observers"]["norm_conservation"])
    _CACHE[ticks] = out
    return out


def test_L1_one_run_two_grids_neutral():
    ur, _ = _run()
    for r in ur:
        assert abs(r["net_charge"]) < 1e-9, r["net_charge"]


def test_L2_norms_conserved():
    _, nc = _run()
    assert nc["summary"]["max_rel_drift"]["atom"] < 1e-9


def test_L3_electron_orbit_resolved_and_bounded():
    ur, _ = _run()
    re = [r["electron_rms_coarse"] for r in ur]
    assert min(re) > 3.0, f"orbit sub-cell/unresolved: {min(re):.2f}"
    assert max(re) < 12.0, f"orbit dispersing: {max(re):.2f}"
    assert (max(re) - min(re)) / re[0] < 0.2, "orbit not stable"


def test_L4_proton_confined():
    ur, _ = _run()
    rp = [r["proton_rms_fine"] for r in ur]
    assert max(rp) < 5.0, f"proton not confined (fine RMS {max(rp):.2f})"


def test_L5_physical_scale_ratio_live():
    ur, _ = _run()
    dec = [r["represented_decades"] for r in ur]
    assert min(dec) > 4.5, f"scale ratio too small: {min(dec):.2f} decades"


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
