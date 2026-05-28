"""
F46 — Spherical Pythagorean identity for lattice mass:
    cos Ω_Dirac(k, m) = cos Ω_rest(m) · cos Ω_kin(k)
================================================================
2026-05-28

Hypothesis (linking F26 photon-rotation-rate and F27 chiral-SU(2) mass)
-----------------------------------------------------------------------
For the exact-QCA Dirac propagator D_k = [[n W_k, im I],[im I, n W_k†]]
with n = √(1−m²) (Paper 1 Eq. 23) — i.e. the F27 mass step composed with
the F25/F26 Weyl kinetic step — the per-tick eigen-frequency Ω_Dirac
satisfies the **spherical Pythagorean identity**

    cos Ω_Dirac(k, m) = cos Ω_rest(m) · cos Ω_kin(k)

where:
    Ω_rest(m)   = arcsin(m)            ← F27 "rest rotation rate"
                                          (= zitterbewegung / 2)
    Ω_kin(k)    = arccos(c_x c_y)   in 2D
                = arccos(u^±(k))    on BCC (Paper 1 Eq. 15)

This is the spherical law of cosines for a right spherical triangle with
hypotenuse Ω_Dirac and legs Ω_rest, Ω_kin.

In the small-quantity limit cos x ≈ 1 − x²/2, multiplying the right-hand
side gives  Ω² ≈ m² + Ω_kin² + O(4) — i.e. Einstein's

    E² = p² c² + m² c⁴

with c = c_lat = dΩ_kin/d|k||_{k→0}  (= 1/√2 in 2D, 1/√3 on BCC).
The continuum dispersion is the **continuum limit of an exact discrete
spherical-trigonometric identity** on the lattice.

Tests (all targets machine ε)
-----------------------------
  P1  Closed-form algebraic identity  (2D, random k & m)
  P2  Identity from explicit 4×4 D_k eigenvalues (2D)
  P3  Identity from time-evolved eigenstates via dirac_step_2d_splitstep
  P4  BCC extension: 4×4 BCC-Dirac block, eigenvalue identity (3D, both ±)
  P5  Photon limit m=0:   Ω_Dirac(k,0) = Ω_kin(k)  (2D and BCC)
  P6  Rest limit  k=0:    Ω_Dirac(0,m) = arcsin(m) = Ω_rest(m)
  P7  Continuum Pythagorean residual:  |Ω² − m² − Ω_kin²|  small with k,m
  P8  F26 cross-link:  dΩ/d|k||_{k→0, m=0} = c_lat exactly;
                       dΩ/d|k||_{k→0, m>0} = 0 (massive at rest)

Run:
    cd ca-simulation && python ../model-tests/test_F46_pythagorean_mass.py

Writes test-results/F46_pythagorean_mass.json.
"""

from __future__ import annotations

import os, sys, json, time
import numpy as np

# Make ca-simulation importable.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
_SIM  = os.path.join(_ROOT, 'ca-simulation')
sys.path.insert(0, _SIM)

import ca_dirac as cd
import ca_bcc   as cb
import ca_core_exact as ce


# ──────────────────────────────────────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────────────────────────────────────

def omega_rest(m: float) -> float:
    """Ω_rest(m) = arcsin(m) — the F27 mass-step rest rotation rate."""
    return float(np.arcsin(m))


def omega_kin_2d(kx: float, ky: float) -> float:
    """Ω_kin in 2D: massless Weyl QCA dispersion = arccos(c_x c_y)."""
    cxcy = np.cos(kx / np.sqrt(2.0)) * np.cos(ky / np.sqrt(2.0))
    return float(np.arccos(np.clip(cxcy, -1.0, 1.0)))


def omega_kin_bcc(kx: float, ky: float, kz: float, sign: str = '+') -> float:
    """Ω_kin on BCC: arccos(u^±(k)) where u^± = c_x c_y c_z ± s_x s_y s_z."""
    return float(cb.bcc_dispersion(kx, ky, kz, sign=sign))


def omega_dirac_2d_closed(kx: float, ky: float, m: float) -> float:
    """Closed form: arccos(√(1−m²) · c_x c_y) — from ca_dirac._dirac_dispersion."""
    return float(cd._dirac_dispersion(np.array(kx), np.array(ky), m))


