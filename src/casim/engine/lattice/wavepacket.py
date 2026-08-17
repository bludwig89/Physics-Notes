"""wavepacket.py — closed-form group velocity of a BCC wavepacket (F20 remediation).

Why this module exists
----------------------
F20 launched Gaussian wavepackets on a 64³ BCC lattice and compared the measured
centroid slope ``dx̄/dt`` to ``c_lat``. The independent review of 2026-08-03
(`docs/reviews/F20-review-2026-08-03.md`) found that comparison to be against the
wrong target and on the wrong box:

* the correct prediction for a packet of finite transverse width, seeded with a
  **fixed** spinor, is ``c_lat·⟨n̂ₓ²⟩`` — not ``c_lat``;
* on a periodic 64³ box the packet wraps within 44 ticks, and the resulting
  centroid bias partially cancels the real deficit. Wrap-free, the same physics
  agrees with ``c_lat·⟨n̂ₓ²⟩`` to ~1×10⁻⁶ rather than with ``c_lat`` to 0.4%.

So the demonstration-grade number was hiding a quantitative one. This module owns
the quantitative statements:

1. **Exact on-axis identity.** With ``k = (k,0,0)`` we have ``c_y = c_z = 1`` and
   ``s_y = s_z = 0``, so ``u^± = cos(k/√3)`` for *both* branches and

       ω(k x̂) = arccos(cos(k/√3)) = k/√3      exactly, for 0 ≤ k ≤ π√3.

   This is an algebraic identity, not a small-k limit: ``∂²ω/∂k_x² ≡ 0`` along a
   coordinate axis, so the on-axis lattice light cone has **no** curvature and no
   Lorentz-violating ``k²`` term at all.

2. **Closed-form group velocity.** Since ``∂u/∂k_x = −(1/√3)·n_x`` and
   ``√(1−u²) = |n|``,

       ∂ω/∂k_x = c_lat · n̂ₓ(k)                          (massless Weyl)
       ∂ω/∂k_x = c_lat · n_kin · n_x / √(1 − n_kin²u²)   (Dirac, n_kin = √(1−m²))

3. **Finite-width packet velocity.** Two corrections, both required:

   * *aperture / tilt* — the packet's off-axis modes have ``n̂ₓ < 1``;
   * *branch admixture* — a **fixed** seed spinor ``χ₊(k₀)`` is not an eigenspinor
     at ``k ≠ k₀``; weight ``(1−n̂ₓ)/2`` lands on the opposite branch, which moves
     at ``−v_x``. This **doubles** the tilt deficit.

   Together: ``⟨dx̄/dt⟩ = c_lat·⟨n̂ₓ²⟩`` for a fixed-spinor seed, and
   ``c_lat·⟨n̂ₓ⟩`` for a per-k helicity-pure seed. F20's own text carried only the
   first correction and was therefore wrong by a factor of two in the deficit.

Everything here is analytic except :func:`run_packet`, which propagates a real
packet with the engine's own step function so the closed forms can be checked
against the automaton rather than against themselves.

Findings: F20 (remediated 2026-08-03), F26 (c_lat as a rotation rate).
"""
from __future__ import annotations

from casim.numerics import xp as np
from casim.numerics import fft as _fft
from casim.constants import c_lat
from casim.engine.lattice import bcc as _bcc
from casim.engine.particles import dirac_bcc as _dbcc

__all__ = [
    "onaxis_dispersion_residual",
    "weyl_group_velocity",
    "dirac_group_velocity",
    "packet_momentum_weights",
    "predicted_packet_velocity",
    "run_packet",
    "check_group_velocity_closed_forms",
]


# ══════════════════════════════════════════════════════════════════
#  1. The exact on-axis identity
# ══════════════════════════════════════════════════════════════════

def _onaxis_k(n_k: int, axis: int):
    k = np.linspace(0.0, np.pi / c_lat, int(n_k))
    zeros = np.zeros_like(k)
    comp = [zeros, zeros, zeros]
    comp[int(axis)] = k
    return k, comp


