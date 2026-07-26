# Applied Note 1 — Ionocraft / Asymmetric-Capacitor Thrust in the Lattice EM Sector: Efficiency Formulas, Optimal Design, and the Vacuum Prediction

**B. Ludwig**
*Independent researcher*

*Applied note to the "A Universe in a Bottle" series. This is not a core paper (I–XI); it is an engineering application of the electromagnetic sector (Paper IV) to electrohydrodynamic (EHD) propulsion. Created 2026-07-02 - 22:35.*

---

## Abstract

The ionocraft ("lifter", asymmetric-capacitor thruster, Biefeld–Brown device) is fully contained in the electromagnetic sector of the lattice model (Paper IV): its thrust is the reaction to an **ion-wind momentum-transfer chain**, and no coupling to the gravity sector (Paper VII, source $T^{00}$, F106) is present or predicted. Because the EM sector reproduces classical Maxwell electrodynamics exactly at accessible scales, the lattice inherits — and does not tighten — the standard EHD engineering relations. We record the working formulas, the exact efficiency ratio, the optimal-design rule, and a worked efficiency table grounded in air at sea level. We separate cleanly what is **computable from air constants alone** (the thrust-to-power ratio and the optimal geometry) from what **requires an empirical current input** (absolute thrust in newtons). Finally we state the model's falsifiable vacuum prediction — zero net steady-DC thrust in true vacuum — and show it agrees with the experimental record (Talley 1988; Tajmar 2004; NASA/Canning 2004; Tajmar et al. 2024).

---

## 1. Where the device sits in the model

The lift is a four-step momentum-transfer chain, every step of which is ordinary charged-particle electromagnetism already derived in Paper IV:

1. **Field ionisation / corona.** The sharp emitter produces a very high local $|\mathbf E|$ (Coulomb tail of $U(1)$ charge). Above the corona-onset field it strips electrons from neutral air molecules.
2. **Ion acceleration.** Freed ions feel the Lorentz force — the $U(1)$ minimal-coupling term the identity channel forces (Paper IV; F68).
3. **Momentum transfer ("ion wind").** Drifting ions collide with neutral air molecules and dump momentum into the bulk gas.
4. **Reaction thrust.** The reaction on the electrode structure is the measured force.

The electrostatic forces between the two electrodes are **internal**; they sum to zero on the isolated device by momentum conservation, which the EM sector enforces exactly. Thrust exists **only** because momentum is exported to the neutral gas. This is the entire physical content and it fixes the vacuum prediction in §6.

---

## 2. Working formulas (air at sea level)

Let $V$ be the applied voltage, $d$ the emitter–collector gap, $I$ the corona current, $\mu$ the ion mobility of the drift gas, and $g$ standard gravity.

**Ion mobility (the one dominant empirical constant).** For positive ions in dry air at sea level,
$$
\mu \approx 2.0\times10^{-4}\ \mathrm{m^2\,V^{-1}\,s^{-1}}
\qquad(\text{literature range } 1.4\text{–}2.7\times10^{-4}).
$$

**Thrust (momentum-transfer law).**
$$
F \;=\; \frac{I\,d}{\mu}.
\tag{2.1}
$$
Thrust scales with gap and current and is **independent of voltage at fixed current**.

**Electrical power.**
$$
P \;=\; I\,V.
\tag{2.2}
$$

**Thrust-to-power ratio (the exact efficiency figure).**
$$
\boxed{\ \frac{F}{P} \;=\; \frac{d}{\mu\,V}\ }
\tag{2.3}
$$
This depends only on gap and voltage (and the gas constant $\mu$) — no geometry fit required.

**Lifted mass.** $m = F/g$.

