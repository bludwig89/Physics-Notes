"""Geometry sector — the lattice ruler, the lattice light speed, the SI anchors.

Roadmap C2 (D7): these are now **owned** here, not merely described.  Before
C2, ``a/ell_P`` appeared at three different precisions and ``c_lat`` had ~74
independent definitions; both now resolve from closed form and every physics
module imports them.

    from casim.constants import c_lat, a_over_ellP
"""
from __future__ import annotations

import math

from . import Constant, Site, register

# ---------------------------------------------------------------------------
# a / ell_P  —  the SI ruler (F79 closed form, adopted as canonical by F107)
#
# C2.1: closed form, never a decimal.  The two historically-truncated sites are
# recorded as `literal` with their own precision so the difference stays
# visible; the 5-sf 6.5978 carries 3.4e-6 relative error against this.
# ---------------------------------------------------------------------------
A_OVER_ELLP = math.sqrt(8.0 * math.pi) * 3.0 ** 0.25      # 6.5978224...

register(Constant(
    symbol="a_over_ellP",
    value=A_OVER_ELLP,
    units="dimensionless (multiples of the Planck length)",
    exactness="exact",
    provenance=("F79", "F107"),
    derivation=r"a/\ell_P = \sqrt{8\pi}\,3^{1/4}; parameter-free (F79 structural G), "
               r"adopted as THE SI ruler by F107 after the L4 lensing check and the "
               r"GRB gate, which excludes the F83 fermion-mass ceiling by ~9 decades.",
    sector="geometry",
    supersedes=("F83-ceiling-anchor",),
    tol=1e-9,
    sites=(
        Site("src/casim/engine/lattice/si_scale.py", "A_OVER_ELLP", kind="import",
             note="was the canonical closed form; now imports the registry's"),
        Site("src/casim/engine/interactions/running_alpha_s.py", "A_OVER_LP", kind="import",
             note="was a 6-sf truncation (6.59782); now exact"),
        Site("src/casim/engine/interactions/qed_renormalization.py", "A_OVER_LPLANCK",
             kind="import",
             note="was a 5-sf truncation (6.5978, ~3.4e-6 relative); now exact"),
        Site("src/casim/engine/interactions/cosmology_growth.py", "A_CELL_M",
             kind="import",
             note="F288 B1: a = a_over_ellP * ell_P_m is the cell size the "
                  "structure-formation discreteness bound is measured in. The "
                  "bound (<= 1.3e-112 at the Lyman-alpha scale) is what "
                  "licenses using the continuum growth equation at all, so "
                  "this site is load-bearing rather than decorative."),
        Site("src/casim/engine/interactions/horizon_entanglement.py", "_A_OVER_ELLP",
             kind="import",
             note="F355: a/ell_P sets BOTH halves of the E9 comparison -- the "
                  "required per-cell entropy S_CELL_REQUIRED = (a/ell_P)^2/4 "
                  "(== 2 pi sqrt3, F190) and the ruler stretch that would "
                  "reconcile the computed entanglement entropy with it. The "
                  "finding's result IS a ratio of these two, so this site is "
                  "load-bearing rather than decorative."),
        Site("src/casim/engine/particles/derive_higgs_bhl_compositeness.py",
             "_A_OVER_ELLP", kind="import",
             note="F352: Lambda_model = E_Planck / (a/ell_P) is the "
                  "compositeness/UV cutoff for the BHL-style top-"
                  "condensation RG attempt at the F73 Cooper-pair scalar."),
        Site("src/casim/engine/interactions/gravity_band_cutoff.py",
             "_A_OVER_ELLP", kind="import",
             note="F357: tau/t_Planck = a_over_ellP/sqrt(3) (F79 Sec.5's own "
                  "a/tau = c*sqrt(3)) converts the exact dimensionless band "
                  "top Omega_max=pi into E_max/E_Planck = pi*sqrt(3)/a_over_ellP "
                  "= sqrt(pi*sqrt(3)/8); load-bearing, not decorative -- it is "
                  "the finding's one physical-units anchor."),
        Site("src/casim/engine/interactions/graviton_collapse_threshold.py",
             "_A_OVER_ELLP", kind="import",
             note="F359: re-derives F228's one-cell remnant mass M_rem/M_Pl = "
                  "a_over_ellP/(4*sqrt(pi)) from the SAME registered ruler "
                  "(A^2=8*pi*sqrt(3) is F79/F107's own canonical-cell "
                  "identity), then compares it to F357's E_max via the same "
                  "ruler -- both numbers this finding compares trace to this "
                  "one site; load-bearing, not decorative."),
    ),
    notes="C2 deleted the two truncated copies. The drift that introduces is "
          "recorded in the C2 changelog entry: both sites now carry the exact "
          "closed form, which is a 3.4e-6 relative MOVE at the 5-sf site. "
          "Prefer the closed form over any decimal, everywhere.",
))

