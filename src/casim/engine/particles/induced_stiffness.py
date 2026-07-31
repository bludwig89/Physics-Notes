"""
ca_induced_stiffness.py — the induced gauge-stiffness one-loop on the BCC walk
(the F138 induced-Y-kinetic-term loop; first computable piece of F141's U2).

Computes the static polarization (induced inverse-coupling density) of the
free fermion sea for two gauge channels:

  * vector channel    — ordinary U(1) Peierls phase on the walk hops; the
                        SU(2)_L Cartan bubble is (1/4)·Σ_branches of this
                        (T_3 = ±1/2 on the branch index, F34/F35/F51).
  * staggered channel — the F51 hypercharge: parity charge P = (−1)^{x+y+z},
                        gauged consistently on the two-tick (stroboscopic)
                        walk: tick 1 carries the source-site charge, tick 2
                        the target-site charge, so the composite hop
                        x → x+d+d' carries exactly P(x)·A·(d+d').

Momentum work is in lattice coordinates q_i = k_i/√3 ∈ (−π,π]³, hops on the 8
body diagonals d ∈ {±1}³ (ca_bcc conventions, Paper 1 Eq. 15).

KEY STRUCTURE (exact):
  * Hop decomposition  A(q) = Σ_d e^{i d·q} C_d   (8 harmonics only, A₀=0).
  * Parity theorem (from F51 S1, {P,W}=0):
        ω(q+Q) = π − ω(q),   n(q+Q) = −n(q)   (helicity flips),
    so the staggered partner of every mode sits at exactly opposite two-tick
    quasienergy Ω = ∓2ω mod 2π — the Y channel is stroboscopically gapless.
  * Both channels share ONE midpoint vertex V(q+q̃/2); the channel structure
    is exactly:
        δW₂_vec  = W(q+q̃)·V + V·W(q)            (anticommutator-like)
        δW₂_stag = W(q+q̃+Q)·V − V·W(q)          (commutator-like; the −1 is
                                                  e^{i d·Q} = −1 ∀ odd hops)

PERTURBATION THEORY ON THE QUASIENERGY CIRCLE:
  H₂ = i log W₂ has a branch cut at Ω = ±π; matrix elements of δH₂ across the
  cut are pathological.  The correct, cut-free object is the hermitian
  generator K = i δW₂ W₂†  (K_mn = i e^{iΩ_n} ⟨m|δW₂|n⟩), with the circle
  kernel cot(ΔΩ/2) replacing 1/ΔΩ (reduces to Hamiltonian PT for small gaps).
  Sea energy susceptibility:
      χ(q̃) = (pref/N) Σ_q Σ_{occ n → emp m} |K_mn|² · cot((Ω_m−Ω_n)/2)
  The prefactor and the brute-force factor (cos-wave: χ_bf = χ_PT/2) are
  validated numerically against dense real-space gauged operators.

SEA CONVENTIONS (the Floquet choice is physics, not bookkeeping):
  * 'one-tick' : fill the −ω band of H_eff = ω n̂·σ (project standard, F46).
                 Staggered transitions are gapped (~π−2ω) → no IR log.
  * 'two-tick' : fill Ω ∈ (−π,0] of H₂ (F51 §3: the physical fermion lives on
                 the stroboscopic lattice).  Staggered transitions gapless
                 (gap → 4ω̃ at the cones, ω̃ = min(ω, π−ω)); NOTE this sea has
                 a second Fermi boundary at the cut Ω=±π (the ω=π/2 surface)
                 whose contribution is tracked separately (`cut_frac`).

Spinor algebra is hand-rolled (no np.linalg on the 2×2 chiral structure —
chiral_core practice).  Brute-force validation uses np.linalg.eigvals on the
dense gauged W₂ (unitary; cross-validated against PT, which is linalg-free).

Author: research-assistant session, 2026-06-11.
"""

import numpy as np
import sys
import os

# The `sys.path.insert(0, dirname(__file__))` that used to sit here served a
# bare `import ca_bcc`. Roadmap C5 rewrote that to an absolute path, leaving the
# insert dead and shadowing top-level names (see the note in `element.py`).
from casim.engine.lattice import bcc as ca_bcc  # noqa: E402

Q_STAG = np.array([np.pi, np.pi, np.pi])
DIAGS = [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]


# ----------------------------------------------------------------------
# Walk in lattice coordinates q (= k/√3 of ca_bcc)
# ----------------------------------------------------------------------
def walk_unitary_q(q, sign='+'):
    """A^s(q) as a (...,2,2) array; q in lattice coords (last axis = 3)."""
    q = np.asarray(q, dtype=float)
    k = q * np.sqrt(3.0)
    ff, fg, gf, gg = ca_bcc.bcc_unitary(k[..., 0], k[..., 1], k[..., 2], sign=sign)
    out = np.empty(np.shape(ff) + (2, 2), dtype=complex)
    out[..., 0, 0], out[..., 0, 1] = ff, fg
    out[..., 1, 0], out[..., 1, 1] = gf, gg
    return out


def uvec_q(q, sign='+'):
    q = np.asarray(q, dtype=float)
    k = q * np.sqrt(3.0)
    return ca_bcc._bcc_uvec(k[..., 0], k[..., 1], k[..., 2], sign=sign)


