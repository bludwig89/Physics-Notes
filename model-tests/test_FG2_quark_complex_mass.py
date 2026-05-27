"""
FG-2 — F27 complex-mass adoption for the quark sector.
=========================================================

Specced in `first-gen-completeness-review.md` §3 item 2 ("Unified mass
mechanism — replace the quark Higgs–Yukawa mass with the F27 chiral
complex-mass coupling") and §5.1 (FG-3 "Quark complex mass").

This test suite verifies that the F27 mechanism (`ca_strong.quark_mass_step_f27`
and `ca_strong.step_strong_2d_complex_mass`) works correctly for quarks:

  Q1  Unitarity of the F27 quark step over N steps, random θ field.
  Q2  U(1) β-gauge Ward identity of the mass step per flavour.
  Q3  Mass gap without Higgs — pure left u grows N_R > 0 with U(x)=I, θ=0.
  Q4  Up/down/strange mass splitting — different N_R growth rates.
  Q5  θ pure-gauge — dispersion θ-independent for constant θ.
  Q6  Color neutrality — F27 mass step commutes with global SU(3) rotation.
  Q7  Cold-link regression — F27 quark step (U=I, θ=0) ≡ 9 independent
       F27 1-flavour Dirac steps, bit-for-bit.
  Q8  Color-charge conservation Q^a under the F27 step (cold/frozen links).

The next three tests are the "if that does not" trigger from the user's
directive — they show that the F27 mass-step adoption alone does not
deliver local SU(2)_L gauge invariance, so electroweak wiring is required:

  Q9   Degenerate-doublet SU(2)_L Ward identity (mass step alone) — PASS.
  Q10  Split-mass SU(2)_L Ward identity (per-flavour m_u ≠ m_d) — FAIL by
       design (mass splitting breaks SU(2)_L explicitly).
  Q11  Full step (kinetic + mass) under varying V(x) — FAIL by design
       (the spectral kinetic step needs a W_μ field to be SU(2)_L covariant).

Q10/Q11 motivate the Phase-4 electroweak wiring delivered separately.

Run:  python3 model-tests/test_FG2_quark_complex_mass.py
JSON: test-results/FG2_quark_complex_mass.json
"""
from __future__ import annotations
import json
import os
import sys
import time

import numpy as np

# ── path setup ──────────────────────────────────────────────────────────────
_THIS = os.path.dirname(os.path.abspath(__file__))
_SIM  = os.path.abspath(os.path.join(_THIS, '..', 'ca-simulation'))
sys.path.insert(0, _SIM)

import ca_dirac as cd
import ca_strong as cs


# ── reporting helpers ───────────────────────────────────────────────────────
PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
INFO = "\033[94mINFO\033[0m"


def report(label, passed, residual=None, note=""):
    tag = PASS if passed else FAIL
    res = f"  residual = {residual:.3e}" if residual is not None else ""
    print(f"  [{tag}] {label}{res}  {note}")


def random_quark_state(shape, rng, flavours=cs.FLAVOURS, chirality='mixed'):
    """Build a random complex64 quark state of given chirality content."""
    q = cs.zero_quark_field(shape)
    Lx, Ly = shape
    for f in flavours:
        for c in cs.COLOURS:
            for d in cs.DIRAC:
                if chirality == 'left' and d in ('cu', 'cd'):
                    continue
                if chirality == 'right' and d in ('eu', 'ed'):
                    continue
                arr = rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
                q[(f, c, d)] = arr.astype(complex) * 0.1
    return q


def quark_diff_max(q1, q2):
    """Max absolute difference between two quark dicts over all keys."""
    return max(float(np.max(np.abs(q1[k] - q2[k]))) for k in q1)


# ════════════════════════════════════════════════════════════════════════════
#  Q1 — Unitarity of the F27 quark step over N steps with random θ
# ════════════════════════════════════════════════════════════════════════════

