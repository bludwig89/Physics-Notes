"""
F199 — First-principles attempt at the angular self-duality C/|B| = 1/(2 cos 2/3).

Tests, all real arithmetic (no chiral transforms), sympy for the exact parts:

  A  ANCHOR (necessary): massless-electron Koide texture forces 3delta = pi/4 exactly.
  S1 STEP 1 (second relation): Q is purely radial (delta-independent) -> the F92
     analogue second exact relation for 3delta provably does NOT exist.
  S2 STEP 2 (alpha cancellation): B is an O(alpha^0) sea loop, C an O(alpha^>=1)
     induced coupling -> alpha_eff does NOT cancel in C/|B|; the bare Fierz rational
     2/9 misses the target -> computed nonperturbative number, not a theorem.
  S3 STEP 3 (BPS degeneracy): the only special C/|B| the wall/bulk structure picks
     out is the tetragonal->orthorhombic threshold 1/2, NOT the self-dual 0.636.
  V  VALUE DISCRIMINATION: the derived (bare) solve lands off BOTH 0.63622 and 2/pi
     by ~9% (>> 1e-4); the data point sits at the self-dual value (the relabel/target),
     but the *derivation* cannot discriminate -> honest terminus = forced posit.

Verdict: FORCED POSIT. The angular self-duality 3delta = Q is not derivable from the
existing structure; it must be posited (consistent with F176/F177/F179, sharpened here).
"""
import json, math, os
import sympy as sp

RESULTS = {}
PASS = {}

# ---------------------------------------------------------------- constants
# PDG charged-lepton masses (MeV), same values as F179
ME, MMU, MTAU = 0.51099895, 105.6583755, 1776.86
MTAU_ERR = 0.12
I2 = 0.2202          # F95 lattice constant  <cot omega>_BCC
# F118 published saturation-point values for the angular Landau invariants
B_ABS_F118 = 0.0569  # |B|, full nonperturbative sea cubic at the wall-pinned point
E6_F118 = 0.14897    # e^6 at that point  (back-out: C_req/lambda6 = 0.636|B|/0.243)

SELF_DUAL = 1.0 / (2.0 * math.cos(2.0 / 3.0))   # 0.63622
COMPETITOR = 2.0 / math.pi                        # 0.63662


def reduced_cos3delta(masses):
    """Assignment-independent cos(3 delta) from the Foot-circle phase."""
    sq = [math.sqrt(m) for m in masses]
    mubar = sum(sq) / 3.0
    c = [(s / mubar - 1.0) / math.sqrt(2.0) for s in sq]   # = cos(theta_a)
    X = sum(c[k] * math.cos(2 * math.pi * k / 3) for k in range(3))   # (3/2) cos d
    Y = -sum(c[k] * math.sin(2 * math.pi * k / 3) for k in range(3))  # (3/2) sin d
    delta = math.atan2(Y, X)
    return math.cos(3 * delta), delta


# =====================================================================  A
def test_A_anchor_pi_over_4():
    """Massless texture (m_h, m_mid, 0): Q=2/3 <=> delta=15deg, 3delta=pi/4 exact."""
    u = sp.symbols('u', positive=True)
    Q = (1 + u**2) / (1 + u)**2
    tan_d = sp.sqrt(3) * u / (2 - u)
    sols = sp.solve(sp.Eq(Q, sp.Rational(2, 3)), u)
    u0 = [s for s in sols if (s > 0) == True and (s < 1) == True][0]
    assert sp.simplify(u0 - (2 - sp.sqrt(3))) == 0
    delta0 = sp.atan(tan_d.subs(u, u0))
    assert sp.simplify(delta0 - sp.pi / 12) == 0           # 15 deg
    assert sp.simplify(sp.cos(3 * delta0) - 1 / sp.sqrt(2)) == 0   # 3delta = pi/4
    RESULTS['A_anchor'] = {
        'u_star': '2 - sqrt(3)', 'delta_deg': 15.0,
        'three_delta': 'pi/4', 'cos3delta': float(1 / sp.sqrt(2)),
        'statement': 'massless Koide point forces 3delta = pi/4 EXACTLY'}
    PASS['A'] = True


