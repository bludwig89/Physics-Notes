# Review of `physics-notes-complete.md` — Model Support, Falsifiers, Improvements

**Date:** 2026-05-27 - 22:50
**Reviewer:** assistant
**Scope:** Full re-read of the 3,362-line transcribed notebook (pages 1–182) against current model state (findings F16–F42, `key-decisions.md`, `findings.md`, `exactness-inventory.md`, and existing CA modules).
**Goal:** Identify elements that (a) **support** the CA / Higgs-free / chiral-SU(2) model, (b) **falsify** or pressure-test it, or (c) suggest **improvements** that have not yet been captured in findings.

---

## 1. Summary verdict

The notebook is broadly consistent with the present model and contains four kinds of material:

1. **Hard support for current findings.** Several pages are the direct source for F25–F27, F35, F38, F41, F42 and remain the canonical motivation for the project's three key decisions (composite photon, $c_\text{lat}$ as rotation rate, Higgs-free chiral SU(2)).
2. **Notebook items not yet captured as findings but worth promoting.** The strongest are the helical-rotation effective-velocity construction (pp.73–74), the "$A$ ↔ spin, $W$ ↔ isospin" duality (pp.67, 71), the lepton-octet anomaly bookkeeping table (pp.89–90, 92–97), the Majorana neutrino-mass option (p.76), and the longitudinal-only constraint on the Weyl-on-null-vector reduction (pp.161–175, p.3201).
3. **Specific calculations that conflict with the present implementation and require reconciliation.** Two stand out: (i) the page 65–66 derivation of $m_Z$ produces an "anomalous" cross term $m_Z^2\,W_0\!\cdot\!W_3$ and gives $m_Z^2 = m_W^2 \cos^2\theta_W + m_{W_0}^2 \sin^2\theta_W$, **not** the $m_Z = m_W/\cos\theta_W$ relation used in F35; (ii) the page 70 "factors of 2" problem in the kinetic terms for the two-doublet Higgs-free Lagrangian. Both need an explicit reconciliation note tying the notebook's bare construction to the corrections made in F34b (Stueckelberg) and F35 (mass matrix derivation).
4. **Numerical speculations and dead ends already correctly classified as such by the author.** E.g. p.73 "way way — no good", the p.90 "Could $Z$ be a bound state of $W^+W^-$? Energies just don't work out." These are useful negative evidence (do not chase them) and are listed below to make the negative call explicit.

There are **no items that outright falsify** any current confirmed finding. There are **two items that constrain it** (sections 3.1 and 3.2 below) and **at least five concrete improvements** that should be folded into the model.

---

## 2. Support for the model — page-by-finding mapping

