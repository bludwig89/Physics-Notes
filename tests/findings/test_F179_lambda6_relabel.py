"""[PARTIALLY SUPERSEDED 2026-07-16 by F253, F255, F256 — ledger S6-F253-weight-as-phase]

  DEAD:
    D5 verdict bookkeeping: 'one-angle consistency fit ... NOT zero-parameter'
    and listing delta* among fitted_inputs.

  STILL LIVE:
    D1 condensate invariants; D2 lambda_6 not a clean rational (re-affirmed by
    F256); D3 3 delta* = Q = 2/3 within 1 sigma — now the canonical
    falsification handle; D4 spectrum to ~0.01%.

  See docs/theory/supersessions.yaml for the full record.

F179 — The E_g sextic brake lambda_6 / C: derivation attempt closes negative;
the lepton spectrum is honestly relabelled as a ONE-ANGLE consistency fit whose
single parameter is the convention-independent condensate angle delta* (not the
convention-laden lambda_6), Koide-locked to delta* = 2/9 rad at < 1 sigma.

Addresses audit-2026-06-29 C2 ("derive C(lambda_6) or relabel"). This finding
does NOT achieve a first-principles derivation of lambda_6 (that is the
saturated-condensate induced-coupling solve F92 s.6 / F95 s.7 / F118 s.7 / F150
s.7 leave open). It establishes the decisive numerical facts that fix the honest
epistemic status:

  D1  Condensate invariants from PDG: A/ybar = sqrt2 (=> Q = 2/3, derived F92),
      cos3delta* = 0.785874, delta* = 12.7328 deg, all reproduced.
  D2  lambda_6 is NOT a clean rational: the two recurring block rationals that
      bracket the F118 fit — 2/9 (Fierz, F145) and 1/4 (rotor, F115) — give
      condensate angles 10.25 deg and 13.40 deg, MISSING the data 12.7328 deg by
      2.48 deg and 0.67 deg. So lambda_6 = 0.243 carries a non-rational
      saturation normalization; the bare induced rational does not deliver it.
  D3  The convention-INDEPENDENT target works: 3delta* = Q = 2/3 rad
      (delta* = 2/9 rad) reproduces the data angle and is satisfied to < 1 sigma
      under m_tau experimental error (same confidence class as Koide itself).
  D4  Prediction content if the two candidate-exact relations (Q = 2/3 and
      delta* = 2/9 rad) are GRANTED: one mass anchor (m_tau) then fixes the whole
      charged-lepton spectrum to ~0.01% (m_mu/m_tau and m_e/m_tau). This quantifies
      the spectrum as a one-angle fit, not a zero-parameter prediction.
  D5  Verdict bookkeeping: derivation attempt negative; relabel is the honest
      outcome; the residual is the single shared IR normalization (F150 cluster).

Real arithmetic only (PDG masses + closed forms); no chiral transforms; numpy-safe.
"""
import json
import os
import numpy as np

# PDG charged leptons (MeV) — identical to F92/F93/F95/F150
ME, MMU, MTAU = 0.51099895, 105.6583755, 1776.86
DMTAU = 0.12  # PDG 1-sigma on m_tau (MeV); m_e, m_mu uncertainties negligible

# F118/F150 reference point: fitted lambda_6 <-> data angle
LAM_FIT = 0.243
COS3D_DATA_REF = 0.785874


def condensate_invariants(me=ME, mmu=MMU, mtau=MTAU):
    """y_a = sqrt(m_a) = ybar + A cos(delta + 2 pi a/3). Z3 decomposition.
    cos(3 delta) is assignment-independent; returned with Q, A/ybar."""
    m = np.array([me, mmu, mtau])
    y = np.sqrt(m)
    ybar = y.mean()
    p = y - ybar
    Q = m.sum() / (y.sum() ** 2)
    Aratio = np.sqrt((2.0 / 3.0) * np.sum(p ** 2)) / ybar
    w = np.exp(2j * np.pi * np.arange(3) / 3.0)
    Z = (2.0 / 3.0) * np.sum(p * np.conj(w))          # = A e^{i delta}
    cos3delta = np.cos(3.0 * np.angle(Z))              # invariant
    delta = np.degrees(np.arccos(cos3delta)) / 3.0     # hierarchical branch [0,60)
    return dict(ybar=ybar, Aratio=Aratio, Q=Q, cos3delta=cos3delta,
                delta_deg=delta, three_delta_rad=np.radians(3.0 * delta))


def angle_from_lambda(lam):
    """At fixed (derived) B and amplitude, cos3delta = -B/(2C) scales as 1/lambda_6.
    Calibrate off the F118 data point (lambda=0.243 <-> cos3delta=0.785874)."""
    c = COS3D_DATA_REF * LAM_FIT / lam
    return c, np.degrees(np.arccos(c)) / 3.0


