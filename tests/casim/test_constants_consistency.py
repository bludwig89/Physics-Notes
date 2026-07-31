"""Roadmap C2.4 — the constants gate, with its polarity flipped.

P0.2 asked *"does every recorded site still agree with the registry?"*  That
was the right question while decision D2 kept the flat kernels authoritative.
C2's decision **D7** makes `casim.constants` the source of truth, so this file
now asks the stronger one:

    **Does any unregistered site exist at all?**

The difference is not cosmetic.  Under P0, adding a 75th independent definition
of ``c_lat`` passed as long as it agreed to 1e-9 — provenance was satisfied and
the sprawl was untouched.  Under C2 it fails, and the fix is to import the
constant.  The 12 sites P0 recorded as *unenforceable* (re-exports, function
default arguments like ``gap_solve(..., Lam3=0.347)``, runtime-computed values)
become enforceable for exactly this reason: the pattern they hid behind is what
disappears when the value comes from an import.

The sweep engine lives in `tools/audit_constants.py` so that this gate and the
`--ratchet` CI counter cannot diverge — the same reason C7 makes pytest
delegate to the test registry rather than reimplement it.

Everything works by **AST inspection, never import**.  Importing a
`ca-simulation` kernel is mostly harmless; importing a `tests/findings` module
executes its physics and writes JSON, so a provenance check that imported its
subjects would be slow and destructive.

Scope: `src/` and `ca-simulation/` are the C2 gate and must be at zero.
`tests/` is the C7 backlog — counted, ratcheted, not yet enforced, because a
test registry that pointed at pre-migration paths would have to be rewritten.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction


class _StandaloneSkip(Exception):
    """Raised by the pytest shim's skip(); caught by the standalone runner."""


try:
    import pytest
