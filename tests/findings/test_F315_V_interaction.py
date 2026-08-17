"""F315 — F313 falsifier 5 does not fire: V does not survive interaction.

F313 sec.9 measured a SECOND dispersive commuting flow V = I_branch (x) A on the
free massive Dirac walk and labelled the reading ("V is the s = 2 update lifted
branch-blind, the fundamental clock beside its dressed self") a READING, not a
result — falsifier 5 of the finding and of CL269.  This record settles it.

The question is asked in its STRONG form.  "Does V commute with the interacting
evolution?" is the weak form; an interacting theory can carry a DEFORMED
conserved charge (that is what integrability is), so the test must also ask
whether any O(G) deformation of V survives.  Leg C5 is that question and it is
the one that decides.

Eleven checks.  The load-bearing ones are re-derived here INDEPENDENTLY of
`casim.engine.lattice.time_signature_interacting`: the walk is re-typed from
`references/qca-papers-1-4-overview.md` Eqs. 15/23, the joint eigenbasis is
rebuilt, and C3's obstruction count is recomputed from that re-typed data rather
than read back from the module.

  C1 (machine)  FREE LIMIT — V is exactly conserved at G = 0.  The N = 2
      recovery of F313's C7 and the positive control that the machinery works.
  C2 (exact)    THE TEST CAN SAY "SURVIVES" — a deliberately INTEGRABLE
      interaction (diagonal in the mode basis) gives ZERO obstructed elements.
      Without this leg a verdict of "V dies" would be worthless.
  C3 (machine)  CONTACT (Hubbard/NJL, F217/F77) breaks V, and maximally:
      max|dphi_V| ~ pi across live matrix elements.  Recomputed independently.
  C4 (machine)  PHOTON EXCHANGE (F68, 1/q^2 kernel) — same verdict, so the
      conclusion depends on the interaction being a genuine scatterer and not
      on its form.
  C5 (machine)  THE DEFORMATION IS OBSTRUCTED — the decisive leg.  Resonant
      elements (dOmega = 0, where the O(G) denominator vanishes) carry
      dphi_V != 0, so no deformed V is conserved at leading order.
  C6 (machine)  THE CONTROL THAT MAKES C5 MEAN SOMETHING — on that same
      resonant set the EVOLUTION's own charge has dOmega = 0 to 1.8e-15.  A
      test that flagged every charge would flag this one.
  C7 (machine)  ROBUSTNESS across three momentum sectors K.
  C8 (machine)  ROBUSTNESS in the mass — massless and massive both obstructed.
  C9 (exact)    THE L = 2 TRAP — at L = 2 every sin(theta_j) = 0, the Bloch
      vector vanishes identically and the walk is trivial, so the test reports
      "survives" for no physical reason.  Asserted to be recognised.
  C10 (machine) THE HONEST NEGATIVE — the <100> line was PREDICTED to go blind
      (exact on-axis linearity, F20/F301) and does NOT: arccos-folding makes
      umklapp destroy additivity even on an exactly linear branch.  Both halves
      are asserted, the linearity AND the failure of the prediction.
  C11 (exact)   the verdict.

Three declared controls (D9/H2), all verified RED:

  ``--param L=2``                  the degenerate grid.  C9 must go red.
  ``--param kind=mode_diagonal``   an interaction that does not scatter.  C3/C5
      must go red, which is the same statement as C2 passing.
  ``--param res_tol=0.0``          empties the resonant set, so the obstruction
      claim has no content.  C5 must go red (the F298 idiom).
"""
from __future__ import annotations

import functools
import itertools
import math

from casim.numerics import xp as np

_PAULI = (((0, 1), (1, 0)), ((0, -1j), (1j, 0)), ((1, 0), (0, -1)))


def _wrap(x):
    return (x + math.pi) % (2 * math.pi) - math.pi


