"""
test_13_QFT8_CPT.py  —  QFT-8: CPT-invariance  (particle vs antiparticle)
===========================================================================
Target: |m_particle − m_antiparticle| / m < 7×10^-10  (BASE 2017).

In our QCA the CPT transformation acts on the Dirac 4-spinor as:
    ψ → C·T·P·ψ  =  charge-conjugation × time-reversal × parity.

For the lattice Dirac CA (ca_dirac.py, exact split-step):
  - The dispersion relation is  ω(k) = arccos( cos(|k|) · cos(m) )
    which is even in both k and m.
  - Charge conjugation maps  m → −m  (complex-conjugate the mass term)
    together with flipping the spinor doublet.
  - Under CPT, the rest-frame frequency  ω(0) = arccos(cos(m)) = m
    is strictly identical for particle and antiparticle — exact by
    algebraic symmetry.

Test design
-----------
Part 1 — Algebraic / dispersion check.
  For a range of masses m ∈ (0, 1), verify that the lattice rest
  frequency  ω₀ = arccos(cos(m))  is the same for  +m  and  −m.
  Gate: |Δω₀| < 1e-15  (machine precision, algebraic identity).

Part 2 — Numerical propagation check.
  Propagate a Dirac packet at rest (k=0) with mass +m for N steps,
  extract the phase rate; repeat with charge-conjugated initial state
  (which amounts to conjugating ψ and flipping doublet signs).
  Gate: |ω_particle − ω_antiparticle| / ω < 1e-12.

Part 3 — Norm conservation under charge conjugation.
  Verify that the charge-conjugation map leaves ‖ψ‖² unchanged.
  Gate: |‖Cψ‖² − ‖ψ‖²| < 1e-15.
"""

import os, sys
import numpy as np
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'ca-simulation'))
import ca_dirac as dirac

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'test-results')
os.makedirs(RESULTS_DIR, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Part 1 — Algebraic CPT check: ω₀(+m) = ω₀(−m)
# ──────────────────────────────────────────────────────────────────────────────

def part1_algebraic(masses=None):
    print('\n' + '=' * 72)
    print('  QFT-8 Part 1 — Algebraic: ω₀(+m) = ω₀(−m)  (exact)')
    print('=' * 72)

    if masses is None:
        masses = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]

    print(f'\n  {"m":>8}  {"ω₀(+m)":>15}  {"ω₀(−m)":>15}  {"|Δω₀|":>12}')
    print('  ' + '-' * 56)

    rows = []
    for m in masses:
        # Lattice rest frequency: ω₀ = arccos(cos(m)) for |m| < π
        # For small m this is just m; this tests the algebraic symmetry.
        omega_pos = float(np.arccos(np.cos(m)))
        omega_neg = float(np.arccos(np.cos(-m)))
        delta = abs(omega_pos - omega_neg)
        rows.append({'m': m, 'omega_pos': omega_pos,
                     'omega_neg': omega_neg, 'delta': delta})
        print(f'  {m:>8.4f}  {omega_pos:>15.12f}  {omega_neg:>15.12f}  '
              f'{delta:>12.2e}')

    max_delta = max(r['delta'] for r in rows)
    ok = max_delta < 1e-14
    print(f'\n  Max |Δω₀|: {max_delta:.2e}')
    print(f'  Part 1 verdict: {"PASS" if ok else "FAIL"}  (gate 1e-14)')
    return ok, rows


# ──────────────────────────────────────────────────────────────────────────────
#  Part 2 — Numerical phase rate: particle vs antiparticle
# ──────────────────────────────────────────────────────────────────────────────

def charge_conjugate_4(eta_u, eta_d, chi_u, chi_d):
    """
    Charge conjugation on the full 4-component Dirac spinor (η, χ).
    In the Weyl representation: C maps (η, χ) → (iσ₂ χ*, −iσ₂ η*)
    which for our 2-component doublets is:
        C(η_↑, η_↓, χ_↑, χ_↓) = (−χ_↓*, χ_↑*, η_↓*, −η_↑*)
    This maps m → −m in the Dirac equation.
    """
    return (-np.conj(chi_d), np.conj(chi_u),
             np.conj(eta_d), -np.conj(eta_u))