# ---------------------------------------------------------------------------
# c_lat  —  the lattice light speed on the d=3 BCC lattice (F26)
# ---------------------------------------------------------------------------
C_LAT_BCC = 1.0 / math.sqrt(3.0)                          # 0.5773502691896258

register(Constant(
    symbol="c_lat",
    value=C_LAT_BCC,
    units="cells per tick",
    exactness="exact",
    provenance=("F26",),
    derivation=r"c_\text{lat} = d\Omega/d|\mathbf k| as |\mathbf k|\to 0, with "
               r"\Omega = 2\omega(|\mathbf k|/2) the rotation angle the (E,B) pair "
               r"traverses per tick. On the d=3 BCC lattice this is 1/\sqrt3. "
               r"It is a rotation RATE, not a phase velocity (a core design decision).",
    sector="geometry",
    tol=1e-12,
    sites=(
        # --- kernels ---------------------------------------------------------
        Site("src/casim/engine/interactions/gravity.py", "C_LAT_BCC", kind="import"),
        Site("src/casim/engine/lattice/blockspin.py", "C_LAT", kind="import"),
        Site("src/casim/engine/interactions/qi_decoherence_floor.py", "C_LAT", kind="import"),
        Site("src/casim/engine/lattice/bcc.py", "BCC_C", kind="import"),
        Site("src/casim/engine/lattice/wavepacket.py", "c_lat", kind="import",
             note="F20 remediation: c_lat is the group-velocity scale in the "
                  "closed forms dw/dk_x = c_lat*n_hat_x and the finite-width "
                  "packet predictions c_lat*<n_hat_x^2> / c_lat*<n_hat_x>"),
        Site("src/casim/engine/gauge/photon_packet.py", "c_lat", kind="import",
             note="F314: c_lat is the argument scale of the BCC trig factors in "
                  "the closed-form pair group velocity dOmega_pair/dk_i, the "
                  "exact on-axis value of that velocity, and the reference the "
                  "measured beam deficit is quoted against"),
        Site("src/casim/engine/interactions/derive_boost_covariance.py", "c_lat",
             kind="import",
             note="F301: c_lat sets the BCC trig argument scale, the Minkowski "
                  "metric in Phi = (Omega^2 - c_lat^2 k^2)/2 c_lat^2, and the "
                  "chiral-branch defect coefficient D_i = -s c_lat (kykz, ...). "
                  "The module evaluates 1/sqrt3 at mpmath working precision and "
                  "ASSERTS agreement with the registry float to 1e-15 -- "
                  "mp.mpf() of a double would carry 1e-16 error into radical "
                  "identities the finding checks at 1e-46"),
        Site("src/casim/engine/interactions/horizon_entanglement.py", "_C_LAT",
             kind="import",
             note="F355: A_CUBE = 2 c_lat is F278's BCC conventional cube edge, "
                  "which is what makes 'nats per horizon cell' and 'nats per "
                  "a^2 of boundary area' the same statement -- BCC puts exactly "
                  "one site per a^2 in every (001) layer."),
        Site("src/casim/engine/particles/dirac_bcc.py", "C_LAT_3D", kind="import"),
        Site("src/casim/engine/interactions/qi_cluster_interacting_3d.py", "c_lat",
             kind="import",
             note="F331: c_lat sets ROOT3=1/c_lat (exactly sqrt3) used in the "
                  "exact axis100/axis110 kappa closed forms and as the "
                  "physical-distance-per-index-step normalisation for the "
                  "oblique-BZ real-space correlator."),
        Site("src/casim/engine/gauge/bilinear.py", None, kind="import",
             note="two inv_root3 locals in the BCC helicity helpers"),
        Site("src/casim/engine/interactions/qed_casimir.py", "C_LAT", kind="import"),
        Site("src/casim/engine/interactions/qed_vacuum_polarization.py", "C_LAT", kind="import"),
        Site("src/casim/engine/gauge/gluon_self_energy.py", "C_LAT", kind="import"),
        Site("src/casim/engine/interactions/qed_ir_bremsstrahlung.py", "C_LAT", kind="import"),
        Site("src/casim/engine/interactions/qed_electron_self_energy.py", "C_LAT", kind="import"),
        Site("src/casim/engine/gauge/colour_dielectric.py", None, kind="import",
             note="c_lat local in the renormalised-rotation helper"),
        Site("src/casim/engine/interactions/superconductivity.py", None, kind="import",
             note="was a function DEFAULT ARGUMENT (massive_photon_omega), the "
                  "pattern C2.4 exists to eliminate: outside the static reader's "
                  "reach until the value came from an import"),
        Site("src/casim/engine/gauge/weak_wmu.py", None, kind="import",
             note="INV_SQRT3 local in the dispersion helper"),
        # --- forks -----------------------------------------------------------
        Site("src/casim/engine/forks/gravity/gr_fork_F216_massive_spin2.py", "c_lat",
             kind="import"),
        Site("src/casim/engine/forks/gravity/gr_fork_F180_gw_speed.py", "C_LAT", kind="import"),
        Site("src/casim/engine/forks/gravity/gr_fork_F248_tt_graviton_bcc.py", "C_LAT",
             kind="import"),
        Site("src/casim/engine/forks/gravity/gr_fork_F59_induced_eh_prefactor.py", "INV_R3",
             kind="import"),
        Site("src/casim/engine/forks/gauge/curl_fork_baseline_bcc.py", "C_LAT", kind="import"),
        Site("src/casim/engine/forks/lattice/smearing_fork_harness.py", "C_LAT", kind="import"),
        Site("src/casim/engine/forks/gravity/gr_fork_F60_channel_reconciliation.py", None,
             kind="import", note="one element of a deliberate channel-speed scan"),
        Site("src/casim/engine/gauge/photon.py", None, kind="import",
             note="the group-velocity print in __main__"),
        # --- package ---------------------------------------------------------
        Site("src/casim/engine/core/simulation.py", None, kind="import",
             note="LatticeSpec.c_lat default"),
    ),
    notes="Before C2 this had ~74 independent definitions in two spellings: the "
          "1/sqrt(3) family and a hardcoded 0.5773502691896258. C2 deleted every "
          "one in src/ (before C9, two); tests/ drains during C7. The genuine "
          "exceptions are typed MeasuredConstant records in "
          "casim/constants/measured.py — the 2-D square lattice (1/sqrt2), the "
          "simple-cubic fork (1.0), and the SU(3) lambda_8 normalisation, which "
          "is 1/sqrt(3) for entirely unrelated reasons.",
))

