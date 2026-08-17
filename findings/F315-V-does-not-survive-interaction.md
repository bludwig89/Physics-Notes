# F315 — F313 falsifier 5 does not fire: the second clock is an artifact of freeness

*2026-08-12 - 11:30 · sector `lattice` · module `casim.engine.lattice.time_signature_interacting` ·
test record `F315-V-interaction` (11/11 PASS, gate tier) ·
results `test-results/F315_V_interaction.json`*

**Target.** F313 falsifier 5, which is also the second of CL269's two contingencies:

> *5. Show $V=\mathbb I\otimes A$ survives the model's interactions — gauge coupling (F68 minimal
> coupling), or the F86 colour dielectric — as a local homogeneous symmetry of the *interacting*
> walk. Then the second dispersive flow is physical and §9's reading is wrong. Conversely, showing
> it does **not** survive would upgrade §9 from residual to result.*

**It does not survive.** The falsifier fails to fire, and §9 is upgraded.

---

## 1. What was open

F313 proved that at the minimal cell $s=2$ the update's commutant splits into exactly the shift
lattice and exactly $\langle A\rangle$, giving $d_\text{time}=\operatorname{rank}\mathfrak{su}(2)=1$.
It then measured a residual at $s=4$: the model's own massive Dirac walk
$D=\bigl(\begin{smallmatrix} nA & im\mathbb I\\ im\mathbb I & nA^\dagger\end{smallmatrix}\bigr)$
commutes with $V=\mathbb I_\text{branch}\otimes A$ at **every** mass
($\lVert[V,D]\rVert\le2.2\times10^{-16}$), so a free composite cell carries two independent clocks.

F313 §9 offered a reading — *$V$ is the $s=2$ update lifted branch-blind, the fundamental clock
beside its mass-dressed self* — and was careful to call it a reading. This finding replaces it with
a measurement.

---

## 2. The question has to be asked in its strong form

*"Does $V$ commute with the interacting evolution?"* is the **weak** form, and answering only it
would have been a mistake. An interacting theory can carry a **deformed** conserved charge —
that is precisely what integrability is — so a symmetry can fail in its free form and still be
present as $Q=Q_1+GQ_2+O(G^2)$. If that happened, the model would still have two times; they would
just be dressed.

Both forms are answered below, and **the second is the one that decides**.

---

## 3. The setting, and why it is fair

Modes are $(k,a)$ with $k$ on the periodic BCC momentum grid and $a$ indexing the **joint**
eigenbasis of $D(k)$ and $V(k)$ — which exists precisely because F313 established $[V,D]=0$. Both
flows are therefore diagonal at once, and each mode carries two phases: $\Omega_a(k)$ (the
evolution) and $\phi^V_a(k)$ (the candidate second clock). Joint-diagonalisation residual
$2.0\times10^{-15}$.

The two-particle basis is **antisymmetrised** and restricted to fixed total momentum $K$. Fixing
$K$ is what keeps the test **homogeneous**: translation invariance is exact throughout, so a
symmetry that fails here cannot blame a broken setup. (This is the trap in the naive version of
the test — switching on a position-dependent background breaks *everything*, including the shifts,
and proves nothing.)

**The reduction is an identity, not an approximation.** Since $\Gamma(V)$ commutes with $\Gamma(D)$
exactly, the interacting one-tick evolution $U=\Gamma(D)e^{-iH_\text{int}}$ obeys

$$[\Gamma(V),U] \;=\; \Gamma(D)\,[\Gamma(V),e^{-iH_\text{int}}],$$

so $V$ survives **iff** $\Gamma(V)$ commutes with $H_\text{int}$; and as $\Gamma(V)$ is diagonal
with eigenvalue $e^{-iq_V}$, that holds iff every nonvanishing matrix element of $H_\text{int}$
connects states of equal $q_V$ **mod $2\pi$**.

---

## 4. Results

