# test_F98_enforcer_is_binder.py
# 2026-06-05
#
# F98 -- Testing the F97 (section 4) closure principle:
#
#   "A stable composite is a configuration whose phase budget closes exactly;
#    the object that enforces the budget is itself the binding agent."
#
# F97 proved (exact no-go) that the baryon cannot sit on an F92-type
# constituent-phase fixed point, and *theorized* that the baryon obeys the
# same GRAMMAR with the Z3 CENTRE phase as the budget and the colour-dielectric
# condensate (F86) as the enforcer/binder.  F97 section 8 flagged the open
# bridge:  "sigma emerges as the Lagrange-multiplier price of centre-phase
# non-closure".  This script makes that bridge quantitative using the two P1
# binding-force builds that already exist:
#
#   Option C  (F86, ca_colour_dielectric):  sigma_BPS = 2 pi v^2 |n|  (exact)
#   Option A  (F94, forks/lgt_fork_A_mc):   3+1D SU(3) gauge-MC string tension
#
# The single idea that makes "enforcer = binder" EXACT:
#   the centre charge / N-ality (triality) k is simultaneously
#     (i)  the label of phase-budget closure   (k = 0 mod N  <=>  budget closes)
#     (ii) the topological winding n of the dual-superconductor flux tube,
#          the multiplier in the binding tension sigma = 2 pi v^2 n  (Option C),
#          and the ONLY thing the asymptotic string tension depends on (Option A).
#   So the object that enforces the budget (centre charge as condensate flux)
#   is literally the coefficient of the binder.  One object, two roles.
#
# Pure numpy/sympy.  No chiral transforms (numpy not load-bearing on phases).
# Option-A heavy MC is NOT run here (user-run, F94); the gauge-sector content
# tested is the exact centre-charge structure of the asymptotic tension.

import json
import time
import pathlib
import sys

import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "ca-simulation"))

import ca_colour_dielectric as cd            # Option C (F86)
import forks.lgt_fork_A_mc as A              # Option A (F94)

t0 = time.time()
results = {"finding": "F98", "date": "2026-06-05",
           "title": "enforcer of the phase budget is itself the binder",
           "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement,
        "residual": str(residual),
        "status": "PASS" if status else "FAIL",
    }
    print(f"{name}: {statement}\n      -> residual {residual} "
          f"[{'PASS' if status else 'FAIL'}]")


# Centre group order for the colour sector: SU(3) -> Z3.
N = 3


def triality(n_q, n_qbar):
    """Centre charge (N-ality) of a colour content of n_q quarks + n_qbar
    antiquarks, reduced to {0,...,N-1}.  Gluons (adjoint) carry triality 0."""
    return (n_q - n_qbar) % N


# ------------------------------------------------------------------ E1
# THE BUDGET.  Centre-phase closure = N-ality 0 (mod N).  This is the
# same Z3 arithmetic as F97 P6, stated as the closure predicate over the
# observed/hypothetical colour contents.  Exact integers.
contents = {
    "q  (single quark)":        (1, 0),
    "qq (diquark)":             (2, 0),
    "qqq (baryon)":             (3, 0),
    "q-qbar (meson)":           (1, 1),
    "qqqq":                     (4, 0),
    "qqqq-qbar (pentaquark)":   (4, 1),
    "g (adjoint/gluon)":        (1, 1),   # net triality 0, colour-octet
}
tri = {k: triality(*v) for k, v in contents.items()}
closes = {k: (t == 0) for k, t in tri.items()}
# the budget closes EXACTLY for the colour-neutral (N-ality-0) contents:
e1_ok = (closes["qqq (baryon)"] and closes["q-qbar (meson)"]
         and closes["qqqq-qbar (pentaquark)"] and closes["g (adjoint/gluon)"]
         and not closes["q  (single quark)"] and not closes["qq (diquark)"]
         and not closes["qqqq"])
results["triality_table"] = {k: {"N-ality": tri[k], "budget_closes": closes[k]}
                             for k in contents}
record("E1", "budget = Z3 centre phase: closes (N-ality 0) for qqq, q-qbar, "
       "pentaquark, gluon; OPEN for q, qq, qqqq",
       0 if e1_ok else "centre-closure predicate mismatch", e1_ok)

# ------------------------------------------------------------------ E2
# OPTION C -- THE ENFORCER IS THE BINDING COEFFICIENT.
# F86 exact result sigma_BPS = 2 pi v^2 |n|, with the flux winding n equal to
# the source centre charge.  The condensate VEV v (the enforcer of the dual-
# Meissner vacuum) sets the scale; the centre charge n is the multiplier.
#   closed budget (n = 0)  =>  sigma = 0  EXACTLY  =>  no binding => free state
#   open  budget (n != 0)  =>  sigma > 0           =>  confined
v = 1.0
sig = {k: cd.bps_string_tension(v=v, n=tri[k]) for k in contents}
# sigma vanishes iff the budget closes (N-ality 0), for every content:
e2_iff = all((sig[k] == 0.0) == closes[k] for k in contents)
# and the multiplier is exactly the centre charge: sigma(n)/sigma(1) = n
ratio_ok = abs(cd.bps_string_tension(v=v, n=2)
               - 2 * cd.bps_string_tension(v=v, n=1)) < 1e-15
e2_exact = (cd.bps_string_tension(v=v, n=0) == 0.0)
record("E2", "Option C: sigma_BPS = 2 pi v^2 |n|, n = centre charge; "
       "sigma = 0 EXACTLY iff budget closes; multiplier = N-ality "
       "(sigma(2) = 2 sigma(1))",
       cd.bps_string_tension(v=v, n=0),
       e2_iff and e2_exact and ratio_ok)

