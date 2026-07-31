# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_qcd_scale_ratio.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/running_scale_ratio.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_qcd_scale_ratio.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_qcd_scale_ratio.py
=====================

The F123 open debt: derive the ratio of the model's TWO QCD calibrations —
the confinement scale sqrt(sigma) (P1: F70/F86/F88/F94/F101) and the chiral-
symmetry-breaking scale f_pi (F77/F103 NJL) — from first principles, i.e.
predict the pure number sqrt(sigma)/f_pi (empirically ~4.56).

THE STRATEGY
------------
Both scales descend from the SAME BCC lattice rule, whose gauge coupling is
NOT free (F115: the rotor stiffness locks g_s^2 chi = 1/4) and whose NJL cutoff
is NOT free (F116: Lambda is the Brillouin-zone edge).  So sqrt(sigma)/f_pi is
a pure lattice number, and we factor it as

    sqrt(sigma)/f_pi  =  (Lambda / f_pi)  x  (sqrt(sigma) / Lambda)
                          \___chiral___/      \__confinement__/

  * CHIRAL factor  Lambda/f_pi : an EXACT NJL output (Pagels-Stokar loop), no
    free knob beyond the dimensionless {G Lam^2, m0/Lam}.  = 7.04.
  * CONFINEMENT factor sqrt(sigma)/Lambda : sqrt(sigma) in lattice units
    (units of 1/a) over the BZ-edge cutoff Lambda (also ~ 1/a).  Two model
    sources for sigma_lat:
       - CONDENSED VACUUM (F86/F88): sigma = 2 pi v^2, v = m_D/e = 0.713
         (a measured property of the compact gauge vacuum) -> sigma_lat = 3.19.
       - BARE ROTOR (F100/F101/F115): sigma_lat = (1/4)<1/Omega>_BZ = 0.2015,
         the rule's locked weak-coupling value.
    and two BZ-edge <-> 3-momentum-cutoff conventions:
       - 'axis'   : Lambda = pi/a            (per-axis zone edge)
       - 'sphere' : Lambda = (6 pi^2)^{1/3}/a (sphere of equal BZ volume)

RESULT (honest)
---------------
The CHIRAL factor Lambda/f_pi = 7.04 is exact.  The CONDENSED-vacuum route gives
sqrt(sigma)/f_pi ~ 3.2-4.0 (within ~15-30% of the empirical 4.56) — the model
reproduces the ratio to O(1) and reduces the open number to ONE confinement
ratio sqrt(sigma)/Lambda whose residual is the BZ-edge<->cutoff convention and
the Abelian-vs-Casimir centre caveat (F99-F101).  The BARE-ROTOR route gives
~1.0-1.4: the rule's weak-coupling rotor sits a factor ~4 in sqrt(sigma) BELOW
the confined vacuum — and that factor IS the QCD scale-setting (the IR
confinement scale separating from the UV lattice cutoff), exactly the strong-
coupling regime F70/F101 say confinement lives in.  Pinning the single self-
consistent lattice spacing where BOTH chi-SB and confinement take physical
values (dimensional transmutation) is the residual gap.

