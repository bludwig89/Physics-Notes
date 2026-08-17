"""
derive_boost_covariance.py — finite-$a$ boost covariance on the canonical BCC lattice
=====================================================================================

Rubric row **A2** (Lorentz invariance) of `docs/status/completeness-2026-08-04.md`
carried the residual "**finite-a boost covariance unaddressed**", and the F24
remediation (2026-08-04, ledger item 10) DEFERRED the load-bearing question into
`docs/roadmaps/next-steps.md`:

    does the lattice EVOLUTION commute with a Lorentz boost at finite a, at what
    order in ka does it fail, and does the coefficient match F15/F22's beta_LV?

This module answers it WITHOUT choosing a boost implementation, which is the trap
the question contains: any concrete "lattice boost" is a convention, and a defect
measured against a convention is a property of the convention. Instead the test is
the **Poincare algebra** itself.

THE OBSERVABLE
--------------
For a free lattice channel with H = Omega(k), P_i = k_i and x_i = i d/dk_i, the
boost generator is K_i = (1/2c^2){x_i, Omega}. Then, for ARBITRARY Omega:

    [K_i, P_j] = i delta_ij Omega / c^2          <-- EXACT, no defect, any Omega
    [K_i, H]   = i P_i + i D_i                   <-- D_i is the defect
    [K_i, K_j] = -(i/c^2) eps_ijk J_k
                 + (i/c^2)( D_i x_j - D_j x_i )  <-- SAME D_i, nothing new

        D_i(k) = (1/2c^2) d_i( Omega^2 ) - k_i = d_i Phi,
        Phi(k) = ( Omega(k)^2 - c^2|k|^2 ) / (2c^2).

Three consequences make D_i the right object rather than one choice among many:

1. **D_i is a gradient.** The whole failure of the Poincare algebra is carried by
   ONE scalar potential Phi -- the off-shell invariant mass. Boost covariance at
   finite a is exactly the statement that the invariant mass does not run with
   momentum.  D_i == 0 for all i  <=>  Omega^2 - c^2|k|^2 = const.
2. **D_i is the complete obstruction.** [K,P] never fails; the [K,K] defect is
   algebraically the same D_i. There is no second, independent seam.
3. **D_i cannot be gauged away in momentum space.** K_i -> K_i + f(k) for any
   real f leaves D_i unchanged (verified symbolically), so the defect is not an
   artifact of the minimal choice of K.

D_i also has a direct operational meaning: for a boost of VELOCITY v along vhat,
the off-shell residual of the linear SR boost is

    Omega' - Omega(k') = v ( D . vhat ) + O(v^2),

so D IS the coefficient F22 measured in 1D. In the 1D reduction it collapses to
D/k = 1/rho - 1 = 2 beta_LV/(1 - 2 beta_LV).

WHAT COMES OUT (all verified below)
-----------------------------------
A. **An exact massive mass shell, at finite a, on BCC.** With n = sqrt(1-m^2),

       sin^2 omega(k,m) - (1-m^2) sin^2 omega_0(k) = m^2      IDENTICALLY,

   omega_0 = arccos(u_s) the massless branch of the SAME chirality. So
   E = sin omega, c|P| = n sin omega_0(k) puts the lattice on the exact
   Minkowski shell E^2 - c^2|P|^2 = m^2 for every m and every k in the BZ. F22
   recorded this as missing ("the BCC form ... has no obvious analogue of
   sin^2 omega - n^2 sin^2 u = m^2, and no code path exists"); the analogue is
   the massless branch. Mass enters EXACTLY relativistically: the whole lattice
   deformation sits in the mass-INDEPENDENT map k -> sin omega_0(k).

B. **Exact all-order covariance on the cubic axes.** Along <100>, u_s reduces to
   cos(k/sqrt3) on both branches, so omega = c_lat|k| EXACTLY, Phi is constant
   and D vanishes to all orders in ka -- not to leading order, exactly.

C. **The photon defect, closed form.** For the F26 even law,

       D_x = -(|k|^3/36) khat_x (khat_y^2 + khat_z^2)(1 + 3 khat_y^2 khat_z^2),
       D . khat = -(1/18)( p + 3q ) |k|^3,

   with F246's cubic invariants p, q. The sqrt3's cancel: the coefficient is
   RATIONAL. Radial extrema: -2/81 |k|^3 along <111>, -1/72 |k|^3 along <110>,
   0 along <100>.

D. **The chiral-branch defect, closed form, one order WORSE.** For a single Weyl
   branch s = +/-1,

       D_i = -s c_lat ( k_y k_z, k_z k_x, k_x k_y ) + O(|k|^3),

   i.e. O(|k|^2). Its origin is the k^2 dispersion term F246 showed the even
   symmetrisation removes, whose closed form is derived here for the first time:
   b_2(khat) = -(1/3) khat_x khat_y khat_z for omega_+(k), equivalently
   c_2(khat) = -(1/6) khat_x khat_y khat_z for Omega_single = 2 omega_+(k/2)
   (F246 left this as two numbers, -sqrt3/54 on <111> and -sqrt6/108 on <211>).

E. **Why the photon is better: the defect is chirality-odd.** b_2 is a degree-3
   odd harmonic, so D^(+) = -D^(-) at leading order and the pair/even channel
   cancels it. The F26 even law buys exactly ONE order of boost covariance, and
   the mechanism is the same helicity symmetrisation that kills birefringence.

F. **A no-go, with a coefficient: no UNIVERSAL momentum map.** A nonlinear (DSR)
   realisation exists per channel -- P = (E/c) khat linearises any single massless
   channel trivially, and leg A does it exactly for the massive branch -- but a
   spacetime symmetry must use ONE map. Universality needs
   Omega_even(k) = omega_+(k), and

       Omega_even(k) - omega_+(k) = +(1/3) khat_x khat_y khat_z |k|^2 + O(|k|^3),

   nonzero except on the three coordinate planes. So the DSR loophole is closed
   for the multi-channel model, and the obstruction is the SAME chiral k^2 term.

THE DICHOTOMY, STATED PLAINLY
-----------------------------
Either P generates lattice translations (P = k) and the Poincare algebra fails at
O(|k|^2) on chiral branches / O(|k|^3) on the even law -- or the algebra closes on
the deformed P of leg A, which is NOT the generator of lattice translations, is not
conjugate to the lattice site, and is not the same map for the photon and the
fermion (leg F). Finite-a boost covariance is broken; what this module supplies is
the exact order, the exact coefficient, and the exact reason.

NOT CLOSED HERE: an experimental bound on the chiral-branch O(|k|^2) coefficient
(F28's GRB bound constrains the photon |k|^3 term, not this one); the |k|^5 term;
the same programme for the W/Z/gluon propagators of F91; and a lattice-native
rotation generator -- the [K,K] bracket returns the CONTINUOUS J, of which only
the 48-element O_h subgroup is an exact lattice symmetry.

DOMAIN. x_i = i d/dk_i is the position operator on the BZ torus, so every
statement here is for smooth wavepackets in the interior of the BZ, away from
k = 0 (where |k| is non-analytic) and away from the zone edge (where Omega stops
being monotone along rays and the deformed map of leg A stops being invertible).
"""
from __future__ import annotations

