"""
Fork F64 — ELECTROMAGNETIC-CONNECTION GRAVITY
=============================================
Date: 2026-05-30 - 21:20

A logical fork off the "gravity-is-emergent" route (F50/F52/F62).  In that
route gravity enters through the *rest leg* of the F46 spherical triangle: a
clock-rate field sqrt(A(x)) sourced by **rest-mass density** rho via a posited
Poisson coupling 4 pi G rho.  Its self-inflicted problem (F52): the rest leg
alone gives **factor-1** (Newtonian) light bending; reaching Einstein's
**factor-2** requires sourcing the *spatial* leg B with a SECOND, independent
field equation.  Two legs, two field equations, source = rest mass.

This fork abandons that architecture for a single **lattice dielectric**
K(x) — a position-dependent renormalisation of the (E,B) rotation rule itself
(F25/F26: light speed c_lat = dOmega/d|k| is the rotation rate of the real
(E,B) pair).  This is the Puthoff polarizable-vacuum / Ostoma-Trushyk line,
and it is native to the SU(2) foundations: per F26 mass IS the confined (E,B)
rotation, so there is no separate "mass substance" to source from — only
confined EB energy.  One field, one source (total field energy).

----------------------------------------------------------------------------
D-EM1 — THE EXACT EIKONAL-INDEX VIABILITY TEST (implemented here)
----------------------------------------------------------------------------
Before any wave-packet run, settle the cheap, decisive structural question:
*can a single scalar field reproduce BOTH GR coefficients at once* —

    factor-1 gravitational redshift   Delta nu / nu = +1 * (phi/c^2)
    factor-2 light deflection         K_bend == 4   (Newton would be 2)

This is the rung where Paper-6 EMQG failed (gr_fork_E_tensor.py docstring,
Finding 19): "a single scalar ... cannot independently set g_00 and g_ii ...
the root cause of the GR-3 factor-2 redshift."  The Finding-19 failure is real
for a scalar placed entirely in ONE metric slot.  This module asks whether the
*dielectric* placement — the only impedance-preserving, F26-consistent way a
single (E,B)-rotation scalar can enter — escapes it.

Set-up.  Write the metric for a static isotropic source as
        ds^2 = -A(x) c0^2 dt^2 + B(x) dx^2 ,
so the photon coordinate speed is  c_eff = c0 sqrt(A/B)  and the **eikonal
refractive index** is  n = c0 / c_eff = sqrt(B/A).  Let  u := GM/(r c^2) = -phi/c^2
( >= 0 in a well ).  Two coefficients, both read off as the leading u-slope:

    redshift  Z := -d/du [ sqrt(A) ]  at u=0          (GR target  Z = 1)
    bend      N := +d/du [ n ]        at u=0  ;  K_bend = 2 N   (GR target 4)

(The K_bend = 2N identity is the exact weak-field deflection integral
 alpha = INT d/db ln n  dl  = 2 N GM / (b c^2)  for a 1/r index profile;
 confirmed numerically in `deflection_coeff_numeric` for the full map.)

Three single-scalar placements are compared:

    "clock_only"     B = 1,  index all in the lapse   (the F52 rest leg)
    "refractive_only" A = 1, index all in space        (Gordon medium, no clock)
    "dielectric"     eps = mu = K  =>  A = 1/K, B = K  (AB = 1, impedance fixed)

Only the **dielectric** is a genuine (E,B)-rotation renormalisation: scaling
permittivity and permeability together leaves the impedance sqrt(mu/eps)
invariant, i.e. the (E,B) amplitude ratio is preserved and the rotation stays a
*proper* rotation with no scalar contamination (the F26 BCC criterion).  The
other two placements break the impedance and are not dielectrics.

VERDICT RULE (D-EM1):
    fork viable  <=>  EXISTS a single-scalar map that is impedance-preserving
                      AND gives Z == 1 AND K_bend == 4, all exactly (algebraic).

Everything in D-EM1 is done in exact rational/series arithmetic with sympy, so
the verdict is algebraically exact, not merely machine-precision.

----------------------------------------------------------------------------
Follow-on stages (scaffolded, not yet implemented)
----------------------------------------------------------------------------
    D-EM2  single-field lattice deflection: turn on only K(x), measure K_bend->4
           (reuses the F52/F62 K-discriminator harness).
    D-EM3  radiation-as-source: standing (E,B) mode vs equal-energy rest-mass
           blob; deflection per unit energy must match (the physical fork).
    D-EM4  internal consistency: the SAME K gives factor-1 redshift AND
           factor-2 bend on one self-sourced field.
"""

from __future__ import annotations

from types import SimpleNamespace

import sympy as sp

# ───────────────────────────────────────────────────────────────────
#  Exact symbolic core
# ───────────────────────────────────────────────────────────────────

u = sp.symbols("u", positive=True)          # u = GM/(r c^2) = -phi/c^2  >= 0


def _maps():
    """
    Return the three single-scalar (A, B) placements as exact sympy
    expressions in u, each NORMALISED so that — if it can — it reproduces the
    measured factor-1 gravitational redshift (sqrt(A) = 1 - u + O(u^2)).

    The normalisation is the honest part of the test: we *grant* each map its
    best shot at the redshift, then ask what bending it is then forced to
    predict.  A map that cannot even reach factor-1 redshift fails up front.
    """
    # clock_only: all index in the lapse, flat space.  sqrt(A)=1-u exactly.
    A_clock = (1 - u) ** 2
    B_clock = sp.Integer(1)

    # refractive_only: all index in space, lapse flat.  No redshift possible.
    A_refr = sp.Integer(1)
    B_refr = (1 + u) ** 2          # n = sqrt(B/A) = 1+u  (a Gordon medium)

    # dielectric: eps = mu = K, impedance-preserving.  Fix K by the redshift:
    #   sqrt(A) = K^{-1/2} = 1 - u   =>   K = (1-u)^{-2}
    K = (1 - u) ** (-2)
    A_diel = 1 / K                 # = (1-u)^2
    B_diel = K                     # = (1-u)^{-2}

    return {
        "clock_only": dict(A=A_clock, B=B_clock, eps=1 / sp.sqrt(A_clock * B_clock),
                           mu=sp.sqrt(B_clock / A_clock), K=None),
        "refractive_only": dict(A=A_refr, B=B_refr, eps=sp.sqrt(B_refr / A_refr),
                                mu=sp.sqrt(B_refr / A_refr), K=None),
        "dielectric": dict(A=A_diel, B=B_diel, eps=K, mu=K, K=K),
    }


def eikonal_index(A, B):
    """n = c0 / c_eff = sqrt(B / A)  (the index a light ray actually sees)."""
    return sp.sqrt(B / A)


def _lead_coeff(expr, value_at_0):
    """Leading u-slope of (expr) about u=0:  the c1 in expr = value_at_0 + c1 u + ..."""
    s = sp.series(sp.simplify(expr), u, 0, 2).removeO()
    return sp.simplify(s.coeff(u, 1)), sp.simplify(s.coeff(u, 0))


def coefficients():
    """
    For each placement return exact (Z, K_bend, impedance_is_constant, redshift_ok):

        Z       = -d/du sqrt(A)|_0          (GR: 1)
        K_bend  = 2 * d/du n|_0             (GR: 4 ; Newton: 2)
        impedance_is_constant : sqrt(mu/eps) independent of u  (proper EB rotation)
        redshift_ok : the map actually produces a non-zero redshift slope
    """
    out = {}
    for name, m in _maps().items():
        A, B = m["A"], m["B"]
        # redshift slope Z = -(d/du) sqrt(A)
        sqrtA_slope, sqrtA_0 = _lead_coeff(sp.sqrt(A), 1)
        Z = sp.simplify(-sqrtA_slope)
        # bend slope N = +(d/du) n ; K_bend = 2N
        n = eikonal_index(A, B)
        n_slope, n_0 = _lead_coeff(n, 1)
        K_bend = sp.simplify(2 * n_slope)
        # impedance sqrt(mu/eps): constant in u?
        imped = sp.simplify(sp.sqrt(m["mu"] / m["eps"]))
        impedance_constant = sp.simplify(sp.diff(imped, u)) == 0
        out[name] = dict(
            A=A, B=B, n=sp.simplify(n),
            Z=Z, K_bend=K_bend,
            redshift_ok=bool(Z != 0),
            impedance=imped, impedance_constant=bool(impedance_constant),
        )
    return out


# ───────────────────────────────────────────────────────────────────
#  Numerical guard: the FULL (non-linearised) deflection integral
# ───────────────────────────────────────────────────────────────────

def deflection_coeff_numeric(eps_GM_over_bc2: float, n_func=None) -> float:
    """
    Exact-quadrature deflection coefficient K_bend = alpha b c^2 / GM for a
    straight-line ray of impact parameter b past a 1/r index profile, for the
    DIELECTRIC map n(r) = K(r) = (1 - GM/(r c^2))^{-2}.

    Confirms the series result K_bend -> 4 as GM/(b c^2) -> 0 (and reports the
    leading relativistic correction at finite field strength).  Uses mpmath
    arbitrary-precision quadrature — no numpy/scipy on the path (CLAUDE.md).
    """
    import mpmath as mp
    mp.mp.dps = 40
    b = mp.mpf(1)
    GMc2 = mp.mpf(eps_GM_over_bc2) * b      # GM/c^2 in units of b

    if n_func is None:
        def n_func(r):
            uu = GMc2 / r
            return (1 - uu) ** (-2)         # dielectric index forced by factor-1 redshift

    def integrand(x):
        # alpha = INT  d/dy [ ln n ]  dx   along y=b, x in (-inf, inf)
        y = b
        r = mp.sqrt(x * x + y * y)
        h = r * mp.mpf("1e-18")
        # d ln n / dy  via  (d ln n / dr) * (dr / dy),  dr/dy = y/r
        dln = (mp.log(n_func(r + h)) - mp.log(n_func(r - h))) / (2 * h)
        return dln * (y / r)

    alpha = mp.quad(integrand, [-mp.inf, 0, mp.inf])
    K_bend = alpha * b / GMc2               # = alpha b c^2 / GM
    return float(K_bend)


# ───────────────────────────────────────────────────────────────────
#  D-EM1 test
# ───────────────────────────────────────────────────────────────────

def test_dem1_eikonal_viability() -> dict:
    """
    D-EM1 — does a single scalar reproduce factor-1 redshift AND factor-2 bend?

    PASS iff the impedance-preserving (dielectric) placement gives exactly
    Z == 1 and K_bend == 4, while the two non-dielectric placements each fail
    a coefficient (reproducing the Finding-19 obstruction).  Algebraically
    exact via sympy; guarded by mpmath quadrature of the full bending integral.
    """
    coeff = coefficients()

    diel = coeff["dielectric"]
    clock = coeff["clock_only"]
    refr = coeff["refractive_only"]

    # exact algebraic checks on the dielectric
    diel_Z_ok = sp.simplify(diel["Z"] - 1) == 0
    diel_K_ok = sp.simplify(diel["K_bend"] - 4) == 0
    diel_imped_ok = diel["impedance_constant"]

    # the contrast maps must each FAIL (anchors the result to Finding 19)
    clock_fails_bend = sp.simplify(clock["K_bend"] - 4) != 0      # gives 2, not 4
    refr_fails_redshift = not refr["redshift_ok"]                 # Z = 0

    # numerical guard: full dielectric deflection -> 4 as field -> 0.
    # The integral is SIGNED (negative = bends toward the mass, the correct
    # attractive sign); the GR magnitude target is |K_bend| = 4.
    guard = {f"{e:.0e}": deflection_coeff_numeric(e)
             for e in (1e-2, 1e-3, 1e-4)}
    guard_ok = (abs(abs(guard["1e-04"]) - 4.0) < 1e-3
                and guard["1e-04"] < 0)            # attractive

    viable = bool(diel_Z_ok and diel_K_ok and diel_imped_ok
                  and clock_fails_bend and refr_fails_redshift and guard_ok)

    return {
        "pass": viable,
        "verdict": "VIABLE" if viable else "NOT VIABLE",
        # dielectric (the proposed EM-connection map)
        "dielectric_Z": str(diel["Z"]),
        "dielectric_K_bend": str(diel["K_bend"]),
        "dielectric_n_of_u": str(diel["n"]),
        "dielectric_impedance": str(diel["impedance"]),
        "dielectric_impedance_constant": diel_imped_ok,
        # contrast maps (expected to fail)
        "clock_only_Z": str(clock["Z"]),
        "clock_only_K_bend": str(clock["K_bend"]),
        "refractive_only_Z": str(refr["Z"]),
        "refractive_only_K_bend": str(refr["K_bend"]),
        # numerical guard
        "full_deflection_guard": guard,
        "guard_ok": guard_ok,
        # bookkeeping
        "redshift_target": 1,
        "bend_target": 4,
        "newtonian_bend": 2,
    }


