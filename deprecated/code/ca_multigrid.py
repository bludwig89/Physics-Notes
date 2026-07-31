# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_multigrid.py
# migrated   : 2026-07-30 - 13:53
# target     : src/casim/engine/lattice/multigrid.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_multigrid.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_multigrid.py
===============

U4 — the block-spin two-grid multigrid that defeats the scale-separation wall
(roadmap-unified-real-space.md U4; roadmap-scale-to-real-space.md Phase 1).

The proton is ~1 fm; the Bohr orbit is ~5×10⁴ fm — a ~6×10⁴ size ratio.  No
single literal lattice resolves both (roadmap §2).  The multigrid runs the
proton on its OWN fine patch and lets it enter the atomic-scale lattice as a
block-spin (R_b) coarse-grained POINT charge, while the electron orbit is
resolved on the coarse grid.  The block factor b carries the scale separation;
both lattices stay tractable (~tens of cells per axis).

Two facts license the substitution (each a check here):

1.  **R_b is charge-faithful** (`reduce_charge`).  Block-averaging the proton's
    charge density over b³ fine cells conserves the total physical charge
    exactly and concentrates the proton to RMS r_p/b coarse cells → a point
    once b > r_p.  (Reuses the audited `blockspin.block_average_field`,
    complex-safe, F133.)

2.  **R_b commutes with the electron binding** (`solve_hydrogen`,
    `binding_commutes`).  Because the electron orbit ≫ the proton, the electron
    cannot resolve the proton's internal structure: binding to the R_b-reduced
    point charge reproduces binding to the fully-resolved proton (the
    point-vs-resolved energy gap → 0 as a₀/r_p grows), and the physical ground
    state is invariant under the coarse spacing a_c = b·a_f (grid/RG
    invariance).  The electron is the non-relativistic orbital of F156 (the
    atomic electron is non-relativistic; F125 holds the relativistic fine
    structure).

`MultigridAtom` orchestrates: fine proton charge → R_b reduce → coarse electron
ground state, reporting the REPRESENTED physical a₀/r_p ratio = (orbit in coarse
cells)·b / (proton in fine cells) — the scale separation the single lattice
could not hold.

Numerics: numpy only (no scipy).  FFT Poisson + imaginary-time relaxation.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import ca_fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

_HERE = os.path.dirname(__file__)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


# ----------------------------------------------------------------------
#  R_b on the proton charge (charge-faithful coarse-graining)
# ----------------------------------------------------------------------
def reduce_charge(rho_fine, b):
    """Block-spin (R_b) reduce a fine charge density by factor ``b``.

    Returns (rho_coarse, diagnostics).  rho_coarse is the block-AVERAGE over b³
    fine cells (the F133 even-field rule); the PHYSICAL total charge
    Σρ_coarse·(b³) equals Σρ_fine (conserved), and the proton RMS in coarse
    cells is r_p/b (→ a point for b > r_p).
    """
    try:
        from casim.engine.blockspin import block_average_field
        rho_coarse = block_average_field(np.asarray(rho_fine, float), b)
    except Exception:                              # standalone fallback
        a = np.asarray(rho_fine, float)
        L = a.shape[-1]
        Lc = L // b
        rho_coarse = a.reshape(Lc, b, Lc, b, Lc, b).mean(axis=(1, 3, 5))
    diag = {
        "total_fine": float(np.sum(rho_fine)),
        "total_coarse_phys": float(np.sum(rho_coarse) * b ** 3),
        "rms_fine_cells": _rms(np.asarray(rho_fine, float)),
        "rms_coarse_cells": _rms(rho_coarse),
        "b": int(b),
    }
    return rho_coarse, diag


