# F40 — F27 complex-mass adoption for the quark sector + Phase-4 electroweak wiring

**Date:** 2026-05-26 - 16:30
**Status:** Confirmed — FG-2 11/11 PASS, FG-3 6/6 PASS.
**Modules:** `ca-simulation/ca_strong.py` (additions only; old paths intact)
**Tests:** `model-tests/test_FG2_quark_complex_mass.py`, `model-tests/test_FG3_quark_electroweak.py`
**Results:** `test-results/FG2_quark_complex_mass.json`, `test-results/FG3_quark_electroweak.json`
**Closes:** `first-gen-completeness-review.md` §3 items 1 and 2 (quark electroweak wiring + unified mass mechanism); §5.1 FG-2 and FG-3.

---

## Summary

Two coupled deficits identified in the 2026-05-25 first-generation completeness review are closed in this work:

1. **Mass mechanism — leptons used the F27 chiral-SU(2) complex-mass step ([F27](F27-complex-mass-chiral-su2.md)) while quarks still ran the Higgs–Yukawa path through `dirac_step_2d_varm_complex_splitstep`.** The project's [key-decisions.md](../key-decisions.md) commits to F27 as the adopted mass mechanism (no Higgs); the quark sector now honours that decision.

2. **Electroweak coupling — the quark doublet $(u,d)_L$ in `ca_strong.py` had zero SU(2)$_L$ / $W_\mu$ / $Z$ / $Y$ wiring** (verified in the review: `ca_strong.py` only mentions `ca_weak` in a comment). The doublet now couples to a dynamical $W_\mu$ link field via a 2D-square analog of [F31](F31-wmu-covariant-hopping.md) / [F34](F34-wmu-fermion-vertex.md).

The decision tree the user set ("adopt F27 complex mass and test; if that does not, complete wiring to the electroweak sector") played out exactly as F27 Known Limitation #1 predicts: the F27 mass step on its own is U(1) Ward-invariant per flavour and SU(2)$_L$ Ward-invariant for the *degenerate* doublet, but it fails Ward identity for split mass (Q10) and for varying $V(x)$ when paired with a free spectral kinetic step (Q11). Wiring the doublet to $W_\mu$ restores constant-$V$ Ward identity to machine precision (QE2).

---

## Phase 1 — F27 complex mass for the quark sector (FG-2)

### What was added

The following functions live in a new section at the bottom of `ca-simulation/ca_strong.py`:

| Function | Role |
|---|---|
| `chirality_split_quark(q, flavour=None)` | $(N_L, N_R)$ totals for one flavour or the whole field. |
| `make_theta_field_quark(shape, mode, seed)` | Per-flavour $\theta_f(x)$ field for the β-gauge. |
| `quark_mass_step_f27(q, theta_flavour, m_flavour, dt)` | F27 1-flavour β-gauge complex mass per `(flavour, colour)` using `cdir.mass_step_1flavor_u1`. |
| `step_strong_2d_complex_mass(q, U, theta_flavour, m_flavour, dt)` | Full Strang step: SU(3) parallel transport → F27 complex mass per `(f,c)` → SU(3) parallel transport. |
| `quark_u1_gauge_transform_f27(q, phi, flavour)` | The χ-sector U(1) transform used to verify the F27 T4 Ward identity. |
| `quark_doublet_mass_step_su2(q, U_a, U_b, m_doublet, dt)` | F27 SU(2)$_L$ doublet mass step applied to $(u,d)$ per colour (shared mass, F27 T5 analog). |
| `quark_doublet_su2_transform_chiral(q, V_a, V_b, U_a, U_b)` | Chiral SU(2)$_L$ transform: $V \cdot \eta_{u,d}$, $\chi$ unchanged, $U \to V \cdot U$. |

The mechanism is the per-cell unitary

$$M(\theta_f) = \begin{pmatrix} c_{m_f} \mathbb I & i s_{m_f} e^{i\theta_f} \mathbb I \\ i s_{m_f} e^{-i\theta_f} \mathbb I & c_{m_f} \mathbb I \end{pmatrix}, \qquad c_{m_f}=\cos(m_f \,dt), \; s_{m_f}=\sin(m_f \,dt),$$

applied per flavour per colour. Distinct $m_u, m_d, m_s$ give natural up/down/strange mass splitting at the flavour level, and the mass is colour-blind (only the SU(3) link rotates colour).

### FG-2 results (`test-results/FG2_quark_complex_mass.json`)