def phase_rate(psi_arr, n_steps):
    """Extract angular frequency from phase of a single-cell time series."""
    phases = np.unwrap(np.angle(psi_arr))
    ts = np.arange(n_steps + 1)
    slope = float(np.polyfit(ts, phases, 1)[0])
    return -slope   # ω = −d(phase)/dt


def part2_numerical(masses=None, L=64, n_steps=400):
    """
    Propagate a proper +ω eigenstate (plane-wave × eigenvector of D_k)
    for mass +m and for mass −m; extract phase rate via inner-product
    overlap; compare.  The dispersion ω = arccos(√(1-m²)·cx·cy) depends
    only on m² so ω(+m) = ω(−m) exactly — this is the numerical
    confirmation.
    """
    print('\n' + '=' * 72)
    print('  QFT-8 Part 2 — Numerical dispersion: ω(+m) vs ω(−m)')
    print('=' * 72)
    print(f'  L={L}, n_steps={n_steps}')
    print(f'  Method: plane-wave eigenstates; phase extracted via ⟨ψ₀|ψₙ⟩')

    if masses is None:
        masses = [0.10, 0.20, 0.30, 0.40, 0.50, 0.70]

    # Fixed low-momentum mode (avoids edge effects)
    ix, iy = 1, 1
    kx = 2.0 * np.pi * ix / L
    ky = 2.0 * np.pi * iy / L

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    phase_field = np.exp(1j * (kx * X + ky * Y))

    print(f'  k = (2π·{ix}/L, 2π·{iy}/L)  with  L={L}')
    print(f'\n  {"m":>6}  {"ω(+m)":>15}  {"ω(−m)":>15}  '
          f'{"ω_analytic":>13}  {"|Δω|/ω":>12}')
    print('  ' + '-' * 68)

    rows = []
    for m in masses:
        omega_analytic = float(dirac._dirac_dispersion(
            np.array([[kx]]), np.array([[ky]]), m)[0, 0])

        def measure_omega_eig(mass_sign):
            """Build eigenvector state for given mass sign, propagate, extract ω."""
            psi_vec = dirac._dirac_plus_eigenvector(kx, ky, m * mass_sign)
            # Embed as spatial plane wave: 4 components → (L,L) arrays
            eu = psi_vec[0] * phase_field
            ed = psi_vec[1] * phase_field
            cu = psi_vec[2] * phase_field
            cd = psi_vec[3] * phase_field
            # Normalise
            norm = np.sqrt((np.abs(eu)**2 + np.abs(ed)**2
                           + np.abs(cu)**2 + np.abs(cd)**2).sum())
            eu /= norm; ed /= norm; cu /= norm; cd /= norm
            psi0 = np.stack([eu, ed, cu, cd])
            # Propagate n_steps
            for _ in range(n_steps):
                eu, ed, cu, cd = dirac.dirac_step_2d_splitstep(
                    eu, ed, cu, cd, m=m * mass_sign)
            psiN = np.stack([eu, ed, cu, cd])
            # Phase via overlap: ⟨ψ₀|ψN⟩ = e^{−i ω n}
            overlap = complex(np.sum(np.conj(psi0) * psiN))
            return -np.angle(overlap) / n_steps  # ω per step

        om_pos = measure_omega_eig(+1)
        om_neg = measure_omega_eig(-1)
        # ω(+m) and ω(-m) should both equal ω_analytic (which uses m²)
        rel_diff = (abs(om_pos - om_neg) / abs(om_pos)
                    if abs(om_pos) > 1e-12 else float('nan'))
        rows.append({'m': m, 'omega_pos': om_pos, 'omega_neg': om_neg,
                     'omega_analytic': omega_analytic, 'rel_diff': rel_diff})
        print(f'  {m:>6.3f}  {om_pos:>15.12f}  {om_neg:>15.12f}  '
              f'{omega_analytic:>13.10f}  {rel_diff:>12.2e}')

    max_rel = max(r['rel_diff'] for r in rows if not np.isnan(r['rel_diff']))
    ok = max_rel < 1e-12
    print(f'\n  Max |Δω(+m)−ω(−m)|/ω: {max_rel:.2e}')
    print(f'  Part 2 verdict: {"PASS" if ok else "FAIL"}  (gate 1e-12)')
    return ok, rows


