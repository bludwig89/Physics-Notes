"""
F145 — Route C of the QCD calibration block: the NJL coupling ghat = G Lambda^2
as an induced coupling — exact Fierz, momentum-resolved kernel, and the
composition with Route A's running.

Checks (zero free parameters; g_s^2 = 1/4 from F144, m_D measured F88/F117):

  N1 (exact)    Full 24-dim Fierz of one-gluon exchange: c = 2/9 in ALL FOUR
                chiral channels (machine-exact) — the induced interaction is
                exactly U(2)_L x U(2)_R symmetric (the F77 form is FORCED);
                corrects F116 NJ4's 4/9 (colour-only factor).  Plus the Fock
                kernel identity sum gam^mu T^a . gam_mu T^a = 4 C_F = 16/3.

  N2 (machine)  Contact-limit anchor: analytic R = g_contact <1/sqrt(K)>_BZ
                equals the power-iteration eigenvalue (<1e-12); the induced
                gap equation reduces to the F116 NJ2 lattice machinery.

  N3 (decisive) Bare-coupling no-go: at g_s^2 = 1/4 the momentum-resolved
                kernel gives R = G/G_c ~ 0.07-0.10 << 1 at the measured m_D —
                the bare rule coupling cannot break chiral symmetry; the F117
                dielectric enhancement (eps_c down to 1/4) cannot rescue it
                (R < 0.25).  NJ4's near-criticality was contact x (4/9).

  N4 (structural) Route A x Route C: with the running g^2(mu(q)) at the
                exchange virtuality (IR-frozen, 0.40-0.65 GeV scan;
                Lambda3 in {F144 1-loop, FLAG}), R = 2.6-15 >> 1 — chiral
                symmetry breaking is GUARANTEED by the RG growth.  Criticality
                inequality alpha_eff >= alpha_crit(M_g) = 1/(4 pi R0) with
                alpha_crit ~ 0.20-0.27.

  N5 (residual) The F77 fit G/G_c = 1.277 corresponds to alpha_eff = 0.26-0.34
                — inside the model's running band at the chiral scale and
                bracketed by N3/N4.  The exact ghat awaits the nonperturbative
                IR coupling: the same single scale-setting residual as
                F124 §5 / F144 A4.

numpy only; ~60 s (power iterations on 32^3).
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "..", "ca-simulation")))
import ca_njl_induced_coupling as RC  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
results = {}

rep = RC.route_c_report(L=32)


def check_N1():
    f, k = rep["fierz"], rep["fock_identity"]
    ok = (f["max_dev_from_2/9"] < 1e-13
          and f["chiral_symmetric_spread"] < 1e-13
          and k["dev"] < 1e-12 and k["offdiag"] < 1e-12)
    return ok, {"fierz": f, "fock": k}


def check_N2():
    a1, a2 = rep["anchor_F88"], rep["anchor_F117"]
    ok = a1["dev"] < 1e-10 and a2["dev"] < 1e-10
    return ok, {"anchor_F88": a1, "anchor_F117": a2}


def check_N3():
    b1, b2 = rep["F88_mD=0.532"], rep["F117_mV=0.727"]
    ok = (b1["R_resolved_bare"] < 0.5 and b2["R_resolved_bare"] < 0.5
          and b1["R_resolved_bare_epsc=0.25"] < 1.0
          and b2["R_resolved_bare_epsc=0.25"] < 1.0)
    return ok, {t: {k: rep[t][k] for k in
                    ("R_contact_bare", "R_resolved_bare",
                     "R_resolved_bare_epsc=0.52", "R_resolved_bare_epsc=0.25",
                     "ghat_resolved_bare")}
                for t in ("F88_mD=0.532", "F117_mV=0.727")}


def check_N4():
    b1, b2 = rep["F88_mD=0.532"], rep["F117_mV=0.727"]
    ok = (b1["running_R_range"][0] > 1.0 and b2["running_R_range"][0] > 1.0
          and 0.1 < b1["alpha_crit"] < 0.5 and 0.1 < b2["alpha_crit"] < 0.5)
    return ok, {t: {"running_R_range": rep[t]["running_R_range"],
                    "alpha_crit": rep[t]["alpha_crit"],
                    "ghat_running_range": rep[t]["ghat_running_range"]}
                for t in ("F88_mD=0.532", "F117_mV=0.727")}


def check_N5():
    b1, b2 = rep["F88_mD=0.532"], rep["F117_mV=0.727"]
    # the fitted point must sit between the bare no-go and the running band,
    # and its alpha_eff must lie in the perturbative-to-chiral window
    ok = True
    for b in (b1, b2):
        ok &= b["R_resolved_bare"] < RC.GGC_F77 < b["running_R_range"][1]
        ok &= 0.15 < b["alpha_eff_for_F77_fit"] < 0.6
    return ok, {"alpha_eff_F88": b1["alpha_eff_for_F77_fit"],
                "alpha_eff_F117": b2["alpha_eff_for_F77_fit"],
                "targets": rep["targets"],
                "note": "fit bracketed: bare 0.07-0.10 < 1.277 < running "
                        "2.6-15; residual = the nonperturbative IR coupling "
                        "(same scale-setting constant as F124/F144-A4)"}


n_pass = 0
for name, fn in (("N1", check_N1), ("N2", check_N2), ("N3", check_N3),
                 ("N4", check_N4), ("N5", check_N5)):
    ok, detail = fn()
    results[name] = {"PASS": bool(ok), "detail": detail}
    n_pass += int(ok)

results["ALL_PASS"] = all(results[k]["PASS"]
                          for k in ("N1", "N2", "N3", "N4", "N5"))
results["report"] = rep
results["CALIBRATION_NOTE"] = (
    "Inputs: g_s^2=1/4 DERIVED (F144 A1); m_D measured (F88 CC8 0.532 / F117 "
    "0.727, MC at beta=1.8); Lambda_NJL=651.5 MeV is the F116 chiral-scale "
    "ruler; running from F144 (1-loop nf=3, Lambda3 = chain 272 MeV / FLAG "
    "343 MeV sensitivity). Targets only: F77 fit G/G_c=1.277, ghat=2.10. "
    "Open: the nonperturbative IR coupling (one number, shared with "
    "F124/F144-A4); the m_D beta-dependence inherits F88's honest scope.")

out = os.path.join(ROOT, "test-results", "F145_route_c_induced_njl.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=float)

print("=" * 72)
print("F145 — Route C: the induced NJL coupling (exact Fierz + criticality)")
print("=" * 72)
fz = rep["fierz"]
print(f"  Fierz: c = 2/9 in all four chiral channels "
      f"(dev {fz['max_dev_from_2/9']:.1e}); Fock = 4C_F = 16/3 exact")
for t in ("F88_mD=0.532", "F117_mV=0.727"):
    b = rep[t]
    print(f"  [{t}] bare: contact {b['R_contact_bare']:.3f} -> resolved "
          f"{b['R_resolved_bare']:.3f} (no-go) | running R = "
          f"{b['running_R_range'][0]:.2f}..{b['running_R_range'][1]:.2f} "
          f"(chi-SB guaranteed) | alpha_crit {b['alpha_crit']:.3f}")
print(f"  F77 fit G/G_c = {RC.GGC_F77} <=> alpha_eff = "
      f"{rep['F88_mD=0.532']['alpha_eff_for_F77_fit']:.3f} (F88) / "
      f"{rep['F117_mV=0.727']['alpha_eff_for_F77_fit']:.3f} (F117)")
for k in ("N1", "N2", "N3", "N4", "N5"):
    print(f"  {k}: {'PASS' if results[k]['PASS'] else 'FAIL'}")
print(f"  ALL_PASS = {results['ALL_PASS']}")
