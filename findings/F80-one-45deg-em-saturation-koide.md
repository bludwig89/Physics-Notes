# F80 — One 45°: the charged-lepton Koide point and the F73 bound-pair cap are the same SO(2) equipartition, selected by electromagnetism

**Date:** 2026-06-02 - 11:57
**Status:** Partial — 4/4 checks PASS + 1 honest residual recorded. **Exact/derived:** the amplitude-rotation→Koide map $Q(\phi)=1/(3\cos^2\phi)$, the SO(2) unification of the F73 constituent cap and the generation equipartition (the *same* 45° equal-split), and that the measured leptons sit at $\phi=45°$. **Hypothesis (the user's insight, now testable):** electromagnetism is the *selector* — only charged leptons couple to the clean abelian rotation, so only they land on the critical point; quarks (QCD-contaminated) and neutrinos (neutral) do not. **Honest residual:** perturbative EM is ~340× too weak to be the *driver*; EM explains *which sector*, not the *magnitude* of the 45° rotation.
**Script:** `model-tests/test_F80_em_saturation_45deg.py` (<1 s)
**Results:** `test-results/F80_em_saturation_45deg.json`
**Numbering note:** built concurrently with the structural-Newton-constant finding that took **F79**; this 45°/EM-selection finding is **F80**.
**Cross-references:** [[F78-koide-amplitude-from-cooper-pair]] (the $\sqrt m$ amplitude and the equipartition characterisation this closes), [[F77-njl-gap-rpa-selfconsistent]] (the dynamical-mass / gap machinery), [[F73-spin0-bound-pair-scalar]] (the 45° stability cap $\arcsin m_c=\pi/4$), [[F76-generation-mass-hierarchy-crystal-field]], [[F75-three-generations-from-bcc-irrep-selection]], [[F47-majorana-seesaw-higgs-free]] (the neutral-lepton mass route that lacks the EM rotation).

---

## 1. The two things asked

F78 left a single sharp question: *show the lepton condensate is driven to the
critical midpoint $Q=\tfrac23$ by the same dynamics that cap the F73 pair at
$\arcsin m_c = 45°$, and explain why only charged leptons sit there.* This
finding (i) makes the "same dynamics / same 45°" precise and exact, and (ii)
implements the proposed answer to the selection — **electromagnetism** — as a
falsifiable rule, while being explicit about what it does and does not settle.

---

## 2. The exact map: rotation angle → Koide ratio (D1)

Write the amplitude vector $\mathbf y=\sqrt m$ as a unit-scale vector rotated by
an angle $\phi$ off the democratic axis $\hat n=(1,1,1)/\sqrt3$:

$$\mathbf y = R\big[\cos\phi\,\hat n + \sin\phi\,\hat u\big],\qquad \hat u\perp\hat n.$$

Because the perpendicular ($T_{1u}$) part contributes nothing to the (signed)
sum, $\sum y=\sqrt3\,R\cos\phi$ and $\sum y^2=R^2$, so

$$\boxed{\;Q(\phi)=\dfrac{\sum y^2}{(\sum y)^2}=\dfrac{1}{3\cos^2\phi}\;}$$

with three landmark angles (all verified exactly):

| $\phi$ | $Q$ | meaning |
|---|---|---|
| $0°$ | $1/3$ | democratic floor (degenerate generations) |
| $\mathbf{45°}$ | $\mathbf{2/3}$ | **equipartition (the charged-lepton point)** |
| $54.7356°=\arccos\tfrac1{\sqrt3}$ | $1$ | single-axis ceiling (one massive generation) |

So $Q=2/3$ is *exactly* a 45° rotation of the mass amplitude away from
democracy.

---

## 3. The unification: it is the same SO(2) rotation as F73 (D2)

Both of the model's mass "rotations" are a unit 2-vector turned by an angle,
whose two squared components (weights) are $\cos^2,\sin^2$ and become **equal at
45°**:

- **F73 constituent (bound-pair):** the constituent carries
  $(n_c,m_c)=(\cos t,\sin t)$ — the kinetic complement and the rest mass. The
  pair phase $\Omega_\text{pair}=2t$ saturates the stability bound at
  $\Omega=\pi/2$ exactly when $t=45°$, i.e. $m_c=1/\sqrt2$, where **rest and
  kinetic weights equipartition** ($\sin=\cos=1/\sqrt2$).
- **Generation (Koide):** the amplitude carries $(\text{common},\text{diff})=(\cos\phi,\sin\phi)$ — the $A_{1g}$ democratic mode and the $T_{1u}$ splitting. Koide equipartition $|A_{1g}|=|T_{1u}|$ is exactly $\phi=45°$.

Numerically the two states are the **identical 45°-rotated unit vector**
$(1/\sqrt2,1/\sqrt2)$, and the F73 pair phase there is exactly $\pi/2$. The
constituent-level 45° of F73 and the generation-level 45° of Koide are **one and
the same object** — the equal-split point of a 2-channel unitary rotation. This
is the single thread linking the bound-pair sector (F73/F74/F77) to the
generation/Koide sector (F75/F76/F78): *mass is an SO(2) rotation, and 45° is its
distinguished equipartition angle, appearing once per level.*

---

## 4. The charged leptons sit at the 45° saturation (D3)

Inverting the map on the measured charged-lepton masses,

$$\phi_\text{lepton}=\arccos\sqrt{\tfrac{1}{3Q_\text{lepton}}}=44.99974°\;=\;\underbrace{\arcsin\tfrac1{\sqrt2}}_{\text{F73 cap}}=45°.$$

The charged-lepton mass amplitude is **at the saturation angle** — the same 45°
that caps the F73 bound pair, to one part in $10^5$.

---

## 5. Why only charged leptons: electromagnetism as the selector (D4)

The proposed reason the *charged leptons* (and not the others) land on the
critical point is that **only they couple to the clean, abelian, long-range EM
rotation** — uncontaminated by colour and present at all (unlike the neutral
sector). The data are consistent with this selection:

| sector | EM coupling | $Q$ | at $2/3$? |
|---|---|---|---|
| charged leptons $e,\mu,\tau$ | full ($q=-1$), no colour | $0.66666$ | **yes (45°)** |
| up-type quarks $u,c,t$ | $q=+\tfrac23$, **+ colour/QCD** | $0.849$ | no |
| down-type quarks $d,s,b$ | $q=-\tfrac13$, **+ colour/QCD** | $0.731$ | no |
| neutrinos $\nu$ | **none** ($q=0$; Majorana/seesaw, F47) | ordering-dependent $0.34$–$0.59$ | no (unpinned) |

Quarks carry the EM rotation too, but their mass dynamics are **dominated by the
non-abelian QCD condensate**, which pushes them off the clean EM point (and the
two quark charges give two *different* $Q$'s, $0.85\neq0.73$ — no universal
value). Neutrinos have **no EM rotation at all** (they are neutral; their mass
is the Majorana/seesaw route of F47), so nothing pins them to $2/3$, and indeed
their Koide ratio is not even well-defined yet (it swings $0.34$–$0.59$ with the
unknown lightest mass and ordering). The large leptonic *mixing* (near
tribimaximal PMNS), in contrast to the small quark CKM mixing, is the
independent democratic signature of the neutral sector.

So **electric charge is the selection rule**: the unique sector that is
EM-coupled *and* colour-free — the charged leptons — is the one sitting exactly
at the universal 45° critical point.

---

## 6. Honest residual: EM selects the sector, it does not supply the magnitude (D5)

The rotation from democracy ($\phi=0$, $Q=1/3$) to equipartition ($\phi=45°$,
$Q=2/3$) is a **full 45°**. A *perturbative* electromagnetic self-energy supplies
only

$$\Delta\phi_\text{EM}\sim\frac{\alpha}{\pi}=0.13°,\qquad \frac{45°}{0.13°}\approx340.$$

Perturbative EM is therefore ~$340\times$ too weak to *drive* the rotation. The
electromagnetic interaction can explain **which** sector sits at the critical
point (the selection of §5), but **not the magnitude** of the rotation. The
value 45° (equipartition, $Q=2/3$) is a *critical/saturation* condition — pinned
by the data and now expressed as a single clean statement ($\phi=45°$) — whose
derivation from the **non-perturbative EM-driven gap** remains open. Two hints
toward that derivation, both flagged as suggestive only:

1. The recurrence of $1/\sqrt2$/45° at *both* levels (F73 constituent cap, and
   the $C_{3v}$ analysis of F78-B4) says the leptons sit at a genuine
   **criticality** of the pairing dynamics, not at a generic coupling value.
2. The Cooper pair is a **spin-0 singlet** $(\!\uparrow\downarrow-\downarrow\uparrow)/\sqrt2$ — itself a maximally-mixed $1/\sqrt2$ (45°) state. The generation-space equipartition may be the image of the pair's own internal $1/\sqrt2$ structure. (Conjecture.)

---

## 7. Test summary (`test_F80_em_saturation_45deg.py`, 2026-06-02 - 11:57)

| Check | Statement | Result | Status |
|---|---|---|---|
| D1 | $Q(\phi)=1/(3\cos^2\phi)$; $45°\to2/3$ | exact at $0/45/54.74°\to1/3,2/3,1$ | PASS |
| D2 | SO(2) unification of F73 cap & Koide | identical $(1/\sqrt2,1/\sqrt2)$; $\Omega_\text{pair}=\pi/2$ | PASS |
| D3 | leptons at the 45° saturation | $\phi_\text{lepton}=44.99974°=$ F73 cap | PASS |
| D4 | EM selection rule | leptons $0.667$; quarks $0.85,0.73$; $\nu$ unpinned | PASS |
| D5 | honest residual (recorded) | perturbative EM $0.13°$ vs $45°$ needed (340×) | (info) |

**Overall 4/4 PASS** (+ recorded residual).

---

## 8. Verdict

**Answered (exact):** "the same dynamics" is now precise — the F73 constituent
stability cap and the generation Koide equipartition are *the identical SO(2)
rotation evaluated at the same 45°*, and $Q(\phi)=1/(3\cos^2\phi)$ makes
$45°\leftrightarrow2/3$ exact. The charged leptons sit at that 45°.

**Answered (mechanism, as a selection rule):** electric charge selects the
sector — only the EM-coupled, colour-free charged leptons land on the universal
critical point; QCD pushes the quarks off, and the neutral neutrinos are
unpinned. This is the user's electromagnetic insight, and it survives the data
contrast.

**Still open (sharpened to one line):** *why the charged-lepton EM criticality
falls exactly at the equipartition angle 45° rather than anywhere else.*
Perturbative EM cannot supply it (340× too weak); it is a non-perturbative
critical condition, plausibly the image of the Cooper-pair singlet's own
$1/\sqrt2$ — the next thing to derive.

---

## 9. Provenance

- Closes the open question posed at the end of F78; the SO(2) unification, the
  $Q(\phi)$ map, and the EM selection rule are new.
- Verification: `model-tests/test_F80_em_saturation_45deg.py`
  (2026-06-02 - 11:57, 4/4 PASS + residual), results
  `test-results/F80_em_saturation_45deg.json`.
- Masses: PDG charged leptons; PDG quark masses (scheme-rough, conclusion
  robust); neutrino $\Delta m^2_{21}=7.5\times10^{-5}$, $\Delta m^2_{31}=2.5\times10^{-3}$ eV².
