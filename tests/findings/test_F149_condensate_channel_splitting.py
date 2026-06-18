"""
F149 — the condensate-sector response: mass is the unique channel-splitting
agent, the F147 channel lock breaks ∝ m², the one-tick rigidity survives the
mass, and charge content cannot supply the F49 ratio (exact no-go).

Continues F147 (massless walk loop) per F141 §4 / U2:

  N1  Dirac parity theorem: ω_m(q+Q) = π−ω_m(q) and D(q+Q) = −X D(q) X,
      X = diag(I,−I) — the massless parity theorem survives the mass exactly
  N2  {S, D_A} = 0 with S = P̂·X̂, for a GAUGED massive walk (ε = 0.3) —
      the bipartite closure generalizes to the Dirac case
  N3  massless limit + eig validation: at m = 0 the channel comparison is
      machine-equal (F147 recovered through the 4×4 Dirac path), and the
      batched numpy eig is checked against the analytic dispersion
      arccos(n·u) (the CLAUDE.md numpy/chiral guard)
  N4  massive one-tick rigidity: χ = 0 (both channels, m = 0.4) — the
      stiffness is irreducibly stroboscopic even in the condensate-dressed
      sea
  N5  the channel lock BREAKS for m > 0: pointwise matrix-element split
      turns on monotonically in m while the circle gaps stay EXACTLY equal
      (Dirac parity theorem) — the mass splits weights, not kinematics
  N6  brute-force full response (L=6, two-tick): channel split nonzero for
      m > 0, onset consistent with ∝ m² at small m
  N7  paramagnetic small-q̃ ratio: smooth monotone drift of vec/stag from
      exactly 1 at m = 0 (channel lock) — sign: staggered enhanced
      (paramagnetic piece only; physical small-q̃ ratio needs the
      diamagnetic-complete computation — flagged open)
  N8  charge-content bookkeeping (exact fractions): bare content t² = 1/4
      (s² = 1/5); full F38 SM-generation content ΣT₃² = 2, Σ(Y/2)² = 10/3
      ⟹ t² = 3/5, s² = 3/8 (the classic equal-quanta/GUT value).  NEITHER
      equals 2/7: required factors 8/7 (bare) and 21/10 (SM) — charge
      content alone cannot supply the F49 ratio.  Combined with N5/N6: the
      8/7 must be dynamical (condensate splitting) and/or geometric
      multiplicity (F141-U1/U3), and the splitting mechanism with the
      required structure now exists.

Runtime ~60 s.
"""

import json
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "ca-simulation")))
import ca_induced_stiffness as cis  # noqa: E402

RESULTS = os.path.normpath(
    os.path.join(HERE, "..", "..", "test-results", "F149_condensate_channel_splitting.json"))

results = {"finding": "F149", "checks": {}}
failures = []


