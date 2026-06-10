#!/usr/bin/env python3
"""
test_F92_per_constituent_phase.py
=================================

F92 — Deriving the per-constituent phase identification (F81 input (b)) as a
consistency fixed point of the model's two established mass laws.

The target
----------
F81/F84 carry one load-bearing identification: that the generation-space
angle phi (the angle of the amplitude vector y = sqrt(m) off the democratic
axis, F80) is a *per-constituent rotation phase* obeying the F69 pair-sum
rule, so the composite mass is m_H = sin(2*phi).  F84 lists this as
irreducible structural input #1.

The claim tested here
---------------------
The identification need not be assumed globally.  The chain already contains
TWO independent mass laws for the same composite:

  L1 (F73/F69, exact kinematics):  m_comp = sin(t1 + t2) = sin(2t)
      for an equal pair, t = per-constituent rest phase (F46: m_c = sin t).

  L2 (F78, pair-bilinear premise): m_comp = y^2,
      y = the pair's constituent amplitude.

For a NORMALIZED pair state, the two-quantum Fock amplitude is sqrt(2) times
the single-quantum amplitude ((a^dag)^2 |0> = sqrt(2) |2>, exact), so
y = sqrt(2) sin t.  Demanding L1 and L2 describe the same object:

      2 sin^2 t = sin 2t   <=>   tan t = 1   <=>   t = 45 deg  (unique).

So the identification is CONSISTENT AT EXACTLY ONE ANGLE — 45 deg — and the
observed charged leptons sit there to 1e-5.  The per-constituent
identification + the 45 deg location collapse into a single self-consistency
statement; the only new input is the Bose pair factor sqrt(2), which the
data pin to c^2 = 2 +/- ~2e-5.

Checks
------
  P1  Model code: the F27 mass step (ca_dirac.mass_step_1flavor_u1) at k=0
      allocates amplitude (stay, transfer) = (cos t, sin t) — a unit
      2-vector whose angle is the rest phase.  Same for the F46 D_k block
      (entries n = cos(arcsin m), m = sin(arcsin m)).  Mass amplitude IS the
      sine of a rotation; this grounds the rotation reading of y in code.
  P2  Fock pair factor: (a^dag)^2 |0> = sqrt(2) |2>, exact (sympy).
  P3  Consistency theorem: 2 sin^2 t = sin 2t has the unique solution
      t = pi/4 on (0, pi/2); Q(pi/4) = 1/(3 cos^2) = 2/3 exactly (sympy).
      => a third, independent derivation of Q = 2/3 — one that does not
      ASSUME the per-constituent identification but solves for where it can
      hold.
  P4  Unitarity saturation: y(t) = sqrt(2) sin t <= 1  <=>  t <= 45 deg
      <=>  m_c <= 1/sqrt(2)  — the F73 stability cap re-derived as
      unitarity of the pair amplitude; at t = 45 deg, y = 1 and
      m_comp = sin(2t) = 1 saturate SIMULTANEOUSLY.
  P5  Normalization sensitivity + data pin: t*(c) = arctan(2/c^2); only the
      Fock value c^2 = 2 gives 45 deg.  PDG charged leptons give
      c^2_data = 2 cot(phi_lepton) = 2 to ~1e-5.

Honest scope: this shows the identification is the unique consistent joint
solution of L1+L2 given the Fock normalization.  It is NOT a derivation from
the QCA update rule of why the generation-space angle participates in the
pair phase budget at all — that bridge remains, but it is now pinned to a
single standard-QM input (the two-quantum Bose factor) instead of a free
structural assumption.
"""

import json
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))
from ca_dirac import mass_step_1flavor_u1  # noqa: E402

