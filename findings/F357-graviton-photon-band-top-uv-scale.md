# F357 — The paired photon/graviton band top: $\Omega_\text{max}=\pi$ exactly, and it sits at $0.8247\,E_\text{Planck}$ — a computed, closed-form answer to E12's "UV completion beyond lattice-is-cutoff", scoped independently of A11/K9's $\rho_\text{vac}$ residual

**Date:** 2026-09-03 - 16:45
**Status:** Candidate finding — 6/6 checks PASS. The pi-bound theorem (A, D) is **exact-algebraic** (sympy: an exact trig identity plus a strict-monotonicity argument, cross-checked numerically to $4.4\times10^{-16}$); the domain fact it rests on (B) is exact by construction; the zone-sweep confirmation (C) is **lattice-numeric** (dense $161^3$ sweep, residual $4.4\times10^{-16}$ — floating-point precision at the exact boundary point, not a discretization floor, see §2); the Planck-unit number and its relation to F352's cruder cutoff (E, F) are **exact-algebraic given F79/F107's registered ruler** $a/\ell_P$ (residuals $2.2\times10^{-16}$ and $8.9\times10^{-16}$ against the closed form, no new free input).
**Checked:** 2026-09-03 - 16:40 — 12 PASS / 1 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/interactions/gravity_band_cutoff.py` (real arithmetic + sympy; `casim.numerics.xp` for all array work, no chiral/complex spinor transform touched — this is a real scalar dispersion law throughout, per F248's own convention).
**Tests / results:** `tests/registry/interactions.yaml` id `F357-graviton-band-top` → `test-results/F357_graviton_band_cutoff.json` (6/6).
**Cross-references:** [[F248-tt-graviton-bcc-explicit]] (**the parent**: built the paired "even" dispersion law $\Omega_\text{even}(\mathbf K)=\omega_+(\mathbf K/2)+\omega_-(\mathbf K/2)$ this module bounds, and proved it is *the* physical photon/graviton law — non-birefringent, luminal, $k\to0$ slope $c_\text{lat}$ — but never asked for its band **top**), [[F69-paired-spinor-photon]] (why the law is the symmetric *pair* sum, not a single branch — the fact that makes the $\pi$ bound possible at all), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=d\Omega/d|k|$; $\Omega$ *is* the rotation angle per CA tick, the quantity this module puts a hard ceiling on), [[F79-structural-newton-constant]] / F61 (the structural ruler $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ and $a/\tau=c\sqrt3$ this module's Planck-unit conversion reuses verbatim, with zero new free input), [[F352-higgs-bhl-compositeness-rg-negative]] (the model's *other*, cruder UV-cutoff estimate $\Lambda_\text{model}=E_\text{Planck}/(a/\ell_P)\approx0.152\,E_\text{Planck}$ — this finding's F-check shows $E_\text{max}=\pi\sqrt3\,\Lambda_\text{model}$ exactly, i.e. the two numbers were never independent), [[F216-massive-spin2-dark-mode]] (established the graviton is exactly massless with 2 TT dof — the *kinematic identity* this module now puts a hard *energy ceiling* on), [[F264-qed-allorders-renormalizability-anomaly]] / the A11 rubric row (a **different, adjacent** residual — the finite-EFT-operator-coefficient count, of which $\rho_\text{vac}$ is the one still wrong; this finding does not touch it, see §1). External: Donoghue, "General relativity as an effective field theory" (gr-qc/9512024) and standard graviton-graviton unitarity-violation-at-$M_\text{Planck}$ EFT power counting (cited for scale only, no numeric coefficient imported).

---

## 1. Scoping: why this is not K9/A11 restated

The task prompt for rubric row **E12** (quantum-gravity sector, `docs/status/completeness-2026-08-20-prompts.md`) flags that its residual — *"UV completion beyond 'lattice is the cutoff' undeveloped"* — might be **the same object** as rubric row **A11**'s residual, which is explicitly the $\rho_\text{vac}$ EFT-operator coefficient (ledger row G1, off by 120.8 orders, the K9 cosmological-constant target). The prompt's own first step was to check this before doing new physics.

**It is not the same object, and the two open sessions already on it should not be duplicated.** At the time this session opened (`docs/design/session-claims.yaml`, session `quiet-precise-regge`):

- Session `lucid-candid-wheeler` is **open**, working A11 directly.
- Session `careful-lucid-lemaitre` is **open**, working K9/ledger-G1 directly — the actual $\rho_\text{vac}$ target A11 points to.

A11's own text (`completeness-2026-08-20-prompts.md`) is explicit that its content is a *Wilsonian EFT operator-coefficient count*: "exactly two cutoff-carrying coefficients exist with no free parameter: $G$ (right, to $3\times10^{-8}$) and $\rho_\text{vac}$ (wrong, by 120.8 orders)." That is a statement about which **local operators appear in the effective action below the cutoff and whether their coefficients match observation** — a completely different question from E12's own framing, which is about the graviton's **propagating kinematics** ("Graviton massless, 2 dof") and whether the theory supplies **a genuine energy ceiling**, not a slogan, for that propagating mode. F216/F248 already closed the kinematic-identity half (massless, 2 TT dof, luminal, non-birefringent); nobody had yet asked *what the top of that band actually is*, in Planck units, with a number. That is this finding's content, and it touches no file either open session owns (cosmology/EFT-counting modules for K9/A11 vs. this session's `interactions/gravity_band_cutoff.py`, a new file, plus one `Site()` addition to the already-shared `a_over_ellP` registry entry).

## 2. The result: $\Omega_\text{even}\le\pi$ exactly (A, B, D)

F248 built the photon/graviton dispersion as the **paired**, helicity-symmetric "even" law (F69):

$$\Omega_\text{even}(\mathbf K)=\omega_+(\mathbf K/2)+\omega_-(\mathbf K/2),\qquad \omega_\pm(\mathbf q)=\arccos\!\big(u_\pm(\mathbf q)\big),\qquad u_\pm(\mathbf q)=c_xc_yc_z\pm s_xs_ys_z,$$

with $c_i=\cos(q_i/\sqrt3)$, $s_i=\sin(q_i/\sqrt3)$. The natural single-constituent-branch Brillouin zone is, per `bcc.py`'s own comment, $|q_i|\le\pi\sqrt3/2$ (equivalently $\theta_i\equiv q_i/\sqrt3\in[-\pi/2,\pi/2]$), so on this domain $c_i\ge0$ for every $i$.

Write $a=u_+(\mathbf K/2)$, $b=u_-(\mathbf K/2)$. Then

$$a+b=2\,c_xc_yc_z\ \ge0\qquad\text{everywhere on the declared domain.}$$

**Theorem (A).** For $a,b\in[-1,1]$, $\arccos(a)+\arccos(b)\le\pi\iff a+b\ge0$, with equality iff $a+b=0$. *Proof:* $\arccos(-a)=\pi-\arccos(a)$ exactly — both $\pi-\arccos(a)$ and $\arccos(-a)$ lie in $[0,\pi]$ and $\cos$ is injective there, and sympy confirms $\cos(\pi-\arccos a)=-a$ identically. So $g(a,b)\equiv\arccos(a)+\arccos(b)-\pi$ vanishes exactly at $b=-a$ for every $a$, and $\partial g/\partial b=-1/\sqrt{1-b^2}<0$ strictly on $(-1,1)$ (sympy, exact), so $g$ is strictly decreasing in $b$: $g\le0$ (sum $\le\pi$) exactly when $b\ge-a$, i.e. $a+b\ge0$. Numeric cross-check over $2\times10^5$ random $a$: $\max|\arccos(a)+\arccos(-a)-\pi|=4.4\times10^{-16}$.

Combined with $a+b\ge0$ on the domain (check B, exact by construction — $\cos$ of an angle in $[-\pi/2,\pi/2]$), this **forces**

$$\boxed{\Omega_\text{even}(\mathbf K)\ \le\ \pi\quad\text{everywhere on the BCC Brillouin zone, exactly.}}$$

**Equality is exact and holds on the whole zone boundary, not just at corners (D).** Setting any one constituent angle to its own edge, $\theta_x=\pi/2$ ($c_x=0$), gives $u_+=s_xs_ys_z$ and $u_-=-s_xs_ys_z=-u_+$ — sympy confirms $u_++u_-\to0$ identically, for **every** $\theta_y,\theta_z$, not merely at special points. So $\Omega_\text{even}=\pi$ exactly on an entire boundary face, and the maximum is attained (a supremum that is reached, not merely approached).

**Numeric confirmation (C).** A dense $161^3$ sweep of the pair momentum $|K_i|\le\pi\sqrt3$ (the pair carries $\mathbf K=2\mathbf q$, so its own zone is double the single-branch one) finds $\max\Omega_\text{even}=3.14159265358979\ldots$, i.e. $\pi$ to a residual $4.4\times10^{-16}$. Because `linspace` always includes the exact boundary endpoint, this residual is floating-point/transcendental-function precision at that point, *not* a discretization effect — an **off-grid** check (a $2\times10^6$-point random interior sweep avoiding exact endpoints, run during review) finds the same bound holds with **no violation** anywhere, maximum measured deviation from the true supremum $1.5\times10^{-8}$, consistent with equality holding on a whole boundary *face* (as (D) proves) rather than isolated points reachable only by grid alignment. The exact statement is (A)+(D) above, not either sweep.

**Prior art, stated plainly.** That a single CA tick's unitary phase is bounded — some "Nyquist-type" ceiling on the rotation any one discrete-time step can apply — is generic to unitary QCA/lattice constructions and is not this finding's novel content; the finding does not claim the mere existence of *a* ceiling is new. What is specific to this construction, and is what checks A/D/the control actually establish, is that the **paired** law saturates a ceiling of exactly $\pi$ (not some other value) on the **whole** zone boundary, while the *un-paired* single-branch law does not respect that same ceiling at all (it reaches $2\pi$) — i.e. the content is the pairing-specific saturation proof, not the generic fact that some bound exists.

## 3. The bound is pairing-specific, not generic arccos saturation (control)

The **un-paired** single-branch doubled law $2\,\omega_+(\mathbf K/2)$ — explicitly flagged in F248/CLAUDE.md as *not* the physical photon/graviton dispersion — has no analogous bound: its own "$a+b$" is $2u_+(\mathbf K/2)$, not sign-definite on the domain ($u_+$ ranges over $[-1,1]$ regardless of the $c_i\ge0$ restriction). Its zone-sweep maximum measures $2\pi$ exactly — double the paired law's ceiling. This is the module's one control parameter (`pairing_law="chiral_double"`); it correctly turns checks C, E, F red (§6), which is the honest way to show the $\pi$ bound is a genuine, falsifiable consequence of the **pairing structure** (F69) specifically, not an artifact of arccos ranges in general.

## 4. The Planck-unit number (E)

$\Omega_\text{max}=\pi$ is a **rotation angle per CA tick $\tau$** (F26: $\Omega$ is exactly the $(\mathbf E,\mathbf B)$ rotation angle per tick). The physical maximum photon/graviton angular frequency is therefore $\omega_\text{max}=\pi/\tau$. F79 §5 gives the lightcone constraint $a/\tau=c\sqrt d$ ($d=3$), so with F79/F107's registered ruler $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$,

$$\frac{\tau}{t_\text{Planck}}=\frac{a/\ell_P}{\sqrt3}=\frac{\sqrt{8\pi}\,3^{1/4}}{\sqrt3}=\sqrt{8\pi}\,3^{-1/4}=3.80925\ldots$$

(the same number F79 §5 and F61 Part C already tabulate for $g_*=48$ — reused here verbatim, not re-derived), giving the closed form

$$\frac{E_\text{max}}{E_\text{Planck}}=\frac{\Omega_\text{max}}{\tau/t_\text{Planck}}=\frac{\pi}{\sqrt{8\pi}\,3^{-1/4}}=\pi\cdot\frac{3^{1/4}}{\sqrt{8\pi}}=\sqrt{\frac{\pi\sqrt3}{8}}=0.824727\ldots$$

verified two independent ways in the module: symbolically (sympy closed form vs. the registered `a_over_ellP` evaluated to float, residual $<10^{-9}$) and against the check-C zone-sweep maximum converted through the same $\tau/t_\text{Planck}$ (residual $2\times10^{-10}$). **This uses zero new free parameters** — $a/\ell_P$ is F79's own structural output (fixed by matching $G$, not by anything in this finding), so the ratio $E_\text{max}/E_\text{Planck}$ is a genuine, parameter-free prediction of the model, not a fit.

## 5. Relation to F352's $\Lambda_\text{model}$ (F)

F352 already uses a cruder UV-cutoff estimate for an unrelated calculation (BHL-style compositeness RG for the F73 scalar): $\Lambda_\text{model}=E_\text{Planck}/(a/\ell_P)\approx0.1516\,E_\text{Planck}\approx1.85\times10^{18}$ GeV — the naive "set $k\sim1/a$" substitution into $E=\hbar c\,k$, with no reference to the actual dispersion functional form. This finding's own $E_\text{max}$ is **not** the same number:

$$\frac{E_\text{max}}{\Lambda_\text{model}}=\sqrt{\frac{\pi\sqrt3}{8}}\cdot\sqrt{8\pi}\,3^{1/4}=\pi\sqrt3=5.44140\ldots$$

verified in-module to $8.9\times10^{-16}$. This is not a new independent number either: per `bcc.py`'s own F273 comment ("$4\pi/a=2\pi\sqrt3$" — the measured reciprocal-lattice period), $\pi\sqrt3$ is exactly **one reciprocal-lattice-vector magnitude** $2\pi/a$ in that convention. So the two cutoff estimates the model now carries — F352's naive $k\sim1/a$ substitution and this finding's exact dispersion-band top — differ by exactly the model's own reciprocal-lattice scale, a structural relation rather than a coincidence needing its own explanation.

## 6. Results

| Check | Statement | Residual / value | Tier |
|---|---|---|---|
| A | $\arccos(a)+\arccos(b)\le\pi\iff a+b\ge0$ (exact trig identity + strict monotonicity) | sympy $=0$; numeric $4.4\times10^{-16}$ | exact-algebraic |
| B | $c_i=\cos\theta_i\ge0$ on $\theta_i\in[-\pi/2,\pi/2]$ | $\min c_i=6.1\times10^{-17}$ (endpoint) | exact by construction |
| C | zone-sweep $\max\Omega_\text{even}=\pi$ | $4.4\times10^{-16}$ | lattice-numeric |
| D | $u_++u_-=0$ identically on the whole boundary face | sympy $=0$ | exact-algebraic |
| E | $E_\text{max}/E_\text{Planck}=\sqrt{\pi\sqrt3/8}=0.82473$ | symbolic-vs-registry $<10^{-9}$ | exact-algebraic (given F79's ruler) |
| F | $E_\text{max}=\pi\sqrt3\,\Lambda_\text{model}$ | $8.9\times10^{-16}$ | exact-algebraic |

**Control** (`pairing_law="chiral_double"`, the un-paired doubled law): C, E, F correctly measure $2\pi$, $1.6495$, $2\pi\sqrt3$ against the fixed physical targets $\pi$, $0.8247$, $\pi\sqrt3$ and go **red**; A, B do not read the dispersion law and stay green; D is reported not-applicable (`pass=None`, uncounted) rather than forced red, since the boundary-saturation identity is a statement about the *even* law specifically.

## 7. What this does and does not close

**Closed.** E12's "lattice is the cutoff" slogan now has a number: the photon/graviton sector's propagating band has an exact, closed-form top, $\Omega_\text{max}=\pi$ radians/tick, translating (zero new free parameters) to $E_\text{max}=0.8247\,E_\text{Planck}$ — an $O(1)$ fraction of the Planck energy, not off by many orders in either direction, and related by an exact closed form to the model's other existing cutoff estimate (F352). This is a genuine **kinematic** UV-completion statement distinct from A11/K9's $\rho_\text{vac}$ EFT-coefficient residual: it says there is no super-Planckian propagating photon/graviton mode *at all* on this lattice — not as an approximation or an EFT power-counting argument, but as an exact consequence of the pairing structure (F69) that already gives the model its non-birefringence.

**Not closed — honest scope.** This is a **single-particle kinematic bound**, not a dynamical statement about graviton-graviton **scattering**. Continuum quantum GR's own UV-completion problem is usually stated as a *scattering-amplitude* unitarity violation (graviton-graviton or graviton-matter 2→2 amplitudes growing like $E^2/M_\text{Planck}^2$ per vertex, standard EFT-of-gravity power counting, e.g. Donoghue gr-qc/9512024) — this finding does not compute any such amplitude, interaction vertex, or partial-wave unitarity bound; it establishes only that **the single graviton line itself cannot carry more than $0.8247\,E_\text{Planck}$ of energy in the first place**, which removes the *kinematic* precondition for a super-Planckian collision without addressing the *dynamical* question of what a would-be near-band-top graviton-graviton collision actually does. A full closure of E12 in the "self-interaction/scattering" sense the completeness-report prompt names would need that dynamical calculation; this finding supplies the kinematic half and leaves the dynamical half explicitly open. The $O(1)$ (rather than exactly $1$) coefficient $0.8247$ is a genuine model output, not a target to tune toward $1$ — no claim is made that it "should" be closer to unity.

## Reviewed & corrected

**2026-09-03 - 16:40** — attack pass: **CONFIRMED-NARROWER**. Found: (i) the finding's own residual self-reports for checks C and F were wrong by about three orders of magnitude — stated as $\le5\times10^{-13}$ in four places, actual measured values (from `test-results/F357_graviton_band_cutoff.json` and an independent re-run) are $4.4\times10^{-16}$ (C) and $8.9\times10^{-16}$ (F); (ii) describing C's residual as a "grid resolution floor" was a mischaracterization — `linspace` always includes the exact boundary endpoint regardless of resolution, so the tiny residual measured there is floating-point/transcendental precision at that point, not a discretization effect; (iii) attack 11 (prior art) WEAKENS: the generic fact that a single CA tick's phase is Nyquist-bounded is not novel and the finding did not contextualize this, risking an inflated reading of "$\Omega_\text{max}=\pi$" as more surprising than it is. Fixed: all four residual figures corrected to their true values (§0 status line, §2, §5, §6 table); §2's characterization of C's residual corrected and backed with an independent off-grid/$2\times10^6$-point random-interior sweep (no violation found, consistent with equality on a whole boundary face); a "Prior art, stated plainly" paragraph added at the end of §2 narrowing the novelty claim to the pairing-specific saturation proof, not the existence of a ceiling per se. Rejected: none. Deferred: none — every attack (13/13, including a live `casim test --id ... --control` run and an independent sympy re-derivation of every closed form) either passed cleanly or was fixed in place; no defect required escalation under the review skill's Step 3 hard-verdict gate (not REFUTED/CIRCULAR, no exactness downgrade, no core-decision or supersession touched).

## 8. Files
- Module: `src/casim/engine/interactions/gravity_band_cutoff.py`
- Test record: `tests/registry/interactions.yaml` id `F357-graviton-band-top`
- Results: `test-results/F357_graviton_band_cutoff.json`
- Claim: `docs/claims/CL297-graviton-photon-band-top-planck-scale.md`
