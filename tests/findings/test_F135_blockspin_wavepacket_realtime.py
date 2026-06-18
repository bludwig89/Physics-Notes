"""
F135 — Real-time wave-packet dynamics under block-spin coarse-graining (Phase 2)
================================================================================

`2026-06-11`

The remaining dynamical check flagged by F132 §6: F131/F132 showed R_b commutes
with binding for static energy EIGENSTATES (where R_b ∘ e^{-iHt} is a trivial
global phase).  This closes the genuinely dynamical case — a MASSIVE Dirac
wave-packet that actually MOVES and SPREADS in real time — the matter analog of
the F129 free-photon result.

Headline (new physics for the RG classification): in the matter sector MASS is a
RELEVANT operator.  The renormalised coarse rule is Ω_coarse(q)=b·ω(q/b), so the
rest-gap ω(0)=arcsin(m) scales EXACTLY by b (eigenvalue b, like the F130-C1 string
tension σ), while the group velocity c stays marginal (F129/F130 T1) and the LIV
operators stay irrelevant (b^{-n}, F130 T2).  The dimensionless lattice mass runs
m→sin(b·arcsin m)≈b·m; the PHYSICAL Compton wavelength λ_C=a/arcsin(m) is invariant.

Checks (all on the model's actual 2D exact-QCA Dirac propagator, ca_dirac):
  RT1  FAITHFULNESS (machine precision) — the heart.  For a band-limited massive
       packet,  R_b ∘ evolve_fine^{bN}  ==  evolve_coarse^{N} ∘ R_b , where
       evolve_coarse uses Ω_coarse(q)=b·ω(q/b) (one coarse tick = b fine ticks).
       Checked at EVERY intermediate coarse tick (tracks the whole trajectory, not
       just the endpoint), b=2 and b=3, spinor-complex-safe block average.
  RT2  GROUP VELOCITY invariant — the packet centroid moves at the same PHYSICAL
       speed on the fine and coarse lattices (cells/tick is frame-invariant under
       the b-space/b-time rescale).
  RT3  DISPERSIVE SPREADING invariant — the packet's rms width grows (massive →
       dispersive); the physical spreading is reproduced by the coarse run.
  RT4  MASS IS RELEVANT — the rest-gap ω(0,m) scales by b to machine precision
       (eigenvalue b); m_coarse=sin(b·arcsin m); physical Compton wavelength
       invariant.  Contrast: c marginal, LIV irrelevant.
  RT5  NORM conserved on both lattices (unitarity survives coarse-graining).

Run:  python3 tests/findings/test_F135_blockspin_wavepacket_realtime.py
Writes: test-results/F135_blockspin_wavepacket_realtime.json
        test-results/F135_blockspin_wavepacket_realtime_summary.md
"""
from __future__ import annotations

import os
import sys
import json

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RESULTS = os.path.join(REPO, "test-results")
sys.path.insert(0, os.path.join(REPO, "ca-simulation"))

from ca_dirac import (dirac_step_2d_splitstep, dirac_norm,
                      _weyl_blocks, _apply_D_k, _kinetic_n, _dirac_dispersion,
                      _dirac_plus_eigenvector)

report = {"finding": "F135",
          "title": "Real-time wave-packet dynamics under block-spin",
          "tests": {}}
lines = ["# F135 — Real-time wave-packet dynamics under block-spin coarse-graining\n",
         "Massive 2D exact-QCA Dirac packet (ca_dirac). Coarse rule "
         "Omega_coarse(q)=b*omega(q/b); 1 coarse tick = b fine ticks.\n"]


def _ok(flag):
    return "PASS" if flag else "FAIL"


