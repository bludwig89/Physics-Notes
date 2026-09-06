"""
F339 — F127's four-avenue alpha_em no-go, characterized
=========================================================

This is NOT a derivation of alpha_em. It re-verifies, independently and from
scratch, the two algebraic facts that F127's avenues A and D reopening
conditions rest on (Ward transversality of the one-loop vacuum polarization;
the rank of the hypercharge-quantization linear system), cross-checks the
mu_star = 4*pi*v structural identification (F138) against the E_lat/mu_star
ratio F127 itself computed, and documents why a superficially tempting
"e^-34 e-foldings" reading of that ratio is tautological and carries no
independent information (a rejected-idea record, not a result).

See findings/F339-alpha-em-nogo-reopening-conditions.md for the full writeup.

RESULT: 4/4 PASS

Date: 2026-08-31
"""

import json
import os
import numpy as np
import sympy as sp

RESULTS = {}


def test_ward_transversality_exact():
    """Avenue A's reopening condition rests on q_mu Pi^mu_nu(q) = 0 being an
    exact identity for the transverse tensor structure, independent of which
    module computes it. Re-derive it from scratch with generic symbolic q.

    (F251/F277 compute this on the model's actual one-loop fermion-bubble
    kernel; this check re-derives the pure tensor-algebra identity that
    result depends on, without importing casim, as an independent check.)
    """
    q0, q1, q2, q3, Pi = sp.symbols('q0 q1 q2 q3 Pi', real=True)
    q = sp.Matrix([q0, q1, q2, q3])
    eta = sp.diag(1, -1, -1, -1)
    q2_scalar = (q.T * eta * q)[0, 0]

    # Pi^{mu nu} = Pi(q^2) * (q^2 eta^{mu nu} - q^mu q^nu)
    Pi_munu = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            Pi_munu[mu, nu] = Pi * (q2_scalar * eta[mu, nu] - q[mu] * q[nu])

    # contract with q_mu = eta_{mu alpha} q^alpha
    q_lower = eta * q
    contraction = sp.simplify((q_lower.T * Pi_munu))
    contraction = sp.Matrix([sp.expand(c) for c in contraction])

    is_zero = all(sp.simplify(c) == 0 for c in contraction)

    RESULTS['ward_transversality'] = {
        'verdict': 'EXACT_ZERO' if is_zero else 'FAIL',
        'contraction': [str(c) for c in contraction],
    }
    assert is_zero, f"q_mu Pi^munu did not vanish identically: {contraction}"
    return True


def test_hypercharge_rank_one_free_direction():
    """Avenue D's reopening condition rests on hypercharge quantisation
    (F165/F279) fixing RATIOS only -- rank 6 in 7 unknowns, nullspace dim 1.
    Re-derive the rank from the six constraint rows independently.

    Unknowns, in order: y_Q, y_u, y_d, y_L, y_e, y_nu, y_phi
    Rows (F279 section 4):
      [SU(2)_L]^2 U(1):     3 y_Q + y_L = 0
      [SU(3)_c]^2 U(1):     2 y_Q - y_u - y_d = 0
      mass step (Q,d):      y_d = y_Q - y_phi   ->  y_Q - y_d - y_phi = 0
      mass step (L,e):      y_e = y_L - y_phi   ->  y_L - y_e - y_phi = 0
      mass step (L,nu):     y_nu = y_L + y_phi  ->  y_L - y_nu + y_phi = 0
      F47 Majorana:         2 y_nu = 0
    """
    # columns: y_Q, y_u, y_d, y_L, y_e, y_nu, y_phi
    rows = [
        [3, 0, 0, 1, 0, 0, 0],
        [2, -1, -1, 0, 0, 0, 0],
        [1, 0, -1, 0, 0, 0, -1],
        [0, 0, 0, 1, -1, 0, -1],
        [0, 0, 0, 1, 0, -1, 1],
        [0, 0, 0, 0, 0, 2, 0],
    ]
    M = sp.Matrix(rows)
    rank = M.rank()
    n_unknowns = M.shape[1]
    nullspace_dim = n_unknowns - rank

    # Confirm the derived ratio line matches F279's stated result on that
    # nullspace, up to the free overall scale y_Q.
    ns = M.nullspace()
    assert len(ns) == 1
    v = ns[0]
    v = v / v[0]  # normalize to y_Q = 1
    expected_ratio = sp.Matrix([sp.Rational(1), sp.Rational(4), sp.Rational(-2),
                                 sp.Rational(-3), sp.Rational(-6), sp.Rational(0),
                                 sp.Rational(3)])
    ratios_match = sp.simplify(v - expected_ratio) == sp.zeros(7, 1)

    RESULTS['hypercharge_rank'] = {
        'verdict': 'RANK_6_NULLSPACE_1' if (rank == 6 and nullspace_dim == 1) else 'FAIL',
        'rank': rank,
        'nullspace_dim': nullspace_dim,
        'ratios_match_F279': bool(ratios_match),
        'ratio_line': [str(x) for x in v],
    }
    assert rank == 6 and nullspace_dim == 1, f"rank={rank}, expected 6"
    assert ratios_match, f"nullspace line {v} does not match F279's stated ratios"
    return True


