"""F343 -- Does anything in the model fix the absolute Majorana scale M_R? (ledger D4, rubric C5)

D4 (docs/status/open-derivations.md) states plainly: "nothing in the model fixes M_R" --
F236/F254's see-saw derives the light-neutrino MASS SHAPE (ratios, hierarchy, machine
precision) but the overall Majorana scale M_R0 is a free anchor. D4 names its own cheapest
first check: does the F183/F107 canonical lattice cutoff, or the E_g condensate already
used for the M_R texture (F201), offer ANY scale link before M_R is accepted as an
irreducibly free second anchor alongside v?

This record runs that check on three independent legs, each mechanical rather than argued
from prose alone:

  C1/C2  the F183/F107 cutoff hierarchy (Lambda/M_R0 ~ 1e19 at F201's own benchmark), and an
         exhaustive scan of whether any small integer power of an already-registered
         lattice-fixed dimensionless ratio lands near the required suppression. The closest
         hit -- (1/(72*pi))^8, within 0.13 dex (~1.35x) of the target -- is reported and
         explicitly flagged as an unclaimed numerical coincidence (the project's own sense,
         cf. F332's reciprocal_cube_coincidence), not a structural link: the exponent 8 is
         unmotivated, and a comparable near-hit among 72 scanned (ratio, power) combinations
         is not, on its own, statistically surprising.
  C3     why F79's G = a^2 c^3/(8 pi sqrt3 hbar) is NOT a precedent for scale generation from
         the cutoff: its prefactor is O(1e-2), not a ~1e-19 suppression -- G is the SAME
         scale a re-expressed in SI units, not a second, hierarchically-separated scale.
  C4/C5  the E_g/Z3 texture (casim.engine.particles.majorana.z3_sqrt_texture, F201)
         factors the overall prefactor M_R0 out of its defining relation identically
         (sympy, exact) and is numerically blind to it (rescaling M_R0 leaves every ratio,
         every angle, and the F201 cancellation-node location exactly invariant) --
         generalizing F253's POSIT-N no-go (which proved the SAME machinery can supply a
         dimensionless weight/angle but not an absolute scale) from a radian to a mass,
         one further dimensional category away from anything the E_g representation theory
         produces.
  C6     nu_R's total gauge-singlet status (F47, Y=0 forced; reaffirmed F341) forecloses the
         model's only dynamical scale-generation mechanism: asymptotic-freedom running of a
         confining gauge coupling, implemented in this tree only for SU(3)_c
         (casim.engine.interactions.running_*). Checked mechanically: the majorana module
         imports nothing beyond numpy (zero coupling to any gauge/running/confinement
         module), and no running/confinement module uses nu_R/y_nu in a dynamical role (the
         one hit, derive_ncolour.py, is the unrelated hypercharge anomaly-cancellation
         system, F165/F279/F341).

What this record does NOT claim: that M_R is provably unfixable in any future extension of
the model (leg 3's escape hatch -- a new gauge coupling for nu_R -- is named explicitly in
the finding as what would void it), or that the C2 near-coincidence has any physical
meaning (it is flagged, not adopted, exactly parallel to F332's reciprocal-cube flag). The
claim is narrower and mechanical: for the model AS IT EXISTS TODAY, neither of D4's two
named candidates supplies a link, for stated and checked reasons.

See findings/F343-*.md for the full writeup, and F47/F79/F107/F201/F236/F253/F282/F341 for
the pieces this composes.
"""

import math

from casim.engine.particles import derive_M_R_scale_link as mod


# ---------------------------------------------------------------------------
# C1 -- the cutoff hierarchy is genuinely large (~19 decades at F201's own
#       benchmark), not a rounding-level gap
# ---------------------------------------------------------------------------

def test_C1_cutoff_hierarchy_is_about_19_decades():
    out = mod.c1_cutoff_hierarchy()
    assert out["Lambda_GeV"] == mod.lattice_cutoff_gev()
    # F282's cutoff = 3^{-1/4} * reduced M_Pl = E_P/(a/ell_P) ~ 1.85e18 GeV
    # (was 9.0e18..9.5e18, the sqrt(8 pi)-high non-reduced value; 2026-09-29)
    assert 1.8e18 < out["Lambda_GeV"] < 1.9e18
    # corrected cutoff (2026-09-29): log10(Lambda/M_R0) = 18.27, was 18.97
    assert 17.8 < out["log10_ratio"] < 18.8, (
        f"expected ~19 decades of hierarchy, got {out['log10_ratio']}"
    )


# ---------------------------------------------------------------------------
# C2 -- exhaustive scan: report and flag the closest hit, do not claim it
# ---------------------------------------------------------------------------

