# Appendix A3 — Constants Ledger and the Free-Parameter Count

*Every registered constant (`src/casim/constants/`) the monograph's 26 chapter files actually use,
cross-referenced against its registered closed form, cross-checked against `docs/monograph/A4-open-residuals.md`
§A4.2's provisional free-parameter list, and reconciled explicitly rather than silently replaced. Per
CLAUDE.md decision D7, values that numerically coincide but arise from different sectors are kept as
distinct registered constants throughout this table — most visibly the three separate $2/9$'s
($\delta^*$, $\sin^2\theta_W^\text{on-shell}$, $c_\text{Fierz}^\text{colour}$) and the two $1/\sqrt3$'s
($c_\text{lat}$, a momentum scale elsewhere) — never merged.*

**Categories used throughout** (per the build brief): **derived** (follows from more primitive
structure with zero free choice, given the postulates already adopted), **anchored** (one external
measured number sets its scale, with everything else following), **fitted** (tuned to or read from
data with no independent derivation, and — per chapters 14/16/21/22's own explicit findings — in
several cases *proven* not to be derivable by any mechanism currently in the tree, not merely
unfinished), and **conventional** (a choice among equally valid options, e.g. a normalization or
labelling convention, carrying no physical content).

---

## A3.1 Lattice geometry and kinematics (Chapters 1–7, structural)

