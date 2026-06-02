"""
test_F66_allsky_birefringence_anisotropy.py
===========================================

Does the BCC birefringence anisotropy rescue a Planck-scale cell size a from
the vacuum-birefringence polarization bound?

Context.  F65 showed the two photon helicities ride the two BCC chiral branches
Omega^pm, so the model predicts LINEAR (dim-5, CPT-odd) vacuum birefringence.
With the F64 cell size a = 6.16e-35 m (g*=16) the body-diagonal effect overshoots
the GRB-polarimetry bound by ~14-15 decades.  But the effect is ANISOTROPIC: zero
along cube axes, maximal along body diagonals.  This script asks whether that
anisotropy can suppress the signal for real (generic-sky-position) sources by the
~10^14 needed -- or only by an O(1) factor.

Approach
  1. Derive + numerically verify the directional birefringence law
        DeltaOmega(k, n_hat) = Omega^+ - Omega^- = -(k^2/3) * n_x n_y n_z   (small k)
     against the exact BCC dispersion (closed-form, no numpy chiral eig).
  2. Map to the standard Myers-Pospelov dim-5 parameter
        eta(n_hat) = (a/ell_P)/(2*sqrt3) * |n_x n_y n_z|,   eta_max = (a/ell_P)/18.
  3. Monte-Carlo the all-sky distribution of the suppression factor
        f(n_hat) = |n_x n_y n_z| / (1/(3*sqrt3))  in [0,1]
     -> median / mean / percentiles (is a typical source suppressed?).
  4. Compute the sky fraction with eta < bound (the "protected" fraction), via MC
     plus a near-coordinate-plane analytic check, and the combined exclusion from
     N independent polarized sources.
  5. Confront real polarized sources (GRB 041219A, a high-z optical case) with the
     accumulated helicity phase slip.

Self-contained: numpy only.
"""

import numpy as np

ROOT3 = np.sqrt(3.0)
INV_ROOT3 = 1.0 / ROOT3

# ---- constants ----
c = 2.99792458e8
hbar = 1.054571817e-34
hbarc_eVm = 1.97326980e-7          # eV*m
lP = 1.616255e-35                  # m
EP_eV = 1.220890e28                # Planck energy in eV (M_Pl c^2)
GEV = 1e9

# ---- model cell size (F61/F64, g*=16 one generation incl nu_R) ----
A_OVER_LP = np.sqrt(2*np.pi*(1/12)*16) * 3**0.25     # = 3.809
a = A_OVER_LP * lP


# ----------------------------------------------------------------------
# BCC dispersion (closed form; Paper 1 Eq.15 signs per ca_bcc._bcc_uvec)
# ----------------------------------------------------------------------
def u_branch(kx, ky, kz, sign=+1):
    cx, cy, cz = np.cos(kx*INV_ROOT3), np.cos(ky*INV_ROOT3), np.cos(kz*INV_ROOT3)
    sx, sy, sz = np.sin(kx*INV_ROOT3), np.sin(ky*INV_ROOT3), np.sin(kz*INV_ROOT3)
    s = 1.0 if sign > 0 else -1.0
    return cx*cy*cz + s*sx*sy*sz


def Omega_branch(kx, ky, kz, sign=+1):
    # photon convention Omega^pm(k) = 2 omega_pm(k/2)
    return 2.0*np.arccos(np.clip(u_branch(kx/2, ky/2, kz/2, sign), -1, 1))


def dOmega_exact(kmag, nhat):
    kx, ky, kz = kmag*nhat
    return Omega_branch(kx, ky, kz, +1) - Omega_branch(kx, ky, kz, -1)


def dOmega_law(kmag, nhat):
    return -(kmag**2/3.0) * nhat[0]*nhat[1]*nhat[2]