def onaxis_u_residual(n_k: int = 500, sign: str = "+", axis: int = 0) -> float:
    """max |u^±(k·ê) − cos(k·c_lat)| along a coordinate axis. **Exactly zero.**

    This is the identity itself, stated at the level where it is exact. With
    ``k = (k,0,0)`` the transverse cosines are ``cos(0) = 1.0`` and the transverse
    sines are ``sin(0) = 0.0`` — both representable — so

        u^± = c_x·1·1 ± s_x·0·0 = cos(k·c_lat)

    holds *bit-for-bit* in floating point, for both branches, over the whole
    on-axis Brillouin range. Expected value 0.0 at tolerance 0.

    It is zero by algebra, not by a symmetry the code enforces: see
    :func:`offaxis_u_residual` for the same quantity along the body diagonal,
    where it is O(1) — that control is what gives this check a failure mode.
    """
    k, comp = _onaxis_k(n_k, axis)
    u, _, _, _ = _bcc._bcc_uvec(comp[0], comp[1], comp[2], sign=sign)
    return float(np.max(np.abs(u - np.cos(k * c_lat))))


def offaxis_u_residual(n_k: int = 500, sign: str = "+") -> float:
    """The control for :func:`onaxis_u_residual`: same quantity, body diagonal.

    Along ``k = (k,k,k)/√3`` the transverse factors are no longer 1 and 0, the
    identity fails, and this residual is O(1). A test that asserts the on-axis
    residual is 0 must also assert this one is not, or it is asserting a tautology.
    """
    k = np.linspace(0.0, np.pi / c_lat, int(n_k))
    d = k / np.sqrt(3.0)
    u, _, _, _ = _bcc._bcc_uvec(d, d, d, sign=sign)
    return float(np.max(np.abs(u - np.cos(k * c_lat))))


def arccos_amplification_bound(n_k: int = 500) -> float:
    """Pre-registered float64 bound on the ω-level residual of the same identity.

    ``ω = arccos(u)`` amplifies a round-off ``δu`` by ``1/√(1−u²) = 1/sin ω``, and
    the worst sampled point is the one nearest an endpoint, at
    ``ω = Δ ≡ π/(n_k−1)``. So the bound is ``2·eps/sin Δ``, derived from the
    conditioning of ``arccos`` and from ``n_k`` alone — it is not read off the
    residual.
    """
    delta = np.pi / (int(n_k) - 1)
    return float(2.0 * np.finfo(float).eps / np.sin(delta))


def onaxis_dispersion_residual(n_k: int = 500, sign: str = "+", axis: int = 0) -> float:
    """max |ω(k·ê) − k·c_lat| over the full on-axis Brillouin range.

    The same identity carried through ``arccos``: ``ω = arccos(cos(k·c_lat)) =
    k·c_lat`` for ``k·c_lat ∈ [0, π]``. Exact in exact arithmetic; in float64 it
    is bounded by :func:`arccos_amplification_bound`, which is a MACHINE-class
    statement rather than an EXACT one. The EXACT form is
    :func:`onaxis_u_residual`.
    """
    k, comp = _onaxis_k(n_k, axis)
    omega = _bcc.bcc_dispersion(comp[0], comp[1], comp[2], sign=sign)
    return float(np.max(np.abs(omega - k * c_lat)))


def onaxis_curvature(k0: float = 0.8, h: float = 1e-3, sign: str = "+") -> float:
    """Second derivative ∂²ω/∂k_x² on the x-axis by central difference.

    Zero to the ``h²`` floor — the on-axis cone is exactly straight, so there is
    no lattice ``k²`` dispersion for a packet travelling down a coordinate axis.
    """
    ks = np.array([k0 - h, k0, k0 + h])
    z = np.zeros_like(ks)
    w = _bcc.bcc_dispersion(ks, z, z, sign=sign)
    return float((w[0] - 2.0 * w[1] + w[2]) / h ** 2)


# ══════════════════════════════════════════════════════════════════
#  2. Closed-form group velocities
# ══════════════════════════════════════════════════════════════════

