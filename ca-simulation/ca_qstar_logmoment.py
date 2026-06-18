"""
ca_qstar_logmoment.py — Residual A of the strong-sector scale problem:
a FIRST-PRINCIPLES estimate of the matching scale q* (the one piece F151 left
"implied" by the PDG match).

F151 reduced the rule->MSbar scheme constant to:  Delta(1/alpha)=0.640 =
a1(6)/4pi (=0.292, EXACT) + 2 b0^alpha ln(1/(q* a)) (=0.348), with the data
implying q* = 0.733/a inside a derived geometric band [1/sqrt3, 1]/a. F151 did
not COMPUTE q* — it bisected it to match alpha_s(M_Z).

q* is the BLM / Lepage-Mackenzie scale of the one-loop coupling: the bare lattice
coupling equals the V-scheme running coupling at the typical loop momentum, i.e.
the log-moment of the gluon propagator over the Brillouin zone. The rule's lock
is TADPOLE-FREE (F151 S2), so the matching constant is just this propagator
log-moment (no compact-link Z0 term). We compute it directly:

    ln(q*^2 a^2) = < ln K_hat(q) >_w  ,    q* a = exp( 1/2 <ln K_hat>_w )

over the BZ with K_hat(q) = sum_i 2(1-cos q_i) (the rule's gluon kinetic kernel,
small-q -> q^2), for several principled weights w:
    flat      : the bare BZ log-moment (Symanzik/perfect-action leading term)
    prop 1/K  : propagator-weighted (the static-potential / V-scheme integrand)
both in 3D (the static-potential Coulomb is spatial) and 4D.

This is the LEADING (propagator-moment) term of the tadpole-free constant; the
full vertex-resolved one-loop self-energy is the residual. We report each scale,
whether it lands in F151's band, and the deviation from the implied 0.733/a.

Pure numpy.
"""
from __future__ import annotations

import math

import numpy as np

import ca_scheme_constant as sc   # F151: a1, band, implied_qstar

SQRT3 = math.sqrt(3.0)
BAND = (1.0 / SQRT3, 1.0)         # F151 q* band in units of 1/a
GEOM_MEAN_BAND = 3.0 ** (-0.25)   # 0.7598, geometric mean of the band


def _Khat(n: int, d: int) -> np.ndarray:
    """Lattice gluon kernel sum_i 2(1-cos q_i) on a d-dim BZ grid, q=0 excluded."""
    ax = (np.arange(n) + 0.5) / n * 2 * math.pi - math.pi   # midpoint, avoids q=0
    grids = np.meshgrid(*([ax] * d), indexing="ij")
    K = sum(2 * (1 - np.cos(g)) for g in grids)
    return K


def logmoment_qstar(n: int = 64, d: int = 3, weight: str = "flat") -> dict:
    """q* a = exp(1/2 < ln K >_w)."""
    K = _Khat(n, d)
    lnK = np.log(K)
    if weight == "flat":
        w = np.ones_like(K)
    elif weight == "prop":          # propagator 1/K  (static-potential integrand)
        w = 1.0 / K
    elif weight == "prop2":         # 1/K^2  (vacuum-polarisation-like)
        w = 1.0 / K ** 2
    else:
        raise ValueError(weight)
    mean_lnK = float(np.sum(w * lnK) / np.sum(w))
    qstar_a = math.exp(0.5 * mean_lnK)
    return {"d": d, "weight": weight, "n": n, "mean_lnK": mean_lnK,
            "qstar_a": qstar_a, "in_band": BAND[0] <= qstar_a <= BAND[1]}


def report(n: int = 64) -> dict:
    implied = sc.implied_qstar()
    scales = {}
    for d in (3, 4):
        for w in ("flat", "prop", "prop2"):
            scales[f"d{d}_{w}"] = logmoment_qstar(n=n, d=d, weight=w)
    # which is closest to the implied q*?
    best = min(scales.values(), key=lambda s: abs(s["qstar_a"] - implied))
    return {
        "implied_qstar_a_F151": implied,               # 0.733 (PDG match)
        "band": BAND, "geom_mean_band": GEOM_MEAN_BAND,
        "a1_6_exact": sc.a1(6),
        "logmoment_scales": scales,
        "closest_to_implied": {"key": [k for k, v in scales.items()
                                       if v is best][0],
                               "qstar_a": best["qstar_a"],
                               "dev_vs_implied_%": 100 * (best["qstar_a"] / implied - 1)},
        "all_in_band": all(s["in_band"] for s in scales.values()),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
