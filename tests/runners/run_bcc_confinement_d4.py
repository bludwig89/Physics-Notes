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

The anisotropy is now DERIVED, and the default encodes it.  `--beta-t` defaults
to `beta_s * 4`, from `bcc_action.anisotropy_from_c_lat()`: isotropy of the
weak-field limit forces `beta_t/beta_s = 4 lambda^2/a_t^2`, F313's primitivity
(no local half-tick) is what licenses a FIXED a_t rather than a refinable one,
and `c_lat^2 = 1/3` fixes the value -- giving `xi = 1/c_lat = sqrt3` and
`beta_t/beta_s = 4` exactly.  Note that is `(4/3) xi^2`, NOT the hypercubic
`xi^2`: the 4/3 is BCC geometry.  Pass `--beta-t` explicitly to override, and
`--isotropic` to reproduce the earlier `beta_t = beta_s` convention.

It also executes F299's d=4 Casimir successor, which F299 specified in
`mc_reach()` and left unrun: the higher-rep loops chi_6, chi_8, chi_10 built
from Tr W, Tr W^2, Tr W^3 of the same loop matrices ("no new sampling -- the
same configurations, a different trace").  Casimir scaling is expected at
INTERMEDIATE R only; the triality-0 reps 8 and 10 must fall below the Casimir
line asymptotically once the string can break, and locating that crossover is
the question d=2 could not be asked.  Use `--N 3` -- the character polynomials
are SU(3).
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
                   help="beta_t; defaults to the DERIVED beta_s * 4/(3 c_lat^2)")
    p.add_argument("--isotropic", action="store_true",
                   help="force beta_t = beta_s, the superseded convention")
    p.add_argument("--casimir", action="store_true",
                   help="also run F299's d=4 higher-rep measurement (needs --N 3)")
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

    der = B.anisotropy_from_c_lat()
    beta_s = args.beta
    if args.beta_t is not None:
        beta_t = args.beta_t
        xi_source = "explicit --beta-t"
    elif args.isotropic:
        beta_t = beta_s
        xi_source = "--isotropic, the superseded beta_t = beta_s convention"
    else:
        beta_t = beta_s * float(der["beta_ratio"])
        xi_source = ("derived: beta_t/beta_s = 4 lambda^2/a_t^2 "
                     "= 4/(3 c_lat^2) = %s, xi = 1/c_lat = %.6f"
                     % (der["beta_ratio"], der["xi"]))
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

    casimir = None
    if args.casimir:
        if args.N != 3:
            p.error("--casimir needs --N 3: chi_6, chi_8 and chi_10 are the "
                    "SU(3) character polynomials")
        rep_tabs = []
        for _ in range(max(1, args.meas // 4)):
            for _ in range(4):
                B.sweep_4d(links, beta_s, beta_t, gen, n_or=args.n_or)
            rep_tabs.append(B.higher_rep_loop_table(links, args.r_max,
                                                    args.t_max))
        avg = {}
        for lab in rep_tabs[0]:
            avg[lab] = {k: float(np.mean([t[lab][k] for t in rep_tabs]))
                        for k in rep_tabs[0][lab]}
        casimir = B.casimir_scaling_from_loops(avg)
        casimir["n_configs"] = len(rep_tabs)
        casimir["rep_loops"] = {lab: {f"{R}x{T}": v
                                      for (R, T), v in avg[lab].items()}
                                for lab in avg}
        casimir["character_identity"] = B.character_identity_residual(
            n_samples=4)

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
                      "beta_ratio": beta_t / beta_s,
                      "xi": der["xi"], "xi_sq": str(der["xi_sq"]),
                      "beta_ratio_derived": str(der["beta_ratio"]),
                      "bcc_factor_vs_hypercubic": str(
                          der["beta_ratio"] / der["xi_sq"]),
                      "source": xi_source},
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
        "casimir_d4": casimir,
        "scope": ("Wilson loops and Creutz ratios on the model's own BCC "
                  "action, and (with --casimir) F299's d=4 higher-rep "
                  "successor. NOT a claim of an area law or a string tension: "
                  "row B7's residual is a missing transfer matrix with "
                  "positivity, which no amount of sampling supplies. The "
                  "anisotropy IS derived (see couplings.source); what is not "
                  "derived is the radiative correction to it -- the Karsch "
                  "coefficients of the hypercubic literature -- since the "
                  "matching here is tree level."),
    }

    # The runner's own failure mode (P1 / D9). Its registry record
    # `run-bcc-confinement-d4` fails by baseline diff, but the FILE had no
    # assert and the manifest could not link either artifact to it (the linker
    # matches `F107_x.json <-> test_F107_x.py` by stem, and `run_` is not
    # `test_`), so tools/audit_tests.py read it as UNFALSIFIABLE — which is what
    # put it on the 2026-08-19 ratchet list. These three are properties of the
    # SAMPLER, not of the physics under study, so they cannot make a real result
    # pass by accident: the links must stay in SU(N) (this is the check that
    # catches a broken reunitarisation or a wrong generator basis), and a mean
    # plaquette or Wilson loop is Re Tr U / N over a unitary loop, so it is
    # bounded by 1 by construction. A run that violates any of them has a broken
    # update, and every number below it is noise.
    assert res["unitarity_residual"] < 1e-10, (
        f"links left SU({args.N}): unitarity residual "
        f"{res['unitarity_residual']:.3e}")
    for _name, _v in res["plaquette"].items():
        assert -1.0 <= _v <= 1.0, f"plaquette {_name} = {_v} is not Re Tr U / N"
    for _loop, _v in res["wilson_loops"].items():
        assert -1.0 <= _v <= 1.0, f"Wilson loop {_loop} = {_v} is not Re Tr U / N"

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
        f"beta_s = {beta_s}, beta_t = {beta_t}; xi = {der['xi']:.6f} = 1/c_lat, "
        f"beta_t/beta_s derived {der['beta_ratio']} = "
        f"{der['beta_ratio'] / der['xi_sq']} x xi^2 (the 4/3 is BCC geometry).",
        f"Anisotropy source: {xi_source}.",
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
    if casimir:
        lines += ["", "## F299 d=4 Casimir successor", "",
                  f"{casimir['n_configs']} configs; character polynomials "
                  f"verified against explicit rep matrices at "
                  f"{casimir['character_identity']['worst_overall']:.2e}.", "",
                  "| R x T | sigma_6/sigma_3 | 5/2 | sigma_8/sigma_3 | 9/4 "
                  "| sigma_10/sigma_3 | 9/2 |",
                  "|---|---:|---:|---:|---:|---:|---:|"]
        if not casimir["rows"]:
            lines += [f"| (none) | — | 2.5 | — | 2.25 | — | 4.5 |", "",
                      f"**No usable row.** {casimir['coverage']}. This is a "
                      f"regime/statistics statement, not a failure: "
                      f"chi_8/d_8 = (|Tr W|^2 - 1)/8 sits near zero on a "
                      f"disordered configuration, so a corner loop goes "
                      f"non-positive and -ln is undefined. Raise --meas and "
                      f"--r-max, and go to the scaling window beta 5.8-6.2."]
        for row in casimir["rows"]:
            lines.append(
                f"| {row['R']} x {row['T']} "
                f"| {row.get('ratio_6') if row.get('ratio_6') is None else format(row['ratio_6'], '.4f')} | 2.5 "
                f"| {row.get('ratio_8') if row.get('ratio_8') is None else format(row['ratio_8'], '.4f')} | 2.25 "
                f"| {row.get('ratio_10') if row.get('ratio_10') is None else format(row['ratio_10'], '.4f')} | 4.5 |")
        lines += ["", casimir["coverage"], "", casimir["note"]]
    lines += ["", "## Scope", "", res["scope"], ""]

    out_md = os.path.join(root, "test-results", "bcc_confinement_d4.md")
    with open(out_md, "w") as fh:
        fh.write("\n".join(lines))

    print("\n".join(lines))
    print(f"\nwrote {out_json}\nwrote {out_md}")
    return res


if __name__ == "__main__":
    main()
