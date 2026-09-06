"""thermodynamics_interacting.py -- G10 residual: does the free sector's GGE
break down toward genuine (ETH) thermalisation once an interacting term is
turned on? (rubric row G10, F300 sec4.1 / F309 sec7.2 named next step)

F300 built lattice-native thermodynamics for the free (quadratic) photon
sector and showed, exactly, that the 2N branch occupations n_pm(k) are
conserved charges: the free sector reaches a generalised Gibbs ensemble
(GGE), never a Gibbs state (F300 sec4.1). F309 extended the equilibrium
side to the fermionic content and reaffirmed the same GGE caveat (F309
sec7.2, "nothing here shows the fermionic sector thermalises either").
Both findings name the same next step: "thermalisation on F110's link
Hamiltonian". F110's link Hamiltonian is a *pure gauge* Kogut-Susskind
construction on static charges -- F110 sec5 says plainly "dynamical
(quark) matter is not yet coupled" -- so coupling it to this tree's
Gaussian fermion machinery is a separate, larger engineering project, not
something this module attempts.

WHAT THIS MODULE DOES INSTEAD: the smallest interacting extension of the
free-fermion lattice machinery that can be built and exactly diagonalised
today. The free sector's defining structural feature -- an extensive tower
of exactly conserved mode occupations, giving a GGE rather than a Gibbs
state -- is not particular to the 3D BCC paired-photon/fermion dispersion;
it is the generic feature of ANY quadratic (free) fermion lattice
Hamiltonian, because a quadratic H is always diagonalised by *some* set of
single-particle modes whose occupations are then exactly conserved. So the
model's own single-band OBC hopping chain (the L^3 BCC walk collapsed to
its own single-band 1D analogue: same physics question, tractable Hilbert
space) already carries F300/F309's structural GGE feature, and adding a
quartic (density-density) term is the minimal, lattice-native way to break
the quadratic structure and ask whether the GGE gives way to ETH.

THE MINIMAL EXTENSION, AND WHY IT NEEDS TWO TERMS NOT ONE
----------------------------------------------------------
  H = -t sum_i (c_i^dag c_{i+1} + h.c.)          free / quadratic
      + V1 sum_i n_i n_{i+1}                     nearest-neighbour (NN)
      + V2 sum_i n_i n_{i+2}                      next-nearest-neighbour (NNN)

on an open (OBC) chain, half filling (N = L/2). This is not an arbitrary
choice: NN hopping + NN density-density interaction (V1 alone) is the
*textbook t-V model*, and it is exactly Jordan-Wigner-dual to the XXZ spin
chain, which is Bethe-ansatz integrable for every V1. So "the smallest
interacting extension" in the naive sense (V1 alone) turns on an
interaction but does NOT generically break integrability -- it trades one
integrable model for another. Adding V2 (next-nearest-neighbour) is the
standard, minimal way in the ETH literature (Santos & Rigol, Phys. Rev. E
81, 036206 (2010), arXiv:0910.2985) to leave the integrable manifold. This module therefore
runs THREE regimes side by side at the same L, t=1:

  "free"          V1 = V2 = 0   quadratic; every single-particle mode
                                occupation is exactly conserved (F300/F309's
                                own structural feature, reproduced here)
  "integrable_V1" V1 = 0.5, V2 = 0   interacting but JW-integrable (XXZ)
  "generic_V1V2"  V1 = 0.5, V2 = 0.5  generic, expected non-integrable

and asks, with three independent standard diagnostics, whether "generic"
alone shows the onset of eigenstate thermalisation (ETH) while
"integrable_V1" does not -- i.e. whether merely turning on AN interaction
is enough, or whether the interaction has to generically break integrability.

THE THREE DIAGNOSTICS (all standard, all computed exactly -- exact
diagonalisation in the fixed particle-number sector, no truncation, no
Trotter error; entanglement entropy computed by direct SVD of the
bipartite amplitude tensor, no approximation)

  D1  Level-spacing ratio <r> (Oganesyan-Huse / Atas et al.). Poisson
      (integrable) -> 0.3863; GOE (generic, quantum-chaotic) -> 0.5307.
      Computed within the reflection-parity-resolved subspace to remove
      the one discrete symmetry OBC leaves behind (translation is already
      broken by the open boundary).

  D2  Long-time entanglement-entropy plateau of a domain-wall quench,
      exact real-time evolution in the many-body eigenbasis (no Trotter),
      reported as a fraction of the absolute volume-law ceiling
      L_A ln 2. A GGE-constrained system should sit at a LOWER fraction
      than a genuinely thermalising one, and the gap should not close (it
      should widen) as L grows, because the extra conserved quantities are
      extensive.

  D3  Eigenstate-to-eigenstate fluctuation of the half-chain entanglement
      entropy across eigenstates in a narrow energy window around the
      quench's mean energy (the standard ETH diagnostic: D'Alessio, Kafri,
      Polkovnikov & Rigol, Adv. Phys. 65, 239 (2016)). ETH predicts this
      fluctuation SHRINKS with L; a non-ergodic (integrable) system shows
      no such shrinkage.

WHAT IS MODEL-NATIVE AND WHAT IS NOT
-------------------------------------
MODEL-NATIVE: the question being asked (does the free sector's GGE survive
an interaction) and the free/quadratic half of the machinery are directly
inherited from F300/F309 (the same "2N conserved charges -> GGE" structure,
same style of exact-real-time, no-truncation evolution). NOT model-native:
V1, V2 and t are dimensionless toy couplings, not derived from the BCC
walk's own coupling constants, and the chain is single-band OBC 1D, not
the model's own 3D two-branch BCC lattice. This is declared, not hidden --
see SCOPE below. The result is a genuine measured answer to "does an
interacting extension of THIS tree's free-sector machinery show
GGE-breakdown", using the model's own conserved-charge structure and
entropy machinery, at the size the actual coupling (F110's link
Hamiltonian to dynamical matter) is not yet built.

SCOPE -- what is NOT claimed
-----------------------------
1. This is not F110's link Hamiltonian coupled to matter. That coupling
   (gauge d.o.f. + dynamical fermions) is F300/F309's literal next step
   and remains open; see "next steps" below.
2. V1, V2, t are toy couplings on a 1D single-band reduction, not values
   derived from the BCC dispersion's own expansion coefficients (F300 sec
   2.1, F309 sec2). No claim is made that this chain's V1/V2 correspond to
   any specific interaction strength the model's own gauge sector would
   generate.
3. Finite L (10, 12, 14). The level-statistics and ETH-fluctuation trends
   are measured to move in the expected direction as L grows across three
   sizes; this is evidence of a trend, not a thermodynamic-limit proof.
4. The "free" regime's own <r> does not cleanly track the Poisson value
   across L (0.571, 0.438, 0.613 at L=10,12,14) -- flagged, not hidden.
   The likely cause is an extra exact symmetry beyond reflection (a
   bipartite/chiral single-particle spectrum symmetric under
   eps_k -> -eps_{L+1-k} gives extra exact many-body degeneracies at half
   filling that parity-resolution alone does not remove). This is a
   property of the EXACTLY solvable free point and does not affect the
   integrable_V1-vs-generic_V1V2 comparison, which is the finding's actual
   claim; see the finding file sec7 for the full discussion.

Everything is reported by `check_f375()`. Run as `__main__` to write the
artifact.
"""

