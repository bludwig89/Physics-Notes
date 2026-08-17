# Bucket C pass criteria from live data, not from a judgement call

*Opened 2026-08-08. Companion to `control-soundness-rollout.md`. Status: **proposal +
one live result that should be acted on regardless**.*

The five remaining cannot-fail gate records are all cosmology: **F283, F285, F286, F295, F296**
(measured by execution trace, `make can-fail`; see completeness Amendment 3). They compute real
physics and then narrate it — F295 ends with a field called `answer_to_ben`, F283 with 14 prose
strings — so nothing can score them FAIL.

The question was whether their pass criteria have to be Ben's thresholds. **Mostly they don't.**
Four of the five compare a model number against a measured one, and the criterion can be
*"agrees with the published measurement to within N σ"* — which is not a personal choice, moves
when the data moves, and is the shape F297 already used to grade G5.

---

## 0. The live result, which is not a proposal

**F295's headline prediction is parameter-free, and the data has moved under it.**

`cosmology_anomalous_dimension.py` computes `g_eff = 2π(1 − n_s)` and compares it to `2/9` — a
registered exact constant that already appears three times in the model (`delta_star`,
`sin2_thetaW_onshell`, `c_fierz_colour`). Setting them equal is a prediction with **zero free
parameters**:

$$1-n_s=\frac{1}{9\pi}\qquad\Longrightarrow\qquad n_s=1-\frac{1}{9\pi}=0.9646322$$

| Dataset | $n_s$ | F295 vs data |
|---|---|---:|
| Planck 2018 (**hardcoded in the module**) | $0.9649\pm0.0042$ | **−0.06 σ** |
| CMB-only: Planck PR3/PR4 + SPT-3G D1 + ACT DR6 + BK | $0.9682\pm0.0032$ | **−1.12 σ** |
| CMB + DESI DR2 BAO | $0.9728\pm0.0029$ | **−2.82 σ** |

The prediction has not moved. **The measurement has, by 0.8 σ of its own 2018 error bar, and its
error bar has shrunk by 31 %.** A bullseye in 2018 is a 2.8 σ tension against CMB+BAO in 2026 — and
the module cannot see it, because `NS_OBS, NS_SIGMA = 0.9649, 0.0042` is typed into line 110 and
`RUN_OBS, RUN_SIGMA = -0.0045, 0.0067` into line 111.

This is the F297-vs-F122 pattern exactly: *an assembly grades its own inputs*, and here the input is
someone else's dataset from eight years ago. It is also a live instance of the thing this repo is
best at catching and worst at noticing — **a number that was fitted, reported as agreeing, and never
re-checked**. `gamma_from_data` says so in its own name.

**Recommended action independent of everything below:** register these as `MeasuredConstant`s (D7)
with dataset provenance instead of module-level literals. The rule already exists — *"every constant
needs a `provenance` finding, an `exactness` class and a `derivation` string"* — and a
`MeasuredConstant` is the declared vehicle for "same quantity, different regime". Then the 2.8 σ is
visible on the next `make gate` rather than in a session like this one.

> **Caveat, stated because it changes what the 2.8 σ means.** The CMB+BAO $n_s$ is the highest of the
> three and the one furthest from F295; the CMB-only number is at 1.1 σ and SPT-3G D1 alone is
> $0.951\pm0.011$, which sits on the *other* side. The honest reading is *"drifting away, not
> excluded"*, and the criterion below is written at 3 σ so it says that rather than more.

---

## 1. Proposed criteria, per record

Each is a leg with a measured comparator. `reds:` targets in brackets.

### F295 — tilt is an anomalous dimension (K3)

| Leg | Criterion | Now |
|---|---|---|
| `K3-ns` | $\lvert n_s^{\text{pred}}-n_s^{\text{obs}}\rvert/\sigma<3$, $n_s^{\text{pred}}=1-1/(9\pi)$ exactly | 2.82 σ — **passes, barely** |
| `K3-run0` | constant-γ predicts $dn_s/d\ln k=0$; require $\lvert 0-\alpha_s^{\text{obs}}\rvert/\sigma<3$ | 1.19 σ ✓ |
| `K3-sep` | the two subclasses are **not yet separable**: require $\sigma_{\alpha}^{\text{obs}}>$ separation $2.6165\times10^{-4}$ | $5.2\times10^{-3}$, i.e. 20× too coarse ✓ |
| `K3-2/9` | `g_eff` agrees with the registered `2/9` within 3 σ | same test as `K3-ns`, stated in the model's units |

`K3-sep` is the interesting one: it is a leg that **goes red when the data gets good enough**, which
is a prediction about future measurements rather than about the past. At Planck 2018 it was 26× too
coarse; today 20×. CMB-S4/LiteBIRD forecasts are the thing to watch.

Control: `--param ns_obs=0.99` must redden `K3-ns` and `K3-2/9` and nothing else.

### F286 — second-scale classification (K3, K12)

