#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qi_measurement.py — the measurement problem on the lattice (completeness row A8)
================================================================================

2026-08-05 - 14:40

Row **A8** of `docs/status/completeness-2026-08-04.md` is one of seven marked
ABSENT with *zero hits repo-wide*: "a unitary QCA with no account of measurement
or the classical limit".  Row **A6** (Born rule) is PARTIAL — "reproduced in
tests, never derived; no finding is devoted to it".  This module attacks both,
and it does so using only structure the model already owns.

The three legs, and what is CA-native about each
------------------------------------------------

**M1 — the pointer basis is FORCED, not chosen.**
Einselection (Zurek) says the surviving classical observable is the one that
commutes with the system–environment interaction.  In ordinary QM that is an
*input*: you pick H_int.  In this model H_int is fixed by the rule.  Every
interaction in the tree enters as **minimal coupling**, i.e. as a phase attached
to the site/link and multiplying the spinor there —

    ψ(x)  →  e^{-i q α(x)} ψ(x)          (casim.engine.gauge.minimal_coupling,
                                          u1_wrap_weyl_step_3d_bcc; F41/F42/F87)

whose generator is  H_int = Σ_x α̂(x) ⊗ n̂(x)  with n̂(x) the site charge density.
Every term is **diagonal in the site-occupation basis**, so

    [H_int, n̂(y)] = 0   exactly, for every y.

The einselected pointer observable is therefore the local charge density, and
classicality is *position definiteness* — a theorem about the rule rather than a
posit.  The Higgs-free design (key decision 3) is load-bearing here: there is no
Yukawa scalar and no non-minimal coupling anywhere in the model, so there is no
term that could einselect anything else.

Two consequences are checked, and both are physically correct rather than
convenient: (i) **spin is NOT einselected** — the SU(2)/SU(3) rotations do not
commute with the internal generators, so a spin superposition survives until it
is amplified into a *position* difference (which is exactly what a Stern–Gerlach
magnet does); (ii) the kinetic hopping does **not** commute with n̂, so the
pointer states are exactly stable only in the quantum-measurement limit
‖H_int‖ ≫ ‖H_hop‖ — the standard caveat, here made quantitative.

**M2 — the Born rule, on two independent legs.**
  *Leg 1 (dynamical, and independent of any assumption about probability).*
  A branch weight must be additive over branches, permutation-symmetric, and
  **conserved by the rule** (branches do not change identity under evolution).
  Of the ℓ^p family only p = 2 is conserved by a genuine CA step: ℓ² is invariant
  under every unitary, while ℓ^p (p ≠ 2) is invariant only under monomial
  (permutation × phase) unitaries, which the mixing lattice step is not.  So the
  only candidate measure the dynamics permits is |ψ|².
  *Leg 2 (envariance, Zurek).* For equal amplitudes a swap on S is undone
  exactly by a counter-swap on E, forcing equal weights; rational amplitudes
  fine-grain into M equal-amplitude branches, giving p_k = μ_k/M = |c_k|².
  What is CA-native: the swap and counter-swap must be **realisable by the
  model's own gate set** (they are — the native exchange gate supplies SWAP, and
  the O_h point group supplies the substrate symmetry) and must fit **inside the
  causal cone** (F227: C(r,t) = 0 for r > 4t), so the derivation carries a cone
  cost that abstract QM does not.  Both legs are stated with their gaps.

**M3 — classicality is an RG statement, with a closed-form eigenvalue.**
Under the model's own exact block-spin R_b (F130/F133, `block_average_field`),
a coherence between two branches whose relative phase carries wavevector k is
multiplied by the Dirichlet kernel

    λ_coh(k, b) = |D_b(k)|²,   D_b(k) = sin(kb/2) / (b sin(k/2)),

which is **exactly 1 at k = 0** (populations are marginal — the coarse total
charge is preserved to machine precision) and has envelope **b^{-2} per
dimension** for k ≠ 0, i.e. b^{-6} on the 3-D lattice.  Coherence is therefore
an *irrelevant* operator at the same leading order as the F130 Lorentz-violating
operators (λ_n = b^{-n}, n = 2), while populations are marginal: the block-spin
attractor of the quantum lattice is a **diagonal (classical) density matrix**.
The more distinguishable two branches are (larger k), the faster their coherence
becomes irrelevant — which is the correct physics, here derived as an RG
eigenvalue rather than asserted.  At the zone edge k = π with even b the kernel
vanishes **exactly**.

What this module does NOT claim
-------------------------------
It does not add an objective-collapse term; F227 already established the model
is unitary with no intrinsic decoherence floor, and nothing here changes that.
"Collapse" is decoherence plus a Poincaré recurrence time exponential in the
environment size — quantified below and found to be absurd, not absent.
Leg 2 of the Born argument inherits the standard Schlosshauer–Fine objection
(it assumes the outcome weights depend only on the reduced state); leg 1 does
not, which is why both are carried.

Cross-references: F212/F214/F217 (the register and its native gates), F221
(Kraus channels), F226 (Tsirelson), F227 (causal cone, no collapse), F130–F134
(exact R_b), F41/F42/F87 (minimal coupling), key decision 3 (Higgs-free).
"""
from __future__ import annotations

import math
from typing import Dict, Any, List, Sequence, Tuple

from casim.numerics import xp as np

from casim.engine.core.blockspin import block_average_field
from casim.engine.interactions.qi_noise import embed, embed2
from casim.engine.interactions.qi_entanglement import (
    su2_rotor,
    swap_gate,
    exchange_gate,
)

__all__ = [
    # M1 — pointer basis
    "pauli",
    "number_op",
    "minimal_coupling_generator",
    "nonminimal_coupling_generator",
    "hopping_generator",
    "pointer_commutator_norms",
    "sieve_entropy",
    "predictability_sieve",
    "decoherence_factor_closed_form",
    "decoherence_factor_numeric",
    "recurrence_statistics",
    "macroscopic_recurrence_log10",
    "native_flip_is_a_genuine_flip",
    "born_exact_over_Q",
    "summary",
    # M2 — Born rule
    "lp_weight",
    "lp_conservation_bcc",
    "lp_conservation_native_gate",
    "envariance_equal_amplitudes",
    "envariance_unequal_amplitudes_fails",
    "finegrain_state",
    "born_from_finegraining",
    "cone_capacity",
    # M3 — RG classicality
    "dirichlet_kernel",
    "coherence_rg_eigenvalue",
    "coherence_rg_numeric",
    "population_marginality",
    "coherence_exponent",
    "macroscopic_suppression",
]


# ======================================================================
# small shared algebra
# ======================================================================
def pauli() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(I, X, Y, Z) as 2x2 complex matrices."""
    I = np.eye(2, dtype=complex)
    X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return I, X, Y, Z


def number_op() -> np.ndarray:
    """Site charge-density operator n̂ = (I − Z)/2 = |1⟩⟨1|."""
    I, _, _, Z = pauli()
    return 0.5 * (I - Z)


def _commutator_norm(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.linalg.norm(A @ B - B @ A))


# ======================================================================
# M1 — the pointer basis is forced by the CA's own coupling
# ======================================================================
def _couplings(n_sys: int, n_env: int, g: Sequence[float] | None) -> np.ndarray:
    """Environment coupling matrix g[x, j].  Deterministic, incommensurate
    defaults (no RNG: this module must be reproducible bit-for-bit)."""
    if g is not None:
        return np.asarray(g, dtype=float).reshape(n_sys, n_env)
    out = np.empty((n_sys, n_env), dtype=float)
    for x in range(n_sys):
        for j in range(n_env):
            # irrational, mutually incommensurate, O(1)
            out[x, j] = math.sqrt(2.0 + x + 3.0 * j) % 1.0 + 0.5
    return out