from __future__ import annotations

import itertools
import math

from casim.numerics import xp  # noqa: F401  (D8: array namespace of record; = numpy today)
import numpy as np

# ==========================================================================
#  Basis / Hamiltonian construction (spinless fermions, occupation basis,
#  bit i of the python int == occupation of site i)
# ==========================================================================

def make_basis(L, N):
    basis = []
    for occ in itertools.combinations(range(L), N):
        b = 0
        for s in occ:
            b |= (1 << s)
        basis.append(b)
    basis.sort()
    index = {b: i for i, b in enumerate(basis)}
    return basis, index


def _popcount(x):
    return bin(x).count("1")


def _parity_below(b, k):
    mask = (1 << k) - 1
    return _popcount(b & mask) & 1


def build_H(L, N, t=1.0, V1=0.0, V2=0.0, eps=0.0, basis=None, index=None):
    """H = -t sum (c_i^dag c_{i+1} + h.c.) + V1 sum n_i n_{i+1}
         + V2 sum n_i n_{i+2} + eps sum (i - center) n_i   (OBC, 0..L-1).

    Fermionic sign uses the standard convention c_k|n> = (-1)^{parity_below(n,k)}
    |n with bit k cleared> (n_k=1 required); c_k^dag analogous. Validated
    (see finding F376 sec2) against (a) the exact free-fermion single-particle
    spectrum sum, machine precision, and (b) an independent full-Fock-space
    Jordan-Wigner construction, elementwise to 1.1e-16.
    """
    if basis is None:
        basis, index = make_basis(L, N)
    dim = len(basis)
    H = np.zeros((dim, dim))
    center = (L - 1) / 2.0
    for a, b in enumerate(basis):
        diag = 0.0
        for i in range(L):
            ni = (b >> i) & 1
            if not ni:
                continue
            diag += eps * (i - center) * ni
            if i + 1 < L:
                diag += V1 * ni * ((b >> (i + 1)) & 1)
            if i + 2 < L:
                diag += V2 * ni * ((b >> (i + 2)) & 1)
        H[a, a] += diag
        for i in range(L - 1):
            j = i + 1
            ni = (b >> i) & 1
            nj = (b >> j) & 1
            if ni == 0 and nj == 1:
                sign = (-1) ** _parity_below(b, j)
                b1 = b & ~(1 << j)
                sign *= (-1) ** _parity_below(b1, i)
                b2 = b1 | (1 << i)
                a2 = index[b2]
                H[a2, a] += -t * sign
                H[a, a2] += -t * sign
    return H, basis, index


