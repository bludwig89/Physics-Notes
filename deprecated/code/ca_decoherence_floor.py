# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_decoherence_floor.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qi_decoherence_floor.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_decoherence_floor.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_decoherence_floor.py  —  intrinsic-decoherence / unitarity floor (F227)
==========================================================================

Route 4 of the QC-empirical thread (docs/roadmaps/qc-routes-3-4-prompt.md).

Question
--------
If the lattice is physical, does a long quantum computation show any intrinsic
departure from perfect unitarity — a minimum decoherence rate, a maximum
entangling velocity (Lieb–Robinson bound = c_lat), or a gate-error floor — set
by the fundamental spacing a and c_lat?  F222 finds the register's norm drift is
pure floating point (~1e-13): the model asserts NO intrinsic floor.  This module
makes that assertion quantitative and bounds it against experiment.

Results established here
------------------------
1. Intrinsic unitarity-violation rate.  The emergent gates are exactly unitary,
   so at the level where the model reproduces QM the intrinsic decoherence is
   ZERO.  The only way discreteness could induce non-unitarity is through
   Lorentz-violating (LIV) operators in the underlying walk, and F130 proves
   these are RG-IRRELEVANT (λ_n = b^{-n}, n≥2).  Hence any residual rate is at
   most Planck-suppressed:
       Γ_intrinsic ≲ (E/ħ)(E/E_lat)²  =  E³/(ħ E_lat²)      (F130 n=2 leading),
   with the softer single-operator ceiling  Γ ≲ E²/(ħ E_lat) = E² τ/ħ².
   Both are ≥10 orders below the deepest measured decoherence.

2. Lieb–Robinson / maximum-entangling velocity.  The fundamental signalling
   speed of the substrate is c_lat = 1/√3 (F26/F180, exact — slope identity
   dΩ/d|k| = 1/√3).  The QC sector inherits this as its hard light cone; the
   emergent super-exchange chain saturates a SMALLER velocity v_eff ~ J·(a/τ) <
   c_lat (super-exchange is 2nd-order/virtual), so correlations never outrun the
   lattice light cone.

3. Confrontation with collapse models & experiment.  The predicted floor sits
   far below CSL, Diósi–Penrose, atomic-clock, and interferometry bounds — the
   model is a UNITARY theory with no objective collapse, consistent with all
   current null results.

4. The one non-Planck-suppressed native channel is the EMERGENT doublon leakage
   d=(2t/U)² (F220/F225) — a material-scale (~1e-3) two-site-Hubbard effect,
   ~20+ orders above the fundamental discreteness floor; kept strictly separate.

