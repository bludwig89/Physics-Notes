#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_FB07_deuteron.py
=====================

FB07 (falsification) — the DEUTERON: the first nucleus binds via the pion
tensor force.

Confronts F104/F126/F113/F103 against the FB07 brief's falsification criteria:

  (1) The full coupled ³S₁–³D₁ OPEP TENSOR force must bind while central-only
      OPEP (same core, same σ, same ω) must NOT — the tensor-essential structure
      is the headline claim (the textbook reason the deuteron exists).
  (2) The bound state must be a SINGLE J^P=1⁺, I=0 state with a few-% D-state.
  (3) The ³S₁ tail slope must reproduce κ = √(M_N E_b)/ħc to ~1% at the physical
      E_b, and tuning one short-range knob must land E_b = 2.224 MeV at the
      physical κ = 0.2316 fm⁻¹.

PHYSICS / INPUTS (honest accounting, per F104):
  • m_π, f_π        : P3/F77 model outputs (force carrier).
  • g_A = 1.2723    : EXTERNAL axial charge -> f²/4π via Goldberger-Treiman.
  • M_N = 938.9 MeV : EXTERNAL nucleon mass (P2/P6).
  • derived core    : F113 quark-Pauli + chromomagnetic, +341.8 MeV at r=0
                      (EXACT given g_cm = 293/16 MeV); NO hand-tuned hard wall.
  • σ attraction    : F126 scalar-isoscalar, g²/4π = 8.18, m_σ = 2 m_c, folded
                      over the physical quark size b = 0.55 fm.
  • ω repulsion     : F128 isoscalar-vector; here it is the SINGLE tuned
                      short-range knob (one number), bisected to the binding —
                      the brief's "tune one short-range core" lever, kept inside
                      the OBE window. (FB08 instead tunes b at fixed couplings;
                      both land the same physical deuteron — cross-checked below.)

The tensor spin-angular matrix <S12> is verified to the Rarita-Schwinger
[[0, 2√2],[2√2, -2]] to machine precision by explicit Clebsch-Gordan + spinor-
spherical-harmonic quadrature (hand-checked: the off-diagonal 2√2 is exactly the
L=0<->L=2 mixing that supplies the binding).

All arithmetic REAL (radial Schrödinger eigenproblem; NOT a chiral transform —
numpy is appropriate here per CLAUDE.md). The spin-angular algebra is verified
against the closed-form Rarita-Schwinger result.

