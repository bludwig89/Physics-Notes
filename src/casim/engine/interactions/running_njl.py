"""
ca_njl_induced_coupling.py — Route C of the QCD calibration block:
the NJL contact coupling ghat = G*Lambda^2 as an INDUCED coupling — the exact
Fierz coefficient, the momentum-resolved kernel on the lattice BZ, and the
composition with Route A's running coupling.

(2026-06-12)  See docs/theory/qcd-calibration-derivation-routes.md (Route C),
F116 NJ4 (the mechanism + order-of-magnitude this sharpens), F117 (the
gap-massive dielectric gluon propagator used as the exchange kernel),
F88 (the measured dual-Meissner mass m_D), F144 (Route A running).

What is computed
----------------
C1 (exact): the COMPLETE Fierz coefficient of one-gluon exchange into the
    NJL channel.  Full 24-dim (Dirac4 x colour3 x flavour2) operator algebra:

        sum_{mu,a} (gam^mu T^a)(gam_mu T^a)  --Fierz-->
            (2/9) [ (qbar q)^2 + (qbar i g5 tau q)^2
                  + (qbar tau q)^2 + (qbar i g5 q)^2 ] + other channels

    i.e. c = 2/9 in ALL FOUR chiral channels (the induced interaction is
    exactly U(2)_L x U(2)_R symmetric — the F77 form is forced, not chosen).
    Decomposition: 2/9 = (4/9 colour) x (1 Dirac V->S) x (1/2 flavour).
    This CORRECTS F116 NJ4's 4/9 (colour factor only): with the second-order
    effective Lagrangian L = -(g^2/2) j.D.j the induced NJL coupling is
        G = (2/9)(g^2 / 2 M_g^2) = g^2 / (9 M_g^2)    [contact limit],
    a factor 4 below NJ4.

C2 (anchor): in the contact limit the induced gap equation reduces exactly
    to the F116 NJ2 lattice-BZ gap equation, with criticality
    R = G/G_c = g_contact * <1/sqrt(K)>_BZ.  Verified analytic == power
    iteration to 1e-12.

C3 (decisive negative): with the BARE locked coupling g_s^2 = 1/4 (F144) the
    momentum-resolved kernel D(q) = 1/(K(q)+M_g^2) gives R ~ 0.10 << 1 at the
    measured m_D — the bare rule coupling CANNOT break chiral symmetry.  The
    near-criticality in NJ4 was an artifact of (contact approx) x (4/9).
    The F117 dielectric enhancement (eps_c < 1) raises R but cannot rescue
    the bare coupling (R < 0.25 even at eps_c = 1/4).

C4 (structural positive): with Route A's RUNNING coupling at the exchange
    virtuality, g^2(mu(q)), mu(q) = sqrt(K+M_g^2) * (Lambda_NJL/pi), IR-frozen
    (mu_eff = sqrt(mu^2 + mu_fr^2) — the gap-massive propagator justifies a
    freeze at/below the dual-Meissner scale), R = 2.6 .. 15 >> 1: chiral
    symmetry breaking is GUARANTEED by the RG growth Route A derived.  The
    criticality condition is the derived inequality
        alpha_eff >= alpha_crit(M_g) = 1/(4 pi R0(M_g)),
    with R0 the pure kernel-geometry eigenvalue (g^2 == 1).

C5 (the residual, quantified): the F77 fit G/G_c = 1.277 corresponds to
    alpha_eff = R_fit/(4 pi R0) ~ 0.26 — inside the model's running band at
    the chiral scale.  The exact ghat awaits the nonperturbative IR coupling
    — the SAME single scale-setting residual as F124 §5 / F144 A4.

numpy only; power iteration on L^3 grids (default 32).
"""

from __future__ import annotations

import math

import numpy as np
from casim.constants import m_D_F88_lattice, m_V_F117_lattice, Lambda_NJL_GeV
from casim.constants import (
    G_Lambda2_NJL as _G_Lambda2_NJL,
    c_fierz_colour_f as _c_fierz_colour_f,
)
from casim.numerics import fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

# ----------------------------------------------------------------------
#  Constants / model inputs (all measured or derived upstream)
# ----------------------------------------------------------------------
G_S2_BARE   = 0.25          # g_s^2 = 1/4, DERIVED (F144 A1)
M_D_F88     = m_D_F88_lattice   # dual-Meissner mass, lattice units (F88 CC8, 8^3)
M_V_F117    = m_V_F117_lattice  # same chain, F117 representative run (L=6)
LAMBDA_NJL  = Lambda_NJL_GeV    # GeV; BZ edge pi <-> 651.5 MeV (F116 NJ1)
LAMBDA3_1L  = 0.272         # GeV; F144 1-loop chain Lambda_MS^(3)
LAMBDA3_FLAG = 0.343        # GeV; FLAG target (sensitivity row)
GGC_F77     = 1.277         # the fitted G/G_c (F77 / F116 NJ1) — the target
GHAT_F77    = _G_Lambda2_NJL          # the fitted ghat = G Lambda^2 — the target
GC_LAM2     = math.pi ** 2 / 6.0   # continuum G_c Lambda^2 (F77), = 1.645


