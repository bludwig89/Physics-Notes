"""
Fork F56 — DERIVING THE EINSTEIN COUPLING 16πG/c⁴ FROM THE LATTICE + F25/F26
============================================================================
Drafted 2026-05-29.  A derivation *attempt* (status: partial) for the coupling
F55 had to posit.  The strategy is to factor the coupling into pieces and ask,
for each, whether the lattice fixes it:

        16πG/c⁴   =   (16π)   ×   G   ×   c⁻⁴
                      └ geom ┘    └ dimensionful ┘

PART A — the 16π is pure lattice geometry (DERIVABLE, exact)
------------------------------------------------------------
• The 4π in Newton's  ∇²φ = 4πGρ  is the far-field coefficient of the lattice
  Green's function:  the discrete Laplacian's point-source solution obeys
  G(r) → −1/(4π r).  This 4π is the solid angle of 3-D space as the lattice's
  long-wavelength modes resolve it — the SAME small-k isotropy that F25/F26
  used to define a direction-independent  c_lat = dΩ/d|k|.  (PART B test.)
• The step 4π → 16π is the trace-reversal factor (F55):  given Newton's 4π and
  the static-dust trace reversal, the tensor coupling ξ in □h̄_μν = −ξ T_μν is
  FORCED to 16πG/c⁴ (and the Einstein-tensor coupling to 8πG/c⁴).  No freedom.
  (PART A solve below.)

PART B — the dimensionful G is NOT a free number; it is the lattice spacing
---------------------------------------------------------------------------
A dimensionless lattice cannot manufacture a dimensionful constant.  What it CAN
do (Sakharov / induced gravity) is fix G in terms of the lattice cutoff:
integrating out the lattice's propagating modes induces an Einstein–Hilbert term
whose coefficient 1/(16πG) is a Brillouin-zone integral over the F26 dispersion
ω(k), UV-dominated, scaling as the cutoff squared:

        1/(16πG_ind)  ∝  ∫_BZ d³k/(2π)³ · ω(k)⁻¹  ∝  Λ²/c_lat ,   Λ = π/ℓ

so  G_ind ∝ ℓ²  — i.e. the lattice spacing is the Planck length (Finding 10's
identification, with the √d subtlety), and the phase-matching speed c_lat = 1/√d
enters the O(1) coefficient.  The exponent 2 and the c_lat dependence are
derivable; the absolute O(1) prefactor is scheme-dependent and, together with
the lattice spacing in metres, is the single irreducible input.  (PART C test.)

Net honest claim:  everything in 16πG/c⁴ except the choice of lattice spacing is
derivable — the 16π from lattice isotropy + trace reversal (exact), and the
ℓ²-scaling of G from the F26 phase-matching dispersion (Sakharov).  Choosing the
lattice spacing in physical units IS choosing G.
"""

from __future__ import annotations

import os
import sys

import numpy as np

_THIS = os.path.dirname(__file__)
if _THIS not in sys.path:
    sys.path.insert(0, _THIS)
_SIM = os.path.abspath(os.path.join(_THIS, ".."))
if _SIM not in sys.path:
    sys.path.insert(0, _SIM)

import ca_bcc as bcc                              # noqa: E402  F26 dispersion ω(k)


# ───────────────────────────────────────────────────────────────────
#  PART A — the coupling lock: 4π (Newton) ⇒ 16π (Einstein), via F55
# ───────────────────────────────────────────────────────────────────

def derive_tensor_coupling(newton_coeff=4.0 * np.pi, G=1.0, c=1.0):
    """Solve for the tensor coupling ξ in  □h̄_μν = −ξ T_μν  GIVEN:
      (i)   Newtonian limit          ∇²φ = newton_coeff · G ρ      (4πGρ)
      (ii)  weak-field metric        h₀₀ = −2φ/c²
      (iii) static-dust trace rev.   h̄₀₀ = 2 h₀₀   (F55: h̄₀₀=−4φ/c², h₀₀=−2φ/c²)
      (iv)  static dust              T₀₀ = ρ c²

    Then  ∇²h̄₀₀ = 2∇²h₀₀ = 2(−2/c²)∇²φ = (−4/c²)(newton_coeff·Gρ),
    and equating to −ξ T₀₀ = −ξ ρc²  gives  ξ = (4·newton_coeff) G/c⁴.
    For newton_coeff = 4π this is 16πG/c⁴.  The Einstein-tensor coupling is ξ/2.
    """
    xi = 4.0 * newton_coeff * G / c**4           # □h̄ = −ξ T  coupling
    einstein_tensor_coeff = xi / 2.0             # G_μν = (ξ/2) T  = 8πG/c⁴
    return {
        "newton_coeff": float(newton_coeff),
        "box_hbar_coupling_xi": float(xi),
        "xi_over_(G_c4)": float(xi / (G / c**4)),
        "einstein_tensor_coupling": float(einstein_tensor_coeff),
        "einstein_over_(G_c4)": float(einstein_tensor_coeff / (G / c**4)),
    }


# ───────────────────────────────────────────────────────────────────
#  PART B — the 4π is the lattice solid angle (no 4π inserted by hand)
# ───────────────────────────────────────────────────────────────────

