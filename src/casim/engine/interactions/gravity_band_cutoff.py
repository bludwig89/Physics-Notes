"""gravity_band_cutoff.py -- the paired photon/graviton band top: Omega_max = pi
exactly, and its Planck-unit value  (rubric row E12, quantum-gravity sector).
===============================================================================

**The residual this addresses.**  E12 (docs/status/completeness-2026-08-20.md)
reads "Graviton massless, 2 dof; UV completion beyond 'lattice is the cutoff'
undeveloped."  F216/F248 establish the graviton's KINEMATICS exactly (massless,
2 TT dof, luminal, non-birefringent) but never quote a number for the cutoff
itself -- "the lattice is the cutoff" stays a qualitative slogan.  A11/K9 name
a DIFFERENT residual (the rho_vac EFT-operator coefficient, ledger row G1) that
this module does not touch and does not duplicate -- see F357 Sec.1 for the
scoping argument and docs/design/session-claims.yaml (session
quiet-precise-regge) for the collision check against the concurrent K9/A11
sessions.

**THE RESULT (A-D).**  The photon/graviton "even" paired dispersion law (F69,
F26, F105, F248)

    Omega_even(K) = omega_+(K/2) + omega_-(K/2),   omega_pm(q) = arccos(u_pm(q)),
    u_pm(q) = cos(qx/root3) cos(qy/root3) cos(qz/root3)
              +- sin(qx/root3) sin(qy/root3) sin(qz/root3)

is BOUNDED ABOVE BY PI EXACTLY throughout the natural BCC Brillouin zone (the
domain |k_i| <= pi*root3/2 bcc.py's own comment declares canonical for a single
constituent branch, doubled here since the pair carries K = 2q).  The bound is
not a numerical observation: writing a = u_+(K/2), b = u_-(K/2),

    a + b = 2 cos(Kx/(2 root3)) cos(Ky/(2 root3)) cos(Kz/(2 root3)) >= 0

on the stated domain (each cosine factor is a cosine of an angle in
[-pi/2, pi/2], hence non-negative), and arccos(a) + arccos(b) <= pi whenever
a + b >= 0 -- an exact consequence of arccos(-a) = pi - arccos(a) (both sides
lie in [0, pi] and cos is injective there) plus d/db[arccos b] = -1/sqrt(1-b^2)
< 0 (monotone decreasing).  Equality is exact and holds on the WHOLE zone
boundary (any single constituent momentum component reaching the edge of ITS
OWN single-particle BZ forces u_-(K/2) = -u_+(K/2) identically, independent of
the other two components) -- verified both symbolically (checks A, D) and by a
dense numerical zone sweep (check C).

**THE CONTROL (F).**  The bound is a genuine consequence of PAIRING, not a
generic arccos saturation: the un-paired, single-branch "doubled" law
2 omega_+(K/2) -- explicitly flagged in F248/CLAUDE.md as *not* the physical
photon/graviton law -- has no such bound (its own "a+b" is 2 u_+(K/2), which is
not sign-definite on the domain) and its zone-sweep maximum is measured at
2*pi, exactly double.  Selecting this law is the module's one control
parameter, `pairing_law="chiral_double"` (default "even"), and checks C, E, F
are the reds it must produce (D9/H2).

**THE PLANCK-UNIT NUMBER (E-F).**  Omega_max = pi is an angle (radians) turned
per CA tick tau, so the physical maximum photon/graviton frequency is
omega_max = pi / tau.  Using F79's own closed-form ratio a/tau = c*sqrt(d)
(d=3) together with the registered a_over_ellP (F79/F107), tau/t_Planck =
a_over_ellP / sqrt(3) exactly, giving the closed form

    E_max / E_Planck = pi / (tau/t_Planck) = pi*sqrt(3) / a_over_ellP
                      = sqrt(pi*sqrt(3)/8)  =  0.82479...

-- an O(1) fraction of the Planck energy, computed with ZERO new free
parameters (a_over_ellP is F79's own structural output).  Check F relates this
to the model's OTHER, cruder cutoff estimate already on the record --
Lambda_model = E_Planck/a_over_ellP, F352's naive "set k ~ 1/a" compositeness
scale -- and finds the exact closed-form ratio E_max = pi*sqrt(3) * Lambda_model,
where pi*sqrt(3) is (per bcc.py's own F273 comment, "4 pi/a = 2 pi sqrt(3)")
exactly ONE reciprocal-lattice-vector magnitude 2*pi/a in that convention, not
an independent number.

**Numerics discipline (CLAUDE.md).**  All elementwise array work uses
`casim.numerics.xp` (numpy today); the exact-algebraic checks use sympy on
real symbols only (no chiral/complex spinor transforms are touched by this
module at all -- it is a real scalar dispersion law throughout, per F248's own
"real arithmetic + sympy" convention).

Run:  python3 -m casim.engine.interactions.gravity_band_cutoff
"""

