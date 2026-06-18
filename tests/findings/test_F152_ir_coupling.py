"""
F152 — The IR FACE of the strong coupling (the object F151-S5 split off).

F151 determined the UV face (V-scheme + a1 + q* band). This finding develops the
IR face: the gap-saturated effective coupling alpha_eff* ~ 0.39.

  J1  the IR value alpha_eff* = 0.376/0.411 ~ 0.39 (F151-S5 / F145), spread ~9%.
  J2  freeze scale = dual-Meissner gluon mass m_D; m_D/Lambda = O(1); finite
      alpha(0) -> saturating (decoupling) branch.
  J3  continuum grounding: alpha_hat(0)/pi=0.97 [CZBR], m_g=0.5(2) GeV; model
      gap matches; alpha_eff* ~ 0.39 in the continuum frozen-coupling range.
  J4  F150's lambda_6 belongs to this (IR) face, not the UV scheme constant.
  J5  IR face is NOT identical to the UV scheme constant (F151-S5); residual =
      the full crossover solve.
"""
import math

import ca_ir_coupling as irc


def run():
    results = {}
    rep = irc.report()

    # J1 — the IR coupling value
    v = rep["J1_ir_value"]
    j1 = (abs(v["alpha_eff_star_mD"] - 0.376) < 1e-6
          and abs(v["alpha_eff_star_mV"] - 0.411) < 1e-6
          and 0.35 < v["alpha_eff_star_mean"] < 0.42
          and v["spread_frac"] < 0.12)
    results["J1"] = dict(passed=bool(j1), mean=v["alpha_eff_star_mean"],
                         mD=v["alpha_eff_star_mD"], mV=v["alpha_eff_star_mV"])

    # J2 — saturating branch, m_D/Lambda = O(1), finite alpha(0)
    s = rep["J2_saturating_branch"]
    j2 = (s["on_saturating_branch"]
          and (0.3 < s["mD_over_Lambda"] < 5.0)
          and (0.3 < s["mg_continuum_over_Lambda"] < 5.0)
          and math.isfinite(s["alpha0_massive_1loop"]) and s["alpha0_massive_1loop"] > 0)
    results["J2"] = dict(passed=bool(j2), Lambda3_GeV=s["Lambda3_GeV"],
                         mD_over_Lambda=s["mD_over_Lambda"],
                         mg_over_Lambda=s["mg_continuum_over_Lambda"],
                         alpha0=s["alpha0_massive_1loop"])

    # J3 — continuum grounding
    g = rep["J3_continuum_grounding"]
    j3 = (abs(g["alpha_hat0_over_pi"] - 0.97) < 1e-9
          and g["model_gap_matches_continuum"]
          and g["alpha_eff_star_in_continuum_frozen_range"])
    results["J3"] = dict(passed=bool(j3), alpha_hat0_over_pi=g["alpha_hat0_over_pi"],
                         m_g_GeV=g["m_g_continuum_GeV"], model_mD_GeV=g["model_mD_scale_GeV"],
                         frozen_range=g["continuum_frozen_range"])

    # J4 — lambda_6 on the IR face
    l = rep["J4_lambda6"]
    j4 = (abs(l["lambda6_F150"] - 0.243) < 1e-9 and len(l["ir_face_owns"]) == 2)
    results["J4"] = dict(passed=bool(j4), ir_face_owns=l["ir_face_owns"])

    # J5 — distinct from UV face; residual present
    u = rep["J5_uv_relation"]
    j5 = (u["identical"] is False and bool(u["residual"]))
    results["J5"] = dict(passed=bool(j5), identical=u["identical"])

    n = sum(r["passed"] for r in results.values())
    results["summary"] = dict(passed=n, total=5, all_pass=n == 5)
    return results


if __name__ == "__main__":
    import json
    r = run()
    print(json.dumps(r, indent=2, default=str))
    assert all(r[k]["passed"] for k in ("J1", "J2", "J3", "J4", "J5")), "F152 checks failed"
    print("\nF152: 5/5 PASS")
