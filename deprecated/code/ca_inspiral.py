# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_inspiral.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/inspiral.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_inspiral.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_inspiral.py  --  Compact-binary inspiral & GW phasing (post-Newtonian)
=========================================================================

Scenario S6.  The two-body / gravitational-wave sector of the F178 gravity
model.  The graviton speed is already fixed to c_lat = c_photon (F180); here we
build the leading-order (quadrupole / 0PN) inspiral: the chirp-mass-driven
frequency sweep, the time to merger, and the GW150914-like waveform, against
which the model makes standard-GR predictions.

Quadrupole results (geometric G=c=1; SI conversions provided):
    chirp mass  Mc = (m1 m2)^{3/5} / (m1+m2)^{1/5}
    df/dt = (96/5) pi^{8/3} Mc^{5/3} f^{11/3}            (GW frequency f = 2 f_orb)
    time to merger from f:  tau = (5/256) Mc^{-5/3} (pi f)^{-8/3}
    strain amplitude  h ~ (4/D)(pi f)^{2/3} Mc^{5/3}

Self-contained: numpy + a local RK4.  Date: 2026-06-30 (F189).
"""

from __future__ import annotations

import numpy as np
from casim.constants import G_CODATA as _G_CODATA, c_SI as _c_SI

G = _G_CODATA; C = _c_SI
MSUN = 1.98892e30; MPC = 3.0856775814913673e22
T_SUN = G * MSUN / C**3          # solar mass in seconds (geometric) = 4.925e-6 s


def chirp_mass_solar(m1, m2):
    return (m1 * m2) ** 0.6 / (m1 + m2) ** 0.2


def df_dt(f, Mc_solar):
    """GW-frequency chirp rate df/dt (Hz/s) at frequency f (Hz)."""
    Mc = Mc_solar * T_SUN                     # seconds
    return (96.0 / 5.0) * np.pi ** (8.0 / 3.0) * Mc ** (5.0 / 3.0) * f ** (11.0 / 3.0)


def time_to_merger(f, Mc_solar):
    """Coalescence time from GW frequency f (Hz) -> seconds (0PN)."""
    Mc = Mc_solar * T_SUN
    return (5.0 / 256.0) * Mc ** (-5.0 / 3.0) * (np.pi * f) ** (-8.0 / 3.0)


def isco_gw_frequency(M_total_solar):
    """GW frequency at the Schwarzschild ISCO of the total mass (Hz):
    f_GW = 2 f_orb = (1/pi) (1/6^{3/2}) / (G M/c^3)."""
    M = M_total_solar * T_SUN
    f_orb = (1.0 / (2.0 * np.pi)) * 6.0 ** (-1.5) / M
    return 2.0 * f_orb


def evolve_chirp(m1, m2, f_start=35.0, f_end=None):
    """Integrate f(t) from f_start to the ISCO frequency; return t, f, and the
    quadrupole waveform h(t) ~ amplitude(f) cos(phase)."""
    Mc = chirp_mass_solar(m1, m2)
    if f_end is None:
        f_end = isco_gw_frequency(m1 + m2)
    f = f_start; t = 0.0
    ts, fs = [t], [f]
    dt = 1e-4
    while f < f_end:
        k1 = df_dt(f, Mc)
        k2 = df_dt(f + dt/2 * k1, Mc)
        k3 = df_dt(f + dt/2 * k2, Mc)
        k4 = df_dt(f + dt * k3, Mc)
        f = f + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
        t += dt
        ts.append(t); fs.append(min(f, f_end))
    ts = np.array(ts); fs = np.array(fs)
    # phase = integral 2 pi f dt
    phase = np.concatenate([[0], np.cumsum(0.5 * (fs[1:] + fs[:-1]) * np.diff(ts))]) * 2 * np.pi
    amp = (np.pi * fs) ** (2.0 / 3.0) * (Mc * T_SUN) ** (5.0 / 3.0)
    h = amp * np.cos(phase)
    return {"t": ts, "f": fs, "h": h, "Mc_solar": Mc,
            "f_isco_Hz": f_end, "duration_s": float(ts[-1])}


def gw150914():
    """Canonical-source check against GW150914 (m1=36, m2=29 M_sun)."""
    m1, m2 = 36.0, 29.0
    Mc = chirp_mass_solar(m1, m2)
    f_isco = isco_gw_frequency(m1 + m2)
    tau = time_to_merger(35.0, Mc)            # from 35 Hz GW frequency
    ev = evolve_chirp(m1, m2, f_start=35.0)
    return {"Mc_solar": Mc, "f_isco_Hz": f_isco,
            "time_from_35Hz_s": tau, "evolved_duration_s": ev["duration_s"],
            "M_total": m1 + m2}
