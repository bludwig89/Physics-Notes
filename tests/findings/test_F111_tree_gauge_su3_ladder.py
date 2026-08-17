# test_F111_tree_gauge_su3_ladder.py
# 2026-06-07
#
# F111 -- The two scope items posed by F110, built and verified:
#
#   (I)  3D TREE-GAUGE: real-time Kogut-Susskind link Hamiltonian on 3D
#        lattices.  The planar height trick (F110) does not extend to 3D
#        (Bianchi constraints per cube), but Gauss's law is solved exactly by
#        maximal-tree elimination: E_tree = M . E_off + b(q), with the
#        off-tree electric fields as the free physical variables (cycle
#        space, dim = n_links - n_sites + 1).  Plaquette operators shift the
#        off-tree digits along plaquette cycles; tree consistency
#        c_tree = M . c_off is asserted per plaquette at build time.
#
#   (II) SU(3) CASIMIR LADDER: the electric spectrum of an SU(3) link is the
#        Casimir ladder C2(p,q) = (p^2+q^2+pq+3p+3q)/3.  A gauge-invariant
#        flux chain with static R, Rbar end charges costs (g^2/2)C2(R)L
#        exactly => Casimir scaling sigma_R/sigma_3 = C2(R)/C2(3) = 9/4
#        (adjoint), 5/2 (sextet), 9/2 (decuplet).  The Z3 centre theory sees
#        only N-ality (sigma_q2 = sigma_q1 exactly) -- the F98-F101 A-vs-C
#        dichotomy as two computable laws.  The SU(3) CHARACTER ROTOR
#        H = (g^2/2)C2 - (lam/2)(chi_F + chi_Fbar) extends the F101 rotor
#        from U(1) charges to SU(3) irreps (fusion adjacency = the cos-phi
#        analogue); its strong-coupling law s1 -> lam/(2g^2) is IDENTICAL to
#        the F101 U(1) rotor's 2*lam*chi under the F110 map chi = 1/(4g^2).
#
#   T1  direct-vs-tree spectral identity: unit cube (vacuum + charged) and
#       the 2D reduction (tree builder == F110 dual height builder).
#   T2  3D strong-coupling exactness: lambda=0 gives V(R) = (g^2/2)R on the
#       3x1x1 cube tube (Z3 R=1..3, U1 R=1..2), integer arithmetic.
#   T3  3D PT cross-check: sigma(lam) = g^2/2 - c2 lam^2 + O(lam^3) with c2
#       from programmatic 2nd-order PT on plaquette cycles (2x1x1 tube).
#   T4  3D real-time: unitarity + energy conservation on the cube; quenched
#       string-link flux excess persists at confining coupling.
#   T5  SU(3) ladder data exact: C2, dim, triality, conjugation symmetry,
#       fusion dimension identity (all integer/Fraction, residual 0).
#   T6  Casimir scaling vs N-ality: chain energies exact Fractions, ratios
#       9/4, 5/2, 9/2; singlet constraint certified by division-free
#       Weyl-torus character integration; Z3 engine q=2 == q=1 exactly.
#   T7  SU(3) rotor: strong-coupling s1 -> lam/(2g^2) == U(1) rotor 2*lam*chi
#       (Richardson -> 1); weak-coupling sigma1 ~ lam^(-1/2); cutoff
#       convergence; monotone.
#
# Run:  python test_F111_tree_gauge_su3_ladder.py [T1 T2 ...]   (default all)
# Results accumulate into test-results/F111_tree_gauge_su3_ladder.json

import json
import math
import time
import pathlib
import sys
from fractions import Fraction

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import link_hamiltonian as lh
from casim.engine.gauge import su3_ladder as su

OUT = ROOT / "test-results" / "F111_tree_gauge_su3_ladder.json"
t0 = time.time()

if OUT.exists():
    results = json.loads(OUT.read_text())
else:
    results = {"finding": "F111", "date": "2026-06-07",
               "title": "3D tree-gauge KS link Hamiltonian + SU(3) Casimir "
                        "ladder / character rotor",
               "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement, "residual": str(residual),
        "status": "PASS" if status else "FAIL"}
    print(f"{name}: {statement}\n      -> residual {residual} "
          f"[{'PASS' if status else 'FAIL'}]")


