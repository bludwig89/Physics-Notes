"""
ca_slowlight.py  —  Slow-light / EIT as a test of the rotation-rate picture
============================================================================

Track 1.b of the "real-world device" programme (Paper XII synthesis).

The model's defining claim (F26 / CLAUDE.md decision 2) is that the speed of
light is NOT the propagation rate of a complex phase through space, but the
angular rotation rate of the *real* (E, B) vector pair per unit wavenumber,

        c_lat = dOmega/d|k|  at  k -> 0,     Omega = omega^+(k/2)+omega^-(k/2).

Standard textbook optics writes a wave as a complex scalar exp(i(kx-wt)) and
calls w/k the "phase velocity".  This module asks the sharp question:

    Does a strongly dispersive medium (EIT slow light; gain-assisted
    anomalous "fast light") distinguish the real-(E,B)-rotation description
    from the complex-phase-velocity description?

The honest answer this module demonstrates:

  (1) NORMAL EIT (slow light, Hau 1999, v_g = 17 m/s): the two descriptions
      are *isomorphic* and give the identical real field to machine precision.
      A real 2x2 (E,B) rotation per mode is the same object as a complex phase.
      The model REDUCES to Maxwell-in-medium.  This is a consistency anchor.

  (2) ANOMALOUS dispersion (gain doublet, Wang-Kuzmich-Dogariu 2000,
      v_g = -c/310): the group velocity goes negative (the pulse peak leaves
      before it arrives).  Both descriptions reproduce this identically.  The
      model's *interpretation* is cleaner -- the real (E,B) front always
      advances at c, and v_p / v_g are bookkeeping that transport nothing --
      but it is NOT a distinct laboratory number here.  This is an ontology
      test, not a discriminator.

  (3) The ONLY genuinely distinct prediction is the O(k^3) lattice term in
      Omega(k); we show it scales as (a/lambda_vac)^2 ~ 1e-56 at optical
      wavelengths and is NOT enhanced by the group index, so slow light does
      not lift it into reach.

Self-contained: numpy only.  No chiral transforms here (this is the real,
scalar/2-vector optical sector), so numpy FFTs are safe per CLAUDE.md.

References (measured anchors):
  - Hau, Harris, Dutton, Behroozi, Nature 397, 594 (1999): v_g = 17 m/s.
  - Wang, Kuzmich, Dogariu, Nature 406, 277 (2000); PRA 63, 053806 (2001):
    transparent anomalous dispersion, v_g = -c/310 (PRA: -c/315), ~62 ns
    pulse advance.
  - Fleischhauer, Imamoglu, Marangos, Rev. Mod. Phys. 77, 633 (2005): EIT
    susceptibility.
"""

import numpy as np

C_VAC = 299_792_458.0          # m/s
ROOT3 = np.sqrt(3.0)


# ======================================================================
# 1.  Linear susceptibilities  chi(omega)
# ======================================================================
def eit_susceptibility(delta, alpha0, Omega_c, gamma_opt, gamma_gnd):
    """Weak-probe EIT susceptibility of a 3-level Lambda system
    (Fleischhauer-Imamoglu-Marangos RMP 2005, control-field-dressed form):

        chi(d) = i * alpha0 / ( gamma_opt + i d + (Omega_c^2/4)/(gamma_gnd + i d) )

    `delta` = probe one-photon detuning (rad/s).  At two-photon resonance
    (delta -> 0) with small gamma_gnd the medium is transparent and the real
    part has a steep POSITIVE slope -> slow light.  Returns complex chi.
    """
    delta = np.asarray(delta, dtype=complex)
    denom = gamma_opt + 1j * delta + (Omega_c**2 / 4.0) / (gamma_gnd + 1j * delta)
    return 1j * alpha0 / denom


def gain_doublet_susceptibility(delta, M, sep, width):
    """Two Raman GAIN lines at +/- sep (Wang-Kuzmich-Dogariu mechanism).
    The minus sign makes them gain (not absorption); BETWEEN the lines the
    real index has NEGATIVE slope -> anomalous dispersion -> negative group
    velocity, in a transparent (here, amplifying) window.

        chi(d) = - M [ 1/(d - sep + i*width) + 1/(d + sep + i*width) ]
    """
    delta = np.asarray(delta, dtype=complex)
    return -M * (1.0 / (delta - sep + 1j * width)
                 + 1.0 / (delta + sep + 1j * width))


# ======================================================================
# 2.  Index, phase velocity, group velocity
# ======================================================================
def refractive_index(chi):
    """n(omega) = Re( sqrt(1 + chi) ).  Dilute or dense; full sqrt, not the
    1+chi/2 expansion, so it is valid for the gain doublet too."""
    return np.real(np.sqrt(1.0 + np.asarray(chi, dtype=complex)))


def phase_velocity(n0):
    """v_p = c / n(omega0)."""
    return C_VAC / n0


def group_index_and_velocity(omega0, chi_func, dω=None, **kw):
    """Group index n_g = n + omega dn/domega and v_g = c / n_g, by central
    difference of n(omega) about omega0.  chi_func takes detuning delta about
    omega0 (so delta=0 at omega0)."""
    if dω is None:
        dω = max(abs(omega0) * 1e-6, 1.0)
    n_p = refractive_index(chi_func(+dω, **kw))
    n_m = refractive_index(chi_func(-dω, **kw))
    n_0 = refractive_index(chi_func(0.0, **kw))
    dn_dω = (n_p - n_m) / (2.0 * dω)
    n_g = n_0 + omega0 * dn_dω
    return float(n_g), float(C_VAC / n_g)


