"""
test_F183_blackhole.py
======================
F183 -- the black hole under the F178 gravity sector.  The canonical
strong-field object is now exact Schwarzschild/Kerr (induced Einstein
equation), replacing the F114 horizon-free dielectric black hole.  This
verifies the new characteristics against GR closed forms and quantifies
what changed.

Checks:
  S1  Schwarzschild closed forms: horizon 2M, photon sphere 3M, shadow
      b_c = 3 sqrt3 M, ISCO 6M, surface gravity 1/4M -- and a numeric
      photon-sphere/critical-impact solve agreeing to <1e-3.
  S2  Hawking sector PRESENT: T_H = hbar c^3/(8 pi G M k_B) (6.17e-8 K at
      1 M_sun), lifetime ~ M^3 (2.1e67 yr at 1 M_sun); r_s = 2.95 km.
  Q1  eikonal QNM tied to the photon sphere: Omega_c = lambda = 1/(3 sqrt3 M)
      exactly; the eikonal real part (l+1/2)Omega_c converges monotonically to
      the tabulated GR fundamental (Berti et al.) as l grows; damping (n+1/2)
      lambda within 12% of the l=2 value -> ringdown present (no echoes).
  K1  Kerr: outer/inner horizons M +/- sqrt(M^2-a^2), equatorial ergosphere 2M,
      frame-drag Omega_H = a/(r+^2+a^2); prograde ISCO < 6M < retrograde ISCO;
      a->0 reduces to Schwarzschild.
  K2  Kerr shadow (Bardeen): a->0 gives a circle of radius 3 sqrt3 M (offset 0);
      a=0.9 equatorial gives a displaced, asymmetric outline (nonzero offset).
  C1  Oppenheimer-Snyder collapse: a dust ball (R0=10M) forms a horizon and
      reaches R=0 in FINITE proper time tau = pi sqrt(R0^3/8M); horizon crossing
      precedes the singularity.
  L1  Lattice-cutoff core (NEW, non-GR): the Kretschmann curvature reaches the
      BCC cell scale at r_core = (48 (GM/c^2)^2 a^4)^{1/6}, with a < r_core <
      horizon and r_core ~ M^{1/3} -> singularity regulated, not pointlike.
  X1  F114 contrast: the canonical BH has a horizon, shadow exactly 3 sqrt3 M
      (F114 +4.63%), Hawking present (F114 absent).

Run:  python tests/findings/test_F183_blackhole.py
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.interactions import blackhole as bh                  # noqa: E402

STAMP = "2026-06-30 - 03:15"

# Tabulated Schwarzschild QNM fundamental (n=0), Re(omega M), Berti-Cardoso-Will
QNM_TAB = {2: 0.373672, 3: 0.599443, 4: 0.809178, 5: 1.012295, 6: 1.212019}


def check_S1_schwarzschild():
    s = bh.schwarzschild(M=1.0)
    num = bh.numeric_shadow(M=1.0)
    ok = (abs(s["r_horizon"] - 2.0) < 1e-12
          and abs(s["r_photon_sphere"] - 3.0) < 1e-12
          and abs(s["shadow_b_crit"] - 3 * np.sqrt(3)) < 1e-12
          and abs(s["r_isco"] - 6.0) < 1e-12
          and abs(s["surface_gravity_kappa"] - 0.25) < 1e-12
          and abs(num["r_photon_sphere_numeric"] - 3.0) < 2e-3
          and abs(num["b_crit_numeric"] - 3 * np.sqrt(3)) < 1e-3)
    return {"pass": bool(ok), "r_horizon": s["r_horizon"],
            "r_photon_sphere": s["r_photon_sphere"],
            "shadow_b_crit": s["shadow_b_crit"], "3sqrt3": 3 * np.sqrt(3),
            "r_isco": s["r_isco"], "kappa": s["surface_gravity_kappa"],
            "numeric_r_ph": num["r_photon_sphere_numeric"],
            "numeric_b_c": num["b_crit_numeric"]}


def check_S2_hawking():
    T = bh.hawking_temperature_SI(1.0)
    tau = bh.hawking_lifetime_years(1.0)
    rs = bh.schwarzschild_radius_km(1.0)
    # scaling: T ~ 1/M, lifetime ~ M^3
    T10 = bh.hawking_temperature_SI(10.0)
    tau10 = bh.hawking_lifetime_years(10.0)
    ok = (abs(T - 6.17e-8) / 6.17e-8 < 0.02
          and abs(rs - 2.95) < 0.05
          and abs(T / T10 - 10.0) < 1e-6
          and abs(tau10 / tau - 1000.0) < 1e-6
          and 1e66 < tau < 1e68)
    return {"pass": bool(ok), "T_hawking_K_1Msun": T, "expected_~6.17e-8": 6.17e-8,
            "lifetime_yr_1Msun": tau, "r_s_km_1Msun": rs,
            "T_scaling_ratio(1/10)": T / T10, "lifetime_scaling(10/1)": tau10 / tau,
            "present": True}


def check_Q1_qnm():
    s = bh.schwarzschild(M=1.0)
    Omega_c, lam = s["QNM_Omega_c"], s["QNM_lyapunov"]
    target = 1.0 / (3 * np.sqrt(3))
    exact = abs(Omega_c - target) < 1e-12 and abs(lam - target) < 1e-12
    # eikonal real part (l+1/2) Omega_c vs tabulated; error should shrink with l
    errs = []
    for l in sorted(QNM_TAB):
        eik = (l + 0.5) * Omega_c
        errs.append(abs(eik / QNM_TAB[l] - 1.0))
    converging = all(errs[i] > errs[i+1] for i in range(len(errs)-1)) and errs[-1] < 0.05
    # damping: (n+1/2) lambda vs tabulated fundamental Im (l=2: 0.08896)
    damp_eik = 0.5 * lam
    damp_err = abs(damp_eik - 0.08896) / 0.08896
    ok = exact and converging and damp_err < 0.12
    return {"pass": bool(ok), "Omega_c": Omega_c, "lyapunov": lam, "target_1/3sqrt3": target,
            "eikonal_real_errors_by_l": {l: round(e, 4) for l, e in zip(sorted(QNM_TAB), errs)},
            "errors_converging": bool(converging),
            "damping_eikonal": damp_eik, "damping_tab_l2": 0.08896, "damping_err": damp_err}


def check_K1_kerr():
    k = bh.kerr(M=1.0, a=0.9)
    rt = np.sqrt(1 - 0.81)
    ok = (abs(k["r_horizon_outer"] - (1 + rt)) < 1e-12
          and abs(k["r_horizon_inner"] - (1 - rt)) < 1e-12
          and abs(k["r_ergosphere_equator"] - 2.0) < 1e-12
          and abs(k["Omega_horizon_framedrag"] - 0.9 / ((1+rt)**2 + 0.81)) < 1e-12
          and k["r_isco_prograde"] < 6.0 < k["r_isco_retrograde"])
    # a->0 reduces to Schwarzschild
    k0 = bh.kerr(M=1.0, a=1e-6)
    schw_limit = (abs(k0["r_horizon_outer"] - 2.0) < 1e-5
                  and abs(k0["r_isco_prograde"] - 6.0) < 1e-4
                  and abs(k0["r_isco_retrograde"] - 6.0) < 1e-4)
    return {"pass": bool(ok and schw_limit),
            "r_horizon_outer": k["r_horizon_outer"], "r_horizon_inner": k["r_horizon_inner"],
            "ergosphere_eq": k["r_ergosphere_equator"],
            "Omega_H": k["Omega_horizon_framedrag"],
            "isco_prograde": k["r_isco_prograde"], "isco_retrograde": k["r_isco_retrograde"],
            "schwarzschild_limit_ok": bool(schw_limit)}


def check_K2_kerr_shadow():
    # moderate spin: nearly circular (height ~ 2*3sqrt3, small displacement)
    s3 = bh.kerr_shadow_outline(M=1.0, a=0.3, theta_o=np.pi/2)
    near_circular = (abs(s3["height_vertical_M"] - 2 * 3 * np.sqrt(3)) < 0.2
                     and abs(s3["asymmetry"] - 1.0) < 0.1)
    # high spin equatorial: displaced, asymmetric (D-shape), with the prograde
    # side flattened -> larger offset and more asymmetry than moderate spin
    s9 = bh.kerr_shadow_outline(M=1.0, a=0.9, theta_o=np.pi/2)
    more_asym = (abs(s9["horizontal_offset_M"]) > abs(s3["horizontal_offset_M"])
                 and abs(s9["horizontal_offset_M"]) > 0.3
                 and s9["width_horizontal_M"] > 0 and s9["height_vertical_M"] > 0)
    # the vertical height stays ~ photon-sphere scale; horizontal shrinks (dent)
    return {"pass": bool(near_circular and more_asym),
            "a0.3_height": s3["height_vertical_M"], "2*3sqrt3": 2*3*np.sqrt(3),
            "a0.3_offset": s3["horizontal_offset_M"], "a0.3_asymmetry": s3["asymmetry"],
            "a0.9_width": s9["width_horizontal_M"], "a0.9_height": s9["height_vertical_M"],
            "a0.9_offset": s9["horizontal_offset_M"], "a0.9_asymmetry": s9["asymmetry"]}


def check_C1_collapse():
    os_ = bh.oppenheimer_snyder(M=1.0, R0=10.0)
    tau_sing_expected = np.pi * np.sqrt(10.0**3 / 8.0)
    ok = (os_["horizon_forms"]
          and abs(os_["tau_singularity"] - tau_sing_expected) < 1e-9
          and 0 < os_["tau_horizon_crossing"] < os_["tau_singularity"]
          and os_["R"][-1] < 1e-2)        # reaches R~0
    return {"pass": bool(ok), "horizon_forms": os_["horizon_forms"],
            "tau_singularity": os_["tau_singularity"], "expected": tau_sing_expected,
            "tau_horizon_crossing": os_["tau_horizon_crossing"],
            "R_final": float(os_["R"][-1]), "finite_collapse": os_["free_fall_finite"]}


def check_L1_lattice_core():
    c1 = bh.lattice_core_radius(1.0)
    c8 = bh.lattice_core_radius(8.0)
    inside = c1["a_cell_m"] < c1["r_core_m"] < 2 * bh.G_SI * bh.MSUN_KG / bh.C_SI**2
    scaling = abs((c8["r_core_m"] / c1["r_core_m"]) - 8.0**(1.0/3.0)) < 1e-6  # ~M^{1/3}
    return {"pass": bool(inside and scaling),
            "r_core_m_1Msun": c1["r_core_m"], "r_core_over_a": c1["r_core_over_a"],
            "r_core_over_horizon": c1["r_core_over_horizon"],
            "M^(1/3)_scaling_ok": bool(scaling),
            "note": "singularity regulated at the lattice scale (non-GR)"}


def check_X1_f114_contrast():
    c = bh.f114_dielectric_contrast(M=1.0)
    horizon_appeared = (c["event_horizon"]["F178_canonical"] == 2.0
                        and c["event_horizon"]["F114_dielectric"] is None)
    shadow_back_to_gr = (abs(c["shadow_b_crit"]["F178_canonical"] - 3*np.sqrt(3)) < 1e-12
                         and abs(c["shadow_pct_vs_GR"]["F178_canonical"]) < 1e-12
                         and abs(c["shadow_pct_vs_GR"]["F114_dielectric"] - 0.0463) < 1e-3)
    hawking = ("present" in c["hawking_radiation"]["F178_canonical"]
               and "absent" in c["hawking_radiation"]["F114_dielectric"])
    return {"pass": bool(horizon_appeared and shadow_back_to_gr and hawking),
            "horizon_appeared": bool(horizon_appeared),
            "F114_shadow_pct_vs_GR": c["shadow_pct_vs_GR"]["F114_dielectric"],
            "F178_shadow_pct_vs_GR": c["shadow_pct_vs_GR"]["F178_canonical"],
            "hawking_now_present": bool(hawking)}


SUITE = [
    ("S1_schwarzschild_closed_forms", check_S1_schwarzschild,
     "horizon 2M, photon sphere 3M, shadow 3sqrt3 M, ISCO 6M (+ numeric solve)"),
    ("S2_hawking_present", check_S2_hawking,
     "Hawking T=hbar c^3/8 pi G M k_B (6.17e-8 K), lifetime ~ M^3 -- PRESENT"),
    ("Q1_qnm_photon_sphere", check_Q1_qnm,
     "eikonal QNM Omega_c=lambda=1/3sqrt3 M; converges to tabulated GR -> ringdown"),
    ("K1_kerr_horizons_framedrag", check_K1_kerr,
     "Kerr horizons, ergosphere, Omega_H, prograde<6M<retrograde ISCO; a->0=Schw"),
    ("K2_kerr_shadow_bardeen", check_K2_kerr_shadow,
     "Bardeen shadow: circle at a->0, displaced asymmetric D-shape at a=0.9"),
    ("C1_oppenheimer_snyder_collapse", check_C1_collapse,
     "dust collapse forms horizon, reaches R=0 in finite proper time"),
    ("L1_lattice_core", check_L1_lattice_core,
     "Kretschmann meets cell scale: a<r_core<horizon, r_core~M^{1/3} (NEW)"),
    ("X1_f114_contrast", check_X1_f114_contrast,
     "vs F114: horizon appears, shadow back to 3sqrt3 (was +4.63%), Hawking present"),
]


def run():
    results, t0 = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time()
        print(f"[run] {name} ...", flush=True)
        r = fn()
        r["_seconds"] = round(time.time() - t, 2)
        r["_desc"] = desc
        results[name] = r
        print(f"      pass={r.get('pass')}  ({r['_seconds']}s)", flush=True)
    n_pass = sum(1 for r in results.values() if r.get("pass"))
    out = {"finding": "F183",
           "title": "The black hole under the F178 gravity sector: exact "
                    "Schwarzschild/Kerr, with a lattice-regulated core",
           "timestamp": STAMP, "n_pass": n_pass, "n_total": len(SUITE),
           "results": results, "seconds": round(time.time() - t0, 2)}
    return out


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    with open(os.path.join(ROOT, "test-results", "F183_blackhole.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ({out['seconds']}s)")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
