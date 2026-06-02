# F78 — Why $\sqrt m$: the Cooper-pair bilinear, and the equipartition amplitude as the democratic–hierarchical midpoint

**Date:** 2026-06-01 - 21:14
**Status:** Partial — 6/6 checks PASS. **Part A is a derivation** (why the cubic vector is $\sqrt m$, given the model's own Cooper-pair premise) and resolves the open puzzle F76 left. **Part B is a sharp characterisation plus an honest negative**: the equipartition amplitude $\sqrt2$ (Koide $Q=2/3$) is the exact democratic↔hierarchical midpoint, but it is **not** produced by the cube's symmetric dynamics (which give the degenerate $Q=1/3$). So $\sqrt2$ remains an input — now pinned to a single critical condition.
**Script:** `model-tests/test_F78_koide_amplitude_pairing.py` (<1 s)
**Results:** `test-results/F78_koide_amplitude_pairing.json`
**Numbering note:** built concurrently with the NJL-gap finding that took **F77**; this Koide-amplitude finding is **F78**.
**Cross-references:** [[F76-generation-mass-hierarchy-crystal-field]] (the $\sqrt m$ puzzle this answers), [[F75-three-generations-from-bcc-irrep-selection]] ($T_{1u}$ triplet), [[F73-spin0-bound-pair-scalar]] / [[F74-two-constituent-bound-state-binding]] / [[F77-njl-gap-rpa-selfconsistent]] (the Cooper-pair condensate, its 45° stability bound, and the constituent-mass gap machinery), [[F80-one-45deg-em-saturation-koide]] (closes the open problem below: the 45° unification + the EM selection rule), [[F69-paired-spinor-photon]] (the pairing channel); McPhee notebook pp.5–6 ("the Higgs is the Cooper pair").

---

## 1. The two questions F76 left

F76 found the charged-lepton masses obey Koide $Q=\sum m/(\sum\sqrt m)^2=2/3$ to
$10^{-5}$, read as: the vector $\sqrt m$ is the cubic $T_{1u}$ object, split into an
$A_{1g}$ democratic part and a $T_{1u}$ traceless part of **equal** length. It
left two things unexplained:

1. **Why $\sqrt m$** (not $m$) is the vector coordinate.
2. **Why the equipartition amplitude is $\sqrt2$** (i.e. why $Q$ is *exactly* $2/3$).

---

## 2. Part A — $m=y^2$ from the Cooper-pair bilinear (derivation)

The project already treats the symmetry-breaking sector as superconductor-like:
the physical scalar is a **Cooper pair** (F73/F74, McPhee pp.5–6), a spin-0
condensate of two spin-½ constituents. Apply the *same* premise to the source
of fermion mass: generation $a$'s mass is set by a **pair condensate**, a
bilinear in the constituent amplitude $y_a$,

$$m_a \;\propto\; \langle y_a\,y_a\rangle \;=\; y_a^{\,2}.$$

The constituent amplitude $y_a$ is the object that carries the lattice
quantum numbers — in particular it is the **$T_{1u}$ vector** of F75/F76 (one
component per orthorhombic axis, F76-C1). Therefore

$$\boxed{\;\sqrt{m_a} \;=\; y_a \;=\; \text{the } T_{1u}\text{ vector component on axis } a\;}$$

and **Koide is a statement about $y$, not about $m$** — exactly because mass is
*quadratic* in the fundamental pairing amplitude. This is the cleanest reason
the relation lives in $\sqrt m$: the same "mass = bilinear condensate" logic
that makes the Higgs a Cooper pair makes the fermion mass the square of a
vector amplitude.

**Test A1.** With $m_a=y_a^2$, $Q$ in $y$-language is $\sum y^2/(\sum y)^2 = 0.666661$ ✓.

**Test A2 (the data pick the bilinear).** Generalise to $u_a=m_a^{\,s}$ and ask
which power makes the relation a clean rational. The participation ratio
$1/Q(s)=(\sum m^s)^2/\sum m^{2s}$ equals the simple value $3/2$ **only at
$s=\tfrac12$** ($1.500014$), and is far from any clean rational at the neighbours
($s=\tfrac13\!:1.834$, $s=1\!:1.119$). The data independently single out the
square-root (bilinear) variable — corroborating $m=y^2$ rather than assuming it.

---

## 3. Part B — what the equipartition amplitude actually is

### 3.1 Three exact, equivalent characterisations of $Q=2/3$

In $y$-space, write $\mathbf y = (\text{A}_{1g}\text{ part along }\hat n) + (\text{T}_{1u}\text{ part}\perp\hat n)$, $\hat n=(1,1,1)/\sqrt3$. Then (B1, B2):

$$Q=\tfrac23 \iff |A_{1g}|=|T_{1u}| \iff \mathrm{CV}(y)\equiv\frac{\sigma_y}{\bar y}=1 \iff \angle(\mathbf y,\hat n)=45^\circ.$$

Measured: $|A_{1g}|^2/|T_{1u}|^2 = 1.00002$, $\mathrm{CV}=0.99999$, angle $44.99974^\circ$.

### 3.2 The new exact framing: $2/3$ is the *midpoint* of the allowed range (B1)

For any non-negative amplitudes, $Q=\sum y^2/(\sum y)^2$ is bounded:

$$\tfrac13 \;\le\; Q \;\le\; 1,\qquad
\begin{cases}Q=\tfrac13 & \text{fully democratic } y=(1,1,1)\ \text{(degenerate)}\\[2pt]
Q=1 & \text{fully hierarchical } y=(1,0,0)\ \text{(one mass)}\end{cases}$$

and the leptons sit at

$$Q=\tfrac23=\tfrac12\Big(\tfrac13+1\Big)\quad=\quad\textbf{the exact midpoint.}$$

So the equipartition amplitude $\sqrt2$ is precisely the value at which the
generation amplitudes are **maximally balanced between the democratic floor and
the single-axis ceiling** — equidistant, in $Q$, from "all generations equal"
and "only one generation exists." This is the sharpest model-independent
statement of what $\sqrt2$ *is*.

### 3.3 The honest negative: symmetric cube dynamics give $Q=\tfrac13$, not $\tfrac23$ (B3)

Does the lattice's own (flavour-symmetric) dynamics produce equipartition? No.
A mean-field NJL gap with a flavour-symmetric democratic coupling
$A_{ab}=(1-\kappa)\delta_{ab}+\tfrac{\kappa}{3}$ (the $O_h$-symmetric choice),
solved self-consistently from an asymmetric start, drives all three masses to a
**common value** (relative spread $<10^{-8}$): the gap solution is degenerate,
$Q\to\tfrac13$. A flavour-blind, cube-symmetric mass mechanism **cannot** make
the hierarchy — it lands on the democratic floor, the point *farthest* (in the
allowed range) from the observed $2/3$.

**Consequence:** equipartition is not a small correction to a symmetric vacuum;
it is a **large, specific symmetry-breaking** carrying the amplitude all the way
from the floor ($\tfrac13$) to the midpoint ($\tfrac23$). $\sqrt2$ is therefore
**not derived** by the symmetric model — it is a *critical* condition that some
explicit breaking must impose.

### 3.4 Why the cube's natural site symmetry can't be the breaking (B4)

The obvious residual symmetry — the cube's threefold body-diagonal site
symmetry $C_{3v}$ — is also ruled out as the source. A real mass operator
commuting with $C_{3v}$ is forced to the form $\mu\mathbb 1+\nu(\text{symmetric
circulant})$, whose eigenvalues are $\{\mu+2\nu,\,\mu-\nu,\,\mu-\nu\}$ — a
**$[2,1]$ degeneracy**. It *does* reach $Q=2/3$, and revealingly at
$\nu/\mu=1/\sqrt2$ (the $\sqrt2$ reappears), but with two $\sqrt$-masses equal
$(2.414,\,0.293,\,0.293)$ — one heavy, two degenerate. That is not three
distinct leptons. Three distinct masses require the lower **orthorhombic**
symmetry (F76-C1), and there the $\sqrt2$ is no longer fixed by any symmetry.

---

## 4. A suggestive (not derived) parallel: 45° here and 45° in F73

Two independent 45°'s have now appeared:

- **F73 (constituent stability):** a bound pair is stable up to constituent
  rotation $\arcsin m_c = 45^\circ$ ($m_c=1/\sqrt2$), where the rest-rotation
  and its complement are equal ($\sin=\cos=1/\sqrt2$) — *constituent-level
  equipartition*.
- **F77/F76 (generation):** the $\sqrt m$ vector sits at $45^\circ$ to the
  democratic axis — *generation-level equipartition*, $Q=2/3$.

Both are "$1/\sqrt2$ / 45° balance" conditions, and the same $\sqrt2$ surfaced
again in the $C_{3v}$ analysis (B4). This is a strong hint that the lepton
amplitude sits at a **critical/saturation point** of the same pairing dynamics
that bounds the F73 composite — but a rigorous map from the constituent-rotation
45° to the generation-vector 45° is **not** established here, and is flagged as
the key conjecture to close.

---

## 5. Test summary (`test_F78_koide_amplitude_pairing.py`, 2026-06-01 - 21:14)

| Check | Statement | Result | Status |
|---|---|---|---|
| A1 | $m=y^2$ reproduces Koide ($Q$ in $y$) | $0.666661$ | PASS |
| A2 | power $s=\tfrac12$ uniquely clean | $1/Q=1.500014$ ($s=\tfrac12$) vs $1.834,1.119$ | PASS |
| B1 | $Q=2/3$ = midpoint of $[\tfrac13,1]$ | floor $0.3333$, ceiling $1.0$, leptons $0.66666$ | PASS |
| B2 | equipartition identity | $|A_{1g}|/|T_{1u}|{=}1$, CV${=}1$, $45^\circ$ | PASS |
| B3 | symmetric gap is degenerate | spread $<10^{-8}$, $Q\to\tfrac13$ | PASS |
| B4 | $C_{3v}$ forces $[2,1]$; $\sqrt2$ at $\nu/\mu{=}1/\sqrt2$ | two equal $(2.414,0.293,0.293)$ | PASS |

**Overall 6/6 PASS.**

---

## 6. Verdict — what moved, what didn't

**Derived (Part A):** *Why $\sqrt m$.* Given the model's own Cooper-pair premise
(mass = condensate bilinear), the fermion mass is the **square** of the
constituent amplitude $y$, so the cubic $T_{1u}$ vector is $\sqrt m$ and Koide is
a statement about $y$. The data independently select the bilinear power
$s=\tfrac12$ (A2). This closes the open puzzle of F76.

**Characterised exactly (Part B):** $Q=2/3$ is the **midpoint of the allowed
range $[\tfrac13,1]$** — maximal democratic↔hierarchical balance — equivalently
$|A_{1g}|=|T_{1u}|$, CV$=1$, $45^\circ$.

**Still not derived:** the value $\sqrt2$ itself. The cube's *symmetric*
dynamics give the degenerate floor $Q=\tfrac13$ (B3), and its natural $C_{3v}$
site symmetry gives a $[2,1]$ degeneracy (B4) — neither yields three distinct
masses at the midpoint. So equipartition is a *critical, maximally-broken*
condition that requires an explicit ingredient the symmetric model does not
contain. The recurring $\sqrt2$/45° (B4, F73) hints this ingredient is the
**saturation/criticality of the pairing dynamics**, but the constituent-45° →
generation-45° map is the open conjecture.

**The open problem, now sharpened to one sentence:** show that the lepton
pairing condensate is driven to the *critical midpoint* $Q=\tfrac23$ (the $\sqrt2$
saturation) by the same dynamics that cap the F73 bound pair at
$\arcsin m_c=45^\circ$ — and explain why only the charged leptons sit there
($Q_\text{up}=0.85$, $Q_\text{down}=0.73$ do not).

---

## 7. Provenance

- Part A applies the F73/F74/F69 Cooper-pair premise to fermion-mass
  generation; the $m=y^2 \Rightarrow \sqrt m$ identification and the $s=\tfrac12$
  data selection are new.
- Part B's range-midpoint framing of $Q=2/3$, the symmetric-gap degeneracy, and
  the $C_{3v}$ $[2,1]$ result are new.
- Verification: `model-tests/test_F78_koide_amplitude_pairing.py`
  (2026-06-01 - 21:14, 6/6 PASS), results `test-results/F78_koide_amplitude_pairing.json`.
