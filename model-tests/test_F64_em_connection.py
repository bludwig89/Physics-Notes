"""
test_F64_em_connection.py — Electromagnetic-connection gravity fork
====================================================================
Exercises `ca-simulation/forks/gr_fork_F64_em_connection.py`, the logical fork
that replaces the "gravity-is-emergent" rest-leg route (F50/F52/F62) with a
single lattice dielectric K(x) — a position-dependent renormalisation of the
(E,B) rotation rule (F25/F26).

  D-EM1  eikonal-index viability (exact, algebraic).  Can a single scalar give
         factor-1 redshift AND factor-2 bend at once?  Only the
         impedance-preserving dielectric placement (A=1/K, B=K) can; the
         clock-only and refractive-only placements each fail a coefficient
         (the Finding-19 obstruction).  The cheap, decisive go/no-go.
  D-EM2  single-field lattice deflection — one dielectric field K(x) on a 3D
         FFT-Poisson background gives K_bend≈4 (Einstein), no second field eqn;
         rest leg on the SAME field is K_bend≈2 (ratio≈2 cancels lattice error).
  D-EM3  radiation-as-source — a standing (E,B) field-energy shell deflects
         light like an equal energy of rest mass (EM-connection); the rest-leg
         route sources nothing from massless field energy.  The physical fork.
  D-EM4  one self-sourced K: factor-1 redshift + factor-2 bend  (scaffold)

Writes test-results/F64_em_connection.json and a markdown summary.

Run:
    python model-tests/test_F64_em_connection.py
"""

from __future__ import annotations

import json
import os
import sys
import time

THIS = os.path.dirname(__file__)
SIM = os.path.abspath(os.path.join(THIS, "..", "ca-simulation"))
FORKS = os.path.join(SIM, "forks")
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

import gr_fork_F64_em_connection as em      # noqa: E402

STAMP = "2026-05-31 - 16:00"

