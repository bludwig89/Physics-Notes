# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_horizon_entropy.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/horizon_entropy.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_horizon_entropy.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_horizon_entropy.py  --  Lattice microstates & the Bekenstein-Hawking area law
================================================================================

Scenario S7 (speculative).  With a true horizon restored (F183), the model owes
a microscopic account of black-hole entropy.  This module sets up the horizon
as a tiling of F107 canonical cells and asks what per-cell entropy reproduces
S = A/(4 l_P^2) (k_B = 1).  The area law S ~ A is automatic from the tiling;
the coefficient 1/4 then *fixes* the required per-cell entropy in closed form.

F107 cell:  a = sqrt(8 pi) 3^{1/4} l_P  =>  a^2 = 8 pi sqrt3 l_P^2.
N_cells on the horizon = A / a^2.  Requiring N_cells * s_cell = A/(4 l_P^2):

    s_cell = a^2 / (4 l_P^2) = 8 pi sqrt3 / 4 = 2 pi sqrt3 nats  (≈ 10.88).

So Bekenstein-Hawking is reproduced iff each horizon cell carries 2 pi sqrt3
nats (~e^{10.9} ≈ 5.4e4 microstates).  This is a consistency relation tying the
F107 cell to S = A/4; deriving s_cell = 2 pi sqrt3 from the lattice degrees of
freedom is the open step.

Self-contained: numpy only.  Date: 2026-06-30 (F190).
"""

from __future__ import annotations

import numpy as np
from casim.constants import (
    G_CODATA as _G_CODATA,
    a_over_ellP as _a_over_ellP,
    c_SI as _c_SI,
    ell_P_m as _ell_P_m,
    hbar_SI as _hbar_SI,
)

G = _G_CODATA; C = _c_SI; HBAR = _hbar_SI
MSUN = 1.98892e30; KB = 1.380649e-23
ELLP = _ell_P_m
A_CELL = _a_over_ellP * ELLP        # F107 canonical cell
ELLP2 = ELLP ** 2


def horizon_area_m2(M_solar):
    r_h = 2.0 * G * (M_solar * MSUN) / C ** 2
    return 4.0 * np.pi * r_h ** 2


def bekenstein_hawking_entropy(M_solar):
    """S = A / (4 l_P^2)  (dimensionless, k_B = 1)."""
    return horizon_area_m2(M_solar) / (4.0 * ELLP2)


def lattice_cell_count(M_solar):
    """Number of F107 cells tiling the horizon, N = A / a^2."""
    return horizon_area_m2(M_solar) / A_CELL ** 2


def required_entropy_per_cell():
    """Closed form: s_cell = a^2/(4 l_P^2) = 2 pi sqrt3 nats."""
    return A_CELL ** 2 / (4.0 * ELLP2)        # == 2 pi sqrt3


def summary(M_solar=1.0):
    S = bekenstein_hawking_entropy(M_solar)
    N = lattice_cell_count(M_solar)
    s_cell = S / N
    return {"M_solar": M_solar, "S_BH": S, "N_cells": N,
            "s_per_cell": s_cell, "s_per_cell_closed_form": 2 * np.pi * np.sqrt(3),
            "microstates_per_cell": float(np.exp(s_cell)),
            "area_m2": horizon_area_m2(M_solar)}


def area_law_check(M1=1.0, M2=2.0):
    """S ~ A ~ M^2: S(M2)/S(M1) should equal (M2/M1)^2 exactly."""
    return {"ratio_S": bekenstein_hawking_entropy(M2) / bekenstein_hawking_entropy(M1),
            "ratio_M2_expected": (M2 / M1) ** 2}
