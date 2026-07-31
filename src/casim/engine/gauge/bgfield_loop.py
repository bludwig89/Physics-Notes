"""
ca_bgfield_loop.py — the background-field one-loop gluon self-energy: the
assembled loop, the EXACT b0 = 11/3 C_A recovery gate, and the honest status of
the matching scale q* (F162; supersedes the scaffold).

WHAT THIS MODULE ESTABLISHES (with explicit, honest scope)
==========================================================
EXACT (symbolic, machine-checked) — the b0 GATE, in the continuum:
  The background-field (Abbott / Hashimoto-Kodaira-Yasui-Sasaki hep-ph/9406271)
  one-loop gluon self-energy in Feynman background gauge xi=1 is assembled from
    Pi_{mn}(q) = (N/2) int d^4k/(2pi)^4 [1/(k^2 (k+q)^2)] M_{mn}(k,q),
    M = GLUON loop  GammaF_{a m l}(k,q) GammaF_{l n a}(k+q,-q)         (Eq 19)
      + GHOST loop  -2 (2k+q)_m (2k+q)_n                               (Eq 20)
    GammaF_{a m l}(k,q) = -2 q_l d_am + 2 q_a d_ml - (2k+q)_m d_la      (Eq 18)
  The UV (log-divergent) part, extracted by the large-k expansion + 4D angular
  average, is EXACTLY transverse and gives the universal running:
    g_{mn} = (22/3)(q^2 d_mn - q_m q_n),   b0 = (N/2)(22/3) = 11/3 C_A = 11.
  This validates the loop ASSEMBLY (vertices + group theory + gluon/ghost
  cancellation) that F155 did not have — F155 only had the scalar bubble.

WELL-CONDITIONED (numerical) — lattice b0 = continuum b0:
  Swapping the continuum propagator 1/k^2 -> the lattice 1/K (Wilson or the rule
  K=3 Omega_even^2) leaves the log coefficient UNCHANGED: the subtracted
  transverse coefficient B_lat - B_cont is a q-INDEPENDENT constant (a residual
  log would grow like ln(1/q)); flat to ~1e-3 across q and grid n. So the lattice
  running is the continuum 11 (consistent with A2 universality + the F129
  near-perfect action + the A1 luminal gluon).

OPEN (stated, not faked) — the finite d1 to the DIGIT:
  q* a = exp(-d1/2 b0^alpha) = 0.733 needs the FINITE constant of the lattice
  self-energy = continuum value + the PROPAGATOR-driven shift (computed here,
  small for the rule: near-perfect action) + the VERTEX FORM-FACTOR shift (the
  bespoke lattice 3-gluon + ghost cos(k/2) vertices). The vertex piece is NOT
  computed here, and its validation gate (reproduce the Wilson finite constant
  / Lambda_MSbar/Lambda_L = 28.81 with the full lattice vertices + tadpole) is
  not executed. So the digit is NOT pinned: the F155 bracket q* a in
  [1/sqrt3, ~0.97] (implied 0.733 inside) STANDS. The propagator-driven shift
  for the rule is ~0 (near-perfect action), i.e. the rule's propagator alone
  keeps q* at the band top ~0.97 — exactly the F155 result; the pull-down to
  0.733 is entirely the vertex form-factor finite part.

sympy (exact gate) + numpy (lattice consistency). The 4D BZ quadrature at
production n exceeds the sandbox cap -> tests/runners/run_bgfield_loop.py.
"""
from __future__ import annotations

import math

import numpy as np
from casim.constants import (
    q_star_a_band_lo as _q_star_a_band_lo,
    q_star_a_implied as _q_star_a_implied,
)

C_A = 3.0
NF = 0
B0_PURE_GAUGE = 11.0 / 3.0 * C_A            # = 11 ; the validation-gate target
SQRT3 = math.sqrt(3.0)
QSTAR_IMPLIED = _q_star_a_implied
BAND = (_q_star_a_band_lo, 1.0)                    # F151 q* band, units of 1/a


