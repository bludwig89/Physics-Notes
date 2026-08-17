"""
run_Q3_omega_degeneracy.py — Q3: is the absolute g_omegaNN deuteron-observable?
================================================================================

Open-derivation Q3 (open-derivations-prompts-v2.md). F240 derived the omega
channel's sign, mass (m_omega=m_rho), and g_omegaNN/g_rhoNN=3 ratio (Tier-1), and
the vector-universality chain predicts g_omegaNN^2/4pi = 25.9 -- which OVERSHOOTS
(unbinds the deuteron). The NN-required value is a bracket [5.4, 11.1].

This runner tests WHY g_omegaNN cannot be pinned: the deuteron constrains only the
TOTAL short-range repulsion = (F113 quark-Pauli core, strength g_cm) + (omega). It
maps the (g_cm, g_omega*) binding valley: for each core strength g_cm, the omega
coupling g_omega* that binds the deuteron to E_b = 2.224 MeV. A flat valley =>
g_omega is degenerate with the core strength => not separately deuteron-observable.

Also reports the route-A prediction at the N-Delta-DERIVED core g_cm = 18.31 MeV.

Emits test-results/Q3_omega_degeneracy.json. Runtime ~1-2 min at N=500.
Run:  python3 run_Q3_omega_degeneracy.py
"""
import json

from casim.numerics import xp as np                # D8: no bare numpy import
from casim.engine.particles import nuclear as nuc
from casim.engine.particles._results_path import results_path

TARGET = 2.224          # MeV, physical deuteron binding
N = 500                 # radial nodes (dense eigvalsh; lighter than 900 for speed)
R_MAX = 20.0
B = 0.55                # fm quark size
G_OMEGA_UNIV = 9.0 * (nuc.M_OMEGA_DEFAULT / (np.sqrt(2) * nuc.F_PI_DEFAULT)) ** 2 / (4 * np.pi)


def Eb(g_cm, gw):
    r = nuc.solve_deuteron(core="derived", b=B, g_cm=g_cm, sigma=True,
                           omega=(gw > 0), omega_g2_4pi=max(gw, 1e-9),
                           tensor=True, vectors=False, N=N, R_max=R_MAX)
    return r["E_b"]


def bisect_gw(g_cm, lo=0.01, hi=26.0, iters=34):
    flo = Eb(g_cm, lo) - TARGET
    fhi = Eb(g_cm, hi) - TARGET
    if flo * fhi > 0:
        return None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = Eb(g_cm, mid) - TARGET
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


#: the four core strengths F247 tabulates; the middle one is the N-Delta-derived
#: value, so the row that carries the finding's headline number is included.
_ANCHORS = (0.0, 9.155, 18.31, 27.47)


