"""F402 — the Ji-type four-term nucleon-mass decomposition, built in the model's
own sectors: what it supports and what it does not.

Answers NB2-004 "New questions opened" item 2. The load-bearing identities are
re-derived here INDEPENDENTLY of `casim.engine.particles.baryon_mass_decomposition`
(finite differences of the gap equation and of the ECG eigenvalue, an RK4 solve of
the momentum-fraction ODE) so this is a cross-check, not a restatement.

  A1 (machine)      NJL dilatation identity  M = m0 dM/dm0 - 2G dM/dG + Lam dM/dLam,
      by the test's own finite differences at four parameter points.
  A2 (quantitative) NJL sigma term sigma_N = 3 m0 dM_c/dm0 = 46.2 MeV, against the
      test's own finite difference; and its honest comparison with the measured
      nucleon sigma term (undershoot of 2-4 sigma).
      DECLARED CONTROL: doubling m0 must take sigma_N out of that band.
  B1 (machine)      Cornell three-body Hellmann-Feynman:  m dM/dm = 3m - <T>,
      sigma dM/dsigma = <V_conf>, alpha dM/dalpha = <V_coul>.
  B2 (quantitative) The virial residual, on which the energies-vs-momentum-fraction
      constructions agree, falls with the basis (8 -> 14 mesh; not strictly
      monotonic beyond, ~7e-5 at 18); and H_a - (M - H_m)/4 equals
      -virial/4 EXACTLY (an algebraic identity), so the quarter rule holds iff
      the virial theorem does.
  B3 (quantitative) At the F122 baseline the NR quark-mass term H_m = 3m - <T> is
      NEGATIVE (psibar psi < 0 is impossible relativistically): the NR string
      solver cannot supply the mass term. At the half-rule it is positive but
      2.7x the NJL value. DECLARED CONTROL: heavy quarks (m = 5) must make H_m
      positive, flipping the negativity assertion.
  C1 (exact)        LO second-moment evolution: closed form == RK4 of the ODE,
      momentum conservation, asymptote 16/(16+3 n_f).
  C2 (quantitative) Model-native gluon momentum fraction at 2 GeV (0.18-0.25) is
      2-3 sigma below the lattice values (chiQCD-derived 0.49(9); ETMC 0.427(92)),
      needing 2.3-3.0x more evolution than the model's alpha_s supplies, or a
      gluon share of 0.29-0.40 already present at Lam_NJL: the H_E / H_g SPLIT is
      not supported, and the deficit is a statement about the x_g = 0 start.
"""
from __future__ import annotations

import math
import random

from casim.constants import G_Lambda2_NJL, Lambda_NJL_GeV
from casim.engine.particles import baryon_mass_decomposition as D
from casim.engine.particles import meson as MES

LAM = float(Lambda_NJL_GeV)
GL2 = float(G_Lambda2_NJL)


def _M(G, Lam, m0):                       # the test's own gap solve handle
    return MES.gap_solve(G, Lam, m0, 0.3)


def _fd(f, x, h=1e-6):
    return (f(x * (1 + h)) - f(x * (1 - h))) / (2 * x * h)


# ── A ─────────────────────────────────────────────────────────────────────

def check_A1_njl_dilatation():
    worst = 0.0
    pts = [(GL2, LAM, 0.0055), (1.8, LAM, 0.0055), (3.0, 0.5, 0.008),
           (2.4, 0.8, 0.003)]
    for gl2, lam, m0 in pts:
        G = gl2 / lam ** 2
        M = _M(G, lam, m0)
        dm = _fd(lambda x: _M(G, lam, x), m0)
        dG = _fd(lambda x: _M(x, lam, m0), G)
        dL = _fd(lambda x: _M(G, x, m0), lam)
        res = abs(m0 * dm - 2 * G * dG + lam * dL - M) / M
        worst = max(worst, res)
        assert res < 1e-6, (gl2, lam, m0, res)
        mod = D.njl_nucleon_analog(gl2, lam, m0)
        assert mod["dilatation_residual"] < 1e-12
    return {"worst_independent_fd_residual": worst, "n_points": len(pts)}


