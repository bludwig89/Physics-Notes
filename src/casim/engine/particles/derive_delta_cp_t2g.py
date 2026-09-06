"""
derive_delta_cp_t2g.py — does F254's T_2g no-go inherit to the Dirac CP phase?
===============================================================================

open-derivations D4 / parameter #26 follow-up to F254.  F254 proved that the
D_2h stabiliser of the E_g-broken vacuum acts on the T_2g triplet
(t_xy, t_yz, t_zx) as three INEQUIVALENT nontrivial 1-d irreps (B_1g, B_2g,
B_3g), so no residual symmetry relates the three (real) mixing amplitudes and
the F92 equipartition selector cannot apply -- the PMNS ANGLES are genuinely
free.  D4's own text states the working (unconfirmed) hypothesis: "delta_CP
inherits F254's no-go -- if the T_2g amplitudes are free, the phase built from
them is too."

This module checks that inheritance directly, in two parts:

  A.  GROUP THEORY (formal, exact).  D_2h acts on a T_2g entry t_ab by the real
      sign s_a s_b -- REGARDLESS of whether t_ab is real or complex.  A real
      orthogonal similarity transform T -> S T S^T can only flip the overall
      SIGN of a complex number (equivalently: it shifts its phase by 0 or pi
      exactly); it cannot rotate a phase to any other value.  So F254's T1
      (three inequivalent irreps) and T2 (democracy unprotected, order 2 of 8;
      equipartition inapplicable) transfer to a complex T_2g VERBATIM, with
      NO new argument needed -- the phase content of each amplitude is exactly
      as unrelated by the residual symmetry as the magnitude is.

  B.  NUMERICS (the physical content).  The Dirac CP phase enters the model
      only through the phases of (t_xy, t_yz, t_zx), via the standard
      rephasing-invariant Jarlskog combination J = Im(U_e1 U_mu2 U_e2* U_mu1*)
      built from the light-neutrino PMNS matrix U (F236/F254's own
      takagi_light_masses / pmns_angles pipeline).  Starting from F254's own
      NuFIT-fit amplitudes (which reproduce the 3 angles with a REAL T_2g, so
      J = 0 there identically -- CP conservation is a consequence of that
      construction using only real inputs, not a prediction forced by any
      symmetry) this module turns on independent phases on top of those SAME
      magnitudes and shows J is generic, continuous and NOT protected at any
      special value by the D_2h stabiliser -- neither the fully "democratic"
      phase choice (all three phases equal) nor any single-channel phase
      choice is picked out, exactly paralleling F254's T2/T3 for the angles.

  BONUS (repo hygiene, F353 T5/T6).  Building this check surfaced TWO real
  pre-existing defects in casim.engine.particles.majorana.takagi_light_masses,
  of very different severity, both fixed here (F236/F254 are untouched by
  either -- both are exclusively real, and use ONLY the real branch):

    T5 (severe).  The branch test `np.allclose(m_nu.imag, 0.0)` was called
       with numpy's DEFAULT absolute tolerance (atol=1e-8).  This model's
       light-neutrino m_nu is ~1e-9 to 1e-20 in these units, so that test
       silently classified EVERY physically-scaled complex m_nu as "real" and
       took the real-only branch, discarding all phase content.  The complex
       branch was unreachable dead code for any realistic input -- so any
       naive attempt to read a CP-violating observable off this pipeline
       before today would have gotten a spurious, input-independent J = 0,
       not a genuine null result.  Fixed by comparing the imaginary part to
       the matrix's OWN scale rather than an absolute constant.

    T6 (minor, sign-convention only).  Once T5 is fixed, the pre-existing
       complex branch used the raw eigenvectors of m_nu^dagger m_nu directly
       as U.  These are provably equal to conj(U_true) (the true Takagi
       factor's entrywise complex conjugate) -- which reproduces every
       modulus |U_ij| exactly (so every PMNS ANGLE is unaffected) but flips
       the SIGN of the Jarlskog invariant / delta_CP in a way that depends on
       eigh's internal, unspecified per-eigenvector phase convention, and was
       never checked against the reconstruction identity m_nu = U diag(m) U^T
       at all.  Fixed with a proper SVD-based Autonne-Takagi construction
       (Horn & Johnson, *Matrix Analysis*, Cor. 4.4.4) whose reconstruction
       is verified to machine precision and folded into the returned
       residual.

  T5 is the one that matters operationally (it is what makes ANY delta_CP /
  Jarlskog computation on this pipeline trustworthy at all); T6 is a hygiene
  improvement (a well-defined sign, a checked reconstruction) layered on top.

Run:  python3 derive_delta_cp_t2g.py
"""
from __future__ import annotations

