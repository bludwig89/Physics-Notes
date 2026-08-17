"""thermodynamics.py — lattice-native statistical mechanics (rubric row G10).

**Rubric row G10**, the last `ABSENT` row of
`docs/status/completeness-2026-08-04.md` after F297 closed K2.  The row reads:

    Temperature enters cosmology and superconductivity as an external
    parameter; no lattice-native thermodynamics.  18 findings mention
    entropy, all of it black-hole or information entropy.

Both halves are true and this module addresses both.  Nothing here introduces
new physics: every ingredient is a quantity the tree already derived.  That is
the point — the 2026-08-04 report's own amendment argued the remaining ABSENT
rows should be read as *assembly* problems, and that an assembled sector is a
review instrument because it forces old inputs through an observation that was
never applied to them.  This assembly does that to one input in particular:
**F297's thermal history assumed the continuum `rho = (pi^2/30) g T^4` and
`p = rho/3`, and nothing in the tree had ever checked that the lattice supplies
them.**  Section A checks it, and quantifies the margin.

WHAT IS MODEL-NATIVE AND WHAT IS NOT
------------------------------------
MODEL-NATIVE (derived in this tree, nothing imported):

  * the dispersion            — `Omega_pair(k) = omega^+(k/2) + omega^-(k/2)`,
                                the paired-spinor photon (F67/F68/F69), itself
                                built from the BCC Weyl walk (F26).  Every
                                thermodynamic quantity below is a Brillouin-zone
                                integral over THIS function and no other.
  * `c_lat = 1/sqrt3`         — F26.  Appears only through the dispersion.
  * `a = 6.5978 ell_P`        — F107, the SI ruler.  Sets the tick and hence the
                                one temperature scale in the problem.
  * the unitary walk          — `bcc_unitary`, F26.  Sections B/C run on it.

EXTERNAL INPUT (not derived, not claimed to be):

  * `k_B`, `hbar`, `c`, `ell_P` — unit conversions.  `k_B` is exact by SI
    definition and is a *ruler for temperature*, not physics; it is carried as a
    module literal exactly as `superconductivity.py`, `horizon_entropy.py`,
    `blackhole.py` and `qed_casimir_materials.py` already do.  It is NOT in the
    D7 registry, and adding it there with all six sites is a named mechanical
    follow-up (see the finding), not something this module should do silently.
  * `T_CMB`, BBN temperatures — the comparison points in section A5, quoted from
    observation to state a margin.  No result depends on their values.

THE FOUR SECTIONS
-----------------
A. EQUATION OF STATE.  Build `Z(beta)` from the derived dispersion.  The
   low-`k` expansion of `Omega_pair` is obtained in closed form; the leading
   lattice corrections to `u`, `p/u` and `s` then follow in closed form too,
   and are confirmed against direct Brillouin-zone quadrature.  Result: the
   continuum radiation EoS is a *theorem* of the model, with a computed
   correction that is 45 orders of magnitude below anything BBN or the CMB
   could see.

B. THE SECOND LAW.  Fine-grained von Neumann entropy is exactly conserved by
   the model's own walk (measured on a MIXED state, so the statement is not the
   trivial `S = 0` of a pure state).  Coarse-grained entropy rises.  The
   increase survives its controls, including time reversal — which is the
   honest lattice-native statement: the arrow is in the initial condition and
   the coarse-graining, not in the dynamics.

C. WHAT DOES *NOT* HAPPEN.  The free sector cannot reach a Gibbs state: the
   branch occupations `n_pm(k)` are exactly conserved, so there are `2N`
   conserved charges and the stationary ensemble is a GGE.  Measured: the
   coarse-grained plateau approaches the GGE prediction as the subsystem
   fraction falls (0.554 -> 0.901 -> 0.987 -> 0.998).  True thermalisation needs
   the interacting sector, i.e. the F110 link Hamiltonian.  Named, not waved at.

D. THE CELL CONSTANT (rubric E9 / F190).  F190's open step is written as "show
   a boundary cell carries `e^(2 pi sqrt3)` states from the BCC/Weyl content".
   That step is impossible as written and this module says why in one line:
   `e^(2 pi sqrt3)` is not an integer.  What survives, and what replaces it, is
   in `cell_capacity()`.

Everything is reported by `check_g10()`.  Run as `__main__` to write the
artifact.
"""

