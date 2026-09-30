"""
casim.engine.forks.particles.koide_pseudomass_minimal
=====================================================

F407 fork -- derivation three of the 2026-09-24 flavour report
(`reports/Quark neutrino hierarchy lattice fit.md`): the pseudo-mass quark
fit per sector in the report's MINIMAL ansatz, with masses AND CKM fitted
as observables with errors, in the mixed and M_Z schemes.

F404 (`koide_pseudomass_fork`) tested route 1 with a GENERAL Hermitian
amplitude matrix per sector and the masses imposed as exact eigenvalues
(14 real parameters against 5 CKM observables).  This module tests the
ansatz the report actually specifies:

    S_f = mu_f (1 + sqrt2 E(delta_f))            A_1g + E_g, exact Koide k = 1
          + sum_{a<b} t_f,ab (e_ab + e_ba)        three real T_2g amplitudes
          + i phi (e_ab - e_ba)                   ONE T_1g amplitude, one slot,
                                                  in one sector (the CP phase)

At fixed E_g angles (delta_U, delta_D) that is 2 + 6 + 1 = 9 real
parameters against 10 independent observables (six masses and the four CKM
parameters): one genuine degree of freedom.  The CKM is entered as five
measured numbers, |V_us|, |V_cb|, |V_ub|, |V_td| and J, as in F404: J alone
leaves the sign of cos(delta_CP) open, and without |V_td| the fit lands on
the wrong branch (|V_td| ~ 0.0105).  The fifth number is redundant up to the
0.119 chi^2 floor that the best unitary matrix already pays on these inputs
(F404 `unitary_floor`), so the test statistic is dchi2 = chi2 - 0.119 with
one dof.  Mass eigenvalues are signed amplitudes; the
sign pattern is an OUTPUT of S, not an input (F404 imposed it).

The minimal ansatz is a subset of F404's general Hermitian one, so every
F404 no-go (P3 Schur-Horn window, P4a all-positive joint failure, P6 CP
needs T_1g) holds here a fortiori.  What this module adds:

  M1  parameter count: 9 vs 10, and the observable Jacobian has full rank 9
      at the fitted point (no redundant parameter -> 1 real dof).
  M2  the candidate E_g angle pairs (delta*, delta*), (delta*/3, 2delta*/3)
      [Zenczykowski's physical-mass angles, reused as pseudo-angles] and
      (delta*/3, delta*/2) all fit at dchi2 <= 3.84 (95%, 1 dof), with
      |m_s pull| < 1 and a NOT-all-positive down sector selected by the fit
      itself (a negative amplitude, lightest or middle).  Each pair is
      certified by the best of (i) a multistart, (ii) continuation along the
      delta band, (iii) a stored deep-search certificate re-polished and
      re-evaluated here.  Values are upper bounds on the minimum.
  M3  off-band pairs fail (chi^2 > 9).
  M4  forcing lepton-like all-positive amplitudes and freeing m_s, the fit
      closes only by moving m_s far BELOW its PDG value.
  M5  GST does not emerge: with |V_us|, |V_td| AND J held out (keeping J
      would impose |V_us| >= J/(|V_cb||V_ub|) ~ 0.199 by unitarity alone,
      2026-09-24 review), fitted solutions reach |V_us| < 0.15 and spread
      over > 0.3.

Numerics: the hand-written Levenberg-Marquardt from F404 (the numerics
facade has no least-squares routine).  Deterministic multistart via
casim.numerics.rng.

This is a FORK: a tested branch that preserves its falsification record.
"""

from __future__ import annotations

import math

from casim.constants import delta_star_f
from casim.engine.forks.particles.koide_pseudomass_fork import (
    CKM_MODULI, CKM_SIGMA, QUARK_MASSES_MEV, _J_OBS, _J_SIG,
    _levenberg_marquardt, koide_shape, unitary_floor)
from casim.numerics import rng, xp