# =====================================================================  S1
def test_S1_no_second_relation():
    """Q = 1/3 + r^2/6 is delta-independent: no kinematic 2nd relation for 3delta."""
    r, d, mu = sp.symbols('r delta mu', positive=True)
    roots = [mu * (1 + r * sp.cos(d + 2 * sp.pi * k / 3)) for k in range(3)]
    S1 = sp.simplify(sum(roots))
    S2 = sp.simplify(sum(x**2 for x in roots))
    Qexpr = sp.simplify(S2 / S1**2)
    assert sp.simplify(Qexpr - (sp.Rational(1, 3) + r**2 / 6)) == 0
    assert sp.simplify(sp.diff(Qexpr, d)) == 0             # delta drops out
    # and Q=2/3 <=> r = sqrt2 (F92), still says nothing about delta
    rstar = sp.solve(sp.Eq(Qexpr, sp.Rational(2, 3)), r)
    assert any(sp.simplify(rr - sp.sqrt(2)) == 0 for rr in rstar)
    RESULTS['S1_second_relation'] = {
        'Q_expr': '1/3 + r^2/6', 'dQ_ddelta': 0,
        'r_at_Q_two_thirds': 'sqrt(2)',
        'verdict': 'Q purely RADIAL, 3delta purely ANGULAR (orthogonal). '
                   'The F92 analogue (two mass laws intersecting) does NOT exist. '
                   'NO second exact relation forces 3delta = Q.'}
    PASS['S1'] = True


# =====================================================================  S2
def test_S2_alpha_does_not_cancel():
    """B ~ O(alpha^0) sea loop; C ~ O(alpha^>=1) induced -> ratio carries alpha."""
    rows = {}
    for name, lam6 in [('Fierz_2_9', 2/9), ('rotor_1_4', 0.25), ('fit', 0.243)]:
        C = lam6 * E6_F118
        cob = C / B_ABS_F118
        cos3 = 1.0 / (2.0 * cob)
        delta_deg = math.degrees(math.acos(cos3)) / 3.0
        rows[name] = {'lambda6': lam6, 'C_over_B': cob,
                      'cos3delta': cos3, 'delta_deg': delta_deg}
    # bare Fierz rational misses the target by a real, non-rational margin
    cob_bare = (2/9) * E6_F118 / B_ABS_F118
    enhancement = SELF_DUAL / cob_bare
    assert abs(rows['Fierz_2_9']['C_over_B'] - SELF_DUAL) > 1e-2   # bare misses
    assert enhancement > 1.0                                       # needs IR boost
    RESULTS['S2_alpha_cancellation'] = {
        'B_order': 'O(alpha^0)  (Dirac-sea cubic, parameter-free, F95 D1-D4)',
        'C_order': 'O(alpha^>=1) (induced E_g clock self-coupling, F145/F118)',
        'cancels': False,
        'rows': rows, 'target_C_over_B': SELF_DUAL,
        'bare_Fierz_C_over_B': cob_bare,
        'nonperturbative_enhancement_needed': enhancement,
        'verdict': 'alpha_eff does NOT cancel (different alpha-orders). '
                   'Bare Fierz 2/9 gives C/|B|=%.4f, needs %.3fx uncomputed IR factor '
                   'to reach 0.63622 -> COMPUTED number, not a theorem.'
                   % (cob_bare, enhancement)}
    PASS['S2'] = True


# =====================================================================  S3
def test_S3_bps_degeneracy_at_one_half():
    """Wall/bulk degeneracy of V(x)=B x + C x^2 is at C/|B|=1/2, not 0.636."""
    C, absB, x = sp.symbols('C B_abs x', positive=True)
    V = -absB * x + C * x**2
    xstar = sp.solve(sp.diff(V, x), x)[0]
    assert sp.simplify(xstar - absB / (2 * C)) == 0
    Vint = V.subs(x, xstar)
    V0 = V.subs(x, 1)                       # delta = 0 symmetric point
    gap = sp.simplify(sp.factor(V0 - Vint))
    # gap = (2C - |B|)^2 / (4C) >= 0, =0 only at C = |B|/2  => C/|B| = 1/2
    assert sp.simplify(gap - (2 * C - absB)**2 / (4 * C)) == 0
    threshold = sp.solve(sp.Eq(2 * C - absB, 0), C)[0]   # C = |B|/2
    assert sp.simplify(threshold / absB - sp.Rational(1, 2)) == 0
    assert abs(0.5 - SELF_DUAL) > 0.1       # 1/2 != 0.636
    RESULTS['S3_bps_degeneracy'] = {
        'interior_vacuum': 'x* = -B/(2C)',
        'V0_minus_Vint': '(2C-|B|)^2 / (4C)',
        'degeneracy_C_over_B': 0.5,
        'self_dual_C_over_B': SELF_DUAL,
        'verdict': 'Only special ratio the wall picks is the tetragonal->orthorhombic '
                   'threshold C/|B|=1/2 (vacuum existence). 0.636 != 0.5: standard BPS '
                   'does NOT pin the angle (F177-B2 made quantitative).'}
    PASS['S3'] = True


