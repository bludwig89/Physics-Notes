# Paper II — The Photon as a Bound Pair of Spin-½ Lattice Quanta: A Non-Birefringent, Luminal, Transverse Composite

**B. Ludwig**
*Independent researcher*

**Notebook source material:** M. Ludwig (2007), *Physics Notes*, pp. 5–6 ("spinor electrodynamics")

*Series: "A Universe in a Bottle" — Paper II of XI. Builds directly on Paper I (BCC QCA substrate; speed of light as rotation rate).*

*Revision 2 (2026-06-08): re-issued for the eleven-paper series; cell-size statements updated to the canonical F107 value $a=6.5978\,\ell_P$ adopted in Paper VII.*

---

## Abstract

We construct the electromagnetic photon not as a fundamental spin-1 gauge boson but as a bound pair of two spin-$\tfrac12$ Weyl quanta of the underlying body-centred-cubic (BCC) quantum cellular automaton — the lattice realisation of de Broglie's neutrino theory of light. The pair carries total momentum $\mathbf k$ shared as $\mathbf k/2$ between two constituents on opposite chiral branches, so its real $(\mathbf E,\mathbf B)$ field rotates at the **helicity-symmetric** rate $\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)\equiv\Omega_\text{even}(\mathbf k)$. We show this object is (i) massless and luminal, with group velocity $\to1/\sqrt3=c_\text{lat}$; (ii) transverse and spin-1, with two physical polarisations; and (iii) **exactly non-birefringent**, because both helicities ride the single rate $\Omega_\text{pair}$ — there is no single-branch photon to split against. This last property is decisive: an earlier composite construction (the $\sigma$-bilinear photon) assigned each helicity to its own branch and was therefore birefringent at first order in $k$, a prediction excluded by gamma-ray-burst (GRB) and active-galactic-nucleus (AGN) polarimetry by many orders of magnitude at the gravitationally-fixed cell size. The paired photon removes that prediction entirely and is independently forced from three directions — observation, $U(1)$ minimal coupling, and Ludwig's notebook construction — that all land on the same dispersion. All claims are verified to machine precision (5/5 checks; residuals $0$ to $\sim10^{-15}$).

---

## 1. Introduction

Paper I established that on the BCC QCA a correlated pair of lattice spinors furnishes a real field pair $(\mathbf E,\mathbf B)$ whose free evolution is an exact rotation, and that the speed of light is the rotation rate of that pair per unit wavenumber. The present paper answers the next question: *what, precisely, is the photon?*

In the Standard Model the photon is a fundamental spin-1 gauge field $A_\mu$ introduced by hand to gauge $U(1)$. On the lattice no such field need be posited. Following a proposal recorded in Ludwig's 2007 notebook (pp. 5–6) — and ultimately de Broglie's 1930s neutrino theory of light — the photon is a **bound pair of two spin-$\tfrac12$ "fermion-photons" $\gamma_{1/2}$ that behave together as a single boson and only occur as a pair; they do not occur separately.** This is structurally the same idea as a Cooper pair in superconductivity: two spin-$\tfrac12$ objects bound into a single bosonic excitation.

The composite photon arises *natively* from the lattice's own Weyl quanta and requires no additional field construct, which is its chief economy over the Standard-Model photon. The task of this paper is to make the construction precise, derive its propagation law, and confront its observational consequences.

---

## 2. The two-branch structure of the BCC walk

From Paper I (Eq. 2.1) the free Weyl walk has two dispersion branches,

$$
\omega^{\pm}(\mathbf k) = \arccos\!\big(c_xc_yc_z \pm s_xs_ys_z\big),
\qquad c_i=\cos\tfrac{k_i}{\sqrt3},\ s_i=\sin\tfrac{k_i}{\sqrt3},
\tag{2.1}
$$

related by parity $\omega^+(-\mathbf k)=\omega^-(\mathbf k)$. The two branches are the two chiralities/helicities of the walk. A real electromagnetic field is built from the Riemann–Silberstein (RS) combinations

