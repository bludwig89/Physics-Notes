---
id: CL309
title: The notebook's factorization identity (null vector = spinor bilinear; timelike vector = two null vectors with free direction on S²) is exact and boost-covariant, is redundant with F168/F169 for the photon's binding, and fixes the F169 O(k²) offset as |k_x k_y k_z|/(3|k|)
slug: factorization-route-redundant-with-f168-offset-derived
tier: supporting
kind: derivation
status: live
domain: [SR, QFT]
exactness: quantitative
findings: [F397, F24, F69, F91, F168, F169]
tests: [F397-factorization-route]
modules: [casim.engine.gauge.factorization]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-21'
last_verified: '2026-09-22'
provenance: authored
review_state: authored
confidence: medium
---

# CL309 — Factorization is structurally true and adds one number

## Statement

(1) $\sigma\!\cdot\!V=\psi\psi^\dagger$ for every future null $V$ and $V=a+b$ with $a=a_0(1,\hat a)$, $a_0=V\!\cdot\!V/[2(V_0-\hat a\!\cdot\!\vec V)]$, for every timelike $V$ and every $\hat a\in S^2$; the leg space is $U(2)/U(1)^2$ and the decomposition is $SL(2,\mathbb C)$-covariant. The notebook's boxed closed form (p.181) is not null and is superseded by this one. (2) The paired photon's $V$ is null (T1 only, no free $\hat a$); massive vectors carry $\hat a\in S^2$. (3) The F169 offset is $\Omega_\text{even}-T=|k_xk_yk_z|/(3|\vec k|)+O(k^3)$, the linear lift of the flat collinear valley that the $V$-null degeneracy leaves in the continuum. (4) *(added 2026-09-22, R11)* The paired photon's lattice 4-momentum is **not exactly null**: $V\!\cdot\!V=-\kappa(\hat k)|k|^4$ with the exact rational $\kappa(\hat k)=(1-\sum_i\hat k_i^4)/216+(\hat k_x\hat k_y\hat k_z)^2/36=2c_\text{lat}^2|C(\hat k)|$, where $C$ is the **already-established dimension-6 photon Lorentz-violation coefficient** of [CL274](CL274-no-dimension-5-photon-operator.md). The $O(k^4)$ null defect and the dimension-6 operator are the same statement in two variables; nothing downstream of the photon construction moves. Verified at 60-digit precision over 16 directions, worst absolute difference $2.2\times10^{-16}$ on $\kappa\sim10^{-3}$. (5) The identity does **not** predict $g_c$, does **not** map F91's chiral W± onto a degenerate leg, does **not** match F91's mass-suppressed Z axial split, and its free phase is **not** the EM $U(1)$.

## What it extends

Special relativity / Weyl-spinor algebra: the (½,½) ≅ spinor⊗spinor identification of a vector, used in the composite-photon literature (Srednicki/Varlamov via Perkins) as motivation for a *dynamical* pair. This card records that the identity is algebraic (no binding, no energy) and that, for the photon, it reproduces F168's zero-binding argument rather than improving it.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F397-notebook-factorization-route-pp176-182.md` | T1 $5.8\times10^{-15}$; T2 $2.7\times10^{-15}$; covariance $5.2\times10^{-14}$; offset ratio $1.054,1.026,1.013\to1$ | machine |
| `tests/registry/gauge.yaml` `F397-factorization-route` | 19 legs, declared control reddens only the null-pair leg | machine |
| `physics_notes_0708.pdf` pp.155–156 | Source: any $\hat u$ for $(t,0)$; table's "1" is canonical | source |

## Falsifier

Items (1) are identities (an algebraic failure would be an error, not a physics result); only item (3) is empirically falsifiable, and items (2) and (4) are structural. Failure modes: any timelike $V$ and $\hat a$ for which the corrected T2 pair is non-null or a leg has $a_0\le0$; a boost under which the decomposition is not covariant; or an F169 threshold search whose $(\Omega_\text{even}-T)/|\varepsilon(\vec k)|$ fails to tend to 1 as $|\vec k|\to0$ off the coordinate planes. Separately, a derivation of $g_c$ from the identity would overturn item (4).

## Status & history

Issued 2026-09-21 at `live`. Not claimed: identification of the leg-space $SU(2)$ with weak isospin (structural analogy only); the spin content of the F169 threshold endpoint (flagged in F397 R6(ii)).

## Sources

- `findings/F397-notebook-factorization-route-pp176-182.md`
- `findings/F169-photon-interacting-two-body-wavefunction.md`
- `findings/F168-paired-photon-binding-gauge-protected.md`
- `findings/F91-pairing-classification-theorem.md`
- `references/physics-notes-complete.md` §Pages 141–160, 176–182