| leg | interaction | live elements | $\max\lvert\Delta\phi_V\rvert$ | resonant | obstructed | verdict |
|---|---|---:|---:|---:|---:|---|
| I2 | **mode-diagonal (integrable control)** | 214 | $0.0000$ | 214 | **0** | $V$ **survives** |
| I3 | contact — Hubbard/NJL (F217, F77) | 44 618 | $3.1130$ | 1 930 | **1 340** | $V$ **dies** |
| I4 | photon exchange — F68, $1/q^2$ | 44 618 | $3.1130$ | 1 930 | **1 340** | $V$ **dies** |

- **I1 — free limit.** At $G=0$, $V$ is exactly conserved: the $N=2$ recovery of F313's C7, and the
  positive control that the machinery works.
- **I2 — the test can say "survives".** A deliberately integrable interaction, diagonal in the mode
  basis, leaves $V$ exactly conserved with **zero** obstructed elements. Without this leg a verdict
  of "$V$ dies" would be worthless: a test that always says *dies* has measured nothing.
- **I3/I4 — $V$ is broken, and maximally.** $\max\lvert\Delta\phi_V\rvert\simeq\pi$ — not a small
  violation but the largest a phase difference can be. The verdict is identical for a contact
  kernel and a $1/q^2$ kernel, so it depends on the interaction **being a genuine scatterer**, not
  on its form.

### 4.1 I5 — the deformation is obstructed, which is the decisive leg

At $O(G)$ a deformed charge $Q_1+GQ_2$ requires $[Q_1,H_\text{int}]+[Q_2,H_0]=0$, i.e. per matrix
element $\Delta q_V\,W-\Delta\Omega\,(Q_2)=0$, solvable as

$$Q_2 \;=\; \frac{\Delta q_V\; W}{\Delta\Omega}.$$

So a deformation exists **except** on **resonant** elements, where $\Delta\Omega\equiv0\pmod{2\pi}$
and the denominator vanishes. There $\Delta q_V$ must vanish on its own — and it does not:
**1 340 resonant elements carry $\Delta q_V$ up to $2.876$ rad**. No deformation of $V$ can be
conserved at leading order. $V$ is not merely broken in its free form; it is **unrepairable**.

### 4.2 I6 — the control that makes I5 mean something

On that *same* resonant set, the **evolution's own** charge has $\Delta\Omega=1.8\times10^{-15}$ —
machine zero, by construction. A test that flagged every charge would have flagged this one too.
It does not. The obstruction is specific to $V$.

### 4.3 I7 — robustness

Three momentum sectors $K=(0,0,0),(1,0,0),(1,2,0)$ and both massive ($m=0.37$) and massless
($m=0$): obstructed counts 5 132 / 2 152 / 1 340 and 260 respectively. Same verdict everywhere.

---

## 5. An honest negative — a prediction of mine that was wrong

The $\langle100\rangle$ restriction was **expected to go blind**. The model's on-axis dispersion is
exactly linear (F20/F301; measured here at residual $10^{-16}$), a linear phase is additive under
momentum conservation, and $q_V$ would then be a combination of the momentum charges and survive.

**It does not go blind:** the on-axis run returns **2 592** obstructed elements. The reason is that
the eigenphase is $\arccos$-folded into $(-\pi,\pi]$, so **umklapp destroys additivity even for an
exactly linear branch** — e.g. $(0,0,0)+(2,0,0)\to(1,0,0)+(1,0,0)$ carries $\Delta\phi_V=2\pi/3$.

This is recorded rather than the leg being quietly dropped, because it changes the *mechanism*: the
breaking is not driven by lattice curvature alone, as first supposed, but by the mod-$2\pi$
structure of a QCA eigenphase — which is a stronger and more generic reason, and it is why the
result does not depend on going off-axis.

---

## 6. The $L=2$ trap