# ---- data ------------------------------------------------------------------
# PDG 2025 1-sigma, relative (u, d, s MS-bar 2 GeV; c, b at m(m); t direct).
# The M_Z masses (Antusch-Hinze-Saad 2025) are given the same RELATIVE errors:
# the report fetched their central values only.  Declared assumption.
MASS_REL_SIGMA = {"U": (0.07 / 2.16, 4.6 / 1273.0, 310.0 / 172560.0),
                  "D": (0.07 / 4.70, 0.8 / 93.5, 7.0 / 4183.0)}
CKM5 = tuple(CKM_MODULI) + (_J_OBS,)          # |V_us| |V_cb| |V_ub| |V_td| J
CKM5_SIGMA = tuple(CKM_SIGMA) + (_J_SIG,)
N_PARAMS = 9
N_OBS = 10                  # independent: 6 masses + 4 CKM parameters
N_MEASURED = 11             # fitted numbers: 6 masses + 5 CKM entries
UNITARY_FLOOR = 0.119       # display value; the record recomputes it via F404's unitary_floor()
DCHI2_95_1DOF = 3.84

_OFF = ((0, 1), (0, 2), (1, 2))
SLOTS = tuple((s, i) for s in "UD" for i in range(3))   # where the one T_1g sits

# E_g angle pairs (delta_U, delta_D) named in the report
CANDIDATE_PAIRS = {
    "universal_delta_star": (delta_star_f, delta_star_f),
    "zenczykowski_third_twothirds": (delta_star_f / 3.0, 2.0 * delta_star_f / 3.0),
    "coincidence_third_half": (delta_star_f / 3.0, delta_star_f / 2.0),
}
OFF_BAND_PAIRS = ((0.24, 0.01), (0.15, 0.30))

# Deep-search certificates (80 starts per T_1g slot, scipy least_squares in a
# scratch session, 2026-09-24).  Layout: (mu_U, mu_D, t_U[3], t_D[3], phi).
# They are CANDIDATES: the record re-polishes each one with its own LM and
# re-evaluates the chi^2, so a wrong vector cannot pass by being stored.
CERTIFICATES = {
    "mixed": {
        "universal_delta_star": (("U", 1), (150.85158386387877, 24.060539336595117, 30.873382298839783,
            -132.903512874234, -3.04174989469624, 6.814646162537515, -18.70181025631357,
            2.767721675883112, -4.991982668576511)),
        "zenczykowski_third_twothirds": (("U", 2), (127.06976821383988, 19.053716633760875,
            141.27309056616915, -122.94605005761555, -57.64911037967391, 25.469480415534388,
            -17.473423348273343, -9.867597832635541, 9.207017731794016)),
        "coincidence_third_half": (("D", 0), (149.87140237826193, 24.06067231649604, 106.10768931336725,
            -85.40164021798411, -31.338111532379724, 15.9937685932771, -9.902392133465828,
            -7.066017232931047, -0.24194631585344947)),
    },
    "MZ": {
        "universal_delta_star": (("D", 1), (145.43925019517522, 19.644330254158678, -28.717854299913906,
            -140.80179416630008, 19.54341995931867, -2.0668558939651844, -16.13440704063471,
            4.920704706620222, -0.6507179807601366)),
        "zenczykowski_third_twothirds": (("D", 2), (128.84193503856895, 15.870152822446048,
            -130.38948870211524, -122.58075282823522, 51.58942446982628, -20.344143865874244,
            -15.463151689516643, 6.1768819498679255, 0.4280335849588775)),
        "coincidence_third_half": (("U", 0), (145.43922055994614, 19.644244087700148, 97.26040253218497,
            -101.87343497893423, -34.529701748062585, 11.8820211364859, -10.33471458870737,
            -6.422556357665797, 1.2997225541021686)),
    },
}


# M5 certificates: |V_us| pinned at 0.10 with |V_us|, |V_td|, J held out.
# The M_Z one came from the review's blind agent (scipy, 1200 starts, units
# converted); the record re-polishes it with its own LM and residuals.
M5_CERTIFICATES = {
    "MZ": (("U", 1), (128.842259511516, 15.869917066858287, 43.60861604457072, -177.88272085686114,
                      -33.36088226950198, 3.573430530073775, -25.299993875275117, -6.20488255128542,
                      5.658650413605586)),
}