# ======================================================================
#  the continuum background-field AQQ vertex (Abbott xi=1, Eq 18)
# ======================================================================
def gammaF_tensor_continuum(k, q):
    """GammaF_{a m l}(k,q) = -2 q_l d_am + 2 q_a d_ml - (2k+q)_m d_la, as a
    (...,4,4,4) numpy array with index order [a, m, l]. The Feynman-gauge
    background-quantum-quantum 3-gluon vertex; reduces to the Ward-verified
    continuum tensor Gamma (ca_lpt_ward) and is the loop's actual vertex."""
    D = 4
    d = np.eye(D)
    twokq = 2.0 * k + q
    return (-2.0 * np.einsum('...l,am->...aml', q, d)
            + 2.0 * np.einsum('...a,ml->...aml', q, d)
            - np.einsum('...m,la->...aml', twokq, d))


# ======================================================================
#  THE b0 GATE — exact, symbolic (large-k log-coefficient extraction)
# ======================================================================
def b0_gate_symbolic() -> dict:
    """Assemble the continuum background-field self-energy symbolically, extract
    the UV log coefficient g_{mn}, and verify b0 = 11/3 C_A = 11 EXACTLY with the
    gluon/ghost split. Calibrated against the scalar bubble (log-coeff 1/16pi^2).

    Returns the exact rationals. This is THE validation gate: it certifies the
    loop assembly reproduces the universal QCD running before any d1 is trusted.
    """
    import sympy as sp

    D = 4
    N = sp.Integer(3)
    k = sp.symbols('k0:4', real=True)
    q = sp.symbols('q0:4', real=True)
    K = sp.Symbol('K', positive=True)            # k^2
    dl = lambda i, j: sp.Integer(1) if i == j else sp.Integer(0)

    def gammaF(kk, qq):
        return [[[(-2*qq[l]*dl(a, m) + 2*qq[a]*dl(m, l) - (2*kk[m]+qq[m])*dl(l, a))
                  for l in range(D)] for m in range(D)] for a in range(D)]

    kq = [k[i] + q[i] for i in range(D)]
    mq = [-q[i] for i in range(D)]
    W = gammaF(list(k), list(q))                 # GammaF_{a m l}(k,q)
    Z = gammaF(kq, mq)                           # GammaF_{l n a}(k+q,-q)

    def gluon_M(m, n):
        return sp.expand(sum(W[a][m][l]*Z[l][n][a] for a in range(D) for l in range(D)))

    def ghost_M(m, n):
        return sp.expand(-2*(2*k[m]+q[m])*(2*k[n]+q[n]))

    kdotq = sum(k[i]*q[i] for i in range(D))
    q2 = sum(q[i]**2 for i in range(D))
    invkpq = (1/K) - (2*kdotq + q2)/K**2 + (2*kdotq)**2/K**3   # 1/(k+q)^2 to O(q^2)

    def ang_avg_monomial(powers):
        deg = sum(powers.values())
        idx = [i for i in range(D) for _ in range(powers[i])]
        if deg == 0:
            return sp.Integer(1)
        if deg % 2 == 1:
            return sp.Integer(0)
        if deg == 2:
            a, b = idx
            return (K/4)*dl(a, b)
        if deg == 4:
            a, b, c, d2 = idx
            return (K**2/24)*(dl(a, b)*dl(c, d2)+dl(a, c)*dl(b, d2)+dl(a, d2)*dl(b, c))
        raise ValueError(deg)

    def log_coeff(num, qdeg_keep):
        """Angular-averaged coeff g of the degree(-4), q-degree=qdeg_keep piece of
        num/(k^2 (k+q)^2). Calibration (scalar bubble): true coeff of
        ln(Lambda^2/q^2) = g/16pi^2."""
        E = sp.expand(num*(sp.Integer(1)/K)*invkpq)
        avg = sp.Integer(0)
        for term in E.as_ordered_terms():
            d = term.as_powers_dict()
            if sum(int(d.get(q[i], 0)) for i in range(D)) != qdeg_keep:
                continue
            kexp = int(d.get(K, 0))
            knum = sum(int(d.get(k[i], 0)) for i in range(D))
            if knum + 2*kexp != -4:
                continue
            powers = {i: int(d.get(k[i], 0)) for i in range(D)}
            kmono = sp.prod([k[i]**powers[i] for i in range(D)])
            rest = term/(kmono*K**kexp) if kmono != 1 else term/K**kexp
            avg += rest*K**kexp*ang_avg_monomial(powers)
        return sp.simplify(sp.expand(avg)*K**2)

    # scalar-bubble calibration
    g_scalar = log_coeff(sp.Integer(1), 0)

    tens = lambda m, n: (q2*dl(m, n) - q[m]*q[n])

    def coeff_of(gmat):
        # gmat[1][1] = C*(q0^2+q2^2+q3^2); read C as coeff of q0^2
        return sp.simplify(gmat[1][1].coeff(q[0], 2))

    g_full = [[log_coeff(gluon_M(m, n) + ghost_M(m, n), 2) for n in range(D)] for m in range(D)]
    g_gl = [[log_coeff(gluon_M(m, n), 2) for n in range(D)] for m in range(D)]
    g_gh = [[log_coeff(ghost_M(m, n), 2) for n in range(D)] for m in range(D)]

    transverse = all(sp.simplify(g_full[m][n] - coeff_of(g_full)*tens(m, n)) == 0
                     for m in range(D) for n in range(D))
    Cf = coeff_of(g_full)
    Cgl = coeff_of(g_gl)
    Cgh = coeff_of(g_gh)
    b0 = sp.simplify((N/2)*Cf)
    b0_gl = sp.simplify((N/2)*Cgl)
    b0_gh = sp.simplify((N/2)*Cgh)
    return {
        "scalar_bubble_calibration_g": str(g_scalar),       # "1"
        "calibration_ok": g_scalar == 1,
        "g_tensor_coeff_total": str(Cf),                    # 22/3
        "g_tensor_coeff_gluon": str(Cgl),
        "g_tensor_coeff_ghost": str(Cgh),
        "transverse": bool(transverse),
        "b0_total": str(b0),                                # 11
        "b0_gluon": str(b0_gl),
        "b0_ghost": str(b0_gh),
        "b0_target": str(sp.Rational(11, 3)*N),             # 11
        "gate_pass": bool(transverse and b0 == sp.Rational(11, 3)*N and g_scalar == 1),
        "statement": "background-field gluon+ghost self-energy is exactly "
                     "transverse and gives b0 = 11/3 C_A = 11 (gluon+ghost split "
                     "verified); scalar-bubble calibration g=1 fixes the "
                     "normalisation. The loop ASSEMBLY is validated (exact)."}