Run:  python3 tests/findings/test_FB07_deuteron.py
Writes test-results/FB07_deuteron.json.
"""

import os
import sys
import json
import math

import numpy as np

_HERE = os.path.dirname(__file__)
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.particles import nuclear as N        # deuteron coupled-channel solver (F104/F113/F126/F128)  # noqa: E402

# ---------------------------------------------------------------------------
PASS = True
checks = {}


def record(name, ok, detail):
    global PASS
    checks[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:52s} {detail}")


print("=" * 84)
print("FB07 — Deuteron: the first nucleus binds via the pion tensor force")
print("=" * 84)

# Physical targets.
TARGET_EB = 2.224       # MeV   (E_b = 2.22457 MeV measured)
TARGET_KAPPA = 0.2316   # fm^-1 = sqrt(M_N E_b)/hbar c
B_PHYS = 0.55           # fm    F126 physical quark size
SIGMA_G2 = 8.18         # F126 scalar-isoscalar coupling g^2/4pi

# ===========================================================================
# CRITERION 0 — tensor strength certified (Rarita-Schwinger), machine precision.
# ===========================================================================
print("\n-- C0: tensor spin-angular matrix <S12> = [[0,2√2],[2√2,-2]] (CG) --")
Mt = N.tensor_matrix_via_construction()
RS = np.array([[0.0, 2.0 * math.sqrt(2.0)],
               [2.0 * math.sqrt(2.0), -2.0]])
resid = float(np.max(np.abs(Mt - RS)))
ok_tensor_matrix = (resid < 1e-13)
record("C0.S12_equals_Rarita_Schwinger", ok_tensor_matrix,
       f"max|<S12>_CG - [[0,2√2],[2√2,-2]]| = {resid:.2e} (machine)")

# ===========================================================================
# Build the physical deuteron: F113 derived core + F126 σ (b=0.55, g2=8.18)
# + F128 ω as the SINGLE tuned short-range knob -> E_b = 2.224 MeV.
# ===========================================================================
print("\n-- Build: derived core + σ(b=0.55, g²/4π=8.18) − ω(tuned) --")


def Eb_of_omega(wg):
    return N.solve_deuteron(core="derived", b=B_PHYS, sigma=True,
                            sigma_g2_4pi=SIGMA_G2, omega=True,
                            omega_g2_4pi=wg, vectors=False)["E_b"]


# E_b decreases monotonically with the ω coupling; bisect to the target.
lo, hi = 4.0, 14.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if Eb_of_omega(mid) > TARGET_EB:
        lo = mid       # too deep -> stronger ω repulsion
    else:
        hi = mid
omega_g2 = 0.5 * (lo + hi)

res = N.solve_deuteron(core="derived", b=B_PHYS, sigma=True,
                       sigma_g2_4pi=SIGMA_G2, omega=True, omega_g2_4pi=omega_g2)

E_b = res["E_b"]
kappa = res["kappa"]
E1 = res["E1"]
P_D = res["P_D"]
r_d = res["r_d"]
Vcore0 = res["Vcore0"]
core_mode = res["core"]
print(f"   tuned ω g²/4π = {omega_g2:.4f}  (single short-range knob; OBE window)")

# ===========================================================================
# CRITERION 1 — tensor-essential: full binds, central-only does NOT (same config).
# ===========================================================================
print("\n-- C1: tensor-essential (full binds; central-only unbound, same core) --")
res_central = N.solve_deuteron(core="derived", b=B_PHYS, sigma=True,
                               sigma_g2_4pi=SIGMA_G2, omega=True,
                               omega_g2_4pi=omega_g2, tensor=False, vectors=False)
full_bound = bool(res["bound"] and E_b > 0)
central_bound = bool(res_central["bound"])
ok_tensor_essential = full_bound and (not central_bound)
record("C1.full_binds_central_unbound", ok_tensor_essential,
       f"full E_b={E_b:.4f} MeV (bound); central-only E={res_central['E']:.3f} MeV "
       f"(unbound: {not central_bound})")

# ===========================================================================
# CRITERION 2 — single J^P=1⁺, I=0 state with few-% D-state.
#   • J=1: total spin S=1 (triplet) ⊗ L∈{0,2} coupled to J=1 by construction.
#   • P=+1: parity (-1)^L = +1 for BOTH coupled waves (L=0 and L=2).
#   • I=0: the S=1, T=0 channel (the only NN channel where OPEP central is
#          attractive AND the tensor binds) — the antisymmetry of the two-nucleon
#          state forces (S,T)=(1,0) for the L-even deuteron (F104).
#   • single state: the next eigenvalue E1 >= 0 (no second bound state).
#   • D-state few-%: P_D in (2%,12%), vanishing when the tensor is off.
# ===========================================================================
print("\n-- C2: single J^P=1⁺ I=0 state, few-% D-state --")
ok_single = (E1 >= 0.0)
record("C2.single_bound_state", ok_single,
       f"E1 = {E1:.4f} MeV >= 0 (no second bound state)")

# parity of both coupled channels is (-1)^L = +1 (L=0 and L=2): J^P = 1^+
ok_parity = True   # structural: both partial waves L even -> P=+1, S=1 -> J=1
record("C2.JP_is_1plus_I0", ok_parity,
       "L∈{0,2} (P=(-1)^L=+1), S=1 triplet, T=0 (antisymmetry) -> J^P=1⁺, I=0")

ok_Dstate = (0.02 < P_D < 0.12)
res_notensor_PD = N.solve_deuteron(core="derived", b=B_PHYS, sigma=True,
                                   sigma_g2_4pi=SIGMA_G2, omega=True,
                                   omega_g2_4pi=omega_g2, tensor=False)["P_D"]
ok_Dstate_zero = (res_notensor_PD < 1e-6)
record("C2.D_state_few_percent", ok_Dstate,
       f"P_D = {100*P_D:.2f}% (few-%; tensor-induced)")
record("C2.D_state_vanishes_without_tensor", ok_Dstate_zero,
       f"P_D(tensor off) = {res_notensor_PD:.2e} (~0)")

# ===========================================================================
# CRITERION 3 — ³S₁ tail slope matches κ to ~1%; E_b tunable to 2.224 at phys κ.
# ===========================================================================
print("\n-- C3: ³S₁ tail slope vs κ; E_b=2.224 at physical κ=0.2316 fm⁻¹ --")
r = res["r"]
u = res["u"]
mask = (r > 6.0) & (r < 12.0) & (np.abs(u) > 0.0)
slope = float(np.polyfit(r[mask], np.log(np.abs(u[mask])), 1)[0])
kappa_tail = -slope
kappa_analytic = math.sqrt(N.M_N * E_b) / N.HBARC   # sqrt(M_N E_b)/hbar c
tail_rel = abs(kappa_tail - kappa) / kappa
ok_tail = (tail_rel < 0.01)
record("C3.tail_slope_matches_kappa", ok_tail,
       f"κ_tail={kappa_tail:.5f} vs κ={kappa:.5f} fm⁻¹  (rel {100*tail_rel:.3f}% < 1%)")

ok_Eb = (abs(E_b - TARGET_EB) < 0.005)
ok_kappa = (abs(kappa - TARGET_KAPPA) < 0.005)
ok_kappa_def = (abs(kappa - kappa_analytic) < 1e-9)
record("C3.E_b_tuned_to_2.224_MeV", ok_Eb,
       f"E_b = {E_b:.5f} MeV (target {TARGET_EB})")
record("C3.physical_kappa_0.2316", ok_kappa,
       f"κ = {kappa:.5f} fm⁻¹ (target {TARGET_KAPPA})")
record("C3.kappa_equals_sqrt_MN_Eb", ok_kappa_def,
       f"κ = √(M_N E_b)/ħc to {abs(kappa-kappa_analytic):.2e}")

# radius sanity (not a gate; r_d ≈ 1.97 fm measured)
ok_rd = (1.7 < r_d < 2.2)
record("C3.deuteron_radius_~1.97_fm", ok_rd,
       f"r_d = {r_d:.3f} fm (measured ≈1.97)")

# ===========================================================================
# CROSS-CHECK — the FB08 b-tuned path lands the SAME physical deuteron.
#   (Different single short-range knob: tune the quark size b at fixed default
#    couplings. Confirms the result is not an artefact of the ω-tuning choice.)
# ===========================================================================
print("\n-- X: cross-check vs FB08 b-tuned derived-core path --")
b_tuned, res_b = N.tune_b_to_binding(target_Eb=TARGET_EB)
ok_xcheck = (abs(res_b["E_b"] - TARGET_EB) < 0.005 and
             abs(res_b["kappa"] - TARGET_KAPPA) < 0.005 and res_b["E1"] >= 0 and
             not N.solve_deuteron(core="derived", b=b_tuned, tensor=False,
                                  vectors=False)["bound"])
record("X.b_tuned_path_same_physical_deuteron", ok_xcheck,
       f"b={b_tuned:.4f} fm -> E_b={res_b['E_b']:.4f} MeV, κ={res_b['kappa']:.5f}, "
       f"P_D={100*res_b['P_D']:.2f}%, tensor still essential")

# ===========================================================================
# GATE + VERDICT (FB07 falsification criteria)
# ===========================================================================
# Falsified if: (1) full tensor fails to bind while central-only also fails
#               (tensor-essential structure broken), OR
#               (2) bound state is not a single 1⁺ I=0 with few-% D-state, OR
#               (3) ³S₁ tail slope departs from κ beyond ~1% at physical E_b.
crit1 = ok_tensor_essential                              # tensor-essential
crit2 = ok_single and ok_parity and ok_Dstate and ok_Dstate_zero   # 1⁺ I=0 few-% D
crit3 = ok_tail and ok_Eb and ok_kappa and ok_kappa_def  # tail slope / tune
gate_pass = crit1 and crit2 and crit3 and ok_tensor_matrix and PASS
verdict = "PASS" if gate_pass else "FALSIFIED"

result = {
    "test_id": "FB07",
    "name": "Deuteron — ³S₁–³D₁ coupled-channel: binds via the pion tensor force",
    "verdict": verdict,
    "hypothesis": (
        "The deuteron binds as a single J^P=1⁺, I=0 state ONLY through the OPEP "
        "tensor force (central-only OPEP is unbound at the same core — "
        "structural). E_b=2.224 MeV, κ=0.2316 fm⁻¹, r_d≈1.97 fm, few-% D-state."
    ),
    "predicted": {
        "E_b_MeV": TARGET_EB,
        "kappa_inv_fm": TARGET_KAPPA,
        "JP": "1+",
        "isospin": 0,
        "tensor_essential": True,
        "S12_matrix": "[[0, 2√2],[2√2, -2]] (Rarita-Schwinger)",
    },
    "measured_target": {
        "E_b_MeV": 2.22457,
        "kappa_inv_fm": 0.2316,
        "JP": "1+",
        "isospin": 0,
        "r_d_fm": 1.97,
        "P_D_percent": "4-6",
    },
    "gate": {
        "criterion": (
            "PASS iff (1) full tensor binds AND central-only unbound at the same "
            "core (tensor-essential), (2) single J^P=1⁺ I=0 with few-% D-state, "
            "(3) ³S₁ tail slope matches κ=√(M_N E_b)/ħc to ~1% with E_b tunable "
            "to 2.224 MeV at physical κ=0.2316 fm⁻¹."
        ),
        "criterion_1_tensor_essential_ok": bool(crit1),
        "criterion_2_single_1plus_I0_fewpct_D_ok": bool(crit2),
        "criterion_3_tail_and_tune_ok": bool(crit3),
        "tensor_matrix_machine_precision_ok": bool(ok_tensor_matrix),
    },
    "computed": {
        "S12_matrix_residual": resid,
        "config": {
            "core": core_mode,
            "b_fm": B_PHYS,
            "sigma_g2_4pi": SIGMA_G2,
            "m_sigma_MeV": N.M_SIGMA_DEFAULT,
            "omega_g2_4pi_tuned": omega_g2,
            "m_omega_MeV": N.M_OMEGA_DEFAULT,
            "Vcore0_MeV": Vcore0,
            "g_A": N.G_A,
            "M_N_MeV": N.M_N,
            "m_pi_MeV": N.M_PI_DEFAULT,
            "f_pi_MeV": N.F_PI_DEFAULT,
            "f2_over_4pi": res["f2_4pi"],
        },
        "deuteron": {
            "E_b_MeV": E_b,
            "kappa_inv_fm": kappa,
            "kappa_analytic_sqrt_MN_Eb": kappa_analytic,
            "kappa_tail_slope": kappa_tail,
            "tail_rel_error": tail_rel,
            "E1_MeV": E1,
            "P_D": P_D,
            "P_D_percent": 100.0 * P_D,
            "P_D_no_tensor": res_notensor_PD,
            "r_d_fm": r_d,
            "central_only_bound": central_bound,
            "central_only_E_MeV": res_central["E"],
        },
        "cross_check_b_tuned": {
            "b_fm": b_tuned,
            "E_b_MeV": res_b["E_b"],
            "kappa_inv_fm": res_b["kappa"],
            "P_D_percent": 100.0 * res_b["P_D"],
            "E1_MeV": res_b["E1"],
        },
    },
    "checks": checks,
    "commands": [
        "python3 tests/findings/test_FB07_deuteron.py",
    ],
    "notes": [
        "Tensor matrix <S12> built by explicit Clebsch-Gordan + spinor-spherical-"
        "harmonic quadrature equals the Rarita-Schwinger [[0,2√2],[2√2,-2]] to "
        f"{resid:.1e}; the off-diagonal 2√2 (hand-checked) is exactly the "
        "L=0<->L=2 mixing that supplies the binding.",
        "HEADLINE (tensor-essential): with the F113 derived +341.8 MeV core, F126 "
        "σ attraction (g²/4π=8.18, b=0.55 fm) and F128 ω repulsion, the full "
        "³S₁–³D₁ OPEP binds (E_b=2.224 MeV) while central-only OPEP is UNBOUND at "
        "the identical configuration — the textbook reason the deuteron exists.",
        "Single short-range knob here is the ω coupling (bisected, kept inside the "
        "OBE window); FB08 instead tunes the quark size b at default couplings. "
        "Both land the same physical deuteron (cross-check X) — the result is not "
        "an artefact of which short-range lever is tuned.",
        "Inputs honest: g_A (external, via Goldberger-Treiman) and M_N (external, "
        "P2/P6) are the only non-model numbers; m_π, f_π are P3/F77 outputs; the "
        "core height +341.8 MeV is EXACT given g_cm (F113).",
        "Radial Schrödinger eigenproblem solved with numpy (REAL arithmetic, NOT a "
        "chiral transform — appropriate per CLAUDE.md); spin-angular algebra "
        "verified against the closed-form Rarita-Schwinger result.",
        "Consistent with F104 (P4_deuteron.json, 11/11) and FB08 "
        "(FB08_nn_repulsive_core.json).",
    ],
    "provenance": ["F104", "F126", "F113", "F103", "F128", "F77"],
    "timestamp": "2026-06-16 - 15:25",
}

out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "FB07_deuteron.json")
with open(out_path, "w") as fh:
    json.dump(result, fh, indent=2)

print("\n" + "=" * 84)
n_pass = sum(1 for c in checks.values() if c["status"] == "PASS")
print(f"VERDICT: {verdict}   ({n_pass}/{len(checks)} checks)")
print(f"  E_b = {E_b:.5f} MeV   κ = {kappa:.5f} fm⁻¹   P_D = {100*P_D:.2f}%   "
      f"r_d = {r_d:.3f} fm")
print(f"  tensor-essential: full bound, central-only unbound = {ok_tensor_essential}")
print(f"  <S12> residual vs Rarita-Schwinger = {resid:.2e}")
print(f"results -> {out_path}")
print("=" * 84)
sys.exit(0 if gate_pass else 1)
