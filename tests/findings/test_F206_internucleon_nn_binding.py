#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F206 — Tier-B inter-nucleon NN one-boson-exchange binding (closes the F195
Tier-B frontier).

The F195 live block-spin atom confined each nucleon's three quarks to their own
COM but left the A nucleons MUTUALLY UNBOUND ("the inter-nucleon OBE binding is
not yet wired into Tier B"; the He cluster breathed ~50 %).  This test certifies
the now-wired model NN one-boson-exchange (``ElementAtomChannel._setup_nn_potential``
+ ``_apply_nn_binding``): the central V_pair(r) = σ(F126) + ω(F128) +
quark-Pauli core(F113) − V0·π-tensor(F104), with V0 fixed to the MODEL deuteron
binding (no experimental nucleus), applied as an exactly-unitary Lorentz-scalar
η↔χ mass rotation (the F135 MIT-bag mechanism) — a genuine attractive
inter-nucleon force.

Checks (all pure-diagnostic; the engine arithmetic is REAL / numpy):
  C1  exact unitarity — quark norm conserved to machine precision under binding.
  C2  charge conservation — net charge ≡ 0, +Z from the live rho_em.
  C3  binding contracts — with the force ON the two-body (deuteron) COM
      separation is pulled well inside the unbound seed separation.
  C4  bounded equilibrium — the ON separation SATURATES (does not collapse to a
      point, does not diverge): late-time variation is small.
  C5  repulsive core sets the floor — a stronger coupling does NOT collapse the
      cluster further (equilibrium is set by the F113/F128 core, not g_nn).
  C6  many-body (He-4) — the 4-nucleon COM cluster contracts vs the unbound
      control while net charge / norm stay machine-precision.
"""
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import numpy as np                                       # noqa: E402
import numpy.random as npr                               # noqa: E402
import casim                                              # noqa: E402,F401
from casim.engine import LatticeSpec                      # noqa: E402
from casim.engine.channel import build_channel            # noqa: E402

_CACHE = {}


def _centroid(d, L):
    ax = np.arange(L)
    tot = d.sum()
    if tot <= 0:
        return np.array([L / 2.0] * 3)
    return np.array([float((d.sum(axis=tuple(j for j in range(3) if j != i)) * ax).sum() / tot)
                     for i in range(3)])


def _nucleon_coms(ch, st):
    coms = []
    for grp in ch._nuc_groups:
        d = None
        for nm in grp:
            fs = st[f"fine::{nm}"]
            dd = (np.abs(fs["eta_u"]) ** 2 + np.abs(fs["eta_d"]) ** 2
                  + np.abs(fs["chi_u"]) ** 2 + np.abs(fs["chi_d"]) ** 2).sum(axis=0)
            d = dd if d is None else d + dd
        coms.append(_centroid(np.asarray(d.real), ch.Lf))
    return coms


def _quark_norm(ch, st):
    return sum(float((np.abs(st[f"fine::{nm}"]["eta_u"]) ** 2
                      + np.abs(st[f"fine::{nm}"]["eta_d"]) ** 2
                      + np.abs(st[f"fine::{nm}"]["chi_u"]) ** 2
                      + np.abs(st[f"fine::{nm}"]["chi_d"]) ** 2).sum())
               for nm in ch._fine_names)


def _net_charge(ch, st):
    rho = None
    for nm in ch._fine_names:
        r = st[f"fine::{nm}"].get("rho_em")
        if r is not None:
            rho = r if rho is None else rho + r
    return float(np.sum(rho)) if rho is not None else 0.0


def _run(Z, N, nn_binding, g_nn=0.012, ticks=100, spread=2.5):
    key = (Z, N, nn_binding, g_nn, ticks, spread)
    if key in _CACHE:
        return _CACHE[key]
    fine = {"L": 12, "sigma": 0.5, "spread": spread, "live_quarks": True,
            "dt": 0.5, "mass": 0.9, "nn_binding": nn_binding, "g_nn": g_nn}
    coarse = {"L": 24, "m": 1.0, "k": 0.6, "dt": 0.4, "relax_steps": 120,
              "scf_iters": 3, "gs_every": 1, "hartree_every": 4}
    cfg = {"type": "element_atom", "name": "atom", "Z": Z, "N": N, "b": 30000,
           "fine": fine, "coarse": coarse, "free": False}
    ch = build_channel(cfg)
    rng = npr.default_rng(7)
    lat = LatticeSpec(L=ch.Lc, topology="bcc")
    st = ch.init_state(lat, rng)
    n0 = _quark_norm(ch, st)
    coms0 = _nucleon_coms(ch, st)
    com_rms0 = float(np.sqrt(np.mean((np.array(coms0) - np.array(coms0).mean(0)) ** 2)))
    seps, com_rmss, norms, charges = [], [], [], []
    for t in range(ticks):
        st = ch.step(st, lat, context=None, rng=rng)
        if t % 5 == 0 or t == ticks - 1:
            cs = np.array(_nucleon_coms(ch, st))
            if len(cs) == 2:
                seps.append(float(np.linalg.norm(cs[0] - cs[1])))
            com_rmss.append(float(np.sqrt(np.mean((cs - cs.mean(0)) ** 2))))
            norms.append(_quark_norm(ch, st))
            charges.append(_net_charge(ch, st))
    out = {
        "Z": Z, "N": N, "nn_binding": nn_binding, "g_nn": g_nn,
        "com_rms_seed": com_rms0, "com_rms_first": com_rmss[0],
        "com_rms_last": com_rmss[-1], "com_rms_min": min(com_rmss),
        "sep_seed": (seps and seps[0]), "sep_last": (seps[-1] if seps else None),
        "sep_late": (seps[-4:] if len(seps) >= 4 else seps),
        "norm_drift": (max(norms) - min(norms)) / n0,
        "charge_last": charges[-1], "n_meta": getattr(ch, "_nn_meta", None),
    }
    _CACHE[key] = out
    return out


# ---- C1: exact unitarity under binding --------------------------------------
def test_C1_unitary_under_binding():
    r = _run(1, 1, True, g_nn=0.012, ticks=100)
    assert r["norm_drift"] < 1e-10, r["norm_drift"]


# ---- C2: charge conserved, +Z from live rho_em ------------------------------
def test_C2_charge_conserved():
    r = _run(1, 1, True, g_nn=0.012, ticks=100)
    assert abs(r["charge_last"] - 1.0) < 1e-3, r["charge_last"]   # Z=1 proton


# ---- C3: binding contracts the deuteron vs the unbound control --------------
def test_C3_binding_contracts():
    on = _run(1, 1, True, g_nn=0.012, ticks=100)
    off = _run(1, 1, False, ticks=100)
    # the force pulls the two nucleons well inside the unbound separation
    assert on["sep_last"] < 0.75 * off["sep_last"], (on["sep_last"], off["sep_last"])


# ---- C4: bounded equilibrium (saturates, no collapse, no divergence) --------
def test_C4_bounded_equilibrium():
    on = _run(1, 1, True, g_nn=0.012, ticks=100)
    late = on["sep_late"]
    assert min(late) > 1.0, ("collapsed", late)                  # not a point
    assert max(late) < on["sep_seed"], ("not bound", late)       # inside seed
    spread = (max(late) - min(late)) / np.mean(late)
    assert spread < 0.15, ("not saturated", spread, late)        # steady


# ---- C5: the repulsive core sets the floor (stronger g ≠ tighter collapse) ---
def test_C5_core_sets_floor():
    weak = _run(1, 1, True, g_nn=0.012, ticks=100)
    strong = _run(1, 1, True, g_nn=0.03, ticks=100)
    # a 2.5x stronger coupling does not collapse the cluster further: the
    # equilibrium is governed by the F113/F128 repulsive core, not g_nn.
    assert strong["sep_last"] > 0.85 * weak["sep_last"], (weak["sep_last"], strong["sep_last"])


# ---- C6: many-body He-4 cluster contracts, machine-precision conserved -------
def test_C6_helium_cluster_binds():
    on = _run(2, 2, True, g_nn=0.012, ticks=60, spread=2.0)
    off = _run(2, 2, False, ticks=60, spread=2.0)
    assert on["com_rms_last"] < off["com_rms_last"], (on["com_rms_last"], off["com_rms_last"])
    assert on["norm_drift"] < 1e-10, on["norm_drift"]
    assert abs(on["charge_last"] - 2.0) < 1e-3, on["charge_last"]


def _dump_results():
    res = {
        "finding": "F206",
        "title": "Tier-B inter-nucleon NN one-boson-exchange binding",
        "deuteron_off": _run(1, 1, False, ticks=100),
        "deuteron_on_g0.012": _run(1, 1, True, g_nn=0.012, ticks=100),
        "deuteron_on_g0.03": _run(1, 1, True, g_nn=0.03, ticks=100),
        "helium_off": _run(2, 2, False, ticks=60, spread=2.0),
        "helium_on_g0.012": _run(2, 2, True, g_nn=0.012, ticks=60, spread=2.0),
    }
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "..", "test-results",
                       "F206_internucleon_nn_binding.json")
    with open(out, "w") as f:
        json.dump(res, f, indent=2)
    return out


if __name__ == "__main__":
    p = _dump_results()
    print("wrote", p)
