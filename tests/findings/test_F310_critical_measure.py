"""F310 — K3/G2: gamma is a block-spin eigenvalue, and the model needs no dual.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.cosmology_critical_measure.check_critical_measure`
(record `F310-critical-measure`, tier gate), so this file deliberately defines
no `test_*` functions -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts.

    casim test --id F310-critical-measure
    casim test --id F310-critical-measure --param protected_stress_tensor=False   # red
    casim test --id F310-critical-measure --param integer_spectrum_control=True   # red

This takes the in-repo step named in `docs/status/open-derivations.md` row G2:
*decide whether the model claims a 3D dual at all.*  The answer is no, and the
reason it does not need one is the whole finding.

The legs that matter for reading the result:

  C0     The question, answered.  Holographic cosmology reaches for a 3D QFT by
         DUALITY.  This model's t=0 state on a rigid 3D lattice (F284) IS a
         measure on 3D field configurations, and F285's Poisson relation makes
         the primordial spectrum literally its energy-energy correlator.  There
         is no dictionary, which is why F296 L5's r exclusion -- computed from
         HC's field-content formula, an artifact OF the dictionary -- does not
         transfer.

  C1     The identity that does the work: n_s = 3 - 2y and therefore
         gamma == y - 1, with no approximation.  The anomalous dimension the
         tilt needs IS the anomalous part of the model's own block-spin
         relevant eigenvalue.  That is the operator identification G2 asked
         for, and F296 had to go outside the model to get.

  C2     A correction to F285 D1 row 2, exact and in F285's favour.  Its
         parenthetical "or even a critical Gaussian field squared" gives k^0 is
         wrong -- F285's own hypothesis is "integrable P_phi", and the critical
         case is not integrable.  Done properly the convolution is pi^3/k, so
         n_s = -1, which is FURTHER from 0.965 than 0 is.  The gapped sub-case
         (C2b) is untouched and still gives white noise.

  C3/C4  Why every earlier route failed, stated as one sentence: an anomalous
         dimension is a NON-INTEGER RG exponent, and every exponent F130
         measured is an integer -- b^0, b^+1, b^-n.  F130 says why without
         meaning to (lambda_n = b^-n is "a round-off-floor identity,
         independent of fit"), because a linear block average on free fields is
         a Gaussian calculation and Gaussian calculations have no anomalous
         dimensions.  Run F130's own relevant eigenvalue y=1 through C1 and the
         model predicts Harrison-Zel'dovich, excluded at 9.4-9.9 sigma on the
         two 2025 datasets.

  C6     The prediction that separates this from the dual reading, and the only
         zero-parameter number here.  In ANY CFT the stress tensor's dimension
         is protected by its own conservation, Delta_T = d exactly, while the
         energy operator's is not.  Hence n_t = 2 EXACTLY and, 58.26 decades
         below the BZ edge, log10 r(k_*) ~ -118.  F296's naive dual gave
         r = 0.32-0.97 against BK18's 0.034, excluded by 9.5-28.5x.

Three things this file will NOT assert, each deliberate:

  * **that the initial condition is derived.**  It is not.  F282/F284/F285 are
    untouched: P(k) is still free.  What narrows is the SHAPE of the freedom --
    a free function becomes a choice of universality class, one discrete label
    that then fixes n_s, n_t, r and dn_s/dlnk with nothing further.
  * **that the t=0 measure is critical.**  That is inferred from the observed
    power law, not proved, and it is the finding's largest residual.
  * **that the 1/N reading is a derivation.**  C8 asserts the opposite.  The
    data wants N ~ 63-81 and no count the model owns lands there; C8's
    `C8-no-hit` leg deliberately goes RED if one ever does, so that a
    coincidence has to be read by a human before it can be claimed.

Run standalone:  python3 tests/findings/test_F310_critical_measure.py
"""

from __future__ import annotations

import json

from casim.engine.interactions.cosmology_critical_measure import (
    check_critical_measure,
)


def main() -> dict:
    res = check_critical_measure()
    print(json.dumps(res["checks"], indent=2, sort_keys=False))
    print(f"\n{sum(res['checks'].values())}/{res['n_checks']} PASS")

    # This file carries its own failure mode rather than delegating all of it to
    # the entry, so it is in neither delta of `audit_tests --ratchet`.  The five
    # asserts below are the finding's headline statements, not a restatement of
    # `all_pass`.
    assert res["all_pass"], (
        f"only {sum(res['checks'].values())}/{res['n_checks']} legs passed")

    # the identity that IS the operator identification
    assert res["C1_dimension_relation"][
        "gamma_is_the_anomalous_part_of_the_eigenvalue"], \
        "C1: gamma == y - 1 is the whole finding; it must hold identically"

    # the F285 correction, and its direction
    assert res["C2_critical_gaussian"]["n_s"] == -1, \
        "C2: a critical Gaussian squared gives pi^3/k, so n_s = -1, not k^0"

    # no anomalous dimension anywhere in the measured spectrum
    assert res["C3_rg_spectrum"]["all_exponents_integer"] and not \
        res["C3_rg_spectrum"]["anomalous_dimensions_present"], \
        "C3: F130's measured RG exponents must all be integers"

    # the zero-parameter prediction, and that it repairs F296 L5
    assert res["C6_tensor"]["n_t_is_two_exactly"] and \
        res["C6_tensor"]["identity_reading_repairs_F296_L5"], \
        "C6: n_t = 2 exactly, and r at the pivot must clear BK18 on every dataset"

    # the discipline guard: C8 is a target and must keep saying so
    assert not res["C8_large_n_target"]["is_a_derivation"], \
        "C8: the 1/N reading is a target and must not be presented as derived"

    c1 = res["C1_dimension_relation"]
    c4 = res["C4_model_rg_predicts_hz"]
    c5 = res["C5_required_eigenvalue"]
    c6 = res["C6_tensor"]
    print(f"\nC1  n_s = {c1['n_s_of_y']},  gamma = {c1['gamma_of_y']}  (identity)")
    print(f"C2  P_rho = {res['C2_critical_gaussian']['P_rho']}  =>  n_s = "
          f"{res['C2_critical_gaussian']['n_s']}  (F285 row 2 said 0)")
    print(f"C4  F130's y = {c4['lambda_sigma_exponent_measured_by_F130']} "
          f"=> n_s = {c4['n_s_predicted']} exactly; excluded at "
          + ", ".join(f"{k} {v['exclusion_sigma']:.2f}s"
                      for k, v in c4["vs_data"].items()))
    print("C5  required y = "
          + ", ".join(f"{k} {v['y_required']:.6f}"
                      for k, v in c5["per_dataset"].items()))
    print(f"C6  n_t = {c6['n_t']} exactly => log10 r(k_*) = "
          + ", ".join(f"{k} {v['log10_r_at_pivot']:.2f}"
                      for k, v in c6["per_dataset"].items())
          + f"  (BK18 r < {c6['BK18_bound']})")
    return res


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    result = main()
    out = results_path("F310_critical_measure.json")
    with open(out, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote", out)
