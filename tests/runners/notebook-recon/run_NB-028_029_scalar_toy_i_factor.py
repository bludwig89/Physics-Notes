"""
NB-028/NB-029 (pp.21-22): scalar-field "toy matter" Lagrangian introduced to test the
Theta^{mu nu} formalism: L_M = i (d_mu phi)(d^mu phi) - mu^2 phi^2 (notebook's own transcription,
lines 487/491), carried through into H_M = i d_0 phi d^0 phi + i grad(phi).grad(phi) + mu^2 phi^2
(lines 501/505) and the final boxed total Hamiltonian (NB-030, p.22).

Checks whether the literal "i" prefactor on the kinetic term is consistent with a real scalar
field having a sensible (real) equation of motion, by deriving the Euler-Lagrange equation for
BOTH the as-transcribed L_M and the standard real-KG L_M = 1/2(d phi)^2 - 1/2 mu^2 phi^2, and
comparing.
"""
import sympy as sp
import json, pathlib

t, x, y, z, mu = sp.symbols('t x y z mu', real=True)
phi = sp.Function('phi')(t, x, y, z)
phit, phix, phiy, phiz = [sp.diff(phi, v) for v in (t, x, y, z)]


def euler_lagrange(L):
    dL_dphit = sp.diff(L, phit)
    dL_dphix = sp.diff(L, phix)
    dL_dphiy = sp.diff(L, phiy)
    dL_dphiz = sp.diff(L, phiz)
    dL_dphi = sp.diff(L, phi)
    return sp.expand(sp.diff(dL_dphit, t) + sp.diff(dL_dphix, x) + sp.diff(dL_dphiy, y)
                      + sp.diff(dL_dphiz, z) - dL_dphi)


# as literally transcribed on p.21 (line 487/491)
L_as_transcribed = sp.I * (phit**2 - phix**2 - phiy**2 - phiz**2) - mu**2 * phi**2
EL_as_transcribed = euler_lagrange(L_as_transcribed)

# standard real-scalar KG Lagrangian (the physically sensible normalization)
L_standard = sp.Rational(1, 2) * (phit**2 - phix**2 - phiy**2 - phiz**2) - sp.Rational(1, 2) * mu**2 * phi**2
EL_standard = euler_lagrange(L_standard)

box_phi = sp.diff(phi, t, 2) - sp.diff(phi, x, 2) - sp.diff(phi, y, 2) - sp.diff(phi, z, 2)

# does the as-transcribed EOM reduce to a REAL relation between box(phi) and phi, as required
# for a real scalar field's equation of motion?
# EL_as_transcribed = 2*mu^2*phi + 2i*box(phi) = 0  =>  box(phi) = i*mu^2*phi  (has an explicit i)
solved_box_coefficient = sp.simplify(sp.solve(sp.Eq(EL_as_transcribed, 0), box_phi)[0] / phi) if False else None
# (direct inspection instead, since box_phi isn't a free symbol to solve for symbolically here)
has_imaginary_unit_in_EOM = sp.I in EL_as_transcribed.atoms(sp.I) or 'I' in str(EL_as_transcribed)

result = {
    "build": "NB-028/NB-029",
    "EL_as_transcribed_with_stray_i": str(EL_as_transcribed),
    "EL_standard_real_KG": str(EL_standard),
    "as_transcribed_EOM_contains_imaginary_unit": bool(has_imaginary_unit_in_EOM),
    "conclusion": "The literal p.21 Lagrangian L_M = i(d phi)^2 - mu^2 phi^2 produces the "
                  "Euler-Lagrange equation 2 mu^2 phi + 2i*Box(phi) = 0, i.e. Box(phi) = i mu^2 "
                  "phi -- an equation with an explicit factor of i relating two otherwise-real "
                  "quantities, which is not a sensible equation of motion for a real scalar "
                  "field. This is a genuine error (or a slip for the standard 1/2 normalization, "
                  "not merely a stylistic choice): dropping the 'i' (replacing with 1 or 1/2) "
                  "recovers the standard real KG equation of motion.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-028_029_scalar_toy_i_factor.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