# ---------------------------------------------------------------------------
# The external SI anchors.  These are CODATA/SI, not model outputs; they are
# registered so `ca_si_scale.canonical_cell()` stops carrying its own copies
# and so a CODATA revision is a one-line change with a visible blast radius.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="ell_P_m",
    value=1.616255e-35,
    units="m",
    exactness="external",
    provenance=("CODATA",),
    derivation="CODATA Planck length. The ruler a/ell_P is converted to metres "
               "through this and nothing else.",
    sector="geometry",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/lattice/si_scale.py", "ELL_P", kind="import"),
        Site("src/casim/engine/interactions/cosmology_lattice_elasticity.py",
             "ell_P_m", kind="import",
             note="F284: converts the F107 ruler to metres for the first-"
                  "resolvable-epoch numbers and the Hubble cell budget."),
    ),
))

register(Constant(
    symbol="c_SI",
    value=2.99792458e8,
    units="m/s",
    exactness="external",
    provenance=("SI",),
    derivation="Exact by SI definition since 1983 — it defines the metre.",
    sector="geometry",
    tol=0.0,
    sites=(
        Site("src/casim/engine/lattice/si_scale.py", "C_SI", kind="import"),
        Site("src/casim/engine/interactions/cosmology_lattice_elasticity.py",
             "c_SI", kind="import",
             note="F284: t_min = a/c_lat in seconds, and the present Hubble "
                  "radius in cells."),
    ),
    notes="'external' rather than 'exact': it is exact by convention, not by "
          "derivation in this model. The exactness class records provenance, "
          "not arithmetic.",
))

