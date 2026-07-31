"""
Fork F57 — REDUCING THE EINSTEIN–HILBERT TERM FROM LEG-FIELD BACK-REACTION
==========================================================================
Drafted 2026-05-29.  Attempts to DERIVE (not assume) the Sakharov induced
Einstein–Hilbert term that F56 Part B took as given, by computing the matter
back-reaction directly: integrating out the propagating modes generates an
effective action for the metric leg-fields, and the gradient (curvature) piece
of that action IS the EH term.

The set-up
----------
F52/F55 write gravity as two leg-fields the matter modes propagate on:
  • rest leg   √A(x)  — the clock-rate field; couples to the matter energy
    density (the Newtonian potential Φ, with h₀₀ = −2Φ/c²).
  • kinetic leg √(A/B) — the propagation speed; couples to the spatial stress.

When the matter (the F26 Weyl modes) is integrated out, its one-loop effective
action in a slowly-varying background metric is the standard

      W[g] = ½ Tr ln(−□_g + …)  =  ∫ d⁴x √−g [ Λ_ind  +  R/(16πG_ind) + … ].

The coefficient of R — the induced 1/(16πG) — is the gradient response of the
matter vacuum to a metric perturbation, i.e. the q² piece of the matter
stress/density polarization Π(q).  On a lattice this polarization is a FINITE
Brillouin-zone integral (the lattice is a physical UV cutoff — no regulator
freedom), so the coefficient F56 left scheme-ambiguous becomes a definite number
set by the F26 dispersion.

The Newtonian (rest-leg, h₀₀) channel computed here
---------------------------------------------------
Coupling the metric potential Φ to the matter density (the F52 coupling
S_int = ∫ Φ ρ, ρ = T₀₀), the one-loop effective action is
S_eff[Φ] = −½ ∫ Φ(−q) Π(q) Φ(q), with the vacuum static density polarization

      Π(q) = ∫_BZ d³k/(2π)³ · 1/( ω(k) + ω(k+q) )            (ω from F26)

Its small-q expansion  Π(q) = Π(0) − Π₂ q² + …  separates two sectors:
  • Π(0)  — the q=0 value.  This is F56's ∫d³k/(2ω); it scales as Λ² and is the
            VACUUM-ENERGY / cosmological-constant sector, NOT Newton's constant.
  • Π₂    — the gradient coefficient.  This is the graviton KINETIC term: in
            position space S_eff ⊃ ½ Π₂ (∇Φ)², i.e. the induced EH term, with
            1/(16πG_ind) ∝ Π₂.

So the induced Newton constant is Π₂, the gradient response — a refinement of
F56, which had identified the wrong (q=0) object.  The back-reaction GENERATES a
positive (∇Φ)² stiffness ⇒ a propagating, attractive gravitational potential
emerges; gravity is dynamical, not assumed.

What this fork establishes vs leaves open
-----------------------------------------
Established (computable, robust): (i) Π is UV-finite on the lattice — no scheme
freedom; (ii) the back-reaction generates the EH kinetic term Π₂ > 0 (correct
sign, dynamical gravity); (iii) Π(0) ∝ Λ² (Λ sector) and Π₂ runs only
logarithmically — this Newtonian/rest-leg channel reproduces Adler–Zee
running-G, not the quadratic Sakharov estimate.
Open: the quadratic Sakharov piece comes from the SPATIAL-STRESS (kinetic-leg,
F55) channel of the full Tμν Tαβ correlator, not the density channel here; and
the absolute 1/G still needs the gravitating mode count g_* and an IR matching
scale.  So the EH term is reduced to a definite lattice integral + mode count,
not produced as a pure number — but the mechanism is exhibited, not assumed.
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

import ca_bcc as bcc                              # noqa: E402  F26 dispersion ω(k)


# ───────────────────────────────────────────────────────────────────
#  Matter static density polarization  Π(q)  over the F26 dispersion
# ───────────────────────────────────────────────────────────────────

def static_polarization(q_vec, n_grid=96, Lambda=np.pi, spherical=False):
    """Π(q) = ∫_BZ d³k/(2π)³ · 1/(ω(k) + ω(k+q))  on the BCC lattice.

    q_vec      : 3-vector momentum transfer.
    n_grid     : k-grid points per axis over [−Λ, Λ).
    Lambda     : cube half-width (default π = full BZ proxy).
    spherical  : if True, restrict to |k| < Λ (used for cutoff-scaling studies).
    """
    g = np.linspace(-Lambda, Lambda, n_grid, endpoint=False) + Lambda / n_grid
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    w1 = bcc.bcc_dispersion(KX, KY, KZ)
    w2 = bcc.bcc_dispersion(KX + q_vec[0], KY + q_vec[1], KZ + q_vec[2])
    denom = w1 + w2
    integ = np.where(denom > 1e-9, 1.0 / denom, 0.0)
    if spherical:
        kk = np.sqrt(KX**2 + KY**2 + KZ**2)
        integ = np.where(kk < Lambda, integ, 0.0)
    dk = g[1] - g[0]
    return float(integ.sum() * dk**3 / (2.0 * np.pi)**3)


def polarization_gradient_coefficient(n_grid=96, Lambda=np.pi, spherical=False,
                                      qmags=(0.04, 0.08, 0.12, 0.16),
                                      direction=(1.0, 0.0, 0.0)):
    """Fit Π(q) = Π₀ − Π₂ q² along `direction` and return (Π₀, Π₂).

    Π₂ > 0 is the induced graviton/EH kinetic-term coefficient (the gradient
    stiffness of the metric potential):  S_eff ⊃ ½ Π₂ (∇Φ)².
    """
    v = np.asarray(direction, dtype=np.float64)
    v = v / np.linalg.norm(v)
    qs = np.asarray(qmags, dtype=np.float64)
    Pq = np.array([static_polarization(qq * v, n_grid=n_grid, Lambda=Lambda,
                                       spherical=spherical) for qq in qs])
    A = np.vstack([np.ones_like(qs), qs**2]).T
    coef, *_ = np.linalg.lstsq(A, Pq, rcond=None)
    Pi0, neg_Pi2 = coef[0], coef[1]
    return float(Pi0), float(-neg_Pi2)


# ───────────────────────────────────────────────────────────────────
#  Cutoff scaling of the two sectors
# ───────────────────────────────────────────────────────────────────

def cutoff_scaling(Lambdas, n_grid=110, qmags=(0.03, 0.06, 0.09)):
    """For each spherical cutoff Λ, return Π(0;Λ) (the Λ/vacuum-energy sector)
    and Π₂(Λ) (the Newton/EH kinetic sector).  Fits the power-law exponent of
    each: Π(0) ∝ Λ^{p0} (expect ≈ 2) and Π₂ ∝ Λ^{p2} (expect ≪ 2; logarithmic).
    """
    Lambdas = np.asarray(Lambdas, dtype=np.float64)
    P0, P2 = [], []
    for L in Lambdas:
        P0.append(static_polarization((0, 0, 0), n_grid=n_grid, Lambda=L,
                                       spherical=True))
        _, p2 = polarization_gradient_coefficient(n_grid=n_grid, Lambda=L,
                                                   spherical=True, qmags=qmags)
        P2.append(p2)
    P0 = np.array(P0)
    P2 = np.array(P2)
    p0_exp = float(np.polyfit(np.log(Lambdas), np.log(np.abs(P0)), 1)[0])
    p2_exp = float(np.polyfit(np.log(Lambdas), np.log(np.abs(P2)), 1)[0])
    log_slope = float(np.polyfit(np.log(Lambdas), P2, 1)[0])  # Π₂ ~ a ln Λ + b
    return {
        "Lambdas": [float(x) for x in Lambdas],
        "Pi0": [float(x) for x in P0],
        "Pi2": [float(x) for x in P2],
        "Pi0_exponent": p0_exp,
        "Pi2_exponent": p2_exp,
        "Pi2_log_slope": log_slope,
    }


NAME = "fork_F57_induced_eh_from_backreaction"
DESCRIPTION = ("Induced EH term from matter back-reaction: the metric gradient "
               "stiffness Π₂ (graviton kinetic term) emerges with correct sign, "
               "finite on the lattice; Newtonian/rest-leg channel runs "
               "logarithmically (Adler–Zee), distinct from F56's Λ² Π(0).")
