"""casim.cli — command-line entry point.

    casim run scenarios/photon_pair.yaml [--ticks N] [--seed S] [--out PATH]
    casim resume checkpoints/run_t1000.npz [--ticks N] [--out PATH]
    casim export checkpoints/run_t1000.npz [--out PATH] [--stride N]
    casim analyze test-results/photon_pair.json [--table]
    casim list-channels
    casim gui [scenario.yaml]            # Phase E (not yet implemented)
"""
from __future__ import annotations

import argparse
import sys
import time
from typing import List, Optional

from . import __version__
from .engine import (
    Simulation, registered_channels, registered_observers,
)
from .io import load_scenario, write_results, read_results, export_checkpoint
from . import analysis


def _cmd_run(args) -> int:
    scenario = load_scenario(args.scenario)
    if args.ticks is not None:
        scenario["ticks"] = args.ticks
    if args.seed is not None:
        scenario["seed"] = args.seed
    if args.L is not None:
        scenario.setdefault("lattice", {})["L"] = args.L
    sim = Simulation.from_scenario(scenario)
    if sim.title:
        print(f"[casim] {sim.title}")
    if sim.description:
        print(f"[casim] {sim.description}")
    print(f"[casim] running {sim.name!r}: lattice={sim.lattice.to_dict()} "
          f"seed={sim.seed} ticks={scenario['ticks']}")
    results = sim.run(int(scenario["ticks"]))

    out = args.out or scenario.get("output", {}).get("json")
    if out:
        path = write_results(results, out)
        print(f"[casim] wrote {path}")
    print(analysis.format_table(analysis.exactness_rows(results)))
    return 0


def _cmd_resume(args) -> int:
    sim = Simulation.resume(args.checkpoint)
    target = args.ticks if args.ticks is not None else sim.target_ticks
    sim.target_ticks = target
    print(f"[casim] resumed {sim.name!r} at tick {sim.tick}; "
          f"continuing to {target}")
    results = sim.run_to_target()
    out = args.out
    if out:
        path = write_results(results, out)
        print(f"[casim] wrote {path}")
    print(analysis.format_table(analysis.exactness_rows(results)))
    return 0


def _cmd_export(args) -> int:
    path = export_checkpoint(args.checkpoint, out=args.out, stride=args.stride)
    print(f"[casim] exported {args.checkpoint} → {path}")
    # Echo a one-line headline per channel so the terminal is useful too.
    results = read_results(path)
    print(f"[casim] {results['name']}  tick={results['tick']}  "
          f"lattice={results['lattice']}")
    for cname, c in results["channels"].items():
        drift = c.get("rel_drift")
        drift_s = f" drift={drift:.2e}" if isinstance(drift, float) else ""
        print(f"  {cname:16s} {c.get('label', c['type']):18s} "
              f"energy={c['energy']:.6g}{drift_s}")
    return 0


def _cmd_analyze(args) -> int:
    results = read_results(args.results)
    summ = analysis.summarize(results)
    if summ.get("title"):
        print(f"[casim] {summ['title']}")
    if summ.get("description"):
        print(f"[casim] {summ['description']}")
    print(f"[casim] {summ['name']}  ticks={summ['ticks']}  "
          f"lattice={summ['lattice']}")
    for oname, o in summ["observers"].items():
        print(f"  {o.get('label') or oname:22s} [{o['exactness']}]  "
              f"records={o['n_records']}  summary={o['summary']}")
    if args.table:
        print()
        print(analysis.format_table(analysis.exactness_rows(results)))
    return 0


def _cmd_list_channels(args) -> int:
    print("Channels (type → label, propagator class, topologies):")
    for name, cls in sorted(registered_channels().items()):
        label = cls.label or name
        print(f"  {name:20s} {label:20s} {cls.propagator:14s} "
              f"{list(cls.topologies)}")
    print("\nObservers (type → label, exactness):")
    for name, cls in sorted(registered_observers().items()):
        label = cls.label or name
        print(f"  {name:20s} {label:20s} {cls.exactness}")
    return 0


