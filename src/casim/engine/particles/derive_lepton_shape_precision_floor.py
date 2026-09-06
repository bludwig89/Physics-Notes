"""
derive_lepton_shape_precision_floor.py -- F348: is the charged-lepton shape residual
======================================================================================
(ledger row E1, docs/status/open-derivations.md) closeable by a computed next-order
correction, or is it already measurement-floor-limited?

F175 (D4) uses the two DERIVED numbers delta* = 2/9 rad (F175, the exact E_g
representation weight dim(E_g)/dim(T_1u tensor T_1u)) and eta^2 = 1/2 (F92, the
derived 45-degree Cooper-pair equipartition amplitude) in the circulant ansatz

    sqrt(m_a) = mu * (1 + 2*sqrt(eta2) * cos(delta + 2*pi*a/3)),   a = 0, 1, 2

to predict the charged-lepton mass ratios with ZERO shape parameters:
m_mu/m_e to +0.001% and m_tau/m_e to +0.007% (F175 D4). F174 S4 already flagged
that the free 3-parameter fit to PDG masses lands at delta_fit = 0.222229 rad,
eta2_fit = 0.4999908 -- each within ~1 sigma of the exact {2/9, 1/2} -- and F175
Sec.5 already attributes the 0.007% residual to "the ~0.9 sigma eta2-delta
tension ... at current mass precision," without quantifying it further.

This module (ledger E1's first attack on "is a next-order correction tractable")
does three things NOT done before:

  D1  Recomputes the exact-point vs PDG residual directly in MeV and in units of
      the current PDG m_tau uncertainty (+-0.12 MeV) -- the single dominant error
      source, since m_e and m_mu are known many orders of magnitude more precisely.
  D2  Uses a numeric Jacobian of the two ratios (m_mu/m_e, m_tau/m_e) with respect
      to (delta, eta2) at the exact point to show that a SINGLE common small
      parameter offset (delta_fit - 2/9, eta2_fit - 1/2) reproduces BOTH the
      0.001% and 0.007% residuals simultaneously (linear reconstruction agrees
      with the direct recomputation to <1%) -- i.e. there are not two independent
      unexplained residuals, only one joint offset, already named by F174 S4.
  D3  Computes the m_tau precision (holding today's PDG central value fixed) at
      which this joint offset would become a 3-sigma or 5-sigma discrepancy --
      an explicit, falsifiable threshold for when this ledger row could move.

It does NOT re-derive delta*=2/9 (F175) or eta^2=1/2 (F92), and does NOT
re-litigate F256's route-(I) dynamical no-go (cos(3 delta*) = -B/(2C) cannot be
exact because the sea-B and induced-C terms have independent origins with no
locking relation) -- F256's conclusion is used as given: the model supplies no
mechanism capable of computing an independent next-order correction to delta*,
so any number invented to close the 0.007% residual by hand would violate the
project's algebraic/machine-precision philosophy (CLAUDE.md Practices) rather
than extend it.

Verdict target: given D1-D3, is the 0.007% residual a live discrepancy the model
owes a correction for, or is it currently indistinguishable from measurement
noise on m_tau -- in which case ledger row E1 stays QUANT x2 honestly, with a
named, computed re-attack condition instead of a fabricated correction term.
"""
import math
import os

from casim.constants import delta_star_f


# PDG 2024 charged-lepton pole masses (MeV), reused from F175/F76/F174.
M_E = 0.51099895000
M_MU = 105.6583755
M_TAU = 1776.86
M_TAU_UNC = 0.12          # PDG 2024 m_tau uncertainty (MeV) -- dominant error source

DELTA_STAR = delta_star_f  # F175: exact E_g representation weight (rad); casim.constants, not re-typed
ETA2_STAR = 0.5           # F92: exact Cooper-pair equipartition amplitude

# F174 S1: free 3-parameter (mu, eta, delta) fit to the same PDG masses,
# quoted to 6 decimal places -- reused, not refit here.
DELTA_FIT = 0.222229
ETA2_FIT = 0.4999908


def _lepton_ratios(delta, eta2):
    """Koide-Foot-Brannen circulant, returned as (m_mu/m_e, m_tau/m_e)."""
    amp = 2.0 * math.sqrt(eta2)
    v = sorted((1.0 + amp * math.cos(delta + 2.0 * math.pi * a / 3.0)) ** 2
               for a in range(3))
    return v[1] / v[0], v[2] / v[0]


def _jacobian(delta, eta2, h=1e-7):
    """Numeric d(r_mu, r_tau)/d(delta, eta2) by central differences."""
    r0mu, r0tau = _lepton_ratios(delta, eta2)
    rdmu, rdtau = _lepton_ratios(delta + h, eta2)
    remu, retau = _lepton_ratios(delta, eta2 + h)
    return {
        "dmu_ddelta": (rdmu - r0mu) / h, "dtau_ddelta": (rdtau - r0tau) / h,
        "dmu_deta2": (remu - r0mu) / h, "dtau_deta2": (retau - r0tau) / h,
    }


