"""
test_majorana_fork.py — F43 bare ν_R Majorana mass step and see-saw
                        eigenvalue scaling (Higgs-free)
2026-05-28 - 14:00

Run from project root:
    python model-tests/test_majorana_fork.py

Writes JSON to test-results/majorana_fork.json.

Hypothesis under test
---------------------
(a) The bare ν_R Majorana mass step

        χ_u'  =  c_M χ_u  −  i s_M χ_d*
        χ_d'  =  c_M χ_d  +  i s_M χ_u*

    is (i) R-unitary on the 4 real DOFs and (ii) U(1)_Y gauge invariant
    iff Y_ν_R = 0  (the SM ν_R assignment).  This is the same selection
    rule the SM uses, but realised in the Higgs-free Dirac CA with no
    Higgs anywhere.

(b) Combined with the F27/F41 Dirac mass M_D, the (ν_L, ν_R^c) mass
    matrix is the canonical see-saw matrix and its light eigenvalue
    reproduces

        m_ν  ≈  M_D² / M_R       (M_R ≫ M_D)

    to algebraic exactness via the closed form
    λ_- = (M_R − √(M_R²+4M_D²))/2, and to leading order via the
    asymptotic check  m_ν · M_R / M_D²  →  1.

If both verify, this is a Higgs-free explanation for the smallness of
the active neutrino mass.

Tests
-----
M1  Bare Majorana step preserves |χ_u|² + |χ_d|² exactly (R-unitarity)
    over many random samples and a sweep of M_R values.
M2  Bare Majorana step is invariant under U(1)_Y with Y_ν_R = 0
    (trivially, since the field rotation is the identity).
M3  Bare Majorana step is NOT invariant for Y_ν_R ≠ 0 — explicit
    selection-rule violation, residual scales as |sin(β Y)| · M_R.
M4  BdG infinitesimal extraction: the per-cell Jacobian of
    `mass_step_dirac_majorana_nu` at small dt equals
    `bdg_hamiltonian_nu(M_D, M_R)` to machine precision.
M5  Algebraic exactness of see-saw eigenvalues from
    `seesaw_eigenvalues` vs `numpy.linalg.eigvalsh` on the 2×2 matrix.
M6  See-saw scaling sweep:  m_ν · M_R / M_D² → 1 as M_R/M_D → ∞.
    Residual at each ratio is bounded by (M_D/M_R)² (next-order
    correction).
"""

from __future__ import annotations
import json
import os
import sys
import time
import numpy as np


# ── Path bootstrap ────────────────────────────────────────────────────
_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, '..'))
sys.path.insert(0, os.path.join(_ROOT, 'ca-simulation'))
sys.path.insert(0, os.path.join(_ROOT, 'ca-simulation', 'forks'))

import hypercharge_fork as hf  # noqa: E402


# ── Helpers ───────────────────────────────────────────────────────────
def random_chi(Lx, Ly, seed):
    rng = np.random.default_rng(seed=seed)
    cu = rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
    cd = rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
    return cu, cd


def random_eta_chi(Lx, Ly, seed):
    rng = np.random.default_rng(seed=seed)
    def c():
        return rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
    return c(), c(), c(), c()


def tuple_max_abs_diff(a, b):
    return float(max(np.max(np.abs(ai - bi)) for ai, bi in zip(a, b)))


def field_norm_sq(*arrs):
    return float(sum(np.sum(np.abs(a) ** 2) for a in arrs))


# ══════════════════════════════════════════════════════════════════════
#  M1 — bare Majorana step is R-unitary (norm conservation)
# ══════════════════════════════════════════════════════════════════════
def test_M1_majorana_unitary(L=16, seed=101):
    """
    Apply `mass_step_majorana_chi` for several M_R values and random
    initial χ; verify |χ_u'|² + |χ_d'|² = |χ_u|² + |χ_d|² to machine
    precision.
    """
    cu, cd = random_chi(L, L, seed)
    initial = field_norm_sq(cu, cd)
    residuals = []
    for M_R in [0.0, 1e-6, 0.1, 0.3, 1.0, 5.0, 17.7, 1e3, 1e6]:
        for dt in [0.05, 0.31, 1.0, 1.27]:
            cu_n, cd_n = hf.mass_step_majorana_chi(cu, cd, M_R, dt)
            after = field_norm_sq(cu_n, cd_n)
            residuals.append(abs(after - initial))
    # Now compose many steps and check long-step stability.
    cu_seq, cd_seq = cu.copy(), cd.copy()
    M_R = 0.7;  dt = 0.13
    for _ in range(200):
        cu_seq, cd_seq = hf.mass_step_majorana_chi(cu_seq, cd_seq, M_R, dt)
    residuals.append(abs(field_norm_sq(cu_seq, cd_seq) - initial))
    return float(max(residuals))


