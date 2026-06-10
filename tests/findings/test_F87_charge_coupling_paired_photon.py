"""
test_F87_charge_coupling_paired_photon.py
=========================================

End-to-end re-verification of the U(1) charge-coupling path on the **paired
photon** (`ca_photon_pair.py`), the field that replaced the SM-style U(1)-gauge
photon whose `aharonov_bohm_test` driver was removed from `ca_dirac.py` in May.

The charge-coupling path is two coupled halves, verified together here:

  AB  — Aharonov–Bohm holonomy.  The U(1) coupling is the Peierls c-number phase
        P = e^{i q A·dl} I_2 (F68: identity channel).  The loop holonomy is the
        discrete Stokes theorem  W = exp(i q ∮A·dl) = exp(i q Φ_enc), exact on
        the lattice; a charged fermion encircling a flux tube picks up q·Φ_enc on
        a field-free path, identically for either helicity (charge couples, spin
        does not).

  MX  — Sourced Maxwell curl.  The paired photon's curl generator is C(k)=2 n(k/2)
        (odd part, real-field).  Minimal coupling adds the charge current to
        Ampère:  Ė = i C×B − J,  Ḃ = −i C×E.  Because C·(C×x) ≡ 0, the Gauss
        constraint i C·E = ρ is preserved bit-for-bit under charge continuity
        ∂_tρ = −i C·J: electric charge is conserved by the coupling.

  E2E — the two halves on ONE field: a static current sources B_z by the discrete
        magnetostatic curl, and the holonomy of the Coulomb-gauge A solved from
        that same B returns q·(current-driven flux).  charge → field → phase.

Tiers:  [machine] = FFT/round-off floor;  [exact] = algebraic identity (e.g.
discrete Stokes, charge linearity over ℚ);  [quant] = quantitative match.

Run:  python tests/findings/test_F87_charge_coupling_paired_photon.py
Writes test-results/F87_charge_coupling_paired_photon.json
"""

import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ca-simulation'))

import numpy as np
import ca_charge_coupling as cc
from ca_lattice import make_kgrid_3d
from ca_bcc import bcc_unitary, _bcc_uvec, bcc_dispersion

ROOT3 = np.sqrt(3.0)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)


# ======================================================================
#  Block AB — Aharonov–Bohm holonomy on the paired-photon (E,B)
# ======================================================================
# Compact, well-separated tube pair so Gaussian tails are below the round-off
# floor (width 1.5 ⇒ tail at the loop edges ~e^{-50} ≈ 1e-22): then loop flux is
# the full ±Φ and path-independence / net-zero become genuinely machine-exact.
_ABL = 96
_AB_C1 = (24, 48)
_AB_C2 = (72, 48)
_AB_W = 1.5


def _ab_field(Phi=0.7):
    Bz = cc.make_flux_tube_pair(_ABL, _AB_C1, _AB_C2, width=_AB_W, Phi=Phi)
    Ax, Ay = cc.solve_A_coulomb_2d(Bz)
    return Bz, Ax, Ay


def ab1_coulomb_gauge_exists():
    """A from a flux-tube pair: discrete curl(A)=B and discrete div(A)=0, both
    machine-exact -> the Coulomb-gauge vector potential of the paired-photon B
    field exists on the lattice."""
    Bz, Ax, Ay = _ab_field()
    curl_res = float(np.max(np.abs(cc.discrete_curl_z(Ax, Ay) - Bz)))
    div_res = float(np.max(np.abs(cc.discrete_div(Ax, Ay))))
    return {'curl_minus_B_max': curl_res, 'div_A_max': div_res,
            'tier': 'machine'}


