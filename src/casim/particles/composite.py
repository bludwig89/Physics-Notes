"""casim.particles.composite — stacked multi-quark composites + processes (P4).

Phase P4 of ``roadmap-particle-layer.md``: build the first composite hadron as
a **stacked multi-quark particle** (the F71 proton, an ``ε_abc`` colour
singlet) and express **β-decay as a particle-level process** (F54).  As in
those findings this is the *structural / operator* level — exact quantum
numbers, colour-singlet gauge invariance, and exact conservation ledgers — with
the real-time dynamical bound state left to a later phase (F71 scope).

Nothing here recomputes physics by hand: the colour-singlet algebra is the
audited ``ca_baryon`` (F71) and the conservation arithmetic is the audited
``ca_charged_current.conservation_residuals`` (F54).  This module is the typed
``ParticleSpec``-level wiring over them, with every charge an exact
``fractions.Fraction``.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, FrozenSet, List, Tuple

from .spec import ParticleSpec, get_spec

F = Fraction


# ----------------------------------------------------------------------
# CompositeSpec — exact quantum numbers of a bound multi-quark state
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class CompositeSpec:
    """A composite particle: a tuple of constituent ``ParticleSpec`` quarks.

    Aggregate charges are exact ``Fraction`` sums of the constituents; the
    Gell-Mann–Nishijima relation ``Q = T3 + Y/2`` is re-checked on the totals.
    For a three-quark baryon the colour structure is the totally antisymmetric
    ``ε_abc`` singlet (F71), validated against the audited ``ca_baryon`` algebra
    by :meth:`colour_singlet_residual`.
    """

    name: str
    constituents: Tuple[ParticleSpec, ...]
    colour_structure: str = "epsilon_abc_singlet"

    def __post_init__(self):
        if not self.constituents:
            raise ValueError(f"{self.name}: a composite needs constituents")
        if self.colour_structure == "epsilon_abc_singlet":
            if len(self.constituents) != 3:
                raise ValueError(
                    f"{self.name}: the ε_abc colour singlet needs exactly 3 "
                    f"quarks (got {len(self.constituents)})")
            if not all(s.colour for s in self.constituents):
                raise ValueError(f"{self.name}: ε_abc singlet needs coloured "
                                 f"quarks")
        # Gell-Mann–Nishijima on the totals (exact).
        qn = self.quantum_numbers()
        if qn["Q"] != qn["T3"] + qn["Y"] / 2:
            raise ValueError(
                f"{self.name}: composite GMN violated: Q={qn['Q']} != "
                f"T3+Y/2={qn['T3'] + qn['Y'] / 2}")

    # ------------------------------------------------------------------
    def quantum_numbers(self) -> Dict[str, Fraction]:
        """Exact aggregate ``Q, B, Lnum, T3, Y`` (sum over constituents)."""
        def s(attr):
            return sum((getattr(c, attr) for c in self.constituents), F(0))
        return {"Q": s("Q"), "B": s("B"), "Lnum": s("Lnum"),
                "T3": s("T3"), "Y": s("Y")}

    def charges(self) -> Dict[str, object]:
        """JSON-safe aggregate charges (strings), plus colour-singlet flag."""
        qn = self.quantum_numbers()
        return {"Q": str(qn["Q"]), "T3": str(qn["T3"]), "Y": str(qn["Y"]),
                "B": str(qn["B"]), "L": str(qn["Lnum"]),
                "colour_singlet": self.is_colour_singlet,
                "content": "".join(self._flavour(c) for c in self.constituents)}

    @staticmethod
    def _flavour(spec: ParticleSpec) -> str:
        # "u_L" -> "u";  robust to chirality suffixes.
        return spec.name.split("_")[0]

    @property
    def is_colour_singlet(self) -> bool:
        return self.colour_structure == "epsilon_abc_singlet"

    def couples_to(self) -> FrozenSet[str]:
        """A colour singlet does **not** couple to the strong force at long
        range (no net colour, F71); residual forces are the union of the
        constituents' non-strong couplings, plus em iff the total Q ≠ 0."""
        forces = {"gravity"}
        if self.quantum_numbers()["Q"] != 0:
            forces.add("em")
        if any("weak" in c.couples_to() for c in self.constituents):
            forces.add("weak")
        return frozenset(forces)

    # ------------------------------------------------------------------
    def colour_singlet_residual(self) -> float:
        """max_a ‖G^a|S⟩‖ for the ε_abc singlet — 0 iff truly colourless.

        Delegates to the audited F71 ``ca_baryon.singlet_charge_residual``."""
        if not self.is_colour_singlet:
            return float("nan")
        import ca_baryon
        return float(ca_baryon.singlet_charge_residual())

    def colour_casimir(self) -> float:
        """Quadratic Casimir on the singlet (0 for a true singlet, F71)."""
        if not self.is_colour_singlet:
            return float("nan")
        import ca_baryon
        return float(ca_baryon.singlet_casimir())


# ----------------------------------------------------------------------
# Composite registry — the first-generation baryons
# ----------------------------------------------------------------------
def _baryon(name: str, flavours: Tuple[str, str, str]) -> CompositeSpec:
    # Use the left-handed quark specs so total isospin T3 comes out physical
    # (u_L,d_L carry T3 = ±1/2; the proton is the T3 = +1/2 member).
    specs = tuple(get_spec(f"{fl}_L") for fl in flavours)
    return CompositeSpec(name=name, constituents=specs)


COMPOSITES: Dict[str, CompositeSpec] = {
    "proton": _baryon("proton", ("u", "u", "d")),
    "neutron": _baryon("neutron", ("u", "d", "d")),
}


def get_composite(name: str) -> CompositeSpec:
    try:
        return COMPOSITES[name]
    except KeyError:
        raise KeyError(f"unknown composite {name!r}; "
                       f"registered: {sorted(COMPOSITES)}")


# ----------------------------------------------------------------------
# β-decay as a particle-level process (F54)
# ----------------------------------------------------------------------
def beta_decay_ledger() -> Dict[str, object]:
    """Exact conservation ledger for the F54 β-decay chain.

    Two vertices, each checked with the audited
    ``ca_charged_current.conservation_residuals`` (exact ``Fraction`` ΔQ/ΔB/ΔL):

      1. the quark charged-current vertex   d → u + W⁻
      2. the W decay                        W⁻ → e⁻ + ν̄_e

    and the composite-level neutron β-decay  n → p + e⁻ + ν̄_e built from them.
    Every Δ is exactly 0.
    """
    import ca_charged_current as cc
    vertex = cc.conservation_residuals(["d"], ["u", "W-"])
    wdecay = cc.conservation_residuals(["W-"], ["e", "nubar"])
    full = cc.conservation_residuals(["d"], ["u", "e", "nubar"])

    # Composite level: neutron (udd) → proton (uud) + e⁻ + ν̄_e — one d→u.
    n = get_composite("neutron").quantum_numbers()
    p = get_composite("proton").quantum_numbers()
    e = get_spec("e_L")          # electron (L=+1, Q=−1)
    # ν̄_e: conjugate of ν_e (L=−1, Q=0).
    nubar = get_spec("nu_e_L").conjugate()
    comp = {
        "dQ": (p["Q"] + e.Q + nubar.Q) - n["Q"],
        "dB": (p["B"] + e.B + nubar.B) - n["B"],
        "dL": (p["Lnum"] + e.Lnum + nubar.Lnum) - n["Lnum"],
    }
    return {"vertex_d_to_u_W": vertex, "W_to_e_nubar": wdecay,
            "full_d_to_u_e_nubar": full, "neutron_to_proton": comp}