# ------------------------------------------------------------------ T1
def check_T1():
    details = []
    worst = 0.0
    cube = lh.LatticeGraph3D(1, 1, 1)
    for label, charges in (("cube vacuum", None),
                           ("cube charged R=1",
                            {(0, 0, 0): 1, (1, 0, 0): -1})):
        Ht, _, _ = lh.build_tree_hamiltonian(cube, charges, g2=1.0, lam=0.7,
                                             group='Z3')
        Hd, n_phys = lh.build_direct_zn_graph(cube, g2=1.0, lam=0.7, N=3,
                                              charges=charges)
        assert n_phys == Ht.shape[0]
        wt = np.sort(np.linalg.eigvalsh(Ht.toarray()))
        wd = np.sort(np.linalg.eigvalsh(Hd.toarray()))
        r = float(np.max(np.abs(wt - wd)))
        worst = max(worst, r)
        details.append(f"{label}: dim {n_phys}, max|dE| {r:.2e}")
    # 2D reduction: tree-gauge builder == F110 dual height builder
    gg = lh.LatticeGraph3D(2, 2, 0)
    geom = lh.PlaquetteGrid(2, 2)
    Ha, _, _ = lh.build_tree_hamiltonian(gg, None, g2=1.0, lam=0.7,
                                         group='Z3')
    Hb, _ = lh.build_dual_hamiltonian(geom, None, g2=1.0, lam=0.7,
                                      group='Z3')
    wa = np.sort(np.linalg.eigvalsh(Ha.toarray()))
    wb = np.sort(np.linalg.eigvalsh(Hb.toarray()))
    r2d = float(np.max(np.abs(wa - wb)))
    worst = max(worst, r2d)
    details.append(f"2D tree==F110 dual: dim {Ha.shape[0]}, max|dE| {r2d:.2e}")
    record("T1", "tree-gauge construction == direct link-basis Gauss sector "
                 "(unit cube, vacuum + charged) and == F110 dual height "
                 "representation in the 2D reduction (full spectra)",
           "; ".join(details), worst < 1e-12)


# ------------------------------------------------------------------ T2
def check_T2():
    tube = lh.LatticeGraph3D(3, 1, 1)
    v0 = lh.tree_lambda0_min(tube, None, g2=1.0, group='Z3')
    worst = 0.0
    for R in (1, 2, 3):
        v = lh.tree_lambda0_min(tube, {(0, 0, 0): 1, (R, 0, 0): -1},
                                g2=1.0, group='Z3')
        worst = max(worst, abs((v - v0) - 0.5 * R))
    tube2 = lh.LatticeGraph3D(2, 1, 1)
    v0u = lh.tree_lambda0_min(tube2, None, g2=1.0, group='U1', m_max=1)
    for R in (1, 2):
        v = lh.tree_lambda0_min(tube2, {(0, 0, 0): 1, (R, 0, 0): -1},
                                g2=1.0, group='U1', m_max=1)
        worst = max(worst, abs((v - v0u) - 0.5 * R))
    record("T2", "3D strong-coupling exactness: lambda=0 V(R) = (g^2/2)R on "
                 "the cube tube (Z3 3x1x1 R=1..3, U1 2x1x1 R=1..2; integer "
                 "arithmetic)",
           f"max |V - g^2 R/2| = {worst:.1e}", worst == 0.0)


# ------------------------------------------------------------------ T3
def check_T3():
    tube = lh.LatticeGraph3D(2, 1, 1)
    c2 = lh.sigma_strong_pt2_graph(
        tube, {(0, 0, 0): 1, (2, 0, 0): -1}, {(0, 0, 0): 1, (1, 0, 0): -1},
        g2=1.0, group='Z3')
    lams = (0.025, 0.05, 0.1)
    ratios = []
    for lam in lams:
        V = lh.static_potential_3d(lambda: tube, [1, 2], g2=1.0, lam=lam,
                                   group='Z3')
        sigma_ed = V[2] - V[1]
        ratios.append((0.5 - sigma_ed) / (c2 * lam ** 2))
    rich = [2 * ratios[i] - ratios[i + 1] for i in range(2)]
    ok = abs(rich[0] - 1.0) < 0.01 and abs(ratios[0] - 1.0) < 0.05
    record("T3", "3D strong-coupling PT cross-check: sigma(lam) = g^2/2 - "
                 "c2 lam^2 + O(lam^3), c2 from plaquette-cycle 2nd-order PT "
                 "(2x1x1 tube, Richardson removes the Z3 winding term)",
           f"c2 = {c2:.6f}; ratios {[round(r, 5) for r in ratios]} "
           f"(lam={lams}); Richardson -> {[round(r, 5) for r in rich]}", ok)