from __future__ import annotations

import math

import numpy as np

from casim.numerics import xp  # noqa: F401  (D8: array namespace of record)
from casim.constants import c_lat, ell_P_m, c_SI, hbar_SI, a_over_ellP
from casim.engine.gauge.photon import pair_dispersion
from casim.engine.lattice.bcc import bcc_unitary

# --- external unit rulers -------------------------------------------------
# k_B is exact by SI definition (2019 redefinition).  Not a D7 registry symbol
# today; see the module docstring.
K_B_SI = 1.380649e-23          # J / K   (exact)

C = float(c_lat)               # 1/sqrt3
G_POL = 2.0                    # photon polarisations


# ==========================================================================
#  A.  EQUATION OF STATE
# ==========================================================================
#
#  A1.  The closed-form low-k expansion of the DERIVED pair dispersion.
#
#       Omega_pair(k) = c_lat |k| [ 1 - A(nhat) |k|^2 ] + O(|k|^5)
#
#       with, writing S2 = sum_{i<j} n_i^2 n_j^2 and P3 = (n_x n_y n_z)^2,
#
#       A(nhat) = S2/72 + P3/24 .
#
#  Two structural facts fall out and both are checked below:
#    * A vanishes identically along <100>: the pair dispersion is EXACTLY
#      linear along a cubic axis, at every |k|, not just asymptotically.
#    * the odd (branch-asymmetric) term cancels in the (+,-) sum, which is the
#      F67/F68 non-birefringence statement seen from the thermodynamic side.

def A_anisotropy(nx, ny, nz):
    """Leading anisotropic softening coefficient A(nhat).  nhat must be unit."""
    s2 = nx * nx * ny * ny + nx * nx * nz * nz + ny * ny * nz * nz
    p3 = (nx * ny * nz) ** 2
    return s2 / 72.0 + p3 / 24.0


MEAN_A_EXACT = 1.0 / 315.0
"""<A> over the unit sphere.  Exact: <n_i^2 n_j^2> = 1/15 (i != j) gives
3/(15*72) = 1/360, and <n_x^2 n_y^2 n_z^2> = 1/105 gives 1/2520; the sum is
8/2520 = 1/315."""


def dispersion_expansion(n_dirs=400, k_probe=(0.02, 0.05), seed=0):
    """A1: check the closed form against the model's own `pair_dispersion`.

    The residual must be O(|k|^4) *relative*, i.e. the next term in the series,
    not a constant offset.  Reported as sup |residual| / |k|^4.
    """
    rng = np.random.default_rng(seed)
    worst = 0.0
    axis_max = 0.0
    for _ in range(n_dirs):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        A = A_anisotropy(*n)
        for K in k_probe:
            om = float(pair_dispersion(*(K * n)))
            pred = C * K * (1.0 - A * K * K)
            worst = max(worst, abs(om - pred) / (C * K) / K ** 4)
    # <100> exactness, all the way out
    for K in (0.1, 0.5, 1.0, 2.0, 3.0):
        om = float(pair_dispersion(K, 0.0, 0.0))
        axis_max = max(axis_max, abs(om - C * K) / (C * K))
    return {"rel_residual_over_k4": worst, "axis_100_max_rel": axis_max}


def mean_anisotropy(n_theta=200, n_phi=400):
    """A2: <A> over the sphere, by quadrature, against the exact 1/315."""
    x, w = np.polynomial.legendre.leggauss(n_theta)
    ph = (np.arange(n_phi) + 0.5) * 2.0 * np.pi / n_phi
    tot = 0.0
    for xi, wi in zip(x, w):
        s = math.sqrt(1.0 - xi * xi)
        tot += wi * float(np.sum(A_anisotropy(s * np.cos(ph), s * np.sin(ph),
                                              np.full(n_phi, xi))))
    tot *= 2.0 * np.pi / n_phi
    val = tot / (4.0 * np.pi)
    return {"mean_A": val, "exact": MEAN_A_EXACT,
            "rel_err": abs(val / MEAN_A_EXACT - 1.0)}


