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

G = 6.67430e-11; C = 2.99792458e8; HBAR = 1.054571817e-34
MSUN = 1.98892e30; KB = 1.380649e-23
ELLP = 1.616255e-35
A_CELL = np.sqrt(8 * np.pi) * 3 ** 0.25 * ELLP        # F107 canonical cell
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