def ab2_holonomy_is_stokes():
    """Loop holonomy = q·enclosed flux (discrete Stokes), path-independent, and
    zero for loops enclosing no net flux."""
    Bz, Ax, Ay = _ab_field()
    # loop A: encloses tube1 only
    hA = cc.peierls_loop_phase(Ax, Ay, 8, 48, 8, 88, q=1.0)
    fA = cc.enclosed_flux(Bz, 8, 48, 8, 88, q=1.0)
    # loop B: a DIFFERENT rectangle also enclosing only tube1
    hB = cc.peierls_loop_phase(Ax, Ay, 12, 44, 16, 80, q=1.0)
    fB = cc.enclosed_flux(Bz, 12, 44, 16, 80, q=1.0)
    # loop C: encloses BOTH tubes -> net flux 0
    hC = cc.peierls_loop_phase(Ax, Ay, 8, 88, 8, 88, q=1.0)
    # loop D: encloses NEITHER tube (corner region)
    hD = cc.peierls_loop_phase(Ax, Ay, 2, 16, 2, 16, q=1.0)
    return {
        'holo_minus_flux_loopA': float(abs(hA - fA)),          # discrete Stokes
        'holo_minus_flux_loopB': float(abs(hB - fB)),
        'path_independence_A_vs_B': float(abs(hA - hB)),        # same enclosed flux
        'holo_both_tubes_netzero': float(abs(hC)),
        'holo_no_tube': float(abs(hD)),
        'holo_value': float(hA),
        'tier': 'exact/machine'}


def ab3_field_free_path():
    """The Aharonov–Bohm signature: the encircling path is (essentially) field
    free, |B|_path ≪ |B|_peak, yet the holonomy is non-zero = q·Φ_enc."""
    L = 64
    Bz = cc.make_flux_tube_pair(L, (32, 32), (10, 10), width=1.6, Phi=1.0)
    Ax, Ay = cc.solve_A_coulomb_2d(Bz)
    holo = cc.peierls_loop_phase(Ax, Ay, 22, 43, 22, 43, q=1.0)
    flux = cc.enclosed_flux(Bz, 22, 43, 22, 43, q=1.0)
    peak = float(np.abs(Bz).max())
    on_path = cc.field_on_loop(Bz, 22, 43, 22, 43)
    return {'holo': float(holo), 'flux': float(flux),
            'peak_B': peak, 'field_on_path': on_path,
            'path_to_peak_ratio': on_path / peak, 'tier': 'quant'}


def ab4_helicity_blind():
    """F68 end-to-end: the holonomy operator P = e^{iqΦ} I_2 acts identically on
    + and − Weyl spinors (charge couples, spin does not); and [P, U^±(k)] = 0
    over sampled k (the c-number phase commutes with both Weyl branches).

    The applied phase on a spinor ψ is arg⟨ψ|P|ψ⟩ (basis- and wrap-robust); for
    P = e^{iΦ}I it equals Φ for every ψ, so the +helicity and −helicity applied
    phases are identical — the helicity 'split' is 0."""
    Phi = 0.7
    P = np.exp(1j * Phi) * I2
    rng = np.random.default_rng(3)
    splits = []
    comms = []
    for _ in range(200):
        k = rng.standard_normal(3) * 1.5
        applied = {}
        for sign in ('+', '-'):
            _, nx, ny, nz = _bcc_uvec(*k, sign=sign)
            nm = np.sqrt(nx*nx + ny*ny + nz*nz) + 1e-30
            nds = (nx*SX + ny*SY + nz*SZ) / nm
            w, V = np.linalg.eigh(nds)            # 2x2 Hermitian (NOT a chiral op)
            psi = V[:, -1]                        # +helicity eigenvector of n·σ
            applied[sign] = np.angle(np.vdot(psi, P @ psi))   # = Φ for any ψ
            a, b, c, d = bcc_unitary(*k, sign=sign)
            U = np.array([[a, b], [c, d]], complex)
            comms.append(np.max(np.abs(P @ U - U @ P)))
        splits.append(abs(applied['+'] - applied['-']))
    return {'max_helicity_phase_split': float(max(splits)),
            'max_commutator_P_U': float(max(comms)), 'tier': 'machine'}


def ab5_charge_linearity():
    """Holonomy is exactly linear in the charge q (q=1,2,3 → 1×,2×,3× the
    flux), an exact rational scaling — the coupling is genuinely q·∮A·dl."""
    Bz, Ax, Ay = _ab_field(Phi=0.5)
    h1 = cc.peierls_loop_phase(Ax, Ay, 8, 48, 8, 88, q=1.0)
    h2 = cc.peierls_loop_phase(Ax, Ay, 8, 48, 8, 88, q=2.0)
    h3 = cc.peierls_loop_phase(Ax, Ay, 8, 48, 8, 88, q=3.0)
    return {'q2_minus_2q1': float(abs(h2 - 2*h1)),
            'q3_minus_3q1': float(abs(h3 - 3*h1)), 'tier': 'exact'}


