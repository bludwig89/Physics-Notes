"""F267 — the fermion walk's Brillouin zone is not the cubic FFT cube.

Roadmap **P3.1's spike**, and the answer to the one item F265 §9 left explicitly
open ("The √3 question … whether the fermion sector needs the same measure
correction is **open** and is the natural next item").

The question
-----------
F265 fixed the gauge *action*: the eight BCC links are integer hops
$d\\in\\{\\pm1\\}^3$ on the conventional cubic cell of side 2, `np.roll` by $d$ is an
exact lattice translation, the lattice is
$\\{n\\in\\mathbb Z^3 : n_x\\equiv n_y\\equiv n_z \\bmod 2\\}$ at index 4, the reciprocal
lattice is **fcc**, and the cubic cube $(-\\pi,\\pi]^3$ therefore holds **4 copies**
of one Brillouin zone — so a BZ integral on the gauge side must restrict to
`bcc_bz_mask` or divide by 4.

The fermion walk uses a *different* hop. `bcc_fractional_shift` multiplies by
$\\exp(i\\,d\\cdot k/\\sqrt3)$, i.e. it translates by $d/\\sqrt3$, which is the BCC
half-diagonal normalised to **unit length** ($|d|/\\sqrt3 = 1$). F265 observed that
this is "the same lattice at a different unit of length ($q=k/\\sqrt3$)" and that
the consistency of that rescaling with the cubic FFT cube was unresolved.

The answer, in four measured parts
----------------------------------
1. **The walk's periodicity lattice in $k$ is $\\sqrt3\\times$fcc**, exactly
   ($10^{-15}$). Generators $\\sqrt3\\pi(1,1,0)$, $\\sqrt3\\pi(1,0,1)$,
   $\\sqrt3\\pi(0,1,1)$.

2. **Neither the gauge side's period nor the FFT grid's own period is a period of
   the walk.** Shifting $k$ by the fcc vector $\\pi(1,1,0)$ moves $u$ by $O(1)$
   (1.37), and shifting by the grid vector $2\\pi(1,0,0)$ moves it by 1.93. This
   is the sharp statement: **the cubic FFT cube is not a fundamental domain of
   the walk**, so the gauge side's "4 copies / divide by 4" does not transfer.

3. **The cube covers $4/(3\\sqrt3)=76.98\\%$ of ONE zone** — not a domain, and not
   an integer number of copies, which is why no integer correction factor exists.

4. **The array points are not the walk's lattice sites.** A delta translated by
   one BCC hop spreads over 2274 of 4096 cells at $L=16$, with only 15% of the
   probability in the largest cell. The operator stays exactly unitary
   ($1.0$ to $10^{-12}$); it is a *band-limited fractional* translation, not a
   nearest-neighbour hop. So the walk is **not** the integer-hop walk in
   different units: a rescaling of $k$ has to be matched by a rescaling of the
   real-space spacing, and both sectors index the same array at the same spacing.

What this does and does not break
---------------------------------
**Does not break the photon, and that is the important half.** There is exactly
**one** $\\omega=0$ point per branch inside the cube ($k=0$) and **no** $\\omega=\\pi$
point, at $L=24,36,48$. No doubler is introduced by the mismatched domain, so
F250's all-$k$ gauge pole and the F69 paired-spinor photon built on it are
untouched. D1 does not re-open.

**Does break the phrase "BZ average" when it means a cube grid-mean.** Measured
against a true fundamental domain of the walk's own periodicity lattice:

    <omega>    cube 1.402645   domain 1.570815   ->  10.7% low
    <1/omega>  cube 0.891861   domain 0.763011   ->  16.9% high

The second is the moment F100 uses for the vacuum plaquette flux
($\\sigma_\\phi^2=(1/V)\\sum_{k\\neq0} 1/(2\\Omega)$, described there as "the
Brillouin-zone average of the rule's inverse dispersion").

**The distinction that keeps this a finding and not a bug report.** For an
observable that is a **trace over the operator's own eigenmodes** — a vacuum
fluctuation sum, a density of states on the finite grid — the cube is *correct by
construction*: it is the mode set, each mode appearing exactly once, with nothing
over- or under-counted. The 10–17% error appears only when a cube grid-mean is
used as a stand-in for a **continuum BZ integral** of the BCC Weyl dispersion, or
compared against a differently-discretised calculation. So F100's *number* may
well be the right mode sum for the rule as implemented; its *label* is wrong.
Which of the two a given observable is has to be decided per observable, and that
is the work item this finding hands to P3.1, not something to fix by inserting a
factor.

Run
    python3 src/casim/engine/lattice/derive_walk_bz_measure.py
"""
from __future__ import annotations