| Leg | Criterion | Now |
|---|---|---|
| `K3-log` | the log class predicts $dn_s/d\ln k=-2.6165\times10^{-4}$; require within 3 σ of measured | 1.24 σ ✓ |
| `K3-classes` | both classes consistent **and** unseparated — the same statement as `K3-sep`, from the other side | ✓ |

Note the sign flip worth recording: Planck 2018 preferred $\alpha_s=-0.0045\pm0.0067$; the current
baseline ΛCDM+running fit is $+0.0062\pm0.0052$ (P-ACT-LB). The module's hardcoded value has the
**wrong sign** relative to current data. Neither class is threatened — both predictions are ≈0 — but
the comparator is stale.

### F296 — holographic anomalous dimension (K3)

| Leg | Criterion | Now |
|---|---|---|
| `K3-r` | the holographic route's $r$ **must stay excluded**: require $r^{\text{pred}}/r^{\text{limit}}_{95\%}>1$ | 9.0–26.9× over BK18's 0.036 → **9.5–28.5× over 0.034** ✓ |

This is a no-go leg, so the criterion is an *exclusion that must hold*. It goes red if the limit ever
rises to admit the prediction, which is the correct failure mode for a finding whose content is
"this route is closed". Tightening 0.036 → 0.034 strengthens it.

### F285 — initial-condition measure (K5, K12)

| Leg | Criterion | Now |
|---|---|---|
| `K5-ns1` | $n_s=1$ is excluded by the data the finding invokes; require the exclusion in σ to exceed its claimed 8.4 σ | at $0.9682\pm0.0032$: $(1-0.9682)/0.0032=$ **9.9 σ**; at +DESI, 9.4 σ ✓ |
| `K12-nongeneric` | the required non-genericity ($10^{-56}$ vs white noise at the pivot; $\sim2\times10^{6}$ enhanced at the PBH scale) is a computed ratio — assert both signs and orders | internal, no data needed |
| `K5-As` | $A_s$ is a declared free input, not a prediction — assert the record makes **no** claim on it | guards against a future session quietly fitting it |

F285's 8.4 σ was computed against Planck; live data makes it **stronger**, not weaker. Good news that
should still be mechanised, because the number in the finding is now wrong in the safe direction and
nothing would notice if it went the other way.

### F283 — elastic-lattice / no-slow-roll (K4)

**The one that needs no observational data at all.** Its content is exact and internal:

| Leg | Criterion |
|---|---|
| `K4-cutoff` | $a/\ell_{\text{red}}=3^{1/4}$ **exactly** (rational/sympy, tol 0) |
| `K4-fbound` | every compact CA direction has $M_{\text{Pl}}^2/f^2\ge\sqrt3$ — an inequality over the enumerated directions |
| `K4-invariance` | $\partial r/\partial s\equiv0$, the obstruction's invariance under $a\to sa$ — a literal zero |

Three exact assertions, no threshold, no judgement. F283 is the cheapest of the five and should be
done first for that reason.

---

## 2. What this does and does not settle

**Settled without your input:** the *form* of every criterion above — a published central value, its
published σ, and a 3 σ band. The only convention is "3", and it is the convention already in use
(F297 quoted −0.11 σ and −1.8 σ as passes and 36.6 σ as an exclusion).

**Still yours:** (a) whether 3 σ is the right band, or 2 σ, or per-row; (b) **which dataset row is
canonical** — CMB-only or CMB+BAO — and this is not cosmetic, it is the difference between F295
sitting at 1.1 σ and at 2.8 σ; (c) whether F295's γ should stay *fitted* (`gamma_from_data`) or be
re-stated as the $1/(9\pi)$ prediction it implies, which is a claim-card question.

**One structural recommendation.** Do not put these numbers in the drivers. Register them once as
`MeasuredConstant`s with dataset provenance and let all five records read them. Five modules each
hardcoding their own Planck 2018 copy is how a bullseye became a 2.8 σ tension without a single check
going red.

---

## Sources

- Balkenhol et al., *Inflation at the End of 2025: Constraints on $r$ and $n_s$* — $n_s=0.9682\pm0.0032$ (Planck PR3/PR4 + SPT-3G D1 + ACT DR6 + BK), $n_s=0.9728\pm0.0029$ (+DESI DR2), $r<0.034$ / $r<0.035$ (95 %). https://arxiv.org/pdf/2512.10613
- ACT DR6 extended-model paper — baseline ΛCDM+running: $dn_s/d\ln k=0.0062\pm0.0052$ (P-ACT-LB), $0.0060\pm0.0055$ (P-ACT). https://act.princeton.edu/sites/g/files/toruqf1171/files/documents/act_dr6_extended.pdf
- Component values quoted by Balkenhol et al. from Camphuis et al. (2025): Planck alone $0.9657\pm0.0040$; ACT DR6 alone $0.9682\pm0.0069$; SPT-3G D1 alone $0.951\pm0.011$.
- In-repo comparators, currently hardcoded: `cosmology_anomalous_dimension.py:110-111`.
