"""
ca_nuclear_core.py — the NN short-range repulsive core, derived from the model
==============================================================================

Created: 2026-06-08

Phase P4 of `roadmap-matter-binding.md` named the **short-range repulsive core**
of the nucleon-nucleon force as the one ingredient the model did not yet have
(the OPEP attractive tail is the F103 pion).  This module derives that core
from the model's own first principles — no new free physics, no phenomenology.

THE MECHANISM (entirely model-native)
-------------------------------------
A nucleon is a colour-singlet of THREE genuine CA fermions: colour-antisymmetric
ε_{abc} (F71) × SU(6) spin-flavour-symmetric.  Two nucleons pushed on top of one
another are SIX identical fermions, so the **total six-quark wavefunction must be
antisymmetric** (the F71 Pauli antisymmetriser, extended 3q→6q).  Pauli therefore
forbids the two clusters from both sitting in the lowest spatial orbital unless
the colour-spin (chromomagnetic) state rearranges into the spatially-symmetric
[6] configuration.  That [6] state is chromomagnetically *unfavourable*: its
colour-spin energy is far above two free nucleons, so the overlap costs energy —
a repulsion.  This is the quark-Pauli / colour-magnetic origin of the hard core
(Oka–Yazaki, Faessler et al.), here computed directly in the model's algebra.

EXACT ALGEBRA (no numpy on chiral objects; pure rationals — CLAUDE.md compliant)
--------------------------------------------------------------------------------
The chromomagnetic operator is built from the model's own colour/spin generators
(T^a = λ^a/2 as in ca_strong) via the SU(N) Fierz swap identities, exact:

    λ_i·λ_j = 2 P^c_ij − 2/3        (SU(3) fundamental)
    σ_i·σ_j = 2 P^s_ij − 1          (SU(2) fundamental)
    H_CM     = − Σ_{i<j} (λ_i·λ_j)(σ_i·σ_j)             [units of g_cm]

with P^c, P^s the colour / spin transposition operators (label swaps).  Every
expectation value below is a rational number.

RESULTS (see test_F113_repulsive_core.py)
-----------------------------------------
    single nucleon      ⟨H_CM⟩ = −8 g_cm        (binding; the usual N value)
    Δ(1232)             ⟨H_CM⟩ = +8 g_cm        ⇒ M_Δ−M_N = 16 g_cm
    g_cm calibrated by  M_Δ−M_N = 293 MeV       ⇒ g_cm = 18.31 MeV
    [6] 6q at R=0       ⟨H_CM⟩ = +8/3 g_cm
    two free nucleons               = −16 g_cm
    core height  ΔE_CM  = +56/3 g_cm = +341.8 MeV   (> 0  ⇒  REPULSIVE)

The repulsion turns on over the quark overlap range (Gaussian s = e^{−R²/8b²}):
~342 MeV at R=0, falling monotonically to 0 by R ≈ 4b — the empirical NN hard
core (several hundred MeV, radius ~0.5 fm).  Combined with the F103 one-pion-
exchange tail this gives the full short-repulsive / long-attractive NN potential
that P4 (the deuteron) consumes.

Conventions match ca_baryon.py / ca_strong.py: colour (r,g,b)=(0,1,2); the SU(6)
proton spin-flavour wavefunction is the F71 symmetric 56-plet.
"""

from fractions import Fraction as Fr
from itertools import permutations
import math

