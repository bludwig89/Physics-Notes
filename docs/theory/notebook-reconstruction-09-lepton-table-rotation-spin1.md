# Notebook Reconstruction — Batch 09: EM/Weak Lepton-Doublet Table,
# Monopole/Confinement Analogies, Rotation-Matrix Tensor Products, Spin-1
# Clebsch–Gordan, 3D "Dirac" Equation (pp. 92–101)

Cold, independent reconstruction of `references/physics-notes-complete.md` pages 92–101
(NB-120 – NB-129). Continues directly from batch 08 (NB-100 – NB-119, pp.78–91). Per the
governing prompt's firewall, this batch does not consult `findings/`, `docs/claims/`, or any of
the other excluded files; the only inputs used are the notebook transcription itself and
standard-textbook electroweak theory / representation theory, verified independently with sympy.

Date-time stamp: 2026-09-22 - (batch 09).

Scripts: `tests/runners/notebook-recon/run_NB-120_lepton_doublet_table.py`,
`run_NB-121_122_monopole_confinement_analogies.py`,
`run_NB-123_124_125_rotation_tensor_products.py`,
`run_NB-126_127_spin1_clebsch_gordan.py`,
`run_NB-128_129_3d_dirac_riemann_silberstein.py`.
Results: `test-results/notebook-recon/NB-120_lepton_doublet_table.json` and four companion JSON
files with matching names.

---

## NB-120 (pp.92–97) — The 8-Component Lepton-Doublet EM/W Table: **Confirmed Exactly**

**Notebook:** decomposes the electron+neutrino Dirac fields into 8 chiral × particle/antiparticle
Weyl components ($e_R^-, e_L^+, e_R^+, e_L^-, \nu_R, \bar\nu_L, \bar\nu_R, \nu_L$) and tabulates
which ones couple to EM and/or the weak $W$, finding exactly 2 states that couple to both, 2 to EM
only, 2 to $W$ only, and 2 to neither — calling this "a very symmetric representation."

**Reconstruction.** Built the electroweak $(T_3, Y)$ quantum-number assignment for the four
"primary" chiral fields from the textbook Standard Model doublet/singlet structure alone
($L=(\nu_L,e_L)$: $T_3=\pm\tfrac12$, $Y=-\tfrac12$; $e_R$: $T_3=0,Y=-1$; $\nu_R$: $T_3=0,Y=0$),
generated the four charge-conjugate partners by the standard $C$ rule (flip every additive charge,
flip chirality), and applied two purely group-theoretic rules with **no reference to the
notebook's own table**: EM coupling iff $Q=T_3+Y\ne0$; $W$ coupling iff $T_3\ne0$ (nontrivial
$SU(2)_L$ doublet membership).

**Verified** (`run_NB-120_lepton_doublet_table.py`): all 8 derived (EM, W) coupling flags match
the notebook's table **exactly**, including the two non-obvious cross-assignments — $e_R^+$
(right-handed positron) and $\bar\nu_R$ couple to $W$ because they are the $C$-conjugates of the
left-handed doublet members $e_L^-,\nu_L$, while $e_L^+$ and $\bar\nu_L$ (conjugates of the
right-handed singlets) do not. Category counts (2 both / 2 EM-only / 2 $W$-only / 2 neither) also
match exactly.

**Verdict: SOLID.** This is a completely standard, correctly-executed piece of electroweak
bookkeeping — an accurate and, per the notebook's own framing, deliberately "symmetric"
presentation of facts that most textbook treatments state less explicitly.

## NB-121/NB-122 (p.97) — Monopole and Confinement Analogies

**Notebook:** "the neutrino would be the magnetic monopole that doesn't exist" (both are the
"missing" member of an otherwise-populated set of charge states); and quark confinement likened to
orbital-angular-momentum quantization (integer $L$ only) forcing "intrinsic" fractional charges to
stay hidden, the way half-integer spin is allowed only as an intrinsic (not orbital) property.

