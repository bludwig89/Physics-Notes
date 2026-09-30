"""
NB-002 (p.1) vs NB-049 (p.42): Fourier-mode convention self-consistency.

p.1 (NB-002) writes (3D, but we test the 1D analogue -- the power-counting argument is
dimension-independent given below):
    phi_k = ((2 pi)^3 2 omega_k)^{-1/2} * INT phi(x) e^{ikx} d^3x        ... (A, forward)
    phi(x) = (2 pi)^3 * INT phi_k (2 omega_k)^{1/2} e^{-ikx} d^3x        ... (B, "inverse", as transcribed)

p.42 (NB-049) writes:
    phit(k) = 2 omega_k * INT phi(x) e^{ikx} d^3x                       ... (C, forward)
    phi(x) = INT phit(k) e^{-ikx} d^3k / ((2 pi)^3 2 omega_k)           ... (D, inverse)
and the notebook ITSELF verifies (D) is self-consistent with (C) via the delta-function
identity (2 pi)^3 delta^3(x) = INT e^{ikx} d^3k (lines 1021-1033 of the transcription).

This script checks, numerically in 1D (the delta-function/Fourier-pair algebra is
dimension-independent -- only the power of (2 pi) picked up by the delta-function identity
changes with dimension, and that power is what we are checking), whether:
  1. convention (C)/(D) [p.42] round-trips a test function phi(x) back to itself
  2. convention (A)/(B) AS LITERALLY TRANSCRIBED on p.1 does NOT round-trip
  3. what power of (2 pi) convention (B) NEEDS to round-trip correctly

Uses numerical quadrature (scipy), not symbolic delta functions, so this is an actual
number-producing check, not a restatement of the algebra.
"""
import numpy as np
from scipy import integrate
import json, pathlib

# 1D test function and its "mass" (arbitrary, both omega_k are the same weight function so
# it cancels in the round-trip -- this isolates the (2 pi) power question cleanly)
m = 1.3

def omega(k):
    return np.sqrt(k**2 + m**2)

def phi(x):
    return np.exp(-x**2 / 2.0)  # normalized-ish test bump

def forward_transform(k, prefactor_fn):
    integrand_re = lambda x: phi(x) * np.cos(k * x)
    integrand_im = lambda x: phi(x) * np.sin(k * x)
    re, _ = integrate.quad(integrand_re, -12, 12, limit=200)
    im, _ = integrate.quad(integrand_im, -12, 12, limit=200)
    return prefactor_fn(k) * (re + 1j * im)


def round_trip(x0, forward_prefactor, inverse_prefactor, k_max=15.0):
    """phi_reconstructed(x0) = INT phit(k) * inverse_prefactor(k) * e^{-ikx0} dk"""
    def integrand_re(k):
        val = forward_transform(k, forward_prefactor) * inverse_prefactor(k) * np.exp(-1j * k * x0)
        return val.real

    def integrand_im(k):
        val = forward_transform(k, forward_prefactor) * inverse_prefactor(k) * np.exp(-1j * k * x0)
        return val.imag

    re, _ = integrate.quad(integrand_re, -k_max, k_max, limit=400)
    im, _ = integrate.quad(integrand_im, -k_max, k_max, limit=400)
    return re + 1j * im


x0 = 0.7
phi_true = phi(x0)

# --- Convention (C)/(D), p.42: forward prefactor 2*omega_k, inverse prefactor 1/((2pi)*2*omega_k)
# (1D analogue of d^3k/((2pi)^3 2 omega_k): the (2 pi) power tracks dimension, so in 1D it's (2pi)^1)
recon_CD = round_trip(
    x0,
    forward_prefactor=lambda k: 2 * omega(k),
    inverse_prefactor=lambda k: 1.0 / (2 * np.pi * 2 * omega(k)),
)

# --- Convention (A)/(B) AS LITERALLY TRANSCRIBED on p.1: forward prefactor ((2pi)*2*omega_k)^{-1/2}
# (1D analogue), inverse prefactor (2 pi)^{1} * (2 omega_k)^{1/2}  [note: SAME sign/power of (2pi)
# as transcribed -- (2 pi)^{+d} on the inverse, not (2 pi)^{-d}]
recon_AB_as_written = round_trip(
    x0,
    forward_prefactor=lambda k: 1.0 / np.sqrt(2 * np.pi * 2 * omega(k)),
    inverse_prefactor=lambda k: (2 * np.pi) * np.sqrt(2 * omega(k)),
)

# --- Convention (A) forward, but with the CORRECTED inverse power (2 pi)^{-d/2} that self-consistency
# actually requires (derived analytically: phi_k = A(k) phihat(k), phihat(k)=FT(phi), A(k)=((2pi)2wk)^-1/2
# so phi(x) = INT phihat(k) e^{-ikx} dk/(2pi) = INT phi_k/A(k) e^{-ikx} dk/(2pi)
#           = INT phi_k * sqrt(2wk) * (2pi)^{1/2} e^{-ikx} dk / (2pi) = INT phi_k sqrt(2wk) e^{-ikx} dk (2pi)^{-1/2})
recon_AB_corrected = round_trip(
    x0,
    forward_prefactor=lambda k: 1.0 / np.sqrt(2 * np.pi * 2 * omega(k)),
    inverse_prefactor=lambda k: np.sqrt(2 * omega(k)) / np.sqrt(2 * np.pi),
)

result = {
    "build": "NB-002 vs NB-049",
    "test_point_x0": x0,
    "phi_true": phi_true,
    "p42_convention_CD_reconstruction": {"re": recon_CD.real, "im": recon_CD.imag},
    "p42_matches_true_to_1pct": bool(abs(recon_CD.real - phi_true) < 0.01 and abs(recon_CD.imag) < 0.01),
    "p1_convention_AB_as_transcribed_reconstruction": {
        "re": recon_AB_as_written.real, "im": recon_AB_as_written.imag
    },
    "p1_as_transcribed_matches_true_to_1pct": bool(
        abs(recon_AB_as_written.real - phi_true) < 0.01 and abs(recon_AB_as_written.imag) < 0.01
    ),
    "p1_convention_AB_with_corrected_2pi_power_reconstruction": {
        "re": recon_AB_corrected.real, "im": recon_AB_corrected.imag
    },
    "p1_corrected_matches_true_to_1pct": bool(
        abs(recon_AB_corrected.real - phi_true) < 0.01 and abs(recon_AB_corrected.imag) < 0.01
    ),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-002_fourier_convention.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
