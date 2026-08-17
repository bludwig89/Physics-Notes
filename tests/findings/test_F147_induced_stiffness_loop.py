"""
F147 — the induced gauge-stiffness one-loop on the BCC walk
(the F138 induced-Y-kinetic-term loop; the dynamical half of F141's U2).

Checks (module: src/casim/engine/particles/induced_stiffness.py):

  L1  hop decomposition A(q) = Σ_d e^{i d·q} C_d exact (both branches)
  L2  parity theorem ω(q+Q) = π−ω(q), n(q+Q) = −n(q) (from F51 S1)
  L3  circle perturbation theory: δ²Ω_n/δε² = Σ_m |K_nm|² cot((Ω_n−Ω_m)/2)
      for U(ε) = e^{iεK}U₀ — validated on a random unitary
  L4  Ward: two-tick gauging exactly gauge-invariant (both channels);
      one-tick staggered gauge invariance FAILS (the asymmetry is physics:
      hypercharge gauge structure exists only stroboscopically, F51 §3)
  L5  spectral closures of the GAUGED walk at strong field (ε=0.3):
      λ → −λ  ({P,W_A}=0, any A)  and  λ → −λ̄  (θ → π−θ)
  L6  one-tick rigidity: the filled one-tick sea has EXACTLY zero static
      response in BOTH channels (E constant mod quantized 2π cut-crossings)
      ⟹ no induced kinetic term for any gauge channel at one-tick level
  L7  channel-equality theorem, pointwise: |M_stag| = |M_vec| and equal
      circle gaps on dense grids (two-tick sea), face + diagonal q̃
  L8  channel equality in the FULL response (brute-force dense gauged W₂,
      paramagnetic + diamagnetic): χ_stag = χ_vec at L=6 and L=8
  L9  exact rational bookkeeping: equal per-charge quanta + bare charges
      (q_P = ±1, T₃ = ±1/2) ⟹ t² = g'²/g² = 1/4, sin²θ_W(free) = 1/5;
      F49 target 2/7 differs by exactly 8/7 (the content factor left open)

Runtime ~40 s (dense 2L³ eig at L=8 dominates).
"""

import json
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.particles import induced_stiffness as cis  # noqa: E402

RESULTS = os.path.normpath(
    os.path.join(HERE, "..", "..", "test-results", "F147_induced_stiffness_loop.json"))

results = {"finding": "F147", "checks": {}}
failures = []


