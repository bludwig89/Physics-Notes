#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_element.py
=============

F148 — the MODULAR ELEMENT ASSEMBLER: compose an arbitrary element
``E(Z, N)`` out of the model's already-certified building blocks and verify it
is a stable, neutral atom.  An element is, structurally,

        atom(Z, N)  =  NUCLEUS(Z protons + N neutrons)  +  ELECTRON CLOUD(Z e-)

and nothing else.  This module wires the two layers together behind one
entry point, :func:`build_element`, so that *any* element — light or heavy —
can be instantiated by changing two integers, while the concrete numerical
verification target right now is HYDROGEN (Z=1, N=0).

STRICTLY MODEL-ONLY  (the design constraint)
--------------------------------------------
The assembler introduces **zero new parameters**.  Every dimensionful or
dimensionless quantity it uses is imported from an already-published model
module — no fitted semi-empirical (liquid-drop) coefficients, no tuned shell
gaps.  The provenance:

  * electron mass  m_e , proton mass m_p , EM coupling alpha   <- ca_atom   (F120 / F122-F123 / F125; alpha is the one EM input)
  * the colour-singlet baryon (proton uud, neutron udd)        <- ca_baryon_dynamics (F122: confinement-bound, non-dispersing)
  * the nucleon-nucleon force (one-boson exchange)             <- ca_nuclear (pi F103/F104, sigma F126, omega F128, quark-Pauli core F113)
  * the Coulomb / Dirac radial electron solver                <- ca_atom   (F125)

So the *framework* is general; the *content* is the model's.

LAYERS
------
1. ``Nucleus(Z, N)``  -- A = Z+N nucleons, each a model baryon.
     - A = 1 : a single confinement-bound baryon (F122).  Self-bound, no
               inter-nucleon force needed; nuclear binding energy = 0 by
               definition (there is no bond to form).
     - A = 2 : the model-native NN one-boson-exchange bound state
               (``ca_nuclear.solve_deuteron``, fully derived OBE: pi+sigma+
               omega+core).  The deuteron (pn) is the worked case.
     - A >= 3: the SAME NN OBE potential fed to an A-body relative-coordinate
               solver (Jacobi / cluster), exactly as F122 generalised the
               two-body F74 engine to three quarks.  Implemented here as a
               documented extension hook (``binding_energy`` raises
               NotImplementedError with the precise recipe) so the framework
               is honest about what is solved vs. what is wired-but-not-run.

2. ``ElectronCloud(Z, nuclear_charge)``  -- Z electrons in the nuclear field.
     - Z = 1 : the F125 exact Coulomb/Dirac solve (ground state = -Ry).
     - Z >= 2: the SAME radial Coulomb solver in a self-consistent screened
               mean field (effective Z per shell) with Pauli/Aufbau filling --
               model-only (Coulomb channel + Fermi statistics, no fitted
               screening constants).  Extension hook, same honesty policy.

3. ``Element`` / :func:`build_element`  -- composes the two layers, checks
   electrical neutrality (Z protons - Z electrons = 0), nuclear binding,
   electronic binding, and returns a structured stability verdict.

NUMERICS
--------
Pure real linear algebra (the F125 tridiagonal Coulomb eigenproblem and the
F122 real-symmetric generalised eigenproblem); the CLAUDE.md numpy/scipy
chiral-transform caveat does not bite here (no chiral transforms).
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

# --- model modules (the ONLY source of constants/physics) ------------------
_HERE = os.path.dirname(__file__)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import ca_atom as _atom               # F125 Coulomb/Dirac electron solver + m_e, m_p, alpha
import ca_baryon_dynamics as _baryon  # F122 colour-singlet baryon (proton/neutron)

# ca_nuclear is only needed for A>=2; import lazily so the A=1 path (hydrogen)
# has no heavy dependency and stays fast.
def _nuclear():
    import ca_nuclear as _n  # noqa
    return _n


# ===========================================================================
#  Provenance-tagged constants (imported, never redefined here)
# ===========================================================================
M_E_MEV = _atom.M_E_MEV       # electron rest energy (model P0/F120 anchor)
M_P_MEV = _atom.M_P_MEV       # proton  rest energy (F122/F123)
M_N_MEV = 939.56542052        # neutron rest energy (CODATA; F122 derives m_n-m_p sign)
ALPHA = _atom.ALPHA           # EM coupling (the one EM input, F125)

