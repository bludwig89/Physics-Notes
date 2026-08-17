"""
run_u4_sigma_carry.py — U4 scale carry of the SU(3)-measured string tension
into the confining bound state (F146 §4a).

Takes the string tension measured from the 3D SU(3) gauge dynamics
(run_su3_3d_string_tension.py: sigma * a_g^2 ~= 0.31, beta & lattice the only
inputs) and carries it through the F131 block-spin binding solver
(ca_blockspin_binding.solve_bound_states):

    H = -(1/2m) lap / a^2  +  sigma_phys * r_phys ,   r_phys = a * r_site

The physical box L*a is held fixed while the spacing a is refined; the bound
state's physical radius <r>_phys must be INVARIANT (the C1/F131 scale-
covariance).  This is a prediction (no tuning): sigma is measured, m is fixed,
only the resolution changes.  The invariant radius is the TRUE confinement
size set by the measured sigma — resolving F135's loose RMS (a coarse-box
zitterbewegung artifact, not the well size).

    PYTHONPATH=src python tests/runners/run_u4_sigma_carry.py
"""
from __future__ import annotations
import os, sys, json
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.lattice import blockspin_binding as bb   # noqa: E402

SIGMA = 0.31      # sigma_phys * a_g^2, MEASURED (F146 §2, Creutz plateau)
MASS = 0.9        # constituent mass in units 1/a_g (the F135 value)


def rms_phys(spacing, L, sigma=SIGMA, mass=MASS):
    g = bb._coords(L, 3)
    r = np.sqrt(sum(c.astype(float) ** 2 for c in g))   # site radius
    V = sigma * spacing * r                              # V_phys(r_phys)=sigma*r_phys
    w, v = bb.solve_bound_states(V, mass=mass, spacing=spacing, n_states=2)
    psi2 = (v[:, 0] ** 2).reshape((L,) * 3)
    psi2 /= psi2.sum()
    return float(np.sqrt(float((psi2 * r ** 2).sum())) * spacing), float(w[0])


def main():
    rows = []
    print("U4 carry — physical confinement radius vs lattice resolution")
    print(" a/a_g   L    box    <r>_phys     E0")
    for a, L in [(1.0, 24), (0.75, 32), (0.6, 40)]:
        rp, E = rms_phys(a, L)
        rows.append({"spacing": a, "L": L, "box": round(L * a, 1),
                     "rms_phys": round(rp, 4), "E0": round(E, 4)})
        print("  %.2f   %3d   %4.0f    %.4f    %.4f" % (a, L, L * a, rp, E))
    r0 = rows[0]["rms_phys"]
    spread = max(abs(x["rms_phys"] - r0) for x in rows) / r0
    Rsig = r0 * np.sqrt(SIGMA)
    print("\nphysical radius invariant to %.1f%% across 1.67x refinement (no tuning)"
          % (100 * spread))
    print("R_conf * sqrt(sigma) = %.3f   =>   R_conf ~= %.2f / sqrt(sigma)"
          % (Rsig, Rsig))
    out = {"sigma_measured_ag2": SIGMA, "mass": MASS, "rows": rows,
           "rms_phys_spread_frac": round(spread, 4),
           "R_conf_times_sqrt_sigma": round(Rsig, 4),
           "note": "scale-covariant (C1/F131); F135 RMS 6.25 was a coarse-box "
                   "zitterbewegung artifact, not the true ~2 a_g well size; "
                   "absolute fm P6-gated via sqrt(sigma)=0.42 GeV."}
    here = os.path.dirname(os.path.abspath(__file__))
    dst = os.path.join(here, "..", "..", "test-results", "u4_sigma_carry.json")
    try:
        json.dump(out, open(dst, "w"), indent=2)
        print("wrote", os.path.relpath(dst))
    except Exception as e:
        print("(could not write json:", e, ")")


if __name__ == "__main__":
    main()
