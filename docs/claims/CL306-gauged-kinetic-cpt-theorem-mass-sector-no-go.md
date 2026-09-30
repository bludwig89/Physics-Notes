---
id: CL306
title: 'A uniform SU(2)_L link grafted into the free BCC Dirac walk''s kinetic term admits an exact discrete CPT-type theorem via the SU(2) pseudoreality identity tau_2 U tau_2^-1 = U*, with a flipped (non-Kramers) antiunitary involution; the same walk''s SU(2)-gauged mass-generation mechanism admits no fixed-isospin-operator analogue, by a general group-theoretic obstruction'
slug: gauged-kinetic-cpt-theorem-mass-sector-no-go
tier: supporting
kind: derivation
status: live
domain: [SM, QFT]
exactness: exact
findings: [F378, F328, F53]
tests: [F378-discrete-cpt-gauged-theorem]
modules: [casim.engine.particles.discrete_cpt_gauged]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL285
falsifier: stated
first_issued: 2026-09-09
last_verified: 2026-09-09
provenance: authored
review_state: authored
confidence: high
---

# CL306 — The SU(2)$_L$-gauged kinetic term extends F328's discrete CPT theorem via SU(2) pseudoreality; the model's own gauged mass mechanism does not, by a general obstruction

## Statement

Grafting a spatially-uniform SU(2) link $U$ into **just the kinetic block** of the free massive
BCC Dirac walk's own branch-$+$/dagger architecture (`casim.engine.particles.dirac_bcc`, the
module [[F328]] covers) gives $D'(\mathbf k)=\begin{pmatrix}n(A^+(\mathbf k)\otimes U) & im\mathbb1_4\\
im\mathbb1_4 & n(A^+(\mathbf k)\otimes U)^\dagger\end{pmatrix}$, and

$$\Theta' D'(\mathbf k)\Theta'^{-1}=D'(\mathbf k)^{-1},\qquad
\Theta':=M'\cdot K,\quad M':=\Sigma\cdot(\sigma_y\!\otimes\!\tau_2\ \oplus\ \sigma_y\!\otimes\!\tau_2),$$

holds **exactly**, every sampled $\mathbf k$, every $|m|\le1$ (edge cases included, no small-$k$
expansion), machine precision $\sim10^{-16}$ — using the SU(2) pseudoreality identity
$\tau_2 U\tau_2^{-1}=U^{*}$ (true for every $U\in SU(2)$) in place of F328's identity (I) for the
isospin factor. $\Theta'^2=+\mathbb1$, **not** F328's Kramers $\Theta^2=-\mathbb1$: tensoring a
second pseudoreal twist onto the spin twist flips the antiunitary involution class.

Once the **mass** term is also SU(2)-gauged (a second, independent link $V$ mixing the two
chiralities — the Stueckelberg-type mechanism `casim.engine.gauge.weak_wmu.covariant_dirac_doublet_step`
actually uses), $\Theta'$ fails at $O(1)$ for every tested $V$ (residual $2.85$, random samples),
and **no fixed isospin operator can fix this**: the block algebra requires $\Lambda V^T\Lambda^{-1}=V$
for every $V\in SU(2)$, but $V\mapsto V^T$ is a group anti-automorphism while conjugation by any
fixed $\Lambda$ is an automorphism, and the two coincide only on an abelian group — SU(2) is not
one. A 500-sample Monte-Carlo search over random unitary $2\times2$ $\Lambda$ against two fixed
non-commuting SU(2) elements finds no candidate closer than $0.28$, consistent with the algebraic
impossibility being generic.

## What it extends