register(Constant(
    symbol="hbar_SI",
    value=1.054571817e-34,
    units="J s",
    exactness="external",
    provenance=("CODATA",),
    derivation="CODATA reduced Planck constant.",
    sector="geometry",
    tol=1e-9,
    sites=(Site("src/casim/engine/lattice/si_scale.py", "HBAR", kind="import"),),
))

register(Constant(
    symbol="hbar_SI_from_h",
    value=6.62607015e-34 / (2.0 * math.pi),
    units="J s",
    exactness="exact",
    provenance=("SI",),
    derivation="h/(2 pi) with h = 6.62607015e-34 J s EXACT by SI definition "
               "since 2019, so this is exact arithmetic, not a measurement.",
    sector="geometry",
    tol=1e-15,
    sites=(Site("src/casim/engine/interactions/superconductivity.py", "HBAR",
                kind="runtime",
                note="computed as H_PLANCK/(2 pi) in the module, which is this "
                     "constant. Left computed: the two-line derivation from the "
                     "exact h is clearer at the point of use than an import."),),
    notes="Deliberately NOT the same registry entry as hbar_SI. They differ by "
          "6e-11 relative — hbar_SI is CODATA's 10-digit quote, this is the "
          "exact quotient. C2.4's sweep found the discrepancy in "
          "ca_superconductivity.py, where the exact form was in use and a "
          "substitution would have QUIETLY COARSENED it. Same rule as the three "
          "f_pi: two numbers, two constants, no silent reconciliation.",
))

register(Constant(
    symbol="G_CODATA",
    value=6.67430e-11,
    units="m^3 kg^-1 s^-2",
    exactness="external",
    provenance=("CODATA",),
    derivation="CODATA Newton constant. A COMPARISON TARGET: F79's closed form "
               "predicts it to 3.0e-8, which is the check, not the input.",
    sector="geometry",
    tol=1e-9,
    sites=(Site("src/casim/engine/lattice/si_scale.py", "G_CODATA", kind="import"),),
    notes="Deliberately distinct from G_LATTICE (gravity sector), which is the "
          "model's structural 1/(72 pi). Conflating them would turn F79's "
          "prediction into an input — the same hazard as f_pi anchor vs target.",
))