def predict_spectrum(Aratio, delta_rad, anchor_mtau=MTAU):
    """Whole charged-lepton spectrum from (A/ybar, delta) + one mass anchor."""
    a = np.arange(3)
    y = 1.0 + Aratio * np.cos(delta_rad + 2.0 * np.pi * a / 3.0)
    m = np.sort(y ** 2)
    return m * anchor_mtau / m[2]


def test_F179():
    results = {"checks": {}}

    # ---- D1: condensate invariants ----
    inv = condensate_invariants()
    d1 = (abs(inv["Aratio"] - np.sqrt(2)) < 5e-5 and
          abs(inv["Q"] - 2.0 / 3.0) < 1e-4 and
          abs(inv["cos3delta"] - COS3D_DATA_REF) < 5e-6 and
          abs(inv["delta_deg"] - 12.7328) < 1e-3)
    results["checks"]["D1_invariants"] = {
        "Aratio": inv["Aratio"], "Q": inv["Q"], "cos3delta": inv["cos3delta"],
        "delta_deg": inv["delta_deg"], "pass": bool(d1)}
    assert d1

    # ---- D2: lambda_6 is NOT a clean rational (both brackets miss the angle) ----
    c_29, d_29 = angle_from_lambda(2.0 / 9.0)
    c_14, d_14 = angle_from_lambda(1.0 / 4.0)
    miss_29 = abs(d_29 - inv["delta_deg"])
    miss_14 = abs(d_14 - inv["delta_deg"])
    # both rationals must MISS the data angle by a physically resolvable amount
    d2 = (miss_29 > 1.0) and (miss_14 > 0.3)
    results["checks"]["D2_lambda6_not_rational"] = {
        "delta(2/9)_deg": d_29, "miss_2/9_deg": miss_29,
        "delta(1/4)_deg": d_14, "miss_1/4_deg": miss_14,
        "data_delta_deg": inv["delta_deg"], "pass": bool(d2)}
    assert d2

    # ---- D3: convention-independent target 3delta* = Q = 2/3, within 1 sigma ----
    diffs = []
    for sign in (-1, 0, 1):
        b = condensate_invariants(mtau=MTAU + sign * DMTAU)
        diffs.append(b["three_delta_rad"] - b["Q"])
    hi = condensate_invariants(mtau=MTAU + DMTAU)
    lo = condensate_invariants(mtau=MTAU - DMTAU)
    sigma_c3 = abs(hi["cos3delta"] - lo["cos3delta"]) / 2.0
    n_sigma = abs(inv["cos3delta"] - np.cos(2.0 / 3.0)) / sigma_c3
    d3 = (abs(inv["three_delta_rad"] - inv["Q"]) < 5e-5) and (n_sigma < 1.0)
    results["checks"]["D3_target_3delta_eq_Q"] = {
        "three_delta_rad": inv["three_delta_rad"], "Q": inv["Q"],
        "abs_diff": abs(inv["three_delta_rad"] - inv["Q"]),
        "cos3delta_minus_cos(2/3)": inv["cos3delta"] - np.cos(2.0 / 3.0),
        "sigma_cos3delta_from_mtau": sigma_c3, "deviation_in_sigma": n_sigma,
        "diffs_over_mtau_band": diffs, "pass": bool(d3)}
    assert d3

    # ---- D4: prediction content if both relations granted -> ~0.01% spectrum ----
    m = predict_spectrum(np.sqrt(2), 2.0 / 9.0)
    err_mu = m[1] / m[2] / (MMU / MTAU) - 1.0
    err_e = m[0] / m[2] / (ME / MTAU) - 1.0
    d4 = (abs(err_mu) < 1e-3) and (abs(err_e) < 1e-3)
    results["checks"]["D4_granted_prediction"] = {
        "m_mu_over_m_tau_err": err_mu, "m_e_over_m_tau_err": err_e,
        "pass": bool(d4)}
    assert d4

    # ---- D5: verdict bookkeeping (derivation negative -> relabel) ----
    verdict = {
        "lambda6_derived_from_first_principles": False,
        "honest_label": "one-angle consistency fit (delta* = 2/9 rad), NOT zero-parameter",
        "convention_independent_parameter": "delta* (3delta* = Q = 2/3 rad)",
        "spectrum_accuracy_if_granted": "~0.01% (m_mu, m_e relative to m_tau)",
        "residual": "single shared IR-coupling normalization (F124/F144/F145/F150 cluster)",
        "derived_inputs": ["generation count 3 (F75)", "Q = 2/3 equipartition (F92)"],
        "fitted_inputs": ["overall scale N (F119)", "condensate angle delta* (this/F118/F150)"],
    }
    results["checks"]["D5_verdict"] = {"verdict": verdict, "pass": True}
    results["verdict"] = verdict

    out = os.path.join(os.path.dirname(__file__), "..", "..",
                       "test-results", "F179_lambda6_relabel.json")
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    r = test_F179()
    for name, c in r["checks"].items():
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {name}")
    print("\nverdict:", json.dumps(r["verdict"], indent=2))
    print("\nOverall:", "5/5 PASS" if all(c["pass"] for c in r["checks"].values()) else "FAIL")
