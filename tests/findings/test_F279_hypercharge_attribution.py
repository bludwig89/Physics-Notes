"""F279 — Where the hypercharge quantisation constraint actually comes from.

F165 claims the five generation hypercharges are forced, up to one overall
normalisation, by three anomaly rows plus two mass-step rows. This test
re-derives that system independently and adjudicates two of its statements.

CONFIRMED (F165's conclusion stands):
    the hypercharges ARE forced up to one normalisation, over Q.

CORRECTED (F165's attribution and its colour claim do not):

  A1  Once nu_R is carried as a field with a hypercharge and its own Dirac
      mass step, the [grav]^2 U(1) row is IDENTICALLY satisfied by the other
      five constraints -- rank is 5 with or without it. F165's system reaches
      dimension 1 only because it OMITS nu_R from the gravitational trace,
      which is numerically identical to imposing y_nu = 0 without saying so.

  A2  The constraint that actually closes the system is y_nu = 0, and the
      model supplies it independently: the F47 Higgs-free Majorana step
      nu_R^T C nu_R carries hypercharge 2*y_nu, so U(1)_Y invariance of that
      term forces y_nu = 0 exactly. Restoring nu_R and adding the Majorana
      row recovers F165's line exactly -- same rank deficit, same ratios,
      same normalised SM values.

  A3  F165 section 3 states that removing colour breaks the closure ("set the
      multiplicity to 1 and the system no longer closes to a single line").
      It does not. The system closes to a one-dimensional line for EVERY
      N_c, with ratios 1 : (1+N_c) : (1-N_c) : -N_c : -2*N_c, and the cubic
      U(1)^3 anomaly vanishes identically on that line for every N_c too.
      N_c = 3 supplies the VALUE of the fraction (thirds), not the FACT of
      commensurability.

  A4  The single shared mass phase IS load-bearing (F165 attributes this
      correctly to F27/F41): allowing independent down-sector and lepton-
      sector phases returns a 2-dimensional space in which the quark
      hypercharges float.

Convention: standard weak hypercharge y, Q = T_3 + y. F38 quotes Y = 2y.
All arithmetic over sympy Rationals -- residuals are the literal integer 0.

2026-08-06 -- F279 follow-up 1 closed, and this file is where it is guarded.
`check_registry_values_are_on_the_derived_line` asserts that the three lepton
hypercharges in `casim.constants` ARE the solution above at the normalisation
the registry declares, and that `casim.engine.gauge.hypercharge` imports them
instead of writing its own. Before that promotion the module carried them as
literals under a comment reading "SM hypercharge assignment", which is the
opposite of what this finding concluded.
"""

import sympy as sp

yQ, yu, yd, yL, ye, ynu, yphi, ypd, ype = sp.symbols(
    "yQ yu yd yL ye ynu yphi ypd ype", rational=True
)

U7 = [yQ, yu, yd, yL, ye, ynu, yphi]

# --- the model's constraint rows, named ------------------------------------
SU2_ROW = 3 * yQ + yL                      # [SU(2)_L]^2 U(1)
SU3_ROW = 2 * yQ - yu - yd                 # [SU(3)_c]^2 U(1)
GRAV_ROW = 6 * yQ - 3 * yu - 3 * yd + 2 * yL - ye - ynu   # [grav]^2 U(1), nu_R included
MASS_DOWN = yd - (yQ - yphi)               # F27/F41 mass step, down-type
MASS_LEPTON = ye - (yL - yphi)             # F27/F41 mass step, charged lepton
MASS_NU_DIRAC = ynu - (yL + yphi)          # conjugate phase (hypercharge.py DELTA_Y_NU)
MAJORANA = 2 * ynu                         # F47: nu_R^T C nu_R carries 2*y_nu


def _dim(eqs, unknowns):
    """(nullspace dimension, rank) of a linear system over Q."""
    A, _ = sp.linear_eq_to_matrix(eqs, unknowns)
    return len(A.nullspace()), A.rank()


# NOTE (2026-08-02, F287): the five gates below were named `test_*` AND this
# file was registered with an `entry:`, which made the record both a pytest file
# and an entry point -- forbidden in combination (test_registry_entries.py),
# because the two contracts can disagree about what "pass" means. They are
# renamed `check_*`; `check_hypercharge_attribution()` already called all five
# directly, so it is now the single contract and nothing is lost.
def check_F165_own_system_reproduces():
    """F165's published system does give a 1-dimensional space and its ratios."""
    u6 = [yQ, yu, yd, yL, ye, yphi]
    eqs = [
        3 * yQ + yL,
        2 * yQ - yu - yd,
        6 * yQ - 3 * yu - 3 * yd + 2 * yL - ye,   # nu_R absent, as published
        yd - (yQ - yphi),
        ye - (yL - yphi),
    ]
    d, r = _dim(eqs, u6)
    assert (d, r) == (1, 5)
    sol = sp.solve(eqs, [yu, yd, yL, ye, yphi], dict=True)[0]
    ratios = {str(k): sp.simplify(v / yQ) for k, v in sol.items()}
    assert ratios == {"yu": 4, "yd": -2, "yL": -3, "ye": -6, "yphi": 3}


