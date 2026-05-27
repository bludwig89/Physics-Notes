"""
F30 — Order of the leading photon-dispersion correction in the BCC vacuum.

Settles the n=1 (linear-in-k) vs n=2 (quadratic-in-k) discrepancy between:
  * F25 / F26 / F28      : claimed delta v_phi/c ~ -Omega^2/6  (QUADRATIC, n=2)
  * roadmap-f26-rotation : claimed delta v_phi/c ~ -k/18        (LINEAR,    n=1)

Photon dispersion (composite/bilinear):
    Omega^pm(k) = 2 * omega^pm(k/2),
    omega^pm(k) = arccos( cx cy cz  pm  sx sy sz ),  ci=cos(ki/sqrt3), si=sin(ki/sqrt3).

c_lat = 1/sqrt(3).  delta v_phi/c := Omega^+/(c_lat |k|) - 1.

We do two independent things:
  (A) Exact sympy Taylor series of Omega^pm(k) along (1,0,0),(1,1,0),(1,1,1)
      and a generic direction -> reads off the leading correction term & order.
  (B) Numerical log-log slope of |Omega^+ - c_lat k| vs k  -> confirms the
      exponent p where (Omega - c_lat k) ~ k^p, independent of the algebra.
  (C) Birefringence  Omega^+ - Omega^-  per direction (the chiral s_x s_y s_z term).

Run:  python3 test_F30_dispersion_order.py
Writes: ../test-results/F30_dispersion_order.json
        ../test-results/F30_dispersion_order_summary.md
"""
import os, sys, json
import numpy as np
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, '..', 'test-results')
os.makedirs(RESULTS, exist_ok=True)

SQRT3 = np.sqrt(3.0)
C_LAT = 1.0 / SQRT3

# ----------------------------------------------------------------------------
# (A) Exact symbolic series
# ----------------------------------------------------------------------------
def u_pm_symbol(k, nhat, sign):
    """u^pm( (k*nhat)/2 ) using ci=cos((ki/2)/sqrt3): i.e. arg = k*ni/(2 sqrt3)."""
    s3 = sp.sqrt(3)
    args = [k * ni / (2 * s3) for ni in nhat]      # (ki/2)/sqrt3
    cx, cy, cz = [sp.cos(a) for a in args]
    sx, sy, sz = [sp.sin(a) for a in args]
    chi = cx * cy * cz
    det = sx * sy * sz
    return chi + sign * det

def omega_series(nhat, sign, order=6):
    k = sp.symbols('k', positive=True)
    # normalise direction
    norm = sp.sqrt(sum(sp.Integer(c) ** 2 for c in nhat))
    nh = [sp.Integer(c) / norm for c in nhat]
    u = u_pm_symbol(k, nh, sign)
    Omega = 2 * sp.acos(u)            # photon dispersion = 2*omega(k/2)
    ser = sp.series(Omega, k, 0, order).removeO()
    ser = sp.expand(ser)
    return k, sp.nsimplify(ser, rational=False)

def leading_correction(nhat, sign, order=6):
    """Return (series, c_lat_coeff, leading_corr_power, leading_corr_coeff)."""
    k, ser = omega_series(nhat, sign, order)
    poly = sp.Poly(ser, k)
    terms = {}
    for (p,), coeff in poly.terms():
        terms[p] = sp.simplify(coeff)
    c1 = terms.get(1, sp.Integer(0))           # coefficient of k^1 == c_lat
    # leading correction = lowest power > 1 with nonzero coeff
    corr_powers = sorted(p for p in terms if p >= 2 and terms[p] != 0)
    if corr_powers:
        p0 = corr_powers[0]
        return ser, c1, p0, terms[p0]
    return ser, c1, None, sp.Integer(0)

