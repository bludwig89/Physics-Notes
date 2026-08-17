"""The negative-control machinery, and a negative control for it (D9, row H2).

Registry record: `control-soundness` (gate tier). Machinery lives in
`casim.tests.registry` (the `control:` schema) and `casim.tests.runner`
(`run_control`, `leg_map`, `record_fingerprint`).

Why this file exists
--------------------
Gap #3 of `docs/status/completeness-2026-08-07.md` asks for a mechanism that
refuses a check which cannot go red. Shipping that mechanism without a
demonstration that *it* can go red would reproduce the defect one level up — and
this repo has already been burned by exactly that shape twice in one week: F22's
identity check was a tautology for months, and F298–F303 claimed gate records
with declared controls while the tree held four `legacy_script` stubs, both times
with every check green.

So the load-bearing test here is :func:`test_a_noop_perturbation_is_reported_as_leak`.
``_synthetic_check`` accepts a switch that changes **nothing**. A checker that
scored that sound would be worthless, and nothing else in this file would notice.

The rest of the cases pin the vocabulary apart. LEAK, SPILL and INVALID are three
different failures and collapsing any pair of them would let the easy one absorb
the hard one — which is the A10 over-grade this very report had to correct by
hand ("a row graded on its easier half").
"""
from __future__ import annotations

import pytest

from casim.tests import registry as treg
from casim.tests import runner as trunner


# ---------------------------------------------------------------------------
# The synthetic driver. Three switches: one that reddens the declared leg, one
# that reddens nothing, one that reddens everything. Underscore-prefixed so
# pytest does not collect it as a test.
# ---------------------------------------------------------------------------
def _synthetic_check(real_control: bool = False, noop_control: bool = False,
                     global_control: bool = False) -> dict:
    checks = [
        {"id": "S1", "pass": not global_control},
        {"id": "S2", "pass": not (real_control or global_control)},
    ]
    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "all_pass": n_pass == len(checks)}


def _rec(control: list[dict]) -> treg.TestRecord:
    """A record whose entry point is `_synthetic_check` in this very file."""
    return treg.TestRecord(
        id="synthetic-control-probe",
        kind="assertion",
        sector="suite",
        tier="battery",
        path="tests/casim/test_control_soundness.py",
        entry="_synthetic_check",
        control=treg.normalise_controls(control),
        evidence={"pytest_funcs": True},
    )


def _verdicts(control: list[dict]) -> list[trunner.RunResult]:
    return trunner.run_control(_rec(control), timeout=60.0)


# ---------------------------------------------------------------------------
# the one that matters
# ---------------------------------------------------------------------------
def test_a_noop_perturbation_is_reported_as_leak():
    """THE self-control. A switch that changes nothing must not read as sound.

    If this test is the only one in the file that fails, the soundness checker
    is decorative and every CONTROL verdict in the journal is worthless.
    """
    res, = _verdicts([{"params": {"noop_control": True}, "reds": ["S2"],
                       "reason": "deliberately inert — the checker must catch "
                                 "that this proves nothing"}])
    assert res.status == "LEAK", (res.status, res.detail)
    assert "S2" in res.detail


def test_a_real_perturbation_is_reported_as_control():
    res, = _verdicts([{"params": {"real_control": True}, "reds": ["S2"],
                       "reason": "reddens exactly S2"}])
    assert res.status == "CONTROL", (res.status, res.detail)
    assert res.ok


def test_reddening_undeclared_legs_is_a_spill_not_a_pass():
    """'And only where declared' — the clause ten records already claim in prose.

    A perturbation that breaks the whole run is a broken run, and it is also the
    cheapest way to make a control look green.
    """
    res, = _verdicts([{"params": {"global_control": True}, "reds": ["S2"],
                       "reason": "reddens S1 too, which it does not declare"}])
    assert res.status == "SPILL", (res.status, res.detail)
    assert not res.ok
    assert "S1" in res.detail


def test_only_false_accepts_a_deliberately_global_perturbation():
    res, = _verdicts([{"params": {"global_control": True}, "reds": ["S2"],
                       "only": False,
                       "reason": "global on purpose, declared as such"}])
    assert res.status == "CONTROL", (res.status, res.detail)


