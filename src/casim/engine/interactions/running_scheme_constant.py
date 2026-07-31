"""
ca_scheme_constant.py — the shared scheme/scale constant of F144-A4 / F145-N5
/ F124 §5, determined: the rule's coupling is the V-scheme coupling (exact
tree identity), the one-loop conversion is the KNOWN constant a1, and the
residual collapses to a matching-scale choice bounded by the model's own two
UV scales — with the data landing on their geometric mean.

(2026-06-12)  Finding F151.  Builds on ca_alpha_s_running (F144) and
ca_njl_induced_coupling (F145).

The determination
-----------------
FACE 1 — scheme identification (exact):
  The F144 lock g_s^2 = 1/4 normalises the STATIC ELECTRIC ENERGY: F110's
  lambda=0 potential is exactly V(R) = (g^2/2) q^2 R, and the model's kinetic
  term is spectral-exact, so the tree-level Coulomb of the Hamiltonian theory
  is the continuum one with NO lattice renormalisation.  A coupling defined
  through the static-source energy is, by definition, the V-scheme coupling:

        alpha_rule = alpha_V (tree-exact)            [S1]

  The one-loop V -> MS-bar conversion is then the KNOWN exact constant
        Delta(1/alpha) = a1(nf)/(4 pi),  a1 = (31 C_A - 20 T_F nf)/9,
  = 0.2918 at nf=6: this is "the single number" at the order it is defined.
  It supplies 0.292 of the 0.640 the data implies (F144 A4) and converts the
  converged alpha_s(M_Z) from +8.4% to +4.4%.

FACE 2 — why the constant is small (the Wilson contrast):
  Compact-link schemes acquire the huge tadpole renormalisation (Wilson:
  Lambda_MS/Lambda_lat = 28.81, dominated by the tadpole integral
  Z0 = int_BZ 1/K_hat = 0.154933).  The rule's lock is taken on the exact
  spectral quadratic form — there is no compact-link expansion anywhere in
  the coupling's definition, so the tadpole term is structurally absent.
  Z0 is reproduced here to quantify the contrast.                       [S2]

FACE 3 — the residual = a matching scale inside a derived band:
  After a1, the remaining Delta(1/alpha) = 0.348 is exactly a choice of the
  scale q* at which alpha_V(q*) = 1/(16 pi).  The model owns TWO natural UV
  scales separated by exactly c_lat = 1/sqrt(3): the cutoff wavenumber
  (hbar c/a) and the cutoff rotation rate (x 1/sqrt3).  The band
  q* in [1/sqrt3, 1]/a maps to alpha_s(M_Z) in [0.1143, 0.1232] — which
  BRACKETS the measured 0.1180 with zero free parameters.  The geometric
  mean q* = 3^(-1/4)/a gives alpha_s(M_Z) = 0.1186 (+0.50%) and
  Lambda_MS^(3) = 356 MeV (x1.04 FLAG); the data-implied point is
  q* = 0.7327/a, 3.6% from the geometric mean.                    [S3/S4]

FACE 4 — the IR face (refinement of F145-N5):
  The self-consistent resolved gap (M(0) = 1.50 lattice units = the F77
  constituent mass) requires alpha_eff = 0.376-0.411 (stable across the
  m_D spread) — a sharp nonperturbative target, but a DIFFERENT object from
  the UV constant: with the UV face now pinned, the F144/F145/F124 "one
  shared number" refines to (a1 exact) + (q* in a sqrt3 band) at the UV end,
  and the strong-coupling crossover at the IR end.                     [S5]

numpy only (+ ca_link_hamiltonian for the exact static-energy check).
"""

from __future__ import annotations

import math

import numpy as np

from casim.engine.interactions import running_alpha_s as RA
from casim.constants import (
    c_fierz_colour_f as _c_fierz_colour_f,
    m_D_F88_lattice as _m_D_F88_lattice,
    m_V_F117_lattice as _m_V_F117_lattice,
    q_star_a_band_lo as _q_star_a_band_lo,
)
from casim.constants import M0_constituent_lattice as _M0_constituent_lattice
import ca_fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

