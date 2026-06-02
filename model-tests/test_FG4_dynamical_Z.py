"""
test_FG4_dynamical_Z.py
========================

FG-4 — Dynamical Z neutral-current sector.  Promotes F35 from algebraic
mixing to a propagating Z field coupled to the fermion neutral current
J^Z_μ = J^3_μ − sin²θ_W · J^em_μ.

Tests
-----
  Z1   Per-species (g_L, g_R) match T_3 − Q s²_W and −Q s²_W (7 species)
  Z2   Source-basis identity:
       g W^3 J^3 + g'(B)(J^em − J^3) = e A J^em + g_Z Z (J^3 − s²_W J^em)
  Z3   m_Z / m_W = 1/cos θ_W (replays F35 W6.3 via z_mass_from_w)
  Z4   Free Z propagation dispersion = even BCC dispersion (massless)
  Z5   Massive Proca Z dispersion ω² = m_Z² + Ω_even²(k)
  Z6   Z from weinberg_mix∘(W^3,B) and direct z propagation commute
  Z7   Source kick:  E_Z(t+1) − E_Z_free(t+1) = g_Z · J_Z · dt exact
  Z8   Neutrino Z coupling has no θ_W dependence (g_L^ν = 1/2)
  Z9   Photon-neutrino coupling identically zero (Q_ν = 0)
  Z10  (g_V, g_A) = (T_3 − 2Q s²_W, T_3) for all 7 species
  Z11  F45 bare angle (sin²θ_W = 1/4): g_V^e = 0 exactly
  Z12  Massless Proca step reduces bit-for-bit to massless step

Run:  python3 model-tests/test_FG4_dynamical_Z.py
"""

import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np

from ca_z_field import (
    SPECIES, T3_TABLE, Q_TABLE, THETA_W_F45,
    z_couplings, z_coupling_strength, photon_coupling_strength,
    z_mass_from_w,
    fermion_em_current, fermion_T3_current,
    fermion_neutral_current, fermion_neutral_current_per_species,
    make_z_field,
    z_propagation_step_spectral, z_massive_propagation_step_spectral,
    z_sourced_propagation_step,
    z_from_w3_b, photon_from_w3_b,
    source_basis_identity_residual,
)
from ca_wmu import (
    weinberg_mix, weinberg_unmix, ew_charge,
    hypercharge_propagation_step,
)
from ca_bcc import bcc_dispersion
from ca_lattice import make_kgrid_3d as _kgrid3d
import ca_fft as _fft


L = 16
rng = np.random.default_rng(seed=2026)


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _rand_field():
    f = rng.standard_normal((L, L, L))
    return (f / np.sqrt(np.mean(f**2))).astype(float)


