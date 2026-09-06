---
id: CL285
title: 'The free BCC Dirac walk has an exact discrete CPT theorem: Theta = Sigma . (sigma_y (+) sigma_y) . K satisfies Theta D(k) Theta^-1 = D(k)^-1 at every k and every mass, and no fixed unitary parity can exist at finite k at all'
slug: discrete-cpt-theorem-free-dirac-walk
tier: headline
kind: derivation
status: live
domain: [SR, QFT]
exactness: exact
findings: [F328, F53, F301, F327, F26]
tests: [F328-discrete-cpt-theorem]
modules: [casim.engine.particles.discrete_cpt]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-26
last_verified: 2026-08-26
provenance: authored
review_state: authored
confidence: high
---

# CL285 — An exact discrete CPT theorem for the free BCC Dirac walk

## Statement

The BCC Weyl one-tick unitary $A^s(\mathbf k)=u^s(\mathbf k)\mathbb1-i(n_x^s\sigma_x+n_y^s\sigma_y+n_z^s\sigma_z)$
obeys two exact algebraic identities of its specific cos/sin embedding: $A^s(\mathbf k)^{*}=\sigma_y
A^s(\mathbf k)\sigma_y$ at any fixed $\mathbf k$, and $A^{-s}(-\mathbf k)=\sigma_y A^s(\mathbf k)\sigma_y$
(branch swap plus momentum flip). Chaining these through the massive BCC Dirac one-tick unitary
$D(\mathbf k)=\begin{pmatrix}nA^+(\mathbf k)&im\mathbb1\\im\mathbb1&nA^+(\mathbf k)^\dagger\end{pmatrix}$
gives, for **every** momentum $\mathbf k$ and **every** admissible mass $\lvert m\rvert\le1$, with no
small-$k$ expansion anywhere:

$$\Theta\,D(\mathbf k)\,\Theta^{-1}=D(\mathbf k)^{-1},\qquad \Theta:=M\cdot K,\quad
M:=\Sigma\cdot(\sigma_y\!\oplus\!\sigma_y),\quad \Sigma=\begin{pmatrix}0&\mathbb1\\\mathbb1&0\end{pmatrix}.$$

$K$ is complex conjugation and $\Sigma$ the $\eta\leftrightarrow\chi$ block swap (the standard Dirac
parity matrix $\gamma^0$ in the Weyl basis). In position space $(\Theta\psi)(x)=M\psi(-x)^{*}$ — spatial
reflection, an internal spin-and-chirality twist, and complex conjugation combined into one antiunitary
operator, satisfying $\Theta^2=-1$ exactly (the Kramers signature of a genuine spin-$\tfrac12$
antiunitary symmetry). Verified to literal `0.0` over 500 random $(\mathbf k,m)$ samples plus the
$\mathbf k=0$/axis-aligned/$\lvert m\rvert\in\{0,1\}$ edge cases, and confirmed at machine precision
($\sim10^{-16}$) in a full nonlinear, many-step, FFT-mediated real-space propagation test.

**Companion no-go, same finding:** conjugation by any fixed (momentum-independent) unitary preserves a
matrix's eigenvalue spectrum, and $D(\mathbf k)$, $D(-\mathbf k)$ generically have **different** spectra
($\omega(\mathbf k)=\arccos(n\,u^+(\mathbf k))\ne\omega(-\mathbf k)$, vanishing only on the cubic axes) —
so **no fixed unitary parity operator can exist for this walk at any finite $\mathbf k$**, even for the
free, gauge-decoupled kinetic+mass term. This is a spectral obstruction, not merely an unproven claim,
and it independently re-derives F301's chirality-odd finite-$a$ Poincaré defect as a property of
$D(\mathbf k)$'s own eigenvalues.

## What it extends

**Completeness rubric row A4** ("CPT, and C, P, T separately"), PARTIAL for five prior reports on the
strength of F53's charge-*label* bookkeeping ($C$, $P$ maximal, $CP$ exact per species — a statement
about SU(2)$\times$U(1) representation content, not an operator on the model's Hilbert space) and F53
P6's scalar corollary $\omega_0(+m)=\omega_0(-m)$. No module before this one built $C$, $P$ or $T$ as a
matrix on the one-tick unitary and checked it against the rule. This card is the first operator-level
discrete-symmetry theorem in the project.

It is also a direct answer to the row's own standing question — whether a CPT theorem can exist here at
all, given the model is only PARTIAL on continuum Lorentz invariance (row A2) and standard CPT proofs
(Streater–Wightman) assume it: **yes, for the free sector, and the proof route used here does not invoke
continuum Lorentz invariance at any step** — it is a direct algebraic identity of the lattice
construction, exact at finite $\mathbf k$, not a continuum-limit statement.

## What it explicitly does NOT claim