def check_A1_grav_row_is_not_independent_once_nu_R_is_carried():
    """The gravitational anomaly adds no rank once nu_R has a mass step."""
    others = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC]
    _, rank_without = _dim(others, U7)
    _, rank_with = _dim(others + [GRAV_ROW], U7)
    assert rank_without == rank_with == 5, (rank_without, rank_with)

    # and it is not merely dependent -- it is identically zero on the others
    sol = sp.solve(others, [yu, yd, yL, ye, ynu], dict=True)[0]
    assert sp.simplify(GRAV_ROW.subs(sol)) == 0

    # so the anomaly rows + mass rows alone leave TWO free parameters
    d, _ = _dim(others + [GRAV_ROW], U7)
    assert d == 2, "with nu_R carried, F165's rows do not fix the ratios"


def check_A2_majorana_row_is_what_closes_the_system():
    """y_nu = 0, from the F47 Majorana step, restores F165's line exactly."""
    # the Majorana bilinear carries 2*y_nu; gauge invariance forces y_nu = 0
    assert sp.solve(sp.Eq(MAJORANA, 0), ynu) == [0]

    corrected = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC, MAJORANA]
    d, r = _dim(corrected, U7)
    assert (d, r) == (1, 6)

    sol = sp.solve(corrected, [yu, yd, yL, ye, ynu, yphi], dict=True)[0]
    ratios = {str(k): sp.simplify(v / yQ) for k, v in sol.items()}
    assert ratios == {"yu": 4, "yd": -2, "yL": -3, "ye": -6, "ynu": 0, "yphi": 3}

    # both anomalies are consistency checks on that line, not constraints
    cubic = (6 * yQ ** 3 - 3 * yu ** 3 - 3 * yd ** 3
             + 2 * yL ** 3 - ye ** 3 - ynu ** 3)
    assert sp.simplify(sp.expand(GRAV_ROW.subs(sol))) == 0
    assert sp.simplify(sp.expand(cubic.subs(sol))) == 0

    # normalising yQ = 1/6 gives the F38 table over Q (Y = 2y)
    Y = {k: 2 * sp.Rational(1, 6) * v for k, v in ratios.items()}
    assert Y == {"yu": sp.Rational(4, 3), "yd": sp.Rational(-2, 3),
                 "yL": -1, "ye": -2, "ynu": 0, "yphi": 1}


def check_A3_closure_holds_for_every_N_c():
    """F165 section 3 is wrong: colour multiplicity does not gate the closure."""
    N = sp.symbols("N", positive=True, integer=True)
    u6 = [yQ, yu, yd, yL, ye, yphi]
    eqs = [
        N * yQ + yL,
        2 * yQ - yu - yd,
        2 * N * yQ - N * yu - N * yd + 2 * yL - ye,
        yd - (yQ - yphi),
        ye - (yL - yphi),
    ]
    sol = sp.solve(eqs, [yu, yd, yL, ye, yphi], dict=True)[0]
    assert sp.simplify(sol[yu] / yQ - (N + 1)) == 0
    assert sp.simplify(sol[yd] / yQ - (1 - N)) == 0
    assert sp.simplify(sol[yL] / yQ + N) == 0
    assert sp.simplify(sol[ye] / yQ + 2 * N) == 0

    # explicitly at N_c = 1, the case F165 says fails
    for Nc in (1, 2, 3, 4, 5):
        e = [Nc * yQ + yL, 2 * yQ - yu - yd,
             2 * Nc * yQ - Nc * yu - Nc * yd + 2 * yL - ye,
             yd - (yQ - yphi), ye - (yL - yphi)]
        d, r = _dim(e, u6)
        assert (d, r) == (1, 5), f"N_c={Nc} gave dim {d}, rank {r}"

    # the cubic anomaly is identically zero for every N_c, so it selects nothing
    cubic = 2 * N * yQ ** 3 - N * yu ** 3 - N * yd ** 3 + 2 * yL ** 3 - ye ** 3
    assert sp.simplify(sp.expand(cubic.subs(sol))) == 0