# ──────────────────────────────────────────────────────────────────
#  single-quark label encoding:  q = 4*colour + 2*spin + flavour
#    colour ∈ {0,1,2}=(r,g,b),  spin ∈ {0=↑,1=↓},  flavour ∈ {0=u,1=d}
# ──────────────────────────────────────────────────────────────────
def enc(c, s, f): return c * 4 + s * 2 + f
def dec(q):       return (q // 4, (q // 2) % 2, q % 2)

# ε_{abc} on colour
_EPS = {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1,
        (2, 1, 0): -1, (0, 2, 1): -1, (1, 0, 2): -1}

_PERMS6 = list(permutations(range(6)))


# ──────────────────────────────────────────────────────────────────
#  nucleon wavefunctions (F71 SU(6) symmetric × colour ε)
# ──────────────────────────────────────────────────────────────────
def _proton_spin_flavour(up=True):
    """SU(6)-symmetric proton spin-flavour wf, dict{(s,f)×3 : Fraction}."""
    U, D = (0, 1) if up else (1, 0)        # spin code for chosen S_z / opposite
    psi = {}
    def add(st, a): psi[st] = psi.get(st, Fr(0)) + a
    def symm(seed, co):
        seen = set()
        for pr in set(permutations(range(3))):
            st = tuple(seed[pr[i]] for i in range(3))
            if st in seen:
                continue
            seen.add(st); add(st, co)
    symm([(U, 'u'), (U, 'u'), (D, 'd')], Fr(2))    # +2 terms
    symm([(U, 'u'), (D, 'u'), (U, 'd')], Fr(-1))   # −1 terms
    return psi

def _neutron_spin_flavour(up=True):
    sw = {'u': 'd', 'd': 'u'}
    return {tuple((s, sw[f]) for (s, f) in k): v
            for k, v in _proton_spin_flavour(up).items()}

def nucleon(which='p', up=True):
    """Totally-antisymmetric 3-quark nucleon, dict{(q1,q2,q3): Fraction}.
       colour-antisymmetric ε × spin-flavour-symmetric SU(6)."""
    sf = _proton_spin_flavour(up) if which == 'p' else _neutron_spin_flavour(up)
    fc = {'u': 0, 'd': 1}
    psi = {}
    for (c1, c2, c3), e in _EPS.items():
        for k, a in sf.items():
            (s1, f1), (s2, f2), (s3, f3) = k
            key = (enc(c1, s1, fc[f1]), enc(c2, s2, fc[f2]), enc(c3, s3, fc[f3]))
            psi[key] = psi.get(key, Fr(0)) + Fr(e) * a
    return psi

def delta_pp():
    """Δ⁺⁺ (uuu, S_z=3/2), colour-singlet — for the N–Δ calibration."""
    psi = {}
    for (c1, c2, c3), e in _EPS.items():
        key = (enc(c1, 0, 0), enc(c2, 0, 0), enc(c3, 0, 0))
        psi[key] = psi.get(key, Fr(0)) + Fr(e)
    return psi

def two_cluster(SA=True, SB=True, isospin='singlet'):
    """Two-nucleon state on 6 slots (1-3 = cluster A, 4-6 = B).
       Deuteron channel = (SA=SB=True ⇒ S=1,S_z=1) × (isospin='singlet' ⇒ T=0)."""
    pA, nA = nucleon('p', SA), nucleon('n', SA)
    pB, nB = nucleon('p', SB), nucleon('n', SB)
    Phi = {}
    def comb(X, Y, co):
        for ka, va in X.items():
            for kb, vb in Y.items():
                key = ka + kb
                Phi[key] = Phi.get(key, Fr(0)) + co * va * vb
    if isospin == 'singlet':                      # T=0  (pn − np)
        comb(pA, nB, Fr(1)); comb(nA, pB, Fr(-1))
    else:                                          # T=1, T3=0  (pn + np)
        comb(pA, nB, Fr(1)); comb(nA, pB, Fr(1))
    return Phi


# ──────────────────────────────────────────────────────────────────
#  permutation / overlap primitives
# ──────────────────────────────────────────────────────────────────
def perm_sign(p):
    p = list(p); seen = [False] * len(p); sg = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i; L = 0
        while not seen[j]:
            seen[j] = True; j = p[j]; L += 1
        if L % 2 == 0:
            sg = -sg
    return sg

def apply_perm(Phi, p):
    out = {}
    for k, a in Phi.items():
        nk = tuple(k[p[i]] for i in range(len(p)))
        out[nk] = out.get(nk, Fr(0)) + a
    return out

def overlap(A, B):
    if len(A) > len(B):
        A, B = B, A
    s = Fr(0)
    for k, v in A.items():
        w = B.get(k)
        if w is not None:
            s += v * w
    return s

def _cross(p):
    """number of cluster-A slots {0,1,2} sent into cluster B by p (the k in s^{2k})."""
    return sum(1 for i in (0, 1, 2) if p[i] in (3, 4, 5))


# ──────────────────────────────────────────────────────────────────
#  chromomagnetic operator  H_CM = −Σ_{i<j}(λ_i·λ_j)(σ_i·σ_j)
#    = −Σ_{i<j} (2P^c−2/3)(2P^s−1)
#    = −Σ_{i<j} [ 4 P^cP^s − 2 P^c − 4/3 P^s + 2/3 ]
# ──────────────────────────────────────────────────────────────────
def _swap_colour(k, i, j):
    a = list(k); (ci, si, fi) = dec(a[i]); (cj, sj, fj) = dec(a[j])
    a[i] = enc(cj, si, fi); a[j] = enc(ci, sj, fj); return tuple(a)
def _swap_spin(k, i, j):
    a = list(k); (ci, si, fi) = dec(a[i]); (cj, sj, fj) = dec(a[j])
    a[i] = enc(ci, sj, fi); a[j] = enc(cj, si, fj); return tuple(a)

def H_CM(Phi, n):
    out = {}
    def add(k, v): out[k] = out.get(k, Fr(0)) + v
    for i in range(n):
        for j in range(i + 1, n):
            for k, a in Phi.items():
                add(_swap_spin(_swap_colour(k, i, j), i, j), Fr(-4) * a)
                add(_swap_colour(k, i, j),                   Fr(2) * a)
                add(_swap_spin(k, i, j),                     Fr(4, 3) * a)
                add(k,                                       Fr(-2, 3) * a)
    return out

def chromomagnetic_energy(Phi, n):
    """⟨H_CM⟩ in units of g_cm (exact Fraction)."""
    return overlap(Phi, H_CM(Phi, n)) / overlap(Phi, Phi)


# ──────────────────────────────────────────────────────────────────
#  RGM norm kernel  n(R)  and the chromomagnetic core profile V_core(R)
# ──────────────────────────────────────────────────────────────────
def norm_kernel_coeffs(Phi):
    """Exact K_m = Σ_{P:cross=m} sgn(P)⟨Φ|P|Φ⟩.
       n(R) = (Σ_m K_m s^{2m})/K_0 with s = exp(−R²/8b²); n(∞)=1."""
    K = {0: Fr(0), 1: Fr(0), 2: Fr(0), 3: Fr(0)}
    for p in _PERMS6:
        K[_cross(p)] += Fr(perm_sign(p)) * overlap(Phi, apply_perm(Phi, p))
    return K

def antisymmetrised_6q_energy(Phi):
    """⟨𝒜Φ|H_CM|𝒜Φ⟩/⟨𝒜Φ|𝒜Φ⟩ at full overlap R=0 (exact). H_CM commutes with 𝒜."""
    APhi = {}
    for p in _PERMS6:
        sg = Fr(perm_sign(p))
        for k, v in apply_perm(Phi, p).items():
            APhi[k] = APhi.get(k, Fr(0)) + sg * v
    return overlap(Phi, H_CM(APhi, 6)) / overlap(Phi, APhi)

def core_profile(Phi, xb_list):
    """Chromomagnetic ⟨H_CM⟩(R) of the antisymmetrised two-cluster state vs R/b.
       Returns list of (R/b, ⟨H_CM⟩(R)).  Float (speed); exact endpoints checked
       separately by chromomagnetic_energy / antisymmetrised_6q_energy."""
    Phif = {k: float(v) for k, v in Phi.items()}
    Hphif = {k: float(v) for k, v in H_CM(Phi, 6).items()}
    def ovf(A, B):
        if len(A) > len(B):
            A, B = B, A
        s = 0.0
        for k, v in A.items():
            w = B.get(k)
            if w is not None:
                s += v * w
        return s
    def applyf(P, p):
        out = {}
        for k, a in P.items():
            nk = tuple(k[p[i]] for i in range(6))
            out[nk] = out.get(nk, 0.0) + a
        return out
    pre = []
    for p in _PERMS6:
        sg = float(perm_sign(p)); k = _cross(p); Pp = applyf(Phif, p)
        pre.append((k, sg * ovf(Hphif, Pp), sg * ovf(Phif, Pp)))
    res = []
    for xb in xb_list:
        s = math.exp(-(xb ** 2) / 8.0); num = 0.0; den = 0.0
        for k, n_, d_ in pre:
            w = s ** (2 * k); num += n_ * w; den += d_ * w
        res.append((xb, num / den))
    return res


# ──────────────────────────────────────────────────────────────────
#  one-call summary
# ──────────────────────────────────────────────────────────────────
def derive_core(M_Delta_minus_N_MeV=293.0):
    """Full derivation summary.  g_cm calibrated by the N–Δ splitting."""
    eN = chromomagnetic_energy(nucleon('p', True), 3)
    eD = chromomagnetic_energy(delta_pp(), 3)
    g_cm = M_Delta_minus_N_MeV / float(eD - eN)        # MeV per unit
    Phi = two_cluster(True, True, 'singlet')
    K = norm_kernel_coeffs(Phi)
    e6 = antisymmetrised_6q_energy(Phi)
    dE = e6 - 2 * eN
    prof = core_profile(Phi, [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5,
                              1.75, 2.0, 2.5, 3.0, 4.0])
    return {
        'E_N': eN, 'E_Delta': eD, 'N_Delta_split_gcm': eD - eN,
        'g_cm_MeV': g_cm,
        'norm_kernel_K': K, 'n_at_R0': sum(K.values()) / K[0],
        'E_6q_R0': e6, 'two_free_N': 2 * eN, 'dE_CM_gcm': dE,
        'V_core0_MeV': float(dE) * g_cm,
        'profile_MeV': [(xb, g, g_cm * (g - 2 * float(eN))) for xb, g in prof],
    }


if __name__ == "__main__":
    r = derive_core()
    print(f"E_N = {r['E_N']} g_cm,  E_Δ = {r['E_Delta']} g_cm,  "
          f"N–Δ = {r['N_Delta_split_gcm']} g_cm  ⇒  g_cm = {r['g_cm_MeV']:.2f} MeV")
    print(f"norm kernel K = {{m:str for m}}: "
          f"{ {m: str(r['norm_kernel_K'][m]) for m in r['norm_kernel_K']} }")
    print(f"n(R=0) = {r['n_at_R0']}  (>0 ⇒ deuteron channel not Pauli-forbidden)")
    print(f"[6] 6q ⟨H_CM⟩(R=0) = {r['E_6q_R0']} g_cm   vs  two free N = "
          f"{r['two_free_N']} g_cm")
    print(f"ΔE_CM = {r['dE_CM_gcm']} g_cm = +{r['V_core0_MeV']:.1f} MeV  (REPULSIVE)")
    print("R/b   ⟨H_CM⟩(R)   V_core(MeV)")
    for xb, g, V in r['profile_MeV']:
        print(f"{xb:4.2f}  {g:8.4f}   {V:8.1f}")
