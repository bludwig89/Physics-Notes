#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────────
#  test_P0_dynamical_fermions.py
#
#  P0 of roadmap-matter-binding.md — certify the electron and the up / down
#  quarks as DYNAMICAL objects: measured, non-dispersing, correctly-charged
#  real-time wavepackets on the BCC lattice.
#
#  This is certification of existing machinery (ca_dirac_bcc, ca_bcc,
#  ca_strong, ca_charged_current), not new physics.  It is the foundation
#  P1–P5 rest on.
#
#  Parts
#  -----
#   A  Dispersion / group velocity   (e, u, d as Dirac/Weyl wavepackets)
#   B  Norm conservation (unitarity) over a long real-time run
#   C  Zitterbewegung frequency  ω_Z = 2·arcsin(m)
#   D  Charges  Q = T3 + Y/2  exact over ℚ  (e → −1, u → +2/3, d → −1/3)
#   E  Quark colour-triplet structure  (SU(3) covariance + colour-charge
#      conservation under real-time propagation)
#
#  Dimensionless lattice masses used below are REPRESENTATIVE test values
#  (O(0.05–0.4)), chosen to exercise the dynamics across the mass range and
#  to honour the F40 d>u splitting (r_d/r_u ≈ 4).  The PHYSICAL m_lat values
#  are ~1e-22 (F83) and are a P6 (scale-fixing) concern, not a P0 one.
# ──────────────────────────────────────────────────────────────────────────
import sys
import os
import json
import time
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_bcc as bcc                      # noqa: E402
import ca_dirac_bcc as cdb                # noqa: E402
import ca_strong as cs                    # noqa: E402
import ca_charged_current as ccur         # noqa: E402
from ca_lattice import make_kgrid_3d      # noqa: E402

# Representative dimensionless lattice masses (see header note).
M_E = 0.05          # electron — light
M_U = 0.10          # up
M_D = 0.40          # down  (≈ 4× up, F40 splitting)

ROOT3 = np.sqrt(3.0)
results = {}
checks = []   # (name, residual, target, passed)


def record(name, residual, target, passed):
    checks.append(dict(name=name, residual=float(residual),
                       target=float(target), passed=bool(passed)))


# ══════════════════════════════════════════════════════════════════════════
#  Helpers — narrow-band 3D BCC wavepacket
# ══════════════════════════════════════════════════════════════════════════
def weyl_packet_3d(L, k0, sigma_x=4.0, center=None, helicity='+',
                   transverse_uniform=False):
    """
    Build a Gaussian wavepacket centred on lattice momentum k0, projected
    onto the BCC Weyl +helicity eigenstate AT EVERY k (via the k-space
    helicity projector P₊(k) = (I + n̂(k)·σ)/2), so the packet is a clean
    single-branch state with no −branch contamination.

    transverse_uniform=True makes the envelope depend on x only (uniform in
    y,z) ⇒ every mode has k_y=k_z=0, so ω=k_x/√3 is *exactly* linear and the
    packet translates rigidly at the on-axis group velocity c_lat=1/√3 with
    no transverse-spread bias.  (A full 3D Gaussian has k_y,k_z spread and a
    genuinely lower packet-averaged v_x — real physics, not an artefact.)

    Returns (f, g) complex arrays of shape (L, L, L).
    """
    if center is None:
        center = (L // 2, L // 2, L // 2)
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x - center[0], x - center[1], x - center[2],
                          indexing='ij')
    if transverse_uniform:
        env = np.exp(-(X**2) / (2.0 * sigma_x**2))
    else:
        env = np.exp(-(X**2 + Y**2 + Z**2) / (2.0 * sigma_x**2))
    carrier = np.exp(1j * (k0[0] * X + k0[1] * Y + k0[2] * Z))
    scalar = (env * carrier).astype(np.complex128)

    # Project onto the +helicity eigenstate at EVERY Fourier mode.
    S = np.fft.fftn(scalar)
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    nhat = bcc.bcc_spin_axis(KX, KY, KZ, sign=helicity)   # (3, L, L, L)
    nx, ny, nz = nhat[0], nhat[1], nhat[2]
    # +eigenvector of (n̂·σ) ∝ first column of P₊ = ((1+n_z)/2, (n_x+i n_y)/2).
    # NORMALISE per-k so the projection preserves the k-space envelope (an
    # un-normalised projector reweights modes by √((1+n_z)/2) and shifts the
    # packet's effective central momentum → biased group velocity).
    ef = (1.0 + nz) / 2.0
    eg = (nx + 1j * ny) / 2.0
    nrm = np.sqrt(np.abs(ef)**2 + np.abs(eg)**2)
    nrm = np.where(nrm > 1e-12, nrm, 1.0)
    F = S * ef / nrm
    G = S * eg / nrm
    return np.fft.ifftn(F), np.fft.ifftn(G)