def check_degeneracy():
    """
    F247 (Q3) — registry entry point for `F247-q3-omega-degeneracy`.

    Added 2026-08-03 by gap #5 of the 2026-08-02 completeness sweep, which
    found this module registered `dead_candidate` while F247 was cited as a
    CLOSED open-derivation with no test record.  `main()` below prints and
    dumps JSON but asserts nothing.

    Four checks.  F247's claim is a NEGATIVE — that g_omega is a genuine free
    input — so the checks are built to fail if that negative ever stops being
    true, which is the only way a documented-free-input result can regress.

      D1  The binding valley: for each core strength g_cm, bisect the omega
          coupling that binds the deuteron to E_b = 2.224 MeV.  Reproduces
          F247's tabulated 11.15 / 8.26 / 5.39 / 2.56.
      D2  The valley is near-LINEAR: g_omega^2/4pi = 11.13 - 0.313 g_cm with
          max residual <= 0.03.  Linearity IS the degeneracy — a curved or
          flat-bottomed valley would mean the deuteron does separate the two,
          and the finding would be wrong.
      D3  The degeneracy is not marginal: the omega coupling required varies
          by more than a factor of four across the physically admissible core
          range, so the F240 bracket [5.4, 11.1] is a SLICE of this valley
          rather than an uncertainty on omega alone.
      D4  F247's correction to F240 holds: at the N-Delta-DERIVED core the
          quench vs the 25.9 universality ceiling is 0.208, NOT the 0.43 that
          F240 remarked on — 0.43 is the core-OFF (route B) row, which is the
          g_cm = 0 entry of this same valley.  Asserted in both directions so
          the correction cannot be silently reverted.

    Runs the deuteron solver ~140 times at N=500 (~10 s).  Returns the result
    dict; raises AssertionError on any failure.
    """
    out = {"target_Eb": TARGET, "g_omega_universality": G_OMEGA_UNIV,
           "g_cm_derived_NDelta": nuc.GCM_DEFAULT, "N": N, "valley": []}

    # -- D1: the valley ----------------------------------------------------
    gws = []
    for g_cm in _ANCHORS:
        gw = bisect_gw(g_cm)
        assert gw is not None, f"deuteron unbound at g_cm={g_cm}"
        gws.append(gw)
        out["valley"].append({"g_cm": g_cm, "core_frac": g_cm / nuc.GCM_DEFAULT,
                              "g_omega_star": gw, "quench": gw / G_OMEGA_UNIV})
    # F247's tabulated column, 3 s.f.  NOTE (2026-08-03): the g_cm = 9.155 row
    # is printed as 8.26 but the solver returns 8.2549, which rounds to 8.25 —
    # a one-digit rounding slip in the finding's table, not a numerical
    # disagreement (every other row reproduces to <1e-3).  Recorded in
    # docs/audits/module-disposition-2026-08-03.md; the bound is 1e-2 so the
    # record asserts what is true rather than inheriting the typo.
    expected = (11.15, 8.26, 5.39, 2.56)
    for g_cm, gw, exp in zip(_ANCHORS, gws, expected):
        assert abs(gw - exp) < 1e-2, (g_cm, gw, exp)

    # -- D2: linearity = degeneracy ---------------------------------------
    x = np.array(_ANCHORS)
    y = np.array(gws)
    slope, intercept = np.polyfit(x, y, 1)
    resid = float(np.max(np.abs(np.polyval([slope, intercept], x) - y)))
    out["fit"] = {"intercept": float(intercept), "slope": float(slope),
                  "max_residual": resid}
    assert abs(intercept - 11.13) < 0.02, intercept
    assert abs(slope + 0.313) < 0.005, slope
    assert resid <= 0.03, resid

    # -- D3: the degeneracy is wide, not marginal --------------------------
    span = max(gws) / min(gws)
    out["valley_span_ratio"] = span
    assert span > 4.0, span

    # -- D4: F247's correction to F240's "0.43 ~ 0.45" remark --------------
    q_derived = gws[_ANCHORS.index(18.31)] / G_OMEGA_UNIV
    q_core_off = gws[_ANCHORS.index(0.0)] / G_OMEGA_UNIV
    out["quench_at_derived_core"] = q_derived
    out["quench_core_off_routeB"] = q_core_off
    assert abs(q_derived - 0.208) < 0.005, q_derived
    assert abs(q_core_off - 0.431) < 0.005, q_core_off
    assert q_derived < 0.30, "the physical quench must NOT be the 0.43 figure"

    out["n_checks"] = 4
    out["verdict"] = (
        "The absolute g_omegaNN is a genuine free input. The deuteron fixes "
        "only the TOTAL short-range repulsion, and the omega coupling trades "
        "against the F113 quark-Pauli core strength along a near-linear "
        "valley g_omega^2/4pi = 11.13 - 0.313 g_cm, so omega is not "
        "separately deuteron-observable and F240's bracket [5.4, 11.1] is a "
        "slice of that valley. At the N-Delta-derived core the quench is "
        "0.208, not 0.43; the 0.43 figure is the core-off row."
    )
    return out


def main():
    out = {"target_Eb": TARGET, "g_omega_universality": G_OMEGA_UNIV,
           "g_cm_derived_NDelta": nuc.GCM_DEFAULT, "N": N, "valley": []}
    print(f"g_omega universality ceiling = {G_OMEGA_UNIV:.3f}")
    print(f"{'g_cm(MeV)':>10} {'core/derived':>13} {'g_w2/4pi*':>11} {'quench':>8}")
    for g_cm in [0.0, 4.58, 9.155, 13.73, 18.31, 22.89, 27.47]:
        gw = bisect_gw(g_cm)
        q = (gw / G_OMEGA_UNIV) if gw else None
        row = {"g_cm": g_cm, "core_frac": g_cm / nuc.GCM_DEFAULT,
               "g_omega_star": gw, "quench": q}
        out["valley"].append(row)
        gstr = f"{gw:.3f}" if gw else "unbound"
        qstr = f"{q:.3f}" if q else "  -  "
        print(f"{g_cm:>10.2f} {g_cm/nuc.GCM_DEFAULT:>13.2f} {gstr:>11} {qstr:>8}")

    # route A at the derived core, with eigenvectors for r_d / P_D
    gw = bisect_gw(nuc.GCM_DEFAULT)
    r = nuc.solve_deuteron(core="derived", b=B, g_cm=nuc.GCM_DEFAULT, sigma=True,
                           omega=True, omega_g2_4pi=gw, tensor=True, vectors=True,
                           N=N, R_max=R_MAX)
    out["routeA"] = {"g_cm": nuc.GCM_DEFAULT, "g_omega_star": gw,
                     "E_b": r["E_b"], "r_d": r["r_d"], "P_D": r["P_D"],
                     "quench": gw / G_OMEGA_UNIV}
    print(f"\nRoute A (N-Delta-derived core g_cm=18.31): g_w2/4pi*={gw:.3f} "
          f"E_b={r['E_b']:.3f} r_d={r['r_d']:.3f} P_D={r['P_D']*100:.1f}% "
          f"quench={gw/G_OMEGA_UNIV:.3f}")

    # Was the literal "../test-results/Q3_omega_degeneracy.json" — a
    # working-directory-relative artifact path, which only resolved from the
    # directory this file used to live in (CLAUDE.md "Result artifacts and
    # paths"). Repointed at `_results_path` 2026-08-03.
    path = results_path("Q3_omega_degeneracy.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
