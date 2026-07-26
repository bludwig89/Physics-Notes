# F255 — E1 follow-up: the F118/F234 self-consistent solve **does** implicitly fix the $E_g$ generator norm ($R=1$) — the condensate phase is the *canonical* $E_g$-plane angle (Schur-isotropic metric), a genuine radian, **not** a weight×free-scale — so F253's POSIT-N part (a) is **derived**; but E1 still does **not** close, its residual sharpening to the single sextic coupling $\lambda_6=0.243$ (the weight-identity remains circular)

**Date:** 2026-07-16 - 17:40
**Numbering:** F254 taken by a concurrent session (D1/PMNS $T_{2g}$ selector); this is **F255**. Direct follow-up to **F253** (E1 weight→phase), answering: *does the F118/F234 $(W,v,c)$ solve implicitly fix the generator normalization $R$?*
**Status:** Confirmed (partial-positive: one half of POSIT-N derived; the other half sharpened) — 4/4 checks PASS. **What this establishes:** F253 reduced E1 to a single posit POSIT-N with two logically separable halves — **(a)** the $E_g$ phase is a genuine radian (generator norm $R=1$, no free scale), and **(b)** that radian equals the $E_g$ weight $\tfrac29$. This finding checks both against the F118 functional. **Half (a) is DERIVED, not posited:** in the F118 second-shell functional the angle $\delta$ is literally the argument of the $E_g$ order-parameter doublet in the *deviation simplex* — the lepton amplitude deviations $p_a=\sqrt{m_a}-\overline{\sqrt m}$ lie in the $E_g$ plane (⊥ $(1,1,1)$) to $2.3\times10^{-16}$, and by **Schur's lemma** the $E_g$ irrep's invariant metric is isotropic (its $O_h$ generators act orthogonally, $D^{\mathsf T}D=\mathbb 1$ to $4.4\times10^{-16}$), so the plane angle is **canonical** — a genuine radian whose only freedom is an overall scale that does not affect angles. Hence $R=1$ is **forced by representation theory**, removing F253's "$\delta=\text{weight}\times R$ with $R$ free" escape hatch. The direct geometric angle $=0.22223$ rad $=\tfrac29$ to $0.003\%$, identical to the Koide azimuth. **Half (b) does NOT close:** the value of that genuine angle is set dynamically by $\cos3\delta^*=-B/2C$ (F230/F118), i.e. by the sextic $\lambda_6=C/e^6$; F234 pins $\lambda_6=0.243$ *by assuming* $\delta^*=\tfrac29$, so using it to *derive* $\tfrac29$ is **circular**, F118's sea loop is excluded from sourcing $C$ (wrong sign + scaling, F118-B1/B2), and the suggestive $\lambda_6=\tfrac14$ (the F115 rotor value) misses $\tfrac29$ by $\sim5\%$. **Net:** E1's residual is refined and *moved* — no longer "a normalization ($R$) **plus** an identity", but the **single** dimensionless coupling $\lambda_6=0.243\ (\approx\tfrac14)$: the $E_g$ sextic clock self-interaction. The generator-norm question the user posed is **answered yes**; E1 is one coupling away from closure.
**Script:** `ca-simulation/derive_generator_norm_from_F118.py` (analysis; real numpy + PDG masses, no chiral transforms)
**Test:** `tests/findings/test_F255_generator_norm_from_F118.py` (4/4, <4 s)
**Results:** `test-results/F255_generator_norm_from_F118.json`
**Cross-references:** [[F253-weight-as-phase-scale-nogo]] (the parent E1 finding — POSIT-N and the topological exclusion this refines; part (a) is upgraded from posit to theorem here), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the $(W,v,c)$ functional whose $\delta$ is the $E_g$-plane angle; B1/B2 exclude the sea loop from sourcing $C$; localizes $\lambda_6=0.243$), [[F234-Wvc-triple-closed-delta-2-9-pins-brake]] (pins $\lambda_6$ **from** $\delta^*=\tfrac29$ — the circular leg), [[F175-lattice-2-9-eg-weight]] (the $E_g$ weight $\tfrac29$), [[F230-lepton-angle-geometric-nogo]] ($\cos3\delta^*=-B/2C$; $Q$ is $\delta$-blind), [[F95-B-derived-C-localized]] (the derived cubic $B=-0.0569$), [[F92-per-constituent-phase-consistency]] (the saturation amplitude $e\approx0.733$, $r=\sqrt2$), [[F115-f116-coupling-magnitudes-njl]] (the rotor $g_s^2\chi=\tfrac14$ that $\lambda_6$ flirts with), [[F93-orthorhombic-Eg-vacuum]] ($E_g$ is the spontaneous condensation channel).

