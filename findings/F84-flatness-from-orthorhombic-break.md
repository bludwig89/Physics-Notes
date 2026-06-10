# F84 — Why the generation rotation is flat: it is the same orthorhombic break that F76 needed for three distinct masses (closure of the F75→F84 descent)

**Date:** 2026-06-03 - 00:28
**Status:** Partial (closing) — 4/4 checks PASS. **This identifies F82's "flat direction" assumption physically and closes the loop:** the stiffness $\kappa$ that F82 needed to vanish *is* the residual democratic ($S_3$ generation-permutation) symmetry, and it is removed by the **same orthorhombic break** F76 invoked for three distinct masses. The Koide ratio interpolates $\tfrac13\leftrightarrow\tfrac23$ between the cubic-degenerate vacuum (F75) and the complete orthorhombic break (F76/F82). The descent now bottoms out at two clearly-identified structural primitives; the final residual — that the charged-lepton break is *essentially complete* — is bounded by the data to $\kappa/\lambda\lesssim2\times10^{-5}$.
**Script:** `tests/findings/test_F84_flatness_from_orthorhombic_break.py` (<1 s)
**Results:** `test-results/F84_flatness_from_orthorhombic_break.json`
**Numbering note:** built concurrently with the lattice-spacing finding that took **F83**; this flatness/closure finding is **F84**.
**Cross-references:** [[F82-why-saturation-composite-mass-peak]] (the flatness assumption this explains), [[F76-generation-mass-hierarchy-crystal-field]] (the orthorhombic break for three distinct masses), [[F75-three-generations-from-bcc-irrep-selection]] (the cubic degenerate triplet — the $\kappa\to\infty$ endpoint), [[F80-one-45deg-em-saturation-koide]] / [[F81-why-45deg-pair-phase-saturation]] (the $45°$/$N=2$ chain), [[F92-per-constituent-phase-consistency]] / [[F93-orthorhombic-Eg-vacuum]] (2026-06-04: the two §6 irreducible inputs attacked — input #1 reduced to a consistency fixed point of the F73+F78 mass laws with the Fock $\sqrt2$ as the only new input; input #2 identified as an $E_g$ condensate on the second-neighbour shell with $\kappa=0$ as a stabilizer theorem).

---

## 1. The residual F82 left

F82 showed the lepton sits at $\phi=45°$ because the composite mass $m_H=\sin(2\phi)$
peaks there and the energy follows the mass — **provided** $\phi$ is a *flat*
direction (no stiffness $\kappa>0$ pulling back toward the democratic point). It
flagged that the exact-$45°$ data require $\kappa=0$ but did not say *why* the
direction is flat. This finding identifies $\kappa$ and removes the assumption.

---

## 2. $\kappa$ is the residual democratic symmetry (H1)

The stiffness in $E(\phi)=\tfrac12\kappa\phi^2-\lambda\sin(2\phi)$ is precisely the
**restoring force toward equal generations** — the residual $S_3$
(generation-permutation / "democratic") symmetry. Scanning it:

| $\kappa$ (democratic stiffness) | $\phi^\*$ | $Q$ | vacuum |
|---|---|---|---|
| $\to\infty$ | $0°$ | $1/3$ | **cubic** ($S_3$ intact, generations equal) |
| $1$ | $35.9°$ | $0.508$ | partial break |
| $0$ | $45°$ | $2/3$ | **orthorhombic** ($S_3$ fully broken) |

$Q$ interpolates monotonically from $1/3$ to $2/3$ as the democratic symmetry is
switched off.

## 3. The two endpoints are F75 and F76/F82 (H2)

- **$\kappa\to\infty$ (cubic vacuum, full $S_3$):** $\phi\to0$, $Q\to1/3$ — the
  **degenerate $T_{1u}$ triplet of F75** (three generations of equal mass at the
  fully cubic point). ✓
- **$\kappa=0$ (orthorhombic vacuum, no $S_3$):** $\phi=45°$, $Q=2/3$ — the
  **equipartition of F76/F82**. ✓

So the $\kappa$-interpolation literally connects F75 (cubic, degenerate) to
F76/F82 (orthorhombic, equipartitioned). The Koide ratio is a *dial reading of
how completely the democratic symmetry is broken.*

## 4. One break, two consequences (H3)

The order parameter is the **orthorhombicity** $s$ (the inequivalence of the
three cube axes), and it controls *both* phenomena, at two thresholds:

| $s$ | three distinct masses? | $\kappa$ | $Q$ |
|---|---|---|---|
| $0$ (cubic) | no (degenerate) | $\infty$ | $1/3$ |
| $0.3$ (weak) | **yes** | $11.1$ | $0.343$ |
| $1$ | yes | $1.0$ | $0.508$ |
| $5$ | yes | $0.04$ | $0.657$ |
| $50$ (complete) | yes | $4\times10^{-4}$ | $0.667$ |

- **Three distinct masses** turn on at *any* $s>0$ — the F76-C1 threshold.
- **Equipartition ($Q\to2/3$)** needs the break to be *complete* ($s$ large,
  $\kappa\to0$).

This is the unification: the **same orthorhombic break** that F76 needed to lift
the $T_{1u}$ triplet into three distinct masses is what removes the democratic
restoring force and lets the binding term (F82) saturate $\phi$ at $45°$. One
structural fact — an orthorhombic vacuum — supplies the three generations (F75),
their distinctness (F76), *and* the flat $\phi$ that gives $Q=2/3$ (F82/F84).

## 5. Robustness: the break is essentially complete (H4)

The charged leptons sit at $Q=2/3$ to one part in $10^5$
($|Q-\tfrac23|=6.2\times10^{-6}$, a $0.91\sigma$, measurement-limited deviation —
consistent with *exactly* $2/3$, F76-C3). Translated through $\phi^\*(\kappa)$
near $\kappa=0$, this **bounds the residual democratic stiffness**:

$$\frac{\kappa}{\lambda}\lesssim2\times10^{-5},$$

i.e. the charged-lepton orthorhombic break is essentially *complete*. $Q=2/3$ is
therefore robust — the value is not finely tuned but sits at the $\kappa=0$
attractor, with current data placing it there to $\sim10^{-5}$.

---

## 6. Closure: where the descent bottoms out (H5)

The chain that began at F75 now reads end-to-end:

> **F75** count $=3$ (max cubic single-valued irrep) → **F76** hierarchy needs an
> orthorhombic break ($T_{1u}\to B_{1u}\oplus B_{2u}\oplus B_{3u}$) → **F78**
> $\sqrt m$ is the constituent amplitude ($m=y^2$, Cooper-pair bilinear) →
> **F76/F80** equipartition $Q=2/3$ → **F80/F81** $45°$ as the $N=2$ pair's half
> of the $\pi/2$ phase budget → **F82** the pair sits there because the composite
> mass peaks at $45°$ (any binding, coupling-independent) → **F84** the direction
> is flat because the orthorhombic vacuum has removed the democratic restoring
> force.

It bottoms out at **two irreducible structural inputs**:

1. **The per-constituent identification** — the generation polar angle $\phi$ is
   the constituent rest-phase, so the composite mass is $m_H=\sin(2\phi)$.
   Strongly supported by the $N=2$ readout (F81-E2), but not derived from the
   QCA update rule.
2. **The orthorhombic vacuum** — the lattice ground state has three inequivalent
   axes. This single fact gives the three generations (F75), their distinctness
   (F76-C1), and the flat $\phi$ / $\kappa\to0$ that fixes $Q=2/3$ (F82/F84).

So the charged-lepton value $Q=2/3$ follows from *a two-constituent pair (F73) on
an orthorhombic vacuum (F76), with the per-constituent-phase identification.*
"Why these two" $=$ "why this lattice vacuum" — the model's deepest primitive,
and the honest end of this particular thread.

---

## 7. Test summary (`test_F84_flatness_from_orthorhombic_break.py`, 2026-06-03 - 00:28)

| Check | Statement | Result | Status |
|---|---|---|---|
| H1 | $Q$ interpolates $\tfrac13\!\leftrightarrow\!\tfrac23$ with democratic stiffness $\kappa$ | monotonic | PASS |
| H2 | endpoints $=$ F75 cubic ($1/3$) and F76/F82 ortho ($2/3$) | both recovered | PASS |
| H3 | one order parameter $s$; distinctness at $s>0$, equipartition at complete break | verified | PASS |
| H4 | residual $\kappa/\lambda\lesssim2\times10^{-5}$ from $|Q-\tfrac23|$ | bounded | PASS |
| H5 | closure: two irreducible inputs (recorded) | — | (info) |

**Overall 4/4 PASS.**

---

## 8. Provenance

- Closes the flatness residual of F82 by identifying $\kappa$ with the residual
  democratic symmetry and tying its removal to the F76 orthorhombic break; the
  $\kappa$-interpolation between F75 and F76/F82, and the closure statement, are
  new.
- Verification: `tests/findings/test_F84_flatness_from_orthorhombic_break.py`
  (2026-06-03 - 00:28, 4/4 PASS), results
  `test-results/F84_flatness_from_orthorhombic_break.json`.