# ----------------------------------------------------------------------
# 1. verify directional law  DeltaOmega = -(k^2/3) nx ny nz
# ----------------------------------------------------------------------
def section_1(seed=3):
    rng = np.random.default_rng(seed)
    worst = 0.0
    cases = []
    for _ in range(40):
        v = rng.standard_normal(3); nhat = v/np.linalg.norm(v)
        k = 1e-3                              # small k: leading-order regime
        ex = dOmega_exact(k, nhat)
        law = dOmega_law(k, nhat)
        if abs(ex) > 1e-18:
            rel = abs(ex-law)/abs(ex)
            worst = max(worst, rel)
    # named directions
    for name, nv in [("axis(1,0,0)", [1,0,0]),
                     ("face(1,1,0)", [1,1,0]),
                     ("body(1,1,1)", [1,1,1])]:
        nv = np.array(nv, float); nv/=np.linalg.norm(nv)
        cases.append((name, float(dOmega_exact(1e-3, nv)), float(dOmega_law(1e-3, nv))))
    return {'max_rel_err_vs_law': float(worst), 'named': cases}


# ----------------------------------------------------------------------
# 2 & 3. eta mapping + all-sky distribution of the suppression factor
# ----------------------------------------------------------------------
def eta_of_dir(nhat):
    return (A_OVER_LP/(2*ROOT3))*abs(nhat[0]*nhat[1]*nhat[2])

ETA_MAX = A_OVER_LP/18.0          # body diagonal