def _reflect(b, L):
    r = 0
    for i in range(L):
        if (b >> i) & 1:
            r |= 1 << (L - 1 - i)
    return r


def build_parity_transform(basis, index, L):
    """Orthonormal change of basis diagonalising the reflection i -> L-1-i,
    which commutes with H for eps=0 (OBC hopping/V1/V2 are all reflection-
    symmetric). Returns (U, labels) with labels[k] in {'e','o'}, GROUPED (all
    'e' columns first, then all 'o') so that a caller may safely slice the
    first `sum(labels=='e')` rows/columns as the even block -- interleaving
    e/o columns silently produces a bogus block split (caught by C1)."""
    dim = len(basis)
    seen = np.zeros(dim, bool)
    even_cols, odd_cols = [], []
    for a, b in enumerate(basis):
        if seen[a]:
            continue
        a2 = index[_reflect(b, L)]
        if a2 == a:
            v = np.zeros(dim); v[a] = 1.0
            even_cols.append(v)
            seen[a] = True
        else:
            ve = np.zeros(dim); ve[a] = 1 / np.sqrt(2); ve[a2] = 1 / np.sqrt(2)
            vo = np.zeros(dim); vo[a] = 1 / np.sqrt(2); vo[a2] = -1 / np.sqrt(2)
            even_cols.append(ve); odd_cols.append(vo)
            seen[a] = seen[a2] = True
    cols = even_cols + odd_cols
    labels = ['e'] * len(even_cols) + ['o'] * len(odd_cols)
    U = np.array(cols).T
    return U, np.array(labels)


def gap_ratio(evals, trim=0.05):
    evals = np.sort(evals)
    d = np.diff(evals)
    d = d[d > 1e-12]
    n = len(d)
    lo, hi = int(n * trim), int(n * (1 - trim))
    d = d[lo:hi]
    r = np.minimum(d[1:], d[:-1]) / np.maximum(d[1:], d[:-1])
    return float(np.mean(r)), float(np.std(r) / np.sqrt(len(r)))


def half_chain_entropy_from_state(psi, basis, L, LA):
    """Von Neumann entropy (nats) of the reduced density matrix of the first
    LA sites, computed by direct SVD of the bipartite amplitude tensor. The
    fixed site-index-ordered occupation basis (c_1^dag...c_L^dag|0>) means a
    contiguous bipartition needs no extra Jordan-Wigner sign: all of A's
    creation operators already precede all of B's in the canonical ordering."""
    dimA = 1 << LA
    M = np.zeros((dimA, 1 << (L - LA)), dtype=complex)
    maskA = dimA - 1
    for a, b in enumerate(basis):
        M[b & maskA, b >> LA] = psi[a]
    s = np.linalg.svd(M, compute_uv=False)
    p = s ** 2
    p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


POISSON_R = 0.3863
GOE_R = 0.5307


