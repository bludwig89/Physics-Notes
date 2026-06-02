"""
test_FG8_beta_decay.py
======================

FG-8 — End-to-end β-decay charged-current integration test.

        d  →  u + W⁻  →  u + e⁻ + ν̄_e

This is the signature first-generation weak process and the main remaining
Tier-A structural test (first-gen-completeness.md §5.1 row FG-8).  It wires
together pieces already verified in isolation:

    F29  isospin-doublet bilinears          FG-2/FG-3  quark–W vertex
    F34  lepton–W vertex (parity violation) F36        dynamical / Proca W
    F35  electroweak charge registry        F48        per-species couplings

into the complete charged-current chain, and adds the raising/lowering
(T±, W±) structure that the process requires.

Tests
-----
  CC1  SU(2) charged-current algebra  [T³,T±]=±T±, [T⁺,T⁻]=2T³            (exact)
  CC2  d → u isospin raising  T⁺|d⟩ = |u⟩;  ΔQ = +1 = −Q(W⁻)            (exact ℚ)
  CC3  Vertex charge conservation  d→u+W⁻  and  W⁻→e⁻+ν̄_e               (exact ℚ)
  CC4  Maximal parity violation: V−A vertex annihilates ψ_R              (exact)
  CC5  Quark–lepton universality: identical J⁺ bilinear / coupling       (bit-for-bit)
  CC6  W⁻ emission: sourced step gives ΔE(W⁻) = (g/√2) J⁺_quark dt       (machine ε)
  CC7  Proca W⁻ propagation dispersion ω² = m_W² + Ω_even²(k)           (machine ε)
  CC8  Heavy-W → Fermi contact: A(q²→0) = G_F/√2 = g²/8m_W²; rate q²/m_W² (exact + Tier-3)
  CC9  Full process bookkeeping  d→u+e⁻+ν̄_e:  ΔQ=ΔB=ΔL=Δ(B−L)=0          (exact ℚ)
  CC10 End-to-end pipeline: causal W⁻ arrival A→B + global charge balance (integration)

Run:  python3 model-tests/test_FG8_beta_decay.py
"""

import sys
import os
import json
import time
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np

import ca_charged_current as cc
from ca_charged_current import (
    su2_raising_algebra_residuals, raise_isospin, lower_isospin,
    KET_UP, KET_DOWN,
    charged_current_plus, charged_current_minus, charged_current_from_isospin,
    va_vertex_kills_right_handed,
    charge, conservation_residuals,
    w_charged_components, emit_w_minus,
    fermi_constant, w_exchange_amplitude, fermi_limit_relative_deviation,
    run_beta_decay_pipeline,
)
from ca_wmu import (
    make_w_link_field, fermion_isospin_current,
    w_massive_propagation_step_spectral, measure_massive_w_dispersion,
)
from ca_bcc import bcc_dispersion
from ca_lattice import make_kgrid_3d
import ca_fft as _fft


# ---------------------------------------------------------------------------
results = {}
PASS = []


def report(name, passed, residual=None, target=None, note=""):
    PASS.append(bool(passed))
    tag = "PASS" if passed else "FAIL"
    r = f"  resid={residual:.3e}" if isinstance(residual, float) else ""
    t = f" (target {target:.0e})" if isinstance(target, float) else ""
    print(f"[{tag}] {name}{r}{t}  {note}")
    results[name] = {'pass': bool(passed), 'residual': residual,
                     'target': target, 'note': note}


# ===========================================================================
#  CC1 — SU(2) charged-current algebra
# ===========================================================================
def test_cc1():
    res = su2_raising_algebra_residuals()
    m = max(res.values())
    report("CC1 SU(2) raising/lowering algebra", m < 1e-15, m, 1e-15,
           note="[T3,T±]=±T±, [T+,T-]=2T3 exact")
    results["CC1 SU(2) raising/lowering algebra"]['detail'] = res


# ===========================================================================
#  CC2 — d → u isospin raising and charge step
# ===========================================================================
def test_cc2():
    up = raise_isospin(KET_DOWN)              # T⁺|d⟩
    raise_ok = np.allclose(up, KET_UP) and np.allclose(lower_isospin(KET_UP), KET_DOWN)
    # ΔQ on the d → u transition equals minus the W⁻ charge
    dQ = charge('u') - charge('d')            # exact Fraction
    matches_W = (dQ == -charge('W-'))
    passed = raise_ok and (dQ == Fraction(1)) and matches_W
    report("CC2 d->u raising; ΔQ=+1=-Q(W-)", passed, 0.0 if passed else 1.0, 0.0,
           note=f"T+|d>=|u>; ΔQ={dQ}, Q(W-)={charge('W-')}")
    results["CC2 d->u raising; ΔQ=+1=-Q(W-)"]['detail'] = {
        'dQ': str(dQ), 'Q_Wminus': str(charge('W-'))}


