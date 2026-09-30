"""p.77 charge-partition hypothesis — Leg A (J = L + S under the Dirac mass step)
and Leg B (per-tick charge bookkeeping of the F27/F41 beta-gauged mass step).

Created 2026-09-21 - 12:00.  Finding: F396.  Claim: CL308.

Notebook p.77: the weak mass term "violates charge conservation" as spin
conservation is violated by the free-Dirac mass term, and J = L + S rescues the
latter; so charge = intrinsic + field leg, and the field leg is the W±.

LEG A (BCC Dirac kernel, ``particles.dirac_bcc``)
    The mass step is the pointwise eta<->chi rotation exp(-i beta theta), and
    [Sigma, beta] = 0, so it changes Sigma_z by exactly zero.  Spin is exchanged
    with orbital motion only by the KINETIC step.  Lattice spin frame: the BCC
    Weyl block is A ~ 1 - i k.sigma^*/sqrt3 with sigma^* = (sx, -sy, sz), the
    complex-conjugate representation, so the spin generator is -sigma^*/2 and
    S_z = -sigma_z/2 (sign fixed empirically by J_z conservation), NOT +sigma_z/2.  The exact
    lattice point group of the block is D2 (C2x, C2y, C2z at 1e-16); C4z and
    C3 are not, so J_z is conserved only to O(k) — a continuum-limit statement.

LEG B (``gauge.hypercharge.mass_step_doublet_su2xu1y``)
    Operator identity Q = T3 + Y/2 holds on all eight components (exact).  The
    mass step conserves electric charge in the frame eta~ = U^dagger eta (the
    unitary gauge, where the step is diagonal in isospin) and violates T3 and Y
    by opposite amounts (dT3 = -dY/2).  Charge measured on the raw eta (frame
    where U is off-diagonal) is NOT conserved, by s^2 |b|^2 |eta_e|^2 for a
    pure-eta_e state — a gauge artifact that vanishes at b = 0, and that is
    unrelated to the F54 left-handed current eta_nu^* eta_e (which is 0 there).

Entry ``check_charge_partition`` returns {'checks': {...}, ...} for the D9
registry record ``F396-charge-partition-p77``.
"""
from fractions import Fraction

from casim.constants import c_lat
from casim.numerics import fft as _fft, xp as np
from casim.engine.lattice import bcc
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.particles.dirac_bcc import dirac_step_3d_bcc_splitstep
from casim.engine.gauge.hypercharge import mass_step_doublet_su2xu1y

_SX = np.array([[0, 1], [1, 0]], complex)
_SY = np.array([[0, -1j], [1j, 0]], complex)
_SZ = np.diag([1, -1]).astype(complex)


# ─────────────────────────── Leg A ───────────────────────────
def _packet(L, sig, k0, seed=1):
    r = np.arange(L) - L // 2
    X, Y, Z = np.meshgrid(r, r, r, indexing='ij')
    env = np.exp(-(X**2 + Y**2 + Z**2) / (2 * sig**2))
    ph = np.exp(1j * (k0[0] * X + k0[1] * Y + k0[2] * Z))
    rng = np.random.default_rng(seed)
    c = rng.normal(size=4) + 1j * rng.normal(size=4)
    f = [c[i] * env * ph for i in range(4)]
    n = np.sqrt(sum((abs(a)**2).sum() for a in f))
    return [a / n for a in f], (X, Y)


def _sz(f, sgn):
    return 0.5 * sgn * sum(s * (abs(a)**2).sum() for a, s in zip(f, [1, -1, 1, -1]))


def _lz(f, pos, L):
    X, Y = pos
    KX, KY, _ = make_kgrid_3d(L, L, L)
    tot = 0.0
    for a in f:
        A = _fft.fftn(a)
        tot += np.vdot(a, X * _fft.ifftn(KY * A) - Y * _fft.ifftn(KX * A)).real
    return tot