# ----------------------------------------------------------------------
# I1 — exact 8-hop decomposition  A(q) = Σ_d e^{i d·q} C_d
# ----------------------------------------------------------------------
def hop_matrices(sign='+'):
    """
    Exact C_d (8 hop matrices, 2×2).  Every entry of A is a product of three
    single-axis trig factors, so the only harmonics are e^{i(±q1±q2±q3)};
    sampling q_i ∈ {0, π/2} (2 points per axis) inverts them exactly:
    basis (e^{+iq}, e^{−iq}) sampled at (0, π/2) → F = [[1,1],[i,−i]].
    """
    pts = [0.0, np.pi / 2]
    Finv = np.linalg.inv(np.array([[1, 1], [1j, -1j]], dtype=complex))
    S = np.empty((2, 2, 2, 2, 2), dtype=complex)
    for a, qa in enumerate(pts):
        for b, qb in enumerate(pts):
            for c, qc in enumerate(pts):
                S[a, b, c] = walk_unitary_q([qa, qb, qc], sign=sign)
    S = np.einsum('pa,abcij->pbcij', Finv, S)
    S = np.einsum('qb,pbcij->pqcij', Finv, S)
    S = np.einsum('rc,pqcij->pqrij', Finv, S)
    sgn = {1: 0, -1: 1}
    return {d: S[sgn[d[0]], sgn[d[1]], sgn[d[2]]] for d in DIAGS}


def hop_decomposition_residual(sign='+', n=200, seed=0):
    """max |A(q) − Σ_d e^{i d·q} C_d| over random q (machine-zero ⇒ exact)."""
    rng = np.random.default_rng(seed)
    C = hop_matrices(sign)
    q = rng.uniform(-np.pi, np.pi, size=(n, 3))
    A = walk_unitary_q(q, sign=sign)
    R = np.zeros((n, 2, 2), dtype=complex)
    for d, Cd in C.items():
        R += np.exp(1j * (q @ np.array(d, dtype=float)))[:, None, None] * Cd
    return float(np.max(np.abs(A - R)))


# ----------------------------------------------------------------------
# I2 — the parity theorem (exact consequence of F51 S1)
# ----------------------------------------------------------------------
def parity_theorem_residual(sign='+', n=200, seed=1):
    """ω(q+Q) = π−ω(q) and n(q+Q) = −n(q).  Returns (res_omega_u, res_n)."""
    rng = np.random.default_rng(seed)
    q = rng.uniform(-np.pi, np.pi, size=(n, 3))
    u1, nx1, ny1, nz1 = uvec_q(q, sign)
    u2, nx2, ny2, nz2 = uvec_q(q + Q_STAG, sign)
    res_u = np.max(np.abs(u2 + u1))
    res_n = max(np.max(np.abs(nx2 + nx1)), np.max(np.abs(ny2 + ny1)),
                np.max(np.abs(nz2 + nz1)))
    w1 = np.arccos(np.clip(u1, -1, 1))
    w2 = np.arccos(np.clip(u2, -1, 1))
    res_w = np.max(np.abs(w2 - (np.pi - w1)))
    return float(max(res_u, res_w)), float(res_n)


# ----------------------------------------------------------------------
# Analytic spinors of n̂·σ (hand-rolled, pole-safe two-gauge construction)
# ----------------------------------------------------------------------
def spinors(q, sign='+'):
    """Eigenvectors |±⟩ of n̂(q)·σ and ω(q).  Returns (chi_p, chi_m, omega)."""
    u, nx, ny, nz = uvec_q(q, sign)
    sn = np.sqrt(np.maximum(1.0 - u * u, 0.0))
    omega = np.arccos(np.clip(u, -1, 1))
    safe = sn > 1e-14
    nhx = np.where(safe, nx / np.where(safe, sn, 1), 0.0)
    nhy = np.where(safe, ny / np.where(safe, sn, 1), 0.0)
    nhz = np.where(safe, nz / np.where(safe, sn, 1), 1.0)
    north = nhz > -0.5
    den_a = np.sqrt(np.maximum(2.0 * (1.0 + nhz), 1e-300))
    pa = np.stack([(1.0 + nhz) / den_a, (nhx + 1j * nhy) / den_a], axis=-1)
    ma = np.stack([(-nhx + 1j * nhy) / den_a, (1.0 + nhz) / den_a], axis=-1)
    den_b = np.sqrt(np.maximum(2.0 * (1.0 - nhz), 1e-300))
    pb = np.stack([(nhx - 1j * nhy) / den_b, (1.0 - nhz) / den_b], axis=-1)
    mb = np.stack([(1.0 - nhz) / den_b, (-nhx - 1j * nhy) / den_b], axis=-1)
    w = north[..., None]
    return np.where(w, pa, mb * 0 + pb), np.where(w, ma, mb), omega


# ----------------------------------------------------------------------
# Vertices — one shared midpoint vertex; exact channel structure
# ----------------------------------------------------------------------
def vertex_one_tick(q_mid, ehat, C):
    """V(q_mid) = i Σ_d (d·ê) e^{i d·q_mid} C_d  (midpoint Peierls)."""
    out = np.zeros(np.shape(q_mid)[:-1] + (2, 2), dtype=complex)
    eh = np.asarray(ehat, dtype=float)
    for d, Cd in C.items():
        dv = np.array(d, dtype=float)
        ph = 1j * float(dv @ eh) * np.exp(1j * (np.asarray(q_mid) @ dv))
        out += ph[..., None, None] * Cd
    return out


def vertex_W2(q, qt, ehat, C, sign='+', channel='vector'):
    """
    ⟨q+q̃_eff| δW₂ |q⟩ at O(ε) for A(x) = ε e^{i q̃·x} ê (q̃_eff = q̃, or q̃+Q
    for the staggered channel).  Exact forms (see module docstring):
        vector   : W(q+q̃)·V(q+q̃/2) + V(q+q̃/2)·W(q)
        staggered: W(q+q̃+Q)·V(q+q̃/2) − V(q+q̃/2)·W(q)
    """
    q = np.asarray(q, dtype=float)
    qt = np.asarray(qt, dtype=float)
    V = vertex_one_tick(q + qt / 2.0, ehat, C)
    Wq = walk_unitary_q(q, sign)
    if channel == 'vector':
        Wp = walk_unitary_q(q + qt, sign)
        return Wp @ V + V @ Wq
    elif channel == 'staggered':
        Wp = walk_unitary_q(q + qt + Q_STAG, sign)
        return Wp @ V - V @ Wq
    raise ValueError(channel)


