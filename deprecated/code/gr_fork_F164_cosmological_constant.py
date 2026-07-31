# ===== deprecated/code backup =====================================
# source     : ca-simulation/forks/gr_fork_F164_cosmological_constant.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/forks/gravity/gr_fork_F164_cosmological_constant.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: gr_fork_F164_cosmological_constant.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
gr_fork_F164_cosmological_constant.py
=====================================
Finding F164 — the cosmological-constant (vacuum-energy) sector of the
BCC Weyl QCA.  Self-contained (mirrors ca_bcc F26 dispersion, real
arithmetic only; no numpy.linalg on chiral transforms).

What this computes
------------------
1.  The dimensionless zero-point integral over the Brillouin zone,
        I_CC = ∫_BZ d³k/(2π)³ · ω(k)/2 ,
    for the BCC + branch dispersion ω(k) = arccos(u), and the exact
    mean rotation ⟨ω⟩_BZ = π/2.
2.  The bare lattice vacuum-energy density at the F107 canonical cell,
        ρ_vac = g_* · (ħ/τ) · (1/a³) · I_CC = g_* · √3 · I_CC · ħc/a⁴ ,
    and its ratio to the observed dark-energy density ρ_Λ.

The result is the model's quantitative statement of the
"120-orders-of-magnitude" cosmological-constant problem: a definite,
finite number (no regularisation ambiguity — the BZ is the physical
cutoff), wrong by ≈10¹²¹.
"""

import json
import os
import numpy as np
from casim.constants import (
    a_over_ellP as _a_over_ellP,
    c_SI as _c_SI,
    ell_P_m as _ell_P_m,
    hbar_SI as _hbar_SI,
)

# ── physical constants (SI / CODATA) ──────────────────────────────
HBAR = _hbar_SI      # J s
C    = _c_SI         # m / s
ELLP = _ell_P_m         # m   (Planck length)
EV   = 1.602176634e-19      # J

# F107 canonical cell:  a = √(8π)·3^{1/4}·ℓ_P ,  τ = a/(c√3)
A_CELL = _a_over_ellP * ELLP
TAU    = A_CELL / (C * np.sqrt(3.0))

# observed dark-energy density  Ω_Λ·ρ_crit ≈ (2.3 meV)⁴
RHO_LAMBDA = 6.0e-10        # J / m³


def omega_plus(qx, qy, qz):
    """BCC '+' branch rotation angle per tick, dimensionless variable q = k/√3."""
    cx, cy, cz = np.cos(qx), np.cos(qy), np.cos(qz)
    sx, sy, sz = np.sin(qx), np.sin(qy), np.sin(qz)
    u = cx * cy * cz + sx * sy * sz
    return np.arccos(np.clip(u, -1.0, 1.0))


def bz_mean_omega(n_samples=200000, seed=0):
    """⟨ω⟩ over the period cube q∈[-π,π]³ — exact value π/2 (see pairing below)."""
    rng = np.random.default_rng(seed)
    q = rng.uniform(-np.pi, np.pi, size=(n_samples, 3))
    return float(omega_plus(q[:, 0], q[:, 1], q[:, 2]).mean())


def zero_point_integral(n=220):
    """
    I_CC = ∫_BZ d³k/(2π)³ ω/2 with k = √3·q (lattice momentum k_phys = k/a).
    Integrate q over one period cube [-π,π]³; Jacobian d³k = 3^{3/2} d³q.
    """
    q = (np.arange(n) + 0.5) / n * 2 * np.pi - np.pi
    dq = 2 * np.pi / n
    QX, QY, QZ = np.meshgrid(q, q, q, indexing="ij")
    w = omega_plus(QX, QY, QZ)
    jac = 3 ** 1.5
    I_cc = float((w / 2).sum() * dq ** 3 * jac / (2 * np.pi) ** 3)
    return I_cc, float(w.mean())


def vacuum_energy_density(I_cc, g_star=2):
    """ρ_vac = g_*·(ħ/τ)·(1/a³)·I_CC  =  g_*·√3·I_CC·ħc/a⁴   [J/m³]."""
    return g_star * (HBAR / (TAU * A_CELL ** 3)) * I_cc


def quartic_scale_eV(rho):
    """(ρ)^{1/4} expressed as an energy scale in eV."""
    return (rho * (HBAR * C) ** 3) ** 0.25 / EV


def run():
    I_cc, w_mean_grid = zero_point_integral()
    w_mean_mc = bz_mean_omega()

    # exact pairing check: u(q) + u(q + π x̂) = 0  ⟹  ω + ω' = π  ⟹  ⟨ω⟩ = π/2
    rng = np.random.default_rng(1)
    qa = rng.uniform(-np.pi, np.pi, size=(50000, 3))
    qb = qa.copy(); qb[:, 0] += np.pi
    def _u(q):
        cx, cy, cz = np.cos(q[:, 0]), np.cos(q[:, 1]), np.cos(q[:, 2])
        sx, sy, sz = np.sin(q[:, 0]), np.sin(q[:, 1]), np.sin(q[:, 2])
        return cx * cy * cz + sx * sy * sz
    pairing_residual = float(np.max(np.abs(_u(qa) + _u(qb))))

    g_star = 2
    rho_vac = vacuum_energy_density(I_cc, g_star=g_star)
    ratio = rho_vac / RHO_LAMBDA

    result = {
        "finding": "F164",
        "canonical_cell_a_m": A_CELL,
        "a_over_ellP": A_CELL / ELLP,
        "tau_s": TAU,
        "I_CC_dimensionless": I_cc,
        "mean_omega_grid": w_mean_grid,
        "mean_omega_mc": w_mean_mc,
        "mean_omega_exact_pi_over_2": np.pi / 2,
        "pi_over_2_pairing_residual": pairing_residual,
        "g_star": g_star,
        "rho_vac_bare_J_per_m3": rho_vac,
        "hbar_c_over_a4_J_per_m3": HBAR * C / A_CELL ** 4,
        "rho_Lambda_observed_J_per_m3": RHO_LAMBDA,
        "ratio_rho_vac_over_rho_Lambda": ratio,
        "log10_ratio": np.log10(ratio),
        "rho_vac_quartic_eV": quartic_scale_eV(rho_vac),
        "rho_Lambda_quartic_eV": quartic_scale_eV(RHO_LAMBDA),
        "energy_scale_ratio": quartic_scale_eV(rho_vac) / quartic_scale_eV(RHO_LAMBDA),
        "sign_note": "all-fermion vacuum ⟹ bare zero-point sum is NEGATIVE; "
                     "magnitude reported, sign is -1 (opposite the observed +ρ_Λ).",
    }
    return result


if __name__ == "__main__":
    res = run()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.normpath(os.path.join(
        here, "..", "..", "test-results", "F164_cosmological_constant.json"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2)
    for k, v in res.items():
        print(f"{k:38s} = {v}")
    print(f"\nwrote {out}")
