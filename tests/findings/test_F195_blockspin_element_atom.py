"""F195 — Fully stable block-spin atom for a general element (Z, N).

Generalises the F160 live two-grid hydrogen atom to a general element:

  * FINE patch  — Tier A: A=Z+N nucleon charge blobs in a bound cluster whose
    net rho_em integrates to EXACTLY +Z (the N neutrons carry zero net charge),
    R_b-reduced to a single +Z coarse point source (F159 faithful).  Tier B
    (He-capped) runs 3·A live quark_dirac quarks instead.
  * COARSE grid — Z electrons filled into the Aufbau configuration as distinct
    spatial orbitals (Hund's rule), each an exactly-unitary F156 split-step
    packet in the self-consistent mean field = +Z nuclear well + the live
    Hartree repulsion of the OTHER electrons.  Pauli antisymmetry is enforced
    by Gram-Schmidt orthonormalising the occupied orbitals each tick.

Acceptance gates ("fully stable") — certified on H → He → Li → C:

  L1  net charge ≡ 0 to machine precision (integer Z·(+1) + Z·(−1))
  L2  every norm conserved to ~1e-13 (the kernels are exactly unitary)
  L3  Pauli: occupied orbitals stay mutually orthogonal (overlap ~1e-13)
  L4  every radius bounded over a long run (≥300 ticks): cloud RMS neither
      collapses sub-cell nor disperses to the box
  L5  cloud surrounds nucleus (represented cloud radius ≫ nucleus radius) and
      the cloud centroid tracks the nucleus (separation ≪ cloud radius)
  L6  bounded-vs-ballistic: the matched free control (no well, no e-e field)
      disperses while the bound cloud stays bounded — binding is exhibited
  L7  the represented a₀/r_nuc scale ratio is carried by b (>4 decades)
  L8  Tier B (He): 3·A live confined quarks are loop-live (‖J_em‖>0), the
      nucleus charge integrates to +Z, net charge + norms machine-precision

Structure + scale ratio are the deliverable; absolute fm/eV stay P6/scale-gated
(F123).  Open shells (Li/C) are the F157-flagged frontier — certified stable
here with the uniform deep coarse config.

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/findings/test_F195_blockspin_element_atom.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import numpy as np                                     # noqa: E402
import casim                                            # noqa: E402,F401
from casim.engine import Simulation, LatticeSpec        # noqa: E402
from casim.engine.channel import build_channel          # noqa: E402
from casim.engine.observers import build_observer        # noqa: E402

# uniform deep coarse config that certifies the whole H→He→Li→C ladder
_COARSE = {"L": 28, "m": 1.0, "k": 0.6, "dt": 0.4, "relax_steps": 1000,
           "scf_iters": 12, "gs_every": 1, "hartree_every": 3}
_CACHE = {}


def _run(Z, N, ticks=300, free=False, live_quarks=False, coarse=None):
    key = (Z, N, ticks, free, live_quarks)
    if key in _CACHE:
        return _CACHE[key]
    coarse = dict(coarse or _COARSE)
    Lc = coarse["L"]
    fine = {"L": 12, "sigma": 0.5, "spread": 2.0}
    if live_quarks:
        fine["live_quarks"] = True
        fine.update({"dt": 0.5, "mass": 0.9})
    cfg = {"type": "element_atom", "name": "atom", "Z": Z, "N": N, "b": 30000,
           "fine": fine, "coarse": coarse, "free": free}
    ch = build_channel(cfg)
    obs = [build_observer({"type": "atom_stability_readout", "every": 25})]
    if not free:
        obs.append(build_observer({"type": "norm_conservation", "every": 25,
                                   "channels": ["atom"]}))
    sim = Simulation(LatticeSpec(L=Lc, topology="bcc"), [ch], observers=obs,
                     seed=7)
    res = sim.run(ticks)
    rec = res["observers"]["atom_stability_readout"]["records"]
    drift = (res["observers"]["norm_conservation"]["summary"]
             ["max_rel_drift"]["atom"]) if not free else None
    out = (rec, drift)
    _CACHE[key] = out
    return out


_LADDER = [(2, 2, "He"), (3, 4, "Li"), (6, 6, "C")]


# ---- L1: net charge ≡ 0 (machine precision) ---------------------------------
def test_L1_net_charge_zero():
    for Z, N, nm in _LADDER:
        rec, _ = _run(Z, N)
        for r in rec:
            assert abs(r["net_charge"]) < 1e-12, (nm, r["net_charge"])


# ---- L2: norms conserved to ~1e-13 ------------------------------------------
def test_L2_norms_conserved():
    for Z, N, nm in _LADDER:
        _, drift = _run(Z, N)
        assert drift < 1e-12, (nm, drift)


# ---- L3: Pauli orthogonality ------------------------------------------------
def test_L3_pauli_orthogonality():
    for Z, N, nm in _LADDER:
        rec, _ = _run(Z, N)
        mx = max(r["max_orbital_overlap"] for r in rec)
        assert mx < 1e-10, (nm, mx)


# ---- L4: bounded radii over a long run --------------------------------------
def test_L4_radii_bounded():
    for Z, N, nm in _LADDER:
        rec, _ = _run(Z, N)
        cr = [r["cloud_rms_coarse"] for r in rec]
        assert min(cr) > 1.0, (nm, "cloud collapsed", min(cr))
        assert max(cr) < 0.5 * _COARSE["L"], (nm, "cloud dispersing", max(cr))
        assert (max(cr) - min(cr)) / cr[0] < 0.25, (nm, "cloud not stable")
        # every individual shell bounded within the box too
        for r in rec:
            assert max(r["shell_rms_coarse"]) < 0.5 * _COARSE["L"], nm


# ---- L5: cloud surrounds nucleus + centroid tracking ------------------------
def test_L5_cloud_surrounds_and_tracks():
    for Z, N, nm in _LADDER:
        rec, _ = _run(Z, N)
        for r in rec:
            assert r["cloud_surrounds_nucleus"], nm
            # cloud centroid sits on the nucleus (point at coarse centre)
            assert r["cloud_centroid_sep"] < 0.25 * r["cloud_rms_coarse"], nm


# ---- L6: bounded-vs-ballistic (free control disperses) ----------------------
def test_L6_free_control_disperses():
    for Z, N, nm in _LADDER:
        rec_b, _ = _run(Z, N)
        rec_f, _ = _run(Z, N, ticks=120, free=True)
        bound_max = max(r["cloud_rms_coarse"] for r in rec_b)
        free_max = max(r["cloud_rms_coarse"] for r in rec_f)
        assert free_max > 1.8 * bound_max, (nm, bound_max, free_max)


# ---- L7: represented scale ratio carried by b -------------------------------
def test_L7_scale_decades():
    for Z, N, nm in _LADDER:
        rec, _ = _run(Z, N)
        dec = [r["represented_decades"] for r in rec]
        assert min(dec) > 4.0, (nm, min(dec))


# ---- L8: Tier B (He) live quarks loop-live + bounded ------------------------
def test_L8_tierB_helium_live_quarks():
    rec, drift = _run(2, 2, ticks=60, live_quarks=True,
                      coarse={"L": 24, "m": 1.0, "k": 0.6, "dt": 0.4,
                              "relax_steps": 300, "scf_iters": 5,
                              "gs_every": 1, "hartree_every": 4})
    last = rec[-1]
    assert last["tier"].startswith("B"), last["tier"]
    # +Z nucleus from the live rho_em
    assert abs(last["nuc_charge"] - 2.0) < 1e-3, last["nuc_charge"]
    assert abs(last["net_charge"]) < 1e-10, last["net_charge"]
    assert drift < 1e-10, drift
    # loop liveness: the quarks carry a non-zero EM current
    ll = last["loop_liveness"]
    assert ll is not None and ll["J_em_norm"] > 0 and ll["rho_em_norm"] > 0, ll
    # nucleus cluster bounded within the fine patch (Lf=12) for the run
    nr = [r["nucleus_rms_fine"] for r in rec]
    assert max(nr) < 5.0, max(nr)


# ---- H consistency (element_atom path; F160 two_grid_atom untouched) ---------
def test_L9_hydrogen_consistent():
    rec, drift = _run(1, 0, ticks=200)
    last = rec[-1]
    assert abs(last["net_charge"]) < 1e-12
    assert drift < 1e-12
    assert last["n_orbitals"] == 1 and last["occupations"] == [1]
    assert last["cloud_surrounds_nucleus"]


def _dump_results():
    """Collect a results JSON for the finding (standalone run)."""
    import json
    summary = {"finding": "F195", "ladder": {}, "tierB_He": {}}
    for Z, N, nm in [(1, 0, "H")] + _LADDER:
        rec, drift = _run(Z, N, ticks=300 if (Z, N) != (1, 0) else 200)
        cr = [r["cloud_rms_coarse"] for r in rec]
        rec_f, _ = _run(Z, N, ticks=120, free=True)
        free_max = max(r["cloud_rms_coarse"] for r in rec_f)
        last = rec[-1]
        summary["ladder"][nm] = {
            "Z": Z, "N": N, "A": Z + N,
            "n_orbitals": last["n_orbitals"], "occupations": last["occupations"],
            "net_charge": last["net_charge"], "norm_drift": drift,
            "max_orbital_overlap": max(r["max_orbital_overlap"] for r in rec),
            "cloud_rms_min": min(cr), "cloud_rms_max": max(cr),
            "cloud_reldrift": (max(cr) - min(cr)) / cr[0],
            "nucleus_rms_fine": last["nucleus_rms_fine"],
            "free_cloud_rms_max": free_max,
            "represented_decades": last["represented_decades"],
            "cloud_centroid_sep": last["cloud_centroid_sep"],
            "tier": last["tier"],
        }
    rb, dB = _run(2, 2, ticks=60, live_quarks=True,
                  coarse={"L": 24, "m": 1.0, "k": 0.6, "dt": 0.4,
                          "relax_steps": 300, "scf_iters": 5,
                          "gs_every": 1, "hartree_every": 4})
    lastB = rb[-1]
    summary["tierB_He"] = {
        "nuc_charge": lastB["nuc_charge"], "net_charge": lastB["net_charge"],
        "norm_drift": dB, "loop_liveness": lastB["loop_liveness"],
        "nucleus_rms_fine_max": max(r["nucleus_rms_fine"] for r in rb),
        "tier": lastB["tier"],
    }
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "..", "test-results",
                       "F195_blockspin_element_atom.json")
    with open(os.path.abspath(out), "w") as fh:
        json.dump(summary, fh, indent=2)
    return os.path.abspath(out)


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    p = f = 0
    for fn in fns:
        try:
            fn(); print("PASS", fn.__name__); p += 1
        except Exception as e:                          # noqa: BLE001
            print("FAIL", fn.__name__, repr(e)); traceback.print_exc(); f += 1
    path = _dump_results()
    print(f"results → {path}")
    print(f"== {p} passed, {f} failed ==")
    sys.exit(1 if f else 0)
