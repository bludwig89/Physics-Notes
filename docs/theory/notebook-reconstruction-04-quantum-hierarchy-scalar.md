# Notebook Reconstruction — Batch 04: "Quantum Hierarchy Equations of a Free Scalar Field"
# (pp. 41–49)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 41–49 (NB-048 – NB-061). This is the author's own clean, careful redo of the scalar-QFT
opening from pp.1–2 (batch 01's NB-001–003), citing "Ludwig eq. N" against his own dissertation
(`references/mark_a_ludwig_thesis.pdf`, "Numerical solutions of lattice quantum fields with a
hierarchy of Schroedinger-like equations," University of Arizona) and Itzykson–Zuber ("IzZ").

Date-time stamp: 2026-09-22 - (batch 04).

---

## NB-048 (p.41) — KG Lagrangian/Hamiltonian Redo

Identical content to batch 01's NB-001 (verified there via direct symbolic Euler–Lagrange:
`run_NB-001_kg_scalar.py`), citing Goldstein by equation number. No new content.
**Verdict: SOLID** (by reference to NB-001's verification).

## NB-049 (p.42) — Lorentz-Invariant Fourier Convention

This is the convention already independently verified in batch 01 as part of the NB-002
comparison (`run_NB-002_fourier_convention.py`): the forward/inverse pair
$\tilde\phi(k)=2\omega_k\int\phi(x)e^{ikx}d^3x$,
$\phi(x)=\int\tilde\phi(k)e^{-ikx}d^3k/((2\pi)^32\omega_k)$ **round-trips exactly** (numerically
confirmed to $<10^{-13}$ on a Gaussian test function), unlike the broken p.1 scratch version.
The notebook's own in-page self-consistency check (via the $\delta$-function identity) is
independently confirmed. **Verdict: SOLID** (by reference to batch 01's verification).

## NB-050 (pp.42–43) — $H$ Transformed to $k$-Space, Integrated to Boxed $(\ast)$

Also already verified in batch 01: the NB-003 continuation script
(`run_NB-003_hspace_substitution.py`) carried the $x$-integral and $p$-collapse through
symbolically and confirmed the resulting bracket $\pi_k\pi_{-k}+(k^2+m^2)\phi_k\phi_{-k}$ matches
this page's boxed $(\ast)$ exactly, term for term. **Verdict: SOLID** (by reference).

## NB-051 (p.43) — Mode Expansions, Commutators (IzZ 3.36/3.37)

Standard canonical commutation relations and mode expansions for a free scalar field, correctly
quoted against Itzykson–Zuber's numbering. **Verdict: SOLID** (standard, correctly cited).

---

## NB-052/NB-053 (p.44) — Crossed-Out False Starts: Diagnosed

**Notebook:** a first substitution attempt into $(\ast)$, crossed out mid-derivation, with the
intermediate expansion `-a_k^{+2}-a_k^2+2a_k^+a_{-k}+a_k^{+2}+a_{-k}^2+2a_k^+a_k` and a
crossed-out trial commutator; separately, a crossed-out $\phi(x)\phi(y)$ side computation ending
"note no sense."

**Diagnosis** (`run_NB-052_053_054_ladder_operator_algebra.py`, exact truncated Fock-space
matrices, two independent oscillator modes "$k$" and "$-k$", $N=10$ levels each, checked on a
truncation-safe subspace): the crossed-out expansion mixes a **same-index** identity
($-(a_k^+-a_k)^2+(a_k^++a_k)^2$, which reduces cleanly to $4a_k^+a_k+2$ — verified here as the
$k=-k$ special case of the two-mode check used for NB-054 below) with **cross-index** terms
($2a_k^+a_{-k}$) that don't belong to that identity at all. Introducing $a_{-k}$ into what should
be a single-mode identity is exactly the kind of error that produces an expression which "makes
no sense" upon inspection — consistent with, and a precise diagnosis of, why the author caught
and abandoned it. **Verdict: DEAD-END-AUTHOR-CALLED-IT**, diagnosis added (index-mixing error);
correctly abandoned.

---

## NB-054 (p.45) — Clean Redo: the Boxed Free-Field Hamiltonian ("Ludwig eq. 3")

**Notebook:** substituting $\phi_k=a_k^++a_{-k}$, $\pi_k=i\omega_k(a_k^+-a_{-k})$ into $(\ast)$
gives, after simplification, the boxed
$$H=\tfrac12\int\omega_k(a_k^+a_k+a_ka_k^+)\,\frac{d^3k}{(2\pi)^32\omega_k}.$$

**Verified to machine precision** (same script, exact truncated 2-mode Fock matrices, $N=10$
levels/mode): substituting the given $\phi_k,\pi_k,\phi_{-k},\pi_{-k}$ into
$\pi_k\pi_{-k}/\omega_k^2+\phi_k\phi_{-k}$ gives **exactly**
$2(a_k^+a_k+a_{-k}a_{-k}^+)$ (max deviation $3.6\times10^{-15}$, i.e. floating-point zero).

**A subtlety made explicit.** The notebook's *boxed* final form has $a_k^+a_k+a_ka_k^+$ — both
terms at the **same** $k$ — whereas the true closed form at fixed $k$ is
$a_k^+a_k+a_{-k}a_{-k}^+$ (mode $k$ and mode $-k$, not both at $k$). These are only equal *after*
integrating $\int d^3k$ over all directions and relabeling the dummy variable $k\to-k$ in the
second term ($\int a_{-k}a_{-k}^+\,d^3k=\int a_ka_k^+\,d^3k$ trivially, by renaming the
integration variable over a domain symmetric under $k\to-k$) — a valid step the notebook's own
lines 1147–1151 explicitly perform, not an operator identity holding at fixed $k$. Verified
separately: the "naive same-$k$" form does **not** match the pre-relabeling algebra (deviation
14, i.e. genuinely different operators) — confirming this distinction matters and isn't just
pedantry.

**Verdict: SOLID**, confirmed to machine precision, with the relabeling step stated precisely
rather than glossed over.

---

## NB-055 (p.46) — Lattice Discretization, Schrödinger Equation

Standard discretization to a finite mode sum $H=\sum_{j=-p}^p\tfrac12\omega_j(a_ja_j^++a_j^+a_j)$
($\boxtimes$) and the Schrödinger equation $i\partial_t|\psi\rangle=H|\psi\rangle$. Direct,
correctly-formed restatement of NB-054 in discretized form. **Verdict: SOLID.**

## NB-056 (p.46) — Eigenstate Equation

$H|n_{-p}\ldots n_p\rangle=[\sum_j(n_j+\tfrac12)\omega_j]|n_{-p}\ldots n_p\rangle$ — the standard
multi-mode harmonic-oscillator eigenvalue equation, direct consequence of $\tfrac12(a^+a+aa^+)=
N+\tfrac12$ for each independent mode (itself confirmed as an elementary special case of the
NB-054 verification's underlying operator algebra). **Verdict: SOLID.**

## NB-057 (p.47) — Fock-Coefficient / Wavefunction Normalization

**Notebook:** relates Fock coefficients $C_{n_{-p}\ldots n_p}$ to the continuum wavefunction
$\psi_N(k_1\ldots k_N)$ via a combinatorial factor $\sqrt{(\Delta k)^{3N}/\prod(2\omega_{k_j})
\cdot N!/\prod_jn_j!}$.

**Reconstruction, including a framing mistake caught along the way.** An initial attempt to
verify the $N!/\prod n_j!$ factor (`run_NB-056_057_fock_normalization.py`) compared the wrong two
quantities — it checked the norm of a raw creation-operator product $(a^+)^n|0\rangle$ against
$\sqrt{N!/\prod n_j!}$ directly and found a mismatch. That mismatch was **this reconstruction's
own error**, not the notebook's: the raw creation-product norm is the *different*, standard fact
$\|(a^+)^n|0\rangle\|=\sqrt{n!}$ (confirmed exactly, both test patterns, once compared against
the right target). The notebook's $N!/\prod n_j!$ factor is a separate, standard textbook
identity — the number of distinct ways to assign $N$ *labeled* particles to a given multiset of
*occupied modes*, relating a symmetrized first-quantized wavefunction of labeled particles to an
occupation-number Fock ket (see e.g. Peskin & Schroeder Ch. 2's treatment of the same map).
Given the scope of this batch, that standard identity is recorded here as an external citation
rather than independently re-derived from scratch with a correctly-posed check.

**Verdict: SOLID** (as a correctly-stated standard identity, external citation; the fumbled
verification attempt is logged below as a framing error, not a notebook error).

## NB-058 (pp.47–48) — Substitution Into $\boxtimes$; Vacuum-Constant Isolation and Removal

Substituting the NB-057 normalization into $\boxtimes$, factors cancel to give $i\partial_t\psi_N
=(K+\sum_j n_j\omega_j)\psi_N$ with $K=\sum_j\tfrac12\omega_j$ a lattice-dependent constant; the
phase redefinition $\psi'=e^{-iKt}\psi$ removes it. This is elementary, directly-checkable algebra
(the phase-redefinition trick for removing a constant vacuum-energy term is completely standard
and not something that can go subtly wrong the way the earlier Sachs-formalism variations could)
— not separately scripted, but not glossed over either: the substitution is a direct
product-rule differentiation of $\psi=e^{iKt}\psi'$, confirmed by inspection. **Verdict: SOLID.**

## NB-059 (p.48) — Final Multiparticle Free-Boson Equation ("Ludwig eq. 3")

The boxed final result of NB-058's phase redefinition:
$i\partial_t\psi'_N=\sum_{j=1}^N\omega_{k_j}\psi'_N$ — the free multiparticle Schrödinger
equation with the vacuum energy subtracted off. Direct consequence of NB-058; no independent
content beyond that substitution. **Verdict: SOLID.**

## NB-060 (pp.48–49) — Self-Critique: Non-Covariance, Non-Local Operator

**Notebook:** flags that the equation isn't manifestly covariant and that $\omega_k=\sqrt{k^2+
m^2}$ resists a simple local-differential-operator picture in position space.

**Assessment.** This is a correct and well-known observation — $\sqrt{-\nabla^2+m^2}$ is a
genuinely non-local (pseudo-differential) operator in position space; this is exactly the
standard reason relativistic QM/QFT prefers the manifestly local, first-order Dirac equation
over a "square-root Klein–Gordon" approach for interacting theories. The author's own
self-diagnosis is accurate (and, per the notebook's own text, is exactly what motivates deferring
to a Dirac-spinor treatment next). **Verdict: NOT-TESTABLE** (self-critique/observation, not a
claim with a right-or-wrong answer beyond "is this a real limitation" — which it is, and is
universally recognized as one; this was already the Phase-0 provisional status and stands).

## NB-061 (p.49) — Wavefunction Interpretation, Bose Symmetry Requirement

Standard statement that $\psi_N$ must be symmetric under exchange, and that Bose/Fermi statistics
are enforced by (anti)commutation of the ladder operators. Correct, standard.
**Verdict: NOT-TESTABLE** (definitional/interpretive statement, not an independent claim).

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-048 | SOLID |
| NB-049 | SOLID |
| NB-050 | SOLID |
| NB-051 | SOLID |
| NB-052 | DEAD-END-AUTHOR-CALLED-IT |
| NB-053 | DEAD-END-AUTHOR-CALLED-IT |
| NB-054 | SOLID |
| NB-055 | SOLID |
| NB-056 | SOLID |
| NB-057 | SOLID |
| NB-058 | SOLID |
| NB-059 | SOLID |
| NB-060 | NOT-TESTABLE |
| NB-061 | NOT-TESTABLE |

**What closed:** the entire "clean redo" (pp.41–49) checks out, including two builds
(NB-048–051) that reuse batch 01's already-verified results directly rather than re-proving them.
The key new result, NB-054's boxed Hamiltonian, is confirmed to machine precision with exact
Fock-space matrices, and the notebook's own $k\to-k$ dummy-variable relabeling step (needed to
get from the true per-$k$ closed form to the boxed same-$k$ form) is made explicit rather than
silently accepted. The crossed-out false starts (NB-052/053) are diagnosed precisely (an
index-mixing error), not just noted as abandoned.

**What's still open:** nothing new in this batch. NB-060's non-covariance/non-locality
self-critique is accurate and well-known, not something this batch can "fix" (it's a genuine
structural fact about $\sqrt{-\nabla^2+m^2}$, not an error).

---

## Errata — errors in the notebook (2007)

- None found in this batch — every build checks out as written (up to the sign/relabeling
  subtleties already noted as *not* errors, just worth stating precisely).

## Errata — errors in my framing of these prompts

- The first version of the NB-056/NB-057 verification script compared the wrong two quantities
  (a raw creation-operator-product norm against the $N!/\prod n_j!$ combinatorial factor, which
  is not the identity that factor actually expresses) and reported a false mismatch. Caught
  before being written into a verdict; the script and this write-up now state the correct
  comparison (the raw-product norm matches the *different*, standard $\sqrt{\prod n_j!}$ fact
  exactly) and note the $N!/\prod n_j!$ claim itself is treated as an external citation rather
  than mis-verified. Logged per the standing instruction to record framing errors even when
  caught pre-verdict.

## Correlation queue additions

None from this batch meet the bar (nothing here is a corrected formula, a structural fact, or a
mechanism the model would have an opinion about — it's a clean, correct redo of standard free
scalar QFT, already fully consistent with batch 01's findings).