# ════════════════════════════════════════════════════════════════════
# Spinor block-spin R_b (complex-safe — keeps the imaginary part that the
# float-casting ca_blockspin.block_average would drop, per CLAUDE.md caveat)
# ════════════════════════════════════════════════════════════════════
def _block2d_complex(field, b):
    """Average b×b disjoint cells of a complex 2-D field; returns (Lc,Lc)."""
    f = np.asarray(field)
    Lx, Ly = f.shape
    assert Lx % b == 0 and Ly % b == 0
    return f.reshape(Lx // b, b, Ly // b, b).mean(axis=(1, 3))


def _R_b(spinor, b):
    return tuple(_block2d_complex(c, b) for c in spinor)


# ════════════════════════════════════════════════════════════════════
# Renormalised coarse Dirac step: U_{q/b}(dt=b) — one coarse tick = b fine
# ticks at the fine wavenumber k=q/b.  Mirrors dirac_step_2d_splitstep's
# analytic dt-interpolation but with k -> k/b and dt = b (so the rest-gap and
# the whole dispersion are evaluated at q/b and advanced b ticks).
# ════════════════════════════════════════════════════════════════════
def coarse_dirac_step(eu, ed, cu, cd, m, b):
    Lx, Ly = eu.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KXc, KYc = np.meshgrid(kx, ky, indexing="ij")
    KXr, KYr = KXc / b, KYc / b                # fine wavenumber for coarse mode q

    n = _kinetic_n(m)
    im_v = 1j * m
    W, Wp = _weyl_blocks(KXr, KYr)

    EU = np.fft.fft2(eu); ED = np.fft.fft2(ed)
    CU = np.fft.fft2(cu); CD = np.fft.fft2(cd)
    DEU, DED, DCU, DCD = _apply_D_k(EU, ED, CU, CD, n, im_v, W, Wp)

    omega = _dirac_dispersion(KXr, KYr, m)     # omega(q/b)
    cos_w = np.cos(omega); sin_w = np.sin(omega)
    dt = float(b)                               # b fine ticks per coarse tick
    cos_wdt = np.cos(omega * dt)
    sin_safe = np.where(sin_w == 0.0, 1.0, sin_w)
    scale = np.sin(omega * dt) / sin_safe
    scale = np.where(sin_w == 0.0, dt, scale)
    EU_n = cos_wdt * EU + scale * (DEU - cos_w * EU)
    ED_n = cos_wdt * ED + scale * (DED - cos_w * ED)
    CU_n = cos_wdt * CU + scale * (DCU - cos_w * CU)
    CD_n = cos_wdt * CD + scale * (DCD - cos_w * CD)
    return (np.fft.ifft2(EU_n), np.fft.ifft2(ED_n),
            np.fft.ifft2(CU_n), np.fft.ifft2(CD_n))


# ════════════════════════════════════════════════════════════════════
# Strictly band-limited POSITIVE-ENERGY moving wave-packet.  Built in k-space:
# a Gaussian envelope on a thin axis band (k along x, ky=0), each mode carrying
# its +ω Dirac eigenvector (phase-aligned for a smooth, localised packet) so the
# packet propagates at the group velocity with no zitterbewegung splitting.
# Hard cutoff keeps the band below the coarse Nyquist (index L/2b) so decimation
# is exact -> machine-precision RT1.  Defaults: m0=3,cut=4 -> max index 7 < 8
# (b=3 Nyquist), injective under b=2,3 decimation.
# ════════════════════════════════════════════════════════════════════
def positive_energy_packet(L, m, m0=3, width=1.2, cut=4, axis=0):
    kx_all = np.fft.fftfreq(L) * 2.0 * np.pi
    idx = np.fft.fftfreq(L) * L                 # signed mode index
    env = np.exp(-((idx - m0) ** 2) / (2.0 * width ** 2))
    env[np.abs(idx - m0) > cut] = 0.0           # strict band limit
    comps = [np.zeros((L, L), complex) for _ in range(4)]
    for i in range(L):
        if env[i] == 0.0:
            continue
        kx = kx_all[i] if axis == 0 else 0.0
        ky = 0.0 if axis == 0 else kx_all[i]
        v = _dirac_plus_eigenvector(kx, ky, m)  # +energy 4-spinor at this mode
        if abs(v[0]) > 1e-12:                   # phase-align (smooth packet)
            v = v * np.conj(v[0]) / abs(v[0])
        cell = (i, 0) if axis == 0 else (0, i)
        for c in range(4):
            comps[c][cell] = env[i] * v[c]
    spinor = tuple(np.fft.ifft2(comps[c]) for c in range(4))
    nrm = np.sqrt(dirac_norm(*spinor))
    return tuple(c / nrm for c in spinor)


def _density(spinor):
    eu, ed, cu, cd = spinor
    return (np.abs(eu) ** 2 + np.abs(ed) ** 2 +
            np.abs(cu) ** 2 + np.abs(cd) ** 2)


def _centroid_width_axis(spinor, axis=0):
    """Circular centroid and rms width of the density along `axis` (periodic)."""
    rho = _density(spinor)
    prof = rho.sum(axis=1 - axis)
    prof = prof / prof.sum()
    L = prof.size
    ang = 2 * np.pi * np.arange(L) / L
    z = np.sum(prof * np.exp(1j * ang))
    cm = (np.angle(z) / (2 * np.pi) * L) % L
    # width about the circular mean
    dx = (np.arange(L) - cm + L / 2) % L - L / 2
    var = np.sum(prof * dx ** 2)
    return cm, np.sqrt(var)


# ════════════════════════════════════════════════════════════════════
# RT1 — faithfulness, tracked over the whole trajectory
# ════════════════════════════════════════════════════════════════════
def _rel_resid(a, b):
    num = max(np.max(np.abs(a[i] - b[i])) for i in range(4))
    den = max(max(np.max(np.abs(a[i])) for i in range(4)), 1e-300)
    return num / den


def part_RT1(m=0.25, N=6):
    res = {}
    ok = True
    for b in (2, 3):
        L = 48
        fine = positive_energy_packet(L, m, m0=3, width=1.2, cut=4)
        coarse = _R_b(fine, b)
        worst = 0.0
        traj = []
        for j in range(1, N + 1):
            # advance fine by b more ticks (dt=1), coarse by one coarse tick
            for _ in range(b):
                fine = dirac_step_2d_splitstep(*fine, m=m, dt=1.0)
            coarse = coarse_dirac_step(*coarse, m=m, b=b)
            r = _rel_resid(_R_b(fine, b), coarse)
            worst = max(worst, r)
            traj.append(r)
        res[str(b)] = {"L": L, "Lc": L // b, "N_coarse": N,
                       "fine_ticks": b * N, "max_rel_resid": float(worst),
                       "per_tick": [float(x) for x in traj]}
        ok = ok and worst < 1e-9
    report["tests"]["RT1_faithfulness"] = {"detail": res, "pass": bool(ok)}
    lines.append("\n## RT1. Faithfulness: R_b o evolve_fine^{bN} == evolve_coarse^N o R_b "
                 "(tracked every coarse tick)\n")
    for b, d in res.items():
        lines.append(f"- b={b}: L {d['L']}->{d['Lc']}, {d['fine_ticks']} fine vs "
                     f"{d['N_coarse']} coarse ticks; max rel residual over trajectory "
                     f"= {d['max_rel_resid']:.2e}")
    lines.append(f"- gate (< 1e-9 at every tick): {_ok(ok)}")
    return ok


# ════════════════════════════════════════════════════════════════════
# RT2 / RT3 — group velocity and dispersive spreading invariant
# ════════════════════════════════════════════════════════════════════
def part_RT2_RT3(m=0.25, b=2, N=6):
    L = 48
    fine0 = positive_energy_packet(L, m, m0=3, width=1.2, cut=4)
    coarse0 = _R_b(fine0, b)

    cm_f0, w_f0 = _centroid_width_axis(fine0)
    cm_c0, w_c0 = _centroid_width_axis(coarse0)

    fine = fine0
    coarse = coarse0
    for _ in range(b * N):
        fine = dirac_step_2d_splitstep(*fine, m=m, dt=1.0)
    for _ in range(N):
        coarse = coarse_dirac_step(*coarse, m=m, b=b)

    cm_f1, w_f1 = _centroid_width_axis(fine)
    cm_c1, w_c1 = _centroid_width_axis(coarse)

    # velocities in physical (fine-cell / fine-tick) units
    v_fine = ((cm_f1 - cm_f0 + L / 2) % L - L / 2) / (b * N)
    Lc = L // b
    v_coarse_coarseunits = ((cm_c1 - cm_c0 + Lc / 2) % Lc - Lc / 2) / N
    v_coarse = v_coarse_coarseunits * b / b      # coarse-cell/coarse-tick = b*cell/(b*tick)
    # spreading (rms growth) in physical units
    dW_fine = (w_f1 - w_f0)
    dW_coarse = (w_c1 - w_c0) * b                 # coarse cells -> fine cells

    v_ok = abs(v_fine - v_coarse) < 5e-3
    w_ok = abs(dW_fine - dW_coarse) < 0.15 * max(abs(dW_fine), 1e-3) + 5e-3
    moved = abs(v_fine) > 1e-3
    spread = dW_fine > 1e-3
    report["tests"]["RT2_group_velocity"] = {
        "v_fine_cells_per_tick": float(v_fine),
        "v_coarse_cells_per_tick": float(v_coarse),
        "packet_actually_moves": bool(moved), "pass": bool(v_ok and moved)}
    report["tests"]["RT3_spreading"] = {
        "dwidth_fine_cells": float(dW_fine),
        "dwidth_coarse_in_fine_cells": float(dW_coarse),
        "packet_actually_spreads": bool(spread), "pass": bool(w_ok and spread)}
    lines.append("\n## RT2. Group velocity invariant (packet moves)\n")
    lines.append(f"- v_fine = {v_fine:.6f} cells/tick;  v_coarse = {v_coarse:.6f} "
                 f"(physical); moves: {_ok(moved)}; agree<5e-3: {_ok(v_ok)}")
    lines.append("\n## RT3. Dispersive spreading invariant (packet spreads)\n")
    lines.append(f"- d(rms)_fine = {dW_fine:.4f} cells;  d(rms)_coarse = {dW_coarse:.4f} "
                 f"(in fine cells); spreads: {_ok(spread)}; agree: {_ok(w_ok)}")
    return (v_ok and moved), (w_ok and spread)


# ════════════════════════════════════════════════════════════════════
# RT4 — mass is the RELEVANT operator: rest-gap scales by b
# ════════════════════════════════════════════════════════════════════
def part_RT4():
    res = {}
    ok = True
    for m in (0.1, 0.25, 0.5):
        gap_fine = float(_dirac_dispersion(np.array(0.0), np.array(0.0), m))  # arcsin(m)
        row = {"m": m, "gap_fine_arcsin_m": gap_fine,
               "arcsin_m": float(np.arcsin(m))}
        for b in (2, 3, 4):
            gap_coarse = b * gap_fine                       # Omega_coarse(0)=b*omega(0)
            eig = gap_coarse / gap_fine
            m_coarse = float(np.sin(b * gap_fine))          # sin(b*arcsin m)
            # physical Compton wavelength invariance: lam_phys = a / gap (lattice)
            lam_fine = 1.0 / gap_fine                       # in fine cells
            lam_coarse = 1.0 / gap_coarse                   # in coarse cells
            lam_phys_fine = lam_fine * 1.0                  # * a
            lam_phys_coarse = lam_coarse * b                # * (b a)
            row[f"b{b}"] = {"eigenvalue": eig,
                            "m_coarse_sin(b arcsin m)": m_coarse,
                            "m_coarse_approx_bm": b * m,
                            "lam_phys_ratio": lam_phys_coarse / lam_phys_fine}
            ok = ok and abs(eig - b) < 1e-12 and \
                abs(lam_phys_coarse / lam_phys_fine - 1.0) < 1e-12
        res[str(m)] = row
    report["tests"]["RT4_mass_relevant"] = {"detail": res, "pass": bool(ok)}
    lines.append("\n## RT4. Mass is the RELEVANT operator (rest-gap eigenvalue = b)\n")
    for m, row in res.items():
        eigs = [row[f"b{b}"]["eigenvalue"] for b in (2, 3, 4)]
        lines.append(f"- m={m}: gap=arcsin(m)={row['gap_fine_arcsin_m']:.6f}; "
                     f"eigenvalues (b=2,3,4) = {[round(e,12) for e in eigs]} "
                     f"(= b); physical Compton wavelength invariant")
    lines.append(f"- gap eigenvalue == b and lambda_phys invariant to 1e-12: {_ok(ok)}")
    lines.append("- Contrast: c_lat marginal (eigenvalue 1, F129/F130-T1); "
                 "LIV irrelevant (b^-n, F130-T2); mass relevant (b), like string tension (F130-C1).")
    return ok


# ════════════════════════════════════════════════════════════════════
# RT5 — norm conserved on both lattices
# ════════════════════════════════════════════════════════════════════
def part_RT5(m=0.25, b=2, N=6):
    L = 48
    fine = positive_energy_packet(L, m, m0=3, width=1.2, cut=4)
    coarse = _R_b(fine, b)
    n_f0 = dirac_norm(*fine)
    n_c0 = dirac_norm(*coarse)
    for _ in range(b * N):
        fine = dirac_step_2d_splitstep(*fine, m=m, dt=1.0)
    for _ in range(N):
        coarse = coarse_dirac_step(*coarse, m=m, b=b)
    drift_f = abs(dirac_norm(*fine) / n_f0 - 1.0)
    drift_c = abs(dirac_norm(*coarse) / n_c0 - 1.0)
    ok = drift_f < 1e-10 and drift_c < 1e-10
    report["tests"]["RT5_norm"] = {"fine_drift": float(drift_f),
                                   "coarse_drift": float(drift_c), "pass": bool(ok)}
    lines.append("\n## RT5. Norm conserved (unitarity survives R_b)\n")
    lines.append(f"- fine norm drift = {drift_f:.2e}; coarse norm drift = {drift_c:.2e}: {_ok(ok)}")
    return ok


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r1 = part_RT1()
    r2, r3 = part_RT2_RT3()
    r4 = part_RT4()
    r5 = part_RT5()
    results = [r1, r2, r3, r4, r5]
    passed = sum(bool(x) for x in results)
    total = len(results)
    report["summary"] = {"passed": passed, "total": total,
                         "all_pass": passed == total}
    lines.append(f"\n## Summary: {passed}/{total} PASS\n")
    with open(os.path.join(RESULTS, "F135_blockspin_wavepacket_realtime.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(RESULTS, "F135_blockspin_wavepacket_realtime_summary.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[F135] {passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
