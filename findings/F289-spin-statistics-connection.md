# F289 — Spin-statistics: the model **derives the theorem's own two premises** — $R(2\pi)=-\mathbb 1$ from its rotor and $\pi_1=S_n$ from its derived $d=3$ — so Fermi statistics for spin-½ and Bose for the paired-spinor photon follow rather than being imported

**Date:** 2026-08-05 - 17:40
**Numbering:** **F289**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `tender-gifted-pascal-2`, sector `interactions`.
**Status:** Confirmed — **11/11 PASS**, three declared controls each verified red **and verified red only where expected**. Five residuals are literal `0.0`; the rest are $\le3.5\times10^{-16}$.
**Verdict:** Completeness row **A9** leaves `ABSENT`. **Read the scope statement in §1 before the results** — this is *not* a new proof of the spin-statistics theorem, and saying so is the point of the finding.
**Modules:** `src/casim/engine/interactions/qi_spin_statistics.py`
**Test / results:** record `F289-spin-statistics` (tier gate, entry `check_spin_statistics`), driver `tests/findings/test_F289_spin_statistics.py` → `test-results/F289_spin_statistics.json`
**Cross-references:** [[F291-why-three-plus-one-dimensions]] / [[F292-no-higher-multiple-of-three]] ($d=3$ derived — premise I1), [[F26-speed-of-light-as-rotation-rate]] (the rotor), [[F217-field-native-fermion-entanglement]] (Jordan–Wigner, shown here to be a *realisation* rather than a premise), [[F195-blockspin-element-atom]] (Gram–Schmidt Pauli), [[F68-paired-spinor-photon]] / key decision 5 (the photon is a bound pair of two spin-½ Weyl quanta), [[F281-measurement-pointer-basis-born-rule-rg-classicality]] (the neighbouring A8 work). External: Finkelstein & Rubinstein, *J. Math. Phys.* **9** (1968) 1762; Leinaas & Myrheim, *Nuovo Cim.* **B37** (1977) 1.

---

## 1. What is claimed, stated before the results

The completeness report's wording is exact and worth quoting: *"Fermionic antisymmetry is **implemented** (F217 Jordan–Wigner, F195 live Gram–Schmidt Pauli); the connection is **imported**."* F217 **posits** anticommuting operators; F195 **posits** orthogonalisation. Neither asks why spin-½ *must* be antisymmetric.

The standard topological derivation (Finkelstein–Rubinstein; the belt trick) needs **two premises it cannot supply itself**:

> **I1 — the spatial dimension.** $\pi_1$ of the configuration space of $n$ identical particles is the **symmetric** group $S_n$ for $d\ge3$ and the **braid** group $B_n$ for $d=2$. Only in the first case is a transposition an involution, $\sigma^2=1$, and only then are $\pm1$ the *only* options. In $d=2$ any phase is allowed and anyons exist.
>
> **I2 — the $2\pi$ rotation phase** of the object being exchanged, because exchanging two identical particles is homotopic to rotating one of them by $2\pi$, so the exchange sign **is** that phase.

**In ordinary quantum mechanics both are inputs. In this model both are outputs.** $d=3$ is derived (F291: two independent selectors fix it; F292: $d=6$ and $d=9$ excluded), and the $2\pi$ phase is a property of the model's own SU(2) rotor, in the tree since F26.

So the claim is: **this model, unlike the theories the theorem is usually stated for, derives the theorem's own premises** — plus the machine-checked consequences below. It is a narrower claim than "we proved spin-statistics", and it is the honest one. The claim card CL255 says the same thing.

---

## 2. Premise I2 — the rotor supplies $R(2\pi)=-\mathbb 1$

| Quantity | Residual |
|---|---:|
| $\lVert R(2\pi)+\mathbb 1\rVert$ | $1.73\times10^{-16}$ |
| $\lVert R(4\pi)-\mathbb 1\rVert$ | $1.73\times10^{-16}$ |
| worst over **60** distinct rotation axes | $1.73\times10^{-16}$ |

The axis sweep matters: if the $-1$ depended on the axis it would be a property of a chosen frame rather than of the group, and the argument would not go through. It does not — the spin-½ representation is double-valued, full stop.

**A convention note that is load-bearing, not pedantry.** The rotor is $R(\theta,\hat n)=\cos\theta\,\mathbb 1-i\sin\theta\,(\hat n\!\cdot\!\vec\sigma)$, a Bloch rotation by $2\theta$, so a *physical* rotation by $\phi$ is the rotor at $\theta=\phi/2$. Getting this backwards is exactly how F281's envariance leg first went vacuous, and the module carries the conversion in one named helper for that reason.

---

## 3. Premise I1 — $d\ge3$ makes the exchange an involution

| Quantity | Value |
|---|---|
| $\lVert \text{SWAP}^2-\mathbb 1\rVert$ | **`0.0`** |
| spectrum | exactly $\{+1^{(3)},\,-1^{(1)}\}$, deviation `0.0` |
| anyonic exchange $e^{i\pi\alpha}\,$SWAP, $\alpha\in\{\tfrac14,\tfrac13,\tfrac12,\tfrac34\}$ — **unitary?** | **yes**, residual `0.0` |
| ... **involutive?** | **no**, for every $\alpha$ |

