"""photon_packet.py — real-space propagation of the PAIRED-SPINOR photon (F314).

Why this module exists
----------------------
F20 item (3) claimed "the photon exists and moves end-to-end". It made that claim
with the **σ-bilinear composite photon** (`casim.engine.gauge.bilinear`), which
`S1-F69-sigma-bilinear-photon` retired on 2026-06-01 — helicity↔branch, linearly
birefringent, excluded by GRB/AGN polarimetry (F65/F66/F67). The F20 remediation
of 2026-08-03 withdrew that leg and left a **DEFERRED** item: the model had no
real-space demonstration that *its own* photon propagates.

The photon of the model is the paired-spinor photon (F67/F68/F69, CLAUDE.md Core
Design Decision 5): a bound (+,−) pair sharing the total momentum, rotating the
real (E, B) doublet at

    Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2)          (`gauge.photon.pair_dispersion`)

per tick. This module supplies what F20's Weyl and Dirac legs got in remediation
and its photon leg never did: a **closed-form** group velocity, a **wrap-free**
measured run, and a pre-registered tolerance derived from the estimator rather
than read off the residual.

It is the photon analogue of `casim.engine.lattice.wavepacket` (F20, Weyl and
Dirac). That module is imported read-only, for its float64 `arccos` conditioning
bound, so the two legs are guarded to the same standard.

The three closed forms
----------------------
**1. The pair group velocity, all three axes.** With
``u^s = c_x c_y c_z + s·s_x s_y s_z`` (`lattice.bcc._bcc_uvec`) and
``ω^s = arccos(u^s)``,

    ∂ω^s/∂k_i = −(∂u^s/∂k_i)/√(1−(u^s)²) = c_lat · g^s_i / √(1−(u^s)²)

    g^s_x = s_x c_y c_z − s·c_x s_y s_z
    g^s_y = c_x s_y c_z − s·s_x c_y s_z
    g^s_z = c_x c_y s_z − s·s_x s_y c_z

and therefore, because the constituents each carry k/2,

    ∂Ω_pair/∂k_i (k) = (c_lat/2)·[ ĝ⁺_i(k/2) + ĝ⁻_i(k/2) ],   ĝ ≡ g/√(1−u²).

**A note on ``lattice.wavepacket.weyl_group_velocity``, which is NOT this.** That
function returns ``c_lat·n̂_i``. The identity ``∂ω/∂k_i = c_lat·n̂_i`` holds for
``i = x`` **only**: measured against a central difference of the analytic
dispersion at 200 random k, ``g_x ≡ n_x`` (residual 1.2e-10, the h² floor) but
``g_y = −s·n_y`` (a *sign flip*) and ``g_z`` is not ±``n_z`` at all — the second
term of ``n_z`` carries the opposite sign to the one differentiation produces
(residual 0.41 and 0.70 respectively). F20 is unaffected because every call site
there passes ``axis=0``; the general statement in its docstring is wrong and is
flagged in F314 §"Defect found in a neighbouring module" rather than patched
here, since `lattice/` belongs to another sector's claim.

**2. On a coordinate axis the pair velocity is exactly c_lat.** On-axis
``c_y = c_z = 1`` and ``s_y = s_z = 0`` exactly, so ``u^± = cos(k·c_lat/2)`` at
the half-momentum bit-for-bit on both branches (this is F20's identity and F105's
corollary), hence ``Ω_pair(k x̂) = k·c_lat`` and ``∂Ω_pair/∂k_x = c_lat`` with
**zero curvature**: no lattice dispersion on-axis at any k in the zone.

**3. The finite-width packet.** A beam of finite transverse width has an angular
spectrum, so its centroid moves at the *packet-weighted* velocity

    ⟨dx̄/dt⟩ = Σ_k w(k) · ∂Ω_pair/∂k_x,      w(k) = |F̃(k)|² / Σ|F̃|².

F105 quotes the small-angle approximation ``Δv/v ≈ 1/(2(k₀σ⊥)²)`` for this and
measured it at the percent level on a *periodic* box (2.5% observed vs 2.3%
predicted). The approximation is good to about 6% **of the deficit**; the sum
above is the exact statement, and against it the same physics closes at 1e-11.

Why "one-sided" is the photon's branch-pure seed
------------------------------------------------
`gauge.photon.photon_step_spectral` sends the real doublet to
``E → cosΩ·E + sinΩ·B``, ``B → −sinΩ·E + cosΩ·B``, i.e.

    F̃(k) → e^{−iΩ(k)} F̃(k),    F ≡ E + iB.

``Ω_pair`` is **even** in k (``u^±(−k) = u^∓(k)``, which is the same algebra that
makes the pair non-birefringent), so a seed with spectral support at both ±k₀
carries two groups with opposite ∇_k Ω and splits into counter-propagating halves.
A seed whose analytic field F̃ is supported on **one side only** has no such
partner, no beat, and its centroid velocity is an exact Ehrenfest statement — the
photon's counterpart of the branch-pure spinor seed F20 needed for its 1e-15 rows.
This is the codebase's own beam convention (`gauge.photon.build_beam_packet`,
F105): B is the *quadrature* of E within one Cartesian component.

Findings: F314 (this module), F20 (the deferred item it closes), F69, F105, F26.
"""
from __future__ import annotations

