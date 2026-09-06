"""
test_F356_eos_robustness.py
============================
F356 -- multi-EoS robustness of the F181/F184 tabulated-EoS neutron-star kernel
against CURRENT (2024) NICER/PSR mass-radius data.

F184 validated the F181 two-function TOV kernel against a physical band
(PSR J0740+6620 mass, ~NICER radius band) for ONE EoS family (SLy) only; APR
and MPA1 were in the machinery (Read et al. 2009 Table III) but were only
ever used for the *relative* stiffness-ordering check (F184 N2), never
checked against an absolute mass-radius band themselves.  This finding runs
all three published cores (SLy, APR4, MPA1) through the SAME absolute-band
check F184 ran on SLy alone, using the two tightest CURRENT measurements:

  PSR J0740+6620:  M = 2.08 +/- 0.07 Msun (Fonseca et al. 2021, arXiv:2104.00880,
                    radio Shapiro delay -- unchanged since F184);
                    R = 12.92 (+2.09/-1.13) km, 68% CI (Dittmann et al. 2024,
                    arXiv:2406.14467 -- UPDATED NICER+XMM data, supersedes the
                    looser band F184 cited; not to be confused with the companion
                    Salmi et al. 2024, arXiv:2406.14466, which reports a different
                    number and is not used here).
  PSR J0437-4715:   M = 1.418 +/- 0.037 Msun, R = 11.36 (+0.95/-0.63) km, 68% CI
                    (Choudhury et al. 2024, arXiv:2407.06789 -- the nearest,
                    brightest MSP; the TIGHTEST current NICER radius band, and
                    close enough to 1.4 Msun to compare almost directly to the
                    canonical R(1.4) figure of merit).

Two more Read et al. (2009) Table III entries -- WFF1 (soft) and MS1 (very
stiff, the literature's standard "too stiff" boundary case) -- are added to
`ns_eos.EOS_PARAMS` (this finding) specifically so the comparison has a
chance to FAIL: an absolute-band check that only ever runs on cores already
known to work would be vacuous.

Checks:
  E1  Physically-standard cores (SLy, APR4, MPA1): each has a turnover,
      M_max clears the PSR J0740 mass lower edge (2.01 Msun), and R at
      M=1.418 Msun falls inside the PSR J0437-4715 68% radius band
      [10.73, 12.31] km.
  E2  Bracket falsification: the two deliberately extreme cores (WFF1 soft,
      MS1 stiff) are each turned away by the SAME J0437-4715 radius band --
      i.e. the check in E1 has genuine discriminating power rather than
      passing everything it is given.  (Both still clear the J0740 mass
      floor -- it is the tight radius band that does the discriminating,
      consistent with the literature's read that modern NICER radii are the
      sharper current lever on EoS stiffness, not the pulsar masses.)
  E3  GR/TOV structure: every one of the five cores (the F184 three plus the
      two added here) shows a stable rising branch terminating in a
      maximum-mass turnover -- extends F184 N3 to WFF1/MS1.

Run:  python tests/findings/test_F356_eos_robustness.py
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np

THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from casim.engine.interactions import ns_eos as e                      # noqa: E402

STAMP = "2026-09-03 - 16:30"

# Current (2024) NICER/PSR mass-radius anchors -- see module docstring for citations.
J0740 = dict(M=2.08, M_lo=2.01, M_hi=2.15, R=12.92, R_lo=11.79, R_hi=15.01)
J0437 = dict(M=1.418, R=11.36, R_lo=10.73, R_hi=12.31)

STANDARD_CORES = ["SLy", "APR", "MPA1"]
EXTREME_CORES = ["WFF1", "MS1"]


def _scan(name, n=80):
    s = e.summarize(e.PiecewisePolytrope(name), n=n)
    c = s["curve"]; i = int(np.argmax(c["M_msun"]))
    Ms, Rs = c["M_msun"][:i+1], c["R_km"][:i+1]
    R1418 = float(np.interp(J0437["M"], Ms, Rs)) if Ms.max() >= J0437["M"] else None
    R208 = float(np.interp(J0740["M"], Ms, Rs)) if Ms.max() >= J0740["M"] else None
    return {
        "M_max": s["M_max"], "R_at_Mmax_km": s["R_at_Mmax_km"],
        "z_surf_at_Mmax": s["z_surf_at_Mmax"], "turnover": s["turnover"],
        "R_1418_km": R1418, "R_208_km": R208,
        "mass_ok_J0740": bool(s["M_max"] >= J0740["M_lo"]),
        "radius_ok_J0437": bool(R1418 is not None and J0437["R_lo"] <= R1418 <= J0437["R_hi"]),
        # only penalise J0740's radius band if the EoS actually reaches that mass
        "radius_ok_J0740": bool(R208 is None or J0740["R_lo"] <= R208 <= J0740["R_hi"]),
        "_curve_i_turnover": i, "_curve_n": len(c["M_msun"]),
        "_stable_rising": bool(np.all(np.diff(Ms) > 0)) if len(Ms) > 1 else False,
        "_falls_after": bool(i < len(c["M_msun"]) - 1 and c["M_msun"][-1] < s["M_max"]),
    }


def check_E1_standard_cores_absolute():
    rows = {name: _scan(name) for name in STANDARD_CORES}
    ok = all(rows[n]["turnover"] and rows[n]["mass_ok_J0740"] and rows[n]["radius_ok_J0437"]
             for n in STANDARD_CORES)
    return {"pass": bool(ok), "cores": rows,
            "band_J0740": J0740, "band_J0437": J0437}


def check_E2_bracket_falsification():
    rows = {name: _scan(name) for name in EXTREME_CORES}
    # the check has power iff BOTH extremes are excluded by the J0437 radius band
    # (mass floor alone does not discriminate at these central densities)
    excluded = all(not rows[n]["radius_ok_J0437"] for n in EXTREME_CORES)
    still_massive_enough = all(rows[n]["mass_ok_J0740"] for n in EXTREME_CORES)
    return {"pass": bool(excluded and still_massive_enough), "cores": rows,
            "note": "both WFF1 and MS1 clear the J0740 mass floor but are excluded "
                    "by the tighter J0437-4715 radius band -- the discriminator with "
                    "current data is the radius, not the mass"}


def check_E3_stable_branch_all_five():
    rows = {}
    ok = True
    for name in STANDARD_CORES + EXTREME_CORES:
        r = _scan(name)
        rows[name] = {"turnover": r["turnover"], "stable_rising": r["_stable_rising"],
                      "falls_after_turnover": r["_falls_after"],
                      "i_turnover": r["_curve_i_turnover"], "n": r["_curve_n"]}
        ok = ok and r["turnover"] and r["_stable_rising"] and r["_falls_after"]
    return {"pass": bool(ok), "cores": rows}


SUITE = [
    ("E1_standard_cores_absolute", check_E1_standard_cores_absolute,
     "SLy+APR4+MPA1 each: turnover, M_max>=J0740 floor, R(1.418)@J0437-4715 band"),
    ("E2_bracket_falsification", check_E2_bracket_falsification,
     "WFF1/MS1 both excluded by the J0437-4715 radius band -- check has real power"),
    ("E3_stable_branch_all_five", check_E3_stable_branch_all_five,
     "all five cores: stable rising branch + maximum-mass turnover"),
]


def run():
    results, t0 = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time(); print(f"[run] {name} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = desc
        results[name] = r; print(f"      pass={r.get('pass')}  ({r['_seconds']}s)", flush=True)
    n_pass = sum(1 for r in results.values() if r.get("pass"))
    return {"finding": "F356", "title": "Multi-EoS robustness of the F181/F184 kernel vs current NICER/PSR data",
            "timestamp": STAMP, "n_pass": n_pass, "n_total": len(SUITE),
            "results": results, "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    with open(os.path.join(ROOT, "test-results", "F356_eos_robustness.json"), "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ({out['seconds']}s)")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
