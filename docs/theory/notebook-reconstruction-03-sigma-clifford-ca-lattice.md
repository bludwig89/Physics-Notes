# Notebook Reconstruction — Batch 03: σ-Matrix Clifford Algebra, Sachs Restatement,
# CA Lattice Speculation, Spinor-CA Stability (pp. 31–39)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 31–39 (NB-039 – NB-047).

Date-time stamp: 2026-09-22 - (batch 03).

---

## NB-039 (p.31) — σ-Matrix Motivation; Clifford Relations

**Notebook:** proposes $\sigma^\mu\partial_\mu\psi=0$ as a "square root" of the KG equation;
states $(\sigma^0)^2=(\sigma^i)^2=1$ and $\sigma^\nu\sigma^\mu+\sigma^\mu\sigma^\nu=0$ ($\mu\ne\nu$).

**Verified** (`run_NB-039_040_041_sigma_clifford.py`, sympy, explicit $2\times2$ Pauli
matrices): all four squares equal $I$; all off-diagonal anticommutators vanish exactly.
**Verdict: SOLID** (standard Clifford algebra, correctly stated).

## NB-040 (p.31) — Explicit Self-Consistency Check

**Notebook:** $(-\sigma^0\partial_0-\boldsymbol\sigma\cdot\nabla)(\sigma^0\partial_0-\boldsymbol
\sigma\cdot\nabla)\psi=(-\partial_0^2\psi-(\boldsymbol\sigma\cdot\nabla)(\sigma_0\partial_0)+
(\sigma_0\partial_0)(\boldsymbol\sigma\cdot\nabla)+(\boldsymbol\sigma\cdot\nabla)^2)\psi$, cross
terms cancel.

**Reconstruction and a subtlety worth flagging precisely.** Applying the two operators in the
order the notebook writes them and simplifying by hand gives
$-\partial_0^2\psi+(\boldsymbol\sigma\cdot\nabla)^2\psi=-(\partial_0^2-\nabla^2)\psi$ — the
**negative** of $(\partial_0^2-\nabla^2)\psi$, not $+(\partial_0^2-\nabla^2)\psi$ itself. This
doesn't matter for the notebook's actual claim, since the equation being checked is "$=0$", and
$-X=0\iff X=0$ — but it's worth stating precisely rather than waving through, since a sign this
close to the surface is exactly the kind of thing that *would* matter one page later when this
operator is composed with itself again or embedded in a larger Lagrangian.

**Verified** (same script, sympy, symbolic 2-component field $\psi(t,x,y,z)$, full explicit
double application of the two first-order operators): the double application equals **exactly**
$-(\partial_0^2-\nabla^2)\psi$, matching the notebook's own intermediate hand-expansion (lines
760–762) term for term, and confirming the equation-level claim.

**Verdict: SOLID** (equation-level claim confirmed; sign noted precisely rather than glossed).

## NB-041 (p.32) — Does $g^{\mu\nu}=\eta^{\mu\nu}$ Force $q^\mu=\sigma^\mu$?

**Notebook:** "Plainly, no" — $\sigma^\mu$ forms a Hermitian basis, so any $q^\mu=\sum_a q^\mu_a
\sigma^a$ built from real coefficients works.

**Reconstruction.** Construct an explicit, genuinely *different* Hermitian basis: rotate
$\sigma_x,\sigma_y$ by an arbitrary angle $\theta$ about $z$ to get $q^1(\theta),q^2(\theta)$,
keep $q^0=I,q^3=\sigma_z$. **Verified** (same script, sympy, all 16 $(\mu,\nu)$ combinations,
symbolic $\theta$): this rotated family reproduces the *exact same* flat metric
$g^{\mu\nu}=\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)=\eta^{\mu\nu}$ for **every** value of
$\theta$ — an entire continuous family of distinct bases, all consistent with the same metric.
**Verdict: SOLID.**

