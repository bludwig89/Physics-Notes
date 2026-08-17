"""
gr_fork_F199_amplitude_mode_stability.py
========================================
Finding F199 — taking F198's freeze-out route at face value: work out the E_g
amplitude mode's mass and ANNIHILATION/DECAY channels from F73/F93, and ask
whether Omega_DM = 0.26 actually falls out.

It does not — for a reason more basic than the abundance: STABILITY.

Two distinct "amplitude modes" must be separated (this is the F197/F198 fix):
  (1) the ELECTROWEAK symmetry-breaking condensate's radial mode = the F73
      Cooper-pair scalar = the observed 125 GeV Higgs.  It decays (Gamma_H ~ 4
      MeV -> tau ~ 1.6e-22 s).  Observed, not dark.
  (2) the F93 SECOND-SHELL E_g condensate's amplitude mode — the scalar F197/F198
      actually meant.  But this condensate's DEFINING role is to set the charged-
      lepton mass hierarchy (it is the crystal field on the T_1u triplet, F93 O1).
      So its amplitude fluctuation couples LINEARLY to the lepton mass operator,
      g_l ~ m_l / f, and DECAYS to lepton pairs.

A thermal relic must be cosmologically stable.  This fork computes the E_g
amplitude mode's decay width to leptons and its lifetime, and compares to the
age of the universe.  The lifetime is ~1e-21 s — 38 orders below cosmological.
So the freeze-out WIMP window of F198 is moot: the E_g sector has no stable
relic, because the same coupling that would set its abundance also makes it
decay.  The obstruction MOVES from "abundance" to "stability/identity": dark
matter needs a conserved charge (a Z2/U(1)) that the E_g condensate lacks.

Self-contained, real arithmetic.  Mirrors the gr_fork_F19x posture.
"""

import json
import os
import numpy as np

# ── constants ─────────────────────────────────────────────────────
HBAR_GEV_S = 6.582119569e-25      # GeV·s
AGE_UNIVERSE_S = 4.35e17          # s  (13.8 Gyr)
HUBBLE_TIME_S  = 4.55e17          # s  (1/H0)

# lepton masses (GeV, PDG)
M_E, M_MU, M_TAU = 0.51099895e-3, 105.6583755e-3, 1.77686
LEPTONS = {"e": M_E, "mu": M_MU, "tau": M_TAU}

# scales
V_EW   = 246.0                    # GeV   electroweak VEV
F_COND = 123.11                   # GeV   E_g / Stueckelberg condensate scale (F44/F73)
M_HIGGS = 125.25                  # GeV   observed
GAMMA_HIGGS = 4.07e-3             # GeV   SM Higgs total width (~4 MeV)


def f73_composite_mass(m_c_lat):
    """F73 exact composite-mass law for a spin-0 bound pair of equal constituents:
    m_H = sin(2 arcsin m_c) = 2 m_c sqrt(1-m_c^2).  At EW scale m_lat<<1 -> free sum."""
    return float(2 * m_c_lat * np.sqrt(1 - m_c_lat**2))


def higgs_mode():
    """Mode (1): the F73 electroweak radial mode = observed 125 GeV Higgs. Decays."""
    tau = HBAR_GEV_S / GAMMA_HIGGS
    return {"identity": "electroweak radial mode = observed 125 GeV Higgs (F73)",
            "mass_GeV": M_HIGGS, "width_GeV": GAMMA_HIGGS, "lifetime_s": tau,
            "stable_on_cosmo_time": bool(tau > AGE_UNIVERSE_S),
            "is_dark_matter": False,
            "note": "observed at LHC; decays to bb/WW/ZZ -> not dark matter"}


def scalar_to_leptons_width(m_S, f=F_COND):
    """Mode (2): the E_g second-shell amplitude mode. It modulates lepton masses,
    so it couples as g_l = m_l / f (Yukawa).  Width to l+l-:
        Gamma = sum_l (g_l^2 m_S / 8pi) (1 - 4 m_l^2/m_S^2)^{3/2}, kinematics allowed."""
    g = 0.0
    chans = {}
    for name, m_l in LEPTONS.items():
        if m_S <= 2 * m_l:
            chans[name] = 0.0
            continue
        g_l = m_l / f
        beta = (1 - 4 * m_l**2 / m_S**2) ** 1.5
        gamma = g_l**2 * m_S / (8 * np.pi) * beta
        chans[name] = float(gamma)
        g += gamma
    return float(g), chans


def eg_amplitude_mode(m_S=None, f=F_COND):
    """Mode (2): mass scale set by the E_g Landau curvature ~ f (F73 says the
    natural scalar scale is the condensate scale). Compute decay to leptons."""
    if m_S is None:
        m_S = f                     # natural: amplitude (radial) mode at the condensate scale
    gamma, chans = scalar_to_leptons_width(m_S, f)
    tau = HBAR_GEV_S / gamma if gamma > 0 else np.inf
    return {"identity": "E_g second-shell condensate amplitude mode (sets lepton masses, F93 O1)",
            "mass_GeV": m_S, "f_GeV": f, "coupling_g_tau": M_TAU / f,
            "width_GeV": gamma, "channels_GeV": chans, "lifetime_s": tau,
            "dominant_channel": max(chans, key=chans.get) if chans else None,
            "stable_on_cosmo_time": bool(tau > AGE_UNIVERSE_S),
            "orders_below_cosmo": float(np.log10(AGE_UNIVERSE_S / tau)) if np.isfinite(tau) and tau > 0 else None,
            "is_dark_matter": bool(tau > AGE_UNIVERSE_S)}