# ------------------------------------------------------------------ T4
def check_T4():
    cube = lh.LatticeGraph3D(1, 1, 1)
    charges = {(0, 0, 0): 1, (1, 0, 0): -1}
    lam = 0.3                                      # confining on this volume
    Hv, _, Ev = lh.build_tree_hamiltonian(cube, None, g2=1.0, lam=lam,
                                          group='Z3')
    _, psiv = lh.ground_state(Hv)
    prof_vac = lh.link_E2_profile(psiv, Ev)
    H, _, E_vals = lh.build_tree_hamiltonian(cube, charges, g2=1.0, lam=lam,
                                             group='Z3')
    # string link = the x link (0,0,0)->(1,0,0)
    s_link = cube.link_id[('x', 0, 0, 0)]
    # (a) ground-state flux tube: excess localised on the string link
    _, psig = lh.ground_state(H)
    exg = lh.link_E2_profile(psig, E_vals) - prof_vac
    gs_share = float(exg[s_link] / exg.sum())
    # (b) real-time quench of the bare string (digits-0 basis state)
    psi = np.zeros(H.shape[0]); psi[0] = 1.0
    assert E_vals[0, s_link] == 1 and np.sum(E_vals[0] ** 2) == 1
    t_grid = np.linspace(0.0, 20.0, 21)
    traj = lh.evolve_krylov(H, psi, t_grid)
    norms = np.linalg.norm(traj, axis=1)
    ens = np.array([lh.energy_expect(H, traj[n]) for n in range(len(t_grid))])
    norm_drift = float(np.max(np.abs(norms - 1.0)))
    en_drift = float(np.max(np.abs(ens - ens[0])))
    psi_dense = lh.evolve_dense(H, psi, [t_grid[-1]])[0]
    kry_err = float(np.linalg.norm(traj[-1] - psi_dense))
    exq = np.mean([lh.link_E2_profile(traj[n], E_vals) - prof_vac
                   for n in range(1, len(t_grid))], axis=0)
    contrast = float(exq[s_link] / np.max(np.delete(exq, s_link)))
    ok = (norm_drift < 1e-12 and en_drift < 1e-11 and kry_err < 1e-10
          and gs_share > 0.7 and exq[s_link] > 0
          and contrast > 4.0)
    record("T4", "3D real-time on the unit cube (lam=0.3): unitary, "
                 "energy-conserving (Krylov certified vs dense); ground-state "
                 "flux tube localised on the string link; quenched bare "
                 "string keeps its excess there (>4x any other link)",
           f"norm drift {norm_drift:.1e}, energy drift {en_drift:.1e}, "
           f"|Krylov - dense| {kry_err:.1e}, GS share {gs_share:.4f}, "
           f"quench excess {exq[s_link]:.4f} ({contrast:.1f}x next link)",
           ok)


# ------------------------------------------------------------------ T5
def check_T5():
    known = {(0, 0): (1, Fraction(0)), (1, 0): (3, Fraction(4, 3)),
             (0, 1): (3, Fraction(4, 3)), (1, 1): (8, Fraction(3)),
             (2, 0): (6, Fraction(10, 3)), (3, 0): (10, Fraction(6)),
             (2, 1): (15, Fraction(16, 3))}
    bad = 0
    for r, (d, c) in known.items():
        if su.dim_irrep(*r) != d or su.casimir2(*r) != c:
            bad += 1
    conj_bad = sum(1 for r in su.irrep_ladder(8)
                   if su.casimir2(*r) != su.casimir2(*su.conjugate(*r)))
    fus = su.fusion_dim_identity_residual(8)
    tri = (su.triality(1, 0), su.triality(0, 1), su.triality(2, 0),
           su.triality(1, 1))
    ladder = su.irrep_ladder(6)
    c2s = [su.casimir2(*r) for r in ladder]
    mono = all(a <= b for a, b in zip(c2s, c2s[1:]))
    ok = (bad == 0 and conj_bad == 0 and fus == 0
          and tri == (1, 2, 2, 0) and mono)
    record("T5", "SU(3) electric Casimir ladder exact: C2=(p^2+q^2+pq+3p+3q)/3 "
                 "and dims match the standard table (Fractions); conjugation "
                 "symmetry; fusion dimension identity sum(dim F x R) = 3 dim R; "
                 "trialities; ladder sorted by C2",
           f"table errors {bad}, conj errors {conj_bad}, fusion-dim residual "
           f"{fus}, trialities {tri}, ladder monotone {mono}", ok)