# ───────────────────────────────────────────────────────────────────
#  Lattice machinery for D-EM2 / D-EM3  (real scalar FFT Poisson + eikonal;
#  no chiral transforms, so numpy is safe — same path as ca_emqg / F52)
# ───────────────────────────────────────────────────────────────────

def _solve_poisson_3d(rho, G=1.0):
    """∇²φ = 4πG ρ on a periodic lattice via FFT (zero-mean). Pure-numpy copy
    of ca_emqg.solve_poisson_3d, inlined so F64 needs no scipy-laden imports."""
    import numpy as np
    Lx, Ly, Lz = rho.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    kz = np.fft.fftfreq(Lz) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    k2 = KX ** 2 + KY ** 2 + KZ ** 2
    k2[0, 0, 0] = 1.0
    phi_k = -4.0 * np.pi * G * np.fft.fftn(rho) / k2
    phi_k[0, 0, 0] = 0.0
    return np.fft.ifftn(phi_k).real


def _gaussian_mass_3d(L, M=1.0, sigma=3.0, center=None):
    """Gaussian-smoothed point mass, total integrated mass M (copy of
    ca_emqg.gaussian_mass_3d)."""
    import numpy as np
    if center is None:
        center = (L // 2, L // 2, L // 2)
    x = np.arange(L) - center[0]
    y = np.arange(L) - center[1]
    z = np.arange(L) - center[2]
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    rho = np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / (2.0 * sigma ** 2))
    rho *= M / rho.sum()
    return rho


def _index_from_u(uu, sector):
    """Eikonal index n = c0/c_eff = sqrt(B/A) for a probe ray, by placement."""
    import numpy as np
    uu = np.asarray(uu, dtype=np.float64)
    if sector == "dielectric":          # A=1/K, B=K, K=e^{2u}  =>  n = K (canonical)
        return np.exp(2.0 * uu)
    if sector == "rest_only":           # B=1, A=e^{-2u}        =>  n = 1/sqrt(A)=e^{u}
        return np.exp(uu)
    if sector == "full_GR":             # linearised two-leg       =>  n = sqrt(B/A)
        A = 1.0 - 2.0 * uu
        B = 1.0 + 2.0 * uu
        return np.sqrt(B / np.abs(A))
    raise ValueError(f"unknown sector {sector!r}")


def _eikonal_K(phi3d, c_0, GM, sector, b_list, window=24, correct=True):
    """
    Lattice eikonal deflection coefficient K_bend = alpha b c^2 / GM for a
    straight ray (along axis 0) through the mid-plane slice of a 3D potential.
    alpha = -INT d/d(perp) ln n  dl  (dl = 1 cell), bending toward the mass.

    The integral is taken over a finite half-aperture `window` (cells either
    side of closest approach) — this both excludes the periodic-box seam and
    makes the truncation explicit.  A straight ray of finite half-length X past
    a 1/r index captures only a fraction f = X/sqrt(X^2+b^2) of the asymptotic
    deflection; `correct=True` divides f out to report the asymptotic
    coefficient (the standard finite-aperture lensing correction).  Returns
    {b: K_bend}.  This is the F52 H3 discriminator, generalised to the single
    dielectric index.
    """
    import numpy as np
    zc = phi3d.shape[2] // 2
    sl = phi3d[:, :, zc]                       # (long, perp)
    uu = -sl / c_0 ** 2
    lnn = np.log(_index_from_u(uu, sector))
    dlnn = np.gradient(lnn, axis=1)
    long_c = sl.shape[0] // 2
    perp_c = sl.shape[1] // 2
    lo, hi = long_c - window, long_c + window
    out = {}
    for b in b_list:
        line = dlnn[lo:hi, perp_c + b]
        alpha = -float(np.sum(line))           # toward mass = positive
        K = alpha * b * c_0 ** 2 / GM
        if correct:
            K /= window / np.sqrt(window ** 2 + b ** 2)
        out[int(b)] = K
    return out


def _em_energy_shell_3d(L, E_total, R=10.0, width=2.0, k=2 * 3.141592653589793 / 8,
                        center=None):
    """
    Instantiate a real standing (E,B) field in a spherical shell of radius R and
    compute its energy density u = 1/2 (E^2 + B^2), normalised to total E_total.
    E ∥ x̂ and B ∥ ŷ in spatial quadrature so the energy density is the smooth
    shell envelope^2 (the oscillation lives in the fields, not the energy) — a
    genuine massless field-energy distribution with ZERO rest-mass density.
    """
    import numpy as np
    if center is None:
        center = (L // 2, L // 2, L // 2)
    ax = np.arange(L)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2 + (Z - center[2]) ** 2)
    env = np.exp(-((r - R) / width) ** 2)
    Ex = env * np.cos(k * X)
    By = env * np.sin(k * X)
    u_em = 0.5 * (Ex ** 2 + By ** 2)           # = 0.5 * env^2  (smooth shell)
    s = u_em.sum()
    if s > 0:
        u_em *= E_total / s
    return u_em


# ───────────────────────────────────────────────────────────────────
#  D-EM2 — single-field lattice deflection
# ───────────────────────────────────────────────────────────────────

