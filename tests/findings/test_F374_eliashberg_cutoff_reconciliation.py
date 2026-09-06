"""
test_F374 — Reconciling the F215 Eliashberg solver's Coulomb cutoff with the
F242 derived mu*, and locating the true floor of the Allen-Dynes Tc residual.
============================================================================
F242 derived mu* from the F64 dielectric assuming the solver's Coulomb cutoff
is omega_c = 6*omega_log (correct for spectrum='einstein', where the solver's
own phonon scale omega_E==omega_log).  Its own C5 check then fed that same
mu* into the spectrum='debye' Eliashberg solve, whose actual cutoff scale is
omega_max=sqrt(e)*omega_log (F218b AF2) -- sqrt(e)=1.6487x larger.  This
finding (1) fixes that mismatch, (2) rules out finite-N truncation as an
alternative explanation, (3) scans the cutoff factor and the mu*-uniform (no
window) limit to bound how much of the Eliashberg residual is cutoff
convention vs genuine physics, (4) tests the model's OWN closed-form
strong-coupling shape factor r=sqrt(e/2) (exact, from the F218b Debye alpha^2F)
in the Allen-Dynes f2 correction, and (5) concludes the Allen-Dynes 6.3%
headline (F242) remains the tightest Tc estimator the model's current
(single-band jellium + isotropic Debye acoustic phonon) construction can
produce; the Eliashberg-solver route, even fully reconciled, plateaus at
~16-17% and does not go below it.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
RESULTS = os.path.join(HERE, "..", "..", "test-results")
from casim.engine.interactions import superconductivity as sc

NA = 6.02214076e23
KB_J = 1.380649e-23
EV_J = 1.602176634e-19

ELEM = {   # rho[kg/m3], M[g/mol], Z
    "Al": (2700.0,  26.982, 3), "Sn": (7265.0, 118.710, 4),
    "In": (7310.0, 114.818, 3), "Ta": (16690.0,180.948, 5),
    "Nb": (8570.0,  92.906, 5), "Pb": (11340.0,207.200, 4),
    "Hg": (13534.0,200.592, 2),
}

def n_of(el):
    rho, M, Z = ELEM[el]
    return Z * rho * NA / (M * 1e-3)

def mustar_einstein_convention(el, wlog, ocf=6.0):
    """F242's ORIGINAL derivation: cutoff = ocf*omega_log unconditionally."""
    n = n_of(el)
    E_F = sc.fermi_energy_free_electron(n)
    wc_eV = KB_J * ocf * wlog / EV_J
    mstar, mu, L = sc.mustar_from_dielectric(n, wc_eV, E_F_eV=E_F)
    return mstar

def mustar_spectrum_consistent(el, wlog, ocf, spectrum):
    """The F374 fix: cutoff matches the solver's own scale for `spectrum`."""
    n = n_of(el)
    E_F = sc.fermi_energy_free_electron(n)
    return sc.mustar_from_dielectric_for_spectrum(n, wlog, omega_c_factor=ocf,
                                                  spectrum=spectrum, E_F_eV=E_F)[0]

def mean_err(tc_fn):
    errs = []
    for el, (lam, mustar_tab, wlog, thetaD, tc_exp) in sc.REAL_SUPERCONDUCTORS.items():
        errs.append(abs(tc_fn(el, lam, wlog) - tc_exp) / tc_exp)
    return sum(errs) / len(errs), errs


