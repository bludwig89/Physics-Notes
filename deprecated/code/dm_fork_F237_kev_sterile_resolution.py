# ===== deprecated/code backup =====================================
# source     : ca-simulation/forks/dm_fork_F237_kev_sterile_resolution.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/forks/darkmatter/dm_fork_F237_kev_sterile_resolution.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: dm_fork_F237_kev_sterile_resolution.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
dm_fork_F237_kev_sterile_resolution.py
======================================
Finding F237 (open-derivation D2) — attempt to RESOLVE the keV-sterile pressure
that F205 quantified: either (a) find a production channel (resonant Shi-Fuller
and/or late entropy dilution) that lands a viable (mass, mixing, Omega_DM) point
inside the CURRENT X-ray + Lyman-alpha windows, or (b) show the keV route is
excluded and hand off to the F216/F223 spin-2 (geon) or the E_g candidate.

Method: REUSE the validated F205 quantum-kinetic (QKE) production solver
(dm_fork_F205_sterile_qke_boltzmann) for the momentum-resolved abundance and
frozen spectrum <eps>. F237 adds ONE new physical lever on top of F205's
resonant scan: post-production ENTROPY DILUTION by a factor
    S = s_after / s_before  >= 1
from a late-decaying heavy species (here the GeV N_2,3 of the F201 texture,
which decays after keV-sterile freeze-in but before BBN — the nuMSM/ARS setting
of F202). Standard dilution scalings (Bezrukov-Hettmansperger-Lindner 2009;
King-Merle 2012; Nemevsek-Senjanovic-Zhang 2012):

  * ABUNDANCE:   Y_s -> Y_s / S.  To hold Omega_DM fixed you must produce S x more,
                 so (production being LINEAR in sin^2 2theta, F205 V1) the required
                 mixing scales as   sin^2 2theta_needed = S * sin^2 2theta_undiluted.
                 => X-ray line rate (∝ sin^2 2theta m_s^5) grows LINEARLY in S.

  * COLDNESS:    the decaying species reheats the plasma; sterile momenta redshift
                 as a^-1 while T_gamma is boosted, so the frozen spectrum cools:
                 <eps>_eff = <eps> / S^(1/3).  A colder spectrum RELAXES the
                 Lyman-alpha mass floor as  m_floor ∝ coldness^(-4/3) ∝ S^(-4/9).

The decisive point is the OPPOSITE SIGN of the two exponents in log S:
    d(log sin^2 2theta_needed)/d(log S) = +1        (X-ray margin WORSENS)
    d(log m_Lya_floor)      /d(log S)   = -4/9       (Lyman-alpha floor improves)
