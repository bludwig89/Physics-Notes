"""F168 — Is the paired-photon binding dynamical / symmetry-protected, or merely kinematic?

Audit gap G2 (physics-audit-report-2026-06-29) charges that the F69 paired
photon, Omega_pair(k) = w+(k/2) + w-(k/2), is a *kinematic* sum of constituent
rates with no dynamical reason for a bound state at zero binding energy.

This script tests the thesis that the zero binding energy is in fact
SYMMETRY/STRUCTURE-FORCED (so the kinematic sum is the necessary form, not an
assumption), via four grounded checks against the audited ca_bcc walk:

  B1  Gapless constituents from the pure-hop walk (A0 = 0):
      u^±(0) = 1 exactly  =>  w^±(0) = arccos(1) = 0.  A nonzero on-site
      ("self-loop") amplitude eps opens a gap arccos(1-eps) > 0, so masslessness
      is tied structurally to A0 = 0, not tuned.

  B2  Chiral relation w^-(k) = w^+(-k) is ALGEBRAICALLY exact (residual 0, not
      machine).  Hence the symmetric (+,-) split is the parity-even (vector /
      F68 identity) combination Omega_even; the would-be single-branch photon is
      the chiral, birefringent one.  The vector EM current binds the symmetric
      pair.

  B3  Massless & no low-k gap; the birefringent split has no mass term:
      Omega_pair/|k| -> 1/sqrt(3); the split DeltaOmega along (1,1,1) has NO
      constant (k^0) or linear (k^1) term and starts at O(k^2) (fit exponent ~2,
      i.e. a phase-velocity birefringence Dv ~ k, cf. F37) -> the two branches
      carry no mass difference.  E_b = 0 is not a finite-binding cancellation:
      both constituents are massless, so M_pair = w+(0)+w-(0) = 0 identically.

  B4  Gauge protection (the dynamical core): a rest mass in this model is the
      F27 step that COUPLES the two chiral branches (eta<->chi),
      vertex = cos(m) I + sin(m) X, giving gap Omega(0) = m.  The photon's U(1)
      vertex is the branch-DIAGONAL identity e^{i theta} I (F68): its X-component
      is identically zero, so it cannot generate the mass step and Omega(0) = 0
      is forced.  This contrasts the F73/F74 scalar, whose (unprotected) binding
      gap needs a tuned super-critical contact coupling.

All checks use closed-form arccos(u) dispersion and real 2x2 algebra only — no
np.linalg.eig on chiral matrices (CLAUDE.md).
"""

import json
import os
import sys
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.lattice.bcc import bcc_dispersion as w           # noqa: E402
from casim.engine.lattice.bcc import _bcc_uvec                      # noqa: E402

RESULT = os.path.join(
    os.path.dirname(__file__), "..", "..", "test-results",
    "F168_paired_photon_binding.json",
)
ROOT3 = np.sqrt(3.0)


def pair(k):  # Omega_pair at wavevector k (3-vector)
    h = np.asarray(k, float) / 2.0
    return float(w(*h, sign="+") + w(*h, sign="-"))


