"""[HISTORICAL BASELINE 2026-06-29 — ledger S4-F178-full-stress-energy]

  NOTE:
    N3/N4/N5 energy-only departures are no longer predictions, but the finding
    records them as the DIAGNOSIS that forced F178, so the file is the
    standing exclusion record. N1/N2 are live canon.

  See docs/theory/supersessions.yaml for the full record.

test_F174_stellar_overlay.py  --  GR-TOV vs dielectric-model neutron stars.

Closes the open observable of FC09/F173: solve each theory's own hydrostatic
structure for a representative EoS and compare mass-radius + surface-redshift
curves against NICER.

Checks
------
N1  Newtonian limit: as central density -> 0 the two theories' (M, R) converge
    (validates the solver and F173's "null in the solar system").
N2  GR-TOV reproduces a realistic neutron star: a maximum-mass turnover at
    ~2 Msun (the EoS is tuned to PSR J0740+6620, M = 2.08 +/- 0.07 Msun).
N3  The dielectric model (literal F106, energy-only) has NO maximum-mass
    turnover in the NS range and overpredicts the mass at fixed central density
    by a large factor -- a qualitative failure to reproduce neutron stars.
N4  At a fixed gravitational mass (1.4 Msun) the model predicts a substantially
    larger radius and different surface redshift than GR.
N5  Surface-redshift offset (model - GR) is positive and grows with compactness
    (same sign as the F173 central-redshift discriminator).

Run:  python tests/findings/test_F174_stellar_overlay.py
"""
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))
import ca_stellar as st

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "test-results", "F174_stellar_overlay.json")
results = {}

# Gamma=2 polytrope tuned so GR M_max ~ 2.0-2.1 Msun (J0740 scale)
EOS = st.Polytrope(K=250.0, Gamma=2.0)
RHO_C = np.geomspace(3e-5, 1.6e-2, 40)

gr = st.mass_radius_curve(RHO_C, "gr", EOS)
md = st.mass_radius_curve(RHO_C, "model", EOS)


def check_N1():
    lowrc = [1e-6, 1e-5, 1e-4]
    ratios = []
    for rc in lowrc:
        Rg, Mg, _ = st.integrate_star(rc, "gr", EOS, h=2e-3)
        Rm, Mm, _ = st.integrate_star(rc, "model", EOS, h=2e-3)
        ratios.append({"rho_c": rc, "compactness_GR": Mg / Rg,
                       "M_ratio": Mm / Mg, "R_ratio": Rm / Rg})
    # convergence: ratio -> 1 as compactness -> 0 (monotone toward unity)
    converges = (abs(ratios[0]["M_ratio"] - 1.0) < 5e-3
                 and ratios[0]["M_ratio"] < ratios[-1]["M_ratio"])
    results["N1_newtonian_convergence"] = {
        "rows": ratios, "M_ratio_at_lowest": ratios[0]["M_ratio"],
        "PASS": converges}


def check_N2():
    mm = st.max_mass(gr)
    results["N2_gr_realistic"] = {
        "GR_M_max_msun": mm["M_max_msun"], "GR_R_at_max_km": mm["R_at_max_km"],
        "turnover_present": mm["turnover_present"],
        "anchor": "PSR J0740+6620 M=2.08+/-0.07 Msun, R~12.4 km",
        "PASS": mm["turnover_present"] and 1.8 < mm["M_max_msun"] < 2.4}


def check_N3():
    mm_md = st.max_mass(md)
    # overprediction factor at a representative NS central density
    rc = 2e-3
    _, Mg, _ = st.integrate_star(rc, "gr", EOS)
    _, Mm, _ = st.integrate_star(rc, "model", EOS)
    results["N3_model_no_turnover"] = {
        "model_turnover_in_range": mm_md["turnover_present"],
        "model_M_at_top_of_range_msun": float(md["M_msun"][-1]),
        "mass_overprediction_factor_at_rhoc_2e-3": Mm / Mg,
        "PASS": (not mm_md["turnover_present"]) and (Mm / Mg > 1.5)}


def check_N4():
    g14 = st.at_fixed_mass(gr, 1.4)
    m14 = st.at_fixed_mass(md, 1.4)
    # radius at the J0740 mass (2.08 Msun): GR sits near its turnover; the model
    # reaches it on its rising branch at much lower density / larger radius
    g208 = st.at_fixed_mass(gr, 2.08)
    m208 = st.at_fixed_mass(md, 2.08)
    results["N4_fixed_mass_comparison"] = {
        "at_1.4_msun": {"GR": g14, "model": m14,
                        "R_diff_km": (m14["R_km"] - g14["R_km"]) if (g14 and m14) else None,
                        "z_diff": (m14["z_surf"] - g14["z_surf"]) if (g14 and m14) else None},
        "at_2.08_msun_J0740": {"GR_R_km": g208["R_km"] if g208 else None,
                               "model_R_km": m208["R_km"] if m208 else None,
                               "NICER_R_km": "12.4 +/- 0.75 (Miller 2021)"},
        "PASS": bool(g14 and m14 and (m14["R_km"] - g14["R_km"]) > 0.5)}


def check_N5():
    # redshift offset vs compactness along the GR rising branch
    i = int(np.argmax(gr["M_msun"]))
    rows = []
    for j in range(0, i + 1, max(1, i // 6)):
        comp = gr["M_msun"][j] * st.MSUN_KM / gr["R_km"][j]
        rows.append({"compactness": float(comp),
                     "z_GR": float(gr["z_surf"][j]), "z_model": float(md["z_surf"][j]),
                     "z_offset": float(md["z_surf"][j] - gr["z_surf"][j])})
    grows = rows[-1]["z_offset"] > rows[0]["z_offset"] > -1e-6
    results["N5_redshift_offset_grows"] = {"rows": rows, "PASS": grows}


def _np(o):
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    raise TypeError(repr(o))


if __name__ == "__main__":
    check_N1(); check_N2(); check_N3(); check_N4(); check_N5()
    n_pass = sum(1 for v in results.values() if v.get("PASS"))
    summary = {"n_checks": len(results), "n_pass": n_pass, "all_pass": n_pass == len(results)}
    overlay = {"eos": "Gamma=2 polytrope, K=250 km^2 (tuned to J0740)",
               "gr": {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in gr.items()},
               "model": {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in md.items()}}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"summary": summary, "checks": results, "overlay_curves": overlay}, f, indent=2, default=_np)
    print(json.dumps({"summary": summary, "checks": results}, indent=2, default=_np))
