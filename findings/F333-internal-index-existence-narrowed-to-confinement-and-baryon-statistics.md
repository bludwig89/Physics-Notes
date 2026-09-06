# F333 — Why the colour index has to exist at all, narrowed: not derived, but reduced from a bare fiat to two named observational facts — baryons are fermions, and quarks are confined

**Date:** 2026-08-28 - 21:22
**Numbering:** **F333**, taken as `NEXT FREE NUMBER` (max+1; no gap closed). Session `patient-lucid-noether`, sector `gauge`.
**Status:** Confirmed — **6/6 PASS** (≈2.4 s), **four** declared controls each verified red **and red only where declared** (`casim test --control --id F333-internal-index-existence`).
**Checked:** 2026-08-28 — 11 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED**
**Verdict:** Row **B1**'s last-standing residual — F324 §10 item 1's own words, *"the index exists by fiat"* — is **not derived from nothing**, and this finding does not claim otherwise. What moves is that the fiat is replaced by two small, named, extremely well-established observational facts (real baryons are fermions; quarks are never observed free) combined with the model's own SU(N) representation theory (genuinely generalised here, not just re-quoted) and its already-derived Fermi statistics (F289). The residual is renamed and shrunk again, in exactly the sense F317 and F318 both used that phrase for their own attacks on the same row.
**Modules:** `src/casim/engine/gauge/derive_internal_index_existence.py` (new)
**Test / results:** record `F333-internal-index-existence` (tier gate, entry `check_internal_index_existence`), driver `tests/findings/test_F333_internal_index_existence.py` → `test-results/F333_internal_index_existence.json`
**Cross-references:** [[F317-su3-structure-derived]] (§6, the fixed-k=3 precedent this finding's §1 generalises to a full (N,k) theorem), [[F318-cell-carries-the-internal-index]] (§D, the "cell does not force existence" verdict this finding narrows further), [[F324-ncolour-bracket-closed]] (§10 item 1, the residual verbatim; the {3,5,7,…} bracket this finding's §4 reproduces **independently**, from different premises, as a cross-check only), [[F289-spin-statistics-connection]] (derived Fermi statistics, imported not re-derived), [[F86-colour-dielectric-dual-superconductor]] / [[F110-realtime-link-hamiltonian-confinement]] (confinement, cited for motivation only — **not used as a premise**, precisely to avoid assuming $N=3$ already in order to derive $N>1$).

---

## 0. What this attacks, and what it does not

`docs/status/completeness-2026-08-20.md` row **B1** reads, after F317 and F318:

> one input: that the internal index exists | Reduced six-to-one by F317 (unitarity, specialness, locality⇒connection, vector-likeness); F318 shows the cell permits but does not force the index's existence

F318 §D found the forcing does not come from the cell — the cell is *indifferent* — but comes instead from the model's own derived Fermi statistics plus one further fact: *that the matter sector contains a three-constituent bound state*. F324, written after both, restates the same gap in its own §10 item 1 without moving it: *"Premise (ii) — the index exists by fiat. This finding needs colour to exist in order to count it."*

**This finding does not re-derive $N_c=3$.** That stays exactly where F317 §6 / F318 §D / F324 leave it — a genuine open question (row B10) this finding does not touch. What it attacks is narrower and is the literal target this row names: not *which* $N$, but whether $N>1$ at all, i.e. whether an internal index exists **as opposed to** the $N=1$ case, which is definitionally *no* internal index (a quark structurally identical, in this respect, to an ordinary lepton).

**Also not re-attacked:** any of F317's four closed legs (unitarity, specialness, locality⇒connection, vector-likeness), F27's chirality, or F291/F313's dimension counts.

---

## 1. The generalised constituent-count theorem

F317 §6 computed the dimension of the $SU(N)$-invariant subspace of $\Lambda^3(\mathbb C^N)$ for $N=2..6$ and found a singlet at exactly $N=3$, consuming "baryons have three constituents" as a fixed input. That result is a **single diagonal slice** ($k=3$) of a more general fact from $SU(N)$ representation theory: $\Lambda^k(\mathbb C^N)$, as a representation of the fundamental, is irreducible and non-trivial for $0<k<N$, and is the 1-dimensional determinant (trivial) representation exactly at $k=N$.

