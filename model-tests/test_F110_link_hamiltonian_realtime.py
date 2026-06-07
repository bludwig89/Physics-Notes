# test_F110_link_hamiltonian_realtime.py
# 2026-06-06
#
# F110 -- Real-time Kogut-Susskind link Hamiltonian evolution for the
# confinement sector (audit B.2 item 2: "real-time link Hamiltonian evolution
# is not built; Wilson-loop tests run on frozen links").
#
# The build: H = (g^2/2) Sum_links E_hat^2 - lambda Sum_plaq cos(phi_hat) on an
# open 2D spatial lattice, in the gauge-invariant DUAL (plaquette-height)
# representation, where Gauss's law div E = q is solved exactly by
# E_l = m_{p+} - m_{p-} + eta_l (eta = static-charge background string).
# This is the F101 compact rotor made multi-plaquette and real-time.
# Groups: Z3 (the SU(3) centre, EXACT finite Hilbert space) and compact U(1)
# (truncated electric basis, convergence checked).
#
#   C1  direct-vs-dual identity: full spectrum of the direct link-basis KS
#       Hamiltonian restricted to the Gauss sector == dual spectrum, machine
#       precision, vacuum AND charged sectors (proves Gauss law is exact and
#       the dual construction is the gauge theory, not a model of it).
#   C2  strong-coupling exactness: lambda=0 gives V(R) = (g^2/2) q^2 R exactly
#       (Tier 1; integer arithmetic).
#   C3  linear static potential at finite coupling: V(R) from Lanczos ground
#       states is linear (Creutz-style residual small), sigma falls with lambda.
#   C4  PT cross-check: sigma(lambda) -> g^2/2 - c2*lambda^2 with c2 from
#       programmatic 2nd-order strong-coupling PT (asymptotic, ratio -> 1).
#   C5  real-time unitarity + energy conservation: Krylov evolution of the
#       charged ground state; norm and <H> drift at the 1e-13 floor; Krylov
#       path certified against dense eigendecomposition evolution.
#   C6  real-time string persistence: quench a bare flux string; at confining
#       coupling the electric energy stays on the string row (time-averaged
#       string fraction high), at weak coupling it delocalises (fraction
#       drops toward the uniform value) -- confinement seen in real time.
#   C7  F101 rotor contact: the 1-plaquette dual U(1) Hamiltonian IS the F101
#       rotor with chi = 1/(4 g^2) (matrix identity, exact); sigma_1 at
#       lambda=1, chi=1 reproduces the F101 table 0.29551; truncation
#       convergence at the F101 policy.
#
# Run:  python test_F110_link_hamiltonian_realtime.py [C1 C2 ...]   (default all)
# Results accumulate into test-results/F110_link_hamiltonian_realtime.json

import json
import time
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ca-simulation"))

import ca_link_hamiltonian as lh

OUT = ROOT / "test-results" / "F110_link_hamiltonian_realtime.json"
t0 = time.time()

if OUT.exists():
    results = json.loads(OUT.read_text())
else:
    results = {"finding": "F110", "date": "2026-06-06",
               "title": "real-time Kogut-Susskind link Hamiltonian evolution "
                        "(dual height representation, Z3 + U(1))",
               "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement, "residual": str(residual),
        "status": "PASS" if status else "FAIL"}
    print(f"{name}: {statement}\n      -> residual {residual} "
          f"[{'PASS' if status else 'FAIL'}]")