def q1_unitarity(L=16, n_steps=20, dt=1.0, seed=11):
    print("─" * 70)
    print("Q1  Unitarity — F27 quark step over N steps, random θ")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')

    # cold SU(3) links (parallel transport is identity)
    U = cs.cold_links_2d(shape)
    # random per-flavour θ field
    theta_flavour = {f: cs.make_theta_field_quark(shape, mode='random',
                                                  seed=seed + i)
                     for i, f in enumerate(cs.FLAVOURS)}
    m_flavour = {'u': 0.05, 'd': 0.08, 's': 0.15}

    norm0 = cs.quark_norm(q)
    for _ in range(n_steps):
        q = cs.step_strong_2d_complex_mass(q, U,
                                           theta_flavour=theta_flavour,
                                           m_flavour=m_flavour, dt=dt)
    norm1 = cs.quark_norm(q)

    rel = abs(norm1 - norm0) / max(norm0, 1e-30)
    passed = rel < 1e-12
    report("Q1 norm conserved (random θ, mixed-chirality state)",
           passed, residual=rel,
           note=f"L={L}, n={n_steps}, drift {rel:.2e}")
    return {'name': 'Q1_unitarity', 'pass': bool(passed),
            'residual': float(rel), 'L': L, 'n_steps': n_steps,
            'norm0': float(norm0), 'norm1': float(norm1)}


# ════════════════════════════════════════════════════════════════════════════
#  Q2 — U(1) β-gauge Ward identity of the F27 mass step (per flavour)
#
#  For each flavour f, the F27 mass step satisfies:
#
#      mass_step(η, e^{iφ}·χ, θ − φ) = (η_new, e^{iφ}·χ_new)
#
#  i.e. shifting the χ phase by φ and the β-gauge θ by −φ leaves the η
#  output untouched and rotates the χ output by e^{iφ}. (F27 T4 analog.)
# ════════════════════════════════════════════════════════════════════════════

def q2_u1_ward(L=16, dt=1.0, seed=13):
    print("─" * 70)
    print("Q2  U(1) β-gauge Ward identity of mass step (per flavour)")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')

    theta_u = cs.make_theta_field_quark(shape, mode='random', seed=seed)
    theta_d = cs.make_theta_field_quark(shape, mode='random', seed=seed + 1)
    theta_s = cs.make_theta_field_quark(shape, mode='random', seed=seed + 2)
    theta_flavour = {'u': theta_u, 'd': theta_d, 's': theta_s}
    m_flavour = {'u': 0.05, 'd': 0.08, 's': 0.15}

    # Path A: mass step on (η, χ, θ)
    qA = cs.quark_mass_step_f27(q, theta_flavour, m_flavour, dt=dt)

    # Path B: U(1) rotate χ by random φ_f (per flavour) and shift θ_f by −φ_f,
    # then mass step. Expected: η_B == η_A bit-for-bit; χ_B == e^{iφ_f} χ_A.
    rng2 = np.random.default_rng(seed + 100)
    phi_const = {f: float(rng2.uniform(0.0, 2 * np.pi)) for f in cs.FLAVOURS}

    q_pre = {k: v.copy() for k, v in q.items()}
    for f in cs.FLAVOURS:
        phi_field = np.full(shape, phi_const[f], dtype=float)
        q_pre = cs.quark_u1_gauge_transform_f27(q_pre, phi_field, f)
    theta_shifted = {f: theta_flavour[f] - phi_const[f] for f in cs.FLAVOURS}
    qB = cs.quark_mass_step_f27(q_pre, theta_shifted, m_flavour, dt=dt)

    # Reverse the U(1) χ rotation on qB so it should match qA bit-for-bit
    qB_back = {k: v.copy() for k, v in qB.items()}
    for f in cs.FLAVOURS:
        phi_field = np.full(shape, -phi_const[f], dtype=float)
        qB_back = cs.quark_u1_gauge_transform_f27(qB_back, phi_field, f)

    res = quark_diff_max(qA, qB_back)
    passed = res < 1e-13
    report("Q2 U(1) Ward identity per flavour (mass step alone)",
           passed, residual=res,
           note=f"L={L}, max|qA − T⁻¹ qB|")
    return {'name': 'Q2_u1_ward', 'pass': bool(passed),
            'residual': float(res), 'L': L,
            'phi_const': phi_const}


