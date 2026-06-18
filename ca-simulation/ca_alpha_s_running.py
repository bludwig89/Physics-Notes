"""
ca_alpha_s_running.py — Route A of the QCD calibration block:
alpha_s predicted from the rule, by dimensional transmutation.

(2026-06-12)  See docs/theory/qcd-calibration-derivation-routes.md (Route A)
and the finding F144.

The chain
---------
STEP 1 (the lock, exact — this module derives it, not assumes it):
    (a) The rule's F26 update is an EXACT circular rotation R(Omega(k)) on the
        real pair (E,B), per Fourier mode (kernel check, machine precision).
    (b) LEMMA (sympy-exact): the one-tick flow of a quadratic rotor
        H = (a/2)E^2 + (b/2)B^2 is an orthogonal (circular) map iff a == b.
        So the rule's circular rotation FORCES equal electric/magnetic
        stiffness: chi = 1 in the rotor normalisation (F101 S7, now derived).
    (c) F110 C7 matrix identity (re-verified here): the 1-plaquette dual U(1)
        link Hamiltonian IS the compact rotor with chi = 1/(4 g_s^2)
        (a single open plaquette has 4 exclusive boundary links:
        (g^2/2)*4*m^2 = (1/(2chi))*m^2).
    (a)+(b)+(c)  ==>  g_s^2 = 1/4,  g_s = 1/2  at the lattice (bare) scale,
                      alpha_s(mu0) = g_s^2/(4 pi) = 1/(16 pi)   [zero knobs]

STEP 2 (the scale): the bare coupling lives at the lattice cutoff
    mu0 = hbar c / a = E_Planck / 6.59782 = 1.8504e18 GeV   (F107 canonical a).
    Convention band: the cutoff convention spans mu0 = 1/a ... pi/a (the same
    BZ-edge ambiguity F124 carries); 1/a is the standard scheme-bare choice.

STEP 3 (dimensional transmutation): run alpha_s down with the MS-bar beta
    function (1..4 loops; QCD running is Higgs-independent, so the model's
    Higgs-free structure does not modify it at these orders), flavour
    thresholds at m_t, m_b, m_c.  PREDICT alpha_s(M_Z), Lambda_MS^(3,5), and
    the hadron/Planck hierarchy N — with NO free parameter.

STEP 4 (the honest coefficient): the model statement "g_s = 1/2 in the rule
    normalisation" is not yet a continuum-scheme statement.  The required
    scheme conversion is parametrised, as in lattice PT, by a single constant
    d1:   1/alpha_MS(mu0) = 1/alpha_rule(mu0) + d1/(2 pi) * (2 pi) ... here we
    report the IMPLIED shift  Delta(1/alpha) = 1/alpha_needed(mu0) - 16 pi
    obtained by running the measured alpha_s(M_Z) UP, and the equivalent
    multiplicative Lambda-ratio exp(Delta/(2 b0)).  For the Wilson action the
    known one-loop constant is huge (Lambda_MS/Lambda_lat = 28.81, i.e.
    Delta(1/alpha) ~ 2*5.88); the rule's implied conversion is O(0.1-1) —
    i.e. the rule normalisation is already nearly continuum-like.  Computing
    the model-action d1 from first principles is the one open coefficient.

Numerics: numpy only (RK4 in ln mu); sympy for the exact lemma.
"""

from __future__ import annotations

import math

import numpy as np

# ----------------------------------------------------------------------
#  Constants (PDG 2024 / CODATA / FLAG; targets, not inputs to the chain)
# ----------------------------------------------------------------------
E_PLANCK_GEV   = 1.220890e19        # CODATA Planck energy, GeV
A_OVER_LP      = 6.59782            # F79/F107 canonical cell
MU0_GEV        = E_PLANCK_GEV / A_OVER_LP    # hbar c / a = 1.8504e18 GeV
M_Z            = 91.1880            # GeV
M_T_POLE       = 172.57             # GeV (PDG 2024 pole-ish average)
M_B            = 4.18               # GeV (mb(mb))
M_C            = 1.27               # GeV (mc(mc))
ALPHA_S_MZ_PDG = 0.1180             # PDG world average (+- 0.0009)
LAMBDA3_FLAG   = 0.343              # GeV, FLAG Lambda_MS^(nf=3) (+- 0.012)
N_F119         = 5.5e-19            # F119 hierarchy number m_lat(tau)

