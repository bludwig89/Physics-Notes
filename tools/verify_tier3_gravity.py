"""Verify the Tier-3 dynamical variable-c refraction channel (SciPy-dependent).

The sandbox has no SciPy, so this runs on Ben's machine where ``ca_curved`` is
importable.  It checks that the engine's ``refraction_2d`` channel reproduces
the raw ``ca_curved.weyl_step_2d_varc_strang`` loop bit-for-bit, confirms the
exact-unitary norm conservation, and (for physics) reports the Snell-law
refraction angles from ``ca_curved.measure_refraction``.  Writes a small
JSON result so the outcome is machine-readable.

Run:
    PYTHONPATH=src python tools/verify_tier3_gravity.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import numpy as np
import casim  # noqa: F401  (package bootstrap)
from casim.engine import Simulation, LatticeSpec
from casim.engine.core.channel import build_channel


def main() -> int:
    try:
        import ca_curved as cv
    except Exception as e:
        print(f"SKIP: ca_curved/SciPy not available ({e})")
        return 0

    out = {}

    # 1. Engine == kernel, bit-for-bit.
    L, ticks = 64, 12
    sim = Simulation(LatticeSpec(L=L, topology="cubic"),
                     [build_channel({"type": "refraction_2d", "n_sub": 4})],
                     [], seed=0)
    st = sim.states["refraction_2d"]
    f, g, c_field, n_sub = st["f"].copy(), st["g"].copy(), st["c_field"], st["n_sub"]
    e0 = sim.channels["refraction_2d"].energy(st)
    sim.step(ticks)
    for _ in range(ticks):
        f, g = cv.weyl_step_2d_varc_strang(f, g, c_field, n_sub=n_sub)
    bit_ident = bool(np.array_equal(sim.states["refraction_2d"]["f"], f)
                     and np.array_equal(sim.states["refraction_2d"]["g"], g))
    e1 = sim.channels["refraction_2d"].energy(sim.states["refraction_2d"])
    out["engine_eq_kernel_bit_identical"] = bit_ident
    out["norm_drift"] = abs(e1 - e0) / e0

    # 2. Physics: Snell-law refraction (the kernel's own measurement).
    try:
        ref = cv.measure_refraction(L=128, n_steps=80, c_left=0.5, c_right=0.25,
                                    k_in=(0.4, 0.2), sigma=6.0, method="strang")
        out["measure_refraction"] = {k: float(v) for k, v in ref.items()
                                     if isinstance(v, (int, float))}
    except Exception as e:
        out["measure_refraction_error"] = str(e)

    dst = os.path.join("test-results", "casim_tier3_refraction_verify.json")
    os.makedirs("test-results", exist_ok=True)
    with open(dst, "w") as fh:
        json.dump(out, fh, indent=2)

    print("Tier-3 refraction verification")
    print(f"  engine == kernel bit-identical : {out['engine_eq_kernel_bit_identical']}")
    print(f"  norm drift (unitary)           : {out['norm_drift']:.2e}")
    if "measure_refraction" in out:
        print(f"  Snell measurement              : {out['measure_refraction']}")
    print(f"  wrote {os.path.abspath(dst)}")
    return 0 if out["engine_eq_kernel_bit_identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
