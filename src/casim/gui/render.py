"""casim.gui.render — pure (numpy-only) rendering helpers for the point cloud.

No vispy/Qt import here, so this is unit-testable headless.  The vispy/Qt app
(``casim.gui.app``) consumes these.
"""
from __future__ import annotations

from typing import Tuple
import numpy as np

# Colour control points (density low → high), RGB in [0,1].
_STOPS = np.array([
    [0x00, 0x00, 0x10],
    [0x0a, 0x0a, 0xff],
    [0x00, 0xdd, 0xff],
    [0xff, 0xaa, 0x00],
    [0xff, 0xff, 0xff],
], dtype=np.float64) / 255.0


def density_to_rgba(values: np.ndarray, vmax: float) -> np.ndarray:
    """Map density values → RGBA (float32), brighter+more opaque = denser."""
    values = np.asarray(values, dtype=np.float64).ravel()
    if vmax < 1e-12 or values.size == 0:
        return np.zeros((values.size, 4), dtype=np.float32)
    t = np.clip(values / vmax, 0.0, 1.0)
    n = len(_STOPS) - 1
    pos = t * n
    lo = np.clip(np.floor(pos).astype(int), 0, n - 1)
    frac = (pos - lo)[:, None]
    rgb = _STOPS[lo] * (1 - frac) + _STOPS[lo + 1] * frac
    rgba = np.empty((values.size, 4), dtype=np.float32)
    rgba[:, :3] = rgb
    rgba[:, 3] = np.clip(np.sqrt(t), 0.1, 1.0)
    return rgba


def bloch_rgb(f: np.ndarray, g: np.ndarray, amp: np.ndarray | None = None,
              vmax: float | None = None) -> np.ndarray:
    """Bloch-sphere colouring of a 2-spinor (f, g) → RGBA (float32).

    Mirrors ``ca-simulation/spinor_color.py``: a spinor ψ=(f,g) up to overall
    phase/amplitude is a point on ℂP¹≅S² (the Bloch sphere), mapped to colour so
    *orientation* and *phase* are visible rather than just |ψ|².

        θ = 2·atan2(|g|, |f|)  ∈ [0,π]   polar angle (helicity): f-pole vs g-pole
        φ = arg(g) − arg(f)    ∈ [−π,π]  relative phase

        hue        ← φ        (full colour wheel)
        lightness  ← cos θ    (f-pole bright, g-pole dark; mid-grey for mixed)
        saturation ← 1        (orientation always reads as a hue)
        opacity    ← √(amp/vmax)  amplitude, so faint sites stay faint

    ``amp`` defaults to the spinor density |f|²+|g|²; ``vmax`` to its max.  All
    inputs are flattened together, so pass the values at the *selected* voxels.
    Pure numpy (no colorsys), so this stays headless-testable.
    """
    f = np.asarray(f, dtype=complex).ravel()
    g = np.asarray(g, dtype=complex).ravel()
    if f.size == 0:
        return np.zeros((0, 4), dtype=np.float32)
    abs_f, abs_g = np.abs(f), np.abs(g)
    theta = 2.0 * np.arctan2(abs_g, abs_f)            # [0, π]
    phi = np.angle(g) - np.angle(f)                   # [-π, π]
    hue = (phi % (2.0 * np.pi)) / (2.0 * np.pi)       # [0, 1)
    # lightness in [0.12, 0.88] so both poles stay visible
    lightness = 0.5 + 0.38 * np.cos(theta)
    sat = np.ones_like(hue)
    rgb = _hls_to_rgb(hue, lightness, sat)
    if amp is None:
        amp = abs_f ** 2 + abs_g ** 2
    else:
        amp = np.asarray(amp, dtype=np.float64).ravel()
    if vmax is None:
        vmax = float(amp.max()) if amp.size else 0.0
    rgba = np.empty((f.size, 4), dtype=np.float32)
    rgba[:, :3] = rgb
    if vmax < 1e-12:
        rgba[:, 3] = 0.1
    else:
        rgba[:, 3] = np.clip(np.sqrt(np.clip(amp / vmax, 0.0, 1.0)), 0.1, 1.0)
    return rgba


def _hls_to_rgb(h: np.ndarray, l: np.ndarray, s: np.ndarray) -> np.ndarray:
    """Vectorised HLS→RGB (arrays in [0,1]); returns (N,3) float64."""
    def chan(n):
        k = (n + h * 12.0) % 12.0
        a = s * np.minimum(l, 1.0 - l)
        return l - a * np.clip(np.minimum(k - 3.0, 9.0 - k), -1.0, 1.0)
    return np.stack([chan(0.0), chan(8.0), chan(4.0)], axis=-1)