def _jz_ratio(sig, k0, m, sgn, L=32, n=12, seed=1):
    f, pos = _packet(L, sig, k0, seed=seed)
    S, Lz = [], []
    for _ in range(n + 1):
        S.append(_sz(f, sgn)); Lz.append(_lz(f, pos, L))
        f = list(dirac_step_3d_bcc_splitstep(*f, m=m))
    S, Lz = np.array(S), np.array(Lz)
    return float(np.ptp(S + Lz) / np.ptp(S)), float(np.ptp(S))


def _mass_step_dSz():
    f, _ = _packet(16, 2.0, (0.3, 0.2, 0.0))
    th = 0.3
    c, s = np.cos(th), np.sin(th)
    g = [c * f[0] - 1j * s * f[2], c * f[1] - 1j * s * f[3],
         c * f[2] - 1j * s * f[0], c * f[3] - 1j * s * f[1]]
    return abs(_sz(g, 1) - _sz(f, 1))


def _bcc_block(k, sign='+'):
    ff, fg, gf, gg = bcc.bcc_unitary(*[np.array([x]) for x in k], sign=sign)
    return np.array([[ff[0], fg[0]], [gf[0], gg[0]]])


def _rot(axis, ang):
    n = np.array(axis, float) / np.linalg.norm(axis)
    M = n[0] * _SX + n[1] * _SY + n[2] * _SZ
    return np.cos(ang / 2) * np.eye(2) - 1j * np.sin(ang / 2) * M


def _symmetry_residuals():
    rng = np.random.default_rng(0)
    ks = rng.uniform(-2, 2, (60, 3))

    def err(kmap, R, s1='+', s2='+'):
        return max(np.abs(R @ _bcc_block(k, s1) @ R.conj().T - _bcc_block(kmap(k), s2)).max()
                   for k in ks)
    c2 = {'x': (lambda k: np.array([k[0], -k[1], -k[2]]), (1, 0, 0)),
          'y': (lambda k: np.array([-k[0], k[1], -k[2]]), (0, 1, 0)),
          'z': (lambda k: np.array([-k[0], -k[1], k[2]]), (0, 0, 1))}
    d2 = max(min(err(km, _rot(ax, np.pi)), err(km, _rot(ax, -np.pi))) for km, ax in c2.values())
    c4 = lambda k: np.array([-k[1], k[0], k[2]])
    c4z = min(err(c4, _rot((0, 0, 1), a), s1, s2)
              for a in (np.pi / 2, -np.pi / 2) for s1 in '+-' for s2 in '+-')
    return d2, c4z


def _lowk_frame_residual():
    k = np.array([2e-4, 1.3e-4, -0.7e-4])
    a = _bcc_block(k)
    model = np.eye(2) - 1j * (k[0] * _SX + k[1] * _SY.conj() + k[2] * _SZ) * c_lat
    return float(np.abs(a - model).max() / np.linalg.norm(k))


# ─────────────────────────── Leg B ───────────────────────────
# Component order (nu_L, e_L, nu_R, e_R): exact Fraction quantum numbers.
_T3 = (Fraction(1, 2), Fraction(-1, 2), Fraction(0), Fraction(0))
_Y = (Fraction(-1), Fraction(-1), Fraction(0), Fraction(-2))
_Q = (Fraction(0), Fraction(-1), Fraction(0), Fraction(-1))


def _rand_state(rng, shape):
    """8 comps: eta_nu_u, eta_nu_d, eta_e_u, eta_e_d, chi_nu_u, chi_nu_d, chi_e_u, chi_e_d."""
    v = [rng.normal(size=shape) + 1j * rng.normal(size=shape) for _ in range(8)]
    n = np.sqrt(sum((abs(a)**2).sum() for a in v))
    return [a / n for a in v]


def _rand_U(rng, shape):
    z = rng.normal(size=(2,) + shape) + 1j * rng.normal(size=(2,) + shape)
    nrm = np.sqrt(abs(z[0])**2 + abs(z[1])**2)
    return z[0] / nrm, z[1] / nrm


