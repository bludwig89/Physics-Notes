# F92 — The per-constituent phase identification as a consistency fixed point: the chain's two mass laws are jointly satisfiable only at 45°, and the data pin the pair normalization to the Fock $\sqrt2$

**Date:** 2026-06-04 - 20:35
**Status:** Partial (closing) — 5/5 checks PASS. **What is derived (exact):** the model's two established mass laws — F73's pair-sum kinematics $m=\sin 2t$ and F78's bilinear premise $m=y^2$ — are *jointly satisfiable at exactly one angle*, $t=45°$, given the standard two-quantum Fock normalization $y=\sqrt2\sin t$; the F73 stability cap $m_c\le1/\sqrt2$ is re-derived as **unitarity of the pair amplitude** ($y\le1$); and the "mass amplitude = sine of a rest rotation" reading is grounded in the model's own code (the F27 mass step allocates $(\cos t,\sin t)$ exactly). **What this changes:** F84's irreducible input #1 ("the generation polar angle $\phi$ is the constituent rest-phase") no longer needs to be assumed *and then* driven to 45° by energetics — the identification and the 45° location collapse into a single self-consistency statement whose only new input is the Bose pair factor $\sqrt2$, which the measured lepton masses pin to $c^2=2$ at the $10^{-5}$ level. **What remains:** a derivation from the QCA update rule of *why* the generation-space angle participates in the pair phase budget at all. See §6.
**Script:** `model-tests/test_F92_per_constituent_phase.py` (<1 s)
**Results:** `test-results/F92_per_constituent_phase.json`
**Cross-references:** [[F84-flatness-from-orthorhombic-break]] (irreducible input #1, the target), [[F81-why-45deg-pair-phase-saturation]] (identification (b) this addresses), [[F82-why-saturation-composite-mass-peak]] (the energetic route this complements), [[F80-one-45deg-em-saturation-koide]] ($Q(\phi)$ map; the singlet-$1/\sqrt2$ conjecture this makes precise), [[F78-koide-amplitude-from-cooper-pair]] (the bilinear law L2), [[F73-spin0-bound-pair-scalar]] (the pair-sum law L1 and the $1/\sqrt2$ cap), [[F69-paired-spinor-photon]] (phase-sum rule), [[F46-pythagorean-lattice-mass]] ($m=\sin\Omega_\text{rest}$), [[F27-complex-mass-chiral-su2]] (the mass step exercised in P1), [[F93-orthorhombic-Eg-vacuum]] (the companion finding on input #2).

---

## 1. The target

F84 closed the F75→F84 descent on two irreducible structural inputs. Input #1:

> **The per-constituent identification** — the generation polar angle $\phi$ is
> the constituent rest-phase, so the composite mass is $m_H=\sin(2\phi)$.
> Strongly supported by the $N=2$ readout (F81-E2), but not derived from the
> QCA update rule.

This finding attempts the derivation. The honest outcome is not a derivation
from the update rule, but something almost as strong: the identification is
shown to be **the unique consistent joint solution of two laws the model has
already derived separately**, with the lone new input being a standard
quantum-mechanical normalization constant that the data independently confirm.

## 2. The two mass laws, and the consistency demand

The chain applies two different mass laws to the same composite object:

- **L1 (pair-sum kinematics — F73/F69, exact).** A bound pair of equal
  constituents with rest-phase $t$ each ($m_c=\sin t$, F46) has composite mass
  $$m_\text{comp}=\sin(t+t)=\sin 2t .$$
- **L2 (bilinear condensate — F78).** The composite mass is the square of the
  pair's constituent amplitude, $m_\text{comp}=y^2$.

For a **normalized** pair state, the two-quantum Fock amplitude is $\sqrt2$
times the single-quantum amplitude — $(a^\dagger)^2\lvert0\rangle=\sqrt2\,\lvert2\rangle$,
exact (P2) — so the pair's constituent amplitude is

$$y=\sqrt2\,\sin t .$$

Demanding L1 and L2 describe the same object:

$$2\sin^2 t=\sin 2t \iff \tan t=1 \iff \boxed{\,t=45°\ \ \text{(unique on }(0°,90°))\,}$$

verified symbolically (P3, sympy `solveset` returns exactly $\{\pi/4\}$), with
$Q(45°)=1/(3\cos^2 45°)=2/3$ exact. **The two laws are inconsistent at every
other angle.** The identification cannot hold anywhere except 45° — so
"identification (b) + sitting at saturation" was never two assumptions; it is
one consistency condition with one solution.

## 3. The F73 cap is unitarity of the pair amplitude (P4, exact)

The same normalization gives the stability cap a sharper meaning:

$$y=\sqrt2\,\sin t\le1 \iff t\le45° \iff m_c\le\tfrac1{\sqrt2},$$

which is *exactly* the F73 over-wrap bound, now read as: **the pair's bilinear
amplitude may not exceed the unit (unitarity) budget.** At $t=45°$ three
saturations coincide simultaneously and exactly: the pair amplitude fills the
budget ($y=1$), the composite mass peaks ($m_\text{comp}=\sin90°=1$), and the
pair phase fills $\pi/2$ (F81). "Sitting at saturation" (F82's energetic
statement) is equivalently "the pair amplitude exactly fills unitarity."

## 4. Grounding in the model's code (P1, exact)

The reading "mass amplitude = sine of a rest rotation" is not an analogy; it is
what the model's mass step does. Applied at $k=0$:

- `ca_dirac.mass_step_1flavor_u1` allocates $(\text{stay},\text{transfer})=(\cos t,\sin t)$
  with $t=m\,dt$ — residual $0.0$ (bit-for-bit);
- the F46 $D_k$ block (entries $n=\sqrt{1-m^2}$, $im$) allocates
  $(\cos t,\sin t)$ with $t=\arcsin m$ — residual $1.1\times10^{-16}$.

In both conventions the one-tick allocation between the kinetic ("stay") and
mass ("transfer") channels is a **unit 2-vector whose angle is the rest
phase**, forced by unitarity. The amplitude that F78 squares is the sine of a
rotation by construction of the model itself.

## 5. The data pin the normalization (P5)

Inverting the consistency condition with a general normalization $y=c\sin t$
gives $t^*(c)=\arctan(2/c^2)$:

| $c^2$ | $t^*$ | $Q^*=1/(3\cos^2 t^*)$ |
|---|---|---|
| 1 | $63.43°$ | $1.667$ |
| **2 (Fock)** | $\mathbf{45°}$ | $\mathbf{2/3}$ |
| 3 | $33.69°$ | $0.481$ |
| 4 | $26.57°$ | $0.417$ |

Only the Fock value $c^2=2$ lands on $45°$/$Q=2/3$. Running the logic in
reverse, the measured charged leptons ($\phi=44.99974°$) **measure** the
normalization:

$$c^2_\text{data}=2\cot\phi_\text{lepton}=2.000018,\qquad |c^2-2|=1.9\times10^{-5}.$$

The lepton mass spectrum independently returns the two-quantum Bose factor to
one part in $10^5$. This is the precise version of F80's conjecture that the
Cooper-pair singlet's $1/\sqrt2$ is behind the equipartition.

## 6. What moved, what remains (read this)

**Derived / exact:**
- The consistency theorem: L1 + L2 + Fock $\sqrt2$ ⟹ $t=45°$, unique (P3).
  This is a **third independent route to $Q=2/3$** (after F81's phase-budget
  split and F82's mass-peak energetics) — and the only one that does not
  *assume* the per-constituent identification but solves for where it can hold.
- The F73 cap as pair-amplitude unitarity, with the triple saturation at 45° (P4).
- The code-level grounding of "amplitude = sin(rest phase)" (P1).
- The Fock factor itself (P2) and the data pin $c^2=2\pm1.9\times10^{-5}$ (P5).

**Logical status change:** F84 input #1 is downgraded from a free structural
hypothesis to: *the generation-space angle obeys the same two mass laws as
every other pair in the model, and those laws have exactly one common point.*
The 45° is no longer where the lepton "happens to sit"; it is the only angle at
which the chain is not self-contradictory.

**Still not derived (the honest residual):** why the **generation-space**
(A$_{1g}$/T$_{1u}$) angle is subject to the pair phase-sum rule at all — i.e.
the bridge from the per-tick chirality allocation (P1, a statement about one
constituent's internal plane) to the collective flavor-space vector. The
consistency theorem constrains this bridge to a single point but does not
build it from the update rule. That build — a flavor-resolved pairing
simulation in which the condensate's (common, differential) decomposition is
*measured* rather than posited — is the remaining step.

**Falsifiable handle:** $c^2=2\cot\phi$ is a measurement. A future shift in
$m_\tau$ moves $\phi$; the prediction is that improved data keep
$c^2\to2$ exactly (currently $0.91\sigma$-limited by $m_\tau$, same as Koide).

## 7. Test summary (`test_F92_per_constituent_phase.py`, 2026-06-04 - 20:31)

| Check | Statement | Result | Status |
|---|---|---|---|
| P1 | mass step allocates $(\cos t,\sin t)$, unit 2-vector | code $0.0$; $D_k$ $1.1\times10^{-16}$ | PASS |
| P2 | $(a^\dagger)^2\lvert0\rangle=\sqrt2\lvert2\rangle$ | residual $0$ (sympy) | PASS |
| P3 | $2\sin^2t=\sin2t$ unique at $\pi/4$; $Q=2/3$ | exact ($\{\pi/4\}$, $2/3$) | PASS |
| P4 | F73 cap $=$ pair-amplitude unitarity; triple saturation | exact ($1/\sqrt2$, $1$, $1$) | PASS |
| P5 | $t^*(c)=\arctan(2/c^2)$; data pin $c^2$ | $c^2_\text{data}=2.000018$ | PASS |

**Overall 5/5 PASS** (<1 s).

## 8. Provenance

- New content: the L1+L2 consistency theorem and its uniqueness; the
  unitarity reading of the F73 cap; the $c^2=2\cot\phi$ data pin; the P1
  code-level grounding. Builds directly on F73/F78/F80/F81/F82/F84.
- Verification: `model-tests/test_F92_per_constituent_phase.py`
  (2026-06-04 - 20:31, 5/5 PASS), results
  `test-results/F92_per_constituent_phase.json`.
- Masses: PDG ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV).
