# F230 — E1: deriving $\delta^*=\tfrac29$ rad from the crystal-field / equipartition geometry closes **negative** — geometry fixes only the phase-coordinate **endpoints** (democratic $0$, massless-Koide $3\delta=\pi/4$, equipartition $45°$); the **interior** stopping point is dynamics ($\lambda_6$), and a radian cannot equal a ratio without a scale

> **Numbering note:** this is **F230** (E1). Companion open-derivation findings from this batch: **F231** (E2) and **F232** (L3). Concurrent sessions took F233 (mass-scale $N$/E3), F234 (W,v,c triple/E4), F235 ($\sqrt\sigma/f_\pi$/Q1); F229 is left vacant by the collision reshuffle.

**Date:** 2026-07-02 - 16:35
**Status:** Confirmed (negative / sharpened no-go) — 6/6 checks PASS. Attempts the E1 target — derive the charged-lepton spectrum angle $\delta^*=\tfrac29$ rad ($3\delta^*=Q=\tfrac23$) from the F75/F76 $T_{1u}$ crystal-field geometry + F78/F80 Cooper-pair equipartition ($45°$) — along the **geometric** route (distinct from F179's induced-coupling route and F199's BPS route). It **closes negative**, and sharpens the reason: the geometry produces only the **endpoints** of the phase coordinate $3\delta$ (democratic $3\delta=0$; massless-Koide $3\delta=\pi/4$, *exact*; equipartition $\phi=45°$), while the physical **interior** value $3\delta^*=\tfrac23$ rad is fixed by the brake ratio $B/C$ (cubic crystal-field vs sextic self-coupling), a dynamical number. The **dimensional no-go**: $3\delta^*$ is a radian, $Q$ is a pure ratio; crystal-field geometry yields only trig ratios and rational irrep multiplicities and cannot force radian $=$ ratio without a dynamical scale. This is consistent with, and subsumed by, **F199**'s three-way structural no-go; $\delta^*=\tfrac29$ rad remains a Koide-confidence **target**, not a derivation.
**Module:** (analysis-only; PDG masses + F80/F92/F96 closed forms; real arithmetic — no chiral transforms)
**Script:** `tests/findings/test_F230_lepton_angle_geometric_nogo.py` (<1 s, stdlib only)
**Results:** `test-results/F230_lepton_angle_geometric_nogo.json`
**Cross-references:** [[F199-angular-self-duality-derivation-forced-posit]] (the **definitive** structural no-go on this exact target: $Q$ is $\delta$-blind so there is no second relation; $C/\lvert B\rvert$ carries $\alpha_\text{eff}^*$ undiluted so it is computed not algebraic; BPS degeneracy sits at $\tfrac12$ not $0.636$ — this finding reaches the same terminus by the crystal-field route and adds the endpoint/interior + radian-vs-ratio framing), [[F179-lambda6-derivation-attempt-and-relabel]] (the relabel of the lepton spectrum as a one-angle fit; $\delta^*$ Koide-locked to $-0.89\sigma$), [[F96-second-shell-Eg-gap-saturation]] (the exact massless endpoint $Q=\tfrac23\iff\delta=15°\iff3\delta=\pi/4$), [[F80-one-45deg-em-saturation-koide]] ($Q(\phi)=1/(3\cos^2\phi)$, equipartition $45°$; EM selects the sector but perturbative EM is $340\times$ too weak to *drive* the angle), [[F92-per-constituent-phase-consistency]] ($Q=\tfrac23$ from equipartition; $Q=\tfrac13+\tfrac16r^2$ is $\delta$-blind), [[F76-generation-mass-hierarchy-crystal-field]] / [[F75-three-generations-from-bcc-irrep-selection]] ($T_{1u}$ crystal-field geometry), [[F232-lattice-spacing-degeneracy-scale-invariance]] (companion "radian/ratio vs geometry" theme — a dimensionless number cannot come from the wrong kind of input), [[F49-bcc-finite-k-weinberg-angle]] (the $\sin^2\theta_W=\tfrac29$ echo, §G5, cross-referenced to F231).

---

## 1. The target and the geometric route requested