def weyl_group_velocity(kx, ky, kz, sign: str = "+", axis: int = 0):
    """∂ω/∂k_axis for the massless BCC Weyl walk, in closed form.

    ``∂ω/∂k_i = c_lat · n̂_i(k)`` — the group velocity is ``c_lat`` times the
    direction cosine of the Bloch spin axis, so it is bounded by ``c_lat`` and
    saturates it only where n̂ is aligned with the axis.
    """
    n_hat = _bcc.bcc_spin_axis(kx, ky, kz, sign=sign)
    return c_lat * n_hat[int(axis)]


def dirac_group_velocity(kx, ky, kz, m: float, sign: str = "+", axis: int = 0):
    """∂ω/∂k_axis for the massive BCC Dirac walk, in closed form.

    ``ω = arccos(n_kin·u)`` with ``n_kin = √(1−m²)``, so

        ∂ω/∂k_i = c_lat · n_kin · n_i / √(1 − n_kin² u²).
    """
    n_kin = float(np.sqrt(1.0 - float(m) ** 2))
    u, nx, ny, nz = _bcc._bcc_uvec(kx, ky, kz, sign=sign)
    n_i = (nx, ny, nz)[int(axis)]
    denom = np.sqrt(np.clip(1.0 - (n_kin * u) ** 2, 1e-300, None))
    return c_lat * n_kin * n_i / denom


# ══════════════════════════════════════════════════════════════════
#  3. Finite-width packet prediction
# ══════════════════════════════════════════════════════════════════

def packet_momentum_weights(shape, sigma, k0, exact: bool = True):
    """Normalised |ψ̃(k)|² of the packet envelope, on the lattice k-grid.

    ``sigma`` is the **amplitude** width: the real-space envelope is
    ``exp(−Σᵢ (xᵢ−cᵢ)²/2σᵢ²)``. Stating the convention matters — reading σ as the
    *density* width instead moves the answer by ~1%, which is larger than the
    agreement F20 originally quoted.

    ``exact=True`` (default) transforms the **actual discrete envelope**, so the
    weights carry the lattice's periodic image sum and its finite k-grid exactly.
    ``exact=False`` uses the continuum Gaussian ``exp(−(k−k₀)²σ²)``, which is the
    same to ~1×10⁻³ and is kept only to show that the difference is the
    discretisation, not the physics.

    Returns ``(w, KX, KY, KZ)`` with ``w.sum() == 1``.
    """
    Lx, Ly, Lz = (int(s) for s in shape)
    kx = 2.0 * np.pi * np.fft.fftfreq(Lx)
    ky = 2.0 * np.pi * np.fft.fftfreq(Ly)
    kz = 2.0 * np.pi * np.fft.fftfreq(Lz)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    if exact:
        env = _gaussian_envelope(shape, (Lx / 2.0, Ly / 2.0, Lz / 2.0), sigma, k0)
        w = np.abs(_fft.fftn(env)) ** 2
    else:
        sx, sy, sz = (float(s) for s in
                      np.atleast_1d(np.asarray(sigma, float)) * np.ones(3))
        w = np.exp(-((KX - k0[0]) ** 2 * sx ** 2
                     + (KY - k0[1]) ** 2 * sy ** 2
                     + (KZ - k0[2]) ** 2 * sz ** 2))
    return w / w.sum(), KX, KY, KZ


