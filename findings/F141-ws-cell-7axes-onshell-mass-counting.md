# F141 — The "7 bond axes" of F49 are the Wigner–Seitz facet axes of BCC (exact lemma), and the 2 : 7 assignment is an on-shell mass-counting statement: $m_W^2 : m_Z^2 = 7 : 9$

**Date:** 2026-06-11 - 21:30
**Status:** Partial — the geometric lemma (§2) and the on-shell reframing (§3) are exact and close two of the gaps named in F49; the condensate mass-counting derivation (§4) is a defined programme with its obstacles identified, not yet executed.
**Script:** `tests/findings/test_F141_ws_cell_mass_counting.py` (<5 s, stdlib only — integer/`fractions` arithmetic, no numpy/scipy; 11/11 PASS)
**Results:** `test-results/F141_ws_cell_mass_counting.json`
**Cross-references:** [[F49-bcc-finite-k-weinberg-angle]] (the 2 : 7 assignment this finding grounds), [[F51-bipartite-sublattice-hypercharge]] (the "2" — sublattice parity as the unique abelian carrier, already derived), [[F138-weinberg-gap-closure-4piv-matching]] (the scheme constraint: 2/9 must be on-shell, 1/4 is the UV cap at $\mu_\star=4\pi v$), [[F45-sigma-tau-swap-weinberg-angle]], [[F35-electroweak-mixing]] (W/Z mixing structure), [[F41-hypercharge-higgs-free-su2]], [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the Higgs-free condensate sector the §4 programme lives in).

---

## 1. Context: what was still open in F49 after F51 and F138

F49 produced $\sin^2\theta_W = 2/9$ from "2 sublattices : 7 bond axes" but listed the assignment itself as underived. Since then:

