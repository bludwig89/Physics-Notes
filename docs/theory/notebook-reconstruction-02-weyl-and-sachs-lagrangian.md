# Notebook Reconstruction — Batch 02: Weyl Representation, Riemannian Background,
# Sachs Electrogravity Lagrangian (pp. 12–29)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 12–29 (NB-014 – NB-038). Written for a reader holding the notebook and no repo access.

Date-time stamp: 2026-09-22 - (batch 02).

**Scope note on Sachs' formalism.** Pages 15–29 work through Mendel Sachs' unified
electrogravity Lagrangian in his quaternion/2-spinor ($q^\mu$, $\Omega_\mu$) formalism, citing
specific numbered equations from his book by page/equation (e.g. "6.41," "3.59'," "3.77"). A
full independent re-derivation of Sachs' entire generalized-relativity apparatus from scratch is
outside what this batch can do (it would mean reconstructing a large fraction of his 1982 book).
What this batch does instead, consistent with "reconstruct independently... redo the steps": (1)
verify the concrete algebraic/matrix machinery the author himself uses (trace-derivative
identities, Hermiticity arguments, Euler–Lagrange variations) with symbolic computation on
generic objects, not just citing the formulas; (2) treat Sachs' own numbered results as external,
cited literature — correctly quoted or not, checked where checkable, flagged as unverifiable
citations where not; (3) put real independent effort into the two places the author himself
flags as uncertain (NB-025's abandoned attempt, NB-037's self-flagged discrepancy with Sachs).

---

## NB-014 (p.12) — Massive Weyl-Basis Equations

**Notebook:** $i\hbar\partial_t\psi_+=-i\hbar c\,\boldsymbol\sigma\cdot\nabla\psi_+-m_0c^2\psi_-$ (1a),
$i\hbar\partial_t\psi_-=i\hbar c\,\boldsymbol\sigma\cdot\nabla\psi_--m_0c^2\psi_+$ (1b).

**Reconstruction.** These are the standard Weyl-basis form of the massive Dirac equation — the
question worth actually checking is whether this coupled 2×2-block system reproduces the correct
relativistic dispersion $E^2=p^2c^2+m_0^2c^4$, i.e. whether it's a legitimate "square root" of
KG with mass (as claimed structurally at NB-039/p.31 for the massless case).

**Verified** (`run_NB-014_015_weyl_massive.py`, sympy, plane-wave ansatz, exact $4\times4$
characteristic-polynomial computation via `det(M-EI)`, not a schematic argument): built the
$4\times4$ matrix coupling $(\psi_+,\psi_-)$ from (1a)/(1b) on a plane wave and computed its
characteristic polynomial in $E$ exactly. Result: $(E^2-c^2p^2-m_0^2c^4)^2=0$ — an exact,
term-by-term match (the squaring reflects the double degeneracy from the two spin/helicity
components within each 2-spinor).

**Verdict: SOLID.**

## NB-015 (pp.12–13) — Massless Decoupling

**Notebook:** setting $m_0\to0$ in (1a),(1b) gives two independent helicity equations (2a,2b);
parity interchanges them.