**Assessment** (`run_NB-121_122_monopole_confinement_analogies.py`). Both analogies rest on
individually correct facts (no observed right-handed weak current; no observed magnetic monopole;
$L\in\{0,1,2,\dots\}$ strictly while $S$ may be half-integer) but neither analogy is a structural
equivalence: the missing right-handed current is a dynamical/representation choice (nothing
prevents writing it down; the SM simply doesn't gauge it), while the absent monopole is a
topological fact about the trivial $U(1)$ bundle — a qualitatively different kind of "missing."
Likewise, quark confinement is a strong-coupling dynamical effect (the linear QCD flux-tube
potential), not a representation-theoretic selection rule of the kind that forbids half-integer
orbital angular momentum. The notebook's own language ("might... provide important clues,"
"perhaps... under a Heisenberg-like arrangement") is appropriately tentative and does not overclaim
a mechanism. **Verdict: NOT-TESTABLE (both)** — apt, self-aware analogies, not closed claims.

---

## NB-123/NB-124/NB-125 (p.98) — Rotation-Matrix Tensor Products

### NB-123: $R_z\otimes R_z$ — **Confirmed Exactly**

**Notebook:** $R_z(\theta)=\mathrm{diag}(e^{i\theta/2},e^{-i\theta/2})$, and
$R_z\otimes R_z=\mathrm{diag}(e^{i\theta},1,1,e^{-i\theta})$.

**Verified** (sympy matrix exponential + Kronecker product, no reference to the notebook's
algebra): both the single-particle $R_z$ and the tensor product match exactly. **Verdict: SOLID.**

### NB-124: $R_x(\phi)=\exp(i\sigma_x\phi/2)$ — **A Transcription Error Found and Traced Through**

**Notebook:** states
$R_x(\phi)=\begin{pmatrix}i\sin\phi/2 & \cos\phi/2\\ \cos\phi/2 & i\sin\phi/2\end{pmatrix}$.

**Reconstruction.** The standard matrix exponential of a Pauli generator,
$\exp(i\sigma_x\alpha)=\cos\alpha\,\mathbb I+i\sin\alpha\,\sigma_x$, gives
$\begin{pmatrix}\cos(\phi/2) & i\sin(\phi/2)\\ i\sin(\phi/2) & \cos(\phi/2)\end{pmatrix}$ —
the diagonal and off-diagonal entries are **swapped** relative to the notebook's version.

Rather than stop there, this reconstruction traced the error's *consequences* by building the
tensor product two ways: (1) from the correct matrix, and (2) from the notebook's own (swapped)
matrix, to see whether the notebook's subsequent algebra is at least self-consistent. **Result:**
the notebook's own stated $4\times4$ tensor product **does** follow exactly from its own (wrong)
$R_x$ — the swap doesn't introduce a *second* independent error at that step. The real second
error surfaces one step later: the "double-angle simplified" final matrix replaces the cross term
$i\sin(\phi/2)\cos(\phi/2)$ with $2i\sin\phi$ where the correct half-angle identity gives
$i\sin(\phi/2)\cos(\phi/2)=\tfrac{i}{2}\sin\phi$ — **the notebook's simplification is exactly a
factor of 4 too large.** Substituting the correct $\tfrac12\sin\phi$ factor into the "simplified"
matrix reproduces the notebook's own pre-simplification tensor product exactly.

**Verdict: INCORRECT (as transcribed) / SOLID-WITH-CORRECTION.** Two findable, independent slips:
(1) $R_x(\phi)$'s diagonal/off-diagonal entries are swapped relative to the standard
$\exp(i\sigma_x\phi/2)$; (2) the final "double-angle" simplification is exactly $4\times$ too
large in its cross term. Neither propagates past this page (the boxed spin-1/2 rotation matrices
are not reused numerically anywhere later in this batch).

### NB-125: $R_y(\phi)\otimes R_y(\phi)$ — **Left Incomplete; Completed Here**

**Notebook:** $R_y(\phi)=\begin{pmatrix}\sin\phi/2 & \cos\phi/2\\ -\cos\phi/2 & -\sin\phi/2\end{pmatrix}$,
tensor product computed, "left incomplete" (no double-angle reduction attempted, unlike NB-124).