| Symbol | Closed form | Float value | Exactness | Provenance (Ch./F#) | Category |
|---|---|---|---|---|---|
| $d$ | spatial dimension, forced | $3$ | exact | Ch.2, F291/F292 | **derived** |
| $s$ | minimal spinor cell dimension | $2$ | exact (imported BDPT theorem, not re-derived) | Ch.2 §2.1 | **derived**, conditional on the imported $s=2$ minimality premise |
| $a$ (native) | BCC cube edge in lattice-native units | $2/\sqrt3=2c_\text{lat}$ | exact | Ch.2, F278 (`c_lat`) | **derived** |
| $c_\text{lat}$ | $d\Omega/d\lvert\mathbf k\rvert\rvert_0$ | $1/\sqrt3=0.5773502692$ | exact | Ch.6, F26 (registered `c_lat`) | **derived** |
| $\hat{\mathbf n}(\mathbf k)$, dispersion coefficients | closed forms (R6.8, R6.13, R7.11) | — | exact | Ch.6/7, F26b/F246/F319 | **derived** |
| $O_h$, $D_{2h}$, $D_{4h}$ | point-group content of the walk | — | exact | Ch.2, F344 | **derived** |
| $R_3$ / rest-mass slope-intercept identity | $\Omega_\text{Dirac}(\mathbf k,m)$ | — | exact | Ch.11, F167 | **derived** |
| $a/\ell_P$ | $\sqrt{8\pi}\,3^{1/4}$ | $6.59782$ | exact (registered `a_over_ellP`) | Ch.18, F79/F107 | **derived**, given $G$ as the anchor that converts it to metres — see A3.6 |

## A3.2 Electroweak sector (Chapter 12)

| Symbol | Closed form | Float value | Exactness | Provenance | Category |
|---|---|---|---|---|---|
| $\sin^2\theta_W^\text{UV}$ | $1/4$ (registered `sin2_thetaW_uv`) | $0.25$ | exact rational | F45/F231 | **derived** (bare $\sigma\!\leftrightarrow\!\tau$ swap counting; MS-bar cap at $\mu_\star=4\pi v$) |
| $\sin^2\theta_W^\text{on-shell}$ | $2/9$ (registered `sin2_thetaW_onshell`) | $0.2222\overline2$ | exact rational | F49/F138/F141/F231 | **derived** — **deliberately distinct from $\delta^*$ and $c_\text{Fierz}^\text{colour}$ (D7)** despite the identical fraction |
| $u$ | stiffness quantum, $18\pi\alpha/7$ | — | exact given $\alpha_\text{em}$ | F320 | **derived**, conditional on hypothesis (U) (unproven, §A4.1) |
| $m_W$, $m_Z$ | $\tfrac{3v}2\sqrt{2\pi\alpha}$, $\tfrac{9v}2\sqrt{2\pi\alpha/7}$ | $79.08$, $89.67$ GeV (tree) | exact form, given $\{v,\alpha\}$ | F320 | **derived**, given the two anchors $v,\alpha_\text{em}$ |
| $\rho\equiv m_W^2/(m_Z^2\cos^2\theta_W)$ | $1$, exactly for every $u$ | $1$ | exact | F320 | **derived** |
| $Y_L,Y_e,Y_\nu$ | hypercharge ratios $4:{-2}:{-3}:{-6}:0$ | — | exact rational | F165/F279 (`Y_LEPTON_L` etc.) | **derived** ratios; the overall normalization ($Y_L=-1$ specifically, vs. $-2,-1/2,\ldots$) is a **conventional** SM-labelling choice, not physical content (Ch.12 §12.2.13) |

## A3.3 Strong sector (Chapters 13a/13b, 14)

| Symbol | Closed form | Float value | Exactness | Provenance | Category |
|---|---|---|---|---|---|
| $N_c$ | number of colours | $3$ | bracketed to $\{3,5,7,\ldots\}$; $3$ selected only empirically | F293/F324/F325/F338 | **anchored** (empirically selected by a 28-decade confinement-scale lever; not derived to the specific integer) |
| $c_\text{Fierz}^\text{colour}$ | $2/9$ (Fraction, registered `c_fierz_colour`) | $0.2222\overline2$ | exact rational | F77/F116/F256 | **derived** — the third, independent $2/9$ (D7) |
| $g_s(\mu_0)$ | $1/2$ | $0.5$ | derived, conditional on two inherited normalization choices | F144 | **derived**, not zero-knob (§13b.2.1) |
| $\alpha_s(\mu_0)$ | $1/(16\pi)$ | $0.019894$ | exact given $g_s$ | F144 | **derived** |
| $a_1(n_f{=}6)$ | $11/3$ | $3.6\overline6$ | exact rational | F151 | **derived** |
| $q_\ast$ / $d_1$ (equiv. $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$) | bracketed $[1,7.98]$ (registered `q_star_a_band_lo`/`q_star_a_implied`) | native-run extrapolation $\approx31$–$34$, **outside** the bracket | genuinely open | F280/F337/F350 (Gap G-11) | **fitted** — the single largest unresolved open number in the strong sector; NOT derived, and the native computation has not yet converged inside its own tadpole-free bracket |
| $\alpha_\text{eff}^\ast$ | IR frozen coupling | $\approx0.39$ | bracketed (registered `alpha_eff_star`) | F151/F152/F154 | **derived**, given the same open $q_\ast$ this constant is downstream of |
| $\beta_t/\beta_s$ | lattice anisotropy | $4$ | exact | F323 | **derived** |
| $f_\pi$ | QCD-scale anchor | $92.07$ MeV (registered `f_pi_anchor_MeV`) | external | F77/F123 | **anchored** — the model's one hadron-sector dimensionful anchor |
| $\Lambda_\text{NJL}$ | BZ edge | $651.5$ MeV | mechanistically identified as the BZ edge, not a free cutoff (F116) | F77/F116 | **derived** (the cutoff itself), but the coupling $G\Lambda^2=2.10$ riding on it is **anchored/fitted** — not pinned to a digit (Ch.14 §14.9) |
| $m_0$ (current quark mass, NJL) | — | $5.5$ MeV | external | F77/F116 | **fitted** — flagged forward to the same lepton-style texture machinery Ch.15 built, never completed for quarks |
| $\sqrt\sigma$ | string tension (via $\sqrt\sigma/f_\pi$) | $0.42$ GeV anchor | derived given $f_\pi$; the $+12\%$ residual is not removable (F235) | F86/F88/F235 | **derived**, with an honestly disclosed, non-removable $+12\%$ systematic (compounded by the F146 pre-BCC action caveat, Ch.14/17) |
| $g_\text{cm}$ | colour-magnetic (N–$\Delta$) coupling | $18.31$ MeV | external, reused not new | F113 (Ch.14) | **anchored** (fixed by the measured $N$–$\Delta$ splitting) |
| Up/down/strange/charm/bottom/top masses | — | PDG values consumed as-is | **no derived shape mechanism** — F346/F347 show the Ch.15 weight-as-phase construction does not transplant to quarks (decisive for up-type, unresolved-but-unconfirmed for down-type) | F346, F347 | **fitted** — six genuinely free numbers (or five ratios + one scale), a distinct free-parameter bucket from the anchors above |
| $b$ (OBE quark cluster size) | — | $0.55$ fm | cross-checked to $5.5\%$ against an independent gauge-sector prediction $R_\text{conf}$, not eliminated | F373 (Ch.14) | **fitted**, with a genuine (not decisive) independent consistency check |
| $g_{\omega NN}^2/4\pi$ | — | $5.39$ (NN-fit value) | **proven not derivable** at the static-OBE level, for two independent stated reasons (a real $\rho NN$-universality vertex-renormalization effect, and an exact algebraic degeneracy with the quark-Pauli core strength) | F240/F247 (Ch.14) | **fitted**, explicitly disclosed as a genuine free input, not an unfinished calculation |

## A3.4 Lepton sector (Chapter 15)

| Symbol | Closed form | Float value | Exactness | Provenance | Category |
|---|---|---|---|---|---|
| $\delta^*$ | $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=2/9$ rad (registered `delta_star`) | $0.2222\overline2$ rad | exact rational, **adopted as a founding principle** (weight-as-phase) | F175/F253/F255/F256 | **derived**, in the specific sense that every dynamical alternative producing the same number is proved closed (§A1.51); the *identification* of the weight with a radian is the one adopted principle, not itself derivable |
| $\eta^2$ | $\sin^2t^*=1/2$ at $t^*=45°$ | $0.5$ | exact, derived four independent ways given the Cooper-pair premise | F92/F81/F82/F109 | **derived**, conditional on the Cooper-pair mass-generation premise inherited from Ch.11 |
| $\lambda_6$ | $C/e^6=0.636\lvert B\rvert/e^6$ | $0.243$ | exact given $\delta^*$ and the derived cubic $B$ (registered `lambda_6`) | F234 | **derived** — an *output* of $\delta^*$, not an independent input (supersedes F179's "one-angle fit" reading) |
| $W^*=6\lambda_6$ | — | $1.458$ | exact given $\lambda_6$ | F101b/F108/F118/F234 | **derived** |
| $m_\mu/m_e$, $m_\tau/m_e$ | shape formula in $\{\delta^*,\eta^2\}$ | $206.770$, $3477.47$ | $+0.001\%$, $+0.007\%$ vs. PDG | F175/F234 | **derived**, zero shape parameters |
| $N\equiv m_\text{lat}(\tau)$ (overall lepton mass scale) | — | $5.54\times10^{-19}$ (dimensionless) | **argued** (not proven) to be QCD-transmutation-generated to a factor $\approx1.9$ (F233); genuinely anchored via $m_\tau$ | F119/F233 (Ch.17) | **anchored** — the model's lepton-sector overall-scale anchor (equivalently $m_\tau$); F233's transmutation argument narrows, but does not eliminate, its status as an external input |

## A3.5 Neutrino sector (Chapter 16)

| Symbol | Closed form | Float value | Exactness | Provenance | Category |
|---|---|---|---|---|---|
| $M_R$ / $M_{R0}$ (absolute Majorana scale) | — | model-dependent, e.g. $\sim1$ GeV ($\nu$MSM benchmark) or $10^{12}$–$10^{15}$ GeV (heavy see-saw benchmark) | **proven not fixed by anything in the model**, on three independently checked legs (no registered dimensionless ratio's small power lands near the required suppression; the $E_g$ texture provably factors $M_{R0}$ out identically; $\nu_R$'s total-singlet status forecloses the model's only dynamical scale-generating mechanism) | F343 | **fitted** — a genuinely free scale, not merely unfitted |
| $\theta_{12},\theta_{13},\theta_{23}$ (PMNS angles) | — | fit to NuFIT-5.2 | **proven** no residual-symmetry or equipartition selector can exist (an exact group-theory theorem: the three $T_{2g}$ amplitudes transform as inequivalent 1-d irreps of $D_{2h}$) | F236/F254 | **fitted** — three genuinely free numbers, proven so |
| $\delta_{CP}$ | — | fit | identical no-go, extended formally to the phase content | F353 | **fitted** |
| $\delta_\nu$ (neutrino $E_g$ condensate angle) | — | free | argued (not derived) to share the charged-lepton texture *form*, not its value | F201/F236 | **fitted** |

## A3.6 Gravity and cosmology (Chapters 17–21)

| Symbol | Closed form | Float value | Exactness | Provenance | Category |
|---|---|---|---|---|---|
| $G$ (equivalently $\ell_P$) | $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ | $6.6743\times10^{-11}$ m$^3$kg$^{-1}$s$^{-2}$ (registered `G_LATTICE`, CODATA compared as `G_CODATA`) | ratio derived exactly; the absolute SI anchor is external | F79/F107 | **anchored** — the model's one gravity-sector anchor (any theory needs one length/mass/time anchor; the model's own contribution is that the *ratio* $a/\ell_P$ is parameter-free) |
| $\alpha_\text{em}$ | — | $1/137.036$ (CODATA) | **proven** not derivable by any of four checked avenues (Sakharov induction, an $O(1)$ scale coincidence, topology/anomaly cancellation, structural normalization); two concrete but unattempted reopening routes named | F127/F339/F349 | **anchored** — "the model's last irreducible dimensionless input" (Ch.9's own words) |
| $v$ (electroweak scale, equiv. $G_F$) | — | $246.22$ GeV | not forced by $G$ (mechanical type-check); loop-induction checked and found negligible ($\le0.36\%$); dynamical transmutation is live but **unproven** specifically for $v$ | F351 | **anchored**, with a disclosed, plausible-but-unconfirmed collapse into the same $d_1$ residual as $N$ and $\lambda_6$ |
| $\Omega_\Lambda$ (equiv. $\Omega_m=1-\Omega_\Lambda$) | — | $0.6847$ (Planck 2018) | the holographic sector fixes only the *ceiling* $\Omega_\Lambda\le1$ (the exponent $p=2$ is genuinely derived, F196); the coincidence-problem residual is **proven not derivable** from the same sector | F241 | **fitted** — a genuinely free cosmological number, identically the present matter fraction |
| $s_\text{cell}$ (horizon per-cell entropy) | $2\pi\sqrt3$ nats exactly | $10.883$ | fixed exactly by $S=A/4$; its *derivation* from lattice microstates is open, and disputed by a factor bracketed $[0.79,3.18]$ between two of the model's own computations (F79 heat-kernel vs. F355 entanglement) | F190/F355 | **derived** (the target value) but with an **open, disputed** first-principles derivation (§A4.1) |

## A3.7 Dark sector (Chapter 22)

| Symbol | Closed form | Float value | Exactness | Provenance | Category |
|---|---|---|---|---|---|
| $L$ (lepton asymmetry) | — | free | drives resonant sterile-neutrino production; not derived | F205 | **fitted** |
| $S$ (entropy-dilution factor) | — | free | opposite-sign scaling vs. $L$ excludes the sterile as 100% DM (F237); the model's bounded *sub-dominant* fraction still needs this number | F237 | **fitted** |
| $\mu$ (geon virial mass) | $\sqrt2\,M_\text{Pl}$ | $1.73\times10^{19}$ GeV | order-of-magnitude derived (virial argument), given the graviton-graviton binding is confirmed exact | F223 | **derived** (order of magnitude) |
| $M_\text{rem}$ (geon/PBH remnant mass) | $(\sqrt3/2)^{1/2}M_\text{Pl}$ | $\approx0.9306\,M_\text{Pl}$ | exact-algebraic (F190 horizon-cell floor + F107 canonical cell) | F228 | **derived** |
| $\beta(M_\text{form})$ (PBH collapse fraction) | — | $\sim10^{-15}$–$10^{-9}$ needed | **proven not derivable**: traces to a required primordial curvature amplitude $\sim2\times10^6\times$ the measured CMB amplitude, and the model has (and per F282, structurally cannot have) a standard inflaton sector to supply it | F238 | **fitted** — the geon's sole free abundance input, proven non-derivable along the standard route (a structurally distinct non-inflationary channel, F366, is open in principle but not derived) |

## A3.8 QED / atomic sector (Chapters 23–24)

Every quantity in these two chapters is a **derived** consequence of the model's fields, consuming
only $\alpha_\text{em}$ and the lepton masses (already counted in A3.6/A3.4) as external numbers —
Chapter 23's own explicit accounting. No new registered free constant is introduced by either chapter;
the two-loop QED coefficient $A_2=-0.328478966\ldots$, the Bethe logarithms, the Euler–Heisenberg
coefficients, and every ionization-energy/Lamb-shift/hyperfine number are all closed-form or
numerically-converged consequences of the vertex and propagators already fixed elsewhere. The one
partially-external number this sector still imports is the two-loop Källén–Sabry non-log constant
($\zeta(3)-5/24$, cited, not derived — F311/F336) and the hadronic-VP piece beyond $\rho+\omega$
(F334, explicitly $\sim90\%$ uncovered) — both flagged as open residuals in A4, not counted as new
free parameters since they are sub-percent corrections to already-derived leading terms, not new
scale-setting or mixing inputs.

## A3.9 Condensed matter (Chapter 25)

Every superconductivity and quantum-information result in this chapter is likewise **derived**,
given the *material-specific* inputs BCS/Eliashberg theory itself always needs ($N(0)V$, equivalently
$\lambda,\omega_\text{log}$, per real element) — these are not new model free parameters in the sense
of A3.1–A3.7; they are the same kind of per-material input every microscopic theory of superconductivity
requires, here shown to arise from the model's own $F64$ dielectric (the deformation potential
$D=\tfrac23E_F$) and Thomas–Fermi screening ($\mu^*(r_s)$), with **zero new fitted constants**
introduced beyond one disclosed, explicitly-left-open item: tantalum's DOS enhancement factor $\alpha_\text{Ta}$
(F375, deliberately not estimated by analogy).

---

## A3.10 The free-parameter count — reconciled against A4 §A4.2

**A4's own provisional list** (`docs/monograph/A4-open-residuals.md` §A4.2) states: *"today the model
uses at minimum $\{G, f_\pi, m_\tau\text{ (or }N\text{)}, v\}$ as independent dimensionful external
anchors (Ch.17), plus the still-external $\alpha_\text{em}$ (Ch.9's four-avenue no-go) and the
per-flavor fermion mass magnitudes (Ch.11). Chapter 17's own synthesis flags an unconfirmed case that
three of these collapse to one shared constant $d_1$ — which would cut the count from four to two if
the Ch.13b non-convergence resolves in its favor."*

**This is correct as far as it goes, and this appendix's own count agrees with it exactly on the five
items A4 names explicitly** ($G$, $f_\pi$, $m_\tau/N$, $v$, $\alpha_\text{em}$) — see A3.3/A3.4/A3.6
above, all independently confirmed as anchored, not derived, reading each chapter's own text directly
rather than trusting A4's summary. **Where this appendix's count is larger is not a disagreement with
A4 — it is a reconciliation of A4's own admittedly compressed phrase "the per-flavor fermion mass
magnitudes," plus items several chapters read *after* A4 was drafted (Chapters 16, 20–22, and 14's own
NN-potential material) that are not fermion masses at all and so were never going to be captured by
that phrase.** Naming them explicitly, by sector, rather than leaving them folded into a vague catch-all:

| Bucket | Count | What it actually is | Not a fermion mass because |
|---|---|---|---|
| The five scale/coupling anchors A4 names | **5** | $G$, $f_\pi$, $m_\tau(N)$, $v$, $\alpha_\text{em}$ | — (A4's own list) |
| Quark mass texture | **6** (or 5 ratios + 1 scale) | up, down, strange, charm, bottom, top | this *is* what A4's phrase covers — the one bucket genuinely subsumed by "per-flavor fermion mass magnitudes" |
| PMNS mixing | **4** | $\theta_{12},\theta_{13},\theta_{23},\delta_{CP}$ | mixing angles/phases, not masses — proven (not merely unfitted) free, F254/F353 |
| Absolute Majorana scale | **1** | $M_{R0}$ | an overall mass *scale*, arguably fermion-mass-adjacent, but proven free on three independent structural legs distinct from the ordinary "magnitude not yet derived" framing A4's phrase implies — F343 |
| NN one-boson-exchange coupling | **1** | $g_{\omega NN}^2/4\pi$ | a meson-nucleon coupling constant, not a fermion mass — proven free, F247 |
| Strong-sector scheme-matching constant | **1** | $d_1$ (equiv. $q_\ast$) | a lattice-to-continuum renormalization constant — the one item A4 itself already flags as live and unresolved |
| Cosmological coincidence | **1** | $\Omega_\Lambda$ (equiv. $\Omega_m$) | a cosmological density fraction, not a particle-physics input at all — proven free, F241 |
| Dark-sector abundance | **2–3** | $L$, $S$ (sterile neutrino); $\beta(M_\text{form})$ (geon) | production-history/initial-condition parameters, not fermion masses — both proven free by distinct mechanisms, F237/F238 |

**Reconciled total: $5+6+4+1+1+1+1+(2\text{–}3)=21$–$22$ genuinely free (anchored or fitted) numbers**,
against A4's compressed "four dimensionful anchors + $\alpha_\text{em}$ + an unspecified number of
fermion masses." **The two counts do not actually disagree** — A4's own text is explicit that its list
is a floor ("at minimum") and that "the per-flavor fermion mass magnitudes" is a placeholder phrase,
not a completed enumeration; this appendix supplies the completed enumeration A4's own §A4.2 called
for but, being written earlier in the build, could not yet perform, since the neutrino (16), cosmology/
dark-sector (20–22), and NN-potential (14) chapters that name most of the additional items were read
after A4 was drafted (per `00-plan.md`'s own build order, Chapter 14 predates A4 while 16/20–22 are
concurrent-or-later). **Both numbers are honest for what they measure**: A4's "four, plus $\alpha$,
plus fermion masses" is the correct floor if one restricts to Chapter 17's own scale-setting question;
this appendix's $\sim21$ is the correct count if one asks, monograph-wide, "how many numbers does this
model need from measurement, in total, that are not conventions and not derived." Neither number is
wrong; they answer different, adjacent questions, and this appendix states which one it is answering.

**One further honest caveat, stated because CLAUDE.md's own elegant-design stance (P7) makes it
tempting to round this down prematurely**: several of the $\sim21$ items are *argued* (not yet proven)
to collapse onto one another — most concretely, $d_1$ is argued to be the shared residual behind
$N$'s transmutation factor, the $\lambda_6$ derivation's own completion couplings, and possibly $v$'s
residual (Ch.17 §17.2.6/§17.2.9) — a documented, **not-yet-confirmed** reduction path that, if it were
established, would remove roughly 2–3 of the 21 as independently-countable (folding $N$'s residual,
part of $v$'s residual, and the strong-sector $d_1$ itself into one number). This appendix reports the
current, unreduced count as the honest state of the model today, exactly as Chapter 17 itself insists
on reporting "four in current practice," not the hoped-for two.

---

## A3.11 Deliberately-preserved numerical coincidences (CLAUDE.md decision D7)

Per the standing rule that values which numerically coincide but arise from different sectors are
different constants, never merged — confirmed directly against each sector's own registered symbol
and derivation string, not merely asserted:

| Value | Distinct registered constants | Sectors |
|---|---|---|
| $2/9$ | `delta_star` (Ch.15, lepton $E_g$ representation weight), `sin2_thetaW_onshell` (Ch.12, electroweak mass-ratio), `c_fierz_colour` (Ch.13b, strong-sector Fierz coefficient) | lepton / electroweak / strong — three independent origins, confirmed by this build's own chapter-by-chapter reading, not merely cited from CLAUDE.md |
| $1/\sqrt3$ | `c_lat` (the lattice speed of light, a rotation rate) and a momentum-scale use flagged separately in CLAUDE.md's own D7 note (not separately re-derived by any chapter read here; carried forward as a standing instruction, not independently re-confirmed in this build) | electrodynamics / kinematics |
| $2/9$-adjacent numerology | $\delta^*/2\pi=1/(9\pi)$ vs. the primordial tilt's anomalous dimension $\gamma$ (Ch.20, F286) — checked directly against a pre-registered look-elsewhere family and found to be a $p=0.32$ coincidence, **not adopted** | lepton / cosmology — an explicit *rejected* coincidence, recorded here as the discipline's own negative control |

---

*This appendix touches only the file `docs/monograph/A3-constants.md`, per the build's own scope
restriction. Cross-checked against `src/casim/constants/geometry.py`, `gravity.py`, `lepton.py`,
`strong.py`, and `electroweak.py` directly (grepped for every `symbol=`/`exactness=`/`provenance=`
field) rather than trusting any chapter's restatement of a registered value.*
