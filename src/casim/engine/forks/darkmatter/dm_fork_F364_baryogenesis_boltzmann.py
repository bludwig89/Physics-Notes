"""
dm_fork_F364_baryogenesis_boltzmann.py
=======================================
Finding F364 — rubric row K6 (baryogenesis): a real Boltzmann/quantum-kinetic
computation of the baryon asymmetry Y_B = n_B/s, replacing F202's Sakharov-
conditions CHECKLIST with an actual NUMBER.

F202 established (NOT re-attacked here) that all three Sakharov conditions are
available in the model's own structure: L-violation is derived (F47 anti-linear
Majorana step), CP violation is available (F53: three-generation Dirac+Majorana
phases), and out-of-equilibrium + SU(2)_L sphalerons supply the rest. F202's own
honest caveat: "the asymmetry's size (CP phases + N2,3 degeneracy) is the free,
inherited residual" — this fork BUILDS THE MACHINE that turns that residual into
a computed Y_B, and quantifies exactly how large the free residual has to be.

METHOD (resonant / ARS-adjacent leptogenesis, leading order, unflavoured):

  1. Heavy Majorana masses M2, M3 come from the model's OWN F201 Z3/E_g
     texture (M_R0=1 GeV, delta_nu=134.86 deg — the SAME landing point F201
     already used for the keV DM sterile M1) — NOT re-tuned here. F201's
     texture gives M2~0.40 GeV, M3~5.60 GeV: an O(1) split, not automatically
     near-degenerate.

  2. The Dirac mass matrix M_D (3x2, flavour x heavy) is fixed by the
     Casas-Ibarra parametrisation: it reproduces the MEASURED light-neutrino
     masses and PMNS mixing (external, standard oscillation global-fit values,
     minimal seesaw m1=0) for ANY complex orthogonal R(omega) — omega is
     exactly the free CP phase F202 already flagged as not derived.

  3. CP asymmetry: the Pilaftsis-Underwood regulated RESONANT formula (valid
     at any mass splitting, not only exact degeneracy — the same formula
     Drewes-Garbrecht 2013 use for GeV-seesaw leptogenesis without imposing
     exact degeneracy).

  4. Standard vanilla-leptogenesis Boltzmann equations (K1/K2 Bessel time
     dilation, decay + inverse-decay washout) integrated with a FREEZE-IN
     initial condition (Y_N=0 at high T — these Yukawas never reach thermal
     equilibrium at the relevant epoch) from T_i >> T_sph down to the standard
     sphaleron freeze-out T_sph=131.7 GeV (D'Onofrio-Rummukainen 2014), where
     the accumulated Y_{B-L} is converted via the standard SM sphaleron factor
     c_sph=28/79 (Harvey-Turner 1990, N_f=3, N_H=1 — inherited, not re-derived
     for this model's own Higgs-free U(1)_Y content: an explicit caveat below).

  5. Condition-1 (B-violation) MAGNITUDE: Gamma_sph/H in the symmetric phase
     (T > T_sph) is computed from the model's OWN sin^2(theta_W)=2/9 (F320)
     -> alpha_W, confirming sphalerons are parametrically fast (>>H) above
     T_sph, giving condition 1 an actual rate, not just "present".

RESULT (leading order, honestly scoped — see caveats):
  - At the model's OWN native M2, M3 (untuned), scanning ONLY the free CP
    phase omega caps out ~10-11 decades short of the measured Y_B before
    Yukawa-driven washout self-limits further growth.
  - Scanning ONLY the free N2,3 mass-splitting (holding Yukawas fixed, small
    and perturbative) shows a sharp resonance: Y_B matches the measured value
    for Delta M_23/M in a narrow window around ~1e-17 — a degeneracy roughly
    16 orders of magnitude finer than the O(1) split (~1.7) the F201 texture
    actually predicts at the keV-DM-producing angle.
  - So: the machine runs, produces real numbers, and both free "residual"
    levers F202 already named are now QUANTIFIED — and both show the model's
    own natural landing point is parametrically far from viable baryogenesis
    without additional, unexplained tuning beyond what F201/F202 already
    flagged as free.

Self-contained, real arithmetic (numpy + scipy.special/scipy.integrate — no
chiral transforms; this stays outside casim.numerics per D8 since it is a
particle-cosmology rate calculation, not a lattice/chiral kernel).
"""