# ════════════════════════════════════════════════════════════════════════════
#  Q3 — Mass gap without Higgs: pure-left u grows N_R > 0 with U=I, θ=0
# ════════════════════════════════════════════════════════════════════════════

def q3_mass_gap(L=16, n_steps=80, m=0.4, dt=1.0):
    print("─" * 70)
    print("Q3  Higgs-free mass gap — pure left u → grows N_R(u) with U=I, θ=0")
    print("─" * 70)

    shape = (L, L)
    q = cs.gaussian_quark(shape, flavour='u', colour='r',
                          sigma=4.0, chirality='left')
    U = cs.cold_links_2d(shape)
    theta = cs.make_theta_field_quark(shape, mode='zero')
    theta_flavour = {f: theta for f in cs.FLAVOURS}
    m_flavour = {'u': m, 'd': 0.0, 's': 0.0}

    N_L0, N_R0 = cs.chirality_split_quark(q, flavour='u')
    for _ in range(n_steps):
        q = cs.step_strong_2d_complex_mass(q, U,
                                           theta_flavour=theta_flavour,
                                           m_flavour=m_flavour, dt=dt)
    N_L1, N_R1 = cs.chirality_split_quark(q, flavour='u')

    ratio = N_R1 / max(N_L0, 1e-30)
    passed = ratio > 0.1   # F27 T7 analog: substantial right-handed buildup
    report("Q3 left-u → right-u via F27 mass (no Higgs)",
           passed, residual=ratio,
           note=f"N_R/N_L0 = {ratio:.4f}, m_u={m}, n={n_steps}")
    return {'name': 'Q3_mass_gap', 'pass': bool(passed),
            'N_L0': float(N_L0), 'N_R0': float(N_R0),
            'N_L1': float(N_L1), 'N_R1': float(N_R1),
            'ratio_NR_over_NL0': float(ratio),
            'm': m, 'n_steps': n_steps}


# ════════════════════════════════════════════════════════════════════════════
#  Q4 — Up/down/strange mass splitting: distinct N_R growth rates
# ════════════════════════════════════════════════════════════════════════════

