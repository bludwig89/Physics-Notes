"""
test_F199_amplitude_mode_stability.py
=====================================
F199 — does Omega_DM=0.26 fall out of the F198 amplitude-mode freeze-out once
the actual F73/F93 mass and couplings are used? No: stability fails first.

5 checks:
  H1  the F73 ELECTROWEAK radial mode is the observed 125 GeV Higgs (decays,
      lifetime << age) -> not dark matter.
  H2  the F93 E_g SECOND-SHELL amplitude mode couples to leptons (g_l=m_l/f, its
      defining role) and decays in ~1e-21 s -> not stable.
  H3  instability is generic across the EW-TeV range (all >30 orders below age).
  H4  therefore the F198 freeze-out WIMP window is MOOT (no stable relic).
  H5  a viable relic needs a conserved charge the E_g condensate lacks -> the DM
      identity must move to a sterile/topological/hidden sector.
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# Forks are loaded by bare name, not as package submodules;
# importing casim appends engine/forks/<sector>/ to sys.path.
import casim as _casim  # noqa: E402,F401
import gr_fork_F199_amplitude_mode_stability as F199   # noqa: E402
STAMP = "2026-06-30 - 20:40"

OUT = F199.run()


def check_H1_higgs_not_dm():
    h = OUT["two_modes_separated"]["electroweak_higgs"]
    ok = (not h["is_dark_matter"]) and h["lifetime_s"] < F199.AGE_UNIVERSE_S
    return {"pass": bool(ok), "mass_GeV": h["mass_GeV"], "lifetime_s": h["lifetime_s"],
            "note": "F73 EW radial mode = observed 125 GeV Higgs; decays -> not DM"}


def check_H2_eg_amplitude_unstable():
    e = OUT["two_modes_separated"]["Eg_amplitude_mode"]
    ok = (not e["stable_on_cosmo_time"]) and e["lifetime_s"] < 1e-15 and e["dominant_channel"] == "tau"
    return {"pass": bool(ok), "mass_GeV": e["mass_GeV"], "f_GeV": e["f_GeV"],
            "coupling_g_tau": e["coupling_g_tau"], "lifetime_s": e["lifetime_s"],
            "orders_below_cosmo": e["orders_below_cosmo"], "dominant_channel": e["dominant_channel"],
            "note": "E_g amplitude mode sets lepton masses -> couples g_l=m_l/f -> decays to tau+tau-"}


def check_H3_instability_generic():
    scan = OUT["instability_scan"]
    ok = all(s["orders_below_age"] > 30 for s in scan)
    return {"pass": bool(ok), "scan": scan,
            "note": "unstable across 10 GeV - 3 TeV: 38-40 orders below the age of the universe"}


def check_H4_freezeout_moot():
    f = OUT["freezeout_moot"]
    ok = (f["F198_found_WIMP_window"] and f["but_relic_must_be_stable"] and not f["stable"])
    return {"pass": bool(ok), "Eg_amplitude_lifetime_s": f["Eg_amplitude_lifetime_s"],
            "age_of_universe_s": f["age_of_universe_s"],
            "note": "abundance undefined for an unstable state -> F198 WIMP window unrealisable here"}


def check_H5_requires_conserved_charge():
    r = OUT["viable_relic_requirement"]
    ok = (not r["Eg_condensate_has_it"]) and len(r["model_native_candidates"]) >= 2
    return {"pass": bool(ok), "requirement": r["requirement"],
            "Eg_has_it": r["Eg_condensate_has_it"], "candidates": r["model_native_candidates"],
            "note": "DM identity moves out of the E_g sector to a conserved-charge sector"}


SUITE = [
    ("H1_higgs_not_dm", check_H1_higgs_not_dm, "EW radial mode = observed Higgs, decays"),
    ("H2_eg_amplitude_unstable", check_H2_eg_amplitude_unstable, "E_g amplitude mode decays to leptons (~1e-21 s)"),
    ("H3_instability_generic", check_H3_instability_generic, "unstable across EW-TeV (>30 orders)"),
    ("H4_freezeout_moot", check_H4_freezeout_moot, "freeze-out window moot without stability"),
    ("H5_requires_conserved_charge", check_H5_requires_conserved_charge, "DM needs a conserved charge E_g lacks"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F199",
            "title": "Amplitude-mode mass/channels from F73/F93: stability fails before abundance (E_g modes decay to leptons)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F199_amplitude_mode_stability_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