import itertools
import numpy as np

from casim.engine.particles import majorana as cm
from casim.engine.particles import derive_t2g_pmns as D2G

DEG = np.pi / 180.0


# ---------------------------------------------------------------------------
# A.  D_2h acts on a COMPLEX T_2g entry by the same real sign -- formal check
# ---------------------------------------------------------------------------

def d2h_elements():
    return [np.diag(s) for s in itertools.product((1, -1), repeat=3)]


def check_complex_amplitude_transport(seed=0, n=200):
    """For random complex t_ab and every S in D_2h, verify (S T S^T)_ab is
    EXACTLY the real sign s_a s_b times t_ab (magnitude unchanged, phase
    shifted by 0 or pi only -- never rotated to an intermediate value).

    This is the formal content of "F254's T1/T2 transfer to complex T_2g
    verbatim": the group's action never sees the phase, so it can no more
    relate/fix three phases than it could relate/fix three magnitudes.
    """
    rng = np.random.default_rng(seed)
    idx = {"t_xy": (0, 1), "t_yz": (1, 2), "t_zx": (2, 0)}
    max_dev = 0.0
    max_phase_shift_dev = 0.0
    for _ in range(n):
        r = rng.uniform(0.1, 5.0, 3)
        phi = rng.uniform(0.0, 2 * np.pi, 3)
        t = {name: r[k] * np.exp(1j * phi[k]) for k, name in enumerate(idx)}
        T = np.zeros((3, 3), dtype=complex)
        for name, (a, b) in idx.items():
            T[a, b] = t[name]
            T[b, a] = t[name]
        for S in d2h_elements():
            Tp = S @ T @ S.T
            for name, (a, b) in idx.items():
                sign = S[a, a] * S[b, b]
                predicted = sign * t[name]
                max_dev = max(max_dev, abs(Tp[a, b] - predicted))
                shift = np.angle(Tp[a, b] / t[name]) if sign > 0 else \
                    np.angle(-Tp[a, b] / t[name])
                max_phase_shift_dev = max(max_phase_shift_dev, abs(shift))
    return {
        "max_transport_deviation": float(max_dev),
        "max_phase_shift_deviation_from_0_or_pi": float(max_phase_shift_dev),
        "pass": bool(max_dev < 1e-10 and max_phase_shift_dev < 1e-8),
    }


def analyse_irreps_complex():
    """The F254 character analysis (real signs only) -- unchanged by field
    extension. Included so the complex-inheritance claim cites its own copy
    of T1/T2 rather than merely reading F254's."""
    return D2G.analyse_irreps()


# ---------------------------------------------------------------------------
# B.  Numerics: J is generic and unprotected once T_2g carries phases
# ---------------------------------------------------------------------------

def f254_fit_point():
    """F254's own full 3-amplitude NuFIT fit (real): (delta_nu_deg, t_xy, t_yz, t_zx)."""
    full = D2G.fit_full()
    return tuple(full["params"])


def _mnu_complex(delta_nu_deg, t_xy, t_yz, t_zx):
    dl = D2G._light_diag(delta_nu_deg)
    sc = np.mean(np.abs(dl))
    off = np.array([[0, t_xy, t_zx], [t_xy, 0, t_yz], [t_zx, t_yz, 0]],
                    dtype=complex) * sc
    return np.diag(dl).astype(complex) + off


def check_baseline_real_is_CP_conserving():
    """F254's construction (real T_2g) gives J = 0 EXACTLY -- a consequence of
    using only real inputs, not a D_2h-protected value (part B's phase scan
    shows nearby complex points are generically NOT at J = 0)."""
    dnu, txy, tyz, tzx = f254_fit_point()
    m = _mnu_complex(dnu, txy, tyz, tzx)
    masses, U, res = cm.takagi_light_masses(m)
    sind, J = cm.sin_delta_cp(U)
    return {"J": J, "sin_delta": sind, "residual": res,
            "pass": bool(abs(J) < 1e-8 and res < 1e-6)}


