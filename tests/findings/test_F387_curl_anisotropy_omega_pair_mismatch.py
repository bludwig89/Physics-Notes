"""F387 -- the Ĉ(k) direction anisotropy and the Ω_pair(k)/|C_odd(k)|
sourcing mismatch: a Stage-4 design fix (docs/roadmaps/photon-fermion-coupling.md).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.em_photon_sourcing.check_em_photon_sourcing` (record
`F387-curl-anisotropy-omega-pair-mismatch`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F387-curl-anisotropy-omega-pair-mismatch
    casim test --id F387-curl-anisotropy-omega-pair-mismatch --param use_split_for_no_monopole_check=false   # red

Twelve legs (see `em_photon_sourcing.check_em_photon_sourcing`'s own
docstring and `findings/F387-curl-anisotropy-omega-pair-mismatch.md` for the
full derivation of each):

    curl_direction_matches_cubic_axis           angle(Ĉ,k̂)=0 on-axis
    curl_direction_face_diagonal_90deg          angle=90° on a face diagonal
    curl_direction_body_diagonal_arccos_1_3     angle=arccos(1/3) on the body
                                                 diagonal
    curl_direction_anisotropy_stable_with_L     angle unchanged L=16->64 --
                                                 a continuum-limit property,
                                                 not a finite-lattice artifact
    curl_magnitude_isotropic                    |C|/|k| axis~=body to O(k^2)
    omega_pair_matches_curl_at_small_k          Ω_pair(k)/|C_odd(k)| -> 1
    omega_pair_diverges_from_curl_away_from_small_k
                                                 ratio grows well past 1 near
                                                 the BZ edge
    rotation_commutes_with_TL_projection        photon_step_spectral commutes
                                                 exactly with the Ĉ(k)
                                                 transverse/longitudinal split
    naive_sourcing_violates_no_monopole         the roadmap's own Stage-4
                                                 sketch (E+=g.J unprojected)
                                                 develops iĈ.B!=0
    split_sourcing_preserves_no_monopole        the fix: iĈ.B stays ~0
    split_sourcing_couples_charge_into_EL       the fix still carries the
                                                 charge's own Coulomb field
    split_sourcing_reduces_to_free_rotation_when_uncharged
                                                 J=0 -> identical to plain
                                                 photon_step_spectral
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import em_photon_sourcing as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_em_photon_sourcing()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  angle_body_diagonal_deg={res['angle_body_diagonal_deg']:.6f}  "
          f"ratio_omega_pair_over_Codd_edge_k={res['ratio_omega_pair_over_Codd_edge_k']:.6f}  "
          f"naive_final_monopole_residual={res['naive_final_monopole_residual']:.3e}  "
          f"split_final_monopole_residual={res['split_final_monopole_residual']:.3e}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F387_curl_anisotropy_omega_pair_mismatch.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F387 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
