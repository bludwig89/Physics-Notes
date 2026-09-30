"""F397 — the notebook's FACTORIZATION ROUTE (pp.176-182): a vector is two null vectors,
a null vector is a spinor outer product.

Two theorems from the Ludwig notebook, tested against the model's own lattice constituents:

  T1  every null 4-vector is a spinor bilinear   sigma.V = psi psi^dagger   (phase of psi free)
  T2  every timelike V is a sum of two null vectors, V = a + b, with a free direction a_hat

Convention (notebook p.176): sigma.V = [[V0-Vz, -Vx+iVy], [-Vx-iVy, V0+Vz]], so
det(sigma.V) = V.V and sigma.V = psi psi^dagger  <=>  V null, future-pointing.

This is **not** the audit-3.3 object (notebook pp.161-175; cf. F25, whose curl-residual reading is
superseded by S18).  The audit's longitudinal-only result is about the
*dynamics* of one spinor, sigma^mu d_mu acting on a single null V.  T2 is the *algebraic*
decomposition of a non-null V.  They must not be conflated.

Correction found here (F397): the notebook's boxed closed form
    a_mu = (1/2V0)(V0^2-|V|^2 + 2 a_hat.V)(1, a_hat)
is dimensionally inconsistent and does NOT give a null pair.  The notebook's own preceding line,
a0 (V0 - a_hat.V) = (1/2)(V0^2 - |V|^2), gives the correct
    a0 = V.V / (2 (V0 - a_hat.V)).
Both are implemented; ``formula="notebook"`` is the declared negative control.

Only closed-form 2x2 algebra and the audited BCC dispersion are used.  No eigensolver on any
chiral matrix (CLAUDE.md): the Hermitian square root is the closed form
sqrt(M) = (M + sqrt(det M) 1) / sqrt(tr M + 2 sqrt(det M)).
"""

from casim.numerics import xp
from casim.engine.lattice.bcc import bcc_dispersion as _w, bcc_spin_axis as _n
from casim.constants import c_lat

_S0 = xp.eye(2, dtype=complex)
_SX = xp.array([[0, 1], [1, 0]], dtype=complex)
_SY = xp.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = xp.array([[1, 0], [0, -1]], dtype=complex)


# ── Minkowski / sigma.V ────────────────────────────────────────────────────
def mink(V):
    """V.V = V0^2 - |V|^2."""
    return V[0] ** 2 - V[1] ** 2 - V[2] ** 2 - V[3] ** 2


def sigma_dot(V):
    """Notebook p.176: [[V0-Vz, -Vx+iVy], [-Vx-iVy, V0+Vz]]."""
    return xp.array([[V[0] - V[3], -V[1] + 1j * V[2]],
                     [-V[1] - 1j * V[2], V[0] + V[3]]], dtype=complex)


def sigma_bar_dot(V):
    """The parity partner  sigma-bar.V = sigma_y (sigma.V)^T sigma_y."""
    return xp.array([[V[0] + V[3], V[1] - 1j * V[2]],
                     [V[1] + 1j * V[2], V[0] - V[3]]], dtype=complex)


def vec_from_M(M):
    """Inverse of sigma_dot for a Hermitian M."""
    return xp.array([((M[0, 0] + M[1, 1]) / 2).real, -M[0, 1].real,
                     M[0, 1].imag, ((M[1, 1] - M[0, 0]) / 2).real])


# ── T2: timelike decomposition ─────────────────────────────────────────────
def t2_decompose(V, ahat, formula="corrected"):
    """Return (a, b), V = a + b, a = a0 (1, ahat).

    ``formula="corrected"``: a0 = V.V / (2 (V0 - ahat.Vvec))   [from a.a = 0 and (V-a).(V-a) = 0].
    ``formula="notebook"`` : the notebook's boxed form (V0^2-|V|^2+2 ahat.V)/(2 V0)  [wrong].
    """
    ahat = ahat / xp.sqrt(ahat @ ahat)
    dot = ahat @ V[1:]
    if formula == "corrected":
        a0 = mink(V) / (2.0 * (V[0] - dot))
    elif formula == "notebook":
        a0 = (V[0] ** 2 - V[1:] @ V[1:] + 2.0 * dot) / (2.0 * V[0])
    else:
        raise ValueError(formula)
    a = xp.concatenate([xp.array([a0]), a0 * ahat])
    return a, V - a


