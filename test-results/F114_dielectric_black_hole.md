# F114 — The dielectric black hole (2026-06-08 - 20:41)

Exponential metric n=K=e^{2u}, A=1/K, B=K (units GM/c^2). **9/9 checks PASS.**

| feature | tier | dielectric model | Schwarzschild | verdict | ok |
|---|---|---|---|---|---|
| event horizon | PREDICTION | NONE (g_tt=-e^{-2u} has no finite root; local c=e^{-2u}->0 only at r->0) | horizon at R=2 | horizon-free: asymptotic freeze, no one-way membrane | PASS |
| throat (min areal radius) | PREDICTION | R_min = E = 2.7183 GM/c^2 at isotropic r=1 | (no analogue; horizon at 2) | areal radius bottoms out just outside the Schwarzschild radius | PASS |
| photon sphere | PREDICTION | R_ph = 2*exp(1/2) = 3.2974 GM/c^2 (isotropic r=2) | R_ph = 3 GM/c^2 | +9.9% vs GR | PASS |
| shadow impact parameter b_c | PREDICTION | b_c = 2*E = 5.4366 GM/c^2 | 3*sqrt3 = 5.1962 GM/c^2 | +4.63% larger shadow | PASS |
| surface redshift at throat | PREDICTION | 1+z = E = 2.7183 (finite; z=1.718) | 1+z -> infinity at horizon | finite at the throat; diverges only as r->0 (no infinite-redshift surface) | PASS |
| 2nd-order deflection coefficient | PREDICTION | alpha_2 = 4*pi = 4*pi (exponential index sigma=2) | 15*pi/4 (Schwarzschild sigma=7/4) | excess = pi/4 per eps^2 (bends more) | PASS |
| EHT shadow — M87* | FALSIFIER | 41.5 uas (lattice) | 39.7 uas (GR) | +4.63%; ring meas 42+/-3 uas | PASS |
| EHT shadow — Sgr A* | FALSIFIER | 55.7 uas (lattice) | 53.3 uas (GR) | +4.63%; ring meas 52+/-2 uas | PASS |
| GW ringdown echoes | PREDICTION | echoes present (no horizon to absorb the ringdown) | no echoes (horizon absorbs) | horizonless object reflects -> late-time GW echoes (LIGO/Virgo target) | PASS |

## EHT shadow numbers

| source | theta_g (uas) | GR shadow | lattice shadow | enlargement | measured ring |
|---|---|---|---|---|---|
| M87* | 3.819 | 39.7 uas | 41.5 uas | +4.63% | 42+/-3 uas |
| Sgr A* | 5.124 | 53.3 uas | 55.7 uas | +4.63% | 52+/-2 uas |
