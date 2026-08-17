"""Battery runner: the d=4 confinement measurement on the model's OWN lattice.

Replaces `forks/gauge/lgt_fork_A_mc.py` as the 3+1D confinement leg.  The fork
samples a SIMPLE-HYPERCUBIC ensemble with the textbook Wilson action; this runs
the genuine BCC action of F265 -- 6 minimal 4-bond rhombi per site plus 4 mixed
space-time rectangles -- on `BCC_3 spatial x Z Euclidean time`.

This is a `result_dump` at tier `battery`, NOT a gate record, and deliberately:
the gate budget is under two minutes and a single sandbox bash call is killed at
~45 s, so an area-law measurement cannot live there.  The gate record
`gauge-bcc-mc-d4` carries the exact/deterministic legs of the same engine.

    # sandbox smoke (seconds, statistics are meaningless)
    python3 tests/runners/run_bcc_confinement_d4.py --L 4 --Lt 4 --sweeps 40

    # production, on Ben's machine (hours)
    python3 tests/runners/run_bcc_confinement_d4.py \
        --L 12 --Lt 12 --N 3 --beta 2.2 --therm 2000 --meas 4000 --n-or 4 \
        --r-max 5 --t-max 5

WHAT IS AND IS NOT CLAIMED.  This emits Wilson loops, Creutz ratios and the
Polyakov loop.  A rising static potential and a plateau in chi(R,T) would be
EVIDENCE for an area law on the model's lattice; neither this script nor the
tree currently claims one, and completeness row B7's residual ("3+1D is
constructed, not proven") is untouched by any amount of sampling -- a proof
needs a transfer matrix with positivity, which the repo does not have at any
dimension above a single mode.  The honest contribution here is that the d=4
leg now runs on the right lattice.

The anisotropy is a free input.  `--beta-t` defaults to `--beta`, i.e.
xi = a_s/a_t = 1 by CONVENTION.  F313's primitivity result (no local half-tick)
says a_t is fixed by the rule rather than tunable and c_lat = 1/sqrt3 is where a
derived xi would come from, but that argument is not made here and no default
encodes it.  Sweep `--beta-t` to see how much it matters.
"""

import argparse
import json
import os
import sys
import time


