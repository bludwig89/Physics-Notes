"""
F200 — The saturated-condensate induced-coupling computation of the E_g sextic
brake C/|B| (the angular self-duality 0.63622 vs 2/pi), built end-to-end.

This executes the F199 "honest terminus" as an actual machine calculation:
B (full-BZ sea loop), e^6 (saturation amplitude), alpha_eff* (full nonlinear
gap solve), and lambda_6 (induced per-order Fierz) -> C/|B|, value-discriminated.

Checks:
  G1  B is the FULL-BZ Dirac-sea cubic at saturation: B<0 (hierarchical side),
      full/leading ~1.8 (higher-order sea terms at saturation amplitude).
  G2  the sea's OWN sextic C6 is NEGATIVE (anti-brake) -> C is NOT the sea loop;
      it must be the induced clock self-coupling (reproduces F118 B1).
  G3  alpha_eff* recomputed end-to-end from the nonlinear gap M(k): in the
      F152/F154 band [0.376, 0.411], mean ~0.39 (no value imported).
  G4  DERIVATION CONTENT: lambda_6 = (2/9) c_quartic (per-order induced Fierz);
      with the F118 self-consistent quartic c=1.10 this gives 0.244, matching
      F118's INDEPENDENT fit 0.243 to <=1% -> the sextic/quartic ratio IS the
      F145 colour-blind Fierz rational 2/9.
  G5  ASSEMBLY: C/|B| computed = (2/9) c e^6/|B| lands ~0.69 (central), the
      residual band over c in [0.75,1.20] brackets BOTH targets, and the
      calculation CANNOT discriminate 0.63622 from 2/pi (split 4e-4) ->
      alpha_eff* does NOT cancel; C/|B| is a computed nonperturbative number
      whose residual is now the single O(1) quartic c (the F199 verdict,
      quantified).

Real arithmetic + numpy only (no chiral transforms). ~3 s.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.particles import eg_sextic as eg   # noqa: E402

RESULTS = {}
PASS = {}

SELF_DUAL = eg.SELF_DUAL       # 0.636224
TWO_OVER_PI = eg.TWO_OVER_PI   # 0.636620

# one end-to-end run, reused by all checks
REP = eg.report(L_sea=24, L_gap=24)
SEA = REP["sea"]
AE = REP["alpha_eff"]
ROWS = REP["rows"]
SUM = REP["summary"]


def test_G1_full_bz_B():
    assert SEA["B"] < 0                                  # hierarchical side (F95 D6)
    ratio = SUM["B_full_over_leading"]
    assert 1.4 < ratio < 2.2                             # higher-order sea at sat.
    RESULTS["G1_fullBZ_B"] = {
        "B": SEA["B"], "B_abs": SEA["B_abs"],
        "B_leadingform": SEA["B_leadingform"],
        "full_over_leading": ratio, "ybar_sat": SEA["ybar"],
        "statement": "full-BZ sea cubic at saturation; B<0; ~1.8x leading form"}
    PASS["G1"] = True


def test_G2_sea_sextic_wrong_sign():
    assert SEA["C6_sea"] < 0                             # anti-brake (F118 B1)
    RESULTS["G2_sea_sextic_sign"] = {
        "C6_sea": SEA["C6_sea"], "sign": SEA["C_sea_sign"],
        "statement": "sea's own sextic is NEGATIVE -> C is the INDUCED clock "
                     "self-coupling, not the sea loop (reproduces F118 B1)"}
    PASS["G2"] = True


def test_G3_alpha_eff_end_to_end():
    band = AE["alpha_eff_star_band"]
    mean = AE["alpha_eff_star_mean"]
    assert 0.37 < band[0] < 0.39 and 0.40 < band[1] < 0.42   # F152/F154
    assert 0.38 < mean < 0.40
    RESULTS["G3_alpha_eff_star"] = {
        "band_mD_mV": band, "mean": mean,
        "statement": "alpha_eff* recomputed end-to-end from the nonlinear gap "
                     "M(0)=1.5 solve; reproduces F152/F154 [0.376,0.411]"}
    PASS["G3"] = True


def test_G4_lambda6_per_order_fierz():
    # lambda_6 = (2/9) c ; with F118 c=1.10 -> 0.2444 vs F118 fit 0.243
    lam6 = eg.induced_lambda6(eg.C_QUARTIC_F118)["lambda6"]
    miss = abs(lam6 - 0.243) / 0.243
    assert abs(lam6 - (2.0 / 9.0) * 1.10) < 1e-9
    assert miss <= 0.01                                  # <=1% vs independent fit
    RESULTS["G4_lambda6_per_order"] = {
        "relation": "lambda_6 = (2/9) * c_quartic",
        "lambda6_computed": lam6, "lambda6_F118_independent_fit": 0.243,
        "fractional_miss": miss,
        "sextic_over_quartic_F118": 0.243 / 1.10, "fierz_2_9": 2.0 / 9.0,
        "statement": "sextic/quartic ratio of the E_g composite = Fierz 2/9 "
                     "(F145); matches F118's independent (lambda6,c) to <=1%"}
    PASS["G4"] = True


def test_G5_assembly_and_discrimination():
    central = ROWS["C_over_B_central"]
    band = ROWS["C_over_B_band_over_quartic_0.75_1.20"]
    # central lands in the right neighbourhood (0.6-0.75), residual band brackets target
    assert 0.55 < central < 0.80
    assert band[0] < SELF_DUAL < band[1]
    assert band[0] < TWO_OVER_PI < band[1]
    # the calculation CANNOT discriminate self-dual from 2/pi (residual >> split)
    assert not ROWS["discriminates_self_dual_vs_2pi"]
    # alpha does not cancel (B is O(alpha^0), C is O(alpha^>=1))
    assert SUM["alpha_does_not_cancel"] is True
    RESULTS["G5_assembly"] = {
        "C_over_B_central": central,
        "C_over_B_residual_band": band,
        "self_dual": SELF_DUAL, "two_over_pi": TWO_OVER_PI,
        "split": SUM["split_self_dual_2pi"],
        "quartic_needed_for_self_dual": SUM["quartic_needed_for_self_dual"],
        "e6_over_Babs": SUM["e6_over_Babs"],
        "discriminates": ROWS["discriminates_self_dual_vs_2pi"],
        "band_brackets_both": ROWS["band_brackets_both_targets"],
        "statement": "C/|B| = (2/9) c e^6/|B| computed ~0.69 central; residual "
                     "band brackets both targets; cannot discriminate 0.63622 vs "
                     "2/pi -> computed nonperturbative number, residual = the one "
                     "O(1) quartic c (F199 verdict, quantified)"}
    PASS["G5"] = True


def test_write_results():
    for t in (test_G1_full_bz_B, test_G2_sea_sextic_wrong_sign,
              test_G3_alpha_eff_end_to_end, test_G4_lambda6_per_order_fierz,
              test_G5_assembly_and_discrimination):
        t()
    RESULTS["summary"] = {
        "what": "end-to-end induced-coupling computation of C/|B|",
        "B_abs_fullBZ": SEA["B_abs"], "e6_saturation": SEA["e6"],
        "alpha_eff_star_mean": AE["alpha_eff_star_mean"],
        "lambda6_per_order": "(2/9) c_quartic",
        "C_over_B_central": ROWS["C_over_B_central"],
        "self_dual_target": SELF_DUAL, "two_over_pi": TWO_OVER_PI,
        "verdict": "COMPUTED number ~0.69(central); residual = single O(1) "
                   "quartic c; cannot discriminate self-dual vs 2/pi; "
                   "alpha_eff* does NOT cancel -> confirms F199 terminus",
        "checks": {k: ("PASS" if PASS.get(k) else "FAIL")
                   for k in ["G1", "G2", "G3", "G4", "G5"]},
        "overall": "5/5 PASS" if all(PASS.get(k) for k in
                   ["G1", "G2", "G3", "G4", "G5"]) else "FAIL"}
    out = os.path.abspath(os.path.join(HERE, "..", "..", "test-results",
                                       "F200_eg_sextic_coupling.json"))
    with open(out, "w") as f:
        json.dump(RESULTS, f, indent=2, default=float)
    assert RESULTS["summary"]["overall"] == "5/5 PASS"


if __name__ == "__main__":
    test_write_results()
    print(json.dumps(RESULTS["summary"], indent=2, default=float))