ALPHA_S_UV     = 0.25 / (4.0 * math.pi)      # = 1/(16 pi), from the lock


# ======================================================================
#  STEP 1a — the rule's step is an exact circular rotation on (E, B)
# ======================================================================
def rule_step_rotation_residual(L: int = 8, seed: int = 0) -> dict:
    """
    Extract the per-mode 2x2 map of ca_wmu._f26_rotation_step by acting on the
    basis states (E,B)=(1,0) and (0,1), and measure (i) orthogonality
    R^T R = 1, (ii) det R = 1, (iii) equal diagonal (circularity).
    All three must vanish to machine precision.
    """
    import ca_wmu as wmu

    ks = 2.0 * math.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing="ij")
    one = np.ones_like(KX); zero = np.zeros_like(KX)

    E1, B1 = wmu._f26_rotation_step(one.copy(),  zero.copy(), KX, KY, KZ)
    E2, B2 = wmu._f26_rotation_step(zero.copy(), one.copy(),  KX, KY, KZ)
    # per-mode map R = [[E1, E2], [B1, B2]]
    orth1 = np.max(np.abs(E1 * E1 + B1 * B1 - 1.0))      # |col1|^2 = 1
    orth2 = np.max(np.abs(E2 * E2 + B2 * B2 - 1.0))      # |col2|^2 = 1
    orth12 = np.max(np.abs(E1 * E2 + B1 * B2))           # col1 . col2 = 0
    det = np.max(np.abs(E1 * B2 - E2 * B1 - 1.0))        # det = 1
    circ = np.max(np.abs(E1 - B2))                        # equal diagonal
    return {"orth_col1": float(orth1), "orth_col2": float(orth2),
            "orth_cross": float(orth12), "det_minus_1": float(det),
            "diag_equal": float(circ),
            "max_residual": float(max(orth1, orth2, orth12, det, circ))}


# ======================================================================
#  STEP 1b — LEMMA: circular flow  <=>  equal stiffness (sympy-exact)
# ======================================================================
def circular_iff_equal_stiffness() -> dict:
    """
    H = (a/2) E^2 + (b/2) B^2,  Hamiltonian flow  dE/dt = b B, dB/dt = -a E.
    One-tick map M(t) = exp(t [[0, b], [-a, 0]]).  Exactly:

        M = [[cos(w t),        (b/w) sin(w t)],
             [-(a/w) sin(w t),  cos(w t)     ]],     w = sqrt(a b).

    M is orthogonal (a pure circular rotation) iff (b/w) = (w/a) = 1, i.e.
    a = b.  Verified symbolically; returns the exact off-orthogonality
    factor M^T M - I ~ diag(...) whose vanishing forces a = b.
    """
    import sympy as sp

    a, b, t = sp.symbols("a b t", positive=True)
    w = sp.sqrt(a * b)
    M = sp.Matrix([[sp.cos(w * t), (b / w) * sp.sin(w * t)],
                   [-(a / w) * sp.sin(w * t), sp.cos(w * t)]])
    # check M is the flow map: dM/dt = [[0,b],[-a,0]] M, M(0)=1
    Gen = sp.Matrix([[0, b], [-a, 0]])
    flow_resid = sp.simplify(M.diff(t) - Gen * M)
    # orthogonality defect
    D = sp.simplify(M.T * M - sp.eye(2))
    # D = sin^2(wt) * diag(a/b - 1, b/a - 1)  (up to simplification):
    d00 = sp.simplify(D[0, 0] / sp.sin(w * t) ** 2)
    d11 = sp.simplify(D[1, 1] / sp.sin(w * t) ** 2)
    # exact statements
    flow_ok = flow_resid == sp.zeros(2, 2)
    offdiag_ok = sp.simplify(D[0, 1]) == 0 and sp.simplify(D[1, 0]) == 0
    d00_is = sp.simplify(d00 - (a / b - 1)) == 0
    d11_is = sp.simplify(d11 - (b / a - 1)) == 0
    # a/b - 1 = 0 and b/a - 1 = 0  <=>  a = b  (and then M in SO(2))
    circular_at_equal = sp.simplify(D.subs(b, a)) == sp.zeros(2, 2)
    return {"flow_map_exact": bool(flow_ok),
            "offdiag_zero": bool(offdiag_ok),
            "defect_00_equals_a_over_b_minus_1": bool(d00_is),
            "defect_11_equals_b_over_a_minus_1": bool(d11_is),
            "orthogonal_iff_a_eq_b": bool(circular_at_equal and d00_is and d11_is),
            "conclusion": "rule's circular rotation forces chi_E = chi_B = 1"}


