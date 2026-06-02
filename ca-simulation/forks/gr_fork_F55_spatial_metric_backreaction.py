"""
Fork F55 — SOURCING THE SPATIAL METRIC: EINSTEIN'S FACTOR-2 FROM TRACE REVERSAL
===============================================================================
Drafted 2026-05-29.  Companion to F52; promotes the loop from Newton to Einstein.

Where F52 left off
------------------
F52 closed the F50 loop for the REST leg: a clock-rate field sourced directly by
rest-mass density (∇²Φ = 4πGρ) reproduces the imported lapse √A and gives the
correct factor-1 redshift.  But it also proved that sourcing ONLY the rest/clock
leg (spatial metric B ≡ 1) gives the Newtonian deflection 2GM/(bc²) — factor 1.
The missing half of the light bending is the part of the metric the rest leg
never touches: the spatial metric B (the kinetic-leg renormalisation
c_eff = c₀√(A/B)).

The F55 hypothesis
------------------
Source B from the SAME mass density via the linearised Einstein equation, and
ask whether Einstein's factor-2 emerges self-consistently (not imposed).

The principled mechanism is the TRACE REVERSAL.  Linearised Einstein in Lorenz
gauge is  □ h̄_μν = −(16πG/c⁴) T_μν,  with h̄_μν = h_μν − ½η_μν h̄ the
trace-reversed perturbation.  A STATIC DUST source has only T₀₀ = ρc² — its
spatial stress T_ij = 0.  Naïvely the spatial metric should not be sourced at
all.  But the trace reversal feeds the temporal source back into the spatial
components:

    ∇² h̄₀₀ = −4 ∇²φ/c²           (from T₀₀ = ρc², ∇²φ = 4πGρ)   ⇒  h̄₀₀ = −4φ/c²
    h̄ = η^μν h̄_μν = −h̄₀₀ = 4φ/c²
    h₀₀ = h̄₀₀ − ½η₀₀h̄ = −2φ/c²
    h_ij = h̄_ij − ½η_ij h̄ = −2φ/c² δ_ij        ←  EQUAL to h₀₀, although T_ij = 0

So the trace reversal forces  h_ij = h₀₀.  Reading off the metric
(g_μν = η_μν + h_μν, η = diag(−1,1,1,1)):

    A ≡ −g₀₀ = 1 + 2φ/c² = 1 − 2u
    B ≡  g_ii = 1 − 2φ/c² = 1 + 2u ,        u ≡ −φ/c² = GM/(rc²)

which is exactly the gr_fork_E_tensor *linearised* metric — but here DERIVED from
a single mass-sourced scalar plus the trace-reversal identity, not posited.  The
equality |B−1| = |A−1| is the extra factor-1 that turns the rest-leg's Newtonian
2GM/(bc²) into Einstein's 4GM/(bc²).

What this fork exposes
----------------------
    newtonian_potential(rho, G)                  Φ : ∇²Φ = 4πGρ  (reuses F52)
    trace_reversed_perturbation(phi, c_0)        dict h̄₀₀, h₀₀, h_ij  (explicit)
    metric_trace_reversed(phi, c_0)              (A, B) from the trace reversal
    metric_spatial_fraction(phi, c_0, lam)       A fixed, B carries fraction λ of
                                                 the trace-reversed spatial dev
                                                 (λ=0 → F52 rest-only; λ=1 → GR)
    eikonal_deflection_AB(A_slice, B_slice, …)   weak-field deflection from (A,B)

The λ knob is the uniqueness test: the eikonal coefficient is K(λ) = 2(1+λ), so
ONLY the trace-reversal value λ = 1 gives Einstein's factor-2.  The model is not
free to give any answer — factor-2 is selected by the trace reversal.

What is derived vs posited
--------------------------
Posited (a stronger input than F52's scalar): the linearised Einstein equation
with the 16πG/c⁴ tensor coupling and Lorenz gauge.  Derived/tested: that this,
applied to a static-dust source, forces h_ij = h₀₀ by trace reversal (J1), keeps
the redshift at factor-1 (J2), and makes the deflection factor-2 emerge — uniquely
at the trace-reversal coefficient (J3, J4) — self-consistently from ρ.
"""

from __future__ import annotations

import os
import sys

import numpy as np

_THIS = os.path.dirname(__file__)
if _THIS not in sys.path:
    sys.path.insert(0, _THIS)
_SIM = os.path.abspath(os.path.join(_THIS, ".."))
if _SIM not in sys.path:
    sys.path.insert(0, _SIM)

import gr_fork_F52_restleg_backreaction as f52    # noqa: E402  (Poisson + rest leg)
import gr_fork_E_tensor as forkE                  # noqa: E402  (linearised x-check)


# ───────────────────────────────────────────────────────────────────
#  The single mass-sourced potential (same field as F52)
# ───────────────────────────────────────────────────────────────────

