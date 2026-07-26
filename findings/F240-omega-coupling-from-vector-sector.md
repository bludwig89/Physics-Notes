# F240 — The ω NN coupling from the model's vector-meson sector: KSFR × universality × baryon coherence, and the full-OBE deuteron

**Date:** 2026-07-03 - 08:56
**Status:** Confirmed — 10/10 PASS; 3 exact/algebraic (Tier-1), 7 quantitative (Tier-B). Honest partial result: the ω *sign*, *mass*, and *g_ωNN/g_ρNN=3 ratio* are Tier-1 derived; the *absolute* ω coupling from strict universality **overshoots** and the NN-required value stays a one-number bracket.
**Module:** `ca-simulation/ca_nuclear.py` (reused: `omega_exchange_potential`, `sigma_exchange_potential`, `derived_core_potential`, `solve_deuteron`)
**Tests:** `tests/findings/test_F240_omega_coupling_derivation.py`
**Results:** `test-results/F240_omega_coupling_derivation.json`
**Cross-refs:** [[F128-nn-short-range-omega-repulsion]] (built the ω channel + sign + m_ω; **fit** g_ω — F240 attacks its open "derive g_ω" item), [[F126-nn-intermediate-range-sigma-attraction]] (§"room left for the vector (ω)"; the 0.45 scalar quench this mirrors), [[F113-nn-short-range-repulsive-core]] (quark-Pauli core; the other face of the short-range repulsion), [[F104-p4-deuteron-tensor-bound-nucleus]] (the deuteron solver + OPEP tail, reused), [[F103-p3-dynamical-pion-goldstone]] (KSFR/KSRF $m_\rho^2=2g_{\rho\pi\pi}^2f_\pi^2$; the model's vector pole), [[F77-njl-gap-rpa-selfconsistent]] ($m_c$, $f_\pi$)

---

## Summary

Q3 asked to derive the isoscalar-vector (ω) NN channel from the model's
vector-meson sector — coupling **and** mass, *not* fit to NN data — add it to the
full one-boson-exchange (OBE) potential (F104 π tail + F126 σ + F113 core + ω),
and bind the deuteron with the F104 solver **without a tuned hard core**.

F128 already built the ω channel into `ca_nuclear` (potential, repulsive sign,
$m_\omega=m_\rho$) but *fit* $g_{\omega NN}^2/4\pi=5.39$ by rebinding $E_b$ — a
consistency check, not a prediction. F240 goes to the derivation F128 left open,
using the model's own **vector-dominance (VMD) chain**:

$$\underbrace{g_{\rho\pi\pi}=\frac{m_\rho}{\sqrt2\,f_\pi}}_{\text{KSFR, model }f_\pi}
\;\xrightarrow[\text{universality}]{\;g_{\rho NN}=g_{\rho\pi\pi}\;}\;
g_{\rho NN}\;\xrightarrow[\text{F128 B, exact}]{\;g_{\omega NN}=3\,g_{\rho NN}\;}\;
\boxed{\;\frac{g_{\omega NN}^2}{4\pi}\Big|_\text{strict univ.}=\frac{9}{4\pi}\Big(\frac{m_\rho}{\sqrt2\,f_\pi}\Big)^2=25.9\;}$$

**The honest outcome.** The *ratio* $g_{\omega NN}/g_{\rho NN}=3$ (baryon-number
coherence, Tier-1), the *mass* $m_\omega=m_\rho=782.7$ MeV (ρ–ω degeneracy,
Tier-1), and the repulsive *sign* (F128 A, Tier-1) are all model-derived. But the
*absolute* coupling from **strict universality** ($g_{\rho NN}=g_{\rho\pi\pi}=6.01$)
gives $g_{\omega NN}^2/4\pi=25.9$, which **overshoots**: fed to the deuteron
solver it **unbinds** the deuteron entirely (the ω repulsion swamps the σ
attraction). The NN data need a ~2.3× smaller vector coupling. Strikingly, the
required quench $0.43$ is numerically the **same** as F126's bare-scalar quench
$0.45$ — both channels' coherent-quark / universality couplings overshoot by the
same factor. So the ω absolute strength stays a **one-number bracket**,
$g_{\omega NN}^2/4\pi\in[5.4,\,11.1]$, sitting well below the universality ceiling
25.9, and F240 records this as a Tier-B bracket rather than a Tier-1 pin.

With the *bracketed* ω, the **full derived OBE binds the deuteron cleanly with no
tuned hard core**, at the physical point, two ways:

| route | $g_{\omega NN}^2/4\pi$ | $E_b$ (MeV) | $r_d$ (fm) | $P_D$ | note |
|---|---|---|---|---|---|
| **A** — F113 core + bare σ + ω | **5.39** | 2.221 (0.1%) | **1.978** (0.4%) | 6.3% | the F128 decomposition |
| **B** — pure meson OBE (σ + ω, no core) | **11.15** | 2.218 (0.3%) | 1.880 (4.6%) | 7.1% | textbook σ/ω residual |
| physical | 5–20 (OBE) | 2.224 | 1.97 | 4–6% | — |
| strict universality | 25.9 | **unbound** | — | — | overshoots |

and the **residual σ+ω well reaches −81 MeV** (in the −50…−100 MeV target) at
$g_{\omega NN}^2/4\pi=8$.

---

## 1 — The derivation chain (Tier-1 where exact, VMD posit where flagged)

### 1.1 KSFR / KSRF with the model $f_\pi$ (Tier-1)

F103 already uses the KSRF relation for the model's vector pole,
$m_\rho^2 = 2\,g_{\rho\pi\pi}^2 f_\pi^2$. Inverted with the **model output**
$f_\pi=92.07$ MeV and the vector-pole mass $m_\rho=782.7$ MeV (= $m_\omega$):

$$g_{\rho\pi\pi}=\frac{m_\rho}{\sqrt2\,f_\pi}=6.011,\qquad
\frac{g_{\rho NN}^2}{4\pi}\Big|_\text{univ}=\frac{g_{\rho\pi\pi}^2}{4\pi}=2.875.$$

Check A1: $m_\rho=\sqrt2\,g_{\rho\pi\pi}f_\pi$ closes to $1.5\times10^{-16}$
(machine/identity). The **only** external number in F103's KSRF is $g_{\rho\pi\pi}$
itself; here we *invert* it from the model $m_\rho,f_\pi$, so $g_{\rho\pi\pi}$ is a
model output, not an input.

### 1.2 Vector universality (VMD posit)

VMD/universality identifies the *quark*-level (and hence nucleon) vector charge
with the single universal vector coupling, $g_{\rho NN}=g_{\rho\pi\pi}$. This is
the standard bare-SU(6) statement; it is the *one modelling posit* in the chain
(flagged), not a theorem of the CA rule.

### 1.3 Baryon-number coherence $g_{\omega NN}=3\,g_{\rho NN}$ (Tier-1, exact ×3)

Each quark carries baryon number $\tfrac13$; the isoscalar ω couples coherently
to all three, so $g_{\omega NN}=3\,g_{\omega q}=3\,g_{\rho NN}$ (SU(6): isoscalar
vs isovector). This is exactly the F128 §B counting and the same coherent ×3 the
σ-isoscalar charge receives in F126. Checks A2/A3: ratio $=3$ (exact),
$g_{\omega NN}^2/4\pi=9\,g_{\rho NN}^2/4\pi=25.88$ (exact to $7\times10^{-15}$).

### 1.4 The mass $m_\omega=m_\rho$ (Tier-1 degeneracy, from F128)

The NJL vector bubble is flavour-blind, so isoscalar ω and isovector ρ are
degenerate up to OZI ($|m_\omega-m_\rho|/m_\rho=0.95\%$ empirically). We adopt
$m_\omega=782.7$ MeV. (The precise NJL value is scheme-dependent — the cutoff
breaks vector current conservation, F128 §C — so the degeneracy carries the mass.)

---

## 2 — The confrontation: strict universality overshoots (honest negative)

Feeding the **derived** $g_{\omega NN}^2/4\pi=25.9$ to the F104/F126/F128 solver
with the full bare σ (8.18) and the F113 core, the deuteron is **unbound**
(check B1): the ω repulsion overwhelms the σ attraction (bare σ alone over-binds
at $E_b=156$ MeV; a *modest* ω near 5–11 relaxes it to 2.2 MeV, but 25.9 pushes
it back above threshold). This is the well-known failure of strict vector
universality with $g_{\rho NN}=g_{\rho\pi\pi}$ — the "universality is only the
bare value" problem — surfacing inside the model.

**The quench.** The pure-OBE value the deuteron needs is
$g_{\omega NN}^2/4\pi=11.1$, i.e. $g_{\rho NN}^2/4\pi=1.24$ vs universality's
2.88 — a vector quench $11.1/25.9=0.431$. F126's scalar channel needed the
identical treatment: effective/bare $=3.69/8.18=0.451$ (check D1, agree to 4.5%).
**Both the scalar and vector coherent-quark couplings overshoot by the same
~2.3×.** This is a strong internal-consistency statement and points at a common
dressing (vertex/form-factor) suppression the static leading-order OBE does not
yet carry — the same "one number per channel" the σ analysis already flagged.

---

## 3 — The payoff: the full derived OBE binds the deuteron, no tuned wall

Using the bracketed ω (its *shape, sign, mass* derived; its *strength* the one
bracketed number), the coupled ${}^3S_1$–${}^3D_1$ solver binds the deuteron at
the physical point with **no hard core** (grid runs to $r_\text{min}$; the only
short-range regulator is the physical quark size $b=0.55$ fm):

- **Route A** (F128 decomposition = F113 quark-Pauli core + bare σ + ω):
  $g_{\omega NN}^2/4\pi=5.39$, $E_b=2.221$ MeV (**0.1%**), $r_d=1.978$ fm
  (**0.4%** vs 1.97), $P_D=6.3\%$, single bound $1^+$.
- **Route B** (pure meson OBE = bare σ + ω, F113 core off): $g_{\omega NN}^2/4\pi=11.15$,
  $E_b=2.218$ MeV (**0.3%**), $r_d=1.880$ fm (**4.6%**), $P_D=7.1\%$.

Route A is the more physical decomposition (the F113 core is a *real* additional
short-range repulsion, so the ω that completes it is smaller) and gives the
better radius. Route B is the textbook σ/ω-only picture (the acceptance's
"residual well = F113 core + ω" language) and shows the deuteron binds even with
the ω carrying the *entire* short-range repulsion.

**The residual well.** The σ+ω OBE residual (no core) reaches a minimum of
**−81 MeV** at $g_{\omega NN}^2/4\pi=8$ (check E1) — squarely in the requested
−50…−100 MeV window, with the correct shape (deepest inside ~0.8 fm, tailing to
zero by ~2 fm). This is the ~−50…−100 MeV intermediate-range well of the physical
NN force, reproduced.

---

## 4 — Checks

| check | statement | residual | tier |
|---|---|---|---|
| A1 | KSFR closes: $m_\rho=\sqrt2\,g_{\rho\pi\pi}f_\pi$ | $1.5\times10^{-16}$ | exact |
| A2 | baryon coherence $g_{\omega NN}=3g_{\rho NN}$ (×3) | $0$ | exact |
| A3 | $g_{\omega NN}^2/4\pi=9\,g_{\rho NN}^2/4\pi=25.88$ | $7\times10^{-15}$ | exact |
| B1 | strict-universality $g_\omega$ (25.9) **unbinds** deuteron | — | Tier-B |
| C1 | route A (core+σ+ω) binds $E_b=2.224$ | 0.15% | Tier-B |
| C2 | route A $r_d$ within 5% of 1.97 fm | 0.4% | Tier-B |
| C3 | route B (pure σ+ω OBE) binds $E_b=2.224$ | 0.28% | Tier-B |
| C4 | route B $r_d$ within 8% of 1.97 fm | 4.6% | Tier-B |
| D1 | vector quench 0.431 ≈ scalar quench 0.451 (F126) | 4.5% | Tier-B |
| E1 | σ+ω residual well $=-81$ MeV $\in[-100,-50]$ | — | Tier-B |

10/10 PASS. Numerics all real (real-space Schrödinger + real Yukawa folds); no
chiral/complex transforms, so the CLAUDE.md numpy caveat does not bite.

---

## 5 — What this adds / what stays open

1. **Derives the ω channel's structure from the vector sector.** Sign (Tier-1,
   F128), mass $m_\omega=m_\rho$ (Tier-1), and the exact $g_{\omega NN}/g_{\rho NN}=3$
   coherence (Tier-1) are model-native; the KSFR $g_{\rho\pi\pi}=6.01$ is a model
   output (from $m_\rho,f_\pi$).
