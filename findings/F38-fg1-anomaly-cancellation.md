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

## 7. The 8-state lepton vector and the (right-handed weak ↔ magnetic monopole) correspondence

*2026-05-28 - 02:44 — Organising-principle addendum to FG-1. Records the notebook's L/R-symmetric lepton octet (pp.89–97; cross-checked in [physics-notes-complete-review.md](../physics-notes-complete-review.md) §4.1) as a single 8-state object and identifies its four EM-neutral states with the two gauge channels that are absent in nature: right-handed weak SU(2)$_R$ and magnetic monopole U(1)$_{em}^\star$. Also tightens [F37](F37-rs-bcc-chirality-helicity.md)'s RS-BCC chirality/helicity bookkeeping by giving that section's 4-state photon split a matching 8-state lepton target.*

### 7.1 The lepton octet

Arrange the L- and R-chirality Weyl content for one lepton generation — keeping $\nu_R$ and $\bar\nu_L$ even though they are SM-sterile (§6 item 3 above) — as

$$
\Psi_{\text{lep}} \;=\; \bigl(\,
\underbrace{e_R^{-},\ e_L^{+},\ e_R^{+},\ e_L^{-}}_{\text{EM-charged (4)}}\;,\;
\underbrace{\nu_R,\ \bar\nu_L,\ \bar\nu_R,\ \nu_L}_{\text{EM-neutral (4)}}\,
\bigr).
$$

The eight components partition $2\times 2\times 2$ as (chirality L/R) $\times$ (C-conjugation particle/antiparticle) $\times$ (isospin $t_3=\pm\tfrac12$, electron/neutrino). EM-charge tracks isospin alone; weak-charge tracks the L/R label.

### 7.2 The (EM-charge, W-charge) classification

| Pair | EM-charge | $W$-charge | SM status | Missing-channel identification |
|------|-----------|------------|-----------|--------------------------------|
| $e_R^{-},\ e_L^{+}$ | yes | no | SM (singlet sector) | — |
| $e_R^{+},\ e_L^{-}$ | yes | yes | SM (L-doublet member) | — |
| $\bar\nu_R,\ \nu_L$ | no | yes | SM (L-doublet partner of $e_L^{-}$) | magnetic monopole U(1)$_{em}^\star$ |
| $\nu_R,\ \bar\nu_L$ | no | no | SM-absent | right-handed weak SU(2)$_R$ |

The four EM-charged states populate both ($W$, no-$W$) entries — exactly the structure gauged in the SM by $\{$U(1)$_Y$, SU(2)$_L\}$. The four EM-neutral states populate the *same* two entries with neither of the corresponding gauge interactions present in nature.

### 7.3 Structural identity

The notebook's observation on pp.94–95 — "the right-handed weak interaction does not exist, and neither does the magnetic monopole" — is the statement that

> the absence of SU(2)$_R$ and the absence of U(1)$_{em}^\star$ are **the same fact** in the L/R-symmetric octet: both express that the four EM-neutral lepton states sit in the kernel of every gauge operator that is realised in nature, rather than in the image of right-handed or dual gauge channels.

So the missing magnetic monopole and the missing $W_R$ are not two independent omissions but a single structural choice — the EM-neutral half of $\Psi_{\text{lep}}$ is gauge-sterile under everything the SM gauges.

### 7.4 Consequence for the FG-1 traces

Within the §3 traces, the SM-absent states $\nu_R$ and $\bar\nu_L$ contribute exactly $0$ to (A)–(F): they carry $Y=0$, no SU(2)$_L$, no SU(3)$_c$, and $A(\mathbf 1)=0$. Adding them to the octet therefore does not perturb any of FG-1's six rationals. This is the §6 item 3 footnote made constructive — the *reason* the right-handed neutrino can be appended without re-running the anomaly arithmetic is that it sits in the missing-channel sector defined by §7.2.

### 7.5 Tightening the F37 bookkeeping

[F37](F37-rs-bcc-chirality-helicity.md) splits the BCC photon into a $2\times 2$ object: two RS eigenstates $\mathbf F_\pm = \mathbf E \pm i\mathbf B$ on two BCC chirality branches $\Omega^\pm$, giving 4 propagating modes per wavevector. Gauged minimally by U(1)$_{em}$, those 4 modes couple to only 4 of $\Psi_{\text{lep}}$'s 8 components — the EM-charged half. Two observations follow once the L/R-symmetric extension of §7.1 is adopted:

1. **One vector, two ledgers.** F37's helicity/chirality bookkeeping and the §3 anomaly bookkeeping become bookkeeping over a *single* 8-state object. F37's $(\mathbf F_+, \Omega^+)$ / $(\mathbf F_-, \Omega^-)$ pairing acts on the 4 EM-charged components of $\Psi_{\text{lep}}$; the 4 EM-neutral components are the would-be targets for the dual $\mathbf F_\pm^{\star}$ (magnetic-monopole) and the SU(2)$_R$ partner of the W. The latter are absent precisely by §7.3, so the photon-side count (4 modes) matches the lepton-side count of *gauged* channels (4 states) exactly. The L/R-symmetric octet is therefore the smallest closed system in which the F37 split and the FG-1 traces operate on the same vector space.

2. **No birefringent neutrino channel.** F37's predicted vacuum birefringence $\Delta v_\phi/c \approx -k/18$ along $(1,1,1)$ is a property of the EM-charged sector's coupling to the BCC chirality branches. The EM-neutral half — carrying no U(1)$_{em}$ charge — sees no analogous chirality-branch splitting, and §7.3 rules out a parallel "neutrino magnetic-monopole birefringence" channel by the same structural fact that rules out SU(2)$_R$.

Neither observation modifies FG-1 (six exact zeros stand) or F37's algebraic identities (RS ↔ BCC chirality correspondence stands). They reorganise the two findings around one 8-state object rather than two disjoint 4-state ledgers.

---

## 8. Files

- Test script: [`model-tests/test_FG1_anomaly_cancellation.py`](../model-tests/test_FG1_anomaly_cancellation.py)
- Results JSON: [`test-results/FG1_anomaly_cancellation.json`](../test-results/FG1_anomaly_cancellation.json)
- Inventory entries: #86 (FG-1.A) through #91 (FG-1.F) in [exactness-inventory.md](../exactness-inventory.md)
- Review rows updated: §0 dated note, §2.3 "Anomaly cancellation" → ✅, §5.1 FG-1 row, §5.4 QFT-6 moved to "already run," §7 sequencing item 1 closed.

---

*End of finding.*