# ======================================================================
#  STEP 1c — F110 C7 matrix identity: chi = 1/(4 g_s^2)  (re-verified)
# ======================================================================
def chi_lock_identity(m_max: int = 12, lam: float = 1.0) -> dict:
    """
    The 1-plaquette dual U(1) link Hamiltonian (4 exclusive boundary links,
    electric term (g^2/2) sum_l E_l^2) IS the F101 compact rotor with
    chi = 1/(4 g^2) — as a matrix identity.  At the rule's chi = 1 this
    forces g_s^2 = 1/4.  Checked at several g^2 (identity holds for all).
    """
    import ca_link_hamiltonian as lh

    out = {}
    geom = lh.PlaquetteGrid(1, 1)
    for g2 in (0.25, 0.5, 1.0):
        Hd, _ = lh.build_dual_hamiltonian(geom, None, g2=g2, lam=lam,
                                          group="U1", m_max=m_max)
        Hr = lh.rotor_hamiltonian(lam, chi=1.0 / (4.0 * g2), m_max=m_max)
        out[f"matrix_resid_g2={g2}"] = float(np.max(np.abs(Hd.toarray() - Hr)))
    out["g_s2_at_chi_1"] = 0.25
    out["g_s"] = 0.5
    out["alpha_s_uv"] = ALPHA_S_UV
    out["max_resid"] = max(v for k, v in out.items() if k.startswith("matrix"))
    return out


# ======================================================================
#  STEP 3 — MS-bar running, 1..4 loops, flavour thresholds
# ======================================================================
def _beta_coeffs(nf: int) -> tuple:
    """MS-bar beta coefficients, convention  da/dlnmu^2 = -a^2 sum_i b_i a^i
    with a = alpha_s/(4 pi):  b0..b3 (4-loop, van Ritbergen-Vermaseren-Larin)."""
    z3 = 1.2020569031595943
    b0 = 11.0 - 2.0 * nf / 3.0
    b1 = 102.0 - 38.0 * nf / 3.0
    b2 = 2857.0 / 2.0 - 5033.0 * nf / 18.0 + 325.0 * nf ** 2 / 54.0
    b3 = (149753.0 / 6.0 + 3564.0 * z3
          - (1078361.0 / 162.0 + 6508.0 * z3 / 27.0) * nf
          + (50065.0 / 162.0 + 6472.0 * z3 / 81.0) * nf ** 2
          + 1093.0 * nf ** 3 / 729.0)
    return b0, b1, b2, b3


def _beta(a: float, nf: int, loops: int) -> float:
    """da/dln(mu) = 2 * da/dln(mu^2) = -2 a^2 (b0 + b1 a + ...)."""
    b = _beta_coeffs(nf)
    s = 0.0
    for i in range(loops):
        s += b[i] * a ** i
    return -2.0 * a * a * s


def run_alpha(alpha_hi: float, mu_hi: float, mu_lo: float, nf: int,
              loops: int, n_steps: int = 4000) -> float:
    """RK4 integration of a(ln mu) downward (or upward) at fixed nf."""
    a = alpha_hi / (4.0 * math.pi)
    t0, t1 = math.log(mu_hi), math.log(mu_lo)
    h = (t1 - t0) / n_steps
    for _ in range(n_steps):
        k1 = _beta(a, nf, loops)
        k2 = _beta(a + 0.5 * h * k1, nf, loops)
        k3 = _beta(a + 0.5 * h * k2, nf, loops)
        k4 = _beta(a + h * k3, nf, loops)
        a += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if a <= 0 or a > 1.0:      # Landau-pole guard
            return float("nan")
    return a * 4.0 * math.pi


def alpha_s_chain(alpha_uv: float, mu0: float, loops: int) -> dict:
    """mu0 -> m_t -> M_Z (and on to m_b, m_c); continuous matching at
    thresholds (loop-order matching discontinuities are << the scheme band
    and are absorbed in the A4 diagnostic)."""
    a_mt = run_alpha(alpha_uv, mu0, M_T_POLE, nf=6, loops=loops)
    a_mz = run_alpha(a_mt, M_T_POLE, M_Z, nf=5, loops=loops)
    a_mb = run_alpha(a_mz, M_Z, M_B, nf=5, loops=loops)
    a_mc = run_alpha(a_mb, M_B, M_C, nf=4, loops=loops)
    return {"alpha_mt": a_mt, "alpha_MZ": a_mz,
            "alpha_mb": a_mb, "alpha_mc": a_mc}