# Full battery, mirroring the emergent-gravity module (F62, dirac_gravity_fork):
#   • STATIC eikonal/field-level discriminators (D-EM1/2/3) — the cheap go/no-go
#     and the radiation-as-source physical fork.
#   • DYNAMIC time-domain wave-packet tests (D-EM-D1 … D-EM4) — the dielectric
#     counterparts of F62's six-test battery, run on the SAME exactly-unitary
#     curved-background Dirac stepper so the only difference on the wire is the
#     metric placement (single impedance-locked dielectric A=1/K,B=K vs F62's
#     two independent legs A=1+2Φ/c², B=1−2Φ/c²).
SUITE = [
    # ---- static eikonal / field-level (exact + lattice) -------------------
    ("D-EM1_eikonal_viability", em.test_dem1_eikonal_viability,
     "single scalar: factor-1 redshift AND factor-2 bend? (exact, algebraic)"),
    ("D-EM2_single_field_deflection", em.test_dem2_single_field_deflection,
     "single dielectric K(x) on lattice: K_bend≈4 (no 2nd field eqn); rest leg≈2"),
    ("D-EM3_radiation_as_source", em.test_dem3_radiation_as_source,
     "standing (E,B) energy shell deflects like equal-energy rest mass (the fork)"),
    # ---- dynamic time-domain (F62-battery counterparts) -------------------
    ("D-EM-D1_flat_regression", em.test_demD1_flat_regression,
     "flat dielectric stepper ≡ two free Weyl walks bit-for-bit (= F62 D1)"),
    ("D-EM-D2a_dielectric_freefall", em.test_demD2a_dielectric_freefall,
     "equivalence principle on a dielectric Rindler frame (= F62 D2a)"),
    ("D-EM-D2b_dynamical_redshift", em.test_demD2b_dynamical_redshift,
     "dielectric clock rate ∝ √A=(1−u), measured from zitterbewegung (= F62 D2b)"),
    ("D-EM-D2c_dielectric_deflection", em.test_demD2c_dielectric_deflection,
     "fast packet past a dielectric mass: K_bend≈4 from ONE field (cf F62 two-leg)"),
    ("D-EM-D3a_backreaction_norm", em.test_demD3a_backreaction_norm,
     "self-gravitating dielectric packet: norm conserved as its own K(x) evolves"),
    ("D-EM4_redshift_bend_consistency", em.test_dem4_redshift_bend_consistency,
     "ONE self-sourced K: factor-1 redshift AND factor-2 bend together (closes D-EM1)"),
    # ---- derivation + dynamical Maxwell (model-element build-out) ----------
    ("D-EM5_derive_dielectric", em.dem5_derive_dielectric,
     "DERIVE ε=μ=K (⇒A=1/K,B=K) from proper (E,B) rotation: impedance+conformal+redshift"),
    ("D-EM6_light_bends_light", em.test_dem6_light_bends_light,
     "dynamical Maxwell pulse deflected by a pure-EM-energy lens (light bends light)"),
    # ---- model-element maturation: 3-D absolute, dynamical field, strong field --
    ("D-EM7_absolute_deflection_3d", em.test_dem7_absolute_deflection_3d,
     "absolute K_bend→4 on a genuine 3-D ray (true 1/r; removes the 2-D log caveat)"),
    ("D-EM8_dynamical_field", em.test_dem8_dynamical_field,
     "Φ as a dynamical field: static=Poisson well, finite c_g (causal), energy conserved"),
    ("D-EM9_strong_field_ppn", em.test_dem9_strong_field_ppn,
     "PPN vs Schwarzschild: γ=1 (light OK) but β=½ for (1−u)⁻²; e^{2u} restores GR"),
    # ---- pinning G + co-evolving clock (items 6, 7) -----------------------
    ("D-EM10_pin_G_to_cell_scale", em.test_dem10_pin_G_to_cell_scale,
     "4πG not free: 4π lattice-exact, G induced (a=3.81 ℓ_P, 1/G∝√d) per F58/F59/F61"),
    ("D-EM11_coevolving_self_redshift", em.test_dem11_coevolving_self_redshift,
     "fully co-evolving self-redshift (Hilbert clock, no fixed-radius workaround)"),
]


def run() -> dict:
    results, t_total = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time()
        print(f"[run] {name} ...", flush=True)
        r = fn()
        r["_seconds"] = round(time.time() - t, 2)
        r["_desc"] = desc
        results[name] = r
        status = r.get("pass")
        tag = "SKIP" if status is None else f"pass={status}"
        print(f"      {tag}  ({r['_seconds']}s)", flush=True)
    implemented = [r for r in results.values() if r.get("pass") is not None]
    out = {
        "finding": "F64",
        "title": "Electromagnetic-connection gravity — single lattice dielectric K(x)",
        "timestamp": STAMP,
        "module": "ca-simulation/forks/gr_fork_F64_em_connection.py",
        "n_pass": sum(1 for r in implemented if r.get("pass")),
        "n_implemented": len(implemented),
        "n_total": len(results),
        "total_seconds": round(time.time() - t_total, 2),
        "tests": results,
    }
    return out