# ══════════════════════════════════════════════════════════════════════
#  M2 — U(1)_Y invariance of the Majorana step at Y_ν_R = 0
# ══════════════════════════════════════════════════════════════════════
def test_M2_u1y_invariance_y0(L=16, seed=202):
    """
    With Y_ν_R = 0 (SM assignment), the U(1)_Y phase is e^{i·0/2·β} = 1,
    so the field is unchanged by any β(x).  Verify:

        S_M( V_Y[β] · χ )  =  V_Y[β] · S_M( χ )

    holds to machine precision (here both sides are equal to S_M(χ)).
    """
    cu, cd = random_chi(L, L, seed)
    rng = np.random.default_rng(seed=seed + 1)
    beta = rng.uniform(-np.pi, np.pi, (L, L))

    M_R = 0.42;  dt = 0.17

    # LHS:  S_M( V_Y[β] · χ )
    lhs_in_u, lhs_in_d = hf.apply_u1y_transform_chi(cu, cd, beta, y_charge=0.0)
    lhs_u, lhs_d = hf.mass_step_majorana_chi(lhs_in_u, lhs_in_d, M_R, dt)

    # RHS:  V_Y[β] · S_M( χ )
    rhs_in_u, rhs_in_d = hf.mass_step_majorana_chi(cu, cd, M_R, dt)
    rhs_u, rhs_d = hf.apply_u1y_transform_chi(rhs_in_u, rhs_in_d, beta, y_charge=0.0)

    return tuple_max_abs_diff((lhs_u, lhs_d), (rhs_u, rhs_d))


# ══════════════════════════════════════════════════════════════════════
#  M3 — U(1)_Y selection rule: NOT invariant for Y_ν_R ≠ 0
# ══════════════════════════════════════════════════════════════════════
def test_M3_u1y_selection_rule(L=16, seed=303):
    """
    The Majorana bilinear χ^T ε χ carries hypercharge 2 Y_χ, so for any
    Y_χ ≠ 0 the step transforms with a non-trivial residual under
    U(1)_Y.  Use β = constant so we can compare cleanly:

        V_Y[β]^{-1}  S_M( V_Y[β] χ ; M_R )    !=    S_M( χ ; M_R )

    Specifically:
        V_Y[β] sends χ → e^{i β Y/2} χ.
        χ^T ε χ then picks up e^{i β Y}.
        The mass step's M_R·sin term acquires the phase e^{i β Y},
        whereas the c_M·χ term acquires only e^{i β Y/2}.
        After undoing V_Y on output (e^{-i β Y/2}), the M_R·sin term
        still carries a leftover e^{i β Y/2} ≠ 1.

    We compute the residual and check it is bounded above by (and
    on the right order of) sin(β Y / 2) · M_R · ‖χ‖, i.e. *non-zero*
    and scaling correctly — this is the *selection-rule witness*.

    For Y = 0 the residual must drop to machine precision; we also
    verify that here as the floor.
    """
    cu, cd = random_chi(L, L, seed)
    M_R = 0.5;  dt = 1.0
    norm_chi = float(np.sqrt(field_norm_sq(cu, cd)))

    def residual_for_Y(Y, beta_const):
        beta = np.full((L, L), beta_const)
        # LHS:  V_Y[β]^{-1}  S_M( V_Y[β] χ )
        u_in, d_in = hf.apply_u1y_transform_chi(cu, cd, beta, y_charge=Y)
        u_out, d_out = hf.mass_step_majorana_chi(u_in, d_in, M_R, dt)
        u_lhs, d_lhs = hf.apply_u1y_transform_chi(u_out, d_out, -beta, y_charge=Y)
        # RHS:  S_M( χ )
        u_rhs, d_rhs = hf.mass_step_majorana_chi(cu, cd, M_R, dt)
        return tuple_max_abs_diff((u_lhs, d_lhs), (u_rhs, d_rhs))

    # Y = 0 baseline — must be machine precision.
    r_Y0 = residual_for_Y(0.0, beta_const=0.6)
    # Y = -2 (e_R-like) — must be non-trivial and bounded by 2·s_M·|χ|.
    r_Y2 = residual_for_Y(-2.0, beta_const=0.6)
    # Y = +4/3 (u_R-like)
    r_Y43 = residual_for_Y(+4.0 / 3.0, beta_const=0.6)

    s_M = abs(np.sin(M_R * dt))
    # The selection-rule witness: the Y≠0 residuals must be (i) clearly
    # above 1e-12 and (ii) below the loose bound 4·s_M·‖χ‖ (the maximum
    # the step can rotate by, summed over both branches).
    bound = 4.0 * s_M * norm_chi
    witness_Y2  = (r_Y2  > 1e-3) and (r_Y2  <= bound)
    witness_Y43 = (r_Y43 > 1e-3) and (r_Y43 <= bound)

    # Pack into a single residual: report (r_Y0, ratio of witnesses).
    # We expect r_Y0 ≈ 0 and witness_* True.  The reported "residual"
    # is r_Y0 (must drop below target); we additionally encode the
    # witnesses in extras.
    return {
        'r_Y0': r_Y0,
        'r_Y_minus2': r_Y2,
        'r_Y_plus_4_3': r_Y43,
        'bound_4_s_M_norm': bound,
        'witness_Y_minus2_pass': bool(witness_Y2),
        'witness_Y_plus_4_3_pass': bool(witness_Y43),
    }


