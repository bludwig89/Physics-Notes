"""
gr_fork_F201_kev_from_eg_texture.py
===================================
Finding F201 — part (a): does the lattice PREFER a keV eigenvalue in the F47
Majorana matrix M_R, or is keV just a free input?

Idea.  The charged-lepton masses follow the F93/F76 Z_3 (E_g-condensate) texture
    sqrt(m_a) = M_0 [ 1 + sqrt2 cos(delta + 2 pi a/3) ],   a = 0,1,2,
the same crystal-field structure that splits the F75 T_1u generation triplet.
The right-handed Majorana sector is three copies of the SAME singlet on the SAME
BCC lattice, so its mass matrix M_R should carry the SAME texture — with its OWN
condensate angle delta_nu (a different sector can sit at a different angle).

This texture has Z_3 CANCELLATION NODES: at the angle where 1 + sqrt2 cos(phi)=0
(phi = 135 deg), one sqrt(M_a) -> 0, so that eigenvalue is parametrically light.
A light sterile is therefore NATURAL: it is the generation that sits nearest a
node, exactly as the electron is the lightest charged lepton.  This fork:
  (1) reproduces the charged-lepton hierarchy from the texture (delta_e=12.73 deg);
  (2) shows a generic delta_nu gives three distinct, mildly hierarchical M_R;
  (3) shows delta_nu near a node gives ONE parametrically light eigenvalue;
  (4) finds the delta_nu that yields M_1/M_3 ~ keV/GeV = 1e-6 and quantifies the
      tuning; with overall scale M_R0 ~ GeV this lands M_1 ~ keV.

So keV is not pinned, but ONE light sterile is structural (the texture's node),
and the value needs two inputs: the overall scale M_R0 and the node-proximity.

Self-contained, real arithmetic.
"""

import json
import os
import numpy as np

# charged-lepton data (F93 O7): the texture sits at delta_e = 12.7328 deg
DELTA_E_DEG = 12.7328
M_E, M_MU, M_TAU = 0.51099895e-3, 105.6583755e-3, 1.77686    # GeV
SQRT2 = np.sqrt(2.0)


def z3_sqrt_masses(delta_rad):
    """The F93/F76 Z_3 texture: sqrt(m_a)/M_0 = 1 + sqrt2 cos(delta + 2 pi a/3)."""
    return np.array([1.0 + SQRT2 * np.cos(delta_rad + 2 * np.pi * a / 3.0) for a in range(3)])


def masses_from_texture(delta_rad, scale=1.0):
    """Eigenvalue magnitudes m_a = (M_0 * sqrt-texture)^2 (sign-folded)."""
    s = z3_sqrt_masses(delta_rad)
    return scale * s**2


def charged_lepton_check():
    """Reproduce the charged-lepton hierarchy from the texture at delta_e."""
    s = z3_sqrt_masses(np.radians(DELTA_E_DEG))
    m = s**2
    m = np.sort(np.abs(m))
    ratios = m / m[-1]
    obs = np.sort([M_E, M_MU, M_TAU]); obs = obs / obs[-1]
    return {"delta_e_deg": DELTA_E_DEG, "texture_mass_ratios": ratios.tolist(),
            "observed_mass_ratios": obs.tolist(),
            "lightest_ratio_texture": float(ratios[0]),
            "lightest_ratio_observed": float(obs[0]),
            "note": "same Z_3 texture; electron is the near-node generation (lightest)"}


def node_angle_deg():
    """The Z_3 cancellation node: 1 + sqrt2 cos(phi) = 0 -> phi = arccos(-1/sqrt2)=135 deg.
    For branch a=0 this is delta = 135 deg (mod the 2 pi a/3 offsets)."""
    return float(np.degrees(np.arccos(-1.0 / SQRT2)))


