"""F302 — which spinor bilinear is a spatial 3-vector, and which sectors use it.

The question, from the independent review of F17 (`docs/reviews/F17-review-
2026-08-03.md`): the retired composite-photon field is built from
``G^i = phi^T sigma^i psi`` (TRANSPOSE, not dagger; `bilinear.py:186`), and the
review measured ``||G_T||^2 = 2 (n_hat . y_hat)^2`` — an amplitude that tracks
the axis of the one ANTISYMMETRIC Pauli matrix and vanishes on the whole great
circle ``n_hat perp y_hat``. Ledger record ``S1-F69-sigma-bilinear-photon``
retains "the sigma-bilinear FIELD CONSTRUCTION" for W / Z / gluon, so if those
sectors used the same contraction they would carry a preferred Cartesian y-axis:
an isotropy violation nobody had looked for.

Two separate things are established here, and they are graded differently.

THE ALGEBRA (exact, sympy-checkable, no lattice).  ``eps = i sigma_2`` is the
SU(2) invariant tensor: ``U^T eps U = eps`` for every ``U`` with ``det U = 1``.
Therefore

    U^T (eps sigma^i) U  =  eps (eps^{-1} U^T eps) sigma^i U
                         =  eps U^{-1} sigma^i U
                         =  eps U^dag sigma^i U
                         =  R^{ij} (eps sigma^j)                        (exact)

using the standard adjoint identity ``U^dag sigma^i U = R^{ij} sigma^j``.  So
``eps`` is precisely the object that converts DAGGER covariance into TRANSPOSE
covariance, and ``psi^T eps sigma psi`` is a genuine 3-vector while
``psi^T sigma psi`` is not.  Concretely, ``eps sigma^i`` are all three symmetric
whereas ``sigma_2`` is antisymmetric, so ``psi^T sigma_2 psi == 0`` identically
and the plain triple is the covariant one with its y-component deleted:

    psi^T sigma psi      = ( 2ab,        0,          a^2 - b^2 )
    psi^T eps sigma psi  = ( a^2 - b^2,  i(a^2+b^2), -2ab      )

The Cartan/Penrose object is also null for EVERY spinor — ``G.G = 0`` with no
helicity condition — where the plain one gives ``G.G = (psi^T psi)^2``.

THE AUDIT (measurement, on this tree's own code).  The feared isotropy violation
is NOT in the gauge sectors.  W, Z and gluon never adopted the transpose form:
F29 had already found it fails SU(2) (and `gluon.py`'s own comment records that
it fails SU(3) too, "Hermitian only"), so every production construction is the
Hermitian one, which is covariant because ``U^dag sigma U = R sigma`` directly.
The transpose bilinear has **no live physics consumer** — only retired-photon
diagnostics and one fork harness.

Why the transpose form was reached for in the first place, and why "just use
Hermitian" is not an available fix for a one-mode construction: the Hermitian
singlet of a mode with ITSELF is ``psi^dag sigma psi = n_hat`` exactly, i.e.
purely LONGITUDINAL, so it carries no transverse field at all.  The Cartan form
is the object that is both covariant and transverse — ``||G_T||^2 = 2`` for
every direction.  That is the decision this module records.

Entry points (all exact / machine-precision, no free inputs):

    so3_covariance()     transpose vs Cartan vs the three production Hermitian
                         forms, under matched SU(2)/SO(3) pairs
    amplitude_signature() the 2 (n_hat . y_hat)^2 law on real BCC eigenmodes,
                         against the Cartan form's direction-independent 2
    sector_audit()       which constructions each gauge sector actually uses

Run as ``python3 -m casim.engine.gauge.derive_bilinear_so3`` to write
``test-results/F302_bilinear_so3.json``.

Note on randomness: this module takes an explicit ``seed`` and builds its own
generator rather than drawing from ``casim.numerics.rng``. That façade hands out
one stream per named CHANNEL, keyed off a global run seed, which is exactly what
you want for a simulation and exactly what you do not want for a gate assertion —
the registry record pins ``seed: 7`` so the 40 rotations are the same 40 every
run, and a covariance residual that moved would then be a real change.
"""
from __future__ import annotations

import json
import os

from casim.numerics import xp

from casim.engine.gauge import bilinear as _bl

__all__ = [
    "eps_sigma",
    "cartan_bilinear",
    "su2_so3_pair",
    "so3_covariance",
    "amplitude_signature",
    "sector_audit",
]

# The three Pauli matrices, taken from the module under audit so this cannot
# drift away from what the sectors actually contract with.
_S = tuple(xp.asarray(m, dtype=complex) for m in _bl._PAULIS)
_EPS = 1j * _S[1]                    # eps = i sigma_2, the SU(2) invariant tensor