# ---- A3.  The closed-form corrections -----------------------------------
#
#  With Omega = c k (1 - A k^2), Bose occupation at dimensionless
#  Theta = k_B T tau / hbar, and the two Bose integrals
#
#      int_0^inf x^3/(e^x - 1) dx = pi^4/15 ,
#      int_0^inf x^5/(e^x - 1) dx = 8 pi^6/63 ,
#
#  the leading relative corrections are pure numbers times Theta^2:
#
#      u / u_SB - 1 = (200 pi^2 / 21) <A> Theta^2 / c^2  =  (40 pi^2/441) Theta^2
#      1/3 - p/u    = ( 80 pi^2 / 63) <A> Theta^2 / c^2  =  (16 pi^2/1323) Theta^2
#      s / s_SB - 1 =                                       ( 4 pi^2/49)  Theta^2
#
#  and therefore the parameter-free ratio  C_u / C_w = 15/2, EXACTLY.
#
#  Pressure is the momentum-flux definition p = (1/3V) sum_k n_B (k . grad_k
#  Omega) — the one that enters T^{ij} and therefore the Einstein equation.  On
#  a rigid substrate that is the physically meaningful pressure; -dF/dV is not,
#  because the substrate's volume is not a thermodynamic variable.

C_U_EXACT = 40.0 * math.pi ** 2 / 441.0
C_W_EXACT = 16.0 * math.pi ** 2 / 1323.0
C_S_EXACT = 4.0 * math.pi ** 2 / 49.0


def _angular_grid(n_theta=48, n_phi=96):
    xt, wt = np.polynomial.legendre.leggauss(n_theta)
    ph = (np.arange(n_phi) + 0.5) * 2.0 * np.pi / n_phi
    wph = 2.0 * np.pi / n_phi
    NX, NY, NZ, W = [], [], [], []
    for xi, wi in zip(xt, wt):
        s = math.sqrt(1.0 - xi * xi)
        NX.append(s * np.cos(ph))
        NY.append(s * np.sin(ph))
        NZ.append(np.full(n_phi, xi))
        W.append(np.full(n_phi, wi * wph))
    return (np.concatenate(NX), np.concatenate(NY),
            np.concatenate(NZ), np.concatenate(W))


def photon_eos(theta, x_max=45.0, n_r=300, n_theta=48, n_phi=96,
               linear_control=False):
    """Energy density, pressure and entropy density of the photon gas at Theta.

    Direct quadrature over the model's own dispersion.  `linear_control=True`
    replaces it by the exactly linear `c|k|` — the control under which every
    lattice-correction check below MUST go red.
    """
    NX, NY, NZ, W = _angular_grid(n_theta, n_phi)
    xr, wr = np.polynomial.legendre.leggauss(n_r)
    k_max = x_max * theta / C
    k = 0.5 * k_max * (xr + 1.0)
    wk = 0.5 * k_max * wr
    KX, KY, KZ = np.outer(k, NX), np.outer(k, NY), np.outer(k, NZ)

    if linear_control:
        Om = C * np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2)
        kdg = Om.copy()                       # Euler: homogeneous of degree 1
    else:
        Om = pair_dispersion(KX, KY, KZ)
        h = 1e-3                              # 4th-order radial derivative
        def _d(f):
            return pair_dispersion(KX * f, KY * f, KZ * f)
        kdg = (_d(1 - 2 * h) - 8.0 * _d(1 - h)
               + 8.0 * _d(1 + h) - _d(1 + 2 * h)) / (12.0 * h)

    with np.errstate(over="ignore"):
        nB = 1.0 / np.expm1(Om / theta)
    wgt = (wk[:, None] * W[None, :]) * (k ** 2)[:, None]
    pref = G_POL / (2.0 * np.pi) ** 3
    u = pref * float(np.sum(wgt * Om * nB))
    p = pref / 3.0 * float(np.sum(wgt * kdg * nB))
    u_sb = G_POL * np.pi ** 2 * theta ** 4 / (30.0 * C ** 3)
    s_sb = 4.0 / 3.0 * u_sb / theta
    return {"theta": theta, "u": u, "p": p, "w": p / u,
            "s": (u + p) / theta,
            "u_over_SB": u / u_sb, "s_over_SB": ((u + p) / theta) / s_sb}