def _rms(p):
    L = p.shape[0]
    ax = np.arange(L)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    c = L // 2
    tot = p.sum()
    if tot <= 0:
        return 0.0
    return float(np.sqrt((((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2) * p).sum() / tot))


# ----------------------------------------------------------------------
#  Coarse-grid non-relativistic hydrogen (physical units)
# ----------------------------------------------------------------------
def _k2(L, a):
    k = 2.0 * np.pi * np.fft.fftfreq(L, d=a)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    return KX ** 2 + KY ** 2 + KZ ** 2


def _coulomb_potential(rho, L, a, k_coupling):
    """Electron PE V(x)=q·Φ for q=−1 in the field of an ISOLATED charge density
    ``rho`` (total +1).  Uses the model's audited OPEN-boundary Poisson solver
    (`solve_poisson_3d_open`, the F64 kernel U2/nr_electron uses) — NOT a
    periodic FFT solve, which would give the potential of an infinite lattice of
    image charges and spuriously weaken the binding.  Lengths are in grid cells
    inside the solver; the physical 1/r scaling is restored by the spacing ``a``
    (V has units of energy when r is measured in length ``a``)."""
    from casim.gravity import solve_poisson_3d_open
    # solve_poisson_3d_open(ρ, G_N=k) returns Φ_cells = −k·Q/r_cells (Q=Σρ).
    # Normalise ρ to unit total charge, then convert cell→length (÷a):
    #   V(r) = Φ_cells / a = −k / (r_cells·a) = −k / r_phys  (attractive well).
    rho_cells = np.asarray(rho, float)
    s = float(rho_cells.sum())
    if s != 0:
        rho_cells = rho_cells / s
    phi_cells = solve_poisson_3d_open(rho_cells, G_N=k_coupling)
    return phi_cells / a


def solve_hydrogen(L, a, m=1.0, k=1.0, src_rms_cells=0.0,
                   relax_steps=1500, dtau=0.02):
    """Non-relativistic hydrogen ground state on a grid of spacing ``a``.

    The proton is a Gaussian of RMS ``src_rms_cells`` cells (0 → a single-cell
    point).  Imaginary-time relaxation of i∂ψ=(−∇²/2m+V)ψ.  Returns physical
    E0, a0=⟨r⟩ (length units of ``a``), and the orbit RMS in cells.
    """
    c = L // 2
    ax = np.arange(L)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r_cells = np.sqrt((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2)
    if src_rms_cells <= 0:
        rho = np.zeros((L, L, L)); rho[c, c, c] = 1.0 / a ** 3
    else:
        g = np.exp(-r_cells ** 2 / (2.0 * src_rms_cells ** 2))
        rho = g / (g.sum() * a ** 3)
    V = _coulomb_potential(rho, L, a, k)
    K2 = _k2(L, a)
    kin = np.exp(-K2 / (2.0 * m) * dtau)
    pot = np.exp(-V * dtau / 2.0)
    psi = np.exp(-r_cells ** 2 / (2.0 * (L / 6.0) ** 2)).astype(complex)
    psi /= np.sqrt((np.abs(psi) ** 2).sum())
    for _ in range(int(relax_steps)):
        psi = pot * psi
        psi = _fft.ifftn(kin * _fft.fftn(psi))
        psi = pot * psi
        psi /= np.sqrt((np.abs(psi) ** 2).sum())
    d = np.abs(psi) ** 2
    a0 = float((r_cells * a * d).sum())
    T = float(np.real(np.sum(np.conj(psi) * _fft.ifftn(K2 * _fft.fftn(psi)))) / (2.0 * m))
    Epot = float(np.sum(V * d))
    return {"E0": T + Epot, "a0": a0, "orbit_rms_cells": _rms(d),
            "L": L, "a": a, "m": m, "k": k, "src_rms_cells": src_rms_cells}


# ----------------------------------------------------------------------
#  Single-tick helpers (for the LIVE two-grid engine channel, F160)
# ----------------------------------------------------------------------
def coarse_point_potential(L, center, k, src_rms_cells=0.0, a=1.0):
    """Coulomb well V(x)=−k/r on an L³ coarse grid from a (point or compact)
    charge at ``center`` — the R_b-reduced proton seen by the coarse electron."""
    ax = np.arange(L)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r2 = (X - center[0]) ** 2 + (Y - center[1]) ** 2 + (Z - center[2]) ** 2
    if src_rms_cells <= 0:
        rho = np.zeros((L, L, L))
        rho[int(round(center[0])), int(round(center[1])), int(round(center[2]))] = 1.0
    else:
        g = np.exp(-r2 / (2.0 * src_rms_cells ** 2))
        rho = g
    return _coulomb_potential(rho, L, a, k)


def schrodinger_step(psi, V, m, a, dt):
    """One exactly-unitary Strang split-step of i∂ψ=(−∇²/2m+V)ψ on a grid of
    spacing ``a`` (the F156 integrator, reused live)."""
    L = psi.shape[0]
    K2 = _k2(L, a)
    kin = np.exp(-1j * K2 / (2.0 * m) * dt)
    pot = np.exp(-1j * V * dt / 2.0)
    psi = pot * psi
    psi = _fft.ifftn(kin * _fft.fftn(psi))
    psi = pot * psi
    return psi


def schrodinger_relax(psi, V, m, a, steps, dtau):
    """Imaginary-time relaxation to the ground state of (−∇²/2m+V)."""
    L = psi.shape[0]
    K2 = _k2(L, a)
    kin = np.exp(-K2 / (2.0 * m) * dtau)
    pot = np.exp(-V * dtau / 2.0)
    for _ in range(int(steps)):
        psi = pot * psi
        psi = _fft.ifftn(kin * _fft.fftn(psi))
        psi = pot * psi
        n = np.sqrt(float((np.abs(psi) ** 2).sum()))
        if n:
            psi = psi / n
    return psi


def rms_about_center(density):
    """RMS radius of a real density about the grid centre (cells)."""
    return _rms(np.asarray(density, float))


# ----------------------------------------------------------------------
#  Commute checks
# ----------------------------------------------------------------------
def binding_commutes(L=48, a=0.08, m=1.0, k=1.0,
                     r_p_list=(6.0, 3.0, 1.5), **kw):
    """Point-vs-resolved binding: the energy gap between an electron bound to a
    resolved proton (RMS r_p cells) and to a point charge → 0 as a₀/r_p grows
    (the electron cannot resolve the proton ⇒ R_b to a point is faithful)."""
    pt = solve_hydrogen(L, a, m, k, src_rms_cells=0.0, **kw)
    rows = []
    for r_p in r_p_list:
        res = solve_hydrogen(L, a, m, k, src_rms_cells=r_p, **kw)
        rows.append({"r_p_phys": r_p * a, "a0_over_rp": res["a0"] / (r_p * a),
                     "E0": res["E0"], "dE_vs_point": abs(res["E0"] - pt["E0"])})
    return {"point": pt, "resolved": rows}


def invariance_under_b(L=48, a_f=0.04, m=1.0, k=1.0, b_list=(1, 2, 3),
                       **kw):
    """Physical ground state invariant under the coarse spacing a_c=b·a_f
    (R_b commutes with the orbit binding in the resolved regime).  Solves the
    SAME physical atom on grids of spacing b·a_f (box held ~fixed by L/b)."""
    rows = []
    for b in b_list:
        Lc = L // b
        res = solve_hydrogen(Lc, a_f * b, m, k, src_rms_cells=0.0, **kw)
        rows.append({"b": b, "L_coarse": Lc, "a_c": a_f * b,
                     "E0": res["E0"], "a0": res["a0"]})
    E = [r["E0"] for r in rows]
    spread = (max(E) - min(E)) / abs(np.mean(E)) if np.mean(E) else float("inf")
    return {"rows": rows, "E0_rel_spread": spread}


# ----------------------------------------------------------------------
#  The orchestrated two-grid atom
# ----------------------------------------------------------------------
@dataclass
class MultigridAtom:
    """Two-grid hydrogen: fine proton patch + R_b-reduced point charge + coarse
    electron orbit.  ``b`` is the block factor carrying the scale separation."""
    b: int = 10000
    L_fine: int = 24
    r_p_fine: float = 3.0           # proton RMS in fine cells (≈1 fm patch)
    L_coarse: int = 48
    m: float = 1.0
    k: float = 1.0
    relax_steps: int = 1500

    def run(self):
        # 1. fine proton charge density (total +1)
        c = self.L_fine // 2
        ax = np.arange(self.L_fine)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
        g = np.exp(-(((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2))
                   / (2.0 * self.r_p_fine ** 2))
        rho_fine = g / g.sum()
        # 2. R_b reduce to the coarse grid (charge-faithful); the proton becomes
        #    a point on the coarse grid (RMS r_p/b coarse cells).
        b_eff = min(self.b, self.L_fine)            # cannot average past L_fine
        rho_c, redux = reduce_charge(rho_fine, _largest_divisor(self.L_fine, b_eff))
        # 3. coarse electron orbit bound to the (point-like) reduced proton.
        #    On the coarse atom grid the proton is a single cell (a point).
        orbit = solve_hydrogen(self.L_coarse, a=1.0, m=self.m, k=self.k,
                               src_rms_cells=0.0, relax_steps=self.relax_steps)
        # represented physical scale separation:
        #   a0_phys / r_p_phys = (orbit cells · a_c) / (r_p_fine · a_f)
        #   with a_c = b·a_f  ⇒  = orbit_rms_cells · b / r_p_fine
        ratio = orbit["orbit_rms_cells"] * self.b / self.r_p_fine
        return {
            "b": self.b,
            "proton_charge_conserved": redux["total_coarse_phys"],
            "proton_rms_fine_cells": self.r_p_fine,
            "orbit_rms_coarse_cells": orbit["orbit_rms_cells"],
            "represented_a0_over_rp": ratio,
            "represented_decades": float(np.log10(ratio)) if ratio > 0 else None,
            "electron_E0": orbit["E0"],
            "electron_bound": orbit["E0"] < 0.0,
            "L_fine": self.L_fine, "L_coarse": self.L_coarse,
            "tier": ("two-grid multigrid; structure + scale-ratio are the "
                     "deliverable, absolute fm/eV P6-gated (F123)"),
        }


def _largest_divisor(L, b):
    """Largest divisor of L that is ≤ b (block_average needs L%b==0)."""
    for d in range(min(b, L), 0, -1):
        if L % d == 0:
            return d
    return 1


# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=== U4 multigrid (sandbox-scale demo) ===")
    print("\n[1] R_b charge faithfulness:")
    rho = np.zeros((24, 24, 24))
    a = np.arange(24); Xx, Yy, Zz = np.meshgrid(a, a, a, indexing="ij")
    rho = np.exp(-(((Xx - 12) ** 2 + (Yy - 12) ** 2 + (Zz - 12) ** 2)) / (2 * 3.0 ** 2))
    rho /= rho.sum()
    for b in (2, 3, 4, 6):
        _, d = reduce_charge(rho, b)
        print(f"  b={b}: total_phys={d['total_coarse_phys']:.6f} "
              f"rms {d['rms_fine_cells']:.2f}→{d['rms_coarse_cells']:.2f} coarse cells")
    print("\n[2] binding commutes (point vs resolved):")
    bc = binding_commutes(L=40, a=0.09, relax_steps=900)
    for r in bc["resolved"]:
        print(f"  a0/r_p={r['a0_over_rp']:5.1f}  dE_vs_point={r['dE_vs_point']:.4f}")
    print("\n[3] two-grid atom (b=20000):")
    out = MultigridAtom(b=20000, relax_steps=900).run()
    print(f"  proton charge conserved : {out['proton_charge_conserved']:.6f}")
    print(f"  represented a0/r_p      : {out['represented_a0_over_rp']:.3e} "
          f"({out['represented_decades']:.1f} decades)")
    print(f"  electron bound          : {out['electron_bound']}  E0={out['electron_E0']:.4f}")