---

## 1. The question

F253 localized the whole E1 residual to POSIT-N: *the $E_g$ order-parameter generator is unit-normalized so the democratic phase budget $=1$ rad*, giving $\delta^*=\text{weight}\times R=\tfrac29\times1$. Its two halves:

- **(a) normalization** — $\delta$ is a genuine radian ($R=1$, no free scale);
- **(b) identity** — that radian equals the representation weight $\tfrac29$.

The follow-up asks whether the F118/F234 self-consistent $(W,v,c)$ solve — which reproduces the exact lepton spectrum on the spontaneous-$E_g$ branch — *implicitly* supplies either half.

## 2. Half (a) is derived: the phase is the canonical $E_g$-plane angle ($R=1$ forced)

In the F118 functional the flavour vector is $y_a=\sqrt{m_a}$ (wall-normalized) and the order parameter is the **deviation** $p_a=y_a-\bar y$. Two facts make $\delta$ a canonical radian:

**(N1) The deviations live in the $E_g$ plane.** $\sum_a p_a=0$ identically, so $p\perp(1,1,1)$ — verified at $|p\cdot(1,1,1)|/\lVert p\rVert=2.3\times10^{-16}$. The 2D plane ⊥ $(1,1,1)$ is exactly the $E_g$ doublet plane (the $A_{1g}$ direction is $(1,1,1)$; $p$ carries no $A_{1g}$ part by construction). So $\delta\equiv\arg(p\ \text{in the }E_g\text{ plane})$ is a literal geometric angle, and $\Phi=e\,e^{i\delta}$ with $e=\lVert p\rVert$.

**(N2) Schur makes that angle canonical — $R=1$ is not a choice.** $E_g$ is a 2-dimensional *irreducible* representation of $O_h$. By Schur's lemma its invariant bilinear form is unique up to an overall scalar; concretely the $O_h$ generators act on the $(d_{z^2},d_{x^2-y^2})$ doublet as **orthogonal** matrices ($D^{\mathsf T}D=\mathbb 1$ to $4.4\times10^{-16}$ for $C_3,C_4,C_2$). An isotropic (scalar$\times\mathbb 1$) metric is angle-preserving, and an overall scale cancels in an angle. Therefore the $E_g$-plane angle $\delta$ is **canonical** — a genuine radian with **no free normalization**. This is precisely $R=1$, now a *theorem* (representation theory), not the posit F253 conservatively flagged.

The measured value of this canonical angle is $\delta=0.22223$ rad $=\tfrac29$ to $0.003\%$, identical (both $C_{3v}$ foldings agree) to the Koide circulant azimuth — as it must be, since it is the same $E_g$ phase.

> **Correction to F253.** F253 wrote "$\delta=\text{weight}\times R$ with $R$ free." That over-counted the freedom: $R$ is fixed to $1$ by Schur-isotropy of the $E_g$ metric. POSIT-N part (a) is retired.

## 3. Half (b) does not close: the weight-identity stays circular ($\lambda_6$)

With $R=1$ fixed, the identity $\delta^*=\tfrac29$ is *not* automatic — it is the statement that the **dynamically** selected angle equals the weight. F118/F230 select it via the Landau minimiser

$$\cos3\delta^*=-\frac{B}{2C},\qquad B=-0.0569\ (\text{derived, F95}),\quad C=\lambda_6 e^6\ (\text{open}).$$

Assuming $\delta^*=\tfrac29$ gives $C_\text{req}=|B|/(2\cos\tfrac23)=0.0362$ and $\lambda_6=0.243$ (F234, reproduced here). But this is the **circular** leg: F234 obtains $\lambda_6$ **from** $\tfrac29$, so it cannot deliver $\tfrac29$. Independently:

- **F118-B1/B2** exclude the sea loop as the source of $C$: at saturation its sextic is *wrong-sign* ($C_\text{loop}=-0.018$, an anti-brake) and at small amplitude *wrong-scaling* ($\sim\bar y^7$). No independent $\lambda_6$ emerges.
- The tempting $\lambda_6=\tfrac14$ (the F115 rotor $g_s^2\chi=\tfrac14$) gives, at the same $e\approx0.728$, $\delta=0.234$ — a $\sim5\%$ miss from $\tfrac29$. So $\tfrac14$ is *not* the exact value; the spectrum needs $0.243$.

Hence half (b) — why the canonical angle lands on the weight — remains open, and it is now the **only** open piece: a first-principles $\lambda_6=0.243$ (or a direct reason $\arccos(-B/2C)/3=\tfrac29$).

## 4. What moved

- **New (positive):** POSIT-N part (a) is **derived** — the $E_g$ condensate phase is the canonical $E_g$-plane angle, $R=1$ forced by Schur-isotropy of the irrep metric (N1/N2). The user's question — *does the F118/F234 solve implicitly fix the generator norm?* — is answered **yes**. F253's "free $R$" is corrected.
- **New (sharpening):** E1's residual collapses from "normalization $R$ **and** identity" to the **single** coupling $\lambda_6=0.243\ (\approx\tfrac14)$ — the $E_g$ sextic clock self-interaction — with the sea loop excluded (F118) and $\tfrac14$ shown to miss by $5\%$. The weight-identity is currently **circular** (F234) and awaits an independent $\lambda_6$.
- **Reused:** F118 (functional, B1/B2), F234 (the pin), F175 (weight), F230 (minimiser), F95 ($B$), F92 ($e$), F115 ($\tfrac14$). PDG masses.

## 5. Checks (`test_F255_generator_norm_from_F118.py`, 2026-07-16 - 17:40)

| # | Statement | Tier | Result |
|---|---|---|---|
| N1 | deviation $p\perp(1,1,1)$ (lives in $E_g$ plane) | exact | PASS ($2.3\times10^{-16}$) |
| N2 | $E_g$ metric isotropic ($D^{\mathsf T}D=\mathbb 1$) ⇒ angle canonical, $R=1$ forced (Schur) | exact | PASS ($4.4\times10^{-16}$) |
| N3 | geometric $E_g$ angle $=$ Koide azimuth $=\tfrac29$ rad to $<0.01\%$ | data/target | PASS ($0.003\%$) |
| N4 | weight-identity circular: $\lambda_6$ from $\tfrac29$ (F234); $\lambda_6=\tfrac14$ misses $\sim5\%$ | negative | PASS |

**Overall 4/4 PASS** (<4 s).

## 6. Verdict

The F118/F234 solve **does** implicitly fix the $E_g$ generator normalization: its condensate phase is the canonical $E_g$-plane angle, a genuine radian with $R=1$ **forced by Schur's lemma** (the $E_g$ irrep metric is isotropic), so the weight→radian bridge is *not* a free normalization — F253's POSIT-N part (a) is derived. But E1 does **not** close: the remaining half — that this canonical angle equals the weight $\tfrac29$ — is set by the sextic $\lambda_6$, which F234 pins only by *assuming* $\tfrac29$ (circular), which the sea loop cannot source (F118), and which the rotor $\tfrac14$ reproduces only to $\sim5\%$. **E1 is now exactly one dimensionless number from closure:** an independent $\lambda_6=0.243$ (equivalently, a dynamical reason the $E_g$ minimiser $\arccos(-B/2C)/3$ sits at the representation weight).

## 7. Provenance

- **New content:** the Schur-isotropy proof that the $E_g$ condensate phase is a canonical radian ($R=1$ forced, N2); the identification of the F118 deviation-simplex angle with the Koide azimuth (N1/N3); the explicit separation of POSIT-N into a *derived* half (a) and a *circular/open* half (b); the correction to F253's "$R$ free" and the $\lambda_6=\tfrac14$ $5\%$-miss check.
- **Reused:** F118, F234, F175, F230, F95, F92, F115, F93. PDG charged-lepton masses ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV).
- **Verification:** `tests/findings/test_F255_generator_norm_from_F118.py` (2026-07-16 - 17:40, 4/4 PASS), results `test-results/F255_generator_norm_from_F118.json`, script `ca-simulation/derive_generator_norm_from_F118.py`. Real arithmetic — numpy-safe.