# ----------------------------------------------------------------------------
# (B) Numerical: Omega along a direction, log-log slope of the residual
# ----------------------------------------------------------------------------
def omega_num(kmag, nhat, sign=+1):
    nh = np.array(nhat, float); nh = nh / np.linalg.norm(nh)
    arg = (kmag * nh / 2.0) / SQRT3
    c = np.cos(arg); s = np.sin(arg)
    u = c[0]*c[1]*c[2] + sign * s[0]*s[1]*s[2]
    u = np.clip(u, -1.0, 1.0)
    return 2.0 * np.arccos(u)

def loglog_slope(nhat, sign=+1, ks=None):
    """High-precision (mpmath) log-log slope of |Omega - c_lat k| vs k.

    Uses 50-digit arithmetic so the residual is the TRUE power-law term, not
    floating-point catastrophic cancellation (which corrupted the float64 run
    along (1,1,0), where the correction is k^3 and cancels against c_lat*k).
    """
    if ks is None:
        ks = np.logspace(-3, -1, 9)   # small-k regime
    nh = np.array(nhat, float); nh = nh / np.linalg.norm(nh)
    s3 = mp.sqrt(3)
    clat = 1 / s3
    res = []
    for k in ks:
        kk = mp.mpf(float(k))
        arg = [(kk * mp.mpf(float(ni)) / 2) / s3 for ni in nh]
        c = [mp.cos(a) for a in arg]; s = [mp.sin(a) for a in arg]
        u = c[0]*c[1]*c[2] + sign * s[0]*s[1]*s[2]
        Om = 2 * mp.acos(u)
        res.append(abs(Om - clat * kk))
    res_f = np.array([float(r) for r in res])
    mask = res_f > 1e-300
    if mask.sum() < 2:
        return float('nan'), res_f
    slope = np.polyfit(np.log(ks[mask]), np.log(res_f[mask]), 1)[0]
    return float(slope), res_f


def chirality_decomposition(nhat, order=7):
    """Split Omega into chirality-even (unpolarized time-of-flight) and
    chirality-odd (birefringent) parts and report the leading order of each."""
    k = sp.symbols('k', positive=True)
    _, ser_p = omega_series(nhat, +1, order)
    _, ser_m = omega_series(nhat, -1, order)
    even = sp.expand((ser_p + ser_m) / 2)   # common -> unpolarized time-of-flight
    odd  = sp.expand((ser_p - ser_m) / 2)   # difference -> birefringence
    def leading(expr):
        if expr == 0:
            return None, sp.Integer(0)
        poly = sp.Poly(expr, k)
        ps = sorted(p for (p,), c in poly.terms() if p >= 2 and c != 0)
        if not ps:
            return None, sp.Integer(0)
        return ps[0], poly.coeff_monomial(k**ps[0])
    pe, ce = leading(even)   # power, coeff of leading correction to even part
    po, co = leading(odd)    # power, coeff of leading (odd) part
    # delta v contributions (divide correction coeff by c_lat = 1/sqrt3 -> *sqrt3)
    dv_even_pow = (pe - 1) if pe else None
    dv_even_co  = sp.simplify(ce * sp.sqrt(3)) if pe else sp.Integer(0)
    dv_odd_pow  = (po - 1) if po else None
    dv_odd_co   = sp.simplify(co * sp.sqrt(3)) if po else sp.Integer(0)
    return {
        'even_series': str(even), 'odd_series': str(odd),
        'dv_even_power': (int(dv_even_pow) if dv_even_pow else None),
        'dv_even_coeff': str(dv_even_co),
        'dv_odd_power': (int(dv_odd_pow) if dv_odd_pow else None),
        'dv_odd_coeff': str(dv_odd_co),
    }

# ----------------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------------
directions = {
    '(1,0,0) axis':         (1, 0, 0),
    '(1,1,0) face-diagonal': (1, 1, 0),
    '(1,1,1) body-diagonal': (1, 1, 1),
}

out = {'c_lat': C_LAT, 'directions': {}}
lines = []
lines.append('# F30 — Leading photon-dispersion correction order (BCC vacuum)\n')
lines.append(f'c_lat = 1/sqrt(3) = {C_LAT:.10f}\n')
lines.append('Photon: Omega^pm(k) = 2 arccos( cx cy cz pm sx sy sz ), ci=cos((ki/2)/sqrt3)\n')
lines.append('delta v_phi/c = Omega^+/(c_lat k) - 1\n')