import mpmath as mp

from casim.constants import c_lat

mp.mp.dps = 45

# c_lat is EXACT (F26) but the registry exports a float, and mp.mpf() of a float
# inherits the double-precision error — which then propagates into every radical
# identity checked below and breaks them at 1e-16 rather than 1e-45. So the
# closed form is evaluated at working precision and CROSS-CHECKED against the
# registry value; the import stays load-bearing instead of decorative.
_R3 = mp.sqrt(3)
_C = 1 / _R3                # lattice light speed 1/sqrt3 (F26)
_C2 = _C ** 2               # c_lat^2 = 1/3
assert abs(_C - mp.mpf(c_lat)) < mp.mpf('1e-15'), (_C, c_lat)

__all__ = [
    "omega_branch", "omega_even", "omega_single", "mass_function",
    "defect", "defect_closed_even", "defect_closed_branch", "b2_closed",
    "deformed_EP", "deformed_to_k", "lorentz",
    "check_boost_covariance", "verify",
]


# ----------------------------------------------------------------------------
# exact BCC dispersions (casim.engine.lattice.bcc._bcc_uvec / F26; args k_i/sqrt3)
# ----------------------------------------------------------------------------
def _u(kv, s, m=0):
    n = mp.sqrt(1 - mp.mpf(m) ** 2)
    a = [mp.mpf(kv[i]) * _C for i in range(3)]
    c = [mp.cos(x) for x in a]
    sn = [mp.sin(x) for x in a]
    return n * (c[0] * c[1] * c[2] + s * sn[0] * sn[1] * sn[2])


def omega_branch(kv, s=1, m=0):
    """Exact BCC branch dispersion omega^s(k) = arccos(n u_s(k)), n = sqrt(1-m^2)."""
    return mp.acos(_u(kv, s, m))


def omega_even(kv):
    """F26 even (paired-spinor photon) law Omega = omega_+(k/2) + omega_-(k/2)."""
    h = [mp.mpf(x) / 2 for x in kv]
    return omega_branch(h, 1) + omega_branch(h, -1)