def _charges(v, frame_U=None):
    """(Q, T3, Y) totals.  frame_U=(a,b): measure the eta doublet in the unitary
    gauge eta~ = U^dagger eta; None: raw eta."""
    e_nu_u, e_nu_d, e_e_u, e_e_d = v[0:4]
    if frame_U is not None:
        a, b = frame_U
        ac, bc = np.conj(a), np.conj(b)
        e_nu_u, e_e_u = ac * v[0] + bc * v[2], -b * v[0] + a * v[2]
        e_nu_d, e_e_d = ac * v[1] + bc * v[3], -b * v[1] + a * v[3]
    n = [(abs(e_nu_u)**2 + abs(e_nu_d)**2).sum(), (abs(e_e_u)**2 + abs(e_e_d)**2).sum(),
         (abs(v[4])**2 + abs(v[5])**2).sum(), (abs(v[6])**2 + abs(v[7])**2).sum()]
    q = sum(float(w) * x for w, x in zip(_Q, n))
    t3 = sum(float(w) * x for w, x in zip(_T3, n))
    y = sum(float(w) * x for w, x in zip(_Y, n))
    return q, t3, y


def _step(v, U, alpha, m):
    return list(mass_step_doublet_su2xu1y(*v, U[0], U[1], alpha, m))


def _leg_b(charge_frame, mass_mixing="diagonal", n_samples=40):
    rng = np.random.default_rng(7)
    shape = (5, 5)
    m = 0.3
    dQ_frame, dQ_raw, dT3_plus_dY2, dT3_max, dY_max, cf_res, ident_res = 0., 0., 0., 0., 0., 0., 0.
    for _ in range(n_samples):
        v = _rand_state(rng, shape)
        U = _rand_U(rng, shape)
        al = rng.uniform(-3, 3, shape)
        vv = v
        if mass_mixing == "charged":      # control: chi_nu <-> chi_e swapped => eta_nu mixes with chi_e
            vv = v[:4] + [v[6], v[7], v[4], v[5]]
        w = _step(vv, U, al, m)
        if mass_mixing == "charged":
            w = w[:4] + [w[6], w[7], w[4], w[5]]
        fr = U if charge_frame == "unitary" else None
        q0, t0, y0 = _charges(v, fr)
        q1, t1, y1 = _charges(w, fr)
        # NOTE: post-step frame uses the same (static) U.
        dQ_frame = max(dQ_frame, abs(q1 - q0))
        dT3_plus_dY2 = max(dT3_plus_dY2, abs((t1 - t0) + 0.5 * (y1 - y0) - (q1 - q0)))
        dT3_max = max(dT3_max, abs(t1 - t0))
        dY_max = max(dY_max, abs(y1 - y0))
        qr0, _, _ = _charges(v, None)
        qr1, _, _ = _charges(w, None)
        dQ_raw = max(dQ_raw, abs(qr1 - qr0))
    return dict(dQ_frame=dQ_frame, dQ_raw=dQ_raw, dT3_max=dT3_max, dY_max=dY_max,
                q_t3y_identity_res=dT3_plus_dY2)


def _u_identity_step():
    """U = I, alpha = 0: the discriminator run."""
    rng = np.random.default_rng(3)
    shape = (5, 5)
    v = _rand_state(rng, shape)
    one, zero = np.ones(shape, complex), np.zeros(shape, complex)
    w = _step(v, (one, zero), np.zeros(shape), 0.3)
    q0, t0, y0 = _charges(v); q1, t1, y1 = _charges(w)
    return abs(q1 - q0), abs(t1 - t0), abs(y1 - y0)


