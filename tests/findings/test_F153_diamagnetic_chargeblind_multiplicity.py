"""F153 — the diamagnetic Peierls contact is charge-blind (exact), the channel
splitting is therefore purely paramagnetic, the small-q̃ R(m) is not cleanly
extractable in the two-tick sea (cut/cone artifacts), and the vector stiffness
does not reduce to a clean 7- or 8-fold channel count.

Checks
  D1  analytic δ²D₂ operator (ca_induced_stiffness.dirac_d2_transfer0) matches
      the dense gauged D₂ transfer-0 block (vector)               [machine]
  D2  dense STAGGERED transfer-0 block == dense VECTOR block      [exact→1e-9]
      ⇒ diamagnetic contact charge-blind ⇒ splitting purely paramagnetic
  N1  two-tick small-q̃ stiffness artifact-dominated: y↔z asymmetry of the
      transverse response at L=6 is O(signal) though symmetry forces 0;
      sign of χ_stag−χ_vec flips with q̃ direction                [numeric, neg]
  M1  channel matrix χ_dd' (8×8): face-axis (|d−d'|²=4) couplings present at
      fixed ê but cancel under transverse ê-sum; m>0 splitting localizes in
      the antipodal (|d−d'|²=12) group; eigenvalues = 4 anisotropic pairs,
      not a flat 7/8-fold                                          [structural]
  P1  the physical condensate coupling is O(1) (F118 lepton point e≈0.73),
      outside the perturbative small-m R(m) regime; on-shell 2/9 (F141) is
      exact algebra independent of the dynamical route            [algebraic]
"""
import sys, os, json
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ca-simulation'))
import ca_induced_stiffness as cis  # noqa: E402

results = {"finding": "F153", "checks": {}}
def check(name, ok, msg):
    results["checks"][name] = {"pass": bool(ok), "detail": msg}
    print(("PASS" if ok else "FAIL"), name, "—", msg)

C = cis.hop_matrices('+')
DIAGS = cis.DIAGS
Q = cis.Q_STAG

# ---- dense gauged D₂ and plane-wave transfer-0 block -------------------
def dense_D2(L, m, eps, ehat, qt, channel):
    N = L**3; n = float(np.sqrt(max(0.0, 1-m*m)))
    coords = np.array([(x, y, z) for x in range(L) for y in range(L) for z in range(L)])
    idx = {tuple(c): i for i, c in enumerate(coords)}
    par = (-1.0)**coords.sum(1); eh = np.asarray(ehat, float)
    def build(tick, e):
        D = np.zeros((4*N, 4*N), complex)
        for i in range(N):
            D[4*i, 4*i+2] = 1j*m; D[4*i+1, 4*i+3] = 1j*m
            D[4*i+2, 4*i] = 1j*m; D[4*i+3, 4*i+1] = 1j*m
        for d, Cd in C.items():
            dv = np.array(d); Cmd = np.conj(C[(-d[0], -d[1], -d[2])].T)
            tgt = (coords+dv) % L
            amid = e*np.cos((coords+0.5*dv)@qt)*float(dv@eh)
            qchg = (par if tick == 1 else -par) if channel == 'staggered' else 1.0
            ph = np.exp(1j*qchg*amid); rows = np.array([idx[tuple(t)] for t in tgt])
            for i in range(N):
                r, c = 4*rows[i], 4*i
                D[r:r+2, c:c+2] += n*ph[i]*Cd
                D[r+2:r+4, c+2:c+4] += n*ph[i]*Cmd
        return D
    return build(2, eps) @ build(1, eps)

def pw_block(Dmat, L, q):
    N = L**3
    coords = np.array([(x, y, z) for x in range(L) for y in range(L) for z in range(L)])
    pw = np.exp(1j*(coords@np.asarray(q, float)))/np.sqrt(N)
    P4 = np.zeros((4, 4*N), complex); Pk = np.zeros((4*N, 4), complex)
    for b in range(4):
        P4[b, b::4] = np.conj(pw); Pk[b::4, b] = pw
    return P4 @ Dmat @ Pk

def dense_coeff(L, m, ehat, qt, q, channel, e=1e-3):
    bp = pw_block(dense_D2(L, m, e, ehat, qt, channel), L, q)
    bm = pw_block(dense_D2(L, m, -e, ehat, qt, channel), L, q)
    b0 = pw_block(dense_D2(L, m, 0.0, ehat, qt, channel), L, q)
    return (bp+bm-2*b0)/e**2/2

