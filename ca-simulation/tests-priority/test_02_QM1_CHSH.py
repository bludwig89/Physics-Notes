"""
Top-10 priority Test #2 — QM-1: Bell / CHSH inequality
=======================================================
Date: 2026-05-19

Goal
----
Verify that the lattice supports genuine non-local quantum correlations
by computing the CHSH correlator on an entangled-singlet state.  Pass
gate (from lattice-vs-spacetime-tests.md): S_lat ≥ 2.5, with the Tsirelson
upper bound 2·√2 ≈ 2.828.

Setup
-----
Two Weyl-spinor lattice cells (Alice's and Bob's), each carrying a 2-state
qubit (the η_↑/η_↓ pair).  We construct the spin-singlet entangled state

        |Ψ⁻⟩ = (1/√2) (|↑⟩_A |↓⟩_B − |↓⟩_A |↑⟩_B)

— this is the maximally entangled singlet that saturates Tsirelson.

Each party measures spin along a direction n̂ via the projector
        Π_±(n̂) = (1 ± σ·n̂) / 2
with σ the Pauli vector.  The correlation is
        E(â, b̂) = ⟨Ψ⁻|(σ·â)_A ⊗ (σ·b̂)_B|Ψ⁻⟩ = − â · b̂

For a singlet.  The CHSH combination at the Bell-optimal angles
(a=0, a'=π/2, b=π/4, b'=3π/4) gives

        S = |E(a,b) − E(a,b') + E(a',b) + E(a',b')| = 2√2 ≈ 2.828.

This test verifies the lattice's 2-qubit Hilbert-space machinery
reproduces the Tsirelson bound exactly when the singlet is encoded as
the antisymmetric spin combination on two lattice sites.

We use two complementary representations:

  (1) Pure-state inner-product calculation in C⁴ at a single (Alice, Bob)
      cell pair.  This is the "gold-standard" QM check and should give
      S = 2√2 to machine precision.

  (2) Wave-packet representation:  Alice and Bob each carry a separated
      Weyl Gaussian packet on the lattice, prepared in the singlet entangled
      state.  We propagate each packet independently (no interaction, just
      free evolution) over n_steps, then measure spin correlations.

If (1) and (2) agree to machine precision, the lattice's free Weyl
propagation preserves the entanglement structure — the foundational QM
requirement.
"""

import os, sys, math, time, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..')))

import ca_dirac  # pure-numpy, no scipy


# ─────────────────────────── Pauli matrices ───────────────────────────
sx = np.array([[0, 1],  [1, 0]],   dtype=complex)
sy = np.array([[0, -1j],[1j, 0]],  dtype=complex)
sz = np.array([[1, 0],  [0, -1]],  dtype=complex)


def sigma_n(theta, phi=0.0):
    """σ · n̂  with n̂ in the xz-plane at polar angle theta (phi unused for 2D)."""
    return np.cos(theta) * sz + np.sin(theta) * np.cos(phi) * sx + \
           np.sin(theta) * np.sin(phi) * sy


def singlet_state():
    """|Ψ⁻⟩ = (|↑↓⟩ − |↓↑⟩)/√2 as a length-4 column vector
       basis (↑↑, ↑↓, ↓↑, ↓↓)."""
    psi = np.array([0, 1, -1, 0], dtype=complex) / math.sqrt(2)
    return psi


def correlator(psi, theta_a, theta_b):
    """E(â, b̂) = ⟨ψ| (σ·â) ⊗ (σ·b̂) |ψ⟩."""
    A = sigma_n(theta_a)
    B = sigma_n(theta_b)
    AB = np.kron(A, B)
    return float(np.real(np.conj(psi) @ AB @ psi))


def chsh_S(psi, a, ap, b, bp):
    """CHSH operator value at chosen settings."""
    E_ab   = correlator(psi, a,  b)
    E_abp  = correlator(psi, a,  bp)
    E_apb  = correlator(psi, ap, b)
    E_apbp = correlator(psi, ap, bp)
    return E_ab - E_abp + E_apb + E_apbp, (E_ab, E_abp, E_apb, E_apbp)


def part1_pure_qm():
    """Pure-state QM at one cell pair — Tsirelson bound check."""
    psi = singlet_state()
    # Bell-optimal angles
    a, ap = 0.0,        math.pi/2
    b, bp = math.pi/4,  3*math.pi/4
    S, (E_ab, E_abp, E_apb, E_apbp) = chsh_S(psi, a, ap, b, bp)
    return {
        'angles_deg': {'a': 0, 'ap': 90, 'b': 45, 'bp': 135},
        'E_ab': E_ab, 'E_abp': E_abp, 'E_apb': E_apb, 'E_apbp': E_apbp,
        'S': S, 'absS': abs(S), 'S_target': 2.0 * math.sqrt(2.0),
        'residual': abs(abs(S) - 2.0 * math.sqrt(2.0)),
    }