$$
\mathbf F_\pm(\mathbf k) = \mathbf E(\mathbf k)\pm i\mathbf B(\mathbf k),
\tag{2.2}
$$

which are exactly the eigenvectors of the one-tick rotation matrix $R(\Omega)$ of Paper I: $R(\Omega)(1,\mp i)^\mathsf T=e^{\mp i\Omega}(1,\mp i)^\mathsf T$. Reality of $(\mathbf E,\mathbf B)$ forces $\mathbf F_+(-\mathbf k)=\mathbf F_-^*(\mathbf k)$.

### 2.1 The fork: two ways to assign helicities to branches

There are two consistent ways to propagate the RS eigenstates while preserving the reality (Hermitian-symmetry) constraint:

- **Chiral assignment (the $\sigma$-bilinear photon, F29/F37/F39):** let each helicity ride its own branch, $\mathbf F_+\!\to\!\Omega^+=2\omega^+(\mathbf k/2)$ and $\mathbf F_-\!\to\!\Omega^-=2\omega^-(\mathbf k/2)$. Hermitian symmetry is preserved because $\Omega^+(-\mathbf k)=\Omega^-(\mathbf k)$.
- **Even assignment (the paired photon, this paper):** let *both* helicities ride the single symmetric rate $\Omega_\text{pair}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)=\Omega_\text{even}$.

These two laws are physically inequivalent, and §4 shows the first is observationally dead while the second survives. The chiral law is retained only for the massive/confined sectors (Papers V–VI), which carry no astrophysical vacuum-birefringence bound. The systematic statement of which sector rides which law is the pairing classification theorem of Paper IV (Finding F91): the propagator law is *forced* by the chirality structure of each coupling, not chosen.

---

## 3. The paired photon

### 3.1 Construction

The photon is a bound $(+,-)$ pair: total momentum $\mathbf k$ shared by two Weyl constituents at $\mathbf k/2$ each, one on the $+$ branch and one on the $-$ branch. Because the pair is bound and symmetric, the phase it accumulates per tick is the **sum** of the constituent phases:

$$
\boxed{\;\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)\;\equiv\;\Omega_\text{even}(\mathbf k).\;}
\tag{3.1}
$$

This is exactly the even-law rotation rate of the lattice's $(\mathbf E,\mathbf B)$ propagator from Paper I — no new propagator is invented; the pairing *names* the even law as the photon law and supplies its physical interpretation. The free field then evolves by the exact rotation (Paper I, Eq. 3.1) with $\Omega=\Omega_\text{pair}$. The propagator is implemented as `ca_photon_pair.py` (propagator = even law `ca_wmu._f26_rotation_step`).

### 3.2 Why non-birefringent — the mechanism

In the chiral construction the two photon helicities $\mathbf F^\pm$ were assigned to the two branches independently, so a generic linear polarisation (a superposition of $\mathbf F^+$ and $\mathbf F^-$) acquired a relative phase $\Delta\Omega\,N$ after $N$ ticks and its plane of polarisation rotated — vacuum birefringence. In the **paired** photon there is no single-branch photon: it "only occurs as a pair," always containing both branches symmetrically, so both helicities of the resulting field ride the *one* rate $\Omega_\text{pair}$. The split has nothing to split against. Formally, the birefringence

$$
\Delta\Omega(\mathbf k)=\Omega^+(\mathbf k)-\Omega^-(\mathbf k)
\tag{3.2}
$$

which is non-zero for the chiral law (see §4), never enters the paired-photon evolution because the pair is built symmetrically in $\pm$ from the start.

### 3.3 Massless, luminal, transverse, spin-1

Direct evaluation of (3.1) gives:

- **Massless and luminal:** $\Omega_\text{pair}(0)=0$ and $\Omega_\text{pair}/|\mathbf k|\to0.577350=1/\sqrt3$, with group velocity $d\Omega_\text{pair}/d|\mathbf k|\to1/\sqrt3=c_\text{lat}$ (verified to $7.7\times10^{-6}$ by finite difference; the slope along the body diagonal evaluates to $0.5773503$).
- **Transverse, spin-1:** the field has two transverse polarisations, $|\mathbf E\!\cdot\!\hat{\mathbf k}|/|\mathbf E|=1.8\times10^{-17}$; it is real ($10^{-15}$) and norm-conserving ($6\times10^{-15}$).
- **"Only as a pair":** the pair phase equals the constituent sum $\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ exactly (residual $0$); an unpaired single branch would carry $\Omega^\pm$, which differs (median split $5.3\times10^{-3}$).