# ------------------------------------------------------------------ T6
def check_T6():
    # (a) chain energies and Casimir scaling -- exact Fractions
    tab = su.casimir_scaling_table()
    ratios = {k: v[2] for k, v in tab.items()}
    exact = (ratios['8'] == Fraction(9, 4) and ratios['6'] == Fraction(5, 2)
             and ratios['10'] == Fraction(9, 2) and ratios['15'] == Fraction(4)
             and ratios['3bar'] == 1)
    chain_ok = all(su.chain_energy(R, L) ==
                   Fraction(1, 2) * su.casimir2(*R) * L
                   for R in ((1, 0), (1, 1), (2, 0), (3, 0))
                   for L in (1, 2, 5))
    # (b) the chain constraint (singlet iff B = Abar) certified on the torus
    worst_t = 0.0
    reps = su.irrep_ladder(3)
    for A in reps:
        for B in reps:
            v = su.singlet_multiplicity_torus(A, B)
            worst_t = max(worst_t, abs(v - su.singlet_in_product(A, B)))
    # (c) the Z3 N-ality contrast: q=2 string == q=1 string EXACTLY
    geom = lh.PlaquetteGrid(6, 1)
    eta1, _ = geom.background_string(1, 4, 0, q=1)
    eta2, _ = geom.background_string(1, 4, 0, q=2)
    H1, _ = lh.build_dual_hamiltonian(geom, eta1, g2=1.0, lam=0.5, group='Z3')
    H2, _ = lh.build_dual_hamiltonian(geom, eta2, g2=1.0, lam=0.5, group='Z3')
    w1 = np.sort(np.linalg.eigvalsh(H1.toarray()))
    w2 = np.sort(np.linalg.eigvalsh(H2.toarray()))
    nality = float(np.max(np.abs(w1 - w2)))
    ok = exact and chain_ok and worst_t < 1e-12 and nality < 1e-12
    record("T6", "Casimir scaling vs N-ality (the F98-F101 A-vs-C dichotomy, "
                 "both laws computed): SU(3) chain sigma_R/sigma_3 = 9/4 "
                 "(8), 5/2 (6), 9/2 (10), 4 (15) exact Fractions, chain "
                 "constraint certified by torus character integration; Z3 "
                 "centre theory q=2 isospectral to q=1 (full spectra)",
           f"ratios exact {exact}, chain exact {chain_ok}, torus worst "
           f"{worst_t:.1e} (100 pairs), Z3 q2-vs-q1 max|dE| {nality:.1e}",
           ok)
    results.setdefault("tables", {})["casimir_ratios"] = \
        {k: str(v) for k, v in ratios.items()}


# ------------------------------------------------------------------ T7
def check_T7():
    g2 = 1.0
    # cutoff convergence at the moderate coupling
    s_cuts = [su.su3_rotor_sigma1(g2, 1.0, cut)[0] for cut in (10, 14, 18)]
    trunc = max(abs(s_cuts[0] - s_cuts[2]), abs(s_cuts[1] - s_cuts[2]))
    # strong coupling: s1 -> lam/(2 g^2), the F101 U(1) rotor law 2*lam*chi
    # at chi = 1/(4g^2); the subleading term is linear -> Richardson
    lams = (0.003, 0.001)
    rat = [su.su3_rotor_sigma1(g2, lam, 12)[1] / (lam / (2.0 * g2))
           for lam in lams]
    rich = (3.0 * rat[1] - rat[0]) / 2.0
    # direct numerical contact with the F101 U(1) rotor at the same map
    chi = 1.0 / (4.0 * g2)
    s1_u1 = lh.rotor_sigma1(0.001, chi=chi, m_max=20)[1]
    s1_su3 = su.su3_rotor_sigma1(g2, 0.001, 12)[1]
    cross = abs(s1_su3 / s1_u1 - 1.0)
    # weak coupling: sigma1 ~ lam^(-1/2)
    sa = su.su3_rotor_sigma1(g2, 200.0, 30)[0]
    sb = su.su3_rotor_sigma1(g2, 2000.0, 40)[0]
    slope = (math.log(sb) - math.log(sa)) / (math.log(2000.0) - math.log(200.0))
    # monotone
    sig_seq = [su.su3_rotor_sigma1(g2, lam, 16)[0]
               for lam in (0.05, 0.2, 1.0, 5.0)]
    mono = all(a > b for a, b in zip(sig_seq, sig_seq[1:]))
    ok = (trunc < 1e-12 and abs(rich - 1.0) < 1e-3 and cross < 5e-3
          and abs(slope + 0.5) < 0.01 and mono)
    record("T7", "SU(3) character rotor: strong-coupling law s1 -> "
                 "lam/(2g^2) -- IDENTICAL to the F101 U(1) rotor 2*lam*chi "
                 "under the F110 map chi=1/(4g^2) (group changes the Casimir "
                 "ladder, not the leading log); weak-coupling sigma1 ~ "
                 "lam^(-1/2); truncation-converged; monotone",
           f"trunc {trunc:.1e}; strong ratios {[round(r, 5) for r in rat]} "
           f"Richardson {rich:.6f}; U(1) cross {cross:.1e}; weak log-slope "
           f"{slope:.4f}; sigma1(lam=1) {s_cuts[-1]:.5f}", ok)
    results.setdefault("tables", {})["su3_rotor_sigma1"] = \
        {str(l): su.su3_rotor_sigma1(g2, l, 16)[0]
         for l in (0.05, 0.2, 1.0, 5.0)}


CHECKS = {"T1": check_T1, "T2": check_T2, "T3": check_T3, "T4": check_T4,
          "T5": check_T5, "T6": check_T6, "T7": check_T7}

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