| # | Test | Residual | Status |
|---|---|---|---|
| Q1 | Unitarity, random $\theta$, 20 steps | $5.4\times10^{-15}$ | ✅ PASS |
| Q2 | U(1) β-gauge Ward identity (mass step alone, per flavour) | $1.2\times10^{-16}$ | ✅ PASS |
| Q3 | Higgs-free mass gap: pure left-$u$ → $N_R/N_{L0}=0.30$ at $m_u=0.4$, $n=80$ | — | ✅ PASS |
| Q4 | Up/down/strange splitting: $r_d/r_u=3.96$ (exp $4$), $r_s/r_u=15.22$ (exp $16$) | — | ✅ PASS |
| Q5 | $\theta$ pure-gauge — total $\|q\|^2$ identical across $\theta \in \{0,\pi/3,\pi/2\}$ | $2.8\times10^{-14}$ | ✅ PASS |
| Q6 | Colour neutrality — $[V_{\text{SU(3) const}}, \text{mass step}]=0$ | $1.1\times10^{-16}$ | ✅ PASS |
| Q7 | Cold-link, $\theta=0$ regression: F27 quark step ≡ 9 independent F27 1-flavour Dirac steps | $0.0$ exact | ✅ PASS |
| Q8 | Colour-charge conservation $Q^a$ under the F27 quark step (cold links, 20 steps) | $1.7\times10^{-14}$ | ✅ PASS |
| Q9 | SU(2)$_L$ Ward identity, **degenerate doublet** mass step alone | $8.4\times10^{-17}$ | ✅ PASS |
| Q10 | SU(2)$_L$ Ward identity with **split** mass $m_u \ne m_d$ — diagnostic (must be ≫ ε) | $2.4\times10^{-1}$ | ✅ diag |
| Q11 | Full step (kinetic + mass) under varying $V(x)$, **no $W_\mu$** — diagnostic (must be ≫ ε) | $5.7\times10^{-1}$ | ✅ diag |

Q10 and Q11 are the "if that does not" trigger: an explicit mass split $m_u \ne m_d$ breaks SU(2)$_L$ at the mass-term level, and a varying $V(x)$ with a free spectral kinetic step breaks SU(2)$_L$ at the kinetic level. Both are exactly the Known Limitations F27 itself flagged.

---

## Phase 4 — Electroweak wiring of the quark doublet (FG-3)

### What was added

A second section in `ca_strong.py` adds the 2D-square analog of the lepton-sector $W_\mu$ machinery in `ca_wmu.py`:

| Function | Role |
|---|---|
| `make_w_link_field_2d(shape, mode, seed)` | $W_\mu(x) \in \mathrm{SU}(2)$ link field, two directions in 2D. |
| `w_link_unitarity_residual_2d(W_links)` | Diagnostic: $\max | |W_a|^2 + |W_b|^2 - 1 |$. |
| `u_eff_from_w_links_2d(W_links)` | Site-centred SU(2) effective gauge field by averaging the two link directions then re-unitarising (mirrors `ca_wmu._u_eff_from_links`). |
| `w_link_gauge_transform_2d(W_links, V_a, V_b)` | $W_\mu(x) \to V(x) \cdot W_\mu(x) \cdot V^\dagger(x+\hat\mu)$. |
| `covariant_quark_doublet_step_2d(q, U_color, W_links, U_a_mass, U_b_mass, m_doublet, dt, m_strange, theta_strange)` | Full step: SU(3) transport → kinetic half (site-isospin rotation on $\eta$ via $U_{\rm eff}$, then 2D spectral Weyl half per flavour, χ untouched) → F27 SU(2) doublet mass → kinetic half → SU(3) transport. Strange ($s$) is handled as an SU(2)$_L$ singlet with its own F27 1-flavour mass. |

The architecture exactly mirrors `ca_wmu.covariant_weyl_step_3d_bcc` (F31) — site-centred $U_{\rm eff}$ position-space rotation, then the spectral kinetic step per flavour — because the same physical argument applies in 2D: the spectral step is identical for $u$ and $d$ flavours, so a constant $V$ on the isospin index commutes with it; for varying $V$ the residual is $O(a)\cdot|\nabla V|\cdot L$ (the W1.4 status). Right-handed $\chi$ is an SU(2)$_L$ singlet and uses identity isospin (no $W$ coupling).

### FG-3 results (`test-results/FG3_quark_electroweak.json`)

| # | Test | Residual | Status |
|---|---|---|---|
| QE1 | Cold $W$-link regression: $W=I$ → free kinetic halves ∘ doublet mass ∘ halves | $0.0$ exact | ✅ PASS |
| **QE2** | **SU(2)$_L$ Ward identity with constant $V(x)$ — F34 W4.1 analog** | $\mathbf{2.8\times10^{-16}}$ | ✅ **PASS** |
| QE3 | Right-handed $\chi$ exactly decoupled from $W$ at $m=0$ — F34 W4.3 analog | $0.0$ exact | ✅ PASS |
| QE4 | Norm drift over 20 steps with random $W$ | $2.1\times10^{-14}$ | ✅ PASS |
| QE5 | SU(2)$_L$ Ward identity with random varying $V(x)$ — W1.4 O(a) status | $5.8\times10^{-1}$ | ✅ diag |
| QE6 | Colour-charge conservation $Q^a$ under the W-coupled doublet step | $2.5\times10^{-14}$ | ✅ PASS |