# ======================================================================
#  Block MX — sourced Maxwell curl on the paired photon
# ======================================================================
def mx1_luminal_curl_rate():
    """The curl generator's magnitude |C(k)| → |k|/√3 at small k: the sourced
    curl propagates at the paired-photon light speed c_lat = 1/√3."""
    h = 1e-5
    errs = []
    rng = np.random.default_rng(5)
    for _ in range(12):
        n = rng.standard_normal(3); n /= np.linalg.norm(n)
        # |C_odd| at k = h n
        kx, ky, kz = h * n
        up, nxp, nyp, nzp = _bcc_uvec(kx/2, ky/2, kz/2, sign='+')
        um, nxm, nym, nzm = _bcc_uvec(-kx/2, -ky/2, -kz/2, sign='+')
        Cmag = np.sqrt((nxp-nxm)**2 + (nyp-nym)**2 + (nzp-nzm)**2)
        errs.append(abs(Cmag/h - 1.0/ROOT3))
    return {'max_err_C_over_k_vs_inv_sqrt3': float(max(errs)),
            'c_lat': 1.0/ROOT3, 'tier': 'quant'}


def mx2_curl_sources_no_charge():
    """The identity C·(C×B) ≡ 0 over random modes — the curl term contributes
    nothing to ∇·E, so it cannot create or destroy charge."""
    L = 17
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = cc.bcc_curl_symbol(KX, KY, KZ)
    rng = np.random.default_rng(7)
    B = [rng.standard_normal((L, L, L)) for _ in range(3)]
    cxB = cc._cross_k(Cx, Cy, Cz, *B)
    ident = cc._dot_k(Cx, Cy, Cz, *cxB)
    return {'max_C_dot_C_cross_B': float(np.abs(ident).max()), 'tier': 'machine'}


def mx3_charge_conservation_dynamical():
    """Electric charge conservation: evolve the sourced curl stepper N ticks with
    a source J and a co-evolving ρ obeying continuity ∂_tρ = −i C·J; the Gauss
    residual i C·E − ρ stays at the round-off floor."""
    L = 17
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = cc.bcc_curl_symbol(KX, KY, KZ)
    rng = np.random.default_rng(9)
    E = np.array([rng.standard_normal((L, L, L)) for _ in range(3)]) * 0.1
    B = np.array([rng.standard_normal((L, L, L)) for _ in range(3)]) * 0.1
    Ek = [np.fft.fftn(E[a]) for a in range(3)]
    rho_k = 1j * cc._dot_k(Cx, Cy, Cz, *Ek)            # Gauss holds at t0
    J = np.array([rng.standard_normal((L, L, L)) for _ in range(3)]) * 0.05
    dt = 0.1
    maxres = 0.0
    for _ in range(100):
        E, B = cc.maxwell_curl_step(E, B, J=J, dt=dt)
        Jk = [np.fft.fftn(J[a]) for a in range(3)]
        rho_k = rho_k - dt * (1j * cc._dot_k(Cx, Cy, Cz, *Jk))
        Ek = [np.fft.fftn(E[a]) for a in range(3)]
        g = 1j * cc._dot_k(Cx, Cy, Cz, *Ek) - rho_k
        maxres = max(maxres, float(np.abs(g).max()))
    return {'gauss_residual_max_100steps': maxres, 'tier': 'machine'}