def eos_coefficients(thetas=(0.002, 0.005, 0.01, 0.02), linear_control=False):
    """A3/A4: measure C_u, C_w, C_s and compare with the closed forms."""
    rows = []
    for th in thetas:
        r = photon_eos(th, linear_control=linear_control)
        rows.append({"theta": th,
                     "du_over_u": r["u_over_SB"] - 1.0,
                     "third_minus_w": 1.0 / 3.0 - r["w"],
                     "ds_over_s": r["s_over_SB"] - 1.0,
                     "Cu_meas": (r["u_over_SB"] - 1.0) / th ** 2,
                     "Cw_meas": (1.0 / 3.0 - r["w"]) / th ** 2,
                     "Cs_meas": (r["s_over_SB"] - 1.0) / th ** 2})
    cu = float(np.mean([r["Cu_meas"] for r in rows]))
    cw = float(np.mean([r["Cw_meas"] for r in rows]))
    cs = float(np.mean([r["Cs_meas"] for r in rows]))
    return {"rows": rows,
            "Cu_meas": cu, "Cu_exact": C_U_EXACT,
            "Cu_rel": abs(cu / C_U_EXACT - 1.0),
            "Cw_meas": cw, "Cw_exact": C_W_EXACT,
            "Cw_rel": abs(cw / C_W_EXACT - 1.0),
            "Cs_meas": cs, "Cs_exact": C_S_EXACT,
            "Cs_rel": abs(cs / C_S_EXACT - 1.0),
            "ratio_meas": cu / cw, "ratio_exact": 7.5,
            "ratio_rel": abs(cu / cw / 7.5 - 1.0)}


def boundary_independence(theta=0.005, x_maxes=(45.0, 60.0, 75.0)):
    """A4 control: the Brillouin-zone BOUNDARY does not enter.

    The occupation is exponentially small at the zone edge, so the EoS in the
    `Theta << 1` regime cannot depend on where the radial domain is cut.  This
    is what lets section A quote a result without first settling the shape of
    the paired photon's zone — an honest scope limit, made into a measurement.
    """
    vals = [photon_eos(theta, x_max=xm)["u_over_SB"] - 1.0 for xm in x_maxes]
    spread = max(vals) - min(vals)
    return {"x_maxes": list(x_maxes), "du_over_u": vals,
            "spread": spread, "rel_spread": spread / abs(vals[-1])}


# ---- A5.  The one temperature scale, and the margins ---------------------

def lattice_scales():
    """The tick, and the temperature at which Theta = 1."""
    a_m = a_over_ellP * ell_P_m
    tau_s = a_m / (c_SI * math.sqrt(3.0))      # a/tau = c sqrt3 (F107 option C)
    T_lat = hbar_SI / (K_B_SI * tau_s)
    return {"a_m": a_m, "tau_s": tau_s, "T_lattice_K": T_lat,
            "E_lattice_GeV": hbar_SI / tau_s / 1.602176634e-10}


def cosmology_margins():
    """A5: what the lattice correction is worth where the tree actually uses it.

    F297 (BBN) and every cosmology finding in the tree assume `w = 1/3` and the
    continuum Stefan-Boltzmann `u(T)`.  This turns that assumption into a
    number with an error bar.
    """
    T_lat = lattice_scales()["T_lattice_K"]
    pts = {"CMB (2.7255 K)": 2.7255,
           "BBN, T9 = 1 (1e9 K)": 1.0e9,
           "BBN, 1 MeV (1.1605e10 K)": 1.16045e10,
           "QCD crossover (1.7e12 K)": 1.7e12,
           "electroweak (1.6e15 K)": 1.6e15}
    out = {}
    for lab, T in pts.items():
        th = T / T_lat
        out[lab] = {"T_K": T, "theta": th,
                    "du_over_u": C_U_EXACT * th ** 2,
                    "third_minus_w": C_W_EXACT * th ** 2,
                    "frac_softening_of_w": 3.0 * C_W_EXACT * th ** 2}
    # inversion: where does the EoS soften by 1 % ?
    th_1pc = math.sqrt(0.01 / (3.0 * C_W_EXACT))
    out["_T_at_1pc_softening_K"] = th_1pc * T_lat
    out["_T_lattice_K"] = T_lat
    return out