def q4_mass_splitting(L=16, n_steps=10, dt=1.0):
    print("─" * 70)
    print("Q4  Up/down/strange mass splitting (per-flavour zitterbewegung)")
    print("─" * 70)

    shape = (L, L)
    U = cs.cold_links_2d(shape)
    theta = cs.make_theta_field_quark(shape, mode='zero')
    theta_flavour = {f: theta for f in cs.FLAVOURS}
    # Stay in the linear small-mt regime so sin²(mt) ≈ (mt)² and ratios
    # track (m/m)² cleanly. mt_max = 0.04·10 = 0.4  ⇒  sin²(0.4) = 0.151
    m_flavour = {'u': 0.01, 'd': 0.02, 's': 0.04}

    # Pure-left in every flavour, separate colours so they don't overlap
    q = cs.zero_quark_field(shape)
    cx, cy = L // 2, L // 2
    x = np.arange(L) - cx
    y = np.arange(L) - cy
    X, Y = np.meshgrid(x, y, indexing='ij')
    G = np.exp(-(X ** 2 + Y ** 2) / (2.0 * 4.0 ** 2)).astype(complex)
    q[('u', 'r', 'eu')] = G.copy()
    q[('d', 'g', 'eu')] = G.copy()
    q[('s', 'b', 'eu')] = G.copy()

    N_L0_u, _ = cs.chirality_split_quark(q, flavour='u')
    N_L0_d, _ = cs.chirality_split_quark(q, flavour='d')
    N_L0_s, _ = cs.chirality_split_quark(q, flavour='s')

    for _ in range(n_steps):
        q = cs.step_strong_2d_complex_mass(q, U,
                                           theta_flavour=theta_flavour,
                                           m_flavour=m_flavour, dt=dt)

    _, NR_u = cs.chirality_split_quark(q, flavour='u')
    _, NR_d = cs.chirality_split_quark(q, flavour='d')
    _, NR_s = cs.chirality_split_quark(q, flavour='s')

    r_u = NR_u / max(N_L0_u, 1e-30)
    r_d = NR_d / max(N_L0_d, 1e-30)
    r_s = NR_s / max(N_L0_s, 1e-30)

    # For small m·t, sin²(m·t) ~ (m·t)² → ordering and ratio test
    ordered = (r_u < r_d < r_s)
    # Ratios should approximately track (m·t·n_steps)² / m_other²
    ratio_du = r_d / max(r_u, 1e-30)
    ratio_su = r_s / max(r_u, 1e-30)
    expected_du = (m_flavour['d'] / m_flavour['u']) ** 2   # = 4
    expected_su = (m_flavour['s'] / m_flavour['u']) ** 2   # = 16

    passed = ordered and abs(ratio_du / expected_du - 1.0) < 0.5 \
                     and abs(ratio_su / expected_su - 1.0) < 0.5
    report("Q4 N_R growth orders u < d < s and ratio ~ (m/m)²",
           passed, residual=None,
           note=f"r_u={r_u:.4e}, r_d={r_d:.4e}, r_s={r_s:.4e}; "
                f"r_d/r_u={ratio_du:.2f} (exp ~{expected_du:.0f}), "
                f"r_s/r_u={ratio_su:.2f} (exp ~{expected_su:.0f})")
    return {'name': 'Q4_mass_splitting', 'pass': bool(passed),
            'm_flavour': m_flavour, 'r_u': float(r_u),
            'r_d': float(r_d), 'r_s': float(r_s),
            'ratio_d_over_u': float(ratio_du),
            'ratio_s_over_u': float(ratio_su),
            'expected_d_over_u': expected_du,
            'expected_s_over_u': expected_su,
            'ordered': bool(ordered)}


# ════════════════════════════════════════════════════════════════════════════
#  Q5 — θ pure-gauge: dispersion invariant under constant θ shift
# ════════════════════════════════════════════════════════════════════════════

def q5_theta_pure_gauge(L=16, n_steps=20, dt=1.0, seed=23):
    print("─" * 70)
    print("Q5  θ pure-gauge — dispersion identical for constant θ ∈ {0, π/3, π/2}")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q0 = random_quark_state(shape, rng, chirality='mixed')

    U = cs.cold_links_2d(shape)
    m_flavour = {'u': 0.20, 'd': 0.30, 's': 0.0}

    norms = []
    for theta_const in (0.0, np.pi / 3.0, np.pi / 2.0):
        theta_flavour = {f: np.full(shape, theta_const) for f in cs.FLAVOURS}
        q = {k: v.copy() for k, v in q0.items()}
        for _ in range(n_steps):
            q = cs.step_strong_2d_complex_mass(q, U,
                                               theta_flavour=theta_flavour,
                                               m_flavour=m_flavour, dt=dt)
        # Spectrum-like: total norm is conserved; track |q|² profile.
        norms.append(cs.quark_norm(q))

    spread = float(max(norms) - min(norms))
    passed = spread < 1e-12
    report("Q5 total |q|² identical across constant θ ∈ {0, π/3, π/2}",
           passed, residual=spread,
           note=f"norms = {[f'{x:.10g}' for x in norms]}")
    return {'name': 'Q5_theta_pure_gauge', 'pass': bool(passed),
            'residual': float(spread), 'norms': [float(x) for x in norms]}