def build_dirac_bcc_4x4(kx: float, ky: float, kz: float, m: float,
                        sign: str = '+') -> np.ndarray:
    """
    BCC-extension of the F27 Dirac block:

        D^BCC_k = [[ n U^±(k),   im·I₂   ],
                   [ im·I₂,     n U^±(k)† ]]    with n = √(1−m²).

    Same construction as ca_dirac._dirac_4x4_at_k but with the 2×2 Weyl
    block replaced by the 2×2 BCC unitary from ca_bcc.bcc_unitary.

    Returns a 4×4 complex matrix.  Verified unitary by the same algebra
    as in ca_dirac (UU† = I, n² + m² = 1).
    """
    n   = float(np.sqrt(max(0.0, 1.0 - m * m)))
    U_ff, U_fg, U_gf, U_gg = cb.bcc_unitary(
        np.array(kx), np.array(ky), np.array(kz), sign=sign)
    # Hermitian conjugate of the 2×2 [[a,b],[c,d]] is [[ā,c̄],[b̄,d̄]].
    Up_ff = np.conj(U_ff); Up_fg = np.conj(U_gf)
    Up_gf = np.conj(U_fg); Up_gg = np.conj(U_gg)
    im = 1j * m
    D = np.array([
        [n*U_ff,  n*U_fg,  im,       0.0     ],
        [n*U_gf,  n*U_gg,  0.0,      im      ],
        [im,      0.0,     n*Up_ff,  n*Up_fg ],
        [0.0,     im,      n*Up_gf,  n*Up_gg ],
    ], dtype=complex)
    return D


def positive_omega_from_unitary(M: np.ndarray) -> float:
    """
    Given a unitary M whose eigenvalues come in pairs (e^{−iω}, e^{+iω}),
    return the largest |ω| ∈ [0, π] (= Ω_full for that mode).  Robust to
    eigenvalue degeneracy.
    """
    evals = np.linalg.eigvals(M)
    angles = np.abs(np.angle(evals))      # |arg(λ)| ∈ [0, π]
    # Avoid trivial ω≈0 modes that could appear from numerical noise; take max.
    return float(np.max(angles))


# ──────────────────────────────────────────────────────────────────────────────
# P1 — closed-form algebraic identity (2D)
# ──────────────────────────────────────────────────────────────────────────────

def test_P1_closed_form_2d(n_samples: int = 200, rng_seed: int = 0) -> dict:
    """
    For random (k, m), verify cos Ω_Dirac = cos Ω_rest · cos Ω_kin
    from the closed-form expressions only.  This is the structural identity.
    """
    rng = np.random.default_rng(rng_seed)
    # k_i ∈ (−π/√2, π/√2) is the natural 2D Brillouin zone since c_i=cos(k_i/√2).
    k_max = 0.9 * np.pi / np.sqrt(2.0)
    residuals = []
    for _ in range(n_samples):
        kx, ky = rng.uniform(-k_max, k_max, 2)
        m      = rng.uniform(-0.95, 0.95)
        cO_D   = np.cos(omega_dirac_2d_closed(kx, ky, m))
        cO_r   = np.cos(omega_rest(m))               # = √(1−m²)
        cO_k   = np.cos(omega_kin_2d(kx, ky))        # = c_x c_y
        residuals.append(abs(cO_D - cO_r * cO_k))
    return {
        'name':        'P1_closed_form_2d',
        'n_samples':   n_samples,
        'max_residual': float(np.max(residuals)),
        'mean_residual': float(np.mean(residuals)),
        'target':      1e-15,
        'passed':      bool(np.max(residuals) <= 1e-15),
    }


# ──────────────────────────────────────────────────────────────────────────────
# P2 — explicit 4×4 D_k eigenvalues (2D)
# ──────────────────────────────────────────────────────────────────────────────

def test_P2_eigenvalues_2d(n_samples: int = 80, rng_seed: int = 1) -> dict:
    """
    Build the explicit 4×4 D_k from ca_dirac._dirac_4x4_at_k, extract Ω from
    the eigenvalues, and verify cos Ω = √(1−m²)·c_x c_y to machine precision.
    """
    rng = np.random.default_rng(rng_seed)
    k_max = 0.9 * np.pi / np.sqrt(2.0)
    residuals = []
    for _ in range(n_samples):
        kx, ky = rng.uniform(-k_max, k_max, 2)
        m      = rng.uniform(-0.95, 0.95)
        D      = cd._dirac_4x4_at_k(kx, ky, m)
        Om_eig = positive_omega_from_unitary(D)
        cO_pred = np.sqrt(1.0 - m*m) * np.cos(kx/np.sqrt(2.0)) * np.cos(ky/np.sqrt(2.0))
        # Compare cosines (single-valued) rather than Ω directly.
        residuals.append(abs(np.cos(Om_eig) - cO_pred))
    return {
        'name':        'P2_eigenvalues_2d',
        'n_samples':   n_samples,
        'max_residual': float(np.max(residuals)),
        'mean_residual': float(np.mean(residuals)),
        'target':      1e-14,
        'passed':      bool(np.max(residuals) <= 1e-14),
    }