Pure numpy; the LR light-cone uses the native exchange gate on a flat state
vector (plain complex linear algebra — safe per the CLAUDE.md chiral note).
"""
from __future__ import annotations
import math
import numpy as np
from casim.constants import c_lat

try:
    import ca_entanglement as _E
except Exception:  # pragma: no cover
    _E = None

# ─────────────────────────── SI bridge (F107/F123) ─────────────────────
TAU_S = 2.05366e-43            # fundamental CA tick [s]
A_M = 1.06638e-34             # fundamental cell size [m]
HBAR_EV_S = 6.582119569e-16   # ħ [eV·s]
E_LAT_EV = HBAR_EV_S / TAU_S   # lattice energy ħ/τ ≈ 3.205e27 eV (F119 hierarchy scale)
E_PLANCK_EV = 1.22089e28      # Planck energy [eV]
C_LAT = c_lat  # F26

# collapse-model reference values (see finding for citations)
CSL_LAMBDA_GRW = 1e-16        # s^-1, GRW original
CSL_LAMBDA_ADLER = 1e-8       # s^-1, Adler (now excluded by X-ray tests)
CSL_RC_M = 1e-7               # m
DP_R0_LOWER_M = 4e-10         # m, current DP lower bound (~4 Å)

# experimental coherence references (see finding for citations)
CLOCK_COHERENCE_S = 118.0     # Sr optical lattice clock T2* (2025)
TRANSMON_T2_S = 1.06e-3       # superconducting transmon T2,echo record (2025)


# ═══════════════════════════════════════════════════════════════════════
#  1. Intrinsic unitarity-violation rate (zero or Planck-suppressed)
# ═══════════════════════════════════════════════════════════════════════
def intrinsic_rate_liv(E_eV: float) -> float:
    """Leading LIV-suppressed intrinsic decoherence rate [s^-1]:
       Γ ≲ (E/ħ)(E/E_lat)² = E³ /(ħ E_lat²)   (F130: leading LIV op n=2)."""
    return (E_eV / HBAR_EV_S) * (E_eV / E_LAT_EV) ** 2


def intrinsic_rate_conservative(E_eV: float) -> float:
    """Softer single-operator ceiling  Γ ≲ E²/(ħ E_lat) = E² τ/ħ² [s^-1]
    (one power of Planck suppression only — a deliberately pessimistic bound)."""
    return E_eV ** 2 / (HBAR_EV_S * E_LAT_EV)


def unitary_floor_is_zero(engine_norm_drift: float = 1e-13) -> dict:
    """The emergent gates are exact unitaries ⇒ the effective-theory floor is
    identically zero; the observed register norm drift (F222 ~1e-13) is
    floating-point, not physics."""
    return {'effective_theory_floor': 0.0,
            'observed_norm_drift_F222': engine_norm_drift,
            'interpretation': 'floating-point round-off, not intrinsic non-unitarity'}


# ═══════════════════════════════════════════════════════════════════════
#  2. Lieb–Robinson / maximum entangling velocity
# ═══════════════════════════════════════════════════════════════════════
def fundamental_dispersion_slope(dk: float = 1e-6) -> float:
    """dΩ/d|k| at k→0 for the on-axis exact dispersion Ω(k)=|k|/√3 (F105/F26/F180).
    Returns the group velocity = c_lat = 1/√3 (exact)."""
    Omega = lambda k: k / math.sqrt(3.0)     # closed-form on-axis (F105)
    return (Omega(dk) - Omega(0.0)) / dk


def exchange_chain_lightcone(nqubits: int = 11, theta: float = math.pi / 16,
                             nlayers: int = 2):
    """Evolve a 1-D chain under nearest-neighbour native exchange gates and show
    the STRICT Lieb–Robinson causal cone: starting from the Néel PRODUCT
    |0101…⟩, the connected correlation C(r,t)=⟨Z_0 Z_r⟩−⟨Z_0⟩⟨Z_r⟩ is EXACTLY
    zero (machine precision) for r > 4t.  Each brick-wall tick (even bonds then
    odd bonds) spreads a single operator by 2 cells, so the two-point correlator
    — built from two operators, each Heisenberg-evolved — has a hard cone of 4t.
    A finite Lieb–Robinson cone (the QC-sector analogue of the F180 signal
    speed), not instantaneous propagation.

    Returns (times, [(front, cone_4t)…], max_outside_cone_correlation)."""
    if _E is None:
        raise RuntimeError("ca_entanglement not importable; add ca-simulation to sys.path")
    n = nqubits
    kets = [_E.KET0 if i % 2 == 0 else _E.KET1 for i in range(n)]
    psi = _E.product_state(kets)
    G = _E.exchange_gate(theta)
    SZ = _E.SZ

    def z_exp(p, q):
        return float(np.real(np.conj(p) @ _E.apply_gate(p, SZ, [q], n)))

    def zz_exp(p, q0, q1):
        v = _E.apply_gate(p, SZ, [q0], n)
        v = _E.apply_gate(v, SZ, [q1], n)
        return float(np.real(np.conj(p) @ v))

    times, fronts, outside = [], [], 0.0
    for t in range(1, nlayers + 1):
        for parity in (0, 1):                      # brick-wall tick
            for q in range(parity, n - 1, 2):
                psi = _E.apply_gate(psi, G, [q, q + 1], n)
        z0 = z_exp(psi, 0)
        front = 0
        cone = 4 * t
        for r in range(1, n):
            c = abs(zz_exp(psi, 0, r) - z0 * z_exp(psi, r))
            if c > 1e-6:
                front = r
            if r > cone:                           # strictly outside the cone
                outside = max(outside, c)
        times.append(t); fronts.append((front, cone))
    return times, fronts, float(outside)


# ═══════════════════════════════════════════════════════════════════════
#  3. Confrontation with collapse models & experiment
# ═══════════════════════════════════════════════════════════════════════
def confront_experiment(E_eV: float = 1.8) -> dict:
    """Compare the predicted intrinsic floor against measured decoherence rates
    and collapse-model rates.  E_eV default = optical clock transition (~1.8 eV)."""
    gamma_liv = intrinsic_rate_liv(E_eV)             # model's actual prediction
    gamma_cons = intrinsic_rate_conservative(E_eV)   # deliberately pessimistic ceiling
    clock_rate = 1.0 / CLOCK_COHERENCE_S
    transmon_rate = 1.0 / TRANSMON_T2_S
    return {
        'E_eV': E_eV,
        'gamma_intrinsic_liv_s^-1': gamma_liv,
        'gamma_intrinsic_conservative_s^-1': gamma_cons,
        'measured_clock_decoherence_s^-1': clock_rate,
        'measured_transmon_decoherence_s^-1': transmon_rate,
        'CSL_GRW_s^-1': CSL_LAMBDA_GRW,
        'CSL_Adler_s^-1_excluded': CSL_LAMBDA_ADLER,
        # conservative ceiling vs MEASURED decoherence (both experimental floors):
        'conservative_orders_below_clock': math.log10(clock_rate / gamma_cons),
        'conservative_orders_below_transmon': math.log10(transmon_rate / gamma_cons),
        # model's actual (LIV-suppressed) rate vs collapse-model rates:
        'liv_orders_below_CSL_GRW': math.log10(CSL_LAMBDA_GRW / gamma_liv),
        'liv_orders_below_CSL_Adler': math.log10(CSL_LAMBDA_ADLER / gamma_liv),
        'note_CSL_is_per_nucleon': ('CSL λ is a per-nucleon localisation rate; the '
                                    'model has NO such stochastic term — it is unitary'),
        'verdict': ('intrinsic floor Planck-suppressed below ALL measured decoherence '
                    'and below the collapse-model rates; model is unitary with no '
                    'objective collapse (no DP/CSL term)'),
    }


# ═══════════════════════════════════════════════════════════════════════
#  4. Emergent doublon leakage vs the fundamental floor (kept separate)
# ═══════════════════════════════════════════════════════════════════════
def doublon_leakage(tU: float) -> float:
    """Emergent field-native leakage d=(2t/U)² (F220/F225 leading order) — a
    material-scale two-site-Hubbard effect, NOT a discreteness floor."""
    return (2.0 * tU) ** 2


def floor_vs_leakage_separation(E_eV: float = 1.8, tU: float = 0.018) -> dict:
    """Per-gate comparison: emergent doublon-leakage probability vs the
    fundamental discreteness non-unitarity per gate (Γ·τ_gate, τ_gate≈ħ/E)."""
    leak = doublon_leakage(tU)                       # ~1e-3 at device U/t≈55
    tau_gate_s = HBAR_EV_S / E_eV                     # ~ħ/E gate time
    intrinsic_per_gate = intrinsic_rate_liv(E_eV) * tau_gate_s
    return {
        'doublon_leakage_per_gate': leak,
        'intrinsic_nonunitarity_per_gate': intrinsic_per_gate,
        'separation_orders': math.log10(leak / intrinsic_per_gate),
        'note': 'emergent (material-scale) vs fundamental (Planckian) — distinct channels',
    }


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    print("dispersion slope (=c_lat):", fundamental_dispersion_slope(), C_LAT)
    print("confront:", confront_experiment())
    t, f, v = exchange_chain_lightcone()
    print("exchange-chain front:", list(zip(t, f)), "v_eff cells/tick:", v)
    print("separation:", floor_vs_leakage_separation())
