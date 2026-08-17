"""F134 — Unified real-space integration: the full chain on one BCC lattice.

roadmap-unified-real-space.md, U0–U2.  Asserts the *structural* deliverables of
the unified real-space run (the loops are live, the engine is consistent) and
the *quantified physics* outcome (the linearised gluon back-reaction does not
confine — coupled ≡ free; the Coulomb loop measurably attracts the electron
when driven).

  U0.1  full chain runs; every channel's norm conserved to machine precision
  U0.2  all four coupling loops live (‖J_colour‖, ‖gluon A‖, ‖J_em‖, ‖α‖ > 0)
  U0.3  system net EM charge is exactly 0 (uud + e)
  U1    NO real-space confinement from the linearised sourced gluon: the
        proton RMS-radius trajectory is identical coupled-vs-free (the F74 /
        F122 lesson — binding is the non-perturbative string, not exchange)
  U2    the EM/Coulomb loop is responsive: a strongly-driven well attracts the
        electron (smaller initial e-radius / a late pull-back) vs the free
        control, i.e. the binding mechanism is exhibited (not a stationary
        orbit at this compressed scale)

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/findings/test_F134_unified_real_space.py
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

L = 16
TICKS = 30          # shorter than the shipped scenario, for test speed
EVERY = 5


def _base_channels(em_couplings=True, strong_couplings=True,
                    g_coulomb=6.0, m_e=0.3, e_center=(12, 8, 8), e_width=2.0):
    qcoup = ({"strong": "gluon_field", "em": "photon_field", "gravity": "gmass"}
             if strong_couplings else {})
    ecoup = ({"em": "photon_field", "gravity": "gmass"} if em_couplings else {})
    specs = [
        {"type": "gravity_dielectric", "name": "gmass", "M": 1.0, "sigma": 3.0},
        {"type": "gluon_sourced", "name": "gluon_field",
         "sources": ["u_r", "u_g", "d_b"], "g_lat": 1.0, "dt": 1.0},
        {"type": "photon_sourced", "name": "photon_field",
         "sources": ["u_r", "u_g", "d_b", "electron"], "dt": 0.1,
         "g_em": 1.0, "coulomb": True, "g_coulomb": g_coulomb},
        {"type": "particle", "name": "u_r", "species": "u_L", "colour": "r",
         "init": {"center": [8, 8, 8], "width": 1.5},
         "couplings": qcoup, "eps_strong": 0.3},
        {"type": "particle", "name": "u_g", "species": "u_L", "colour": "g",
         "init": {"center": [8, 8, 8], "width": 1.5},
         "couplings": qcoup, "eps_strong": 0.3},
        {"type": "particle", "name": "d_b", "species": "d_L", "colour": "b",
         "init": {"center": [8, 8, 8], "width": 1.5},
         "couplings": qcoup, "eps_strong": 0.3},
        {"type": "particle", "name": "electron", "species": "e_L", "mass": m_e,
         "init": {"center": list(e_center), "width": e_width},
         "couplings": ecoup},
    ]
    return [build_channel(s) for s in specs]


def _run(channels, ticks=TICKS):
    lat = LatticeSpec(L=L, topology="bcc",
                      c_lat=0.5773502691896258)
    obs = [build_observer({"type": "unification_readout", "every": EVERY}),
           build_observer({"type": "norm_conservation", "every": EVERY,
                           "channels": ["u_r", "u_g", "d_b", "electron"]})]
    sim = Simulation(lat, channels, observers=obs, seed=11)
    res = sim.run(ticks)
    ur = res["observers"]["unification_readout"]["records"]
    nc = res["observers"]["norm_conservation"]
    return ur, nc


def test_U0_norm_conservation_and_loops_and_neutrality():
    ur, nc = _run(_base_channels())
    # U0.1 — every matter channel norm-conserving to machine precision
    drift = nc["summary"]["max_rel_drift"]
    for cname, d in drift.items():
        assert d < 1e-9, f"{cname} norm drift {d:.2e} too large"
    # U0.2 — all four loops live
    loops = ur[-1]["loops"]
    for k in ("J_colour", "gluon_A", "J_em", "photon_alpha"):
        assert loops[k] > 0.0, f"loop {k} is dead ({loops[k]})"
    # U0.3 — exact neutrality (uud + e)
    assert abs(ur[-1]["net_charge"]) < 1e-12


def test_U1_no_realspace_confinement_coupled_equals_free():
    """The linearised sourced-gluon back-reaction does NOT confine: the proton
    RMS-radius trajectory is identical with strong coupling on vs off."""
    ur_on, _ = _run(_base_channels(strong_couplings=True))
    ur_off, _ = _run(_base_channels(strong_couplings=False))
    on = [r["proton_rms"] for r in ur_on]
    off = [r["proton_rms"] for r in ur_off]
    max_rel = max(abs(a - b) / b for a, b in zip(on, off) if b > 0)
    # coupled and free dispersion agree to <1% — confinement is absent
    assert max_rel < 0.01, f"unexpected confinement effect {max_rel:.3%}"
    # and the proton genuinely disperses (saturates the box), not stays bound
    assert on[-1] > 2.5 * on[0]


def test_U2_em_loop_is_responsive():
    """A strongly-driven Coulomb well attracts the electron vs the free
    control — the binding MECHANISM is exhibited (not a stationary orbit).

    Matched initial conditions, EM-on vs EM-off, run long enough for the well
    to act (the pull-back appears ~tick 55).  The signature is the minimum
    proton-electron separation: the driven electron is pulled CLOSER than it
    starts, while the free control only ever moves away from its initial sep.
    """
    kw = dict(g_coulomb=80.0, m_e=0.9, e_center=(11, 8, 8), e_width=1.5)
    ur_on, _ = _run(_base_channels(em_couplings=True, **kw), ticks=60)
    ur_off, _ = _run(_base_channels(em_couplings=False, **kw), ticks=60)
    s_minsep = min(r["ep_separation"] for r in ur_on)
    f_minsep = min(r["ep_separation"] for r in ur_off)
    start = ur_on[0]["ep_separation"]
    # the driven electron is pulled closer than its start; the free one is not
    assert s_minsep < start, f"no inward pull: min {s_minsep:.2f} >= start {start:.2f}"
    assert s_minsep < f_minsep - 0.3, (
        f"EM loop shows no attraction vs free: min-sep on {s_minsep:.2f} "
        f"vs off {f_minsep:.2f}")


if __name__ == "__main__":
    test_U0_norm_conservation_and_loops_and_neutrality()
    print("U0  PASS — chain live, loops on, neutral, norms machine-precision")
    test_U1_no_realspace_confinement_coupled_equals_free()
    print("U1  PASS — no confinement from linearised gluon (coupled == free)")
    test_U2_em_loop_is_responsive()
    print("U2  PASS — EM Coulomb loop is responsive (attraction exhibited)")
    print("F134 3/3 PASS")
