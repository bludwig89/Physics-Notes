#!/usr/bin/env python3
"""Roadmap C2.4 — the constants sweep, with its polarity flipped.

P0.2 asked *"does every recorded site still agree with the registry?"*  That is
a provenance question, and it was the right one while decision D2 kept the
kernels authoritative.  C2's decision D7 makes the registry the source of
truth, so the question becomes the stronger one:

    **Does any unregistered site exist at all?**

This module is the engine for that sweep.  It is shared by
`tests/casim/test_constants_consistency.py` (the gate) and by the
`--ratchet` mode below (the countable-debt tracker, same pattern as
`tools/audit_tests.py` and C1's `tools/audit_numerics.py`).

Everything works by **AST inspection, never import**.  Importing a
`ca-simulation` kernel is mostly harmless; importing a `tests/findings` module
executes its physics and writes JSON.  A provenance check that imported its
subjects would be a slow, destructive test.

What counts as a finding
------------------------
A **rogue literal** is an expression that

  1. evaluates, under the safe literal-and-arithmetic subset below, to a value
     matching a registry constant that is marked ``sweep=True``,
  2. lives outside `src/casim/constants/`,
  3. is not covered by a ``MeasuredConstant`` record (C2.3), and
  4. is not itself a reference to a symbol imported from `casim.constants`.

Two constants can share a value (delta* = 2/9 and sin^2 theta_W on-shell = 2/9
are different objects, F231).  The sweep reports **every** symbol a value could
be, and never picks one — resolving that ambiguity is the author's job, and the
fix is to import the one they mean.

Usage
-----
    python3 tools/audit_constants.py                # human report
    python3 tools/audit_constants.py --list         # every rogue, with lines
    python3 tools/audit_constants.py --ratchet      # CI: fail on regression
    python3 tools/audit_constants.py --json out.json
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import os
import sys
from dataclasses import dataclass, asdict
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
if os.path.join(_REPO, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_REPO, "src"))

from casim.constants import (                                      # noqa: E402
    all_constants, all_measured, sweepable_constants, get,
)

# Roots swept, and what a finding in each one means.
GATE_ROOTS = ("src", "ca-simulation")     # C2 owns these: findings are failures
BACKLOG_ROOTS = ("tests",)                # C7 owns these: findings are counted
_SKIP_DIRS = ("__pycache__", ".pytest_cache", "deprecated", ".git", ".venv")

# The registry itself is where values live; it is not swept.
_EXEMPT_PREFIXES = ("src/casim/constants/",)

_RATCHET_FILE = os.path.join(_HERE, "constants_baseline.json")


# ---------------------------------------------------------------------------
# A safe evaluator for the literal-and-arithmetic subset the tree actually uses
# ---------------------------------------------------------------------------
_CONST_ATTRS = {
    ("math", "pi"): math.pi, ("np", "pi"): math.pi, ("numpy", "pi"): math.pi,
    ("math", "e"): math.e, ("np", "e"): math.e,
    ("math", "tau"): math.tau,
}
_FUNCS = {
    ("math", "sqrt"): math.sqrt, ("np", "sqrt"): math.sqrt,
    ("numpy", "sqrt"): math.sqrt,
    ("math", "cos"): math.cos, ("np", "cos"): math.cos,
    ("math", "sin"): math.sin, ("np", "sin"): math.sin,
    ("math", "log"): math.log, ("np", "log"): math.log,
    ("math", "exp"): math.exp, ("np", "exp"): math.exp,
}
_BUILTINS = {"float": float, "abs": abs, "int": int, "Fraction": Fraction}


class Unevaluable(Exception):
    """The expression uses something outside the safe subset."""


def safe_eval(node: ast.AST, env: dict[str, float]) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise Unevaluable("bool")
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise Unevaluable(f"non-numeric constant {node.value!r}")

    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise Unevaluable(f"unknown name {node.id}")

    if isinstance(node, ast.UnaryOp):
        v = safe_eval(node.operand, env)
        if isinstance(node.op, ast.USub):
            return -v
        if isinstance(node.op, ast.UAdd):
            return v
        raise Unevaluable("unary op")

    if isinstance(node, ast.BinOp):
        a, b = safe_eval(node.left, env), safe_eval(node.right, env)
        op = node.op
        if isinstance(op, ast.Add):
            return a + b
        if isinstance(op, ast.Sub):
            return a - b
        if isinstance(op, ast.Mult):
            return a * b
        if isinstance(op, ast.Div):
            return a / b
        if isinstance(op, ast.Pow):
            return a ** b
        raise Unevaluable("binary op")

    if isinstance(node, ast.Attribute):
        if isinstance(node.value, ast.Name):
            key = (node.value.id, node.attr)
            if key in _CONST_ATTRS:
                return _CONST_ATTRS[key]
        raise Unevaluable("attribute")

    if isinstance(node, ast.Call):
        fn = node.func
        if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name):
            key = (fn.value.id, fn.attr)
            if key in _FUNCS:
                return _FUNCS[key](*[safe_eval(a, env) for a in node.args])
            # sympy exact rationals: sp.Rational(2, 9) -> 2/9
            if fn.attr == "Rational" and len(node.args) == 2:
                return (safe_eval(node.args[0], env)
                        / safe_eval(node.args[1], env))
        elif isinstance(fn, ast.Name) and fn.id in _BUILTINS:
            return float(_BUILTINS[fn.id](*[safe_eval(a, env) for a in node.args]))
        raise Unevaluable("call")

    raise Unevaluable(type(node).__name__)


def module_assignments(path: str) -> dict[str, float]:
    """Module-level names -> numeric value, for everything safely evaluable.

    Best-effort: names whose right-hand side falls outside the safe subset are
    omitted.  This is a reader, not a Python interpreter.
    """
    with open(path, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=path)
    env: dict[str, float] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if node.value is None:
            continue
        try:
            val = safe_eval(node.value, env)
        except (Unevaluable, ZeroDivisionError, TypeError, ValueError, OverflowError):
            continue
        for t in targets:
            if isinstance(t, ast.Name):
                env[t.id] = val
    return env


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------
@dataclass
class Rogue:
    path: str
    lineno: int
    value: float
    could_be: list[str]          # every registry symbol this value matches
    binding: str | None          # the name it is assigned to, if any
    root: str                    # "gate" or "backlog"

    def __str__(self) -> str:
        who = self.binding or "<inline>"
        return (f"{self.path}:{self.lineno}: {who} = {self.value!r} "
                f"-> {' | '.join(self.could_be)}")


def _iter_py_files(roots):
    for root in roots:
        base = os.path.join(_REPO, root)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            for fn in sorted(filenames):
                if not fn.endswith(".py"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, _REPO).replace(os.sep, "/")
                if any(rel.startswith(p) for p in _EXEMPT_PREFIXES):
                    continue
                yield rel, full


def registry_imports(tree: ast.AST) -> set[str]:
    """Registry symbols this module imports (by their registry name)."""
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "casim.constants" or \
               node.module.startswith("casim.constants."):
                for a in node.names:
                    out.add(a.name)
    return out


def _binding_name(parents: dict, node: ast.AST) -> str | None:
    """The name an expression is bound to, walking up assignments/defaults."""
    cur = node
    for _ in range(6):
        p = parents.get(id(cur))
        if p is None:
            return None
        if isinstance(p, ast.Assign):
            for t in p.targets:
                if isinstance(t, ast.Name):
                    return t.id
            return None
        if isinstance(p, ast.AnnAssign) and isinstance(p.target, ast.Name):
            return p.target.id
        if isinstance(p, ast.keyword):
            return p.arg
        if isinstance(p, ast.arguments):
            return "<default>"
        cur = p
    return None


def scan(roots=GATE_ROOTS, root_label="gate") -> list[Rogue]:
    consts = sweepable_constants()
    measured = all_measured()
    rogues: list[Rogue] = []

    for rel, full in _iter_py_files(roots):
        try:
            src = open(full, encoding="utf-8").read()
            tree = ast.parse(src, filename=rel)
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue

        imported = registry_imports(tree)
        # MeasuredConstant records covering this file (C2.3), plus symbols the
        # registry has explicitly recorded as bound here at RUN TIME or as a
        # re-export.  Both are declarations: the registry already says how this
        # path gets the value, so a literal-looking node is expected.
        exempt_syms = {m.compares_to for m in measured if m.path == rel}
        exempt_syms |= {c.symbol for c in all_constants() for s in c.sites
                        if s.path == rel and s.kind in ("runtime", "reexport")}

        # Seed the evaluator with the module's own names, so the very common
        # two-step spelling
        #     SQRT3 = math.sqrt(3.0)
        #     C_LAT = 1.0 / SQRT3
        # is caught.  Four QED-precision kernels hid a c_lat definition behind
        # exactly this indirection and the first cut of the sweep walked past
        # all of them.  Names bound to an imported registry symbol are absent
        # from this env (an import is not an assignment), so a module that has
        # already been migrated stays clean.
        try:
            env = module_assignments(full)
        except (SyntaxError, ValueError, OSError):
            env = {}
        # Do not let a name that IS the registry import resolve to a number.
        for sym in imported:
            env.pop(sym, None)

        parents: dict[int, ast.AST] = {}
        for p in ast.walk(tree):
            for ch in ast.iter_child_nodes(p):
                parents[id(ch)] = p

        matched_nodes: set[int] = set()

        def _covered(node: ast.AST) -> bool:
            cur = parents.get(id(node))
            while cur is not None:
                if id(cur) in matched_nodes:
                    return True
                cur = parents.get(id(cur))
            return False

        for node in ast.walk(tree):
            if not isinstance(node, (ast.Constant, ast.BinOp, ast.Call,
                                     ast.UnaryOp)):
                continue
            if isinstance(node, ast.Constant) and not isinstance(node.value, float):
                continue          # a bare int cannot be a registry value
            if _covered(node):
                continue
            try:
                val = safe_eval(node, env)
            except (Unevaluable, ZeroDivisionError, TypeError, ValueError,
                    OverflowError):
                continue

            hits = [c.symbol for c in consts
                    if c.contains(val, rel=max(c.tol, 1e-9))]
            if not hits:
                continue
            matched_nodes.add(id(node))
            # A `coincidence` record says "in this file, a value that looks
            # like <compares_to> is a different object."  It clears the node
            # when <compares_to> is among the candidates, even if the value is
            # ambiguous between several constants — which it usually is, since
            # ambiguity is what made the collision worth declaring.
            if any(m.kind == "coincidence" and m.compares_to in hits
                   for m in measured if m.path == rel):
                continue
            # Already declared. Two different quantifiers, on purpose:
            #   ANY explicit declaration (a MeasuredConstant, or a registry
            #       Site of kind runtime/reexport) naming one of the candidates
            #       resolves the ambiguity — someone read this line and said
            #       which constant it is.
            #   ALL candidates must be imported for an import to clear it,
            #       because an import of delta_star does not explain a 2/9 that
            #       could equally be the Fierz coefficient.
            if any(h in exempt_syms for h in hits):
                continue
            if all(h in imported for h in hits):
                continue
            rogues.append(Rogue(
                path=rel,
                lineno=getattr(node, "lineno", 0),
                value=val,
                could_be=sorted(hits),
                binding=_binding_name(parents, node),
                root=root_label,
            ))
    return rogues


def unverified_import_sites() -> list[str]:
    """Sites declaring kind='import' whose file does not actually import it.

    A registry record that claims a module imports a constant, when it does
    not, is a provenance record that lies — the same failure P0's
    `test_every_recorded_site_exists` was built to catch, one level up.
    """
    bad: list[str] = []
    cache: dict[str, set[str]] = {}
    for c in all_constants():
        for s in c.sites:
            if s.kind != "import":
                continue
            full = os.path.join(_REPO, s.path)
            if not os.path.exists(full):
                bad.append(f"{c.symbol} -> {s.path} (file missing)")
                continue
            if s.path not in cache:
                try:
                    cache[s.path] = registry_imports(
                        ast.parse(open(full, encoding="utf-8").read()))
                except (SyntaxError, UnicodeDecodeError, OSError):
                    cache[s.path] = set()
            got = cache[s.path]
            # `<symbol>_f` is the float face of a Fraction-valued constant, and
            # importing it satisfies the site.  A BRACKETED constant has no
            # scalar surface at all (C2.2), so its sites import `endpoint` or
            # `bracket` instead — that is the friction working as designed, not
            # a missing import.
            if (c.symbol + "_f") in got:
                continue
            if c.bracket is not None and ({"endpoint", "bracket"} & got):
                continue
            if c.symbol not in got:
                bad.append(f"{c.symbol} -> {s.path} declares kind='import' but "
                           f"does not import {c.symbol} from casim.constants")
    return bad


def literal_site_count() -> dict[str, int]:
    """The C2 ratchet number: sites still holding their own value."""
    out: dict[str, int] = {}
    for c in all_constants():
        n = len(c.sites_of_kind("literal"))
        if n:
            out[c.symbol] = n
    return out


# ---------------------------------------------------------------------------
# Report / ratchet
# ---------------------------------------------------------------------------
def build_report() -> dict:
    gate = scan(GATE_ROOTS, "gate")
    backlog = scan(BACKLOG_ROOTS, "backlog")
    lits = literal_site_count()
    return {
        "constants": len(all_constants()),
        "sweepable": len(sweepable_constants()),
        "measured_records": len(all_measured()),
        "rogue_gate": len(gate),
        "rogue_backlog": len(backlog),
        "literal_sites": sum(lits.values()),
        "literal_sites_by_symbol": lits,
        "unverified_import_sites": unverified_import_sites(),
        "rogues": [asdict(r) for r in gate + backlog],
    }


def _load_baseline() -> dict:
    if os.path.exists(_RATCHET_FILE):
        with open(_RATCHET_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true",
                    help="print every rogue literal with its line")
    ap.add_argument("--ratchet", action="store_true",
                    help="fail if any counter regressed against the baseline")
    ap.add_argument("--write-baseline", action="store_true",
                    help="record the current counters as the new high-water mark")
    ap.add_argument("--json", metavar="PATH", help="write the full report as JSON")
    args = ap.parse_args(argv)

    rep = build_report()

    print(f"[constants] {rep['constants']} registered "
          f"({rep['sweepable']} sweepable), "
          f"{rep['measured_records']} MeasuredConstant records")
    print(f"[constants] rogue literals: {rep['rogue_gate']} in "
          f"{'/'.join(GATE_ROOTS)} (C2 gate), "
          f"{rep['rogue_backlog']} in {'/'.join(BACKLOG_ROOTS)} (C7 backlog)")
    print(f"[constants] sites still declaring their own value: "
          f"{rep['literal_sites']}")
    if rep["unverified_import_sites"]:
        print(f"[constants] {len(rep['unverified_import_sites'])} "
              f"UNVERIFIED import sites:")
        for b in rep["unverified_import_sites"]:
            print(f"    {b}")

    if args.list:
        for r in rep["rogues"]:
            tag = "GATE " if r["root"] == "gate" else "c7   "
            who = r["binding"] or "<inline>"
            print(f"  {tag} {r['path']}:{r['lineno']}: {who} = {r['value']!r} "
                  f"-> {' | '.join(r['could_be'])}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2)
        print(f"[constants] wrote {args.json}")

    if args.write_baseline:
        base = {k: rep[k] for k in
                ("rogue_gate", "rogue_backlog", "literal_sites")}
        with open(_RATCHET_FILE, "w", encoding="utf-8") as fh:
            json.dump(base, fh, indent=2)
        print(f"[constants] baseline written: {base}")
        return 0

    if args.ratchet:
        base = _load_baseline()
        if not base:
            print("[constants] no baseline; run --write-baseline once")
            return 1
        bad = []
        for k in ("rogue_gate", "rogue_backlog", "literal_sites"):
            if rep[k] > base.get(k, 0):
                bad.append(f"{k}: {base.get(k, 0)} -> {rep[k]}")
        if rep["unverified_import_sites"]:
            bad.append("unverified import sites present (see above)")
        if bad:
            print("\n[constants] RATCHET FAILED — these only go down:")
            for b in bad:
                print(f"    {b}")
            print("    Import the constant from casim.constants, or declare a "
                  "MeasuredConstant with a reason in casim/constants/measured.py.")
            return 1
        print("[constants] ratchet OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
