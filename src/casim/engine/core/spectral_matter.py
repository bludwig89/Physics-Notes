"""casim.engine.core.spectral_matter — compute-once matter-sector channels.

These three channels wrap the audited *momentum-space* matter solvers
(``ca_meson``, ``ca_si_scale``, ``ca_qcd_scale_ratio``) so the falsification
suite's matter-sector briefs (FB02/FB03/FB09 + FA06) have a one-command
``casim run`` target like every other test.

They do **not** evolve a field on the lattice geometry — each is a *spectral*
solve (NJL gap + RPA ladder; the f_pi-anchored constituent nucleon; the two
QCD calibrations).  So the pattern is "compute-once": ``init_state`` runs the
solver and stores every physics number plus its PDG/empirical comparison in the
state; ``step`` is a no-op; the ``field_snapshot`` observer dumps the
``observables`` dict to the result JSON at tick 0.  Pure numpy — sandbox-fast,
fully reproducible.  (Same "doesn't fit the unitary tick loop" rationale as the
Tier-3 ``gauge_mc`` / ``refraction_2d`` channels.)

Channels
--------
  * ``njl_meson``     — pion/sigma χSB sector (FB03): m_c, m_pi, m_sigma, f_pi,
                        condensate, GMOR residual, + a chiral-limit Goldstone
                        check (m0→0 ⇒ m_pi→0).
  * ``njl_nucleon``   — f_pi-anchored constituent nucleon (FB02 + FA06):
                        m_c, m_p≈3m_c vs PDG 938.27, and the n−p splitting.
  * ``string_tension``— √σ/f_π via the two QCD calibrations (FB09):
                        (Λ/f_π)(√σ/Λ), condensate axis/sphere vs empirical 4.56.
"""
from __future__ import annotations

from typing import Any, Dict

from .channel import Channel, register
from casim.constants import (
    f_pi_anchor_MeV as _f_pi_anchor_MeV,
    f_pi_pdg_target_MeV as _f_pi_pdg_target_MeV,
)


