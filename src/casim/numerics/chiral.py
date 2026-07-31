"""casim.numerics.chiral — the hand-rolled chiral primitives. Roadmap C1.1.

CLAUDE.md's standing caveat: *"using numpy or scipy on chiral transforms may
not produce desired results. Check them first when troubleshooting. If they are
returning wrong results or dropping the real or imaginary elements, begin
writing our own library of functions from scratch so we know what they are
doing."*

`casim.lattice.chiral_core` is that from-scratch library and remains where the
physics lives (the BCC Weyl 2x2 unitary, the W+- Riemann-Silberstein branch
rotation). This module holds the two *arithmetic* primitives it is built on,
lifted into the numerics façade because they are the thing a future backend
must reproduce — a device backend has to prove it does complex multiplication
on explicit real pairs correctly before it may touch a chiral transform.

Every complex multiply is done on explicit (re, im) arrays. No complex dtype
handling is trusted, and no `np.linalg` is used on a chiral matrix.
"""
from __future__ import annotations

import numpy as np

__all__ = ["cmul", "su2_apply", "components_preserved"]


def cmul(ar, ai, br, bi):
    """(ar + i*ai) * (br + i*bi) on real arrays -> (real, imag).

    No complex dtype anywhere in the expression.
    """
    return ar * br - ai * bi, ar * bi + ai * br


def su2_apply(Uff, Ufg, Ugf, Ugg, F, G):
    """Apply the 2x2 mix [[Uff, Ufg], [Ugf, Ugg]] to the spinor (F, G).

    Arguments arrive as complex arrays for convenience, but every product is
    formed by :func:`cmul` on the explicit real/imaginary parts and the result
    is reassembled only at the end.
    """
    Ff_r, Ff_i = F.real, F.imag
    G_r, G_i = G.real, G.imag
    a1r, a1i = cmul(Uff.real, Uff.imag, Ff_r, Ff_i)
    a2r, a2i = cmul(Ufg.real, Ufg.imag, G_r, G_i)
    b1r, b1i = cmul(Ugf.real, Ugf.imag, Ff_r, Ff_i)
    b2r, b2i = cmul(Ugg.real, Ugg.imag, G_r, G_i)
    F_new = (a1r + a2r) + 1j * (a1i + a2i)
    G_new = (b1r + b2r) + 1j * (b1i + b2i)
    return F_new, G_new


def components_preserved(before, after, tol: float = 0.0) -> bool:
    """Did a transform keep BOTH components non-trivial?

    The specific failure CLAUDE.md warns about is a routine that silently
    returns only the real (or only the imaginary) part. That is invisible to a
    norm check when the dropped part was small, so it gets its own predicate:
    if `before` had an imaginary part, `after` must too.
    """
    b, a = np.asarray(before), np.asarray(after)
    for part in ("real", "imag"):
        had = np.any(np.abs(getattr(b, part)) > tol)
        has = np.any(np.abs(getattr(a, part)) > tol)
        if had and not has:
            return False
    return True