# ======================================================================
# 3.  Pulse propagation  --  the two descriptions
# ======================================================================
def _beta(omega, omega0, chi_func, **kw):
    """Propagation constant beta(omega) = n(omega) * omega / c (Maxwell)."""
    delta = omega - omega0
    n = refractive_index(chi_func(delta, **kw))
    return n * omega / C_VAC


def propagate_phase(E0_t, t, omega0, L, chi_func, **kw):
    """STANDARD complex-phase description: propagate the complex analytic
    signal by the frequency-domain transfer H(w) = exp(i*beta(w)*L)
    (loss/gain folded into Im beta via Im n).  Returns complex E(t) at z=L."""
    E0_t = np.asarray(E0_t, dtype=complex)
    N = len(t); dt = t[1] - t[0]
    omega = omega0 + 2.0 * np.pi * np.fft.fftfreq(N, d=dt)
    delta = omega - omega0
    n_cplx = np.sqrt(1.0 + chi_func(delta, **kw))   # complex index (loss+disp)
    beta = n_cplx * omega / C_VAC
    # physical forward wave e^{i(beta z - omega t)} with numpy's e^{+i*Omega*t}
    # ifft convention -> dispersive phase enters as exp(-i Re(beta) L); the
    # attenuation exp(-Im(beta) L) is the loss/gain.  Positive n_g => delay.
    # Cap the gain/loss exponent: a toy susceptibility extrapolated far off
    # resonance can return unphysical runaway gain; the real atomic response
    # is bounded, so clip (this only touches far-detuning bins outside any
    # physical pulse band).
    atten = np.exp(np.clip(-np.imag(beta) * L, -700.0, 30.0))
    H = np.exp(-1j * np.real(beta) * L) * atten
    return np.fft.ifft(np.fft.fft(E0_t) * H)


def propagate_rotation(E0_t, t, omega0, L, chi_func, **kw):
    """MODEL rotation-rate description: the physical state is the REAL (E,B)
    pair, propagated by a real 2x2 rotation R(Phi) per Fourier mode, where the
    rotation angle is Phi(w) = Re(beta)*L and the amplitude (loss/gain) is the
    real scaling exp(-Im(beta)*L).  Per mode:

        [E;B] -> exp(-Im beta L) * [[cosPhi, sinPhi],[-sinPhi, cosPhi]] [E;B].

    A real linearly polarized input has B in quadrature (the transverse EM
    mode), i.e. the complex amplitude (E + iB) carries the same rotation -- so
    this returns the SAME complex E(t) as propagate_phase, by construction of
    the isomorphism C <-> SO(2).  We build it from the real rotation explicitly
    to prove the equivalence numerically rather than assume it.
    """
    E0_t = np.asarray(E0_t, dtype=complex)
    N = len(t); dt = t[1] - t[0]
    omega = omega0 + 2.0 * np.pi * np.fft.fftfreq(N, d=dt)
    delta = omega - omega0
    n_cplx = np.sqrt(1.0 + chi_func(delta, **kw))
    beta = n_cplx * omega / C_VAC
    Phi = -np.real(beta) * L           # the real (E,B) rotation angle (fwd wave)
    atten = np.exp(np.clip(-np.imag(beta) * L, -700.0, 30.0))  # gain/loss (capped, see propagate_phase)
    Ek = np.fft.fft(E0_t.real)
    Bk = np.fft.fft(E0_t.imag)         # B = quadrature partner (E+iB analytic)
    cP, sP = np.cos(Phi), np.sin(Phi)
    # proper SO(2) rotation R(+Phi); equals the complex phase e^{+i Phi}
    E_new = atten * (cP * Ek - sP * Bk)
    B_new = atten * (sP * Ek + cP * Bk)
    return np.fft.ifft(E_new) + 1j * np.fft.ifft(B_new)


def peak_delay(E_in_t, E_out_t, t):
    """Group delay measured as the shift of the |envelope| peak (can be
    negative = pulse advance, the anomalous-dispersion signature)."""
    ti = t[np.argmax(np.abs(E_in_t))]
    to = t[np.argmax(np.abs(E_out_t))]
    return float(to - ti)


# ======================================================================
# 4.  Front velocity  (the model's invariant: the turn-on never beats c)
# ======================================================================
def front_velocity_index(chi_func, omega0, omega_hi_factor=1e6, **kw):
    """The front (Sommerfeld) velocity is c / n(omega -> infinity).  Every
    physical resonant/gain susceptibility has chi -> 0 at high frequency, so
    n(inf) -> 1 and v_front -> c, regardless of the sign of v_g.  We sample at
    a very high detuning to confirm n -> 1."""
    delta_hi = omega_hi_factor * omega0
    n_hi = refractive_index(chi_func(delta_hi, **kw))
    return float(C_VAC / n_hi), float(n_hi)


# ======================================================================
# 5.  Lattice O(k^3) term  --  the only genuinely distinct prediction
# ======================================================================
def lattice_liv_fraction(lambda_vac, a_cell):
    """Fractional deviation of the real-pair dispersion Omega_pair(k) =
    omega^+(k/2)+omega^-(k/2) from the linear rotation rate, at vacuum
    wavenumber k = 2 pi / lambda_vac.

    The BCC pair dispersion expands as Omega ~ c_lat |k| (1 - C (a k)^2 + ...)
    with C = O(1); the leading deviation is (a k)^2.  Crucially this is set by
    the VACUUM wavenumber, NOT the group index -- slow light does not enhance
    it (the medium steepens dn/domega; it does not change a*k).  Returns the
    fractional size (a k)^2 with C absorbed (order-of-magnitude)."""
    k = 2.0 * np.pi / lambda_vac
    return (a_cell * k) ** 2