**Reconstruction.** The same diagonal/off-diagonal-swap pattern as NB-124 recurs: the correct
$\exp(i\sigma_y\phi/2)=\begin{pmatrix}\cos(\phi/2)&\sin(\phi/2)\\-\sin(\phi/2)&\cos(\phi/2)\end{pmatrix}$
has $\cos$ on the diagonal and $\sin$ off it — the reverse of the notebook's matrix. Building the
tensor product from the notebook's own (swapped) $R_y$ and comparing element-by-element to its
own stated $4\times4$ result finds one further internal mismatch beyond the swap (one entry
transcribed as $\cos^2(\phi/2)\sin(\phi/2)$ where the notebook's own input matrix would give
$-\sin(\phi/2)\cos(\phi/2)$) — most likely a transcription slip on an already-terse, unfinished
page rather than a second conceptual error. Completing the derivation independently (this
reconstruction's own contribution, since the page stops before any simplification): the correctly
computed $R_y\otimes R_y$, using the standard $\exp(i\sigma_y\phi/2)$, is
$$
R_y\otimes R_y=\begin{pmatrix}
\cos^2\tfrac\phi2 & \sin\tfrac\phi2\cos\tfrac\phi2 & \sin\tfrac\phi2\cos\tfrac\phi2 & \sin^2\tfrac\phi2\\
-\sin\tfrac\phi2\cos\tfrac\phi2 & \cos^2\tfrac\phi2 & -\sin^2\tfrac\phi2 & \sin\tfrac\phi2\cos\tfrac\phi2\\
-\sin\tfrac\phi2\cos\tfrac\phi2 & -\sin^2\tfrac\phi2 & \cos^2\tfrac\phi2 & \sin\tfrac\phi2\cos\tfrac\phi2\\
\sin^2\tfrac\phi2 & -\sin\tfrac\phi2\cos\tfrac\phi2 & -\sin\tfrac\phi2\cos\tfrac\phi2 & \cos^2\tfrac\phi2
\end{pmatrix},
$$
which double-angle-reduces the same way NB-124's should have (cross terms $\to\tfrac12\sin\phi$,
not $2\sin\phi$).

**Verdict: INCORRECT (as transcribed) / SOLID-WITH-CORRECTION** — same swap pattern as NB-124,
plus one further transcription mismatch; the unfinished derivation is completed above to a closed
result.

---

## NB-126 (p.99) — Real Spin-1 Matrices and Pauli Tensor Products: **Confirmed Exactly**

**Notebook:** explicit $3\times3$ real-Cartesian $S_x,S_y,S_z$ (the standard $L=1$ generators),
and $\sigma_x\otimes\sigma_x,\sigma_y\otimes\sigma_y,\sigma_z\otimes\sigma_z$ ($4\times4$).

**Verified** (`run_NB-126_127_spin1_clebsch_gordan.py`): $S_x,S_y,S_z$ satisfy
$[S_i,S_j]=i\epsilon_{ijk}S_k$ exactly and have Casimir $S^2=2\,\mathbb I$ (the correct $s(s+1)=2$
for spin 1); all three Pauli tensor products match the notebook's stated matrices exactly.
**Verdict: SOLID.**

## NB-127 (pp.99–100) — Block-Diagonalizing into Spin-1 ⊕ Spin-0: **A Genuine, Self-Detectable Error Found and Corrected**

**Notebook:** states the goal as turning "$\sigma_z\otimes\sigma_z$ etc. into
$\begin{pmatrix}0&\cdot\\\cdot&S_x\end{pmatrix}$" via a stated $3\times3$ real orthogonal transform
$A=\tfrac1{\sqrt2}\begin{pmatrix}1&0&1\\0&\sqrt2&0\\1&0&-1\end{pmatrix}$, giving new-basis
$S_x=\begin{pmatrix}0&1&0\\1&0&1\\0&1&0\end{pmatrix}$,
$S_y=\begin{pmatrix}0&-i&0\\i&0&-i\\0&i&0\end{pmatrix}$, $S_z=\mathrm{diag}(1,0,-1)$.

**Reconstruction, two independent checks:**