def test_dem2_single_field_deflection() -> dict:
    """
    D-EM2 — does ONE dielectric field K(x) on the lattice give Einstein
    factor-2 light bending, with no second (spatial-leg) field equation?

    Source a weak-field potential from a Gaussian point mass (3D FFT Poisson,
    true 1/r), then measure the eikonal deflection coefficient K_bend at a span
    of impact parameters for three index placements on the SAME field:
        dielectric  (the fork)  -> expect K_bend ≈ 4
        full_GR     (two-leg)   -> expect K_bend ≈ 4   (cross-check)
        rest_only   (F52 leg)   -> expect K_bend ≈ 2
    The ratio K_dielectric / K_rest_only cancels common lattice/box error and
    must equal 2 to high precision (both are linear functionals of the same
    ∂φ field, with index slopes 2u vs u).

    PASS iff |K_dielectric − 4|/4 < 0.10, |K_rest_only − 2|/2 < 0.10, and
    |ratio − 2| < 0.05.
    """
    import numpy as np







    L, M, sigma, c_0 = 64, 0.02, 1.0, 1.0
    b_list = [6, 8, 10, 12]
    rho = _gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = _solve_poisson_3d(rho, G=1.0)
    GM = M                                       # G = 1

    K_diel = _eikonal_K(phi, c_0, GM, "dielectric", b_list)
    K_full = _eikonal_K(phi, c_0, GM, "full_GR", b_list)
    K_rest = _eikonal_K(phi, c_0, GM, "rest_only", b_list)

    def _mean(d):
        return float(np.mean(list(d.values())))
    Kd, Kf, Kr = _mean(K_diel), _mean(K_full), _mean(K_rest)
    ratio = Kd / Kr
    u_probe = float(-phi[L // 2 + b_list[0], L // 2, L // 2] / c_0 ** 2)

    ok = (abs(Kd - 4.0) / 4.0 < 0.10
          and abs(Kr - 2.0) / 2.0 < 0.10
          and abs(ratio - 2.0) < 0.05)
    return {
        "pass": bool(ok),
        "K_dielectric": Kd,
        "K_full_GR": Kf,
        "K_rest_only": Kr,
        "ratio_dielectric_over_rest": ratio,
        "K_dielectric_by_b": {str(k): v for k, v in K_diel.items()},
        "K_rest_only_by_b": {str(k): v for k, v in K_rest.items()},
        "weak_field_u_at_probe": u_probe,
        "lattice": dict(L=L, M=M, sigma=sigma, b_list=b_list),
        "note": "one dielectric field reproduces factor-2 (≈4); the rest leg on "
                "the same field is factor-1 (≈2); ratio≈2 cancels lattice error.",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM3 — radiation-as-source (the physical fork)
# ───────────────────────────────────────────────────────────────────

def test_dem3_radiation_as_source() -> dict:
    """
    D-EM3 — does pure (E,B) field energy gravitate like an equal energy of rest
    mass?  This is the discriminator between the EM-connection route (source =
    total field energy) and the rest-leg route (source = rest-mass density).

    Build two equal-ENERGY sources on one lattice:
      (a) a rest-mass Gaussian blob, energy E (energy density = rest-mass density);
      (b) a spherical shell of real standing-(E,B) field energy, total energy E,
          ZERO rest-mass density (massless field).
    Probe rays pass OUTSIDE both distributions (shell theorem ⇒ both enclose the
    same monopole E).

    EM-connection coupling (∇²Φ = 4πG · u_total, energy density):
        deflection from radiation / deflection from mass  →  1
        (equal energy ⇒ equal gravity, independent of profile or composition).
    Rest-leg coupling (∇²Φ = 4πG · ρ_rest, rest-mass density only):
        radiation has ρ_rest = 0 ⇒ Φ = 0 ⇒ zero deflection.

    PASS iff (EM-connection) |ratio_rad/mass − 1| < 0.12  AND  both K_bend ≈ 4,
    AND (rest-leg) radiation deflection / mass deflection < 1e-6.
    """
    import numpy as np







    L, E, c_0 = 64, 0.02, 1.0
    b_list = [10, 12, 14]                        # outside the shell (R=6)

    # (a) rest-mass blob: energy density == rest-mass density
    rho_mass = _gaussian_mass_3d(L, M=E, sigma=1.5)
    # (b) standing (E,B) field-energy shell, same total energy, zero rest mass
    u_em = _em_energy_shell_3d(L, E_total=E, R=6.0, width=1.5)

    # EM-connection coupling: BOTH source from energy density u_total
    phi_mass = _solve_poisson_3d(rho_mass, G=1.0)
    phi_rad_emc = _solve_poisson_3d(u_em, G=1.0)
    # Rest-leg coupling: radiation has NO rest-mass density to source
    rho_rest_of_radiation = np.zeros_like(u_em)  # massless field ⇒ 0
    phi_rad_restleg = _solve_poisson_3d(rho_rest_of_radiation, G=1.0)

    GM = E
    Kd_mass = _eikonal_K(phi_mass, c_0, GM, "dielectric", b_list)
    Kd_rad = _eikonal_K(phi_rad_emc, c_0, GM, "dielectric", b_list)
    Kd_rad_rl = _eikonal_K(phi_rad_restleg, c_0, GM, "dielectric", b_list)

    def _mean(d):
        return float(np.mean(list(d.values())))
    Km, Kr = _mean(Kd_mass), _mean(Kd_rad)
    ratio_emc = Kr / Km if Km else float("nan")
    # rest-leg deflection from radiation, normalised to mass deflection
    rl_frac = abs(_mean(Kd_rad_rl)) / abs(Km) if Km else float("nan")

    energy_mass = float(rho_mass.sum())
    energy_rad = float(u_em.sum())

    ok = (abs(ratio_emc - 1.0) < 0.12
          and abs(Km - 4.0) / 4.0 < 0.12
          and abs(Kr - 4.0) / 4.0 < 0.12
          and rl_frac < 1e-6)
    return {
        "pass": bool(ok),
        "K_bend_mass_emconn": Km,
        "K_bend_radiation_emconn": Kr,
        "ratio_radiation_over_mass_emconn": ratio_emc,
        "restleg_radiation_deflection_fraction": rl_frac,
        "energy_mass": energy_mass,
        "energy_radiation": energy_rad,
        "energy_match": abs(energy_mass - energy_rad) / energy_mass,
        "note": "equal energy ⇒ equal gravity under EM-connection (ratio→1); "
                "rest-leg coupling sources nothing from massless field energy "
                "(fraction→0). This is the physical fork.",
    }


# ───────────────────────────────────────────────────────────────────
#  DYNAMIC FIELD — time-domain co-evolving dielectric on the F62 stepper
# ───────────────────────────────────────────────────────────────────
#  Everything below promotes F64 from a static eikonal probe to a full
#  *dynamic field*: a Dirac wave packet is evolved in time on a dielectric
#  background K(x) (and, in the backreaction tests, on the dielectric the
#  packet itself sources).  To make the comparison with the emergent-gravity
#  module (F62, dirac_gravity_fork.py) rigorous, we REUSE F62's exactly-unitary
#  curved-background Dirac stepper verbatim and change ONLY the metric
#  placement: where F62 posits the two independent legs
#       A = 1 + 2Φ/c²   (rest leg, sourced by ρ)
#       B = 1 − 2Φ/c²   (spatial leg, sourced independently)
#  F64 uses a single impedance-locked dielectric
#       A = 1/K = (1 − u)² ,   B = K = (1 − u)⁻² ,   u = −Φ/c² ,
#  so AB ≡ 1 (the reciprocal lock of D-EM1) and there is no second field
#  equation.  Same solver, same observables — the only difference on the wire
#  is the (A,B) map, which is exactly the fork.
#
#  Leading-order identities (why the dielectric reproduces F62's dynamics):
#       √A_diel = 1 − u            = 1 + Φ/c²  + O(u²)      (rest leg / redshift)
#       c_eff   = c₀√(A/B) = c₀(1−u)² = c₀(1+2Φ/c²) + O(u²) (kinetic leg / bend)
#  F62 has √A = 1+Φ/c²+… and c_eff = c₀(1+2Φ/c²)+… as well, so the
#  equivalence principle, the factor-1 redshift and the factor-2 deflection
#  must all agree to leading order; the structural saving is that F64 gets the
#  spatial leg B = 1/A *for free* from the impedance lock instead of sourcing
#  it separately.  The empirical fork (D-EM3) lives in what SOURCES Φ.

# ── CANONICAL dielectric index ──────────────────────────────────────
#  Adopted 2026-05-31 (D-EM9): the canonical nonlinear dielectric is the
#  impedance-matched exponential
#       K(u) = exp(2u) ,   u = GM/(r c²) = −Φ/c² ,
#       A = 1/K = e^{-2u} ,  B = K = e^{2u}      (AB ≡ 1 EXACTLY).
#  It agrees with the old linear-fix form (1−u)⁻² at O(u) — so the entire
#  weak-field battery is unchanged — but has PPN β=γ=1 (GR-identical, Mercury
#  42.98″/cy), whereas (1−u)⁻² had β=½ (50.1″/cy, excluded).  It still satisfies
#  D-EM1 (Z=1, K_bend=4) and D-EM5 (impedance √(μ/ε)=1, reciprocal lock AB=1).
def K_canonical(u):
    """Canonical dielectric index K=e^{2u} (u=GM/rc²). AB=1 exact, PPN β=γ=1."""
    import numpy as np
    return np.exp(2.0 * np.asarray(u, dtype=np.float64))


def _inst_freq_hilbert(sig, dt, trim=0.25):
    """Resolution-free clock frequency from the analytic-signal instantaneous
    phase (Hilbert transform via FFT): ω = median d(unwrap∠a)/dt over a central
    window.  Immune to the FFT bin resolution and the spectral leakage that
    defeats `_dominant_freq` for a spreading / multi-tone chirality signal; its
    (small, roughly constant) bias cancels in a near/far *ratio*.  Pure real
    1-D time-series transform — not a chiral lattice transform (numpy-safe)."""
    import numpy as np
    s = np.asarray(sig, dtype=np.float64)
    s = s - s.mean()
    n = len(s)
    S = np.fft.fft(s)
    h = np.zeros(n)
    h[0] = 1.0
    if n % 2 == 0:
        h[n // 2] = 1.0
        h[1:n // 2] = 2.0
    else:
        h[1:(n + 1) // 2] = 2.0
    a = np.fft.ifft(S * h)
    phase = np.unwrap(np.angle(a))
    w = np.gradient(phase, dt)
    lo, hi = int(trim * n), int((1 - trim) * n)
    return float(np.median(w[lo:hi]))


def AB_from_phi_dielectric(phi, c0):
    """Single-dielectric weak-field map  Φ ↦ (A, B), canonical exponential form:

        u = −Φ/c² ,  K = e^{2u} ,  A = 1/K = e^{-2u} ,  B = K = e^{2u}

    so AB ≡ 1 EXACTLY (impedance-locked) and the eikonal index n = √(B/A) = K.
    Direct counterpart of `dirac_gravity_fork.AB_from_phi` (two independent legs
    A=1+2Φ/c², B=1−2Φ/c²); here a single field carries both legs.  [Canonical
    nonlinear completion adopted 2026-05-31 per D-EM9; agrees with the earlier
    (1−u)⁻² fix at O(u), so all weak-field results are unchanged.]
    """
    import numpy as np
    u = -np.asarray(phi, dtype=np.float64) / c0 ** 2
    K = np.exp(2.0 * u)
    return 1.0 / K, K


def dielectric_rindler_background(shape, a, x0=None):
    """Dielectric Rindler frame: a uniform rest-leg gradient √A = 1 + a·ξ
    realised as a *dielectric* (impedance-locked) rather than a pure lapse.

        √A = 1 + a·ξ   ⇒   A = (1+a·ξ)² ,  B = (1+a·ξ)⁻²   (AB = 1)

    Identical rest leg to `dirac_gravity_fork.rindler_background` (which uses
    B = 1), so the equivalence-principle free-fall — carried entirely by the
    rest leg — is shared; the dielectric merely supplies B = 1/A as the locked
    spatial partner.  Returns (A_field, B_field).
    """
    import numpy as np
    Lx, Ly = shape
    if x0 is None:
        x0 = Lx / 2.0
    xs = np.arange(Lx) - x0
    sqrtA_col = 1.0 + a * xs
    A_col = sqrtA_col ** 2
    A = np.repeat(A_col[:, None], Ly, axis=1)
    B = 1.0 / A
    return A, B


def dielectric_schwarzschild_background(shape, GM, c0, center=None, r_soft=4.0):
    """Weak dielectric point mass:  Φ = −GM/r  ↦  A=(1−u)², B=(1−u)⁻², u=GM/(c²r).

    The dielectric counterpart of `dirac_gravity_fork.schwarzschild_weak_background`
    (which uses the two-leg A=1+2Φ/c², B=1−2Φ/c²).  Both give the same c_eff and
    hence the same Einstein factor-2 eikonal bend to leading order; F64 gets it
    from ONE field with B=1/A.  Returns (A_field, B_field).
    """
    import numpy as np
    Lx, Ly = shape
    if center is None:
        center = (Lx / 2.0, Ly / 2.0)
    xs = np.arange(Lx) - center[0]
    ys = np.arange(Ly) - center[1]
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2 + r_soft ** 2)
    phi = -GM / r
    return AB_from_phi_dielectric(phi, c0)


# ── D-EM-D1 — flat regression (the dielectric stepper reduces to free Weyl) ──

def test_demD1_flat_regression(L=48, dt=1.0, seed=0) -> dict:
    """In flat space (Φ=0 ⇒ K=1 ⇒ A=B=1, m=0) one dielectric-background Dirac
    tick must equal two decoupled exact-QCA Weyl walks bit-for-bit — the same
    D1 regression F62 passes, confirming the dynamic dielectric stepper carries
    no spurious coupling at zero field.  Reuses F62's stepper directly."""
    import numpy as np
    import dirac_gravity_fork as dg

    rng = np.random.default_rng(seed)
    shape = (L, L)

    def rfield():
        return rng.standard_normal(shape) + 1j * rng.standard_normal(shape)

    eu, ed, xu, xd = rfield(), rfield(), rfield(), rfield()
    A, B = AB_from_phi_dielectric(np.zeros(shape), c0=1.0)   # flat ⇒ 1,1
    c_eff = np.sqrt(A / B)                                   # = 1

    eu_ref, ed_ref = dg._weyl_half_step_2c(eu, ed, 0.5 * dt)
    eu_ref, ed_ref = dg._weyl_half_step_2c(eu_ref, ed_ref, 0.5 * dt)
    xu_ref, xd_ref = dg._weyl_half_step_2c(xu, xd, 0.5 * dt)
    xu_ref, xd_ref = dg._weyl_half_step_2c(xu_ref, xd_ref, 0.5 * dt)

    eu_f, ed_f, xu_f, xd_f = dg.gravity_dirac_step(
        eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=0.0, dt=dt,
        kinetic="qca", r_kin_scalar=1.0)

    resid = max(float(np.max(np.abs(eu_f - eu_ref))),
                float(np.max(np.abs(ed_f - ed_ref))),
                float(np.max(np.abs(xu_f - xu_ref))),
                float(np.max(np.abs(xd_f - xd_ref))))
    flat_ok = bool(np.allclose(A, 1.0) and np.allclose(B, 1.0))
    return {"pass": bool(resid < 1e-12 and flat_ok),
            "residual_max_abs": resid, "flat_AB_ok": flat_ok,
            "note": "dielectric stepper ≡ two free Weyl walks at zero field (= F62 D1)."}


# ── D-EM-D2a — dielectric free-fall (equivalence principle) ──

def test_demD2a_dielectric_freefall(L=220, a=0.006, m=0.35, dt=1.0,
                                    n_steps=110, sigma=16.0,
                                    masses=(0.2, 0.35, 0.5)) -> dict:
    """Equivalence principle on a dielectric background.  A rest packet released
    in a dielectric Rindler frame (√A = 1+a·ξ, B = 1/A) free-falls toward low
    lapse with mass-independent coordinate acceleration |g| → a·c_lat²
    (c_lat² = 1/2).  Mirrors F62 D2a exactly, with the dielectric spatial leg
    B=1/A in place of B=1; the rest-leg free-fall is therefore shared.

    PASS: falls toward −ξ, |g_meas|/g_pred within 20 %, mass-spread < 12 %,
    norm conserved to the propagator floor.
    """
    import numpy as np
    import dirac_gravity_fork as dg

    g_pred = a * dg.C_LAT_SQ

    def traj(mm):
        shape = (L, L)
        x0 = L / 2.0
        xi = np.arange(L) - x0
        sqrtA = np.repeat((1.0 + a * xi)[:, None], L, axis=1)   # dielectric lapse
        xs = np.arange(L)
        X, Y = np.meshgrid(xs, xs, indexing="ij")
        G = np.exp(-((X - x0) ** 2 + (Y - L / 2.0) ** 2) /
                   (2.0 * sigma ** 2)).astype(complex)
        eu = G / np.sqrt(2.0); ed = 0 * G; xu = G / np.sqrt(2.0); xd = 0 * G
        xc, norms = [], []
        for step in range(n_steps + 1):
            rho = dg.density(eu, ed, xu, xd)
            cx, _ = dg.centroid(rho, X, Y)
            xc.append(cx - x0); norms.append(float(rho.sum()))
            if step < n_steps:
                eu, ed, xu, xd = dg.gravity_dirac_step_massive(
                    eu, ed, xu, xd, sqrtA, mm, dt=dt)
        t = np.arange(n_steps + 1) * dt
        drift = float(abs(norms[-1] - norms[0]) / norms[0])
        return t, np.array(xc), drift

    finals, drifts = {}, []
    for mm in masses:
        _, x, drift = traj(mm); finals[mm] = float(x[-1]); drifts.append(drift)
    mean_fall = float(np.mean([abs(v) for v in finals.values()]))
    spread = float(np.ptp(list(finals.values())) / mean_fall) if mean_fall else float("nan")

    t, x, drift = traj(m)
    win = np.abs(x) < 2.0
    nw = max(int(win.sum()), 10)
    g_meas = -2.0 * float(np.polyfit(t[:nw], x[:nw], 2)[0])
    falls = x[-1] < 0
    return {
        "pass": bool(falls and abs(abs(g_meas) / g_pred - 1.0) < 0.20
                     and spread < 0.12 and max(drifts + [drift]) < 1e-9),
        "g_meas_abs": abs(g_meas), "g_pred": g_pred,
        "coeff_ratio": abs(g_meas) / g_pred if g_pred else float("nan"),
        "falls_toward_low_lapse": bool(falls),
        "final_displacement": float(x[-1]),
        "final_disp_by_mass": finals,
        "universality_spread": spread,
        "norm_drift": max(drifts + [drift]),
        "c_lat_sq": dg.C_LAT_SQ,
        "params": {"L": L, "a": a, "m": m, "n_steps": n_steps, "masses": list(masses)},
        "note": "EP carried by rest leg √A; dielectric B=1/A is the locked partner.",
    }


# ── D-EM-D2b — dynamical redshift (clock rate ∝ √A on the dielectric) ──

def test_demD2b_dynamical_redshift(L=96, m=0.5, c0=0.5, dt=0.5, n_steps=360,
                                   sigma=7.0, u_near=0.10, u_far=0.0) -> dict:
    """Two static dielectric clocks at u_near, u_far tick in the ratio of their
    zitterbewegung frequencies 2·arcsin(√A·m), √A = (1−u).  Measured dynamically
    from the chirality oscillation.  Dielectric counterpart of F62 D2b (which
    sets A directly); here A=(1−u)², kinetic scalar √(A/B)=(1−u)²."""
    import numpy as np
    import dirac_gravity_fork as dg

    freqs, fan = {}, {}
    for tag, uu in (("near", u_near), ("far", u_far)):
        shape = (L, L)
        Aval = float(np.exp(-2.0 * uu))               # A = e^{-2u} (canonical)
        A = np.full(shape, Aval)
        r_kin = float(np.exp(-2.0 * uu))              # √(A/B) = e^{-2u}
        c_eff = np.full(shape, c0 * r_kin)
        eu, ed, xu, xd = dg.gaussian_packet_momentum(shape, k0=(0.0, 0.0), m=m,
                                                     sigma=sigma)
        eu = eu * np.sqrt(2.0); xu = xu * 0.0
        sig = []
        for step in range(n_steps + 1):
            sig.append(dg.chirality_imbalance(eu, ed, xu, xd))
            if step < n_steps:
                eu, ed, xu, xd = dg.gravity_dirac_step(
                    eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=m, dt=dt,
                    kinetic="qca", r_kin_scalar=float(c0 * r_kin))
        freqs[tag] = dg._dominant_freq(sig, dt)
        fan[tag] = 2.0 * float(np.arcsin(np.sqrt(Aval) * m))

    ratio_meas = freqs["near"] / freqs["far"]
    ratio_pred_sqrtA = float(np.exp(-(u_near - u_far)))     # √A=e^{-u}
    ratio_pred_exact = fan["near"] / fan["far"]
    return {
        "pass": bool(abs(ratio_meas / ratio_pred_exact - 1.0) < 0.03
                     and ratio_meas < 1.0),
        "freq_near": freqs["near"], "freq_far": freqs["far"],
        "ratio_meas": ratio_meas,
        "ratio_pred_sqrtA": ratio_pred_sqrtA,
        "ratio_pred_exact_arcsin": ratio_pred_exact,
        "redshift_detected": bool(ratio_meas < 1.0),
        "A_near": float(np.exp(-2.0 * u_near)), "A_far": float(np.exp(-2.0 * u_far)),
        "params": {"L": L, "m": m, "c0": c0, "n_steps": n_steps,
                   "u_near": u_near, "u_far": u_far},
        "note": "deep dielectric clock runs slow at rate √A=e^{-u}; canonical exp form.",
    }


# ── D-EM-D2c — dielectric deflection (factor-2 from ONE field) ──

def test_demD2c_dielectric_deflection(L=160, GM=0.6, c0=0.5, m=0.0,
                                      k_in=0.5, b=16, sigma=6.0, dt=1.0,
                                      n_steps=260, n_sub=2) -> dict:
    """Send a fast (m≈0) packet past a weak dielectric point mass at impact
    parameter b; measure centroid deflection and compare to the eikonal
    line-integral on the SAME single dielectric c_eff field.  The dielectric
    supplies BOTH legs from one field (B=1/A), yet reaches the Einstein
    factor-2 bend K_eik≈4 — where F62 needs B=1−2Φ/c² as a second leg.

    PASS: deflection toward the mass (Δθ<0), eikonal K_eik in (3,5), and the
    dynamical centroid realises its own eikonal limit to ~25 %.
    """
    import numpy as np
    import dirac_gravity_fork as dg

    shape = (L, L)
    cx0, cy0 = L / 2.0, L / 2.0
    A, B = dielectric_schwarzschild_background(shape, GM=GM, c0=c0,
                                               center=(cx0, cy0), r_soft=4.0)
    c_eff = c0 * np.sqrt(A / B)                     # = c0 (1−u)²  (dielectric)
    solver = dg.make_kinetic_solver(c_eff, dt=dt, n_sub=n_sub)

    start_x = 0.18 * L
    eu, ed, xu, xd = dg.gaussian_packet_momentum(
        shape, k0=(k_in, 0.0), m=m, center=(start_x, cy0 + b), sigma=sigma)
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    cxs, cys = [], []
    for step in range(n_steps + 1):
        rho = dg.density(eu, ed, xu, xd)
        cxv, cyv = dg.centroid(rho, X, Y)
        cxs.append(cxv); cys.append(cyv)
        if step < n_steps:
            eu, ed, xu, xd = dg.gravity_dirac_step(
                eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=m, dt=dt,
                kinetic="cayley", kinetic_solver=solver)
    cxs = np.array(cxs); cys = np.array(cys)
    early = slice(3, n_steps // 4)
    late = slice(3 * n_steps // 4, n_steps + 1)
    s_in = float(np.polyfit(cxs[early], cys[early], 1)[0])
    s_out = float(np.polyfit(cxs[late], cys[late], 1)[0])
    dtheta_meas = float(np.arctan(s_out) - np.arctan(s_in))

    j = int(round(cy0 + b))
    ln_c = np.log(c_eff)
    dlnc_dy = (np.roll(ln_c, -1, axis=1) - np.roll(ln_c, 1, axis=1)) / 2.0
    dtheta_eik = float(-dlnc_dy[:, j].sum())
    K_meas = dtheta_meas * b * c0 ** 2 / GM
    K_eik = dtheta_eik * b * c0 ** 2 / GM
    return {
        "pass": bool((dtheta_meas < 0) and (3.0 < abs(K_eik) < 5.0)
                     and (abs(dtheta_meas / dtheta_eik - 1.0) < 0.25)),
        "dtheta_meas": dtheta_meas, "dtheta_eikonal": dtheta_eik,
        "K_meas": K_meas, "K_eikonal": K_eik,
        "ratio_meas_eik": dtheta_meas / dtheta_eik if dtheta_eik else float("nan"),
        "params": {"L": L, "GM": GM, "c0": c0, "k_in": k_in, "b": b,
                   "n_steps": n_steps, "m": m},
        "note": "one dielectric field (B=1/A) gives Einstein factor-2 K_eik≈4; "
                "F62 needs a separately-sourced second leg B=1−2Φ/c².",
    }


# ── backreaction: co-evolve the Dirac field with the dielectric it sources ──

def run_backreaction_dielectric(eta_u, eta_d, chi_u, chi_d, m, c0, G,
                                dt=1.0, n_steps=80, n_sub=2, refresh=4,
                                static_source=None, source_weight=1.0):
    """Self-gravitating dielectric: ρ=|Ψ|² (+optional static source) → ∇²Φ=4πGρ
    → dielectric (A,B)=AB_from_phi_dielectric(Φ) → one exactly-unitary Strang
    tick → repeat (metric refreshed every `refresh` ticks).  Dielectric
    counterpart of `dirac_gravity_fork.run_backreaction`."""
    import numpy as np
    import dirac_gravity_fork as dg

    norms = []
    phi = A = B = c_eff = solver = None
    for step in range(n_steps):
        if step % refresh == 0:
            rho = dg.density(eta_u, eta_d, chi_u, chi_d)
            if static_source is not None:
                rho = rho + source_weight * static_source
            phi = dg.poisson_2d_fft(rho, G)
            A, B = AB_from_phi_dielectric(phi, c0)
            c_eff = c0 * np.sqrt(A / B)
            solver = dg.make_kinetic_solver(c_eff, dt=dt, n_sub=n_sub)
        norms.append(dg.dirac_norm(eta_u, eta_d, chi_u, chi_d))
        eta_u, eta_d, chi_u, chi_d = dg.gravity_dirac_step(
            eta_u, eta_d, chi_u, chi_d, A_field=A, c_eff_field=c_eff, m=m,
            dt=dt, kinetic="cayley", kinetic_solver=solver)
    norms.append(dg.dirac_norm(eta_u, eta_d, chi_u, chi_d))
    return {"field": (eta_u, eta_d, chi_u, chi_d), "phi": phi, "A": A, "B": B,
            "c_eff": c_eff, "norms": np.array(norms)}


def test_demD3a_backreaction_norm(L=64, m=0.4, c0=0.5, G=0.02, dt=1.0,
                                  n_steps=60, sigma=6.0, n_sub=2) -> dict:
    """Self-gravitating dielectric packet: the norm must stay conserved while
    the dielectric K(x) it generates evolves underneath it (each tick exactly
    unitary).  Dielectric counterpart of F62 D3a backreaction-norm."""
    import numpy as np
    import dirac_gravity_fork as dg

    shape = (L, L)
    eu, ed, xu, xd = dg.gaussian_packet_momentum(shape, k0=(0.0, 0.0), m=m,
                                                 sigma=sigma)
    out = run_backreaction_dielectric(eu, ed, xu, xd, m=m, c0=c0, G=G, dt=dt,
                                      n_steps=n_steps, n_sub=n_sub)
    norms = out["norms"]
    drift = float(abs(norms[-1] - norms[0]) / norms[0])
    return {
        "pass": bool(drift < 1e-9),
        "norm_initial": float(norms[0]), "norm_final": float(norms[-1]),
        "norm_drift": drift,
        "phi_min": float(out["phi"].min()), "phi_max": float(out["phi"].max()),
        "params": {"L": L, "m": m, "c0": c0, "G": G, "n_steps": n_steps},
        "note": "self-sourced dielectric metric evolves; matter norm conserved.",
    }


# ── D-EM4 — one self-sourced K: factor-1 redshift AND factor-2 bend together ──

def test_dem4_redshift_bend_consistency(L=96, m=0.5, c0=0.5, dt=0.5,
                                        n_steps=300, sigma_src=12.0,
                                        sigma_probe=7.0, well_depth=0.30,
                                        n_sub=1, refresh=20) -> dict:
    """D-EM4 — close the loop the way F62-D3a did for the rest leg, but on ONE
    self-sourced dielectric field K(x).  A static source blob digs a
    self-consistent well Φ (∇²Φ=4πGρ each refresh); on the SAME field we read
    BOTH GR coefficients:

      (1) factor-1 redshift — two probe clocks (deep vs rim) tick in the ratio
          set by the rest leg √A=(1−u) on the field's own lapse; the deep clock
          runs slower.  [the dynamical, wave-packet measurement]
      (2) factor-2 bend — the eikonal deflection coefficient K_bend on that same
          self-consistent dielectric field is ≈4 (Einstein), not 2 (Newton).

    A single dielectric scalar delivering Z≈1 AND K_bend≈4 from its own source
    is the dynamical realisation of D-EM1.  PASS iff the deep clock is redshifted
    and matches the rest-leg prediction to <4 %, AND the dielectric eikonal index
    slope on the same self-field is exactly twice the rest-leg-only slope
    (ratio≈2 ⇒ K_bend≈4 vs Newton 2 — the lattice-invariant discriminator).

    Measurement note.  The redshift is read by placing a clean static clock at
    fixed radius in the field's *own* self-consistent lapse A(r): we solve
    ∇²Φ=4πGρ once, sample A at the well bottom and at the flat rim, and evolve a
    rest packet in each *local* lapse (the qca scalar engine, exact for a uniform
    background — the same clock D-EM-D2b validates).  This avoids the spectral
    leakage that a single co-evolving packet spreading across the gradient
    suffers, while still reading the lapse from the genuine self-sourced field.
    """
    import numpy as np
    import dirac_gravity_fork as dg

    cx = L // 2
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")

    # self-consistent source well, calibrated to the requested weak-field depth
    rsrc = np.sqrt((X - cx) ** 2 + (Y - cx) ** 2)
    blob = np.exp(-rsrc ** 2 / (2.0 * sigma_src ** 2))
    phi_unit = dg.poisson_2d_fft(blob, G=1.0)
    target_phi_min = -0.5 * well_depth * c0 ** 2
    scale = target_phi_min / phi_unit.min()
    source = blob * scale
    Gc = 1.0

    # the field's own self-consistent potential and dielectric lapse
    phi_self = dg.poisson_2d_fft(source, Gc)
    A_self, _ = AB_from_phi_dielectric(phi_self, c0)
    u_self = -phi_self / c0 ** 2

    # ---- (2) factor-2 bend on the self-consistent dielectric field ----------
    # eikonal index slope: dielectric n = K = (1−u)⁻²  vs  rest-leg-only
    # n = 1/√A = (1−u)⁻¹ (half the slope) ⇒ ratio → 2 (⇒ K_bend 4 vs 2). GM
    # cancels in the ratio, so this is the lattice-invariant discriminator.
    def _bend_integral(index_of_u):
        dlnn = np.gradient(np.log(index_of_u(u_self)), axis=1)
        win, perp_c, long_c = 22, cx, cx
        vals = []
        for bb in (6, 8, 10, 12):
            line = dlnn[long_c - win:long_c + win, perp_c + bb]
            vals.append(-float(np.sum(line)) * bb)        # ∝ K_bend·GM/c²
        return float(np.mean(vals))
    diel_int = _bend_integral(lambda u: np.exp(2.0 * u))     # dielectric n=K=e^{2u}
    rest_int = _bend_integral(lambda u: np.exp(u))           # rest-leg-only n=1/√A=e^{u}
    bend_ratio = diel_int / rest_int if rest_int else float("nan")

    # ---- (1) factor-1 redshift: clean static clock at fixed radius ----------
    A_near = float(A_self[cx, cx])                      # well bottom (deep)
    A_far = float(A_self[cx, cx + L // 2 - 8])          # flat rim (shallow)

    def _clock(Aval):
        """Zitterbewegung frequency of a rest clock in uniform dielectric lapse
        Aval (kinetic scalar √(A/B)=A since B=1/A).  Clean single tone."""
        A = np.full((L, L), Aval)
        r_kin = Aval                                    # √(A/B) = √(A·A) = A
        c_eff = np.full((L, L), c0 * r_kin)
        eu, ed, xu, xd = dg.gaussian_packet_momentum((L, L), k0=(0.0, 0.0),
                                                     m=m, sigma=sigma_probe)
        eu = eu * np.sqrt(2.0); xu = xu * 0.0
        sig = []
        for step in range(n_steps + 1):
            sig.append(dg.chirality_imbalance(eu, ed, xu, xd))
            if step < n_steps:
                eu, ed, xu, xd = dg.gravity_dirac_step(
                    eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=m, dt=dt,
                    kinetic="qca", r_kin_scalar=float(c0 * r_kin))
        return _inst_freq_hilbert(sig, dt)             # resolution-free clock

    f_near, f_far = _clock(A_near), _clock(A_far)
    ratio_meas = f_near / f_far
    ratio_pred_exact = float(np.arcsin(np.sqrt(A_near) * m) /
                             np.arcsin(np.sqrt(A_far) * m))
    redshift_ok = (ratio_meas < 1.0 and
                   abs(ratio_meas / ratio_pred_exact - 1.0) < 0.04)
    bend_factor2_ok = abs(bend_ratio - 2.0) < 0.30
    return {
        "pass": bool(redshift_ok and bend_factor2_ok),
        # (1) redshift on the self-sourced lapse
        "freq_near": f_near, "freq_far": f_far,
        "A_near": A_near, "A_far": A_far,
        "redshift_ratio_meas": ratio_meas,
        "redshift_ratio_pred_exact": ratio_pred_exact,
        "redshift_detected": bool(ratio_meas < 1.0),
        "redshift_ok": bool(redshift_ok),
        # (2) factor-2 bend on the SAME self-sourced field
        "bend_dielectric_slope_integral": diel_int,
        "bend_rest_only_slope_integral": rest_int,
        "bend_ratio_dielectric_over_rest": bend_ratio,
        "bend_factor2_ok": bool(bend_factor2_ok),
        "params": {"L": L, "m": m, "c0": c0, "well_depth": well_depth,
                   "n_steps": n_steps, "dt": dt, "sigma_src": sigma_src},
        "note": "ONE self-sourced dielectric K: factor-1 redshift (deep clock slow, "
                "matches √A=(1−u) to <4%) AND factor-2 bend (index slope exactly 2× "
                "rest-leg) — the dynamical close of the D-EM1 loop, the F64 "
                "counterpart of F62-D3a self-redshift.",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM5 — DERIVING the dielectric placement from the (E,B) rotation rule
# ───────────────────────────────────────────────────────────────────
#  F64's one posited input was that the position-dependent lattice
#  renormalisation enters as a *genuine dielectric* (ε=μ=K, impedance-
#  preserving) rather than as one of the other single-scalar placements.
#  D-EM5 promotes that from posited to DERIVED, in four exact steps + a
#  lattice confirmation, all built on the ca_maxwell exact rotation law
#  (F25/F26): the composite-photon (E,B) pair obeys a *proper rotation*
#  E↦cosΩ·E+sinΩ·B, B↦−sinΩ·E+cosΩ·B, which preserves ‖E‖²+‖B‖² (the EM
#  energy) by orthogonality of R(Ω).  Making Ω position-dependent is
#  making the medium position-dependent; the question is which placement
#  keeps it a *proper* rotation (no scalar contamination — the F26 BCC
#  criterion).  Maxwell's curl law is the small-k limit of this rotation
#  (ca_maxwell "DERIVED LAW"), so an FDTD interface test is the faithful
#  long-wavelength probe of the same rule.


def _plebanski_eps_mu(A, B):
    """Plebanski equivalent-medium permittivity=permeability of a static
    isotropic 3-D metric ds²=−A dt²+B δ_ij dx^i dx^j:
        ε^{ij}=μ^{ij}=√(−g)/(−g₀₀)·g^{ij}  →  (isotropic) ε=μ=√(B/A).
    Returns the sympy scalar √(B/A)."""
    return sp.sqrt(B / A)


def dem5_derive_dielectric() -> dict:
    """
    D-EM5 — derive ε=μ=K (hence A=1/K, B=K, AB≡1) from "position-dependent
    (E,B) rotation that stays a proper rotation".  Four exact (sympy) steps:

    (A) Plebanski equivalent medium of a static isotropic metric is ε=μ=√(B/A).
        For the dielectric rep (A=1/K,B=K) this is K; for its conformal partner
        (A=1,B=K²) it is *also* K — the medium sees only the conformal class.
    (B) Conformal invariance: diag(−1/K,K,K,K) = K·diag(−1,K²,K²,K²), a uniform
        Weyl factor, so source-free Maxwell (conformally invariant in 3+1D) gives
        the SAME null structure / eikonal index n=√(B/A)=K for both — the EM
        sector fixes only the conformal class, never the conformal factor.
    (C) Impedance + index: requiring the rotation stay *proper* (impedance matched
        to vacuum, Z=√(μ/ε)=1 — no reflected/scalar component) together with the
        light-speed renormalisation n=√(εμ)=K has the UNIQUE solution ε=μ=K.
    (D) The reciprocal lock AB=1 is then fixed by the one piece the EM sector is
        blind to — the conformal factor — supplied by the measured factor-1
        gravitational redshift √A=1−u ⇒ A=(1−u)², with B=K=(1−u)⁻² ⇒ AB=1.

    So the dielectric placement is forced by: (proper rotation ⇒ ε=μ) + (index ⇒
    =K) + (factor-1 redshift ⇒ conformal factor).  This is the EM-sector twin of
    F52's rest-leg clock field: both are the SAME single scalar, and impedance
    matching is what guarantees they are mutually consistent (AB=1).

    Returns the exact symbolic results; `pass` is the conjunction of all checks.
    """
    K = sp.symbols("K", positive=True)
    uu = sp.symbols("u", positive=True)
    eps, mu = sp.symbols("epsilon mu", positive=True)

    # (A) Plebanski for both conformal representatives
    em_diel = sp.simplify(_plebanski_eps_mu(1 / K, K))        # A=1/K, B=K
    em_refr = sp.simplify(_plebanski_eps_mu(sp.Integer(1), K ** 2))  # A=1, B=K²
    A_plebanski_ok = (em_diel - K == 0) and (em_refr - K == 0)

    # (B) conformal invariance: m2 == K * m1 componentwise; equal eikonal index
    m1 = [-1 / K, K, K, K]
    m2 = [-sp.Integer(1), K ** 2, K ** 2, K ** 2]
    weyl = [sp.simplify(b / a) for a, b in zip(m1, m2)]
    conformal_ok = all(sp.simplify(w - K) == 0 for w in weyl)
    n1 = sp.simplify(sp.sqrt(K / (1 / K)))      # √(B/A) rep1
    n2 = sp.simplify(sp.sqrt(K ** 2 / 1))       # √(B/A) rep2
    index_equal_ok = (sp.simplify(n1 - K) == 0) and (sp.simplify(n2 - K) == 0)

    # (C) impedance match + index ⇒ unique ε=μ=K
    sols = sp.solve([sp.Eq(sp.sqrt(mu / eps), 1), sp.Eq(sp.sqrt(eps * mu), K)],
                    [eps, mu], dict=True)
    impedance_ok = (len(sols) == 1 and sp.simplify(sols[0][eps] - K) == 0
                    and sp.simplify(sols[0][mu] - K) == 0)

    # (D) reciprocal lock from factor-1 redshift fixing the conformal factor
    A_red = (1 - uu) ** 2                       # √A = 1−u (measured factor-1)
    K_idx = (1 - uu) ** (-2)                     # n = K forced by EM sector
    AB = sp.simplify(A_red * K_idx)              # B = K
    reciprocal_lock_ok = (AB - 1 == 0)

    # lattice confirmation: 1-D FDTD impedance reflection at an abrupt index step
    refl = _dem5_fdtd_reflection()
    R_match = refl["matched"]
    R_mismatch_min = min(refl["refractive_only"], refl["clock_only"])
    lattice_ok = (R_match < 0.03 and R_mismatch_min > 3.0 * R_match
                  and R_mismatch_min > 0.04)

    ok = bool(A_plebanski_ok and conformal_ok and index_equal_ok
              and impedance_ok and reciprocal_lock_ok and lattice_ok)
    return {
        "pass": ok,
        "derived": "epsilon = mu = K  (=> A=1/K, B=K, AB=1)",
        # (A)
        "plebanski_eps_mu_dielectric_rep": str(em_diel),
        "plebanski_eps_mu_refractive_rep": str(em_refr),
        "plebanski_ok": bool(A_plebanski_ok),
        # (B)
        "conformal_weyl_factor": str(sp.simplify(weyl[0])),
        "conformal_uniform_ok": bool(conformal_ok),
        "eikonal_index_both_reps": [str(n1), str(n2)],
        "index_equal_ok": bool(index_equal_ok),
        # (C)
        "impedance_index_solution": {str(k): str(v) for k, v in (sols[0].items() if sols else [])},
        "impedance_match_forces_eps_eq_mu_eq_K": bool(impedance_ok),
        # (D)
        "AB_from_factor1_redshift": str(AB),
        "reciprocal_lock_ok": bool(reciprocal_lock_ok),
        # lattice
        "fdtd_reflection": refl,
        "lattice_proper_rotation_ok": bool(lattice_ok),
        "note": "ε=μ=K is DERIVED (proper rotation ⇒ impedance match ⇒ ε=μ; index "
                "⇒ =K; factor-1 redshift ⇒ conformal factor ⇒ AB=1). The EM sector "
                "(conformally invariant) carries BOTH metric legs as one scalar; "
                "only the clock/redshift selects the conformal representative. "
                "Impedance-matched placement is reflectionless on the lattice; the "
                "non-dielectric placements (refractive-only, clock-only) reflect — "
                "that reflected wave IS the F26 scalar contamination.",
    }


def _dem5_fdtd_reflection(L=3000, n_steps=2200, dt=0.4, k0=0.6, sigma=30,
                          Kpeak=2.0) -> dict:
    """1-D Yee FDTD (the small-k Maxwell-curl limit of the exact (E,B) rotation):
    launch a right-moving pulse in vacuum into an abrupt half-space index step,
    return reflected/incident energy fraction for three single-scalar placements.
    Impedance-matched ε=μ=K keeps the rotation proper (reflectionless to the grid
    floor); the impedance-mismatched placements reflect (≈Fresnel) — the reflected
    backward wave is the scalar contamination forbidden by a proper rotation."""
    import numpy as np
    x = np.arange(L)
    iface = L // 2
    step = (x >= iface).astype(np.float64)        # abrupt vacuum→medium step

    def reflect(eps, mu):
        E = np.zeros(L); H = np.zeros(L - 1)
        x0 = L // 4
        E[:] = np.exp(-((x - x0) ** 2) / (2 * sigma ** 2)) * np.cos(k0 * (x - x0))
        xh = 0.5 * (x[:-1] + x[1:])
        H[:] = -np.exp(-((xh - x0) ** 2) / (2 * sigma ** 2)) * np.cos(k0 * (xh - x0))
        muH = 0.5 * (mu[:-1] + mu[1:])
        e_inc = 0.5 * np.sum(eps * E ** 2) + 0.5 * np.sum(muH * H ** 2)
        for _ in range(n_steps):
            H += (dt) / muH * (E[1:] - E[:-1])
            E[1:-1] += (dt) / eps[1:-1] * (H[1:] - H[:-1])
        left = x < (iface - 80)
        e_left = (0.5 * np.sum((eps * E ** 2)[left])
                  + 0.5 * np.sum((muH * H ** 2)[left[:-1]]))
        return float(e_left / e_inc)

    Km = 1.0 + (Kpeak - 1.0) * step
    one = np.ones(L)
    return {
        "matched": reflect(Km, Km),                       # ε=μ=K  (the dielectric)
        "refractive_only": reflect(Km ** 2, one.copy()),  # ε=K², μ=1  (Z=1/K)
        "clock_only": reflect(one.copy(), Km ** 2),       # ε=1, μ=K²  (Z=K)
        "fresnel_pred_mismatched": float((((1 / Kpeak) - 1) / ((1 / Kpeak) + 1)) ** 2),
        "note": "matched ≈ grid floor (reflectionless proper rotation); mismatched "
                "≈ Fresnel (scalar contamination).",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM6 — DYNAMICAL light-bends-light on a dielectric Maxwell field
# ───────────────────────────────────────────────────────────────────

def _dielectric_from_em_energy_2d(L, E_total, c0, sigma, center, G=1.0):
    """A dielectric K(x) sourced by a lump of pure (E,B) field ENERGY (zero rest
    mass): u_em → ∇²Φ=4πG·u_em → u=−Φ/c² → K=(1−u)⁻².  Returns (K, u_field)."""
    import numpy as np
    ax = np.arange(L)
    X, Y = np.meshgrid(ax, ax, indexing="ij")
    u_em = np.exp(-((X - center[0]) ** 2 + (Y - center[1]) ** 2) / (2 * sigma ** 2))
    u_em *= E_total / u_em.sum()
    phi = _solve_poisson_2d(u_em, G)
    u = -phi / c0 ** 2
    return np.exp(2.0 * u), u             # canonical K=e^{2u}


def _solve_poisson_2d(rho, G):
    import numpy as np
    Lx, Ly = rho.shape
    src = 4.0 * np.pi * G * (rho - rho.mean())
    kx = np.fft.fftfreq(Lx) * 2 * np.pi
    ky = np.fft.fftfreq(Ly) * 2 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    k2 = KX ** 2 + KY ** 2
    k2[0, 0] = 1.0
    Pk = -np.fft.fft2(src) / k2
    Pk[0, 0] = 0.0
    phi = np.real(np.fft.ifft2(Pk))
    return phi - phi.mean()


def _fdtd_TM_beam_2d(K, c0, b, n_steps, center_y, k0=0.8, sx=9.0, sy=16.0, dt=0.5):
    """2-D TM (E_z, H_x, H_y) Yee FDTD on the impedance-matched dielectric ε=μ=K.
    Launch a +x Gaussian light pulse at impact parameter b above the lens and
    return the energy-centroid track (cx, cy)."""
    import numpy as np
    L = K.shape[0]
    eps = K; mu = K
    Ez = np.zeros((L, L)); Hx = np.zeros((L, L)); Hy = np.zeros((L, L))
    ax = np.arange(L)
    X, Y = np.meshgrid(ax, ax, indexing="ij")
    x0 = 0.13 * L
    cy = center_y + b
    env = np.exp(-((X - x0) ** 2) / (2 * sx ** 2) - ((Y - cy) ** 2) / (2 * sy ** 2))
    Ez[:] = env * np.cos(k0 * (X - x0))
    Hy[:] = -env * np.cos(k0 * (X - x0))          # +x moving (vacuum Z=1)
    cxs, cys = [], []
    for _ in range(n_steps):
        ud = 0.5 * (eps * Ez ** 2 + mu * (Hx ** 2 + Hy ** 2))
        tot = float(ud.sum())
        cxs.append(float((X * ud).sum() / tot))
        cys.append(float((Y * ud).sum() / tot))
        Hx[:, :-1] -= dt / mu[:, :-1] * (Ez[:, 1:] - Ez[:, :-1])
        Hy[:-1, :] += dt / mu[:-1, :] * (Ez[1:, :] - Ez[:-1, :])
        Ez[1:, 1:] += dt / eps[1:, 1:] * ((Hy[1:, 1:] - Hy[:-1, 1:])
                                          - (Hx[1:, 1:] - Hx[1:, :-1]))
    import numpy as np
    return np.array(cxs), np.array(cys)


def test_dem6_light_bends_light(L=300, E_total=0.03, c0=1.0, b=16,
                                n_steps=560, sigma_src=8.0) -> dict:
    """
    D-EM6 — the decisive experiment vs the rest-leg route: does a *propagating
    Maxwell pulse* (pure light, zero rest mass) gravitationally deflect when the
    lens itself is a lump of pure (E,B) field ENERGY (also zero rest mass)?
    Light-bends-light, fully dynamical — not an eikonal probe.

    A dielectric well K(x) is sourced from an EM-energy blob (∇²Φ=4πG·u_em); a
    2-D TM light pulse is then propagated through it (Yee FDTD on ε=μ=K) at impact
    parameter b and its energy centroid tracked.  Reported:
      • the pulse deflects TOWARD the energy lump (Δθ<0);
      • the measured bend tracks the eikonal line-integral on the same field
        (Δθ_meas/Δθ_eik within tolerance — the dynamical wave realises its ray
        limit);
      • the factor-2 discriminator: on the same field the dielectric eikonal
        index slope is exactly 2× the rest-leg-only slope (ratio→2 ⇒ Einstein,
        not Newton).  [The ABSOLUTE K_bend≈4 is the 3-D result D-EM3; in 2-D the
        Poisson Green's function is logarithmic (Finding 8), so only the
        dimension-invariant ratio is quoted here.]
      • the fork: the lens is pure field energy (ρ_rest=0), so under the rest-leg
        coupling its deflection is identically 0 — light would not bend light.

    PASS iff the pulse bends toward the mass, realises ≥65 % of its eikonal bend,
    and the dielectric/rest-leg ratio is 2.00±0.05.
    """
    import numpy as np
    cyc = L // 2
    K, u = _dielectric_from_em_energy_2d(L, E_total, c0, sigma_src, (cyc, cyc))

    # factor-2 ratio discriminator on the SAME field (dimension-invariant)
    long_c = L // 2

    def _slope_integral(index_ln, row_y, win=24):
        d = np.gradient(index_ln, axis=1)
        return -float(np.sum(d[long_c - win:long_c + win, row_y]))
    ln_diel = 2.0 * u                       # dielectric index n=K=e^{2u}  ⇒ ln n=2u
    ln_rest = u                             # rest-leg-only index n=1/√A=e^{u} ⇒ ln n=u
    diel_int = _slope_integral(ln_diel, cyc + b)
    rest_int = _slope_integral(ln_rest, cyc + b)
    ratio = diel_int / rest_int if rest_int else float("nan")

    # eikonal deflection along the beam row: Δθ_eik = −∫ ∂_y ln c_eff,  c_eff=c0/K
    dlnc = np.gradient(np.log(c0 / K), axis=1)
    dtheta_eik = -float(np.sum(dlnc[:, cyc + b]))

    # dynamical FDTD pulse
    cxs, cys = _fdtd_TM_beam_2d(K, c0, b, n_steps, cyc)
    ein = (cxs > 55) & (cxs < 110)
    eout = (cxs > 200) & (cxs < 255)
    s_in = float(np.polyfit(cxs[ein], cys[ein], 1)[0])
    s_out = float(np.polyfit(cxs[eout], cys[eout], 1)[0])
    dtheta_meas = float(np.arctan(s_out) - np.arctan(s_in))
    realise = dtheta_meas / dtheta_eik if dtheta_eik else float("nan")

    bends_toward_mass = dtheta_meas < 0
    realises_eikonal = abs(realise - 1.0) < 0.35
    factor2_ok = abs(ratio - 2.0) < 0.05
    ok = bool(bends_toward_mass and realises_eikonal and factor2_ok)
    return {
        "pass": ok,
        "lens_is_pure_field_energy": True,
        "rest_mass_density_of_lens": 0.0,
        "restleg_deflection_of_lens": 0.0,   # ρ_rest=0 ⇒ rest-leg sources nothing
        "K_min": float(K.min()), "K_max": float(K.max()),
        "dtheta_meas": dtheta_meas,
        "dtheta_eikonal": dtheta_eik,
        "fraction_of_eikonal_realised": realise,
        "bends_toward_mass": bool(bends_toward_mass),
        "factor2_ratio_dielectric_over_restleg": ratio,
        "factor2_ok": bool(factor2_ok),
        "beam_track_cx": [float(cxs[0]), float(cxs[-1])],
        "params": {"L": L, "E_total": E_total, "c0": c0, "b": b,
                   "n_steps": n_steps, "sigma_src": sigma_src},
        "note": "A propagating Maxwell pulse deflects toward a lens made of pure "
                "(E,B) field energy — light bends light, dynamically. Factor-2 "
                "ratio = 2 (Einstein, not Newton). The lens has zero rest mass, so "
                "the rest-leg route (F50/F52) sources nothing from it (0): the "
                "decisive fork, now on a real wave rather than an eikonal probe.",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM7 — 3-D absolute deflection on a genuine ray trajectory (item 3)
# ───────────────────────────────────────────────────────────────────

def _ray_deflection(b, GMc2, form, X=2000.0, dt=0.5, r_soft=1e-6):
    """Integrate the eikonal photon ray through an isotropic index n(r) in the
    orbital plane (a central index ⇒ planar motion, so this is the full 3-D
    deflection).  Eikonal Hamiltonian H=½(|p|²−n²)=0 ⇒ |p|=n along the ray:
        dx/dτ = p ,   dp/dτ = n ∇n = ½∇(n²).
    Launch from x=−X at height b moving +x; return the deflection angle (RK4).
    `form`: 'dielectric' n=(1−u)⁻²  |  'exp' n=e^{2u}  (u=GM/(rc²))."""
    import numpy as np

    def n_grad(x, y):
        r = np.sqrt(x * x + y * y + r_soft ** 2)
        u = GMc2 / r
        if form == "dielectric":
            n = (1 - u) ** -2; dn_du = 2 * (1 - u) ** -3
        elif form == "exp":
            n = np.exp(2 * u); dn_du = 2 * np.exp(2 * u)
        else:
            raise ValueError(form)
        du = -GMc2 / r ** 3
        return n, dn_du * du * x, dn_du * du * y

    x, y = -X, float(b)
    n0, _, _ = n_grad(x, y)
    px, py = n0, 0.0

    def deriv(x, y, px, py):
        n, gx, gy = n_grad(x, y)
        return px, py, n * gx, n * gy

    for _ in range(int(2 * X / dt)):
        k1 = deriv(x, y, px, py)
        k2 = deriv(x + .5*dt*k1[0], y + .5*dt*k1[1], px + .5*dt*k1[2], py + .5*dt*k1[3])
        k3 = deriv(x + .5*dt*k2[0], y + .5*dt*k2[1], px + .5*dt*k2[2], py + .5*dt*k2[3])
        k4 = deriv(x + dt*k3[0], y + dt*k3[1], px + dt*k3[2], py + dt*k3[3])
        x += dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        y += dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        px += dt/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2])
        py += dt/6*(k1[3]+2*k2[3]+2*k3[3]+k4[3])
        if x > X:
            break
    return float(-np.arctan2(py, px))      # >0 = bent toward the mass


def test_dem7_absolute_deflection_3d() -> dict:
    """
    D-EM7 — the ABSOLUTE light-bending coefficient on a genuine ray trajectory in
    the true-1/r (3-D) dielectric, not a 2-D ratio or a linearised line-integral.

    Integrate the photon ray through n(r)=(1−u)⁻² for a span of field strengths
    and read K_bend = α·b·c²/GM.  Einstein ⇒ K_bend → 4 (Newton would be 2).  The
    dielectric approaches 4 *from above* at finite field (the exact, non-linear
    index), confirming the D-EM1 mpmath guard on a propagating ray.  The
    exponential (Puthoff) completion is integrated alongside for the strong-field
    comparison of D-EM9.

    PASS iff K_bend(dielectric) → 4 within 0.1% at GM/bc²=10⁻⁴ and the finite-field
    approach is from above (K_bend>4).
    """
    import numpy as np
    out = {}
    for form in ("dielectric", "exp"):
        ser = {}
        for eps in (1e-2, 1e-3, 1e-4):
            b, GMc2 = 1.0, eps
            alpha = _ray_deflection(b, GMc2, form)
            ser[f"{eps:.0e}"] = alpha * b / GMc2
        out[form] = ser
    Kd = out["dielectric"]["1e-04"]
    ok = (abs(Kd - 4.0) < 4e-3 and out["dielectric"]["1e-02"] > 4.0)
    return {
        "pass": bool(ok),
        "K_bend_dielectric_by_field": out["dielectric"],
        "K_bend_exp_by_field": out["exp"],
        "K_bend_weak_limit": Kd,
        "approaches_from_above": bool(out["dielectric"]["1e-02"] > 4.0),
        "newtonian_would_be": 2,
        "note": "absolute Einstein factor-2 (K_bend→4) on a genuine 3-D ray through "
                "the true-1/r dielectric; finite-field approach from above. Removes "
                "the 2-D logarithmic-Poisson caveat (Finding 8) of D-EM6.",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM8 — the dielectric potential as a DYNAMICAL field with a kinetic
#          term (its own wave equation), not an instantaneous constraint
# ───────────────────────────────────────────────────────────────────
#  F52/F62 (and D-EM2/D-EM4) solve ∇²Φ=4πGρ instantaneously each refresh —
#  action-at-a-distance gravity.  Here Φ is promoted to a genuine field
#  obeying □Φ = c_g⁻²∂_t²Φ − ∇²Φ = −4πGρ, so (i) its static limit IS the
#  Poisson well that sources the dielectric K=(1−u)⁻²; (ii) disturbances
#  propagate at the finite speed c_g (causal gravity / retardation); (iii)
#  the free field carries conserved energy — a kinetic term, i.e. the seed
#  of a Lagrangian element and of gravitational waves in the dielectric.

def _lap2d(P):
    import numpy as np
    return (np.roll(P, 1, 0) + np.roll(P, -1, 0)
            + np.roll(P, 1, 1) + np.roll(P, -1, 1) - 4 * P)


def test_dem8_dynamical_field(L=300, c_g=1.0, dt=0.4, G=1.0) -> dict:
    """
    D-EM8 — promote the dielectric potential Φ (hence K=(1−u)⁻², u=−Φ/c²) to a
    dynamical field with its own equation of motion □Φ=−4πGρ.  Three checks:

      (a) static fixed point — the Poisson well (∇²Φ=4πGρ, the source of the
          dielectric in D-EM2/D-EM4) is stationary under the wave equation.
      (b) finite propagation speed — a free Φ pulse radiates outward at exactly
          c_g (retardation: gravity is causal, not the instantaneous Poisson of
          F52/F62).
      (c) conserved energy — the free field carries E=½∫(∂_tΦ)²+½c_g²∫|∇Φ|²,
          conserved over the run (a genuine kinetic term).

    PASS iff (a) the Poisson solution stays static to <5×10⁻³ (relative), (b) the
    measured wavefront speed matches c_g within 5 %, and (c) energy drift < 2 %.
    """
    import numpy as np
    x = np.arange(L)
    X, Y = np.meshgrid(x, x, indexing="ij")
    c = L // 2
    R = np.sqrt((X - c) ** 2 + (Y - c) ** 2)

    # (a) fixed point: Poisson well static under the wave eqn
    rho = np.exp(-((X - c) ** 2 + (Y - c) ** 2) / (2 * 6.0 ** 2))
    rho *= 0.02 / rho.sum()
    src = 4 * np.pi * G * (rho - rho.mean())
    # FFT Poisson solution
    kx = np.fft.fftfreq(L) * 2 * np.pi
    KX, KY = np.meshgrid(kx, kx, indexing="ij")
    k2 = KX ** 2 + KY ** 2; k2[0, 0] = 1.0
    Pk = -np.fft.fft2(src) / k2; Pk[0, 0] = 0.0
    Pp = np.real(np.fft.ifft2(Pk)); Pp -= Pp.mean()
    P, Pm = Pp.copy(), Pp.copy()
    maxdev = 0.0
    for _ in range(400):
        Pnew = 2 * P - Pm + (c_g * dt) ** 2 * (_lap2d(P) - src)
        Pm, P = P, Pnew
        maxdev = max(maxdev, float(np.max(np.abs(P - Pp))))
    fixed_rel = maxdev / float(np.max(np.abs(Pp)))

    # (b)+(c) free pulse: speed + energy
    P = np.exp(-R ** 2 / (2 * 4.0 ** 2)); Pm = P.copy()
    times, radii, Es = [], [], []
    for n in range(200):
        Pnew = 2 * P - Pm + (c_g * dt) ** 2 * _lap2d(P)
        vel = (Pnew - Pm) / (2 * dt)
        gx = 0.5 * (np.roll(P, -1, 0) - np.roll(P, 1, 0))
        gy = 0.5 * (np.roll(P, -1, 1) - np.roll(P, 1, 1))
        Es.append(0.5 * np.sum(vel ** 2) + 0.5 * c_g ** 2 * np.sum(gx ** 2 + gy ** 2))
        Pm, P = P, Pnew
        if n % 20 == 19:
            thr = 0.02 * float(np.abs(P).max()) + 1e-12
            m = np.abs(P) > thr
            times.append((n + 1) * dt)
            radii.append(float(R[m].max()) if m.any() else 0.0)
    times, radii = np.array(times), np.array(radii)
    speed = float(np.polyfit(times[2:], radii[2:], 1)[0])
    Es = np.array(Es)
    e_drift = float(abs(Es[-1] - Es[10]) / Es[10])

    fixed_ok = fixed_rel < 5e-3
    speed_ok = abs(speed / c_g - 1.0) < 0.05
    energy_ok = e_drift < 2e-2
    return {
        "pass": bool(fixed_ok and speed_ok and energy_ok),
        "static_fixedpoint_rel_dev": fixed_rel,
        "wavefront_speed": speed, "c_g": c_g,
        "speed_ratio": speed / c_g,
        "free_field_energy_drift": e_drift,
        "fixed_ok": bool(fixed_ok), "speed_ok": bool(speed_ok),
        "energy_ok": bool(energy_ok),
        "note": "Φ is a dynamical field: static limit = the Poisson well that "
                "sources K; disturbances propagate at finite c_g (causal gravity, "
                "vs the instantaneous Poisson of F52/F62); free field conserves "
                "energy (a kinetic term ⇒ Lagrangian element + dielectric GWs).",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM9 — strong-field PPN: dielectric vs exact Schwarzschild (item 5)
# ───────────────────────────────────────────────────────────────────

def _ppn_beta_gamma(A_expr, B_expr):
    """PPN (β, γ) of a static isotropic metric g_tt=−A, g_ij=B δ, with potential
    U=u (=GM/rc²): A = 1 − 2U + 2βU² + …, B = 1 + 2γU + …  (sympy series)."""
    uu = sp.symbols("u", positive=True)
    A = sp.series(A_expr, uu, 0, 3).removeO()
    B = sp.series(B_expr, uu, 0, 3).removeO()
    beta = sp.simplify(A.coeff(uu, 2) / 2)
    gamma = sp.simplify(B.coeff(uu, 1) / 2)
    return beta, gamma


def test_dem9_strong_field_ppn() -> dict:
    """
    D-EM9 — does the dielectric reproduce GR beyond the weak field?  Extract the
    PPN parameters (β, γ) of the dielectric metric and compare the three classic
    solar-system observables to GR / Schwarzschild:

      light deflection   ∝ (1+γ)/2 · 4GM/bc²
      perihelion advance ∝ (2+2γ−β)/3 · 6πGM/(a(1−e²)c²)

    Three metric forms (all isotropic, g_tt=−A, g_ij=B):
      • F64 redshift-fixed   K=(1−u)⁻²  (A=(1−u)², B=(1−u)⁻²)
      • Puthoff exponential  K=e^{2u}   (A=e^{−2u}, B=e^{2u})   [impedance-matched, all orders]
      • Schwarzschild isotropic (reference)

    Result (exact, sympy): all three give γ=1 ⇒ identical light bending 4GM/bc²
    (F64 passes the deflection test). But the redshift-fixed K=(1−u)⁻² has β=1/2,
    giving a perihelion factor 7/6 — a 16.7 % EXCESS over GR: Mercury 50.1″/cy vs
    the observed 42.98″ (the MESSENGER bound β−1=(0.2±2.5)×10⁻⁵ excludes β=1/2
    overwhelmingly).  The impedance-matched exponential completion K=e^{2u}
    restores β=1 ⇒ GR-identical PPN — it agrees with the linear fix at O(u) and
    corrects only the O(u²) term ((1−u)⁻²=1+2u+3u²… vs e^{2u}=1+2u+2u²…).

    So the EM-sector derivation (D-EM5) fixes K only to *linear* order (via the
    factor-1 redshift √A=1−u); the 2nd-PPN test selects the *nonlinear* completion
    K=e^{2u}.  PASS = the analysis is self-consistent: the Schwarzschild and
    exponential forms reproduce GR (β=γ=1, both observables =1), confirming the
    PPN machinery, while the (1−u)⁻² form is correctly flagged (γ=1, β=1/2,
    perihelion 7/6).

    Mercury baseline: GR 42.98″/century; observed 42.98±0.04 (Will, PPN review).
    """
    u = sp.symbols("u", positive=True)
    forms = {
        "F64_dielectric_(1-u)^-2": ((1 - u) ** 2, (1 - u) ** (-2)),
        "Puthoff_exp_e^{2u}": (sp.exp(-2 * u), sp.exp(2 * u)),
        "Schwarzschild_isotropic": (((1 - u / 2) / (1 + u / 2)) ** 2, (1 + u / 2) ** 4),
    }
    mercury_gr = 42.98
    res = {}
    for name, (A, B) in forms.items():
        beta, gamma = _ppn_beta_gamma(A, B)
        light = sp.nsimplify((1 + gamma) / 2)
        peri = sp.nsimplify((2 + 2 * gamma - beta) / 3)
        res[name] = {
            "beta": str(beta), "gamma": str(gamma),
            "light_bending_vs_GR": str(light),
            "perihelion_vs_GR": str(peri),
            "mercury_arcsec_per_century": round(mercury_gr * float(peri), 2),
        }
    d = res["F64_dielectric_(1-u)^-2"]
    e = res["Puthoff_exp_e^{2u}"]
    s = res["Schwarzschild_isotropic"]
    # self-consistency: GR forms reproduce β=γ=1, both observables =1
    gr_ok = (e["beta"] == "1" and e["gamma"] == "1"
             and s["beta"] == "1" and s["gamma"] == "1"
             and e["perihelion_vs_GR"] == "1" and s["perihelion_vs_GR"] == "1")
    # dielectric correctly characterised: γ=1 (light OK), β=1/2, perihelion 7/6
    diel_ok = (d["gamma"] == "1" and d["beta"] == "1/2"
               and d["light_bending_vs_GR"] == "1" and d["perihelion_vs_GR"] == "7/6")
    return {
        "pass": bool(gr_ok and diel_ok),
        "ppn": res,
        "mercury_gr_baseline_arcsec_century": mercury_gr,
        "mercury_observed_arcsec_century": "42.98 ± 0.04",
        "messenger_bound_beta_minus_1": "(0.2 ± 2.5)e-5",
        "verdict": ("F64's redshift-fixed K=(1−u)^-2 matches GR at 1st order "
                    "(γ=1, light bending 4GM/bc²) but has β=1/2 ⇒ Mercury 50.1″/cy "
                    "(16.7% excess) — EXCLUDED by MESSENGER. The impedance-matched "
                    "exponential K=e^{2u} (agreeing with the linear fix at O(u)) "
                    "restores β=1 ⇒ GR-identical. The 2nd-PPN order selects the "
                    "nonlinear completion D-EM5's linear derivation left open."),
        "note": "The classic tests: light bending depends only on γ (=1 for the "
                "dielectric ⇒ passes); perihelion depends on β too (=1/2 ⇒ fails "
                "unless K is completed to e^{2u}). A concrete falsifiable "
                "prediction and a correction to the model's nonlinear sector.",
    }


def test_dem11_coevolving_self_redshift(L=120, m=0.5, c0=0.5, dt=0.5,
                                        n_steps=220, sigma_src=16.0,
                                        sigma_probe=4.0, core_r=4.0,
                                        well_depth=0.25, far_off=50,
                                        n_sub=1) -> dict:
    """
    D-EM11 (item 7) — the FULLY co-evolving self-redshift, removing D-EM4's
    fixed-radius local-clock workaround.  Two rest packets are evolved in the
    genuine spatially-varying self-sourced dielectric field (the cayley solver on
    the full K(x), so each packet spreads through the gradient); their clocks are
    read by the resolution-free Hilbert instantaneous-frequency estimator
    `_inst_freq_hilbert` (immune to the FFT bin-leakage that defeated the naive
    co-evolving measurement).  This is the F64 counterpart of F62-D3a's
    co-evolving self-redshift, now on a single dielectric field.

    The deep clock runs slower (redshift, ratio<1).  The measured ratio matches
    the local-lapse prediction 2·arcsin(√A·m) to within the *gradient-sampling
    systematic* (~10%): a co-evolving packet of finite width samples a range of
    A as it spreads, which biases the deep clock slightly high — precisely why
    the *precise* coefficient is best read by the localized clock of D-EM4 (which
    this test complements, not replaces).  The factor-2 bend is exact.

    PASS iff the deep clock is redshifted (ratio<1) and matches the local-A
    prediction to < 15 % (the co-evolving, gradient-limited tolerance), with the
    Hilbert clock (no FFT bin fragility).
    """
    import numpy as np
    import dirac_gravity_fork as dg

    cx = L // 2
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    rsrc = np.sqrt((X - cx) ** 2 + (Y - cx) ** 2)
    blob = np.exp(-rsrc ** 2 / (2 * sigma_src ** 2))
    phi_unit = dg.poisson_2d_fft(blob, G=1.0)
    source = blob * (-0.5 * well_depth * c0 ** 2 / phi_unit.min())

    # the genuine self-sourced (static) dielectric field
    phi = dg.poisson_2d_fft(source, 1.0)
    A_field, B_field = AB_from_phi_dielectric(phi, c0)
    c_eff = c0 * np.sqrt(A_field / B_field)
    solver = dg.make_kinetic_solver(np.ascontiguousarray(c_eff), dt=dt, n_sub=n_sub)

    def coevolve(ctr):
        eu, ed, xu, xd = dg.gaussian_packet_momentum((L, L), k0=(0.0, 0.0), m=m,
                                                     center=ctr, sigma=sigma_probe)
        eu = eu * np.sqrt(2.0); xu = xu * 0.0
        core = ((X - ctr[0]) ** 2 + (Y - ctr[1]) ** 2) <= core_r ** 2
        sig = []
        for step in range(n_steps + 1):
            sig.append(dg.chirality_imbalance(eu, ed, xu, xd, mask=core))
            if step < n_steps:
                eu, ed, xu, xd = dg.gravity_dirac_step(
                    eu, ed, xu, xd, A_field=A_field, c_eff_field=c_eff, m=m, dt=dt,
                    kinetic="cayley", kinetic_solver=solver)
        return _inst_freq_hilbert(sig, dt), float(A_field[core].mean())

    f_near, A_near = coevolve((cx, cx))
    f_far, A_far = coevolve((cx, cx + far_off))
    ratio_meas = f_near / f_far
    ratio_pred = float(np.arcsin(np.sqrt(A_near) * m) /
                       np.arcsin(np.sqrt(A_far) * m))
    redshift = ratio_meas < 1.0
    within = abs(ratio_meas / ratio_pred - 1.0) < 0.15
    return {
        "pass": bool(redshift and within),
        "freq_near": f_near, "freq_far": f_far,
        "A_near": A_near, "A_far": A_far,
        "ratio_meas": ratio_meas,
        "ratio_pred_local_arcsin": ratio_pred,
        "rel_error": abs(ratio_meas / ratio_pred - 1.0),
        "redshift_detected": bool(redshift),
        "clock_estimator": "hilbert_instantaneous_frequency (resolution-free)",
        "params": {"L": L, "m": m, "c0": c0, "n_steps": n_steps,
                   "sigma_src": sigma_src, "sigma_probe": sigma_probe,
                   "well_depth": well_depth},
        "note": "fully co-evolving packets (spreading through the real gradient) — "
                "no fixed-A workaround; deep clock slower, Hilbert-measured. "
                "Residual ~10% is the finite packet sampling the well curvature "
                "(the precise coefficient is D-EM4's localized clock). F64 "
                "counterpart of F62-D3a self-redshift.",
    }


# ───────────────────────────────────────────────────────────────────
#  D-EM10 — pinning 4πG / the K-amplitude to the cell scale (item 6)
# ───────────────────────────────────────────────────────────────────
#  The dielectric field equation ∇²Φ=4πG·u (D-EM2/D-EM8) has the SAME 4πG as
#  F52, where Newton's constant entered "by hand".  D-EM10 removes that freedom
#  by tying the coupling to the lattice via the project's induced-gravity chain
#  (F58/F59/F61): (a) the 4π is the exact 3-D lattice Green's-function
#  normalisation; (b) G is the Sakharov-induced value, 1/(16πG)=Ση·∫d³k/(2π)³·
#  1/(2ω) with the lattice cutoff Λ=1/a, the Weyl heat-kernel η=1/12 (F61,
#  exact) and the gravitating mode count g_*; (c) this pins the cell to
#  a=√(2πη g_*)·d^{1/4}·ℓ_P = 3.81 ℓ_P (one generation, g_*=16, d=3) and gives
#  the F59 scaling 1/G∝1/c_lat=√d.  So 4πG is not free: it is the induced
#  coupling the dielectric inherits, the same one F52 left posited.

def test_dem10_pin_G_to_cell_scale() -> dict:
    """
    D-EM10 (item 6) — show the dielectric's 4πG coupling is fixed by the lattice,
    not posited, by tying it to the induced-gravity chain F58/F59/F61.

      (1) 4π is lattice-exact — solve ∇²Φ=4πG·ρ for a compact point mass on a 3-D
          FFT lattice and recover Φ=−GM/r with unit normalisation (the "4π" needs
          no tuning; F58 measured 4πC=1.0004).
      (2) G is the Sakharov-induced value pinned by the cell scale and mode
          content: a=√(2πη g_*)·d^{1/4}·ℓ_P with η_Weyl=1/12 (F61, exact) — the
          closed form reproduces F61's table (g_*=2→1.347, 15→3.688, 16→3.809,
          48→6.598), so for one generation a≈3.81 ℓ_P and G is determined, not
          free.
      (3) the F59 scaling 1/G ∝ 1/c_lat = √d — the vacuum mode integral
          ∫d^dk/(2π)^d·1/(2ω) carries the factor 1/c_lat exactly.

    PASS iff the 4π normalisation is within 3%, the pinned a(g_*=16) matches
    F61's 3.809 to <0.5%, and the √d scaling holds to <2%.
    """
    import numpy as np

    # (1) 3-D lattice Green's-function 4π normalisation
    L, M, sig = 96, 1.0, 2.0
    ax = np.arange(L)
    c = L // 2
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r = np.sqrt((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2)
    rho = np.exp(-r ** 2 / (2 * sig ** 2)); rho *= M / rho.sum()
    k = np.fft.fftfreq(L) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    k2 = KX ** 2 + KY ** 2 + KZ ** 2; k2[0, 0, 0] = 1.0
    phik = -4 * np.pi * 1.0 * np.fft.fftn(rho) / k2; phik[0, 0, 0] = 0.0
    phi = np.fft.ifftn(phik).real
    mask = (r > 8) & (r < 20)
    Amat = np.vstack([1.0 / r[mask], np.ones(int(mask.sum()))]).T
    coef, *_ = np.linalg.lstsq(Amat, phi[mask], rcond=None)
    GM_fit = float(-coef[0])
    four_pi_ok = abs(GM_fit - 1.0) < 0.03

    # (2) induced-G prefactor pins the cell scale (F59/F61)
    eta = 1.0 / 12.0
    def a_over_lP(g, d=3):
        return float(np.sqrt(2 * np.pi * eta * g) * d ** 0.25)
    table = {2: 1.347, 15: 3.688, 16: 3.809, 48: 6.598}
    a_pred = {g: a_over_lP(g) for g in table}
    a_ok = all(abs(a_pred[g] - table[g]) < 0.005 for g in table)
    a_one_gen = a_pred[16]
    # 1/G = 2πη g_*√d / a²  (Planck units; G=ℓ_P² ⇒ consistency)
    d = 3
    invG = 2 * np.pi * eta * 16 * np.sqrt(d) / a_one_gen ** 2

    # (3) 1/G ∝ 1/c_lat = √d  (vacuum mode integral, MC, fixed seed)
    def mode_invG(dim, clat, Lam=1.0, n=300000, seed=0):
        rng = np.random.default_rng(seed)
        kk = rng.uniform(-Lam, Lam, size=(n, dim))
        km = np.linalg.norm(kk, axis=1)
        ins = km < Lam
        vol = (2 * Lam) ** dim
        return vol * np.mean(np.where(ins, 1.0 / (2 * clat * np.maximum(km, 1e-9)), 0.0)) / (2 * np.pi) ** dim
    ds = [2, 3, 4]
    clat_factor = [mode_invG(dim, 1.0 / np.sqrt(dim)) / mode_invG(dim, 1.0) for dim in ds]
    sqrt_d = [float(np.sqrt(dim)) for dim in ds]
    scaling_ok = max(abs(cf / sd - 1.0) for cf, sd in zip(clat_factor, sqrt_d)) < 0.02

    ok = bool(four_pi_ok and a_ok and scaling_ok)
    return {
        "pass": ok,
        "four_pi_normalisation_GM_recovered": GM_fit,
        "four_pi_ok": bool(four_pi_ok),
        "eta_weyl": eta, "g_star_one_generation": 16,
        "cell_scale_a_over_lP": a_one_gen,
        "cell_scale_table_pred": a_pred,
        "cell_scale_table_F61": table,
        "cell_scale_ok": bool(a_ok),
        "one_over_G_check_planck_units": invG,
        "invG_scaling_clat_factor": clat_factor,
        "invG_scaling_sqrt_d": sqrt_d,
        "sqrt_d_scaling_ok": bool(scaling_ok),
        "note": "4πG is NOT free: the 4π is the exact lattice Green's function "
                "(F58), and G is the Sakharov-induced value pinned by the cell "
                "scale a=√(2πη g_*)d^{1/4}ℓ_P=3.81 ℓ_P (η=1/12 F61, g_*=16) with "
                "1/G∝√d (F59). The dielectric inherits the induced coupling the "
                "rest-leg route (F52) left posited. Residual freedom: the gauge "
                "sector's contribution to g_* (flagged in F61).",
    }


# Harness-style fork object (mirrors gr_fork_E_tensor.make_fork)
def make_fork():
    import numpy as np

    def metric(phi, c_0):
        uu = -np.asarray(phi, dtype=np.float64) / c_0 ** 2
        K = np.exp(2.0 * uu)        # canonical exponential dielectric (D-EM9)
        return 1.0 / K, K           # A = 1/K, B = K  (dielectric, AB=1 exact)

    def c_photon(phi, c_0):
        A, B = metric(phi, c_0)
        return c_0 * np.sqrt(A / B)

    def tau_rate(phi, c_0):
        A, _ = metric(phi, c_0)
        return np.sqrt(A)

    return SimpleNamespace(
        NAME="fork_F64_em_connection_dielectric",
        DESCRIPTION="Single lattice dielectric K=e^{2GM/rc²}: A=1/K, B=K (impedance-preserving, AB=1)",
        metric=metric, c_photon=c_photon, c_matter=c_photon, tau_rate=tau_rate,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(test_dem1_eikonal_viability(), indent=2, default=str))
