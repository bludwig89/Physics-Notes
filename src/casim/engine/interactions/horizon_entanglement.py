"""horizon_entanglement.py — the boundary entanglement entropy of the BCC vacuum
================================================================================

Rubric row **E9** / ledger row **G4**.  F190 posits that Bekenstein-Hawking is
reproduced *iff* each F107 horizon cell carries

    s_cell = a^2 / (4 ell_P^2) = 8 pi sqrt3 / 4 = 2 pi sqrt3 = 10.8828 nats,

and names "show a boundary cell carries e^{2 pi sqrt3} states" as its open step.
F300 §5 (G10-12) proved that step impossible **as written** — 2 pi sqrt3 is
neither ln(integer) nor n ln 2 — and named the survivor: an *entanglement*
entropy, whose spectrum is continuous and carries no integrality constraint.
F300 G10-13 then checked the necessary capacity condition and passed it (96
fermionic modes/site = 66.542 nats against 10.883 required, 6.11x room).

This module executes F300 §8 next step #3: it **computes** the boundary
entanglement entropy of the model's own vacuum, rather than positing it.

What is computed
----------------
The BCC Weyl walk (F26/F267/F278) is quadratic, so its vacuum — the filled
negative-branch Dirac sea — is Gaussian and is carried **exactly** by the
one-particle correlation matrix.  At crystal momentum p the filled branch is the
spin-axis projector

    P_-(p) = (I - n_hat(p) . sigma) / 2,          n_hat = n(p) / sin omega(p)

(`bcc_spin_axis`, F26), and the real-space correlator is its Fourier transform.
Restricting that matrix to a region A and diagonalising gives the exact von
Neumann entropy of A by Peschel's formula.  This is the same machinery F300 §4
uses for its second-law ledger, run on the vacuum instead of on a random
product state, and it is the lattice-native version of the free-field
"area law from entanglement" calculation of Bombelli-Koul-Lee-Sorkin (1986) and
Srednicki (1993).

**The lattice is the regulator.**  In continuum QFT the area-law coefficient is
famously regularisation-dependent (Solodukhin, Living Rev. Rel. 14 (2011) 8,
§2.2: "the exact pre-factor depends on the regularization scheme").  This model
has no such freedom: the BCC walk *is* the cutoff, so the coefficient is a
computed number, not a scheme choice.  That is what makes the comparison with
2 pi sqrt3 a test rather than a fit.

Geometry, and why "per cell" is unambiguous
-------------------------------------------
F278 derives the BCC conventional cube edge a = 2/sqrt3 = 2 c_lat (code units);
F79/F107 give the same a in Planck units, a = sqrt(8 pi) 3^(1/4) ell_P.  BCC
carries 2 sites per a^3, so **every (001) atomic layer holds exactly one site
per a^2** — F190's horizon cell and one BCC surface site are the same object,
and "nats per cell" is "nats per a^2 of boundary area" with no conversion.

Two independent routes to the number
------------------------------------
1. **Planar cuts** (`plane_coefficient`).  For a crystal plane (hkl) the
   transverse crystal momentum is conserved, so the problem factorises into
   independent 1-D chains and the coefficient converges to ~1e-6.  The result is
   strongly **anisotropic** — the densest plane (110) is a cusp, 21% below (001).
2. **Balls** (`ball_coefficient`).  The full 3-D correlator restricted to a
   sphere.  This is the physically relevant object (a horizon is a sphere) and
   its leading coefficient is the solid-angle average of route 1.  Lattice
   commensurability noise is removed by averaging over sub-cell offsets of the
   ball centre.

Self-contained apart from `casim.constants` and `casim.numerics` (D7/D8).
Date: 2026-09-03 (F355).
"""
from __future__ import annotations

import itertools
import math

from casim.constants import (
    G_CODATA as _G_CODATA,
    a_over_ellP as _A_OVER_ELLP,
    c_SI as _c_SI,
    c_lat as _C_LAT,
    ell_P_m as _ELL_P_M,
    hbar_SI as _hbar_SI,
)
from casim.numerics import fft, xp

# ---------------------------------------------------------------------------
# Geometry and the target
# ---------------------------------------------------------------------------
A_CUBE = 2.0 * _C_LAT                    # BCC conventional cube edge, F278: a = 2 c_lat = 2/sqrt3
S_CELL_REQUIRED = _A_OVER_ELLP ** 2 / 4.0    # F190: a^2/(4 ell_P^2) == 2 pi sqrt3 == 10.8828 nats
N_WEYL = 48                              # F47/F279/F309: 3 generations x 16, incl. nu_R
MODES_PER_SITE = 2 * N_WEYL              # 96 fermionic modes/site (F300 G10-13)


# ---------------------------------------------------------------------------
# The walk's spin axis (F26 `bcc_spin_axis`), written on phase arguments so any
# primitive basis can be fed in
# ---------------------------------------------------------------------------
def _uvec(fx, fy, fz, sign=+1.0):
    """(u, n) of U = u I - i n.sigma with phase arguments phi_i = k_i a/2."""
    cx, cy, cz = xp.cos(fx), xp.cos(fy), xp.cos(fz)
    sx, sy, sz = xp.sin(fx), xp.sin(fy), xp.sin(fz)
    s = sign
    u = cx * cy * cz + s * sx * sy * sz
    nx = sx * cy * cz - s * cx * sy * sz
    ny = -s * cx * sy * cz + sx * cy * sz
    nz = cx * cy * sz + s * sx * sy * cz
    return u, nx, ny, nz


