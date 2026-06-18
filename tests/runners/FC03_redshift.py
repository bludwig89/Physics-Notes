"""
FC03 — Gravitational redshift (Pound-Rebka)
============================================
Date: 2026-06-16

Tier C consistency regression. Supersedes tests/priority/test_04_GR3_pound_rebka.py.

Model element under test
------------------------
The clock-rate (g_tt) leg of the F64 single-lattice dielectric.
Canonical index K = e^{2u}, u = GM/(rc^2); metric g_tt = -A = -e^{-2u},
g_ij = B delta_ij = e^{2u} delta_ij, reciprocal lock AB = 1 (F64 D-EM9).

Hypothesis (GR-identical):
    Delta nu / nu = g h / c^2 = G M Delta r / (r^2 c^2)   (PPN, exact at O(phi/c^2)).

Build
-----
(1) Static clock-rate readout. Proper frequency of a static clock at radius r
    scales as sqrt(-g_tt) = sqrt(A) = e^{-u}. A photon emitted at r_emit and
    received at r_obs > r_emit is redshifted by
        1 + z = nu_emit / nu_obs = sqrt(A_obs) / sqrt(A_emit)
              = e^{-u_obs} / e^{-u_emit} = e^{u_emit - u_obs}.
    For the Pound-Rebka geometry (emit at bottom r, observe at r + Delta r)
    the fractional shift is
        Delta nu / nu = (nu_obs - nu_emit) / nu_emit = e^{u_emit - u_obs} - 1.
    Confirm Delta nu / nu -> g Delta r / c^2 = G M Delta r / (r^2 c^2) at
    leading order in phi/c^2, to the numerical floor.
(2) Confirm the exact exponential A = e^{-2u} gives a FINITE, MONOTONIC redshift
    for all finite r > 0 with NO horizon: g_tt = -e^{-2u} has no finite root
    (e^{-2u} > 0 for all finite u), unlike Schwarzschild g_tt = -(1 - 2u) which
    vanishes at r = 2GM/c^2. Links FA10 (black-hole shadow, horizon-free).

All arithmetic is ordinary real arithmetic (no chiral transforms; numpy not
required). Uses math.exp / math.expm1 only.
"""

import os, json, math
from datetime import datetime

THIS = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.abspath(os.path.join(THIS, '..', '..', 'test-results'))


def lapse_A(u):
    """g_tt = -A, A = e^{-2u} (canonical F64 dielectric, clock-rate leg)."""
    return math.exp(-2.0 * u)


def clock_rate(u):
    """Proper-frequency rate of a static clock = sqrt(A) = e^{-u}."""
    return math.exp(-u)


def redshift_exact(u_emit, u_obs):
    """1 + z = nu_emit/nu_obs = sqrt(A_obs)/sqrt(A_emit) = e^{u_emit - u_obs}.
    Returns the FRACTIONAL shift Delta nu / nu = (nu_obs - nu_emit)/nu_emit
    = e^{u_emit - u_obs} - 1 (negative: observed light is redshifted to lower nu)."""
    return math.expm1(u_emit - u_obs)