def predicted_packet_velocity(shape, sigma, k0, seed: str = "fixed",
                              m: float = 0.0, sign: str = "+", axis: int = 0) -> float:
    """Analytic centroid velocity of a finite-width packet.

    ``seed="fixed"``        — one spinor χ₊(k₀) used at every k. The mismatch at
                              k ≠ k₀ puts weight ``(1−n̂ₓ)/2`` on the counter-
                              propagating branch, giving ``c_lat·⟨n̂ₓ²⟩``.
    ``seed="helicity"``     — the per-k eigenspinor. No admixture, so
                              ``c_lat·⟨n̂ₓ⟩ = ⟨∂ω/∂k_x⟩``.

    For ``m > 0`` the same weighting is applied to the massive closed form.
    """
    w, KX, KY, KZ = packet_momentum_weights(shape, sigma, k0)
    n_hat = _bcc.bcc_spin_axis(KX, KY, KZ, sign=sign)[int(axis)]
    if m:
        # Massive case: only the branch-pure ⟨∂ω/∂k⟩ is available in closed form
        # here. The fixed-4-spinor admixture correction needs the positive-energy
        # projector of D_k and is deliberately NOT modelled — see F20 §Corrections.
        if seed != "helicity":
            raise ValueError(
                "massive fixed-spinor prediction is not closed-form; "
                "use seed='helicity' and compare the measured admixture deficit")
        v = dirac_group_velocity(KX, KY, KZ, m, sign=sign, axis=axis)
        return float(np.sum(w * v))
    if seed == "fixed":
        return float(c_lat * np.sum(w * n_hat ** 2))
    if seed == "helicity":
        return float(c_lat * np.sum(w * n_hat))
    raise ValueError(f"seed must be 'fixed' or 'helicity', got {seed!r}")


# ══════════════════════════════════════════════════════════════════
#  4. The measured run — wrap-free by construction
# ══════════════════════════════════════════════════════════════════

def _fixed_spinor(k0, sign: str = "+"):
    """The +helicity eigenspinor of n̂(k₀)·σ, built analytically (no eig call)."""
    nh = _bcc.bcc_spin_axis(k0[0], k0[1], k0[2], sign=sign)
    nx, ny, nz = (float(nh[0]), float(nh[1]), float(nh[2]))
    theta = np.arccos(np.clip(nz, -1.0, 1.0))
    phi = np.arctan2(ny, nx)
    return np.array([np.cos(theta / 2.0),
                     np.exp(1j * phi) * np.sin(theta / 2.0)], dtype=complex)


def _helicity_pure_seed(env, sign: str = "+"):
    """Branch-pure massless seed: the per-k helicity projector ``(I + n̂·σ)/2``.

    With no counter-propagating admixture the centroid has no ±-branch beat and
    its drift is exactly ``c_lat⟨n̂ₓ⟩``.
    """
    from casim.engine.lattice.geometry import make_kgrid_3d as _kgrid3d
    KX, KY, KZ = _kgrid3d(*env.shape)
    nh = _bcc.bcc_spin_axis(KX, KY, KZ, sign=sign)
    nx, ny, nz = nh[0], nh[1], nh[2]
    a, b = np.ones_like(KX, dtype=complex), 0.5 * np.ones_like(KX, dtype=complex)
    p0 = 0.5 * ((1.0 + nz) * a + (nx - 1j * ny) * b)
    p1 = 0.5 * ((nx + 1j * ny) * a + (1.0 - nz) * b)
    nrm = np.sqrt(np.abs(p0) ** 2 + np.abs(p1) ** 2)
    nrm = np.where(nrm < 1e-14, 1.0, nrm)
    E = _fft.fftn(env)
    return [_fft.ifftn(E * p0 / nrm), _fft.ifftn(E * p1 / nrm)]


def _positive_energy_seed(env, m: float, sign: str = "+"):
    """Branch-pure Dirac seed: P₊(k) applied per k-mode, then re-normalised.

    ``D_k`` has eigenvalues ``e^{∓iω}``, each twofold. The positive-energy
    projector is ``P₊ = (D_k − e^{iω}I)/(e^{−iω} − e^{iω})``. Applying it to a
    constant reference 4-vector and normalising each mode to unit 4-norm gives a
    seed with **no** negative-energy admixture, so the centroid carries no
    zitterbewegung beat and its drift is exactly ``⟨∂ω/∂k_x⟩``.

    This is what F20's Caveats section was reaching for ("the naive η-only seed
    gives an 8.4% velocity error"); doing it per-k rather than at ``k₀`` alone
    removes the residual admixture at ``k ≠ k₀`` as well.
    """
    from casim.engine.lattice.geometry import make_kgrid_3d as _kgrid3d
    KX, KY, KZ = _kgrid3d(*env.shape)
    n_kin = _dbcc._kinetic_n(m)
    A, Ap = _dbcc._bcc_weyl_blocks(KX, KY, KZ, sign=sign)
    omega = _dbcc.bcc_dirac_dispersion(KX, KY, KZ, m, sign=sign)

    one = np.ones_like(KX, dtype=complex)
    ref = (one, 0.5 * one, 0.25 * one, 0.125 * one)     # generic, not an eigenvector
    D = _dbcc._apply_D_k(*ref, n_kin, 1j * m, A, Ap)
    ep, em = np.exp(1j * omega), np.exp(-1j * omega)
    denom = em - ep
    denom = np.where(np.abs(denom) < 1e-14, 1.0, denom)
    P = [(D[i] - ep * ref[i]) / denom for i in range(4)]
    nrm = np.sqrt(sum(np.abs(c) ** 2 for c in P))
    nrm = np.where(nrm < 1e-14, 1.0, nrm)

    E = _fft.fftn(env)
    return [_fft.ifftn(E * c / nrm) for c in P]