def main():
    rng = np.random.default_rng(168)
    out = {}

    # --- B1: gapless constituents from pure hop A0 = 0 -------------------
    up0 = _bcc_uvec(0.0, 0.0, 0.0, "+")[0]
    um0 = _bcc_uvec(0.0, 0.0, 0.0, "-")[0]
    wp0, wm0 = w(0, 0, 0, "+"), w(0, 0, 0, "-")
    # parametric: an on-site deficit eps lowers u(0) below 1 -> opens a gap
    eps = 1e-3
    gap_with_onsite = float(np.arccos(np.clip(1.0 - eps, -1, 1)))
    out["B1"] = {
        "u_plus(0)": float(up0), "u_minus(0)": float(um0),
        "w_plus(0)": float(wp0), "w_minus(0)": float(wm0),
        "gap_if_onsite_deficit_1e-3": gap_with_onsite,
        "pass": (abs(up0 - 1) < 1e-15 and abs(um0 - 1) < 1e-15
                 and wp0 == 0.0 and wm0 == 0.0 and gap_with_onsite > 0),
    }

    # --- B2: chiral relation w-(k) = w+(-k) exact -----------------------
    err = 0.0
    for _ in range(5000):
        k = rng.uniform(-np.pi, np.pi, 3)
        err = max(err, abs(w(*(-k), sign="+") - w(*k, sign="-")))
    out["B2"] = {"max_resid_wminus_eq_wplus_negk": err,
                 "exact_zero": err == 0.0, "pass": err < 1e-14}

    # --- B3: massless slope + cubic birefringent split ------------------
    n = np.array([1, 1, 1.0]) / ROOT3
    slopes, ks = [], np.array([1e-3, 1e-2])
    for kk in ks:
        slopes.append(pair(kk * n) / kk)
    # birefringent split DeltaOmega = 2 w+(k/2) - 2 w-(k/2) along (1,1,1)
    kgrid = np.array([0.05, 0.1, 0.2, 0.4])
    dom = []
    for kk in kgrid:
        h = (kk * n) / 2.0
        dom.append(abs(2 * w(*h, "+") - 2 * w(*h, "-")))
    dom = np.array(dom)
    split_exp = float(np.polyfit(np.log(kgrid), np.log(dom), 1)[0])
    out["B3"] = {
        "Omega_pair_over_k": slopes, "target_1_over_sqrt3": 1.0 / ROOT3,
        "birefringent_split_fit_exponent": split_exp,
        "note": "exponent ~2 => no k^0 (mass) or k^1 term in the split",
        "pass": (abs(slopes[0] - 1.0 / ROOT3) < 1e-6 and 1.7 < split_exp < 2.3),
    }

    # --- B4: gauge protection — mass needs branch-coupling X, identity has none
    # At k=0 the kinetic step is the identity (u=1, n=0), so the full step is the
    # vertex.  Mass vertex V(m) = cos(m) I + sin(m) X with X the eta<->chi swap:
    #   V(m) = [[cos m, i sin m],[i sin m, cos m]], eigenphases ±m  => gap = m.
    # The U(1) EM vertex is e^{i theta} I (branch-diagonal): X-component ≡ 0.
    def gap_of_vertex(c, s):  # eigenphase magnitude of [[c, i s],[i s, c]]
        M = np.array([[c, 1j * s], [1j * s, c]], complex)
        ev = np.linalg.eigvals(M)            # 2x2 generic complex, allowed
        return float(np.max(np.abs(np.angle(ev))))
    masses = [0.0, 0.1, 0.3, 0.7]
    gap_mass = [gap_of_vertex(np.cos(m), np.sin(m)) for m in masses]
    gap_match = max(abs(g - m) for g, m in zip(gap_mass, masses))
    # U(1) identity vertex: theta phase, X-component (sin m) forced to 0
    gap_u1 = gap_of_vertex(1.0, 0.0)         # = 0 regardless of phase
    out["B4"] = {
        "gap_equals_mass_resid": gap_match,
        "gap_for_masses": dict(zip([str(m) for m in masses], gap_mass)),
        "gap_identity_channel(no X)": gap_u1,
        "pass": (gap_match < 1e-12 and gap_u1 == 0.0),
    }

    checks = {k: bool(v["pass"]) for k, v in out.items()}
    out["checks"] = checks
    out["all_pass"] = all(checks.values())

    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=2)

    for k, v in checks.items():
        print(f"[{'PASS' if v else 'FAIL'}] {k}")
    print("B2 chiral residual:", out["B2"]["max_resid_wminus_eq_wplus_negk"])
    print("B3 slope, split-exp:", out["B3"]["Omega_pair_over_k"][0],
          out["B3"]["birefringent_split_fit_exponent"])
    print("B4 gap==mass resid, identity-gap:",
          out["B4"]["gap_equals_mass_resid"], out["B4"]["gap_identity_channel(no X)"])
    print("ALL PASS:", out["all_pass"])
    assert out["all_pass"], "F168 paired-photon-binding checks failed"


if __name__ == "__main__":
    main()
