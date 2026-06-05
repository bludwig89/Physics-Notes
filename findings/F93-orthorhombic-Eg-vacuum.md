# F93 — The orthorhombic vacuum identified: an $E_g$ condensate on the second-neighbour shell — unique non-mixing splitting channel, $D_{2h}$ stabilizer ($\kappa$-removal as a theorem), the sextic Landau criterion, and proof the break must be spontaneous

**Date:** 2026-06-04 - 20:40
**Status:** Partial (major reframing) — 8/8 checks PASS. **What is exact:** the crystal field that splits the F75 $T_{1u}$ generation triplet into three distinct masses *without mixing axes* is **uniquely the $E_g$ channel** (O1); its minimal lattice home is the **BCC second-neighbour (cube-axis) shell** — the first shell contains no $E_g$ at all (O2); a generic-angle $E_g$ condensate leaves stabilizer $D_{2h}$ with **no residual axis permutation**, so no symmetry can generate the democratic stiffness $\kappa$ — F84's flatness becomes a stabilizer theorem (O3); F76-C6's $Z_3$ parametrization **is** an $E_g$ condensate at angle $\delta$, exactly (O4); and the vacuum dispersion (including the F30 anisotropy) is exactly $O_h$-symmetric, so it supplies **zero** explicit $E_g$ field — the break **must be spontaneous** (O6). **What is mechanism, not derivation:** the Landau theory (O5) gives the exact criterion for the orthorhombic phase to win — sextic invariant required, $C>0$ and $|B|<2C$, with $\cos3\delta^*=-B/(2C)$ — but the coefficients are not derived from the QCA rule. The data (O7) give $\delta=12.73°$ (generic — orthorhombic confirmed), amplitude ratio $\sqrt2$ to $10^{-5}$, and the one remaining free number $\cos3\delta=-B/(2C)=0.7859$. See §8.
**Script:** `model-tests/test_F93_orthorhombic_Eg_vacuum.py` (~2 s)
**Results:** `test-results/F93_orthorhombic_Eg_vacuum.json`
**Cross-references:** [[F84-flatness-from-orthorhombic-break]] (irreducible input #2, the target), [[F76-generation-mass-hierarchy-crystal-field]] (C1 orthorhombic requirement; C6 $Z_3$ form), [[F75-three-generations-from-bcc-irrep-selection]] ($T_{1u}$ triplet; the $O_h$ machinery), [[F78-koide-amplitude-from-cooper-pair]] (B3: symmetric dynamics give the democratic floor — consistent with O5b), [[F30-photon-dispersion-order-anisotropy-birefringence]] (the anisotropy O6 shows is $O_h$-symmetric, hence *not* the break), [[F49-bcc-finite-k-weinberg-angle]] (the second shell reappears), [[F92-per-constituent-phase-consistency]] (companion finding on input #1), [[F95-B-derived-C-localized]] (2026-06-04: the §8 open problem half-closed — $B$ derived from the QCA Dirac sea, closed form $-3\sqrt2 I_2\bar y^4$ with the correct sign; $C$ proven impossible from any per-axis loop and localized to the second-shell condensate's own sextic self-interaction, required size $0.636|B|$).

---

## 1. The target

F84 bottomed the F75→F84 descent out at two irreducible inputs. Input #2:

> **The orthorhombic vacuum** — the lattice ground state has three
> inequivalent axes. This single fact gives the three generations (F75), their
> distinctness (F76-C1), and the flat $\phi$ / $\kappa\to0$ that fixes
> $Q=2/3$ (F82/F84).

"Orthorhombic vacuum" was a name, not a theory: no statement of *what object*
breaks the symmetry, *where it lives* on the lattice, *why three distinct
axes* rather than the crystallographically common tetragonal $[2,1]$, or *why*
the break is not simply inherited from the BCC dispersion anisotropy (F30).
This finding answers all four structurally, and reduces the dynamical question
to one Landau criterion plus one number.

## 2. O1 (exact) — the splitting field is uniquely $E_g$

The generation mass operator lives on the $T_{1u}$ triplet. Its possible
crystal-field perturbations form the symmetric product

$$\mathrm{sym}(T_{1u}\otimes T_{1u}) \;=\; A_{1g}\ \oplus\ E_g\ \oplus\ T_{2g}
\qquad (\text{Schur degeneracies } [1,2,3],\ \text{verified}),$$

with the exact identification (integer arithmetic over the 48 $O_h$ ops):
$A_{1g}$ = the trace (shifts all three masses equally — no split); $E_g$ = the
**diagonal-traceless** doublet (splits the three axes *without mixing them*);
$T_{2g}$ = the off-diagonal triplet (only mixes axes). Therefore:

$$\boxed{\ \text{three distinct masses without axis mixing}\iff\text{a nonzero }E_g\text{ field}\ }$$

The "orthorhombicity $s$" of F76/F84 *is* an $E_g$ condensate. This is forced
by representation theory, not chosen.

## 3. O2 (exact) — it lives on the second-neighbour shell

Decomposing the BCC shells by Schur averaging (exact integer permutation
representations):

| shell | sites | decomposition | contains $E_g$? |
|---|---|---|---|
| 1st (cube vertices) | 8 | $A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$ $[1,1,3,3]$ | **no** |
| 2nd (cube axes) | 6 | $A_{1g}\oplus E_g\oplus T_{1u}$ $[1,2,3]$ | **yes** |

The first shell — the one the F27 mass step couples to, which supplied the
generation triplet (F75) — **cannot carry the splitting field at all**. The
minimal lattice home of the orthorhombic order parameter is the
second-neighbour shell: an occupation/bond imbalance among the three cube
axes. (The explicit doublet $\{s_x-s_y,\ s_x+s_y-2s_z\}$, $s_a=f(+a)+f(-a)$,
is verified invariant and inversion-even.) Notably this is the same second
shell whose bond-axis counting produced F49's $\sin^2\theta_W=2/9$ — two
independent roles for the same geometric object.

## 4. O3 (exact) — $\kappa$-removal is a stabilizer theorem

For the mass operator $M(\delta)=m_0 I+e\,\mathrm{diag}(d_a)$,
$d_a=\cos(\delta-2\pi(a-1)/3)$, counting the $O_h$ elements with
$RMR^T=M$:

| $\delta$ | stabilizer | order | axis-permuting elements | masses |
|---|---|---|---|---|
| generic (e.g. $12.7°$) | $D_{2h}$ | 8 | **0** | three distinct |
| $0°$ (mod $60°$) | $D_{4h}$ | 16 | 8 | $[2,1]$ degenerate |
| $30°$ (max ortho) | $D_{2h}$ | 8 | 0 | three distinct |

At a generic condensate angle the residual group is $D_{2h}$ = the eight sign
matrices — it contains **no nontrivial axis permutation**. The generation
permutation symmetry $S_3$ is *completely* broken, so no symmetry exists that
could generate a restoring force toward the democratic point: **F84's
$\kappa=0$ is now a theorem about the stabilizer**, not an inference from the
data. Conversely at $\delta\equiv0\ (\mathrm{mod}\ 60°)$ a residual swap
survives, two masses are forced degenerate, and a protected $\kappa$ exists —
exactly F84's interpolation endpoints, now group-theoretic.

**Genericity inversion.** Three-distinct-masses is the *generic* state of an
$E_g$ condensate ($\delta$ off a measure-zero set); the tetragonal $[2,1]$
case is the fine-tuned one. "Why orthorhombic?" inverts to "why would it be
anything else, once $E_g$ condenses at a generic angle?" — the burden shifts
to the angle selection (§6).

## 5. O4 (exact) — F76-C6 *is* the $E_g$ condensate

With $E_1=\mathrm{diag}(2,-1,-1)/\sqrt6$, $E_2=\mathrm{diag}(0,1,-1)/\sqrt2$
and $(e_1,e_2)=e(\cos\delta,\sin\delta)$, the diagonal shifts are **exactly**

$$d_a=e\,\sqrt{\tfrac23}\,\cos\!\big(\delta-\tfrac{2\pi(a-1)}{3}\big)\qquad(\text{sympy residual }0),$$

i.e. F76-C6's celebrated $Z_3$ form $\sqrt{m_a}=M_0\big[1+\sqrt2\cos(\delta+2\pi a/3)\big]$
is, term for term, *an $A_{1g}$ background plus an $E_g$ condensate at angle
$\delta$*. F76's fitted phase was the condensate angle all along, and the
$\sqrt2$ amplitude is the $45°$ equipartition (F80/F92), not a separate input.

## 6. O5 (mechanism) — when the orthorhombic phase wins: the sextic criterion

The most general $O_h$-invariant Landau energy for the $E_g$ doublet through
sixth order is

$$F(e,\delta)=\tfrac r2 e^2+\tfrac b3 e^3\cos3\delta+\tfrac u4 e^4+\tfrac w6 e^6\cos^23\delta .$$

At fixed $e$ the angle part is $f=B\cos3\delta+C\cos^23\delta$ with
$B=be^3/3$, $C=we^6/6$, so:

$$\boxed{\ \text{orthorhombic (generic }\delta^*\text{, three distinct masses)}\iff C>0\ \text{and}\ |B|<2C,\quad \cos3\delta^*=-\tfrac{B}{2C}\ }$$

otherwise the minimum sits at $\delta^*\equiv0\ (\mathrm{mod}\ 60°)$
(tetragonal-type $[2,1]$). Verified against numerical global minimization over
a $13\times13$ $(b,w)$ grid with **zero mismatches**; corollaries:

- **the quartic theory can never do it** — at $w=0$ the cubic invariant
  $e^3\cos3\delta$ always locks $\delta$ to a multiple of $60°$ (0 orthorhombic
  points found); the sextic invariant is structurally required;
- $b=0$, $w>0$ gives the maximal orthorhombic point $\delta^*=30°$ exactly;
- **O5b (negative control):** a $T_{1u}$ *vector* condensate at quartic order
  points only along $(111)$ or $(100)$ — a vector order parameter cannot
  orthorhombify the vacuum; the $E_g$ channel is not optional. (Consistent
  with F78-B3's democratic-floor result for flavour-symmetric dynamics.)

## 7. O6 (machine-exact) — the break must be spontaneous

For 10 random $k$ and all 48 $O_h$ operations, the BCC dispersion satisfies
$\{\omega^+(Rk),\omega^-(Rk)\}=\{\omega^+(k),\omega^-(k)\}$ to
$4.7\times10^{-16}$. The vacuum dispersion — *including* the F30 body-diagonal
anisotropy — is exactly $O_h$-symmetric, i.e. **cubic-anisotropic but not
orthorhombic**: it carries zero $E_g$ component. The orthorhombic field cannot
be inherited from the lattice geometry or dispersion; it must arise by
**spontaneous condensation** (the O5 mechanism) or be external. This closes a
loophole F76 left open ("any vacuum strain… supplies the $D_{2h}$ field" — the
strain cannot come from the dispersion itself).

## 8. O7 (data) — the condensate angle, and what remains free

From the PDG charged leptons ($y=\sqrt m$, $Z_3$ Fourier):

| quantity | value | meaning |
|---|---|---|
| $\delta_\text{data}$ | $12.7328°$ | generic — $12.7°$ from the nearest tetragonal point: **orthorhombic confirmed** |
| $A/\bar y$ | $1.414201$ vs $\sqrt2=1.414214$ | the $45°$ equipartition (F80/F92), to $10^{-5}$ |
| mass reconstruction | $1.8\times10^{-14}$ rel | the $E_g$+$A_{1g}$ form is exact on the data |
| $\cos3\delta=-B/(2C)$ | $0.785874$ | **the one remaining free number** |

*Numerical note (flagged, not used):* $\delta_\text{data}=0.22224$ rad is
numerically close to $2/9=0.22222$ rad ($12.7324°$), the phase long noted in
the Koide literature; if a future derivation of the Landau ratio lands on
$\cos(2/3)$… it would fix $-B/2C=0.785887$. Recorded as a target, not a claim.

**What remains free, sharply:** F76's free phase $\delta$ is now the **ratio
of two Landau coefficients**, $\cos3\delta^*=-B/(2C)$, i.e. the relative
strength of the cubic and sextic $E_g$ invariants of the second-shell
condensate — plus the fact of condensation itself ($r<0$, $C>0$, $|B|<2C$).
Deriving $B$ and $C$ from the QCA rule (a gap computation in the second-shell
$E_g$ channel) is the single dynamical step that would make the entire
charged-lepton spectrum — count, distinctness, $Q=2/3$, *and* the individual
mass ratios — an output of the lattice. That is the sharpest formulation of
the model's deepest open problem to date.

## 9. Falsifiable structural commitments

1. Any inter-generation mixing operator the model builds must come from the
   **second-shell $E_g$/$T_{2g}$ channels**; $T_{2g}$ (axis-mixing) is the
   unique channel for off-diagonal (CKM/PMNS-like) structure — a constraint on
   admissible mixing textures.
2. If the second-shell gap computation produces $|B|>2C$, the model predicts a
   tetragonal $[2,1]$ lepton spectrum — falsified by the data; the criterion
   is sharp enough to kill the mechanism.
3. The $E_g$ condensate is inversion-even and lives on bonds, not sites: it
   does not break parity or translation — consistent with the unbroken
   $C/P/CP$ structure of F53.

## 10. Test summary (`test_F93_orthorhombic_Eg_vacuum.py`, 2026-06-04 - 20:33)

| Check | Statement | Result | Status |
|---|---|---|---|
| O1 | $\mathrm{sym}(T_{1u}^{\otimes2})=A_{1g}\oplus E_g\oplus T_{2g}$; $E_g$ = unique non-mixing splitter | $[1,2,3]$; diag sector exactly invariant | PASS |
| O2 | shell homes: 1st $[1,1,3,3]$ (no $E_g$); 2nd $[1,2,3]$ ($E_g$) | exact | PASS |
| O3 | generic $\delta$: $\lvert\text{stab}\rvert=8$, 0 axis perms; $\delta=0$: 16, swap present | exact counts | PASS |
| O4 | $E_g$ doublet $\equiv$ $Z_3$ cosine shifts (F76-C6) | sympy residuals $0$ | PASS |
| O5 | Landau: ortho iff $C>0,\ \lvert B\rvert<2C$; quartic never; $b=0\Rightarrow30°$ | 0/169 mismatches | PASS |
| O5b | quartic $T_{1u}$ vector OP: only $(111)$/$(100)$ | confirmed | PASS |
| O6 | dispersion exactly $O_h$-symmetric ⇒ zero explicit $E_g$ | $4.7\times10^{-16}$ | PASS |
| O7 | data: $\delta=12.7328°$ generic; $A/\bar y=\sqrt2$ ($10^{-5}$); $\cos3\delta=0.7859$ | PASS | PASS |

**Overall 8/8 PASS** (~2 s).

## 11. Provenance

- New content: the $E_g$ identification of the orthorhombic order parameter
  (O1), its second-shell home (O2), the stabilizer theorem for $\kappa$-removal
  (O3), the C6$\equiv E_g$ identity (O4), the sextic Landau criterion and the
  quartic no-go's (O5/O5b), the dispersion-spontaneity proof (O6), and the
  reduction of F76's phase to a Landau-coefficient ratio (O7).
- Group machinery follows F75 (here: the 48 signed permutation matrices,
  exact integers). Dispersion via `ca_bcc.bcc_dispersion`.
- Verification: `model-tests/test_F93_orthorhombic_Eg_vacuum.py`
  (2026-06-04 - 20:33, 8/8 PASS), results
  `test-results/F93_orthorhombic_Eg_vacuum.json`.
- Masses: PDG ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV).