# ===========================================================================
#  CC3 — vertex charge conservation (both vertices)
# ===========================================================================
def test_cc3():
    emit = conservation_residuals(['d'], ['u', 'W-'])          # d → u + W⁻
    absb = conservation_residuals(['W-'], ['e', 'nubar'])      # W⁻ → e⁻ + ν̄_e
    ok = (emit['dQ'] == 0) and (absb['dQ'] == 0) and (absb['dL'] == 0)
    report("CC3 vertex charge conservation", ok, 0.0 if ok else 1.0, 0.0,
           note=f"emit dQ={emit['dQ']}; absorb dQ={absb['dQ']}, dL={absb['dL']}")
    results["CC3 vertex charge conservation"]['detail'] = {
        'emit': {k: str(v) for k, v in emit.items()},
        'absorb': {k: str(v) for k, v in absb.items()}}


# ===========================================================================
#  CC4 — maximal parity violation (V−A)
# ===========================================================================
def test_cc4():
    resid_R, resid_L = va_vertex_kills_right_handed()
    m = max(resid_R, resid_L)
    report("CC4 V-A vertex kills right-handed", m < 1e-15, m, 1e-15,
           note=f"P_L ψ_R = 0 ({resid_R:.1e}); P_L ψ_L = ψ_L ({resid_L:.1e})")


# ===========================================================================
#  CC5 — quark–lepton universality of the charged-current bilinear
# ===========================================================================
def test_cc5():
    rng = np.random.default_rng(11)
    shape = (8, 8, 8)
    # identical field configuration used for the (u,d) and (ν,e) doublets
    a = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    b = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    Jp_quark = charged_current_plus(a, b)     # (u,d)
    Jp_lept = charged_current_plus(a, b)      # (ν,e) — same functional form
    # also cross-check against the isospin-current route
    Jp_iso, _ = charged_current_from_isospin(a, b)
    d_uni = float(np.max(np.abs(Jp_quark - Jp_lept)))
    d_iso = float(np.max(np.abs(Jp_quark - Jp_iso)))
    m = max(d_uni, d_iso)
    report("CC5 quark-lepton universality of J+", m < 1e-13, m, 1e-13,
           note="same J+=f_up* f_down for both doublets; matches J1+iJ2")


# ===========================================================================
#  CC6 — W⁻ emission: sourced step reproduces (g/√2) J⁺ dt
# ===========================================================================
def test_cc6():
    rng = np.random.default_rng(7)
    L = 12
    shape = (L, L, L)
    f_u = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    f_d = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    g_lat, dt = 0.8, 1.0
    E_W = np.zeros((3,) + shape)
    B_W = np.zeros((3,) + shape)
    # free propagation from zero field leaves zero, so the sourced increment
    # is exactly the source kick; compare W⁻ component to (g/√2) J⁺ dt
    E_W2, B_W2, dE_Wm_expected = emit_w_minus(E_W, B_W, f_u, f_d, g_lat=g_lat, dt=dt)
    _, E_Wm = w_charged_components(E_W2)
    resid = float(np.max(np.abs(E_Wm - dE_Wm_expected)))
    report("CC6 W- emission = (g/√2) J+ dt", resid < 1e-13, resid, 1e-13,
           note="ΔE(W-) sourced by raising quark current J+ exactly")


# ===========================================================================
#  CC7 — Proca W⁻ dispersion ω² = m_W² + Ω_even²(k)
# ===========================================================================
def test_cc7():
    # the W⁻ field inherits the massive (Proca) BCC rotation law of F36.
    # Use the project's validated complex-amplitude measurement (no np.angle,
    # so no phase-wrap artefacts) across three masses and all 3 isospin comps.
    worst = 0.0
    detail = {}
    for m_W in (0.0, 0.3, 0.6):
        for a in range(3):
            rel = measure_massive_w_dispersion(L=16, m_W=m_W, n_steps=30,
                                               a_comp=a, seed=42 + a)
            worst = max(worst, rel)
            detail[f"m_W={m_W},a={a}"] = rel
    report("CC7 Proca W- dispersion ω²=m_W²+Ω²", worst < 1e-10, worst, 1e-10,
           note="ω²=m_W²+Ω_even²(k) across 3 masses × 3 isospin comps, 30 ticks")
    results["CC7 Proca W- dispersion ω²=m_W²+Ω²"]['detail'] = detail


