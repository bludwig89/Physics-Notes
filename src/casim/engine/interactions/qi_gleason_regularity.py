#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qi_gleason_regularity.py — closing A6r's last residual: a non-negative frame
function on this model's ray spaces is automatically regular (F329)
=====================================================================

2026-08-27 - 14:40

F304 section 5 proved the frame-function dichotomy (Born forced, the d=2 hole
derived, not exhibited) **for f in L^2** -- by harmonic analysis, not by citing
Gleason.  Section 5.5 then named exactly one residual:

    "Gleason's theorem holds for merely BOUNDED f, and the bridge -- that a
     non-negative frame function is automatically continuous -- is the
     Cooke-Keane-Moran regularity lemma (Cooke, Keane & Moran 1985), which is
     not reproved here.  What the lemma excludes is a non-measurable weight
     assignment."

CL264 carries that residual as its named `contingent` hypothesis: "Closing it
is a real, bounded piece of work (CKM is three pages of sphere geometry)."

This module closes it -- and it turns out the three pages were never CKM's own
to begin with.  **The identical proposition is already Theorem 2.8 of
Gleason's own 1957 paper** [Gleason 1957], the theorem F304 section 5
independently re-derives the OTHER half of (Theorem 2.3: continuous frame
function on R^3 is regular, via harmonic analysis).  Gleason's own proof needs
nothing beyond non-negativity and compactness of the sphere -- no appeal to
CKM's separate, later, more-elementary-but-not-shorter method is required, and
none is made here.

