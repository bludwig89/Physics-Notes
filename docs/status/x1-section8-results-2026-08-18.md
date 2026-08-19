# X1 §8 — the five checks, run

**Date:** 2026-08-18
**Companion to:** `docs/status/x1-colour-normalisation-fork-2026-08-18.md` §8
**Reproduction:** `tools/x1_probe.py` (§2/§3/§5 of the companion), `tools/x1_s8_magnetic.py` (§8.2 here)
**Code landed:** `casimir_ladder.py` (+`numerator` param, `operator_consistency()`, leg L6), `derive_coupling_normalisation.py` (+`casimir_branch_vs_f280_band()`, leg N8), `tests/registry/gauge.yaml` (+2 controls)

---

## 0. Verdict

**The resolution survives all five checks, and comes out stronger than it went in.** Two of them changed the picture materially:

* Check 1 (the one that could have reversed everything) resolves cleanly against branch A: the integer flux spectrum is a modelling choice, and the tree says so in its own words in four places.
* Check 2 turned up something the ledger does not know: **the genuine SU(N) link Hamiltonian that F294 asked for and F110 deferred already existed on 2026-06-07** — `su3_ladder.py`, finding **F111b**, check **T7** — five days *before* F144, and it reports the C7 map as $\chi=1/(4g^2)$ **with no $C_F$**. None of F294/F298/F299/F303 cites it. F294 §"Remains" item 1 was closed two months before it was written.

Two new defects were found on the way, and both are recorded here rather than buried: **F111b T7's identity is link-count inconsistent** (§2.3), and **F144 A1 step 2 does not derive $\chi=1$** (§2.5). Neither restores branch A. The second is the honest replacement for X1's residual.

| check | verdict | effect on the resolution |
|---|---|---|
| **1** integer spectrum derived or chosen? | **CHOICE** — decisive, with quotes | premise holds; branch A not restored |
| **2** magnetic side of C7 | **closes negatively** — no factor; and the SU(N) rotor already existed and agrees | residual closed; two new defects found |
| **3** operator control on `F298-casimir-ladder` | **landed, verified `CONTROL`** | the record can now see its own premise fail — and the cost is bigger than CN19 (§3.2) |
| **4** branch-A exclusion vs CL252 | **landed, verified `CONTROL`** | 5.63 decades, in-gate |
| **5** $d_1$ native sweep | **not runnable here, and no longer decisive** | its role changed from choosing a branch to pinning $\alpha_s$ |

---

## 1. Check 1 — is the integer flux quantisation derived from the rule?

**Answer: no. It is an exactly-solvable modelling choice, and four separate places in the tree say so.**

This was the check that could reverse the whole resolution: if the rule itself forces an integer-spectrum $\hat E$ on a link, the mixed matching is the physical one, branch A returns and CN19 with it.

**(a) The rule's own fields are continuous.** `weak_wmu._f26_rotation_step` is `E_new = cos(Ω)E + sin(Ω)B`, `B_new = −sin(Ω)E + cos(Ω)B` on floating-point FFT arrays; `gluon.gluon_rotation_step_spectral_2d` takes `E_G, B_G : (8, Lx, Ly) real`; F26 §: *"The physical fields $(\mathbf E,\mathbf B)$ are **real-valued 3-vectors**."* There is no integer variable anywhere in the rule.

**(b) The integer spectrum is asserted, and the tree's own word for it is "the fix".** F101 §2 introduces $\hat E|m\rangle=m|m\rangle$ by fiat and frames the move as a choice to keep — *"This finding **keeps the same transfer operator but compact**"* against F100's non-compact Gaussian. `test_F101_strong_coupling_sigma.py` header: *"**The fix** is the rule's single-plaquette transfer operator kept COMPACT."* `link_hamiltonian.py`: *"$\hat E_\ell$ the **integer** (compact) electric field"*, with the U(1) option *"truncated at $|m|\le m_\text{max}$"*.

**(c) The three near-misses each stop short.** Gauss's law is *"solved, not imposed"* (F110) — but by the **height** representation, which exists only for abelian groups, and integrality is an input to it (*"with **integer** height operators"*). The $\mathbb Z_3$ centre symmetry **is** exact in the update rule (F99 D3, verified $5\times10^{-16}$) — but it is checked on **SU(3) matrices**, is the standard centre symmetry of any SU(3) LGT, and licenses classification by N-ality rather than quantisation of $\hat E$. F88 comes closest and names it as an assumption: *"compactness of $U(x)$ — **which the model has by construction**"*.