All arithmetic REAL.  numpy only.  Imports the validated F77/F103 solver.
"""

from __future__ import annotations

import numpy as np
import ca_meson as MES
from casim.constants import (  # noqa: E501
    Lambda_NJL_GeV,
    G_Lambda2_NJL,
    m0_current_quark_MeV,
    sqrt_sigma_GeV,
)

# Canonical NJL point (F77/F103).
LAM, GLAM2, M0 = Lambda_NJL_GeV, G_Lambda2_NJL, m0_current_quark_MeV / 1e3   # GeV
N_C = 3

# Confinement-sector lattice inputs (from the cited findings).
V_F88 = 0.713          # colour-magnetic condensate VEV v = m_D/e (F88, lattice)
SIGMA_ROTOR = 0.2015   # bare rotor sigma_lat = (1/4)<1/Omega>_BZ (F100/F101, 2D)

# Empirical targets.
SQRT_SIGMA_PHYS = sqrt_sigma_GeV   # GeV (lattice/Sommer-scale string tension)
F_PI_PHYS = 0.09207       # GeV


# ===========================================================================
#  Chiral factor — exact NJL ratios (Pagels-Stokar).
# ===========================================================================
def njl_chiral_ratios():
    G = GLAM2 / LAM ** 2
    M = MES.gap_solve(G, LAM, M0)
    fpi = MES.f_pi(M, LAM)
    K0 = MES.K0_closed(M, LAM)
    qq = MES.condensate_perflavour(M, LAM)      # negative
    return {
        "M_GeV": M,
        "f_pi_GeV": fpi,
        "M_over_Lam": M / LAM,
        "f_pi_over_M": fpi / M,
        "f_pi_over_Lam": fpi / LAM,
        "Lam_over_f_pi": LAM / fpi,
        "pagels_stokar_check": 2.0 * np.sqrt(N_C * K0),   # == f_pi/M
        "condensate_root_GeV": -(-qq) ** (1.0 / 3.0),
    }


# ===========================================================================
#  Confinement factor — sqrt(sigma)/Lambda in lattice units.
# ===========================================================================
def bz_cutoff_lattice(convention="axis"):
    """BZ-edge 3-momentum cutoff Lambda in lattice units (1/a)."""
    if convention == "axis":
        return np.pi                       # per-axis zone edge
    if convention == "sphere":
        return (6.0 * np.pi ** 2) ** (1.0 / 3.0)   # sphere of equal BZ volume
    raise ValueError(convention)


def sigma_lattice(route="condensate", casimir=False):
    """sqrt(sigma) in lattice units (1/a) from the chosen confinement source."""
    if route == "condensate":
        sig = 2.0 * np.pi * V_F88 ** 2     # F86 BPS, F88 v  -> 3.19
    elif route == "rotor":
        sig = SIGMA_ROTOR                  # F101 bare locked rotor -> 0.2015
    else:
        raise ValueError(route)
    if casimir:
        sig *= 2.0                         # Abelian sigma_2 = 2 sigma_1 caveat
    return np.sqrt(sig)


def sqrt_sigma_over_fpi(route="condensate", convention="axis", casimir=False):
    """The headline ratio via  (Lambda/f_pi) x (sqrt(sigma)/Lambda)."""
    chi = njl_chiral_ratios()
    Lam_over_fpi = chi["Lam_over_f_pi"]               # 7.04 (chiral, exact)
    sqrt_sig_lat = sigma_lattice(route, casimir)      # 1/a units
    Lam_lat = bz_cutoff_lattice(convention)           # 1/a units
    sqrt_sig_over_Lam = sqrt_sig_lat / Lam_lat        # confinement factor
    return Lam_over_fpi * sqrt_sig_over_Lam, {
        "Lam_over_f_pi": Lam_over_fpi,
        "sqrt_sigma_lat": sqrt_sig_lat,
        "Lam_lat": Lam_lat,
        "sqrt_sigma_over_Lam": sqrt_sig_over_Lam,
    }


def empirical_decomposition():
    chi = njl_chiral_ratios()
    return {
        "sqrt_sigma_over_f_pi": SQRT_SIGMA_PHYS / F_PI_PHYS,
        "sqrt_sigma_over_Lam": SQRT_SIGMA_PHYS / LAM,
        "sqrt_sigma_over_M": SQRT_SIGMA_PHYS / chi["M_GeV"],
        "Lam_over_f_pi": chi["Lam_over_f_pi"],
    }


def summary():
    chi = njl_chiral_ratios()
    emp = empirical_decomposition()
    out = {"njl": chi, "empirical": emp, "model": {}}
    for route in ("condensate", "rotor"):
        for conv in ("axis", "sphere"):
            val, detail = sqrt_sigma_over_fpi(route, conv)
            out["model"][f"{route}_{conv}"] = {"sqrt_sigma_over_f_pi": val, **detail}
    return out


if __name__ == "__main__":
    s = summary()
    chi, emp = s["njl"], s["empirical"]
    print("=== Deriving sqrt(sigma)/f_pi from the model ===\n")
    print("CHIRAL factor (exact NJL):")
    print(f"  f_pi/M = {chi['f_pi_over_M']:.4f}  (Pagels-Stokar {chi['pagels_stokar_check']:.4f})")
    print(f"  Lambda/f_pi = {chi['Lam_over_f_pi']:.3f}   M = {chi['M_GeV']*1e3:.1f} MeV\n")
    print(f"EMPIRICAL: sqrt(sigma)/f_pi = {emp['sqrt_sigma_over_f_pi']:.3f}, "
          f"sqrt(sigma)/Lambda = {emp['sqrt_sigma_over_Lam']:.3f}\n")
    print("MODEL sqrt(sigma)/f_pi by route x BZ convention:")
    for k, v in s["model"].items():
        print(f"  {k:18s}: {v['sqrt_sigma_over_f_pi']:.3f}   "
              f"(sqrt(sigma)/Lam = {v['sqrt_sigma_over_Lam']:.3f})")