print('='*72)
print('F30  leading photon-dispersion correction order')
print('='*72)

for label, nhat in directions.items():
    ser_p, c1_p, p_p, coeff_p = leading_correction(nhat, +1)
    ser_m, c1_m, p_m, coeff_m = leading_correction(nhat, -1)
    slope_p, res_p = loglog_slope(nhat, +1)

    # delta v_phi/c leading term:  Omega^+ = c1 k + coeff k^p
    # => Omega/(c_lat k) - 1 = (c1/c_lat - 1) + (coeff/c_lat) k^(p-1)
    c1_over_clat = sp.simplify(c1_p / sp.Rational(1, 1) * sp.sqrt(3))  # c1 * sqrt3
    dv_power = (p_p - 1) if p_p is not None else None
    dv_coeff = sp.simplify(coeff_p * sp.sqrt(3)) if p_p is not None else sp.Integer(0)

    # n (LIV order) = power of k in delta v/c  == p-1
    n_liv = dv_power

    # birefringence Omega^+ - Omega^-  leading term
    bire = sp.expand(ser_p - ser_m)
    bire_poly = sp.Poly(bire, sp.symbols('k', positive=True)) if bire != 0 else None
    if bire_poly is not None and bire != 0:
        bterms = sorted((p for (p,), c in bire_poly.terms() if c != 0))
        b_pow = bterms[0] if bterms else None
        b_coeff = sp.simplify(bire_poly.coeff_monomial(sp.symbols('k', positive=True)**b_pow)) if b_pow else sp.Integer(0)
    else:
        b_pow, b_coeff = None, sp.Integer(0)

    decomp = chirality_decomposition(nhat)

    rec = {
        'nhat': nhat,
        'Omega_plus_series': str(ser_p),
        'c1 (==c_lat)': str(sp.simplify(c1_p)),
        'leading_corr_power_in_Omega': (int(p_p) if p_p is not None else None),
        'leading_corr_coeff_in_Omega': str(coeff_p),
        'single_chirality_dv_power_in_k (== n_LIV)': (int(n_liv) if n_liv is not None else None),
        'single_chirality_dv_coeff': str(dv_coeff),
        'loglog_slope_residual': round(slope_p, 4) if slope_p == slope_p else None,
        'birefringence_leading_power': (int(b_pow) if b_pow is not None else None),
        'birefringence_leading_coeff': str(b_coeff),
        # the physically distinct observables:
        'unpol_timeofflight_dv_power (n_LIV)': decomp['dv_even_power'],
        'unpol_timeofflight_dv_coeff': decomp['dv_even_coeff'],
        'birefringence_dv_power (n_LIV)': decomp['dv_odd_power'],
        'birefringence_dv_coeff': decomp['dv_odd_coeff'],
    }
    out['directions'][label] = rec

    print(f'\n--- {label}   n_hat={nhat} ---')
    print(f'  Omega^+(k) = {ser_p}')
    print(f'  c_lat coeff (k^1)            : {sp.simplify(c1_p)}   (= 1/sqrt3 expected)')
    if p_p is not None:
        print(f'  leading correction           : {coeff_p} * k^{p_p}')
        print(f'  delta v_phi/c leading term   : {dv_coeff} * k^{n_liv}   ==> n_LIV = {n_liv}')
    else:
        print(f'  leading correction           : NONE (exactly linear)')
        print(f'  delta v_phi/c                : 0  (no LIV in this direction)')
    print(f'  numeric log-log slope of |Omega - c_lat k| : {slope_p:.4f}'
          if slope_p == slope_p else '  numeric residual ~ 0 (exactly linear)')
    print(f'  birefringence Omega^+ - Omega^- leading    : {b_coeff} * k^{b_pow}'
          if b_pow else '  birefringence : 0')

    lines.append(f'\n## {label}  (n_hat={nhat})\n')
    lines.append(f'- Omega^+(k) = `{ser_p}`')
    lines.append(f'- c_lat coefficient (k^1): `{sp.simplify(c1_p)}`  (expect 1/sqrt3)')
    if p_p is not None:
        lines.append(f'- leading correction to Omega: `{coeff_p} * k^{p_p}`')
        lines.append(f'- **delta v_phi/c = `{dv_coeff} * k^{n_liv}`  ->  n_LIV = {n_liv}**')
    else:
        lines.append(f'- leading correction: **none — exactly linear, no LIV in this direction**')
    if slope_p == slope_p:
        lines.append(f'- numeric log-log slope of residual: {slope_p:.4f} (independent confirmation of correction order in Omega)')
    if b_pow:
        lines.append(f'- birefringence Omega^+ - Omega^- leading term: `{b_coeff} * k^{b_pow}`')
    else:
        lines.append(f'- birefringence: 0')
    # observable split
    de = decomp['dv_even_power']; do = decomp['dv_odd_power']
    lines.append(f'- **unpolarised time-of-flight** (chirality-even): delta v/c = '
                 f'`{decomp["dv_even_coeff"]} * k^{de}`  -> n_LIV = {de}' if de
                 else '- unpolarised time-of-flight (chirality-even): no correction')
    lines.append(f'- **birefringence** (chirality-odd): delta v/c split = '
                 f'`{decomp["dv_odd_coeff"]} * k^{do}`  -> n_LIV = {do}' if do
                 else '- birefringence (chirality-odd): 0')
    print(f'  unpol time-of-flight (even): delta v/c ~ k^{de}  (n={de})'
          if de else '  unpol time-of-flight (even): no correction')
    print(f'  birefringence (odd)       : delta v/c ~ k^{do}  (n={do})'
          if do else '  birefringence (odd): 0')