def _f(x) -> float:
    """Coerce a (possibly numpy) scalar to a JSON-safe Python float."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


# ======================================================================
# 1. NJL meson sector — the pion as the χSB Goldstone (FB03 / F77 / F103)
# ======================================================================
@register
class NJLMesonChannel(Channel):
    """Dynamical light-meson spectrum from the canonical SU(2) NJL fit.

    Config (all optional; default = the F77 canonical fit, GeV):
      ``Lam`` (0.6515), ``GLam2`` (2.10), ``m0`` (0.0055), ``g_rhopipi`` (6.0).
    """
    type_name = "njl_meson"
    label = "NJL Meson Sector"
    propagator = "spectral"
    topologies = ("cubic", "bcc")

    # PDG / lattice anchors (MeV) used only for scoring, never as inputs.
    TARGETS = {"m_c": 325.0, "m_pi": 137.0, "f_pi": _f_pi_pdg_target_MeV}

    def _solve(self) -> Dict[str, Any]:
        from casim.engine.particles import meson as M
        cfg = self.config
        kw = {}
        for k in ("Lam", "GLam2", "m0", "g_rhopipi"):
            if k in cfg:
                kw[k] = cfg[k]
        spec = M.solve_meson_spectrum(**kw)
        # chiral-limit Goldstone check: m0 -> 0 must drive m_pi -> 0
        chiral_kw = dict(kw)
        chiral_kw["m0"] = 0.0
        spec_chiral = M.solve_meson_spectrum(**chiral_kw)
        return spec, spec_chiral

    def init_state(self, lattice, rng):
        spec, spec_chiral = self._solve()
        # everything in MeV for the report card
        m_c = _f(spec["m_c"]) * 1e3
        m_pi = _f(spec["m_pi"]) * 1e3
        m_sigma = _f(spec["m_sigma"]) * 1e3
        m_rho = _f(spec["m_rho"]) * 1e3
        f_pi = _f(spec["f_pi"]) * 1e3
        qq_root = _f(spec["condensate_root"]) * 1e3
        m_pi_chiral = _f(spec_chiral["m_pi"]) * 1e3
        T = self.TARGETS
        obs = {
            "m_c_MeV": m_c,
            "m_pi_MeV": m_pi,
            "m_sigma_MeV": m_sigma,
            "m_rho_MeV": m_rho,
            "f_pi_MeV": f_pi,
            "condensate_root_MeV": qq_root,
            "gmor_rel_residual": _f(spec["gmor_rel"]),
            "m_sigma_over_2mc": _f(spec["m_sigma_over_2mc"]),
            # chiral-limit Goldstone diagnostic
            "m_pi_chiral_limit_MeV": m_pi_chiral,
            "goldstone_ok": abs(m_pi_chiral) < 1.0,   # < 1 MeV ⇒ massless
            # PDG scoring
            "m_c_rel_err": (m_c - T["m_c"]) / T["m_c"],
            "m_pi_rel_err": (m_pi - T["m_pi"]) / T["m_pi"],
            "f_pi_rel_err": (f_pi - T["f_pi"]) / T["f_pi"],
            "targets_MeV": T,
        }
        return {"obs": obs, "_e": f_pi}

    def step(self, state, lattice, context=None, rng=None):
        return state

    def energy(self, state) -> float:
        return float(state["_e"])

    def observables(self, state, lattice) -> Dict[str, Any]:
        return state["obs"]


# ======================================================================
# 2. f_pi-anchored constituent nucleon (FB02 + FA06 / F123 / F97)
# ======================================================================
@register
class NJLNucleonChannel(Channel):
    """Nucleon mass m_p≈3m_c and the n−p splitting from one f_π anchor.

    Config (optional): ``f_pi_MeV`` (default 92.07, the F123 user-selected
    chiral anchor — the only dimensionful strong input).
    """
    type_name = "njl_nucleon"
    label = "NJL Nucleon (f_pi-anchored)"
    propagator = "spectral"
    topologies = ("cubic", "bcc")

    PDG = {"m_p": 938.272, "m_n": 939.565, "n_minus_p": 1.293, "m_N_third": 312.97}

    def init_state(self, lattice, rng):
        from casim.engine.lattice import si_scale as S
        f_pi = float(self.config.get("f_pi_MeV", _f_pi_anchor_MeV))
        reg = S.si_registry(f_pi_phys=f_pi)
        strong, nuc = reg["strong"], reg["nucleon"]
        nps = reg.get("np_split") or S.np_splitting(f_pi)
        P = self.PDG
        m_c = _f(strong.get("m_c", nuc.get("m_c_MeV")))
        m_p = _f(nuc.get("m_p_3mc_MeV"))
        n_minus_p = _f(nps.get("m_n_minus_m_p"))
        obs = {
            "f_pi_anchor_MeV": f_pi,
            "m_c_MeV": m_c,
            "m_c_rel_err": (m_c - P["m_N_third"]) / P["m_N_third"],
            "m_p_3mc_MeV": m_p,
            "m_p_rel_err": (m_p - P["m_p"]) / P["m_p"],
            "n_minus_p_MeV": n_minus_p,
            "n_minus_p_sign_positive": (n_minus_p is not None and n_minus_p > 0),
            "np_strong_term_MeV": _f(nps.get("m_d_minus_m_u")),
            "np_em_term_MeV": _f(nps.get("em_term")),
            "pdg": P,
        }
        return {"obs": obs, "_e": m_p}

    def step(self, state, lattice, context=None, rng=None):
        return state

    def energy(self, state) -> float:
        return float(state["_e"])

    def observables(self, state, lattice) -> Dict[str, Any]:
        return state["obs"]


# ======================================================================
# 3. √σ/f_π — the two QCD calibrations reconciled (FB09 / F124)
# ======================================================================
@register
class StringTensionFpiChannel(Channel):
    """√σ/f_π = (Λ/f_π)(√σ/Λ): chiral × confinement, vs empirical 4.56.

    Config: none (the routes/conventions are enumerated internally).
    """
    type_name = "string_tension"
    label = "√σ/f_π (two QCD calibrations)"
    propagator = "spectral"
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        from casim.engine.interactions import running_scale_ratio as Q
        s = Q.summary()
        emp = s["empirical"]["sqrt_sigma_over_f_pi"]
        axis = s["model"]["condensate_axis"]["sqrt_sigma_over_f_pi"]
        sphere = s["model"]["condensate_sphere"]["sqrt_sigma_over_f_pi"]
        obs = {
            "Lam_over_f_pi_chiral": _f(s["njl"]["Lam_over_f_pi"]),
            "sqrt_sigma_over_fpi_axis": _f(axis),
            "sqrt_sigma_over_fpi_sphere": _f(sphere),
            "empirical_sqrt_sigma_over_fpi": _f(emp),
            "axis_rel_err": (_f(axis) - _f(emp)) / _f(emp),
            "sphere_rel_err": (_f(sphere) - _f(emp)) / _f(emp),
            "band": f"{_f(sphere):.2f}-{_f(axis):.2f}",
        }
        return {"obs": obs, "_e": _f(axis)}

    def step(self, state, lattice, context=None, rng=None):
        return state

    def energy(self, state) -> float:
        return float(state["_e"])

    def observables(self, state, lattice) -> Dict[str, Any]:
        return state["obs"]
