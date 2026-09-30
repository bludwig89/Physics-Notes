"""
Verification script for the F389/F390 photon-fermion momentum investigation.

Self-contained: re-implements, from their source, exactly three casim objects --
    lattice.bcc._bcc_uvec
    gauge.charge_coupling.bcc_curl_symbol
    gauge.photon.pair_dispersion / photon_step_spectral / build_beam_packet / build_pair_mode
    gauge.em_photon_sourcing.split_transverse_longitudinal
-- and measures the two structural defects the investigation found.

No casim import, so it runs anywhere numpy runs.  Every number quoted in
docs/audits/2026-09-16-photon-fermion-momentum-investigation.md comes from here.

    python3 verify_photon_momentum_diagnosis.py
"""
import numpy as np

ROOT3 = np.sqrt(3.0)
c_lat = 1.0 / ROOT3
BAR = "=" * 94


# ---------------------------------------------------------------- casim, re-implemented
def _bcc_uvec(kx, ky, kz, sign='+'):
    """lattice/bcc.py:81 -- verbatim."""
    inv = c_lat
    cx, cy, cz = np.cos(kx * inv), np.cos(ky * inv), np.cos(kz * inv)
    sx, sy, sz = np.sin(kx * inv), np.sin(ky * inv), np.sin(kz * inv)
    s = 1.0 if sign == '+' else -1.0
    u = cx * cy * cz + s * sx * sy * sz
    nx = sx * cy * cz - s * cx * sy * sz
    ny = -s * cx * sy * cz + sx * cy * sz
    nz = cx * cy * sz + s * sx * sy * cz
    return u, nx, ny, nz


def bcc_dispersion(kx, ky, kz, sign='+'):
    u, _, _, _ = _bcc_uvec(kx, ky, kz, sign)
    return np.arccos(np.clip(u, -1.0, 1.0))


def pair_dispersion(kx, ky, kz):
    """gauge/photon.py:64 -- Omega_pair."""
    return (bcc_dispersion(kx / 2, ky / 2, kz / 2, '+')
            + bcc_dispersion(kx / 2, ky / 2, kz / 2, '-'))


def bcc_curl_symbol(KX, KY, KZ):
    """gauge/charge_coupling.py:190 -- verbatim."""
    _, nxp, nyp, nzp = _bcc_uvec(KX / 2, KY / 2, KZ / 2, '+')
    _, nxm, nym, nzm = _bcc_uvec(-KX / 2, -KY / 2, -KZ / 2, '+')
    C = [nxp - nxm, nyp - nym, nzp - nzm]

    def gn(S):
        return np.roll(S[::-1, ::-1, ::-1], 1, axis=(0, 1, 2))
    return tuple(0.5 * (c - gn(c)) for c in C)


def kgrid(L):
    k = np.fft.fftfreq(L) * 2 * np.pi
    return np.meshgrid(k, k, k, indexing='ij')


def photon_step_spectral(E, B, Om):
    """gauge/photon.py:88 -- rotate (E,B) by Omega_pair(k) per mode."""
    c, s = np.cos(Om), np.sin(Om)
    Ek = np.fft.fftn(E, axes=(-3, -2, -1))
    Bk = np.fft.fftn(B, axes=(-3, -2, -1))
    return (np.fft.ifftn(c * Ek + s * Bk, axes=(-3, -2, -1)).real,
            np.fft.ifftn(-s * Ek + c * Bk, axes=(-3, -2, -1)).real)


def split_TL(V, C):
    """gauge/em_photon_sourcing.py:112 -- Chat(k)-transverse/longitudinal split."""
    Cx, Cy, Cz = C
    C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
    nz = C2 > 1e-14
    Vk = [np.fft.fftn(V[a]) for a in range(3)]
    CdV = Cx * Vk[0] + Cy * Vk[1] + Cz * Vk[2]
    VT, VL = [], []
    for a, c in enumerate((Cx, Cy, Cz)):
        p = np.zeros_like(Vk[a])
        p[nz] = c[nz] * CdV[nz] / C2[nz]
        VL.append(p)
        VT.append(Vk[a] - p)
    return (np.array([np.fft.ifftn(v).real for v in VT]),
            np.array([np.fft.ifftn(v).real for v in VL]))


