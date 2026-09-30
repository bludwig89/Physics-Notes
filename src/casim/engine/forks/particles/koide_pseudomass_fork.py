"""
casim.engine.forks.particles.koide_pseudomass_fork
==================================================

F404 fork -- route 1 of the 2026-09-24 flavour research report: Koide
"pseudo-masses" for quarks (Gerard-Goffinet-Herquet PLB 633 (2006) 563;
Zenczykowski arXiv:1301.4143), built in the model's own language and tested
for viability.

The fork's hypothesis, in lattice terms.  Each charged sector f carries a
Hermitian amplitude matrix on the T_1u generation triplet (F78: the mass is
the square of the amplitude, M_f = S_f^2):

    S_f = mu_f (1 + sqrt2 E(delta_f))  +  T_f

  * A_1g + E_g part, diagonal on the cube axes: EXACT Koide, k = 1, at an
    E_g angle delta_f -- the same structure that gives the charged leptons
    (F76/F93/F175);
  * T_f = real-symmetric T_2g + imaginary-antisymmetric T_1g off-diagonals.
    These carry BOTH the quark departure from Q = 2/3 AND the CKM matrix,
    CKM = U_U^dagger U_D with S_f = U_f diag(lambda_f) U_f^dagger.

The weak-basis diagonal of S_f is the "pseudo-mass" amplitude; physical
masses are the eigenvalues lambda_f,i = +-sqrt(m_f,i).

What is exact and what is not.
  P1  (exact, sympy)  tr S^2 = sum diag^2 + 2 sum_{a<b} |S_ab|^2, hence
      Q_phys - Q_pseudo = ||S_off||_F^2 / (tr S)^2  for every Hermitian S.
      With Q_pseudo = 2/3 the off-diagonal weight is FIXED by data.
  P2  (quantitative)  that weight, per sector and scheme.
  P3  (exact criterion, quantitative input)  Schur-Horn: a Hermitian S with
      eigenvalues lambda and diagonal d exists iff d is majorised by lambda.
      Gives the admissible E_g angles delta_f per sector and sign pattern.
  P4  (numerical)  joint existence: do U_U, U_D exist with BOTH diagonals of
      exact Koide form AND U_U^dagger U_D equal to the measured CKM moduli?
  P5  (quantitative)  the charged leptons need ||S_off|| = 0 exactly.

Data: PDG 2025 quark masses (u,d,s MS-bar at 2 GeV; c,b at m(m); t direct);
running masses at M_Z from Antusch-Hinze-Saad arXiv:2510.01312 (m = y v/sqrt2,
v = 246.22 GeV); CKM moduli from the PDG 2025 CKM review.  Values as
fetched into research_notes/Quark neutrino hierarchy lattice fit/ on
2026-09-24.

This is a FORK: a tested branch that preserves its falsification record.
It is not the adopted model.
"""

from __future__ import annotations

import math

import sympy as sp

from casim.constants import delta_star_f
from casim.numerics import rng, xp

# ---- data ----------------------------------------------------------------
_V_EW_MEV = 246.22e3 / math.sqrt(2.0)

QUARK_MASSES_MEV = {
    # PDG 2025 "mixed" convention -- reproduces the model's Q_up = 0.849,
    # Q_down = 0.731 (F76) to 0.1%
    "mixed": {"U": (2.16, 1273.0, 172560.0), "D": (4.70, 93.5, 4183.0)},
    # all six at M_Z, MS-bar (Antusch et al. 2025 Yukawas)
    "MZ": {"U": (7.04e-6 * _V_EW_MEV, 3.56e-3 * _V_EW_MEV, 0.967 * _V_EW_MEV),
           "D": (1.54e-5 * _V_EW_MEV, 3.06e-4 * _V_EW_MEV, 1.630e-2 * _V_EW_MEV)},
}
# charged-lepton pole masses (PDG 2025), MeV
LEPTON_MASSES_MEV = (0.51099895, 105.6583755, 1776.93)

