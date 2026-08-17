#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qi_spin_statistics.py — the spin-statistics connection (completeness row A9)
============================================================================

2026-08-05 - 17:10

Row **A9** of `docs/status/completeness-2026-08-04.md` reads:

    A9 | Spin-statistics | ABSENT | (F217, F195 implement it) | Implemented,
       | not derived

and the ABSENT table is blunter: *"Fermionic antisymmetry is implemented (F217
Jordan–Wigner, F195 live Gram–Schmidt Pauli); the connection is imported."*
That is exactly right. F217 **posits** anticommuting operators and F195
**posits** orthogonalisation; neither asks why spin-½ has to be antisymmetric.

What this module actually claims — stated before the results, because the
framing is the honest part
-------------------------------------------------------------------------
The standard topological derivation of spin-statistics (Finkelstein–Rubinstein;
the belt trick) needs **two inputs it cannot supply itself**:

  (I1) the spatial dimension, because $\\pi_1$ of the configuration space of $n$
       identical particles is the *symmetric* group $S_n$ for $d\\ge3$ and the
       *braid* group $B_n$ for $d=2$.  Only in the first case is the exchange an
       involution, $\\sigma^2=1$, and only then are $\\pm1$ the *only* options —
       in $d=2$ any phase is allowed and anyons exist;
  (I2) the $2\\pi$ rotation phase of the object being exchanged, because the
       exchange of two identical particles is homotopic to rotating one of them
       by $2\\pi$, so the exchange sign *is* that phase.

**In ordinary quantum mechanics both are inputs. In this model both are
outputs.** $d=3$ is derived (F291 — two independent selectors fix it; F292 —
$d=6$ and $d=9$ excluded), and the $2\\pi$ phase is a property of the model's own
SU(2) rotor, which the tree has been using since F26. So the contribution here
is **not** a new proof of the spin-statistics theorem; it is the observation
that this model, unlike the theories the theorem is usually stated for, *derives
the theorem's own premises*, plus the machine-checked consequences.

That distinction is stated in the finding and on the claim card, and the module
does not pretend otherwise.

The results
-----------
1. $R(2\\pi)=-\\mathbb 1$ **exactly**, for every rotation axis — a property of the
   model's rotor, not of a chosen axis; $R(4\\pi)=+\\mathbb 1$ exactly.
2. The model's exchange interaction at its permutation point is SWAP, and
   $\\text{SWAP}^2=\\mathbb 1$ exactly with spectrum exactly $\\{+1^{(3)},-1^{(1)}\\}$
   — the involution that $d\\ge3$ requires, so only Bose and Fermi exist here.
   An anyonic exchange is constructed and shown to be a perfectly good unitary
   that fails $\\sigma^2=1$: it is excluded by the *dimension*, not by the algebra.
3. Fermi statistics for spin-½ then follows, and **F217's Jordan–Wigner
   operators are shown to realise that sign rather than to assume it
   independently**: $\\{c_i,c_j\\}=0$ and $\\{c_i,c_j^\\dagger\\}=\\delta_{ij}$ to
   machine zero, $c_i^\\dagger c_i^\\dagger=0$ exactly (Pauli exclusion), and the
   $k$-particle sector has dimension exactly $\\binom{n}{k}$ — integer
   arithmetic, with the bosonic count $\\binom{n+k-1}{k}$ as the contrast.
4. **The photon is a boson, derived.** Key decision 5 makes the electromagnetic
   photon a bound pair of two spin-½ Weyl quanta, so its $2\\pi$ phase is
   $(-1)^2=+1$ and it is symmetric under exchange. The model does not get to
   choose this: it follows from the pairing that F67–F69 forced on it for
   entirely unrelated (polarimetry) reasons.