1. **Literal reading — transform the tensor *products*.** Built the full unitary $4\times4$
Clebsch–Gordan matrix $U$ mapping the product basis $(|{+}{+}\rangle,|{+}{-}\rangle,|{-}{+}\rangle,|{-}{-}\rangle)$
to the coupled basis $(|1,1\rangle,|1,0\rangle,|1,{-}1\rangle,|0,0\rangle)$, and computed
$U(\sigma_z\otimes\sigma_z)U^\dagger$. **Result: this does NOT give $\mathrm{diag}(1,0,-1)$ on the
triplet block** — it gives eigenvalues $\pm1$ unrelated to the $S_z$ pattern (confirmed exactly:
$\sigma_z\otimes\sigma_z$ is a *product* operator, not a *sum*, and block-diagonalizing a product
operator has nothing to do with total-spin quantum numbers). **The page's own prose is imprecise**
— literally transforming $\sigma_i\otimes\sigma_i$ does not produce the spin-1 generators.

2. **Standard construction — transform the *sum* (total spin).** Built
$S_i^{\rm tot}=(\sigma_i\otimes\mathbb I+\mathbb I\otimes\sigma_i)/2$ (angular-momentum addition,
$\tfrac12\otimes\tfrac12=1\oplus0$) and applied the same $U$. **Result: $S_z^{\rm tot}$ reduces
EXACTLY to the notebook's stated $\mathrm{diag}(1,0,-1)$ on the triplet block, and $S_x^{\rm tot},
S_y^{\rm tot}$ reduce to the notebook's stated matrices up to a missing overall factor of
$1/\sqrt2$.**

3. **Independent internal-consistency check, with no external derivation at all:** do the
notebook's own stated $S_x,S_y,S_z$ satisfy their own $\mathfrak{su}(2)$ algebra? **No** —
$[S_x,S_y]=2iS_z$ (should be $iS_z$), and the Casimir $S_x^2+S_y^2+S_z^2$ has diagonal entries
$(3,4,3)$, not a scalar multiple of the identity as it must be for a genuine spin operator. This is
detectable from the page's own numbers alone, independent of any comparison to the "correct"
construction. **Dividing $S_x$ and $S_y$ each by $\sqrt2$ fixes both defects exactly**
(commutator becomes $iS_z$ exactly; Casimir becomes $2\,\mathbb I$ exactly) — the same correction
found by the Clebsch–Gordan route in step 2, arrived at two independent ways.

**Verdict: SOLID-WITH-CORRECTION.** $S_z=\mathrm{diag}(1,0,-1)$ is exactly correct as written and
needs no fix. $S_x,S_y$ each carry a missing $1/\sqrt2$ normalization factor, confirmed two
independent ways (external Clebsch–Gordan re-derivation, and internal $\mathfrak{su}(2)$-algebra
self-consistency). The stated $3\times3$ transform $A$ is itself genuinely orthogonal. The page's
framing ("transform $\sigma_i\otimes\sigma_i$") is imprecise — the construction that actually
works is the *sum*, $S_i^{\rm tot}=(\sigma_i\otimes\mathbb I+\mathbb I\otimes\sigma_i)/2$, standard
angular-momentum addition, not a literal transform of the tensor products written two lines
earlier on the same page.

---

## NB-128 (pp.100–101) — "3D Dirac Equation" $\partial_t\psi_\pm=\mp c\,\mathbf S\cdot\nabla\psi_\pm$: **Confirmed, Using NB-127's Own (Uncorrected) Matrices**

**Notebook:** builds $\mathbf S\cdot\nabla$ from the immediately-preceding page's spin-1 matrices
and displays both the boxed $3\times3$ matrix of partial derivatives and its componentwise
expansion acting on $\psi_+=(\psi_+^1,\psi_+^2,\psi_+^3)$.

**Verified** (`run_NB-128_129_3d_dirac_riemann_silberstein.py`): tested against *two* candidate
generator sets — the raw Cartesian $S_x,S_y,S_z$ of NB-126, and NB-127's "new-basis" matrices
(taken literally as transcribed, i.e. *without* the $1/\sqrt2$ correction just found above).
**The notebook's boxed matrix and its componentwise expansion match NB-127's new-basis generators
exactly** (not the Cartesian ones) — the author is carrying the immediately preceding
construction forward, consistently, rather than restarting from the Cartesian generators two
pages back. **Verdict: SOLID.**

