# F76 — The generation mass hierarchy: a crystal-field splitting of the F75 $T_{1u}$ triplet, and the Koide relation as its cubic-vector signature

**Date:** 2026-06-01 - 20:41
**Status:** Candidate — 6/6 checks PASS. **Two tiers of claim, kept strictly separate:** the *structural* results (C1 splitting pattern, C4 equipartition identity) are exact; the *numerical* results (C3 Koide $Q=2/3$, C5 $m_\tau$ prediction, C6 $Z_3$ reconstruction) are the empirical charged-lepton Koide relation re-expressed in the model's cubic language. The amplitude $\sqrt2$ ($\Leftrightarrow Q=2/3$) and the phase $\delta$ are **inputs, not derived** from the QCA rule. Quarks/neutrinos are **not** fit. See §6.
**Module:** none new. **Test:** `model-tests/test_F76_generation_hierarchy.py`; results `test-results/F76_generation_hierarchy.json`.
**Cross-references:** F75 (generation count = $T_{1u}$ triplet — this is its hierarchy follow-up), F46 (mass as $\Omega_\text{rest}=\arcsin m$ rotation), F69/F73 (bound-pair fermion → motivates $\sqrt m$ as the fundamental amplitude), F30/F37 (BCC anisotropy — the physical origin of an axis-splitting field).

---

## 1. The gap F75 left

F75 fixed the generation **count** at three (the unique odd-parity cubic
triplet $T_{1u}$) but left the three states **degenerate** — at the fully
$O_h$-symmetric point they share one mass. The observed hierarchy
$m_e:m_\mu:m_\tau \approx 1:207:3477$ must come from a **symmetry-lowering
("crystal-field") perturbation** that splits $T_{1u}$. This finding asks two
questions: *what splitting pattern does the cubic geometry allow*, and *do the
measured lepton masses fit it*.

---

## 2. C1 — Three distinct masses force an orthorhombic break (exact)

The $T_{1u}$ mass operator is a real-symmetric $3\times3$ matrix acting on the
vector components $(x,y,z)$. Counting distinct eigenvalues as the symmetry is
lowered:

| Vacuum symmetry | mass operator | level pattern | distinct masses |
|---|---|---|---|
| cubic $O_h$ | $m_0\,\mathbb 1$ | $[3]$ | 1 (F75 degenerate triplet) |
| tetragonal $D_{4h}$ (one axis) | $\mathrm{diag}(a,a,b)$ | $[2,1]$ | 2 |
| **orthorhombic $D_{2h}$** (three axes) | $\mathrm{diag}(a,b,c)$ | $[1,1,1]$ | **3** |

So **three non-degenerate generations require breaking all the way to three
inequivalent axes**: $T_{1u}\to B_{1u}\oplus B_{2u}\oplus B_{3u}$. This is a
structural prediction — the three generations are the **three orthorhombic axes
$x,y,z$** of a triaxially-distorted cubic vacuum. (A merely tetragonal
distortion would predict two light generations degenerate and one split off —
not what is observed.) A natural physical source of such a field already exists
in the project: the BCC dispersion is anisotropic (F30/F37), and any vacuum
strain that distinguishes the three body-diagonal/face directions supplies the
$D_{2h}$ field.

---

## 3. C2 — A *linear* crystal field cannot do it (exact, negative)

The obvious mechanism — a perturbation linear in the mass, $m_a = m_0 + \lambda\,\varepsilon_a$
with $\sum_a \varepsilon_a = 0$ — fails quantitatively. The fit forces
$m_0 = \overline m = 627.7$ MeV and splits $(-627,-522,+1149)$ MeV, so

$$\frac{\max_a|m_a-\overline m|}{\overline m} = 1.83 \;>\; 1.$$

The "splitting" is *larger than the mean*: this is not a perturbation, and a
crystal field linear in $m$ cannot generate ratios of $\sim\!200$ and
$\sim\!3500$. The hierarchy is not a small distortion of a degenerate level —
the correct variable must be one in which the three values are an $O(1)$
spread, not a huge one.

---

## 4. C3–C4 — The cubic vector lives in $\sqrt m$: Koide $Q=2/3$ is equipartition (exact identity + spectacular data match)

