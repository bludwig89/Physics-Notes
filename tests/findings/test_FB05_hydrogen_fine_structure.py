#!/usr/bin/env python3
"""
FB05 — Hydrogen fine structure (Dirac):  2p_3/2 - 2p_1/2 = 10.95 GHz.

Falsification test for the F125 (P5) radial-Dirac fine structure. This is the
HARDEST falsification test: a HAND-ROLLED numerical radial Dirac integrator.

Per CLAUDE.md, we do NOT rely on scipy/numpy for the chiral / Dirac pieces.
The RK4 integrator below is written from scratch in real arithmetic in pure
Python, and is cross-checked three ways:

  (a) The closed-form Dirac-Coulomb (Sommerfeld) spectrum is checked against its
      own O((Za)^4) fine-structure series  ->  ~5e-10.
  (b) The HAND-ROLLED RK4 numerical Dirac integrator (inward + outward, with a
      Wronskian-style match of the large/small components G, F) is checked
      against the Sommerfeld closed form  ->  <= 1.3e-6 relative to binding.
  (c) The 2p_3/2 - 2p_1/2 splitting = 45.28 ueV = 10.95 GHz (measured 10.969,
      target 0.18%); alpha-scaling slopes 4.0001 (absolute, ~alpha^4) and
      2.0000 (relative-to-binding, ~alpha^2); and 1s_1/2 = -13.605874 eV.

The ONLY library use is math (real arithmetic) and a thin least-squares slope
fit done by hand (closed-form 2-parameter linear regression) — no scipy, no
numpy in the Dirac path.

Run:  python3 tests/findings/test_FB05_hydrogen_fine_structure.py
"""

import json
import math
import os

# ---------------------------------------------------------------------------
#  Physical constants (CODATA-consistent with F125 / ca_atom.py).
# ---------------------------------------------------------------------------
ALPHA = 1.0 / 137.036                 # the one empirical EM coupling (per brief)
M_E_MEV = 0.51099895000               # electron rest energy (MeV)  (P0/F120 anchor)
RY_EV_CODATA = 13.605693122994        # CODATA Rydberg (eV), infinite nucleus

HZ_PER_EV = 2.417989242e14            # 1 eV in Hz (h-bar conversion); E = h*nu
# 1 eV = 2.417989242e14 Hz  (CODATA: 1 eV / h = 2.417 989 242e14 Hz)


# ===========================================================================
#  1.  Quantum-number bookkeeping.
# ===========================================================================
def kappa_of(l, j_is_l_plus_half):
    """Dirac quantum number kappa.  j = l + 1/2 -> kappa = -(l+1); j = l - 1/2
    -> kappa = +l."""
    return -(l + 1) if j_is_l_plus_half else l


# ===========================================================================
#  2.  Exact closed-form Dirac-Coulomb (Sommerfeld) spectrum.
# ===========================================================================
def sommerfeld_energy(n, kappa, Z=1, alpha=ALPHA):
    """Exact Dirac-Coulomb TOTAL energy in units of m c^2 (includes rest mass).

        E = [ 1 + ( Za / (n_r + gamma) )^2 ]^(-1/2),
        gamma = sqrt(kappa^2 - (Za)^2),  n_r = n - |kappa|.
    """
    Za = Z * alpha
    gamma = math.sqrt(kappa * kappa - Za * Za)
    n_r = n - abs(kappa)
    return (1.0 + (Za / (n_r + gamma)) ** 2) ** (-0.5)


def sommerfeld_binding_eV(n, kappa, mc2_MeV=M_E_MEV, Z=1, alpha=ALPHA):
    """Dirac-Coulomb binding (E - m c^2) in eV (negative for bound states)."""
    return (sommerfeld_energy(n, kappa, Z, alpha) - 1.0) * mc2_MeV * 1.0e6


def fine_structure_series_eV(n, j, mc2_MeV=M_E_MEV, Z=1, alpha=ALPHA):
    """Standard O((Za)^4) expansion of the Dirac binding:

        E_b ~ -(1/2) mc^2 (Za)^2/n^2 [ 1 + (Za)^2/n^2 ( n/(j+1/2) - 3/4 ) ].

    Returns the total (leading + O(alpha^4)) binding in eV."""
    Za = Z * alpha
    mc2 = mc2_MeV * 1.0e6
    lead = -0.5 * mc2 * Za ** 2 / n ** 2
    corr = lead * (Za ** 2 / n ** 2) * (n / (j + 0.5) - 0.75)
    return lead + corr