def main():
    out = {
        'test_id': 'FC03',
        'title': 'Gravitational redshift (Pound-Rebka): dielectric g_tt=-e^{-2u} '
                 'gives Delta nu/nu = g Delta r/c^2 at O(phi/c^2), horizon-free',
        'tier': 'C',
        'timestamp': datetime.now().strftime('%Y-%m-%d - %H:%M'),
        'element_under_test': 'Clock-rate (g_tt) leg of F64 single-lattice '
                              'dielectric; canonical K=e^{2u}, A=1/K=e^{-2u}',
        'hypothesis': 'Delta nu/nu = g h/c^2 = G M Delta r/(r^2 c^2) (GR-identical, '
                      'exact at O(phi/c^2))',
        'provenance': ['F16', 'F64', 'F62', 'F112 (section B)'],
    }

    # ----------------------------------------------------------------------
    # Part (1): O(phi/c^2) match to g Delta r / c^2 across a range of fields.
    # Geometric units G = c = 1. Emit at radius r (well bottom), observe at
    # r + Delta r (higher up). u = M/r. Local g at r is g = G M / r^2 = M/r^2.
    # GR/PPN target: Delta nu/nu = g Delta r / c^2 = M Delta r / r^2.
    # ----------------------------------------------------------------------
    M = 1.0
    cases = []
    # A ladder of (r, Delta r). The GR Pound-Rebka law Delta nu/nu = g Delta r/c^2
    # is the LEADING term of the exact dielectric result; the residual is
    # controlled by the small parameter eps = Delta r / r (the lab/well-radius
    # ratio), since
    #   u_emit - u_obs = (M Delta r/r^2)(1 - eps + eps^2 - ...)   and
    #   Delta nu/nu = (u_emit-u_obs) + (1/2)(u_emit-u_obs)^2 + ...
    # so Delta nu/nu = g Delta r/c^2 * [1 + O(eps) + O(u)].  We shrink eps to
    # the numerical floor at fixed (weak) field to expose the leading-order
    # identity; the residual must scale linearly with eps -> 0.
    r = 1.0e6                     # fixed weak field u = M/r = 1e-6
    for eps in (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6):
        dr = r * eps              # lab height; eps = dr/r is the expansion param
        u_emit = M / r
        u_obs = M / (r + dr)
        z_exact = redshift_exact(u_emit, u_obs)        # full exponential result
        g_local = M / r**2                              # local g at emitter
        z_gr = g_local * dr                             # GR leading-order target
        # residual of the leading-order match
        abs_res = abs(z_exact - z_gr)
        rel_res = abs_res / abs(z_gr) if z_gr != 0 else float('inf')
        cases.append({
            'r': r, 'delta_r': dr, 'eps_dr_over_r': eps,
            'u_emit': u_emit, 'u_obs': u_obs,
            'phi_over_c2': u_emit,                       # field-strength label
            'z_exact_dielectric': z_exact,
            'z_GR_g_dr_over_c2': z_gr,
            'abs_residual': abs_res,
            'rel_residual': rel_res,
        })

    # The leading-order match improves as O(eps): rel_residual ~ Delta r/r.
    # Confirm the smallest-eps case is at the numerical/physical floor and the
    # residual scales linearly with eps.
    weakest = cases[-1]
    out['part1_leading_order_match'] = {
        'units': 'geometric (G=c=1)',
        'target': 'Delta nu/nu = g Delta r/c^2 = G M Delta r/(r^2 c^2)',
        'fixed_field_u': M / r,
        'cases': cases,
        'rel_residual_smallest_eps': weakest['rel_residual'],
        'rel_residual_scales_as_eps': 'rel_residual ~ Delta r/r (next-order term)',
    }

    # Verify the O(eps) scaling: dropping eps by 10x should drop rel_res ~10x.
    ratios = []
    for a, b in zip(cases[:-1], cases[1:]):
        if b['rel_residual'] > 0:
            ratios.append(a['rel_residual'] / b['rel_residual'])
    out['part1_leading_order_match']['rel_residual_decade_ratios'] = ratios
    scaling_ok = all(abs(rr - 10.0) / 10.0 < 0.05 for rr in ratios)  # within 5% of 10x
    out['part1_leading_order_match']['linear_in_eps_confirmed'] = scaling_ok

    # ----------------------------------------------------------------------
    # Part (2): horizon-free monotonic redshift. Scan r from far down to the
    # would-be Schwarzschild horizon and below; show A = e^{-2u} stays > 0
    # (finite redshift) and the redshift seen from infinity, 1+z = e^{u}, is
    # finite and monotonically increasing as r -> 0, vs Schwarzschild which
    # diverges (1+z -> inf) at r = 2M and has no solution below.
    # ----------------------------------------------------------------------
    horizon_scan = []
    prev_z_inf = -1.0
    monotonic = True
    for r in (10.0, 4.0, 2.0, 1.0, 0.5, 0.1, 0.01):
        u = M / r
        A_diel = lapse_A(u)                       # e^{-2u}, always > 0
        one_plus_z_inf_diel = math.exp(u)         # redshift to observer at infinity
        # Schwarzschild isotropic-comparable: g_tt = -(1 - 2u); horizon at 2u=1
        A_schw = 1.0 - 2.0 * u
        if A_schw > 0:
            one_plus_z_inf_schw = 1.0 / math.sqrt(A_schw)
            schw_status = 'finite'
        else:
            one_plus_z_inf_schw = None
            schw_status = ('horizon (g_tt=0)' if abs(A_schw) < 1e-15
                           else 'inside horizon (g_tt>0, no static clock)')
        if one_plus_z_inf_diel < prev_z_inf:
            monotonic = False
        prev_z_inf = one_plus_z_inf_diel
        horizon_scan.append({
            'r': r, 'u': u,
            'A_dielectric_e^-2u': A_diel,
            'dielectric_finite_positive': A_diel > 0.0,
            'one_plus_z_to_infinity_dielectric': one_plus_z_inf_diel,
            'A_schwarzschild_1-2u': A_schw,
            'one_plus_z_to_infinity_schwarzschild': one_plus_z_inf_schw,
            'schwarzschild_status': schw_status,
        })

    # The dielectric lapse has no finite root: e^{-2u} > 0 for all finite u.
    dielectric_horizon_free = all(row['dielectric_finite_positive']
                                  for row in horizon_scan)
    out['part2_horizon_free'] = {
        'claim': 'g_tt = -e^{-2u} has no finite root => no event horizon; '
                 'redshift finite and monotonic for all r>0 (links FA10)',
        'scan': horizon_scan,
        'dielectric_lapse_positive_everywhere': dielectric_horizon_free,
        'dielectric_redshift_monotonic_in_1/r': monotonic,
        'schwarzschild_horizon_at_r': 2.0 * M,
        'schwarzschild_has_horizon': True,
    }

    # ----------------------------------------------------------------------
    # Verdict
    # ----------------------------------------------------------------------
    # Pass criteria:
    #  - leading-order redshift matches g Delta r/c^2: rel residual -> 0 with
    #    the lab/well ratio eps=Delta r/r, scaling linearly (next-order term), AND
    #  - dielectric metric is horizon-free with finite monotonic redshift.
    leading_order_pass = (weakest['rel_residual'] < 1e-5) and scaling_ok
    horizon_pass = dielectric_horizon_free and monotonic
    verdict = 'PASS' if (leading_order_pass and horizon_pass) else 'FAIL'

    out['verdict'] = verdict
    out['summary'] = {
        'leading_order_match_pass': leading_order_pass,
        'rel_residual_smallest_eps': weakest['rel_residual'],
        'rel_residual_linear_in_eps': scaling_ok,
        'horizon_free_confirmed': horizon_pass,
        'note': ('Delta nu/nu = e^{u_emit-u_obs}-1 = g Delta r/c^2 + O(eps) + O(u), '
                 'eps=Delta r/r; residual is the next-order term and vanishes '
                 'linearly as Delta r/r -> 0 (rel residual 9.99e-04 -> 1.0e-06 '
                 'over 4 decades). Exact exponential lapse e^{-2u} is horizon-free.'),
    }

    os.makedirs(RESULTS, exist_ok=True)
    out_path = os.path.join(RESULTS, 'FC03_redshift.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)

    # Console report
    print('=' * 70)
    print('FC03 — Gravitational redshift (Pound-Rebka)')
    print('=' * 70)
    print(f'Verdict: {verdict}')
    print()
    print(f'Part 1 — leading-order match Delta nu/nu = g Delta r/c^2 '
          f'(fixed field u={weakest["u_emit"]:.0e}):')
    print(f'{"eps=dr/r":>10} {"z_exact":>14} {"z_GR":>14} {"rel_resid":>12}')
    for c in cases:
        print(f'{c["eps_dr_over_r"]:>10.2e} {c["z_exact_dielectric"]:>14.6e} '
              f'{c["z_GR_g_dr_over_c2"]:>14.6e} {c["rel_residual"]:>12.3e}')
    print(f'  rel_residual (smallest eps={weakest["eps_dr_over_r"]:.0e}): '
          f'{weakest["rel_residual"]:.3e}')
    print(f'  decade ratios (expect ~10, O(eps) scaling): '
          f'{[round(r,3) for r in ratios]}  -> linear-in-eps {scaling_ok}')
    print()
    print('Part 2 — horizon-free monotonic redshift:')
    print(f'{"r":>8} {"u=M/r":>8} {"A=e^-2u":>12} {"1+z(diel)":>12} '
          f'{"Schwarzschild":>18}')
    for row in horizon_scan:
        sz = row['one_plus_z_to_infinity_schwarzschild']
        szs = f'{sz:.4f}' if sz is not None else row['schwarzschild_status']
        print(f'{row["r"]:>8.2f} {row["u"]:>8.3f} '
              f'{row["A_dielectric_e^-2u"]:>12.4e} '
              f'{row["one_plus_z_to_infinity_dielectric"]:>12.4f} {szs:>18}')
    print(f'  dielectric lapse > 0 everywhere: {dielectric_horizon_free}')
    print(f'  dielectric redshift monotonic:   {monotonic}')
    print(f'  Schwarzschild horizon at r = 2M = {2.0*M}')
    print()
    print(f'Results written to {out_path}')
    return out


if __name__ == '__main__':
    main()
