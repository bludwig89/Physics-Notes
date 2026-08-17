"""F135 — Real-space confinement (U1): the proton holds together as a
scalar-confined three-body bound state.

roadmap-unified-real-space.md, U1.  Closes F134's U1 null (the linearised
gluon does not confine).  The derived fix: confinement is the F86/F70
**string** — a Lorentz-SCALAR linear potential (position-dependent Dirac mass
m_eff(x)=m+σ|x−R|, the MIT-bag / dual-superconductor mechanism, = F86 ε_c→0 ⇒
∞ effective mass in the vacuum) — which BINDS even a light fermion, whereas a
**vector** (time-component) potential of the same shape Klein-tunnels and does
NOT bind.

  K1  kernel: dirac_step_3d_bcc_varm reduces to the constant-m step
      bit-for-bit on a uniform field; norm conserved to machine precision
  S1  scalar confinement BINDS: a three-body cluster RMS radius stays
      bounded/plateaus, while the free control disperses to box saturation
  V1  vector confinement does NOT bind (Klein): vector-mode RMS ≈ free
  N1  every constituent norm conserved to machine precision throughout

Runs under pytest, or standalone:
    PYTHONPATH=src python tests/findings/test_F135_realspace_confinement.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "src"))

import casim  # noqa: E402,F401
from casim.engine import Simulation, LatticeSpec  # noqa: E402
from casim.engine.core.channel import build_channel  # noqa: E402

L = 16
P = ["q1", "q2", "q3"]
_IDX = np.indices((L, L, L))


# ----------------------------------------------------------------------
# K1 — the variable-mass kernel itself
# ----------------------------------------------------------------------
def test_K1_varm_kernel_reduction_and_unitarity():
    from casim.engine.particles import dirac_bcc as db
    rng = np.random.default_rng(0)

    def rnd():
        return (rng.standard_normal((L, L, L))
                + 1j * rng.standard_normal((L, L, L)))
    eu, ed, xu, xd = rnd(), rnd(), rnd(), rnd()
    m0 = 0.3
    a = db.dirac_step_3d_bcc_varm_splitstep(
        eu, ed, xu, xd, m_field=np.full((L, L, L), m0), m0=m0)
    b = db.dirac_step_3d_bcc_splitstep(eu, ed, xu, xd, m=m0)
    assert max(np.max(np.abs(x - y)) for x, y in zip(a, b)) == 0.0
    # norm conservation under a strong linear scalar well over 100 steps
    r = np.sqrt(sum(((_IDX[k] - 8) ** 2) for k in range(3)))
    mfield = 0.05 + 0.25 * r

    def packet():
        rr = sum(((_IDX[k] - 8) ** 2) for k in range(3))
        p = np.exp(-rr / (2 * 1.5 ** 2)).astype(complex)
        return p / np.sqrt((np.abs(p) ** 2).sum())
    e = packet()
    z = np.zeros_like(e)
    s = (e, z.copy(), z.copy(), z.copy())
    n0 = sum(np.sum(np.abs(c) ** 2) for c in s)
    for _ in range(100):
        s = db.dirac_step_3d_bcc_varm_splitstep(*s, m_field=mfield, m0=0.05)
    n1 = sum(np.sum(np.abs(c) ** 2) for c in s)
    assert abs(n1 - n0) / n0 < 1e-12


# ----------------------------------------------------------------------
# engine helpers
# ----------------------------------------------------------------------
def _cons(name, center, sigma, mode):
    cfg = {"type": "particle", "name": name, "species": "nu_e_L",
           "mass": 0.9, "init": {"center": list(center), "width": 1.3},
           "couplings": {}}
    if sigma > 0:
        cfg["confine"] = {"sigma": sigma, "dt": 0.5, "mode": mode,
                          "anchor": "com", "partners": P}
    return cfg


def _cluster_rms(sim):
    d = sum(np.asarray(sim.channels[n].density_field(sim.states[n]))
            for n in P)
    tot = float(d.sum())
    c = [float((d.sum(axis=tuple(j for j in range(3) if j != k))
                * np.arange(L)).sum() / tot) for k in range(3)]
    r2 = sum(((_IDX[k] - c[k] + L / 2.0) % L - L / 2.0) ** 2 for k in range(3))
    return float(np.sqrt(float((d * r2).sum()) / tot))


def _run(sigma, mode="scalar", ticks=150):
    ch = [build_channel(_cons("q1", (7, 8, 8), sigma, mode)),
          build_channel(_cons("q2", (9, 8, 8), sigma, mode)),
          build_channel(_cons("q3", (8, 10, 8), sigma, mode))]
    sim = Simulation(LatticeSpec(L=L, topology="bcc",
                                 c_lat=0.5773502691896258),
                     ch, observers=[], seed=11)
    n0 = {n: sim.channels[n].energy(sim.states[n]) for n in P}
    rmax = _cluster_rms(sim)
    series = [_cluster_rms(sim)]
    for _ in range(ticks):
        sim.step(1)
        rmax = max(rmax, _cluster_rms(sim))
        series.append(_cluster_rms(sim))
    drift = max(abs(sim.channels[n].energy(sim.states[n]) - n0[n]) / n0[n]
                for n in P)
    return {"first": series[0], "last": series[-1], "max": rmax,
            "drift": drift}


def test_S1_scalar_confinement_binds_vs_free():
    conf = _run(0.5, "scalar")
    free = _run(0.0, "scalar")
    # confined cluster stays bounded (plateau well below the box scale)…
    assert conf["max"] < 5.0, f"confined cluster not bounded: {conf['max']:.2f}"
    # …while the free cluster disperses toward box saturation
    assert free["last"] > 6.0, f"free cluster did not disperse: {free['last']:.2f}"
    # clear separation
    assert conf["last"] < 0.65 * free["last"]
    # N1 — norms machine-precision in the binding run
    assert conf["drift"] < 1e-10 and free["drift"] < 1e-10


def test_V1_vector_confinement_does_not_bind():
    """A vector (phase-kick) potential of the same σ Klein-tunnels: it does
    not bind — vector-mode dispersal matches the free control."""
    vec = _run(0.5, "vector")
    free = _run(0.0, "scalar")
    assert vec["last"] > 6.0, f"vector unexpectedly bound: {vec['last']:.2f}"
    assert abs(vec["last"] - free["last"]) / free["last"] < 0.15


if __name__ == "__main__":
    test_K1_varm_kernel_reduction_and_unitarity()
    print("K1  PASS — varm kernel: uniform==constant-m bit-for-bit, unitary")
    test_S1_scalar_confinement_binds_vs_free()
    print("S1  PASS — scalar confinement binds (bounded cluster vs free dispersal)")
    test_V1_vector_confinement_does_not_bind()
    print("V1  PASS — vector confinement Klein-tunnels (no binding)")
    print("F135 3/3 PASS")
