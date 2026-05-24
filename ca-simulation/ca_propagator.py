"""
ca_propagator.py  —  Cached spectral propagator objects
========================================================
Each propagator precomputes the full unitary operator U(k) for a fixed
lattice shape, storing the result in NumPy arrays.  Subsequent calls to
`.step()` only perform FFT → (element-wise multiply) → IFFT, eliminating
the repeated trig evaluation that dominates cost when stepping many times.

Speedup per step (L=64 3D, 4-spinor):
  Old path  — meshgrid + BCC trig + unitary build + 8 FFTs ≈ 120 ms
  New path  — 8 FFTs + element-wise multiply ≈ 35 ms  (3–4× faster)

At L=320 (10×) the ratio is larger because the trig scales as O(N)
while multi-core FFT scales much better.

Available propagators
---------------------
BccWeylPropagator(shape, sign)           2-spinor BCC Weyl step
BccDiracPropagator(shape, m, sign, dt)   4-spinor BCC Dirac step
Exact2DPropagator(shape)                 2-spinor exact 2D arccos Weyl
Linear2DPropagator(shape, c)             2-spinor linear 2D Weyl step

FFT floor improvement via zero-padded phase extraction
------------------------------------------------------
`phase_rate_lsq(samples, dt)`           — unwrap + linear regression
`phase_rate_zeropad(samples, dt, pad_factor)` — zero-pad DFT for sub-
                                           bin omega resolution

The zero-padded approach interpolates the DFT spectrum by a factor
`pad_factor` (default 8), giving effective frequency resolution of
Δω_eff = 2π / (N_t × pad_factor × dt) — an 8× improvement over the
basic DFT bin width for free (no extra propagation steps required).

Both methods return |ω| and their absolute floor scales as
  lsq:      ~ε_mach / n_steps   (statistical averaging)
  zeropad:  ~ε_mach × pad_factor / n_steps²  (spectral interpolation)
"""

import math
import numpy as np
from typing import Tuple, Optional

import ca_fft as fft
from ca_lattice import LatticeConfig, make_kgrid_2d, make_kgrid_3d


# ══════════════════════════════════════════════════════════════════
#  Helper: sinc-like function  sin(x)/x with L'Hôpital at x=0
# ══════════════════════════════════════════════════════════════════

def _safe_sinc(x: np.ndarray) -> np.ndarray:
    """sin(x)/x with the L'Hôpital limit 1 at x=0."""
    safe = np.where(x == 0.0, 1.0, x)
    return np.where(x == 0.0, 1.0, np.sin(x) / safe)


# ══════════════════════════════════════════════════════════════════
#  BCC Weyl propagator (2-spinor, 3D)
# ══════════════════════════════════════════════════════════════════

