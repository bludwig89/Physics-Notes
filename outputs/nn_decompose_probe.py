#!/usr/bin/env python3
"""Decompose the Tier-B He 'breathing' into INTER-nucleon COM spread (what the
NN binding should control) vs INTRA-nucleon blob RMS (controlled by the F135
confinement, not NN).  Steps the ElementAtomChannel directly so we get a
per-tick time series, and scans g_nn."""
import os, sys, json
_REPO = "/sessions/jolly-upbeat-meitner/mnt/Physics Notes"
for _p in (os.path.join(_REPO, "src"), os.path.join(_REPO, "ca-simulation")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import numpy as np
import casim  # noqa
from casim.engine.channel import build_channel


def _centroid(d, L):
    ax = np.arange(L)
    tot = d.sum()
    if tot <= 0:
        return np.array([L / 2.0] * 3)
    return np.array([float((d.sum(axis=tuple(j for j in range(3) if j != i)) * ax).sum() / tot)
                     for i in range(3)])


def make_channel(nn_binding, g_nn):
    fine = {"L": 12, "sigma": 0.5, "spread": 2.0, "live_quarks": True,
            "dt": 0.5, "mass": 0.9, "nn_binding": nn_binding, "g_nn": g_nn}
    coarse = {"L": 24, "m": 1.0, "k": 0.6, "dt": 0.4, "relax_steps": 200,
              "scf_iters": 4, "gs_every": 1, "hartree_every": 4}
    cfg = {"type": "element_atom", "name": "atom", "Z": 2, "N": 2, "b": 30000,
           "fine": fine, "coarse": coarse, "free": False}
    return build_channel(cfg)


def decompose(ch, st):
    """Return (com_rms over nucleon centres, mean intra-nucleon blob rms)."""
    Lf = ch.Lf
    coms, intra = [], []
    for grp in ch._nuc_groups:
        d = None
        for nm in grp:
            fs = st[f"fine::{nm}"]
            dd = (np.abs(fs["eta_u"]) ** 2 + np.abs(fs["eta_d"]) ** 2
                  + np.abs(fs["chi_u"]) ** 2 + np.abs(fs["chi_d"]) ** 2).sum(axis=0)
            d = dd if d is None else d + dd
        d = np.asarray(d.real if np.iscomplexobj(d) else d)
        c = _centroid(d, Lf)
        coms.append(c)
        # intra blob rms about its own centroid
        ax = np.arange(Lf)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
        tot = d.sum()
        r2 = ((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2)
        intra.append(float(np.sqrt((d * r2).sum() / tot)) if tot > 0 else 0.0)
    coms = np.array(coms)
    com_rms = float(np.sqrt(np.mean((coms - coms.mean(0)) ** 2)))
    return com_rms, float(np.mean(intra))


def run(nn_binding, g_nn=0.012, ticks=80, rng_seed=7):
    import numpy.random as npr
    ch = make_channel(nn_binding, g_nn)
    rng = npr.default_rng(rng_seed)
    # init_state needs a lattice; reuse the coarse lattice spec
    from casim.engine import LatticeSpec
    lat = LatticeSpec(L=ch.Lc, topology="bcc")
    st = ch.init_state(lat, rng)
    series = []
    for t in range(ticks):
        st = ch.step(st, lat, context=None, rng=rng)
        if t % 10 == 0 or t == ticks - 1:
            com_rms, intra = decompose(ch, st)
            series.append({"tick": t + 1, "com_rms": round(com_rms, 4),
                           "intra_rms": round(intra, 4)})
    first, last = series[0], series[-1]
    return {
        "nn_binding": nn_binding, "g_nn": g_nn,
        "com_rms_first": first["com_rms"], "com_rms_last": last["com_rms"],
        "com_rms_drift": (last["com_rms"] - first["com_rms"]) / first["com_rms"],
        "intra_rms_first": first["intra_rms"], "intra_rms_last": last["intra_rms"],
        "intra_rms_drift": (last["intra_rms"] - first["intra_rms"]) / first["intra_rms"],
        "nn_meta": getattr(ch, "_nn_meta", None),
        "series": series,
    }


if __name__ == "__main__":
    out = {"off": run(False)}
    print("OFF:", json.dumps({k: out["off"][k] for k in
          ("com_rms_first", "com_rms_last", "com_rms_drift",
           "intra_rms_first", "intra_rms_last", "intra_rms_drift")}, indent=2))
    for g in (0.006, 0.012, 0.024, 0.05):
        r = run(True, g_nn=g)
        out[f"on_g{g}"] = r
        print(f"\nON g_nn={g}:", json.dumps({k: r[k] for k in
              ("com_rms_first", "com_rms_last", "com_rms_drift",
               "intra_rms_first", "intra_rms_last", "intra_rms_drift")}, indent=2))
    with open(os.path.join(os.path.dirname(__file__),
                           "nn_decompose_probe.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved nn_decompose_probe.json")
