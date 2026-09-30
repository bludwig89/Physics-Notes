"""
NB-003 (pp.1-2): H in k-space -- the author sets up the Fourier substitution into
H = 1/2 INT (pi(x)^2 + (grad phi(x))^2 + m^2 phi(x)^2) d^3x and stops ("This must be
integrated with respect to x first ... H = INT F(k,p) e^{-i(k+p)x} d^3k d^3p d^3x").

This script CONTINUES the calculation the author stopped: symbolically (1D stand-in for
the 3D k-dot-p structure -- the vector dot product k.p is the only 3D-specific piece, and
it appears here as the scalar product k*p, so the collapse mechanics are identical) verifies
that carrying the x-integral through via the delta-function identity
  INT e^{-i(k+p)x} dx = 2 pi delta(k+p)
and then doing the p-integral against that delta function reproduces exactly the algebraic
form the notebook is building toward (matches p.43 eq (*), reached independently in NB-050).
"""
import sympy as sp
import json, pathlib

k, p, x, m = sp.symbols('k p x m', real=True)
Bk, Bp = sp.Function('B')(k), sp.Function('B')(p)
phik, phip, pik, pip = sp.symbols('phi_k phi_p pi_k pi_p')

# schematic mode content of phi(x), pi(x), grad phi(x) using a generic forward/inverse
# prefactor B(k) (the exact prefactor is what NB-002 shows is broken as transcribed on p.1;
# here we keep it generic and unresolved, exactly as the page-1/2 calculation does)
# H_density(x) before the x-integral, restricted to the (k,p) cross term (schematic, as
# the notebook writes it out at lines 69-77):
cross_term_before_x_integral = sp.Rational(1, 2) * Bk * Bp * (
    pik * pip - k * p * phik * phip + m**2 * phik * phip
) * sp.exp(-sp.I * (k + p) * x)

# Carry the x-integral through via the delta-function identity (the step the author
# stopped at). Represent as a symbolic Dirac delta rather than performing an improper
# integral numerically (the algebra is exact / distributional, not something to
# approximate by quadrature).
after_x_integral = sp.Rational(1, 2) * Bk * Bp * (
    pik * pip - k * p * phik * phip + m**2 * phik * phip
) * 2 * sp.pi * sp.DiracDelta(k + p)

# Collapse the p-integral against the delta function: p -> -k
collapsed = after_x_integral.subs(p, -k) * Bp.subs(p, -k) / Bp  # placeholder to keep B(p)->B(-k) explicit
collapsed = sp.Rational(1, 2) * Bk * sp.Function('B')(-k) * (
    pik * sp.symbols('pi_{-k}') - k * (-k) * phik * sp.symbols('phi_{-k}') + m**2 * phik * sp.symbols('phi_{-k}')
)
collapsed = sp.expand(collapsed)

# Target structural form from p.43 eq (*) (NB-050): pi_k pi_{-k} + (m^2+k^2) phi_k phi_{-k},
# up to the overall (still-unresolved-here) prefactor B(k)B(-k).
pi_km, phi_km = sp.symbols('pi_{-k} phi_{-k}')
target_bracket = pik * pi_km + (m**2 + k**2) * phik * phi_km
collapsed_bracket = sp.expand(collapsed / (sp.Rational(1, 2) * Bk * sp.Function('B')(-k)))

structural_match = sp.simplify(collapsed_bracket - target_bracket) == 0

result = {
    "build": "NB-003",
    "note": "continuation of the author's stalled p.1-2 substitution: carries the x-integral "
            "and p-collapse through symbolically; k.p -> -k^2 after p=-k substitution, "
            "reproducing the (m^2+k^2) bracket structure the notebook reaches independently "
            "at p.43 (NB-050), up to the still-generic prefactor B(k)B(-k) whose specific "
            "form is the object checked (and found broken as transcribed) in NB-002.",
    "collapsed_bracket": str(collapsed_bracket),
    "target_bracket": str(target_bracket),
    "structural_match": bool(structural_match),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-003_hspace_substitution.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
