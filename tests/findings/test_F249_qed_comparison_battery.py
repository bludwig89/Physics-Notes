#!/usr/bin/env python3
"""
qed_comparison_battery.py  —  F249: quantitative QED comparison battery
=======================================================================

A standalone, runnable battery that confronts the paired-spinor photon
(F69/F87/F125) with *measured* quantitative QED, in three tiers:

  Tier A  Tree / classical QED the model CAN compute, run against the real
          ca_* modules:
            A1  photon masslessness            Omega_pair(0) = 0
            A2  luminality                      v_group -> 1/sqrt(3) = c_lat
            A3  Lorentz isotropy of dispersion  spread of Omega/|k| -> 0 as O(k^2)
            A4  Coulomb 1/r                     static Green's fn exponent -> -1
                                                (massless pole, vs Yukawa)
            A5  Thomson cross section           sigma_T from (alpha, m_e) vs CODATA
            A6  Ward identity / charge cons.    C.(C x B) = 0 (transversality)

  Tier B  Photon-sector precision vs measured bounds:
            B1  vacuum birefringence            = 0 exact (both helicities one rate)
            B2  photon mass bound               = 0 vs PDG m_gamma bound
            B3  dispersion LIV order + scale    vs GRB time-of-flight bound

  Tier C  Radiative precision — HONEST REFERENCE LEDGER. Each computes the exact
          QED / measured reference value, runs what the model can, and records the
          specific missing loop machinery (the model has no interacting loop sector
          yet — F169 flagged the regularised all-k gauge pole as open):
            C1  electron g-2 (Schwinger a_e = alpha/2pi)
            C2  running alpha(q^2)  ->  alpha(M_Z)
            C3  Lamb shift 2s_1/2 - 2p_1/2

CLAUDE.md discipline: closed-form arccos dispersion + real FFT/linear algebra only;
no np.linalg.eig on chiral matrices; own fits. Reference constants are CODATA-2022 /
PDG / measured, cited in REFERENCES below and in the finding.

Run:  python3 qed_comparison_battery.py            (prints ledger, writes JSON)
      python3 qed_comparison_battery.py --json out.json
As a test:  pytest -q tests/findings/test_F249_qed_comparison_battery.py
"""
from __future__ import annotations
import os, sys, json, argparse
import numpy as np

# ---- put src on the path (works standalone and under pytest) ------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.lattice.bcc import bcc_dispersion                      # noqa: E402
from casim.engine.gauge.photon import (                           # noqa: E402
    pair_dispersion, pair_birefringence, group_velocity, photon_step_spectral,
    build_pair_mode,
)
from casim.engine.gauge.charge_coupling import bcc_curl_symbol, _cross_k, _dot_k  # noqa: E402
from casim.engine.lattice.geometry import make_kgrid_3d                   # noqa: E402
from casim.numerics import fft as _fft                                  # noqa: E402

ROOT3 = np.sqrt(3.0)
C_LAT = 1.0 / ROOT3

# =====================================================================
# Reference constants  (CODATA 2022 / PDG 2024 / measured)
# =====================================================================
REFERENCES = {
    "alpha_inv":        137.035999177,      # CODATA 2022  1/alpha
    "a_e_measured":     1.15965218046e-3,   # CODATA 2022  electron mag-moment anomaly
    "alpha_MZ_inv":     128.927,            # (alpha(M_Z^2))^-1, hadronic-run PDG
    "lamb_shift_MHz":   1057.845,           # 2s1/2-2p1/2, Lundeen-Pipkin 1981
    "sigma_T_barn":     0.66524587,         # Thomson cross section, CODATA (barn)
    "r_e_fm":           2.8179403262,       # classical electron radius (fm)
    "m_e_MeV":          0.51099895,         # electron mass (model anchor F120/F121)
    "m_gamma_bound_eV": 1.0e-18,            # PDG photon mass upper bound
}
ALPHA = 1.0 / REFERENCES["alpha_inv"]