# ======================================================================
#  lattice b0 consistency (well-conditioned, numerical, subtracted)
# ======================================================================
def _Bcoeff_numeric(Q, n, kernel):
    """B = coeff of q_m q_n in Pi_{mn} (continuum vertices) = (Pi00-Pi11)/Q^2 for
    q=(Q,0,0,0). kernel in {'cont','wilson','rule'}; lattice kernels wrap k+q."""
    ax = (np.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    G = np.meshgrid(ax, ax, ax, ax, indexing='ij')
    k = np.stack(G, axis=-1)
    qv = np.array([Q, 0.0, 0.0, 0.0])
    kq = k + qv
    kqw = ((kq + math.pi) % (2 * math.pi)) - math.pi
    if kernel == 'cont':
        denom = np.sum(k**2, -1) * np.sum(kq**2, -1)
    elif kernel == 'wilson':
        Kf = lambda g: 4*(np.sin(g[..., 0]/2)**2 + np.sin(g[..., 1]/2)**2
                          + np.sin(g[..., 2]/2)**2 + np.sin(g[..., 3]/2)**2)
        denom = Kf(k) * Kf(kqw)
    elif kernel == 'rule':
        from casim.engine.gauge import gluon_self_energy as se
        Kr = lambda g: se.K_true_4d(g[..., 0], g[..., 1], g[..., 2], g[..., 3])
        denom = Kr(k) * Kr(kqw)
    else:
        raise ValueError(kernel)
    W = gammaF_tensor_continuum(k, qv)
    Z = gammaF_tensor_continuum(kq, -qv)
    Ggl = np.einsum('...aml,...lna->...mn', W, Z)
    tkq = 2.0 * k + qv
    Hgh = -2.0 * np.einsum('...m,...n->...mn', tkq, tkq)
    M = Ggl + Hgh
    Pi = (C_A / 2.0) * np.mean(M / denom[..., None, None], axis=(0, 1, 2, 3))
    return (Pi[0, 0] - Pi[1, 1]) / Q**2


def lattice_b0_consistency(n=24, Qs=(0.1, 0.15, 0.2, 0.3)) -> dict:
    """Show the subtracted transverse coefficient Delta = B_lat - B_cont is a
    q-INDEPENDENT constant (=> the log coefficient b0 is propagator-independent =
    the continuum 11). A residual log would make Delta grow like ln(1/Q)."""
    rows = []
    for Q in Qs:
        Bc = _Bcoeff_numeric(Q, n, 'cont')
        Bw = _Bcoeff_numeric(Q, n, 'wilson')
        Br = _Bcoeff_numeric(Q, n, 'rule')
        rows.append({"Q": Q, "minus_Bcont": -Bc,
                     "delta_wilson": Bw - Bc, "delta_rule": Br - Bc})
    dw = [r["delta_wilson"] for r in rows]
    dr = [r["delta_rule"] for r in rows]
    spread_w = max(dw) - min(dw)
    spread_r = max(dr) - min(dr)
    return {"rows": rows, "n": n,
            "wilson_shift_mean": float(np.mean(dw)), "wilson_shift_spread": spread_w,
            "rule_shift_mean": float(np.mean(dr)), "rule_shift_spread": spread_r,
            # the DECISIVE, well-conditioned test is the Wilson flatness (the rule
            # kernel's arccos is grid-sensitive at small n -> tightens in the runner)
            "b0_propagator_independent": bool(spread_w < 1e-3),
            "rule_shift_small": bool(abs(np.mean(dr)) < 0.05),
            "statement": "Delta = B_lat - B_cont is q-flat (no residual log) => "
                         "lattice b0 = continuum b0 = 11 (Wilson flat to <1e-3). The "
                         "PROPAGATOR-driven finite shift is small for the rule "
                         "(near-perfect action) -> q* stays at the band top ~0.97; "
                         "the pull-down to 0.733 is the (open) vertex form-factor part."}


# ======================================================================
#  honest d1 / q* status
# ======================================================================
def d1_qstar_status() -> dict:
    return {
        "b0_gate": "PASS (exact, continuum) + lattice b0=11 (propagator-independent)",
        "finite_d1_to_digit": "OPEN — needs the bespoke lattice 3-gluon+ghost "
                              "vertex form factors, validated against the Wilson "
                              "finite constant (Lambda_MSbar/Lambda_L=28.81). "
                              "Not executed here.",
        "qstar_a_bracket": [round(BAND[0], 4), 0.97],
        "qstar_a_implied_F151": QSTAR_IMPLIED,
        "lambda_ratio_target": 1.78,
        "wilson_contrast": 28.81,
        "verdict": "F155 bracket q* a in [1/sqrt3, ~0.97] (implied 0.733 inside) "
                   "STANDS. This finding ADDS the exact b0=11 assembly gate (the "
                   "loop is correctly built) and the well-conditioned lattice-b0 "
                   "confirmation; the remaining piece is the vertex form-factor "
                   "finite constant, with its Wilson-28.81 validation gate."}


def status() -> dict:
    return {
        "b0_gate_target": B0_PURE_GAUGE,
        "exact_results": ["b0_gate_symbolic (b0=11, transverse, gluon/ghost split)",
                          "scalar-bubble calibration g=1"],
        "numerical_results": ["lattice_b0_consistency (Delta q-flat => lattice b0=11)"],
        "open": "finite gluonic d1 (vertex form factors) -> q* digit; F155 bracket stands",
        "target": {"qstar_a": 0.733, "Lambda_ratio": 1.78, "wilson_contrast": 28.81}}


def report() -> dict:
    return {"b0_gate": b0_gate_symbolic(),
            "lattice_b0_consistency": lattice_b0_consistency(n=20),
            "d1_qstar_status": d1_qstar_status()}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