def eps_sigma():
    """The symmetric triple ``eps sigma^i``. All three are symmetric."""
    return tuple(_EPS @ M for M in _S)


def cartan_bilinear(psi, phi=None):
    """``G'^i = phi^T (eps sigma^i) psi`` — the Cartan/Penrose bilinear.

    With ``phi is None`` the spinor is contracted with itself, which is the
    single-mode (photon-like) case. Null for every spinor: ``G'.G' = 0``.
    """
    if phi is None:
        phi = psi
    ES = eps_sigma()
    return xp.array([phi @ M @ psi for M in ES])


def su2_so3_pair(rng):
    """A random ``U`` in SU(2) and its matched ``R`` in SO(3).

    ``R^{ij} = 1/2 tr(sigma^i U sigma^j U^dag)`` is the adjoint image, so
    ``U^dag sigma^i U = R^{ij} sigma^j`` holds by construction and any covariance
    failure below is a property of the CONTRACTION, not of the pair.
    """
    n = rng.normal(size=3)
    n = n / xp.linalg.norm(n)
    th = rng.uniform(0.0, 2.0 * xp.pi)
    U = xp.cos(th / 2) * xp.eye(2) - 1j * xp.sin(th / 2) * sum(
        n[k] * _S[k] for k in range(3))
    R = xp.real(xp.array([[0.5 * xp.trace(_S[i] @ U @ _S[j] @ U.conj().T)
                           for j in range(3)] for i in range(3)]))
    return U, R


def _rel(a, b):
    d = float(xp.abs(xp.asarray(a) - xp.asarray(b)).max())
    s = max(float(xp.abs(xp.asarray(a)).max()),
            float(xp.abs(xp.asarray(b)).max()), 1e-300)
    return d / s


def so3_covariance(n_trials: int = 40, seed: int = 7):
    """Max relative violation of ``G(U psi) = R G(psi)`` for each construction.

    Returns ``{name: max_rel_err}``. Everything except the transpose form is a
    genuine 3-vector and lands at the round-off floor; the transpose form is
    O(1) and that is the whole point.
    """
    from casim.engine.gauge import weak_wmu as _wm
    from casim.engine.gauge import gluon as _gl
    from casim.engine.gauge import strong as _cstr

    g = xp.random.default_rng(seed)
    out: dict[str, float] = {}

    err_t, err_c = [], []
    for _ in range(n_trials):
        U, R = su2_so3_pair(g)
        psi = g.normal(size=2) + 1j * g.normal(size=2)
        phi = g.normal(size=2) + 1j * g.normal(size=2)
        err_t.append(_rel(_bl.bilinear_G(U @ psi, U @ phi),
                          R @ _bl.bilinear_G(psi, phi)))
        err_c.append(_rel(cartan_bilinear(U @ psi, U @ phi),
                          R @ cartan_bilinear(psi, phi)))
    out["transpose_bilinear_G"] = max(err_t)
    out["cartan_eps_sigma"] = max(err_c)

    err_s, err_w = [], []
    for _ in range(n_trials):
        U, R = su2_so3_pair(g)
        a = g.normal(size=(2, 2)) + 1j * g.normal(size=(2, 2))
        b = g.normal(size=(2, 2)) + 1j * g.normal(size=(2, 2))
        aU = xp.array([U @ a[k] for k in range(2)])
        bU = xp.array([U @ b[k] for k in range(2)])
        err_s.append(_rel(_bl._singlet_bilinear_H(bU, aU),
                          R @ _bl._singlet_bilinear_H(b, a)))
        err_w.append(_rel(_bl._triplet_bilinear_H(bU, aU),
                          _bl._triplet_bilinear_H(b, a) @ R.T))
    out["hermitian_singlet_H"] = max(err_s)
    out["hermitian_triplet_H"] = max(err_w)

    # Production W current: the spin index runs over (f, g) per isospin leg.
    shp = (2, 2, 2)
    mk = lambda: g.normal(size=shp) + 1j * g.normal(size=shp)   # noqa: E731
    f_nu, f_e, g_nu, g_e = mk(), mk(), mk(), mk()
    err = []
    for _ in range(min(n_trials, 12)):
        U, R = su2_so3_pair(g)
        fn = U[0, 0] * f_nu + U[0, 1] * g_nu
        gn = U[1, 0] * f_nu + U[1, 1] * g_nu
        fe = U[0, 0] * f_e + U[0, 1] * g_e
        ge = U[1, 0] * f_e + U[1, 1] * g_e
        J = _wm.fermion_current_isospin(f_nu, f_e, g_nu, g_e)
        JU = _wm.fermion_current_isospin(fn, fe, gn, ge)
        err.append(_rel(JU, xp.einsum('ij,ajxyz->aixyz', R, J)))
    out["weak_wmu_fermion_current_isospin"] = max(err)

    # Production colour octet, both geometries.
    for tag, shape, fn_octet in (
            ("gluon_quark_colour_octet_bilinear_bcc", (2, 2, 2),
             _gl.quark_colour_octet_bilinear_bcc),
            ("gluon_quark_colour_octet_bilinear_2d", (2, 2),
             _gl.quark_colour_octet_bilinear_2d)):
        q = {(f, c, d): g.normal(size=shape) + 1j * g.normal(size=shape)
             for f in _cstr.FLAVOURS for c in _cstr.COLOURS
             for d in ('eu', 'ed', 'cu', 'cd')}
        err = []
        for _ in range(4):
            U, R = su2_so3_pair(g)
            qU = dict(q)
            for f in _cstr.FLAVOURS:
                for c in _cstr.COLOURS:
                    for up, dn in (('eu', 'ed'), ('cu', 'cd')):
                        a_, b_ = q[(f, c, up)], q[(f, c, dn)]
                        qU[(f, c, up)] = U[0, 0] * a_ + U[0, 1] * b_
                        qU[(f, c, dn)] = U[1, 0] * a_ + U[1, 1] * b_
            G, GU = fn_octet(q), fn_octet(qU)
            err.append(_rel(GU, xp.einsum('ij,a...j->a...i', R, G)))
        out[tag] = max(err)

    return out


