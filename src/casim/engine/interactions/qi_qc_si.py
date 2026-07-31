#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_qc_si.py  —  SI-anchoring of the quantum-computing / super-exchange sector (F224)
====================================================================================

The QC thread (F212→F222) is dimensionless — every rate is in lattice units.
This module attaches the SI bridge so the DERIVED super-exchange coupling J, the
entangling (Bell-pair) time, and the super-exchange oscillation period come out
in Hz and seconds, and can be laid next to real measurements.

The honest scale story
----------------------
The FUNDAMENTAL lattice is Planckian: canonical cell (F107/F123)
    a = 6.598 ℓ_P = 1.06638e-34 m,   τ = a/(c√3) = 2.05366e-43 s,
so the fundamental per-tick energy ħ/τ ≈ 3.2e18 GeV.  A super-exchange run on the
fundamental lattice would therefore oscillate at ~10^27 Hz — nothing like a real
device.  What is physical and scale-free is the DIMENSIONLESS relation

    J(t,U) = ½(√(U² + 16 t²) − U)            (exact two-site Hubbard gap, F214)
           → 4 t²/U            (t ≪ U, the textbook leading order)

which is RG-invariant under block-spin coarse-graining (F130): it holds at ANY
emergent lattice scale.  Real quantum-simulation platforms realise it on a coarse
EMERGENT lattice (an optical lattice, a double quantum dot) with their own (t,U);
the model's content is the functional form + the exact-gap refinement, tested by
whether it reproduces the measured coupling and dynamics.

Empirical anchor (cold atoms) — Trotzky et al., Science 319, 295 (2008),
"Time-resolved observation and control of superexchange interactions with
ultracold atoms in optical lattices": coherent super-exchange measured with
couplings J/h ≈ 5 Hz … 1 kHz; the t²/U (i.e. 4t²/U) scaling law confirmed by
varying lattice depth; symmetric double well operated at J/U ≈ 0.08.
"""
from __future__ import annotations

import numpy as np
from casim.constants import (
    a_over_ellP as _a_over_ellP,
    c_SI as _c_SI,
    ell_P_m as _ell_P_m,
    hbar_SI as _hbar_SI,
)

# ── physical constants / canonical cell (F107/F123) ────────────────────────
HBAR_J = _hbar_SI        # J·s
H_J = 2.0 * np.pi * HBAR_J      # J·s (Planck)
C_SI = _c_SI             # m/s
ELL_P = _ell_P_m            # m
A_CELL = _a_over_ellP * ELL_P     # F79 cell edge, m
TAU_CELL = A_CELL / (C_SI * np.sqrt(3.0))               # cell tick, s
EV_PER_J = 1.0 / 1.602176634e-19

# ── empirical reference (Trotzky 2008) ─────────────────────────────────────
TROTZKY_J_MIN_HZ = 5.0
TROTZKY_J_MAX_HZ = 1.0e3
TROTZKY_SYMMETRIC_J_OVER_U = 0.08

# ── empirical reference (semiconductor quantum-dot exchange qubit) ──────────
# Cerfontaine et al., Nature Communications 11, 4144 (2020): closed-loop GaAs
# singlet–triplet exchange qubit — (99.50 ± 0.04)% single-qubit gate fidelity
# and a measured LEAKAGE of 0.13% out of the computational subspace (the S(0,2)
# doubly-occupied singlet admixture — physically the model's virtual doublon).
GAAS_ST_LEAKAGE = 0.0013
GAAS_ST_FIDELITY = 0.9950


# ── the dimensionless model relation ───────────────────────────────────────
def J_exact(t, U):
    """Exact two-site half-filling Hubbard singlet–triplet gap (any units for
    t,U; result in the same units).  J = ½(√(U²+16t²) − U)."""
    return 0.5 * (np.sqrt(U ** 2 + 16.0 * t ** 2) - U)


def J_leading(t, U):
    """Leading-order super-exchange 4t²/U (t ≪ U) — the textbook expression the
    cold-atom scaling law is usually quoted against."""
    return 4.0 * t ** 2 / U


def exact_vs_leading_fraction(t, U):
    """Fractional difference (J_exact − J_leading)/J_leading — the model's
    predicted refinement beyond the textbook leading order."""
    return (J_exact(t, U) - J_leading(t, U)) / J_leading(t, U)


# ── dimensionful (SI) quantities ───────────────────────────────────────────
def entangling_time_s(J_hz):
    """Time to form a maximally-entangled (Bell) pair under the super-exchange
    entangler, in seconds.  H_eff=(hJ/4)σ·σ ⇒ U_exch(θ)=e^{−iθσ·σ} with
    θ=(2π J/4)·t; the perfect-entangler point θ=π/8 is reached at t=1/(4J)."""
    return 1.0 / (4.0 * np.asarray(J_hz, float))


def superexchange_period_s(J_hz):
    """Full super-exchange (spin-swap) oscillation period 1/J in seconds — the
    observable Trotzky et al. time-resolved."""
    return 1.0 / np.asarray(J_hz, float)


def fundamental_cell_energy_ev():
    """The fundamental per-tick energy ħ/τ of the Planckian cell, in eV."""
    return (HBAR_J / TAU_CELL) * EV_PER_J


# ── doublon leakage (F220 native decoherence) vs quantum-dot data ──────────
def double_occupancy_gs(t, U):
    """Total ground-state double occupancy ⟨n↑n↓⟩ of the two-site half-filling
    Hubbard singlet — the virtual-doublon weight that leaks out of the one-
    fermion-per-site (computational) subspace.  Exact closed form
        d = ½(1 − 1/√(1+(4t/U)²)),
    which the second-quantized diagonalisation (F217) reproduces to machine
    precision, and which → (2t/U)² as t≪U (the standard virtual-tunnelling
    admixture, physically = the S(0,2) leakage of an exchange spin qubit)."""
    x = 4.0 * t / U
    return 0.5 * (1.0 - 1.0 / np.sqrt(1.0 + x ** 2))


def leakage_leading(t, U):
    """Leading-order doublon leakage (2t/U)² (t ≪ U)."""
    return (2.0 * t / U) ** 2


def tU_from_leakage(d):
    """Invert `double_occupancy_gs` for t/U given a measured leakage d
    (analytic; no scipy):  x=4t/U with x² = 1/(1−2d)² − 1, so t/U = x/4."""
    x2 = 1.0 / (1.0 - 2.0 * d) ** 2 - 1.0
    return np.sqrt(x2) / 4.0


def dimensionless_to_hz(J_dimensionless, tau_eff_s):
    """Map a dimensionless per-tick J (energy in units of ħ/τ_eff) to Hz for an
    emergent lattice of tick time τ_eff:  J_Hz = J_dimensionless/(2π τ_eff)."""
    return J_dimensionless / (2.0 * np.pi * tau_eff_s)


def tau_eff_for_target_J(J_dimensionless, J_target_hz):
    """The emergent tick time τ_eff that reproduces a target J in Hz from the
    model's dimensionless J — i.e. what coarse lattice a device corresponds to."""
    return J_dimensionless / (2.0 * np.pi * J_target_hz)
