"""
F351 -- Ledger row E7 / parameter #17 (v): is v a second dimensionful pin
analogous to G (F79/F232, row L3), or forced by that same G?

This finding does no new lattice computation. T1 is a mechanical symbolic
check (sympy) that v is outside the free-symbol set of F79's G-fixing
equation. T2 flags a documentation hazard: F118/F234's "v" is a different,
dimensionless, unrelated free-energy coefficient. T3 and T4 reproduce
already-published numbers from F143 and F233 respectively (artifact/prose
verification, not a re-run of the underlying lattice code). T5 is an
illustrative order-of-magnitude type-check.

Date: 2026-09-02
"""

import json
import math
import os

import sympy as sp

RESULTS = {}
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _grep_count(pattern, path):
    full = os.path.join(REPO_ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return text.count(pattern)


def test_T1_G_equation_free_symbols_exclude_v():
    """F79's structural relation 1/G = 2*pi*eta*g_*  sqrt(d) * hbar/(a^2 c^3)
    is one scalar equation in {a, G} given {eta, g_*, d, hbar, c} fixed. Build
    it symbolically and confirm v is not among its free symbols -- i.e. this
    equation cannot, by construction, constrain v at all."""
    a, hbar, c, eta, gstar, d, v = sp.symbols('a hbar c eta g_star d v', positive=True)
    inv_G = 2 * sp.pi * eta * gstar * sp.sqrt(d) * hbar / (a**2 * c**3)
    free = inv_G.free_symbols
    names = sorted(str(s) for s in free)
    v_excluded = v not in free
    expected = {'a', 'hbar', 'c', 'eta', 'g_star', 'd'}
    ok = v_excluded and set(names) == expected
    # numeric sanity: this is F232's own T1, reproduced (a/ell_P = sqrt(8 pi) 3^(1/4))
    eta_v, gstar_v, d_v = sp.Rational(1, 12), 48, 3
    a_over_lP = sp.sqrt(2 * sp.pi * eta_v * gstar_v) * sp.Rational(d_v) ** sp.Rational(1, 4)
    a_over_lP_f = float(a_over_lP)
    numeric_ok = abs(a_over_lP_f - 6.59782) < 1e-4
    RESULTS['T1'] = {
        'statement': 'v not in free_symbols(1/G); G-equation cannot pin a second unknown',
        'free_symbols': names,
        'v_excluded': v_excluded,
        'a_over_ellP_reproduced': a_over_lP_f,
        'pass': bool(ok and numeric_ok),
    }
    assert ok, f"unexpected free symbols: {names}"
    assert numeric_ok, f"a/ell_P mismatch: {a_over_lP_f}"
    return True


def test_T2_v_notation_collision_flagged():
    """F118/F234's self-consistent (W,v,c) triple's 'v' (~0.16, dimensionless,
    a per-axis quartic coefficient in the second-shell lepton free energy) is
    numerically and dimensionally disjoint from ledger parameter #17, the
    electroweak scale V_EW = (sqrt(2) G_F)^(-1/2) = 246.22 GeV. Confirm the
    gap and confirm neither is a registered casim.constants Constant (both
    are module-local literals, per derive_gauge_boson_masses.py's own docstring
    and F118's free-energy functional)."""
    G_FERMI = 1.1663787e-5  # GeV^-2, PDG 2024 -- as coded in derive_gauge_boson_masses.py
    V_EW = 1.0 / math.sqrt(math.sqrt(2.0) * G_FERMI)
    v_F118 = 0.16  # F118 sec.4 representative point

    ratio = V_EW / v_F118
    disjoint = ratio > 100  # obviously not the same number under any unit reading

    # neither symbol is registered as a Constant under the bare name 'v'
    const_dir = os.path.join(REPO_ROOT, 'src', 'casim', 'constants')
    v_registered = False
    if os.path.isdir(const_dir):
        for fn in os.listdir(const_dir):
            if fn.endswith('.py'):
                full = os.path.join(const_dir, fn)
                with open(full, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                if 'symbol="v"' in text or "symbol='v'" in text:
                    v_registered = True

    RESULTS['T2'] = {
        'statement': "F118/F234 'v' (~0.16, dimensionless) vs ledger v (246.22 GeV): disjoint, neither registered",
        'V_EW_GeV': V_EW,
        'v_F118': v_F118,
        'ratio': ratio,
        'disjoint': disjoint,
        'v_registered_as_constant': v_registered,
        'pass': bool(disjoint and not v_registered),
    }
    assert abs(V_EW - 246.22) < 0.05, f"V_EW mismatch: {V_EW}"
    assert disjoint
    assert not v_registered, "a bare 'v' Constant is registered -- re-check the collision claim"
    return True


def test_T3_F143_fermion_loop_share_reproduced():
    """Reproduce F143 Sec.5's fermion-loop share of v^2 from its own quoted
    inputs: m_t = 172.57 GeV, hat_f in [0.17, 0.38], (Delta Y/2)^2 = 1/4,
    N_c = 3, v = 246.22 GeV. F143's own quoted band is 96-215 GeV^2, i.e.
    0.16-0.36% of v^2."""
    m_t = 172.57
    v = 246.22
    n_c = 3
    dy2 = 0.25
    f_lo, f_hi = 0.17, 0.38

    def share(f_hat):
        return dy2 * n_c * (f_hat * m_t ** 2) / (4 * math.pi ** 2)

    lo, hi = share(f_lo), share(f_hi)
    frac_lo, frac_hi = lo / v ** 2, hi / v ** 2

    ok = (90 < lo < 100) and (210 < hi < 220) and (0.0015 < frac_lo < 0.0017) and (0.0035 < frac_hi < 0.0037)
    RESULTS['T3'] = {
        'statement': 'fermion-loop share of v^2 reproduces F143 Sec.5 (96-215 GeV^2, 0.16-0.36%)',
        'share_GeV2_lo': lo, 'share_GeV2_hi': hi,
        'fraction_lo': frac_lo, 'fraction_hi': frac_hi,
        'pass': bool(ok),
    }
    assert ok, f"share band mismatch: {lo}, {hi}, {frac_lo}, {frac_hi}"
    return True


def test_T4_F233_transmutation_factor_reproduced():
    """Reproduce F233's headline factor: N_F119 / N_pred ~ 1.9, where
    N_F119 = m_lat(tau) = 5.54e-19 and N_pred = 2.86e-19 (loop-converged
    QCD asymptotic-freedom running, F233/F144)."""
    n_f119 = 5.54e-19
    n_pred = 2.86e-19
    ratio = n_f119 / n_pred
    ok = abs(ratio - 1.9) < 0.1
    RESULTS['T4'] = {
        'statement': 'F233 transmutation factor N_F119/N_pred ~ 1.9',
        'N_F119': n_f119, 'N_pred': n_pred, 'ratio': ratio,
        'pass': bool(ok),
    }
    assert ok, f"ratio mismatch: {ratio}"
    return True


def test_T5_v_lat_order_of_magnitude_typecheck():
    """Illustrative only: v_lat = v / (hbar c / a) sits in the same order-of-
    magnitude regime as fermion m_lat's (F119: tau=5.54e-19, top=5.39e-17),
    confirming v is a mass-TYPE quantity, not a mass-blind dimensionless
    invariant of the kind F232's degeneracy theorem excludes."""
    v_gev = 246.22
    hbar_c_gev_fm = 0.197327  # GeV.fm
    a_m = 1.06638e-34  # F79/F232 structural cell, metres
    a_fm = a_m * 1e15
    lambda_lat_gev = hbar_c_gev_fm / a_fm  # hbar c / a, GeV

    v_lat = v_gev / lambda_lat_gev
    tau_m_lat = 5.54e-19
    top_m_lat = 5.39e-17

    same_regime = tau_m_lat < v_lat < 10 * top_m_lat
    RESULTS['T5'] = {
        'statement': 'v_lat in the fermion m_lat order-of-magnitude regime (illustrative)',
        'lambda_lat_GeV': lambda_lat_gev,
        'v_lat': v_lat,
        'tau_m_lat': tau_m_lat, 'top_m_lat': top_m_lat,
        'pass': bool(same_regime),
    }
    assert same_regime, f"v_lat={v_lat} not in expected regime"
    return True


if __name__ == '__main__':
    tests = [
        ('T1', "G's equation excludes v (mechanical, sympy)", test_T1_G_equation_free_symbols_exclude_v),
        ('T2', "F118/F234 'v' notation collision flagged", test_T2_v_notation_collision_flagged),
        ('T3', 'F143 fermion-loop share of v^2 reproduced', test_T3_F143_fermion_loop_share_reproduced),
        ('T4', 'F233 transmutation factor ~1.9 reproduced', test_T4_F233_transmutation_factor_reproduced),
        ('T5', 'v_lat order-of-magnitude type-check (illustrative)', test_T5_v_lat_order_of_magnitude_typecheck),
    ]

    print("=" * 72)
    print("F351 -- Is v a second dimensionful pin analogous to G, or forced by it?")
    print("=" * 72)

    passed = 0
    for tag, label, fn in tests:
        try:
            fn()
            status = "PASS"
            passed += 1
        except Exception as e:
            status = f"FAIL ({e})"
        print(f"  {tag}  {label:65s}  {status}")

    results_dir = os.path.join(REPO_ROOT, 'test-results')
    os.makedirs(results_dir, exist_ok=True)
    out_path = os.path.join(results_dir, 'F351_v_second_pin_scope.json')

    summary = {
        'finding': 'F351',
        'date': '2026-09-02',
        'overall': f'{passed}/{len(tests)} PASS',
        'checks': RESULTS,
        'conclusion': (
            'v is not forced by G (mechanically -- v is outside the free-symbol set '
            "of F79's G-fixing equation), and v is not an independent scale gap "
            'needing its own new dimensionful pin: the Sakharov/loop-induction route '
            'is checked and negligible (F143, 0.16-0.36% of v^2), and the NJL/dynamical-'
            'transmutation route is NOT absent as F119 originally concluded -- F233 '
            'already supersedes that for the sibling quantity N via QCD asymptotic '
            'freedom (factor 1.9), contingent on the shared constant d_1. v is '
            'plausibly (not yet provably) the same single d_1 residual as N and the '
            'lepton brake lambda_6. No number for v is claimed; ledger row E7 stays '
            'FIT(N=1).'
        )
    }
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Results -> {out_path}")
    print(f"  {passed}/{len(tests)} PASS")
    print("=" * 72)