def lambda_msbar_2loop(alpha: float, mu: float, nf: int) -> float:
    """2-loop closed-form Lambda (the standard convention):
    Lambda = mu * (b0 a)^(-b1/(2 b0^2)) * exp(-1/(2 b0 a)),  a = alpha/4pi."""
    b0, b1, _, _ = _beta_coeffs(nf)
    a = alpha / (4.0 * math.pi)
    return mu * (b0 * a) ** (-b1 / (2.0 * b0 ** 2)) * math.exp(-1.0 / (2.0 * b0 * a))


# ======================================================================
#  STEP 4 — the implied scheme-conversion constant (diagnostic)
# ======================================================================
def implied_scheme_shift(loops: int, mu0: float = MU0_GEV) -> dict:
    """
    Run the MEASURED alpha_s(M_Z) UP to mu0 at this loop order and report
    Delta(1/alpha) = 1/alpha_measured(mu0) - 16 pi  — the shift a scheme
    conversion of the rule coupling must supply.  Express also as the
    equivalent multiplicative Lambda factor exp(Delta/(2 b0_bar)) with
    b0_bar in the alpha convention at nf=6 (b0/(4 pi) per ln mu^2 ...);
    for reference, the Wilson-action constant is Lambda_MS/Lambda_lat=28.81.
    """
    a_mt = run_alpha(ALPHA_S_MZ_PDG, M_Z, M_T_POLE, nf=5, loops=loops)
    a_mu0 = run_alpha(a_mt, M_T_POLE, mu0, nf=6, loops=loops)
    delta_inv = 1.0 / a_mu0 - 1.0 / ALPHA_S_UV
    # 1-loop alpha-convention: 1/alpha = (b0/(2pi)) * 2 ln(mu/Lambda)
    b0 = _beta_coeffs(6)[0]                 # 4pi-convention
    b0_alpha = b0 / (4.0 * math.pi)         # d(1/alpha)/dln mu^2
    lam_factor = math.exp(delta_inv / (2.0 * b0_alpha))
    return {"alpha_measured_at_mu0": a_mu0,
            "one_over_alpha_measured": 1.0 / a_mu0,
            "one_over_alpha_rule": 1.0 / ALPHA_S_UV,
            "delta_inv_alpha": delta_inv,
            "equiv_Lambda_ratio": lam_factor,
            "wilson_reference_Lambda_ratio": 28.809}


# ======================================================================
#  The full Route-A report
# ======================================================================
def route_a_report() -> dict:
    rep = {"mu0_GeV": MU0_GEV, "alpha_s_uv": ALPHA_S_UV,
           "one_over_alpha_uv": 1.0 / ALPHA_S_UV}
    for loops in (1, 2, 3, 4):
        ch = alpha_s_chain(ALPHA_S_UV, MU0_GEV, loops)
        lam5 = lambda_msbar_2loop(ch["alpha_MZ"], M_Z, nf=5)
        lam3 = lambda_msbar_2loop(ch["alpha_mc"], M_C, nf=3)
        dev = 100.0 * (ch["alpha_MZ"] / ALPHA_S_MZ_PDG - 1.0)
        rep[f"{loops}loop"] = {
            "alpha_s_MZ": ch["alpha_MZ"], "dev_vs_PDG_%": dev,
            "Lambda5_GeV": lam5, "Lambda3_GeV": lam3,
            "Lambda3_dev_vs_FLAG_%": 100.0 * (lam3 / LAMBDA3_FLAG - 1.0),
            "hierarchy_N": lam3 / MU0_GEV,
            "scheme_diag": implied_scheme_shift(loops),
        }
    # cutoff-convention band: mu0' = pi/a  (the F124 axis-edge convention)
    ch_pi = alpha_s_chain(ALPHA_S_UV, math.pi * MU0_GEV, 1)
    rep["band_mu0_pi_over_a_1loop_alpha_MZ"] = ch_pi["alpha_MZ"]
    return rep


if __name__ == "__main__":
    import json
    print(json.dumps(route_a_report(), indent=2))
