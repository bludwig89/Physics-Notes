"""
test_F62_dirac_gravity_fork.py — Dynamical Dirac CA on a curved background (D2)
+ linearized backreaction (D3a)
==============================================================================
Exercises `ca-simulation/forks/dirac_gravity_fork.py`, the time-domain
realisation of `ca-dirac-gravity-plan.md` Stages D2 and D3a.  Stage D1 (the
flat Dirac propagator, m=0 → Weyl) already lives in `ca_dirac.py`; the dispersion
identity for the static background already lives in `gr_fork_F46_dirac.py`
(F46/F50).  What is new and verified here is the **wave-packet evolution**:

  D1   flat m=0 regression — gravity stepper reduces to two decoupled exact
       Weyl walks, bit-for-bit (machine ε).
  D2a  Rindler free-fall (equivalence principle) — a rest packet falls toward
       LOW lapse at d²ξ/dt² → −a·c_lat² (c_lat²=1/2), independent of mass.
  D2b  dynamical gravitational redshift — a clock's chirality-oscillation
       frequency scales as √A; near/far ratio = 2·arcsin(√A·m) ratio.
  D2c  weak-Schwarzschild deflection — a fast packet bends toward the mass; the
       c_eff field carries the Einstein factor-2 bend (eikonal K ≈ 4); the
       dynamical centroid realises its own eikonal limit to ~25%.
  D3a  backreaction norm conservation — norm conserved while the self-sourced
       metric evolves underneath the field (each tick exactly unitary).
  D3a  self-redshift — the lapse is sourced from ρ via ∇²Φ=4πGρ (not an imported
       −GM/r); a probe clock deep in the field's OWN well runs slow, matching
       the rest-leg prediction (the backreaction loop closes).

Writes test-results/F62_dirac_gravity_fork.json and a markdown summary.

Run:
    python model-tests/test_F62_dirac_gravity_fork.py
"""

from __future__ import annotations

import json
import os
import sys
import time

THIS = os.path.dirname(__file__)
SIM = os.path.abspath(os.path.join(THIS, "..", "ca-simulation"))
FORKS = os.path.join(SIM, "forks")
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

import dirac_gravity_fork as dg          # noqa: E402

STAMP = "2026-05-30 - 15:30"

SUITE = [
    ("D1_flat_weyl_regression", dg.test_d1_flat_weyl_regression,
     "flat m=0 ⇒ two decoupled exact Weyl walks (machine ε)"),
    ("D2a_rindler_freefall", dg.test_rindler_freefall,
     "equivalence principle: rest packet falls toward low lapse at a·c_lat²"),
    ("D2b_dynamical_redshift", dg.test_dynamical_redshift,
     "clock frequency scales as √A (gravitational redshift)"),
    ("D2c_schwarzschild_deflection", dg.test_schwarzschild_deflection,
     "fast packet bends toward mass; eikonal K ≈ 4 (Einstein)"),
    ("D3a_backreaction_norm", dg.test_backreaction_norm,
     "norm conserved while self-sourced metric evolves"),
    ("D3a_self_redshift", dg.test_self_redshift,
     "probe clock slow in the field's own well (loop closes)"),
]


def run() -> dict:
    results, t_total = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time()
        print(f"[run] {name} ...", flush=True)
        r = fn()
        r["_seconds"] = round(time.time() - t, 2)
        r["_desc"] = desc
        results[name] = r
        print(f"      pass={r.get('pass')}  ({r['_seconds']}s)", flush=True)
    out = {
        "finding": "F62",
        "title": "Dynamical Dirac CA on a curved background (D2) + "
                 "linearized backreaction (D3a)",
        "timestamp": STAMP,
        "module": "ca-simulation/forks/dirac_gravity_fork.py",
        "n_pass": sum(1 for r in results.values() if r.get("pass")),
        "n_total": len(results),
        "total_seconds": round(time.time() - t_total, 2),
        "tests": results,
    }
    return out


def write_markdown(out: dict, path: str) -> None:
    L = []
    L.append(f"# {out['finding']} — {out['title']}")
    L.append("")
    L.append(f"_Generated {out['timestamp']} by "
             f"`model-tests/test_F62_dirac_gravity_fork.py`._")
    L.append("")
    L.append(f"**{out['n_pass']}/{out['n_total']} PASS** "
             f"(total {out['total_seconds']} s). "
             f"Module: `{out['module']}`.")
    L.append("")
    L.append("| Test | Pass | Key numbers |")
    L.append("|---|---|---|")
    t = out["tests"]
    def g(name, k, fmt="{:.4g}"):
        v = t[name].get(k)
        return fmt.format(v) if isinstance(v, (int, float)) else str(v)
    L.append(f"| D1 flat Weyl regression | {t['D1_flat_weyl_regression']['pass']} | "
             f"residual = {g('D1_flat_weyl_regression','residual_max_abs','{:.1e}')} |")
    L.append(f"| D2a Rindler free-fall | {t['D2a_rindler_freefall']['pass']} | "
             f"|g|/a·c_lat² = {g('D2a_rindler_freefall','coeff_ratio')}, "
             f"mass-universality spread = {g('D2a_rindler_freefall','universality_spread')}, "
             f"norm drift = {g('D2a_rindler_freefall','norm_drift','{:.1e}')} |")
    L.append(f"| D2b dynamical redshift | {t['D2b_dynamical_redshift']['pass']} | "
             f"ratio_meas = {g('D2b_dynamical_redshift','ratio_meas')}, "
             f"pred = {g('D2b_dynamical_redshift','ratio_pred_exact_arcsin')} |")
    L.append(f"| D2c Schwarzschild deflection | {t['D2c_schwarzschild_deflection']['pass']} | "
             f"K_eik = {g('D2c_schwarzschild_deflection','K_eikonal')}, "
             f"K_meas = {g('D2c_schwarzschild_deflection','K_meas')}, "
             f"meas/eik = {g('D2c_schwarzschild_deflection','ratio_meas_eik')} |")
    L.append(f"| D3a backreaction norm | {t['D3a_backreaction_norm']['pass']} | "
             f"norm drift = {g('D3a_backreaction_norm','norm_drift','{:.1e}')} |")
    L.append(f"| D3a self-redshift | {t['D3a_self_redshift']['pass']} | "
             f"A_near = {g('D3a_self_redshift','A_near')}, "
             f"A_far = {g('D3a_self_redshift','A_far')}, "
             f"ratio_meas = {g('D3a_self_redshift','ratio_meas')}, "
             f"pred = {g('D3a_self_redshift','ratio_pred_exact_arcsin')} |")
    L.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))


def main():
    out = run()
    res_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(res_dir, exist_ok=True)
    jpath = os.path.join(res_dir, "F62_dirac_gravity_fork.json")
    mpath = os.path.join(res_dir, "F62_dirac_gravity_fork.md")
    with open(jpath, "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    write_markdown(out, mpath)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  "
          f"({out['total_seconds']}s)")
    print(f"Wrote {jpath}")
    print(f"Wrote {mpath}")
    return out


if __name__ == "__main__":
    main()
