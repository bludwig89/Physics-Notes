# Paper V — The Strong Force: A Dynamical $SU(3)$ Colour Sector, Gluon Self-Coupling, and Confinement from Exact Area Law to Colour-Dielectric Condensate

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper V of XI. Builds on Paper I (rotation propagator) and Paper IV (gauge principle); supplies the binding for the baryon sector (Paper X).*

*Revision 2 (2026-06-08): re-issued for the eleven-paper series; extended beyond the exact 2D area law (Rev. 1) to the $3+1$D confinement story — the colour-dielectric dual superconductor (F86), the lattice-gauge Monte-Carlo string tension (F94), and the centre-phase closure principle (F97/F98). Gluon propagator law updated to the even law forced by F91.*

---

## Abstract

We construct the strong interaction on the BCC quantum-cellular-automaton vacuum as a dynamical $SU(3)_c$ colour gauge theory built by the *same* prescription that produces electromagnetism and the weak force: a colour-octet bilinear propagated by the lattice rotation law, with Yang–Mills self-coupling supplied by the $SU(3)$ structure constants $f^{abc}$. The gluon octet is verified to transform in the adjoint, to conserve the colour Casimir, and to preserve link unitarity under self-coupling, all to machine precision. The gluon propagator rides the **even** rotation law — forced, not chosen, because colour coupling is chirality-blind (the F91 classification theorem). We then establish confinement at three complementary levels: (i) in two dimensions the lattice gauge theory is exactly solvable, the Wilson loop obeys a strict area law, and the static potential is exactly linear $V(R)=\sigma R$ with $\sigma(\beta)=-\ln w(\beta)>0$ for every finite coupling; (ii) in $3+1$D a colour-dielectric dual-superconductor (BPS) construction gives the flux-tube tension $\sigma_\text{BPS}=2\pi v^2 n$ exactly, with $n$ the centre charge; (iii) a $3+1$D $SU(3)$ heat-bath lattice Monte-Carlo with Lüscher–Weisz multilevel sampling measures the area-law tension directly and fixes the condensate scale via $v^*=\sqrt{\sigma_A/2\pi}$. The unifying statement (the closure principle) is that a stable colour state is one whose $\mathbb Z_3$ centre-phase budget closes exactly (N-ality 0), and the object enforcing the budget — the colour-dielectric condensate — is itself the binder. Confinement plus the colour-singlet construction together explain why no free quark exists and why the colour-neutral baryon does — the structural prerequisite for Paper X.

---

## 1. Introduction

The strong force binds quarks into hadrons and confines colour so that no isolated quark is ever observed. In the Standard Model it is quantum chromodynamics (QCD), a non-Abelian $SU(3)$ gauge theory whose confining property, while overwhelmingly supported by lattice QCD, is not analytically proven in $3+1$ dimensions (it is one of the Clay Millennium problems).

On the BCC lattice the colour sector is built by transcribing, group-for-group, the construction that produced the weak $W$ (Paper VI) and the photon (Papers II, IV): replace the weak isospin $\tau^a/2$ by the colour generators $T^a=\lambda^a/2$ and the antisymmetric symbol $\epsilon^{abc}$ by the $SU(3)$ structure constants $f^{abc}$. This paper delivers (i) the dynamical gluon field with self-coupling, (ii) confinement at the exactly-solvable 2D level, and (iii) the $3+1$D confinement mechanism — a colour-dielectric condensate cross-checked against a genuine gauge-Monte-Carlo string tension — culminating in a single closure principle that the baryon sector (Paper X) inherits.

---

## 2. The dynamical gluon sector

### 2.1 Structure constants

The totally antisymmetric $SU(3)$ structure constants follow from $[T^a,T^b]=if^{abc}T^c$, with nine independent non-zero values