def test_a_leg_that_stays_green_is_a_leak_even_when_others_go_red():
    """Attribution, not accounting: the run went red, but not where declared."""
    res, = _verdicts([{"params": {"real_control": True}, "reds": ["S1"],
                       "reason": "misattributed — S1 is not what this reddens"}])
    assert res.status == "LEAK", (res.status, res.detail)


def test_an_unaccepted_parameter_is_invalid_not_a_leak():
    """`_call` drops unknown keywords on purpose, so this would be a silent no-op.

    Reporting it as LEAK would blame the physics for a typo in the control.
    """
    res, = _verdicts([{"params": {"no_such_switch": True}, "reds": ["S2"],
                       "reason": "the entry point does not take this"}])
    assert res.status == "INVALID", (res.status, res.detail)
    assert "no_such_switch" in res.detail


def test_a_leg_that_does_not_exist_is_invalid():
    """A control naming a leg the driver stopped emitting has stopped testing."""
    res, = _verdicts([{"params": {"real_control": True}, "reds": ["S99"],
                       "reason": "names a leg that is not in the payload"}])
    assert res.status == "INVALID", (res.status, res.detail)
    assert "S99" in res.detail


def test_no_control_declared_is_noctrl_and_does_not_wall_the_gate():
    res, = trunner.run_control(_rec([]), timeout=60.0)
    assert res.status == "NOCTRL"
    assert res.ok, "debt must not turn the gate red; the ratchet drives it down"


# ---------------------------------------------------------------------------
# leg extraction — three payload shapes are in use in this repo
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("payload,expected", [
    ({"checks": [{"id": "A", "pass": True}, {"id": "B", "pass": False}]},
     {"A": True, "B": False}),
    ({"checks": {"symbolic_identity": True, "numeric_identity": False}},
     {"symbolic_identity": True, "numeric_identity": False}),
    ({"checks": [{"name": "A", "ok": False}]}, {"A": False}),
    ({"n_pass": 3}, {}),
    ("not a dict", {}),
])
def test_leg_map_reads_every_shape_in_use(payload, expected):
    assert trunner.leg_map(payload) == expected


# ---------------------------------------------------------------------------
# leg-tag resolution — half the drivers emit "tag + description" as one key
# ---------------------------------------------------------------------------
def test_a_tag_resolves_against_a_tag_plus_description_key():
    legs = {"L1 C_2(fund) = (N^2-1)/2N": True,
            "L2 the C7 identity exists ONLY for N <= 3": True}
    hit, why = trunner.resolve_leg("L2", legs)
    assert hit == "L2 the C7 identity exists ONLY for N <= 3"
    assert why == ""


def test_a_tag_does_not_swallow_a_longer_sibling_tag():
    """S4 and S4b are different legs in F299, each declared by its own control."""
    legs = {"S4 casimir ratio at weak coupling": True,
            "S4b bijection at N=3": True}
    hit, _ = trunner.resolve_leg("S4", legs)
    assert hit == "S4 casimir ratio at weak coupling"
    hit_b, _ = trunner.resolve_leg("S4b", legs)
    assert hit_b == "S4b bijection at N=3"


def test_an_ambiguous_tag_is_reported_not_guessed():
    """Picking one of two would be the checker inventing what it audits."""
    legs = {"N1 first": True, "N1 second": True}
    hit, why = trunner.resolve_leg("N1", legs)
    assert hit is None and "ambiguous" in why


def test_an_unmatched_tag_resolves_to_nothing():
    hit, why = trunner.resolve_leg("Z9", {"A1 x": True})
    assert hit is None and why == ""


# ---------------------------------------------------------------------------
# can-fail, measured by execution rather than inferred from the AST
#
# The three probes below are the three answers a gate entry can give, and the
# first one is the one the AST walk got wrong on three real records.
# ---------------------------------------------------------------------------
def _guarded_leg():
    assert 1 + 1 == 2          # a real assert line, reached only via the table
    return True


_PROBE_CHECKS = (("P1", _guarded_leg),)