# CKM: |V_us|, |V_cb|, |V_ub|, |V_td| and 1-sigma (PDG 2025 review).  A MIXED
# set: |V_us| (lambda) and J are global-fit values, |V_cb|, |V_ub|, |V_td| are
# direct-measurement averages.  Their mutual tension is what sets the unitary
# floor chi^2_min = 0.119 (review 2026-09-24); with a pure global-fit set the
# floor is ~0.  The floor is computed below (unitary_floor), not assumed.
CKM_MODULI = (0.22501, 0.0411, 0.00382, 0.0086)
CKM_SIGMA = (0.00068, 0.0012, 0.0002, 0.0002)
# standard-parametrisation angles at M_Z (UTfit via Antusch et al.)
CKM_ANGLES = (0.2251, 0.04193, 0.00370, 1.139)


# ---- helpers ---------------------------------------------------------------

def koide_shape(delta: float):
    """Exact-Koide (k = 1) amplitude shape 1 + sqrt2 cos(delta + 2 pi a/3)."""
    return [1.0 + math.sqrt(2.0) * math.cos(delta + 2.0 * math.pi * a / 3.0) for a in range(3)]


def koide_Q(masses):
    r = [math.copysign(math.sqrt(abs(m)), m) for m in masses]
    return sum(m * m for m in r) / sum(r) ** 2


def q_from_amplitudes(lam):
    return sum(x * x for x in lam) / sum(lam) ** 2


def schur_horn(d, lam, tol=1e-12) -> bool:
    """Does a Hermitian matrix with eigenvalues `lam` and diagonal `d` exist?"""
    ds, ls = sorted(d, reverse=True), sorted(lam, reverse=True)
    return (abs(sum(ds) - sum(ls)) < 1e-9 * max(1.0, abs(sum(ls)))
            and ds[0] <= ls[0] + tol and ds[0] + ds[1] <= ls[0] + ls[1] + tol)


def admissible_delta_intervals(lam, step=1e-3):
    """E_g angles delta in [0, pi/3] (one fundamental cell of the shape's
    S3 relabelling symmetry) for which the k = 1 pseudo-diagonal with the
    trace of lam is Schur-Horn admissible."""
    T = sum(lam)
    n = int(round((math.pi / 3.0) / step))
    ok = [i * step for i in range(n + 1)
          if schur_horn([T / 3.0 * s for s in koide_shape(i * step)], lam)]
    iv = []
    for x in ok:
        if iv and x - iv[-1][1] < 1.5 * step:
            iv[-1][1] = x
        else:
            iv.append([x, x])
    return [(round(a, 3), round(b, 3)) for a, b in iv]


# ---- P1: the exact trace identity -----------------------------------------

def p1_trace_identity() -> bool:
    """For a general Hermitian 3x3 S: tr S^2 = sum_a S_aa^2 + 2 sum_{a<b} |S_ab|^2,
    so Q(eigenvalues) - Q(diagonal) = ||S_off||_F^2 / (tr S)^2 exactly."""
    d = sp.symbols("d0:3", real=True)
    x = sp.symbols("x0:3", real=True)
    y = sp.symbols("y0:3", real=True)
    off = [x[i] + sp.I * y[i] for i in range(3)]
    S = sp.Matrix([[d[0], off[0], off[1]],
                   [sp.conjugate(off[0]), d[1], off[2]],
                   [sp.conjugate(off[1]), sp.conjugate(off[2]), d[2]]])
    lhs = sp.expand((S * S).trace())
    rhs = sp.expand(sum(di ** 2 for di in d) + 2 * sum(x[i] ** 2 + y[i] ** 2 for i in range(3)))
    # Q_phys = tr S^2 / (tr S)^2 because tr S^2 = sum lambda^2 = sum m, tr S = sum lambda
    return sp.simplify(lhs - rhs) == 0


def required_offdiag_fraction(masses, signs=(1, 1, 1)) -> float:
    """||S_off||_F / tr S needed for an exact-Koide (Q = 2/3) pseudo-diagonal."""
    lam = [s * math.sqrt(m) for s, m in zip(signs, masses)]
    q = q_from_amplitudes(lam)
    return math.sqrt(q - 2.0 / 3.0) if q > 2.0 / 3.0 else float("nan")


# ---- P4: the joint pseudo-mass + CKM problem --------------------------------

def _U3(t12, t13, t23, d):
    s12, c12, s13, c13 = math.sin(t12), math.cos(t12), math.sin(t13), math.cos(t13)
    s23, c23 = math.sin(t23), math.cos(t23)
    e = complex(math.cos(d), math.sin(d))
    return xp.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