from __future__ import annotations

import sympy as sp

from casim.constants import a_over_ellP as _A_OVER_ELLP
from casim.numerics import xp

# ---- constants (D7: imported, never re-typed as literals) ------------------
A_OVER_ELLP = _A_OVER_ELLP                     # F79/F107 structural SI ruler
SQRT3 = float(xp.sqrt(3.0))
TAU_OVER_TP = A_OVER_ELLP / SQRT3              # F79 Sec.5: a/tau = c*sqrt(3)
LAMBDA_MODEL_OVER_EPLANCK = 1.0 / A_OVER_ELLP  # F352's own naive k~1/a cutoff

CHECKS: dict[str, dict] = {}


def _record(name: str, passed: bool | None, detail: dict) -> dict:
    out = {"pass": (None if passed is None else bool(passed)), "detail": detail}
    CHECKS[name] = out
    return out


# ===========================================================================
# A -- the exact identity + monotonicity theorem (sympy, law-independent)
# ===========================================================================
def check_A_identity_theorem() -> dict:
    """arccos(-a) = pi - arccos(a) exactly (both branches land in [0,pi] and
    cos is injective there), and d/db[arccos a + arccos b] = -1/sqrt(1-b^2) < 0
    strictly on (-1,1) -- so arccos(a)+arccos(b) <= pi  <=>  a+b >= 0, equality
    iff a+b = 0."""
    a, b = sp.symbols("a b", real=True)
    identity_residual = sp.simplify(sp.cos(sp.pi - sp.acos(a)) - (-a))
    dg_db = sp.diff(sp.acos(a) + sp.acos(b), b)
    dg_db_closed = sp.simplify(dg_db - (-1 / sp.sqrt(1 - b**2)))
    # numeric cross-check of the identity itself (independent of the symbolic
    # simplification path), matching the project's exact+numeric pairing habit
    rng = xp.random.default_rng(0)
    avals = rng.uniform(-1.0, 1.0, 200_000)
    max_resid = float(xp.max(xp.abs(xp.arccos(avals) + xp.arccos(-avals) - xp.pi)))
    return _record(
        "A_identity_theorem",
        identity_residual == 0 and dg_db_closed == 0 and max_resid < 1e-12,
        {
            "cos(pi-acos(a))+a": str(identity_residual),
            "d/db[acos a+acos b] - (-1/sqrt(1-b^2))": str(dg_db_closed),
            "numeric_identity_max_residual": max_resid,
        },
    )


# ===========================================================================
# B -- domain non-negativity for the physical "even" pairing law
# ===========================================================================
def check_B_domain_nonneg(n=4001) -> dict:
    """On the declared single-constituent-branch BZ, theta_i = q_i/root3 in
    [-pi/2, pi/2] (bcc.py's own comment), so c_i = cos(theta_i) >= 0. This is
    the fact check A's a+b>=0 hypothesis rests on."""
    theta = xp.linspace(-xp.pi / 2.0, xp.pi / 2.0, n)
    c = xp.cos(theta)
    min_c = float(xp.min(c))
    endpoint_resid = float(max(abs(xp.cos(-xp.pi / 2.0)), abs(xp.cos(xp.pi / 2.0))))
    return _record(
        "B_domain_nonneg",
        min_c >= -1e-14 and endpoint_resid < 1e-12,
        {"min_cos_over_domain": min_c, "cos(+-pi/2)_residual": endpoint_resid},
    )


# ===========================================================================
#  the dispersion laws (real arithmetic; K is the PAIR's external momentum)
# ===========================================================================
def _u_pm(qx, qy, qz, sign):
    r3 = xp.sqrt(3.0)
    cx, cy, cz = xp.cos(qx / r3), xp.cos(qy / r3), xp.cos(qz / r3)
    sx, sy, sz = xp.sin(qx / r3), xp.sin(qy / r3), xp.sin(qz / r3)
    return cx * cy * cz + sign * sx * sy * sz


def omega_even(Kx, Ky, Kz):
    """The physical photon/graviton paired law (F69/F26/F105/F248):
    omega_+(K/2) + omega_-(K/2)."""
    qx, qy, qz = 0.5 * Kx, 0.5 * Ky, 0.5 * Kz
    up = xp.clip(_u_pm(qx, qy, qz, +1.0), -1.0, 1.0)
    um = xp.clip(_u_pm(qx, qy, qz, -1.0), -1.0, 1.0)
    return xp.arccos(up) + xp.arccos(um)


