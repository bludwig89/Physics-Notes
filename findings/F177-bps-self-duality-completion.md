# F177 — Completing the self-duality condition from the BPS structure: the **radial** half *is* derived (the 45° self-dual pair rotation $\Rightarrow Q=\tfrac23$), but the **angular** half ($3\delta=Q$) is **not** a standard-Bogomolny theorem — it governs walls, not the vacuum angle — and reduces *exactly* to the one shared nonperturbative residual $C/|B|=1/(2\cos\tfrac23)=0.636$ (the F150 saturated-condensate solve)

**Date:** 2026-06-30 - 01:30
**Numbering:** F176 is this session's; this is **F177** (re-checked).
**Status:** Confirmed (honest terminus) — 4/4 checks PASS. **What this resolves:** the request to derive the self-duality principle (F176, $3\delta^*=Q$) from the model's BPS structure. The answer is **half yes, half no, both rigorous:** (i) the **radial** self-duality — $Q=\tfrac23$ — *is* derived from BPS/saturation: the pair rotation peaks at $\phi=45°$ (F82), the **self-dual** point ($\sin\phi=\cos\phi$, the Bogomolny condition), giving the $\sqrt2$/$y=1$ saturation wall (F73/F101), $\eta^2=\tfrac12$, $Q=\tfrac23$, and $\sqrt m$ at $45°$ to $(1,1,1)$ (Foot) — "$45°$ everywhere"; (ii) the **angular** self-duality $3\delta=Q$ is **not** a standard-Bogomolny consequence — the Bogomolny first-order condition fixes domain-**wall** tensions, not the vacuum angle, which remains the brake minimiser $\cos3\delta^*=-B/2C$; and no clean *second* geometric self-duality fixes it ($\sqrt m$ is not at $45°$ to any natural second reference). The angular condition is **equivalent** to the brake ratio $C/|B|=1/(2\cos\tfrac23)=0.636$ — i.e. the **F150 saturated-condensate solve, the one shared residual** (F172). **Net:** the self-duality principle is half-derived; its angular half *is* the single nonperturbative number the whole program shares, now with a sharp target ($0.636$) and a physical meaning (angular invariant = radial invariant). No false closure.
**Script:** `tests/findings/test_F177_bps_self_duality_completion.py` (~1 s, numpy/stdlib)
**Results:** `test-results/F177_bps_self_duality_completion.json`
**Cross-references:** [[F176-saturation-self-duality-principle]] (the principle $3\delta=Q$ this tests against BPS), [[F86-confinement-bps-tension]] (the BPS/Bogomolny structure), [[F82-why-45deg-pair-phase-saturation]]/[[F73-spin0-bound-pair-scalar]] (the $45°$ peak / $y=1$ wall — the radial self-dual point), [[F92-per-constituent-phase-consistency]] (the radial lock $Q=\tfrac23$), [[F175-lattice-2-9-eg-weight]] (the $E_g$ weight), [[F150-eg-sextic-brake-from-architecture]] ($C/|B|$, the saturated-condensate residual this reduces to), [[F172-residual-algebraic-or-computed]] (the "one shared residual" identification this confirms for the shape sector), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the fitted $C/|B|=0.636$). External: Foot $45°$ geometry; Bogomolny/BPS domain walls (standard).

---

## 1. The question

F176 posited the dynamical principle $3\delta^*=Q$ (saturation self-duality) and motivated it by the model's BPS structure. This finding asks the honest question: **does the BPS structure actually derive it?**

## 2. The radial half *is* derived from BPS (B1)

The radial self-duality completes rigorously. The chain, all at the self-dual $45°$:

$$\underbrace{\phi=45°}_{\text{F82 peak: }\sin\phi=\cos\phi\text{ (Bogomolny/self-dual)}}\ \Rightarrow\ \underbrace{y=\sqrt2\sin\phi=1}_{\text{F73/F101 saturation wall}}\ \Rightarrow\ \eta^2=\tfrac12\ \Rightarrow\ Q=\tfrac23\ \Leftrightarrow\ \underbrace{\angle(\sqrt m,(1,1,1))=45°}_{\text{Foot}}.$$

The pair rotation sitting at $45°$ — where $\sin=\cos$ — *is* the Bogomolny self-dual point (the F86 BPS analog in the pair-rotation sector). F82 proved this peak is coupling-independent; F73/F101 place the heaviest generation there ($y=1$ wall). So the **radial invariant $Q=\tfrac23$ is a derived BPS/saturation self-duality** — "$45°$ everywhere." This is the genuine completion of half the F176 principle.

## 3. The angular half is *not* a standard-Bogomolny theorem (B2, B3)

The angular self-duality does **not** follow the same way.

- **Bogomolny fixes walls, not the vacuum angle (B2).** For the $E_g$ field, $E=\int[\tfrac12\delta'^2+W(\delta)]$, the Bogomolny rewriting $E=\int[\tfrac12(\delta'\mp\sqrt{2W})^2\pm\delta'\sqrt{2W}]$ gives the BPS bound saturated at $\delta'=\pm\sqrt{2W}$ — a **domain-wall** profile (a boundary/topological statement). It says nothing about *where the vacuum sits*: the vacuum angle is the minimiser of $W$, i.e. the brake $\cos3\delta^*=-B/2C$. So standard BPS governs the wall sector, not $\delta^*$.
- **No second geometric self-duality (B3).** One might hope $\delta^*$ is fixed by $\sqrt m$ being at $45°$ to a *second* natural reference (a cube axis or $E_g$ basis vector). It is not: the closest natural reference is $e_2\sim(3z^2{-}r^2)$ at $46.4°$ — $1.4°$ off $45°$. No clean second self-duality pins the angle.