# ---------------------------------------------------------------------------
# F327 — the J <-> GeV bridge, and the two external LIV bounds the chiral
# O(|k|^2) boost defect (F301) is confronted with.
#
# `J_per_GeV` is exact by SI (the elementary charge has been a defined constant
# since 2019), so this is arithmetic, not a measurement.  It is registered
# because si_scale.canonical_cell() and derive_chiral_liv_bound both convert
# hbar*c/a into GeV and were each carrying their own copy.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="J_per_GeV",
    value=1.602176634e-10,
    units="J/GeV",
    exactness="exact",
    provenance=("SI",),
    derivation="1 GeV = 1e9 * e joule with e = 1.602176634e-19 C EXACT by SI "
               "definition since 2019.",
    sector="geometry",
    tol=0.0,
    sites=(
        Site("src/casim/engine/lattice/si_scale.py", "J_PER_GEV", kind="import",
             note="canonical_cell()'s UV cutoff hbar c / a in GeV; was a bare "
                  "literal until F327 needed the same bridge."),
        Site("src/casim/engine/interactions/derive_chiral_liv_bound.py",
             "J_PER_GEV", kind="import",
             note="F327: E_a = hbar c / a in GeV is the whole conversion that "
                  "turns F301's lattice-unit coefficient into an SME-comparable "
                  "number, so this bridge is load-bearing for the exclusion."),
        Site("src/casim/engine/interactions/qed_uv_completion.py", "joule_per_GeV",
             kind="import",
             note="lambda_uv_GeV()'s hbar c / a in GeV; was a bare literal until "
                  "F327 registered the bridge."),
        Site("src/casim/engine/interactions/thermodynamics.py", "J_per_GeV",
             kind="import",
             note="E_lattice_GeV = hbar/tau in GeV; was a bare literal until F327."),
        Site("src/casim/engine/forks/gravity/gr_fork_F223_spin2_binding_relic.py",
             "Mpl_GeV", kind="runtime",
             note="1e9*eV inside Mpl_GeV; left computed - see the F238 note below."),
        Site("src/casim/engine/forks/gravity/gr_fork_F228_geon_production_stability.py",
             "Mpl_GeV", kind="runtime",
             note="1e9*eV inside Mpl_GeV; left computed - see the F238 note below."),
        Site("src/casim/engine/forks/gravity/gr_fork_F228_geon_production_stability.py",
             "GeV_per_kg", kind="runtime",
             note="1e9*eV inside GeV_per_kg; left computed - see the F238 note."),
        Site("src/casim/engine/forks/gravity/gr_fork_F238_geon_relic_abundance.py",
             "GeV_per_kg", kind="runtime",
             note="computed in place as 1e9 * eV from the exact SI elementary "
                  "charge, inside GeV_per_kg = c^2/(1e9 eV). LEFT COMPUTED on "
                  "purpose: a fork is a preserved falsification record (CLAUDE.md "
                  "'a fork is a tested and rejected or live-exploratory branch, "
                  "not dead code'), so rewriting its arithmetic to import a "
                  "constant registered two months later would edit the record. "
                  "Same treatment as hbar_SI_from_h's superconductivity site. "
                  "Surfaced by F327, which is what registered J_per_GeV."),
    ),
))

register(Constant(
    symbol="E_LV_e_sup_min_GeV",
    value=9.4e25,
    units="GeV",
    exactness="external",
    provenance=("F327",),
    derivation="Li & Ma, Phys. Lett. B 829 (2022) 137034, arXiv:2204.02956 - "
               "the SUPERLUMINAL n=1 (dimension-5) electron LIV scale from the "
               "1.12 +- 0.09 PeV LHAASO photon from the Crab Nebula, via the "
               "absence of vacuum Cherenkov radiation. Convention "
               "E^2 = m^2 + p^2[1 - s (p/E_LV)^n] with s = -1 superluminal; "
               "equivalently |eta| = M_Pl/E_LV <= 1.3e-7 in the Myers-Pospelov "
               "normalisation E^2 = p^2 + m^2 + eta p^3/M_Pl.",
    sector="geometry",
    tol=0.0,
    notes="A BOUND, not a measurement: the registered value is the published "
          "lower limit on E_LV, so the model passes only if its own E_LV "
          "EXCEEDS it. Registered under geometry because the quantity it "
          "constrains in this model is the ruler a/ell_P (F79/F107), not any "
          "lepton-sector parameter.",
))