# ------------------------------------------------------------------ C1
def check_C1():
    worst = 0.0
    details = []
    cases = [
        ("ladder 2x1 vacuum", lh.PlaquetteGrid(2, 1), None),
        ("ladder 2x1 charged R=1", lh.PlaquetteGrid(2, 1), (0, 1, 0)),
        ("grid 2x2 vacuum", lh.PlaquetteGrid(2, 2), None),
        ("grid 2x2 charged R=2", lh.PlaquetteGrid(2, 2), (0, 2, 1)),
    ]
    for label, geom, chg in cases:
        if chg is None:
            eta = np.zeros(geom.n_links, dtype=np.int64)
            charges = {}
        else:
            x1, x2, row = chg
            eta, charges = geom.background_string(x1, x2, row)
        Hd, _ = lh.build_dual_hamiltonian(geom, eta, g2=1.0, lam=0.7,
                                          group='Z3')
        Hf, n_phys = lh.build_direct_zn(geom, g2=1.0, lam=0.7, N=3,
                                        charges=charges)
        dim_dual = Hd.shape[0]
        assert n_phys == dim_dual, (n_phys, dim_dual)
        wd = np.sort(np.linalg.eigvalsh(Hd.toarray()))
        wf = np.sort(np.linalg.eigvalsh(Hf.toarray()))
        r = float(np.max(np.abs(wd - wf)))
        worst = max(worst, r)
        details.append(f"{label}: dim {dim_dual}, max|dE| {r:.2e}")
    ok = worst < 1e-12
    record("C1", "direct link-basis KS Hamiltonian on the Gauss sector == "
                 "dual height Hamiltonian (full spectra, vacuum + charged)",
           "; ".join(details), ok)


# ------------------------------------------------------------------ C2
def check_C2():
    geom = lh.PlaquetteGrid(8, 1)
    g2 = 1.0
    worst = 0.0
    for R in range(1, 7):
        eta, _ = geom.background_string(1, 1 + R, 0)
        E0 = lh.ground_energy_lambda0(geom, eta, g2=g2, group='Z3')
        worst = max(worst, abs(E0 - 0.5 * g2 * R))
    # U(1) too (raw integer electric values)
    geom6 = lh.PlaquetteGrid(6, 1)
    for R in range(1, 5):
        eta, _ = geom6.background_string(1, 1 + R, 0)
        E0 = lh.ground_energy_lambda0(geom6, eta, g2=g2, group='U1', m_max=2)
        worst = max(worst, abs(E0 - 0.5 * g2 * R))
    record("C2", "lambda=0 static potential exact: V(R) = (g^2/2) R "
                 "(Z3 ladder R=1..6, U1 ladder R=1..4; integer arithmetic)",
           f"max |V - g^2 R/2| = {worst:.1e}", worst == 0.0)


# ------------------------------------------------------------------ C3
def check_C3():
    # sigma from the interior increment V(R) - V(R-1) (the Hamiltonian
    # Creutz estimator): converges as the string-end self-energy saturates.
    geom = lh.PlaquetteGrid(10, 1)
    sig = {}
    cauchy = {}
    for lam in (0.2, 0.5, 1.0):
        V = lh.static_potential(geom, 0, range(1, 6), g2=1.0, lam=lam,
                                group='Z3')
        inc = [V[R] - V[R - 1] for R in range(2, 6)]
        sig[lam] = inc[-1]
        cauchy[lam] = abs(inc[-1] - inc[-2]) / inc[-1]
        assert all(a > b for a, b in zip(inc, inc[1:])), "inc not monotone"
    mono = sig[0.2] > sig[0.5] > sig[1.0] > 0
    conv = max(cauchy.values()) < 1e-2
    record("C3", "linear static potential from real ground states "
                 "(Z3 ladder 10x1, R=1..5): increment estimator "
                 "V(R)-V(R-1) converges (Cauchy < 1%), sigma "
                 "monotone-decreasing in lambda, all positive (confining)",
           f"sigma {dict((k, round(v, 5)) for k, v in sig.items())}, "
           f"max increment Cauchy {max(cauchy.values()):.1e}", mono and conv)
    results.setdefault("tables", {})["sigma_vs_lambda_Z3"] = sig


# ------------------------------------------------------------------ C4
def check_C4():
    geom = lh.PlaquetteGrid(8, 1)
    c2 = lh.sigma_strong_pt2(geom, 0, g2=1.0, group='Z3')
    lams = (0.025, 0.05, 0.1)
    ratios = []
    for lam in lams:
        V = lh.static_potential(geom, 0, [2, 3], g2=1.0, lam=lam, group='Z3')
        sigma_ed = V[3] - V[2]              # interior increment
        ratios.append((0.5 - sigma_ed) / (c2 * lam ** 2))
    # Z3 has a genuine O(lambda^3) winding term (0->1->2->0), so the ratio
    # approaches 1 LINEARLY in lambda; Richardson-extrapolate it out.
    rich = [2 * ratios[i] - ratios[i + 1] for i in range(2)]
    ok = abs(rich[0] - 1.0) < 0.01 and abs(ratios[0] - 1.0) < 0.03
    record("C4", "strong-coupling PT cross-check (asymptotic): "
                 "sigma(lambda) = g^2/2 - c2 lambda^2 + O(lambda^3), c2 from "
                 "programmatic 2nd-order PT; the O(lambda^3) Z3 winding term "
                 "Richardson-extrapolates away",
           f"c2 = {c2:.6f}; ratios {[round(r, 5) for r in ratios]} "
           f"(lam={lams}); Richardson -> {[round(r, 5) for r in rich]}", ok)


