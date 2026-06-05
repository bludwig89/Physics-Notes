"""casim.particles.spec — typed particles with exact quantum numbers.

A ``ParticleSpec`` carries the exact (``fractions.Fraction``) charges of one
Weyl species.  The force-applicability matrix is *derived* from the charges
(``couples_to``), never declared per particle, so a scenario can only wire a
particle to a force the physics permits (e.g. leptons carry no colour, so the
strong force cannot be attached to them — refused at build time).

Conventions match the audited test suites:
  * Gell-Mann–Nishijima ``Q = T3 + Y/2`` — validated exactly at construction
    (FG-1 / F38, F35 W6.4).
  * Charge conjugation ``C: (T3, Q, Y) → (−T3, −Q, −Y)`` (F53 P1); antiparticle
    specs are generated, not typed in.
  * First-generation content = the anomaly-free FG-1 table (F38).

Everything in this module is pure bookkeeping — Tier-1 exact, no floats except
the optional lattice ``mass`` parameter (F27 complex-mass, default 0).
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Dict, FrozenSet

FORCES = ("gravity", "em", "weak", "strong")

F = Fraction  # local alias


@dataclass(frozen=True)
class ParticleSpec:
    """Exact quantum numbers of one Weyl species (or a left doublet)."""

    name: str
    kind: str                      # "lepton" | "quark"
    T3: Fraction = F(0)
    Y: Fraction = F(0)
    Q: Fraction = F(0)
    colour: bool = False
    B: Fraction = F(0)             # baryon number
    Lnum: Fraction = F(0)          # lepton number
    chirality: str = "L"           # "L" | "R"
    mass: float = 0.0              # F27 complex-mass parameter (lattice units)
    antiparticle: bool = False

    def __post_init__(self):
        if self.kind not in ("lepton", "quark"):
            raise ValueError(f"{self.name}: unknown kind {self.kind!r}")
        if self.chirality not in ("L", "R"):
            raise ValueError(f"{self.name}: chirality must be 'L' or 'R'")
        # Gell-Mann–Nishijima, exact (FG-1 / F35 W6.4).
        if self.Q != self.T3 + self.Y / 2:
            raise ValueError(
                f"{self.name}: Gell-Mann–Nishijima violated: "
                f"Q={self.Q} != T3+Y/2={self.T3 + self.Y / 2}")
        if self.colour and self.kind != "quark":
            raise ValueError(f"{self.name}: only quarks carry colour")
        if self.kind == "quark" and not self.colour:
            raise ValueError(f"{self.name}: quarks are colour triplets")

    # ------------------------------------------------------------------
    def couples_to(self) -> FrozenSet[str]:
        """Force set derived from the charges (the applicability matrix)."""
        forces = {"gravity"}                      # universal (F64)
        if self.Q != 0:
            forces.add("em")                      # U(1)_em minimal coupling (F68)
        if self.T3 != 0 or self.Y != 0:
            forces.add("weak")                    # W needs T3; Z/B needs Y
        if self.colour:
            forces.add("strong")                  # SU(3) triplet only
        return frozenset(forces)

    def conjugate(self) -> "ParticleSpec":
        """F53 charge conjugation: (T3, Q, Y, B, L) → −(T3, Q, Y, B, L).

        Chirality flips (the conjugate of a right-handed field is left-handed,
        e.g. e_R → e^c_L)."""
        bar = (self.name[:-4] if self.antiparticle else self.name + "_bar")
        flip = "L" if self.chirality == "R" else "R"
        return replace(self, name=bar, T3=-self.T3, Y=-self.Y, Q=-self.Q,
                       B=-self.B, Lnum=-self.Lnum, chirality=flip,
                       antiparticle=not self.antiparticle)

    def charges(self) -> Dict[str, object]:
        """Exact charges as strings (JSON-safe, no float coercion)."""
        return {"Q": str(self.Q), "T3": str(self.T3), "Y": str(self.Y),
                "B": str(self.B), "L": str(self.Lnum),
                "colour": self.colour, "chirality": self.chirality}


# ----------------------------------------------------------------------
# First-generation registry (FG-1 / F38 anomaly-free content).
# ----------------------------------------------------------------------
def _lep(name, T3, Y, chirality):
    return ParticleSpec(name=name, kind="lepton", T3=F(T3[0], T3[1]),
                        Y=F(Y[0], Y[1]), Q=F(T3[0], T3[1]) + F(Y[0], Y[1]) / 2,
                        Lnum=F(1), chirality=chirality)


def _qrk(name, T3, Y, chirality):
    return ParticleSpec(name=name, kind="quark", T3=F(T3[0], T3[1]),
                        Y=F(Y[0], Y[1]), Q=F(T3[0], T3[1]) + F(Y[0], Y[1]) / 2,
                        colour=True, B=F(1, 3), chirality=chirality)


_FIRST_GEN = [
    _lep("nu_e_L", (1, 2), (-1, 1), "L"),
    _lep("e_L",   (-1, 2), (-1, 1), "L"),
    _lep("e_R",    (0, 1), (-2, 1), "R"),
    _qrk("u_L",    (1, 2), (1, 3), "L"),
    _qrk("d_L",   (-1, 2), (1, 3), "L"),
    _qrk("u_R",    (0, 1), (4, 3), "R"),
    _qrk("d_R",    (0, 1), (-2, 3), "R"),
]

REGISTRY: Dict[str, ParticleSpec] = {}
for _s in _FIRST_GEN:
    REGISTRY[_s.name] = _s
    _a = _s.conjugate()
    REGISTRY[_a.name] = _a

# Left doublets — the covariant-step objects (E2E B1 / FG-3 patterns).
DOUBLETS: Dict[str, tuple] = {
    "lepton_doublet_L": ("nu_e_L", "e_L"),
    "quark_doublet_L": ("u_L", "d_L"),
}


def get_spec(name: str) -> ParticleSpec:
    try:
        return REGISTRY[name]
    except KeyError:
        raise KeyError(f"unknown particle {name!r}; "
                       f"registered: {sorted(REGISTRY)}")


def doublet_specs(name: str) -> tuple:
    try:
        up, down = DOUBLETS[name]
    except KeyError:
        raise KeyError(f"unknown doublet {name!r}; "
                       f"registered: {sorted(DOUBLETS)}")
    return get_spec(up), get_spec(down)


def anomaly_traces() -> Dict[str, Fraction]:
    """FG-1 anomaly traces over the L-handed content (conjugates of R).

    All six vanish exactly for the registry content (F38); recomputed here so
    the registry itself is regression-locked, not just the original test.
    Multiplicity n_i = colour factor × doublet factor.
    """
    # L-handed Weyl fields: doublets as-is; R fields enter as conjugates.
    fields = []
    for nm in ("nu_e_L", "e_L", "u_L", "d_L"):
        fields.append(REGISTRY[nm])
    for nm in ("e_R", "u_R", "d_R"):
        fields.append(REGISTRY[nm].conjugate())   # e^c_L, u^c_L, d^c_L
    def n(s):  # multiplicity
        return (3 if s.colour else 1)
    grav_Y = sum(n(s) * s.Y for s in fields)
    Y3 = sum(n(s) * s.Y ** 3 for s in fields)
    su2_Y = sum(n(s) * s.Y for s in fields if s.T3 != 0) / 2
    su3_Y = sum(s.Y for s in fields if s.colour)
    su3_cube = sum((1 if not s.antiparticle else -1)
                   for s in fields if s.colour)
    return {"grav_Y": grav_Y, "Y3": Y3, "SU22_Y": su2_Y,
            "SU32_Y": su3_Y, "SU33": F(su3_cube)}