def _bloch(psi):
    return xp.real(xp.array([xp.conj(psi) @ M @ psi for M in _S])) / float(
        xp.vdot(psi, psi).real)


def amplitude_signature(k_mag: float = 0.05, seed: int = 3):
    """The ``2 (n_hat . y_hat)^2`` law, measured on real BCC helicity eigenmodes.

    Returns ``(rows, summary)``. For each propagation direction: the transverse
    amplitude of the transpose bilinear against ``2 (n_hat . y_hat)^2``, and the
    Cartan bilinear's amplitude against the direction-independent 2.
    """
    g = xp.random.default_rng(seed)
    dirs = {'x_hat': (1, 0, 0), 'y_hat': (0, 1, 0), 'z_hat': (0, 0, 1),
            '(1,1,1)': (1, 1, 1), '(1,0,1)': (1, 0, 1), '(1,2,3)': (1, 2, 3)}
    for _ in range(4):
        v = g.normal(size=3)
        dirs["rand_" + "_".join(f"{x:+.3f}" for x in v / xp.linalg.norm(v))] = tuple(v)

    rows, dev_t, dev_c, dev_null, dev_trans = [], 0.0, 0.0, 0.0, 0.0
    for name, v in dirs.items():
        kh = xp.asarray(v, dtype=float)
        kh = kh / xp.linalg.norm(kh)
        psi_p, _, _ = _bl.weyl_eigenmodes_3d_bcc(*(k_mag * kh))
        psi_p = psi_p / xp.linalg.norm(psi_p)
        n_hat = _bloch(psi_p)
        G_t = _bl.bilinear_G(psi_p, psi_p)
        G_c = cartan_bilinear(psi_p)
        amp_t = float(xp.vdot(_bl._transverse_part(G_t, n_hat),
                              _bl._transverse_part(G_t, n_hat)).real)
        amp_c = float(xp.vdot(_bl._transverse_part(G_c, n_hat),
                              _bl._transverse_part(G_c, n_hat)).real)
        law = 2.0 * float(n_hat[1]) ** 2
        rows.append({"direction": name, "n_dot_y": float(n_hat[1]),
                     "amp_transpose": amp_t, "law_2_ny_sq": law,
                     "amp_cartan": amp_c,
                     "cartan_longitudinal": float(abs(xp.dot(n_hat, G_c))),
                     "cartan_self_dot": float(abs(xp.dot(G_c, G_c)))})
        dev_t = max(dev_t, abs(amp_t - law))
        dev_c = max(dev_c, abs(amp_c - 2.0))
        dev_null = max(dev_null, rows[-1]["cartan_self_dot"])
        dev_trans = max(dev_trans, rows[-1]["cartan_longitudinal"])

    # The Hermitian singlet of a mode with itself: purely longitudinal.
    kh = xp.asarray([1.0, 2.0, 3.0])
    kh = kh / xp.linalg.norm(kh)
    psi_p, _, _ = _bl.weyl_eigenmodes_3d_bcc(*(k_mag * kh))
    psi_p = psi_p / xp.linalg.norm(psi_p)
    n_hat = _bloch(psi_p)
    G_H = xp.array([xp.conj(psi_p) @ M @ psi_p for M in _S])
    G_HT = _bl._transverse_part(xp.real(G_H), n_hat)

    summary = {
        "max_dev_transpose_from_2_ny_sq": dev_t,
        "max_dev_cartan_from_2": dev_c,
        "max_cartan_self_dot": dev_null,
        "max_cartan_longitudinal": dev_trans,
        "hermitian_singlet_equals_n_hat": float(
            xp.abs(xp.real(G_H) - n_hat).max()),
        "hermitian_singlet_transverse_amp": float(xp.dot(G_HT, G_HT)),
    }
    return rows, summary