# ======================================================================
#  C1 — exact Fierz in the 24-dim one-quark space
# ======================================================================
def _basis():
    I4, I3, I2 = np.eye(4), np.eye(3), np.eye(2)
    g0 = np.diag([1, 1, -1, -1]).astype(complex)
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.array([[1, 0], [0, -1]], complex)

    def gi(s):
        return np.block([[np.zeros((2, 2)), s],
                         [-s, np.zeros((2, 2))]]).astype(complex)

    gam = [g0, gi(sx), gi(sy), gi(sz)]
    g5 = 1j * gam[0] @ gam[1] @ gam[2] @ gam[3]
    lam = []

    def gm(m, scale=1.0):
        lam.append(np.array(m, complex) / 2 * scale)

    gm([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    gm([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]])
    gm([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
    gm([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
    gm([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]])
    gm([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    gm([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]])
    gm([[1, 0, 0], [0, 1, 0], [0, 0, -2]], 1.0 / math.sqrt(3))
    taus = [sx, sy, sz]
    return I4, I3, I2, gam, g5, lam, taus


def kron3(A, B, C):
    return np.kron(np.kron(A, B), C)


def fierz_coefficients() -> dict:
    """Exchanged-channel projection coefficients of sum_{mu,a} V^A (x) V_A."""
    I4, I3, I2, gam, g5, lam, taus = _basis()
    eta = [1, -1, -1, -1]
    O = np.zeros((24, 24, 24, 24), complex)
    for mu in range(4):
        for a in range(8):
            V = kron3(gam[mu], lam[a], I2)
            O += eta[mu] * np.einsum("ij,kl->ijkl", V, V)
    Otil = np.transpose(O, (0, 3, 2, 1))     # exchanged pairing (14)(32)

    def coeff(G1, G2):
        n1 = np.trace(G1 @ G1.conj().T).real
        n2 = np.trace(G2 @ G2.conj().T).real
        return complex(np.einsum("abcd,ba,dc->", Otil,
                                 G1.conj().T, G2.conj().T) / (n1 * n2))

    S = kron3(I4, I3, I2)
    P0 = kron3(1j * g5, I3, I2)
    out = {
        "c_scalar_isoscalar": coeff(S, S).real,
        "c_pseudo_isoscalar": coeff(P0, P0).real,
        "c_scalar_isovector": np.mean([coeff(kron3(I4, I3, t),
                                             kron3(I4, I3, t)).real
                                       for t in taus]),
        "c_pseudo_isovector": np.mean([coeff(kron3(1j * g5, I3, t),
                                             kron3(1j * g5, I3, t)).real
                                       for t in taus]),
    }
    out["target_2_over_9"] = _c_fierz_colour_f
    out["max_dev_from_2/9"] = float(max(abs(v - _c_fierz_colour_f)
                                        for k, v in out.items()
                                        if k.startswith("c_")))
    # chiral symmetry of the induced interaction: all four equal
    vals = [out[k] for k in out if k.startswith("c_")]
    out["chiral_symmetric_spread"] = float(max(vals) - min(vals))
    return out


def fock_kernel_identity() -> dict:
    """sum_{mu,a} gam^mu T^a . 1 . gam_mu T^a = 4 C_F * 1  (scalar channel)."""
    I4, I3, I2, gam, g5, lam, taus = _basis()
    eta = [1, -1, -1, -1]
    Ksum = np.zeros((24, 24), complex)
    for mu in range(4):
        for a in range(8):
            V = kron3(gam[mu], lam[a], I2)
            Ksum += eta[mu] * V @ V
    c = np.trace(Ksum).real / 24.0
    return {"coefficient": c, "four_CF": 16.0 / 3.0,
            "dev": abs(c - 16.0 / 3.0),
            "offdiag": float(np.max(np.abs(Ksum - c * np.eye(24))))}


# ======================================================================
#  The lattice-BZ induced gap kernel and its criticality eigenvalue
# ======================================================================
def _K(L: int) -> np.ndarray:
    k = 2 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    return 2 * (1 - np.cos(KX)) + 2 * (1 - np.cos(KY)) + 2 * (1 - np.cos(KZ))


def g2_running(mu_GeV, Lam3: float = LAMBDA3_1L, mu_fr: float = 0.50):
    """1-loop n_f=3 running g^2(mu), IR-frozen: mu_eff = sqrt(mu^2+mu_fr^2)."""
    mu_eff = np.sqrt(np.asarray(mu_GeV) ** 2 + mu_fr ** 2)
    inv_alpha = (9.0 / (2 * math.pi)) * np.log(mu_eff / Lam3)
    return 4 * math.pi / np.maximum(inv_alpha, 1e-6)


def criticality_R(Mg: float, L: int = 32, mode: str = "resolved",
                  g_s2: float = G_S2_BARE, eps_c: float = 1.0,
                  mu_fr: float = 0.50, Lam3: float = LAMBDA3_1L,
                  Mreg: float = 1e-3, iters: int = 400) -> float:
    """
    Largest eigenvalue R of the linearised induced gap equation
        M(k) = 24 <G_S(k-q) M(q)/sqrt(K(q))>_q       (chiral limit, M->0).
    R = G/G_c: R > 1 <=> chiral symmetry breaks.

    mode = 'contact'  : G_S = (2/9)(g^2/2)/Mg^2            (NJ4 corrected)
           'resolved' : G_S(q) = (2/9)(g^2/2)/(eps_c K + Mg^2)
           'running'  : as resolved with g^2 -> g^2(mu(q)) from Route A,
                        mu(q) = sqrt(K+Mg^2) * (Lambda_NJL/pi) GeV.
    """
    K = _K(L)
    if mode == "contact":
        GS = np.full_like(K, (_c_fierz_colour_f) * (g_s2 / 2.0) / Mg ** 2)
    elif mode == "resolved":
        GS = (_c_fierz_colour_f) * (g_s2 / 2.0) / (eps_c * K + Mg ** 2)
    elif mode == "running":
        mu_q = np.sqrt(K + Mg ** 2) * (LAMBDA_NJL / math.pi)
        GS = (_c_fierz_colour_f) * (g2_running(mu_q, Lam3, mu_fr) / 2.0) \
            / (eps_c * K + Mg ** 2)
    else:
        raise ValueError(mode)
    w = 1.0 / np.sqrt(K + Mreg ** 2)
    GSk = _fft.fftn(GS)
    v = np.random.default_rng(0).random((L, L, L))
    v /= np.linalg.norm(v)
    lam = 0.0
    for _ in range(iters):
        u = 24.0 * np.real(_fft.ifftn(GSk * _fft.fftn(w * v))) / L ** 3
        ln = np.linalg.norm(u)
        u /= ln
        if abs(ln - lam) < 1e-12:
            return float(ln)
        v, lam = u, ln
    return float(lam)


def contact_anchor(Mg: float, L: int = 32) -> dict:
    """Analytic contact R = g_contact*<1/sqrt(K)> vs power iteration."""
    K = _K(L)
    g_contact = 24.0 * (_c_fierz_colour_f) * (G_S2_BARE / 2.0) / Mg ** 2
    I1 = float(np.mean(1.0 / np.sqrt(K + 1e-3 ** 2)))
    R_analytic = g_contact * I1
    R_power = criticality_R(Mg, L, mode="contact")
    return {"R_analytic": R_analytic, "R_power": R_power,
            "dev": abs(R_analytic - R_power), "g_c_lattice": 1.0 / I1}


def kernel_geometry_R0(Mg: float, L: int = 32) -> float:
    """R at g^2 == 1 (resolved): R(g^2) = g^2 * R0; alpha_crit = 1/(4 pi R0)."""
    return criticality_R(Mg, L, mode="resolved", g_s2=1.0)


# ======================================================================
#  The Route-C report
# ======================================================================
def route_c_report(L: int = 32) -> dict:
    rep = {"fierz": fierz_coefficients(),
           "fock_identity": fock_kernel_identity()}
    rep["anchor_F88"] = contact_anchor(M_D_F88, L)
    rep["anchor_F117"] = contact_anchor(M_V_F117, L)
    for tag, Mg in (("F88_mD=0.532", M_D_F88), ("F117_mV=0.727", M_V_F117)):
        R0 = kernel_geometry_R0(Mg, L)
        block = {
            "R_contact_bare": criticality_R(Mg, L, "contact"),
            "R_resolved_bare": criticality_R(Mg, L, "resolved"),
            "R_resolved_bare_epsc=0.52": criticality_R(Mg, L, "resolved",
                                                       eps_c=0.52),
            "R_resolved_bare_epsc=0.25": criticality_R(Mg, L, "resolved",
                                                       eps_c=0.25),
            "R0_geometry": R0,
            "alpha_crit": 1.0 / (4 * math.pi * R0),
            "alpha_eff_for_F77_fit": GGC_F77 / (4 * math.pi * R0),
            "running": {},
        }
        for mu_fr in (0.40, 0.50, 0.65):
            for Lam3 in (LAMBDA3_1L, LAMBDA3_FLAG):
                key = f"mu_fr={mu_fr}_Lam3={Lam3}"
                block["running"][key] = criticality_R(
                    Mg, L, "running", mu_fr=mu_fr, Lam3=Lam3)
        rvals = list(block["running"].values())
        block["running_R_range"] = [min(rvals), max(rvals)]
        block["ghat_contact_bare"] = block["R_contact_bare"] * GC_LAM2
        block["ghat_resolved_bare"] = block["R_resolved_bare"] * GC_LAM2
        block["ghat_running_range"] = [min(rvals) * GC_LAM2,
                                       max(rvals) * GC_LAM2]
        rep[tag] = block
    rep["targets"] = {"G_over_Gc_F77": GGC_F77, "ghat_F77": GHAT_F77}
    return rep


if __name__ == "__main__":
    import json
    print(json.dumps(route_c_report(), indent=2, default=float))
