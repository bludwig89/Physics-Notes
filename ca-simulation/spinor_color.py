"""
spinor_color.py  —  Bloch-sphere → RGB coloring for spinor fields
==================================================================

A 2-component spinor ψ = (f, g) ∈ ℂ², up to overall phase and overall
amplitude, defines a point on ℂP¹ ≅ S² (the Bloch sphere).  This module
maps that point to a color so a single 2D heatmap shows spinor orientation,
not just |ψ|².

Mapping
-------
    θ = 2·arctan(|g|/|f|)          ∈ [0, π]    (polar angle on S²)
    φ = arg(g) − arg(f)            ∈ [−π, π]   (azimuthal phase)

    hue        ← φ (mapped to [0, 1])
    lightness  ← (1 + cos θ) / 2  (north pole bright, south pole dark)
    saturation ← clip(|ψ|² / peak, 0, 1)

A cell with f-only is "north-pole bright" (left helicity in our convention).
A cell with g-only is "south-pole dark".  Mixed states pick up a hue from
their relative phase.

This is for the 2-component Weyl spinor.  For Dirac (4-component) use two
side-by-side panels: one for the η (left) chirality, one for χ (right).
"""

import numpy as np
import colorsys


def spinor_to_rgb(f, g, peak=None):
    """
    Map a 2-component spinor field (f, g) to RGB.

    Parameters
    ----------
    f, g : complex ndarrays of the same shape
        Upper and lower spinor components.
    peak : float or None
        Normalization for |ψ|² saturation.  If None, uses the global max.

    Returns
    -------
    rgb : ndarray with shape (..., 3), values in [0, 1]
    """
    f = np.asarray(f, dtype=complex)
    g = np.asarray(g, dtype=complex)

    abs_f = np.abs(f)
    abs_g = np.abs(g)
    density = abs_f**2 + abs_g**2

    # θ ∈ [0, π]:  pure f → θ=0, pure g → θ=π
    # Use atan2 to avoid division by zero
    theta = 2.0 * np.arctan2(abs_g, abs_f)

    # φ ∈ [-π, π]:  relative phase
    # When either component is exactly zero, atan2(0,0) = 0; that's fine.
    phi = np.angle(g) - np.angle(f)
    # Wrap to [0, 2π) for hue
    hue = (phi % (2.0 * np.pi)) / (2.0 * np.pi)

    # Lightness from cos θ.  Map to [0.15, 0.85] to keep both poles visible.
    lightness = 0.15 + 0.7 * (1.0 + np.cos(theta)) / 2.0

    # Saturation from density
    if peak is None:
        peak = density.max() if density.max() > 0 else 1.0
    saturation = np.clip(density / peak, 0.0, 1.0) ** 0.5  # sqrt for better visual

    # Vectorized HSL → RGB
    rgb = _hls_to_rgb_vec(hue, lightness, saturation)
    return rgb


def _hls_to_rgb_vec(h, l, s):
    """Vectorized HLS → RGB.  h, l, s are arrays in [0,1]."""
    # Use the standard formula
    def _f(n, h, l, s):
        k = (n + h * 12.0) % 12.0
        a = s * np.minimum(l, 1.0 - l)
        return l - a * np.clip(np.minimum(k - 3.0, 9.0 - k), -1.0, 1.0)

    r = _f(0, h, l, s)
    g = _f(8, h, l, s)
    b = _f(4, h, l, s)
    return np.stack([r, g, b], axis=-1)


def make_bloch_legend(size=128):
    """
    Render a (size × size) RGB legend showing the Bloch hue/lightness wheel.

    Each pixel corresponds to a point on the Bloch sphere stereographically
    projected to the unit disk.  Outside the disk is white.
    """
    xs = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    r = np.sqrt(X**2 + Y**2)
    mask = r <= 1.0

    # Stereographic projection: r=0 ↔ north pole (θ=0), r=1 ↔ south pole (θ=π)
    theta = 2.0 * np.arctan(r)          # r=0 → θ=0; r=1 → θ=π/2; need different mapping
    # Use r ↦ θ = π·r so that r=1 maps to south pole
    theta = np.pi * r
    phi = np.arctan2(Y, X)

    f = np.cos(theta / 2.0)
    g = np.sin(theta / 2.0) * np.exp(1j * phi)
    rgb = spinor_to_rgb(f, g)

    # Mask outside disk
    rgb = np.where(mask[..., None], rgb, 1.0)
    return rgb