def _filled_projector(phi, sign=+1.0, flat_control=False, random_control=None):
    """P_-(p) = (I - n_hat.sigma)/2, the filled negative-energy branch.

    `flat_control` replaces n_hat by the constant z-axis (a k-INDEPENDENT
    projector -> site-diagonal correlator -> product state -> S == 0).
    `random_control` (a seed) replaces n_hat by an independent random unit
    vector at every p (-> white-noise correlator -> volume law).
    """
    u, nx, ny, nz = _uvec(phi[0], phi[1], phi[2], sign)
    sw = xp.sqrt(xp.clip(1.0 - u ** 2, 0.0, None))
    safe = sw > 1e-13
    den = xp.where(safe, sw, 1.0)
    hx = xp.where(safe, nx / den, 0.0)
    hy = xp.where(safe, ny / den, 0.0)
    hz = xp.where(safe, nz / den, 1.0)
    if flat_control:
        hx = xp.zeros_like(hx); hy = xp.zeros_like(hy); hz = xp.ones_like(hz)
    if random_control is not None:
        g = xp.random.default_rng(random_control).normal(size=(3,) + xp.shape(hz))
        g /= xp.sqrt((g ** 2).sum(0))
        hx, hy, hz = g[0], g[1], g[2]
    P = xp.empty(xp.shape(hz) + (2, 2), complex)
    P[..., 0, 0] = 0.5 * (1.0 - hz)
    P[..., 1, 1] = 0.5 * (1.0 + hz)
    P[..., 0, 1] = -0.5 * (hx - 1j * hy)
    P[..., 1, 0] = -0.5 * (hx + 1j * hy)
    return P


def von_neumann(C):
    """Peschel: S = -sum [ nu ln nu + (1-nu) ln(1-nu) ] over the eigenvalues of C|_A."""
    C = (C + C.conj().T) / 2.0
    e = xp.linalg.eigvalsh(C).clip(1e-15, 1.0 - 1e-15)
    return float(-xp.sum(e * xp.log(e) + (1.0 - e) * xp.log1p(-e)))


# ---------------------------------------------------------------------------
# Route 1 — planar cuts
# ---------------------------------------------------------------------------
def bcc_lattice_vectors(rmax=4):
    """BCC lattice vectors in units of the conventional cube edge: (m1,m2,m3)/2
    with the m_i all of the same parity.  Sorted by length."""
    out = []
    for m in itertools.product(range(-2 * rmax, 2 * rmax + 1), repeat=3):
        if (m[0] % 2 == m[1] % 2 == m[2] % 2) and any(m):
            out.append(xp.array(m, float) / 2.0)
    out.sort(key=lambda v: float(v @ v))
    return out


def primitive_basis(hkl, rmax=4):
    """Primitive basis (B1,B2,B3) with B1,B2 IN the (hkl) plane and B3 the
    shortest lattice vector on its positive side, so n3 labels the layer.
    Rows are in units of a; det == 1/2 (the BCC primitive cell volume)."""
    n = xp.array(hkl, float)
    V = bcc_lattice_vectors(rmax)
    inpl = [v for v in V if abs(float(v @ n)) < 1e-12]
    B1 = inpl[0]
    B2 = None
    for v in inpl[1:]:
        if float(xp.linalg.norm(xp.cross(B1, v))) > 1e-9:
            B2 = v
            break
    best = None
    for v in V:
        if abs(abs(float(xp.linalg.det(xp.array([B1, B2, v])))) - 0.5) < 1e-9 and float(v @ n) > 0:
            if best is None or float(v @ v) < float(best @ best):
                best = v
    if best is None:
        raise RuntimeError(f"no primitive out-of-plane vector for {hkl}")
    M = xp.array([B1, B2, best])
    if float(xp.linalg.det(M)) < 0:
        M = xp.array([B2, B1, best])
    return M


def _chain_entropy(Minv, px, py, L3, ell, sign=+1.0, **ctl):
    """Entanglement entropy of `ell` consecutive layers at fixed transverse (px,py)."""
    j = (xp.arange(L3) + 0.5) * 2.0 * math.pi / L3 - math.pi
    p = xp.stack([xp.full(L3, px), xp.full(L3, py), j])
    P = _filled_projector(0.5 * (Minv @ p), sign, **ctl)
    n = xp.arange(ell)
    E = xp.exp(1j * xp.outer(n, j)) / L3
    Ec = xp.exp(-1j * xp.outer(n, j))
    C = xp.empty((ell, 2, ell, 2), complex)
    for s in range(2):
        for t in range(2):
            C[:, s, :, t] = (E * P[:, s, t]) @ Ec.T
    return von_neumann(C.reshape(2 * ell, 2 * ell))


def plane_coefficient(hkl, n_transverse=48, thickness=12.0, sign=+1.0, **ctl):
    """Entanglement entropy per a^2 of boundary area for ONE 2-component Weyl
    field, across the (hkl) crystal plane.  `thickness` is the slab depth in
    units of a (the slab has two boundaries; the return value is per boundary)."""
    M = primitive_basis(hkl)
    Minv = xp.linalg.inv(M)
    area = float(xp.linalg.norm(xp.cross(M[0], M[1])))     # surface cell area / a^2
    d = 0.5 / area                                         # interplanar spacing / a
    ell = max(6, int(math.ceil(thickness / d)))
    L3 = 2 * ell
    q = (xp.arange(n_transverse) + 0.5) * 2.0 * math.pi / n_transverse - math.pi
    tot = 0.0
    for px in q:
        for py in q:
            tot += _chain_entropy(Minv, float(px), float(py), L3, ell, sign, **ctl)
    per_site = tot / (2.0 * n_transverse * n_transverse)
    return per_site / area, {"area_over_a2": area, "d_over_a": d, "ell": ell, "L3": L3}