register(Constant(
    symbol="E_LV_e_sub_min_GeV",
    value=1.0e24,
    units="GeV",
    exactness="external",
    provenance=("F327",),
    derivation="Li & Ma, arXiv:2204.02956, the complementary SUBLUMINAL n=1 "
               "electron bound from Crab synchrotron radiation (a subluminal "
               "dispersion lowers the maximum synchrotron energy an electron "
               "can reach). Same convention as E_LV_e_sup_min_GeV, s = +1.",
    sector="geometry",
    tol=0.0,
    notes="Weaker than the superluminal bound by ~2 decades, and quoted "
          "separately because the model's coefficient is CHIRALITY- and "
          "DIRECTION-odd: whichever sign a given sky octant carries for "
          "electrons, the opposite sign is carried by positrons and by the "
          "antipodal octant, so BOTH bounds apply and neither can be evaded "
          "by choosing the sign.",
))

register(Constant(
    symbol="m_e_GeV",
    value=0.51099895000e-3,
    units="GeV",
    exactness="external",
    provenance=("CODATA",),
    derivation="CODATA/PDG electron rest mass. Enters F327 only through the "
               "vacuum-Cherenkov threshold E_th = (m_e^2 M_Pl / eta)^(1/3).",
    sector="geometry",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/interactions/derive_chiral_liv_bound.py", "m_e_GeV",
             kind="import",
             note="F327: the vacuum-Cherenkov threshold (m_e^2 M_Pl/eta)^(1/3)."),
        Site("src/casim/engine/interactions/qed_renormalization.py", "M_E_GEV",
             kind="import",
             note="was a bare literal 0.51099895e-3 until F327 registered the "
                  "constant and found five independent copies of it in the tree."),
        Site("src/casim/engine/interactions/qed_uv_completion.py", "scales",
             kind="import",
             note="U6 decoupling scale table; was a literal."),
        Site("src/casim/engine/interactions/qed_uv_completion.py", "me",
             kind="import",
             note="U7 perturbative-domain log; was a second literal in the same "
                  "file as the U6 one."),
        Site("src/casim/engine/forks/gravity/gr_fork_F199_amplitude_mode_stability.py",
             "m_e_GeV", kind="runtime",
             note="inline 0.51099895e-3; a fork is a preserved falsification "
                  "record and its arithmetic is left as written."),
        Site("src/casim/engine/forks/gravity/gr_fork_F201_kev_from_eg_texture.py",
             "m_e_GeV", kind="runtime",
             note="inline 0.51099895e-3; same reason as the F199 fork."),
    ),
    notes="Registered under geometry rather than lepton because its single "
          "use is the F327 LIV threshold, which is a statement about the "
          "lattice ruler; the lepton sector's own mass work (F253-F256) uses "
          "shape angles and ratios, never an absolute m_e in GeV.",
))

register(Constant(
    symbol="E_crab_photon_max_GeV",
    value=1.12e6,
    units="GeV",
    exactness="external",
    provenance=("F327",),
    derivation="LHAASO's highest-energy photon from the Crab Nebula, "
               "1.12 +- 0.09 PeV (Cao et al., Science 373 (2021) 425; used as "
               "the input of Li & Ma, arXiv:2204.02956). F327 uses it as a "
               "CONSERVATIVE FLOOR on the parent electron energy: inverse "
               "Compton hands the photon at most the electron's energy, so "
               "E_e >= E_gamma, and the true inferred parent is higher.",
    sector="geometry",
    tol=0.0,
    sites=(
        Site("src/casim/engine/interactions/derive_chiral_liv_bound.py",
             "E_crab_photon_max_GeV", kind="import",
             note="F327 leg C3: the vacuum-Cherenkov threshold is compared "
                  "against this. Registered after the 2026-08-26 attack pass "
                  "found it as a bare literal in two places and mislabelled "
                  "as the parent ELECTRON energy."),
    ),
))