import json
import os
import numpy as np
from scipy.special import kv
from scipy.integrate import solve_ivp
from casim.constants import sin2_thetaW_onshell

SQRT2 = np.sqrt(2.0)
ZETA3 = 1.2020569031595943015

# ---------------------------------------------------------------------------
# Cosmology / SM-inherited constants (flagged: standard values, not re-derived
# for this model's specific Higgs-free gauge content)
# ---------------------------------------------------------------------------
M_PL_GEV = 1.221e19
GSTAR = 106.75                  # SM relativistic dof at the GeV-TeV era (standard)
T_SPH_GEV = 131.7                # sphaleron freeze-out (D'Onofrio-Rummukainen 2014)
C_SPH = 28.0 / 79.0               # sphaleron B<-B-L conversion, N_f=3, N_H=1 (Harvey-Turner 1990)
V_EW_GEV = 246.22                 # v = (sqrt2 G_F)^-1/2 -- same convention already used in
                                   # derive_higgs_bhl_compositeness.py's V_EW_GEV
Y_B_OBSERVED = 8.7e-11            # n_B/s, Planck -- same constant F202's own fork already used
SIN2_THETAW_MODEL = float(sin2_thetaW_onshell)  # registry import (F320), not a literal
ALPHA_EM = 1.0 / 137.035999       # representative low-energy value (order-of-magnitude use only)

# ---------------------------------------------------------------------------
# 1. F201's OWN Z3/E_g texture -- the SAME landing point (M_R0, delta_nu),
#    NOT re-tuned. Reproduces the F201 keV/GeV split exactly.
# ---------------------------------------------------------------------------
M_R0_GEV = 1.0
DELTA_NU_DEG = 134.86


def z3_sqrt_masses(delta_rad):
    return np.array([1.0 + SQRT2 * np.cos(delta_rad + 2 * np.pi * a / 3.0) for a in range(3)])


def f201_texture_masses():
    s = z3_sqrt_masses(np.radians(DELTA_NU_DEG))
    m = np.abs(M_R0_GEV * s ** 2)
    m.sort()
    M1, M2, M3 = m
    return {"M1_GeV": float(M1), "M1_keV": float(M1 * 1e6), "M2_GeV": float(M2), "M3_GeV": float(M3),
            "M23_split_relative": float(abs(M3 - M2) / (0.5 * (M2 + M3))),
            "note": "F201's own landing point (M_R0=1 GeV, delta_nu=134.86 deg) — not re-tuned here"}


# ---------------------------------------------------------------------------
# 2. Light-neutrino data (EXTERNAL: standard oscillation global-fit central
#    values, normal ordering; minimal seesaw m1=0 since only N2,N3 seed the
#    active sector — N1's Yukawa is the F201 feeble DM-sterile coupling and
#    is dropped here, standard nuMSM practice, its seesaw contribution to
#    active masses is ~1e-4 eV, sub-percent of the atmospheric splitting)
# ---------------------------------------------------------------------------
DM21_SQ_EV2 = 7.42e-5
DM31_SQ_EV2 = 2.514e-3
M2_LIGHT_GEV = np.sqrt(DM21_SQ_EV2) * 1e-9
M3_LIGHT_GEV = np.sqrt(DM31_SQ_EV2) * 1e-9
TH12, TH23, TH13, DELTA_CP = (np.radians(x) for x in (33.44, 49.2, 8.57, 194.0))


def pmns_matrix(th12, th23, th13, delta):
    c12, s12 = np.cos(th12), np.sin(th12)
    c23, s23 = np.cos(th23), np.sin(th23)
    c13, s13 = np.cos(th13), np.sin(th13)
    return np.array([
        [c12 * c13, s12 * c13, s13 * np.exp(-1j * delta)],
        [-s12 * c23 - c12 * s23 * s13 * np.exp(1j * delta),
         c12 * c23 - s12 * s23 * s13 * np.exp(1j * delta), s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * np.exp(1j * delta),
         -c12 * s23 - s12 * c23 * s13 * np.exp(1j * delta), c23 * c13]], dtype=complex)


U_PMNS = pmns_matrix(TH12, TH23, TH13, DELTA_CP)
U_HAT = U_PMNS[:, 1:3]   # columns for (m2, m3); m1=0 dropped