def run_regime(L, N, t, V1, V2, tag, times, LA=None, n_window=60, n_window_sA=30):
    basis, index = make_basis(L, N)
    dim = len(basis)
    H, basis, index = build_H(L, N, t, V1, V2, 0.0, basis, index)

    U, labels = build_parity_transform(basis, index, L)
    Hp = U.T @ H @ U
    ne = int(np.sum(labels == 'e'))
    off = Hp.copy(); off[:ne, :ne] = 0; off[ne:, ne:] = 0
    parity_offblock_max = float(np.max(np.abs(off)))
    evals_e = np.linalg.eigvalsh(Hp[:ne, :ne])
    r_mean, r_err = gap_ratio(evals_e)

    evals, evecs = np.linalg.eigh(H)

    b0 = (1 << N) - 1  # domain wall: leftmost N sites filled
    a0 = index[b0]
    psi0 = np.zeros(dim); psi0[a0] = 1.0
    c = evecs.conj().T @ psi0
    E0 = float(np.real(np.sum(np.abs(c) ** 2 * evals)))

    if LA is None:
        LA = L // 2
    sA_t = []
    for tt in times:
        psit = evecs @ (np.exp(-1j * evals * tt) * c)
        sA_t.append(half_chain_entropy_from_state(psit, basis, L, LA))
    sA_plateau = float(np.mean(sA_t[len(sA_t) // 2:]))
    ceiling = LA * math.log(2.0)

    order = np.argsort(np.abs(evals - E0))
    win = order[:n_window]
    site_c = L // 2
    nc_diag = np.array([1.0 if (b >> site_c) & 1 else 0.0 for b in basis])
    nc_eigs = np.einsum('an,a->n', np.abs(evecs) ** 2, nc_diag)
    ETH_nc_std = float(np.std(nc_eigs[win]))

    sub = win[:min(n_window_sA, len(win))]
    sA_eigs = [half_chain_entropy_from_state(evecs[:, n], basis, L, LA) for n in sub]
    ETH_sA_std = float(np.std(sA_eigs))

    return {"tag": tag, "L": L, "N": N, "dim": dim, "n_even": ne,
            "parity_offblock_max": parity_offblock_max,
            "r_mean": r_mean, "r_err": r_err,
            "E0": E0, "sA_plateau": sA_plateau, "ceiling": ceiling,
            "frac_ceiling": sA_plateau / ceiling,
            "ETH_nc_std": ETH_nc_std, "ETH_sA_std": ETH_sA_std}


REGIMES = (("free", 0.0, 0.0), ("integrable_V1", 0.5, 0.0), ("generic_V1V2", 0.5, 0.5))


def scan(Ls=(10, 12, 14), t=1.0, n_times=30, t_max=40.0):
    times = list(np.linspace(0.5, t_max, n_times))
    out = {}
    for L in Ls:
        N = L // 2
        out[L] = [run_regime(L, N, t, V1, V2, tag, times) for tag, V1, V2 in REGIMES]
    return out


def free_ground_state_check(Ls=(6, 8, 10, 12, 14)):
    """C0: construction sanity -- the free (V1=V2=0) many-body ground state
    energy must equal the sum of the N lowest single-particle OBC
    tight-binding energies, -2 t cos(k pi/(L+1)), k=1..L. Exact identity."""
    worst = 0.0
    for L in Ls:
        N = L // 2
        basis, index = make_basis(L, N)
        H, _, _ = build_H(L, N, 1.0, 0.0, 0.0, 0.0, basis, index)
        gs = float(np.linalg.eigvalsh(H).min())
        sp = np.sort(-2.0 * np.cos(np.arange(1, L + 1) * np.pi / (L + 1)))
        gs_sp = float(sp[:N].sum())
        worst = max(worst, abs(gs - gs_sp))
    return worst


def check_f375(Ls=(10, 12, 14), v2_control=False):
    """v2_control=True: force V2 -> 0 in the 'generic_V1V2' regime (i.e. the
    declared gate control). This must turn C2/C3's GOE-separation checks red,
    because the 'generic' Hamiltonian then IS the integrable_V1 Hamiltonian."""
    regimes = list(REGIMES)
    if v2_control:
        regimes = [(tag, V1, (0.0 if tag == "generic_V1V2" else V2))
                   for tag, V1, V2 in regimes]

    times = list(np.linspace(0.5, 40.0, 30))
    by_L = {}
    for L in Ls:
        N = L // 2
        by_L[L] = [run_regime(L, N, 1.0, V1, V2, tag, times) for tag, V1, V2 in regimes]

    checks = []

    def add(cid, desc, ok, measured, expected):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok),
                        "measured": measured, "expected": expected})

    c0 = free_ground_state_check()
    add("C0", "construction check: free many-body GS == sum of N lowest "
              "single-particle OBC levels (validates the fermionic sign "
              "convention)", c0 < 1e-10, c0, "< 1e-10")

    off_max = max(r["parity_offblock_max"] for L in Ls for r in by_L[L])
    add("C1", "reflection-parity transform block-diagonalises H (U orthonormal, "
              "H commutes with reflection) for every regime and L",
        off_max < 1e-10, off_max, "< 1e-10")

    L_top = max(Ls)
    r_int = next(r for r in by_L[L_top] if r["tag"] == "integrable_V1")["r_mean"]
    err_int = next(r for r in by_L[L_top] if r["tag"] == "integrable_V1")["r_err"]
    add("C2", f"integrable_V1 <r> consistent with Poisson ({POISSON_R}) at L={L_top}",
        abs(r_int - POISSON_R) < 3 * err_int + 0.01, r_int, f"~ {POISSON_R}")

    r_gen = next(r for r in by_L[L_top] if r["tag"] == "generic_V1V2")["r_mean"]
    err_gen = next(r for r in by_L[L_top] if r["tag"] == "generic_V1V2")["r_err"]
    sigma_from_poisson = (r_gen - POISSON_R) / err_gen
    add("C3", f"generic_V1V2 <r> separated from Poisson by >10 sigma and closer "
              f"to GOE ({GOE_R}) than to Poisson at L={L_top} "
              "-- RED under the V2->0 control",
        (sigma_from_poisson > 10.0) and (abs(r_gen - GOE_R) < abs(r_gen - POISSON_R)),
        {"r_gen": r_gen, "sigma_from_Poisson": sigma_from_poisson}, "> 10 sigma, closer to GOE")

    r_gen_by_L = [next(r for r in by_L[L] if r["tag"] == "generic_V1V2")["r_mean"] for L in sorted(Ls)]
    r_int_by_L = [next(r for r in by_L[L] if r["tag"] == "integrable_V1")["r_mean"] for L in sorted(Ls)]
    add("C4", "finite-size flow: generic_V1V2 <r> increases with L (toward GOE) "
              "and integrable_V1 <r> converges toward Poisson",
        (r_gen_by_L[-1] > r_gen_by_L[0]) and (abs(r_int_by_L[-1] - POISSON_R) < abs(r_int_by_L[0] - POISSON_R)),
        {"generic_by_L": r_gen_by_L, "integrable_by_L": r_int_by_L}, "monotone toward class value")

    frac_int_by_L = [next(r for r in by_L[L] if r["tag"] == "integrable_V1")["frac_ceiling"] for L in sorted(Ls)]
    frac_gen_by_L = [next(r for r in by_L[L] if r["tag"] == "generic_V1V2")["frac_ceiling"] for L in sorted(Ls)]
    add("C5", "entanglement-plateau fraction of the volume-law ceiling: "
              "generic_V1V2 > integrable_V1 at every L, and the gap does not "
              "close as L grows (GGE-style suppression persists for V1-only)",
        all(g > i for g, i in zip(frac_gen_by_L, frac_int_by_L))
        and (frac_gen_by_L[-1] - frac_int_by_L[-1]) >= (frac_gen_by_L[0] - frac_int_by_L[0]) - 0.02,
        {"integrable_by_L": frac_int_by_L, "generic_by_L": frac_gen_by_L}, "generic > integrable, gap non-closing")

    sA_std_int_by_L = [next(r for r in by_L[L] if r["tag"] == "integrable_V1")["ETH_sA_std"] for L in sorted(Ls)]
    sA_std_gen_by_L = [next(r for r in by_L[L] if r["tag"] == "generic_V1V2")["ETH_sA_std"] for L in sorted(Ls)]
    add("C6", "ETH signature: eigenstate-to-eigenstate entanglement-entropy "
              "fluctuation shrinks with L for generic_V1V2 and does not shrink "
              "for integrable_V1",
        (sA_std_gen_by_L[-1] < sA_std_gen_by_L[0]) and (sA_std_int_by_L[-1] >= sA_std_int_by_L[0] - 0.02),
        {"integrable_by_L": sA_std_int_by_L, "generic_by_L": sA_std_gen_by_L}, "generic shrinks, integrable does not")

    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "all_pass": n_pass == len(checks),
            "by_L": {str(L): by_L[L] for L in Ls},
            "control": {"v2_control": v2_control}}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    out = check_f375()
    for c in out["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:4s} {c['desc']}")
    print(f"  {out['n_pass']}/{out['n_total']}")
    path = results_path("F376_interacting_sector_eth_onset.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("wrote", path)
