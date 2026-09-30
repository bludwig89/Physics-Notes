# F378 — F328's discrete CPT theorem extends to the SU(2)_L-gauged kinetic term via SU(2) pseudoreality; the model's own SU(2)-gauged mass mechanism obstructs it by a general group-theoretic no-go

**Date:** 2026-09-09 - 00:45
**Numbering:** **F378**, taken as `NEXT FREE NUMBER` (max+1; no gaps were free). Session `cowork-A4r-cpt-gauged-2026-09-09`, sector `particles`.
**Status:** Confirmed — **11/11 PASS**, one declared `--param` control verified red on exactly four legs.
**Reviewed:** 2026-09-09 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F378-review-2026-09-09.md))
**Module:** `src/casim/engine/particles/discrete_cpt_gauged.py` (new)
**Test record:** record `F378-discrete-cpt-gauged-theorem` (tier battery, kind assertion, `expect.exactness: exact`) → `test-results/F378_discrete_cpt_gauged_theorem.json`
**Extends (narrowly, two directions):** ledger row **A4r** / completeness rubric row **A4** — moves from "an exact free-sector theorem; the gauge-coupled extension is the named residual" to "the SU(2)_L-gauged *kinetic* term also has an exact theorem, via a specific isospin generalisation of F328's twist; the model's own SU(2)-gauged *mass* mechanism has a genuine, general, algebraic obstruction to that same ansatz." Does **not** close row A4r outright: see §6.
**Cross-references:** [[F328-discrete-cpt-theorem-free-bcc-dirac-walk]] (the free-sector theorem this extends; its Θ, its identity (I), and its own stated residual — this finding's starting point), [[F53-fg9-C-CP-per-species]] (per-species charge-label C/P/CP; "C, P maximally violated by the charged current" is the observation ledger row A4r asked this session to make operator-precise), [[F91-pairing-classification-theorem]] (even/chiral propagator classification — cited for context on the gauge sector, not reused algebraically)
**Explicitly excluded:** [[F321-strong-cp-theta-zero-and-loop-stable]] (θ_QCD reality, rubric row B11, a different object — not invoked anywhere below, per the same standing trap F328 already flagged for this row).

---

## 1. What was open

F328 proved $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ exactly for the free (gauge-decoupled) massive BCC Dirac walk, and named the SU(2)$_L$ charged-current extension as the row's residual (ledger row A4r): does $\Theta$ — possibly composed with an isospin-space operation — still intertwine the full gauge-coupled one-tick evolution with its inverse? The row's own brief warned against assuming the continuum Lüders–Pauli argument transfers, since its hypotheses (continuum Lorentz invariance) are exactly what row A2 only partially has, and named the FIRST STEP: build the gauge-coupled walk as an explicit momentum-diagonal matrix and test F328's $\Theta$ against it numerically before attempting an analytic extension.

## 2. Building the momentum-diagonal gauge-coupled walk

`casim.engine.gauge.weak_wmu.covariant_dirac_doublet_step` couples an SU(2)$_L$ doublet $(\nu,e)$ or $(u,d)$ to a link field via `covariant_weyl_step_3d_bcc`: gauge-rotate the isospin doublet in **position space** with a site-centred effective link $U_\text{eff}(x)$, then apply the ordinary spectral BCC Weyl step. At a **spatially uniform** link ($U_\text{eff}(x)\equiv U$, a fixed SU(2) matrix), the gauge rotation commutes with the FFT, so the whole kinetic step is *exactly* momentum-diagonal and factorises as a Kronecker product of the spin operator (acting on the BCC Weyl 2-spinor) and the constant isospin matrix $U$ (acting on $(\nu,e)$) — no O(a) approximation, no lattice-spacing caveat, at this special uniform configuration. The right-handed singlet $\chi$ uses identity links always (no SU(2)$_L$ coupling, per F53/F34). The mass step is a Strang-type rotation $\cos(m)\,\mathbb 1\oplus\cos(m)\,\mathbb 1$ off-diagonal-mixed by $i\sin(m)\,(\mathbb 1_2\otimes V)$, with $V$ a second SU(2) link (the model's Stueckelberg-type mass-generation mechanism, CLAUDE.md decision 4).

This gives an explicit closed-form $8\times8$ matrix `D_covariant_doublet(k, m, U, V)` (basis order $[f_\nu,f_e,g_\nu,g_e,\chi_\nu^f,\chi_e^f,\chi_\nu^g,\chi_e^g]$, spin-major/isospin-minor within each chirality block), **verified against the real module function to $1.2\times10^{-15}$** at a grid-compatible momentum and a uniform link field (leg X0) — the closed form is not a hand-derived proxy, it reproduces the actual code.

## 3. First result: the actual module fails already at zero gauge coupling (leg E1)

Testing F328's $\Theta$ (isospin left untouched, $\Theta_8=\Sigma_8\cdot(\sigma_y\otimes\mathbb 1_2\oplus\sigma_y\otimes\mathbb 1_2)\cdot K$) against `D_covariant_doublet(k,m,\mathbb 1,\mathbb 1)$ — **zero gauge coupling, $U=V=\mathbb1$** — gives a residual of $1.96$, an $O(1)$ failure, over 300 random $(\mathbf k,m)$ samples. This is **not** a statement about the SU(2)$_L$ coupling: it happens because `covariant_dirac_doublet_step`'s kinetic term pairs branch $+$ ($\eta$) with the **true opposite branch** $-$ ($\chi$, via `sign='-'` in its own `covariant_weyl_step_3d_bcc` call), not with branch $+$'s **own dagger** the way `casim.engine.particles.dirac_bcc.dirac_step_3d_bcc_splitstep` does (F328's own module, whose docstring calls that pairing "the choice forced by unitarity of the full $4\times4$ $D_k$" for *its* non-Strang-split mass ansatz). These are two different discretisations of "the massive BCC Dirac fermion" already coexisting in the tree, unitary by two different mechanisms (dagger-pairing vs. Strang-split trigonometric mixing), and only `dirac_bcc.py`'s has a proven CPT theorem. **This cross-module mismatch is named here, not resolved** — see §6.

## 4. Isolating the gauge-coupling question: kinetic sector (positive result)

To separate the branch-pairing mismatch from the actual gauge-coupling question, this finding builds a companion construction, `D_grafted(k,m,U,V)`, that grafts the SU(2) link directly into `dirac_bcc.py`'s **own** branch-$+$/dagger architecture — literally $A^+(\mathbf k)\to A^+(\mathbf k)\otimes U$ in the kinetic block, everything else (including unitarity, which now follows automatically since $(A\otimes U)^\dagger=A^\dagger\otimes U^\dagger$) unchanged. With $V=$ none (mass stays an isospin scalar, $im\,\mathbb1_4$):

$$D'(\mathbf k) = \begin{pmatrix} n\,(A^+(\mathbf k)\otimes U) & im\,\mathbb1_4\\ im\,\mathbb1_4 & n\,(A^+(\mathbf k)\otimes U)^\dagger\end{pmatrix}.$$

**Claim:** $\Theta' D'(\mathbf k)\Theta'^{-1}=D'(\mathbf k)^{-1}$ exactly, with

$$\Theta' := M'\cdot K,\qquad M':=\Sigma_8\cdot(\sigma_y\otimes\tau_2\ \oplus\ \sigma_y\otimes\tau_2),$$

where $\tau_2=\sigma_y$ (numerically the same $2\times2$ matrix, kept as a separate name for the isospin factor) and $\Sigma_8$ swaps the $\eta$/$\chi$ 4-blocks as before.

**Why:** the mechanism is F328's own §3.2 argument with the isospin factor threaded through. F328's identity (I), $\sigma_y A^s(\mathbf k)^{*}\sigma_y = A^s(\mathbf k)$, generalises using the **pseudoreality of the fundamental SU(2) representation**: for every $U\in SU(2)$,

$$\tau_2\,U\,\tau_2^{-1} = U^{*}\qquad\text{(identity (III), verified to literal }0.0\text{ over 500 random }U\text{, leg A1)}$$

— the standard fact underlying the reality of the SU(2) doublet and Majorana mass constructions. Combined with F328's identity (I) for the spin factor via the mixed-product rule $(\sigma_y\otimes\tau_2)(A\otimes U)(\sigma_y\otimes\tau_2)=(\sigma_yA\sigma_y)\otimes(\tau_2U\tau_2)=A^{*}\otimes U^{*}=(A\otimes U)^{*}$, the block-swap argument of F328 §3.2 goes through **verbatim** with $A^+(\mathbf k)$ replaced by $A^+(\mathbf k)\otimes U$ throughout, since the off-diagonal mass terms are untouched isospin scalars. Verified over 300 random $(\mathbf k,m,U)$ samples to $6.7\times10^{-16}$ (leg B1) and at the five $\mathbf k=0$/axis/$|m|\in\{0,1\}$ edge cases to $3.1\times10^{-16}$ (leg B2, no small-$\mathbf k$ expansion anywhere), with $D'(\mathbf k)$ itself exactly unitary (leg B3).

**The Kramers signature flips.** F328's $\Theta$ satisfies $\Theta^2=-1$ because $M=\Sigma(\sigma_y\oplus\sigma_y)$ is a *real* matrix ($M^{*}=-M$ since $\sigma_y^{*}=-\sigma_y$ and $\Sigma$ is real), giving $\Theta^2=MM^{*}=-M^2=-\mathbb1$. Here $\sigma_y\otimes\tau_2$ is a Kronecker product of **two** purely-imaginary matrices, hence itself **real** ($(\sigma_y\otimes\tau_2)^{*}=(-\sigma_y)\otimes(-\tau_2)=\sigma_y\otimes\tau_2$), so $M'$ is real too, but now $M'^2=\mathbb1$ ($\Sigma_8^2=\mathbb1$, $(\sigma_y\otimes\tau_2)^2=\sigma_y^2\otimes\tau_2^2=\mathbb1$), giving $\Theta'^2=M'M'^{*}=M'^2=+\mathbb1$ — verified to literal `0.0` against $+\mathbb1$ (leg C1) and confirmed **not** $-1$ (residual $2.0$ against $-\mathbb1$, leg C1b). This is not a numerical curiosity: tensoring a **second** pseudoreal (spin-$\tfrac12$-like) twist onto the first flips the antiunitary involution class, the generic behaviour Wigner's classification predicts for composing two independent Kramers-type structures — the isospin doublet is "spin-$\tfrac12$-like" in exactly the representation-theoretic sense that makes this happen.

## 5. Companion no-go: the model's own SU(2)-gauged mass mechanism obstructs it

`covariant_dirac_doublet_step`'s actual mass term does not leave the doublet an isospin scalar — it mixes $\eta,\chi$ through a **second**, independent SU(2) link $V$ (the Stueckelberg-type mass-generation mechanism). Grafting this into `D_grafted` as $D''(\mathbf k)$ with off-diagonal blocks $im(\mathbb1_2\otimes V)$, $im(\mathbb1_2\otimes V^\dagger)$, and testing the **same** $\Theta'$:

$$\max\ \lVert\Theta' D''(\mathbf k)\Theta'^{-1}-D''(\mathbf k)^{-1}\rVert = 2.85\quad\text{(random }(\mathbf k,m,U,V),\text{ leg D2)} — \text{an }O(1)\text{ failure, for }V=U,\ V=U^\dagger,\text{ and independent }V\text{ alike.}$$

**This is not merely "not found" — it is a provable obstruction.** Working through the block algebra with a general fixed isospin operator $\Lambda$ in place of $\tau_2$ shows the off-diagonal (mass) block requires

$$\Lambda\, V^{T}\, \Lambda^{-1} = V \qquad\text{for every }V\in SU(2)$$

— a **transpose**, not the conjugate relation the kinetic block needed. The map $V\mapsto V^{T}$ is a group **anti-automorphism** ($(V_1V_2)^{T}=V_2^{T}V_1^{T}$); conjugation by any fixed $\Lambda$ is always an **automorphism**; the composition of an automorphism and the anti-automorphism $(\cdot)^T$ is itself an anti-automorphism. An anti-automorphism can equal the identity map only if the group is **abelian** (identity is trivially an automorphism, and $\phi=\text{id}$ being simultaneously anti-automorphic forces $V_1V_2=V_2V_1$ for all $V_1,V_2$). **SU(2) is not abelian, so no fixed $\Lambda$ satisfies this for every $V$** — a structural fact, not a search failure.

**Novelty scope, per the 2026-09-09 independent review:** no-go theorems for discrete symmetries (C, P, CP) on non-abelian lattice gauge fields are an established research area — e.g. the chiral-anomaly-driven obstructions surveyed for lattice chiral gauge theories (hep-lat/0302003) and the representation-dependent C/T transformation properties of non-abelian gauge bosons (arXiv:2212.08907, which studies precisely the "does $\Theta$ also transform the background field" question this finding's §6 leaves open). The mechanism here (conjugation-by-a-fixed-operator is always an automorphism; $V\mapsto V^{T}$ is always an anti-automorphism; the two coincide only on an abelian group) is an elementary consequence of standard SU(2) representation theory, not a citation of either of those results — this section's claim is novelty **to this project's tree**, not to the field.

Two checks support this without relying on the argument alone:
- $\tau_2$ satisfies a **related but different** true identity, $\tau_2 V^{T}\tau_2^{-1}=V^{-1}$ for every $V$ (verified to $4.7\times10^{-16}$, leg D1) — $\tau_2$ solves a neighbouring problem, not this one, ruling out "maybe a different fixed twist works" for the specific candidate that succeeded on the kinetic sector.
- A 500-sample Monte-Carlo search over **random Haar-unitary $2\times2$ operators** $\Lambda$ (not just $\mathbb1_2$ and $\tau_2$), tested against two fixed non-commuting SU(2) elements $V_1,V_2$ simultaneously, finds no $\Lambda$ driving both residuals below $0.28$ (leg D3) — consistent with the algebraic impossibility being generic rather than an artefact of the two analytic candidates tried.

## 6. Scope, stated narrowly — what remains open (do not overclaim)

**This is not a claim that the model's SU(2)$_L$ gauge theory violates CPT as a physical statement.** Every test above holds the classical gauge/mass link **fixed** under the antiunitary map — $\Theta$ is asked to map the walk at background $(U,V)$ to the *inverse* of the walk at the **same** $(U,V)$, the literal discrete analogue of how F328 tested $D(\mathbf k)$ against $D(\mathbf k)^{-1}$ at the same $m$. The continuum Lüders–Pauli argument for a real gauge theory instead lets $C,P,T$ **also** transform the gauge field itself (e.g. charge conjugation acting on the connection, not holding it pointwise fixed) — and this finding's own **positive** kinetic-sector result already needed exactly this kind of structure implicitly satisfied (the pseudoreality relation $\tau_2U\tau_2^{-1}=U^{*}$ is precisely "how $U$ transforms," not "$U$ held fixed while something else moves"). Whether letting $\Theta$ **also** map the mass background $V$ to some other $V'$ (rather than requiring the identity at the same $V$) restores a theorem for the mass sector is a different, more general question this finding does **not** attempt. Per [[CL285]]'s own falsifier text and ledger row A4r's own caution, promoting the §5 no-go to "the model's SU(2)$_L$ sector violates CPT" would need its own claim card and a named experimental confrontation — not done here, and not implied.

Separately unresolved: §3's cross-module branch-pairing mismatch (`covariant_dirac_doublet_step`'s branch $+/-$ vs. `dirac_bcc.py`'s branch $+$/dagger) is a pre-existing architectural inconsistency in the tree, independent of the CPT question, flagged but not fixed here.

So: ledger row A4r moves from *"the gauge-coupled extension is untested"* to *"the kinetic half of the gauge coupling has an exact CPT-type theorem via SU(2) pseudoreality (with a flipped Kramers signature); the mass-generation half has a genuine, general, provable obstruction to the same fixed-background ansatz, and whether a background-transforming $\Theta$ resolves it is the new, narrower residual."* Rubric row A4 stays **PARTIAL**.

## 7. Checks (11/11 PASS)

| Leg | Statement | Result |
|---|---|---|
| X0 | `D_covariant_doublet(k)` reproduces the real `covariant_dirac_doublet_step` output exactly, uniform link, grid-compatible $k$ | $1.2\times10^{-15}$ |
| E1 | the ACTUAL module fails F328's identity already at $U=V=\mathbb1$ (branch mismatch, not a coupling effect) | $1.96$ |
| A1 | $\tau_2 U\tau_2^{-1}=U^{*}$ for every $U\in SU(2)$ (300 samples) | `0.0` |
| B1 | $\Theta' D_\text{grafted}(\mathbf k)\Theta'^{-1}=D_\text{grafted}(\mathbf k)^{-1}$, kinetic-only, random $(\mathbf k,m,U)$ | $6.7\times10^{-16}$ |
| B2 | same, at $\mathbf k=0$/axis/$\lvert m\rvert\in\{0,1\}$ edge cases | $3.1\times10^{-16}$ |
| B3 | $D_\text{grafted}$ (kinetic-only) exactly unitary | $6.7\times10^{-16}$ |
| C1 | $\Theta'^2=+1$ (residual to $+\mathbb1$) | `0.0` |
| C1b | confirms $\Theta'^2\ne-1$ (residual to $-\mathbb1$) | $2.0$ |
| D1 | $\tau_2V^T\tau_2^{-1}=V^{-1}$ for every $V$ (a true, different identity) | $4.7\times10^{-16}$ |
| D2 | grafting an independent SU(2) mass link breaks $\Theta'$ at $O(1)$, random $(\mathbf k,m,U,V)$ | $2.85$ |
| D3 | 500-sample Monte-Carlo search over random unitary $2\times2$ $\Lambda$: none solves the mass-sector identity for two fixed non-commuting $V_1,V_2$ | $0.28$ |

**Control** (`use_naive_iso=true`, swaps $\tau_2\to\mathbb1_2$ in the kinetic-sector legs only): reddens B1 ($1.85$), B2 ($1.41$), C1 ($2.0$ — $\Theta^2$ reverts to F328's Kramers $-1$, so the "$+1$" assertion fails), and C1b ($0.0$ — confirming $\Theta^2$ really is $-1$ again, not the flipped class). X0, A1, B3, D1, D2, D3, E1 all stay green, confirming the reddened legs measure the $\tau_2$ twist specifically and not a bookkeeping tautology. **VERIFIED RED 2026-09-09.**

## 8. New exactness-inventory entries

- **Tier 1 (algebraic exact):** identity (III) $\tau_2U\tau_2^{-1}=U^{*}$ (A1); the kinetic-sector CPT operator identity $\Theta'D'(\mathbf k)\Theta'^{-1}=D'(\mathbf k)^{-1}$ at every sampled $(\mathbf k,m,U)$ and the edge cases (B1, B2); $\Theta'^2=+1$ (C1, C1b); the true identity $\tau_2V^T\tau_2^{-1}=V^{-1}$ (D1).
- **Tier 2 (machine precision):** cross-check of the closed form against the real module (X0, $1.2\times10^{-15}$); $D_\text{grafted}$ unitarity (B3, $6.7\times10^{-16}$).
- **Measured, not exact by construction:** E1's zero-coupling branch-mismatch residual ($1.96$); D2's gauged-mass no-go residual ($2.85$, generic across $V=U,V=U^\dagger$, independent $V$); D3's Monte-Carlo search floor ($0.28$ over 500 random $\Lambda$).
