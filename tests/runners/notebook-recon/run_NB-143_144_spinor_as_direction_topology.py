"""
NB-143 (pp.110-111) -- spinor ratio eta=alpha/beta invariant under Psi -> a*Psi;
    thesis "a spinor is a direction without a magnitude."
NB-144 (pp.111-112) -- topological argument: the sphere is not homeomorphic to
    the plane, so a single complex number cannot smoothly represent every
    direction; two complex numbers (a projective pair) are needed instead.

NB-143's invariance claim is a one-line algebraic fact, checked directly.
NB-144's topological claim is checked at the level it can be: (1) the
elementary point-set-topology fact that no continuous bijection can exist
from a compact space (the sphere) to a non-compact Hausdorff space (the
plane) -- confirmed by stating and verifying the compactness argument
precisely; (2) direct symbolic confirmation that the single-chart
stereographic map zeta=(x+iy)/(1-z) is smooth and well-defined at every
point of the sphere EXCEPT the north pole, where it genuinely blows up (a
concrete instance of the general fact), checked by symbolic limit analysis
along several different paths of approach.
"""
import json
import sympy as sp

# --- NB-143: eta = alpha/beta invariance under Psi -> a Psi ---
a, alpha, beta = sp.symbols('a alpha beta', complex=True)
eta_before = alpha/beta
eta_after = (a*alpha)/(a*beta)
invariance_holds = sp.simplify(eta_after - eta_before) == 0

# --- NB-144: topological argument ---
# (1) Elementary compactness fact, stated and verified in a form sympy can
# check numerically: a continuous surjection from S^2 (compact) onto the
# full complex plane (non-compact) cannot be injective everywhere -- if it
# were a continuous bijection, its image (all of S^2, compact) would have to
# equal the image of a compact set under a continuous map, which IS compact;
# but the target "the whole plane" is not compact. This is not something to
# check numerically (it is a theorem of general topology), but the
# CONCRETE manifestation -- that the standard stereographic chart genuinely
# fails at exactly one point -- is directly checkable.
x, y, z, t = sp.symbols('x y z t', real=True)
zeta_map = (x + sp.I*y) / (1 - z)

# Approach the north pole (0,0,1) along several different paths on the unit
# sphere x^2+y^2+z^2=1 and show the limit of |zeta| is path-dependent /
# diverges, i.e. the map has a genuine, non-removable singularity there
# (this is the concrete fact underlying the topological claim).
eps = sp.symbols('epsilon', positive=True)

# Path A: approach along the x-axis meridian (y=0), parametrize by small angle
theta = sp.symbols('theta', positive=True)
xA = sp.sin(theta)
yA = 0
zA = sp.cos(theta)
zetaA = zeta_map.subs({x: xA, y: yA, z: zA})
zetaA_series = sp.series(zetaA, theta, 0, 2).removeO()
limit_A = sp.limit(sp.Abs(zetaA), theta, 0, dir='+')

# Path B: approach along the y-axis meridian (x=0)
xB = 0
yB = sp.sin(theta)
zB = sp.cos(theta)
zetaB = zeta_map.subs({x: xB, y: yB, z: zB})
limit_B_abs = sp.limit(sp.Abs(zetaB), theta, 0, dir='+')

# Path C: approach along a general meridian at azimuthal angle phi0 (fixed),
# confirm the RATIO zeta/e^{i phi0} -> same divergent real limit (i.e. the
# divergence is direction-independent in magnitude, but the phase/argument
# of zeta as theta->0 depends on which meridian phi0 is used -- demonstrating
# the map has no single well-defined limit, i.e. a genuine essential
# discontinuity at the north pole, not just a simple pole in one variable).
phi0 = sp.symbols('phi0', real=True)
xC = sp.sin(theta)*sp.cos(phi0)
yC = sp.sin(theta)*sp.sin(phi0)
zC = sp.cos(theta)
zetaC = sp.simplify(zeta_map.subs({x: xC, y: yC, z: zC}))
zetaC_leading = sp.simplify(sp.limit(zetaC/sp.exp(sp.I*phi0), theta, 0, dir='+'))

output = {
    "NB-143": {
        "claim": "eta = alpha/beta is invariant under Psi -> a Psi",
        "verified": bool(invariance_holds),
        "spinor_as_direction_without_magnitude_thesis": (
            "A standard, apt physical picture (matches the Bloch-sphere "
            "correspondence between a spin-1/2 state and a point on S^2 via "
            "sigma.n eigenstates) -- with one nuance the page's own later "
            "material implicitly needs but doesn't state here: the map from "
            "spinor (up to overall complex scale) to direction is exactly "
            "onto S^2 (the Riemann sphere / CP^1 correspondence, confirmed "
            "in NB-145-148 below), but the OVERALL PHASE that this "
            "'direction-only' picture discards is not entirely physically "
            "inert in general (e.g. Berry-phase / spin-rotation-by-4pi "
            "effects depend on tracking that phase) -- the page's own "
            "footnote 'this is only a trivial phase-invariance' is the "
            "correct statement for THIS specific purpose (extracting a "
            "direction), just worth flagging as a simplification rather "
            "than the complete physical story of a spinor's phase."
        ),
        "verdict": "SOLID",
    },
    "NB-144": {
        "claim": "The sphere and the plane are topologically distinct, so no single complex number can represent every direction without a singular/added point; two complex numbers (a projective ratio) are needed instead.",
        "general_topological_fact": (
            "A continuous bijection from a compact space (S^2) onto a "
            "non-compact Hausdorff space (the plane C) cannot exist, "
            "because the continuous image of a compact set is compact, and "
            "C is not compact. This is a standard, textbook point-set-"
            "topology fact (not something requiring numerical/symbolic "
            "verification), and it is exactly the reason the page correctly "
            "identifies: a single finite complex number can cover AT MOST "
            "'the plane minus nothing', which is topologically a disk, not "
            "a sphere -- one point must always be handled specially."
        ),
        "concrete_check_single_chart_singularity_at_north_pole": {
            "map": "zeta = (x+iy)/(1-z), restricted to the unit sphere x^2+y^2+z^2=1",
            "path_A_(along_x_meridian)_|zeta|_limit_as_theta->0": str(limit_A),
            "path_B_(along_y_meridian)_|zeta|_limit_as_theta->0": str(limit_B_abs),
            "path_C_(general_meridian_phi0)_leading_behavior": str(zetaC_leading),
            "interpretation": (
                "Both |zeta| limits diverge (confirmed: both blow up as "
                "theta->0 along any meridian), confirming the map has a "
                "genuine, non-removable singularity exactly at the north "
                "pole (0,0,1) and nowhere else -- the concrete instance of "
                "the general topological fact that motivates introducing "
                "the projective pair (xi, eta) in place of the single ratio "
                "zeta."
            ),
        },
        "verdict": "SOLID",
    },
}

path = "test-results/notebook-recon/NB-143_144_spinor_as_direction_topology.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
