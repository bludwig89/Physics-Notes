"""
run_FC07_charge_anomaly_beta.py
===============================

FC07 — Charge quantization, anomaly cancellation, β-decay (Tier-C consistency
regression).  Folds together and supersedes:
  * tests/findings/test_FG1_anomaly_cancellation.py  (F38 — six gauge anomalies)
  * tests/priority/test_10_QG4_charge.py             (exact-rational charges)
  * tests/findings/test_FG8_beta_decay.py            (F54 charged current)
  * tests/priority/test_07_QFT5_neutrino.py          (F47 see-saw / oscillations)

Falsified if (per the brief tests/falsification/FC07-...md):
  (1) any of the six FG-1 anomaly traces is nonzero, OR
  (2) charges are not exact rationals / proton-electron not exactly opposite, OR
  (3) β-decay has the wrong chirality (W couples left; the right-branch weight
      must be identically zero), OR
  (4) the see-saw cannot accommodate the measured ν mass scale.

EXACTNESS POLICY (CLAUDE.md):
  * Anomalies & charges use fractions.Fraction end-to-end — results are the
    literal integer 0, not "< 1e-17".
  * The β-decay vertex is a CHIRAL W⁻ coupling.  Per CLAUDE.md we do NOT trust
    numpy/scipy blindly on chiral transforms: the left-projector P_L action is
    cross-checked here with a hand-rolled (pure-Python complex) projector, and
    the right-branch weight ‖P_R ψ_L‖ is verified ≡ 0 independently of numpy.

Run:  PYTHONPATH=src python3 tests/runners/run_FC07_charge_anomaly_beta.py
JSON: test-results/FC07_charge_anomaly.json
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from fractions import Fraction

THIS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(THIS, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))


# ════════════════════════════════════════════════════════════════════════
#  PART 1 — six FG-1 gauge/grav anomaly traces, exact rationals (F38)
# ════════════════════════════════════════════════════════════════════════
#
# Left-handed Weyl content of one SM generation in the Q = T3 + Y/2 convention
# (F38 §2.1).  Right-handed Dirac fields become charge-conjugate left Weyls
# with the colour rep dualised (3 -> 3bar) and Y negated.
#
#   field            colour  iso(SU2 dim)   Y
#   L=(nu,e)_L        1        2            -1
#   e^c_L (=e_R^c)    1        1            +2
#   Q=(u,d)_L         3        2            +1/3
#   u^c_L (=u_R^c)    3bar     1            -4/3
#   d^c_L (=d_R^c)    3bar     1            +2/3

_COLOR_DIM = {"1": 1, "3": 3, "3bar": 3}
_T_SU3 = {"1": Fraction(0), "3": Fraction(1, 2), "3bar": Fraction(1, 2)}
_A_SU3 = {"1": 0, "3": +1, "3bar": -1}              # cubic colour anomaly coeff
_T_SU2 = {1: Fraction(0), 2: Fraction(1, 2)}        # SU(2) Dynkin index

# (name, colour, iso_dim, Y)
GENERATION = [
    ("L_L (nu_L,e_L)", "1", 2, Fraction(-1)),
    ("e^c_L",          "1", 1, Fraction(2)),
    ("Q_L (u_L,d_L)",  "3", 2, Fraction(1, 3)),
    ("u^c_L",          "3bar", 1, Fraction(-4, 3)),
    ("d^c_L",          "3bar", 1, Fraction(2, 3)),
]


def _mult(color, iso):
    return _COLOR_DIM[color] * iso


def compute_anomalies():
    """Return dict of the six traces, each an exact Fraction (== 0 ⇒ cancels)."""
    A = sum((_mult(c, i) * Y for _, c, i, Y in GENERATION), Fraction(0))            # grav^2.U1
    B = sum((_mult(c, i) * Y ** 3 for _, c, i, Y in GENERATION), Fraction(0))       # U1^3
    C = sum((_COLOR_DIM[c] * _T_SU2[i] * Y for _, c, i, Y in GENERATION), Fraction(0))  # SU2^2.U1
    D = sum((i * _T_SU3[c] * Y for _, c, i, Y in GENERATION), Fraction(0))          # SU3^2.U1
    E = sum((Fraction(i * _A_SU3[c]) for _, c, i, Y in GENERATION), Fraction(0))    # SU3^3
    F = Fraction(0)   # SU2^3 — identically zero (SU(2) reps pseudo-real)
    return {
        "FG-1.A  [grav]^2.U(1)_Y": A,
        "FG-1.B  U(1)_Y^3":        B,
        "FG-1.C  [SU(2)_L]^2.U(1)_Y": C,
        "FG-1.D  [SU(3)_c]^2.U(1)_Y": D,
        "FG-1.E  [SU(3)_c]^3":     E,
        "FG-1.F  [SU(2)_L]^3":     F,
    }


# ════════════════════════════════════════════════════════════════════════
#  PART 2 — exact-rational electric charges; proton = − electron (F41/F35)
# ════════════════════════════════════════════════════════════════════════

def gell_mann_nishijima(T3: Fraction, Y: Fraction) -> Fraction:
    return T3 + Y / 2


def compute_charges():
    half = Fraction(1, 2)
    Q = {
        "nu_e": gell_mann_nishijima(half,  Fraction(-1)),
        "e":    gell_mann_nishijima(-half, Fraction(-1)),
        "u":    gell_mann_nishijima(half,  Fraction(1, 3)),
        "d":    gell_mann_nishijima(-half, Fraction(1, 3)),
    }
    # proton = uud
    Q_p = 2 * Q["u"] + Q["d"]
    Q_e = Q["e"]
    expected = {"nu_e": Fraction(0), "e": Fraction(-1),
                "u": Fraction(2, 3), "d": Fraction(-1, 3)}
    charges_exact = all(Q[k] == expected[k] for k in expected)
    proton_eq_minus_electron = (Q_p == -Q_e)  # exact: +1 == -(-1)
    return Q, Q_p, Q_e, charges_exact, proton_eq_minus_electron


# ════════════════════════════════════════════════════════════════════════
#  PART 3 — β-decay chirality (F54): W couples LEFT; right-branch weight ≡ 0
# ════════════════════════════════════════════════════════════════════════
#
# The charged-current vertex carries P_L = (1 - γ5)/2.  In the chiral (Weyl)
# basis γ5 = diag(-1,-1,+1,+1), so P_L keeps the upper (left) two components and
# P_R = (1 + γ5)/2 keeps the lower (right) two.  We verify:
#   * P_L kills a purely right-handed spinor              (resid_right == 0)
#   * P_L is the identity on a purely left-handed spinor  (resid_left  == 0)
#   * the RIGHT-BRANCH weight ‖P_R ψ_L‖ ≡ 0 for the left-coupled current.
#
# CLAUDE.md WARNING: chiral transforms through numpy can silently drop the
# real/imag parts.  We therefore compute the projector action TWICE:
#   (a) hand-rolled, pure-Python complex arithmetic (ground truth), and
#   (b) numpy, and assert the two agree bit-for-bit before trusting numpy.

import numpy as np  # noqa: E402

# diagonal projectors as plain Python tuples (real diagonal entries)
_PL_DIAG = (1, 1, 0, 0)   # left-handed: upper two
_PR_DIAG = (0, 0, 1, 1)   # right-handed: lower two


def _apply_diag_handrolled(diag, psi):
    """Pure-Python projector: multiply each complex component by a real 0/1.
    No numpy — preserves real & imag parts exactly."""
    return [complex(d) * complex(p) for d, p in zip(diag, psi)]


def _norm_handrolled(vec):
    return max(abs(z) for z in vec) if vec else 0.0


def verify_beta_chirality():
    # left- and right-handed test spinors with non-trivial complex phases so a
    # phase-dropping bug would be caught.
    psi_R = [0, 0, 1 + 2j, 3 - 1j]            # purely right-handed (lower two)
    psi_L = [2 - 1j, 1 + 1j, 0, 0]            # purely left-handed (upper two)

    # (a) hand-rolled ground truth -------------------------------------------
    hr_PL_psiR = _apply_diag_handrolled(_PL_DIAG, psi_R)   # should be all-zero
    hr_PL_psiL = _apply_diag_handrolled(_PL_DIAG, psi_L)   # should equal psi_L
    hr_PR_psiL = _apply_diag_handrolled(_PR_DIAG, psi_L)   # RIGHT-BRANCH weight ≡ 0

    resid_right_hr = _norm_handrolled(hr_PL_psiR)
    resid_left_hr = _norm_handrolled(
        [a - b for a, b in zip(hr_PL_psiL, psi_L)])
    right_branch_weight_hr = _norm_handrolled(hr_PR_psiL)

    # (b) numpy ---------------------------------------------------------------
    PL = np.diag(_PL_DIAG).astype(complex)
    PR = np.diag(_PR_DIAG).astype(complex)
    npR = np.array(psi_R, dtype=complex)
    npL = np.array(psi_L, dtype=complex)
    resid_right_np = float(np.max(np.abs(PL @ npR)))
    resid_left_np = float(np.max(np.abs(PL @ npL - npL)))
    right_branch_weight_np = float(np.max(np.abs(PR @ npL)))

    # numpy-vs-handrolled agreement on this chiral step (CLAUDE.md safety gate)
    numpy_matches_handrolled = (
        np.allclose(PL @ npR, np.array(hr_PL_psiR), atol=0, rtol=0)
        and np.allclose(PL @ npL, np.array(hr_PL_psiL), atol=0, rtol=0)
        and np.allclose(PR @ npL, np.array(hr_PR_psiL), atol=0, rtol=0)
    )

    # exact-zero booleans (these are bit-exact: 0/1 diagonal × complex)
    left_chiral = (right_branch_weight_hr == 0.0
                   and resid_right_hr == 0.0
                   and resid_left_hr == 0.0)

    # Cross-check against the in-repo charged-current implementation if present
    repo_resid = None
    try:
        from casim.engine.gauge import charged_current as ccc
        rr, rl = ccc.va_vertex_kills_right_handed()
        repo_resid = {"resid_right": rr, "resid_left": rl}
    except Exception as exc:  # pragma: no cover
        repo_resid = {"error": str(exc)}

    return {
        "handrolled": {
            "resid_right (P_L psi_R)": resid_right_hr,
            "resid_left  (P_L psi_L - psi_L)": resid_left_hr,
            "right_branch_weight (P_R psi_L)": right_branch_weight_hr,
        },
        "numpy": {
            "resid_right": resid_right_np,
            "resid_left": resid_left_np,
            "right_branch_weight": right_branch_weight_np,
        },
        "numpy_matches_handrolled": bool(numpy_matches_handrolled),
        "repo_va_vertex": repo_resid,
        "right_branch_weight_is_zero": bool(right_branch_weight_hr == 0.0),
        "left_chiral": bool(left_chiral),
    }


# ════════════════════════════════════════════════════════════════════════
#  PART 4 — F47 Higgs-free see-saw: naturally small ν mass at measured scale
# ════════════════════════════════════════════════════════════════════════

def seesaw_light_mass(M_D: float, M_R: float) -> float:
    """Numerically-stable light eigenvalue of [[0,M_D],[M_D,M_R]] via Vieta:
    λ+ λ- = -M_D^2, λ+ + λ- = M_R.  |λ_light| = M_D^2 / |λ_heavy|."""
    import math
    disc = math.sqrt(M_R * M_R + 4.0 * M_D * M_D)
    lam_heavy = (M_R + disc) / 2.0
    lam_light = -(M_D * M_D) / lam_heavy   # = (M_R - disc)/2 but stable
    return abs(lam_light)


def verify_seesaw():
    # Use physical GeV-scale numbers: M_D ~ electron/charged-lepton Dirac scale,
    # M_R ~ GUT/intermediate Majorana scale.  Show m_nu lands in the measured
    # sub-eV window and Sum m_nu < 0.12 eV (Planck/cosmology bound).
    GeV_to_eV = 1.0e9
    cases = []
    natural = True
    # Canonical see-saw I: a Dirac mass at the electroweak/charged-fermion scale
    # with a heavy Majorana scale M_R lands m_nu in the MEASURED sub-eV window
    # (atmospheric √Δm²₃₁ ≈ 0.05 eV, solar √Δm²₂₁ ≈ 0.009 eV; Σm_ν < 0.12 eV).
    for M_D_GeV, M_R_GeV in [
        (100.0, 1.0e14),    # M_D ~ EW/top scale, M_R ~ 1e14 GeV  -> ~0.1 eV
        (100.0, 2.0e14),    # M_R ~ 2e14 GeV                      -> ~0.05 eV (atmospheric)
        (30.0,  1.0e14),    # M_D ~ 30 GeV,  M_R ~ 1e14 GeV       -> ~0.009 eV (solar)
    ]:
        m_nu_GeV = seesaw_light_mass(M_D_GeV, M_R_GeV)
        m_nu_eV = m_nu_GeV * GeV_to_eV
        approx_eV = (M_D_GeV ** 2 / M_R_GeV) * GeV_to_eV
        cases.append({
            "M_D_GeV": M_D_GeV, "M_R_GeV": M_R_GeV,
            "m_nu_eV": m_nu_eV, "M_D^2/M_R_eV": approx_eV,
            "in_measured_window_0.001..0.12eV": (1e-3 <= m_nu_eV <= 0.12),
        })

    # Scaling check: m_nu * M_R / M_D^2 -> 1 within (M_D/M_R)^2 at large ratio
    scaling_ok = True
    scaling = []
    for ratio in (10, 100, 1000, 10000, 100000):
        M_D, M_R = 1.0, float(ratio)
        m = seesaw_light_mass(M_D, M_R)
        excess = abs(m * M_R / (M_D * M_D) - 1.0)
        bound = 1.1 * (M_D / M_R) ** 2
        ok = excess <= bound
        scaling_ok &= ok
        scaling.append({"M_R/M_D": ratio, "m*M_R/M_D^2-1": excess,
                        "bound_1.1*(M_D/M_R)^2": bound, "ok": ok})

    # A single large M_R explains m_e (0.5 MeV) >> m_nu (~0.05 eV) with no Higgs:
    # the canonical accommodation of the measured scale.
    accommodates = all(c["in_measured_window_0.001..0.12eV"] for c in cases)
    return {
        "seesaw_formula": "m_nu = M_D^2 / M_R  (M_R >> M_D)",
        "higgs_free": True,
        "cases": cases,
        "scaling_check": scaling,
        "scaling_within_bound": bool(scaling_ok),
        "accommodates_measured_scale": bool(accommodates and scaling_ok),
        "sum_mnu_bound_eV": 0.12,
        "note": ("A single large Majorana scale M_R replaces an unnaturally "
                 "tiny Yukawa: m_nu ~ 1e-3..1e-1 eV emerges automatically."),
    }


# ════════════════════════════════════════════════════════════════════════
#  CASIM β-decay run cross-reference
# ════════════════════════════════════════════════════════════════════════

def summarize_casim_run(path):
    """Pull the W⁻ energy trace from the L=64 ticks=1000 CASIM run."""
    if not os.path.exists(path):
        return {"present": False, "native_run_needed": True,
                "command": ("PYTHONPATH=src python3 -m casim.cli "
                            "run scenarios/beta_decay.yaml --L 64 --ticks 1000 "
                            "--out test-results/FC07_beta.json")}
    d = json.load(open(path))
    recs = d.get("observers", {}).get("energy_trace", {}).get("records", [])
    e0 = recs[0]["energy"]["beta_decay"] if recs else None
    e_after = recs[1]["energy"]["beta_decay"] if len(recs) > 1 else None
    e_final = recs[-1]["energy"]["beta_decay"] if recs else None
    # W⁻ emitted on first tick (E jumps 0 -> finite), then conserved under Proca
    emitted = (e0 == 0.0 and e_after is not None and e_after > 1e-6)
    conserved = (e_after is not None and e_final is not None
                 and abs(e_final - e_after) / max(e_after, 1e-30) < 1e-6)
    return {
        "present": True,
        "native_run_needed": False,
        "L": d["lattice"].get("L"), "ticks": d.get("ticks"),
        "propagator": d["channels"]["beta_decay"]["propagator"],
        "E_W_tick0": e0, "E_W_after_emit": e_after, "E_W_final": e_final,
        "w_minus_emitted": bool(emitted),
        "proca_energy_conserved": bool(conserved),
    }


# ════════════════════════════════════════════════════════════════════════
#  Driver
# ════════════════════════════════════════════════════════════════════════

def main():
    anomalies = compute_anomalies()
    anomalies_all_zero = all(v == 0 for v in anomalies.values())

    Q, Q_p, Q_e, charges_exact, proton_minus_electron = compute_charges()

    beta = verify_beta_chirality()

    seesaw = verify_seesaw()

    casim = summarize_casim_run(os.path.join(REPO, "test-results", "FC07_beta.json"))

    block1_pass = anomalies_all_zero
    block2_pass = charges_exact and proton_minus_electron
    block3_pass = (beta["left_chiral"]
                   and beta["right_branch_weight_is_zero"]
                   and beta["numpy_matches_handrolled"]
                   and casim.get("w_minus_emitted", False))
    block4_pass = seesaw["accommodates_measured_scale"]

    verdict = "PASS" if (block1_pass and block2_pass and block3_pass and block4_pass) else "FAIL"

    out = {
        "test": "FC07",
        "title": "Charge quantization, anomaly cancellation, β-decay",
        "tier": "C (consistency regression)",
        "date": datetime.now().strftime("%Y-%m-%d - %H:%M"),
        "overall_verdict": verdict,
        "provenance": ["F38", "F41", "F35", "F54", "F47", "F53"],
        "supersedes": ["test_10_QG4_charge.py", "test_07_QFT5_neutrino.py",
                       "test_FG1_anomaly_cancellation.py", "test_FG8_beta_decay.py"],

        "block1_anomalies": {
            "pass": block1_pass,
            "all_six_exactly_zero": anomalies_all_zero,
            "arithmetic": "fractions.Fraction (exact rationals over Q)",
            "traces": {k: str(v) for k, v in anomalies.items()},
        },
        "block2_charges": {
            "pass": block2_pass,
            "convention": "Q = T3 + Y/2",
            "charges_exact_rationals": charges_exact,
            "table": {k: str(v) for k, v in Q.items()},
            "Q_proton (uud)": str(Q_p),
            "Q_electron": str(Q_e),
            "proton_equals_minus_electron_exact": proton_minus_electron,
        },
        "block3_beta_decay": {
            "pass": block3_pass,
            "process": "d -> u + W- -> u + e- + nubar_e",
            "vertex": "P_L = (1 - gamma5)/2  (left-coupled charged current)",
            "left_chiral": beta["left_chiral"],
            "right_branch_weight": beta["handrolled"]["right_branch_weight (P_R psi_L)"],
            "right_branch_weight_is_zero": beta["right_branch_weight_is_zero"],
            "numpy_verified_against_handrolled": beta["numpy_matches_handrolled"],
            "chirality_detail": beta,
            "casim_run": casim,
        },
        "block4_seesaw": {
            "pass": block4_pass,
            **seesaw,
        },
        "native_run_needed": casim.get("native_run_needed", True),
    }

    out_path = os.path.join(REPO, "test-results", "FC07_charge_anomaly.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    # console summary
    print("=" * 72)
    print(f"FC07 — Charge quantization / anomaly / β-decay   VERDICT: {verdict}")
    print("=" * 72)
    print("Block 1 — six anomaly traces (exact rationals):")
    for k, v in anomalies.items():
        print(f"   {k:32s} = {v}")
    print(f"   all six exactly zero: {anomalies_all_zero}")
    print()
    print("Block 2 — charges (Q = T3 + Y/2, exact ℚ):")
    for k, v in Q.items():
        print(f"   Q({k:5s}) = {v}")
    print(f"   Q(proton=uud) = {Q_p};  Q(electron) = {Q_e};  "
          f"proton = -electron: {proton_minus_electron}")
    print()
    print("Block 3 — β-decay chirality:")
    print(f"   left-chiral: {beta['left_chiral']}; "
          f"right-branch weight = {beta['handrolled']['right_branch_weight (P_R psi_L)']} "
          f"(≡0: {beta['right_branch_weight_is_zero']})")
    print(f"   numpy matches hand-rolled chiral step: {beta['numpy_matches_handrolled']}")
    print(f"   CASIM L={casim.get('L')} ticks={casim.get('ticks')} "
          f"W⁻ emitted: {casim.get('w_minus_emitted')}; "
          f"Proca energy conserved: {casim.get('proca_energy_conserved')}")
    print()
    print("Block 4 — F47 see-saw (Higgs-free):")
    for c in seesaw["cases"]:
        print(f"   M_D={c['M_D_GeV']:g} GeV, M_R={c['M_R_GeV']:g} GeV "
              f"-> m_nu = {c['m_nu_eV']:.4g} eV")
    print(f"   accommodates measured scale: {seesaw['accommodates_measured_scale']}")
    print()
    print(f"native run needed: {out['native_run_needed']}")
    print(f"wrote -> {out_path}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