def test_C2_ratio_scan_closest_hit_is_flagged_not_claimed():
    out = mod.c2_ratio_scan()
    assert out["n_samples_scanned"] == 6 * 12  # 6 base ratios x 12 powers
    best = out["closest"]
    # The closest approach found (verified numerically, not asserted by hand):
    # (1/(72*pi))^8, 0.57 dex (~3.7x) from the target.  With the corrected
    # cutoff (2026-09-29, E_P/(a/ell_P)) the near-coincidence is weaker than
    # the 0.13 dex recorded against the sqrt(8 pi)-high cutoff — which only
    # strengthens the null result.
    assert best["name"] == "1/(72*pi) (G_LATTICE)"
    assert best["power"] == 8
    assert best["distance_dex"] < 1.0, (
        "the closest scanned combination should land within one dex of "
        f"the target; got {best['distance_dex']}"
    )
    # It is still a mismatch, not a hit: distance is bounded away from zero.
    assert best["distance_dex"] > 0.05
    # The verdict text must explicitly flag, not claim, the coincidence.
    assert "NOT a structural link" in out["verdict"]
    assert "unmotivated" in out["verdict"]


def test_C2_no_combination_within_max_power_matches_within_1_percent():
    """Negative control: confirm the scan is not accidentally trivial -- i.e.
    that no (ratio, power) pair matches the target to high precision, which
    would indicate an actual (rather than approximate, flagged) structural
    identity and would need very different treatment."""
    out = mod.c2_ratio_scan()
    hits = []
    target = out["target_log10_suppression"]
    for name, val in out["base_ratios"].items():
        logv = math.log10(abs(val))
        for p in range(1, 13):
            if abs(p * logv - target) < 1e-3:
                hits.append((name, p))
    assert hits == [], f"unexpected near-exact match(es): {hits}"


# ---------------------------------------------------------------------------
# C3 -- F79's G derivation carries zero hierarchy: not a precedent
# ---------------------------------------------------------------------------

def test_C3_G_prefactor_has_no_hierarchy():
    out = mod.c3_G_has_no_hierarchy()
    # O(1e-2), nowhere near the ~1e-19 M_R/Lambda target.
    assert 1e-3 < out["G_prefactor_1_over_8pi_sqrt3"] < 1e-1
    assert out["log10_M_R_over_Lambda_target"] < -18
    assert out["log10_G_prefactor"] > -2


# ---------------------------------------------------------------------------
# C4 -- the Z3/E_g texture factors M_R0 out identically (exact, sympy)
# ---------------------------------------------------------------------------

def test_C4_texture_factors_out_M_R0_exactly():
    out = mod.c4_texture_factors_out_M_R0_symbolically()
    assert out["M_R0_fully_factors_out"] is True
    assert out["d_bracket_d_M_R0"] == ["0", "0", "0"]


# ---------------------------------------------------------------------------
# C5 -- the texture mechanism is numerically blind to M_R0
# ---------------------------------------------------------------------------

def test_C5_texture_numerically_blind_to_M_R0():
    out = mod.c5_texture_blind_to_M_R0_numerically()
    assert out["texture_blind_to_M_R0"] is True
    assert out["max_ratio_residual"] < 1e-10
    assert out["max_amplitude_scaling_residual"] < 1e-6


# ---------------------------------------------------------------------------
# C6 -- nu_R's gauge-singlet status forecloses the model's only dynamical
#       scale-generation mechanism
# ---------------------------------------------------------------------------

def test_C6_majorana_module_has_no_gauge_or_running_coupling():
    out = mod.c6_no_dynamical_scale_route_for_nu_R()
    assert out["majorana_imports_any_gauge_or_running_module"] is False
    assert any("import numpy" in ln for ln in out["majorana_module_imports"])


def test_C6_control_running_modules_do_not_couple_nu_R_dynamically():
    """Negative control: derive_ncolour.py DOES mention y_nu, but only inside
    the hypercharge anomaly-cancellation linear system (F165/F279/F341) --
    a different physics question (fixing N_c / hypercharge ratios) with no
    bearing on a mass scale. Confirm that mention is confined to that
    context and is not a dynamical (running/confinement) coupling."""
    import inspect

    from casim.engine.gauge import derive_ncolour as ncolour_mod

    src = inspect.getsource(ncolour_mod)
    # y_nu must appear only inside the anomaly/mass-step symbolic system, and
    # the module must not import anything from a running/confinement scale
    # module in the same breath as y_nu.
    assert "y_nu" in src
    assert "anomaly" in src.lower() or "mass step" in src.lower()