def _pure_eta_e_closed_form():
    """State with only eta_e (so the F54 left-handed current eta_nu^* eta_e = 0):
    dQ_raw = Q_after - Q_before = +s^2 |b|^2 |eta_e|^2 in the raw frame, alpha-independent."""
    rng = np.random.default_rng(11)
    shape = (5, 5)
    m = 0.3
    zero = np.zeros(shape, complex)
    e_u = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    e_d = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    nrm = np.sqrt((abs(e_u)**2 + abs(e_d)**2).sum())
    e_u, e_d = e_u / nrm, e_d / nrm
    v = [zero, zero, e_u, e_d, zero, zero, zero, zero]
    U = _rand_U(rng, shape)
    al = rng.uniform(-3, 3, shape)
    w = _step(v, U, al, m)
    j_plus = abs(np.conj(v[0]) * v[2]).max() + abs(np.conj(v[1]) * v[3]).max()
    q0, _, _ = _charges(v); q1, _, _ = _charges(w)
    s2 = np.sin(m)**2
    pred = s2 * ((abs(U[1])**2) * (abs(e_u)**2 + abs(e_d)**2)).sum()
    return abs((q1 - q0) - pred), abs(q1 - q0), float(j_plus)


def _ward_residual():
    """F27 Ward identity restated (not re-attacked): V acts on eta only."""
    rng = np.random.default_rng(5)
    shape = (5, 5)
    v = _rand_state(rng, shape)
    U = _rand_U(rng, shape)
    Va, Vb = _rand_U(rng, shape)
    al = rng.uniform(-3, 3, shape)
    m = 0.3

    def actV(x):
        (nu_u, nu_d, e_u, e_d) = x[0:4]
        Vac, Vbc = np.conj(Va), np.conj(Vb)
        return [Va * nu_u - Vbc * e_u, Va * nu_d - Vbc * e_d,
                Vb * nu_u + Vac * e_u, Vb * nu_d + Vac * e_d] + x[4:]
    lhs = actV(_step(v, U, al, m))
    Ua, Ub = U
    Vac, Vbc = np.conj(Va), np.conj(Vb)
    UV = (Va * Ua - Vbc * Ub, Vb * Ua + Vac * Ub)     # V U
    rhs = _step(actV(v), UV, al, m)
    return max(float(np.abs(a - b).max()) for a, b in zip(lhs, rhs))


def _qprime_identity():
    """Q' = (t3 - s^2 Q)/(s c) = t3 cot(theta) - t0 tan(theta),  t0 = Q - t3  (pp.103-104)."""
    rng = np.random.default_rng(2)
    res = 0.0
    for th in rng.uniform(0.1, 1.4, 40):
        for q, t3 in ((0, .5), (-1, -.5), (-1, 0), (0, 0)):
            t0 = q - t3
            lhs = (t3 - np.sin(th)**2 * q) / (np.sin(th) * np.cos(th))
            rhs = t3 / np.tan(th) - t0 * np.tan(th)
            res = max(res, abs(lhs - rhs))
    th = np.arcsin(0.5)      # sin^2 = 1/4 (F138): coefficients sqrt3 and 1/sqrt3
    res_w = max(abs(1 / np.tan(th) - np.sqrt(3)), abs(np.tan(th) - c_lat))
    return res, res_w