def scan_phase_freedom(seed=1, n=1000):
    """At F254's own fit magnitudes, draw independent random phases on the
    three amplitudes and show J populates a continuous, nonzero-generic
    range -- no D_2h-protected value (T3-analogue for the phase sector)."""
    dnu, txy, tyz, tzx = f254_fit_point()
    rng = np.random.default_rng(seed)
    Js = []
    for _ in range(n):
        p1, p2, p3 = rng.uniform(0, 2 * np.pi, 3)
        m = _mnu_complex(dnu, txy * np.exp(1j * p1), tyz * np.exp(1j * p2),
                          tzx * np.exp(1j * p3))
        _, U, _ = cm.takagi_light_masses(m)
        _, J = cm.sin_delta_cp(U)
        Js.append(J)
    Js = np.array(Js)
    frac_zero = float(np.mean(np.abs(Js) < 1e-8))
    return {
        "n": n, "min": float(Js.min()), "max": float(Js.max()),
        "std": float(Js.std()), "frac_at_zero": frac_zero,
        "pass": bool(Js.std() > 1e-3 and frac_zero < 0.01),
    }


def check_democratic_phase_unprotected(seed=2, n=300):
    """Phase-democracy (t_xy=t_yz=t_zx = r e^{i phi}) is exactly as
    unprotected as magnitude-democracy was in F254 T2 (same order-2
    stabiliser): scanning (r, phi) gives a generic nonzero, continuously
    varying J -- no single value is picked out by the residual symmetry."""
    dnu, _, _, _ = f254_fit_point()
    rng = np.random.default_rng(seed)
    Js = []
    for _ in range(n):
        r = rng.uniform(0.1, 5.0)
        phi = rng.uniform(0, 2 * np.pi)
        t = r * np.exp(1j * phi)
        m = _mnu_complex(dnu, t, t, t)
        _, U, _ = cm.takagi_light_masses(m)
        _, J = cm.sin_delta_cp(U)
        Js.append(J)
    Js = np.array(Js)
    return {
        "n": n, "max_abs_J": float(np.abs(Js).max()), "std": float(Js.std()),
        "pass": bool(np.abs(Js).max() > 1e-3),
    }


# ---------------------------------------------------------------------------
# C.  Bonus: reproduce and characterise the two pre-existing Takagi defects
# ---------------------------------------------------------------------------

def _pre_fix_takagi(m_nu):
    """Literal reproduction of takagi_light_masses's complex path exactly as
    it read before F353 (T5: allclose at numpy's default atol=1e-8; T6: raw
    eigh(m_nu^dagger m_nu) eigenvectors used directly as U, no phase fix)."""
    m_nu = np.asarray(m_nu)
    if np.allclose(m_nu.imag, 0.0):   # T5: numpy DEFAULT atol=1e-8
        M = m_nu.real
        w, V = np.linalg.eigh(M)
        masses = np.abs(w)
        order = np.argsort(masses)
        return masses[order], V[:, order], "REAL_BRANCH"
    H = m_nu.conj().T @ m_nu          # T6: no Takagi phase correction
    w2, V = np.linalg.eigh(H)
    masses = np.sqrt(np.clip(w2, 0.0, None))
    order = np.argsort(masses)
    return masses[order], V[:, order], "COMPLEX_BRANCH_UNCORRECTED"


def _raw_eigh_takagi(m_nu):
    """T6 in isolation (T5 already fixed): raw eigh(H) eigenvectors, still no
    phase correction, always reaching the complex branch."""
    H = m_nu.conj().T @ m_nu
    w2, V = np.linalg.eigh(H)
    masses = np.sqrt(np.clip(w2, 0.0, None))
    order = np.argsort(masses)
    return masses[order], V[:, order]


def check_T5_branch_selection_bug(seed=3, n=50):
    """T5 (severe): pre-fix code takes the REAL branch on every draw at this
    model's physical mass scale, discarding all phase content, so J = 0
    identically no matter what phase is injected -- a spurious, silent
    null result, not a genuine one."""
    dnu, txy, tyz, tzx = f254_fit_point()
    rng = np.random.default_rng(seed)
    branches, Js = [], []
    for _ in range(n):
        p1, p2, p3 = rng.uniform(0, 2 * np.pi, 3)
        m = _mnu_complex(dnu, txy * np.exp(1j * p1), tyz * np.exp(1j * p2),
                          tzx * np.exp(1j * p3))
        _, U, branch = _pre_fix_takagi(m)
        branches.append(branch)
        Js.append(cm.jarlskog_invariant(U))
    Js = np.array(Js)
    all_real_branch = all(b == "REAL_BRANCH" for b in branches)
    return {
        "n": n, "all_took_real_branch": all_real_branch,
        "max_abs_J_pre_fix": float(np.abs(Js).max()),
        "pass": bool(all_real_branch and np.abs(Js).max() < 1e-12),
    }