## NB-129 (p.101) — Margin Note "if $\psi_+=E+iB$": **An Exactly Correct, Independently Verifiable Physical Claim — With an Honest Caveat About Which Basis It Needs**

**Notebook:** a single unelaborated margin line, "if $\psi_+=E+iB$ [note for further
investigation]" — no derivation, immediately followed by the end of the extractable material on
this page.

**Reconstruction.** This is the classical **Riemann–Silberstein-vector** construction (later
revived in the "photon wavefunction" literature, e.g. Bialynicki-Birula): the complex combination
$\mathbf F=\mathbf E+i\mathbf B$ satisfies a single first-order evolution equation built from the
angular-momentum-1 generators that is exactly equivalent to the *pair* of source-free Maxwell curl
equations. Verified in two steps: (1) using the **raw Cartesian** $S_x,S_y,S_z$ from NB-126,
$\mathbf S\cdot\nabla\,\mathbf F=+i(\nabla\times\mathbf F)$ **exactly**, for a fully general
symbolic vector field (confirmed by direct symbolic differentiation, no approximation); (2)
substituting $\psi_+=\mathbf E+i\mathbf B$ into $\partial_t\psi_+=-c\,\mathbf S\cdot\nabla\psi_+$
built from these Cartesian generators, the real and imaginary parts separate **exactly** into
$\partial_t\mathbf E=c\,\nabla\times\mathbf B$ (Ampère, source-free) and
$\partial_t\mathbf B=-c\,\nabla\times\mathbf E$ (Faraday) — the complete vacuum Maxwell curl
system, confirmed by exact symbolic cancellation, not approximation.

**One honest caveat, found by checking rather than assuming:** this clean reduction requires the
**Cartesian** ($S_x,S_y,S_z$ of NB-126) generators. NB-128's own displayed matrix — confirmed
above to use NB-127's *rotated* ("new-basis") generators instead — does **not** give a clean
Maxwell split if $\psi_+^1,\psi_+^2,\psi_+^3$ are literally identified with Cartesian
$E_1{+}iB_1,E_2{+}iB_2,E_3{+}iB_3$ component-by-component (verified: the resulting expression is a
genuine mix of $\partial_i E_j$ and $\partial_i B_j$ terms that does not separate into recognizable
curl components). The two pages use two different, though related, bases for "$\mathbf S$," and
the margin note's claim is correct precisely in the basis where the physics is transparent (NB-126's
Cartesian one) — not automatically as a literal next line continuing NB-128's own equation.

**Verdict: SOLID (as an independent, verifiable physical claim)** — a genuinely correct piece of
classical electrodynamics that the author flagged with a single margin line and never followed up,
best read as an independent flash of insight rather than a completed derivation chained onto the
immediately preceding page.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-120 | SOLID |
| NB-121 | NOT-TESTABLE |
| NB-122 | NOT-TESTABLE |
| NB-123 | SOLID |
| NB-124 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-125 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-126 | SOLID |
| NB-127 | SOLID-WITH-CORRECTION |
| NB-128 | SOLID |
| NB-129 | SOLID (independent claim; basis caveat noted) |

**What closed:** NB-120's lepton-doublet EM/W table is exactly reproduced from SM group theory
alone, including its two non-obvious cross-assignments. NB-124/NB-125's rotation matrices both
carry the same diagonal/off-diagonal sin↔cos swap relative to the standard
$\exp(i\sigma\phi/2)$ formula, and NB-124's subsequent "double-angle simplification" carries an
independent, exact factor-of-4 error in its cross term — both traced to precise, quantified
corrections. NB-125's incomplete derivation is carried to a closed result. NB-127 contains a
genuine, two-ways-confirmed error (a missing $1/\sqrt2$ on two of three new-basis spin matrices) —
found first by external re-derivation via the correct (sum, not product) Clebsch–Gordan
construction, then independently confirmed by the new-basis triple's own internal
$\mathfrak{su}(2)$-algebra self-consistency, with both methods agreeing on the identical fix.
NB-128 is confirmed to build correctly on NB-127's own (uncorrected) matrices, and NB-129's
one-line margin note is confirmed to be an exactly correct, well-known piece of physics (the
Riemann–Silberstein vector) — with the added, checked observation that it requires the
Cartesian basis to work cleanly, not the specific rotated matrix written immediately above it.