def sky_sample(N, seed=7):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((N, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    g = np.abs(v[:,0]*v[:,1]*v[:,2])          # |nx ny nz|
    f = g/(1/(3*ROOT3))                        # suppression factor in [0,1]
    return f, g

def section_2_3(N=4_000_000):
    f, g = sky_sample(N)
    eta = (A_OVER_LP/(2*ROOT3))*g
    pct = {p: float(np.percentile(f, p)) for p in (10,50,90,99)}
    # protected fraction: eta < bound, for several bounds
    fracs = {}
    for bound in (1e-15, 1e-16):
        fracs[f'eta<{bound:.0e}'] = float(np.mean(eta < bound))
    # MC scaling of P(f<tau) to confirm ~linear-with-log trend
    taus = np.array([1e-1,1e-2,1e-3,1e-4,1e-5])
    Pf = np.array([np.mean(f < t) for t in taus])
    return {'eta_max_bodydiag': float(ETA_MAX),
            'eta_median_sky': float(np.median(eta)),
            'f_percentiles': pct,
            'protected_fraction': fracs,
            'P_f_lt_tau': {f'{t:.0e}': float(p) for t,p in zip(taus,Pf)}}


def analytic_protected_fraction(eta_bound):
    """Near-coordinate-plane estimate of sky fraction with eta < eta_bound.

    eta = K |nx ny nz|, K = (a/lP)/(2 sqrt3).  eta<bound <=> |nx ny nz| < tau,
    tau = bound/K.  For tiny tau the region hugs the 3 coordinate planes.
    Near plane nz=0: fraction with |nz| < tau/|nx ny| integrated over the
    equator phi.  P ~ (3/pi) * tau * INT_eps^{pi/2-eps} 2/|sin 2phi| dphi.
    The integral ~ 2 ln(1/tau) (cut off self-consistently where the bands of
    two planes meet, |nx ny| ~ tau).  So P(tau) ~ (6/pi) tau ln(1/tau).
    """
    K = (A_OVER_LP/(2*ROOT3))
    tau = eta_bound/K
    if tau <= 0 or tau >= 1:
        return float('nan'), tau
    P = (6.0/np.pi)*tau*np.log(1.0/tau)
    return P, tau


# ----------------------------------------------------------------------
# 4. helicity phase slip for real polarized sources (generic orientation)
# ----------------------------------------------------------------------
def phase_slip(E_eV, L_m, nhat):
    """Accumulated phase difference between the two helicities:
       Dphi = |DeltaOmega(k_lat,nhat)| * N_ticks,  N_ticks = L/(c tau),
       k_lat = E a/(hbar c),  tau = a/(c sqrt3)."""
    klat = E_eV*a/hbarc_eVm
    dO = abs((klat**2/3.0)*nhat[0]*nhat[1]*nhat[2])
    tau = a/(c*ROOT3)
    N = L_m/(c*tau)
    return dO*N

def section_4():
    # representative comoving distances (order-of-magnitude)
    sources = [
        ("GRB041219A  ~200 keV, z~0.3", 2.0e5, 1.2e25),
        ("GRB pol  ~100 keV, z~1 (3 Gpc)", 1.0e5, 1.0e26),
        ("high-z galaxy optical 2 eV, z~2", 2.0, 1.7e26),
    ]
    nbody = np.array([1,1,1.])/ROOT3      # worst case (max effect)
    rng = np.random.default_rng(11)
    out = []
    for name, E, L in sources:
        # generic random sky direction
        v = rng.standard_normal(3); ngen = v/np.linalg.norm(v)
        out.append({'source': name,
                    'Dphi_bodydiag': phase_slip(E, L, nbody),
                    'Dphi_generic_dir': phase_slip(E, L, ngen),
                    'f_generic': float(3*ROOT3*abs(ngen[0]*ngen[1]*ngen[2]))})
    return out


if __name__ == '__main__':
    import json
    s1 = section_1()
    s23 = section_2_3()
    s4 = section_4()

    print("model cell size a =", f"{a:.3e} m =", f"{A_OVER_LP:.3f} lP")
    print("\n--- 1. directional law DeltaOmega = -(k^2/3) nx ny nz ---")
    print(f"  max rel err vs exact BCC (k=1e-3): {s1['max_rel_err_vs_law']:.2e}")
    for nm, ex, law in s1['named']:
        print(f"  {nm:14s} exact={ex:+.3e}  law={law:+.3e}")

    print("\n--- 2-3. all-sky suppression + protected fraction ---")
    print(f"  eta_max (body diag)   = {s23['eta_max_bodydiag']:.3f}")
    print(f"  eta_median (all sky)  = {s23['eta_median_sky']:.3e}")
    print(f"  suppression f pctiles = {s23['f_percentiles']}")
    print(f"  protected fraction    = {s23['protected_fraction']}")
    print(f"  MC P(f<tau)           = {s23['P_f_lt_tau']}")
    for b in (1e-15, 1e-16):
        P, tau = analytic_protected_fraction(b)
        print(f"  analytic P(eta<{b:.0e}) ~ {P:.2e}  (tau=|nxnynz|<{tau:.2e})")
    # MC power-law extrapolation (corroborates the analytic order of magnitude)
    taus = np.array([1e-3,1e-4,1e-5]); Ps = np.array([s23['P_f_lt_tau'][f'{t:.0e}'] for t in taus])
    p, logC = np.polyfit(np.log(taus), np.log(Ps), 1)
    for b in (1e-15, 1e-16):
        K = (A_OVER_LP/(2*ROOT3)); tau_f = (b/K)*3*ROOT3   # threshold in f
        P_mc = np.exp(logC)*tau_f**p
        print(f"  MC-extrap P(eta<{b:.0e}) ~ {P_mc:.2e}  (f-power p={p:.2f})")

    print("\n--- 4. helicity phase slip Dphi (rad); washout if >~1 ---")
    for r in s4:
        print(f"  {r['source']:34s} body={r['Dphi_bodydiag']:.2e}  "
              f"generic={r['Dphi_generic_dir']:.2e} (f={r['f_generic']:.2f})")

    # combined exclusion
    P15, _ = analytic_protected_fraction(1e-15)
    print("\n=== VERDICT ===")
    print(f"  Typical (median) sky suppression f = {s23['f_percentiles'][50]:.2f}"
          f"  -> O(1), NOT the ~1e-14 needed.")
    print(f"  eta_typical ~ {s23['eta_median_sky']:.1e} vs bound ~1e-15:"
          f" overshoot ~{s23['eta_median_sky']/1e-15:.0e}.")
    print(f"  Sky fraction evading the bound ~ {P15:.1e}.")
    print(f"  Prob. that N independent polarized sources ALL evade: ({P15:.0e})^N.")
    print("  => Anisotropy gives only an O(1) rescue. A single generic-position")
    print("     polarized GRB/AGN excludes a=6.2e-35 m. Model FALSIFIED at this a")
    print("     unless the lattice axes are fine-tuned to the line of sight.")