def check_charge_partition(spin_frame="primed", charge_frame="unitary", mass_mixing="diagonal"):
    """Return {'checks','n_pass','n_checks', measured numbers}.

    spin_frame   : 'primed' (S_z = -sigma_z/2, the lattice's own generator) | 'raw' (S = sigma/2)
    mass_mixing  : 'diagonal' (the F27 step) | 'charged' (control: eta_nu coupled to chi_e, breaks Q)
    charge_frame : 'unitary' (charges measured on U^dagger eta) | 'raw' (charges on eta as stored)
    """
    sgn = -1 if spin_frame == "primed" else 1
    out = {}
    # Leg A
    out['mass_dSz'] = _mass_step_dSz()
    # ratio is packet-specific (review F396: 0.04-0.11 small-k, 0.06-0.30 large-k across
    # seeds); the gate uses the mean over four seeds, not one packet.
    rs = [_jz_ratio(4.0, (0.15, 0.10, 0.0), 0.2, sgn, seed=sd) for sd in (1, 2, 3, 4)]
    rb = [_jz_ratio(2.5, (0.5, 0.3, 0.0), 0.2, sgn, seed=sd) for sd in (1, 2, 3, 4)]
    r_small, s_small = float(np.mean([a for a, _ in rs])), float(np.mean([b for _, b in rs]))
    r_big, s_big = float(np.mean([a for a, _ in rb])), float(np.mean([b for _, b in rb]))
    out.update(jz_ratio_small_k=r_small, jz_ratio_large_k=r_big,
               sz_range_small_k=s_small, sz_range_large_k=s_big)
    d2, c4z = _symmetry_residuals()
    out.update(d2_residual=d2, c4z_residual=c4z, lowk_frame_residual=_lowk_frame_residual())
    # Leg B
    b = _leg_b(charge_frame, mass_mixing)
    out.update(b)
    dq_u, dt3_u, dy_u = _u_identity_step()
    out.update(u_identity_dQ=dq_u, u_identity_dT3=dt3_u, u_identity_dY=dy_u)
    cf_res, dq_pure, jplus = _pure_eta_e_closed_form()
    out.update(pure_eta_e_closed_form_res=cf_res, pure_eta_e_dQ_raw=dq_pure, pure_eta_e_Jplus=jplus)
    out['ward_residual'] = _ward_residual()
    out['qprime_res'], out['qprime_weinberg_res'] = _qprime_identity()
    out['qty_identity_exact'] = all(qq == tt + yy / 2 for qq, tt, yy in zip(_Q, _T3, _Y))

    checks = {
        # Leg A
        'mass_step_conserves_Sz': out['mass_dSz'] < 1e-14,
        'spin_exchanged_only_by_kinetic_step': out['sz_range_large_k'] > 0.05,
        'Jz_conserved_at_small_k': out['jz_ratio_small_k'] < 0.2,
        'Jz_defect_grows_with_k': out['jz_ratio_large_k'] > out['jz_ratio_small_k'],
        'lattice_group_is_D2_not_C4': out['d2_residual'] < 1e-13 and out['c4z_residual'] > 0.5,
        'lowk_block_is_conjugate_rep_sigma_star': out['lowk_frame_residual'] < 1e-3,
        # Leg B
        'Q_equals_T3_plus_Y_over_2_exact': out['qty_identity_exact'] and out['q_t3y_identity_res'] < 1e-14,
        'Q_conserved_by_mass_step_unitary_frame': out['dQ_frame'] < 1e-14,
        'raw_frame_Q_not_conserved': out['dQ_raw'] > 1e-3,
        'weak_charges_violated_dT3_eq_minus_dY_half': out['dT3_max'] > 1e-3 and out['q_t3y_identity_res'] < 1e-14,
        'U_identity_mass_allowed_Q_kept_T3_Y_violated':
            out['u_identity_dQ'] < 1e-14 and out['u_identity_dT3'] > 1e-3 and out['u_identity_dY'] > 1e-3,
        'raw_dQ_closed_form_and_F54_current_zero':
            out['pure_eta_e_closed_form_res'] < 1e-14 and out['pure_eta_e_dQ_raw'] > 1e-3 and out['pure_eta_e_Jplus'] < 1e-15,
        'F27_Ward_identity_restated': out['ward_residual'] < 1e-14,
        'neutral_charge_operator_identity': out['qprime_res'] < 1e-12 and out['qprime_weinberg_res'] < 1e-12,
    }
    n_pass = sum(bool(v) for v in checks.values())
    return dict(checks={k: bool(v) for k, v in checks.items()}, n_pass=n_pass,
                n_checks=len(checks), **out)


if __name__ == "__main__":
    r = check_charge_partition()
    for k, v in r['checks'].items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"{r['n_pass']}/{r['n_checks']}")
    for k, v in r.items():
        if k not in ('checks', 'n_pass', 'n_checks'):
            print(f"  {k} = {v}")
