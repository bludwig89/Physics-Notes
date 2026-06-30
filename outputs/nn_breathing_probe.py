#!/usr/bin/env python3
"""Probe: does the wired Tier-B NN one-boson-exchange binding stop the He
cluster 'breathing' reported in F195?  Runs live-quark He with nn_binding
ON and OFF and reports the nucleus-RMS drift + inter-nucleon COM separation
over the run.  Pure diagnostic; no asserts."""
import os, sys, json
_REPO = "/sessions/jolly-upbeat-meitner/mnt/Physics Notes"
for _p in (os.path.join(_REPO, "src"), os.path.join(_REPO, "ca-simulation")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import numpy as np
import casim  # noqa
from casim.engine import Simulation, LatticeSpec
from casim.engine.channel import build_channel
from casim.engine.observers import build_observer


def run(nn_binding, ticks=80, g_nn=0.012):
    fine = {"L": 12, "sigma": 0.5, "spread": 2.0, "live_quarks": True,
            "dt": 0.5, "mass": 0.9, "nn_binding": nn_binding, "g_nn": g_nn}
    coarse = {"L": 24, "m": 1.0, "k": 0.6, "dt": 0.4, "relax_steps": 300,
              "scf_iters": 5, "gs_every": 1, "hartree_every": 4}
    cfg = {"type": "element_atom", "name": "atom", "Z": 2, "N": 2, "b": 30000,
           "fine": fine, "coarse": coarse, "free": False}
    ch = build_channel(cfg)
    obs = [build_observer({"type": "atom_stability_readout", "every": 10}),
           build_observer({"type": "norm_conservation", "every": 10,
                           "channels": ["atom"]})]
    sim = Simulation(LatticeSpec(L=24, topology="bcc"), [ch], observers=obs,
                     seed=7)
    res = sim.run(ticks)
    rec = res["observers"]["atom_stability_readout"]["records"]
    drift = res["observers"]["norm_conservation"]["summary"]["max_rel_drift"]["atom"]
    nr = [r["nucleus_rms_fine"] for r in rec]
    # also pull the live nucleon COM spread directly from the channel state
    st = sim.states["atom"]
    coms = ch._nucleon_coms({nm: st[f"fine::{nm}"] for nm in ch._fine_names}) \
        if getattr(ch, "_nuc_groups", None) else []
    coms = np.array(coms)
    if len(coms) >= 2:
        # pairwise COM separations (fine cells)
        seps = [np.linalg.norm(coms[i] - coms[j])
                for i in range(len(coms)) for j in range(i + 1, len(coms))]
        com_rms = float(np.sqrt(np.mean((coms - coms.mean(0)) ** 2)))
    else:
        seps, com_rms = [], None
    meta = getattr(ch, "_nn_meta", None)
    return {
        "nn_binding": nn_binding, "g_nn": g_nn,
        "nuc_rms_first": nr[0], "nuc_rms_last": nr[-1],
        "nuc_rms_min": min(nr), "nuc_rms_max": max(nr),
        "nuc_rms_reldrift": (max(nr) - min(nr)) / nr[0],
        "net_charge_last": rec[-1]["net_charge"],
        "nuc_charge_last": rec[-1]["nuc_charge"],
        "norm_drift": drift,
        "final_com_rms_cells": com_rms,
        "final_pair_seps_cells": [round(s, 3) for s in seps],
        "nn_meta": meta,
        "nuc_rms_series": [round(x, 4) for x in nr],
    }


if __name__ == "__main__":
    out = {}
    print("=== NN binding OFF (control) ===")
    out["off"] = run(False)
    print(json.dumps(out["off"], indent=2))
    print("\n=== NN binding ON (default g_nn=0.012) ===")
    out["on"] = run(True)
    print(json.dumps(out["on"], indent=2))
    with open(os.path.join(os.path.dirname(__file__),
                           "nn_breathing_probe.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved nn_breathing_probe.json")