| Notes pages | Content | Finding(s) supported | Status |
|---|---|---|---|
| pp.5–6 | Composite photon: two correlated spin-½ "spinor photons" exchanged in an X-configuration, behaving like a single boson "that only occurs as a pair." | F18, F25, F39 ("De Broglie composite photon" — `key-decisions.md` item 1) | Confirmed |
| p.35 | "Dependence implies neighborhood. Rules imply geometry." Foundational CA principle. | The entire CA framework | Foundational |
| p.36 | Connection number → dimensionality; specifically 4-connection lattices "form 2D or 3D lattices or 3D tubes/torus." | BCC nearest-neighbour choice (`ca_bcc.py`) | Foundational |
| pp.37–39 | Spinor-valued Weyl CA, explicit discrete update; author observes "the factor needed to keep it at unity… has to do with the speed of light; a ½ gives $c=1$." | F25, F26 (the factor-of-2 is the very $c_\text{lat}=1/\sqrt3$ relation later proved exactly); split-step note dated 2026-05-13 already validates this. | Confirmed |
| pp.59–60 | "Complex mass" — gauging $\beta$ via $U = \mathrm{diag}(1, e^{i\theta(x)})$ produces a local SU(2) symmetry acting only on one chirality. | F27 (canonical source — `key-decisions.md` item 3), F40, F41, F42 | Confirmed and implemented |
| pp.62–67 | Weinberg–Salam **without Higgs**; explicit Lagrangian with both $L$- and $R$-doublets retained; introduction of an "$A_\mu$ ↔ isospin, $W_\mu$ ↔ spin" duality. | F35 (electroweak mixing), F41 (hypercharge Higgs-free) | Confirmed for the mixing structure; the duality observation has not yet been folded into a finding (see §4.2). |
| pp.85–90 | Plane-wave Weyl spinor reconstruction with explicit "right particle / left particle / right antiparticle / left antiparticle" classification. | F37 (RS-BCC chirality/helicity), F39 (two-helicity photon bilinear) | Confirmed |
| pp.92–97 | The 8-state lepton vector $(e_R^-, e_L^+, e_R^+, e_L^-, \nu_R, \bar\nu_L, \bar\nu_R, \nu_L)$ — explicitly **keeps** $\nu_R$ and $\bar\nu_L$. | F37, F38 (FG-1 anomaly cancellation, where keeping the right-handed neutrino is structurally needed). | Confirmed |
| pp.103–104 | Neutral charge operator $Q' = t_3\cot\theta_W - t_0\tan\theta_W$ with experimental $\sin^2\theta_W = 0.232 \pm 0.009$. | F35 W6.4 (Gell-Mann–Nishijima) | Confirmed |
| pp.110–124 | Spinor as a direction-without-magnitude; stereographic projection; null vectors and the topological reason a spinor needs two components. | F26, F37 (geometric interpretation of the Weyl spinor field) | Confirmed |
| pp.141–160 | $V^\mu\,\partial_\nu V_\mu = 0$ and $\vec V\cdot\partial_\mu \vec V = 0$ as light-cone and unit-length constraints. | F24 (SL(2,C) boost / 4-current covariance), F25 | Supports the underlying covariance structure |
| pp.161–175 | Weyl operator acting on a quaternion $\sigma^\mu V_\mu$ yields source-free Maxwell equations — both Gauss laws and both curl laws, with $V_0$ as an "ancillary field." | F25 (real-rotation exact discrete-time Maxwell) | Confirmed — the notebook is the conceptual source of F25. |

**Net:** the notebook is the most concentrated single source of motivation for F25, F26, F27, F35, F37, F38, F41 — i.e. for every "key decision" except the choice of BCC topology itself.

---

## 3. Items that constrain the model (potential falsifiers / pressure points)

### 3.1 The page 65–66 $m_Z$ derivation differs from F35 by an "anomalous" cross term

The notebook derives
$$\mathcal L_{m_{30}} \supset \tfrac12 m_W^2 (W_3\cos\theta - A\sin\theta)^2 + \tfrac12 m_{W_0}^2 (W_3\sin\theta + A\cos\theta)^2$$
which expands to
$$m_Z^2 = m_W^2 \cos^2\theta + m_{W_0}^2 \sin^2\theta,\qquad m_A^2 = m_W^2 \sin^2\theta + m_{W_0}^2 \cos^2\theta,$$
**plus a cross term** $\mathcal L_\text{Anom} = m_Z^2\,W_{0\mu}W_3^\mu$ that the author flags but does not resolve: "what happens to it? Presumably, it is transformed away or hidden somehow." Page 66 then forces $m_A = 0$ by hand and recovers the SM relation $m_Z^2 = m_W^2/\cos^2\theta_W$ only **as a consistency requirement**.