def omega_single(kv):
    """Single-chirality baseline 2 omega_+(k/2) (F246's comparison law)."""
    return 2 * omega_branch([mp.mpf(x) / 2 for x in kv], 1)


def _unit(d):
    n = mp.sqrt(sum(mp.mpf(x) ** 2 for x in d))
    return [mp.mpf(x) / n for x in d]


def _norm(v):
    return mp.sqrt(sum(mp.mpf(x) ** 2 for x in v))


# ----------------------------------------------------------------------------
# the observable
# ----------------------------------------------------------------------------
def mass_function(Om, kv):
    """Off-shell invariant mass squared Omega^2 - c^2|k|^2 (= 2 c^2 Phi)."""
    return Om(kv) ** 2 - _C2 * sum(mp.mpf(x) ** 2 for x in kv)


def defect(Om, kv, i=None):
    """D_i = (1/2c^2) d_i(Omega^2) - k_i.  Returns the component, or the vector."""
    if i is None:
        return [defect(Om, kv, j) for j in range(3)]
    f = lambda t: Om([mp.mpf(kv[j]) + (t if j == i else 0) for j in range(3)]) ** 2
    return mp.diff(f, mp.mpf(0)) / (2 * _C2) - mp.mpf(kv[i])


def defect_closed_even(kv):
    """Leading closed form, F26 even law: -(|k|^3/36) kx(ky^2+kz^2)(1+3 ky^2 kz^2)."""
    k = _norm(kv)
    u = [mp.mpf(x) / k for x in kv]
    out = []
    for i in range(3):
        j, l = [(1, 2), (2, 0), (0, 1)][i]
        out.append(-(k ** 3 / 36) * u[i] * (u[j] ** 2 + u[l] ** 2)
                   * (1 + 3 * u[j] ** 2 * u[l] ** 2))
    return out


def defect_closed_branch(kv, s=1):
    """Leading closed form, single chiral branch: -s c_lat (ky kz, kz kx, kx ky)."""
    k = [mp.mpf(x) for x in kv]
    return [-s * _C * k[1] * k[2], -s * _C * k[2] * k[0], -s * _C * k[0] * k[1]]


def b2_closed(d):
    """Closed form of the chiral k^2 dispersion term: b2(khat) = -(1/3) kx ky kz."""
    u = _unit(d)
    return -u[0] * u[1] * u[2] / 3


def _series(Om, d, powers, ks):
    """Fit Om(k d)/|k| = sum_j a_j |k|^{powers[j]} on the given |k| samples."""
    d = _unit(d)
    n = len(powers)
    A = mp.matrix(n, n)
    b = mp.matrix(n, 1)
    for i, kk in enumerate(ks):
        b[i] = Om([kk * x for x in d]) / kk
        for j, p in enumerate(powers):
            A[i, j] = kk ** p
    return mp.lu_solve(A, b)


def _richardson(f, ks, p=1):
    """Two-point Richardson extrapolation of f(k) = f0 + O(k^p) to k -> 0.

    The order p is not cosmetic. The even-law radial coefficient carries an
    O(|k|^2) correction (odd powers only, F246), the chiral-branch ratios carry
    O(|k|), and using the wrong p leaves a residual LARGER than the raw value
    at the smaller sample — which is how this check first went red.
    """
    k1, k2 = mp.mpf(ks[0]), mp.mpf(ks[1])
    a1, a2 = k1 ** p, k2 ** p
    return (a2 * f(k1) - a1 * f(k2)) / (a2 - a1)


# ----------------------------------------------------------------------------
# the deformed (E, P) realisation — leg A
# ----------------------------------------------------------------------------
def deformed_EP(kv, s=1, m=0):
    """(E, P) = (sin omega, (n/c) sin omega_0 khat) — the exact Minkowski shell."""
    n = mp.sqrt(1 - mp.mpf(m) ** 2)
    k = _norm(kv)
    s0 = mp.sin(omega_branch(kv, s, 0))
    return mp.sin(omega_branch(kv, s, m)), [(n / _C) * s0 * mp.mpf(x) / k for x in kv]


def lorentz(E, P, v, nh):
    """Linear Lorentz boost of VELOCITY v along nh, acting on (E, c P)."""
    b = mp.mpf(v) / _C
    g = 1 / mp.sqrt(1 - b ** 2)
    pp = sum(P[i] * nh[i] for i in range(3))
    pp2 = g * (pp - b * E / _C)
    return g * (E - b * _C * pp), [P[i] + (pp2 - pp) * nh[i] for i in range(3)]


