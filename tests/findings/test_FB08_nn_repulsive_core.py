#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_FB08_nn_repulsive_core.py
==============================

FB08 (falsification) — the NN short-range REPULSIVE CORE, derived (no tuned wall).

Confronts the F113 derivation against two falsification criteria (FB08 brief):

  1. The quark-Pauli + chromomagnetic (one-gluon-exchange) mechanism must give a
     core of the RIGHT SIGN (repulsive, +) and RIGHT SCALE (+341.8 MeV at full
     overlap), computed directly from the model's own colour-spin algebra given
     the chromomagnetic coupling g_cm (fixed by the measured N-Delta splitting).

  2. Feeding that DERIVED core (no hand-tuned hard wall) into the FB07-style
     deuteron solve, the deuteron must still bind at the physical
     E_b = 2.224 MeV, kappa = 0.2316 fm^-1.

Part 1 (the core height) is recomputed here from the exact rational kernels in
ca_nuclear_core (CLAUDE.md: pure-Fraction arithmetic, no numpy on chiral
objects).  Part 2 reuses the F113-wired ca_nuclear deuteron solver
(solve_deuteron(core="derived", ...)), tuning the single physical knob b (quark
size) to the binding via the model's own bisection helper — exactly the
"derived core, no hard wall" path of F104/F113.

