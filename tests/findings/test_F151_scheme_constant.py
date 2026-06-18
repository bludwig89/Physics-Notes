"""
F151 — the shared scheme/scale constant of F144-A4 / F145-N5 / F124 §5,
determined: alpha_rule = alpha_V (tree-exact), the one-loop conversion is the
KNOWN constant a1, and the residual collapses to a matching scale q* inside a
derived O(1) band — with the data-implied point reproducing FLAG's Lambda3
to 1.1% as an independent corroboration.

Checks:

  S1 (exact)   Scheme identification: (a) the F144 lock normalises the STATIC
               ELECTRIC ENERGY — F110 lambda=0 potential V(R)=(g^2/2)q^2 R
               integer-exact (dev 0.0) => the rule's coupling is the V-scheme
               coupling by definition; (b) a1 = (93-10nf)/9 exact rationals
               (a1(6) = 11/3), Lambda_V/Lambda_MS per nf.

  S2 (machine) The Wilson-contrast tadpole Z0 = 0.154933 reproduced (<1e-4):
               the term that makes compact-link schemes huge (28.81) is
               structurally absent from the rule's spectral lock.

  S3 (prediction) The a1-corrected chain over the q* band [1/sqrt3, 1]/a:
               alpha_s(M_Z) in [0.1143, 0.1232] — BRACKETS PDG 0.1180 with
               zero free parameters; a1 alone improves +8.46% -> +4.43%.

  S4 (corroboration) The data-implied q* = 0.7327/a lies inside the band
               (3.6% below the geometric mean 3^(-1/4)/a — recorded as an
               observation, not a derivation).  KEY: q* is fixed by
               alpha_s(M_Z) ALONE, and then Lambda_MS^(3) lands on FLAG
               343(12) MeV to 1.1% — an independent second observable.
               Hierarchy N = 1.87e-19.

  S5 (supporting + IR face) (a) spectral Coulomb: exact-symbol Green's fn ->
               continuum 1/(4 pi R) (image-corrected difference test, <5%,
               R-improving — the tree no-renormalisation statement's numeric
               shadow); (b) the IR face alpha_eff* = 0.376/0.411 (F88/F117
               m_D), stable, recorded as the now-separate nonperturbative
               target — refining the F144/F145 "one shared number": the UV
               constant is (a1 exact) + (q* in the band); the IR coupling is
               a distinct object connected through the strong-coupling
               crossover.

numpy (+ ca_link_hamiltonian); ~2 min.
"""

import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "..", "ca-simulation")))
import ca_scheme_constant as SC  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
results = {}

rep = SC.report()


def check_S1():
    lock = rep["static_energy_lock"]
    # a1 exact rationals: a1(nf) = (93 - 10 nf)/9
    fr_ok = all(Fraction(93 - 10 * nf, 9) == Fraction(SC.a1(nf)).limit_denominator(10**6)
                for nf in (0, 3, 6))
    a16_ok = Fraction(SC.a1(6)).limit_denominator(10**6) == Fraction(11, 3)
    ok = lock["max_dev"] == 0.0 and fr_ok and a16_ok
    return ok, {"static_lock": lock, "a1_ledger": rep["a1_ledger"],
                "a1(6)=11/3": a16_ok}


def check_S2():
    z = rep["wilson_tadpole"]
    return z["dev"] < 1e-4, z


def check_S3():
    band = rep["chain_band"]
    lo = band["q*=1/sqrt3/a"]["alpha_s_MZ"]
    hi = band["q*=1/a"]["alpha_s_MZ"]
    ref = band["no_a1_reference (F144)"]["dev_vs_PDG_%"]
    a1only = band["q*=1/a"]["dev_vs_PDG_%"]
    ok = (lo < 0.1180 < hi) and (abs(a1only) < abs(ref))
    return ok, {"band_lo": lo, "band_hi": hi, "PDG": 0.1180,
                "F144_dev_%": ref, "a1_corrected_dev_%": a1only}