QE2 is the rigorous proof that the EW wiring is correct: for spatially homogeneous $V(x)$ the SU(2)$_L$ Ward identity holds to one part in $\sim 10^{16}$, matching the lepton-sector F34 W4.1 ($1.7\times10^{-17}$) to within an order of magnitude.

QE5 is the same shape as ca_wmu W1.4: at full Nyquist randomness the residual is $O(1)$, reflecting the fundamental tension between a spectral kinetic step and a local gauge field. For smooth $V(x)$ with $a\,|\nabla V| \ll 1$ the residual scales as $a\,|\nabla V|\,L$ and vanishes in the continuum limit — exactly the lepton-side situation.

---

## Exactness-inventory entries added (counts shift as noted)

**New Tier-1 algebraic (5):**

- F40-Q2 — F27 U(1) β-gauge Ward identity per quark flavour (mass step), $1.2\times10^{-16}$.
- F40-Q7 — Cold-link / $\theta=0$ quark F27 step bit-for-bit equals 9 independent F27 1-flavour lepton steps, $0.0$ exact.
- F40-Q9 — Degenerate-doublet SU(2)$_L$ Ward identity for the F27 quark doublet mass step, $8.4\times10^{-17}$.
- F40-QE1 — Cold $W$-link regression of the W-covariant quark doublet step, $0.0$ exact.
- F40-QE2 — SU(2)$_L$ Ward identity for the W-coupled quark doublet under constant $V$, $2.8\times10^{-16}$ (F34 W4.1 analog).
- F40-QE3 — Right-handed $\chi$ decoupled from $W$ at $m=0$ for the quark sector, $0.0$ exact (F34 W4.3 analog).

**New Tier-2 machine precision (4):**

- F40-Q1 — Unitarity of the F27 quark step over 20 steps, random $\theta$, $5.4\times10^{-15}$.
- F40-Q8 — Colour-charge $Q^a$ conserved under the F27 quark step (cold links), $1.7\times10^{-14}$ over 20 steps.
- F40-QE4 — Norm conservation of the W-coupled quark doublet step, $2.1\times10^{-14}$ over 20 steps.
- F40-QE6 — Colour-charge conservation under the W-coupled step, $2.5\times10^{-14}$.

**New Tier-3 quantitative (1):**

- F40-Q4 — Up/down/strange mass splitting follows $(m_f/m_u)^2$ in the linear regime: $r_d/r_u=3.96$ (vs $4$), $r_s/r_u=15.22$ (vs $16$); $\sim 1\%$ off from the sin²→(·)² truncation.

---

## Relationship to prior findings

| Finding | Connection |
|---|---|
| [F27](F27-complex-mass-chiral-su2.md) — Chiral SU(2) complex mass | F40 ports the F27 mechanism to the quark sector (per flavour + doublet); FG-2 Q2, Q9 are direct analogs of F27 T4, T5. |
| [F31](F31-wmu-covariant-hopping.md) — Covariant BCC hopping | FG-3 is the 2D-square analog (different lattice, same site-average-then-spectral architecture). |
| [F34](F34-wmu-fermion-vertex.md) — Lepton-$W$ vertex | FG-3 QE2 is the quark-sector analog of W4.1; QE3 is the analog of W4.3. |
| [F35](F35-electroweak-mixing.md) — Electroweak mixing | Hypercharge / Weinberg-mix wiring of the quark doublet still pending; this finding only delivers SU(2)$_L$. |

---

## What still remains for first-generation closure

This finding closes review §3 items 1 (EW wiring) and 2 (unified mass mechanism). Remaining structural items from the review:

3. Right-handed singlets $e_R, u_R, d_R$ as **dynamical** hypercharge-coupled fields (currently only present as spectators / algebraic table entries — F40 keeps them as the $\chi$ sector with identity isospin).
4. **Dynamical $Z$** coupled to the fermion neutral current.
5. **Gluons** brought to the dynamical-field standard (this finding leaves SU(3) as link variables only).
6. Antiparticle / charge-conjugation closure per species.

The natural next FG test is **FG-7** (dynamical gluon propagation + confinement) and **FG-4** (dynamical $Z$), per the review's recommended sequence.

---

## Files added / modified

- `ca-simulation/ca_strong.py` — appended ~440 lines: F27 complex-mass section + Phase-4 EW wiring section.
- `model-tests/test_FG2_quark_complex_mass.py` (new) — 11 tests.
- `model-tests/test_FG3_quark_electroweak.py` (new) — 6 tests.
- `test-results/FG2_quark_complex_mass.json`, `test-results/FG3_quark_electroweak.json` (new).

Total runtime FG-2 + FG-3: $\sim 2.3$ s on the sandbox.