**(d) The model's links are SU(3)-valued, in a parallel stack.** `strong.py`: *"**Link field $U_\mu(x)\in SU(3)$** for each forward direction"*; `gluon.py` (Gell-Mann `_T_STACK`, `_su3_expmap_field`); `bcc_action.plaquette_field_strength_su3`; `confinement.py` (SU(3) Weyl-torus, $N=3$); F94 (*"the full non-Abelian SU(3)"*, abelian-projection-free). **`link_hamiltonian.py` contains no SU(3) matrix at all.**

**(e) F298 and F303 already call the $\mathbb Z_3$ side an effective description.** F303 §3: *"The model's $\mathbb Z_3$ Hamiltonian is a *correct* **effective description** of the $SU(3)$ ladder at $N=3$."* F298 §3: same words. F110's own scope note: *"$\mathbb Z_3$ / U(1), **not** the SU(3) Casimir ladder."*

**One document disagrees and should be marked stale.** `docs/audits/project-audit-inputs-dynamism-2026-06-06.md` line 41 files the compact rotor under *"A.1 Derived (formerly inputs, now closed) — from rule's transfer operator"*. It predates F294/F298/F299/F303 by two months and is the only "derived" claim in the tree.

**Consequence.** The consistent C7 evaluation is the $SU(N)$ one, $\chi=1/(4g^2)$, no $C_F$ — and **CN19 falls** as forecast, since the $N_c\le3$ restriction is a property of the mixed matching. The weakened implementation-validity statement (§4 of the companion) stands.

---

## 2. Check 2 — the magnetic side of C7

### 2.1 The named residual closes, negatively

The companion's §2 matched only the electric term. The worry was that the $SU(3)$ plaquette operator is not $\cos\hat\phi$ — its matrix elements between irreps could carry dimension or $6j$ factors — and would move $\chi$ off 1 by an $O(1)$ amount.

**Measured: it does not.** The magnetic operator in both theories is $-\tfrac{\lambda}{2}\times$ (unit-entry adjacency $+$ transpose):

| theory | magnetic operator | non-zero entries |
|---|---|---|
| compact U(1) | $-\lambda\cos\hat\phi=-\tfrac\lambda2(\Gamma+\Gamma^\dagger)$ | $1$ |
| $SU(3)$ | $-\tfrac\lambda2(\chi_F+\chi_{\bar F})$, fusion adjacency $M_F$ | $\{1.0\}$ (measured over the ladder to $p+q\le6$) |

$\chi_F\cdot\chi_R=\sum_{R'\in F\otimes R}\chi_{R'}$ is multiplicity-free, so $M_F$ is a 0/1 matrix — the exact analogue of $\cos\hat\phi$ shifting the U(1) charge by $\pm1$. **Coefficient to coefficient, $\lambda\leftrightarrow\lambda$: the magnetic term introduces no factor into the $\chi$-map.** What differs between the groups is the *fusion degeneracy* and the observable normalisation $1/d_F$ — see §2.4, which moves $\sigma_1$, not $g_s$.

### 2.2 The SU(N) link Hamiltonian F294 asked for already existed

`src/casim/engine/gauge/su3_ladder.py`, created **2026-06-07**, finding **F111b** (*"Recovered and renumbered 2026-07-31"*), registry record `F111-tree-gauge-su3-ladder`. Its docstring:

> **The SU(3) character rotor** — the F101 compact rotor with the U(1) charge basis replaced by the SU(3) irrep (character) basis:
> $H=(g^2/2)\hat C_2-(\lambda/2)(\chi_F+\chi_{\bar F})$ …
> Strong-coupling PT: $a_3=(\lambda/2)/((g^2/2)C_2(F))=3\lambda/(4g^2)$, giving
> $s_1\to(1/3)(a_3+a_{\bar3})=\lambda/(2g^2)=\mathbf{2\lambda\chi}$ **at $\chi=1/(4g^2)$**
> — the SAME leading non-perturbative log law as the F101 U(1) rotor **under the F110 $\chi$-map**. **The group changes the string tension ladder (Casimir scaling); it does not change the leading strong-coupling logarithm.**

F111b's summary says it again: *"Its strong-coupling law $s_1\to\lambda/(2g^2)$ is **identical** to the F101 U(1) rotor's $2\lambda\chi$ under the F110 map $\chi=1/(4g^2)$."*

