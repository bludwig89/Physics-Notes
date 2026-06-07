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


def _cmd_gui(args) -> int:
    from .gui import gui_available, launch
    if not gui_available():
        print("[casim] GUI needs the optional extra: pip install casim[gui] "
              "(vispy + PyQt6).", file=sys.stderr)
        return 2
    launch(args.scenario)
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

    g = sub.add_parser("gui", help="(Phase E) interactive viewer")
    g.add_argument("scenario", nargs="?", default=None)
    g.set_defaults(func=_cmd_gui)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