# ── T1: null vector -> spinor ──────────────────────────────────────────────
def t1_spinor(N, theta=0.0):
    """psi = (alpha, beta) with psi psi^dagger = sigma.N (N null, future).  ``theta`` is the free
    phase (the notebook's 'ambiguity of e^{i theta}')."""
    al2 = N[0] - N[3]
    if al2 > 1e-14 * N[0]:
        al = xp.sqrt(al2)
        be = (-N[1] - 1j * N[2]) / al           # from M_21 = alpha^* beta  (alpha real)
    else:                                       # N along -z axis: alpha = 0
        al = 0.0
        be = xp.sqrt(N[0] + N[3])
    return xp.exp(1j * theta) * xp.array([al, be], dtype=complex)


def _outer(psi):
    return xp.outer(psi, psi.conj())


def sqrtm_herm2(M):
    """Closed-form PSD square root of a 2x2 Hermitian matrix."""
    d = xp.sqrt(max((M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]).real, 0.0))
    t = (M[0, 0] + M[1, 1]).real
    return (M + d * _S0) / xp.sqrt(t + 2.0 * d)


# ── SL(2,C) boost / rotation (closed-form exponential) ────────────────────
def sl2c_element(zeta, theta):
    """S = exp( (zeta - i theta) . sigma / 2 ), det S = 1, closed form via cosh/sinh."""
    z = 0.5 * (xp.asarray(zeta, dtype=complex) - 1j * xp.asarray(theta, dtype=complex))
    r2 = z @ z
    r = xp.sqrt(r2 + 0j)
    if abs(r) < 1e-15:
        return _S0 + z[0] * _SX + z[1] * _SY + z[2] * _SZ
    zs = z[0] * _SX + z[1] * _SY + z[2] * _SZ
    return xp.cosh(r) * _S0 + xp.sinh(r) / r * zs


def lorentz_act(S, V):
    """V -> Lambda(S) V via sigma.V -> S (sigma.V) S^dagger."""
    return vec_from_M(S @ sigma_dot(V) @ S.conj().T)


# ── checks ─────────────────────────────────────────────────────────────────
def _rand_timelike(g, n):
    out = []
    for _ in range(n):
        v = g.normal(size=3)
        v = v / xp.sqrt(v @ v) * g.uniform(0.0, 2.0)
        out.append(xp.concatenate([xp.array([xp.sqrt(v @ v + g.uniform(0.05, 3.0) ** 2)]), v]))
    return out


def _rand_dir(g):
    a = g.normal(size=3)
    return a / xp.sqrt(a @ a)


def _pair_lattice(k):
    """(leg defects, pair defect) for k: legs at k/2 on the two branches, V = (Omega_even, c k)."""
    h = k / 2.0
    wp, wm = _w(*h, "+"), _w(*h, "-")
    kk = xp.sqrt(k @ k)
    q = xp.sqrt(h @ h)
    dp, dm = wp ** 2 - (c_lat * q) ** 2, wm ** 2 - (c_lat * q) ** 2
    om = wp + wm
    return dp, dm, om ** 2 - (c_lat * kk) ** 2, om


def _eps(q):
    """Leading odd-chirality term  omega^+(q) = c|q| + eps(q) + O(q^3),  eps = -q_x q_y q_z /(3|q|)."""
    return -q[0] * q[1] * q[2] / (3.0 * xp.sqrt(q @ q))


def _E0(k, p):
    return _w(*(k / 2 + p), "+") + _w(*(k / 2 - p), "-")