# ==========================================================================
#  B / C.  ENTROPY UNDER THE MODEL'S OWN WALK
# ==========================================================================
#
#  Free (quadratic) dynamics, so the many-body state is Gaussian and is carried
#  exactly by the one-particle correlation matrix C_{ij} = <c_i^dag c_j>.  No
#  truncation, no Trotter error: this is exact many-body evolution of a
#  2 L^3-mode Fock space, done in O(M^2) per step.

def _walk_setup(L):
    N = L ** 3
    M = 2 * N
    kk = np.fft.fftfreq(L) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing="ij")
    Uff, Ufg, Ugf, Ugg = bcc_unitary(KX, KY, KZ, sign="+")
    U = np.zeros((N, 2, 2), complex)
    U[:, 0, 0] = Uff.ravel(); U[:, 0, 1] = Ufg.ravel()
    U[:, 1, 0] = Ugf.ravel(); U[:, 1, 1] = Ugg.ravel()
    ev = np.zeros((N, 2), complex)
    V = np.zeros((N, 2, 2), complex)
    Vi = np.zeros((N, 2, 2), complex)
    for i in range(N):
        w, v = np.linalg.eig(U[i])
        ev[i] = w; V[i] = v; Vi[i] = np.linalg.inv(v)
    idx = np.arange(L)
    F1 = np.exp(-1j * 2.0 * np.pi * np.outer(idx, idx) / L) / math.sqrt(L)
    Fm = np.kron(np.kron(np.kron(F1, F1), F1), np.eye(2))
    return N, M, ev, V, Vi, Fm


def _prop(N, M, ev, V, Vi, t):
    lam = ev ** t
    D = np.zeros((M, M), complex)
    for i in range(N):
        D[2 * i:2 * i + 2, 2 * i:2 * i + 2] = V[i] @ np.diag(lam[i]) @ Vi[i]
    return D


def _vn(Cm):
    e = np.linalg.eigvalsh((Cm + Cm.conj().T) / 2.0).clip(1e-14, 1 - 1e-14)
    return float(-np.sum(e * np.log(e) + (1 - e) * np.log1p(-e)))