def newtonian_potential(rho, G=1.0):
    """Φ solving ∇²Φ = 4πG ρ from rest-mass density directly (reuses F52)."""
    return f52.restleg_potential_fft(rho, G=G)


# ───────────────────────────────────────────────────────────────────
#  Trace reversal: static dust → equal temporal & spatial perturbations
# ───────────────────────────────────────────────────────────────────

def trace_reversed_perturbation(phi, c_0):
    """Explicit linearised trace reversal for a STATIC DUST source.

    Returns a dict with the trace-reversed temporal source h̄₀₀, its trace h̄,
    and the physical metric perturbations h₀₀ and h_ij (spatial diagonal).  The
    point: h_ij comes out EQUAL to h₀₀ even though the spatial stress T_ij = 0.
    """
    phi = np.asarray(phi, dtype=np.float64)
    over_c2 = 1.0 / c_0**2
    hbar00 = -4.0 * phi * over_c2                 # ∇²h̄₀₀ = -4∇²φ/c²
    hbar_trace = -hbar00                          # h̄ = η^μν h̄_μν = -h̄₀₀
    # h_μν = h̄_μν - ½ η_μν h̄ ;  η = diag(-1,1,1,1)
    h00 = hbar00 - 0.5 * (-1.0) * hbar_trace      # = -2φ/c²
    hij = 0.0 - 0.5 * (1.0) * hbar_trace          # = -2φ/c²  (h̄_ij = 0)
    return {"hbar00": hbar00, "hbar_trace": hbar_trace, "h00": h00, "hij": hij}


def metric_trace_reversed(phi, c_0):
    """(A, B) with g₀₀ = -A, g_ii = B, derived from the trace reversal:
        A = 1 + h₀₀ ... wait: A ≡ -g₀₀ = -(η₀₀ + h₀₀) = 1 - h₀₀ ... see below.
    Using η₀₀ = -1, η_ii = +1:
        g₀₀ = -1 + h₀₀ ⇒ A = -g₀₀ = 1 - h₀₀ = 1 + 2φ/c² = 1 - 2u
        g_ii = 1 + h_ij ⇒ B = 1 + h_ij = 1 - 2φ/c² = 1 + 2u
    """
    tr = trace_reversed_perturbation(phi, c_0)
    A = 1.0 - tr["h00"]        # = 1 + 2φ/c²
    B = 1.0 + tr["hij"]        # = 1 - 2φ/c²
    return A, B


def metric_spatial_fraction(phi, c_0, lam):
    """Rest leg (A) fully sourced; spatial metric B carries a *fraction* λ of the
    trace-reversed spatial perturbation.

        λ = 0  →  B = 1                (F52 rest-leg-only; Newtonian factor-1)
        λ = 1  →  B = trace-reversed   (GR; Einstein factor-2)

    Used as the uniqueness knob: K(λ) = 2(1+λ).
    """
    A, B_full = metric_trace_reversed(phi, c_0)
    B = 1.0 + lam * (B_full - 1.0)
    return A, B


# ───────────────────────────────────────────────────────────────────
#  Eikonal deflection from an explicit (A, B) slice
# ───────────────────────────────────────────────────────────────────

def refractive_index_AB(A, B, c_0):
    """n = c₀ / c_eff with c_eff = c₀√(A/B)  ⇒  n = √(B/A)."""
    A = np.abs(np.asarray(A, dtype=np.float64))
    B = np.asarray(B, dtype=np.float64)
    return np.sqrt(B / A)


def eikonal_deflection_AB(A_slice, B_slice, c_0, axis_long=0, axis_perp=1,
                          impact_index=None, window=None):
    """Weak-field eikonal deflection α = −∫ ∂_⊥ n  dl through a 2D (A,B) slice.

    For n − 1 = κ u  (u = GM/rc²) this evaluates to α = 2κ GM/(b c₀²), so the
    coefficient K ≡ α b c₀²/GM reads off 2κ:  rest-only (B=1) → 2, GR → 4.
    """
    n = refractive_index_AB(A_slice, B_slice, c_0)
    dn = np.gradient(n, axis=axis_perp)
    Lperp = n.shape[axis_perp]
    if impact_index is None:
        impact_index = Lperp // 2 + 6
    sl = [slice(None), slice(None)]
    sl[axis_perp] = impact_index
    dn_line = dn[tuple(sl)]
    Llong = dn_line.shape[0]
    if window is None:
        lo, hi = 0, Llong
    else:
        c = Llong // 2
        lo, hi = max(0, c - window), min(Llong, c + window)
    return float(-np.sum(dn_line[lo:hi]))


# ───────────────────────────────────────────────────────────────────
#  Harness drop-in
# ───────────────────────────────────────────────────────────────────

NAME = "fork_F55_spatial_metric_backreaction"
DESCRIPTION = ("Spatial metric B sourced from mass via linearised trace "
               "reversal; h_ij = h₀₀ for static dust turns the rest-leg's "
               "Newtonian factor-1 deflection into Einstein's factor-2.")