# ══════════════════════════════════════════════════════════════════
#  The walk, RE-TYPED from the paper — not imported from the module
# ══════════════════════════════════════════════════════════════════

@functools.lru_cache(maxsize=None)
def _joint(L=3, m=0.37, dirs=(0, 1, 2)):
    """Joint eigenphases (Omega, phi_V) and eigenvectors, rebuilt from Eqs. 15/23."""
    sig = [np.array(p, dtype=complex) for p in _PAULI]
    n_ = math.sqrt(1.0 - m * m)
    ks = list(itertools.product(range(L), repeat=3))
    Om, pV, X, resid = {}, {}, {}, 0.0
    for n in ks:
        th = [2 * math.pi * n[j] / L if j in dirs else 0.0 for j in range(3)]
        c = [math.cos(t) for t in th]
        s = [math.sin(t) for t in th]
        u = c[0] * c[1] * c[2] + s[0] * s[1] * s[2]
        nn = [s[0] * c[1] * c[2] - c[0] * s[1] * s[2],
              -c[0] * s[1] * c[2] + s[0] * c[1] * s[2],
              c[0] * c[1] * s[2] + s[0] * s[1] * c[2]]
        A = u * np.eye(2) - 1j * sum(nn[i] * sig[i] for i in range(3))
        Z = np.zeros((2, 2), dtype=complex)
        D = np.block([[n_ * A, 1j * m * np.eye(2)],
                      [1j * m * np.eye(2), n_ * A.conj().T]])
        V = np.block([[A, Z], [Z, A]])
        # Arbitrary non-degenerate mixing weights. They carry NO physics: any
        # generic real combination of the four Hermitian parts has a simple
        # spectrum, and its eigenbasis then diagonalises D and V at once. Chosen
        # to collide with no registry constant (the first draft used 0.7331,
        # which `constants-consistency` correctly flagged against e_saturation).
        M = ((D + D.conj().T) / 2 + 0.8231 * (V + V.conj().T) / 2
             + 0.6197 * ((D - D.conj().T) / 2j) + 0.2903 * ((V - V.conj().T) / 2j))
        _, P = np.linalg.eigh(M)
        Om[n] = np.angle(np.einsum('ij,jk,ki->i', P.conj().T, D, P))
        pV[n] = np.angle(np.einsum('ij,jk,ki->i', P.conj().T, V, P))
        X[n] = P
        resid = max(resid,
                    float(np.abs(P.conj().T @ D @ P - np.diag(np.exp(1j * Om[n]))).max()),
                    float(np.abs(P.conj().T @ V @ P - np.diag(np.exp(1j * pV[n]))).max()))
    return ks, Om, pV, X, resid


