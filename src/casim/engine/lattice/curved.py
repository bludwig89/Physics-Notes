"""
ca_curved.py  —  Variable-c stepper  (Phase C1)
=================================================
Approximate refractive-index analog for the Weyl CA.  Allows c to vary
across position via c(x) on the lattice.

Implementation approach
-----------------------
For piecewise-constant c with smooth transitions:
  1. Run the FFT propagator twice — once with c_L, once with c_R.
  2. Position-mask-blend the two results back together using a smooth
     spatial weighting α(x) ∈ [0, 1].

This is **not exactly unitary across the boundary** — there is a small
norm-drift term proportional to (c_L − c_R)² and the gradient of α at
the boundary.  It is a faithful demonstration of qualitative refraction:
a wave packet crossing the boundary changes direction according to a
Snell-like rule for the analog refractive index n = c_0 / c.

For the exact-but-still-CA-friendly path, see C1 in
`ca-next-steps-plan.md` (operator splitting with Trotter error and
sub-stepping).  That is left as a follow-up.
"""

import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from casim.engine.lattice.core import weyl_step_2d_splitstep
from casim.numerics import fft as _fft  # roadmap C1.3: route FFTs through casim.numerics


def make_c_field_step(L, c_left=0.5, c_right=0.25, x_boundary=None,
                       transition_width=2.0):
    """
    Build a smooth two-region c-field with values c_left for x < x_boundary
    and c_right for x > x_boundary.  Transition is a tanh of width
    transition_width.

    Returns
    -------
    c_field : (L, L) array of c values per cell
    """
    if x_boundary is None:
        x_boundary = L // 2
    xs = np.arange(L)
    X, _ = np.meshgrid(xs, xs, indexing='ij')
    alpha = 0.5 * (1.0 + np.tanh((X - x_boundary) / transition_width))
    return c_left * (1.0 - alpha) + c_right * alpha


def weyl_step_2d_varc(f, g, c_field):
    """
    One step of the Weyl CA with position-dependent c — BLENDING method.

    Two FFT propagators (one at c_min, one at c_max) are computed and
    position-weighted blended.  Norm is not exactly conserved — drift
    scales with |∇c|.  Kept for comparison with the Strang-split version
    below; for production runs use `weyl_step_2d_varc_strang`.
    """
    c_lo = float(c_field.min())
    c_hi = float(c_field.max())
    if c_lo == c_hi:
        return weyl_step_2d_splitstep(f, g, c_lo)

    f_lo, g_lo = weyl_step_2d_splitstep(f, g, c_lo)
    f_hi, g_hi = weyl_step_2d_splitstep(f, g, c_hi)

    w = (c_field - c_lo) / (c_hi - c_lo)
    f_new = (1.0 - w) * f_lo + w * f_hi
    g_new = (1.0 - w) * g_lo + w * g_hi
    return f_new, g_new


# ══════════════════════════════════════════════════════════════════
#  Proper Strang splitting for variable-c
# ══════════════════════════════════════════════════════════════════
#
# H(x) = c(x)·σ·p̂  =  c_0·σ·p̂  +  δc(x)·σ·p̂
#                    └ H_0 ┘     └  δH  ┘
#
# Strang symmetric split per timestep:
#     ψ → exp(-i δH dt/2) · exp(-i H_0 dt) · exp(-i δH dt/2) · ψ
#
# H_0 = c_0·σ·p̂ is FFT-diagonal — apply via the existing split-step.
# δH = δc(x)·σ·p̂ is position-space but with a momentum-operator core.
#
# ── F276 (2026-08-01), porting F271's two derived corrections ────────────
# Both defects F271 found and fixed in the 3-D (E,B) dielectric propagator
# were present here, in the 2-D construction F271 was itself lifted from:
#
#   (i)  ORDERING.  δc(x)·σ·p̂ has an operator-ordering ambiguity, and the
#        asymmetric choice is not self-adjoint, so the generator is not
#        anti-Hermitian and the evolution is not unitary AT ANY STEP SIZE.
#        Measured before the fix: norm drift PLATEAUED at 6.08e-2 and a 32x
#        refinement moved it 0.23%.  Weyl-symmetric ordering makes the
#        generator exactly anti-Hermitian, so the residual is pure Taylor
#        truncation and CONVERGES.
#   (ii) TRUNCATION ORDER.  exp(-hW) = I - hW + h²W²/2 + O(h³); keeping only
#        I - hW leaves an O(h²) local error Strang does not cancel, so the
#        scheme was globally FIRST order despite the symmetric composition.
#        The h²W²/2 term is free to derive and restores second order.
#
# See `casim.engine.gauge.photon._M_weyl` / `_dielectric_half` for the same
# two corrections in the (E,B) sector, and F271/F276 for the measurements.
# ══════════════════════════════════════════════════════════════════

