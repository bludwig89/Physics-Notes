"""F320 — the absolute W and Z masses, and rho = 1 (completeness row B12).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_gauge_boson_masses.check_gauge_boson_masses`
(record `F320-gauge-boson-masses`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven records
from file collection so nothing runs twice under two contracts.

    casim test --id F320-gauge-boson-masses
    casim test --id F320-gauge-boson-masses --param equal_stiffness=false    # red
    casim test --id F320-gauge-boson-masses --param rank_two_breaking=true   # red
    casim test --id F320-gauge-boson-masses --param eliminate_u=false        # red

WHAT IS AND IS NOT CLAIMED.  This record does **not** derive the electroweak
scale.  v stays an anchor, ledger 17 stays FIT(N=1), and F119's finding that
the overall scale N has no O(1) mechanism is untouched.  What it establishes is
that CL016's scope line -- "m_W and m_Z in absolute terms are not predicted" --
was drawn one step too far in.  Given {alpha, G_F}, which are TWO inputs where
the Standard Model's electroweak sector takes THREE, the model's own on-shell
sin^2(theta_W) = 2/9 delivers both boson masses as outputs.

  B0a-c the 7:2 Wigner-Seitz / sublattice counting is RECOMPUTED, not trusted,
        and asserted equal to the registry sin2_thetaW_onshell.  c^2/s^2 = 7/2
        exactly, which is the coefficient Delta_rho carries inside Delta_r.
  B1a   det M^2 vanishes IDENTICALLY in the stiffness quantum u -- checked at
        five independent rationals -- because F41 absorbs exactly ONE
        Stueckelberg direction, so the breaking is rank one.
  B1b   the photon is therefore exactly massless, not massless to a tolerance.
  B1c   rho = 1 EXACTLY, for every u.  The model has no Higgs field and so
        cannot borrow the custodial-SU(2) argument; rank is its own reason.
  B1d   the massless eigenvector is (sqrt2, sqrt7)/3 at the BCC counts.
  B2a-b u is DETERMINED, not free.  F141 got only the ratio because u was an
        open normalisation; eliminating it against e = g sin(theta_W) gives
        g^2 = 18 pi alpha and g'^2 = 36 pi alpha / 7, both exact.
  B2c   hence the closed forms  m_W = (3v/2) sqrt(2 pi alpha)  and
        m_Z = (9v/2) sqrt(2 pi alpha/7), reproducing the matrix solve.
  B3a-c the tree numbers, 79.0836 and 89.6724 GeV, -1.60 % and -1.66 %.  That
        deficit is Delta_r and the SM's own tree relation carries it too.
  B4a   THE LOAD-BEARING LEG.  m_W(model)/m_W(obs) = sqrt(s2_obs/s2_model) for
        EVERY Delta_r in [0, 0.10] to 2.2e-16: the radiative correction is
        common to model and SM and cancels in the ratio.  So the absolute-mass
        residual is the ANGLE residual and nothing else, and the headline
        number does not depend on anybody's Delta_r.
  B4b-c +0.222 % on m_W, +0.158 % on m_Z, Delta_r-free.
  B4d   the one place Delta_r is NOT common -- the model's c^2/s^2 = 7/2 sits
        where the SM has 3.4830 -- is measured at -0.0095 % on m_W.
  B5a-c the absolute numbers as a BRACKET over Delta_r, m_W in [80.147,
        80.548] GeV, which CONTAINS the PDG 80.3692 at 55 % of its width.  The
        bracket's upper endpoint is CALIBRATED from the PDG masses, which is
        stated rather than hidden -- it is why B4a and not B5a is the headline.
  B6a-b the input count, which is the whole accounting claim: two, not three,
        and neither of them is a boson mass.

THE THREE CONTROLS REDDEN DISJOINT LEG SETS, and that is their purpose.
Breaking the counting kills the ratio block and leaves rho standing; forcing a
rank-two breaking kills rho and leaves the counting standing; refusing to
eliminate u kills the absolute block and leaves both.  Each of the three
results therefore rests on a different structural input, and the record
measures that rather than asserting it.
"""
import json
import os
import sys


def _bootstrap():
    """Import the module by path so this driver runs from a bare checkout too."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_gauge_boson_masses as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_gauge_boson_masses()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
        if c["note"]:
            print(f"          {c['note']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F320_gauge_boson_masses.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["n_pass"] == res["n_total"], (
        "F320 gate failed: " + json.dumps(
            [c for c in res["checks"] if not c["ok"]], default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