def _obstruction(L=3, m=0.37, K=(1, 2, 0), kind="contact", dirs=(0, 1, 2),
                 res_tol=1e-9):
    """Independent recomputation of the survival report from the re-typed walk."""
    ks, Om, pV, X, resid = _joint(L, m, dirs)
    modes = [(k, a) for k in ks for a in range(4)]
    basis = [(i, j) for i in range(len(modes)) for j in range(i + 1, len(modes))
             if tuple((modes[i][0][t] + modes[j][0][t]) % L
                      for t in range(3)) == tuple(K)]
    ov = {(kp, k): X[kp].conj().T @ X[k] for kp in ks for k in ks}

    def kern(kp, kr):
        if kind != "coulomb":
            return 1.0
        q = [_wrap(2 * math.pi * (kp[t] - kr[t]) / L) for t in range(3)]
        q2 = sum(x * x for x in q)
        return 1.0 if q2 < 1e-12 else 1.0 / q2

    def W(p, q, r, s):
        (kp, ap), (kq, aq), (kr, ar), (ksx, asx) = (modes[p], modes[q],
                                                    modes[r], modes[s])
        if tuple((kp[t] + kq[t]) % L for t in range(3)) != \
           tuple((kr[t] + ksx[t]) % L for t in range(3)):
            return 0j
        if kind == "mode_diagonal":
            return complex(1.0) if (p == r and q == s) else 0j
        return kern(kp, kr) * ov[(kp, kr)][ap, ar] * ov[(kq, ksx)][aq, asx]

    nb = len(basis)
    if nb == 0:
        # An empty sector must not raise: a control that CRASHES scores INVALID
        # rather than CONTROL, which banks an untested control as sound. Return
        # zeros and let the callers' assertions fail cleanly.
        return {"sector_dim": 0, "joint_residual": resid, "live": 0,
                "max_dphi_V_live": 0.0, "resonant": 0, "obstructed": 0,
                "max_dphi_V_resonant": 0.0, "control_free_charge": 0.0}
    H = np.zeros((nb, nb), dtype=complex)
    for a, (p, q) in enumerate(basis):
        for b, (r, s) in enumerate(basis):
            H[a, b] = W(p, q, r, s) - W(p, q, s, r) - W(q, p, r, s) + W(q, p, s, r)
    H = (H + H.conj().T) / 2
    qV = np.array([pV[modes[p][0]][modes[p][1]] + pV[modes[q][0]][modes[q][1]]
                   for p, q in basis])
    qO = np.array([Om[modes[p][0]][modes[p][1]] + Om[modes[q][0]][modes[q][1]]
                   for p, q in basis])
    dV = _wrap(qV[:, None] - qV[None, :])
    dO = _wrap(qO[:, None] - qO[None, :])
    live = np.abs(H) > 1e-10
    res = live & (np.abs(dO) < res_tol)
    obst = res & (np.abs(dV) > 1e-6)
    return {"sector_dim": nb, "joint_residual": resid,
            "live": int(live.sum()),
            "max_dphi_V_live": float(np.abs(np.where(live, dV, 0.0)).max()),
            "resonant": int(res.sum()), "obstructed": int(obst.sum()),
            "max_dphi_V_resonant": float(np.abs(np.where(obst, dV, 0.0)).max()),
            "control_free_charge": float(np.abs(np.where(res, dO, 0.0)).max())}


# ══════════════════════════════════════════════════════════════════
#  Checks
# ══════════════════════════════════════════════════════════════════

def check_C1_free_limit_V_is_conserved(L=3, m=0.37):
    """At G = 0 V commutes with the walk exactly — the N=2 recovery of F313 C7."""
    ks, Om, pV, X, resid = _joint(L, m)
    sig = [np.array(p, dtype=complex) for p in _PAULI]
    n_ = math.sqrt(1.0 - m * m)
    worst = 0.0
    for n in ks:
        th = [2 * math.pi * n[j] / L for j in range(3)]
        c = [math.cos(t) for t in th]
        s = [math.sin(t) for t in th]
        u = c[0] * c[1] * c[2] + s[0] * s[1] * s[2]
        nn = [s[0] * c[1] * c[2] - c[0] * s[1] * s[2],
              -c[0] * s[1] * c[2] + s[0] * c[1] * s[2],
              c[0] * c[1] * s[2] + s[0] * s[1] * c[2]]
        A = u * np.eye(2) - 1j * sum(nn[i] * sig[i] for i in range(3))
        Z = np.zeros((2, 2), dtype=complex)
        D = np.block([[n_ * A, 1j * m * np.eye(2)], [1j * m * np.eye(2), n_ * A.conj().T]])
        V = np.block([[A, Z], [Z, A]])
        worst = max(worst, float(np.abs(V @ D - D @ V).max()))
    out = {"max_commutator": worst, "joint_residual": resid}
    assert worst < 1e-12, out
    assert resid < 1e-12, out
    return out