On an $L=2$ grid every $\theta_j\in\{0,\pi\}$, so every $\sin\theta_j=0$ and the Bloch vector
vanishes identically: $A(k)=\pm\mathbb I$ everywhere and the walk is **trivial**. Every commutator
is then zero and the test reports "$V$ survives" for a reason that has nothing to do with physics.

This was hit during the work — the first run of the many-body test was at $L=2$ and returned
$\lVert[\Gamma(V),U_\text{int}]\rVert=10^{-16}$, a clean false negative. It is now a declared
control (`L=2` must go **RED**) and it is exactly the shape the F298 idiom names: *a scan that
cannot see the failure cannot claim it.*

---

## 7. What this settles

$V$ is an **artifact of freeness**. A free theory is integrable and its commutant is large; the
model's interactions remove the extra flow, and remove it unrepairably. Therefore:

- **F313 §9's reading is confirmed** — promoted from reading to result.
- **The rank-1 time count is not confined to the minimal cell.** F313 could only claim
  $d_\text{time}=1$ as a theorem at $s=2$, because a free $s=4$ composite carried a second flow.
  That composite is free; the model is not. **The count is the count of the interacting theory at
  any cell.**
- **CL269 loses one of its two contingencies** and keeps the other (Abel's theorem).

---

## 8. What this does not settle

1. **All orders.** I5 is a **leading-order** obstruction. That is the standard and decisive form of
   the no-extra-conserved-charge argument, but it is not an all-orders proof, and this finding does
   not claim one.
2. **The F86 colour dielectric specifically.** Falsifier 5 named two interactions; the contact
   (F77/F217) and photon-exchange (F68) kernels are tested here. The confining non-Abelian sector
   is **not** — it is a harder object and stays named.
3. **Abel's theorem** (F313 §6) is untouched and remains imported.
4. **The arrow of time** remains rubric row A4's problem, exactly as F313 left it.

---

## 9. Falsifiers

1. **Exhibit a nonzero $Q_2$ solving $[Q_1,H_\text{int}]+[Q_2,H_0]=0$ with $Q_1=q_V$** — i.e. show
   the 1 340 resonant obstructions are an artifact of the resonance tolerance rather than exact
   degeneracies. §4.1 dies.
2. **Show the resonant set is empty at a defensible tolerance.** The obstruction claim then has no
   content. (This is the `res_tol=0.0` control, declared and verified RED.)
3. **Exhibit a model interaction under which $V$ survives** — a genuine scatterer, not
   mode-diagonal. §7 dies.
4. **Show the F86 colour dielectric conserves $q_V$.** The confining sector would then restore the
   second flow that the Abelian sectors remove; §8.2 becomes a result against this finding.
5. **Show the obstruction vanishes as $L\to\infty$** — i.e. that it is a finite-grid umklapp
   artifact with no continuum counterpart. Given §5 this is the most interesting attack on the
   finding, and it is not answered here.

---

## 10. Provenance

- Module: `src/casim/engine/lattice/time_signature_interacting.py` (`lattice` sector,
  `exactness=machine`, `_SPINE`, D11). Explicit complex arithmetic; no chiral transform is
  delegated to a library routine (CLAUDE.md).
- Test record: `F315-V-interaction`, `kind: assertion`, `tier: gate`, entry `check_all`, 11/11 PASS,
  with **three declared controls** (`L=2`, `kind=mode_diagonal`, `res_tol=0.0`), each verified RED.
- Runner: `tests/runners/run_f315_v_interaction.py` → `test-results/F315_V_interaction.json`.
- Claim card: **CL269** updated (one contingency discharged); **CL270** issued for this result.
- Reads: F313 (§9 and falsifier 5 — the target), F291, F20/F301 (exact on-axis linearity), F68
  (minimal coupling), F77 (NJL four-fermion), F217 (the Hubbard on-site vertex), F86 (named, not
  tested).
- **Supersedes nothing.** F313 is left bit-unchanged; per D12 the object that moves is the claim
  card, not the finding.