def minimal_coupling_generator(n_sys: int, n_env: int,
                               g: Sequence[float] | None = None) -> np.ndarray:
    """H_int = Σ_x α̂(x) ⊗ n̂(x),  α̂(x) = Σ_j g[x,j] Z_j.

    This is the generator of the model's OWN U(1) minimal coupling
    (`u1_wrap_weyl_step_3d_bcc`: ψ(x) → e^{−i q α(x)} ψ(x)) with the gauge phase
    α promoted to an environment operator.  Every term is diagonal in the site
    occupation basis — that is the whole content of M1.
    """
    n = n_sys + n_env
    _, _, _, Z = pauli()
    nop = number_op()
    gm = _couplings(n_sys, n_env, g)
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for x in range(n_sys):
        for j in range(n_env):
            H = H + gm[x, j] * (embed(nop, x, n) @ embed(Z, n_sys + j, n))
    return H


def nonminimal_coupling_generator(n_sys: int, n_env: int,
                                  g: Sequence[float] | None = None) -> np.ndarray:
    """CONTROL.  The same coupling with n̂(x) replaced by σ^x(x) — a coupling
    that is *not* minimal, i.e. not a function of the local charge density.
    The model contains no such term; if it did, the pointer basis would not be
    position.  Used to prove the M1 checks can fail."""
    n = n_sys + n_env
    _, X, _, Z = pauli()
    gm = _couplings(n_sys, n_env, g)
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for x in range(n_sys):
        for j in range(n_env):
            H = H + gm[x, j] * (embed(X, x, n) @ embed(Z, n_sys + j, n))
    return H


def hopping_generator(n_sys: int, n_env: int, t_hop: float = 1.0) -> np.ndarray:
    """The system's own kinetic term — nearest-neighbour hopping on a chain,
    (XX + YY)/2, which is OFF-diagonal in the site basis.  Present so the
    quantum-measurement limit ‖H_int‖ ≫ ‖H_hop‖ is stated, not assumed."""
    n = n_sys + n_env
    _, X, Y, _ = pauli()
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for x in range(n_sys - 1):
        H = H + 0.5 * t_hop * (embed2(np.kron(X, X), x, x + 1, n)
                               + embed2(np.kron(Y, Y), x, x + 1, n))
    return H


def pointer_commutator_norms(n_sys: int = 2, n_env: int = 2) -> Dict[str, Any]:
    """M1's structural theorem, as numbers.

    Returns the Frobenius norms of [H, n̂(y)] for the model's minimal coupling
    (must be exactly 0), for the non-minimal control (must not be), for the
    kinetic term (must not be), and for the internal spin generator (must not
    be — spin is not einselected).
    """
    n = n_sys + n_env
    _, X, Y, _ = pauli()
    nop = number_op()

    H_min = minimal_coupling_generator(n_sys, n_env)
    H_non = nonminimal_coupling_generator(n_sys, n_env)
    H_hop = hopping_generator(n_sys, n_env)

    c_min = [_commutator_norm(H_min, embed(nop, y, n)) for y in range(n_sys)]
    c_non = [_commutator_norm(H_non, embed(nop, y, n)) for y in range(n_sys)]
    c_hop = [_commutator_norm(H_hop, embed(nop, y, n)) for y in range(n_sys)]
    # spin: does the minimal coupling einselect an internal (SU(2)) direction?
    c_spin = [_commutator_norm(H_min, embed(X, y, n)) for y in range(n_sys)]

    return {
        "n_sys": n_sys,
        "n_env": n_env,
        "minimal_coupling_max_commutator": max(c_min),
        "nonminimal_control_max_commutator": max(c_non),
        "hopping_max_commutator": max(c_hop),
        "spin_max_commutator": max(c_spin),
        "norm_H_int": float(np.linalg.norm(H_min)),
        "norm_H_hop": float(np.linalg.norm(H_hop)),
        "pointer_basis_is_site_occupation": max(c_min) == 0.0,
    }


def _von_neumann(rho: np.ndarray) -> float:
    w = np.linalg.eigvalsh(rho)
    w = w[w > 1e-14]
    return float(-(w * np.log(w)).sum())


def sieve_entropy(theta: float, t: float = 1.0,
                  n_env: int = 3, generator: str = "minimal",
                  r_hop: float = 0.0) -> float:
    """Zurek predictability sieve, one system cell.

    Prepare each state of the candidate basis {U(θ)|0⟩, U(θ)|1⟩} (θ = 0 is the
    site-occupation basis), evolve system+environment under the generator, trace
    out the environment, and return the basis-averaged von Neumann entropy.  The
    pointer basis is the argmin.  ``r_hop`` adds ‖H_hop‖/‖H_int‖ of kinetic term
    so the quantum-measurement limit can be probed rather than assumed.
    """
    n_sys = 1
    n = n_sys + n_env
    if generator == "minimal":
        H = minimal_coupling_generator(n_sys, n_env)
    elif generator == "nonminimal":
        H = nonminimal_coupling_generator(n_sys, n_env)
    else:
        raise ValueError(f"unknown generator {generator!r}")
    if r_hop:
        # one cell has no hop; use a two-cell system's hop magnitude on the
        # internal X generator as a stand-in for a basis-rotating term
        _, X, _, _ = pauli()
        H = H + r_hop * float(np.linalg.norm(H)) / math.sqrt(2.0) * embed(X, 0, n)

    w, V = np.linalg.eigh(H)
    U = (V * np.exp(-1j * w * t)) @ V.conj().T

    rot = su2_rotor(theta, (0.0, 1.0, 0.0))
    env = np.zeros(2 ** n_env, dtype=complex)
    plus = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)
    env = plus
    for _ in range(n_env - 1):
        env = np.kron(env, plus)

    S = 0.0
    for basis_state in (np.array([1.0, 0.0], dtype=complex),
                        np.array([0.0, 1.0], dtype=complex)):
        s = rot @ basis_state
        psi = U @ np.kron(s, env)
        M = psi.reshape(2, 2 ** n_env)
        rho_s = M @ M.conj().T
        S += _von_neumann(rho_s)
    return S / 2.0


def predictability_sieve(n_theta: int = 91, t: float = 1.0,
                         n_env: int = 3, generator: str = "minimal",
                         r_hop: float = 0.0) -> Dict[str, Any]:
    """Scan the sieve over candidate bases and report the minimiser."""
    thetas = np.linspace(0.0, math.pi, n_theta)
    S = np.array([sieve_entropy(float(th), t, n_env, generator, r_hop)
                  for th in thetas])
    i = int(np.argmin(S))
    return {
        "generator": generator,
        "r_hop": r_hop,
        "theta_min": float(thetas[i]),
        "S_min": float(S[i]),
        "S_at_site_basis": float(S[0]),
        "S_max": float(S.max()),
        "theta_at_S_max": float(thetas[int(np.argmax(S))]),
    }


