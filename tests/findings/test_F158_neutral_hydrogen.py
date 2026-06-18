"""F158 — U3: neutral hydrogen as ONE dynamic real-space object.

roadmap-unified-real-space.md, U3.  Combines the U1 confined, charged proton
(three colour Dirac quarks held by the F135/F86 scalar Y-string) and the U2
bound electron (non-relativistic orbital relaxed into the proton's Coulomb
well) on ONE BCC lattice, and certifies the composite-neutral-atom signatures:

  H1  exact neutrality: net EM charge = 0 (uud + e) for the whole run
  H2  all four coupling loops live (J_colour, gluon A, J_em, photon alpha)
  H3  every channel norm conserved to machine precision
  H4  the proton stays CONFINED (bounded cluster RMS) vs the free control,
      which disperses
  H5  the electron cloud TRACKS the proton: the e–p centroid separation stays
      small compared with the cloud radius (a concentric bound cloud)
  H6  the electron stays BOUND (bounded cloud RMS) vs the free control

Compressed scale (one tractable lattice holds both; the physical proton:orbit
~1e4 size ratio is U4).  Structure is the deliverable; absolute fm/eV are
P6/scale-gated (F123).

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/findings/test_F158_neutral_hydrogen.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import casim  # noqa: E402,F401  (puts ca-simulation on sys.path)
from casim.engine import Simulation, LatticeSpec  # noqa: E402
from casim.engine.observers import build_observer  # noqa: E402
from casim.engine.channel import build_channel  # noqa: E402

L = 24
TICKS = 80
EVERY = 20
_CACHE = {}                       # memoize the 3 distinct configs across tests


def _channels(confine=True, bind=True):
    conf = {"mode": "scalar", "anchor": "com", "sigma": 0.5, "dt": 0.5,
            "partners": ["u_r", "u_g", "d_b"]}
    qkw = dict(couplings={"strong": "gluon", "em": "photon"}, eps_strong=0.05)
    cen = [(11, 12, 12), (13, 12, 12), (12, 14, 12)]
    col = ["r", "g", "b"]
    spc = ["u_L", "u_L", "d_L"]
    nm = ["u_r", "u_g", "d_b"]
    specs = [
        {"type": "gluon_sourced", "name": "gluon",
         "sources": nm, "g_lat": 0.5, "dt": 1.0},
        {"type": "photon_sourced", "name": "photon",
         "sources": nm + ["electron"], "dt": 0.1, "g_em": 1.0,
         "coulomb": True, "g_coulomb": 1.0},
    ]
    for i in range(3):
        s = {"type": "quark_dirac", "name": nm[i], "species": spc[i],
             "colour": col[i], "mass": 0.9,
             "init": {"center": list(cen[i]), "width": 1.3}, **qkw}
        if confine:
            s["confine"] = conf
        specs.append(s)
    specs.append(
        {"type": "nr_electron", "name": "electron", "mass": 1.0,
         "charge": -1.0, "g_coulomb": 30.0 if bind else 0.0, "dt": 0.2,
         "sources": nm,
         "init": {"center": [12, 12.7, 12], "width": 3.0,
                  "ground_state": bool(bind), "relax_steps": 600,
                  "relax_dtau": 0.05}})
    return [build_channel(s) for s in specs]


def _run(confine=True, bind=True, ticks=TICKS):
    key = (confine, bind, ticks)
    if key in _CACHE:
        return _CACHE[key]
    lat = LatticeSpec(L=L, topology="bcc", c_lat=0.5773502691896258)
    obs = [build_observer({"type": "unification_readout", "every": EVERY,
                           "gluon": "gluon", "photon": "photon"}),
           build_observer({"type": "norm_conservation", "every": EVERY,
                           "channels": ["u_r", "u_g", "d_b", "electron"]})]
    sim = Simulation(lat, _channels(confine, bind), observers=obs, seed=11)
    res = sim.run(ticks)
    out = (res["observers"]["unification_readout"]["records"],
           res["observers"]["norm_conservation"])
    _CACHE[key] = out
    return out


def test_H1_exact_neutrality():
    ur, _ = _run()
    for r in ur:
        assert abs(r["net_charge"]) < 1e-12, r["net_charge"]


def test_H2_all_loops_live():
    ur, _ = _run()
    loops = ur[-1]["loops"]
    for k in ("J_colour", "gluon_A", "J_em", "photon_alpha"):
        assert loops[k] > 0.0, f"loop {k} dead"


def test_H3_norms_conserved():
    _, nc = _run()
    for cname, d in nc["summary"]["max_rel_drift"].items():
        assert d < 1e-9, f"{cname} drift {d:.2e}"


def test_H4_proton_confined_vs_free():
    ur_c, _ = _run(confine=True)
    ur_f, _ = _run(confine=False)
    pc = ur_c[-1]["proton_rms"]
    pf = ur_f[-1]["proton_rms"]
    # confined proton stays compact; free disperses noticeably more
    assert pc < 0.75 * pf, f"no confinement: confined {pc:.2f} vs free {pf:.2f}"


def test_H5_electron_tracks_proton():
    ur, _ = _run()
    # concentric: the e–p separation stays small vs the electron cloud radius
    for r in ur:
        assert r["ep_separation"] < r["electron_rms_self"], (
            f"electron not concentric at t={r['tick']}: "
            f"sep {r['ep_separation']:.2f} >= rms {r['electron_rms_self']:.2f}")


def test_H6_electron_bound_vs_free():
    ur_b, _ = _run(bind=True)
    ur_f, _ = _run(bind=False)
    eb = ur_b[-1]["electron_rms_self"]
    ef = ur_f[-1]["electron_rms_self"]
    assert eb < 0.75 * ef, f"electron not bound: {eb:.2f} vs free {ef:.2f}"


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