**S1, computed rather than quoted, and run as a genuine two-parameter scan.** Over the grid $N=1..6$, $k=1..4$ (wherever $N^k$ stays computationally small — the eigen/SVD route is the same joint-kernel construction F317 §6 used, generalised from three tensor factors to $k$):

$$\dim\big(\Lambda^k(\mathbb C^N)\big)^{SU(N)} = \begin{cases}1 & k=N\\0 & k\ne N\end{cases}$$

confirmed on **every** tested $(N,k)$ pair with $k\ge1$ — 24 pairs, 0 mismatches. This is standard mathematics (not claimed as new); what is new here is running it as a theorem about $(N,k)$ jointly rather than the single $k=3$ slice F317 needed for its own purpose. **Disclosed limitation:** the diagonal case $k=N$ is computationally verified this way only through $N=4$ (the committed grid caps $k\le4$ for cost — $N=5,6$ at $k=N$ dimension $3125$/$46656$ push past a single test-run's time budget); $N=5,6$'s own diagonal is not independently recomputed here and rests on the standard, uncomputed-in-this-finding fact that $\Lambda^N(\mathbb C^N)$ is always the 1-dimensional determinant representation for any $N$ (cited, not re-derived, in §"Prior art" below).

**Control.** `--param partial_generator_check=true` checks invariance under only the *first* generator of $\mathfrak{su}(N)$ instead of the full joint kernel. Several off-diagonal cells then acquire spurious "singlets" — e.g. $(N,k)=(4,2)$ goes from singlet dimension 0 to 2 — showing the "iff $k=N$" result genuinely depends on the full algebra, not a partial check. S1 alone goes red.

---

## 2. Composite exchange statistics, built and measured rather than quoted

**S2.** A composite made of $k$ identical spin-1/2 fermions is itself a fermion under particle exchange iff $k$ is odd — a standard fact (used, for instance, to say why $^3\mathrm{He}$ is a fermion and $^4\mathrm{He}$ a boson), verified here rather than invoked: the permutation exchanging two blocks of $k$ labelled identical particles (block swap $i\leftrightarrow i+k$ on $2k$ particles) is built explicitly and its signature computed with `sympy.combinatorics.Permutation.signature`:

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|
| measured sign | $-1$ | $+1$ | $-1$ | $+1$ | $-1$ | $+1$ |
| $(-1)^k$ | $-1$ | $+1$ | $-1$ | $+1$ | $-1$ | $+1$ |

Exact match at every $k$ tested. **Control.** `--param bosonic_baryon=true` forces the sign to $+1$ regardless of $k$ (the composite treated as if built from non-identical or bosonic constituents) — see §3's control, where this is the leg it reddens.

---

## 3. Hence: a quark-only colour-$N$ baryon is fermionic iff $N$ is odd

**S3.** Combine §1 and §2. A colour-singlet built from valence quarks *alone* (no antiquarks — the $\varepsilon$-tensor construction, the same one F317 §6 used) has, by §1, exactly $k=N$ constituents. By §2, that composite is a fermion iff $N$ is odd. Checked against the **observational** premise that real baryons — the model's own quark-only colour singlets, i.e. the proton and neutron — are observed fermions:

$$\text{predicted fermionic at } N=3:\ \text{yes (3 is odd)}\quad=\quad\text{observed fermionic: yes}$$

**This does not yet exclude $N=1$.** A lone free quark ($k=1$) is trivially odd and trivially a fermion — statistics alone is silent between $N=1$ and $N=3,5,7,\dots$.

**Controls, both on S3.** `--param n_probe=4` (an even colour count): the predicted 4-quark composite is bosonic, contradicting the observed fermionic baryon — S3 reddens, showing the oddness requirement is a real discriminator and not vacuously satisfied at every $N$. `--param bosonic_baryon=true` (constituents artificially made non-fermionic): S3 reddens **at $N=3$ too** — without fermionic valence quarks, nothing ever predicts a fermionic baryon at *any* colour count, which is what shows §2's fermion-specific sign, not group theory alone, is doing the work in §3.

---

## 4. Hence: $N=1$ is excluded by confinement, and the bracket

**S4.** $\dim\mathfrak{su}(N)=N^2-1$ (F317's own construction, reused). At $N=1$ this is **exactly zero** — literally no generators, hence no possible gauge boson, hence no possible confining force. A theory with $N=1$ "colour" is, in every operational sense, a theory with no colour at all. Checked against the **observational** premise that quarks are never seen as free, isolated particles — no fractionally-charged free particle has ever been detected, historically one of the two founding pieces of evidence for colour (the other being §3's Δ⁺⁺/Greenberg statistics argument):

$$N=3:\ \dim\mathfrak{su}(3)=8>0\quad\text{consistent with observed confinement}$$

**Control.** `--param n_probe=1`: $\dim\mathfrak{su}(1)=0$, so a gauge boson to confine *with* does not exist — S4 reddens, and this is the leg that actually excludes $N=1$; §3 alone (oddness) cannot, since $N=1$ is itself odd.

**S5, the bracket.** $\{N : N\text{ odd},\ N\ge2\}$ over $N=1..12$ is exactly

$$\{3,5,7,9,11\}.$$

**This matches F324's own independent post-S22 bracket** (`docs/design/session-claims.yaml`/F324 §"X1 RESOLVED": *"The bracket is now odd $N_c\ne1$: $\{3,5,7,\dots\}$"*) — reached there from entirely different premises (Witten's $SU(2)_L$ global anomaly, Bär–Wiese's generation-parity argument). **Recorded as a cross-check, not a dependency**: this finding does not use F324's premises, F324 does not use this finding's, and neither is needed to derive the other's bracket. **Honestly weighted, not oversold:** "odd and $\ge2$" is a fairly generic shape for a mod-2-type structural constraint to take, so two routes landing on it is a real but modest cross-check, not the striking coincidence a match on an arbitrary specific number would be. Neither pins $N=3$ within it, and this finding does not attempt to.

---

## 5. What this closes, and what remains

**Closes.** Nothing is *closed* in the sense of F317/F318's usage (a leg fully derived). What moves is the **shape** of the residual:

* **Before:** "the internal index exists" — F324's own words, "by fiat."
* **After:** two named observational facts — (a) real baryons are fermions, (b) quarks are confined (never observed free) — combined with (i) a genuinely generalised SU(N) representation-theory theorem (§1, not merely F317 §6's fixed slice) and (ii) an explicitly computed, not quoted, composite-statistics rule (§2) — together forcing $N$ odd and $N\ge2$, i.e. $N\ne1$: **an internal index must exist.**

**Remains, and is the honest headline.**

1. **(a) and (b) are not derived from anything more basic in this tree.** They are named, well-established observational facts about the real world (the existence of stable fermionic nuclear matter; the total absence, over decades of searches, of free fractional electric charge) — not measured numbers, and not re-derivable from the model's own dynamics as it stands. This is the same honest trade F324 §6 draws for its own six premises: "no measured number" is not "no empirical input."
2. **$N=3$ itself is untouched.** §5's bracket $\{3,5,7,9,11,\dots\}$ still needs F317 §6 / F318 §D's three-constituent input (or F324's own separate six-premise chain) to land on 3 rather than 5 or 7. This finding trades nothing against that residual and does not claim to.
3. **The confinement leg (S4) is deliberately not drawn from F86/F110's own confinement dynamics.** Using this model's confinement mechanism directly would risk circularity (F86/F110 are built at $N=3$ already); S4 instead rests on the model-independent fact $\dim\mathfrak{su}(1)=0$, which holds regardless of what $N$ turns out to be. This is a narrower and more defensible claim than "the model's confinement forces colour," and is stated as such rather than oversold.
4. **This does not address why the matter content is quarks-plus-leptons at all**, why leptons carry no such index, or any dynamical origin for confinement itself (that quarks *should* be confined, as opposed to the model's leptons, is read off observation here, not derived from the model's own Lagrangian).

---

## Reviewed & corrected

**2026-08-28 - 21:50** — attack pass (cold adversarial subagent, 13/13 attacks): **CONFIRMED**.
Found: two WEAKENS, neither structural. (1) §1's diagonal $k=N$ case is computationally verified
only through $N=4$ in the committed grid — $N=5,6$ ($\dim=3125$/$46656$) push past a safe
single-run time budget and were not included by default. (2) §4's cross-check against F324's
bracket was framed as more striking than it is — "odd and $\ge2$" is a fairly generic shape for a
mod-2 constraint, so two independent routes landing on it is real but modest, not a rare
coincidence. Fixed: both disclosed explicitly in §1 and §4 above, rather than expanding the
default grid (confirmed by hand that $(N,k)=(5,5)$ computes correctly and consistently with the
theorem — `has_singlet=True` — but at 23-46s depending on machine, which is not worth adding to
the gate-tier record's default runtime for a case standard representation theory already settles).
Rejected: none. Deferred: none — both fixes are complete as disclosure. All 13 attacks otherwise
PASS: not circular (S3/S4 compare a genuinely computed prediction against two named constants, and
the controls show the comparison is real); the two premises are logically independent and smaller
than F318's three-constituent input; `exactness: exact` on the module correctly describes the
arithmetic, with the claim card's `status: contingent` carrying the physical caveat; both
observational premises are current and correctly, carefully stated (routed through
$\dim\mathfrak{su}(1)=0$ rather than the tree's own confinement dynamics, precisely to avoid
circularity); no citation, scope, or supersession defects found; the underlying representation-
theory and composite-statistics facts are correctly identified as standard, with novelty claimed
only for the joint scan and the explicit computation; the N=1 special case in the code
(`su_n_generators(1)` returning an empty list) was verified necessary and correctly handled; the
logical structure — oddness alone excludes $N=2$, confinement alone excludes $N=1$ — was
independently re-verified and confirmed stated correctly, not muddled.

## 6. Falsifiers

1. **§1's theorem** fails if a genuine SU(N) singlet is found in $\Lambda^k(\mathbb C^N)$ for some tested $k\ne N$ — checkable independently in `sympy` (representation theory of the exterior powers of the fundamental is completely standard, so this is not expected to fail, but the grid is finite and stated as such).
2. **§2's parity rule** fails if a block-swap of $k$ labelled fermions is found with a sign other than $(-1)^k$ — a pure combinatorics statement, not expected to fail, included because this repo's culture is to compute rather than quote (F317/F318's own stated principle).
3. **§3 fails** if a genuinely stable, quark-only (no antiquark) hadronic bound state with an *even* number of valence constituents were ever observed as an isolated fermion, or if the proton/neutron were shown not to be fermions — neither is remotely on the table, but is the correct falsification target for the *physical content* (as opposed to the mathematics) of S3.
4. **§4 fails** if a consistent confining gauge theory were exhibited with a rank-0 (trivial) internal symmetry algebra — impossible by the definition of "gauge boson," which is why this leg is the least likely to move, and is closer to a definitional clarification than a physical risk.
5. **The whole finding is falsified as an argument for $N>1$**, without any of 1–4 failing individually, if either observational premise (baryons are fermions; quarks are confined) turned out false — which would be among the most significant discoveries in particle physics, not a plausible outcome, and is named as the honest dependency rather than hidden.

## Prior art

The Δ⁺⁺ problem (Greenberg 1964) and its statistics argument is the standard historical motivation for colour and is not claimed as new (F317 §6 already cites it; §3 here is the same argument run in the opposite logical direction — used to constrain $N$'s parity rather than to fix $N=3$ given a known multiplicity). The fact that confinement requires a non-trivial gauge connection is elementary once $\dim\mathfrak{su}(1)=0$ is stated; nothing here is new mathematics. What is new is: (i) running the constituent-count theorem as a genuine $(N,k)$ scan rather than the fixed-$k=3$ slice F317 needed, (ii) computing rather than quoting the composite-exchange-parity rule, and (iii) combining the two, plus the two named observational facts, into a derivation of $N\ne1$ that does not import $N=3$ anywhere along the way — and that happens to reproduce F324's bracket independently.

**Claim:** `docs/claims/CL287-internal-index-existence-narrowed-to-confinement-and-baryon-statistics.md` — `status: contingent`, rolls up to CL272. Names the two observational premises (baryons are fermions; quarks are confined) precisely, and does not itself move row B1's grade.
