"""F136 — Real-space confined PROTON on genuine SU(3) colour-triplet quarks
(roadmap-unified-real-space.md, U3 Part 1).

Promotes F135's scalar confinement from colour-blind Dirac stand-ins to real
massive colour-triplet Dirac quarks (uud), with the SU(3) gluon loop live and
the EM loop present.

  Q1  exact aggregate quantum number: Σ Q = +1 (uud)
  Q2  scalar string binds the colour-quark cluster (bounded RMS) vs free
      dispersal; norms machine-precision
  Q3  the SU(3) loop is live: each quark publishes J_colour and the gluon
      octet potential A grows from it

Standalone:
    PYTHONPATH=src python tests/findings/test_F136_colour_quark_confinement.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import casim  # noqa: E402,F401
from casim.engine import Simulation, LatticeSpec  # noqa: E402
from casim.engine.channel import build_channel  # noqa: E402

L = 16
P = ["u_r", "u_g", "d_b"]
_IDX = np.indices((L, L, L))
_CENTERS = {"u_r": [7, 8, 8], "u_g": [9, 8, 8], "d_b": [8, 10, 8]}
_FLAV = {"u_r": "u_L", "u_g": "u_L", "d_b": "d_L"}
_COL = {"u_r": "r", "u_g": "g", "d_b": "b"}


def _quark(n, sigma):
    cfg = {"type": "quark_dirac", "name": n, "species": _FLAV[n],
           "colour": _COL[n], "mass": 0.9,
           "init": {"center": _CENTERS[n], "width": 1.3},
           "couplings": {"strong": "gluon", "em": "photon"},
           "eps_strong": 0.05}
    if sigma > 0:
        cfg["confine"] = {"sigma": sigma, "dt": 0.5, "mode": "scalar",
                          "anchor": "com", "partners": P}
    return cfg


def _build(sigma):
    ch = [build_channel({"type": "gluon_sourced", "name": "gluon",
                         "sources": P, "g_lat": 0.5, "dt": 1.0}),
          build_channel({"type": "photon_sourced", "name": "photon",
                         "sources": P, "dt": 0.1, "coulomb": True,
                         "g_coulomb": 2.0})]
    return ch + [build_channel(_quark(n, sigma)) for n in P]


def _cluster_rms(sim):
    d = sum(np.asarray(sim.channels[n].density_field(sim.states[n]))
            for n in P)
    tot = float(d.sum())
    c = [float((d.sum(axis=tuple(j for j in range(3) if j != k))
                * np.arange(L)).sum() / tot) for k in range(3)]
    r2 = sum(((_IDX[k] - c[k] + L / 2.0) % L - L / 2.0) ** 2 for k in range(3))
    return float(np.sqrt(float((d * r2).sum()) / tot))


def _run(sigma, ticks=120):
    sim = Simulation(LatticeSpec(L=L, topology="bcc",
                                 c_lat=0.5773502691896258),
                     _build(sigma), observers=[], seed=11)
    n0 = {n: sim.channels[n].energy(sim.states[n]) for n in P}
    rmax = _cluster_rms(sim)
    for _ in range(ticks):
        sim.step(1)
        rmax = max(rmax, _cluster_rms(sim))
    drift = max(abs(sim.channels[n].energy(sim.states[n]) - n0[n]) / n0[n]
                for n in P)
    jcol = sum(float(np.sqrt((sim.states[n]["J_colour"] ** 2).sum()))
               for n in P)
    gA = float(np.sqrt((sim.states["gluon"]["A"] ** 2).sum()))
    return {"last": _cluster_rms(sim), "max": rmax, "drift": drift,
            "jcol": jcol, "gA": gA}


def test_Q1_proton_charge_is_plus_one():
    from casim.particles import get_spec
    Q = sum(float(get_spec(_FLAV[n]).Q) for n in P)
    assert abs(Q - 1.0) < 1e-12, f"uud charge {Q} != +1"


def test_Q2_scalar_string_binds_colour_quarks():
    conf = _run(0.5)
    free = _run(0.0)
    assert conf["max"] < 4.5, f"confined proton not bound: {conf['max']:.2f}"
    assert free["last"] > 6.0, f"free quarks did not disperse: {free['last']:.2f}"
    assert conf["last"] < 0.65 * free["last"]
    assert conf["drift"] < 1e-10 and free["drift"] < 1e-10


def test_Q3_su3_loop_is_live():
    conf = _run(0.5, ticks=60)
    assert conf["jcol"] > 0.0, "J_colour is dead — quarks not sourcing gluon"
    assert conf["gA"] > 0.0, "gluon potential A did not grow from J_colour"


if __name__ == "__main__":
    test_Q1_proton_charge_is_plus_one()
    print("Q1  PASS — uud aggregate charge = +1")
    test_Q2_scalar_string_binds_colour_quarks()
    print("Q2  PASS — scalar string binds the colour-quark cluster vs free")
    test_Q3_su3_loop_is_live()
    print("Q3  PASS — SU(3) loop live (J_colour sources gluon A)")
    print("F136 3/3 PASS")