# ----------------------------------------------------------------------
# Band data for the two sea conventions (states are W-eigenstates in both)
# ----------------------------------------------------------------------
def bands(q, sign='+', sea='two-tick'):
    """
    Returns (chi_occ, chi_emp, Om_occ, Om_emp): occupied/empty W₂ eigenstates
    and their quasienergies Ω ∈ (−π,π] (W₂ = e^{−iH₂}).
      one-tick: occ = |−⟩ (H-eigenvalue −ω); Ω_occ = −2ω wrapped to (−π,π].
      two-tick: occ = state with Ω ∈ (−π,0]: |−⟩ if ω ≤ π/2 else |+⟩.
    """
    cp, cm, w = spinors(q, sign)
    if sea == 'one-tick':
        Om_m = _wrap(-2.0 * w)   # quasienergy of |−⟩
        Om_p = _wrap(+2.0 * w)
        return cm, cp, Om_m, Om_p
    elif sea == 'two-tick':
        lower = w <= np.pi / 2
        Om_occ = np.where(lower, -2.0 * w, 2.0 * w - 2.0 * np.pi)
        sel = lower[..., None]
        chi_occ = np.where(sel, cm, cp)
        chi_emp = np.where(sel, cp, cm)
        return chi_occ, chi_emp, Om_occ, -Om_occ
    raise ValueError(sea)


def _wrap(x):
    """Wrap to (−π, π]."""
    return -((-x + np.pi) % (2.0 * np.pi) - np.pi)


# ----------------------------------------------------------------------
# Polarization via circle perturbation theory (cut-free)
# ----------------------------------------------------------------------
def polarization(L, m_qt, ehat, qdir, channel, sea='two-tick', sign='+',
                 C=None, return_split=False):
    """
    PARAMAGNETIC bubble χ_para(q̃) per site for plane-wave transfer
    q̃ = (2π m_qt/L)·q̂dir and gauge polarization ê:

        χ = (1/N) Σ_q |K_eo|² · cot(ΔΩ/2),   ΔΩ = circle gap Ω_e ⊖ Ω_o,
        K_eo = i e^{iΩ_o} ⟨emp(q′)| δW₂ |occ(q)⟩,   q′ = q + q̃ (+Q if stag).

    The cot(Δ/2) circle kernel is the exact eigenphase PT of unitaries
    (validated to 1e-6 on random unitaries; reduces to 2/Δ Hamiltonian PT).

    SCOPE NOTE: this is the paramagnetic piece only — the diamagnetic
    (Peierls-contact, O(ε²)) term of the full response is NOT included, so
    absolute values are not gauge-complete; use `brute_force_chi` for the
    full response.  Channel COMPARISONS are unaffected: the parity mapping
    W(q+Q) = −W(q) makes both the paramagnetic and diamagnetic pieces
    channel-equal in the two-tick sea (verified by brute force).
    Half-shifted grid avoids all gapless points exactly.
    If return_split: returns (χ, χ_cut) where χ_cut collects pairs whose
    gap passes through the cut (|Ω_e − Ω_o| > π as real numbers) — the
    ω≈π/2 second-Fermi-boundary contribution of the two-tick sea.
    """
    if C is None:
        C = hop_matrices(sign)
    qdir = np.asarray(qdir, dtype=float)
    qt = (2.0 * np.pi * m_qt / L) * qdir
    g = (np.arange(L) + 0.5) * (2.0 * np.pi / L) - np.pi
    qx, qy, qz = np.meshgrid(g, g, g, indexing='ij')
    q = np.stack([qx, qy, qz], axis=-1).reshape(-1, 3)
    qp = q + qt + (Q_STAG if channel == 'staggered' else 0.0)

    chi_o, _, Om_o, _ = bands(q, sign, sea)
    _, chi_e, _, Om_e = bands(qp, sign, sea)

    dW = vertex_W2(q, qt, ehat, C, sign=sign, channel=channel)
    M = np.einsum('...i,...ij,...j->...', np.conj(chi_e), dW, chi_o)
    K = 1j * np.exp(1j * Om_o) * M           # ⟨e|K|o⟩, K = i δW₂ W₂†

    dOm_raw = Om_e - Om_o                     # in (−2π, 2π)
    dOm = _wrap(dOm_raw)                      # circle gap in (−π, π]
    # guard: exclude numerically degenerate pairs (measure-zero on shifted grid)
    ok = np.abs(dOm) > 1e-12
    kern = np.zeros_like(dOm)
    kern[ok] = 1.0 / np.tan(dOm[ok] / 2.0)
    contrib = (np.abs(K) ** 2) * kern
    through_cut = np.abs(dOm_raw) > np.pi
    chi_main = float(np.sum(contrib[~through_cut]) / q.shape[0])
    chi_cut = float(np.sum(contrib[through_cut]) / q.shape[0])
    if return_split:
        return chi_main + chi_cut, chi_cut
    return chi_main + chi_cut