def mx4_magnetic_gauss():
    """∇·B = 0 (i C·B) preserved under the sourced evolution."""
    L = 17
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = cc.bcc_curl_symbol(KX, KY, KZ)
    rng = np.random.default_rng(11)
    E = np.array([rng.standard_normal((L, L, L)) for _ in range(3)]) * 0.1
    # start from a divergence-free B (B = curl of something): use magnetostatic_B
    J = np.zeros((3, L, L, L))
    xs = np.arange(L); X, Y, Z = np.meshgrid(xs, xs, xs, indexing='ij')
    dx = X - L/2.0; dy = Y - L/2.0
    g = np.exp(-(dx**2 + dy**2) / (2*4.0**2))
    J[0] = -dy*g; J[1] = dx*g
    B, _ = cc.magnetostatic_B(J)
    maxdiv = 0.0
    for _ in range(50):
        E, B = cc.maxwell_curl_step(E, B, J=None, dt=0.1)
        Bk = [np.fft.fftn(B[a]) for a in range(3)]
        maxdiv = max(maxdiv, float(np.abs(1j*cc._dot_k(Cx, Cy, Cz, *Bk)).max()))
    return {'magnetic_gauss_max_50steps': maxdiv, 'tier': 'machine'}


def mx5_magnetostatics():
    """A steady current sources a magnetostatic B with a machine-exact Ampère
    residual i C×B = J_T on the resolved sector (|C|>tol); reports the
    longitudinal fraction the BCC chirality projects out."""
    L = 17
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = cc.bcc_curl_symbol(KX, KY, KZ)
    xs = np.arange(L); X, Y, Z = np.meshgrid(xs, xs, xs, indexing='ij')
    dx = X - L/2.0; dy = Y - L/2.0
    g = np.exp(-(dx**2 + dy**2) / (2*4.0**2))
    J = np.zeros((3, L, L, L)); J[0] = -dy*g; J[1] = dx*g
    B, lon = cc.magnetostatic_B(J)
    Bk = [np.fft.fftn(B[a]) for a in range(3)]
    cxB = cc._cross_k(Cx, Cy, Cz, *Bk)
    Jk = [np.fft.fftn(J[a]) for a in range(3)]
    C2 = Cx**2 + Cy**2 + Cz**2
    CdotJ = cc._dot_k(Cx, Cy, Cz, *Jk)
    mask = C2 > 1e-6
    JT = [Jk[a] - np.where(mask, (Cx, Cy, Cz)[a]*CdotJ/np.where(mask, C2, 1.0), 0.0)
          for a in range(3)]
    amp = [1j*cxB[a] - JT[a] for a in range(3)]
    num = np.sqrt(sum(np.sum((np.abs(amp[a])**2)[mask]) for a in range(3)))
    den = np.sqrt(sum(np.sum((np.abs(JT[a])**2)[mask]) for a in range(3)))
    return {'ampere_residual_resolved': float(num/den),
            'longitudinal_fraction': float(lon), 'tier': 'machine/quant'}


# ======================================================================
#  Block E2E — charge -> field -> A -> holonomy, on one field
# ======================================================================
def e2e_charge_to_phase():
    """A static in-plane current sources B_z by the discrete magnetostatic curl;
    the holonomy of the Coulomb-gauge A solved from that SAME B returns
    q·(current-driven flux) to machine precision.  The whole charge-coupling
    loop closes on one paired-photon field."""
    L = 96
    Bz, Ax, Ay = cc.sourced_flux_tube_2d(L, (24, 48), (72, 48),
                                         radius=4.0, current=1.0)
    curl_res = float(np.max(np.abs(cc.discrete_curl_z(Ax, Ay) - Bz)))
    # Ampère self-consistency: the wall current J = ∇×B reproduces ∇×B
    Jx, Jy = cc.ampere_current_2d(Bz)
    curlB_x = Bz - np.roll(Bz, 1, axis=1)            # (∇×B)_x = ∂_y B_z (bwd)
    curlB_y = -(Bz - np.roll(Bz, 1, axis=0))
    ampere_res = float(np.max(np.abs(curlB_x - Jx)) + np.max(np.abs(curlB_y - Jy)))
    holo = cc.peierls_loop_phase(Ax, Ay, 8, 48, 8, 88, q=1.0)
    flux = cc.enclosed_flux(Bz, 8, 48, 8, 88, q=1.0)
    peak = float(np.abs(Bz).max())
    on_path = cc.field_on_loop(Bz, 8, 48, 8, 88)
    return {'curl_minus_B_max': curl_res,
            'ampere_curlB_minus_J': ampere_res,
            'holo_minus_flux': float(abs(holo - flux)),
            'holo_value': float(holo),
            'enclosed_flux': float(flux),
            'field_on_path_ratio': on_path / peak, 'tier': 'machine'}