**What's still open:** nothing left materially open in this batch — every build reached either a
clean SOLID or a fully closed, quantified correction.

---

## Errata — errors in the notebook (2007)

- **p.98 (NB-124):** $R_x(\phi)=\exp(i\sigma_x\phi/2)$ has its diagonal and off-diagonal entries
  swapped relative to the correct
  $\begin{pmatrix}\cos(\phi/2)&i\sin(\phi/2)\\i\sin(\phi/2)&\cos(\phi/2)\end{pmatrix}$; a second,
  independent error follows in the "double-angle simplified" tensor product, whose cross term
  ($2i\sin\phi$) is exactly $4\times$ too large (should be $\tfrac{i}{2}\sin\phi$). Neither error
  propagates past this page.
- **p.98 (NB-125):** $R_y(\phi)=\exp(i\sigma_y\phi/2)$ carries the same diagonal/off-diagonal swap
  as NB-124's $R_x$, plus one further isolated transcription mismatch in the stated $4\times4$
  tensor product. The derivation is left incomplete on the page; completed here in closed form.
- **p.99–100 (NB-127):** the new-basis $S_x,S_y$ matrices (used to block-diagonalize
  $\tfrac12\otimes\tfrac12=1\oplus0$) are each missing an overall factor of $1/\sqrt2$ — confirmed
  two independent ways: (1) they don't match the correctly-normalized Clebsch–Gordan reduction of
  the total-spin sum operator, and (2) they fail their own stated $\mathfrak{su}(2)$ commutation
  algebra and Casimir by exactly the amount this factor would fix. $S_z=\mathrm{diag}(1,0,-1)$
  is exact and needs no correction. This error propagates into NB-128 (which uses these matrices
  literally, uncorrected) but does not change NB-128's or NB-129's own verdicts, since NB-128 is
  checked against the notebook's own (consistently-used) numbers and NB-129's Maxwell-equation
  claim is verified independently against the unrelated Cartesian basis.

## Errata — errors in my framing of these prompts

- An initial attempt at NB-128/NB-129 assumed the "3D Dirac equation" page must be using the same
  raw Cartesian $S_x,S_y,S_z$ given at the very top of p.99 (NB-126), since that is the natural
  basis for a clean Maxwell-equation identification. Substituting literal $E+iB$ components into
  the notebook's own displayed matrix under that assumption produced an inconsistent, non-Maxwell
  mess. Rather than conclude NB-129 was simply wrong, the two candidate generator sets in play on
  the page (NB-126's Cartesian vs. NB-127's rotated "new-basis") were tested explicitly against
  the notebook's own boxed matrix; NB-127's matrices turned out to be the ones actually used in
  NB-128, resolving the apparent inconsistency as a basis mismatch between adjacent pages rather
  than an error in the margin note itself.
- An initial reading of NB-127 assumed the page's own words ("transform $\sigma_z\otimes\sigma_z$
  into $S_x$") should be checked literally by block-diagonalizing the raw tensor *product*
  operators. This produced a clean numerical non-match (confirmed, not a bug) that could have been
  mistaken for the page's central claim being wrong. Re-reading the physics (Clebsch–Gordan
  addition of angular momentum couples the *sum* of two spins, not their *product*) resolved this
  as an imprecision in the page's prose rather than an error in its actual stated numerical
  results, which do check out once the right construction (the sum) is used.

## Correlation queue additions

One entry added — see `docs/theory/notebook-reconstruction-correlation-queue.md` for the full
row. NB-129's Riemann–Silberstein-vector identification ($\psi_+=E+iB$ satisfying a spin-1
"Weyl-like" equation, confirmed here to reduce exactly to vacuum Maxwell) is a genuinely
independent 2007 discovery of a classical construction with a documented connection to the modern
"photon wavefunction" literature — and CLAUDE.md's own decision 5 describes the model's photon as
built from a real $(\mathbf E,\mathbf B)$ vector pair with a rotation-rate structure (finding
25/26). This is exactly the kind of structural resemblance the correlation queue exists to flag,
phrased as a question rather than an answered claim.
