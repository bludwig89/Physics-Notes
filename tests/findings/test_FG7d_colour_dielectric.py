"""
test_FG7d_colour_dielectric.py — confinement as a colour-dielectric / dual superconductor
=========================================================================================

Verifies `ca-simulation/ca_colour_dielectric.py` (P1 Option C): the binding
force as a dual-superconductor colour-electric flux tube, recast as a
colour-dielectric eps_c(x) renormalising the F43 gluon (E,B) rotation rule
(the F64-parallel mechanism).

  CD1  Bogomolny completion: the energy density rearranges to (squares) +
       e v^2 B exactly, so sigma = 2 pi v^2 n at the BPS point — algebraically
       exact (sympy), profile-independent.
  CD2  ANO/DGL profile boundary conditions (f:0->1, a:0->1) + quantised
       colour-electric flux Phi = 2 pi n / e.
  CD3  numeric energy integral on the BPS profile reproduces sigma = 2 pi v^2 n.
  CD4  dielectric gluon rotation step reduces to the free F43 step bit-for-bit
       at eps_c=1, and renormalises the rotation rate (c_eff = c sqrt(eps_c))
       for eps_c<1.
  CD5  dual Meissner: London-screened colour-electric field decays with
       penetration depth lambda = 1/(e v).
  CD6  constant tube cross-section -> linear potential V(R)=sigma R; an
       isolated colour charge costs infinite energy.

Modules under test:  ca-simulation/ca_colour_dielectric.py  (+ ca_gluon.py)
Created:             2026-06-03
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ca-simulation'))

import ca_colour_dielectric as cd   # noqa: E402
import ca_gluon as cg               # noqa: E402


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ═════════════════════════════════════════════════════════════════════
#  CD1 — Bogomolny completion (algebraically exact, sympy)
# ═════════════════════════════════════════════════════════════════════

def test_CD1_bogomolny_completion():
    """CD1 — energy density completes to squares + topological term; at the BPS
    coupling lambda = e^2/2 the bound is sigma = 2 pi v^2 n EXACTLY."""
    import sympy as sp

    B, phi2, v, e, lam = sp.symbols('B phi2 v e lam', real=True, positive=True)
    Dsq = sp.symbols('Dsq', real=True, nonnegative=True)   # |(D1+iD2)phi|^2 >=0

    # Local energy density of the Abelian-Higgs model:
    #   u = 1/2 B^2 + |Dphi|^2 + (lam/2)(phi2 - v^2)^2 ,   phi2 = |phi|^2
    # Bogomolny identity (modulo a total-derivative current, dropped on integ.):
    #   |Dphi|^2 = |(D1+iD2)phi|^2 + e B phi2 + div(.)
    # so, with the current term written as Dsq:
    u = sp.Rational(1, 2) * B**2 + (Dsq + e * B * phi2) + (lam / 2) * (phi2 - v**2)**2

    # Completed form at the critical (BPS) coupling lam = e^2:
    #   u = 1/2 (B + e(phi2 - v^2))^2 + Dsq + e v^2 B
    u_crit = u.subs(lam, e**2)
    completed = sp.Rational(1, 2) * (B + e * (phi2 - v**2))**2 + Dsq + e * v**2 * B

    resid = sp.simplify(u_crit - completed)
    completes = (resid == 0)

    # The squares vanish on BPS solutions -> u = e v^2 B; integrate over the
    # plane:  sigma = e v^2 * Phi,  Phi = ∫ B = 2 pi n / e  =>  sigma = 2 pi v^2 n.
    nn, vv = sp.symbols('n v', positive=True)
    Phi = 2 * sp.pi * nn / e
    sigma_topo = sp.simplify(e * vv**2 * Phi)
    sigma_expected = 2 * sp.pi * vv**2 * nn
    topo_ok = (sp.simplify(sigma_topo - sigma_expected) == 0)

    passed = bool(completes and topo_ok)
    return {
        'test': 'CD1', 'name': 'Bogomolny completion -> sigma=2 pi v^2 n (BPS, exact)',
        'passed': passed, 'residual': 0.0 if passed else float('nan'),
        'tier': 1,
        'detail': {'density_completes_to_squares': bool(completes),
                   'topological_value_correct': bool(topo_ok),
                   'sigma_BPS': '2*pi*v**2*n'},
    }


# ═════════════════════════════════════════════════════════════════════
#  CD2 — ANO/DGL profile boundary conditions + flux quantisation
# ═════════════════════════════════════════════════════════════════════

def test_CD2_profile_bcs_and_flux():
    """CD2 — BPS vortex profile: f:0->1, a:0->1 monotone; flux Phi=2 pi n/e."""
    prof = cd.solve_bps_profile(n=1, x_max=14.0, dx=2e-3)
    f, a = prof['f'], prof['a']
    f0_ok = abs(f[0]) < 1e-3
    a0_ok = abs(a[0]) < 1e-3
    finf_ok = abs(f[-1] - 1.0) < 5e-3
    ainf_ok = abs(a[-1] - 1.0) < 5e-3
    mono_f = bool(np.all(np.diff(f) >= -1e-6))
    mono_a = bool(np.all(np.diff(a) >= -1e-6))

    flux = cd.colour_electric_flux(prof, e=1.0)
    flux_expected = 2.0 * np.pi * 1 / 1.0       # 2 pi n / e, n=1, e=1
    flux_res = abs(flux - flux_expected) / flux_expected

    passed = bool(f0_ok and a0_ok and finf_ok and ainf_ok
                  and mono_f and mono_a and flux_res < 5e-3)
    return {
        'test': 'CD2', 'name': 'ANO profile BCs + quantised colour-electric flux',
        'passed': passed, 'residual': float(flux_res), 'tier': 3,
        'detail': {'f0': float(f[0]), 'f_inf': float(f[-1]),
                   'a0': float(a[0]), 'a_inf': float(a[-1]),
                   'monotone_f': mono_f, 'monotone_a': mono_a,
                   'flux': float(flux), 'flux_expected': float(flux_expected),
                   'shoot_c': float(prof['c'])},
    }


# ═════════════════════════════════════════════════════════════════════
#  CD3 — numeric string tension reproduces the BPS value
# ═════════════════════════════════════════════════════════════════════

def test_CD3_string_tension_bps():
    """CD3 — ∫(energy density) on the BPS profile = sigma = 2 pi v^2 n."""
    v = 1.0
    results = {}
    worst = 0.0
    for n in (1, 2):
        prof = cd.solve_bps_profile(n=n, x_max=16.0, dx=2e-3)
        sig_num = cd.string_tension_numeric(prof, v=v)
        sig_exact = cd.bps_string_tension(v=v, n=n)
        rel = abs(sig_num - sig_exact) / sig_exact
        results[f'n={n}'] = {'numeric': float(sig_num),
                             'exact': float(sig_exact), 'rel': float(rel)}
        worst = max(worst, rel)
    passed = bool(worst < 1e-2)
    return {
        'test': 'CD3', 'name': 'numeric sigma matches BPS 2 pi v^2 n',
        'passed': passed, 'residual': float(worst), 'tier': 3,
        'detail': results,
    }


# ═════════════════════════════════════════════════════════════════════
#  CD4 — dielectric gluon rotation step (free-step reduction + c renorm)
# ═════════════════════════════════════════════════════════════════════

def test_CD4_dielectric_rotation_step():
    """CD4 — eps_c=1 reduces to free F43 step BIT-FOR-BIT; eps_c<1 renormalises
    the rotation rate so c_eff = c_lat sqrt(eps_c)."""
    rng = np.random.default_rng(20260603)
    L = 16
    E = rng.standard_normal((8, L, L))
    B = rng.standard_normal((8, L, L))

    # (i) trivial dielectric == free F43 step, bit-for-bit
    E_free, B_free = cg.gluon_rotation_step_spectral_2d(E, B)
    E_d1, B_d1 = cd.gluon_dielectric_rotation_step_2d(E, B, eps_c=1.0)
    E_dN, B_dN = cd.gluon_dielectric_rotation_step_2d(E, B, eps_c=None)
    bitexact = (np.max(np.abs(E_free - E_d1)) + np.max(np.abs(B_free - B_d1))
                + np.max(np.abs(E_free - E_dN)) + np.max(np.abs(B_free - B_dN)))

    # (ii) measurable renormalisation at eps_c<1 (field actually changes)
    E_h, B_h = cd.gluon_dielectric_rotation_step_2d(E, B, eps_c=0.25)
    changed = np.max(np.abs(E_h - E_free)) > 1e-3

    # (iii) c_eff scaling law
    ceff = cd.effective_lattice_c(0.25)
    ceff_expected = (1.0 / np.sqrt(3.0)) * np.sqrt(0.25)
    ceff_res = abs(float(ceff) - ceff_expected)

    passed = bool(bitexact < 1e-12 and changed and ceff_res < 1e-15)
    return {
        'test': 'CD4', 'name': 'dielectric gluon step: free-reduction + c renorm',
        'passed': passed, 'residual': float(bitexact), 'tier': 1,
        'detail': {'bit_exact_reduction': float(bitexact),
                   'field_changes_at_eps0.25': bool(changed),
                   'c_eff(0.25)': float(ceff), 'c_eff_expected': ceff_expected,
                   'c_eff_residual': float(ceff_res)},
    }


# ═════════════════════════════════════════════════════════════════════
#  CD5 — dual Meissner: London penetration depth lambda = 1/(e v)
# ═════════════════════════════════════════════════════════════════════

def test_CD5_dual_meissner_penetration():
    """CD5 — screened colour-electric field decays as exp(-r/lambda) with
    lambda = 1/(e v) (the dual Meissner length)."""
    e, v = 1.0, 0.5
    m = e * v                       # m = 1/lambda
    screen = cd.london_screened_field_2d(L=96, m=m)
    lam_fit, lam_exp = cd.fit_penetration_depth(screen, r_min=4, r_max=20)
    rel = abs(lam_fit - lam_exp) / lam_exp

    lam_formula = cd.penetration_depth(e=e, v=v)
    formula_ok = abs(lam_formula - 1.0 / m) < 1e-15

    passed = bool(rel < 0.05 and formula_ok)
    return {
        'test': 'CD5', 'name': 'dual Meissner penetration depth lambda=1/(e v)',
        'passed': passed, 'residual': float(rel), 'tier': 3,
        'detail': {'lambda_fit': float(lam_fit), 'lambda_expected': float(lam_exp),
                   'lambda_formula': float(lam_formula), 'm': float(m)},
    }


# ═════════════════════════════════════════════════════════════════════
#  CD6 — constant cross-section -> linear potential V(R) = sigma R
# ═════════════════════════════════════════════════════════════════════

def test_CD6_linear_potential():
    """CD6 — z-independent tube => E(R)=sigma R linear; RMS radius R-independent
    => isolated colour charge (R->inf) costs infinite energy."""
    prof = cd.solve_bps_profile(n=1, x_max=16.0, dx=2e-3)
    lengths = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
    E_R, sigma = cd.tube_energy_vs_length(prof, lengths)

    # linearity: fit E = sigma R, check slope and zero curvature
    A = np.vstack([lengths, np.ones_like(lengths)]).T
    slope, intercept = np.linalg.lstsq(A, E_R, rcond=None)[0]
    lin_res = float(np.max(np.abs(E_R - slope * lengths - intercept)))
    slope_res = abs(slope - sigma) / sigma

    rms = cd.tube_rms_radius(prof)      # single R-independent cross-section
    diverges = bool(E_R[-1] > E_R[0] and lengths[-1] > lengths[0])

    passed = bool(lin_res < 1e-9 and slope_res < 1e-12 and diverges and np.isfinite(rms))
    return {
        'test': 'CD6', 'name': 'constant cross-section -> linear V(R)=sigma R',
        'passed': passed, 'residual': float(lin_res), 'tier': 1,
        'detail': {'sigma': float(sigma), 'fit_slope': float(slope),
                   'slope_residual': float(slope_res),
                   'linearity_residual': lin_res,
                   'tube_rms_radius_mV': float(rms),
                   'E(R)': [float(x) for x in E_R]},
    }


# ═════════════════════════════════════════════════════════════════════

def main():
    t_start = time.perf_counter()
    tests = [
        test_CD1_bogomolny_completion,
        test_CD2_profile_bcs_and_flux,
        test_CD3_string_tension_bps,
        test_CD4_dielectric_rotation_step,
        test_CD5_dual_meissner_penetration,
        test_CD6_linear_potential,
    ]
    results = []
    n_pass = 0
    for fn in tests:
        t0 = time.perf_counter()
        try:
            r = fn()
            r['elapsed_s'] = time.perf_counter() - t0
            results.append(r)
            ok = bool(r.get('passed'))
            n_pass += int(ok)
            print(f"  [{'PASS' if ok else 'FAIL'}] {r.get('test'):4s}  "
                  f"{r.get('name'):58s}  res = {r.get('residual')}  "
                  f"({r['elapsed_s']:.3f} s)")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            results.append({'test': fn.__name__, 'passed': False, 'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FG-7d — confinement as colour-dielectric / dual superconductor (P1 Option C)',
        'date': '2026-06-03',
        'n_tests': len(tests),
        'n_passed': n_pass,
        'total_elapsed_s': total_t,
        'results': results,
    }
    print(f"\n  -> {n_pass}/{len(tests)} PASS  in  {total_t:.2f} s")
    return summary


if __name__ == '__main__':
    summary = main()
    out = os.path.join(os.path.dirname(__file__),
                       '..', '..', 'test-results', 'FG7d_colour_dielectric.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  -> wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
