# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_euler_heisenberg.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qed_euler_heisenberg.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_euler_heisenberg.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_euler_heisenberg.py — the nonlinear corner of QED (F263): the one-loop
Euler-Heisenberg effective Lagrangian, light-by-light scattering
gamma gamma -> gamma gamma, and strong-field vacuum birefringence.

This is the SAME electron loop that F251 (ca_vacuum_polarization.py) uses for the
photon self-energy Pi^{mn} (two external photon legs, the bubble), now taken with
FOUR external photon legs (the box) in the low-frequency / constant-field limit.
Integrating out the electron in a constant background gives the effective action
whose leading four-field term is the Euler-Heisenberg Lagrangian. The external
photons are the F69/F250 even-law paired photon (single massless transverse gauge
pole across the BZ); the four-photon amplitude built here is EXACTLY transverse on
every leg (each photon enters only through f^i_{mn} = k^i_m eps^i_n - k^i_n eps^i_m,
which vanishes when eps^i -> k^i), so the F250 gauge structure is preserved.

F249-B1 confirmed zero *linear* vacuum birefringence (a free paired photon does not
split). Euler-Heisenberg gives the *nonlinear*, field-induced birefringence — the
physical, non-zero effect (a probe photon in a strong background B), distinct from
and consistent with the free-photon result.

WHAT THIS MODULE ESTABLISHES (explicit scope)
=============================================
EXACT (symbolic, sympy):

  EH1  eh_coefficients_symbolic():  from the Schwinger proper-time one-loop
       determinant in a constant background, the weak-field expansion of the
       secular integrand (x coth x)(y cot y) - 1 - (x^2 - y^2)/3 to fourth order,
       integrated with int_0^inf s e^{-m^2 s} ds = 1/m^4, gives EXACTLY

         L_EH = (2 alpha^2 / 45 m^4) [ (E^2 - B^2)^2 + 7 (E.B)^2 ].

       Both the coefficient 2 alpha^2 / 45 AND the relative weight 7 (the box
       result) fall out. In the invariant basis L = c_F (cal F)^2 + c_G (cal G)^2
       the weights are 8/45 : 14/45 = 4 : 7.  Rational-exact.

  EH2  light_by_light_cross_section():  the contact four-photon vertex read off
       from L_EH, contracted with physical CM kinematics and summed over the 16
       linear-polarisation configurations, integrated over solid angle with the
       identical-particle factor, gives the low-energy Karplus-Neuman cross
       section EXACTLY:

         sigma(gamma gamma -> gamma gamma) = (973 / 10125 pi) alpha^4 omega^6 / m^8

       (omega = CM energy per photon, omega << m). Symbolic-exact (the angular
       integral closes to a rational times 1/pi).

  EH3  ward_and_bose_gates():  the four-photon amplitude vanishes identically
       when any polarisation eps^i -> its momentum k^i (Ward on every leg, exact
       literal 0) and is invariant under exchange of any two photons (Bose). Both
       are exact gates, the four-leg counterpart of F251's two-leg Ward identity.

  EH4  birefringence_ratio_symbolic():  expanding L_EH to second order in a probe
       field about a constant background B, the two probe eigen-polarisations
       (E parallel vs perpendicular to B) acquire refractive-index shifts in the
       ratio 7 : 4 EXACTLY:

         n_par - 1 = (7/2)(2 alpha^2/45)(B^2/m^4),
         n_perp - 1 = (4/2)(2 alpha^2/45)(B^2/m^4).

       This is the nonlinear counterpart of F249-B1's zero *linear* birefringence.

QUANTITATIVE (numeric, honest scope):
  EH5  observational_contact():  the ATLAS Pb+Pb observation of light-by-light
       scattering (Nature Phys. 13, 852, 2017) is the measured contact point; the
       low-energy coefficient above is the pole-mass limit, the full box (all
       omega) is the ATLAS regime. Stated, not fit.

sympy (exact gates) + closed forms. No np.linalg.eig on chiral matrices
(CLAUDE.md): everything here is real tensor contraction of the f^i_{mn} field
strengths and rational angular averages.