def sector_audit():
    """Which contraction each gauge sector actually builds its field from.

    A static statement of the audit, kept next to the measurement so the two
    cannot drift apart. ``form`` is one of ``transpose`` | ``hermitian`` |
    ``none``; only ``transpose`` carries the defect.
    """
    return [
        {"sector": "photon (canonical, F69)", "module": "gauge/photon.py",
         "form": "none",
         "note": "paired-spinor; builds no sigma-bilinear at all"},
        {"sector": "photon (retired, F65-F67)", "module": "gauge/bilinear.py",
         "form": "transpose",
         "note": "bilinear_G; retired as the photon, diagnostics only"},
        {"sector": "W triplet", "module": "gauge/bilinear.py:_triplet_bilinear_H",
         "form": "hermitian", "note": "F29 construction"},
        {"sector": "W current (production)",
         "module": "gauge/weak_wmu.py:fermion_current_isospin",
         "form": "hermitian", "note": "eta^dag sigma^i tau^a eta"},
        {"sector": "W (SU(2) action)", "module": "gauge/weak.py",
         "form": "none", "note": "SU(2) acts ON the doublet; no field built from spinors"},
        {"sector": "Z", "module": "gauge/weak_z.py", "form": "none",
         "note": "independent (E_Z,B_Z) pair; scalar site-density currents only"},
        {"sector": "charged current", "module": "gauge/charged_current.py",
         "form": "none", "note": "scalar isospin ladder, no sigma^i"},
        {"sector": "gluon / colour octet",
         "module": "gauge/gluon.py:quark_colour_octet_bilinear_{2d,bcc}",
         "form": "hermitian",
         "note": "own comment: transpose fails SU(3) too, Hermitian only"},
        {"sector": "strong / su3_ladder / colour_*",
         "module": "gauge/{strong,su3_ladder,colour_*}.py", "form": "none",
         "note": "link variables and irrep labels; no spinor bilinear"},
    ]


def symbolic_core():
    """The exact algebra, sympy, residuals identically zero.

    Four statements, in the order they are needed:

    1. ``U^T eps U = det(U) eps`` for an ARBITRARY 2x2 matrix. This is the whole
       reason ``eps`` works — it is not an SU(2) fact, it is the adjugate
       identity, and SU(2) only enters by fixing ``det U = 1``.
    2. ``eps sigma^i`` is symmetric for all three ``i`` (so no component of
       ``psi^T eps sigma psi`` is annihilated), while ``sigma_2`` is
       antisymmetric (so ``psi^T sigma_2 psi`` vanishes identically).
    3. ``(psi^T eps sigma psi) . (psi^T eps sigma psi) = 0`` for every spinor —
       the Cartan/Penrose nullity, with no helicity condition.
    4. ``(psi^T sigma psi) . (psi^T sigma psi) = (psi^T psi)^2`` — the Fierz
       value the transpose form gives instead, which is why it is null only on
       the measure-zero set ``psi^T psi = 0``.

    Returns a dict of residuals; every one is an exact sympy zero.
    """
    import sympy as sp

    s1 = sp.Matrix([[0, 1], [1, 0]])
    s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    s3 = sp.Matrix([[1, 0], [0, -1]])
    S = [s1, s2, s3]
    eps = sp.I * s2

    a, b, c, d = sp.symbols('a b c d')
    U = sp.Matrix([[a, b], [c, d]])
    r_adj = sp.simplify(U.T * eps * U - U.det() * eps)

    r_sym = sum(sp.simplify((eps * M).T - (eps * M)).norm() for M in S)
    r_anti = sp.simplify(s2.T + s2).norm()

    x, y = sp.symbols('x y')
    psi = sp.Matrix([x, y])
    G_c = sp.Matrix([sp.expand((psi.T * (eps * M) * psi)[0]) for M in S])
    G_p = sp.Matrix([sp.expand((psi.T * M * psi)[0]) for M in S])
    r_null = sp.simplify((G_c.T * G_c)[0])
    r_fierz = sp.simplify((G_p.T * G_p)[0] - ((psi.T * psi)[0]) ** 2)
    r_y = sp.simplify((psi.T * s2 * psi)[0])

    return {
        "U_T_eps_U_minus_detU_eps": complex(r_adj.norm()),
        "eps_sigma_asymmetry": complex(r_sym),
        "sigma2_symmetry": complex(r_anti),
        "cartan_self_dot": complex(r_null),
        "transpose_self_dot_minus_fierz": complex(r_fierz),
        "psi_T_sigma2_psi": complex(r_y),
    }