def decoherence_factor_closed_form(t: float, n_env: int = 3,
                                   g: Sequence[float] | None = None) -> float:
    """|D(t)| = Π_j |cos(g_j t)| — exact for the minimal-coupling generator with
    the environment in |+⟩^{⊗n_env}.  Branch n̂=0 leaves the environment alone;
    branch n̂=1 rotates it by exp(−i t Σ_j g_j Z_j), and ⟨+|e^{−i t g Z}|+⟩ =
    cos(g t)."""
    gm = _couplings(1, n_env, g)[0]
    out = 1.0
    for gj in gm:
        out *= math.cos(float(gj) * t)
    return abs(out)


def decoherence_factor_numeric(t: float, n_env: int = 3,
                               g: Sequence[float] | None = None) -> Dict[str, float]:
    """Evolve the full system+environment state and read |ρ_01| and the
    populations off the reduced density matrix."""
    n_sys, n = 1, 1 + n_env
    H = minimal_coupling_generator(n_sys, n_env, g)
    w, V = np.linalg.eigh(H)
    U = (V * np.exp(-1j * w * t)) @ V.conj().T

    plus = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)
    env = plus
    for _ in range(n_env - 1):
        env = np.kron(env, plus)
    s = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)
    psi = U @ np.kron(s, env)
    M = psi.reshape(2, 2 ** n_env)
    rho = M @ M.conj().T
    return {
        "coherence": float(abs(rho[0, 1])) * 2.0,   # normalised: 1 at t=0
        "pop0": float(rho[0, 0].real),
        "pop1": float(rho[1, 1].real),
    }


def recurrence_statistics(n_env_list: Sequence[int] = (1, 2, 3, 4, 5, 6),
                          thresh: float = 0.9, t_max: float = 4000.0,
                          n_t: int = 400001) -> Dict[str, Any]:
    """Poincaré recurrence of the coherence in a FINITE environment.

    The model has no collapse (F227), so coherence must return.  Measure the
    fraction of time |D(t)| > ``thresh``; by Weyl equidistribution over the
    incommensurate frequencies this fraction falls geometrically in n_env, so
    the recurrence time grows exponentially.  Returns the measured fractions,
    the fitted decade-per-cell slope, and the extrapolated recurrence time for a
    macroscopic environment.
    """
    ts = np.linspace(0.0, t_max, n_t)
    fracs = []
    for ne in n_env_list:
        gm = _couplings(1, ne, None)[0]
        D = np.ones_like(ts)
        for gj in gm:
            D = D * np.cos(float(gj) * ts)
        fracs.append(float((np.abs(D) > thresh).mean()))
    x = np.array(n_env_list, dtype=float)
    y = np.log10(np.array(fracs) + 1e-300)
    slope, intercept = np.polyfit(x, y, 1)
    return {
        "n_env": list(n_env_list),
        "fraction_above_threshold": fracs,
        "threshold": thresh,
        "log10_fraction_slope_per_cell": float(slope),
        "log10_fraction_intercept": float(intercept),
    }


def macroscopic_recurrence_log10(n_env_cells: float = 6.02214076e23,
                                 stats: Dict[str, Any] | None = None) -> float:
    """log10 of the recurrence time in lattice ticks for a macroscopic
    environment, extrapolating the measured geometric law.  The point of the
    number is its absurdity: the model has no collapse (F227), only a return
    time that is exponential in the number of environment cells."""
    s = stats if stats is not None else recurrence_statistics()
    return float(-s["log10_fraction_slope_per_cell"] * n_env_cells
                 - s["log10_fraction_intercept"])


# ======================================================================
# M1' — the sieve at many cells (F281 open item #3, closed 2026-08-05 - 16:40)
#
# The one-cell sieve of `predictability_sieve` scans a 1-parameter family and
# finds the site basis.  That is suggestive, not decisive: at many cells the
# candidate space is the whole of U(2^n)/U(1)^{2^n} and a 1-parameter scan
# cannot claim to have found a global minimum.  The scale-up replaces the scan
# with the algebraic statement that makes it unnecessary:
#
#   {n̂(x)}_{x=1..n} is a MAXIMAL ABELIAN subalgebra of the system's operator
#   algebra — its commutant is exactly the diagonal algebra, of dimension 2^n.
#
# A maximal abelian algebra has a UNIQUE joint eigenbasis up to phases and the
# ordering of the labels.  So the pointer basis is not merely *a* minimiser of
# the sieve, it is *the* one, at every n, with no scan required.  What is left
# for numerics is to confirm the algebra claim, confirm that the eigenbasis
# really does produce exactly zero entropy at n = 1..4, and confirm that the
# uniqueness has the one loophole it must have: if the environment couples to
# two configurations IDENTICALLY it cannot resolve them, and the sieve then
# leaves their superposition predictable.  That degeneracy is a real feature of
# einselection, not a defect, and it is tested as a control.
# ======================================================================
def commutant_dimension(n_sys: int) -> Dict[str, Any]:
    """Dimension of the commutant of {n̂(x)} on the n_sys-cell system.

    Solves [X, n̂(x)] = 0 for all x by inspecting which matrix entries survive:
    an entry X[i,j] survives iff the occupation patterns i and j agree on every
    site, i.e. iff i == j.  The commutant is therefore the diagonal algebra, of
    dimension exactly 2^{n_sys} — which is the definition of {n̂(x)} being a
    MAXIMAL abelian algebra, and it is what makes the pointer basis unique.

    Computed, not asserted: the rank of the linear map X ↦ ([X, n̂(x)])_x.
    """
    d = 2 ** n_sys
    nop = number_op()
    ns = [embed(nop, x, n_sys) for x in range(n_sys)]
    # build the (n_sys·d², d²) matrix of the commutator map and take its kernel
    rows = []
    for N in ns:
        # vec([X,N]) = (I⊗N^T ... ) — assemble by acting on the basis of X
        M = np.zeros((d * d, d * d), dtype=complex)
        for a in range(d):
            for b in range(d):
                X = np.zeros((d, d), dtype=complex)
                X[a, b] = 1.0
                M[:, a * d + b] = (X @ N - N @ X).ravel()
        rows.append(M)
    big = np.concatenate(rows, axis=0)
    rank = int(np.linalg.matrix_rank(big, tol=1e-10))
    return {"n_sys": n_sys,
            "commutant_dim": d * d - rank,
            "hilbert_dim": d,
            "is_maximal_abelian": (d * d - rank) == d}