**Not** a theorem about the gauge-coupled sector. The SU(2)$_L$ charged current couples to the left
($\eta$) block only (F53's own "$C$, $P$ maximally violated by the coupling"), is a nonlinear
multiplicative gate rather than a closed-form momentum-diagonal unitary, and whether $\Theta$ — possibly
composed with F53's charge-conjugation label map — still intertwines the full gauged evolution with its
inverse is open (ledger row `A4r`), not attempted and not assumed to transfer from the continuum
Lüders–Pauli argument.

**Not** a reuse of F321's $\theta_\text{QCD}$ reality result. F321 is a statement about the strong-CP
angle (row B11), a different object; three prior completeness reports flagged borrowing it for row A4 as
a standing trap, and this card does not do so.

**Not** a claim that ordinary parity or time-reversal individually hold anywhere in this model — the
companion no-go above shows the opposite for the free sector, and F53 already showed it for the
interaction. The claim is specifically about the **combined** antiunitary $\Theta$.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` §3.1 | identities (I) $A^s(\mathbf k)^{*}=\sigma_y A^s(\mathbf k)\sigma_y$ and (II) $A^{-s}(-\mathbf k)=\sigma_y A^s(\mathbf k)\sigma_y$ | exact, $0.0$ over 500 samples (legs A1, A2) |
| `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` §3.2 | the block-matrix chain: (I)+(II) $\Rightarrow \Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ | exact, $0.0$ at 500 random $(\mathbf k,m)$ plus 5 edge cases incl. $\mathbf k=0$, axis-aligned, $\lvert m\rvert\in\{0,1\}$ (legs B1, B2); $D(\mathbf k)$ unitary to floating floor (leg B3) |
| `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` §3.4 | $\Theta^2=-1$ exactly (Kramers), $M$ unitary | exact, $0.0$ (legs C1, C2) |
| `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` §4 | spectral no-go: $\omega(\mathbf k)\ne\omega(-\mathbf k)$ at generic $\mathbf k$ (nonzero over 500 samples), vanishes on cubic axes, naive block-swap-only parity misses $D(-\mathbf k)$ by $O(1)$ | exact/structural (legs D1, D2, D3) |
| `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` §3.3 | real-space many-step ($N=12$) nonlinear FFT round trip under the real $\Theta$; contrast against plain forward-then-dagger invertibility (not a symmetry test) | machine, $8.5\times10^{-16}$ (leg E1) vs. sanity-only leg E2 |
| record `F328-discrete-cpt-theorem` → `test-results/F328_discrete_cpt_theorem.json` | 12/12, gate tier, `exact`, tol $10^{-10}$; one `--param use_naive_theta=True` control verified red on exactly B1, B2, C1, E1 | machine |

External anchor: Streater & Wightman, *PCT, Spin and Statistics, and All That* (the continuum CPT
theorem this result does not invoke — the proof route here uses no continuum Lorentz invariance at any
step, which is the point).

## Falsifier

A momentum $\mathbf k$ and mass $m$ (within $\lvert m\rvert\le1$) at which
$\lVert\Theta D(\mathbf k)\Theta^{-1}-D(\mathbf k)^{-1}\rVert\neq0$ to machine precision would falsify
the theorem as stated — not expected, since the identity is proved algebraically in closed form
(`findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` §3) rather than fit or sampled into agreement, and the derivation uses no
approximation. A discovery that some OTHER fixed unitary $\Pi\neq\Sigma$ implements exact parity
($\Pi D(\mathbf k)\Pi^{-1}=D(-\mathbf k)$ for all $\mathbf k$) would falsify the companion no-go — ruled
out here by the spectral mismatch argument, which holds for any fixed $\Pi$, not just $\Sigma$.


## Status & history

`live` as stated, first issued 2026-08-26, closing (narrowly) rubric row A4 for the free sector.
Rubric row A4 stays `PARTIAL` overall — the gauge-coupled extension is the named residual, tracked as
ledger row `A4r`, not silently assumed. This is the same "row narrowed, not closed" shape as ledger row
`A6r`.

## Sources

- `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md`
- `findings/F53-fg9-C-CP-per-species.md` (per-species C, P, CP charge-label content this extends past, in kind not in content)
- `findings/F301-finite-a-boost-covariance-poincare-defect.md` (the spectral defect the companion no-go re-derives)
- `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` (independent confirmation that
  $D(\mathbf k)$, $D(-\mathbf k)$ carry different physics at finite $\mathbf k$)
- `docs/theory/ca-reference.md` Time-reversibility section (shown, via the E2 control leg, to test plain
  unitary invertibility rather than any antiunitary symmetry)
- `docs/status/open-derivations.md` row `A4r`
- Streater & Wightman, *PCT, Spin and Statistics, and All That* (Princeton, 1964/2000) — the continuum
  CPT theorem this generalizes past, deliberately without its hypothesis