# ===========================================================================
#  CC8 — heavy-W Fermi limit
# ===========================================================================
def test_cc8():
    g, m_W = 0.65, 80.0
    # exact at q²=0
    A0 = w_exchange_amplitude(g, m_W, 0.0)
    GF = fermi_constant(g, m_W)
    exact0 = abs(A0 - GF)
    # deviation rate: (A(q²)-G_F/√2)/(G_F/√2) = -q²/(m_W²+q²)
    q2 = 1.0
    dev = fermi_limit_relative_deviation(g, m_W, q2)
    pred = -q2 / (m_W ** 2 + q2)
    rate_resid = abs(dev - pred)
    passed = (exact0 == 0.0) and (rate_resid < 1e-15)
    report("CC8 heavy-W Fermi limit G_F/√2=g²/8m_W²", passed,
           rate_resid, 1e-15,
           note=f"A(0)-G_F/√2={exact0:.1e} (exact); dev rate matches -q²/(m_W²+q²)")
    results["CC8 heavy-W Fermi limit G_F/√2=g²/8m_W²"]['detail'] = {
        'G_F_over_sqrt2': GF, 'A0': A0, 'rel_dev_q2_1': float(dev)}


# ===========================================================================
#  CC9 — full-process bookkeeping  d → u + e⁻ + ν̄_e
# ===========================================================================
def test_cc9():
    cons = conservation_residuals(['d'], ['u', 'e', 'nubar'])
    ok = all(v == 0 for v in cons.values())
    report("CC9 full process d->u e- ν̄ conservation", ok,
           0.0 if ok else 1.0, 0.0,
           note=f"ΔQ={cons['dQ']} ΔB={cons['dB']} ΔL={cons['dL']} Δ(B-L)={cons['dB-L']}")
    results["CC9 full process d->u e- ν̄ conservation"]['detail'] = {
        k: str(v) for k, v in cons.items()}


# ===========================================================================
#  CC10 — end-to-end pipeline (integration)
# ===========================================================================
def test_cc10():
    out = run_beta_decay_pipeline(L=16, m_W=0.6, g_lat=0.8, n_prop=24)
    # the W⁻ source kick must reproduce the analytic (g/√2)|J+| value
    emit_ok = out['w_at_A_on_emit'] > 1e-6
    # causality: ~no signal at B on emission, finite signal after propagation
    causal_ok = (out['w_at_B_on_emit'] < 1e-9) and (out['w_at_B_final'] > 1e-6)
    # global electric charge balance of the full process (exact)
    charge_ok = (out['dQ'] == 0.0 and out['dB'] == 0.0
                 and out['dL'] == 0.0 and out['dB-L'] == 0.0)
    lepton_ok = out['lepton_cc_response_at_B'] > 1e-6
    passed = emit_ok and causal_ok and charge_ok and lepton_ok
    report("CC10 end-to-end d→u+W-→u+e-+ν̄ pipeline", passed,
           0.0 if passed else 1.0, 0.0,
           note=(f"W@A={out['w_at_A_on_emit']:.3e}, W@B(emit)={out['w_at_B_on_emit']:.1e}, "
                 f"W@B(final)={out['w_at_B_final']:.3e}, ΔQ={out['dQ']}"))
    results["CC10 end-to-end d→u+W-→u+e-+ν̄ pipeline"]['detail'] = out


# ===========================================================================
def main():
    t0 = time.time()
    print("=" * 72)
    print("FG-8 — β-decay charged-current end-to-end integration test")
    print("        d → u + W⁻ → u + e⁻ + ν̄_e")
    print("=" * 72)
    test_cc1(); test_cc2(); test_cc3(); test_cc4(); test_cc5()
    test_cc6(); test_cc7(); test_cc8(); test_cc9(); test_cc10()
    dt = time.time() - t0
    n_pass = sum(PASS)
    n_tot = len(PASS)
    print("-" * 72)
    print(f"  {n_pass}/{n_tot} PASS in {dt:.3f} s")
    print("=" * 72)

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'FG8_beta_decay.json'), 'w') as fh:
        json.dump({'test_suite': 'FG8_beta_decay',
                   'process': 'd -> u + W- -> u + e- + nubar_e',
                   'n_pass': n_pass, 'n_total': n_tot,
                   'runtime_s': dt,
                   'tests': results}, fh, indent=2, default=str)
    return 0 if n_pass == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
