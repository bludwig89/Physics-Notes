# F165 — Hypercharge quantisation: the SM Y-values are forced, up to one normalisation

> **[SUB-CLAIM SUPERSEDED 2026-08-02 by F279 — ledger S13-F279-hypercharge-attribution]**
>
> **DEAD:** Two steps INSIDE the finding, not its conclusion. (1) Section 2 lists the [grav]^2 U(1) anomaly as one of five independent constraints; it is not -- once nu_R is carried as a field with a hypercharge and its own Dirac mass step, the grav row is identically satisfied by the other five, and F165 reached dimension 1 only by omitting nu_R from the gravitational trace, which is numerically identical to imposing y_nu = 0 without saying so. (2) The attribution of what closes the system.
>
> **STILL LIVE:** EVERYTHING F165 CONCLUDES. The hypercharges ARE forced up to one overall normalisation; the ratios 1:4:-2:-3:-6 stand; y_phi = 3 y_Q stands; the normalised values reproduce the F38 table and the SM electric charges over Q; the residual input is one charge unit, not five values; y_u = y_Q + y_phi is genuinely OUTPUT by the [SU(3)]^2 U(1) row; and the single shared mass phase (F27/F41) is correctly identified as load-bearing.
>
> **NOTE:** The closing constraint is the F47 Higgs-free Majorana step, not the gravitational anomaly. This is the finding whose contradiction with Claims-and-Falsifiers revision 2 -- asserted on the same day -- is the reason the claims layer (D12) exists. Carried live as claim card CL010.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-06-29 - 16:59
**Status:** Confirmed — exact-rational derivation; 4/4 checks PASS over ℚ (literal integer zero, not float)
**Modules touched:** none (analytical study + verification harness only)
**Verification script:** `tests/findings/test_hypercharge_quantisation.py`
**Result file:** `test-results/hypercharge_quantisation.json`

> ## ⚠ Partially superseded by [F279](F279-hypercharge-constraint-attribution.md) (2026-08-02, S13)
>
> **The conclusion of this finding stands in full** — the hypercharges are forced up to one
> overall normalisation, the ratios $1:4:-2:-3:-6$ are right, $y_\phi=3y_Q$, the normalised
> values reproduce the F38 table and the SM electric charges over ℚ, the residual is one
> charge unit rather than five values, the up-type relation $y_u=y_Q+y_\phi$ really is
> *output* by the $[SU(3)_c]^2U(1)$ row, and the single shared mass phase really is
> load-bearing. F279 re-derived all of it independently and it all holds.
>
> **Two steps below are wrong.**
>
> 1. **§2 — the $[\text{grav}]^2U(1)$ row is not an independent constraint.** The system
>    below omits $\nu_R$. Carry it (the model has one — F47's see-saw needs it, and
>    `hypercharge.py` encodes its conjugate mass phase) and the grav row becomes *identically*
>    satisfied by the other five: rank 5 with it and without it. The remaining system is
>    **two-dimensional**, with $y_Q$ and $y_\phi$ both free. This finding reached dimension 1
>    only by leaving $\nu_R$ out of the gravitational trace, which is numerically identical to
>    imposing $y_\nu=0$ without saying so.
>
>    **What actually closes the system is the F47 Majorana step:** $\nu_R^{\mathsf T}C\nu_R$
>    carries hypercharge $2y_\nu$, so gauge invariance of that term forces $y_\nu=0$ exactly.
>    Adding that row gives rank 6, dimension 1, and this finding's line — with *both* the grav
>    and cubic anomalies then identically zero on it, i.e. two consistency checks rather than
>    one. The corrected route is **stronger**: it rests on the model's own Higgs-free see-saw
>    rather than on the imported Minahan–Ramond–Warner / Geng–Marshak theorem.
>
> 2. **§3 — the colour claim is false.** "Remove colour … and the system no longer closes to a
>    single line" is not true. It closes to a one-dimensional line for **every** $N_c$, with
>    ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$ (checked at $N_c=1{-}5$ and symbolically), and the
>    cubic anomaly vanishes identically for every $N_c$. Commensurability is derived for any
>    $N_c$; that the unit is a **third** is $N_c=3$, which this model takes as an input.
>
> Read §2 and §3 below with those corrections applied. Everything else is current.

Closes the audit gap **G4** (`docs/audits/physics-audit-report-2026-06-29.md`, §G4 / next-step 5): *"charge quantisation not derived — the specific charge assignments (Y_L=−1, Y_eR=−2, Y_Q=+1/3, …) are SM values put in by hand."* This finding shows they are **not** free inputs: given the lattice-fixed representation content, the five generation hypercharges are the **unique** solution — up to a single overall normalisation — of anomaly cancellation together with mass-step gauge invariance.

