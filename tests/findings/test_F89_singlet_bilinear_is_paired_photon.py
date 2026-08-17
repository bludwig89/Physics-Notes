"""
test_F89_singlet_bilinear_is_paired_photon.py
=============================================
2026-06-03 - constructive closure of the F68/F69 "two entities?" question.

CLAIM UNDER TEST (F89): there is ONE underlying gauge-boson entity — a
bilinear of two Weyl constituents on the BCC walk — and the photon vs
W/Z/gluon distinction is a CHANNEL distinction of that one entity, not two
different kinds of object:

    2 ⊗ 2 (spin space)  =  singlet (σ⁰ / ε)  ⊕  σ-vector triplet

  * singlet channel  → helicity-blind → Ω_even = Ω_pair  → the photon (F68/F69)
  * σ-vector channel → branch-split  → Ω^± (chiral law) → W/Z/gluon (F39/F29)

F69 built the paired photon at the *dispersion* level.  What was argued but
not constructively verified is that the singlet bilinear, built from the SAME
Weyl constituents the σ-bilinear machinery uses, propagates at exactly the
even-law rate of `ca_wmu._f26_rotation_step` = `ca_photon_pair.pair_dispersion`.
This test verifies it with the real model operators.

Checks
------
T1  Cross-branch pair bilinear rate is Ω_pair, exactly.
    ψ⁺ = positive eigenmode of U⁺(k/2), φ⁻ = positive eigenmode of U⁻(k/2),
    each evolved by ITS OWN branch unitary (matrix multiplication — the real
    walk operator, no np.linalg.eig, no stipulated phases).  The pairing
    singlet  G_s = φ^T (iσ_y) ψ  (the ε-contraction — the invariant of 2⊗2)
    advances per tick by exactly  Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2).
    Additionally: ALL Paper-1 channels G^i = φ^T σ^i ψ of the SAME cross-
    branch pair advance at the SAME Ω_pair — the rate attaches to the
    pairing (the entity), not to the channel operator.

T2  Measured pair-bilinear rate == rotation angle actually applied by
    `ca_wmu._f26_rotation_step` (the canonical photon/even propagator),
    mode by mode.

T3  Branch symmetry: swapping which constituent rides which branch
    (ψ⁻, φ⁺) leaves the rate unchanged — "only occurs as a pair" has no
    orientation; zero birefringence in the singlet channel.

T4  Contrast (the kept non-Abelian construction): SAME-branch pairs built
    with the SAME bilinear operators advance at Ω⁺ = 2ω⁺(k/2) and
    Ω⁻ = 2ω⁻(k/2); their split equals `ca_photon_pair.pair_birefringence`
    exactly and is nonzero on the body diagonal.  Same machinery, different
    branch pairing → the chiral (W/Z/gluon) law.

T5  Operator-level channel split (constructive version of F68 T1/T3):
    under simultaneous same-branch evolution ψ→Uψ, φ→Uψ-style transport,
    the Hermitian identity-channel bilinear  s = φ†σ⁰ψ  is EXACTLY invariant
    (helicity/phase-blind — the U(1) coupling channel), while the Hermitian
    σ-vector  v^i = φ†σ^iψ  precesses about n̂ by exactly 2ω per tick
    (the adjoint rotation the W sector rides).

Pass criteria: T1–T4 residuals ≤ 5e-13 (machine, accumulated matrix
round-off); T4 split nonzero where pair_birefringence is nonzero; T5
invariance ≤ 5e-13 and adjoint-rotation residual ≤ 5e-13.

Writes test-results/F89_singlet_bilinear_paired_photon.json.
"""

import json
import os
import sys
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.lattice import bcc as bcc
from casim.engine.gauge import photon as pp
from casim.engine.gauge.weak_wmu import _f26_rotation_step

RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results',
                            'F89_singlet_bilinear_paired_photon.json')

ROOT3 = np.sqrt(3.0)

_S_X = np.array([[0, 1], [1, 0]], dtype=complex)
_S_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_S_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS = (_S_X, _S_Y, _S_Z)
_EPS = 1j * _S_Y                      # ε = iσ_y : the 2⊗2 singlet contraction
_I2 = np.eye(2, dtype=complex)

MACHINE = 5e-13