def deformed_to_k(E, P, s=1, m=0, seed=mp.mpf('0.5')):
    """Invert (E,P) -> k on the branch: solve sin omega_0(|k| Phat) = c|P|/n."""
    n = mp.sqrt(1 - mp.mpf(m) ** 2)
    pn = _norm(P)
    kh = [mp.mpf(x) / pn for x in P]
    tgt = _C * pn / n
    kn = mp.findroot(
        lambda t: mp.sin(omega_branch([t * x for x in kh], s, 0)) - tgt, seed)
    return [kn * x for x in kh]


# ----------------------------------------------------------------------------
# the gate entry
# ----------------------------------------------------------------------------
def check_boost_covariance():
    """Ten checks on the finite-a Poincare defect. Six are negative controls."""
    out = {}
    dirs = [(1, 1, 1), (2, 1, 1), (1, 1, 0), (3, 1, 2), (5, 3, 2)]

    # -- B1: the exact massive mass shell (algebraic) -------------------------
    worst = mp.mpf(0)
    for m in ['0.3', '0.7', '0.95']:
        for d in dirs:
            for kk in ['0.2', '0.9', '1.7']:
                kv = [mp.mpf(kk) * x for x in _unit(d)]
                r = (mp.sin(omega_branch(kv, 1, m)) ** 2
                     - (1 - mp.mpf(m) ** 2) * mp.sin(omega_branch(kv, 1, 0)) ** 2
                     - mp.mpf(m) ** 2)
                worst = max(worst, abs(r))
    out["B1_massive_shell_worst_residual"] = mp.nstr(worst, 4)
    assert worst < mp.mpf('1e-40'), worst
    # control: perturb n^2 by 1% and the identity must break
    kv = [mp.mpf('0.9') * x for x in _unit((1, 1, 1))]
    ctl = (mp.sin(omega_branch(kv, 1, '0.7')) ** 2
           - mp.mpf('1.01') * (1 - mp.mpf('0.49'))
           * mp.sin(omega_branch(kv, 1, 0)) ** 2 - mp.mpf('0.49'))
    out["B1_control_wrong_n2_residual"] = mp.nstr(abs(ctl), 4)
    assert abs(ctl) > mp.mpf('1e-4'), ctl

    # -- B2: exact all-order covariance on the cubic axes ---------------------
    worst_ax = mp.mpf(0)
    laws = (omega_even, lambda v: omega_branch(v, 1), lambda v: omega_branch(v, -1))
    for kk in ['0.5', '1.5', '2.5', '3.0']:
        for ax in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            kv = [mp.mpf(kk) * x for x in ax]
            for Om in laws:
                worst_ax = max(worst_ax, abs(Om(kv) - _C * mp.mpf(kk)))
                worst_ax = max(worst_ax, max(abs(x) for x in defect(Om, kv)))
    out["B2_axis_worst_deviation_and_defect"] = mp.nstr(worst_ax, 4)
    assert worst_ax < mp.mpf('1e-35'), worst_ax
    # control: <111> must NOT be covariant
    kv = [mp.mpf('0.5') * x for x in _unit((1, 1, 1))]
    off = max(abs(x) for x in defect(omega_even, kv))
    out["B2_control_111_defect"] = mp.nstr(off, 4)
    assert off > mp.mpf('1e-6'), off

    # -- B3: photon closed form ----------------------------------------------
    worst_rel = mp.mpf(0)
    for d in dirs:
        for kk in ['1e-5', '1e-6']:
            kv = [mp.mpf(kk) * x for x in _unit(d)]
            num = defect(omega_even, kv)
            cf = defect_closed_even(kv)
            scale = max(abs(x) for x in cf)
            worst_rel = max(worst_rel,
                            max(abs(num[i] - cf[i]) for i in range(3)) / scale)
    out["B3_photon_closed_form_worst_rel"] = mp.nstr(worst_rel, 4)
    assert worst_rel < mp.mpf('1e-12'), worst_rel
    # radial form -(1/18)(p+3q), Richardson-extrapolated to k -> 0
    rad = {}
    worst_rad = mp.mpf(0)
    for d in [(1, 1, 1), (1, 1, 0), (2, 1, 1), (3, 1, 2)]:
        u = _unit(d)
        x2, y2, z2 = u[0] ** 2, u[1] ** 2, u[2] ** 2
        p = x2 * y2 + y2 * z2 + z2 * x2
        q = x2 * y2 * z2
        f = lambda kk: (sum(defect(omega_even, [kk * x for x in u], i) * u[i]
                            for i in range(3)) / kk ** 3)
        meas = _richardson(f, ['2e-3', '1e-3'], p=2)
        pred = -(p + 3 * q) / 18
        rad[str(d)] = [mp.nstr(meas, 12), mp.nstr(pred, 12)]
        worst_rad = max(worst_rad, abs(meas - pred))
    out["B3_radial_minus_p_plus_3q_over_18"] = rad
    out["B3_radial_worst_abs"] = mp.nstr(worst_rad, 4)
    assert worst_rad < mp.mpf('1e-15'), worst_rad
    # the two rational anchors, exactly
    assert abs(-mp.mpf(1) / 18 * (mp.mpf(1) / 3 + mp.mpf(3) / 27)
               + mp.mpf(2) / 81) < mp.mpf('1e-40')
    assert abs(-mp.mpf(1) / 18 * mp.mpf(1) / 4 + mp.mpf(1) / 72) < mp.mpf('1e-40')
    out["B3_anchors"] = {"<111>": "-2/81", "<110>": "-1/72", "<100>": "0"}

    # -- B4: chiral b2 closed form (extends F246) -----------------------------
    # Two independent estimators. The direct Richardson limit is the assertion:
    # its residual is O(|k|^2) and is CHECKED to scale as O(|k|^2), so the
    # agreement is not a tolerance that happens to be loose enough. The 5-term
    # Vandermonde fit is the cross-check and floors at ~1e-14 on CONDITIONING,
    # not precision — raising dps does not move it.
    worst_b2 = mp.mpf(0)
    worst_scale = mp.mpf(0)
    resid = {}
    for d in dirs + [(1, 0, 0)]:
        u = _unit(d)
        f = lambda kk, u=u: (omega_branch([kk * x for x in u], 1) / kk - _C) / kk
        fine = abs(_richardson(f, ['1e-5', '5e-6'], p=1) - b2_closed(d))
        coarse = abs(_richardson(f, ['1e-4', '5e-5'], p=1) - b2_closed(d))
        worst_b2 = max(worst_b2, fine)
        resid[str(d)] = mp.nstr(fine, 4)
        if b2_closed(d) != 0:                      # generic direction
            worst_scale = max(worst_scale, abs(coarse / fine - 100) / 100)
    out["B4_b2_richardson_worst"] = mp.nstr(worst_b2, 4)
    out["B4_b2_residual_is_O_k2_worst_rel"] = mp.nstr(worst_scale, 4)
    out["B4_b2_residual_by_direction"] = resid
    assert worst_b2 < mp.mpf('1e-13'), worst_b2
    assert worst_scale < mp.mpf('1e-2'), worst_scale
    # on a coordinate plane b2 vanishes identically, so the residual there is
    # the NEXT odd term and must be orders smaller than the generic direction
    assert (mp.mpf(resid["(1, 1, 0)"]) * 100
            < mp.mpf(resid["(1, 1, 1)"])), (resid["(1, 1, 0)"], resid["(1, 1, 1)"])
    worst_fit = mp.mpf(0)
    ks = [mp.mpf('1e-3') * (i + 1) for i in range(5)]
    for d in dirs + [(1, 0, 0)]:
        co = _series(lambda v: omega_branch(v, 1), d, [0, 1, 2, 3, 4], ks)
        worst_fit = max(worst_fit, abs(co[1] - b2_closed(d)))
        assert abs(co[0] - _C) < mp.mpf('1e-15'), (d, co[0])
    out["B4_b2_series_fit_worst"] = mp.nstr(worst_fit, 4)
    assert worst_fit < mp.mpf('1e-12'), worst_fit
    # F246's two published numbers, from the closed form
    out["B4_c2_111_vs_minus_sqrt3_over_54"] = mp.nstr(
        abs(b2_closed((1, 1, 1)) / 2 + _R3 / 54), 4)
    out["B4_c2_211_vs_minus_sqrt6_over_108"] = mp.nstr(
        abs(b2_closed((2, 1, 1)) / 2 + mp.sqrt(6) / 108), 4)
    assert abs(b2_closed((1, 1, 1)) / 2 + _R3 / 54) < mp.mpf('1e-40')
    assert abs(b2_closed((2, 1, 1)) / 2 + mp.sqrt(6) / 108) < mp.mpf('1e-40')
    # differential control: the EVEN law must have c2 -> 0 where the single law does not
    kse = [mp.mpf('1e-2') * (i + 1) for i in range(5)]
    co_e = _series(omega_even, (1, 1, 1), [0, 1, 2, 3, 4], kse)
    co_s = _series(omega_single, (1, 1, 1), [0, 1, 2, 3, 4], kse)
    out["B4_even_c2_vs_single_c2"] = [mp.nstr(co_e[1], 4), mp.nstr(co_s[1], 10)]
    assert abs(co_e[1]) < mp.mpf('1e-10') < abs(co_s[1]), (co_e[1], co_s[1])

    # -- B5: chiral defect closed form + chirality-oddness --------------------
    worst_br = mp.mpf(0)
    for s in (1, -1):
        for d in [(1, 1, 1), (2, 1, 1), (3, 1, 2)]:
            u = _unit(d)
            for i in range(3):
                def f(kk, i=i, s=s, u=u):
                    kv = [kk * x for x in u]
                    return (defect(lambda v: omega_branch(v, s), kv, i)
                            / defect_closed_branch(kv, s)[i])
                worst_br = max(worst_br, abs(_richardson(f, ['1e-5', '5e-6']) - 1))
    out["B5_branch_closed_form_worst_rel"] = mp.nstr(worst_br, 4)
    assert worst_br < mp.mpf('1e-12'), worst_br
    # chirality-odd: the SUM of the two branch defects is one order smaller
    ratios = []
    for kk in ['0.02', '0.01']:
        kv = [mp.mpf(kk) * x for x in _unit((1, 1, 1))]
        dp = defect(lambda v: omega_branch(v, 1), kv, 0)
        dm = defect(lambda v: omega_branch(v, -1), kv, 0)
        ratios.append(abs(dp + dm) / abs(dp))
    out["B5_chirality_odd_ratio_at_k_0.02_0.01"] = [mp.nstr(r, 4) for r in ratios]
    assert ratios[0] < mp.mpf('1e-2'), ratios
    assert ratios[0] / ratios[1] > mp.mpf('1.5'), ratios   # it is a k-suppression

    # -- B6: F22 bridge — 1D reduction and the BCC massive limit --------------
    from casim.engine.interactions.derive_velocity_addition import rho as rho_1d
    c1 = 1 / mp.sqrt(2)
    om1 = lambda k, m: mp.acos(mp.sqrt(1 - mp.mpf(m) ** 2) * mp.cos(k / mp.sqrt(2)))
    worst_1d = mp.mpf(0)
    tab = {}
    for m in ['0.3', '0.5', '0.7', '0.95']:
        k = mp.mpf('1e-6')
        D = mp.diff(lambda t: om1(t, m) ** 2, k) / (2 * c1 ** 2) - k
        pred = 1 / mp.mpf(rho_1d(float(m))) - 1
        worst_1d = max(worst_1d, abs(D / k - pred))
        tab[m] = [mp.nstr(D / k, 12), mp.nstr(pred, 12)]
    out["B6_1d_D_over_k_equals_one_over_rho_minus_one"] = tab
    assert worst_1d < mp.mpf('1e-9'), worst_1d
    # control: F22's own deliberately-wrong rho = m/asin(m) must NOT match
    m = mp.mpf('0.5')
    bad = 1 / (m / mp.asin(m)) - 1
    k = mp.mpf('1e-6')
    D = mp.diff(lambda t: om1(t, '0.5') ** 2, k) / (2 * c1 ** 2) - k
    out["B6_control_wrong_rho_gap"] = mp.nstr(abs(D / k - bad), 4)
    assert abs(D / k - bad) > mp.mpf('1e-3'), bad
    # BCC massive branch: D_i -> (1/rho - 1) k_i, the SAME rho(m)
    worst_3d = mp.mpf(0)
    tab3 = {}
    for m in ['0.3', '0.5', '0.7']:
        u = _unit((1, 1, 1))
        f = lambda kk: (defect(lambda v: omega_branch(v, 1, m),
                               [kk * x for x in u], 0) / (kk * u[0]))
        meas = _richardson(f, ['1e-7', '5e-8'])
        pred = 1 / mp.mpf(rho_1d(float(m))) - 1
        tab3[m] = [mp.nstr(meas, 10), mp.nstr(pred, 10)]
        worst_3d = max(worst_3d, abs(meas - pred) / abs(pred))
    out["B6_bcc_massive_rho"] = tab3
    out["B6_bcc_massive_worst_rel"] = mp.nstr(worst_3d, 4)
    assert worst_3d < mp.mpf('1e-13'), worst_3d

    # -- B7: operational meaning — off-shell residual = v (D . vhat) ---------
    nh = _unit((1, 0, 0))
    scaling = {}
    for label, Om in [("even", omega_even),
                      ("branch+", lambda v: omega_branch(v, 1))]:
        kv = [mp.mpf('0.05') * x for x in _unit((2, 1, 1))]
        Dv = sum(defect(Om, kv, i) * nh[i] for i in range(3))
        errs = []
        for v in ['1e-11', '1e-13']:
            vv = mp.mpf(v)
            E2, k2 = lorentz(Om(kv), kv, vv, nh)
            errs.append(abs((E2 - Om(k2)) / vv - Dv) / abs(Dv))
        scaling[label] = [mp.nstr(e, 4) for e in errs]
        # residual = v(D.vhat) + O(v^2): 100x smaller v => ~100x smaller rel err
        assert errs[0] / errs[1] > 50, (label, errs)
        assert errs[1] < mp.mpf('1e-13'), (label, errs)
    out["B7_residual_is_v_times_D_rel_err_at_v_1e-11_1e-13"] = scaling

    # -- B8: the deformed realisation is exact, and closes -------------------
    worst_sh = mp.mpf(0)
    worst_cl = mp.mpf(0)
    for m in ['0', '0.5']:
        for d in [(1, 1, 1), (2, 1, 1)]:
            kv = [mp.mpf('0.6') * x for x in _unit(d)]
            E, P = deformed_EP(kv, 1, m)
            worst_sh = max(worst_sh, abs(E ** 2 - _C2 * sum(x ** 2 for x in P)
                                         - mp.mpf(m) ** 2))
            v1, v2 = mp.mpf('0.13') * _C, mp.mpf('0.21') * _C
            E1, P1 = lorentz(E, P, v1, _unit((1, 0, 0)))
            k1 = deformed_to_k(E1, P1, 1, m, mp.mpf('0.6'))
            worst_sh = max(worst_sh, abs(mp.sin(omega_branch(k1, 1, m)) - E1))
            E2a, P2a = lorentz(E1, P1, v2, _unit((1, 0, 0)))
            vt = (v1 + v2) / (1 + v1 * v2 / _C2)
            E2b, P2b = lorentz(E, P, vt, _unit((1, 0, 0)))
            worst_cl = max(worst_cl, abs(E2a - E2b),
                           max(abs(P2a[i] - P2b[i]) for i in range(3)))
    out["B8_deformed_shell_worst"] = mp.nstr(worst_sh, 4)
    out["B8_deformed_closure_worst"] = mp.nstr(worst_cl, 4)
    assert worst_sh < mp.mpf('1e-38'), worst_sh
    assert worst_cl < mp.mpf('1e-38'), worst_cl
    # control: the CANONICAL momentum does NOT sit on the same shell
    kv = [mp.mpf('0.6') * x for x in _unit((1, 1, 1))]
    canon = abs(mp.sin(omega_branch(kv, 1, 0)) ** 2
                - _C2 * sum(x ** 2 for x in kv))
    out["B8_control_canonical_k_shell_violation"] = mp.nstr(canon, 4)
    assert canon > mp.mpf('1e-3'), canon

    # -- B9: no universal momentum map (the DSR no-go) -----------------------
    tabu = {}
    worst_u = mp.mpf(0)
    for d in [(1, 1, 1), (2, 1, 1), (3, 1, 2)]:
        u = _unit(d)
        f = lambda kk: (omega_even([kk * x for x in u])
                        - omega_branch([kk * x for x in u], 1)) / kk ** 2
        meas = _richardson(f, ['1e-5', '5e-6'], p=1)
        pred = u[0] * u[1] * u[2] / 3
        tabu[str(d)] = [mp.nstr(meas, 10), mp.nstr(pred, 10)]
        worst_u = max(worst_u, abs(meas - pred))
        assert abs(meas) > mp.mpf('1e-3'), (d, meas)
    out["B9_universality_gap_one_third_kxkykz"] = tabu
    out["B9_universality_worst_abs"] = mp.nstr(worst_u, 4)
    assert worst_u < mp.mpf('1e-13'), worst_u
    # control: it DOES vanish on a coordinate plane — the gap is not a fit artifact
    u = _unit((1, 1, 0))
    plane = abs(omega_even([mp.mpf('0.02') * x for x in u])
                - omega_branch([mp.mpf('0.02') * x for x in u], 1))
    out["B9_control_coordinate_plane_gap"] = mp.nstr(plane, 4)
    assert plane < mp.mpf('1e-7'), plane

    # -- B10: the algebra bookkeeping, symbolically --------------------------
    out.update(_check_algebra())

    out["n_checks"] = 10
    out["n_controls"] = 6
    out["verdict"] = (
        "Finite-a boost covariance on BCC is BROKEN, with an exact order, an "
        "exact coefficient and an exact reason. The whole Poincare defect is the "
        "gradient of one scalar, Phi = (Omega^2 - c^2 k^2)/2c^2 -- boost "
        "covariance IS the non-running of the off-shell invariant mass, and "
        "[K,P] never fails while the [K,K] defect reduces to the same D_i. It "
        "is EXACT to all orders on the three cubic axes; O(|k|^3) for the F26 "
        "even photon, D.khat = -(1/18)(p+3q)|k|^3 with rational anchors -2/81 "
        "on <111> and -1/72 on <110>; and one order worse, O(|k|^2), on a "
        "chiral branch, D = -s c_lat (kykz, kzkx, kxky). The even law's extra "
        "order is the chirality-oddness of b2(khat) = -(1/3)kxkykz -- the same "
        "helicity symmetrisation that kills birefringence. In 1D the defect "
        "reduces to F22's 1/rho - 1, and the BCC massive branch reproduces the "
        "same rho(m) F22 said had no BCC analogue. A deformed (E,P) realisation "
        "IS exact -- sin^2 w - (1-m^2) sin^2 w_0 = m^2 identically, at finite "
        "a, for every m -- but it is not universal: Omega_even - omega_+ = "
        "(1/3) khatx khaty khatz |k|^2, so no single momentum map serves the "
        "photon and the fermion."
    )
    return out


