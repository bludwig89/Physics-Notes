"""
test_FG7d_baryon_singlet.py — colour-singlet three-quark (proton) construction
==============================================================================

Verifies `ca-simulation/ca_baryon.py`: the ε_{abc} three-quark operator is a
colour singlet with the proton's quantum numbers and Fermi statistics, and is
energetically bound by the exact string tension.

  BS1  ε_{abc} is totally antisymmetric (exact)
  BS2  det V = 1 for SU(3) gauge matrices (machine ε) — source of invariance
  BS3  colour-singlet gauge invariance  B → det(V)·B = B  under local V(x)
  BS4  zero total colour charge:  G^a|S⟩ = 0 ∀a;  Casimir C₂|S⟩ = 0
  BS5  proton uud quantum numbers exact (rational):  Q=+1, B=1, GMN consistent
  BS6  proton spin-flavour wavefunction is S₃-symmetric (exact)
  BS7  full wavefunction antisymmetric under quark exchange (Pauli/Fermi)
  BS8  energetic binding: V(R)=σR → ∞ (a free quark costs infinite energy)

Module under test:  ca-simulation/ca_baryon.py
Created:            2026-06-01
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_baryon as cb         # noqa: E402
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
        from fractions import Fraction
        if isinstance(obj, Fraction):
            return str(obj)
        return super().default(obj)


def _local_V_field(shape, rng):
    Vfield = np.zeros(shape + (3, 3), dtype=complex)
    flat = Vfield.reshape(-1, 3, 3)
    for n in range(flat.shape[0]):
        flat[n] = cs.su3_exp(rng.standard_normal(8))
    return Vfield


def _random_triplet(shape, rng):
    return (rng.standard_normal(shape + (3,))
            + 1j * rng.standard_normal(shape + (3,)))


# ═════════════════════════════════════════════════════════════════════

def test_BS1_epsilon_antisymmetric():
    """BS1 — ε_{abc} is totally antisymmetric (swap any pair → sign flip)."""
    eps = cb.levi_civita_3()
    worst = 0.0
    for (i, j) in ((0, 1), (0, 2), (1, 2)):
        axes = [0, 1, 2]
        axes[i], axes[j] = axes[j], axes[i]
        worst = max(worst, float(np.max(np.abs(np.transpose(eps, axes) + eps))))
    return {'test': 'BS1', 'name': 'ε_{abc} totally antisymmetric',
            'residual': worst, 'target': 0.0,
            'passed': bool(worst == 0.0),
            'description': 'colour wavefunction antisymmetry — exact'}


def test_BS2_det_unity():
    """BS2 — det V = 1 for SU(3) gauge matrices (machine ε)."""
    rng = np.random.default_rng(3)
    Vfield = _local_V_field((6, 6), rng)
    res = cb.det_residual_field(Vfield)
    return {'test': 'BS2', 'name': 'det V = 1 for SU(3) (source of invariance)',
            'residual': res, 'target': 1e-12,
            'passed': bool(res < 1e-12),
            'description': 'B → det(V)·B; det V=1 makes B invariant'}


def test_BS3_singlet_gauge_invariance():
    """BS3 — B = ε_{abc}q1^a q2^b q3^c is invariant under local SU(3) V(x)."""
    rng = np.random.default_rng(5)
    shape = (8, 8)
    t1 = _random_triplet(shape, rng)
    t2 = _random_triplet(shape, rng)
    t3 = _random_triplet(shape, rng)
    Vfield = _local_V_field(shape, rng)
    res = cb.singlet_gauge_residual(t1, t2, t3, Vfield)
    B = cb.baryon_field(t1, t2, t3)
    scale = float(np.max(np.abs(B)))
    rel = res / scale
    return {'test': 'BS3', 'name': 'Colour-singlet gauge invariance B→det(V)B=B',
            'residual': rel, 'target': 1e-12,
            'abs_residual': res, 'field_scale': scale,
            'passed': bool(rel < 1e-12),
            'description': 'the proton is colourless — exact under local SU(3)'}


def test_BS4_zero_colour_charge():
    """BS4 — singlet carries no colour charge: G^a|S⟩=0 ∀a; Casimir=0."""
    charge_res = cb.singlet_charge_residual()
    casimir = cb.singlet_casimir()
    res = max(charge_res, abs(casimir))
    return {'test': 'BS4', 'name': 'Zero colour charge: G^a|S⟩=0, C₂|S⟩=0',
            'residual': res, 'target': 1e-12,
            'charge_residual': charge_res, 'casimir': casimir,
            'passed': bool(res < 1e-12),
            'description': 'antisymmetric ε is the unique SU(3) singlet of 3⊗3⊗3'}


def test_BS5_proton_quantum_numbers():
    """BS5 — proton uud: Q=+1, B=1, Gell-Mann–Nishijima consistent (exact)."""
    qn = cb.proton_quantum_numbers()
    ok = qn['Q_int'] and qn['B_int'] and qn['gmn_consistent']
    return {'test': 'BS5', 'name': 'Proton uud quantum numbers (exact rational)',
            'residual': 0.0 if ok else 1.0, 'target': 0.0,
            'Q': str(qn['Q']), 'B': str(qn['B']), 'T3': str(qn['T3']),
            'gmn_consistent': qn['gmn_consistent'],
            'passed': bool(ok),
            'description': 'Q=2/3+2/3−1/3=1, B=1; fractions.Fraction exact'}


def test_BS6_spin_flavour_symmetric():
    """BS6 — proton spin-flavour wavefunction is fully S₃-symmetric (exact)."""
    psi = cb.proton_spin_flavour_wavefunction()
    res = cb.spin_flavour_symmetry_residual(psi)
    norm = float(np.sqrt(sum(a * a for a in psi.values())))
    return {'test': 'BS6', 'name': 'Proton spin-flavour wavefunction S₃-symmetric',
            'residual': res, 'target': 1e-12,
            'n_terms': len(psi), 'norm': norm,
            'passed': bool(res < 1e-12 and abs(norm - 1.0) < 1e-12),
            'description': 'SU(6) 56-plet symmetric combination, ‖·‖²=18'}


def test_BS7_fermi_antisymmetry():
    """BS7 — full wavefunction antisymmetric under quark exchange (Pauli)."""
    info = cb.total_wavefunction_antisymmetry()
    signs = info['total_exchange_sign']
    worst = max(abs(s + 1.0) for s in signs.values())
    worst = max(worst, info['spin_flavour_symmetry_residual'])
    return {'test': 'BS7', 'name': 'Total wavefunction antisymmetric (Fermi statistics)',
            'residual': worst, 'target': 1e-12,
            'colour_sign': info['colour_sign'],
            'total_exchange_sign': signs,
            'passed': bool(info['fermi_ok']),
            'description': 'colour(−1) × spin-flavour(+1) × space(+1) = −1'}


def test_BS8_energetic_binding():
    """BS8 — V(R)=σR → ∞: isolating one quark costs infinite energy."""
    beta = 2.0
    sigma, energies = cb.quark_isolation_energy(beta)
    Rs = sorted(energies)
    increasing = all(energies[Rs[i]] < energies[Rs[i + 1]] for i in range(len(Rs) - 1))
    # linearity: V(R)/R constant = σ
    ratios = [energies[R] / R for R in Rs]
    lin_dev = float(np.max(np.abs(np.array(ratios) - sigma)))
    ok = (sigma > 0) and increasing and (lin_dev < 1e-12)
    return {'test': 'BS8', 'name': 'Energetic binding V(R)=σR → ∞ (no free quark)',
            'residual': lin_dev, 'target': 1e-12,
            'sigma': float(sigma), 'energies': energies,
            'passed': bool(ok),
            'description': 'exact 2D string tension binds the colour singlet'}


# ─────────────────────────────────────────────────────────────────────

def main():
    t_start = time.perf_counter()
    tests = [
        test_BS1_epsilon_antisymmetric,
        test_BS2_det_unity,
        test_BS3_singlet_gauge_invariance,
        test_BS4_zero_colour_charge,
        test_BS5_proton_quantum_numbers,
        test_BS6_spin_flavour_symmetric,
        test_BS7_fermi_antisymmetry,
        test_BS8_energetic_binding,
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
            print(f"  [{'PASS' if ok else 'FAIL'}] {r.get('test'):5s}  "
                  f"{r.get('name'):62s}  res = {r.get('residual')}  "
                  f"({r['elapsed_s']:.3f} s)")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            results.append({'test': fn.__name__, 'passed': False, 'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FG-10 — colour-singlet three-quark (proton) construction',
        'date': '2026-06-01',
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
                       '..', 'test-results', 'FG10_baryon_singlet.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  → wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