from casim.numerics import xp as np
from casim.numerics import fft as _fft
from casim.constants import c_lat
from casim.engine.gauge import photon as _photon
from casim.engine.lattice.geometry import make_kgrid_3d as _kgrid3d
from casim.engine.lattice.wavepacket import arccos_amplification_bound

__all__ = [
    "pair_group_velocity",
    "onaxis_pair_u_residual",
    "offaxis_pair_u_residual",
    "onaxis_pair_dispersion_residual",
    "onaxis_pair_velocity_residual",
    "onaxis_pair_curvature",
    "packet_spectrum",
    "predicted_packet_velocity",
    "diffraction_deficit_approx",
    "run_photon_packet",
    "run_inphase_transverse_packet",
    "check_pair_group_velocity_closed_form",
    "check_photon_packet_propagation",
]


# ══════════════════════════════════════════════════════════════════
#  1. Closed-form pair group velocity
# ══════════════════════════════════════════════════════════════════

def _u_and_grad(kx, ky, kz, sign: str, axis: int):
    """Return ``(u^s, g^s_axis)`` — the Bloch scalar and the component of
    ``−∂u^s/∂k`` divided by ``c_lat``, both in closed form.

    Written out rather than routed through ``bcc.bcc_spin_axis`` on purpose: the
    n-vector is *not* ∇u except on the x-axis (see the module docstring), so the
    only safe general form is the derivative itself.
    """
    s = 1.0 if sign == "+" else -1.0 if sign == "-" else None
    if s is None:
        raise ValueError(f"sign must be '+' or '-', got {sign!r}")
    cx, cy, cz = np.cos(kx * c_lat), np.cos(ky * c_lat), np.cos(kz * c_lat)
    sx, sy, sz = np.sin(kx * c_lat), np.sin(ky * c_lat), np.sin(kz * c_lat)
    u = cx * cy * cz + s * sx * sy * sz
    g = (sx * cy * cz - s * cx * sy * sz,
         cx * sy * cz - s * sx * cy * sz,
         cx * cy * sz - s * sx * sy * cz)[int(axis)]
    return u, g


def pair_group_velocity(kx, ky, kz, axis: int = 0):
    """``∂Ω_pair/∂k_axis`` in closed form. Scalars or arrays.

    The two constituents each carry ``k/2``, so the chain rule contributes the
    factor ``1/2``:

        ∂Ω_pair/∂k_i = (c_lat/2)·[ g⁺_i(k/2)/sin ω⁺ + g⁻_i(k/2)/sin ω⁻ ].

    Matches a central difference of :func:`gauge.photon.pair_dispersion` at the
    ``h²`` floor (≈7e-11 at h=1e-5) on **all three** axes — that three-axis check
    is the one that fails for the ``c_lat·n̂_i`` form.
    """
    total = 0.0
    for sign in ("+", "-"):
        u, g = _u_and_grad(kx / 2.0, ky / 2.0, kz / 2.0, sign, axis)
        total = total + g / np.sqrt(np.clip(1.0 - u * u, 1e-300, None))
    return 0.5 * c_lat * total


# ══════════════════════════════════════════════════════════════════
#  2. The exact on-axis statements
# ══════════════════════════════════════════════════════════════════

def _onaxis_k(n_k: int, axis: int):
    k = np.linspace(0.0, np.pi / c_lat, int(n_k))
    comp = [np.zeros_like(k), np.zeros_like(k), np.zeros_like(k)]
    comp[int(axis)] = k
    return k, comp