def casas_ibarra_MD(M2h, M3h, omega):
    """3x2 Dirac mass matrix reproducing the measured light spectrum exactly,
    for ANY complex omega=omega_R+i*omega_I (the free CP-violating angle)."""
    Dm_sqrt = np.diag([np.sqrt(M2_LIGHT_GEV), np.sqrt(M3_LIGHT_GEV)])
    DM_sqrt = np.diag([np.sqrt(M2h), np.sqrt(M3h)])
    R = np.array([[np.cos(omega), np.sin(omega)], [-np.sin(omega), np.cos(omega)]], dtype=complex)
    return 1j * U_HAT @ Dm_sqrt @ R @ DM_sqrt


def seesaw_reproduction_residual(MD, Mheavy):
    """Check: does M_D correctly regenerate the input light masses? (should be ~0)"""
    MRinv = np.diag(1.0 / np.array(Mheavy, dtype=float))
    m_nu = MD @ MRinv @ MD.T
    ev = np.sort(np.sqrt(np.abs(np.linalg.eigvalsh(m_nu @ m_nu.conj().T))))
    target = np.sort([0.0, M2_LIGHT_GEV, M3_LIGHT_GEV])
    return float(np.max(np.abs(ev - target) / target[1:].mean()))


# ---------------------------------------------------------------------------
# 3. Widths and the Pilaftsis-Underwood regulated resonant CP asymmetry.
#    A well-conditioned (r=Delta M/M) variant avoids float64 cancellation
#    when scanning tiny mass splittings (needed for the resonance scan).
# ---------------------------------------------------------------------------
def widths_and_epsilon(MD, Mheavy):
    Y = SQRT2 * MD / V_EW_GEV
    YtY = Y.conj().T @ Y
    M = np.array(Mheavy, dtype=float)
    Gamma = np.array([YtY[I, I].real * M[I] / (8 * np.pi) for I in range(2)])
    eps = np.zeros(2)
    for I in range(2):
        J = 1 - I
        den = YtY[I, I].real * YtY[J, J].real
        if den <= 0:
            continue
        num = (YtY[I, J] ** 2).imag
        reg = (M[I] ** 2 - M[J] ** 2) * M[I] * Gamma[J] / ((M[I] ** 2 - M[J] ** 2) ** 2 + M[I] ** 2 * Gamma[J] ** 2)
        eps[I] = (num / den) * reg
    return Gamma, eps


def widths_and_epsilon_wellconditioned(MD, M2v, r):
    """M3 = M2*(1+r); uses M3^2-M2^2 = M2^2*(2r+r^2) directly (no cancellation)
    so the resonance can be scanned down to r ~ 1e-20 without losing precision."""
    M3v = M2v * (1 + r)
    Y = SQRT2 * MD / V_EW_GEV
    YtY = Y.conj().T @ Y
    Mh = [M2v, M3v]
    Gamma = np.array([YtY[I, I].real * Mh[I] / (8 * np.pi) for I in range(2)])
    dM2 = M2v ** 2 * (2 * r + r ** 2)   # = M3^2 - M2^2, well-conditioned
    eps = np.zeros(2)
    den0 = YtY[0, 0].real * YtY[1, 1].real
    if den0 > 0:
        reg0 = (-dM2) * M2v * Gamma[1] / (dM2 ** 2 + M2v ** 2 * Gamma[1] ** 2)
        eps[0] = ((YtY[0, 1] ** 2).imag / den0) * reg0
    den1 = YtY[1, 1].real * YtY[0, 0].real
    if den1 > 0:
        reg1 = dM2 * M3v * Gamma[0] / (dM2 ** 2 + M3v ** 2 * Gamma[0] ** 2)
        eps[1] = ((YtY[1, 0] ** 2).imag / den1) * reg1
    return Mh, Gamma, eps


# ---------------------------------------------------------------------------
# 4. Cosmology + the Boltzmann/QKE integration (freeze-in -> sphaleron
#    freeze-out). Standard vanilla-leptogenesis form (Kolb-Wolfram / Buchmuller
#    -Di Bari-Plumacher), unflavoured (single effective lepton-asymmetry
#    channel -- an explicit leading-order approximation, see caveats).
# ---------------------------------------------------------------------------
def hubble(T):
    return 1.66 * np.sqrt(GSTAR) * T ** 2 / M_PL_GEV