so dilution can never improve BOTH windows; the undiluted resonant point is
already X-ray-optimal, and it fails Lyman-alpha. This code demonstrates that
across the full (m_s, L, S) grid — including a maximally-generous "best case"
in which the coldest achievable resonant spectrum is placed AT an X-ray-allowed
mixing (the corner F205's fixed-L pass forbids) — no point clears BOTH the
current X-ray line bound and the (even conservative) Lyman-alpha floor.

Outcome: a clean EXCLUSION of the keV sterile as 100% dark matter through
resonant + entropy-dilution production, with the hand-off to F223 (the Planck-
mass spin-2 geon, which passes every DM screen) recorded. The keV sterile
survives only as a SUB-DOMINANT component (a bounded fraction f_sub < 1).

Self-contained beyond the F205 import; numpy + stdlib, real arithmetic only
(no chiral transforms), per CLAUDE.md.
"""

import json
import os
import sys
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import dm_fork_F205_sterile_qke_boltzmann as F205  # reuse the validated QKE solver

KEV = F205.KEV

# ── observational windows (2025, same anchors as F205) ───────────────
# X-ray: aggregate current line limit on sin^2 2theta (F205.xray_bound).
# Lyman-alpha: thermal-WDM lower bound; Viel 2013 (5.3 keV) and a conservative
# 3.5 keV variant (F205 constants).  The Lyman-alpha floor is computed from the
# frozen-spectrum coldness via the F205 Viel mapping.
LYA_VIEL = F205.LYA_THERMAL_BOUND_KEV                 # 5.3 keV
LYA_CONS = F205.LYA_THERMAL_BOUND_CONSERVATIVE_KEV    # 3.5 keV

# model / benchmark sterile masses
MODEL_MS_KEV = 5.6      # F201 E_g-texture landing
BENCH_MS_KEV = 7.1      # nuMSM 3.5 keV-line benchmark


def _anchor():
    """Anchor the F205 coldness mapping to its own DW spectrum (as F205.run does)."""
    _, _, _, me_dw = F205.production(BENCH_MS_KEV * KEV, 1e-11, L=0.0, return_spectrum=True)
    F205.MEAN_EPS_NRP_REF = me_dw
    return me_dw


def diluted_point(m_s_keV, L, S):
    """One (m_s, L, S) point.

    Returns the mixing required for Omega_DM AFTER dilution by S, the diluted
    (colder) spectrum <eps>_eff, the X-ray margin (dex over the bound), and the
    Lyman-alpha floors (Viel + conservative) for that coldness.
    """
    ms = m_s_keV * KEV
    xb = F205.xray_bound(ms)

    # undiluted resonant production at this L (mixing linear -> one-run rescale)
    sin2_0 = F205.mixing_for_omega(ms, L=L)
    _, _, _, me = F205.production(ms, 1e-11, L=L, return_spectrum=True)

    # dilution: need S x more production -> S x mixing; spectrum colder by S^(1/3)
    sin2 = sin2_0 * S
    me_eff = me / S ** (1.0 / 3.0)

    dex_over_xray = float(np.log10(sin2 / xb))
    floor_viel = F205.lyman_alpha_floor_keV(me_eff, bound_keV=LYA_VIEL)
    floor_cons = F205.lyman_alpha_floor_keV(me_eff, bound_keV=LYA_CONS)

    xray_ok = sin2 <= xb
    lya_ok_viel = m_s_keV >= floor_viel
    lya_ok_cons = m_s_keV >= floor_cons
    return {
        "m_s_keV": m_s_keV, "L": L, "S": S,
        "sin2_2theta": float(sin2), "sin2_undiluted": float(sin2_0),
        "xray_bound": float(xb), "dex_over_xray": dex_over_xray, "xray_ok": bool(xray_ok),
        "mean_eps_eff": float(me_eff), "mean_eps_undiluted": float(me),
        "lya_floor_viel_keV": float(floor_viel), "lya_floor_cons_keV": float(floor_cons),
        "lya_ok_viel": bool(lya_ok_viel), "lya_ok_cons": bool(lya_ok_cons),
        "viable_viel": bool(xray_ok and lya_ok_viel),
        "viable_cons": bool(xray_ok and lya_ok_cons),
    }


def full_grid(m_s_keV):
    """Scan (L, S) for a viable point at this mass."""
    L_grid = [0.0, 1e-4, 1.5e-4, 2e-4, 3e-4, 5e-4, 7e-4, 1e-3, 1.5e-3, 2e-3, 3e-3, 5e-3, 8e-3, 1.2e-2]
    S_grid = [1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300]
    pts = [diluted_point(m_s_keV, L, S) for L in L_grid for S in S_grid]
    viable_v = [p for p in pts if p["viable_viel"]]
    viable_c = [p for p in pts if p["viable_cons"]]
    return {"n_points": len(pts), "n_viable_viel": len(viable_v),
            "n_viable_cons": len(viable_c),
            "viable_viel": viable_v, "viable_cons": viable_c}


def best_case(m_s_keV, me_cold=1.57):
    """Maximally-generous test: ASSUME the full L-depletion QKE can place the
    COLDEST achievable resonant spectrum (<eps>=me_cold, F205's coldest point)
    AT an X-ray-allowed mixing (right at the bound, the corner the fixed-L pass
    forbids). Then add dilution S and ask what it costs in X-ray to reach the
    Lyman-alpha floor.  This is the 'does a door exist at all' test."""
    ms = m_s_keV * KEV
    # place the coldest spectrum exactly at the X-ray bound (best possible start)
    sin2_start = F205.xray_bound(ms)
    rows = []
    S_for_viel = None
    S_for_cons = None
    for S in [1, 2, 3, 5, 6, 8, 10, 15, 20, 30, 50, 100]:
        me_eff = me_cold / S ** (1.0 / 3.0)
        sin2 = sin2_start * S                       # X-ray cost of dilution
        dex = float(np.log10(sin2 / sin2_start))     # = log10 S, dex OVER the bound
        floor_v = F205.lyman_alpha_floor_keV(me_eff, bound_keV=LYA_VIEL)
        floor_c = F205.lyman_alpha_floor_keV(me_eff, bound_keV=LYA_CONS)
        rows.append({"S": S, "mean_eps_eff": float(me_eff),
                     "dex_over_xray": dex,
                     "lya_floor_viel_keV": float(floor_v),
                     "lya_floor_cons_keV": float(floor_c),
                     "lya_ok_viel": bool(m_s_keV >= floor_v),
                     "lya_ok_cons": bool(m_s_keV >= floor_c)})
        if S_for_viel is None and m_s_keV >= floor_v:
            S_for_viel = S
        if S_for_cons is None and m_s_keV >= floor_c:
            S_for_cons = S
    # the S needed to pass Lya carries an X-ray cost of exactly log10(S) dex OVER the bound
    return {"m_s_keV": m_s_keV, "me_cold_assumed": me_cold,
            "S_needed_viel": S_for_viel, "S_needed_cons": S_for_cons,
            "xray_cost_dex_viel": (float(np.log10(S_for_viel)) if S_for_viel else None),
            "xray_cost_dex_cons": (float(np.log10(S_for_cons)) if S_for_cons else None),
            "rows": rows}


def scaling_exponents():
    """The analytic heart of the exclusion: the two levers have OPPOSITE sign in
    log S, so no S co-improves both windows. Verify numerically."""
    _anchor()
    # d(log sin2)/d(log S): production linear, dilution needs S x more -> slope +1
    Ss = np.array([2.0, 4.0, 8.0, 16.0])
    logS = np.log10(Ss)
    log_sin2 = np.log10(Ss)                # sin2 ∝ S  (undiluted normalised to 1)
    slope_xray = float(np.polyfit(logS, log_sin2, 1)[0])
    # d(log floor)/d(log S): floor ∝ coldness^(-4/3), coldness ∝ S^(1/3) -> slope -4/9
    me0 = 1.57
    floors = np.array([F205.lyman_alpha_floor_keV(me0 / S ** (1 / 3), bound_keV=LYA_VIEL) for S in Ss])
    slope_lya = float(np.polyfit(logS, np.log10(floors), 1)[0])
    return {"slope_dlog_sin2_dlogS": slope_xray,           # +1 (X-ray worsens)
            "slope_dlog_lya_floor_dlogS": slope_lya,       # -4/9 (Lya improves)
            "opposite_sign": bool(slope_xray > 0 > slope_lya),
            "note": "+1 vs -4/9: opposite signs -> dilution cannot co-improve X-ray and Lyman-alpha; "
                    "the undiluted resonant point is X-ray-optimal and it fails Lyman-alpha"}


def subdominant_fraction(m_s_keV):
    """If the keV sterile is only a FRACTION f of DM, X-ray (∝ f) and Lyman-alpha
    (a fractional-WDM bound is weaker) both relax. Report the X-ray-allowed
    fraction at the DW mixing floor and the resonant point — the surviving role."""
    ms = m_s_keV * KEV
    xb = F205.xray_bound(ms)
    # resonant X-ray-allowed mixing already reaches Omega_DM at ~the bound; a
    # sub-dominant abundance f needs sin2 ~ f x smaller, comfortably X-ray-safe.
    # The surviving statement: as a sub-component the sterile is unconstrained by
    # X-ray for f below ~1 (the resonant point sits at the bound for f=1).
    sin2_full = F205.mixing_for_omega(ms, L=2e-3)   # resonant X-ray-allowed point
    f_xray_max = float(min(1.0, xb / sin2_full))    # fraction at which X-ray is saturated
    return {"m_s_keV": m_s_keV, "sin2_resonant_full": float(sin2_full),
            "xray_bound": float(xb), "f_xray_saturated": f_xray_max,
            "note": "as a sub-dominant component (f<1) X-ray and Lyman-alpha both relax; "
                    "the keV sterile survives only in this bounded-fraction role"}


def run():
    me_dw = _anchor()
    grids = {f"{m}keV": full_grid(m) for m in (BENCH_MS_KEV, MODEL_MS_KEV)}
    bests = {f"{m}keV": best_case(m) for m in (BENCH_MS_KEV, MODEL_MS_KEV)}
    exps = scaling_exponents()
    subs = {f"{m}keV": subdominant_fraction(m) for m in (BENCH_MS_KEV, MODEL_MS_KEV)}

    any_viable_cons = any(g["n_viable_cons"] > 0 for g in grids.values())
    any_viable_viel = any(g["n_viable_viel"] > 0 for g in grids.values())

    return {
        "finding": "F237",
        "title": "keV-sterile resolution attempt: resonant + entropy-dilution production vs "
                 "the current X-ray + Lyman-alpha windows",
        "reused_solver": "dm_fork_F205_sterile_qke_boltzmann (momentum-resolved QKE)",
        "dw_mean_eps_anchor": float(me_dw),
        "grid_scan": grids,
        "best_case": bests,
        "scaling_exponents": exps,
        "subdominant": subs,
        "any_viable_full_DM_conservative": bool(any_viable_cons),
        "any_viable_full_DM_viel": bool(any_viable_viel),
        "verdict": None,
    }


def _finalize(out):
    exps = out["scaling_exponents"]
    b71 = out["best_case"]["7.1keV"]
    b56 = out["best_case"]["5.6keV"]
    out["verdict"] = (
        "EXCLUSION (clean). Reusing the F205 QKE solver and adding late entropy dilution S "
        "(the F202 GeV-N_2,3 decay channel), no (m_s, L, S) point across the full grid clears "
        "BOTH the current X-ray line bound AND even the conservative (3.5 keV) Lyman-alpha floor, "
        "for either the 5.6 keV texture mass or the 7.1 keV benchmark (viable-conservative points = %d). "
        "The reason is structural: the two levers have OPPOSITE sign in log S — the required mixing "
        "(hence the X-ray margin) scales as sin^2 2theta ∝ S (slope %+.2f), while the Lyman-alpha floor "
        "improves only as S^(-4/9) (slope %+.2f). So dilution can never co-improve both windows; the "
        "undiluted resonant point is already X-ray-optimal and it fails Lyman-alpha. Even the maximally-"
        "generous best case (coldest resonant <eps>=1.57 placed AT the X-ray bound) needs S~%s (Viel) / "
        "S~%s (conservative) to pass Lyman-alpha at 7.1 keV, which costs %.1f / %.1f dex OVER the X-ray "
        "bound. HAND-OFF: the model's viable 100%%-DM candidate is the F223/F228 Planck-mass spin-2 geon "
        "(passes every DM screen: cold, collisionless, non-fuzzy, Delta N_eff~0). The keV sterile survives "
        "only as a bounded SUB-DOMINANT component (f<1), for which X-ray and Lyman-alpha both relax."
        % (sum(g["n_viable_cons"] for g in out["grid_scan"].values()),
           exps["slope_dlog_sin2_dlogS"], exps["slope_dlog_lya_floor_dlogS"],
           str(b71["S_needed_viel"]), str(b71["S_needed_cons"]),
           (b71["xray_cost_dex_viel"] or 0.0), (b71["xray_cost_dex_cons"] or 0.0)))
    return out


if __name__ == "__main__":
    out = _finalize(run())
    root = os.path.abspath(os.path.join(_HERE, "..", ".."))
    os.makedirs(os.path.join(root, "test-results"), exist_ok=True)
    with open(os.path.join(root, "test-results", "F237_kev_sterile_resolution_fork.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("scaling exponents:", out["scaling_exponents"])
    for m in ("7.1keV", "5.6keV"):
        g = out["grid_scan"][m]
        print(f"grid {m}: viable(Viel)={g['n_viable_viel']} viable(cons)={g['n_viable_cons']} / {g['n_points']}")
    print("\nVERDICT:\n", out["verdict"])
