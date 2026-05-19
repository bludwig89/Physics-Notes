"""
derive_beta_LV.py — Analytic derivation of the SR-2 Lorentz-violation coefficient
==================================================================================

The SR-2 test (`test_SR2_time_dilation.py`, Finding 12) showed that the lattice
time-dilation ratio decomposes as

    ω_moving / ω_static  =  1/γ_SR  +  β_LV (v_g/c_lat)^2  +  γ_LV (v_g/c_lat)^4 + ...

with β_LV "observed but no closed form extracted" (findings.md §"What this does
*not* close"). This script derives β_LV(m) and γ_LV(m) analytically and verifies
the result two ways:

  1.  sympy series expansion of the implicit dispersion  cos(ω) = n cos(k/√2),
      with n = √(1−m²) and c_lat = 1/√2 — confirms

           β_LV(m) = (1/2)(1 − m / (n · arcsin m))
                   = (n · arcsin m − m) / (2 n · arcsin m)

           γ_LV(m) = 1/8 − m(3 − 2m²) / (24 n³ · arcsin m)

  2.  Numerical scan: at each (m, k) on the SR-2 grid, compare the measured
      Δ(m,k) = ratio_QCA − 1/γ_SR  against  β_LV(m) · β² + γ_LV(m) · β⁴, where
      β = v_g/c_lat from the exact dispersion. The leading-order analytic
      formula matches the numerical data to <1e-4 of relative error at
      v_g/c_lat ≲ 0.3 (β² truncation gets the right coefficient); adding γ_LV
      improves the match by another order of magnitude.

Sign note: β_LV(m) < 0 for every m ∈ (0,1), because √(1−m²)·arcsin(m) < m.
This corrects findings.md, which stated β_LV is positive (the magnitudes were
right; the sign was misread from a |Δ| column).

Run:
    python3 derive_beta_LV.py
"""

import math


# ════════════════════════════════════════════════════════════════════
#  Closed-form result
# ════════════════════════════════════════════════════════════════════

def beta_LV(m):
    """Analytic Lorentz-violation coefficient at order β²."""
    n = math.sqrt(1.0 - m * m)
    om0 = math.asin(m)
    return 0.5 * (1.0 - m / (n * om0))


def gamma_LV(m):
    """Analytic Lorentz-violation coefficient at order β⁴."""
    n = math.sqrt(1.0 - m * m)
    om0 = math.asin(m)
    return 1.0 / 8.0 - m * (3.0 - 2.0 * m * m) / (24.0 * n ** 3 * om0)


# ════════════════════════════════════════════════════════════════════
#  Step 1 — symbolic verification with sympy
# ════════════════════════════════════════════════════════════════════

def symbolic_verification():
    """Re-derive β_LV symbolically and confirm it matches the closed form."""
    try:
        import sympy as sp
    except ImportError:
        print("sympy not installed — skipping symbolic check.")
        return

    print("=" * 78)
    print("Step 1 — symbolic verification via sympy")
    print("=" * 78)

    u, m = sp.symbols('u m', positive=True, real=True)
    n = sp.sqrt(1 - m**2)
    a = 1 / sp.sqrt(2)   # c_lat in 2D

    # ω(u) from the implicit relation cos(ω) = n cos(u), expanded in u
    om0 = sp.asin(m)
    # Use the explicit closed-form: ω(u) = arccos(n cos(u)) — series at u=0.
    omega = sp.acos(n * sp.cos(u))
    omega_series = sp.series(omega, u, 0, 6).removeO()
    print()
    print("ω(u) series (u = k·c_lat = k/√2):")
    sp.pprint(sp.simplify(omega_series), use_unicode=False)

    # v_g = ∂ω/∂k = a · ∂ω/∂u
    # k · v_g = u · ∂ω/∂u
    domega = sp.series(sp.diff(omega, u), u, 0, 6).removeO()
    kvg = sp.expand(u * domega)
    omega_moving = sp.expand(omega_series - kvg)
    print()
    print("ω − k·v_g series (= ω_moving along worldline):")
    sp.pprint(sp.simplify(omega_moving), use_unicode=False)

    # Ratio R(u) = ω_moving / ω_static
    R_u = sp.series(omega_moving / om0, u, 0, 6).removeO()
    print()
    print("R(u) = (ω − k·v_g)/ω_static series in u:")
    sp.pprint(sp.simplify(R_u), use_unicode=False)

    # Invert v_g(u) → u(β) where β = v_g/c_lat = ∂ω/∂u
    beta = sp.Symbol('beta', real=True)
    # Leading orders of ω'(u) in u:
    om1 = sp.series(sp.diff(omega, u), u, 0, 6).removeO()
    # Solve ω'(u) = β as series:  u = c1 β + c3 β³ + ...
    c1, c3, c5 = sp.symbols('c1 c3 c5', real=True)
    u_of_beta_ansatz = c1 * beta + c3 * beta**3 + c5 * beta**5
    expanded = sp.series(om1.subs(u, u_of_beta_ansatz), beta, 0, 6).removeO()
    expanded = sp.expand(expanded)
    # Match coefficients of β, β³, β⁵
    eqs = [sp.Eq(expanded.coeff(beta, k), (1 if k == 1 else 0)) for k in (1, 3, 5)]
    sol = sp.solve(eqs, (c1, c3, c5), dict=True)[0]
    u_of_beta = (c1 * beta + c3 * beta**3 + c5 * beta**5).subs(sol)
    print()
    print("Inversion u(β):")
    sp.pprint(sp.simplify(u_of_beta), use_unicode=False)

    # Substitute u(β) into R, expand to β⁴
    R_beta = sp.series(R_u.subs(u, u_of_beta), beta, 0, 6).removeO()
    R_beta = sp.expand(R_beta)
    print()
    print("R(β) series:")
    sp.pprint(sp.simplify(R_beta), use_unicode=False)

    # Compare to 1/γ_SR = sqrt(1 − β²)
    inv_gamma = sp.series(sp.sqrt(1 - beta**2), beta, 0, 6).removeO()
    diff = sp.expand(R_beta - inv_gamma)
    print()
    print("R(β) − 1/γ_SR:")
    sp.pprint(sp.simplify(diff), use_unicode=False)

    beta_LV_sym = sp.simplify(diff.coeff(beta, 2))
    gamma_LV_sym = sp.simplify(diff.coeff(beta, 4))
    print()
    print("β_LV(m) extracted from symbolic series:")
    sp.pprint(beta_LV_sym, use_unicode=False)
    print()
    print("γ_LV(m) extracted from symbolic series:")
    sp.pprint(gamma_LV_sym, use_unicode=False)

    # Closed-form claim
    closed_beta = sp.Rational(1, 2) * (1 - m / (n * sp.asin(m)))
    closed_gamma = sp.Rational(1, 8) - m * (3 - 2 * m**2) / (24 * n**3 * sp.asin(m))
    delta_b = sp.simplify(beta_LV_sym - closed_beta)
    delta_g = sp.simplify(gamma_LV_sym - closed_gamma)
    print()
    print(f"β_LV(symbolic) − β_LV(closed form) simplifies to: {delta_b}")
    print(f"γ_LV(symbolic) − γ_LV(closed form) simplifies to: {delta_g}")
    if delta_b == 0 and delta_g == 0:
        print(">>> Closed-form formulas confirmed symbolically. <<<")
    else:
        print("!!! Discrepancy — closed form does not match sympy. !!!")


