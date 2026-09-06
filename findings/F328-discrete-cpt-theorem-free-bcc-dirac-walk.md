# F328 — An exact discrete CPT theorem for the free BCC Dirac walk, and why parity alone cannot exist at finite lattice spacing

**Date:** 2026-08-26 - 21:10
**Numbering:** **F328**, taken as `NEXT FREE NUMBER` (max+1; no gaps were free). Session `bold-lucid-kostelecky-cpt`, sector `particles`.
**Status:** Confirmed — **12/12 PASS**, one declared `--param` control verified red on exactly four legs.
**Reviewed:** 2026-08-27 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F328-review-2026-08-27.md))
**Module:** `src/casim/engine/particles/discrete_cpt.py` (new)
**Test record:** record `F328-discrete-cpt-theorem` (tier gate, kind assertion, `expect.exactness: exact`) → `test-results/F328_discrete_cpt_theorem.json`
**Closes (narrowly):** completeness rubric row **A4** ("CPT, and C, P, T separately") — unmoved for five reports (`docs/status/completeness-2026-08-02.md` through `-2026-08-20.md`) — moves from PARTIAL-with-no-theorem to PARTIAL-with-an-exact-free-sector-theorem-and-a-named-residual. Does **not** close the row outright: see §6.
**Cross-references:** [[F53-fg9-C-CP-per-species]] (the row's existing C/P/CP content — label-level, not operator-level; superseded in *character*, not withdrawn, by this finding's §5), [[F301-finite-a-boost-covariance-poincare-defect]] (the chirality-odd defect this finding re-derives independently as a spectral obstruction, §4), [[F327-chiral-liv-coefficient-excluded-by-crab-electrons]] (a different, experimental argument against a single physical branch — cited for contrast, not reused), [[F91-pairing-classification-theorem]] (even-vs-chiral branch structure), [[F26 / c_lat rotation reinterpretation]] (the BCC Weyl unitary this finding builds on)
**Explicitly excluded:** [[F321-strong-cp-theta-zero-and-loop-stable]]. F321's reality of the Euclidean action from closure of the loop set under reversal is a statement about $\theta_\text{QCD}$ (row B11), a **different object**, and three prior completeness reports (`-2026-08-07`, `-2026-08-18`, `-2026-08-20`) flagged borrowing it here as this row's standing trap. Nothing below cites F321 for anything but this exclusion.

---

## 1. What was open

Row A4 has read the same way for five reports: [[F53]] built $C$, $P$ and $CP$ at the level of SU(2)$\times$U(1) charge **labels** $(T_3, Q, Y, \chi)$ and coupling-strength **magnitudes** — an antiparticle table, current-magnitude comparisons, a Jarlskog count. Its own "CPT" content, part P6, is the scalar statement $\omega_0(+m) = \omega_0(-m)$. None of this is an **operator** on the model's one-tick unitary: nowhere in the tree is there a matrix $C$, $P$, or $T$ built on the Weyl/Dirac walk's Hilbert space and checked against the rule the way a CPT theorem actually requires (Streater–Wightman and successors: an operator $\Theta$ intertwining the dynamics with its own reverse). `docs/theory/ca-reference.md`'s "Time-reversibility" section reinforces the gap by checking something adjacent and calling it done: it runs the same forward walk backward at $-c_\text{lat}$ and measures a $6\times10^{-14}$ round-trip residual — which is a statement about the walk's own invertibility (true of **any** unitary CA, on inspection, for free) and carries no antiunitary content at all.

The research brief for this row was explicit that the standard proof route might not transfer: continuum CPT theorems (Streater–Wightman; Greaves & Thomas) assume continuum Lorentz invariance, and this model is only PARTIAL on that (row A2), so **whether a CPT theorem exists here at all was a live, unresolved question**, not merely an unbuilt one.

## 2. The construction

The BCC Weyl one-tick unitary (`casim.engine.lattice.bcc.bcc_unitary`, Paper 1 Eq. 15) is, per chirality branch $s\in\{+1,-1\}$,

