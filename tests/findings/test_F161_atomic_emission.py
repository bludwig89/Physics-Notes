"""F161 — Dynamical-processes layer P1: photon emission from atoms.

The static bound-state machinery (F125/F156) is turned into a RATE and a
SPECTRUM: an excited electron drops and radiates.  From the model's own m_e and
alpha (no new inputs), ca_emission predicts the atomic emission spectrum (line
frequencies = level differences) and the spontaneous-emission Einstein A
coefficients (dipole matrix element + Δl=±1 selection rule).

  E1  spectral lines: Lyman-α and the Balmer visible series match data
  E2  spontaneous-emission rate: 2p→1s = 6.27e8 s⁻¹ (lifetime 1.6 ns)
  E3  more rates: 3p→1s, 3p→2s match the known hydrogen A-coefficients
  E4  selection rule: 2s→1s (Δl=0) is dipole-forbidden (A=0)

Runs under pytest, or standalone:
    PYTHONPATH=ca-simulation python tests/findings/test_F161_atomic_emission.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "ca-simulation"))

import ca_emission as em      # noqa: E402


def test_E1_spectral_lines():
    assert abs(em.wavelength_nm(2, 1) - 121.567) / 121.567 < 0.01    # Lyman-α
    balmer = {3: 656.3, 4: 486.1, 5: 434.0, 6: 410.2}                # visible
    for ni, lam in balmer.items():
        assert abs(em.wavelength_nm(ni, 2) - lam) / lam < 0.01, ni


def test_E2_lyman_alpha_rate_and_lifetime():
    A = em.einstein_A_si(2, 1, 1, 0)                  # 2p → 1s
    assert abs(A - 6.27e8) / 6.27e8 < 0.05, A
    tau_ns = em.lifetime_s(2, 1, 1, 0) * 1e9
    assert abs(tau_ns - 1.6) < 0.1, tau_ns


def test_E3_other_rates():
    assert abs(em.einstein_A_si(3, 1, 1, 0) - 1.67e8) / 1.67e8 < 0.05   # 3p→1s
    assert abs(em.einstein_A_si(3, 1, 2, 0) - 2.24e7) / 2.24e7 < 0.06   # 3p→2s


def test_E4_dipole_selection_rule():
    assert em.einstein_A_si(2, 0, 1, 0) == 0.0       # 2s→1s, Δl=0 forbidden
    assert em.einstein_A_si(3, 2, 1, 0) == 0.0       # 3d→1s, Δl=2 forbidden
    assert em.einstein_A_si(2, 1, 1, 0) > 0.0        # 2p→1s, Δl=1 allowed


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