# ---- the ansatz ------------------------------------------------------------

def amplitude_matrix(mu, delta, t, phi=0.0, t1g_index=None):
    """A_1g + E_g (exact Koide) diagonal, real T_2g off-diagonals t, and an
    optional single T_1g (imaginary antisymmetric) amplitude phi."""
    S = xp.diag(xp.array(koide_shape(delta)) * mu).astype(complex)
    for (a, b), x in zip(_OFF, t):
        S[a, b] = S[b, a] = x
    if t1g_index is not None:
        a, b = _OFF[t1g_index]
        S[a, b] += 1j * phi
        S[b, a] -= 1j * phi
    return S


def _eig_by_modulus(S):
    w, U = xp.linalg.eigh(S)
    o = xp.argsort(abs(w))
    return w[o], U[:, o]


def observables(p, deltas, slot, t1g=True):
    """p = (mu_U, mu_D, t_U[3], t_D[3], phi).  Returns signed amplitudes
    (U, D), masses (U, D) and the CKM entries (|V_us|, |V_cb|, |V_ub|, |V_td|, J)."""
    phi = p[8] if t1g else 0.0
    su = amplitude_matrix(p[0], deltas[0], p[2:5], phi, slot[1] if slot[0] == "U" else None)
    sd = amplitude_matrix(p[1], deltas[1], p[5:8], phi, slot[1] if slot[0] == "D" else None)
    wu, Uu = _eig_by_modulus(su)
    wd, Ud = _eig_by_modulus(sd)
    V = Uu.conj().T @ Ud
    J = (V[0, 0] * V[1, 1] * V[0, 1].conjugate() * V[1, 0].conjugate()).imag
    return {"amp_U": wu, "amp_D": wd, "m_U": wu ** 2, "m_D": wd ** 2,
            "ckm": [float(abs(V[0, 1])), float(abs(V[1, 2])), float(abs(V[0, 2])),
                    float(abs(V[2, 0])), float(abs(J))]}


def _residuals(p, deltas, slot, scheme, *, t1g=True, hold_out=(), vus_pin=None,
               ms_free=False, force_positive=False):
    o = observables(p, deltas, slot, t1g)
    m = QUARK_MASSES_MEV[scheme]
    r = [(o["m_U"][i] / m["U"][i] - 1.0) / MASS_REL_SIGMA["U"][i] for i in range(3)]
    r += [(o["m_D"][i] / m["D"][i] - 1.0) / MASS_REL_SIGMA["D"][i]
          for i in range(3) if not (ms_free and i == 1)]
    r += [(o["ckm"][i] - CKM5[i]) / CKM5_SIGMA[i] for i in range(5) if i not in hold_out]
    if vus_pin is not None:
        r.append((o["ckm"][0] - vus_pin) / 1e-4)
    if force_positive:
        r += [min(float(w), 0.0) / 1e-3 for w in list(o["amp_U"]) + list(o["amp_D"])]
    return xp.array(r, dtype=float)


def fit(deltas, scheme="mixed", slots=SLOTS, n_starts=8, seed=0, stop_below=None, **opts):
    """Multistart LM fit at fixed E_g angles.  Starts go round-robin over the
    T_1g slots and alternate a narrow and a wide off-diagonal spread (the
    wide one reaches the middle-negative sign branch).  With `stop_below`
    the search ends at the first solution under that chi^2: an existence
    certificate, not the minimum.  Returns the best solution and all
    converged solutions."""
    m = QUARK_MASSES_MEV[scheme]
    tu = sum(math.sqrt(v) for v in m["U"]) / 3.0
    td = sum(math.sqrt(v) for v in m["D"]) / 3.0
    gen = rng.for_channel(f"koide_pseudomass_minimal/{scheme}/{seed}")
    best, allsol = None, []
    for k in range(n_starts):
        spread = 0.3 if k % 2 == 0 else 0.7
        for slot in slots:
            fun = lambda x, _s=slot: _residuals(x, deltas, _s, scheme, **opts)
            x0 = xp.concatenate([[tu * gen.uniform(0.8, 1.2), td * gen.uniform(0.8, 1.2)],
                                 gen.normal(0.0, spread, 3) * tu, gen.normal(0.0, spread, 3) * td,
                                 [gen.normal(0.0, 0.05) * td]])
            x, r, cost = _levenberg_marquardt(fun, x0, iters=200)
            sol = {"chi2": float(cost), "x": x, "slot": slot, "n_tried": len(allsol) + 1}
            allsol.append(sol)
            if best is None or cost < best["chi2"]:
                best = sol
        if stop_below is not None and best["chi2"] < stop_below:
            break
    best["obs"] = observables(best["x"], deltas, best["slot"], opts.get("t1g", True))
    return best, allsol