# ──────────────────────────────────────────────────────────────────────────────
# P3 — time-evolution identity (2D)
# ──────────────────────────────────────────────────────────────────────────────

def test_P3_time_evolution_2d(L: int = 32, n_steps: int = 25,
                              m_values=(0.0, 0.1, 0.3, 0.5, 0.7, 0.9),
                              k_modes=((1,0),(0,1),(1,1),(2,1),(3,2),(1,4))
                              ) -> dict:
    """
    For each (k_mode, m), build the +ω D_k eigenstate, propagate n_steps with
    dirac_step_2d_splitstep, and verify the identity directly:

        ⟨ψ_0 | ψ_N⟩ · e^{+iN·Ω_pred}  ≃ 1

    where Ω_pred = arccos(√(1−m²)·c_x c_y).  If the identity holds and the
    QCA reproduces D_k bit-for-bit, the result is e^{i·N·(Ω_pred − Ω_num)}
    whose phase is the residual — and stays inside (−π, π) regardless of N.
    """
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    rows = []
    max_res = 0.0
    for m in m_values:
        for ix, iy in k_modes:
            kx = 2.0 * np.pi * ix / L
            ky = 2.0 * np.pi * iy / L
            psi = cd._dirac_plus_eigenvector(kx, ky, m)
            phase = np.exp(1j*(kx*X + ky*Y))
            eu = psi[0]*phase;  ed = psi[1]*phase
            cu = psi[2]*phase;  cd_ = psi[3]*phase
            eu0, ed0, cu0, cd0 = (a.copy() for a in (eu, ed, cu, cd_))
            for _ in range(n_steps):
                eu, ed, cu, cd_ = cd.dirac_step_2d_splitstep(
                    eu, ed, cu, cd_, m=m, dt=1.0)
            ip0 = np.sum(np.conj(eu0)*eu0 + np.conj(ed0)*ed0
                       + np.conj(cu0)*cu0 + np.conj(cd0)*cd0)
            ip  = np.sum(np.conj(eu0)*eu  + np.conj(ed0)*ed
                       + np.conj(cu0)*cu  + np.conj(cd0)*cd_) / ip0
            # Predicted Ω from the spherical Pythagorean identity:
            Om_pred = float(np.arccos(np.clip(
                np.sqrt(1.0 - m*m) *
                np.cos(kx/np.sqrt(2.0)) * np.cos(ky/np.sqrt(2.0)),
                -1.0, 1.0)))
            # If identity holds, ip · e^{+iN·Ω_pred} = 1 (the +ω eigenvector
            # gives ip = e^{−iN·Ω_num} ≃ e^{−iN·Ω_pred}; the residual phase
            # is small and does NOT wrap).
            test_phase = ip * np.exp(1j * n_steps * Om_pred)
            phase_residual = float(abs(np.angle(test_phase)) / n_steps)
            # Translate to a Ω-residual: Ω_num − Ω_pred = −(arg test_phase)/N
            dOm = -float(np.angle(test_phase)) / n_steps
            Om_num = Om_pred + dOm
            res = phase_residual
            max_res = max(max_res, res)
            rows.append({
                'm': m, 'kx': float(kx), 'ky': float(ky),
                'omega_numeric':   Om_num,
                'omega_predicted': Om_pred,
                'residual':        res,
            })
    return {
        'name':        'P3_time_evolution_2d',
        'n_modes':     len(rows),
        'max_residual': max_res,
        'target':      1e-12,
        'passed':      bool(max_res <= 1e-12),
        'sample_rows':  rows[:6],
    }


# ──────────────────────────────────────────────────────────────────────────────
# P4 — BCC extension (3D, both helicity branches)
# ──────────────────────────────────────────────────────────────────────────────