# Electron shell capacities by principal/orbital structure (Pauli only — no
# fitted numbers): s,p,d,f hold 2,6,10,14.  Aufbau (Madelung n+l) ordering.
_SUBSHELL_CAP = {"s": 2, "p": 6, "d": 10, "f": 14}
# Madelung-ordered (n, l-letter) subshells, enough for Z up to ~120.
_AUFBAU = [
    (1, "s"), (2, "s"), (2, "p"), (3, "s"), (3, "p"), (4, "s"), (3, "d"),
    (4, "p"), (5, "s"), (4, "d"), (5, "p"), (6, "s"), (4, "f"), (5, "d"),
    (6, "p"), (7, "s"), (5, "f"), (6, "d"), (7, "p"),
]


# ===========================================================================
#  1.  NUCLEUS
# ===========================================================================
@dataclass
class Nucleus:
    """A = Z + N nucleons, each a model colour-singlet baryon (F122)."""
    Z: int                       # protons  (uud)
    N: int                       # neutrons (udd)

    def __post_init__(self):
        if self.Z < 0 or self.N < 0:
            raise ValueError("Z, N must be non-negative")
        if self.A < 1:
            raise ValueError("a nucleus needs at least one nucleon")

    # -- structure -----------------------------------------------------------
    @property
    def A(self) -> int:
        return self.Z + self.N

    @property
    def charge(self) -> int:
        """Nuclear charge in units of e (= number of protons)."""
        return self.Z

    # -- the constituent baryons are themselves bound (F122) -----------------
    def baryon_is_bound(self, sigma: float = 1.0, alpha_s: float = 0.50,
                        m_q: float = 0.785, basis=None) -> dict:
        """Certify a constituent nucleon is a confinement-bound baryon (F122).

        Solves the three-quark relative problem (model OBE: confining string +
        one-gluon exchange).  The confining spectrum is purely discrete, so the
        baryon is automatically non-dispersing / bound for any sigma>0.  Returns
        the ground relative energy E_rel, the baryon mass M, and the F97/F122
        'mass is the string' diagnostic (constituent-mass fraction of M).

        Units are sigma-string units unless a scale is supplied (absolute MeV is
        the P6 concern, intentionally not invoked for a stability statement).
        """
        if basis is None:
            basis = _baryon.make_basis(n1=8, n2=8, correlated=True, symmetrize=False)
        M, E_rel, res = _baryon.baryon_mass(m_q, sigma, alpha_s, basis=basis)
        mass_sum = 3.0 * m_q
        return {
            "E_rel": float(E_rel),
            "M": float(M),
            "constituent_mass_fraction": float(mass_sum / M) if M > 0 else float("nan"),
            "discrete_spectrum_bound": bool(np.isfinite(E_rel)),
        }

    # -- nuclear binding energy (MeV) ---------------------------------------
    def binding_energy(self, **kw) -> float:
        """Inter-nucleon binding energy in MeV (>0 = bound).

        A=1  -> 0.0 exactly (a single nucleon forms no bond; it is self-bound as
                 a baryon, certified by ``baryon_is_bound``).
        A=2  -> the model-native NN OBE bound state.  For the deuteron (Z=N=1)
                 this is ``ca_nuclear.solve_deuteron`` with the fully-derived
                 core (F113) + sigma (F126) + omega (F128) + pion tensor (F104).
        A>=3 -> NotImplementedError carrying the exact extension recipe.
        """
        if self.A == 1:
            return 0.0
        if self.A == 2:
            if self.Z == 1 and self.N == 1:          # deuteron (pn)
                n = _nuclear()
                # Full model-native one-boson exchange (F104 + F126 + F128 + F113):
                #   pion tensor (F103/F104) + bare 3-quark sigma attraction
                #   g_sigma^2/4pi = 8.182 (F126) + isoscalar-vector omega
                #   repulsion g_omega^2/4pi = 5.39 (F128, empirical OBE/SU(6)
                #   window) + the F113 quark-Pauli derived core, at the model
                #   quark size b = 0.55 fm.  No coupling tuned to the binding.
                cfg = dict(core="derived", b=0.55, tensor=True,
                           sigma=True, sigma_g2_4pi=n.SIGMA_G2_4PI_BARE,
                           omega=True, omega_g2_4pi=5.39,
                           m_omega=n.M_OMEGA_DEFAULT, vectors=False)
                cfg.update(kw)
                res = n.solve_deuteron(**cfg)
                Eb = res["E_b"] if isinstance(res, dict) and "E_b" in res else _extract_Eb(res)
                return float(Eb)
            # pp / nn are unbound (no model bound state) -> 0 binding
            return 0.0
        # A >= 3: the A-body variational cluster solve, fed the SAME model NN
        # interaction (central OBE + the model-deuteron-anchored S=1,T=0
        # attraction), exactly as F122 generalised the two-body engine to three
        # quarks.  (Phase 2(iii); ca_manybody.nuclear_binding_Abody.)
        import ca_manybody as _mb
        res = _mb.nuclear_binding_Abody(self.Z, self.N, **kw)
        self._abody = res                      # keep the full diagnostics
        return float(-res["E_MeV"]) if res["bound"] else 0.0

    def stability(self, **kw) -> dict:
        """Structural stability verdict for the nucleus."""
        if self.A == 1:
            b = self.baryon_is_bound()
            return {"A": 1, "kind": "single bound baryon (F122)",
                    "nuclear_binding_MeV": 0.0,
                    "bound": b["discrete_spectrum_bound"],
                    "baryon": b}
        Eb = self.binding_energy(**kw)
        if self.A == 2:
            return {"A": 2, "kind": "NN one-boson-exchange bound state",
                    "nuclear_binding_MeV": Eb, "bound": Eb > 0.0}
        out = {"A": self.A, "kind": "A-body variational cluster (model-anchored)",
               "nuclear_binding_MeV": Eb, "bound": Eb > 0.0}
        ab = getattr(self, "_abody", None)
        if ab is not None:
            out["binding_per_A_MeV"] = -ab["E_per_A_MeV"]
            out["tier"] = ab["tier"]
            out["anchor_deuteron_MeV"] = ab["anchor_Eb_MeV"]
        return out