def continue_fit(sol, from_pair, to_pair, scheme="mixed", steps=24, **opts):
    """Deterministic continuation: carry a converged solution along the
    straight path from one E_g angle pair to another, refitting at each
    step.  Success certifies that both pairs sit on one solution branch."""
    x, slot = sol["x"], sol["slot"]
    fun = None
    for k in range(1, steps + 1):
        s = k / steps
        pr = tuple(a + s * (b - a) for a, b in zip(from_pair, to_pair))
        fun = lambda y, _pr=pr: _residuals(y, _pr, slot, scheme, **opts)
        x, r, cost = _levenberg_marquardt(fun, x, iters=200)
    out = {"chi2": float(cost), "x": x, "slot": slot, "via": "continuation"}
    out["obs"] = observables(x, to_pair, slot, opts.get("t1g", True))
    return out


def polish_certificate(scheme, name, **opts):
    """Re-polish a stored certificate with the record's own LM and residuals."""
    slot, x0 = CERTIFICATES[scheme][name]
    pr = CANDIDATE_PAIRS[name]
    fun = lambda y: _residuals(y, pr, slot, scheme, **opts)
    x, r, cost = _levenberg_marquardt(fun, xp.array(x0, dtype=float), iters=200)
    out = {"chi2": float(cost), "x": x, "slot": slot, "via": "certificate"}
    out["obs"] = observables(x, pr, slot, opts.get("t1g", True))
    return out


def jacobian_rank(x, deltas, slot, scheme, h=1e-6, rtol=1e-8, **opts):
    """Numerical rank of d(fitted numbers)/d(9 parameters) at x."""
    f0 = _residuals(x, deltas, slot, scheme, **opts)
    J = xp.empty((len(f0), len(x)))
    for k in range(len(x)):
        dx = xp.zeros(len(x))
        dx[k] = h * max(1.0, abs(float(x[k])))
        J[:, k] = (_residuals(x + dx, deltas, slot, scheme, **opts) - f0) / dx[k]
    s = xp.linalg.svd(J, compute_uv=False)
    return int((s > rtol * s[0]).sum()), [float(v) for v in s]


def _pull_ms(o, scheme):
    return (float(o["m_D"][1]) / QUARK_MASSES_MEV[scheme]["D"][1] - 1.0) / MASS_REL_SIGMA["D"][1]


# ---- heavy scans (results artifact only; not in the gate record) -----------

def delta_landscape(scheme="mixed", n=21, n_starts=6):
    """Best chi^2 over a grid of (delta_U, delta_D) in [0, pi/3]^2."""
    step = (math.pi / 3.0) / (n - 1)
    out = {}
    for i in range(n):
        for j in range(n):
            b, _ = fit((i * step, j * step), scheme, n_starts=n_starts, seed=i * n + j)
            out[f"{i * step:.4f},{j * step:.4f}"] = round(b["chi2"], 3)
    return out