**Corona-onset field (Peek's law), sets the minimum useful voltage.** For an emitter of radius $r$ and relative air density $\delta$ ($\delta\approx1$ at sea level),
$$
E_\text{onset} \;\approx\; 3.0\times10^{6}\,\delta\left(1 + \frac{0.03}{\sqrt{\delta\,r}}\right)\ \mathrm{V\,m^{-1}}\quad(r\ \text{in m}),
\tag{2.4}
$$
and corona begins when the local emitter field $\sim V/[\,r\ln(d/r)\,]$ reaches $E_\text{onset}$.

**Current — the one geometry-dependent input.** Corona current follows a Townsend quadratic
$$
I \;=\; C\,V\,(V - V_0),
\tag{2.5}
$$
with onset voltage $V_0$ and a geometry coefficient $C$ (emitter radius, gap, wire length). $C$ and $V_0$ must be taken from **one measured $I$–$V$ point** on the actual device, or estimated from Peek/space-charge modelling (good to $\sim\!\times2$).

**Space-charge upper bound (planar Mott–Gurney), sanity-check only.**
$$
J_\text{SCLC} \;=\; \frac{9}{8}\,\varepsilon_0\,\mu\,\frac{V^2}{d^3}\quad[\mathrm{A\,m^{-2}}].
\tag{2.6}
$$

---

## 3. The exact efficiency figure and the optimal-design rule

Equation (2.3) is the whole optimisation. Since $F/P \propto d/V$:

- **Operate just above corona onset (minimum $V$).** Every excess volt lowers $F/P$. The floor is set by $E_\text{onset}$ (§2.4): you cannot drop $V$ below what sustains saturated corona ($\sim\!3$ kV cm$^{-1}$ order in the gap).
- **Maximise the gap $d$.** Both $F$ (2.1) and $F/P$ (2.3) grow with $d$; the ceiling is gap breakdown (arc-over).
- **Sharpest emitter, smooth large collector.** Small emitter radius $r$ lowers $E_\text{onset}$ (2.4), letting you satisfy the low-$V$ rule; the large smooth collector prevents a counter-corona.
- **Low-mobility drift gas** (if the medium is a design variable): smaller $\mu$ raises thrust per unit current (2.1). Not available in open air.

The optimum is therefore the **largest gap and lowest voltage that still sustains a stable saturated corona without arc-over**, driven from the sharpest practical emitter.

---

## 4. Worked efficiency table (air, sea level, $\mu = 2.0\times10^{-4}$)

Thrust-to-power from (2.3); field column $=V/d$ (mean gap field).

| Voltage | Gap | Mean field | Thrust / Power |
|--------:|----:|-----------:|---------------:|
| 30 kV | 3 cm | 10 kV/cm | 5.0 N/kW |
| 30 kV | 5 cm | 6 kV/cm | 8.3 N/kW |
| 20 kV | 3 cm | 6.7 kV/cm | 7.5 N/kW |
| 40 kV | 5 cm | 8 kV/cm | 6.2 N/kW |
| 10 kV | 3 cm | 3.3 kV/cm | 15 N/kW |

These fall in the measured band for real lifters and the MIT ion-wind aircraft ($\sim$few to tens of N/kW) and confirm §3: efficiency rises as $V$ falls and $d$ grows, bounded below by the corona-sustain field.

**Absolute thrust** needs the current (2.5). Worked point at 30 kV, 3 cm gap:

| Current | Thrust | Lifted mass | Power | Thrust/Power |
|--------:|-------:|------------:|------:|-------------:|
| 0.2 mA | 30 mN | 3.1 g | 6 W | 5.0 N/kW |
| 0.5 mA | 75 mN | 7.6 g | 15 W | 5.0 N/kW |
| 1.0 mA | 150 mN | 15.3 g | 30 W | 5.0 N/kW |

(The Mott–Gurney planar bound (2.6) gives $J\approx66$ mA m$^{-2}$ and $\sim10$ N m$^{-2}$ thrust density at 30 kV/3 cm, bracketing these correctly.)

---

## 5. Honesty boundary (what the lattice does and does not add)

Everything above is the EM/EHD sector, which the lattice reproduces **identically** to classical electrodynamics at these scales. The lattice therefore:

- **gives, exactly:** the efficiency ratio $F/P=d/\mu V$ and the optimal-geometry rule (§3), from air constants alone;
- **does not tighten:** absolute thrust, because the missing inputs — $\mu$, corona onset, and the Townsend coefficient $C$ — are **continuum gas-kinetics quantities, not lattice-derived**. There is no lattice knob that predicts them from first principles.

This is the same boundary noted for all applied-EM problems: the model wins on mechanism and structure, not on empirical transport constants.

---

## 6. Vacuum prediction and the experimental record

**Model prediction (falsifiable).** In true vacuum under steady DC, the momentum-transfer chain (§1) has no neutral gas to ionise (no carriers) and no neutral reservoir to receive momentum. The inter-electrode forces are internal and cancel. Therefore the model predicts **zero net steady-DC thrust in high vacuum**. Because gravity is sourced by stress-energy $T^{00}$ (Paper VII; F106) and a lifter warps no metric, the "electrogravitic / anti-gravity" interpretation is **excluded**, not merely unsupported.

**Experimental record (consistent):**

- **Talley (1988/1990, USAF):** Brown-type electrodes at $10^{-6}$ torr under steady DC — **no thrust**; force appeared only during electrical breakdown (current flowing).
- **Tajmar (2004, AIAA J. 42(2) 315):** enclosing the electrodes to exclude corona wind removed the linear thrust — Biefeld–Brown effect is **misinterpreted corona wind**.
- **NASA / Canning, Melcher & Winet (2004):** force attributed to ion wind.
- **Tajmar, Kößling & Neunzig (2024, *Sci. Rep.* 14:19427):** high-sensitivity dedicated search for any gravity–EM coupling with steady fields — **no anomalous force**.

Occasional "positive" vacuum reports correlate with breakdown currents, outgassing, or very high voltages (residual ionisation), i.e. the chain of §1 re-established by a trace medium — not a propellantless force. The record thus **confirms** the model's prediction.

---

## 7. References

- T. B. Bahder & C. Fazi, *Force on an Asymmetric Capacitor*, US Army Research Laboratory (2003).
- R. L. Talley, *Twenty-First Century Propulsion Concept*, PL-TR-91-3009, DTIC (1990).
- M. Tajmar, *Biefeld–Brown Effect: Misinterpretation of Corona Wind Phenomena*, AIAA Journal **42**(2), 315–318 (2004).
- F. X. Canning, C. Melcher & E. Winet, *Asymmetrical Capacitors for Propulsion*, NASA CR-2004-213312 (2004).
- M. Tajmar, M. Kößling & O. Neunzig, *In-depth experimental search for a coupling between gravity and electromagnetism with steady fields*, Scientific Reports **14**, 19427 (2024).
- E. D. Fylladitakis, M. P. Theodoridis & A. X. Moronis, *Review on the History, Research, and Applications of Electrohydrodynamics*, IEEE Trans. Plasma Sci. **42**(2), 358–375 (2014).

---

*Companion tool: `papers/tools/ehd-lifter-calculator.html` — enter voltage, gap, and electrode sizes to get thrust, power, efficiency, and required current, using the formulas of §2.*
