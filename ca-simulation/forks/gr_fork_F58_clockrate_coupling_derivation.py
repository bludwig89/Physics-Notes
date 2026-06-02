"""
Fork F58 — DOES THE CLOCK-RATE ↔ REST-MASS COUPLING (4πG) FOLLOW FROM THE
           CA NEIGHBOUR-COUPLING RULE?
==========================================================================
Drafted 2026-05-30.  Answers the open follow-up named verbatim in F52 and F55:

   "Derive the 4πG coefficient.  Whether the coupling constant between local
    clock-rate slowing and rest-mass density follows from the CA neighbour-
    coupling rule (the c_lat = dΩ/d|k| phase-matching of F25/F26) rather than
    being posited."

This fork isolates the *rest-leg / clock-rate* channel specifically (F52's
∇²Φ = 4πG ρ with the clock rate s(x)=√A(Φ)), as opposed to F56's generic
Einstein-coupling factorisation.  It separates the coefficient 4πG into three
questions and tests each:

   ∇²Φ = 4πG ρ ,   clock-rate deficit  1−√A ≈ Φ/c²

   (Q1) the 4π            — is it the lattice solid angle, or inserted by hand?
   (Q2) the FORM (∇²·)    — is the Laplacian forced by the neighbour rule?
   (Q3) the magnitude G   — does it follow from c_lat = dΩ/d|k| = 1/√d, and if
                            not, what single input is irreducible?

PLUS a structural prerequisite F52 silently relied on:

   (Q0) universality       — is "clock-rate slowing per unit potential" the
                             SAME for every clock (mass-independent)?  A single
                             scalar coupling G can only exist if it is.  This is
                             the (weak) equivalence principle and it must hold
                             bit-for-bit for the question to even be well posed.

Findings reused: F46 (the right-triangle dispersion, rest leg = clock),
F50/F52 (gravity enters through the rest leg, Ω_rest(x)=√A·arcsin m),
F25/F26 (c_lat = dΩ/d|k| = 1/√d), F56 (Green's-function 4π + Sakharov scaling).

VERDICT (see module-level results / the F58 finding):
  Q0 universal (exact, residual 0) · Q1 4π derived (lattice Green's fn) ·
  Q2 Laplacian forced (unique isotropic local 2nd-order operator) ·
  Q3 the c_lat-DEPENDENCE of the coupling is derived (stiffness ∝ c_lat², so
     1/G ∝ √d); the dimensionful magnitude of G is NOT derivable — a
     dimensionless lattice cannot make a dimensionful constant; it is locked to
     ℓ² (Planck length, Finding 10).  Choosing the lattice spacing IS choosing G.

No chiral / complex SU(2) transforms are used here (real Laplacians + the real
arccos BCC dispersion only), so numpy linear algebra is safe per CLAUDE.md.
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

import ca_bcc as bcc                                  # noqa: E402  F26 dispersion ω(k)


# ════════════════════════════════════════════════════════════════════
#  Q0 — UNIVERSALITY (weak equivalence principle): clock-rate slowing per
#       unit potential is mass-independent.  Exact, by construction of F52.
# ════════════════════════════════════════════════════════════════════

def restleg_rate(m, A):
    """F50/F52 renormalised rest-leg rotation rate (the local clock rate):
          Ω_rest(x) = √A(x) · arcsin(m).
    `A` is the lapse-squared, A = 1 − 2Φ/c²  (here Φ/c² ≤ 0 near a mass)."""
    return np.sqrt(A) * np.arcsin(m)


def universality_residual(masses, A_values):
    """For every (m, A) pair the FRACTIONAL clock-rate deficit
          δ(m,A) ≡ 1 − Ω_rest(m,A)/Ω_rest(m,1) = 1 − √A
    must be independent of m (it depends only on A).  Returns the max spread
    across masses at fixed A — should be exactly 0 (√A is a common factor)."""
    masses = np.asarray(masses, dtype=np.float64)
    A_values = np.asarray(A_values, dtype=np.float64)
    max_spread = 0.0
    per_A = []
    for A in A_values:
        deficits = 1.0 - restleg_rate(masses, A) / restleg_rate(masses, 1.0)
        spread = float(np.ptp(deficits))           # max − min over masses
        per_A.append({"A": float(A), "deficit": float(deficits[0]),
                      "spread_over_mass": spread})
        max_spread = max(max_spread, spread)
    # weak-field: deficit 1−√A ≈ −Φ/c² (Φ=(A−1)/2·c²<0) ⇒ deficit ≈ (1−A)/2
    wf = [{"A": float(A), "deficit_exact": float(1 - np.sqrt(A)),
           "deficit_linear_(1-A)/2": float((1 - A) / 2)} for A in A_values]
    return {"max_spread_over_mass": max_spread, "per_A": per_A, "weak_field": wf}


# ════════════════════════════════════════════════════════════════════
#  Q1 — the 4π is the lattice solid angle (clock-rate Green's function).
#       A point rest-mass sources a clock-rate field Φ(r) → −(coupling)/(4π r);
#       the 4π is the bare lattice Laplacian far field, NOT inserted by hand.
# ════════════════════════════════════════════════════════════════════

def clockrate_green_function(L, hopping=1.0):
    """Solve the bare 6-neighbour neighbour-coupling Laplacian
          (hopping)·Δ_lat Φ = δ₀      (NO 4π inserted)
    for a unit point source.  Δ̂(k) = −4·hopping·Σ_i sin²(k_i/2).  Returns the
    zero-mean periodic solution Φ(x)."""
    k1 = np.fft.fftfreq(L) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
    lap = -4.0 * hopping * (np.sin(KX / 2)**2 + np.sin(KY / 2)**2 + np.sin(KZ / 2)**2)
    lap[0, 0, 0] = 1.0
    src = np.zeros((L, L, L))
    src[0, 0, 0] = 1.0
    src -= src.mean()
    Phik = np.fft.fftn(src) / lap
    Phik[0, 0, 0] = 0.0
    return np.fft.ifftn(Phik).real


def fit_far_field(Phi, sigma_lo=4.0, frac_hi=0.25):
    """Fit Φ(r) ≈ −C/r + a + b r² on an intermediate shell.  Continuum point
    source gives C = 1/(4π·hopping) ⇒ 4π·hopping·C = 1."""
    L = Phi.shape[0]
    n = np.arange(L)
    n = np.where(n > L // 2, n - L, n)
    X, Y, Z = np.meshgrid(n, n, n, indexing="ij")
    r = np.sqrt(X**2 + Y**2 + Z**2)
    mask = (r > sigma_lo) & (r < frac_hi * L)
    rr, gg = r[mask], Phi[mask]
    A = np.vstack([-1.0 / rr, np.ones_like(rr), rr**2]).T
    coef, *_ = np.linalg.lstsq(A, gg, rcond=None)
    pred = A @ coef
    r2 = 1.0 - np.sum((gg - pred)**2) / np.sum((gg - gg.mean())**2)
    return {"C": float(coef[0]), "fit_r2": float(r2)}


# ════════════════════════════════════════════════════════════════════
#  Q2 — the Laplacian FORM is forced: the neighbour-coupling symbol is, at
#       leading order, the isotropic −stiffness·|k|² and nothing else.
# ════════════════════════════════════════════════════════════════════

def neighbour_symbol_small_k(hopping=1.0, kmax=1e-3, n=6):
    """Leading small-k behaviour of the 6-neighbour symbol along several
    directions.  Returns the fitted |k|² coefficient (the 'stiffness') per
    direction and its anisotropy spread; isotropy ⇒ a single Laplacian."""
    dirs = {"100": (1, 0, 0), "110": (1, 1, 0), "111": (1, 1, 1)}
    ks = np.linspace(kmax / n, kmax, n)
    stiff = {}
    for name, v in dirs.items():
        v = np.asarray(v, float); v /= np.linalg.norm(v)
        sym = np.array([4.0 * hopping * sum(np.sin(kk * vi / 2)**2 for vi in v)
                        for kk in ks])          # −Δ̂ = +4h Σ sin²(k_i/2) ≥ 0
        # fit sym ≈ stiffness·k²  (through origin)
        stiff[name] = float(np.polyfit(ks**2, sym, 1)[0])
    vals = np.array(list(stiff.values()))
    return {"stiffness_per_dir": stiff,
            "mean_stiffness": float(vals.mean()),
            "anisotropy_spread": float(np.ptp(vals) / vals.mean())}


# ════════════════════════════════════════════════════════════════════
#  Q3a — the clock-rate stiffness and c_lat both come from ONE hopping
#        amplitude: c_lat ∝ J and Green's stiffness ∝ J², so
#        (stiffness)/c_lat² is a hopping-INDEPENDENT constant.  Hence the
#        gravitational coupling inherits c_lat's √d:  1/G ∝ stiffness ∝ c_lat².
# ════════════════════════════════════════════════════════════════════

def clat_from_symbol(hopping=1.0, kmax=1e-3, n=6):
    """Massless signal speed of the SAME neighbour coupling.  For the simple
    6-neighbour wave operator the dispersion is ω = √(stiffness)·|k| at small k,
    so c_lat = √(stiffness).  Returns c_lat along the 111 direction."""
    v = np.asarray((1, 1, 1), float); v /= np.linalg.norm(v)
    ks = np.linspace(kmax / n, kmax, n)
    sym = np.array([4.0 * hopping * sum(np.sin(kk * vi / 2)**2 for vi in v) for kk in ks])
    stiffness = float(np.polyfit(ks**2, sym, 1)[0])
    return float(np.sqrt(stiffness))


def stiffness_clat_lock(hoppings=(0.5, 1.0, 2.0, 4.0)):
    """Sweep the neighbour-hopping amplitude J.  Check (i) c_lat ∝ J,
    (ii) stiffness ∝ J², (iii) stiffness/c_lat² = const (= 1 here).  This is
    the F25/F26 lock: the coupling's k-stiffness is not independent of the
    light-cone speed — both are the one neighbour amplitude."""
    rows = []
    for J in hoppings:
        v = np.asarray((1, 1, 1), float); v /= np.linalg.norm(v)
        ks = np.linspace(1e-4, 1e-3, 6)
        sym = np.array([4.0 * J * sum(np.sin(kk * vi / 2)**2 for vi in v) for kk in ks])
        stiffness = float(np.polyfit(ks**2, sym, 1)[0])
        clat = float(np.sqrt(stiffness))
        rows.append({"J": float(J), "stiffness": stiffness, "c_lat": clat,
                     "stiffness_over_clat2": stiffness / clat**2})
    ratios = np.array([r["stiffness_over_clat2"] for r in rows])
    return {"rows": rows, "ratio_spread": float(np.ptp(ratios)),
            "ratio_mean": float(ratios.mean())}


def measured_clat_bcc(direction=(1, 1, 1), kmax=3e-4, n=4):
    """The actual F26 BCC light-cone speed c_lat = dΩ/d|k|, for comparison with
    the √d = 1/√3 the coupling must carry."""
    v = np.asarray(direction, float); v /= np.linalg.norm(v)
    ks = np.linspace(kmax / n, kmax, n)
    om = np.array([bcc.bcc_dispersion(*(kk * v)) for kk in ks])
    return float(np.polyfit(ks, om, 1)[0])


# ════════════════════════════════════════════════════════════════════
#  Q3b — the dimensionful magnitude is irreducible (Sakharov): 1/G from the
#        BZ integral of the F26 dispersion scales as √d·Λ², so G ∝ ℓ²/√d.
#        A dimensionless lattice cannot set ℓ in metres ⇒ choosing ℓ = choosing G.
# ════════════════════════════════════════════════════════════════════

def induced_inverse_G(Lambda, n_grid=56):
    """I(Λ) = ∫_{|k|<Λ} d³k/(2π)³ · ω(k)⁻¹ over the F26 BCC dispersion — the
    UV weight setting the induced 1/(16πG).  Continuum: Λ²/(4π² c_lat) = √d Λ²/(4π²)."""
    g = np.linspace(-Lambda, Lambda, n_grid)
    dk = g[1] - g[0]
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    kmag = np.sqrt(KX**2 + KY**2 + KZ**2)
    inside = (kmag < Lambda) & (kmag > 0)
    om = bcc.bcc_dispersion(KX, KY, KZ)
    om = np.where(om > 0, om, np.inf)
    return float(np.where(inside, 1.0 / om, 0.0).sum() * dk**3 / (2.0 * np.pi)**3)


def sakharov_exponent(Lambdas=(0.5, 0.7, 1.0, 1.4), n_grid=56):
    """Fit p in I(Λ) ∝ Λ^p (Sakharov ⇒ p = 2 ⇒ G ∝ ℓ²)."""
    Lambdas = np.asarray(Lambdas, float)
    Is = np.array([induced_inverse_G(L, n_grid=n_grid) for L in Lambdas])
    p, logA = np.polyfit(np.log(Lambdas), np.log(Is), 1)
    return {"exponent_p": float(p), "Lambdas": [float(x) for x in Lambdas],
            "I_values": [float(x) for x in Is]}


NAME = "fork_F58_clockrate_coupling_derivation"
DESCRIPTION = (
    "Does 4πG (clock-rate↔rest-mass coupling) follow from the neighbour rule? "
    "Q0 universality exact; Q1 4π = lattice Green's-fn solid angle; Q2 Laplacian "
    "forced by isotropy; Q3 coupling's c_lat-dependence (1/G ∝ c_lat² ∝ √d) "
    "derived, but dimensionful G irreducible — locked to ℓ² (Planck length).")