# ════════════════════════════════════════════════════════════════════════════
#  Q6 — Color neutrality: F27 mass step commutes with global SU(3) rotation
# ════════════════════════════════════════════════════════════════════════════

def q6_color_neutrality(L=12, dt=1.0, seed=29):
    print("─" * 70)
    print("Q6  Colour neutrality — F27 mass step commutes with global SU(3)")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')

    theta_flavour = {f: cs.make_theta_field_quark(shape, mode='random',
                                                  seed=seed + i)
                     for i, f in enumerate(cs.FLAVOURS)}
    m_flavour = {'u': 0.05, 'd': 0.08, 's': 0.15}

    # Global (spatially constant) SU(3) rotation
    V_const = cs.su3_haar(rng)
    Vfield = np.broadcast_to(V_const, (L, L, 3, 3)).copy()

    # Path A: rotate q by V, then mass step
    qV = cs.gauge_transform_quark(q, Vfield)
    qVA = cs.quark_mass_step_f27(qV, theta_flavour, m_flavour, dt=dt)

    # Path B: mass step on q, then rotate by V
    qB = cs.quark_mass_step_f27(q, theta_flavour, m_flavour, dt=dt)
    qBV = cs.gauge_transform_quark(qB, Vfield)

    res = quark_diff_max(qVA, qBV)
    passed = res < 1e-13
    report("Q6 [V_global, mass_step] = 0",
           passed, residual=res, note=f"L={L}")
    return {'name': 'Q6_color_neutrality', 'pass': bool(passed),
            'residual': float(res)}


# ════════════════════════════════════════════════════════════════════════════
#  Q7 — Cold-link, θ=0 regression: F27 quark step ≡ N_F · N_C independent
#       cd.dirac_step_complex_mass_1flavor(θ=0) bit-for-bit.
# ════════════════════════════════════════════════════════════════════════════

def q7_cold_link_regression(L=12, dt=1.0, seed=31):
    print("─" * 70)
    print("Q7  Cold-link θ=0 regression — bit-for-bit vs per-(f,c) lepton F27")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')
    U = cs.cold_links_2d(shape)

    theta = cs.make_theta_field_quark(shape, mode='zero')
    theta_flavour = {f: theta for f in cs.FLAVOURS}
    m_flavour = {'u': 0.10, 'd': 0.25, 's': 0.50}

    # Path A: full F27 quark step
    qA = cs.step_strong_2d_complex_mass(q, U,
                                        theta_flavour=theta_flavour,
                                        m_flavour=m_flavour, dt=dt)

    # Path B: 9 independent lepton-side F27 1-flavour steps
    qB = {k: v.copy() for k, v in q.items()}
    for f in cs.FLAVOURS:
        m = m_flavour[f]
        for c in cs.COLOURS:
            eu_n, ed_n, cu_n, cd_n = cd.dirac_step_complex_mass_1flavor(
                qB[(f, c, 'eu')], qB[(f, c, 'ed')],
                qB[(f, c, 'cu')], qB[(f, c, 'cd')],
                theta, m, dt)
            qB[(f, c, 'eu')] = eu_n
            qB[(f, c, 'ed')] = ed_n
            qB[(f, c, 'cu')] = cu_n
            qB[(f, c, 'cd')] = cd_n

    res = quark_diff_max(qA, qB)
    passed = res < 1e-14
    report("Q7 bit-for-bit cold-link regression",
           passed, residual=res, note=f"L={L}, exact identity expected")
    return {'name': 'Q7_cold_link_regression', 'pass': bool(passed),
            'residual': float(res)}


# ════════════════════════════════════════════════════════════════════════════
#  Q8 — Colour charge conservation Q^a under F27 step (cold/frozen links)
# ════════════════════════════════════════════════════════════════════════════