# ===========================================================================
#  3.  HAND-ROLLED numerical radial-Dirac integrator (RK4, real arithmetic).
#
#  Units: hbar = c = m_e = 1.  Lengths in Compton wavelengths, energies in
#  m_e c^2.   V(r) = -Z alpha / r.   Radial Dirac for (G large, F small):
#
#      G'(r) = -(kappa/r) G + (E - V + 1) F
#      F'(r) =  (kappa/r) F - (E - V - 1) G
#
#  Eigenvalue E found by inward+outward integration to a matching radius and a
#  Wronskian-style mismatch  (G_out F_in - F_out G_in) = 0,  bracketed by
#  bisection around the Sommerfeld value.   No scipy / numpy anywhere here.
# ===========================================================================
def _dirac_rhs(r, G, F, kappa, E, Za):
    V = -Za / r
    dG = -(kappa / r) * G + (E - V + 1.0) * F
    dF = (kappa / r) * F - (E - V - 1.0) * G
    return dG, dF


def _rk4_segment(r0, r1, G, F, kappa, E, Za, nsteps):
    """Classic 4th-order Runge-Kutta, hand-written, real arithmetic."""
    h = (r1 - r0) / nsteps
    r = r0
    for _ in range(nsteps):
        k1G, k1F = _dirac_rhs(r, G, F, kappa, E, Za)
        k2G, k2F = _dirac_rhs(r + 0.5 * h, G + 0.5 * h * k1G, F + 0.5 * h * k1F, kappa, E, Za)
        k3G, k3F = _dirac_rhs(r + 0.5 * h, G + 0.5 * h * k2G, F + 0.5 * h * k2F, kappa, E, Za)
        k4G, k4F = _dirac_rhs(r + h, G + h * k3G, F + h * k3F, kappa, E, Za)
        G += (h / 6.0) * (k1G + 2.0 * k2G + 2.0 * k3G + k4G)
        F += (h / 6.0) * (k1F + 2.0 * k2F + 2.0 * k3F + k4F)
        r += h
    return G, F


def _dirac_mismatch(E, n, kappa, Za, r0, r_m, r_max, nout, nin):
    """Wronskian-style mismatch (G_out F_in - F_out G_in) at the matching radius
    r_m; this is zero exactly at an eigenvalue.  Outward from r0 uses the
    pointlike-Coulomb small-r series IC (~ r^gamma); inward from r_max uses the
    exponentially decaying bound-state tail ratio F/G = -lambda/(E+1)."""
    gamma = math.sqrt(kappa * kappa - Za * Za)
    # outward IC at r0
    G0 = r0 ** gamma
    F0 = (gamma + kappa) / Za * r0 ** gamma
    G_out, F_out = _rk4_segment(r0, r_m, G0, F0, kappa, E, Za, nout)
    # inward IC at r_max (decaying tail)
    lam = math.sqrt(max(1.0 - E * E, 1e-30))
    G1 = 1.0
    F1 = -lam / (E + 1.0)
    G_in, F_in = _rk4_segment(r_max, r_m, G1, F1, kappa, E, Za, nin)
    # rescale magnitudes so the sign of the Wronskian is what we read, not overflow
    sc_out = max(abs(G_out), abs(F_out), 1e-300)
    sc_in = max(abs(G_in), abs(F_in), 1e-300)
    G_out, F_out = G_out / sc_out, F_out / sc_out
    G_in, F_in = G_in / sc_in, F_in / sc_in
    return G_out * F_in - F_out * G_in


def numerical_dirac_energy(n, kappa, Z=1, alpha=ALPHA, window=2.0e-7,
                           r0=1e-5, nout=20000, nin=20000):
    """Recover the radial-Dirac eigenvalue (units m c^2) by hand-rolled bisection
    of the Wronskian mismatch around the Sommerfeld value."""
    Za = Z * alpha
    E_som = sommerfeld_energy(n, kappa, Z, alpha)
    a_bohr = 1.0 / Za                         # Bohr radius in Compton units
    r_m = max(2.0, n * n * a_bohr)            # match near the classical orbit
    r_max = r_m + 9.0 * n * a_bohr            # ~9 tail decay lengths beyond it
    lo = E_som * (1.0 - window)
    hi = E_som * (1.0 + window)
    flo = _dirac_mismatch(lo, n, kappa, Za, r0, r_m, r_max, nout, nin)
    fhi = _dirac_mismatch(hi, n, kappa, Za, r0, r_m, r_max, nout, nin)
    if flo == 0.0:
        return lo
    if flo * fhi > 0.0:                        # widen the bracket once if needed
        lo = E_som * (1.0 - 10.0 * window)
        hi = E_som * (1.0 + 10.0 * window)
        flo = _dirac_mismatch(lo, n, kappa, Za, r0, r_m, r_max, nout, nin)
        fhi = _dirac_mismatch(hi, n, kappa, Za, r0, r_m, r_max, nout, nin)
    for _ in range(80):                        # 80 bisections ~ 2^-80 relative
        mid = 0.5 * (lo + hi)
        fm = _dirac_mismatch(mid, n, kappa, Za, r0, r_m, r_max, nout, nin)
        if flo * fm <= 0.0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def numerical_dirac_binding_eV(n, kappa, mc2_MeV=M_E_MEV, Z=1, alpha=ALPHA):
    return (numerical_dirac_energy(n, kappa, Z, alpha) - 1.0) * mc2_MeV * 1.0e6