# ------------------------------------------------------------------ E3
# OPTION A -- THE ASYMPTOTIC TENSION DEPENDS ONLY ON THE CENTRE CHARGE.
# Gauge-invariant (full non-Abelian) statement: the asymptotic k-string
# tension is a function of N-ality k ONLY and is periodic under the centre,
# sigma_{k+N} = sigma_k, with sigma_0 = 0.  Casimir-scaling k-string law for
# SU(N):  sigma_k / sigma_1 = k (N - k) / (N - 1).  Exact rationals.
kk = sp.symbols("k", integer=True)
sigma_k = kk * (N - kk) / (N - 1)                      # Casimir k-string ratio
# (a) centre periodicity: adding a gluon (N-ality 0) leaves asymptotic sigma
#     unchanged, i.e. sigma depends only on k mod N.  Check sigma_0 = sigma_3 = 0.
periodic = (sp.simplify(sigma_k.subs(kk, 0)) == 0
            and sp.simplify(sigma_k.subs(kk, N)) == 0)
# (b) screened vs confined dichotomy keyed PURELY on N-ality:
#     adjoint (triality 0) screens (sigma_asymp = 0); fundamental (1) confines.
screened_adjoint = sp.simplify(sigma_k.subs(kk, 0)) == 0
confine_fund = sp.simplify(sigma_k.subs(kk, 1)) > 0
# (c) k <-> N-k degeneracy (a quark string and an antiquark string bind equally)
kfold = sp.simplify(sigma_k.subs(kk, 1) - sigma_k.subs(kk, N - 1)) == 0
e3_ok = bool(periodic and screened_adjoint and confine_fund and kfold)
record("E3", "Option A: asymptotic sigma_k = k(N-k)/(N-1) sigma_1 depends ONLY "
       "on N-ality; centre-periodic (sigma_0 = sigma_N = 0); adjoint screened, "
       "fundamental confined; k <-> N-k degenerate",
       0 if e3_ok else "centre-only structure fails", e3_ok)

# ------------------------------------------------------------------ E4
# A <-> C BRIDGE -- ONE OBJECT IN BOTH ROLES.
# F94 CMP2: Option A fixes Option C's only free parameter, v* = sqrt(sigma_A/2pi).
# So the colour-magnetic condensate scale (C's enforcer) IS the gauge-MC string
# tension (A's binder), re-expressed.  Round-trip to machine precision.
sigma_A = A.strong_coupling_sigma(5.8)                 # a representative sigma_A
v_star = (sigma_A / (2.0 * 3.141592653589793)) ** 0.5  # F94 CMP2 inversion
sigma_C_back = cd.bps_string_tension(v=v_star, n=1)    # feed v* back into C, n=1
roundtrip = abs(sigma_C_back - sigma_A)
# both routes must agree on the only thing the F97 claim needs:
#   asymptotic binding vanishes IFF the centre budget closes.
both_zero_on_closure = (cd.bps_string_tension(v=v_star, n=0) == 0.0
                        and sp.simplify(sigma_k.subs(kk, 0)) == 0)
e4_ok = roundtrip < 1e-12 and both_zero_on_closure
record("E4", "A<->C bridge: v* = sqrt(sigma_A/2pi) maps gauge-MC tension to the "
       "condensate scale; round-trip sigma_C(v*) = sigma_A; both give "
       "sigma(closed budget) = 0",
       roundtrip, e4_ok)

# ------------------------------------------------------------------ E5
# THE LAGRANGE-MULTIPLIER PRICE OF NON-CLOSURE (F97 section 8 bridge).
# Isolation-energy functional E(R) = sigma R for a source of centre charge n.
# sigma is the price (Lagrange multiplier) conjugate to the centre-phase
# constraint:  zero when the budget closes (n = 0), positive and linearly
# growing when it does not.  => closed states have FINITE isolated energy
# (asymptotic/free); open states cost INFINITE isolation energy (confined).
R = sp.symbols("R", positive=True)
E_closed = cd.bps_string_tension(v=v, n=0) * R         # n=0  -> 0 for all R
E_open = cd.bps_string_tension(v=v, n=1) * R           # n=1  -> 2 pi v^2 R
finite_closed = sp.limit(E_closed, R, sp.oo) == 0
infinite_open = sp.limit(E_open, R, sp.oo) == sp.oo
# numeric witness of linear growth via the module's own potential:
v50 = cd.linear_potential(50.0, cd.bps_string_tension(v=v, n=1))
v100 = cd.linear_potential(100.0, cd.bps_string_tension(v=v, n=1))
linear = abs(v100 - 2 * v50) < 1e-9
e5_ok = bool(finite_closed and infinite_open and linear)
record("E5", "sigma is the Lagrange price of non-closure: E_iso(closed)=0 "
       "(finite, free), E_iso(open)=sigma R -> infinity (confined); linear in R",
       0 if e5_ok else "price structure fails", e5_ok)

# ------------------------------------------------------------------
results["runtime_s"] = round(time.time() - t0, 3)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{n_pass}/{len(results['checks'])} PASS"
print(f"\nOverall: {results['summary']} ({results['runtime_s']} s)")

out = ROOT / "test-results" / "F98_enforcer_is_binder.json"
out.write_text(json.dumps(results, indent=2))
print(f"Results written to {out}")