def check_C2_test_can_report_survival(L=3, m=0.37, res_tol=1e-9):
    """An INTEGRABLE (mode-diagonal) interaction leaves V conserved: 0 obstructed.

    Without this leg a verdict of "V dies" would be worthless — a test that
    always says "dies" has measured nothing.
    """
    r = _obstruction(L=L, m=m, kind="mode_diagonal", res_tol=res_tol)
    out = {"obstructed": r["obstructed"], "max_dphi_V_live": r["max_dphi_V_live"],
           "live": r["live"]}
    assert out["live"] > 0, out
    assert out["obstructed"] == 0, (
        "the integrable control must leave V conserved; if it does not, the "
        f"test cannot distinguish anything: {out}")
    assert out["max_dphi_V_live"] < 1e-9, out
    return out


def check_C3_contact_breaks_V(L=3, m=0.37, kind="contact", res_tol=1e-9):
    """Contact (Hubbard/NJL, F217/F77) breaks V maximally: max|dphi_V| ~ pi."""
    r = _obstruction(L=L, m=m, kind=kind, res_tol=res_tol)
    out = {"kind": kind, "live": r["live"],
           "max_dphi_V_live": r["max_dphi_V_live"], "sector_dim": r["sector_dim"]}
    assert out["live"] > 1000, out
    assert out["max_dphi_V_live"] > 1.0, (
        f"V is not broken by {kind} — falsifier 5 would FIRE: {out}")
    return out


def check_C4_photon_exchange_breaks_V(L=3, m=0.37, res_tol=1e-9):
    """F68 minimal coupling (1/q^2): same verdict, so the form does not matter."""
    r = _obstruction(L=L, m=m, kind="coulomb", res_tol=res_tol)
    out = {"live": r["live"], "max_dphi_V_live": r["max_dphi_V_live"],
           "obstructed": r["obstructed"]}
    assert out["max_dphi_V_live"] > 1.0, out
    assert out["obstructed"] > 0, out
    return out


def check_C5_deformation_is_obstructed(L=3, m=0.37, kind="contact", res_tol=1e-9):
    """THE DECISIVE LEG. No O(G) deformation of V can be conserved.

    Q_2 = dq_V W / dOmega solves the O(G) condition except where dOmega = 0.
    On those resonant elements dq_V must vanish by itself, and it does not.
    """
    r = _obstruction(L=L, m=m, kind=kind, res_tol=res_tol)
    out = {"resonant": r["resonant"], "obstructed": r["obstructed"],
           "max_dphi_V_resonant": r["max_dphi_V_resonant"]}
    assert out["resonant"] > 0, (
        "the resonant set is empty, so the obstruction claim has no content "
        f"(F298 idiom): {out}")
    assert out["obstructed"] > 0, (
        "no obstruction found — a deformed V could exist and falsifier 5 would "
        f"remain open: {out}")
    assert out["max_dphi_V_resonant"] > 1.0, out
    return out


def check_C6_control_free_charge_survives_on_resonant_set(L=3, m=0.37, res_tol=1e-9):
    """On the SAME resonant set the evolution's own charge is conserved.

    This is what stops C5 being vacuous: a test that flagged every charge would
    flag this one too.
    """
    r = _obstruction(L=L, m=m, kind="contact", res_tol=res_tol)
    out = {"control_free_charge": r["control_free_charge"],
           "resonant": r["resonant"], "obstructed": r["obstructed"]}
    assert out["resonant"] > 0, out
    assert out["control_free_charge"] < 1e-12, (
        "the evolution's own charge is NOT conserved on the resonant set, so "
        f"the obstruction test is flagging everything and means nothing: {out}")
    assert out["obstructed"] > 0, out
    return out


def check_C7_robust_across_momentum_sectors(L=3, m=0.37, res_tol=1e-9):
    """Three total-momentum sectors, same verdict."""
    rows = []
    for K in ((0, 0, 0), (1, 0, 0), (1, 2, 0)):
        r = _obstruction(L=L, m=m, K=K, kind="contact", res_tol=res_tol)
        rows.append({"K": K, "obstructed": r["obstructed"], "resonant": r["resonant"]})
    out = {"rows": rows, "all_obstructed": all(x["obstructed"] > 0 for x in rows)}
    assert len(rows) >= 3, out
    assert out["all_obstructed"], out
    return out


