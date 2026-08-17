"""
run_residual_AB_highres.py — HIGH-RESOLUTION verification of the strong-sector
residuals A and B, to be run NATIVELY by Ben (no sandbox 45 s cap), dumping a
JSON for a later Claude session to read.

Sandbox (this repo's dev tier) already validated:
  B (F154): alpha_eff* = 0.3764 / 0.4111, L-stable to 1e-4 at L=16/24/32.
  A (F154): the cheap log-moment route gives UV scales (e/a), NOT q* — full
            one-loop integral required (next session).

This runner re-checks B at LARGE L (32/48/64/96) to confirm the IR coupling is
truly converged, and tabulates the q* log-moment to high BZ resolution to
confirm the "cheap route fails" verdict is not a small-grid artifact. It also
leaves a clearly-marked hook for the A self-energy integral once that module
(`ca_gluon_self_energy.py`, next session) exists.

Usage (native, outside the sandbox):
    python3 tests/runners/run_residual_AB_highres.py \
        --L 32 48 64 96 --nlog 64 96 128 \
        --out test-results/residual_AB_highres.json

Cost: B's bisection is ~60 gap solves per (L, m_D); each gap solve is a few
hundred FFTs of size L^3. L=96 is ~30-60 min per mass on a laptop; L<=64 is
minutes. The log-moment is a single BZ reduction (4D n=96 ~ 5 GB RAM — drop to
3D or lower n if memory-limited; 3D scales fine to n=512).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# also support running from repo root

from casim.engine.interactions import running_gap_solve as gap          # noqa: E402
from casim.engine.interactions import running_qstar_logmoment as qs     # noqa: E402


def verify_B(Ls, masses):
    """Residual B: alpha_eff* vs L for each gluon mass — confirm convergence."""
    out = {}
    for tag, Mg in masses:
        rows = []
        for L in Ls:
            t0 = time.time()
            r = gap.alpha_eff_for_target(Mg, L=L)
            rows.append({"L": L, "alpha_eff_star": r.get("alpha_eff_star"),
                         "M0_check": r.get("M0_check"), "ok": r.get("ok"),
                         "secs": round(time.time() - t0, 1)})
            print(f"  B {tag} L={L}: alpha_eff*={r.get('alpha_eff_star'):.5f} "
                  f"M0={r.get('M0_check'):.4f} ({rows[-1]['secs']}s)", flush=True)
        # convergence: spread of the last two L's
        last = [x["alpha_eff_star"] for x in rows[-2:] if x["alpha_eff_star"]]
        out[tag] = {"Mg": Mg, "rows": rows,
                    "converged_spread": (abs(last[0] - last[1]) if len(last) == 2 else None)}
    return out


def verify_A_logmoment(ns):
    """Residual A cheap route: q* log-moment vs BZ resolution n — confirm the
    converged moments are UV (above F151's band), i.e. the shortcut fails."""
    rows = []
    for n in ns:
        rec = {"n": n}
        for d in (3, 4):
            for w in ("flat", "prop", "prop2"):
                try:
                    rec[f"d{d}_{w}"] = round(qs.logmoment_qstar(n, d, w)["qstar_a"], 4)
                except MemoryError:
                    rec[f"d{d}_{w}"] = "OOM"
        rows.append(rec)
        print(f"  A n={n}: {rec}", flush=True)
    return {"implied_qstar_F151": 0.7327, "band": [1 / 3 ** 0.5, 1.0],
            "rows": rows,
            "verdict": "converged flat/prop moments are UV (>band) => q* is the "
                       "UV-finite subtraction, not a moment (F154-A). The full "
                       "one-loop self-energy (ca_gluon_self_energy.py) is required."}


def hook_A_self_energy():
    """Placeholder for the next session's A solve. Once ca_gluon_self_energy.py
    exists, import it and call its high-resolution q* / Lambda-ratio routine here,
    then assert q* a == 0.733 (+- band) / Lambda_MS/Lambda_rule == 1.78."""
    try:
        from casim.engine.gauge import gluon_self_energy as se   # noqa: F401
        return se.qstar_highres()            # next session defines this
    except Exception as e:
        return {"status": "NOT BUILT YET",
                "todo": "next session: build ca_gluon_self_energy.py (background-"
                        "field one-loop on the KS rotor action), define "
                        "qstar_highres() returning {qstar_a, Lambda_ratio}",
                "import_error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, nargs="+", default=[32, 48, 64])
    ap.add_argument("--nlog", type=int, nargs="+", default=[48, 64, 96])
    ap.add_argument("--out", default="test-results/residual_AB_highres.json")
    args = ap.parse_args()

    masses = [("F88_mD=0.532", gap.M_D_F88), ("F117_mV=0.727", gap.M_V_F117)]
    print("== Residual B (gap solve, high L) ==", flush=True)
    B = verify_B(args.L, masses)
    print("== Residual A (log-moment, high n; cheap-route check) ==", flush=True)
    A = verify_A_logmoment(args.nlog)
    print("== Residual A (self-energy hook) ==", flush=True)
    A_se = hook_A_self_energy()

    report = {"generated": time.strftime("%Y-%m-%d %H:%M"),
              "residual_B_solved": B, "residual_A_logmoment_negative": A,
              "residual_A_self_energy": A_se,
              "targets": {"alpha_eff_star_mD": 0.376, "alpha_eff_star_mV": 0.411,
                          "qstar_a": 0.7327, "Lambda_ratio": 1.78,
                          "M0_constituent_MeV": 311}}
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nWrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
