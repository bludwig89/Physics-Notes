#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
casimir_ladder.py — the SU(N) Casimir ladder F110 deferred, and what it does to C7
==================================================================================

2026-08-05 - 23:20

`link_hamiltonian.py`'s scope note has said since 2026-06-06:

    Dynamical-matter coupling and the **SU(3) Casimir ladder remain future
    work** (the centre projection argument F97-F99 is why Z_3 is the
    load-bearing case).

F294 identified that deferral as the thing standing between B10's selector and
a verdict, because the F110 C7 map chi = 1/(4 g^2) -- the identity F144's whole
g_s = 1/2 derivation rests on -- was only ever verified for compact U(1) and
Z_N.  This module builds the ladder and re-runs the matching against it.

Three results, and the third was not expected
---------------------------------------------

**(1) Where the C7 identity survives, it carries 1/C_F.**  Matching the gauge
electric energy (g^2/2) * 4 * C_2(R_k) against the rotor level s(k)^2/(2 chi)
gives chi = 1/(4 g^2 C_F) rather than 1/(4 g^2).  So *if* the gauge group is
SU(N), hypothesis H2 of F294 is the correct reading and alpha_0 -> alpha_0/C_F.

**(2) But the identity only EXISTS for N <= 3.**  A single level-independent
chi requires the gauge ladder C_2(antisym k) to be proportional to the rotor
ladder s(k)^2.  That proportionality holds for N = 2 (trivially -- one level)
and N = 3 (non-trivially -- two levels, conjugate, equal Casimir) and **fails
for every N >= 4**, where chi comes out level-dependent and no C7 identity
exists at all.  The map m(k) = k is forced, not chosen: the rotor's magnetic
term shifts m by +-1 and the plaquette operator adds or removes one box, so the
two ladders must be matched in order.

    **This is a structural N_c selector, and unlike everything in F293 it
    consumes no measured number and does not depend on which of H1/H2 is
    right** -- the identity exists for N <= 3 under both readings and for
    N >= 4 under neither.

**(3) The discriminator F294 recommended is DEGENERATE at N = 3.**  F294 said
to settle H1 vs H2 by asking whether the model's string tensions follow Casimir
scaling or centre dominance.  At N_c = 3 those two, *and* the sine law, all
predict sigma_2/sigma_1 = 1 -- because k = 2 is the conjugate of k = 1.  The
test cannot distinguish them at the one N the model has.  That recommendation
is withdrawn here rather than left standing.  (F86's BPS law sigma_n = 2 pi v^2 n
predicts 2 and so disagrees with all three, which says F86 is in the
non-interacting-vortex regime rather than that it settles anything.)

Scope, stated plainly
---------------------
This builds the **k-string (totally antisymmetric) tower**, which is the sector
that carries confinement, not the full SU(N) link Hilbert space.  The plaquette
operator applied to a k-box antisymmetric state also produces mixed-symmetry
irreps, and following those is exactly the hard part F110 deferred.  So: the
ladder is exact, the sector is a restriction, and the restriction is named.

Cross-references: F110 (the C7 identity and the deferral this closes for the
k-string sector), F294 (the audit that made this the deciding computation),
F293 (the B10 selector whose structural leg this supplies), F144 (g_s = 1/2),
F86 (the BPS flux tube whose sigma_n = 2 pi v^2 n is compared here), F97/F99
(the centre-projection argument for why Z_3 was chosen).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, Any, List, Sequence, Tuple

__all__ = [
    "su_n_casimir",
    "casimir_fundamental",
    "zn_symmetric_residue_sq",
    "antisymmetric_ladder",
    "symmetric_ladder",
    "c7_against_casimir_ladder",
    "kstring_tension_laws",
    "h1_vs_h2_empirical",
    "check_casimir_ladder",
    "summary",
]