def test_mu_star_is_4pi_v_not_a_lattice_scale():
    """Avenue B's reopening condition: mu_star is structural (F138: 4*pi*v)
    but that structure constrains sin^2(theta_W)/v, not alpha -- and the
    lattice-scale ratio F127 computed is still tiny regardless. Both must be
    true simultaneously for the resolution in the finding's Sec.3 to hold.
    """
    G_F = 1.1663788e-5          # GeV^-2 (PDG)
    v = (np.sqrt(2) * G_F) ** (-0.5)   # GeV
    mu_star_4piv = 4 * np.pi * v

    F138_quoted_4piv = 3094.0     # GeV, "3.094 TeV" as quoted in F138
    F138_quoted_higgsfree_cross = 3420.0   # GeV, "mu_x = 3.42 TeV" (Higgs-free running)

    agree_with_F138_quote = abs(mu_star_4piv - F138_quoted_4piv) / F138_quoted_4piv
    ln_offset_vs_crossing = abs(np.log(mu_star_4piv / F138_quoted_higgsfree_cross))

    # Lattice scale, as in F127's own avenue B (recomputed independently here)
    LP_SI = 1.616255e-35
    A_OVER_LP = np.sqrt(8 * np.pi) * 3 ** 0.25
    A_SI = A_OVER_LP * LP_SI
    HBAR = 1.054572e-34
    C_SI = 2.998e8
    E_LAT_GEV = HBAR * C_SI / A_SI / 1.602177e-10
    ratio_to_lattice = mu_star_4piv / E_LAT_GEV

    structural_pass = agree_with_F138_quote < 0.01          # v-derivation reproduces F138's quoted number
    scale_matching_pass = ln_offset_vs_crossing < 0.15       # F138's own "~10%" NDA-order match
    still_tiny_vs_lattice = ratio_to_lattice < 1e-10          # avenue B's original observation still holds

    RESULTS['mu_star'] = {
        'verdict': 'STRUCTURAL_BUT_NOT_ALPHA_CONSTRAINING',
        'v_GeV': v,
        'mu_star_4piv_GeV': mu_star_4piv,
        'agree_with_F138_quote': agree_with_F138_quote,
        'ln_offset_vs_higgsfree_crossing': ln_offset_vs_crossing,
        'E_lat_GeV': E_LAT_GEV,
        'mu_star_over_E_lat': ratio_to_lattice,
    }
    assert structural_pass, f"4*pi*v = {mu_star_4piv} does not reproduce F138's quoted 3.094 TeV"
    assert scale_matching_pass, f"ln-offset {ln_offset_vs_crossing} exceeds F138's own NDA band"
    assert still_tiny_vs_lattice, f"ratio {ratio_to_lattice} unexpectedly not tiny"
    return True


def test_log_ratio_coincidence_is_tautological():
    """Documented rejected idea: mu_star/E_lat ~ exp(-34) is NOT independent
    evidence of a 34-e-folding RG mechanism, because r = exp(-ln(1/r)) for
    ANY ratio r -- the identity carries zero information about physics.
    Asserted here, mechanically, for several unrelated ratios, so this
    specific dead end is not re-attempted by a future session.
    """
    test_ratios = [2e-15, 0.5, 1e-3, 1.0 / 137.036, np.pi / 1e6]
    checks = []
    for r in test_ratios:
        reconstructed = np.exp(-np.log(1.0 / r))
        checks.append(abs(reconstructed - r) / r < 1e-12)

    all_tautological = all(checks)

    RESULTS['log_ratio_tautology'] = {
        'verdict': 'TAUTOLOGICAL_NO_INFORMATION' if all_tautological else 'FAIL',
        'ratios_checked': test_ratios,
        'reason': 'r == exp(-ln(1/r)) identically for any r>0; "the log of the ratio '
                  'looks like a round e-folding count" is not evidence of an RG mechanism '
                  'unless that count is reproduced by an independent beta-function '
                  'integration. No such independent calculation exists for mu_star/E_lat.',
    }
    assert all_tautological
    return True


if __name__ == '__main__':
    tests = [
        ('ward_transversality', 'Ward transversality, re-derived symbolically',
         test_ward_transversality_exact),
        ('hypercharge_rank', 'Hypercharge rank 6/7 (one free direction)',
         test_hypercharge_rank_one_free_direction),
        ('mu_star', 'mu_star = 4*pi*v, structural but not alpha-constraining',
         test_mu_star_is_4pi_v_not_a_lattice_scale),
        ('log_ratio_tautology', 'log-ratio "34 e-foldings" rejected as tautological',
         test_log_ratio_coincidence_is_tautological),
    ]

    print("=" * 72)
    print("F339 — F127 reopening-condition characterization")
    print("=" * 72)

    passed = 0
    for tag, label, fn in tests:
        try:
            fn()
            status = "PASS"
            passed += 1
        except Exception as e:
            status = f"FAIL ({e})"
        v = RESULTS.get(tag, {}).get('verdict', '')
        print(f"  {tag:10s} {label:55s} {status:6s} [{v}]")

    results_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results')
    os.makedirs(results_dir, exist_ok=True)
    out_path = os.path.join(results_dir, 'F339_alpha_em_reopening_conditions.json')

    def convert(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj

    summary = {
        'finding': 'F339',
        'date': '2026-08-31',
        'overall': f'{passed}/{len(tests)} PASS',
        'checks': convert(RESULTS),
        'conclusion': (
            'F127 four-avenue no-go re-examined per the D#14 ledger prompt. Avenue A '
            'narrowed (Ward transversality now independently re-verified, not just '
            'imported QED lore -- reopening requires a specific composite-photon '
            'form-factor effect, no candidate named). Avenue B premise corrected: '
            'mu_star=4*pi*v IS structural (F138, one day after F127) but constrains v, '
            'not alpha -- folds into D#17, not D#14. Avenue C: a Dirac-monopole route is '
            'the one genuinely unexplored fifth avenue (zero mentions in the whole '
            'findings index), flagged but not attempted. Avenue D confirmed still open '
            'and precisely bounded: hypercharge quantisation is rank 6/7, ratios only, '
            'independently re-derived here. alpha_em stays OPEN; the grade change is '
            'characterization, not a result.'
        )
    }
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Results -> {out_path}")
    print(f"  {passed}/{len(tests)} PASS")
    print("=" * 72)