def test_P4_bcc_extension(n_samples: int = 80, rng_seed: int = 2) -> dict:
    """
    Build the BCC-Dirac 4×4 D^BCC_k from build_dirac_bcc_4x4 and verify
    cos Ω_BCCDirac = √(1−m²) · u^±(k)  for random (k, m) and both signs.
    """
    rng = np.random.default_rng(rng_seed)
    # k_i ∈ (−π√3/2, π√3/2) is the natural BCC BZ.
    k_max = 0.55 * np.sqrt(3.0)   # well inside BZ
    residuals = []
    rows = []
    for sign in ('+', '-'):
        for _ in range(n_samples):
            kx, ky, kz = rng.uniform(-k_max, k_max, 3)
            m          = rng.uniform(-0.95, 0.95)
            D    = build_dirac_bcc_4x4(kx, ky, kz, m, sign=sign)
            Om   = positive_omega_from_unitary(D)
            # Predicted: cos Ω = √(1−m²) · u^±(k)
            u, *_ = cb._bcc_uvec(np.array(kx), np.array(ky), np.array(kz), sign=sign)
            cO_pred = np.sqrt(1.0 - m*m) * float(u)
            res = abs(np.cos(Om) - cO_pred)
            residuals.append(res)
            if len(rows) < 6:
                rows.append({
                    'sign': sign, 'kx': float(kx), 'ky': float(ky), 'kz': float(kz),
                    'm': float(m),
                    'cos_omega_eig': float(np.cos(Om)),
                    'cos_omega_pred': cO_pred,
                    'residual': res,
                })
    return {
        'name':         'P4_bcc_extension',
        'n_samples':    2 * n_samples,
        'max_residual': float(np.max(residuals)),
        'mean_residual':float(np.mean(residuals)),
        'target':       1e-14,
        'passed':       bool(np.max(residuals) <= 1e-14),
        'sample_rows':  rows,
    }


# ──────────────────────────────────────────────────────────────────────────────
# P5 — photon limit (m = 0)
# ──────────────────────────────────────────────────────────────────────────────

def test_P5_photon_limit(n_samples: int = 60, rng_seed: int = 3) -> dict:
    """
    At m=0: cos Ω_rest = 1, so the identity reduces to cos Ω_Dirac = cos Ω_kin.
    Verify exactly in 2D and BCC.
    """
    rng = np.random.default_rng(rng_seed)
    residuals_2d  = []
    residuals_bcc = []

    k_max_2d  = 0.9 * np.pi / np.sqrt(2.0)
    k_max_bcc = 0.55 * np.sqrt(3.0)

    for _ in range(n_samples):
        kx, ky = rng.uniform(-k_max_2d, k_max_2d, 2)
        residuals_2d.append(abs(
            omega_dirac_2d_closed(kx, ky, 0.0) - omega_kin_2d(kx, ky)))

        kx, ky, kz = rng.uniform(-k_max_bcc, k_max_bcc, 3)
        D = build_dirac_bcc_4x4(kx, ky, kz, m=0.0, sign='+')
        Om = positive_omega_from_unitary(D)
        residuals_bcc.append(abs(Om - omega_kin_bcc(kx, ky, kz, sign='+')))

    res_2d_max  = float(np.max(residuals_2d))
    res_bcc_max = float(np.max(residuals_bcc))
    return {
        'name':            'P5_photon_limit',
        'max_residual_2d': res_2d_max,
        'max_residual_bcc':res_bcc_max,
        'target':          1e-13,
        'passed':          bool(res_2d_max <= 1e-13 and res_bcc_max <= 1e-13),
    }


# ──────────────────────────────────────────────────────────────────────────────
# P6 — rest limit (k = 0)
# ──────────────────────────────────────────────────────────────────────────────

def test_P6_rest_limit(m_values=(0.0, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99)) -> dict:
    """
    At k=0: cos Ω_kin = 1, identity gives cos Ω_Dirac = cos Ω_rest, i.e.
    Ω_Dirac(0, m) = arcsin(m).  Verified in 2D (closed form) and BCC
    (eigenvalues of D^BCC_k=0).
    """
    rows = []
    max_res_2d  = 0.0
    max_res_bcc = 0.0
    for m in m_values:
        # 2D closed form
        Om_2d  = omega_dirac_2d_closed(0.0, 0.0, m)
        # BCC from eigenvalues
        D_bcc  = build_dirac_bcc_4x4(0.0, 0.0, 0.0, m, sign='+')
        Om_bcc = positive_omega_from_unitary(D_bcc)
        target = abs(omega_rest(m))   # arcsin |m|
        res_2d  = abs(Om_2d  - target)
        res_bcc = abs(Om_bcc - target)
        max_res_2d  = max(max_res_2d, res_2d)
        max_res_bcc = max(max_res_bcc, res_bcc)
        rows.append({
            'm': float(m),
            'omega_dirac_2d':  float(Om_2d),
            'omega_dirac_bcc': float(Om_bcc),
            'omega_rest':      float(target),
            'res_2d':          float(res_2d),
            'res_bcc':         float(res_bcc),
        })
    return {
        'name':            'P6_rest_limit',
        'max_residual_2d': float(max_res_2d),
        'max_residual_bcc':float(max_res_bcc),
        'target':          1e-14,
        'passed':          bool(max_res_2d <= 1e-14 and max_res_bcc <= 1e-14),
        'rows':            rows,
    }