def _gaussian_envelope(shape, center, sigma, k0):
    Lx, Ly, Lz = (int(s) for s in shape)
    s = np.atleast_1d(np.asarray(sigma, float)) * np.ones(3)
    X, Y, Z = np.meshgrid(np.arange(Lx), np.arange(Ly), np.arange(Lz), indexing="ij")
    r2 = (((X - center[0]) / s[0]) ** 2
          + ((Y - center[1]) / s[1]) ** 2
          + ((Z - center[2]) / s[2]) ** 2)
    return (np.exp(-r2 / 2.0)
            * np.exp(1j * (k0[0] * X + k0[1] * Y + k0[2] * Z))).astype(np.complex128)


def run_packet(shape=(256, 48, 48), sigma=(6.0, 10.0, 10.0), k0=(0.8, 0.0, 0.0),
               n_steps: int = 44, sample: int = 2, m: float = 0.0,
               sign: str = "+", x_start: float = 60.0, tail_ticks: int = 14,
               seed: str = "fixed"):
    """Propagate a fixed-spinor Gaussian packet and fit dx̄/dt.

    The box is **long in x and the packet starts well inside it**, so the
    envelope never reaches a boundary within ``n_steps``. That is the whole point:
    on a periodic 64³ box the arithmetic centroid picks up a wrap bias of order
    +1.4%, comparable to the physics being measured, and the trend with ``L_x`` is
    monotone and can even exceed ``c_lat``.

    Returns a dict with the fitted slope, the leaked weight at the boundary, and
    the analytic prediction for the same configuration.
    """
    shape = tuple(int(s) for s in shape)
    k0 = tuple(float(k) for k in k0)
    center = (float(x_start), shape[1] / 2.0, shape[2] / 2.0)
    env = _gaussian_envelope(shape, center, sigma, k0)
    chi = _fixed_spinor(k0, sign=sign)

    if m:
        if seed != "branch-pure":
            raise ValueError("the massive run is only defined for seed='branch-pure'")
        fields = _positive_energy_seed(env, m, sign=sign)
    elif seed == "branch-pure":
        fields = _helicity_pure_seed(env, sign=sign)
    elif seed == "fixed":
        fields = [chi[0] * env, chi[1] * env]
    else:
        raise ValueError(f"seed must be 'fixed' or 'branch-pure', got {seed!r}")

    ax = np.arange(shape[0], dtype=float)
    steps, xs, every = [], [], []
    for n in range(n_steps + 1):
        rho = sum(np.abs(c) ** 2 for c in fields)
        wcol = rho.sum(axis=(1, 2))
        xbar = float((ax * wcol).sum() / wcol.sum())
        every.append(xbar)
        if n % sample == 0:
            steps.append(float(n))
            xs.append(xbar)
        if n < n_steps:
            if m:
                fields = list(_dbcc.dirac_step_3d_bcc_splitstep(*fields, m, sign=sign))
            else:
                fields = list(_bcc.weyl_step_3d_bcc(fields[0], fields[1], sign=sign))

    steps_a = np.array(steps)
    A = np.vstack([steps_a, np.ones_like(steps_a)]).T
    slope = float(np.linalg.lstsq(A, np.array(xs), rcond=None)[0][0])

    # The asymptotic drift. A fixed seed spinor puts weight on both branches, so
    # the centroid carries a ±-branch beat at 2ω on top of the drift. The beat
    # dephases across the packet's k-spread, so the per-tick displacement relaxes
    # onto the closed form; the least-squares slope over the WHOLE window (which is
    # what F20 fitted) still carries the transient at the ~2e-4 level.
    per_tick = np.diff(np.array(every))
    tail = per_tick[-tail_ticks:] if tail_ticks else per_tick
    drift = float(tail.mean())

    rho = sum(np.abs(c) ** 2 for c in fields)
    wcol = rho.sum(axis=(1, 2))
    edge = float((wcol[:4].sum() + wcol[-4:].sum()) / wcol.sum())

    pred = predicted_packet_velocity(
        shape, sigma, k0, m=m, sign=sign,
        seed=("helicity" if (m or seed == "branch-pure") else "fixed"))
    return {
        "lstsq_slope": slope,                  # F20's estimator, transient-contaminated
        "asymptotic_drift": drift,             # the physical group velocity
        "predicted_vg": pred,
        "rel_err_lstsq": abs(slope - pred) / abs(pred),
        "rel_err_drift": abs(drift - pred) / abs(pred),
        "vs_c_lat": (drift - c_lat) / c_lat,
        "first_tick_displacement": float(per_tick[0]),
        "edge_weight": edge,
        "shape": list(shape), "sigma": list(sigma), "k0": list(k0),
        "n_steps": int(n_steps), "sample": int(sample), "m": float(m),
        "tail_ticks": int(tail_ticks),
        "seed": seed, "centroid_start": xs[0], "centroid_end": xs[-1],
    }