def _cmd_inventory(args) -> int:
    from .analysis.inventory import generate
    from . import verify
    checks = verify.run_all()
    path = generate(args.out)
    n_pass = sum(1 for c in checks if c.passed)
    for c in checks:
        flag = "PASS" if c.passed else "FAIL"
        print(f"  {c.name:22s} {c.channel:18s} {c.exactness:18s} "
              f"{c.residual:.3e}  {flag}")
    print(f"[casim] {n_pass}/{len(checks)} checks pass; wrote {path}")
    return 0 if n_pass == len(checks) else 1


def _cmd_test_registry(args) -> int:
    """Run declarative test-registry records — roadmap C7.2, decision D9.

    This is the selector half of `casim test`. The scale-tier suite (`--scale`,
    `--groups`) still exists for long scenario sweeps; anything addressed by
    id / finding / sector / kind / tier / exactness / param comes through here,
    where the registry — not a directory listing — decides what runs.
    """
    from .tests import registry as treg
    from .tests import runner as trunner

    ids = ([s.strip() for s in args.id.split(",") if s.strip()]
           if args.id else None)
    recs = treg.select(ids=ids, finding=args.finding, sector=args.sector,
                       kind=args.kind, tier=args.tier,
                       exactness=args.exactness, path=args.path,
                       include_archive=args.include_archive)
    if not recs:
        print("[casim] no registry record matches that selection.")
        print(f"        {len(treg.all_records())} record(s) available; "
              f"try `casim test --list --tier gate`.")
        return 1

    overrides: dict = {}
    for spec in (args.param or []):
        k, v = treg.parse_param(spec)
        overrides[k] = v

    if args.list:
        print(f"[casim] {len(recs)} registry record(s)"
              + (f"  (params overridden: {overrides})" if overrides else ""))
        for r in recs:
            fm = "" if r.has_failure_mode else "  [NO FAILURE MODE — debt]"
            print(f"  {r.tier:8s} {r.kind:14s} {r.sector:13s} {r.id}{fm}")
            if r.entry:
                print(f"           -> {r.module or r.path}:{r.entry}"
                      f"{('  params=' + str(r.params)) if r.params else ''}")
        c = treg.counts()
        print(f"\n  registry: {c['records']} record(s), "
              f"{c['legacy_script']} still legacy_script (declared debt)")
        return 0

    errs = treg.validate_all(recs)
    if errs:
        print("[casim] the selected records do not validate:")
        for e in errs[:20]:
            print(f"    {e}")
        return 2

    print(f"[casim] running {len(recs)} registry record(s)"
          + (f"; swept params {overrides}" if overrides else ""))

    def echo(res: "trunner.RunResult") -> None:
        print(f"  [{res.status:5s}] {res.id:44s} ({res.seconds:6.1f}s)"
              + (f"  — {res.detail[:110]}" if res.detail else ""), flush=True)

    report = trunner.run_selection(recs, overrides=overrides or None,
                                   timeout=args.timeout, on_result=echo,
                                   out_dir=args.out)
    print(trunner.format_report(report))
    if overrides:
        # A sweep's product is the drift, not a verdict.
        drifted = [i for i in report["items"] if i["metrics"].get("drift")]
        print(f"\n[casim] sweep: {len(drifted)} of {report['n']} record(s) "
              f"moved against the committed baseline.")
        for i in drifted[:10]:
            for line in i["metrics"]["drift"][:3]:
                print(f"    {i['id']}: {line[:140]}")
        return 0
    return 0 if not report["failed"] else 1