# ----------------------------------------------------------------------
# Brute-force validation: dense real-space gauged W₂ on a small torus
# ----------------------------------------------------------------------
def brute_force_chi(L, m_qt, ehat, qdir, channel, sign='+', eps=1e-3,
                    sea='two-tick', twist=0.3819660112501051):
    """
    Ground truth on an L³ torus: A(x) = ε cos(q̃·x) ê, midpoint Peierls
    (parity-charged per tick for the staggered channel), dense eigenphases,
    fill by sea convention, χ = −[E(ε)+E(−ε)−2E(0)]/(ε² N).
    one-tick filling: fill the L³ states adiabatically connected to the
    −ω band — implemented as filling by the ungauged assignment is not
    possible after gauging, so one-tick brute force fills the LOWEST N
    eigenphases of the one-tick walk's H = i log W instead (equivalent at
    ε=0; adiabatic at small ε).  two-tick: fill Ω(W₂) ∈ (−π, 0].
    Keep L ≤ 8 (dense 2L³ × 2L³).  `twist` applies twisted boundary
    conditions (an irrational fraction of a flux quantum per axis): shifts
    the momentum grid by 2π·twist/L per axis so no grid mode sits exactly on
    a gapless point or on the filling boundary (Γ-cone zero modes and the
    ω=π/2 cut surface otherwise destabilise the occupancy at L ≡ 0 mod 4).
    """
    C = hop_matrices(sign)
    N = L ** 3
    qt = (2.0 * np.pi * m_qt / L) * np.asarray(qdir, dtype=float)
    eh = np.asarray(ehat, dtype=float)
    tw = 2.0 * np.pi * twist / L
    coords = np.array([(x, y, z) for x in range(L) for y in range(L) for z in range(L)])
    idx = {tuple(c): i for i, c in enumerate(coords)}
    par = (-1.0) ** coords.sum(axis=1)

    def build_W(tick, e):
        W = np.zeros((2 * N, 2 * N), dtype=complex)
        for d, Cd in C.items():
            dv = np.array(d)
            tgt = (coords + dv) % L
            a_mid = e * np.cos((coords + 0.5 * dv) @ qt) * float(np.array(d, dtype=float) @ eh)
            tw_ph = np.exp(1j * tw * float(dv.sum()))   # uncharged BC twist
            if channel == 'vector':
                ph = np.exp(1j * a_mid) * tw_ph
            else:  # staggered: tick 1 source charge P(x), tick 2 target −P(x)
                qchg = par if tick == 1 else -par
                ph = np.exp(1j * qchg * a_mid) * tw_ph
            rows = np.array([idx[tuple(t)] for t in tgt])
            for i in range(N):
                W[2 * rows[i]:2 * rows[i] + 2, 2 * i:2 * i + 2] += ph[i] * Cd
        return W

    def sea_energy(e):
        W1 = build_W(1, e)
        if sea == 'two-tick':
            lam = np.linalg.eigvals(build_W(2, e) @ W1)
            Om = -np.angle(lam / np.abs(lam))
            return float(np.sum(Om[Om <= 0.0]))
        # one-tick: quasienergies of W itself, fill lowest half (the −ω band)
        lam = np.linalg.eigvals(W1)
        th = -np.angle(lam / np.abs(lam))       # H eigenvalues in (−π,π]
        th = np.sort(th)
        return float(2.0 * np.sum(th[:N]))      # ×2: H₂ = 2H units, as in PT

    e0, ep, em = sea_energy(0.0), sea_energy(eps), sea_energy(-eps)
    return float(-(ep + em - 2.0 * e0) / (eps ** 2) / N)


def gauge_invariance_residual(L=6, sign='+', eps=0.37, sea='two-tick',
                              channel='staggered'):
    """
    Exact Ward check of the two-tick gauging.  For a PURE-GAUGE config,
    phases built from exact differences ΔΛ telescope:
        staggered: tick 1 carries P(x)·[Λ(x+d)−Λ(x)], tick 2 carries
                   P(x+d)·[Λ(x+d)−Λ(x)]  ⇒ composite = P(x)·[Λ(x'')−Λ(x)]
                   ⇒ W₂^Λ = e^{iΛ̂P̂} W₂ e^{−iΛ̂P̂}  (exact conjugation);
        vector   : ordinary e^{iΔΛ} per hop ⇒ W^Λ = e^{iΛ̂} W e^{−iΛ̂}.
    The sea energy must be invariant to round-off at FINITE eps.
    Returns |E(eps) − E(0)| / |E(0)|.
    """
    C = hop_matrices(sign)
    N = L ** 3
    coords = np.array([(x, y, z) for x in range(L) for y in range(L) for z in range(L)])
    idx = {tuple(c): i for i, c in enumerate(coords)}
    par = (-1.0) ** coords.sum(axis=1)
    lam = eps * np.cos(2.0 * np.pi * coords[:, 0] / L + 0.7) \
        * np.sin(4.0 * np.pi * coords[:, 1] / L + 0.3)

    def build_W(tick, on):
        W = np.zeros((2 * N, 2 * N), dtype=complex)
        for d, Cd in C.items():
            dv = np.array(d)
            tgt = (coords + dv) % L
            rows = np.array([idx[tuple(t)] for t in tgt])
            dlam = lam[rows] - lam  # Λ(x+d) − Λ(x), exact difference
            if not on:
                ph = np.ones(N)
            elif channel == 'staggered':
                qchg = par if tick == 1 else -par   # P(x) / P(x+d) = −P(x)
                ph = np.exp(1j * qchg * dlam)
            else:
                ph = np.exp(1j * dlam)
            for i in range(N):
                W[2 * rows[i]:2 * rows[i] + 2, 2 * i:2 * i + 2] += ph[i] * Cd
        return W

    def sea_energy(on):
        if sea == 'two-tick':
            lam_e = np.linalg.eigvals(build_W(2, on) @ build_W(1, on))
            Om = -np.angle(lam_e / np.abs(lam_e))
            return float(np.sum(Om[Om <= 0.0]))
        th = np.sort(-np.angle(np.linalg.eigvals(build_W(1, on))))
        return float(2.0 * np.sum(th[:N]))

    e0, e1 = sea_energy(False), sea_energy(True)
    return float(abs(e1 - e0) / abs(e0))