def _dispatch_entry():
    """Asserts, but only through a dispatch table, and declares no verdict key."""
    out = {}
    for name, fn in _PROBE_CHECKS:
        out[name] = fn()
    return out


def _naked_entry():
    """No assert, no raise, no verdict key. The genuine cannot-fail shape."""
    return {"measurement": 1.234, "verdict": "a paragraph of English"}


def _probe(entry: str) -> dict:
    return trunner.probe_can_fail(
        treg.TestRecord(id=f"probe-{entry}", kind="assertion", sector="suite",
                        tier="gate", path="tests/casim/test_control_soundness.py",
                        entry=entry, evidence={"pytest_funcs": True}),
        timeout=30.0)


def test_a_guard_reached_only_through_a_dispatch_table_is_seen():
    """THE regression. `for name, fn in CHECKS: fn()` defeated the AST walk.

    F282, F291 and F292 were reported cannot-fail on that basis while holding
    41, 39 and 30 reachable asserts. Execution does not care about indirection.
    """
    r = _probe("_dispatch_entry")
    assert r["verdict"] == "CAN_FAIL", r
    assert r["route"] == "guard", r
    assert r["guards_executed"] >= 1


def test_a_verdict_key_counts_as_a_failure_route():
    """F300 asserts nothing and returns `all_pass`; tracing alone called it
    cannot-fail, which is the AST mistake mirrored."""
    r = _probe("_synthetic_check")
    assert r["verdict"] == "CAN_FAIL", r
    assert r["route"] == "verdict_key", r
    assert r["guards_executed"] == 0


def test_measurements_and_a_paragraph_are_not_a_failure_mode():
    r = _probe("_naked_entry")
    assert r["verdict"] == "CANNOT_FAIL", r
    assert r["can_fail"] is False
    assert r["route"] is None


def test_a_timeout_is_inconclusive_and_never_cannot_fail():
    """Absence of evidence recorded as evidence of absence is the original defect."""
    r = trunner.probe_can_fail(
        treg.TestRecord(id="probe-slow", kind="assertion", sector="suite",
                        tier="gate", path="tests/casim/test_control_soundness.py",
                        entry="_slow_naked_entry"),
        timeout=0.05)
    assert r["verdict"] == "INCONCLUSIVE", r
    assert r["can_fail"] is None, "None, not False — nothing was established"
    assert "NOT cannot-fail" in r["detail"]


def _slow_naked_entry():
    """Burns time in THIS file so the tracer is active, and never guards."""
    total = 0.0
    for i in range(400000):
        total += i * 0.5
        total -= i * 0.5
    return {"total": total}


# ---------------------------------------------------------------------------
# schema validation
# ---------------------------------------------------------------------------
def test_a_control_without_a_reason_is_rejected():
    errs = treg._validate_controls(_rec([{"params": {"real_control": True}}]))
    assert any("reason" in e for e in errs), errs


def test_a_control_with_neither_params_nor_test_is_rejected():
    errs = treg._validate_controls(_rec([{"reason": "empty"}]))
    assert any("params" in e for e in errs), errs


def test_an_unknown_control_key_is_rejected():
    errs = treg._validate_controls(
        _rec([{"params": {"real_control": True}, "reason": "x", "redz": ["S2"]}]))
    assert any("redz" in e for e in errs), errs


def test_params_on_a_record_with_no_entry_is_rejected():
    """The override would be dropped, so the control would pass by inaction."""
    rec = treg.TestRecord(id="x", kind="assertion", sector="suite", tier="gate",
                          path="tests/casim/test_control_soundness.py",
                          control=treg.normalise_controls(
                              [{"params": {"a": 1}, "reason": "y"}]))
    errs = treg._validate_controls(rec)
    assert any("entry" in e for e in errs), errs


def test_control_params_keep_exact_rationals():
    """A perturbation of an exact constant must stay a Fraction, not become str.

    Otherwise the run goes red because the type changed, not because the value
    did — a red for the wrong reason still scores as a sound control.
    """
    from fractions import Fraction
    (c,) = treg.normalise_controls([{"params": {"delta_star": "2/9"},
                                     "reason": "z"}])
    assert c["params"]["delta_star"] == Fraction(2, 9)