def check(name, ok, detail):
    results["checks"][name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures.append(name)


EH, QD = [0, 1, 0], [1, 0, 0]

# N1 — Dirac parity theorem
rd, ro = cis.dirac_parity_residuals(0.4)
check("N1_dirac_parity_theorem", max(rd, ro) < 5e-15,
      f"omega_m(q+Q)=pi−omega_m: {rd:.2e}; D(q+Q)=−X D X: {ro:.2e} (m=0.4)")

# N2 — generalized bipartite closure, gauged
rs = cis.dirac_S_anticommutation(L=4, m=0.4, eps_field=0.3)
check("N2_S_anticommutation_gauged", rs < 1e-13,
      f"{{S, D_A}} = 0 with S = P·diag(I,−I), eps=0.3: {rs:.2e}")

# N3 — massless limit + eig validation
rel0, gres0, dres0 = cis.dirac_channel_compare(14, 1, EH, QD, 0.0)
check("N3_massless_limit_lock", rel0 < 1e-12 and gres0 < 1e-12 and dres0 < 1e-12,
      f"m=0 channel lock through the 4x4 path: rel dT {rel0:.1e}, dGap {gres0:.1e}; "
      f"numpy eig vs analytic arccos(n·u): {dres0:.1e}")

# N4 — massive one-tick rigidity
cv1 = cis.dirac_brute_force_chi(6, 1, EH, QD, 'vector', m=0.4, sea='one-tick', eps=1e-2)
cs1 = cis.dirac_brute_force_chi(6, 1, EH, QD, 'staggered', m=0.4, sea='one-tick', eps=1e-2)
check("N4_massive_one_tick_rigidity", max(abs(cv1), abs(cs1)) < 1e-9,
      f"one-tick chi at m=0.4: vec {cv1:.1e}, stag {cs1:.1e} — rigidity survives the mass")

# N5 — the lock breaks for m>0, monotone; gaps stay exactly equal
ms = [0.05, 0.1, 0.2, 0.4]
rels, gmax = [], 0.0
for m in ms:
    rel, gres, _ = cis.dirac_channel_compare(14, 1, EH, QD, m)
    rels.append(rel)
    gmax = max(gmax, gres)
results["checks"]["_split_vs_m"] = {"m": ms, "rel_dT": rels}
mono = all(rels[i] < rels[i + 1] for i in range(len(rels) - 1))
check("N5_mass_splits_channels",
      rels[1] > 0.1 and mono and gmax < 1e-12,
      f"pointwise rel dT: {[f'{r:.3f}' for r in rels]} at m={ms} (monotone: {mono}); "
      f"gaps equal to {gmax:.1e} at ALL m — weights split, kinematics locked")

# N6 — brute-force full-response split, ~m^2 onset
diffs = {}
for m in (0.05, 0.1, 0.2):
    bv = cis.dirac_brute_force_chi(6, 1, EH, QD, 'vector', m=m, sea='two-tick', eps=1e-3)
    bs = cis.dirac_brute_force_chi(6, 1, EH, QD, 'staggered', m=m, sea='two-tick', eps=1e-3)
    diffs[m] = bs - bv
results["checks"]["_bf_split"] = {str(m): d for m, d in diffs.items()}
r_m2 = (diffs[0.05] / 0.05 ** 2) / (diffs[0.1] / 0.1 ** 2)
check("N6_full_response_split_m2_onset",
      abs(diffs[0.1]) > 1e-3 and 0.6 < r_m2 < 1.6,
      f"(chi_stag−chi_vec): {diffs[0.05]:.4f} (m=0.05), {diffs[0.1]:.4f} (m=0.1), "
      f"{diffs[0.2]:.4f} (m=0.2); m^2-scaling ratio {r_m2:.2f} (1 = exact m^2)")

# N7 — paramagnetic small-q̃ ratio: smooth monotone drift from 1
C = cis.hop_matrices('+')
def chi_para(L, m_qt, m, ch):
    qt = (2 * np.pi * m_qt / L) * np.array(QD, dtype=float)
    g = (np.arange(L) + 0.3819660112501051) * (2 * np.pi / L) - np.pi
    qx, qy, qz = np.meshgrid(g, g, g, indexing='ij')
    q = np.stack([qx, qy, qz], axis=-1).reshape(-1, 3)
    qp = q + qt + (cis.Q_STAG if ch == 'staggered' else 0.0)
    Po, _, Oo, _, _ = cis.dirac_bands(q, m)
    _, Pe, _, Oe, _ = cis.dirac_bands(qp, m)
    dW = cis.dirac_vertex_W2(q, qt, np.array(EH, dtype=float), C, m, channel=ch)
    Mop = Pe @ dW @ Po
    T = np.einsum('...ij,...ij->...', Mop, np.conj(Mop)).real
    dOm = cis._wrap(Oe - Oo)
    ok = np.abs(dOm) > 1e-12
    return float(np.sum(T[ok] / np.tan(dOm[ok] / 2)) / q.shape[0])

ratios = []
for m in (0.0, 0.1, 0.2, 0.4):
    cv = chi_para(20, 1, m, 'vector')
    s = chi_para(20, 1, m, 'staggered')
    ratios.append(cv / s)
results["checks"]["_para_ratio_vs_m"] = {"m": [0.0, 0.1, 0.2, 0.4], "vec_over_stag": ratios}
check("N7_para_ratio_smooth_drift",
      abs(ratios[0] - 1.0) < 1e-12
      and all(ratios[i] > ratios[i + 1] for i in range(3)),
      f"paramagnetic vec/stag: {[f'{r:.4f}' for r in ratios]} at m=0,0.1,0.2,0.4 — "
      f"exactly 1 at m=0, monotone drift (staggered enhanced in the para piece; "
      f"physical small-q ratio needs the diamagnetic term — open)")

# N8 — charge-content bookkeeping (exact fractions)
# bare walk content: q_P = ±1 both branches, T3 = ±1/2
t2_bare = Fraction(1, 2) / Fraction(2)            # (ΣT3²)/(Σq_P²) = (1/2)/2
# F38 SM generation (Q = T3 + Y/2; Y_L=−1, e_R −2, Q_L +1/3, u_R +4/3, d_R −2/3)
sum_T3 = 2 * Fraction(1, 4) + 3 * 2 * Fraction(1, 4)          # lep + 3-colour quark doublets
sum_Y2 = (2 * Fraction(1, 4) + Fraction(1)                     # L doublet (Y/2=−1/2), e_R (−1)
          + 6 * Fraction(1, 36) + 3 * Fraction(4, 9) + 3 * Fraction(1, 9))  # Q_L, u_R, d_R
t2_sm = sum_T3 / sum_Y2
s2_sm = t2_sm / (1 + t2_sm)
need_bare = Fraction(2, 7) / t2_bare
need_sm = Fraction(2, 7) / t2_sm
check("N8_content_no_go",
      t2_bare == Fraction(1, 4) and sum_T3 == 2 and sum_Y2 == Fraction(10, 3)
      and t2_sm == Fraction(3, 5) and s2_sm == Fraction(3, 8)
      and need_bare == Fraction(8, 7) and need_sm == Fraction(10, 21),
      f"bare: t²={t2_bare} (needs ×{need_bare}); F38 SM generation: ΣT₃²={sum_T3}, "
      f"Σ(Y/2)²={sum_Y2} ⟹ t²={t2_sm}, sin²θ_W={s2_sm} (the equal-quanta/GUT value; "
      f"needs ×{need_sm}) — no charge set gives 2/7: content no-go")

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