def _ckm_observables(V):
    J = (V[0, 0] * V[1, 1] * V[0, 1].conjugate() * V[1, 0].conjugate()).imag
    return [abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2]), abs(V[2, 0]), abs(J)]


_J_OBS, _J_SIG = 3.12e-5, 0.13e-5          # PDG 2025 Jarlskog


def _levenberg_marquardt(fun, x0, iters=300, lam0=1e-3, h=1e-7):
    """Small hand-written LM (the numerics facade has no least-squares routine)."""
    x = xp.array(x0, dtype=float)
    r = fun(x)
    cost = float(r @ r)
    lam = lam0
    n = len(x)
    for _ in range(iters):
        J = xp.empty((len(r), n))
        for k in range(n):
            dx = xp.zeros(n)
            dx[k] = h
            J[:, k] = (fun(x + dx) - r) / h
        A = J.T @ J
        g = J.T @ r
        improved = False
        for _try in range(12):
            step = xp.linalg.solve(A + lam * xp.diag(xp.diag(A) + 1e-12), -g)
            xn = x + step
            rn = fun(xn)
            cn = float(rn @ rn)
            if cn < cost:
                x, r, cost = xn, rn, cn
                lam = max(lam / 3.0, 1e-12)
                improved = True
                break
            lam *= 4.0
        if not improved or float(xp.linalg.norm(step)) < 1e-13:
            break
    return x, r, cost


def joint_search(scheme="mixed", signs=((1, 1, 1), (1, 1, 1)), fixed_delta=None,
                 ckm_weight=1.0, n_starts=24, seed=20260924, koide_weight=1e4):
    """Search U_U, U_D (and the E_g angles, unless fixed) for exact-Koide
    pseudo-diagonals in BOTH sectors with the measured CKM.

    Returns the best (smallest pseudo-residual) solution found and the best
    CKM chi^2 among Koide-exact solutions."""
    m = QUARK_MASSES_MEV[scheme]
    lu = xp.array([s * math.sqrt(v) for s, v in zip(signs[0], m["U"])])
    ld = xp.array([s * math.sqrt(v) for s, v in zip(signs[1], m["D"])])
    obs = list(CKM_MODULI) + [_J_OBS]
    sig = list(CKM_SIGMA) + [_J_SIG]

    def parts(x):
        Uu = _U3(*x[0:4])
        P = xp.diag(xp.array([1.0, complex(math.cos(x[8]), math.sin(x[8])),
                              complex(math.cos(x[9]), math.sin(x[9]))]))
        Ud = P @ _U3(*x[4:8])
        du, dd = fixed_delta if fixed_delta else (x[10], x[11])
        su = (abs(Uu) ** 2) @ lu
        sd = (abs(Ud) ** 2) @ ld
        ru = (su - float(lu.sum()) / 3.0 * xp.array(koide_shape(du))) / float(abs(lu).sum())
        rd = (sd - float(ld.sum()) / 3.0 * xp.array(koide_shape(dd))) / float(abs(ld).sum())
        return ru, rd, Uu.conj().T @ Ud

    def fun(x):
        ru, rd, V = parts(x)
        c = xp.array([(a - b) / s for a, b, s in zip(_ckm_observables(V), obs, sig)])
        return xp.concatenate([koide_weight * ru, koide_weight * rd, ckm_weight * c])

    gen = rng.for_channel(f"koide_pseudomass_fork/{seed}")
    out = []
    for _ in range(n_starts):
        x, _, _ = _levenberg_marquardt(fun, gen.uniform(0.0, 2.0 * math.pi, 12))
        ru, rd, V = parts(x)
        pres = max(float(abs(ru).max()), float(abs(rd).max()))
        chi2 = sum(((a - b) / s) ** 2 for a, b, s in zip(_ckm_observables(V), obs, sig))
        out.append({"pseudo_resid": pres, "chi2": float(chi2), "x": [float(v) for v in x],
                    "ckm": [float(v) for v in _ckm_observables(V)]})
    exact = [o for o in out if o["pseudo_resid"] < 1e-8]
    best_exact = min(exact, key=lambda o: o["chi2"]) if exact else None
    held = [o for o in out if o["chi2"] <= 1.0]
    return {"min_pseudo_resid": min(o["pseudo_resid"] for o in out),
            # the physically meaningful figure: smallest Koide violation among
            # solutions that actually reproduce the CKM (chi^2 <= 1).  The bare
            # min_pseudo_resid is a penalty compromise that scales ~1/koide_weight.
            "min_pseudo_resid_ckm_held": min((o["pseudo_resid"] for o in held), default=None),
            "n_exact": len(exact), "best_exact": best_exact}


