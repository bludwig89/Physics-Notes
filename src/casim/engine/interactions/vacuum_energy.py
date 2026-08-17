"""
ca_vacuum_energy.py  --  The cosmological constant under the full-tensor source
===============================================================================

Scenario S9 (speculative / open).  F178 makes vacuum energy gravitate through
the full tensor: the vacuum has w = -1, so rho + 3p = -2 rho < 0 -- it
accelerates the expansion, exactly the dark-energy role.  But the *magnitude*
remains the F164 problem: the bare BCC zero-point density overshoots the
observed Lambda by ~10^120.  This module reframes F164 under the full-tensor
source and tabulates the candidate cancellations (none yet derived to zero) --
it quantifies the problem, it does not solve it.

Reuses the F164 fork for the bare zero-point integral.  Date: 2026-06-30 (F192).
"""

from __future__ import annotations

import os
import sys
import numpy as np

# C6: the F164 fork moved with this module (legacy forks/ ->
# casim.engine.forks.gravity/), so the old `<my dir>/forks` sys.path insert no
# longer names anything. Imported as a package module instead of by sys.path
# injection — same object, and it survives the C9 deletion of the legacy tree.
from casim.engine.forks.gravity import (                       # noqa: E402
    gr_fork_F164_cosmological_constant as f164)

RHO_LAMBDA_OBS = 6.0e-10        # J/m^3 (observed dark-energy density)


def vacuum_equation_of_state():
    """Vacuum w = -1: the full-tensor source term is rho + 3p = -2 rho < 0,
    i.e. vacuum accelerates the expansion (dark-energy sign).  The demoted
    energy-only law would have used rho > 0 -> deceleration (wrong sign)."""
    w = -1.0
    accel_full = -(1.0 + 3.0 * w)     # sign of -(rho+3p)/... : +2 -> accelerating
    accel_energy_only = -1.0          # uses rho only -> decelerating (wrong)
    return {"w_vacuum": w, "rho_plus_3p_over_rho": 1 + 3 * w,
            "full_tensor_accelerates": accel_full > 0,
            "energy_only_sign": "decelerates (wrong)",
            "note": "pressure of the vacuum is what makes Lambda accelerate; "
                    "the full-tensor source gets the SIGN right automatically"}


def bare_overshoot():
    """Bare BCC zero-point density vs observed Lambda (reuses F164)."""
    I_cc, _ = f164.zero_point_integral(n=160)
    rho_vac = f164.vacuum_energy_density(I_cc, g_star=2)     # J/m^3
    ratio = rho_vac / RHO_LAMBDA_OBS
    return {"I_cc": I_cc, "rho_vac_J_m3": rho_vac,
            "rho_Lambda_obs_J_m3": RHO_LAMBDA_OBS,
            "overshoot_ratio": ratio, "log10_overshoot": float(np.log10(ratio))}


def cancellation_ledger():
    """Candidate cancellations carried over from F164 -- what each would buy and
    whether it is derived.  None reaches the observed value from first
    principles; this is the honest open status."""
    return {
        "boson_fermion_sign": {
            "mechanism": "fermion loops contribute with opposite sign to bosons; "
                         "net depends on the BCC mode content g_*",
            "buys": "could cancel leading quartic if Bose/Fermi DOF balance",
            "derived": False, "issue": "all-fermion content gives the WRONG sign (F164)"},
        "CA_native_tHooft_vacuum": {
            "mechanism": "the discrete 't Hooft-type vacuum reorganises zero-point modes",
            "buys": "leading candidate per F164", "derived": False},
        "F64_sequestering": {
            "mechanism": "the dielectric/conformal structure sequesters the vacuum trace",
            "buys": "removes the trace piece that would gravitate", "derived": False},
        "F69_marginal_binding": {
            "mechanism": "marginal binding of the paired-photon vacuum (F69)",
            "buys": "soft suppression", "derived": False},
    }


def summary():
    return {"equation_of_state": vacuum_equation_of_state(),
            "bare_overshoot": bare_overshoot(),
            "candidates": cancellation_ledger(),
            "status": "full-tensor fixes the dark-energy SIGN (w=-1 accelerates); "
                      "the ~10^120 MAGNITUDE problem (F164) remains open"}
