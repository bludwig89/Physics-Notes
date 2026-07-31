# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_qnm.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qnm.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_qnm.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_qnm.py  --  Quasinormal-mode ringdown spectrum (WKB Regge-Wheeler)
=====================================================================

Scenario S4.  The ringdown of the canonical (F178) black hole.  Solves the
axial gravitational (Regge-Wheeler, spin-2) perturbation problem by the WKB
method (Schutz & Will 1985) to predict the quasinormal-mode frequencies, and
compares them to the tabulated GR values (Berti-Cardoso-Will) -- the LIGO/Virgo
ringdown observable.  Also bounds the late-time "echo" amplitude from the
F183 lattice-regulated core, contrasting the F114 horizonless object (order-one
echoes) with the canonical BH (a true horizon -> exponentially small echoes).

Regge-Wheeler potential (geometric units, M):
    V(r) = (1 - 2M/r) [ l(l+1)/r^2 - 6M/r^3 ] ,    dr*/dr = 1 - 2M/r .

WKB-1 (peak of V in the tortoise coordinate r*):
    omega^2 = V0 - i (n + 1/2) sqrt(-2 V0''),   V0'' = d^2V/dr*^2 |_peak .

Self-contained: numpy only.  Date: 2026-06-30 (F187).
"""

from __future__ import annotations

import numpy as np

# tabulated Schwarzschild QNMs (M=1), Berti-Cardoso-Will:  omega = wR - i wI
QNM_TAB = {
    (2, 0): (0.373672, 0.088962),
    (2, 1): (0.346711, 0.273915),
    (3, 0): (0.599443, 0.092703),
    (3, 1): (0.582644, 0.281298),
    (4, 0): (0.809178, 0.094164),
}


def rw_potential(r, l, M=1.0):
    f = 1.0 - 2.0 * M / r
    return f * (l * (l + 1) / r**2 - 6.0 * M / r**3)


def _peak(l, M=1.0):
    """Locate the RW potential maximum (in r) and V0, V0'' (in r*) there."""
    r = np.linspace(2.001 * M, 12.0 * M, 2_000_001)
    V = rw_potential(r, l, M)
    i = int(np.argmax(V))
    r0 = r[i]; V0 = V[i]
    dr = r[1] - r[0]
    f0 = 1.0 - 2.0 * M / r0
    # at the peak dV/dr = 0, so d^2V/dr*^2 = f^2 d^2V/dr^2
    d2V_dr2 = (V[i+1] - 2 * V[i] + V[i-1]) / dr**2
    V0pp_rstar = f0**2 * d2V_dr2
    return r0, V0, V0pp_rstar


def qnm_wkb(l, n=0, M=1.0):
    """WKB-1 quasinormal frequency for mode (l, n)."""
    _, V0, V0pp = _peak(l, M)
    omega2 = V0 - 1j * (n + 0.5) * np.sqrt(-2.0 * V0pp)
    omega = np.sqrt(omega2)
    if omega.real < 0:
        omega = -omega
    return complex(omega.real, -abs(omega.imag))   # convention: damped (Im<0)


def spectrum(M=1.0):
    """WKB spectrum vs tabulated GR for the catalogued modes."""
    out = {}
    for (l, n), (wR, wI) in QNM_TAB.items():
        w = qnm_wkb(l, n, M)
        out[f"l{l}_n{n}"] = {
            "wkb_real": w.real, "wkb_imag": -w.imag,
            "tab_real": wR, "tab_imag": wI,
            "err_real": abs(w.real - wR) / wR,
            "err_imag": abs(-w.imag - wI) / wI,
        }
    return out


def ringdown_waveform(l=2, n=0, M=1.0, t=None):
    """h(t) ~ exp(-t/tau) cos(wR t): the damped sinusoid set by the QNM."""
    w = qnm_wkb(l, n, M)
    if t is None:
        t = np.linspace(0, 80 * M, 2000)
    tau = 1.0 / abs(w.imag)
    h = np.exp(-t / tau) * np.cos(w.real * t)
    Q = 0.5 * w.real / abs(w.imag)            # quality factor
    return {"t": t, "h": h, "tau_ringdown_M": tau, "quality_factor": Q,
            "f_real_per_M": w.real}


def echo_amplitude_bound(M_solar=1.0):
    """Order-of-magnitude bound on the late-time echo amplitude from the F183
    lattice core.  For a horizonless reflector at proper depth set by the cell
    scale, the near-horizon potential barrier transmits with probability
    ~ exp(-2 pi b_c omega) per traversal; with omega ~ 1/M (geometric) and the
    core at r_core << r_h, the round-trip transmission (hence echo amplitude) is
    suppressed by the enormous logarithmic depth -> effectively zero, unlike the
    F114 horizonless object whose echoes are order one."""
    # geometric barrier suppression for the fundamental mode (illustrative)
    wM = 0.3737                                # |omega| M (l=2 n=0)
    supp = np.exp(-2.0 * np.pi * 3.0 * np.sqrt(3.0) * wM)   # exp(-2 pi b_c omega)
    return {"single_barrier_transmission_~": float(supp),
            "echo_regime": "exponentially suppressed (true horizon present)",
            "contrast_F114": "F114 horizonless -> order-one echoes; canonical BH -> none detectable",
            "note": "a real LIGO/Virgo bound requires a Teukolsky solve; this is the qualitative scale"}