# ---- D1: analytic operator vs dense (note: pw_block uses e^{+iq.x} ⇒ the
#         module convention A(q)=Σ e^{+iq.d} maps to base −q here) ---------
L = 6; m = 0.2; ehat = [0., 1., 0.]
qt = (2*np.pi/L)*np.array([1., 0, 0]); q = (2*np.pi/L)*np.array([2., 1., 3.])
Gh = cis.dirac_d2_transfer0(-q, qt, ehat, C, m)
cd = dense_coeff(L, m, ehat, qt, q, 'vector')
d1 = float(np.max(np.abs(Gh - cd)))
check("D1_analytic_seagull_matches_dense", d1 < 1e-6,
      f"max|analytic(−q) − dense transfer-0 block| = {d1:.2e}")

# ---- D2: charge-blind — staggered transfer-0 block == vector -----------
cv = dense_coeff(L, m, ehat, qt, q, 'vector')
csg = dense_coeff(L, m, ehat, qt, q, 'staggered')
d2 = float(np.max(np.abs(cv - csg)))
check("D2_diamagnetic_charge_blind", d2 < 1e-9,
      f"max|stag transfer-0 block − vector block| = {d2:.2e} (P²=1) "
      f"⇒ channel splitting is purely paramagnetic")

# ---- N1: artifacts — y↔z asymmetry and direction-dependent sign ---------
# transverse ê=y vs ê=z, q̃∥x, must be equal by symmetry at convergence
by = cis.dirac_brute_force_chi(6, 1, [0, 1, 0], [1, 0, 0], 'vector', 0.2)
bz = cis.dirac_brute_force_chi(6, 1, [0, 0, 1], [1, 0, 0], 'vector', 0.2)
asym = abs(by - bz); sig = max(abs(by), abs(bz))
# channel difference sign across two q̃ directions (longitudinal ê=qdir)
diff_100 = (cis.dirac_brute_force_chi(6, 1, [1, 0, 0], [1, 0, 0], 'staggered', 0.2)
            - cis.dirac_brute_force_chi(6, 1, [1, 0, 0], [1, 0, 0], 'vector', 0.2))
diff_111 = (cis.dirac_brute_force_chi(6, 1, [1, 1, 1], [1, 1, 1], 'staggered', 0.2)
            - cis.dirac_brute_force_chi(6, 1, [1, 1, 1], [1, 1, 1], 'vector', 0.2))
results["checks"]["_N1_numbers"] = {
    "transverse_y": by, "transverse_z": bz, "yz_asym": asym, "yz_signal": sig,
    "chan_diff_qhat_100": diff_100, "chan_diff_qhat_111": diff_111}
check("N1_small_q_artifact_dominated",
      asym > 0.3*sig and (np.sign(diff_100) != np.sign(diff_111)),
      f"L=6 transverse y vs z differ by {asym:.3f} (signal {sig:.3f}; symmetry⇒0); "
      f"χ_stag−χ_vec sign flips: q̂=[100] {diff_100:+.4f}, q̂=[111] {diff_111:+.4f} "
      f"⇒ clean isotropic small-q̃ R(m) not extractable at reachable L")

# ---- M1: channel matrix χ_dd' (paramagnetic vertex bilinear) -----------
def hop_vertex4(q_mid, eh, d, m):
    n = float(np.sqrt(max(0.0, 1-m*m))); dv = np.array(d, float)
    ph = 1j*float(dv@np.asarray(eh, float))*np.exp(1j*(np.asarray(q_mid)@dv))
    sh = np.shape(q_mid)[:-1]; V = np.zeros(sh+(4, 4), complex)
    V[..., :2, :2] = n*ph[..., None, None]*C[d]
    V[..., 2:, 2:] = n*ph[..., None, None]*np.conj(np.swapaxes(C[(-d[0], -d[1], -d[2])], -1, -2))
    return V

def chi_matrix(L, eh, m, channel):
    qt = (2*np.pi/L)*np.array([1., 0, 0])
    g = (np.arange(L)+0.3819660112501051)*(2*np.pi/L)-np.pi
    qx, qy, qz = np.meshgrid(g, g, g, indexing='ij')
    q = np.stack([qx, qy, qz], -1).reshape(-1, 3)
    qp = q+qt+(Q if channel == 'staggered' else 0.0)
    Po, _, Oo, _, _ = cis.dirac_bands(q, m); _, Pe, _, Oe, _ = cis.dirac_bands(qp, m)
    Dq = cis.dirac_matrix_q(q, m); Dp = cis.dirac_matrix_q(qp, m)
    dOm = cis._wrap(Oe-Oo); ok = np.abs(dOm) > 1e-12
    kern = np.zeros_like(dOm); kern[ok] = 1.0/np.tan(dOm[ok]/2)
    Mops = {}
    for d in DIAGS:
        Vd = hop_vertex4(q+qt/2.0, eh, d, m)
        Bd = Dp@Vd+Vd@Dq if channel == 'vector' else Dp@Vd-Vd@Dq
        Mops[d] = Pe@Bd@Po
    M = np.zeros((8, 8), complex)
    for i, d in enumerate(DIAGS):
        for j, dp in enumerate(DIAGS):
            t = np.einsum('...ij,...ij->...', Mops[d], np.conj(Mops[dp]))
            M[i, j] = np.sum(t*kern)/q.shape[0]
    return M

