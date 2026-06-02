# F75 — Exactly three generations from BCC point-group selection of the F27 chiral mass step

**Date:** 2026-06-01 - 20:08
**Status:** Candidate finding — 8/8 checks PASS (all group data built from generators; multiplicities exact rationals, character table cross-checked orthonormal over the integers). The *group theory* is exact; the *physical identification* (generation index = orbital shell irrep) is a stated hypothesis, not a theorem. See §7 limitations.
**Module:** no new model module — analytic group-theory result on the existing `ca_bcc.py` nearest-neighbour shell + the F27 chiral mass step.
**Verification script:** `model-tests/test_F75_three_generations_irrep.py`
**Results:** `test-results/F75_three_generations_irrep.json`
**Cross-references:** F27 (chiral SU(2) mass step), F37 (BCC chirality/helicity), F46 (spherical-Pythagorean mass — the scalar-mass requirement), F26/F30 (BCC lattice & its dispersion), F38 (one-generation anomaly cancellation — the quantum numbers that generations must share).

---

## 1. The question

The Standard Model contains three fermion generations with identical gauge
quantum numbers and a steep mass hierarchy; *why three* is undetermined in the
SM, where the number is an input. The project's framework offers two places a
discrete "3" could be hiding:

1. the **F27 chiral mass step** (the only place a fermion mass enters), and
2. the **discrete symmetry of the BCC lattice** (the vacuum's point group).

This finding asks whether either admits **exactly three** independent, stable
mass eigen-solutions, with a **fourth forbidden or unstable**.

We define a *generation multiplet* operationally, matching the SM's own
defining property of generations:

> A generation multiplet is a set of fermion states that (i) carry **identical
> gauge quantum numbers** (so they are copies, not new particles — cf. F38's
> single-generation anomaly content), (ii) are related by an **exact symmetry of
> the vacuum** (so they are forced to be degenerate and mutually equivalent),
> and (iii) are **mutually independent** (linearly independent states).

Condition (ii)+(iii) is exactly the statement that the multiplet is a single
**irreducible representation** (irrep) of the vacuum symmetry group. For the
BCC vacuum that group is the cubic point group $O_h$ (order 48).

---

## 2. Result in one line

$$
\boxed{\;
\text{generations} \;=\; \dim\big(\text{the unique odd-parity \emph{triplet} irrep } T_{1u} \text{ of } O_h\big) \;=\; 3,
\quad\text{and } O_h \text{ has no 4-dim single-valued irrep, so a 4th is forbidden.}
\;}
$$

The argument is a four-step chain, each step verified with exact arithmetic.

---

## 3. The chain

### Step 1 — $O_h$ has maximal single-valued irrep dimension 3 (check `T1`)

Building $O_h$ from two cube rotations and inversion gives the 48 elements and,
by genuine conjugation, the 10 conjugacy classes. The single-valued (tensor)
irreps are

$$
A_{1g},A_{2g},E_g,T_{1g},T_{2g}\;(\text{parity }+),\qquad
A_{1u},A_{2u},E_u,T_{1u},T_{2u}\;(\text{parity }-),
$$

of dimensions $1,1,2,3,3$ in each parity sector. The sum of squared
dimensions is $2(1+1+4+9+9)=48=|O_h|$ (Burnside — the table is complete), and
the embedded character table passes $\langle\chi_a,\chi_b\rangle=48\,\delta_{ab}$
**exactly over the integers**. The largest single-valued irrep is
**3-dimensional**.

By Schur's lemma a symmetry-protected, mutually-equivalent, independent
multiplet must fill one irrep, so it has **at most three** members. A fourth
symmetry-degenerate partner would need a 4-dimensional single-valued irrep,
**which $O_h$ does not possess** — the fourth is forbidden by representation
theory, not by dynamics.

### Step 2 — the BCC nearest-neighbour shell realises a triplet (check `T2`)

The F27 mass step couples the anchored chirality to its partner on the
neighbouring sites. The BCC nearest-neighbour shell is the **8 body-diagonal
neighbours** — the 8 vertices of the surrounding cube. Their permutation
representation, decomposed by exact rational projection against the $O_h$
table, is

$$
\Gamma_{\text{shell}} \;=\; A_{1g}\,\oplus\,A_{2u}\,\oplus\,T_{1u}\,\oplus\,T_{2g}
\qquad(1+1+3+3=8).
$$

The decomposition **contains a 3-dimensional irrep**, so the triplet channel is
not merely allowed in the abstract — it is *present* in the actual lattice
neighbourhood the mass step acts on. (This is why the answer is **3**, not 1 or
2: the lattice physically furnishes a triplet.)

### Step 3 — parity selects the *unique* odd triplet $T_{1u}$ (check `T3`)

The Dirac/F27 mass is a **scalar** (it must be, for the F46 spherical-Pythagorean
dispersion $\cos\Omega_{\text{Dirac}}=\sqrt{1-m^2}\cos\omega_{\text{kin}}$ to hold —
a pseudoscalar mass would not give that clean rest-rotation $\arcsin m$). A
scalar mass $\bar\eta\,\chi$ links the two opposite chiralities, which under
parity carry **opposite spatial parity**. The anchored chirality $\eta$ sits in
the totally symmetric $A_{1g}$ s-orbital of the cell; for the bilinear to be a
true scalar, the partner $\chi$ must occupy an **odd-parity ($u$) shell orbital**.

The odd-parity content of the shell is exactly $A_{2u}\oplus T_{1u}$. Among these
the **only triplet is $T_{1u}$**. $T_{2g}$ is even-parity → excluded as a
scalar-mass partner; $A_{2u}$ is a lone non-degenerate singlet → not a generation
*multiplet*. Hence the mass-carrying generation multiplet is **uniquely $T_{1u}$,
of dimension exactly 3.**

### Step 4 — Schur stability: the fourth is forbidden or split off (checks `T4`, `T4b`)

Any $O_h$-invariant Hermitian mass operator on the shell is, by Schur, **constant
on each irrep block**; its eigenvalue degeneracy multiset is therefore the irrep
dimensions $\{1,1,3,3\}$. A group-averaged random Hermitian operator confirms
this: it commutes with all 48 elements (residual $4.4\times10^{-16}$) and has
eigenvalue degeneracies exactly $[1,1,3,3]$. The maximal **symmetry-protected**
degeneracy is **3**.

A would-be fourth generation degenerate with the triplet cannot be added: a
4-dimensional degenerate block does **not commute with $O_h$** (the simplest
4-site block has commutator norm $1.0$ with the group — check `T4b`), so forcing
a 4-fold degeneracy *requires breaking the lattice symmetry*. Under any
symmetry-respecting dynamics the fourth state lives in a different irrep, takes a
generically different eigenvalue, and **splits away** — it is not a stable fourth
generation. This is precisely the requested "fourth forbidden **or** unstable":
forbidden as a symmetry partner, unstable (split, non-degenerate) as an
independent level.

---

## 4. Verdict on the two candidate mechanisms

- **The lattice discrete symmetry — YES, it carries the result.** The cubic
  point group's representation theory both *caps* the count at three (no 4-dim
  single-valued irrep) and *realises* exactly three (the $T_{1u}$ shell triplet).
  The "3" of generations is the same "3" as the three rows of a cubic vector
  (the $T_{1u}\cong$ vector irrep) and, ultimately, the three spatial dimensions
  the BCC lattice tiles.

