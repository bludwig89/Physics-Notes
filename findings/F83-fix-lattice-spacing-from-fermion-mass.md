# F83 — Fixing the lattice spacing $a$ from a measured fermion mass: the F46/F12 map gives a relation, not a value; the heaviest fermion sets the ceiling

> **Numbering note:** F82 was taken by a concurrent finding (`F82-why-saturation-composite-mass-peak.md`, 2026-06-02 - 19:38); this is **F83**.

**Date:** 2026-06-02 - 20:05
**Status:** Confirmed (negative/conditional result) — 5/5 checks PASS, round-trip at machine precision ($2.5\times10^{-16}$). The algebra is exact; the headline is that a single measured mass **cannot** fix $a$, but it imposes an exact ceiling and, once $a$ is pinned elsewhere, an exact $m_\text{lat}$.
**Module:** none new — analytic identity on F46 (rest-leg rotation) + F10/F26 (lightcone) + F61 (cell size).
**Verification script:** `tests/findings/test_F83_fix_lattice_spacing.py`
**Results:** `test-results/F83_fix_lattice_spacing.json`
**Cross-references:** F46 (spherical-Pythagorean lattice mass, $\Omega_\text{rest}=\arcsin m$), F12/F15 (SR dispersion + $\beta_\text{LV}$, the $m\ll1$ regime), F10 (the $\sqrt d$ Planck mismatch and its three resolutions), F26 ($c$ as rotation rate), F59/F61 (induced-$G$ cell size $a\approx3.81\,\ell_P$), `deprecated/si-units-options.md` §3.3 / §5 Option D.

---

## 1. Statement

The **F46/F12 lattice-mass map** carries a fermion's rest energy into SI through the F46 rest-leg rotation rate. With $\Omega_\text{rest}(m_\text{lat})=\arcsin(m_\text{lat})$ radians per tick (F46/F27, exact) and a tick of duration $\tau$,

$$
\boxed{\;m_\text{phys}\,c^2 \;=\; \hbar\,\frac{\arcsin(m_\text{lat})}{\tau}\;}\tag{$\star$}
$$

This is the exact map; $m_\text{lat}\in(0,1]$ is the dimensionless lattice mass and $\tau$ the tick. Converting the tick to the cell with the lattice-lightcone identity $a/\tau=c\sqrt d$ (F10 resolution 3 / F26 / si-units Option C),

$$
\boxed{\;a \;=\; \sqrt d\;\arcsin(m_\text{lat})\;\frac{\hbar}{m_\text{phys}\,c}\;=\;\sqrt d\;\arcsin(m_\text{lat})\;\bar\lambda_C\;}\tag{$\triangle$}
$$

where $\bar\lambda_C=\hbar/(m_\text{phys}c)$ is the **reduced Compton wavelength** of the fermion.

**The result of the attempt:** Eq. ($\triangle$) is *one equation in two unknowns* ($a$ and $m_\text{lat}$). A measured fermion mass alone therefore **does not fix $a$** — it fixes only the one-parameter family $a(m_\text{lat})$. This is the §7 "no first-principles $a$" caveat of `deprecated/si-units-options.md` made precise: the mass anchor (Option D) supplies a *relation*, and a second anchor is still required to pin the scale.

What the measured mass *does* fix exactly:

1. **A ceiling on $a$.** Since $\arcsin(m_\text{lat})\le\pi/2$,
   $$a \;\le\; a_\text{max}(m_\text{phys}) \;=\; \sqrt d\,\frac{\pi}{2}\,\bar\lambda_C \;=\; \frac{\sqrt d\,\pi\hbar}{2\,m_\text{phys}c}.$$
   The ceiling is tightest for the **heaviest** fermion (smallest $\bar\lambda_C$). The top quark gives $a\le 3.11\times10^{-18}\,\text{m}$.