# ----------------------------------------------------------------------
C_A, T_F = 3.0, 0.5
SQRT3 = math.sqrt(3.0)
QSTAR_LO, QSTAR_HI = _q_star_a_band_lo, 1.0          # the band, units of 1/a
QSTAR_GEO = 3.0 ** -0.25                        # geometric mean
M_TARGET_LAT = _M0_constituent_lattice   # F77 constituent mass 311 MeV, units 651.5/pi
M_D_F88, M_V_F117 = _m_D_F88_lattice, _m_V_F117_lattice


def a1(nf: int) -> float:
    """One-loop static-potential constant a1 = (31 C_A - 20 T_F nf)/9."""
    return (31.0 * C_A - 20.0 * T_F * nf) / 9.0


def a1_ledger() -> dict:
    out = {}
    for nf in (0, 3, 6):
        b0 = 11.0 - 2.0 * nf / 3.0
        out[f"nf={nf}"] = {"a1": a1(nf),
                           "Delta_inv_alpha": a1(nf) / (4 * math.pi),
                           "Lambda_V_over_MS": math.exp(a1(nf) / (2 * b0))}
    return out


# ======================================================================
#  S1 — the scheme identification (exact pieces)
# ======================================================================
def static_energy_lock(R_list=(1, 2, 3, 4), g2: float = 0.25) -> dict:
    """F110 lambda=0: V(R) = (g^2/2) q^2 R exactly (dual rep, H diagonal).
    The coupling is DEFINED by the static-source energy => V-scheme."""
    import ca_link_hamiltonian as lh

    geom = lh.PlaquetteGrid(4, 2)
    devs = []
    for R in R_list:
        eta = np.zeros(geom.n_links, dtype=np.int64)
        # unit-charge pair on a horizontal row: string of eta=1 links
        row = 1
        for x in range(R):
            eta[geom.link_id[("H", x, row)]] = 1
        E0 = lh.ground_energy_lambda0(geom, eta, g2=g2, group="U1", m_max=2)
        devs.append(abs(E0 - 0.5 * g2 * R))
    return {"max_dev": float(max(devs)),
            "statement": "V(R) = (g^2/2) q^2 R exact at lambda=0 — "
                         "the lock normalises the static electric energy"}


def spectral_coulomb_check(L: int = 96, pairs=((6, 12), (8, 16))) -> dict:
    """The model's kinetic term is spectral-exact: the lattice Green's
    function of the exact |k|^2 symbol reproduces the continuum Coulomb
    (with periodic images) — no tree-level coupling renormalisation."""
    k = 2 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    K2 = KX ** 2 + KY ** 2 + KZ ** 2
    K2[0, 0, 0] = 1.0
    inv = 1.0 / K2
    inv[0, 0, 0] = 0.0
    # phi(R) along the x-axis
    phi_k = inv
    phi = np.real(_fft.ifftn(phi_k))     # = (1/L^3) sum_k e^{ikR}/k^2

    def cont(Rv):
        # continuum Coulomb with periodic images (zero-mode removed -> use
        # differences only); direct image sum over a modest shell
        s = 0.0
        for nx in range(-3, 4):
            for ny in range(-3, 4):
                for nz in range(-3, 4):
                    d = math.sqrt((Rv + nx * L) ** 2 + (ny * L) ** 2
                                  + (nz * L) ** 2)
                    s += 1.0 / (4 * math.pi * d)
        return s

    rels = []
    for R1, R2 in pairs:
        lat = phi[R1, 0, 0] - phi[R2, 0, 0]
        con = cont(R1) - cont(R2)
        rels.append(abs(lat / con - 1.0))
    return {"max_rel_dev": float(max(rels)), "L": L,
            "statement": "exact-symbol Green's fn = continuum Coulomb "
                         "(difference test, image-corrected)"}