# ======================================================================
def main():
    t0 = time.time()
    res = {
        'AB1_coulomb_gauge': ab1_coulomb_gauge_exists(),
        'AB2_holonomy_stokes': ab2_holonomy_is_stokes(),
        'AB3_field_free_path': ab3_field_free_path(),
        'AB4_helicity_blind': ab4_helicity_blind(),
        'AB5_charge_linearity': ab5_charge_linearity(),
        'MX1_luminal_curl': mx1_luminal_curl_rate(),
        'MX2_curl_no_charge': mx2_curl_sources_no_charge(),
        'MX3_charge_conservation': mx3_charge_conservation_dynamical(),
        'MX4_magnetic_gauss': mx4_magnetic_gauss(),
        'MX5_magnetostatics': mx5_magnetostatics(),
        'E2E_charge_to_phase': e2e_charge_to_phase(),
    }

    # ---- PASS/FAIL gating ----
    checks = []
    def chk(name, cond, val):
        checks.append((name, bool(cond), val))

    a1 = res['AB1_coulomb_gauge']
    chk('AB1 curl(A)=B', a1['curl_minus_B_max'] < 1e-12, a1['curl_minus_B_max'])
    chk('AB1 div(A)=0', a1['div_A_max'] < 1e-12, a1['div_A_max'])
    a2 = res['AB2_holonomy_stokes']
    chk('AB2 holonomy=flux (Stokes)', a2['holo_minus_flux_loopA'] < 1e-12, a2['holo_minus_flux_loopA'])
    chk('AB2 path independence', a2['path_independence_A_vs_B'] < 1e-10, a2['path_independence_A_vs_B'])
    chk('AB2 both-tubes loop ~0', a2['holo_both_tubes_netzero'] < 1e-10, a2['holo_both_tubes_netzero'])
    chk('AB2 no-tube loop ~0', a2['holo_no_tube'] < 1e-3, a2['holo_no_tube'])
    a3 = res['AB3_field_free_path']
    chk('AB3 field-free path (<5%)', a3['path_to_peak_ratio'] < 0.05, a3['path_to_peak_ratio'])
    chk('AB3 holonomy nonzero', abs(a3['holo']) > 0.1, a3['holo'])
    a4 = res['AB4_helicity_blind']
    chk('AB4 helicity split=0', a4['max_helicity_phase_split'] < 1e-12, a4['max_helicity_phase_split'])
    chk('AB4 [P,U]=0', a4['max_commutator_P_U'] < 1e-12, a4['max_commutator_P_U'])
    a5 = res['AB5_charge_linearity']
    chk('AB5 q-linearity', max(a5['q2_minus_2q1'], a5['q3_minus_3q1']) < 1e-12,
        max(a5['q2_minus_2q1'], a5['q3_minus_3q1']))
    m1 = res['MX1_luminal_curl']
    chk('MX1 |C|/k -> 1/sqrt3', m1['max_err_C_over_k_vs_inv_sqrt3'] < 1e-3, m1['max_err_C_over_k_vs_inv_sqrt3'])
    m2 = res['MX2_curl_no_charge']
    chk('MX2 C.(CxB)=0', m2['max_C_dot_C_cross_B'] < 1e-10, m2['max_C_dot_C_cross_B'])
    m3 = res['MX3_charge_conservation']
    chk('MX3 Gauss conserved 100 steps', m3['gauss_residual_max_100steps'] < 1e-9, m3['gauss_residual_max_100steps'])
    m4 = res['MX4_magnetic_gauss']
    chk('MX4 div B=0', m4['magnetic_gauss_max_50steps'] < 1e-9, m4['magnetic_gauss_max_50steps'])
    m5 = res['MX5_magnetostatics']
    chk('MX5 Ampere residual (resolved)', m5['ampere_residual_resolved'] < 1e-10, m5['ampere_residual_resolved'])
    e2 = res['E2E_charge_to_phase']
    chk('E2E curl(A)=B', e2['curl_minus_B_max'] < 1e-12, e2['curl_minus_B_max'])
    chk('E2E Ampere ∇×B=J', e2['ampere_curlB_minus_J'] < 1e-12, e2['ampere_curlB_minus_J'])
    chk('E2E holonomy=flux', e2['holo_minus_flux'] < 1e-12, e2['holo_minus_flux'])
    chk('E2E flux nonzero', abs(e2['enclosed_flux']) > 0.5, e2['enclosed_flux'])

    npass = sum(1 for _, ok, _ in checks if ok)
    ntot = len(checks)

    print("=" * 74)
    print("F87 — charge-coupling path re-verified end-to-end on the PAIRED PHOTON")
    print("=" * 74)
    print("\n--- AB: Aharonov–Bohm holonomy (Peierls phase on the (E,B) field) ---")
    print(f"  AB1  discrete curl(A)-B = {a1['curl_minus_B_max']:.2e}   div(A) = {a1['div_A_max']:.2e}")
    print(f"  AB2  holonomy - flux (discrete Stokes) = {a2['holo_minus_flux_loopA']:.2e}")
    print(f"       path independence (loopA vs loopB) = {a2['path_independence_A_vs_B']:.2e}")
    print(f"       both-tubes loop = {a2['holo_both_tubes_netzero']:.2e}   no-tube loop = {a2['holo_no_tube']:.2e}")
    print(f"  AB3  field-on-path/peak = {a3['path_to_peak_ratio']:.2e}  (holonomy = {a3['holo']:+.4f}, field-free AB)")
    print(f"  AB4  helicity phase split = {a4['max_helicity_phase_split']:.2e}   max|[P,U^±]| = {a4['max_commutator_P_U']:.2e}")
    print(f"  AB5  q-linearity residual = {max(a5['q2_minus_2q1'], a5['q3_minus_3q1']):.2e}")
    print("\n--- MX: sourced Maxwell curl (Ė = iC×B − J, C = 2n(k/2)) ---")
    print(f"  MX1  |C|/|k| → 1/√3, max err = {m1['max_err_C_over_k_vs_inv_sqrt3']:.2e}")
    print(f"  MX2  C·(C×B) = {m2['max_C_dot_C_cross_B']:.2e}  (curl sources no charge)")
    print(f"  MX3  Gauss residual, 100 sourced steps = {m3['gauss_residual_max_100steps']:.2e}  (charge conserved)")
    print(f"  MX4  ∇·B preserved, 50 steps = {m4['magnetic_gauss_max_50steps']:.2e}")
    print(f"  MX5  Ampère residual (resolved) = {m5['ampere_residual_resolved']:.2e}  (lon. frac {m5['longitudinal_fraction']:.2f})")
    print("\n--- E2E: charge → field → A → holonomy, on one paired-photon field ---")
    print(f"  E2E  curl(A)-B = {e2['curl_minus_B_max']:.2e}   ∇×B - J = {e2['ampere_curlB_minus_J']:.2e}")
    print(f"       holonomy - flux = {e2['holo_minus_flux']:.2e}   enclosed flux = {e2['enclosed_flux']:+.4f}")
    print(f"       (current-sourced holonomy = {e2['holo_value']:+.4f}, field-free ratio {e2['field_on_path_ratio']:.2e})")
    print("\n--- checks ---")
    for name, ok, val in checks:
        print(f"   [{'PASS' if ok else 'FAIL'}] {name:34s} {val:.2e}")
    print(f"\n=== {npass}/{ntot} PASS   ({time.time()-t0:.2f} s) ===")
    if npass == ntot:
        print("  The charge-coupling path is intact on the paired photon: the Peierls")
        print("  holonomy is the discrete Stokes flux (helicity-blind, F68), and the")
        print("  sourced even-law curl conserves electric charge to machine precision.")

    res['_summary'] = {'pass': npass, 'total': ntot,
                       'checks': [{'name': n, 'ok': ok, 'val': v} for n, ok, v in checks],
                       'runtime_s': time.time() - t0}
    dst = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results',
                       'F87_charge_coupling_paired_photon.json')
    try:
        with open(dst, 'w') as fh:
            json.dump(res, fh, indent=2)
        print(f"  wrote {dst}")
    except Exception as e:
        print(f"  (could not write json: {e})")
    return npass == ntot


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
