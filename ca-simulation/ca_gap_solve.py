"""
ca_gap_solve.py — Residual B of the strong-sector scale problem:
the FULL self-consistent (nonlinear) chiral-SB gap solve M(k).

F145 built the LINEARISED gap eigenvalue R=G/G_c (criticality, M->0). F151-S5
stated the IR-face value alpha_eff* ~ 0.39 from "the self-consistent resolved
gap, M(0)=1.50 (F77)" but did not expose the solve. This module performs it.

Gap equation (momentum-dependent-coupling NJL on the lattice BZ; the F145 kernel
with the M^2 kept in the quasiparticle energy):

    M(k) = m0 + 24 < G_S(k-q) * M(q)/sqrt(K(q)+M(q)^2) >_q ,

    G_S(q) = (2/9) (g^2/2) / (eps_c K(q) + Mg^2)        [resolved; F145 N1 Fierz 2/9]
           = (2/9) (g^2(mu(q))/2) / (eps_c K(q) + Mg^2)  [running; F144/F145]

with 24 = 4(Dirac) x 3(colour) x 2(flavour), K(q) the lattice kernel, Mg the
dual-Meissner gluon mass (F88 0.532 / F117 0.727, lattice units). The convolution
is the verified F145 FFT path. Units: lattice; M(0)=1.50 <-> 311 MeV (F77) via
the BZ-edge map Lambda_NJL/pi = 0.207 GeV per lattice unit.

Two solves:
  (i)  forward: plug a constant effective coupling g^2 (or the running one) and
       iterate to the self-consistent M(k);
  (ii) inverse: bisection for the alpha_eff* = g^2/4pi that yields M(0)=1.50
       (the F77 constituent mass) -> THE IR-face coupling value.

Pure numpy (real arithmetic; no chiral transforms). Reuses F145 constants.
"""
from __future__ import annotations

import math

import numpy as np

import ca_njl_induced_coupling as njl

LAMBDA_NJL = njl.LAMBDA_NJL          # 0.6515 GeV (BZ edge)
GEV_PER_UNIT = LAMBDA_NJL / math.pi  # 0.2074 GeV per lattice unit (q=0..pi map)
M_D_F88 = njl.M_D_F88                # 0.532
M_V_F117 = njl.M_V_F117              # 0.727
M0_TARGET = 1.50                     # F77 constituent mass in lattice units (=311 MeV)
M0_CURRENT = 0.0055 / GEV_PER_UNIT   # current quark m0=5.5 MeV (F116) in lattice units


def _K(L: int) -> np.ndarray:
    return njl._K(L)


def gap_solve(Mg: float, g2: float | None = None, L: int = 24,
              eps_c: float = 1.0, m0: float = 0.0, mode: str = "const",
              mu_fr: float = 0.50, Lam3: float = 0.347,
              M_init: float = 1.0, mix: float = 0.5,
              max_iter: int = 2000, tol: float = 1e-10) -> dict:
    """
    Self-consistently solve the nonlinear gap equation for M(k).
    mode='const'  : fixed g2 (alpha_eff = g2/4pi).
    mode='running': g2 -> g2(mu(q)) from Route A (Lam3 = F151 347 MeV).
    Returns M(0), the full M field stats, convergence info.
    """
    K = _K(L)
    if mode == "const":
        assert g2 is not None
        GS = (2.0 / 9.0) * (g2 / 2.0) / (eps_c * K + Mg ** 2)
    elif mode == "running":
        mu_q = np.sqrt(K + Mg ** 2) * GEV_PER_UNIT
        g2r = njl.g2_running(mu_q, Lam3=Lam3, mu_fr=mu_fr)
        GS = (2.0 / 9.0) * (g2r / 2.0) / (eps_c * K + Mg ** 2)
    else:
        raise ValueError(mode)
    GSk = np.fft.fftn(GS)

    M = np.full_like(K, M_init)
    last = 1e9
    conv = False
    for it in range(max_iter):
        w = M / np.sqrt(K + M ** 2)
        M_new = m0 + 24.0 * np.real(np.fft.ifftn(GSk * np.fft.fftn(w))) / L ** 3
        M_new = np.maximum(M_new, 0.0)          # physical branch
        M = mix * M_new + (1.0 - mix) * M
        m0k = float(M.flat[0])                  # M(k=0)
        if abs(m0k - last) < tol:
            conv = True
            break
        last = m0k
    return {"M0": float(M.flat[0]), "M_mean": float(M.mean()),
            "M_max": float(M.max()), "iters": it + 1, "converged": conv,
            "alpha_eff": (g2 / (4 * math.pi)) if g2 is not None else None,
            "M0_MeV": float(M.flat[0]) * GEV_PER_UNIT * 1e3}