2. **An exact $m_\text{lat}$ once $a$ is pinned independently.** Inverting ($\triangle$), $m_\text{lat}=\sin\!\big(a/(\sqrt d\,\bar\lambda_C)\big)$. With the F59/F61 induced-gravity cell $a\approx3.81\,\ell_P$, every charged fermion lands at $m_\text{lat}\ll1$ (electron $9.2\times10^{-23}$), confirming the small-mass regime F12/F15 assume.

---

## 2. Why a single mass cannot fix $a$ (the degeneracy)

($\star$) relates the *measured* $m_\text{phys}$ to the *product structure* $\arcsin(m_\text{lat})/\tau$. The lattice carries two free scales here — the dimensionless mass $m_\text{lat}$ and the tick $\tau$ (equivalently the cell $a$) — and the measurement constrains only their combination. Concretely (script test **T5**), the electron mass $0.511\,\text{MeV}$ is reproduced *exactly* by an entire family of lattices:

| $m_\text{lat}$ | $a$ solving ($\triangle$) | $a/\ell_P$ | recovered mass |
|---|---|---|---|
| $10^{-30}$ | $6.7\times10^{-43}$ m | $4.1\times10^{-8}$ | 0.511 MeV |
| $10^{-23}$ | $6.7\times10^{-36}$ m | $0.41$ | 0.511 MeV |
| $0.5$ | $3.5\times10^{-13}$ m | $2.2\times10^{22}$ | 0.511 MeV |
| $0.999$ | $1.0\times10^{-12}$ m | $6.5\times10^{22}$ | 0.511 MeV |

Every row satisfies ($\star$) to round-off. The mass fixes the *ray* $a=\sqrt d\,\arcsin(m_\text{lat})\,\bar\lambda_C$ in the $(a,m_\text{lat})$ plane, nothing more. This is exactly the over-/under-determination `deprecated/si-units-options.md` §2 flagged: three SI base units need three anchors; $c$ fixes $a/\tau$, $\hbar$ is the action quantum, and *one* mass fixes one combination — leaving the absolute scale $a$ free.

---

## 3. The ceiling: the top quark is the tightest mass constraint on $a$

Because all fermions must live on the *same* lattice (one $a$), and each needs $m_\text{lat}\le1$, the heaviest fermion imposes the smallest $a_\text{max}$. Test **T2** (PDG 2024 masses, $d=3$):

| fermion | $m$ (MeV) | $\bar\lambda_C$ (m) | $a_\text{max}=\sqrt d\,\tfrac\pi2\bar\lambda_C$ (m) | $a_\text{max}/\ell_P$ |
|---|---|---|---|---|
| **top** | $1.726\times10^5$ | $1.14\times10^{-18}$ | $\mathbf{3.11\times10^{-18}}$ | $1.9\times10^{17}$ |
| bottom | 4180 | $4.72\times10^{-17}$ | $1.28\times10^{-16}$ | $7.9\times10^{18}$ |
| tau | 1776.86 | — | $3.02\times10^{-16}$ | $1.9\times10^{19}$ |
| charm | 1270 | — | $4.23\times10^{-16}$ | $2.6\times10^{19}$ |
| muon | 105.66 | — | $5.08\times10^{-15}$ | $3.1\times10^{20}$ |
| strange | 93.4 | — | $5.75\times10^{-15}$ | $3.6\times10^{20}$ |
| down | 4.67 | — | $1.15\times10^{-13}$ | $7.1\times10^{21}$ |
| up | 2.16 | — | $2.49\times10^{-13}$ | $1.5\times10^{22}$ |
| electron | 0.511 | $3.86\times10^{-13}$ | $1.05\times10^{-12}$ | $6.5\times10^{22}$ |

