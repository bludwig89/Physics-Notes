# F79 — Newton's constant from the lattice structure itself: freeing $G$ from the Sakharov premise, verifying the loop channel, and the closed form

**Date:** 2026-06-02 - 02:35
**Status:** Candidate finding — 6/6 checks PASS. The channel-selection argument (S3/S4) and the structural mode count (S5) are **exact** (machine-precision tracelessness, exact rationals, exact integers); the assembled closed form (S6) is **exact-algebraic given its three structural inputs**. The one honest limit is dimensional: the model predicts the *dimensionless* number $a/\ell_P$, not a dimensionful $G$ from pure numbers (no theory can — that needs one ruler). See §6.
**Module:** `ca-simulation/forks/gr_fork_F79_structural_G.py` (self-contained; numpy + fractions, real arithmetic).
**Tests:** `model-tests/test_F79_structural_G.py`; results `test-results/F79_structural_G.json`.
**Cross-references:** [[F56-einstein-coupling-from-lattice-phase-matching]], [[F57-induced-eh-term-from-leg-field-backreaction]], [[F58-clockrate-coupling-from-neighbour-rule]], [[F59-induced-eh-prefactor-and-f10-selection]], [[F60-induced-G-channel-reconciliation]] (the channel fork this closes non-circularly), [[F61-weyl-eta-and-gstar-prefactor]] ($\eta=1/12$, $g_*$), [[F64-em-connection-gravity]] (D-EM5 conformal-factor derivation; D-EM10 G-pinning this replaces), [[F75-three-generations-from-bcc-irrep-selection]] (makes $g_*$ structural), F38 (anomaly-free content), [[f41-hypercharge-higgs-free]], F47 ($\nu_R$).

---

## 1. The three questions

1. **Free the gravity sector from the Sakharov premise.** F56–F61 read $1/G$ off the
   Einstein–Hilbert term *induced* by integrating out matter modes. That treats the
   matter fields as an external ingredient one "integrates out", and F60 had to
   *choose* the loop channel over F58's tree channel by invoking "the project's
   emergent-gravity commitment — a stated premise, not a theorem."
2. **Verify the choice of loop channel is correct.** F58 (tree) gives $1/G\propto c_\text{lat}^2$;
   F59/F60 (loop) give $1/G\propto 1/c_\text{lat}$. They differ by $c_\text{lat}^3$. Which is physical?
3. **Derive Newton's constant $G$.**

This finding answers all three from one observation: **the gravity field $K(x)$ is not a
fundamental field on the lattice — it is a reparametrization of the $(\mathbf E,\mathbf B)$
rotation rule (F64 D-EM5), so it carries no bare kinetic term, and its entire stiffness is
forced to be the induced response.** That dissolves the premise (1), forces the loop channel
as a theorem rather than a preference (2), and — with $g_*$ now structural via F75 — assembles
$1/G$ from inputs that are all fixed by the lattice (3).

---

## 2. The pivot: $K$ is a conformal factor, not a field (S3 — exact)

F64 D-EM5 established that gravity enters as a single dielectric index $K(x)$ renormalising the
rotation rule, with $A=1/K,\ B=K$, and — crucially — that **source-free Maxwell is conformally
invariant in $3{+}1$D**, so the EM sector sees only the conformal *class*; $K$ is exactly the
conformal factor the electromagnetic action is blind to.

A conformal (Weyl) rescaling $g_{\mu\nu}\to e^{2\sigma}g_{\mu\nu}$ couples to matter through the
**trace** of the stress tensor:

$$\delta S_\text{matter} = \int\! \sqrt{g}\,T^{\mu}{}_{\mu}\,\delta\sigma .$$

If $T^{\mu}{}_{\mu}=0$, the conformal factor $\sigma=\tfrac12\ln K$ has **no source and no tree
action** — it is a flat direction classically. The source-free electromagnetic stress tensor is
**traceless in $3{+}1$D**:

$$T^{\mu}{}_{\mu}^{\,\text{(EM)}} = -T^{00}+\textstyle\sum_i T^{ii}
= -\tfrac12(E^2+B^2) + \big[\!-\!(E^2+B^2)+\tfrac32(E^2+B^2)\big] = 0 .$$

The module verifies this on 4000 random $(\mathbf E,\mathbf B)$ to $|T^{\mu}{}_{\mu}|_\text{max}=3.6\times10^{-15}$
(machine precision). **So the dominant lattice sector gives the gravity field $K$ exactly zero
tree stiffness.** By contrast a *massive* scalar has $T^{\mu}{}_{\mu}=m^2\phi^2\neq0$ (control:
mean $0.49>0$) — it *does* source $K$, which is precisely the F52 rest-leg mass coupling. Mass
sources gravity; the massless kinetic modes set its *stiffness*, and they do so with **no tree
term**.

This is the whole pivot: there is no fundamental graviton on this lattice whose bare stiffness
F58 could be measuring. $K$ is a derived reparametrization; a derived quantity has no independent
kinetic term — its dynamics are the collective response of the fundamental $(\mathbf E,\mathbf B)$/spinor
modes. That response is the loop.