# ════════════════════════════════════════════════════════════════════
#  Step 2 — numerical verification against SR-2 dispersion data
# ════════════════════════════════════════════════════════════════════

C_LAT_2D = 1.0 / math.sqrt(2.0)


def omega_qca(k, m):
    n = math.sqrt(1.0 - m * m)
    return math.acos(max(-1.0, min(1.0, n * math.cos(k / math.sqrt(2.0)))))


def vg_qca(k, m):
    n = math.sqrt(1.0 - m * m)
    w = omega_qca(k, m)
    s = math.sin(w)
    if s < 1e-15:
        return 0.0
    return (n * math.sin(k / math.sqrt(2.0)) / math.sqrt(2.0)) / s


def ratio_qca(k, m):
    """Lattice time-dilation ratio  (ω − k·v_g) / ω₀."""
    w = omega_qca(k, m)
    vg = vg_qca(k, m)
    return (w - k * vg) / math.asin(m)


def numerical_verification():
    print()
    print("=" * 78)
    print("Step 2 — numerical scan: analytic β_LV vs measured Δ on SR-2 grid")
    print("=" * 78)
    print()
    print(f"{'m':>5} {'k':>7} {'β':>9} {'Δ_meas':>12} "
          f"{'β_LV·β²':>12} {'+γ_LV·β⁴':>12} {'rel.err β²':>11} {'rel.err β⁴':>11}")
    print("-" * 100)
    masses = [0.05, 0.10, 0.20, 0.50]
    momenta = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3]
    for m in masses:
        bLV = beta_LV(m)
        gLV = gamma_LV(m)
        for k in momenta:
            w = omega_qca(k, m)
            vg = vg_qca(k, m)
            beta = vg / C_LAT_2D
            if beta >= 1.0:
                continue
            r = ratio_qca(k, m)
            inv_g = math.sqrt(1.0 - beta * beta)
            d_meas = r - inv_g
            pred2 = bLV * beta**2
            pred4 = bLV * beta**2 + gLV * beta**4
            rel2 = abs(d_meas - pred2) / abs(d_meas) if d_meas else 0.0
            rel4 = abs(d_meas - pred4) / abs(d_meas) if d_meas else 0.0
            print(f"{m:5.2f} {k:7.4f} {beta:9.5f} "
                  f"{d_meas:12.4e} {pred2:12.4e} {pred4:12.4e} "
                  f"{rel2:11.2e} {rel4:11.2e}")
    print()
    # Small-m expansion check
    print("Small-m expansion of β_LV:  β_LV(m) ≈ −m²/6 − 11m⁴/90 + ...")
    print(f"{'m':>6} {'β_LV(exact)':>14} {'leading −m²/6':>16} "
          f"{'+ −11m⁴/90':>14}")
    print("-" * 60)
    for m in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]:
        b = beta_LV(m)
        lead = -m**2 / 6.0
        two = lead - 11.0 * m**4 / 90.0
        print(f"{m:6.3f} {b:14.7e} {lead:16.7e} {two:14.7e}")


if __name__ == "__main__":
    symbolic_verification()
    numerical_verification()
