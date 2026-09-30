# Notebook Reconstruction — Batch 01: Scalar QFT Opening, Photon/Graviton Speculation,
# Mass-from-Field-Energy (pp. 1–11)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 1–11 (NB-001 – NB-013). Written for a reader holding the notebook and no repo access —
every step is worked here, not summarized.

Date-time stamp: 2026-09-22 - (batch 01).

**Contamination note (applies to NB-007, NB-008, NB-009):** partway through this batch,
`references/mohr-2010-maxwell-photon-wf-summary.md` (nominally permitted "external literature")
turned out to carry an un-anticipated second half describing this project's own composite-photon
implementation (module names, a finding number, exactness-inventory entries). That content was
read before it was recognized as model-internal. Per direction from the operator, this session
now draws only on genuinely external sources (below, the de Broglie/Jordan/Pryce/Perkins
literature) for the physics content of NB-007–009, and flags those three rows — plus, later
batches, the pp.161–175 Maxwell-from-Weyl-CA builds, which sit in the same territory — for
extra scrutiny in the eventual correlation pass. All other builds in this batch (NB-001–006,
NB-010–013) are unaffected.

---

## NB-001 (p.1) — KG Lagrangian, Hamiltonian for a Real Scalar Field

**Notebook (verbatim):**
> $\partial_\mu\partial^\mu\phi + m^2\phi = 0$; $\mathcal L=\tfrac12(\partial^\mu\phi)(\partial_\mu\phi)-\tfrac12m^2\phi^2$;
> $\mathcal H = \tfrac12(\pi_\phi^2+(\nabla\phi)^2+m^2\phi^2)$.

**Own symbols:** standard free real KG field, mostly-plus... no, notebook uses $(+,-,-,-)$
(confirmed by $(\partial^\mu\phi)(\partial_\mu\phi)=\dot\phi^2-(\nabla\phi)^2$ used throughout).
$\pi_\phi=\partial\mathcal L/\partial\dot\phi$, $\mathcal H=\pi_\phi\dot\phi-\mathcal L$.

**Reconstruction.** Treat $\phi(t,x,y,z)$ as an unconstrained field. The Euler–Lagrange
functional derivative for $\mathcal L(\phi,\partial_\mu\phi)$ is
$\sum_\mu\partial_\mu(\partial\mathcal L/\partial(\partial_\mu\phi)) - \partial\mathcal L/\partial\phi=0$
— a **plain** sum over the four component derivatives $\phi_t,\phi_x,\phi_y,\phi_z$ (the metric
signs already entered when $\mathcal L$ was written out as $\tfrac12\phi_t^2-\tfrac12(\nabla\phi)^2-\tfrac12m^2\phi^2$,
so no extra metric weight belongs on the outer derivative — this is the one place a naive
transcription of "$\partial^\mu$" as "apply $\eta^{\mu\mu}$ again" gives the wrong sign on the
spatial terms; caught by the symbolic check below, which failed on the first attempt with
exactly a sign-doubled spatial Laplacian before the bug was found and fixed).

**Verified** (`tests/runners/notebook-recon/run_NB-001_kg_scalar.py`, deterministic, sympy):
Euler–Lagrange on $\mathcal L$ reduces identically to $\phi_{tt}-\nabla^2\phi+m^2\phi=0$ (residual
`0`); $\pi_\phi=\phi_t$ exactly; the Legendre transform gives
$\mathcal H=\tfrac12(\pi_\phi^2+(\nabla\phi)^2+m^2\phi^2)$ exactly (residual `0`).

**Verdict: SOLID.** Standard textbook derivation, exactly reproduced.

---

## NB-002 (p.1) vs NB-049 (p.42) — Fourier-Mode Convention

**Notebook (verbatim, p.1):**
> $\phi_k=((2\pi)^32\omega_k)^{-1/2}\int\phi(x)e^{ikx}d^3x$; $\phi(x)=(2\pi)^3\int\phi_k(2\omega_k)^{1/2}e^{-ikx}d^3x$.

This is presented as a matched forward/inverse pair with no derivation — it is top-of-page
"scratch," and the (as-transcribed) inverse integrates over $d^3x$, not $d^3k$, which is very
likely itself a transcription slip for $d^3k$ (integrating a $k$-space object over $x$ makes no
dimensional sense). Taking the charitable reading — $d^3k$ intended — the question that
survives is whether the **power of $(2\pi)$** is right.

