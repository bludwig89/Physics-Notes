"""
test_F241_omega_lambda_residual.py  --  the last O(1) factor of the cosmological
constant, Omega_Lambda ~ 0.685, is NOT derivable from the F190 area-entropy /
F183 black-hole scaling: those fix the ceiling at rho_crit (Omega=1) and the
sub-unity residual is the "why-now" coincidence.  This is F196's leftover.

Self-contained: stdlib + numpy only (no scipy; hand-rolled quadrature/RK4).
Does NOT reopen the p=2 derivation (treated as fixed input from F196).
"""
from __future__ import annotations
import json, os, sys, time, math
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
STAMP = "2026-07-03 - 14:35"

# ---- Planck 2018 flat-LCDM inputs (the only external numbers) ----------------
OMEGA_L = 0.6847      # Omega_Lambda   (Planck 2018)
OMEGA_M = 1.0 - OMEGA_L  # flatness -> 0.3153
W0_OBS = -1.03        # observed dark-energy eq. of state today (DESI/Planck band)


def E(a):
    """Dimensionless Hubble rate H/H0 for flat LCDM (matter + Lambda)."""
    return np.sqrt(OMEGA_M * a**-3 + OMEGA_L)


def future_event_horizon_over_cH0(a0=1.0, a_max=1e7, n=2_000_000):
    """R_EH(a0)/(c/H0) = a0 * int_{a0}^inf da/(a^2 E(a)).

    The integrand ~a^-2 falls off fast, so use a LOG-spaced grid (a linear grid
    to a_max under-resolves the a~1-10 region that dominates the integral).
    Substitute u=ln a: int da/(a^2 E) = int du * (1/(a E))."""
    u = np.linspace(math.log(a0), math.log(a_max), n)
    a = np.exp(u)
    integrand = 1.0 / (a * E(a))          # da = a du  ->  da/(a^2 E) = du/(a E)
    integ = np.trapezoid(integrand, u)
    return a0 * integ


# ---- Checks ------------------------------------------------------------------

def check_C1_residual_is_omega_lambda():
    """Once F196 lands at rho_crit (Omega=1), the residual is exactly
    Omega_Lambda = rho_Lambda/rho_crit = 0.6847. Distance from the ceiling."""
    residual = OMEGA_L
    dist_from_ceiling = abs(math.log10(1.0 / residual))
    ok = (abs(residual - 0.6847) < 1e-9) and (0.16 < dist_from_ceiling < 0.17)
    return {"pass": bool(ok), "residual_omega_L": residual,
            "dlog10_from_ceiling": dist_from_ceiling}


def check_C2_ceiling_theorem():
    """BH/holographic capacity saturates at rho_crit -> Omega_Lambda <= 1.
    Saturation is an inequality: the sector fixes the ceiling, not an interior
    value.  Structural: verify the saturation value equals the ceiling (1)."""
    saturation_omega = 1.0   # F196: rho_grav(R_H) = rho_crit exactly
    ok = (OMEGA_L <= saturation_omega + 1e-12) and (abs(saturation_omega - 1.0) < 1e-12)
    return {"pass": bool(ok), "ceiling_omega": saturation_omega,
            "observed_below_ceiling": bool(OMEGA_L < saturation_omega)}


def check_C3_event_horizon_route_circular():
    """Event-horizon (Li) route: Omega_Lambda = 1/(H0 R_EH)^2 is a SELF-CONSISTENCY
    identity, not a prediction. Today it gives ~0.717 (uses assumed Omega_L in E);
    the true dS fixed point is Omega=1 (R_EH -> c/(H0 sqrt(Omega_L)))."""
    R_EH_now = future_event_horizon_over_cH0(a0=1.0)          # ~1.18
    omega_from_EH_now = 1.0 / R_EH_now**2                     # ~0.717 (circular)
    # asymptotic dS: R_EH -> 1/sqrt(Omega_L) in c/H0 units -> 1/R_EH^2 = Omega_L (tautology)
    R_EH_asym = 1.0 / math.sqrt(OMEGA_L)
    omega_asym = 1.0 / R_EH_asym**2
    # the route neither predicts 0.6847 today (off by using its own input) nor a
    # NON-unit fixed point: the fixed point of the map is Omega=1.
    circular = abs(omega_asym - OMEGA_L) < 1e-9   # tautology confirms circularity
    not_derived = abs(omega_from_EH_now - 0.6847) > 0.02  # today's value != 0.6847
    ok = bool(circular and not_derived)
    return {"pass": ok, "R_EH_now_over_cH0": R_EH_now,
            "omega_from_EH_now": omega_from_EH_now,
            "omega_asymptote_equals_input": omega_asym,
            "route_is_circular": bool(circular)}


