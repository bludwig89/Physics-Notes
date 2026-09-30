# Notebook Reconstruction — Correlation Queue

Handoff artifact for the later correlation pass (run by the operator, not this session — see
the governing prompt's firewall). One row per item: what this cold reconstruction established,
the specific question to put to the model, and why it matters. **These questions are not
answered here.** No entry is softened because the model might disagree with it.

Created: 2026-09-22 (batch 01). Updated every batch. Last updated: 2026-09-22 — the cold
reconstruction is now complete (batches 01–14 plus the contamination-deferred subagent pass, see
`docs/theory/notebook-reconstruction-index.md`'s Next-steps section); no further rows were added
by batches 11–14 or the subagent pass (each explicitly recorded finding nothing new meeting this
queue's bar — see those write-ups' own "Correlation queue additions" sections). This file is now
handed off in full to the operator's own correlation pass.

---

| NB-ID(s) | What the reconstruction established | Question for the model | Why it matters |
|---|---|---|---|
| NB-005, NB-006, NB-044 | Tetrahedron (4-vertex, degree-3) "3-particle-type, must join each vertex" isomer count is exactly 2 under the rotation group only (verified by brute-force group-orbit enumeration, clean $S_4\to S_3$ quotient explanation). Octahedron 2-particle case claimed "3" could not be reconstructed from the transcription — no vertex-subset reading (k=1,2,3 of 6) reproduces 3. Separately (batch 03, p.36), the notebook's "dimensionality from connection number" claim that **4 connections can give a genuine 3D lattice** is confirmed against real crystallography: the diamond-cubic structure has coordination number exactly 4 (verified from real fractional-coordinate lattice geometry, not citation). | Does the model's lattice choice (BCC base layer, coordination number, `casim.engine.lattice.bcc`) have any structural relationship to vertex/edge coordination-number combinatorics like this — i.e. did anything resembling this 2007 tetrahedron/octahedron isomer-counting or connection-number reasoning play any role in arriving at the model's current lattice geometry (BCC has coordination number 8, not 4 — was a lower-coordination lattice like diamond-cubic ever considered and rejected, and if so why), or is the resemblance (if any) coincidental? | CLAUDE.md's Decision D1 treats the lattice geometry (BCC vs. simple-cubic) as a specific, deliberate choice; this 2007 material is the notebook's earliest attempt to reason about which lattice connectivity is even possible, from pure combinatorics/crystallography rather than physics output (dispersion, isotropy, etc.). |
| NB-007 | The "two spin-½ $\gamma_{1/2}$ that only occur as a pair, forming a single boson $\gamma$" idea (pp.5) is independently the same structural idea as de Broglie's 1932 neutrino-theory-of-light / the modern composite-photon literature (Jordan, Pryce 1938, Case, Berezinskii, W.A. Perkins arXiv:1503.00661). The correction the literature supplies: exact Bose commutation for the composite is impossible (Pryce), so any such construction must rely on approximate/asymptotic boson behavior, as with a Cooper pair, deuteron, pion, or kaon. | CLAUDE.md states the model's photon is "the paired-spinor photon — a bound pair of two spin-½ Weyl quanta... 'only occurs as a pair.'" Does the model's construction address the Pryce 1938 exact-vs-approximate-Bose-statistics distinction explicitly, or does it sidestep it structurally (e.g. by not requiring exact bosonic commutators in the first place)? Is the model's paired-spinor photon aware of, or independently convergent with, the de Broglie/Jordan/Perkins literature line? | This is the single clearest point of contact between the 2007 notebook and a named, current model decision (decision 5 in CLAUDE.md). It is also the exact point (Pryce's objection) where the *historical* version of this idea was shown to be non-trivial — worth knowing whether the model's version inherits, resolves, or was never exposed to that constraint. |
| NB-012, NB-013 | EM field self-energy $\xi=(8\pi)^{-1}(E^2+B^2)$ and its divergence as $r_0\to0$ are standard and correctly used by the notebook to motivate "mass from field energy" as a research direction (pp.10–11), explicitly flagged by the author as *not yet quantitative*. | CLAUDE.md decision 3 states hypercharge is put on $U(x)$ specifically "avoiding any need for the Higgs field," and decision 7 gives a specific weight-as-phase mechanism for the charged-lepton mass *shape* ($\delta^*=2/9$). Does the model's mass-generation mechanism have any residual connection to a divergent-self-energy / field-energy picture at all, or has it moved to a completely different (representation-weight / geometric) origin story with no contact with this 2007 starting point? | Establishes whether the notebook's very first mass-generation idea (2007) is a genuine ancestor of the model's current approach, or whether the model's mass mechanism arose from an unrelated line of reasoning that happens to land on a different answer to the same "why do the leptons have different masses" question. |
| NB-037 | pp.28–29's variation of the Sachs electrogravity Lagrangian w.r.t. the spin connection $\Omega_{\rho,\nu}$ gives a nonzero result, $\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}=-\tfrac i2\eta^+q^\rho\eta$, which the author flags as disagreeing with "Sachs gets 0 on the LHS." This reconstruction identifies the discrepancy's likely resolution as structurally matching Einstein–Cartan–Sciama–Kibble (ECSK) theory: first-order gravity with independently-varied connection + spinor matter generically produces algebraic torsion sourced by the matter spin current, rather than the vacuum/bosonic-matter zero. Not closed to an exact term-by-term match. | Does the model's gravity sector (`casim.engine.interactions.gravity*`) work in a torsion-free formulation throughout (per CLAUDE.md decision 4's "induced Einstein equation" / dielectric-$K$ picture, this looks torsion-free), or does spinor spin-current ever source a connection/torsion-like term anywhere in the model? If torsion-free throughout, does the model ever address why the torsion this 2007 notebook derives from spinor matter should vanish (a symmetric-stress-only assumption, a specific gauge choice, or something else)? | This is a case where the notebook's own 2007 self-doubt ("not good!") may have been premature — the discrepancy looks like a real physical effect (ECSK torsion-from-spin) rather than an error, which is exactly the kind of situation where knowing the model's stance would clarify whether it inherited, independently avoided, or never encountered this issue. |
| NB-133, NB-134 | p.104's idle "what if the charged-current coupling to $W^\pm$ is exactly $3e$?" hypothesis leads, via $\sqrt2/\sin\theta_W=3$, to $\sin^2\theta_W=2/9$ exactly — confirmed (batch 10) to be correct algebra given that starting hypothesis. The notebook itself treats this as unmotivated numerology ("is there any significance to this?") and its own very next calculation (NB-134, the $Q_z$ matrix and a follow-up self-consistency check) fails on its own terms (a self-flagged ✗, confirmed genuine by this reconstruction — $11/6+6/11=157/66\ne7/3$), so the notebook does not treat $2/9$ as a settled result here. | The governing prompt's own decision 7 states the model's charged-lepton condensate angle $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=2/9$ rad is a "founding principle," described as primary and load-bearing, derived from $O_h$ representation-weight/Schur-isotropy arguments with no free shape parameters. Is there any relationship — historical, structural, or purely coincidental — between this 2007 marginal weak-mixing-angle numerology (a guessed exact coupling ratio, $\sin^2\theta_W=2/9$) and the model's later, completely differently-derived $\delta^*=2/9$ representation-weight angle? Or are these two appearances of "$2/9$" in entirely unrelated contexts (an electroweak mixing angle vs. a lattice representation-theory angle) that happen to share a value with no common origin at all? | This is the clearest *numerical* (as opposed to structural) coincidence this reconstruction has found between the 2007 notebook and a named, "primary"/load-bearing model decision. It is flagged with the caveats stated plainly: the two derivations share no identifiable route, arise from unrelated physical hypotheses (a coupling-strength guess vs. a group-representation weight), and the notebook's own instance is self-undermined by its own arithmetic on the same page — so the honest answer may well be "coincidence," but the correlation queue's standing rule is to ask rather than pre-judge. |
| NB-128, NB-129 | p.101's one-line margin note "if $\psi_+=E+iB$," attached to a "3D Dirac equation" $\partial_t\psi_\pm=\mp c\,\mathbf S\cdot\nabla\psi_\pm$ built from real spin-1 angular-momentum generators, is confirmed (batch 09) to be an exactly correct, independently verifiable statement of the classical Riemann–Silberstein-vector construction: $\mathbf F=\mathbf E+i\mathbf B$ satisfies exactly this type of first-order evolution equation (built from the Cartesian $L{=}1$ generators, where $\mathbf S\cdot\nabla=+i(\nabla\times)$ exactly), and its real/imaginary parts separate exactly into the two source-free vacuum Maxwell curl equations. This is a genuine, self-contained 2007 discovery, verified with no reference to any later literature. | CLAUDE.md decision 5 describes the model's photon as built from a real $(\mathbf E,\mathbf B)$ vector pair with a rotation-rate structure (findings 25/26: $c_\text{lat}=d\Omega/d|\mathbf k|$, $\Omega$ the rotation angle the $(\mathbf E,\mathbf B)$ pair traverses per tick) and as a "paired-spinor" bound state of two spin-½ Weyl quanta (finding 67–69). Does the model's photon construction have any structural relationship to a Riemann–Silberstein-type complex combination of $\mathbf E$ and $\mathbf B$ (i.e., is $\mathbf E+i\mathbf B$, or some analogous complex pairing, used anywhere in `casim.engine.gauge.photon` or the rotation-rate derivation), or did the model's $(\mathbf E,\mathbf B)$-rotation-rate picture arise by a route with no contact with this classical construction at all? | This is the second-clearest point of contact this reconstruction has found between the 2007 notebook and a *named* model decision (after NB-007's photon-pair correlation-queue entry) — both involve combining $\mathbf E$ and $\mathbf B$ into a single object with a rotation structure, but from a completely different starting point (a real spin-1 "Dirac equation" vs. a lattice CA rotation rate), and it is worth knowing whether the resemblance is substantive or coincidental. |

---

## Closures (Notebook v2, append-only — rows above are not edited)

- **NB-133, NB-134 row: CLOSED → `docs/theory/notebook-v2/NB2-002-sin2thetaW-2over9-lineage.md`**
  (2026-09-23). The row's literal question (connection to $\delta^*$) is answered **no,
  structurally** — the constants registry (D7) already treats $\delta^*$ and
  `sin2_thetaW_onshell` as three deliberately-unmerged $2/9$'s, and NB-133/134's content is about
  the latter only. The sharper question the row was reaching for (is NB-133's "$W^\pm=3e$" route
  an independent derivation of the model's own on-shell $\sin^2\theta_W=2/9$, vs. F49's BCC
  facet-axis count) is answered **no** — NB-133's guessed ratio fails to reproduce the model's
  *primary* value ($\sin^2\theta_W=\tfrac14$ at $\mu_\star=4\pi v$; the guess gives $2\sqrt2$, not
  $3$, at that point) and NB-134's corrected $Q_z$ entries carry no content beyond the angle
  itself once corrected. Coincidence, not lineage.
- **NB-128, NB-129 row: CLOSED → `docs/theory/notebook-v2/NB2-003-riemann-silberstein-eigenbasis.md`**
  (2026-09-23). Yes, concretely — `findings/F37-rs-bcc-chirality-helicity.md` builds
  $\mathbf F_\pm=E\pm iB$ as the exact eigenbasis of the same rotation matrix $R(\Omega)$ the F26
  even-law propagator (and hence F69's paired photon) still uses; not superseded, still load-bearing.
- **NB-037 row: CLOSED → `docs/theory/notebook-v2/NB2-005-torsion-tabletop-test.md`** (2026-09-23).
  The model's gravity sector is torsion-free **structurally** (the adopted F64/F178 construction has
  no independent connection for torsion to be nonzero of), not as an unexamined omission — the one
  place a genuine torsion magnitude *was* estimated (F63, standard EC coefficient, Hehl-Datta
  $3\kappa/16$, independently cross-checked against this session's read of the 2024 tabletop-test
  paper's own normalization) rests on the since-superseded F62 fork, a named, real, but currently
  low-priority gap. Fetched and read arXiv:2309.11536 in full: since ECSK carries no free constant
  beyond $G$, and the model's own $G$ is already exact (F79/F107), the model's predicted signal for
  the paper's proposed neutron-polarization tabletop test would be numerically identical to the
  paper's own quoted estimate if built — ≈20 orders of magnitude below current sensitivity. No D12
  claim card needed: not an independent falsifiable assertion, and not reachable by any known
  near-term measurement either way.
- **NB-005, NB-006, NB-044 row: CLOSED (the "was diamond-cubic ever a live alternative" half) →
  `docs/theory/notebook-v2/index.md` §1 row NB2-008, `findings/F400-bcc-vs-diamond-cubic-coordination-selector.md`**
  (2026-09-23). BCC's own coordination-8 shell was not "chosen over" a leaner coordination-4
  option: checked exactly, one of BCC's two constituent tetrahedra (the walk's own generator set,
  Paper 2 Eq. 20) is vertex-for-vertex identical to diamond-cubic's own coordination-4 bond
  tetrahedron — the same four integer vectors. What actually excludes diamond-cubic is a level
  below coordination-number combinatorics: it is not a Bravais lattice (its two sublattices are
  not related by any pure translation, checked exactly in rational arithmetic), so it fails
  BDPT's own single-orbit $(s{=}2,G=\mathbb Z^3)$ premise before dimension-counting is reached —
  it was never a competing candidate for F291/F292's own dimension selector to accept or reject.
  So "was a lower-coordination lattice ever considered and rejected" has a precise answer: it was
  never a candidate at the axiom level BDPT's theorem operates at, for a structural reason (basis
  vs. Bravais), not a coordination-number threshold. Not closed: whether a non-abelian generator
  group (Paper 1's own unsolved sketch) could realize a genuine coordination-4, $d=3$ QCA — named
  as unexplored, not ruled out.

## Notes for the correlation pass

- NB-007 additionally carries a **contamination caveat**: this session's read of it was informed
  in part by literature exposure that happened adjacent to (but not sourced from) the model's own
  `mohr-2010-maxwell-photon-wf-summary.md` comparison section (see batch-01 write-up header).
  The de Broglie/Jordan/Pryce/Perkins material itself is genuinely external and pre-dates the
  model by decades, so the *physics content* of the NB-007 verdict is sound — but treat the
  specific framing of "this is the exact point of contact with the model" with slightly more
  suspicion than the other rows, since this session was not perfectly blind when writing it.