RESULTS = {}
PASS = True


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ════════════════════════════════════════════════════════════════════
# P1 — the model's own mass step allocates (cos t, sin t): a unit
#      2-vector whose angle is the rest phase.  Two conventions checked:
#      (a) the code step (angle t = m*dt), (b) the F46 D_k block
#      (amplitude m, angle t = arcsin m).  Both are exact.
# ════════════════════════════════════════════════════════════════════
worst_code = 0.0
worst_dk = 0.0
for m in (0.1, 0.3, 0.5, 1.0 / np.sqrt(2.0), 0.9):
    # (a) code step at k=0: uniform eta=(1,0), chi=0, theta=0
    shape = (2, 2)
    eu = np.ones(shape, dtype=complex)
    ed = np.zeros(shape, dtype=complex)
    xu = np.zeros(shape, dtype=complex)
    xd = np.zeros(shape, dtype=complex)
    th = np.zeros(shape)
    eu2, ed2, xu2, xd2 = mass_step_1flavor_u1(eu, ed, xu, xd, th, m, dt=1.0)
    stay = float(np.abs(eu2[0, 0]))
    transfer = float(np.abs(xu2[0, 0]))
    t_code = m * 1.0
    res = max(abs(stay - np.cos(t_code)), abs(transfer - np.sin(t_code)),
              abs(stay**2 + transfer**2 - 1.0))
    worst_code = max(worst_code, res)

    # (b) F46 D_k block at k=0: entries (n, i m), n = sqrt(1-m^2)
    n = np.sqrt(1.0 - m * m)
    Dk = np.array([[n, 1j * m], [1j * m, n]], dtype=complex)
    out = Dk @ np.array([1.0, 0.0], dtype=complex)
    t_dk = np.arcsin(m)
    res2 = max(abs(abs(out[0]) - np.cos(t_dk)), abs(abs(out[1]) - np.sin(t_dk)),
               abs(abs(out[0])**2 + abs(out[1])**2 - 1.0))
    worst_dk = max(worst_dk, res2)

record("P1_allocation_is_unit_rotation",
       worst_code < 1e-14 and worst_dk < 1e-14,
       {"code_step_residual": worst_code, "Dk_block_residual": worst_dk,
        "statement": "(stay, transfer) = (cos t, sin t) exactly; "
                     "mass amplitude = sine of the rest phase"})


# ════════════════════════════════════════════════════════════════════
# P2 — Fock pair factor: (a^dag)^2 |0> = sqrt(2) |2>  (exact, sympy)
# ════════════════════════════════════════════════════════════════════
N = 6
adag = sp.zeros(N, N)
for nq in range(N - 1):
    adag[nq + 1, nq] = sp.sqrt(nq + 1)
vac = sp.zeros(N, 1)
vac[0] = 1
pair = adag * adag * vac
expected = sp.zeros(N, 1)
expected[2] = sp.sqrt(2)
res_fock = sp.simplify((pair - expected).norm())
record("P2_fock_pair_factor",
       res_fock == 0,
       {"residual": str(res_fock),
        "statement": "(a^dag)^2 |0> = sqrt(2)|2> exactly: the normalized "
                     "two-quantum amplitude is sqrt(2) x single"})


# ════════════════════════════════════════════════════════════════════
# P3 — consistency theorem: 2 sin^2 t = sin 2t  <=>  t = pi/4, unique
#      on (0, pi/2); and Q(pi/4) = 2/3 exactly.
# ════════════════════════════════════════════════════════════════════
t = sp.symbols('t', positive=True)
sols = sp.solveset(sp.Eq(2 * sp.sin(t)**2, sp.sin(2 * t)),
                   t, sp.Interval.open(0, sp.pi / 2))
unique_45 = sols == sp.FiniteSet(sp.pi / 4)
Q_at = sp.simplify(1 / (3 * sp.cos(sp.pi / 4)**2))
record("P3_consistency_unique_45deg",
       unique_45 and Q_at == sp.Rational(2, 3),
       {"solutions_on_(0,pi/2)": str(sols), "Q(pi/4)": str(Q_at),
        "statement": "L1 (m=sin2t, F73 pair sum) and L2 (m=y^2, F78 "
                     "bilinear with y=sqrt(2) sin t) are jointly "
                     "satisfiable ONLY at t=45deg; Q=2/3 follows"})