def check_A2_sigma_term(m0_MeV=5.5):
    m0 = m0_MeV * 1e-3
    G = GL2 / LAM ** 2
    M0 = _M(G, LAM, m0)
    fd = _fd(lambda x: _M(G, LAM, x), m0)
    sig_fd = 3.0 * m0 * fd * 1e3
    nj = D.njl_nucleon_analog(m0=m0)
    assert abs(nj["H_m"] * 1e3 - sig_fd) / sig_fd < 1e-6, (nj["H_m"], sig_fd)
    lat = D.lattice_targets()
    pull_h = (sig_fd - lat["sigma_piN_hoferichter_MeV"]["value"]) / \
        lat["sigma_piN_hoferichter_MeV"]["unc"]
    pull_f = (sig_fd - lat["sigma_piN_flag2024_MeV"]["value"]) / \
        lat["sigma_piN_flag2024_MeV"]["unc"]
    # DECLARED CONTROL: the band [-4.5, -1.5] sigma pins the documented
    # undershoot; doubling m0 leaves it.
    assert -4.5 < pull_h < -1.5 and -4.5 < pull_f < -1.5, (pull_h, pull_f)
    return {"sigma_N_MeV": sig_fd, "M_c_GeV": M0, "pull_vs_hoferichter": pull_h,
            "pull_vs_flag2024": pull_f}


# ── B ─────────────────────────────────────────────────────────────────────

def check_B1_cornell_hellmann_feynman():
    out = D.cornell_fh_residuals(0.785, 1.0, 0.5, n_mesh=8)
    for k in ("rel_resid_m", "rel_resid_sigma", "rel_resid_alpha"):
        assert out[k] < 1e-6, (k, out[k])
    return {k: out[k] for k in ("rel_resid_m", "rel_resid_sigma",
                                "rel_resid_alpha")}


def check_B2_virial_and_quarter_rule():
    res = {}
    for n in (8, 14):
        ex = D.cornell_expectations(0.785, 1.0, 0.5, n_mesh=n)
        q = D.cornell_quartet(ex)
        res[n] = abs(q["virial_residual"])
        # exact algebra: H_a - (M-H_m)/4 = -virial/4 (in units of M)
        M = ex["M"]
        lhs = q["H_a"] - 0.25 * (M - q["H_m"])
        assert abs(lhs - (-0.25 * q["virial_residual"] * M)) / M < 1e-9
        assert abs(q["sum_over_M"] - 1.0) < 1e-9
        assert q["energies_vs_fractions_HE"] < 1e-12
    assert res[14] < res[8] and res[14] < 1e-3, res
    return {"virial_residual_by_basis": res}


def check_B3_nr_mass_term_unphysical(cornell_m=0.785):
    ex = D.cornell_expectations(cornell_m, 1.0, 0.5, n_mesh=10)
    q = D.cornell_quartet(ex)
    assert q["H_m_negative"] is True, (
        "expected the NR quark-mass term to be negative at the F122 baseline",
        q["H_m"])
    half = D.cornell_quartet(D.cornell_expectations(
        0.785, 1.0, 0.5, n_mesh=10, **D.HALF_RULE))
    nj = D.njl_nucleon_analog()
    assert not half["H_m_negative"]
    assert half["frac"]["H_m"] > 2.0 * nj["H_m_frac"]
    # both string routes leave the gluon share far short of the lattice value
    assert q["x_g"] < 0.25 and half["x_g"] < 0.25
    return {"baseline_H_m_frac": q["frac"]["H_m"], "half_H_m_frac":
            half["frac"]["H_m"], "njl_H_m_frac": nj["H_m_frac"],
            "x_g_baseline": q["x_g"], "x_g_half": half["x_g"]}


# ── C ─────────────────────────────────────────────────────────────────────

