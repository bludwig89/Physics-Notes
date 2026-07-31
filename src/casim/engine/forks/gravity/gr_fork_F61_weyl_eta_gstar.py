"""
F61 — Deriving the Weyl-spinor heat-kernel coefficient eta and the gravitating
      mode count g_*, turning F59's placeholder P_pre = sqrt(2 pi eta g_*) into a
      number.

Part A — eta from the Seeley-DeWitt a_1 coefficient (analytic, verified here by
         exact rational arithmetic).
  Convention (F59): 1/(16 pi G)_per dof = eta * INT d3k/(2pi)^3 /(2 omega).
  Flat-space:       INT_{|k|<Lam} d3k/(2pi)^3 /(2 omega) = Lam^2/(8 pi^2)  (c=1),
                    spin-INDEPENDENT (same omega for a scalar or each Weyl comp).
  Heat kernel:      1/(16 pi G)_per dof = c_dof * Lam^2/(4 pi)^2,
                    so  eta_dof = c_dof / 2,  with c = a_1/R (statistics-signed),
                    normalised so a minimal real scalar has c_0 = 1/6.
  Seeley-DeWitt a_1 for a Laplace-type op  -Box + E  on a bundle:
                    a_1 = (1/6) R * tr(1) - tr(E).
    * minimal real scalar: E=0, tr1=1  -> a_1 = R/6      -> c_scalar = +1/6.
    * Dirac (Lichnerowicz slashedD^2 = -Box + R/4, tr1_4 = 4, fermionic sign -1):
        a_1 = (4/6 - 4/4) R = -R/3 ;  c_Dirac = -(a_1/R) = +1/3.
    * Weyl = half a Dirac:  c_Weyl = +1/6  ->  eta_Weyl = 1/12.
  => eta_Weyl = 1/12, i.e. F59's placeholder was the exact per-Weyl value.

Part B — g_*: number of 2-component Weyl fields that gravitate, from the model's
         first-generation content (first-gen-completeness.md Table 1).

Part C — assemble P_pre = sqrt(2 pi * sum eta_i) = sqrt(pi g_* / 6) and the
         resulting (a, tau) for d=3.

Real arithmetic only -> numpy safe per CLAUDE.md.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as Fr
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
_THIS = os.path.dirname(os.path.abspath(__file__))
# allow importing ca_bcc when run from the project tree (optional, for Part A check)
for p in (_THIS, os.path.abspath(os.path.join(_THIS, "..")),
          os.path.abspath(os.path.join(_THIS, "..", "ca-simulation"))):
    if p not in sys.path:
        sys.path.insert(0, p)


# ----- Part A: heat-kernel coefficients via exact rational arithmetic --------
def a1_over_R(trace_dim, E_over_R):
    """Seeley-DeWitt a_1/R for operator -Box + E on a bundle of dim trace_dim,
    with endomorphism E = (E_over_R) * R * 1.   a_1 = (1/6) R tr1 - tr E."""
    return Fr(1, 6) * trace_dim - E_over_R * trace_dim

def heat_kernel_table():
    rows = {}
    # minimal real scalar
    a1 = a1_over_R(Fr(1), Fr(0)); c = a1                      # boson: c = +a1/R
    rows["scalar_min"] = {"a1_over_R": a1, "c": c, "eta": c/2}
    # Dirac fermion: trace 4, E = R/4, fermionic sign flips overall -> c = -a1/R
    a1d = a1_over_R(Fr(4), Fr(1, 4)); cD = -a1d
    rows["dirac"] = {"a1_over_R": a1d, "c": cD, "eta": cD/2}
    # Weyl = half Dirac
    cW = cD / 2
    rows["weyl"] = {"a1_over_R": a1d/2, "c": cW, "eta": cW/2}
    return rows


# ----- Part A check: the BCC 2-spinor's two eigenphases share one |omega| -----
def eigenphase_symmetry(n_samples=4000, seed=0):
    """The spin-independence of the phase-space factor INT 1/(2 omega) rests on
    the BCC Weyl 2x2 unitary U(k) having eigenphases +/- omega with EQUAL
    magnitude, so each spinor component contributes the same 1/(2 omega) as a
    scalar with that dispersion.  Sample the BZ, diagonalise U(k), confirm
    | |arg(lam1)| - |arg(lam2)| | = 0 to machine precision.  Returns max residual
    and the per-component INT 1/(2w) over the BCC dispersion (the actual number)."""
    try:
        import ca_bcc as bcc
    except Exception:
        return {"available": False}
    rng = np.random.default_rng(seed)
    kmax = 0.6*np.sqrt(3.0)
    K = rng.uniform(-kmax, kmax, size=(n_samples, 3))
    max_res = 0.0
    for kx, ky, kz in K:
        Uff, Ufg, Ugf, Ugg = bcc.bcc_unitary(kx, ky, kz)
        M = np.array([[Uff, Ufg], [Ugf, Ugg]], dtype=complex)
        w = np.linalg.eigvals(M)
        max_res = max(max_res, abs(abs(np.angle(w[0])) - abs(np.angle(w[1]))))
    # per-component phase-space integral over the actual BCC dispersion
    Lam, ng = 0.8*np.pi, 110
    g = np.linspace(-Lam, Lam, ng, endpoint=False) + Lam/ng
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    kk = np.sqrt(KX**2+KY**2+KZ**2); om = bcc.bcc_dispersion(KX, KY, KZ)
    I = np.where((kk < Lam) & (om > 1e-12), 1.0/(2*om), 0.0).sum()*(g[1]-g[0])**3/(2*np.pi)**3
    return {"available": True, "eigenphase_abs_diff_max": float(max_res),
            "intphase_per_component_BCC": float(I)}


# ----- Part B: gravitating Weyl count for the model's first generation -------
def gstar_table():
    # first-gen-completeness.md Table 1 (SM content, Higgs-free SU(2))
    content = [
        ("L=(nu,e)_L", 1, 2),   # color 1, SU(2) doublet => 2 Weyl
        ("e_R",        1, 1),
        ("Q=(u,d)_L",  3, 2),   # color 3, doublet => 6 Weyl
        ("u_R",        3, 1),
        ("d_R",        3, 1),
    ]
    n_charged = sum(col*iso for _, col, iso in content)         # 15
    return {"per_field": [{"field": f, "weyl": col*iso} for f, col, iso in content],
            "g_charged_15": n_charged,
            "g_with_nuR_16": n_charged + 1,                     # sterile nu_R
            "g_three_gen_48": 3*(n_charged + 1)}


# ----- Part C: assemble -------------------------------------------------------
def assemble(g_star, eta=Fr(1, 12), d=3):
    P = np.sqrt(float(2*np.pi*eta*g_star))
    return {"g_star": g_star, "P_pre": P,
            "a_over_ellP": P*d**0.25, "tau_over_tP": P*d**-0.25,
            "invariant_over_ellP": P}


if __name__ == "__main__":
    res = {}
    print("=== Part A: heat-kernel coefficients (exact rationals) ===")
    hk = heat_kernel_table()
    res["heat_kernel"] = {k: {kk: str(vv) for kk, vv in v.items()} for k, v in hk.items()}
    for name, v in hk.items():
        print(f"  {name:11s}: a1/R={str(v['a1_over_R']):>5}  c={str(v['c']):>4}  eta={str(v['eta'])}")
    assert hk["weyl"]["eta"] == Fr(1, 12), "Weyl eta must be 1/12"
    print("  -> eta_Weyl = 1/12 (confirms F59 placeholder exactly)")

    print("\n=== Part A check: BCC 2-spinor eigenphases share one |omega| ===")
    ps = eigenphase_symmetry()
    res["phase_space"] = ps
    if ps.get("available"):
        print(f"  max | |arg lam1| - |arg lam2| | = {ps['eigenphase_abs_diff_max']:.2e} "
              f"(=> both Weyl components share one dispersion magnitude)")
        print(f"  per-component INT 1/(2w) over BCC dispersion = {ps['intphase_per_component_BCC']:.6f}")
    else:
        print("  ca_bcc not importable in this run; skipped (run from project tree).")

    print("\n=== Part B: gravitating Weyl count ===")
    gt = gstar_table()
    res["gstar"] = gt
    for r in gt["per_field"]:
        print(f"  {r['field']:11s}: {r['weyl']} Weyl")
    print(f"  charged g_*=15 ; with nu_R g_*=16 ; three generations g_*=48")

    print("\n=== Part C: assemble P_pre and (a,tau) at d=3 ===")
    res["assembly"] = {}
    for label, g in [("minimal_2", 2), ("one_gen_15", 15), ("one_gen_nuR_16", 16),
                     ("three_gen_48", 48)]:
        A = assemble(g)
        res["assembly"][label] = A
        print(f"  g_*={g:2d}: P_pre={A['P_pre']:.3f}  a={A['a_over_ellP']:.3f} ellP  "
              f"tau={A['tau_over_tP']:.3f} tP  sqrt(a.ctau)={A['invariant_over_ellP']:.3f} ellP")

    with open(os.path.join(OUT, "f61_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("\nwrote f61_results.json")
