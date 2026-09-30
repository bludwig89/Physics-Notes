#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qi_cluster_asymptotic_series.py — F380: naming F331's residual as ONE object
=============================================================================

completeness row A10 (cluster decomposition), QUANT -> PARTIAL.

2026-09-10 - 00:xx  (mechanism corrected 2026-09-10 - 11:xx, post review — see
findings/F380-cluster-asymptotic-series-residual-named.md "Reviewed & corrected")

THE QUESTION.  F331 closed F290's residual 1 (interacting, 3-D cluster
decomposition) but left its own Piece 1 residual as a TABLE: the measured/
exact ratio of the (100)-axis decay rate kappa_100(m) shrinks monotonically
from 1.53 at m=0.05 to 0.95 at m=0.95 (F331 Sec.1 table).  That is a
mass-dependent TOLERANCE, not a named object -- the QUANT->PARTIAL rung
(`.claude/commands/state-of-model.md` Sec.7.1) requires exactly that
demotion: "turn 'agrees to x%' into 'derived up to this one object'".

FIRST STEP TAKEN.  Evaluate F331's own (unmodified) `axis100_measured_kappa`
at the mass the self-consistent NJL gap equation actually selects
(m*=0.6055 for g=2.9, F331 Sec.2) instead of the registry default m=0.5.
Result: ratio(m*) = 1.1096, L-converged -- NOT 1 to the numerical floor.  So
the first-step hypothesis in its literal form (m* is special and collapses
the ratio) is FALSIFIED.  What is found instead is more useful: m* is
UNREMARKABLE -- just another point on the same curve as every other mass in
F331's table (see below), which is what lets the whole table collapse to
one object.

THE MECHANISM.  F331's `_fit_kappa` fits a PURE exponential,
ln|C(r)| = a - kappa*r, to the model's own periodic (100)-axis correlator.
A 3-D lattice Green's function does not decay as a pure exponential, and TWO
independent effects contribute an algebraic prefactor r^{-p} on top of it:

  (i) TRANSVERSE (stationary phase).  Near the dominant saddle (b,c)=(0,0)
      the pole-locus R(b,c)^2 = 1-b^2-c^2+2*b^2*c^2 is quadratic to leading
      order, so Gaussian-integrating the 2 real transverse momenta
      contributes r^{-2/2} = r^{-1}.

  (ii) AXIAL (branch-point, not a simple pole -- CORRECTED 2026-09-10).  The
      earlier version of this module claimed the axial direction supplies no
      further power ("same structure as the continuum static Yukawa
      propagator e^{-kappa r}/r", p=1 total).  This was WRONG, caught by
      this finding's own review-finding pass: the model's dispersion is
      omega(a) = arccos(n*u(a)), and AT the pole condition n*u(a)=1 the
      dispersion vanishes as a SQUARE ROOT, omega(a0+eps) ~ sqrt(2*eps)
      (arccos(1-eps) ~ sqrt(2*eps) for small eps), NOT linearly -- i.e. the
      propagator 1/(2*omega) has an inverse-square-root BRANCH POINT at the
      pole, not a simple pole.  A 1-D Fourier transform of a
      (k-k0)^{-alpha} branch-point singularity contributes r^{alpha-1} by
      Watson's-lemma endpoint asymptotics (a simple pole, alpha=1, gives
      r^0 -- no extra power, which is the continuum-Yukawa case and is NOT
      this model's case); here alpha=1/2, contributing an EXTRA r^{-1/2}.

  TOTAL: p = 1 (transverse) + 1/2 (axial branch point) = 3/2, not p=1.
  Verified independently in this finding's review pass three ways: (a) a
  cold blind-rederivation subagent reached p=3/2 from the dispersion's own
  functional form without reading this module; (b) a direct numerical
  power-law fit (kappa fixed to the exact closed form, p left free) on wide
  windows at L=512 gives p_fit in [1.48, 1.52] across m=0.1-0.5; (c) the
  OLS-exact bias formula below (no free fit at all) gives a mean effective
  power of 1.489 +/- 0.039 across the WHOLE admissible mass range, 0.7% off
  the theoretical 3/2.

THE MEASUREMENT.  A free-power 3-parameter refit (fitting a, kappa AND the
prefactor power simultaneously) was tried and rejected: numerically
ill-conditioned on F331's short adaptive windows (as few as 3 points at the
high-mass end).  What replaces it is not a floating fit at all -- it is the
EXACT, closed-form OLS bias that a KNOWN, theoretically fixed power p
produces in a plain 2-parameter (a, kappa) linear fit of ln|C(r)| against r:
if the true model is ln|C(r)| = const - p*ln(r) - kappa*r, then the OLS
slope of a plain linear fit (which omits the -p*ln(r) term) is biased by
EXACTLY

    kappa_measured - kappa_exact = p * S_{r,ln r} / S_{rr}