def centroid_x_circular(field_list):
    """
    Torus-aware (circular-mean) centroid along x of |Ψ|² — immune to the
    packet wrapping the periodic boundary.  Returns x̄ ∈ [0, L).
    """
    rho = sum(np.abs(f)**2 for f in field_list)
    L = rho.shape[0]
    profile = rho.sum(axis=(1, 2))
    ang = np.angle((profile * np.exp(2j * np.pi * np.arange(L) / L)).sum())
    return (ang * L / (2 * np.pi)) % L


def circular_disp(x1, x0, L):
    """Signed displacement x1−x0 wrapped into (−L/2, L/2]."""
    d = (x1 - x0) % L
    if d > L / 2:
        d -= L
    return d


# ══════════════════════════════════════════════════════════════════════════
#  PART A — dispersion / group velocity
# ══════════════════════════════════════════════════════════════════════════
def part_A():
    print("\n[A] dispersion + group velocity")

    # A1 — exact ω(k): eigenphase of D_k vs analytic arccos, for e/u/d masses.
    for tag, m in (('e', M_E), ('u', M_U), ('d', M_D)):
        err = cdb.verify_dirac_dispersion_3d_bcc(L=16, n_modes=16, m=m, seed=3)
        ok = err < 1e-12
        record(f"A1-disp-{tag}", err, 1e-12, ok)
        print(f"  A1 {tag}: |ω_meas-ω_ana| max = {err:.2e}  {'PASS' if ok else 'FAIL'}")

    # A2 — group velocity of a real-time Weyl packet (massless limit) vs the
    #      analytic ∂ω/∂k.  A clean single-branch packet translates rigidly at
    #      v_g; we measure the centroid drift along the propagation axis.
    L = 48
    k0mag = 0.45
    khat = np.array([1.0, 0.0, 0.0])           # along a cube axis (LV-free dir)
    k0 = k0mag * khat
    f, g = weyl_packet_3d(L, k0, sigma_x=5.0, helicity='+',
                          transverse_uniform=True)
    n_steps = 25
    x0 = centroid_x_circular([f, g])
    for _ in range(n_steps):
        f, g = bcc.weyl_step_3d_bcc(f, g, sign='+')
    x1 = centroid_x_circular([f, g])
    v_meas = circular_disp(x1, x0, L) / n_steps   # cells per tick along x

    # Analytic group velocity ∂ω/∂k_x at k0 (central finite difference).
    eps = 1e-4
    wp = float(bcc.bcc_dispersion(k0[0] + eps, k0[1], k0[2], sign='+'))
    wm = float(bcc.bcc_dispersion(k0[0] - eps, k0[1], k0[2], sign='+'))
    v_ana = (wp - wm) / (2 * eps)
    rel = abs(v_meas - v_ana) / abs(v_ana)
    ok = rel < 5e-3                            # rigid translation; centroid floor
    record("A2-groupvel-weyl", rel, 2e-2, ok)
    print(f"  A2 v_g: measured {v_meas:.5f}  analytic {v_ana:.5f}  "
          f"(c_lat=1/√3={1/ROOT3:.5f})  rel={rel:.2e}  {'PASS' if ok else 'FAIL'}")
    results['A2'] = dict(v_meas=v_meas, v_ana=v_ana, c_lat=1/ROOT3, rel=rel)


# ══════════════════════════════════════════════════════════════════════════
#  PART B — norm conservation (unitarity) over a long real-time run
# ══════════════════════════════════════════════════════════════════════════
def part_B():
    print("\n[B] norm conservation over 1000 ticks")
    for tag, m in (('e', M_E), ('u', M_U), ('d', M_D)):
        drift = abs(cdb.norm_drift_3d_bcc(L=20, n_steps=1000, m=m, seed=1))
        ok = drift < 1e-10
        record(f"B-norm-{tag}", drift, 1e-10, ok)
        print(f"  B {tag} (m={m}): |norm(1000)/norm(0)-1| = {drift:.2e}  "
              f"{'PASS' if ok else 'FAIL'}")
        results[f'B_{tag}'] = drift


