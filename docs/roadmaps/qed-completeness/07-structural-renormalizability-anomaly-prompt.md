# Session prompt — structural closure: renormalizability, Ward–Takahashi to all orders, RG, and the chiral anomaly / lattice-doubling consistency

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Establish the **all-orders / structural** completeness of the model's QED — the statements that make it a *theory* and not just a list of one-loop diagrams:

1. **Renormalizability closure** — a finite counterterm set $\{Z_1,Z_2,Z_3,\delta m\}$ suffices; no new (non-renormalizable) counterterms are generated.
2. **Ward–Takahashi to all orders → charge universality** — $Z_1=Z_2$ order by order, so the renormalized charge is $e=Z_1^{-1}Z_2 Z_3^{1/2}e_0=Z_3^{1/2}e_0$ (universal, independent of the fermion species).
3. **Renormalization group** — the Callan–Symanzik equation as the framework, with the one-loop $\beta$ ($b_0=4/3$, F251) as its leading coefficient.
4. **Chiral anomaly & lattice-doubling consistency** — the model is a *lattice Weyl* construction, so it must reproduce the correct axial (ABJ) anomaly coefficient, carry **no spurious gauge anomaly**, and have the doubling/anomaly interplay (Nielsen–Ninomiya) accounted for. F250 folded out the gauge doubler; this session settles the anomaly.

## Why this is tractable now (read first)

- **F251 / F252 / F258** — the three one-loop 1PI functions $\Pi$ (Z₃), $\Lambda$ (Z₁), $\Sigma$ (Z₂) and $\delta m$. The renormalizability and WT statements are structural claims *about these objects*; wait for the electron self-energy (Prompt 1, F258) so all three are computed.
- **F250** (`findings/F250-allk-gauge-pole-paired-photon.md`) — the paired-photon $k/2$ sharing folds out the Weyl doublers (a single BZ gauge zero at $k=0$). This is the lattice-doubling half of the anomaly story; build the axial-current side on top.
- **F68/F87** — the U(1) identity-channel coupling: its branch-blind structure is why the vector current is exactly conserved (Ward) and is the starting point for the axial-current (anomalous) divergence.
- **F162 / F155** (gluon sector) — the non-abelian $b_0=11$ machinery; your abelian RG statement is the $\text{U}(1)$ analogue with the F251 $b_0=4/3$.

## What to build

1. **Superficial-degree-of-divergence / counterterm closure — algebraic gate.** Enumerate the primitively-divergent 1PI amplitudes of QED by power counting (only the electron self-energy, photon self-energy, and vertex diverge; the 4-photon box is finite by gauge invariance despite naive counting). Show the divergences are absorbed by exactly $\{Z_1,Z_2,Z_3,\delta m\}$ — no others. sympy/symbolic power-counting.
2. **Ward–Takahashi all-orders → $Z_1=Z_2$ — exact gate.** From the U(1) identity-channel vertex (F68/F87), derive the WT identity $q_\mu\Gamma^\mu(p,p')=S^{-1}(p')-S^{-1}(p)$ as an operator statement (current conservation), and show it forces $Z_1=Z_2$ to all orders, hence $e_R=Z_3^{1/2}e_0$ — charge universality (the same renormalized charge for electron, muon, any species). Verify at one loop against F252/F258 as the concrete instance.
3. **Callan–Symanzik / RG — algebraic gate.** Write the CS equation for a QED Green's function with $\beta(e)=\tfrac{e^3}{12\pi^2}+\dots$ (i.e. the F251 $b_0=4/3$) and $\gamma_2,\gamma_3$ the field anomalous dimensions from $Z_2,Z_3$. Show the one-loop coefficients are consistent (e.g. $\gamma_3$ ↔ the running of $\alpha$ of F251). State the Landau-pole caveat honestly.
4. **Chiral (ABJ) anomaly + doubling — exact gate.** Compute the axial-current divergence $\partial_\mu j_5^\mu=\tfrac{e^2}{16\pi^2}\epsilon^{\mu\nu\rho\sigma}F_{\mu\nu}F_{\rho\sigma}$ (the triangle) and get the coefficient $\tfrac{1}{16\pi^2}$ (or $\tfrac{\alpha}{2\pi}$ form). Then the **lattice consistency**: show the F250 doubler-folding is what keeps the *vector* current anomaly-free (gauge current conserved — Ward exact, already used throughout) while the *axial* current carries the physical anomaly — i.e. the model realizes the Nielsen–Ninomiya trade-off correctly (the paired-photon $k/2$ structure removes the doubler that would otherwise cancel the anomaly). This is the deepest lattice-QFT completeness check.

## Method + hygiene

- Exactness ladder: power-counting closure, WT-all-orders/$Z_1=Z_2$, and the anomaly coefficient $\tfrac{1}{16\pi^2}$ all via **sympy** (these are algebraic); the CS coefficients tie to F251 numerically. Record in `docs/status/exactness-inventory.md`.
- The anomaly triangle needs the Dirac trace with $\gamma_5$ — build $\gamma_5$ explicitly with the F252 gamma basis; no `eig` on chiral matrices, and be careful with the regularization (the anomaly is exactly the scheme-dependent piece — document the regulator and that the coefficient is regulator-independent).
- Depends on Prompt 1 (F258) for the concrete $Z_2$; if it is not yet on disk, reproduce the one-loop $Z_2$ log-coefficient inline and note the dependency.
- Deliverables: `ca-simulation/ca_qed_renormalization.py` (power-counting + WT/RG) and `ca-simulation/ca_chiral_anomaly.py`, tests, JSON, finding. `grep` the true max first (suggested F264). Regen indexes, changelog, exactness-inventory.

## Definition of done

Counterterm closure shown (only $\{Z_1,Z_2,Z_3,\delta m\}$); $Z_1=Z_2$ to all orders from WT → charge universality; the CS equation assembled with the F251 one-loop $\beta$; and the ABJ anomaly coefficient $\tfrac{1}{16\pi^2}$ reproduced with the F250 doubler-folding shown to keep the vector current anomaly-free while the axial current carries the anomaly (Nielsen–Ninomiya consistency). This is the structural statement that the model's QED is a renormalizable, anomaly-consistent gauge theory.

## External references

- F. J. Dyson, *Phys. Rev.* 75, 1736 (1949) — the S-matrix, renormalization, and the counterterm program.
- J. C. Ward, *Phys. Rev.* 78, 182 (1950); Y. Takahashi, *Nuovo Cim.* 6, 371 (1957) — the Ward–Takahashi identity and $Z_1=Z_2$.
- C. G. Callan, *Phys. Rev. D* 2, 1541 (1970); K. Symanzik, *Commun. Math. Phys.* 18, 227 (1970) — the renormalization-group equation.
- S. L. Adler, *Phys. Rev.* 177, 2426 (1969); J. S. Bell & R. Jackiw, *Nuovo Cim. A* 60, 47 (1969) — the ABJ axial anomaly.
- H. B. Nielsen & M. Ninomiya, *Nucl. Phys. B* 185, 20 (1981); 193, 173 (1981) — the fermion-doubling no-go on the lattice.
- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §10 (power counting / renormalizability), §19 (the axial anomaly).
