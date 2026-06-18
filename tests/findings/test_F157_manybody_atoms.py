"""F157 — Phase 2(iii): multi-nucleon nuclei and multi-electron clouds.

roadmap-scale-to-real-space.md Phase 2(iii) / F148 extension.  Lifts the
modular element assembler from "A=1 / Z=1 verified, A>=3 / Z>=2 wired-but-not-
run" to actually COMPUTING multi-nucleon nuclei and multi-electron clouds from
the model's own building blocks (ca_manybody), with no fitted semi-empirical
coefficients.

  E1  multi-electron Hartree SCF reproduces the helium ionization energy
      (Koopmans ~24 eV vs CODATA 24.59) from m_e + alpha alone
  E2  the SCF generalises (Aufbau) and stays bound for Li, C
  N1  the A-body variational cluster, anchored ONLY to the model deuteron,
      binds the alpha particle near experiment (A=4: ~30 MeV vs 28.3)
  N2  the lighter A=3 system is bound
  A1  the assembler composes a full neutral, stable multi-nucleon/multi-
      electron atom (He-4) end to end

Runs under pytest, or standalone:
    PYTHONPATH=ca-simulation python tests/findings/test_F157_manybody_atoms.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "ca-simulation"))

import ca_manybody as mb          # noqa: E402
import ca_element as el           # noqa: E402


def test_E1_helium_ionization_from_first_principles():
    r = mb.electron_cloud_hartree(2)
    assert r["converged"]
    # Koopmans IP within 10% of CODATA 24.59 eV (Hartree, no exchange)
    assert abs(r["ionization_eV"] - 24.59) / 24.59 < 0.10, r["ionization_eV"]
    # total energy bound and near the Hartree limit (~ −77.9 eV)
    assert r["total_energy_eV"] < -70.0


def test_E2_scf_generalises_and_binds():
    for Z in (3, 6):
        r = mb.electron_cloud_hartree(Z)
        assert r["converged"]
        assert r["total_energy_eV"] < 0.0
        assert r["ionization_eV"] > 0.0          # a bound, ionizable valence e


def test_N1_alpha_particle_binds_near_experiment():
    r = mb.nuclear_binding_Abody(2, 2)
    assert r["bound"]
    # A=4 binding anchored ONLY to the model deuteron; exp −28.3 MeV
    assert abs(r["E_MeV"] - (-28.3)) / 28.3 < 0.20, r["E_MeV"]


def test_N2_A3_system_binds():
    r = mb.nuclear_binding_Abody(2, 1)
    assert r["bound"] and r["E_MeV"] < 0.0
    assert r["A"] == 3


def test_A1_assembler_composes_full_atom():
    e = el.build_element(2, 2)               # He-4
    rep = e.verify_stability()
    assert rep["neutral"] and rep["net_charge_e"] == 0
    assert rep["nucleus"]["bound"] is True
    assert rep["electrons"]["bound"] is True
    assert rep["stable"] is True


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    p = f = 0
    for fn in fns:
        try:
            fn(); print("PASS", fn.__name__); p += 1
        except Exception as e:           # noqa: BLE001
            print("FAIL", fn.__name__, repr(e)); traceback.print_exc(); f += 1
    print(f"== {p} passed, {f} failed ==")
    sys.exit(1 if f else 0)