_kgrid2d_cache: dict = {}


def _kgrid_2d(Lx, Ly):
    """Cached (KX, KY) spectral first-derivative multipliers, Nyquist-zeroed.

    The Nyquist zeroing is required, not cosmetic.  For even ``L`` the FFT
    frequency set contains ``-pi`` with no ``+pi`` partner, so the symbol
    ``ik`` is not odd there and the spectral derivative is **not**
    anti-Hermitian at that bin — which would reintroduce exactly the
    non-unitarity correction (i) exists to remove.  Zeroing the Nyquist
    multiplier is the standard spectral remedy and is what the centred
    finite-difference path does automatically.
    """
    key = (Lx, Ly)
    if key not in _kgrid2d_cache:
        kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
        ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
        if Lx % 2 == 0:
            kx[Lx // 2] = 0.0
        if Ly % 2 == 0:
            ky[Ly // 2] = 0.0
        KX, KY = np.meshgrid(kx, ky, indexing='ij')
        KX.setflags(write=False)
        KY.setflags(write=False)
        _kgrid2d_cache[key] = (KX, KY)
    return _kgrid2d_cache[key]


def _sigma_grad_2d(f, g, use_fft=True):
    """Apply ``σ·∇`` to the 2-spinor ψ = (f, g).

        (σ·∇ψ)_top = ∂_x g − i ∂_y g
        (σ·∇ψ)_bot = ∂_x f + i ∂_y f

    ``σ·∇`` is anti-Hermitian on the periodic lattice — spectrally once the
    Nyquist bin is zeroed (see :func:`_kgrid_2d`), and identically for the
    centred difference, which is anti-symmetric by construction.
    """
    if use_fft:
        KX, KY = _kgrid_2d(*f.shape)
        F = _fft.fft2(f)
        G = _fft.fft2(g)
        sg_f = _fft.ifft2(1j * KX * G + KY * G)   # ikx·g − i·iky·g
        sg_g = _fft.ifft2(1j * KX * F - KY * F)   # ikx·f + i·iky·f
    else:
        dgx = (np.roll(g, -1, axis=0) - np.roll(g, 1, axis=0)) * 0.5
        dgy = (np.roll(g, -1, axis=1) - np.roll(g, 1, axis=1)) * 0.5
        dfx = (np.roll(f, -1, axis=0) - np.roll(f, 1, axis=0)) * 0.5
        dfy = (np.roll(f, -1, axis=1) - np.roll(f, 1, axis=1)) * 0.5
        sg_f = dgx - 1j * dgy
        sg_g = dfx + 1j * dfy
    return sg_f, sg_g


def _W_dH(f, g, dc, use_fft=True, ordering='weyl'):
    """The generator ``W`` of the inhomogeneous half-step, ``exp(-h W)``.

    ``δH = δc(x)·σ·p̂`` with ``σ·p̂ = -i σ·∇``, so ``-i δH = -W`` with

        W = ½ {δc, σ·∇}      (Weyl / symmetric — the canonical choice)
        W = δc · (σ·∇)       (asymmetric — SUPERSEDED, retained for F276)

    ``δc`` is Hermitian and ``σ·∇`` anti-Hermitian, so their **anticommutator**
    is anti-Hermitian and ``exp(-hW)`` is exactly unitary.  The asymmetric
    product is neither, which is why its norm error plateaus rather than
    converging.

    ``ordering='asymmetric'`` reproduces the pre-F276 operator bit-for-bit and
    exists so the superseded scheme stays measurable, not as a supported mode.
    """
    if ordering == 'asymmetric':
        a_f, a_g = _sigma_grad_2d(f, g, use_fft)
        return dc * a_f, dc * a_g
    if ordering != 'weyl':
        raise ValueError(f"ordering must be 'weyl' or 'asymmetric', got {ordering!r}")
    a_f, a_g = _sigma_grad_2d(f, g, use_fft)              # (σ·∇)ψ  → then δc·
    b_f, b_g = _sigma_grad_2d(dc * f, dc * g, use_fft)    # (σ·∇)(δc ψ)
    return 0.5 * (dc * a_f + b_f), 0.5 * (dc * a_g + b_g)


def _half_step_dH(f, g, dc, dt, use_fft=True, ordering='weyl', order=2):
    """Apply ``exp(-i δH dt) ψ`` to second order, ``δH = δc(x)·σ·p̂``.

    With ``W = ½{δc, σ·∇}`` anti-Hermitian (:func:`_W_dH`),

    .. math:: e^{-hW} = \\mathbb{I} - hW + \\tfrac{h^2}{2}W^2 + O(h^3)

    and both retained terms are cheap: ``W²`` is one more application of the
    same operator.  The truncation is unitary to ``O(h³)`` and, crucially,
    its norm error **converges** with sub-stepping instead of plateauing,
    because the generator itself is now anti-Hermitian.

    Parameters
    ----------
    ordering : {'weyl', 'asymmetric'}
        ``'asymmetric'`` restores the pre-F276 non-self-adjoint product.
    order : {1, 2}
        ``1`` restores the pre-F276 first-order truncation.

    The two legacy switches are how F276's before/after is measured; neither
    is a supported production setting.
    """
    W_f, W_g = _W_dH(f, g, dc, use_fft, ordering)
    f_new = f - dt * W_f
    g_new = g - dt * W_g
    if order >= 2:
        WW_f, WW_g = _W_dH(W_f, W_g, dc, use_fft, ordering)
        f_new = f_new + 0.5 * dt * dt * WW_f
        g_new = g_new + 0.5 * dt * dt * WW_g
    return f_new, g_new


# ══════════════════════════════════════════════════════════════════
#  P3 (2026-05-15) — Cayley / Crank–Nicolson exact-unitary stepper
# ══════════════════════════════════════════════════════════════════
#
# Solves   (I + i·dt/2·H_disc)·ψ_new = (I − i·dt/2·H_disc)·ψ_old
#
# where H_disc is the *Hermitized* discrete Weyl operator with variable
# c(x):  the centered first-difference is taken with the **face-averaged**
# c — c_face(i+½, j) = (c(i,j) + c(i+1,j))/2 — to make the discrete
# operator exactly Hermitian on the periodic lattice.  The Cayley
# transform of a Hermitian operator is unitary at the discrete level:
# norm is conserved to the linear-solver tolerance (1e-14 with LU).
#
# Cost: one sparse LU factorisation per c_field change (~5 ms for L=64);
# each subsequent step is one back-substitution (~1 ms).  For static
# c-field problems (Snell), factor once and reuse.  For dynamic c-field
# problems (F3b — c sourced by Φ), refactor each step or every few steps.
# ══════════════════════════════════════════════════════════════════

def _build_cayley_matrix_2d(c_field, dt, sign=+1.0):
    """
    Build sparse  M = I + sign·i·dt/2·H_disc  for the 2D variable-c Weyl
    operator on a periodic lattice with face-averaged c.

    Vector layout: flat array of size 2·L² with the first L² entries
    holding f (component 0) and the next L² holding g (component 1),
    each in row-major order.

    Returns scipy.sparse.csc_matrix of shape (2L², 2L²), complex.

    Coefficient algebra
    -------------------
    For 2D, σ·k = σ_x·k_x + σ_y·k_y with σ_x = ((0,1),(1,0)), σ_y =
    ((0,−i),(i,0)).  H_disc = c·σ·(−i·∇).  On f-row, H_f = −i·T_x·g −
    T_y·g where T_h(c) is the Hermitized centred difference with face-
    averaged c:

        [T_h(c)·g](i,j) = (c_face(i+½)·g_{i+1} − c_face(i−½)·g_{i−1}) / 2

    so [i·dt/2·H]_f = (dt/4)·(c_face_xp·g_xp − c_face_xm·g_xm) −
                      (i·dt/4)·(c_face_yp·g_yp − c_face_ym·g_ym).
    The g-row swaps σ_y's sign on the y term.
    """
    Lx, Ly = c_field.shape
    N = Lx * Ly

    # Face-averaged c at the +/-x, +/-y faces of each cell.
    cxp = 0.5 * (c_field + np.roll(c_field, -1, axis=0))   # face at (i+½, j)
    cxm = 0.5 * (c_field + np.roll(c_field, +1, axis=0))   # face at (i−½, j)
    cyp = 0.5 * (c_field + np.roll(c_field, -1, axis=1))   # face at (i, j+½)
    cym = 0.5 * (c_field + np.roll(c_field, +1, axis=1))   # face at (i, j−½)

    coef = sign * dt * 0.25   # = sign·dt/4

    # Flat indices for the cells and their 4 neighbours, vectorised.
    ii, jj = np.indices((Lx, Ly))
    idx_self = ii * Ly + jj                               # (Lx, Ly)
    idx_xp = ((ii + 1) % Lx) * Ly + jj
    idx_xm = ((ii - 1) % Lx) * Ly + jj
    idx_yp = ii * Ly + ((jj + 1) % Ly)
    idx_ym = ii * Ly + ((jj - 1) % Ly)

    flat_self = idx_self.ravel()                          # (N,)
    flat_xp = idx_xp.ravel(); flat_xm = idx_xm.ravel()
    flat_yp = idx_yp.ravel(); flat_ym = idx_ym.ravel()
    cxp_f = cxp.ravel(); cxm_f = cxm.ravel()
    cyp_f = cyp.ravel(); cym_f = cym.ravel()

    # Build COO triplets.  For each cell, 1 diagonal entry + 4 off-diag
    # entries per spinor component, so 2·(1+4) = 10 nonzeros per cell.
    rows = np.empty(10 * N, dtype=np.int64)
    cols = np.empty(10 * N, dtype=np.int64)
    vals = np.empty(10 * N, dtype=np.complex128)

    # Row of f-component (index_self), columns 0..N-1 are f, N..2N-1 are g.
    # Diagonal on (f, f)
    rows[0*N:1*N] = flat_self;             cols[0*N:1*N] = flat_self;             vals[0*N:1*N] = 1.0
    # f-row, off-diag on g-columns
    rows[1*N:2*N] = flat_self;             cols[1*N:2*N] = flat_xp + N;           vals[1*N:2*N] = coef * cxp_f
    rows[2*N:3*N] = flat_self;             cols[2*N:3*N] = flat_xm + N;           vals[2*N:3*N] = -coef * cxm_f
    rows[3*N:4*N] = flat_self;             cols[3*N:4*N] = flat_yp + N;           vals[3*N:4*N] = -1j * coef * cyp_f
    rows[4*N:5*N] = flat_self;             cols[4*N:5*N] = flat_ym + N;           vals[4*N:5*N] = +1j * coef * cym_f
    # Diagonal on (g, g)
    rows[5*N:6*N] = flat_self + N;         cols[5*N:6*N] = flat_self + N;         vals[5*N:6*N] = 1.0
    # g-row, off-diag on f-columns (opposite y-sign vs f-row from σ_y)
    rows[6*N:7*N] = flat_self + N;         cols[6*N:7*N] = flat_xp;               vals[6*N:7*N] = coef * cxp_f
    rows[7*N:8*N] = flat_self + N;         cols[7*N:8*N] = flat_xm;               vals[7*N:8*N] = -coef * cxm_f
    rows[8*N:9*N] = flat_self + N;         cols[8*N:9*N] = flat_yp;               vals[8*N:9*N] = +1j * coef * cyp_f
    rows[9*N:10*N] = flat_self + N;        cols[9*N:10*N] = flat_ym;              vals[9*N:10*N] = -1j * coef * cym_f

    return sp.csc_matrix((vals, (rows, cols)), shape=(2 * N, 2 * N), dtype=np.complex128)


class CayleyVarcSolver2D:
    """
    Reusable variable-c Cayley solver.  Factorises the LHS matrix M once;
    each subsequent .step(f, g) does `n_sub` back-substitutions to advance
    one external timestep.

    Why sub-step?  Cayley/Crank–Nicolson is exactly unitary at any dt, but
    has O(dt²) numerical dispersion per micro-step.  For Snell-law-type
    direction measurements, sub-stepping (n_sub≥4) keeps the phase error
    below the angular resolution.  Norm conservation is unaffected by
    sub-stepping (every micro-step is still exact-unitary).

    Use when c(x, t) is static (Snell) or refactor when it changes (F3b)
    via `.refactor(c_field, dt, n_sub)`.
    """
    __slots__ = ('Lx', 'Ly', 'N', 'dt_ext', 'dt_sub', 'n_sub',
                 'M', 'N_mat', 'lu', '_c_field')

    def __init__(self, c_field, dt=1.0, n_sub=4):
        self.Lx, self.Ly = c_field.shape
        self.N = self.Lx * self.Ly
        self.refactor(c_field, dt, n_sub)

    def refactor(self, c_field, dt=None, n_sub=None):
        if dt is not None:
            self.dt_ext = float(dt)
        if n_sub is not None:
            self.n_sub  = int(n_sub)
        self._c_field = c_field
        self.dt_sub  = self.dt_ext / self.n_sub
        self.M       = _build_cayley_matrix_2d(c_field, self.dt_sub, sign=+1.0)
        self.N_mat   = _build_cayley_matrix_2d(c_field, self.dt_sub, sign=-1.0)
        self.lu      = spla.splu(self.M)

    def step(self, f, g):
        """Advance one *external* timestep (= n_sub Cayley micro-steps)."""
        Lx, Ly, N = self.Lx, self.Ly, self.N
        psi = np.empty(2 * N, dtype=np.complex128)
        psi[:N] = f.ravel()
        psi[N:] = g.ravel()
        for _ in range(self.n_sub):
            rhs = self.N_mat @ psi
            psi = self.lu.solve(rhs)
        return psi[:N].reshape(Lx, Ly), psi[N:].reshape(Lx, Ly)


def weyl_step_2d_varc_cayley(f, g, c_field, dt=1.0, n_sub=4):
    """
    One external Cayley step (no caching).  For repeated calls with the
    same c_field, use `CayleyVarcSolver2D` to amortise the LU factorisation.
    """
    solver = CayleyVarcSolver2D(c_field, dt=dt, n_sub=n_sub)
    return solver.step(f, g)


def weyl_step_2d_varc_strang(f, g, c_field, n_sub=4,
                             ordering='weyl', order=2):
    """
    Variable-c Weyl propagator using proper Strang operator splitting.

    Parameters
    ----------
    c_field : (Lx, Ly) array — position-dependent c.
    n_sub : int — number of sub-steps in one timestep (default 4).
    ordering, order : passed through to :func:`_half_step_dH`; the defaults
        are the F276 Weyl-symmetric second-order scheme.  The legacy values
        ``('asymmetric', 1)`` reproduce the pre-F276 stepper bit-for-bit.

    Convergence (F276, measured — supersedes the pre-F276 docstring's
    "Trotter error drops like 1/n_sub², norm drift drops like 1/n_sub",
    which described a scheme that was globally first order and whose norm
    error did not drop at all):

    * norm drift **converges** instead of plateauing at 6.08e-2;
    * global order **2**, which is what the Strang composition was always
      supposed to deliver.

    Returns
    -------
    (f_new, g_new)
    """
    c0 = float(c_field.mean())
    dc = c_field - c0
    dt_sub = 1.0 / n_sub

    for _ in range(n_sub):
        # Half-step δH
        f, g = _half_step_dH(f, g, dc, dt_sub * 0.5, ordering=ordering, order=order)
        # Full kinetic step (FFT, exact unitary)
        f, g = weyl_step_2d_splitstep(f, g, c0 * dt_sub)
        # Second half-step δH
        f, g = _half_step_dH(f, g, dc, dt_sub * 0.5, ordering=ordering, order=order)

    return f, g


def f276_convergence_check(L=48, ticks=10, dc_amp=0.05) -> bool:
    """F276 falsification handle, as a registry entry point (D9).

    Two sharp claims, both of which the algebra fixes and neither of which is
    fitted:

    1. **Global order is exactly 2.**  Self-convergence against a refined
       reference must show exponent 2 to within 0.1.  The pre-F276 scheme
       measures **0.00** here — it does not converge to the true operator at
       all — so this assertion cannot pass by accident.
    2. **Norm error converges as** :math:`1/n_\\text{sub}^3`, because the Weyl
       generator is anti-Hermitian.  Ratio per doubling must be >= 6 (ideal 8).
       The pre-F276 ratio is 1.00, a plateau.

    Returns True, or raises AssertionError naming the measurement that failed.
    """
    x = np.arange(L) - L / 2
    f0 = (np.exp(-(x[:, None] ** 2 + x[None, :] ** 2) / 64).astype(complex)
          * np.exp(1j * 0.4 * x[:, None]))
    g0 = f0 * 0.3
    c_field = 0.5 + dc_amp * np.tanh(x[:, None] / 8.0) * np.ones((L, L))
    n0 = float(np.sum(np.abs(f0) ** 2 + np.abs(g0) ** 2))

    def run(n_sub):
        f, g = f0.copy(), g0.copy()
        for _ in range(ticks):
            f, g = weyl_step_2d_varc_strang(f, g, c_field, n_sub=n_sub)
        return f, g

    # (1) global order
    ref = run(256)
    errs = []
    for n in (2, 4, 8):
        f, g = run(n)
        errs.append(max(float(np.abs(f - ref[0]).max()),
                        float(np.abs(g - ref[1]).max())))
    orders = [math.log(errs[i] / errs[i + 1]) / math.log(2.0)
              for i in range(len(errs) - 1)]
    assert all(abs(o - 2.0) < 0.1 for o in orders), \
        f"F276: global order must be 2, measured {orders}"

    # (2) norm-error convergence rate
    drifts = []
    for n in (2, 4, 8, 16):
        f, g = run(n)
        drifts.append(abs(float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2)) - n0) / n0)
    ratios = [drifts[i] / drifts[i + 1] for i in range(len(drifts) - 1)]
    assert all(r >= 6.0 for r in ratios), \
        f"F276: norm error must converge as 1/n^3 (ratio>=6), measured {ratios}"
    return True