def grouped(M):
    from collections import defaultdict
    cls = defaultdict(float)
    for i, d in enumerate(DIAGS):
        for j, dp in enumerate(DIAGS):
            if i == j:
                continue
            dd = tuple(np.array(d)-np.array(dp)); cls[int(np.dot(dd, dd))] += M[i, j].real
    return {k: round(cls[k], 4) for k in sorted(cls)}

LM = 16
# transverse-summed (O_h-restricted to ⊥q̃) vector
Mv = chi_matrix(LM, [0., 1., 0.], 0.0, 'vector') + chi_matrix(LM, [0., 0., 1.], 0.0, 'vector')
gv0 = grouped(Mv)
# m>0 antipodal localisation of the splitting
Mv2 = chi_matrix(LM, [0., 1., 0.], 0.2, 'vector') + chi_matrix(LM, [0., 0., 1.], 0.2, 'vector')
Ms2 = chi_matrix(LM, [0., 1., 0.], 0.2, 'staggered') + chi_matrix(LM, [0., 0., 1.], 0.2, 'staggered')
gv2, gs2 = grouped(Mv2), grouped(Ms2)
evals = np.sort(np.linalg.eigvalsh(0.5*(Mv+Mv.conj().T)))
# 4 distinct pairs ⇒ pair-gaps large, within-pair gaps small
pairs = evals.reshape(4, 2)
within = float(np.max(np.abs(pairs[:, 0]-pairs[:, 1])))
between = float(np.min(np.abs(np.diff(pairs.mean(1)))))
results["checks"]["_M1_numbers"] = {
    "faceaxis_dd2_4_transverse_summed": gv0.get(4),
    "facediag_dd2_8": gv0.get(8), "antipodal_dd2_12": gv0.get(12),
    "antipodal_vec_m02": gv2.get(12), "antipodal_stag_m02": gs2.get(12),
    "eigs_transverse": [round(x, 4) for x in evals.tolist()],
    "within_pair_max": within, "between_pair_min": between}
check("M1_no_clean_channel_count",
      abs(gv0.get(4)) < 1e-3 and within < 0.3*between
      and (gs2.get(12) > gv2.get(12)),
      f"transverse-summed face-axis(|Δd|²=4)→{gv0.get(4)} (cancels); "
      f"face-diag→{gv0.get(8)}, antipodal→{gv0.get(12)}; eigs=4 pairs "
      f"(within {within:.3f} ≪ between {between:.3f}); m=0.2 antipodal "
      f"splitting vec {gv2.get(12)} vs stag {gs2.get(12)} (the −1 tick sign)")

# ---- P1: physical condensate coupling is O(1) --------------------------
y = np.array([1.0, 0.2439, 0.0170])         # F118 lepton ground state (τ,μ,e)
ybar = y.mean(); p = y - ybar; e_Eg = float(np.sqrt(np.sum(p**2)))
s2_os = Fraction(2, 9); mZmW = (3.0)/np.sqrt(7.0)
pdg_mZmW = 91.1880/80.3692
results["checks"]["_P1_numbers"] = {
    "Eg_amplitude_e_at_lepton_point": e_Eg, "y_tau_wallpinned": 1.0,
    "sin2_os_2_9": float(s2_os), "mZ_over_mW_3_sqrt7": mZmW,
    "pdg_mZ_over_mW": pdg_mZmW, "resid_mZmW_pct": 100*(mZmW/pdg_mZmW-1),
    "resid_s2_pct": 100*(float(s2_os)/0.22305-1)}
check("P1_physical_coupling_is_O1",
      e_Eg > 0.5 and abs(100*(mZmW/pdg_mZmW-1)) < 0.1,
      f"E_g amplitude at lepton point e={e_Eg:.3f} (O(1), y_τ=1) ⇒ outside the "
      f"perturbative small-m R(m) regime; on-shell 2/9 ⇒ m_Z/m_W=3/√7={mZmW:.6f} "
      f"vs PDG {pdg_mZmW:.6f} ({100*(mZmW/pdg_mZmW-1):+.3f}%) stands as exact algebra")

n_pass = sum(c["pass"] for c in results["checks"].values() if isinstance(c, dict) and "pass" in c)
n_tot = sum(1 for c in results["checks"].values() if isinstance(c, dict) and "pass" in c)
results["summary"] = f"{n_pass}/{n_tot} PASS"
print("\n", results["summary"])
out = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results',
                   'F153_diamagnetic_chargeblind_multiplicity.json')
with open(out, 'w') as f:
    json.dump(results, f, indent=2)
print("wrote", out)
assert n_pass == n_tot