def run():
    checks, notes = [], {}

    # ---- D1: reproduce the F242 baseline (sanity: einstein-convention mu*
    # fed into a debye-spectrum solve, mean err ~21.6%, as F242 C5 reported) ----
    def tc_baseline(el, lam, wlog):
        ms = mustar_einstein_convention(el, wlog)
        return sc.eliashberg_tc(lam, wlog, ms, spectrum="debye")
    err_baseline, _ = mean_err(tc_baseline)
    checks.append(("D1 reproduces F242 C5 baseline (20%<err<24%)",
                    0.20 < err_baseline < 0.24))
    notes["baseline_mismatched_cutoff_mean_err"] = err_baseline

    # ---- D2: the cutoff-scale fix (mu* at the debye-consistent omega_c)
    # tightens the Eliashberg mean error ----
    def tc_fixed(el, lam, wlog):
        ms = mustar_spectrum_consistent(el, wlog, 6.0, "debye")
        return sc.eliashberg_tc(lam, wlog, ms, spectrum="debye")
    err_fixed, errs_fixed = mean_err(tc_fixed)
    checks.append(("D2 cutoff-scale fix tightens Eliashberg error (fixed<baseline)",
                    err_fixed < err_baseline))
    notes["cutoff_fixed_mean_err"] = err_fixed

    # ---- D3: sqrt(e) is exactly the ratio of the two cutoff conventions ----
    ratio = sc.eliashberg_matsubara_cutoff_eV(291.0, 6.0, "debye") / \
            sc.eliashberg_matsubara_cutoff_eV(291.0, 6.0, "einstein")
    checks.append(("D3 debye/einstein cutoff ratio == sqrt(e) exactly",
                    abs(ratio - math.sqrt(math.e)) < 1e-12))

    # ---- D4: finite-N truncation is NOT the source of the residual (rho(Tc)
    # converged to <1% already at the solver's own default N) ----
    lam, wlog = sc.REAL_SUPERCONDUCTORS["Al"][0], sc.REAL_SUPERCONDUCTORS["Al"][2]
    ms = mustar_spectrum_consistent("Al", wlog, 6.0, "debye")
    omega_max = sc.omega_max_from_omega_log(wlog)
    T_guess = sc.allen_dynes_tc(lam, ms, wlog)
    scale = omega_max
    default_N = min(sc._N_MAX, max(64, int(6.0 * scale / (2 * math.pi * T_guess)) + 8))
    rho_default = sc.eliashberg_tc_eigenvalue(T_guess, lam, wlog, ms, N=default_N,
                                              spectrum="debye", omega_max=omega_max)
    rho_converged = sc.eliashberg_tc_eigenvalue(T_guess, lam, wlog, ms, N=3000,
                                                spectrum="debye", omega_max=omega_max)
    rel_shift = abs(rho_default - rho_converged) / rho_converged
    checks.append(("D4 default-N eigenvalue within 1% of N=3000 converged value",
                    rel_shift < 0.01))
    notes["N_convergence_rel_shift"] = rel_shift

    # ---- D5: increasing the Coulomb cutoff factor (self-consistently
    # re-deriving mu* each time) does NOT converge below ~16% -- rules out
    # "cutoff too small" as the whole story ----
    ocf_scan = {}
    for ocf in (1.0, 2.0, 4.0, 6.0, 10.0, 15.0):
        def tc_ocf(el, lam, wlog, _ocf=ocf):
            ms = mustar_spectrum_consistent(el, wlog, _ocf, "debye")
            return sc.eliashberg_tc(lam, wlog, ms, omega_c_factor=_ocf, spectrum="debye")
        e, _ = mean_err(tc_ocf)
        ocf_scan[ocf] = e
    checks.append(("D5 ocf-scan plateaus above 6.3% AD floor for every factor tested",
                    all(e > 0.063 for e in ocf_scan.values())))
    checks.append(("D5b ocf-scan is monotone non-increasing (bigger cutoff, no worse)",
                    all(ocf_scan[a] >= ocf_scan[b] - 1e-9
                        for a, b in zip(sorted(ocf_scan), sorted(ocf_scan)[1:]))))
    notes["ocf_scan_mean_err"] = ocf_scan

    # ---- D6: the model's own exact strong-coupling shape factor
    # r=sqrt(e/2) (F218b Debye alpha^2F second moment) fed into Allen-Dynes'
    # f2 correction does NOT tighten the fit -- the unadorned f2=1 formula
    # (F242's headline 6.3%) is the tightest available, not an oversight ----
    r_model = math.sqrt(math.e / 2.0)
    def ad_no_r(el, lam, wlog):
        ms = mustar_spectrum_consistent(el, wlog, 6.0, "einstein")
        return sc.allen_dynes_tc(lam, ms, wlog)
    def ad_with_r(el, lam, wlog):
        ms = mustar_spectrum_consistent(el, wlog, 6.0, "einstein")
        return sc.allen_dynes_tc(lam, ms, wlog, omega2_over_wlog=r_model)
    err_no_r, _ = mean_err(ad_no_r)
    err_with_r, _ = mean_err(ad_with_r)
    checks.append(("D6 F242 6.3% headline reproduced with einstein-consistent mu*",
                    abs(err_no_r - 0.0635) < 0.002))
    checks.append(("D6b model's own r=sqrt(e/2) shape factor does not tighten Allen-Dynes",
                    err_with_r >= err_no_r))
    notes["r_model"] = r_model
    notes["allen_dynes_mean_err_no_r"] = err_no_r
    notes["allen_dynes_mean_err_with_model_r"] = err_with_r

    # ---- D7: removing the Coulomb window entirely (mu* applied uniformly
    # at all Matsubara frequencies, no cutoff at all) is WORSE, not better --
    # rules out "just drop the window" as a fix ----
    def eliashberg_tc_eigenvalue_nocutoff(T, lam, omega_E, mustar, spectrum, omega_max):
        scale = sc._cutoff_scale(spectrum, omega_E, omega_max)
        N = min(sc._N_MAX, max(64, int(6.0 * scale / (2 * math.pi * T)) + 8))
        w = sc._matsubara(T, N)
        L = sc._lambda_matrix(T, N, spectrum, lam, omega_E, omega_max)
        Z = 1.0 + (math.pi * T / w) * (L @ np.sign(w))
        M = (math.pi * T) * (L - mustar) / (Z[:, None] * np.abs(w)[None, :])
        v = np.ones(2 * N) / math.sqrt(2 * N)
        rho = 0.0
        for _ in range(3000):
            u = M @ v
            rho_new = np.linalg.norm(u)
            v = u / rho_new
            if abs(rho_new - rho) < 1e-12:
                rho = rho_new
                break
            rho = rho_new
        return rho

    def tc_nocutoff(el, lam, wlog):
        ms = mustar_spectrum_consistent(el, wlog, 6.0, "debye")
        omega_max = sc.omega_max_from_omega_log(wlog)
        f = lambda T: eliashberg_tc_eigenvalue_nocutoff(T, lam, wlog, ms, "debye", omega_max) - 1.0
        guess = sc.allen_dynes_tc(lam, ms, wlog)
        lo, hi = max(1e-4 * omega_max, 0.02 * guess), max(3.0 * guess, 0.05 * omega_max)
        for _ in range(40):
            if f(lo) > 0 and f(hi) < 0:
                break
            if f(lo) < 0:
                lo *= 0.5
            if f(hi) > 0:
                hi *= 1.5
        return sc._bisect(f, lo, hi, tol=1e-6)

    err_nocutoff, _ = mean_err(tc_nocutoff)
    checks.append(("D7 removing the Coulomb window entirely is worse than windowed (fixed)",
                    err_nocutoff > err_fixed))
    notes["no_cutoff_mean_err"] = err_nocutoff

    # ---- D8: the reconciled Eliashberg floor (~16-17%) still exceeds the
    # Allen-Dynes headline (6.3%) by a wide margin -- the attack does not
    # cross the target threshold ----
    checks.append(("D8 reconciled Eliashberg floor still exceeds the 6.3% AD target",
                    err_fixed > 0.063))

    result = dict(checks={k: bool(v) for k, v in checks}, notes=notes)
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "F374_eliashberg_cutoff_reconciliation.json"), "w") as f:
        json.dump(result, f, indent=2)

    npass = sum(1 for _, v in checks if v)
    for k, v in checks:
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"  baseline (mismatched cutoff) mean err: {err_baseline:.1%}")
    print(f"  fixed (spectrum-consistent cutoff) mean err: {err_fixed:.1%}")
    print(f"  no-cutoff-window mean err: {err_nocutoff:.1%}")
    print(f"  Allen-Dynes (einstein-consistent mu*, no r) mean err: {err_no_r:.1%}")
    print(f"  Allen-Dynes with model r=sqrt(e/2): {err_with_r:.1%}")
    print(f"F374: {npass}/{len(checks)} PASS")
    return npass == len(checks)


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
