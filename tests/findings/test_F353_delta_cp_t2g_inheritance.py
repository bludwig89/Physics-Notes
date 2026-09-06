"""
test_F353_delta_cp_t2g_inheritance.py
======================================
F353 — Does F254's T_2g no-go inherit to the Dirac CP phase delta_CP?
open-derivations D4 / parameter #26 follow-up to F254/F236.

D4's own text states the working hypothesis: "delta_CP inherits F254's no-go
-- if the T_2g amplitudes are free, the phase built from them is too. Worth
one session to confirm that inheritance formally, which would move #26
ABSENT -> EXCLUDED (a result)". This module confirms it.

Result encoded here:
  - T1  D_2h transports a COMPLEX T_2g entry by the same real sign s_a s_b as
        a real one (magnitude fixed, phase shifted by 0 or pi only, never
        rotated) -- so F254's T1/T2 (three inequivalent irreps; democracy
        unprotected, order 2 of 8; F92 equipartition inapplicable) transfer
        to a complex T_2g VERBATIM, with no new group-theory argument needed.
  - T2  F254's own real NuFIT fit gives the standard Jarlskog invariant
        J = Im(U_e1 U_mu2 U_e2* U_mu1*) = 0 EXACTLY -- a consequence of using
        only real inputs, not a value protected by any symmetry.
  - T3  Turning on independent phases on TOP of F254's own fit magnitudes
        (1000 random draws) populates a continuous, generic, nonzero range of
        J with no special value picked out -- the phase sector is exactly as
        unprotected as the magnitude sector was (T2/T3-analogue).
  - T4  The phase-democratic point (t_xy=t_yz=t_zx, common magnitude AND
        phase) is likewise unprotected: it does NOT force J to any special
        value (same order-2-of-8 stabiliser as F254's magnitude-democracy).
  - T5  BONUS (severe, repo hygiene): building this check found that
        majorana.takagi_light_masses's branch test used numpy's DEFAULT
        absolute tolerance (atol=1e-8) against this model's light-neutrino
        mass scale (~1e-9 to 1e-20), so the complex branch was unreachable
        dead code -- any naive attempt at this exact check before today would
        have silently gotten J = 0 for every input. Fixed (scale-relative
        tolerance); F236/F254 untouched (both exclusively real).
  - T6  BONUS (minor, sign-convention only): the pre-fix complex branch (once
        T5 is fixed) used raw eigh(m_nu^dagger m_nu) eigenvectors directly as
        U; these equal conj(U_true) exactly, flipping the SIGN of J in an
        eigh-implementation-dependent way without corrupting its magnitude,
        and without ever checking the reconstruction m_nu = U diag(m) U^T.
        Fixed with a proper SVD-based Autonne-Takagi construction, verified
        to machine precision.

Verdict: delta_CP is GENUINELY FREE by the identical mechanism F254 proved for
the mixing angles -- ledger parameter #26: ABSENT -> EXCLUDED.
"""
from __future__ import annotations

import json
import os
import sys
import time

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from casim.engine.particles import derive_delta_cp_t2g as X  # noqa: E402

STAMP = "2026-09-03 - 00:40"


def check_T1_complex_transport():
    r = X.check_complex_amplitude_transport()
    return {
        "pass": r["pass"],
        "max_transport_deviation": r["max_transport_deviation"],
        "max_phase_shift_deviation_from_0_or_pi": r["max_phase_shift_deviation_from_0_or_pi"],
        "note": "D_2h transports a complex t_ab by the exact real sign s_a s_b "
                "(never rotates its phase) -- F254 T1/T2 transfer verbatim.",
    }


def check_T2_baseline_real_CP_conserving():
    r = X.check_baseline_real_is_CP_conserving()
    return {
        "pass": r["pass"],
        "J": r["J"], "sin_delta": r["sin_delta"], "residual": r["residual"],
        "note": "F254's own real NuFIT fit gives J=0 exactly -- a consequence "
                "of real-only inputs, not a symmetry-protected value.",
    }


def check_T3_phase_freedom():
    r = X.scan_phase_freedom()
    return {
        "pass": r["pass"],
        "J_min": r["min"], "J_max": r["max"], "J_std": r["std"],
        "frac_at_zero": r["frac_at_zero"],
        "note": "1000 random independent phase triples on F254's own fit "
                "magnitudes populate a continuous, generic, unprotected J.",
    }


def check_T4_democratic_phase_unprotected():
    r = X.check_democratic_phase_unprotected()
    return {
        "pass": r["pass"],
        "max_abs_J": r["max_abs_J"], "J_std": r["std"],
        "note": "phase-democracy (common magnitude+phase) is unprotected, "
                "same order-2-of-8 stabiliser as F254's magnitude-democracy.",
    }


def check_T5_branch_selection_bug():
    r = X.check_T5_branch_selection_bug()
    return {
        "pass": r["pass"],
        "all_took_real_branch_pre_fix": r["all_took_real_branch"],
        "max_abs_J_pre_fix": r["max_abs_J_pre_fix"],
        "note": "pre-fix code used np.allclose(imag,0) at numpy's default "
                "atol=1e-8 >> this model's mass scale, so it always took the "
                "real branch and silently returned J=0 for every phase.",
    }


def check_T6_sign_convention_only():
    r = X.check_T6_sign_convention_only()
    return {
        "pass": r["pass"],
        "max_abs_J_fixed_plus_J_raw": r["max_abs_J_fixed_plus_J_raw"],
        "note": "raw eigh(H) eigenvectors equal conj(U_true): J_raw=-J_fixed "
                "to machine precision (sign-convention only, not a magnitude "
                "error); the fixed path additionally verifies reconstruction.",
    }


CHECKS = [
    ("T1_complex_transport", check_T1_complex_transport),
    ("T2_baseline_real_CP_conserving", check_T2_baseline_real_CP_conserving),
    ("T3_phase_freedom", check_T3_phase_freedom),
    ("T4_democratic_phase_unprotected", check_T4_democratic_phase_unprotected),
    ("T5_branch_selection_bug", check_T5_branch_selection_bug),
    ("T6_sign_convention_only", check_T6_sign_convention_only),
]


def main():
    t0 = time.time()
    results = {}
    n_pass = 0
    for name, fn in CHECKS:
        r = fn()
        results[name] = r
        ok = r.get("pass", False)
        n_pass += int(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {r.get('note', '')}")
    summary = {
        "finding": "F353",
        "stamp": STAMP,
        "n_pass": n_pass,
        "n_total": len(CHECKS),
        "elapsed_s": round(time.time() - t0, 2),
        "results": results,
    }
    out_dir = os.path.join(ROOT, "test-results")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "F353_delta_cp_t2g_inheritance.json")
    with open(out, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"\n{n_pass}/{len(CHECKS)} PASS  ({summary['elapsed_s']} s)  -> {out}")
    return n_pass == len(CHECKS)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