---

## 3. Channel verified: the loop is forced, not chosen (S4 — exact)

With S3 in hand the F60 fork is settled without the emergent-gravity *premise*. Reconfirming the
two stiffnesses' scaling (machine precision):

| object | meaning | scaling in $c_\text{lat}$ | exponent |
|---|---|---|---|
| $S_\text{bare}=c_\text{lat}^2$ | tree wave-operator stiffness (F58) | $c_\text{lat}^{+2}$ | $2.0000$ |
| $B\propto 1/c_\text{lat}$ | induced loop stiffness (F59) | $c_\text{lat}^{-1}$ | $-1.0000$ |
| $B/S_\text{bare}$ | gap | $c_\text{lat}^{-3}$ | $-3.0000$ |

F60 chose $B$ by *committing* to emergent gravity. F79 **derives** the choice: $S_\text{bare}$ is
the stiffness of a *fundamental* graviton kinetic term, and S3 shows the gravity field has **no
such term** (the EM sector, conformally invariant, hands it zero tree action). There is nothing
for the tree channel to measure. Hence the physical coupling is the loop channel,

$$\boxed{\ \frac{1}{16\pi G}=B\propto\frac{1}{c_\text{lat}}=\sqrt d\ }\qquad(c_\text{lat}=1/\sqrt d,\ \text{F26}),$$

and the $(a,\tau)$ selection power is $d^{+1/4}$ — F59/F60 confirmed, now as a consequence of the
lattice's structure rather than a stated ontology.

---

## 4. Every input is now structural

The Sakharov integral is no longer "matter we integrate out"; it is the lattice computing its own
dielectric stiffness, and each ingredient is fixed by the lattice itself:

| input | value | fixed by | check |
|---|---|---|---|
| $c_\text{lat}$ | $1/\sqrt d$ | BCC rotation rule (F25/F26) | S1: $I\!\cdot\!c$ flat, spread $1.7\times10^{-18}$ |
| $\eta_\text{Weyl}$ | $\tfrac1{12}$ | Seeley–DeWitt $a_1$ + Lichnerowicz + statistics (F61) | S2: exact rational |
| $g_*$ | $48$ | $O_h$ rep theory (F75) $\times$ anomaly-free content (F38/F47) | S5: $16\times3$ |

The decisive upgrade over F59–F61 is **$g_*$**. There it was "assumed three generations"; F75 makes
the generation count a **theorem about the BCC point group** — three is the dimension of the unique
odd cubic triplet $T_{1u}$, and $O_h$ has *no* 4-dimensional single-valued irrep, so a fourth is
forbidden. With the anomaly-free Higgs-free content of 16 Weyl fields per generation
($L{=}2,\ e_R{=}1,\ Q{=}6,\ u_R{=}3,\ d_R{=}3,\ \nu_R{=}1$),

$$g_* = 16\times 3 = 48,$$

is not a matter-content input but a count of the lattice's own protected normal modes. The apparent
"dependence of $G$ on how much matter exists" was always dependence on the vacuum's representation
theory.

---

## 5. The closed form and the number (S6 — exact-algebraic)

Assembling $1/(16\pi G)=\eta\,g_*\!\int d^3k/(2\omega)/a^2$ with the lattice cell $a$ the only length,
and using the Finding-10 lightcone constraint $a/\tau=c\sqrt d$ and $\ell_P^2=\hbar G/c^3$:

$$\boxed{\ \frac{1}{G}=2\pi\,\eta\,g_*\sqrt d\;\frac{\hbar}{a^2 c^3}\ }\qquad\Longleftrightarrow\qquad
G=\frac{a^2 c^3}{2\pi\,\eta\,g_*\sqrt d\;\hbar},$$

with the **parameter-free coefficient**

$$2\pi\,\eta\,g_*\sqrt d = 2\pi\cdot\tfrac1{12}\cdot 48\cdot\sqrt3 = 8\pi\sqrt3 = 43.531\ldots$$

The dimensionless content the lattice actually predicts is

$$\frac{a}{\ell_P}=\sqrt{2\pi\,\eta\,g_*}\;d^{1/4}=\sqrt{8\pi}\,\cdot 3^{1/4}=6.59782,\qquad
\frac{\ell_P}{a}=0.151565,$$

with $\tau/t_P=\sqrt{8\pi}\,3^{-1/4}=3.80925$ and the $d$-independent invariant
$\sqrt{a\,c\tau}/\ell_P=\sqrt{8\pi}=5.01326$. Anchoring $a$ at $\ell_P$ for an SI readout gives
$a=1.066\times10^{-34}\,\text{m}$, $\tau=2.054\times10^{-43}\,\text{s}$, and the closed form returns
$G=6.6743\times10^{-11}\,\text{m}^3\text{kg}^{-1}\text{s}^{-2}$ — self-consistent to $3\times10^{-8}$
(CODATA round-off), confirming the algebra rather than fitting anything.