def light_eigenvalue_vs_angle():
    """Scan delta_nu; report the smallest eigenvalue ratio M_min/M_max."""
    out = []
    for dd in [10.0, 60.0, 100.0, 130.0, 134.0, 134.9, 134.99]:
        m = np.sort(np.abs(masses_from_texture(np.radians(dd))))
        out.append({"delta_nu_deg": dd, "M_min_over_M_max": float(m[0] / m[-1])})
    return out


def find_delta_for_ratio(target_ratio=1e-6):
    """Find delta_nu near the node giving M_1/M_3 = target_ratio, and the tuning."""
    node = node_angle_deg()
    # search a small window above the node where one eigenvalue dips
    best = None
    lt = np.log10(target_ratio)
    for delta in np.linspace(node - 5.0, node + 5.0, 200001):
        m = np.sort(np.abs(masses_from_texture(np.radians(delta))))
        r = m[0] / m[-1]
        if r <= 0:
            continue
        if best is None or abs(np.log10(r) - lt) < abs(np.log10(best[1]) - lt):
            best = (delta, r)
    delta_star, ratio = best
    return {"target_ratio": target_ratio, "delta_nu_deg": float(delta_star),
            "achieved_ratio": float(ratio),
            "proximity_to_node_deg": float(abs(delta_star - node)),
            "proximity_to_node_rad": float(np.radians(abs(delta_star - node)))}


def run():
    node = node_angle_deg()
    cl = charged_lepton_check()
    scan = light_eigenvalue_vs_angle()
    tune = find_delta_for_ratio(1e-6)

    # land the physical numbers: overall scale M_R0 ~ GeV (nuMSM heavy-sterile scale)
    M_R0_GeV = 1.0
    m_min = np.sort(np.abs(masses_from_texture(np.radians(tune["delta_nu_deg"]), scale=M_R0_GeV)))[0]
    m_max = np.sort(np.abs(masses_from_texture(np.radians(tune["delta_nu_deg"]), scale=M_R0_GeV)))[-1]
    m1_keV = m_min / 1e-6     # GeV -> keV

    return {
        "texture": "sqrt(M_a) = M_R0 [1 + sqrt2 cos(delta_nu + 2 pi a/3)]  (F93/F76 Z_3 / E_g)",
        "z3_node_deg": node,
        "charged_lepton_reproduction": cl,
        "light_eigenvalue_vs_angle": scan,
        "kev_tuning": tune,
        "physical_landing": {
            "M_R0_GeV": M_R0_GeV, "delta_nu_deg": tune["delta_nu_deg"],
            "M_lightest_GeV": float(m_min), "M_lightest_keV": float(m1_keV),
            "M_heaviest_GeV": float(m_max),
            "hierarchy_M1_over_M3": float(m_min / m_max),
            "node_proximity_rad": tune["proximity_to_node_rad"],
            "tuning_severity": "modest: ~%.1e rad from the Z_3 node" % tune["proximity_to_node_rad"]},
        "verdict": ("The lattice does NOT pin keV, but it provides a NATURAL MECHANISM for one light "
                    "sterile: the F93 Z_3/E_g generation texture, applied to M_R, has cancellation "
                    "nodes where one eigenvalue -> 0. A light (keV) sterile is the generation nearest "
                    "a node — structurally the same reason the electron is the lightest charged "
                    "lepton. Hitting keV needs two inputs: the overall scale M_R0 ~ GeV (the nuMSM "
                    "heavy-sterile scale) and a node-proximity delta_nu ~ 1e-3 rad (modest tuning). "
                    "So 'one light sterile' is structural; its exact keV value is accommodated."),
    }


if __name__ == "__main__":
    out = run()
    here = os.path.dirname(__file__)
    # C6: five '..' — this fork moved from the legacy forks/ dir (2 levels below
    # the repo root) to src/casim/engine/forks/<sector>/ (5 levels). Same dir.
    root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", ".."))
    os.makedirs(os.path.join(root, "test-results"), exist_ok=True)
    with open(os.path.join(root, "test-results", "F201_kev_from_eg_texture.json"), "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(json.dumps(out, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o))