The third and fourth rows are the point, and they are the reason F291/F292 are load-bearing here rather than decorative. **An anyonic exchange is a perfectly good unitary — the algebra does not forbid it.** What forbids it is $\sigma^2=1$, which holds only because $\pi_1$ is $S_n$ rather than $B_n$, i.e. **only because $d\ge3$**. A finding that checked only $\text{SWAP}^2=\mathbb 1$ would have proved nothing about anyons; checking that the alternative is *available and excluded* is what locates the exclusion in the dimension.

With $\sigma^2=1$ the eigenvalues are $\pm1$ and there are **exactly two** statistics. Premise I2 then picks the one for spin-½: $-1$, i.e. **Fermi**.

---

## 4. F217's Jordan–Wigner operators *realise* the sign

| Check | Residual |
|---|---:|
| $\{c_i,c_j\}=0$, all $i,j$ | **`0.0`** |
| $\{c_i,c_j^\dagger\}=\delta_{ij}$ | **`0.0`** |
| **control:** the same operators with the $Z$-**string removed** | $4.0$ |

The control is the content. Without the Jordan–Wigner string the operators *commute* — they are bosonic. **The string is what carries the $-1$**, so F217's construction is the lattice realisation of the exchange sign derived above, not an independent assumption that happens to agree with it.

**Pauli exclusion follows, and is not a separate postulate:**

| Check | Value |
|---|---|
| $c_i^\dagger c_i^\dagger=0$ | **`0.0`** |
| antisymmetriser on a **same-mode** state | **`0.0`** |
| antisymmetriser on **distinct-mode** states | $\ge0.707$ |
| rank of the antisymmetriser | $15=\binom62$ ✓ |
| $k$-particle sector dimensions, $n=6$ | $[1,6,15,20,15,6,1]$ |
| $=\binom nk$ (Fermi)? | **yes** |
| $=\binom{n+k-1}k$ (Bose)? | **no** |

Two deliberate choices here. First, the exclusion statement is made about the **projector's rank**, because writing $\phi\otimes\phi-\phi\otimes\phi$ and observing that it vanishes is a tautology of subtraction — precisely defect #1 of the 2026-08-04 completeness report. A projector that annihilated *everything* would also pass, so the distinct-mode row is carried alongside. Second, the sector dimensions are **exact integers** and the bosonic count is different integers, so this row discriminates the statistics rather than merely confirming a Hilbert-space size.

---

## 5. A derived consequence: the model's photon is a boson

Key decision 5 makes the electromagnetic photon a **bound pair of two spin-½ Weyl quanta**. Rotating the pair by $2\pi$ rotates both constituents, so its phase is

$$(-1)\times(-1)=+1,\qquad \lVert R(2\pi)\otimes R(2\pi)-\mathbb 1\rVert=3.46\times10^{-16}.$$

The pair is single-valued under rotations, symmetric under exchange, and therefore a **boson**.

What makes this worth stating rather than obvious: **the model did not choose the pairing for statistical reasons.** F65–F67 forced it by *polarimetry* — the composite $\sigma$-bilinear photon is birefringent and excluded by GRB/AGN data. That the same forced pairing independently delivers the correct statistics for the photon is a consistency the model was not tuned for.

---

## 6. Controls

| Perturbation | Goes red at | Meaning |
|---|---|---|
| `--param rotation_turns=2.0` | S1, S6 | $4\pi$ gives $+1$: the double-valuedness the whole argument rests on is gone |
| `--param exchange_alpha=0.5` | S3 | an anyonic exchange — still unitary (S3b), excluded only by $d\ge3$ |
| `--param jw_string=false` | S4 | without the string the operators commute; the string carries the $-1$ |

Each is asserted in the driver to go red **and to go red only where expected**, so a control that started reddening unrelated checks would itself fail.

---

## What this closes and what remains

**Closes.** Row A9 leaves `ABSENT`. Fermionic antisymmetry is no longer an import: the two premises the topological argument needs are outputs of this model, the exchange sign follows, F217's string is shown to realise it, Pauli exclusion follows from the sign, and the photon's Bose statistics are a derived consequence of a pairing forced for unrelated reasons.

**Remains, and is not hidden.**

1. **The topological step itself is imported.** That $\pi_1(\text{config space})=S_n$ for $d\ge3$ is standard algebraic topology, used here as an external result. This finding does not re-derive it and does not claim to. What is new is that its *input* — the dimension — is derived rather than assumed.
2. **The homotopy between exchange and $2\pi$ rotation** (the belt trick) is likewise the external Finkelstein–Rubinstein construction. A lattice-native version — an explicit path of BCC hops realising the exchange and its $2\pi$ counterpart, with the phase read off the walk — is the natural next step and is *not* done here.
3. **Spin ≥ 1 is untouched.** The argument is run for spin-½ and for the spin-½ **pair**. A general-spin statement needs the higher representations.
4. **No new empirical prediction.** Every number here is a structural residual; nothing is confronted with data.