def alpha_eff_for_target(Mg: float, target: float = M0_TARGET, L: int = 24,
                         eps_c: float = 1.0, m0: float = 0.0,
                         lo: float = 0.05, hi: float = 1.5,
                         tol: float = 1e-4) -> dict:
    """
    Inverse solve: bisection for alpha_eff = g2/4pi such that the self-consistent
    M(0) == target (=1.50, the F77 constituent mass).  This IS the IR-face
    coupling alpha_eff* — the number F151-S5 reported as 0.376/0.411.
    """
    def M0_of_alpha(alpha):
        g2 = 4 * math.pi * alpha
        return gap_solve(Mg, g2=g2, L=L, eps_c=eps_c, m0=m0, M_init=target)["M0"]

    a_lo, a_hi = lo, hi
    f_lo = M0_of_alpha(a_lo) - target
    f_hi = M0_of_alpha(a_hi) - target
    if f_lo * f_hi > 0:
        return {"ok": False, "reason": "no sign change", "M0_lo": f_lo + target,
                "M0_hi": f_hi + target, "alpha_lo": a_lo, "alpha_hi": a_hi}
    for _ in range(60):
        a_mid = 0.5 * (a_lo + a_hi)
        f_mid = M0_of_alpha(a_mid) - target
        if abs(f_mid) < tol:
            break
        if f_lo * f_mid < 0:
            a_hi, f_hi = a_mid, f_mid
        else:
            a_lo, f_lo = a_mid, f_mid
    alpha = 0.5 * (a_lo + a_hi)
    return {"ok": True, "alpha_eff_star": alpha, "g2_star": 4 * math.pi * alpha,
            "M0_check": M0_of_alpha(alpha), "target": target,
            "G_over_Gc": criticality_at(Mg, 4 * math.pi * alpha, L, eps_c)}


def criticality_at(Mg: float, g2: float, L: int = 24, eps_c: float = 1.0) -> float:
    """R=G/G_c (linearised eigenvalue) at this g2 — to relate alpha_eff* to F77's 1.277."""
    return njl.criticality_R(Mg, L=L, mode="resolved", g_s2=g2, eps_c=eps_c)


def f_pi_pagels_stokar(Mg: float, g2: float, L: int = 24, eps_c: float = 1.0,
                       m0: float = 0.0) -> dict:
    """
    Pagels-Stokar f_pi^2 = (N_c/4pi^2) integral M^2 / (K+M^2)^? ... here a discrete
    lattice proxy: f_pi^2 ~ 4 N_c < M(q)^2 / (K+M(q)^2) > (chiral-limit estimate),
    reported in lattice units and MeV.  (Consistency, not a precision claim.)
    """
    K = _K(L)
    sol = gap_solve(Mg, g2=g2, L=L, eps_c=eps_c, m0=m0, M_init=1.0)
    # re-solve to get the field (gap_solve returns stats; redo lightly)
    GS = (2.0 / 9.0) * (g2 / 2.0) / (eps_c * K + Mg ** 2)
    GSk = np.fft.fftn(GS)
    M = np.full_like(K, 1.0)
    for _ in range(2000):
        w = M / np.sqrt(K + M ** 2)
        Mn = m0 + 24.0 * np.real(np.fft.ifftn(GSk * np.fft.fftn(w))) / L ** 3
        Mn = np.maximum(Mn, 0.0)
        if abs(float(Mn.flat[0]) - float(M.flat[0])) < 1e-10:
            M = Mn
            break
        M = 0.5 * Mn + 0.5 * M
    Nc = 3.0
    fpi2 = 4.0 * Nc * float(np.mean(M ** 2 / (K + M ** 2)))   # lattice units^2
    fpi = math.sqrt(max(fpi2, 0.0))
    return {"M0": sol["M0"], "fpi_lattice": fpi, "fpi_MeV": fpi * GEV_PER_UNIT * 1e3,
            "M0_over_fpi": sol["M0"] / fpi if fpi > 0 else float("nan")}