# ══════════════════════════════════════════════════════════════════════════
#  PART C — zitterbewegung  ω_Z = 2·arcsin(m)
# ══════════════════════════════════════════════════════════════════════════
def part_C():
    print("\n[C] zitterbewegung frequency ω_Z = 2·arcsin(m)")
    # A rest packet (uniform field = pure k=0) prepared as a chirality
    # eigenstate (η only) is NOT an energy eigenstate: at k=0 the D_k off-
    # diagonal i·m mixes η↔χ with eigenphases ±arcsin(m), so the chirality
    # population oscillates at the difference 2·arcsin(m).
    for tag, m in (('e', M_E), ('u', M_U), ('d', M_D)):
        L = 4
        eu = np.ones((L, L, L), dtype=np.complex128)   # η_↑ = 1 everywhere (k=0)
        ed = np.zeros((L, L, L), dtype=np.complex128)
        cu = np.zeros((L, L, L), dtype=np.complex128)
        cd = np.zeros((L, L, L), dtype=np.complex128)
        dt = 0.25
        n_steps = 2000
        sig = np.empty(n_steps)
        for t in range(n_steps):
            # chirality signal: left-handed probability fraction
            nL = np.abs(eu)**2 + np.abs(ed)**2
            nR = np.abs(cu)**2 + np.abs(cd)**2
            sig[t] = float((nL - nR).sum() / (nL + nR).sum())
            eu, ed, cu, cd = cdb.dirac_step_3d_bcc_splitstep(
                eu, ed, cu, cd, m=m, dt=dt)
        sig = sig - sig.mean()
        # Hann window → clean main lobe so quadratic peak interpolation is
        # accurate for a pure-tone (two-level) zitter signal at any frequency.
        win = np.hanning(n_steps)
        spec = np.abs(np.fft.rfft(sig * win))
        dw = 2 * np.pi / (n_steps * dt)                      # angular bin width
        i = 1 + int(np.argmax(spec[1:]))
        # Parabolic (quadratic) interpolation of the peak for sub-bin accuracy.
        if 1 <= i < len(spec) - 1:
            a, b, c = spec[i - 1], spec[i], spec[i + 1]
            denom = (a - 2 * b + c)
            delta = 0.5 * (a - c) / denom if denom != 0 else 0.0
        else:
            delta = 0.0
        w_meas = (i + delta) * dw
        w_ana = 2.0 * np.arcsin(m)
        rel = abs(w_meas - w_ana) / w_ana
        ok = rel < 2e-3                                       # sub-bin interp
        record(f"C-zitter-{tag}", rel, 5e-3, ok)
        print(f"  C {tag}: ω_Z measured {w_meas:.5f}  analytic {w_ana:.5f}  "
              f"rel={rel:.2e}  {'PASS' if ok else 'FAIL'}")
        results[f'C_{tag}'] = dict(w_meas=w_meas, w_ana=w_ana, rel=rel)


# ══════════════════════════════════════════════════════════════════════════
#  PART D — charges  Q = T3 + Y/2  exact over ℚ
# ══════════════════════════════════════════════════════════════════════════
def part_D():
    print("\n[D] charges  Q = T3 + Y/2  (exact ℚ)")
    expected = {'e': Fraction(-1), 'u': Fraction(2, 3), 'd': Fraction(-1, 3)}
    for sp in ('e', 'u', 'd'):
        Q = ccur.charge(sp)
        qn = ccur.QUANTUM_NUMBERS[sp]
        ok = (Q == expected[sp])
        # residual is exactly 0 for a correct rational; encode as 0.0/1.0
        record(f"D-charge-{sp}", 0.0 if ok else 1.0, 0.0, ok)
        print(f"  D {sp}: T3={qn['T3']}  Y={qn['Y']}  Q={Q}  "
              f"(expected {expected[sp]})  {'PASS' if ok else 'FAIL'}")
        results[f'D_{sp}'] = dict(T3=str(qn['T3']), Y=str(qn['Y']), Q=str(Q))


