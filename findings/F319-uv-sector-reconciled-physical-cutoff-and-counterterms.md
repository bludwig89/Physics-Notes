# F319 — The UV sector reconciled: a physical Brillouin-zone cutoff and a counterterm program are the same statement, the leading irrelevant operator is dimension-6 with an exact rational coefficient, and the $\Lambda^4$/$\Lambda^2$ Sakharov sectors are **not independently tunable** — which excludes F164's own leading cancellation channel

**Date:** 2026-08-16 - 18:05
**Status:** Confirmed — 21/21 legs PASS, 4/4 controls verified red and red only where declared. Tiering: U5's closed form and U9's ledger/power-counting are **exact-algebraic** (60-digit and sympy-literal); U2/U3/U4 are **machine** ($2.0\times10^{-12}$, $8.4\times10^{-12}$, $1.9\times10^{-14}$); U1/U6/U7/U8 are **computed**. The U8 exclusion is exact in *form* (a 2×2 linear system) and computed in its numbers.
**Module:** `src/casim/engine/interactions/qed_uv_completion.py`
**Registry record:** `F319-uv-completion` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F319_uv_completion.json`
**Addresses:** completeness row **A11** (UV completeness), `PARTIAL` and explicitly *"unmoved for three reports"* in `docs/status/completeness-2026-08-07.md`.
**Cross-references:** [[F264-qed-allorders-renormalizability-anomaly]] (the counterterm program this re-reads; its R1/R8 are re-verified here, not replaced), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the $\Lambda^4$ sector, whose candidate list §C this **reorders**), [[F116-njl-calibration-bz-cutoff-induced-G]] ("the cutoff is the zone, not a knob" — the reading generalised here from the NJL sector to the whole theory), [[F284-rigid-lattice-expansion-and-primordial-state]] ($\Lambda_\text{UV}=3^{-1/4}M_\text{Pl}$, the fixed mode set), [[F59-induced-eh-prefactor-and-f10-selection]] (the $\Lambda^2$ moment $\int d^3k/2\omega$), [[F79-structural-newton-constant]] ($G$ structural — why there is no $G$ counterterm), [[F107-canonical-a-adoption-L4-grb-gate]] (the cell that fixes $\Lambda_\text{UV}$), [[F251-qed-vacuum-polarization-running-alpha]] ($b_0=\tfrac43$ — the scheme-independent half of U3), [[F301-poincare-defect-single-function]] (the $\langle100\rangle$ exactness U5 recovers analytically), [[F69-paired-spinor-photon]] / [[F67-paired-photon-nonbirefringent]] (the propagator U5 expands), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$). External: Wilson & Kogut 1974; Symanzik 1983; Sakharov 1967; Dyson 1952; Hofmann & Müller 2018.

---

## 1. The contradiction, stated as A11 states it

> The BZ edge is a **physical** cutoff, yet F264 runs the full renormalisation program with counterterms on top. F284 §5 sharpens the first picture without reconciling it with the second. Both individually sound, nowhere reconciled.

The row is right that nothing reconciles them, and right that both are sound. What it does not say — because no finding says it — is that the reconciliation is standard, that the tree has never written it down, and that writing it down is not free: it forces two results the model did not know it had.

A grep is the evidence for the middle claim. `wilson` in this repo returns the Wilson gauge **action** (F163, F280) and the Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L$ constant. It never returns Wilson's renormalisation group. `effective field theory`, `irrelevant operator`, `decoupling`, `dimension-6` return nothing at all. The model has been doing Wilsonian physics for 300 findings without the Wilsonian vocabulary, and A11 is where the missing vocabulary shows up as an apparent contradiction.

## 2. The dictionary

**On a physical cutoff there are no divergences, so a counterterm is not a subtraction of an infinity. It is the finite map from bare lattice parameters to measured ones.**

F264's theorem is untouched. $D=4-\tfrac32E_f-E_\gamma$ with $\partial D/\partial V=\partial D/\partial L=0$ is re-derived here in sympy (U9) precisely because this finding *reinterprets* it, and a reinterpretation that quietly assumed its own premise would be worth nothing. What changes is the reading:

| | continuum QED | this model |
|---|---|---|
| $D\ge0$ means | the amplitude **diverges** | the amplitude is **$\Lambda$-sensitive**, and finite |
| $Z_1,Z_2,Z_3,\delta m$ are | subtractions of infinities | finite bare→measured reparametrisations |
| the theorem says | finitely many counterterms suffice | finitely many operator coefficients carry the cutoff |
| $D<0$ means | the amplitude is finite | the amplitude is suppressed by $(E/\Lambda_\text{UV})^{|D|}$ |
| what is universal | the $\ln$ coefficient | the same $\ln$ coefficient |
| what is convention | the subtraction scheme | the lattice action |

The second column is strictly *stronger* than the first, and entirely finite. So F264 is not running a program "on top of" the cutoff; F264 is computing the only observable content the cutoff has at accessible energies. §5 measures how little that is.

The rest of this finding is that table made checkable, plus the two things it forces.

## 3. The licence: scheme differences are IR-blind (U1–U4)

The dictionary is only legitimate if a counterterm fitted in one regularisation absorbs the cutoff-dependence of another. That is a property, not a definition, and it is measurable. The one-loop log structure is evaluated in the Schwinger representation, which turns the 4-D zone integral into a 1-D one:

$$I_\text{lat}(m)=\int_0^\infty\!dt\;t\,e^{-tm^2}D(t)^4,\qquad D(t)=\int_{-\pi}^{\pi}\frac{dk}{2\pi}e^{-t\hat k^2(k)}$$

**U1 — the lattice loop is finite; the continuum one is not, from the same integrand.** $I_\text{lat}$ is a number. The hard-sphere continuum integral at the same $m$ grows without bound in $\Lambda$, at the measured rate $2\ln10^3/16\pi^2$ per three decades (matched to $<10^{-6}$). Same integrand, compact domain versus non-compact.

**U2 — the lattice-minus-continuum constant is IR-independent.** Referenced against Pauli–Villars (exact: $I_\text{PV}=\ln(M^2/m^2)/16\pi^2$), the Wilson scheme constant over a six-decade mass ladder:

| $m$ | $10^{-1}$ | $10^{-2}$ | $10^{-3}$ | $10^{-4}$ | $10^{-5}$ | $10^{-6}$ |
|---|---|---|---|---|---|---|
| $\lim I_\text{lat}+\ln m^2/16\pi^2$ | 0.0238929 | 0.0240113 | 0.0240132 | 0.02401318 | 0.024013181 | 0.024013181 |

Drift over the last decade **$2.0\times10^{-12}$**. The difference between a compact-BZ regulator and a continuum one does not know about the infrared. *That* is what licenses one counterterm to absorb the other, and it is the whole content of "F264 is legitimate on a physical cutoff".

**U3 — the $\ln$ coefficient is universal; the constant is not.** The coefficient is read off the kernel without integrating: $I\sim c\ln(1/m^2)$ iff $P(t)=D(t)^4\to c/t^2$, so $c=\lim t^2P(t)$, which depends only on $D(t)\to(4\pi t)^{-1/2}$ — fixed by $\hat k^2\to k^2$, which *every* regulator in the class satisfies because that is what makes it a regulator.

| scheme | $c$ | rel. err vs $1/16\pi^2$ |
|---|---|---|
| BZ lattice, Wilson | $6.332590\times10^{-3}$ | $2.5\times10^{-6}$ |
| BZ lattice, Symanzik-improved | $6.3325740\times10^{-3}$ | $8.4\times10^{-12}$ |
| Pauli–Villars | $1/16\pi^2$ | exact (sympy) |
| dimensional, $\overline{\rm MS}$ | $1/16\pi^2$ | exact (sympy) |

(The Wilson residual is its own $0.25/t$ approach to the asymptote — the unimproved action is further from the continuum at the probe, which is what "unimproved" means.) So $b_0=\tfrac43$ (F251) is physics and the constant is bookkeeping. That split *is* the renormalisation group, and it is why the model can have both a physical cutoff and a meaningful $\beta$ function.

**U4 — the scheme dependence is a constant computable at literally $m=0$.** Two lattice actions share the leading $(4\pi t)^{-2}$, so their difference integrand decays as $t^{-2}$ and converges with **no infrared regulator at all**:

$$\Delta_{\rm W-S}=\int_0^\infty\!dt\,t\,[P_\text{W}(t)-P_\text{S}(t)]=8.30668156\times10^{-3}$$

against $8.30668156\times10^{-3}$ from the $m$-ladder route — two independent computations agreeing to **$1.9\times10^{-14}$**. Not "the $m$-dependence cancels to some tolerance": $m$ never appears.

## 4. The leading irrelevant operator is dimension-6, and its coefficient is exact (U5)

For the F69 paired-spinor photon — the propagator the model actually runs — the deviation from linear dispersion is

$$\boxed{\;\frac{\Omega_\text{pair}(k)-c_\text{lat}\lvert k\rvert}{c_\text{lat}\lvert k\rvert}\;=\;-\Big[\frac{1-\sum_i\hat n_i^4}{144}+\frac{\hat n_x^2\hat n_y^2\hat n_z^2}{24}\Big]\lvert k\rvert^{2}\;+\;O(\lvert k\rvert^{4})\;}$$

verified against the F26 symbol to **$1.1\times10^{-20}$** over nine directions in 60-digit arithmetic, and against the shipped float64 `pair_dispersion` to $1.1\times10^{-7}$ (that residual is `arccos` conditioning at the probe, not physics — both legs are reported so the distinction is visible rather than averaged away).

Three things follow, and the first is the load-bearing one.

- **There is no $O(\lvert k\rvert)$ term — the model has no dimension-5 Lorentz-violating photon operator at all.** Measured as a scaling *exponent* ($p=2$ to $<10^{-4}$) rather than a small number, because a small number at one $\lvert k\rvert$ is consistent with a small dim-5 coefficient whereas $p=2$ excludes the operator. This is the phenomenologically decisive one: dim-5 photon LV is bounded near $10^{-30}$ by GRB/AGN polarimetry, which is the same bound that killed the $\sigma$-bilinear photon (F65–F67). The paired photon does not merely *pass* it — the operator is absent, because $\Omega_\text{pair}$ is even in the branch label by construction.
- **The coefficient is bounded exactly:** the two cubic invariants are extremised together, so the range is $[-\tfrac1{162},0]$ — $-1/162$ along $\langle111\rangle$, and identically $0$ along $\langle100\rangle$, where $q_y=q_z=0$ makes $\Omega=2\arccos(\cos q_x)$ **linear to all orders**. That recovers F301's $\langle100\rangle$ result ($3.5\times10^{-46}$) analytically rather than numerically.
- **The coefficient is $O(10^{-2})$ and rational.** No tuning, no hierarchy, no free parameter — the leading irrelevant operator's Wilson coefficient is a number the lattice geometry hands over.

## 5. Decoupling, and why nobody can see any of this (U6–U7)

With $\Lambda_\text{UV}=\hbar c/a=1.8504\times10^{18}$ GeV at the F107 cell, $\lvert k\rvert_\text{lat}=E/\Lambda_\text{UV}$ and the §4 bound gives the maximum fractional deviation from continuum dispersion:

| scale | $E$ | $\lvert k\rvert_\text{lat}$ | max fractional deviation |
|---|---|---|---|
| $m_e$ | $511$ keV | $2.8\times10^{-22}$ | $4.7\times10^{-46}$ |
| $M_Z$ | $91.19$ GeV | $4.9\times10^{-17}$ | $1.5\times10^{-35}$ |
| LHC | $13$ TeV | $7.0\times10^{-15}$ | $3.0\times10^{-31}$ |
| LHAASO | $1.4$ PeV | $7.6\times10^{-13}$ | $3.5\times10^{-27}$ |

And the theory stays weakly coupled across its entire domain: running $\alpha$ from $m_e$ with F251's $b_0=\tfrac43$, $\alpha(\Lambda_\text{UV})=0.00791$, while the Landau pole sits at $10^{277.2}$ GeV — **258.9 decades above the zone edge**, outside the theory's domain of definition (re-verifying F264 R8 against the constants registry rather than re-asserting it). QED triviality is not solved here; it is *not applicable*, because the theory is defined with a cutoff and never asked to be continued past it.

**So the reconciliation is not merely consistent — it is forced.** At every energy anyone can reach, the cutoff's own residue is $\le10^{-27}$, which is far below every measurement F251–F264 compare against. The continuum counterterm program is not an approximation the model tolerates; over the accessible domain it is the model's exact content to 27 significant figures, and the physical cutoff's only observable consequences are the two coefficients of §7.

## 6. The result that costs something: the two Sakharov sectors are locked together (U8)

F164 gives three candidate resolutions of its 120.8-order cosmological-constant overshoot and calls **channel (i)** — *"the CA ontic vacuum is a single configuration; applying the rotation rule to the zero configuration costs nothing, so the CA ground-state energy is exactly zero by construction"* — the leading, elegant-design-preferred one. It is stated there as "a position, not a calculation."

Do the calculation and it fails, on the model's own arithmetic.

F59 Part A assembles $1/(16\pi G)$ from $\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{1}{2\omega}$. F164 Part A assembles $\rho_\text{vac}$ from $\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{\omega}{2}$. **Same modes, same measure, same factor of $\tfrac12$** — they are two moments of one zero-point sum, the $a_0$ and $a_1$ coefficients of one heat-kernel expansion. Computing them in one function over one grid (which is why `sakharov_moments` returns both) makes that impossible to overlook: $I_\text{cc}=4.0810486$ (reproducing F164's $4.081$ independently) and $I_g=1.9807020$.

Weight the sum by a uniform $\lambda$ and **both** move. Because they carry different powers of the cell,

$$\frac{1}{16\pi G}\sim\frac{\lambda}{a^{2}},\qquad \rho_\text{vac}\sim\frac{\lambda}{a^{4}},$$

demanding the measured $G$ **and** the measured $\rho_\Lambda$ is a 2×2 system with a unique solution:

$$\boxed{\;a^\star=a_0\sqrt{\rho_\text{vac}/\rho_\Lambda}=2.559\times10^{26}\ \text{m}\;(8.29\ \text{Gpc}),\qquad \lambda^\star=5.76\times10^{120}\;}$$

A lattice cell $0.58\times$ the comoving radius of the observable universe, and a zero-point weight 121 orders **above** the canonical $\tfrac12$. Note the sign: $\lambda^\star$ is an *enhancement*. Suppressing the mode sum to fix the CC makes $G$ worse; re-fixing $G$ by shrinking $a$ makes the CC worse again. **The two sectors pull opposite ways, and the uniform channel is not disfavoured — it is over-determined into absurdity.**

This is a genuine cost. F164's preferred escape is closed, and the reason is the model's own successful derivation of $G$: *you cannot delete the zero-point sum without deleting F79.*

### What survives, and the number A11 still owes

The exclusion is of the **uniform** class. What it leaves is a sharp requirement on any survivor: the mechanism must be **order-selective in the heat-kernel expansion** — suppress $a_0$ by $\ge120.8$ decades while perturbing $a_1$ by $\le2.2\times10^{-5}$ (CODATA's relative uncertainty on $G$). That is a required relative selectivity between two *adjacent* heat-kernel coefficients of

$$\ge1.27\times10^{116}.$$

F164's **channel (ii)** — sequestering through the $AB\equiv1$ dielectric — is order-selective by construction: it removes the *constant* piece of $T^{00}$ from the source while leaving the curvature response. Channel (iii) was already labelled a consistency statement rather than a cancellation. So on the model's own arithmetic **channel (ii) is promoted to sole survivor**, and this finding reorders F164 §C accordingly.

## 7. The $\Lambda$-sensitivity ledger — what A11's residual actually is (U9)

Enumerating every operator with $D\ge0$ in the *full* theory, gravity included, and asking of each whether the model has a free parameter to absorb its cutoff-dependence:

| operator | dim | $D$ | free parameter? | disposition |
|---|---:|---:|---|---|
| identity (cosmological constant) | 0 | 4 | **no** | **UNABSORBABLE** — F164's 120.8 orders |
| $R$ (Einstein–Hilbert, $1/16\pi G$) | 2 | 2 | **no** | **UNABSORBABLE** — and the induced value *is* the prediction, and it lands (F79/F107) |
| $A_\mu A^\mu$ (photon mass) | 2 | 2 | no | **forbidden**, not unabsorbable — $q_\mu\Pi^{\mu\nu}=0$ exactly (F251/Pi1) |
| $\bar\psi i\gamma\!\cdot\!\partial\psi$ | 4 | 0 | yes | absorbed ($Z_2$) |
| $e\bar\psi\gamma\!\cdot\!A\psi$ | 4 | 0 | yes | absorbed ($Z_1$) |
| $m\bar\psi\psi$ | 4 | 0 | yes | absorbed ($\delta m$) |
| $F_{\mu\nu}F^{\mu\nu}$ | 4 | 0 | yes | absorbed ($Z_3$) |
| dim $\ge6$ | 6 | $-2$ | — | irrelevant; coefficient measured exactly in §4 |

**Exactly two coefficients have no free parameter to absorb them, and they are precisely the two Sakharov sectors F59 separated by their $\Lambda$-scaling.** The model gets one right and one wrong. That is the whole of A11:

> UV completeness is not "partly reconciled". The model **is** UV-finite (no divergences, no Landau pole in domain, a fixed mode set, $2.1\times10^{180}$ cells in the Hubble volume — F284). Its residual is **one number**, $\rho_\text{vac}$, overshooting by $10^{120.76}$; and §6 now says what the closing mechanism must look like and how selective it must be.

Two remarks on the count, because both are load-bearing. First, the four QED counterterms are an **upper bound on the model's UV freedom, not a fixed cost**: $m_0$ and $e$ are free *at the level of the QED sector's own accounting*, and the model separately attempts to derive them (F116 §6 for $m_0$, F115/F251 for $e$). Every counterterm derived elsewhere is one fewer free parameter, so this ledger tightens as the rest of the tree lands. Second, the photon-mass row is a different kind of entry and must not be counted as a success of absorption: nothing absorbs it, it is *forbidden* by exact transversality.

## 8. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $D=4-\tfrac32E_f-E_\gamma$, $\partial_VD=\partial_LD=0$ | **exact** (sympy, literal 0) — re-verified, F264's |
| $\ln$ coefficient $=\lim t^2P(t)=1/16\pi^2$, PV and dim-reg closed forms | **exact** (sympy) |
| $\delta\Omega/\Omega=-[(1-S_4)/144+T^2/24]\lvert k\rvert^2$; range $[-\tfrac1{162},0]$; $\langle100\rangle$ linear to all orders | **exact-algebraic** ($1.1\times10^{-20}$, 60 dps) |
| no dimension-5 photon operator (exponent $p=2$) | **exact in form**, measured to $10^{-4}$ |
| IR-independence of the scheme constant | **machine** ($2.0\times10^{-12}$) |
| two independent routes to $\Delta_{\rm W-S}$ | **machine** ($1.9\times10^{-14}$) |
| $\Lambda_\text{UV}=1.8504\times10^{18}$ GeV; decoupling table; $\alpha(\Lambda_\text{UV})$; 258.9-decade Landau gap | **computed** |
| $I_\text{cc}=4.0810486$, $I_g=1.9807020$, overshoot $10^{120.76}$ | **computed** (reproduces F164 independently) |
| $a^\star$, $\lambda^\star$, and the exclusion of the uniform channel | **exact in form** (2×2 linear system), **computed** in value |
| required order-selectivity $\ge1.27\times10^{116}$ | **computed** |
| An order-selective mechanism that actually delivers it | **OPEN** — the one thing A11 still owes |

## 9. Honest scope

- **§3 uses the hypercubic $\hat k^2$, not the BCC symbol.** Deliberately: the claim is about the *class* of compact-BZ regulators, and it is demonstrated by exhibiting four members of the class (two lattice, two continuum) agreeing on the log and disagreeing on the constant. Redoing it on the BCC symbol would produce a fifth constant and change no conclusion. What it would add is the BCC value of that constant, which nothing currently needs.
- **§6's exclusion is of the *uniform* class only.** A mechanism with any dependence on the heat-kernel order escapes it — that is precisely why channel (ii) survives, so the restriction is the useful part rather than a hedge. What is *not* shown is that channel (ii) actually delivers $10^{116}$ of selectivity; it is shown to be the only candidate of the three that is the right *shape*.
- **§6 also assumes the two moments carry the same $g_*$ and the same $\eta$-type prefactor up to $O(1)$.** They do in F59/F164 as written. An $O(1)$ error changes $a^\star$ by an $O(1)$ factor and changes nothing about a 121-order exclusion.
- **The lattice does not fix Dyson's asymptotic series.** Removing UV divergences is not the same as making perturbation theory convergent; Dyson's 1952 argument is about the instability of the vacuum at $e^2<0$ and is untouched by a cutoff. The model's QED is UV-finite order by order and still only asymptotic in the sum. Nothing here claims otherwise.
- **U6 assumes the dim-6 coefficient of §4 bounds the whole dim-6 sector.** It is the photon-dispersion coefficient specifically. Other dim-6 operators (four-fermion, $F^3$) are not computed here; power counting puts them at the same $(E/\Lambda_\text{UV})^2$ suppression, and that suppression is $10^{-31}$ at LHC, so the conclusion is robust to $O(1)$ or even $O(10^{10})$ coefficient differences — but the *coefficients* are not measured.
- **§7's "free parameter?" column is a judgement about the model's structure, not a theorem.** It is stated operator by operator so it can be disagreed with row by row.

## 10. Falsifiers

1. **A scheme in the compact-BZ class returning a different $\ln$ coefficient.** Would break U3 and with it the claim that $b_0$ is physics. The kernel argument says this is impossible for any regulator with $\hat k^2\to k^2$; a counterexample would mean the model's regulator is not in the class.
2. **A measured IR-dependence of the lattice-vs-continuum constant.** Would remove the licence for F264's counterterms and re-open A11 as originally stated.
3. **Detection of dimension-5 photon Lorentz violation.** §4 says the operator is absent, not small. Any nonzero $O(\lvert k\rvert)$ dispersion term falsifies the paired photon's evenness.
4. **A dispersion measurement contradicting $-[(1-S_4)/144+T^2/24]$ at $O(\lvert k\rvert^2)$.** Requires $E\sim\Lambda_\text{UV}$, so this is not a terrestrial falsifier; it is recorded because the coefficient is a genuine prediction, not a fit.
5. **A uniform-$\lambda$ mechanism that fixes the CC without moving $G$.** Would falsify §6. It cannot exist as stated — the two sectors carry different powers of $a$ — so a claimed counterexample is a claim that F59's $\Lambda^2$ or F164's $\Lambda^4$ assignment is wrong.
6. **A derivation of $\rho_\Lambda$ from an order-selective mechanism.** Would *close* A11 rather than falsify this, and is the outcome this finding is trying to make reachable.

## 11. Files

- Module: `src/casim/engine/interactions/qed_uv_completion.py`
- Test: registry record `F319-uv-completion` in `tests/registry/interactions.yaml`
- Results: `test-results/F319_uv_completion.json`
