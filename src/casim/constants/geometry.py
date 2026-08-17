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
        Site("src/casim/engine/particles/dirac_bcc.py", "C_LAT_3D", kind="import"),
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