def unitary_floor(n_starts=12, seed=20260924):
    """Best chi^2 of ANY unitary CKM (standard parametrisation) on the five
    observables -- the floor no mass-matrix construction can beat."""
    obs = list(CKM_MODULI) + [_J_OBS]
    sig = list(CKM_SIGMA) + [_J_SIG]

    def fun(x):
        return xp.array([(a - b) / s for a, b, s in zip(_ckm_observables(_U3(*x)), obs, sig)])

    gen = rng.for_channel(f"koide_pseudomass_fork/floor/{seed}")
    best = None
    for _ in range(n_starts):
        x, r, cost = _levenberg_marquardt(fun, gen.uniform(0.0, 0.5, 4))
        best = cost if best is None else min(best, cost)
    return float(best)


def real_S_gives_J_zero() -> bool:
    """P6 (exact): if both amplitude matrices are real symmetric (no T_1g), U_U
    and U_D are real orthogonal, V = U_U^T U_D is real, and J = Im(V V V* V*) = 0."""
    a = sp.symbols("a0:9", real=True)
    b = sp.symbols("b0:9", real=True)
    V = sp.Matrix(3, 3, a).T * sp.Matrix(3, 3, b)
    J = sp.im(V[0, 0] * V[1, 1] * sp.conjugate(V[0, 1]) * sp.conjugate(V[1, 0]))
    return sp.simplify(J) == 0


# ---- the record ------------------------------------------------------------