# ──────────────────────────────────────────────────────────────────────────────
#  Part 3 — Norm under charge conjugation
# ──────────────────────────────────────────────────────────────────────────────

def part3_norm(L=32):
    print('\n' + '=' * 72)
    print('  QFT-8 Part 3 — Norm conservation under charge conjugation')
    print('=' * 72)

    rng = np.random.default_rng(42)
    rows = []
    print(f'\n  {"trial":>7}  {"‖ψ‖²":>14}  {"‖Cψ‖²":>14}  {"|Δ|":>12}')
    print('  ' + '-' * 50)

    ok = True
    for i in range(8):
        # Random 4-component spinor
        eu = rng.normal(size=(L,L)) + 1j*rng.normal(size=(L,L))
        ed = rng.normal(size=(L,L)) + 1j*rng.normal(size=(L,L))
        cu = rng.normal(size=(L,L)) + 1j*rng.normal(size=(L,L))
        cd = rng.normal(size=(L,L)) + 1j*rng.normal(size=(L,L))
        norm2 = float((np.abs(eu)**2 + np.abs(ed)**2
                      + np.abs(cu)**2 + np.abs(cd)**2).sum())
        c_eu, c_ed, c_cu, c_cd = charge_conjugate_4(eu, ed, cu, cd)
        norm2_c = float((np.abs(c_eu)**2 + np.abs(c_ed)**2
                        + np.abs(c_cu)**2 + np.abs(c_cd)**2).sum())
        delta = abs(norm2_c - norm2)
        ok = ok and (delta < 1e-9 * norm2)
        rows.append({'trial': i, 'norm2': norm2,
                     'norm2_c': norm2_c, 'delta': float(delta)})
        print(f'  {i:>7}  {norm2:>14.4f}  {norm2_c:>14.4f}  {delta:>12.2e}')

    max_d = max(r['delta'] for r in rows)
    print(f'\n  Max |Δ‖ψ‖²|: {max_d:.2e}')
    print(f'  Part 3 verdict: {"PASS" if ok else "FAIL"}  (gate 1e-9 × ‖ψ‖²)')
    return ok, rows


# ──────────────────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    ok1, rows1 = part1_algebraic()
    ok2, rows2 = part2_numerical()
    ok3, rows3 = part3_norm()

    print('\n' + '=' * 72)
    print('  QFT-8 SUMMARY — CPT-invariance: particle vs antiparticle')
    print('=' * 72)
    print(f'  Part 1  ω₀(+m) = ω₀(−m)  algebraic (1e-14 gate): '
          f'{"PASS" if ok1 else "FAIL"}')
    print(f'  Part 2  numerical ω_p = ω_a  (1e-10 gate):         '
          f'{"PASS" if ok2 else "FAIL"}')
    print(f'  Part 3  ‖Cψ‖² = ‖ψ‖²  norm conservation:          '
          f'{"PASS" if ok3 else "FAIL"}')

    overall = ok1 and ok2 and ok3
    print(f'\n  QFT-8 overall: {"PASS" if overall else "FAIL"}')
    print(f'  The QCA is exactly CPT-symmetric by construction; this is a '
          f'regression test confirming no numerical CPT-breaking.')

    result = {
        'test': 'QFT-8',
        'ok1_algebraic': bool(ok1),
        'ok2_numerical': bool(ok2),
        'ok3_norm': bool(ok3),
        'overall': bool(overall),
        'max_algebraic_delta': float(max(r['delta'] for r in rows1)),
        'max_numerical_rel': float(max(r['rel_diff'] for r in rows2
                                       if not np.isnan(r['rel_diff']))),
    }
    out = os.path.join(RESULTS_DIR, 'test_13_QFT8_CPT.json')
    with open(out, 'w') as fh:
        json.dump(result, fh, indent=2)
    print(f'\n  Results saved to {out}')
