# test_F97_baryon_phase_closure.py
# 2026-06-05 - 13:30
#
# F97 — Does the F92 consistency fixed point extend to three constituents
# (the baryon sector)?
#
# F92 (N=2): L1 pair-sum kinematics m=sin(2t) [F73/F69/F46] and
# L2 bilinear condensate m=y^2 [F78] with Fock normalization y=sqrt(2) sin t
# are jointly satisfiable ONLY at t=45 deg, where three saturations coincide:
# amplitude unitarity (y=1), composite-mass peak (m=1), phase wrap (2t=pi/2).
#
# This script tests the N=3 (colour-neutral three-quark) extension:
#   L1(3): m = sin(3t)            (phase per tick = sum of constituent phases)
#   L2(3): m = y^3 (trilinear, baryon operator is eps_abc qqq) or m = y^2
#   Fock:  y = sqrt(3) sin t      (<2|a|3> = sqrt(3))
#   Caps:  wrap 3t <= pi/2 (F73 over-wrap bound) ; unitarity y <= 1
#
# Pure sympy/trig — no chiral transforms, numpy not load-bearing.

import json
import time
import sympy as sp

t0 = time.time()
results = {"finding": "F97", "date": "2026-06-05 - 13:30", "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement,
        "residual": str(residual),
        "status": "PASS" if status else "FAIL",
    }
    print(f"{name}: {statement} -> residual {residual} [{'PASS' if status else 'FAIL'}]")


t = sp.symbols("t", positive=True)
s = sp.sin(t)

# ---------------------------------------------------------------- P1
# N=2 recap (regression vs F92): unique fixed point at pi/4, caps coincide.
sol2 = sp.solveset(sp.Eq(2 * s**2, sp.sin(2 * t)), t,
                   domain=sp.Interval.open(0, sp.pi / 2))
p1a = sol2 == sp.FiniteSet(sp.pi / 4)
p1b = sp.simplify(sp.asin(1 / sp.sqrt(2)) - sp.pi / 4) == 0
record("P1", "N=2: unique fixed point {pi/4}; unitarity cap == wrap cap",
       0 if (p1a and p1b) else "solset/cap mismatch", p1a and p1b)

# ---------------------------------------------------------------- P2
# Cap-coincidence theorem: sin(pi/(2N)) = N^(-1/2) iff N in {1,2}.
# Proof for N>=3: sin x < x and pi/(2N) < N^(-1/2) iff N > pi^2/4 ~ 2.467,
# so sin(pi/(2N)) <= pi/(2N) < 1/sqrt(N) strictly for all N >= 3.
p2_exact = all(
    sp.simplify(sp.sin(sp.pi / (2 * N)) - 1 / sp.sqrt(N)) == 0
    for N in (1, 2)
)
p2_bound = sp.simplify(sp.pi**2 / 4) < 3  # pi^2/4 < 3, the N>=3 strictness driver
p2_split = all(
    sp.N(sp.sin(sp.pi / (2 * N)) - 1 / sp.sqrt(N)) < 0 for N in range(3, 13)
)
record("P2", "caps coincide iff N in {1,2}; strict split for N>=3 "
       "(sin x < x and pi/(2N) < N^(-1/2) for N > pi^2/4)",
       0 if (p2_exact and p2_bound and p2_split) else "theorem fails",
       p2_exact and bool(p2_bound) and p2_split)

# ---------------------------------------------------------------- P3
# N=3 trilinear fixed point: 3*sqrt(3)*sin^3 t = sin 3t.
# Closed form: sin^2 t* = 3/(4+3 sqrt 3) = (9 sqrt 3 - 12)/11.
s2_star = sp.Rational(3) / (4 + 3 * sp.sqrt(3))
closed = sp.simplify(sp.radsimp(s2_star) - (9 * sp.sqrt(3) - 12) / 11) == 0
s_star = sp.sqrt(s2_star)
res3 = sp.N(3 * sp.sqrt(3) * s_star**3 - sp.sin(3 * sp.asin(s_star)), 50)
t_star = sp.deg(sp.asin(s_star))
wrap3 = sp.deg(3 * sp.asin(s_star))
overwrap = sp.N(wrap3) > 90
record("P3", f"N=3 trilinear fixed point sin^2 t*=(9sqrt3-12)/11, "
       f"t*={sp.N(t_star, 8)} deg, 3t*={sp.N(wrap3, 8)} deg > 90 (over-wrap)",
       res3, closed and abs(res3) < 1e-45 and overwrap)