References: Heisenberg-Euler Z.Phys. 98, 714 (1936); Weisskopf (1936);
Karplus-Neuman Phys.Rev. 83, 776 (1951) (the 973/10125 cross section);
Adler Ann.Phys. 67, 599 (1971) (birefringence); Dunne hep-th/0406216 (review);
ATLAS Nature Phys. 13, 852 (2017).
"""
from __future__ import annotations

import math

# CODATA 2022 / PDG reference constants
ALPHA_INV = 137.035999177
ALPHA = 1.0 / ALPHA_INV
M_E_MEV = 0.51099895069

# targets (exact rationals / literature)
EH_PREFACTOR_NUM = (2, 45)          # 2/45 (times alpha^2/m^4)
EH_INVARIANT_WEIGHT = 7             # (E.B)^2 relative to (E^2-B^2)^2
LBL_COEFF = (973, 10125)            # 973/(10125 pi) alpha^4 omega^6/m^8
BIREFRINGENCE_RATIO = (7, 4)        # n_par-1 : n_perp-1


# ======================================================================
#  EH1 — Euler-Heisenberg coefficients (proper-time weak-field expansion)
# ======================================================================
def eh_coefficients_symbolic() -> dict:
    """Derive L_EH = (2 alpha^2/45 m^4)[(E^2-B^2)^2 + 7(E.B)^2] from the Schwinger
    proper-time one-loop determinant.

    The renormalised constant-field effective Lagrangian is
      L = -(1/8pi^2) int_0^inf ds/s^3 e^{-m^2 s}
              [ e^2 s^2 a b coth(e a s) cot(e b s) - 1 - (e^2 s^2/3)(a^2 - b^2) ],
    with secular invariants a^2 - b^2 = 2 cal F = B^2 - E^2, a^2 b^2 = cal G^2,
    cal F = (1/4)F.F, cal G = (1/4)F.Ftilde. Writing x = e a s, y = e b s the
    integrand core is (x coth x)(y cot y) - 1 - (x^2 - y^2)/3; its weak-field
    (fourth-order) part, integrated with int_0^inf s e^{-m^2 s} ds = 1/m^4 and
    e^4 = 16 pi^2 alpha^2, yields the coefficients. Returns exact rationals."""
    import sympy as sp

    x, y = sp.symbols("x y", positive=True)
    a, b, m, al = sp.symbols("a b m alpha", positive=True)

    # secular integrand core, series to 4th order in the fields (6th in x,y series)
    core = (sp.series(x * sp.coth(x), x, 0, 6).removeO()
            * sp.series(y * sp.cot(y), y, 0, 6).removeO())
    core = sp.expand(core - 1 - (x ** 2 - y ** 2) / 3)
    c_x4 = core.coeff(x, 4).coeff(y, 0)         # -1/45
    c_y4 = core.coeff(y, 4).coeff(x, 0)         # -1/45
    c_x2y2 = core.coeff(x, 2).coeff(y, 2)       # -1/9

    # I(s) = e^4 s^4 [ c_x4 a^4 + c_y4 b^4 + c_x2y2 a^2 b^2 ]
    # L = -(1/8pi^2) * I_coef * (e^4/m^4) with the s-integral giving 1/m^4
    Icoef = c_x4 * a ** 4 + c_y4 * b ** 4 + c_x2y2 * a ** 2 * b ** 2
    L = sp.expand(-sp.Rational(1, 8) / sp.pi ** 2 * Icoef
                  * (16 * sp.pi ** 2 * al ** 2) / m ** 4)

    # collect on secular invariants: a^4 + b^4 = 4 F^2 + 2 G^2, a^2 b^2 = G^2
    cA = sp.simplify(L.coeff(a, 4).coeff(b, 0))          # coeff of a^4 = b^4
    cAB = sp.simplify(sp.expand(L - cA * a ** 4 - cA * b ** 4)
                      .coeff(a, 2).coeff(b, 2))          # coeff of a^2 b^2
    coeff_F2 = sp.simplify(4 * cA)                       # -> 8/45
    coeff_G2 = sp.simplify(2 * cA + cAB)                 # -> 14/45

    # physical basis: (E^2-B^2)^2 = 4 F^2, (E.B)^2 = G^2
    coeff_EmB = sp.simplify(coeff_F2 / 4)                # coeff of (E^2-B^2)^2
    coeff_EdotB = sp.simplify(coeff_G2)                  # coeff of (E.B)^2
    weight = sp.simplify(coeff_EdotB / coeff_EmB)        # -> 7

    prefactor = sp.simplify(coeff_EmB / (al ** 2 / m ** 4))   # -> 2/45
    target_pref = sp.Rational(*EH_PREFACTOR_NUM)
    gate = (prefactor == target_pref
            and weight == EH_INVARIANT_WEIGHT
            and sp.simplify(coeff_F2 / (al ** 2 / m ** 4)) == sp.Rational(8, 45)
            and sp.simplify(coeff_G2 / (al ** 2 / m ** 4)) == sp.Rational(14, 45))

    return {
        "series_coeffs": {"x4": str(c_x4), "y4": str(c_y4), "x2y2": str(c_x2y2)},
        "coeff_EmB2_over_a2m4": str(prefactor),       # 2/45
        "coeff_EdotB2_over_a2m4": str(sp.simplify(coeff_EdotB / (al ** 2 / m ** 4))),
        "invariant_weight": str(weight),              # 7
        "coeff_F2_over_a2m4": str(sp.simplify(coeff_F2 / (al ** 2 / m ** 4))),   # 8/45
        "coeff_G2_over_a2m4": str(sp.simplify(coeff_G2 / (al ** 2 / m ** 4))),   # 14/45
        "invariant_basis_ratio": "8/45 : 14/45 = 4 : 7",
        "L_EH": "(2 alpha^2/45 m^4)[(E^2-B^2)^2 + 7 (E.B)^2]",
        "gate_pass": bool(gate),
        "statement": "Euler-Heisenberg coefficient 2 alpha^2/45 and the box-diagram "
                     "invariant weight 7 both derived exactly from the proper-time "
                     "one-loop determinant (sympy). The 7 = 2/45 (from a^4+b^4) + "
                     "5/45 (from a^2 b^2) over the 2/45 of (E^2-B^2)^2.",
    }


# ======================================================================
#  four-photon amplitude machinery (shared by EH2 + EH3)
# ======================================================================
def _amp_builder():
    """Return (amp, K, base_pols, symbols) — the contact four-photon amplitude
    M = 8 mu S_Phi + 8 nu S_Psi read off from L = mu (F.F)^2 + nu (F.Ftilde)^2,
    with mu = alpha^2/90 m^4, nu = 7 alpha^2/360 m^4. Each photon enters through
    f^i_{mn} = k^i_m eps^i_n - k^i_n eps^i_m only, so Ward is manifest."""
    import sympy as sp
    from sympy import LeviCivita

    g = sp.diag(1, -1, -1, -1)               # metric (+---)
    w, c = sp.symbols("w c", real=True)      # omega, cos(theta)
    s2 = sp.sqrt(1 - c ** 2)
    al, m = sp.symbols("alpha m", positive=True)

    # CM kinematics: 1,2 in along z; 3,4 out at angle theta in x-z plane
    k1 = [w, 0, 0, w]; k2 = [w, 0, 0, -w]
    k3 = [w, w * s2, 0, w * c]; k4 = [w, -w * s2, 0, -w * c]
    K = [k1, k2, k3, k4]

    def fmunu(k, eps):
        return sp.Matrix(4, 4, lambda mu, nu: k[mu] * eps[nu] - k[nu] * eps[mu])

    def cff(fa, fb):        # f^a_{mn} f^{b mn}  (raise both indices)
        return sum(fa[mu, nu] * fb[mu, nu] * g[mu, mu] * g[nu, nu]
                   for mu in range(4) for nu in range(4))

    def cfd(fa, fb):        # f^a_{mn} ftilde^{b mn} = (1/2) eps^{mnrs} fa_{mn} fb_{rs}
        return sum(LeviCivita(mu, nu, r, si) * fa[mu, nu] * fb[r, si]
                   for mu in range(4) for nu in range(4)
                   for r in range(4) for si in range(4)) / 2

    mu_c = al ** 2 / (90 * m ** 4)
    nu_c = 7 * al ** 2 / (360 * m ** 4)
    pair = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]

    def amp(pols, Kuse=None):
        Ku = Kuse if Kuse is not None else K
        f = [fmunu(Ku[i], pols[i]) for i in range(4)]
        S_Phi = sum(cff(f[a], f[b]) * cff(f[cc], f[d]) for (a, b), (cc, d) in pair)
        S_Psi = sum(cfd(f[a], f[b]) * cfd(f[cc], f[d]) for (a, b), (cc, d) in pair)
        return sp.expand(8 * mu_c * S_Phi + 8 * nu_c * S_Psi)

    base = [[0, 1, 0, 0], [0, 0, 1, 0],
            [0, c, 0, -s2], [0, c, 0, -s2]]           # one transverse pol per leg
    return amp, K, base, (w, c, al, m)


# ======================================================================
#  EH2 — light-by-light cross section (exact angular integral)
# ======================================================================
def light_by_light_cross_section() -> dict:
    """Sum |M|^2 over the 16 linear-polarisation configurations, integrate over
    solid angle (phi-symmetric) with the identical-particle factor 1/2 and the
    2->2 massless phase space dsigma/dOmega = |M|^2/(64 pi^2 s), s = 4 omega^2.
    Returns the exact low-energy cross section coefficient 973/10125."""
    import sympy as sp
    import itertools

    amp, K, base, (w, c, al, m) = _amp_builder()
    # two transverse pols per leg for the polarisation sum
    e_perp = {0: [[0, 1, 0, 0], [0, 0, 1, 0]],
              1: [[0, 1, 0, 0], [0, 0, 1, 0]],
              2: [[0, c, 0, -sp.sqrt(1 - c ** 2)], [0, 0, 1, 0]],
              3: [[0, c, 0, -sp.sqrt(1 - c ** 2)], [0, 0, 1, 0]]}

    M2 = sp.Integer(0)
    for h in itertools.product([0, 1], repeat=4):
        A = amp([e_perp[i][h[i]] for i in range(4)])
        M2 += A ** 2
    M2 = sp.expand(M2)

    s_mand = 4 * w ** 2
    dsig = M2 / sp.Integer(4) / (64 * sp.pi ** 2 * s_mand)   # avg over 4 initial pols
    sigma = sp.Rational(1, 2) * sp.integrate(dsig, (c, -1, 1)) * 2 * sp.pi
    sigma = sp.simplify(sigma)

    target = sp.Rational(*LBL_COEFF) / sp.pi * al ** 4 * w ** 6 / m ** 8
    coeff = sp.simplify(sigma * sp.pi * m ** 8 / (al ** 4 * w ** 6))  # -> 973/10125
    gate = sp.simplify(sigma - target) == 0

    return {
        "sigma": str(sigma),
        "coeff_times_pi": str(coeff),              # 973/10125
        "coeff_target": str(sp.Rational(*LBL_COEFF)),
        "scaling": "alpha^4 omega^6 / m^8",
        "gate_pass": bool(gate),
        "statement": "low-energy gamma gamma -> gamma gamma cross section = "
                     "(973/10125 pi) alpha^4 omega^6/m^8 (Karplus-Neuman), "
                     "reproduced EXACTLY from the L_EH contact vertex; angular "
                     "integral closes to a rational times 1/pi.",
    }


# ======================================================================
#  EH3 — Ward (all four legs) + Bose gates
# ======================================================================
def ward_and_bose_gates() -> dict:
    """Exact gates on the four-photon amplitude: (a) Ward — replacing any single
    polarisation eps^i by its momentum k^i gives literal 0 (transverse on every
    leg); (b) Bose — invariance under exchange of any two photons."""
    import sympy as sp

    amp, K, base, syms = _amp_builder()

    ward = {}
    for i in range(4):
        test = list(base)
        test[i] = K[i]
        ward[f"leg{i + 1}"] = sp.simplify(amp(test))
    ward_ok = all(v == 0 for v in ward.values())

    # Bose: swap photons 1<->2 (momenta and pols) — amplitude invariant
    M0 = amp(base)
    Kswap = [K[1], K[0], K[2], K[3]]
    Bswap = [base[1], base[0], base[2], base[3]]
    Mswap = amp(Bswap, Kuse=Kswap)
    bose_12 = sp.simplify(M0 - Mswap) == 0
    # swap 3<->4
    Kswap2 = [K[0], K[1], K[3], K[2]]
    Bswap2 = [base[0], base[1], base[3], base[2]]
    bose_34 = sp.simplify(M0 - amp(Bswap2, Kuse=Kswap2)) == 0

    return {
        "ward_leg_residuals": {k: str(v) for k, v in ward.items()},
        "ward_all_legs_zero": bool(ward_ok),
        "bose_1_2_invariant": bool(bose_12),
        "bose_3_4_invariant": bool(bose_34),
        "gate_pass": bool(ward_ok and bose_12 and bose_34),
        "statement": "four-photon amplitude is exactly transverse on every leg "
                     "(eps^i -> k^i gives 0) and Bose-symmetric; the four-leg "
                     "counterpart of F251's two-leg Ward identity, preserving the "
                     "F250 massless gauge structure.",
    }


# ======================================================================
#  EH4 — field-induced vacuum birefringence (7:4)
# ======================================================================
def birefringence_ratio_symbolic() -> dict:
    """Expand L_EH to second order in a probe field about a constant background B
    (along x, probe propagating along z). The two eigen-polarisations, E parallel
    vs perpendicular to B, get refractive-index shifts in the ratio 7:4 exactly.
    n - 1 = (Delta L)/(2 e^2) reproduces the standard prefactors 7/2 and 4/2."""
    import sympy as sp

    kap, B, ee = sp.symbols("kappa B e", positive=True)   # kappa = 2 alpha^2/45 m^4
    ex, ey, ez, bx, by, bz = sp.symbols("e_x e_y e_z b_x b_y b_z", real=True)
    t = sp.symbols("t")

    E2 = ex ** 2 + ey ** 2 + ez ** 2
    b2 = bx ** 2 + by ** 2 + bz ** 2
    S = E2 - (B ** 2 + 2 * B * bx + b2)        # E^2 - |B xhat + b|^2
    P = B * ex + (ex * bx + ey * by + ez * bz)  # E . (B xhat + b)
    L = kap * (S ** 2 + 7 * P ** 2)

    sub = {ex: t * ex, ey: t * ey, ez: t * ez, bx: t * bx, by: t * by, bz: t * bz}
    L2 = sp.expand(sp.series(L.subs(sub), t, 0, 3).removeO().coeff(t, 2))

    # parallel mode: E = e xhat, B_probe = e yhat  (propagation zhat)
    par = L2.subs({ex: ee, ey: 0, ez: 0, bx: 0, by: ee, bz: 0})
    # perpendicular mode: E = e yhat, B_probe = -e xhat
    per = L2.subs({ex: 0, ey: ee, ez: 0, bx: -ee, by: 0, bz: 0})

    coef_par = sp.simplify(par / (kap * B ** 2 * ee ** 2))   # -> 7
    coef_per = sp.simplify(per / (kap * B ** 2 * ee ** 2))   # -> 4
    ratio = sp.simplify(par / per)                            # -> 7/4
    gate = (coef_par == 7 and coef_per == 4
            and ratio == sp.Rational(*BIREFRINGENCE_RATIO))

    return {
        "coeff_parallel": str(coef_par),          # 7
        "coeff_perp": str(coef_per),              # 4
        "ratio_par_perp": str(ratio),             # 7/4
        "n_par_minus_1": "(7/2)(2 alpha^2/45)(B^2/m^4)",
        "n_perp_minus_1": "(4/2)(2 alpha^2/45)(B^2/m^4)",
        "gate_pass": bool(gate),
        "statement": "field-induced vacuum birefringence ratio "
                     "(n_par-1):(n_perp-1) = 7:4 (Adler 1971), derived exactly "
                     "from L_EH; the nonlinear, non-zero counterpart of F249-B1's "
                     "zero LINEAR birefringence for the free paired photon.",
    }


# ======================================================================
#  EH5 — observational contact (honest scope)
# ======================================================================
def observational_contact() -> dict:
    """The measured contact point: ATLAS observed light-by-light scattering
    gamma gamma -> gamma gamma in ultraperipheral Pb+Pb collisions (Nature Phys.
    13, 852, 2017). The low-energy coefficient here is the omega << m limit; the
    ATLAS diphoton invariant masses (~ few GeV) probe the full electron box, not
    the pure contact term. Stated, not fit."""
    return {
        "experiment": "ATLAS Pb+Pb, Nature Phys. 13, 852 (2017)",
        "regime": "high-energy box (m_gg ~ GeV), beyond the omega<<m contact limit",
        "model_contact": "sigma_LE = (973/10125 pi) alpha^4 omega^6/m^8 (this module)",
        "statement": "light-by-light scattering is experimentally observed; the "
                     "model reproduces the analytic low-energy limit exactly. No "
                     "cross-section fit to the ATLAS high-energy regime is claimed.",
    }


def report() -> dict:
    return {
        "EH1_coefficients": eh_coefficients_symbolic(),
        "EH2_light_by_light": light_by_light_cross_section(),
        "EH3_ward_bose": ward_and_bose_gates(),
        "EH4_birefringence": birefringence_ratio_symbolic(),
        "EH5_observation": observational_contact(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