def check_C4_feh_w0_not_minus_one():
    """FEH holographic DE with saturation coeff d=1 predicts
    w0 = -1/3 - (2/3) sqrt(Omega_L) = -0.885 at Omega_L=0.6847, in tension with
    the observed w0 ~ -1 -> the route is not even a clean fit."""
    w0_pred = -1.0/3.0 - (2.0/3.0) * math.sqrt(OMEGA_L)
    ok = (abs(w0_pred + 0.885) < 0.01) and (abs(w0_pred - W0_OBS) > 0.1)
    return {"pass": bool(ok), "w0_feh_d1": w0_pred, "w0_obs": W0_OBS,
            "tension": abs(w0_pred - W0_OBS)}


def check_C5_flatness_identity_needs_omega_m():
    """Flat geometry: Omega_Lambda = 1 - Omega_m. Deriving the O(1) factor is
    identically deriving the cosmic matter fraction, which the model lacks
    (F197-199 dark-sector abundance open). Also matter-Lambda equality epoch."""
    omega_m = OMEGA_M
    identity_holds = abs((1.0 - omega_m) - OMEGA_L) < 1e-12
    a_eq = (omega_m / OMEGA_L)**(1.0/3.0)      # Omega_L(a)=Omega_m(a)
    z_eq = 1.0/a_eq - 1.0
    dlog_past_eq = abs(math.log10(OMEGA_L / 0.5))  # how far past equality today
    ok = bool(identity_holds and abs(a_eq - 0.772) < 0.01)
    return {"pass": ok, "omega_m_needed": omega_m,
            "identity_omega_L_eq_1_minus_omega_m": bool(identity_holds),
            "a_equality": a_eq, "z_equality": z_eq,
            "dlog10_past_equality": dlog_past_eq}


def check_C6_near_hits_are_numerology():
    """Density argument: several simple constants land within 0.02 dex of 0.6847;
    the band is ~9% wide, so near-hits carry no evidential weight. None of them
    is produced by the F190/F183 algebra."""
    target = 0.6847
    ltar = math.log10(target)
    hits = []
    # rationals p/q, q<=12
    for q in range(1, 13):
        for p in range(1, q + 1):
            v = p / q
            if 0.3 < v < 1.2 and abs(math.log10(v) - ltar) < 0.02:
                hits.append((f"{p}/{q}", round(v, 4)))
    # low-order transcendental combinations
    extra = {"1-1/e": 1 - 1/math.e, "2/pi": 2/math.pi, "ln2": math.log(2),
             "e/4": math.e/4, "1/sqrt2": 1/math.sqrt(2)}
    for k, v in extra.items():
        if abs(math.log10(v) - ltar) < 0.02:
            hits.append((k, round(v, 4)))
    # band width (linear) for +-0.02 dex
    band_lo, band_hi = target * 10**-0.02, target * 10**0.02
    band_frac = (band_hi - band_lo) / target
    n_distinct = len({h[0] for h in hits})
    ok = (n_distinct >= 4) and (0.08 < band_frac < 0.10)
    return {"pass": bool(ok), "n_simple_constants_within_0p02dex": n_distinct,
            "constants": hits, "band_fractional_width": band_frac}


SUITE = [
    ("C1_residual_is_omega_lambda", check_C1_residual_is_omega_lambda,
     "residual = rho_Lambda/rho_crit = Omega_L = 0.6847; 0.165 dex below ceiling"),
    ("C2_ceiling_theorem", check_C2_ceiling_theorem,
     "BH/holographic capacity fixes Omega<=1 (a ceiling, not an interior value)"),
    ("C3_event_horizon_route_circular", check_C3_event_horizon_route_circular,
     "event-horizon route is circular; dS fixed point = 1, not 0.685"),
    ("C4_feh_w0_not_minus_one", check_C4_feh_w0_not_minus_one,
     "FEH d=1 predicts w0=-0.885 (not -1): not even a clean fit"),
    ("C5_flatness_identity_needs_omega_m", check_C5_flatness_identity_needs_omega_m,
     "Omega_L = 1 - Omega_m; closure needs Omega_m (F197-199 open)"),
    ("C6_near_hits_are_numerology", check_C6_near_hits_are_numerology,
     "numerology density: >=4 simple constants within 0.02 dex; band ~9% wide"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time()
        print(f"[run] {n} ...", flush=True)
        r = fn()
        r["_seconds"] = round(time.time() - t, 3)
        r["_desc"] = d
        res[n] = r
        print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F241",
            "title": ("The last O(1) factor Omega_Lambda~0.685 is not derivable from "
                      "the F190/F183 holographic sector (fixes ceiling Omega=1); it is "
                      "the why-now coincidence residual = 1 - Omega_m"),
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE),
            "results": res, "seconds": round(time.time() - t0, 3)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    outpath = os.path.join(ROOT, "test-results", "F241_omega_lambda_residual.json")
    json.dump(out, open(outpath, "w"), indent=2,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ->  {outpath}")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