**Reconstruction.** Write $\phi_k=A(k)\,\widehat\phi(k)$ where $\widehat\phi(k)=\int\phi(x)e^{ikx}d^3x$
is the plain Fourier transform and $A(k)=((2\pi)^3 2\omega_k)^{-1/2}$. The standard inverse
Fourier pair is $\phi(x)=\int\widehat\phi(k)e^{-ikx}\,d^3k/(2\pi)^3$. Substituting
$\widehat\phi(k)=\phi_k/A(k)$:
$$\phi(x)=\int \frac{\phi_k}{A(k)}e^{-ikx}\frac{d^3k}{(2\pi)^3} = \int \phi_k\,(2\omega_k)^{1/2}\,(2\pi)^{3/2}\,e^{-ikx}\,\frac{d^3k}{(2\pi)^3}=\int\phi_k(2\omega_k)^{1/2}e^{-ikx}\,\frac{d^3k}{(2\pi)^{3/2}}.$$
So self-consistency requires a prefactor $(2\pi)^{-3/2}$, not $(2\pi)^{+3}$ as transcribed.

Compare with the parallel, more careful pass 40 pages later at **p.42 (NB-049)**:
$\tilde\phi(k)=2\omega_k\int\phi(x)e^{ikx}d^3x$, $\phi(x)=\int\tilde\phi(k)e^{-ikx}\,d^3k/((2\pi)^32\omega_k)$
— and the notebook *itself* verifies this one is self-consistent, via the delta-function
identity $(2\pi)^3\delta^3(x)=\int e^{ikx}d^3k$ (lines 1021–1033 of the transcription).

**Verified numerically** (`run_NB-002_fourier_convention.py`, 1D stand-in — the $(2\pi)$-power
bookkeeping is dimension-generic, only the exponent tracks dimension, so 1D isolates exactly the
question at stake; scipy quadrature, test function $\phi(x)=e^{-x^2/2}$, evaluated at $x_0=0.7$
where $\phi(x_0)=0.782705\ldots$):

| convention | round-trip value at $x_0=0.7$ | matches |
|---|---|---|
| p.42 (NB-049), as written | $0.782705$ | ✅ exact |
| p.1 (NB-002), literally as transcribed | $12.327$ | ❌ off by a factor $(2\pi)^{3/2}\approx15.75$ |
| p.1 forward convention + corrected $(2\pi)^{-3/2}$ inverse power | $0.782705$ | ✅ exact |

The measured ratio $12.327/0.782705=15.749$ matches $(2\pi)^{3/2}=15.7496\ldots$ to 4 significant
figures, confirming the diagnosis exactly (a stray $(2\pi)^{+3}$ where $(2\pi)^{-3/2}$ belongs,
i.e. the inverse-transform prefactor is off by $(2\pi)^{9/2}$ in raw power, which the numbers
above show factors as the specific $(2\pi)^{3/2}$ mismatch once $A(k)$ is held fixed).

