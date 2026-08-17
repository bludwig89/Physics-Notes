# F295 — Freeing $\alpha$ and $G$ does **not** narrow the loop ($\alpha$ would need evaluating 68 decades above the model's own cutoff; $G$'s coupling is a *power*, killed by F286 T1 on shape before magnitude) — but asking the question exposed that **F286 mis-read its own theorem**: T1's allowed $p=0$ branch is not "trivial", it is a **scale-free anomalous dimension** $\gamma$, which needs **no second scale at all**, predicts $dn_s/d\ln k=0$ **exactly**, and is precisely the free marginal label on F285 D3's proven line of fixed points; the question is not *where is the scale* but *which operator carries $\gamma$*

**Date:** 2026-08-02 - 19:35
**Status:** **A correction to F286's framing + a decisive negative on the inverse problem + a sharpened target.** 8/8 checks PASS. A1 (the $p=0$ branch, $dn_s/d\ln k\equiv0$) is **exact-algebraic** (sympy); A3 is **computed** against the model's own cutoff; A4 is **structural** and explicitly *not* a derivation.
**Module:** `src/casim/engine/interactions/cosmology_anomalous_dimension.py`
**Registry record:** `F295-tilt-is-an-anomalous-dimension` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F295_anomalous_dimension.json`
**Corrects:** [[F286-second-scale-must-be-a-log-not-a-length]] — its **framing**, not its algebra. T1 is correct and is reused here unchanged; what was wrong is the reading of T1's own $p=0$ solution as trivial, and the consequent "we need a second scale" title. **F286's T5 look-elsewhere count stands unaltered.**
**Refines:** [[F285-initial-condition-measure-cannot-tilt]] — its "the only scale-free choice is $n_s=1$, excluded at 8.4σ" row is the $\gamma=0$ case, so that exclusion is the **positive** statement $\gamma\ne0$ rather than a dead end.
**Cross-references:** [[F285-initial-condition-measure-cannot-tilt]] (D3's line of fixed points — $\gamma$ **is** its marginal label), [[F286-second-scale-must-be-a-log-not-a-length]] (T1 reused; T2's log class becomes a *sibling* sub-class with a discriminator), [[F284-rigid-lattice-expansion-and-primordial-state]] (rigidity; and $\dot G/G\equiv0$ is no longer a liability once no running coupling is needed), [[F175-lattice-2-9-eg-weight]] / [[F138-weinberg-gap-closure-4piv-matching]] / [[F145-route-c-induced-njl-coupling]] (the **three** independent registered constants equal to $\tfrac29$), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] (the cutoff A3 measures $\alpha$ against), [[F253-weight-as-phase-scale-nogo]] / [[F256-lambda6-sextic-derivative-nogo]] (the coincidence standard, still applied). External: Planck 2018 X ($n_s=0.9649\pm0.0042$, $dn_s/d\ln k=-0.0045\pm0.0067$).

Raised by Ben, 2026-08-02: *"if, for the sake of testing, we allow for $\alpha$ and $G$ to be different than adopted, does that help us with narrowing down the loop? Based on the model geometry, can we get closer to a predictive mechanism?"*

---

## 1. The direct answer first

**No, freeing the two adopted constants does not narrow the loop** — and the way each fails is more informative than the failure.

At one loop $1-n_s=g_\text{eff}/2\pi$, so the data demands

$$g_\text{eff}=2\pi(1-n_s)=0.2205\pm0.0264.$$

| Freed constant | What it would take | Verdict |
|---|---|---|
| $\alpha$ | Reaching $\alpha=0.2205$ by one-loop QED running from $m_e$ needs $\ln(\mu/m_e)=208$, i.e. $\mu\sim10^{87}$ GeV — **68.1 decades above the model's own lattice cutoff** $\Lambda_\text{UV}=3^{-1/4}M_\text{Pl}\sim10^{19}$ GeV | **Excluded** — and excluded *by the model's own structure*, not by a fit. There is no such scale |
| $G$ | Gravity's dimensionless coupling is $g_\text{grav}(k)=(k/M_\text{Pl})^2$ — a **power, $p=2$**, which F286 T1 already excludes on *shape*. Magnitude is $1.7\times10^{-116}$, 115 decades short | **Doubly excluded**, shape first |

The useful half: this does not merely say "those two numbers are wrong". It says **the loop cannot be a running gauge coupling at all.** A running coupling either dies in the IR ($\alpha_s$, F286), is far too small ($\alpha$), or has the wrong $k$-shape ($G$). That closes a whole category.

## 2. What the question exposed — F286 mis-read its own theorem

F286 T1 proved: if $n_s-1=F(k\xi)$, then $|d\ln F/d\ln x|<0.32$, so a power $F=Cx^p$ needs $|p|<0.32$. F286 concluded "only a log survives" and set $p=0$ aside as the trivial case.

**$p=0$ is not trivial. It is the answer.** A constant $F$ is a scale-free **anomalous dimension**:

$$n_s-1=-2\gamma\ \text{(constant)}\quad\Longrightarrow\quad \Delta^2(k)\propto k^{\,n_s-1},\qquad \boxed{\frac{dn_s}{d\ln k}=0\ \text{exactly}}$$

(verified symbolically: the log-slope of $\Delta^2$ is $-2\gamma$ and its derivative is identically zero). Three consequences, all of which improve the position:

1. **No second scale is needed at all.** The entire framing of F286 — and its title — was too narrow. A tilt is not necessarily a *scale* effect; it is a *scaling-dimension* effect.
2. **It is more consistent with the data than the log class**, not less: Planck's running is consistent with zero, and this branch predicts exactly zero.
3. **It is exactly F285 D3's marginal label.** D3 proved every power law is a fixed point of block-spin and the exponent is a free marginal label along a *line* of fixed points. $\gamma$ **is** that label. D3 said block-spin cannot *select* it — which is true, and is not the same as saying it cannot exist.

**This also repairs F285's own row.** F285 listed "scale-free in the metric $\Rightarrow n_s=1$, excluded at 8.4σ" as a failure. It is the $\gamma=0$ case, so read correctly it is a **positive result**: the data requires $\gamma\ne0$, specifically $\gamma=(1-n_s)/2=0.01755$.

> The question is no longer *where is the second scale*. It is **which operator sets the initial amplitude, and what is its anomalous dimension.** That is a much better-posed question, and it is answerable in principle by the model's own group theory rather than by cosmology.

## 3. Two sub-classes, and a real discriminator

| Sub-class | $dn_s/d\ln k$ | Status |
|---|---:|---|
| **Constant $\gamma$** (this finding) | $0$ **exactly** | consistent |
| **Log-type** (F286 T2) | $-2.62\times10^{-4}$ | consistent |

Both sit inside Planck's $-0.0045\pm0.0067$. They separate at $\sigma\sim2.6\times10^{-4}$ — beyond CMB-S4, so not a near-term test, but it is a genuine discriminator between two otherwise-identical pictures and it belongs on the register now rather than being rediscovered later.

## 4. Can geometry get closer? — stated at its real strength, and no further

A constant $\gamma$ needs a coupling that is **scale-independent**. That requirement is what kills $\alpha$, $\alpha_s$ and $G$ (all run, or die in the IR) — and it is exactly what an **exact representation weight** supplies: a pure group-theoretic ratio, evaluable at CMB momenta trivially because it does not depend on momentum at all.

The model owns such objects, and the required value lands on one:

$$g_\text{eff}=0.2205\pm0.0264\qquad\text{vs}\qquad \tfrac29=0.2222\quad(\textbf{0.064σ}),$$

where $\tfrac29$ appears in this model as **three independent registered constants** — $\delta^*$ (the $E_g$ representation weight, F175), $\sin^2\theta_W$ on-shell (F138), and $c_\text{Fierz}^\text{colour}$ (F145). CLAUDE.md requires they stay separate precisely because they are *unrelated quantities that happen to share a value*.

**What this is:** a **shape-justified target**. F286 reported a bare numerical coincidence; what has changed is that the *kind* of object now matches the *kind* of requirement — scale-free coupling, scale-free tilt, one-loop $g/2\pi$.

**What this is not:** a derivation. Three things are still missing, and none should be glossed:

- **No operator has been identified.** Nothing yet says the initial amplitude is set by an operator carrying the $E_g$ weight, or any weight.
- **F286 T5's look-elsewhere count applies unchanged to the *value*.** 396 candidates, 6 hits in the 1σ window, $p=0.32$. Improving the *shape* argument does not improve the *statistics*, and it would be a cheat to let it appear to.
- **Which of the three $\tfrac29$'s?** They are separate constants by decree. A mechanism must pick one, and picking one is most of the work.

> **Honest verdict on the user's second question: yes, geometry gets closer — but "closer" here means the target is now the right *shape*, not that it is hit.** The distance to a prediction is exactly one identified operator.

## 5. Verdict

> **No** to freeing $\alpha$ and $G$: $\alpha$ needs a scale 68 decades above the model's own cutoff, $G$'s coupling is a power that F286 T1 excludes on shape before magnitude, and between them they close the running-gauge-coupling category entirely. **But** the question exposed a framing error worth more than the answer: F286's T1 allows $p=0$, and $p=0$ is a **scale-free anomalous dimension** — no second scale required, $dn_s/d\ln k=0$ exactly, and identical to the marginal label F285 D3 already proved exists on a line of fixed points. F285's 8.4σ exclusion of $n_s=1$ is therefore the positive statement $\gamma=0.01755\ne0$. Geometry then offers the right *kind* of object: a scale-free representation weight, with $\tfrac29$ at 0.064σ from the required $g_\text{eff}$ — **a shape-justified target, not a derivation**, with the look-elsewhere count on its value unchanged.

## 6. Falsifiers

1. **An operator whose anomalous dimension is computable and $\ne0.01755$.** Would falsify the whole constant-$\gamma$ branch, which is now the leading one.
2. **A measured $dn_s/d\ln k$ significantly nonzero.** Would kill constant-$\gamma$ and favour F286's log class — the discriminator in §3.
3. **A running coupling in the model evaluable at CMB momenta.** Would reopen §1's closed category.
4. **A derivation picking one of the three $\tfrac29$'s.** Would convert §4 from target to prediction — this is the single highest-value next step.
5. **A demonstration that the initial amplitude carries no operator at all** (a pure initial condition with no scaling dimension). Would make $\gamma$ meaningless and return the tilt to being a free number.

## 7. What is exact vs computed vs open

| Piece | Status |
|---|---|
| Constant $\gamma$ $\Rightarrow$ $\Delta^2\propto k^{-2\gamma}$, $dn_s/d\ln k\equiv0$ | **exact-algebraic** (sympy, literal zero) |
| $p=0$ is inside F286 T1's own allowed band | **exact** (T1 reused unchanged) |
| $\gamma$ is F285 D3's marginal label | **structural** (D3 proved the fixed line) |
| $\gamma_\text{required}=(1-n_s)/2=0.01755$ | **computed** |
| $\alpha$ route: $\ln(\mu/m_e)=208$, 68.1 decades above the cutoff | **computed** (one-loop QED, $N=3$) |
| $G$ route: $p=2$ excluded on shape; $g_\text{grav}=1.7\times10^{-116}$ | **exact** (shape) $+$ **computed** (magnitude) |
| Sub-class discriminator at $2.62\times10^{-4}$ | **computed** |
| $g_\text{eff}=0.2205\pm0.0264$ vs $\tfrac29$ at 0.064σ | **computed**; **significance nil** (F286 T5) |
| Three registered constants equal $\tfrac29$ | **exact** (registry) |
| **Which operator carries $\gamma$** | **open — and now the only remaining question** |

## 8. Honest scope

A1 is the load-bearing result and it is embarrassingly cheap: it is one line of sympy plus the observation that a constant is a legitimate solution of a bound that was already proved. That it went unnoticed in F286 is worth recording as much as the result — the error was in the *reading*, not the algebra, and a finding's framing can be wrong while every equation in it is right. A3 is solid but uses one-loop QED with $N=3$ charged leptons; a fuller running would shift 68 decades by a few, which changes nothing. A4 is deliberately under-claimed: the shape argument is real, the value argument is not, and the two are kept apart in the text because merging them is exactly how a coincidence gets promoted by accident. What this finding does **not** do is identify an operator; §7's last row is the whole remaining problem, and it is now a single well-posed question rather than a search.

## 9. Files
- Module: `src/casim/engine/interactions/cosmology_anomalous_dimension.py`
- Test: `tests/findings/test_F295_anomalous_dimension.py`
- Results: `test-results/F295_anomalous_dimension.json`
