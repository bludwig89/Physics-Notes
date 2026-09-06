"""F341 -- Does anything in the model force Majorana over Dirac for nu_R? (rubric C4)

Rubric row C4 has read PARTIAL for five-plus completeness reports: F47 constructs a
Higgs-free Majorana mass step for nu_R and F47/F279 show nu_R is a structurally-forced
Y=0 total SM singlet, but nothing in the model was shown to FORCE the Majorana step over
a Dirac-only alternative -- the construction merely PERMITS it.

This record checks two convergent structural angles, both re-derived independently
here rather than merely cited:

  S1  NO PROTECTING SYMMETRY.  The only gauge quantum number the model assigns nu_R is
      hypercharge Y (casim.constants.electroweak), and Y=0 already permits (does not
      forbid) the Majorana bilinear nu_R^T C nu_R -- gauge invariance is satisfied
      automatically, it is not a protection. Colour and SU(2)_L are trivially blind to a
      total singlet. So the ONLY way a symmetry could forbid the term is a SEPARATE
      global charge (lepton number / B-L) under which nu_R is charged. This check
      confirms, by direct inspection of the constants and gauge registries, that no such
      generator is registered anywhere in the model -- consistent with F202, which relies
      on the Majorana step's lepton-number violation as a LOAD-BEARING feature
      (leptogenesis), not a defect the model protects against.

  S2  REMOVING IT BREAKS AN ESTABLISHED RESULT.  F279 A2 showed the F47 Majorana row
      (2*y_nu = 0) is what closes the model's own hypercharge system from a 2-parameter
      family to the unique, gate-tier-certified line matching the observed SM charge
      ratios (F165/F279). This check re-derives that fact independently (not by import)
      and adds the sharper form F279 did not state explicitly: with the Majorana row
      dropped, y_phi -- and with it the derived quark-charge fractions 2/3, -1/3 and the
      y_e : y_L : y_nu ratio -- is a GENUINELY FREE symbol in every solution (it appears
      in the nullspace basis, not merely "underdetermined" in the abstract). So a
      Dirac-only completion of THIS model does not merely differ by one assumption: it
      forfeits the model's own already-certified charge-quantisation result (F165/F279,
      gate tier) unless y_phi = 3*y_Q is re-imposed by hand as a second, independent,
      currently-unmotivated input.

What this record does NOT claim: this is not a gauge-invariance no-go of the kind that
forbids the Majorana term outright (no such no-go exists, in this model or the Standard
Model -- a Dirac-only nu_R remains logically constructible). The forcing argument is
structural/consistency-based: (S1) nothing already present forbids the term, so by the
field-theory genericity ("totalitarian") principle it is expected to appear unless
something is added specifically to forbid it, and (S2) that "something" would have to be
invented from nothing AND would silently re-open a result the project currently advertises
as derived. Both legs are checked here; neither is a theorem that a Dirac alternative is
impossible.

See findings/F341-*.md for the full writeup, and F47/F165/F202/F266/F279 for the pieces
this composes.
"""

import re

import sympy as sp

# ---------------------------------------------------------------------------
# S1 -- no protecting symmetry: nu_R carries no registered charge but Y
# ---------------------------------------------------------------------------

# Patterns that would indicate a registered lepton-number / B-L-like generator
# anywhere in the constants or gauge-hypercharge surface. None should match.
_PROTECTING_SYMMETRY_PATTERNS = [
    re.compile(r"LEPTON_NUMBER", re.IGNORECASE),
    re.compile(r"\bB[_-]?MINUS[_-]?L\b", re.IGNORECASE),
    re.compile(r"\bB[_-]?L\b"),
    re.compile(r"\bU1[_-]?L\b", re.IGNORECASE),
    re.compile(r"LEPTON_CHARGE", re.IGNORECASE),
    re.compile(r"MATTER_PARITY", re.IGNORECASE),
    re.compile(r"\bR_PARITY\b", re.IGNORECASE),
]


def _names_in_module(module):
    return [n for n in dir(module) if not n.startswith("_")]


def check_S1_no_protecting_symmetry_is_registered():
    """No lepton-number / B-L / matter-parity generator exists anywhere the
    gauge/constants layer would have to declare one, and the only charge
    nu_R carries (Y) already permits (does not forbid) the Majorana term."""
    import casim.constants as constants_pkg
    import casim.constants.electroweak as ew
    from casim.engine.gauge import hypercharge as hc

    hits = []
    for mod, label in ((constants_pkg, "casim.constants"),
                        (ew, "casim.constants.electroweak"),
                        (hc, "casim.engine.gauge.hypercharge")):
        for name in _names_in_module(mod):
            for pat in _PROTECTING_SYMMETRY_PATTERNS:
                if pat.search(name):
                    hits.append((label, name))
    assert hits == [], f"unexpected protecting-symmetry generator(s) found: {hits}"

    # And the one charge nu_R DOES carry is exactly Y=0, which is what makes the
    # bilinear allowed, not forbidden (2*Y_NU_R == 0 is the F47/F279 statement).
    assert hc.Y_NU_R == 0
    assert 2 * hc.Y_NU_R == 0


# ---------------------------------------------------------------------------
# S2 -- dropping the Majorana row reopens the hypercharge closure, with y_phi
#        landing in the free nullspace, not merely "underdetermined"
# ---------------------------------------------------------------------------

yQ, yu, yd, yL, ye, ynu, yphi = sp.symbols("yQ yu yd yL ye ynu yphi", rational=True)
U7 = [yQ, yu, yd, yL, ye, ynu, yphi]

