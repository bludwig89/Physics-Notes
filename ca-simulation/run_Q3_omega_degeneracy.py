"""
run_Q3_omega_degeneracy.py — Q3: is the absolute g_omegaNN deuteron-observable?
================================================================================

Open-derivation Q3 (open-derivations-prompts-v2.md). F240 derived the omega
channel's sign, mass (m_omega=m_rho), and g_omegaNN/g_rhoNN=3 ratio (Tier-1), and
the vector-universality chain predicts g_omegaNN^2/4pi = 25.9 -- which OVERSHOOTS
(unbinds the deuteron). The NN-required value is a bracket [5.4, 11.1].

This runner tests WHY g_omegaNN cannot be pinned: the deuteron constrains only the
TOTAL short-range repulsion = (F113 quark-Pauli core, strength g_cm) + (omega). It
maps the (g_cm, g_omega*) binding valley: for each core strength g_cm, the omega
coupling g_omega* that binds the deuteron to E_b = 2.224 MeV. A flat valley =>
g_omega is degenerate with the core strength => not separately deuteron-observable.

Also reports the route-A prediction at the N-Delta-DERIVED core g_cm = 18.31 MeV.

Emits test-results/Q3_omega_degeneracy.json. Runtime ~1-2 min at N=500.
Run:  python3 run_Q3_omega_degeneracy.py
"""
import json
import os
import numpy as np
import ca_nuclear as nuc

TARGET = 2.224          # MeV, physical deuteron binding
N = 500                 # radial nodes (dense eigvalsh; lighter than 900 for speed)
R_MAX = 20.0
B = 0.55                # fm quark size
G_OMEGA_UNIV = 9.0 * (nuc.M_OMEGA_DEFAULT / (np.sqrt(2) * nuc.F_PI_DEFAULT)) ** 2 / (4 * np.pi)


def Eb(g_cm, gw):
    r = nuc.solve_deuteron(core="derived", b=B, g_cm=g_cm, sigma=True,
                           omega=(gw > 0), omega_g2_4pi=max(gw, 1e-9),
                           tensor=True, vectors=False, N=N, R_max=R_MAX)
    return r["E_b"]


def bisect_gw(g_cm, lo=0.01, hi=26.0, iters=34):
    flo = Eb(g_cm, lo) - TARGET
    fhi = Eb(g_cm, hi) - TARGET
    if flo * fhi > 0:
        return None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = Eb(g_cm, mid) - TARGET
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def main():
    out = {"target_Eb": TARGET, "g_omega_universality": G_OMEGA_UNIV,
           "g_cm_derived_NDelta": nuc.GCM_DEFAULT, "N": N, "valley": []}
    print(f"g_omega universality ceiling = {G_OMEGA_UNIV:.3f}")
    print(f"{'g_cm(MeV)':>10} {'core/derived':>13} {'g_w2/4pi*':>11} {'quench':>8}")
    for g_cm in [0.0, 4.58, 9.155, 13.73, 18.31, 22.89, 27.47]:
        gw = bisect_gw(g_cm)
        q = (gw / G_OMEGA_UNIV) if gw else None
        row = {"g_cm": g_cm, "core_frac": g_cm / nuc.GCM_DEFAULT,
               "g_omega_star": gw, "quench": q}
        out["valley"].append(row)
        gstr = f"{gw:.3f}" if gw else "unbound"
        qstr = f"{q:.3f}" if q else "  -  "
        print(f"{g_cm:>10.2f} {g_cm/nuc.GCM_DEFAULT:>13.2f} {gstr:>11} {qstr:>8}")

    # route A at the derived core, with eigenvectors for r_d / P_D
    gw = bisect_gw(nuc.GCM_DEFAULT)
    r = nuc.solve_deuteron(core="derived", b=B, g_cm=nuc.GCM_DEFAULT, sigma=True,
                           omega=True, omega_g2_4pi=gw, tensor=True, vectors=True,
                           N=N, R_max=R_MAX)
    out["routeA"] = {"g_cm": nuc.GCM_DEFAULT, "g_omega_star": gw,
                     "E_b": r["E_b"], "r_d": r["r_d"], "P_D": r["P_D"],
                     "quench": gw / G_OMEGA_UNIV}
    print(f"\nRoute A (N-Delta-derived core g_cm=18.31): g_w2/4pi*={gw:.3f} "
          f"E_b={r['E_b']:.3f} r_d={r['r_d']:.3f} P_D={r['P_D']*100:.1f}% "
          f"quench={gw/G_OMEGA_UNIV:.3f}")

    os.makedirs("../test-results", exist_ok=True)
    path = "../test-results/Q3_omega_degeneracy.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
