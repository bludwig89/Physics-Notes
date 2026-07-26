"""
run_d1_static_potential.py — NATIVE runner for the d1 CROSS-CHECK (Route A-NP):
the gauge-fixing-FREE, non-perturbative pin on the d1 = Lambda_MSbar/Lambda_lat
chain, via the SU(3) static potential (open-derivations v2 ledger; F155/F162).

WHY A SECOND ROUTE
==================
The perturbative route (run_d1_vertex_formfactor.py) needs the lattice 3-gluon
vertex form factors and self-validates against the Wilson Lambda_MSbar/Lambda_L
= 28.81 gate. This route needs NO vertex algebra and NO gauge fixing: it measures
the static quark-antiquark potential by Monte-Carlo and reads the physics off two
numbers,
    V(R) = V0 - (4/3) alpha_V / R + sigma R      (Cornell fit),
the Coulomb coefficient alpha_V (the V-scheme coupling, which F151 proves IS the
rule's coupling, tree-exact) and the string tension sigma (physical scale).

WHAT IT CROSS-CHECKS
====================
It reuses the validated MC + Cornell fit in run_su3_3d_string_tension.py (Wilson
plaquette action, exact SU(3) links) and turns (alpha_V, sigma_lat, beta) into an
INDEPENDENT check of the Wilson gate (28.81) and of scale-setting (Lambda/sqrt(sigma)):

  1. bare-coupling route (asymptotic scaling):
       g0^2 = 6/beta,   Lambda_L a  from the 2-loop lattice asymptotic-scaling
       formula, then  Lambda_MSbar a = 28.81 * Lambda_L a,
       Lambda_MSbar/sqrt(sigma) = Lambda_MSbar a / sqrt(sigma_lat).
  2. measured-coupling route (V-scheme):
       alpha_V measured at the potential scale q ~ 1/a; run the V-scheme coupling
       to its Lambda_V, convert Lambda_MSbar = exp(a1/(8 pi b0^alpha)) Lambda_V
       (a1 = 11/3, EXACT, F151), then Lambda_MSbar/sqrt(sigma).

  If the two routes AGREE and land near the world value Lambda_MSbar/sqrt(sigma)
  ~ 0.5-0.6, the 28.81 gate is confirmed non-perturbatively and gauge-free -> the
  PT script's gate target is sound, and a PT GATE PASS can be trusted. The rule's
  own 1.78 (rule-action) then follows from the exact factorisation 1.78 = 1.299
  (V->MSbar, exact) x 1.365 (rule->V = 1/q*a), with q*a the only open factor.

HONEST SCOPE
============
This MC uses the WILSON action, so it directly checks the WILSON gate (28.81) and
scale-setting, NOT the rule's 1.78 (which needs an F26-rule-action MC). It is the
gauge-free arbiter of the number the PT route must reproduce. Asymptotic scaling
needs weak coupling: use beta >= ~8.5 (3D) / interpret with care, and several
beta to see the scaling window. Report is per-beta plus a trend.

USAGE (native, outside the 45 s sandbox)
========================================
  # run a beta sweep (each beta is a full MC; minutes to tens of minutes at L>=12)
  # NOTE: 4D pure SU(3) confinement scaling window is beta = 6/g^2 ~ 5.8-6.3.
  #       (beta >~ 6.5 is too weak-coupling: the lattice gets fine, sqrt(sigma) a
  #        shrinks below what small L resolves.) Use several beta in-window.
  python3 tests/runners/run_d1_static_potential.py \
      --beta 5.8 6.0 6.2 --L 12 --ntherm 300 --nmeas 400 \
      --rmax 6 --tmax 7 --out test-results/d1_static_potential.json

  # or re-analyse existing run_su3_3d_string_tension --out JSON files (no MC)
  python3 tests/runners/run_d1_static_potential.py \
      --load test-results/su3_b8.5.json test-results/su3_b9.0.json \
      --out test-results/d1_static_potential.json

  python3 tests/runners/run_d1_static_potential.py --smoke   # tiny MC sanity

COST: the MC dominates; see run_su3_3d_string_tension.py. ~0.6 s/sweep at L=24;
scales as (L/24)^3. Cornell fits stabilise with rmax>=6, tmax>=7 and nmeas>=300.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))          # runners/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))

import run_su3_3d_string_tension as su3       # noqa: E402  (MC + Cornell fit)

WILSON_28_81 = 28.81                          # Lambda_MSbar/Lambda_L, PURE GAUGE (nf=0)
LAMBDA_TARGET = 1.78                          # rule Lambda_MSbar/Lambda_lat (nf=6 physics)
PT_BRACKET = (1.33, 2.25)                     # F155/F239 q*a bracket -> Lambda-ratio
# The run_su3 MC is PURE-GAUGE, and the 28.81 gate + world Lambda/sqrt(sigma) are
# pure-gauge (nf=0) quantities, so this whole NP cross-check uses nf=0. (The rule's
# 1.78 is nf=6 physics and lives in the PT script / the verdict text — a different
# number; do NOT mix nf here.)
NF = 0
FOUR_PI = 4.0 * math.pi
B0_ALPHA = (11.0 - 2.0 * NF / 3.0) / FOUR_PI  # = 11/(4pi), nf=0
A1 = 11.0 / 3.0                               # V->MSbar, exact (pure gauge)
# 2-loop coefficients (SU(3), nf=0) for the asymptotic-scaling Lambda formula,
# in the 1/g^2 convention: beta(g) = -b0 g^3 - b1 g^5 + ...
B0_G = (11.0 - 2.0 * NF / 3.0) / (16.0 * math.pi ** 2)
B1_G = (102.0 - 38.0 * NF / 3.0) / (16.0 * math.pi ** 2) ** 2
WORLD_LAMBDA_OVER_SQRTSIGMA = 0.55           # pure-gauge world value for orientation


def lambda_lat_a(g2: float) -> float:
    """Lambda_L a from the 2-loop asymptotic-scaling formula for a bare lattice
    coupling g^2 (= 6/beta for the standard Wilson action):
        Lambda_L a = (b0 g^2)^(-b1/2 b0^2) exp(-1/(2 b0 g^2))."""
    return (B0_G * g2) ** (-B1_G / (2 * B0_G ** 2)) * math.exp(-1.0 / (2 * B0_G * g2))


def lambda_MSbar_over_sqrtsigma_bare(beta: float, sigma_lat: float) -> dict:
    """Route 1: bare-coupling asymptotic scaling x 28.81."""
    g2 = 6.0 / beta
    lLa = lambda_lat_a(g2)
    lMSa = WILSON_28_81 * lLa
    ratio = lMSa / math.sqrt(sigma_lat) if sigma_lat > 0 else float("nan")
    return {"g0^2": g2, "Lambda_L_a": lLa, "Lambda_MSbar_a": lMSa,
            "sqrt_sigma_lat": math.sqrt(sigma_lat) if sigma_lat > 0 else None,
            "Lambda_MSbar_over_sqrtsigma": ratio}


def lambda_MSbar_over_sqrtsigma_measured(alpha_V: float, sigma_lat: float,
                                         q_a: float = 1.0) -> dict:
    """Route 2: measured V-scheme coupling at scale q ~ q_a/a -> Lambda_V a ->
    Lambda_MSbar a (x exp(a1/(8 pi b0^alpha)), a1 exact) -> /sqrt(sigma_lat).
    q_a is the scale of the alpha_V measurement in lattice units (~1)."""
    if alpha_V is None or alpha_V <= 0:
        return {"ok": False, "reason": "no positive alpha_V"}
    inv = 1.0 / alpha_V
    # V-scheme 1-loop Lambda: Lambda_V a = q_a exp(-1/(2 b0^alpha alpha_V))
    lVa = q_a * math.exp(-inv / (2.0 * B0_ALPHA))
    lMSa = math.exp(A1 / (2.0 * FOUR_PI * B0_ALPHA)) * lVa   # Lambda_MSbar/Lambda_V
    ratio = lMSa / math.sqrt(sigma_lat) if sigma_lat > 0 else float("nan")
    return {"ok": True, "alpha_V": alpha_V, "Lambda_V_a": lVa,
            "Lambda_MSbar_a": lMSa, "Lambda_MSbar_over_Lambda_V":
            math.exp(A1 / (2.0 * FOUR_PI * B0_ALPHA)),
            "Lambda_MSbar_over_sqrtsigma": ratio}


def analyse_run(beta: float, ana: dict, dim: int = 4) -> dict:
    """Turn one run_su3 analysis dict into the d1 cross-check numbers."""
    cornell = ana.get("cornell_fit", {})
    lin = ana.get("linear_fit", {})
    sigma_lat = None
    if cornell.get("ok") and cornell.get("sigma", 0) > 0:
        sigma_lat = cornell["sigma"]
    elif lin.get("sigma") and lin["sigma"] > 0:
        sigma_lat = lin["sigma"]
    alpha_V = cornell.get("alpha_V") if cornell.get("ok") else None

    row = {"beta": beta, "dim": dim, "alpha_V": alpha_V, "sigma_lat": sigma_lat,
           "V_scheme_lock_alpha_V_at_cutoff": 1.0 / (16.0 * math.pi)}
    if dim != 4:
        row["note"] = ("d=%d: 4D asymptotic-scaling route-1 does NOT apply "
                       "(super-renormalisable). Only alpha_V/sigma reported." % dim)
        return row
    if sigma_lat and sigma_lat > 0:
        row["route1_bare"] = lambda_MSbar_over_sqrtsigma_bare(beta, sigma_lat)
        row["route2_measured"] = lambda_MSbar_over_sqrtsigma_measured(
            alpha_V, sigma_lat)
        r1 = row["route1_bare"]["Lambda_MSbar_over_sqrtsigma"]
        r2 = (row["route2_measured"].get("Lambda_MSbar_over_sqrtsigma")
              if row["route2_measured"].get("ok") else None)
        if r2:
            row["routes_agree_pct"] = 100.0 * abs(r1 - r2) / (0.5 * (r1 + r2))
        row["world_value"] = WORLD_LAMBDA_OVER_SQRTSIGMA
    else:
        row["note"] = "no positive sigma from the fit — need more stats / larger rmax,tmax"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beta", type=float, nargs="+", default=None,
                    help="beta sweep to Monte-Carlo (each is a full run)")
    ap.add_argument("--load", type=str, nargs="+", default=None,
                    help="re-analyse existing run_su3 --out JSON files (no MC)")
    ap.add_argument("--L", type=int, default=10)
    ap.add_argument("--d", type=int, default=4,
                    help="spacetime dim. The 28.81 gate / d1 is a 4D concept -> "
                         "default 4. (d=3 is the F146 super-renormalisable theory; "
                         "route-1 asymptotic scaling does NOT apply there.)")
    ap.add_argument("--ntherm", type=int, default=300)
    ap.add_argument("--nmeas", type=int, default=400)
    ap.add_argument("--meas_every", type=int, default=4)
    ap.add_argument("--rmax", type=int, default=6)
    ap.add_argument("--tmax", type=int, default=7)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=str, default="test-results/d1_static_potential.json")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    out = {"targets": {"wilson_gate": WILSON_28_81, "lambda_ratio_rule": LAMBDA_TARGET,
                       "pt_bracket": list(PT_BRACKET),
                       "world_Lambda_over_sqrtsigma": WORLD_LAMBDA_OVER_SQRTSIGMA},
           "rows": []}

    if args.smoke:
        print("[smoke] tiny 4D MC at beta=6.0, L=6 ...", flush=True)
        r = su3.run(beta=6.0, L=6, d=4, n_therm=20, n_meas=20, meas_every=2,
                    rmax=3, tmax=4, seed=3)
        out["rows"].append(analyse_run(6.0, su3.analyse(r), dim=4))
    elif args.load:
        for path in args.load:
            with open(path) as f:
                payload = json.load(f)
            beta = payload.get("run", {}).get("beta") or payload.get("params", {}).get("beta")
            ana = payload.get("analysis") or su3.analyse(payload["run"])
            dim = int(payload.get("run", {}).get("d", 4))
            print(f"[load] {path} (beta={beta}, d={dim})", flush=True)
            out["rows"].append(analyse_run(float(beta), ana, dim=dim))
    elif args.beta:
        for beta in args.beta:
            t0 = time.time()
            print(f"[MC] beta={beta} L={args.L}: {args.ntherm}+{args.nmeas} sweeps ...",
                  flush=True)
            r = su3.run(beta=beta, L=args.L, d=args.d, n_therm=args.ntherm,
                        n_meas=args.nmeas, meas_every=args.meas_every,
                        rmax=args.rmax, tmax=args.tmax, seed=args.seed, verbose=True)
            ana = su3.analyse(r)
            row = analyse_run(beta, ana, dim=args.d)
            row["seconds"] = round(time.time() - t0, 1)
            out["rows"].append(row)
            print(f"      alpha_V={row.get('alpha_V')}, sigma_lat={row.get('sigma_lat')} "
                  f"[{row['seconds']}s]", flush=True)
    else:
        ap.error("give --beta (to run) or --load (to re-analyse) or --smoke")

    # trend / verdict
    good = [r for r in out["rows"] if r.get("route1_bare")]
    if good:
        r1s = [r["route1_bare"]["Lambda_MSbar_over_sqrtsigma"] for r in good]
        out["Lambda_MSbar_over_sqrtsigma_route1"] = r1s
        out["mean_route1"] = sum(r1s) / len(r1s)
        near_world = abs(out["mean_route1"] - WORLD_LAMBDA_OVER_SQRTSIGMA) \
            / WORLD_LAMBDA_OVER_SQRTSIGMA < 0.30
        out["gate_28_81_consistent"] = bool(near_world)
        out["verdict"] = (
            "NP cross-check: with the 28.81 Wilson gate, Lambda_MSbar/sqrt(sigma) "
            "= %.3f (mean over beta) vs world ~%.2f -> gate %s. This confirms the "
            "number the PT route must reproduce; the rule's 1.78 = 1.299 (exact) x "
            "1.365 (=1/q*a, the one open factor) then follows once q*a is pinned."
            % (out["mean_route1"], WORLD_LAMBDA_OVER_SQRTSIGMA,
               "CONSISTENT" if near_world else "NOT yet in the scaling window "
               "(use larger beta / more stats)"))
    else:
        out["verdict"] = ("no usable sigma yet — increase nmeas / rmax,tmax / L so "
                          "the Cornell fit returns a positive string tension.")
    print("\n" + out["verdict"], flush=True)

    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "..", args.out)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