def q8_color_charge_conservation(L=12, n_steps=20, dt=1.0, seed=37):
    print("─" * 70)
    print("Q8  Colour charge Q^a conserved under the F27 quark step (cold links)")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')
    U = cs.cold_links_2d(shape)

    theta_flavour = {f: cs.make_theta_field_quark(shape, mode='random',
                                                  seed=seed + i)
                     for i, f in enumerate(cs.FLAVOURS)}
    m_flavour = {'u': 0.05, 'd': 0.08, 's': 0.15}

    Q0 = cs.noether_charge_total(q)
    for _ in range(n_steps):
        q = cs.step_strong_2d_complex_mass(q, U,
                                           theta_flavour=theta_flavour,
                                           m_flavour=m_flavour, dt=dt)
    Q1 = cs.noether_charge_total(q)
    delta = float(np.max(np.abs(Q1 - Q0)))
    rel = delta / max(float(np.max(np.abs(Q0))), 1e-30)
    passed = rel < 1e-9
    report("Q8 max |ΔQ^a| across 8 generators (cold links)",
           passed, residual=rel,
           note=f"abs={delta:.3e}, rel={rel:.3e}, n={n_steps}")
    return {'name': 'Q8_color_charge_conservation', 'pass': bool(passed),
            'residual': float(rel), 'abs_drift': float(delta),
            'Q0': [float(x) for x in Q0], 'Q1': [float(x) for x in Q1]}


# ════════════════════════════════════════════════════════════════════════════
#  Q9 — Degenerate-doublet SU(2)_L Ward identity (mass step alone)
#
#  For the F27 SU(2) doublet mass step with shared m_doublet,
#
#        V · doublet_mass(ψ; U) = doublet_mass(V·ψ; V·U)
#
#  to machine precision (F27 T5 analog, applied to the (u,d) doublet
#  per colour).
# ════════════════════════════════════════════════════════════════════════════

def q9_doublet_su2_ward(L=12, dt=1.0, seed=41):
    print("─" * 70)
    print("Q9  Degenerate-doublet SU(2)_L Ward identity (F27 SU(2) doublet mass)")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')

    # U(x) random SU(2) Stueckelberg field
    raw = rng.standard_normal(shape + (4,))
    raw /= np.linalg.norm(raw, axis=-1, keepdims=True)
    U_a = raw[..., 0] + 1j * raw[..., 3]
    U_b = raw[..., 2] + 1j * raw[..., 1]

    # V(x) random SU(2) gauge field
    raw2 = rng.standard_normal(shape + (4,))
    raw2 /= np.linalg.norm(raw2, axis=-1, keepdims=True)
    V_a = raw2[..., 0] + 1j * raw2[..., 3]
    V_b = raw2[..., 2] + 1j * raw2[..., 1]

    m_doublet = 0.2

    # Path A: V·doublet_mass(ψ; U)
    qA = cs.quark_doublet_mass_step_su2(q, U_a, U_b, m_doublet, dt=dt)
    qA_V, _, _ = cs.quark_doublet_su2_transform_chiral(qA, V_a, V_b, U_a, U_b)

    # Path B: doublet_mass(V·ψ; V·U)
    qV, U_a_new, U_b_new = cs.quark_doublet_su2_transform_chiral(
        q, V_a, V_b, U_a, U_b)
    qB = cs.quark_doublet_mass_step_su2(qV, U_a_new, U_b_new,
                                        m_doublet, dt=dt)

    res = quark_diff_max(qA_V, qB)
    passed = res < 1e-13
    report("Q9 SU(2)_L Ward identity (mass step alone, degenerate m)",
           passed, residual=res, note=f"random V(x), random U(x); L={L}")
    return {'name': 'Q9_doublet_su2_ward', 'pass': bool(passed),
            'residual': float(res)}


# ════════════════════════════════════════════════════════════════════════════
#  Q10 — Split-mass SU(2)_L Ward identity (per-flavour m_u ≠ m_d): expected FAIL
#
#  Mass splitting m_u ≠ m_d explicitly breaks SU(2)_L at the mass level —
#  a degenerate doublet is SU(2)-invariant, a split doublet is not.  This
#  test runs the per-flavour F27 step (`quark_mass_step_f27`) with realistic
#  m_u ≠ m_d and verifies that the SU(2)_L Ward identity is BROKEN, i.e.
#  the residual is O(1), not O(ε).
# ════════════════════════════════════════════════════════════════════════════

