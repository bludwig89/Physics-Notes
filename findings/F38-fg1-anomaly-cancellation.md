# F38 — First-Generation Anomaly Cancellation (FG-1, all six traces exactly zero)

*2026-05-26 - 02:02 — Algebraic, Tier-1 exact-rational result. The L-handed Weyl content of one Standard-Model generation, with the hypercharge assignments adopted in [first-gen-completeness-review.md](../first-gen-completeness-review.md) §1, satisfies every gauge and gravitational anomaly cancellation condition exactly (over $\mathbb Q$ / $\mathbb Z$, not "to machine precision"). This closes the FG-1 entry in §5.1 of the completeness review, promotes §2.3's "anomaly cancellation" row from ❌ to ✅, and supersedes [F27](F27-complex-mass-chiral-su2.md)'s "anomaly cancellation … not tested" caveat. It is also the QFT-6 entry in `lattice-vs-spacetime-tests.md`.*

Cross-references: [F27 complex mass / chiral SU(2)](F27-complex-mass-chiral-su2.md) (mass mechanism and the original "not tested" note); [F34 W-fermion vertex](F34-wmu-fermion-vertex.md) (left-handed doublet structure); [F35 electroweak mixing](F35-electroweak-mixing.md) (Gell-Mann–Nishijima charges, W6.4); [first-gen-completeness-review.md](../first-gen-completeness-review.md) §1–§5.1; [exactness-inventory.md](../exactness-inventory.md) entries #86–91; results JSON [`test-results/FG1_anomaly_cancellation.json`](../test-results/FG1_anomaly_cancellation.json); test script [`model-tests/test_FG1_anomaly_cancellation.py`](../model-tests/test_FG1_anomaly_cancellation.py).

---

## 1. Why this matters

Anomaly cancellation is the structural proof that the charge assignments of a single Standard-Model generation are mutually consistent — that the gauge symmetries SU(3)$_c$, SU(2)$_L$, $U(1)_Y$, and the diffeomorphism (gravity) symmetry survive quantisation. Until FG-1, the project carried the charge content of [F35](F35-electroweak-mixing.md) (W6.4) on the assumption that it would cancel, with [F27](F27-complex-mass-chiral-su2.md) explicitly flagging "anomaly cancellation … not tested." This finding discharges that assumption.

The result is *not* a continuum identity that happens to be reproduced in the lattice. It is a property of the charge assignments alone — and therefore both the SM continuum theory and the present lattice-CA implementation inherit it the moment they adopt the same generation content. What FG-1 verifies is that we have not silently broken those assignments anywhere in the model.

---

## 2. Setup

### 2.1 Convention

The completeness-review §1 table uses $Q = T_3 + Y/2$, so all hypercharges quoted below are twice the "weak hypercharge" of the other common convention. With that fixed:

| Field | SU(3)$_c$ | SU(2)$_L$ | $Y$ | $Q = T_3 + Y/2$ |
|---|---|---|---|---|
| $L = (\nu_e, e)_L$ | $\mathbf 1$ | $\mathbf 2$ | $-1$ | $0,\ -1$ |
| $e_R$ | $\mathbf 1$ | $\mathbf 1$ | $-2$ | $-1$ |
| $Q = (u, d)_L$ | $\mathbf 3$ | $\mathbf 2$ | $+\tfrac13$ | $+\tfrac23,\ -\tfrac13$ |
| $u_R$ | $\mathbf 3$ | $\mathbf 1$ | $+\tfrac43$ | $+\tfrac23$ |
| $d_R$ | $\mathbf 3$ | $\mathbf 1$ | $-\tfrac23$ | $-\tfrac13$ |

### 2.2 Left-handed Weyl basis

Every fermion is rewritten as a left-handed Weyl, so right-handed Dirac components become charge-conjugate left-handed states with the SU(3) representation dualised and $Y$ negated:

$$
e_R \to e^c_L : (\mathbf 1,\ \mathbf 1,\ +2),\quad u_R \to u^c_L : (\bar{\mathbf 3},\ \mathbf 1,\ -\tfrac43),\quad d_R \to d^c_L : (\bar{\mathbf 3},\ \mathbf 1,\ +\tfrac23).
$$

### 2.3 Group-theoretic constants used

Dynkin indices $T(R)$ and pure cubic anomaly coefficients $A(R)$:

$$
T(\text{fund SU}(N)) = T(\overline{\text{fund SU}(N)}) = \tfrac12,\qquad A(\mathbf 3) = +1,\ A(\bar{\mathbf 3}) = -1,\qquad A(\text{any SU(2) rep}) = 0.
$$

The last identity is the reason $[SU(2)]^3$ never produces an anomaly: SU(2) representations are pseudo-real.

---

## 3. The six anomaly traces, evaluated exactly

Each Weyl species $i$ contributes with multiplicity $n_i = \dim_c(R_3^i)\cdot\dim_2(R_2^i)$ to traces over all states. Below, all arithmetic is over $\mathbb Q$.

### (A) Mixed gravitational anomaly $[\text{grav}]^2 \!\cdot\! U(1)_Y$

$$
\sum_i n_i\, Y_i \;=\; \underbrace{2(-1)}_{L} + \underbrace{1\cdot(2)}_{e^c} + \underbrace{6\cdot\tfrac13}_{Q} + \underbrace{3\cdot(-\tfrac43)}_{u^c} + \underbrace{3\cdot\tfrac23}_{d^c} \;=\; -2 + 2 + 2 - 4 + 2 \;=\; 0.
$$

### (B) Pure $U(1)_Y^3$ anomaly

$$
\sum_i n_i\, Y_i^3 \;=\; 2(-1)^3 + 1\cdot(2)^3 + 6\cdot(\tfrac13)^3 + 3\cdot(-\tfrac43)^3 + 3\cdot(\tfrac23)^3
\;=\; -2 + 8 + \tfrac{6}{27} - \tfrac{192}{27} + \tfrac{24}{27}
\;=\; 6 + \tfrac{-162}{27}
\;=\; 6 - 6
\;=\; 0.
$$

The non-trivial cancellation here is between $e^c_L$'s $+8$ and the quark-sector total of $-6 + \tfrac{-162}{27} = -6 - 6 = -12$, plus $L$'s $-2$ — the leptons and the colour-3 quarks balance only because the cubed-hypercharge weights line up exactly with the colour multiplicity factor of 3.

### (C) $[SU(2)_L]^2 \!\cdot\! U(1)_Y$ — sum over SU(2) doublets, weighted by colour multiplicity

$$
\sum_\text{doublets} \dim_c \cdot T(R_2) \cdot Y \;=\; \underbrace{1\cdot\tfrac12\cdot(-1)}_{L} + \underbrace{3\cdot\tfrac12\cdot\tfrac13}_{Q} \;=\; -\tfrac12 + \tfrac12 \;=\; 0.
$$

This is the cleanest of the cancellations: it forces the three-colour quark doublet to carry exactly $Y = +\tfrac13$ given that the lepton doublet carries $Y = -1$.

### (D) $[SU(3)_c]^2 \!\cdot\! U(1)_Y$ — sum over SU(3) (anti)triplets, weighted by isospin multiplicity

$$
\sum_\text{triplets} \dim_2 \cdot T(R_3) \cdot Y \;=\; \underbrace{2\cdot\tfrac12\cdot\tfrac13}_{Q} + \underbrace{1\cdot\tfrac12\cdot(-\tfrac43)}_{u^c} + \underbrace{1\cdot\tfrac12\cdot\tfrac23}_{d^c} \;=\; \tfrac13 - \tfrac23 + \tfrac13 \;=\; 0.
$$

Note that this trace receives no contribution from the lepton sector — leptons are colour singlets.

### (E) $[SU(3)_c]^3$ — pure colour cubic anomaly

$$
\sum_\text{quark Weyls} \dim_2 \cdot A(R_3) \;=\; \underbrace{2\cdot(+1)}_{Q\ (\mathbf 3)} + \underbrace{1\cdot(-1)}_{u^c\ (\bar{\mathbf 3})} + \underbrace{1\cdot(-1)}_{d^c\ (\bar{\mathbf 3})} \;=\; 2 - 1 - 1 \;=\; 0.
$$

This says the quark sector is vector-like under colour — every L-handed colour triplet has an R-handed colour triplet at the same energy — which is the structural origin of the SU(3) vector-likeness of QCD.

### (F) $[SU(2)_L]^3$

$A(R) \equiv 0$ for every SU(2) representation (pseudo-reality), so the trace is identically zero with no need for cancellation between species.

### Summary table

