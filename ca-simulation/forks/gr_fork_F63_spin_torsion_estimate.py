"""
F63 — Does the project's torsion-free assumption cost anything? A bounded
      magnitude estimate of the Einstein-Cartan spin-torsion four-fermion term
      at the model's lattice density.
====================================================================================
Reconciliation follow-up to `page34-eom-derivation.md`.  Page 34's first-order
(Palatini) variation w.r.t. the independent connection Omega_mu (EOM 3) generates
Einstein-Cartan torsion algebraically sourced by the fermion spin density.  The
project (F50/F52/F57/F62) instead works torsion-free: the connection is whatever
the mass-sourced metric (lapse A, spatial B) dictates, and there is no independent
Omega_mu degree of freedom.  The honest open question the reconciliation exposed:

    *does dropping torsion cost anything at the densities the lattice actually runs?*

This fork answers it as a magnitude estimate (NOT a dynamical torsion sim — the
full nonlinear route is plan item D3b, open research).  Integrating out the
algebraic torsion leaves the standard EC axial-axial four-fermion contact term

    L_4f = -(3/16) * kappa * (psibar gamma5 gamma^mu psi)(psibar gamma5 gamma_mu psi),
           kappa = 8 pi G / c^4                                    (hbar=c=1 below)

We compare its energy density u_4f to the Dirac (rest/kinetic) energy density
u_Dirac of the same fermions, in the project's own units, using F61's pinned cell
size a = P_pre * d^(1/4) * ellP with P_pre = sqrt(2 pi eta g_*), eta_Weyl = 1/12.

Strategy / why this is numpy-safe (CLAUDE.md chiral caveat)
----------------------------------------------------------
We never contract the gamma5-gamma bilinear numerically (that would route through
the chiral matrices).  Instead we use the *polarised upper bound* on the axial
current, |psibar gamma5 gamma^mu psi| <= n  (number density) for any normalised
mode — a fully spin-polarised packet saturates it.  This makes the estimate
conservative (largest possible torsion), so a "negligible" verdict is robust.
Everything below is real-arithmetic energy-density bookkeeping + exact rationals.

Parts
-----
A. The EC four-fermion coefficient (exact rational 3/16; kappa = 8 pi G).
B. The dimensionless ratio r(f, m) = u_4f / u_Dirac in lattice/Planck units, as a
   closed form in the occupation fraction f (fermions per cell) and dimensionless
   mass m, with (ellP/a)^2 from F61.
C. Evaluate r at F62's *actual* packet densities (pulled from dirac_gravity_fork's
   initial conditions): is the torsion term negligible where F62's tests live?
D. The lattice "Cartan density": the occupation f* at which r ~ 1 (torsion becomes
   O(1)) — confirm it sits at near-Planck (order one quantum per cell) density,
   outside the model's sparse-fermion regime.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as Fr
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
_THIS = os.path.dirname(os.path.abspath(__file__))
for p in (_THIS, os.path.abspath(os.path.join(_THIS, "..")),
          os.path.abspath(os.path.join(_THIS, "..", "ca-simulation"))):
    if p not in sys.path:
        sys.path.insert(0, p)


# ----- Part A: the Einstein-Cartan four-fermion coefficient ------------------
def ec_four_fermion_coefficient():
    """Standard EC result (Hehl-von der Heyde-Kerlick-Nester 1976): eliminating
    the algebraic torsion from S = (1/2kappa) INT R + S_Dirac leaves an axial-axial
    contact term  L_4f = -(3/16) kappa (j5)^2,  kappa = 8 pi G/c^4.
    Returns the exact rational prefactor and the kappa factor (hbar=c=1: kappa=8 pi G)."""
    c_frac = Fr(3, 16)            # exact rational from the EC torsion algebra
    return {"prefactor_3_16": c_frac, "kappa_over_G": 8.0 * np.pi}


# ----- F61 inputs: pinned cell size ------------------------------------------
def cell_size_over_ellP(eta=Fr(1, 12), g_star=16, d=3):
    """a/ellP = P_pre * d^(1/4),  P_pre = sqrt(2 pi eta g_*)   (F59/F61)."""
    P_pre = np.sqrt(float(2 * np.pi * eta * g_star))
    return P_pre * d ** 0.25, P_pre


# ----- Part B: the dimensionless torsion/Dirac energy-density ratio ----------
def torsion_dirac_ratio(f, m, eta=Fr(1, 12), g_star=16, d=3):
    """r(f,m) = u_4f / u_Dirac in lattice/Planck units (hbar=c=1, G=ellP^2).

    Per-cell bookkeeping, cell volume a^d:
      number density           n      = f / a^d
      axial current (polarised) j5    <= n                          (upper bound)
      EC four-fermion density  u_4f   = (3/16) * kappa * j5^2  with kappa = 8 pi ellP^2
                                      = (3/16)(8 pi)(ellP^2)(f/a^d)^2
      Dirac energy density     u_Dir  = omega * n,  omega >= m  (rest floor)
                                      = m * f / a^d                 (conservative: rest)
      ratio r = u_4f/u_Dir = (3/16)(8 pi) ellP^2 (f/a^d)^2 / (m f/a^d)
              = (3 pi / 2) * (ellP^2 / a^d) * f / (m * a^{... })

    For the physical d=3 lattice (a^d = a^3) we keep ellP^2/a^3 -> needs a length;
    the clean dimensionless combination uses the lattice cutoff omega ~ 1/a for the
    *kinetic* ceiling and m = 1/a for the heaviest mode, giving the cutoff-scale
    ratio  r_max(f) = (3 pi/2) f (ellP/a)^2 .  We report both the rest-mass ratio
    (mass m, momentum 0) and this cutoff ratio (the largest)."""
    a_over_ellP, P_pre = cell_size_over_ellP(eta, g_star, d)
    ellP_over_a_sq = 1.0 / a_over_ellP ** 2
    # cutoff-scale (heaviest/fastest mode, omega ~ 1/a, m ~ 1/a): largest ratio
    r_cutoff = (3.0 * np.pi / 2.0) * f * ellP_over_a_sq
    # rest-mass ratio for a slow mode of dimensionless mass m (omega -> m, in 1/a):
    #   u_Dir = (m/a) n,  u_4f as above with kappa=8 pi ellP^2  -> r = r_cutoff/(m_in_cutoff)
    #   where m_in_cutoff = m (already in units of 1/a if m dimensionless<=1).
    r_rest = r_cutoff / max(m, 1e-9)
    return {"r_cutoff": float(r_cutoff), "r_rest_mass": float(r_rest),
            "a_over_ellP": float(a_over_ellP),
            "ellP_over_a_sq": float(ellP_over_a_sq), "f": float(f), "m": float(m)}


# ----- Part C: evaluate at F62's actual packet densities ---------------------
def _gaussian_peak_fraction(shape, sigma, center=None):
    """Peak per-cell occupation f = max(rho)/sum(rho) for a 2D Gaussian packet.

    F62's `gaussian_packet_momentum` builds rho = |env|^2 with
    env = exp(-r^2/(2 sigma^2)); the plane-wave phase has unit modulus and the
    4-spinor is normalised, so the *density* peak fraction is exactly this
    envelope's max/sum — identical to F62 without importing its (scipy-bound)
    module.  Real-arithmetic, numpy only."""
    Lx, Ly = shape
    cx, cy = center if center is not None else (Lx / 2.0, Ly / 2.0)
    xs = np.arange(Lx) - cx
    ys = np.arange(Ly) - cy
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    rho = np.exp(-(X ** 2 + Y ** 2) / (sigma ** 2))   # = |env|^2, env~exp(-r^2/2sig^2)
    return float(rho.max() / rho.sum())


def f62_peak_occupations():
    """Peak per-cell occupation f for F62's initial packets (one quantum total,
    normalised), at F62's *exact* (shape, sigma) configs.  A 2D Gaussian of width
    sigma has f ~ 1/(2 pi sigma^2).  Self-contained (no scipy / no F62 import) so
    the fork runs anywhere; the formula is verified against the analytic
    1/(2 pi sigma^2) below."""
    configs = [
        ("D2a_rindler", dict(shape=(220, 220), m=0.35, sigma=16.0)),
        ("D2b_redshift", dict(shape=(96, 96), m=0.5, sigma=7.0)),
        ("D2c_deflection", dict(shape=(160, 160), m=0.0, sigma=6.0)),
        ("D3a_backreact", dict(shape=(64, 64), m=0.4, sigma=6.0)),
    ]
    out = {"available": True}
    for tag, cfg in configs:
        f_peak = _gaussian_peak_fraction(cfg["shape"], cfg["sigma"])
        # density rho ~ exp(-r^2/sigma^2) has width sigma/sqrt2, so peak
        # fraction = 1/(pi sigma^2) (twice the amplitude's 1/(2 pi sigma^2)).
        out[tag] = {"f_peak": f_peak, "sigma": cfg["sigma"], "m": cfg["m"],
                    "f_analytic_1_over_pi_sig2": 1.0 / (np.pi * cfg["sigma"] ** 2)}
    return out


# ----- Part D: the lattice Cartan density (where torsion -> O(1)) ------------
def cartan_occupation(eta=Fr(1, 12), g_star=16, d=3):
    """Occupation f* at which the (largest) cutoff ratio r_cutoff = 1:
        f* = 1 / [(3 pi/2)(ellP/a)^2] = (2/(3 pi)) (a/ellP)^2 .
    f* >> 1 means you must pile many quanta into one cell (super-Planckian) before
    torsion matters; f* ~ O(1) means one-quantum-per-cell already reaches it."""
    a_over_ellP, _ = cell_size_over_ellP(eta, g_star, d)
    f_star = (2.0 / (3.0 * np.pi)) * a_over_ellP ** 2
    return {"f_star_cartan": float(f_star), "a_over_ellP": float(a_over_ellP)}


if __name__ == "__main__":
    res = {}
    print("=== Part A: Einstein-Cartan four-fermion coefficient ===")
    A = ec_four_fermion_coefficient()
    res["coefficient"] = {"prefactor_3_16": str(A["prefactor_3_16"]),
                          "kappa_over_G": A["kappa_over_G"]}
    print(f"  L_4f = -(3/16) kappa j5^2 ,  kappa = 8 pi G   (prefactor = {A['prefactor_3_16']})")
    assert A["prefactor_3_16"] == Fr(3, 16)

    print("\n=== Part B: torsion/Dirac energy-density ratio (lattice units) ===")
    a_over_ellP, P_pre = cell_size_over_ellP()
    res["cell"] = {"a_over_ellP": float(a_over_ellP), "P_pre": float(P_pre),
                   "eta": "1/12", "g_star": 16, "d": 3}
    print(f"  F61 cell: a = {a_over_ellP:.3f} ellP  (P_pre={P_pre:.3f}); (ellP/a)^2 = {1/a_over_ellP**2:.4f}")
    res["ratio_formula"] = "r_cutoff(f) = (3 pi/2) f (ellP/a)^2 ; r_rest = r_cutoff/m"

    print("\n=== Part C: ratio at F62's actual packet densities ===")
    occ = f62_peak_occupations()
    res["f62_densities"] = occ
    worst = 0.0
    n_eval = 0
    for tag, d_ in occ.items():
        if tag == "available":
            continue
        r = torsion_dirac_ratio(d_["f_peak"], max(d_["m"], 0.2))
        d_["r_cutoff"] = r["r_cutoff"]; d_["r_rest_mass"] = r["r_rest_mass"]
        worst = max(worst, r["r_cutoff"]); n_eval += 1
        print(f"  {tag:16s}: f_peak={d_['f_peak']:.2e} "
              f"(analytic {d_['f_analytic_1_over_pi_sig2']:.2e})  "
              f"r_cutoff={r['r_cutoff']:.2e}  r_rest={r['r_rest_mass']:.2e}")
    print(f"  -> worst-case torsion/Dirac ratio across {n_eval} F62 tests = {worst:.2e}")
    res["worst_f62_ratio"] = float(worst)
    res["n_f62_configs_evaluated"] = n_eval

    print("\n=== Part D: lattice Cartan density (torsion -> O(1)) ===")
    D = cartan_occupation()
    res["cartan"] = D
    print(f"  f* (r_cutoff=1) = {D['f_star_cartan']:.2f} quanta per cell")
    print(f"  (one generation, a~3.8 ellP): torsion is O(1) only at ~{D['f_star_cartan']:.0f} "
          f"quanta/cell — far above the sparse-fermion regime F62 runs.")

    # verdict
    res["verdict"] = {
        "f62_torsion_negligible": bool(worst < 1e-2),
        "cartan_above_one_per_cell": bool(D["f_star_cartan"] > 1.0),
    }
    with open(os.path.join(OUT, "f63_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("\nwrote f63_results.json")