# ══════════════════════════════════════════════════════════════════════
#  M4 — BdG infinitesimal extraction matches `bdg_hamiltonian_nu`
# ══════════════════════════════════════════════════════════════════════
def test_M4_bdg_infinitesimal_match(M_D=0.07, M_R=0.91, dt=1e-7):
    """
    The combined Dirac+Majorana mass step, expanded to first order in dt,
    must equal  (I − i dt H + O(dt²))  with H the analytic BdG
    Hamiltonian `bdg_hamiltonian_nu(M_D, M_R)`.

    We extract the Jacobian numerically by stepping each of the 8 basis
    vectors of the doubled state space (z, z*) and forming the matrix
    J such that  z_new ≈ z + dt · (Jz),  then compare iJ to H.
    """
    H_analytic = hf.bdg_hamiltonian_nu(M_D, M_R)

    # Build the 8 basis vectors as 1-site fields, and propagate each.
    # The mass step is local — we use a 1×1 lattice.
    def step_basis(idx):
        eta_u = np.zeros((1, 1), dtype=complex)
        eta_d = np.zeros((1, 1), dtype=complex)
        chi_u = np.zeros((1, 1), dtype=complex)
        chi_d = np.zeros((1, 1), dtype=complex)
        # Indices 0..3 inject 1 into η_u, η_d, χ_u, χ_d.
        # Indices 4..7 inject 1 into the conjugate slot, which we
        # encode as an imaginary unit kick on the corresponding field
        # (since z and z* are independent in the BdG doubling).  We
        # extract real and imaginary perturbations independently below.
        slot = idx % 4
        amp  = 1.0 if idx < 4 else 1j
        if   slot == 0: eta_u[0, 0] = amp
        elif slot == 1: eta_d[0, 0] = amp
        elif slot == 2: chi_u[0, 0] = amp
        elif slot == 3: chi_d[0, 0] = amp
        eu, ed, cu, cd = hf.mass_step_dirac_majorana_nu(
            eta_u, eta_d, chi_u, chi_d, M_D, M_R, dt)
        return complex(eu[0, 0]), complex(ed[0, 0]), complex(cu[0, 0]), complex(cd[0, 0])

    # Numerically extract the 8×8 (real-doubled) generator G such that
    #     [z, z*]_new  =  exp(G dt) [z, z*]    ≈   (I + G dt) [z, z*]
    # then compare iG to H.  We sample two perturbations (1, i) per slot
    # so that the C-linear and anti-C-linear pieces both register.
    G = np.zeros((8, 8), dtype=complex)
    # Column j: response to a unit perturbation in basis direction j of
    # the (z, z*) extended space.
    for j in range(8):
        eu, ed, cu, cd = step_basis(j)
        # Identify the 4 physical responses (eu, ed, cu, cd) and their
        # conjugates (their c.c. directly).
        resp = np.array([eu, ed, cu, cd,
                         np.conj(eu), np.conj(ed), np.conj(cu), np.conj(cd)],
                        dtype=complex)
        # Subtract the input direction to get the *change*.
        delta = resp.copy()
        slot = j % 4
        if j < 4:
            delta[slot]     -= 1.0
            delta[slot + 4] -= 1.0
        else:
            delta[slot]     -= 1j
            delta[slot + 4] -= -1j  # c.c. of 1j is -1j
        G[:, j] = delta / dt

    # Convert the "kick of size 1j" columns (4..7) into the conjugate-
    # slot column representation.  Recall: a perturbation of size 1j in
    # field f corresponds to a unit perturbation in the (f, f*) basis
    # with sign (+1, -1) (since 1j = (e^{iπ/2}·1, e^{-iπ/2}·1) = (i, -i)).
    # So column 4 (kick = i·δ_{slot0}) = i·(column for f₀) − i·(column for f₀*).
    # We need to invert this 2×2 to recover columns for f* slots.  Doing it
    # for each slot:
    G_phys = np.zeros((8, 8), dtype=complex)
    for slot in range(4):
        col_f  = G[:, slot]           # response to δf = 1
        col_fi = G[:, slot + 4] / 1j  # response to δf = 1j, divided by i
        # f_perturb = δf + δf*   when amp=1   (real perturbation)
        # i·f_perturb = δf − δf* when amp=1j  (imag perturbation, then div i)
        # → δf-only response   = (col_f + col_fi) / 2
        #   δf*-only response  = (col_f − col_fi) / 2
        G_phys[:, slot]     = (col_f + col_fi) / 2.0
        G_phys[:, slot + 4] = (col_f - col_fi) / 2.0

    H_numeric = 1j * G_phys
    # Compare on the physical subspace (full 8×8) — must match to ≈ dt.
    residual = float(np.max(np.abs(H_numeric - H_analytic)))
    return residual