def omega_chiral_double(Kx, Ky, Kz):
    """CONTROL ONLY -- the un-paired single-branch doubled law 2*omega_+(K/2),
    explicitly flagged in F248/CLAUDE.md as NOT the physical photon/graviton
    dispersion. Included only to show the pi-bound is pairing-specific."""
    qx, qy, qz = 0.5 * Kx, 0.5 * Ky, 0.5 * Kz
    up = xp.clip(_u_pm(qx, qy, qz, +1.0), -1.0, 1.0)
    return 2.0 * xp.arccos(up)


_LAWS = {"even": omega_even, "chiral_double": omega_chiral_double}


# ===========================================================================
# C -- dense zone-sweep numeric confirmation of the band top
# ===========================================================================
def check_C_grid_bandtop(pairing_law: str = "even", n=161) -> dict:
    """Dense sweep of the pair BZ |K_i| <= pi*root3 (K=2q, q the constituent
    momentum on bcc.py's own |q_i|<=pi*root3/2 domain). Expect max=pi for the
    physical even law; the chiral_double control expects max=2*pi."""
    law = _LAWS[pairing_law]
    bound = xp.pi * xp.sqrt(3.0)
    grid = xp.linspace(-bound, bound, n)
    KX, KY, KZ = xp.meshgrid(grid, grid, grid, indexing="ij")
    vals = law(KX, KY, KZ)
    grid_max = float(xp.max(vals))
    grid_min = float(xp.min(vals))
    # PHYSICAL prediction is fixed at pi regardless of which law is actually
    # evaluated -- this is what makes pairing_law="chiral_double" a genuine
    # control (its own grid_max is 2*pi, which fails this fixed target) rather
    # than a second branch that trivially predicts itself.
    physical_expected = float(xp.pi)
    return _record(
        "C_grid_bandtop",
        abs(grid_max - physical_expected) < 5e-4,
        {
            "pairing_law": pairing_law,
            "grid_max": grid_max,
            "grid_max_over_pi": grid_max / float(xp.pi),
            "grid_min": grid_min,
            "physical_expected_max": physical_expected,
            "n_per_axis": n,
        },
    )


# ===========================================================================
# D -- exact boundary-saturation locus (sympy; even law only)
# ===========================================================================
def check_D_boundary_saturation() -> dict:
    """At theta_x = pi/2 (Kx = pi*root3, the constituent BZ edge), u_-(K/2) =
    -u_+(K/2) IDENTICALLY for every theta_y, theta_z -- so Omega_even = pi
    exactly on the WHOLE boundary face, not just at isolated corners."""
    ty, tz = sp.symbols("theta_y theta_z", real=True)
    cx, sx = sp.cos(sp.pi / 2), sp.sin(sp.pi / 2)  # theta_x = pi/2 exactly
    cy, sy = sp.cos(ty), sp.sin(ty)
    cz, sz = sp.cos(tz), sp.sin(tz)
    u_plus = cx * cy * cz + sx * sy * sz
    u_minus = cx * cy * cz - sx * sy * sz
    residual = sp.simplify(u_plus + u_minus)
    return _record(
        "D_boundary_saturation",
        residual == 0,
        {"u_plus_plus_u_minus_at_theta_x=pi/2": str(residual)},
    )


# ===========================================================================
# E -- the Planck-unit number (exact-algebraic given the registered ruler)
# ===========================================================================
def check_E_planck_ratio(pairing_law: str = "even") -> dict:
    """E_max/E_Planck = Omega_max * (t_Planck/tau) = Omega_max / (a_over_ellP/root3).
    Closed form for the physical even law: sqrt(pi*sqrt(3)/8) = 0.82479...
    Cross-checked two ways: (i) the symbolic closed form vs a float evaluation
    through the registered a_over_ellP, (ii) against the check-C grid max
    actually found (so the control law is graded on the SAME formula, not a
    hardcoded even-law number, and correctly goes red)."""
    grid_max = CHECKS["C_grid_bandtop"]["detail"]["grid_max"]
    ratio_numeric = grid_max / TAU_OVER_TP

    pi_s, sqrt3_s, ap_s = sp.pi, sp.sqrt(3), sp.nsimplify(A_OVER_ELLP, [sp.sqrt(sp.pi), sp.Integer(3) ** sp.Rational(1, 4)])
    closed_form_even = sp.sqrt(pi_s * sqrt3_s / 8)
    closed_form_even_float = float(closed_form_even)

    # PHYSICAL prediction fixed at the even-law closed form (see check C).
    resid_vs_physical = abs(ratio_numeric - closed_form_even_float)
    resid_symbolic_vs_registry = abs(closed_form_even_float - float(sp.pi / (ap_s / sqrt3_s)))
    return _record(
        "E_planck_ratio",
        resid_vs_physical < 5e-4 and resid_symbolic_vs_registry < 1e-9,
        {
            "pairing_law": pairing_law,
            "tau_over_tPlanck": TAU_OVER_TP,
            "E_max_over_E_Planck_numeric": ratio_numeric,
            "E_max_over_E_Planck_closed_form_even_law": closed_form_even_float,
            "closed_form_expr": "sqrt(pi*sqrt(3)/8)",
            "physical_expected": closed_form_even_float,
        },
    )


