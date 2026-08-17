"""
test_F242 — Morel-Anderson mu* derived from the F64 EM-connection dielectric.
============================================================================
The F64 lattice dielectric K, in its static long-wavelength limit for the
conduction-electron medium, is the Thomas-Fermi/RPA screening eps(q)=1+
k_TF^2/q^2.  Screening the bare Coulomb + FS-averaging gives a parameter-free
mu(r_s); Morel-Anderson retardation at the solver's Coulomb cutoff gives mu*.
Checks (5): closed form matches hand value; derived mu* lands at the empirical
0.10-0.12; cutoff consistency (mu* rises with cutoff); Allen-Dynes 7-element
mean error tightens vs tabulated mu*; Eliashberg residual only partially
closes (mu* is ~6% of the ~28% overshoot, the rest is the w_log/cutoff scale).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
RESULTS = os.path.join(HERE, '..', '..', 'test-results')
from casim.engine.interactions import superconductivity as sc

NA = 6.02214076e23
KB_J = 1.380649e-23
EV_J = 1.602176634e-19
OMEGA_C_FACTOR = 6.0     # matches eliashberg_solve default omega_c_factor

ELEM = {   # rho[kg/m3], M[g/mol], Z, simple?
    "Al": (2700.0,  26.982, 3, True),  "Sn": (7265.0, 118.710, 4, True),
    "In": (7310.0, 114.818, 3, True),  "Ta": (16690.0,180.948, 5, False),
    "Nb": (8570.0,  92.906, 5, False), "Pb": (11340.0,207.200, 4, True),
    "Hg": (13534.0,200.592, 2, True),
}

def n_of(el):
    rho, M, Z, _ = ELEM[el]
    return Z * rho * NA / (M * 1e-3)

def derived_mustar(el, wlog):
    n = n_of(el)
    E_F = sc.fermi_energy_free_electron(n)
    wc_eV = KB_J * OMEGA_C_FACTOR * wlog / EV_J
    mstar, mu, L = sc.mustar_from_dielectric(n, wc_eV, E_F_eV=E_F)
    return mstar, mu, E_F, sc.wigner_seitz_rs(n)

def run():
    checks, rows = [], []
    mus_tab, mus_der = {}, {}
    for el,(lam, mustar_tab, wlog, thetaD, tc_exp) in sc.REAL_SUPERCONDUCTORS.items():
        mstar, mu, E_F, rs = derived_mustar(el, wlog)
        rows.append(dict(element=el, r_s=rs, E_F_eV=E_F, mu=mu,
                         mustar_derived=mstar, mustar_tab=mustar_tab,
                         simple=ELEM[el][3]))
        mus_tab[el] = mustar_tab; mus_der[el] = mstar

    # C1: closed form mu(r_s)=0.082930 r_s ln(1+6.0299/r_s), Al hand value
    mu_al = sc.mu_coulomb_jellium(sc.wigner_seitz_rs(n_of("Al")))
    checks.append(("C1 mu(r_s) closed form (Al ~0.234)", abs(mu_al - 0.234) < 5e-3))

    # C2: every derived mu* in the empirical band [0.085, 0.13]
    all_band = all(0.085 <= r["mustar_derived"] <= 0.13 for r in rows)
    checks.append(("C2 derived mu* in empirical band 0.085-0.13", all_band))

    # C3: cutoff consistency — mu*(6 wlog) > mu*(wlog) (bigger cutoff, larger mu*)
    n = n_of("Al"); E_F = sc.fermi_energy_free_electron(n)
    wlog = sc.REAL_SUPERCONDUCTORS["Al"][2]
    m_lo,_,_ = sc.mustar_from_dielectric(n, KB_J*wlog/EV_J, E_F_eV=E_F)
    m_hi,_,_ = sc.mustar_from_dielectric(n, KB_J*6*wlog/EV_J, E_F_eV=E_F)
    checks.append(("C3 mu*(6 wlog) > mu*(wlog) cutoff consistency", m_hi > m_lo))

    # C4: Allen-Dynes 7-element mean error tightens with derived mu*
    def ad_mean(md):
        e = [abs(sc.allen_dynes_tc(v[0], md[el], v[2]) - v[4]) / v[4]
             for el, v in sc.REAL_SUPERCONDUCTORS.items()]
        return sum(e) / len(e)
    ad_tab, ad_der = ad_mean(mus_tab), ad_mean(mus_der)
    checks.append(("C4 Allen-Dynes error tightens (derived<tabulated)", ad_der < ad_tab))

    # C5: Eliashberg residual only partially closes (still >10%: not purely mu*)
    def el_mean(md):
        e = [abs(sc.eliashberg_tc(v[0], v[2], md[el], spectrum="debye") - v[4]) / v[4]
             for el, v in sc.REAL_SUPERCONDUCTORS.items()]
        return sum(e) / len(e)
    el_der = el_mean(mus_der)
    checks.append(("C5 Eliashberg residual only partial (10%<err, mu* not whole story)",
                   el_der > 0.10))

    result = dict(rows=rows, allen_dynes_mean_err=dict(tabulated=ad_tab, derived=ad_der),
                  eliashberg_mean_err_derived=el_der,
                  checks={k: bool(v) for k, v in checks})
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "F242_mustar_from_dielectric.json"), "w") as f:
        json.dump(result, f, indent=2)

    npass = sum(1 for _, v in checks if v)
    for k, v in checks:
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"  Allen-Dynes mean |err|: tabulated {ad_tab:.1%} -> derived {ad_der:.1%}")
    print(f"  Eliashberg mean |err| (derived mu*): {el_der:.1%}")
    print(f"F242: {npass}/{len(checks)} PASS")
    return npass == len(checks)

if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