def build_beam_packet(L, m_index, axis=0, pol_axis=None, sigma=3.0, center=None):
    """gauge/photon.py:342 -- E = Re F, B = Im F, BOTH in component pol_axis."""
    if pol_axis is None:
        pol_axis = (axis + 1) % 3
    k0 = 2 * np.pi * m_index / L
    if center is None:
        center = [L / 4 if a == axis else L / 2 for a in range(3)]
    sig = np.broadcast_to(np.asarray(sigma, float), (3,))
    X = np.meshgrid(*[np.arange(L, dtype=float)] * 3, indexing='ij')
    d = [np.remainder(X[a] - center[a] + L / 2, L) - L / 2 for a in range(3)]
    env = np.exp(-sum((d[a] / sig[a]) ** 2 for a in range(3)) / 2)
    F = env * np.exp(1j * k0 * d[axis])
    E = np.zeros((3, L, L, L)); B = np.zeros((3, L, L, L))
    E[pol_axis] = F.real
    B[pol_axis] = F.imag
    kv = np.zeros(3); kv[axis] = k0
    return E, B, kv, pol_axis


def build_beam_packet_RS_null(L, m_index, axis=0, sigma=3.0, center=None):
    """PROPOSED FIX: complex circular polarization e = (e1 + i e2)/sqrt(2),
    so E _|_ B, |E| = |B|, and F.F = 0 (a genuine null Riemann-Silberstein field)."""
    a1, a2 = (axis + 1) % 3, (axis + 2) % 3
    k0 = 2 * np.pi * m_index / L
    if center is None:
        center = [L / 4 if a == axis else L / 2 for a in range(3)]
    sig = np.broadcast_to(np.asarray(sigma, float), (3,))
    X = np.meshgrid(*[np.arange(L, dtype=float)] * 3, indexing='ij')
    d = [np.remainder(X[a] - center[a] + L / 2, L) - L / 2 for a in range(3)]
    env = np.exp(-sum((d[a] / sig[a]) ** 2 for a in range(3)) / 2)
    f = env * np.exp(1j * k0 * d[axis])
    e = np.zeros(3, complex); e[a1] = 1 / np.sqrt(2); e[a2] = 1j / np.sqrt(2)
    F = np.array([e[a] * f for a in range(3)])
    kv = np.zeros(3); kv[axis] = k0
    return F.real, F.imag, kv


def build_pair_mode(L, m_index, khat, e1):
    """gauge/photon.py:294 -- E || e1, B || e2 = khat x e1  (correct, E _|_ B)."""
    khat = np.asarray(khat, float); khat = khat / np.linalg.norm(khat)
    e1 = np.asarray(e1, float); e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(khat, e1); e2 /= np.linalg.norm(e2)
    Ek = np.zeros((3, L, L, L), complex); Bk = np.zeros((3, L, L, L), complex)
    idx = tuple(int(round(m_index)) for _ in range(3))
    cid = tuple((-int(round(m_index))) % L for _ in range(3))
    for a in range(3):
        Ek[a][idx] = e1[a]; Bk[a][idx] = e2[a]
        Ek[a][cid] = np.conj(e1[a]); Bk[a][cid] = np.conj(e2[a])
    return (np.array([np.fft.ifftn(Ek[a]).real for a in range(3)]),
            np.array([np.fft.ifftn(Bk[a]).real for a in range(3)]))


def P(E, B):
    """core/observers.py Momentum.P_field  ==  sum_x E x B."""
    return np.stack([E[1] * B[2] - E[2] * B[1],
                     E[2] * B[0] - E[0] * B[2],
                     E[0] * B[1] - E[1] * B[0]]).sum((1, 2, 3))


def Pmax(E, B):
    return np.abs(np.stack([E[1] * B[2] - E[2] * B[1],
                            E[2] * B[0] - E[0] * B[2],
                            E[0] * B[1] - E[1] * B[0]])).max()