def _cmd_test(args) -> int:
    registry_mode = any([args.id, args.finding, args.sector, args.kind,
                         args.tier, args.exactness, args.path, args.param,
                         args.registry])
    if registry_mode:
        return _cmd_test_registry(args)
    from .suite import run_suite, build_plan, tier_names
    from .suite.runner import find_repo_root
    groups = tuple(g.strip() for g in args.groups.split(",") if g.strip())
    only = [s.strip() for s in args.only.split(",") if s.strip()] if args.only else None
    repo_root = find_repo_root()

    if args.list:
        import json as _json
        plan = build_plan(args.scale, groups, repo_root, only=only)
        print(f"[casim] suite plan — scale={args.scale}  groups={list(groups)}")
        for b in plan.get("battery", []):
            print(f"  battery/{b['group']:10s} {b['path']}")
        for grp in ("scenarios", "realspace"):
            for s in plan.get(grp, []):
                if s.get("error"):
                    print(f"  {grp}/{s['name']:26s} ERROR {s['error']}")
                    continue
                if s.get("realspace"):
                    print(f"  {grp}/{s['name']:26s} patch={s['physical_L']}^? "
                          f"block={s['block']}  ~{s['represented_cells']:.2e} cells  "
                          f"compute={s['compute_cells']:.2e}  ~{s['mem_gb']:.2f} GB"
                          + ("  [skip]" if s['skipped'] else ""))
                else:
                    print(f"  {grp}/{s['name']:26s} L={s['L']:<5d} ticks={s['ticks']:<6d} "
                          f"×{s['cost_factor']:<7.0f} ~{s['mem_gb']:.2f} GB"
                          + ("  [skip]" if s['skipped'] else ""))
        return 0

    report = run_suite(
        scale=args.scale, groups=groups, out_dir=args.out,
        report_every=args.report_every, checkpoint_every=args.checkpoint_every,
        mem_limit_gb=args.mem_gb, only=only, repo_root=repo_root,
        script_timeout=args.script_timeout, run_scripts=not args.no_scripts,
    )
    c = report["counts"]
    return 0 if (c.get("FAIL", 0) == 0 and c.get("ERROR", 0) == 0) else 1