$$
f^{123}=1,\quad f^{147}=f^{246}=f^{257}=f^{345}=\tfrac12,\quad f^{156}=f^{367}=-\tfrac12,\quad f^{458}=f^{678}=\tfrac{\sqrt3}{2}.
\tag{2.1}
$$

The Jacobi identity $f^{abe}f^{ecd}+f^{bce}f^{ead}+f^{cae}f^{ebd}=0$ holds at $1.1\times10^{-16}$ across all $8^4$ index combinations.

### 2.2 Colour-octet bilinear and free propagation

Following the photon/$W$ construction, build the colour-octet Pauli-vector bilinear from the quark colour-triplet field $q^{f,c}$ (flavour $f$, colour $c$):

$$
G^{a,i}(\mathbf x)=\sum_f\sum_{cc'}(T^a)_{cc'}\sum_{\alpha\beta}q^{f,c,\alpha\dagger}(\mathbf x)\,\sigma^i_{\alpha\beta}\,q^{f,c',\beta}(\mathbf x),
\qquad a=1,\dots,8,
\tag{2.2}
$$

with **Hermitian** (not transpose) conjugation, required because $V^\mathsf T V\neq I$ for $SU(3)$. The eight components are the gluon octet, propagated by the Paper I rotation law per colour index. The octet transforms as the $SU(3)$ adjoint (residual $6.7\times10^{-16}$ in 2D, $7.8\times10^{-16}$ on BCC) and conserves the colour Casimir $\sum_a\|G^a\|^2$ (bit-for-bit) (Finding F43).

**Propagator law — forced to be even (F91).** Whereas the chiral $W^\pm$ ride the chiral law and the photon rides the even law, the gluon propagator is **even**, and this is forced rather than chosen: colour coupling acts as $g_s\,T^a$ on the colour index and is *blind to chirality* (both branches carry the same colour weight $g_s$), so the F68 commutator argument that selects the even law for the helicity-blind photon applies verbatim in colour. Accordingly the BCC gluon propagator was migrated chiral→even on 2026-06-04 (`gluon_rotation_step_spectral_bcc`; the pre-migration chiral step is retained as `..._chiral` for historical comparison). The migration changes no observable (gluons are confined) but brings the code into conformity with the forcing principle.

### 2.3 Yang–Mills self-coupling

The Wilson plaquette field strength is

$$
G^a_{\mu\nu}(\mathbf x)=\frac{-i}{g\,a^2}\,\mathrm{Tr}\!\big[T^a(U_\square-U_\square^\dagger)\big]=\frac{2}{g\,a^2}\,\mathrm{Im}\,\mathrm{Tr}\!\big[T^aU_\square\big],
\tag{2.3}
$$

which vanishes bit-for-bit on identity ("cold") links because $T^a$ is traceless. The self-coupling tick

$$
\delta W^a=g\,\Delta t\,f^{abc}\,W^b\,G^c,\qquad U_\ell\to e^{i\,\delta W^a T^a}\,U_\ell,
\tag{2.4}
$$

is the $SU(3)$ analogue of the $W$ self-interaction and preserves link unitarity to $\sim10^{-15}$ on both lattices (the update is a product of two $SU(3)$ elements). The quark colour current sources the gluon by the abelian-linearised Yang–Mills equation $\partial_t E^a(\mathbf k)=\Omega(\mathbf k)B^a(\mathbf k)+gJ^a(\mathbf k)$, with each octet component sourced only by its own current (diagonal, exact zero off-diagonal). The colour sector is thus structurally parallel to the weak sector: cold-link vacuum gives $F=0$ exactly, constant-gauge field-strength magnitude is invariant at machine $\varepsilon$, and unitarity is guaranteed because $\exp(iH)U$ stays in the group.

---

## 3. Confinement I: exact area law in two dimensions

### 3.1 Why 2D is the rigorous testbed

In two Euclidean dimensions, after gauge-fixing to axial gauge $U_x\equiv I$, the plaquette variables are statistically independent. By Schur's lemma the single-plaquette mean of the class-invariant Wilson distribution is

$$
\langle U\rangle=w(\beta)\,I,\qquad w(\beta)=\Big\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,U\Big\rangle,\qquad d\mu_\beta(U)\propto e^{(\beta/N)\mathrm{Re}\,\mathrm{Tr}\,U}\,dU.
\tag{3.1}
$$

A Wilson loop enclosing area $A=R\cdot T$ is the ordered product of the enclosed independent plaquettes, so

$$
\Big\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,W(R,T)\Big\rangle=w(\beta)^{A}\quad\text{exactly.}
\tag{3.2}
$$

### 3.2 Linear potential and string tension

Equation (3.2) gives, with no approximation,

$$
\boxed{\;\sigma(\beta)=-\ln w(\beta)>0\ \ \forall\,\beta<\infty,\qquad \chi(R,T)=\sigma,\qquad V(R)=\sigma R.\;}
\tag{3.3}
$$

Here $w(\beta)$ is computed deterministically by $SU(3)$ Weyl-torus quadrature (spectrally accurate, grid-converged to $3\times10^{-17}$). The **Creutz ratio** $\chi(R,T)=-\ln\frac{W(R,T)W(R-1,T-1)}{W(R-1,T)W(R,T-1)}=-\ln w=\sigma$ is independent of loop size to $2.2\times10^{-16}$, because the area difference of the four loops is exactly one plaquette. A size-independent Creutz ratio is equivalent to a strict area law, equivalent to a linear potential, equivalent to confinement. Representative string tensions:

| $\beta$ | 0.25 | 0.5 | 1.0 | 2.0 | 4.0 | 8.0 | 20.0 |
|---|---|---|---|---|---|---|---|
| $\sigma(\beta)$ | 4.256 | 3.543 | 2.811 | 2.051 | 1.274 | 0.624 | 0.219 |

$\sigma$ is strictly positive at every coupling: **2D $SU(3)$ confines for all $\beta$.** This is the first place the model *predicts* confinement rather than being merely compatible with it (Finding F70).

### 3.3 The gradient-flow / cooling driver

A gauge-covariant Wilson gradient-flow (Lüscher) and checkerboard-cooling driver is provided and validated as a cold fixed point (bit-for-bit), action-monotone ($dS_W/dt\le0$), $\mathfrak{su}(3)$-valued ($5.6\times10^{-16}$), gauge-covariant ($7.8\times10^{-15}$), and genuinely diffusive (acts as the lattice Laplacian, $4.9\times10^{-10}$). A caveat verified directly: cooling is a *smoother*, not a confiner — flowing a disordered ensemble dissolves the string tension — so the static potential must be read from the unflowed ensemble. The flow's legitimate role is scale-setting and topological studies.

### 3.4 Scope of the exact result

The exact area law is special to two dimensions (independent plaquettes). Confinement in $3+1$D requires either a constructive condensate model (§4) or genuine Monte-Carlo (§5); the 2D result is the rigorous, exactly-solvable anchor. The linear potential is the quenched (static-source) potential — no dynamical quark loops, hence no string breaking.

---

## 4. Confinement II: the colour-dielectric dual superconductor (3+1D)

The $3+1$D confining vacuum is modelled as a **dual superconductor**: a colour-magnetic condensate that expels colour-electric flux into a thin tube (the dual Meissner effect), exactly as a type-II superconductor expels magnetic flux into Abrikosov vortices. In this picture the lattice is a **colour dielectric** $\varepsilon_c(\mathbf x)$ — the colour analogue of the gravitational dielectric of Paper VII — whose condensate VEV $v$ sets the confinement scale (Finding F86, "Option C").

At the Bogomolny (BPS) point the flux-tube tension is exact:

$$
\boxed{\;\sigma_\text{BPS}=2\pi v^2\,|n|\;}
\tag{4.1}
$$

with $n$ the topological winding of the tube, equal to the source's $\mathbb Z_3$ **centre charge** (triality/N-ality). The construction was built and verified (6/6) with the BPS tension exact (Tier-1). The condensate itself is obtained self-consistently from the model in Finding F88, fixing $v$ rather than leaving it free.

The decisive identification (Finding F98) is that the centre charge $n$ plays two roles at once: it is the **budget label** (a colour state is asymptotic iff its centre phase closes, N-ality 0) *and* the **binder coefficient** (the multiplier of the tension (4.1)). One object, two roles: the enforcer of the budget is literally the coefficient of the binding tension, so $\sigma=0$ exactly when the budget closes and $\sigma>0$ otherwise.

---

## 5. Confinement III: gauge Monte-Carlo string tension (3+1D)

To check that the constructive condensate matches a genuine non-Abelian gauge sector, a $3+1$D $SU(3)$ heat-bath lattice Monte-Carlo with Lüscher–Weisz multilevel sampling (84$\times$ variance reduction) measures the area-law tension $\sigma_A$ directly (Finding F94, "Option A"). The asymptotic $k$-string tensions follow the Casimir/centre law

$$
\sigma_k=\frac{k(N-k)}{N-1}\,\sigma_1,
\tag{5.1}
$$

which depends only on the N-ality $k$ (centre-periodic: $\sigma_0=\sigma_N=0$; adjoint screened, fundamental confined; $k\leftrightarrow N-k$ degenerate). The two $3+1$D routes are tied together by the exact bridge $v^*=\sqrt{\sigma_A/2\pi}$: the gauge-MC string tension *is* the colour-dielectric condensate scale, re-expressed (round-trip $\sigma_C(v^*)=\sigma_A$ to $<10^{-12}$). The two routes agree on everything the confinement claim needs — $\sigma_0=0$ and $\sigma_{k\neq0}>0$ — and differ only on the relative weight of the $k=2$ string (Abelian-BPS $\sigma_2=2\sigma_1$ vs non-Abelian Casimir $\sigma_2=\sigma_1$), a known and flagged A-vs-C gap. The model predicts the non-Abelian Casimir/sine-law regime is physical, in agreement with lattice QCD.

---

## 6. The closure principle and the road to hadrons

Confinement ($\sigma>0$ off centre-closure) makes an isolated colour charge infinitely costly; the finite-energy configuration is the colour singlet. The unique singlet of $3\otimes3\otimes3=1\oplus8\oplus8\oplus10$ is the totally antisymmetric contraction $\varepsilon_{abc}q^aq^bq^c$, gauge-invariant because $\det V=1$ for $SU(3)$. Stated in the closure language (Findings F97/F98):

> **Closure principle.** A stable composite is a configuration whose phase budget closes exactly; the object that enforces the budget is itself the binding agent. For colour the budget is the $\mathbb Z_3$ centre phase: $qqq$ gives $3\times\tfrac{2\pi}3=2\pi\equiv0$ (closed), $q\bar q$ gives $0$ (closed), but a diquark $qq$ gives $\tfrac{4\pi}3\not\equiv0$ (open, confined, never asymptotic).

This is the colour-sector instance of the same grammar that governs the pair sector (where the budget is the unitarity wrap $\pi/2$, Paper III §6 / Finding F92). A no-go theorem (F97) shows the two-body pair fixed point does not extend to three constituents — the baryon cannot be a phase-kinematic bound state — which *predicts* that baryon mass is $\sim99\%$ field energy rather than constituent rest phase (PDG quark sum is $0.96\%$ of $m_p$). The strong sector thus supplies both halves of "why no free quarks, and why a proton exists": separating one quark from a singlet costs $\sigma R\to\infty$, while the singlet itself is colour-neutral, centre-closed, and bound. Paper X builds the proton, pion, and deuteron on this foundation.

---

## 7. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| $f^{abc}$ Jacobi identity | §2.1 | $1.1\times10^{-16}$ |
| Octet adjoint transform (2D / BCC) | §2.2 | $6.7\times10^{-16}$ / $7.8\times10^{-16}$ |
| Colour Casimir conservation | §2.2 | $0$ (bit-for-bit) |
| Even gluon propagator forced (F91) | §2.2 | structural (chirality-blind coupling) |
| Cold-link $G^a_{\mu\nu}=0$ | §2.3 | $0$ (bit-for-bit) |
| Self-coupling link unitarity | §2.3 | $\sim10^{-15}$ |
| Area law $\langle W\rangle=w^{RT}$ / Creutz ratio | §3.1–3.2 | $2.2\times10^{-16}$ |
| Linear potential $V(R)=\sigma R$, $\sigma>0\ \forall\beta$ | §3.2 | $\sigma_\text{min}=0.219$ |
| Gradient-flow gauge covariance | §3.3 | $7.8\times10^{-15}$ |
| BPS flux-tube tension $\sigma=2\pi v^2 n$ | §4 | exact (Tier-1) |
| A↔C bridge $v^*=\sqrt{\sigma_A/2\pi}$ | §5 | $<10^{-12}$ |
| $\mathbb Z_3$ closure ($qqq,q\bar q\to0$; $qq\to4\pi/3$) | §6 | exact (integer) |

Underlying findings: F43 (dynamical gluons), F70 (gradient flow + exact 2D confinement), F71 (colour-singlet baryon), F86 (colour-dielectric dual superconductor), F88 (condensate from the model), F91 (even gluon propagator), F94 (gauge-MC string tension + A↔C bridge), F97 (centre-phase closure no-go), F98 (enforcer = binder).

---

## 8. Discussion

The strong sector demonstrates the modularity of the construction: the *same* rotation propagator, plaquette field strength, and structure-constant self-coupling that built the weak sector build the colour sector, with only the group swapped — and the propagator law (even) is forced by the chirality-blindness of colour, not chosen. The qualitatively new physics — confinement — is delivered exactly where it can be delivered exactly (2D), modelled constructively in $3+1$D as a colour dielectric, and cross-checked against a genuine gauge Monte-Carlo, with all three views unified by the centre-phase closure principle.

Two limits are explicit. First, the absolute $3+1$D string tension and the QCD scale $\Lambda$ remain calibration (Tier-B) items; the gauge-MC production run is user-run. Second, deriving $\sigma$ as the Lagrange-multiplier price of centre-phase non-closure *inside the QCA update rule itself* (the deepest form of the closure principle) is future work. Neither affects the structural result: colour is confined, singlets are neutral and bound, and the gluon is a fully dynamical adjoint field with the correct self-coupling.

---

## References

1. K. G. Wilson, "Confinement of quarks," *Phys. Rev. D* **10**, 2445 (1974).
2. M. Creutz, *Quarks, Gluons and Lattices* (Cambridge, 1983); A. M. Polyakov, *Gauge Fields and Strings* (1987) — exact 2D solvability.
3. G. 't Hooft, "Topology of the gauge condition and new confinement phases," *Nucl. Phys. B* **190**, 455 (1981); S. Mandelstam, *Phys. Rep.* **23**, 245 (1976) — dual superconductor.
4. M. Lüscher, "Properties and uses of the Wilson flow in lattice QCD," *JHEP* **08**, 071 (2010); M. Lüscher, P. Weisz, "Locality and the continuum limit..." (multilevel).
5. M. Gell-Mann, "Symmetries of Baryons and Mesons," *Phys. Rev.* **125**, 1067 (1962) — $SU(3)$ and $f^{abc}$.
6. Project findings: F43, F70, F71, F86, F88, F91, F94, F97, F98.

*Companion papers: I (substrate), IV (electromagnetism / gauge principle), VI (weak), XI (baryons).*
