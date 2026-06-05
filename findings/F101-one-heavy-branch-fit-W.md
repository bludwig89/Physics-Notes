# F101 — The one-heavy lepton branch located and exactly fitted: the sea cliff pins $m_\tau$ at saturation, the closed-form coupling family carries the exact spectrum, F95's angle requirement and the spectrum fit select the same $W\approx1.5$ — and two sharp negatives (metastability; static RPA has the wrong sign)

**Date:** 2026-06-05 - 14:20
**Numbering note:** F97 was taken by the concurrent baryon-phase finding; this is **F101** (F98–F100 also taken by concurrent findings during the build).
**Status:** Partial (located + fitted + cross-validated, with two honest negatives) — 6/6 checks PASS. **New exact structure:** (A0) the BCC sea has a **cliff** at saturation — $f'(m)\to-\infty$ as $m\to1$ (the arccos edge of the F46 dispersion) — so an interior heavy flavor is *always* a saddle: the heavy generation is **forced onto the wall exactly**, $y_\tau=1$. The τ mass *is* the saturation scale — the sharpest scale statement the chain has produced. (A1) With the τ wall-pinned, the inverse problem is **linear**: the two light-flavor stationarity equations give $(\kappa_E,\mu)(W)$ in closed form — the exact measured spectrum $(1,\sqrt{m_\mu/m_\tau},\sqrt{m_e/m_\tau})$ is a genuine KKT local vacuum of the $W$-completed gap theory along a one-parameter family, $W\in[0.10,21.6]$, with $W>0$ **emergent** and $r=\kappa_E/\kappa_0\approx0.986$ (a near-pure per-flavor contact). (B) **Two independent routes meet:** F95's Landau localization $C=0.636|B|$ selects $W^*=6C/e^6=1.46$ — *inside* the admissible window, with all KKT conditions holding at exactly that point. **The honest negatives:** (A2) along the minimal 3-coupling family the lepton point is **metastable** — squeezed between the all-saturated $(1,1,1)$ vacuum (small $W$) and the empty $(0,0,0)$ vacuum (large $W$), closest gap $2.5\times10^{-2}$ at $W\approx0.69$; (C) the static uniform-mode RPA gives a **negative** sextic (an anti-brake) and loses positivity near the wall — $W$ is *not* derivable at static one-loop. See §6.
**Script:** `model-tests/test_F101_one_heavy_branch_fit_W.py` (~40 s)
**Results:** `test-results/F101_one_heavy_branch_fit_W.json`
**Cross-references:** [[F96-second-shell-Eg-gap-saturation]] (the framework; the wall result this sharpens), [[F95-B-derived-C-localized]] (the $C=0.636|B|$ requirement that meets the fit at $W^*=1.46$), [[F93-orthorhombic-Eg-vacuum]] (the $E_g$ condensate), [[F92-per-constituent-phase-consistency]] (saturation kinematics), [[F83-fix-lattice-spacing-from-fermion-mass]] (the scale question A0 sharpens), [[F46-pythagorean-lattice-mass]] (the dispersion whose arccos edge is the cliff).

---

## 1. A0 — the cliff: $m_\tau$ sits at saturation *exactly*

The sea energy per generation, $f(m)=-\langle\arccos(\sqrt{1-m^2}\cos\omega_\text{kin})\rangle_\text{BZ}$, has divergent slope at the saturation edge: numerically $g'(y)=-0.41,\ -1.50,\ -4.98,\ -13.6$ at $y=0.9,\,0.99,\,0.999,\,1.0$ (table-limited; the true slope diverges as $-m/\sqrt{1-m^2}$ from $d\sqrt{1-m^2}/dm$). Consequence: any *interior* heavy flavor is a saddle (verified: the interior fit at $s=0.9$ has Hessian eigenvalue $-1.94$). The heavy generation cannot hover near the wall — it must sit **on** it:

$$\boxed{\;y_\tau=1\ \text{exactly: the τ mass is the saturation scale of the condensate.}\;}$$

This converts F96's "heavy at the wall" from a phase-map observation into a structural theorem of the sea, and it is the first statement in the chain that *pins a physical mass to a lattice-intrinsic scale* (the condensate-internal saturation point). The F83/F92 scale question is now: what maps the saturation scale to 1776.86 MeV.

## 2. A1 — the exact fit: a closed-form one-parameter family

With $y_\tau=1$ pinned (wall KKT inequality), the two light-flavor stationarity
conditions

$$\kappa_E y_a+\mu\bar y+g'(y_a)+2WS_3(3p_a^2-P_2)=0,\qquad a=\mu,e$$

are **linear** in $(\kappa_E,\mu)$ at given $W$ — closed-form solution per $W$.
Scanning $W\in[0.05,30]$: admissible window $W\in[0.096,21.6]$ (positivity,
wall KKT margin $-12.7$, constrained $2\times2$ Hessian PD). Sample at
mid-window ($W=1.57$): $\kappa_E=0.702$, $\mu=0.0103$, $\kappa_0=0.713$,
$r=0.9855$. Two notable emergent facts:

- $W>0$ over the *whole* family — the brake sign was not imposed;
- $\mu\ll\kappa$: the fitted interaction is a **near-pure per-flavor contact**
  ($r\approx0.99$), with the structure carried almost entirely by $W$ — a
  two-number theory at heart.

## 3. B — the convergence: F95's angle requirement = the spectrum fit

At the lepton point's invariants ($\bar y=0.4203$, $e=0.728$), the sea's cubic
projection is $B_\text{sea}=-5.69\times10^{-2}$, so F95's requirement
$C=|B|/(2\times0.785874)=0.636|B|$ gives

$$W^*=\frac{6\,C_\text{req}}{e^6}=1.46,$$

