"""Gravity sector — Newton's constant in lattice units and the F106 coefficient.

The best-behaved sector in the tree: single source, clean re-export, and
already asserted by tests/casim/test_gravity_element.py before P0 existed.

    from casim.constants import G_LATTICE
"""
from __future__ import annotations

import math

from . import Constant, Site, register

# ---------------------------------------------------------------------------
# G in lattice units — structural, not a knob.
# C2.1: resolved from the closed form c_lat^4/(8 pi) = 1/(72 pi), not a decimal.
# ---------------------------------------------------------------------------
G_LATTICE = 1.0 / (72.0 * math.pi)                        # 0.00442097...

register(Constant(
    symbol="G_LATTICE",
    value=G_LATTICE,
    units="lattice natural units (a = tau = hbar = 1)",
    exactness="exact",
    provenance=("F79", "F107"),
    derivation=r"G = a^2c^3/(8\pi\sqrt3\,\hbar) (F79 closed form) evaluated in "
               r"lattice units, where the SI light speed is numerically "
               r"c_\text{lat} = 1/\sqrt3, giving G = c_\text{lat}^4/(8\pi) = 1/(72\pi). "
               r"Structural: no free coupling anywhere in the chain.",
    sector="gravity",
    tol=1e-12,
    sites=(
        Site("src/casim/engine/interactions/gravity.py", "G_LATTICE", kind="import",
             note="was the canonical definition; now imports the registry's"),
        Site("src/casim/gravity/__init__.py", None, kind="reexport",
             note="re-export of the canonical value, not a redefinition — the "
                  "pattern the other sectors now follow by construction"),
    ),
    notes="Asserted at tests/casim/test_gravity_element.py:59 — the one constant "
          "in the repo that already had a regression barrier before P0.",
))

# ---------------------------------------------------------------------------
# The F106 sourcing coefficient
# ---------------------------------------------------------------------------
register(Constant(
    symbol="F106_COEFF_LATTICE",
    value=1.0,
    units="lattice natural units",
    exactness="exact",
    provenance=("F106", "F178"),
    derivation=r"8\pi G/c^4 = a^2c_\text{lat}/(\hbar c) \to 1 exactly in lattice "
               r"units (F106-E1, exactness row #181), so \nabla^2\ln K = -T^{00}.",
    sector="gravity",
    tol=0.0,
    sweep=False,
    sweep_reason="The value is exactly 1.0. Sweeping for it would flag every "
                 "module-level `SOMETHING = 1.0` in the tree — 93 of them at the "
                 "C2 measurement — which is noise, not evidence. Its one site is "
                 "recorded explicitly instead.",
    sites=(Site("src/casim/engine/interactions/gravity.py", "F106_COEFF_LATTICE",
                kind="import"),),
    notes="F178 reclassified the energy-only law this coefficient belongs to as the "
          "STATIC WEAK-FIELD REDUCTION of the induced Einstein equation, not the "
          "fundamental law. The coefficient is unchanged; its status is not. See "
          "docs/theory/supersessions.yaml (F178).",
))