# ---------------------------------------------------------------------------
# the D9 requirement and its scope
# ---------------------------------------------------------------------------
def test_the_requirement_is_scoped_to_gate_tier_assertions():
    for kind, tier, want in [("assertion", "gate", True),
                             ("assertion", "battery", False),
                             ("result_dump", "gate", False),
                             ("scenario", "gate", False),
                             ("legacy_script", "gate", False)]:
        rec = treg.TestRecord(id="x", kind=kind, sector="suite", tier=tier)
        assert rec.needs_control is want, (kind, tier)


def test_strength_separates_harness_applied_from_in_file_controls():
    assert _rec([]).control_strength == "none"
    assert _rec([{"params": {"real_control": True},
                  "reason": "r"}]).control_strength == "strong"
    assert _rec([{"test": "test_x", "reason": "r"}]).control_strength == "weak"


def test_the_fingerprint_moves_when_the_control_changes():
    """What arms the gate's static check: a verdict names the code it measured.

    Same bargain a `result_dump` record makes by committing its baseline.
    """
    a = trunner.record_fingerprint(
        _rec([{"params": {"real_control": True}, "reason": "r"}]))
    b = trunner.record_fingerprint(
        _rec([{"params": {"real_control": True}, "reason": "r"},
              {"params": {"global_control": True}, "only": False,
               "reason": "r2"}]))
    assert a != b
    assert a == trunner.record_fingerprint(
        _rec([{"params": {"real_control": True}, "reason": "r"}]))


def test_every_declared_control_in_the_registry_is_well_formed():
    """The live registry, not a fixture. This is the gate's static half."""
    errs: list[str] = []
    for r in treg.all_records():
        if r.control:
            errs += [f"{r.id}: {e}" for e in treg._validate_controls(r)]
    assert not errs, errs


def test_the_journal_carries_verdicts_for_records_outside_the_selection(tmp_path):
    """Slicing is forced by the 45 s ceiling, so a slice must not erase the rest.

    Caught by running this pass for real: `--id F298,F303` then `--id F300` left
    a journal holding only F300, so the gate would have demanded a re-verify of
    everything but the last slice — a resumable pass that never finishes.
    """
    j = str(tmp_path / "j.json")
    good = [{"params": {"real_control": True}, "reds": ["S2"], "reason": "r"}]
    a = _rec(good)
    b = treg.replace(a, id="synthetic-control-probe-2")
    trunner.control_selection([a], journal=j, timeout=60.0)
    trunner.control_selection([b], journal=j, timeout=60.0)
    import json
    ids = {str(i["id"]).split("#")[0]
           for i in json.load(open(j))["items"]}
    assert ids == {a.id, b.id}, ids


def test_the_debt_count_is_a_count_of_records_not_of_controls():
    c = treg.counts()
    assert c["gate_assertion_no_control"] <= c["needs_control"]
    assert (c["control_strong"] + c["control_weak"]
            >= c["needs_control"] - c["gate_assertion_no_control"])


def test_the_debt_is_actually_ratcheted():
    """The wiring, not the number. A counter nothing enforces is a report.

    That distinction is the entire content of gap #3: the H2 norm was written in
    ten findings' `notes:` and propagated to every new session, and the three
    instrument counts came back bit-identical across three days because no
    mechanism read them.
    """
    import json
    import os
    import sys
    repo = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    sys.path.insert(0, os.path.join(repo, "tools"))
    import audit_tests

    assert "gate_assertion_no_control" in audit_tests._RATCHET_KEYS
    with open(os.path.join(repo, "tools", "test_health_baseline.json"),
              encoding="utf-8") as fh:
        base = json.load(fh)
    assert "gate_assertion_no_control" in base, (
        "the key is ratcheted but never baselined, so it can only ever be "
        "compared against the 1e9 default — i.e. never fail")
    assert (treg.counts()["gate_assertion_no_control"]
            <= base["gate_assertion_no_control"]), (
        "more gate-tier assertions now lack a declared control than the "
        "recorded high-water mark; declare one or `make control-todo`")
