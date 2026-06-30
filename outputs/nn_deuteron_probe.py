#!/usr/bin/env python3
"""Cleanest inter-nucleon binding test: the TWO-body case (Z=1,N=1 = the
deuteron the V0 was calibrated to).  Track the proton-neutron COM separation
over time with NN binding ON vs OFF, and check the ON case is pulled to a
bounded equilibrium near the V_pair attractive well (not collapsed, not drifting
apart).  Also confirms exact unitarity (norm/charge)."""
import os, sys, json
_REPO = "/sessions/jolly-upbeat-meitner/mnt/Physics Notes"
for _p in (os.path.join(_REPO, "src"), os.path.join(_REPO, "ca-simulation")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import numpy as np
import numpy.random as npr
import casim  # noqa
from casim.engine import LatticeSpec
from casim.engine.channel import build_channel


def _centroid(d, L):
    ax = np.arange(L)
    tot = d.sum()
    if tot <= 0:
        return np.array([L / 2.0] * 3)
    return np.array([float((d.sum(axis=tuple(j for j in range(3) if j != i)) * ax).sum() / tot)
                     for i in range(3)])


def pn_separation(ch, st):
    Lf = ch.Lf
    coms = []
    for grp in ch._nuc_groups:
        d = None
        for nm in grp:
            fs = st[f"fine::{nm}"]
            dd = (np.abs(fs["eta_u"]) ** 2 + np.abs(fs["eta_d"]) ** 2
                  + np.abs(fs["chi_u"]) ** 2 + np.abs(fs["chi_d"]) ** 2).sum(axis=0)
            d = dd if d is None else d + dd
        coms.append(_centroid(np.asarray(d.real), Lf))
    return float(np.linalg.norm(coms[0] - coms[1]))  # fine cells


def run(nn_binding, g_nn=0.012, ticks=120, spread=2.5):
    fine = {"L": 12, "sigma": 0.5, "spread": spread, "live_quarks": True,
            "dt": 0.5, "mass": 0.9, "nn_binding": nn_binding, "g_nn": g_nn}
    coarse = {"L": 24, "m": 1.0, "k": 0.6, "dt": 0.4, "relax_steps": 150,
              "scf_iters": 3, "gs_every": 1, "hartree_every": 4}
    cfg = {"type": "element_atom", "name": "atom", "Z": 1, "N": 1, "b": 30000,
           "fine": fine, "coarse": coarse, "free": False}
    ch = build_channel(cfg)
    rng = npr.default_rng(7)
    lat = LatticeSpec(L=ch.Lc, topology="bcc")
    st = ch.init_state(lat, rng)
    seps, norms = [], []
    n0 = sum(float((np.abs(st[f"fine::{nm}"]["eta_u"]) ** 2
                    + np.abs(st[f"fine::{nm}"]["eta_d"]) ** 2
                    + np.abs(st[f"fine::{nm}"]["chi_u"]) ** 2
                    + np.abs(st[f"fine::{nm}"]["chi_d"]) ** 2).sum())
             for nm in ch._fine_names)
    for t in range(ticks):
        st = ch.step(st, lat, context=None, rng=rng)
        if t % 8 == 0 or t == ticks - 1:
            seps.append((t + 1, round(pn_separation(ch, st), 4)))
            n = sum(float((np.abs(st[f"fine::{nm}"]["eta_u"]) ** 2
                           + np.abs(st[f"fine::{nm}"]["eta_d"]) ** 2
                           + np.abs(st[f"fine::{nm}"]["chi_u"]) ** 2
                           + np.abs(st[f"fine::{nm}"]["chi_d"]) ** 2).sum())
                    for nm in ch._fine_names)
            norms.append(n)
    return {
        "nn_binding": nn_binding, "g_nn": g_nn, "spread": spread,
        "sep_first_cells": seps[0][1], "sep_last_cells": seps[-1][1],
        "sep_min": min(s for _, s in seps), "sep_max": max(s for _, s in seps),
        "norm_drift": (max(norms) - min(norms)) / n0,
        "nn_meta": getattr(ch, "_nn_meta", None),
        "sep_series": seps,
    }


if __name__ == "__main__":
    out = {}
    out["off"] = run(False, ticks=120, spread=2.5)
    print("OFF (no force):", out["off"]["sep_first_cells"], "->",
          out["off"]["sep_last_cells"], "cells; series", out["off"]["sep_series"])
    for g in (0.012, 0.03):
        r = run(True, g_nn=g, ticks=120, spread=2.5)
        out[f"on_g{g}"] = r
        print(f"ON g={g}:", r["sep_first_cells"], "->", r["sep_last_cells"],
              "cells; norm_drift", f'{r["norm_drift"]:.2e}', "; series", r["sep_series"])
    print("\nV_pair meta:", out["on_g0.012"]["nn_meta"])
    with open(os.path.join(os.path.dirname(__file__), "nn_deuteron_probe.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("Saved nn_deuteron_probe.json")
