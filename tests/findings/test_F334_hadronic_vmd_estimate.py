#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F334_hadronic_vmd_estimate.py
===================================

F334 — A model-internal (non-imported) narrow-resonance VMD estimate of the
hadronic piece of Delta alpha(M_Z): rho + omega, from the model's own KSRF
g_rhopipi (F103/F240) and the quark-charge photon-coupling weighting (F41/F42),
and its effect on rubric row B6/B9's EW-leg residual.

WHAT THIS TARGETS
------------------
Rubric row B6 (Weinberg angle, with scale), shared open target with B9 and G3
(completeness-2026-08-20-prompts.md; F322 SS7): the hadronic vacuum polarisation
piece of Delta alpha(M_Z) is declared out of scope everywhere in the model (G3),
and its absence doubles B9/B6's EW-leg residual on the model's own leptonic-only
alpha (+0.222% -> +0.450%, the missing 3.795 in 1/alpha_MSbar). This finding
gives the model a FIRST non-imported number for a piece of that gap.

DERIVATION SUMMARY (full derivation in findings/F334-*.md)
------------------------------------------------------------
  Gamma(V->e+e-) = 4 pi alpha^2 m_V / (3 g_V^2)                [VMD width]
  Delta alpha_V(s) = 3 Gamma_ee/(alpha m_V) * s/(s-m_V^2)      [narrow resonance
                                                                 dispersion integral]
  => Delta alpha_V(M_Z^2) ~= 4 pi alpha / g_V^2   (s >> m_V^2, m_V cancels)

  g_rho,EM = g_rhopipi (model KSRF output, universality posit -- F240's SAME
             posit, applied here to the photon instead of the nucleon)
  g_omega,EM = 3 g_rho,EM (from quark charges Q_u=2/3, Q_d=-1/3, NOT F128/F240's
             baryon coherence -- independently the same number, V2 below)

HONEST SCOPE: two narrow resonances only (no phi, no continuum, no charm/
bottom); the real rho is broad (Gamma/m~19%) so the narrow-width formula is a
KNOWN underestimate (duality violation) -- V5 measures this directly against
the PDG rho0->e+e- width rather than asserting it. This is NOT a replacement
for the data-driven Delta alpha_had^(5)(M_Z) (DHMZ2020); it is the model's
first quantitative, non-imported handle on a piece of it.

Run:  python3 tests/findings/test_F334_hadronic_vmd_estimate.py
Writes test-results/F334_hadronic_vmd_estimate.json
"""

import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
from casim.engine.interactions import running_alpha_lattice_bound as ralb  # noqa: E402

results = {"finding": "F334",
           "title": "Model-internal rho+omega VMD estimate of the hadronic "
                     "Delta alpha(M_Z) piece, and its effect on B6/B9's EW leg",
           "checks": {}, "derived": {}, "notes": []}
PASS = True


def record(name, ok, what, extra=None):
    global PASS
    results["checks"][name] = {"status": "PASS" if ok else "FAIL", "what": what}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:4s} {what}")
    if extra:
        for k, v in extra.items():
            print(f"         {k} = {v}")


print("=" * 80)
print("F334 — rho+omega VMD hadronic Delta alpha(M_Z) estimate (model-internal)")
print("=" * 80)

out = ralb.check_f334_hadronic_vmd()
for cid, c in out["checks"].items():
    record(cid, c["ok"], c["what"],
           extra={k: v for k, v in c.items() if k not in ("ok", "what")})

results["derived"] = {
    "photon_charge_weights": out["photon_charge_weights"],
    "hadronic_vmd": out["hadronic_vmd"],
    "ew_leg_with_hadronic_vmd": out["ew_leg_with_hadronic_vmd"],
}

# ---------------------------------------------------------------------------
# D9/H2 controls: verify each declared perturbation reddens ONLY its named leg.
# ---------------------------------------------------------------------------
print("\ncontrols (D9/H2) — verify red-and-only-there")

ctrl1 = ralb.check_f334_hadronic_vmd(charge_weight_control=1.0)
red1 = [k for k, v in ctrl1["checks"].items() if not v["ok"]]
record("control-charge-weight", red1 == ["V2"],
       "charge_weight_control=1.0 (drops the exact x3 isoscalar/isovector "
       "ratio) reddens V2 and ONLY V2",
       extra={"reddened": red1})

ctrl2 = ralb.check_f334_hadronic_vmd(dhmz_reference_control=0.001)
red2 = [k for k, v in ctrl2["checks"].items() if not v["ok"]]
record("control-dhmz-reference", red2 == ["V4"],
       "dhmz_reference_control=0.001 (a wildly wrong external anchor) "
       "reddens V4 and ONLY V4",
       extra={"reddened": red2})

results["all_pass"] = PASS
results["n_pass"] = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["n_total"] = len(results["checks"])

print("=" * 80)
print(f"{'ALL PASS' if PASS else 'SOME FAILED'}: {results['n_pass']}/{results['n_total']}")
print("=" * 80)

out_dir = os.path.join(HERE, "..", "..", "test-results")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "F334_hadronic_vmd_estimate.json")
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2, default=str)
print("wrote", out_path)

assert PASS, f"F334: {results['n_pass']}/{results['n_total']} checks passed -- see {out_path}"