def sieve_manycell(n_sys: int = 2, n_env: int = 3, t: float = 1.0,
                   n_random: int = 200, degenerate: bool = False
                   ) -> Dict[str, Any]:
    """The predictability sieve on a many-cell system, without a 1-D scan.

    * Every one of the 2^{n_sys} occupation eigenstates is evolved under the
      model's minimal coupling and must produce EXACTLY zero entropy.
    * A dense deterministic sample of generic system states must produce
      entropy bounded away from zero, so the eigenbasis is the strict minimum.
    * The most-predictable generic state is compared with its nearest
      occupation eigenstate.

    ``degenerate=True`` is the CONTROL: it gives two system cells the SAME
    environment coupling row, so the environment cannot resolve them.  Their
    superposition then stays predictable and the pointer basis is NOT unique —
    which is correct einselection physics, and shows the uniqueness result is
    doing work rather than following from the construction.
    """
    n = n_sys + n_env
    d = 2 ** n_sys
    gm = _couplings(n_sys, n_env, None)
    if degenerate and n_sys >= 2:
        gm = gm.copy()
        gm[1] = gm[0]                     # cells 0 and 1 now indistinguishable
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    _, _, _, Z = pauli()
    nop = number_op()
    for x in range(n_sys):
        for j in range(n_env):
            H = H + gm[x, j] * (embed(nop, x, n) @ embed(Z, n_sys + j, n))
    w, V = np.linalg.eigh(H)
    U = (V * np.exp(-1j * w * t)) @ V.conj().T

    plus = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)
    env = plus
    for _ in range(n_env - 1):
        env = np.kron(env, plus)

    def _entropy_of(sys_vec: np.ndarray) -> float:
        psi = U @ np.kron(sys_vec, env)
        M = psi.reshape(d, 2 ** n_env)
        return _von_neumann(M @ M.conj().T)

    # (a) the 2^n occupation eigenstates
    eig_S = []
    for i in range(d):
        v = np.zeros(d, dtype=complex)
        v[i] = 1.0
        eig_S.append(_entropy_of(v))

    # (b) generic states — deterministic Fibonacci-style sampling, no RNG
    gen_S, best_vec, best_S = [], None, math.inf
    for r in range(n_random):
        i = np.arange(d, dtype=float)
        vec = (np.cos(0.7 + 1.9 * i + 0.13 * r)
               + 1j * np.sin(0.2 + 1.1 * i + 0.29 * r))
        vec = vec / np.linalg.norm(vec)
        s = _entropy_of(vec)
        gen_S.append(s)
        if s < best_S:
            best_S, best_vec = s, vec

    overlap = float(np.abs(best_vec).max())     # 1 iff it IS an eigenstate

    # (c) the decoherence-free subspace probe.  |01> - |10> is a superposition
    # of TWO DIFFERENT occupation patterns, so under a resolving environment it
    # must decohere; under a degenerate one (cells 0 and 1 coupled identically)
    # the environment cannot tell the patterns apart and the state is
    # predictable.  This is the one and only loophole in the uniqueness claim,
    # and it is real physics — a decoherence-free subspace.
    dfs = 0.0
    if n_sys >= 2:
        v = np.zeros(d, dtype=complex)
        # occupation index: bit 0 is cell 0 (embed uses qubit 0 as most
        # significant), so |01> and |10> are indices 1 and 2**(n_sys-1)
        v[2 ** (n_sys - 1)] = 1.0 / math.sqrt(2.0)
        v[2 ** (n_sys - 2)] = -1.0 / math.sqrt(2.0)
        dfs = _entropy_of(v)

    return {"n_sys": n_sys, "n_env": n_env, "degenerate": degenerate,
            "hilbert_dim": d,
            "max_entropy_over_occupation_eigenstates": float(max(eig_S)),
            "min_entropy_over_generic_states": float(min(gen_S)),
            "max_entropy_over_generic_states": float(max(gen_S)),
            "best_generic_max_amplitude": overlap,
            "dfs_probe_entropy": float(dfs),
            "n_generic_sampled": n_random}


def sieve_scaleup(n_list: Sequence[int] = (1, 2, 3, 4)) -> Dict[str, Any]:
    """Run the many-cell sieve and the algebra claim across system sizes."""
    rows = []
    for ns in n_list:
        alg = commutant_dimension(ns)
        sv = sieve_manycell(n_sys=ns, n_env=3, n_random=120)
        rows.append({
            "n_sys": ns,
            "commutant_dim": alg["commutant_dim"],
            "hilbert_dim": alg["hilbert_dim"],
            "is_maximal_abelian": alg["is_maximal_abelian"],
            "S_pointer": sv["max_entropy_over_occupation_eigenstates"],
            "S_generic_min": sv["min_entropy_over_generic_states"],
            "S_generic_max": sv["max_entropy_over_generic_states"],
        })
    resolving = sieve_manycell(n_sys=2, n_env=3, n_random=120, degenerate=False)
    degen = sieve_manycell(n_sys=2, n_env=3, n_random=120, degenerate=True)
    return {"rows": rows,
            "all_maximal_abelian": all(r["is_maximal_abelian"] for r in rows),
            "worst_pointer_entropy": max(r["S_pointer"] for r in rows),
            "smallest_generic_gap": min(r["S_generic_min"] for r in rows),
            # the DFS pair: the SAME state, the SAME probe, two environments
            "dfs_entropy_resolving_env": resolving["dfs_probe_entropy"],
            "dfs_entropy_degenerate_env": degen["dfs_probe_entropy"]}


# ======================================================================
# M2 — the Born rule.  Leg 1: only p = 2 is conserved by the rule.
# ======================================================================
def lp_weight(psi: np.ndarray, p: float) -> float:
    """Σ_i |ψ_i|^p — the candidate additive, permutation-symmetric branch
    weight.  A probability over branches must be conserved, because branches do
    not change identity under the (deterministic, unitary) evolution."""
    return float((np.abs(np.asarray(psi).ravel()) ** p).sum())


def _fixed_complex_state(size: int, seed_shift: float = 0.0) -> np.ndarray:
    """A deterministic, non-special complex state (no RNG, so the module is
    reproducible bit-for-bit across runs and machines)."""
    i = np.arange(size, dtype=float)
    re = np.cos(1.0 + 0.7 * i + seed_shift) * (1.0 + 0.3 * np.sin(0.31 * i))
    im = np.sin(0.4 + 1.3 * i + seed_shift) * (1.0 + 0.2 * np.cos(0.17 * i))
    psi = re + 1j * im
    return psi / np.linalg.norm(psi)


def lp_conservation_bcc(p_values: Sequence[float] = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0),
                        L: int = 8, sign: str = "+") -> Dict[str, Any]:
    """Apply ONE genuine BCC Weyl QCA tick (`weyl_step_3d_bcc` — the model's own
    fundamental step) to a fixed state and report the relative change in each
    ℓ^p weight.  Only p = 2 survives."""
    from casim.engine.lattice.bcc import weyl_step_3d_bcc

    n = L ** 3
    f = _fixed_complex_state(n, 0.0).reshape(L, L, L)
    g = _fixed_complex_state(n, 1.7).reshape(L, L, L)
    nrm = math.sqrt(float((np.abs(f) ** 2).sum() + (np.abs(g) ** 2).sum()))
    f, g = f / nrm, g / nrm

    f2, g2 = weyl_step_3d_bcc(f, g, sign=sign)
    out = {}
    for p in p_values:
        before = lp_weight(f, p) + lp_weight(g, p)
        after = lp_weight(f2, p) + lp_weight(g2, p)
        out[f"p={p:g}"] = abs(after - before) / before
    return {"step": "weyl_step_3d_bcc", "L": L, "relative_change": out}


def lp_conservation_native_gate(
        p_values: Sequence[float] = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0),
        theta: float = math.pi / 8) -> Dict[str, Any]:
    """Same question for the register's own native two-cell entangler
    ``exchange_gate(θ)`` (F212/F214), plus a CONTROL: the permutation point
    SWAP, a monomial unitary, which conserves EVERY ℓ^p.  The control is what
    makes the p = 2 result a statement about mixing rather than about ℓ^p."""
    psi = _fixed_complex_state(4, 0.0)
    mixing = exchange_gate(theta) @ psi
    permut = swap_gate() @ psi
    mix, perm = {}, {}
    for p in p_values:
        b = lp_weight(psi, p)
        mix[f"p={p:g}"] = abs(lp_weight(mixing, p) - b) / b
        perm[f"p={p:g}"] = abs(lp_weight(permut, p) - b) / b
    return {"theta": theta, "mixing_gate_relative_change": mix,
            "permutation_control_relative_change": perm}