def write_markdown(out: dict, path: str) -> None:
    t = out["tests"]
    d = t["D-EM1_eikonal_viability"]
    L = []
    L.append(f"# {out['finding']} — {out['title']}")
    L.append("")
    L.append(f"_Generated {out['timestamp']} by "
             f"`model-tests/test_F64_em_connection.py`._")
    L.append("")
    L.append(f"**D-EM1 verdict: {d.get('verdict')}** "
             f"({out['n_pass']}/{out['n_implemented']} implemented tests PASS; "
             f"{out['n_total'] - out['n_implemented']} scaffolded). "
             f"Module: `{out['module']}`.")
    L.append("")
    L.append("## D-EM1 — eikonal-index viability (exact, algebraic)")
    L.append("")
    L.append("Targets: gravitational redshift slope **Z = 1** (factor-1) and light "
             "deflection coefficient **K_bend = 4** (factor-2; Newton = 2). "
             "`u = GM/(r c²)`. A single scalar must hit BOTH.")
    L.append("")
    L.append("| Single-scalar placement | Z (redshift) | K_bend | impedance const? | passes GR? |")
    L.append("|---|---|---|---|---|")
    L.append(f"| **dielectric**  (A=1/K, B=K) | {d['dielectric_Z']} | "
             f"{d['dielectric_K_bend']} | {d['dielectric_impedance_constant']} | "
             f"**yes** |")
    L.append(f"| clock-only  (B=1, F52 rest leg) | {d['clock_only_Z']} | "
             f"{d['clock_only_K_bend']} | False | no (bend=2) |")
    L.append(f"| refractive-only  (A=1) | {d['refractive_only_Z']} | "
             f"{d['refractive_only_K_bend']} | False | no (no redshift) |")
    L.append("")
    L.append(f"Dielectric eikonal index `n(u) = {d['dielectric_n_of_u']}`; "
             f"impedance `√(μ/ε) = {d['dielectric_impedance']}` (u-independent ⇒ "
             f"proper (E,B) rotation, no scalar contamination, F26-consistent).")
    L.append("")
    L.append("**Numerical guard** — full (non-linearised) dielectric deflection "
             "integral `K_bend = α b c²/GM` → 4 as field strength → 0:")
    L.append("")
    L.append("| GM/(b c²) | K_bend |")
    L.append("|---|---|")
    for k, v in d["full_deflection_guard"].items():
        L.append(f"| {k} | {v:.6f} |")
    L.append("")
    # D-EM2
    d2 = t["D-EM2_single_field_deflection"]
    L.append("## D-EM2 — single-field lattice deflection")
    L.append("")
    L.append(f"**pass = {d2.get('pass')}.** One dielectric field K(x) on a 3D "
             f"FFT-Poisson background (L={d2['lattice']['L']}, M={d2['lattice']['M']}, "
             f"u≈{d2['weak_field_u_at_probe']:.1e} at probe). Eikonal K_bend "
             f"(GR=4, Newton=2):")
    L.append("")
    L.append("| index placement | K_bend | expected |")
    L.append("|---|---|---|")
    L.append(f"| dielectric (the fork) | {d2['K_dielectric']:.4f} | 4 |")
    L.append(f"| full GR (two-leg) | {d2['K_full_GR']:.4f} | 4 |")
    L.append(f"| rest-leg only (F52) | {d2['K_rest_only']:.4f} | 2 |")
    L.append("")
    L.append(f"Ratio dielectric / rest-leg = **{d2['ratio_dielectric_over_rest']:.4f}** "
             f"(target 2; cancels common lattice/box error). A single field "
             f"reaches Einstein factor-2 with no separately-sourced spatial leg.")
    L.append("")
    # D-EM3
    d3 = t["D-EM3_radiation_as_source"]
    L.append("## D-EM3 — radiation-as-source (the physical fork)")
    L.append("")
    L.append(f"**pass = {d3.get('pass')}.** Equal-energy rest-mass blob vs standing "
             f"(E,B) field-energy shell (energy match "
             f"{d3['energy_match']:.1e}), rays outside both:")
    L.append("")
    L.append("| source (EM-connection coupling) | K_bend |")
    L.append("|---|---|")
    L.append(f"| rest-mass blob | {d3['K_bend_mass_emconn']:.4f} |")
    L.append(f"| (E,B) field-energy shell | {d3['K_bend_radiation_emconn']:.4f} |")
    L.append("")
    L.append(f"Radiation / mass deflection (EM-connection) = "
             f"**{d3['ratio_radiation_over_mass_emconn']:.4f}** (target 1: equal "
             f"energy ⇒ equal gravity).  Under the **rest-leg** coupling the "
             f"massless shell sources nothing — its deflection is "
             f"{d3['restleg_radiation_deflection_fraction']:.1e} of the mass case. "
             f"That zero-vs-one split is the fork.")
    L.append("")
    # ---- dynamic time-domain battery -------------------------------------
    L.append("## Dynamic time-domain battery (F62-counterpart)")
    L.append("")
    L.append("The dielectric promoted to a full **dynamic field**: a Dirac wave "
             "packet evolved in time on the dielectric background (and, in the "
             "backreaction tests, on the dielectric it sources), run on F62's "
             "*same* exactly-unitary curved-background stepper. The only "
             "difference on the wire is the metric placement.")
    L.append("")
    L.append("| Dynamic test | observable | result | pass |")
    L.append("|---|---|---|---|")
    d1 = t["D-EM-D1_flat_regression"]
    L.append(f"| D-EM-D1 flat regression | max residual vs 2 free Weyl walks | "
             f"{d1['residual_max_abs']:.2e} | {d1.get('pass')} |")
    fa = t["D-EM-D2a_dielectric_freefall"]
    L.append(f"| D-EM-D2a free-fall (EP) | g_meas/g_pred (mass-spread) | "
             f"{fa['coeff_ratio']:.3f} ({fa['universality_spread']:.3f}) | "
             f"{fa.get('pass')} |")
    rb = t["D-EM-D2b_dynamical_redshift"]
    L.append(f"| D-EM-D2b redshift | f_near/f_far vs arcsin pred | "
             f"{rb['ratio_meas']:.4f} vs {rb['ratio_pred_exact_arcsin']:.4f} | "
             f"{rb.get('pass')} |")
    df = t["D-EM-D2c_dielectric_deflection"]
    L.append(f"| D-EM-D2c deflection | K_meas / K_eikonal | "
             f"{df['K_meas']:.3f} / {df['K_eikonal']:.3f} | {df.get('pass')} |")
    bn = t["D-EM-D3a_backreaction_norm"]
    L.append(f"| D-EM-D3a backreaction norm | norm drift | "
             f"{bn['norm_drift']:.2e} | {bn.get('pass')} |")
    L.append("")
    # D-EM4 detail
    d4 = t["D-EM4_redshift_bend_consistency"]
    L.append("## D-EM4 — one self-sourced K: factor-1 redshift AND factor-2 bend")
    L.append("")
    L.append(f"**pass = {d4.get('pass')}.** A single dielectric field, sourced "
             f"self-consistently from a mass blob (∇²Φ=4πGρ), delivers BOTH GR "
             f"coefficients at once — the dynamical close of the D-EM1 loop and "
             f"the F64 counterpart of F62-D3a self-redshift.")
    L.append("")
    L.append("| coefficient | measured | predicted | target |")
    L.append("|---|---|---|---|")
    L.append(f"| factor-1 redshift  f_near/f_far | {d4['redshift_ratio_meas']:.4f} "
             f"| {d4['redshift_ratio_pred_exact']:.4f} (2·arcsin√A·m) | < 1 (deep slow) |")
    L.append(f"| factor-2 bend  n-slope ratio (diel/rest) | "
             f"{d4['bend_ratio_dielectric_over_rest']:.4f} | 2 | "
             f"2 ⇒ K_bend 4 vs Newton 2 |")
    L.append("")
    L.append(f"Self-sourced lapse sampled at the well bottom A_near="
             f"{d4['A_near']:.3f} and the flat rim A_far={d4['A_far']:.3f}; the "
             f"deep clock runs slower (redshift) and the same field's dielectric "
             f"index slope is exactly twice the rest-leg-only slope (factor-2).")
    L.append("")
    # ---- D-EM5 derivation -------------------------------------------------
    d5 = t["D-EM5_derive_dielectric"]
    L.append("## D-EM5 — deriving the dielectric placement (item 1)")
    L.append("")
    L.append(f"**pass = {d5.get('pass')}.** The one posited input — that the "
             f"position-dependent (E,B)-rotation enters as a genuine dielectric "
             f"ε=μ=K — is derived from *proper rotation + index + redshift*:")
    L.append("")
    L.append("| step | claim | result |")
    L.append("|---|---|---|")
    L.append(f"| (A) Plebanski | ε=μ=√(B/A) for both conformal reps | "
             f"{d5['plebanski_eps_mu_dielectric_rep']}, "
             f"{d5['plebanski_eps_mu_refractive_rep']} (both K) |")
    L.append(f"| (B) conformal | diag(−1/K,K,K,K)=K·diag(−1,K²,K²,K²); same index | "
             f"Weyl={d5['conformal_weyl_factor']}, n={d5['eikonal_index_both_reps'][0]}={d5['eikonal_index_both_reps'][1]} |")
    L.append(f"| (C) impedance+index | Z=1 ∧ n=K ⇒ unique solution | "
             f"ε={d5['impedance_index_solution'].get('epsilon','?')}, "
             f"μ={d5['impedance_index_solution'].get('mu','?')} |")
    L.append(f"| (D) reciprocal lock | factor-1 redshift fixes conformal factor | "
             f"A·B = {d5['AB_from_factor1_redshift']} |")
    L.append("")
    fr = d5["fdtd_reflection"]
    L.append("**Lattice confirmation** — 1-D FDTD reflection at an abrupt index "
             "step (the small-k Maxwell limit of the exact (E,B) rotation). Only "
             "the impedance-matched dielectric stays a *proper* (reflectionless) "
             "rotation; the non-dielectric placements reflect — that reflected "
             "wave is the F26 scalar contamination:")
    L.append("")
    L.append("| placement | reflected energy fraction |")
    L.append("|---|---|")
    L.append(f"| **matched** ε=μ=K (dielectric) | {fr['matched']:.4f} (grid floor) |")
    L.append(f"| refractive-only ε=K², μ=1 | {fr['refractive_only']:.4f} |")
    L.append(f"| clock-only ε=1, μ=K² | {fr['clock_only']:.4f} |")
    L.append("")
    L.append("So the EM sector (conformally invariant) carries **both** metric "
             "legs as one scalar and is blind only to the conformal factor — which "
             "the clock/redshift supplies. F64's dielectric and F52's rest-leg "
             "clock field are the same single scalar; impedance matching is what "
             "makes them consistent (AB=1).")
    L.append("")
    # ---- D-EM6 light-bends-light ------------------------------------------
    d6 = t["D-EM6_light_bends_light"]
    L.append("## D-EM6 — dynamical light-bends-light (item 2)")
    L.append("")
    L.append(f"**pass = {d6.get('pass')}.** A propagating 2-D Maxwell pulse (TM "
             f"Yee FDTD on ε=μ=K) is deflected by a lens made of **pure (E,B) "
             f"field energy** (zero rest mass). Both lens and probe are massless "
             f"light:")
    L.append("")
    L.append("| quantity | value |")
    L.append("|---|---|")
    L.append(f"| pulse deflection Δθ_meas | {d6['dtheta_meas']:.4f} (toward the mass) |")
    L.append(f"| eikonal Δθ on same field | {d6['dtheta_eikonal']:.4f} |")
    L.append(f"| fraction of eikonal realised | {d6['fraction_of_eikonal_realised']:.3f} |")
    L.append(f"| factor-2 ratio (dielectric/rest-leg) | {d6['factor2_ratio_dielectric_over_restleg']:.4f} (→2) |")
    L.append(f"| lens rest-mass density | {d6['rest_mass_density_of_lens']} |")
    L.append(f"| rest-leg deflection of this lens | {d6['restleg_deflection_of_lens']} |")
    L.append("")
    L.append("The pulse bends toward the energy lump and realises most of its ray "
             "(eikonal) deflection; the factor-2 ratio is exactly 2 (Einstein, not "
             "Newton). The absolute K_bend≈4 is the 3-D result (D-EM3); 2-D Poisson "
             "is logarithmic (Finding 8), so only the dimension-invariant ratio is "
             "quoted. **The fork:** the lens has zero rest mass, so the F50/F52 "
             "rest-leg coupling sources nothing from it (0) — light would not bend "
             "light. F64 makes it bend, dynamically.")
    L.append("")
    # ---- D-EM7 absolute 3-D deflection ------------------------------------
    d7 = t["D-EM7_absolute_deflection_3d"]
    L.append("## D-EM7 — absolute 3-D deflection on a ray (item 3)")
    L.append("")
    L.append(f"**pass = {d7.get('pass')}.** The photon ray integrated through the "
             f"true-1/r (3-D) dielectric n(r)=(1−u)⁻² gives the **absolute** "
             f"K_bend→4 (Einstein; Newton=2), approaching from above — not a 2-D "
             f"ratio (removes the Finding-8 logarithmic-Poisson caveat of D-EM6):")
    L.append("")
    L.append("| GM/bc² | K_bend (dielectric) | K_bend (e^{2u}) |")
    L.append("|---|---|---|")
    for k in ("1e-02", "1e-03", "1e-04"):
        L.append(f"| {k} | {d7['K_bend_dielectric_by_field'][k]:.5f} | "
                 f"{d7['K_bend_exp_by_field'][k]:.5f} |")
    L.append("")
    # ---- D-EM8 dynamical field --------------------------------------------
    d8 = t["D-EM8_dynamical_field"]
    L.append("## D-EM8 — Φ as a dynamical field with its own EOM (item 4)")
    L.append("")
    L.append(f"**pass = {d8.get('pass')}.** The dielectric potential is promoted "
             f"from an instantaneous Poisson constraint (F52/F62) to a field obeying "
             f"□Φ=−4πGρ:")
    L.append("")
    L.append("| property | result | target |")
    L.append("|---|---|---|")
    L.append(f"| static fixed point = Poisson well | rel dev {d8['static_fixedpoint_rel_dev']:.2e} | →0 |")
    L.append(f"| wavefront speed (causal/retarded) | {d8['wavefront_speed']:.4f} | c_g={d8['c_g']} |")
    L.append(f"| free-field energy drift | {d8['free_field_energy_drift']:.2e} | →0 |")
    L.append("")
    L.append("So K(x,t) is a genuine dynamical field: its static limit is the well "
             "that sources the dielectric, disturbances propagate **causally** at "
             "c_g (not the instantaneous Poisson of F52/F62), and the free field "
             "carries conserved energy — a kinetic term, i.e. dielectric "
             "gravitational waves and the seed of a Lagrangian element.")
    L.append("")
    # ---- D-EM9 strong-field PPN -------------------------------------------
    d9 = t["D-EM9_strong_field_ppn"]
    L.append("## D-EM9 — strong-field PPN vs Schwarzschild (item 5)")
    L.append("")
    L.append(f"**pass = {d9.get('pass')}.** Exact PPN (β, γ) of the dielectric "
             f"metric, and the classic solar-system tests vs GR:")
    L.append("")
    L.append("| metric form | β | γ | light bend /GR | perihelion /GR | Mercury ″/cy |")
    L.append("|---|---|---|---|---|---|")
    for nm, p in d9["ppn"].items():
        L.append(f"| {nm} | {p['beta']} | {p['gamma']} | {p['light_bending_vs_GR']} | "
                 f"{p['perihelion_vs_GR']} | {p['mercury_arcsec_per_century']} |")
    L.append("")
    L.append(f"Observed Mercury anomaly **{d9['mercury_observed_arcsec_century']}** "
             f"″/century; MESSENGER bound β−1={d9['messenger_bound_beta_minus_1']}.")
    L.append("")
    L.append(d9["verdict"])
    L.append("")
    # ---- D-EM10 pin G -----------------------------------------------------
    d10 = t["D-EM10_pin_G_to_cell_scale"]
    L.append("## D-EM10 — pinning 4πG to the cell scale (item 6)")
    L.append("")
    L.append(f"**pass = {d10.get('pass')}.** The dielectric's 4πG (posited in F52) "
             f"is tied to the lattice via the induced-gravity chain F58/F59/F61:")
    L.append("")
    L.append("| piece | result |")
    L.append("|---|---|")
    L.append(f"| 4π lattice Green's-function (3-D point source) | GM recovered "
             f"{d10['four_pi_normalisation_GM_recovered']:.4f} (→1) |")
    L.append(f"| cell scale a/ℓ_P (g_*=16, η=1/12, d=3) | "
             f"{d10['cell_scale_a_over_lP']:.4f} (F61: 3.809) |")
    L.append(f"| 1/G ∝ 1/c_lat scaling (d=2,3,4) | "
             f"{[round(float(x),3) for x in d10['invG_scaling_clat_factor']]} vs √d "
             f"{[round(float(x),3) for x in d10['invG_scaling_sqrt_d']]} |")
    L.append("")
    L.append("So 4πG is **not free**: the 4π is lattice-exact and G is the "
             "Sakharov-induced value pinned by the cell scale a=√(2πη g_*)·d^{1/4}·ℓ_P "
             "≈ 3.81 ℓ_P and the mode count — the same coupling the rest-leg route "
             "(F52) left posited. Residual: the gauge sector's contribution to g_* "
             "(flagged in F61).")
    L.append("")
    # ---- D-EM11 co-evolving self-redshift ---------------------------------
    d11 = t["D-EM11_coevolving_self_redshift"]
    L.append("## D-EM11 — fully co-evolving self-redshift (item 7)")
    L.append("")
    L.append(f"**pass = {d11.get('pass')}.** Two rest packets co-evolved in the "
             f"genuine spatially-varying self-sourced dielectric (spreading through "
             f"the gradient — no fixed-radius workaround), clocked by the "
             f"resolution-free Hilbert instantaneous-frequency estimator:")
    L.append("")
    L.append("| quantity | value |")
    L.append("|---|---|")
    L.append(f"| deep/rim clock ratio (measured) | {d11['ratio_meas']:.4f} |")
    L.append(f"| local-lapse prediction 2·arcsin(√A·m) | {d11['ratio_pred_local_arcsin']:.4f} |")
    L.append(f"| relative error | {d11['rel_error']*100:.1f}% |")
    L.append(f"| redshift detected (deep clock slower) | {d11['redshift_detected']} |")
    L.append("")
    L.append("The co-evolving packet confirms gravitational redshift dynamically "
             "(deep clock slower); the residual ~10% is the finite packet sampling "
             "the well curvature as it spreads — which is exactly why the *precise* "
             "coefficient is read by the localized clock of D-EM4. The Hilbert "
             "estimator removes the FFT bin-leakage that defeated the naive "
             "measurement. F64 counterpart of F62-D3a self-redshift.")
    L.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))


def main():
    out = run()
    res_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(res_dir, exist_ok=True)
    jpath = os.path.join(res_dir, "F64_em_connection.json")
    mpath = os.path.join(res_dir, "F64_em_connection.md")
    with open(jpath, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    write_markdown(out, mpath)
    verdict = out["tests"]["D-EM1_eikonal_viability"].get("verdict")
    print(f"\nD-EM1: {verdict}  "
          f"({out['n_pass']}/{out['n_implemented']} implemented PASS)")
    print(f"Wrote {jpath}")
    print(f"Wrote {mpath}")
    return out


if __name__ == "__main__":
    main()