# ════════════════════════════════════════════════════════════════════
# Z1 — Per-species (g_L, g_R)
# ════════════════════════════════════════════════════════════════════
def test_Z1_per_species_couplings():
    """
    Direct algebraic check of the SM neutral-current per-species
    couplings against T_3 − Q sin²θ_W (left) and −Q sin²θ_W (right).

    For each of the 7 first-generation species (ν_L, e_L, u_L, d_L,
    e_R, u_R, d_R) at three different Weinberg angles, we compare
    z_couplings to the closed-form expression.

    Residual ≤ 1 ulp.
    """
    angles = [0.1, THETA_W_F45, 0.4916]
    max_res = 0.0
    rows = []
    for tW in angles:
        s2 = np.sin(tW) ** 2
        coup = z_couplings(tW)
        for sp in SPECIES:
            T3 = T3_TABLE[sp]
            Q  = Q_TABLE[sp]
            # left-handed → T3 − Q s²; right-handed → 0 (no L-current) on gL
            gL_expected = (T3 - Q * s2) if sp.endswith('_L') else 0.0
            gR_expected = -Q * s2
            r = max(abs(coup[sp]['gL'] - gL_expected),
                    abs(coup[sp]['gR'] - gR_expected))
            max_res = max(max_res, r)
            rows.append({
                'theta_W': float(tW), 'species': sp,
                'gL': coup[sp]['gL'], 'gR': coup[sp]['gR'],
                'gL_pred': gL_expected, 'gR_pred': gR_expected,
                'residual': r,
            })
    passed = bool(max_res <= 1e-15)
    return {
        'test': 'Z1', 'residual': float(max_res), 'target': 1e-15,
        'passed': passed, 'rows_count': len(rows),
        'description': f'per-species (gL,gR) match SM table at 3 angles, 7 species each: max|Δ| = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z2 — Source-basis identity (algebraic)
# ════════════════════════════════════════════════════════════════════
def test_Z2_source_basis_identity():
    """
    g · W^3 · J^3  +  g' · B · (J^em − J^3)
        =  e · A · J^em  +  g_Z · Z · (J^3 − s²_W · J^em)

    holds per site when (A, Z) come from weinberg_mix(W^3, B) and the
    couplings satisfy tan θ_W = g'/g (i.e. e = g s_W = g' c_W,
    g_Z = g/c_W).

    Cross-checked against fermion_neutral_current_per_species: the
    sum Σ_f (g_L^f ρ_L^f + g_R^f ρ_R^f) equals J^3 − s²_W J^em over
    the lattice, also per site.

    Both identities are bit-for-bit (algebraic).
    """
    # Pick θ_W and infer g' from g via the relation g' = g · tan θ_W
    g = 0.65
    sub_residuals = []

    for tW in [0.3, THETA_W_F45, 0.4916, 1.0]:
        gp = g * np.tan(tW)
        # Random gauge potentials and currents on the lattice
        W3_E = _rand_field()
        B_E  = _rand_field()
        J3   = _rand_field()
        Jem  = _rand_field()

        res_a = source_basis_identity_residual(
            W3_E, B_E, J3, Jem, g, gp, tW
        )
        sub_residuals.append(res_a)

    # Now the per-species cross-check.  Build random per-species densities
    # and verify both forms of the neutral current agree per site.
    densities = {sp: _rand_field() ** 2 + 0.1 for sp in SPECIES}
    for tW in [0.3, THETA_W_F45, 0.4916, 1.0]:
        Ja = fermion_neutral_current(densities, tW)
        Jb = fermion_neutral_current_per_species(densities, tW)
        # the per-species sum coincides with J^3 − s²_W J^em iff
        # for L-species we have g_L = T_3 − Q s²_W and the R-species
        # contribute via g_R = −Q s²_W; algebraically equivalent.
        res_b = float(np.max(np.abs(Ja - Jb)))
        sub_residuals.append(res_b)

    max_res = float(max(sub_residuals))
    passed = bool(max_res <= 1e-14)
    return {
        'test': 'Z2', 'residual': max_res, 'target': 1e-14,
        'sub_residuals': sub_residuals,
        'passed': passed,
        'description': f'source-basis identity (W3,B)↔(A,Z) and J^Z decomposition: max|Δ| = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z3 — Mass ratio m_Z = m_W / cos θ_W
# ════════════════════════════════════════════════════════════════════
def test_Z3_mass_ratio():
    """
    F35 W6.3 replayed via z_mass_from_w.  Should be bit-for-bit at any θ.
    """
    rows = []
    max_res = 0.0
    for tW in [0.1, THETA_W_F45, 0.4916, 1.0, 1.2]:
        for m_W in [0.1, 0.3, 0.5]:
            m_Z_helper = z_mass_from_w(m_W, tW)
            m_Z_closed = m_W / np.cos(tW)
            r = float(abs(m_Z_helper - m_Z_closed))
            max_res = max(max_res, r)
            rows.append({'theta_W': float(tW), 'm_W': m_W,
                         'm_Z': m_Z_helper, 'residual': r})
    passed = bool(max_res == 0.0)
    return {
        'test': 'Z3', 'residual': max_res, 'target': 0.0,
        'passed': passed,
        'description': f'm_Z = m_W/cos θ_W (5 angles × 3 masses): max|Δ| = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z4 — Free massless Z propagation dispersion
# ════════════════════════════════════════════════════════════════════
def test_Z4_free_dispersion():
    """
    Evolve a random (E_Z, B_Z) for n_steps under z_propagation_step_spectral
    and verify the final Fourier amplitudes match the F26 even-dispersion
    prediction
        C_n(k) = C_0(k) · exp(−i · Ω_even(k) · n_steps)
    where C = E_k + i B_k.

    This is the photon dispersion (W6.2 / W6.5) — Z inherits it as a real
    linear combination of W^3 and B.
    """
    n_steps = 40
    E = _rand_field(); B = _rand_field()
    KX, KY, KZ = _kgrid3d(L, L, L)
    E0_k = _fft.fftn(E)
    B0_k = _fft.fftn(B)
    C0 = E0_k + 1j * B0_k

    Ec, Bc = E.copy(), B.copy()
    for _ in range(n_steps):
        Ec, Bc = z_propagation_step_spectral(Ec, Bc)

    En_k = _fft.fftn(Ec)
    Bn_k = _fft.fftn(Bc)
    Cn = En_k + 1j * Bn_k

    omega_p = bcc_dispersion(KX/2, KY/2, KZ/2, sign='+')
    omega_m = bcc_dispersion(KX/2, KY/2, KZ/2, sign='-')
    Omega_even = omega_p + omega_m
    C_expected = C0 * np.exp(-1j * Omega_even * n_steps)

    amp0 = np.abs(C0)
    sig = amp0 > 1e-8 * np.max(amp0)
    rel = np.where(sig, np.abs(Cn - C_expected) / (amp0 + 1e-30), 0.0)
    res = float(np.max(rel))
    passed = bool(res <= 1e-12)
    return {
        'test': 'Z4', 'residual': res, 'target': 1e-12,
        'n_steps': n_steps, 'passed': passed,
        'description': f'free massless Z dispersion = Ω_even(k) over {n_steps} ticks: max rel err = {res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z5 — Massive Proca dispersion
# ════════════════════════════════════════════════════════════════════
def test_Z5_proca_dispersion():
    """
    z_massive_propagation_step_spectral evolves at
        ω_eff(k) = sqrt(m_Z² + Ω_even²(k))
    Verify by Fourier-mode comparison after n_steps for several m_Z.
    """
    n_steps = 30
    KX, KY, KZ = _kgrid3d(L, L, L)
    omega_p = bcc_dispersion(KX/2, KY/2, KZ/2, sign='+')
    omega_m = bcc_dispersion(KX/2, KY/2, KZ/2, sign='-')
    Omega_even = omega_p + omega_m

    rels = {}
    max_res = 0.0
    for m_Z in [0.0, 0.1, 0.3, 0.5]:
        E = _rand_field(); B = _rand_field()
        E0_k = _fft.fftn(E); B0_k = _fft.fftn(B)
        C0 = E0_k + 1j * B0_k
        Ec, Bc = E.copy(), B.copy()
        for _ in range(n_steps):
            Ec, Bc = z_massive_propagation_step_spectral(Ec, Bc, m_Z)
        En_k = _fft.fftn(Ec); Bn_k = _fft.fftn(Bc)
        Cn = En_k + 1j * Bn_k
        omega_eff = np.sqrt(m_Z**2 + Omega_even**2)
        C_expected = C0 * np.exp(-1j * omega_eff * n_steps)
        amp0 = np.abs(C0)
        sig = amp0 > 1e-8 * np.max(amp0)
        rel = float(np.max(np.where(sig,
            np.abs(Cn - C_expected) / (amp0 + 1e-30), 0.0)))
        rels[f'mZ={m_Z}'] = rel
        max_res = max(max_res, rel)
    passed = bool(max_res <= 1e-12)
    return {
        'test': 'Z5', 'residual': max_res, 'target': 1e-12,
        'rels_by_mZ': rels, 'passed': passed,
        'description': f'massive Z (Proca) ω²=m²+Ω_even² over {n_steps} ticks at 4 masses: max rel = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z6 — Mixing/propagation commutation, with Z mass set by F35
# ════════════════════════════════════════════════════════════════════
def test_Z6_mixing_propagation_commute():
    """
    Initialize random (W^3, B).  Two paths:

    PATH A:  propagate W^3 (massless even rotation) and B independently,
             then weinberg_mix → (A', Z') after n_steps.
    PATH B:  weinberg_mix at t=0 → (A, Z); propagate A under the photon
             rotation (massless even) and Z under z_propagation_step
             (massless even).  After n_steps → (A'', Z'').

    A' = A''  and  Z' = Z''  to FFT floor.  This confirms that the
    F35 mixing rotation commutes with the dynamical Z propagation in
    the massless limit.  (Mass enters only through the mass-eigenstate
    propagator; mixing the gauge potentials before or after a massless
    rotation is the same operation.)
    """
    n_steps = 25
    W3_E = _rand_field(); W3_B = _rand_field()
    B_E  = _rand_field(); B_B  = _rand_field()
    tW = THETA_W_F45

    # PATH A: propagate gauge basis (each with even dispersion), then mix
    Wa_E, Wa_B = W3_E.copy(), W3_B.copy()
    Ba_E, Ba_B = B_E.copy(),  B_B.copy()
    for _ in range(n_steps):
        Wa_E, Wa_B = z_propagation_step_spectral(Wa_E, Wa_B)  # W^3 propagates like Z (real even)
        Ba_E, Ba_B = z_propagation_step_spectral(Ba_E, Ba_B)  # B propagates like A
    Aa_E, Aa_B, Za_E, Za_B = weinberg_mix(Wa_E, Wa_B, Ba_E, Ba_B, tW)

    # PATH B: mix at t=0, then propagate the mass eigenstates
    Ab_E, Ab_B, Zb_E, Zb_B = weinberg_mix(W3_E, W3_B, B_E, B_B, tW)
    for _ in range(n_steps):
        Ab_E, Ab_B = z_propagation_step_spectral(Ab_E, Ab_B)
        Zb_E, Zb_B = z_propagation_step_spectral(Zb_E, Zb_B)

    res = float(max(
        np.max(np.abs(Aa_E - Ab_E)), np.max(np.abs(Aa_B - Ab_B)),
        np.max(np.abs(Za_E - Zb_E)), np.max(np.abs(Za_B - Zb_B)),
    ))
    passed = bool(res <= 1e-12)
    return {
        'test': 'Z6', 'residual': res, 'target': 1e-12,
        'n_steps': n_steps, 'passed': passed,
        'description': f'[mix, z_propagate] = 0 over {n_steps} ticks at θ_W=π/6: max|Δ| = {res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z7 — Source kick is bit-for-bit additive
# ════════════════════════════════════════════════════════════════════
def test_Z7_source_kick_additive():
    """
    z_sourced_propagation_step Strang-splits as (free Proca rotation,
    then real-space source kick).  Therefore

        E_Z_sourced(t+1) − E_Z_free(t+1) = g_Z · J_Z · dt   exactly

    on a per-site basis, and B is unchanged by the kick.  Bit-for-bit
    test across two masses and two dt values.
    """
    densities = {sp: 0.1 + _rand_field()**2 for sp in SPECIES}
    tW = THETA_W_F45
    g = 0.65
    g_Z = z_coupling_strength(g, tW)
    J_Z = fermion_neutral_current(densities, tW)

    sub_residuals = []
    for m_Z in [0.0, 0.4]:
        for dt in [1.0, 0.5]:
            E, B = make_z_field(L, mode='random', seed=7)
            # free Proca evolution
            if m_Z == 0.0:
                E_free, B_free = z_propagation_step_spectral(E, B)
            else:
                E_free, B_free = z_massive_propagation_step_spectral(E, B, m_Z, dt)
            # sourced evolution
            E_src, B_src = z_sourced_propagation_step(E, B, J_Z, g_Z=g_Z,
                                                       dt=dt, m_Z=m_Z)
            # bit-for-bit additive in E, no change in B
            r_E = float(np.max(np.abs((E_src - E_free) - g_Z * J_Z * dt)))
            r_B = float(np.max(np.abs(B_src - B_free)))
            sub_residuals.append(r_E)
            sub_residuals.append(r_B)
    max_res = max(sub_residuals)
    # Algebraically the kick is exact, but float addition (A+B)-A loses
    # ~|B|·ε in cancellation; target = machine ε.
    passed = bool(max_res <= 1e-14)
    return {
        'test': 'Z7', 'residual': max_res, 'target': 1e-14,
        'sub_residuals': sub_residuals, 'passed': passed,
        'description': f'source kick additive in E, B unchanged, 2 masses × 2 dt: max|Δ| = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z8 — Neutrino Z coupling is θ_W-independent
# ════════════════════════════════════════════════════════════════════
def test_Z8_neutrino_no_theta_dependence():
    """
    Because Q_ν = 0, the SM formula g_L^ν = T_3^ν − Q^ν sin²θ_W reduces
    to g_L^ν = T_3^ν = +1/2 for any θ_W.  And g_R^ν = 0 always (no ν_R
    in the minimal model).

    Verify across many θ_W that z_couplings('nu_L') is constant.
    """
    angles = np.linspace(0.01, np.pi/2 - 0.01, 20)
    deviations = []
    for tW in angles:
        c = z_couplings(float(tW))['nu_L']
        deviations.append((c['gL'] - 0.5, c['gR'] - 0.0,
                           c['gV'] - 0.5, c['gA'] - 0.5))
    max_res = float(max(max(abs(d[i]) for i in range(4)) for d in deviations))
    passed = bool(max_res == 0.0)
    return {
        'test': 'Z8', 'residual': max_res, 'target': 0.0,
        'n_angles': len(angles), 'passed': passed,
        'description': f'ν_L Z coupling (gL,gR,gV,gA)=(1/2,0,1/2,1/2) ∀θ_W: max|Δ| = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z9 — Photon-neutrino coupling is zero
# ════════════════════════════════════════════════════════════════════
def test_Z9_photon_neutrino_zero():
    """
    The electromagnetic current evaluated on a neutrino-only density is
    identically zero (Q_ν = 0).  Bit-for-bit.
    """
    densities = {sp: _rand_field()**2 for sp in SPECIES}
    # Strip everyone except ν
    nu_only = {'nu_L': densities['nu_L']}
    Jem = fermion_em_current(nu_only)
    res = float(np.max(np.abs(Jem)))
    passed = bool(res == 0.0)
    return {
        'test': 'Z9', 'residual': res, 'target': 0.0, 'passed': passed,
        'description': f'photon does not couple to ν (J^em on ν density): max|Δ| = {res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z10 — (g_V, g_A) decomposition
# ════════════════════════════════════════════════════════════════════
def test_Z10_vector_axial():
    """
    SM vector / axial neutral-current couplings.  For each species:
        g_V^f = T_3^f − 2 Q^f sin²θ_W
        g_A^f = T_3^f          (R species: T_3 = 0)

    Bit-for-bit at multiple angles.
    """
    angles = [0.1, THETA_W_F45, 0.4916, 1.0]
    rows = []
    max_res = 0.0
    for tW in angles:
        s2 = np.sin(tW)**2
        coup = z_couplings(tW)
        for sp in SPECIES:
            T3 = T3_TABLE[sp]; Q = Q_TABLE[sp]
            if sp.endswith('_L'):
                gV_pred = T3 - 2 * Q * s2
                gA_pred = T3
            else:  # right-handed: gL=0 so gV=gR, gA=-gR
                gV_pred = -Q * s2
                gA_pred = +Q * s2
            r = max(abs(coup[sp]['gV'] - gV_pred),
                    abs(coup[sp]['gA'] - gA_pred))
            max_res = max(max_res, r)
            rows.append({'theta_W': float(tW), 'species': sp,
                         'gV': coup[sp]['gV'], 'gA': coup[sp]['gA'],
                         'gV_pred': gV_pred, 'gA_pred': gA_pred,
                         'residual': r})
    passed = bool(max_res <= 1e-15)
    return {
        'test': 'Z10', 'residual': float(max_res), 'target': 1e-15,
        'rows_count': len(rows), 'passed': passed,
        'description': f'(gV,gA) match SM formula, 4 angles × 7 species: max|Δ| = {max_res:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Z11 — F45 bare-angle: electron Z vector coupling vanishes
# ════════════════════════════════════════════════════════════════════
def test_Z11_F45_electron_gV_vanishes():
    """
    At F45 bare angle sin²θ_W = 1/4:

        g_V^e_L = -1/2 − 2(-1)(1/4) = 0       <-- vanishes!
        g_V^ν   = +1/2
        g_V^u_L = +1/2 − 2(2/3)(1/4) = 1/6
        g_V^d_L = -1/2 − 2(-1/3)(1/4) = -1/3

    These are bit-for-bit at sin²θ_W = 1/4 because the rational
    arithmetic closes exactly in float64.  Counter-check at the W6.3
    angle 0.4916 rad (sin²θ_W ≈ 0.231): g_V^e_L should be ≈ −0.038,
    visibly non-zero — i.e. the vanishing at F45 is a non-trivial
    prediction, not a generic feature.
    """
    tW = THETA_W_F45
    s2 = np.sin(tW) ** 2
    s2_resid = abs(s2 - 0.25)

    coup = z_couplings(tW)
    gV_e = coup['e_L']['gV']
    gV_nu = coup['nu_L']['gV']
    gV_u = coup['u_L']['gV']
    gV_d = coup['d_L']['gV']

    # F45 predictions
    pred = {'e_L': 0.0, 'nu_L': 0.5, 'u_L': 1.0/6.0, 'd_L': -1.0/3.0}
    residuals = {
        'sin2theta_W - 1/4': s2_resid,
        'gV^e_L (should be 0)': abs(gV_e - pred['e_L']),
        'gV^nu_L (should be 1/2)': abs(gV_nu - pred['nu_L']),
        'gV^u_L (should be 1/6)': abs(gV_u - pred['u_L']),
        'gV^d_L (should be -1/3)': abs(gV_d - pred['d_L']),
    }
    max_res = float(max(residuals.values()))

    # Sanity counter-check: at the W6.3 angle 0.4916 rad, gV^e_L is NOT zero
    counter_coup = z_couplings(0.4916)
    gV_e_counter = counter_coup['e_L']['gV']
    counter_passes = abs(gV_e_counter) > 1e-3  # visibly non-zero

    passed = bool(max_res <= 1e-15 and counter_passes)
    return {
        'test': 'Z11', 'residual': max_res, 'target': 1e-15,
        'residuals': residuals,
        'gV^e_L at F45 (π/6)': gV_e,
        'gV^e_L at W6.3 (0.4916 rad)': gV_e_counter,
        'counter_check_visibly_nonzero': counter_passes,
        'passed': passed,
        'description': f'F45 prediction: g_V^e_L = 0 at sin²θ_W = 1/4 exact; nonzero at PDG angle',
    }


# ════════════════════════════════════════════════════════════════════
# Z12 — Massless Proca reduces to massless step
# ════════════════════════════════════════════════════════════════════
def test_Z12_proca_zero_mass_reduction():
    """
    z_massive_propagation_step_spectral(…, m_Z=0, dt=1) reduces
    bit-for-bit to z_propagation_step_spectral on the same field.
    Pure code-equivalence check.
    """
    E = _rand_field(); B = _rand_field()
    E1, B1 = z_propagation_step_spectral(E, B)
    E2, B2 = z_massive_propagation_step_spectral(E, B, m_Z=0.0, dt=1.0)
    r = float(max(np.max(np.abs(E1 - E2)), np.max(np.abs(B1 - B2))))
    passed = bool(r == 0.0)
    return {
        'test': 'Z12', 'residual': r, 'target': 0.0, 'passed': passed,
        'description': f'massive step at m_Z=0 reduces bit-for-bit to massless step: max|Δ| = {r:.2e}',
    }


# ════════════════════════════════════════════════════════════════════
# Runner
# ════════════════════════════════════════════════════════════════════
def run_all():
    tests = [
        test_Z1_per_species_couplings,
        test_Z2_source_basis_identity,
        test_Z3_mass_ratio,
        test_Z4_free_dispersion,
        test_Z5_proca_dispersion,
        test_Z6_mixing_propagation_commute,
        test_Z7_source_kick_additive,
        test_Z8_neutrino_no_theta_dependence,
        test_Z9_photon_neutrino_zero,
        test_Z10_vector_axial,
        test_Z11_F45_electron_gV_vanishes,
        test_Z12_proca_zero_mass_reduction,
    ]
    results = []
    t0 = time.time()
    for fn in tests:
        r = fn()
        status = 'PASS' if r['passed'] else 'FAIL'
        print(f"  [{status}] {r['test']:4s}  residual={r['residual']:.3e}  "
              f"target={r['target']:.0e}  {r['description']}")
        results.append(r)
    elapsed = time.time() - t0
    n_pass = sum(r['passed'] for r in results)
    overall = 'PASS' if n_pass == len(results) else 'FAIL'
    print(f"\n  OVERALL: {overall}  ({n_pass}/{len(results)} PASS, {elapsed:.2f}s)")

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'FG4_dynamical_Z.json')
    with open(out_path, 'w') as fh:
        json.dump({'test_suite': 'FG4_dynamical_Z',
                   'results': results,
                   'elapsed': elapsed,
                   'n_pass': int(n_pass),
                   'n_total': len(results),
                   'overall': overall}, fh, indent=2, cls=_NumpyEncoder)
    print(f"  Results -> {out_path}")
    return results


if __name__ == '__main__':
    print("FG-4 — Dynamical Z neutral-current sector")
    print("=" * 60)
    run_all()