# ════════════════════════════════════════════════════════════════════
# P4 — unitarity saturation: y = sqrt(2) sin t <= 1 <=> t <= pi/4
#      <=> m_c = sin t <= 1/sqrt(2)  (the F73 cap), and at t = pi/4 the
#      pair amplitude and the composite mass saturate together.
# ════════════════════════════════════════════════════════════════════
y_expr = sp.sqrt(2) * sp.sin(t)
# boundary of y<=1 on (0, pi/2):
bound = sp.solveset(sp.Eq(y_expr, 1), t, sp.Interval.open(0, sp.pi / 2))
cap_equiv = bound == sp.FiniteSet(sp.pi / 4)
mc_at_cap = sp.simplify(sp.sin(sp.pi / 4))          # = 1/sqrt(2): F73 cap
mcomp_at_cap = sp.simplify(sp.sin(2 * sp.pi / 4))   # = 1: lattice max
y_at_cap = sp.simplify(y_expr.subs(t, sp.pi / 4))   # = 1: unitarity edge
# monotonicity: y < 1 strictly below, > 1 strictly above (sample exactly)
below = sp.simplify(y_expr.subs(t, sp.pi / 6)) < 1
above = sp.simplify(y_expr.subs(t, sp.pi / 3)) > 1
record("P4_unitarity_saturation_equals_F73_cap",
       cap_equiv and mc_at_cap == 1 / sp.sqrt(2) and mcomp_at_cap == 1
       and y_at_cap == 1 and below and above,
       {"y=1 boundary": str(bound), "m_c at cap": str(mc_at_cap),
        "m_comp at cap": str(mcomp_at_cap),
        "statement": "F73 stability cap m_c<=1/sqrt2 == unitarity of the "
                     "pair amplitude y=sqrt(2)m_c<=1; y, m_comp saturate "
                     "simultaneously at 45deg"})


# ════════════════════════════════════════════════════════════════════
# P5 — normalization sensitivity + data pin.
#      t*(c) = arctan(2/c^2): only c^2 = 2 gives 45 deg.  PDG leptons
#      pin c^2 = 2 cot(phi_lepton) to ~1e-5.
# ════════════════════════════════════════════════════════════════════
table = {}
for c2 in (1, 2, 3, 4):
    tstar = float(np.degrees(np.arctan2(2.0, c2)))
    Qstar = 1.0 / (3.0 * np.cos(np.radians(tstar))**2)
    table[f"c^2={c2}"] = {"t*_deg": round(tstar, 4), "Q*": round(Qstar, 6)}

# PDG charged-lepton masses (MeV)
m_e, m_mu, m_tau = 0.51099895, 105.6583755, 1776.86
y = np.sqrt(np.array([m_e, m_mu, m_tau]))
nhat = np.ones(3) / np.sqrt(3.0)
cosphi = float(y @ nhat / np.linalg.norm(y))
phi = np.arccos(cosphi)
phi_deg = float(np.degrees(phi))
c2_data = 2.0 / np.tan(phi)
ok_45 = abs(phi_deg - 45.0) < 1e-3
ok_c2 = abs(c2_data - 2.0) < 5e-5
record("P5_data_pin_c2_equals_2",
       ok_45 and ok_c2 and abs(table["c^2=2"]["t*_deg"] - 45.0) < 1e-12,
       {"t*(c) table": table, "phi_lepton_deg": round(phi_deg, 5),
        "c^2_data = 2*cot(phi)": f"{c2_data:.6f}",
        "|c^2-2|": f"{abs(c2_data - 2.0):.2e}",
        "statement": "only the Fock value c^2=2 gives 45deg; the measured "
                     "lepton masses pin c^2 to 2 at the 1e-5 level"})


# ════════════════════════════════════════════════════════════════════
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "test-results")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F92_per_constituent_phase.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)

n_pass = sum(1 for r in RESULTS.values() if r["pass"])
print(f"\n{'=' * 60}\nF92 per-constituent phase: {n_pass}/{len(RESULTS)} PASS"
      f"  ->  overall {'PASS' if PASS else 'FAIL'}")
sys.exit(0 if PASS else 1)