F294 §"Remains" item 1 read: *"**Build the $SU(N)$ Casimir ladder** that F110 deferred, and re-run C7 against it. This is the one computation that decides between H1 and H2."* It had been built and run **two months earlier**, and neither F294, F298, F299 nor F303 cites F111b. F299 does cite *"F111-su3-ladder-casimir-scaling"* in its cross-reference list — a link to a finding file that does not exist under that name (`F111-second-order-light-deflection.md` holds the bare number) — so the pointer was there and dangling.

### 2.3 …but F111b T7 is link-count inconsistent, and must not be quoted as confirmation

Re-run (F111b itself flags the record as a C7 close-out **regression candidate**, so this needed re-checking):

```
su3_rotor_sigma1(g2=1, lam=1e-3)          s1 = 0.0005005627
rotor_sigma1(lam=1e-3, chi=1/(4 g^2))     s1 = 0.0004999999
|ratio - 1| = 1.126e-03      (T7 tolerance 5e-3)     -> T7 REPRODUCES
```

The identity as coded is real. **The two Hamiltonians are not the same physical system.**

| | electric term | gap to the first excited level |
|---|---|---|
| `su3_rotor_hamiltonian` | $\tfrac{g^2}{2}C_2(R)$ — **one** link | $0.666667$ |
| `rotor_sigma1` at $\chi=1/(4g^2)$ | $\tfrac1{2\chi}m^2=\tfrac{g^2}{2}\cdot4\cdot m^2$ — **four** links | $2.000000$ |
| | | ratio **3** $=n/C_F$ |

Compared consistently — same $n$ on both sides — the two rotors do **not** agree, and the discrepancy is exact and group-theoretic:

$$\frac{s_1^{SU(N)}}{s_1^{U(1)}}=\frac{2}{N^2-1}\qquad\text{independent of }n.$$

| $N$ | $n=1$ | $n=4$ | $2/(N^2-1)$ |
|---:|---:|---:|---:|
| 2 | 1.333326 | 1.333333 | 0.666667 ✗ |
| 3 | 0.250282 | 0.250070 | 0.250000 |
| 4 | 0.133334 | 0.133333 | 0.133333 |
| 5 | 0.083334 | 0.083333 | 0.083333 |

