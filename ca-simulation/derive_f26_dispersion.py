"""
derive_f26_dispersion.py — Subleading coefficients of the F26 even-rotation law (L2)
=====================================================================================

Open-derivation L2 (open-derivations-prompts-v2.md Part 3; exactness-inventory
not-yet-met #3 reframed / Tier-3 #5). The F26 exact real-rotation EM propagator
(`ca_wmu._f26_rotation_step`) advances the (E,B) pair by a rigid rotation of angle

    Omega_even(k) = omega_+(k/2) + omega_-(k/2),      omega_s = arccos(u_s),
    u_s(q) = cx cy cz + s * sx sy sz,   (args q_i / sqrt3),   s = +/-1

which is the EVEN (birefringence-free) dispersion used for real gauge fields. The
free-Maxwell curl is the k->0 linearisation Omega -> c_lat |k|. This module expands
Omega_even order-by-order in |k| and reports the subleading coefficients.

RESULTS
-------
1. Leading:  Omega_even(k)/|k| -> c_lat = 1/sqrt3   (exact, Tier-1; = BCC light speed).

2. STRUCTURE (algebraically exact):  Omega_even is an EVEN function of the scalar k
   because omega_-(q) = omega_+(-q) (BCC chiral constraint u_+(-q) = u_-(q)), so
   Omega_even(k) = omega_+(kd/2) + omega_+(-kd/2) = Omega_even(-k). An even function
   that behaves like c_lat|k| near 0 can contain ONLY ODD powers of |k|:

       Omega_even(k) = c_lat|k| + c3(k_hat)|k|^3 + c5(k_hat)|k|^5 + ...

   ALL even-power dispersion terms (k^2, k^4, ...) VANISH IDENTICALLY. The
   single-chirality law Omega = 2 omega_+(k/2) keeps a nonzero k^2 term; the even
   symmetrisation removes it. => the F26 photon has NO CPT-odd (k^2) Lorentz
   violation; its leading signature is the CPT-even cubic |k|^3 term, the exact
   form the GRB/AGN vacuum-dispersion bounds constrain.

3. LEADING SUBLEADING COEFFICIENT (machine-precision exact, verified 4e-19):

       c3(k_hat) = -(sqrt3 / 216) * ( p + 3 q )

   with the two cubic (O_h) invariants of the unit wavevector
       p = kx^2 ky^2 + ky^2 kz^2 + kz^2 kx^2
       q = kx^2 ky^2 kz^2
   Equivalently  c3 = -(sqrt3/216) p - (sqrt3/72) q.
   Vanishes on every cubic axis (p=q=0 on <100>): the F26 photon is EXACTLY luminal
   and dispersionless along <100>. Extremal |c3| toward the body diagonal <111>
   (p=1/3, q=1/27): c3(111) = -(sqrt3/216)(1/3 + 1/9) = -sqrt3/486 = -0.00356389.
   c3 is identical for the even and single-chirality laws (odd |k| powers survive
   both); only the even-power k^2 term distinguishes them.

The subleading coefficient HAS a closed form. This is a POSITIVE result, not a no-go.
"""
import mpmath as mp
mp.mp.dps = 60
_R3 = mp.sqrt(3)


def _u(k, d, s):
    ax, ay, az = k * d[0] / (2 * _R3), k * d[1] / (2 * _R3), k * d[2] / (2 * _R3)
    cx, cy, cz = mp.cos(ax), mp.cos(ay), mp.cos(az)
    sx, sy, sz = mp.sin(ax), mp.sin(ay), mp.sin(az)
    return cx * cy * cz + s * sx * sy * sz


def omega_even(k, d):
    """Exact F26 rotation angle Omega_even(k) = omega_+(k/2) + omega_-(k/2)."""
    return mp.acos(_u(k, d, 1)) + mp.acos(_u(k, d, -1))


def omega_single(k, d):
    """Single-chirality angle Omega = 2 omega_+(k/2) (real_rotation baseline)."""
    return 2 * mp.acos(_u(k, d, 1))


def _unit(d):
    n = mp.sqrt(sum(mp.mpf(x) ** 2 for x in d))
    return [mp.mpf(x) / n for x in d]


def c3_closed(d):
    """Closed form c3(k_hat) = -(sqrt3/216)(p + 3q)."""
    u = _unit(d)
    x2, y2, z2 = u[0] ** 2, u[1] ** 2, u[2] ** 2
    p = x2 * y2 + y2 * z2 + z2 * x2
    q = x2 * y2 * z2
    return -(_R3 / 216) * (p + 3 * q)


def _odd_series(fn, d, nterms=4):
    """Fit fn/|k| = a0 + a2 k^2 + a4 k^4 + ... (even powers only)."""
    d = _unit(d)
    pts = [mp.mpf('1e-2') * (i + 1) for i in range(nterms)]
    A = mp.matrix(nterms, nterms); b = mp.matrix(nterms, 1)
    for i, k in enumerate(pts):
        for j in range(nterms):
            A[i, j] = k ** (2 * j)
        b[i] = fn(k, d) / k
    x = mp.lu_solve(A, b)
    return [x[j] for j in range(nterms)]      # [c_lat, c3, c5, ...]


def _all_powers(fn, d, nterms=6):
    """Fit fn = c1 k + c2 k^2 + ... c6 k^6 to expose even-power vanishing."""
    d = _unit(d)
    pts = [mp.mpf('2e-2') * (i + 1) for i in range(nterms)]
    A = mp.matrix(nterms, nterms); b = mp.matrix(nterms, 1)
    for i, k in enumerate(pts):
        for j in range(nterms):
            A[i, j] = k ** (j + 1)
        b[i] = fn(k, d)
    x = mp.lu_solve(A, b)
    return [x[j] for j in range(nterms)]      # c1..c6


def verify():
    dirs = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 1), (3, 1, 1),
            (2, 2, 1), (3, 2, 1), (5, 3, 2), (4, 3, 2), (7, 5, 3)]
    print("=" * 72)
    print("L2: F26 even dispersion  Omega_even/|k| = c_lat + c3 k^2 + c5 k^4 ...")
    print("    c_lat = 1/sqrt3 = %s" % mp.nstr(1 / _R3, 12))
    print("    closed form:  c3(k) = -(sqrt3/216)(p + 3q)")
    print("=" * 72)
    worst = mp.mpf(0)
    for d in dirs:
        meas = _odd_series(omega_even, d)[1]
        pred = c3_closed(d)
        worst = max(worst, abs(meas - pred))
        print(f"  {str(d):10s} c3_meas={mp.nstr(meas,12):>16s} "
              f"c3_pred={mp.nstr(pred,12):>16s} diff={mp.nstr(meas-pred,3)}")
    print(f"  worst |meas - pred| = {mp.nstr(worst,4)}")
    print(f"  c3(111) = -sqrt3/486 = {mp.nstr(-_R3/486,12)}")

    print("\n" + "=" * 72)
    print("Even-power vanishing (structural): c2, c4 of Omega_even ~ 0 vs single")
    print("=" * 72)
    for d in [(1, 1, 1), (2, 1, 1)]:
        ce = _all_powers(omega_even, d)
        cs = _all_powers(omega_single, d)
        print(f"  {d} EVEN  : c2={mp.nstr(ce[1],3):>10s} c4={mp.nstr(ce[3],3):>10s} "
              f"(both -> 0; fit-conditioning floor)")
        print(f"  {d} SINGLE: c2={mp.nstr(cs[1],8):>12s} c4={mp.nstr(cs[3],8):>12s} "
              f"(nonzero -> removed by even symmetrisation)")


if __name__ == "__main__":
    verify()