def check_koide_pseudomass_fork(scheme: str = "mixed",
                                down_signs: str = "-++",
                                n_starts: int = 24,
                                ckm_weight: float = 1.0,
                                koide_weight: float = 100.0) -> dict:
    """F404.  Legs: P1 exact identity; P2 required off-diagonal weights; P3
    Schur-Horn delta windows; P4a lepton-like (all-positive) amplitudes cannot
    hold exact Koide in both sectors AND the measured CKM; P4b with the
    lightest down amplitude negative they can, at chi^2 < 1, for a universal
    delta* = 2/9; P5 leptons need zero off-diagonal amplitude; P6 CP violation
    needs the T_1g component."""
    checks = {}
    ok_all = True

    def rec(name, ok, detail=None):
        nonlocal ok_all
        checks[name] = {"pass": bool(ok), **{k: str(v) for k, v in (detail or {}).items()}}
        ok_all = ok_all and bool(ok)

    dsg = tuple(-1 if c == "-" else 1 for c in down_signs)
    m = QUARK_MASSES_MEV[scheme]

    rec("P1_trace_identity_exact", p1_trace_identity())

    fu = required_offdiag_fraction(m["U"])
    fd_pos = required_offdiag_fraction(m["D"])
    fd = required_offdiag_fraction(m["D"], dsg)
    rec("P2_required_offdiag_weight", fu > 0.3 and fd_pos > 0.2,
        {"scheme": scheme, "U": round(fu, 4), "D_all_positive": round(fd_pos, 4),
         f"D_{down_signs}": round(fd, 4), "U_over_Eg": round(fu * math.sqrt(3), 4),
         "D_over_Eg": round(fd * math.sqrt(3), 4)})

    lamU = [math.sqrt(v) for v in m["U"]]
    lamD_pos = [math.sqrt(v) for v in m["D"]]
    lamD = [s * math.sqrt(v) for s, v in zip(dsg, m["D"])]
    ivU, ivDp, ivD = (admissible_delta_intervals(lamU), admissible_delta_intervals(lamD_pos),
                      admissible_delta_intervals(lamD))
    ds = delta_star_f
    in_iv = lambda iv: any(a <= ds <= b for a, b in iv)
    rec("P3_schur_horn_delta_windows",
        in_iv(ivU) and not in_iv(ivDp) and in_iv(ivD),
        {"U": ivU, "D_all_positive": ivDp, f"D_{down_signs}": ivD,
         "delta_star_in_U": in_iv(ivU), "delta_star_in_D_all_positive": in_iv(ivDp),
         f"delta_star_in_D_{down_signs}": in_iv(ivD)})

    # P4a -- report the smallest Koide violation among solutions that HOLD the
    #   CKM (chi^2 <= 1), not the penalty compromise (review 2026-09-24: at
    #   koide_weight = 1e4 the 'minimum' 1.9e-3 sat at |V_cb| = 0.124).
    pos = joint_search(scheme, ((1, 1, 1), (1, 1, 1)), ckm_weight=ckm_weight,
                       n_starts=n_starts, koide_weight=koide_weight)
    held = pos["min_pseudo_resid_ckm_held"]
    rec("P4a_lepton_like_amplitudes_fail_jointly", held is not None and held > 5e-3,
        {"min_koide_violation_over_trS_at_ckm_chi2_le_1": f"{held:.2e}" if held is not None else None,
         "penalty_min_any_chi2": f"{pos['min_pseudo_resid']:.2e}",
         "koide_weight": koide_weight, "n_starts": n_starts})

    neg = joint_search(scheme, ((1, 1, 1), dsg), fixed_delta=(ds, ds), n_starts=max(6, n_starts // 4))
    be = neg["best_exact"]
    rec("P4b_universal_delta_star_fits_with_signed_down",
        be is not None and be["chi2"] < 1.0,
        {"down_signs": down_signs, "n_exact": neg["n_exact"],
         "best_chi2_5obs": round(be["chi2"], 3) if be else None,
         "ckm_Vus_Vcb_Vub_Vtd_J": [round(v, 5) for v in be["ckm"][:4]] + [f"{be['ckm'][4]:.2e}"] if be else None})

    # P7 -- non-predictive for the CKM, but the angles are CORRELATED.  With the
    #      signed down sector, pairs inside the band -0.05 <~ dD - dU <~ 0.1 fit
    #      at the unitary floor (incl. Zenczykowski's (2/27, 4/27) and the
    #      (2/27, 1/9) candidate); an off-band pair inside both Schur-Horn
    #      windows, (0.24, 0.01), has no exact-Koide solution holding the CKM.
    floor = unitary_floor()
    pairs = [(0.05, 0.05), (2.0 / 27.0, 4.0 / 27.0), (2.0 / 27.0, 1.0 / 9.0), (0.2, 0.3)]
    fits = {}
    for pr in pairs:
        r = joint_search(scheme, ((1, 1, 1), dsg), fixed_delta=pr, n_starts=max(6, n_starts // 4))
        fits[str(tuple(round(v, 4) for v in pr))] = round(r["best_exact"]["chi2"], 4) if r["best_exact"] else None
    off = joint_search(scheme, ((1, 1, 1), dsg), fixed_delta=(0.24, 0.01), n_starts=n_starts)
    off_fails = off["best_exact"] is None or off["best_exact"]["chi2"] > 1.0
    rec("P7_signed_route_nonpredictive_but_angles_correlated",
        all(v is not None and abs(v - floor) < 1e-2 for v in fits.values()) and off_fails,
        {"chi2_by_delta_pair": fits, "unitary_floor_chi2": round(floor, 4),
         "off_band_(0.24,0.01)_fails": off_fails,
         "off_band_min_koide_violation": f"{off['min_pseudo_resid']:.2e}"})

    lep = [math.sqrt(v) for v in LEPTON_MASSES_MEV]
    q_lep = q_from_amplitudes(lep)
    rec("P5_leptons_need_no_offdiag", abs(q_lep - 2.0 / 3.0) < 2e-5,
        {"Q_lep": f"{q_lep:.7f}",
         "offdiag_over_trS_upper": f"{math.sqrt(max(q_lep - 2.0 / 3.0, 0.0)):.2e}"})

    rec("P6_CP_needs_T1g_exact", real_S_gives_J_zero())

    return {"pass": ok_all, "checks": checks, "scheme": scheme}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path
    res = check_koide_pseudomass_fork()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}  {({k: v for k, v in c.items() if k != 'pass'})}")
    with open(results_path("F404_koide_pseudomass_fork.json"), "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("OVERALL", "PASS" if res["pass"] else "FAIL")