*(the $N=2$ row reads 1.3333 against $2/(N^2-1)=0.6667$ because $\mathbb Z_2$'s $s(1)^2$ tower has one rung; the ratio law is verified on $N\ge3$ and analytically for all $N$.)*

**So there is no $N_c$ selector hiding here.** $2/(N^2-1)=1$ needs $N^2=3$. T7's agreement at $N=3$ is exactly the 1-vs-4 mismatch: $3\times\tfrac43=4$, i.e. $C_F\cdot d_F=(N^2-1)/2=4$ at $N=3$ coincides numerically with the four links. That coincidence is attractive enough to be re-derived by someone who does not know it is a convention artefact — recording it here for the same reason F303 §4.2 recorded the three-bond plaquette.

**Net effect on the resolution: neutral-to-positive.** F111b is *not* an independent confirmation of $\chi=1/(4g^2)$ — but it is also not evidence against it, and the §2.1 coefficient argument stands on its own. F111b needs a correction note and T7 needs its comparison rebuilt at equal $n$.

### 2.4 New, and exact: the model's $\sigma_1$ is off by $\ln 4$ if the group is $SU(3)$

Because $s_1^{SU(N)}/s_1^{U(1)}=2/(N^2-1)$ exactly at the same $(\chi,\lambda)$,

$$\sigma_1^{SU(N)}-\sigma_1^{U(1)}=\ln\frac{N^2-1}{2}\;\xrightarrow{\,N=3\,}\;\ln 4=\mathbf{1.386294}\ \text{nats}.$$

That is a real, previously unrecorded correction to F99/F100/F101's string tension if the colour group is $SU(3)$ rather than the implemented $\mathbb Z_3$/U(1) — and it is **orthogonal to $g_s$**, which is why it does not disturb anything in §5 of the companion. It should be carried into the confinement sector as its own item.

### 2.5 The real gap: F144 A1 step 2 does not derive $\chi=1$

Re-deriving F303's N1 symbolically (`sympy`, reproducing its own factorisation):

```
M^T M - I  with a = r b:
  [0,0] = (r-1) sin^2(b sqrt(r) t)      [0,1] = (1-r) sin(2 b sqrt(r) t)/(2 sqrt(r))
solve for r  (b, t free)  ->  [{r: 1}, {r: pi^2/(b^2 t^2)}]
M^T M - I  at a = b       ->  Matrix([[0, 0], [0, 0]])   for EVERY b
```

F303 §2 states this premise verbatim — *"orthogonality at generic tick holds **iff $r=1$, whatever $b$ is**… the lemma constrains a *ratio* and nothing else"* — and then concludes *"steps 1–2 survive"*. The consequence it does not draw: **a lemma that fixes only a ratio does not fix $\chi$.** At $a=b$ the per-tick rotation angle is $\omega t=b t$, so with $t=1$ tick

$$a=b=\Omega(k)\qquad\Longrightarrow\qquad \boxed{\chi=1/\Omega(k)},$$

and $\chi=1$ requires $\Omega=1$, which the lemma does not supply. `running_alpha_s.py` states the derivation as *"the rule's circular rotation FORCES equal electric/magnetic stiffness: chi = 1 in the rotor normalisation (F101 S7, **now derived**)"* — the forcing is real, the value is inherited from F101 §7's normalisation. And that normalisation is the *same* compactification choice as check 1's, so **F144's A1 carries two inherited choices of one origin, not zero knobs.**

Scale of the gap, on the rule's own 2D dispersion $\Omega(k)=2\arccos\!\big(\cos\tfrac{k_x}{2\sqrt2}\cos\tfrac{k_y}{2\sqrt2}\big)$:

| quantity | value |
|---|---|
| $\Omega$ range over the BZ | $[0,\;2.744692]$ |
| $\Omega$ at the BZ corner $(\pi,\pi)$ / edge $(\pi,0)$ | $2.744692$ / $2.221441$ |
| $\langle\Omega\rangle_\text{BZ}$ | $1.645850$ |
| F101 S5's hardcoded representative | $1.3$ |
| $\Omega$ the measured $\alpha_s(M_Z)$ demands ($=4g_s^2$) | $\mathbf{0.997829}$ ($\chi=1.002176$) |
| $\Omega$ the Casimir branch would need ($\chi=1/C_F$) | $4/3=1.3333$ |
| locus of $\Omega=1$ | $\lvert k\rvert a=\sqrt2$ exactly on axis ($\Omega=\lvert k\rvert/\sqrt2$ there); $1.429781$ on the diagonal |

**This does not restore branch A** — branch A needs $\chi=3/4$, i.e. $\Omega=4/3$, and nothing selects that either. What it does is relocate F144's open normalisation from *"zero knobs"* to *"one $k$-selection"*, and that selection is plausibly the same object as the matching scale $q_\ast$ (F155's $q_\ast a\in[0.577,0.979]$). **Flagged as an observation, not a claim** — the model's lattice is BCC and this is the 2D square dispersion; the BCC $\Omega$ is the one that matters and has not been computed against this question.

This is the honest replacement for X1's residual: not *"is there a $C_F$?"* (no) but *"which $\Omega$ does the single-plaquette rotor carry?"*

---

## 3. Check 3 — the missing operator control on `F298-casimir-ladder`

**Landed and verified.**

`c7_against_casimir_ladder(..., numerator="zn" | "casimir")` — `"zn"` keeps the shipped mixed matching; `"casimir"` takes the rotor eigenvalue from the same operator as the gauge theory's. New `operator_consistency()` reports all three evaluations over $\mathbb Q$, on the $k$-string tower and on the full irrep set. New leg **L6** carries the result. Registry control added to `tests/registry/gauge.yaml`.

```
casim test --id F298-casimir-ladder                          PASS   9/9
check_control_soundness --run --id F298-casimir-ladder
  [CONTROL] control0  --param tower=symmetric     reddens exactly ['L2','L3'] of 9
  [CONTROL] control1  --param n_max=3             reddens exactly ['L2']      of 9
  [CONTROL] control2  --param numerator=casimir   reddens exactly ['L2','L3'] of 9
```

What the new leg reports:

| $N$ | both abelian | **mixed (shipped)** | both $SU(N)$ | full irrep scan |
|---:|---:|---:|---:|---|
| 2 | 1 | 4/3 | 1 | 5 irreps → {1} |
| 3 | 1 | 3/4 | 1 | 11 irreps → {1} |
| 4 | 1 | 8/15, 8/5 | 1 | 15 irreps → {1} |
| 5 | 1 | 5/12, 10/9 | 1 | 17 irreps → {1} |
| 6 | 1 | 12/35, 6/7, 12/7 | 1 | 18 irreps → {1} |
| 7 | 1 | 7/24, 7/10, 21/16 | 1 | 18 irreps → {1} |

Also corrected in place: the module's `note` field claimed *"$m(k)=k$ is forced, not chosen"*. That argument forces the **ordering** of the two ladders, not the identification of their **eigenvalues** — a compact U(1) rotor ($m^2$) and a non-abelian one ($C_2$) are exactly a pair with matched ladder structure and different spectra. The note now says so.

### 3.2 The cost is bigger than CN19: F324's upper constraint goes with it

The working tree contains two findings dated **2026-08-17**, written after the X1 ledger row and not yet in it: **F323** (the BCC anisotropy derived; F299's $d=4$ Casimir successor runs) and **F324** (*"The $N_c$ interval closes on $\{3\}$"*), plus card **CL281**. F324's verdict:

> Row **B10**: the $\Lambda$-scale selector is **no longer load-bearing**, and B10 **stops being a dependent of the X1 fork**.

It closes $N_c=3$ from two constraints: a **lower** one — the $\mathbb Z_2$ doublet parity of the model's own derived $SU(2)_L$ (Witten's global anomaly ⇒ $N_c$ odd; prior art, Bär & Wiese 2001, and F324 says so) — and an **upper** one, imported verbatim from F298:

> **U1.** F298's criterion unchanged: a level-independent $\chi_k=s(k)^2/(4g^2C_2(\text{antisym }k))$ exists iff the k-string tower is non-empty and every level agrees.

That is the mixed matching. **Under the operator-consistent evaluation there is no upper constraint at all** — $\chi=1/(4g^2)$ for every $N$ — so B10 does not close on $\{3\}$; it closes on **odd $N_c$, unbounded above**: $\{3,5,7,\dots\}$ once premise (ii) removes $N=1$. That is the real cost of check 3, and it is larger than the CN19 loss the companion forecast.

**F324 reaches the same place from the other side, and books it.** Its §3 U1c — *"the truncation cuts both ways, and this direction had not been named"* — measures the sextet off the k-string tower and finds the mixed matching already level-dependent **at $N=3$**:

> $\chi_{\mathbf 6}=\tfrac{3}{10}$ against the tower's $\chi=1/C_F=\tfrac34$ … So the support $\{2,3\}$ is a property of the **truncation**, not yet of the model. That is **falsifier 5b and it is the most serious structural exposure on the upper side.**

Falsifier 5b is not merely exposed. It is realised, and the full picture is worse than the one rung F324 sampled. Measured here over the $N=3$ irreps up to 27:

| irrep | $C_2$ | triality | rotor level $s^2$ | $\chi$ mixed | $\chi$ consistent |
|---|---:|---:|---:|---:|---:|
| $3$ | 4/3 | 1 | 1 | 3/4 | **1** |
| $\bar3$ | 4/3 | 2 | 1 | 3/4 | **1** |
| $6$ | 10/3 | 2 | 1 | **3/10** | **1** |
| $8$ | 3 | 0 | **0** | **undefined** | **1** |
| $10$ | 6 | 0 | **0** | **undefined** | **1** |
| $15$ | 16/3 | 1 | 1 | **3/16** | **1** |
| $27$ | 8 | 0 | **0** | **undefined** | **1** |

Three distinct values and three undefined. The undefined rows are the sharpest statement available of what the mixed matching is: a $\mathbb Z_3$ rotor cannot see triality-0 flux, so $s^2=0$ while $C_2\neq0$, and the matching therefore assigns **zero electric cost to an adjoint, decuplet or 27 link**. That is not an approximation with a small error; it is a category error, and it is exactly why the "identity" appears to exist only on a tower every rung of which carries non-zero triality.

Both facts are now carried by leg **L6** (`operator_consistency()` returns `su3_off_tower`, `mixed_off_tower_chi_values`, `mixed_off_tower_undefined_for`), so the record asserts them rather than a later reader rediscovering them.

**What survives for B10.** F324's lower constraint is untouched — it consumes no C7 input and no X1 branch. So the honest post-resolution position is: **$N_c$ odd, $N_c\neq1$**, i.e. $\{3,5,7,\dots\}$, with $N_c=3$ favoured by everything empirical and by nothing structural. F324's own §8 already prices its incremental content at *"one bit"*; removing the upper constraint spends that bit.