# ----------------------------------------------------------------------
# Closed-form BCC operators (no np.linalg.eig — CLAUDE.md chiral practice)
# ----------------------------------------------------------------------
def U_matrix(kx, ky, kz, sign='+'):
    """U^±(k) = u·I − i(n·σ) as an explicit 2×2 complex matrix."""
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    return np.array([
        [u - 1j * nz,          -1j * (nx - 1j * ny)],
        [-1j * (nx + 1j * ny),  u + 1j * nz],
    ], dtype=complex)


def positive_eigenmode(kx, ky, kz, sign='+'):
    """Closed-form positive-frequency eigenmode: U χ = e^{−iω} χ.

    χ is the (n̂·σ) = +1 spinor: with n̂ = n/|n|,
        χ = ( cos(θ/2), e^{iφ} sin(θ/2) )  built algebraically from n̂.
    Then U χ = (u − i|n|) χ = e^{−iω} χ since cos ω = u, sin ω = |n|.
    """
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    nmag = np.sqrt(nx * nx + ny * ny + nz * nz)
    if nmag < 1e-300:
        raise ValueError("k too close to 0: eigenmode degenerate")
    nhx, nhy, nhz = nx / nmag, ny / nmag, nz / nmag
    if nhz < -1.0 + 1e-12:           # n̂ ≈ −ẑ: χ₊ = (0, 1)
        chi = np.array([0.0, 1.0], dtype=complex)
    else:
        norm = np.sqrt(2.0 * (1.0 + nhz))
        chi = np.array([(1.0 + nhz) / norm,
                        (nhx + 1j * nhy) / norm], dtype=complex)
    omega = float(np.arccos(np.clip(u, -1.0, 1.0)))
    return chi, omega


def per_tick_phase(g_prev, g_next):
    """−arg(g_next/g_prev) ∈ [0, 2π): the rotation rate the bilinear rides."""
    return float(np.mod(-np.angle(g_next / g_prev), 2.0 * np.pi))


def circ_diff(a, b):
    """Distance between two angles mod 2π."""
    d = np.mod(a - b, 2.0 * np.pi)
    return float(np.minimum(d, 2.0 * np.pi - d))