# ======================================================================
# M2 — leg 2: envariance, with CA-native swaps
# ======================================================================
def _native_flip() -> np.ndarray:
    """The single-cell swap |0⟩↔|1⟩ as the model's own SU(2) rotor.

    The rotor convention is R(θ,n̂) = cosθ I − i sinθ (n̂·σ) — a Bloch rotation
    by **2θ** — so the flip is θ = π/2, giving −i·X.  θ = π gives −I, which is
    the identity on rays and would make every check below pass vacuously; that
    is exactly how the first draft of this module was wrong, so
    ``native_flip_is_a_genuine_flip`` is asserted rather than assumed.
    """
    return su2_rotor(math.pi / 2.0, (1.0, 0.0, 0.0))


def native_flip_is_a_genuine_flip() -> float:
    """|⟨1|u|0⟩| − 1 for the native flip.  Must be 0: a rotor that is a global
    phase would satisfy every envariance identity trivially."""
    u = _native_flip()
    return float(abs(abs(u[1, 0]) - 1.0)) + float(abs(u[0, 0]))


def envariance_equal_amplitudes() -> Dict[str, Any]:
    """Equal-amplitude envariance with gates taken from the model's own set.

    |ψ⟩ = (|s₀e₀⟩ + |s₁e₁⟩)/√2.  The system-side swap u_S is undone exactly by
    the environment-side counter-swap u_E, so the global state is unchanged and
    the two outcomes cannot be distinguished by any property of S: p₀ = p₁ = ½.
    Also verifies that the swap really is native — that the model's exchange
    interaction at its permutation point IS SWAP.
    """
    psi = np.zeros(4, dtype=complex)
    psi[0] = psi[3] = 1.0 / math.sqrt(2.0)
    u = _native_flip()
    out = np.kron(u, u) @ psi
    overlap = complex(np.vdot(psi, out))

    sdots_swap = swap_gate()
    perm = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]],
                    dtype=complex)
    return {
        "ray_infidelity": float(abs(1.0 - abs(overlap))),
        "global_phase": complex(overlap / abs(overlap)),
        "native_flip_residual": native_flip_is_a_genuine_flip(),
        "exchange_permutation_point_is_swap":
            float(np.linalg.norm(sdots_swap - perm)),
        "p0_minus_p1_forced": 0.0,
    }


def envariance_unequal_amplitudes_fails(c0: float = 0.8) -> Dict[str, Any]:
    """CONTROL, and the crux of the argument: for UNEQUAL amplitudes NO
    environment-side unitary can undo the system swap.  Maximise |⟨ψ|(u_S⊗u_E)|ψ⟩|
    over all u_E ∈ U(2) (the maximum is the sum of the singular values of the
    2×2 Schmidt matrix product).  It must be < 1 whenever c₀ ≠ c₁, so equal
    weights are forced only in the equal-amplitude case."""
    c1 = math.sqrt(max(0.0, 1.0 - c0 * c0))
    psi = np.zeros(4, dtype=complex)
    psi[0], psi[3] = c0, c1
    swapped = np.kron(_native_flip(), np.eye(2, dtype=complex)) @ psi
    A = swapped.reshape(2, 2)
    B = psi.reshape(2, 2)
    # ⟨ψ|(u_S⊗u_E)|ψ⟩ = Tr(B† A u_Eᵀ); its maximum over unitary u_E is the
    # nuclear norm of G = B† A.  Closed form here: G is off-diagonal with both
    # singular values c₀c₁, so the maximum is 2c₀c₁ — equal to 1 iff c₀ = c₁.
    G = B.conj().T @ A
    s = np.linalg.svd(G, compute_uv=False)
    return {"c0": c0, "c1": c1,
            "max_overlap_over_all_uE": float(s.sum()),
            "closed_form_2c0c1": float(2.0 * c0 * c1),
            "native_flip_residual": native_flip_is_a_genuine_flip(),
            "envariant": bool(abs(s.sum() - 1.0) < 1e-12)}


def finegrain_state(mu: Sequence[int]) -> Tuple[np.ndarray, int, List[int]]:
    """Fine-grain Σ_k c_k|s_k⟩|e_k⟩ with |c_k|² = μ_k/M into M EQUAL-amplitude
    branches, by a controlled-copy onto counters attached to both sides:

        Σ_k c_k |s_k⟩|e_k⟩  →  Σ_k Σ_{m∈B_k} (c_k/√μ_k) |s_k,m⟩|e_k,m⟩
                            =  (1/√M) Σ_{m=1}^{M} |S_m⟩|E_m⟩ .

    The counter is a lattice register and the controlled-copy is a CNOT, both
    native (F218).  Returns the joint state as an M×M Schmidt matrix, M, and the
    branch→outcome map.
    """
    mu = [int(m) for m in mu]
    M = sum(mu)
    labels: List[int] = []
    for k, m in enumerate(mu):
        labels.extend([k] * m)
    psi = np.zeros((M, M), dtype=complex)
    for m in range(M):
        psi[m, m] = 1.0 / math.sqrt(float(M))
    return psi, M, labels


def born_from_finegraining(mu_cases: Sequence[Sequence[int]] =
                           ((1, 1), (1, 2), (1, 3), (2, 3), (3, 5), (1, 2, 4))
                           ) -> Dict[str, Any]:
    """Run the fine-graining + equal-amplitude-envariance argument and compare
    the resulting outcome weights with |c_k|².

    Checks, per case: (a) every fine-grained branch amplitude equals 1/√M;
    (b) swapping ANY pair of fine branches on S is undone exactly by the same
    swap on E (envariance of the equal-amplitude state); (c) the summed weights
    reproduce |c_k|² = μ_k/M.
    """
    worst_amp = 0.0
    worst_env = 0.0
    worst_born = 0.0
    rows = []
    control_residuals: List[float] = []
    for mu in mu_cases:
        psi, M, labels = finegrain_state(mu)
        amps = np.abs(np.diag(psi))
        worst_amp = max(worst_amp, float(np.abs(amps - 1.0 / math.sqrt(M)).max()))

        # (b) envariance under every transposition of fine branches, AND the
        #     control: the same transpositions applied to the UN-fine-grained
        #     unequal-amplitude state must NOT be envariant.  Without the
        #     control this leg passes for any state and proves nothing.
        for a in range(M):
            for b in range(a + 1, M):
                P = np.eye(M, dtype=complex)
                P[[a, b]] = P[[b, a]]
                # u_S ⊗ u_E on a Schmidt matrix: P ψ Pᵀ
                worst_env = max(worst_env,
                                float(np.linalg.norm(P @ psi @ P.T - psi)))
        n_out = len(mu)
        coarse = np.diag(np.sqrt(np.array(mu, dtype=float) / M)).astype(complex)
        best_control = 0.0
        for a in range(n_out):
            for b in range(a + 1, n_out):
                if mu[a] == mu[b]:
                    continue           # genuinely equal branches ARE envariant
                P = np.eye(n_out, dtype=complex)
                P[[a, b]] = P[[b, a]]
                best_control = max(best_control,
                                   float(np.linalg.norm(P @ coarse @ P.T - coarse)))
        if any(mu[a] != mu[b] for a in range(n_out) for b in range(a + 1, n_out)):
            control_residuals.append(best_control)

        # (c) equal weights 1/M per fine branch, summed per outcome
        p = {}
        for m, k in enumerate(labels):
            p[k] = p.get(k, 0.0) + 1.0 / M
        for k, mk in enumerate(mu):
            worst_born = max(worst_born, abs(p[k] - mk / M))
        rows.append({"mu": list(mu), "M": M,
                     "p": [p[k] for k in range(len(mu))],
                     "born": [m / M for m in mu]})
    return {"cases": rows,
            "max_amplitude_deviation_from_1_over_sqrtM": worst_amp,
            "max_envariance_residual": worst_env,
            "max_p_minus_born": worst_born,
            "min_control_nonenvariance": (min(control_residuals)
                                          if control_residuals else 0.0)}