def entropy_density(T):
    return (2 * np.pi ** 2 / 45.0) * GSTAR * T ** 3


def bessel_ratio_K1K2(z):
    if z < 1e-3:
        return (z / 2.0) * (1.0 + z ** 2 / 8.0)
    return kv(1, z) / kv(2, z)


def Y_N_eq(z, T):
    if z < 1e-3:
        n = 0.75 * (ZETA3 / np.pi ** 2) * 2 * T ** 3     # ultra-relativistic Majorana (g=2)
    else:
        M = z * T
        n = (M ** 3 / (np.pi ** 2 * z)) * kv(2, z)
    return n / entropy_density(T)


def Y_l_eq(T, g_l=6.0):
    # g_l=6: 3 flavours x 2 doublet dof, unflavoured/summed reference abundance
    return 0.75 * (ZETA3 / np.pi ** 2) * g_l * T ** 3 / entropy_density(T)


def run_boltzmann(Mheavy, Gamma, eps, T_i=1.0e5):
    """Integrate freeze-in (Y_N=0 at T_i >> T_sph) down to T_sph=131.7 GeV.
    z = M2/T. Returns (Y_B, Y_BL, solver report)."""
    M2h, M3h = Mheavy
    z_i, z_f = M2h / T_i, M2h / T_SPH_GEV
    u_i, u_f = np.log(z_i), np.log(z_f)

    def rhs(u, Y):
        z = np.exp(u)
        T = M2h / z
        YN2, YN3, YBL = Y
        z2, z3 = M2h / T, M3h / T
        r2, r3 = bessel_ratio_K1K2(z2), bessel_ratio_K1K2(z3)
        YN2eq, YN3eq = Y_N_eq(z2, T), Y_N_eq(z3, T)
        Yleq = Y_l_eq(T)
        Hz = hubble(T) * z
        src2 = (Gamma[0] / Hz) * r2 * (YN2 - YN2eq)
        src3 = (Gamma[1] / Hz) * r3 * (YN3 - YN3eq)
        wash2 = 0.5 * (Gamma[0] / Hz) * r2 * (YN2eq / Yleq) * YBL
        wash3 = 0.5 * (Gamma[1] / Hz) * r3 * (YN3eq / Yleq) * YBL
        dYN2_dz, dYN3_dz = -src2, -src3
        dYBL_dz = eps[0] * src2 + eps[1] * src3 - wash2 - wash3
        return [z * dYN2_dz, z * dYN3_dz, z * dYBL_dz]

    sol = solve_ivp(rhs, [u_i, u_f], [0.0, 0.0, 0.0], method="Radau", rtol=1e-7, atol=1e-30)
    YN2f, YN3f, YBLf = sol.y[:, -1]
    YB = C_SPH * YBLf
    return {"Y_B": float(YB), "Y_BL": float(YBLf), "Y_N2": float(YN2f), "Y_N3": float(YN3f),
            "solver_success": bool(sol.success)}


# ---------------------------------------------------------------------------
# 5. Condition-1 magnitude: sphaleron rate vs Hubble in the symmetric phase,
#    using the MODEL's own sin^2(theta_W)=2/9 (F320) -> alpha_W.
# ---------------------------------------------------------------------------
def sphaleron_rate_over_hubble(T, kappa=25.0):
    alpha_W = ALPHA_EM / SIN2_THETAW_MODEL
    Gamma_sph = kappa * alpha_W ** 5 * T ** 4          # symmetric-phase estimate (standard)
    return float(Gamma_sph / hubble(T))


# ---------------------------------------------------------------------------
# 6. The two scans this finding reports
# ---------------------------------------------------------------------------
def scan_cp_phase(omega_R=np.pi / 4, n=40, wI_max=12.0):
    """Native F201 masses fixed; scan ONLY the free CP phase omega_I."""
    tex = f201_texture_masses()
    M2v, M3v = tex["M2_GeV"], tex["M3_GeV"]
    out = []
    best = None
    for wI in np.linspace(0.0, wI_max, n):
        MD = casas_ibarra_MD(M2v, M3v, omega_R + 1j * wI)
        Gamma, eps = widths_and_epsilon(MD, (M2v, M3v))
        Y = SQRT2 * MD / V_EW_GEV
        ymax = float(np.max(np.abs(Y)))
        res = run_boltzmann((M2v, M3v), Gamma, eps)
        ratio = res["Y_B"] / Y_B_OBSERVED
        row = {"omega_I": float(wI), "Y_max": ymax, "Y_B": res["Y_B"], "ratio_to_observed": ratio}
        out.append(row)
        if ymax <= 1.0 and (best is None or abs(ratio) > abs(best["ratio_to_observed"])):
            best = row
    return {"omega_R_fixed": float(omega_R), "M2_GeV": M2v, "M3_GeV": M3v,
            "scan": out, "best_perturbative_point": best}