So the *measured fermion spectrum* alone forces $a\lesssim 3\times10^{-18}\,\text{m}$ — about **17 orders of magnitude above** the Planck length. The mass anchor is real but extraordinarily loose: it rules out a lattice coarser than $\sim10^{-18}\,$m (the top-quark Compton scale) and nothing finer. The Planck-scale cell the rest of the project uses ($a\approx3.81\,\ell_P\approx6\times10^{-35}$ m, F61) sits comfortably $\sim17$ decades below this ceiling, i.e. consistent but not selected by it.

---

## 4. Closing the degeneracy: pin $a$ with F61, read off $m_\text{lat}$

The complementary use of ($\triangle$) is the productive one. Take $a$ from the **independent** induced-Newton-constant derivation (F59/F61: $a=\sqrt{2\pi\eta g_*}\,d^{1/4}\ell_P$, $\eta=1/12$, $g_*=16$ ⇒ $a=3.81\,\ell_P=6.16\times10^{-35}$ m) and invert. Test **T3** ($m_\text{lat}=\sin(a/(\sqrt d\,\bar\lambda_C))$, indistinguishable from the linear $a/(\sqrt d\,\bar\lambda_C)$ at this scale to $\sim10^{-44}$):

| fermion | $m_\text{lat}$ at $a=3.81\,\ell_P$ |
|---|---|
| electron | $9.21\times10^{-23}$ |
| up | $3.89\times10^{-22}$ |
| down | $8.41\times10^{-22}$ |
| strange | $1.68\times10^{-20}$ |
| muon | $1.90\times10^{-20}$ |
| charm | $2.29\times10^{-19}$ |
| bottom | $7.53\times10^{-19}$ |
| tau | $3.20\times10^{-19}$ |
| top | $3.11\times10^{-17}$ |

All $m_\text{lat}\ll1$ — the regime in which F12/F15's $\beta_\text{LV}\approx-m_\text{lat}^2/6$ Lorentz-violation deformation is utterly negligible ($\sim10^{-44}$ for the electron), and in which $\arcsin(m_\text{lat})\approx m_\text{lat}$ to $\sim10^{-44}$ relative. This is the quantitative backing for the assumption, used throughout the SR sector, that laboratory fermions sit in the linear corner of the F46 spherical triangle.

---

## 5. A $\sqrt d$ correction to `deprecated/si-units-options.md` §3.3

`deprecated/si-units-options.md` §3.3 wrote the map as $m_\text{lat}=m_\text{phys}c\,a/\hbar$ and quoted $m_\text{lat}(e^-)\approx4\times10^{-23}$ at $a=\ell_P$. That expression uses $a/\tau=c$ (the naive Planck pairing), **not** the Option-C lightcone $a/\tau=c\sqrt d$ that the same document recommends in §6. The exact small-mass map from ($\triangle$) is

$$m_\text{lat}\;\approx\;\frac{m_\text{phys}\,c\,a}{\sqrt d\,\hbar}\qquad(\text{Option C}),$$

i.e. smaller by $\sqrt d$. Test **T4** confirms the arithmetic exactly: at $a=\ell_P$, the §3.3 formula gives $4.185\times10^{-23}$ (matching the quoted $\approx4\times10^{-23}$) while the Option-C value is $2.416\times10^{-23}$; their ratio is $1.73205=\sqrt3$ to $<10^{-6}$. The §3.3 estimate is internally a *different convention* (Option A/B, $a/\tau=c$); under the document's own preferred Option C the electron figure becomes $2.4\times10^{-23}$ at $a=\ell_P$ and $9.2\times10^{-23}$ at the F61 cell. Recommend annotating §3.3 with the $\sqrt d$ factor.

---

## 6. Test results (`test_F83_fix_lattice_spacing.py`, 2026-06-02 - 20:05)