def rodrigues(n_hat, angle):
    """3×3 rotation about unit axis n̂ by `angle` (right-handed)."""
    n = np.asarray(n_hat, float)
    Km = np.array([[0, -n[2], n[1]],
                   [n[2], 0, -n[0]],
                   [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(angle) * Km + (1 - np.cos(angle)) * (Km @ Km)


def random_k(rng, kmin=0.05, kmax=1.2):
    """Random k with ω⁺+ω⁻ safely inside (0, 2π) — no phase wraparound."""
    d = rng.standard_normal(3)
    d /= np.linalg.norm(d)
    return float(rng.uniform(kmin, kmax)) * d


# ----------------------------------------------------------------------
# T1/T2/T3 — cross-branch pair: singlet (and all channels) ride Ω_pair
# ----------------------------------------------------------------------
def run_T123(n_k=2000, n_ticks=8, seed=70):
    rng = np.random.default_rng(seed)
    worst_T1_singlet = 0.0
    worst_T1_channels = 0.0
    worst_T2 = 0.0
    worst_T3 = 0.0
    used = 0
    for _ in range(n_k):
        k = random_k(rng)
        kh = k / 2.0
        Up = U_matrix(*kh, sign='+')
        Um = U_matrix(*kh, sign='-')
        psi, _ = positive_eigenmode(*kh, sign='+')   # rides ω⁺(k/2)
        phi, _ = positive_eigenmode(*kh, sign='-')   # rides ω⁻(k/2)

        Omega_pair = float(pp.pair_dispersion(*k))

        # evolve with the real branch unitaries; track all four channels
        ps, ph = psi.copy(), phi.copy()
        g_s_prev = ph @ _EPS @ ps
        if abs(g_s_prev) < 1e-9:                      # degenerate sample
            continue
        g_c_prev = np.array([ph @ S @ ps for S in _PAULIS])
        used += 1
        for _t in range(n_ticks):
            ps = Up @ ps
            ph = Um @ ph
            g_s = ph @ _EPS @ ps
            g_c = np.array([ph @ S @ ps for S in _PAULIS])

            # T1a: singlet rate == Ω_pair
            rate = per_tick_phase(g_s_prev, g_s)
            worst_T1_singlet = max(worst_T1_singlet,
                                   circ_diff(rate, Omega_pair))

            # T1b: every nonzero Paper-1 σ-channel of the SAME pair
            # rides the SAME Ω_pair (rate attaches to the pairing)
            for a in range(3):
                if abs(g_c_prev[a]) > 1e-9:
                    worst_T1_channels = max(
                        worst_T1_channels,
                        circ_diff(per_tick_phase(g_c_prev[a], g_c[a]),
                                  Omega_pair))

            # T2: == the angle _f26_rotation_step actually applies
            KX = np.array([k[0]]); KY = np.array([k[1]]); KZ = np.array([k[2]])
            e1, b1 = _f26_rotation_step(np.array([1.0 + 0j]),
                                        np.array([0.0 + 0j]), KX, KY, KZ)
            Omega_prop = float(np.mod(np.arctan2(-b1.real[0], e1.real[0]),
                                      2.0 * np.pi))
            worst_T2 = max(worst_T2, circ_diff(rate, Omega_prop))

            g_s_prev, g_c_prev = g_s, g_c

        # T3: branch swap — (ψ on '−', φ on '+') rides the same rate
        psi2, _ = positive_eigenmode(*kh, sign='-')
        phi2, _ = positive_eigenmode(*kh, sign='+')
        g0 = phi2 @ _EPS @ psi2
        if abs(g0) > 1e-9:
            g1 = (Up @ phi2) @ _EPS @ (Um @ psi2)
            worst_T3 = max(worst_T3,
                           circ_diff(per_tick_phase(g0, g1), Omega_pair))
    return worst_T1_singlet, worst_T1_channels, worst_T2, worst_T3, used


# ----------------------------------------------------------------------
# T4 — same machinery, same-branch pairing → the chiral (W) rates
# ----------------------------------------------------------------------
def run_T4(n_k=2000, seed=71):
    rng = np.random.default_rng(seed)
    worst_rate_p = 0.0
    worst_rate_m = 0.0
    worst_split = 0.0
    splits = []
    for _ in range(n_k):
        k = random_k(rng)
        kh = k / 2.0
        for sign, rec in (('+', 'p'), ('-', 'm')):
            Us = U_matrix(*kh, sign=sign)
            chi, om = positive_eigenmode(*kh, sign=sign)
            # same-branch pair: both constituents on this branch
            g0 = chi @ _EPS @ chi
            # ε-contraction of a spinor with itself vanishes (antisymmetric);
            # use the σ-channels, which is what the W machinery does
            g0 = np.array([chi @ S @ chi for S in _PAULIS])
            a = int(np.argmax(np.abs(g0)))
            g1 = (Us @ chi) @ _PAULIS[a] @ (Us @ chi)
            rate = per_tick_phase(g0[a], g1)
            Omega_branch = float(np.mod(2.0 * om, 2.0 * np.pi))
            err = circ_diff(rate, Omega_branch)
            if rec == 'p':
                worst_rate_p = max(worst_rate_p, err)
                Op = 2.0 * om
            else:
                worst_rate_m = max(worst_rate_m, err)
                Om_ = 2.0 * om
        split = Op - Om_
        split_exact = float(pp.pair_birefringence(*k))
        worst_split = max(worst_split, abs(split - split_exact))
        splits.append(abs(split_exact))
    # body diagonal: split must be nonzero (the chiral law is really chiral)
    kbd = 0.4 * np.array([1.0, 1.0, 1.0]) / ROOT3
    split_bd = float(pp.pair_birefringence(*kbd))
    return worst_rate_p, worst_rate_m, worst_split, float(np.median(splits)), split_bd


# ----------------------------------------------------------------------
# T5 — operator-level channel split: σ⁰ frozen, σ-vector precesses by 2ω
# ----------------------------------------------------------------------
def run_T5(n_k=500, n_ticks=6, seed=72):
    rng = np.random.default_rng(seed)
    worst_singlet = 0.0
    worst_adjoint = 0.0
    for _ in range(n_k):
        k = random_k(rng)
        kh = k / 2.0
        sign = '+' if rng.uniform() < 0.5 else '-'
        Us = U_matrix(*kh, sign=sign)
        u, nx, ny, nz = bcc._bcc_uvec(*kh, sign=sign)
        nmag = np.sqrt(nx * nx + ny * ny + nz * nz)
        n_hat = np.array([nx, ny, nz]) / nmag
        om = float(np.arccos(np.clip(u, -1.0, 1.0)))
        R = rodrigues(n_hat, 2.0 * om)

        # generic (non-eigen) spinors — both transported by the same walk
        psi = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        phi = rng.standard_normal(2) + 1j * rng.standard_normal(2)

        s_prev = np.conj(phi) @ _I2 @ psi
        v_prev = np.array([np.conj(phi) @ S @ psi for S in _PAULIS])
        for _t in range(n_ticks):
            psi = Us @ psi
            phi = Us @ phi
            s = np.conj(phi) @ _I2 @ psi
            v = np.array([np.conj(phi) @ S @ psi for S in _PAULIS])
            # σ⁰ channel: exactly invariant (identity channel is blind)
            worst_singlet = max(worst_singlet, abs(s - s_prev))
            # σ-vector channel: exact adjoint rotation by 2ω about n̂
            worst_adjoint = max(worst_adjoint,
                                float(np.max(np.abs(v - R @ v_prev))))
            s_prev, v_prev = s, v
    return worst_singlet, worst_adjoint


def main():
    print("F89 — singlet bilinear IS the paired photon (one entity, two channels)")
    print("=" * 74)

    t1s, t1c, t2, t3, used = run_T123()
    print(f"T1a singlet rate == Ω_pair          : {t1s:.3e}   ({used} k-points)")
    print(f"T1b all σ-channels of pair == Ω_pair: {t1c:.3e}")
    print(f"T2  rate == _f26_rotation_step angle: {t2:.3e}")
    print(f"T3  branch-swap symmetry            : {t3:.3e}")

    t4p, t4m, t4split, t4median, t4bd = run_T4()
    print(f"T4  same-branch '+' rate == Ω⁺      : {t4p:.3e}")
    print(f"T4  same-branch '−' rate == Ω⁻      : {t4m:.3e}")
    print(f"T4  split == pair_birefringence     : {t4split:.3e}")
    print(f"T4  median |ΔΩ| (chiral channel)    : {t4median:.3e}  (nonzero)")
    print(f"T4  body-diagonal ΔΩ at k=0.4       : {t4bd:.3e}  (nonzero)")

    t5s, t5a = run_T5()
    print(f"T5  σ⁰ channel invariance           : {t5s:.3e}")
    print(f"T5  σ-vector adjoint rotation (2ω)  : {t5a:.3e}")

    checks = {
        "T1a_singlet_rate_eq_pair_dispersion": {"residual": float(t1s), "pass": bool(t1s <= MACHINE)},
        "T1b_all_channels_ride_pair_rate": {"residual": float(t1c), "pass": bool(t1c <= MACHINE)},
        "T2_rate_eq_f26_rotation_step": {"residual": float(t2), "pass": bool(t2 <= MACHINE)},
        "T3_branch_swap_symmetric": {"residual": float(t3), "pass": bool(t3 <= MACHINE)},
        "T4_same_branch_plus_rate": {"residual": float(t4p), "pass": bool(t4p <= MACHINE)},
        "T4_same_branch_minus_rate": {"residual": float(t4m), "pass": bool(t4m <= MACHINE)},
        "T4_split_eq_pair_birefringence": {"residual": float(t4split), "pass": bool(t4split <= MACHINE)},
        "T4_chiral_split_nonzero_body_diag": {"value": float(t4bd), "pass": bool(abs(t4bd) > 1e-6)},
        "T5_sigma0_invariant": {"residual": float(t5s), "pass": bool(t5s <= MACHINE)},
        "T5_sigma_vector_adjoint_2omega": {"residual": float(t5a), "pass": bool(t5a <= MACHINE)},
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    verdict = "PASS" if n_pass == len(checks) else "FAIL"
    print("-" * 74)
    print(f"{n_pass}/{len(checks)} checks pass → {verdict}")

    out = {
        "finding": "F89",
        "title": "Singlet bilinear is the paired photon — one entity, two channels",
        "date": "2026-06-03",
        "claim": ("2⊗2 of the same Weyl constituents: singlet/ε channel rides "
                  "Ω_pair = Ω_even (photon); σ-vector channel rides Ω± "
                  "(W/Z/gluon). Same machinery, channel distinction only."),
        "checks": checks,
        "verdict": verdict,
        "params": {"n_k_T123": 2000, "n_ticks": 8, "n_k_T4": 2000,
                   "n_k_T5": 500, "machine_threshold": MACHINE},
    }
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"results → {os.path.relpath(RESULTS_PATH, os.path.dirname(__file__))}")
    return 0 if verdict == "PASS" else 1


if __name__ == '__main__':
    sys.exit(main())
