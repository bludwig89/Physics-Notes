"""casim.constants — the single **source of truth** for the model's constants.

Roadmap C2 (`docs/roadmaps/roadmap-casim-consolidation.md`), decision **D7**.

**This module owns values.**  Roadmap decision D7 reverses D2: where P0 built a
registry that only *described* what the flat ``ca-simulation/ca_*.py`` kernels
declared, C2 makes the registry authoritative.  Physics modules now write

    from casim.constants import c_lat, G_LATTICE, delta_star

and the literal is deleted.  ~74 independent definitions of ``c_lat`` was never
a provenance problem; it was a source-of-truth problem, and P0.2's consistency
test has flipped polarity to match: from *"every recorded site agrees"* to
*"no unregistered site exists"* (C2.4).

For every constant the registry still records the four things a bare literal
never could:

  1. which finding(s) fixed it,
  2. what exactness class it belongs to,
  3. how it is derived (or that it is an external anchor),
  4. every place in the tree that binds it — and, per C2, *how* it binds it.

Exact constants resolve from **closed form, never a decimal** (C2.1):
``a/ell_P = sqrt(8 pi) 3^(1/4)``, ``c_lat = 1/sqrt(3)``, ``delta* = 2/9`` as a
``Fraction``, ``G_LATTICE = 1/(72 pi)``, ``W = 6 lambda_6``.  A ``Fraction``-
valued constant exposes both the exact object (under its own symbol) and a
float (under ``<symbol>_f``); a test asserting exactness must use the former.

Constants that legitimately disagree stay **separate constants** with distinct
symbols, never reconciled into one contested number (C2.2).  So ``f_pi`` is
three entries (the 92.07 model anchor, the 92.4 PDG comparison target, the
92.28 Gamma-convention value), ``sin^2 theta_W`` is two (the F45 UV 1/4 and the
F49 on-shell 2/9, reconciled by F231), ``cos 3delta*`` is two (the derived
cos(2/3) and the empirical F93-O7 value, 1.7e-5 apart — that gap *is* the F256
near-coincidence), and ``alpha_eff_star`` is a **bracket with no scalar value**.
Papering over any of those would turn a prediction into an input.

Site kinds (C2)
---------------
A ``Site`` now declares *how* a path binds the constant:

  ``import``   — imports it from this registry.  The target state.  The
                 consistency test asserts the import really is there and that
                 no local literal shadows it.
  ``literal``  — still defines its own value.  Legacy; the C2 ratchet
                 (``tools/audit_constants.py --ratchet``) drives this to zero.
  ``reexport`` — re-exports another module's binding; nothing here can drift.
  ``runtime``  — computed at run time (a fit, a dispersion measurement, a
                 config default).  Recorded for provenance, not checkable
                 statically.

The ``@measured`` escape hatch (C2.3)
-------------------------------------
Some modules must *compute* a number that looks like a registry constant,
because the derivation is the physics under test — ``derive_velocity_addition``
at 1/sqrt(2) on the 2-D square lattice, ``forks/curl_fork_cubic`` at 1.0 on the
simple-cubic fork, every ``c_lat`` that emerges from a dispersion fit.  Those
are ``MeasuredConstant`` records: **enumerated and reasoned, not allowlisted by
regex.**  P0's ALLOWLIST dict becomes a typed declaration.

Usage
-----
    from casim.constants import c_lat, G_LATTICE, delta_star
    from casim.constants import get, value, all_constants

    get("c_lat").provenance        # ('F26',)
    value("G_LATTICE")             # 0.004420970641441537
    float(delta_star)              # 0.2222222222222222
    delta_star == Fraction(2, 9)   # True — exact, not a float compare
    [c.symbol for c in all_constants(sector="lepton")]
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable

__all__ = [
    "Constant", "Site", "MeasuredConstant",
    "EXACTNESS_CLASSES", "SECTORS", "SITE_KINDS", "MEASURED_KINDS",
    "register", "register_measured",
    "get", "value", "exact", "all_constants", "by_finding", "sites_for",
    "all_measured", "measured_at", "sweepable_constants",
]

# ---------------------------------------------------------------------------
# Exactness classes — the same vocabulary as the pytest markers and
# docs/status/exactness-inventory.md.  Do not invent new ones here without
# updating both.  C8.4 depends on this set being closed.
# ---------------------------------------------------------------------------
EXACTNESS_CLASSES = {
    "exact":        "closed form; algebraically exact, residual == 0",
    "machine":      "holds to the float/FFT round-off floor (<1e-12)",
    "quantitative": "a computed number with a declared tolerance",
    "bracketed":    "known only within a range; the range IS the result",
    "external":     "measured input from outside the model (CODATA/PDG/FLAG)",
}

SECTORS = ("geometry", "gravity", "lepton", "strong", "electroweak")

# How a recorded path binds the constant.  See the module docstring.
SITE_KINDS = {
    "import":   "imports the value from casim.constants — the C2 target state",
    "literal":  "still defines its own value; legacy, driven to zero by the ratchet",
    "reexport": "re-exports another module's binding; nothing here can drift",
    "runtime":  "computed at run time (fit, dispersion measurement, config default)",
}

# The two honest ways a site can hold a number that matches a registry value.
MEASURED_KINDS = {
    "measured":    "the same quantity in a regime where the answer differs",
    "coincidence": "a different quantity that happens to equal the same number",
}

_REGISTRY: dict[str, "Constant"] = {}
_MEASURED: list["MeasuredConstant"] = []

# Values too common to sweep for.  A literal 1.0, 6.0 or 0.5 anywhere in the
# tree is a loop bound, a dimension or a lattice size far more often than it is
# a physical constant, so finding one is not evidence.  A constant whose value
# lands here must declare sweep=False with a reason.
_UNDIAGNOSTIC_FRACTIONS = (0.25, 0.5, 0.75, 1.5, 2.5)


def _is_diagnostic_value(v: float) -> bool:
    """Is finding this number somewhere actually evidence of anything?"""
    if abs(v) <= 100.0 and abs(v - round(v)) <= 1e-12:
        return False                     # a small integer: 0, 1, 3, 6, 24, ...
    return not any(abs(v - u) <= 1e-12 for u in _UNDIAGNOSTIC_FRACTIONS)


@dataclass(frozen=True)
class Site:
    """A place in the tree that binds a constant.

    ``path`` is repo-relative.  ``name`` is the identifier bound there, or None
    if the value appears as a bare literal or inside a call.  ``kind`` says
    *how* it binds (see SITE_KINDS) and is what the C2 ratchet counts.
    ``expected`` overrides the constant's own value for ``literal`` sites that
    legitimately carry a rounded or unit-converted form (e.g. a 5-significant-
    figure 6.5978 against the exact closed form) — the consistency test then
    holds that site to its own precision rather than silently accepting drift.
    """
    path: str
    name: str | None = None
    kind: str = "literal"
    expected: float | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if self.kind not in SITE_KINDS:
            raise ValueError(
                f"{self.path}: unknown site kind {self.kind!r}; "
                f"expected one of {sorted(SITE_KINDS)}")
        if self.expected is not None and self.kind != "literal":
            raise ValueError(
                f"{self.path}: `expected` is only meaningful for kind='literal' "
                f"(a rounded local copy). A {self.kind!r} site cannot round.")


@dataclass(frozen=True)
class Constant:
    symbol: str
    units: str
    exactness: str
    provenance: tuple[str, ...]          # finding IDs that fixed it
    derivation: str
    sector: str
    value: float | Fraction | None = None
    bracket: tuple[float, float] | None = None
    supersedes: tuple[str, ...] = ()
    sites: tuple[Site, ...] = ()
    tol: float = 1e-9                    # site-agreement tolerance (relative)
    sweep: bool = True                   # participates in the C2.4 rogue sweep
    sweep_reason: str = ""               # required when sweep is False
    notes: str = ""

    def __post_init__(self) -> None:
        if self.exactness not in EXACTNESS_CLASSES:
            raise ValueError(
                f"{self.symbol}: unknown exactness class {self.exactness!r}; "
                f"expected one of {sorted(EXACTNESS_CLASSES)}")
        if self.sector not in SECTORS:
            raise ValueError(f"{self.symbol}: unknown sector {self.sector!r}")
        if not self.provenance:
            raise ValueError(
                f"{self.symbol}: no provenance. Every constant must record the "
                f"finding that fixed it (or 'CODATA'/'PDG'/'FLAG' if external).")
        if self.value is None and self.bracket is None:
            raise ValueError(f"{self.symbol}: needs a value or a bracket")
        if self.value is not None and self.bracket is not None:
            raise ValueError(f"{self.symbol}: has both a value and a bracket")
        if self.bracket is not None:
            lo, hi = self.bracket
            if lo > hi:
                raise ValueError(f"{self.symbol}: inverted bracket {self.bracket}")
        if not self.symbol.isidentifier():
            raise ValueError(
                f"{self.symbol!r}: registry symbols are exported as Python names "
                f"by casim.constants, so they must be valid identifiers.")
        if not self.sweep and not self.sweep_reason:
            raise ValueError(
                f"{self.symbol}: sweep=False needs a sweep_reason. Excluding a "
                f"constant from the C2.4 rogue sweep is a judgement call and "
                f"has to be written down.")

    # -- values -------------------------------------------------------------
    @property
    def exact_value(self) -> float | Fraction | None:
        """The exact object: a ``Fraction`` where the constant is rational,
        else the float closed form.  ``None`` for bracketed constants."""
        return self.value

    @property
    def float_value(self) -> float:
        """Numeric value; for bracketed constants, the bracket midpoint.

        Callers that care about the distinction should check ``bracket`` first.
        A midpoint is a convenience for display, never a result.
        """
        if self.value is not None:
            return float(self.value)
        lo, hi = self.bracket           # type: ignore[misc]
        return 0.5 * (lo + hi)

    @property
    def is_diagnostic(self) -> bool:
        """Is this value distinctive enough that finding it is evidence?

        A constant equal to 1.0 cannot be swept for: every module in the tree
        assigns 1.0 to something.  Used to sanity-check `sweep`.
        """
        if self.value is None:
            return True
        return _is_diagnostic_value(float(self.value))

    def contains(self, x: float, rel: float | None = None) -> bool:
        """Does `x` agree with this constant (within tolerance, or in bracket)?"""
        if self.bracket is not None:
            lo, hi = self.bracket
            pad = (hi - lo) * 1e-9
            return lo - pad <= x <= hi + pad
        v = float(self.value)           # type: ignore[arg-type]
        rel = self.tol if rel is None else rel
        return abs(x - v) <= rel * max(abs(v), 1e-300)

    # -- site queries --------------------------------------------------------
    def sites_of_kind(self, kind: str) -> tuple[Site, ...]:
        return tuple(s for s in self.sites if s.kind == kind)


@dataclass(frozen=True)
class MeasuredConstant:
    """A site that legitimately computes its own value for a registry symbol.

    C2.3.  This is the typed replacement for P0's regex ALLOWLIST.  The point
    is that the derivation *is* the physics under test: `derive_velocity_
    addition.py` measures the emergent light speed on a 2-D square lattice and
    gets 1/sqrt(2), and `forks/curl_fork_cubic.py` measures it on the simple
    cubic lattice and gets 1.0.  Neither is a drifted `c_lat`; both are
    experiments whose whole point is to land somewhere else.

    ``compares_to`` names the registry constant this record is *about*.
    ``value`` is what the site is expected to produce (None if the measurement
    has no predetermined answer — a dispersion fit converging on the canonical
    value, say).  ``reason`` is mandatory and must say why the number differs.

    ``kind`` distinguishes the two honest ways a site can carry a number that
    looks like a registry constant:

      ``measured``    — the SAME physical quantity, measured in a regime where
                        the answer differs (2-D square lattice, cubic fork).
      ``coincidence`` — a DIFFERENT physical quantity that happens to equal the
                        same number.  The registry already documents one of
                        these in prose (F231: the electroweak on-shell 2/9 and
                        the lepton delta* = 2/9 are unrelated); this makes the
                        category typed instead of a footnote.
    """
    path: str
    name: str | None
    compares_to: str
    reason: str
    kind: str = "measured"
    value: float | None = None
    provenance: tuple[str, ...] = ()
    tol: float = 1e-9

    def __post_init__(self) -> None:
        if self.kind not in MEASURED_KINDS:
            raise ValueError(
                f"{self.path}: unknown MeasuredConstant kind {self.kind!r}; "
                f"expected one of {sorted(MEASURED_KINDS)}")
        if not self.reason.strip():
            raise ValueError(
                f"{self.path}:{self.name}: a MeasuredConstant without a reason "
                f"is an allowlist entry with extra steps.")


def register(c: Constant) -> Constant:
    if c.symbol in _REGISTRY:
        raise ValueError(f"duplicate constant symbol {c.symbol!r}")
    _REGISTRY[c.symbol] = c
    return c


def register_measured(m: MeasuredConstant) -> MeasuredConstant:
    _MEASURED.append(m)
    return m


def get(symbol: str) -> Constant:
    try:
        return _REGISTRY[symbol]
    except KeyError:
        raise KeyError(
            f"no constant {symbol!r} in the registry; known: "
            f"{sorted(_REGISTRY)}") from None


def value(symbol: str) -> float:
    """The float value.  Use `exact()` when the exactness is the point."""
    return get(symbol).float_value


def exact(symbol: str) -> float | Fraction | None:
    """The exact object — a `Fraction` for the rational constants."""
    return get(symbol).exact_value


def all_constants(sector: str | None = None) -> list[Constant]:
    out = list(_REGISTRY.values())
    if sector is not None:
        out = [c for c in out if c.sector == sector]
    return sorted(out, key=lambda c: (c.sector, c.symbol))


def sweepable_constants() -> list[Constant]:
    """Constants distinctive enough for the C2.4 unregistered-literal sweep."""
    return [c for c in all_constants() if c.sweep and c.value is not None]


def by_finding(finding: str) -> list[Constant]:
    """Every constant whose provenance includes `finding` (e.g. 'F175')."""
    f = finding.upper()
    return [c for c in all_constants() if f in {p.upper() for p in c.provenance}]


def sites_for(path_fragment: str) -> list[tuple[Constant, Site]]:
    """Every (constant, site) whose recorded path contains `path_fragment`."""
    return [(c, s) for c in all_constants() for s in c.sites
            if path_fragment in s.path]


def all_measured() -> list[MeasuredConstant]:
    return list(_MEASURED)


def measured_at(path: str, name: str | None) -> MeasuredConstant | None:
    """The MeasuredConstant declared for (path, name), if any."""
    for m in _MEASURED:
        if m.path == path and (m.name == name or m.name is None):
            return m
    return None


# ---------------------------------------------------------------------------
# Importing the sector modules populates the registry.  Order is cosmetic.
# ---------------------------------------------------------------------------
from . import geometry, gravity, lepton, strong, electroweak  # noqa: E402,F401
from . import measured  # noqa: E402,F401  (C2.3 declarations)


# ---------------------------------------------------------------------------
# C2.1 — the value surface.  Every registry symbol becomes an importable name.
#
#     from casim.constants import c_lat, G_LATTICE, delta_star
#
# The exported name IS the registry symbol; there is no second naming scheme to
# keep in sync.  Rational constants export the `Fraction` under the symbol and
# a float under `<symbol>_f`, so a test that needs exactness and a kernel that
# needs a float array can each ask for what they need.  Bracketed constants
# export nothing scalar on purpose (C2.2): ask for an endpoint explicitly.
# ---------------------------------------------------------------------------
def _export() -> None:
    g = globals()
    for c in _REGISTRY.values():
        if c.bracket is not None:
            continue                     # no scalar surface, by design
        g[c.symbol] = c.value
        __all__.append(c.symbol)
        if isinstance(c.value, Fraction):
            g[c.symbol + "_f"] = float(c.value)
            __all__.append(c.symbol + "_f")


_export()


def bracket(symbol: str) -> tuple[float, float]:
    """The (lo, hi) of a bracketed constant.  Raises if it is not bracketed."""
    c = get(symbol)
    if c.bracket is None:
        raise ValueError(
            f"{symbol} is not bracketed — it has a value; import it directly.")
    return c.bracket


def endpoint(symbol: str, which: str) -> float:
    """An explicit endpoint of a bracketed constant: 'lo' or 'hi'.

    Bracketed constants have no midpoint accessor on purpose.  The frequently
    quoted alpha_eff* ~ 0.39 is the midpoint of two *scale choices*, not an
    independently determined number; making a caller name the endpoint is the
    correct friction (C2.2).
    """
    lo, hi = bracket(symbol)
    if which == "lo":
        return lo
    if which == "hi":
        return hi
    raise ValueError(f"endpoint must be 'lo' or 'hi', not {which!r}")


__all__ += ["bracket", "endpoint"]