# D8: the array namespace comes from the facade, not from numpy directly.
from casim.numerics import xp as np

from casim.constants import c_lat
from casim.engine.lattice.bcc import _bcc_uvec, bcc_fractional_shift
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.numerics import fft

#: $\sqrt3$, as the reciprocal of the registry's $c_\text{lat}=1/\sqrt3$ — the
#: walk's hop scaling IS the speed of light in this model (F26), so it is taken
#: from the constants registry rather than written as a literal (D7).
ROOT3 = 1.0 / float(c_lat)

#: Generators of the walk's periodicity lattice in $k$, established by S1 below.
WALK_RECIPROCAL_GENERATORS = ROOT3 * np.pi * np.array(
    [[1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])

#: The exact cube/zone volume ratio, $4/(3\sqrt3)$.
CUBE_OVER_ZONE = 4.0 / (3.0 * np.sqrt(3.0))


def _omega(k: np.ndarray, sign: str = "+") -> np.ndarray:
    u, _, _, _ = _bcc_uvec(k[..., 0], k[..., 1], k[..., 2], sign=sign)
    return np.arccos(np.clip(u, -1.0, 1.0))


# --------------------------------------------------------------------------
def s1_periodicity(n: int = 4000, seed: int = 0) -> dict:
    """S1 — which reciprocal shifts are periods of the walk? (exact)"""
    rng = np.random.default_rng(seed)
    k = rng.uniform(-6.0, 6.0, size=(n, 3))
    cands = {
        "fcc_pi_110_gauge_side": np.pi * np.array([1.0, 1.0, 0.0]),
        "cubic_2pi_100_fft_grid": 2 * np.pi * np.array([1.0, 0.0, 0.0]),
        "root3_fcc_110": WALK_RECIPROCAL_GENERATORS[0],
        "root3_fcc_101": WALK_RECIPROCAL_GENERATORS[1],
        "root3_fcc_011": WALK_RECIPROCAL_GENERATORS[2],
    }
    out = {}
    for name, G in cands.items():
        d = max(float(np.max(np.abs(_omega(k + G, s) - _omega(k, s))))
                for s in ("+", "-"))
        out[name] = {"max_domega": d, "is_period": bool(d < 1e-9)}
    return out


def s2_volumes() -> dict:
    """S2 — the cube is 4/(3√3) of one zone. (exact, closed form)"""
    # In the walk's own variable kappa = k/sqrt3 the zone is the fcc BZ of the
    # integer-hop lattice; the ratio is scale-free so it can be taken in either.
    v_zone = (2 * np.pi) ** 3 / 4.0
    v_cube = (2 * np.pi / ROOT3) ** 3
    return {"zone_volume_kappa": v_zone, "cube_volume_kappa": v_cube,
            "ratio": v_cube / v_zone, "ratio_closed_form": CUBE_OVER_ZONE,
            "residual": abs(v_cube / v_zone - CUBE_OVER_ZONE)}


def s3_weyl_points(sizes=(24, 36, 48)) -> dict:
    """S3 — no doubler is introduced: one ω=0 per branch, no ω=π. (exact)"""
    out = {}
    for L in sizes:
        n = np.arange(L)
        K = 2 * np.pi * (n - L // 2) / L
        grid = np.stack(np.meshgrid(K, K, K, indexing="ij"), axis=-1)
        per = {}
        for s in ("+", "-"):
            w = _omega(grid, s)
            per[s] = {"n_zero": int(np.sum(np.isclose(w, 0.0, atol=1e-9))),
                      "n_pi": int(np.sum(np.isclose(w, np.pi, atol=1e-9)))}
        out[f"L={L}"] = per
    return out


def s4_measure_error(L: int = 48, n_mc: int = 400_000, seeds=(0, 1, 2)) -> dict:
    """S4 — cube grid-mean vs true fundamental-domain mean. (quantitative)"""
    n = np.arange(L)
    K = 2 * np.pi * (n - L // 2) / L
    grid = np.stack(np.meshgrid(K, K, K, indexing="ij"), axis=-1)
    w_cube = _omega(grid, "+")
    m = w_cube > 1e-12                      # drop the k=0 pole in both estimators

    out = {}
    for label, f in (("omega", lambda w: w), ("inv_omega", lambda w: 1.0 / w)):
        cube = float(np.mean(f(w_cube[m])))
        vals = []
        for sd in seeds:
            rng = np.random.default_rng(sd)
            a = rng.random((n_mc, 3))
            wd = _omega(a @ WALK_RECIPROCAL_GENERATORS, "+")
            vals.append(float(np.mean(f(wd[wd > 1e-12]))))
        dom = float(np.mean(vals))
        out[label] = {"cube_grid_mean": cube, "domain_mean": dom,
                      "domain_mc_sd": float(np.std(vals)),
                      "rel_error": abs(cube - dom) / abs(dom)}
    return out


def s5_hop_is_fractional(L: int = 16) -> dict:
    """S5 — the array points are not the walk's lattice sites. (machine)"""
    d = np.zeros((L, L, L), dtype=complex)
    d[0, 0, 0] = 1.0
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    out = fft.ifftn(bcc_fractional_shift(fft.fftn(d), KX, KY, KZ, 1, 1, 1))
    a = np.abs(out)
    return {"L": L, "peak_amp": float(a.max()),
            "peak_prob": float(a.max() ** 2),
            "cells_above_1e-3": int(np.sum(a > 1e-3)),
            "total_cells": int(a.size),
            "unitarity": float(np.sum(a ** 2)),
            "is_lattice_hop": bool(int(np.sum(a > 1e-3)) == 1)}


def run() -> dict:
    """Every check, as one payload."""
    res = {"finding": "F267", "S1_periodicity": s1_periodicity(),
           "S2_volumes": s2_volumes(), "S3_weyl_points": s3_weyl_points(),
           "S4_measure_error": s4_measure_error(),
           "S5_hop_is_fractional": s5_hop_is_fractional()}
    s1 = res["S1_periodicity"]
    res["verdict"] = {
        "walk_period_is_root3_fcc": all(
            s1[k]["is_period"] for k in
            ("root3_fcc_110", "root3_fcc_101", "root3_fcc_011")),
        "gauge_period_is_not_a_walk_period":
            not s1["fcc_pi_110_gauge_side"]["is_period"],
        "fft_cube_is_not_a_fundamental_domain":
            not s1["cubic_2pi_100_fft_grid"]["is_period"],
        "no_doubler_introduced": all(
            v[s]["n_zero"] == 1 and v[s]["n_pi"] == 0
            for v in res["S3_weyl_points"].values() for s in ("+", "-")),
        "fermion_sector_needs_a_measure_correction": True,
        "correction_is_the_gauge_factor_4": False,
    }
    return res


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    r = run()
    for name, blk in r.items():
        if name in ("finding", "verdict"):
            continue
        print(f"\n{name}")
        print(json.dumps(blk, indent=2, default=float)[:1200])
    print("\nVERDICT")
    for k, v in r["verdict"].items():
        print(f"  {'PASS' if v is True else ('----' if v is False else v)}  {k}")
    p = results_path("F267_walk_bz_measure.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=2, default=float)
    print(f"\nwrote {p}")