# ------------------------------------------------------------------ C5
def check_C5():
    geom = lh.PlaquetteGrid(4, 2)
    eta, _ = geom.background_string(1, 3, 1)
    H, digits = lh.build_dual_hamiltonian(geom, eta, g2=1.0, lam=0.5,
                                          group='Z3')
    E0, psi0 = lh.ground_state(H)
    # excite: superpose ground state with a bare-string basis state
    bare = np.zeros(H.shape[0]); bare[0] = 1.0
    psi = (psi0 + bare) / np.linalg.norm(psi0 + bare)
    t_grid = np.linspace(0.0, 20.0, 21)
    traj = lh.evolve_krylov(H, psi, t_grid)
    norms = np.linalg.norm(traj, axis=1)
    ens = np.array([lh.energy_expect(H, traj[n]) for n in range(len(t_grid))])
    norm_drift = float(np.max(np.abs(norms - 1.0)))
    en_drift = float(np.max(np.abs(ens - ens[0])))
    # certify Krylov against dense-exact evolution at the final time
    psi_dense = lh.evolve_dense(H, psi, [t_grid[-1]])[0]
    kry_err = float(np.linalg.norm(traj[-1] - psi_dense))
    ok = norm_drift < 1e-12 and en_drift < 1e-11 and kry_err < 1e-10
    record("C5", "real-time evolution is unitary and conserves <H> "
                 "(Z3 4x2 grid, dim 6561, t=0..20); Krylov path certified "
                 "against dense eigendecomposition",
           f"norm drift {norm_drift:.1e}, energy drift {en_drift:.1e}, "
           f"|Krylov - dense| {kry_err:.1e}", ok)


# ------------------------------------------------------------------ C6
def check_C6():
    # Flux-tube localisation and real-time persistence, measured as the
    # string-row share of the EXCESS electric energy over the (same-coupling)
    # vacuum profile -- the background-subtracted flux tube.
    geom = lh.PlaquetteGrid(4, 2)
    eta, _ = geom.background_string(0, 4, 1)          # full-width string, row 1
    eta0 = np.zeros(geom.n_links, dtype=np.int64)
    sl = [geom.link_id[('H', i, 1)] for i in range(4)]
    uniform = len(sl) / geom.n_links
    gs_frac, quench = {}, {}
    for lam in (0.5, 4.0):
        Hv, digits = lh.build_dual_hamiltonian(geom, eta0, g2=1.0, lam=lam,
                                               group='Z3')
        Ev = lh.link_E_values(geom, digits, eta0, group='ZN', N=3)
        _, psiv = lh.ground_state(Hv)
        prof_vac = lh.link_E2_profile(psiv, Ev)
        H, _ = lh.build_dual_hamiltonian(geom, eta, g2=1.0, lam=lam,
                                         group='Z3')
        E_vals = lh.link_E_values(geom, digits, eta, group='ZN', N=3)
        # (a) the charged ground state: where does the flux tube live?
        _, psig = lh.ground_state(H)
        ex = lh.link_E2_profile(psig, E_vals) - prof_vac
        gs_frac[lam] = float(ex[sl].sum() / ex.sum())
        # (b) real-time quench of the bare string (heights = 0 basis state)
        psi = np.zeros(H.shape[0]); psi[0] = 1.0
        traj = lh.evolve_krylov(H, psi, np.linspace(0.0, 12.0, 13))
        fr, tot = [], []
        for n in range(1, 13):
            exq = lh.link_E2_profile(traj[n], E_vals) - prof_vac
            tot.append(exq.sum())
            fr.append(exq[sl].sum() / exq.sum())
        quench[lam] = {"frac": float(np.mean(fr)),
                       "min_total_excess": float(np.min(tot))}
    ok = (gs_frac[0.5] > 0.55 and gs_frac[0.5] - gs_frac[4.0] > 0.2
          and quench[0.5]["frac"] > 1.8 * uniform
          and quench[0.5]["min_total_excess"] > 0
          and quench[4.0]["min_total_excess"] < 0)
    record("C6", "real-time flux tube: ground-state excess flux localised on "
                 "the string row at confining coupling and delocalised at "
                 "weak coupling; quenched bare string PERSISTS as a positive "
                 "flux excess (>1.8x uniform share) at lam=0.5 but MELTS "
                 "below the vacuum fluctuation level at lam=4.0 "
                 f"(uniform share {uniform:.3f})",
           f"GS excess frac lam=0.5: {gs_frac[0.5]:.4f}, lam=4.0: "
           f"{gs_frac[4.0]:.4f}; quench frac lam=0.5: "
           f"{quench[0.5]['frac']:.4f} (min total excess "
           f"{quench[0.5]['min_total_excess']:+.3f}); lam=4.0 min total "
           f"excess {quench[4.0]['min_total_excess']:+.3f}", ok)
    results.setdefault("tables", {})["flux_tube"] = {
        "gs_excess_fraction": gs_frac, "quench": quench,
        "uniform_share": uniform}


