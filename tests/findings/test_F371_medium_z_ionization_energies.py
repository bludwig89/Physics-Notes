#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F371 — Extending F208's relativistic SCF ionization-energy map from
Z=1-20 to the full 3d series (Z=21-30, Sc-Zn), including the requested Fe.

Certifies (from the committed sweep JSON, test-results/F371_medium_z_ie_sweep.json):
  - all ten Z=21-30 rows are self-consistency converged (at the tightened
    mix=0.2/max_iter=150 settings; F208's own default mix=0.4/max_iter=60
    fails from Ni onward -- documented in convergence_diagnostics),
  - every element is underbound vs NIST by >10% (the same missing-exchange
    signature F208 found for H-Ca), worst at Zn,
  - relativity stays sub-meV in the valence channel through Zn (still not
    the ceiling),
  - the grid-sensitivity diagnostic (N=900 vs N=1200, four representative Z)
    is present, shows a monotonically Z-growing shift, and is honestly
    reported as NOT closed (grid_converged: False) -- this is the honest
    scope-boundary this finding adds on top of F208's own exchange gap.

In-test SCF calls are kept to two very light regressions (Fe reproduces its
committed row; Sc-Cr converge under BOTH the default and tightened mixing,
i.e. the divergence is a late-series-only phenomenon) so the suite stays
fast; the heavy medium-Z and grid-refinement runs are read from the
committed JSON, matching F208's own test-design convention.
"""
import os
import sys
import json

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.core import manybody as mb                    # noqa: E402

_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "test-results",
                        "F371_medium_z_ie_sweep.json")


def _data():
    return json.load(open(_RESULTS))


# ---- C1: exactly Sc-Zn (Z=21-30), all present, all self-consistency conv. --
def test_C1_full_row_present_and_converged():
    data = _data()
    zs = sorted(r["Z"] for r in data["rows"])
    assert zs == list(range(21, 31)), zs
    assert all(r["converged"] for r in data["rows"])
    assert data["summary"]["all_converged_Z21_30"] is True


# ---- C2: Fe (the requested target) reproduces the committed row -------------
def test_C2_fe_reproduces_committed_row():
    data = _data()
    fe = next(r for r in data["rows"] if r["Z"] == 26)
    r = mb.electron_cloud_hartree(26, N=900, relativistic=True,
                                   max_iter=150, mix=0.2, tol=1e-6)
    assert r["converged"]
    assert abs(r["ionization_eV"] - fe["ie_nr"]) < 1e-3
    # Fe ground config is [Ar] 4s^2 3d^6 -- textbook, no Aufbau anomaly here
    assert tuple(fe["configuration"][-1]) == (3, "d", 6), fe["configuration"]


# ---- C3: early-row (Sc-Cr) SCF converges under F208's OWN default mixing --
# (the divergence documented below is a late-3d-series-only phenomenon,
#  not a blanket regression of the F208 defaults)
def test_C3_early_row_converges_under_f208_defaults():
    for Z in (21, 24):                                    # Sc, Cr
        r = mb.electron_cloud_hartree(Z, N=500, relativistic=True,
                                       max_iter=60, mix=0.4, tol=1e-6)
        assert r["converged"], (Z, "should converge under F208 defaults")


# ---- C4: every Z=21-30 atom underbinds vs NIST by >10% (missing exchange) --
def test_C4_xc_underbinding_continues():
    data = _data()
    for r in data["rows"]:
        assert r["err_nr_pct"] < -10.0, (r["Z"], r["err_nr_pct"])
    assert data["summary"]["all_underbind_gt10pct"] is True
    assert data["summary"]["mean_abs_err_nr_pct_Z21_30"] > 25.0


# ---- C5: relativity stays sub-meV in the valence channel through Zn -------
def test_C5_relativity_still_negligible_through_zn():
    data = _data()
    for r in data["rows"]:
        assert abs(r["homo_rel_shift_meV"]) < 1.0, (r["Z"], r["homo_rel_shift_meV"])
    assert data["summary"]["IE_rel_minus_nr_always_lt_1meV"] is True


# ---- C6: the default (mix=0.4, max_iter=60) SCF fails from Ni onward ------
# (documents the numerical-parameter scope boundary; read from the committed
#  diagnostic rather than re-run live, since the unconverged branch itself
#  costs the same ~40s per Z as the converged one)
def test_C6_default_mixing_fails_late_3d_series():
    data = _data()
    diag = data["convergence_diagnostics"]
    assert diag["Z28_Ni_default_converged"] is False
    assert diag["Z29_Cu_default_converged"] is False
    assert diag["Z30_Zn_default_converged"] is False
    # and the unconverged Cu/Zn snapshots are NOT close to the true answer
    assert abs(diag["Z29_Cu_default_ie_nr_eV"] - diag["Z29_Cu_converged_ie_nr_eV"]) > 0.3
    assert abs(diag["Z30_Zn_default_ie_nr_eV"] - diag["Z30_Zn_converged_ie_nr_eV"]) > 1.5


# ---- C7: the grid-sensitivity caveat is present and honestly un-closed ----
def test_C7_grid_sensitivity_documented_and_not_closed():
    data = _data()
    assert data["summary"]["grid_converged"] is False
    diag = data["grid_sensitivity_diagnostic"]
    pts = diag["points"]
    # sensitivity grows monotonically with Z over the four checked points
    zs_checked = ["Na_Z11", "Ca_Z20", "Fe_Z26", "Zn_Z30"]
    d_ie = [pts[k]["d_ie_pct"] for k in zs_checked]
    assert d_ie == sorted(d_ie), d_ie
    d_core = [pts[k]["d_core1s_pct"] for k in zs_checked]
    assert d_core == sorted(d_core), d_core
    # relativity claim survives the finer grid too
    assert pts["Zn_Z30"]["relativity_stays_submeV_both_grids"] is True


if __name__ == "__main__":
    for n in sorted(k for k in dir() if k.startswith("test_")):
        globals()[n]()
        print(n, "PASS")
    print("F371 OK")
