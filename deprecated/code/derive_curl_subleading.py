# ===== deprecated/code backup =====================================
# source     : ca-simulation/derive_curl_subleading.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/derive_curl_subleading.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: derive_curl_subleading.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
derive_curl_subleading.py — Closed forms for the composite-photon curl-residual
subleading coefficients (Finding 7 / L1, exactness-inventory not-yet-met #5).
================================================================================

Finding 7 measured the pointwise composite-photon curl residual

    curl_residual / |k|  =  1/sqrt(2d)  +  (subleading)  +  ...

with leading constant 1/sqrt(2d) = (1/sqrt2)*c_lat (Tier-1, dimensionality-driven,
F7). The SUBLEADING coefficients were "measured numerically, no closed form":
  * 2D square:  curl/k = 1/2   + alpha * k^2 + O(k^3),  alpha ~ -0.0104
  * 3D BCC:     curl/k = 1/sqrt6 + beta * k  + O(k^2),  beta  ~ +0.01883

This module derives BOTH in closed form and verifies them at mpmath precision by
replicating the exact eigenmode/bilinear construction of ca_maxwell_2d.py and
ca_maxwell.py (cross-checked against those numpy modules to 10 digits).

RESULTS
-------
2D square (k at angle p from x-axis):
    alpha(p) = (cos 4p - 9) / 768                         [machine-precision exact]
      * on-axis (p=0, pi/2):  alpha = -1/96  = -0.0104166...   <-- Finding 7's "-0.0104"
      * at 45 deg:            alpha = -5/384 = -0.0130208...   (max |alpha|)
      * direction average:    <alpha> = -9/768 = -3/256 = -0.0117187...
    The on-axis value is derived ALGEBRAICALLY below (analytic_alpha_axis()):
        r/k = sqrt2 * sin(k/(2 sqrt2)) / k = 1/2 - k^2/96 + O(k^4)  =>  -1/96 exact.

3D BCC (k a unit vector):
    beta(k_hat) = -(sqrt2 / 12) * k_x_hat * k_y_hat * k_z_hat  [machine-precision exact]
      * vanishes on every coordinate plane (any component 0)  -> pure cubic T2 harmonic
      * max |beta| at (1,1,1)/sqrt3: sqrt2/12 * 1/(3 sqrt3) = sqrt6/108 = 0.0226805
      * Finding 7's "0.01883" is NOT a constant: it is beta at the seed-0
        max-residual random direction (0.7415,0.5385,-0.4002), = 0.018833.

CONCLUSION: both "open" numbers are closed. The 3D 0.01883 was a random-seed
artifact of a direction-dependent quantity; the 2D -0.0104 is the on-axis (=
max-residual) value of alpha(p). Neither is a new fundamental constant.
"""
import mpmath as mp
mp.mp.dps = 50
I = mp.mpc(0, 1)
SX = [[0, 1], [1, 0]]; SY = [[0, -I], [I, 0]]; SZ = [[1, 0], [0, -1]]


def _bil(a, b):
    out = []
    for S in (SX, SY, SZ):
        out.append(sum(a[i] * S[i][j] * b[j] for i in range(2) for j in range(2)))
    return out


def _dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def _norm(v):
    return mp.sqrt(sum((x * mp.conj(x)).real for x in v))


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def _residual(u, nx, ny, nz, omega, same_mode):
    """Given the half-momentum unitary data, return the normalised curl residual
    max(resE, resB)/(|E0|+|B0|), replicating ca_maxwell(_2d).py exactly."""
    U = [[u - I * nz, -I * (nx - I * ny)], [-I * (nx + I * ny), u + I * nz]]
    lam_p = mp.e ** (-I * omega)
    psi = [U[0][1], lam_p - U[0][0]]
    psi = [v / _norm(psi) for v in psi]
    if same_mode:            # 2D: phi = psi_+
        phi = psi
    else:                    # 3D: phi = psi_-  (negative eigenmode)
        lam_m = mp.e ** (I * omega)
        phi = [U[0][1], lam_m - U[0][0]]
        phi = [v / _norm(phi) for v in phi]
    nhalf = [nx, ny, nz]; nmag = _norm(nhalf); nhat = [c / nmag for c in nhalf]

    def EB(ps, ph):
        G = _bil(ph, ps); gd = _dot(G, nhat)
        GT = [G[i] - gd * nhat[i] for i in range(3)]
        GTd = [mp.conj(x) for x in GT]
        E = [nmag * (GT[i] + GTd[i]) for i in range(3)]
        B = [I * nmag * (GTd[i] - GT[i]) for i in range(3)]
        return E, B

    E0, B0 = EB(psi, phi)
    ph_ = mp.e ** (-I * omega)
    Et, Bt = EB([v * ph_ for v in psi], [v * ph_ for v in phi])
    twn = [2 * c for c in nhalf]
    rE = [I * c for c in _cross(twn, B0)]
    rB = [-I * c for c in _cross(twn, E0)]
    den = _norm(E0) + _norm(B0)
    resE = _norm([Et[i] - E0[i] - rE[i] for i in range(3)])
    resB = _norm([Bt[i] - B0[i] - rB[i] for i in range(3)])
    return max(resE, resB) / den


def curl_resid_2d(k, p):
    r2 = mp.sqrt(2)
    ax = k * mp.cos(p) / 2 / r2; ay = k * mp.sin(p) / 2 / r2
    cx, cy, sx, sy = mp.cos(ax), mp.cos(ay), mp.sin(ax), mp.sin(ay)
    u = cx * cy; nx = sx * cy; ny = cx * sy; nz = sx * sy
    return _residual(u, nx, ny, nz, mp.acos(u), same_mode=True)


def curl_resid_3d(k, dvec):
    r3 = mp.sqrt(3)
    kx, ky, kz = k * dvec[0], k * dvec[1], k * dvec[2]
    ax, ay, az = kx / 2 / r3, ky / 2 / r3, kz / 2 / r3
    cx, cy, cz = mp.cos(ax), mp.cos(ay), mp.cos(az)
    sx, sy, sz = mp.sin(ax), mp.sin(ay), mp.sin(az)
    u = cx * cy * cz + sx * sy * sz
    nx = sx * cy * cz - cx * sy * sz
    ny = -cx * sy * cz + sx * cy * sz
    nz = cx * cy * sz + sx * sy * cz
    return _residual(u, nx, ny, nz, mp.acos(u), same_mode=False)


# ---- closed forms ----
def alpha_2d(p):
    return (mp.cos(4 * p) - 9) / 768


def beta_3d(dvec):
    n = mp.sqrt(sum(c * c for c in dvec))
    d = [c / n for c in dvec]
    return -(mp.sqrt(2) / 12) * d[0] * d[1] * d[2]


def analytic_alpha_axis(k):
    """Algebraic on-axis 2D residual: r/k = sqrt2 sin(k/(2 sqrt2))/k."""
    return mp.sqrt(2) * mp.sin(k / (2 * mp.sqrt(2))) / k


def _coeff2d(p):
    def f(k):
        return (curl_resid_2d(k, p) / k - mp.mpf('0.5')) / k**2
    k = mp.mpf('1e-3'); return (4 * f(k / 2) - f(k)) / 3


def _coeff3d(dvec):
    inv6 = 1 / mp.sqrt(6)
    n = mp.sqrt(sum(c * c for c in dvec))
    d = [c / n for c in dvec]          # unit vector: |k| = k exactly
    def f(k):
        return (curl_resid_3d(k, d) / k - inv6) / k
    k = mp.mpf('1e-4'); return 2 * f(k / 2) - f(k)


def verify():
    print("=" * 70)
    print("2D square:  alpha(p) = (cos4p - 9)/768")
    print("=" * 70)
    worst = mp.mpf(0)
    for deg in [0.0001, 15, 22.5, 30, 45, 60, 75, 90]:
        p = mp.pi * mp.mpf(deg) / 180
        meas = _coeff2d(p); pred = alpha_2d(p)
        worst = max(worst, abs(meas - pred))
        print(f"  {deg:8}deg  meas={mp.nstr(meas,12)}  pred={mp.nstr(pred,12)}")
    print(f"  worst |meas-pred| = {mp.nstr(worst,4)}")
    print(f"  on-axis alpha = {mp.nstr(alpha_2d(mp.pi/2),12)}  (= -1/96)")
    # algebraic on-axis series
    ser = [ (analytic_alpha_axis(mp.mpf(k))-mp.mpf('0.5'))/mp.mpf(k)**2
            for k in ['1e-2','1e-3'] ]
    print(f"  analytic r/k on-axis -> alpha = {mp.nstr((4*ser[1]-ser[0])/3,12)} (algebraic -1/96)")
    print()
    print("=" * 70)
    print("3D BCC:  beta(k_hat) = -(sqrt2/12) * kx*ky*kz")
    print("=" * 70)
    worst = mp.mpf(0)
    for d in [(1,1,1),(2,1,1),(3,1,1),(2,2,1),(3,2,1),(5,3,2),(1,1,0),(1,0,0)]:
        meas = _coeff3d(d); pred = beta_3d(d)
        worst = max(worst, abs(meas - pred))
        print(f"  {str(d):10s}  meas={mp.nstr(meas,11)}  pred={mp.nstr(pred,11)}")
    print(f"  worst |meas-pred| = {mp.nstr(worst,4)} (Richardson-limited)")
    print(f"  max |beta| at (1,1,1) = sqrt6/108 = {mp.nstr(mp.sqrt(6)/108,12)}")
    print(f"  Finding-7 '0.01883' = beta at seed-0 max dir "
          f"= {mp.nstr(beta_3d((mp.mpf('0.7415052'),mp.mpf('0.53854712'),mp.mpf('-0.40017126'))),8)}")


if __name__ == "__main__":
    verify()