def onaxis_pair_u_residual(n_k: int = 500, sign: str = "+", axis: int = 0) -> float:
    """``max |u^±(k/2 · ê) − cos(k·c_lat/2)|`` — **exactly zero**, both branches.

    The pair evaluates its constituents at half the total momentum, so this is
    F20's on-axis identity read at ``k/2``. The transverse factors are
    ``cos 0 = 1`` and ``sin 0 = 0``, both exactly representable, so the ± term
    vanishes identically and the equality holds bit-for-bit in float64.
    Expected 0.0 at tolerance 0; :func:`offaxis_pair_u_residual` is the control
    that stops this being a tautology.
    """
    k, comp = _onaxis_k(n_k, axis)
    u, _ = _u_and_grad(comp[0] / 2.0, comp[1] / 2.0, comp[2] / 2.0, sign, 0)
    return float(np.max(np.abs(u - np.cos(k * c_lat / 2.0))))


def offaxis_pair_u_residual(n_k: int = 500, sign: str = "+") -> float:
    """The control: the same residual along the body diagonal, where it is O(1).

    Along ``k(1,1,1)/√3`` the transverse factors are neither 1 nor 0, the ± term
    survives, and the identity fails. A test that asserts the on-axis residual is
    zero must also assert this one is not.
    """
    k = np.linspace(0.0, np.pi / c_lat, int(n_k))
    d = k / np.sqrt(3.0) / 2.0
    u, _ = _u_and_grad(d, d, d, sign, 0)
    return float(np.max(np.abs(u - np.cos(k * c_lat / 2.0))))


def onaxis_pair_dispersion_residual(n_k: int = 500, axis: int = 0) -> float:
    """``max |Ω_pair(k·ê) − k·c_lat|`` over the full on-axis zone range.

    The identity above carried through ``arccos`` twice and summed. Exact in
    exact arithmetic; in float64 bounded by
    :func:`lattice.wavepacket.arccos_amplification_bound` — a MACHINE-class
    statement, where :func:`onaxis_pair_u_residual` is the EXACT one. (F105 states
    the same identity; this is its guarded form.)
    """
    k, comp = _onaxis_k(n_k, axis)
    om = _photon.pair_dispersion(comp[0], comp[1], comp[2])
    return float(np.max(np.abs(om - k * c_lat)))


def onaxis_pair_velocity_residual(n_k: int = 500, axis: int = 0) -> float:
    """``max |∂Ω_pair/∂k_axis − c_lat|`` on a coordinate axis.

    The physical content of the identity: an axis-aligned photon has group
    velocity exactly ``c_lat`` at **every** k in the zone, not merely as k → 0.
    The endpoints are skipped — ``sin ω`` vanishes there and the closed form is
    0/0, which is a property of the coordinate, not of the physics.
    """
    k, comp = _onaxis_k(n_k, axis)
    sl = slice(1, -1)
    v = pair_group_velocity(comp[0][sl], comp[1][sl], comp[2][sl], axis=axis)
    return float(np.max(np.abs(v - c_lat)))


def onaxis_pair_curvature(k0: float = 0.8, h: float = 1e-3, axis: int = 0) -> float:
    """``∂²Ω_pair/∂k_axis²`` by central difference — zero to the ``h²`` floor.

    Zero curvature is the strong form of "no on-axis lattice dispersion": there
    is no ``k²`` Lorentz-violating term for axis-aligned propagation at any
    energy, which is the algebraic root of F28's on-axis null result.
    """
    ks = np.array([k0 - h, k0, k0 + h])
    z = np.zeros_like(ks)
    comp = [z, z, z]
    comp[int(axis)] = ks
    w = _photon.pair_dispersion(comp[0], comp[1], comp[2])
    return float((w[0] - 2.0 * w[1] + w[2]) / h ** 2)


# ══════════════════════════════════════════════════════════════════
#  3. The finite-width packet prediction
# ══════════════════════════════════════════════════════════════════

