# test_F102_coupled_rotors.py
# 2026-06-05
#
# F102 -- Coupling several rotors: does the F101 single-plaquette crossover
# survive when plaquettes are coupled through shared links?
#
# F101 solved ONE compact rotor (single plaquette) exactly and found the
# Gaussian (weak) <-> log-confinement (strong) crossover.  The honest open
# question (F101 section 7): in 2+1D the plaquettes are NOT independent -- they
# share links -- so does the crossover survive the coupling?
#
# This builds the genuinely-coupled theory: Z_3 (the physical centre) lattice
# gauge theory in 2+1D, Hamiltonian form, on open strips of P = 1, 2, 3
# plaquettes, solved by EXACT diagonalisation (matvec Lanczos, no truncation --
# Z_N operators are exact finite unitaries).
#
#   H = -Gamma sum_links (X_l + X_l^dag) - lambda sum_plaq (B_p + B_p^dag)
#   B_p = prod_{l in p} Z_l^{+-1}   (oriented plaquette),  X clock-shift, Z clock.
#   strong coupling = small lambda (electric dominates -> confined),
#   weak coupling   = large lambda (magnetic dominates -> deconfined).
#   confinement order parameter: <B_p>  (= F101's s_1, now in the COUPLED theory).
#
#   M1  Lanczos validated vs dense ED; ground state in the trivial Gauss sector
#       (<A_s> = 1) -- correctness.
#   M2  the crossover SURVIVES: <B_p>(lambda) runs 0 -> 1 for P = 1, 2, 3, and is
#       IDENTICAL across P at strong coupling (plaquettes decouple); strong-
#       coupling <B_p> ~ lambda (the -ln(lambda) log law of F101/F70).
#   M3  area-law factorisation: <W_P> = <prod_p B_p> ~ C_P <B_p>^P at strong
#       coupling (F70's independent-plaquette product recovered, C_P -> O(1));
#       the shared-link correction -> 1 only deep in the deconfined phase.
#   M4  sigma = -ln<B_p> stays positive with the strong-coupling log slope ~ -1
#       for every P -- confinement survives coupling.
#   M5  weak-coupling order INCREASES with P (more rotors = more ordered) --
#       the finite-size precursor of the deconfinement transition: coupling not
#       only preserves the crossover, it organises it into a transition.
#
# Pure numpy.  Ground state by matvec Lanczos with full reorthogonalisation;
# H applied on the reshaped (3,)*L state via np.roll (electric) and a diagonal
# phase (magnetic) -- no dense H stored.

import json
import time
import pathlib

import numpy as np

t0 = time.time()
results = {"finding": "F102", "date": "2026-06-05",
           "title": "coupling several rotors -- does the crossover survive?",
           "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement, "residual": str(residual),
        "status": "PASS" if status else "FAIL"}
    print(f"{name}: {statement}\n      -> residual {residual} "
          f"[{'PASS' if status else 'FAIL'}]")


W3 = np.exp(2j * np.pi / 3)
phZ = np.array([1.0, W3, W3 ** 2], complex)        # Z clock phases


# ---- geometry: open strip of P plaquettes ----------------------------
def make_strip(P):
    links = {}
    idx = 0
    for y in (0, 1):
        for x in range(P):
            links[("h", x, y)] = idx; idx += 1
    for x in range(P + 1):
        links[("v", x)] = idx; idx += 1
    L = idx
    plaqs = []
    for x in range(P):                              # corners (x,0)(x+1,0)(x+1,1)(x,1)
        plaqs.append([(links[("h", x, 0)], +1), (links[("v", x + 1)], +1),
                      (links[("h", x, 1)], -1), (links[("v", x)], -1)])
    # site -> incident links with orientation, for the Gauss operator
    sites = {}
    for (kind, *coord), li in links.items():
        if kind == "h":
            x, y = coord
            sites.setdefault((x, y), []).append((li, +1))      # out of (x,y)
            sites.setdefault((x + 1, y), []).append((li, -1))  # into (x+1,y)
        else:
            x, = coord
            sites.setdefault((x, 0), []).append((li, +1))
            sites.setdefault((x, 1), []).append((li, -1))
    return L, plaqs, sites


def plaq_phase(L, plaq):
    arr = np.ones([3] * L, complex)
    for lk, s in plaq:
        ph = phZ if s > 0 else phZ.conj()
        shape = [1] * L; shape[lk] = 3
        arr = arr * ph.reshape(shape)
    return arr


def Hmatvec(psi, L, Gamma, lam, mdiag):
    out = np.zeros_like(psi)
    for l in range(L):
        out += -Gamma * (np.roll(psi, +1, axis=l) + np.roll(psi, -1, axis=l))
    out += -lam * mdiag * psi
    return out


