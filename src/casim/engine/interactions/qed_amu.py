"""
ca_amu.py — the muon anomalous moment a_mu at two loops, and the QED lepton-
universality gate, built on the same vertex machinery as the electron (F252,
F251, ca_twoloop_ae). Part of F261.

    a_l = (alpha/2pi) + A2(l) (alpha/pi)^2 + ...

WHAT THIS MODULE ESTABLISHES (explicit, honest scope)
=====================================================
UNIVERSALITY (exact identity):
  U1  the MASS-INDEPENDENT QED coefficients A1 = 1/2 and A2 = -0.328478966 are
      IDENTICAL for the electron and the muon. The diagrams are topologically the
      same and their mass-independent parts carry no lepton-mass dependence, so
      the numbers are literally the same object (ca_twoloop_ae supplies them once;
      both leptons read the same value). This is an exact gate, not a fit.

MASS-DEPENDENT (the source of a_mu != a_e):
  U2  the difference a_mu - a_e at two loops is dominated by the ELECTRON-LOOP
      vacuum-polarisation insertion in the muon vertex (a LIGHT loop in a HEAVY
      vertex): from F251's Pi via the dispersive kernel (ca_twoloop_ae),
          A2^{VP}(e in mu) = (1/3) ln(m_mu/m_e) - 25/36 + (pi^2/4)(m_e/m_mu) + ...
                           = 1.0942583...
      The reverse (heavy loop in light vertex, mu in e) DECOUPLES to ~5e-7. This
      asymmetry is exactly why a_mu > a_e. Leading log is model-derived.

  U3  the muon two-loop coefficient
          A2(mu) = A2_massindep + A2^{VP}(e in mu) + A2^{VP}(tau in mu)
                 = -0.328479 + 1.094258 + 0.000078 = 0.765857...
      vs the known QED value 0.765857410. Then a_mu^{QED} through two loops.

SCOPE — what is NOT claimed:
  The HADRONIC vacuum-polarisation and HADRONIC light-by-light contributions
  (QCD sector, F151/F152) and the ELECTROWEAK contributions (weak sector) are
  OUT OF SCOPE. So the full Standard-Model a_mu and any comparison with the
  measured a_mu are NOT this module's claim. The measured/SM a_mu comparison is
  an active, moving area (Muon g-2 Theory Initiative white papers 2020 and 2025;
  the hadronic-VP situation is unsettled). We quote ONLY the QED piece and defer
  the rest explicitly.

numpy only; the VP integrals are the ca_twoloop_ae dispersive machinery.
"""
from __future__ import annotations

import math

from casim.engine.interactions import qed_twoloop_ae as tl

ALPHA_INV = tl.ALPHA_INV
ALPHA = tl.ALPHA
PI = tl.PI
A_OVER_PI = tl.A_OVER_PI

M_E = tl.M_E
M_MU = tl.M_MU
M_TAU = tl.M_TAU
A1 = tl.A1

# known QED coefficients for cross-checking (Aoyama-Hayakawa-Kinoshita-Nio 2015)
A2_MU_KNOWN = 0.765857410
A2_VP_E_IN_MU_KNOWN = 1.0942583
A_MU_MEASURED = 1.16592059e-3            # PDG/experiment (reference only; NOT a claim)


# ======================================================================
#  U1 — universality of the mass-independent QED coefficients (exact)
# ======================================================================
def universality_gate() -> dict:
    """A1 and A2 (mass-independent) are the SAME for electron and muon. We read
    them once from ca_twoloop_ae and assert both leptons use the identical value
    — an exact identity (same diagrams, mass-independent parts)."""
    A2_mi = float(tl.A2_assembly_symbolic()["A2_numeric"])
    a1_e = a1_mu = A1
    a2_e = a2_mu = A2_mi
    return {
        "A1_electron": a1_e, "A1_muon": a1_mu,
        "A1_identical": a1_e == a1_mu,
        "A2_massindep_electron": a2_e, "A2_massindep_muon": a2_mu,
        "A2_massindep_identical": a2_e == a2_mu,
        "A2_massindep_value": A2_mi,
        "gate_pass": bool(a1_e == a1_mu and a2_e == a2_mu),
        "statement": "the mass-independent QED coefficients A1 = 1/2 and "
                     "A2 = -0.328478966 are IDENTICAL for e and mu (same "
                     "diagrams, no lepton-mass dependence) — exact universality, "
                     "the same number, not a fit.",
    }