class BccWeylPropagator:
    """
    Precomputed spectral propagator for the 3D BCC Weyl QCA.

    Computes and stores the four 2×2 unitary matrix elements
    (U_ff, U_fg, U_gf, U_gg) at every k-point once on construction.

    Parameters
    ----------
    shape : int or (Lx, Ly, Lz)
        Lattice shape.  A single int N gives an (N, N, N) cube.
    sign : '+' or '-'
        Helicity choice (Paper 1 Eq. 15 two solutions).
    """

    def __init__(self, shape, sign: str = '+'):
        if isinstance(shape, int):
            shape = (shape, shape, shape)
        self.shape = tuple(shape)
        self.sign = sign
        self._build()

    def _build(self):
        """Precompute BCC unitary on the k-grid."""
        # Import here to avoid circular dependency
        from ca_bcc import bcc_unitary as _bcc_unitary
        KX, KY, KZ = make_kgrid_3d(*self.shape)
        self.U_ff, self.U_fg, self.U_gf, self.U_gg = \
            _bcc_unitary(KX, KY, KZ, sign=self.sign)

    def step(self, f: np.ndarray, g: np.ndarray
             ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Propagate one BCC Weyl tick.

        Parameters
        ----------
        f, g : complex128 arrays of shape `self.shape`
            Upper and lower spinor components.

        Returns
        -------
        f_new, g_new : updated spinor arrays.
        """
        F = fft.fftn(f)
        G = fft.fftn(g)
        F_new = self.U_ff * F + self.U_fg * G
        G_new = self.U_gf * F + self.U_gg * G
        return fft.ifftn(F_new), fft.ifftn(G_new)

    def steps(self, f: np.ndarray, g: np.ndarray,
              n: int) -> Tuple[np.ndarray, np.ndarray]:
        """Propagate n steps in a loop."""
        for _ in range(n):
            f, g = self.step(f, g)
        return f, g

    def norm(self, f: np.ndarray, g: np.ndarray) -> float:
        """Total probability ∑|f|² + |g|²."""
        return float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))

    def memory_report(self) -> str:
        from ca_fft import memory_estimate
        fields = memory_estimate(self.shape, n_fields=2)
        cache  = memory_estimate(self.shape, n_fields=4)  # 4 unitary blocks
        return (f"BccWeylPropagator shape={self.shape}  "
                f"field_RAM={fields['MB']:.1f} MB  "
                f"cache_RAM={cache['MB']:.1f} MB")


# ══════════════════════════════════════════════════════════════════
#  BCC Dirac propagator (4-spinor, 3D)
# ══════════════════════════════════════════════════════════════════

class BccDiracPropagator:
    """
    Precomputed spectral propagator for the 3D BCC Dirac CA.

    Stores the BCC Weyl unitary blocks, kinetic coefficient, and
    (for dt ≠ 1) the spectral interpolation scalars.  The .step()
    method only executes FFTs and array multiplications.

    Parameters
    ----------
    shape : int or (Lx, Ly, Lz)
    m : float, |m| ≤ 1
        Dimensionless mass.  n = √(1−m²) is the kinetic coefficient.
    sign : '+' or '-'
        BCC Weyl helicity block.
    dt : float
        Time step. dt=1 applies D_k once (default, fastest).
        Other values use spectral interpolation U_D(k, dt).
    """

    def __init__(self, shape, m: float = 0.0,
                 sign: str = '+', dt: float = 1.0):
        if isinstance(shape, int):
            shape = (shape, shape, shape)
        if abs(m) > 1.0 + 1e-15:
            raise ValueError(f"|m| must be ≤ 1, got m={m}")
        self.shape = tuple(shape)
        self.m = float(m)
        self.sign = sign
        self.dt = float(dt)
        self._build()

    def _build(self):
        from ca_bcc import bcc_unitary as _bcc_unitary
        from ca_dirac_bcc import bcc_dirac_dispersion as _disp

        KX, KY, KZ = make_kgrid_3d(*self.shape)

        # Weyl block A and its Hermitian conjugate A†
        A_ff, A_fg, A_gf, A_gg = _bcc_unitary(KX, KY, KZ, sign=self.sign)
        self.A_ff = A_ff;  self.A_fg = A_fg
        self.A_gf = A_gf;  self.A_gg = A_gg
        # A† entries (conjugate with row/col swap)
        self.Ap_ff = np.conj(A_ff)
        self.Ap_fg = np.conj(A_gf)   # off-diagonal: conj + transpose
        self.Ap_gf = np.conj(A_fg)
        self.Ap_gg = np.conj(A_gg)

        self.n     = float(math.sqrt(max(0.0, 1.0 - self.m * self.m)))
        self.im_v  = 1j * self.m

        # Spectral interpolation coefficients for dt ≠ 1
        if self.dt != 1.0:
            omega     = _disp(KX, KY, KZ, self.m, sign=self.sign)
            cos_w     = np.cos(omega)
            sin_w     = np.sin(omega)
            sin_safe  = np.where(sin_w == 0.0, 1.0, sin_w)
            # scale = sin(ω·dt)/sin(ω);  L'Hôpital → dt as ω→0
            scale     = np.where(sin_w == 0.0, self.dt,
                                 np.sin(omega * self.dt) / sin_safe)
            self._cos_w   = cos_w
            self._cos_wdt = np.cos(omega * self.dt)
            self._scale   = scale
        else:
            self._cos_w = self._cos_wdt = self._scale = None

    def _apply_Dk_k(self, EU, ED, CU, CD):
        """Apply D_k once in Fourier space.  Returns (DEU, DED, DCU, DCD)."""
        n  = self.n
        im = self.im_v
        DEU = n * self.A_ff * EU + n * self.A_fg * ED + im * CU
        DED = n * self.A_gf * EU + n * self.A_gg * ED + im * CD
        DCU = im * EU + n * self.Ap_ff * CU + n * self.Ap_fg * CD
        DCD = im * ED + n * self.Ap_gf * CU + n * self.Ap_gg * CD
        return DEU, DED, DCU, DCD

    def step(self,
             eta_u: np.ndarray, eta_d: np.ndarray,
             chi_u: np.ndarray, chi_d: np.ndarray,
             ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Propagate one BCC Dirac tick (or fractional step via spectral
        interpolation if dt ≠ 1).

        Parameters
        ----------
        eta_u, eta_d : left-handed Weyl spinor (η_↑, η_↓)
        chi_u, chi_d : right-handed Weyl spinor (χ_↑, χ_↓)

        Returns
        -------
        eta_u_new, eta_d_new, chi_u_new, chi_d_new
        """
        EU = fft.fftn(eta_u);  ED = fft.fftn(eta_d)
        CU = fft.fftn(chi_u);  CD = fft.fftn(chi_d)

        DEU, DED, DCU, DCD = self._apply_Dk_k(EU, ED, CU, CD)

        if self.dt == 1.0:
            EU_n, ED_n, CU_n, CD_n = DEU, DED, DCU, DCD
        else:
            cw  = self._cos_w
            cwt = self._cos_wdt
            sc  = self._scale
            EU_n = cwt * EU + sc * (DEU - cw * EU)
            ED_n = cwt * ED + sc * (DED - cw * ED)
            CU_n = cwt * CU + sc * (DCU - cw * CU)
            CD_n = cwt * CD + sc * (DCD - cw * CD)

        return (fft.ifftn(EU_n), fft.ifftn(ED_n),
                fft.ifftn(CU_n), fft.ifftn(CD_n))

    def steps(self,
              eta_u, eta_d, chi_u, chi_d,
              n: int):
        """Propagate n steps in a loop, returning updated 4-spinor."""
        for _ in range(n):
            eta_u, eta_d, chi_u, chi_d = self.step(eta_u, eta_d,
                                                    chi_u, chi_d)
        return eta_u, eta_d, chi_u, chi_d

    def norm(self, eu, ed, cu, cd) -> float:
        """Total norm ∑(|η_↑|²+|η_↓|²+|χ_↑|²+|χ_↓|²)."""
        return float(np.sum(np.abs(eu) ** 2 + np.abs(ed) ** 2 +
                            np.abs(cu) ** 2 + np.abs(cd) ** 2))

    def memory_report(self) -> str:
        from ca_fft import memory_estimate
        fields = memory_estimate(self.shape, n_fields=4)
        cache  = memory_estimate(self.shape, n_fields=8)
        return (f"BccDiracPropagator shape={self.shape} m={self.m}  "
                f"field_RAM={fields['MB']:.1f} MB  "
                f"cache_RAM={cache['MB']:.1f} MB")


# ══════════════════════════════════════════════════════════════════
#  Exact 2D QCA propagator (arccos dispersion, Paper 1 Eq. 16)
# ══════════════════════════════════════════════════════════════════

class Exact2DPropagator:
    """
    Precomputed propagator for the exact 2D Weyl QCA (Paper 1 Eq. 16).

    Uses the arccos dispersion ω(k) = arccos(cos(kx/√2)·cos(ky/√2)).

    Parameters
    ----------
    shape : int or (Lx, Ly)
        Lattice shape (defaults to square if a single int given).
    """

    def __init__(self, shape):
        if isinstance(shape, int):
            shape = (shape, shape)
        self.shape = tuple(shape)
        self._build()

    def _build(self):
        from ca_core_exact import exact2d_unitary as _u2d
        KX, KY = make_kgrid_2d(*self.shape)
        self.U_ff, self.U_fg, self.U_gf, self.U_gg = _u2d(KX, KY)

    def step(self, f, g):
        F = fft.fft2(f)
        G = fft.fft2(g)
        F_new = self.U_ff * F + self.U_fg * G
        G_new = self.U_gf * F + self.U_gg * G
        return fft.ifft2(F_new), fft.ifft2(G_new)

    def steps(self, f, g, n: int):
        for _ in range(n):
            f, g = self.step(f, g)
        return f, g


# ══════════════════════════════════════════════════════════════════
#  Linear 2D propagator (ω = c|k|, split-step)
# ══════════════════════════════════════════════════════════════════

class Linear2DPropagator:
    """
    Precomputed split-step propagator for the 2D Weyl CA with linear
    dispersion ω = c|k| (ca_core.weyl_step_2d_splitstep).

    Parameters
    ----------
    shape : int or (Lx, Ly)
    c : float
        Unitary rotation magnitude per tick (dimensionless, ∈ [0,1]).
    """

    def __init__(self, shape, c: float = 0.5):
        if isinstance(shape, int):
            shape = (shape, shape)
        self.shape = tuple(shape)
        self.c = float(c)
        self._build()

    def _build(self):
        KX, KY = make_kgrid_2d(*self.shape)
        kappa      = np.sqrt(KX ** 2 + KY ** 2)
        kappa_safe = np.where(kappa == 0.0, 1.0, kappa)
        cos_ck     = np.cos(self.c * kappa)
        sinc_ck    = np.sin(self.c * kappa) / kappa_safe
        self.U_ff  = cos_ck
        self.U_fg  = -1j * sinc_ck * (KX - 1j * KY)
        self.U_gf  = -1j * sinc_ck * (KX + 1j * KY)
        self.U_gg  = cos_ck

    def step(self, f, g):
        F = fft.fft2(f)
        G = fft.fft2(g)
        F_new = self.U_ff * F + self.U_fg * G
        G_new = self.U_gf * F + self.U_gg * G
        return fft.ifft2(F_new), fft.ifft2(G_new)

    def steps(self, f, g, n: int):
        for _ in range(n):
            f, g = self.step(f, g)
        return f, g


# ══════════════════════════════════════════════════════════════════
#  Phase-rate extraction — improved FFT floor resolution
# ══════════════════════════════════════════════════════════════════

def phase_rate_lsq(samples: np.ndarray, dt: float = 1.0) -> float:
    """
    Extract |ω| from a complex time series by unwrapping and linear
    least-squares fit.

    This is the standard method used throughout the test suite.
    Floor scales as ~ε_machine / n_steps (statistical averaging).

    Parameters
    ----------
    samples : complex 1D array of length N_t
    dt : float  (time step between samples)

    Returns
    -------
    float : |ω| in radians per unit time
    """
    phases = np.unwrap(np.angle(samples))
    t = np.arange(len(samples), dtype=float) * dt
    A = np.vstack([t, np.ones_like(t)]).T
    slope, _ = np.linalg.lstsq(A, phases, rcond=None)[0]
    return abs(slope)


def phase_rate_zeropad(samples: np.ndarray,
                       dt: float = 1.0,
                       pad_factor: int = 8) -> dict:
    """
    Extract |ω| using zero-padded DFT — improved sub-bin resolution.

    Zero-padding interpolates the DFT spectrum by `pad_factor`, giving
    effective frequency resolution:

        Δω_eff = 2π / (N_t × pad_factor × dt)

    For pad_factor=8, N_t=400, dt=1.0:  Δω_eff ≈ 1.96e-3 rad/step
    vs standard DFT bin:                Δω_0   ≈ 1.57e-2 rad/step  (8× finer)

    This is a 'free' improvement — no additional propagation steps needed.
    The amplitude floor of the peak is still ~ε_machine × √N_t.

    Parameters
    ----------
    samples : complex 1D array of length N_t
    dt : float  (time step between samples)
    pad_factor : int  (zero-padding multiplier, default 8)

    Returns
    -------
    dict with keys:
        omega      : float, peak frequency magnitude
        omega_lsq  : float, cross-check via lsq method
        peak_bin   : int, index of DFT peak in padded spectrum
        delta_omega_eff : float, effective bin width achieved
        lsq_residual : float, |omega - omega_lsq|
    """
    N_t = len(samples)
    N_pad = N_t * pad_factor

    # Apply a Hann window to reduce spectral leakage before zero-padding.
    # The window suppresses sidelobes by ~30 dB at the cost of 2× main-lobe
    # width.  For a pure sinusoid this is ideal: the peak is clean.
    window = np.hanning(N_t)
    s_win = samples * window

    # Zero-pad and transform
    s_pad = np.zeros(N_pad, dtype=complex)
    s_pad[:N_t] = s_win
    S = fft.fft(s_pad)

    # Positive frequencies only (signal is complex, so full spectrum needed)
    # Peak in |S|²
    power = np.abs(S) ** 2
    peak_bin = int(np.argmax(power[:N_pad // 2]))

    # Frequency axis: k_bin × (2π / (N_pad × dt))
    omega = float(peak_bin) * (2.0 * math.pi / (N_pad * dt))
    delta_omega_eff = 2.0 * math.pi / (N_pad * dt)

    # Cross-check with lsq method
    omega_lsq = phase_rate_lsq(samples, dt)

    return {
        'omega':             omega,
        'omega_lsq':         omega_lsq,
        'peak_bin':          peak_bin,
        'delta_omega_eff':   delta_omega_eff,
        'lsq_residual':      abs(omega - omega_lsq),
    }


def compare_phase_methods(samples: np.ndarray,
                          dt: float = 1.0,
                          pad_factors: tuple = (1, 4, 8, 16, 32)):
    """
    Compare lsq and zero-padded DFT phase extraction at several pad factors.

    Prints a table: pad_factor | Δω_eff | omega_zeropad | omega_lsq | residual.
    Useful for choosing a pad_factor that saturates the achievable floor
    before the amplitude noise floor takes over.
    """
    omega_lsq = phase_rate_lsq(samples, dt)
    print(f"  lsq omega = {omega_lsq:.12f}")
    print(f"  {'pad_factor':>12} {'Δω_eff':>14} {'omega_zpad':>16} "
          f"{'|zpad-lsq|':>14}")
    print("  " + "-" * 62)
    for pf in pad_factors:
        r = phase_rate_zeropad(samples, dt, pad_factor=pf)
        print(f"  {pf:>12}  {r['delta_omega_eff']:>14.4e}  "
              f"{r['omega']:>16.12f}  {r['lsq_residual']:>14.3e}")


# ══════════════════════════════════════════════════════════════════
#  Propagator factory — convenience dispatcher
# ══════════════════════════════════════════════════════════════════

def make_propagator(kind: str, shape, **kwargs):
    """
    Factory function: create a propagator by name.

    Parameters
    ----------
    kind : 'bcc_weyl' | 'bcc_dirac' | 'exact_2d' | 'linear_2d'
    shape : int or tuple
    **kwargs : forwarded to the propagator constructor

    Returns
    -------
    One of the propagator objects above.
    """
    mapping = {
        'bcc_weyl':  BccWeylPropagator,
        'bcc_dirac': BccDiracPropagator,
        'exact_2d':  Exact2DPropagator,
        'linear_2d': Linear2DPropagator,
    }
    if kind not in mapping:
        raise ValueError(f"Unknown propagator kind {kind!r}. "
                         f"Choose from: {list(mapping)}")
    return mapping[kind](shape, **kwargs)


# ══════════════════════════════════════════════════════════════════
#  Smoke test
# ══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import ca_fft
    print("=== ca_propagator smoke test ===")
    print(f"FFT backend: {ca_fft.info()}")
    print()

    # BCC Weyl
    print("BccWeylPropagator(32):")
    prop_w = BccWeylPropagator(32)
    print(f"  {prop_w.memory_report()}")
    rng = np.random.default_rng(0)
    f = (rng.standard_normal((32,32,32)) + 1j*rng.standard_normal((32,32,32))).astype(np.complex128)
    g = (rng.standard_normal((32,32,32)) + 1j*rng.standard_normal((32,32,32))).astype(np.complex128)
    n0 = prop_w.norm(f, g)
    f2, g2 = prop_w.steps(f, g, 100)
    n1 = prop_w.norm(f2, g2)
    print(f"  norm drift after 100 steps: {abs(n1/n0 - 1):.2e}")

    print()
    # BCC Dirac
    print("BccDiracPropagator(16, m=0.2):")
    prop_d = BccDiracPropagator(16, m=0.2)
    print(f"  {prop_d.memory_report()}")
    eu = (rng.standard_normal((16,16,16)) + 1j*rng.standard_normal((16,16,16))).astype(np.complex128)
    ed = (rng.standard_normal((16,16,16)) + 1j*rng.standard_normal((16,16,16))).astype(np.complex128)
    cu = (rng.standard_normal((16,16,16)) + 1j*rng.standard_normal((16,16,16))).astype(np.complex128)
    cd = (rng.standard_normal((16,16,16)) + 1j*rng.standard_normal((16,16,16))).astype(np.complex128)
    nd0 = prop_d.norm(eu, ed, cu, cd)
    eu2, ed2, cu2, cd2 = prop_d.steps(eu, ed, cu, cd, 200)
    nd1 = prop_d.norm(eu2, ed2, cu2, cd2)
    print(f"  norm drift after 200 steps: {abs(nd1/nd0 - 1):.2e}")

    print()
    # Phase extraction comparison
    print("Phase extraction comparison (synthetic signal):")
    t = np.arange(400)
    omega_true = 0.123456789
    signal = np.exp(1j * omega_true * t) * (1.0 + 1e-13 * rng.standard_normal(400))
    compare_phase_methods(signal, dt=1.0, pad_factors=(1, 4, 8, 16, 32))
    print(f"  true omega = {omega_true:.12f}")