def _threshold(k):
    """T(k) = min_p E0(p;k): deterministic pattern search from three starts (symmetric split and
    the two collinear endpoints), each step-halving with a hard iteration cap."""
    best = 1e9
    for st in (xp.zeros(3), k / 2, -k / 2):
        p, step, e, it = st.copy(), xp.sqrt(k @ k) / 4, _E0(k, st), 0
        while step > 1e-11 and it < 600:
            it += 1
            imp = False
            for d in xp.concatenate([xp.eye(3), -xp.eye(3)]):
                e2 = _E0(k, p + step * d)
                if e2 < e - 1e-18:
                    p, e, imp = p + step * d, e2, True
            if not imp:
                step /= 2
        best = min(best, e)
    return best


def _slope(xs, ys):
    lx, ly = xp.log(xp.abs(xp.array(xs))), xp.log(xp.abs(xp.array(ys)))
    return float(((lx - lx.mean()) * (ly - ly.mean())).sum() / ((lx - lx.mean()) ** 2).sum())


def check_factorization_route(seed=397, n=40, formula="corrected"):
    """F397 gate entry. Legs (each able to fail); the declared control is ``formula="notebook"``."""
    g = xp.random.default_rng(seed)
    checks, meas = {}, {}

    # T2 -- null pair, closed form
    worst_null, worst_sum, min_e = 0.0, 0.0, 1e9
    for V in _rand_timelike(g, n):
        for _ in range(6):
            a, b = t2_decompose(V, _rand_dir(g), formula)
            worst_null = max(worst_null, abs(mink(a)), abs(mink(b)))
            worst_sum = max(worst_sum, float(xp.max(xp.abs(a + b - V))))
            min_e = min(min_e, a[0], b[0])
    checks["t2_pair_null_and_sums"] = bool(worst_null < 1e-12 and worst_sum < 1e-13 and min_e > 0)
    meas["t2_null_residual"] = float(worst_null)

    # the notebook's boxed formula is NOT null (documents the transcription/notebook error)
    dn = max(abs(mink(t2_decompose(V, _rand_dir(g), "notebook")[1])) for V in _rand_timelike(g, n))
    checks["notebook_boxed_formula_defective"] = bool(dn > 1e-2)
    meas["notebook_boxed_defect"] = float(dn)

    # canonical decomposition of p.145 = a_hat = +Vhat, in the corrected formula
    V = _rand_timelike(g, 1)[0]
    vh = V[1:] / xp.sqrt(V[1:] @ V[1:])
    a, _ = t2_decompose(V, vh, "corrected")
    can = xp.concatenate([xp.array([0.5 * (V[0] + xp.sqrt(V[1:] @ V[1:]))]),
                          0.5 * (V[0] + xp.sqrt(V[1:] @ V[1:])) * vh])
    checks["canonical_split_is_ahat_equals_Vhat"] = bool(float(xp.max(xp.abs(a - can))) < 1e-13)

    # T1 -- null vector = spinor outer product, phase free
    w1 = w2 = 0.0
    for _ in range(n):
        Vd = _rand_timelike(g, 1)[0]
        a, _b = t2_decompose(Vd, _rand_dir(g))
        p1, p2 = t1_spinor(a, 0.0), t1_spinor(a, g.uniform(0, 6.28))
        w1 = max(w1, float(xp.max(xp.abs(_outer(p1) - sigma_dot(a)))))
        w2 = max(w2, float(xp.max(xp.abs(_outer(p2) - sigma_dot(a)))))
    checks["t1_outer_product"] = bool(w1 < 1e-13 and w2 < 1e-13)
    meas["t1_residual"] = float(max(w1, w2))

    # U(2)/U(1)^2 = S^2 : Psi = (xi, eta) satisfies Psi Psi^dag = M  => M^{-1/2} Psi is unitary
    wu, rk = 0.0, 0
    for V in _rand_timelike(g, n):
        M = sigma_dot(V)
        R = sqrtm_herm2(M)
        Ri = xp.linalg.inv(R)
        a, b = t2_decompose(V, _rand_dir(g))
        Psi = xp.stack([t1_spinor(a), t1_spinor(b)], axis=1)
        U = Ri @ Psi
        wu = max(wu, float(xp.max(xp.abs(U @ U.conj().T - _S0))),
                 float(xp.max(xp.abs(Psi @ Psi.conj().T - M))))
    checks["leg_space_is_U2_unitary"] = bool(wu < 1e-12)
    meas["U2_residual"] = float(wu)
    # rank of the map ahat -> a at fixed V is 2 (the free direction is a 2-sphere, not a point)
    V = xp.array([1.3, 0.3, 0.2, 0.4])
    a0 = xp.array([0.6, 0.48, 0.64])
    J = []
    for t in (xp.cross(a0, xp.array([1.0, 0, 0])), xp.cross(a0, xp.array([0, 1.0, 0]))):
        h = 1e-6
        J.append((t2_decompose(V, a0 + h * t)[0] - t2_decompose(V, a0 - h * t)[0]) / (2 * h))
    Jm = xp.stack(J)
    sv = xp.linalg.svd(Jm, compute_uv=False)
    checks["ahat_is_a_free_2_sphere"] = bool(sv[1] > 1e-3 * sv[0])
    meas["jacobian_singular_values"] = [float(x) for x in sv]

    # SL(2,C) covariance (gate 1e)
    wc = 0.0
    for V in _rand_timelike(g, n):
        S = sl2c_element(g.normal(size=3) * 0.7, g.normal(size=3) * 0.7)
        a, b = t2_decompose(V, _rand_dir(g))
        V2, a2 = lorentz_act(S, V), lorentz_act(S, a)
        a2r, b2r = t2_decompose(V2, a2[1:] / a2[0])
        wc = max(wc, float(xp.max(xp.abs(a2r - a2))), float(xp.max(xp.abs(b2r - lorentz_act(S, b)))))
    checks["sl2c_covariance"] = bool(wc < 1e-12)
    meas["covariance_residual"] = float(wc)

    # chirality-blindness: the right-handed leg is fixed by the left-handed one (sigma_y psi^*)
    wch = 0.0
    for _ in range(n):
        Vd = _rand_timelike(g, 1)[0]
        a, _b = t2_decompose(Vd, _rand_dir(g))
        p = t1_spinor(a)
        pr = _SY @ p.conj()
        wch = max(wch, float(xp.max(xp.abs(_outer(pr) - sigma_bar_dot(a)))))
    checks["chirality_is_not_extra_data"] = bool(wch < 1e-13)

    # timelike => neither leg can vanish (massive boson has two real legs; b=0 <=> V null)
    lo = min(min(t2_decompose(V, _rand_dir(g))[0][0], t2_decompose(V, _rand_dir(g))[1][0])
             for V in _rand_timelike(g, n))
    checks["timelike_legs_nondegenerate"] = bool(lo > 0)

    # leg-energy spread = |V| independent of mass (contrast: F91 Z axial split ~ k^3)
    ratios = []
    for m in (0.01, 0.1, 0.3, 1.0):
        kk = 0.7
        V = xp.array([xp.sqrt(kk ** 2 + m ** 2), 0.0, 0.0, kk])
        e = [t2_decompose(V, xp.array([0, 0, s]))[0][0] for s in (-1.0, 1.0)]
        ratios.append(float((e[1] - e[0]) / kk))
    checks["ahat_spread_is_not_mass_suppressed"] = bool(max(abs(r - 1.0) for r in ratios) < 1e-9)
    meas["leg_energy_spread_over_k"] = ratios

    # degree-of-freedom arithmetic (exact integers): real parameters, spinor vs vector
    dof = {"null":     {"V_components": 4, "constraint": 1, "V_free": 3, "spinor_real": 4, "phase": 1},
           "timelike": {"V_components": 4, "constraint": 0, "V_free": 4, "spinor_pair_real": 8,
                        "leg_U2": 4, "ahat_S2": 2, "leg_phases": 2}}
    n_ok = (dof["null"]["V_components"] - dof["null"]["constraint"] == dof["null"]["spinor_real"] - dof["null"]["phase"]
            and dof["timelike"]["spinor_pair_real"] - dof["timelike"]["V_free"] == dof["timelike"]["leg_U2"]
            == dof["timelike"]["ahat_S2"] + dof["timelike"]["leg_phases"])
    meas["dof_arithmetic_closes"] = bool(n_ok)   # integer bookkeeping, documented not gated
    meas["dof"] = dof

    # lattice: constituent and pair defects, exponents
    ks, dps, dms, vs = [], [], [], []
    k0 = xp.array([0.5, 0.5, 0.5])
    for s in (1.0, 0.5, 0.25, 0.125):
        dp, dm, v2, _om = _pair_lattice(k0 * s)
        ks.append(s); dps.append(dp); dms.append(dm); vs.append(v2)
    e_leg, e_pair = _slope(ks, dps), _slope(ks, vs)
    checks["lattice_leg_defect_cubic"] = bool(abs(e_leg - 3.0) < 0.05)
    checks["lattice_pair_defect_quartic"] = bool(abs(e_pair - 4.0) < 0.05)
    checks["leg_defects_opposite_sign"] = bool(all(dp * dm < 0 for dp, dm in zip(dps, dms))
                                                and abs(dps[-1] / dms[-1] + 1) < 0.05)
    meas["leg_defect_exponent"], meas["pair_defect_exponent"] = e_leg, e_pair
    meas["pair_V2_over_k4_at_111"] = float(vs[-1] / (xp.sqrt(k0 @ k0) * ks[-1]) ** 4)

    # eps closed form and the O(k^2) offset  Omega_even - T(k) = |eps(k)| + O(k^3)
    eres = []
    for s in (0.2, 0.1, 0.05):
        q = xp.array([0.3, 0.2, -0.5]) * s
        eres.append((_w(*q, "+") - c_lat * xp.sqrt(q @ q) - _eps(q)) / (xp.sqrt(q @ q)) ** 3)
    checks["eps_closed_form"] = bool(max(abs(eres[i] - eres[0]) for i in range(3)) < 5e-3)
    rat = []
    for s in (0.5, 0.25, 0.125):
        k = xp.array([0.3, 0.2, -0.5]) * s
        rat.append(float((_E0(k, xp.zeros(3)) - _threshold(k)) / abs(_eps(k))))
    checks["F169_offset_equals_abs_eps"] = bool(abs(rat[2] - 1) < 0.015 and abs(rat[1] - 1) < 0.03
                                                and abs(rat[0] - 1) < 0.06
                                                and abs(rat[2] - 1) < abs(rat[1] - 1) < abs(rat[0] - 1))
    meas["offset_over_abs_eps"] = rat
    # collinear valley is linear:  E0(x) = c|k| + eps(k)(2x-1) + O(k^3)  (x = momentum fraction of the + leg)
    k = xp.array([0.3, 0.2, -0.5]) * 0.5
    kn = xp.sqrt(k @ k)
    dev = max(abs(_E0(k, (x - 0.5) * k) - (c_lat * kn + _eps(k) * (2 * x - 1))) for x in (0.0, 0.25, 0.75, 1.0))
    # must RESOLVE the lift: deviation from the linear law is < 25% of the lift itself
    checks["collinear_valley_linear_lift"] = bool(dev < 0.25 * abs(_eps(k)))
    meas["valley_dev_over_k3"] = float(dev / kn ** 3)
    # along a coordinate plane eps = 0 and the offset drops to O(k^3)
    o = []
    for s in (0.5, 0.25, 0.125):
        k = xp.array([1.0, 0.0, 0.3]) * s
        o.append(float(_E0(k, xp.zeros(3)) - _threshold(k)))
    checks["offset_cubic_on_coordinate_plane"] = bool(abs(_slope([0.5, 0.25, 0.125], o) - 3.0) < 0.15)
    meas["plane_offset_exponent"] = _slope([0.5, 0.25, 0.125], o)

    # local U(1): Berry connection of the T1 phase
    checks_u1, meas_u1 = _u1_checks(g)
    checks.update(checks_u1)
    meas.update(meas_u1)

    return {"checks": checks, "all_pass": all(checks.values()), "measured": meas}