The two transverse polarisations and the masslessness together give the photon its spin-1 content without any spin-1 field being fundamental: the spin-1 object is the symmetric combination of two spin-$\tfrac12$ constituents ($\tfrac12\otimes\tfrac12 = 1\oplus0$, with the antisymmetric singlet being the pseudoscalar partner — the pion-channel sibling of Paper XI).

---

## 4. Confrontation with polarimetry: why the chiral photon is excluded

Along the BCC body diagonal $(1,1,1)$ the chiral-law birefringence is, to leading order (expansion of (2.1)),

$$
\Delta\Omega \approx -\frac{\sqrt3}{27}\,k^2,
\qquad
\frac{\Delta v_\phi}{c_\text{lat}} \approx -\frac{k}{18},
\tag{4.1}
$$

i.e. **linear vacuum birefringence** in photon energy ($k\propto E_\gamma/E_\text{Planck}$); it vanishes on the cube axes and is maximal along the body diagonals. Linear birefringence rotates the polarisation angle of light from a distant source by $\Delta\theta\sim\Delta k\cdot d$, and is tightly constrained by GRB and AGN polarimetry (INTEGRAL, *Fermi*/GBM). At the cell size that the gravity sector independently requires (Paper VII; $a=6.5978\,\ell_P=1.07\times10^{-34}$ m), the chiral law overshoots the polarimetry bound by many orders of magnitude — it is excluded precisely at the gravitationally-fixed cell size (Findings F65/F66).

The paired photon (3.1) removes this prediction entirely: there is no helicity split, so a linearly polarised body-diagonal mode shows the symmetric phase $S=\phi_++\phi_-=-1.8\times10^{-15}$ (exactly non-birefringent) where the chiral law gives $S=+0.0792=-\Delta\Omega\,N$. This is the decisive empirical reason the paired photon supersedes the $\sigma$-bilinear as *the* electromagnetic photon (Finding F67).

---

## 5. Three independent routes to the same object

The paired photon is not an *ad hoc* repair. It is forced from three independent directions that now agree:

1. **Observation (§4):** the photon must be non-birefringent $\Rightarrow$ it must ride the helicity-symmetric rate $\Omega_\text{even}$.
2. **$U(1)$ minimal coupling (Paper IV; Finding F68):** the charge-coupling photon is the $U(1)$ *identity channel* $e^{i\theta}\mathbf I$, which acts identically on both helicities — helicity-blind, hence $\Omega_\text{even}$. The general statement (F91) is that the unique identity-channel direction of any neutral coupling $aT_3+bY/2$ is the one proportional to electric charge $Q$; that direction *is* the photon.
3. **Ludwig's notebook (pp. 5–6):** the photon is a bound pair of two $\gamma_{1/2}$, symmetric in $(+,-)$, hence rate $\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)=\Omega_\text{even}$.

All three land on the same dispersion. The notebook's open question "Is there a scalar photon?" (p. 6) is thereby answered: the scalar/identity photon **is** the paired photon, and it is the physical one.

---

## 6. Consistency with the gravity sector

The non-birefringence of the paired photon does more than settle a polarimetry tension: it **restores the cell size the gravity sector requires** (Paper VII). The structural (Sakharov-induced) value of Newton's constant pins the cell at the parameter-free value $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.5978\,\ell_P$ (Finding F79/F107). The chiral photon was falsified *at that very cell size*; the paired photon survives all astrophysical vacuum-birefringence bounds there, with the Lorentz-violation ($n=2$) cutoff at $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV — above the current GRB/LHAASO time-of-flight bounds. The model's dimensionless predictions (Weinberg angle, mass ratios, $c_\text{lat}=1/\sqrt3$, PPN $\beta=\gamma=1$, Mercury precession, factor-2 light bending) are cell-size-independent and unchanged; what the paired photon buys is that the gravity-fixed $a$ is no longer ruled out by the photon sector. This co-certification ties Papers II, VII and VIII together.