def _beam_analytic_field(shape, sigma, m_index, axis, center):
    """The one-sided analytic field ``F(x) = env(x)·e^{i k₀·(x−x₀)}``.

    ``k₀ = 2π·m_index/L_axis`` sits exactly on the k-grid, so the carrier is
    representable and the backward content is only the Gaussian tail
    ``~exp(−(2k₀σ_axis)²)`` — 1e-19 at the defaults, far below the estimator floor.
    Same construction as :func:`gauge.photon.build_beam_packet`, generalised off
    the cubic box because a wrap-free run needs a long axis.
    """
    shape = tuple(int(s) for s in shape)
    sig = np.atleast_1d(np.asarray(sigma, float)) * np.ones(3)
    k0 = 2.0 * np.pi * float(m_index) / float(shape[int(axis)])
    X = np.meshgrid(*[np.arange(n, dtype=float) for n in shape], indexing="ij")
    d = [np.remainder(X[a] - center[a] + shape[a] / 2.0, shape[a]) - shape[a] / 2.0
         for a in range(3)]
    env = np.exp(-0.5 * sum((d[a] / sig[a]) ** 2 for a in range(3)))
    return env * np.exp(1j * k0 * d[int(axis)]), k0


def packet_spectrum(shape, sigma=(4.0, 6.0, 6.0), m_index: int = 16,
                    axis: int = 0, center=None):
    """Normalised momentum weights ``w(k) = |F̃(k)|²/Σ|F̃|²`` of the beam.

    The **actual discrete** analytic field is transformed, not a continuum
    Gaussian, so the weights carry the lattice's periodic image sum and its
    finite k-grid exactly. ``σ`` is the **amplitude** width (envelope
    ``exp(−Σ(xᵢ−cᵢ)²/2σᵢ²)``); reading it as a density width moves the deficit by
    a factor of two, which is larger than everything measured here.
    """
    shape = tuple(int(s) for s in shape)
    if center is None:
        center = [shape[a] / 4.0 if a == int(axis) else shape[a] / 2.0
                  for a in range(3)]
    F, k0 = _beam_analytic_field(shape, sigma, m_index, axis, center)
    w = np.abs(_fft.fftn(F)) ** 2
    return w / w.sum(), k0


def predicted_packet_velocity(shape, sigma=(4.0, 6.0, 6.0), m_index: int = 16,
                              axis: int = 0, center=None) -> float:
    """``Σ_k w(k)·∂Ω_pair/∂k_axis`` — the exact finite-width centroid velocity.

    This is the target the measured drift is compared against. It is not a fitted
    quantity and not a frozen script output: it is a closed-form derivative
    averaged over a spectrum computed from the seed.
    """
    w, _ = packet_spectrum(shape, sigma, m_index, axis, center)
    KX, KY, KZ = _kgrid3d(*(int(s) for s in shape))
    return float(np.sum(w * pair_group_velocity(KX, KY, KZ, axis=axis)))


def diffraction_deficit_approx(k0: float, sigma_perp: float) -> float:
    """F105's small-angle approximation to the fractional deficit,
    ``1/(2(k₀σ⊥)²)``.

    Kept so the exact prediction can be scored against it. It is the right order
    and the right scaling; it is not the right number, and F105's percent-level
    beam demonstration is where the difference showed up as "2.5% measured vs
    2.3% predicted".
    """
    return 1.0 / (2.0 * (float(k0) * float(sigma_perp)) ** 2)


# ══════════════════════════════════════════════════════════════════
#  4. The measured run — wrap-free by construction
# ══════════════════════════════════════════════════════════════════

def _centroid_track(E, B, axis, n_steps, step):
    shape = E.shape[1:]
    ax = np.arange(shape[int(axis)], dtype=float)
    other = tuple(a for a in range(3) if a != int(axis))
    track, energy = [], []
    for n in range(int(n_steps) + 1):
        rho = (E ** 2).sum(axis=0) + (B ** 2).sum(axis=0)
        col = rho.sum(axis=other)
        track.append(float((ax * col).sum() / col.sum()))
        energy.append(float(rho.sum()))
        if n < int(n_steps):
            E, B = step(E, B)
    rho = (E ** 2).sum(axis=0) + (B ** 2).sum(axis=0)
    col = rho.sum(axis=other)
    edge = float((col[:4].sum() + col[-4:].sum()) / col.sum())
    return np.array(track), np.array(energy), edge, E, B


#: Pre-registered wrap-free ceiling. Asserted, and set by geometry alone: the
#: packet starts ``x₀/σₓ ≈ 6.4`` standard deviations from the near edge and the
#: carrier satisfies ``k₀σₓ ≈ 5.9``, so the backward-going spectral tail is
#: ``exp(−4k₀²σₓ²) ~ 1e-15``. Both are choices, not observations.
EDGE_WEIGHT_CEILING = 1e-15

#: Pre-registered tolerance for the drift-vs-closed-form comparison, `machine`
#: class. Derived, not read off the residual — see :func:`centroid_bias_bound`.
DRIFT_TOL = 1e-12