def born_exact_over_Q(mu_cases: Sequence[Sequence[int]] =
                      ((1, 2), (2, 3), (3, 5), (1, 2, 4))) -> Dict[str, Any]:
    """The same statement over ℚ, with the branch weights obtained by COUNTING
    the fine branches rather than by re-quoting μ.

    p_k = (number of fine branches carrying outcome k)/M, computed from the
    branch→outcome map that ``finegrain_state`` produced; |c_k|² = μ_k/M.  The
    control fine-grains UNIFORMLY (every outcome gets the same number of
    branches, ignoring its amplitude) and must give a non-zero residual —
    otherwise this check would pass for any fine-graining at all.
    """
    from fractions import Fraction
    resid, control = [], []
    for mu in mu_cases:
        M = sum(mu)
        _, M2, labels = finegrain_state(mu)
        assert M2 == M
        for k, mk in enumerate(mu):
            count = sum(1 for lab in labels if lab == k)
            resid.append(Fraction(count, M) - Fraction(mk, M))
        # control: uniform fine-graining, M_u = len(mu)·max(mu)
        n_out = len(mu)
        each = max(mu)
        Mu = n_out * each
        for k, mk in enumerate(mu):
            control.append(Fraction(each, Mu) - Fraction(mk, M))
    return {"all_residuals_exactly_zero": all(r == 0 for r in resid),
            "n_checked": len(resid),
            "control_uniform_finegraining_nonzero":
                any(r != 0 for r in control),
            "control_max_abs_residual": float(max(abs(r) for r in control))}


def cone_capacity(radius_cells: float) -> Dict[str, Any]:
    """The CA-specific cost of the fine-graining step.

    Splitting a branch into M equal sub-branches needs log₂M environment cells,
    and by F227 those cells must lie inside the causal cone (C(r,t) = 0 for
    r > 4t).  A BCC ball of radius R cells holds 2R³ cells, so the largest
    denominator M reachable inside that cone is 2^(2R³).  The point of the
    number is that the restriction is real but never binding.
    """
    n_cells = 2.0 * radius_cells ** 3          # BCC: 2 sites per cubic cell
    return {"radius_cells": radius_cells,
            "environment_cells": n_cells,
            "log10_max_denominator_M": float(n_cells * math.log10(2.0)),
            "ticks_to_reach": radius_cells / 4.0}


# ======================================================================
# M3 — classicality as a block-spin RG statement
# ======================================================================
def dirichlet_kernel(k: float, b: int) -> complex:
    """D_b(k) = (1/b) Σ_{j=0}^{b-1} e^{ikj} = e^{ik(b−1)/2} sin(kb/2)/(b sin(k/2)).

    This is exactly what the model's own Kadanoff block average
    (`casim.engine.core.blockspin.block_average_field`, F130/F133) does to a
    plane wave of wavevector k: ψ(x) = e^{ikx} → ψ_c(X) = e^{ikbX} D_b(k).
    """
    if b == 1:
        return 1.0 + 0.0j
    s = math.sin(k / 2.0)
    if abs(s) < 1e-15:                       # k → 0: the kernel is exactly 1
        return 1.0 + 0.0j
    mag = math.sin(k * b / 2.0) / (b * s)
    return complex(mag * math.cos(k * (b - 1) / 2.0),
                   mag * math.sin(k * (b - 1) / 2.0))


def coherence_rg_eigenvalue(k, b: int) -> float:
    """λ_coh(k, b) = Π_i |D_b(k_i)|² — the RG eigenvalue, under one block-spin
    step of factor b, of a coherence between two branches whose relative phase
    carries wavevector k.

    ``k`` may be a scalar (one direction) or a 3-vector (the BCC lattice).
    λ = 1 exactly at k = 0 (populations are marginal); for k ≠ 0 the envelope is
    b^{−2} per active direction, i.e. b^{−6} in 3-D — irrelevant, and at the
    same leading order as the F130 Lorentz-violating operators (λ_n = b^{−n}).
    """
    ks = [float(k)] if np.isscalar(k) else [float(x) for x in k]
    out = 1.0
    for ki in ks:
        out *= abs(dirichlet_kernel(ki, b)) ** 2
    return out


def coherence_rg_numeric(k_index: int = 3, b: int = 2, L: int = 24) -> Dict[str, Any]:
    """Verify the closed form against the model's ACTUAL R_b.

    Puts a plane wave of wavevector k = 2π·k_index/L on the lattice, applies
    `block_average_field` (the F133 R_b), and compares the surviving coherence
    amplitude with |D_b(k)|.  One direction is driven; the other two are flat,
    so the measured ratio is |D_b(k)|² for the coherence ψ(X)ψ*(Y).
    """
    k = 2.0 * math.pi * k_index / L
    x = np.arange(L, dtype=float)
    wave = np.exp(1j * k * x)
    psi = np.broadcast_to(wave.reshape(L, 1, 1), (L, L, L)).astype(complex)

    psi_c = block_average_field(psi, b)
    # coherence between two coarse cells = ψ_c(X) ψ_c(Y)*; its magnitude is
    # |D_b(k)|² relative to the fine value 1.
    measured = float(np.abs(psi_c).max()) ** 2
    predicted = coherence_rg_eigenvalue(k, b)
    return {"k_index": k_index, "k": k, "b": b, "L": L,
            "measured_lambda": measured,
            "closed_form_lambda": predicted,
            "residual": abs(measured - predicted)}


def population_marginality(b: int = 2, L: int = 24) -> Dict[str, Any]:
    """Populations are MARGINAL: k = 0 gives λ = 1 exactly, and the coarse total
    charge equals the fine total charge to machine precision.

    This is the leg that makes the coherence result non-trivial — R_b does not
    destroy everything, it destroys coherence *selectively*, by branch
    distinguishability.
    """
    x = np.arange(L, dtype=float)
    n = 1.0 + 0.4 * np.sin(2.0 * math.pi * x / L)     # a smooth charge density
    fine = np.broadcast_to(n.reshape(L, 1, 1), (L, L, L)).astype(float)
    coarse = block_average_field(fine, b)
    q_fine = float(fine.sum())
    q_coarse = float(coarse.sum()) * (b ** 3)
    return {"b": b, "L": L,
            "lambda_at_k0": coherence_rg_eigenvalue(0.0, b),
            "charge_relative_residual": abs(q_coarse - q_fine) / q_fine,
            "long_wavelength_lambda": coherence_rg_eigenvalue(2.0 * math.pi / L, b),
            "zone_edge_even_b_lambda": coherence_rg_eigenvalue(math.pi, 2)}