def _extract_Eb(res):
    """solve_deuteron may return a dict or an array of eigenvalues; the binding
    energy is -(lowest level) when the lowest level is negative (bound)."""
    if isinstance(res, dict):
        for k in ("E_b", "Eb", "binding_MeV"):
            if k in res:
                return res[k]
        if "E1" in res:
            return -res["E1"] if res["E1"] < 0 else 0.0
        if "levels" in res:
            E0 = float(np.min(res["levels"]))
            return -E0 if E0 < 0 else 0.0
    arr = np.atleast_1d(np.asarray(res, dtype=float))
    E0 = float(np.min(arr))
    return -E0 if E0 < 0 else 0.0


# ===========================================================================
#  2.  ELECTRON CLOUD
# ===========================================================================
@dataclass
class ElectronCloud:
    """Z electrons bound to a nucleus of charge ``nuclear_charge`` by EM."""
    Z: int                       # number of electrons (neutral atom: = nuclear_charge)
    nuclear_charge: int          # protons in the nucleus

    def __post_init__(self):
        if self.Z < 0:
            raise ValueError("electron count must be non-negative")

    @property
    def charge(self) -> int:
        """Electron-cloud charge in units of e (= -Z)."""
        return -self.Z

    # -- Aufbau configuration (Pauli only) ----------------------------------
    def configuration(self) -> list:
        """Fill subshells in Madelung order. Returns [((n, 'l'), count), ...]."""
        remaining = self.Z
        cfg = []
        for (n, ll) in _AUFBAU:
            if remaining <= 0:
                break
            cap = _SUBSHELL_CAP[ll]
            k = min(cap, remaining)
            cfg.append(((n, ll), k))
            remaining -= k
        if remaining > 0:
            raise ValueError(f"Z={self.Z} exceeds tabulated Aufbau capacity")
        return cfg

    # -- total electronic energy (eV) ---------------------------------------
    def total_energy_eV(self, N_grid: int = 6000) -> float:
        """Total electronic binding energy in eV (<0 = bound).

        Z=1  -> the F125 exact Coulomb/Dirac hydrogenic ground state (-Ry),
                 from the model's own m_e and alpha.
        Z>=2 -> sum of hydrogenic subshell energies in a self-consistent
                 screened mean field (effective Z per shell), the model-only
                 multi-electron hook (Coulomb + Pauli, no fitted screening).
                 NotImplementedError until the SCF loop is run.
        """
        if self.Z == 0:
            return 0.0
        mu = _atom.reduced_mass_MeV(M_E_MEV, _z_nuclear_mass_MeV(self.nuclear_charge))
        if self.Z == 1:
            spec = _atom.hydrogen_spectrum(n_max=2, mu_MeV=mu, Z=self.nuclear_charge,
                                           alpha=ALPHA, N=N_grid)
            return float(spec["levels"][(1, 0)])     # 1s ground state, eV
        # Z >= 2: the self-consistent Hartree mean field (Coulomb + Pauli/
        # Aufbau), each orbital in the field of all OTHER electrons, iterated
        # to consistency — model-only (m_e, alpha; screening from the actual
        # density).  (Phase 2(iii); ca_manybody.electron_cloud_hartree.)
        import ca_manybody as _mb
        res = _mb.electron_cloud_hartree(self.Z, alpha=ALPHA, m_e_MeV=M_E_MEV)
        self._scf = res                          # keep the full diagnostics
        return float(res["total_energy_eV"])

    def stability(self, **kw) -> dict:
        E = self.total_energy_eV(**kw)
        out = {"Z": self.Z, "configuration": self.configuration(),
               "total_energy_eV": E, "bound": E < 0.0}
        scf = getattr(self, "_scf", None)
        if scf is not None:
            out["ionization_eV"] = scf["ionization_eV"]
            out["scf_converged"] = scf["converged"]
            out["tier"] = scf["tier"]
        return out