- **The F27 mass step — it is the *selector*, not the source.** F27 alone (a
  $2\times2$ chiral rotation with a pure-gauge phase $\theta$) has no discrete
  generation structure; the SU(2) direction is gauge (F27 T3, F53 P5). What F27
  contributes is the **scalar-mass / opposite-parity** requirement (Step 3) that
  picks the *unique odd triplet* out of the shell's two triplets, collapsing a
  potential six ($T_{1u}\oplus T_{2g}$) to exactly three.

The two mechanisms are not alternatives — they compose: **the lattice supplies
the triplet, the chiral mass step selects which one.**

---

## 5. Test summary (`test_F75_three_generations_irrep.py`, 2026-06-01 - 20:08)

| Check | Statement | Result | Status |
|---|---|---|---|
| G1 | Group orders built from generators | $\lvert O\rvert=24,\ \lvert O_h\rvert=48$ | PASS |
| G2 | Ten conjugacy classes (real conjugation) | 10 classes, correct sizes | PASS |
| G3 | Shell permutation character (# fixed vertices) | $[E{=}8,8C_3{=}2,6\sigma_d{=}4,\text{rest}{=}0]$ | PASS |
| G4 | Embedded $O_h$ table orthonormal over $\mathbb Z$ | $\langle\chi_a,\chi_b\rangle=48\delta_{ab}$ exact | PASS |
| **T1** | **Max single-valued irrep dim** | **3** ($\sum d^2=48$) | **PASS** |
| **T2** | **Shell decomposition** | $A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$ | **PASS** |
| **T3** | **Parity-selected triplet** | unique odd triplet $=T_{1u}$, dim **3** | **PASS** |
| **T4** | **Schur degeneracies** | $[1,1,3,3]$, commutator $4.4\times10^{-16}$ | **PASS** |
| T4b | 4-fold block breaks $O_h$ | commutator $=1.0$ | PASS |

**Overall: 8/8 PASS.** All multiplicities are exact rationals; the only
floating-point number in the chain is the Schur degeneracy demo's commutator
($4.4\times10^{-16}$, linear-algebra floor).

---

## 6. Why this is more than numerology

The result makes **falsifiable structural commitments**:

1. The generation multiplet transforms as the **vector irrep $T_{1u}$** of the
   cubic group. The three generations are therefore predicted to be a
   *cubic-vector triplet* — under the residual lattice symmetry they rotate into
   one another exactly as $(x,y,z)$ do. Any inter-generation operator the model
   builds must be a $T_{1u}$ tensor; this constrains the allowed mixing (CKM/PMNS)
   textures the lattice can produce.
2. A **fourth generation is excluded as a symmetry partner** — not disfavoured,
   but representation-theoretically impossible for $O_h$. This agrees with the
   experimental exclusion of a sequential fourth generation (LHC Higgs
   production, $Z$ invisible width $N_\nu=2.984\pm0.008$), and here it is a
   theorem about the vacuum's point group rather than a fit.
3. It ties the number 3 to the **3 spatial dimensions** via the same vector
   irrep — consistent with the project's thesis that the lattice geometry is the
   source of the particle content.

---

## 7. Honest limitations (what is *not* proven)

1. **The physical identification is a hypothesis.** "Generation index = orbital
   irrep of the nearest-neighbour shell" is a *model*, motivated by the F27 mass
   step acting on neighbours, but it is not derived from the QCA update rule. The
   group theory below it is exact; the bridge to "these are the muon/tau" is not.
2. **Mass hierarchy not derived.** This explains the *count* (and the forbidden
   fourth), not *why* $m_e\ll m_\mu\ll m_\tau$. The three $T_{1u}$ partners are
   degenerate at the symmetric point; the hierarchy must come from a
   symmetry-lowering (e.g. anisotropy / a $T_{1u}\!\to\!A\oplus E$ crystal-field
   splitting) that is left open. A natural next step is to compute that splitting
   pattern and compare its *ratios* to the observed lepton masses.
3. **The double-group caveat.** Fermions strictly carry the *double* cover
   $O_h'$, whose spinor (double-valued) irreps include a **4-dimensional** one
   ($G_{3/2}$). The argument here counts generations as a **single-valued**
   (spin-scalar) multiplicity, on the grounds that all three generations share
   the same spin-½ — the family label does not change spin, so it lives in the
   tensor irreps (max dim 3). This is the physically correct split, but it is an
   assumption that the generation quantum number factorises from spin, and it is
   the load-bearing assumption behind "no fourth."
4. **One triplet vs the shell's two.** Step 3 uses parity to discard $T_{2g}$.
   This is clean for a pure scalar mass, but the model also admits a pseudoscalar
   ($\gamma_5$) mass channel; if that channel were ever dynamically active it
   would couple the even triplet and the simple "exactly three" would become
   "three per active mass-parity channel." F46/F53 indicate the scalar channel is
   the physical one (θ pure gauge), which is why the count is three, but this
   should be stress-tested.

---

## 8. Provenance

- Hypothesis: that the BCC vacuum's point-group representation theory caps and
  realises the generation count, with the F27 scalar-mass parity rule as
  selector. New here (no prior project finding addressed generation number).
- Derivation: §3, built from generators + exact rational projection.
- Verification: `model-tests/test_F75_three_generations_irrep.py`
  (2026-06-01 - 20:08, 8/8 PASS, <1 s), results in
  `test-results/F75_three_generations_irrep.json`.