Run:  python3 tests/findings/test_FB08_nn_repulsive_core.py
Writes test-results/FB08_nn_repulsive_core.json.
"""

import os
import sys
import json
from fractions import Fraction as Fr

_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "..", "ca-simulation"))

import ca_nuclear_core as C       # exact rational core derivation (F113)  # noqa: E402
import ca_nuclear as N            # deuteron coupled-channel solver         # noqa: E402

# ---------------------------------------------------------------------------
PASS = True
checks = {}


def record(name, ok, detail):
    global PASS
    checks[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:48s} {detail}")


print("=" * 80)
print("FB08 — NN short-range repulsive core (derived) + deuteron binding")
print("=" * 80)

# ===========================================================================
# PART 1 — derive the core height from the model (exact, pure-Fraction).
#   Single nucleon  <H_CM> = -8 g_cm   (binding)
#   Delta(1232)     <H_CM> = +8 g_cm   => M_Delta - M_N = 16 g_cm
#   g_cm fixed by   M_Delta - M_N = 293 MeV  =>  g_cm = 18.31 MeV
#   [6] 6q at R=0   <H_CM> = +8/3 g_cm  vs  two free N = -16 g_cm
#   core height     dE_CM = +56/3 g_cm = +341.8 MeV  (> 0 => REPULSIVE)
# ===========================================================================
print("\n-- Part 1: derived core height (exact rational chromomagnetic algebra) --")

M_DELTA_N = 293.0   # MeV, measured N-Delta splitting (the one external number)

eN = C.chromomagnetic_energy(C.nucleon("p", True), 3)   # -8 g_cm
eD = C.chromomagnetic_energy(C.delta_pp(), 3)           # +8 g_cm
ok_baryon = (eN == Fr(-8) and eD == Fr(8))
g_cm = M_DELTA_N / float(eD - eN)                       # MeV per unit g_cm
record("P1.baryon_chromomagnetic_N=-8_Delta=+8", ok_baryon,
       f"E_N={eN} g_cm, E_Delta={eD} g_cm, split={eD-eN} g_cm => g_cm={g_cm:.2f} MeV")

# six-quark deuteron channel (S=1, T=0, L=0)
Phi = C.two_cluster(True, True, "singlet")

# Pauli norm kernel: n(R=0) = 20/9 > 0 => channel is NOT kinematically forbidden
K = C.norm_kernel_coeffs(Phi)
n0 = sum(K.values()) / K[0]
ok_norm = (n0 == Fr(20, 9) and n0 > 0)
record("P1.pauli_norm_n0=20/9_not_forbidden", ok_norm,
       f"K0={K[0]}, K1={K[1]}, K2={K[2]}, K3={K[3]}; n(R=0)={n0} (>0)")

# the core: antisymmetrised [6] 6q energy at R=0 vs two free nucleons
e6 = C.antisymmetrised_6q_energy(Phi)                   # +8/3 g_cm
dE = e6 - 2 * eN                                        # +56/3 g_cm
V_core0 = float(dE) * g_cm                              # MeV
ok_exact_frac = (e6 == Fr(8, 3) and dE == Fr(56, 3))
ok_repulsive = (dE > 0)
ok_height = (abs(V_core0 - 341.8) < 0.05)               # +341.8 MeV target
record("P1.core_dE=+56/3_gcm_(exact_rational)", ok_exact_frac,
       f"E_6q(R0)={e6} g_cm, 2N={2*eN} g_cm, dE={dE} g_cm")
record("P1.core_REPULSIVE_sign(+)", ok_repulsive,
       f"dE_CM={dE} g_cm > 0  =>  V_core(0)=+{V_core0:.1f} MeV (repulsive)")
record("P1.core_height_+341.8_MeV", ok_height,
       f"V_core(0) = +{V_core0:.4f} MeV  (target +341.8)")

# profile sanity: positive, monotone-decreasing, vanishing at large R
prof = C.core_profile(Phi, [0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0])
Vprof = [(xb, g_cm * (g - 2 * float(eN))) for xb, g in prof]
Vvals = [v for _, v in Vprof]
mono = all(Vvals[i] > Vvals[i + 1] - 1e-9 for i in range(len(Vvals) - 1))
posv = all(v > -1e-6 for v in Vvals)
vanish = (Vvals[-1] < 0.05 * Vvals[0])
ok_prof = mono and posv and vanish and abs(Vvals[0] - V_core0) < 1e-6
record("P1.profile_positive_monotone_vanishing", ok_prof,
       f"V(0)={Vvals[0]:.1f}, V(2b)={Vprof[4][1]:.1f}, V(4b)={Vvals[-1]:.1f} MeV")

# Cross-check: the closed-form core embedded in the deuteron solver (numpy) must
# reproduce the exact-rational R=0 height (verify-the-scipy/numpy-path, CLAUDE.md).
V0_solver = float(N.derived_core_potential(0.0, b=N.B_QUARK_DEFAULT, g_cm=g_cm))
ok_solver_core = (abs(V0_solver - V_core0) < 1e-6)
record("P1.solver_closed_form_matches_exact", ok_solver_core,
       f"ca_nuclear.derived_core_potential(0)=+{V0_solver:.4f} MeV "
       f"vs exact +{V_core0:.4f} MeV")

# ===========================================================================
# PART 2 — feed the DERIVED core (no hard wall) into the deuteron solve.
#   solve_deuteron(core="derived", b=...) replaces the tuned hard wall with the
#   F113 V_core(r;b); tune the single physical knob b (quark size) to the
#   physical binding via the model's own bisection.  Confirm E_b = 2.224 MeV
#   and kappa = 0.2316 fm^-1.
# ===========================================================================
print("\n-- Part 2: deuteron binds with the derived core (no tuned wall) --")

TARGET_EB = 2.224     # MeV
TARGET_KAPPA = 0.2316  # fm^-1

b_tuned, res = N.tune_b_to_binding(target_Eb=TARGET_EB, g_cm=g_cm)

E_b = res["E_b"]
kappa = res["kappa"]
bound = res["bound"]
E1 = res["E1"]
P_D = res["P_D"]
Vcore0_used = res["Vcore0"]
core_mode = res["core"]

ok_core_mode = (core_mode == "derived")           # no hard wall path
ok_bound = bool(bound and E_b > 0)
ok_Eb = (abs(E_b - TARGET_EB) < 0.005)
ok_kappa = (abs(kappa - TARGET_KAPPA) < 0.005)
ok_one_state = (E1 >= 0.0)                         # still a single bound state
ok_solver_height = (abs(Vcore0_used - 341.8) < 0.05)

record("P2.core_mode_is_derived_no_hard_wall", ok_core_mode,
       f"core='{core_mode}', b_tuned={b_tuned:.4f} fm (physical quark size), "
       f"Vcore0={Vcore0_used:.1f} MeV")
record("P2.deuteron_binds", ok_bound, f"bound={bound}, E_b={E_b:.4f} MeV")
record("P2.E_b=2.224_MeV", ok_Eb, f"E_b={E_b:.5f} MeV (target {TARGET_EB})")
record("P2.kappa=0.2316_inv_fm", ok_kappa,
       f"kappa={kappa:.5f} fm^-1 (target {TARGET_KAPPA})")
record("P2.single_bound_state", ok_one_state, f"E1={E1:.4f} MeV (>=0)")
record("P2.solver_used_derived_341.8_core", ok_solver_height,
       f"Vcore0 in solve = +{Vcore0_used:.4f} MeV")

# Tensor still essential with the derived core (central-only must be unbound).
res_central = N.solve_deuteron(core="derived", b=b_tuned, g_cm=g_cm,
                               tensor=False, vectors=False)
ok_tensor = (not res_central["bound"])
record("P2.tensor_still_essential", ok_tensor,
       f"central-only E={res_central['E']:.3f} MeV (unbound: {not res_central['bound']})")

# ===========================================================================
# GATE + JSON
# ===========================================================================
gate_core = ok_height and ok_repulsive and ok_exact_frac
gate_bind = ok_bound and ok_Eb and ok_kappa and ok_core_mode
gate_pass = gate_core and gate_bind and PASS
verdict = "PASS" if gate_pass else "FALSIFIED"

result = {
    "test_id": "FB08",
    "name": "NN short-range repulsive core, derived (quark Pauli + chromomagnetic)",
    "verdict": verdict,
    "predicted": {
        "core_height_MeV": 56.0 / 3.0 * g_cm,
        "core_height_frac_gcm": "56/3",
        "core_sign": "repulsive (+)",
        "deuteron_E_b_MeV": TARGET_EB,
        "deuteron_kappa_inv_fm": TARGET_KAPPA,
    },
    "measured_target": {
        "N_Delta_splitting_MeV": M_DELTA_N,
        "deuteron_E_b_MeV": 2.224,
        "deuteron_kappa_inv_fm": 0.2316,
        "phenomenology": "Argonne-v18-class: strong repulsive core (~GeV wall "
                         "inside ~0.5 fm); deuteron is the single shallow 1+ I=0 "
                         "bound state.",
    },
    "gate": {
        "criterion": "PASS iff derived core +341.8 MeV REPULSIVE (exact given "
                     "g_cm) AND deuteron binds at physical E_b/kappa with the "
                     "derived core (no tuned hard wall).",
        "core_height_repulsive_ok": bool(gate_core),
        "deuteron_binds_physical_ok": bool(gate_bind),
    },
    "computed": {
        "g_cm_MeV": g_cm,
        "E_N_gcm": str(eN),
        "E_Delta_gcm": str(eD),
        "norm_kernel_K": {m: str(K[m]) for m in K},
        "n_at_R0": str(n0),
        "E_6q_R0_gcm": str(e6),
        "dE_CM_gcm": str(dE),
        "V_core0_MeV": V_core0,
        "V_core0_solver_MeV": V0_solver,
        "core_profile_MeV": [(xb, v) for xb, v in Vprof],
        "deuteron": {
            "core": core_mode,
            "b_tuned_fm": b_tuned,
            "E_b_MeV": E_b,
            "kappa_inv_fm": kappa,
            "E1_MeV": E1,
            "P_D": P_D,
            "Vcore0_MeV": Vcore0_used,
            "central_only_bound": bool(res_central["bound"]),
        },
    },
    "checks": checks,
    "commands": [
        "python3 tests/findings/test_FB08_nn_repulsive_core.py",
    ],
    "notes": [
        "Part 1 (core height) computed in THIS test from the exact rational "
        "chromomagnetic algebra in ca_nuclear_core (Fierz swap identities; pure "
        "Fraction arithmetic, no numpy on chiral objects per CLAUDE.md): "
        "dE_CM = +56/3 g_cm exactly; g_cm = 293/16 = 18.31 MeV from the N-Delta "
        "splitting => +341.79 MeV, REPULSIVE.",
        "Part 2 reuses the F113-wired ca_nuclear.solve_deuteron(core='derived'), "
        "which embeds the SAME exact rational core kernel (closed-form "
        "derived_core_potential, cross-checked here to reproduce the exact R=0 "
        "height) and replaces the old tuned hard wall; the single physical knob "
        "is the quark size b, bisected to the binding by the model's own helper.",
        "g_cm is NOT a new parameter: it is the existing N-Delta colour-magnetic "
        "coupling. The core HEIGHT and SHAPE are derived; only b (a genuine "
        "quark/nucleon-core length, ~0.41 fm) is tuned to the shallow binding.",
        "Consistent with the independent P4 deuteron result "
        "(test-results/P4_deuteron.json, checks I1-I5 PASS).",
    ],
    "timestamp": "2026-06-16",
}

out_dir = os.path.abspath(os.path.join(_HERE, "..", "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "FB08_nn_repulsive_core.json")
with open(out_path, "w") as fh:
    json.dump(result, fh, indent=2)

print("\n" + "=" * 80)
n_pass = sum(1 for c in checks.values() if c["status"] == "PASS")
print(f"VERDICT: {verdict}   ({n_pass}/{len(checks)} checks)")
print(f"  core height  = +{V_core0:.4f} MeV  (target +341.8, repulsive)")
print(f"  deuteron E_b = {E_b:.5f} MeV   kappa = {kappa:.5f} fm^-1  "
      f"(b={b_tuned:.4f} fm, core='derived')")
print(f"results -> {out_path}")
print("=" * 80)
sys.exit(0 if gate_pass else 1)