---

## 7. Verification summary

| # | Check | Result | Status |
|---|---|---|---|
| PP1 | $\Omega_\text{pair}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)=$ even-law rate (2000 modes) | residual $0$ | exact |
| PP2 | Non-birefringent: linearly polarised body-diagonal mode, 6 ticks | paired $S=-1.8\times10^{-15}$ vs chiral $S=+0.0792$ | machine |
| PP3 | Massless & luminal: $\Omega_\text{pair}/k\to0.57735$, $v_g\to1/\sqrt3$ | err $7.7\times10^{-6}$ | quantitative |
| PP4 | "Only as a pair" (constituent sum vs single-branch split) | residual $0$ | machine |
| PP5 | Spin-1, two transverse polarisations, real, norm-conserving | $\le6\times10^{-15}$ | machine |

Underlying findings: F69 (paired-spinor photon), F67/F68 (even-law vs bilinear; minimal coupling forces the even photon), F65/F66 (helicity–chirality map; all-sky birefringence bound), F37 (RS/BCC chirality), F39 (the retired two-helicity bilinear), F91 (pairing classification theorem).

---

## 8. Discussion

**What is gained.** The photon is now an emergent composite of the lattice's own quanta, with no new fundamental field. Its masslessness, luminality, transversality and — crucially — its exact non-birefringence are all consequences of the symmetric pairing, not inputs. The construction unifies an observational constraint, a gauge-theoretic requirement, and a 2007 notebook conjecture.

**What is retained for other sectors.** The chiral $\sigma$-bilinear is *not* discarded wholesale: it remains the correct *field construction* for the massive and non-Abelian sectors — $W$, $Z$, and gluons (Papers V, VI) — which are massive or confined and carry no astrophysical vacuum-birefringence bound. Indeed the pairing classification theorem (F91) shows the propagator *law* (even vs chiral) is forced sector by sector: $\gamma$ even (forced), $W^\pm$ chiral (forced; left-projector coupling), $Z$ even for its vector part with a mass-suppressed axial split, gluon even (forced; colour coupling is branch-blind).

**Open items.** (i) A genuine two-constituent bound-state simulation of the pair — the "negative binding energy" of the notebook and the massless-pair condition — beyond the present dispersion-level treatment (partly addressed by the bound-state machinery of Findings F73/F74 used in Paper XI). (ii) Whether a clean paired construction exists for the massive sectors.

---

## References

1. L. de Broglie, *Une nouvelle conception de la lumière* (Hermann, 1934); P. Jordan, "Über die Polarisation der Lichtquanten," *Z. Phys.* (1935) — composite (neutrino) theory of light.
2. A. Bisio, G. M. D'Ariano, P. Perinotti, A. Tosini, "Weyl, Dirac and Maxwell quantum cellular automata," (2015).
3. I. Bialynicki-Birula, "Photon wave function," *Prog. Opt.* **36**, 245 (1996) — Riemann–Silberstein vector.
4. P. Laurent *et al.*, "Constraints on Lorentz Invariance Violation using INTEGRAL/IBIS," *Phys. Rev. D* **83**, 121301 (2011); *Fermi*/GBM and INTEGRAL gamma-ray polarimetry constraints on vacuum birefringence.
5. M. Ludwig, *Physics Notes* (2007), pp. 5–6 ("spinor electrodynamics; two $\gamma_{1/2}$ that only occur as a pair").
6. Project findings: F69 (paired-spinor photon), F68 (minimal coupling forces the even photon), F67 (even-law vs bilinear mutually exclusive), F66/F65 (birefringence bounds; helicity–chirality map), F37 (RS/BCC chirality), F39 (two-helicity composite, retired as the photon), F91 (pairing classification).

*Companion papers: I (substrate), IV (electromagnetism), VII (gravity), VIII (black hole / cell-size co-certification).*