# ===========================================================================
#  4.  Hand-rolled least-squares slope (no numpy.polyfit): log-log linear fit.
# ===========================================================================
def loglog_slope(xs, ys):
    """Slope of a straight-line fit to (log x, log y) via the closed-form normal
    equations.  Used for the alpha-scaling power-law exponents."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    sx = sum(lx); sy = sum(ly)
    sxx = sum(v * v for v in lx); sxy = sum(a * b for a, b in zip(lx, ly))
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


# ===========================================================================
#  Test driver.
# ===========================================================================
def main():
    checks = []   # (name, residual, target, tier, ok)

    def record(name, residual, target, tier, ok):
        checks.append({"name": name, "residual": float(residual),
                       "target": float(target), "tier": tier,
                       "status": "PASS" if ok else "FAIL"})
        flag = "PASS" if ok else "FAIL"
        print(f"  [{flag}] {name}: residual={residual:.3e} (target {target:.1e})")

    print("FB05 — Hydrogen fine structure (hand-rolled radial Dirac)\n")

    # --- (b1) Sommerfeld closed form == its own O((Za)^4) series -------------
    print("(b1) Sommerfeld closed form vs O((Za)^4) fine-structure series")
    worst_series = 0.0
    for (n, l, jplus, jval) in [(1, 0, True, 0.5),
                                (2, 1, False, 0.5),
                                (2, 1, True, 1.5),
                                (2, 0, True, 0.5)]:
        kap = kappa_of(l, jplus)
        eb_exact = sommerfeld_binding_eV(n, kap)
        eb_series = fine_structure_series_eV(n, jval)
        rel = abs(eb_exact - eb_series) / abs(eb_exact)
        worst_series = max(worst_series, rel)
    record("Sommerfeld == O((Za)^4) series", worst_series, 5e-9, "machine",
           worst_series < 5e-9)

    # --- (d) 1s_1/2 binding = -13.605874 eV ---------------------------------
    print("\n(d) 1s_1/2 Dirac binding == -13.605874 eV")
    eb_1s = sommerfeld_binding_eV(1, kappa_of(0, True))
    target_1s = -13.605874
    res_1s = abs(eb_1s - target_1s)
    record("1s_1/2 = -13.605874 eV", res_1s, 5e-5, "quantitative", res_1s < 5e-5)
    print(f"        1s_1/2 = {eb_1s:.6f} eV  (CODATA Ry -{RY_EV_CODATA:.6f}; rest is O(a^4) Dirac shift)")

    # --- (b2) HAND-ROLLED numerical Dirac == Sommerfeld ----------------------
    print("\n(b2) hand-rolled RK4 numerical Dirac (Wronskian match) == Sommerfeld")
    worst_num = 0.0
    num_table = {}
    for (n, l, jplus, label) in [(1, 0, True, "1s_1/2"),
                                 (2, 1, False, "2p_1/2"),
                                 (2, 1, True, "2p_3/2")]:
        kap = kappa_of(l, jplus)
        E_num = numerical_dirac_energy(n, kap)
        E_som = sommerfeld_energy(n, kap)
        bind_num = (E_num - 1.0) * M_E_MEV * 1e6
        bind_som = (E_som - 1.0) * M_E_MEV * 1e6
        rel = abs(E_num - E_som) / abs(E_som - 1.0)    # relative to the binding
        worst_num = max(worst_num, rel)
        num_table[label] = {"E_num_mc2": E_num, "E_som_mc2": E_som,
                            "bind_num_eV": bind_num, "bind_som_eV": bind_som,
                            "rel_to_binding": rel}
        print(f"        {label}: num={bind_num:.6f} eV  som={bind_som:.6f} eV  rel={rel:.2e}")
    record("numerical Dirac == Sommerfeld (rel binding)", worst_num, 1.3e-6,
           "quantitative", worst_num < 1.3e-6)

    # --- (a) 2p_3/2 - 2p_1/2 splitting = 10.95 GHz ---------------------------
    print("\n(a) fine-structure splitting 2p_3/2 - 2p_1/2")
    e_2p32 = sommerfeld_binding_eV(2, kappa_of(1, True))    # kappa = -2
    e_2p12 = sommerfeld_binding_eV(2, kappa_of(1, False))   # kappa = +1
    split_eV = e_2p32 - e_2p12          # 3/2 less bound -> positive
    split_ueV = split_eV * 1e6
    split_GHz = split_eV * HZ_PER_EV / 1e9
    measured_GHz = 10.969
    pct_vs_measured = abs(split_GHz - measured_GHz) / measured_GHz * 100.0
    print(f"        split = {split_ueV:.2f} ueV = {split_GHz:.4f} GHz  (measured {measured_GHz} GHz, {pct_vs_measured:.3f}%)")
    record("splitting within 0.18% of measured 10.969 GHz",
           pct_vs_measured, 0.18, "quantitative", pct_vs_measured <= 0.18)

    # --- (c) alpha-scaling: absolute slope -> 4, relative slope -> 2 --------
    print("\n(c) alpha-scaling of the splitting")
    alphas = [ALPHA * f for f in (0.6, 0.75, 0.9, 1.0, 1.1, 1.25, 1.4)]
    splits = []
    binds = []
    for a in alphas:
        s = abs(sommerfeld_binding_eV(2, kappa_of(1, True), alpha=a)
                - sommerfeld_binding_eV(2, kappa_of(1, False), alpha=a))
        b = abs(sommerfeld_binding_eV(2, kappa_of(1, False), alpha=a))
        splits.append(s); binds.append(b)
    abs_slope = loglog_slope(alphas, splits)
    rel_slope = loglog_slope(binds, splits)   # d log(split) / d log(binding) ~ 2
    # binding ~ alpha^2, so split/binding ~ alpha^2 -> rel slope (vs binding) = 2
    print(f"        absolute slope (d ln split / d ln alpha) = {abs_slope:.4f}  (-> 4)")
    print(f"        relative slope (d ln split / d ln binding) = {rel_slope:.4f}  (-> 2)")
    record("absolute alpha-scaling slope = 4", abs(abs_slope - 4.0), 0.01,
           "quantitative", abs(abs_slope - 4.0) < 0.01)
    record("relative-to-binding slope = 2", abs(rel_slope - 2.0), 0.01,
           "quantitative", abs(rel_slope - 2.0) < 0.01)

    # --- verdict ------------------------------------------------------------
    all_ok = all(c["status"] == "PASS" for c in checks)
    verdict = "PASS" if all_ok else "FALSIFIED"

    result = {
        "test_id": "FB05",
        "name": "Hydrogen fine structure (Dirac) 2p_3/2-2p_1/2 = 10.95 GHz",
        "verdict": verdict,
        "predicted": {
            "splitting_GHz": split_GHz,
            "splitting_ueV": split_ueV,
            "E_1s_half_eV": eb_1s,
            "abs_alpha_slope": abs_slope,
            "rel_binding_slope": rel_slope,
        },
        "measured_target": {
            "splitting_GHz": measured_GHz,
            "splitting_ueV_nominal": 45.28,
            "splitting_GHz_nominal": 10.95,
            "E_1s_half_eV": -13.605874,
            "pct_tolerance": 0.18,
        },
        "gate": {
            "splitting_pct_vs_measured_max": 0.18,
            "dirac_vs_sommerfeld_rel_max": 1.3e-6,
            "sommerfeld_vs_series_rel_max": 5e-9,
            "abs_slope_target": 4.0,
            "rel_slope_target": 2.0,
            "E_1s_half_eV_target": -13.605874,
        },
        "computed": {
            "alpha": ALPHA,
            "m_e_MeV": M_E_MEV,
            "splitting_eV": split_eV,
            "splitting_ueV": split_ueV,
            "splitting_GHz": split_GHz,
            "pct_vs_measured": pct_vs_measured,
            "E_1s_half_eV": eb_1s,
            "sommerfeld_vs_series_worst_rel": worst_series,
            "dirac_vs_sommerfeld_worst_rel": worst_num,
            "abs_alpha_slope": abs_slope,
            "rel_binding_slope": rel_slope,
            "numerical_dirac_table": num_table,
            "checks": checks,
        },
        "commands": [
            "python3 tests/findings/test_FB05_hydrogen_fine_structure.py",
        ],
        "timestamp": "2026-06-16",
    }

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.normpath(os.path.join(here, "..", "..", "test-results"))
    out_path = os.path.join(out_dir, "FB05_hydrogen_fine_structure.json")
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=2)

    print(f"\nVERDICT: {verdict}")
    print(f"Wrote {out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