# ══════════════════════════════════════════════════════════════════
#  5. Registry entry
# ══════════════════════════════════════════════════════════════════

def check_group_velocity_closed_forms(k0: float = 0.8, m: float = 0.3,
                                      n_k: int = 500, h: float = 1e-5):
    """Entry point for the F20 gate record. All-analytic, sub-second.

    Four checks, each with a real failure mode:

    1. the on-axis identity ω(k x̂) = k·c_lat is EXACT (tol 0 up to arccos floor);
    2. the on-axis cone has zero curvature;
    3. the Weyl closed form c_lat·n̂ₓ matches a central difference of the
       analytic dispersion at 30 random off-axis k;
    4. the Dirac closed form matches likewise at mass ``m``.
    """
    res = {}
    res["onaxis_u_residual"] = onaxis_u_residual(n_k=n_k, sign="+")
    res["onaxis_u_residual_minus"] = onaxis_u_residual(n_k=n_k, sign="-")
    res["offaxis_u_residual"] = offaxis_u_residual(n_k=n_k, sign="+")
    res["onaxis_residual"] = onaxis_dispersion_residual(n_k=n_k, sign="+")
    res["onaxis_residual_minus"] = onaxis_dispersion_residual(n_k=n_k, sign="-")
    res["arccos_bound"] = arccos_amplification_bound(n_k=n_k)
    res["onaxis_curvature"] = onaxis_curvature(k0=k0)

    gen = np.random.default_rng(20)
    ks = gen.uniform(-1.2, 1.2, size=(30, 3))

    def _fd(func, i, **kw):
        p = list(ks.T)
        pm = [np.array(c) for c in p]
        pp = [np.array(c) for c in p]
        pp[i] = pp[i] + h
        pm[i] = pm[i] - h
        return (func(*pp, **kw) - func(*pm, **kw)) / (2.0 * h)

    fd_w = _fd(_bcc.bcc_dispersion, 0, sign="+")
    cf_w = weyl_group_velocity(ks[:, 0], ks[:, 1], ks[:, 2], sign="+", axis=0)
    res["weyl_closed_form_residual"] = float(np.max(np.abs(fd_w - cf_w)))

    fd_d = _fd(lambda a, b, c, **kw: _dbcc.bcc_dirac_dispersion(a, b, c, m, **kw), 0, sign="+")
    cf_d = dirac_group_velocity(ks[:, 0], ks[:, 1], ks[:, 2], m, sign="+", axis=0)
    res["dirac_closed_form_residual"] = float(np.max(np.abs(fd_d - cf_d)))

    res["checks"] = {
        # EXACT — tolerance 0, both branches. The identity at the u level.
        "onaxis_u_exact_plus": res["onaxis_u_residual"] == 0.0,
        "onaxis_u_exact_minus": res["onaxis_u_residual_minus"] == 0.0,
        # The control: the same residual off-axis must NOT be zero, otherwise the
        # two checks above are asserting a tautology rather than a direction.
        "offaxis_control_nonzero": res["offaxis_u_residual"] > 1e-3,
        # MACHINE — carried through arccos, bounded by its own conditioning.
        "onaxis_omega_plus": res["onaxis_residual"] <= res["arccos_bound"],
        "onaxis_omega_minus": res["onaxis_residual_minus"] <= res["arccos_bound"],
        "onaxis_flat": abs(res["onaxis_curvature"]) <= 1e-6,
        "weyl_closed_form": res["weyl_closed_form_residual"] <= 1e-8,
        "dirac_closed_form": res["dirac_closed_form_residual"] <= 1e-8,
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


def check_packet_velocity(m: float = 0.3, seed: str = "branch-pure",
                          shape=(256, 64, 64), n_steps: int = 44,
                          tol: float = 1e-12):
    """Entry point for the F20 wavepacket record.

    Propagates a real packet with the engine's own step function in a **wrap-free**
    box and asserts the measured centroid drift equals the closed-form
    ``⟨∂ω/∂k_x⟩`` for the seeded branch.

    Pre-registered tolerance: ``1e-12``, the repo's `machine` class. It is not read
    off the residual — a branch-pure seed has no ±beat, so the centroid velocity is
    an exact Ehrenfest statement and the only error left is float64 FFT round-off.
    The fixed-spinor seed (``seed='fixed'``, massless only) is a different claim and
    relaxes to its closed form only asymptotically; it is checked at ``1e-6``.

    Has a real failure mode: perturbing ``m`` moves both the measurement and the
    prediction (m=0.3 → 0.4654258, m=0.5 → 0.3485063), and mis-stating either
    closed form fails immediately.
    """
    r = run_packet(shape=shape, m=m, seed=seed, n_steps=n_steps)
    if seed != "branch-pure":
        use_tol = 1e-6            # fixed seed: relaxes onto its closed form
    elif m:
        use_tol = float(tol)      # gapped walk: projector regular everywhere
    else:
        # Massless branch-pure: the helicity projector (I + n̂·σ)/2 is SINGULAR at
        # k = 0, where ω = 0 and n̂ is undefined. The packet carries only ~e^{-23}
        # weight there, but the round-off near the singular point is the floor,
        # and it is one decade above the gapped case. Stated, not fitted — the
        # massive walk has no gapless point and does hold at 1e-12.
        use_tol = 1e-11
    r["tol"] = use_tol
    r["checks"] = {
        "drift_matches_closed_form": r["rel_err_drift"] <= use_tol,
        "wrap_free": r["edge_weight"] <= 1e-12,
        "subluminal": r["asymptotic_drift"] < c_lat,
    }
    r["n_pass"] = int(sum(r["checks"].values()))
    r["n_checks"] = len(r["checks"])
    r["ok"] = r["n_pass"] == r["n_checks"]
    return r


if __name__ == "__main__":  # pragma: no cover - artifact write is guarded
    import json
    from casim.engine.particles._results_path import results_path

    out = {"closed_forms": check_group_velocity_closed_forms()}
    out["dirac_m0.3"] = check_packet_velocity(m=0.3, seed="branch-pure")
    out["dirac_m0.5"] = check_packet_velocity(m=0.5, seed="branch-pure")
    out["weyl_branch_pure"] = check_packet_velocity(m=0.0, seed="branch-pure")
    out["weyl_fixed_seed"] = check_packet_velocity(m=0.0, seed="fixed")
    print(json.dumps(out, indent=2))
    with open(results_path("F20_wavepacket_group_velocity.json"), "w") as fh:
        json.dump(out, fh, indent=2)