def centroid_bias_bound(shape, axis: int, edge_weight: float = EDGE_WEIGHT_CEILING) -> float:
    """Bound on the arithmetic-centroid estimator's bias, per tick.

    The estimator is ``Σ x ρ / Σ ρ`` on a **linear** x-array over a **periodic**
    box. Weight ``ε`` that has wrapped past the boundary is counted at the wrong
    end of the array, so each per-tick displacement can be biased by at most
    ``ε·L``. This is the failure that produced F20's original numbers: on its
    periodic 64³ box the packet wrapped within 44 ticks and the box scan reached
    ``1.024 c_lat`` — superluminal — at ``L_x = 192``.

    Evaluated at :data:`EDGE_WEIGHT_CEILING` and ``L = 128`` the bias is
    ``1.3e-13`` absolute, ``2.3e-13`` relative — under :data:`DRIFT_TOL`, which
    is therefore the binding pre-registration. The float64 FFT round-off floor
    over ``n_steps`` spectral rotations is the other contributor and is of the
    same order. Neither number comes from the residual; the residual comes in
    three decades below both.
    """
    return float(edge_weight) * float(shape[int(axis)])


def run_photon_packet(shape=(128, 48, 48), sigma=(5.0, 7.0, 7.0), m_index: int = 24,
                      axis: int = 0, pol_axis: int | None = None,
                      n_steps: int = 24, tail_ticks: int = 8, center=None):
    """Propagate a one-sided photon beam with the engine's own photon step.

    The box is long along ``axis`` and the packet starts a quarter of the way in,
    so the envelope never reaches a boundary within ``n_steps`` — the wrap bias
    that dominated F20's original periodic-box numbers is measured and reported
    (``edge_weight``), not assumed away.

    **Two geometric conditions, and both bind.** The start point is ``6.4σₓ`` from
    the near edge, which is the obvious one. The second is ``k₀σₓ ≈ 5.9``: the
    seed is only one-sided up to the Gaussian tail of its own carrier, and the
    backward weight ``exp(−4k₀²σₓ²)`` runs *backwards* at ``−c_lat`` and reaches
    the boundary first. At ``k₀σₓ = 3.14`` — the "``≳ 3``" that
    :func:`gauge.photon.build_beam_packet` suggests — that tail alone puts
    ``1.8e-8`` at the edge and the residual degrades from 8e-16 to **1.1e-6**,
    six decades, with nothing else changed. The carrier, not just the box, is
    part of being wrap-free.

    The *transverse* envelope does touch its boundary at the 1e-7 level; that is
    harmless because it enters the prediction too — :func:`packet_spectrum`
    transforms the same discrete envelope, so the periodic image sum is carried
    exactly on both sides of the comparison. Only the **axial** arithmetic
    centroid can be biased by wrap, and only that one is asserted.

    Propagator: :func:`gauge.photon.photon_step_spectral` — the even law
    ``R(Ω_pair)``, unmodified. Nothing about the photon is re-implemented here;
    only the seed, the estimator and the closed-form target belong to this module.

    Returns the fitted slope, the asymptotic drift, the closed-form prediction,
    the boundary leakage, and the fractional energy drift over the run.
    """
    shape = tuple(int(s) for s in shape)
    axis = int(axis)
    if pol_axis is None:
        pol_axis = (axis + 1) % 3
    pol_axis = int(pol_axis)
    if pol_axis == axis:
        raise ValueError("beam polarisation must be transverse (pol_axis != axis)")
    if center is None:
        center = [shape[a] / 4.0 if a == axis else shape[a] / 2.0 for a in range(3)]

    F, k0 = _beam_analytic_field(shape, sigma, m_index, axis, center)
    E = np.zeros((3,) + shape)
    B = np.zeros((3,) + shape)
    E[pol_axis] = F.real
    B[pol_axis] = F.imag

    track, energy, edge, E, B = _centroid_track(
        E, B, axis, n_steps, _photon.photon_step_spectral)

    per_tick = np.diff(track)
    tail = per_tick[-int(tail_ticks):] if tail_ticks else per_tick
    drift = float(tail.mean())
    t = np.arange(len(track), dtype=float)
    A = np.vstack([t, np.ones_like(t)]).T
    slope = float(np.linalg.lstsq(A, track, rcond=None)[0][0])

    pred = predicted_packet_velocity(shape, sigma, m_index, axis, center)
    sig = np.atleast_1d(np.asarray(sigma, float)) * np.ones(3)
    perp = float(np.sqrt(sig[(axis + 1) % 3] * sig[(axis + 2) % 3]))
    return {
        "lstsq_slope": slope,
        "asymptotic_drift": drift,
        "predicted_vg": pred,
        "rel_err_drift": abs(drift - pred) / abs(pred),
        "rel_err_lstsq": abs(slope - pred) / abs(pred),
        "per_tick_std": float(per_tick.std()),
        "first_tick_displacement": float(per_tick[0]),
        "edge_weight": edge,
        "k0_sigma_axis": k0 * float(sig[axis]),
        "centroid_bias_bound": centroid_bias_bound(shape, axis),
        "energy_rel_drift": float((energy.max() - energy.min()) / energy[0]),
        "vs_c_lat": (drift - c_lat) / c_lat,
        "deficit_measured": 1.0 - drift / c_lat,
        "deficit_predicted": 1.0 - pred / c_lat,
        "deficit_f105_approx": diffraction_deficit_approx(k0, perp),
        "k0": k0,
        "shape": list(shape), "sigma": list(sig), "m_index": int(m_index),
        "axis": axis, "pol_axis": pol_axis,
        "n_steps": int(n_steps), "tail_ticks": int(tail_ticks),
        "centroid_start": float(track[0]), "centroid_end": float(track[-1]),
    }