---

## 1. Claim

[F51](F51-bipartite-sublattice-hypercharge.md) fixes *which* degree of freedom carries U(1)_Y (the bipartite sublattice parity) and that its bare charge is $q_P=\pm1$. [F38](F38-fg1-anomaly-cancellation.md) verifies the SM Y-values cancel all six anomalies exactly — but treats those values as adopted. The open question (G4) is whether the **values themselves** are forced by the structure or are independent inputs.

They are forced. Let the one-generation left-handed Weyl content carry standard weak hypercharges $y$ (with $Q=T_3+y$; F38 quotes $Y=2y$ in the $Q=T_3+Y/2$ convention). The constraint system

$$
\begin{aligned}
[SU(2)_L]^2\,U(1):&\quad 3\,y_Q + y_L = 0,\\
[SU(3)_c]^2\,U(1):&\quad 2\,y_Q - y_u - y_d = 0,\\
[\text{grav}]^2\,U(1):&\quad 6\,y_Q - 3\,y_u - 3\,y_d + 2\,y_L - y_e = 0,\\
\text{down-type mass step }(Q,d):&\quad y_d = y_Q - y_\phi,\\
\text{lepton mass step }(L,e):&\quad y_e = y_L - y_\phi,
\end{aligned}
$$

in the six unknowns $(y_Q,y_u,y_d,y_L,y_e,y_\phi)$ has a **one-dimensional** solution space over ℚ — a line through the origin. Every hypercharge is therefore fixed up to one common scale. The pure-cubic $U(1)^3$ anomaly is satisfied **identically** on that line (a consistency check, not a sixth constraint). The ratios are

$$
y_Q : y_u : y_d : y_L : y_e \;=\; 1 : 4 : -2 : -3 : -6 \qquad(\text{with } y_\phi = 3\,y_Q).
$$

Normalising $y_Q=\tfrac16$ reproduces the SM exactly: $y=(\tfrac16,\tfrac23,-\tfrac13,-\tfrac12,-1)$, i.e. the F38 table $Y=(\tfrac13,\tfrac43,-\tfrac23,-1,-2)$, and the Gell-Mann–Nishijima electric charges $Q_u=+\tfrac23,\ Q_d=-\tfrac13,\ Q_\nu=0,\ Q_e=-1$.

---

## 2. Where each constraint comes from in the model

Nothing here is a continuum import that the lattice merely echoes; each equation is sourced by a structural fact the model already establishes.

**Representation content (the inputs that are lattice-fixed, not free).**

- *Colour triplet* (the factor of $3$ in the SU(2)²U(1) and grav traces, and the $\dim_2$ weights in SU(3)²U(1)): the quark sector is a genuine $SU(3)_c$ triplet — [F136](F136-colour-triplet-dirac-quark-confinement.md)/[F71](F71-colour-singlet-baryon-proton.md).
- *SU(2)_L doublet/singlet split* (which fields are doublets, which singlets): the cell isospin SU(2) of [F34](F34-wmu-fermion-vertex.md)/[F35](F35-electroweak-mixing.md).
- *The abelian carrier* on which all $y$ live: the F51 sublattice $U(1)_Y$, unique at $s=2$ minimality.
- *Generation content* (one full generation, count = 3): [F75](F75-three-generations-from-bcc-irrep-selection.md).

**The five equations.**

1–3, the **anomaly** rows, are the linear members of the same six traces F38 evaluates; their group-theoretic coefficients ($A(\mathbf 3)=+1$, $T(\text{fund})=\tfrac12$, $A(SU(2)\text{ rep})=0$) are fixed by the reps above.
4–5, the **mass-step** rows, are the Higgs-free analogue of Yukawa gauge invariance: the [F41](F41-hypercharge-higgs-free-su2.md) field $U(x)$ carries a single hypercharge phase $y_\phi$ that connects each left-handed doublet to its right-handed singlet through the [F27](F27-complex-mass-chiral-su2.md) mass step. Gauge-neutrality of that connection is exactly $y_d=y_Q-y_\phi$ (down/quark) and $y_e=y_L-y_\phi$ (lepton). The up-type relation $y_u=y_Q+y_\phi$ is **not** assumed — it is *output* by the SU(3)²U(1) anomaly row, which is why a single Higgs-free phase suffices.

So the only genuinely "by hand" number left is the overall scale $y_Q$ — the **unit of charge**. That is a normalisation (it sets the U(1)_Y coupling relative to charge), not a quantisation: it does not tell you the spectrum is discrete or commensurate; the derivation does.

---