# ================================================================ DEFECT 1
def defect_1(L=16, SIG=3.0):
    print(BAR)
    print("DEFECT 1 -- build_beam_packet carries EXACTLY ZERO field momentum")
    print(BAR)
    KX, KY, KZ = kgrid(L)
    C = bcc_curl_symbol(KX, KY, KZ)
    Om = pair_dispersion(KX, KY, KZ)

    print()
    print("1a.  The beam helper F390 uses.  E and B occupy the SAME Cartesian component,")
    print("     so E || B pointwise and E x B vanishes identically.")
    print("      axis pol  m   max|ExB| pointwise   |sum ExB|     field energy")
    for axis in (0, 1, 2):
        for m in (2, 4):
            E, B, kv, pol = build_beam_packet(L, m, axis=axis, sigma=SIG)
            print("       %d    %d   %d   %.3e            %.3e     %.4f" % (
                axis, pol, m, Pmax(E, B), np.linalg.norm(P(E, B)),
                float(np.sqrt((E ** 2 + B ** 2).sum()))))

    print()
    print("1b.  After the Chat-transverse projection F388/F390 apply before injection,")
    print("     the field momentum is still only machine noise:")
    print("      axis  m   |sum ExB| after projection   cos(P, khat)")
    for axis in (0, 1, 2):
        for m in (2, 4):
            E, B, kv, pol = build_beam_packet(L, m, axis=axis, sigma=SIG)
            ET, _ = split_TL(E, C); BT, _ = split_TL(B, C)
            p = P(ET, BT); n = np.linalg.norm(p); kh = kv / np.linalg.norm(kv)
            print("       %d    %d   %.4e                  %+.6f" % (axis, m, n, float(p @ kh / n)))

    print()
    print("1c.  PROPOSED FIX -- a genuine null Riemann-Silberstein beam: complex circular")
    print("     polarization e = (e1 + i e2)/sqrt(2), so F.F = 0, i.e. E _|_ B and |E| = |B|.")
    print("      axis  m   |sum ExB|   cos(P,khat)   E.B/(|E||B|)   |E_L|/|E| (Chat-leak)")
    for axis in (0, 1, 2):
        for m in (2, 4):
            E, B, kv = build_beam_packet_RS_null(L, m, axis=axis, sigma=SIG)
            p = P(E, B); n = np.linalg.norm(p); kh = kv / np.linalg.norm(kv)
            eb = float((E * B).sum() / (np.linalg.norm(E) * np.linalg.norm(B)))
            leak = np.linalg.norm(split_TL(E, C)[1]) / np.linalg.norm(E)
            print("       %d    %d   %.4f    %+.6f      %+.2e       %.4f" % (
                axis, m, n, float(p @ kh / n), eb, leak))

    print()
    print("1d.  Is the fixed beam's momentum conserved by casim's OWN free propagator?")
    for nm, (E, B) in (("build_pair_mode k=(1,1,1)", build_pair_mode(L, 2, [1, 1, 1], [1, 0, 0])),
                       ("RS-null beam axis=0 m=2", build_beam_packet_RS_null(L, 2, axis=0, sigma=SIG)[:2]),
                       ("RS-null beam axis=1 m=2", build_beam_packet_RS_null(L, 2, axis=1, sigma=SIG)[:2])):
        p0 = P(E, B)
        for _ in range(40):
            E, B = photon_step_spectral(E, B, Om)
        p1 = P(E, B)
        print("       %-28s |P0|=%.6f  |P40|=%.6f  rel drift %.3e" % (
            nm, np.linalg.norm(p0), np.linalg.norm(p1),
            np.linalg.norm(p1 - p0) / max(np.linalg.norm(p0), 1e-30)))


