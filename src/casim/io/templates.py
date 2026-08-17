"""casim.io.templates — matter templates for the scenario ``extends:`` key.

Roadmap P4: "``extends:`` + matter templates — 'Put a hydrogen atom at (12,8,8)'
instead of 6 hand-matched channels in the right order.  The 46 YAMLs are
copy-paste variants."

A template is a partial scenario (channels + observers + lattice defaults).
``extends: hydrogen`` merges the named template *under* the scenario: the
scenario's own keys win, its ``lattice`` block is merged key-by-key, and its
``channels``/``observers`` — if given — replace the template's rather than
appending, so a scenario can start from a template and then fully override.

This is deliberately a small, closed registry rather than a plugin system:
the point is to collapse the copy-paste variants that already exist, not to
invent a second scenario language.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List

from casim.constants import c_lat as _C_LAT

# The lattice light speed 1/√3 is the registry constant, not a literal (D7).
_C = float(_C_LAT)

# The paired-spinor hydrogen chain (unified_hydrogen.yaml, roadmap U0): three
# colour quarks (uud) ↔ gluon confinement loop, (p,e) charge ↔ photon Coulomb α,
# an F64 dielectric gravity background, and the unification readout.
_HYDROGEN: Dict[str, Any] = {
    "lattice": {"L": 16, "topology": "bcc", "c_lat": _C},
    "channels": [
        {"type": "gravity_dielectric", "name": "gmass", "M": 1.0, "sigma": 3.0},
        {"type": "gluon_sourced", "name": "gluon_field",
         "sources": ["u_r", "u_g", "d_b"], "g_lat": 1.0, "dt": 1.0},
        {"type": "photon_sourced", "name": "photon_field",
         "sources": ["u_r", "u_g", "d_b", "electron"], "dt": 0.1,
         "g_em": 1.0, "coulomb": True, "g_coulomb": 6.0},
        {"type": "particle", "name": "u_r", "species": "u_L", "colour": "r",
         "init": {"center": [8, 8, 8], "width": 1.5},
         "couplings": {"strong": "gluon_field", "em": "photon_field",
                       "gravity": "gmass"}, "eps_strong": 0.3},
        {"type": "particle", "name": "u_g", "species": "u_L", "colour": "g",
         "init": {"center": [8, 8, 8], "width": 1.5},
         "couplings": {"strong": "gluon_field", "em": "photon_field",
                       "gravity": "gmass"}, "eps_strong": 0.3},
        {"type": "particle", "name": "d_b", "species": "d_L", "colour": "b",
         "init": {"center": [8, 8, 8], "width": 1.5},
         "couplings": {"strong": "gluon_field", "em": "photon_field",
                       "gravity": "gmass"}, "eps_strong": 0.3},
        {"type": "particle", "name": "electron", "species": "e_L", "mass": 0.3,
         "init": {"center": [12, 8, 8], "width": 2.0},
         "couplings": {"em": "photon_field", "gravity": "gmass"}},
    ],
    "observers": [
        {"type": "norm_conservation", "every": 10,
         "channels": ["u_r", "u_g", "d_b", "electron"]},
        {"type": "particle_readout", "every": 20},
        {"type": "unification_readout", "every": 5},
    ],
}

# The bare paired-spinor photon (photon_pair.yaml) — the smallest useful base.
_PHOTON: Dict[str, Any] = {
    "lattice": {"L": 16, "dims": 3, "topology": "cubic",
                "c_lat": _C},
    "channels": [{"type": "photon_pair", "init": "random"}],
    "observers": [
        {"type": "norm_conservation", "every": 5},
        {"type": "dispersion_fit", "every": 40},
    ],
}

TEMPLATES: Dict[str, Dict[str, Any]] = {
    "hydrogen": _HYDROGEN,
    "photon": _PHOTON,
}


def _merge(base: Dict[str, Any], over: Dict[str, Any]) -> Dict[str, Any]:
    """Merge ``over`` onto a deep copy of ``base``.

    Scalars and lists in ``over`` replace; nested mappings (only ``lattice``
    here) merge key-by-key so a scenario can override ``L`` without restating
    ``topology``/``c_lat``.
    """
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k == "extends":
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            merged = dict(out[k])
            merged.update(v)
            out[k] = merged
        else:
            out[k] = copy.deepcopy(v)
    return out


def resolve_extends(data: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve a scenario's ``extends:`` key into a fully materialised mapping.

    ``extends`` may be a template name or a list of names applied left-to-right
    (later ones override earlier ones), with the scenario itself applied last.
    Returns a new dict; the input is not mutated.  A no-op when ``extends`` is
    absent.
    """
    ext = data.get("extends")
    if not ext:
        return dict(data)
    names: List[str] = [ext] if isinstance(ext, str) else list(ext)
    acc: Dict[str, Any] = {}
    for name in names:
        if name not in TEMPLATES:
            raise KeyError(
                f"scenario extends unknown template {name!r}; "
                f"available: {sorted(TEMPLATES)}")
        acc = _merge(acc, TEMPLATES[name]) if acc else copy.deepcopy(
            TEMPLATES[name])
    return _merge(acc, data)


__all__ = ["TEMPLATES", "resolve_extends"]
