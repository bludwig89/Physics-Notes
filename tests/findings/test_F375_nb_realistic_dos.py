"""
test_F375 — A real (DFT-sourced) N(0) for Nb, not free-electron, in the F242
mu* derivation: the flagged open next step from F374.
============================================================================
F374 closed the Eliashberg-solver/cutoff route to beating the Allen-Dynes
6.3% headline (F242) as a NO-GO, and named the actual next step: the model's
free-electron N(0) understates the true density of states for the d-band
metals Nb/Ta, and correcting it (not the solver's cutoff bookkeeping) is
where the residual actually lives. This finding does that correction for Nb,
using a density of states sourced from a DFT band-structure calculation (not
a fit), and tests what it does to both the Allen-Dynes headline and the
already-reconciled (F374) Eliashberg mean error. Ta is intentionally left
uncorrected -- no equally solid sourced N(Ef) for Ta was found this session,
and guessing one would violate the same "no fit, no invention" standard this
whole derivation chain (F242/F374) depends on.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
RESULTS = os.path.join(HERE, "..", "..", "test-results")
from casim.engine.interactions import superconductivity as sc

NA = 6.02214076e23
OCF = 6.0

ELEM = {   # rho[kg/m3], M[g/mol], Z
    "Al": (2700.0,  26.982, 3), "Sn": (7265.0, 118.710, 4),
    "In": (7310.0, 114.818, 3), "Ta": (16690.0,180.948, 5),
    "Nb": (8570.0,  92.906, 5), "Pb": (11340.0,207.200, 4),
    "Hg": (13534.0,200.592, 2),
}

def n_of(el):
    rho, M, Z = ELEM[el]
    return Z * rho * NA / (M * 1e-3)

def mustar_for(el, wlog, spectrum):
    """Free-electron mu* for elements not in DOS_ENHANCEMENT; the sourced
    real-DOS mu* (mustar_from_real_dos) for elements that are (today: Nb)."""
    n = n_of(el)
    E_F = sc.fermi_energy_free_electron(n)
    if el in sc.DOS_ENHANCEMENT:
        alpha, _source = sc.DOS_ENHANCEMENT[el]
        ms, mu, L = sc.mustar_from_real_dos(n, wlog, alpha, OCF, spectrum, E_F_eV=E_F)
    else:
        ms, mu, L = sc.mustar_from_dielectric_for_spectrum(n, wlog, OCF, spectrum, E_F_eV=E_F)
    return ms

def mean_err(tc_fn):
    errs = {}
    for el, (lam, mustar_tab, wlog, thetaD, tc_exp) in sc.REAL_SUPERCONDUCTORS.items():
        errs[el] = abs(tc_fn(el, lam, wlog) - tc_exp) / tc_exp
    return sum(errs.values()) / len(errs), errs


def run():
    checks, notes = [], {}

    # ---- D1: alpha=1 reduces mu_coulomb_real_dos to mu_coulomb_jellium
    # exactly, for a spread of r_s values (the generalization is loss-free) ----
    ok = all(abs(sc.mu_coulomb_jellium(rs) - sc.mu_coulomb_real_dos(rs, 1.0)) < 1e-14
             for rs in (1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 4.0))
    checks.append(("D1 mu_coulomb_real_dos(rs, alpha=1) == mu_coulomb_jellium(rs) exactly", ok))

    # ---- D2: the sourced alpha for Nb is pinned (regression-style) to the
    # DFT value this finding cites, and alpha>1 (real d-band DOS exceeds the
    # free-electron estimate, as physically expected) ----
    alpha_nb, source_nb = sc.DOS_ENHANCEMENT["Nb"]
    n_nb = n_of("Nb")
    E_F_nb = sc.fermi_energy_free_electron(n_nb)
    N0_free_nb = 3.0 * ELEM["Nb"][2] / (2.0 * E_F_nb)     # both-spin, per atom
    N0_real_nb = 1.49                                      # De Marzi et al./Frontiers Phys 2023
    alpha_recomputed = N0_real_nb / N0_free_nb
    checks.append(("D2a alpha_Nb matches recomputation from cited N(Ef)=1.49 eV^-1/atom",
                    abs(alpha_recomputed - alpha_nb) < 1e-3))
    checks.append(("D2b alpha_Nb > 1 (real d-band DOS exceeds free-electron)", alpha_nb > 1.0))
    notes["alpha_Nb"] = alpha_nb
    notes["N0_free_Nb_eV-1_per_atom_bothspin"] = N0_free_nb
    notes["N0_real_Nb_eV-1_per_atom_bothspin_source"] = source_nb

    # ---- D3: Allen-Dynes, einstein-cutoff mu* convention (matches the
    # official 6.3% G9 headline basis, F242/F374 D6) -- baseline (all
    # free-electron) vs Nb-corrected ----
    def ad_baseline(el, lam, wlog):
        n = n_of(el)
        ms = sc.mustar_from_dielectric_for_spectrum(n, wlog, OCF, "einstein",
                                                     E_F_eV=sc.fermi_energy_free_electron(n))[0]
        return sc.allen_dynes_tc(lam, ms, wlog)

    def ad_nb_corrected(el, lam, wlog):
        ms = mustar_for(el, wlog, "einstein")
        return sc.allen_dynes_tc(lam, ms, wlog)

    err_ad_baseline, errs_ad_baseline = mean_err(ad_baseline)
    err_ad_corrected, errs_ad_corrected = mean_err(ad_nb_corrected)
    checks.append(("D3a reproduces F242/F374 6.3% Allen-Dynes baseline (within 0.2pt)",
                    abs(err_ad_baseline - 0.0635) < 0.002))
    checks.append(("D3b Nb-corrected Allen-Dynes mean error is lower than baseline",
                    err_ad_corrected < err_ad_baseline))
    checks.append(("D3c Nb-corrected Allen-Dynes mean error crosses below the 6.3% G9 target",
                    err_ad_corrected < 0.063))
    checks.append(("D3d Nb's own Allen-Dynes error improves substantially (corrected < baseline/2)",
                    errs_ad_corrected["Nb"] < 0.5 * errs_ad_baseline["Nb"]))
    notes["allen_dynes_mean_err_baseline"] = err_ad_baseline
    notes["allen_dynes_mean_err_nb_corrected"] = err_ad_corrected
    notes["allen_dynes_per_element_baseline"] = errs_ad_baseline
    notes["allen_dynes_per_element_nb_corrected"] = errs_ad_corrected

    # ---- D4: Eliashberg, debye-consistent mu* convention (F374's own 17.2%
    # reconciled baseline) -- Nb correction should still move the same
    # direction (lower), even though F374 already showed this route alone
    # cannot cross 6.3% for the FULL solver (that finding stands; this is a
    # consistency check, not a re-attack on the closed cutoff/window route) ----
    def el_baseline(el, lam, wlog):
        n = n_of(el)
        ms = sc.mustar_from_dielectric_for_spectrum(n, wlog, OCF, "debye",
                                                     E_F_eV=sc.fermi_energy_free_electron(n))[0]
        return sc.eliashberg_tc(lam, wlog, ms, spectrum="debye")

    def el_nb_corrected(el, lam, wlog):
        ms = mustar_for(el, wlog, "debye")
        return sc.eliashberg_tc(lam, wlog, ms, spectrum="debye")

    err_el_baseline, errs_el_baseline = mean_err(el_baseline)
    err_el_corrected, errs_el_corrected = mean_err(el_nb_corrected)
    checks.append(("D4a reproduces F374's 17.2% reconciled Eliashberg baseline (within 0.5pt)",
                    abs(err_el_baseline - 0.172) < 0.005))
    checks.append(("D4b Nb-corrected Eliashberg mean error is lower than baseline (same direction)",
                    err_el_corrected < err_el_baseline))
    checks.append(("D4c reconciled Eliashberg floor (Nb-corrected) still exceeds 6.3% "
                    "-- F374's NO-GO on the solver route is untouched, not re-litigated",
                    err_el_corrected > 0.063))
    notes["eliashberg_mean_err_baseline"] = err_el_baseline
    notes["eliashberg_mean_err_nb_corrected"] = err_el_corrected

    # ---- D5: Ta is explicitly and machine-checkably NOT corrected this
    # session (scope boundary, not an oversight) ----
    checks.append(("D5 Ta intentionally absent from DOS_ENHANCEMENT (no sourced N(Ef) found)",
                    "Ta" not in sc.DOS_ENHANCEMENT))

    # ---- D6: robustness (review attack 7/12) -- the "crosses below 6.3%"
    # conclusion does not hinge on getting alpha_Nb exactly right: it holds
    # over a wide perturbation of alpha (not just at the one sourced value),
    # so a modest revision of the literature N(Ef) would not overturn it ----
    def ad_mean_err_at_alpha(alpha):
        def fn(el, lam, wlog):
            n = n_of(el)
            E_F = sc.fermi_energy_free_electron(n)
            if el == "Nb":
                ms, _, _ = sc.mustar_from_real_dos(n, wlog, alpha, OCF, "einstein", E_F_eV=E_F)
            else:
                ms, _, _ = sc.mustar_from_dielectric_for_spectrum(n, wlog, OCF, "einstein", E_F_eV=E_F)
            return sc.allen_dynes_tc(lam, ms, wlog)
        e, _ = mean_err(fn)
        return e
    alpha_scan = {a: ad_mean_err_at_alpha(a) for a in (1.0, 2.0, 2.5, 3.0839, 4.0, 4.5, 6.0)}
    checks.append(("D6a perturbing alpha_Nb changes the result (test can fail, not vacuous)",
                    alpha_scan[1.0] > 0.063 and alpha_scan[3.0839] < 0.063))
    checks.append(("D6b crossing below 6.3% is robust over alpha in [2.0, 4.5], not fine-tuned",
                    all(alpha_scan[a] < 0.063 for a in (2.0, 2.5, 3.0839, 4.0, 4.5))))
    notes["alpha_sensitivity_scan_mean_err"] = alpha_scan

    result = dict(checks={k: bool(v) for k, v in checks}, notes=notes)
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "F375_nb_realistic_dos.json"), "w") as f:
        json.dump(result, f, indent=2)

    npass = sum(1 for _, v in checks if v)
    for k, v in checks:
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"  Allen-Dynes mean |err|: baseline {err_ad_baseline:.2%} -> Nb-corrected {err_ad_corrected:.2%}")
    print(f"  Nb Allen-Dynes |err|:   baseline {errs_ad_baseline['Nb']:.1%} -> Nb-corrected {errs_ad_corrected['Nb']:.1%}")
    print(f"  Eliashberg mean |err| (F374 basis): baseline {err_el_baseline:.1%} -> Nb-corrected {err_el_corrected:.1%}")
    print(f"F375: {npass}/{len(checks)} PASS")
    return npass == len(checks)


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