F35 (W6.3) treats the analogous result as an algebraic identity from $m_W = gv/2$, $m_Z = (v/2)\sqrt{g^2+g'^2}$, i.e. it presumes the SM mass-matrix structure that the notebook is explicitly trying to **derive**. In the Higgs-free model the bare mass term $\tfrac12 m_W^2 \vec W\!\cdot\!\vec W + \tfrac12 m_{W_0}^2 W_0\!\cdot\!W_0$ is exactly what F34b's Stueckelberg construction produces — and Stueckelberg implies $m_W$ and $m_{W_0}$ are **independent inputs**, *not* coupled by a single Higgs VEV.

**Implication / action item:** (To Test) in the Higgs-free model, F35's "exact" $m_Z/m_W = 1/\cos\theta_W$ holds **only if we additionally impose $m_A = 0$** (i.e. require the diagonalised photon to remain massless). This is a non-trivial constraint that is not automatic in the Stueckelberg-only construction, and the cross term $m_Z^2 W_0 W_3$ from page 65 needs an explicit reconciliation. Suggest a new finding `F43-higgs-free-mz-mw-constraint.md` that proves the $m_A = 0$ requirement is consistent with the F34b Stueckelberg masses and shows where the cross term is absorbed (probably into the off-diagonal of the W6.1 rotation, which is why mix∘unmix = identity to $10^{-16}$ in F35).

### 3.2 The page 70 "factors of 2" in the Higgs-free kinetic terms

The notebook writes out the kinetic terms for the simultaneous $(e_R, e_L)$ EM doublet **and** the $(\nu_L, e_L)$ weak doublet — both of which contain $e_L$ — and finds:
$$\binom{i\bar\sigma_\mu \partial^\mu e_R + 2i\sigma_\mu \partial^\mu e_L + \cdots}{2i\sigma_\mu \partial^\mu e_R + \cdots}$$
i.e. *the field that participates in both doublets picks up a factor of 2 in its kinetic term.* The author notes "this is becoming an ugly way to write equations of motion" and switches to a quadruplet $(e_L, e_R, \nu_L, \nu_R)$ representation — but the factor-of-2 problem is not actually resolved in the notebook.

The present code (`ca_dirac.py`, `ca_wmu.py`, `ca_hypercharge.py`) appears to organise fields so that this never arises — each Weyl species has exactly one kinetic step per tick — but the **reason** that this is allowed in the Higgs-free model is not stated in any finding. The notebook is the explicit warning that naive Lagrangian addition of L- and R-doublet kinetic terms double-counts the shared $e_L$ field.

**Implication / action item:** (To Test) add a short note to F41 or F42, or as `F44-higgs-free-kinetic-no-double-count.md`, that records: (i) the bare additive Lagrangian double-counts $e_L$; (ii) the resolution adopted in `ca_dirac.py`/`ca_wmu.py` is to label each Weyl field by its full $(SU(2)_L, SU(2)_R\!\sim\!I, U(1)_Y)$ identity and apply *one* kinetic step that carries the appropriate covariant derivatives. A unit test that recomputes the kinetic energy from the notebook's naive sum and from the implementation, and shows the implementation's value is consistent with $E^2 = p^2 + m^2$ for each Weyl species, would discharge this.

### 3.3 Page 161–175: Weyl-on-null-vector forces longitudinal-only solutions

Pages 161–175 derive Maxwell-like equations by acting with $\sigma^\mu\partial_\mu$ on a quaternion $\sigma^\mu V_\mu$ that is null and unimodular, and at the end (p.3201 in the transcription) state explicitly: "A pure transverse wave, e.g., $\vec V = v\hat x\,e^{i(kz-\omega t)}$, has $\partial_z V_x \neq 0$ but $\partial_x V_z = 0$, so it is **not allowed**. One way or another, this drives us to a **pure longitudinal wave**."

This is a structural statement about the *Weyl-acting-on-a-single-spinor* reduction, not about the composite-photon bilinear $G_T = (\mathbf E, \mathbf B)$ that F25/F30 study (where transverse polarisations are exactly what propagates). But it does mean **the single-spinor reduction is not the photon** — the photon is the *bilinear* of two spinor fields, which restores transversality. F39 (two-helicity photon bilinear) already states this implicitly; F25 makes it explicit at the level of the rotation generator.

**Implication / action item:** this is not a falsifier, but it **is** a warning sign that any future attempt to identify the photon with a single (rather than bilinear) Weyl field will fail at the level of polarisation content. Worth a one-paragraph note in F25 or F39 citing pages 161–175 explicitly so that future readers do not redo this work.

### 3.4 Page 73 helical-mass picture: author's own rejection should be revisited

The notebook proposes that "mass" is the effect of a particle's trajectory being a helix rather than a straight line, giving $v_\text{eff} = \sqrt{c^2 - 4\pi^2\nu^2 r^2}$. After plugging in $\hbar\omega = E$, $E^2 = p^2 c^2 + m^2 c^4$ the author derives $v^2 = c^2 - E_0^2/E^2$ and writes "**Way way — no good.**" because $v\to c$ as $E\to\infty$ rather than recovering Newtonian behaviour at low energy.

The author's rejection is **wrong** by present understanding: $v\to c$ as $E\to\infty$ for a massive particle is exactly the correct relativistic result; the issue was that the author was comparing to a Newtonian intuition $v_\text{eff} \to 0$ for high $\omega$. In our framework F26 already says $c$ is a rotation rate, and the helical picture is essentially a real-space realisation of F26's "phase-velocity = rotation rate" idea applied to the *fermion* (not the photon). The picture
$$c^2 = v_\text{eff}^2 + (2\pi\nu r)^2$$
is exactly the lattice Pythagorean decomposition $c_\text{lat}^2 = v_\text{group}^2 + v_\text{rotation}^2$ that should hold for any massive Weyl mode in a chiral SU(2) gauged background (F27).

**Implication / action item:** the helical decomposition is *not* a falsifier — it is a candidate **new finding**. See §4.4 below.

### 3.5 Page 90 "Could Z be viewed as a bound state of $W^+W^-$?"

The notebook records "One would certainly think so. Energies just don't work out." This is a negative result for one of the more intuitive composite-vector-boson hypotheses, and means: do not pursue $Z = W^+W^-$ as a bound state. The author's "energies just don't work out" intuition is correct ($m_Z < 2m_W$, so $Z$ cannot be on-shell two $W$s). The CA model should respect this and treat $Z$ as the F35 linear combination, not a bound state.

**Implication:** no action; documenting this here so the negative call is explicit and we do not waste cycles exploring it.

### 3.6 Page 79 "Maybe we should let $W^\pm$ exist but not $Z$"

Speculation in the notes. The current model uses $Z$ as a derived (mixed) state, which is the standard SM resolution and is exactly what F35 implements. Negative speculation; no action.

---

## 4. Improvements (concrete additions / refinements to the model)

### 4.1 Promote the "8-state lepton vector + neutral-state correspondence" to an organising principle

Pages 89–97 present an extended classification:

| State | EM-charged | W-charged |
|---|---|---|
| $e_R^-, e_L^+$ | yes | no |
| $e_R^+, e_L^-$ | yes | yes |
| $\nu_R, \bar\nu_L$ | no | no |
| $\bar\nu_R, \nu_L$ | no | yes |

and observes: "These neutral states correspond to a 'missing' charge state. The right-handed weak interaction does not exist, and neither does the magnetic monopole." This is a **principle** — that the absence of right-handed weak and absence of magnetic monopole are the same fact in the L/R-symmetric lepton octet — and it is **not** stated in any current finding. It is also a natural complement to F38's anomaly-cancellation table.

**Suggested action:** (To Add) add to F38 (or as a stand-alone `F45-lr-symmetric-lepton-octet.md`) a section that records this correspondence and identifies the four "neutral" states with the missing channels of (right-handed weak, magnetic monopole). This may also tighten F37's RS-BCC chirality/helicity bookkeeping by giving a single 8-state object to gauge.

### (To Test) 4.2 Capture the "$A_\mu \leftrightarrow$ spin, $W_\mu \leftrightarrow$ isospin" duality

Pages 67 and 71 observe:
> "$A_\mu$ works on the isospin vector just like $W$ works on the spin vector."

i.e. for the L-doublet, $A$ couples through $\tfrac12(\tau_0+\tau_3)$ acting on isospin, while $W^3$ couples through $\tfrac12(\sigma_0+\sigma_3)$ acting on spin. This is a *manifest* duality between the two interactions and may be the source of the Weinberg-angle rotation in F35 — i.e. the Weinberg angle could be derivable from the geometry of the $\sigma \leftrightarrow \tau$ exchange rather than fit to experiment.

**Suggested action:** before next test pass on `ca_wmu.py`, attempt to derive $\sin^2\theta_W$ directly from the $\sigma \leftrightarrow \tau$ swap geometry on the BCC lattice. Even if the result is $\sin^2\theta_W = 1/4$ (the symmetric value, which is ~7% off the experimental 0.232), that would be a *prediction* rather than a fit — a much stronger statement than F35 currently makes. Note F35 explicitly treats $\theta_W$ as an input parameter.

### (To Test) 4.3 The page 104 hypothetical $\sin^2\theta_W = 2/9 = 0.222\overline 2$

The notebook records: "What if coupling to $W^\pm = 3e$ exactly? Then $\sqrt2/\sin\theta_W = 3 \Rightarrow \sin\theta_W = \sqrt 2/3$, $\sin^2\theta_W = 2/9 = 0.222\overline 2$." Experimental value is $0.232 \pm 0.009$; $2/9$ is $\sim 1.1\sigma$ low.

**Suggested action:** this is a specific algebraic-rational prediction that could be tested. Either (i) derive $\sin^2\theta_W = 2/9$ from the F35 mixing geometry (in which case the 1.1σ low value is a real prediction of the model and a candidate falsifier of the SM-input $\sin^2\theta_W = 0.232$ that F35 currently consumes), or (ii) prove $\sin^2\theta_W$ is *not* fixed by the BCC geometry and is a free parameter. Either outcome materially sharpens the project's predictive content.

### (Running) 4.4 Helical effective velocity → new finding "F46 — Pythagorean lattice mass decomposition"

As noted in §3.4, the helical-motion construction of pp.73–74 is structurally identical to F26's rotation-rate interpretation of $c_\text{lat}$, applied to a *massive* mode. The notebook's $c^2 = v_\text{eff}^2 + (2\pi\nu r)^2$ should hold for the BCC Weyl dispersion in the form
$$c_\text{lat}^2 = \left(\frac{d\Omega}{d|\mathbf k|}\right)^2 + \Omega_\text{rest}^2,$$
where $\Omega_\text{rest}$ is the cyclic rotation rate of the η↔χ mass step (F27) at $|\mathbf k| = 0$.

**Suggested action:** verify numerically that $\Omega_\text{rest}(m)$ derived from F27's mass step satisfies the lattice-Pythagorean relation against the F30 dispersion. If the relation holds to machine precision, this is a new exact finding linking F26 (photon rotation rate) and F27 (mass rotation rate) and provides a *geometric* derivation of $E^2 = p^2 c^2 + m^2 c^4$ rather than an algebraic one. This would belong on the Tier-1 exact row of `exactness-inventory.md`.

### (To Test) 4.5 Add a Majorana option to the neutrino sector

Page 76 records:
$$\mathcal L_\text{Maj} = M_D \bar\psi_L\psi_R + \tfrac12 M_L \bar\psi_L(\psi_L)^c + \tfrac12 M_R \bar\psi_R(\psi_R)^c + \text{h.c.}$$
and notes that "Majorana mass term violates charge conservation, but not for neutrinos." With F27/F41/F42 the model already has a fully Higgs-free Dirac mass for $\nu$; a Majorana mass for $\nu_R$ alone is *also* compatible with the Higgs-free gauge structure (because $\nu_R$ is a gauge singlet under both SU(2)_L and U(1)_Y, the bare $\nu_R\nu_R$ Majorana term is gauge-invariant).

**Suggested action:** add a Majorana branch to `ca-simulation/forks/hypercharge_fork.py` and test (a) that the bare $\nu_R$ Majorana mass step is unitary and gauge-invariant; (b) whether the see-saw $m_\nu \approx M_D^2/M_R$ scaling is reproduced. If yes, this is the natural Higgs-free explanation for the smallness of neutrino mass — currently not addressed in any finding.

### 4.6 Use the stereographic projection (pp.110–124) as a representation check

The notebook's exposition of the spinor as a stereographic-projected direction is more careful than anything in the current code. Specifically, the observation that
$$\zeta = \frac{\xi}{\eta} = \frac{x + iy}{r - z}$$
and that the "ambiguity in $\xi,\eta$ is exactly the spinor ambiguity" gives a clean way to test that the BCC Weyl spinor field actually represents a sphere of directions and not just a pair of complex numbers.

**Suggested action:** add a unit test to `ca-simulation/ca_dirac.py` or `ca_core.py` that picks 100 random points on the unit sphere, converts them to Weyl spinors via stereographic projection, applies a rotation, converts back, and verifies the result is the rotated point to machine precision. This is a cheap correctness check on the spinor representation that is currently implicit.

### 4.7 Page 27 / 32 tetrad ambiguity: explicit gauge fixing in `ca_dirac.py`

Page 27 asks: "Could there be a whole set of $q$'s at any point that give the same $g_{\mu\nu}$? Presumably so, like a gauge invariance." Page 32 answers: yes, $q^\mu = q^\mu_a \sigma^a$ admits a local Lorentz/tetrad transformation that leaves $g^{\mu\nu} = \tfrac12(q^\mu \tilde q^\nu + q^\nu \tilde q^\mu)$ invariant.

**Suggested action:** when the gravity fork (ca-dirac-gravity-plan.md) is implemented, this tetrad gauge symmetry needs an explicit gauge-fixing choice — Sachs uses one implicit choice but the notebook never names it. Document the choice and verify a unit test that random tetrad rotations leave the lattice $g^{\mu\nu}$ invariant.

---

## 5. Items deliberately not pursued

The notebook also contains material that is either already absorbed into the project or that the author themselves correctly dismissed. Recording them here so future passes do not re-open them:

- **Sachs electrogravity Lagrangian derivation (pp.15–34).** The mathematical structure ($q^\mu, \tilde q^\mu, \Omega_\mu, K_{\mu\nu}$) is sound but Sachs' identification of electromagnetism with the spinor connection is a specific *choice* not adopted in the present model. We use F25's discrete Maxwell + F27's chiral SU(2) gauge instead.
- **Cooper-pair / superconductivity analogy for the photon (pp.5–6).** The intuition is correct but the analogy isn't pursued because F25 gives a cleaner direct derivation.
- **$Z$ as a $W^+W^-$ bound state (p.90).** Author's own "energies just don't work out" call is correct.
- **Massless-only $W^\pm$ with no $Z$ (p.79).** Speculation contradicted by F35.
- **"Helical motion gives $v_\text{eff} \to \infty$" (p.74).** Author's algebra is wrong about the high-energy limit; the actual result $v\to c$ is correct and supportive — see §3.4 / §4.4.
- **Free scalar field hierarchy (pp.41–55).** Standard QFT exposition (Goldstein / Itzykson-Zuber); already in the toolkit, no model implication.
- **Black-body radiation (p.78).** Reference notes only.

---

## 6. Proposed follow-up actions, ranked by priority

| # | Action | Estimated effort | Falsifiability gain |
|---|---|---|---|
| 1 | New finding **F43** — reconciliation of the page 65 $m_Z$ derivation (incl. cross term and $m_A = 0$ constraint) with F35 / F34b. | low | high — makes the Higgs-free $m_Z/m_W$ prediction explicit |
| 2 | New finding **F46** — Pythagorean lattice mass decomposition (§4.4). Numerical check on existing F27+F30 outputs. | low–medium | high — exact relation linking F26 and F27 |
| 3 | New short note **F44** on Higgs-free kinetic double-counting and its resolution in `ca_dirac.py` / `ca_wmu.py`. | low | medium — removes a hidden assumption |
| 4 | Test whether $\sin^2\theta_W$ is geometrically fixed by the BCC mixing (§4.2, §4.3). Either result is a finding. | medium | very high — fits or refutes a single experimentally measured number |
| 5 | Majorana fork for $\nu_R$ (§4.5). | medium | medium — explains neutrino mass smallness in the Higgs-free model |
| 6 | Stereographic-projection unit test for the Weyl spinor representation (§4.6). | low | low — internal consistency only |
| 7 | Document the tetrad-gauge choice for the gravity fork (§4.7). | low | n/a until gravity fork active |
| 8 | Short note in F25 or F39 explicitly citing the longitudinal-only result of pp.161–175 for the single-spinor reduction (§3.3). | very low | low — clarifies why the photon must be a bilinear |

---

## 7. Conclusion

The notebook is **net supportive** of the current model: nothing in it falsifies a confirmed finding, and it remains the canonical motivation for all three of the project's "key decisions" (composite photon, $c_\text{lat}$ as rotation rate, Higgs-free chiral SU(2)).

Two specific calculations (pages 65–66 $m_Z$ derivation, page 70 kinetic factors of 2) need short reconciliation notes because the present implementation silently resolves them and a future reader of the notebook would be confused. One construction (page 73 helical-motion mass) was wrongly dismissed by the author and is a candidate for an exact new finding. Three more items — the $A$↔spin / $W$↔isospin duality, the $\sin^2\theta_W = 2/9$ algebraic prediction, and the Majorana neutrino fork — represent **predictive content the model currently lacks** and should be tested.

Priority recommendation: do **F46 first** (§4.4, §6 row 2). It is cheap, uses already-running F27 and F30 outputs, and a successful test gives a single exact equation linking the photon and the fermion sectors of the model in a way nothing else does.

---

*End of review.*