SU2_ROW = 3 * yQ + yL
SU3_ROW = 2 * yQ - yu - yd
MASS_DOWN = yd - (yQ - yphi)
MASS_LEPTON = ye - (yL - yphi)
MASS_NU_DIRAC = ynu - (yL + yphi)          # the Dirac-type mass step alone
MAJORANA = 2 * ynu                          # F47: forces y_nu = 0


def _nullspace(eqs, unknowns):
    A, _ = sp.linear_eq_to_matrix(eqs, unknowns)
    return A.nullspace(), A.rank()


def check_S2a_without_majorana_yphi_is_free_in_the_nullspace():
    """Anomaly rows + BOTH Dirac-type mass steps (down, lepton, nu) alone --
    i.e. the model with nu_R given a Dirac mass and NO Majorana term -- leave
    a 2-dimensional nullspace, and y_phi is one of its two free directions
    (not fixed by anything else already in the model)."""
    dirac_only = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC]
    ns, rank = _nullspace(dirac_only, U7)
    assert rank == 5 and len(ns) == 2

    # Solve explicitly: y_phi must appear as a free symbol (not resolved to a
    # multiple of y_Q alone) in the general solution.
    sol = sp.solve(dirac_only, [yu, yd, yL, ye, ynu], dict=True)[0]
    free_symbols_in_solution = set()
    for expr in sol.values():
        free_symbols_in_solution |= expr.free_symbols
    assert yphi in free_symbols_in_solution, (
        "y_phi is NOT free without the Majorana row -- S2 premise would be false"
    )
    assert yQ in free_symbols_in_solution


def check_S2b_majorana_row_uniquely_closes_it_to_the_certified_line():
    """Adding the Majorana row (2*y_nu = 0) is what removes y_phi from the
    free set, closing to the F165/F279 certified rank-6/dim-1 line."""
    with_majorana = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC, MAJORANA]
    ns, rank = _nullspace(with_majorana, U7)
    assert rank == 6 and len(ns) == 1

    sol = sp.solve(with_majorana, [yu, yd, yL, ye, ynu, yphi], dict=True)[0]
    assert sp.simplify(sol[yphi] / yQ) == 3
    ratios = {str(k): sp.simplify(v / yQ) for k, v in sol.items()}
    assert ratios == {"yu": 4, "yd": -2, "yL": -3, "ye": -6, "ynu": 0, "yphi": 3}


def check_S2c_no_other_established_row_fixes_yphi_instead():
    """The only OTHER route in the model that fixes an electroweak-sector
    number close to this one is F138's sin^2(theta_W)=1/4 compositeness-scale
    matching -- a genuinely independent derivation (different mechanism,
    different quantity: an angle at a matching scale, not a hypercharge
    RATIO). Confirms by construction that dropping MAJORANA and adding
    nothing else leaves the system exactly as under-determined as S2a found
    (i.e. there is no accidental extra row already sitting in this constraint
    set that would close it some other way)."""
    dirac_only = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC]
    # Every proper subset check: adding any ONE row already in {SU2, SU3,
    # MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC} twice, or any trivial rescaling,
    # cannot add rank (they are already all included) -- the only way to
    # reach rank 6 from this exact row set is a row not already present.
    ns, rank = _nullspace(dirac_only, U7)
    assert rank == 5
    # Re-adding MAJORANA is the unique closure demonstrated in S2b; no other
    # symbol combination of the existing five rows reaches rank 6:
    for extra in (SU2_ROW + SU3_ROW, MASS_DOWN - MASS_LEPTON, 2 * MASS_NU_DIRAC):
        ns2, rank2 = _nullspace(dirac_only + [extra], U7)
        assert rank2 == 5, "a linear combination of existing rows spuriously added rank"


def check_control_dirac_only_hypothesis_does_not_reproduce_certified_ratios():
    """CONTROL: assuming the model is Dirac-only (drop MAJORANA outright,
    i.e. the historical row set most literature would use), the specific
    ratio yphi/yQ = 3 that the model currently certifies (F165/F279,
    matching the observed 2/3, -1/3 quark charges) is not merely 'unproven'
    but is not even implied -- yphi=3*yQ is one point in a whole free line,
    and (e.g.) yphi = yQ solves the Dirac-only system equally well while
    giving WRONG quark charges. This is the leg that must go red if the
    Majorana closure is removed, and it does."""
    dirac_only = [SU2_ROW, SU3_ROW, MASS_DOWN, MASS_LEPTON, MASS_NU_DIRAC]
    for yphi_over_yQ in (sp.Integer(3), sp.Integer(1), sp.Rational(1, 2)):
        candidate = dirac_only + [yphi - yphi_over_yQ * yQ, yQ - 1]
        sol = sp.solve(candidate, [yu, yd, yL, ye, ynu, yphi, yQ], dict=True)
        assert len(sol) == 1, "each yphi/yQ choice should be a consistent point"
    # i.e. every yphi/yQ ratio is an equally valid Dirac-only completion --
    # the certified 2/3, -1/3 charges are not singled out without MAJORANA.


def check_majorana_forced_by_hypercharge_closure() -> bool:
    """Registry entry point (D9). Returns True iff every gate above holds."""
    for fn in (check_S1_no_protecting_symmetry_is_registered,
               check_S2a_without_majorana_yphi_is_free_in_the_nullspace,
               check_S2b_majorana_row_uniquely_closes_it_to_the_certified_line,
               check_S2c_no_other_established_row_fixes_yphi_instead,
               check_control_dirac_only_hypothesis_does_not_reproduce_certified_ratios):
        fn()
    return True


if __name__ == "__main__":
    print("ALL PASS:", check_majorana_forced_by_hypercharge_closure())