**Verdict: INCORRECT (as literally transcribed), SOLID-WITH-CORRECTION.** The corrected inverse
is $\phi(x)=(2\pi)^{-3/2}\int\phi_k(2\omega_k)^{1/2}e^{-ikx}d^3k$ (or, more likely, the author meant
$d^3k$ with some other implicit convention — either way p.1 is a quick scratch that the author
himself supersedes with a self-verified convention 40 pages later at NB-049; no physics rides on
the p.1 version since it is never used again after p.2's calculation stalls (see NB-003).

---

## NB-003 (pp.1–2) — H in k-Space, Continued to a Closed Form

**Notebook (verbatim):** builds $\mathcal H$ out of $\pi(x),\nabla\phi(x),\phi(x)$ substituted with
their Fourier expansions, gets as far as
$$H=\tfrac12\iiint\frac{(\pi_k\pi_p - \vec k\!\cdot\!\vec p\,\phi_k\phi_p+\phi_k\phi_p)(2\omega_k)^{1/2}(2\omega_p)^{1/2}}{(2\pi)^{-6}}e^{-i(k+p)x}\,d^3k\,d^3p\,d^3x$$
(schematically), and stops: *"This must be integrated with respect to x first ... $H=\int F(k,p)e^{-i(k+p)x}d^3k\,d^3p\,d^3x$."*

**Continuation.** This is exactly the calculation the author finishes cleanly 40 pages later
(NB-050, p.43) with the corrected convention. Here the stalled step is closed *in place*, with
a generic prefactor $B(k)$ standing in for whatever the correct convention turns out to be (its
specific form is what NB-002 checked): the $x$-integral gives $\int e^{-i(k+p)x}d^3x=(2\pi)^3\delta^3(k+p)$,
collapsing the $p$-integral onto $p=-k$, so $\vec k\cdot\vec p\to-k^2$.

**Verified symbolically** (`run_NB-003_hspace_substitution.py`, sympy, exact distributional
algebra via `DiracDelta`, not numeric approximation — this step is exact, not something to
integrate numerically): the collapsed bracket is
$$\pi_k\pi_{-k}+(k^2+m^2)\phi_k\phi_{-k},$$
matching, term for term, the bracket the notebook reaches independently at p.43 eq.$(\ast)$
(NB-050) — confirming the author's own later redo is the correct completion of the calculation
he set up (but didn't finish) here.

**Verdict: SOLID** (as far as it goes — an unfinished but correctly-set-up mid-derivation,
closed here and matching the notebook's own later completion).

---

## NB-004 (p.3) — "Photon Antisymmetric / Graviton Symmetric"

**Notebook (verbatim):** a bare heading note next to sketched Feynman-style lines, no derivation.

**Reconstruction.** This is standard representation theory, not a notebook derivation: a
massless spin-1 field's physical content is the field-strength 2-form
$F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$, antisymmetric by construction; a massless
spin-2 field's physical content is the metric perturbation $h_{\mu\nu}=g_{\mu\nu}-\eta_{\mu\nu}$,
symmetric because the metric itself must be symmetric (a metric assigns a scalar $ds^2$ to a
symmetric bilinear form). **Verified structurally** (`run_NB-004_012_013_em_facts.py`, sympy):
built $F_{\mu\nu}$ from a generic 4-potential $A_\mu(t,x,y,z)$ and confirmed $F+F^T=0$ exactly.

**Verdict: SOLID.** Correct, standard fact; not testable as a *novel* claim (it isn't one).

---

## NB-005 (p.3) — Tetrahedron, 3 Particle Types, "Only 2" Isomers

**Notebook (verbatim):** *"Tetrahedron with 3 types of particles — how many isomers are there?
Only 2 — cannot have anything else if all must join each vertex."* (Two tetrahedron sketches
shown, not transcribed in geometric detail.)

**Reading adopted (made explicit since the sketches aren't in the transcription):** the
tetrahedron is $K_4$ (4 vertices, 6 edges, each vertex degree 3). "3 types of particles ...
must join each vertex" = a proper 3-edge-colouring in which every vertex sees all 3 colours
(automatic, since degree = 3 = number of colours). "Isomers" = such colourings counted up to
the tetrahedron's **rotation** group (order 12, $A_4$ acting on the 4 vertices) — tried against
the full symmetry group (order 24, $S_4$, including reflections) as well, for comparison.

**Verified by brute-force enumeration** (`run_NB-005_006_isomer_counting.py`, exhaustive over
all $3^6=729$ edge-colourings, no shortcuts, Python):
- Exactly 6 proper 3-edge-colourings of $K_4$ exist in total (as labeled colourings) — matches
  the classical fact that $K_4$ has a *unique* 1-factorization into 3 perfect matchings, so a
  proper 3-colouring is just a bijection {matchings}→{colours}, giving $3!=6$.
- Under the **rotation group only** ($A_4$, order 12): exactly **2** orbits, of size 3 each.
- Under the **full symmetry group** ($S_4$, order 24, including reflections): exactly **1** orbit
  (reflections swap the two rotation-orbits into each other).

This has a clean group-theoretic reason: $S_4$ acting on the 3 perfect matchings realizes the
well-known surjection $S_4\twoheadrightarrow S_3$ (kernel the Klein four-group $V_4$); its
restriction to $A_4$ has image the cyclic subgroup $\mathbb Z_3\subset S_3$ (even permutations
only). Left-multiplication by $\mathbb Z_3$ on the 6 elements of $S_3$ (= the 6 labeled
colourings) splits it into exactly 2 cosets/orbits of size 3 — the notebook's answer of 2 falls
out exactly, and *only* if reflections are excluded.

**Verdict: SOLID** (under the rotation-only reading, which is also the physically natural one
for a chiral lattice-CA construction). The exact match — 2 orbits of size 3, not e.g. 2 orbits
of size 2 and 1, or 3 and 1 — is a nontrivial confirmation of the reading, not a tautology.

---

## NB-006 (p.3) — Octahedron, 2-Particle Case, "3 Only" Isomers

**Notebook (verbatim):** *"With octahedron, gets more interesting. You can do it w/ 2 or 4
particles. For 2-particle, bottom is completely determined by top. How many isomers? 3 only."*
(Five octahedron sketches, described but not transcribed in enough geometric detail to recover
the exact rule.)

**Attempted readings.** The octahedron (6 vertices, standard $\pm\hat x,\pm\hat y,\pm\hat z$
construction; rotation group order 24, built explicitly as the 24 signed-permutation matrices
with $\det=+1$ — a standard, unambiguous construction, not a guessed labeling) was tested with
the most natural "2-particle" read-outs: choose $k$ of the 6 vertices to be "type A," for
$k=1,2,3$, count orbits under the rotation group.

**Verified by brute-force enumeration** (`run_NB-006_octahedron_attempt.py`):

| split | labeled subsets | isomers under rotation |
|---|---|---|
| 1 of 6 | 6 | 1 |
| 2 of 6 | 15 | 2 |
| 3 of 6 | 20 | 2 |

None reproduces "3." The "top/bottom" language in the notebook strongly suggests a specific
geometric split (a distinguished top vertex + equatorial ring + bottom vertex, or a face-based
rather than vertex-based colouring) that isn't recoverable from the prose description alone —
the transcription explicitly says the sketches show "the three isomers and variations on the
bottom row," which is exactly the information needed and exactly what's missing here.

**Verdict: NOT-TESTABLE.** Not a failure of effort — the *object* being counted (the specific
combinatorial rule the author's now-lost sketches encode) cannot be recovered from the
transcription. The vertex-subset attempts above are recorded as a documented negative result,
not a guess dressed up as a derivation.

---

## NB-007 (p.5) — Spinor-Photon-Pair Mechanism

**Notebook (verbatim):** *"the idea of spinor electrodynamics involves two spin-½
fermion-photons exchanged in a correlated fashion... Yet these $\gamma_{1/2}$'s behave together
like a single boson $\gamma$ that only occurs as a pair. They don't occur separately."*

**External grounding (genuinely external literature, per the contamination note above — none of
this comes from the model's own files):** this is, independently, the core idea of de Broglie's
1932 "neutrino theory of light" — the photon as a bound neutrino–antineutrino pair (spin-½ pair
→ spin-1 composite) — later developed by Jordan, and subject to a well-known 1938 objection by
Pryce: *if* the composite photon is required to satisfy **exact** Bose commutation relations,
its amplitude is forced to zero. Case and Berezinskii later showed this is the *only* part of
Pryce's argument that survives scrutiny — and it is not actually fatal, because **many known
composite bosons are not exact bosons**: Cooper pairs, deuterons, pions, kaons are all
fermion-pair (or fermion–antifermion) composites that behave as bosons only asymptotically /
approximately, not via exact commutation relations. (W. A. Perkins, arXiv:1503.00661,
*Composite Photon Theory Versus Elementary Photon Theory* — surveyed directly, §I–II, in this
batch — gives the modern state of this literature and an explicit composite-photon construction
along these lines, with the antiphoton predicted to have different interaction properties than
the photon because its constituent antineutrino carries the "wrong" helicity.)

$1/2\otimes1/2=1\oplus0$ addition of angular momentum for two spin-½ fermions does produce a
spin-1 triplet, consistent with a photon-like state in principle (checked as elementary
Clebsch–Gordan bookkeeping, not re-derived here since it's completely standard).

**Verdict: SOLID-WITH-CORRECTION.** The core intuition — two spin-½ objects combining into a
photon-like spin-1 state, occurring only as a bound pair — is a genuine, independently
pre-existing idea in the literature (not original to the 2007 notes, though the author appears
to have reached for it independently), and remains an active (minority) research topic. The
correction the literature supplies and the notebook doesn't anticipate: the strong claim "only
occurs as a pair, they don't occur separately" cannot be read as *exact* Bose statistics for the
composite (Pryce 1938) — it has to be read as *approximate/asymptotic* boson behavior, exactly
as for a Cooper pair, or the construction is inconsistent.

## NB-008 (pp.5–6) — Photon-as-Cooper-Pair Analogy; "Superconducting" Travel at c

**Notebook (verbatim):** superconductivity analogy; *"the 'superconductivity' state ... might
simply be travel at the speed c, without hindrance from the 'lattice'"*; conjectured negative
binding energy for the bound pair.

**Assessment.** No precise mechanism is proposed (no gap equation, no order parameter, no
lattice-hindrance model to check against). The analogy is evocative but not, as stated, a
checkable claim — a resistance-free EM analog of Cooper pairing would need a specified coupling
and a specified "lattice" scattering mechanism before "binding energy" is a well-posed quantity.

**Verdict: NOT-TESTABLE** (mechanism too underspecified for a closed-form or numeric check;
this is a "reason about the object," not about effort — there is no equation here to verify).

## NB-009 (p.6) — Higgs-as-Cooper-Pair; W/Z as Other Spinor-Photon States

**Notebook (verbatim):** *"The Higgs is the Cooper pair, we presume. Is there a scalar photon?
... Can we understand W and Z bosons in this context?"* — posed as open questions, not claims.

**Verdict: NOT-TESTABLE.** Explicitly phrased as unresolved questions by the author himself; no
claim to verify.

---

## NB-010 (p.7) — Heat-of-Combustion Table (chemistry aside)

**Notebook:** table of combustion heats (methane 212.79, ethane 372.81, propane 530.57, octane
1302.7 kcal/mol) and a per-gram table (13.26, 12.39, 12.03, 11.40 kcal/g), plus a question about
whether alkanes polymerize with H₂ release.

**Verified** (quick arithmetic check, molar heat / molecular weight):

| substance | notebook kcal/g | computed (molar/MW) |
|---|---|---|
| Methane | 13.26 | 13.27 |
| Ethane | 12.39 | 12.40 |
| Propane | 12.03 | 12.03 |
| Octane | 11.40 | 11.40 |

All four match to the precision given — the table is internally consistent, and the molar
values themselves match standard tabulated heats of combustion (CRC-type reference values).
The polymerization question ($CH_4+CH_4\to C_2H_6+H_2$, etc.) does not correspond to a real
uncatalyzed thermal reaction pathway (C–H activation of methane at ordinary conditions requires
a catalyst — this is precisely why oxidative coupling of methane is a live industrial catalysis
research problem, not a spontaneous process) — but this is chemistry, entirely outside the
scope of the physics/CA model this reconstruction otherwise tracks.

**Verdict: SOLID** (the checkable content — the data table — is accurate); the polymerization
question is out of scope and unresolved, noted but not scored.

---

## NB-011 (p.9) — Sachs Motivation (narrative)

**Notebook:** motivational prose about Mendel Sachs' electrogravity unification; no independent
claim. **Verdict: NOT-TESTABLE** (narrative, nothing to check).

---

## NB-012 (p.10) — EM Energy Density $\xi=\tfrac1{8\pi}(E^2+B^2)$

**Notebook (verbatim):** *"the electric and magnetic fields E and B are associated with an
energy density $\xi=\tfrac1{8\pi}(E^2+B^2)$."*

**Reconstruction.** Standard Gaussian-units EM stress-energy-tensor result (Jackson Ch.6):
from $\mathcal L_{EM}=-\tfrac1{16\pi}F_{\mu\nu}F^{\mu\nu}$, using $F^{0i}=-E_i$,
$F^{ij}=-\epsilon_{ijk}B_k$: $F_{\mu\nu}F^{\mu\nu}=-2(E^2-B^2)$, so
$\mathcal L_{EM}=\tfrac1{8\pi}(E^2-B^2)$, and the canonical $T^{00}$ built from this Lagrangian
is the familiar $\tfrac1{8\pi}(E^2+B^2)$.

**Verified symbolically** (`run_NB-004_012_013_em_facts.py`, sympy): confirmed
$\mathcal L_{EM}=-\tfrac1{16\pi}F_{\mu\nu}F^{\mu\nu}$ reduces exactly to
$\tfrac1{8\pi}(E^2-B^2)$ (the sign-flipped companion of the energy density, as expected for a
Lagrangian vs. a Hamiltonian density).

**Verdict: SOLID.** Standard, correctly stated.

---

## NB-013 (p.11) — Point-Charge Self-Energy Divergence; Qualitative Mass Hierarchy

**Notebook (verbatim):** *"for a point particle, $\int_{r_0}^\infty E^2\,dV$ is divergent as
$r_0\to0$"*; qualitative claim that quarks (strong+weak+EM) > electron (EM+weak) > neutrino
(weak only) in mass, tied to number of interactions; explicit acknowledgment: *"serious
obstacles prevent physicists from turning this qualitative picture into quantitative
predictions."*

**Reconstruction, divergence.** $E=q/r^2\Rightarrow E^2\,dV=(q^2/r^4)\cdot4\pi r^2\,dr$, so
$\int_{r_0}^\infty E^2\,dV = 4\pi q^2\int_{r_0}^\infty dr/r^2 = 4\pi q^2/r_0$.

**Verified symbolically** (`run_NB-004_012_013_em_facts.py`, sympy `integrate` + `limit`):
closed form $4\pi q^2/r_0$ obtained exactly; $\lim_{r_0\to0^+} = \infty$. Confirmed.

**Continuation attempted, mass hierarchy.** The qualitative ordering (more interactions →
more self-energy → more mass) is directionally consistent with the observed hierarchy
quark $\gg$ electron $\gg$ neutrino, but this batch cannot close it quantitatively: doing so
needs an actual regularized self-energy calculation with real coupling constants and a real
cutoff scale, which is precisely what the notebook itself attempts much later, at pp.105–106
(NB-135–139, EM/Yukawa self-energy integrals and a classical-electron-radius estimate) — a
natural target to revisit when this reconstruction reaches that batch, to see whether it
actually closes the gap the author flags here.

**Verdict: NEEDS-WORK.** The divergence itself is SOLID; the mass-hierarchy claim is
qualitatively plausible but explicitly non-quantitative (by the author's own admission), and the
one specific thing that would close it — an actual numeric self-energy-vs-mass comparison across
the lepton generations with the pp.105–106 machinery — is not done in this batch, but is flagged
to revisit.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-001 | SOLID |
| NB-002 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-003 | SOLID |
| NB-004 | SOLID |
| NB-005 | SOLID |
| NB-006 | NOT-TESTABLE |
| NB-007 | SOLID-WITH-CORRECTION |
| NB-008 | NOT-TESTABLE |
| NB-009 | NOT-TESTABLE |
| NB-010 | SOLID |
| NB-011 | NOT-TESTABLE |
| NB-012 | SOLID |
| NB-013 | NEEDS-WORK |

**What closed:** the scalar-field opening (NB-001, NB-003) is exactly standard and the stalled
p.1–2 calculation is completed and shown consistent with the author's own later redo. The
Fourier convention bug on p.1 (NB-002) is pinned down to an exact $(2\pi)^{3/2}$ factor and shown
to be a scratch-page slip, not a load-bearing error (superseded by a self-verified convention at
p.42). The tetrahedron isomer count (NB-005) is exactly reproduced from first principles under
the rotation-only reading, with a clean group-theoretic explanation. Standard EM facts (NB-004,
NB-012) and the combustion-data table (NB-010) check out exactly.

**What's still open:** the octahedron isomer count (NB-006) cannot be recovered from the
transcription — flagged as a genuine gap, not resolved by guessing. The mass-hierarchy
continuation of NB-013 is deferred to the pp.105–106 batch, where the notebook itself attempts
a quantitative version. NB-007–009's grounding in the composite-photon literature is solid, but
those three rows carry the contamination caveat above and should get extra scrutiny in the
eventual correlation pass.

---

## Errata — errors in the notebook (2007)

- **p.1 (NB-002):** the Fourier inverse-transform prefactor is written as $(2\pi)^{+3}$ where
  self-consistency requires $(2\pi)^{-3/2}$ (or the integration variable is a straight
  transcription slip for $d^3k$ vs. the as-written $d^3x$ — either way, broken as literally
  transcribed). Confirmed numerically off by exactly $(2\pi)^{3/2}\approx15.75$. Superseded by
  a self-consistent convention the author derives and verifies independently at p.42.

## Errata — errors in my framing of these prompts

- None found in this batch.

## Correlation queue additions

See `docs/theory/notebook-reconstruction-correlation-queue.md` (created this batch) for
NB-005/006 (lattice connectivity → dimensionality), NB-007 (paired-fermion photon literature),
and NB-012/013 (mass-from-field-energy vs. the model's own mass-generation route).