**Blast radius, measured.** Exactly three registry records consume the two edited modules (`grep -rln` over `src`, `tests`, `tools`): `F298-casimir-ladder`, `F303-coupling-normalisation`, and `F324-ncolour-bracket` via `derive_ncolour_bracket.py`. All three **PASS** after the edits — F324 because its "Mechanical note" re-evaluates the criterion on the imported `antisymmetric_ladder` rather than calling `c7_against_casimir_ladder`, so the new parameter does not reach it. **That is a passing test, not a passing argument:** F324's physics still rests on the mixed matching even though its code path no longer touches the function that implements it.

---

## 4. Check 4 — the branch-A exclusion, registered against CL252

**Landed and verified.** `casimir_branch_vs_f280_band(casimir_on=True)` rebuilds F280's band from the same three committed inputs rather than quoting it, so the check moves if F163 or the KNS anchor moves. New leg **N8**; control `casimir_on=False` sets $C_F\to1$ so the shift vanishes and the requirement collapses onto $\Lambda=1$, inside the band.

```
casim test --id F303-coupling-normalisation                  PASS   9/9
check_control_soundness --run --id F303-coupling-normalisation
  [CONTROL] control0  --param assume_three_bond_loop=True  reddens exactly ['N3'] of 9
  [CONTROL] control1  --param scheme_residual=20.0         reddens exactly ['N4'] of 9
  [CONTROL] control2  --param casimir_on=False             reddens exactly ['N8'] of 9
```

| quantity | computed | F280's published |
|---|---:|---|
| $\Delta C_W=2\ln28.8086$ | 6.721348 | — |
| $\Delta C_W^\text{loops}=6.138643-131/66$ | 4.153795 | — |
| $T_W$ (Wilson seagull + Haar) | 2.567553 | leg 1 $=-2.5676$ ✓ |
| band top $=e^{\Delta C_W^\text{loops}/2}$ | 7.979672 | $[1,7.980]$ ✓ |
| Casimir shift $16\pi(C_F-1)$ | 16.755161 | 16.755 ✓ |
| **branch A required $\Lambda$** | **3 400 378** | $\approx3.4\times10^6$ ✓ |
| branch A required $\Delta C_\text{rule}^\text{loops}$ | 30.078794 | — |
| …as a multiple of Wilson's loops-only | **7.241281×** | — |
| …decades above the band top | **5.629542** | — |
| branch B position in band | 11.08 % | "11.1 %" ✓ |
| Wilson above band top by | 3.610249× | "3.61×" ✓ |

The `x_wilson_loops_only` figure is the one that makes the exclusion independent of F280's named monotonicity assumption: branch A does not merely violate it, it requires the rule's own loops-only one-loop constant to exceed Wilson's by **7.24×**, for an action F287 §4 *measures* at $5.3$–$5.7\times$ **smaller** discretisation error than Wilson's at every grid, with an exactly empty seagull sector ($u_0\equiv1$, F155-A0).

---

## 5. Check 5 — the $d_1$ native sweep

**Not run, for two reasons, and the second one is the interesting one.**

**(i) Not runnable in this environment.** The LPT path needs `scipy`, which is absent on the connected machine (`check_finding_records.py` reports it: *"1 gate entry not analysed — missing dependency: scipy"*). The $n=28$–$40$ native sweep is explicitly a long run to be handed out as a `casim` parameter set with a JSON, per CLAUDE.md — not a session-inline computation.

**(ii) It should not be run yet anyway, and it no longer decides anything about X1.** F307 §3 is unambiguous that the blocker is grid, not physics, and that **L6 must be decided before quoting, not after** — which of the rhombic action's quadratic form or the F26 rotation law LPT inverts (they differ by up to 86 % at generic $k$), and whether the redundant link-axis mode is dynamical (**it flips the sign of $b_0$**). Quoting before L6 would be the F287 §6 mistake one level up.

**Also new in the working tree and relevant here:** **F323** (2026-08-17, 28/28, five verified controls) runs *"F299's $d=4$ Casimir successor"* on the BCC action — the infrared companion question F299 §4 named and left unasked. It is a statement about representation content in $d=4$, i.e. the same premise §2 of the companion turns on, and it does not bear on the coupling normalisation either.