The variable that works is $\sqrt m$. Define the vector
$\mathbf s = (\sqrt{m_e},\sqrt{m_\mu},\sqrt{m_\tau})$ and split it into its
cubic-invariant ($A_{1g}$, along the democratic axis $\hat n=(1,1,1)/\sqrt3$)
and traceless ($T_{1u}$ triplet) parts:

$$\mathbf s = \underbrace{(\mathbf s\!\cdot\!\hat n)\,\hat n}_{A_{1g}\text{ scalar}} \;+\; \underbrace{\mathbf s_\perp}_{T_{1u}\text{ splitting}}.$$

**Exact identity (C4):** the angle $\theta$ between $\mathbf s$ and $\hat n$ obeys

$$\cos^2\theta = \frac{(\sum_a\sqrt{m_a})^2}{3\sum_a m_a} = \frac{1}{3Q},\qquad
Q \equiv \frac{\sum_a m_a}{(\sum_a\sqrt{m_a})^2}.$$

Koide's $Q=\tfrac23$ is therefore **exactly the equipartition condition**
$\cos^2\theta=\tfrac12$, i.e. $\theta=45^\circ$, i.e.
$|A_{1g}|^2=|T_{1u}\text{ triplet}|^2$: the cubic-scalar part and the
symmetry-breaking part of $\sqrt m$ carry **equal weight**.

**Data (C3):** for the measured charged leptons,

$$Q = 0.6666605,\qquad |Q-\tfrac23| = 6.2\times10^{-6}\ \ (0.91\,\sigma\ \text{from the } m_\tau\text{ uncertainty}),$$

and the equipartition reads $\theta = 44.99974^\circ$, ratio
$|A_{1g}|^2/|T_{1u}|^2 = 1.00002$. The charged leptons sit on the
equipartition point to one part in $10^5$.

---

## 5. C5–C6 — Falsifiable: the cubic structure predicts the third mass

Because $Q=\tfrac23$ plus two masses overdetermines the third, the structure is
predictive.

**C5 (Koide $m_\tau$ prediction).** Enforcing $Q=\tfrac23$ and feeding in
$m_e,m_\mu$:

$$m_\tau^\text{pred} = 1776.97\ \text{MeV}\quad\text{vs}\quad m_\tau^\text{PDG}=1776.86\pm0.12\ \text{MeV},\qquad \text{rel. error } 6.1\times10^{-5}.$$

The prediction is *better than* the historical input precision and within
$\sim\!1\sigma$ of the current PDG value. Predicting $m_e$ from $(m_\mu,m_\tau)$
gives $0.5106$ MeV vs $0.5110$ MeV ($7\times10^{-4}$).

**C6 ($Z_3$ cube parametrisation).** Equipartition + the cube's threefold
($Z_3$ body-diagonal) structure is the statement

$$\sqrt{m_a} = M_0\big[\,1 + \sqrt2\,\cos(\delta + \tfrac{2\pi a}{3})\,\big],\qquad a=0,1,2,$$

— the constant is the $A_{1g}$ scalar, the $\sqrt2$ amplitude is the
equipartition ($Q=\tfrac23$) condition, and the $2\pi/3$ phases are the three
cube body-diagonals. Fitting $(M_0,\delta)$ to $(m_e,m_\mu)$ reconstructs
$m_\tau = 1776.94$ MeV ($4.4\times10^{-5}$).

---

## 6. What is derived, what is fit, what fails (read this)

**Derived / exact (structure):**
- C1 — that three distinct masses require an orthorhombic ($D_{2h}$) break,
  $T_{1u}\to B_{1u}\oplus B_{2u}\oplus B_{3u}$ — generations $\leftrightarrow$ the three axes.
- C2 — that a mass-linear crystal field is excluded (non-perturbative).
- C4 — the identity $Q=2/3 \Leftrightarrow$ equipartition of $\sqrt m$ between
  its $A_{1g}$ and $T_{1u}$ parts ($45^\circ$). This *reframes* Koide as a
  cubic-geometry statement.