def measure_refraction(L=128, n_steps=80, c_left=0.5, c_right=0.25,
                        k_in=(0.4, 0.2), sigma=6.0, x_start_frac=0.2,
                        method='strang', n_sub=4):
    """
    Send a Gaussian wave packet from the left region into the right region
    and measure the direction change.

    The incoming wave has angle θ_in from the normal (boundary is vertical).
    Snell's law for the analog n = c_0 / c gives:
        n_L sin(θ_L) = n_R sin(θ_R)
    i.e.   sin(θ_L) / c_L  =  sin(θ_R) / c_R
    so a packet from a faster region to slower region bends toward the normal.

    Returns
    -------
    dict with measured incoming and outgoing direction angles and the
    Snell-predicted outgoing angle.

    .. warning::

       **The outgoing-angle diagnostic does not work, and this is a defect of
       the MEASUREMENT, not of any stepper** (audit V, F276).  At the shipped
       defaults it returns ``theta_out_deg`` ~165 deg against
       ``theta_out_pred_deg`` ~13 deg, and it does so for **all three**
       methods — including ``method='cayley'``, which is exactly unitary by
       construction (~172 deg).  A quantity that is equally wrong under an
       exact stepper is not measuring the stepper.

       The cause is the geometry, not the physics: the lattice is **periodic**,
       so the packet wraps and re-enters, and the right-region centroid in the
       late-time fit window is a mixture of transmitted, reflected and wrapped
       amplitude.  ``arctan2`` of a backward-drifting centroid then lands near
       180 deg.

       Nothing in the test registry asserts this function's angles — its only
       callers are two ``legacy_script`` runners — so no published claim rests
       on it.  **But no published claim is supported by it either**: a
       quantitative Snell confrontation needs open/absorbing boundaries and a
       transmitted-component projection, and that is unbuilt.  ``norm_drift``
       in the returned dict *is* meaningful and is what F276 improved
       (0.0915 -> 0.0 at the defaults).
    """
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    # Initial packet in the left half
    cx0 = int(x_start_frac * L)
    cy0 = L // 2
    envelope = np.exp(-((X - cx0)**2 + (Y - cy0)**2) / (2.0 * sigma**2))
    phase = np.exp(1j * (k_in[0] * X + k_in[1] * Y))

    kappa = float(np.sqrt(k_in[0]**2 + k_in[1]**2))
    phi = np.exp(1j * np.arctan2(k_in[1], k_in[0]))
    h = np.array([1.0, phi], dtype=complex) / np.sqrt(2.0)
    f = h[0] * envelope * phase
    g = h[1] * envelope * phase

    c_field = make_c_field_step(L, c_left=c_left, c_right=c_right,
                                 x_boundary=L // 2, transition_width=2.0)

    # Track centroid in left and right regions separately
    boundary = L // 2
    left_mask = X < boundary
    right_mask = X >= boundary

    centroids_left  = []
    centroids_right = []
    norms = []

    if method == 'strang':
        step_fn = lambda f_, g_: weyl_step_2d_varc_strang(f_, g_, c_field, n_sub=n_sub)
    elif method == 'cayley':
        # P3 (2026-05-15): exact-unitary Cayley/Crank–Nicolson stepper.
        # Static c-field → factor LU once, reuse for every step.
        solver = CayleyVarcSolver2D(c_field, dt=1.0)
        step_fn = lambda f_, g_: solver.step(f_, g_)
    else:
        step_fn = lambda f_, g_: weyl_step_2d_varc(f_, g_, c_field)

    for step in range(n_steps + 1):
        density = np.abs(f)**2 + np.abs(g)**2
        norms.append(float(density.sum()))
        for mask, lst in [(left_mask, centroids_left),
                          (right_mask, centroids_right)]:
            tot = float(density[mask].sum())
            if tot > 1e-6:
                cx = float((X[mask] * density[mask]).sum() / tot)
                cy = float((Y[mask] * density[mask]).sum() / tot)
            else:
                cx, cy = float('nan'), float('nan')
            lst.append((cx, cy, tot))
        if step < n_steps:
            f, g = step_fn(f, g)

    centroids_left  = np.array(centroids_left)
    centroids_right = np.array(centroids_right)

    # Fit incoming direction (early-time slope of left-region centroid)
    early = slice(2, n_steps // 4)
    ts = np.arange(n_steps + 1)
    valid = ~np.isnan(centroids_left[early, 0])
    if valid.sum() < 3:
        v_in = (float('nan'), float('nan'))
    else:
        v_in = (
            float(np.polyfit(ts[early][valid], centroids_left[early, 0][valid], 1)[0]),
            float(np.polyfit(ts[early][valid], centroids_left[early, 1][valid], 1)[0]),
        )

    # Fit outgoing direction (late-time slope of right-region centroid)
    late = slice(3 * n_steps // 4, n_steps + 1)
    valid = ~np.isnan(centroids_right[late, 0])
    if valid.sum() < 3:
        v_out = (float('nan'), float('nan'))
    else:
        v_out = (
            float(np.polyfit(ts[late][valid], centroids_right[late, 0][valid], 1)[0]),
            float(np.polyfit(ts[late][valid], centroids_right[late, 1][valid], 1)[0]),
        )

    # Angles from the boundary normal (the boundary is vertical, so the
    # normal is along x; θ is measured from +x axis)
    theta_in  = float(np.arctan2(v_in[1],  v_in[0]))   # may be 0 if v_in along +x
    theta_out = float(np.arctan2(v_out[1], v_out[0]))

    # Snell prediction: sin(θ_L)/c_L = sin(θ_R)/c_R
    sin_theta_in = np.sin(theta_in)
    sin_theta_pred = sin_theta_in * (c_right / c_left)
    if abs(sin_theta_pred) > 1.0:
        theta_out_pred = float('nan')   # total internal reflection
    else:
        theta_out_pred = float(np.arcsin(sin_theta_pred))

    norms = np.array(norms)
    norm_drift = float(abs(norms[-1] - norms[0]) / norms[0]) if norms[0] > 0 else 0.0

    return {
        'v_in':           v_in,
        'v_out':          v_out,
        'theta_in_deg':   float(np.degrees(theta_in)),
        'theta_out_deg':  float(np.degrees(theta_out)),
        'theta_out_pred_deg':  float(np.degrees(theta_out_pred))
                              if not np.isnan(theta_out_pred) else float('nan'),
        'snell_ratio_in':   sin_theta_in / c_left,
        'snell_ratio_out':  np.sin(theta_out) / c_right,
        'norm_drift':       norm_drift,
        'method':           method,
    }