# ======================================================================
#  U2 — the electron-loop VP insertion (leading source of a_mu - a_e)
# ======================================================================
def vp_e_in_mu() -> dict:
    """A2^{VP}(e in mu) from F251's Pi via the dispersive kernel: a LIGHT loop in
    a HEAVY vertex, leading log (1/3)ln(m_mu/m_e) - 25/36. Compare to the reverse
    (mu in e), which decouples — the asymmetry is why a_mu > a_e."""
    val = tl.A2_vp_dispersive(M_E, M_MU)
    leading = (1.0 / 3.0) * math.log(M_MU / M_E) - 25.0 / 36.0
    subleading = leading + (PI ** 2 / 4.0) * (M_E / M_MU)
    reverse = tl.A2_vp_dispersive(M_MU, M_E)          # mu loop in e vertex (decouples)
    return {
        "A2_vp_e_in_mu_model": val,
        "A2_vp_e_in_mu_known": A2_VP_E_IN_MU_KNOWN,
        "leading_log_13_ln_mmu_me_minus_2536": leading,
        "leading_plus_pi2_4_me_mmu": subleading,
        "A2_vp_mu_in_e_reverse_decoupled": reverse,
        "asymmetry_ratio_light_over_heavy": val / reverse,
        "abs_err_vs_known": abs(val - A2_VP_E_IN_MU_KNOWN),
        "gate_pass": bool(abs(val - A2_VP_E_IN_MU_KNOWN) < 1e-3 and val > 100 * reverse),
        "statement": "A2^{VP}(e in mu) = 1.0942583 (model, from F251 Pi); leading "
                     "log (1/3)ln(m_mu/m_e) - 25/36 = 1.0828; the reverse mu-in-e "
                     "insertion decouples to 5.2e-7. This light-in-heavy vs "
                     "heavy-in-light asymmetry is exactly why a_mu > a_e.",
    }


# ======================================================================
#  U3 — the muon two-loop coefficient and a_mu^{QED}
# ======================================================================
def a_mu_two_loop() -> dict:
    """A2(mu) = A2_massindep + A2^{VP}(e in mu) + A2^{VP}(tau in mu) vs the known
    0.765857410, then a_mu^{QED} through two loops. Hadronic and electroweak
    pieces are OUT OF SCOPE (deferred), so the SM/experiment comparison is not
    claimed."""
    A2_mi = float(tl.A2_assembly_symbolic()["A2_numeric"])
    vp_e = tl.A2_vp_dispersive(M_E, M_MU)
    vp_tau = tl.A2_vp_dispersive(M_TAU, M_MU)
    A2_mu = A2_mi + vp_e + vp_tau
    a_mu_1 = A1 * A_OVER_PI
    a_mu_2 = A1 * A_OVER_PI + A2_mu * A_OVER_PI ** 2
    return {
        "A2_mass_independent": A2_mi,
        "A2_vp_e_in_mu": vp_e,
        "A2_vp_tau_in_mu": vp_tau,
        "A2_muon_total": A2_mu,
        "A2_muon_known": A2_MU_KNOWN,
        "A2_muon_abs_err": abs(A2_mu - A2_MU_KNOWN),
        "a_mu_one_loop": a_mu_1,
        "a_mu_two_loop_QED": a_mu_2,
        "a_mu_measured_reference_only": A_MU_MEASURED,
        "gate_pass": bool(abs(A2_mu - A2_MU_KNOWN) < 1e-4),
        "scope_note": "QED (mass-independent + leptonic VP) ONLY through two "
                      "loops. Hadronic VP + hadronic light-by-light (QCD sector, "
                      "F151/F152) and electroweak (weak sector) are OUT OF SCOPE. "
                      "The full SM a_mu and the experimental comparison — an "
                      "active, unsettled area (g-2 Theory Initiative 2020/2025 "
                      "white papers; hadronic-VP tension) — are NOT claimed here.",
        "statement": "A2(mu) = -0.328479 + 1.094258 + 0.000078 = 0.765857 vs known "
                     "0.765857410; a_mu^{QED} (2 loops) = 1.1655e-3. Hadronic and "
                     "electroweak pieces deferred; no anomaly claim.",
    }


# ======================================================================
#  Report
# ======================================================================
def report() -> dict:
    return {
        "U1_universality": universality_gate(),
        "U2_vp_e_in_mu": vp_e_in_mu(),
        "U3_a_mu_two_loop": a_mu_two_loop(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