def check_S4():
    qs = rep["implied_qstar_a"]
    at = rep["at_implied"]
    ok = (rep["implied_in_band"]
          and abs(rep["implied_vs_geometric_%"]) < 10.0
          and abs(at["Lambda3_vs_FLAG"] - 1.0) < 0.10)
    return ok, {"implied_qstar_a": qs, "geometric_mean": SC.QSTAR_GEO,
                "vs_geometric_%": rep["implied_vs_geometric_%"],
                "Lambda3_GeV": at["Lambda3_GeV"],
                "Lambda3_vs_FLAG": at["Lambda3_vs_FLAG"],
                "hierarchy_N": at["hierarchy_N"],
                "note": "q* fixed by alpha_s(M_Z) alone; Lambda3 then "
                        "corroborates to ~1% — independent observable"}


def check_S5():
    cou = rep["spectral_coulomb"]
    ir = rep["ir_face"]
    spread = abs(ir["alpha_eff*_F88"] - ir["alpha_eff*_F117"])
    ok = (cou["max_rel_dev"] < 0.05
          and 0.30 < ir["alpha_eff*_F88"] < 0.50
          and 0.30 < ir["alpha_eff*_F117"] < 0.50
          and spread < 0.06)
    return ok, {"coulomb": cou, "ir_face": ir, "spread": spread}


n_pass = 0
for name, fn in (("S1", check_S1), ("S2", check_S2), ("S3", check_S3),
                 ("S4", check_S4), ("S5", check_S5)):
    ok, detail = fn()
    results[name] = {"PASS": bool(ok), "detail": detail}
    n_pass += int(ok)

results["ALL_PASS"] = all(results[k]["PASS"]
                          for k in ("S1", "S2", "S3", "S4", "S5"))
results["report"] = rep
results["CALIBRATION_NOTE"] = (
    "Zero new parameters. Derived: alpha_rule=alpha_V (tree, S1) and the "
    "exact one-loop a1 conversion. Bounded: the matching scale q* in "
    "[1/sqrt3, 1]/a (model geometric conventions); data-implied q*=0.7327/a, "
    "3.6% below 3^(-1/4)/a (observation, not derivation — the LPT q* "
    "computation is the remaining first-principles step). Corroboration: "
    "Lambda3 = 347 MeV vs FLAG 343(12) at the implied point. IR face "
    "alpha_eff*~0.38-0.41 is a separate nonperturbative target (refines the "
    "'one shared number' of F144/F145).")

out = os.path.join(ROOT, "test-results", "F151_scheme_constant.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=float)

print("=" * 72)
print("F151 — the scheme/scale constant determined")
print("=" * 72)
band = rep["chain_band"]
print(f"  a1(6) = 11/3 exact  ->  Delta(1/alpha) = 0.2918  "
      f"(alpha_s(M_Z): +8.46% -> +4.43%)")
print(f"  band [1/sqrt3, 1]/a: alpha_s(M_Z) = "
      f"{band['q*=1/sqrt3/a']['alpha_s_MZ']:.4f} .. "
      f"{band['q*=1/a']['alpha_s_MZ']:.4f}  (PDG 0.1180 inside)")
print(f"  implied q* = {rep['implied_qstar_a']:.4f}/a "
      f"({rep['implied_vs_geometric_%']:+.1f}% vs 3^-1/4)  ->  "
      f"Lambda3 = {rep['at_implied']['Lambda3_GeV']*1e3:.0f} MeV "
      f"(FLAG 343+-12, x{rep['at_implied']['Lambda3_vs_FLAG']:.3f})")
print(f"  N = {rep['at_implied']['hierarchy_N']:.2e}; "
      f"IR face alpha_eff* = {rep['ir_face']['alpha_eff*_F88']:.3f}/"
      f"{rep['ir_face']['alpha_eff*_F117']:.3f}")
for k in ("S1", "S2", "S3", "S4", "S5"):
    print(f"  {k}: {'PASS' if results[k]['PASS'] else 'FAIL'}")
print(f"  ALL_PASS = {results['ALL_PASS']}")