def _cmd_index(args) -> int:
    """Regenerate the repo's indexes from the registries — roadmap C8.

    `--check` exits 1 if any generated file is stale, if a finding number is
    duplicated or gapped without a declaration in
    `docs/design/finding-numbers.yaml` (C8.2), or if a tests-index row is empty
    that the test registry could have filled.
    """
    from . import index as cindex

    targets = (tuple(t.strip() for t in args.only.split(",") if t.strip())
               if args.only else cindex.TARGETS)
    unknown = [t for t in targets if t not in cindex.TARGETS]
    if unknown:
        print(f"[casim] unknown index target(s): {unknown}; "
              f"choose from {list(cindex.TARGETS)}", file=sys.stderr)
        return 2

    res = cindex.build(targets, check=args.check)

    for name in targets:
        t = res["targets"].get(name)
        if t is None:
            continue
        state = ("STALE" if args.check and t["changed"] else
                 "wrote" if t["changed"] else "current")
        print(f"  {state:8s} {t['path']:44s} {t['entries']:>5} entries")
    for e in res["errors"]:
        print(f"  ERROR    {e}", file=sys.stderr)

    num = res["numbering"]
    print(f"\nfinding numbers   max F{num['max']}, {num['numbers']} distinct, "
          f"{num['files']} file(s)")
    print(f"  duplicates          {len(num['duplicates'])} "
          f"({len(num['undeclared_duplicates'])} undeclared, "
          f"{len(num['unreviewed_duplicates'])} declared but UNREVIEWED)")
    print(f"  gaps                {len(num['gaps'])} "
          f"({len(num['undeclared_gaps'])} undeclared)")

    st = res.get("staleness") or {}
    if "findings_behind" in st:
        print(f"\nexactness inventory   header {st['header_finding']} vs newest "
              f"{st['newest_finding']}  ->  {st['findings_behind']} findings behind")

    ta = res["tests_audit"]
    if ta["empty_but_linked"]:
        print(f"\ntests-index: {len(ta['empty_but_linked'])} record(s) have "
              f"manifest-linked artifacts they do not declare "
              f"(C7 arming to-do, not an index defect)")

    problems: list[str] = list(res["errors"])
    if num["undeclared_duplicates"]:
        problems.append(
            f"finding number(s) used twice with no entry in "
            f"docs/design/finding-numbers.yaml: {num['undeclared_duplicates']}")
    if num["undeclared_gaps"]:
        problems.append(f"undeclared finding-number gap(s): "
                        f"{num['undeclared_gaps']}")
    if num["undeclared_unnumbered"]:
        problems.append(f"finding file(s) with no F<number>- prefix and no "
                        f"declaration: {num['undeclared_unnumbered']}")
    if num["stale_declared_duplicates"]:
        problems.append(
            f"finding-numbers.yaml declares duplicate(s) that no longer exist "
            f"{num['stale_declared_duplicates']} — remove the exception, or it "
            f"silently re-arms the next collision")
    if st.get("findings_behind"):
        problems.append(f"exactness inventory is {st['findings_behind']} "
                        f"findings behind — run `casim index`")
    if args.check and res["stale"]:
        problems.append(f"stale generated file(s): {res['stale']}")

    if problems:
        print("\n[casim index] PROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        return 1
    if num["unreviewed_duplicates"]:
        print(f"\n[casim index] ok — but {len(num['unreviewed_duplicates'])} "
              f"declared duplicate(s) are still UNREVIEWED: "
              f"{num['unreviewed_duplicates']}. Recorded, not resolved.")
    else:
        print("\n[casim index] ok")
    return 0


def _cmd_gui(args) -> int:
    from .gui import gui_available, launch
    if not gui_available():
        print("[casim] GUI needs the optional extra: pip install casim[gui] "
              "(vispy + PyQt6).", file=sys.stderr)
        return 2
    launch(args.scenario)
    return 0


def _cmd_backend(args) -> int:
    """Report — and optionally benchmark — the active FFT backend.

    Roadmap P2.1. This exists because the fallback used to be invisible: pyfftw
    was preferred by ca_fft and never installed, so the project ran on
    single-threaded scipy for its whole history without ever saying so.
    """
    import numpy as np
    from casim.numerics import fft as ca_fft


    print(f"active FFT backend : {ca_fft.describe()}")
    avail = ["numpy"]
    if getattr(ca_fft, "_scipy_fft", None) is not None:
        avail.append("scipy")
    if getattr(ca_fft, "_pyfftw_fft", None) is not None:
        avail.append("pyfftw")
    print(f"available          : {', '.join(avail)}")
    if "pyfftw" not in avail:
        print("\n  pyfftw is not installed. Six of the eight channel types are\n"
              "  FFT-bound, so this is the cheapest speedup available:\n"
              "      pip install -e '.[fast]'")

    if not args.bench:
        return 0

    L = args.L
    rng = np.random.default_rng(0)
    a = (rng.standard_normal((L, L, L)) +
         1j * rng.standard_normal((L, L, L))).astype(np.complex128)

    print(f"\nbenchmark: complex128 {L}^3 fftn+ifftn, 5 reps after 2 warmups")
    original = ca_fft.get_backend()
    reference = None
    try:
        for name in avail:
            ca_fft.set_backend(name)
            for _ in range(2):
                out = ca_fft.ifftn(ca_fft.fftn(a))
            t0 = time.perf_counter()
            for _ in range(5):
                out = ca_fft.ifftn(ca_fft.fftn(a))
            dt = (time.perf_counter() - t0) / 5
            if reference is None:
                reference = out
                agree = "reference"
            else:
                # Different libraries differ in the last bits. In a project
                # whose product is a 1e-12 gate, quantify that rather than
                # assume it away.
                agree = f"max|delta| = {float(np.max(np.abs(out - reference))):.3e}"
            print(f"  {name:8s} {dt * 1e3:9.2f} ms   {agree}")
    finally:
        ca_fft.set_backend(original)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="casim", description=__doc__)
    p.add_argument("--version", action="version", version=f"casim {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("run", help="run a scenario YAML")
    r.add_argument("scenario")
    r.add_argument("--ticks", type=int, default=None)
    r.add_argument("--seed", type=int, default=None)
    r.add_argument("--L", type=int, default=None,
                   help="lattice edge length override (dial down for sandbox, "
                        "up for production)")
    r.add_argument("--out", default=None, help="JSON output path override")
    r.set_defaults(func=_cmd_run)

    rs = sub.add_parser("resume", help="resume a run from a checkpoint NPZ")
    rs.add_argument("checkpoint")
    rs.add_argument("--ticks", type=int, default=None,
                    help="target total tick count (default: scenario's)")
    rs.add_argument("--out", default=None, help="JSON output path")
    rs.set_defaults(func=_cmd_resume)

    ex = sub.add_parser("export",
                        help="dump a checkpoint NPZ to a compact readable JSON")
    ex.add_argument("checkpoint")
    ex.add_argument("--out", default=None,
                    help="JSON output path (default test-results/export_<name>.json)")
    ex.add_argument("--stride", type=int, default=1,
                    help="keep every Nth observer record (thin long time series)")
    ex.set_defaults(func=_cmd_export)

    a = sub.add_parser("analyze", help="summarise a results JSON")
    a.add_argument("results")
    a.add_argument("--table", action="store_true", help="print exactness table")
    a.set_defaults(func=_cmd_analyze)

    lc = sub.add_parser("list-channels", help="show channel/observer registry")
    lc.set_defaults(func=_cmd_list_channels)

    inv = sub.add_parser("inventory",
                         help="run canonical checks, regenerate exactness inventory")
    inv.add_argument("--out", default="test-results/casim-exactness-inventory.md")
    inv.set_defaults(func=_cmd_inventory)

    t = sub.add_parser("test",
                       help="run the unified grouped test suite at a scale tier")
    t.add_argument("--scale", default="smoke",
                   choices=["smoke", "10x", "100x", "1000x"],
                   help="scale tier: smoke (sandbox) → 1000x (orders of magnitude)")
    t.add_argument("--groups", default="battery,scenarios,realspace",
                   help="comma list: battery,scenarios,realspace")
    t.add_argument("--only", default=None,
                   help="comma list of scenario names to restrict to")
    t.add_argument("--out", default=None,
                   help="report dir (default test-results/suite/<scale>_<stamp>)")
    t.add_argument("--report-every", type=float, default=15.0,
                   help="seconds between progress heartbeats during long runs")
    t.add_argument("--checkpoint-every", type=int, default=0,
                   help="NPZ checkpoint cadence (ticks) for resumable long runs")
    t.add_argument("--mem-gb", type=float, default=None,
                   help="skip scenarios whose projected footprint exceeds this")
    t.add_argument("--script-timeout", type=float, default=900.0,
                   help="per standalone battery script timeout (s)")
    t.add_argument("--no-scripts", action="store_true",
                   help="battery: run only pytest-style files, skip standalone scripts")
    t.add_argument("--list", action="store_true",
                   help="dry-run: print the plan (sizes/cost/memory) and exit")
    # ---- roadmap C7.2 / D9: the test-registry selectors ----
    # Supplying any of these switches `casim test` into registry mode, where
    # the declarative records in tests/registry/*.yaml decide what runs.
    treg_group = t.add_argument_group(
        "test registry (D9)",
        "select declarative records from tests/registry/*.yaml")
    treg_group.add_argument("--id", default=None,
                            help="comma list of registry record ids")
    treg_group.add_argument("--finding", default=None,
                            help="every record verifying this finding, e.g. F234")
    treg_group.add_argument("--sector", default=None,
                            help="core|lattice|gauge|particles|interactions|"
                                 "forks|numerics|suite")
    treg_group.add_argument("--kind", default=None,
                            help="assertion|result_dump|scenario|legacy_script")
    treg_group.add_argument("--tier", default=None,
                            help="gate|battery|archive")
    treg_group.add_argument("--exactness", default=None,
                            help="exact|machine|quantitative|bracketed|external")
    treg_group.add_argument("--path", default=None,
                            help="substring match on a record's test file path")
    treg_group.add_argument("--param", action="append", default=None,
                            metavar="K=V",
                            help="override a record parameter and report the "
                                 "drift (repeatable); e.g. --param delta_star=2/9")
    treg_group.add_argument("--registry", action="store_true",
                            help="registry mode with no filter: every record")
    treg_group.add_argument("--include-archive", action="store_true",
                            help="include tier=archive (superseded) records")
    treg_group.add_argument("--timeout", type=float, default=None,
                            help="per-record timeout override (s)")
    t.set_defaults(func=_cmd_test)

    ix = sub.add_parser("index",
                        help="regenerate the repo indexes from the registries "
                             "(roadmap C8)")
    ix.add_argument("--check", action="store_true",
                    help="exit 1 if any generated index is stale")
    ix.add_argument("--only", default=None,
                    help="comma list of targets: findings,status,tests,code,"
                         "docs,results,exactness")
    ix.set_defaults(func=_cmd_index)

    g = sub.add_parser("gui", help="interactive viewer (needs casim[gui])")
    g.add_argument("scenario", nargs="?", default=None)
    g.set_defaults(func=_cmd_gui)

    b = sub.add_parser("backend",
                       help="show the active FFT backend (and optionally bench it)")
    b.add_argument("--bench", action="store_true",
                   help="time each available backend on a representative transform")
    b.add_argument("--L", type=int, default=64, help="cube edge for --bench")
    b.set_defaults(func=_cmd_backend)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