- **F51 derived the "2".** The sublattice parity $P=(-1)^{x+y+z}$ is the *unique* abelian charge commuting with the walk's $SU(2)$ given $s=2$ minimality — bipartiteness exact, conservation stroboscopic, Schur scalar, orthogonal to chirality. F49's first open bullet is closed.
- **F138 changed what the "7 : 2" can mean.** $\sin^2\theta_W = 1/4$ is the matching value at $\mu_\star = 4\pi v$ (forced by F41's missing $Y$ kinetic term), running down to $0.23173$ at $M_Z$. So **2/9 cannot be a bare coupling ratio** — that would contradict F138. F138 §5 sets the target: 2/9 must emerge as the **on-shell** value, i.e. as the physical mass ratio $m_Z/m_W = 3/\sqrt7$.

What remained: (a) why "first two shells" — the count 7 looked like a truncation choice; (b) why $SU(2)_L$ weights the 7 axes uniformly; (c) why coupling-squared (or now: mass-squared) adds one unit per structural channel. This finding settles (a) exactly, reframes (c) into a sharp condensate statement consistent with F138, and records (b)'s status.

---

## 2. Lemma (exact): 7 = the facet axes of the BCC Wigner–Seitz cell

F49 counted "unique bond axes to second shell" — leaving *why stop at the second shell?* unanswered. The answer is that the count is not a truncation at all:

> **Lemma.** The Voronoi-relevant vectors of the BCC lattice are exactly the $8+6=14$ first- and second-shell vectors; the Wigner–Seitz cell is the truncated octahedron with 14 facets — 8 hexagonal facets normal to the NN body diagonals and 6 square facets normal to the NNN face axes — and therefore exactly **7 facet-normal axes mod inversion**.

Proof structure (all exact, verified over $\mathbb{Z}$ and $\mathbb{Q}$ in V1/V2):

1. **Relevance criterion (integer-exact).** $v$ contributes a facet iff no lattice $w\notin\{0,v\}$ satisfies $\lvert w\rvert^2 \le w\cdot v$. Any violator obeys $\lvert w\rvert \le \lvert v\rvert$, so the check is a finite integer computation. Result: exactly the 14 vectors $(\pm1,\pm1,\pm1)$ and $(\pm2,0,0)$-perms are relevant; no ties (V1a, V1b).
2. **Rigorous closure (no window-dependence).** Every relevant $v$ has $v/2$ on the cell boundary, so $\lvert v\rvert^2 \le 4\mu^2$ where $\mu$ is the covering radius. The cell's 24 vertices (computed exactly by rational $3\times3$ solves; permutations of $(\pm1,\pm\tfrac12,0)$) give $\mu^2 = 5/4$ exactly, hence $\lvert v\rvert^2 \le 5$. The next BCC shell has $\lvert v\rvert^2 = 8 > 5$: nothing beyond the second shell can *ever* be relevant (V2a, V2c).
3. **Facet classification.** 8 hexagonal facets (6 vertices each) ⊥ body diagonals; 6 square facets (4 vertices) ⊥ face axes (V2b).

**Consequence.** The "7" of F49 is the complete set of facet axes of the lattice's Voronoi cell — the natural discrete gradient stencil, intrinsic to BCC with no shell-truncation choice. A gauge field whose lattice kinetic term lives on the WS-cell faces (the canonical discretisation: one flux per face) has exactly 7 independent axis channels, for the same reason a finite-volume scheme on BCC has 14 face fluxes. As context (not used in the argument): among the five Fedorov parallelohedra that tile 3-space by translations, facet counts range from 6 to 14, and the truncated octahedron realises the maximum — BCC is the most-connected case.

This was not recorded anywhere in the repo (checked: no mention of Wigner–Seitz/Voronoi/truncated octahedron in findings, docs, or papers before this).

---

## 3. The on-shell reframing (exact algebra): 2 : 7 is mass counting, $9 = 7 + 2$

Define the **equal-stiffness channel hypothesis**: the EWSB condensate contributes one universal stiffness quantum $u$ per structural channel — one per WS facet axis (7, charged/bond sector) and one per sublattice (2, abelian sector, F51). Then in SM notation $g^2 = 7u$, $g'^2 = 2u$, and (V3, exact over $\mathbb{Q}$):

$$\frac{m_W^2}{m_Z^2} = \frac{g^2}{g^2+g'^2} = \frac{7}{9}, \qquad \frac{m_Z}{m_W} = \frac{3}{\sqrt7}, \qquad \sin^2\theta_W^{\text{os}} \equiv 1-\frac{m_W^2}{m_Z^2} = \frac{2}{9}.$$

The arithmetic of F49's 2/9 is the observation that $9 = 7 + 2$: the Z draws stiffness from **all nine** structural units (7 axis + 2 sublattice channels), the W from the seven axis channels only. Three properties of this reading:

1. **It is scheme-correct under F138.** Masses, not running couplings, define the on-shell angle; F138 §5 demands exactly this. The two Weinberg values stop competing: $1/4$ = UV cap at $4\pi v$ (coupling statement, derived in F138), $2/9$ = on-shell endpoint (mass statement, this counting). The exact bridge $(2/9)/(1/4) = 8/9$ (V3c).
2. **It is sharper than F49's version.** F49 needed "why does $g'^2/g^2$ equal a count ratio" — a question about couplings at an unspecified scale, now known (F138) to be ill-posed. The mass version needs only: equal stiffness per channel **at the condensate scale**, in the scheme where masses are defined. RG running of couplings above/below that scale is irrelevant to the mass ratio.
3. **It is falsifiable to $6\times10^{-4}$ now.** $m_Z/m_W = 3/\sqrt7 = 1.133893$ vs PDG $91.1880/80.3692 = 1.134614$: residual $-0.063\%$ (V4a). If the counting derivation of §4 closes, this becomes an exact lattice prediction; the residual must then be accounted for by the W/Z width-definition and scheme conventions of the PDG on-shell masses, or the derivation is wrong.

---

## 4. The remaining derivation: condensate mass-counting (programme, not result)

What must be shown, in the model's own terms:

**Target.** The Higgs-free EWSB sector (F27/F41/F118) generates the vector-boson mass matrix. In the $(W^3, B)$ basis the SM-form matrix $\tfrac{v^2}{4}\begin{pmatrix} g^2 & -gg' \\ -gg' & g'^2\end{pmatrix}$ has the massless photon automatic; the claim $m_W^2 : m_Z^2 = 7:9$ is **equivalent** to $g^2 : g'^2 = 7 : 2$ *with a common normalisation quantum* $u$ at the mass-generation scale. So the entire remaining content is:

> **(U) Universality:** the condensate's quadratic response assigns the *same* stiffness $u$ to each of the 7 facet-axis channels of the $SU(2)_L$ link field and to each of the 2 sublattice channels of the F51 parity field.

Decomposition of (U) into three pieces, with status:

- **(U1) Equality across the 7 axis channels.** Cubic symmetry $O_h$ forces equality within the 4 body-diagonal axes and within the 3 face axes separately, but **not** 4-set = 3-set; that cross-set equality is the nontrivial part. Partially established: F49 Step 3 shows all 7 axes carry the same leading-order rotation rate $c_\text{lat}=1/\sqrt3$ (chirality-averaged) — the kinematic precondition. What's missing: the *condensate's* response (not the free dispersion) must inherit this equality, i.e. the F118 condensate must be even-channel and isotropic across both facet types at $O(k^0)$.
- **(U2) Equality between axis-quantum and sublattice-quantum.** This is the cross-normalisation between the non-abelian (Killing-form) and abelian sectors — historically the place such counting arguments fail. The model has one structural fact in its favour that the SM lacks: by F41/F138 the abelian channel has **no independent bare stiffness at all** (no $Y$ kinetic term); *all* of its stiffness is induced by the same matter sea on $U(x)$ that stiffens the link channels. One sea, one quantum, is the conjecture. The induced-kinetic-term lattice loop computation flagged as F138's own open item ("a lattice loop calculation of the $Y$ stiffness generated by the fermion sea on $U(x)$") is therefore the *same* computation needed here — closing F138's NDA gap and F141's (U2) in one stroke. That convergence of two open problems onto one calculation is the strongest reason to think the assignment is derivable.
- **(U3) Additivity (one generator per channel, quadrature sum).** Requires the 9 channel currents to couple to orthogonal field components with no cross terms at quadratic order. For the 7 axes this is facet-orthogonality of the WS fluxes (geometric); for axis–sublattice orthogonality it is F51 S3/S4 (the parity charge commutes with both spin and chirality — exact). Mostly in place; needs assembling into the quadratic form explicitly.

**Honest obstacles.** (i) In (U1), the condensate of F118 is the $E_g$ second-shell *lepton-mass* condensate; whether the same object (or the F27/F41 EWSB structure it completes) is what stiffens the vector bosons must be established, not assumed — the model currently has no explicit $m_W$ computation. (ii) The $-0.063\%$ residual: PDG on-shell masses include radiative/width conventions; "exact 3/√7" needs a statement about *which* mass definition (pole vs on-shell-scheme) the lattice counting lands on. (iii) If (U2) fails by a calculable factor (e.g. a Casimir or trace normalisation), the prediction moves off 2/9 entirely — that is the falsification channel.

**Next concrete step.** The induced-stiffness lattice loop: fermion sea on $U(x)$, one loop, computing the coefficient of $(\partial Y)^2$ (sublattice channel) and of the link-field kinetic/mass term (per facet axis), as exact lattice BZ integrals. Success criterion: ratio of induced quanta $= 1$ exactly (or a derived rational), simultaneously fixing F138's $\mu_\star$ (replacing NDA) and F141's (U2).

---

## 5. What this derives and what it does not

**Derived (this finding):**

- The count 7 is the WS-facet axis count of BCC — complete, not a shell truncation; closed rigorously by the covering-radius bound $4\mu^2 = 5 <$ 8 (next shell). Exact (V1, V2).
- The truncated-octahedron structure: 14 facets = 8 hexagonal (NN) + 6 square (NNN), 24 vertices, $\mu^2 = 5/4$. Exact (V2).
- The 2 : 7 assignment, *if* the equal-stiffness hypothesis (U) holds, is equivalent to $m_W^2:m_Z^2 = 7:9$, i.e. on-shell $\sin^2\theta_W = 2/9$ and $m_Z/m_W = 3/\sqrt7$ — the scheme F138 requires. Exact algebra (V3); PDG residuals $-0.063\%$ / $-0.44\%$ (V4).

**Not derived (the programme of §4):**

- (U1) condensate-level equality across the two facet types (kinematic precondition done in F49 Step 3).
- (U2) the axis↔sublattice cross-normalisation — reduces to the same induced-stiffness loop F138 left open.
- (U3) explicit quadratic-form assembly (ingredients exact in F51; not assembled).
- An explicit lattice $m_W$, $m_Z$ computation in the F118 sector.

---

## 6. Check summary (11/11)

| Check | Statement | Tier | Result |
|---|---|---|---|
| V1a–c | 14 relevant vectors (8 NN + 6 NNN), no ties, 7 axes mod inversion | exact (integer) | PASS |
| V2a–c | 24 vertices, $\mu^2=5/4$; 8 hexagons ⊥ NN + 6 squares ⊥ NNN; relevance closed by $4\mu^2=5<8$ | exact (rational) | PASS |
| V3a–c | $\sin^2\theta_W^{\text{os}}=2/9$, $m_W^2{:}m_Z^2=7{:}9$, $m_Z/m_W=3/\sqrt7$, bridge $8/9$ | exact (rational) | PASS |
| V4a–b | $3/\sqrt7$ vs PDG $m_Z/m_W$: $-0.063\%$; $2/9$ vs on-shell: $-0.44\%$ | numeric | PASS |

---

## 7. Files

- `findings/F141-ws-cell-7axes-onshell-mass-counting.md` — this finding
- `tests/findings/test_F141_ws_cell_mass_counting.py` — V1–V4 verification (stdlib-only, exact arithmetic)
- `test-results/F141_ws_cell_mass_counting.json` — full output