def entropy_ledger(L=8, seed=1, times=(1, 17, 101),
                   plateau_times=(5, 8, 13, 21, 34, 55, 89),
                   nonunitary_control=False):
    """B and C in one pass on one lattice.

    B1  fine-grained entropy of a MIXED state, conserved to machine precision
    B2  branch occupations n_pm(k) conserved  -> 2N conserved charges
    B3  coarse-grained entropy: 0 -> plateau, and plateau/GGE vs subsystem size
    B4  time reversal: S_A(-t) rises exactly as S_A(+t) does

    `nonunitary_control=True` inserts a mode-decimation (a non-invertible
    coarse-graining) into the propagator.  B1 MUST then fail: fine-grained
    entropy is conserved by unitarity and by nothing else.
    """
    N, M, ev, V, Vi, Fm = _walk_setup(L)
    rng = np.random.default_rng(seed)

    def prop(t):
        D = _prop(N, M, ev, V, Vi, t)
        if nonunitary_control:
            keep = np.ones(M)
            keep[::4] = 0.5                     # damp every 4th mode
            D = D * keep[:, None]
        return D

    # --- B1: mixed initial state -----------------------------------------
    occ_mixed = rng.uniform(0.1, 0.9, M)
    G_mixed = (Fm * occ_mixed) @ Fm.conj().T
    S0 = _vn(Fm.conj().T @ G_mixed @ Fm)
    b1 = []
    for t in times:
        B = Fm.conj().T @ prop(t)
        b1.append(abs(_vn(B @ G_mixed @ B.conj().T) - S0))
    # --- B2 / B3 / B4: pure product initial state -------------------------
    occ = (rng.random(M) < 0.5).astype(float)
    G0 = (Fm * occ) @ Fm.conj().T

    def branch_occ(t):
        G = prop(t) @ G0 @ prop(t).conj().T
        out = np.zeros((N, 2))
        for i in range(N):
            d2 = Vi[i] @ G[2 * i:2 * i + 2, 2 * i:2 * i + 2] @ V[i]
            out[i] = np.real(np.diag(d2))
        return out

    n0 = branch_occ(0)
    b2 = [float(np.abs(branch_occ(t) - n0).max()) for t in times]

    GG = np.zeros_like(G0)                      # the GGE (dephased) state
    for i in range(N):
        d2 = Vi[i] @ G0[2 * i:2 * i + 2, 2 * i:2 * i + 2] @ V[i]
        GG[2 * i:2 * i + 2, 2 * i:2 * i + 2] = V[i] @ np.diag(np.diag(d2)) @ Vi[i]

    xs = np.arange(N)
    z = xs % L; y = (xs // L) % L; x = xs // (L * L)
    half = L // 2
    regions = [("1/2", x < half),
               ("1/8", (x < half) & (y < half) & (z < half)),
               ("1/64", (x < half // 2) & (y < half // 2) & (z < half // 2)),
               ("1/512", (x < 1) & (y < 1) & (z < 1))]
    b3 = []
    s_at_zero = None
    rev = None
    for lab, sel in regions:
        Am = np.zeros(M, bool)
        Am[2 * xs[sel]] = True
        Am[2 * xs[sel] + 1] = True
        PA = Fm.conj().T[Am, :]
        vals, vals_rev = [], []
        for t in plateau_times:
            B = PA @ prop(t)
            vals.append(_vn(B @ G0 @ B.conj().T))
            Br = PA @ prop(-t)
            vals_rev.append(_vn(Br @ G0 @ Br.conj().T))
        gge = _vn(PA @ GG @ PA.conj().T)
        b3.append({"fraction": lab, "n_modes": int(Am.sum()),
                   "plateau": float(np.mean(vals)),
                   "plateau_sd": float(np.std(vals)),
                   "GGE": gge, "S_max": float(Am.sum() * math.log(2.0)),
                   "plateau_over_GGE": float(np.mean(vals)) / gge})
        if lab == "1/8":
            B0 = PA @ prop(0)
            s_at_zero = _vn(B0 @ G0 @ B0.conj().T)
            rev = {"forward_mean": float(np.mean(vals)),
                   "reversed_mean": float(np.mean(vals_rev)),
                   "rel_gap": abs(np.mean(vals) - np.mean(vals_rev))
                              / np.mean(vals)}
    return {"B1_fine_grained_drift": b1, "B1_S0": S0,
            "B2_branch_occ_drift": b2,
            "B3_regions": b3, "B3_S_A_at_t0": s_at_zero,
            "B4_time_reversal": rev}


# ==========================================================================
#  D.  THE CELL CONSTANT — what counting can and cannot decide (E9 / F190)
# ==========================================================================

def cell_capacity():
    """F190 posits s_cell = 2 pi sqrt3 nats and names "count the microstates"
    as its open step.  Two things follow immediately and neither had been said.

    D1 (a NO-GO, exact).  `e^(2 pi sqrt3)` is not an integer, and
    `2 pi sqrt3 / ln 2` is not an integer either.  An entropy that is a
    *dimension count* of any finite Hilbert space is `ln W` with `W` a positive
    integer; a count of binary modes is `n ln 2` with `n` an integer.  The
    F190 constant is neither.  So the open step CANNOT be discharged as written,
    whatever the BCC/Weyl content turns out to be.  The nearest integer number
    of two-state modes, n = 16, overshoots by 1.9 %.

    D2 (a necessary condition, PASSED).  Counting can still say whether the
    lattice has ENOUGH room.  The model's fermionic content is 48 Weyl fields
    (3 generations x 16 including nu_R, F47/F279), each two-component, so 96
    fermionic modes per site: a capacity of 96 ln 2 = 66.54 nats.  The
    requirement is 10.88.  Capacity exceeds requirement by 6.11x, so F190 is not
    excluded by room — it is under-determined by it, which is a different and
    more useful statement than "open".

    Together: the object F190 needs is an ENTANGLEMENT entropy (continuous
    spectrum, no integrality constraint), not a state count — and section B of
    this module is exactly the machinery that computes one.
    """
    s_cell = 2.0 * math.pi * math.sqrt(3.0)
    W = math.exp(s_cell)
    n_qubits = s_cell / math.log(2.0)
    n_weyl = 48
    modes_per_site = 2 * n_weyl
    capacity = modes_per_site * math.log(2.0)
    return {
        "s_cell_nats": s_cell,
        "implied_W": W,
        "W_distance_to_integer": abs(W - round(W)),
        "n_binary_modes_required": n_qubits,
        "n_distance_to_integer": abs(n_qubits - round(n_qubits)),
        "nearest_integer_modes": int(round(n_qubits)),
        "nearest_integer_overshoot_rel":
            abs(round(n_qubits) * math.log(2.0) / s_cell - 1.0),
        "fermionic_modes_per_site": modes_per_site,
        "capacity_nats": capacity,
        "capacity_over_requirement": capacity / s_cell,
        "occupancy_fraction": s_cell / capacity,
    }


def reciprocal_cube_coincidence():
    """A flagged COINCIDENCE, not a claim (D7 vocabulary, kind=coincidence).

    In the same lattice units the BCC reciprocal (fcc) conventional cube side is
    `4 pi / (2/sqrt3) = 2 pi sqrt3` — numerically identical to F190's per-cell
    entropy in nats, which comes from an entirely different place
    (`a^2 = 8 pi sqrt3 ell_P^2`, F107).  Same number, two unrelated quantities.
    Recorded so that a later session finds it already noticed and NOT claimed.
    """
    return {"reciprocal_cube_side": 2.0 * math.pi * math.sqrt(3.0),
            "F190_s_cell_nats": 2.0 * math.pi * math.sqrt(3.0),
            "identical": True,
            "claimed": False,
            "reason": "different quantities (a reciprocal length and an "
                      "entropy); coincident because both trace to a^2/ell_P^2 "
                      "= 8 pi sqrt3, but no derivation connects them."}


def input_ledger():
    return {
        "model_native": [
            "Omega_pair(k) = omega+(k/2)+omega-(k/2)  (F67/F68/F69 on F26)",
            "c_lat = 1/sqrt3 (F26)",
            "a = 6.5978 ell_P (F107) -> the tick, hence the ONE temperature scale",
            "the unitary BCC walk (F26) -> sections B and C",
            "48 Weyl fields / 2 components (F47/F279) -> section D capacity",
        ],
        "external": [
            "k_B, hbar, c, ell_P: unit rulers (k_B exact by SI definition)",
            "T_CMB, BBN and crossover temperatures: comparison points only",
            "F190's s_cell = 2 pi sqrt3: the target section D grades, not an input",
        ],
        "free_parameters": 0,
    }


# ==========================================================================
#  The G10 battery
# ==========================================================================

def check_g10(linear_control=False, nonunitary_control=False, L=8):
    """Every G10 check, PASS/FAIL, with the two declared controls.

    `linear_control=True`  -> G10-3, G10-4, G10-5, G10-6 MUST fail (no lattice
        term).
    `nonunitary_control=True` -> G10-7, G10-9, G10-10 MUST fail (entropy is not
        conserved).

    Both control sets were re-measured on 2026-08-07 when the record was armed,
    and this docstring is the corrected version: it had listed G10-3/4/5 and
    G10-7, three checks short of what the controls actually redden. The finding
    (F300 section "15/15 PASS") had the sets right; only this docstring was
    behind, and nothing could catch that while the gate record did not exist.
    """
    checks = []

    def add(cid, desc, ok, got, want):
        checks.append({"id": cid, "desc": desc,
                       "pass": bool(ok), "got": got, "want": want})

    d = dispersion_expansion()
    add("G10-1", "closed-form A(nhat) reproduces pair_dispersion, residual O(k^4)",
        d["rel_residual_over_k4"] < 1.0e-3, d["rel_residual_over_k4"], "< 1e-3")
    add("G10-2", "pair dispersion is EXACTLY linear along <100> at all |k|",
        d["axis_100_max_rel"] < 1.0e-13, d["axis_100_max_rel"], "< 1e-13")

    m = mean_anisotropy()
    add("G10-3a", "<A> = 1/315 exactly",
        m["rel_err"] < 1.0e-12, m["rel_err"], "< 1e-12")

    e = eos_coefficients(linear_control=linear_control)
    add("G10-3", "u/u_SB - 1 = (40 pi^2/441) Theta^2 (closed form vs quadrature)",
        e["Cu_rel"] < 3.0e-3, e["Cu_rel"], "< 3e-3")
    add("G10-4", "1/3 - w = (16 pi^2/1323) Theta^2 (closed form vs quadrature)",
        e["Cw_rel"] < 5.0e-3, e["Cw_rel"], "< 5e-3")
    add("G10-5", "s/s_SB - 1 = (4 pi^2/49) Theta^2",
        e["Cs_rel"] < 5.0e-3, e["Cs_rel"], "< 5e-3")
    add("G10-6", "parameter-free ratio C_u/C_w = 15/2",
        e["ratio_rel"] < 5.0e-3, e["ratio_rel"], "< 5e-3")

    b = boundary_independence()
    add("G10-6b", "EoS independent of the radial cut (zone boundary decoupled)",
        b["rel_spread"] < 1.0e-6, b["rel_spread"], "< 1e-6")

    ent = entropy_ledger(L=L, nonunitary_control=nonunitary_control)
    add("G10-7", "fine-grained von Neumann entropy conserved (MIXED state)",
        max(ent["B1_fine_grained_drift"]) < 1.0e-9,
        max(ent["B1_fine_grained_drift"]), "< 1e-9")
    add("G10-8", "branch occupations n_pm(k) exactly conserved -> 2N charges",
        max(ent["B2_branch_occ_drift"]) < 1.0e-11,
        max(ent["B2_branch_occ_drift"]), "< 1e-11")
    add("G10-9", "coarse-grained entropy rises from 0 to a plateau",
        (ent["B3_S_A_at_t0"] < 1.0e-8
         and ent["B3_regions"][1]["plateau"] > 1.0),
        {"S_A(0)": ent["B3_S_A_at_t0"],
         "plateau_1/8": ent["B3_regions"][1]["plateau"]},
        "S_A(0) = 0, plateau > 0")
    add("G10-10", "plateau -> GGE as the subsystem fraction falls",
        ent["B3_regions"][-1]["plateau_over_GGE"] > 0.99,
        [r["plateau_over_GGE"] for r in ent["B3_regions"]], "-> 1")
    add("G10-11", "time reversal: S_A(-t) rises like S_A(+t) (arrow is the "
                  "initial condition, not the dynamics)",
        ent["B4_time_reversal"]["rel_gap"] < 0.05,
        ent["B4_time_reversal"]["rel_gap"], "< 0.05")

    cc = cell_capacity()
    add("G10-12", "F190 no-go: 2 pi sqrt3 nats is not ln(integer) nor n ln 2",
        (cc["W_distance_to_integer"] > 0.01
         and cc["n_distance_to_integer"] > 0.01),
        {"W_dist": cc["W_distance_to_integer"],
         "n_dist": cc["n_distance_to_integer"]}, "both > 0.01")
    add("G10-13", "necessary condition: per-site capacity exceeds 2 pi sqrt3",
        cc["capacity_over_requirement"] > 1.0,
        cc["capacity_over_requirement"], "> 1")

    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "all_pass": n_pass == len(checks),
            "eos": e, "entropy": ent, "cell": cc,
            "scales": lattice_scales(), "margins": cosmology_margins(),
            "coincidence": reciprocal_cube_coincidence(),
            "ledger": input_ledger(),
            "controls": {"linear_control": linear_control,
                         "nonunitary_control": nonunitary_control}}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    out = check_g10()
    for c in out["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:8s} {c['desc']}")
    print(f"  {out['n_pass']}/{out['n_total']}")
    path = results_path("F300_lattice_thermodynamics.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("wrote", path)
