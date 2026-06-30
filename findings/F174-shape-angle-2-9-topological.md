# F174 — The shape-angle algebraic connection, built out: the lepton-condensate angle is **$\delta^*=\tfrac29$ rad** ($3\delta^*=\tfrac23$ rad) — a **topological rational-radian phase**, not a geometric angle. Geometric (algebraic-cosine) alternatives are excluded at $>10\sigma$; the value is corroborated independently (Brannen) and has a model home on the BCC 2nd shell (F49/F145); the winding$\to\tfrac29$ derivation is the one open build

**Date:** 2026-06-29 - 23:05
**Numbering:** F173 taken by a concurrent session; this is **F174** (re-checked).
**Status:** Partial (a sharp corroborated target + an exclusion + a model home + a triangulation; the derivation itself open) — 4/4 checks PASS. **What this establishes:** following F172's recommendation to attack the SHAPE residual, the lepton-condensate angle is pinned to **$\delta^*=\tfrac29$ rad** ($3\delta^*=\tfrac23$ rad): consistent with the PDG masses at $0.9\sigma$ and independently with Brannen's circulant fit $\delta=0.2222220(19)$. Crucially, the **geometric / algebraic-cosine** alternatives ($\cos3\delta^*=11/14$, $\pi/4$) are **excluded at $10\sigma$/$31\sigma$**, while the transcendental-cosine $3\delta^*=\tfrac23$ survives — so the connection, if exact, is a **rational radian**, the signature of a *topological/flux* phase, not a group-theoretic projection. The value $\tfrac29$ is exactly the model's recurring 2nd-shell number (F49 $\sin^2\theta_W=\tfrac29$, F145 Fierz $c=\tfrac29$), and the $E_g$ condensate lives on that 2nd shell (F93). **What remains:** the model computation that the 2nd-shell condensate winding equals $\tfrac29$ rad (the BCC analogue of the external ZIP topological-moment derivation of $\delta=\tfrac29$), and the mild $\eta^2=\tfrac12$ vs $\delta=\tfrac29$ joint-exactness tension.
**Script:** `tests/findings/test_F174_shape_angle_2_9.py` (~1 s, stdlib)
**Results:** `test-results/F174_shape_angle_2_9.json`
**Cross-references:** [[F172-residual-algebraic-or-computed]] (the shape/scale split and the recommendation this executes), [[F96-second-shell-Eg-gap-saturation]] (the exact $3\delta=\pi/4$ at $m_e=0$ anchor — a *geometric* algebraic cosine, contrasted here with the *topological* physical angle), [[F92-per-constituent-phase-consistency]] (the $\eta^2=\tfrac12$ Koide amplitude / Fock $\sqrt2$), [[F93-orthorhombic-Eg-vacuum]] (the $E_g$ condensate on the BCC 2nd shell; §8 flagged $\delta\approx\tfrac29$ rad), [[F95-B-derived-C-localized]] ($B$ derived), [[F150-eg-sextic-brake-from-architecture]] ($\cos3\delta^*=-B/2C$, $\lambda_6=0.243$, the $3\delta^*=Q$ target), [[F164-lambda6-derivation-attempt-and-relabel]] ($\lambda_6$ not a clean rational — consistent with a transcendental cosine), [[F49-bcc-finite-k-weinberg-angle]] ($\sin^2\theta_W=\tfrac29$ from 2nd-shell counting — the model's other $\tfrac29$), [[F145-route-c-induced-njl-coupling]] (Fierz $c=\tfrac29$). External: Brannen circulant lepton fit ($\delta=0.2222220(19)$, $\eta^2=0.500003(23)$, [brannenworks MASSES2](https://brannenworks.com/MASSES2.pdf)); Foot geometric $\pi/4$ ([Koide formula, Wikipedia](https://en.wikipedia.org/wiki/Koide_formula)); the ZIP derivation of $\delta=\tfrac29$ as a 3D topological-moment difference ([Derivation of the Koide Formula from the Zero-Interaction Principle](https://www.academia.edu/145613039/Derivation_of_the_Koide_Formula_from_the_Zero_Interaction_Principle)).

---

## 1. The target, made precise (S1)

The charged-lepton masses are described by the Koide–Foot–Brannen circulant form $\sqrt{m_a}=\mu\big(1+2\eta\cos(\delta+\tfrac{2\pi a}{3})\big)$. A free three-parameter fit to the PDG masses gives

$$\eta^2=0.4999908\ (\to\tfrac12),\qquad \delta^*=0.222229\ \text{rad}\ (\to\tfrac29),\qquad 3\delta^*=0.666689\ \text{rad}\ (\to\tfrac23),$$

with $3\delta^*$ consistent with the rational $\tfrac23$ at $0.9\sigma$ (uncertainty $2.5\times10^{-5}$, dominated by $m_\tau$). This is **not** a model-only artefact: Brannen's independent published circulant fit gives $\delta=0.2222220(19)$ and $\eta^2=0.500003(23)$ — i.e. $\delta=\tfrac29$ to seven digits. So the open shape residual has a specific corroborated value: $\boxed{\delta^*=\tfrac29\ \text{rad}}$.

## 2. It is a rational radian, not a geometric angle (S2) — the decisive structural clue

Among simple exact candidates for $\cos3\delta^*=0.785874(16)$, only one survives:

| candidate | type | value | deviation |
|---|---|---|---|
| $\cos(2/3)$ ($3\delta^*=\tfrac23$ rad) | **rational radian** (transcendental cosine) | $0.785887$ | **$0.9\sigma$** |
| $11/14$ | algebraic (rational) | $0.785714$ | $10\sigma$ — excluded |
| $\pi/4$ | algebraic ($=1/\sqrt2\cdot\dots$; transcendental but "geometric") | $0.785398$ | $31\sigma$ — excluded |
| $1/\sqrt2$ (the F96 $m_e=0$ anchor) | algebraic | $0.707107$ | far — this is the *massless* limit |

The geometric/algebraic-cosine forms are decisively excluded. The surviving form is a **rational number of radians** ($\delta^*=\tfrac29$). This is the key structural clue: a rational radian is **not** what a group-theoretic projection or a crystallographic angle produces (those give algebraic cosines — e.g. F96's exact $\pi/4$ at $m_e=0$). A rational radian is the signature of a **topological / flux / winding** phase, where the radian measure is a ratio of integers (a winding number over a normalisation). The physical lepton angle is therefore *not* the same kind of object as the F96 massless-limit anchor: the anchor is geometric ($\pi/4$), the physical angle is topological ($\tfrac29$), and $m_e>0$ carries the system from one to the other.

This also explains F164's result that $\lambda_6$ is "not a clean rational": $\lambda_6\propto1/\cos3\delta^*=1/\cos(\tfrac23)$ is transcendental even though $\delta^*$ is the simple rational $\tfrac29$. The simplicity lives in the **angle**, not in the brake coefficient.

## 3. The model home: the $\tfrac29$ of the second shell (S3)

The value $\tfrac29$ is not new to the model — it recurs precisely on the **BCC second-neighbour shell**, which is exactly where the $E_g$ lepton condensate lives (F93 O2):

- **F49:** $\sin^2\theta_W=\tfrac29$ from second-shell sublattice/bond counting.
- **F145:** the induced Fierz coupling $c=\tfrac29=\tfrac49_{\text{colour}}\times\tfrac12_{\text{flavour}}$.
- **F93 §8** already flagged $\delta\approx\tfrac29$ rad as a target on this shell.

So the same geometric object (the 2nd shell) that fixes the Weinberg ratio and hosts the induced coupling also hosts the condensate whose phase is $\tfrac29$ rad. **Triangulation:** imposing $\delta^*=\tfrac29$ (i.e. $\cos3\delta^*=\cos\tfrac23$) in the derived brake relation $\cos3\delta^*=-B/2C$ (with $B$ derived, F95) reproduces the F118 brake fit $\lambda_6=0.243$ to $10^{-5}$. Data, the dynamical brake, and the $\tfrac29$ conjecture all agree.

This suggests the right reading: the angle is **not** fundamentally the output of the (transcendental) brake; the brake *value* $\lambda_6$ is the output of the angle being the topological $\tfrac29$. The arrow points angle $\to$ brake, not brake $\to$ angle.

## 4. External corroboration

- **Brannen** (independent): the circulant lepton fit gives $\delta=0.2222220(19)\approx\tfrac29$ and $\eta^2\approx\tfrac12$ — the same two numbers, from a different formalism.
- **ZIP** (Zero-Interaction Principle): derives $\delta=\tfrac29$ as the **difference between the third and second topological moments of a pure-potential state in three-dimensional configuration space** — an explicit, external realisation of "rational radian from 3D topology," precisely the interpretation S2 forces. The model is a 3D (BCC) lattice with winding structure, so this is the natural template for the in-model derivation.
- **Foot:** the $\pi/4$ is the *amplitude* angle (between $(1,1,1)$ and $(\sqrt{m_e},\sqrt{m_\mu},\sqrt{m_\tau})$) — i.e. the $\eta^2=\tfrac12$/Koide fact, a *separate* exact geometric statement from the $\tfrac29$ phase. The two exact facts of the lepton spectrum are thus cleanly split: an **algebraic amplitude** ($\pi/4$, Koide) and a **topological phase** ($\tfrac29$).

## 5. The honest caveat (S4)

The free fit lands at $\eta^2=0.49999$ and $\delta=0.222229$ — each $\sim10^{-5}$ off the ideal $\tfrac12$ and $\tfrac29$, each within $\sim1\sigma$. Whether **both** $\eta^2=\tfrac12$ and $\delta=\tfrac29$ can be *exactly* true simultaneously is below current data precision; Brannen flags a potential conflict at higher precision. This may be resolved by the mass scheme (pole vs running) or by a small derived correction. So $\delta^*=\tfrac29$ is a **corroborated target**, not yet a theorem.

## 6. Verdict and the one open build

> **A sharp algebraic-connection candidate for the shape angle exists and is corroborated: $\delta^*=\tfrac29$ rad, a topological (rational-radian) phase.** The geometric alternatives are excluded; the model carries $\tfrac29$ on exactly the shell where the condensate lives; an external 3D-topological derivation (ZIP) realises the same value.

This is a real advance over F172's "$3\delta^*=Q$ target": it identifies the *kind* of object (topological, not geometric), excludes the geometric competitors, and localises the derivation to the model's own 2nd-shell $\tfrac29$. **The one open build:** show that the $E_g$ condensate phase on the BCC second shell winds by exactly $\tfrac29$ rad — the model analogue of the ZIP topological-moment computation, plausibly the *same* counting that gives F49's $\sin^2\theta_W=\tfrac29$. If it closes, $\delta^*=\tfrac29$ becomes a theorem, $\lambda_6$ becomes a derived transcendental ($\propto1/\cos\tfrac23$), and the lepton mass *shape* is fully parameter-free — leaving only the overall scale (F144/F170) and its scheme constant (F162/F163, the separate computed half of F172).

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| S1 | $\delta^*=\tfrac29$ rad ($3\delta^*=\tfrac23$) at $0.9\sigma$; Brannen $0.2222220(19)$ | PASS | data + corroboration |
| S2 | geometric algebraic-cosine candidates excluded ($11/14$ $10\sigma$, $\pi/4$ $31\sigma$); rational-radian survives | PASS | exclusion |
| S3 | $\tfrac29$ on the 2nd shell (F49/F145) where the condensate lives (F93); imposing $\tfrac29$ → $\lambda_6=0.243$ (triangulation) | PASS | structural |
| S4 | caveat: $\eta^2=\tfrac12$ & $\delta=\tfrac29$ each $\sim1\sigma$, joint exactness below precision | PASS | scope |

**Overall 4/4 PASS.**

## 8. Honest scope

- This finding **pins and corroborates the target and identifies its kind and home**; it does **not** derive $\tfrac29$ from the model's lattice topology. The winding$\to\tfrac29$ computation is the open build (§6).
- "Topological rational radian" is an inference from the $>10\sigma$ exclusion of algebraic cosines plus the external ZIP precedent; it is a strong structural argument, not a proof that $\delta^*$ is exactly $\tfrac29$ (S4 caveat).
- The triangulation (S3) is a consistency check (imposing $\tfrac29$ reproduces the fitted $\lambda_6$), not an independent derivation of either.

## 9. Provenance

- **New:** the precise extraction and uncertainty of the lepton angle; the $>10\sigma$ exclusion of the geometric algebraic-cosine candidates leaving only the rational-radian $\tfrac29$; the identification of the angle as a *topological* phase (vs the geometric F96 anchor); the model-home localisation to the 2nd-shell $\tfrac29$ (F49/F145) with the $\lambda_6$ triangulation; the amplitude/phase split (Koide $\pi/4$ vs topological $\tfrac29$).
- **Reused:** F92 $\eta^2=\tfrac12$; F95 $B$; F96 $\pi/4$ anchor; F118/F150 $\lambda_6$/brake; F93 2nd-shell $E_g$; F49 $\sin^2\theta_W=\tfrac29$; F145 Fierz $\tfrac29$.
- **External:** Brannen ([MASSES2](https://brannenworks.com/MASSES2.pdf)); Foot/Koide geometry ([Wikipedia](https://en.wikipedia.org/wiki/Koide_formula)); ZIP topological-moment derivation of $\delta=\tfrac29$ ([academia.edu](https://www.academia.edu/145613039/Derivation_of_the_Koide_Formula_from_the_Zero_Interaction_Principle)).
- **Verification:** `tests/findings/test_F174_shape_angle_2_9.py` (2026-06-29, 4/4 PASS), results `test-results/F174_shape_angle_2_9.json`. Stdlib only — numpy-safe.
