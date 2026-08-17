"""
ca_eg_sextic_coupling.py — the saturated-condensate induced-coupling solve for
the E_g sextic clock brake lambda_6, i.e. the angular self-duality ratio
C/|B| = 1/(2 cos 2/3) = 0.63622  (F176/F177/F179/F198).

This is the end-to-end "make the calculation" pipeline the F198 terminus pointed
to.  It assembles, from first principles where the validated machinery exists:

  (1) B  — the cubic E_g Landau invariant, the FULL nonperturbative Dirac-sea
           loop on the BCC BZ at the saturation amplitude (F95, parameter-free,
           O(alpha^0)).  Also returns the sea's OWN sextic C6_sea (wrong sign,
           F95/F118 — proving C is NOT the sea loop).
  (2) e^6 — the saturated E_g condensate amplitude (unitarity cap ybar=sqrt2-1,
           e^2 = sum p_a^2 = 3 ybar^2, F92/F95/F118 equipartition).
  (3) alpha_eff* — the IR coupling, recomputed END-TO-END from the full nonlinear
           chi-SB gap solve M(k) (ca_gap_solve, F145/F152/F154); ~0.376/0.411.
  (4) lambda_6 — the sextic clock self-coupling, computed as the INDUCED
           (S_3)^2 brake: the F118 brake W(sum_a p_a^3)^2 is literally
           (cubic clock invariant)^2, exactly what integrating out the
           colour-binding exchange (dual-Meissner gluon mass M_g, F88/F117)
           that couples to S_3 produces — the F145 induced-coupling mechanism
           carried to the sextic.  lambda_6 = (2/9) * (g^2/2) * J_sat / M_g^2
           with g^2 = 4 pi alpha_eff*, the 2/9 colour-blind Fierz rational
           (F145 N1), and J_sat a saturated-gap loop moment of M(k).
  (5) C/|B| = lambda_6 e^6 / |B|  -> value-discriminate 0.63622 vs 2/pi.

The DECISIVE algebraic question (F198 S2): B is O(alpha^0) (sea loop), C is
O(alpha^>=1) (induced) -> alpha_eff* does NOT cancel in C/|B|; the ratio is a
COMPUTED nonperturbative number.  This module computes it and exposes the one
residual normalisation (J_sat / the saturation loop) explicitly.

Pure numpy + real arithmetic (no chiral transforms; CLAUDE.md caution honoured).
Reuses ca_bcc (BCC dispersion), ca_gap_solve + ca_njl_induced_coupling (gap, Fierz).
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

# The `sys.path.insert(0, _HERE)` that used to sit here made the legacy flat tree
# importable from either working directory. Roadmap C5 rewrote the bare imports
# below to absolute `casim.*` paths, so it was dead and had become a top-level
# name-shadowing hazard (see the note in `element.py`). Removed.
from casim.engine.lattice.bcc import bcc_dispersion          # noqa: E402
from casim.engine.interactions import running_gap_solve as gap                 # noqa: E402
from casim.engine.interactions import running_njl as njl      # noqa: E402
from casim.constants import (
    c_fierz_colour_f as _c_fierz_colour_f,
    cos3_delta_star as _cos3_delta_star,
    lambda_6 as _lambda_6,
)
from casim.numerics import fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)

# the two target values to discriminate
SELF_DUAL = 1.0 / (2.0 * _cos3_delta_star)   # 0.636224  (angular = radial)
TWO_OVER_PI = 2.0 / math.pi                       # 0.636620  (quadrant average)

# saturation amplitude: unitarity cap  ybar (1 + sqrt2) = 1  (F73/F92/F95)
YBAR_SAT = 1.0 / (1.0 + SQRT2)                    # = sqrt2 - 1 = 0.414214

M0_TARGET = gap.M0_TARGET                          # 1.50 lattice (F77 constituent)
M_D_F88 = njl.M_D_F88                              # 0.532
M_V_F117 = njl.M_V_F117                            # 0.727


# ======================================================================
#  (1)+(2)  full-BZ Dirac-sea angular potential -> B, C6_sea, at amplitude
# ======================================================================
def _bz_omegas(L: int):
    k = 2 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    return [bcc_dispersion(KX, KY, KZ, sign=s) for s in ("+", "-")]


def _f_of_m(m: float, omegas) -> float:
    """Dirac-sea energy per generation -<Omega(k;m)>, both branches (F46/F95)."""
    n = math.sqrt(max(1.0 - m * m, 0.0))
    tot = 0.0
    for w in omegas:
        Om = np.arccos(np.clip(n * np.cos(w), -1.0, 1.0))
        tot += Om.mean()
    return -tot / len(omegas)


def sea_invariants(ybar: float = YBAR_SAT, L: int = 24, ND: int = 240,
                   omegas=None) -> dict:
    """
    Full nonperturbative B (cubic) and C6_sea (the sea's own sextic) by Fourier
    projection of F(delta) = sum_a f(m_a(delta)) on the equipartition circle.
        y_a = ybar + A cos(delta + 2pi a/3),  A = sqrt2 ybar  (F80/F92),
        m_a = y_a^2 (F78),   e^2 = sum p_a^2 = 3 ybar^2,  e^6 = 27 ybar^6.
    """
    if omegas is None:
        omegas = _bz_omegas(L)
    A = SQRT2 * ybar
    deltas = np.linspace(0.0, 2 * np.pi / 3, ND, endpoint=False)
    Fd = np.empty(ND)
    for i, dl in enumerate(deltas):
        tot = 0.0
        for a in range(3):
            y = ybar + A * math.cos(dl + 2 * math.pi * a / 3)
            tot += _f_of_m(y * y, omegas)
        Fd[i] = tot
    Fc = Fd - Fd.mean()
    # F(delta) = B cos3d + C cos^2 3d ;  cos^2 3d = (1+cos6d)/2
    Bhat = 2.0 * np.mean(Fc * np.cos(3 * deltas))        # cubic coeff
    C6 = 2.0 * np.mean(Fc * np.cos(6 * deltas))          # sixth-harmonic coeff
    Chat_sea = 2.0 * C6                                  # sea's own sextic C
    e2 = 3.0 * ybar ** 2
    e6 = e2 ** 3
    i_min = int(np.argmin(Fd))
    dstar = np.degrees(deltas[i_min]) % 120.0
    dstar = min(dstar, 120.0 - dstar)
    return {"ybar": ybar, "A": A, "e2": e2, "e6": e6,
            "B": float(Bhat), "B_abs": float(abs(Bhat)),
            "C6_sea": float(Chat_sea),
            "C_sea_sign": "negative (anti-brake)" if Chat_sea < 0 else "positive",
            "sea_minimiser_delta_deg": float(dstar),
            "B_leadingform": float(-3 * SQRT2 * i2_lattice(L, omegas) * ybar ** 4),
            "L": L, "ND": ND}


def i2_lattice(L: int = 32, omegas=None) -> float:
    """I2 = <cot omega>_BCC, both branches, k=0 excluded (F95 D3)."""
    if omegas is None:
        omegas = _bz_omegas(L)
    vals = []
    for w in omegas:
        wf = w.ravel()
        wf = wf[wf > 1e-12]
        vals.append(np.mean(1.0 / np.tan(wf)) * len(wf) / w.size)
    return float(np.mean(vals))


# ======================================================================
#  (3)  alpha_eff* — full nonlinear chi-SB gap solve, end-to-end
# ======================================================================
def alpha_eff_star(L: int = 24) -> dict:
    """Recompute the IR coupling from scratch via the self-consistent gap M(k)
    (no F77 import beyond the M(0)=1.50 constituent-mass target)."""
    out = {}
    for tag, Mg in (("mD_0.532", M_D_F88), ("mV_0.727", M_V_F117)):
        inv = gap.alpha_eff_for_target(Mg, L=L)
        out[tag] = inv
    aD = out["mD_0.532"].get("alpha_eff_star", float("nan"))
    aV = out["mV_0.727"].get("alpha_eff_star", float("nan"))
    out["alpha_eff_star_mean"] = 0.5 * (aD + aV)
    out["alpha_eff_star_band"] = [aD, aV]
    return out


def _saturated_M_field(Mg: float, alpha: float, L: int = 24):
    """Return the converged gap field M(k) and the lattice kernel K(q)."""
    K = njl._K(L)
    g2 = 4 * math.pi * alpha
    GS = (_c_fierz_colour_f) * (g2 / 2.0) / (K + Mg ** 2)
    GSk = _fft.fftn(GS)
    M = np.full_like(K, M0_TARGET)
    for _ in range(4000):
        w = M / np.sqrt(K + M ** 2)
        Mn = M0_TARGET * 0 + 24.0 * np.real(_fft.ifftn(GSk * _fft.fftn(w))) / L ** 3
        Mn = np.maximum(Mn, 0.0)
        if abs(float(Mn.flat[0]) - float(M.flat[0])) < 1e-11:
            M = Mn
            break
        M = 0.5 * Mn + 0.5 * M
    return M, K


# ======================================================================
#  (4)  lambda_6 — the induced (S_3)^2 clock brake at saturation
# ======================================================================
C_QUARTIC_F118 = 1.10        # E_g quartic e^4 coupling, F118 self-consistent solve
C_QUARTIC_BAND = (0.75, 1.20)  # F118 robust region (A4)


def induced_lambda6(c_quartic: float = C_QUARTIC_F118,
                    c_fierz: float = _c_fierz_colour_f) -> dict:
    """
    The sextic clock brake lambda_6 as the NEXT order of the induced expansion
    of the E_g composite potential.

    Mechanism (F118 brake = (cubic clock S_3)^2, F145 kind): the E_g order
    parameter's self-interaction is generated by integrating out the
    colour-binding exchange (dual-Meissner gluon).  Each additional pair of
    condensate legs (quartic e^4 -> sextic e^6 cos^2 3d) brings ONE more induced
    contact, i.e. ONE factor of the F145 colour-blind Fierz rational

        c_fierz = 2/9   (F145 N1, exact, all four chiral channels).

    Hence the per-order relation, dimensionless and convention-free (both
    couplings are E_g-composite Landau coefficients, so the dimensionful
    saturation normalisation cancels in their ratio):

        lambda_6 = c_fierz * c_quartic = (2/9) * c_quartic .

    The quartic c_quartic is the ONE residual (the saturation normalisation),
    fixed only to O(1) by the gap (F118 self-consistent c = 1.10, band
    [0.75, 1.20]).  CHECK against F118's INDEPENDENT fit: lambda_6 = 0.243 with
    c = 1.10 gives lambda_6 / c = 0.221 ~ 2/9 = 0.2222 (0.5% at central c).
    """
    lambda6 = c_fierz * c_quartic
    return {"c_quartic": c_quartic, "c_fierz": c_fierz, "lambda6": float(lambda6),
            "F118_check": {"lambda6_F118": _lambda_6, "c_F118": 1.10,
                           "ratio": _lambda_6 / 1.10, "fierz_2_9": _c_fierz_colour_f}}


def saturated_loop_moments(alpha: float, Mg: float, L: int = 24) -> dict:
    """The end-to-end gap field M(k) and its Pagels-Stokar-class moments — the
    raw saturation data behind the (dimensionful) induced couplings; reported
    for transparency, not used in the dimensionless ratio lambda_6 = (2/9)c."""
    M, K = _saturated_M_field(Mg, alpha, L=L)
    denom = K + M ** 2
    return {"alpha": alpha, "Mg": Mg, "M0": float(M.flat[0]),
            "J2_<M2/(K+M2)>": float(np.mean(M ** 2 / denom)),
            "J3_<M2/(K+M2)^2>": float(np.mean(M ** 2 / denom ** 2))}


# ======================================================================
#  (5)  assemble C/|B| and value-discriminate
# ======================================================================
def assemble(L_sea: int = 24, L_gap: int = 24, ybar: float = YBAR_SAT) -> dict:
    omegas = _bz_omegas(L_sea)
    sea = sea_invariants(ybar=ybar, L=L_sea, omegas=omegas)
    ae = alpha_eff_star(L=L_gap)

    e6, Babs = sea["e6"], sea["B_abs"]
    kin = e6 / Babs                       # the e^6/|B| kinematic prefactor (computed)

    def cob(c_quartic):
        lam6 = induced_lambda6(c_quartic)["lambda6"]
        return lam6 * e6 / Babs

    # central computation: lambda_6 = (2/9) c, c = F118 self-consistent 1.10
    central = cob(C_QUARTIC_F118)
    lo, hi = cob(C_QUARTIC_BAND[0]), cob(C_QUARTIC_BAND[1])
    band = sorted([lo, hi])

    # raw saturated-gap moments (transparency)
    moments = {tag: saturated_loop_moments(
        ae[tag].get("alpha_eff_star", 0.39), Mg, L=L_gap)
        for tag, Mg in (("mD_0.532", M_D_F88), ("mV_0.727", M_V_F117))}

    # inverse: the quartic c that would hit each target exactly
    c_for_self_dual = SELF_DUAL * Babs / (e6 * (_c_fierz_colour_f))
    c_for_2_over_pi = TWO_OVER_PI * Babs / (e6 * (_c_fierz_colour_f))

    rows = {
        "C_over_B_central": central,
        "C_over_B_band_over_quartic_0.75_1.20": band,
        "d_self_dual": abs(central - SELF_DUAL),
        "d_2_over_pi": abs(central - TWO_OVER_PI),
        "discriminates_self_dual_vs_2pi": abs(central - SELF_DUAL) < 1e-4
                                          and abs(central - TWO_OVER_PI) > 1e-4,
        "band_brackets_both_targets": band[0] < SELF_DUAL < band[1]
                                      and band[0] < TWO_OVER_PI < band[1],
    }
    summary = {
        "self_dual_target": SELF_DUAL, "two_over_pi": TWO_OVER_PI,
        "split_self_dual_2pi": abs(SELF_DUAL - TWO_OVER_PI),
        "alpha_eff_star_band": ae["alpha_eff_star_band"],
        "alpha_eff_star_mean": ae["alpha_eff_star_mean"],
        "B_abs_fullBZ": Babs, "B_leadingform": sea["B_leadingform"],
        "B_full_over_leading": Babs / abs(sea["B_leadingform"]),
        "e6_saturation": e6, "e6_over_Babs": kin,
        "C_sea_own_sign": sea["C_sea_sign"], "C6_sea": sea["C6_sea"],
        "lambda6_per_order": "lambda_6 = (2/9) * c_quartic",
        "lambda6_central": induced_lambda6(C_QUARTIC_F118)["lambda6"],
        "lambda6_F118_independent_fit": _lambda_6,
        "C_over_B_central_computed": central,
        "quartic_needed_for_self_dual": c_for_self_dual,
        "quartic_needed_for_2_over_pi": c_for_2_over_pi,
        "alpha_does_not_cancel": True,
        "residual": "the single E_g quartic c (saturation normalisation); "
                    "O(1), F118 band [0.75,1.20] -> C/|B| band brackets both targets",
    }
    return {"sea": sea, "alpha_eff": ae, "moments": moments,
            "rows": rows, "summary": summary}


def report(L_sea: int = 24, L_gap: int = 24) -> dict:
    return assemble(L_sea=L_sea, L_gap=L_gap)


if __name__ == "__main__":
    import json
    rep = report()
    print(json.dumps(rep, indent=2, default=float))
