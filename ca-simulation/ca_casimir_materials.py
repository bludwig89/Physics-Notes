"""
ca_casimir_materials.py  —  realistic Casimir curve vs. sphere-plate data
=========================================================================

Companion to ca_casimir.py / F207.  The model reproduces the IDEAL perfect-
conductor law EXACTLY (F207-C2):  plate-plate P_0 = π²ħc/240 a⁴, and via the
proximity-force approximation (PFA) the sphere-plate force

    F_sp,ideal(a) = 2πR · E_pp(a) = -π³ ħ c R /(360 a³)     (sphere radius R).

Real sphere-plate experiments (Lamoreaux 1997, Mohideen & Roy 1998, Decca
et al. 2007) use gold-coated surfaces at T≈300 K, so the measured force is the
ideal curve reduced by a finite-conductivity + thermal factor η(a).  Those are
standard QED matter-physics on the SAME F69-photon H_int — NOT model
foundations — and are computed here with the Lifshitz formula (plasma model,
gold ω_p = 9.0 eV) to map the ideal curve onto the measured one.

The model-specific deviation from the ideal law is the F207 lattice term
~ β(a_cell/a)², which is ~10⁻⁴⁰ over the experimental range — far below the
experiments' ~0.2–5 % error.  So the model passes the precision sphere-plate
gate exactly as standard QED does, with its own signature unobservable.

Units: SI.  No chiral transforms here (pure dispersion/reflection algebra).
"""

import numpy as np

HBAR = 1.054571817e-34
C = 2.99792458e8
KB = 1.380649e-23
EV = 1.602176634e-19
A_CELL = 1.06638e-34          # F107 BCC cell spacing (m)

WP_GOLD = 9.0 * EV / HBAR     # gold plasma frequency (rad/s), ħω_p = 9.0 eV
LAMBDA_P_GOLD = 2 * np.pi * C / WP_GOLD   # ≈ 138 nm


# ── ideal laws (the model's exact prediction, F207) ──────────────────
def pressure_ideal(a):
    """Ideal plate-plate Casimir pressure (Pa), magnitude."""
    return np.pi ** 2 * HBAR * C / (240.0 * a ** 4)


def sphere_plate_force_ideal(a, R):
    """Ideal sphere-plate Casimir force (N), magnitude, via PFA."""
    return np.pi ** 3 * HBAR * C * R / (360.0 * a ** 3)


# ── Lifshitz reduction factor (plasma model, optional finite T) ──────
def _lifshitz_pressure(a, wp, T=0.0, nz=1600, nx=1800, zmax=45.0, xpad=60.0,
                       nmax=2000):
    """Lifshitz plate-plate pressure (Pa) for identical plasma-model metals.
    T=0 → frequency integral; T>0 → Matsubara sum.  (ζ,x) substitution
    ζ=2aξ/c, x=ζp keeps the domain bounded by e^{-x}."""
    Wp = 2 * a * wp / C

    def mode_integral(zeta):
        # ∫_{zeta}^∞ x² Σ_ν 1/(r_ν^{-2} e^x − 1) dx   at fixed ζ=2aξ/c
        x = np.linspace(max(zeta, 1e-6), zeta + xpad, nx)
        if zeta < 1e-12:
            r2TM = np.ones_like(x); r2TE = np.ones_like(x)   # plasma n=0 limit
        else:
            p = x / zeta
            eps = 1.0 + (Wp / zeta) ** 2
            s = np.sqrt(Wp ** 2 + x ** 2) / zeta
            epsp = eps * p
            r2TM = ((epsp - s) / (epsp + s)) ** 2
            r2TE = ((p - s) / (p + s)) ** 2
        ex = np.exp(x)
        term = (1.0 / (ex / r2TM - 1.0) + 1.0 / (ex / r2TE - 1.0)) * x ** 2
        return np.trapezoid(term, x)

    pref = (C / (2 * a)) ** 4
    if T <= 0.0:
        z = np.linspace(1e-4, zmax, nz)
        inner = np.array([mode_integral(zz) for zz in z])
        # T=0: P=(ħ/2π²c³)(c/2a)^4 ∫_0^∞ dζ ∫_ζ^∞ x²[..]dx
        val = np.trapezoid(inner, z)
        return (HBAR / (2 * np.pi ** 2 * C ** 3)) * pref * val
    # finite T (Matsubara): P=(kT/πc³)(c/2a)³ Σ_n' ∫_{ζ_n}^∞ x²[..]dx
    xi1 = 2 * np.pi * KB * T / HBAR
    s = 0.0
    for n in range(0, nmax + 1):
        zeta_n = 2 * a * (n * xi1) / C
        if zeta_n > zmax + xpad:
            break
        w = 0.5 if n == 0 else 1.0
        s += w * mode_integral(zeta_n)
    return (KB * T / (np.pi * C ** 3)) * (C / (2 * a)) ** 3 * s


def reduction_factor(a, wp=WP_GOLD, T=0.0):
    """η(a) = P_realistic / P_ideal  (≤1)."""
    return _lifshitz_pressure(a, wp, T) / pressure_ideal(a)


def sphere_plate_force_realistic(a, R, wp=WP_GOLD, T=0.0):
    """Measured-equivalent sphere-plate force (N): ideal × η(a) (PFA)."""
    return sphere_plate_force_ideal(a, R) * reduction_factor(a, wp, T)


# ── the model's own lattice deviation from the ideal law (F207-C3) ───
def lattice_fractional_deviation(a, beta=6.6e-3):
    """|ΔF/F| ~ β (a_cell/a)²  — the F207 O((a/L)²) signature (worst-case
    off-axis β; zero for cubic-axis plates).  a in metres."""
    return beta * (A_CELL / a) ** 2