def run_inphase_transverse_packet(shape=(128, 48, 48), sigma=(5.0, 8.0, 8.0),
                                  m_index: int = 16, axis: int = 0,
                                  n_steps: int = 20, center=None):
    """Diagnostic: the same beam seeded as a Maxwell-style **in-phase** mode.

    Here ``Ẽ(k) ∥ ê₁(k)`` and ``B̃(k) = k̂ × Ẽ(k)`` with Hermitian symmetry — a
    real, transverse, linearly polarised traveling wave in the textbook sense
    (``E`` and ``B`` perpendicular and in phase), rather than the codebase's
    quadrature convention (``B`` the same-component quadrature of ``E``).

    **This is a measurement, not a claim.** Under the even pair law such a seed
    has spectral support at both ``±k₀``; ``Ω_pair`` is even, so the two halves
    carry opposite ``∇_k Ω`` and the packet splits into counter-propagating
    halves with net drift ≈ 0 and a growing rms width. The number is reported so
    the two (E, B) identifications are visibly *different objects* under this law.
    Which of them is the physical electromagnetic field is exactly the question
    the curl family F21/F23/F25/F306 is open on; nothing is concluded here.

    Returns the net drift and the rms spread ratio (end/start).
    """
    shape = tuple(int(s) for s in shape)
    axis = int(axis)
    if center is None:
        center = [shape[a] / 4.0 if a == axis else shape[a] / 2.0 for a in range(3)]
    F, _ = _beam_analytic_field(shape, sigma, m_index, axis, center)
    et = _fft.fftn(F)

    KX, KY, KZ = _kgrid3d(*shape)
    kn = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2)
    kn = np.where(kn < 1e-14, 1.0, kn)
    kh = [KX / kn, KY / kn, KZ / kn]
    ref = np.zeros(3)
    ref[(axis + 2) % 3] = 1.0
    dot = sum(kh[i] * ref[i] for i in range(3))
    e1 = [ref[i] - dot * kh[i] for i in range(3)]
    nrm = np.sqrt(sum(c ** 2 for c in e1))
    nrm = np.where(nrm < 1e-12, 1.0, nrm)
    e1 = [c / nrm for c in e1]
    e2 = [kh[1] * e1[2] - kh[2] * e1[1],
          kh[2] * e1[0] - kh[0] * e1[2],
          kh[0] * e1[1] - kh[1] * e1[0]]

    # .real performs the Hermitian symmetrisation, which is what makes the field
    # real AND populates -k0 with the correct transverse partner (B = k_hat x E
    # holds at both +k0 and -k0 because e1 is even in k and e2 is odd).
    E = 2.0 * np.array([_fft.ifftn(et * e1[i]).real for i in range(3)])
    B = 2.0 * np.array([_fft.ifftn(et * e2[i]).real for i in range(3)])

    ax = np.arange(shape[axis], dtype=float)
    other = tuple(a for a in range(3) if a != axis)

    def _rms(Ea, Ba):
        rho = (Ea ** 2).sum(axis=0) + (Ba ** 2).sum(axis=0)
        col = rho.sum(axis=other)
        xb = (ax * col).sum() / col.sum()
        return float(xb), float(np.sqrt((col * (ax - xb) ** 2).sum() / col.sum()))

    x0, rms0 = _rms(E, B)
    track, _energy, _edge, E, B = _centroid_track(
        E, B, axis, n_steps, _photon.photon_step_spectral)
    x1, rms1 = _rms(E, B)
    per = np.diff(track)
    return {
        "net_drift": float(per[-8:].mean()),
        "rms_start": rms0, "rms_end": rms1,
        "rms_ratio": rms1 / rms0,
        "centroid_shift": x1 - x0,
        "shape": list(shape), "m_index": int(m_index), "n_steps": int(n_steps),
    }