def check_A4_single_mass_phase_is_load_bearing():
    """Two independent mass phases and the quark hypercharges float."""
    u8 = [yQ, yu, yd, yL, ye, ynu, ypd, ype]
    eqs = [3 * yQ + yL, 2 * yQ - yu - yd,
           yd - (yQ - ypd), ye - (yL - ype), ynu - (yL + ype), ynu]
    d, _ = _dim(eqs, u8)
    assert d == 2
    sol = sp.solve(eqs, [yu, yd, yL, ye, ynu, ype], dict=True)[0]
    # y_d and y_u still depend on the free down-sector phase
    assert ypd in sp.simplify(sol[yd]).free_symbols
    assert ypd in sp.simplify(sol[yu]).free_symbols


def _rational(x):
    """A registry Fraction as an exact sympy Rational (never via float)."""
    return sp.Rational(x.numerator, x.denominator)


def check_registry_values_are_on_the_derived_line():
    """F279 follow-up 1: the code must hold THIS line, not a remembered table.

    Added 2026-08-06, when the three lepton hypercharges stopped being literals
    in `casim.engine.gauge.hypercharge` and became `casim.constants` entries.
    Until then the module wrote them under a comment reading "SM hypercharge
    assignment" — the one live code-vs-finding contradiction the 2026-08-04
    completeness sweep still carried.

    This is the check that makes the promotion mean something: it ties the
    registered VALUES to the system solved above, in the module's own
    convention (Y = 2y, Q = T_3 + Y/2), and normalises by the registry's own
    Y_L rather than by a chosen y_Q — so the assertion tests the ratios F279
    derives, not the unit F279 leaves free.
    """
    # This file is runnable standalone (`python3 <path>`) as well as through
    # the registry, and only THIS check needs the package -- the rest is pure
    # sympy. Bootstrap src/ locally rather than at module level, so the
    # dependency stays where it is used.
    import os
    import sys
    _src = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "src")
    if _src not in sys.path:
        sys.path.insert(0, _src)

    from casim.constants import Y_LEPTON_L, Y_E_R, Y_NU_R, get
    from casim.engine.gauge import hypercharge as hy

    corrected = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC, MAJORANA]
    sol = sp.solve(corrected, [yu, yd, yL, ye, ynu, yphi], dict=True)[0]

    # Solve for the unit from the registry's declared normalisation: Y_L = 2 y_L
    # and y_L = -3 y_Q, so y_Q = Y_L / (2 * (y_L/y_Q)) = 1/6. Nothing here
    # assumes 1/6 -- it is read back out of the registry.
    yQ_star = _rational(Y_LEPTON_L) / (2 * sp.simplify(sol[yL] / yQ))
    assert yQ_star == sp.Rational(1, 6), yQ_star
    at = {yQ: yQ_star}

    assert 2 * sol[yL].subs(at) == _rational(Y_LEPTON_L)
    assert 2 * sol[ye].subs(at) == _rational(Y_E_R)
    assert 2 * sol[ynu].subs(at) == _rational(Y_NU_R)

    # The two that carry no unit freedom at all: y_nu = 0 is forced by the
    # Majorana row, and Y_e = 2 Y_L survives every N_c (A3). Exact on Fractions.
    assert Y_NU_R == 0
    assert Y_E_R == 2 * Y_LEPTON_L

    # Provenance, not just value: an `exact` value with the wrong story is the
    # defect this follow-up closed.
    for sym in ("Y_LEPTON_L", "Y_E_R", "Y_NU_R"):
        c = get(sym)
        assert c.exactness == "exact", (sym, c.exactness)
        assert "F279" in c.provenance, (sym, c.provenance)

    # And the engine module takes them from the registry rather than redefining
    # them -- the mass-step phases still come out +/-1 exactly.
    assert (hy.Y_LEPTON_L, hy.Y_E_R, hy.Y_NU_R) == (Y_LEPTON_L, Y_E_R, Y_NU_R)
    assert hy.DELTA_Y_E == 1 and hy.DELTA_Y_NU == -1
    assert 2 * sol[yphi].subs(at) == hy.DELTA_Y_E      # the Higgs-equivalent y_phi


def check_hypercharge_attribution() -> bool:
    """Registry entry point (D9). Returns True iff every gate above holds."""
    for fn in (check_F165_own_system_reproduces,
               check_A1_grav_row_is_not_independent_once_nu_R_is_carried,
               check_A2_majorana_row_is_what_closes_the_system,
               check_A3_closure_holds_for_every_N_c,
               check_A4_single_mass_phase_is_load_bearing,
               check_registry_values_are_on_the_derived_line):
        fn()
    return True


if __name__ == "__main__":
    print("ALL PASS:", check_hypercharge_attribution())