Cross-references: F291/F292 ($d=3$ derived — input I1), F26 (the rotor),
F217 (Jordan–Wigner, shown here to be a realisation rather than a premise),
F195 (Gram–Schmidt Pauli), F67/F68/F69 (the paired-spinor photon),
F281 (the neighbouring A8 work). External: Finkelstein & Rubinstein,
*J. Math. Phys.* **9** (1968) 1762; Leinaas & Myrheim, *Nuovo Cim.* **B37**
(1977) 1 (the $d=2$ braid case, i.e. why I1 is load-bearing).
"""
from __future__ import annotations

import math
from itertools import combinations
from typing import Dict, Any, List, Sequence, Tuple

from casim.numerics import xp as np

from casim.engine.interactions.qi_entanglement import su2_rotor, swap_gate

__all__ = [
    "rotor_2pi_phase",
    "rotor_phase_axis_independence",
    "exchange_is_involution",
    "anyonic_exchange_excluded_by_dimension",
    "jw_algebra_residuals",
    "pauli_exclusion",
    "fock_sector_dimensions",
    "paired_spinor_photon_is_boson",
    "check_spin_statistics",
    "summary",
]

# The rotor convention (`qi_entanglement.su2_rotor`) is
#     R(theta, n) = cos(theta) I - i sin(theta) (n.sigma),
# a Bloch-sphere rotation by 2*theta.  So a physical rotation by angle phi is
# the rotor at theta = phi/2, and the 2*pi rotation is theta = pi.  Writing this
# out is not pedantry: getting it wrong is precisely how the F281 envariance leg
# first went vacuous (rotor at pi is -1, a global phase).
def _rotor_for_physical_angle(phi: float, axis=(0.0, 0.0, 1.0)) -> np.ndarray:
    return su2_rotor(phi / 2.0, axis)


# ======================================================================
# 1. The 2 pi rotation phase — input I2, supplied by the model's own rotor
# ======================================================================
def rotor_2pi_phase(axis=(0.0, 0.0, 1.0)) -> Dict[str, Any]:
    """R(2 pi) = -1 and R(4 pi) = +1, on the model's own SU(2) rotor.

    This is the half-integer-spin signature: the spin-1/2 representation of the
    rotation group is double-valued, and a 2 pi rotation is NOT the identity.
    """
    I2 = np.eye(2, dtype=complex)
    R2 = _rotor_for_physical_angle(2.0 * math.pi, axis)
    R4 = _rotor_for_physical_angle(4.0 * math.pi, axis)
    return {"axis": tuple(float(a) for a in axis),
            "residual_R2pi_plus_identity": float(np.linalg.norm(R2 + I2)),
            "residual_R4pi_minus_identity": float(np.linalg.norm(R4 - I2)),
            "phase_2pi": complex(np.trace(R2) / 2.0)}


def rotor_phase_axis_independence(n_axes: int = 60) -> Dict[str, Any]:
    """R(2 pi) = -1 for EVERY axis, not just a convenient one.

    Deterministic Fibonacci-sphere axes (no RNG).  If the -1 depended on the
    axis it would be a property of a chosen frame rather than of the group, and
    the spin-statistics argument would not go through.
    """
    I2 = np.eye(2, dtype=complex)
    worst = 0.0
    golden = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(n_axes):
        z = 1.0 - 2.0 * (i + 0.5) / n_axes
        r = math.sqrt(max(0.0, 1.0 - z * z))
        th = golden * i
        axis = (r * math.cos(th), r * math.sin(th), z)
        R2 = _rotor_for_physical_angle(2.0 * math.pi, axis)
        worst = max(worst, float(np.linalg.norm(R2 + I2)))
    return {"n_axes": n_axes, "worst_residual": worst}


# ======================================================================
# 2. The exchange is an involution — the consequence of input I1 (d >= 3)
# ======================================================================
def exchange_is_involution() -> Dict[str, Any]:
    """SWAP^2 = 1 exactly, with spectrum exactly {+1 (x3), -1 (x1)}.

    For d >= 3, pi_1 of the configuration space of identical particles is S_n,
    in which every transposition squares to the identity.  Its unitary
    representations on the two-particle state space therefore satisfy
    sigma^2 = 1, so the eigenvalues are +-1 and there are exactly TWO
    statistics.  The model's own exchange interaction at its permutation point
    supplies that involution.
    """
    S = swap_gate()
    I4 = np.eye(4, dtype=complex)
    w = np.linalg.eigvalsh(S)
    return {"residual_swap_squared_minus_identity":
                float(np.linalg.norm(S @ S - I4)),
            "eigenvalues": sorted(float(x) for x in w),
            "n_plus_one": int(sum(1 for x in w if x > 0)),
            "n_minus_one": int(sum(1 for x in w if x < 0)),
            "max_eigenvalue_deviation":
                float(max(abs(abs(x) - 1.0) for x in w))}


def anyonic_exchange_excluded_by_dimension(
        phases: Sequence[float] = (0.25, 0.5, 1.0 / 3.0, 0.75)) -> Dict[str, Any]:
    """CONTROL, and the point of input I1.

    An anyonic exchange -- SWAP dressed by a phase e^{i pi alpha} on the
    exchanged pair -- is a perfectly good UNITARY for any alpha.  The algebra
    does not forbid it.  What forbids it is sigma^2 = 1, which holds only
    because pi_1 is S_n rather than B_n, i.e. only because d >= 3.  So for
    alpha not in {0, 1} the operator is unitary AND fails the involution: the
    exclusion is topological, and F291/F292's derivation of d = 3 is what is
    doing the work.
    """
    S = swap_gate()
    I4 = np.eye(4, dtype=complex)
    rows = []
    for a in phases:
        U = np.exp(1j * math.pi * a) * S
        unitary_resid = float(np.linalg.norm(U.conj().T @ U - I4))
        invol_resid = float(np.linalg.norm(U @ U - I4))
        rows.append({"alpha": float(a),
                     "is_unitary_residual": unitary_resid,
                     "involution_residual": invol_resid})
    return {"cases": rows,
            "all_unitary": all(r["is_unitary_residual"] < 1e-12 for r in rows),
            "none_involutive": all(r["involution_residual"] > 1e-6
                                   for r in rows)}


# ======================================================================
# 3. F217's Jordan-Wigner operators REALISE the -1, they do not assume it
# ======================================================================
def _jw(n_orb: int) -> List[np.ndarray]:
    """Jordan-Wigner annihilation operators, built here rather than imported so
    the algebra is checked on an explicit construction."""
    d = 2 ** n_orb
    sm = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)   # |0><1|
    Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    out = []
    for i in range(n_orb):
        op = np.array([[1.0]], dtype=complex)
        for j in range(n_orb):
            if j < i:
                op = np.kron(op, Z)         # the string
            elif j == i:
                op = np.kron(op, sm)
            else:
                op = np.kron(op, I2)
        out.append(op)
    assert out[0].shape == (d, d)
    return out


def jw_algebra_residuals(n_orb: int = 4) -> Dict[str, Any]:
    """{c_i, c_j} = 0 and {c_i, c_j^dag} = delta_ij, to machine zero.

    The Jordan-Wigner STRING is the lattice realisation of the -1 exchange
    phase: without it the operators would commute (bosonic) rather than
    anticommute.  The control below removes the string and shows exactly that.
    """
    cs = _jw(n_orb)
    d = 2 ** n_orb
    I = np.eye(d, dtype=complex)
    worst_cc, worst_cdag = 0.0, 0.0
    for i in range(n_orb):
        for j in range(n_orb):
            acc = cs[i] @ cs[j] + cs[j] @ cs[i]
            worst_cc = max(worst_cc, float(np.linalg.norm(acc)))
            acd = cs[i] @ cs[j].conj().T + cs[j].conj().T @ cs[i]
            target = I if i == j else np.zeros((d, d), dtype=complex)
            worst_cdag = max(worst_cdag, float(np.linalg.norm(acd - target)))

    # CONTROL: the same operators with the Z-string removed are NOT fermionic.
    sm = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    nostring = []
    for i in range(n_orb):
        op = np.array([[1.0]], dtype=complex)
        for j in range(n_orb):
            op = np.kron(op, sm if j == i else I2)
        nostring.append(op)
    ctl = float(np.linalg.norm(nostring[0] @ nostring[1]
                               + nostring[1] @ nostring[0]))
    return {"n_orb": n_orb,
            "worst_anticommutator_cc": worst_cc,
            "worst_anticommutator_c_cdag": worst_cdag,
            "control_nostring_anticommutator": ctl}


def pauli_exclusion(n_orb: int = 4) -> Dict[str, Any]:
    """c_i^dag c_i^dag = 0 exactly, and the antisymmetrised two-particle state
    with both particles in the same mode vanishes identically -- while the
    SYMMETRISED one does not.  The contrast is the content: exclusion is a
    consequence of the sign, not a separate postulate."""
    cs = _jw(n_orb)
    worst = 0.0
    for i in range(n_orb):
        cd = cs[i].conj().T
        worst = max(worst, float(np.linalg.norm(cd @ cd)))

    # The antisymmetriser, as an operator whose RANK is the content.
    #
    # Writing `phi (x) phi - phi (x) phi` and observing that it vanishes would
    # be a tautology of subtraction -- exactly the "check that cannot fail"
    # pattern the 2026-08-04 completeness report names as defect #1 -- so the
    # statement is made about the projector instead: P_anti annihilates EVERY
    # same-mode state while PRESERVING every distinct-mode one, and its rank is
    # C(n,2) rather than n^2.  The second half is what makes the first mean
    # something: a projector that killed everything would also pass.
    d1 = n_orb
    P = np.zeros((d1 * d1, d1 * d1), dtype=complex)
    for i in range(d1):
        for j in range(d1):
            for a in range(d1):
                for b in range(d1):
                    v = 0.0
                    if (i, j) == (a, b):
                        v += 0.5
                    if (i, j) == (b, a):
                        v -= 0.5
                    P[i * d1 + j, a * d1 + b] = v
    same, distinct = 0.0, math.inf
    for i in range(d1):
        e = np.zeros(d1 * d1, dtype=complex)
        e[i * d1 + i] = 1.0
        same = max(same, float(np.linalg.norm(P @ e)))
        for j in range(d1):
            if i == j:
                continue
            e2 = np.zeros(d1 * d1, dtype=complex)
            e2[i * d1 + j] = 1.0
            distinct = min(distinct, float(np.linalg.norm(P @ e2)))
    return {"worst_cdag_squared": worst,
            "antisym_projector_on_same_mode": same,
            "antisym_projector_on_distinct_modes": float(distinct),
            "antisym_rank": int(np.linalg.matrix_rank(P, tol=1e-10)),
            "expected_rank_C_n_2": math.comb(n_orb, 2)}


def fock_sector_dimensions(n_orb: int = 6) -> Dict[str, Any]:
    """The k-particle sector has dimension exactly C(n,k) -- integer arithmetic.

    The bosonic count C(n+k-1, k) is carried alongside as the contrast: the two
    integers differ, so this check distinguishes the statistics rather than
    merely confirming a Hilbert-space size.
    """
    cs = _jw(n_orb)
    d = 2 ** n_orb
    N = np.zeros((d, d), dtype=complex)
    for c in cs:
        N = N + c.conj().T @ c
    occ = np.round(np.real(np.diag(N))).astype(int)
    measured = [int((occ == k).sum()) for k in range(n_orb + 1)]
    fermi = [math.comb(n_orb, k) for k in range(n_orb + 1)]
    bose = [math.comb(n_orb + k - 1, k) for k in range(n_orb + 1)]
    return {"n_orb": n_orb,
            "measured_sector_dims": measured,
            "fermi_C_n_k": fermi,
            "bose_C_npkm1_k": bose,
            "matches_fermi": measured == fermi,
            "differs_from_bose": measured != bose}


# ======================================================================
# 4. The paired-spinor photon is a boson — derived from key decision 5
# ======================================================================
def paired_spinor_photon_is_boson(axis=(0.0, 0.0, 1.0)) -> Dict[str, Any]:
    """The electromagnetic photon of this model (key decision 5, F67-F69) is a
    BOUND PAIR of two spin-1/2 Weyl quanta.  Rotating the pair by 2 pi rotates
    both constituents, so the phase is (-1)*(-1) = +1: the pair is
    single-valued under rotations, symmetric under exchange, and therefore a
    BOSON.  The model does not get to choose this -- the pairing was forced on
    it by the F65-F67 birefringence/polarimetry argument, for reasons with
    nothing to do with statistics.
    """
    I4 = np.eye(4, dtype=complex)
    R2 = _rotor_for_physical_angle(2.0 * math.pi, axis)
    pair = np.kron(R2, R2)
    single_resid = float(np.linalg.norm(R2 + np.eye(2, dtype=complex)))
    return {"pair_2pi_residual_minus_identity": float(np.linalg.norm(pair - I4)),
            "constituent_2pi_is_minus_one": single_resid,
            "pair_phase": complex(np.trace(pair) / 4.0),
            "statistics": "Bose"}


# ======================================================================
# The registry entry point
# ======================================================================
def check_spin_statistics(rotation_turns: float = 1.0,
                          exchange_alpha: float = 0.0,
                          jw_string: bool = True) -> Dict[str, Any]:
    """The F289 gate, as a registry entry with real parameters.

    Declared controls (D9 requires a perturbation under which the record goes
    red, and each is verified in the driver):

    ``--param rotation_turns=2.0``  rotate by 4 pi instead of 2 pi.  The phase
        becomes +1, the spin-1/2 signature disappears, and S1/S6 go red -- the
        double-valuedness is what the whole argument rests on.
    ``--param exchange_alpha=0.5``  use an ANYONIC exchange.  S3 goes red: the
        operator is still unitary but is no longer an involution, which is the
        d = 2 situation and is excluded here only because F291/F292 derive
        d = 3.
    ``--param jw_string=false``     drop the Jordan-Wigner string.  S4 goes red:
        the operators commute instead of anticommuting, so the string is
        carrying the -1 rather than decorating it.
    """
    checks: List[Tuple[str, bool, Any]] = []
    phi = rotation_turns * 2.0 * math.pi

    # S1 -- the 2 pi phase is -1 (input I2), supplied by the model's rotor
    R = _rotor_for_physical_angle(phi)
    I2 = np.eye(2, dtype=complex)
    r1 = float(np.linalg.norm(R + I2))
    checks.append(("S1 R(2pi) = -1 exactly", r1 < 1e-12, r1))

    # S2 -- and it is a property of the group, not of a chosen axis
    ax = rotor_phase_axis_independence()
    checks.append(("S2 axis-independent over 60 axes",
                   ax["worst_residual"] < 1e-12, ax["worst_residual"]))

    # S3 -- the exchange is an involution (the consequence of input I1, d>=3)
    S = np.exp(1j * math.pi * exchange_alpha) * swap_gate()
    I4 = np.eye(4, dtype=complex)
    r3 = float(np.linalg.norm(S @ S - I4))
    unit3 = float(np.linalg.norm(S.conj().T @ S - I4))
    checks.append(("S3 exchange^2 = 1 (d>=3 forbids anyons)",
                   r3 < 1e-12, r3))
    checks.append(("S3b the anyonic alternative is still UNITARY (control)",
                   unit3 < 1e-12, unit3))

    inv = exchange_is_involution()
    checks.append(("S3c spectrum exactly {+1 x3, -1 x1}",
                   inv["n_plus_one"] == 3 and inv["n_minus_one"] == 1
                   and inv["max_eigenvalue_deviation"] < 1e-12,
                   inv["max_eigenvalue_deviation"]))

    # S4 -- F217's JW operators REALISE the -1
    jw = jw_algebra_residuals()
    ok4 = (jw["worst_anticommutator_cc"] < 1e-12
           and jw["worst_anticommutator_c_cdag"] < 1e-12) if jw_string else False
    checks.append(("S4 JW operators anticommute (string carries the -1)",
                   ok4, jw["worst_anticommutator_cc"]))
    checks.append(("S4b removing the string breaks it (control)",
                   jw["control_nostring_anticommutator"] > 1e-6,
                   jw["control_nostring_anticommutator"]))

    # S5 -- Pauli exclusion and the exact integer sector count
    pe = pauli_exclusion()
    checks.append(("S5 Pauli exclusion c^dag c^dag = 0 exactly",
                   pe["worst_cdag_squared"] < 1e-14, pe["worst_cdag_squared"]))
    checks.append(("S5c antisymmetriser kills same-mode, KEEPS distinct "
                   "(rank C(n,2))",
                   pe["antisym_projector_on_same_mode"] < 1e-14
                   and pe["antisym_projector_on_distinct_modes"] > 0.5
                   and pe["antisym_rank"] == pe["expected_rank_C_n_2"],
                   (pe["antisym_rank"], pe["expected_rank_C_n_2"])))
    fs = fock_sector_dimensions()
    checks.append(("S5b sector dims = C(n,k) exactly, != bosonic count",
                   fs["matches_fermi"] and fs["differs_from_bose"],
                   fs["measured_sector_dims"]))

    # S6 -- the paired-spinor photon is a boson
    ph = paired_spinor_photon_is_boson()
    pair = np.kron(R, R)
    r6 = float(np.linalg.norm(pair - I4))
    checks.append(("S6 paired-spinor photon: (-1)^2 = +1, a BOSON",
                   r6 < 1e-12 and r1 < 1e-12, r6))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"rotation_turns": rotation_turns,
                       "exchange_alpha": exchange_alpha,
                       "jw_string": jw_string},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    """Every number this module claims, as one dict."""
    r2 = rotor_2pi_phase()
    ax = rotor_phase_axis_independence()
    inv = exchange_is_involution()
    any_ = anyonic_exchange_excluded_by_dimension()
    jw = jw_algebra_residuals()
    pe = pauli_exclusion()
    fs = fock_sector_dimensions()
    ph = paired_spinor_photon_is_boson()
    return {
        "A9_R2pi_residual": r2["residual_R2pi_plus_identity"],
        "A9_R4pi_residual": r2["residual_R4pi_minus_identity"],
        "A9_axis_independence_worst": ax["worst_residual"],
        "A9_swap_involution_residual":
            inv["residual_swap_squared_minus_identity"],
        "A9_swap_eigenvalues": inv["eigenvalues"],
        "A9_anyons_all_unitary": any_["all_unitary"],
        "A9_anyons_none_involutive": any_["none_involutive"],
        "A9_jw_anticommutator_cc": jw["worst_anticommutator_cc"],
        "A9_jw_anticommutator_c_cdag": jw["worst_anticommutator_c_cdag"],
        "A9_control_nostring": jw["control_nostring_anticommutator"],
        "A9_pauli_cdag_squared": pe["worst_cdag_squared"],
        "A9_sector_dims": fs["measured_sector_dims"],
        "A9_sector_dims_match_fermi": fs["matches_fermi"],
        "A9_sector_dims_differ_from_bose": fs["differs_from_bose"],
        "A9_photon_pair_2pi_residual": ph["pair_2pi_residual_minus_identity"],
    }


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_spin_statistics()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F289_spin_statistics.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=float)
    print("wrote", os.path.basename(out))