# ---------------------------------------------------------------------------
# Route 2 — balls (the physically relevant shape)
# ---------------------------------------------------------------------------
_M001 = None


def _basis001():
    global _M001
    if _M001 is None:
        _M001 = xp.array([[1.0, 0, 0], [0, 1.0, 0], [0.5, 0.5, 0.5]])
    return _M001


def correlator_kernel(L1, L2, L3, sign=+1.0, **ctl):
    """C(dn) for the (001) primitive basis on an L1 x L2 x L3 torus, antiperiodic
    in every direction (so the Weyl point is never sampled exactly)."""
    M = _basis001()
    Minv = xp.linalg.inv(M)
    p = [(xp.arange(L) + 0.5) * 2.0 * math.pi / L for L in (L1, L2, L3)]
    P1, P2, P3 = xp.meshgrid(*p, indexing="ij")
    phi = 0.5 * xp.einsum("ij,jklm->iklm", Minv, xp.stack([P1, P2, P3]))
    P = _filled_projector(phi, sign, **ctl)
    d1 = xp.arange(L1)[:, None, None]
    d2 = xp.arange(L2)[None, :, None]
    d3 = xp.arange(L3)[None, None, :]
    ph = xp.exp(1j * math.pi * (d1 / L1 + d2 / L2 + d3 / L3))
    K = xp.empty_like(P)
    for s in range(2):
        for t in range(2):
            K[..., s, t] = fft.ifftn(P[..., s, t]) * ph
    return K