# ================================================================ DEFECT 2
def defect_2(L=16):
    print()
    print(BAR)
    print("DEFECT 2 -- bcc_curl_symbol is not the symbol of a curl")
    print(BAR)
    KX, KY, KZ = kgrid(L)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    C = np.stack([Cx, Cy, Cz]); K = np.stack([KX, KY, KZ])
    R = np.diag([1.0, -1.0, 1.0])
    RK = np.einsum('ij,jabc->iabc', R, K)
    nC = np.linalg.norm(C, axis=0); nK = np.linalg.norm(K, axis=0)
    nRK = np.linalg.norm(RK, axis=0)
    m = (nC > 1e-12) & (nK > 1e-12)

    print()
    print("2a.  Direction.  A curl's symbol points along k.  This one does not.")
    cosK = (C * K).sum(0)[m] / (nC[m] * nK[m])
    print("       cos(C, k)       min %.9f   max %.9f" % (cosK.min(), cosK.max()))
    print("       modes with cos(C,k) < 0.99 :  %d of %d" % ((cosK < 0.99).sum(), m.sum()))
    print("     The k->0 limit is C ~ R.k with R = diag(1,-1,1), inherited from")
    print("     bcc_spin_axis's y-sign flip (the Bisio walk's chirality convention).")
    print("     That reflection reproduces all three angles F387 measured:")
    for nm, v in (("cubic axis (1,0,0)", [1, 0, 0]), ("face diag (1,1,0)", [1, 1, 0]),
                  ("body diag (1,1,1)", [1, 1, 1])):
        v = np.array(v, float); rv = R @ v
        ang = np.degrees(np.arccos(v @ rv / (np.linalg.norm(v) * np.linalg.norm(rv))))
        print("       angle(R.k, k) on %-20s = %.6f deg" % (nm, ang))

    print()
    print("2b.  THE DEFINING IDENTITY OF A CURL:  curl(grad phi) = 0, i.e. C x G = 0.")
    def xn(A, Bv):
        X = np.stack([A[1] * Bv[2] - A[2] * Bv[1], A[2] * Bv[0] - A[0] * Bv[2],
                      A[0] * Bv[1] - A[1] * Bv[0]])
        return np.linalg.norm(X, axis=0)
    for nm, G in (("spectral   G = k", K),
                  ("fwd-diff   G_j = e^{ik_j}-1",
                   np.stack([np.exp(1j * KX) - 1, np.exp(1j * KY) - 1, np.exp(1j * KZ) - 1]))):
        nG = np.linalg.norm(G, axis=0)
        mm = m & (nG > 1e-12)
        rel = xn(C.astype(complex), G)[mm] / (nC[mm] * nG[mm])
        print("       |C x G| / (|C||G|)  with %-26s :  max %.6f   mean %.6f" % (nm, rel.max(), rel.mean()))
    print("       control, a TRUE curl symbol C = k                         :  max %.3e" % (
        (xn(K, K)[m] / nK[m] ** 2).max()))
    print()
    print("     The identity the codebase cites as its sanity check, C.(C x x) == 0, is")
    print("     VACUOUS -- it holds for every vector field whatsoever, so it carries no")
    print("     information about whether C is a curl.  The no-monopole gate i.Chat.B = 0")
    print("     tests exactly that vacuous identity.  The one that fails was never tested.")

    print()
    print("2c.  On the coordinate axes the reflection is exact at EVERY grid mode,")
    print("     which is the direct mechanism of F390's axis-dependent sign inversion:")
    print("       axis   m    Chat . khat      Chat")
    for axis in (0, 1, 2):
        for mi in (1, 2, 3, 4):
            idx = [0, 0, 0]; idx[axis] = mi
            c = np.array([Cx[tuple(idx)], Cy[tuple(idx)], Cz[tuple(idx)]])
            kk = np.array([KX[tuple(idx)], KY[tuple(idx)], KZ[tuple(idx)]])
            cd = c / np.linalg.norm(c); kd = kk / np.linalg.norm(kk)
            print("        %d     %d    %+.9f    %s" % (axis, mi, cd @ kd, np.round(cd, 6)))
    print()
    print("     Chat = +khat on x and z, but Chat = -khat on y, at every m.  A y-propagating")
    print("     beam therefore has its rotation generator exactly reversed.  Note also that")
    print("     build_beam_packet's default pol_axis = (axis+1)%3 puts each of F390's three")
    print("     beams in a DIFFERENT relation to the reflected (y) axis: axis=0 has the")
    print("     polarization on y, axis=1 has the propagation on y, axis=2 has neither.")


if __name__ == "__main__":
    defect_1()
    defect_2()