# ------------------------------------------------------------------ C7
def check_C7():
    # (a) matrix identity: 1-plaquette dual U(1) H == F101 rotor, chi=1/(4g^2)
    m_max = 12
    g2 = 0.25                                          # -> chi = 1
    geom = lh.PlaquetteGrid(1, 1)
    lam = 1.0
    Hd, digits = lh.build_dual_hamiltonian(geom, None, g2=g2, lam=lam,
                                           group='U1', m_max=m_max)
    Hr = lh.rotor_hamiltonian(lam, chi=1.0 / (4.0 * g2), m_max=m_max)
    mat_resid = float(np.max(np.abs(Hd.toarray() - Hr)))
    # (b) F101 table contact: sigma_1(lambda=1, chi=1) = 0.29551
    sig1, s1 = lh.rotor_sigma1(1.0, chi=1.0, m_max=24)
    w, v = np.linalg.eigh(Hd.toarray())
    g = v[:, 0]
    s1_dual = float(np.sum(g[:-1] * g[1:]))
    sig1_dual = -np.log(s1_dual)
    table_resid = abs(sig1_dual - 0.29551)
    cross_resid = abs(sig1_dual - sig1)
    # (c) truncation convergence (F101 S1 policy)
    Hd2, _ = lh.build_dual_hamiltonian(geom, None, g2=g2, lam=lam,
                                       group='U1', m_max=m_max + 6)
    w2 = np.linalg.eigvalsh(Hd2.toarray())
    trunc = abs(w[0] - w2[0])
    ok = mat_resid == 0.0 and table_resid < 2e-5 and trunc < 1e-13 \
        and cross_resid < 1e-12
    record("C7", "F101 rotor contact: 1-plaquette dual U(1) Hamiltonian IS "
                 "the compact rotor with chi=1/(4g^2) (matrix identity); "
                 "sigma_1(lam=1,chi=1) reproduces the F101 table 0.29551; "
                 "truncation-converged",
           f"matrix resid {mat_resid:.1e}, sigma_1 {sig1_dual:.5f} "
           f"(table resid {table_resid:.1e}, rotor cross {cross_resid:.1e}), "
           f"trunc {trunc:.1e}", ok)


CHECKS = {"C1": check_C1, "C2": check_C2, "C3": check_C3, "C4": check_C4,
          "C5": check_C5, "C6": check_C6, "C7": check_C7}

if __name__ == "__main__":
    names = sys.argv[1:] or list(CHECKS)
    for n in names:
        CHECKS[n]()
    done = [k for k in CHECKS if k in results["checks"]]
    n_pass = sum(results["checks"][k]["status"] == "PASS" for k in done)
    results["summary"] = f"{n_pass}/{len(done)} PASS ({len(CHECKS)} total)"
    results["runtime_s"] = round(time.time() - t0, 3)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"\n{results['summary']}  ->  {OUT.name}")