except ModuleNotFoundError:                                # pragma: no cover
    # Minimal shim so the gate still runs where pytest is not installed.
    class _NoOpMark:
        """`@pytest.mark.x` and `@pytest.mark.x(...)` both become identity."""
        def __getattr__(self, _name):
            def _apply(*args, **kwargs):
                if len(args) == 1 and callable(args[0]) and not kwargs:
                    return args[0]                  # used bare: @mark.exact
                return lambda fn: fn                # used with args
            return _apply

    class _Approx:
        def __init__(self, expected, rel=0.0, abs=0.0):
            self.expected, self.rel, self.abs = expected, rel or 0.0, abs or 0.0

        def __eq__(self, other):
            delta = self.expected - other
            return (delta if delta >= 0 else -delta) <= max(
                self.abs, self.rel * (self.expected if self.expected >= 0
                                      else -self.expected))

    class _Raises:
        """Context manager standing in for `pytest.raises(Exc)`."""
        def __init__(self, expected):
            self.expected = expected

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            if exc_type is None:
                raise AssertionError(
                    f"DID NOT RAISE {self.expected!r}")
            return issubclass(exc_type, self.expected)  # swallow the expected one

    class _PytestShim:
        mark = _NoOpMark()

        @staticmethod
        def approx(expected, rel=0.0, abs=0.0):
            return _Approx(expected, rel, abs)

        @staticmethod
        def skip(msg=""):
            raise _StandaloneSkip(msg)

        @staticmethod
        def raises(expected):
            return _Raises(expected)

    pytest = _PytestShim()                                 # type: ignore[assignment]

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
for _p in (os.path.join(_REPO, "src"), os.path.join(_REPO, "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import audit_constants as AC                                # noqa: E402
from casim.constants import (                               # noqa: E402
    EXACTNESS_CLASSES, SECTORS, SITE_KINDS, MEASURED_KINDS,
    all_constants, all_measured, get, sweepable_constants, endpoint, bracket,
)


# ---------------------------------------------------------------------------
# Registry integrity
# ---------------------------------------------------------------------------
@pytest.mark.exact
def test_registry_is_well_formed():
    cs = all_constants()
    assert cs, "the constants registry is empty"
    for c in cs:
        assert c.provenance, f"{c.symbol}: no provenance finding recorded"
        assert c.exactness in EXACTNESS_CLASSES, f"{c.symbol}: bad exactness class"
        assert c.sector in SECTORS, f"{c.symbol}: bad sector"
        assert c.derivation.strip(), f"{c.symbol}: no derivation recorded"
        for s in c.sites:
            assert s.kind in SITE_KINDS, f"{c.symbol} -> {s.path}: bad site kind"
        if c.bracket is not None:
            lo, hi = c.bracket
            assert lo < hi, f"{c.symbol}: degenerate bracket"
            assert c.value is None, f"{c.symbol}: has both a value and a bracket"


@pytest.mark.exact
def test_sweep_exclusions_are_justified():
    """C2.4: opting a constant out of the sweep is a judgement, so write it down.

    Also checks the judgement is the RIGHT one — a constant excluded from the
    sweep should be one whose value is too common to be diagnostic.  Excluding
    a distinctive value would quietly re-open the hole C2 closed.
    """
    for c in all_constants():
        if c.sweep:
            continue
        assert c.sweep_reason.strip(), f"{c.symbol}: sweep=False with no reason"
        assert not c.is_diagnostic, (
            f"{c.symbol} = {c.float_value!r} is a distinctive value but is "
            f"excluded from the sweep. Only undiagnostic values may be "
            f"excluded: small integers, and 1/4, 1/2, 3/4, 3/2, 5/2.")


@pytest.mark.exact
def test_every_measured_record_is_honest():
    """C2.3: the typed replacement for P0's ALLOWLIST must stay typed."""
    for m in all_measured():
        assert m.kind in MEASURED_KINDS, f"{m.path}: bad MeasuredConstant kind"
        assert m.reason.strip(), f"{m.path}: no reason"
        get(m.compares_to)                       # raises if the symbol is gone
        assert os.path.exists(os.path.join(_REPO, m.path)), \
            f"MeasuredConstant cites a path that does not exist: {m.path}"


@pytest.mark.exact
def test_every_recorded_site_exists():
    """A stale path in the registry is a provenance record that lies."""
    missing = [
        f"{c.symbol} -> {s.path}"
        for c in all_constants() for s in c.sites
        if not os.path.exists(os.path.join(_REPO, s.path))
    ]
    assert not missing, "registry cites paths that do not exist:\n  " + \
                        "\n  ".join(missing)


@pytest.mark.exact
def test_exact_constants_resolve_from_closed_form():
    """C2.1: an `exact` constant may not be a typed-in decimal.

    Spot-checks the five the roadmap names. Each is recomputed here from its
    closed form; if the registry ever swaps one for a truncated literal, this
    catches it. The a/ell_P case is the reason the rule exists: the tree
    carried it at three precisions and the 5-sf copy was 3.4e-6 off.
    """
    import math
    assert get("a_over_ellP").value == math.sqrt(8.0 * math.pi) * 3.0 ** 0.25
    assert get("c_lat").value == 1.0 / math.sqrt(3.0)
    assert get("G_LATTICE").value == 1.0 / (72.0 * math.pi)
    assert get("delta_star").value == Fraction(2, 9)
    assert get("W_star").value == pytest.approx(6 * get("lambda_6").float_value,
                                                rel=1e-12)


@pytest.mark.exact
def test_rational_constants_are_exact_objects():
    """C2.1: a Fraction-valued constant exposes the exact object AND a float.

    Tests that assert exactness must be able to reach the Fraction; array code
    must be able to reach the float without calling float() at every site.
    """
    import casim.constants as K
    for c in all_constants():
        if not isinstance(c.value, Fraction):
            continue
        assert getattr(K, c.symbol) == c.value, \
            f"{c.symbol} is not exported as its exact Fraction"
        assert getattr(K, c.symbol + "_f") == float(c.value), \
            f"{c.symbol}_f missing or wrong"
    # The specific comparison the lepton canon depends on.
    assert K.delta_star == Fraction(2, 9)
    assert 3 * K.delta_star == Fraction(2, 3)          # exact, not 0.6666...


@pytest.mark.exact
def test_bracketed_constants_have_no_scalar_surface():
    """C2.2: `alpha_eff_star` is a range, and the range IS the result.

    The frequently-quoted 0.39 is the midpoint of two SCALE CHOICES, not an
    independently determined number. Making a caller name an endpoint is the
    correct friction; exporting a scalar would launder the range into a result.
    """
    import casim.constants as K
    for c in all_constants():
        if c.bracket is None:
            continue
        assert not hasattr(K, c.symbol), (
            f"{c.symbol} is bracketed but is exported as a scalar; that is "
            f"exactly the laundering C2.2 forbids")
    lo, hi = bracket("alpha_eff_star")
    assert endpoint("alpha_eff_star", "lo") == lo
    assert endpoint("alpha_eff_star", "hi") == hi
    assert lo < hi


@pytest.mark.exact
def test_the_three_hard_cases_stay_separate():
    """C2.2: constants that legitimately disagree are not reconciled.

    f_pi is three constants, sin^2 theta_W is two, cos 3delta* is two. And C2.4
    found a third 2/9 (the NJL colour-Fierz coefficient) and a second 0.733
    (the q* matching scale), both now registered rather than absorbed.
    """
    fpi = {get(s).float_value for s in ("f_pi_anchor_MeV",
                                        "f_pi_pdg_target_MeV",
                                        "f_pi_gamma_convention_MeV")}
    assert len(fpi) == 3, "the three f_pi values have been collapsed"

    assert get("sin2_thetaW_uv").value != get("sin2_thetaW_onshell").value

    d = abs(get("cos3_delta_star").float_value - get("cos3_delta_data").float_value)
    assert 1e-6 < d < 1e-4, (
        f"cos3delta* and its data value differ by {d:.2e}; the ~1.7e-5 gap IS "
        f"the F256 near-coincidence and collapsing it erases the caveat")

    # Three unrelated 2/9s.
    two_ninths = {c.symbol for c in all_constants()
                  if c.value is not None and abs(float(c.value) - 2 / 9) < 1e-15}
    assert two_ninths == {"delta_star", "sin2_thetaW_onshell", "c_fierz_colour"}, (
        f"expected exactly three registered 2/9s in three sectors, got "
        f"{sorted(two_ninths)}")
    assert len({get(s).sector for s in two_ninths}) == 3


# ---------------------------------------------------------------------------
# The gate: no unregistered site exists
# ---------------------------------------------------------------------------
@pytest.mark.exact
def test_no_unregistered_literals_in_src_or_kernels():
    """C2.4, the headline. This is the assertion whose polarity flipped.

    A failure here means a value matching a registry constant is written out
    somewhere in `src/` or `ca-simulation/` without saying which constant it
    is. Three fixes, in order of preference:

      1. import it from `casim.constants` (almost always the right answer);
      2. if the site legitimately computes a DIFFERENT number for the same
         quantity — a 2-D lattice, the cubic fork — add a MeasuredConstant with
         kind='measured' and a reason;
      3. if it is a different quantity that happens to share the value — and
         this model has several, three separate 2/9s among them — add a
         MeasuredConstant with kind='coincidence' and a reason.

    Widening a tolerance is not on the list.
    """
    rogues = AC.scan(AC.GATE_ROOTS, "gate")
    assert not rogues, (
        f"{len(rogues)} unregistered literal(s) matching a registry constant:\n  "
        + "\n  ".join(str(r) for r in rogues[:40])
        + ("\n  ..." if len(rogues) > 40 else "")
        + "\n\nSee the docstring of this test for the three ways to fix it.")


@pytest.mark.exact
def test_declared_import_sites_really_import():
    """A Site claiming kind='import' must actually import the constant.

    Otherwise the registry describes a migration that never happened, which is
    the same class of lie as a stale path — one level up.
    """
    bad = AC.unverified_import_sites()
    assert not bad, "registry claims imports that are not there:\n  " + \
                    "\n  ".join(bad)


@pytest.mark.exact
def test_literal_sites_are_confined_to_tests():
    """The C2 ratchet's target state: no `literal` site left outside tests/.

    Every remaining one is a test file, and C7 drains them when the test
    registry lands. This assertion is what stops them coming back into `src/`.
    """
    stragglers = [f"{c.symbol} -> {s.path}"
                  for c in all_constants() for s in c.sites
                  if s.kind == "literal" and not s.path.startswith("tests/")]
    assert not stragglers, (
        "sites in src/ or ca-simulation/ still declare their own value:\n  "
        + "\n  ".join(stragglers))


@pytest.mark.exact
def test_backlog_is_reported_not_ignored():
    """tests/ is C7's problem, but the number is visible and ratcheted."""
    backlog = AC.scan(AC.BACKLOG_ROOTS, "backlog")
    lits = AC.literal_site_count()
    print(f"\n[constants] {len(all_constants())} registered, "
          f"{len(sweepable_constants())} sweepable, "
          f"{len(all_measured())} MeasuredConstant records")
    print(f"[constants] C7 backlog: {len(backlog)} unregistered literals in "
          f"tests/, {sum(lits.values())} recorded literal sites")
    assert isinstance(backlog, list)


# ---------------------------------------------------------------------------
# Standalone runner — the gate must not depend on pytest being installed.
#
# `casim test` classifies a file as a script when it has no `def test_`, and
# silently SKIPS pytest-style files when pytest is missing (runner.py:365-368).
# A provenance gate that can vanish that quietly is not a gate, so this file
# runs both ways.
# ---------------------------------------------------------------------------
def _run_standalone() -> int:
    checks = [(n, f) for n, f in sorted(globals().items())
              if n.startswith("test_") and callable(f)]
    failures, skipped, ran = [], 0, 0

    def _skip(msg=""):
        raise _StandaloneSkip(msg)

    real_skip = pytest.skip
    pytest.skip = _skip                                    # type: ignore[assignment]
    try:
        for label, fn in checks:
            try:
                fn()
                ran += 1
            except _StandaloneSkip as e:
                skipped += 1
                print(f"SKIP  {label}: {e}")
            except AssertionError as e:
                failures.append(f"{label}: {e}")
                print(f"FAIL  {label}")
    finally:
        pytest.skip = real_skip                            # type: ignore[assignment]

    print(f"\n[constants] {ran} PASS, {skipped} skipped, {len(failures)} FAIL")
    for f in failures:
        print(f"\n--- FAIL {f}")
    return 1 if failures else 0


if __name__ == "__main__":                                 # pragma: no cover
    sys.exit(_run_standalone())
