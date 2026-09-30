#!/usr/bin/env python3
"""F402 runner — emit the Ji-type nucleon-mass-decomposition result artifact.

Writes `test-results/F402_baryon_mass_decomposition.json`. Machine-precision
identities (Hellmann-Feynman, dilatation, virial) plus quantitative comparisons.

    PYTHONPATH=src python3 tests/runners/run_f402_baryon_mass_decomposition.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Put src/ and tests/findings/ on sys.path and return what this runner needs.

    Inside a call, not at module scope — see F291's own runner for why.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "src"),
              os.path.join(here, "..", "findings")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from casim.engine.particles._results_path import results_path
    from test_F402_baryon_mass_decomposition import check_all
    return results_path, check_all


def _assert_verdict(out: dict) -> None:
    assert out["A1_njl_dilatation"]["worst_independent_fd_residual"] < 1e-6
    assert out["B3_nr_mass_term_unphysical"]["baseline_H_m_frac"] < 0.0
    assert out["C2_model_gluon_share_short"]["chiqcd"]["pull"] < -2.0
    assert out["C2_model_gluon_share_short"]["etmc"]["pull"] < -1.5
    assert int(out["n_checks"]) == 7, out["n_checks"]


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()
    _assert_verdict(out)
    dest = results_path("F402_baryon_mass_decomposition.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True, default=str)
    print(f"wrote {dest}")
    print(f"  checks          : {out['n_checks']}")
    print(f"  sigma_N (MeV)   : {out['A2_sigma_term']['sigma_N_MeV']:.2f}")
    c2 = out['C2_model_gluon_share_short']
    print(f"  x_g model       : {c2['x_g_model_hi']:.3f}  (pull {c2['chiqcd']['pull']:.2f} "
          f"chiQCD, {c2['etmc']['pull']:.2f} ETMC)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