# ----------------------------------------------------------------------
# Sweeps
# ----------------------------------------------------------------------
def channel_equality_residual(L, m_qt, ehat, qdir, sign='+', C=None):
    """
    Pointwise verification of the channel-equality theorem in the two-tick
    sea: for every q on the half-shifted L³ grid,

      |⟨emp(q+q̃+Q)| δW₂_stag |occ(q)⟩| = |⟨emp(q+q̃)| δW₂_vec |occ(q)⟩|
      and the circle gaps are equal.

    (Proof sketch: W(q+Q) = −W(q) [F51 S1] gives δW₂_stag = −δW₂_vec as
    blocks; ω̃ = min(ω, π−ω) is Q-invariant so the two-tick gaps match; and
    emp(q′+Q) equals emp(q′) up to phase since n̂(q+Q) = −n̂(q) flips which
    spinor is selected exactly when the band assignment flips.)
    Returns (max |ΔM|, max |Δgap|) over the grid — machine-zero expected.
    """
    if C is None:
        C = hop_matrices(sign)
    qdir = np.asarray(qdir, dtype=float)
    qt = (2.0 * np.pi * m_qt / L) * qdir
    # irrational (golden-ratio) grid offset: kills accidental exact ties on
    # the ω = π/2 surface, where the two-tick band assignment is a
    # circle-degenerate knife edge (the cut Fermi boundary) and the
    # tie-break convention, not physics, decides the partner state.
    g = (np.arange(L) + 0.3819660112501051) * (2.0 * np.pi / L) - np.pi
    qx, qy, qz = np.meshgrid(g, g, g, indexing='ij')
    q = np.stack([qx, qy, qz], axis=-1).reshape(-1, 3)
    # mask any residual near-ties (|ω − π/2| tiny at q' or q'+Q)
    _, _, w_p = spinors(q + qt, sign)
    tie = np.abs(w_p - np.pi / 2) < 1e-9
    res_M, res_G = 0.0, 0.0
    for ch, dQ in (('vector', 0.0), ('staggered', Q_STAG)):
        qp = q + qt + dQ
        chi_o, _, Om_o, _ = bands(q, sign, 'two-tick')
        _, chi_e, _, Om_e = bands(qp, sign, 'two-tick')
        dW = vertex_W2(q, qt, ehat, C, sign=sign, channel=ch)
        M = np.abs(np.einsum('...i,...ij,...j->...', np.conj(chi_e), dW, chi_o))
        gap = _wrap(Om_e - Om_o)
        if ch == 'vector':
            M0, g0 = M, gap
        else:
            res_M = float(np.max(np.abs(M - M0)[~tie]))
            res_G = float(np.max(np.abs(gap - g0)[~tie]))
    return res_M, res_G


def chi_sweep(L, m_list, ehat, qdir, channel, sea, sign='+', C=None):
    """χ(q̃) for q̃ = (2π m/L)·q̂dir, m in m_list.  Returns (qt_mags, chis, cuts)."""
    if C is None:
        C = hop_matrices(sign)
    qts, chis, cuts = [], [], []
    for m in m_list:
        chi, cut = polarization(L, m, ehat, qdir, channel, sea=sea, sign=sign,
                                C=C, return_split=True)
        qts.append(2.0 * np.pi * m / L * float(np.linalg.norm(qdir)))
        chis.append(chi)
        cuts.append(cut)
    return np.array(qts), np.array(chis), np.array(cuts)


def log_fit(qts, chis):
    """Fit χ/q̃² = C·ln(1/q̃) + c.  Returns (C, c, max rel resid)."""
    y = chis / qts ** 2
    x = np.log(1.0 / qts)
    A = np.stack([x, np.ones_like(x)], axis=-1)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = A @ coef - y
    return float(coef[0]), float(coef[1]), float(np.max(np.abs(resid / y)))


# ======================================================================
#  MASSIVE (DIRAC) SECTOR — the condensate-proxy loop (F141 §4 / U2)
# ======================================================================
# Project Dirac convention (ca_dirac_bcc, Paper 1 Eq. 23):
#     D(q) = [[ n·A(q),  i m·I ], [ i m·I,  n·A†(q) ]],  n = √(1−m²),
# eigenphases ±ω_m, twofold each, cos ω_m = n·u(q).
#
# Exact structure (verified by checks below):
#   * Dirac parity theorem:  ω_m(q+Q) = π − ω_m(q)  (u(q+Q) = −u(q)),
#     operator form  D(q+Q) = −X D(q) X  with  X = diag(I₂, −I₂).
#   * The bipartite anticommutation generalizes:  {S, D_A} = 0 with
#     S = P̂·X̂ (sublattice parity × chiral sign), for ARBITRARY gauge
#     fields — the hop blocks are odd under P̂ and even under X̂-flip of
#     sign... combined: S flips hops via P̂ and the on-site mass via X̂.
#     This protects the λ → −λ spectral closure of the massless case.
#   * What the mass CAN break is the second closure (θ → π−θ) that made
#     the one-tick sea rigid — measured, not assumed, by the checks.

def dirac_matrix_q(q, m, sign='+'):
    """D(q) as (...,4,4): [[n·A, im],[im, n·A†]] (ca_dirac_bcc convention)."""
    A = walk_unitary_q(q, sign)
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    sh = A.shape[:-2]
    D = np.zeros(sh + (4, 4), dtype=complex)
    D[..., :2, :2] = n * A
    D[..., 2:, 2:] = n * np.conj(np.swapaxes(A, -1, -2))
    D[..., 0, 2] = D[..., 1, 3] = 1j * m
    D[..., 2, 0] = D[..., 3, 1] = 1j * m
    return D


