"""F156 — U2: a real-space, real-time EM-bound electron (stationary cloud).

roadmap-unified-real-space.md, U2.  Upgrades the F134 U2 result (the EM loop
is *responsive* but not a stationary orbit, because a relativistic Dirac
electron in a vector Coulomb well Klein-tunnels — the F135 vector null / the
Zα→1 Dirac–Coulomb collapse) to a genuine *bound* electron, using the
physically-correct description of an atomic electron: non-relativistic
(v ~ αc), evolved as a Schrödinger orbital by an exactly-unitary split-step
(``nr_electron`` channel).  The relativistic fine structure stays with the
F125 spectral Dirac–Coulomb solve; this is the real-time *binding*.

  B1  the split-step is exactly unitary (orbital norm conserved to the FFT floor)
  B2  the ground state relaxed in the well is STATIONARY: RMS radius flat in
      real time (the bound cloud)
  B3  bounded vs ballistic: the free control (same orbital, no well) disperses
      to many× the bound radius — the binding is real and attractive
  B4  correct attractive sign / neutrality bookkeeping: a +1 source binds the
      q=−1 electron, and the unification readout counts the electron's charge

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/findings/test_F156_realspace_electron_bound.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import casim  # noqa: E402,F401  (package bootstrap)
from casim.engine import Simulation, LatticeSpec  # noqa: E402
from casim.engine.core.observers import build_observer  # noqa: E402
from casim.engine.core.channel import build_channel  # noqa: E402

L = 32
TICKS = 240
EVERY = 40


def _electron_spec(g_coulomb, ground_state, external=True):
    cfg = {
        "type": "nr_electron", "name": "electron",
        "mass": 1.0, "charge": -1.0, "g_coulomb": g_coulomb, "dt": 0.2,
        "init": {"center": [16, 16, 16], "width": 2.0,
                 "ground_state": ground_state,
                 "relax_steps": 600, "relax_dtau": 0.05},
    }
    if external:
        cfg["external_charge"] = {"center": [16, 16, 16], "q": 1.0, "width": 0.8}
    return cfg


def _run(g_coulomb, ground_state, external=True, ticks=TICKS):
    lat = LatticeSpec(L=L, topology="bcc", c_lat=0.5773502691896258)
    chans = [build_channel(_electron_spec(g_coulomb, ground_state, external))]
    obs = [build_observer({"type": "unification_readout", "every": EVERY,
                           "electron": "electron"}),
           build_observer({"type": "norm_conservation", "every": EVERY,
                           "channels": ["electron"]})]
    sim = Simulation(lat, chans, observers=obs, seed=11)
    res = sim.run(ticks)
    ur = res["observers"]["unification_readout"]["records"]
    nc = res["observers"]["norm_conservation"]
    return ur, nc


def test_B1_unitary_norm_conserved():
    _, nc = _run(g_coulomb=12.0, ground_state=True)
    drift = nc["summary"]["max_rel_drift"]["electron"]
    assert drift < 1e-9, f"orbital norm drift {drift:.2e} too large"


def test_B2_ground_state_is_stationary():
    ur, _ = _run(g_coulomb=12.0, ground_state=True)
    rms = [r["electron_rms_self"] for r in ur]
    # the relaxed ground state stays at a fixed, compact radius
    spread = (max(rms) - min(rms)) / rms[0]
    assert spread < 0.05, f"bound RMS not stationary (spread {spread:.3%})"
    assert rms[-1] < 4.0, f"bound radius {rms[-1]:.2f} not compact"


def test_B3_bounded_vs_ballistic():
    ur_b, _ = _run(g_coulomb=12.0, ground_state=True)
    ur_f, _ = _run(g_coulomb=0.0, ground_state=False, external=False)
    rb = ur_b[-1]["electron_rms_self"]
    rf = ur_f[-1]["electron_rms_self"]
    assert rf > 3.0 * rb, (
        f"free control did not disperse relative to bound "
        f"(free {rf:.2f} vs bound {rb:.2f})")


def test_B4_attractive_sign_and_neutrality_count():
    ur, _ = _run(g_coulomb=12.0, ground_state=True)
    # the electron localises ON the +1 source centre (attractive), so its RMS
    # about its own centroid is small and its centroid sits at the source.
    cen = ur[-1]["electron_centroid"]
    assert all(abs(c - 16.0) < 1.0 for c in cen), f"electron off-source {cen}"
    # readout counts the electron's −1 charge
    assert abs(ur[-1]["net_charge"] - (-1.0)) < 1e-9


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