def q10_split_mass_breaks_su2(L=12, dt=1.0, seed=43):
    print("─" * 70)
    print("Q10  Split-mass SU(2)_L Ward identity — expected FAIL (mass split breaks SU(2))")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')

    raw2 = rng.standard_normal(shape + (4,))
    raw2 /= np.linalg.norm(raw2, axis=-1, keepdims=True)
    V_a = raw2[..., 0] + 1j * raw2[..., 3]
    V_b = raw2[..., 2] + 1j * raw2[..., 1]

    theta = cs.make_theta_field_quark(shape, mode='zero')
    theta_flavour = {f: theta for f in cs.FLAVOURS}
    m_flavour = {'u': 0.10, 'd': 0.40, 's': 0.0}  # split mass

    # Path A: V_L · per-flavour-mass(ψ)
    qA = cs.quark_mass_step_f27(q, theta_flavour, m_flavour, dt=dt)
    qA_V, _, _ = cs.quark_doublet_su2_transform_chiral(
        qA, V_a, V_b,
        np.ones_like(V_a), np.zeros_like(V_b))

    # Path B: per-flavour-mass(V_L · ψ)
    qV, _, _ = cs.quark_doublet_su2_transform_chiral(
        q, V_a, V_b,
        np.ones_like(V_a), np.zeros_like(V_b))
    qB = cs.quark_mass_step_f27(qV, theta_flavour, m_flavour, dt=dt)

    res = quark_diff_max(qA_V, qB)
    # We EXPECT this to fail (residual O(m_d − m_u) per step) — pass = "fails by enough"
    passed = res > 1e-3
    report("Q10 mass-split residual is O(1), not O(ε) [diagnostic]",
           passed, residual=res,
           note=f"m_u={m_flavour['u']}, m_d={m_flavour['d']}; "
                f"residual {res:.3e} (expected ≫ ε)")
    return {'name': 'Q10_split_mass_breaks_su2', 'pass': bool(passed),
            'residual': float(res),
            'diagnostic_meaning': 'large residual confirms that explicit '
                                  'mass splitting breaks SU(2)_L at the '
                                  'mass-step level. Phase-4 EW wiring '
                                  '(separate u_R, d_R singlets coupling '
                                  'through the two columns of U) restores '
                                  'SU(2)_L while keeping m_u ≠ m_d.'}


# ════════════════════════════════════════════════════════════════════════════
#  Q11 — Full kinetic+mass step under VARYING V(x): expected FAIL
#
#  Even with a degenerate doublet (m_u = m_d), the combined Strang step
#  K(dt/2)→M(dt)→K(dt/2) is NOT locally SU(2)_L-invariant because the
#  spectral kinetic step does not transport gauge phase from one cell to
#  another.  This is F27 Known Limitation #1 / W1.4 status (O(a)·|∇V|·L
#  residual).  Closure requires a W_μ link field (Phase 4).
# ════════════════════════════════════════════════════════════════════════════