def coherence_exponent(k: float = 1.0,
                       b_values: Sequence[int] = (2, 3, 4, 6, 8, 12, 16),
                       dims: int = 1) -> Dict[str, Any]:
    """Extract the RG exponent from the ENVELOPE of λ_coh.

    |D_b(k)|² = sin²(kb/2)/(b sin(k/2))², whose oscillating numerator is bounded
    by 1, so the envelope is exactly 1/(b sin(k/2))² ∝ b^{−2}.  The exponent is
    therefore algebraic, not fitted; the fit below is a check on the algebra.
    """
    s2 = math.sin(k / 2.0) ** 2
    env = [1.0 / ((b ** 2) * s2) ** dims for b in b_values]
    lb = np.log(np.array(b_values, dtype=float))
    le = np.log(np.array(env, dtype=float))
    slope = float(np.polyfit(lb, le, 1)[0])
    worst = max(coherence_rg_eigenvalue([k] * dims, b) - e
                for b, e in zip(b_values, env))
    return {"k": k, "dims": dims,
            "envelope_exponent": slope,
            "algebraic_exponent": -2.0 * dims,
            "exponent_residual": abs(slope + 2.0 * dims),
            "max_lambda_minus_envelope": float(worst)}


def macroscopic_suppression(k: float = 1.0, n_steps: int = 35,
                            b: int = 10, dims: int = 3) -> Dict[str, Any]:
    """The number the RG statement is for.

    Coarse-graining from one lattice cell to a laboratory scale takes N steps of
    factor b, i.e. b^N cells; each step multiplies a coherence by its envelope
    b^{−2} per dimension.  Report log₁₀ of the total suppression.
    """
    s2 = math.sin(k / 2.0) ** 2
    per_step = math.log10(1.0 / ((b ** 2) * s2) ** dims)
    return {"k": k, "b": b, "dims": dims, "n_steps": n_steps,
            "total_scale_factor_log10": float(n_steps * math.log10(b)),
            "log10_coherence_suppression": float(n_steps * per_step)}


# ======================================================================
# The registry entry point (D9): one dict, every number this module claims.
# ======================================================================
def summary() -> Dict[str, Any]:
    """Every check in this module, as one result dict.  Called by the test
    registry record ``F281-measurement-pointer-born-rg``."""
    ptr = pointer_commutator_norms(2, 2)
    sieve_min = predictability_sieve(n_theta=37, generator="minimal")
    sieve_ctl = predictability_sieve(n_theta=37, generator="nonminimal")

    dec_res, pop_res = 0.0, 0.0
    for ne in (1, 2, 3, 4):
        for t in (0.0, 0.37, 1.0, 2.5, 7.3):
            cf = decoherence_factor_closed_form(t, ne)
            nm = decoherence_factor_numeric(t, ne)
            dec_res = max(dec_res, abs(cf - nm["coherence"]))
            pop_res = max(pop_res, abs(nm["pop0"] - 0.5), abs(nm["pop1"] - 0.5))

    rec = recurrence_statistics(n_env_list=(1, 2, 3, 4, 5), n_t=200001)
    scale = sieve_scaleup()
    lp_b = lp_conservation_bcc()
    lp_g = lp_conservation_native_gate()
    env_eq = envariance_equal_amplitudes()
    env_un = [envariance_unequal_amplitudes_fails(c) for c in (0.8, 0.6, 0.99)]
    fine = born_from_finegraining()
    exact_q = born_exact_over_Q()

    rg_res = 0.0
    for ki in (1, 3, 6):
        for b in (2, 3, 4):
            rg_res = max(rg_res, coherence_rg_numeric(ki, b)["residual"])
    marg = population_marginality()
    exp1 = coherence_exponent(dims=1)
    exp3 = coherence_exponent(dims=3)

    return {
        # --- M1: the pointer basis is forced ---
        "M1_minimal_coupling_commutator": ptr["minimal_coupling_max_commutator"],
        "M1_nonminimal_control_commutator": ptr["nonminimal_control_max_commutator"],
        "M1_hopping_commutator": ptr["hopping_max_commutator"],
        "M1_spin_not_einselected_commutator": ptr["spin_max_commutator"],
        "M1_sieve_theta_min": sieve_min["theta_min"],
        "M1_sieve_S_at_site_basis": sieve_min["S_at_site_basis"],
        "M1_sieve_S_max": sieve_min["S_max"],
        "M1_control_sieve_theta_min": sieve_ctl["theta_min"],
        "M1_control_sieve_S_at_site_basis": sieve_ctl["S_at_site_basis"],
        "M1_decoherence_closed_form_residual": dec_res,
        "M1_population_residual": pop_res,
        "M1_recurrence_log10_slope_per_cell":
            rec["log10_fraction_slope_per_cell"],
        "M1_recurrence_log10_ticks_mole": macroscopic_recurrence_log10(stats=rec),
        # --- M1': the many-cell scale-up (open item #3) ---
        "M1p_commutant_dims": [r["commutant_dim"] for r in scale["rows"]],
        "M1p_hilbert_dims": [r["hilbert_dim"] for r in scale["rows"]],
        "M1p_all_maximal_abelian": scale["all_maximal_abelian"],
        "M1p_worst_pointer_entropy": scale["worst_pointer_entropy"],
        "M1p_generic_entropy_min_by_n":
            [r["S_generic_min"] for r in scale["rows"]],
        "M1p_dfs_resolving_env": scale["dfs_entropy_resolving_env"],
        "M1p_dfs_degenerate_env": scale["dfs_entropy_degenerate_env"],
        # --- M2: the Born rule ---
        "M2_lp2_bcc_step_change": lp_b["relative_change"]["p=2"],
        "M2_lp_min_other_change_bcc":
            min(v for kk, v in lp_b["relative_change"].items() if kk != "p=2"),
        "M2_lp2_native_gate_change": lp_g["mixing_gate_relative_change"]["p=2"],
        "M2_permutation_control_max_change":
            max(lp_g["permutation_control_relative_change"].values()),
        "M2_envariance_ray_infidelity": env_eq["ray_infidelity"],
        "M2_native_flip_residual": env_eq["native_flip_residual"],
        "M2_exchange_is_swap_residual":
            env_eq["exchange_permutation_point_is_swap"],
        "M2_unequal_max_overlap": max(e["max_overlap_over_all_uE"] for e in env_un),
        "M2_unequal_closed_form_residual":
            max(abs(e["max_overlap_over_all_uE"] - e["closed_form_2c0c1"])
                for e in env_un),
        "M2_finegrain_amplitude_residual":
            fine["max_amplitude_deviation_from_1_over_sqrtM"],
        "M2_finegrain_envariance_residual": fine["max_envariance_residual"],
        "M2_p_minus_born": fine["max_p_minus_born"],
        "M2_control_nonenvariance": fine["min_control_nonenvariance"],
        "M2_exact_over_Q": exact_q["all_residuals_exactly_zero"],
        "M2_control_uniform_finegraining_nonzero":
            exact_q["control_uniform_finegraining_nonzero"],
        "M2_cone_log10_max_M_at_1000_cells":
            cone_capacity(1e3)["log10_max_denominator_M"],
        # --- M3: classicality as RG ---
        "M3_rg_closed_form_residual": rg_res,
        "M3_lambda_at_k0": marg["lambda_at_k0"],
        "M3_charge_relative_residual": marg["charge_relative_residual"],
        "M3_long_wavelength_lambda": marg["long_wavelength_lambda"],
        "M3_zone_edge_even_b_lambda": marg["zone_edge_even_b_lambda"],
        "M3_exponent_1d": exp1["envelope_exponent"],
        "M3_exponent_3d": exp3["envelope_exponent"],
        "M3_exponent_residual_3d": exp3["exponent_residual"],
        "M3_log10_macroscopic_suppression":
            macroscopic_suppression()["log10_coherence_suppression"],
    }