# ===========================================================================
# F -- relation to F352's cruder Lambda_model cutoff (exact-algebraic)
# ===========================================================================
def check_F_lambda_model_relation(pairing_law: str = "even") -> dict:
    """E_max = pi*sqrt(3) * Lambda_model exactly for the even law (pi*sqrt(3)
    is, per bcc.py's F273 comment "4 pi/a = 2 pi sqrt(3)", exactly one
    reciprocal-lattice-vector magnitude 2*pi/a in that convention -- not an
    independent number)."""
    e_over_ep = CHECKS["E_planck_ratio"]["detail"]["E_max_over_E_Planck_numeric"]
    ratio_to_lambda_model = e_over_ep / LAMBDA_MODEL_OVER_EPLANCK
    # PHYSICAL prediction fixed at pi*sqrt(3) (see checks C, E).
    physical_expected = float(sp.pi * sp.sqrt(3))
    return _record(
        "F_lambda_model_relation",
        abs(ratio_to_lambda_model - physical_expected) < 5e-4,
        {
            "pairing_law": pairing_law,
            "Lambda_model_over_E_Planck": LAMBDA_MODEL_OVER_EPLANCK,
            "E_max_over_Lambda_model": ratio_to_lambda_model,
            "physical_expected": physical_expected,
            "physical_expected_closed_form": "pi*sqrt(3)",
        },
    )


# ===========================================================================
def run_all(pairing_law: str = "even") -> dict:
    """Gate entry.

    Declared negative control (D9/H2), perturbing the COMPUTED dispersion law:

      ``pairing_law="chiral_double"``  swap the physical paired "even" law
                                        Omega_even = omega_+(K/2)+omega_-(K/2)
                                        for the un-paired doubled law
                                        2*omega_+(K/2) (F248/CLAUDE.md: NOT the
                                        photon/graviton law). Checks C, E, F
                                        test the COMPUTED quantity against a
                                        FIXED physical target (pi; the even-law
                                        closed form 0.82473; pi*sqrt(3)) rather
                                        than adapting to whichever law was
                                        selected, so all three must go red:
                                        the zone-sweep maximum measures 2*pi,
                                        not pi, and the two downstream
                                        Planck-unit/Lambda_model ratios double
                                        with it. A, B do not read the
                                        dispersion law at all and stay green;
                                        D is an even-law-only statement and is
                                        reported not-applicable (pass=None,
                                        uncounted) rather than forced red.
    """
    global CHECKS
    CHECKS = {}
    checks = {
        "A_identity_theorem": check_A_identity_theorem(),
        "B_domain_nonneg": check_B_domain_nonneg(),
        "C_grid_bandtop": check_C_grid_bandtop(pairing_law),
        "D_boundary_saturation": (
            check_D_boundary_saturation() if pairing_law == "even"
            else _record("D_boundary_saturation", None,
                          {"skipped": "boundary-saturation locus is an even-law statement"})
        ),
        "E_planck_ratio": check_E_planck_ratio(pairing_law),
        "F_lambda_model_relation": check_F_lambda_model_relation(pairing_law),
    }
    counted = {k: v for k, v in checks.items() if v.get("pass") is not None}
    n_pass = sum(1 for v in counted.values() if v["pass"])
    return {
        "finding": "F357",
        "title": ("The paired photon/graviton band top: Omega_max = pi exactly, "
                   "and E_max = 0.8248 E_Planck -- a computed answer to E12's "
                   "'UV completion beyond lattice-is-cutoff'"),
        "pairing_law": pairing_law,
        "checks": checks,
        "n_pass": n_pass,
        "n_total": len(counted),
        "all_pass": n_pass == len(counted),
    }


if __name__ == "__main__":            # guard: never write an artifact at import
    import json
    from casim.engine.particles._results_path import results_path

    res = run_all()
    path = results_path("F357_graviton_band_cutoff.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(f"{res['n_pass']}/{res['n_total']} PASS -> {path}")