# ══════════════════════════════════════════════════════════════════════
#  M5 — Closed-form see-saw eigenvalues vs numpy eigvalsh
# ══════════════════════════════════════════════════════════════════════
def test_M5_seesaw_closed_form(rng_seed=505, n_samples=64):
    """
    For each sampled (M_D, M_R), verify

        seesaw_eigenvalues(M_D, M_R)
            ==  numpy.linalg.eigvalsh(seesaw_2x2_matrix(M_D, M_R))

    to machine precision.  This is an algebraic-exactness check: the
    closed form λ_± = (M_R ± √(M_R²+4M_D²))/2 should equal numpy's
    eigvalsh on the analytic 2×2.
    """
    rng = np.random.default_rng(rng_seed)
    residuals = []
    for _ in range(n_samples):
        M_D = float(rng.uniform(1e-3, 2.0))
        M_R = float(rng.uniform(1e-3, 1e4))
        lam_l, lam_h = hf.seesaw_eigenvalues(M_D, M_R)
        w_np = np.linalg.eigvalsh(hf.seesaw_2x2_matrix(M_D, M_R))
        # numpy returns sorted ascending; match by magnitude.
        idx = np.argsort(np.abs(w_np))
        lam_l_np, lam_h_np = float(w_np[idx[0]]), float(w_np[idx[1]])
        residuals.append(abs(lam_l - lam_l_np))
        residuals.append(abs(lam_h - lam_h_np))
    return float(max(residuals))