def check_C1_dglap_closed_form():
    for nf in (3, 4):
        a = D.dglap_asymptote(nf)
        assert abs(a["x_g_inf"] - 16.0 / (16.0 + 3 * nf)) < 1e-15
        tau_end, n = 0.7, 20000
        h = tau_end / n
        xq, xg = 1.0, 0.0
        f = lambda xq_, xg_: (-(16.0 / 9.0) * xq_ + (nf / 3.0) * xg_,
                              (16.0 / 9.0) * xq_ - (nf / 3.0) * xg_)
        for _ in range(n):
            k1 = f(xq, xg)
            k2 = f(xq + 0.5 * h * k1[0], xg + 0.5 * h * k1[1])
            k3 = f(xq + 0.5 * h * k2[0], xg + 0.5 * h * k2[1])
            k4 = f(xq + h * k3[0], xg + h * k3[1])
            xq += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            xg += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        assert abs(xg - D.x_g_evolved(tau_end, nf)) < 1e-9
        assert abs(xq + xg - 1.0) < 1e-12
        rng = random.Random(402)
        for _ in range(5):
            t = rng.uniform(0.05, 1.0)
            assert abs(D.tau_required(D.x_g_evolved(t, nf), nf) - t) < 1e-12
    return {"checked_nf": [3, 4]}


def check_C2_model_gluon_share_short():
    """Against BOTH lattice gluon momentum fractions (chiQCD-derived 0.49(9),
    ETMC 0.427(92)): the model-native value stays below each, at 2-3 sigma,
    needing 2.3-3.0x more evolution. Bands cover both targets (widened on
    review, attack 4: the ETMC target moves the pull to 1.98 sigma)."""
    ev = D.evolution_scenarios()
    hi = ev["x_g_with_frozen_IR_hi"]
    assert ev["x_g_perturbative_start_1GeV"] < hi < 0.30
    out = {"x_g_model_hi": hi}
    for name, t in ev["targets"].items():
        assert hi < t["x_g"], (name, hi, t["x_g"])
        assert -3.5 < t["pull_of_model_hi"] < -1.5, (name, t["pull_of_model_hi"])
        assert 2.0 < t["tau_deficit_factor_hi"] < 3.6, (
            name, t["tau_deficit_factor_hi"])
        assert t["mean_alpha_required"] > 1.0
        # the gluon share the NJL START would need for the model's own tau
        assert 0.25 < t["x_g0_required_at_LamNJL"] < 0.45
        out[name] = {"pull": t["pull_of_model_hi"],
                     "tau_deficit_factor": t["tau_deficit_factor_hi"],
                     "mean_alpha_required": t["mean_alpha_required"],
                     "x_g0_required": t["x_g0_required_at_LamNJL"]}
    # start-value sensitivity: the deficit is a statement about x_g0 = 0
    sens = ev["x_g_start_sensitivity"]
    assert sens["x_g0=0.0"] < sens["x_g0=0.1"] < sens["x_g0=0.3"]
    out["start_sensitivity"] = sens
    return out


CHECKS = (
    ("A1_njl_dilatation", check_A1_njl_dilatation),
    ("A2_sigma_term", check_A2_sigma_term),
    ("B1_cornell_hellmann_feynman", check_B1_cornell_hellmann_feynman),
    ("B2_virial_and_quarter_rule", check_B2_virial_and_quarter_rule),
    ("B3_nr_mass_term_unphysical", check_B3_nr_mass_term_unphysical),
    ("C1_dglap_closed_form", check_C1_dglap_closed_form),
    ("C2_model_gluon_share_short", check_C2_model_gluon_share_short),
)


def check_all(m0_MeV=5.5, cornell_m=0.785):
    """Registry entry point.

    Two declared controls (D9/H2):
    ``--param m0_MeV=11``      doubling the NJL current mass takes sigma_N out of
        the documented 2-4 sigma undershoot band. A2 must go red.
    ``--param cornell_m=5.0``  heavy quarks make the NR mass term 3m - <T>
        positive, so the negativity claim at the F122 baseline fails. B3 must go red.
    """
    kw = {"check_A2_sigma_term": {"m0_MeV": m0_MeV},
          "check_B3_nr_mass_term_unphysical": {"cornell_m": cornell_m}}
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