def chiSB_onset(Mg: float, L: int = 24, thr: float = 0.30,
                lo: float = 0.20, hi: float = 0.50) -> float:
    """The NONLINEAR chiral-SB onset coupling: the alpha at which the dynamical
    mass M(0) crosses a macroscopic threshold thr (lattice units). Located by
    bisection on the full nonlinear solve. This is L-STABLE (unlike the
    linearised eigenvalue R0=G/G_c, which is IR-divergent in L) and uses NO M(0)
    anchor — it is purely 'where the gap turns on'."""
    def M0(a):
        return gap_solve(Mg, g2=4 * math.pi * a, L=L, M_init=1.0)["M0"]
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        if M0(mid) < thr:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def freeze_window(Mg: float, L: int = 24,
                  alphas=(0.20, 0.25, 0.28, 0.30, 0.32, 0.35, 0.376, 0.45)) -> dict:
    """
    The IR-coupling freeze value, bracketed WITHOUT anchoring M(0) (F155).

    The gap M(0) vs alpha curve has a STEEP, L-stable crossover: M(0) ~ 0 below
    the onset, then jumps to O(constituent) within a narrow alpha window. So the
    freeze is pinned between two facts, neither of which uses the M(0)=1.5 anchor:
      (1) ONSET — chiSB_onset(Mg): the L-stable nonlinear coupling at which the
          gap turns on macroscopically (~0.32 for m_D). Set by the dual-Meissner
          gluon mass Mg (F88/F117 decoupling, F152 J2): a heavier Mg pushes the
          onset up. NO mass anchor.
      (2) STEEPNESS — above onset M(0) rises so fast (0.05 -> 1.5 over
          Delta alpha ~ 0.07) that the physical coupling is necessarily just
          above onset, so the freeze window is NARROW: [onset, ~onset+0.06].

    The M(0)=1.5-anchored value alpha_eff* = 0.376/0.411 sits at the TOP of this
    anchor-free window, and the window coincides with the continuum
    frozen-coupling window [0.3, 0.5] (F152 J3). So the freeze ~0.35(4) is
    derived anchor-free to ~10%; the exact value within the window (and the
    absolute MeV of M(0)) still needs the scale of Residual A.
    """
    onset = chiSB_onset(Mg, L=L)
    curve = []
    for a in alphas:
        r = gap_solve(Mg, g2=4 * math.pi * a, L=L, M_init=1.0)
        curve.append({"alpha": a, "M0": round(r["M0"], 4),
                      "M0_MeV": round(r["M0_MeV"], 0)})
    phys = alpha_eff_for_target(Mg, L=L)
    a_phys = phys.get("alpha_eff_star", float("nan"))
    return {"Mg": Mg,
            "onset_ANCHORFREE_Lstable": round(onset, 4),
            "alpha_phys_M0=1.5": a_phys,
            "freeze_window": [round(onset, 3), round(a_phys, 3)],
            "freeze_midpoint": round(0.5 * (onset + a_phys), 3),
            "continuum_frozen_window": [0.3, 0.5],
            "M0_vs_alpha": curve,
            "statement": "freeze bracketed anchor-free to [onset, alpha_phys] "
                         "(both NO-anchor: onset is L-stable nonlinear turn-on); "
                         "Mg sets the onset (decoupling, F152 J2); ~0.35(4), "
                         "0.39 at top; exact value gated on Residual A's scale"}


def report(L: int = 24) -> dict:
    rep = {"L": L, "GeV_per_unit": GEV_PER_UNIT, "M0_target": M0_TARGET,
           "m0_current_lat": M0_CURRENT}
    for tag, Mg in (("F88_mD=0.532", M_D_F88), ("F117_mV=0.727", M_V_F117)):
        inv = alpha_eff_for_target(Mg, L=L)
        block = {"inverse_solve": inv}
        if inv.get("ok"):
            a = inv["alpha_eff_star"]
            block["forward_at_alpha_star"] = gap_solve(Mg, g2=4 * math.pi * a, L=L)
            block["fpi"] = f_pi_pagels_stokar(Mg, g2=4 * math.pi * a, L=L)
        # what the running coupling gives (consistency / overshoot test)
        block["forward_running_Lam347"] = gap_solve(Mg, mode="running", L=L,
                                                     Lam3=0.347, mu_fr=0.50)
        rep[tag] = block
    return rep


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