# =====================================================================  V
def test_V_value_discrimination():
    """Derived (bare) solve lands off BOTH 0.63622 and 2/pi by >>1e-4."""
    # the data point itself (the relabel/target): sits at self-dual to ~1e-5
    cos3_data, _ = reduced_cos3delta([ME, MMU, MTAU])
    cob_data = 1.0 / (2.0 * cos3_data)
    d_self = abs(cob_data - SELF_DUAL)
    d_comp = abs(cob_data - COMPETITOR)
    assert d_self < 1e-4            # data matches self-dual value (TARGET)
    assert d_comp > 1e-4            # data is NOT at 2/pi
    # the *derivation* (bare Fierz) cannot discriminate: off both by ~9%
    cob_bare = (2/9) * E6_F118 / B_ABS_F118
    assert abs(cob_bare - SELF_DUAL) > 1e-2
    assert abs(cob_bare - COMPETITOR) > 1e-2
    # m_tau error on the data invariant (Koide-confidence of the target)
    def cob_of_mtau(mt):
        c3, _ = reduced_cos3delta([ME, MMU, mt])
        return 1.0 / (2.0 * c3)
    sig = abs(cob_of_mtau(MTAU + MTAU_ERR) - cob_of_mtau(MTAU - MTAU_ERR)) / 2.0
    RESULTS['V_value_discrimination'] = {
        'self_dual': SELF_DUAL, 'competitor_2_over_pi': COMPETITOR,
        'split': abs(SELF_DUAL - COMPETITOR),
        'data_C_over_B': cob_data,
        'data_minus_self_dual': d_self, 'data_minus_2_over_pi': d_comp,
        'data_sigma_from_mtau': sig,
        'data_pulls_to_self_dual_by_sigma': d_self / sig if sig else None,
        'bare_solve_C_over_B': cob_bare,
        'bare_off_both_by': min(abs(cob_bare - SELF_DUAL), abs(cob_bare - COMPETITOR)),
        'verdict': 'Data SATISFIES the self-dual value to ~1e-5 (the F176/F179 target), '
                   'but the DERIVATION (bare induced rational) lands off BOTH targets by '
                   '~9%. The solve cannot discriminate -> the value is a computed '
                   'nonperturbative number; self-duality must be POSITED. Honest terminus.'}
    PASS['V'] = True


def test_write_results():
    for t in (test_A_anchor_pi_over_4, test_S1_no_second_relation,
              test_S2_alpha_does_not_cancel, test_S3_bps_degeneracy_at_one_half,
              test_V_value_discrimination):
        t()
    RESULTS['summary'] = {
        'verdict': 'FORCED POSIT (honest terminus)',
        'anchor_recovered': True,
        'second_relation_exists': False,
        'alpha_cancels': False,
        'bps_pins_angle': False,
        'derivation_predicts_value': False,
        'checks': {k: ('PASS' if PASS.get(k) else 'FAIL')
                   for k in ['A', 'S1', 'S2', 'S3', 'V']},
        'overall': '5/5 PASS' if all(PASS.get(k) for k in
                   ['A', 'S1', 'S2', 'S3', 'V']) else 'FAIL'}
    out = os.path.join(os.path.dirname(__file__), '..', '..',
                       'test-results', 'F199_angular_self_duality.json')
    with open(os.path.abspath(out), 'w') as f:
        json.dump(RESULTS, f, indent=2)
    assert RESULTS['summary']['overall'] == '5/5 PASS'


if __name__ == '__main__':
    test_A_anchor_pi_over_4()
    test_S1_no_second_relation()
    test_S2_alpha_does_not_cancel()
    test_S3_bps_degeneracy_at_one_half()
    test_V_value_discrimination()
    test_write_results()
    print(json.dumps(RESULTS['summary'], indent=2))
    print("\nKey numbers:")
    print(f"  self-dual 1/(2cos2/3) = {SELF_DUAL:.5f}")
    print(f"  competitor 2/pi       = {COMPETITOR:.5f}  (split {abs(SELF_DUAL-COMPETITOR):.1e})")
    print(f"  data C/|B|            = {RESULTS['V_value_discrimination']['data_C_over_B']:.5f}")
    print(f"  bare Fierz C/|B|      = {RESULTS['V_value_discrimination']['bare_solve_C_over_B']:.5f}")