def _check_algebra():
    """Sympy: which Poincare brackets survive at finite a, for ARBITRARY Omega."""
    import sympy as sp
    k1, k2, k3 = sp.symbols('k1 k2 k3', real=True)
    K = [k1, k2, k3]
    psi = sp.Function('psi')(k1, k2, k3)
    Om = sp.Function('Omega')(k1, k2, k3)
    f = sp.Function('f')(k1, k2, k3)
    c2 = sp.Rational(1, 3)                      # c_lat^2 on BCC
    x_ = lambda i, e: sp.I * sp.diff(e, K[i])
    D = lambda i: sp.diff(Om ** 2, K[i]) / (2 * c2) - K[i]

    def Kop(i, e, extra=None):
        r = (x_(i, Om * e) + Om * x_(i, e)) / (2 * c2)
        return r if extra is None else r + extra * e

    out = {}
    # [K_i,H] = i P_i + i D_i
    res = [sp.simplify(sp.expand(Kop(i, Om * psi) - Om * Kop(i, psi)
                                 - sp.I * K[i] * psi - sp.I * D(i) * psi))
           for i in range(3)]
    out["B10_KH_defect_is_D"] = [str(r) for r in res]
    assert all(r == 0 for r in res), res
    # invariance under K -> K + f(k)
    inv = sp.simplify(sp.expand(
        (Kop(0, Om * psi, f) - Om * Kop(0, psi, f))
        - (Kop(0, Om * psi) - Om * Kop(0, psi))))
    out["B10_D_invariant_under_K_plus_f"] = str(inv)
    assert inv == 0, inv
    # [K_i,P_j] exact for arbitrary Omega
    bad = []
    for i in range(3):
        for j in range(3):
            r = sp.simplify(Kop(i, K[j] * psi) - K[j] * Kop(i, psi)
                            - (1 if i == j else 0) * sp.I * Om * psi / c2)
            if r != 0:
                bad.append((i, j, str(r)))
    out["B10_KP_exact_for_arbitrary_Omega"] = (not bad)
    assert not bad, bad
    # [K_i,K_j] = rotation + (i/c^2)(D_i x_j - D_j x_i): no new obstruction
    res2 = []
    for (i, j) in [(0, 1), (1, 2), (2, 0)]:
        lhs = Kop(i, Kop(j, psi)) - Kop(j, Kop(i, psi))
        rot = (sp.I / c2) * (K[i] * x_(j, psi) - K[j] * x_(i, psi))
        pred = rot + (sp.I / c2) * (D(i) * x_(j, psi) - D(j) * x_(i, psi))
        res2.append(sp.simplify(sp.expand(lhs - pred)))
    out["B10_KK_defect_reduces_to_D"] = [str(r) for r in res2]
    assert all(r == 0 for r in res2), res2
    # control: a wrong D must NOT close the [K,H] bracket
    ctl = sp.simplify(sp.expand(Kop(0, Om * psi) - Om * Kop(0, psi)
                                - sp.I * K[0] * psi
                                - sp.I * (D(0) + K[0] / 100) * psi))
    out["B10_control_wrong_D_nonzero"] = (ctl != 0)
    assert ctl != 0, ctl
    return out


def verify():
    res = check_boost_covariance()
    print("=" * 78)
    print("Finite-a boost covariance on BCC — the Poincare defect D_i = d_i Phi")
    print("  Phi = (Omega^2 - c_lat^2 |k|^2) / 2 c_lat^2   (off-shell invariant mass)")
    print("=" * 78)
    for k, v in res.items():
        if k == "verdict":
            continue
        print(f"  {k:56s} {v}")
    print("-" * 78)
    print(res["verdict"])
    return res


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path
    r = verify()
    path = results_path("F301_boost_covariance.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2)
    print(f"\nwrote {path}")