def angular_mode_decay(f=F_COND, lam6=0.05):
    """Mode (3): the light angular (axion-like) mode. Couples to lepton-mass
    DIFFERENCES (derivative/anomaly-suppressed), but still to leptons. Even
    ignoring F198's ~15-order under-abundance, it is not protected. Illustrative
    light mass m_a ~ sqrt(lam6)*(low scale)."""
    m_a = np.sqrt(lam6) * 27e-3        # GeV, ~6 MeV illustrative (light)
    # if m_a < 2 m_e it cannot decay to e+e-; then decays to 2 photons (anomaly),
    # very long-lived but ALSO under-abundant (F198). Mark both.
    can_decay_ee = m_a > 2 * M_E
    return {"identity": "E_g angular (axion-like) mode",
            "mass_GeV": float(m_a), "can_decay_to_ee": bool(can_decay_ee),
            "abundance_verdict": "under-produced by ~1e15 (F198)",
            "note": "even if long-lived (if below e+e- threshold), it is far too rare to be the DM (F198)"}


def viable_relic_requirement():
    """What a stable thermal relic actually needs, and whether E_g supplies it."""
    return {
        "requirement": "a conserved charge (Z2/U(1)) making the relic the LIGHTEST "
                       "state carrying it, so it cannot decay to SM",
        "Eg_condensate_has_it": False,
        "why_not": "the E_g amplitude mode is even under the D_2h stabilizer and couples "
                   "linearly to the lepton mass operator (its defining role) -> no symmetry "
                   "forbids S -> l+l-",
        "model_native_candidates": [
            "a STERILE-sector excitation (no SM gauge charge; F191 'sterile-sector' hint)",
            "a topologically conserved lattice excitation (orthorhombic-domain texture / "
            "skyrmion of U(x)) carrying a winding number",
            "the lightest state of a hidden conserved lattice charge (a 'dark baryon', "
            "Z3-centre analog of F97)"],
        "status": "directions, not derivations — flagged speculative",
    }


def run():
    higgs = higgs_mode()
    eg_amp = eg_amplitude_mode()
    # also scan a few masses to show instability is generic across the EW-TeV range
    scan = []
    for m_S in [10.0, 50.0, 123.11, 500.0, 3000.0]:
        g, _ = scalar_to_leptons_width(m_S)
        tau = HBAR_GEV_S / g if g > 0 else np.inf
        scan.append({"m_S_GeV": m_S, "lifetime_s": float(tau),
                     "orders_below_age": float(np.log10(AGE_UNIVERSE_S / tau))})
    ang = angular_mode_decay()
    req = viable_relic_requirement()

    return {
        "two_modes_separated": {
            "electroweak_higgs": higgs,
            "Eg_amplitude_mode": eg_amp,
        },
        "instability_scan": scan,
        "angular_mode": ang,
        "freezeout_moot": {
            "F198_found_WIMP_window": True,
            "but_relic_must_be_stable": True,
            "Eg_amplitude_lifetime_s": eg_amp["lifetime_s"],
            "age_of_universe_s": AGE_UNIVERSE_S,
            "stable": eg_amp["stable_on_cosmo_time"],
            "conclusion": "freeze-out abundance is undefined for an unstable state; the WIMP "
                          "window of F198 cannot be realised by the E_g amplitude mode"},
        "viable_relic_requirement": req,
        "verdict": ("Working out the amplitude mode from F73/F93: the EW radial mode is the "
                    "observed 125 GeV Higgs (decays), and the E_g second-shell amplitude mode "
                    "couples to leptons as g_l=m_l/f (it IS the lepton-mass crystal field), so it "
                    "decays in ~1e-21 s — 38 orders below cosmological. Omega_DM=0.26 does NOT fall "
                    "out: the E_g sector has no STABLE relic. The obstruction moves from abundance "
                    "to stability/identity — dark matter needs a conserved charge the E_g condensate "
                    "lacks (sterile sector / topological winding / hidden conserved charge)."),
    }


if __name__ == "__main__":
    out = run()
    here = os.path.dirname(__file__)
    # C6: five '..' — this fork moved from the legacy forks/ dir (2 levels below
    # the repo root) to src/casim/engine/forks/<sector>/ (5 levels). Same dir.
    root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", ".."))
    os.makedirs(os.path.join(root, "test-results"), exist_ok=True)
    with open(os.path.join(root, "test-results", "F199_amplitude_mode_stability.json"), "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(json.dumps(out, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o))
