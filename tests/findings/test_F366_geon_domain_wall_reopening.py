"""F366 — Is the F238 geon-abundance exclusion scoped to the inflaton/Press-
Schechter route, or does it foreclose every production mechanism?

Four checks, C1-C3 exact-algebraic (sympy, independent of the module's own
internal simplification), C4 structural (a directory search of the six
findings that jointly frame "the geon abundance is a free input").

  C1  (exact)  V(delta) = (A/2)(1 + cos 6 delta) -- the model's own E_g clock
      potential, unchanged from F150/F175/F234/F282 -- has EXACTLY 6 global
      minima per period [0, 2 pi). Re-solved here independently of the module.

  C2  (exact)  Those 6 minima carry identically the same V (confirmed with A
      left symbolic, so it cannot be a numerical coincidence at one A value).

  C3  (exact)  delta -> delta + pi/3 is an EXACT symmetry of V (not merely 6
      minima that happen to agree) -- re-derived independently with a
      different sympy simplification path (trigsimp) from the module's own
      (expand_trig then simplify), to catch a possible simplify() blind spot.

  C4  (structural) None of F238/F228/F282/F283/F284/F285 -- the findings that
      together establish "the geon abundance is a free input, and here is
      exactly why" -- ever mentions a domain wall, topological defect,
      bubble collision, cosmic string or the Kibble mechanism. The exclusion
      was never extended to, or tested against, this channel.

Real arithmetic + sympy only (CLAUDE.md).
"""
from __future__ import annotations

import sympy as sp

from casim.engine.interactions import cosmology_geon_domain_wall_reopening as dw


def check_C1_six_exact_vacua():
    """Independent re-solve: cos(6 delta) = -1 has exactly 6 roots in [0, 2pi)."""
    delta = sp.Symbol("delta", real=True)
    sols = sp.solveset(sp.cos(6 * delta) + 1, delta,
                        domain=sp.Interval.Ropen(0, 2 * sp.pi))
    sols_list = sorted(float(s) for s in sols)
    assert len(sols_list) == 6
    # Independently: they must be evenly spaced by pi/3 starting at pi/6.
    expected = [sp.pi / 6 + sp.pi * n / 3 for n in range(6)]
    for got, exp in zip(sols_list, expected):
        assert abs(got - float(exp)) < 1e-9
    out = dw.z6_degeneracy_exact()
    assert out["n_vacua_exact"] == 6
    return {"n_vacua": len(sols_list), "deltas": sols_list}


def check_C2_vacua_exactly_degenerate():
    """V at each of the 6 minima is identically equal, with A left symbolic."""
    delta, A = sp.symbols("delta A", positive=True)
    V = sp.Rational(1, 2) * A * (1 + sp.cos(6 * delta))
    deltas = [sp.pi / 6 + sp.pi * n / 3 for n in range(6)]
    values = [sp.simplify(V.subs(delta, d)) for d in deltas]
    assert all(sp.simplify(v - values[0]) == 0 for v in values)
    out = dw.z6_degeneracy_exact()
    assert out["exactly_degenerate"] is True
    return {"values": [str(v) for v in values]}


def check_C3_exact_z6_symmetry():
    """delta -> delta + pi/3 is an exact symmetry, re-derived via trigsimp
    (a different simplification path from the module's expand_trig+simplify,
    so this is not just re-running the same code)."""
    delta, A = sp.symbols("delta A", real=True)
    V = sp.Rational(1, 2) * A * (1 + sp.cos(6 * delta))
    shifted = V.subs(delta, delta + sp.pi / 3)
    diff = sp.trigsimp(sp.expand(shifted - V))
    assert sp.nsimplify(diff) == 0
    out = dw.z6_symmetry_exact()
    assert out["identically_zero"] is True
    return {"V_shift_minus_V": str(diff)}


def check_C4_defect_channel_not_previously_examined():
    """Structural fact: the six framing findings never discuss a domain wall /
    topological defect / bubble collision / Kibble / cosmic string channel."""
    out = dw.scope_of_f238_exclusion()
    assert out["defect_channel_previously_discussed"] is False
    for name, rec in out["per_finding"].items():
        assert rec["found_file"] is True, f"{name} file not found"
        assert rec["defect_terms_present"] == []
    return out


def run_all():
    results = {
        "C1_six_exact_vacua": check_C1_six_exact_vacua(),
        "C2_vacua_exactly_degenerate": check_C2_vacua_exactly_degenerate(),
        "C3_exact_z6_symmetry": check_C3_exact_z6_symmetry(),
        "C4_defect_channel_not_previously_examined": check_C4_defect_channel_not_previously_examined(),
    }
    module_result = dw.run_all()
    assert module_result["all_checks_pass"] is True
    results["module_all_checks_pass"] = module_result["all_checks_pass"]
    results["module_reused_clock_amplitude_A"] = module_result["reused_clock_amplitude_A"]
    return results


def test_all():
    results = run_all()
    for key in ("C1_six_exact_vacua", "C2_vacua_exactly_degenerate",
                "C3_exact_z6_symmetry", "C4_defect_channel_not_previously_examined"):
        assert key in results
    assert results["module_all_checks_pass"] is True


if __name__ == "__main__":
    import json
    from pathlib import Path

    r = run_all()
    print(json.dumps(r, indent=2, default=str))
    out = Path(__file__).resolve().parents[2] / "test-results" / "F366_geon_domain_wall_reopening_test.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=2, default=str)