def ms_profile(scheme="mixed", ms_values=(10, 20, 30, 40, 60, 93.5, 150, 230), n_starts=3):
    """All-positive amplitudes: best chi^2 with m_s held at each value,
    minimised over a (delta_U, delta_D) grid."""
    base = QUARK_MASSES_MEV[scheme]["D"]
    out = {}
    for ms in ms_values:
        QUARK_MASSES_MEV[scheme]["D"] = (base[0], float(ms), base[2])
        try:
            best = min(fit((du, dd), scheme, n_starts=n_starts, force_positive=True)[0]["chi2"]
                       for du in xp.linspace(0.0, 0.26, 10) for dd in xp.linspace(0.0, 0.24, 9))
        finally:
            QUARK_MASSES_MEV[scheme]["D"] = base
        out[str(ms)] = round(float(best), 2)
    return out


# ---- the record ------------------------------------------------------------

_POSITIVE_SEED_PAIR = {"mixed": (0.12, 0.08), "MZ": (0.10, 0.10)}


def check_koide_pseudomass_minimal(scheme: str = "mixed", n_starts: int = 10,
                                   t1g: bool = True, force_positive: bool = False) -> dict:
    """F407.  Legs M1-M5 (see module docstring)."""
    checks = {}
    ok_all = True

    def rec(name, ok, detail=None):
        nonlocal ok_all
        checks[name] = {"pass": bool(ok), **{k: str(v) for k, v in (detail or {}).items()}}
        ok_all = ok_all and bool(ok)

    opts = {"t1g": t1g, "force_positive": force_positive}
    floor = unitary_floor()

    # M2 first (M1 reuses its fitted point).  Each pair: multistart with
    # early stop, then continuation from the anchor pair's solution; keep the
    # better.  Either route yields a certificate, not a claimed minimum.
    anchor_pair = CANDIDATE_PAIRS["coincidence_third_half"]
    _, anchor_sols = fit(anchor_pair, scheme, n_starts=max(4, n_starts // 3), seed=11, **opts)
    anchors = {}
    for a in anchor_sols:            # best anchor solution in EACH T_1g slot
        if a["slot"] not in anchors or a["chi2"] < anchors[a["slot"]]["chi2"]:
            anchors[a["slot"]] = a
    fits = {}
    for name, pr in CANDIDATE_PAIRS.items():
        b, sols = fit(pr, scheme, n_starts=n_starts, seed=1,
                      stop_below=floor + 1.0, **opts)
        b["via"] = "multistart"
        for a in anchors.values():
            if a["chi2"] - floor > DCHI2_95_1DOF:
                continue
            c = continue_fit(a, anchor_pair, pr, scheme, **opts)
            if c["chi2"] < b["chi2"]:
                b = c
        c = polish_certificate(scheme, name, **opts)
        if c["chi2"] < b["chi2"]:
            b = c
        o = b["obs"]
        fits[name] = b
        dchi2 = b["chi2"] - floor
        down_signed = min(float(v) for v in o["amp_D"]) < 0.0
        rec(f"M2_{name}_fits", dchi2 <= DCHI2_95_1DOF and abs(_pull_ms(o, scheme)) < 1.0 and down_signed,
            {"deltas": tuple(round(v, 4) for v in pr), "chi2_11": round(b["chi2"], 3),
             "dchi2_1dof": round(dchi2, 3), "t1g_slot": b["slot"], "via": b["via"],
             "starts_used": len(sols),
             "m_s_MeV": round(float(o["m_D"][1]), 2), "m_s_pull": round(_pull_ms(o, scheme), 2),
             "signs_U": [int(math.copysign(1, float(v))) for v in o["amp_U"]],
             "signs_D": [int(math.copysign(1, float(v))) for v in o["amp_D"]],
             "Vus_Vcb_Vub_Vtd": [round(v, 5) for v in o["ckm"][:4]], "J": f"{o['ckm'][4]:.3e}"})

    b0 = min(fits.values(), key=lambda b: b["chi2"])
    pr0 = [CANDIDATE_PAIRS[k] for k, v in fits.items() if v is b0][0]
    rank, sv = jacobian_rank(b0["x"], pr0, b0["slot"], scheme, **opts)
    rec("M1_parameter_count_one_dof", rank == N_PARAMS,
        {"unitary_floor": round(floor, 4), "n_params": N_PARAMS, "n_independent_obs": N_OBS, "n_fitted_numbers": N_MEASURED,
         "jacobian_rank": rank, "sv_min_over_max": f"{sv[-1] / sv[0]:.2e}"})

    offb = {str(pr): round(fit(pr, scheme, n_starts=n_starts, seed=2)[0]["chi2"], 1)
            for pr in OFF_BAND_PAIRS}
    rec("M3_off_band_pairs_fail", all(v - floor > 9.0 for v in offb.values()),
        {"chi2_by_pair": offb})

    bp, _ = fit(_POSITIVE_SEED_PAIR[scheme], scheme, n_starts=n_starts, seed=3,
                ms_free=True, force_positive=True)
    ms_fit = float(bp["obs"]["m_D"][1])
    ms_pdg = QUARK_MASSES_MEV[scheme]["D"][1]
    rec("M4_all_positive_needs_small_ms",
        bp["chi2"] - floor < 1.0 and ms_fit < 0.5 * ms_pdg,
        {"deltas": _POSITIVE_SEED_PAIR[scheme], "chi2": round(bp["chi2"], 3),
         "m_s_fit_MeV": round(ms_fit, 2), "m_s_PDG_MeV": ms_pdg,
         "ratio": round(ms_fit / ms_pdg, 3)})

    pr = CANDIDATE_PAIRS["universal_delta_star"]
    _, sols = fit(pr, scheme, n_starts=2 * n_starts, seed=4, hold_out=(0, 3, 4))
    vus = sorted({round(observables(s["x"], pr, s["slot"])["ckm"][0], 3)
                  for s in sols if s["chi2"] < 1.0})
    pinned = fit(pr, scheme, n_starts=n_starts, seed=5, hold_out=(0, 3, 4), vus_pin=0.10,
                 stop_below=1.0)[0]["chi2"]
    if scheme in M5_CERTIFICATES:
        slot, x0 = M5_CERTIFICATES[scheme]
        fun = lambda y: _residuals(y, pr, slot, scheme, hold_out=(0, 3, 4), vus_pin=0.10)
        pinned = min(pinned, float(_levenberg_marquardt(fun, xp.array(x0, dtype=float), iters=200)[2]))
    gst = math.sqrt(QUARK_MASSES_MEV[scheme]["D"][0] / QUARK_MASSES_MEV[scheme]["D"][1])
    rec("M5_GST_not_emergent",
        len(vus) >= 3 and vus[-1] - vus[0] > 0.3 and pinned < 1.0,
        {"held_out": "|V_us|, |V_td|, J", "vus_solutions": vus,
         "spread": round(vus[-1] - vus[0], 3) if vus else None,
         "GST_sqrt_md_ms": round(gst, 4), "chi2_at_vus_pinned_0.10": round(pinned, 2),
         "unitarity_bound_if_J_kept": round(CKM5[4] / (CKM5[1] * CKM5[2]), 4)})

    return {"pass": ok_all, "checks": checks, "scheme": scheme}


if __name__ == "__main__":
    import json
    import sys
    from casim.engine.particles._results_path import results_path
    out = {}
    for sch in ("mixed", "MZ"):
        res = check_koide_pseudomass_minimal(scheme=sch)
        out[sch] = res
        for name, c in res["checks"].items():
            print(f"  [{sch}] [{'PASS' if c['pass'] else 'FAIL'}] {name}  "
                  f"{({k: v for k, v in c.items() if k != 'pass'})}")
    if "--scans" in sys.argv:
        for sch in ("mixed", "MZ"):
            out[f"{sch}_delta_landscape"] = delta_landscape(sch)
            out[f"{sch}_ms_profile_all_positive"] = ms_profile(
                sch, (10, 20, 30, 40, 60, 93.5, 150, 230) if sch == "mixed"
                else (3, 5, 8, 12, 20, 30, 53.2, 90))
    with open(results_path("F407_koide_pseudomass_minimal.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("OVERALL", "PASS" if all(out[s]["pass"] for s in ("mixed", "MZ")) else "FAIL")