# ══════════════════════════════════════════════════════════════════════════
#  PART E — quark colour triplet:  SU(3) covariance + colour-charge
#           conservation under real-time propagation
# ══════════════════════════════════════════════════════════════════════════
def part_E():
    print("\n[E] quark colour-triplet structure")
    L = 24
    shape = (L, L)
    rng = np.random.default_rng(7)

    # E1 — colour charge conserved under propagation (cold links).
    q = cs.gaussian_quark(shape, flavour='u', colour='r', sigma=4.0)
    # seed all three colours so the SU(3) charge vector is non-trivial
    qd = cs.gaussian_quark(shape, flavour='d', colour='g', sigma=4.0)
    for key, val in qd.items():
        q[key] = q[key] + val
    U_cold = cs.cold_links_2d(shape)
    Q0 = cs.noether_charge_total(q)
    qp = q
    for _ in range(20):
        qp = cs.step_strong_2d(qp, U_cold, m_flavour={'u': M_U, 'd': M_D, 's': 0.0})
    Q1 = cs.noether_charge_total(qp)
    dQ = float(np.max(np.abs(Q1 - Q0)))
    ok = dQ < 1e-10
    record("E1-colour-charge-conserved", dQ, 1e-10, ok)
    print(f"  E1 colour charge drift (20 ticks): {dQ:.2e}  {'PASS' if ok else 'FAIL'}")

    # E2 — SU(3) colour covariance: under a LOCAL rotation V(x) the colour
    #      charge DENSITY rotates in the adjoint at each site, so its pointwise
    #      magnitude Σ_a J^a_0(x)² is invariant cell-by-cell.  (The *total*
    #      charge is only globally invariant, so the right covariance test is
    #      pointwise on the density.)
    Vfield = np.empty((L, L, 3, 3), dtype=complex)
    for i in range(L):
        for j in range(L):
            Vfield[i, j] = cs.su3_haar(rng)
    q_rot = cs.gauge_transform_quark(q, Vfield)
    cas_before = np.sum(cs.noether_charge_density(q)**2, axis=0)      # (L,L)
    cas_after = np.sum(cs.noether_charge_density(q_rot)**2, axis=0)   # (L,L)
    rel = float(np.max(np.abs(cas_after - cas_before)) /
                (np.max(np.abs(cas_before)) + 1e-300))
    ok = rel < 1e-12
    record("E2-su3-density-casimir-invariant", rel, 1e-12, ok)
    print(f"  E2 pointwise SU(3) density Casimir invariance: rel={rel:.2e}  "
          f"{'PASS' if ok else 'FAIL'}")

    # E3 — quark norm conservation under real-time propagation.
    n0 = cs.quark_norm(q)
    qp = q
    for _ in range(50):
        qp = cs.step_strong_2d(qp, U_cold, m_flavour={'u': M_U, 'd': M_D, 's': 0.0})
    n1 = cs.quark_norm(qp)
    drift = abs(n1 / n0 - 1.0)
    ok = drift < 1e-10
    record("E3-quark-norm-conserved", drift, 1e-10, ok)
    print(f"  E3 quark norm drift (50 ticks): {drift:.2e}  {'PASS' if ok else 'FAIL'}")


# ══════════════════════════════════════════════════════════════════════════
def main():
    t0 = time.time()
    print("=" * 70)
    print("P0 — dynamical electron / up / down certification")
    print("=" * 70)
    part_A()
    part_B()
    part_C()
    part_D()
    part_E()

    n_pass = sum(c['passed'] for c in checks)
    n_tot = len(checks)
    dt = time.time() - t0
    print("\n" + "=" * 70)
    print(f"P0 RESULT: {n_pass}/{n_tot} PASS  in {dt:.1f}s")
    print("=" * 70)

    out = dict(suite="P0_dynamical_fermions",
               n_pass=n_pass, n_total=n_tot, seconds=dt,
               masses=dict(e=M_E, u=M_U, d=M_D),
               checks=checks, results=results)
    here = os.path.dirname(__file__)
    dest = os.path.join(here, '..', 'test-results', 'P0_dynamical_fermions.json')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w') as fh:
        json.dump(out, fh, indent=2)
    print(f"results → {os.path.relpath(dest)}")
    return 0 if n_pass == n_tot else 1


if __name__ == '__main__':
    sys.exit(main())