**Completeness rubric row A4 / ledger row A4r**, which [[F328]] moved from "no operator CPT
theorem" to "an exact free-sector theorem; the gauge-coupled extension is the named residual."
This card answers the residual's kinetic half in the affirmative and its mass half in the
negative, for the specific (fixed-background) ansatz tested — see **What it explicitly does NOT
claim** below for the boundary that keeps this narrow.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go.md` §2 | closed-form momentum-diagonal $8\times8$ gauge-coupled walk, verified against the real `covariant_dirac_doublet_step` | machine, $1.2\times10^{-15}$ (leg X0) |
| `findings/F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go.md` §4 | the kinetic-sector CPT theorem $\Theta'D'(\mathbf k)\Theta'^{-1}=D'(\mathbf k)^{-1}$, random $(\mathbf k,m,U)$ and edge cases | exact, $\sim10^{-16}$ (legs A1, B1, B2, B3) |
| `findings/F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go.md` §4 | $\Theta'^2=+\mathbb1$, not $-\mathbb1$ | exact, `0.0` / $2.0$ (legs C1, C1b) |
| `findings/F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go.md` §5 | the mass-sector no-go: algebraic derivation of the required (impossible) identity, plus a true-but-different identity $\tau_2V^T\tau_2^{-1}=V^{-1}$ and a 500-sample Monte-Carlo $\Lambda$-search | exact / structural (legs D1, D2, D3) |
| record `F378-discrete-cpt-gauged-theorem` → `test-results/F378_discrete_cpt_gauged_theorem.json` | 11/11, battery tier, `exact`, tol $10^{-10}$; one `--param use_naive_iso=True` control verified red on exactly four legs | machine |

External anchor: the SU(2) pseudoreality relation ($\tau_2$-conjugation implementing complex
conjugation on the fundamental representation) is the same fact underlying Majorana mass terms
and the reality of the electroweak doublet in the continuum theory — standard, not novel; what is
new here is that it exactly repairs a *discrete*, finite-lattice-spacing CPT identity.

## What it explicitly does NOT claim

**Not** a claim that the model's SU(2)$_L$ gauge theory violates CPT as a physical statement.
Every test above holds the classical gauge/mass link **fixed** under the antiunitary map — $\Theta$
is required to map the walk at background $(U,V)$ to the inverse of the walk at the **same**
$(U,V)$, mirroring exactly how F328 tested $D(\mathbf k)$ against $D(\mathbf k)^{-1}$ at the same
mass $m$. A genuine gauge-theory CPT statement instead lets $C,P,T$ **also** transform the gauge
field itself (the connection does not sit still under charge conjugation in the continuum theory
either); whether letting $\Theta$ map the mass background $V$ to some other $V'$ restores an
identity is a different, unattempted question, named as the new residual on ledger row A4r.

**Not** a resolution of the pre-existing mismatch between `covariant_dirac_doublet_step`'s
branch-$+/-$ kinetic pairing and `dirac_bcc.py`'s branch-$+$/dagger pairing (F378 §3): the actual
gauge-coupled module in the tree fails F328's identity even at **zero** gauge coupling, for a
reason unrelated to this card's content, and that mismatch is named but not fixed here.

**Not** a reuse of F321's $\theta_\text{QCD}$ result, and not a claim about C, P, T individually
outside the combined $\Theta$ (or $\Theta'$) — same scope discipline as [[CL285]].

## Falsifier

A momentum $\mathbf k$, mass $m$, or link $U$ (within $|m|\le1$, $U\in SU(2)$) at which
$\lVert\Theta' D'(\mathbf k)\Theta'^{-1}-D'(\mathbf k)^{-1}\rVert\ne0$ to machine precision, for
the kinetic-only construction, would falsify the positive half — not expected, since the identity
is proved in closed form (F378 §4) via an exact group-theory relation, not fit or sampled into
agreement. A discovery that some OTHER fixed operator $\Lambda\ne\tau_2$ (or a $\Lambda$ acting on
a larger space than the bare isospin doublet) satisfies $\Lambda V^T\Lambda^{-1}=V$ for every
$V\in SU(2)$ would falsify the no-go half — excluded here by the anti-automorphism/automorphism
argument, which holds for any fixed $\Lambda$ on the $2\times2$ isospin space, not just the two
candidates tried.

## Status & history

`live` as stated, first issued 2026-09-09, narrowing ledger row A4r's residual rather than closing
it — the same "narrowed, not closed" shape as CL285 itself and as ledger row A6r before it fully
closed. Rolls up to [[CL285]]; CL285's own "What it explicitly does NOT claim" section should be
read alongside this card's scope note rather than as superseded by it — CL285 still correctly
describes the state of the free sector, and this card adds the gauge-coupled sector's own,
narrower story next to it.

## Sources

- `findings/F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go.md`
- `findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md` (the free-sector theorem this extends)
- `findings/F53-fg9-C-CP-per-species.md` (the charged-current parity-violation observation this
  makes operator-precise for the kinetic sector, and leaves open for the mass sector)
- `docs/claims/CL285-discrete-cpt-theorem-free-dirac-walk.md` (the card this rolls up to)
- `docs/status/open-derivations.md` row A4r