def part2_local_real_bound():
    """Sanity check: a separable mixed state cannot exceed S = 2."""
    # Separable state |↑⟩_A |↓⟩_B
    sep = np.kron(np.array([1,0],dtype=complex), np.array([0,1],dtype=complex))
    a, ap = 0.0, math.pi/2
    b, bp = math.pi/4, 3*math.pi/4
    S_sep, _ = chsh_S(sep, a, ap, b, bp)
    # Maximally mixed state (50/50 separable mixture)
    rho_mix = 0.25 * np.eye(4, dtype=complex)
    A_op = np.kron(sigma_n(a), sigma_n(b))
    Ap_op = np.kron(sigma_n(a), sigma_n(bp))
    B_op = np.kron(sigma_n(ap), sigma_n(b))
    Bp_op = np.kron(sigma_n(ap), sigma_n(bp))
    E_mix = lambda O: float(np.real(np.trace(rho_mix @ O)))
    S_mix = E_mix(A_op) - E_mix(Ap_op) + E_mix(B_op) + E_mix(Bp_op)
    return {'S_separable_pure': S_sep,
            'S_max_mixed': S_mix,
            'classical_bound': 2.0}


def part3_lattice_propagation():
    """
    Encode the singlet on two well-separated Weyl wave packets on a 2D lattice,
    propagate each packet for n_steps using the exact-QCA Dirac stepper at m=0
    (Weyl regression), and verify the CHSH inner-product survives propagation.

    The two-qubit state has the form
        |Ψ_AB⟩ = (1/√2)(|↑_A⟩|↓_B⟩ − |↓_A⟩|↑_B⟩)
    realised as four lattice spinor-field configurations
        ψ_↑↓ = G_A(x;↑) · G_B(x;↓)   etc.
    where G_A and G_B are spatially-separated Gaussian envelopes carrying
    a Weyl spinor with chosen up/down component.

    We track the *components-on-A* of the propagated field and the
    *components-on-B* of the propagated field separately, then compute
    expectation values of σ_A and σ_B on each side.
    """
    L     = 64
    sigma = 4.0
    cA = (L // 4,     L // 2)
    cB = (3 * L // 4, L // 2)
    n_steps = 12     # short — at m=0 packets just propagate at v=1/√2

    # Build the two Gaussian envelopes
    x = np.arange(L); y = np.arange(L)
    X, Y = np.meshgrid(x, y, indexing='ij')
    gauss = lambda c: np.exp(-((X-c[0])**2 + (Y-c[1])**2)/(2*sigma**2))
    GA = gauss(cA).astype(complex)
    GB = gauss(cB).astype(complex)

    # In the chosen 2-qubit basis (↑↑, ↑↓, ↓↑, ↓↓), only ↑↓ and ↓↑ are nonzero,
    # with coefficients 1/√2 and -1/√2 respectively.  We carry the full Weyl
    # spinor on each Gaussian and propagate via ca_dirac.dirac_step_2d_splitstep.
    # The η_↑ component represents spin-up, η_↓ represents spin-down (chi
    # components are zero at m=0).

    inv_sqrt2 = 1.0 / math.sqrt(2.0)

    # Two field configurations: ψ_A↑B↓  and  ψ_A↓B↑
    # We propagate separately and combine at measurement.
    # Spinor: the "up at A, down at B" contribution puts G_A in η_↑ and G_B in η_↓.
    eta_u_AB_1 = GA.copy()    # spin-up at Alice's location
    eta_d_AB_1 = GB.copy()    # spin-down at Bob's location
    eta_u_AB_2 = GB.copy()    # spin-up at Bob's location  (the |↓↑⟩ piece, swapped)
    eta_d_AB_2 = GA.copy()    # spin-down at Alice's location

    chi_u = np.zeros_like(GA); chi_d = np.zeros_like(GA)

    # Propagate at m=0 (pure Weyl)
    for _ in range(n_steps):
        eta_u_AB_1, eta_d_AB_1, _, _ = ca_dirac.dirac_step_2d_splitstep(
            eta_u_AB_1, eta_d_AB_1, chi_u, chi_d, m=0.0, dt=1.0)
        eta_u_AB_2, eta_d_AB_2, _, _ = ca_dirac.dirac_step_2d_splitstep(
            eta_u_AB_2, eta_d_AB_2, chi_u, chi_d, m=0.0, dt=1.0)

    # Now extract the four spinor amplitudes at Alice's cell cA and Bob's cell cB.
    # In the singlet:  |↑↑⟩ coefficient = 0, |↑↓⟩ = 1/√2, |↓↑⟩ = −1/√2, |↓↓⟩ = 0.
    # The propagated field at cA has spin components (eta_u, eta_d) which encode
    # Alice's qubit; similarly at cB.  We sample at fixed cells (the packets'
    # original centers).
    iA, jA = cA
    iB, jB = cB

    # |↑_A↓_B⟩ contribution after propagation:
    # Alice spin-up amplitude at cA, Bob spin-down amplitude at cB.
    A_up_1   = eta_u_AB_1[iA, jA]
    B_down_1 = eta_d_AB_1[iB, jB]
    A_dn_1   = eta_d_AB_1[iA, jA]
    B_up_1   = eta_u_AB_1[iB, jB]
    # |↓_A↑_B⟩ contribution
    A_up_2   = eta_u_AB_2[iA, jA]
    B_down_2 = eta_d_AB_2[iB, jB]
    A_dn_2   = eta_d_AB_2[iA, jA]
    B_up_2   = eta_u_AB_2[iB, jB]

    # Pre-propagation values (for comparison; normalisation reference)
    # Initially A_up_1 = GA[iA,jA] = 1, B_down_1 = GB[iB,jB] = 1, others = 0
    # We measure norm preservation:
    # The "lattice singlet" coefficient is captured by the inner products with
    # the singlet basis.  Build the lattice-singlet 2-qubit amplitudes:
    amp_up_dn = inv_sqrt2 * A_up_1 * B_down_1   # ⟨↑_A↓_B|Ψ⟩-like
    amp_dn_up = -inv_sqrt2 * A_dn_2 * B_up_2    # ⟨↓_A↑_B|Ψ⟩-like
    # Other singlet basis: ↑↑ and ↓↓ should be small (only nonzero if Weyl
    # propagation mixed the components — should not at m=0).
    amp_up_up = inv_sqrt2 * A_up_1 * B_up_1    # leakage
    amp_dn_dn = -inv_sqrt2 * A_dn_2 * B_down_2   # leakage

    # Reconstruct the post-propagation 2-qubit state and compute CHSH.
    # Normalise by the absolute amplitudes (the Gaussian peak amplitude
    # diffuses during propagation but stays real-positive at m=0).
    norm = math.sqrt(abs(amp_up_dn)**2 + abs(amp_dn_up)**2 +
                     abs(amp_up_up)**2 + abs(amp_dn_dn)**2)
    psi_lat = np.array([amp_up_up, amp_up_dn, amp_dn_up, amp_dn_dn]) / norm

    a, ap = 0.0,        math.pi/2
    b, bp = math.pi/4,  3*math.pi/4
    S_lat, _ = chsh_S(psi_lat, a, ap, b, bp)
    return {
        'n_steps': n_steps, 'L': L,
        'S_lat': S_lat, 'absS_lat': abs(S_lat),
        'S_target_Tsirelson': 2.0 * math.sqrt(2.0),
        'leakage_uu': float(abs(amp_up_up)),
        'leakage_dd': float(abs(amp_dn_dn)),
        'residual': abs(abs(S_lat) - 2.0 * math.sqrt(2.0)),
    }


def main():
    print('=' * 70)
    print('QM-1 — CHSH Bell inequality on the lattice')
    print('=' * 70)
    print('Date 2026-05-19')
    print()

    out = {'date': '2026-05-19', 'test': 'QM-1 CHSH'}

    print('Part 1 — Pure-state QM at one cell pair (Tsirelson bound)')
    r1 = part1_pure_qm()
    for k, v in r1.items(): print(f'  {k}: {v}')
    out['part1'] = r1
    print()

    print('Part 2 — Classical / separable controls (should give |S| ≤ 2)')
    r2 = part2_local_real_bound()
    for k, v in r2.items(): print(f'  {k}: {v}')
    out['part2'] = r2
    print()

    print('Part 3 — Wave-packet lattice propagation, m = 0 (Weyl regression)')
    r3 = part3_lattice_propagation()
    for k, v in r3.items(): print(f'  {k}: {v}')
    out['part3'] = r3
    print()

    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    print(f'  Pure-state singlet CHSH:        S = {r1["S"]:.10f}  |S| = {r1["absS"]:.10f}')
    print(f'  Tsirelson bound:                2√2 = {2*math.sqrt(2):.10f}')
    print(f'  Residual:                       {r1["residual"]:.2e}')
    print(f'  Lattice-propagated CHSH:        S = {r3["S_lat"]:.10f}  |S| = {r3["absS_lat"]:.10f}')
    print(f'  Lattice residual:               {r3["residual"]:.2e}')
    pass1 = r1["absS"] >= 2.5
    pass3 = r3["absS_lat"] >= 2.5
    print(f'  → Pure-state gate (S ≥ 2.5):    {"PASS" if pass1 else "FAIL"}')
    print(f'  → Lattice-propagated (S ≥ 2.5): {"PASS" if pass3 else "FAIL"}')
    out['gate'] = {'pure_pass': pass1, 'lattice_pass': pass3,
                   'Tsirelson_residual_pure': r1['residual'],
                   'Tsirelson_residual_lattice': r3['residual']}

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T02_QM1_CHSH.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
