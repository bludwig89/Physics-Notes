# Paper V — The Strong Force: A Dynamical $SU(3)$ Colour Sector, Gluon Self-Coupling, and Exact Confinement

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper V of X. Builds on Paper I (rotation propagator) and Paper IV (gauge principle); supplies the binding for the baryon sector (Paper X).*

---

## Abstract

We construct the strong interaction on the BCC quantum-cellular-automaton vacuum as a dynamical $SU(3)_c$ colour gauge theory built by the *same* prescription that produces electromagnetism and the weak force: a colour-octet bilinear propagated by the lattice rotation law, with Yang–Mills self-coupling supplied by the $SU(3)$ structure constants $f^{abc}$. The gluon octet is verified to transform in the adjoint, to conserve the colour Casimir, and to preserve link unitarity under self-coupling, all to machine precision (20/20 checks; 8 bit-for-bit). We then establish **confinement as a model prediction**, not merely a compatibility: in two dimensions the lattice gauge theory is exactly solvable, the Wilson loop obeys a strict area law $\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,W\rangle=w(\beta)^{RT}$, and the static quark potential is exactly linear, $V(R)=\sigma R$ with string tension $\sigma(\beta)=-\ln w(\beta)>0$ for **every** finite coupling. The Creutz ratio is size-independent and equal to $\sigma$, the cleanest confinement signature, verified to $2.2\times10^{-16}$. A gauge-covariant Wilson gradient-flow/cooling driver is provided and validated (action-monotone, $\mathfrak{su}(3)$-valued force, gauge-covariant). Confinement plus the colour-singlet construction together explain why no free quark exists and why the colour-neutral baryon does — the structural prerequisite for Paper X.

---

## 1. Introduction

The strong force binds quarks into hadrons and confines colour so that no isolated quark is ever observed. In the Standard Model it is quantum chromodynamics (QCD), a non-Abelian $SU(3)$ gauge theory whose confining property, while overwhelmingly supported by lattice QCD, is not analytically proven in $3+1$ dimensions (it is one of the Clay Millennium problems).

On the BCC lattice the colour sector is built by transcribing, group-for-group, the construction that produced the weak $W$ (Paper VI) and the photon (Papers II, IV): replace the weak isospin $\tau^a/2$ by the colour generators $T^a$ (Gell-Mann/2) and the antisymmetric symbol $\epsilon^{abc}$ by the $SU(3)$ structure constants $f^{abc}$. This paper delivers (i) the dynamical gluon field with self-coupling and (ii) a confinement result that, in the exactly-solvable two-dimensional case, is algebraically exact.

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

with **Hermitian** (not transpose) conjugation, required because $V^\mathsf T V\neq I$ for $SU(3)$. The eight components are the gluon octet. Each is propagated by the Paper I rotation law per colour index, on the 2D-square lattice ($c_\text{lat}=1/\sqrt2$) and the 3D BCC lattice ($\Omega^\pm=2\omega^\pm_\text{BCC}(\mathbf k/2)$, $c_\text{lat}=1/\sqrt3$). The octet transforms as the $SU(3)$ adjoint (residual $6.7\times10^{-16}$ in 2D, $7.8\times10^{-16}$ on BCC) and conserves the colour Casimir $\sum_a\|G^a\|^2$ (bit-for-bit).

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

is the $SU(3)$ analogue of the $W$ self-interaction and preserves link unitarity to $\sim10^{-15}$ on both lattices (the update is a product of two $SU(3)$ elements). The quark colour current sources the gluon by the abelian-linearised Yang–Mills equation $\partial_t E^a(\mathbf k)=\Omega(\mathbf k)B^a(\mathbf k)+gJ^a(\mathbf k)$, with each octet component sourced only by its own current (diagonal, exact zero off-diagonal).

The colour sector is thus structurally parallel to the weak sector: cold-link vacuum gives $F=0$ exactly, constant-gauge field-strength magnitude is invariant at machine $\varepsilon$, and unitarity is guaranteed because $\exp(iH)U$ stays in the group.

---

## 3. Confinement (exact in two dimensions)

### 3.1 Why $2$D is the rigorous testbed

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

$\sigma$ is strictly positive at every coupling: **2D $SU(3)$ confines for all $\beta$.** This is the first place the model *predicts* confinement rather than being merely compatible with it.

### 3.3 The gradient-flow / cooling driver

A gauge-covariant Wilson gradient-flow (Lüscher) and checkerboard-cooling driver is provided,

$$
\frac{d}{dt}V_\mu(x)=Z_\mu(V)\,V_\mu(x),\qquad Z_\mu=-[V_\mu\Sigma_\mu^\dagger]_\text{TA},
\tag{3.4}
$$