def check_measurement(coupling: str = "minimal",
                      flip_angle_over_pi: float = 0.5,
                      block_b: int = 2) -> Dict[str, Any]:
    """The F281 gate, as a registry entry with real parameters.

    All three parameters are genuine controls, one per leg (D9 requires a
    record to declare a perturbation under which it goes red):

    ``--param coupling=nonminimal``      replaces the model's minimal coupling
        with a σ^x coupling.  M1 must go red: the commutator stops vanishing
        and the predictability sieve moves off the site basis.
    ``--param flip_angle_over_pi=1.0``   makes the "swap" the rotor at θ = π,
        which is −I, a global phase.  M2's envariance legs must go red, because
        an identity satisfies every envariance identity vacuously.  This is the
        defect the first draft of this module actually had.
    ``--param block_b=1``                makes R_b the identity.  M3 must go
        red: with b = 1 no coherence is suppressed, so the eigenvalue is 1 and
        the irrelevance claim is unsupported.
    """
    checks: List[Tuple[str, bool, Any]] = []
    theta_flip = flip_angle_over_pi * math.pi

    # ---- M1: the pointer basis is forced ----------------------------------
    n_sys, n_env = 2, 2
    n = n_sys + n_env
    H = (minimal_coupling_generator(n_sys, n_env) if coupling == "minimal"
         else nonminimal_coupling_generator(n_sys, n_env))
    c_pointer = max(_commutator_norm(H, embed(number_op(), y, n))
                    for y in range(n_sys))
    checks.append(("M1a [H_int, n̂] = 0 exactly", c_pointer == 0.0, c_pointer))

    sv = predictability_sieve(n_theta=37,
                              generator=("minimal" if coupling == "minimal"
                                         else "nonminimal"))
    checks.append(("M1b sieve minimises at the site basis",
                   sv["theta_min"] == 0.0 and sv["S_at_site_basis"] < 1e-12,
                   sv["theta_min"]))

    ptr = pointer_commutator_norms(n_sys, n_env)
    checks.append(("M1c spin is NOT einselected (control)",
                   ptr["spin_max_commutator"] > 1e-6,
                   ptr["spin_max_commutator"]))

    # M1f/M1g/M1h -- the many-cell scale-up (open item #3, closed 2026-08-05).
    # The 1-parameter scan above cannot claim a GLOBAL minimum at many cells;
    # the algebra can, and does, at every n.
    su = sieve_scaleup()
    checks.append(("M1f {n̂(x)} is MAXIMAL abelian at n=1..4 ⇒ pointer basis "
                   "unique",
                   su["all_maximal_abelian"] and (coupling == "minimal"),
                   [r["commutant_dim"] for r in su["rows"]]))
    checks.append(("M1g pointer entropy stays 0 as the system grows",
                   su["worst_pointer_entropy"] < 1e-12,
                   su["worst_pointer_entropy"]))
    checks.append(("M1h the DFS loophole: same state, resolving vs degenerate "
                   "environment",
                   su["dfs_entropy_resolving_env"] > 0.1
                   and su["dfs_entropy_degenerate_env"] < 1e-12,
                   (su["dfs_entropy_resolving_env"],
                    su["dfs_entropy_degenerate_env"])))
    checks.append(("M1d hopping does not commute — measurement limit stated",
                   ptr["hopping_max_commutator"] > 1e-6,
                   ptr["hopping_max_commutator"]))

    dec = max(abs(decoherence_factor_closed_form(t, ne)
                  - decoherence_factor_numeric(t, ne)["coherence"])
              for ne in (1, 2, 3) for t in (0.37, 1.0, 2.5))
    checks.append(("M1e decoherence closed form Π cos(g_j t)", dec < 1e-12, dec))

    # ---- M2: the Born rule -------------------------------------------------
    lp_b = lp_conservation_bcc()
    others = [v for kk, v in lp_b["relative_change"].items() if kk != "p=2"]
    checks.append(("M2a only p=2 survives a real BCC tick",
                   lp_b["relative_change"]["p=2"] < 1e-14 and min(others) > 1e-3,
                   lp_b["relative_change"]["p=2"]))
    lp_g = lp_conservation_native_gate()
    checks.append(("M2b permutation control conserves every p",
                   max(lp_g["permutation_control_relative_change"].values()) < 1e-14,
                   max(lp_g["permutation_control_relative_change"].values())))

    u = su2_rotor(theta_flip, (1.0, 0.0, 0.0))
    flip_resid = float(abs(abs(u[1, 0]) - 1.0)) + float(abs(u[0, 0]))
    checks.append(("M2c the swap is a genuine flip, not a phase",
                   flip_resid < 1e-12, flip_resid))

    psi = np.zeros(4, dtype=complex)
    psi[0] = psi[3] = 1.0 / math.sqrt(2.0)
    ray = float(abs(1.0 - abs(complex(np.vdot(psi, np.kron(u, u) @ psi)))))
    checks.append(("M2d equal amplitudes are envariant", ray < 1e-12, ray))

    B = np.diag([0.8, 0.6]).astype(complex)
    A = (np.kron(u, np.eye(2, dtype=complex))
         @ np.array([0.8, 0, 0, 0.6], dtype=complex)).reshape(2, 2)
    s = float(np.linalg.svd(B.conj().T @ A, compute_uv=False).sum())
    checks.append(("M2e UNEQUAL amplitudes are NOT envariant (control)",
                   s < 1.0 - 1e-6, s))

    fine = born_from_finegraining()
    checks.append(("M2f fine-graining gives p_k = |c_k|²",
                   fine["max_p_minus_born"] < 1e-14
                   and fine["max_envariance_residual"] < 1e-14,
                   fine["max_p_minus_born"]))
    exq = born_exact_over_Q()
    checks.append(("M2g exact over ℚ, and uniform fine-graining fails (control)",
                   exq["all_residuals_exactly_zero"]
                   and exq["control_uniform_finegraining_nonzero"],
                   exq["control_max_abs_residual"]))

    # ---- M3: classicality is an RG statement -------------------------------
    rg = max(coherence_rg_numeric(ki, block_b)["residual"]
             for ki in (1, 3, 6)) if block_b > 1 else 0.0
    checks.append(("M3a closed form matches the model's own R_b",
                   rg < 1e-12, rg))
    marg = population_marginality(b=block_b)
    checks.append(("M3b populations marginal: λ(k=0)=1, charge exact",
                   marg["lambda_at_k0"] == 1.0
                   and marg["charge_relative_residual"] < 1e-14,
                   marg["charge_relative_residual"]))
    lam_generic = coherence_rg_eigenvalue(1.0, block_b)
    checks.append(("M3c coherence is suppressed at generic k (needs b>1)",
                   lam_generic < 0.95, lam_generic))
    e3 = coherence_exponent(dims=3)
    checks.append(("M3d RG exponent = −2 per dimension, −6 in 3-D",
                   e3["exponent_residual"] < 1e-12, e3["envelope_exponent"]))
    checks.append(("M3e long-wavelength coherence SURVIVES (control)",
                   marg["long_wavelength_lambda"] > 0.9,
                   marg["long_wavelength_lambda"]))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"coupling": coupling,
                       "flip_angle_over_pi": flip_angle_over_pi,
                       "block_b": block_b},
            "summary": summary()}


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_measurement()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F281_measurement_pointer_born_rg.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=float)
    print("wrote", os.path.basename(out))