def scan_mass_splitting(omega=0.3 + 0.5j, r_values=None):
    """Native M2 fixed; M3=M2*(1+r), scan the free splitting r=DeltaM/M with a
    FIXED, small, perturbative Yukawa (the same CP phase throughout)."""
    tex = f201_texture_masses()
    M2v = tex["M2_GeV"]
    if r_values is None:
        r_values = np.logspace(-10, -22, 49)
    out = []
    for r in r_values:
        MD = casas_ibarra_MD(M2v, M2v * (1 + r), omega)
        Mh, Gamma, eps = widths_and_epsilon_wellconditioned(MD, M2v, r)
        res = run_boltzmann(Mh, Gamma, eps)
        ratio = res["Y_B"] / Y_B_OBSERVED
        out.append({"r": float(r), "Y_B": res["Y_B"], "ratio_to_observed": ratio})
    peak = max(out, key=lambda row: abs(row["ratio_to_observed"]))
    above1 = [row for row in out if abs(row["ratio_to_observed"]) >= 1.0]
    window = None
    if above1:
        rs = [row["r"] for row in above1]
        window = {"r_lo": float(min(rs)), "r_hi": float(max(rs))}
    return {"omega_fixed": [omega.real, omega.imag], "M2_GeV": M2v, "scan": out,
            "peak": peak, "success_window_r": window,
            "F201_native_split_r": tex["M23_split_relative"]}


def run():
    tex = f201_texture_masses()
    cp_scan = scan_cp_phase()
    split_scan = scan_mass_splitting()
    seesaw_MD = casas_ibarra_MD(tex["M2_GeV"], tex["M3_GeV"], 0.3 + 0.5j)
    seesaw_resid = seesaw_reproduction_residual(seesaw_MD, (tex["M2_GeV"], tex["M3_GeV"]))
    sph = {T: sphaleron_rate_over_hubble(T) for T in (T_SPH_GEV, 1e3, 1e6, 1e10)}

    return {
        "f201_texture_masses": tex,
        "seesaw_reproduction_residual": seesaw_resid,
        "cp_phase_scan_native_masses": cp_scan,
        "mass_splitting_resonance_scan": split_scan,
        "sphaleron_rate_over_hubble_symmetric_phase": {str(k): v for k, v in sph.items()},
        "Y_B_observed": Y_B_OBSERVED,
        "verdict": (
            "The machine now produces an actual Y_B, not a checklist. At the model's OWN "
            "F201 texture masses (M2~0.40 GeV, M3~5.60 GeV, untuned), scanning only the free "
            f"CP phase caps at ratio~{cp_scan['best_perturbative_point']['ratio_to_observed']:.2e} "
            "to observed before washout self-limits growth -- ~10-11 decades short. Scanning "
            "only the free N2,3 mass-splitting (fixed small perturbative Yukawas) shows a sharp "
            f"resonance, matching observed Y_B in a narrow window "
            f"{split_scan['success_window_r']} -- roughly 16 orders of magnitude finer than the "
            f"F201 texture's own native split ({tex['M23_split_relative']:.2f}, order-unity). "
            "Sphalerons are confirmed fast (Gamma_sph/H >> 1) in the symmetric phase above "
            "T_sph=131.7 GeV, using the model's own sin^2(theta_W)=2/9 (F320). Net: both free "
            "residuals F202 already flagged are now quantified, and the model's OWN natural "
            "landing point is parametrically far (many orders of magnitude, either lever) from "
            "viable baryogenesis without further, unexplained fine-tuning."
        ),
    }


if __name__ == "__main__":
    out = run()
    here = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", ".."))
    os.makedirs(os.path.join(root, "test-results"), exist_ok=True)
    with open(os.path.join(root, "test-results", "F364_baryogenesis_boltzmann.json"), "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(json.dumps(out, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o))