**Empirical input, not derived (the honest core):**
- The amplitude $\sqrt2$ — equivalently $Q=\tfrac23$ exactly — is **not derived**
  from the QCA rule. The construction explains *that there is one amplitude and
  one phase*; it does not yet explain *why the amplitude is $\sqrt2$*. Saying
  "equipartition" is suggestive (equal weight to the symmetric and
  symmetry-breaking parts) but is a principle imposed, not proven.
- The phase $\delta$ is a free fit parameter (the orientation of $\mathbf s_\perp$
  in the plane $\perp\hat n$). It is what is fixed by using a second measured mass.
- So the model currently *predicts the functional form* ($\sqrt m$ = cubic
  vector with $Z_3$ phases) and turns three masses into **one scale + one
  amplitude + one phase**; the amplitude is the lone unexplained pure number.

**Why $\sqrt m$ and not $m$?** Motivated, not proven: if the physical fermion is
a **bound pair** (the project's recurring theme — F69 paired-spinor photon, F73
spin-0 bound pair), its mass is second-order in a fundamental amplitude, so the
amplitude $\sim\!\sqrt m$ is the object that transforms as the $T_{1u}$ vector.
Making this precise (deriving $m\propto(\text{amplitude})^2$ and the $\sqrt2$
from the pairing dynamics) is the key open step.

**What fails / is not claimed:** the up-type ($Q=0.849$) and down-type
($Q=0.731$) quarks do **not** satisfy $Q=\tfrac23$, and neutrinos are
unconstrained here. The charged leptons are the clean case (as in the wider
Koide literature). This construction therefore does **not** yet explain the
quark hierarchy — a single universal cubic mechanism would have to say why only
the charged-lepton sector equipartitions. Open.

---

## 7. Test summary (`test_F76_generation_hierarchy.py`, 2026-06-01 - 20:41)

| Check | Statement | Result | Tier | Status |
|---|---|---|---|---|
| C1 | $T_{1u}$ split: cubic/tetragonal/orthorhombic | $[3]\,/\,[2,1]\,/\,[1,1,1]$ | exact | PASS |
| C2 | linear-$m$ crystal field | $\max\lvert\Delta\rvert/\overline m = 1.83$ (non-pert.) | exact (neg.) | PASS |
| C3 | Koide $Q$ (charged leptons) | $0.6666605$, $0.91\sigma$ from $2/3$ | quantitative | PASS |
| C4 | $Q=2/3 \Leftrightarrow$ equipartition | $\theta=44.99974^\circ$, ratio $1.00002$ | exact identity | PASS |
| C5 | predict $m_\tau$ from $(m_e,m_\mu)$ | $1776.97$ vs $1776.86$ MeV ($6.1\times10^{-5}$) | quantitative | PASS |
| C6 | $Z_3$ cube parametrisation | reconstruct $m_\tau$ to $4.4\times10^{-5}$ | quantitative | PASS |

**Overall 6/6 PASS** (<1 s). Context: quark $Q_\text{up}=0.849$, $Q_\text{down}=0.731$ (not $2/3$).

---

## 8. Verdict

The cubic geometry **does** dictate the *shape* of the hierarchy: three
generations must split orthorhombically into a $\sqrt m$ vector whose
cubic-scalar and triplet parts are the two physical pieces, and the
charged-lepton masses obey this to $10^{-5}$ — with the long-standing Koide
$m_\tau$ prediction falling out as the cubic-vector consistency condition. What
the lattice does **not** yet hand us is the single number $\sqrt2$ (the
equipartition amplitude, $Q=2/3$) and the phase $\delta$; pinning $\sqrt2$ to
the bound-pair ($m\propto$ amplitude$^2$) dynamics, and explaining why only the
charged leptons equipartition, are the two open problems this finding sharpens.

---

## 9. Provenance

- Builds directly on F75 (the $T_{1u}$ triplet). The crystal-field reading and
  the identification of Koide $Q=2/3$ with $\sqrt m$-equipartition in the cubic
  $A_{1g}\oplus T_{1u}$ basis are the new content.
- Verification: `model-tests/test_F76_generation_hierarchy.py`
  (2026-06-01 - 20:41, 6/6 PASS), results `test-results/F76_generation_hierarchy.json`.
- Masses: PDG (m_e, m_mu exact-ish; m_tau $1776.86\pm0.12$ MeV).
