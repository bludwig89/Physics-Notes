"""
test_FG7_gluon_dynamics.py — FG-7: dynamical SU(3) gluon sector
================================================================

Brings the colour sector to the level the W reached:

  Phase A — colour-octet bilinear G^a + free rotation law  (port F29)
  Phase B — Wilson plaquette G^a_{μν} + Yang-Mills self-coupling  (port F33)
  Phase C — Wilson-loop area-law diagnostic on frozen non-trivial links
  Phase D — quark colour current sourcing the gluon (port F36)

Tested on both lattices: 2D-square (`ca_strong.py` native) and 3D BCC
(`ca_wmu.py` style), per the design in `reference-research/ca-strong-design.md`.

Module under test:  ca-simulation/ca_gluon.py
Created:            2026-05-27
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_gluon as cg          # noqa: E402
import ca_strong as cs         # noqa: E402


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def _random_quark(shape, rng, amp=0.3):
    q = cs.zero_quark_field(shape)
    for k in q:
        q[k] = (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) * amp
    return q


def _constant_V(shape, V):
    """Broadcast a 3×3 SU(3) matrix to V(x) constant across shape."""
    return np.broadcast_to(V, shape + (3, 3)).copy()


def _local_V_field(shape, rng):
    """Build a random local V(x) ∈ SU(3) on every cell."""
    Vfield = np.zeros(shape + (3, 3), dtype=complex)
    flat = Vfield.reshape(-1, 3, 3)
    for n in range(flat.shape[0]):
        flat[n] = cs.su3_exp(rng.standard_normal(8))
    return Vfield


# ═════════════════════════════════════════════════════════════════════
#  Phase A  —  Colour-octet bilinear + free rotation law
# ═════════════════════════════════════════════════════════════════════

def test_PA1_jacobi_identity():
    """A1 — SU(3) structure constants satisfy the Jacobi identity exactly."""
    res = cg.structure_constants_jacobi_residual()
    return {'test': 'PA.1', 'name': 'Jacobi identity for f^abc',
            'residual': res, 'target': 1e-13,
            'passed': bool(res < 1e-13),
            'description': 'algebraic identity, machine precision'}


def test_PA2_rotation_magnitude_2d():
    """A2 — 2D rotation law preserves Σ_a (E^a²+B^a²) per tick (machine ε)."""
    rng = np.random.default_rng(11)
    L = 16
    E = rng.standard_normal((8, L, L))
    B = rng.standard_normal((8, L, L))
    mag0 = float(np.sum(E**2 + B**2))
    for _ in range(20):
        E, B = cg.gluon_rotation_step_spectral_2d(E, B)
    magN = float(np.sum(E**2 + B**2))
    drift = abs(magN - mag0) / mag0
    return {'test': 'PA.2', 'name': '2D rotation magnitude conservation (20 ticks)',
            'residual': drift, 'target': 1e-12,
            'passed': bool(drift < 1e-12),
            'description': 'F26 rotation per a — energy preserved geometrically'}


def test_PA3_rotation_magnitude_bcc():
    """A3 — BCC rotation law preserves Σ_a (E^a²+B^a²) per tick (machine ε)."""
    rng = np.random.default_rng(13)
    L = 10
    E = rng.standard_normal((8, L, L, L))
    B = rng.standard_normal((8, L, L, L))
    mag0 = float(np.sum(E**2 + B**2))
    for _ in range(10):
        E, B = cg.gluon_rotation_step_spectral_bcc(E, B)
    magN = float(np.sum(E**2 + B**2))
    drift = abs(magN - mag0) / mag0
    return {'test': 'PA.3', 'name': 'BCC rotation magnitude conservation (10 ticks)',
            'residual': drift, 'target': 1e-12,
            'passed': bool(drift < 1e-12),
            'description': 'F26 rotation per a on the BCC lattice'}


def test_PA4_adjoint_identity_2d():
    """A4 — G_{Vq}^a = R_adj^{ab}(V) G_q^b  (constant V ∈ SU(3))."""
    rng = np.random.default_rng(17)
    shape = (8, 8)
    q = _random_quark(shape, rng)
    G_before = cg.quark_colour_octet_bilinear_2d(q)
    V = cs.su3_exp(rng.standard_normal(8))
    Vfield = _constant_V(shape, V)
    q_rot = cs.gauge_transform_quark(q, Vfield)
    G_after = cg.quark_colour_octet_bilinear_2d(q_rot)
    G_pred = cg.octet_adjoint_rotate(G_before, V)
    res = float(np.max(np.abs(G_after - G_pred)))
    return {'test': 'PA.4', 'name': 'G^a transforms as SU(3) adjoint (2D bilinear)',
            'residual': res, 'target': 1e-13,
            'passed': bool(res < 1e-13),
            'description': 'F29 B2 SU(3) analog'}


def test_PA5_casimir_invariance_2d():
    """A5 — Σ_a ‖G^a‖² is SU(3)-invariant under constant V (2D bilinear)."""
    rng = np.random.default_rng(19)
    shape = (8, 8)
    q = _random_quark(shape, rng)
    G = cg.quark_colour_octet_bilinear_2d(q)
    mag0 = cg.octet_norm_sq(G)
    V = cs.su3_exp(rng.standard_normal(8))
    Vfield = _constant_V(shape, V)
    q_rot = cs.gauge_transform_quark(q, Vfield)
    Gp = cg.quark_colour_octet_bilinear_2d(q_rot)
    magV = cg.octet_norm_sq(Gp)
    rel = abs(magV - mag0) / abs(mag0)
    return {'test': 'PA.5', 'name': 'Σ_a ‖G^a‖² SU(3) Casimir invariance',
            'residual': rel, 'target': 1e-12,
            'passed': bool(rel < 1e-12),
            'description': 'F29 B3 SU(3) analog'}


def test_PA6_adjoint_identity_bcc():
    """A6 — BCC bilinear obeys G_{Vq}^a = R_adj^{ab} G_q^b."""
    rng = np.random.default_rng(21)
    shape = (5, 5, 5)
    q = cs.zero_quark_field((shape[0], shape[1]))   # placeholder shape
    # Build a fresh BCC-shaped quark field
    q = {}
    for f in cs.FLAVOURS:
        for c in cs.COLOURS:
            for d in cs.DIRAC:
                q[(f, c, d)] = (rng.standard_normal(shape)
                                + 1j * rng.standard_normal(shape)) * 0.3
    G_before = cg.quark_colour_octet_bilinear_bcc(q)
    V = cs.su3_exp(rng.standard_normal(8))
    Vfield = np.broadcast_to(V, shape + (3, 3)).copy()
    # gauge_transform_quark is hard-coded to 2D einsum — manual rotation here:
    q_rot = {}
    for f in cs.FLAVOURS:
        for d in cs.DIRAC:
            triplet = np.stack([q[(f, c, d)] for c in cs.COLOURS], axis=-1)
            rotated = np.einsum('xyzij,xyzj->xyzi', Vfield, triplet)
            for i, c in enumerate(cs.COLOURS):
                q_rot[(f, c, d)] = rotated[..., i]
    G_after = cg.quark_colour_octet_bilinear_bcc(q_rot)
    G_pred = cg.octet_adjoint_rotate(G_before, V)
    res = float(np.max(np.abs(G_after - G_pred)))
    return {'test': 'PA.6', 'name': 'G^a transforms as SU(3) adjoint (BCC bilinear)',
            'residual': res, 'target': 1e-12,
            'passed': bool(res < 1e-12),
            'description': 'F29 B2 SU(3) analog on BCC'}


# ═════════════════════════════════════════════════════════════════════
#  Phase B  —  Wilson plaquette G^a_{μν} + Yang-Mills self-coupling
# ═════════════════════════════════════════════════════════════════════

def test_PB1_identity_links_zero_F_2d():
    """B1 — Identity links → G^a_{xy} = 0 exactly (2D-square)."""
    U = cs.cold_links_2d((10, 10))
    G = cg.plaquette_field_strength_su3_2d(U)
    res = float(np.max(np.abs(G)))
    return {'test': 'PB.1', 'name': '2D cold links → G^a = 0',
            'residual': res, 'target': 0.0,
            'passed': bool(res == 0.0),
            'description': 'bit-for-bit identity, Tr(T^a · I) = 0'}


def test_PB2_identity_links_zero_F_bcc():
    """B2 — Identity BCC links → G^a_{μν} = 0 exactly (all 3 planes)."""
    U = cg.make_su3_link_field_bcc(6, mode='identity')
    G = cg.plaquette_field_strength_su3_bcc(U)
    res = max(float(np.max(np.abs(G[k]))) for k in ('xy', 'xz', 'yz'))
    return {'test': 'PB.2', 'name': 'BCC cold links → G^a_{μν} = 0',
            'residual': res, 'target': 0.0,
            'passed': bool(res == 0.0),
            'description': 'all three composite plaquettes vanish exactly'}


def test_PB3_random_links_nonzero_F():
    """B3 — Random non-trivial links → G^a non-zero (structural)."""
    rng = np.random.default_rng(23)
    U = cs.random_su3_links_2d((8, 8), rng=rng)
    G = cg.plaquette_field_strength_su3_2d(U)
    val = float(np.max(np.abs(G)))
    return {'test': 'PB.3', 'name': '2D random links → G^a non-zero',
            'residual': val, 'target': 0.1,         # any O(1) is fine
            'passed': bool(val > 0.1),
            'description': 'non-Abelian plaquette captures U_μ U_ν ≠ U_ν U_μ'}


def test_PB4_constant_V_gauge_invariance_2d():
    """B4 — ‖G‖² SU(3)-invariant under constant V (2D plaquette)."""
    rng = np.random.default_rng(29)
    shape = (8, 8)
    U = cs.random_su3_links_2d(shape, rng=rng)
    G_before = cg.plaquette_field_strength_su3_2d(U)
    V = cs.su3_exp(rng.standard_normal(8))
    Vfield = _constant_V(shape, V)
    U_rot = cs.gauge_transform_links(U, Vfield)
    G_after = cg.plaquette_field_strength_su3_2d(U_rot)
    norm_b = cg.yang_mills_norm_sq_2d(G_before)
    norm_a = cg.yang_mills_norm_sq_2d(G_after)
    rel = abs(norm_a - norm_b) / abs(norm_b)
    return {'test': 'PB.4', 'name': '‖G^a_{xy}‖² constant-V SU(3) invariance',
            'residual': rel, 'target': 1e-12,
            'passed': bool(rel < 1e-12),
            'description': 'F33 W3.3 SU(3) analog'}


def test_PB5_self_coupling_unitarity_2d():
    """B5 — Self-coupling step preserves 2D SU(3) link unitarity (≤ 1e-13)."""
    rng = np.random.default_rng(31)
    U = cs.random_su3_links_2d((8, 8), rng=rng)
    for _ in range(5):
        U = cg.gluon_self_coupling_step_2d(U, dt=0.05)
    res = cg.link_unitarity_residual_su3(U)
    return {'test': 'PB.5', 'name': '2D self-coupling preserves link unitarity (5 ticks)',
            'residual': res, 'target': 1e-13,
            'passed': bool(res < 1e-13),
            'description': 'F33 W3.4 SU(3) analog — δU = exp(iH)·U is SU(3)'}


def test_PB6_self_coupling_unitarity_bcc():
    """B6 — Self-coupling step preserves BCC SU(3) link unitarity (≤ 1e-13)."""
    U = cg.make_su3_link_field_bcc(6, mode='near_id', seed=33)
    for _ in range(5):
        U = cg.gluon_self_coupling_step_bcc(U, dt=0.05)
    res = cg.link_unitarity_residual_su3(U)
    return {'test': 'PB.6', 'name': 'BCC self-coupling preserves link unitarity (5 ticks)',
            'residual': res, 'target': 1e-13,
            'passed': bool(res < 1e-13),
            'description': 'F33 W3.4 SU(3) analog on BCC'}


# ═════════════════════════════════════════════════════════════════════
#  Phase C  —  Wilson-loop area-law diagnostic
# ═════════════════════════════════════════════════════════════════════

def test_PC1_cold_loop_equals_Nc():
    """C1 — Cold links: ⟨Re Tr W(r,t)⟩ = N_c = 3 exactly for any (r,t)."""
    U = cs.cold_links_2d((8, 8))
    worst = 0.0
    for r in (1, 2, 3):
        for t in (1, 2, 3):
            W = cg.wilson_loop_2d_avg(U, r, t)
            worst = max(worst, abs(W - 3.0))
    return {'test': 'PC.1', 'name': 'Cold-link Wilson loop = N_c = 3 (9 sizes)',
            'residual': worst, 'target': 1e-13,
            'passed': bool(worst < 1e-13),
            'description': 'every product term is I·I·...·I = I; Tr I = 3'}


def test_PC2_local_gauge_invariance():
    """C2 — Wilson loop ⟨Re Tr W⟩ invariant under local V(x) gauge transform."""
    rng = np.random.default_rng(37)
    shape = (6, 6)
    U = cs.random_su3_links_2d(shape, rng=rng)
    Vlocal = _local_V_field(shape, rng)
    worst = 0.0
    for r in (1, 2):
        for t in (1, 2):
            res = cg.wilson_loop_gauge_residual_2d(U, Vlocal, r, t)
            worst = max(worst, res)
    return {'test': 'PC.2', 'name': 'Wilson loop local SU(3) gauge invariance',
            'residual': worst, 'target': 1e-12,
            'passed': bool(worst < 1e-12),
            'description': 'V cancels at the closed-loop start/end corner exactly'}


def test_PC3_strong_coupling_decorrelation():
    """
    C3 — Strong-coupling regime: on Haar-random links the cold-link baseline
    ⟨Re Tr W⟩ = N_c = 3 is broken to |W| ≪ 1 for every loop size.

    This is the lattice-gauge "deconfining-to-zero" baseline (strong-coupling
    expansion limit β→0): all loops decorrelate to ~0 because each link is
    independent Haar.  Confining linear regime requires gradient flow / cooling
    from a near-identity start, which is FG-7's next-session item.  Here we
    verify the algebraic property that random-link Wilson traces are bounded
    well below N_c — i.e. the diagnostic distinguishes confined (cold = 3)
    from decorrelated (~0) regimes.
    """
    rng = np.random.default_rng(41)
    U = cs.random_su3_links_2d((10, 10), rng=rng)
    W = {(r, t): cg.wilson_loop_2d_avg(U, r, t) for r in (1, 2, 3) for t in (1, 2, 3)}
    worst = max(abs(v) for v in W.values())
    bounded = worst < 0.5
    return {'test': 'PC.3', 'name': 'Random-link Wilson loops bounded ≪ N_c',
            'residual': worst, 'target': 0.5,
            'loop_traces': {f'{k[0]}x{k[1]}': v for k, v in W.items()},
            'cold_baseline': 3.0,
            'passed': bool(bounded),
            'description': 'strong-coupling decorrelation: |W(r,t)| ≪ N_c=3'}


# ═════════════════════════════════════════════════════════════════════
#  Phase D  —  Quark current sourcing the gluon
# ═════════════════════════════════════════════════════════════════════

def test_PD1_current_octet_from_quark():
    """D1 — quark_colour_current_2d returns 8 charge densities consistent with
    `ca_strong.noether_charge_density` (existing test #8 in inventory)."""
    rng = np.random.default_rng(43)
    q = _random_quark((8, 8), rng)
    J0, Js = cg.quark_colour_current_2d(q)
    Jref = cs.noether_charge_density(q)
    res = float(np.max(np.abs(J0 - Jref)))
    return {'test': 'PD.1', 'name': 'Octet charge density wraps Noether current',
            'residual': res, 'target': 1e-14,
            'passed': bool(res < 1e-14),
            'description': 'wrapper consistency, machine ε'}


def test_PD2_diagonal_coupling():
    """D2 — Pure a=k source drives only E^k component (W^a F36 WB.3 analog)."""
    rng = np.random.default_rng(47)
    shape = (8, 8)
    E_G = np.zeros((8,) + shape)
    B_G = np.zeros((8,) + shape)
    worst = 0.0
    on_diag = []
    for a_drive in range(8):
        J = np.zeros((8,) + shape)
        J[a_drive] = rng.standard_normal(shape)
        E_new, B_new = cg.gluon_sourced_step_2d(E_G, B_G, J, dt=1.0)
        diag = float(np.max(np.abs(E_new[a_drive])))
        on_diag.append(diag)
        for a_other in range(8):
            if a_other == a_drive:
                continue
            v = float(np.max(np.abs(E_new[a_other])))
            worst = max(worst, v)
    return {'test': 'PD.2', 'name': 'Diagonal source coupling (all 8 octet components)',
            'residual': worst, 'target': 0.0,
            'passed': bool(worst == 0.0),
            'on_diagonal_max': max(on_diag),
            'description': 'F36 WB.3 SU(3) analog — exact zero off-diagonal'}


def test_PD3_massless_limit():
    """D3 — gluon_massive_step_spectral_bcc(m=0) bit-for-bit equals free step."""
    rng = np.random.default_rng(53)
    L = 8
    E = rng.standard_normal((8, L, L, L))
    B = rng.standard_normal((8, L, L, L))
    E1, B1 = cg.gluon_rotation_step_spectral_bcc(E.copy(), B.copy())
    E2, B2 = cg.gluon_massive_step_spectral_bcc(E.copy(), B.copy(), m_g=0.0)
    res = max(float(np.max(np.abs(E1 - E2))),
              float(np.max(np.abs(B1 - B2))))
    return {'test': 'PD.3', 'name': 'Massive step at m_g=0 reduces to free step',
            'residual': res, 'target': 0.0,
            'passed': bool(res == 0.0),
            'description': 'F36 WB.5 SU(3) analog — exact bit-for-bit'}


def test_PD4_free_gluon_dispersion():
    """D4 — Free-gluon dispersion ω(k) = Ω⁺(k) on BCC matches F26 to machine ε."""
    err = cg.free_gluon_dispersion_residual_bcc(L=12, n_steps=50, a_comp=0, seed=11)
    return {'test': 'PD.4', 'name': 'Free-gluon BCC dispersion residual (50 ticks)',
            'residual': err, 'target': 1e-12,
            'passed': bool(err < 1e-12),
            'description': 'C_n(k) = C_0(k)·exp(−iΩ⁺(k)·n) per a-component'}


def test_PD5_sourced_step_diagonal_iterates():
    """D5 — Pure a=2 source on free vacuum: after N ticks, other a still zero."""
    rng = np.random.default_rng(59)
    L = 6
    shape = (L, L, L)
    E_G = np.zeros((8,) + shape)
    B_G = np.zeros((8,) + shape)
    J = np.zeros((8,) + shape)
    J[2] = rng.standard_normal(shape)
    for _ in range(20):
        E_G, B_G = cg.gluon_sourced_step_bcc(E_G, B_G, J, dt=1.0)
    worst = max(
        float(np.max(np.abs(E_G[a]))) for a in (0, 1, 3, 4, 5, 6, 7)
    ) + max(
        float(np.max(np.abs(B_G[a]))) for a in (0, 1, 3, 4, 5, 6, 7)
    )
    on_diag = float(np.max(np.abs(E_G[2]))) + float(np.max(np.abs(B_G[2])))
    return {'test': 'PD.5', 'name': '20-tick sourced-step on BCC, off-diagonal stays zero',
            'residual': worst, 'target': 0.0,
            'on_diagonal_max': on_diag,
            'passed': bool(worst == 0.0),
            'description': 'no leakage between a-components at linear order'}


# ─────────────────────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────────────────────

def main():
    t_start = time.perf_counter()
    tests = [
        test_PA1_jacobi_identity,
        test_PA2_rotation_magnitude_2d,
        test_PA3_rotation_magnitude_bcc,
        test_PA4_adjoint_identity_2d,
        test_PA5_casimir_invariance_2d,
        test_PA6_adjoint_identity_bcc,
        test_PB1_identity_links_zero_F_2d,
        test_PB2_identity_links_zero_F_bcc,
        test_PB3_random_links_nonzero_F,
        test_PB4_constant_V_gauge_invariance_2d,
        test_PB5_self_coupling_unitarity_2d,
        test_PB6_self_coupling_unitarity_bcc,
        test_PC1_cold_loop_equals_Nc,
        test_PC2_local_gauge_invariance,
        test_PC3_strong_coupling_decorrelation,
        test_PD1_current_octet_from_quark,
        test_PD2_diagonal_coupling,
        test_PD3_massless_limit,
        test_PD4_free_gluon_dispersion,
        test_PD5_sourced_step_diagonal_iterates,
    ]
    results = []
    n_pass = 0
    for fn in tests:
        t0 = time.perf_counter()
        try:
            r = fn()
            r['elapsed_s'] = time.perf_counter() - t0
            results.append(r)
            ok = bool(r.get('passed'))
            n_pass += int(ok)
            print(f"  [{'PASS' if ok else 'FAIL'}] {r.get('test'):6s}  "
                  f"{r.get('name'):60s}  res = {r.get('residual', 'n/a')}  "
                  f"({r['elapsed_s']:.3f} s)")
        except Exception as exc:
            results.append({'test': fn.__name__, 'passed': False,
                            'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FG-7 — dynamical SU(3) gluon sector',
        'date': '2026-05-27',
        'n_tests': len(tests),
        'n_passed': n_pass,
        'total_elapsed_s': total_t,
        'results': results,
    }
    print(f"\n  → {n_pass}/{len(tests)} PASS  in  {total_t:.2f} s")
    return summary


if __name__ == '__main__':
    summary = main()
    out = os.path.join(os.path.dirname(__file__),
                       '..', 'test-results', 'FG7_gluon_dynamics.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  → wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