| # | Test | Result | Target | Status |
|---|---|---|---|---|
| T1 | Round-trip $a\to m_\text{lat}=\sin(a/(\sqrt d\bar\lambda_C))\to a=\sqrt d\arcsin(m_\text{lat})\bar\lambda_C$, all 9 fermions | max rel residual $2.48\times10^{-16}$ | $10^{-14}$ | **PASS** |
| T2 | Per-fermion ceiling $a_\text{max}=\sqrt d\,\tfrac\pi2\bar\lambda_C$; tightest = heaviest | top, $3.11\times10^{-18}$ m | top | **PASS** |
| T3 | $m_\text{lat}$ at F61-pinned $a=3.81\,\ell_P$; all $\le1$ | all $m_\text{lat}\le3.1\times10^{-17}$ | $\le1$ | **PASS** |
| T4 | si-units §3.3 vs exact Option-C; expose $\sqrt d$ | ratio $=1.73205=\sqrt3$ | $\sqrt d$ | **PASS** |
| T5 | Degeneracy: many $(a,m_\text{lat})$ give same electron mass | exact along the ray | — | **PASS** |

Total **5/5 PASS**, pure-Python arithmetic (no numpy/scipy, per CLAUDE.md chiral-transform caution — not needed here, all real scalars).

---

## 7. What is derived vs assumed

**Exact (this finding):** the map ($\star$); the cell relation ($\triangle$) given the lightcone $a/\tau=c\sqrt d$; the degeneracy (mass fixes a ray, not a point); the ceiling $a\le\sqrt d\,\tfrac\pi2\bar\lambda_C$ with the top quark tightest; the $\sqrt d$ reconciliation with si-units §3.3; the round-trip to $2.5\times10^{-16}$.

**Imported / conditional:** the lightcone convention $a/\tau=c\sqrt d$ (F10 resolution 3 / F26 — a *choice*, the only one F26 forces but still a choice); the F61 cell $a=3.81\,\ell_P$ used in §4 (itself partial — F61's gauge-sector $g_*$ correction is open).

**Not closed:** $a$ is still not fixed from first principles. As `deprecated/si-units-options.md` §7 anticipated, the mass anchor is one constraint short; the missing second anchor is the gravity/EMQG match (F55/F56/L4 absolute lensing coefficient) or the F12 GRB Lorentz-violation floor. This finding sharpens the gap to a number: any first-principles $a$ must fall in $(\,0,\ 3.1\times10^{-18}\,]$ m to be consistent with the top quark, and at $3.81\,\ell_P$ predicts the $m_\text{lat}$ table of §4.

---

## 8. Open follow-ups (not blocking)

1. **Second anchor.** Combine ($\triangle$) with the absolute lensing coefficient $\Delta\theta=4GM/(bc^2)$ (F55/L4, carries an explicit $\sqrt d$, Finding 10) to pin $a$ independently of any mass, then test whether the resulting $a$ reproduces the F61 $3.81\,\ell_P$ — a genuine consistency check between the matter and gravity sectors.
2. **GRB floor.** Convert the §4 $m_\text{lat}$ values + F12/F15 $\beta_\text{LV}$ into an $E_\text{LV}(a)$ and verify $E_\text{LV}(3.81\,\ell_P)\gtrsim10^{19}$ GeV (Fermi GRB 090510). Expected to clear easily; quantifies the one *empirical* bracket on $a$.
3. **Annotate `deprecated/si-units-options.md` §3.3** with the $\sqrt d$ Option-C factor (§5 above).

---

## 9. Provenance

- Map source: F46 (rest-leg rotation $\arcsin m$) + `deprecated/si-units-options.md` §3.3/§5 Option D (mass anchor) + F10/F26 (lightcone $a/\tau=c\sqrt d$).
- Cell value: F61 ($a=3.81\,\ell_P$ for $g_*=16$).
- Masses: PDG 2024 central values; constants CODATA 2018 ($\hbar c=197.3270$ MeV·fm, $\ell_P=1.616255\times10^{-35}$ m).
- Numerical verification: `tests/findings/test_F83_fix_lattice_spacing.py` (2026-06-02, 5/5 PASS), `test-results/F83_fix_lattice_spacing.json`.