The charged-lepton shape reduces to one angular Landau potential (F93/F95/F118)

$$F(\delta)=B\cos3\delta+C\cos^23\delta,\qquad \cos3\delta^*=-\frac{B}{2C},$$

with $B<0$ **derived** (F95 sea loop) and $C=\lambda_6 e^6>0$ open. The data fix $\cos3\delta^*=0.785874$, $\delta^*=12.7328°$, $3\delta^*=0.666689$ rad $\approx Q=\tfrac23$ — the target $\delta^*=\tfrac29$ rad. E1 asks whether the $T_{1u}$ crystal-field geometry + the $45°$ equipartition can *force* this value.

## 2. What the geometry does fix — the endpoints (exact)

The geometry supplies the **coordinate and its endpoints**, all dimensionless/exact:

- **Form.** The $O_h\to$ orthorhombic descent of the $T_{1u}$ triplet (F76) gives the Koide amplitudes $y_a=\bar y+A\cos(\delta+2\pi a/3)$ — the phase $\delta$ is the $E_g$ orientation on the condensate circle.
- **Democratic floor.** $\delta=0$: degenerate generations, $Q=\tfrac13$ (F80).
- **Equipartition.** $Q(\phi)=1/(3\cos^2\phi)$ (F80); the measured leptons sit at $\phi=45°$, $r=A/\bar y=\sqrt2$, $Q=\tfrac23$ — verified $r=1.41420$ (**G1**). This is the F73 constituent cap and the Koide equipartition being the *same* $45°$ SO(2) point.
- **Massless-Koide endpoint (exact).** For $(m_h,m_\text{mid},0)$, $Q=\tfrac23\iff u=2-\sqrt3\iff\delta=15°$, so $\boxed{3\delta=\tfrac\pi4}$, $\cos3\delta=1/\sqrt2$ (F96) — reproduced to $10^{-6}$ (**G3**).

## 3. Why it cannot fix the interior (the negative)

The physical point sits **strictly inside** the coordinate: $3\delta^*=0.6667$ rad, between the democratic $0$ and the massless-Koide $\pi/4=0.7854$ (**G4**). Two independent facts block a geometric derivation of *where* inside:

**(a) No second kinematic relation (F199 S1).** $Q=\tfrac13+\tfrac16r^2$ is **exactly $\delta$-independent** ($\partial Q/\partial\delta\equiv0$): $Q$ is the radial amplitude, $3\delta$ the orthogonal angular coordinate on the *same* circle. There is no geometric second equation to intersect with the minimiser and force $3\delta=Q$. The only equation fixing $\delta$ is $\cos3\delta^*=-B/(2C)$ — which lives in the **dynamics**, not the geometry.