The chain, quoted from the primary source (section numbers are Gleason's own):

  Theorem 2.3   Every CONTINUOUS frame function on the unit sphere in R^3 is
                regular.  [The half F304 section 5 reproves by representation
                theory, for general d, not just d=3.]

  Theorem 2.8   Every NON-NEGATIVE frame function on the unit sphere in R^3 is
                regular.  Proved by first reducing to continuity (subtract a
                constant so inf f = 0; pick a near-minimal point p; the
                "polar rotation" u through pi/2 about p makes
                g(x) = f(x) + f(ux) constant on the equator of p, because
                {p, q, uq} is then an orthonormal triple and the frame
                condition forces f(p) + f(q) + f(uq) = W for EVERY q there --
                this is the one identity this module machine-checks below,
                `equator_constancy_identity`) -- then propagating that
                near-constancy to a global oscillation bound via Lemmas
                2.5-2.7 (a covering argument on great circles), concluding f
                is continuous, hence Theorem 2.3 applies.  The oscillation
                bookkeeping (Lemmas 2.5-2.7's specific constants) is CITED,
                not re-derived here -- see "What is cited vs adapted vs
                verified" below.

  Lemma 3.3 +   A frame function on ANY Hilbert space (real or complex,
  Theorem 3.5   dim >= 3) that is regular on every "completely real" subspace
                (one on which the inner product is real-valued) is regular;
                and every completely real 2-dim subspace embeds in a
                completely real 3-dim one whenever dim >= 3, so Theorem 2.8
                bootstraps from R^3 to any Hilbert space of dimension >= 3.
                This is the reduction the model's own d = 4, 8, 9, 16, 64, 96
                need, and it is unconditional: it needs nothing about the CA
                construction beyond dim >= 3, which F304 section 1.1 and F312
                G7 already established structurally.

Cooke, Keane & Moran (1985) independently reprove the SAME proposition
(Gleason's own Theorems 2.3+2.8 combined) by a different, longer but
lower-prerequisite route through Cauchy's functional equation: a frame
function extended additively to Hermitian operators is bounded (0 <= f <= W
falls straight out of the frame condition plus non-negativity, with no
separate assumption), and a bounded solution of Cauchy's equation is forced
linear by a one-line rational-approximation argument, with no measure theory
at all [Cooke, Keane & Moran 1985; the Cauchy-equation characterisation is
described secondhand, since the scanned 1985 original could not be retrieved
in machine-readable form this session -- see the module docstring's honesty
section].  Either route proves the same theorem; Gleason's own is the one
reproduced/adapted here because its primary-source text was directly
retrievable and quotable.

What is cited vs adapted vs verified (read this before trusting a number)
---------------------------------------------------------------------------
  CITED, not re-derived or re-checked here:
    * Theorem 2.8's proof that SOME propagation constant exists at all --
      Gleason's Lemmas 2.5-2.7, a covering argument on great circles of S^2
      whose specific bookkeeping constants (5, 20, 88 in Gleason's own write-
      up) are quoted from the primary source, not independently re-derived.
      This is the one piece of real analysis this closure still trusts a
      secondary retrieval of rather than reproducing symbol-by-symbol.
    * Theorem 2.3 itself for d=3 (regular <=> continuous, "spherical
      harmonics") -- F304 section 5 already reproves this for GENERAL d by an
      independent method (isotypic decomposition under U(d)); it is not
      re-derived a second time here for d=3 specifically.

  ADAPTED to this model, and where the real content of this finding is:
    * The reduction (Lemma 3.3 / Theorem 3.5) is stated for THIS model's
      actual ray-space dimensions, not left as an abstract "dim >= 3".
    * The equator-constancy identity, the one piece of Theorem 2.8's proof
      that is a clean checkable algebraic fact rather than a covering
      argument, is verified on frame functions built from THIS model's own
      completely-real-subspace embeddings.

  VERIFIED (machine, this module):
    * `completely_real_subspace_exists` -- Theorem 3.5's hypothesis, for
      every dimension this model actually builds a Born-rule measurement
      context on (`MODEL_DIMENSIONS`, from F304 section 1.1 and F312 G7).
    * `frame_condition_across_bases` -- that a regular (quadratic-form)
      function satisfies the frame condition on MANY random bases (the
      converse half of Gleason's Lemma 2.1, which is what licenses testing
      the machinery on a regular example at all), and that an added odd-
      degree-3 harmonic (F304 section 3.1's own P_3(n_z) construction, reused
      here) breaks it at d=3 -- the D9 control.
    * `equator_constancy_identity` -- the {p, q, uq} orthonormal-triple
      identity Theorem 2.8's proof turns on, and that it breaks under the
      SAME control.

  NOT claimed: that the covering/propagation combinatorics of Gleason's
  Lemmas 2.5-2.7 have been independently re-derived, or that a genuinely
  non-measurable (Hamel-basis / axiom-of-choice) frame function has been
  numerically exhibited failing the identity -- neither is possible on a
  computer, and neither is what closes the residual.  What closes it is that
  the PROPOSITION F304 section 5.5 named ("a non-negative frame function is
  automatically continuous") is Gleason's own peer-reviewed Theorem 2.8, in
  print since 1957, requiring nothing about this model beyond the hypothesis
  (dim >= 3, verified) that F304/F312 already established.

Cross-references: [[F304-born-rule-gleason-premises-forced]] (section 5, the
dichotomy this closes the last premise of; section 5.5, the residual named
here), [[F312-born-rule-nonabelian-premises]] (G7, the dimensions this module
reuses), [[F281-measurement-pointer-basis-born-rule-rg-classicality]].
External: A. M. Gleason, *J. Math. Mech.* **6** (1957) 885 (Theorems 2.3, 2.8,
Lemma 3.3, Theorem 3.5, quoted from the primary text); R. Cooke, M. Keane &
W. Moran, *Math. Proc. Camb. Phil. Soc.* **98** (1985) 117 (the alternative,
lower-prerequisite proof of the same proposition, described secondhand).
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from casim.numerics import xp as np

__all__ = [
    "MODEL_DIMENSIONS",
    "build_completely_real_basis",
    "completely_real_subspace_exists",
    "polar_rotation",
    "regular_frame_function",
    "p3_harmonic",
    "frame_condition_across_bases",
    "equator_constancy_identity",
    "summary",
    "check_gleason_regularity",
]

# The Hilbert-space dimensions this model actually builds a Born-rule
# measurement context on -- each traced to the SPECIFIC table cell that
# names it, not merely a number that appears somewhere in F304/F312:
#   3   F312 G7's "dim with no pointer" column for SU(3)_c (N=3, the colour
#       factor alone -- what "SU(3)_c clears d>=3 with no reference to the
#       pointer" means).
#   4   F304 section 1.1's minimal system+record pointer space, no internal
#       factor: 2^(1 system cell + 1 record cell).
#   6   F312 G7's "dim with F304's minimal record pointer" column for
#       SU(3)_c: d_p * N = 2 * 3.
#   64  F312 G4: the SU(2)_L sector with the pointer genuinely present
#       (context-blindness re-measured there).
#   96  F312 G5: the SU(3)_c sector with the pointer genuinely present.
# An earlier draft of this module also listed 8, 9 and 16, sourced (in
# error, caught by this finding's own review pass -- see F329 section
# "Reviewed & corrected") from UNRELATED table cells: 8 is F304 section
# 1.3's POINTER-ONLY commutant dimension 2^3 for three pointer cells with
# no system cell at all (not a measurement context -- it is exactly the
# "no record without cells" case F304 section 1.1 excludes); 9 and 16 are
# F304 section 3.3's d^2 = 3^2, 4^2, the dimension of the FRAME-FUNCTION
# (Hermitian-operator) space at Hilbert dimension d=3, d=4 -- a different
# object from a ray-space dimension, and already implied by 3 and 4 being
# on this list.  Removed rather than reinterpreted, since no reading of
# F304/F312 supports them as measurement-context Hilbert dimensions.
# These are dimension COUNTS, not physical constants -- casim.constants
# (D7) governs measured/derived physical quantities, not the sizes of
# Hilbert spaces the engine happens to build, so this tuple is a plain
# literal.
MODEL_DIMENSIONS: Tuple[int, ...] = (3, 4, 6, 64, 96)

# The one dimension F304/F312 establish is NEVER a valid standalone Born-rule
# measurement context in this model: isospin alone, with no pointer (F312 G7:
# "needs d_p >= 2").  It is included here, separately, as a NEGATIVE control
# on `completely_real_subspace_exists` itself -- Theorem 3.5's hypothesis
# (dim >= 3) must FAIL for it, confirming F304 section 3's own d=2 hole is
# correctly excluded rather than silently papered over by this check.
EXCLUDED_DIMENSION: int = 2


# ----------------------------------------------------------------------------
# Theorem 3.5's hypothesis: a completely real 3-dim subspace, for every
# dimension the model actually uses.
# ----------------------------------------------------------------------------

def build_completely_real_basis(d: int, n: int = 3) -> np.ndarray:
    """n mutually orthonormal REAL-coordinate vectors in C^d, n <= d.

    Gleason's own definition (section 3.1): a real-linear subspace of a
    Hilbert space is "completely real" iff the inner product takes only real
    values on it.  The standard basis vectors e_0..e_{n-1} trivially qualify
    -- <e_i, e_j> = delta_ij is real for every i, j by construction -- and
    the real span of any real-coordinate orthonormal set is completely real,
    so this is not a special property of the standard basis; it is the
    generic case.  Returned as a d x n matrix whose columns are the e_i.
    """
    if n > d:
        raise ValueError(f"need n <= d, got n={n}, d={d}")
    return np.eye(d, n, dtype=complex)


def completely_real_subspace_exists(d: int) -> Dict[str, Any]:
    """Theorem 3.5's hypothesis, MACHINE-checked rather than assumed: does C^d
    (d >= 3) contain a completely real 3-dim subspace?  Checked by exhibiting
    one (`build_completely_real_basis`) and verifying its Gram matrix is
    EXACTLY the real identity -- zero imaginary part, zero real deviation.
    """
    if d < 3:
        return {"d": d, "has_completely_real_3dim_subspace": False,
                "max_imag_inner_product": None,
                "max_real_deviation_from_identity": None}
    B = build_completely_real_basis(d, 3)
    G = B.conj().T @ B
    return {"d": d, "has_completely_real_3dim_subspace": True,
            "max_imag_inner_product": float(np.max(np.abs(G.imag))),
            "max_real_deviation_from_identity":
                float(np.max(np.abs(G.real - np.eye(3))))}


# ----------------------------------------------------------------------------
# The mechanical core of Theorem 2.8's proof: the {p, q, uq} orthonormal
# triple and the equator-constancy identity it forces.
# ----------------------------------------------------------------------------

def polar_rotation(axis: int = 0, n: int = 3) -> np.ndarray:
    """The 'polar rotation through angle pi/2' about `axis`, embedded as an
    n x n real orthogonal matrix (Gleason's own construction in the proof of
    Theorem 2.8; n=3 is that theorem's own setting).  For axis=0 this is the
    standard (x1, x2) -> (-x2, x1) rotation in the plane orthogonal to e_0,
    leaving e_0 itself fixed.
    """
    other = [i for i in range(n) if i != axis]
    i, j = other[0], other[-1]
    U = np.eye(n)
    U[i, i] = 0.0
    U[j, j] = 0.0
    U[i, j] = -1.0
    U[j, i] = 1.0
    return U


def regular_frame_function(T: np.ndarray):
    """f(x) = x^T T x for symmetric real T -- Gleason's Lemma 2.1: in a
    finite-dim real Hilbert space a frame function is regular IFF it is the
    restriction to the sphere of a quadratic form.  Used here as a concrete,
    genuine (non-pathological) frame function to run the mechanics on.
    """
    def f(x: np.ndarray) -> float:
        x = np.asarray(x, dtype=float)
        return float(x @ T @ x)
    return f


def p3_harmonic(x: np.ndarray, axis: int = 1) -> float:
    """P_3(x_axis) -- the degree-3 Legendre harmonic F304 section 3.1 uses to
    exhibit the d=2 hole.  Reused here as the D9 CONTROL: F304 section 5.3
    proves this mode is annihilated by the frame condition (does NOT survive
    1 + (d-1) b_k = 0) for every d >= 3, unlike at d = 2 where every odd k
    survives.  Adding it to a regular f must therefore break the frame
    condition -- and with it, the equator-constancy identity that is a
    CONSEQUENCE of the frame condition -- at d = 3, which is exactly what
    `frame_condition_across_bases` / `equator_constancy_identity` check when
    called with `control=True`.
    """
    t = float(np.asarray(x, dtype=float)[axis])
    return 0.5 * (5.0 * t ** 3 - 3.0 * t)


def _random_orthonormal_basis(n: int, rng) -> np.ndarray:
    A = rng.normal(size=(n, n))
    Q, R = np.linalg.qr(A)
    Q = Q * np.sign(np.diag(R))          # fix the QR sign ambiguity
    return Q


def frame_condition_across_bases(seed: int = 0, n_bases: int = 400,
                                  epsilon: float = 0.0) -> Dict[str, Any]:
    """The frame condition itself, checked directly: sum_i f(e_i) over MANY
    random orthonormal bases of R^3, for f = (regular quadratic form) +
    epsilon * P_3(x_1).

    epsilon = 0  (honest case): sum is EXACTLY constant = Tr(T) for every
                 basis, by the basis-independence of the trace -- the
                 converse half of Gleason's Lemma 2.1, and the fact that
                 licenses testing Theorem 2.8's mechanics on a regular
                 example at all.
    epsilon != 0 (D9 control): the cubic term is NOT annihilated by the
                 frame condition at d=3 (F304 section 5.3), so the sum must
                 vary across bases -- and does.
    """
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(3, 3))
    T = (A + A.T) / 2.0
    f = regular_frame_function(T)
    W = float(np.trace(T))

    sums: List[float] = []
    for _ in range(n_bases):
        Q = _random_orthonormal_basis(3, rng)
        basis = [Q[:, i] for i in range(3)]
        s = sum(f(e) + epsilon * p3_harmonic(e) for e in basis)
        sums.append(s)
    sums = np.array(sums)
    spread = float(np.max(sums) - np.min(sums))
    return {"seed": seed, "n_bases": n_bases, "epsilon": epsilon,
            "W": W, "mean_sum": float(np.mean(sums)),
            "max_sum": float(np.max(sums)), "min_sum": float(np.min(sums)),
            "spread": spread,
            "is_frame_function": spread < 1e-10}


def equator_constancy_identity(seed: int = 0, n_q: int = 500,
                                epsilon: float = 0.0) -> Dict[str, Any]:
    """The mechanical core of Gleason's Theorem 2.8 proof.

    Pick pole p = e_0, the polar rotation u through pi/2 about p.  For every
    q on the equator (q perp p, unit norm), {p, q, uq} is an orthonormal
    triple (checked directly below, not assumed), so the frame condition
    forces

        g(q) := f(q) + f(uq) = W - f(p)      for EVERY q on the equator,

    i.e. g is EXACTLY CONSTANT.  This is the identity Gleason's proof of
    Theorem 2.8 builds on (his own text: "g is a non-negative frame function
    of weight 2W ... g(q) = f(q) + f(uq) = W - f(p); thus g is constant on
    the equator").  Checked here on f = (regular quadratic form) +
    epsilon * P_3(x_1), same construction and same D9 control as
    `frame_condition_across_bases`.
    """
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(3, 3))
    T = (A + A.T) / 2.0
    f = regular_frame_function(T)
    W = float(np.trace(T))

    def f_eps(x: np.ndarray) -> float:
        return f(x) + epsilon * p3_harmonic(x)

    p = np.array([1.0, 0.0, 0.0])
    u = polar_rotation(axis=0, n=3)
    fp = f_eps(p)
    target = W - fp

    thetas = np.linspace(0.0, 2.0 * np.pi, n_q, endpoint=False)
    max_dev = 0.0
    max_orthonormality_defect = 0.0
    for th in thetas:
        q = np.array([0.0, np.cos(th), np.sin(th)])
        uq = u @ q
        gram = np.array([
            [p @ p, p @ q, p @ uq],
            [p @ q, q @ q, q @ uq],
            [p @ uq, q @ uq, uq @ uq],
        ])
        max_orthonormality_defect = max(
            max_orthonormality_defect, float(np.max(np.abs(gram - np.eye(3)))))
        g = f_eps(q) + f_eps(uq)
        max_dev = max(max_dev, abs(g - target))

    return {"seed": seed, "n_q": n_q, "epsilon": epsilon, "W": W, "f_p": fp,
            "target_g": target,
            "max_orthonormality_defect": max_orthonormality_defect,
            "max_equator_constancy_deviation": max_dev,
            "identity_holds": max_dev < 1e-9 and max_orthonormality_defect < 1e-12}


# ----------------------------------------------------------------------------
# Registry entry point
# ----------------------------------------------------------------------------

def summary(control: bool = False, seed: int = 0) -> Dict[str, Any]:
    epsilon = 0.35 if control else 0.0
    return {
        "H1_dimensions": [completely_real_subspace_exists(d)
                           for d in MODEL_DIMENSIONS],
        "H1_excluded_dimension": completely_real_subspace_exists(EXCLUDED_DIMENSION),
        "H2_frame_condition": frame_condition_across_bases(
            seed=seed, epsilon=epsilon),
        "H3_equator_identity": equator_constancy_identity(
            seed=seed, epsilon=epsilon),
        "control": control,
    }


def check_gleason_regularity(control: bool = False, seed: int = 0) -> Dict[str, Any]:
    """Registry entry point.  Returns {'checks': [...], 'n_checks': .., 'all_pass': ..}."""
    s = summary(control=control, seed=seed)
    checks: List[Dict[str, Any]] = []

    def add(cid, desc, ok, value):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok), "value": value})

    for rec in s["H1_dimensions"]:
        d = rec["d"]
        add(f"H1[d={d}]",
            "Theorem 3.5's hypothesis: C^d contains a completely real 3-dim "
            "subspace, d >= 3",
            rec["has_completely_real_3dim_subspace"]
            and rec["max_imag_inner_product"] == 0.0
            and rec["max_real_deviation_from_identity"] == 0.0,
            (rec["max_imag_inner_product"], rec["max_real_deviation_from_identity"]))

    exc = s["H1_excluded_dimension"]
    add(f"H1[d={EXCLUDED_DIMENSION}, excluded]",
        "NEGATIVE control: d=2 (isospin alone, no pointer) must FAIL Theorem "
        "3.5's hypothesis -- confirming F304 section 3's d=2 hole is excluded "
        "by this check, not silently papered over",
        exc["has_completely_real_3dim_subspace"] is False, exc)

    # H2/H3 use a FIXED pass criterion regardless of `control` -- the D9
    # idiom is an honest check whose acceptance condition never changes;
    # only the INPUT (`epsilon`, via `control`) changes, and a gate-tier
    # control is verified by re-running with control=True and confirming
    # THESE SAME criteria go red, not by a second branch that expects the
    # break and reports pass-on-break.
    h2 = s["H2_frame_condition"]
    add("H2", "the frame condition holds across random bases (Lemma 2.1 converse); "
        "must go RED under control=True (F304 section 5.3's k=3 mode is not "
        "annihilated at d=3)",
        h2["is_frame_function"], h2["spread"])

    h3 = s["H3_equator_identity"]
    add("H3", "equator-constancy identity (Theorem 2.8's mechanical core) holds; "
        "must go RED under control=True",
        h3["identity_holds"], h3["max_equator_constancy_deviation"])

    n_pass = sum(c["pass"] for c in checks)
    return {"checks": checks, "n_checks": len(checks), "n_pass": n_pass,
            "n_fail": len(checks) - n_pass, "all_pass": n_pass == len(checks),
            "control": control}