def ground(L, plaqs, Gamma, lam, iters=220, seed=0):
    Bdiag = [plaq_phase(L, p) for p in plaqs]
    mdiag = np.zeros([3] * L)
    for Bp in Bdiag:
        mdiag += 2.0 * Bp.real
    rng = np.random.default_rng(seed)
    v = rng.standard_normal([3] * L) + 1j * rng.standard_normal([3] * L)
    v /= np.linalg.norm(v)
    Vs = [v]; al = []; be = []
    wv = Hmatvec(v, L, Gamma, lam, mdiag); a = np.vdot(v, wv).real
    wv = wv - a * v; al.append(a)
    for k in range(1, iters):
        b = np.linalg.norm(wv)
        if b < 1e-11:
            break
        be.append(b); vk = wv / b; Vs.append(vk)
        wv = Hmatvec(vk, L, Gamma, lam, mdiag); a = np.vdot(vk, wv).real
        wv = wv - a * vk - b * Vs[-2]
        for u in Vs[:-1]:
            wv = wv - np.vdot(u, wv) * u            # full reorthogonalisation
        al.append(a)
    m = len(al)
    T = np.diag(al) + np.diag(be[:m - 1], 1) + np.diag(be[:m - 1], -1)
    ev, evec = np.linalg.eigh(T)
    gs = np.zeros([3] * L, complex)
    for i in range(m):
        gs += evec[i, 0] * Vs[i]
    gs /= np.linalg.norm(gs)
    prob = np.abs(gs) ** 2
    Bexp = [float((prob * Bp).sum().real) for Bp in Bdiag]
    Wall = np.ones([3] * L, complex)
    for Bp in Bdiag:
        Wall = Wall * Bp
    Wexp = float((prob * Wall).sum().real)
    return ev[0], Bexp, Wexp, gs


def dense_ground(L, plaqs, Gamma, lam):
    I3 = np.eye(3, dtype=complex)
    X = np.zeros((3, 3), complex)
    for j in range(3):
        X[(j + 1) % 3, j] = 1.0
    Z = np.diag(phZ)

    def emb(mats):
        out = mats[0]
        for mm in mats[1:]:
            out = np.kron(out, mm)
        return out
    dim = 3 ** L
    H = np.zeros((dim, dim), complex)
    for l in range(L):
        mats = [I3] * L; mats[l] = X
        Xl = emb(mats); H += -Gamma * (Xl + Xl.conj().T)
    for p in plaqs:
        mats = [I3] * L
        for lk, s in p:
            mats[lk] = mats[lk] @ (Z if s > 0 else Z.conj().T)
        Bp = emb(mats); H += -lam * (Bp + Bp.conj().T)
    ev, evec = np.linalg.eigh(H)
    return ev[0]


def gauss_expectation(gs, L, sites, site):
    """<A_s> for the interior site: A_s = prod X_l^{+-1} (roll along incident links)."""
    out = gs.copy()
    for li, orient in sites[site]:
        out = np.roll(out, +1 if orient > 0 else -1, axis=li)
    return complex(np.vdot(gs, out))


# ============================================================ M1
# Lanczos vs dense + Gauss-law (trivial sector) sanity.
e_L, B_L, W_L, gs2 = ground(*make_strip(2)[:2], 1.0, 1.0)
L2, plaqs2, sites2 = make_strip(2)
e_d = dense_ground(L2, plaqs2, 1.0, 1.0)
lanc_err = abs(e_L - e_d)
# interior site (1,0) is shared by both plaquettes
gauss = gauss_expectation(gs2, L2, sites2, (1, 0))
gauss_ok = abs(gauss - 1.0) < 1e-6
m1 = lanc_err < 1e-8 and gauss_ok
record("M1", "matvec Lanczos ground-state energy matches dense ED; ground state "
       "in the trivial Gauss sector (<A_s> = 1) -- coupled Z_3 gauge ED correct",
       f"|E_L - E_dense| {lanc_err:.1e}, <A_s> {gauss.real:.6f}", m1)

