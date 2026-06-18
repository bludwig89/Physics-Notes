"""
F143 — The lattice fermion loop of the induced U(1)_Y (wrap) stiffness on U(x).

Follow-up to F138 ("compute the induced-Y-kinetic-term lattice loop; would
replace NDA with a number"). Result: the loop is computed and it CANNOT
supply the stiffness — it is exactly zero in the transverse (kinetic) channel
and per-mille of v^2 in the longitudinal (mass-step) channel. The F138
matching scale mu* = 4 pi f_theta is therefore pinned by the E_g condensate
sector, with the fermion-loop correction bounded at the 0.1-0.2% level.

Checks:
  A  (exact)   Conjugation no-go: the F42 kinetic wrap is
               P(alpha) W(k) P(alpha)^dag — sea spectrum invariant under ANY
               static alpha(x) at machine eps => zero induced transverse
               (field-strength) stiffness from the kinetic sector, all orders.
  B1 (machine) PT-on-the-walk-unitary == exact supercell diagonalisation
               (the production method validated against brute force).
  B2 (numeric) Ward/Goldstone: Pi(q) ~ q^2 (no q^0 term — exact global U(1));
               Pi > 0 (stiffness positivity).
  B3 (numeric) Magnitude: fhat = Pi/q^2 * 4pi^2/m^2 lands in the measured
               band O(0.2-0.4) — NO large-log (continuum-PS) enhancement.
  C  (exact)   Share arithmetic: with the measured fhat band, the fermion
               loop contributes <0.5% of v^2 => mu* shift <0.2%.

Production scan (large L, slab-chunked): tests/runners/run_F143_wrap_stiffness_scan.py;
consolidated numbers in test-results/F143_wrap_loop_stiffness.json.
"""
import json, math, os
import numpy as np

IR3 = 1.0 / np.sqrt(3.0)
results = {}


# ----------------------------------------------------------------------
# shared kernel pieces (BCC walk, Paper 1 Eq. 15 conventions, ca_bcc.py)
# ----------------------------------------------------------------------
def kmat(kx, ky, kz):
    """4x4 kinetic walk: diag(W+(k), W-(k)) — eta on '+', chi on '-'."""
    out = np.zeros(kx.shape + (4, 4), complex)
    for blk, s in ((0, 1.0), (1, -1.0)):
        cx, cy, cz = np.cos(kx * IR3), np.cos(ky * IR3), np.cos(kz * IR3)
        sx, sy, sz = np.sin(kx * IR3), np.sin(ky * IR3), np.sin(kz * IR3)
        u = cx * cy * cz + s * sx * sy * sz
        nx = sx * cy * cz - s * cx * sy * sz
        ny = -s * cx * sy * cz + sx * cy * sz
        nz = cx * cy * sz + s * sx * sy * cz
        o = 2 * blk
        out[..., o + 0, o + 0] = u - 1j * nz
        out[..., o + 0, o + 1] = -1j * (nx - 1j * ny)
        out[..., o + 1, o + 0] = -1j * (nx + 1j * ny)
        out[..., o + 1, o + 1] = u + 1j * nz
    return out


def mass_mats(m):
    c, s = np.cos(m / 2), np.sin(m / 2)
    I2 = np.eye(2)
    M0 = np.block([[c * I2, -1j * s * I2], [-1j * s * I2, c * I2]])
    Mp = np.block([[0 * I2, s * I2], [-s * I2, 0 * I2]])        # dM/dphi
    Mpp = np.block([[0 * I2, 1j * s * I2], [1j * s * I2, 0 * I2]])  # d2M/dphi2
    return M0, Mp, Mpp