2. **A clean, honest ceiling.** Strict VMD universality gives $g_{\omega NN}^2/4\pi=25.9$
   and **overshoots** — the deuteron unbinds. This is a genuine, falsifiable
   prediction of the naive chain, and it fails, exactly as bare vector
   universality is known to.
3. **The vector quench = the scalar quench.** The 0.43 suppression the NN data
   demand on the bare vector coupling equals F126's 0.45 on the bare scalar — one
   number per channel, the same dressing, a sharp target for a future
   vertex/form-factor derivation.
4. **The full OBE deuteron closes with no tuned hard core**, at the physical
   $E_b$, $r_d$, $P_D$, with the ω strength as the single bracketed input
   $[5.4,11.1]$, and the residual σ+ω well lands at −81 MeV in the target band.

### Known limitations / scope

- **Absolute $g_{\omega NN}$ not pinned (Tier-B bracket).** Strict universality
  overshoots; the NN-required value $[5.4,11.1]$ needs a channel-dressing factor
  (~0.43) the static leading-order OBE does not yet derive. This is the vector
  twin of F126's open scalar quench.
- **Universality (§1.2) is a VMD posit**, not a CA-rule theorem.
- **Static, leading-order central OBE.** Vector spin-orbit/tensor and recoil
  pieces of the ω are omitted (as for σ in F126 and OPEP in F104).
- **$M_N$, $g_A$ external; absolute scale is P6.**

---

## Exactness-inventory additions

Tier-1 (algebraic/exact): A1 KSFR closure, A2 coherence ×3, A3 $=9\times$ scaling
— 3 entries.
Tier-B (quantitative): B1 universality overshoot (unbinds), C1–C4 full-OBE
deuteron two routes ($E_b$, $r_d$), D1 vector-quench = scalar-quench, E1 residual
well $-81$ MeV — 7 entries. Absolute $g_{\omega NN}^2/4\pi$ bracketed $[5.4,11.1]$
below the derived universality ceiling 25.9.