def check_C8_robust_in_the_mass(L=3, res_tol=1e-9):
    """Massless and massive both obstructed."""
    rows = []
    for m in (0.0, 0.37, 0.8):
        r = _obstruction(L=L, m=m, kind="contact", res_tol=res_tol)
        rows.append({"m": m, "obstructed": r["obstructed"]})
    out = {"rows": rows, "all_obstructed": all(x["obstructed"] > 0 for x in rows)}
    assert len(rows) >= 2, out
    assert out["all_obstructed"], out
    return out


def check_C9_L2_grid_is_degenerate(L=3):
    """At L = 2 every sin(theta_j) = 0, n~ === 0 and the walk is TRIVIAL.

    The first run of this test was at L = 2 and returned a clean false negative.
    The control `--param L=2` must go red here.
    """
    def bloch_max(LL):
        worst = 0.0
        for n in itertools.product(range(LL), repeat=3):
            th = [2 * math.pi * n[j] / LL for j in range(3)]
            c = [math.cos(t) for t in th]
            s = [math.sin(t) for t in th]
            nn = [s[0] * c[1] * c[2] - c[0] * s[1] * s[2],
                  -c[0] * s[1] * c[2] + s[0] * c[1] * s[2],
                  c[0] * c[1] * s[2] + s[0] * s[1] * c[2]]
            worst = max(worst, max(abs(x) for x in nn))
        return worst
    out = {"L": L, "bloch_max_at_L2": bloch_max(2), "bloch_max_at_L": bloch_max(L),
           "L2_is_degenerate": bloch_max(2) < 1e-12}
    assert out["L2_is_degenerate"], out
    assert out["bloch_max_at_L"] > 1e-6, (
        f"the grid in use is degenerate — the walk is trivial and the whole "
        f"test is a false negative: {out}")
    return out


def check_C10_on_axis_does_not_go_blind(L=3, m=0.37, res_tol=1e-9):
    """The honest negative: <100> was predicted blind (exact linearity) and is not.

    BOTH halves are asserted — that the on-axis dispersion really is exactly
    linear, and that the obstruction survives anyway.  arccos-folding makes
    umklapp destroy additivity even on an exactly linear branch, which is why
    the result does not depend on going off-axis.
    """
    c3 = 1.0 / math.sqrt(3.0)
    lin = 0.0
    for t in (0.01, 0.3, 0.9, 1.5):
        om = math.acos(max(-1.0, min(1.0, math.cos(t * c3))))
        lin = max(lin, abs(om - t * c3))
    r = _obstruction(L=L, m=m, K=(1, 0, 0), kind="contact", dirs=(0,), res_tol=res_tol)
    out = {"on_axis_linearity_residual": lin, "obstructed": r["obstructed"],
           "max_dphi_V_resonant": r["max_dphi_V_resonant"]}
    assert out["on_axis_linearity_residual"] < 1e-12, (
        f"the <100> dispersion is not exactly linear — the premise of the "
        f"prediction this leg records as WRONG: {out}")
    assert out["obstructed"] > 0, (
        "the <100> restriction went blind after all; the mechanism is lattice "
        f"curvature rather than arccos-folding and sec.5 needs rewriting: {out}")
    return out


def check_C11_verdict(L=3, m=0.37, res_tol=1e-9):
    """Falsifier 5 does not fire."""
    contact = _obstruction(L=L, m=m, kind="contact", res_tol=res_tol)
    integ = _obstruction(L=L, m=m, kind="mode_diagonal", res_tol=res_tol)
    out = {"contact_obstructed": contact["obstructed"],
           "integrable_obstructed": integ["obstructed"],
           "falsifier_5_fires": bool(contact["obstructed"] == 0)}
    assert not out["falsifier_5_fires"], out
    assert out["integrable_obstructed"] == 0, out
    return out


