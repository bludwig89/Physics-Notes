"""F369 -- toward a model-native EH98 replacement (K11/S2).

Six checks plus a two-axis control.

  S1  (exact)  c_s(a) -> 1/sqrt(3) as a -> 0: a sympy literal limit.

  S2  (exact)  R(a) = 3 Omega_b a / (4 Omega_gamma) is EXACTLY linear in a
      (d(R/a)/da is a sympy literal zero).

  D1  (computed)  The sound horizon, integrated on the model's OWN
      background (F182/F188) to the (imported) Planck drag redshift,
      against Planck's own r_drag. 0.11%.
      CAVEAT (added after adversarial review, 2026-09-05): Omega_b, Omega_m,
      h, T_cmb feeding this integral are the SAME Planck-2018-fit values
      Planck's own analysis used to derive r_drag -- so this is
      substantially an INTERNAL-CONSISTENCY check (does the model's own
      integrator, fed Planck's own background parameters, reproduce
      Planck's own reported scale?), not an independent validation against
      a measurement unrelated to its inputs. It remains genuinely
      falsifiable -- a wrong integrator or a wrong E(a) would move this
      number sharply, see the z_drag_multiplier control below -- just not
      a test of the model against nature.

  D2  (computed)  The same model-native integral against the closed-form
      fitting formula ``cosmology_growth.transfer_eh98`` already uses
      internally for the sound horizon -- the model's own direct
      integration is ~16.4x closer to Planck than the fit already in the
      tree.

  D3  (computed / diagnostic)  Swap the model-native sound horizon into the
      (otherwise-still-EH98) shape formula and re-measure sigma_8. The
      shift is two orders of magnitude below the sigma_8-vs-Planck
      residual itself -- this LOCALISES that residual away from the
      sound-horizon scale.
      CAVEAT (added after adversarial review, 2026-09-05): this small shift
      holds only because both candidate s values (146.9, 149.8 Mpc) sit
      close together on a locally flat part of sigma_8(s). The true
      sensitivity is asymmetric (halving s: +1.23%; doubling s: -0.21%),
      so the honest reading is narrower than general insensitivity: sigma_8
      is insensitive to the narrow ~2% band the two candidate estimates
      occupy (itself tightly pinned by Planck), not to the sound-horizon
      scale in general. The localisation conclusion (the residual is not
      in this band) still stands.

  D4  (computed)  Hydrogen recombination redshift from the plain Saha
      equation, using the model's own Rydberg energy (F125) and the
      unchanged imported eta10 (S2 item iii). Reproduces the textbook
      ~25-30% Saha-vs-true bias (the omitted Peebles 1968 non-equilibrium
      correction) -- asserted to land IN that known band, not at zero
      (zero would mean the physics silently, and wrongly, vanished).

  Control (D9/H2, two independent handles):
    z_drag_multiplier != 1  ->  MUST redden D1 and D2.
    b_ion_multiplier   != 1  ->  MUST redden D4 (either direction).

Real arithmetic only (CLAUDE.md); no scipy integrator (D8).
"""
from __future__ import annotations

from casim.engine.interactions import cosmology_transfer_function as tf


def check_S1_sound_speed_radiation_limit() -> dict:
    r = tf.check_S1_sound_speed_radiation_limit()
    assert r["residual"] == "0", r["residual"]
    assert r["pass"]
    return r


def check_S2_R_exactly_linear_in_a() -> dict:
    r = tf.check_S2_R_exactly_linear_in_a()
    assert r["d(R_over_a)/da"] == "0", r["d(R_over_a)/da"]
    assert r["pass"]
    return r


def check_D1_sound_horizon_vs_planck() -> dict:
    r = tf.check_D1_sound_horizon_vs_planck()
    assert abs(r["relative_residual"]) < 0.01, r["relative_residual"]
    assert r["pass"]
    return r


def check_D2_model_native_vs_eh98_internal_fit() -> dict:
    r = tf.check_D2_model_native_vs_eh98_internal_fit()
    assert r["improvement_factor"] > 1.0, r["improvement_factor"]
    assert r["pass"]
    return r


def check_D3_sigma8_shift_localises_residual() -> dict:
    r = tf.check_D3_sigma8_shift_localises_residual()
    assert abs(r["relative_shift"]) < 0.01, r["relative_shift"]
    assert r["pass"]
    return r


def check_D4_saha_recombination_redshift() -> dict:
    r = tf.check_D4_saha_recombination_redshift()
    assert 0.15 < r["relative_bias"] < 0.40, r["relative_bias"]
    assert r["pass"]
    return r


def check_control_z_drag() -> dict:
    """C1a: z_drag_multiplier = 1.1 must redden D1 and D2."""
    r = tf.run(z_drag_multiplier=1.1)
    assert r["D1_sound_horizon_vs_planck"]["pass"] is False
    assert r["D2_model_native_vs_eh98_internal_fit"]["pass"] is False
    return r["control"]


def check_control_b_ion() -> dict:
    """C1b: b_ion_multiplier = 1.2 must redden D4."""
    r = tf.run(b_ion_multiplier=1.2)
    assert r["D4_saha_recombination_redshift"]["pass"] is False
    return r["control"]


CHECKS = [
    ("S1_sound_speed_radiation_limit", check_S1_sound_speed_radiation_limit),
    ("S2_R_exactly_linear_in_a", check_S2_R_exactly_linear_in_a),
    ("D1_sound_horizon_vs_planck", check_D1_sound_horizon_vs_planck),
    ("D2_model_native_vs_eh98_internal_fit", check_D2_model_native_vs_eh98_internal_fit),
    ("D3_sigma8_shift_localises_residual", check_D3_sigma8_shift_localises_residual),
    ("D4_saha_recombination_redshift", check_D4_saha_recombination_redshift),
]


def test_all_checks():
    for name, fn in CHECKS:
        fn()
    check_control_z_drag()
    check_control_b_ion()


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(tf.run(), indent=2, sort_keys=True, default=str))