# ──────────────────────────────────────────────────────────────────────────────
# P7 — continuum Pythagorean limit  Ω² ≈ m² + Ω_kin²
# ──────────────────────────────────────────────────────────────────────────────

def test_P7_continuum_limit(scales=(1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125)) -> dict:
    """
    Define small-quantity scale s and probe at k = (s,s)·k_unit, m = s·m_unit.
    Pythagorean residual is

        r(s) = Ω(k,m)² − m² − Ω_kin(k)²

    From the spherical identity cos Ω = cos m · cos Ω_kin and Taylor:
        Ω² = m² + Ω_kin² − (1/12)(m⁴ + Ω_kin⁴ − 6 m² Ω_kin²) + O(6)

    Hence r(s) should scale as **s⁴** (slope 4 in log-log on s).  This is the
    cleanest signature that the continuum E² = p²c² + m² c⁴ is *exact* to
    leading order in s but the lattice has a known calculable 4th-order
    correction — *not* a generic deviation.

    We fit a log-log slope; expect slope ≈ 4.  No `target`, just record.
    """
    # Pick unit directions for k (face-diagonal-ish) and m (a fixed ratio).
    k_unit = np.array([1.0, 0.7])
    m_unit = 0.3
    rows = []
    rs    = []
    for s in scales:
        kx, ky = s * k_unit
        m      = s * m_unit
        Om     = omega_dirac_2d_closed(kx, ky, m)
        Om_kin = omega_kin_2d(kx, ky)
        r      = Om**2 - m**2 - Om_kin**2
        rs.append(abs(r))
        rows.append({
            's': float(s),
            'm': float(m),
            'kx': float(kx), 'ky': float(ky),
            'omega_dirac': float(Om),
            'omega_kin':   float(Om_kin),
            'pythagorean_residual': float(r),
        })
    # log-log slope of |r(s)| vs s
    log_s = np.log(np.array(scales))
    log_r = np.log(np.array(rs))
    slope, intercept = np.polyfit(log_s, log_r, 1)
    return {
        'name':         'P7_continuum_limit',
        'rows':         rows,
        'loglog_slope': float(slope),
        'slope_target': 4.0,
        'passed':       bool(abs(slope - 4.0) <= 0.05),
    }


# ──────────────────────────────────────────────────────────────────────────────
# P8 — F26 cross-link: c_lat from dΩ/d|k|
# ──────────────────────────────────────────────────────────────────────────────