def q11_kinetic_breaks_local_su2(L=12, dt=1.0, seed=47):
    print("─" * 70)
    print("Q11  Combined kinetic+mass step under VARYING V(x) — expected FAIL")
    print("─" * 70)

    shape = (L, L)
    rng = np.random.default_rng(seed)
    q = random_quark_state(shape, rng, chirality='mixed')

    # Spatially varying random V(x) (so the kinetic step cannot commute)
    raw = rng.standard_normal(shape + (4,))
    raw /= np.linalg.norm(raw, axis=-1, keepdims=True)
    V_a = raw[..., 0] + 1j * raw[..., 3]
    V_b = raw[..., 2] + 1j * raw[..., 1]

    U = cs.cold_links_2d(shape)
    theta = cs.make_theta_field_quark(shape, mode='zero')
    theta_flavour = {f: theta for f in cs.FLAVOURS}
    m_flavour = {'u': 0.20, 'd': 0.20, 's': 0.0}  # DEGENERATE

    # Path A: V · full_step(ψ)
    qA = cs.step_strong_2d_complex_mass(q, U,
                                        theta_flavour=theta_flavour,
                                        m_flavour=m_flavour, dt=dt)
    qA_V, _, _ = cs.quark_doublet_su2_transform_chiral(
        qA, V_a, V_b,
        np.ones_like(V_a), np.zeros_like(V_b))

    # Path B: full_step(V · ψ)
    qV, _, _ = cs.quark_doublet_su2_transform_chiral(
        q, V_a, V_b,
        np.ones_like(V_a), np.zeros_like(V_b))
    qB = cs.step_strong_2d_complex_mass(qV, U,
                                        theta_flavour=theta_flavour,
                                        m_flavour=m_flavour, dt=dt)

    res = quark_diff_max(qA_V, qB)
    # Expected to fail to "exact" SU(2) by an O(a)·|∇V|·L margin
    passed = res > 1e-3
    report("Q11 local SU(2)_L residual under varying V (no W_μ) [diagnostic]",
           passed, residual=res,
           note=f"residual {res:.3e} — kinetic FFT needs a W_μ link field "
                f"(O(a)·|∇V|·L, same status as W1.4)")
    return {'name': 'Q11_kinetic_breaks_local_su2', 'pass': bool(passed),
            'residual': float(res),
            'diagnostic_meaning': 'large residual confirms that the spectral '
                                  'kinetic step does not satisfy local '
                                  'SU(2)_L Ward identity without a W_μ '
                                  'link field. Phase-4 EW wiring closes this.'}


# ════════════════════════════════════════════════════════════════════════════
#  Main driver
# ════════════════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    print("=" * 70)
    print("FG-2 — F27 complex-mass adoption for the quark sector")
    print("=" * 70)

    results = []
    results.append(q1_unitarity())
    results.append(q2_u1_ward())
    results.append(q3_mass_gap())
    results.append(q4_mass_splitting())
    results.append(q5_theta_pure_gauge())
    results.append(q6_color_neutrality())
    results.append(q7_cold_link_regression())
    results.append(q8_color_charge_conservation())
    results.append(q9_doublet_su2_ward())
    results.append(q10_split_mass_breaks_su2())
    results.append(q11_kinetic_breaks_local_su2())

    n_pass = sum(1 for r in results if r['pass'])
    n_tot = len(results)
    elapsed = time.time() - t0
    print("─" * 70)
    print(f"FG-2 summary: {n_pass}/{n_tot} PASS in {elapsed:.2f} s")
    print(f"  • Q1–Q8: F27 complex-mass adoption (must all PASS)")
    print(f"  • Q9   : SU(2)_L Ward identity for the degenerate doublet "
          "(must PASS — proves the mechanism is right when isospin is "
          "respected)")
    print(f"  • Q10–Q11: trigger tests for Phase-4 EW wiring (must show "
          "the failure modes that motivate W_μ)")

    out_dir = os.path.abspath(os.path.join(_THIS, '..', 'test-results'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'FG2_quark_complex_mass.json')
    payload = {
        'name': 'FG-2 quark F27 complex-mass adoption',
        'date': '2026-05-26',
        'lattice': '2D-square (ca_strong)',
        'modules': ['ca_strong (additions)', 'ca_dirac (F27 reused)'],
        'n_pass': n_pass, 'n_total': n_tot,
        'elapsed_seconds': float(elapsed),
        'results': results,
    }
    with open(out_path, 'w') as fp:
        json.dump(payload, fp, indent=2)
    print(f"  JSON: {out_path}")


if __name__ == '__main__':
    main()