where S_{rr} = sum((r_i-rbar)^2) and S_{r,ln r} = sum((r_i-rbar)(ln r_i -
ln r bar)) over the SAME window F331's own `_adaptive_window` already uses
-- no new fit, no free parameter, just linear-regression bookkeeping applied
to F331's existing numbers.  Solving for the IMPLIED effective power,

    p_eff(m) := (kappa_measured(m) - kappa_exact(m)) * S_{rr} / S_{r,ln r}

should equal the theoretical p=3/2 if the mechanism above is the whole
story (to the order this leading-term analysis captures).

RESULT (measured, `test-results/F380_cluster_asymptotic_series.json`):

    p_eff = 1.489 +/- 0.039   (2.65% relative spread), m in [0.05, 0.90], L=256
    p_eff(m*=0.6055) = 1.465  (z = -0.62 sigma from the scan mean)
    theory: p = 3/2 = 1.500   (mean deviates from theory by 0.71%)

against the raw ratio's own relative spread of 7.6% (mean 1.161, same 18
masses) -- p_eff is a 2.9x tighter descriptor, AND it lands within
measurement scatter of an independently, first-principles-derived number,
which the earlier (wrong-mechanism, crude r_mid-proxy) version of this
module did not achieve: its own K=1.71 had no independent theoretical
anchor to be checked against.  m* sits comfortably inside the p_eff
distribution (z=-0.62), unremarkable -- the promised payoff of the "first
step": m* needs no special treatment, because the WHOLE table (m* included)
is one object.  Control: replacing the reference closed form with the WRONG
one (`axis110_kappa_exact`, correct for a different axis) breaks p_eff's
stability outright (mean shifts to 5.10, far from 1.5; relative spread
33.6%) -- p_eff's meaning is tied to the specific closed form
`axis100_kappa_exact` being measured, not a generic artifact of the
S_{r,ln r}/S_{rr} rescaling.

WHAT THIS PROMOTES.  Row A10's Piece-1 residual is no longer an opaque
18-entry tolerance table; it is ONE named quantity -- the algebraic-prefactor
power p_eff = 1.49 +/- 0.04, matching a theoretically DERIVED value (3/2,
from the dispersion's own branch-point structure) to under 1%, verified
mass-independent across the entire admissible range including the
dynamically NJL-selected mass.  QUANT -> PARTIAL is exactly this move
(state-of-model.md Sec.7.1): "a named seam is strictly more informative than
a tolerance, even at the same number."

WHAT THIS DOES NOT CLOSE (PARTIAL, not MACHINE).  p_eff=1.489 is MEASURED
against a THEORETICALLY DERIVED target (3/2) -- the derivation in (ii) above
is a leading-order Puiseux/Watson's-lemma argument, not yet a full symbolic
(sympy) computation of the sub-leading term that would explain the
remaining ~1% mean offset and the ~2.6% point-to-point scatter, and not yet
verified to the numerical floor.  That full symbolic derivation is the next
rung (PARTIAL -> MACHINE), named as real remaining work, not performed here.
This module also does not touch F290's separate 1-D exponent shortfall (its
own item 2, untouched by F331 and by this finding) or S-matrix-level
clustering (item 3) -- both stay open, as F331 already disclosed.