def test_P8_c_lat_recovery(m_values=(0.0, 0.1, 0.3), eps: float = 1e-4) -> dict:
    """
    F26 says c_lat = dΩ_kin/d|k||_{k→0}.  Under the spherical identity, near
    k=0 along a fixed axis kx:

        cos Ω_Dirac = √(1−m²) · cos(kx/√d)

    expanding cos(kx/√d) ≈ 1 − kx²/(2d), so

        Ω_Dirac(kx, m) ≈ arcsin(m) + (√(1−m²)/m)·kx²/(2d)   (m > 0)
        Ω_Dirac(kx, 0) ≈ |kx|/√d                            (m = 0, KINK at 0)

    Predictions:
      m = 0:  Ω(kx) ≈ |kx|/√d  →  forward diff at kx=0+ recovers c_lat = 1/√d.
      m > 0:  Ω(kx) − Ω(0) = O(kx²)  →  forward diff at kx=0+ ≈ 0 (linear in eps).

    Verified by one-sided forward difference (central diff would give 0 by
    parity Ω(−k) = Ω(+k)).  d=2 → c_lat = 1/√2 ≈ 0.7071; d=3 → 1/√3 ≈ 0.5774.
    """
    rows = []
    pass_flags = []
    c_lat_2d  = 1.0 / np.sqrt(2.0)
    c_lat_bcc = 1.0 / np.sqrt(3.0)

    for m in m_values:
        # 2D, forward difference along kx-axis at kx=0+.
        Om_p = omega_dirac_2d_closed(+eps, 0.0, m)
        Om_0 = omega_dirac_2d_closed(0.0,  0.0, m)
        dOm_dk_2d = (Om_p - Om_0) / eps
        # BCC, forward difference along kx-axis at kx=0+.
        D_p = build_dirac_bcc_4x4(+eps, 0.0, 0.0, m, sign='+')
        Om_p_bcc = positive_omega_from_unitary(D_p)
        D_0 = build_dirac_bcc_4x4(0.0,  0.0, 0.0, m, sign='+')
        Om_0_bcc = positive_omega_from_unitary(D_0)
        dOm_dk_bcc = (Om_p_bcc - Om_0_bcc) / eps

        if m == 0.0:
            # Expect c_lat to be recovered.  Forward diff of arccos(cos(eps/√d))
            # has catastrophic cancellation near 1; with eps=1e-4 the realized
            # accuracy is ~ε² · |cos''(0)| ≈ 1e-9 in 2D and slightly tighter on
            # the BCC eigenvalue path.  Use a generous tolerance.
            ok_2d  = abs(dOm_dk_2d  - c_lat_2d ) < 1e-6
            ok_bcc = abs(dOm_dk_bcc - c_lat_bcc) < 1e-6
        else:
            # Expect dΩ/dk ≈ 0; the leading term is √(1−m²)/(2dm) · eps,
            # so the absolute value should be < (a few) · eps.
            ok_2d  = abs(dOm_dk_2d ) < 100 * eps
            ok_bcc = abs(dOm_dk_bcc) < 100 * eps
        pass_flags.extend((ok_2d, ok_bcc))
        rows.append({
            'm': float(m),
            'dOmega_dk_2d':    float(dOm_dk_2d),
            'expected_2d':     c_lat_2d if m == 0.0 else 0.0,
            'dOmega_dk_bcc':   float(dOm_dk_bcc),
            'expected_bcc':    c_lat_bcc if m == 0.0 else 0.0,
            'ok_2d':           bool(ok_2d),
            'ok_bcc':          bool(ok_bcc),
        })
    return {
        'name':  'P8_c_lat_recovery',
        'rows':  rows,
        'notes': ("Forward difference (not central, because Ω(−k) = Ω(+k)). "
                  "m=0 ⇒ kink in Ω at 0 with slope c_lat; m>0 ⇒ smooth, slope 0."),
        'passed': all(pass_flags),
    }


# ──────────────────────────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("F46 — spherical Pythagorean lattice mass identity")
    print("===================================================")
    print("cos Ω_Dirac(k,m) = cos Ω_rest(m) · cos Ω_kin(k)")
    print()

    results = []
    for fn in (test_P1_closed_form_2d,
               test_P2_eigenvalues_2d,
               test_P3_time_evolution_2d,
               test_P4_bcc_extension,
               test_P5_photon_limit,
               test_P6_rest_limit,
               test_P7_continuum_limit,
               test_P8_c_lat_recovery):
        r = fn()
        results.append(r)
        passed = r.get('passed', True)
        tag = "PASS" if passed else "FAIL"
        print(f"  {tag}  {r['name']:30s}  ", end='')
        if 'max_residual' in r:
            print(f"max_res = {r['max_residual']:.3e}  (target {r.get('target')})")
        elif 'max_residual_2d' in r:
            print(f"2D max_res = {r['max_residual_2d']:.3e}, "
                  f"BCC max_res = {r['max_residual_bcc']:.3e}")
        elif 'loglog_slope' in r:
            print(f"log-log slope = {r['loglog_slope']:.4f} "
                  f"(target {r['slope_target']:.1f})")
        else:
            print()

    elapsed = time.time() - t0
    all_pass = all(r.get('passed', True) for r in results)
    print()
    print(f"Total: {sum(r.get('passed', True) for r in results)}/{len(results)} "
          f"tests passed  ({elapsed:.2f} s)")
    print("OVERALL: " + ("PASS" if all_pass else "FAIL"))

    # Dump JSON for downstream test-results consumer.
    out = {
        'finding':       'F46',
        'title':         'Spherical Pythagorean lattice-mass identity',
        'identity':      'cos Ω_Dirac = cos Ω_rest · cos Ω_kin',
        'date_utc':      time.strftime('%Y-%m-%d - %H:%M', time.gmtime()),
        'elapsed_sec':   elapsed,
        'all_passed':    all_pass,
        'tests':         results,
    }
    out_path = os.path.join(_ROOT, 'test-results', 'F46_pythagorean_mass.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nResults written to {out_path}")
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