def _spinor_field(x, y):
    """A smooth non-degenerate spinor field psi(x, y) used only for the Berry-connection check."""
    return xp.array([1.0 + 0.3 * xp.sin(x) + 0.2j * y, 0.5 * xp.cos(y) + (0.4 + 0.1 * x) * 1j * xp.sin(x + y)])


def _u1_checks(g):
    h = 1e-5

    def unit(x, y, th=None):
        p = _spinor_field(x, y)
        p = p / xp.sqrt((p.conj() @ p).real)
        return p * xp.exp(1j * th(x, y)) if th else p

    def berry(x, y, th=None):
        d = []
        for dx, dy in ((h, 0), (0, h)):
            dp = (unit(x + dx, y + dy, th) - unit(x - dx, y - dy, th)) / (2 * h)
            d.append((unit(x, y, th).conj() @ dp).imag)
        return xp.array(d)

    def nvec(x, y):
        p = unit(x, y)
        return xp.array([(p.conj() @ (s @ p)).real for s in (_SX, _SY, _SZ)])

    th = lambda x, y: 0.7 * xp.sin(2 * x) * xp.cos(y) + 0.3 * x * y      # a LOCAL phase theta(x)
    x0, y0 = 0.31, -0.47
    # V invariant
    dv = float(xp.max(xp.abs(_outer(unit(x0, y0, th)) - _outer(unit(x0, y0)))))
    # connection shifts by grad theta
    gth = xp.array([(th(x0 + h, y0) - th(x0 - h, y0)) / (2 * h), (th(x0, y0 + h) - th(x0, y0 - h)) / (2 * h)])
    dshift = float(xp.max(xp.abs(berry(x0, y0, th) - berry(x0, y0) - gth)))
    # field strength = (1/2) n . (dx n x dy n), gauge invariant
    def fstr(tf):
        e = 1e-4
        ax = lambda x, y: berry(x, y, tf)[1]
        ay = lambda x, y: berry(x, y, tf)[0]
        return (ax(x0 + e, y0) - ax(x0 - e, y0)) / (2 * e) - (ay(x0, y0 + e) - ay(x0, y0 - e)) / (2 * e)
    dnx = (nvec(x0 + h, y0) - nvec(x0 - h, y0)) / (2 * h)
    dny = (nvec(x0, y0 + h) - nvec(x0, y0 - h)) / (2 * h)
    area = 0.5 * float(nvec(x0, y0) @ xp.cross(dnx, dny))
    f0, f1 = fstr(None), fstr(th)
    # degree-0 in the amplitude of V (Maxwell F is degree 1): direction is all the connection sees
    p = _spinor_field(x0, y0)
    deg0 = float(xp.max(xp.abs(_outer(3.0 * p) / 9.0 - _outer(p))))
    # (A + grad theta) is not null for a null A
    nn = []
    for _ in range(20):
        Vd = _rand_timelike(g, 1)[0]
        A = t2_decompose(Vd, _rand_dir(g))[0]
        gr = g.normal(size=4)
        nn.append(abs(mink(A + gr)))
    return ({"u1_phase_is_local_redundancy": bool(dv < 1e-14 and dshift < 1e-6),
             "u1_connection_is_composite_area_form": bool(abs(abs(f0) - abs(area)) < 1e-4 and abs(f0 - f1) < 1e-5),
             },
            {"u1_degree0_algebra_residual": deg0, "u1_gauge_shift_residual": dshift, "u1_f_vs_area": [float(f0), area],
             "null_defect_after_gradient_shift_min": float(min(nn))})
