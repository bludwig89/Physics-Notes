"""casim.fields — field sectors, organised by the F91 propagator classification.

Sub-modules:
    photon       γ — even (forced)               ca_photon_pair
    electroweak  W± chiral, Z even+axial          ca_wmu, ca_weak, ca_z_field,
                                                  ca_charged_current, ca_hypercharge
    strong       gluon even (forced, F91)         ca_gluon, ca_strong, ca_colour_*,
                                                  ca_confinement, spinor_color
    matter       Weyl/Dirac per-branch            ca_dirac, ca_dirac_bcc, ca_baryon,
                                                  ca_higgs
    em           σ-bilinear (massive/non-Abelian) ca_maxwell, ca_maxwell_2d
"""
from __future__ import annotations

from . import photon, electroweak, strong, matter, em  # noqa: F401

__all__ = ["photon", "electroweak", "strong", "matter", "em"]