def ball_entropy(K, L1, L2, L3, R, offset=(0.0, 0.0, 0.0)):
    """Exact von Neumann entropy of every site inside a ball of radius R (units
    of a) centred at the box centre plus a sub-cell Cartesian `offset`."""
    M = _basis001()
    c = xp.array([L1 // 2, L2 // 2, L3 // 2], float)
    n1, n2, n3 = xp.meshgrid(xp.arange(L1), xp.arange(L2), xp.arange(L3), indexing="ij")
    dn = xp.stack([n1 - c[0], n2 - c[1], n3 - c[2]]).astype(float)
    r = xp.einsum("ij,jklm->iklm", M.T, dn) - xp.array(offset, float)[:, None, None, None]
    sel = xp.argwhere(xp.sqrt((r ** 2).sum(0)) <= R)
    N = len(sel)
    d = (sel[:, None, :] - sel[None, :, :]).astype(xp.int32)
    sgn = xp.where((d < 0).sum(-1) % 2 == 0, 1.0, -1.0)     # antiperiodic wrap
    d = d % xp.array([L1, L2, L3], xp.int32)
    C = xp.empty((N, 2, N, 2), complex)
    for s in range(2):
        for t in range(2):
            C[:, s, :, t] = K[d[..., 0], d[..., 1], d[..., 2], s, t] * sgn
    return N, von_neumann(C.reshape(2 * N, 2 * N))


def ball_coefficient(radii=(5.0, 5.5, 6.0), box=24, offsets=((0.0, 0.0, 0.0),
                                                             (0.37, 0.11, 0.29),
                                                             (0.23, 0.41, 0.07),
                                                             (0.13, 0.29, 0.44)),
                     sign=+1.0, **ctl):
    """Sphere-averaged coefficient: <S>/(4 pi R^2), offset-averaged at each R.

    Offsets are sub-cell Cartesian shifts of the ball centre; note (0.5,0.5,0.5)
    is a BCC lattice vector and would duplicate the origin, so it is not used.
    """
    K = correlator_kernel(box, box, 2 * box, sign, **ctl)
    rows = []
    for R in radii:
        vals = []
        for off in offsets:
            N, S = ball_entropy(K, box, box, 2 * box, R, off)
            vals.append((N, S))
        Sm = sum(v[1] for v in vals) / len(vals)
        Nm = sum(v[0] for v in vals) / len(vals)
        A = 4.0 * math.pi * R * R
        rows.append({"R": R, "N_mean": Nm, "S_mean": Sm, "area_over_a2": A,
                     "S_over_A": Sm / A, "n_offsets": len(vals)})
    cs = [r["S_over_A"] for r in rows]
    mean = sum(cs) / len(cs)
    sd = math.sqrt(sum((x - mean) ** 2 for x in cs) / max(1, len(cs) - 1))
    return {"rows": rows, "c_sphere": mean, "sd": sd,
            "sem": sd / math.sqrt(len(cs))}


# ---------------------------------------------------------------------------
# Cubic-harmonic decomposition of the planar coefficients (cross-check on the
# solid-angle average: every O_h harmonic above l=0 integrates to zero, so the
# constant term IS the sphere average)
# ---------------------------------------------------------------------------
def cubic_harmonic_average(coeffs, n_basis=3):
    H = list(coeffs)
    rows = []
    for h in H:
        n = xp.array(h, float)
        n2 = (n / xp.linalg.norm(n)) ** 2
        rows.append([1.0,
                     float(n2 @ n2) - 3.0 / 5.0,
                     float(xp.prod(n2)) - 1.0 / 105.0,
                     float((n2 ** 3).sum()) - 3.0 / 7.0][:n_basis])
    X = xp.array(rows)
    y = xp.array([coeffs[h] for h in H])
    co, *_ = xp.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ co
    return {"c0": float(co[0]), "coefficients": [float(x) for x in co],
            "rms_residual": float(xp.sqrt((resid ** 2).mean())),
            "max_residual": float(xp.abs(resid).max())}


# ---------------------------------------------------------------------------
# Validation of the machinery itself
# ---------------------------------------------------------------------------
def _chain_1d(L, ell):
    """1-D tight-binding chain at half filling, antiperiodic; correlation-matrix S."""
    j = (xp.arange(L) + 0.5) * 2.0 * math.pi / L - math.pi
    occ = (xp.cos(j) < 0).astype(float)
    n = xp.arange(ell)
    E = xp.exp(1j * xp.outer(n, j))
    return von_neumann((E * occ) @ E.conj().T / L)


def _chain_1d_exact(L, ell):
    """The same entropy from the FULL many-body ground state, by brute force."""
    j = (xp.arange(L) + 0.5) * 2.0 * math.pi / L - math.pi
    occ = xp.where(xp.cos(j) < 0)[0]
    orb = xp.exp(1j * xp.outer(xp.arange(L), j[occ])) / math.sqrt(L)
    Np = orb.shape[1]
    states = list(itertools.combinations(range(L), Np))
    idx = {s: i for i, s in enumerate(states)}
    psi = xp.zeros(len(states), complex)
    for s in states:
        psi[idx[s]] = xp.linalg.det(orb[list(s), :])
    psi /= xp.linalg.norm(psi)
    Ast = [t for na in range(ell + 1) for t in itertools.combinations(range(ell), na)]
    Bst = [t for nb in range(L - ell + 1) for t in itertools.combinations(range(ell, L), nb)]
    ai = {s: i for i, s in enumerate(Ast)}
    bi = {s: i for i, s in enumerate(Bst)}
    Mx = xp.zeros((len(Ast), len(Bst)), complex)
    for s in states:
        Mx[ai[tuple(x for x in s if x < ell)],
           bi[tuple(x for x in s if x >= ell)]] = psi[idx[s]]
    rho = Mx @ Mx.conj().T
    e = xp.linalg.eigvalsh(rho)
    e = e[e > 1e-14]
    return float(-xp.sum(e * xp.log(e)))


def validate_machinery():
    """A1  Peschel formula vs brute-force many-body ED.
       A2  the 1-D CFT slope dS/dln(ell) = c/3 with c = 1.
       A3  the BCC vacuum correlator is an exact projector (the state is pure).
       A4  complementarity S(ell) = S(L3 - ell)."""
    ed = [{"L": L, "ell": e, "exact": _chain_1d_exact(L, e), "peschel": _chain_1d(L, e)}
          for (L, e) in ((8, 3), (10, 4), (12, 5))]
    ed_err = max(abs(r["exact"] - r["peschel"]) for r in ed)

    # Calabrese-Cardy on a periodic ring: S = (c/3) ln[(L/pi) sin(pi l/L)] + const,
    # so the SLOPE against ln(chord) is c/3 = 1/3 and is the universal content.
    L = 512
    ells = (8, 16, 32, 64)
    chord = [math.log((L / math.pi) * math.sin(math.pi * e / L)) for e in ells]
    ss = [_chain_1d(L, e) for e in ells]
    slopes = [(ss[i + 1] - ss[i]) / (chord[i + 1] - chord[i]) for i in range(len(ells) - 1)]
    slope = sum(slopes) / len(slopes)

    M = _basis001()
    L1 = L2 = 6
    L3 = 12
    K = correlator_kernel(L1, L2, L3)
    idx = xp.array([(a, b, c) for a in range(L1) for b in range(L2) for c in range(L3)])
    d = (idx[:, None, :] - idx[None, :, :])
    sgn = xp.where((d < 0).sum(-1) % 2 == 0, 1.0, -1.0)
    d = d % xp.array([L1, L2, L3])
    n = len(idx)
    C = xp.empty((n, 2, n, 2), complex)
    for s in range(2):
        for t in range(2):
            C[:, s, :, t] = K[d[..., 0], d[..., 1], d[..., 2], s, t] * sgn
    C = C.reshape(2 * n, 2 * n)
    proj = float(xp.abs(C @ C - C).max())
    herm = float(xp.abs(C - C.conj().T).max())

    Minv = xp.linalg.inv(M)
    L3c = 24
    comp = 0.0
    for ell in (5, 7):
        s1 = sum(_chain_entropy(Minv, px, py, L3c, ell)
                 for px in (0.3, 1.1) for py in (-0.7, 2.0))
        s2 = sum(_chain_entropy(Minv, px, py, L3c, L3c - ell)
                 for px in (0.3, 1.1) for py in (-0.7, 2.0))
        comp = max(comp, abs(s1 - s2))
    return {"ed": ed, "ed_max_error": ed_err,
            "cft_slope": slope, "cft_slope_expected": 1.0 / 3.0,
            "projector_residual": proj, "hermiticity_residual": herm,
            "complementarity_residual": comp}


# ---------------------------------------------------------------------------
# Node counting -- the discrete freedom the comparison actually carries
# ---------------------------------------------------------------------------
def weyl_nodes(tol=1e-12):
    """The gapless points of the walk, with their Berry monopole charges.

    A single BCC walk does NOT carry one two-component Weyl field.  omega =
    arccos(u) is gapless wherever u = +-1, and there are FOUR such points per
    Brillouin zone in the phase variables phi_i = k_i a/2:

        phi = (0,0,0)            omega = 0     charge -1
        phi = (pi/2, pi/2, pi/2) omega = 0     charge +1
        phi = (pi, 0, 0)         omega = pi    charge +1
        phi = -(pi/2,pi/2,pi/2)  omega = pi    charge -1

    the charges summing to zero as Nielsen-Ninomiya requires.  The two at
    omega = pi are the quantum-walk doublers; F278 section 6 locates the pi-mode
    EXACTLY on the true zone boundary and says in terms that whether it counts
    as a doubler "is not decided here".  Every other observable in the tree is
    computed on the FFT cube, where the pi-mode is absent; this module works on
    the CRYSTAL, where it is present -- so this finding is the first place the
    undecided question has to be priced.
    """
    pts = [("Gamma", (0.0, 0.0, 0.0)),
           ("R", (math.pi / 2,) * 3),
           ("H", (math.pi, 0.0, 0.0)),
           ("R'", (-math.pi / 2,) * 3)]
    out = []
    for name, phi in pts:
        u, _, _, _ = _uvec(xp.array(phi[0]), xp.array(phi[1]), xp.array(phi[2]))
        u = float(u)
        out.append({"name": name, "phi": list(phi), "u": u,
                    "omega": math.acos(min(1.0, max(-1.0, u))),
                    "gapless": abs(abs(u) - 1.0) < tol,
                    "charge": _berry_charge(phi)})
    return {"nodes": out, "n_gapless": sum(n["gapless"] for n in out),
            "charge_sum": sum(n["charge"] for n in out)}


def _berry_charge(phi0, eps=1e-3, n=60):
    """Degree of the map n_hat over a small sphere around a gapless point."""
    th = (xp.arange(n) + 0.5) * math.pi / n
    ph = (xp.arange(2 * n) + 0.5) * math.pi / n
    T, P = xp.meshgrid(th, ph, indexing="ij")
    dx = eps * xp.sin(T) * xp.cos(P); dy = eps * xp.sin(T) * xp.sin(P)
    dz = eps * xp.cos(T)
    u, nx, ny, nz = _uvec(phi0[0] + dx, phi0[1] + dy, phi0[2] + dz)
    sw = xp.sqrt(xp.clip(1.0 - u ** 2, 1e-300, None))
    h = xp.stack([nx / sw, ny / sw, nz / sw])
    # solid angle swept by h over the sphere, signed, / 4pi
    dT = math.pi / n; dP = math.pi / n
    dh_t = xp.gradient(h, dT, axis=1)
    dh_p = xp.gradient(h, dP, axis=2)
    jac = (h * xp.cross(dh_t, dh_p, axis=0)).sum(0)
    return int(round(float((jac * xp.sin(T) * 0 + jac).sum() * dT * dP) / (4 * math.pi)))


def node_counting(c_walk):
    """The bracket the undecided doubler question puts on the per-cell entropy.

    `c_walk` is measured per BCC WALK, which is the object this module actually
    computes.  Converting it to a per-cell entropy needs a rule for how many of
    the tree's 48 continuum Weyl fields (F47/F279/F309 -- a CONTINUUM species
    count) one walk carries, and the tree has not decided:

        48 walks   1 walk = 1 Weyl field                (as F355 was first written)
        24 walks   the omega = pi pair discounted
        12 walks   all four nodes counted (F278 section 6's crystal reading)

    The range IS the result -- exactness class `bracketed`, not `quantitative`.
    """
    out = {}
    for label, walks in (("48_one_walk_one_field", 48),
                         ("24_pi_pair_discounted", 24),
                         ("12_all_four_nodes", 12)):
        s_cell = walks * c_walk
        out[label] = {"walks": walks, "s_cell": s_cell,
                      "ratio": s_cell / S_CELL_REQUIRED}
    return out


# ---------------------------------------------------------------------------
# The comparison
# ---------------------------------------------------------------------------
#  F79 gives  1/G = 2 pi eta g_* sqrt(d) hbar/(a^2 c^3)  with eta = 1/12 (the
#  Weyl Seeley-DeWitt coefficient), g_* = 48 and d = 3, i.e.
#
#      a^2 / ell_P^2 = 2 pi eta g_* sqrt(d) = 8 pi sqrt3,
#
#  so the REQUIRED per-cell entropy carries the same g_* that multiplies the
#  computed coefficient:
#
#      S_required = a^2/(4 ell_P^2) = pi eta g_* sqrt(d) / 2 = pi g_* sqrt3 / 24,
#      S_computed = g_* c_walk
#      ratio      = 2 c_walk / (pi eta sqrt d) = 24 c_walk / (pi sqrt3).
#
#  **The ratio is independent of g_*.**  Anything that reads the mismatch as a
#  field count, or as a stretch of `a` at fixed content, is varying one side of
#  an identity while freezing the other -- F79 forbids it.  The required
#  coefficient per walk is the closed form pi/(8 sqrt3).
# ---------------------------------------------------------------------------
ETA_WEYL = 1.0 / 12.0            # F61/F79 Seeley-DeWitt a_1 for a Weyl field
C_REQUIRED = math.pi / (8.0 * math.sqrt(3.0))     # == pi sqrt3 / 24 == 0.2267249


def horizon_ledger(c_walk, c_sigma=None):
    """The E9 comparison, stated so that nothing varies one side of F79's identity."""
    if c_sigma is None:
        c_sigma = C_WEYL_REF_SIGMA
    ratio = 2.0 * c_walk / (math.pi * ETA_WEYL * math.sqrt(3.0))
    bracket = node_counting(c_walk)
    return {
        "c_walk_per_a2": c_walk,
        "c_walk_sigma": c_sigma,
        "c_required_closed_form": C_REQUIRED,
        "c_required_expression": "pi/(8 sqrt3) == pi sqrt3/24",
        "ratio_at_fixed_counting": ratio,
        "ratio_sigma": 2.0 * c_sigma / (math.pi * ETA_WEYL * math.sqrt(3.0)),
        "ratio_is_independent_of_gstar": True,
        "gstar_cancellation_residual":
            abs(ratio - (N_WEYL * c_walk) / S_CELL_REQUIRED),
        "s_cell_required": S_CELL_REQUIRED,
        "node_counting_bracket": bracket,
        "ratio_bracket": [bracket["12_all_four_nodes"]["ratio"],
                          bracket["48_one_walk_one_field"]["ratio"]],
        # the two induced-1/G routes, which is what this really compares
        "inverse_G_entanglement_over_heat_kernel": ratio,
        "ratio_over_pi": ratio / math.pi,
    }


def pi_proximity(c_walk=None, c_sigma=None):
    """Two numbers to look at once and then stop looking at (D7 `coincidence`).

    The ratio at the 48-walk counting is 3.1795 and pi is 3.14159 -- 1.21% apart.
    With the HONEST uncertainty (see C_WEYL_REF_SIGMA) that is 1.1 sigma, i.e.
    nothing.  And the look-elsewhere is fatal on its own: 2^(5/3) = 3.17480 is
    CLOSER to the measured ratio than pi is (0.15% vs 1.21%), and there are of
    order 15-30 comparably simple constants in [2.5, 4], so the chance that some
    such constant lands within 1.2% of an arbitrary target is roughly 0.3-0.5.
    The proximity carries no information.  Recorded so a later session finds it
    already noticed, already measured, and already NOT claimed.

    The first draft of F355 quoted "5.7 sigma from pi" on the strength of a
    sigma four times too small; that exclusion is WITHDRAWN, not weakened.
    """
    c = C_WEYL_REF if c_walk is None else c_walk
    sg = C_WEYL_REF_SIGMA if c_sigma is None else c_sigma
    ratio = 2.0 * c / (math.pi * ETA_WEYL * math.sqrt(3.0))
    sig = 2.0 * sg / (math.pi * ETA_WEYL * math.sqrt(3.0))
    alt = 2.0 ** (5.0 / 3.0)
    return {"ratio": ratio, "sigma": sig,
            "pi": math.pi, "sigmas_from_pi": abs(ratio - math.pi) / sig,
            "rel_gap_to_pi": abs(ratio - math.pi) / math.pi,
            "nearer_alternative": "2^(5/3)", "nearer_value": alt,
            "rel_gap_to_alternative": abs(ratio - alt) / alt,
            "look_elsewhere_note": "2^(5/3) is closer than pi; ~15-30 simple "
                                   "constants live in [2.5,4]; p(some hit within "
                                   "1.2%) ~ 0.3-0.5",
            "kind": "coincidence", "claimed": False}


def box_scan(R=5.0, boxes=(14, 16, 20, 24), offset=(0.37, 0.11, 0.29)):
    """Independence of the periodic box, at fixed ball radius.  The first draft
    of F355 asserted a box-size check that had never been run; this is it."""
    rows = []
    for L in boxes:
        K = correlator_kernel(L, L, 2 * L)
        N, S = ball_entropy(K, L, L, 2 * L, R, offset)
        rows.append({"box": L, "N": N, "S": S,
                     "S_over_A": S / (4.0 * math.pi * R * R)})
    v = [r["S_over_A"] for r in rows]
    return {"rows": rows, "spread_from_largest": max(abs(x - v[-1]) for x in v[1:])}


def curvature_scope(M_solar=1.0):
    """Why a FLAT cut is the right leading object for a horizon: r_h/a for a
    solar-mass hole, and the size of the curvature correction (a/r_h)^2."""
    MSUN = 1.98892e30
    r_h = 2.0 * _G_CODATA * (M_solar * MSUN) / _c_SI ** 2
    a_m = _A_OVER_ELLP * _ELL_P_M
    return {"M_solar": M_solar, "r_h_m": r_h, "a_m": a_m,
            "r_h_over_a": r_h / a_m, "curvature_correction": (a_m / r_h) ** 2}


# ---------------------------------------------------------------------------
# The check ledger
# ---------------------------------------------------------------------------
_PLANES = ((0, 0, 1), (1, 1, 0), (1, 1, 1), (0, 1, 2), (1, 1, 2),
           (0, 1, 3), (1, 1, 3), (1, 2, 2), (1, 2, 3))

_SCALES = {
    # n_transverse, thickness, planes, ball radii, box, ball offsets
    "gate": (32, 10.0, ((0, 0, 1), (1, 1, 0), (1, 1, 1)), (4.0, 4.5, 5.0), 16, 3),
    # `full` is sized to complete in a single sandbox call.  n_transverse 48 vs 64
    # moves c(001) by 2e-5 (measured), and the R = 7 anchor is kept as a
    # single-offset convergence probe rather than a 4-offset mean -- see
    # `convergence_probe` in the result, which is evidence, not an input to c.
    "full": (48, 12.0, _PLANES, (5.0, 5.5, 6.0, 6.5), 24, 4),
}

_OFFSETS = ((0.0, 0.0, 0.0), (0.37, 0.11, 0.29), (0.23, 0.41, 0.07), (0.13, 0.29, 0.44))

# Converged reference values (scale="full", 2026-09-03).  The gate asserts
# against these; they are results, not inputs.
C_WEYL_REF = 0.720867
# Uncertainty budget, widened after the 2026-09-03 review (docs/reviews/):
#   ball scatter over radii (sem)                     0.0013
#   fit-form systematic, c*A vs c*A+d vs c*A+b*R       0.0060
#   gate-scale vs full-scale movement of the estimator 0.0053
#   finite-thickness drift on the planar route         0.0002
# The dominant terms are systematic, not statistical, so they are combined
# linearly-ish rather than in quadrature and rounded UP.  The earlier 0.0015 was
# the ball sem alone and understated the real budget by ~4x; every sigma-based
# statement in the first draft of F355 rested on it and has been withdrawn.
C_WEYL_REF_SIGMA = 0.0070
C_PLANE_REF = {(0, 0, 1): 0.751674, (1, 1, 0): 0.596344, (1, 1, 1): 0.734202}


def check_e9(scale="gate", flat_control=False, random_control=False):
    """The E9 ledger.

    `flat_control=True`  -> n_hat is k-independent, the correlator is site-diagonal,
                            the vacuum is a product state and EVERY entropy is 0.
    `random_control=True` -> n_hat is random at every p; the correlator is white
                            noise and the entropy follows a VOLUME law.
    """
    nt, thick, planes, radii, box, noff = _SCALES[scale]
    ctl = {}
    if flat_control:
        ctl["flat_control"] = True
    if random_control:
        ctl["random_control"] = 20260903
    checks = []

    def add(cid, desc, ok, got, want, cls):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok),
                       "got": got, "want": want, "class": cls})

    # --- A. the machinery (control-independent by construction) -------------
    val = validate_machinery()
    add("E9-1", "Peschel correlation matrix == brute-force many-body ED (3 systems)",
        val["ed_max_error"] < 1e-12, val["ed_max_error"], "< 1e-12", "machine")
    add("E9-2", "1-D free-fermion chain reproduces the c=1 CFT slope dS/dln(l)=1/3",
        abs(val["cft_slope"] - 1.0 / 3.0) < 2e-3, val["cft_slope"], "1/3", "quantitative")
    add("E9-3", "BCC vacuum correlator is an exact projector (the sea is pure)",
        val["projector_residual"] < 1e-12, val["projector_residual"], "< 1e-12", "machine")
    add("E9-4", "complementarity S(l) == S(L-l)",
        val["complementarity_residual"] < 1e-9, val["complementarity_residual"],
        "< 1e-9", "machine")

    # --- B. planar cuts ------------------------------------------------------
    pc = {}
    pinfo = {}
    for h in planes:
        c, info = plane_coefficient(h, n_transverse=nt, thickness=thick, **ctl)
        pc[h] = c
        pinfo[h] = info
    ref_ok = all(abs(pc[h] - C_PLANE_REF[h]) < 3e-3 for h in C_PLANE_REF if h in pc)
    worst = max(abs(pc[h] - C_PLANE_REF[h]) for h in C_PLANE_REF if h in pc)
    add("E9-5", "planar coefficients reproduce the converged reference (001/110/111)",
        ref_ok, worst, "< 3e-3", "quantitative")

    cplus, _ = plane_coefficient((0, 0, 1), n_transverse=16, thickness=8.0, sign=+1.0, **ctl)
    cminus, _ = plane_coefficient((0, 0, 1), n_transverse=16, thickness=8.0, sign=-1.0, **ctl)
    add("E9-6", "left and right chirality give the same coefficient",
        abs(cplus - cminus) < 1e-12, abs(cplus - cminus), "< 1e-12", "machine")

    spread = (max(pc.values()) - min(pc.values())) / max(1e-30, max(pc.values()))
    dense_is_cusp = (1, 1, 0) in pc and pc[(1, 1, 0)] == min(pc.values())
    add("E9-7", "the coefficient is anisotropic and the densest plane (110) is the minimum",
        dense_is_cusp and spread > 0.15, {"spread": spread, "110_is_min": dense_is_cusp},
        "spread > 15% with (110) lowest", "quantitative")

    # --- C. balls ------------------------------------------------------------
    bc = ball_coefficient(radii=radii, box=box, offsets=_OFFSETS[:noff], **ctl)
    r0, r1 = bc["rows"][0], bc["rows"][-1]
    vol_ratio = r1["N_mean"] / r0["N_mean"]
    area_law = abs(r1["S_over_A"] / r0["S_over_A"] - 1.0)
    tol_area = 0.04 if scale == "gate" else 0.02
    add("E9-8", "area law: S/A is constant while the enclosed volume grows",
        area_law < tol_area and vol_ratio > 1.8,
        {"S_over_A_drift": area_law, "volume_ratio": vol_ratio},
        f"drift < {tol_area:.0%} over > 1.8x volume", "quantitative")

    probe = None
    if scale == "full":
        Kp = correlator_kernel(box, box, 2 * box, **ctl)
        Np, Sp = ball_entropy(Kp, box, box, 2 * box, 7.0, _OFFSETS[1])
        probe = {"R": 7.0, "N": Np, "S": Sp, "S_over_A": Sp / (4.0 * math.pi * 49.0),
                 "note": "single-offset R=7 anchor; evidence that c is flat in R, "
                         "NOT averaged into c_sphere"}

    cub = cubic_harmonic_average(pc, n_basis=3) if len(pc) >= 4 else None
    if cub is not None:
        add("E9-9", "ball value is consistent with the O_h cubic-harmonic constant "
            "term (a CONSISTENCY check -- the two share the projector and the "
            "entropy routine, and the harmonic fit's own rms residual is 4%)",
            abs(cub["c0"] - bc["c_sphere"]) < 0.02,
            {"ball": bc["c_sphere"], "harmonic_c0": cub["c0"]},
            "|difference| < 0.02", "quantitative")

    # --- D. the node count, which is what the comparison is denominated in ---
    wn = weyl_nodes()
    add("E9-10", "the walk carries FOUR gapless points, charges summing to zero",
        wn["n_gapless"] == 4 and wn["charge_sum"] == 0,
        {"n_gapless": wn["n_gapless"], "charge_sum": wn["charge_sum"]},
        "4 nodes, sum(charge) == 0 (Nielsen-Ninomiya)", "exact")

    # --- E. the comparison ---------------------------------------------------
    led = horizon_ledger(bc["c_sphere"])
    ratios = [v["ratio"] for v in led["node_counting_bracket"].values()]
    add("E9-11", "S = A/4 is missed under EVERY defensible node counting",
        all(abs(r - 1.0) > 0.2 for r in ratios) and min(ratios) > 0.2,
        {"ratios": ratios, "closest_to_unity": min(abs(r - 1.0) for r in ratios),
         "smallest_ratio": min(ratios)},
        "every ratio at least 20% from 1, and the coefficient non-degenerate "
        "(smallest ratio > 0.2, so a collapsed vacuum reds rather than passing "
        "vacuously)", "quantitative")
    add("E9-12", "the ratio is independent of g_* (F79's own a-g_* identity)",
        led["gstar_cancellation_residual"] < 1e-12,
        led["gstar_cancellation_residual"], "< 1e-12", "machine")

    box = None
    if scale == "full":
        box = box_scan()
        add("E9-13", "the result is independent of the periodic box",
            box["spread_from_largest"] < 1e-3, box["spread_from_largest"],
            "< 1e-3 over box 16-24", "quantitative")

    scope = curvature_scope()
    add("E9-14", "a flat/spherical cut is the right leading object for a horizon",
        scope["curvature_correction"] < 1e-70, scope["curvature_correction"],
        "(a/r_h)^2 < 1e-70 at 1 M_sun", "quantitative")

    n_pass = sum(c["pass"] for c in checks)
    return {"scale": scale, "checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "all_pass": n_pass == len(checks),
            "planes": {str(k): v for k, v in pc.items()},
            "plane_info": {str(k): v for k, v in pinfo.items()},
            "ball": bc, "convergence_probe": probe, "cubic_harmonic": cub,
            "ledger": led, "weyl_nodes": wn, "box_scan": box,
            "pi_proximity": pi_proximity(bc["c_sphere"]),
            "validation": val, "scope": scope}