def point_cloud_spinor(f_vol: np.ndarray, g_vol: np.ndarray,
                       pctile: float) -> Tuple[np.ndarray, np.ndarray, float, float]:
    """Spinor (f,g) volumes → (coords, Bloch RGBA, max density, total density).

    Voxel *selection* uses the same density-percentile cut as ``point_cloud`` —
    you still draw only active regions — but the *colour* carries Bloch
    orientation (helicity) and relative phase instead of a density ramp.
    ``f_vol``/``g_vol`` are (L,L,L) complex arrays (the channel's ``f``/``g``).
    """
    f_vol = np.asarray(f_vol)
    g_vol = np.asarray(g_vol)
    density = np.abs(f_vol) ** 2 + np.abs(g_vol) ** 2
    density = np.asarray(density.real if np.iscomplexobj(density) else density)
    flat = density.ravel()
    if flat.size > 2 ** 22:
        stride = max(1, flat.size // 2 ** 21)
        threshold = np.percentile(flat[::stride], pctile)
    else:
        threshold = np.percentile(flat, pctile)
    mask = density > threshold
    coords = np.argwhere(mask).astype(np.float32)
    dmax = float(density.max()) if density.size else 0.0
    colours = bloch_rgb(f_vol[mask], g_vol[mask], amp=density[mask], vmax=dmax)
    return coords, colours, dmax, float(density.sum())


#: distinct per-channel tints (RGB in [0,1]) for overlaid field clouds.
CHANNEL_TINTS = [
    (0.25, 0.65, 1.00),   # blue
    (1.00, 0.55, 0.10),   # orange
    (0.30, 1.00, 0.45),   # green
    (1.00, 0.30, 0.55),   # pink
    (0.95, 0.90, 0.20),   # yellow
    (0.70, 0.45, 1.00),   # violet
    (0.20, 1.00, 0.90),   # teal
    (1.00, 0.85, 0.60),   # sand
]


def tinted_rgba(values: np.ndarray, vmax: float, tint) -> np.ndarray:
    """Channel-hued density ramp: dark → tint → white-hot; denser = more opaque.

    Used when several field clouds overlay the same lattice, so each channel
    stays identifiable by hue while peak density still reads white."""
    values = np.asarray(values, dtype=np.float64).ravel()
    if vmax < 1e-12 or values.size == 0:
        return np.zeros((values.size, 4), dtype=np.float32)
    t = np.clip(values / vmax, 0.0, 1.0)[:, None]
    tint = np.asarray(tint, dtype=np.float64)[None, :]
    rgb = tint * (0.25 + 0.75 * t)
    rgb = rgb + (1.0 - rgb) * t ** 4          # white-hot peak
    rgba = np.empty((values.size, 4), dtype=np.float32)
    rgba[:, :3] = rgb
    rgba[:, 3] = np.clip(np.sqrt(t[:, 0]), 0.1, 1.0)
    return rgba


def point_cloud(volume: np.ndarray, pctile: float,
                tint=None) -> Tuple[np.ndarray, np.ndarray, float, float]:
    """Voxels above the ``pctile`` density threshold → (coords, colours, max, sum).

    ``coords`` is (M,3) float32 lattice indices; ``colours`` is (M,4) float32.
    ``tint`` selects the per-channel hued ramp (overlay mode); ``None`` keeps
    the classic multi-stop colormap.  On large lattices (> 2^22 voxels) the
    percentile threshold is estimated on a strided sample — the threshold is a
    visual cut, not a physics quantity, so the approximation is safe.
    """
    density = np.asarray(volume)
    if np.iscomplexobj(density):
        density = density.real
    density = np.abs(density)
    flat = density.ravel()
    if flat.size > 2 ** 22:
        stride = max(1, flat.size // 2 ** 21)
        threshold = np.percentile(flat[::stride], pctile)
    else:
        threshold = np.percentile(flat, pctile)
    mask = density > threshold
    coords = np.argwhere(mask).astype(np.float32)
    values = density[mask]
    dmax = float(density.max()) if density.size else 0.0
    colours = (tinted_rgba(values, dmax, tint) if tint is not None
               else density_to_rgba(values, dmax))
    return coords, colours, dmax, float(density.sum())


def lattice_medium(L: int, topology: str = "cubic",
                   max_points: int = 40_000) -> Tuple[np.ndarray, np.ndarray, int]:
    """Static substrate cloud: the lattice sites the scenario runs on.

    Renders the medium itself as faint points.  An integer stride subsamples
    the sites so the cloud never exceeds ``max_points`` regardless of L (the
    resource guard — a 512³ lattice is shown as a sparse skeleton, not 134M
    points).  BCC adds the body-centred sublattice at half-stride offsets.
    Returns ``(coords (M,3) float32, colours (M,4) float32, stride)``.
    """
    sublattices = 2 if topology == "bcc" else 1
    budget = max(1, max_points // sublattices)
    stride = 1
    while (-(-L // stride)) ** 3 > budget:   # ceil(L/stride)³ points
        stride += 1
    ax = np.arange(0, L, stride, dtype=np.float32)
    g = np.stack(np.meshgrid(ax, ax, ax, indexing="ij"), axis=-1).reshape(-1, 3)
    parts = [g]
    if sublattices == 2:
        parts.append(g + stride / 2.0)      # body-centre sublattice
    coords = np.concatenate(parts, axis=0)
    colours = np.tile(np.array([[0.45, 0.55, 0.75, 0.10]], dtype=np.float32),
                      (len(coords), 1))
    return coords, colours, stride