$$A^s(\mathbf k) = u^s(\mathbf k)\,\mathbb 1 - i\bigl(n_x^s\sigma_x + n_y^s\sigma_y + n_z^s\sigma_z\bigr),$$

with $u^s, \mathbf n^s$ real closed forms in $\cos(k_i/\sqrt3), \sin(k_i/\sqrt3)$ (`bcc._bcc_uvec`). Two algebraic identities matter below, and they are **not both lattice-specific** — this is corrected from an earlier draft that called both specific to this embedding (caught by the 2026-08-27 adversarial review, see `**Reviewed:**` below). Identity (I) is a **generic** fact about any real-$(u,\mathbf n)$-parametrized Pauli-basis unitary $u\mathbb1-i\mathbf n\cdot\boldsymbol\sigma$ — it needs nothing about the BCC cos/sin closed form, only that $u,\mathbf n$ are real (§3.1 says this explicitly; the review verified it numerically on 2000 arbitrary non-BCC real-$(u,\mathbf n)$ matrices). Identity (II) **is** specific to the BCC closed form's behaviour under $\mathbf k\to-\mathbf k$ (§3.1). Since §3.2's headline theorem below uses **only** (I), the headline CPT identity is actually a generic fact about this class of Dirac-type constructions, not a BCC-specific one — what **is** BCC-specific is §4's companion no-go, which needs (II). Both identities follow directly from the cos/sin closed form (that derivation is still the easiest route to (I) even though (I) does not require it):

$$\text{(I)}\quad A^s(\mathbf k)^{*} = \sigma_y\, A^s(\mathbf k)\,\sigma_y \qquad\text{(any fixed }\mathbf k\text{, either branch)}$$

$$\text{(II)}\quad A^{-s}(-\mathbf k) = \sigma_y\, A^s(\mathbf k)\,\sigma_y \qquad\text{(branch swap + momentum flip)}$$

Together, (I) and (II) give $A^s(\mathbf k)^{*} = A^{-s}(-\mathbf k)$ — complex conjugation of a single chirality branch is **exactly** the other branch at the reflected momentum. This is the operator-level face of the `bcc.py` docstring's own remark "$\omega_+(-\mathbf k)=\omega_-(\mathbf k)$", and it is the algebraic seed of everything below.

The massive Dirac one-tick unitary (`dirac_bcc.dirac_step_3d_bcc_splitstep`) pairs **one** branch with its own dagger — not the true opposite branch; `dirac_bcc.py`'s own docstring calls this "the choice forced by unitarity of the full $4\times4$ $D_k$":

$$D(\mathbf k) = \begin{pmatrix} n\,A^+(\mathbf k) & im\,\mathbb 1 \\ im\,\mathbb 1 & n\,A^+(\mathbf k)^\dagger \end{pmatrix}, \qquad n=\sqrt{1-m^2}.$$

Chaining (I) and (II) through this block structure (worked below, §3) gives, for **every** momentum $\mathbf k$ and **every** admissible mass $|m|\le1$, with **no small-$k$ expansion anywhere**:

$$\boxed{\;\Theta\, D(\mathbf k)\, \Theta^{-1} = D(\mathbf k)^{-1}\;},\qquad \Theta := M\cdot K,\quad M:=\Sigma\cdot(\sigma_y\!\oplus\!\sigma_y),\quad \Sigma = \begin{pmatrix}0&\mathbb 1\\ \mathbb 1&0\end{pmatrix},$$

with $K$ complex conjugation and $\Sigma$ the $\eta\leftrightarrow\chi$ block swap (the standard Dirac parity matrix $\gamma^0$ in the Weyl basis). In position space, $(\Theta\psi)(x) = M\,\psi(-x)^{*}$: spatial reflection, an internal spin-and-chirality twist, and complex conjugation, combined into **one** antiunitary operator. It satisfies $\Theta^2=-1$ exactly (§3.4) — the Kramers signature of a genuine spin-$\tfrac12$ antiunitary symmetry, not bookkeeping.

## 3. Derivation