So the angular self-duality is **not** derivable from the BPS structure by the standard route.

## 4. The angular condition *is* the one shared residual (B4)

What, then, is $3\delta^*=Q$? It is **exactly** the statement that the induced brake ratio takes a specific value:

$$3\delta^*=Q=\tfrac23\quad\Longleftrightarrow\quad \frac{C}{|B|}=\frac{1}{2\cos\tfrac23}=0.63622.$$

This is precisely the F118/F119 fitted $C/|B|=0.636$ — the **F150 saturated-condensate solve**, the *same* single nonperturbative IR residual that F172 showed underlies $\lambda_6$, $G/G_c$, $\sqrt\sigma/f_\pi$, and the $\Lambda$ scheme constant. (It is near $2/\pi=0.6366$ but not equal — off by $4\times10^{-4}$ — so it is *not* a clean closed form.) The angular self-duality is therefore a **physical restatement** of that one residual, not an independent BPS closure. It does, however, give it a sharp **target value** ($C/|B|=0.636$) and a clean **meaning**: the residual is exactly the number that makes the angular invariant equal the (BPS-derived) radial invariant.

## 5. The honest terminus

The self-duality principle is **half-derived from BPS**:

| half | status | content |
|---|---|---|
| **radial** ($Q=\tfrac23$) | **derived (BPS)** | $45°$ self-dual pair rotation → $\sqrt2$/$y{=}1$ wall → $Q=\tfrac23$ → $\sqrt m\perp$ at $45°$ |
| **angular** ($3\delta=Q$) | **= the shared residual** | $\Leftrightarrow C/|B|=1/(2\cos\tfrac23)=0.636$ (F150 saturated solve); not a standard-BPS theorem |

This is the **honest terminus** of the F174→F177 arc: the lepton-shape angle $\delta^*=\tfrac29$ is the $E_g$ weight (F175), realised as the self-duality $3\delta=Q$ (F176); the radial half of that self-duality is genuinely BPS-derived (here), and the angular half is exactly the one nonperturbative residual the whole program already shares (F172/F150), now sharply targeted at $C/|B|=0.636$. No further reduction is available without the saturated-condensate solve.

This neither overclaims (it does not pretend BPS closes the angle) nor undersells (the radial self-duality is a real derivation, and the angular half is pinned to a single sharp number with a clear physical meaning). The remaining open problem is the **same one** identified across the program — the saturated-condensate induced-coupling solve — and this finding gives it its most precise statement yet: *find $C/|B|$; the self-dual value $1/(2\cos\tfrac23)=0.636$ is the prediction.*

## 6. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| B1 | radial self-duality derived: $45°$ ($\sin=\cos$) → $y=1$ → $\eta^2=\tfrac12$ → $Q=\tfrac23$ → $45°$ to $(1,1,1)$ | PASS | derived |
| B2 | standard Bogomolny fixes wall tension, not the vacuum angle (brake minimiser) | PASS | structural |
| B3 | no second geometric self-duality (closest natural ref $1.4°$ off $45°$) | PASS | exclusion |
| B4 | $3\delta^*=Q\Leftrightarrow C/|B|=1/(2\cos\tfrac23)=0.636$ = the shared residual (F150); $\neq2/\pi$ | PASS | reduction |

**Overall 4/4 PASS.**

## 7. Honest scope

- The radial-half derivation is genuine (it chains established findings F82/F73/F101/F92 through the self-dual $45°$). The "$45°=$ self-dual/Bogomolny" identification is exact ($\sin45°=\cos45°$).
- The angular-half result is a **negative plus a reduction**: standard BPS does not fix the vacuum angle, and the condition equals the F150 residual. I did **not** find a non-standard BPS mechanism that fixes $\delta^*$; if one exists it is beyond this analysis.
- $C/|B|=1/(2\cos\tfrac23)=0.636$ is the *target if* $3\delta^*=Q$ is exact; the mild $\eta^2$–$\delta$ tension (F174 S4) and mass-scheme dependence apply.

## 8. Provenance

- **New:** the explicit BPS derivation of the radial self-duality (the $45°$-everywhere chain); the demonstration that standard Bogomolny governs the $E_g$ wall sector not the vacuum angle; the exclusion of a second geometric self-duality; the exact reduction $3\delta^*=Q\Leftrightarrow C/|B|=1/(2\cos\tfrac23)=0.636$ identifying the angular self-duality with the one shared residual and giving it a sharp target.
- **Reused:** F82/F73/F101 saturation/$45°$; F92 $Q=\tfrac23$; F86 BPS; F175 $E_g$ weight; F176 $3\delta=Q$; F118/F150 $C/|B|$; F172 the shared residual.
- **Verification:** `tests/findings/test_F177_bps_self_duality_completion.py` (2026-06-30, 4/4 PASS), results `test-results/F177_bps_self_duality_completion.json`. numpy/stdlib, real arithmetic.