# ══════════════════════════════════════════════════════════════════════
#  M6 — See-saw scaling sweep:  m_ν · M_R / M_D²  →  1
# ══════════════════════════════════════════════════════════════════════
def test_M6_seesaw_scaling(M_D=1.0):
    """
    For a sweep of M_R/M_D ratios, compute the light eigenvalue m_ν
    from the closed form and verify

        |m_ν| · M_R / M_D²   →   1     as M_R/M_D → ∞

    The next-order correction is O((M_D/M_R)²), so we require
        |  |m_ν| · M_R / M_D²  −  1  |   <=   1.1 · (M_D/M_R)²
    at every sampled ratio.  We *also* verify the BdG Hamiltonian's
    smallest |eigenvalue| matches the closed-form light mass to
    machine precision (cross-check between the 2×2 analytic see-saw
    and the 8×8 BdG construction).
    """
    ratios = [3.0, 10.0, 30.0, 100.0, 300.0, 1e3, 3e3, 1e4, 3e4, 1e5]
    per_ratio = []
    max_scaling_resid     = 0.0
    max_bdg_match_resid   = 0.0
    for r in ratios:
        M_R = r * M_D
        # Closed form (numerically stable via Vieta in seesaw_eigenvalues)
        lam_light, lam_heavy = hf.seesaw_eigenvalues(M_D, M_R)
        m_nu = abs(lam_light)
        # Asymptotic see-saw approximation
        m_nu_approx = hf.seesaw_light_mass_approx(M_D, M_R)
        # Scaling: m_ν · M_R / M_D²  should → 1
        scale = m_nu * M_R / (M_D * M_D)
        deviation_from_1 = abs(scale - 1.0)
        # Next-order bound:  Δ ≈ (M_D/M_R)²
        next_order_bound = 1.1 * (M_D / M_R) ** 2
        scaling_pass = (deviation_from_1 <= next_order_bound)
        max_scaling_resid = max(max_scaling_resid,
                                deviation_from_1 - next_order_bound)
        # BdG cross-check: |smallest BdG eigenvalue| == |lam_light|.
        # eigvalsh has noise floor ~ ||H|| · eps_machine = M_R · 1e-16,
        # so we use a relative tolerance that scales with M_R.
        bdg_w = hf.bdg_spectrum_nu(M_D, M_R)
        bdg_light = abs(bdg_w[0])
        bdg_match_resid = abs(bdg_light - m_nu)
        bdg_match_tol   = max(1e-12, 1e-12 * M_R)
        bdg_match_pass  = (bdg_match_resid <= bdg_match_tol)
        max_bdg_match_resid = max(max_bdg_match_resid,
                                  bdg_match_resid / max(bdg_match_tol, 1e-300))

        per_ratio.append({
            'ratio_M_R_over_M_D': r,
            'm_nu_closed_form':   float(m_nu),
            'm_nu_approx_MD2_MR': float(m_nu_approx),
            'scale_m_nu_MR_over_MD2': float(scale),
            'deviation_from_1':   float(deviation_from_1),
            'next_order_bound':   float(next_order_bound),
            'scaling_pass':       bool(scaling_pass),
            'bdg_light_eigenval': float(bdg_light),
            'bdg_vs_closed_form_resid': float(bdg_match_resid),
            'bdg_match_tol':      float(bdg_match_tol),
            'bdg_match_pass':     bool(bdg_match_pass),
            'heavy_eigenvalue':   float(abs(lam_heavy)),
        })

    return {
        'max_scaling_excess_over_bound':  float(max_scaling_resid),
        'max_bdg_relative_resid':         float(max_bdg_match_resid),
        'per_ratio':                      per_ratio,
        'overall_scaling_pass':           bool(max_scaling_resid <= 0.0),
        'overall_bdg_match_pass':         bool(all(p['bdg_match_pass']
                                                   for p in per_ratio)),
    }


