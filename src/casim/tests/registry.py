"""casim.tests.registry — declarative test records (roadmap C7.1, decision **D9**).

Before C7 this repo had 345 test files, six invocation conventions, 321 doing
physics at import, 232 with no ``assert``, and 70 with **no failure mode by any
mechanism**. None of that was visible from the files themselves: the only way to
know what a test claimed was to read it.

A registry record makes the contract explicit:

    - id: F234-Wvc-triple-closure
      path: tests/findings/test_F234_Wvc_triple_closed.py
      kind: assertion
      sector: particles
      findings: [F234]
      module: casim.engine.particles.lepton_shape
      entry: check_triple_closure
      params: {delta_star: 2/9}
      expect: {exactness: exact, tol: 0}
      results: [test-results/F234_Wvc.json]
      tier: gate

Four kinds, two result contracts
--------------------------------
=================  ==========================================  =================
kind               contract                                    failure mode
=================  ==========================================  =================
``assertion``      returns bool / raises, or delegates to the  direct
                   file's own pytest functions
``result_dump``    produces a dict written to ``results:``     baseline diff vs
                                                               git HEAD (P1.2)
``scenario``       a scenario YAML run plus ``expect:`` gates   observable out of
                                                               tolerance
``legacy_script``  wraps an unmigrated file                     **declared debt**
=================  ==========================================  =================

``legacy_script`` is the migration ramp. Every test file gets a record on day
one, so coverage is 100% immediately and the remaining work is a *countable*
number that a ratchet drives down, rather than a 345-file big bang.

The teeth
---------
:func:`validate` refuses a record that claims a real kind while having no way to
fail. That is the structural closure of P1's honest PARTIAL on "zero tests in
RAN limbo": a test either has a failure mode, or it is labelled debt. There is
no third state a record can express.

Two vocabularies, one meaning each
----------------------------------
``sector`` uses the **module** sector vocabulary (``casim.engine.registry``'s
``MODULE_SECTORS`` plus ``suite`` for package/infrastructure tests). The C7
roadmap sketch showed ``sector: lepton``; that reading is *not* used, because
C8 joins this registry to the module registry and two meanings of "sector" in
one repo would break both queries. The physics grouping the sketch wanted is
``--finding`` (``casim test --finding F234``), which is exact rather than
inferred.

Field ownership
---------------
``evidence:`` is **generated** — ``tools/gen_test_registry.py`` rewrites it from
the tree on every run. Everything else is **human-owned** and preserved across
regeneration, exactly as ``dead_symbols`` is in the migration manifest.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Any, Iterable

import yaml

from casim.constants import EXACTNESS_CLASSES
from casim.engine.registry import MODULE_SECTORS

__all__ = [
    "TestRecord", "KINDS", "TIERS", "TEST_SECTORS",
    "load", "all_records", "get", "select", "by_finding",
    "test_files", "unregistered_files", "check_coverage",
    "validate", "validate_all", "counts", "registry_dir",
    "parse_param", "REGISTRY_DIR",
    "CONTROL_KEYS", "normalise_controls",
]

# ---------------------------------------------------------------------------
# Closed vocabularies. A record outside them does not load.
# ---------------------------------------------------------------------------
KINDS = {
    "assertion": "returns bool / raises, or delegates to the file's pytest "
                 "functions; the failure mode is direct",
    "result_dump": "emits numbers into `results:`; the failure mode is the "
                   "P1.2 baseline diff against git HEAD",
    "scenario": "a scenario YAML run plus `expect:` gates; fails when a gated "
                "observable leaves tolerance",
    "legacy_script": "wraps an unmigrated file. DECLARED DEBT: whatever failure "
                     "mode it had, which may be none. Counted by the ratchet.",
}

TIERS = {
    "gate": "fast and asserting; runs on every change (`make gate`)",
    "battery": "the full scaled suite; hours, run explicitly",
    "archive": "fully superseded per docs/theory/supersessions.yaml; excluded",
}

# ---------------------------------------------------------------------------
# Negative controls (gap #3 of docs/status/completeness-2026-08-07.md, row H2).
#
# The practice already existed, in prose. Ten gate records say things like
# "`--param tower=symmetric` reds L2 and L3" and "all four controls verified red
# on their own legs" in their `notes:` — a sentence no machine reads, written by
# the same sessions whose ratchet numbers did not move for three days. A norm
# that lives in a paragraph is a norm that is re-decided every session.
#
# A `control:` block is that sentence as data:
#
#     control:
#       - params: {linear_control: true}
#         reds:   [G10-3, G10-4, G10-5, G10-6]
#         reason: dispersion replaced by exactly linear c|k|, so every lattice
#                 correction must vanish
#
# and the contract it declares has THREE parts, all three of which the prose
# already claims and none of which anything checked:
#
#   1. the named legs are GREEN without the perturbation  (else it proves nothing)
#   2. the named legs are RED with it                     (the check can fail)
#   3. nothing else goes red                              ("and only where declared")
#
# Part 3 is not decoration. A perturbation that reddens the whole run is a
# broken run, not a control, and it is the cheap way to fake part 2.
CONTROL_KEYS = {
    "params": "the perturbation, as `casim test --param k=v` would apply it",
    "reds": "leg ids that MUST go red under it; omit to require only that the "
            "record's overall verdict flips PASS -> FAIL",
    "reason": "why a sound check must fail here. REQUIRED — a control whose "
              "point is not stated cannot be reviewed",
    "only": "default true: legs outside `reds` must stay green. Set false when "
            "the perturbation is legitimately global, and say so in `reason`",
    "test": "weak form, for records with no `entry:`: the name of the in-file "
            "pytest function that IS the negative control. Proves one exists "
            "and runs; does NOT prove the harness can perturb the physics",
}

# The module-registry sectors, plus the one home that is not a physics sector.
TEST_SECTORS = tuple(MODULE_SECTORS) + ("suite",)

_HERE = os.path.dirname(os.path.abspath(__file__))                 # src/casim/tests
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))   # repo root
REGISTRY_DIR = os.path.join(_REPO, "tests", "registry")

# Directories that hold test files. `tests/falsification` holds spec briefs
# (markdown), not code, and `tests/test-results` is a stray output dir.
TEST_DIRS = ("tests/casim", "tests/findings", "tests/priority", "tests/runners")
_NOT_A_TEST = {"__init__.py", "conftest.py"}


def registry_dir() -> str:
    return REGISTRY_DIR


# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class TestRecord:
    """One declarative test. See the module docstring for the field contract."""

    id: str
    kind: str
    sector: str
    tier: str = "battery"
    path: str | None = None            # repo-relative test file, if it has one
    findings: tuple[str, ...] = ()
    module: str | None = None          # dotted import path of the entry point
    entry: str | None = None           # callable inside `module` (or `path`)
    params: dict[str, Any] = field(default_factory=dict)
    expect: dict[str, Any] = field(default_factory=dict)
    results: tuple[str, ...] = ()      # baselines, repo-relative
    scenario: str | None = None        # scenarios/*.yaml for kind=scenario
    superseded_by: str | None = None   # supersession-ledger record id
    notes: str = ""
    timeout: float | None = None       # seconds; None = the runner's default
    control: tuple[dict[str, Any], ...] = ()   # declared negative controls
    evidence: dict[str, Any] = field(default_factory=dict)   # GENERATED
    source_file: str | None = None     # which registry YAML it came from

    # -- derived ----------------------------------------------------------
    @property
    def exactness(self) -> str | None:
        v = self.expect.get("exactness")
        return str(v) if v is not None else None

    @property
    def tol(self) -> float | None:
        v = self.expect.get("tol")
        return None if v is None else float(v)

    @property
    def delegates_to_pytest(self) -> bool:
        """True when the file's own pytest functions ARE the entry point.

        This is how `pytest` and `casim test --tier gate` are guaranteed to run
        the same objects: for these records the registry decides *whether* the
        file runs and the tier it runs in, and pytest performs the collection.
        """
        return (self.kind == "assertion" and self.entry is None
                and bool(self.evidence.get("pytest_funcs")))

    @property
    def has_failure_mode(self) -> bool:
        if self.kind == "legacy_script":
            return False                       # the whole point of the label
        if self.kind == "assertion":
            return bool(self.entry) or self.delegates_to_pytest
        if self.kind == "result_dump":
            return bool(self.results) or bool(self.entry)
        if self.kind == "scenario":
            # `gates: all` means "every observable this scenario declares a
            # tolerance for" — the scenario's own committed gates, which is a
            # real failure mode. An empty list is NOT: it gates nothing.
            gates = self.expect.get("gates")
            return bool(self.scenario) and (
                gates == "all" or bool(gates) or self.expect.get("tol") is not None)
        return False

    @property
    def has_control(self) -> bool:
        return bool(self.control)

    @property
    def control_strength(self) -> str:
        """``none`` | ``weak`` | ``strong``.

        ``strong`` means at least one control the harness applies itself, by
        overriding a parameter the entry point actually takes. ``weak`` means
        the record only points at a pytest function that calls itself a negative
        control — worth having, and not the same claim. Keeping the two apart is
        the whole reason this is a vocabulary and not a boolean: a checker that
        scored them alike would let the easy half absorb the hard half, which is
        the A10 mistake this report already had to correct once.
        """
        if not self.control:
            return "none"
        if any(c.get("params") for c in self.control):
            return "strong"
        return "weak"

    @property
    def needs_control(self) -> bool:
        """Scope of the D9 requirement: gate-tier ``assertion`` records.

        Deliberately not all 400. `kind: result_dump` already fails by baseline
        diff and `kind: scenario` by a gated observable; the kind with no
        second opinion is the one that asserts, which is also the kind the
        58-record gate tier is made of.
        """
        return self.kind == "assertion" and self.tier == "gate"

    def as_yaml_record(self) -> dict[str, Any]:
        """The human-owned + generated payload, in a stable field order."""
        out: dict[str, Any] = {"id": self.id, "kind": self.kind,
                               "sector": self.sector, "tier": self.tier}
        if self.path:
            out["path"] = self.path
        if self.findings:
            out["findings"] = list(self.findings)
        if self.module:
            out["module"] = self.module
        if self.entry:
            out["entry"] = self.entry
        if self.params:
            out["params"] = dict(self.params)
        if self.expect:
            out["expect"] = dict(self.expect)
        if self.results:
            out["results"] = list(self.results)
        if self.scenario:
            out["scenario"] = self.scenario
        if self.superseded_by:
            out["superseded_by"] = self.superseded_by
        if self.timeout is not None:
            out["timeout"] = self.timeout
        if self.control:
            out["control"] = [dict(c) for c in self.control]
        if self.notes:
            out["notes"] = self.notes
        if self.evidence:
            out["evidence"] = dict(self.evidence)
        return out


# ---------------------------------------------------------------------------
# Validation — the teeth.
# ---------------------------------------------------------------------------
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")


def validate(rec: TestRecord) -> list[str]:
    """Problems with one record. Empty list means the record is well formed."""
    errs: list[str] = []
    if not _ID_RE.match(rec.id):
        errs.append(f"id {rec.id!r} is not a slug ([A-Za-z0-9_.-])")
    if rec.kind not in KINDS:
        errs.append(f"kind {rec.kind!r} not one of {sorted(KINDS)}")
    if rec.tier not in TIERS:
        errs.append(f"tier {rec.tier!r} not one of {sorted(TIERS)}")
    if rec.sector not in TEST_SECTORS:
        errs.append(f"sector {rec.sector!r} not one of {sorted(TEST_SECTORS)}")
    ex = rec.expect.get("exactness")
    if ex is not None and ex not in EXACTNESS_CLASSES:
        errs.append(f"expect.exactness {ex!r} not in {sorted(EXACTNESS_CLASSES)}")
    if rec.kind == "scenario":
        if not rec.scenario:
            errs.append("kind=scenario needs a `scenario:` YAML path")
    elif not rec.path and not (rec.module and rec.entry):
        errs.append("needs either `path:` or both `module:` and `entry:`")
    if rec.path and not os.path.exists(os.path.join(_REPO, rec.path)):
        errs.append(f"path {rec.path} does not exist")
    if rec.scenario and not os.path.exists(os.path.join(_REPO, rec.scenario)):
        errs.append(f"scenario {rec.scenario} does not exist")
    for r in rec.results:
        if not os.path.exists(os.path.join(_REPO, r)):
            errs.append(f"results entry {r} does not exist")
    if not rec.has_failure_mode and rec.kind != "legacy_script":
        errs.append(
            f"kind={rec.kind} declares no failure mode — give it an `entry:`, "
            f"a `results:` baseline, or `expect:` gates, or label it "
            f"`legacy_script` (declared debt). A record may not declare neither.")
    if rec.entry and not (rec.module or rec.path):
        errs.append("`entry:` needs a `module:` or a `path:` to find it in")
    errs += _validate_controls(rec)
    return errs


def _validate_controls(rec: TestRecord) -> list[str]:
    """Shape of the `control:` blocks. Presence is the ratchet's job, not this.

    The split matters. Refusing every gate record that has no control would turn
    54 of 55 red on the day this lands, and a gate that is red for a week is a
    gate people learn to run with `|| true`. So a MISSING control is a counted
    debt (`gate_assertion_no_control`, ratcheted to zero in audit_tests.py) and a
    MALFORMED one is an immediate error — the same shape as `legacy_script`,
    which is the one migration ramp in this repo that actually drained.
    """
    errs: list[str] = []
    for i, c in enumerate(rec.control):
        where = f"control[{i}]"
        if not isinstance(c, dict):
            errs.append(f"{where} is not a mapping")
            continue
        unknown = sorted(set(c) - set(CONTROL_KEYS))
        if unknown:
            errs.append(f"{where}: unknown key(s) {unknown}; "
                        f"allowed {sorted(CONTROL_KEYS)}")
        if not str(c.get("reason") or "").strip():
            errs.append(f"{where}: `reason:` is required — a perturbation "
                        f"whose point is not written down cannot be reviewed, "
                        f"only re-run")
        has_params = bool(c.get("params"))
        has_test = bool(c.get("test"))
        if not has_params and not has_test:
            errs.append(f"{where}: needs `params:` (the perturbation) or "
                        f"`test:` (the in-file negative control)")
        if has_params and not isinstance(c.get("params"), dict):
            errs.append(f"{where}: `params:` must be a mapping of k: v")
        if has_params and not rec.entry:
            errs.append(
                f"{where}: `params:` cannot be injected into a record with no "
                f"`entry:` — the runner would drop the override and the control "
                f"would pass by doing nothing. Give the record a "
                f"`module:`/`entry:` (C7.4), or use the weak `test:` form")
        reds = c.get("reds")
        if reds is not None:
            if not isinstance(reds, (list, tuple)) or not reds:
                errs.append(f"{where}: `reds:` must be a non-empty list of "
                            f"leg ids")
            elif not all(isinstance(x, str) and x.strip() for x in reds):
                errs.append(f"{where}: `reds:` entries must be leg id strings")
        if has_test and reds:
            errs.append(f"{where}: `reds:` needs a `params:` perturbation to "
                        f"attribute the reddening to; the `test:` form cannot "
                        f"say which legs moved")
        if "only" in c and not isinstance(c["only"], bool):
            errs.append(f"{where}: `only:` must be true or false")
    return errs


def validate_all(records: Iterable[TestRecord]) -> list[str]:
    """Cross-record problems plus every per-record problem, as flat messages."""
    recs = list(records)
    errs: list[str] = []
    seen_id: dict[str, str] = {}
    seen_path: dict[str, str] = {}
    for r in recs:
        for e in validate(r):
            errs.append(f"{r.id}: {e}")
        if r.id in seen_id:
            errs.append(f"{r.id}: duplicate id (also in {seen_id[r.id]})")
        seen_id[r.id] = r.source_file or "?"
        if r.path:
            if r.path in seen_path:
                errs.append(f"{r.id}: path {r.path} already claimed by "
                            f"{seen_path[r.path]}")
            seen_path[r.path] = r.id
    return errs


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
_RECORDS: dict[str, TestRecord] = {}
_LOADED = False


def _coerce(v: Any) -> Any:
    """`2/9` in YAML is a string; a test asserting exactness needs the Fraction.

    Only strings that are unambiguously a rational literal are converted, so a
    note reading "1/2 of the shell" is left alone.
    """
    if isinstance(v, str) and re.fullmatch(r"-?\d+/\d+", v.strip()):
        return Fraction(v.strip())
    return v


def normalise_controls(raw: Any) -> tuple[dict[str, Any], ...]:
    """Accept one control block or a list of them; coerce param literals.

    ``2/9`` in YAML is a string, and a control that perturbs an exact rational
    has to perturb it as a ``Fraction`` or the override silently changes type as
    well as value — which would make the run go red for the wrong reason and
    still be scored as a sound control.
    """
    if raw is None:
        return ()
    blocks = raw if isinstance(raw, list) else [raw]
    out: list[dict[str, Any]] = []
    for b in blocks:
        if not isinstance(b, dict):
            out.append(b)                      # let validate() report it
            continue
        c = dict(b)
        if isinstance(c.get("params"), dict):
            c["params"] = {k: _coerce(v) for k, v in c["params"].items()}
        if isinstance(c.get("reds"), (list, tuple)):
            c["reds"] = [str(x) for x in c["reds"]]
        out.append(c)
    return tuple(out)


def _record_from_dict(d: dict[str, Any], source_file: str) -> TestRecord:
    params = {k: _coerce(v) for k, v in (d.get("params") or {}).items()}
    return TestRecord(
        id=str(d["id"]),
        kind=str(d.get("kind", "legacy_script")),
        sector=str(d.get("sector", "suite")),
        tier=str(d.get("tier", "battery")),
        path=d.get("path"),
        findings=tuple(d.get("findings") or ()),
        module=d.get("module"),
        entry=d.get("entry"),
        params=params,
        expect=dict(d.get("expect") or {}),
        results=tuple(d.get("results") or ()),
        scenario=d.get("scenario"),
        superseded_by=d.get("superseded_by"),
        notes=str(d.get("notes") or ""),
        timeout=d.get("timeout"),
        control=normalise_controls(d.get("control")),
        evidence=dict(d.get("evidence") or {}),
        source_file=source_file,
    )


def load(force: bool = False) -> dict[str, TestRecord]:
    """Read every ``tests/registry/*.yaml``. Cached; ``force=True`` re-reads."""
    global _LOADED
    if _LOADED and not force:
        return _RECORDS
    _RECORDS.clear()
    if os.path.isdir(REGISTRY_DIR):
        for fn in sorted(os.listdir(REGISTRY_DIR)):
            if not fn.endswith((".yaml", ".yml")):
                continue
            full = os.path.join(REGISTRY_DIR, fn)
            with open(full, encoding="utf-8") as fh:
                doc = yaml.safe_load(fh) or {}
            for d in doc.get("tests") or []:
                rec = _record_from_dict(d, f"tests/registry/{fn}")
                _RECORDS[rec.id] = rec
    _LOADED = True
    return _RECORDS


def all_records() -> list[TestRecord]:
    return sorted(load().values(), key=lambda r: r.id)


def get(rec_id: str) -> TestRecord:
    return load()[rec_id]


def by_finding(fid: str) -> list[TestRecord]:
    f = fid.upper()
    return [r for r in all_records() if f in {x.upper() for x in r.findings}]


def select(*, ids: Iterable[str] | None = None, finding: str | None = None,
           sector: str | None = None, kind: str | None = None,
           tier: str | None = None, exactness: str | None = None,
           path: str | None = None,
           include_archive: bool = False) -> list[TestRecord]:
    """Every record matching all supplied filters (roadmap C7.2's selectors)."""
    out = all_records()
    if ids is not None:
        want = set(ids)
        out = [r for r in out if r.id in want]
    if finding:
        f = finding.upper()
        out = [r for r in out if f in {x.upper() for x in r.findings}]
    if sector:
        out = [r for r in out if r.sector == sector]
    if kind:
        out = [r for r in out if r.kind == kind]
    if tier:
        out = [r for r in out if r.tier == tier]
    if exactness:
        out = [r for r in out if r.exactness == exactness]
    if path:
        out = [r for r in out if r.path and path in r.path]
    if not include_archive and tier != "archive":
        out = [r for r in out if r.tier != "archive"]
    return out


# ---------------------------------------------------------------------------
# Coverage — the C7 acceptance gate.
# ---------------------------------------------------------------------------
def test_files() -> list[str]:
    """Every test file on disk, repo-relative."""
    out: list[str] = []
    for d in TEST_DIRS:
        full = os.path.join(_REPO, d)
        if not os.path.isdir(full):
            continue
        for fn in sorted(os.listdir(full)):
            if fn.endswith(".py") and fn not in _NOT_A_TEST:
                out.append(f"{d}/{fn}")
    return sorted(out)


def unregistered_files() -> list[str]:
    claimed = {r.path for r in all_records() if r.path}
    return [p for p in test_files() if p not in claimed]


def check_coverage() -> list[str]:
    """Alias for the gate script. ``()`` means every test file has a record."""
    return unregistered_files()


def counts() -> dict[str, int]:
    """The numbers the C7 ratchet tracks."""
    recs = all_records()
    return {
        "records": len(recs),
        "files": len(test_files()),
        "unregistered": len(unregistered_files()),
        "legacy_script": sum(1 for r in recs if r.kind == "legacy_script"),
        "assertion": sum(1 for r in recs if r.kind == "assertion"),
        "result_dump": sum(1 for r in recs if r.kind == "result_dump"),
        "scenario": sum(1 for r in recs if r.kind == "scenario"),
        "archive": sum(1 for r in recs if r.tier == "archive"),
        "gate": sum(1 for r in recs if r.tier == "gate"),
        # The P1 number, restated over the registry: a MIGRATED record with no
        # failure mode is a validation error, so this can only ever count
        # legacy_script records. It is the debt, named.
        "no_failure_mode": sum(1 for r in recs if not r.has_failure_mode),
        # Baseline provenance (supersessions.yaml `baselines:`, 2026-07-31).
        # `stale_baselines` are decided; `candidate_baselines` are a triage queue
        # that still fails, so it belongs next to the debt count, not hidden.
        "stale_baselines": len(_ledger_counts()[0]),
        "candidate_baselines": len(_ledger_counts()[1]),
        # Gap #3 / row H2. The one number the 2026-08-07 report could not print:
        # how many gate-tier assertions declare a perturbation that must redden
        # them. `gate_assertion_no_control` is the ratcheted one, and it is a
        # count of records, not of controls, so adding a fifth control to a
        # record that already had four does not move it.
        "needs_control": sum(1 for r in recs if r.needs_control),
        "gate_assertion_no_control": sum(1 for r in recs if r.needs_control
                                         and not r.has_control),
        "control_strong": sum(1 for r in recs
                              if r.control_strength == "strong"),
        "control_weak": sum(1 for r in recs if r.control_strength == "weak"),
        "controls_declared": sum(len(r.control) for r in recs),
    }


def _ledger_counts() -> tuple[list, list]:
    try:
        from . import ledger
        return ledger.stale_by_design(), ledger.candidates()
    except Exception:                                    # pragma: no cover
        return [], []


# ---------------------------------------------------------------------------
def parse_param(spec: str) -> tuple[str, Any]:
    """``delta_star=2/9`` -> ``("delta_star", Fraction(2, 9))``.

    Rationals stay exact, ints stay ints, floats parse, ``true``/``false``/
    ``null`` map to Python, and anything else is a string.
    """
    if "=" not in spec:
        raise ValueError(f"--param needs k=v, got {spec!r}")
    k, v = spec.split("=", 1)
    k, v = k.strip(), v.strip()
    low = v.lower()
    if low in ("true", "false"):
        return k, low == "true"
    if low in ("none", "null"):
        return k, None
    if re.fullmatch(r"-?\d+/\d+", v):
        return k, Fraction(v)
    try:
        return k, int(v)
    except ValueError:
        pass
    try:
        return k, float(v)
    except ValueError:
        return k, v


def with_params(rec: TestRecord, overrides: dict[str, Any]) -> TestRecord:
    """A copy of `rec` at a different point in parameter space (C7.2 `--param`)."""
    merged = dict(rec.params)
    merged.update(overrides)
    return replace(rec, params=merged)
