"""[PARTIALLY SUPERSEDED 2026-08-02 by F279 — ledger S13-F279-hypercharge-attribution]

  DEAD:
    The reading of the [grav]^2 U(1) row as an independent constraint, and
    F165 section 3's claim that colour multiplicity gates the closure. The
    test's own arithmetic is correct and still passes -- it is the
    interpretation of the 5-row system that moved.

  STILL LIVE:
    Q1 dimension-1 result, Q2 cubic-identically-zero, Q3 F38 table
    reproduction, Q4 GMN electric charges. All four still hold and are
    re-derived independently by F279.

  See docs/theory/supersessions.yaml for the full record.

F165 — Hypercharge quantisation from anomaly cancellation + mass-step gauge invariance.

Claim: given the lattice-fixed representation content of one Standard-Model
generation (colour-triplet quarks, SU(2)_L doublets/singlets, the F51
sublattice U(1)_Y carrier), the five hypercharges are NOT independent inputs.
The linear constraint system

    anomaly  [SU(2)]^2 U(1)         3 y_Q + y_L                       = 0
    anomaly  [SU(3)]^2 U(1)         2 y_Q - y_u - y_d                 = 0
    anomaly  [grav]^2  U(1)         6 y_Q - 3 y_u - 3 y_d + 2 y_L - y_e = 0
    mass     down-type   (Q,d)      y_d - (y_Q - y_phi)               = 0
    mass     lepton      (L,e)      y_e - (y_L - y_phi)               = 0

has a ONE-dimensional solution space over Q (a line through the origin), so all
six hypercharges (y_Q, y_u, y_d, y_L, y_e, y_phi) are fixed up to a single
overall normalisation. The pure-cubic U(1)^3 anomaly is then satisfied
IDENTICALLY on that line (a consistency check, not an extra constraint).
Normalising y_Q = 1/6 reproduces the SM / F38 assignments exactly over Q.

All arithmetic uses sympy.Rational — residuals are the literal integer 0, not
a float near zero (cf. F38 §5).

Convention here: standard weak hypercharge y, with Q = T_3 + y.
F38 quotes Y = 2y in the Q = T_3 + Y/2 convention; both are printed.
"""

import json
import os
import sympy as sp

RESULT = os.path.join(
    os.path.dirname(__file__), "..", "..", "test-results",
    "hypercharge_quantisation.json",
)


def build_system():
    yQ, yu, yd, yL, ye, yphi = sp.symbols("yQ yu yd yL ye yphi", rational=True)
    unknowns = [yQ, yu, yd, yL, ye, yphi]

    linear = [
        ("SU(2)^2 U(1) anomaly", 3*yQ + yL),
        ("SU(3)^2 U(1) anomaly", 2*yQ - yu - yd),
        ("[grav]^2 U(1) anomaly", 6*yQ - 3*yu - 3*yd + 2*yL - ye),
        ("down-type mass-step invariance", yd - (yQ - yphi)),
        ("lepton mass-step invariance",   ye - (yL - yphi)),
    ]
    cubic = 6*yQ**3 - 3*yu**3 - 3*yd**3 + 2*yL**3 - ye**3  # U(1)^3
    return unknowns, linear, cubic


def main():
    unknowns, linear, cubic = build_system()
    yQ, yu, yd, yL, ye, yphi = unknowns

    # --- A. solution space of the linear system over Q ---
    A, _ = sp.linear_eq_to_matrix([e for _, e in linear], unknowns)
    nullspace = A.nullspace()
    dim = len(nullspace)

    # --- B. solve, parametrised by yQ ---
    sol = sp.solve([e for _, e in linear], [yu, yd, yL, ye, yphi], dict=True)[0]
    ratios = {  # everything as a multiple of yQ
        "yQ": sp.Integer(1),
        "yu": sp.simplify(sol[yu] / yQ),
        "yd": sp.simplify(sol[yd] / yQ),
        "yL": sp.simplify(sol[yL] / yQ),
        "ye": sp.simplify(sol[ye] / yQ),
        "yphi": sp.simplify(sol[yphi] / yQ),
    }

    # --- C. cubic anomaly identically zero on the solution line? ---
    cubic_on_line = sp.simplify(cubic.subs(sol))  # still a function of yQ
    cubic_zero = (cubic_on_line == 0)

    # --- D. normalise yQ = 1/6 -> SM values; compare to F38 (Y = 2y) ---
    norm = {k: sp.Rational(1, 6) * v for k, v in ratios.items()}
    Y_F38 = {k: 2 * v for k, v in norm.items()}  # Q = T3 + Y/2 convention
    F38_table = {"yQ": sp.Rational(1, 3), "yu": sp.Rational(4, 3),
                 "yd": sp.Rational(-2, 3), "yL": sp.Integer(-1),
                 "ye": sp.Integer(-2)}
    f38_match = all(Y_F38[k] == F38_table[k] for k in F38_table)

    # --- E. electric charges via Gell-Mann-Nishijima Q = T3 + y ---
    charges = {
        "u":  sp.Rational(1, 2) + norm["yQ"],
        "d": -sp.Rational(1, 2) + norm["yQ"],
        "nu": sp.Rational(1, 2) + norm["yL"],
        "e": -sp.Rational(1, 2) + norm["yL"],
        "e_R(singlet)": norm["ye"],   # T3 = 0
        "u_R(singlet)": norm["yu"],
        "d_R(singlet)": norm["yd"],
    }
    charges_ok = (charges["u"] == sp.Rational(2, 3) and
                  charges["d"] == sp.Rational(-1, 3) and
                  charges["nu"] == 0 and charges["e"] == -1)

    results = {
        "linear_solution_dimension": dim,
        "dimension_is_one": dim == 1,
        "ratios_to_yQ": {k: str(v) for k, v in ratios.items()},
        "cubic_U1_cubed_on_solution_line": str(cubic_on_line),
        "cubic_identically_zero": bool(cubic_zero),
        "normalised_y (yQ=1/6)": {k: str(v) for k, v in norm.items()},
        "Y_F38_convention (Y=2y)": {k: str(v) for k, v in Y_F38.items()},
        "matches_F38_table": bool(f38_match),
        "electric_charges": {k: str(v) for k, v in charges.items()},
        "charges_match_SM": bool(charges_ok),
    }

    checks = {
        "Q1 linear solution space is 1-dimensional": dim == 1,
        "Q2 U(1)^3 anomaly identically zero on the line": bool(cubic_zero),
        "Q3 normalised Y reproduces F38 table exactly (over Q)": bool(f38_match),
        "Q4 electric charges are SM (2/3,-1/3,0,-1) over Q": bool(charges_ok),
    }
    results["checks"] = checks
    results["all_pass"] = all(checks.values())

    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w") as fh:
        json.dump(results, fh, indent=2)

    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("ratios (multiple of yQ):", results["ratios_to_yQ"])
    print("F38 Y:", results["Y_F38_convention (Y=2y)"])
    print("charges:", results["electric_charges"])
    print("ALL PASS:", results["all_pass"])
    assert results["all_pass"], "F165 hypercharge-quantisation checks failed"


if __name__ == "__main__":
    main()