which lies **inside** the KKT-admissible window, and the closed-form fit at
exactly $W^*$ is fully admissible ($\kappa_E=0.657$, $\kappa_0=0.666$,
Hessian PD, wall margin $-12.8$). Two completely independent constructions —
the F95 Landau angular analysis and the F101 spectrum KKT fit — select the
same brake strength. The theory's one nontrivial coupling is now pinned from
two directions: $W\approx1.5$ in lattice-sea units.

## 4. A2 — honest negative #1: metastability in the minimal form

Global-minimality scan along the family: the lepton point is never the global
ground state. The competitors:

| regime | ground state | E(lepton)−E(ground) |
|---|---|---|
| small $W$ ($\lesssim0.7$) | $(1,1,1)$ all-saturated | $0.27\to0.025$ (falling) |
| large $W$ ($\gtrsim1.3$) | $(0,0,0)$ empty | growing with $W$ |

Closest approach $2.5\times10^{-2}$ at $W\approx0.69$ — the crossover between
the two competitors. Within the strict 3-coupling form the squeeze is
arithmetic: beating $(1,1,1)$ needs a large democratic cost, beating $(0,0,0)$
needs a small total cost, and the light-flavor fit equations leave no room for
both. Promoting the lepton point to the true vacuum requires **one additional
democratic-sector invariant** (e.g. a quartic $\bar y$ cost — it would punish
$(1,1,1)$ without disturbing the light-flavor equations). Deliberately *not*
added here: the next term should be derived, not decorated. (Flagged
speculation, one line: a theory whose three competing vacua are an empty
triplet, a one-heavy triplet, and a degenerate saturated triplet invites a
sector reading — neutrino-like / charged-lepton / quark-like — but nothing
here supports it beyond the pattern.)

## 5. C — honest negative #2: static RPA has the wrong sign

The simplest candidate derivation of $W$ — the uniform-mode Gaussian
fluctuation energy $E_\text{fl}=\tfrac12\ln\det[K+\mathrm{diag}(g''(y_a))]$ of
the same theory — fails informatively:

- wherever defined (probe circles $e_\text{probe}\le0.30$), its sextic
  projection is **negative**: fluctuations *soften* where one flavor is heavy
  — an anti-brake;
- for $e_\text{probe}\gtrsim0.35$ the operator loses positivity (the cliff
  curvature $g''\to-\infty$): the unconstrained Gaussian treatment is invalid
  near the wall.

So the brake does **not** come from static one-loop fluctuations. The
precisely-posed remaining computation is the **momentum-resolved
$E_g$-channel bubble** (the $q\neq0$ stiffness the static approximation
discards is exactly what can flip the sign), and/or the second-shell bond
self-energy — with a hard target: it must produce $C=0.636|B|$, i.e.
$W\approx1.5$, and restore positivity near the wall (where the wall constraint
itself regularizes the cliff).

## 6. Ledger after F92→F101

| item | status |
|---|---|
| generation count = 3 | theorem (F75) |
| splitting field = $E_g$, 2nd shell, spontaneous | theorem (F93) |
| $\kappa=0$ flatness | stabilizer theorem (F93) |
| Landau angular form | derived (F95-D1) |
| $B$ (cubic) | derived, closed form $-3\sqrt2I_2\bar y^4$ (F95) |
| quadratic theory | excluded (two-value theorem, F96) |
| $m_e=0$ texture algebra | exact; $Q=2/3\iff\delta=15°$ (F96) |
| $m_\tau$ scale | **at saturation exactly** (F101-A0) |
| lepton spectrum as a vacuum | exact KKT local vacuum, closed-form couplings (F101-A1) |
| $W$ size | pinned two ways to $\approx1.5$ (F95↔F101-B) |
| $W$ derivation | open — static RPA wrong sign; momentum-resolved bubble posed (F101-C) |
| global stability | open — one democratic invariant short (F101-A2) |
| absolute scale (saturation ↔ MeV) | open (sharpened by A0) |

## 7. Test summary (`test_F101_one_heavy_branch_fit_W.py`, 2026-06-05 - 14:15)

| Check | Statement | Result | Status |
|---|---|---|---|
| A0 | cliff: $g'\to-\infty$ at the wall; interior-heavy is a saddle | $-13.6$ (table edge); eig $-1.94$ | PASS |
| A1 | wall-pinned closed-form fit; $W>0$ emergent | window $[0.096,21.6]$, $r\approx0.986$ | PASS |
| A2 | metastability quantified; competitors identified | closest gap $2.5\times10^{-2}$ @ $W=0.69$ | PASS |
| B | F95's $C=0.636\lvert B\rvert$ ⇒ $W^*=1.46$ inside the window | admissible at $W^*$ | PASS |
| C | static RPA sextic negative; non-PD near wall | all computed $W_\text{RPA}<0$ | PASS |
| D | verdict recorded | — | PASS |

**Overall 6/6 PASS.**

## 8. Provenance

- New content: the cliff theorem and the exact wall-pinning of $m_\tau$ (A0);
  the linear inverse structure and the closed-form coupling family (A1); the
  F95↔F101 two-route convergence on $W\approx1.5$ (B); the quantified
  metastability and its squeeze argument (A2); the static-RPA wrong-sign
  no-go (C).
- Machinery: `ca_bcc.bcc_dispersion` + F46 sea, pure-numpy minimizer (no
  scipy), numerical KKT/Hessian checks.
- Verification: `model-tests/test_F101_one_heavy_branch_fit_W.py`
  (2026-06-05 - 14:15, 6/6 PASS), results
  `test-results/F101_one_heavy_branch_fit_W.json`.
- Masses: PDG charged leptons.