The clean $a\approx\ell_P$ of the minimal-content guess (F59) is gone: the structurally-forced cell is
$a\approx6.6\,\ell_P$, tick $\tau\approx3.8\,t_P$.

---

## 6. What is derived, what is the one honest limit

**Derived / exact**

- $T^{\mu}{}_{\mu}^\text{(EM)}=0\Rightarrow$ the gravity field has **zero tree stiffness** (S3, $3.6\times10^{-15}$): the loop channel is **forced**, F58's tree channel has nothing to act on. *This is the non-circular replacement for F60's premise.*
- $\eta_\text{Weyl}=1/12$ exact (S2); channel exponents $2,-1,-3$ (S4); $g_*=48$ exact integer from F75+F38 (S5); $1/G\propto1/c_\text{lat}=\sqrt d$ exact (S1).
- Closed form $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$, coefficient $8\pi\sqrt3$, and $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$ (S6, exact-algebraic given the three inputs).

**The honest limit — no ruler, no dimensionful $G$ from pure numbers.** The lattice predicts the
*dimensionless* $a/\ell_P$ (equivalently the pure number $8\pi\sqrt3$). To state $G$ in SI one must
anchor the one length $a$ to a measured scale. Two anchors exist: (i) $a=\ell_P$ (the readout above),
which is circular if one wanted $G$ as the output; or (ii) — the genuinely independent route flagged
in `si-units-options.md` — fix $a$ from a **measured fermion mass** through the F46/F12 lattice-mass
map, which references no Planck length at all. Under (ii), $G$ becomes an *output of particle data*:
$G=a^2c^3/(8\pi\sqrt3\,\hbar)$ with $a$ read from, e.g., the electron mass. That is the sharpest
"derive $G$" the framework supports, and it is falsifiable through the $a/\ell_P$ relation.

**Still open (bounded).** The spin-1 gauge contribution to $g_*$ ($W/Z$ massive, non-Abelian anomaly)
is a mild $\sqrt{\cdot}$ correction (F61/F64's flagged piece). Note the **massless photon is itself
conformally invariant (traceless)** — by the very S3 argument it contributes **zero tree** stiffness;
only its conformal-anomaly (induced) piece counts, a separate spin-1 heat-kernel number not computed
here. Including it shifts $a/\ell_P$ upward slightly without touching the channel argument.

---

## 7. Verdict

Gravity is freed from the Sakharov *premise* not by discarding the loop integral but by recognising
what that integral *is*: the lattice's dielectric stiffness against bending its own rotation rule. The
gravity field is a conformal reparametrization with no fundamental kinetic term (zero tree stiffness,
S3), so the induced/loop channel is forced — verifying F60 as a theorem. Its inputs — $c_\text{lat}=1/\sqrt d$,
$\eta=1/12$, and now $g_*=48$ via the $O_h$ generation theorem — are all structural, giving the
parameter-free coefficient $8\pi\sqrt3$ and the prediction $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$.
Newton's constant is $G=a^2c^3/(8\pi\sqrt3\,\hbar)$: the lattice fixes everything but the one ruler no
lattice can supply.

---

## 8. Test summary (`test_F79_structural_G.py`, 2026-06-02 - 02:35)

| Check | Statement | Result | Status |
|---|---|---|---|
| S1 | $I\!\cdot\!c_\text{lat}$ const $\Rightarrow 1/G\propto1/c_\text{lat}=\sqrt d$ | spread $1.7\times10^{-18}$ | PASS |
| S2 | $\eta_\text{Weyl}=1/12$ (Seeley $a_1$, rational) | $1/12$ exact | PASS |
| **S3** | **EM $T^{\mu}{}_{\mu}=0\Rightarrow$ zero tree $K$-stiffness** | $|{\rm tr}T|_\text{max}=3.6\times10^{-15}$ | **PASS** |
| **S4** | **channel gap $c_\text{lat}^3$; loop forced** | $(2.0000,-1.0000,-3.0000)$ | **PASS** |
| **S5** | **$g_*=48$ structural ($16\times\dim T_{1u}$; no 4th)** | $48$ | **PASS** |
| S6 | $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$; $G$ closed form consistent | resid $3.0\times10^{-8}$ | PASS |

**Overall: 6/6 PASS** (<1 s).

## 9. Provenance

- New content: the tracelessness $\Rightarrow$ zero-tree-stiffness argument (S3) that converts F60's
  channel *premise* into a theorem, and the recognition that F75 makes $g_*$ structural — together
  yielding the parameter-free coefficient $8\pi\sqrt3$ and the $a/\ell_P$ prediction.
- Reuses: F26 ($c_\text{lat}=1/\sqrt d$), F61 ($\eta$, $g_*$ machinery), F64 D-EM5 (conformal-factor
  derivation), F75 (generation count), F38/F47 (anomaly-free 16-Weyl content), F46/F12 + `si-units-options.md`
  (the mass-anchor route to a dimensionful $G$).
- Verification: `model-tests/test_F79_structural_G.py` (2026-06-02 - 02:35, 6/6 PASS),
  results `test-results/F79_structural_G.json`.
