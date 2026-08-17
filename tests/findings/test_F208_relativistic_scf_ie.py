#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F208 — relativistic (F125 Dirac–Coulomb) ionization energies in the
multi-electron SCF + the light-element accuracy map.

Certifies the relativistic correction wired into ``ca_manybody`` and the
quantified conclusion: the light-element IE error is exchange-correlation
(Hartree + Koopmans), NOT relativity.  Heavy per-Z SCF work is read from the
committed sweep JSON (``test-results/F208_relativistic_ie_sweep.json``); the
in-test SCF calls are kept light (N=500, a few atoms) so the suite stays fast.
"""
import os
import sys
import json

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

import numpy as np                                       # noqa: E402
from casim.engine.core import manybody as mb                                  # noqa: E402

_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "test-results",
                        "F208_relativistic_ie_sweep.json")


# ---- C1: the scalar shift reproduces the F125 hydrogen 1s value -------------
def test_C1_hydrogen_1s_shift_identity():
    # H 1s: eps = -0.5 Ha, Z_eff = 1, C(1,0)=1 -> ΔE = -α²/8 Ha = -0.181 meV
    a = mb.ALPHA
    d_Ha = mb._scalar_relativistic_shift_Ha(1, 0, -0.5, a)
    assert abs(d_Ha - (-(a ** 2) / 8.0)) < 1e-18, d_Ha
    d_eV = d_Ha * mb.M_E_MEV * 1e6 * a ** 2
    assert abs(d_eV * 1000 - (-0.181)) < 2e-3, d_eV * 1000   # meV


# ---- C2: the C(n,l) spin-average is right (l=0 special case) -----------------
def test_C2_spin_average_factor():
    # for a fixed Z_eff the l=0 factor must be C=n (only j=1/2), not n/(l+1/2)
    a = mb.ALPHA
    # build with a controlled eps so Z_eff=1 at n=2: eps=-Z^2/2n^2=-1/8
    s = mb._scalar_relativistic_shift_Ha(2, 0, -1.0 / 8.0, a)   # 2s, C=2
    expect = -(1.0 * a ** 2) / (2.0 * 16.0) * (2.0 - 0.75)
    assert abs(s - expect) < 1e-18, (s, expect)
    p = mb._scalar_relativistic_shift_Ha(2, 1, -1.0 / 8.0, a)   # 2p, C=n/(l+1/2)=2/1.5
    expect_p = -(1.0 * a ** 2) / (2.0 * 16.0) * (2.0 / 1.5 - 0.75)
    assert abs(p - expect_p) < 1e-18, (p, expect_p)


# ---- C3: hydrogen IE exact (one electron), both nr and rel ------------------
def test_C3_hydrogen_exact():
    r = mb.electron_cloud_hartree(1, N=700, relativistic=True)
    assert abs(r["ionization_eV"] - 13.598) < 0.05, r["ionization_eV"]
    assert abs(r["ionization_eV_rel"] - r["ionization_eV"]) < 1e-3   # ~0.18 meV


# ---- C4: non-relativistic path is unchanged (F157 regression) ---------------
def test_C4_nonrel_path_unchanged():
    r = mb.electron_cloud_hartree(2, N=700)                 # default relativistic=False
    assert "ionization_eV_rel" not in r                     # no extra keys
    assert abs(r["ionization_eV"] - 23.98) < 0.3, r["ionization_eV"]   # He F157


# ---- C5: relativity is negligible for light-atom valence IE -----------------
def test_C5_valence_rel_negligible():
    for Z in (3, 6, 10):                                    # Li, C, Ne
        r = mb.electron_cloud_hartree(Z, N=500, relativistic=True)
        shift_meV = 1000 * (r["ionization_eV_rel"] - r["ionization_eV"])
        assert abs(shift_meV) < 1.0, (Z, shift_meV)         # sub-meV


# ---- C6: the documented breakdown — XC underbinding from Li on --------------
def test_C6_xc_breakdown_from_lithium():
    data = json.load(open(_RESULTS))
    rows = {r["Z"]: r for r in data["rows"]}
    assert abs(rows[1]["err_nr_pct"]) < 0.5            # H exact
    assert abs(rows[2]["err_nr_pct"]) < 5.0            # He good
    # every many-electron atom underbinds by >10%, sign negative (missing exchange)
    for Z in range(3, 19):
        assert rows[Z]["err_nr_pct"] < -10.0, (Z, rows[Z]["err_nr_pct"])
    assert data["summary"]["mean_abs_err_nr_pct_Z2_20"] > 15.0


# ---- C7: relativity grows ~Z^4 in the core ---------------------------------
def test_C7_core_shift_Z4_growth():
    data = json.load(open(_RESULTS))
    rows = {r["Z"]: r for r in data["rows"]}
    ne = abs(rows[10]["core_1s_rel_shift_eV"])
    ar = abs(rows[18]["core_1s_rel_shift_eV"])
    assert ar > ne > 0
    slope = (np.log(ar) - np.log(ne)) / (np.log(18) - np.log(10))
    assert 2.8 < slope < 4.2, slope                    # ~Z^4 fine-structure law
    # and it stays a CORE effect: 1s shift >> valence IE shift at Ar
    assert abs(rows[18]["core_1s_rel_shift_eV"]) > 100 * abs(
        rows[18]["homo_rel_shift_meV"] / 1000.0)


if __name__ == "__main__":
    for n in sorted(k for k in dir() if k.startswith("test_")):
        globals()[n]()
        print(n, "PASS")
    print("F208 OK")