def run_all():
    r_mu_pdg, r_tau_pdg = M_MU / M_E, M_TAU / M_E
    r_mu_ex, r_tau_ex = _lepton_ratios(DELTA_STAR, ETA2_STAR)
    r_mu_fit, r_tau_fit = _lepton_ratios(DELTA_FIT, ETA2_FIT)

    pct_mu = (r_mu_ex / r_mu_pdg - 1.0) * 100.0
    pct_tau = (r_tau_ex / r_tau_pdg - 1.0) * 100.0

    # D1: direct MeV / sigma bookkeeping (m_tau is the dominant error source;
    # m_e, m_mu carry negligible uncertainty by comparison at this precision).
    resid_tau_MeV = (r_tau_ex - r_tau_pdg) * M_E
    resid_tau_sigma = resid_tau_MeV / M_TAU_UNC

    d1 = dict(
        r_mu_e_pred=r_mu_ex, r_mu_e_pdg=r_mu_pdg, pct_err_mu=pct_mu,
        r_tau_e_pred=r_tau_ex, r_tau_e_pdg=r_tau_pdg, pct_err_tau=pct_tau,
        resid_tau_MeV=resid_tau_MeV, m_tau_unc_MeV=M_TAU_UNC,
        resid_tau_sigma=resid_tau_sigma,
    )

    # D2: single common offset reproduces both residuals (Jacobian check)
    jac = _jacobian(DELTA_STAR, ETA2_STAR)
    d_delta = DELTA_FIT - DELTA_STAR
    d_eta2 = ETA2_FIT - ETA2_STAR
    lin_dmu = jac["dmu_ddelta"] * d_delta + jac["dmu_deta2"] * d_eta2
    lin_dtau = jac["dtau_ddelta"] * d_delta + jac["dtau_deta2"] * d_eta2
    actual_dmu = r_mu_fit - r_mu_ex
    actual_dtau = r_tau_fit - r_tau_ex
    rel_err_mu_recon = abs(lin_dmu - actual_dmu) / abs(actual_dmu)
    rel_err_tau_recon = abs(lin_dtau - actual_dtau) / abs(actual_dtau)

    d2 = dict(
        delta_offset=d_delta, eta2_offset=d_eta2, jacobian=jac,
        linearized_delta_r_mu=lin_dmu, actual_delta_r_mu=actual_dmu,
        linearized_delta_r_tau=lin_dtau, actual_delta_r_tau=actual_dtau,
        rel_reconstruction_err_mu=rel_err_mu_recon,
        rel_reconstruction_err_tau=rel_err_tau_recon,
    )

    # D3: precision threshold for future significance (central value held fixed)
    thresholds = {}
    for n_sigma in (2, 3, 5):
        needed_unc = abs(resid_tau_MeV) / n_sigma
        thresholds[str(n_sigma)] = dict(
            needed_unc_MeV=needed_unc,
            improvement_factor=M_TAU_UNC / needed_unc,
        )
    d3 = dict(thresholds=thresholds)

    return dict(D1=d1, D2=d2, D3=d3)


def check_lepton_shape_residual_is_precision_floor_limited():
    """
    F348 verdict record: the E1 shape residual (0.007% on m_tau/m_e) is a
    measurement-floor artefact, not a live gap owed a next-order correction.
    """
    out = run_all()
    d1, d2, d3 = out["D1"], out["D2"], out["D3"]

    checks = {
        "D1_reproduces_F175_D4": (
            abs(d1["pct_err_mu"] - 0.001) < 0.001
            and abs(d1["pct_err_tau"] - 0.007) < 0.001
        ),
        "D1_tau_residual_below_2sigma": abs(d1["resid_tau_sigma"]) < 2.0,
        "D2_single_offset_explains_both_residuals": (
            d2["rel_reconstruction_err_mu"] < 0.01
            and d2["rel_reconstruction_err_tau"] < 0.01
        ),
        "D3_3sigma_needs_improvement_factor_between_2_and_4": (
            2.0 < d3["thresholds"]["3"]["improvement_factor"] < 4.0
        ),
        "D3_5sigma_needs_improvement_factor_between_4_and_6": (
            4.0 < d3["thresholds"]["5"]["improvement_factor"] < 6.0
        ),
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
        "verdict": (
            "No computed next-order correction is available or owed: the "
            "0.007% m_tau/m_e residual from the exact delta*=2/9, eta^2=1/2 "
            "prediction (F175 D4) is a single {:.3f}-sigma effect against the "
            "current PDG m_tau uncertainty (+-{} MeV) -- statistically "
            "indistinguishable from measurement noise, not a discrepancy the "
            "model owes a correction for. A numeric Jacobian shows the SAME "
            "small (delta, eta2) offset that F174 S4 already flagged (the "
            "free-fit values sitting ~1 sigma from the exact ones) "
            "reconstructs both the 0.001% muon and 0.007% tau residuals "
            "simultaneously to <1% relative error -- there is one joint "
            "offset, not two independent unexplained corrections. F256 "
            "already showed the model's only candidate dynamical mechanism "
            "for shifting delta* away from exactly 2/9 (the Landau route "
            "cos(3 delta*)=-B/(2C)) cannot do so exactly, so no in-model "
            "computation can supply an independent next-order term here; "
            "adding one by hand would be a fit, not a derivation, and this "
            "project's stated precision philosophy (CLAUDE.md Practices) "
            "rules that out. Ledger row E1 stays honestly QUANT x2. Named "
            "re-attack condition: the m_tau world average would need to "
            "tighten from +-{} MeV to +-{:.4f} MeV (a {:.2f}x improvement) "
            "for this residual to reach 3-sigma significance, or +-{:.4f} MeV "
            "({:.2f}x) for 5-sigma -- below that, this is not a live "
            "question and effort is better spent on higher-priority ledger "
            "rows.".format(
                d1["resid_tau_sigma"], M_TAU_UNC,
                M_TAU_UNC, d3["thresholds"]["3"]["needed_unc_MeV"],
                d3["thresholds"]["3"]["improvement_factor"],
                d3["thresholds"]["5"]["needed_unc_MeV"],
                d3["thresholds"]["5"]["improvement_factor"],
            )
        ),
    }


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    out = run_all()
    out["verdict_record"] = check_lepton_shape_residual_is_precision_floor_limited()
    path = results_path("F348_lepton_shape_precision_floor.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"wrote {path}")
    print(out["verdict_record"]["verdict"])