def lattice_green_function_sc(L):
    """Green's function of the *bare* simple-cubic 6-neighbour Laplacian,
    solving  Δ_lat G = δ₀  with NO 4π inserted.  Δ_lat symbol on the unit
    lattice is  Δ̂(k) = −4 Σ_i sin²(k_i/2).  Returns G(x) (real, zero-mean)."""
    k1 = np.fft.fftfreq(L) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
    lap = -4.0 * (np.sin(KX / 2)**2 + np.sin(KY / 2)**2 + np.sin(KZ / 2)**2)
    lap[0, 0, 0] = 1.0                  # avoid /0; DC handled below
    src = np.zeros((L, L, L))
    src[0, 0, 0] = 1.0                  # unit point source at origin
    src -= src.mean()                   # zero-mean (periodic solvability)
    Gk = np.fft.fftn(src) / lap
    Gk[0, 0, 0] = 0.0
    return np.fft.ifftn(Gk).real


def fit_green_far_field_coefficient(G, sigma_lo=4.0, frac_hi=0.25):
    """Fit  G(r) ≈ −C/r + a + b r²  on an intermediate radial shell and return
    C and 4πC.  (Continuum: C = 1/(4π) ⇒ 4πC = 1.)"""
    L = G.shape[0]
    n = np.arange(L)
    n = np.where(n > L // 2, n - L, n)          # signed distances
    X, Y, Z = np.meshgrid(n, n, n, indexing="ij")
    r = np.sqrt(X**2 + Y**2 + Z**2)
    mask = (r > sigma_lo) & (r < frac_hi * L)
    rr = r[mask]
    gg = G[mask]
    A = np.vstack([-1.0 / rr, np.ones_like(rr), rr**2]).T
    coef, *_ = np.linalg.lstsq(A, gg, rcond=None)
    C = coef[0]
    pred = A @ coef
    r2 = 1.0 - np.sum((gg - pred)**2) / np.sum((gg - gg.mean())**2)
    return {"C": float(C), "four_pi_C": float(4.0 * np.pi * C), "fit_r2": float(r2)}


def lightcone_slope(direction, kmax=3e-4, n=4):
    """c_lat = dΩ/d|k| along `direction` from the F26 dispersion (Ω = 2ω(k/2)).
    Returns the small-k slope (expected 1/√d, isotropic)."""
    v = np.asarray(direction, dtype=np.float64)
    v = v / np.linalg.norm(v)
    ks = np.linspace(kmax / n, kmax, n)
    # composite-photon rotation Ω = 2 ω(k/2) — but its small-k slope equals the
    # single-Weyl slope, so measure ω directly (cheaper, same c_lat).
    om = np.array([bcc.bcc_dispersion(*(kk * v)) for kk in ks])
    return float(np.polyfit(ks, om, 1)[0])


# ───────────────────────────────────────────────────────────────────
#  PART C — Sakharov: induced 1/G ∝ Λ²/c_lat  ⇒  G ∝ ℓ²
# ───────────────────────────────────────────────────────────────────

def induced_inverse_G_integral(Lambda, n_grid=64):
    """Brillouin-zone integral  I(Λ) = ∫_{|k|<Λ} d³k/(2π)³ · ω(k)⁻¹  using the
    F26 BCC dispersion ω(k).  This is the UV-dominated weight that sets the
    induced Einstein–Hilbert coefficient 1/(16πG_ind) in Sakharov gravity.

    Continuum estimate (ω = c_lat|k|):  I = Λ²/(4π² c_lat) = √d Λ²/(4π²).
    """
    g = np.linspace(-Lambda, Lambda, n_grid)
    dk = g[1] - g[0]
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    kmag = np.sqrt(KX**2 + KY**2 + KZ**2)
    inside = (kmag < Lambda) & (kmag > 0)
    om = bcc.bcc_dispersion(KX, KY, KZ)
    om = np.where(om > 0, om, np.inf)
    integrand = np.where(inside, 1.0 / om, 0.0)
    return float(integrand.sum() * dk**3 / (2.0 * np.pi)**3)


def sakharov_scaling(Lambdas, n_grid=64):
    """Fit the exponent p in  I(Λ) ∝ Λ^p.  Sakharov predicts p = 2 (⇒ G ∝ ℓ²)."""
    Lambdas = np.asarray(Lambdas, dtype=np.float64)
    Is = np.array([induced_inverse_G_integral(L, n_grid=n_grid) for L in Lambdas])
    p, logA = np.polyfit(np.log(Lambdas), np.log(Is), 1)
    return {"exponent_p": float(p), "Lambdas": [float(x) for x in Lambdas],
            "I_values": [float(x) for x in Is], "logA": float(logA)}


NAME = "fork_F56_einstein_coupling_derivation"
DESCRIPTION = ("Derivation attempt for 16πG/c⁴: 16π from lattice isotropy "
               "(F25/26) + trace reversal (F55) [exact]; G∝ℓ² from the Sakharov "
               "BZ integral of the F26 dispersion [scaling]; lattice spacing is "
               "the one irreducible input.")