**(b) Dimensional no-go (the sharpening).** The interior value $3\delta^*=Q$ equates a **radian** (an angle) to a **pure ratio** (a mass combination). Crystal-field geometry produces only two currencies — trig ratios ($\cos, \sin$ of symmetry angles) and rational irrep multiplicities (the $O_h$ character integers) — **neither of which is a radian-valued transcendental tied to a dimensionless ratio.** The endpoints it does fix are exactly of the allowed kind: $\delta=0$, $3\delta=\pi/4$ (a *pure* fraction of $2\pi$), $\phi=45°$. The interior $3\delta^*=\tfrac23$ rad is not a rational multiple of $\pi$; it can only arise if a **dynamical scale** ($\lambda_6$, i.e. $\alpha_\text{eff}^*$) sets $B/C$ so that $\arccos(-B/2C)=Q$. Geometry has no such scale. (This is the lepton-sector twin of F232's theorem: a number of the wrong *kind* cannot come from geometry alone.)

The residual character is exactly F199's: the cubic $B$ is an $O(\alpha^0)$ sea loop, the sextic $C$ is an $O(\alpha^{\ge1})$ induced coupling, so $C/\lvert B\rvert\propto\alpha_\text{eff}^*$ is a **computed nonperturbative number**, and the bare Fierz rational $\tfrac29$ gives $\delta^*=10.25°$ (miss $2.48°$), $\tfrac14$ gives $13.40°$ (miss $0.67°$) — neither reproduces $12.73°$ (F179 D2, F199).

## 4. The target is real (Koide confidence), just not derived

The relation is currently satisfied at Koide confidence: $|3\delta^*-Q|=2.84\times10^{-5}$ (**G2**), $\delta^*$ vs $\tfrac29$ rad to $0.003\%$ (**G2b**) — $-0.89\sigma$ of the PDG $m_\tau$ error (F179 D3). Granting it (plus $Q=\tfrac23$ and one anchor) fixes the whole spectrum to $0.01\%$ (F179 D4). So $\delta^*=\tfrac29$ rad is a **target with a rationale**, answerable only by the saturated-condensate solve that delivers $\alpha_\text{eff}^*$ (F124/F144/F145/F151/F152 cluster) — which this finding, like F179/F199, does not perform.

## 5. Cross-sector echo (flagged, not claimed)

$\sin^2\theta_W=\tfrac29$ (a **ratio**, F49 BCC $2{:}7$ counting) and $\delta^*=\tfrac29$ rad (a **radian**, this sector) share the same rational. By the §3(b) dimensional argument these are **dimensionally distinct** objects; the coincidence is most likely a shared BCC-rational artifact, **not** a derivation link. Flagged open (**G5**), and cross-referenced to F231 (which shows $\tfrac29$ in the EW sector is the *on-shell* face of $\tfrac14$, further weakening any direct tie to a radian angle).

## 6. Check summary (`test_F230_lepton_angle_geometric_nogo.py`, 2026-07-02 - 16:35)

| # | Statement | Tier | Result |
|---|---|---|---|
| G1 | equipartition $r=A/\bar y\to\sqrt2$ ($Q=\tfrac23$, $\phi=45°$) | data/geometry | PASS |
| G2 | $3\delta^*=Q$ to $2.8\times10^{-5}$; $\delta^*$ vs $\tfrac29$ rad to $0.003\%$ | target | PASS |
| G3 | massless endpoint $\delta=15°$, $3\delta=\pi/4\neq Q$ | exact/anchor | PASS |
| G4 | geometry fixes endpoints $\{0,\pi/4\}$; interior is dynamics-set | structural/negative | PASS |
| G5 | echo $\sin^2\theta_W=\tfrac29$ (ratio) vs $\delta^*=\tfrac29$ rad (radian): dimensionally distinct | flag/open | PASS |

**Overall 6/6 PASS** (<1 s).

## 7. Verdict

The crystal-field + equipartition geometry E1 requested reproduces the spectrum's **endpoints** exactly (democratic $0$; massless-Koide $3\delta=\pi/4$; equipartition $45°$) but **cannot** fix the interior stopping point $3\delta^*=\tfrac23$ rad: there is no second kinematic relation ($Q$ is $\delta$-blind), and a radian value cannot be forced equal to a dimensionless ratio by trig-ratio/integer geometry without a dynamical scale. The derivation **closes negative** — the missing input is the saturated-condensate self-coupling $\lambda_6\!\propto\!\alpha_\text{eff}^*$ that sets $B/C$. This reaches, by the geometric route, the same terminus as F199 (BPS route) and F179 (induced-coupling route); the three now converge. $\delta^*=\tfrac29$ rad stands as the sharp, Koide-confidence lepton-sector **target**.

## 8. Provenance

- **New content:** the geometric-route attempt and its endpoint/interior decomposition; the dimensional no-go (radian $\neq$ ratio from trig/integer geometry, §3b); the explicit $\sin^2\theta_W$-vs-$\delta^*$ echo assessment (§5).
- **Reused:** F199 (the three structural no-gos), F179 (relabel, D2/D3/D4), F96 (massless endpoint $3\delta=\pi/4$), F80 ($Q(\phi)$, equipartition), F92 ($Q$ $\delta$-blind), F76/F75 ($T_{1u}$ crystal field). PDG masses ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86\pm0.12$ MeV).
- **Verification:** `tests/findings/test_F230_lepton_angle_geometric_nogo.py` (2026-07-02 - 16:35, 6/6 PASS), results `test-results/F230_lepton_angle_geometric_nogo.json`. Real arithmetic only — numpy-safe.