def check_T6_sign_convention_only(seed=4, n=30):
    """T6 (minor, once T5 is fixed): raw eigh(H) eigenvectors equal
    conj(U_true) up to the usual per-eigenvector phase freedom, so
    J_raw = -J_fixed to machine precision -- a sign-convention artifact, not
    a magnitude error; the fixed path additionally VERIFIES the
    reconstruction m_nu = U diag(m) U^T, which the raw path never checked."""
    dnu, txy, tyz, tzx = f254_fit_point()
    rng = np.random.default_rng(seed)
    max_sum_abs = 0.0
    for _ in range(n):
        p1, p2, p3 = rng.uniform(0, 2 * np.pi, 3)
        m = _mnu_complex(dnu, txy * np.exp(1j * p1), tyz * np.exp(1j * p2),
                          tzx * np.exp(1j * p3))
        _, U_fixed, _ = cm.takagi_light_masses(m)
        _, U_raw = _raw_eigh_takagi(m)
        J_fixed = cm.jarlskog_invariant(U_fixed)
        J_raw = cm.jarlskog_invariant(U_raw)
        max_sum_abs = max(max_sum_abs, abs(J_fixed + J_raw))
    return {"n": n, "max_abs_J_fixed_plus_J_raw": float(max_sum_abs),
            "pass": bool(max_sum_abs < 1e-10)}


# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("A. D_2h transport of a COMPLEX T_2g entry -- formal check")
    r = check_complex_amplitude_transport()
    print(f"   max |S T S^T - sign*t| = {r['max_transport_deviation']:.3e}")
    print(f"   max phase-shift deviation from {{0, pi}} = "
          f"{r['max_phase_shift_deviation_from_0_or_pi']:.3e}")
    print(f"   PASS = {r['pass']}  (=> T1/T2 transfer to complex T_2g verbatim)")

    print("=" * 72)
    print("B. baseline (F254 real fit): J should be exactly 0")
    b = check_baseline_real_is_CP_conserving()
    print(f"   J={b['J']:.3e}  residual={b['residual']:.3e}  PASS={b['pass']}")

    print("   phase-freedom scan (1000 random phase triples, same magnitudes)")
    s = scan_phase_freedom()
    print(f"   J in [{s['min']:.4f}, {s['max']:.4f}], std={s['std']:.4f}, "
          f"frac at J~0 = {s['frac_at_zero']:.3f}  PASS={s['pass']}")

    print("   democratic-phase scan (300 draws)")
    dch = check_democratic_phase_unprotected()
    print(f"   max|J|={dch['max_abs_J']:.4f}  std={dch['std']:.4f}  PASS={dch['pass']}")

    print("=" * 72)
    print("C. bonus -- two pre-existing Takagi defects, characterised")
    t5 = check_T5_branch_selection_bug()
    print(f"   T5 (severe, branch selection): all_real_branch="
          f"{t5['all_took_real_branch']}  max|J|_pre_fix={t5['max_abs_J_pre_fix']:.3e}  "
          f"PASS={t5['pass']}")
    t6 = check_T6_sign_convention_only()
    print(f"   T6 (minor, sign only): max|J_fixed + J_raw|="
          f"{t6['max_abs_J_fixed_plus_J_raw']:.3e}  PASS={t6['pass']}")

    print("=" * 72)
    print("VERDICT: F254's D_2h no-go inherits to the Dirac CP phase. No")
    print("residual symmetry or F92-equipartition mechanism fixes any T_2g")
    print("phase (part A, exact); the resulting Jarlskog invariant is generic,")
    print("continuous and unprotected at every tested slice, including the")
    print("phase-democratic point (part B). delta_CP: ABSENT -> EXCLUDED.")
    return {"A_transport": r, "B_baseline": b, "B_phase_scan": s,
            "B_democratic": dch, "C_T5": t5, "C_T6": t6}


if __name__ == "__main__":
    main()