| # | Anomaly | Trace | Result |
|---|---|---|---|
| FG-1.A | $[\text{grav}]^2 \!\cdot\! U(1)_Y$ | $-2+2+2-4+2$ | $0$ |
| FG-1.B | $U(1)_Y^3$ | $-2 + 8 + \tfrac{6-192+24}{27}$ | $0$ |
| FG-1.C | $[SU(2)_L]^2 \!\cdot\! U(1)_Y$ | $-\tfrac12+\tfrac12$ | $0$ |
| FG-1.D | $[SU(3)_c]^2 \!\cdot\! U(1)_Y$ | $\tfrac13-\tfrac23+\tfrac13$ | $0$ |
| FG-1.E | $[SU(3)_c]^3$ | $2-1-1$ | $0$ |
| FG-1.F | $[SU(2)_L]^3$ | $0$ (pseudo-real) | $0$ |

**All six exact. Over $\mathbb Q$ (rational), not over $\mathbb R$ (floating-point).**

---

## 4. Gell-Mann–Nishijima cross-check

The completeness review's §1 charge assignments and $Q = T_3 + Y/2$ produce the measured electric charges exactly per particle. The test prints these alongside the anomaly traces:

$$
Q(\nu_{eL}) = +\tfrac12 + \tfrac{-1}{2} = 0,\quad
Q(e_L) = -\tfrac12 + \tfrac{-1}{2} = -1,\quad
Q(e_R) = 0 + \tfrac{-2}{2} = -1,
$$

$$
Q(u_L) = +\tfrac12 + \tfrac{1/3}{2} = +\tfrac23,\quad
Q(d_L) = -\tfrac12 + \tfrac{1/3}{2} = -\tfrac13,\quad
Q(u_R) = 0 + \tfrac{4/3}{2} = +\tfrac23,\quad
Q(d_R) = 0 + \tfrac{-2/3}{2} = -\tfrac13.
$$

These are the exact values quoted in §1 of the review and the F35 W6.4 tabulation; FG-1 promotes that earlier "exact to $5.6\times10^{-17}$" floating-point check (Tier-1 #73 in the inventory) to a check over exact rationals.

---

## 5. Implementation note (why the result is **0**, not "10⁻¹⁷")

The test uses Python's `fractions.Fraction` end-to-end, so every multiplication, addition, and cube is performed with arbitrary-precision integer numerators and denominators. There is no floating-point arithmetic anywhere in the computation; the residuals reported by the script are therefore the literal integers $0/1$, not floats indistinguishable from zero.

This is one of the few places in the project where the distinction between "Tier-1 exact algebraic" and "Tier-2 machine-precision" is bit-precise rather than rhetorical: every previous Tier-1 entry that quoted a residual like $\sim 10^{-17}$ was algebraically exact but computed in `complex128`. FG-1's residuals are exactly $0$ as Python integers.

---

## 6. What FG-1 does NOT close

1. **Antiparticle and $C/CP$ structure** still needs to be verified per species (FG-9 in the review). Anomaly cancellation is a charge bookkeeping result; the dynamical structure that realises those charges as antiparticles is a separate check.

2. **Quarks are still electroweak-uncoupled** in the model — the anomaly conditions hold *if* the quark doublet has $Y = +\tfrac13$ and is wired to SU(2)$_L$, but `ca_strong.py` does not yet implement that wiring (the §2.1 quark-EW row remains ❌). FG-2 (quark–$W$ Ward identity) is the next test in line.

3. **A right-handed neutrino** would add a $(1,1,0)$ field, which contributes $0$ to every trace and therefore does not change FG-1's verdict. Whether to include $\nu_R$ is a Dirac-vs-Majorana neutrino-mass choice, deferred per [F27](F27-complex-mass-chiral-su2.md).

---

## 7. Files

- Test script: [`model-tests/test_FG1_anomaly_cancellation.py`](../model-tests/test_FG1_anomaly_cancellation.py)
- Results JSON: [`test-results/FG1_anomaly_cancellation.json`](../test-results/FG1_anomaly_cancellation.json)
- Inventory entries: #86 (FG-1.A) through #91 (FG-1.F) in [exactness-inventory.md](../exactness-inventory.md)
- Review rows updated: §0 dated note, §2.3 "Anomaly cancellation" → ✅, §5.1 FG-1 row, §5.4 QFT-6 moved to "already run," §7 sequencing item 1 closed.

---

*End of finding.*