def dirac_parity_residuals(m, sign='+', n_pts=200, seed=2):
    """
    Exact Dirac parity theorem: ω_m(q+Q) = π−ω_m(q) and the operator
    identity D(q+Q) = −X D(q) X, X = diag(I,−I).  Returns (res_disp, res_op).
    """
    rng = np.random.default_rng(seed)
    q = rng.uniform(-np.pi, np.pi, size=(n_pts, 3))
    n = float(np.sqrt(1.0 - m * m))
    u1, *_ = uvec_q(q, sign)
    u2, *_ = uvec_q(q + Q_STAG, sign)
    w1 = np.arccos(np.clip(n * u1, -1, 1))
    w2 = np.arccos(np.clip(n * u2, -1, 1))
    res_disp = float(np.max(np.abs(w2 - (np.pi - w1))))
    X = np.diag([1.0, 1.0, -1.0, -1.0]).astype(complex)
    D1 = dirac_matrix_q(q, m, sign)
    D2 = dirac_matrix_q(q + Q_STAG, m, sign)
    res_op = float(np.max(np.abs(D2 + X @ D1 @ X)))
    return res_disp, res_op


def _dirac_vertex4(q_mid, ehat, C, m):
    """
    O(ε) hop vertex of the gauged Dirac walk, midpoint Peierls.  Only the
    hop blocks respond (the mass is on-site, zero displacement):
        V₄ = diag( n·V_A(q_mid),  n·V_A†(q_mid) ),
    with V_A = i Σ_d (d·ê) e^{i d·q_mid} C_d and the A†-block hop content
    A†(q) = Σ_d e^{i d·q} C_{−d}†  ⇒  V_A† = i Σ_d (d·ê) e^{i d·q_mid} C_{−d}†.
    """
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    sh = np.shape(q_mid)[:-1]
    Va = np.zeros(sh + (2, 2), dtype=complex)
    Vb = np.zeros(sh + (2, 2), dtype=complex)
    eh = np.asarray(ehat, dtype=float)
    for d, Cd in C.items():
        dv = np.array(d, dtype=float)
        ph = 1j * float(dv @ eh) * np.exp(1j * (np.asarray(q_mid) @ dv))
        Va += ph[..., None, None] * Cd
        Cmd = C[(-d[0], -d[1], -d[2])]
        Vb += ph[..., None, None] * np.conj(np.swapaxes(Cmd, -1, -2))
    V4 = np.zeros(sh + (4, 4), dtype=complex)
    V4[..., :2, :2] = n * Va
    V4[..., 2:, 2:] = n * Vb
    return V4


def dirac_vertex_W2(q, qt, ehat, C, m, sign='+', channel='vector'):
    """⟨q+q̃(+Q)| δD₂ |q⟩: same channel structure as the Weyl case —
    vec: D(q+q̃)V₄ + V₄D(q);  stag: D(q+q̃+Q)V₄ − V₄D(q)."""
    q = np.asarray(q, dtype=float)
    qt = np.asarray(qt, dtype=float)
    V4 = _dirac_vertex4(q + qt / 2.0, ehat, C, m)
    Dq = dirac_matrix_q(q, m, sign)
    if channel == 'vector':
        return dirac_matrix_q(q + qt, m, sign) @ V4 + V4 @ Dq
    elif channel == 'staggered':
        return dirac_matrix_q(q + qt + Q_STAG, m, sign) @ V4 - V4 @ Dq
    raise ValueError(channel)


def dirac_bands(q, m, sign='+'):
    """
    Two-tick band data of D(q) via batched eigendecomposition (validated:
    eigenphases must equal ±arccos(n·u) to machine precision — the
    analytic-dispersion cross-check guards the numpy eig per CLAUDE.md).
    Returns (P_occ, P_emp, Om_occ, Om_emp): projectors onto the twofold
    occupied/empty D² subspaces (Ω = wrap(2θ) ∈ (−π,0] occupied) and their
    quasienergies.
    """
    D = dirac_matrix_q(q, m, sign)
    lam, V = np.linalg.eig(D)
    lam = lam / np.abs(lam)
    th = -np.angle(lam)                       # D = e^{−iθ}
    Om = _wrap(2.0 * th)
    occ = Om <= 0.0
    # orthonormalize eigenvector pairs via projector construction
    sh = D.shape[:-2]
    P_occ = np.zeros_like(D)
    P_emp = np.zeros_like(D)
    Om_o = np.where(occ, Om, 0.0).sum(axis=-1) / 2.0
    Om_e = np.where(~occ, Om, 0.0).sum(axis=-1) / 2.0
    # projector: V·diag(mask)·V^{-1} (D normal ⇒ V unitary up to roundoff)
    Vinv = np.linalg.inv(V)
    P_occ = np.einsum('...ik,...k,...kj->...ij', V, occ.astype(complex), Vinv)
    P_emp = np.einsum('...ik,...k,...kj->...ij', V, (~occ).astype(complex), Vinv)
    # validation payload: max |θ| vs analytic arccos(n·u)
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    u, *_ = uvec_q(q, sign)
    w_an = np.arccos(np.clip(n * u, -1, 1))
    # all four single-tick |θ| equal ω_m = arccos(n·u) (±ω, twofold each)
    disp_resid = float(np.max(np.abs(np.abs(th) - w_an[..., None])))
    return P_occ, P_emp, Om_o, Om_e, disp_resid


