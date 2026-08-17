# F279 — Hypercharge quantisation is real, but the gravitational anomaly is not what derives it: the closing constraint is the F47 Majorana step

**Date:** 2026-08-02 - 08:58
**Status:** Confirmed — F165's *conclusion* upheld, its *attribution* corrected and one of its claims falsified. 5/5 checks PASS over ℚ (literal integer zero, not float).
**Modules touched:** none (analytical study + verification harness).
**Verification script:** `tests/findings/test_F279_hypercharge_attribution.py`
**Registry record:** `F279-hypercharge-attribution` (`tests/registry/gauge.yaml`, kind `assertion`, tier `gate`)
**Cross-references:** [[F165-hypercharge-quantisation-from-anomaly-and-mass]] (the finding under test — conclusion retained, derivation replaced), [[F47-majorana-seesaw-higgs-free]] (supplies the closing constraint), [[F266-sterile-neutrino-dark-matter]] ($Y=0$ structurally forced), [[F38-fg1-anomaly-cancellation]] (the traces), [[F51-bipartite-sublattice-hypercharge]] (the carrier), [[F27-complex-mass-chiral-su2]]/[[F41-hypercharge-higgs-free-su2]] (the single mass phase).

Raised by the 2026-08-02 completeness sweep (`docs/status/completeness-2026-08-02.md`, gap #4), which found F165 and `papers/Claims-and-Falsifiers-Summary.md` revision 2 asserting opposite things about the same quantity on the same day.

---

## 1. The question

F165 (2026-06-29) concludes that the five generation hypercharges are **forced up to one overall normalisation** by three anomaly rows plus two mass-step rows, closing audit gap G4. `papers/Claims-and-Falsifiers-Summary.md` revision 2 (2026-08-02) says under **Scope — what is *not* claimed**:

> **Charge quantisation.** The hypercharge assignment … is the Standard Model's own, entered as literals and *checked* anomaly-free — not derived from anomaly cancellation. … This is an input.

`src/casim/engine/gauge/hypercharge.py:117–121` agrees with the register, writing `Y_LEPTON_L = -1`, `Y_E_R = -2`, `Y_NU_R = 0` as literals. One of the two is wrong. This finding decides which, by re-deriving the system from scratch rather than re-running F165's own script.

## 2. Verdict

**F165's conclusion survives. The register is wrong and is corrected by this finding.** Hypercharge quantisation *is* derived: one normalisation, not five values, is the residual input.

**F165's derivation does not survive, in two respects**, and the corrected version is stronger, not weaker.

---

## 3. A1 — The gravitational anomaly is not an independent constraint

F165's system omits $\nu_R$. The model has one: F47's Higgs-free see-saw needs a right-handed neutrino, `hypercharge.py` carries `Y_NU_R` and a conjugate mass phase `DELTA_Y_NU = Y_L − Y_νR = −1`, and F266 treats $\nu_R$ as a physical field. Carrying it as an unknown $y_\nu$ means:

- it contributes $-y_\nu$ to the gravitational trace, and
- it gets its own Dirac mass-step row $y_\nu = y_L + y_\phi$ (the conjugate phase, exactly as the module encodes it).

With those two additions the gravitational row is **identically satisfied by the other five constraints** — the rank is 5 with it and 5 without it, and substituting the other five into the grav row returns literal $0$. It contributes nothing.

The consequence is not cosmetic. On the anomaly rows plus the three mass-step rows alone, the solution space is **two-dimensional**:

$$
y_L=-3y_Q,\quad y_d=y_Q-y_\phi,\quad y_u=y_Q+y_\phi,\quad y_e=-3y_Q-y_\phi,\quad y_\nu=-3y_Q+y_\phi,
$$

with $y_Q$ **and** $y_\phi$ both free. The Standard Model needs $y_\phi=3y_Q$. Nothing above supplies it.

**F165 reaches a one-dimensional space only by leaving $\nu_R$ out of the gravitational trace, which is numerically identical to imposing $y_\nu=0$ — the very step that needed justifying.** The 1-dimensionality was real; its stated cause was not.

## 4. A2 — What actually closes the system: the F47 Majorana step

The model supplies the missing constraint independently, and from its own Higgs-free structure rather than from a generic Standard-Model theorem.

F47's right-handed neutrino carries a **Majorana** mass term $\nu_R^{\mathsf T}C\,\nu_R$. That bilinear carries hypercharge $2y_\nu$. Gauge invariance of the term is therefore

$$
2y_\nu=0\quad\Longleftrightarrow\quad y_\nu=0,
$$

exact over ℚ, with no normalisation freedom — a Majorana mass is only available to a field of exactly zero hypercharge. This is the same fact F266 records as "$Y=0$ structurally forced".

Adding that row restores F165's result exactly. The **corrected constraint set** is:

$$
\begin{aligned}
[SU(2)_L]^2\,U(1):&\quad 3y_Q+y_L=0,\\
[SU(3)_c]^2\,U(1):&\quad 2y_Q-y_u-y_d=0,\\
\text{mass step }(Q,d):&\quad y_d=y_Q-y_\phi,\\
\text{mass step }(L,e):&\quad y_e=y_L-y_\phi,\\
\text{mass step }(L,\nu):&\quad y_\nu=y_L+y_\phi,\\
\textbf{F47 Majorana}:&\quad 2y_\nu=0,
\end{aligned}
$$

**six constraints in seven unknowns, rank 6, nullspace dimension 1** — the same line, the same ratios

$$
y_Q:y_u:y_d:y_L:y_e:y_\nu \;=\; 1:4:-2:-3:-6:0,\qquad y_\phi=3y_Q,
$$

and the same normalised values at $y_Q=\tfrac16$. **Both** the gravitational and the cubic $U(1)^3$ anomalies are then identically zero on that line — two consistency checks, not two constraints. F165 correctly demoted the cubic; the grav row belongs in the same box.

**Why the corrected route is the better result.** F165's version was the lattice realisation of a known Standard-Model theorem (Minahan–Ramond–Warner; Geng–Marshak) — anomaly freedom plus one Yukawa per charged sector quantises hypercharge. The corrected version leans on something the Standard Model does *not* have: a Higgs-free Majorana step for a right-handed neutrino that the same construction (F27/F41/F47) already required for the see-saw. The quantisation now follows from the model's own distinguishing structure rather than from an imported theorem, and the derivation is conditional on F47 — a finding the model owns — instead of on an omission.

## 5. A3 — The colour claim in F165 §3 is false

F165 §3 states:

> Remove colour (set the multiplicity to 1) and the system no longer closes to a single line; the fractional values are a consequence of the lattice's colour structure, not an input.

It does close. With colour multiplicity $N_c$ carried symbolically, the system has rank 5 and nullspace dimension **1 for every $N_c$**, with ratios

$$
y_Q:y_u:y_d:y_L:y_e \;=\; 1:(1+N_c):(1-N_c):-N_c:-2N_c,
$$

verified explicitly at $N_c=1,2,3,4,5$ and symbolically in $N_c$. At $N_c=1$ — the case F165 says fails — it gives $1:2:0:-1:-2$, a perfectly well-defined line. The cubic $U(1)^3$ anomaly vanishes **identically on that line for every $N_c$**, so it selects nothing either.

The correct statement is narrower and still worth making:

> Commensurability — that lepton charges are integers and quark charges are rationals *of the same unit* — is derived, and holds for any $N_c$. That the unit is a **third** is $N_c=3$, which the model takes as an input.

So charge *quantisation* is derived; the specific *fractions* $\tfrac23,-\tfrac13$ are quantisation **plus** $N_c=3$. Since $N_c=3$ is itself underived in this model (the completeness sweep grades "why 3 colours" `ABSENT`), F165 §3 was claiming as an output something that is downstream of an input.

## 6. A4 — What F165 got right, and should keep credit for

- **The single shared mass phase is load-bearing, and F165 attributes it correctly** to F27/F41. Allowing independent down-sector and lepton-sector phases $y_{\phi d}\ne y_{\phi e}$ returns a **two-dimensional** space in which $y_d$ and $y_u$ float on $y_{\phi d}$ and the quark charges are not fixed. That one field $U(x)$ carries one hypercharge phase is doing real work.
- **The up-type relation $y_u=y_Q+y_\phi$ is genuinely output, not assumed** — it falls out of the $[SU(3)_c]^2U(1)$ row. This survives unchanged and is why a single Higgs-free phase suffices.
- **The residual is one normalisation, not five values**, and it is the unit of charge — the $\alpha$/$\sin^2\theta_W$ question (F49), not a quantisation question. Unchanged.
- **The 1-dimensionality itself.** F165's headline number was right; only its stated cause was wrong.

## 7. Verification summary

`tests/findings/test_F279_hypercharge_attribution.py`. All arithmetic over `sympy.Rational`; every residual is the literal integer $0$.

| Test | Statement | Type | Result |
|------|-----------|------|:------:|
| — | F165's published system does reproduce dim 1, rank 5 and its ratios | exact (ℚ) | PASS |
| A1 | With $\nu_R$ carried, the grav row adds **no rank** and is identically 0 on the others; the remaining system is **2-dimensional** | exact (ℚ) | PASS |
| A2 | $2y_\nu=0\Rightarrow y_\nu=0$; the corrected 6-row set has rank 6, dim 1, F165's ratios, and **both** anomalies vanish on the line | exact (ℚ) | PASS |
| A3 | Closure holds for **every** $N_c$ with ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$; cubic identically 0 for all $N_c$ | exact (ℚ + symbolic $N_c$) | PASS |
| A4 | Two independent mass phases ⇒ dim 2, quark hypercharges float | exact (ℚ) | PASS |

## 8. What this changes

**In the register.** `papers/Claims-and-Falsifiers-Summary.md` Scope bullet on charge quantisation is rewritten: hypercharge quantisation **is** derived, with the residual named as one normalisation and the conditionality named as $N_c=3$ plus the F47 Majorana step. The pre-existing bullet understated a derived result.

**In F165.** §3's colour claim is retracted and §2's attribution of the grav row is corrected, by banner. F165's conclusion, its ratios and its "one normalisation" framing all stand. Recorded as `partially_superseded` in `docs/theory/supersessions.yaml` (**S13**), consistent with the project's standing practice that the supersession unit is a *check*, not a file.

**In the code.** `hypercharge.py` still writes `Y_LEPTON_L`, `Y_E_R`, `Y_NU_R` as literals under a comment calling them SM values. They are derived values and should be registry constants with F279/F165 provenance. **Not done here** — this finding touches no module, and the constants-registry change is a separate, testable edit. Logged as the open follow-up.

**Update 2026-08-06 — done.** The three are `casim.constants` entries in the `electroweak` sector (`Y_LEPTON_L`, `Y_E_R`, `Y_NU_R`), and `hypercharge.py` imports them. The registry does not record them as three equally derived numbers, because they are not: `Y_NU_R = 0` is forced outright by the §4 Majorana row with no normalisation freedom; `Y_E_R = 2·Y_LEPTON_L` is derived and, by §5, holds for every $N_c$; and `Y_LEPTON_L = -1` **is** the residual normalisation this finding names — exact because it is a choice of unit, not because it was computed. `Y_E_R` resolves *from* `Y_LEPTON_L` in the registry rather than being typed as $-2$ (C2.1), so the derived ratio cannot drift away from the unit it depends on.

**What it does not change.** No engine module, no constant, no baseline, no other finding's numbers. The physics is where it was; the derivation is now attributed to the structure that actually performs it.

---

## 9. Open follow-up

1. ~~Promote the three hypercharge literals in `casim.engine.gauge.hypercharge` to `casim.constants` entries with `provenance: F165, F279` and `exactness: exact`, with `Site(...)` records.~~ **Done 2026-08-06.** Registered in the `electroweak` sector with `Site(...)` records for the module (`kind='import'`) and for `forks/electroweak/hypercharge_fork.py` (`kind='reexport'`), and guarded by `check_registry_values_are_on_the_derived_line` in this finding's own gate record — which solves the §4 system and reads the normalisation back out of the registry, so a value that drifts off this line fails the gate rather than merely disagreeing with prose.

   The **quark** hypercharges stay in `hypercharge.py` on purpose, and the reason is §5: their *fractions* are quantisation plus $N_c = 3$, so registering them as `exact` on F165/F279 provenance would launder an underived input into a derived one. (There is a second, mechanical reason recorded at the site: $1/3$, $4/3$ and $-2/3$ are diagnostic values, so the C2.4 sweep cannot exclude them, and registering them would flag every unrelated third in `src/`.) Promoting them is blocked on follow-up 2, not on bookkeeping.
2. $N_c=3$ remains underived, and A3 shows it is load-bearing for the *fractions*. That is the "why three colours" gap, unchanged by this finding but now with a named consumer.

---

*End of finding.*