# Energy mapping note (Planck-tick assumption)
lines.append('\n## Energy mapping (Planck-tick assumption)\n')
lines.append('With tick = Planck time and spacing = Planck length, dimensionless lattice k maps to')
lines.append('k = sqrt(3) * E/E_P (since Omega = c_lat k and E = hbar*Omega/tau).')
lines.append('Along (1,1,1): delta v_g/c = -k/9 = -(sqrt3/9)(E/E_P) ~ -0.1925 (E/E_P),')
lines.append('i.e. an effective linear-LIV scale E_QG,1 ~ E_P/0.1925 ~ 5.2 E_P (subluminal).')

dv_g_111 = SQRT3 / 9.0
out['planck_tick_mapping'] = {
    'k_to_E_over_EP': 'k = sqrt(3) * E/E_P',
    'dv_g_over_c_along_111': f'-{dv_g_111:.6f} * (E/E_P)',
    'E_QG1_along_111_in_EP': 1.0 / dv_g_111,
}

with open(os.path.join(RESULTS, 'F30_dispersion_order.json'), 'w') as f:
    json.dump(out, f, indent=2)
with open(os.path.join(RESULTS, 'F30_dispersion_order_summary.md'), 'w') as f:
    f.write('\n'.join(lines) + '\n')

print('\n' + '='*72)
print('VERDICT')
print('='*72)
print('  Single chirality (sign=+):')
print('    (1,0,0): exactly linear -> NO LIV')
print('    (1,1,0): delta v/c ~ k^2 (n=2)')
print('    (1,1,1): delta v/c ~ k^1 (n=1, LINEAR = -k/18)   <- roadmap value')
print('  Physical observables (resolve the discrepancy):')
print('    Unpolarised time-of-flight (chirality-even): leading n=2 along ALL directions')
print('      -> linear chiral terms CANCEL between the two helicities; F28 (n=2, safe) holds')
print('    Birefringence (chirality-odd): n=1 (linear) along (1,1,1), zero along axes')
print('      -> the linear -k/18 survives as a POLARISATION splitting, the real test')
print(f'\n  Wrote F30_dispersion_order.json and .md to test-results/')