def check(name, ok, detail):
    results["checks"][name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures.append(name)


EH, QD = [0, 1, 0], [1, 0, 0]

# L1 — hop decomposition
r_p = cis.hop_decomposition_residual('+')
r_m = cis.hop_decomposition_residual('-')
check("L1_hop_decomposition", max(r_p, r_m) < 5e-15,
      f"max residual +: {r_p:.2e}, −: {r_m:.2e} (8 harmonics, A0=0)")

# L2 — parity theorem
rw, rn = cis.parity_theorem_residual('+')
check("L2_parity_theorem", max(rw, rn) < 5e-15,
      f"omega(q+Q)=pi−omega: {rw:.2e}; n(q+Q)=−n: {rn:.2e}")

# L3 — circle PT kernel on a random unitary
rng = np.random.default_rng(7)
n = 8
Z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
Qm, R = np.linalg.qr(Z)
U0 = Qm @ np.diag(np.diag(R) / np.abs(np.diag(R)))
lam, V = np.linalg.eig(U0)
Om = -np.angle(lam)
K = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
K = (K + K.conj().T) / 2
Kv = V.conj().T @ K @ V
w_eig, P = np.linalg.eigh(K)
eps = 1e-4
def _phases(e):
    lam_e = np.linalg.eigvals((P * np.exp(1j * e * w_eig)) @ P.conj().T @ U0)
    return np.sort(-np.angle(lam_e))
d2 = (_phases(eps) + _phases(-eps) - 2 * np.sort(Om)) / eps ** 2
order = np.argsort(Om)
pred = np.array([sum(abs(Kv[nn, m]) ** 2 / np.tan((Om[nn] - Om[m]) / 2)
                     for m in range(n) if m != nn) for nn in order])
r3 = float(np.max(np.abs(d2 / pred - 1.0)))
check("L3_circle_pt_kernel", r3 < 1e-4,
      f"cot(dOm/2) kernel, unit prefactor: max |ratio−1| = {r3:.2e}")

# L4 — Ward identities
w_s2 = cis.gauge_invariance_residual(channel='staggered', sea='two-tick')
w_v2 = cis.gauge_invariance_residual(channel='vector', sea='two-tick')
w_s1 = cis.gauge_invariance_residual(channel='staggered', sea='one-tick')
check("L4a_ward_two_tick", max(w_s2, w_v2) < 1e-13,
      f"two-tick pure-gauge E-invariance: stag {w_s2:.2e}, vec {w_v2:.2e} (exact telescoping)")
check("L4b_ward_one_tick_fails", w_s1 > 1e-3,
      f"one-tick staggered gauge invariance fails by {w_s1:.2e} — "
      f"hypercharge gauge structure is stroboscopic-only (F51)")

# L5 — spectral closures of the gauged walk at strong field
C = cis.hop_matrices('+')
L5 = 6
N5 = L5 ** 3
coords = np.array([(x, y, z) for x in range(L5) for y in range(L5) for z in range(L5)])
idx = {tuple(c): i for i, c in enumerate(coords)}
qt5 = (2 * np.pi / L5) * np.array(QD, dtype=float)
W = np.zeros((2 * N5, 2 * N5), dtype=complex)
for d, Cd in C.items():
    dv = np.array(d)
    tgt = (coords + dv) % L5
    a = 0.3 * np.cos((coords + 0.5 * dv) @ qt5) * float(np.array(d, dtype=float) @ np.array(EH, dtype=float))
    rows = np.array([idx[tuple(t)] for t in tgt])
    for i in range(N5):
        W[2 * rows[i]:2 * rows[i] + 2, 2 * i:2 * i + 2] += np.exp(1j * a[i]) * Cd
lam5 = np.linalg.eigvals(W)
lam5 = lam5 / np.abs(lam5)
s1 = np.sort_complex(np.round(lam5, 9))
c_neg = float(np.max(np.abs(s1 - np.sort_complex(np.round(-lam5, 9)))))
c_pic = float(np.max(np.abs(s1 - np.sort_complex(np.round(-np.conj(lam5), 9)))))
check("L5_gauged_spectral_closures", max(c_neg, c_pic) < 1e-8,
      f"lambda→−lambda (bipartite, any A): {c_neg:.1e}; lambda→−conj(lambda) "
      f"(theta→pi−theta): {c_pic:.1e}, at eps=0.3")

# L6 — one-tick rigidity (zero induced stiffness, both channels)
chi_v1 = cis.brute_force_chi(6, 1, EH, QD, 'vector', sea='one-tick', eps=1e-2)
chi_s1 = cis.brute_force_chi(6, 1, EH, QD, 'staggered', sea='one-tick', eps=1e-2)
check("L6_one_tick_rigidity", max(abs(chi_v1), abs(chi_s1)) < 1e-9,
      f"one-tick chi: vec {chi_v1:.1e}, stag {chi_s1:.1e} — exactly zero "
      f"(theta→pi−theta pairs filled states to constant sum −pi)")

# L7 — channel equality, pointwise (two-tick sea)
mf, gf = cis.channel_equality_residual(20, 1, EH, QD)
sq2 = 1.0 / np.sqrt(2.0)
md, gd = cis.channel_equality_residual(20, 1, [0, sq2, -sq2], [1, 1, 1])
check("L7_channel_equality_pointwise", max(mf, gf, md, gd) < 1e-12,
      f"max |dM|, |dGap| — face: {mf:.1e}/{gf:.1e}, diag: {md:.1e}/{gd:.1e} "
      f"(8000-pt grids)")

# L8 — channel equality in the full response (brute force)
rel = {}
for L8 in (6, 8):
    bv = cis.brute_force_chi(L8, 1, EH, QD, 'vector', sea='two-tick', eps=1e-3)
    bs = cis.brute_force_chi(L8, 1, EH, QD, 'staggered', sea='two-tick', eps=1e-3)
    rel[L8] = abs(bs - bv) / abs(bv)
    results["checks"][f"_chi_two_tick_L{L8}"] = {"vector": bv, "staggered": bs}
check("L8_channel_equality_full_response",
      rel[6] < 1e-8 and rel[8] < 1e-5,
      f"para+diamagnetic brute force: rel diff L=6: {rel[6]:.1e}, L=8: {rel[8]:.1e}")

# L9 — exact rational bookkeeping
t2 = (Fraction(1, 1) * 2) ** -1 * 0 + Fraction(1, 4)   # explicit below
# per-branch quantum Pi_b equal in both channels (L7/L8):
#   1/g'^2 = sum q_P^2 Pi_b = 2 Pi_b ;  1/g^2 = sum T3^2 Pi_b = (1/2) Pi_b
inv_gp2 = Fraction(2)        # × Pi_b
inv_g2 = Fraction(1, 2)      # × Pi_b
t2 = inv_g2 / inv_gp2        # g'^2/g^2 = (1/g^2)/(1/g'^2)
s2 = t2 / (1 + t2)
content_factor = Fraction(2, 7) / t2
check("L9_charge_bookkeeping",
      t2 == Fraction(1, 4) and s2 == Fraction(1, 5)
      and content_factor == Fraction(8, 7),
      f"equal quanta + bare charges: t^2 = {t2}, sin^2(theta_W)_free = {s2}; "
      f"F49 target 2/7 = t^2 × {content_factor} — the 8/7 is charge "
      f"content/multiplicity (F38/F141-U1,U3), not loop dynamics")

results["summary"] = {
    "n_pass": sum(1 for c in results["checks"].values()
                  if isinstance(c, dict) and c.get("pass") is True),
    "n_total": sum(1 for c in results["checks"].values()
                   if isinstance(c, dict) and "pass" in c),
}
os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
with open(RESULTS, "w") as f:
    json.dump(results, f, indent=2, default=float)
print(f"\n{results['summary']['n_pass']}/{results['summary']['n_total']} PASS -> {RESULTS}")
if failures:
    raise SystemExit(f"FAILED: {failures}")