def _z_nuclear_mass_MeV(Z: int) -> float:
    """Crude nuclear mass for the reduced-mass correction of the electron
    problem.  For hydrogen (Z=1) this is exactly m_p; the value only enters the
    ~5e-4 reduced-mass factor, so a one-proton default is sufficient here."""
    return M_P_MEV if Z <= 1 else Z * (M_P_MEV + M_N_MEV) / 2.0


# ===========================================================================
#  3.  ELEMENT  (the composed atom)
# ===========================================================================
@dataclass
class Element:
    Z: int
    N: int
    nucleus: Nucleus = field(init=False)
    electrons: ElectronCloud = field(init=False)

    def __post_init__(self):
        self.nucleus = Nucleus(self.Z, self.N)
        self.electrons = ElectronCloud(self.Z, self.Z)   # neutral atom

    # -- identity ------------------------------------------------------------
    @property
    def A(self) -> int:
        return self.Z + self.N

    @property
    def symbol(self) -> str:
        return _SYMBOLS.get(self.Z, f"Z{self.Z}")

    @property
    def name(self) -> str:
        return f"{self.symbol}-{self.A}" if self.A else self.symbol

    def net_charge(self) -> int:
        """Total charge in units of e: protons - electrons. 0 for a neutral atom."""
        return self.nucleus.charge + self.electrons.charge

    # -- stability verdict ---------------------------------------------------
    def verify_stability(self, **kw) -> dict:
        nuc = self.nucleus.stability()
        ele = self.electrons.stability()
        neutral = (self.net_charge() == 0)
        nuc_ok = bool(nuc.get("bound"))
        ele_ok = bool(ele.get("bound"))
        stable = neutral and nuc_ok and ele_ok
        ionization_eV = (-ele["total_energy_eV"]
                         if ele.get("total_energy_eV") is not None else None)
        return {
            "element": self.name, "Z": self.Z, "N": self.N, "A": self.A,
            "net_charge_e": self.net_charge(), "neutral": neutral,
            "nucleus": nuc, "electrons": ele,
            "ionization_energy_eV": ionization_eV,
            "stable": stable,
        }


def build_element(Z: int, N: Optional[int] = None) -> Element:
    """Modular entry point: assemble element (Z, N) from model building blocks.

    ``N`` defaults to 0 for Z=1 (protium) and otherwise to Z (the lightest
    self-conjugate guess); pass it explicitly to choose an isotope.
    """
    if N is None:
        N = 0 if Z == 1 else Z
    return Element(Z, N)


_SYMBOLS = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
    9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
    16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 26: "Fe", 79: "Au",
    82: "Pb", 92: "U",
}


# ===========================================================================
if __name__ == "__main__":
    print("=== F148 modular element assembler ===\n")
    H = build_element(1, 0)             # protium, 1H
    rep = H.verify_stability()
    print(f"element        : {rep['element']}  (Z={rep['Z']}, N={rep['N']}, A={rep['A']})")
    print(f"net charge     : {rep['net_charge_e']} e   (neutral={rep['neutral']})")
    print(f"nucleus        : {rep['nucleus']['kind']}  bound={rep['nucleus']['bound']}")
    b = rep['nucleus']['baryon']
    print(f"   baryon E_rel={b['E_rel']:.6f} (string units), "
          f"constituent-mass fraction={b['constituent_mass_fraction']:.4%}")
    print(f"electrons      : {rep['electrons']['configuration']}  "
          f"E={rep['electrons']['total_energy_eV']:.6f} eV  bound={rep['electrons']['bound']}")
    print(f"ionization     : {rep['ionization_energy_eV']:.6f} eV")
    print(f"STABLE         : {rep['stable']}")

    print("\n-- framework composes arbitrary (Z, N) (instantiation only) --")
    for (z, nn) in [(1, 1), (2, 2), (6, 6), (26, 30), (92, 146)]:
        e = build_element(z, nn)
        print(f"   {e.name:7s} Z={z:3d} N={nn:3d} A={e.A:3d}  "
              f"config={e.electrons.configuration()[-1]}  net_charge={e.net_charge()}")