**What changed:** after checks 1–4, $d_1$'s job is no longer to choose between two branches six decades apart. It is to **pin $\alpha_s(M_Z)$ inside branch B** and close E3/Q1/Q2. Its two-sided falsifier is unchanged and is now the sharper statement: a completed vertex computation returning $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ outside $[1,7.98]$ falsifies the $g_s=\tfrac12$ lock or the monotonicity assumption — and if it returned $3.4\times10^6$, everything in this document is wrong and CN19 comes back.

---

## 6. Gate status

Everything that does not require `pytest` (absent on the connected machine) or `scipy` is green:

| gate stage | result |
|---|---|
| `casim test --id F298-casimir-ladder` | **PASS**, 9/9 |
| `casim test --id F303-coupling-normalisation` | **PASS**, 9/9 |
| `check_control_soundness.py --run` (full) | 135 controls / 79 records — **87 CONTROL, 0 unsound**, 48 NOCTRL (pre-existing debt, unchanged) |
| `check_control_soundness.py --gate` | **OK** — every declared control well-formed, no stale verdict |
| `check_test_registry.py` | **OK** — 430 records cover 411 test files, all valid |
| `gen_test_registry.py --check` | **OK** after regeneration (the edit made `gauge.yaml`'s generated `evidence:` stale; regenerated, and the diff touches only generated fields) |
| `check_finding_records.py` | **OK** — 316 findings, every declared record exists at its claimed tier; cannot-fail gate entries 5, at the ceiling of 5 |
| `run_gate.py` (full) | **cannot complete here** — its `pytest tests/casim` stage has no `pytest` on this machine |

**Two housekeeping notes for whoever runs the full gate.**

1. The working tree was already dirty on arrival (≈20 modified files from a prior session, including `open-derivations.md`, `changelog.md`, `claims-index.md` and several claim cards). Nothing here touched them.
2. `check_control_soundness.py --run --id X` **overwrites** the journal with only that record's verdicts rather than merging — it left `n_records: 1` after a scoped run, which would have reddened the gate for all 78 other records. Regenerated with a full run. Worth a merge, or a warning in the tool.

---

## 7. What to change, updated from the companion's §7

Unchanged from the companion: **CN18** re-characterised, **CN19** withdrawn, **CL022**'s contingency note lifted, **CL252** gains the branch-A exclusion, **CL257** loses the C7-based leg, **B10** back to fully open, the **$d_1$ row** loses its branch alternative, `link_hamiltonian.py`'s scope note rewritten.

Added by this pass:

| object | change |
|---|---|
| **F111b** | correction note: T7's *"IDENTICAL"* compares a 1-link SU(3) rotor with a 4-link U(1) one; rebuild it at equal $n$, where the exact statement is $s_1^{SU(N)}/s_1^{U(1)}=2/(N^2-1)$. Its **regression-candidate flag is discharged in the working tree** — the artifact has been re-run to **7/7 PASS** with T3/T6/T7 now present and T4 flipped FAIL→PASS, and T7's recorded residual `U(1) cross 1.1e-03` is the number measured independently in §2.3. (Git HEAD still holds the old `3/4 PASS (7 total)` artifact with T6/T7 absent.) |
| **F111b / F299** | F299's cross-reference `[[F111-su3-ladder-casimir-scaling]]` points at no such file; the target is `F111b-tree-gauge-su3-ladder` |
| **F294** | its §"Remains" item 1 was already closed by F111b on 2026-06-07; the finding should say so |
| **F144 A1 step 2** | the claim *"$\chi=1$ is not a convention; it is what the rule's circularity means"* is too strong. Circularity fixes $a=b=\Omega(k)$, hence $\chi=1/\Omega(k)$; $\chi=1$ is F101 §7's normalisation. Restate, and open the $\Omega$-selection as the residual |
| **F99/F100/F101** | carry the exact $\ln((N^2-1)/2)=\ln4$ offset between the implemented $\mathbb Z_3$/U(1) $\sigma_1$ and the $SU(3)$ one |
| `docs/audits/project-audit-inputs-dynamism-2026-06-06.md` | line 41 files the compact rotor under "Derived". Mark stale — it is the only place in the tree that claims this |
| **X1 residual** | *"which $\Omega$ does the single-plaquette rotor carry, on the BCC dispersion?"* — plausibly the same object as F155's $q_\ast$. Replaces "the magnetic side is unaudited", which is now closed |