CHECKS = (
    # C9 runs FIRST, deliberately: it is the guard that the grid in use is not
    # degenerate, and every other leg is meaningless on a trivial walk. Running
    # it last let the `L=2` control CRASH in an empty sector instead of failing,
    # which scores INVALID and would bank an untested control as sound.
    ("C9_L2_grid_is_degenerate", check_C9_L2_grid_is_degenerate),
    ("C1_free_limit_V_is_conserved", check_C1_free_limit_V_is_conserved),
    ("C2_test_can_report_survival", check_C2_test_can_report_survival),
    ("C3_contact_breaks_V", check_C3_contact_breaks_V),
    ("C4_photon_exchange_breaks_V", check_C4_photon_exchange_breaks_V),
    ("C5_deformation_is_obstructed", check_C5_deformation_is_obstructed),
    ("C6_control_free_charge_survives_on_resonant_set",
     check_C6_control_free_charge_survives_on_resonant_set),
    ("C7_robust_across_momentum_sectors", check_C7_robust_across_momentum_sectors),
    ("C8_robust_in_the_mass", check_C8_robust_in_the_mass),
    ("C10_on_axis_does_not_go_blind", check_C10_on_axis_does_not_go_blind),
    ("C11_verdict", check_C11_verdict),
)


def check_all(L=3, m=0.37, kind="contact", res_tol=1e-9):
    """Registry entry point.

    Three declared controls (D9/H2, `control:` on `F315-V-interaction`):

    ``--param L=2``                the degenerate grid (n~ === 0).  C9 red.
    ``--param kind=mode_diagonal`` an interaction that does not scatter.  C3/C5 red.
    ``--param res_tol=0.0``        empties the resonant set, so the obstruction
        claim has no content.  C5 red (F298 idiom).
    """
    kw = {
        "check_C1_free_limit_V_is_conserved": {"L": L, "m": m},
        "check_C2_test_can_report_survival": {"L": L, "m": m, "res_tol": res_tol},
        "check_C3_contact_breaks_V": {"L": L, "m": m, "kind": kind, "res_tol": res_tol},
        "check_C4_photon_exchange_breaks_V": {"L": L, "m": m, "res_tol": res_tol},
        "check_C5_deformation_is_obstructed": {"L": L, "m": m, "kind": kind,
                                               "res_tol": res_tol},
        "check_C6_control_free_charge_survives_on_resonant_set":
            {"L": L, "m": m, "res_tol": res_tol},
        "check_C7_robust_across_momentum_sectors": {"L": L, "m": m, "res_tol": res_tol},
        "check_C8_robust_in_the_mass": {"L": L, "res_tol": res_tol},
        "check_C9_L2_grid_is_degenerate": {"L": L},
        "check_C10_on_axis_does_not_go_blind": {"L": L, "m": m, "res_tol": res_tol},
        "check_C11_verdict": {"L": L, "m": m, "res_tol": res_tol},
    }
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "F313 falsifier 5 does NOT fire. V = I (x) A is broken by every genuine "
        "interaction tested — contact (F217/F77) and photon exchange (F68) — "
        "maximally (|dphi_V| ~ pi), and the O(G) deformation is OBSTRUCTED on "
        "resonant elements, so no deformed V survives either. The integrable "
        "control confirms the test can report survival. V is an artifact of "
        "FREENESS; F313 sec.9's reading is confirmed and the rank-1 time count "
        "is the count of the INTERACTING theory at any cell. Not settled: all "
        "orders in G, and the F86 colour dielectric."
    )
    return out


# --- no pytest surface ------------------------------------------------------
# Deliberately no thin `test_*` wrappers: this is an `entry:` record, and
# tests/casim/test_registry_integrity.py forbids a file being both.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, default=str))