def f302_bilinear_so3_check(n_trials: int = 40, seed: int = 7,
                            k_mag: float = 0.05):
    """Gate entry point. Returns True, or raises AssertionError naming the miss.

    Six assertions:
      C1 the exact algebra (sympy, residuals identically zero);
      C2 the transpose bilinear FAILS SO(3) covariance at O(1);
      C3 the Cartan bilinear and all four Hermitian production forms are
         covariant at the round-off floor;
      C4 the transpose amplitude obeys ``2 (n_hat . y_hat)^2`` on real BCC
         eigenmodes, and so vanishes on the great circle ``n_hat perp y_hat``;
      C5 the Cartan amplitude is direction-independent (=2), transverse, null;
      C6 the sector audit finds NO gauge sector on the transpose form.
    """
    sym = symbolic_core()
    for name, val in sym.items():
        assert abs(val) == 0.0, f"C1 symbolic residual {name} = {val!r}, want exact 0"

    cov = so3_covariance(n_trials=n_trials, seed=seed)
    assert cov["transpose_bilinear_G"] > 0.1, (
        "C2 the transpose bilinear was expected to FAIL SO(3) covariance at "
        f"O(1); measured {cov['transpose_bilinear_G']:.3e}")
    for key, val in cov.items():
        if key == "transpose_bilinear_G":
            continue
        assert val < 1e-12, f"C3 {key} is not SO(3)-covariant: {val:.3e}"

    rows, summary = amplitude_signature(k_mag=k_mag, seed=3)
    assert summary["max_dev_transpose_from_2_ny_sq"] < 1e-12, (
        "C4 transpose amplitude departs from 2(n.y)^2 by "
        f"{summary['max_dev_transpose_from_2_ny_sq']:.3e}")
    assert any(r["direction"] == "x_hat" and r["amp_transpose"] < 1e-20
               for r in rows), "C4 the great-circle zero at n_hat = x_hat is missing"
    assert summary["max_dev_cartan_from_2"] < 1e-12, (
        f"C5 Cartan amplitude is not 2: {summary['max_dev_cartan_from_2']:.3e}")
    assert summary["max_cartan_longitudinal"] < 1e-12, "C5 Cartan is not transverse"
    assert summary["max_cartan_self_dot"] < 1e-12, "C5 Cartan is not null"
    assert summary["hermitian_singlet_transverse_amp"] < 1e-20, (
        "C5 the Hermitian singlet of a mode with itself should be purely "
        "longitudinal")

    audit = sector_audit()
    offenders = [a for a in audit
                 if a["form"] == "transpose" and "retired" not in a["sector"]]
    assert not offenders, (
        "C6 a live gauge sector is on the transpose bilinear: "
        + ", ".join(a["sector"] for a in offenders))
    return True


def _results_path(name: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        cand = os.path.join(here, "test-results")
        if os.path.isdir(cand):
            return os.path.join(cand, name)
        here = os.path.dirname(here)
    raise FileNotFoundError("test-results/ not found above " + __file__)


def main() -> int:
    cov = so3_covariance()
    rows, summary = amplitude_signature()
    audit = sector_audit()
    payload = {
        "finding": "F302",
        "symbolic_core_residuals": {k: abs(v) for k, v in symbolic_core().items()},
        "so3_covariance_max_rel_err": cov,
        "amplitude_rows": rows,
        "amplitude_summary": summary,
        "sector_audit": audit,
        "n_transpose_sectors": sum(1 for a in audit if a["form"] == "transpose"),
    }
    with open(_results_path("F302_bilinear_so3.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    for k, v in cov.items():
        print(f"  {k:44s} {v:.3e}")
    print(f"  amplitude: transpose vs 2(n.y)^2 "
          f"{summary['max_dev_transpose_from_2_ny_sq']:.2e}; "
          f"cartan vs 2 {summary['max_dev_cartan_from_2']:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