## 3. Why this *is* charge quantisation

The physical content is that quark charges are forced to be fractional **because there are three colours**: the row $3y_Q+y_L=0$ locks the quark-doublet hypercharge to one-third of (minus) the lepton-doublet hypercharge, and the colour-3 multiplicity in the grav and cubic traces is what makes the leptonic and hadronic contributions cancel only at these specific rationals. Lepton charges are integers and quark charges are thirds **of the same unit** — that commensurability is the derived statement, and it is exact over ℚ. Remove colour (set the multiplicity to 1) and the system no longer closes to a single line; the fractional values are a consequence of the lattice's colour structure, not an input.

This is the lattice realisation of the known SM result (Minahan–Ramond–Warner; Geng–Marshak; Babu–Mohapatra) that anomaly freedom plus one Yukawa per charged sector quantises hypercharge. The model's contribution is that it **independently supplies the representation content** those theorems take as given, so the residual freedom collapses from five numbers to one.

---

## 4. Verification summary

Script `tests/findings/test_hypercharge_quantisation.py`, results `test-results/hypercharge_quantisation.json`. All arithmetic via `sympy.Rational` — residuals are literal integer $0$ (cf. F38 §5), not floats near zero.

| Test | Statement | Type | Result |
|------|-----------|------|:------:|
| Q1 | Linear constraint system has a **1-dimensional** solution space | exact (ℚ nullspace) | PASS |
| Q2 | $U(1)^3$ anomaly is identically $0$ on that line (no extra constraint) | exact (ℚ) | PASS |
| Q3 | Normalised $Y$ ($y_Q=\tfrac16$) reproduces the F38 table exactly | exact (ℚ) | PASS |
| Q4 | GMN electric charges are $(\tfrac23,-\tfrac13,0,-1)$ | exact (ℚ) | PASS |

---

## 5. What this derives and what it does not

**Derived (this finding):**

- The five generation hypercharges are **not** independent: anomaly cancellation + mass-step gauge invariance, on the lattice-fixed reps, leave a one-parameter solution line (Q1).
- The line is exactly the SM ratios $1:4:-2:-3:-6$; normalising one scale gives the F38 values and the measured electric charges over ℚ (Q3, Q4).
- Fractional quark charges are forced by the colour-3 multiplicity — the structural origin of charge quantisation in the model.

**Still an input (one number, not five):**

- The overall normalisation $y_Q$ = the **unit of electric charge** / U(1)_Y coupling normalisation. This is the Weinberg-angle / $\alpha$ question, *not* a quantisation question: the relative coupling $g'^2/g^2$ is [F49](F49-bcc-finite-k-weinberg-angle.md)'s separate, still-partial $2/7\to\sin^2\theta_W=2/9$ problem, and the absolute scale $e$ is the fine-structure constant.

**Assumed upstream (rep content, supplied by other findings):**

- Colour-triplet quarks ([F136](F136-colour-triplet-dirac-quark-confinement.md)/[F71](F71-colour-singlet-baryon-proton.md)), SU(2)_L doublet structure ([F34](F34-wmu-fermion-vertex.md)/[F35](F35-electroweak-mixing.md)), the F51 carrier, the F27/F41 single mass-phase, and generation content ([F75](F75-three-generations-from-bcc-irrep-selection.md)). The derivation is conditional on these; it does not re-derive them.

Net effect on G4: the gap moves from *"five Y-values put in by hand"* to *"one charge-unit normalisation put in by hand"* — the other four ratios, and charge quantisation itself, are now derived.

---

## 6. Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| [F38](F38-fg1-anomaly-cancellation.md) | Supplies the six anomaly traces; F165 uses their linear members as constraints and shows the values F38 *adopted* are the unique solution. |
| [F51](F51-bipartite-sublattice-hypercharge.md) | Fixes the carrier ($q_P=\pm1$); F165 fixes the values that carrier takes. |
| [F41](F41-hypercharge-higgs-free-su2.md)/[F27](F27-complex-mass-chiral-su2.md) | The single $U(x)$ mass phase $y_\phi$ is the source of the two mass-step rows; the up-type relation is anomaly output, so one phase suffices. |
| [F49](F49-bcc-finite-k-weinberg-angle.md) | Owns the residual normalisation as the coupling ratio $\sin^2\theta_W$; F165 leaves that untouched. |
| [F75](F75-three-generations-from-bcc-irrep-selection.md) | Generation content the trace multiplicities assume. |

---

## 7. Files

- `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md` — this finding
- `tests/findings/test_hypercharge_quantisation.py` — Q1–Q4 verification
- `test-results/hypercharge_quantisation.json` — exact-rational output

---

*End of finding.*