def dirac_channel_compare(L, m_qt, ehat, qdir, m, sign='+', C=None):
    """
    Pointwise channel comparison for the MASSIVE walk in the two-tick sea.
    Per grid q: T_ch = Tr[P_emp(q') δD₂ P_occ(q) δD₂†] (basis-invariant
    subspace-summed |M|²) and the circle gap.  Returns
    (max |T_stag − T_vec| / max T_vec, max |Δgap|, max dispersion-eig resid).
    """
    if C is None:
        C = hop_matrices(sign)
    qdir = np.asarray(qdir, dtype=float)
    qt = (2.0 * np.pi * m_qt / L) * qdir
    g = (np.arange(L) + 0.3819660112501051) * (2.0 * np.pi / L) - np.pi
    qx, qy, qz = np.meshgrid(g, g, g, indexing='ij')
    q = np.stack([qx, qy, qz], axis=-1).reshape(-1, 3)
    out = {}
    dres = 0.0
    for ch, dQ in (('vector', None), ('staggered', Q_STAG)):
        qp = q + qt + (dQ if dQ is not None else 0.0)
        Po, _, Oo, _, r1 = dirac_bands(q, m, sign)
        _, Pe, _, Oe, r2 = dirac_bands(qp, m, sign)
        dres = max(dres, r1, r2)
        dW = dirac_vertex_W2(q, qt, ehat, C, m, sign=sign, channel=ch)
        Mop = Pe @ dW @ Po
        T = np.einsum('...ij,...ij->...', Mop, np.conj(Mop)).real
        out[ch] = (T, _wrap(Oe - Oo))
    Tv, gv = out['vector']
    Ts, gs = out['staggered']
    # mask cut-knife-edge ties as in the Weyl case
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    u_p, *_ = uvec_q(q + qt, sign)
    tie = np.abs(np.arccos(np.clip(n * u_p, -1, 1)) - np.pi / 2) < 1e-9
    rel = float(np.max(np.abs(Ts - Tv)[~tie]) / np.max(np.abs(Tv)))
    gres = float(np.max(np.abs(gs - gv)[~tie]))
    return rel, gres, dres


def dirac_brute_force_chi(L, m_qt, ehat, qdir, channel, m, sign='+',
                          eps=1e-3, sea='two-tick',
                          twist=0.3819660112501051):
    """
    Dense real-space gauged Dirac walk on the L³ torus: 4 components/site.
    η-block hops C_d at +d; χ-block hops C_{−d}† at +d (the A† content);
    on-site mass i m (η↔χ); kinetic blocks scaled by n.  Peierls phases on
    hops only, per channel as in the Weyl case; uncharged BC twist.
    χ = −[E(ε)+E(−ε)−2E(0)]/(ε²N) with the sea convention's filling.
    """
    C = hop_matrices(sign)
    N = L ** 3
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    qt = (2.0 * np.pi * m_qt / L) * np.asarray(qdir, dtype=float)
    eh = np.asarray(ehat, dtype=float)
    tw = 2.0 * np.pi * twist / L
    coords = np.array([(x, y, z) for x in range(L) for y in range(L) for z in range(L)])
    idx = {tuple(c): i for i, c in enumerate(coords)}
    par = (-1.0) ** coords.sum(axis=1)

    def build_D(tick, e):
        D = np.zeros((4 * N, 4 * N), dtype=complex)
        for i in range(N):                       # on-site mass block
            D[4 * i + 0, 4 * i + 2] = 1j * m
            D[4 * i + 1, 4 * i + 3] = 1j * m
            D[4 * i + 2, 4 * i + 0] = 1j * m
            D[4 * i + 3, 4 * i + 1] = 1j * m
        for d, Cd in C.items():
            dv = np.array(d)
            Cmd_dag = np.conj(C[(-d[0], -d[1], -d[2])].T)
            tgt = (coords + dv) % L
            a_mid = e * np.cos((coords + 0.5 * dv) @ qt) * float(np.array(d, dtype=float) @ eh)
            tw_ph = np.exp(1j * tw * float(dv.sum()))
            if channel == 'vector':
                ph = np.exp(1j * a_mid) * tw_ph
            else:
                qchg = par if tick == 1 else -par
                ph = np.exp(1j * qchg * a_mid) * tw_ph
            rows = np.array([idx[tuple(t)] for t in tgt])
            for i in range(N):
                r, c = 4 * rows[i], 4 * i
                D[r:r + 2, c:c + 2] += n * ph[i] * Cd
                D[r + 2:r + 4, c + 2:c + 4] += n * ph[i] * Cmd_dag
        return D

    def sea_energy(e):
        if sea == 'two-tick':
            lam = np.linalg.eigvals(build_D(2, e) @ build_D(1, e))
            Om = -np.angle(lam / np.abs(lam))
            return float(np.sum(Om[Om <= 0.0]))
        th = np.sort(-np.angle(np.linalg.eigvals(build_D(1, e))))
        return float(2.0 * np.sum(th[:2 * N]))   # fill the 2N-fold −ω sea

    e0, ep, em = sea_energy(0.0), sea_energy(eps), sea_energy(-eps)
    return float(-(ep + em - 2.0 * e0) / (eps ** 2) / N)


def dirac_S_anticommutation(L=4, m=0.4, eps_field=0.3, sign='+'):
    """
    {S, D_A} = 0 with S = P̂·X̂ (parity × diag(I,−I)) for a GAUGED massive
    walk — the generalized bipartite closure.  Returns max |S D_A S + D_A|.
    """
    C = hop_matrices(sign)
    N = L ** 3
    n = float(np.sqrt(1.0 - m * m))
    coords = np.array([(x, y, z) for x in range(L) for y in range(L) for z in range(L)])
    idx = {tuple(c): i for i, c in enumerate(coords)}
    par = (-1.0) ** coords.sum(axis=1)
    qt = (2.0 * np.pi / L) * np.array([1.0, 0, 0])
    D = np.zeros((4 * N, 4 * N), dtype=complex)
    for i in range(N):
        for (a, b) in ((0, 2), (1, 3), (2, 0), (3, 1)):
            D[4 * i + a, 4 * i + b] = 1j * m
    for d, Cd in C.items():
        dv = np.array(d)
        Cmd_dag = np.conj(C[(-d[0], -d[1], -d[2])].T)
        tgt = (coords + dv) % L
        a_mid = eps_field * np.cos((coords + 0.5 * dv) @ qt) * float(dv @ np.array([0, 1.0, 0]))
        rows = np.array([idx[tuple(t)] for t in tgt])
        for i in range(N):
            r, c = 4 * rows[i], 4 * i
            ph = np.exp(1j * a_mid[i])
            D[r:r + 2, c:c + 2] += n * ph * Cd
            D[r + 2:r + 4, c + 2:c + 4] += n * ph * Cmd_dag
    S = np.zeros((4 * N, 4 * N), dtype=complex)
    for i in range(N):
        S[4 * i + 0, 4 * i + 0] = par[i]
        S[4 * i + 1, 4 * i + 1] = par[i]
        S[4 * i + 2, 4 * i + 2] = -par[i]
        S[4 * i + 3, 4 * i + 3] = -par[i]
    return float(np.max(np.abs(S @ D @ S + D)))