Run standalone:  python3 -m casim.engine.interactions.qi_cluster_asymptotic_series
"""
from __future__ import annotations

import math
from typing import Any, Dict, List

from casim.numerics import xp as np
from casim.engine.interactions.qi_cluster_interacting_3d import (
    ROOT3,
    axis100_kappa_exact,
    axis110_kappa_exact,
    axis100_measured_kappa,
    solve_gap_equation,
)

_STEP_PHYS = 4.0 / ROOT3          # matches _AXIS100_STEP_PHYS in qi_cluster_interacting_3d
_SCAN_MASSES = tuple(round(0.05 + 0.05 * i, 2) for i in range(18))   # 0.05 .. 0.90
THEORY_POWER = 1.5                # transverse (1) + axial branch point (1/2), see module docstring


def _ols_bias_weight(lo: int, hi: int, step_phys: float) -> float:
    """S_{r,ln r} / S_{rr} over F331's own fit-window indices [lo, hi) --
    the EXACT (not leading-order-approximate) weight by which an OLS linear
    fit of ln|C(r)| = a - kappa*r is biased per unit of an omitted
    -p*ln(r) term in the true model.  See module docstring: this is
    ordinary linear-regression bookkeeping, not a new numerical method.
    """
    idx = np.arange(lo, hi, dtype=float)
    r = idx * step_phys
    lnr = np.log(r)
    rbar, lnrbar = r.mean(), lnr.mean()
    s_rr = float(np.sum((r - rbar) ** 2))
    s_r_lnr = float(np.sum((r - rbar) * (lnr - lnrbar)))
    return s_r_lnr / s_rr


def effective_power(m: float, L: int = 256, use_correct_bz: bool = True,
                    reference: str = "axis100") -> Dict[str, Any]:
    """p_eff(m) = (kappa_measured - kappa_reference) / (S_{r,ln r}/S_{rr}),
    built entirely from F331's own unmodified `axis100_measured_kappa` --
    no new fit machinery, just its exact OLS bias re-expressed as an
    implied power.  `reference="axis110"` is the CONTROL: the closed form
    correct for a *different* BCC axis, used deliberately wrong here to
    show p_eff's meaning is tied to the right closed form, not an artifact
    of the S_{r,ln r}/S_{rr} rescaling by itself.
    """
    meas = axis100_measured_kappa(m, L=L, window=None, use_correct_bz=use_correct_bz)
    lo, hi = meas["window"]
    weight = _ols_bias_weight(lo, hi, _STEP_PHYS)
    kappa_ref = meas["kappa_exact"] if reference == "axis100" else axis110_kappa_exact(m)
    kmeas = meas["kappa_measured"]
    p_eff = ((kmeas - kappa_ref) / weight) if (math.isfinite(kmeas) and weight) else float("nan")
    ratio = (kmeas / kappa_ref) if (kappa_ref and math.isfinite(kmeas)) else float("nan")
    return {"m": float(m), "L": L, "window": meas["window"],
            "kappa_measured": kmeas, "kappa_exact_100": meas["kappa_exact"],
            "kappa_reference": kappa_ref, "reference": reference,
            "ols_weight": weight, "p_eff": p_eff, "ratio": ratio}


def scan_p_eff(masses=_SCAN_MASSES, L: int = 256, reference: str = "axis100") -> List[Dict[str, Any]]:
    return [effective_power(m, L=L, reference=reference) for m in masses]


# ======================================================================
# The registry entry point
# ======================================================================
def check_named_residual_K(reference: str = "axis100",
                           g_above_gc: float = 2.9, n_mc: int = 20000,
                           seed: int = 0, L: int = 256) -> Dict[str, Any]:
    """The F380 gate.

    Declared control: ``--param reference=axis110`` -- measure p_eff against
    the closed form for the WRONG BCC axis (correct for (110), not (100)).
    p_eff's stability and its match to the theoretical power both collapse
    (relative spread far above the declared 5% band; mean far from 1.5),
    showing p_eff's meaning is a property of measuring against
    `axis100_kappa_exact` specifically, not a generic consequence of the
    OLS-bias rescaling.
    """
    checks: List[tuple] = []

    rows = scan_p_eff(_SCAN_MASSES, L=L, reference=reference)
    p_eff = np.array([r["p_eff"] for r in rows], dtype=float)
    ratio = np.array([r["ratio"] for r in rows], dtype=float)
    p_mean, p_std = float(p_eff.mean()), float(p_eff.std())
    ratio_mean, ratio_std = float(ratio.mean()), float(ratio.std())
    p_rel = (p_std / abs(p_mean)) if p_mean else float("inf")
    ratio_rel = (ratio_std / abs(ratio_mean)) if ratio_mean else float("inf")

    ok1 = math.isfinite(p_rel) and p_rel < 0.05
    checks.append(("C1 p_eff relative spread < 5% across the full admissible "
                   "mass range (0.05<=m<=0.90)", ok1, p_rel))

    theory_dev = abs(p_mean - THEORY_POWER) / THEORY_POWER if math.isfinite(p_mean) else float("nan")
    ok2 = math.isfinite(theory_dev) and theory_dev < 0.05
    checks.append(("C2 p_eff mean matches the theoretical branch-point+"
                   "transverse power p=3/2 to <5%", ok2, theory_dev))

    gap = solve_gap_equation(g_above_gc, n_mc=n_mc, seed=seed)
    if gap["nontrivial"]:
        star = effective_power(gap["m_star"], L=L, reference=reference)
        z = (abs(star["p_eff"] - p_mean) / p_std) if p_std > 0 else float("inf")
        ok3 = math.isfinite(z) and z < 3.0
    else:
        star, z, ok3 = None, float("nan"), False
    checks.append(("C3 p_eff at the dynamically-selected NJL mass m* is "
                   "unremarkable (within 3 sigma of the scan)", ok3, z))

    rows_out = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows_out,
            "passed": all(r["ok"] for r in rows_out),
            "n_pass": sum(1 for r in rows_out if r["ok"]),
            "n_total": len(rows_out),
            "params": {"reference": reference, "g_above_gc": g_above_gc,
                      "n_mc": n_mc, "seed": seed, "L": L},
            "summary": {
                "F380_p_eff_mean": p_mean, "F380_p_eff_std": p_std,
                "F380_p_eff_rel_spread": p_rel,
                "F380_theory_power": THEORY_POWER,
                "F380_theory_deviation": theory_dev,
                "F380_ratio_mean": ratio_mean, "F380_ratio_rel_spread": ratio_rel,
                "F380_m_star": gap.get("m_star"),
                "F380_p_eff_at_m_star": (star["p_eff"] if star else None),
                "F380_z_at_m_star": z,
                "F380_ratio_at_m_star": (star["ratio"] if star else None),
            }}


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_named_residual_K()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F380_cluster_asymptotic_series.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("wrote", os.path.basename(out))
