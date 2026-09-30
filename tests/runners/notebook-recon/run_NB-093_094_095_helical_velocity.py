"""
NB-093 (p.73): helical trajectory X(t) = r cos(2 pi nu t) xhat + r sin(2 pi nu t) yhat + a t zhat;
v.v = 4 pi^2 nu^2 r^2 + a^2; v_eff = sqrt(c^2 - 4 pi^2 nu^2 r^2).
NB-094 (p.73-74): attempted link via hbar^2 omega^2 = hbar^2 nu^2 c^2 + m^2 c^4 (dimensionally
questionable -- nu here is being conflated with a wavenumber, not the helix frequency);
hbar^2 omega^2 / (m^2 c^2) = v^2 + c^2, giving v_eff -> infinity as omega increases; author
flags "That isn't right!" (DEAD-END-AUTHOR-CALLED-IT, already assigned).
NB-095 (p.74): corrected attempt using relativistic p = m0 v/sqrt(1-v^2/c^2):
    hbar^2 omega^2 = m0^2 v^2 c^2/(1-v^2/c^2) + m0^2 c^4
    ... algebra ...
    v^2 = c^2 - m0^2 c^4/(hbar^2 omega^2) = c^2 - E0^2/E^2
author flags "Way way -- no good."

This script (a) redoes NB-095's algebra symbolically from the SAME starting equation to see if
v^2 = c^2 - E0^2/E^2 is what it actually gives; (b) compares against the independently-known
correct relativistic GROUP velocity relation v_group = dE/dp = c sqrt(1 - E0^2/E^2) (i.e.
v^2 = c^2(1 - E0^2/E^2) = c^2 - c^2 E0^2/E^2, WITH an extra c^2 factor on the second term) to see
exactly how far off the notebook's own final formula is, and whether that's a genuine algebra
slip or a unit-convention artifact.
"""
import sympy as sp
import json, pathlib

hbar, omega, m0, c, v, E0, E = sp.symbols('hbar omega m0 c v E0 E', positive=True)

# starting equation (as in the notebook, with p = m0 v / sqrt(1-v^2/c^2), E=hbar*omega):
lhs = hbar**2 * omega**2
rhs = (m0**2 * v**2 * c**2) / (1 - v**2 / c**2) + m0**2 * c**4

eq = sp.Eq(lhs, rhs)
v2_solutions = sp.solve(eq, v**2)
print("v^2 solutions from direct symbolic solve:", v2_solutions)

# substitute E0 = m0*c^2, E = hbar*omega for readability
v2_sol = v2_solutions[0] if v2_solutions else None
v2_sol_named = v2_sol.subs(m0, E0 / c**2).subs(hbar * omega, E) if v2_sol is not None else None
v2_sol_simplified = sp.simplify(v2_sol_named) if v2_sol_named is not None else None

# notebook's claimed final form
notebook_claim = c**2 - E0**2 / E**2

# the independently-known-correct relativistic group velocity relation
correct_group_velocity_sq = c**2 * (1 - E0**2 / E**2)
correct_expanded = sp.expand(correct_group_velocity_sq)

match_notebook = sp.simplify(v2_sol_simplified - notebook_claim) == 0 if v2_sol_simplified is not None else None
match_correct = sp.simplify(v2_sol_simplified - correct_group_velocity_sq) == 0 if v2_sol_simplified is not None else None

result = {
    "build": "NB-093/NB-094/NB-095",
    "v2_solved_directly_from_the_notebooks_own_starting_equation": str(v2_sol_simplified),
    "notebooks_claimed_final_form": str(notebook_claim),
    "matches_notebooks_claimed_form": match_notebook,
    "independently_known_correct_relativistic_group_velocity_v2": str(correct_expanded),
    "matches_correct_group_velocity_relation": match_correct,
    "conclusion": "Solving the notebook's OWN starting equation (p = m0 v/sqrt(1-v^2/c^2) "
                  "substituted into E^2=p^2c^2+m0^2c^4, i.e. the standard, CORRECTLY-SET-UP "
                  "relativistic energy-momentum relation) gives v^2 = c^2(E^2-E0^2)/E^2 = "
                  "c^2 - c^2*E0^2/E^2 -- which is EXACTLY the correct relativistic group "
                  "velocity relation v_group=dE/dp, confirmed independently. This does NOT "
                  "match the notebook's own claimed final form v^2=c^2-E0^2/E^2, which is "
                  "missing a factor of c^2 on the second term (and is dimensionally suspect as "
                  "written, since c^2 and E0^2/E^2 don't have compatible units unless c=1 is "
                  "implicitly set, which the notebook does NOT do here -- c appears explicitly "
                  "throughout). The starting physics (NB-093's helical setup, the relativistic "
                  "momentum substitution) was correct; the algebra CARRYING OUT the solve for "
                  "v^2 introduced the missing c^2 factor. This precisely explains -- and "
                  "resolves -- the author's own 'Way way, no good' self-assessment: the "
                  "instinct that something was wrong was correct, and it is fixable (not a dead "
                  "end in the physics, just an algebra slip) -- the corrected result "
                  "v^2=c^2(1-E0^2/E^2) is exactly the standard relativistic group-velocity "
                  "formula.",
}
print(json.dumps(result, indent=2, default=str))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-093_094_095_helical_velocity.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2, default=str))
print("wrote", out)