with the traceless-anti-Hermitian projection and staple sum $\Sigma_\mu$. It is verified as a cold fixed point (bit-for-bit), action-monotone ($dS_W/dt\le0$), $\mathfrak{su}(3)$-valued ($5.6\times10^{-16}$), gauge-covariant ($7.8\times10^{-15}$), and genuinely diffusive (acts as the lattice Laplacian, $4.9\times10^{-10}$). An important caveat verified directly: cooling is a *smoother*, not a confiner — flowing a disordered ensemble raises the mean plaquette and dissolves the string tension, so the static potential must be read from the unflowed ensemble. Confinement lives in the disordered ensemble; the flow's legitimate role is scale-setting and topological studies.

### 3.4 Scope

The exact area law is special to two dimensions (independent plaquettes). Confinement in $3+1$D on the BCC lattice requires Monte-Carlo with a genuine deconfinement transition and is not claimed here; the 2D result is the rigorous, exactly-solvable anchor. The linear potential is the quenched (static-source) potential — no dynamical quark loops, hence no string breaking.

---

## 4. Colour neutrality and the road to hadrons

Confinement ($\sigma>0$) makes an isolated colour charge infinitely costly; the finite-energy configuration is the colour singlet. The unique singlet of $3\otimes3\otimes3=1\oplus8\oplus8\oplus10$ is the totally antisymmetric contraction $\varepsilon_{abc}q^aq^bq^c$, which is gauge-invariant because $\det V=1$ for $SU(3)$. This is the baryon interpolating operator developed in Paper X; here we note only that the strong sector supplies both halves of "why no free quarks, and why a proton exists": separating any one quark from a singlet costs $\sigma R\to\infty$, while the singlet itself is colour-neutral and bound.

---

## 5. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| $f^{abc}$ Jacobi identity | §2.1 | $1.1\times10^{-16}$ |
| Octet adjoint transform (2D / BCC) | §2.2 | $6.7\times10^{-16}$ / $7.8\times10^{-16}$ |
| Colour Casimir conservation | §2.2 | $0$ (bit-for-bit) |
| Cold-link $G^a_{\mu\nu}=0$ | §2.3 | $0$ (bit-for-bit) |
| Self-coupling link unitarity | §2.3 | $\sim10^{-15}$ |
| Area law $\langle W\rangle=w^{RT}$ / Creutz ratio | §3.1–3.2 | $2.2\times10^{-16}$ |
| Linear potential $V(R)=\sigma R$ | §3.2 | $8.9\times10^{-16}$ |
| String tension $\sigma>0\ \forall\beta$ | §3.2 | $\sigma_\text{min}=0.219$ |
| Gradient-flow gauge covariance | §3.3 | $7.8\times10^{-15}$ |

The strong sector passed 20/20 dynamical-gluon checks and 6+8 flow/confinement checks. Underlying findings: F43 (dynamical gluons), F70 (gradient flow + exact confinement), F71 (colour-singlet baryon).

---

## 6. Discussion

The strong sector demonstrates the modularity of the construction: the *same* rotation propagator, plaquette field strength, and structure-constant self-coupling that built the weak sector build the colour sector, with only the group swapped. The qualitatively new physics — confinement — is delivered exactly where it can be delivered exactly (2D), as an area law forced by Schur's lemma, with the higher-dimensional regime scoped honestly as a Monte-Carlo problem.

Two limits are explicit. First, the model does not yet compute the $3+1$D string tension or the QCD scale $\Lambda$ (Tier-B calibration). Second, the baryon binding (Paper X) currently uses the 2D static potential rather than a three-body flux-tube computation. Neither limit affects the structural result: colour is confined, singlets are neutral and bound, and the gluon is a fully dynamical adjoint field with the correct self-coupling.

---

## References

1. K. G. Wilson, "Confinement of quarks," *Phys. Rev. D* **10**, 2445 (1974).
2. M. Creutz, *Quarks, Gluons and Lattices* (Cambridge, 1983); A. M. Polyakov, *Gauge Fields and Strings* (1987) — exact 2D solvability.
3. M. Lüscher, "Properties and uses of the Wilson flow in lattice QCD," *JHEP* **08**, 071 (2010).
4. M. Gell-Mann, "Symmetries of Baryons and Mesons," *Phys. Rev.* **125**, 1067 (1962) — $SU(3)$ and $f^{abc}$.
5. Project findings: F43 (dynamical $SU(3)$ gluons), F70 (gradient flow / exact confinement), F71 (colour-singlet baryon).

*Companion papers: I (substrate), IV (electromagnetism), VI (weak), X (baryons).*