def _bootstrap():
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(6):
        root = os.path.dirname(root)
        if os.path.isdir(os.path.join(root, "src", "casim")):
            break
    src = os.path.join(root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return root


def main(argv=None):
    root = _bootstrap()
    import numpy as np
    from casim.engine.gauge import bcc_action as B

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--L", type=int, default=4,
                   help="spatial extent (cubic embedding; must be EVEN, since "
                        "the parity classes are the BCC bipartition)")
    p.add_argument("--Lt", type=int, default=4, help="Euclidean time extent")
    p.add_argument("--N", type=int, default=2, help="gauge group SU(N)")
    p.add_argument("--beta", type=float, default=2.0, help="beta_s")
    p.add_argument("--beta-t", type=float, default=None,
                   help="beta_t; defaults to beta_s (xi = 1 by convention)")
    p.add_argument("--therm", type=int, default=40, help="thermalisation sweeps")
    p.add_argument("--meas", type=int, default=40, help="measurement sweeps")
    p.add_argument("--n-or", type=int, default=1,
                   help="over-relaxation passes per heat-bath pass")
    p.add_argument("--r-max", type=int, default=3)
    p.add_argument("--t-max", type=int, default=3)
    p.add_argument("--start", choices=("hot", "cold"), default="hot")
    p.add_argument("--seed-tag", default="prod")
    args = p.parse_args(argv)

    if args.L % 2:
        p.error("--L must be even: the update checkerboard is the parity "
                "bipartition of the BCC nearest-neighbour graph, and an odd "
                "extent does not close it under a <111> hop")

    beta_s = args.beta
    beta_t = args.beta if args.beta_t is None else args.beta_t
    shape = (args.L, args.L, args.L, args.Lt)
    tag = f"{args.seed_tag}_{args.L}_{args.Lt}_{args.N}_{beta_s}_{beta_t}"

    t0 = time.time()
    links = (B.hot_links_4d(shape, N=args.N, channel="d4_init_" + tag)
             if args.start == "hot" else B.cold_links_4d(shape, N=args.N))

    _, therm_hist = B.thermalise_4d(links, beta_s, beta_t, args.therm,
                                    n_or=args.n_or,
                                    channel="d4_therm_" + tag, record=True)

    gen = B._rng.for_channel("d4_meas_" + tag)
    tables, plaqs, polys = [], [], []
    for _ in range(args.meas):
        B.sweep_4d(links, beta_s, beta_t, gen, n_or=args.n_or)
        tables.append(B.wilson_loop_table(links, args.r_max, args.t_max))
        plaqs.append(B.mean_plaquette_4d(links))
        polys.append(B.polyakov_loop_4d(links))

    keys = sorted(tables[0].keys())
    wl_mean, wl_err = {}, {}
    for k in keys:
        vals = np.array([t[k] for t in tables])
        wl_mean[k] = float(vals.mean())
        wl_err[k] = float(vals.std(ddof=1) / np.sqrt(len(vals))) \
            if len(vals) > 1 else 0.0
    chi = B.creutz_ratios(wl_mean)

    static_v = {}
    for R in range(1, args.r_max + 1):
        # V(R) a_t = -ln[ W(R,T) / W(R,T-1) ] at the largest available T
        T = args.t_max
        if (R, T) in wl_mean and (R, T - 1) in wl_mean:
            num, den = wl_mean[(R, T)], wl_mean[(R, T - 1)]
            if num > 0.0 and den > 0.0:
                static_v[R] = float(-np.log(num / den))

    res = {
        "generated": time.strftime("%Y-%m-%d - %H:%M"),
        "elapsed_s": round(time.time() - t0, 2),
        "lattice": {"geometry": "BCC_3 spatial x Z Euclidean time",
                    "shape": list(shape), "N": args.N,
                    "n_loops_per_site": B.BCC4_N_LOOPS,
                    "rhombus_area": B.BCC_PLAQ_AREA,
                    "mixed_area_over_at": B.BCC4_MIXED_AREA,
                    "sites": (args.L ** 3 // 4) * args.Lt},
        "couplings": {"beta_s": beta_s, "beta_t": beta_t,
                      "xi_note": "beta_t/beta_s is a CONVENTION; xi = a_s/a_t "
                                 "is not derived here"},
        "run": {"start": args.start, "therm": args.therm, "meas": args.meas,
                "n_or": args.n_or, "r_max": args.r_max, "t_max": args.t_max},
        "therm_history": [round(h, 6) for h in therm_hist],
        "plaquette": {"spatial": float(np.mean([p["spatial"] for p in plaqs])),
                      "temporal": float(np.mean([p["temporal"] for p in plaqs])),
                      "all": float(np.mean([p["all"] for p in plaqs]))},
        "polyakov_abs": float(np.mean([abs(z) for z in polys])),
        "unitarity_residual": B.unitarity_residual_4d(links),
        "wilson_loops": {f"{R}x{T}": wl_mean[(R, T)] for (R, T) in keys},
        "wilson_loops_err": {f"{R}x{T}": wl_err[(R, T)] for (R, T) in keys},
        "creutz_ratios": {f"{R}x{T}": v for (R, T), v in sorted(chi.items())},
        "static_potential_at_Tmax": {str(R): v for R, v in static_v.items()},
        "scope": ("Wilson loops and Creutz ratios on the model's own BCC "
                  "action. NOT a claim of an area law or a string tension: "
                  "row B7's residual is a missing transfer matrix with "
                  "positivity, which no amount of sampling supplies."),
    }

    out_json = os.path.join(root, "test-results", "bcc_confinement_d4.json")
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w") as fh:
        json.dump(res, fh, indent=2, default=str)

    lines = [
        "# d=4 confinement on the genuine BCC lattice",
        "",
        f"Generated {res['generated']} in {res['elapsed_s']} s.",
        "",
        f"Lattice `{res['lattice']['geometry']}`, shape {shape}, SU({args.N}), "
        f"{res['lattice']['sites']} genuine BCC sites, "
        f"{B.BCC4_N_LOOPS} plaquettes per site "
        f"(6 rhombi + 4 mixed rectangles).",
        f"beta_s = {beta_s}, beta_t = {beta_t} (xi not derived).",
        "",
        f"Mean plaquette: spatial {res['plaquette']['spatial']:.6f}, "
        f"temporal {res['plaquette']['temporal']:.6f}.",
        f"|Polyakov| = {res['polyakov_abs']:.6f}. "
        f"Unitarity residual {res['unitarity_residual']:.2e}.",
        "",
        "## Wilson loops",
        "",
        "| R x T | W | err |",
        "|---|---:|---:|",
    ]
    for (R, T) in keys:
        lines.append(f"| {R} x {T} | {wl_mean[(R, T)]:.6f} "
                     f"| {wl_err[(R, T)]:.6f} |")
    lines += ["", "## Creutz ratios  chi(R,T)", "",
              "| R x T | chi |", "|---|---:|"]
    for (R, T), v in sorted(chi.items()):
        lines.append(f"| {R} x {T} | {v:.6f} |")
    lines += ["", "## Scope", "", res["scope"], ""]

    out_md = os.path.join(root, "test-results", "bcc_confinement_d4.md")
    with open(out_md, "w") as fh:
        fh.write("\n".join(lines))

    print("\n".join(lines))
    print(f"\nwrote {out_json}\nwrote {out_md}")
    return res


if __name__ == "__main__":
    main()