# ══════════════════════════════════════════════════════════════════
#  5. Registry entries
# ══════════════════════════════════════════════════════════════════

def check_pair_group_velocity_closed_form(n_k: int = 500, k0: float = 0.8,
                                          h: float = 1e-5, seed: int = 314):
    """Entry point for the ``F314-pair-group-velocity-closed-form`` record.

    All analytic, sub-second. Seven checks, each with a real failure mode:

    1-2. the on-axis pair identity ``u^± = cos(k·c_lat/2)`` is EXACT (tol 0), on
         both branches;
    3.   the same residual off-axis is O(1) — the control;
    4.   ``Ω_pair(k x̂) = k·c_lat`` within the float64 ``arccos`` bound;
    5.   ``∂Ω_pair/∂k_x = c_lat`` on-axis at every k;
    6.   the on-axis cone has zero curvature;
    7.   the closed form matches a central difference of ``pair_dispersion`` at 30
         random off-axis k, on **all three** axes.
    """
    res = {
        "onaxis_u_residual_plus": onaxis_pair_u_residual(n_k=n_k, sign="+"),
        "onaxis_u_residual_minus": onaxis_pair_u_residual(n_k=n_k, sign="-"),
        "offaxis_u_residual": offaxis_pair_u_residual(n_k=n_k),
        "onaxis_dispersion_residual": onaxis_pair_dispersion_residual(n_k=n_k),
        "arccos_bound": arccos_amplification_bound(n_k=n_k),
        "onaxis_velocity_residual": onaxis_pair_velocity_residual(n_k=n_k),
        "onaxis_curvature": onaxis_pair_curvature(k0=k0),
    }

    gen = np.random.default_rng(int(seed))
    ks = gen.uniform(-1.2, 1.2, size=(30, 3))
    fd_resid = []
    for a in range(3):
        pp, pm = np.array(ks), np.array(ks)
        pp[:, a] += h
        pm[:, a] -= h
        fd = (_photon.pair_dispersion(*pp.T) - _photon.pair_dispersion(*pm.T)) / (2.0 * h)
        cf = pair_group_velocity(ks[:, 0], ks[:, 1], ks[:, 2], axis=a)
        fd_resid.append(float(np.max(np.abs(fd - cf))))
    res["closed_form_residual_per_axis"] = fd_resid
    res["closed_form_residual"] = float(max(fd_resid))

    res["checks"] = {
        "onaxis_u_exact_plus": res["onaxis_u_residual_plus"] == 0.0,
        "onaxis_u_exact_minus": res["onaxis_u_residual_minus"] == 0.0,
        "offaxis_control_nonzero": res["offaxis_u_residual"] > 1e-3,
        "onaxis_omega_linear": res["onaxis_dispersion_residual"] <= res["arccos_bound"],
        "onaxis_velocity_is_c_lat": res["onaxis_velocity_residual"] <= 1e-10,
        "onaxis_flat": abs(res["onaxis_curvature"]) <= 1e-6,
        "closed_form_all_axes": res["closed_form_residual"] <= 1e-8,
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


def check_photon_packet_propagation(shape=(128, 48, 48), m_index: int = 24,
                                    n_steps: int = 24):
    """Entry point for the ``F314-photon-packet-propagation`` record.

    Propagates the model's own photon across a wrap-free box with
    ``gauge.photon.photon_step_spectral`` and asserts:

    * the measured centroid drift equals the closed-form packet-weighted
      ``⟨∂Ω_pair/∂k_x⟩`` at :data:`DRIFT_TOL` = 1e-12, the repo's `machine` class.
      The tolerance is **derived from the estimator**, not read off the residual:
      the arithmetic centroid on a periodic box is biased by at most ``ε·L`` per
      tick, so at the asserted ``ε ≤ 1e-15`` and ``L = 128`` the bias is 2.3e-13
      relative, and the float64 FFT round-off floor over 24 spectral rotations is
      the same order. The residual lands three decades below both;
    * the run is wrap-free, ``ε ≤`` :data:`EDGE_WEIGHT_CEILING`;
    * total ``Σ(|E|²+|B|²)`` is conserved on the **moving** packet. This is the
      gate F20's item (3) could not pass: the σ-bilinear ``Σ|G^i|²`` fell
      1.000 → 0.628 over 44 ticks, and its quoted conservation figure came from a
      global scalar phase applied with no lattice step at all;
    * the drift is subluminal and does **not** equal ``c_lat`` — the finite
      transverse aperture is real physics, and a test that passed against
      ``c_lat`` would be measuring nothing;
    * the drift is independent of the polarisation axis (bit-level), which the
      even law makes a statement about ``Ω_pair`` being a scalar rather than a
      polarisation-dependent rate;
    * there is **no transient**: the very first tick already moves at the
      asymptotic speed. This is the one-sided seed doing its work. F20's
      fixed-spinor Weyl packet starts at exactly ``c_lat`` and relaxes onto its
      closed form only asymptotically, leaving 2e-4 in a whole-window fit; here
      first tick and tail agree to 1e-8, so the estimator carries no fit-window
      freedom at all;
    * F105's small-angle approximation ``1/(2(k₀σ⊥)²)`` is *close but wrong* —
      the size of that gap is what separates a percent-level demonstration from
      this record.
    """
    r = run_photon_packet(shape=shape, m_index=m_index, n_steps=n_steps)
    alt = run_photon_packet(shape=shape, m_index=m_index, n_steps=n_steps,
                            pol_axis=2)
    r["pol_axis_2_drift"] = alt["asymptotic_drift"]
    r["pol_independence"] = abs(alt["asymptotic_drift"] - r["asymptotic_drift"])

    r["tol"] = DRIFT_TOL
    r["bias_bound_relative"] = r["centroid_bias_bound"] / abs(r["predicted_vg"])
    r["transient_frac"] = abs(
        r["first_tick_displacement"] - r["asymptotic_drift"]) / abs(r["asymptotic_drift"])
    r["approx_error_frac_of_deficit"] = abs(
        r["deficit_f105_approx"] - r["deficit_predicted"]) / r["deficit_predicted"]
    r["checks"] = {
        "drift_matches_closed_form": r["rel_err_drift"] <= DRIFT_TOL,
        "wrap_free": r["edge_weight"] <= EDGE_WEIGHT_CEILING,
        "one_sided_carrier": r["k0_sigma_axis"] >= 5.0,
        "energy_conserved": r["energy_rel_drift"] <= 1e-12,
        "subluminal": r["asymptotic_drift"] < c_lat,
        "aperture_deficit_is_real": r["deficit_measured"] > 1e-4,
        "polarisation_independent": r["pol_independence"] <= 1e-14,
        "no_transient": r["transient_frac"] <= 1e-8,
    }
    r["n_pass"] = int(sum(r["checks"].values()))
    r["n_checks"] = len(r["checks"])
    r["ok"] = r["n_pass"] == r["n_checks"]
    return r


if __name__ == "__main__":  # pragma: no cover - artifact write is guarded
    import json
    from casim.engine.particles._results_path import results_path

    out = {
        "closed_forms": check_pair_group_velocity_closed_form(),
        "propagation": check_photon_packet_propagation(),
        # The production-scale wrap-free run, on F20's own box and tick count.
        "propagation_L256": run_photon_packet(
            shape=(256, 64, 64), sigma=(6.0, 10.0, 10.0), m_index=48,
            n_steps=44, tail_ticks=14, center=(60.0, 32.0, 32.0)),
        # The negative control for `one_sided_carrier`: same physics, same box,
        # carrier at k0*sigma_x = 3.14, which is what build_beam_packet suggests.
        "propagation_undersampled_carrier": run_photon_packet(
            shape=(128, 48, 48), sigma=(4.0, 6.0, 6.0), m_index=16, n_steps=20),
        "inphase_transverse_diagnostic": run_inphase_transverse_packet(),
    }
    print(json.dumps(out, indent=2))
    with open(results_path("F314_photon_packet_propagation.json"), "w") as fh:
        json.dump(out, fh, indent=2)