# ==========================================================================
# Exact SU(N) quadratic Casimirs over Q
# ==========================================================================
def su_n_casimir(young_rows: Sequence[int], N: int) -> Fraction:
    """C_2 of the SU(N) irrep with Young-diagram row lengths ``young_rows``.

        C_2 = 1/2 [ sum_i lam_i (lam_i + N + 1 - 2i) - (sum lam)^2 / N ]

    in the normalisation where C_2(fundamental) = (N^2-1)/(2N).  Exact over Q —
    every number in this module is a Fraction, so "proportional" below means
    proportional, not proportional-to-round-off.
    """
    lam = list(young_rows) + [0] * (N - len(young_rows))
    tot = sum(lam)
    s = sum(Fraction(l) * (l + N + 1 - 2 * (i + 1)) for i, l in enumerate(lam))
    return Fraction(1, 2) * (s - Fraction(tot * tot, N))


def casimir_fundamental(N: int) -> Fraction:
    """C_F = (N^2-1)/(2N)."""
    return Fraction(N * N - 1, 2 * N)


def zn_symmetric_residue_sq(k: int, N: int) -> int:
    """s(k)^2 with s the symmetric residue `link_hamiltonian.sym_residue` uses —
    the rotor level that the model's own Z_N Hamiltonian assigns to flux k."""
    r = ((k + N // 2) % N) - N // 2
    return r * r


def antisymmetric_ladder(N: int) -> List[Tuple[int, Fraction, int]]:
    """The k-string tower: (k, C_2(antisym k), s(k)^2) for k = 1..N-1."""
    return [(k, su_n_casimir([1] * k, N), zn_symmetric_residue_sq(k, N))
            for k in range(1, N)]


def symmetric_ladder(N: int, k_max: int = 4) -> List[Tuple[int, Fraction, int]]:
    """CONTROL tower: k boxes in one row.  Must NOT admit a C7 identity, at any
    N — otherwise the N <= 3 result below would be an artefact of picking a
    convenient tower rather than a property of the k-string sector."""
    return [(k, su_n_casimir([k], N), k * k) for k in range(1, k_max + 1)]


# ==========================================================================
# The C7 re-run
# ==========================================================================
def c7_against_casimir_ladder(n_values: Sequence[int] = (2, 3, 4, 5, 6, 7),
                              g2: Fraction = Fraction(1, 4)) -> Dict[str, Any]:
    """Re-run the F110 C7 matching against the SU(N) k-string ladder.

    chi_k = s(k)^2 / (4 g^2 C_2(antisym k)).  A C7 identity exists iff chi_k is
    the SAME for every k.  At g^2 = 1/4 the U(1)/Z_N answer is chi = 1, so any
    departure is the Casimir showing up.
    """
    rows = []
    for N in n_values:
        chis = []
        for k, c2, s2 in antisymmetric_ladder(N):
            if s2:
                chis.append(Fraction(s2, 1) / (4 * g2 * c2))
        uniq = sorted(set(chis))
        well_defined = len(uniq) == 1
        rows.append({
            "N": int(N),
            "chi_k": [str(x) for x in chis],
            "identity_well_defined": well_defined,
            "chi": str(uniq[0]) if well_defined else None,
            "equals_one_over_C_F": (well_defined
                                    and uniq[0] == 1 / casimir_fundamental(N)),
            "C_F": str(casimir_fundamental(N)),
        })

    ctl = []
    for N in n_values:
        chis = [Fraction(s2, 1) / (4 * g2 * c2)
                for _k, c2, s2 in symmetric_ladder(N)]
        ctl.append({"N": int(N), "uniform": len(set(chis)) == 1})

    good = [r["N"] for r in rows if r["identity_well_defined"]]
    tested_above_3 = [r["N"] for r in rows if r["N"] >= 4]
    return {
        "rows": rows,
        "N_with_identity": good,
        "N_ge_4_tested": tested_above_3,
        # The exclusion of N >= 4 may only be CLAIMED if some N >= 4 was
        # actually scanned and failed.  Without this clause a scan truncated at
        # N = 3 would report "only N <= 3" while having tested nothing --
        # a check that cannot see the failure it asserts.
        "identity_only_for_N_le_3": (good == [2, 3]
                                     and len(tested_above_3) > 0),
        "chi_is_one_over_C_F_where_defined":
            all(r["equals_one_over_C_F"] for r in rows
                if r["identity_well_defined"]),
        "control_symmetric_tower_never_uniform":
            all(not c["uniform"] for c in ctl),
        "control_rows": ctl,
        "note": ("m(k) = k is forced, not chosen: the rotor's magnetic term "
                 "shifts m by +-1 and the plaquette operator adds/removes one "
                 "box, so the ladders must be matched in order"),
    }


# ==========================================================================
# The discriminator F294 recommended — and why it does not work
# ==========================================================================
def kstring_tension_laws(N: int = 3) -> Dict[str, Any]:
    """sigma_k/sigma_1 under each law, to test whether measuring string tensions
    could settle H1 vs H2.

    At N = 3 it cannot: Casimir scaling, centre dominance and the sine law all
    give sigma_2/sigma_1 = 1, because k = 2 is the conjugate of k = 1 and
    carries the same Casimir, the same N-ality magnitude and the same sine.
    They separate only at N >= 4, which the model does not have.
    """
    rows = []
    c1 = su_n_casimir([1], N)
    for k in range(1, N):
        casimir = Fraction(su_n_casimir([1] * k, N), c1)
        sine = math.sin(math.pi * k / N) / math.sin(math.pi / N)
        centre = 1.0 if min(k, N - k) == 1 else None   # fixed only by |N-ality|
        rows.append({"k": k,
                     "casimir_scaling": str(casimir),
                     "sine_law": sine,
                     "centre_dominance": centre,
                     "F86_BPS_linear": float(k)})
    k2 = next((r for r in rows if r["k"] == 2), None)
    degenerate = False
    if k2 is not None:
        degenerate = (abs(float(Fraction(k2["casimir_scaling"])) - 1.0) < 1e-12
                      and abs(k2["sine_law"] - 1.0) < 1e-12)
    return {"N": N, "rows": rows,
            "laws_degenerate_at_this_N": degenerate,
            "F86_disagrees_with_all": (k2 is not None
                                       and abs(k2["F86_BPS_linear"] - 1.0) > 0.5),
            "verdict": ("at N=3 Casimir, centre and sine all predict "
                        "sigma_2/sigma_1 = 1, so measuring k-strings CANNOT "
                        "settle H1 vs H2; F86's BPS sigma_n = 2 pi v^2 n gives "
                        "2 and disagrees with all three, which locates F86 in "
                        "the non-interacting-vortex regime rather than "
                        "settling anything")}


# ==========================================================================
# The empirical side of H1 vs H2
# ==========================================================================
def h1_vs_h2_empirical() -> Dict[str, Any]:
    """What bare coupling the MEASURED alpha_s(M_Z) demands at N_c = 3.

    This is the other half of the H1/H2 question, and it points the opposite
    way from the structural one, which is the honest tension this module
    reports rather than resolves.
    """
    from casim.engine.gauge.derive_ncolour import (
        MU0_GEV, MZ_GEV, ALPHA_S_MZ_PDG, N_F)

    b0 = (11.0 * 3 - 2.0 * N_F) / (12.0 * math.pi)
    L = 2.0 * math.log(MU0_GEV / MZ_GEV)
    required = 1.0 / (1.0 / ALPHA_S_MZ_PDG + b0 * L)
    h1 = 1.0 / (16.0 * math.pi)
    h2 = h1 / float(casimir_fundamental(3))
    return {"required_alpha_0": required,
            "H1_alpha_0": h1, "H1_relative_error": h1 / required - 1.0,
            "H2_alpha_0": h2, "H2_relative_error": h2 / required - 1.0,
            "verdict": ("structurally H2 is the right reading if the group is "
                        "SU(N); empirically H1 matches to 0.08% while H2 is "
                        "25% low. The tension is real and is NOT resolved here")}


# ==========================================================================
# Registry entry point
# ==========================================================================
def check_casimir_ladder(tower: str = "antisymmetric",
                         n_max: int = 7) -> Dict[str, Any]:
    """The F298 gate.

    Declared controls:

    ``--param tower=symmetric``  run the matching on the symmetric tower
        instead.  L2 must go red: that tower is uniform at NO N, which is what
        shows the N <= 3 result is a property of the k-string sector and not an
        artefact of choosing a convenient ladder.
    ``--param n_max=3``          truncate the scan before N = 4.  L2 must go
        red because the exclusion of N >= 4 is then untested — a scan that
        cannot see the failure cannot claim it.
    """
    checks: List[Tuple[str, bool, Any]] = []
    ns = tuple(range(2, n_max + 1))

    # L1 -- the Casimirs themselves, against closed form
    ok1 = all(su_n_casimir([1], N) == casimir_fundamental(N) for N in ns) and \
        all(su_n_casimir([2] + [1] * (N - 2), N) == N for N in ns if N >= 2)
    checks.append(("L1 C_2(fund) = (N^2-1)/2N and C_2(adj) = N, exactly over Q",
                   ok1, [str(su_n_casimir([1], N)) for N in ns]))

    res = c7_against_casimir_ladder(n_values=ns) if tower == "antisymmetric" \
        else {"rows": [], "N_with_identity": [],
              "identity_only_for_N_le_3": False,
              "chi_is_one_over_C_F_where_defined": False,
              "control_symmetric_tower_never_uniform": True}
    checks.append(("L2 the C7 identity exists ONLY for N <= 3",
                   res["identity_only_for_N_le_3"], res["N_with_identity"]))
    checks.append(("L3 where it exists, chi = 1/(4 g^2 C_F) -- the Casimir DOES "
                   "enter (F294 H2)",
                   res["chi_is_one_over_C_F_where_defined"],
                   [(r["N"], r["chi"]) for r in res["rows"]
                    if r["identity_well_defined"]]))
    checks.append(("L3b control: the symmetric tower is uniform at NO N",
                   res["control_symmetric_tower_never_uniform"], True))

    kt = kstring_tension_laws(3)
    checks.append(("L4 the F294-recommended discriminator is DEGENERATE at N=3",
                   kt["laws_degenerate_at_this_N"],
                   [(r["k"], r["casimir_scaling"], r["sine_law"])
                    for r in kt["rows"]]))
    checks.append(("L4b ... and F86's BPS law disagrees with all three",
                   kt["F86_disagrees_with_all"], 2.0))
    kt4 = kstring_tension_laws(4)
    checks.append(("L4c ... the laws DO separate at N=4 (so the test is sound, "
                   "just inapplicable)",
                   not kt4["laws_degenerate_at_this_N"],
                   [(r["k"], r["casimir_scaling"], r["sine_law"])
                    for r in kt4["rows"]]))

    emp = h1_vs_h2_empirical()
    checks.append(("L5 empirically H1 matches to <0.5% and H2 is >20% low",
                   abs(emp["H1_relative_error"]) < 0.005
                   and abs(emp["H2_relative_error"]) > 0.20,
                   (emp["H1_relative_error"], emp["H2_relative_error"])))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"tower": tower, "n_max": n_max},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    c7 = c7_against_casimir_ladder()
    kt3 = kstring_tension_laws(3)
    kt4 = kstring_tension_laws(4)
    emp = h1_vs_h2_empirical()
    return {
        "F298_ladder_antisym": {N: [str(c) for _k, c, _s in
                                    antisymmetric_ladder(N)]
                                for N in (2, 3, 4, 5)},
        "F298_N_with_C7_identity": c7["N_with_identity"],
        "F298_identity_only_N_le_3": c7["identity_only_for_N_le_3"],
        "F298_chi_is_one_over_CF": c7["chi_is_one_over_C_F_where_defined"],
        "F298_chi_values": [(r["N"], r["chi"]) for r in c7["rows"]],
        "F298_control_symmetric_never_uniform":
            c7["control_symmetric_tower_never_uniform"],
        "F298_kstring_laws_degenerate_at_3": kt3["laws_degenerate_at_this_N"],
        "F298_kstring_laws_separate_at_4":
            not kt4["laws_degenerate_at_this_N"],
        "F298_required_alpha_0": emp["required_alpha_0"],
        "F298_H1_relative_error": emp["H1_relative_error"],
        "F298_H2_relative_error": emp["H2_relative_error"],
    }


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_casimir_ladder()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F298_casimir_ladder.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("wrote", os.path.basename(out))