### 3.1 Identities (I) and (II)

Write $A^s(\mathbf k)=u^s\mathbb1 - i(n_x^s\sigma_x+n_y^s\sigma_y+n_z^s\sigma_z)$. Since $u^s,\mathbf n^s$ are real and $\sigma_x,\sigma_z$ are real matrices while $\sigma_y$ is pure imaginary with $\sigma_y^{*}=-\sigma_y$:

$$A^s(\mathbf k)^{*} = u^s\mathbb1 + i(n_x^s\sigma_x - n_y^s\sigma_y + n_z^s\sigma_z) = u^s\mathbb1 -i\bigl(-n_x^s\sigma_x + n_y^s\sigma_y - n_z^s\sigma_z\bigr).$$

Using $\sigma_y\sigma_x\sigma_y=-\sigma_x$, $\sigma_y\sigma_y\sigma_y=\sigma_y$, $\sigma_y\sigma_z\sigma_y=-\sigma_z$ (standard Pauli identities, $\sigma_y^{-1}=\sigma_y$):

$$\sigma_y A^s(\mathbf k)\sigma_y = u^s\mathbb1 - i\bigl(-n_x^s\sigma_x+n_y^s\sigma_y-n_z^s\sigma_z\bigr) = A^s(\mathbf k)^{*}.$$

This is identity (I), and it holds **termwise**, independent of the specific closed forms of $u^s,\mathbf n^s$ — it is a property of "real $u,\mathbf n$ paired with the Pauli basis," true for either branch at any fixed $\mathbf k$.

For (II), the closed forms matter. From `_bcc_uvec` (with $c_i=\cos(k_i/\sqrt3), s_i=\sin(k_i/\sqrt3)$, $s\in\{+1,-1\}$ the branch label): under $\mathbf k\to-\mathbf k$, $c_i$ is even and $s_i$ is odd, giving

$$u^s(-\mathbf k)=u^{-s}(\mathbf k),\quad n_x^s(-\mathbf k)=-n_x^{-s}(\mathbf k),\quad n_y^s(-\mathbf k)=n_y^{-s}(\mathbf k),\quad n_z^s(-\mathbf k)=-n_z^{-s}(\mathbf k)$$