# ---------------------------------------------------------------- P4
# N=3 bilinear variant: 3 sin^2 t = sin 3t  ->  s* = (sqrt(57)-3)/8.
s_bi = (sp.sqrt(57) - 3) / 8
res_bi = sp.N(3 * s_bi**2 - sp.sin(3 * sp.asin(s_bi)), 50)
t_bi = sp.deg(sp.asin(s_bi))
wrap_bi = sp.deg(3 * sp.asin(s_bi))
record("P4", f"N=3 bilinear fixed point s*=(sqrt57-3)/8, "
       f"t*={sp.N(t_bi, 8)} deg, 3t*={sp.N(wrap_bi, 8)} deg > 90 (over-wrap)",
       res_bi, abs(res_bi) < 1e-45 and sp.N(wrap_bi) > 90)

# ---------------------------------------------------------------- P5
# Both N=3 fixed points sit in the gap between the caps:
# wrap cap 30 deg < t* < unitarity cap arcsin(1/sqrt3) = 35.264 deg.
# F73 stability (no over-wrap) therefore EXCLUDES both. Per-constituent
# cap for a stable triple: m_c <= sin(pi/6) = 1/2 exactly.
cap_low = sp.pi / 6
cap_high = sp.asin(1 / sp.sqrt(3))
in_gap = (sp.N(sp.asin(s_star)) > sp.N(cap_low)
          and sp.N(sp.asin(s_star)) < sp.N(cap_high)
          and sp.N(sp.asin(s_bi)) > sp.N(cap_low)
          and sp.N(sp.asin(s_bi)) < sp.N(cap_high))
half = sp.sin(sp.pi / 6) == sp.Rational(1, 2)
record("P5", "both fixed points inside the forbidden gap "
       "(30 deg, 35.264 deg); stable-triple cap m_c <= 1/2 exact",
       0 if (in_gap and half) else "gap/cap check fails", in_gap and half)

# ---------------------------------------------------------------- P6
# Z3 centre-phase closure arithmetic (the proposed baryon analog):
# fundamental quark carries centre phase 2pi/3. Closure (mod 2pi) for
# qqq and q-qbar; NON-closure for the diquark qq. Exact integers.
two_pi = 2 * sp.pi
z = two_pi / 3
qqq = sp.simplify(sp.Mod(3 * z, two_pi)) == 0
qqbar = sp.simplify(sp.Mod(z - z, two_pi)) == 0
diquark = sp.simplify(sp.Mod(2 * z, two_pi)) != 0
record("P6", "Z3 closure: qqq -> 0, q qbar -> 0, qq -> 4pi/3 != 0 (exact)",
       0 if (qqq and qqbar and diquark) else "Z3 arithmetic fails",
       qqq and qqbar and diquark)

# ---------------------------------------------------------------- P7
# Data anchor (quantitative, not exact): the phase-kinematic ceiling for a
# baryon built from constituent rest phases is sub-additive (F73), so the
# proton mass would be <= m_u+m_u+m_d. PDG: 2*2.16+4.67 = 8.99 MeV vs
# 938.272 MeV -> 0.96%. The no-go is CONSISTENT with observation: baryon
# mass is field (confinement) energy, not constituent phase kinematics.
mu, md, mp = 2.16, 4.67, 938.272  # PDG 2024 MSbar(2 GeV) u,d; proton
frac = (2 * mu + md) / mp
record("P7", f"PDG quark-sum/proton = {frac:.4%} (phase kinematics cannot "
       "supply the baryon mass; confinement must)", f"{frac:.6f}",
       frac < 0.02)

# ----------------------------------------------------------------
results["runtime_s"] = round(time.time() - t0, 3)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{n_pass}/{len(results['checks'])} PASS"
print(f"\nOverall: {results['summary']} ({results['runtime_s']} s)")

import pathlib
out = pathlib.Path(__file__).resolve().parent.parent / "test-results" / "F97_baryon_phase_closure.json"
out.write_text(json.dumps(results, indent=2))
print(f"Results written to {out}")