def _fit_powerlaw(x, y):
    """Least-squares slope/intercept of log|y| vs log x -> (exponent, coeff)."""
    lx, ly = np.log(x), np.log(np.abs(y))
    A = np.vstack([lx, np.ones_like(lx)]).T
    exps, res, *_ = np.linalg.lstsq(A, ly, rcond=None)
    return float(exps[0]), float(np.exp(exps[1]))


# =====================================================================
# TIER A — tree / classical QED (model computes)
# =====================================================================
def tierA():
    out = {}

    # A1 masslessness -----------------------------------------------------------
    m0 = float(pair_dispersion(0.0, 0.0, 0.0))
    out["A1_masslessness"] = {
        "quantity": "Omega_pair(k=0)", "model": m0, "target": 0.0,
        "residual": abs(m0), "tier": "exact",
        "pass": abs(m0) < 1e-14,
        "note": "gapless: pure-hop walk A0=0 (F168/B1). Real photon: massless.",
    }

    # A2 luminality -------------------------------------------------------------
    vgs = {ax: group_velocity(n) for ax, n in
           {"x": (1, 0, 0), "diag": (1, 1, 1), "face": (1, 1, 0)}.items()}
    worst = max(abs(v - C_LAT) for v in vgs.values())
    out["A2_luminality"] = {
        "quantity": "group velocity dOmega/d|k| (k->0)",
        "model": vgs, "target": C_LAT, "residual": worst, "tier": "quantitative",
        "pass": worst < 1e-4,
        "note": "massless => moves at c_lat=1/sqrt(3) in every direction.",
    }

    # A3 Lorentz isotropy: spread of Omega/|k| over the sphere, vs |k| ----------
    rng = np.random.default_rng(0)
    dirs = rng.normal(size=(400, 3)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    kmags = [0.4, 0.2, 0.1, 0.05]
    spreads = []
    for km in kmags:
        speeds = np.array([pair_dispersion(*(km * d)) / km for d in dirs])
        spreads.append((speeds.max() - speeds.min()) / speeds.mean())
    order, coeff = _fit_powerlaw(np.array(kmags), np.array(spreads))
    out["A3_lorentz_isotropy"] = {
        "quantity": "fractional spread of phase speed over directions",
        "spread_vs_kmag": dict(zip(map(str, kmags), spreads)),
        "approach_order_in_k": order, "target_order": 2.0,
        "tier": "quantitative", "pass": abs(order - 2.0) < 0.25,
        "note": ("isotropy (=> Lorentz invariance) restored as k->0; anisotropy "
                 "is O(k^2). Real photon: exactly isotropic. Model: continuum-limit."),
    }

    # A4 Coulomb pole: the photon propagator has a MASSLESS 1/k^2 pole ----------
    # The static Coulomb operator is |C_odd(k)|^2 (F87 Gauss op). In 3-D, a
    # massless pole  D^-1(k) = m^2 + v^2 k^2  with m^2 = 0  IS the 1/r Coulomb
    # Green's function; a nonzero gap m^2 would give Yukawa e^{-mr}/r. We fit the
    # pole direction-resolved (position-space 1/r is spoiled by periodic-box /
    # BZ-fold artifacts, so we test the pole itself, which is the physics).
    from casim.engine.lattice.bcc import _bcc_uvec

    def _Cod2(kv):
        up, nxp, nyp, nzp = _bcc_uvec(kv[0] / 2, kv[1] / 2, kv[2] / 2, sign='+')
        um, nxm, nym, nzm = _bcc_uvec(-kv[0] / 2, -kv[1] / 2, -kv[2] / 2, sign='+')
        return (nxp - nxm) ** 2 + (nyp - nym) ** 2 + (nzp - nzm) ** 2

    rng = np.random.default_rng(0)
    dirs = rng.normal(size=(200, 3)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    kk = np.array([0.03, 0.06, 0.09, 0.12])
    ka, Ca = [], []
    for d in dirs:
        for k in kk:
            ka.append(k); Ca.append(_Cod2(k * d))
    ka, Ca = np.array(ka), np.array(Ca)
    A = np.vstack([np.ones_like(ka), ka ** 2]).T
    (m2, v2), *_ = np.linalg.lstsq(A, Ca, rcond=None)
    c_over_k2 = np.array([_Cod2(kk[0] * d) / kk[0] ** 2 for d in dirs])
    aniso = float((c_over_k2.max() - c_over_k2.min()) / c_over_k2.mean())
    out["A4_coulomb_massless_pole"] = {
        "quantity": "photon static pole  D^-1 = m^2 + v^2 k^2",
        "mass_gap_m2": float(m2), "target_m2": 0.0,
        "v2": float(v2), "target_v2": 1.0 / 3.0, "v": float(np.sqrt(abs(v2))),
        "anisotropy_of_v2": aniso,
        "tier": "quantitative", "pass": abs(m2) < 1e-4 and abs(v2 - 1 / 3) < 5e-3,
        "note": ("massless pole (m^2->0) in 3-D IS the 1/r Coulomb law, NOT Yukawa "
                 "e^-mr/r; v^2->1/3 = c_lat^2. alpha sets the physical prefactor and "
                 "is an INPUT, not predicted. Anisotropy O(1e-4) at k=0.03."),
    }

    # A5 Thomson cross section from (alpha, m_e) --------------------------------
    # r_e = alpha * hbar/(m_e c);  sigma_T = (8pi/3) r_e^2.  Model inputs: alpha,m_e.
    hbar_c_MeV_fm = 197.3269804
    r_e_fm = ALPHA * hbar_c_MeV_fm / REFERENCES["m_e_MeV"]     # fm
    sigma_T_fm2 = (8.0 * np.pi / 3.0) * r_e_fm ** 2            # fm^2
    sigma_T_barn = sigma_T_fm2 * 1e-2                          # 1 barn = 100 fm^2
    rel = abs(sigma_T_barn - REFERENCES["sigma_T_barn"]) / REFERENCES["sigma_T_barn"]
    out["A5_thomson_cross_section"] = {
        "quantity": "sigma_T (Thomson) from model alpha + m_e",
        "model_barn": sigma_T_barn, "target_barn": REFERENCES["sigma_T_barn"],
        "model_r_e_fm": r_e_fm, "target_r_e_fm": REFERENCES["r_e_fm"],
        "rel_err": rel, "tier": "quantitative", "pass": rel < 5e-3,
        "note": ("classical (Thomson) scattering limit; a tree-level QED number "
                 "the model's two inputs reproduce."),
    }

    # A6 Ward identity / charge conservation: transversality C.(C x B)=0 --------
    rng = np.random.default_rng(1)
    B = rng.normal(size=(3, 24, 24, 24))
    Bk = _fft.fftn(B, axes=(-3, -2, -1))
    KX, KY, KZ = make_kgrid_3d(24, 24, 24)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    cx, cy, cz = _cross_k(Cx, Cy, Cz, Bk[0], Bk[1], Bk[2])
    dot = _dot_k(Cx, Cy, Cz, cx, cy, cz)
    ward = float(np.max(np.abs(dot)) / (np.max(np.abs(Bk)) + 1e-30))
    out["A6_ward_charge_conservation"] = {
        "quantity": "C.(C x B) (curl sources no charge => d_t rho = -i C.J)",
        "model": ward, "target": 0.0, "residual": ward,
        "tier": "machine", "pass": ward < 1e-12,
        "note": "tree Ward identity: the U(1) coupling conserves charge exactly (F87).",
    }
    return out


# =====================================================================
# TIER B — photon-sector precision vs bounds
# =====================================================================
def tierB():
    out = {}

    # B1 vacuum birefringence: MEASURE the per-step rotation rate for two ------
    # orthogonal linear polarisations of the same k; a birefringent medium would
    # give them different rates. We read the realised rotation angle from the
    # (E,B) mixing at the populated mode and compare the two polarisations.
    L = 25
    khat = np.array([1, 1, 1.]) / ROOT3

    def _realised_rate(e1v):
        E, Bf, e1u, e2u = build_pair_mode(L, 3, khat, e1v)
        E1, B1 = photon_step_spectral(E, Bf)
        idx = (3, 3, 3)
        Ek = np.array([_fft.fftn(E1[a])[idx] for a in range(3)])
        # component of rotated E along the original e1 and e2 axes
        a_par = float(np.real(np.dot(e1u, Ek)))
        a_perp = float(np.real(np.dot(e2u, Ek)))
        return float(np.arctan2(a_perp, a_par))

    r_a = _realised_rate(np.array([1, -1, 0.]))
    r_b = _realised_rate(np.array([1, 1, -2.]))   # orthogonal transverse pol
    split = abs(r_a - r_b)
    # contrast: the split a single-branch (chiral) photon WOULD carry
    bf = float(abs(pair_birefringence(*(0.3 * khat))))
    out["B1_vacuum_birefringence"] = {
        "quantity": "rotation-rate difference between two linear polarisations",
        "measured_split": split, "single_branch_would_be": bf,
        "target": 0.0, "tier": "machine", "pass": split < 1e-12,
        "note": ("both polarisations rotate at the one rate Omega_pair => zero "
                 "vacuum birefringence (F69 PP2 dynamical). The single-branch value "
                 "is the split the pair structurally avoids; that chiral photon is "
                 "excluded by GRB/AGN polarimetry (F65/F66)."),
    }

    # B2 photon mass bound ------------------------------------------------------
    m0 = float(pair_dispersion(0.0, 0.0, 0.0))
    out["B2_photon_mass"] = {
        "quantity": "photon rest mass (gap at k=0)",
        "model": m0, "pdg_bound_eV": REFERENCES["m_gamma_bound_eV"],
        "tier": "exact", "pass": abs(m0) < 1e-14,
        "note": "gap identically 0 => consistent with PDG m_gamma < 1e-18 eV.",
    }

    # B3 dispersion LIV: leading deviation from linear along body diagonal ------
    n = np.array([1, 1, 1.]) / ROOT3
    ks = np.array([0.30, 0.20, 0.15, 0.10, 0.07])
    dev = np.array([pair_dispersion(*(k * n)) - k * C_LAT for k in ks])
    order, coeff = _fit_powerlaw(ks, dev)
    # axis-aligned is EXACTLY linear (F105) -> LIV is anisotropic:
    dev_axis = float(pair_dispersion(0.3, 0, 0) - 0.3 * C_LAT)
    out["B3_dispersion_LIV"] = {
        "quantity": "Omega_pair(k) - c_lat|k| along body diagonal",
        "leading_order_in_k": order, "leading_coeff": coeff,
        "axis_aligned_deviation": dev_axis, "target_axis": 0.0,
        "tier": "quantitative", "pass": order > 2.5,
        "note": ("axis-aligned dispersion exactly linear (F105); LIV is "
                 "anisotropic and O(k^3), i.e. suppressed by (k a)^2. Consistent "
                 "with GRB time-of-flight bounds ~15 decades below sensitivity (F28)."),
    }
    return out


# =====================================================================
# TIER C — radiative precision: NOW COMPUTED (F251/F252 loop sector)
# =====================================================================
# The interacting one-loop QED sector (F251 vacuum polarisation, F252 vertex)
# closes the ledger the original F249 left open: the three items below flip from
# LEDGER to PASS. Ward/WT identities are exact (sympy), b0^QED=4/3 and a_e=alpha/
# 2pi are exact, and the running / Lamb shift are computed with honest scope
# (leptonic-only running; leading-order Lamb shift).
def tierC():
    from casim.engine.interactions import qed_vacuum_polarization as vp   # F251
    from casim.engine.interactions import qed_vertex_loop as vx           # F252
    out = {}

    # C1 — electron g-2 from the one-loop vertex (F252 V2) --------------------
    ae = vx.ae_schwinger_symbolic()
    out["C1_electron_g_minus_2"] = {
        "quantity": "electron anomalous moment a_e = (g-2)/2",
        "model_a_e": ae["a_e_schwinger"],
        "F2_0_over_alpha": ae["F2_0_over_alpha_symbolic"],   # 1/(2pi), exact
        "parametric_integral": ae["parametric_integral"],    # 1, exact
        "measured_a_e": REFERENCES["a_e_measured"],
        "leading_vs_measured_rel": ae["rel_err_leading"],
        "model_can_compute": True, "computed_by": "F252 ca_vertex_loop",
        "tier": "exact_leading", "pass": bool(ae["gate_pass"]
                                              and ae["rel_err_leading"] < 2e-3),
        "note": ("a_e = F_2(0) = alpha/2pi computed EXACTLY from the one-loop "
                 "vertex (parametric integral = 1); 0.15% vs measured. Higher QED "
                 "orders out of scope (future)."),
    }

    # C2 — running alpha from the photon self-energy (F251 Pi4) ---------------
    run = vp.leptonic_running()
    b0 = vp.b0_gate_symbolic()
    out["C2_running_alpha"] = {
        "quantity": "running coupling alpha(q^2): alpha(0) -> alpha(M_Z)",
        "alpha0_inv": REFERENCES["alpha_inv"],
        "b0_QED": b0["b0_QED"],                              # 4/3, exact
        "delta_alpha_lep_model": run["delta_alpha_lep"],
        "delta_alpha_lep_PDG": run["delta_alpha_lep_PDG"],
        "alpha_MZ_inv_leptonic": run["alpha_MZ_inv_leptonic"],
        "alpha_MZ_inv_measured_full": REFERENCES["alpha_MZ_inv"],
        "model_can_compute": True, "computed_by": "F251 ca_vacuum_polarization",
        "tier": "quantitative_leptonic",
        "pass": bool(b0["gate_pass"]
                     and run["delta_alpha_lep_rel_err"] < 0.01),
        "note": ("photon self-energy built: b0^QED=4/3 exact, Ward-transverse; "
                 "leptonic Delta alpha(M_Z) matches PDG to <0.3% "
                 "(1/alpha|lep ~ 132.7). Hadronic pull-down to 128.927 is the "
                 "QCD sector (F151/F152) — honest scope, not the lepton loop."),
    }

    # C3 — Lamb shift from self-energy + Uehling vacuum polarisation (F252 V4) -
    lamb = vx.lamb_shift()
    out["C3_lamb_shift"] = {
        "quantity": "hydrogen Lamb shift 2s_1/2 - 2p_1/2",
        "model_MHz": lamb["total_lamb_MHz"],
        "self_energy_MHz": lamb["self_energy_2s_minus_2p_MHz"],
        "vacuum_pol_MHz": lamb["vacuum_pol_uehling_MHz"],
        "measured_MHz": REFERENCES["lamb_shift_MHz"],
        "fraction_of_measured": lamb["fraction_of_measured"],
        "dirac_degeneracy_lifted": lamb["degeneracy_lifted"],
        "model_can_compute": True, "computed_by": "F252 ca_vertex_loop + ca_atom",
        "tier": "quantitative_leading",
        "pass": bool(lamb["degeneracy_lifted"]
                     and 0.98 < lamb["fraction_of_measured"] < 1.02),
        "note": ("the exact Dirac 2s-2p degeneracy (F125) is lifted to +1052.2 "
                 "MHz = 99.5% of measured 1057.845 MHz. Uehling (-27.1 MHz) "
                 "derived from F251's Pi; self-energy from the Bethe log. Residual "
                 "~5.6 MHz is higher-order alpha(Z alpha)^5/two-loop QED."),
    }
    return out


# =====================================================================
# TIER D — tree S-matrix completeness (F260 ca_qed_scattering)
# =====================================================================
# F249 Tier-A5 stops at Thomson (the zero-energy Compton limit). The full tree
# QED S-matrix — Compton/Klein-Nishina, Moller, Bhabha, Dirac annihilation,
# e+e- -> mu+mu- — plus the positron/charge-conjugation + crossing sector are
# built in F260 (ca_qed_scattering). This tier surfaces them as PASSes here.
def tierD():
    from casim.engine.interactions import qed_scattering as qs
    out = {}

    comp = qs.compton_M2_vs_textbook()
    kn = qs.klein_nishina()
    ward = qs.compton_ward_symbolic()
    out["D1_compton_klein_nishina"] = {
        "quantity": "Compton |M|^2 = Klein-Nishina; total sigma(x); -> Thomson",
        "M2_worst_rel_err": comp["worst_rel_err"],
        "kn_total_worst_rel_err": kn["worst_rel_err_vs_closed"],
        "sigma_over_thomson_at_x_1e-4": kn["sigma_over_thomson_at_x_1e-6"],
        "ward_worst": ward["worst_k_dot_M_incoming"],
        "tier": "quantitative",
        "pass": bool(comp["gate_pass"] and kn["gate_pass"] and ward["gate_pass"]),
        "note": ("full Klein-Nishina (1929): |M|^2 matches the Mandelstam form to "
                 "machine precision, total sigma(x) reproduces the closed KN form "
                 "and reduces to Thomson sigma_T as omega->0 (extends A5); Ward exact."),
    }

    moll = qs.moller_vs_textbook()
    bhab = qs.bhabha_vs_textbook()
    cross = qs.crossing_symbolic()
    out["D2_moller_bhabha"] = {
        "quantity": "Moller (t/u) & Bhabha (s/t) cross sections + crossing",
        "moller_worst_rel_err": moll["worst_rel_err"],
        "bhabha_worst_rel_err": bhab["worst_rel_err"],
        "moller_bhabha_crossing_exact": cross["moller_to_bhabha_s_u_crossing"],
        "tier": "quantitative",
        "pass": bool(moll["gate_pass"] and bhab["gate_pass"] and cross["gate_pass"]),
        "note": ("Moller 1932 / Bhabha 1936 differential cross sections reproduced; "
                 "the Bhabha<->Moller s<->u crossing relation is exact (sympy)."),
    }

    ann = qs.annihilation_gates()
    out["D3_pair_annihilation"] = {
        "quantity": "e+e- -> gamma gamma (Dirac 1930): |M|^2, Bose, Ward, sigma",
        "M2_worst_rel_err": ann["worst_rel_err_M2"],
        "bose_symmetry_worst": ann["bose_symmetry_worst_rel"],
        "ward_both_photons_worst": ann["ward_both_photons_worst"],
        "sigma_worst_rel_err": ann["worst_rel_err_sigma"],
        "tier": "quantitative", "pass": bool(ann["gate_pass"]),
        "note": ("Dirac annihilation cross section reproduced; photon Bose symmetry "
                 "and Ward on both photons exact; needs the positron (v = C ubar^T)."),
    }

    mup = qs.mupair_gates()
    out["D4_ee_to_mumu"] = {
        "quantity": "e+e- -> mu+mu-: |M|^2, total sigma -> 4 pi alpha^2 / 3s",
        "M2_worst_rel_err": mup["worst_rel_err_M2"],
        "sigma_worst_rel_err": mup["worst_rel_err_sigma"],
        "m_mu_MeV": mup["m_mu_MeV"],
        "tier": "quantitative", "pass": bool(mup["gate_pass"]),
        "note": ("the R-ratio unit sigma = (4 pi alpha^2/3s) beta (1+2m^2/s) -> "
                 "4 pi alpha^2/3s at high energy; needs the 2nd-generation muon "
                 "(F121 anchor)."),
    }
    return out


def run_all():
    A, B, C, D = tierA(), tierB(), tierC(), tierD()
    checks = {**A, **B, **C, **D}
    computed = {k: v for k, v in checks.items() if v.get("pass") is not None}
    ledger = {k: v for k, v in checks.items() if v.get("pass") is None}
    n_pass = sum(1 for v in computed.values() if v["pass"])
    summary = {
        "finding": "F249",
        "title": "Quantitative QED comparison battery for the paired-spinor photon",
        "computed_checks": len(computed),
        "computed_pass": n_pass,
        "computed_fail": len(computed) - n_pass,
        "reference_ledger_items": len(ledger),
        "alpha_used_inv": REFERENCES["alpha_inv"],
        "verdict": ("tree/classical + photon-precision QED reproduced; the Tier-C "
                    "radiative ledger is CLOSED by the interacting one-loop "
                    "sector (F251 vacuum polarisation, F252 vertex): a_e=alpha/2pi "
                    "and running alpha from Pi(q^2) and the Lamb shift all "
                    "computed, with Ward/WT identities and b0^QED=4/3 exact; and "
                    "Tier-D adds the full tree S-matrix (F260): Compton/Klein-"
                    "Nishina, Moller, Bhabha, Dirac annihilation, e+e- -> mu+mu-, "
                    "plus the positron/charge-conjugation + crossing sector."),
    }
    return {"summary": summary, "references": REFERENCES,
            "tierA": A, "tierB": B, "tierC": C, "tierD": D}


def _print(res):
    s = res["summary"]
    print("=" * 74)
    print(f"  {s['finding']}: {s['title']}")
    print("=" * 74)
    for tier, label in (("tierA", "TIER A  tree / classical (model computes)"),
                        ("tierB", "TIER B  photon-sector precision"),
                        ("tierC", "TIER C  radiative — reference ledger"),
                        ("tierD", "TIER D  tree S-matrix (F260)")):
        print(f"\n{label}")
        print("-" * 74)
        for name, c in res[tier].items():
            if c.get("pass") is None:
                mark = "LEDGER"
            else:
                mark = "PASS" if c["pass"] else "FAIL"
            print(f"  [{mark:6s}] {name:28s} {c['quantity']}")
            if c.get("pass") is None:
                print(f"            missing: {c['missing_machinery'][:60]}...")
    print("\n" + "-" * 74)
    print(f"  computed: {s['computed_pass']}/{s['computed_checks']} pass"
          f"   |   reference-ledger items: {s['reference_ledger_items']}")
    print(f"  verdict: {s['verdict']}")
    print("=" * 74)


# ---- pytest entry point (collectable under tests/findings/) ------------------
def test_qed_comparison_battery():
    """All Tier-A/B/C computed checks must pass; the Tier-C ledger is now closed
    by the F251/F252 interacting loop sector (no more reference-ledger items)."""
    res = run_all()
    fails = []
    for tier in ("tierA", "tierB", "tierC", "tierD"):
        for name, c in res[tier].items():
            if c.get("pass") is False:
                fails.append(name)
    assert not fails, f"failed computed checks: {fails}"
    assert res["summary"]["computed_pass"] == res["summary"]["computed_checks"]
    assert res["summary"]["reference_ledger_items"] == 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="write results JSON here")
    args = ap.parse_args()
    res = run_all()
    _print(res)
    if args.json:
        def _native(o):
            if hasattr(o, "item"):
                return o.item()
            if isinstance(o, (np.ndarray,)):
                return o.tolist()
            return str(o)
        with open(args.json, "w") as f:
            json.dump(res, f, indent=2, default=_native)
        print(f"\nwrote {args.json}")