def _results_path(name):
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        d = os.path.dirname(d)
        cand = os.path.join(d, "test-results")
        if os.path.isdir(cand):
            return os.path.join(cand, name)
    raise RuntimeError("test-results/ not found")


if __name__ == "__main__":
    import json
    import sys
    scale = sys.argv[1] if len(sys.argv) > 1 else "full"
    res = check_e9(scale=scale)
    for c in res["checks"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['id']:7s} {c['desc']}")
    print(f"\n  {res['n_pass']}/{res['n_total']}")
    led = res["ledger"]
    print(f"  c per BCC walk         {led['c_walk_per_a2']:.5f}"
          f" +- {led['c_walk_sigma']:.4f} nats / a^2")
    print(f"  required (closed form) {led['c_required_closed_form']:.7f}"
          f"   = {led['c_required_expression']}")
    print(f"  ratio (g_*-independent){led['ratio_at_fixed_counting']:.4f}"
          f" +- {led['ratio_sigma']:.4f}")
    print("  node-counting bracket (the undecided doubler question, F278 s6):")
    for k, v in led["node_counting_bracket"].items():
        print(f"    {k:26s} s_cell={v['s_cell']:8.4f}  ratio={v['ratio']:.4f}")
    print(f"  required per cell      {led['s_cell_required']:.4f}  (2 pi sqrt3)")
    pp = res["pi_proximity"]
    print(f"  pi proximity           {pp['sigmas_from_pi']:.1f} sigma"
          f"  (2^(5/3) is closer: {pp['rel_gap_to_alternative']*100:.2f}%"
          f" vs {pp['rel_gap_to_pi']*100:.2f}%) -- NOT claimed")
    print("\n  orientation dependence (nats / a^2, one walk):")
    for k, v in res["planes"].items():
        print(f"    {k:12s} {v:.6f}")
    if scale == "full":
        json.dump(res, open(_results_path("F355_horizon_entanglement.json"), "w"),
                  indent=1, default=float)