# ======================================================================
#  DIAMAGNETIC (Peierls-contact) SECTOR — F153
# ======================================================================
# The momentum-space PT above is paramagnetic-only.  The O(ε²) transfer-0
# (diamagnetic / seagull) operator of the two-tick Dirac walk for a real
# cos-wave field A(x)=ε cos(q̃·x) ê closes the response.  Two pieces:
#   * per-tick contact (DC of cos² = ½):  G₄(q)=diag(n G_A, n G_A†),
#       G_A(q)=−¼ Σ_d (ê·d)² e^{i d·q} C_d  (and C_{−d}† for the χ block);
#   * tick1×tick2 cross at transfer 0 (±q̃ pairing):
#       ¼ [ V₄(q+q̃/2)² + V₄(q−q̃/2)² ].
# Full transfer-0 second-order operator:
#       δ²D₂ = D(q)G₄ + G₄ D(q) + ¼[V₄(q+q̃/2)² + V₄(q−q̃/2)²].
# Verified vs the dense gauged D₂ transfer-0 block to 8×10⁻⁸ (F153 D1).
#
# CHARGE-BLIND (F153 D2, exact 1×10⁻¹⁰): for the staggered channel the parity
# charges square to 1 (P²=1) so the per-tick contact is unchanged, and the
# cross term's two extra sign flips (−P on tick2, and V₄(·+Q)=−V₄ from
# e^{i d·Q}=−1) cancel — so δ²D₂ is IDENTICAL in the vector and staggered
# channels.  Consequence: the channel splitting χ_stag−χ_vec is purely
# PARAMAGNETIC; the seagull cancels in the difference.  (This resolves the
# F149 N6/N7 sign puzzle: full = paramagnetic-split + a large shared
# charge-blind contact that flips which channel looks "enhanced" in absolute
# value with L/q̃.)

def dirac_seagull4(q, ehat, C, m, sign='+'):
    """Per-tick diamagnetic transfer-0 operator G₄(q) (DC of cos² = ½)."""
    n = float(np.sqrt(max(0.0, 1.0 - m * m)))
    sh = np.shape(q)[:-1]
    Ga = np.zeros(sh + (2, 2), dtype=complex)
    Gb = np.zeros(sh + (2, 2), dtype=complex)
    eh = np.asarray(ehat, dtype=float)
    for d, Cd in C.items():
        dv = np.array(d, dtype=float)
        coef = -0.25 * (dv @ eh) ** 2 * np.exp(1j * (np.asarray(q) @ dv))
        Ga += coef[..., None, None] * Cd
        Cmd = C[(-d[0], -d[1], -d[2])]
        Gb += coef[..., None, None] * np.conj(np.swapaxes(Cmd, -1, -2))
    G4 = np.zeros(sh + (4, 4), dtype=complex)
    G4[..., :2, :2] = n * Ga
    G4[..., 2:, 2:] = n * Gb
    return G4


def dirac_d2_transfer0(q, qt, ehat, C, m, sign='+'):
    """Charge-blind O(ε²) transfer-0 (diamagnetic) Dirac operator δ²D₂.
    Identical for the vector and staggered channels (parity charges square
    to 1).  Validated vs the dense gauged D₂ transfer-0 block (F153 D1)."""
    D = dirac_matrix_q(q, m, sign)
    G4 = dirac_seagull4(q, ehat, C, m, sign)
    Vp = _dirac_vertex4(q + qt / 2.0, ehat, C, m)
    Vm = _dirac_vertex4(q - qt / 2.0, ehat, C, m)
    return D @ G4 + G4 @ D + 0.25 * (Vp @ Vp + Vm @ Vm)


def dirac_chi_diamagnetic(L, m_qt, ehat, qdir, m, sign='+', C=None,
                          twist=0.3819660112501051):
    """Diamagnetic (first-order eigenphase) contribution to the sea-energy
    response, per site, summed over the filled set:
        Σ_q Re[ i e^{iΩ_occ} Tr(P_occ δ²D₂) ] / N_q .
    Channel-blind (no channel argument) — δ²D₂ is the same operator for both
    channels (F153 D2).  Golden-offset grid avoids the ω=π/2 cut ties."""
    if C is None:
        C = hop_matrices(sign)
    qdir = np.asarray(qdir, dtype=float)
    qt = (2.0 * np.pi * m_qt / L) * qdir
    g = (np.arange(L) + twist) * (2.0 * np.pi / L) - np.pi
    qx, qy, qz = np.meshgrid(g, g, g, indexing='ij')
    q = np.stack([qx, qy, qz], axis=-1).reshape(-1, 3)
    P_occ, _, Om_o, _, _ = dirac_bands(q, m, sign)
    G = dirac_d2_transfer0(q, qt, ehat, C, m, sign)
    tr = np.einsum('...ij,...ji->...', P_occ, G)
    return float(np.sum((1j * np.exp(1j * Om_o) * tr).real) / q.shape[0])