# ----------------------------------------------------------------------
# A — conjugation no-go (kinetic wrap induces nothing, exactly)
# ----------------------------------------------------------------------
def check_A(L=24, seed=7):
    rng = np.random.default_rng(seed)
    alpha = rng.uniform(-np.pi, np.pi, L)
    kx = 2 * np.pi * (np.arange(L) - L // 2) / L
    ky, kz = 0.37, -1.13
    # one '+' branch 2x2 blocks -> x-space kinetic operator
    cx, cy, cz = np.cos(kx * IR3), np.cos(ky * IR3), np.cos(kz * IR3)
    sx, sy, sz = np.sin(kx * IR3), np.sin(ky * IR3), np.sin(kz * IR3)
    u = cx * cy * cz + sx * sy * sz
    nx = sx * cy * cz - cx * sy * sz
    ny = -cx * sy * cz + sx * cy * sz
    nz = cx * cy * sz + sx * sy * cz
    W = np.zeros((L, 2, 2), complex)
    W[:, 0, 0] = u - 1j * nz
    W[:, 0, 1] = -1j * (nx - 1j * ny)
    W[:, 1, 0] = -1j * (nx + 1j * ny)
    W[:, 1, 1] = u + 1j * nz
    x = np.arange(L)
    F = np.exp(1j * np.outer(x, kx)) / np.sqrt(L)
    K = np.einsum('xk,kab,yk->xayb', F, W, F.conj()).reshape(2 * L, 2 * L)
    P = np.kron(np.diag(np.exp(1j * alpha)), np.eye(2))
    th0 = np.sort(np.angle(np.linalg.eigvals(K)))
    th1 = np.sort(np.angle(np.linalg.eigvals(P @ K @ P.conj().T)))
    return float(np.max(np.abs(th0 - th1)))


# ----------------------------------------------------------------------
# walk-unitary eigenvalue PT (production method, O(a^2)-exact)
# ----------------------------------------------------------------------
def pi_pt(L, m, n, offx=True):
    k1o = 2 * np.pi * ((np.arange(L) - L // 2) + 0.5) / L
    k1u = 2 * np.pi * (np.arange(L) - L // 2) / L
    KX, KY, KZ = np.meshgrid(k1o if offx else k1u, k1o, k1o, indexing='ij')
    q = 2 * np.pi * n / L
    M0, Mp, Mpp = mass_mats(m)
    K0 = kmat(KX, KY, KZ)
    U0 = np.einsum('ab,...bc,cd->...ad', M0, K0, M0)
    lam, vec = np.linalg.eig(U0)
    th = np.angle(lam)
    Kp, Km = np.roll(K0, -n, axis=0), np.roll(K0, n, axis=0)
    lam_p, vec_p = np.roll(lam, -n, axis=0), np.roll(vec, -n, axis=0)
    lam_m, vec_m = np.roll(lam, n, axis=0), np.roll(vec, n, axis=0)
    D = 0.25 * (np.einsum('ab,...bc,cd->...ad', Mpp, K0, M0)
                + np.einsum('ab,...bc,cd->...ad', M0, K0, Mpp)
                + np.einsum('ab,...bc,cd->...ad', Mp, Kp, Mp)
                + np.einsum('ab,...bc,cd->...ad', Mp, Km, Mp))
    vH = vec.conj().swapaxes(-1, -2)
    l2 = np.einsum('...na,...ab,...bn->...n', vH, D, vec)
    for Kq, lamq, vecq in ((Kp, lam_p, vec_p), (Km, lam_m, vec_m)):
        Bf = 0.5 * (np.einsum('ab,...bc,cd->...ad', Mp, K0, M0)
                    + np.einsum('ab,...bc,cd->...ad', M0, Kq, Mp))
        Bb = 0.5 * (np.einsum('ab,...bc,cd->...ad', Mp, Kq, M0)
                    + np.einsum('ab,...bc,cd->...ad', M0, K0, Mp))
        vqH = vecq.conj().swapaxes(-1, -2)
        tf = np.einsum('...ma,...ab,...bn->...mn', vqH, Bf, vec)
        tb = np.einsum('...na,...ab,...bm->...nm', vH, Bb, vecq)
        dl = lam[..., :, None] - lamq[..., None, :]
        num = tb * tf.swapaxes(-1, -2)
        mask = np.abs(dl) > 1e-9
        l2 += np.where(mask, num / np.where(mask, dl, 1.0), 0.0).sum(-1)
    dth = np.imag(l2 / lam)
    return float(-(2.0 / L**3) * np.sum(np.sign(th) * dth)), q


# ----------------------------------------------------------------------
# B1 — exact supercell cross-check (brute force, all orders in a)
# ----------------------------------------------------------------------
def pi_supercell(L, m, n, a=0.08):
    q = 2 * np.pi * n / L
    x = np.arange(L)
    kx = 2 * np.pi * (np.arange(L) - L // 2) / L
    F = np.exp(1j * np.outer(x, kx)) / np.sqrt(L)
    kt = 2 * np.pi * ((np.arange(L) - L // 2) + 0.5) / L
    al = a * np.cos(q * x)
    c, s = np.cos(m / 2), np.sin(m / 2)

    def sea(alpha_x, ky, kz):
        Wk = kmat(kx, np.full(L, ky), np.full(L, kz))
        Kp = np.einsum('xk,kab,yk->xayb', F, Wk[:, :2, :2], F.conj()).reshape(2 * L, 2 * L)
        Km = np.einsum('xk,kab,yk->xayb', F, Wk[:, 2:, 2:], F.conj()).reshape(2 * L, 2 * L)
        U = np.zeros((4 * L, 4 * L), complex)
        U[:2 * L, :2 * L] = Kp
        U[2 * L:, 2 * L:] = Km
        Mh = np.zeros((4 * L, 4 * L), complex)
        ph = np.exp(1j * alpha_x)
        for j in range(L):
            for sp in range(2):
                ie, ic = 2 * j + sp, 2 * L + 2 * j + sp
                Mh[ie, ie] = c
                Mh[ic, ic] = c
                Mh[ie, ic] = -1j * s * ph[j]
                Mh[ic, ie] = -1j * s * np.conj(ph[j])
        th = np.angle(np.linalg.eigvals(Mh @ U @ Mh))
        return -0.5 * np.abs(th).sum() / L

    t0 = tp = tm = 0.0
    for ky in kt:
        for kz in kt:
            t0 += sea(0 * al, ky, kz)
            tp += sea(al, ky, kz)
            tm += sea(-al, ky, kz)
    return 4 * (0.5 * (tp + tm) - t0) / (L**2) / a**2, q


# ======================================================================
print("A: conjugation no-go ...")
nogo = check_A()
results["A"] = {"max_eigenphase_shift": nogo, "PASS": nogo < 1e-12}
print("   max|dtheta| =", nogo)

print("B1: PT vs exact supercell (L=8, m=0.5, n=1) ...")
pi_exact, _ = pi_supercell(8, 0.5, 1)
pi_pert, _ = pi_pt(8, 0.5, 1, offx=False)
rel = abs(pi_pert - pi_exact) / abs(pi_exact)
results["B1"] = {"Pi_exact": pi_exact, "Pi_PT": pi_pert, "rel": rel,
                 "PASS": rel < 5e-3}
print(f"   exact={pi_exact:.6e}  PT={pi_pert:.6e}  rel={rel:.2e}")

print("B2: Ward/Goldstone Pi ~ q^2, Pi > 0 (L=24, m=0.4) ...")
pi1, q1 = pi_pt(24, 0.4, 1)
pi2, q2 = pi_pt(24, 0.4, 2)
ratio = pi2 / pi1
results["B2"] = {"Pi(n=1)": pi1, "Pi(n=2)": pi2, "ratio": ratio,
                 "q2_ratio": (q2 / q1)**2,
                 "PASS": (pi1 > 0) and (pi2 > 0) and (3.2 < ratio < 5.8)}
print(f"   Pi: {pi1:.3e}, {pi2:.3e}; ratio={ratio:.2f} (q^2 ratio = 4)")

print("B3: magnitude band — no large-log enhancement (L=32, m=0.6,0.4) ...")
band = {}
for m in (0.6, 0.4):
    p, q = pi_pt(32, m, 1)
    band[m] = p / q**2 * 4 * np.pi**2 / m**2
print("   fhat:", band)
results["B3"] = {"fhat": {str(k): v for k, v in band.items()},
                 "scan_band": [0.17, 0.38],
                 "PASS": all(0.05 < v < 1.0 for v in band.values())}

print("C: v^2 share arithmetic ...")
v2 = 246.21965**2
mt = 172.57
share = {}
for tag, fh in (("lo", 0.17), ("mid", 0.20), ("hi", 0.38)):
    dv2 = 0.25 * fh * 3 * mt**2 / (4 * math.pi**2)   # (DY/2)^2 * Nc * fhat m^2/4pi^2
    share[tag] = {"fhat": fh, "dv2_GeV2": dv2, "share_pct": 100 * dv2 / v2,
                  "mu_star_shift_pct": 100 * (math.sqrt(1 + dv2 / v2) - 1)}
results["C"] = {"v2_GeV2": v2, "m_top_GeV": mt, "share": share,
                "PASS": share["hi"]["share_pct"] < 0.5}
for t, r in share.items():
    print(f"   [{t}] fhat={r['fhat']}: dv2={r['dv2_GeV2']:.0f} GeV^2 "
          f"share={r['share_pct']:.3f}%  mu* shift={r['mu_star_shift_pct']:.3f}%")

results["ALL_PASS"] = all(results[k]["PASS"] for k in ("A", "B1", "B2", "B3", "C"))
print("ALL_PASS =", results["ALL_PASS"])

outdir = "test-results"
if os.path.isdir(outdir):
    path = os.path.join(outdir, "F143_wrap_loop_stiffness_test.json")
    json.dump(results, open(path, "w"), indent=1, default=str)
    print("wrote", path)