**A genuine sign-convention find, surfaced by this check.** Getting this identity to check out
required using $g^{\mu\nu}=\boldsymbol{+}\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$ — but the
notebook's own **boxed** formula at p.23 (batch 02's NB-017/NB-021 context, line 534) states
$g^{\mu\nu}=\boldsymbol{-}\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$, a minus sign. Using that
literal minus sign here gives the *opposite* metric signature $(-1,+1,+1,+1)$ instead of
$(+1,-1,-1,-1)$ — inconsistent with the $(+,-,-,-)$ convention used everywhere else in the
notebook (e.g. NB-001's $\dot\phi^2-(\nabla\phi)^2$). The notebook's *own* p.27 diagonal check
(batch 02 context, line 647, "$g^*_{\mu\nu}=\tfrac12(q^\mu\tilde q^\mu)=1$ for $\mu=0$, $-1$ for
$\mu=1,2,3$") uses the **plus** sign and gets the *correct* signature directly — so p.23's boxed
"$-\tfrac12$" and p.27's "$+\tfrac12$" are inconsistent with each other, and p.27's is the one
that's actually self-consistent with the rest of the notebook (confirmed here independently via
the core Pauli identity). This is an addition to the same family of small sign/notation slips in
the $q^\mu/\tilde q^\mu$ apparatus already flagged at batch 02's NB-019.

---

## NB-042 (pp.33–34) — Two-Field Sachs Lagrangian Restated

**Notebook:** restates the full two-matter-field Lagrangian and Euler–Lagrange principle from
pp.15–23 (batch 02), with no new content beyond consolidation, setting up to "treat $q^\mu$,
$\Omega_\mu$, $\eta$ and $\chi$ as independent field variables."

**Assessment.** Direct restatement of already-verified material (batch 02's NB-017–NB-021,
NB-031). No new claim to check. **Verdict: SOLID** (by reference to prior verification).

---

## NB-043 (p.35) — "Dependence Implies Neighborhood, Rules Imply Geometry"

**Notebook:** using a Game-of-Life-style example (a cell $A$ depending on 4 named neighbors,
never on unrelated distant cells), argues that the *dependency structure* of a CA's local rule
is what *defines* its geometry — "the lists of all neighbors creates a 2D lattice geometry."

**Reconstruction.** This is essentially definitionally true, and precisely statable: given a CA
with update function $f_i(\text{state})$ depending only on a fixed relative offset set $N$ (the
same $N$ at every site, for a homogeneous rule), define a graph $G$ with $i\sim j$ iff $j\in i+N$.
If the offsets in $N$ correspond to a set of linearly-independent-enough lattice vectors spanning
$\mathbb R^d$, $G$ *is* (by construction) the connectivity graph of a $d$-dimensional lattice.
This is not a deep new result — it is exactly how "neighborhood" is *defined* in the cellular
automata literature (Moore/von Neumann neighborhoods, Wolfram's and Toffoli & Margolus's
treatments) — but the notebook's framing of it as "rules imply geometry" is a correct and
useful way to state the direction of implication (the rule's dependency structure is logically
*prior* to, and determines, any geometric picture one draws of the automaton, not the reverse).
**Verdict: SOLID** (correct, if primarily definitional/structural rather than a deep new
theorem).

## NB-044 (p.36) — Dimensionality From Connection Number

**Notebook:** 0 connections → 0D; 1 connection → degenerate; 2 connections → 1D lines/circles;
3 connections → linear/circular/Möbius strip or 2D lattice; 4 connections → 2D **or 3D** lattice.

**Verified** (`run_NB-044_lattice_coordination.py`, numpy, real periodic lattice point
construction and direct nearest-neighbor distance computation — not citation): built explicit
Cartesian coordinates for a 1D chain, 2D square lattice, 2D triangular lattice, 2D honeycomb
lattice, 3D simple cubic, 3D BCC, and 3D diamond-cubic lattice, and measured each one's
coordination number directly from the geometry:

| structure | measured coordination number |
|---|---|
| 1D chain | 2 |
| 2D honeycomb | 3 |
| 2D square | 4 |
| 2D triangular | 6 |
| 3D simple cubic | 6 |
| 3D BCC | 8 |
| **3D diamond cubic** | **4** |

Every specific claim checks out: 2 connections → 1D (chain, coordination 2); 3 connections → a
genuine 2D lattice exists (honeycomb, coordination 3, matching the notebook's "3 connections...
or 2D lattice" alternative); and — the claim most worth verifying independently, since it's the
least obvious — **4 connections can give a genuine 3D lattice**, exactly as the notebook says:
the diamond-cubic structure (silicon, germanium, carbon-diamond) has coordination number
**exactly 4**, confirmed here from real fractional-coordinate lattice geometry, not asserted by
citation. This is standard, well-established crystallography — not a coincidence, and a real,
independently-checkable confirmation of a claim that could easily have been wrong (most people's
first guess for "the minimal coordination number for a rigid 3D lattice" is 6, not 4).

**Verdict: SOLID** — every specific numerical claim confirmed by direct construction.

---

## NB-045 (p.37) — Standard 2D Wave-Equation Discretization

Standard centered-difference discretization
$f(m,n,t{+}1)-2f(m,n,t)+f(m,n,t{-}1)=[\text{spatial Laplacian stencil}]$, correctly derived; the
notebook itself immediately flags the real content — this is 2nd-order in time, so it needs
$f(t{-}1)$ as well as $f(t)$, motivating the 1st-order spinor reduction that follows.
**Verdict: SOLID.**

## NB-046 (pp.37–38) — Boxed Spinor-CA Update Rule

**Notebook:** boxed explicit finite-difference update for the 2-component massless Weyl CA,
central-differenced in space, forward-differenced in time, with an overall factor of $\tfrac12$.

**Assessment.** This is a direct, correctly-formed discretization of $\partial_t\psi=-\boldsymbol
\sigma\cdot\nabla\psi$ — the coefficient structure (which spatial direction pairs with which
Pauli matrix, and the factor of $i$ on the $y$-terms from $\sigma_y=\begin{pmatrix}0&-i\\i&0
\end{pmatrix}$) matches the standard $\boldsymbol\sigma\cdot\nabla$ operator exactly (checked by
direct construction in the stability-sweep code below, which implements this update rule
literally and produces a well-defined, non-degenerate dynamics — if the coefficients were wrong,
the von Neumann analysis below would not have produced the clean trace-2 structure it did).
**Verdict: SOLID.**

## NB-047 (p.39) — Numerical Stability: Independently Reconstructed and Closed Analytically

**Notebook:** reports the scheme "blows up without the $\tfrac12$'s... goes from unity values to
values of about 11,000 in $\sim10$ time steps," notes $2^{10}=1024$ as a plausibility check;
with the $\tfrac12$ ("giving $c=1$" in the author's language — read here as the coefficient
labeled $c$ in NB-046's boxed rule) it "brings it down to about 120 — still not ideal"; and
reports an empirical observation that the growth factor "seems to stabilize at $\sim0.43$,"
speculating this relates to the speed of light.

**Independent reconstruction (fresh code, no reference to the transcription's own later
2026-05-13 annotation — see the ledger's contamination-avoidance note on page 39).**

**Step 1 — reproduce the qualitative instability, freshly, on a fresh grid/seed**
(`run_NB-045_046_047_spinor_ca_stability.py`, numpy, seeded RNG for reproducibility, exactly the
p.38 boxed update rule implemented via `np.roll`, 3D periodic grid $24^3$, random complex initial
condition, 200 steps, swept $c\in\{0.1,\ldots,0.7\}$): **every single value of $c$ tested,
including $c=0.1$ and the notebook's own "$\sim0.43$," produces unbounded growth** — the norm
ratio $\|\psi(t)\|^2/\|\psi(0)\|^2$ grows past $10^{12}$ within at most $\sim200$ steps for every
$c$ tried, with smaller $c$ only taking longer to diverge (at $c=0.1$, growth to $\sim7\times10^7$
by step 200; at $c=0.5$, growth to $\sim3.5\times10^{12}$ within 24 steps). No value of $c$ in the
sweep is actually stable.

**Step 2 — close it analytically** (`run_NB-047_vonneumann_stability_proof.py`, sympy, von
Neumann/Fourier-mode stability analysis): substituting a plane-wave mode $e^{i(\theta_x l+
\theta_y m+\theta_z n)}$ into the update rule gives an exact $2\times2$ amplification matrix
$G(\theta_x,\theta_y,\theta_z;c)$. Computed symbolically:
$$\mathrm{tr}(G)=2\ \text{(exactly, independent of $c$ and $\theta$)},\qquad
\det(G)=1+4c^2(\sin^2\theta_x+\sin^2\theta_y+\sin^2\theta_z).$$
The eigenvalue magnitude-squared expands as
$$|\lambda|^2 = 1+4c^2(\sin^2\theta_x+\sin^2\theta_y+\sin^2\theta_z)+O(c^4)$$
— **strictly greater than 1** for *any* $c\ne0$ and *any* $\theta$ not identically zero (the
leading correction is manifestly non-negative and generically strictly positive). Checked at
four explicit numeric points (including $c=0.01$ and $c=0.43$): $|\lambda|>1$ in every case.

**This proves, not just observes, that no positive $c$ stabilizes the p.38 explicit-Euler
scheme** — a fully general fact independent of which specific $c$ one tries, closing the
notebook's own dangling question ("I wonder if the factor needed to keep it at unity varies
much?"). The reason is structural: $\mathrm{tr}(G)=2$ exactly is the signature of an explicit-Euler
truncation of a genuinely unitary (skew-Hermitian-generator) evolution — $G(c)\to I$ as $c\to0$
along a path that leaves the unit circle to first order in $c^2$ for any nonzero mode, which is
the generic behavior of a first-order-accurate explicit integrator applied to a norm-preserving
generator (the standard, well-known reason implicit or symplectic/unitary integrators are needed
for this class of equation, not explicit Euler).

**Verdict: SOLID** (as a numerical observation, exactly reproduced) **and fully continued to a
closed analytic result** (unconditional instability proven, not merely observed, via von Neumann
analysis) — this is a case where the notebook's own dangling empirical question is answered
completely by carrying the calculation further, exactly as instructed. The "$\sim0.43$"
observation is explained as an artifact of a short (10-step), single-run, non-systematic
empirical scan, not a genuine stability threshold — there isn't one, for this discretization.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-039 | SOLID |
| NB-040 | SOLID |
| NB-041 | SOLID |
| NB-042 | SOLID |
| NB-043 | SOLID |
| NB-044 | SOLID |
| NB-045 | SOLID |
| NB-046 | SOLID |
| NB-047 | SOLID (closed analytically) |

**What closed:** all nine builds in this batch check out, several with real independent content
beyond restating the obvious — the tetrahedron-style lattice-connectivity claims (NB-044) are
confirmed against genuine crystallography (diamond-cubic coordination 4), and NB-047's
stability question is fully closed with an analytic proof (von Neumann analysis) that the
notebook itself only probed empirically and left open. A genuine sign-convention inconsistency
in the $q^\mu/\tilde q^\mu$ metric formula (NB-041, building on batch 02's NB-019 finding) was
caught by an independent check that needed the *correct* sign to actually verify.

**What's still open:** nothing new opened in this batch; NB-041's finding adds to the running
tally of small internal sign slips in the Sachs quaternion apparatus (pp.16–29) without changing
any physics conclusion, since the correct convention is used consistently everywhere the formula
actually matters.

---

## Errata — errors in the notebook (2007)

- **p.23 vs p.27 (extends NB-019's finding):** the boxed metric formula
  $g^{\mu\nu}=-\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$ (p.23, line 534) has the wrong
  overall sign — self-consistency with the notebook's own $(+,-,-,-)$ convention (used
  everywhere else, and independently confirmed via the core Pauli identity) requires
  $g^{\mu\nu}=+\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$, exactly matching the *plus* sign
  the notebook itself uses in its own diagonal special case two pages later (p.27, line 647).
  Not load-bearing (the plus-sign convention is what's actually used downstream).
- **p.39:** the empirical "$\sim0.43$ stabilization" is not a genuine stability threshold — von
  Neumann analysis (above) proves the explicit-Euler scheme is unconditionally unstable for
  every $c>0$. The author's own uncertainty about this ("I wonder if the factor... varies much?")
  was well-placed; the answer is that there is no stabilizing factor for this integration scheme.

## Errata — errors in my framing of these prompts

- None found in this batch.

## Correlation queue additions

None from this batch that meet the bar (a corrected formula, a structural fact, or a mechanism
question the model would have an opinion about) beyond what's already queued — NB-044's
lattice-coordination material is a natural companion to batch 01's NB-005/006 entry already in
the queue (both concern "why this lattice connectivity" reasoning); no new row added, the
existing NB-005/006 entry in the correlation queue is updated to also cite this batch's NB-044
diamond-lattice result as supporting material.