# ============================================================ M2
# The crossover SURVIVES coupling, for P = 1, 2, 3.
lams = [0.1, 0.3, 1.0, 3.0, 10.0]
Bp_by_P = {}
for P in (1, 2, 3):
    Lp, pl, _ = make_strip(P)
    row = []
    for lam in lams:
        _, B, _, _ = ground(Lp, pl, 1.0, lam)
        row.append(B[len(B) // 2])              # central (most bulk) plaquette
    Bp_by_P[P] = row
# (a) each P shows the full crossover 0 -> 1
crossover = all(Bp_by_P[P][0] < 0.05 and Bp_by_P[P][-1] > 0.9 for P in (1, 2, 3))
# (b) identical across P at strong coupling (plaquettes decouple)
strong_spread = max(abs(Bp_by_P[P][0] - Bp_by_P[1][0]) for P in (2, 3))
decouple = strong_spread < 1e-4
# (c) strong-coupling log law: <B_p> ~ lambda  =>  <B_p>(0.3)/<B_p>(0.1) ~ 3
loglaw = abs(Bp_by_P[2][1] / Bp_by_P[2][0] - 3.0) < 0.2
m2 = bool(crossover and decouple and loglaw)
record("M2", "crossover SURVIVES coupling: <B_p>(lambda) runs 0->1 for P=1,2,3; "
       "identical across P at strong coupling (plaquettes decouple); strong "
       "<B_p> ~ lambda (log law)",
       f"strong-coupling spread {strong_spread:.1e}, "
       f"<B_p>(.3)/<B_p>(.1)={Bp_by_P[2][1]/Bp_by_P[2][0]:.3f}", m2)

# ============================================================ M3
# Area-law factorisation: <W_P> ~ C_P <B_p>^P at strong coupling (F70 recovered).
ratios_strong = {}
ratios_weak = {}
for P in (2, 3):
    Lp, pl, _ = make_strip(P)
    _, Bs, Ws, _ = ground(Lp, pl, 1.0, 0.1)        # strong
    _, Bw, Ww, _ = ground(Lp, pl, 1.0, 10.0)       # weak
    bp_s = np.mean(Bs); bp_w = np.mean(Bw)
    ratios_strong[P] = Ws / bp_s ** P
    ratios_weak[P] = Ww / bp_w ** P
# at strong coupling the ratio is a finite O(1) constant (factorisation up to a
# shared-link prefactor); near deconfinement it tends to 1.
fact_strong = all(0.8 < ratios_strong[P] < 2.0 for P in (2, 3))
toward_one = all(abs(ratios_weak[P] - 1.0) < abs(ratios_strong[P] - 1.0)
                 for P in (2, 3))
m3 = bool(fact_strong and toward_one)
record("M3", "area-law factorisation: <W_P> = C_P <B_p>^P at strong coupling "
       "(F70 independent-plaquette product, C_P = O(1)); ratio -> 1 toward "
       "deconfinement",
       f"strong C_P {{2:{ratios_strong[2]:.3f}, 3:{ratios_strong[3]:.3f}}}, "
       f"weak {{2:{ratios_weak[2]:.3f}, 3:{ratios_weak[3]:.3f}}}", m3)

# ============================================================ M4
# sigma = -ln<B_p> stays positive with strong-coupling log slope ~ -1, all P.
slopes = {}
for P in (1, 2, 3):
    Lp, pl, _ = make_strip(P)
    _, B1, _, _ = ground(Lp, pl, 1.0, 0.1)
    _, B2, _, _ = ground(Lp, pl, 1.0, 0.4)
    s1 = -np.log(B1[len(B1) // 2]); s2 = -np.log(B2[len(B2) // 2])
    slopes[P] = (s2 - s1) / (np.log(0.4) - np.log(0.1))
m4 = all(abs(slopes[P] + 1.0) < 0.1 for P in (1, 2, 3))
record("M4", "sigma = -ln<B_p> positive with strong-coupling log slope "
       "d sigma/d ln(lambda) ~ -1 for every P -- confinement survives coupling",
       f"slopes P=1,2,3: {slopes[1]:.3f}, {slopes[2]:.3f}, {slopes[3]:.3f}", m4)

# ============================================================ M5
# Weak-coupling order increases with P (deconfinement-transition precursor).
weak_order = [Bp_by_P[P][-1] for P in (1, 2, 3)]
increasing = weak_order[0] < weak_order[1] < weak_order[2]
m5 = bool(increasing)
record("M5", "weak-coupling order increases with P (more coupled rotors = more "
       "ordered) -- the finite-size precursor of the deconfinement transition; "
       "coupling organises the crossover into a transition",
       f"<B_p>(lambda=10) for P=1,2,3 = {[round(x,5) for x in weak_order]}", m5)

# ============================================================
results["Bp_by_P"] = {str(P): [round(x, 5) for x in Bp_by_P[P]] for P in (1, 2, 3)}
results["lambdas"] = lams
results["runtime_s"] = round(time.time() - t0, 3)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{n_pass}/{len(results['checks'])} PASS"
print(f"\nOverall: {results['summary']} ({results['runtime_s']} s)")

out = pathlib.Path(__file__).resolve().parent.parent / "test-results" / "F102_coupled_rotors.json"
out.write_text(json.dumps(results, indent=2))
print(f"Results written to {out}")