(direct substitution into the four `_bcc_uvec` formulas; $n_y$ is the odd one out — the module docstring's own remark that "the sign flip on the $y$-component is an intrinsic chirality convention of the Bisio BCC walk" is precisely this asymmetry). Relabelling $s\to-s$: $A^{-s}(-\mathbf k)$ has $(u,n_x,n_y,n_z) = (u^s(\mathbf k), -n_x^s(\mathbf k), n_y^s(\mathbf k), -n_z^s(\mathbf k))$ — exactly the pattern $\sigma_y A^s(\mathbf k)\sigma_y$ produces (same conjugation identities as above, applied to $A^s$ instead of its conjugate). Hence identity (II).

### 3.2 The CPT operator identity for $D(\mathbf k)$

Write $D(\mathbf k)=\begin{pmatrix}a&b\\c&d\end{pmatrix}$ with $a=nA^+(\mathbf k)$, $b=c=im\mathbb1$, $d=n A^+(\mathbf k)^\dagger$. Block-swap-then-conjugate ($M$ acting by conjugation swaps rows then columns, then applies $\sigma_y$ to each resulting block — $\Sigma$ and $\sigma_y\!\oplus\!\sigma_y$ commute as matrices, order is immaterial):

$$M\,D(\mathbf k)^{*}\,M = \begin{pmatrix}\sigma_y\,d^{*}\,\sigma_y & \sigma_y\,c^{*}\,\sigma_y\\ \sigma_y\,b^{*}\,\sigma_y & \sigma_y\,a^{*}\,\sigma_y\end{pmatrix} = \begin{pmatrix} n\,\sigma_y\bigl(A^+(\mathbf k)^\dagger\bigr)^{*}\sigma_y & -im\mathbb1\\ -im\mathbb1 & n\,\sigma_y A^+(\mathbf k)^{*}\sigma_y\end{pmatrix}$$

(the mass terms are unaffected: $m$ real, $(im\mathbb1)^*=-im\mathbb1$, and $\sigma_y\mathbb1\sigma_y=\mathbb1$). Now apply (I) to the conjugate directly — $\sigma_y A^+(\mathbf k)^*\sigma_y = \sigma_y\bigl(\sigma_y A^+(\mathbf k)\sigma_y\bigr)\sigma_y = A^+(\mathbf k)$ (using (I) once and $\sigma_y^2=\mathbb1$ twice) — giving $\sigma_y A^+(\mathbf k)^*\sigma_y = A^+(\mathbf k)$, and its dagger $\sigma_y (A^+(\mathbf k)^\dagger)^*\sigma_y = A^+(\mathbf k)^\dagger$. So:

$$M\,D(\mathbf k)^{*}\,M = \begin{pmatrix} n\,A^+(\mathbf k)^\dagger & -im\mathbb1\\ -im\mathbb1 & n\,A^+(\mathbf k)\end{pmatrix} = D(\mathbf k)^\dagger = D(\mathbf k)^{-1}$$

(the last equality by $D(\mathbf k)$'s own exact unitarity). This is $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ for $\Theta=MK$, at **every** $\mathbf k$, **without invoking identity (II) at all** — (I) alone suffices once chained through the dagger. (II) is not needed for this identity; it is needed for §4's separate, negative statement about parity.

### 3.3 Position-space meaning

Fourier convention: for a position-space field $\psi(x)$, $\bigl(\psi^{*}\bigr)^{\sim}(\mathbf k) = \tilde\psi(-\mathbf k)^{*}$. So the antiunitary map $(\Theta\psi)(x):= M\,\psi(-x)^{*}$ has momentum-space action $(\Theta\psi)^{\sim}(\mathbf k) = M\,\tilde\psi(-\mathbf k)^{*}$. If $\tilde\psi(t+1,\mathbf k)=D(\mathbf k)\tilde\psi(t,\mathbf k)$, define $\phi(t,\mathbf k):=(\Theta\psi(t))^\sim(\mathbf k)=M\tilde\psi(t,-\mathbf k)^{*}$; a short calculation (using $M D(-\mathbf k)^{*}M = D(-\mathbf k)^\dagger$, i.e. §3.2's identity evaluated at $-\mathbf k$ rather than $\mathbf k$ — the identity holds at every momentum, so this substitution is free) shows $\phi(t+1,\mathbf k)=D(\mathbf k)^{-1}\phi(t,\mathbf k)$: $\Theta$ maps a forward-time trajectory of $\psi$ to a **backward-time** trajectory of $\phi=\Theta\psi$, at the same momentum label — the operational meaning of an antiunitary time-reversal-type symmetry for a discrete/Floquet unitary.

### 3.4 $\Theta^2=-1$ (Kramers)

$\Theta(\Theta\psi)(x) = M\bigl[(\Theta\psi)(-x)\bigr]^{*} = M\bigl[M\psi(x)^{*}\bigr]^{*} = MM^{*}\psi(x)$. With $M=\Sigma(\sigma_y\!\oplus\!\sigma_y)$: $M^{*}=\Sigma\bigl(-\sigma_y\!\oplus\!-\sigma_y\bigr)=-M$ ($\Sigma$ real, $\sigma_y^{*}=-\sigma_y$), so $MM^{*}=-M^2=-\mathbb1$ ($\Sigma^2=\mathbb1$, $(\sigma_y\!\oplus\!\sigma_y)^2=\mathbb1$, and they commute). $\Theta^2=-1$ exactly — verified to literal `0.0` (`theta_squared`, leg C1).

## 4. Why parity alone cannot exist at finite $\mathbf k$ (a spectral obstruction, not merely an unproven claim)

$D(\mathbf k)$'s eigenvalues are $e^{\pm i\omega(\mathbf k)}$, $\omega(\mathbf k)=\arccos\bigl(n\,u^+(\mathbf k)\bigr)$, each two-fold degenerate (this is the same fact F327 §2.1 used). Because the construction uses **only** branch $+$ (paired with its own dagger, §2), $\omega(-\mathbf k)$ is governed by $u^+(-\mathbf k)=u^{-}(\mathbf k)$ — a **different** function of $\mathbf k$ than $u^+(\mathbf k)$ in general. Measured over 500 random $(\mathbf k,m)$ samples, $\min|\omega(\mathbf k)-\omega(-\mathbf k)| = 1.58\times10^{-5}$ (never zero at generic $\mathbf k$; leg D1), while it vanishes identically on a cubic axis ($k_y=k_z=0\Rightarrow s_ys_z$-type terms drop out — leg D2, literal `0.0`, matching F301's own "exact on cubic axes").

Conjugation by **any** fixed (momentum-independent) matrix preserves a matrix's eigenvalue spectrum. Since $D(\mathbf k)$ and $D(-\mathbf k)$ generically have **different** spectra, **no fixed unitary $\Pi$ can satisfy $\Pi D(\mathbf k)\Pi^{-1}=D(-\mathbf k)$ for every $\mathbf k$** — not "none has been found," but an outright obstruction from the eigenvalues alone. This re-derives F301's chirality-odd finite-$a$ Poincaré defect independently, as a spectral fact about $D(\mathbf k)$ itself rather than by importing F301's result. Consistently, the naive candidate $\Pi=\Sigma$ (plain block swap, no twist, no $K$) misses $D(-\mathbf k)$ by $O(1)$ — measured $1.93$, not a small defect (leg D3).

**So even the free, gauge-decoupled kinetic+mass term of this lattice Dirac fermion is not parity-symmetric at any finite $\mathbf k$** — a strictly *stronger* and *independent* statement than F53's "$P$ maximally violated by the charged current" (that is about the interaction; this is about the free term) and independent of F327's exclusion of a single physical branch on experimental grounds (that is about which representation is physically realized; this is an algebraic fact about the representation regardless of whether it is realized). Only the **full** combination $\Theta=CPT$-type survives, exactly, to all orders in $\mathbf k$.

## 5. What this supersedes in *character*, not in content

F53 P6 ("$\omega_0(+m)=\omega_0(-m)$") is not withdrawn — it is a true, cheaper corollary of the fact that $D(\mathbf k)$ and $D(\mathbf k)^{-1}$ share a spectrum, which this finding's Θ makes an operator statement rather than leaves as a numerical observation. F53's $C$, $P$ label-level content is untouched; it answers a different question (representation bookkeeping under the gauge group) than this finding does (an operator on the Hilbert space of the free walk). Nothing here rewrites F53.

`ca-reference.md`'s "Time-reversibility" section is reproduced exactly as a **negative control** (`naive_reversal_residual`, leg E2): running $D$ forward then $D^\dagger$ backward returns to the start at the floating-point floor ($8.0\times10^{-16}$) — expected of **any** unitary CA, and carrying no antiunitary content. Contrast leg E1: propagating forward under $\Theta$-then-forward-again (not backward) reproduces $\Theta$ applied to the original state, also at the floating floor ($8.5\times10^{-16}$, $N=12$ steps, full nonlinear FFT-mediated many-step walk, not just the single-tick matrix identity). That distinction — E1 vs E2 — **is** the difference between having a CPT theorem and having noted that a reversible automaton is reversible, and it is why the existing reference section was not sufficient to close this row.

## 6. Scope, stated narrowly — what remains open

This is a **free-fermion** theorem: no SU(2)$_L$ charged current, no hypercharge, no W/Z/gluon coupling. F53's own finding is that $C$ and $P$ are "maximally violated by the charged current" — a statement about the **interaction**, entirely untouched here. The charged-current coupling (`casim.engine.gauge.charged_current`) couples to the left ($\eta$) block only, is a nonlinear multiplicative gate (not a closed-form momentum-diagonal $2\times2$/$4\times4$ unitary the way $D(\mathbf k)$ is), and extending the present algebraic method to it — checking whether $\Theta$, possibly composed with F53's charge-conjugation charge-label map, still intertwines the full gauged one-tick evolution with its inverse — is real additional derivation, **not attempted here** and not assumed to go through by analogy with the continuum Lüders–Pauli argument (that argument's hypotheses — continuum Lorentz invariance chief among them — are exactly what row A2 says this model only partially has).

So: row A4 moves from *"no CPT theorem, T is thin"* to *"an exact CPT-type theorem for the free sector, built and verified at the operator level for the first time in this project; the interacting/gauge-coupled sector's CPT status is a **named**, structurally-scoped open question rather than an unexamined one."* This is a genuine promotion in what the row can honestly claim, not a full closure — the same shape as F327's move on row A2 (narrower and, in that case, worse; here narrower and better, but still not the whole row).

## 7. Checks (12/12 PASS)

| Leg | Statement | Result |
|---|---|---|
| A1 | $A^s(\mathbf k)^{*}=\sigma_y A^s(\mathbf k)\sigma_y$, any fixed $\mathbf k$, either branch (500 samples) | `0.0` |
| A2 | $A^+(\mathbf k)^{*}=A^-(-\mathbf k)$ (500 samples) | `0.0` |
| B1 | $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$, random $(\mathbf k,m)$, 500 samples | `0.0` |
| B2 | same, at $\mathbf k=0$, axis-aligned $\mathbf k$, $\lvert m\rvert\in\{0,1\}$ — no small-$\mathbf k$ expansion | `0.0` |
| B3 | $D(\mathbf k)$ exactly unitary (sanity) | $4.4\times10^{-16}$ |
| C1 | $\Theta^2=-1$ (Kramers) | `0.0` |
| C2 | $M$ exactly unitary | `0.0` |
| D1 | $\omega(\mathbf k)\ne\omega(-\mathbf k)$ generically (min over 500 samples) | $1.58\times10^{-5}$ |
| D2 | vanishes identically on a cubic axis (consistency with F301) | `0.0` |
| D3 | plain $\Sigma$ alone misses $D(-\mathbf k)$ by $O(1)$ | $1.93$ |
| E1 | many-step ($N=12$) nonlinear real-space round trip under $\Theta$ | $8.5\times10^{-16}$ |
| E2 | plain forward/backward invertibility (negative control on the existing reference-doc check) | $8.0\times10^{-16}$ |

**Control** (`use_naive_theta=true`, drops the $\sigma_y$ twist from $M$, keeps $\Sigma$ and $K$): reddens B1 ($1.95$), B2 ($1.34$), C1 ($\Theta^2\to+1$, residual $2.0$ against $-1$), and E1 ($0.093$) — exactly the four legs that depend on the twist. A1, A2 (properties of $A^s(\mathbf k)$ alone), B3, C2 (the internal matrix is still unitary even without the twist), D1–D3 (the parity obstruction, independent of which $\Theta$ is under test), and E2 all stay green, confirming the reddened legs measure the twist and not a bookkeeping tautology. **VERIFIED RED 2026-08-26.**

## 8. New exactness-inventory entries

- **Tier 1 (algebraic exact):** identities (I), (II) (A1, A2); the CPT operator identity $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ at every sampled $\mathbf k,m$ and at the $\mathbf k=0$/axis/$\lvert m\rvert\in\{0,1\}$ edge cases (B1, B2); $\Theta^2=-1$ (C1); $M$ unitarity (C2); the D2 axis-degeneracy of the parity obstruction.
- **Tier 2 (machine precision):** $D(\mathbf k)$ unitarity sanity (B3, $4.4\times10^{-16}$); the many-step real-space round trip (E1, $8.5\times10^{-16}$); the negative-control invertibility check (E2, $8.0\times10^{-16}$).
- **Measured, not exact by construction (a genuine numeric fact about generic $\mathbf k$, not a target tolerance):** D1's spectral mismatch ($1.58\times10^{-5}$ at the sampled minimum) and D3's $O(1)$ naive-parity failure ($1.93$).