**Verified** (same script): confirmed the $4\times4$ coupling matrix's off-diagonal ($\psi_+
\leftrightarrow\psi_-$) blocks vanish identically at $m_0=0$ — full block-diagonal decoupling.
The parity-interchange claim is a standard fact about the Weyl representation (space reflection
swaps the two chiral 2-spinors) not independently re-derived here (it isn't in dispute and
nothing in the notebook's own treatment needs it checked further at this point).

**Verdict: SOLID.**

---

## NB-016 (p.14) — Riemannian Geometry Background

Standard metric-tensor/local-flatness definitions, presented without derivation as background
for what follows. **Verdict: NOT-TESTABLE** (definitional background, textbook GR).

---

## NB-017 (p.15) — Sachs Gravitational Lagrangian, Quoted Formulas

**Notebook:** $\mathcal L_E=R\sqrt g$ (cited "6.41 + my notes p.56"), plus supporting formulas for
$g\equiv-\det g_{\mu\nu}$, $\partial_\sigma g^{\mu\nu}$ (cited "3.59'"), $K_{\rho\lambda}$ (cited
"6.40," "6.45"), $R$ in terms of $K,q,\tilde q$, and $\Omega_\mu$ (cited "3.88").

**Assessment.** These are direct citations to Mendel Sachs' book, by his own equation numbers —
external literature, quoted rather than derived by the author on this page. The one piece that
*is* independently checkable without the source book is the core algebraic identity these
formulas all rest on: that $q^\mu,\tilde q^\mu$ built from Pauli matrices reproduce the flat
Minkowski metric via $g^{\mu\nu}=-\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$ — checked
directly below at NB-019, where it holds exactly.

**Verdict: SOLID** (as a citation, correctly presented as one; underlying algebra independently
confirmed at NB-019).

## NB-018 (p.16) — Free 2-Spinor Lagrangians, Boxed Matter Coupling

**Notebook:** $\mathcal L_\eta=i\eta^+q^\mu\partial_\mu\eta-i\partial_\mu\eta^+q^\mu\eta$,
similarly for $\chi$; boxed covariant coupling
$\mathcal L_M^\eta=\sqrt g\{i\eta^+q^\mu\eta_{;\mu}-i\eta_{;\mu}^+q^\mu\eta\}$.

**Assessment.** This is the standard real (Hermitian) form of a 2-spinor kinetic Lagrangian —
the symmetrized combination $i\eta^+q^\mu\partial_\mu\eta-i\partial_\mu\eta^+q^\mu\eta$ is
exactly what makes $\mathcal L_\eta=\mathcal L_\eta^+$ (needed for a physical, real action), by
the same logic later made explicit at p.24 (NB-033). Correctly formed. **Verdict: SOLID.**

## NB-019 (p.16) — $q^\mu,\tilde q^\mu$ in Pauli Components; the Core Quaternion Identity

**Notebook:** $q_\mu\tilde q^\mu=-4\sigma^0_0$; $q^\mu=q^\mu_4\sigma_0-i\sigma_1q^\mu_1-i\sigma_2q^\mu_2-i\sigma_3q^\mu_3$;
$\tilde q^\mu=-\sigma_0q^\mu_4-i\sigma_1q^\mu_1-i\sigma_2q^\mu_2-i\sigma_3q^\mu_3$; plus Sachs'
own (3.60)/(3.62) forms (quoted, with his idiosyncratic $v^\mu$ notation — not independently
checkable without his book, since the notation isn't otherwise defined in the transcription).

**Reconstruction.** The load-bearing structural fact underneath all of pp.15–29 is the standard
2-spinor identity $\sigma^\mu\tilde\sigma^\nu+\sigma^\nu\tilde\sigma^\mu=2\eta^{\mu\nu}I$ (with
$\sigma^\mu=(I,\sigma_x,\sigma_y,\sigma_z)$, $\tilde\sigma^\mu=(I,-\sigma_x,-\sigma_y,-\sigma_z)$)
— this is what makes $g^{\mu\nu}=-\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$ reduce correctly
to flat Minkowski space when $q^\mu=\sigma^\mu$.

**Verified** (`run_NB-018_019_qmu_pauli_identity.py`, sympy, explicit $2\times2$ matrices, all 16
$(\mu,\nu)$ combinations checked individually, not a schematic argument): the identity holds
**exactly** for every one of the 16 combinations, reproducing $2\,\mathrm{diag}(1,-1,-1,-1)\,I$.

The specific line "$q_\mu\tilde q^\mu=-4\sigma^0_0$" (an unusual same-index-summed statement) was
also checked directly: $\sum_\mu\sigma^\mu\tilde\sigma^\mu=-2I$ (raw sum, no metric weight) or
$+4I$ (metric-weighted sum $\sum_\mu\eta_{\mu\mu}\sigma^\mu\tilde\sigma^\mu$) — **neither matches
$-4I$** as transcribed. Since the surrounding pages (e.g. p.32/NB-041) use a *different*,
internally-consistent tilde convention (plain sign flip on the spatial Pauli matrices, matching
what's verified above), this one line at p.16 is most likely either a genuine slip in the
original notes or a different, unstated sign/normalization convention for $\tilde q$ specific to
that single equation. It is never used again in a way that would propagate the discrepancy
forward (the boxed formulas that matter, at NB-017 and NB-021, use the metric formula that
checks out).

**Verdict: SOLID-WITH-CORRECTION.** The core apparatus (the metric-from-quaternion identity) is
exactly right; the isolated "$-4\sigma^0_0$" line does not match any of the natural readings of
the notation used elsewhere on the same and nearby pages — flagged, not fatal.

Sachs' own quoted (3.60)/(3.62) forms (with $v^\mu$ notation) are recorded as an unverifiable
external citation. **Verdict: NOT-TESTABLE** for that specific sub-claim (no independent way to
check a direct quote from an inaccessible source against itself).

---

## NB-020 (p.17) — Covariant Derivatives, $\Omega^{(\chi)}_\rho$ Formulas

**Notebook:** $\chi=\varepsilon\eta^*$ ansatz (with a margin note preferring space-reflected
$\eta,\chi$ instead, then abandoning that in favor of the original pair "since this falls out
either way"); $\eta_{;\mu}=\partial_\mu\eta+\Omega_\mu\eta$; $\Omega^{(\chi)}_\rho$ formulas
(3.77, 3.79b), cited to Sachs.

**Assessment.** The covariant-derivative *form* ($\partial_\mu+\Omega_\mu$, the standard minimal
spin-connection coupling) is unremarkable and correct as a structural ansatz. The specific
$\Omega^{(\chi)}_\rho$ formula is a Sachs citation, not independently checkable without his book.
The $\chi=\varepsilon\eta^*$ vs. space-reflected-field question is explicitly left as an open
authorial choice ("use $\eta$ and $\chi$" — a decision, not a derived result).

**Verdict: SOLID** (structural form correctly used); the specific cited formula is NOT-TESTABLE
as an external citation.

> **2026-09-22 - 17:25 — cited formulas now tested** (`notebook-reconstruction-02b-nb028-theta-curved.md`
> §7.4, `run_NB-032_tetrad_variation_tetrode.py` V2). Against the first-order tetrad postulate for an
> arbitrary tetrad: (3.79b) is correct as written; (3.77) — and p.15's (3.88) in both forms (NB-017) —
> are the Hermitian conjugates of what the notebook's $\eta_{;\mu}=\partial_\mu\eta+\Omega_\mu\eta$ convention
> needs (boost part right, rotation part sign-flipped). Correct: $\Omega_\rho=\tfrac14\tilde q_\mu(\partial_\rho q^\mu+
> \Gamma^\mu_{\tau\rho}q^\tau)$, $\Omega^{(\chi)}_\rho=-\tfrac14(\partial_\rho q^\mu+\Gamma^\mu_{\tau\rho}q^\tau)\tilde q_\mu$.

## NB-021 (p.17) — Boxed Total Lagrangian

$\mathcal L=\sqrt g\{R+i\eta^+q^\mu\eta_{;\mu}+i\chi^+\tilde q^\mu\chi_{;\mu}\}$ — direct assembly
of NB-017 (gravity term) + NB-018/020 (matter terms). No new content beyond combination.
**Verdict: SOLID.**

---

## NB-022 (p.18) — $T_{00}=\mathcal H$, Einstein Equation Component

**Notebook:** $T_{00}=\mathcal H=\pi\dot\varphi-\mathcal L$; if $G_{\mu\nu}=8\pi T_{\mu\nu}$ then
$T_{00}=\tfrac1{8\pi}G_{00}$ for the gravitational field itself; boxed
$\partial\mathcal L/\partial\dot\varphi_E=\tfrac1{8\pi}(R_{00}-\tfrac12g_{00}R)$; $R_{00}$
expansion in Christoffel symbols.

**Assessment.** This is a direct definitional substitution ($G_{\mu\nu}\equiv R_{\mu\nu}-\tfrac12
g_{\mu\nu}R$, then set $\mu=\nu=0$) plus the standard Ricci-tensor-from-Christoffel formula
$R_{\mu\nu}=\partial_\lambda\Gamma^\lambda_{\mu\nu}-\partial_\mu\Gamma^\lambda_{\nu\lambda}
+\Gamma^\alpha_{\beta\alpha}\Gamma^\beta_{\mu\nu}-\Gamma^\alpha_{\beta\nu}\Gamma^\beta_{\mu\alpha}$
(standard textbook form, e.g. Wald eq. 3.4.4, MTW) restricted to $\mu=\nu=0$ — matches exactly
what's written, term for term, with the correct index contractions. **Verdict: SOLID.**

## NB-023/NB-024 (p.19) — First-Order GR Hamiltonians (Non-Spinor and Spinor)

Structural parallel constructions: treat $(\Gamma,g)$ or $(\Omega,q)$ as independent variables
(the standard Palatini first-order trick, needed to keep the Lagrangian first-order in
derivatives) and write $\mathcal H_E$ in each case. Both are direct, correctly-formed
restatements of NB-022 in first-order form; the spinor version is the natural $q,K$ analog of
the tensor version, structurally parallel term for term. **Verdict: SOLID** (both).

---

## NB-025 (p.20) — First (Abandoned) Matter-Hamiltonian Attempt

**Notebook:** tries $\pi_\eta=i\eta^+q^0$, gets $\mathcal H=i\eta^+q^0\pi_\eta+\ldots$, includes
a margin self-check "$\mathcal L=A\dot\eta,\ \partial\mathcal L/\partial\dot\eta=A,\ \mathcal
H=A\dot\eta-A\dot\eta=0!$" — catching, in real time, that a Lagrangian *linear* in $\dot\eta$
(as this 2-spinor kinetic term is) gives an *identically vanishing* canonical Hamiltonian by the
naive Legendre transform. This is exactly correct and exactly the well-known first-order-fermion
Hamiltonian pathology (the same reason the free Dirac Lagrangian's canonical $\mathcal H$ via a
naive Legendre transform is famously trivial/constrained, requiring the symmetrized form used
next). The author abandons this line immediately ("$=\cdots$ No, we want...").

**Verdict: DEAD-END-AUTHOR-CALLED-IT** — correctly identified as a dead end, for the right
reason (linear-in-velocity Lagrangians are Hamiltonian-constrained/first-class-constraint
territory, not naively Legendre-transformable), immediately abandoned in favor of NB-026's
symmetrized construction.

## NB-026 (p.20) — Symmetrized $\mathcal L_M$; Flat-Space $\Theta^{\mu\nu}$

Standard canonical energy-momentum tensor construction from the symmetrized (real) matter
Lagrangian. Structurally correct, standard field-theory bookkeeping (the same machinery used for
any first-order fermion Lagrangian's stress tensor). **Verdict: SOLID.**

## NB-027 (p.21) — $\mathcal H_M=\Theta^{00}$, Flat-Space Result; Self-Critique

The flat-space $\Theta^{00}$ follows directly from NB-026. The author immediately flags it
himself as incomplete for curved spacetime ("doesn't show any interaction of $\eta,\chi$ with
curvature") — a correct self-diagnosis, fixed at NB-028. **Verdict: SOLID** (correct as far as
it goes, and correctly recognized as incomplete by the author himself).

## NB-028 (p.21) — Covariant $\Theta^{\mu\nu}$ Fix

Redefining $\Theta^{\mu\nu}$ with covariant derivatives ($\eta_{;\mu}$ in place of
$\partial_\mu\eta$) is exactly the right fix for NB-027's flagged gap — this is the standard way
a stress tensor picks up curvature coupling through minimal coupling. **Verdict: SOLID.**

> **2026-09-22 - 16:40 — verdicts revised for NB-026/027/028.** Evaluated explicitly in
> `notebook-reconstruction-02b-nb028-theta-curved.md` (`run_NB-026_027_028_theta_curved.py`):
> the $\partial^
u\eta^+$/$\partial^
u\chi^+$ terms of the p.20 $\Theta^{\mu
u}$ carry the wrong sign
> (should be $-$), so NB-027's $\Theta^{00}$ is $	frac i2\partial_0(\eta^+\eta)$ — imaginary, zero for a
> plane wave — and NB-028 inherits it. NB-026/027 → INCORRECT (as transcribed) /
> SOLID-WITH-CORRECTION; NB-028 → SOLID-WITH-CORRECTION (also needs Tetrode symmetrization to
> source $G_{\mu
u}$). Full curved-spacetime tensor reconstructed and verified there.

---

## NB-029 (p.21) — Scalar Toy Matter Lagrangian: **Genuine Error Found**

**Notebook (verbatim, lines 487, 491):** $\mathcal L_M=i\partial_\mu\varphi\partial^\mu\varphi
-\mu^2\varphi^2$ (flat), $\mathcal L_M=i\varphi_{;\mu}\varphi^{;\mu}-\mu^2\varphi^2$ (GR form).

**Reconstruction.** A real scalar field's kinetic Lagrangian should be
$\tfrac12(\partial\varphi)^2$ (real coefficient) — an explicit factor of $i$ on a term that must
be real for a real field is a red flag. Checked directly: does the Euler–Lagrange equation for
the *literal* $\mathcal L_M=i(\partial\varphi)^2-\mu^2\varphi^2$ come out as a sensible
(real-coefficient) equation of motion?

**Verified** (`run_NB-028_029_scalar_toy_i_factor.py`, sympy, direct Euler–Lagrange on an
unconstrained field, exactly as in NB-001): the literal Lagrangian gives
$2\mu^2\varphi+2i\,\Box\varphi=0$, i.e. $\Box\varphi=i\mu^2\varphi$ — an equation relating two
otherwise-real quantities by an explicit factor of $i$, which is **not** a sensible equation of
motion for a real scalar field (compare: the standard $\tfrac12(\partial\varphi)^2-\tfrac12\mu^2
\varphi^2$ gives the correct real $\Box\varphi+\mu^2\varphi=0$).

**Verdict: INCORRECT (as transcribed), SOLID-WITH-CORRECTION.** Corrected form:
$\mathcal L_M=\tfrac12\varphi_{;\mu}\varphi^{;\mu}-\tfrac12\mu^2\varphi^2$ (drop the stray $i$,
restore the standard $\tfrac12$ normalization). This is a genuine notebook slip, not a
transcription artifact — the "$i$" appears twice, consistently, in both the flat and GR forms,
suggesting the author simply mis-copied or mis-typed the standard scalar Lagrangian at this
point (this toy field is introduced only to test the $\Theta^{\mu\nu}$ machinery on a simple
case and is never used again after NB-030, so the error doesn't propagate into any later result).

## NB-030 (p.22) — $\mathcal H_M$ for the Toy Scalar; Boxed Full Hamiltonian

Inherits NB-029's $i$-factor bug directly (the notebook's $\mathcal H_M=i\partial_0\varphi
\partial^0\varphi+i\nabla\varphi\cdot\nabla\varphi+\mu^2\varphi^2$, lines 501–511, carries the
same stray $i$). With the NB-029 correction applied (drop the $i$'s, use $\tfrac12$
normalization), the Legendre transform reproduces the standard real $\mathcal H_M=\tfrac12
(\partial_0\varphi)^2+\tfrac12(\nabla\varphi)^2+\tfrac12\mu^2\varphi^2$ — the same standard form
already verified independently at NB-001. The gravitational ($\Gamma$) part of the boxed total
Hamiltonian is unaffected (it's NB-023's result, assembled alongside). **Verdict:
SOLID-WITH-CORRECTION** (same correction as NB-029, propagated through).

---

## NB-031 (p.23) — Total Lagrangian Restated, EL Principle Set Up

Direct restatement of NB-021's boxed Lagrangian plus the standard covariant Euler–Lagrange
functional-derivative principle $(\partial\mathcal L/\partial\psi_{;\mu})_{;\mu}-\partial\mathcal
L/\partial\psi=0$ for each independent field. No new content. **Verdict: SOLID.**

## NB-032 (pp.23–24) — Trace-Derivative Identity; Covariant EL Form

**Notebook:** $\partial\mathrm{Tr}(AB)/\partial B=\tilde A$ (transpose); $\partial(-g)^{1/2}/
\partial\tilde q^\lambda=(\tfrac14q_\lambda(-g)^{-1/2})^*$; covariant EL form
$(\partial\mathcal L/\partial\eta_{\rho;\nu})_{;\nu}-\partial\mathcal L/\partial\eta_\rho=0$.

**Verified** (`run_NB-026_032_035_trace_derivative_identities.py`, sympy, generic symbolic
$2\times2$ matrices, direct componentwise partial differentiation of $\mathrm{Tr}(AB)$ w.r.t.
every entry of $B$, not a citation): $\partial\mathrm{Tr}(AB)/\partial B=A^T$ confirmed exactly.

**Verdict: SOLID.**

> **2026-09-22 - 17:25 — NB-032 continued.** The $\partial(-g)^{1/2}/\partial\tilde q^\lambda=(\tfrac14q_\lambda(-g)^{-1/2})^*$
> line has the wrong power of $(-g)$ (scaling weight $s^{+3}$ vs the required $s^{-5}$); correct
> $(\tfrac14q_\lambda(-g)^{+1/2})^*$ → SOLID-WITH-CORRECTION for that line. The program was carried through
> to the tetrad variation of $S_M$: $\Omega$ fixed gives NB-028's canonical $\Theta$, $\Omega=\Omega[q]$ gives the
> Tetrode tensor (02b §7).

## NB-033 (p.24) — Variation of $\mathcal L_\eta$

**Notebook:** computes $\partial\mathcal L/\partial\eta_{;\mu}=\sqrt g\,i\eta^+q^\mu$, then its
covariant derivative; symmetrized form $\mathcal L_\eta=\tfrac12[i\eta^+q^\mu\eta_{;\mu}-i\eta^+_{;\mu}
q^\mu\eta]\sqrt g$; $\partial\mathcal L/\partial\eta=-\tfrac{i}2\eta^+_{;\mu}q^\mu\sqrt g$,
$\partial\mathcal L/\partial\eta^+=\tfrac i2 q^\mu\eta_{;\mu}\sqrt g$.

**Assessment.** These are direct partial derivatives of a linear (in $\eta_{;\mu}$ or $\eta$)
expression, mechanically correct — $\partial(\eta^+q^\mu\eta_{;\mu})/\partial\eta_{;\mu}=\eta^+q^\mu$
treating $\eta,\eta^+$ as formally independent (the standard trick for real/holomorphic
Lagrangians built from a field and its conjugate) is definitional, not something with room to go
wrong given the symmetrized starting form already confirmed at NB-018/NB-026. **Verdict: SOLID.**

## NB-034 (p.25) — Combining the Variations: the Boxed Free EOM

**Notebook:** using $(-g)^{1/2}_{;\mu}=0$ (cited "notebook 2 p.52," standard metric-compatibility
fact) and $q^\mu_{;\mu}=\tilde q^\mu_{;\mu}=0$ (cited "notebook 2 p.42/64," standard result), the
two variational equations reduce to $\eta^+_{;\mu}q^\mu=0$ and $q^\mu\eta_{;\mu}=0$, and the
notebook asserts: **"if $q^\mu$ is Hermitian, $q^{\mu+}=q^\mu$, these are just the same
equation"** — giving the boxed final result $q^\mu\partial_\mu\eta+q^\mu\Omega_\mu\eta=0$.

**Reconstruction.** This claim is worth checking carefully rather than waving through, because
it's *not* obviously true without more input: $\eta^+_{;\mu}q^\mu=0$ involves $\Omega_\mu$
appearing *undaggered but on the wrong side* relative to $q^\mu\eta_{;\mu}=0$'s $\Omega_\mu$, and
the notebook never separately assumes $\Omega_\mu$ is Hermitian. Does Hermiticity of $q^\mu$
*alone* force the equivalence?

**Verified** (`run_NB-031_eom_hermitian_check.py` — filename numbering doesn't match the final
ledger ID, see note below; content covers this exact step): built a fully generic (non-Hermitian)
complex $2\times2$ $\Omega$, a generic Hermitian $q$ (real linear combination of Pauli matrices),
a free 2-spinor $\eta$ and independent symbol $\partial_\mu\eta$, formed both sides exactly as
the notebook defines them, and took the conjugate-transpose ("dagger") of the $\eta^+_{;\mu}q^\mu=0$
row equation symbolically. Result: the dagger of $(2a)$ minus $(2b)$ is the exact zero matrix —
**Hermiticity of $q^\mu$ alone is sufficient**, with no additional assumption on $\Omega_\mu$
needed. (An initial hand-derivation attempt suggested an extra Hermiticity condition on $\Omega$
might be needed — that hand-derivation was itself wrong, caught by redoing it with the correct
involution property $(A^+)^+=A$ applied to the whole covariant-derivative object at once rather
than distributing the dagger term-by-term with a sign slip; the symbolic check settles it.)

**Verdict: SOLID.** The notebook's claim is exactly right, confirmed on genuinely non-Hermitian
$\Omega$, not just a special case.

*(Filename/build-ID note: the runner script for this check is named
`run_NB-031_eom_hermitian_check.py` from an earlier pass through the ledger numbering before the
final NB-017–038 assignment settled; its content is the NB-034 check described above, not
NB-031. Recorded here to avoid confusion for anyone re-running the scripts against the ledger.)*

## NB-035 (pp.26–28) — Variation w.r.t. $\Omega_{\rho,\nu}$

**Notebook:** long trace-derivative matrix algebra computing $\partial\mathcal L/\partial
\Omega_{\rho,\nu}$, using $\partial\mathrm{Tr}(ABC)/\partial B=A^tC^t$ and the p.27 form
$\partial\mathrm{Tr}(AB^+C)/\partial B=CA$.

**Verified** (same trace-derivative script): both identities checked directly and exactly —
$\partial\mathrm{Tr}(ABC)/\partial B=A^TC^T$ confirmed; the p.27 form
$\partial\mathrm{Tr}(AB^+C)/\partial B=CA$ (with $B^+$ standing in for $B^T$ on real sub-blocks,
consistent with how "+" is used elsewhere in this derivation) confirmed **exactly**, componentwise
— no hidden extra transpose, contrary to what a naive first guess might suggest.

**Verdict: SOLID.** The matrix-calculus machinery underlying this long derivation is confirmed
correct in general (not just plausible by citation); the full multi-line assembly built from it
is not re-derived term-by-term here, but rests on verified-correct identities throughout.

## NB-036 (p.28) — $\partial\mathcal L/\partial\Omega_{\rho,\nu}$ Assembled; Current Term

$\partial\mathcal L/\partial\Omega_\rho=\tfrac i2\eta^+q^\rho\eta\sqrt g$ — this is exactly the
standard Noether/matter current one expects from varying a minimally-coupled kinetic term
w.r.t. the connection field it couples through (the Weyl/Dirac vector current $\bar\psi\gamma^\rho
\psi$ analog, here $\eta^+q^\rho\eta$). Structurally exactly right. **Verdict: SOLID.**

---

## NB-037 (pp.28–29) — Self-Flagged Discrepancy With Sachs: Genuine Progress

**Notebook:** computing $(\partial\mathcal L/\partial\Omega_{\rho,\nu})_{;\nu}$ two ways, the
first "appears to all go to 0 — not good!"; the second gives
$$\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}=-\tfrac i2\eta^+q^\rho\eta,$$
and the author notes: *"Sachs gets 0 on the LHS & gets usual relation of $\Omega$ to $q$... but
apparently this doesn't hold!"*

**Reconstruction and continuation.** This discrepancy has a clean, externally-grounded
resolution that the author does not seem to have reached for, worth stating explicitly: this is
exactly the structure of **Einstein–Cartan–Sciama–Kibble (ECSK) theory** — the well-established
(since Kibble 1961 and Sciama 1964) result that when gravity is formulated as a genuinely
first-order (Palatini-type) theory *with the connection $\Omega_\mu$ varied independently of the
tetrad/quaternion $q^\mu$*, and spinor (fermionic) matter is present, the antisymmetric/torsion
part of the connection equation of motion is **not** forced to zero — it is instead **algebraically
sourced by the matter's spin current**. In vacuum (or for spinless/bosonic matter with no
independent spin density), that source vanishes and the connection reduces to the ordinary
torsion-free Levi-Civita-type relation to $q^\mu$ — which is exactly "Sachs gets 0 on the LHS,"
presumably in a treatment without an independent spinor spin-current term feeding back into
$\Omega$'s own field equation.

The right-hand side the notebook derives, $-\tfrac i2\eta^+q^\rho\eta$, has exactly the right
*character* to be such a source: it is a **fermion bilinear current**, of the same general
structure as the vector current whose variation gave NB-036's Noether current. This is a strong
structural match to the ECSK picture (torsion sourced by spin density), not a coincidence of
sign or form.

**What this batch does not close:** a full, term-by-term match between $-\tfrac i2\eta^+q^\rho\eta$
and the specific spin-current tensor of ECSK theory (which for a Dirac-type field is built from
an axial/totally-antisymmetric bilinear, not simply the vector current) requires carrying the
full curved-space torsion tensor construction through explicitly — not attempted here.

**Verdict: NEEDS-WORK**, substantially advanced. The "not good!" self-assessment is very likely
premature: the discrepancy the author found is structurally consistent with a known,
well-established physical effect (torsion sourced by fermion spin density in first-order gravity)
rather than an error, *provided* Sachs' own "usual relation" was derived without an independent
matter spin-current source term. The one specific thing that would close it: derive the ECSK
spin-current tensor for this $\eta,\chi$ 2-spinor matter content explicitly and check it against
$-\tfrac i2\eta^+q^\rho\eta$ term-by-term (queued for correlation — see below, this is exactly
the kind of structural fact the model might independently have an opinion about).

> **2026-09-22 - 18:30 — NB-037 resolved** (`notebook-reconstruction-02b-nb028-theta-curved.md` §8,
> `run_NB-037_ecsk_spin_source.py`, all exact). The LHS $\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}$ is exactly
> Cartan's modified-torsion tensor ($-C^\rho{}_{ab}\Sigma^{ab}$, traceless). The true source is the matrix
> $\tfrac i2(\eta\eta^+q^\rho)^T=\tfrac i2[\tfrac12(\eta^+q^\rho\eta)I+j_a\Sigma^{a\rho}]^T$: the notebook kept only the trace (a U(1)
> charge current, whose gravitational LHS is identically 0) and dropped the traceless ECSK spin
> part $S^{\rho ab}=\tfrac12\varepsilon^{\rho abd}j_d$ (for a 2-spinor the vector bilinear *is* its axial current).
> Corrected, NB-037 is the Cartan equation $T=\kappa S$; Hehl–Datta $\tfrac3{16}\kappa J^5\!\cdot\!J^5$ recovered.
> **Verdict: SOLID-WITH-CORRECTION (resolved).**

## NB-038 (p.29) — $\partial\mathcal L/\partial q^\lambda$; Incomplete

**Notebook:** $\partial\mathcal L/\partial q^\lambda=\sqrt g(-\tfrac12(K^+_{\lambda\rho}\tilde
q^\rho+\tilde q^\rho K_{\lambda\rho})^*+\tfrac14R\tilde q^*_\lambda)$ (gravity term) and
$\partial\mathcal L_M/\partial q^\lambda=(\tfrac i2\eta^+\eta_{;\lambda}-\tfrac i2\eta^+_{;\lambda}
\eta)\sqrt g$ (matter term) — the page ends here, mid-derivation, with a stray note "Need
$\tilde\Omega^{(\chi)}_\rho=-\Omega^{x+}_\rho=\Omega_\rho$" that isn't resolved into a final
equation on the page. Page 30 (blank) and page 31 (a new topic, $\sigma$-matrix motivation) do
not pick this back up anywhere else in the transcribed notebook.

**Verdict: NEEDS-WORK.** Genuinely incomplete — unlike NB-003 (batch 01), which the author
himself completes 40 pages later, this $q^\lambda$-variation is never assembled into a final
boxed equation of motion anywhere in the transcribed material. The specific thing that would
close it: combine the two pieces shown into a single $q^\lambda$ field equation (the natural
analog of NB-034's $\eta$-equation and NB-037's $\Omega$-equation) and check it for
self-consistency with the other two — not attempted here given the scope of this batch.

> **2026-09-22 - 19:30 — NB-038 completed** (`notebook-reconstruction-02b-nb028-theta-curved.md` §9,
> `run_NB-038_q_field_equations.py`, all exact). Assembled $q^\lambda$ equation: $G_{\lambda\nu}(\Omega)=\kappa\Theta_{\lambda\nu}(\Omega)$
> (Sciama–Kibble; tetrad derivative of $\sqrt{-g}R$ = $2\sqrt{-g}G_{\lambda\nu}$). Its antisymmetric part is implied by the
> matter + Ω equations (Belinfante–Rosenfeld, on shell); its symmetric part reduces to
> $\mathring G=\kappa[T^{\rm Tetrode}-\tfrac3{16}\kappa gJ_5^2]$. Missing χ equation and torsion-coupled matter equations
> constructed ($\mp\tfrac{3i}8\kappa J_5\!\cdot\!\sigma$, Hehl–Datta). p.29 corrections: the gravity piece has $K\leftrightarrow K^+$ swapped; the matter piece writes
> the trace for the outer product. The note $-\Omega^{(\chi)+}=\Omega$ holds and is the covariance condition for $\chi=\varepsilon\eta^*$.
> **Verdict: SOLID-WITH-CORRECTION (completed).**

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-014 | SOLID |
| NB-015 | SOLID |
| NB-016 | NOT-TESTABLE |
| NB-017 | SOLID (citation, underlying algebra confirmed) |
| NB-018 | SOLID |
| NB-019 | SOLID-WITH-CORRECTION (core identity) / NOT-TESTABLE (Sachs' own (3.60)/(3.62) quote) |
| NB-020 | SOLID (structural form) / NOT-TESTABLE (cited formula) |
| NB-021 | SOLID |
| NB-022 | SOLID |
| NB-023 | SOLID |
| NB-024 | DEAD-END-AUTHOR-CALLED-IT |
| NB-025 | SOLID |
| NB-026 | SOLID |
| NB-027 | SOLID |
| NB-028 | SOLID |
| NB-029 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-030 | SOLID-WITH-CORRECTION |
| NB-031 | SOLID |
| NB-032 | SOLID |
| NB-033 | SOLID |
| NB-034 | SOLID |
| NB-035 | SOLID |
| NB-036 | SOLID |
| NB-037 | NEEDS-WORK (substantially advanced, ECSK grounding identified) |
| NB-038 | NEEDS-WORK |

**What closed:** the Weyl-equation dispersion relation (NB-014/015) reproduces the correct
relativistic mass shell exactly. The entire trace-derivative/matrix-calculus toolkit underlying
the Sachs-Lagrangian variation (NB-032, NB-035) is independently confirmed correct on generic
symbolic matrices, not just cited. The key Hermiticity argument collapsing the two EL equations
into one (NB-034) is confirmed exactly, including ruling out a plausible-looking hidden
assumption a first hand-check wrongly suggested was needed. A genuine, previously-uncaught error
was found and corrected: the scalar toy-matter Lagrangian (NB-029/030) has a spurious factor of
$i$ that breaks the reality of its equation of motion.

**What's still open:** NB-037's self-flagged Sachs discrepancy is reframed with real
external physics content (Einstein–Cartan–Sciama–Kibble torsion-from-spin), but not fully closed
to an exact term-by-term match. NB-038 trails off mid-derivation in the source material itself
and stays open. Sachs' own directly-quoted equation forms (NB-019's (3.60)/(3.62)) remain
unverifiable citations without access to his book.

---

## Errata — errors in the notebook (2007)

- **p.16 (NB-019):** "$q_\mu\tilde q^\mu=-4\sigma^0_0$" does not match either natural reading of
  the tilde convention used on the same and nearby pages (gives $-2I$ raw-summed or $+4I$
  metric-weighted, not $-4I$) — flagged, not load-bearing.
- **p.21 (NB-029, propagating to NB-030, p.22):** scalar toy-matter Lagrangian
  $\mathcal L_M=i\partial_\mu\varphi\partial^\mu\varphi-\mu^2\varphi^2$ has a spurious factor of
  $i$; the resulting Euler–Lagrange equation $\Box\varphi=i\mu^2\varphi$ is not a sensible
  real-field equation of motion. Corrected form: $\mathcal L_M=\tfrac12\varphi_{;\mu}\varphi^{;\mu}
  -\tfrac12\mu^2\varphi^2$. Confirmed by direct symbolic Euler–Lagrange computation. Does not
  propagate past NB-030 (the toy field is not used again).

## Errata — errors in my framing of these prompts

- An intermediate hand-derivation while checking NB-034 (before writing the symbolic script)
  wrongly suggested $\Omega_\mu$ would need its own Hermiticity assumption for the notebook's
  claim to hold; this was a sign/distribution slip in the hand check, not a real gap, caught and
  corrected by redoing the check with sympy on fully generic (non-Hermitian) $\Omega$. Recorded
  here per the standing instruction to log framing errors, even ones caught before being written
  into a verdict.

## Correlation queue additions

See `docs/theory/notebook-reconstruction-correlation-queue.md` for a new entry on NB-037 (does
the model's gravity sector treat spinor spin-current sourcing of torsion/connection terms
anywhere, e.g. in its Einstein-equation or spin-connection treatment, or does it work entirely in
a torsion-free formulation where this question doesn't arise?) and NB-029 (unrelated to any model
claim — internal notebook arithmetic error only, not queued).