# ======================================================================
#  S2 — the Wilson tadpole contrast
# ======================================================================
def wilson_tadpole(n: int = 48) -> dict:
    """Z0 = int_BZ d^4k/(2pi)^4 1/K_hat(k), Wilson K_hat = 4 sum sin^2(k/2).
    Known value 0.154933.  This integral dominates the Wilson 28.81; the
    rule's lock has no compact-link expansion, so no such term."""
    k = (np.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    KX, KY, KZ, KT = np.meshgrid(k, k, k, k, indexing="ij")
    Kh = 4 * (np.sin(KX / 2) ** 2 + np.sin(KY / 2) ** 2
              + np.sin(KZ / 2) ** 2 + np.sin(KT / 2) ** 2)
    Z0 = float(np.mean(1.0 / Kh))
    return {"Z0": Z0, "known": 0.154933, "dev": abs(Z0 - 0.154933)}


# ======================================================================
#  S3/S4 — the corrected chain over the q* band
# ======================================================================
def corrected_chain(qstar_a: float, loops: int = 4,
                    with_a1: bool = True) -> dict:
    """F144 chain with (i) the exact a1 V->MS conversion at matching and
    (ii) the matching scale mu* = qstar_a / a."""
    inv0 = 16.0 * math.pi + (a1(6) / (4 * math.pi) if with_a1 else 0.0)
    mu = qstar_a * RA.MU0_GEV
    a = RA.run_alpha(1.0 / inv0, mu, RA.M_T_POLE, nf=6, loops=loops)
    a_mz = RA.run_alpha(a, RA.M_T_POLE, RA.M_Z, nf=5, loops=loops)
    a_mb = RA.run_alpha(a_mz, RA.M_Z, RA.M_B, nf=5, loops=loops)
    a_mc = RA.run_alpha(a_mb, RA.M_B, RA.M_C, nf=4, loops=loops)
    lam3 = RA.lambda_msbar_2loop(a_mc, RA.M_C, nf=3)
    return {"alpha_s_MZ": a_mz,
            "dev_vs_PDG_%": 100.0 * (a_mz / RA.ALPHA_S_MZ_PDG - 1.0),
            "Lambda3_GeV": lam3,
            "Lambda3_vs_FLAG": lam3 / RA.LAMBDA3_FLAG,
            "hierarchy_N": lam3 / RA.MU0_GEV}


def implied_qstar(loops: int = 4) -> float:
    """Bisect the q* that reproduces alpha_s(M_Z) = PDG exactly (a1 on)."""
    lo, hi = 0.3, 1.2
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        if corrected_chain(mid, loops)["alpha_s_MZ"] > RA.ALPHA_S_MZ_PDG:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


# ======================================================================
#  S5 — the IR face (self-consistent alpha_eff*)
# ======================================================================
def ir_alpha_eff(Mg: float, L: int = 32, iters: int = 250) -> float:
    """alpha_eff such that the self-consistent resolved gap (F145 kernel,
    constant coupling) gives M(0) = M_TARGET_LAT (the F77 constituent mass)."""
    k = 2 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    K = 2 * (1 - np.cos(KX)) + 2 * (1 - np.cos(KY)) + 2 * (1 - np.cos(KZ))

    def M0(alpha_eff):
        g2 = 4 * math.pi * alpha_eff
        GSk = _fft.fftn((_c_fierz_colour_f) * (g2 / 2.0) / (K + Mg ** 2))
        M = np.full((L, L, L), 0.5)
        for _ in range(iters):
            loop = M / np.sqrt(K + M ** 2)
            Mn = 24.0 * np.real(_fft.ifftn(GSk * _fft.fftn(loop))) / L ** 3
            if np.max(np.abs(Mn - M)) < 1e-10:
                M = Mn
                break
            M = 0.5 * M + 0.5 * Mn
        return float(M.reshape(-1)[0])

    lo, hi = 0.2, 1.5
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if M0(mid) < M_TARGET_LAT:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ======================================================================
#  Report
# ======================================================================
def report() -> dict:
    rep = {"a1_ledger": a1_ledger(),
           "static_energy_lock": static_energy_lock(),
           "spectral_coulomb": spectral_coulomb_check(),
           "wilson_tadpole": wilson_tadpole()}
    rep["chain_band"] = {
        "q*=1/a": corrected_chain(QSTAR_HI),
        "q*=1/sqrt3/a": corrected_chain(QSTAR_LO),
        "q*=3^-1/4/a (geometric mean)": corrected_chain(QSTAR_GEO),
        "no_a1_reference (F144)": corrected_chain(1.0, with_a1=False),
    }
    qs = implied_qstar()
    rep["implied_qstar_a"] = qs
    rep["implied_vs_geometric_%"] = 100.0 * (qs / QSTAR_GEO - 1.0)
    rep["implied_in_band"] = bool(QSTAR_LO < qs < QSTAR_HI)
    rep["at_implied"] = corrected_chain(qs)
    rep["ir_face"] = {"alpha_eff*_F88": ir_alpha_eff(M_D_F88),
                      "alpha_eff*_F117": ir_alpha_eff(M_V_F117)}
    return rep


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=float))