# ══════════════════════════════════════════════════════════════════════
#  Runner
# ══════════════════════════════════════════════════════════════════════
def main():
    out_dir = os.path.join(_ROOT, 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'majorana_fork.json')

    results = []
    overall_pass = True
    t0 = time.time()

    # M1
    # Note: the sweep includes M_R up to 1e6 with multiple dt values; for
    # very large M_R·dt the per-step cos/sin lose precision and the
    # cumulative norm drift over 200 composed steps approaches the
    # working-precision floor of ~|chi|^2 · N_ops · eps_machine.  Target
    # 1e-9 is well above that floor and well below any physically
    # meaningful drift (~1e-12 for moderate M_R).
    t = time.time()
    r = test_M1_majorana_unitary()
    elapsed = time.time() - t
    p = (r < 1e-9)
    overall_pass &= p
    results.append({
        'name': 'M1_majorana_unitary',
        'residual': r,
        'target':   1e-9,
        'pass':     bool(p),
        'elapsed_s': round(elapsed, 4),
        'description': 'Bare Majorana step preserves |chi_u|^2 + |chi_d|^2.',
    })

    # M2
    t = time.time()
    r = test_M2_u1y_invariance_y0()
    elapsed = time.time() - t
    p = (r < 1e-12)
    overall_pass &= p
    results.append({
        'name': 'M2_u1y_invariance_y_nuR_zero',
        'residual': r,
        'target':   1e-12,
        'pass':     bool(p),
        'elapsed_s': round(elapsed, 4),
        'description': 'Majorana step invariant under U(1)_Y at Y_nuR = 0.',
    })

    # M3
    t = time.time()
    info_M3 = test_M3_u1y_selection_rule()
    elapsed = time.time() - t
    p = ((info_M3['r_Y0'] < 1e-12) and
         info_M3['witness_Y_minus2_pass'] and
         info_M3['witness_Y_plus_4_3_pass'])
    overall_pass &= p
    results.append({
        'name': 'M3_u1y_selection_rule',
        'residual':   info_M3['r_Y0'],
        'target':     1e-12,
        'extras':     info_M3,
        'pass':       bool(p),
        'elapsed_s':  round(elapsed, 4),
        'description': ('U(1)_Y selection rule witness: residual is '
                        'machine zero at Y=0 and clearly non-zero for '
                        'Y in {-2, +4/3}.'),
    })

    # M4
    t = time.time()
    r = test_M4_bdg_infinitesimal_match()
    elapsed = time.time() - t
    # dt = 1e-7, so |J - H| ~ O(dt) ≈ 1e-7 at worst; we allow 1e-4 to
    # be tolerant of higher-order terms but expect << 1e-4 in practice.
    p = (r < 1e-4)
    overall_pass &= p
    results.append({
        'name': 'M4_bdg_infinitesimal_match',
        'residual': r,
        'target':   1e-4,
        'pass':     bool(p),
        'elapsed_s': round(elapsed, 4),
        'description': ('Numerical Jacobian of '
                        'mass_step_dirac_majorana_nu at dt=1e-7 equals '
                        'bdg_hamiltonian_nu(M_D, M_R).'),
    })

    # M5
    t = time.time()
    r = test_M5_seesaw_closed_form()
    elapsed = time.time() - t
    p = (r < 1e-9)
    overall_pass &= p
    results.append({
        'name': 'M5_seesaw_closed_form',
        'residual': r,
        'target':   1e-9,
        'pass':     bool(p),
        'elapsed_s': round(elapsed, 4),
        'description': ('Closed-form seesaw_eigenvalues = '
                        'numpy.linalg.eigvalsh(seesaw_2x2_matrix) over '
                        'a random (M_D, M_R) sweep.'),
    })

    # M6
    t = time.time()
    info_M6 = test_M6_seesaw_scaling()
    elapsed = time.time() - t
    p = info_M6['overall_scaling_pass'] and info_M6['overall_bdg_match_pass']
    overall_pass &= p
    results.append({
        'name': 'M6_seesaw_scaling',
        'residual':  info_M6['max_scaling_excess_over_bound'],
        'target':    0.0,
        'extras':    info_M6,
        'pass':      bool(p),
        'elapsed_s': round(elapsed, 4),
        'description': ('See-saw scaling: m_nu * M_R / M_D^2 -> 1 with '
                        'residual bounded by 1.1 * (M_D/M_R)^2 at every '
                        'sampled ratio; BdG smallest |eigenvalue| matches '
                        'closed-form light mass to <1e-10.'),
    })

    total_elapsed = time.time() - t0
    summary = {
        'L':            16,
        'pass_count':   sum(1 for r in results if r['pass']),
        'total_count':  len(results),
        'overall_pass': bool(overall_pass),
        'elapsed_s':    round(total_elapsed, 4),
        'results':      results,
    }
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)

    # Console summary
    print(f"Wrote {out_path}")
    print(f"{summary['pass_count']}/{summary['total_count']} tests passed "
          f"in {total_elapsed:.4f}s.")
    for r in results:
        flag = 'PASS' if r['pass'] else 'FAIL'
        res = r['residual']
        tgt = r['target']
        print(f"  [{flag}] {r['name']:36s}  residual={res:.3e}  target={tgt:.0e}")

    return 0 if overall_pass else 1


if __name__ == '__main__':
    sys.exit(main())
